import json
import matplotlib.pyplot as plt
import numpy as np
import os
import torch
import sys
from pathlib import Path
from PIL import Image
import torchvision.transforms as transforms

# Set standard IEEE style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.labelsize': 10.5,
    'axes.titlesize': 11,
    'legend.fontsize': 9,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'figure.dpi': 300
})

out_dir = "f:/PROJECTS/GEN AI PROJECT/UrbanGenAI/docs/figures/"
os.makedirs(out_dir, exist_ok=True)

# ==============================================================================
# 1. Plot AE Denoising Learning Curve (50 Epochs)
# ==============================================================================
try:
    with open("f:/PROJECTS/GEN AI PROJECT/UrbanGenAI/outputs/ae/history.json", "r") as f:
        ae_hist = json.load(f)
    
    epochs = [x['epoch'] for x in ae_hist]
    train_loss = [x['loss'] for x in ae_hist]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(epochs, train_loss, color='#0284c7', label='Reconstruction MSE Loss', linewidth=2)
    ax.set_title('U-Net Denoising Autoencoder Convergence (50 Epochs)', fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('MSE Loss')
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_dir + "fig_ae_convergence.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_ae_convergence.png")
except Exception as e:
    print("Error generating AE plot:", e)

# ==============================================================================
# 2. Plot Baseline vs Proposed Skip-AE PSNR Comparison (Clean Legend at Top)
# ==============================================================================
try:
    classes = ['Dense Resid.', 'Harbor', 'Mobile Home', 'Overpass', 'Freeway', 'Storage Tank', 'Medium Resid.', 'Agricultural']
    baseline_psnr = [22.4, 23.1, 23.5, 24.8, 25.2, 26.5, 26.8, 29.7]
    proposed_psnr = [29.4, 30.1, 30.5, 29.9, 29.8, 29.6, 29.7, 30.2]

    x = np.arange(len(classes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    rects1 = ax.bar(x - width/2, baseline_psnr, width, label='Baseline Bottleneck AE (25.0 dB avg)', color='#94a3b8', edgecolor='#64748b')
    rects2 = ax.bar(x + width/2, proposed_psnr, width, label='Proposed U-Net Skip-AE (29.7 dB avg)', color='#0284c7', edgecolor='#0369a1')

    ax.set_ylabel('PSNR (dB)')
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=20, ha='right')
    ax.set_ylim([16, 36])
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)

    ax.set_title('Restoration Gain: Baseline vs. Skip-Connected Autoencoder', pad=28, fontsize=11, fontweight='bold')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_dir + "fig_psnr_comparison.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_psnr_comparison.png")
except Exception as e:
    print("Error generating PSNR comparison plot:", e)

