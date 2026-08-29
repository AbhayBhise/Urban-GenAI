import os
import glob
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
from models.transformer import UrbanClassifier
from dataset import URBAN_CLASSES

def evaluate_generated_images(input_dir='../outputs/generated', model_path='../outputs/transformer/model.pth'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    image_paths = glob.glob(os.path.join(input_dir, 'fake_*.png'))
    if not image_paths:
        print(f"No generated images found in {input_dir}. Run generate.py first.")
        return

    model = UrbanClassifier(num_classes=len(URBAN_CLASSES)).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    class_counts = {c: 0 for c in URBAN_CLASSES}
    total_entropy = 0.0
    
    print(f"Evaluating {len(image_paths)} generated images...")
    with torch.no_grad():
        for path in image_paths:
            img = Image.open(path).convert("RGB")
            img_tensor = transform(img).unsqueeze(0).to(device)
            
            logits = model(img_tensor)
            probs = F.softmax(logits, dim=-1)
            pred_idx = torch.argmax(probs, dim=-1).item()
            pred_class = URBAN_CLASSES[pred_idx]
            
            class_counts[pred_class] += 1
            
            # Entropy calculation for prediction confidence
            entropy = -(probs * torch.log(probs + 1e-8)).sum().item()
            total_entropy += entropy
            
    print("\n--- Evaluation Results ---")
    print("Class distribution of generated images (according to Transformer):")
    for cls, count in class_counts.items():
        if count > 0:
            print(f"  {cls}: {count} ({count/len(image_paths)*100:.1f}%)")
            
    avg_entropy = total_entropy / len(image_paths)
    print(f"\nAverage prediction entropy: {avg_entropy:.4f}")
    if avg_entropy < 0.5:
        print("Conclusion: The generated images contain distinct features recognizable by the classifier (Low entropy).")
    else:
        print("Conclusion: The generated images are somewhat ambiguous or noisy (High entropy).")

if __name__ == '__main__':
    evaluate_generated_images()
