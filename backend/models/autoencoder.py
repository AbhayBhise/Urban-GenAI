import torch
import torch.nn as nn
import torchvision.models as models


class DenoisingAE(nn.Module):
    """Denoising autoencoder with a pretrained ResNet18 encoder and U-Net-style
    skip connections to the decoder.

    The original version decoded purely from the 8x8x256 bottleneck (16x
    spatial downsampling), which measurably loses fine detail on tiles with
    many small distinct structures (dense residential, harbor, mobile home
    parks scored ~21dB PSNR vs ~27-28dB for homogeneous classes like forest/
    agricultural) -- the bottleneck simply has nowhere to put that detail.

    Skip connections (Ronneberger et al. 2015, U-Net) concatenate encoder
    activations directly into the matching decoder stage, giving the decoder
    a second, unbottlenecked path back to fine spatial detail instead of
    forcing everything through the 8x8 bottleneck. This is a capacity fix,
    not a loss-function change: the bottleneck (s3) is still what a
    downstream consumer would use as "the compressed representation"; the
    skips only help the decoder reconstruct around it.
    """

    def __init__(self):
        super().__init__()
        resnet = models.resnet18(weights='IMAGENET1K_V1')
        self.stem = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu)  # 128x128 -> 64x64x64
        self.maxpool = resnet.maxpool                                     # -> 32x32x64
        self.layer1 = resnet.layer1                                       # 32x32x64
        self.layer2 = resnet.layer2                                       # 16x16x128
        self.layer3 = resnet.layer3                                       # 8x8x256

        self.up1 = nn.ConvTranspose2d(256, 128, 4, 2, 1)   # 8x8 -> 16x16
        self.dec1 = nn.Sequential(
            nn.Conv2d(128 + 128, 128, 3, 1, 1), nn.BatchNorm2d(128), nn.ReLU(inplace=True),
        )
        self.up2 = nn.ConvTranspose2d(128, 64, 4, 2, 1)    # 16x16 -> 32x32
        self.dec2 = nn.Sequential(
            nn.Conv2d(64 + 64, 64, 3, 1, 1), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
        )
        self.up3 = nn.ConvTranspose2d(64, 32, 4, 2, 1)     # 32x32 -> 64x64
        self.dec3 = nn.Sequential(
            nn.Conv2d(32 + 64, 32, 3, 1, 1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
        )
        self.up4 = nn.ConvTranspose2d(32, 3, 4, 2, 1)      # 64x64 -> 128x128
        self.out_act = nn.Tanh()

    def _encoder_modules(self):
        return [self.stem, self.layer1, self.layer2, self.layer3]

    def set_encoder_trainable(self, trainable: bool):
        for module in self._encoder_modules():
            for p in module.parameters():
                p.requires_grad = trainable

    def encode(self, x):
        """Returns the bottleneck feature map (8x8x256) plus the skip
        activations the decoder needs. The bottleneck alone is the
        "compressed representation" in the traditional AE sense."""
        s0 = self.stem(x)
        p0 = self.maxpool(s0)
        s1 = self.layer1(p0)
        s2 = self.layer2(s1)
        s3 = self.layer3(s2)
        return s3, (s0, s1, s2)

    def forward(self, x):
        bottleneck, (s0, s1, s2) = self.encode(x)

        d1 = self.up1(bottleneck)
        d1 = self.dec1(torch.cat([d1, s2], dim=1))

        d2 = self.up2(d1)
        d2 = self.dec2(torch.cat([d2, s1], dim=1))

        d3 = self.up3(d2)
        d3 = self.dec3(torch.cat([d3, s0], dim=1))

        d4 = self.up4(d3)
        return self.out_act(d4)


# Backwards-compatible alias
Autoencoder = DenoisingAE
