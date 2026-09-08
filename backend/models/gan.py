"""
Conditional DCGAN for urban aerial tile synthesis.

Architecture:
  Generator   — noise z + class label → 128×128 RGB aerial tile
  Discriminator — image + class label → real / fake score

Design choices
--------------
* Class-conditional via label embedding injected into both G and D.
  This lets the model learn class-specific structure (runways look very
  different from forest) rather than a single blurry average.
* Spectral normalisation on every D layer stabilises training and
  prevents mode collapse — a common failure mode on small datasets
  like UCMerced (21 classes × 100 images each).
* G uses BatchNorm + ReLU (standard DCGAN recipe).
* D uses LeakyReLU; no BN on the first layer (also standard).
* Output resolution 128×128 matches the AE/VAE pipeline.
"""

import torch
import torch.nn as nn

# Number of UCMerced land-use classes — must match dataset.URBAN_CLASSES.
NUM_CLASSES = 21
LATENT_DIM = 128          # noise vector size
EMBED_DIM = 64            # class-embedding dimension
G_FEAT = 64               # base feature map count for Generator
D_FEAT = 64               # base feature map count for Discriminator


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class Generator(nn.Module):
    """
    Maps (z, class_label) → 128×128 RGB image in [-1, 1].

    Architecture:
      Embedding(class) → 64-d vector  ─┐
      Linear(z + embed) → 8×8×(8·G_FEAT)  (project + reshape)
      4 × ConvTranspose2d stages, each ×2 upsample:
        8×8 → 16×16 → 32×32 → 64×64 → 128×128
    """

    def __init__(self, latent_dim: int = LATENT_DIM,
                 num_classes: int = NUM_CLASSES,
                 embed_dim: int = EMBED_DIM,
                 gf: int = G_FEAT):
        super().__init__()
        self.latent_dim = latent_dim
        self.embed = nn.Embedding(num_classes, embed_dim)

        # Project noise + class embed to initial 8×8 spatial feature map.
        self.proj = nn.Sequential(
            nn.Linear(latent_dim + embed_dim, 8 * gf * 8 * 8, bias=False),
        )

        # 4 upsample stages: 8→16→32→64→128
        self.main = nn.Sequential(
            # stage 1: 8×8 → 16×16
            nn.ConvTranspose2d(8 * gf, 4 * gf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(4 * gf),
            nn.ReLU(inplace=True),
            # stage 2: 16×16 → 32×32
            nn.ConvTranspose2d(4 * gf, 2 * gf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(2 * gf),
            nn.ReLU(inplace=True),
            # stage 3: 32×32 → 64×64
            nn.ConvTranspose2d(2 * gf, gf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(gf),
            nn.ReLU(inplace=True),
            # stage 4: 64×64 → 128×128
            nn.ConvTranspose2d(gf, 3, 4, 2, 1, bias=False),
            nn.Tanh(),
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, (nn.ConvTranspose2d, nn.Linear)):
                nn.init.normal_(m.weight, 0.0, 0.02)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.normal_(m.weight, 1.0, 0.02)
                nn.init.zeros_(m.bias)

    def forward(self, z: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """
        Args:
            z      : (B, latent_dim) noise vector
            labels : (B,) integer class indices
        Returns:
            images : (B, 3, 128, 128) in [-1, 1]
        """
        e = self.embed(labels)            # (B, embed_dim)
        x = torch.cat([z, e], dim=1)     # (B, latent_dim + embed_dim)
        x = self.proj(x)                  # (B, 8·gf·64)
        x = x.view(x.size(0), -1, 8, 8)  # (B, 8·gf, 8, 8)
        return self.main(x)               # (B, 3, 128, 128)


# ---------------------------------------------------------------------------
# Discriminator
# ---------------------------------------------------------------------------

class Discriminator(nn.Module):
    """
    Maps (image, class_label) → scalar real/fake score (pre-sigmoid logit).

    Architecture:
      class embed projected to (C, 128, 128) and channel-concatenated with
      the image before the first conv — simplest conditional injection.
      5 strided-conv stages reduce 128×128 → 4×4 → scalar.
      Spectral normalisation on every conv for training stability.
    """

    def __init__(self, num_classes: int = NUM_CLASSES,
                 embed_dim: int = EMBED_DIM,
                 df: int = D_FEAT):
        super().__init__()
        self.embed = nn.Embedding(num_classes, embed_dim)
        # Project embed to a per-pixel map matching the image spatial size
        self.embed_proj = nn.Linear(embed_dim, 128 * 128, bias=False)

        in_channels = 3 + 1  # RGB image + 1 projected class channel

        def sn_conv(in_c, out_c, k=4, s=2, p=1):
            return nn.utils.spectral_norm(
                nn.Conv2d(in_c, out_c, k, s, p, bias=False)
            )

        self.main = nn.Sequential(
            # 128×128 → 64×64
            sn_conv(in_channels, df),
            nn.LeakyReLU(0.2, inplace=True),
            # 64×64 → 32×32
            sn_conv(df, 2 * df),
            nn.LeakyReLU(0.2, inplace=True),
            # 32×32 → 16×16
            sn_conv(2 * df, 4 * df),
            nn.LeakyReLU(0.2, inplace=True),
            # 16×16 → 8×8
            sn_conv(4 * df, 8 * df),
            nn.LeakyReLU(0.2, inplace=True),
            # 8×8 → 4×4
            sn_conv(8 * df, 8 * df),
            nn.LeakyReLU(0.2, inplace=True),
            # 4×4 → 1×1 (no padding)
            nn.utils.spectral_norm(
                nn.Conv2d(8 * df, 1, 4, 1, 0, bias=False)
            ),
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, 0.0, 0.02)

    def forward(self, img: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """
        Args:
            img    : (B, 3, 128, 128) in [-1, 1]
            labels : (B,) integer class indices
        Returns:
            logits : (B,) pre-sigmoid real/fake score
        """
        B = img.size(0)
        e = self.embed(labels)                        # (B, embed_dim)
        e = self.embed_proj(e)                        # (B, 128*128)
        e = e.view(B, 1, 128, 128)                    # (B, 1, 128, 128)
        x = torch.cat([img, e], dim=1)               # (B, 4, 128, 128)
        return self.main(x).view(B)                   # (B,)
