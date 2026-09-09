import torch
import torch.optim as optim
import torch.nn.functional as F
from dataset import get_eurosat_dataloaders
from models.diffusion import SimpleUNet, DDPM
import os
import argparse

def train(epochs=100, batch_size=64, lr=1e-4, device="cuda" if torch.cuda.is_available() else "cpu"):
    print(f"Training DDPM on {device}...")
    train_loader, _ = get_eurosat_dataloaders(batch_size=batch_size)
    
    # Model Setup
    unet = SimpleUNet(image_channels=3, down_channels=(64, 128, 256), up_channels=(256, 128, 64), out_dim=3).to(device)
    ddpm = DDPM(unet, num_timesteps=1000, device=device)
    
    optimizer = optim.Adam(ddpm.network.parameters(), lr=lr)
    
    os.makedirs("weights", exist_ok=True)
    
    for epoch in range(epochs):
        ddpm.network.train()
        total_loss = 0
        for batch_idx, (images, _) in enumerate(train_loader):
            images = images.to(device)
            optimizer.zero_grad()
            
            # Forward pass: get noisy images and true noise
            x_t, true_noise, t = ddpm(images)
            
            # Predict noise
            predicted_noise = ddpm.network(x_t, t)
            
            # Calculate loss (MSE between predicted and true noise)
            loss = F.mse_loss(predicted_noise, true_noise)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 50 == 0:
                print(f"Epoch [{epoch+1}/{epochs}] Batch {batch_idx}/{len(train_loader)} Loss: {loss.item():.4f}")
                
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}] Average Loss: {avg_loss:.4f}")
        
        if (epoch + 1) % 10 == 0:
            torch.save(ddpm.network.state_dict(), f"weights/diffusion_ep{epoch+1}.pth")
            
    torch.save(ddpm.network.state_dict(), "weights/diffusion.pth")
    print("Training complete, saved weights/diffusion.pth")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10) # 10 for quick testing
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()
    train(epochs=args.epochs, batch_size=args.batch_size)
