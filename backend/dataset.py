import os
from pathlib import Path
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms

DATASET_PATH = Path("../UCMerced_LandUse/UCMerced_LandUse/Images")
EUROSAT_PATH = Path("../EuroSAT/EuroSAT")

URBAN_CLASSES = [
    "agricultural", "airplane", "baseballdiamond", "beach",
    "buildings", "chaparral", "denseresidential", "forest",
    "freeway", "golfcourse", "harbor", "intersection",
    "mediumresidential", "mobilehomepark", "overpass",
    "parkinglot", "river", "runway", "sparseresidential",
    "storagetanks", "tenniscourt"
]

EURO_CLASSES = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake"
]


class UCMercedDataset(Dataset):
    def __init__(self, root=DATASET_PATH, classes=URBAN_CLASSES, transform=None):
        self.samples = []
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        self.transform = transform or transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        for cls in classes:
            cls_dir = root / cls
            if cls_dir.exists():
                for f in cls_dir.glob("*.tif"):
                    self.samples.append((f, self.class_to_idx[cls]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        return self.transform(img), label


UCMercedUrban = UCMercedDataset


class EuroSATDataset(Dataset):
    def __init__(self, root=EUROSAT_PATH, classes=EURO_CLASSES, transform=None):
        self.samples = []
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        self.transform = transform or transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        for cls in classes:
            cls_dir = root / cls
            if cls_dir.exists():
                for ext in ("*.jpg", "*.jpeg", "*.png"):
                    for f in sorted(cls_dir.glob(ext)):
                        self.samples.append((f, self.class_to_idx[cls]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        return self.transform(img), label


def get_dataloaders(batch_size=32, val_split=0.1):
    dataset = UCMercedDataset()
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)
    print(f"UCMerced: {len(dataset)} images | Train: {train_size} | Val: {val_size}")
    return train_loader, val_loader


def get_eurosat_dataloaders(batch_size=64, val_split=0.1):
    dataset = EuroSATDataset()
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)
    print(f"EuroSAT: {len(dataset)} images | Train: {train_size} | Val: {val_size}")
    return train_loader, val_loader
