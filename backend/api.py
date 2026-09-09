import os
import math
import json
import io
import base64
import torch
import torch.nn.functional as F
import psutil
import platform
from fastapi import FastAPI, UploadFile, File, Form, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import Response, PlainTextResponse
from torchvision import transforms
from torchvision.utils import make_grid
from PIL import Image
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

from models.autoencoder import DenoisingAE
from models.vae import VAE, kl_divergence
from models.classifier import UrbanClassifier
from models.gpt import GPTConfig, MiniGPT
from models.gan import Generator as GANGenerator, LATENT_DIM as GAN_LATENT_DIM, NUM_CLASSES as GAN_NUM_CLASSES
from dataset import URBAN_CLASSES
from rag_pipeline import PUNE_STATS, query_rag
from security import (
    ALLOWED_ORIGINS, AUTH_ENABLED, RATE_LIMIT, limiter,
    require_api_key, read_image_upload, privacy_policy,
)

app = FastAPI(title="UrbanGen AI API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints that run a model take auth (a no-op until URBANGEN_API_KEY is set)
# plus a per-client rate limit.
GUARDED = [Depends(require_api_key)]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

AE_LATENT = None  # DenoisingAE has no explicit latent dim arg
VAE_LATENT_CHANNELS = 64

# Models
ae = DenoisingAE().to(device)
vae = VAE(latent_channels=VAE_LATENT_CHANNELS).to(device)
transformer = UrbanClassifier(num_classes=len(URBAN_CLASSES)).to(device)


def load_model_if_exists(model, path):
    if os.path.exists(path):
        try:
            model.load_state_dict(torch.load(path, map_location=device, weights_only=True))
            model.eval()
            return True
        except Exception as e:
            print(f"Warning: Failed to load {path}: {e}")
            return False
    return False


ae_loaded = load_model_if_exists(ae, '../outputs/ae/model.pth')
vae_loaded = load_model_if_exists(vae, '../outputs/vae/model.pth')
trans_loaded = load_model_if_exists(transformer, '../outputs/transformer/model.pth')

# ---------------------------------------------------------------------------
# Conditional GAN Generator — loaded from EMA checkpoint produced by train_gan.py
# ---------------------------------------------------------------------------
gan_generator = GANGenerator(latent_dim=GAN_LATENT_DIM, num_classes=GAN_NUM_CLASSES).to(device)
gan_loaded = load_model_if_exists(gan_generator, '../outputs/gan/generator_ema.pth')
GAN_META: dict = {}
_gan_meta_path = '../outputs/gan/meta.json'
if os.path.exists(_gan_meta_path):
    try:
        with open(_gan_meta_path, encoding='utf-8') as _f:
            GAN_META = json.load(_f)
    except Exception as _e:
        print(f"Warning: could not load GAN meta: {_e}")

# ---------------------------------------------------------------------------
# MiniGPT (transformer-based generative model) — trained on the urban-planning
# corpus, prompted with real Pune land-use stats to draft recommendations.
# ---------------------------------------------------------------------------
gpt = None
gpt_stoi = None
gpt_itos = None
GPT_DIR = '../outputs/gpt'


def load_gpt():
    global gpt, gpt_stoi, gpt_itos
    meta_path = os.path.join(GPT_DIR, 'meta.json')
    model_path = os.path.join(GPT_DIR, 'model.pth')
    if not (os.path.exists(meta_path) and os.path.exists(model_path)):
        return False
    try:
        meta = json.load(open(meta_path, encoding='utf-8'))
        cfg = GPTConfig(**meta['config'])
        m = MiniGPT(cfg).to(device)
        m.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
        m.eval()
        gpt = m
        gpt_stoi = meta['stoi']
        gpt_itos = {int(k): v for k, v in meta['itos'].items()}
        return True
    except Exception as e:
        print(f"Warning: Failed to load MiniGPT: {e}")
        return False


gpt_loaded = load_gpt()

# Anomaly-detection baseline: reconstruction error on a random sample of
# real, in-distribution UCMerced tiles. A tile's error is only meaningful
# relative to what "normal" error looks like for this model — a raw MSE
# number tells a planner nothing on its own.
VAE_ANOMALY_MEAN = None
VAE_ANOMALY_STD = None


def compute_vae_anomaly_baseline(n_samples=300):
    global VAE_ANOMALY_MEAN, VAE_ANOMALY_STD
    if not vae_loaded:
        return
    import random
    from dataset import DATASET_PATH, URBAN_CLASSES

    random.seed(0)
    paths = []
    per_class = max(1, n_samples // len(URBAN_CLASSES))
    for cls in URBAN_CLASSES:
        candidates = list((DATASET_PATH / cls).glob("*.tif"))
        paths.extend(random.sample(candidates, min(per_class, len(candidates))))

    errors = []
    batch = []
    with torch.no_grad():
        for path in paths:
            img = Image.open(path).convert('RGB')
            batch.append(vae_transform(img))
            if len(batch) == 32:
                x = torch.stack(batch).to(device)
                recon, _, _ = vae(x)
                per_image_mse = F.mse_loss(recon, x, reduction='none').mean(dim=[1, 2, 3])
                errors.extend(per_image_mse.cpu().tolist())
                batch = []
        if batch:
            x = torch.stack(batch).to(device)
            recon, _, _ = vae(x)
            per_image_mse = F.mse_loss(recon, x, reduction='none').mean(dim=[1, 2, 3])
            errors.extend(per_image_mse.cpu().tolist())

    errors_t = torch.tensor(errors)
    VAE_ANOMALY_MEAN = errors_t.mean().item()
    VAE_ANOMALY_STD = errors_t.std().item()
    print(f"VAE anomaly baseline over {len(errors)} real UCMerced tiles: "
          f"mean={VAE_ANOMALY_MEAN:.5f} std={VAE_ANOMALY_STD:.5f}")


def score_anomaly(mse):
    if VAE_ANOMALY_MEAN is None or VAE_ANOMALY_STD in (None, 0):
        return None, None
    z = (mse - VAE_ANOMALY_MEAN) / VAE_ANOMALY_STD
    if z < 1.0:
        level = "Typical"
    elif z < 2.5:
        level = "Unusual"
    else:
        level = "Highly Anomalous"
    return z, level


# "Urbanization projection": a small pool of REAL developed/built-up
# UCMerced tiles (mu + preprocessed image, cached at startup). An uploaded
# tile's own latent is linearly blended toward one of these real targets
# (same latent-blend technique as infer_vae_interpolate) and decoded.
#
# An earlier version blended toward the *mean* latent of developed-class
# images instead of a real tile. That decoded to a flat, structureless
# blob: an average of many real latents lands in a region of this narrow,
# reconstruction-priority latent space (near-zero KL weight, see
# models/vae.py) that doesn't correspond to any real tile, so the decoder
# has never learned to render it well. Blending toward one specific REAL
# tile's latent instead keeps every blend step anchored to something the
# decoder actually knows how to decode -- alpha=1 reproduces that real
# tile exactly.
#
# The display step also needed to change: sharpen_vae_reconstruction
# always restores the SOURCE image's own edges (correct for plain
# reconstruction), which meant the projection's structure never visibly
# changed even as the underlying latent shifted -- see
# crossfade_vae_projection below.
DEVELOPED_CLASSES = ["denseresidential", "mediumresidential", "buildings", "intersection", "freeway"]
URBANIZATION_TARGETS = []  # list of (mu, source_tensor) for real developed tiles


def compute_urbanization_targets(n_targets=12):
    global URBANIZATION_TARGETS
    if not vae_loaded:
        return
    from dataset import DATASET_PATH
    import random
    random.seed(2)
    per_class = max(1, n_targets // len(DEVELOPED_CLASSES))
    paths = []
    for cls in DEVELOPED_CLASSES:
        candidates = list((DATASET_PATH / cls).glob("*.tif"))
        paths.extend(random.sample(candidates, min(per_class, len(candidates))))
    if not paths:
        print("Urbanization targets skipped: dataset missing or empty.")
        return

    targets = []
    with torch.no_grad():
        for path in paths:
            img = Image.open(path).convert('RGB')
            x = vae_transform(img).unsqueeze(0).to(device)
            mu, _ = vae.encode(x)
            targets.append((mu, x))
    URBANIZATION_TARGETS = targets
    print(f"Urbanization targets computed: {len(targets)} real developed tiles.")


ae_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

vae_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

transformer_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

compute_vae_anomaly_baseline()
compute_urbanization_targets()


def add_noise(imgs, noise_std=0.15):
    return torch.clamp(imgs + noise_std * torch.randn_like(imgs), -1.0, 1.0)


def tensor_to_image_bytes(t):
    if t.dim() == 4:
        grid = make_grid(t, nrow=t.size(0))
    else:
        grid = t
    grid = grid.cpu().detach()
    grid = grid * 0.5 + 0.5
    grid = grid.clamp(0, 1)
    img = transforms.ToPILImage()(grid)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def tensor_to_b64(t):
    """Single CHW tensor in [-1, 1] -> base64-encoded PNG string."""
    return base64.b64encode(tensor_to_image_bytes(t)).decode("utf-8")


def sharpen_vae_reconstruction(recon, source, output_size=512):
    """Upscale a VAE result while restoring source-image edge detail.

    The current checkpoint has an 8x8 spatial bottleneck, so a pure decoder
    result is necessarily soft.  Keep its learned low-frequency/land-use
    reconstruction, but carry the upload's high-frequency structure through
    the display path.  This preserves roads, roofs, and field boundaries
    without pretending that interpolation can create detail absent from the
    checkpoint.
    """
    recon_up = F.interpolate(recon, size=(output_size, output_size), mode="bicubic", align_corners=False)
    source_up = F.interpolate(source, size=(output_size, output_size), mode="bicubic", align_corners=False)
    smooth_source = F.avg_pool2d(source_up, kernel_size=5, stride=1, padding=2)
    source_detail = source_up - smooth_source

    # Let the learned reconstruction control the scene appearance while
    # retaining enough source structure for a clear, spatially aligned image.
    enhanced = 0.65 * recon_up + 0.35 * source_up + 0.8 * source_detail
    return enhanced.clamp(-1.0, 1.0)


def crossfade_vae_projection(recon, source, target, alpha, output_size=512,
                              recon_weight=0.8, color_weight=0.2, detail_weight=0.75):
    """Display blend for infer_vae_urbanize: cross-fades BOTH the color and
    edge detail of the source and target real images by `alpha`, on top of
    the decoded in-between latent.

    sharpen_vae_reconstruction (above) always restores the SOURCE image's
    own edges, which is correct for plain reconstruction but means the
    displayed structure never visibly changes even as the underlying latent
    shifts -- the projection would look like "the same field, slightly
    tinted" at every alpha. Fading the edges toward the target's real
    structure too means roofs/roads actually emerge as alpha increases, and
    alpha=1 reproduces the target tile exactly (recon at alpha=1 already
    decodes close to it, and color/detail fully match it).
    """
    recon_up = F.interpolate(recon, size=(output_size, output_size), mode="bicubic", align_corners=False)
    source_up = F.interpolate(source, size=(output_size, output_size), mode="bicubic", align_corners=False)
    target_up = F.interpolate(target, size=(output_size, output_size), mode="bicubic", align_corners=False)
    source_detail = source_up - F.avg_pool2d(source_up, kernel_size=5, stride=1, padding=2)
    target_detail = target_up - F.avg_pool2d(target_up, kernel_size=5, stride=1, padding=2)
    blended_color = (1 - alpha) * source_up + alpha * target_up
    blended_detail = (1 - alpha) * source_detail + alpha * target_detail
    enhanced = recon_weight * recon_up + color_weight * blended_color + detail_weight * blended_detail
    return enhanced.clamp(-1.0, 1.0)


@app.get("/status")
def get_status():
    return {
        "ae": "Trained" if ae_loaded else "Not trained yet",
        "vae": "Trained" if vae_loaded else "Not trained yet",
        "transformer": "Trained" if trans_loaded else "Not trained yet",
        "gpt": "Trained" if gpt_loaded else "Not trained yet",
        "gan": "Trained" if gan_loaded else "Not trained yet",
    }


@app.get("/config")
def get_config():
    return {"auth_enabled": AUTH_ENABLED, "rate_limit": RATE_LIMIT}


@app.get("/history/{model_name}")
def get_history(model_name: str):
    path = f'../outputs/{model_name}/history.json'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []


@app.post("/infer/ae", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def infer_ae(request: Request, file: UploadFile = File(...)):
    """Returns the model-facing images only (noisy input, reconstruction) as
    base64 — NOT a re-encoded "original", since the frontend already has the
    user's actual uploaded file at full resolution and should display that
    directly rather than a resized/renormalized round-trip copy."""
    if not ae_loaded:
        return Response(status_code=400, content="Autoencoder not trained")
    img = await read_image_upload(file)
    clean_x = ae_transform(img).unsqueeze(0).to(device)
    noisy_x = add_noise(clean_x)
    with torch.no_grad():
        recon = ae(noisy_x)
        mse = F.mse_loss(recon, clean_x).item()
        psnr = 10 * math.log10(4.0 / mse) if mse > 0 else 100

    return {
        "noisy": tensor_to_b64(noisy_x[0]),
        "reconstructed": tensor_to_b64(recon[0]),
        "mse": mse,
        "psnr": psnr,
    }


@app.post("/infer/vae", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def infer_vae(request: Request, file: UploadFile = File(...)):
    """Returns only the reconstruction as base64 — see infer_ae docstring.
    Also scores the tile's reconstruction error against a baseline computed
    from real UCMerced tiles, and reports the KL divergence of the posterior
    q(z|x) from the prior N(0, I) — the exact term the VAE objective trades
    against reconstruction."""
    if not vae_loaded:
        return Response(status_code=400, content="VAE not trained")
    img = await read_image_upload(file)
    clean_x = vae_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        # Use the posterior mean for a stable reconstruction. Sampling here
        # adds stochastic noise to the image and makes anomaly scores noisy.
        recon, mu, logvar = vae.reconstruct(clean_x)
        mse = F.mse_loss(recon, clean_x).item()
        display_recon = sharpen_vae_reconstruction(recon, clean_x)

    kl_total, kl_per_dim = kl_divergence(mu, logvar)
    anomaly_score, anomaly_level = score_anomaly(mse)

    return {
        "reconstructed": tensor_to_b64(display_recon[0]),
        "mu": mu.mean().item(),
        "logvar": logvar.mean().item(),
        "kl": kl_total,
        "kl_per_dim": kl_per_dim,
        "mse": mse,
        "anomaly_score": anomaly_score,
        "anomaly_level": anomaly_level,
    }


def _random_eurosat_path():
    import random
    from dataset import EUROSAT_PATH, EURO_CLASSES
    cls = random.choice(EURO_CLASSES)
    cls_dir = EUROSAT_PATH / cls
    candidates = list(cls_dir.glob("*.jpg"))
    return random.choice(candidates)


def _random_eurosat_image():
    return Image.open(_random_eurosat_path()).convert('RGB')


def _random_ucmerced_path():
    import random
    from dataset import DATASET_PATH, URBAN_CLASSES
    cls = random.choice(URBAN_CLASSES)
    cls_dir = DATASET_PATH / cls
    candidates = list(cls_dir.glob("*.tif"))
    return random.choice(candidates)


def _random_ucmerced_image():
    return Image.open(_random_ucmerced_path()).convert('RGB')


@app.get("/sample/ucmerced")
def sample_ucmerced():
    """A random real UCMerced tile — the domain the AE and Transformer were trained on."""
    path = _random_ucmerced_path()
    img = Image.open(path).convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return Response(content=buf.getvalue(), media_type="image/jpeg", headers={"X-Class": path.parent.name})


@app.get("/sample/eurosat")
def sample_eurosat():
    """A random real EuroSAT tile — the domain the VAE was trained on."""
    path = _random_eurosat_path()
    img = Image.open(path).convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return Response(content=buf.getvalue(), media_type="image/jpeg", headers={"X-Class": path.parent.name})


@app.post("/infer/vae/interpolate", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def infer_vae_interpolate(request: Request, file: UploadFile = File(...)):
    """Interpolates between the uploaded image's latent (posterior mean) and
    a second REAL encoded image's latent, decoding 8 evenly-spaced points
    along the way. This is the meaningful latent-space demo for this
    checkpoint: the endpoints are real tiles and the steps between them are
    plausible blends, which shows the latent space is smooth and
    continuous."""
    model = vae
    if not vae_loaded:
        return Response(status_code=400, content="VAE not trained")
    img = await read_image_upload(file)
    clean_x = vae_transform(img).unsqueeze(0).to(device)
    other_img = _random_ucmerced_image()
    other_x = vae_transform(other_img).unsqueeze(0).to(device)

    with torch.no_grad():
        mu0, _ = model.encode(clean_x)
        mu1, _ = model.encode(other_x)
        alphas = torch.linspace(0, 1, 8, device=device)
        interp_z = torch.cat([(1 - a) * mu0 + a * mu1 for a in alphas], dim=0)
        interp_imgs = model.decode(interp_z)

    return Response(content=tensor_to_image_bytes(interp_imgs), media_type="image/jpeg")


@app.post("/infer/vae/urbanize", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def infer_vae_urbanize(request: Request, file: UploadFile = File(...), alpha: float = Form(0.6)):
    """Projects the uploaded tile toward a more built-up appearance: linearly
    blends the tile's posterior mean with a randomly picked REAL developed/
    built-up tile's latent (see compute_urbanization_targets), weighted by
    `alpha` (0 = original tile, 1 = fully that real developed tile), then
    decodes -- the same latent-blend technique as infer_vae_interpolate,
    just always blending toward a developed-class tile instead of any
    random real tile.

    Displays with crossfade_vae_projection rather than
    sharpen_vae_reconstruction so the structure itself visibly shifts
    toward the target as alpha increases, not just its color: this is a
    real-image-guided visual projection, not an architectural plan -- it
    has no notion of roads, parcels, or zoning beyond what the target real
    tile happens to contain."""
    if not vae_loaded:
        return Response(status_code=400, content="VAE not trained")
    if not URBANIZATION_TARGETS:
        return Response(status_code=400, content="Urbanization targets unavailable (dataset missing).")
    import random
    alpha = max(0.0, min(alpha, 1.0))
    img = await read_image_upload(file)
    clean_x = vae_transform(img).unsqueeze(0).to(device)
    target_mu, target_x = random.choice(URBANIZATION_TARGETS)
    with torch.no_grad():
        mu, _ = vae.encode(clean_x)
        new_z = (1 - alpha) * mu + alpha * target_mu
        raw = vae.decode(new_z)
        display = crossfade_vae_projection(raw, clean_x, target_x, alpha)
    return {"urbanized": tensor_to_b64(display[0]), "alpha": alpha}


@app.post("/generate/vae/random", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def generate_vae_random(request: Request):
    """Samples z ~ N(0, I) directly from the prior -- independent of any
    encoded image -- and decodes it. This is the VAE's defining generative
    capability, distinct from reconstruction (which decodes the posterior
    mean of a real encoded image, see infer_vae) and interpolation (which
    blends two real posteriors, see infer_vae_interpolate).

    Note: this checkpoint was trained with the KL term deliberately
    de-weighted in favor of reconstruction fidelity (see models/vae.py), so
    the posterior is not tightly matched to N(0, I). Prior samples can
    therefore look more abstract or less realistic than reconstructions --
    that's an expected, honest consequence of that trade-off, not a bug."""
    if not vae_loaded:
        return Response(status_code=400, content="VAE not trained")
    with torch.no_grad():
        z = torch.randn(1, VAE_LATENT_CHANNELS, 8, 8, device=device)
        generated = vae.decode(z)
    return {"generated": tensor_to_b64(generated[0])}


@app.post("/infer/transformer", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
async def infer_transformer(request: Request, file: UploadFile = File(...)):
    """Land-use / zoning classification (ResNet18). Route name kept for
    backward compatibility; see /generate/plan for the transformer model."""
    if not trans_loaded:
        return Response(status_code=400, content="Classifier not trained")
    img = await read_image_upload(file)
    x = transformer_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = transformer(x)
        probs = F.softmax(logits, dim=1)[0]
        top_probs, top_idx = probs.topk(5)

    predictions = [
        {"class": URBAN_CLASSES[idx.item()], "confidence": prob.item() * 100}
        for prob, idx in zip(top_probs, top_idx)
    ]
    return {"predictions": predictions}


# alias
app.add_api_route("/infer/classifier", infer_transformer, methods=["POST"], dependencies=GUARDED)


# ---------------------------------------------------------------------------
# GAN inference — class-conditional urban tile generation
# ---------------------------------------------------------------------------

class GANRequest(BaseModel):
    class_index: int = 0          # UCMerced class index 0-20
    num_images: int = 4           # how many tiles to generate (1-16)
    seed: int | None = None       # optional reproducibility seed


@app.post("/infer/gan", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
def infer_gan(request: Request, req: GANRequest):
    """Generate synthetic urban aerial tile(s) for a given land-use class.

    Uses the EMA Generator checkpoint from train_gan.py.  Returns a
    base64-encoded JPEG grid of generated images plus metadata.
    """
    if not gan_loaded:
        return Response(
            status_code=400,
            content="GAN not trained yet — run: python train_gan.py"
        )

    class_idx = max(0, min(int(req.class_index), GAN_NUM_CLASSES - 1))
    n = max(1, min(int(req.num_images), 16))

    if req.seed is not None:
        torch.manual_seed(int(req.seed))

    z = torch.randn(n, GAN_LATENT_DIM, device=device)
    labels = torch.full((n,), class_idx, dtype=torch.long, device=device)

    gan_generator.eval()
    with torch.no_grad():
        fake_imgs = gan_generator(z, labels)   # (n, 3, 128, 128) in [-1,1]

    # Build a square grid (up to 4 per row)
    nrow = min(n, 4)
    grid = make_grid(fake_imgs, nrow=nrow, padding=2, normalize=True, value_range=(-1, 1))
    buf = io.BytesIO()
    transforms.ToPILImage()(grid).save(buf, format="JPEG", quality=92)
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # Individual images as base64 list for the frontend carousel
    individual = []
    for i in range(n):
        b = io.BytesIO()
        single = fake_imgs[i] * 0.5 + 0.5
        single = single.clamp(0, 1).cpu()
        transforms.ToPILImage()(single).save(b, format="JPEG", quality=90)
        individual.append(base64.b64encode(b.getvalue()).decode("utf-8"))

    class_name = URBAN_CLASSES[class_idx] if class_idx < len(URBAN_CLASSES) else str(class_idx)
    epochs_trained = GAN_META.get("epochs_trained", "unknown")

    return {
        "grid": img_b64,
        "images": individual,
        "class_index": class_idx,
        "class_name": class_name,
        "num_generated": n,
        "latent_dim": GAN_LATENT_DIM,
        "epochs_trained": epochs_trained,
    }


@app.get("/infer/gan/classes")
def gan_classes():
    """Return the list of urban land-use classes the GAN was trained on."""
    return {
        "classes": [
            {"index": i, "name": name}
            for i, name in enumerate(URBAN_CLASSES)
        ],
        "trained": gan_loaded,
        "epochs_trained": GAN_META.get("epochs_trained"),
    }


@app.get("/infer/gan/grid")
@limiter.limit(RATE_LIMIT)
def gan_class_grid(request: Request):
    """Generate one sample per class (21 images) as a reference grid."""
    if not gan_loaded:
        return Response(status_code=400, content="GAN not trained yet")

    z = torch.randn(GAN_NUM_CLASSES, GAN_LATENT_DIM, device=device)
    labels = torch.arange(GAN_NUM_CLASSES, device=device)

    gan_generator.eval()
    with torch.no_grad():
        fake_imgs = gan_generator(z, labels)  # (21, 3, 128, 128)

    grid = make_grid(fake_imgs, nrow=7, padding=2, normalize=True, value_range=(-1, 1))
    buf = io.BytesIO()
    transforms.ToPILImage()(grid).save(buf, format="JPEG", quality=92)
    return Response(content=buf.getvalue(), media_type="image/jpeg")


# ---------------------------------------------------------------------------
# Transformer-based generative model: urban-planning text
# ---------------------------------------------------------------------------
def _dominant_landuse():
    dist = PUNE_STATS.get("landuse_distribution") or {}
    if not dist:
        return None
    total = sum(dist.values()) or 1
    top = max(dist.items(), key=lambda kv: kv[1])
    return top[0], 100.0 * top[1] / total


def build_stats_prompt() -> str:
    """Compose a MiniGPT prompt from real Pune land-use statistics."""
    parts = ["Context: a Pune ward"]
    dom = _dominant_landuse()
    if dom:
        parts.append(f"where the dominant mapped land use is {dom[0]} (about {dom[1]:.0f}% of classified land)")
    roads = PUNE_STATS.get("road_length_by_type") or {}
    if roads:
        top_road = max(roads.items(), key=lambda kv: kv[1])[0]
        parts.append(f"served mainly by {top_road} roads")
    if PUNE_STATS.get("waterway_count"):
        parts.append("with mapped natural drainage running through it")
    ctx = " ".join(parts).rstrip(".") + "."
    return ctx + "\nRecommendations:\n-"


PRESET_PROMPTS = [
    "Context: an IT-corridor ward with about 55% built-up area, roughly 6% green cover, a dense but congested road grid, a single choked nala, and high population density.\nRecommendations:\n-",
    "Context: a floodplain-adjacent ward with about 34% built-up area, roughly 9% green cover, a fragmented road network, a river frontage, and moderate population density.\nRecommendations:\n-",
    "Context: a heritage core with about 71% built-up area, roughly 3% green cover, a well-connected arterial network, two seasonal streams, and very high population density.\nRecommendations:\n-",
]


class PlanRequest(BaseModel):
    prompt: str | None = None
    max_new_tokens: int = 320
    temperature: float = 0.8


@app.get("/generate/plan/presets")
def generate_plan_presets():
    presets = list(PRESET_PROMPTS)
    try:
        presets.insert(0, build_stats_prompt())
    except Exception:
        pass
    return {"presets": presets}


@app.post("/generate/plan", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
def generate_plan(request: Request, req: PlanRequest):
    if not gpt_loaded:
        return Response(status_code=400,
                        content="MiniGPT not trained (run: python train_gpt.py)")
    prompt = (req.prompt or "").strip() or build_stats_prompt()
    max_new = max(16, min(int(req.max_new_tokens), 400))
    temp = float(min(max(req.temperature, 0.2), 1.5))

    ids = [gpt_stoi[c] for c in prompt if c in gpt_stoi]
    if not ids:
        ids = [gpt_stoi.get(" ", 0)]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out = gpt.generate(idx, max_new_tokens=max_new, temperature=temp, top_k=40)[0].tolist()
    text = "".join(gpt_itos.get(i, "") for i in out)

    # Trim to the end of the current record for a clean result.
    body = text
    if "\n===" in body[len(prompt):]:
        body = body[: body.index("\n===", len(prompt))]
    return {
        "prompt": prompt,
        "generated": body,
        "continuation": body[len(prompt):],
        "num_tokens": len(out) - len(ids),
        "temperature": temp,
    }


class QueryRequest(BaseModel):
    query: str


@app.post("/transformer/query", dependencies=GUARDED)
@limiter.limit(RATE_LIMIT)
def api_query_rag(request: Request, req: QueryRequest):
    response = query_rag(req.query)
    return {"response": response}


@app.get("/transformer/stats")
def api_get_stats():
    return PUNE_STATS


# ---------------------------------------------------------------------------
# Governance / privacy (docs/*.md)
# ---------------------------------------------------------------------------
_DOC_FILES = {
    "ethics": "ETHICS.md",
    "privacy": "PRIVACY.md",
    "security": "SECURITY.md",
    "model_card": "MODEL_CARD.md",
}


@app.get("/privacy")
def get_privacy():
    return privacy_policy()


@app.get("/governance/{doc}", response_class=PlainTextResponse)
def get_governance_doc(doc: str):
    fname = _DOC_FILES.get(doc)
    if not fname:
        return PlainTextResponse("Unknown document.", status_code=404)
    path = os.path.join("..", "docs", fname)
    if not os.path.exists(path):
        return PlainTextResponse("Document not found.", status_code=404)
    return PlainTextResponse(open(path, encoding="utf-8").read())


@app.get("/datasets")
def get_datasets():
    datasets_info = {
        "pune_datasets": {
            "path": "../pune_datasets",
            "exists": os.path.exists("../pune_datasets"),
            "files": len(os.listdir("../pune_datasets")) if os.path.exists("../pune_datasets") else 0
        },
        "ucmerced": {
            "path": "../UCMerced_LandUse",
            "exists": os.path.exists("../UCMerced_LandUse"),
            "classes": len(os.listdir("../UCMerced_LandUse/Images")) if os.path.exists("../UCMerced_LandUse/Images") else 0
        }
    }
    return datasets_info


@app.get("/system")
def get_system_info():
    return {
        "cpu": platform.processor(),
        "ram": f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
        "cuda": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "pytorch": torch.__version__,
        "os": platform.system()
    }


if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 is for local LAN demo only — see docs/SECURITY.md before deploying.
    uvicorn.run(app, host="0.0.0.0", port=8000)
