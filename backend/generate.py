import os
import torch
import torchvision.utils as vutils
from models.vae import VAE

LATENT_CHANNELS = 64


def generate_images(num_images=16, output_dir='../outputs/generated',
                    ckpt='../outputs/vae/model.pth'):
    """Diagnostic: decode random draws from the prior N(0, I).

    NOTE: the VAE is trained with a near-zero KL weight (reconstruction
    priority), so its latent does NOT match the prior and these samples are
    expected to look like noise. The meaningful latent-space demo is
    interpolation between two real encoded tiles — see
    train_vae.py:generate_interpolation and the /infer/vae/interpolate API.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    if not os.path.exists(ckpt):
        raise SystemExit(f"{ckpt} not found. Run: python train_vae.py")
    os.makedirs(output_dir, exist_ok=True)

    model = VAE(latent_channels=LATENT_CHANNELS).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device, weights_only=True))
    model.eval()

    print(f"Generating {num_images} synthetic tiles...")
    with torch.no_grad():
        z = torch.randn(num_images, LATENT_CHANNELS, 8, 8, device=device)
        fake_images = model.decode(z)
        fake_images = torch.clamp((fake_images + 1) / 2.0, 0, 1)

        vutils.save_image(fake_images, os.path.join(output_dir, 'fake_urban_grid.png'), nrow=4)
        for i in range(num_images):
            vutils.save_image(fake_images[i:i + 1], os.path.join(output_dir, f'fake_{i}.png'))

    print(f"Images saved to {output_dir}")


if __name__ == '__main__':
    generate_images()
