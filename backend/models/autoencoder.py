import torch.nn as nn
import torchvision.models as models


class DenoisingAE(nn.Module):
    """Denoising autoencoder with a pretrained ResNet18 encoder (up to layer3)."""

    def __init__(self):
        super().__init__()
        resnet = models.resnet18(weights='IMAGENET1K_V1')
        self.encoder = nn.Sequential(
            resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool,
            resnet.layer1, resnet.layer2, resnet.layer3
        )
        # 128x128 input -> encoder downsamples by 16x -> 8x8x256.
        # Decoder must upsample by exactly 16x (4 stride-2 stages) to get back to 128x128.
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(32, 3, 4, 2, 1), nn.Tanh(),
        )

    def set_encoder_trainable(self, trainable: bool):
        for p in self.encoder.parameters():
            p.requires_grad = trainable

    def forward(self, x):
        return self.decoder(self.encoder(x))


# Backwards-compatible alias
Autoencoder = DenoisingAE
