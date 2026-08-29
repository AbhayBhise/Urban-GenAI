import os
import time
import json
import torch
import torch.nn as nn
from torchvision import transforms
from dataset import UCMercedDataset, URBAN_CLASSES
from torch.utils.data import DataLoader, random_split
from models.transformer import UrbanClassifier

FREEZE_EPOCHS = 10
EPOCHS = 30
BATCH_SIZE = 32
LR_HEAD = 1e-4
LR_FINETUNE = 1e-5


def get_dataloaders_224(batch_size=BATCH_SIZE, val_split=0.1):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    dataset = UCMercedDataset(classes=URBAN_CLASSES, transform=transform)
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
    print(f"UCMerced: {len(dataset)} images | Train: {train_size} | Val: {val_size}")
    return train_loader, val_loader


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            logits = model(imgs)
            loss = criterion(logits, labels)
            total_loss += loss.item()
            _, pred = logits.max(1)
            correct += pred.eq(labels).sum().item()
            total += labels.size(0)
    return total_loss / len(loader), correct / total


def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    train_loader, val_loader = get_dataloaders_224()

    model = UrbanClassifier(num_classes=len(URBAN_CLASSES)).to(device)
    model.set_backbone_trainable(False)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR_HEAD)

    history = []
    print(f"Starting Transformer (ResNet18) training ({EPOCHS} epochs, backbone frozen for first {FREEZE_EPOCHS})...")
    for epoch in range(EPOCHS):
        if epoch == FREEZE_EPOCHS:
            model.set_backbone_trainable(True)
            optimizer = torch.optim.Adam(model.parameters(), lr=LR_FINETUNE)
            print(f"Epoch {epoch+1}: unfreezing backbone, lr -> {LR_FINETUNE}")

        model.train()
        total_loss, correct, total = 0, 0, 0
        start = time.time()
        for batch_idx, (imgs, labels) in enumerate(train_loader):
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            logits = model(imgs)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, pred = logits.max(1)
            correct += pred.eq(labels).sum().item()
            total += labels.size(0)

            if batch_idx % 10 == 0:
                print(f"Epoch {epoch+1} | Batch {batch_idx}/{len(train_loader)} | Loss: {loss.item():.4f} | Acc: {100.*correct/total:.1f}%")

        train_loss = total_loss / len(train_loader)
        train_acc = correct / total
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        history.append({
            "epoch": epoch + 1,
            "loss": train_loss,
            "accuracy": train_acc,
            "val_loss": val_loss,
            "val_accuracy": val_acc,
        })
        print(f"Epoch {epoch+1} done in {time.time()-start:.1f}s | Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        os.makedirs('../outputs/transformer', exist_ok=True)
        torch.save(model.state_dict(), '../outputs/transformer/model.pth')
        with open('../outputs/transformer/history.json', 'w') as f:
            json.dump(history, f)

    print("Transformer training complete and saved.")


if __name__ == '__main__':
    train()
