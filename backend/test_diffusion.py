import torch
from models.diffusion import SimpleUNet, DDPM

def test_diffusion():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Testing on {device}")
    
    try:
        # Create U-Net
        unet = SimpleUNet(image_channels=3, out_dim=3).to(device)
        print("U-Net created successfully.")
        
        # Create DDPM
        ddpm = DDPM(network=unet, num_timesteps=100, device=device).to(device)
        print("DDPM created successfully.")
        
        # Test forward process
        x_0 = torch.randn(2, 3, 32, 32).to(device)
        x_t, noise, t = ddpm(x_0)
        print(f"Forward pass output shapes: x_t={x_t.shape}, noise={noise.shape}, t={t.shape}")
        
        # Test sample
        samples = ddpm.sample(num_samples=2, image_size=32, channels=3)
        print(f"Sample output shape: {samples.shape}")
        
        print("All diffusion model tests passed!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    test_diffusion()
