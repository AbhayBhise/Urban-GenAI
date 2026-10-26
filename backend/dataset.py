import os
from pathlib import Path
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from splits import split_paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "UCMerced_LandUse" / "UCMerced_LandUse" / "Images"
EUROSAT_PATH = PROJECT_ROOT / "EuroSAT" / "EuroSAT"

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
    def __init__(self, root=DATASET_PATH, classes=URBAN_CLASSES, transform=None, paths=None):
        self.samples = []
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        self.transform = transform or transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        if paths is not None:
            for f in paths:
                cls = Path(f).parent.name
                if cls in self.class_to_idx:
                    self.samples.append((Path(f), self.class_to_idx[cls]))
            return
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


def _aerial_train_transform(size):
    return transforms.Compose([
        transforms.Resize((size, size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomChoice([
            transforms.Lambda(lambda img, angle=angle: img.rotate(angle))
            for angle in (0, 90, 180, 270)
        ]),
        transforms.ColorJitter(brightness=0.08, contrast=0.08, saturation=0.06, hue=0.02),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])


def _aerial_eval_transform(size):
    return transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])


def get_dataloaders(batch_size=32, val_split=0.1, seed=42):
    train_base = UCMercedDataset(transform=_aerial_train_transform(128))
    val_base = UCMercedDataset(transform=_aerial_eval_transform(128))
    val_size = int(len(train_base) * val_split)
    train_size = len(train_base) - val_size
    split_generator = torch.Generator().manual_seed(seed)
    train_indices, val_indices = random_split(range(len(train_base)), [train_size, val_size], generator=split_generator)
    train_ds = torch.utils.data.Subset(train_base, train_indices.indices)
    val_ds = torch.utils.data.Subset(val_base, val_indices.indices)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)
    print(f"UCMerced: {len(train_base)} images | Train: {train_size} | Val: {val_size} | seed={seed}")
    return train_loader, val_loader


def get_split_datasets(size=128, train_aug=True):
    train_paths = split_paths("train")
    val_paths = split_paths("val")
    test_paths = split_paths("test")
    train_ds = UCMercedDataset(
        transform=_aerial_train_transform(size) if train_aug else _aerial_eval_transform(size),
        paths=train_paths,
    )
    val_ds = UCMercedDataset(transform=_aerial_eval_transform(size), paths=val_paths)
    test_ds = UCMercedDataset(transform=_aerial_eval_transform(size), paths=test_paths)
    return train_ds, val_ds, test_ds


def get_split_dataloaders(batch_size=16, size=128, num_workers=0, train_aug=True):
    train_ds, val_ds, test_ds = get_split_datasets(size=size, train_aug=train_aug)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)
    print(f"UCMerced stratified split | Train: {len(train_ds)} | Val: {len(val_ds)} | Test: {len(test_ds)}")
    return train_loader, val_loader, test_loader


def get_eurosat_dataloaders(batch_size=64, val_split=0.1):
    dataset = EuroSATDataset()
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)
    print(f"EuroSAT: {len(dataset)} images | Train: {train_size} | Val: {val_size}")
    return train_loader, val_loader