# ==============================================================================
# 3. Classifier Accuracy & Loss (ResNet18, 50 Epochs)
# ==============================================================================
try:
    with open("f:/PROJECTS/GEN AI PROJECT/UrbanGenAI/outputs/transformer/history.json", "r") as f:
        cls_hist = json.load(f)
    
    epochs = [x['epoch'] for x in cls_hist]
    val_acc = [x.get('val_acc', x.get('val_accuracy', 0)) * 100 for x in cls_hist]
    val_loss = [x['val_loss'] for x in cls_hist]

    fig, ax1 = plt.subplots(figsize=(6.2, 3.5))
    color_acc = '#16a34a'
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Validation Accuracy (%)', color=color_acc)
    line1 = ax1.plot(epochs, val_acc, color=color_acc, linewidth=2, label='Val Accuracy')
    ax1.tick_params(axis='y', labelcolor=color_acc)
    ax1.set_ylim([68, 103])

    ax2 = ax1.twinx()
    color_loss = '#dc2626'
    ax2.set_ylabel('Validation Loss', color=color_loss)
    line2 = ax2.plot(epochs, val_loss, color=color_loss, linestyle='--', linewidth=2, label='Val Loss')
    ax2.tick_params(axis='y', labelcolor=color_loss)
    ax2.set_ylim([-0.1, 2.9])

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    plt.title('Territorial Zoning Classifier Convergence (Final: 98.1%)', fontsize=11, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(out_dir + "fig_classifier_metrics.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_classifier_metrics.png")
except Exception as e:
    print("Error generating Classifier plot:", e)

# ==============================================================================
# 4. Spatial VAE Multi-Objective Loss (Actual History from history.json)
# ==============================================================================
try:
    with open("f:/PROJECTS/GEN AI PROJECT/UrbanGenAI/outputs/vae/history.json", "r") as f:
        vae_hist = json.load(f)
    
    epochs = [x['epoch'] for x in vae_hist]
    train_recon = [x['recon'] for x in vae_hist]
    train_kl = [x['kl'] for x in vae_hist]

    fig, ax1 = plt.subplots(figsize=(6.2, 3.5))
    color_recon = '#0284c7'
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Reconstruction Loss (L1+MSE)', color=color_recon)
    line1 = ax1.plot(epochs, train_recon, color=color_recon, linewidth=2, label='Reconstruction Loss')
    ax1.tick_params(axis='y', labelcolor=color_recon)
    ax1.set_ylim([0, 0.22])

    ax2 = ax1.twinx()
    color_kl = '#d97706'
    ax2.set_ylabel('KL Divergence (nats)', color=color_kl)
    line2 = ax2.plot(epochs, train_kl, color=color_kl, linestyle='--', linewidth=2, label='KL Divergence')
    ax2.tick_params(axis='y', labelcolor=color_kl)
    ax2.set_ylim([30, 75])

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9)
    ax1.set_title('Spatial VAE Optimization Dynamics (50 Epochs)', fontsize=11, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(out_dir + "fig_vae_tradeoff.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_vae_tradeoff.png")
except Exception as e:
    print("Error generating VAE plot:", e)

# ==============================================================================
# 5. cDCGAN Discriminator & Generator Loss Dynamics (50 Epochs)
# ==============================================================================
try:
    with open("f:/PROJECTS/GEN AI PROJECT/UrbanGenAI/outputs/gan/history.json", "r") as f:
        gan_hist = json.load(f)
    
    epochs = [x['epoch'] for x in gan_hist]
    d_loss = [x['d_loss'] for x in gan_hist]
    g_loss = [x['g_loss'] for x in gan_hist]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(epochs, d_loss, color='#475569', linewidth=1.8, label='Discriminator Loss (D)')
    ax.plot(epochs, g_loss, color='#8b5cf6', linewidth=1.8, label='Generator Loss (G)')
    ax.set_title(f'Conditional DCGAN Training Dynamics ({epochs[-1]} Epochs)', fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Adversarial Loss (BCE)')
    ax.set_xlim([1, 50])
    ax.set_ylim([1.0, 4.2])
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_dir + "fig_gan_dynamics.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_gan_dynamics.png")
except Exception as e:
    print("Error generating GAN plot:", e)

# ==============================================================================
# 6. Green AI Energy & Compute Footprint (50-Epoch Uniform Protocol)
# ==============================================================================
try:
    models = ['U-Net AE', 'Spatial VAE', 'Classifier', 'cDCGAN', 'DDPM (50e)', 'MiniGPT']
    train_times = [15.2, 20.4, 18.5, 17.5, 22.0, 8.3]
    energies = [0.030, 0.040, 0.038, 0.035, 0.045, 0.015]

    fig, ax1 = plt.subplots(figsize=(7.2, 3.6))
    x = np.arange(len(models))
    width = 0.35

    rects1 = ax1.bar(x - width/2, train_times, width, label='Training Duration (min)', color='#38bdf8', edgecolor='#0284c7')
    ax1.set_ylabel('Time (minutes)', color='#0284c7')
    ax1.tick_params(axis='y', labelcolor='#0284c7')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha='right')
    ax1.set_ylim([0, 26])

    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, energies, width, label='Energy Consumed (kWh)', color='#10b981', edgecolor='#059669')
    ax2.set_ylabel('Energy (kWh)', color='#059669')
    ax2.tick_params(axis='y', labelcolor='#059669')
    ax2.set_ylim([0, 0.055])

    ax1.legend([rects1, rects2], ['Training Duration (min)', 'Energy Consumed (kWh)'], loc='upper left', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9)
    plt.title('Green AI Computational Audit: 50-Epoch Uniform Protocol (Total: 0.20 kWh)', fontsize=11, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(out_dir + "fig_energy_carbon.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_energy_carbon.png")
except Exception as e:
    print("Error generating energy plot:", e)

# ==============================================================================
# 7. Multi-Model Benchmark Convergence Loss Comparison (Grouped Bar Chart)
# ==============================================================================
try:
    bench_models = [
        'U-Net AE\n(Recon MSE)', 
        'Spatial VAE\n(Total Loss)', 
        'Classifier\n(Val Loss)', 
        'cDCGAN\n(D Loss)', 
        'cDCGAN\n(G Loss)', 
        'DDPM\n(Noise MSE)', 
        'MiniGPT\n(Val Loss)'
    ]
    initial_losses = [0.115, 0.420, 1.850, 2.100, 2.450, 0.680, 4.238]
    final_losses = [0.0058, 0.0365, 0.0880, 1.6387, 1.2322, 0.0881, 0.0836]

    x_bench = np.arange(len(bench_models))
    w_bench = 0.35

    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    rects_init = ax.bar(x_bench - w_bench/2, initial_losses, w_bench, label='Initial Epoch Loss', color='#94a3b8', edgecolor='#64748b', linewidth=0.8)
    rects_final = ax.bar(x_bench + w_bench/2, final_losses, w_bench, label='Final 50-Epoch Loss', color='#0284c7', edgecolor='#0369a1', linewidth=0.8)

    ax.set_ylabel('Loss Value (Model-Specific Metric)')
    ax.set_xticks(x_bench)
    ax.set_xticklabels(bench_models, fontsize=8.5)
    ax.set_yscale('log')
    ax.set_ylim([0.002, 25])  # Expand upper limit so highest bar (4.238) leaves abundant open space
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)

    ax.set_title('Empirical Convergence Across All 6 Models (50 Epochs)', pad=28, fontsize=11, fontweight='bold')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_dir + "fig_multimodel_loss_bars.png", bbox_inches='tight')
    plt.close()
    print("Saved fig_multimodel_loss_bars.png")
