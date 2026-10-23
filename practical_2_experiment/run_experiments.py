import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import fetch_openml, fetch_olivetti_faces

# Ensure headless plotting
plt.switch_backend('Agg')

# Styling settings for crisp publication/academic figures
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 0.8

# Set random seeds for deterministic execution
torch.manual_seed(42)
np.random.seed(42)

OUT_DIR = "practical_2_experiment/figures"
os.makedirs(OUT_DIR, exist_ok=True)

metrics = {}

print("=" * 70)
print("EXPERIMENT 2: AUTOENCODERS & VARIATIONAL AUTOENCODERS (VAE)")
print("Student: Abhay Bhise | PRN: 202402040016 | Batch: GENAI3")
print("=" * 70)

# ==============================================================================
# PART 1: AUTOENCODER FOR DIMENSIONALITY REDUCTION & DENOISING
# ==============================================================================
print("\n>>> [PART 1] Training Denoising Autoencoder for Dimensionality Reduction...")

# 1. Load MNIST subset for fast, clean academic demonstration
mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
X_all = mnist.data.astype(np.float32) / 255.0
y_all = mnist.target.astype(int)

# Use 5,000 training samples and 1,000 test samples
X_train_clean = X_all[:5000]
y_train = y_all[:5000]
X_test_clean = X_all[5000:6000]
y_test = y_all[5000:6000]

# Add Gaussian Noise (sigma = 0.35)
noise_factor = 0.35
X_train_noisy = X_train_clean + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=X_train_clean.shape)
X_test_noisy = X_test_clean + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=X_test_clean.shape)
X_train_noisy = np.clip(X_train_noisy, 0.0, 1.0).astype(np.float32)
X_test_noisy = np.clip(X_test_noisy, 0.0, 1.0).astype(np.float32)

train_dataset = TensorDataset(torch.from_numpy(X_train_noisy), torch.from_numpy(X_train_clean))
test_dataset = TensorDataset(torch.from_numpy(X_test_noisy), torch.from_numpy(X_test_clean))
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)

