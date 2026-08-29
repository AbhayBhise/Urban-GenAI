import os
import time
import json
import torch
import torch.nn.functional as F
from torchvision.utils import save_image
from dataset import get_dataloaders
from models.autoencoder import DenoisingAE

FREEZE_ENCODER_EPOCHS = 5
EPOCHS = 50
BATCH_SIZE = 16
LR = 1e-4
NOISE_STD = 0.15


def add_noise(imgs, noise_std=NOISE_STD):
    return torch.clamp(imgs + noise_std * torch.randn_like(imgs), -1.0, 1.0)


def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    train_loader, _ = get_dataloaders(batch_size=BATCH_SIZE)

    model = DenoisingAE().to(device)
    model.set_encoder_trainable(False)

    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    history = []
    os.makedirs('../outputs/ae/samples', exist_ok=True)
    print(f"Starting Denoising AE training ({EPOCHS} epochs, encoder frozen for first {FREEZE_ENCODER_EPOCHS})...")

    for epoch in range(EPOCHS):
        if epoch == FREEZE_ENCODER_EPOCHS:
            model.set_encoder_trainable(True)
            print(f"Epoch {epoch+1}: unfreezing encoder")

        model.train()
        total_loss = 0
        start = time.time()
        for batch_idx, (imgs, _) in enumerate(train_loader):
            imgs = imgs.to(device)
            noisy = add_noise(imgs)

            optimizer.zero_grad()
            recon = model(noisy)
            loss = F.mse_loss(recon, imgs)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item()
            if batch_idx % 10 == 0:
                print(f"Epoch {epoch+1}/{EPOCHS} | Batch {batch_idx}/{len(train_loader)} | Loss: {loss.item():.4f}")

        avg_loss = total_loss / len(train_loader)
        history.append({"epoch": epoch + 1, "loss": avg_loss})
        print(f"Epoch {epoch+1} done in {time.time()-start:.1f}s | Avg Loss: {avg_loss:.4f}")

        if (epoch + 1) % 5 == 0:
            with torch.no_grad():
                sample_noisy = noisy[:8]
                sample_recon = recon[:8]
                sample_clean = imgs[:8]
                grid = torch.cat([sample_noisy, sample_recon, sample_clean], dim=0)
                grid = (grid + 1) / 2
                save_image(grid, f'../outputs/ae/samples/epoch_{epoch+1}.png', nrow=8)

        os.makedirs('../outputs/ae', exist_ok=True)
        torch.save(model.state_dict(), '../outputs/ae/model.pth')

    with open('../outputs/ae/history.json', 'w') as f:
        json.dump(history, f)
    print("Autoencoder training complete.")


if __name__ == '__main__':
    train()
