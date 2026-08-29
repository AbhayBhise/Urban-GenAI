import os
import torch
import torchvision.utils as vutils
from models.vae import VAE

def generate_images(num_images=16, latent_dim=128, output_dir='../outputs/generated'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    os.makedirs(output_dir, exist_ok=True)

    model = VAE(latent_dim=latent_dim).to(device)
    model.load_state_dict(torch.load('../outputs/vae/model.pth', map_location=device, weights_only=True))
    model.eval()

    print(f"Generating {num_images} fake urban images...")
    with torch.no_grad():
        # With a properly-weighted, unclamped KL term the latent should
        # actually approximate N(0,1) — see models/vae.py and train_vae.py —
        # so sampling straight from the prior should decode to plausible
        # (if soft) tiles rather than flat/gray garbage.
        z = torch.randn(num_images, latent_dim).to(device)
        fake_images = model.decode(z)
        
        # Denormalize from [-1, 1] to [0, 1]
        fake_images = (fake_images + 1) / 2.0
        fake_images = torch.clamp(fake_images, 0, 1)
        
        vutils.save_image(fake_images, os.path.join(output_dir, 'fake_urban_grid.png'), nrow=4)
        
        for i in range(num_images):
            vutils.save_image(fake_images[i:i+1], os.path.join(output_dir, f'fake_{i}.png'))
            
    print(f"Images saved to {output_dir}")

if __name__ == '__main__':
    generate_images()