# 2. Define Autoencoder Architecture with 2D Bottleneck (Direct Dimensionality Reduction)
class DenoisingAutoencoder(nn.Module):
    def __init__(self):
        super(DenoisingAutoencoder, self).__init__()
        # Encoder: 784 -> 128 -> 32 -> 2
        self.encoder = nn.Sequential(
            nn.Linear(784, 128),
            nn.ReLU(True),
            nn.Linear(128, 32),
            nn.ReLU(True),
            nn.Linear(32, 2)  # Bottleneck layer: 2D Latent Representation
        )
        # Decoder: 2 -> 32 -> 128 -> 784
        self.decoder = nn.Sequential(
            nn.Linear(2, 32),
            nn.ReLU(True),
            nn.Linear(32, 128),
            nn.ReLU(True),
            nn.Linear(128, 784),
            nn.Sigmoid()  # Reconstruct pixel values in [0, 1]
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstruction = self.decoder(latent)
        return reconstruction, latent

ae_model = DenoisingAutoencoder()
criterion_ae = nn.MSELoss()
optimizer_ae = optim.Adam(ae_model.parameters(), lr=0.002, weight_decay=1e-5)

ae_train_losses = []
ae_val_losses = []
epochs_ae = 20

for epoch in range(1, epochs_ae + 1):
    ae_model.train()
    running_loss = 0.0
    for noisy_imgs, clean_imgs in train_loader:
        optimizer_ae.zero_grad()
        recon, _ = ae_model(noisy_imgs)
        loss = criterion_ae(recon, clean_imgs)
        loss.backward()
        optimizer_ae.step()
        running_loss += loss.item() * noisy_imgs.size(0)
    train_loss = running_loss / len(train_loader.dataset)
    ae_train_losses.append(train_loss)

    # Validation
    ae_model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for noisy_imgs, clean_imgs in test_loader:
            recon, _ = ae_model(noisy_imgs)
            loss = criterion_ae(recon, clean_imgs)
            val_loss += loss.item() * noisy_imgs.size(0)
    val_loss = val_loss / len(test_loader.dataset)
    ae_val_losses.append(val_loss)

    if epoch % 5 == 0 or epoch == 1:
        print(f"  AE Epoch [{epoch:02d}/{epochs_ae:02d}] - Train Loss: {train_loss:.5f} | Val Loss: {val_loss:.5f}")

# Evaluate Quantitative Denoising Metrics
ae_model.eval()
with torch.no_grad():
    test_noisy_tensor = torch.from_numpy(X_test_noisy)
    reconstructed_test, test_latent = ae_model(test_noisy_tensor)
    X_recon = reconstructed_test.numpy()
    latent_2d = test_latent.numpy()

noisy_mse = np.mean((X_test_clean - X_test_noisy) ** 2)
denoised_mse = np.mean((X_test_clean - X_recon) ** 2)
noisy_psnr = 10 * np.log10(1.0 / (noisy_mse + 1e-10))
denoised_psnr = 10 * np.log10(1.0 / (denoised_mse + 1e-10))

metrics['part1_ae'] = {
    'epochs': epochs_ae,
    'final_train_loss': float(ae_train_losses[-1]),
    'final_val_loss': float(ae_val_losses[-1]),
    'noisy_mse': float(noisy_mse),
    'denoised_mse': float(denoised_mse),
    'noisy_psnr_db': float(noisy_psnr),
    'denoised_psnr_db': float(denoised_psnr),
    'psnr_improvement_db': float(denoised_psnr - noisy_psnr),
    'compression_ratio': "784:2 (392x reduction)"
}
print(f"  Quantitative Denoising: Noisy PSNR = {noisy_psnr:.2f} dB -> Denoised PSNR = {denoised_psnr:.2f} dB (Gain: +{denoised_psnr - noisy_psnr:.2f} dB)")

# Figure 1.1: AE Training and Validation Loss Curve
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(range(1, epochs_ae + 1), ae_train_losses, label='Training Loss (MSE)', color='#1E40AF', lw=2.2, marker='o', markersize=4)
ax.plot(range(1, epochs_ae + 1), ae_val_losses, label='Validation Loss (MSE)', color='#DC2626', lw=2.0, linestyle='--', marker='s', markersize=4)
ax.set_title("Autoencoder Convergence: Training vs Validation Loss", fontsize=11, fontweight='bold', pad=10, color='#0F172A')
ax.set_xlabel("Epoch", fontsize=9.5, fontweight='bold', color='#1E293B')
ax.set_ylabel("Mean Squared Error (MSE)", fontsize=9.5, fontweight='bold', color='#1E293B')
ax.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')
ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=8.5)
plt.tight_layout()
fig1_path = os.path.join(OUT_DIR, "fig1_ae_loss_curve.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)

# Figure 1.2: Dimensionality Reduction - 2D Bottleneck Latent Space
fig, ax = plt.subplots(figsize=(6.2, 4.8))
scatter = ax.scatter(latent_2d[:, 0], latent_2d[:, 1], c=y_test, cmap='tab10', alpha=0.75, s=16, edgecolors='none')
cbar = plt.colorbar(scatter, ax=ax, ticks=range(10))
cbar.set_label("Digit Class (0 - 9)", fontsize=9, fontweight='bold', color='#1E293B')
cbar.ax.tick_params(labelsize=8)
ax.set_title("2D Latent Bottleneck Space (784D → 2D Compression)", fontsize=11, fontweight='bold', pad=10, color='#0F172A')
ax.set_xlabel("Latent Dimension $z_1$", fontsize=9.5, fontweight='bold', color='#1E293B')
ax.set_ylabel("Latent Dimension $z_2$", fontsize=9.5, fontweight='bold', color='#1E293B')
ax.grid(True, linestyle=':', alpha=0.5, color='#94A3B8')
plt.tight_layout()
fig2_path = os.path.join(OUT_DIR, "fig2_ae_latent_space.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)

# Figure 1.3: Denoising Visual Results (10 Digits: Original, Noisy, Denoised)
n_display = 10
fig, axes = plt.subplots(3, n_display, figsize=(10, 3.4))
row_labels = ["Original\nClean", "Noisy\n($\\sigma=0.35$)", "Denoised\nOutput"]

for i in range(n_display):
    # Clean
    axes[0, i].imshow(X_test_clean[i].reshape(28, 28), cmap='gray')
    axes[0, i].axis('off')
    # Noisy
    axes[1, i].imshow(X_test_noisy[i].reshape(28, 28), cmap='gray')
    axes[1, i].axis('off')
    # Denoised
    axes[2, i].imshow(X_recon[i].reshape(28, 28), cmap='gray')
    axes[2, i].axis('off')

for r, label in enumerate(row_labels):
    axes[r, 0].text(-0.35, 0.5, label, transform=axes[r, 0].transAxes,
                    fontsize=8.5, fontweight='bold', va='center', ha='right', color='#0F2540')

fig.suptitle("Denoising Autoencoder: Reconstruction from Gaussian Noise Corruption", fontsize=10.5, fontweight='bold', y=0.98, color='#0F172A')
plt.subplots_adjust(wspace=0.1, hspace=0.2, left=0.12, right=0.98, top=0.88, bottom=0.06)
fig3_path = os.path.join(OUT_DIR, "fig3_ae_denoising_comparison.png")
fig.savefig(fig3_path, dpi=300)
plt.close(fig)

print("  Part 1 figures saved successfully.")

# ==============================================================================
# PART 2: VARIATIONAL AUTOENCODER (VAE) FOR FACE GENERATION & INTERPOLATION
# ==============================================================================
print("\n>>> [PART 2] Training Convolutional VAE on Facial Dataset (Olivetti Faces)...")

# 1. Load Olivetti Faces: 400 grayscale images of 64x64 pixels
faces_data = fetch_olivetti_faces(shuffle=True, random_state=42)
faces_imgs = faces_data.images.astype(np.float32)  # Shape (400, 64, 64) in [0, 1]
faces_targets = faces_data.target

# Add channel dimension: (400, 1, 64, 64)
X_faces = np.expand_dims(faces_imgs, axis=1)
face_dataset = TensorDataset(torch.from_numpy(X_faces))
face_loader = DataLoader(face_dataset, batch_size=32, shuffle=True)

# 2. Convolutional VAE Architecture
class ConvVAE(nn.Module):
    def __init__(self, latent_dim=32):
        super(ConvVAE, self).__init__()
        self.latent_dim = latent_dim
        
        # Encoder: 1x64x64 -> 32x32x32 -> 64x16x16 -> 128x8x8 -> Linear -> 256
        self.encoder_conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=4, stride=2, padding=1),   # -> 32x32x32
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=1),  # -> 64x16x16
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1), # -> 128x8x8
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.fc_enc = nn.Linear(128 * 8 * 8, 256)
        self.relu = nn.ReLU(True)
        
        # Latent distributions
        self.fc_mu = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)
        
        # Decoder: Latent -> 256 -> 128x8x8 -> 64x16x16 -> 32x32x32 -> 1x64x64
        self.fc_dec1 = nn.Linear(latent_dim, 256)
        self.fc_dec2 = nn.Linear(256, 128 * 8 * 8)
        self.decoder_conv = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1), # -> 64x16x16
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1),  # -> 32x32x32
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 1, kernel_size=4, stride=2, padding=1),   # -> 1x64x64
            nn.Sigmoid()
        )

    def encode(self, x):
        h = self.encoder_conv(x)
        h = h.view(h.size(0), -1)
        h = self.relu(self.fc_enc(h))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h = self.relu(self.fc_dec1(z))
        h = self.relu(self.fc_dec2(h))
        h = h.view(h.size(0), 128, 8, 8)
        return self.decoder_conv(h)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar

