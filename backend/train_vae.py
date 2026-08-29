import os
import sys
import time
import json
import torch
import torch.nn.functional as F
from torchvision.utils import save_image
from dataset import get_dataloaders
from models.vae import VAE

# Guards against a second concurrent training run corrupting this run's
# checkpoint/log files (observed: an unexplained duplicate process kept
# spawning and writing to the same ../outputs/vae/model.pth mid-run).
LOCK_PATH = '../outputs/vae/.train_lock'

LATENT_CHANNELS = 64
FREEZE_ENCODER_EPOCHS = 5
EPOCHS = 50
BATCH_SIZE = 16
LR = 1e-4
LR_FINETUNE = 1e-5
# Priority here is reconstruction fidelity — the parking-lot-style dense
# scenes need every bit of latent capacity they can get, and a meaningful
# KL weight measurably worsens reconstruction everywhere (verified: beta=0.5
# and beta=0.05 both produced visibly worse reconstructions than this,
# including full posterior collapse at beta=0.5). This trades away the
# "sample straight from the prior" capability — that's a real, known VAE
# trade-off, not an oversight — in favor of the reconstruction quality that
# actually matters for this demo.
BETA_TARGET = 0.0001
KL_WARMUP_EPOCHS = 1
FREE_BITS_PER_DIM = 0.0


def vae_loss(recon, imgs, mu, logvar, beta):
    # MSE alone rewards the decoder for predicting the average colour of
    # neighbouring pixels, which produces the visibly washed-out urban tiles
    # seen in the UI. L1 preserves boundaries better while a smaller MSE term
    # keeps the reconstruction numerically stable.
    recon_loss = 0.7 * F.l1_loss(recon, imgs) + 0.3 * F.mse_loss(recon, imgs)
    # mu/logvar are spatial (B, C, H, W) here — sum over all non-batch dims.
    kl_per_dim = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp())
    kl_per_dim = torch.clamp(kl_per_dim, min=FREE_BITS_PER_DIM)
    kl = kl_per_dim.sum(dim=[1, 2, 3]).mean()
    loss = recon_loss + beta * kl
    return loss, recon_loss, kl


def train():
    os.makedirs('../outputs/vae', exist_ok=True)
    if os.path.exists(LOCK_PATH):
        with open(LOCK_PATH) as f:
            holder_pid = f.read().strip()
        print(f"ERROR: {LOCK_PATH} exists (held by pid {holder_pid}) — another training run "
              f"appears to be in progress. Refusing to start to avoid corrupting the checkpoint. "
              f"If you're sure nothing else is running, delete this file and retry.")
        sys.exit(1)
    with open(LOCK_PATH, 'w') as f:
        f.write(str(os.getpid()))

    try:
        _train_inner()
    finally:
        if os.path.exists(LOCK_PATH):
            os.remove(LOCK_PATH)