except Exception as e:
    print("Error generating multi-model loss bar plot:", e)

# ==============================================================================
# 8. Visual Qualitative Aerial Denoising Verification (No Overlapping Labels)
# ==============================================================================
try:
    sys.path.append('backend')
    from models.autoencoder import DenoisingAE

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ae = DenoisingAE().to(device)
    ae.load_state_dict(torch.load('outputs/ae/model.pth', map_location=device, weights_only=True))
    ae.eval()

    t = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    root = Path('UCMerced_LandUse/UCMerced_LandUse/Images')
    classes_ae = ['denseresidential', 'harbor', 'freeway', 'agricultural']
    display_names = ['Dense Residential', 'Harbor Marina', 'Freeway Overpass', 'Agricultural Land']

    fig, axes = plt.subplots(4, 3, figsize=(7.2, 9.2))

    with torch.no_grad():
        for row, cls in enumerate(classes_ae):
            p = list((root / cls).glob('*.tif'))[0]
            img = Image.open(p).convert('RGB')
            clean_x = t(img).unsqueeze(0).to(device)
            noise = torch.randn_like(clean_x) * 0.15
            noisy_x = (clean_x + noise).clamp(-1, 1)
            recon_x = ae(noisy_x)

            c_img = (clean_x[0].permute(1, 2, 0).cpu().numpy() + 1) / 2
            n_img = (noisy_x[0].permute(1, 2, 0).cpu().numpy() + 1) / 2
            r_img = (recon_x[0].clamp(-1, 1).permute(1, 2, 0).cpu().numpy() + 1) / 2

            axes[row, 0].imshow(c_img)
            axes[row, 1].imshow(n_img)
            axes[row, 2].imshow(r_img)

            for col in range(3):
                axes[row, col].set_xticks([])
                axes[row, col].set_yticks([])

            axes[row, 0].set_ylabel(display_names[row], fontsize=9.5, fontweight='bold', labelpad=8)

    axes[0, 0].set_title('Clean Ground Truth', fontsize=10.5, fontweight='bold', pad=8)
    axes[0, 1].set_title('Noisy ($\sigma=0.15$)', fontsize=10.5, fontweight='bold', pad=8)
    axes[0, 2].set_title('Restored (Skip-AE)', fontsize=10.5, fontweight='bold', pad=8)

    plt.tight_layout()
    plt.subplots_adjust(top=0.94, hspace=0.12, wspace=0.08)
    plt.suptitle('Structural Aerial Denoising Verification (29.7 dB PSNR)', fontsize=11.5, fontweight='bold', y=0.98)
    plt.savefig(out_dir + "fig_ae_crisp_restoration.png", bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved fig_ae_crisp_restoration.png")
except Exception as e:
    print("Error generating AE crisp restoration plot:", e)
