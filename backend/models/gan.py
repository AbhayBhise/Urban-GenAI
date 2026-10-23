"""
Conditional DCGAN for urban aerial tile synthesis.

Architecture:
  Generator     — noise z + class label → 128×128 RGB aerial tile
  Discriminator — image (RGB) → feature representation
                  + Projection-conditioning (Miyato et al.)
                  + Auxiliary Classifier (AC-GAN) prediction head

Design choices
--------------
* Class-conditional via label embedding:
  - Generator: concats z and class embedding, projects into 8x8x512 feature map.
  - Discriminator: takes RGB image directly, computes deep spatial features,
    and uses both projection conditioning (y^T V phi(x)) and an auxiliary
    classifier head to enforce class-specific structural geometry
    (e.g., tennis court lines, runways, planes, building roofs).
* Spectral normalisation on every D conv layer stabilises training.
* G uses BatchNorm + ReLU; D uses LeakyReLU.
* Output resolution: 128×128.
"""

import torch
import torch.nn as nn

NUM_CLASSES = 21
LATENT_DIM = 128          # noise vector size
EMBED_DIM = 64            # class-embedding dimension
G_FEAT = 64               # base feature map count for Generator
D_FEAT = 64               # base feature map count for Discriminator


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------
# Generator (Residual Class-Conditional DCGAN Architecture)
# ---------------------------------------------------------------------------

