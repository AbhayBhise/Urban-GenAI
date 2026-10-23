"""Train the UrbanGenAI image-conditioned scenario diffusion model.

The available UCMerced data has no paired before/after planning labels. The
reproducible training objective therefore learns conditioned reconstruction and
class semantics; future-land-use transformation claims remain out of scope
until paired municipal scenario data is available.
"""

import os
import json
import time
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image

from dataset import get_split_dataloaders, URBAN_CLASSES
from models.diffusion import DiffusionUNet, DDPM

OUTPUT_DIR = '../outputs/diffusion_scenario'
os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def train_diffusion(epochs: int = 50, batch_size: int = 16, lr: float = 2e-4):
    print(f"--- Starting Urban Scenario DDPM Training on {device} for {epochs} epochs ---")
    
    dataloader, _, _ = get_split_dataloaders(batch_size=batch_size, size=128, num_workers=0, train_aug=True)
    
    unet = DiffusionUNet(base_ch=32, num_classes=len(URBAN_CLASSES), condition_channels=3).to(device)
    ddpm = DDPM(unet=unet, timesteps=1000).to(device)
    
    optimizer = torch.optim.AdamW(unet.parameters(), lr=lr, weight_decay=1e-4)
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)
    
    history = []
    
    start_time = time.time()
    for epoch in range(1, epochs + 1):
        ddpm.train()
        total_loss = 0.0
        n_batches = 0
        
        for imgs, labels in dataloader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            loss = ddpm.compute_loss(imgs, labels, condition=imgs)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(unet.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
            n_batches += 1
            
        lr_scheduler.step()
        avg_loss = total_loss / max(1, n_batches)
        history.append({
            "epoch": epoch,
            "loss": float(avg_loss),
            "lr": float(optimizer.param_groups[0]['lr'])
        })
        
        if epoch % 5 == 0 or epoch == epochs:
            elapsed = (time.time() - start_time) / 60.0
            print(f"Epoch [{epoch}/{epochs}] - Loss: {avg_loss:.5f} - Elapsed: {elapsed:.1f}m")
            
            # Save checkpoint
            torch.save(unet.state_dict(), os.path.join(OUTPUT_DIR, 'model.pth'))
            with open(os.path.join(OUTPUT_DIR, 'history.json'), 'w') as f:
                json.dump(history, f, indent=2)

            with open(os.path.join(OUTPUT_DIR, 'meta.json'), 'w') as f:
                json.dump({
                    "model": "urban_scenario_image_conditioned_ddpm",
                    "dataset": "UCMerced LandUse",
                    "split": "stratified train split from backend/splits.py; condition=source tile",
                    "epochs_trained": epoch,
                    "timesteps": 1000,
                    "conditioning": "source image + target land-use class",
                    "sampling": "DDIM",
                    "sampling_steps": 20,
                    "device": str(device),
                }, f, indent=2)
                
    print("DDPM Training finished successfully.")

if __name__ == '__main__':
    train_diffusion(epochs=50)
