# UrbanGen AI — Model Card

This unified Model Card documents every deep learning and generative model integrated into the **UrbanGen AI** municipal urban planning framework. All primary model checkpoints were trained under a standardized, aligned **50-epoch benchmark protocol** on the 21-class **UCMerced LandUse** benchmark using a single consumer-grade edge workstation.

### Common Hardware & Operational Specifications
- **Framework:** PyTorch 2.x, Torchvision, CUDA 12.x
- **Hardware Platform:** Single NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP)
- **Host Workstation:** AMD Ryzen / Intel Core Workstation, 16 GB RAM
- **Training Protocol:** Aligned 50-epoch horizon per image model; 50 equivalent passes (3,000 steps, batch size 64) for causal Transformer
- **Intended Use:** Assistive research prototype and decision-support tool for municipal urban spatial analytics, scenario visualization, and policy drafting
- **Out-of-Scope Use:** Autonomous regulatory zoning enforcement, punitive municipal policing, unverified real-estate automated valuation, or biometric surveillance (see `docs/ETHICS.md`)
- **Shared Domain Limitation:** Trained primarily on UCMerced aerial imagery (US metropolitan areas) and tested in Global South contexts (e.g., Pune, India); domain shift awareness safeguards are strictly enforced.

---

## 1. Denoising Autoencoder with Skip Connections (`ae`)

| Specification | Details |
|:---|:---|
| **Core Architecture** | Pre-trained ResNet-18 Encoder (stem, layer1, layer2, layer3) with **multi-scale transposed convolutional skip connections** (U-Net style). Decodes directly from stem ($64\times 64$), Layer 1 ($32\times 32$), Layer 2 ($16\times 16$), and Layer 3 ($8\times 8$). |
| **Input / Output** | Input: $128 \times 128 \times 3$ RGB corrupted by zero-mean additive Gaussian noise ($\sigma = 0.15$). Output: $128 \times 128 \times 3$ restored clean tile. |
| **Training Objective** | Mean Squared Error: $\mathcal{L}_{\text{AE}} = \frac{1}{N} \sum_{i=1}^N \|x^{(i)} - \hat{x}^{(i)}\|_2^2$ |
| **Training Horizon** | 50 epochs (batch size 16, Adam optimizer, $\text{lr} = 10^{-4}$) |
| **Measured Performance** | **PSNR:** $\mathbf{29.65\,\text{dB}}$ (vs. $25.02\,\text{dB}$ bottleneck baseline; $+4.63\,\text{dB}$ overall gain) <br> **SSIM:** $\mathbf{0.8649}$ <br> **Reconstruction MSE:** $\mathbf{0.00585}$ ($0.00449$ on validation split) <br> **High-Frequency Gain:** $+7.0\,\text{dB}$ individually on dense residential, harbor, and mobile home classes; narrows easy/hard class variance from $7.3\,\text{dB}$ to $2.6\,\text{dB}$. |
| **Role in Pipeline** | Front-end optical restoration; cleans satellite atmospheric scattering, haze, and sensor degradation prior to downstream classification or anomaly ranking. |
| **Limitations** | Optimized for stationary Gaussian sensor degradation; does not perform semantic super-resolution or cloud removal. |

---

## 2. Spatial Variational Autoencoder (`vae`)

| Specification | Details |
|:---|:---|
| **Core Architecture** | ResNet-18 Encoder projecting to parametric mean $\boldsymbol{\mu} \in \mathbb{R}^{64 \times 8 \times 8}$ and log-variance $\log\boldsymbol{\sigma}^2 \in \mathbb{R}^{64 \times 8 \times 8}$ tensors. Preserves an explicit 2D spatial feature map instead of flattening to a 1D vector. Symmetrical transposed-conv decoder. |
| **Training Objective** | $\mathcal{L}_{\text{VAE}} = (0.7\mathcal{L}_1 + 0.3\mathcal{L}_{\text{MSE}}) + \beta \cdot D_{\text{KL}}(q_\phi(z|x) \| p(z))$ with $\beta = 10^{-4}$ (reconstruction-priority regime). |
| **Training Horizon** | 50 epochs (batch size 16, Adam optimizer, $\text{lr} = 10^{-4}$) |
| **Measured Performance** | **Validation PSNR:** $\mathbf{29.75\,\text{dB}}$ <br> **Reconstruction Loss:** $0.0323$ (Total loss $0.0365$) <br> **KL Divergence:** $41.79\,\text{nats}$ <br> **Latent Traversal:** Smooth topological morphing without collapse across agricultural, residential, harbor, and commercial parcels. |
| **Role in Pipeline** | Continuous design space exploration via linear latent interpolation ($z(\alpha) = (1-\alpha)z_A + \alpha z_B$) and unsupervised structural anomaly detection using pixel-wise reconstruction residuals. |
| **Limitations** | Reconstruction-priority regime ($\beta = 10^{-4}$) produces structured latent manifolds but does not support unconstrained random Gaussian sampling; interpolation between real encoded parcels is recommended. |

