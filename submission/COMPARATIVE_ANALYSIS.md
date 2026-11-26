# 📊 Comparative Analysis — UrbanGen AI (First 3 Generative AI Modules)

This document directly satisfies the PPT and Practical Submission requirements:
1. **Comparative analysis table using evaluation metrics of 2 Generative AI models** (Denoising Autoencoder vs. Spatial β-VAE)
2. **Demonstration & Comparative Analysis of the first 3 Generative AI modules** (Denoising AE, Spatial β-VAE, and MiniGPT Transformer)

---

## 1. Quantitative Comparative Analysis Table (2 Vision GenAI Models: AE vs. Spatial β-VAE)

Both models were trained for **50 epochs** on the **UCMerced LandUse** dataset (2,100 aerial RGB tiles across 21 land-use classes, resized to `128×128`, normalized to `[-1, 1]`) on an NVIDIA RTX 4050 (6 GB).

| Evaluation Metric | Module 1: Denoising Autoencoder (U-Net AE) | Module 2: Spatial β-VAE | Winner / Observation |
| :--- | :--- | :--- | :--- |
| **Backbone / Encoder** | Pretrained ResNet-18 (`stem` → `layer3`) | Pretrained ResNet-18 (`stem` → `layer3`) | Same feature extractor |
| **Latent Representation** | Deterministic `8×8×256` bottleneck | Probabilistic `8×8×64` spatial $(\mu, \log\sigma^2)$ | VAE enforces smooth Gaussian prior |
| **Skip Connections** | Full multi-scale U-Net skips | Compact projected skips (`16` ch + `0.2` dropout) | AE preserves sharper edges; VAE prevents KL collapse |
| **Training Objective** | Pixel MSE under $\sigma=0.15$ Gaussian noise | $\text{ELBO} = 0.7\cdot L_1 + 0.3\cdot\text{MSE} + \beta\cdot\text{KL}$ ($\beta=10^{-4}$) | AE optimizes pure denoising; VAE balances reconstruction + distribution |
| **Final Train Loss (Epoch 50)** | `0.00617` (MSE) | `0.08220` (ELBO) / `0.02461` (MSE) | AE achieves lower raw training MSE |
| **Validation / Benchmark PSNR** | **`29.65 dB`** (`MSE: 0.00585`) | **`27.49 dB`** val (`29.75 dB` full eval; `MSE: 0.00713` val) | Comparable high-fidelity reconstruction (~27.5–29.7 dB) |
| **KL Divergence** | N/A (Deterministic) | `60.72` nats (val) / `41.79` nats (eval) | Active latent (no posterior collapse via free bits `0.01`) |
| **Latent Interpolation** | Not smooth (unregularized bottleneck) | **Smooth continuous morphing** between tiles | **VAE** supports semantic land-use interpolation |
| **Primary Urban Planning Role** | Satellite tile denoising & restoration | Unsupervised structural anomaly detection ($z$-score) | Complementary roles in pipeline |

---

## 2. Comparative Overview of All 3 Generative AI Modules

| Dimension | 1. Denoising Autoencoder (`ae`) | 2. Spatial β-VAE (`vae`) | 3. MiniGPT Transformer (`gpt`) |
| :--- | :--- | :--- | :--- |
| **Generative Family** | Deterministic Autoencoder (U-Net) | Variational Autoencoder (Probabilistic) | Autoregressive Decoder-Only Transformer |
| **Modality** | Image $\rightarrow$ Image (`128×128` RGB) | Image $\rightarrow$ Latent $\rightarrow$ Image (`128×128` RGB) | Text $\rightarrow$ Text (Char-level, `block_size=192`) |
| **Architecture** | ResNet-18 + 4-stage skip decoder | ResNet-18 + $\mu/\sigma$ heads + compact skips | 4 Transformer blocks, 4 heads, `d_model=256` |
| **Parameters** | ~11.4M | ~12.1M | ~1.3M (built from scratch) |
| **Dataset** | UCMerced LandUse (2,100 tiles) | UCMerced LandUse (2,100 tiles) | `urban_planning.txt` (241 KB Pune domain corpus) |
| **Training Schedule** | 50 epochs (encoder frozen 5 epochs) | 50 epochs (KL warmup 2 epochs, free bits `0.01`) | 1,000 steps (`AdamW`, `lr=3e-4`, grad clip `1.0`) |
| **Key Final Metrics** | PSNR: `29.65 dB`, MSE: `0.00585` | Val PSNR: `27.49 dB`, KL: `60.72` nats | Train Loss: `0.1475`, Val Loss: `0.1043` (PPL `1.087`, BPC `0.1199`) |
| **Key Strength** | Restores noisy/degraded aerial imagery with high edge fidelity | Smooth latent interpolation & calibrated anomaly detection (`mean=0.00675`) | Generates structured FSI, TOD & drainage policy drafts from GIS stats |
| **Key Limitation** | Cannot sample novel tiles from prior | Slight smoothing compared to DDPM/GAN | Small char-level context window (`192` chars); advisory only |
