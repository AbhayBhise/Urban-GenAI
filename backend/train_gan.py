"""
High-Fidelity Training Script for Conditional DCGAN with Projection Discriminator
and class guidance. The generator objective avoids paired feature/pixel targets:
those targets are not aligned with a random latent sample and were encouraging
the generator to average unrelated tiles into blurry class prototypes.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import transforms
from torchvision.utils import save_image, make_grid
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))

from models.gan import Generator, Discriminator, LATENT_DIM, NUM_CLASSES
from models.classifier import UrbanClassifier
from dataset import UCMercedDataset, URBAN_CLASSES

OUT_DIR = Path("../outputs/gan")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR = OUT_DIR / "samples"
SAMPLE_DIR.mkdir(exist_ok=True)

G_PATH = OUT_DIR / "generator.pth"
D_PATH = OUT_DIR / "discriminator.pth"
G_EMA_PATH = OUT_DIR / "generator_ema.pth"
HISTORY_PATH = OUT_DIR / "history.json"
META_PATH = OUT_DIR / "meta.json"


def get_args():
    p = argparse.ArgumentParser(description="Train Conditional DCGAN with Projection and Classifier Guidance")
    p.add_argument("--epochs", type=int, default=50, help="Number of training epochs (default: 50)")
    p.add_argument("--batch-size", type=int, default=32, help="Batch size (default: 32)")
    p.add_argument("--lr", type=float, default=2e-4, help="Learning rate (default: 2e-4)")
    p.add_argument("--d-steps", type=int, default=1, help="D updates per G update (default: 1)")
    p.add_argument("--latent-dim", type=int, default=LATENT_DIM, help=f"Noise vector size (default: {LATENT_DIM})")
    p.add_argument("--ema-decay", type=float, default=0.999, help="EMA decay (default: 0.999)")
    p.add_argument("--save-every", type=int, default=10, help="Save sample grid every N epochs (default: 10)")
    p.add_argument("--fresh", action="store_true", help="Ignore existing checkpoints and train from scratch")
    return p.parse_args()


class EMA:
    def __init__(self, model: nn.Module, decay: float = 0.999):
        self.decay = decay
        self.shadow = {k: v.clone().detach() for k, v in model.state_dict().items()}

    def update(self, model: nn.Module):
        with torch.no_grad():
            for k, v in model.state_dict().items():
                self.shadow[k] = self.decay * self.shadow[k] + (1 - self.decay) * v

    def apply(self, model: nn.Module):
        model.load_state_dict(self.shadow)


def train():
    args = get_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GAN] Using device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    # Aerial scenes have no canonical up direction. Reusing each tile with
    # orientation-preserving flips/quarter-turns increases the effective
    # variety without inventing labels or mixing classes. Mild colour jitter
    # covers sensor/illumination variation while retaining land-use geometry.
    gan_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomChoice([
            transforms.Lambda(lambda img, angle=angle: img.rotate(angle))
            for angle in (0, 90, 180, 270)
        ]),
        transforms.ColorJitter(brightness=0.08, contrast=0.08, saturation=0.06, hue=0.02),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    raw_dataset = UCMercedDataset(transform=gan_transform)
    if len(raw_dataset) == 0:
        print("[GAN] ERROR: UCMerced dataset not found.")
        sys.exit(1)

    print(f"[GAN] Preloading {len(raw_dataset)} dataset images into RAM memory...")
    t0 = time.time()
    all_imgs = []
    all_labels = []
    for i in range(len(raw_dataset)):
        img, lbl = raw_dataset[i]
        all_imgs.append(img)
        all_labels.append(lbl)

    tensor_imgs = torch.stack(all_imgs)
    tensor_labels = torch.tensor(all_labels, dtype=torch.long)
    print(f"[GAN] Preloaded in {time.time()-t0:.1f}s! Tensor shape: {tensor_imgs.shape}")

    mem_dataset = TensorDataset(tensor_imgs, tensor_labels)
    loader = DataLoader(
        mem_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        drop_last=True
    )

    # Models
    G = Generator(latent_dim=args.latent_dim, num_classes=NUM_CLASSES).to(device)
    D = Discriminator(num_classes=NUM_CLASSES).to(device)
    G_ema = Generator(latent_dim=args.latent_dim, num_classes=NUM_CLASSES).to(device)

    # Resume from existing checkpoints unless a fresh run was requested.
    start_epoch = 1
    if not args.fresh and D_PATH.exists():
        try:
            D.load_state_dict(torch.load(D_PATH, map_location=device, weights_only=True))
            print("[GAN] Resumed Discriminator weights from checkpoint!")
        except Exception as e:
            print(f"[GAN] Discriminator starting fresh: {e}")

    if not args.fresh and G_PATH.exists():
        try:
            G.load_state_dict(torch.load(G_PATH, map_location=device, weights_only=True))
            print("[GAN] Resumed Generator weights from checkpoint!")
            if HISTORY_PATH.exists():
                with open(HISTORY_PATH, "r") as f:
                    history = json.load(f)
                    if history:
                        start_epoch = history[-1]["epoch"] + 1
        except Exception as e:
            print(f"[GAN] Generator starting with upgraded ResNet-DCGAN architecture ({e})")
            start_epoch = 1

    G_ema.load_state_dict(G.state_dict())
    ema = EMA(G, decay=args.ema_decay)

    # Pretrained UrbanClassifier (ResNet18) for auxiliary perceptual guidance
    clf = UrbanClassifier().to(device)
    clf_path = Path("../outputs/transformer/model.pth")
    has_classifier = False
    if clf_path.exists():
        try:
            clf.load_state_dict(torch.load(clf_path, map_location=device))
            clf.eval()
            for p in clf.parameters():
                p.requires_grad = False
            has_classifier = True
            feats = {}
            def _get_hook(name):
                def _hook(m, inp, outp):
                    feats[name] = outp
                return _hook
            clf.model.layer2.register_forward_hook(_get_hook('layer2'))
            clf.model.layer3.register_forward_hook(_get_hook('layer3'))
            print("[GAN] Successfully loaded pretrained UrbanClassifier (ResNet18) for class-guidance loss!")
        except Exception as e:
            print(f"[GAN] Warning: could not load classifier: {e}")

    # Standard ImageNet normalization constants for ResNet18
    mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)

    opt_G = optim.Adam(G.parameters(), lr=args.lr, betas=(0.0, 0.99))
    opt_D = optim.Adam(D.parameters(), lr=args.lr, betas=(0.0, 0.99))

    criterion_bce = nn.BCEWithLogitsLoss()
    criterion_ce = nn.CrossEntropyLoss()

    grid_labels = torch.arange(NUM_CLASSES, device=device)
    grid_z = torch.randn(NUM_CLASSES, args.latent_dim, device=device)

    if 'history' not in locals():
        history = []

    total_target_epochs = max(args.epochs, start_epoch + args.epochs - 1) if start_epoch > 1 else args.epochs
    print(f"[GAN] Commencing training from epoch {start_epoch} to {total_target_epochs} with adversarial/class/diversity objectives...")

    for epoch in range(start_epoch, total_target_epochs + 1):
        G.train()
        D.train()
        epoch_start = time.time()

        d_loss_sum, g_loss_sum = 0.0, 0.0
        batches = 0

        for real_imgs, labels in loader:
            real_imgs = real_imgs.to(device)
            labels = labels.to(device)
            B = real_imgs.size(0)

            # ----------------------------------------------------
            # 1. Train Discriminator
            # ----------------------------------------------------
            opt_D.zero_grad()

            real_adv, real_cls = D(real_imgs, labels, return_cls=True)
            d_real_loss = criterion_bce(real_adv, torch.full((B,), 0.9, device=device))
            d_real_cls_loss = criterion_ce(real_cls, labels)

            z = torch.randn(B, args.latent_dim, device=device)
            fake_imgs = G(z, labels).detach()
            fake_adv, fake_cls = D(fake_imgs, labels, return_cls=True)
            d_fake_loss = criterion_bce(fake_adv, torch.full((B,), 0.1, device=device))

            d_loss = d_real_loss + d_fake_loss + 0.5 * d_real_cls_loss
            d_loss.backward()
            nn.utils.clip_grad_norm_(D.parameters(), max_norm=2.0)
            opt_D.step()

            # ----------------------------------------------------
            # 2. Train Generator
            # ----------------------------------------------------
            opt_G.zero_grad()

            z = torch.randn(B, args.latent_dim, device=device)
            gen_imgs = G(z, labels)
            gen_adv, gen_cls = D(gen_imgs, labels, return_cls=True)

            g_adv_loss = criterion_bce(gen_adv, torch.ones(B, device=device))
            g_cls_loss = criterion_ce(gen_cls, labels)

            g_guidance_loss = torch.tensor(0.0, device=device)
            if has_classifier:
                # Map [-1, 1] -> [0, 1] then apply ImageNet normalization
                gen_01 = (gen_imgs + 1.0) * 0.5
                gen_norm = (gen_01 - mean) / std
                gen_224 = F.interpolate(gen_norm, size=(224, 224), mode='bilinear', align_corners=False)

                real_01 = (real_imgs + 1.0) * 0.5
                real_norm = (real_01 - mean) / std
                real_224 = F.interpolate(real_norm, size=(224, 224), mode='bilinear', align_corners=False)

                clf_logits = clf(gen_224)
                g_guidance_loss = criterion_ce(clf_logits, labels)

            # Diversity loss to penalize mode collapse across latent codes
            half = B // 2
            if half > 0:
                l1_img_diff = (gen_imgs[:half] - gen_imgs[half:2*half]).abs().mean(dim=[1, 2, 3])
                l1_z_diff = (z[:half] - z[half:2*half]).abs().mean(dim=1) + 1e-5
                diversity_loss = -torch.mean(l1_img_diff / l1_z_diff)
            else:
                diversity_loss = torch.tensor(0.0, device=device)

            # No paired feature/edge reconstruction term: the real tile in this
            # batch is not the target for this latent code. Those terms caused
            # averaging, which is exactly the blur/mode-collapse seen in UI.
            g_loss = g_adv_loss + 0.5 * g_cls_loss + 0.5 * g_guidance_loss + 0.08 * diversity_loss
            g_loss.backward()
            nn.utils.clip_grad_norm_(G.parameters(), max_norm=2.0)
            opt_G.step()

            ema.update(G)

            d_loss_sum += d_loss.item()
            g_loss_sum += g_loss.item()
            batches += 1

        d_avg = d_loss_sum / batches
        g_avg = g_loss_sum / batches
        elapsed = time.time() - epoch_start

        if epoch % 5 == 0 or epoch == start_epoch or epoch == total_target_epochs:
            print(f"[GAN] Epoch {epoch:3d}/{total_target_epochs} | D_loss={d_avg:.4f} G_loss={g_avg:.4f} | {elapsed:.1f}s/epoch")

        history.append({
            "epoch": epoch,
            "d_loss": round(d_avg, 6),
            "g_loss": round(g_avg, 6)
        })

        if epoch % args.save_every == 0 or epoch == total_target_epochs:
            G.eval()
            with torch.no_grad():
                ema.apply(G_ema)
                sample_imgs = G_ema(grid_z, grid_labels)
            sample_imgs = sample_imgs * 0.5 + 0.5
            save_image(sample_imgs, SAMPLE_DIR / f"epoch_{epoch:04d}.png", nrow=7, padding=2)

        if epoch % 10 == 0 or epoch == total_target_epochs:
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
                "architecture": "Projection DCGAN + AC-GAN Auxiliary Guidance",
            }
            with open(META_PATH, "w") as f:
                json.dump(meta, f, indent=2)

    print(f"\n[GAN] Training completed successfully!")
    print(f"      Checkpoints saved in {OUT_DIR}")


if __name__ == "__main__":
    train()
