import torch
import torch.nn as nn
import torchvision.models as models


class VAE(nn.Module):
    """Spatial-latent VAE with a detail path and a live latent.

    The encoder is a pretrained ResNet18 up to layer3, producing an 8x8 grid
    of 64 latent channels (4096 dimensions). Keeping the latent spatial rather
    than flattening it preserves parcel, road, and building layout, which is
    what makes interpolation and reconstruction-error anomaly maps meaningful
    for overhead urban imagery.

    A full skip-connected decoder reconstructs sharp tiles but lets the decoder
    ignore the latent, collapsing the KL term. This model therefore uses
    *compact* skips: encoder features are projected to a small number of
    channels and the highest-resolution skip is dropped. The decoder cannot
    recover fine detail from those narrow skips alone, so the latent must stay
    informative, while the mid-resolution skips still preserve large structures
    and keep reconstruction sharp. Skip dropout during training further
    prevents the decoder from over-relying on the detail path.
    """

    def __init__(self, latent_channels=64, use_skips=True, skip_dropout=0.2,
                 skip_channels=16, skip0_channels=16):
        super().__init__()
        resnet = models.resnet18(weights='IMAGENET1K_V1')
        self.use_skips = use_skips
        self.skip_dropout = skip_dropout
        self.stem = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu)  # 64x64x64
        self.maxpool = resnet.maxpool                                      # 32x32x64
        self.layer1 = resnet.layer1                                        # 32x32x64
        self.layer2 = resnet.layer2                                        # 16x16x128
        self.layer3 = resnet.layer3                                        # 8x8x256

        self.mu_head = nn.Conv2d(256, latent_channels, 1)
        self.logvar_head = nn.Conv2d(256, latent_channels, 1)
        self.latent_proj = nn.Conv2d(latent_channels, 256, 1)

        self.skip_channels = skip_channels if use_skips else 0
        self.skip0_channels = skip0_channels if use_skips else 0
        if use_skips:
            self.skip2 = nn.Conv2d(128, skip_channels, 1, bias=False)
            self.skip1 = nn.Conv2d(64, skip_channels, 1, bias=False)
            self.skip0 = nn.Conv2d(64, skip0_channels, 1, bias=False)
            self.dec1 = nn.Sequential(
                nn.Conv2d(128 + skip_channels, 128, 3, 1, 1),
                nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            )
            self.dec2 = nn.Sequential(
                nn.Conv2d(64 + skip_channels, 64, 3, 1, 1),
                nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            )
            self.dec3 = nn.Sequential(
                nn.Conv2d(32 + skip0_channels, 32, 3, 1, 1),
                nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            )
        else:
            self.dec1 = nn.Sequential(
                nn.Conv2d(128, 128, 3, 1, 1),
                nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            )
            self.dec2 = nn.Sequential(
                nn.Conv2d(64, 64, 3, 1, 1),
                nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            )
            self.dec3 = nn.Sequential(
                nn.Conv2d(32, 32, 3, 1, 1),
                nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            )
        self.up1 = nn.ConvTranspose2d(256, 128, 4, 2, 1)   # 8 -> 16
        self.up2 = nn.ConvTranspose2d(128, 64, 4, 2, 1)    # 16 -> 32
        self.up3 = nn.ConvTranspose2d(64, 32, 4, 2, 1)     # 32 -> 64
        self.up4 = nn.ConvTranspose2d(32, 3, 4, 2, 1)      # 64 -> 128
        self.out_act = nn.Tanh()

    def set_encoder_trainable(self, trainable: bool):
        for module in (self.stem, self.layer1, self.layer2, self.layer3):
            for p in module.parameters():
                p.requires_grad = trainable

    def encode_with_skips(self, x):
        s0 = self.stem(x)
        p0 = self.maxpool(s0)
        s1 = self.layer1(p0)
        s2 = self.layer2(s1)
        s3 = self.layer3(s2)
        mu = self.mu_head(s3)
        logvar = torch.clamp(self.logvar_head(s3), min=-20, max=20)
        return mu, logvar, (s0, s1, s2)

    def encode(self, x):
        mu, logvar, _ = self.encode_with_skips(x)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z, skips=None):
        x = self.latent_proj(z)
        if self.use_skips:
            if skips is None:
                b, _, h, w = x.shape
                s2 = torch.zeros(b, self.skip_channels, h * 2, w * 2, device=x.device, dtype=x.dtype)
                s1 = torch.zeros(b, self.skip_channels, h * 4, w * 4, device=x.device, dtype=x.dtype)
                s0 = torch.zeros(b, self.skip0_channels, h * 8, w * 8, device=x.device, dtype=x.dtype)
            else:
                s0, s1, s2 = skips
                s2 = self.skip2(s2)
                s1 = self.skip1(s1)
                s0 = self.skip0(s0)
        else:
            s0 = s1 = s2 = None

        d1 = self.up1(x)
        if s2 is not None:
            d1 = self.dec1(torch.cat([d1, s2], dim=1))
        else:
            d1 = self.dec1(d1)

        d2 = self.up2(d1)
        if s1 is not None:
            d2 = self.dec2(torch.cat([d2, s1], dim=1))
        else:
            d2 = self.dec2(d2)

        d3 = self.up3(d2)
        if s0 is not None:
            d3 = self.dec3(torch.cat([d3, s0], dim=1))
        else:
            d3 = self.dec3(d3)
        return self.out_act(self.up4(d3))

    def reconstruct(self, x):
        mu, logvar, skips = self.encode_with_skips(x)
        return self.decode(mu, skips), mu, logvar

    def forward(self, x):
        mu, logvar, skips = self.encode_with_skips(x)
        z = self.reparameterize(mu, logvar)
        if self.training and self.skip_dropout > 0:
            keep = (torch.rand(mu.size(0), 1, 1, 1, device=mu.device) >= self.skip_dropout).to(mu.dtype)
            skips = tuple(s * keep for s in skips)
        recon = self.decode(z, skips)
        return recon, mu, logvar


def kl_divergence(mu, logvar):
    """Analytic KL( q(z|x) || N(0, I) ) for a diagonal-Gaussian posterior."""
    kl_map = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp())
    per_image = kl_map.sum(dim=[1, 2, 3])
    kl_mean = per_image.mean().item()
    n_dims = mu[0].numel()
    return kl_mean, kl_mean / n_dims