---

## 3. Territorial Land-Use Classifier (`transformer` route)

| Specification | Details |
|:---|:---|
| **Core Architecture** | ResNet-18 convolutional backbone initialized with ImageNet pre-trained weights; final 1000-way classification head replaced with a 21-way linear projection layer. *(Retained under route name `transformer` for backward compatibility).* |
| **Input / Output** | Input: $128 \times 128 \times 3$ RGB aerial tile. Output: 21-class softmax probability distribution. |
| **Training Objective** | Categorical Cross-Entropy Loss with Adam optimizer ($\text{lr} = 10^{-4}$). |
| **Training Horizon** | 50 epochs (batch size 32, stratified 90/10 split) |
| **Measured Performance** | **Top-1 Validation Accuracy:** $\mathbf{98.10\%}$ <br> **Macro F1-Score:** $\mathbf{0.9784}$ <br> **Validation Loss:** $0.0880$ (Training loss $0.0450$) <br> Zero cross-category confusion between agricultural/green parcels and dense urban infrastructure. |
| **Role in Pipeline** | Automated territorial zoning validation; continuous compliance auditing and semantic verification of synthetic generated parcels. |
| **Limitations** | Single-label classification on $128 \times 128$ resolution; does not produce pixel-level semantic segmentation masks. |

---

## 4. Class-Conditional Deep Convolutional GAN (`gan`)

| Specification | Details |
|:---|:---|
| **Core Architecture** | **Generator ($G$):** Latent noise vector $\mathbf{z} \sim \mathcal{N}(0, \mathbf{I}_{128})$ concatenated with 64-d learned class embedding $\mathbf{e}_y \to$ dense linear projection to $8 \times 8 \times 512 \to$ four residual transposed convolution blocks with Batch Normalization and LeakyReLU $\to$ Tanh transfer ($128 \times 128 \times 3$). <br> **Discriminator ($D$):** Five spectral-normalized Conv2d layers with projection conditioning ($D(x,y) = \psi(\phi(x)) + y^T V \phi(x)$) and auxiliary classification head. |
| **Training Objective** | $\mathcal{L}_G = \mathcal{L}_{\text{adv}} + 0.8\mathcal{L}_{\text{AC}} + 1.2\mathcal{L}_{\text{semantic}}$ with soft label smoothing ($y_{\text{real}}=0.9, y_{\text{fake}}=0.1$) and Exponential Moving Average (EMA, decay 0.999). |
| **Training Horizon** | 50 epochs from scratch (batch size 32, Adam optimizer, $\text{lr}_G = 2 \times 10^{-4}, \text{lr}_D = 2 \times 10^{-4}$) |
| **Measured Performance** | **Minimax Equilibrium:** $D = 1.6387, G = 1.2322$ at epoch 50 <br> **Semantic Recognition Proxy:** $\mathbf{99.40\%}$ (167 out of 168 synthesized tiles independently verified by ResNet-18 classifier across all 21 municipal zoning classes). |
| **Role in Pipeline** | Rapid on-demand synthetic aerial parcel generation for counterfactual spatial planning and data augmentation. |
| **Limitations** | Geometric structural lines (e.g. airport runways) can exhibit minor high-frequency wavy artifacts compared to score-based diffusion models. |

---

## 5. Class-Conditional Denoising Diffusion Probabilistic Model (`diffusion`)

