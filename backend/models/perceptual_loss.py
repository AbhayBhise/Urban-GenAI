import torch
import torch.nn as nn
from torchvision.models import vgg16, VGG16_Weights

class VGGPerceptualLoss(nn.Module):
    def __init__(self, resize=True, num_blocks=4):
        super(VGGPerceptualLoss, self).__init__()
        # Load VGG16 features. num_blocks<4 keeps only early, cheap layers —
        # useful for small (e.g. 64x64) inputs where resize=False, since the
        # full 4-block stack at native resolution (no 224 upsample) still
        # captures useful low/mid-level structure at a fraction of the cost.
        all_slices = [(0, 4), (4, 9), (9, 16), (16, 23)]
        blocks = []
        for start, end in all_slices[:num_blocks]:
            blocks.append(vgg16(weights=VGG16_Weights.IMAGENET1K_V1).features[start:end].eval())
        for bl in blocks:
            for p in bl.parameters():
                p.requires_grad = False
        self.blocks = nn.ModuleList(blocks)
        self.transform = torch.nn.functional.interpolate
        self.resize = resize
        self.register_buffer("mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))

    def forward(self, input, target):
        # Input and target are assumed to be in range [-1, 1]
        input = (input + 1) / 2
        target = (target + 1) / 2
        input = (input - self.mean) / self.std
        target = (target - self.mean) / self.std
        if self.resize:
            input = self.transform(input, mode='bilinear', size=(224, 224), align_corners=False)
            target = self.transform(target, mode='bilinear', size=(224, 224), align_corners=False)
        loss = 0.0
        x = input
        y = target
        for block in self.blocks:
            x = block(x)
            y = block(y)
            loss += torch.nn.functional.mse_loss(x, y)
        return loss