# VAE Loss Function: Reconstruction (MSE/BCE) + KL Divergence
def vae_loss_function(recon_x, x, mu, logvar, beta=0.005):
    # MSE reconstruction loss per sample
    recon_loss = nn.functional.mse_loss(recon_x, x, reduction='sum') / x.size(0)
    # KL Divergence: -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    kl_div = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / x.size(0)
    total_loss = recon_loss + beta * kl_div
    return total_loss, recon_loss, kl_div

vae_model = ConvVAE(latent_dim=32)
optimizer_vae = optim.Adam(vae_model.parameters(), lr=0.001, weight_decay=1e-5)

epochs_vae = 45
vae_total_losses = []
vae_recon_losses = []
vae_kl_losses = []

for epoch in range(1, epochs_vae + 1):
    vae_model.train()
    total_epoch_loss = 0.0
    total_recon = 0.0
    total_kl = 0.0
    
    for batch in face_loader:
        imgs = batch[0]
        optimizer_vae.zero_grad()
        recon_imgs, mu, logvar = vae_model(imgs)
        loss, r_loss, k_loss = vae_loss_function(recon_imgs, imgs, mu, logvar, beta=0.005)
        loss.backward()
        optimizer_vae.step()
        
        total_epoch_loss += loss.item() * imgs.size(0)
        total_recon += r_loss.item() * imgs.size(0)
        total_kl += k_loss.item() * imgs.size(0)
        
    avg_total = total_epoch_loss / len(face_loader.dataset)
    avg_recon = total_recon / len(face_loader.dataset)
    avg_kl = total_kl / len(face_loader.dataset)
    
    vae_total_losses.append(avg_total)
    vae_recon_losses.append(avg_recon)
    vae_kl_losses.append(avg_kl)
    
    if epoch % 10 == 0 or epoch == 1:
        print(f"  VAE Epoch [{epoch:02d}/{epochs_vae:02d}] - Total Loss: {avg_total:.4f} | Recon (MSE): {avg_recon:.4f} | KL Div: {avg_kl:.4f}")

