import torch
import torch.nn as nn
import torchvision.models as models


class VAE(nn.Module):
    """Spatial-latent VAE with a pretrained ResNet18 encoder.

    Priority here is reconstruction fidelity, not textbook prior-sampling
    correctness — that's a deliberate choice (see train_vae.py) after
    verifying empirically that a real, non-negligible KL weight measurably
    degrades reconstruction on this dataset (up to full posterior collapse
    at higher weights), and this project's use case (denoising/latent
    exploration/anomaly detection) cares more about the former. Keeping the
    latent as an 8x8 grid of codes (4096 total dims) — rather than
    collapsing to a small flat vector — preserves far more spatial detail
    (roads, field boundaries, buildings) than a low-capacity bottleneck
    could, which is what actually matters for this goal.
    """

    def __init__(self, latent_channels=64):
        super().__init__()
        resnet = models.resnet18(weights='IMAGENET1K_V1')
        self.encoder = nn.Sequential(
            resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool,
            resnet.layer1, resnet.layer2, resnet.layer3
        )  # 128x128 input -> 8x8x256

        self.mu_head = nn.Conv2d(256, latent_channels, 1)
        self.logvar_head = nn.Conv2d(256, latent_channels, 1)
        self.latent_proj = nn.Conv2d(latent_channels, 256, 1)

        # Decoder must upsample by exactly 16x (4 stride-2 stages) to get
        # back to 128x128 — see models/autoencoder.py for why this matters.
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(32, 3, 4, 2, 1), nn.Tanh(),
        )

    def set_encoder_trainable(self, trainable: bool):
        for p in self.encoder.parameters():
            p.requires_grad = trainable

    def encode(self, x):
        h = self.encoder(x)
        mu = self.mu_head(h)
        logvar = self.logvar_head(h)
        logvar = torch.clamp(logvar, min=-20, max=20)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        x = self.latent_proj(z)
        return self.decoder(x)

    def reconstruct(self, x):
        """Reconstruct an input deterministically using the posterior mean.

        Sampling the posterior is useful during training, but it injects
        random noise into a reconstruction and can make the displayed image
        look washed out or change on every request.  The posterior mean is
        the standard deterministic path for reconstruction and anomaly
        scoring.
        """
        mu, logvar = self.encode(x)
        return self.decode(mu), mu, logvar

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z)
        return recon, mu, logvar