| Specification | Details |
|:---|:---|
| **Core Architecture** | Lightweight U-Net with sinusoidal timestep embeddings $\mathbf{t}$ and class label embeddings $c \in \{1, \dots, 21\}$. $T=1000$ linear variance forward diffusion schedule ($\beta_1 = 10^{-4}, \beta_T = 0.02$). Accelerated reverse synthesis via 20-step Denoising Diffusion Implicit Models (DDIM). |
| **Training Objective** | Simplified Noise MSE: $\mathcal{L}_{\text{diffusion}}(\boldsymbol{\theta}) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}, c}\big[\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, c)\|_2^2\big]$ |
| **Training Horizon** | 50 epochs (batch size 16, Adam optimizer, $\text{lr} = 2 \times 10^{-4}$) |
| **Measured Performance** | **Noise Estimation MSE:** $\mathbf{0.08806}$ (Best checkpoint: $\mathbf{0.08412}$) <br> **Inference Acceleration:** 20 deterministic DDIM steps ($50\times$ faster than standard 1,000-step ancestral DDPM sampling). <br> High morphological boundary definition across diverse land fabrics. |
| **Role in Pipeline** | Stochastic high-fidelity aerial parcel synthesis and multi-scale morphological scenario generation. |
| **Limitations** | Requires 20 sequential network evaluations per tile (approx. 1.8 seconds per tile on RTX 4050 vs. 25 milliseconds for cDCGAN). |

---

## 6. Urban Plan Generator — MiniGPT Transformer (`gpt`)

| Specification | Details |
|:---|:---|
| **Core Architecture** | Custom 4-block causal autoregressive decoder-only Transformer built from scratch. Features character-level vocabulary embedding, learned positional embeddings, pre-LayerNorm multi-head self-attention (4 heads, $d_{\text{model}} = 256$, head dimension 64), and weight-tied linear projection head. Context window length $T=192$. |
| **Training Corpus** | `backend/corpus/urban_planning.txt` — domain-curated sustainable urbanism corpus detailing Floor Space Index (FSI), Transit-Oriented Development (TOD), stormwater drainage, rainwater harvesting, and green buffer zoning. |
| **Training Objective** | Next-Token Cross-Entropy Loss: $P(w_t | w_{<t}) = \text{Softmax}(\mathbf{Q}\mathbf{K}^T / \sqrt{d_k} \cdot \mathbf{V})$. |
| **Training Horizon** | 3,000 optimization steps (batch size 64), equivalent to 50 passes over the curated domain corpus. |
| **Measured Performance** | **Held-out Perplexity (PPL):** $\mathbf{1.087}$ <br> **Bits-Per-Character (BPC):** $\mathbf{0.1199}$ <br> **Validation Cross-Entropy:** $0.0836$ <br> Dynamic top-$k$ ($k=40$) and temperature-scaled sampling seeded directly from spatial classification telemetry. |
| **Role in Pipeline** | Qualitative translation layer; converts numerical zoning classifications and anomaly scores into coherent municipal planning policy briefs and development guidelines. |
| **Limitations** | Small-scale domain model; does not have generalized web knowledge or external legal statute lookup. Outputs are advisory drafts requiring planner verification. |

---

## 🌿 Green AI Hardware & Carbon Footprint Audit

All six models were trained and benchmarked on a single consumer laptop workstation. Energy consumption was profiled to verify Green AI accessibility:

| Model Architecture | Training Horizon | Wall Time (min) | Mean Power (W) | Energy (kWh) | Carbon Footprint (gCO$_2$e) |
|:---|:---:|:---:|:---:|:---:|:---:|
| U-Net Denoising Autoencoder | 50 epochs | 15.2 | 118 | 0.030 | 21.3 |
| Spatial Variational Autoencoder | 50 epochs | 20.4 | 118 | 0.040 | 28.4 |
| ResNet-18 Land-Use Classifier | 50 epochs | 18.5 | 123 | 0.038 | 27.0 |
| Residual Class-Conditional DCGAN | 50 epochs | 17.5 | 120 | 0.035 | 24.8 |
| Conditional Diffusion Model (DDPM) | 50 epochs | 22.0 | 123 | 0.045 | 31.9 |
| MiniGPT Planning Transformer | 50 equiv. epochs | 8.3 | 108 | 0.015 | 10.6 |
| **Total Integrated Framework** | **Aligned 50-Epoch Suite** | **101.9 min** | **118 W avg** | **0.203 kWh** | **144.0 gCO$_2$e** |

*Carbon intensity factor: $0.708\,\text{kg CO}_2/\text{kWh}$ (Central Electricity Authority).*
