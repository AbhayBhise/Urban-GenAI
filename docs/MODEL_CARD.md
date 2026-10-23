# UrbanGen AI — Model Card

One document covering every model shipped in the app. Metrics are from the
committed training runs (`outputs/*/history.json`); re-training will vary.

Common properties:
- **Framework:** PyTorch. **Hardware:** single NVIDIA RTX 4050 Laptop GPU (~75 W).
- **Intended use:** teaching / research prototype for AI-assisted, *advisory*
  urban-planning drafting.
- **Out-of-scope use:** see `docs/ETHICS.md §3` (no regulatory, rights-affecting,
  biometric, or synthetic-media-of-real-people use).
- **Shared limitation:** trained on Western datasets / an English corpus, applied
  to Pune — expect degraded reliability on local urban form (`docs/ETHICS.md §2`).

---

## 1. Denoising Autoencoder (`ae`)

| | |
|---|---|
| Architecture | Pretrained ResNet18 encoder (stem/layer1/layer2/layer3) + **U-Net-style skip-connected** transposed-conv decoder, 128×128 RGB. Originally decoded purely from the 8×8×256 bottleneck; skip connections (Ronneberger et al., 2015) were added after measuring the bottleneck-only version losing fine detail on structurally complex tiles |
| Training data | UCMerced LandUse (21 classes, US aerial imagery) |
| Objective | Reconstruct clean tile from Gaussian-noised input, σ=0.15 (MSE) |
| Result | 50 epochs. 21-class average PSNR 25dB → **29.7dB** after adding skip connections; the previously-worst classes (dense residential, harbor, mobile home park) each gained **+7dB**, closing the easy/hard-class gap from 7.3dB to 2.6dB |
| Purpose in project | Pre-clean degraded satellite/aerial imagery before downstream analysis (Classifier, VAE) |
| Limitations | Learns denoising for this domain only; not a super-resolution model |

## 2. Variational Autoencoder (`vae`)

| | |
|---|---|
| Architecture | ResNet18 encoder → 64×8×8 spatial latent (`mu`, `logvar`) → reparameterize `z = mu + σ·ε` → transposed-conv decoder |
| Training data | UCMerced LandUse |
| Objective | `0.7·L1 + 0.3·MSE` reconstruction + `β·KL`, **β = 1e-4** (reconstruction-priority) |
| Result | train recon ≈ 0.075, KL ≈ 103 nats (50 epochs) |
| Purpose in project | Reconstruction; latent **interpolation** between two real encoded tiles; reconstruction-error **anomaly scoring** against a baseline over real tiles |
| KL divergence | Reported per inference and plotted in the Training tab. With β ≈ 0 it is **not minimised** — it rises during training as the latent grows more informative. This is expected for a reconstruction-priority VAE. Sampling straight from the prior is therefore not meaningful on this model (a known β-VAE trade-off); interpolation between real tiles is used instead. A genuinely prior-matched checkpoint was attempted but collapsed at every workable β on this encoder/decoder within the project timeframe |
| Limitations | Latent does not match N(0,1); soft 8×8 spatial bottleneck |

## 3. Urban Plan Generator — MiniGPT (`gpt`)

| | |
|---|---|
| Architecture | Decoder-only Transformer built from scratch: char-level embedding + learned positional embedding, 4 pre-norm blocks (causal multi-head self-attention + MLP), weight-tied LM head. ~n_embd 256, 4 heads, block size 192 |
| Training data | `backend/corpus/urban_planning.txt` — hand-authored sustainable-planning corpus (zoning, green cover, transit-oriented development, stormwater, Pune context) |
| Objective | Next-character cross-entropy; temperature + top-k sampling at inference |
| Purpose in project | Given a prompt seeded from real Pune land-use statistics (`PUNE_STATS`), generate draft sustainability recommendations for planner review |
| Limitations | Small model, small corpus, char-level: fluent-sounding but **no factual grounding, no citations, can self-contradict**. Advisory drafting aid only |
| Train it | `python train_gpt.py` (~5–10 min) |