class ResUpBlock(nn.Module):
    """
    Residual upsampling block:
    Interpolates feature maps 2x, processes through two conv layers with BatchNorm & ReLU,
    and adds a 1x1 conv shortcut. Prevents vanishing gradients and checkerboard artifacts,
    allowing the generator to draw crisp polygonal boundaries (e.g. building rooftops, roads).
    """
    def __init__(self, in_c: int, out_c: int):
        super().__init__()
        self.conv1 = nn.Conv2d(in_c, out_c, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_c)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_c, out_c, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_c)
        self.shortcut = nn.Sequential(
            nn.Conv2d(in_c, out_c, 1, 1, 0, bias=False),
            nn.BatchNorm2d(out_c)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = nn.functional.interpolate(x, scale_factor=2, mode='nearest')
        res = self.conv2(self.relu(self.bn1(self.conv1(h))))
        res = self.bn2(res)
        return self.relu(res + self.shortcut(h))


class Generator(nn.Module):
    """
    Maps (z, class_label) → 128×128 RGB image in [-1, 1].

    Architecture:
      Embedding(class) → 64-d vector  ─┐
      Linear(z + embed) → 8×8×(8·G_FEAT)  (project + reshape)
      4 × ResUpBlock stages, each ×2 upsample:
        8×8 → 16×16 → 32×32 → 64×64 → 128×128
      Final 3×3 Conv2d → Tanh → 128×128×3 RGB tile
    """

    def __init__(self, latent_dim: int = LATENT_DIM,
                 num_classes: int = NUM_CLASSES,
                 embed_dim: int = EMBED_DIM,
                 gf: int = G_FEAT):
        super().__init__()
        self.latent_dim = latent_dim
        self.embed = nn.Embedding(num_classes, embed_dim)

        # Project noise + class embed to initial 8×8 spatial feature map.
        self.proj = nn.Linear(latent_dim + embed_dim, 8 * gf * 8 * 8, bias=False)
        self.bn0 = nn.BatchNorm2d(8 * gf)
        self.relu = nn.ReLU(inplace=True)

        # 4 Residual Upsample stages: 8→16→32→64→128
        self.block1 = ResUpBlock(8 * gf, 4 * gf)  # 8×8 → 16×16 (256 ch)
        self.block2 = ResUpBlock(4 * gf, 2 * gf)  # 16×16 → 32×32 (128 ch)
        self.block3 = ResUpBlock(2 * gf, gf)      # 32×32 → 64×64 (64 ch)
        self.block4 = ResUpBlock(gf, gf // 2)     # 64×64 → 128×128 (32 ch)

        # Final projection to 3 RGB channels
        self.to_rgb = nn.Sequential(
            nn.Conv2d(gf // 2, 3, kernel_size=3, stride=1, padding=1, bias=False),
            nn.Tanh()
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.Linear)):
                nn.init.normal_(m.weight, 0.0, 0.02)
                if hasattr(m, 'bias') and m.bias is not None:
                    nn.init.zeros_(m.bias)
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
        e = self.embed(labels)                   # (B, embed_dim)
        x = torch.cat([z, e], dim=1)            # (B, latent_dim + embed_dim)
        x = self.proj(x)                         # (B, 8·gf·64)
        x = x.view(x.size(0), -1, 8, 8)         # (B, 8·gf, 8, 8)
        x = self.relu(self.bn0(x))
        x = self.block1(x)                       # 16×16
        x = self.block2(x)                       # 32×32
        x = self.block3(x)                       # 64×64
        x = self.block4(x)                       # 128×128
        return self.to_rgb(x)                    # (B, 3, 128, 128)



# ---------------------------------------------------------------------------
# Discriminator (with Projection Discriminator + Auxiliary Classification)
# ---------------------------------------------------------------------------

class Discriminator(nn.Module):
    """
    Discriminator with Projection Conditioning and optional AC-GAN head.

    Architecture:
      RGB image (3 channels) → 5 Spectral-Norm Conv layers → 512-d feature vector phi(x).
      Real/Fake Score = Linear(phi(x)) + (y_embed · phi(x))  [Projection Discriminator]
      Class Logits = AuxClassifier(phi(x))                  [AC-GAN classification]
    """

    def __init__(self, num_classes: int = NUM_CLASSES,
                 embed_dim: int = 512,
                 df: int = D_FEAT):
        super().__init__()
        self.num_classes = num_classes

        def sn_conv(in_c, out_c, k=4, s=2, p=1):
            return nn.utils.spectral_norm(
                nn.Conv2d(in_c, out_c, k, s, p, bias=False)
            )

        # Feature extractor directly on 3-channel RGB image
        self.features = nn.Sequential(
            # 128×128 → 64×64
            sn_conv(3, df),
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
        )

        feat_dim = 8 * df * 4 * 4  # 512 * 16 = 8192 or pooled to 512
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        # Real/Fake scalar output
        self.fc_adv = nn.utils.spectral_norm(nn.Linear(8 * df, 1, bias=True))

        # Projection conditioning embedding (maps class label to 8*df feature vector)
        self.embed_proj = nn.utils.spectral_norm(nn.Embedding(num_classes, 8 * df))

        # Auxiliary classifier head (AC-GAN)
        self.fc_cls = nn.Linear(8 * df, num_classes, bias=True)

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.Linear)):
                if hasattr(m, 'weight'):
                    nn.init.normal_(m.weight, 0.0, 0.02)
                if hasattr(m, 'bias') and m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Embedding):
                nn.init.normal_(m.weight, 0.0, 0.02)

    def forward(self, img: torch.Tensor, labels: torch.Tensor | None = None, return_cls: bool = False):
        """
        Args:
            img        : (B, 3, 128, 128) in [-1, 1]
            labels     : (B,) class labels (required for projection score)
            return_cls : whether to return auxiliary class logits
        Returns:
            If return_cls is False:
                score : (B,) scalar real/fake logit
            If return_cls is True:
                score, cls_logits : (B,), (B, num_classes)
        """
        B = img.size(0)
        h = self.features(img)          # (B, 8*df, 4, 4)
        h_pool = self.pool(h).view(B, -1)  # (B, 8*df)

        # Unconditional real/fake logit
        adv_score = self.fc_adv(h_pool).view(B)

        # If labels are provided, apply projection conditioning
        if labels is not None:
            w = self.embed_proj(labels)  # (B, 8*df)
            proj = (h_pool * w).sum(dim=1)  # (B,) inner product
            adv_score = adv_score + proj

        if return_cls:
            cls_logits = self.fc_cls(h_pool)
            return adv_score, cls_logits

        return adv_score
