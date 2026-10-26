import argparse
import json
import os
import sys
import time

import torch
import torch.nn.functional as F
from torchvision.utils import save_image

from dataset import get_split_dataloaders
from models.vae import VAE

OUT_DIR = "../outputs/vae"
LOCK_PATH = "../outputs/vae/.train_lock"

FREEZE_ENCODER_EPOCHS = 5
EPOCHS = 50
BATCH_SIZE = 32
LR = 2e-4
LR_FINETUNE = 2e-5
LATENT_CHANNELS = 64
BETA_TARGET = 1e-4
KL_WARMUP_EPOCHS = 2
FREE_BITS_PER_DIM = 0.01


def vae_loss(recon, imgs, mu, logvar, beta):
    recon_loss = 0.7 * F.l1_loss(recon, imgs) + 0.3 * F.mse_loss(recon, imgs)
    kl_per_dim = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp())
    kl_per_dim = torch.clamp(kl_per_dim, min=FREE_BITS_PER_DIM)
    kl = kl_per_dim.sum(dim=[1, 2, 3]).mean()
    return recon_loss + beta * kl, recon_loss, kl


def psnr_from_mse(mse):
    import math
    return 10 * math.log10(4.0 / max(mse, 1e-12))


def evaluate(model, loader, device, beta):
    model.eval()
    total_loss = total_recon = total_kl = total_mse = 0.0
    n = 0
    with torch.no_grad():
        for imgs, _ in loader:
            imgs = imgs.to(device)
            recon, mu, logvar = model(imgs)
            loss, recon_loss, kl = vae_loss(recon, imgs, mu, logvar, beta)
            total_loss += loss.item()
            total_recon += recon_loss.item()
            total_kl += kl.item()
            total_mse += F.mse_loss(recon, imgs).item()
            n += 1
    model.train()
    return {
        "loss": total_loss / n,
        "recon": total_recon / n,
        "kl": total_kl / n,
        "mse": total_mse / n,
        "psnr": psnr_from_mse(total_mse / n),
    }


def generate_interpolation(model, device, epoch, real_batch, steps=8):
    model.eval()
    with torch.no_grad():
        real_batch = real_batch[:2].to(device)
        mu0, _, skips0 = model.encode_with_skips(real_batch[0:1])
        mu1, _, skips1 = model.encode_with_skips(real_batch[1:2])
        alphas = torch.linspace(0, 1, steps, device=device)
        recons = []
        for a in alphas:
            z = (1 - a) * mu0 + a * mu1
            if skips0 is None:
                skips = None
            else:
                skips = tuple((1 - a) * s0 + a * s1 for s0, s1 in zip(skips0, skips1))
            recons.append(model.decode(z, skips))
        grid = torch.cat(recons, dim=0)
        grid = (grid + 1) / 2
        os.makedirs(OUT_DIR, exist_ok=True)
        save_image(grid, f'{OUT_DIR}/latent_interpolation_epoch_{epoch}.png', nrow=steps)
    model.train()


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=EPOCHS)
    p.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    p.add_argument("--lr", type=float, default=LR)
    p.add_argument("--beta", type=float, default=BETA_TARGET)
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--skip-dropout", type=float, default=0.2)
    p.add_argument("--skip-channels", type=int, default=16)
    p.add_argument("--skip0-channels", type=int, default=16)
    p.add_argument("--smoke", action="store_true")
    return p.parse_args()


def train():
    args = get_args()
    global OUT_DIR, LOCK_PATH
    OUT_DIR = args.out_dir
    LOCK_PATH = os.path.join(OUT_DIR, ".train_lock")
    os.makedirs(OUT_DIR, exist_ok=True)
    if os.path.exists(LOCK_PATH):
        with open(LOCK_PATH) as f:
            holder_pid = f.read().strip()
        print(f"ERROR: {LOCK_PATH} exists (held by pid {holder_pid}).")
        sys.exit(1)
    with open(LOCK_PATH, "w") as f:
        f.write(str(os.getpid()))
    try:
        _train_inner(args)
    finally:
        if os.path.exists(LOCK_PATH):
            os.remove(LOCK_PATH)


def _train_inner(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    train_loader, val_loader, _ = get_split_dataloaders(
        batch_size=args.batch_size, size=128, num_workers=0
    )
    model = VAE(latent_channels=LATENT_CHANNELS, use_skips=True,
                skip_dropout=args.skip_dropout, skip_channels=args.skip_channels,
                skip0_channels=args.skip0_channels).to(device)
    model.set_encoder_trainable(False)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    history = []
    epochs = 2 if args.smoke else args.epochs
    os.makedirs(f'{OUT_DIR}/samples', exist_ok=True)

    print(f"Starting Spatial Skip-VAE ({epochs} epochs, latent {LATENT_CHANNELS}x8x8, beta={args.beta})")

    for epoch in range(epochs):
        if epoch == FREEZE_ENCODER_EPOCHS:
            model.set_encoder_trainable(True)
            optimizer = torch.optim.Adam(model.parameters(), lr=LR_FINETUNE)
            print(f"Epoch {epoch+1}: unfreezing encoder, lr -> {LR_FINETUNE}")

        beta = args.beta * min(1.0, (epoch + 1) / KL_WARMUP_EPOCHS)
        model.train()
        total_loss = total_recon = total_kl = total_mse = 0.0
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
            total_mse += F.mse_loss(recon, imgs).item()

            if batch_idx % 20 == 0:
                print(f"Epoch {epoch+1}/{epochs} | Batch {batch_idx}/{len(train_loader)} | "
                      f"Loss: {loss.item():.4f} | Recon: {recon_loss.item():.4f} | KL: {kl.item():.2f}")

        n = len(train_loader)
        train_metrics = {
            "loss": total_loss / n,
            "recon": total_recon / n,
            "kl": total_kl / n,
            "mse": total_mse / n,
            "psnr": psnr_from_mse(total_mse / n),
        }
        val_metrics = evaluate(model, val_loader, device, beta)
        history.append({"epoch": epoch + 1, **train_metrics, "val": val_metrics})
        print(f"Epoch {epoch+1} done in {time.time()-start:.1f}s | "
              f"train MSE {train_metrics['mse']:.5f} PSNR {train_metrics['psnr']:.2f} | "
              f"val MSE {val_metrics['mse']:.5f} PSNR {val_metrics['psnr']:.2f} | "
              f"KL {train_metrics['kl']:.2f}")

        torch.save(model.state_dict(), f'{OUT_DIR}/model.pth')
        with open(f'{OUT_DIR}/history.json', 'w') as f:
            json.dump(history, f, indent=2)

        if (epoch + 1) % 10 == 0 or args.smoke:
            with torch.no_grad():
                n_show = min(8, imgs.size(0))
                grid = torch.cat([imgs[:n_show], recon[:n_show]], dim=0)
                save_image((grid + 1) / 2, f'{OUT_DIR}/samples/epoch_{epoch+1}.png', nrow=n_show)
                z_prior = torch.randn(8, LATENT_CHANNELS, 8, 8, device=device)
                save_image((model.decode(z_prior) + 1) / 2,
                           f'{OUT_DIR}/prior_samples_epoch_{epoch+1}.png', nrow=8)
            generate_interpolation(model, device, epoch + 1, imgs)

    print("VAE training complete.")


if __name__ == '__main__':
    train()