## 4. Land-Use Classifier (`transformer` route, ResNet18)

| | |
|---|---|
| Architecture | ResNet18, ImageNet-pretrained, fine-tuned; final FC → 21 classes |
| Training data | UCMerced LandUse (90/10 split) |
| Result | Persisted validation history: 98.1% accuracy and 0.103 loss at epoch 30; the API also reports a separate 105-tile representative runtime evaluation |
| Purpose in project | Automated land-use / zoning audit and land-use-change tracking at city scale |
| Note | This is a **CNN**, not a transformer. It is kept because it does useful project work; the transformer requirement is met by MiniGPT (§3). The API route name `transformer` is retained for backward compatibility |
| Limitations | 21 fixed classes from US imagery; single-label per tile |

## 5. Conditional DCGAN (`gan`)

| | |
|---|---|
| Architecture | Class-conditional DCGAN. Generator: noise (128-d) + class embedding (64-d) → linear/reshape to 8×8×512 → four residual nearest-neighbour upsampling blocks → Tanh, 128×128 RGB. Discriminator: projection-conditioned, five spectral-normalized Conv2d stages with an auxiliary classifier head |
| Training data | UCMerced LandUse (21 classes, 100 images/class) |
| Objective | Non-saturating adversarial BCE with label smoothing (real=0.9, fake=0.1), auxiliary class loss, diversity regularization, and EMA-averaged Generator (decay 0.999) used for inference |
| Result | 120 epochs (no pretrained weights — trained fully from scratch). The current seeded API evaluation reaches 100.0% intended-class recognition over 168 generated samples. This is a classifier-recognition proxy, not a photorealism or planning-validity measure |
| Purpose in project | Class-conditional synthetic tile generation for data augmentation / scenario exploration — distinct from the VAE, which only reconstructs/interpolates real, already-encoded tiles |
| Was untrained | Flagged as the top-priority missing component in `CONTRIBUTING.md` ("implemented but NOT yet trained") prior to this training run |
| Limitations | Geometric structure is not consistently crisp on 2,100 images; the recognition proxy is not a photorealism measure and generated tiles require human inspection |

---

## Sustainability / carbon footprint (Unit 6)

Hardware-level energy and carbon measurements were not recorded with a reproducible protocol, so no numerical footprint is claimed.

| Model | Recorded training |
|---|---|
| AE | 50 epochs |
| VAE | 50 epochs |
| MiniGPT | 3,000 optimization steps |
| Classifier | 30 epochs |
| GAN | 120 epochs |
| **Total** | **Not aggregated across incomparable protocols** |

Design choices that limit compute include pretrained backbones, a small from-scratch
transformer, single-GPU execution, and modest datasets. Inference is CPU-viable; a
quantitative carbon comparison remains future work.

## 6. Urban Scenario Diffusion Model (`diffusion`)

| | |
|---|---|
| Architecture | Lightweight image- and class-conditioned DDPM U-Net with sinusoidal timestep embeddings, label embeddings, and a 1,000-step linear noise schedule; inference uses a 20-step DDIM sampler |
| Training data | UCMerced LandUse, using the reproducible stratified split manifest in `outputs/splits/ucmerced_seed42.json` |
| Objective | MSE noise prediction, `E[||epsilon - epsilon_theta(x_t,t,c)||^2]` |
| Result | 50-epoch CUDA checkpoint: final noise-prediction MSE 0.00421; best 0.00384 |
| Training record | 16.63 min wall time; 28.51 W average GPU power; 61.37 W peak; 7.90 Wh estimated GPU-board energy |
| Purpose in project | Generate a candidate urban-scene alternative from an uploaded tile and target land-use class |
| Evaluation boundary | The available dataset has no paired before/after planning labels. The first valid report must include conditioned reconstruction loss and a human/land-use validity benchmark; no future-development accuracy is claimed |
| Limitations | Small dataset and lightweight U-Net; generated tiles are advisory scenarios and require human/domain review |