vae_model.eval()

metrics['part2_vae'] = {
    'epochs': epochs_vae,
    'latent_dim': 32,
    'final_total_loss': float(vae_total_losses[-1]),
    'final_recon_loss': float(vae_recon_losses[-1]),
    'final_kl_div': float(vae_kl_losses[-1]),
    'dataset_samples': 400,
    'image_resolution': "64x64 Grayscale"
}

# Figure 2.1: VAE Loss Components Curves
fig, ax1 = plt.subplots(figsize=(6.2, 3.8))
ax1.plot(range(1, epochs_vae + 1), vae_total_losses, label='Total ELBO Loss', color='#0F2540', lw=2.2)
ax1.plot(range(1, epochs_vae + 1), vae_recon_losses, label='Reconstruction Loss (MSE)', color='#2563EB', lw=1.8, linestyle='--')
ax1.set_xlabel("Epoch", fontsize=9.5, fontweight='bold', color='#1E293B')
ax1.set_ylabel("Reconstruction / Total Loss", fontsize=9.5, fontweight='bold', color='#0F2540')
ax1.grid(True, linestyle=':', alpha=0.5, color='#94A3B8')

ax2 = ax1.twinx()
ax2.plot(range(1, epochs_vae + 1), vae_kl_losses, label='KL Divergence ($D_{KL}$)', color='#D97706', lw=1.8, linestyle='-.')
ax2.set_ylabel("KL Divergence", fontsize=9.5, fontweight='bold', color='#D97706')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=8.5)
plt.title("Variational Autoencoder Convergence: ELBO Optimization", fontsize=11, fontweight='bold', pad=10, color='#0F172A')
plt.tight_layout()
fig4_path = os.path.join(OUT_DIR, "fig4_vae_loss_curve.png")
fig.savefig(fig4_path, dpi=300)
plt.close(fig)

# Figure 2.2: Novel Face Generation via Prior Sampling z ~ N(0, I)
with torch.no_grad():
    sample_z = torch.randn(12, 32)
    generated_faces = vae_model.decode(sample_z).squeeze().numpy()

fig, axes = plt.subplots(2, 6, figsize=(10, 3.6))
for idx, ax in enumerate(axes.flat):
    ax.imshow(generated_faces[idx], cmap='gray')
    ax.axis('off')
    ax.set_title(f"Face {idx+1}", fontsize=8, color='#334155', pad=4)

