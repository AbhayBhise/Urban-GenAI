import torch.nn as nn
import torchvision.models as models


class UrbanClassifier(nn.Module):
    """ResNet18 fine-tuned for UCMerced land-use classification."""

    def __init__(self, num_classes=21):
        super().__init__()
        self.model = models.resnet18(weights='IMAGENET1K_V1')
        self.model.fc = nn.Linear(512, num_classes)

    def set_backbone_trainable(self, trainable: bool):
        for name, p in self.model.named_parameters():
            if not name.startswith('fc.'):
                p.requires_grad = trainable

    def forward(self, x):
        return self.model(x)


# Backwards-compatible alias
UrbanViT = UrbanClassifier