def _train_inner():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    train_loader, _ = get_dataloaders(batch_size=BATCH_SIZE)
    model = VAE(latent_channels=LATENT_CHANNELS).to(device)
    model.set_encoder_trainable(False)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    history = []
    os.makedirs('../outputs/vae/samples', exist_ok=True)

    print(f"Starting UCMerced VAE training ({EPOCHS} epochs, latent {LATENT_CHANNELS}x8x8, "
          f"KL beta warms up to {BETA_TARGET} over {KL_WARMUP_EPOCHS} epochs, "
          f"encoder frozen for first {FREEZE_ENCODER_EPOCHS})...")

    for epoch in range(EPOCHS):
        if epoch == FREEZE_ENCODER_EPOCHS:
            model.set_encoder_trainable(True)
            optimizer = torch.optim.Adam(model.parameters(), lr=LR_FINETUNE)
            print(f"Epoch {epoch+1}: unfreezing encoder, lr -> {LR_FINETUNE}")

        beta = BETA_TARGET * min(1.0, (epoch + 1) / KL_WARMUP_EPOCHS)

        model.train()
        total_loss = 0
        total_recon = 0
        total_kl = 0
        start = time.time()

        for batch_idx, (imgs, _) in enumerate(train_loader):
            imgs = imgs.to(device)

            optimizer.zero_grad()
            recon, mu, logvar = model(imgs)

            loss, recon_loss, kl = vae_loss(recon, imgs, mu, logvar, beta)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item()
            total_recon += recon_loss.item()
            total_kl += kl.item()

            if batch_idx % 20 == 0:
                print(f"Epoch {epoch+1}/{EPOCHS} | Batch {batch_idx}/{len(train_loader)} | "
                      f"Loss: {loss.item():.4f} | Recon: {recon_loss.item():.4f} | "
                      f"KL(raw): {kl.item():.4f} | beta: {beta:.4f}")

        avg_loss = total_loss / len(train_loader)
        avg_recon = total_recon / len(train_loader)
        avg_kl = total_kl / len(train_loader)
        history.append({"epoch": epoch + 1, "loss": avg_loss, "recon": avg_recon, "kl": avg_kl})
        print(f"Epoch {epoch+1} done in {time.time()-start:.1f}s | Avg Loss: {avg_loss:.4f} | "
              f"Avg Recon: {avg_recon:.4f} | Avg KL: {avg_kl:.4f}")

        os.makedirs('../outputs/vae', exist_ok=True)
        torch.save(model.state_dict(), '../outputs/vae/model.pth')

        if (epoch + 1) % 5 == 0:
            with torch.no_grad():
                n = min(8, imgs.size(0))
                sample_orig = imgs[:n]
                sample_recon = recon[:n]
                grid = torch.cat([sample_orig, sample_recon], dim=0)
                grid = (grid + 1) / 2
                save_image(grid, f'../outputs/vae/samples/epoch_{epoch+1}.png', nrow=n)

                # Prior-sample diagnostic only — with a negligible KL weight
                # (prioritizing reconstruction, see comment above) this is
                # expected to look like noise, not a meaningful capability.
                z_prior = torch.randn(8, LATENT_CHANNELS, 8, 8, device=device)
                prior_samples = model.decode(z_prior)
                prior_samples = (prior_samples + 1) / 2
                save_image(prior_samples, f'../outputs/vae/prior_samples_epoch_{epoch+1}.png', nrow=8)

            generate_interpolation(model=model, device=device, epoch=epoch + 1, real_batch=imgs)
            print(f"Saved reconstruction + prior-sample + interpolation grids for epoch {epoch+1}")

    with open('../outputs/vae/history.json', 'w') as f:
        json.dump(history, f)

    print("VAE training complete.")


def generate_interpolation(steps=8, model=None, device=None, epoch=None, real_batch=None):
    """Interpolates between two REAL encoded images' latents. With a
    genuinely-regularized latent space this should look like a smooth,
    plausible blend at every step (not just at the two real endpoints)."""
    device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if model is None:
        model = VAE(latent_channels=LATENT_CHANNELS).to(device)
        model.load_state_dict(torch.load('../outputs/vae/model.pth', map_location=device, weights_only=True))
    model.eval()

    if real_batch is None:
        loader, _ = get_dataloaders(batch_size=2)
        real_batch, _ = next(iter(loader))
    real_batch = real_batch[:2].to(device)

    with torch.no_grad():
        mu, _ = model.encode(real_batch)
        z0, z1 = mu[0:1], mu[1:2]

        alphas = torch.linspace(0, 1, steps, device=device)
        zs = torch.cat([(1 - a) * z0 + a * z1 for a in alphas], dim=0)

        recon = model.decode(zs)
        recon = (recon + 1) / 2
        os.makedirs('../outputs/vae', exist_ok=True)
        out_path = f'../outputs/vae/latent_interpolation_epoch_{epoch}.png' if epoch else '../outputs/vae/latent_interpolation.png'
        save_image(recon, out_path, nrow=steps)
    model.train()


if __name__ == '__main__':
    train()
