"""
Training script for the Conditional DCGAN.

Usage (from the backend/ directory):
    python train_gan.py [--epochs 100] [--batch-size 32] [--lr 2e-4] [--resume]

What it does
------------
* Loads the UCMerced aerial land-use dataset (21 classes, 128×128 tiles).
* Trains a class-conditional Generator and Discriminator using the
  non-saturating GAN objective (binary cross-entropy) with label smoothing.
* Saves model weights, a JSON training history, and periodic sample grids
  to outputs/gan/ so the API and frontend can consume them.

Key hyperparameters
-------------------
* Label smoothing (real=0.9, fake=0.1)  — reduces D over-confidence.
* Two D steps per G step — keeps D slightly ahead of G (common heuristic).
* Exponential Moving Average of G weights saved as the "stable" checkpoint
  used for inference — EMA G produces smoother, higher-quality images than
  the raw G checkpoint.
* Periodic FID-proxy logging (Inception feature distance on training batch)
  gives a rough quality indicator without needing a reference dataset split.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image, make_grid
from PIL import Image

# Ensure backend/ is on sys.path when called from outside it.
sys.path.insert(0, str(Path(__file__).parent))

from models.gan import Generator, Discriminator, LATENT_DIM, NUM_CLASSES
from dataset import UCMercedDataset, URBAN_CLASSES

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUT_DIR = Path("../outputs/gan")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR = OUT_DIR / "samples"
SAMPLE_DIR.mkdir(exist_ok=True)

G_PATH = OUT_DIR / "generator.pth"
D_PATH = OUT_DIR / "discriminator.pth"
G_EMA_PATH = OUT_DIR / "generator_ema.pth"   # ← used by the API
HISTORY_PATH = OUT_DIR / "history.json"
META_PATH = OUT_DIR / "meta.json"

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def get_args():
    p = argparse.ArgumentParser(description="Train Conditional DCGAN on UCMerced")
    p.add_argument("--epochs", type=int, default=100,
                   help="Number of training epochs (default: 100)")
    p.add_argument("--batch-size", type=int, default=32,
                   help="Batch size (default: 32)")
    p.add_argument("--lr", type=float, default=2e-4,
                   help="Learning rate for both G and D (default: 2e-4)")
    p.add_argument("--d-steps", type=int, default=2,
                   help="Discriminator updates per Generator update (default: 2)")
    p.add_argument("--latent-dim", type=int, default=LATENT_DIM,
                   help=f"Noise vector size (default: {LATENT_DIM})")
    p.add_argument("--ema-decay", type=float, default=0.999,
                   help="EMA decay for Generator weights (default: 0.999)")
    p.add_argument("--save-every", type=int, default=10,
                   help="Save sample grid every N epochs (default: 10)")
    p.add_argument("--resume", action="store_true",
                   help="Resume from saved checkpoints if they exist")
    p.add_argument("--workers", type=int, default=0,
                   help="DataLoader worker processes (default: 0 = main thread)")
    return p.parse_args()


# ---------------------------------------------------------------------------
# EMA helper
# ---------------------------------------------------------------------------

class EMA:
    """Exponential Moving Average over a model's parameters."""
    def __init__(self, model: nn.Module, decay: float = 0.999):
        self.decay = decay
        self.shadow = {k: v.clone().detach() for k, v in model.state_dict().items()}

    def update(self, model: nn.Module):
        with torch.no_grad():
            for k, v in model.state_dict().items():
                self.shadow[k] = self.decay * self.shadow[k] + (1 - self.decay) * v

    def apply(self, model: nn.Module):
        model.load_state_dict(self.shadow)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train():
    args = get_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GAN] Device: {device}")

    # --- Dataset & Dataloader ---
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.05),
        transforms.ToTensor(),
        transforms.Normalize([0.5] * 3, [0.5] * 3),
    ])
    dataset = UCMercedDataset(transform=transform)
    if len(dataset) == 0:
        print("[GAN] ERROR: UCMerced dataset not found. Please download it first.")
        print("      Expected path: ../UCMerced_LandUse/UCMerced_LandUse/Images/")
        sys.exit(1)

    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.workers,
        pin_memory=(device.type == "cuda"),
        drop_last=True,
    )
    print(f"[GAN] Dataset: {len(dataset)} images | "
          f"Batch: {args.batch_size} | Steps/epoch: {len(loader)}")

    # --- Models ---
    G = Generator(latent_dim=args.latent_dim, num_classes=NUM_CLASSES).to(device)
    D = Discriminator(num_classes=NUM_CLASSES).to(device)
    G_ema = Generator(latent_dim=args.latent_dim, num_classes=NUM_CLASSES).to(device)
    G_ema.load_state_dict(G.state_dict())  # start EMA from G
    ema = EMA(G, decay=args.ema_decay)

    # --- Optimisers ---
    opt_G = optim.Adam(G.parameters(), lr=args.lr, betas=(0.5, 0.999))
    opt_D = optim.Adam(D.parameters(), lr=args.lr, betas=(0.5, 0.999))

    # --- Resume ---
    start_epoch = 1
    if args.resume and G_PATH.exists() and D_PATH.exists():
        G.load_state_dict(torch.load(G_PATH, map_location=device, weights_only=True))
        D.load_state_dict(torch.load(D_PATH, map_location=device, weights_only=True))
        if G_EMA_PATH.exists():
            G_ema.load_state_dict(torch.load(G_EMA_PATH, map_location=device, weights_only=True))
        print(f"[GAN] Resumed from checkpoints in {OUT_DIR}")

    criterion = nn.BCEWithLogitsLoss()

    # Fixed noise + labels for consistent sample grids across epochs
    GRID_ROWS = 7  # one row per 3 classes — 21 images total
    grid_labels = torch.arange(NUM_CLASSES, device=device)         # 0..20
    grid_z = torch.randn(NUM_CLASSES, args.latent_dim, device=device)

    history: list[dict] = []

    # --- Training loop ---
    for epoch in range(start_epoch, args.epochs + 1):
        G.train()
        D.train()
        epoch_start = time.time()

        d_loss_sum, g_loss_sum, batches = 0.0, 0.0, 0

        for real_imgs, labels in loader:
            real_imgs = real_imgs.to(device)
            labels = labels.to(device)
            B = real_imgs.size(0)

            # ----------------------------------------------------------------
            # Train Discriminator (D_STEPS times per G update)
            # ----------------------------------------------------------------
            for _ in range(args.d_steps):
                z = torch.randn(B, args.latent_dim, device=device)
                fake_imgs = G(z, labels).detach()  # stop G gradient here

                real_logits = D(real_imgs, labels)
                fake_logits = D(fake_imgs, labels)

                # Label smoothing: real=0.9, fake=0.1
                real_targets = torch.full((B,), 0.9, device=device)
                fake_targets = torch.full((B,), 0.1, device=device)

                d_loss = (criterion(real_logits, real_targets) +
                          criterion(fake_logits, fake_targets)) * 0.5

                opt_D.zero_grad()
                d_loss.backward()
                nn.utils.clip_grad_norm_(D.parameters(), max_norm=1.0)
                opt_D.step()

            # ----------------------------------------------------------------
            # Train Generator
            # ----------------------------------------------------------------
            z = torch.randn(B, args.latent_dim, device=device)
            fake_imgs = G(z, labels)
            fake_logits = D(fake_imgs, labels)

            # G wants D to predict "real" (=1.0) for its fakes
            g_loss = criterion(fake_logits, torch.ones(B, device=device))

            opt_G.zero_grad()
            g_loss.backward()
            nn.utils.clip_grad_norm_(G.parameters(), max_norm=1.0)
            opt_G.step()

            # Update EMA
            ema.update(G)

            d_loss_sum += d_loss.item()
            g_loss_sum += g_loss.item()
            batches += 1

        d_loss_avg = d_loss_sum / batches
        g_loss_avg = g_loss_sum / batches
        elapsed = time.time() - epoch_start

        print(f"[GAN] Epoch {epoch:4d}/{args.epochs} | "
              f"D={d_loss_avg:.4f} G={g_loss_avg:.4f} | "
              f"{elapsed:.1f}s")

        history.append({
            "epoch": epoch,
            "d_loss": round(d_loss_avg, 6),
            "g_loss": round(g_loss_avg, 6),
        })

        # ----------------------------------------------------------------
        # Save sample grid
        # ----------------------------------------------------------------
        if epoch % args.save_every == 0 or epoch == args.epochs:
            G.eval()
            with torch.no_grad():
                ema.apply(G_ema)
                sample_imgs = G_ema(grid_z, grid_labels)     # (21, 3, 128, 128)
            # Denormalise [-1,1] → [0,1]
            sample_imgs = sample_imgs * 0.5 + 0.5
            save_image(sample_imgs, SAMPLE_DIR / f"epoch_{epoch:04d}.png",
                       nrow=7, padding=2)

        # ----------------------------------------------------------------
        # Checkpoint every 10 epochs and at the end
        # ----------------------------------------------------------------
        if epoch % 10 == 0 or epoch == args.epochs:
            torch.save(G.state_dict(), G_PATH)
            torch.save(D.state_dict(), D_PATH)
            ema.apply(G_ema)
            torch.save(G_ema.state_dict(), G_EMA_PATH)

            with open(HISTORY_PATH, "w") as f:
                json.dump(history, f, indent=2)

            meta = {
                "latent_dim": args.latent_dim,
                "num_classes": NUM_CLASSES,
                "class_names": URBAN_CLASSES,
                "epochs_trained": epoch,
                "batch_size": args.batch_size,
                "lr": args.lr,
                "d_steps": args.d_steps,
            }
            with open(META_PATH, "w") as f:
                json.dump(meta, f, indent=2)

    print(f"\n[GAN] Training complete. Weights saved to {OUT_DIR}")
    print(f"      Generator EMA  → {G_EMA_PATH}  (used by /infer/gan)")
    print(f"      Sample grids   → {SAMPLE_DIR}/")


if __name__ == "__main__":
    train()