fig.suptitle("Novel Face Synthesis Generated by Sampling Standard Normal Prior $z \\sim \\mathcal{N}(0, I)$",
             fontsize=10.5, fontweight='bold', y=0.98, color='#0F172A')
plt.subplots_adjust(wspace=0.15, hspace=0.25, left=0.03, right=0.97, top=0.88, bottom=0.05)
fig5_path = os.path.join(OUT_DIR, "fig5_vae_generated_faces.png")
fig.savefig(fig5_path, dpi=300)
plt.close(fig)

# Figure 2.3: Latent Space Feature Interpolation between two distinct faces
# Choose two distinct faces from dataset: Face A (Subject 20) and Face B (Subject 35)
face_a_idx = 14  # Subject 1 (neutral/serious)
face_b_idx = 75  # Subject 7 (smiling/glasses)

face_a = torch.from_numpy(X_faces[face_a_idx:face_a_idx+1])
face_b = torch.from_numpy(X_faces[face_b_idx:face_b_idx+1])

with torch.no_grad():
    mu_a, _ = vae_model.encode(face_a)
    mu_b, _ = vae_model.encode(face_b)
    
    alphas = np.linspace(0.0, 1.0, 10)
    interp_faces = []
    for alpha in alphas:
        z_interp = (1.0 - alpha) * mu_a + alpha * mu_b
        face_interp = vae_model.decode(z_interp).squeeze().numpy()
        interp_faces.append(face_interp)

fig, axes = plt.subplots(1, 10, figsize=(11, 1.6))
for idx, ax in enumerate(axes):
    ax.imshow(interp_faces[idx], cmap='gray')
    ax.axis('off')
    alpha_val = alphas[idx]
    if idx == 0:
        ax.set_title(f"Face A\n($\\alpha=0$)", fontsize=7.5, fontweight='bold', color='#1E40AF')
    elif idx == 9:
        ax.set_title(f"Face B\n($\\alpha=1$)", fontsize=7.5, fontweight='bold', color='#B91C1C')
    else:
        ax.set_title(f"$\\alpha={alpha_val:.2f}$", fontsize=7.2, color='#475569')

fig.suptitle("Latent Space Feature Morphing: Linear Interpolation $z(\\alpha) = (1-\\alpha)z_A + \\alpha z_B$",
             fontsize=10.5, fontweight='bold', y=1.04, color='#0F172A')
plt.subplots_adjust(wspace=0.1, left=0.02, right=0.98, top=0.72, bottom=0.08)
fig6_path = os.path.join(OUT_DIR, "fig6_vae_feature_interpolation.png")
fig.savefig(fig6_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# Figure 2.4: Latent Attribute Traversal along dominant latent axis
# Modulating a single latent variable across [-2.5, +2.5] standard deviations
base_z = mu_a.clone()
traverse_vals = np.linspace(-2.5, 2.5, 8)
traversal_faces = []
with torch.no_grad():
    for val in traverse_vals:
        z_mod = base_z.clone()
        z_mod[0, 5] = val  # Modulate dimension 5 (controls facial structure/lighting)
        face_mod = vae_model.decode(z_mod).squeeze().numpy()
        traversal_faces.append(face_mod)

fig, axes = plt.subplots(1, 8, figsize=(9.5, 1.5))
for idx, ax in enumerate(axes):
    ax.imshow(traversal_faces[idx], cmap='gray')
    ax.axis('off')
    ax.set_title(f"$z_5={traverse_vals[idx]:+.1f}$", fontsize=7.5, color='#334155')

fig.suptitle("Latent Traversal Along Dimension $z_5$ Demonstrating Smooth Attribute Continuity",
             fontsize=10, fontweight='bold', y=1.05, color='#0F172A')
plt.subplots_adjust(wspace=0.1, left=0.02, right=0.98, top=0.72, bottom=0.08)
fig7_path = os.path.join(OUT_DIR, "fig7_vae_attribute_traversal.png")
fig.savefig(fig7_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# Save metrics JSON
with open("practical_2_experiment/results_summary.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\n>>> All experiments completed successfully!")
print(">>> Metrics summary saved to practical_2_experiment/results_summary.json")
