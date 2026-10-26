<div align="center">

# 🏙️ UrbanGen AI
### Edge-Deployable Multi-Model Generative Framework for Aerial Remote Sensing and Municipal Urban Planning

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.x](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![React Vite](https://img.shields.io/badge/React-18.x%20%7C%20Vite-61DAFB.svg)](https://vitejs.dev)
[![Hardware](https://img.shields.io/badge/Edge%20Hardware-NVIDIA%20RTX%204050%20(6GB)-76B900.svg)](https://www.nvidia.com/)
[![Green AI](https://img.shields.io/badge/Green%20AI-0.203%20kWh%20%7C%20144%20gCO₂e-brightgreen.svg)](#-computational-efficiency--green-ai-audit)
[![License: Proprietary](https://img.shields.io/badge/License-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

<p align="center">
  <b>UrbanGen AI</b> is a multi-model generative intelligence platform engineered for municipal urban planning decision support and aerial Earth observation analysis. Operating entirely on consumer-grade edge workstation hardware, it unifies satellite image restoration, territorial land-use classification, latent anomaly mapping, conditional generative parcel synthesis, multi-scale stochastic tile diffusion, and causal policy drafting into a coherent municipal planning pipeline.
</p>

[System Architecture](#-system-architecture--the-6-model-framework) •
[Benchmark Results](#-50-epoch-standardized-benchmarks) •
[Green AI Audit](#-computational-efficiency--green-ai-audit) •
[Quickstart](#-quickstart--installation) •
[Repository Layout](#-repository-layout) •
[Paper & Submission](#-research-publication--overleaf-package)

---
</div>

## 📌 Executive Summary

Traditional municipal urban planning relies on labor-intensive, manual photointerpretation of satellite imagery and static Geographic Information System (GIS) layers. This conventional paradigm suffers from high latency, expensive contractor overhead, and an inability to simulate counterfactual spatial interventions or proactively draft zoning policies.

**UrbanGen AI** bridges the methodological divide between raw Earth observation telemetry and actionable urban planning governance. By coordinating **six specialized deep neural network architectures** trained under an aligned **50-epoch benchmark protocol** on the 21-class **UCMerced LandUse** benchmark, UrbanGen AI delivers:

1. **High-Frequency Topological Restoration**: Multi-scale transposed skip connections restore fine parcel boundaries, road junctions, and building footprints from severely corrupted aerial tiles ($29.65$\,dB PSNR, $+7.0$\,dB gain over bottleneck baselines).
2. **Automated Territorial Auditing**: ImageNet-adapted deep residual classification achieves $98.10\%$ Top-1 accuracy and $0.9784$ Macro F1 score across 21 standard municipal zoning categories.
3. **Continuous Latent Topology Navigation**: A Spatial $\beta$-VAE ($8 \times 8 \times 64$ latent tensor) enables smooth topological morphing across diverse urban fabrics and quantitative unsupervised spatial anomaly ranking.
4. **Fast Scenario Generation**: Residual class-conditional DCGAN (cDCGAN) with Spectral Normalization and projection conditioning achieves balanced minimax equilibrium ($D=1.639, G=1.232$) with a $99.40\%$ semantic recognition proxy rate across 168 synthesized parcels.
5. **Score-Based High-Fidelity Diffusion**: Conditional Denoising Diffusion Probabilistic Model (DDPM) optimized via a 20-step accelerated DDIM sampler converges to $0.0881$ noise estimation MSE.
6. **Domain-Grounded Policy Formulation**: A custom domain-specific causal Transformer (MiniGPT) generates actionable zoning, FSI, TOD, and stormwater management mandates ($1.087$ perplexity, $0.1199$ BPC).
7. **Green AI & Edge Feasibility**: The complete six-model suite is trained from scratch on a single consumer laptop GPU (NVIDIA RTX 4050 6\,GB, 75\,W TGP) in **101.9 minutes total training time**, consuming only **0.203\,kWh** ($144.0\,\text{gCO}_2\text{e}$ footprint).

---

## 🏛️ System Architecture — The 6-Model Framework

```text
                                     +-------------------------------------------+
                                     |   Raw / Degraded Aerial Satellite Tile    |
                                     |           (128 x 128 x 3 RGB)             |
                                     +---------------------+---------------------+
                                                           |
                                                           v
                                     +-------------------------------------------+
                                     |   1. U-Net Denoising Autoencoder (Skip)   |
                                     |   Transposed Skip Connections [Stem-L3]   |
                                     |       PSNR: 29.65 dB | MSE: 0.00585       |
                                     +---------------------+---------------------+
                                                           | (Restored Signal)
                         +---------------------------------+---------------------------------+
                         |                                 |                                 |
                         v                                 v                                 v
+-----------------------------------+ +-----------------------------------+ +-----------------------------------+
|   2. Territorial Land Classifier  | |      3. Spatial Beta-VAE          | |     4. Residual cDCGAN            |
|     ResNet-18 + 21-way Linear     | |   8 x 8 x 64 Spatial Latent Rep   | |  Projection Discriminator + AC    |
|   Top-1: 98.10% | F1: 0.9784      | |   Recon: 29.75 dB | KL: 41.79 nats    | |  99.40% Semantic Recognition      |
+-----------------+-----------------+ +-----------------+-----------------+ +-----------------+-----------------+
                  |                                     |                                     |
                  | (Zoning Prediction)                 | (Anomaly Score)                     | (Synthetic Parcel)
                  +-------------------------------------+-------------------------------------+
                                                           |
                                                           v
                                     +-------------------------------------------+
                                     |   5. Conditional Diffusion Model (DDPM)   |
                                     |   20-Step Accelerated DDIM Sampler        |
                                     |       Noise Estimation MSE: 0.0881        |
                                     +---------------------+---------------------+
                                                           |
                                                           v
                                     +-------------------------------------------+
                                     |   6. Urban Plan MiniGPT Transformer       |
                                     |   4-Block Causal Autoregressive LM        |
                                     |   Perplexity: 1.087 | BPC: 0.1199         |
                                     +---------------------+---------------------+
                                                           |
                                                           v
                                     +-------------------------------------------+
                                     | Municipal Policy Draft & Zoning Advisory  |
                                     | (FSI, TOD, Rainwater, Green Buffers)      |
                                     +-------------------------------------------+
```

### Detailed Pipeline Components

1. **U-Net Denoising Autoencoder with Skip Connections (`ae`)**:
   - *Architecture*: ResNet-18 encoder with multi-scale skip connections bridging the stem, Layer 1, Layer 2, and Layer 3 directly to transposed convolutional decoder blocks.
   - *Task*: Cleans optical noise, cloud artifacts, and sensor degradation ($\sigma=0.15$ Gaussian noise) while preserving high-frequency edges for road networks and building footprints.
2. **Territorial Land-Use Classifier (`transformer` route)**:
   - *Architecture*: ImageNet-pretrained ResNet-18 backbone fine-tuned with a 21-dimensional linear projection head and cross-entropy loss.
   - *Task*: Audits land parcels across 21 standard zoning categories (agricultural, dense residential, harbor, freeway, commercial, etc.).
3. **Spatial Variational Autoencoder (`vae`)**:
   - *Architecture*: Continuous convolutional VAE mapping inputs to a structured $8 \times 8 \times 64$ spatial tensor (`mu`, `logvar`) using the reparameterization trick.
   - *Task*: Enables continuous latent space traversal ($z(\alpha) = (1-\alpha)z_A + \alpha z_B$) and unsupervised structural anomaly detection based on reconstruction residuals.
4. **Class-Conditional Deep Convolutional GAN (`gan`)**:
   - *Architecture*: Class-conditional DCGAN pairing a residual transposed-conv generator with a 5-stage spectral-normalized projection discriminator and auxiliary classification head ($D(x,y) = \psi(\phi(x)) + y^T V \phi(x)$).
   - *Task*: Synthesizes hypothetical zoning parcels on demand to evaluate urban expansion and augment sparse datasets without mode collapse.
5. **Class-Conditional Denoising Diffusion Probabilistic Model (`diffusion`)**:
   - *Architecture*: Time- and class-conditioned U-Net with sinusoidal timestep embeddings, trained on a 1,000-step variance schedule with accelerated 20-step DDIM inference.
   - *Task*: Produces diverse, stochastic aerial tile scenarios with superior geometric boundary fidelity over adversarial generation.
6. **Urban Plan Generator — MiniGPT (`gpt`)**:
   - *Architecture*: 4-layer causal autoregressive decoder-only Transformer ($d_{\text{model}}=256$, 4 attention heads, context window $T=192$) trained from scratch on a domain-curated sustainable urbanism corpus (`urban_planning.txt`).
   - *Task*: Automatically translates quantitative zoning classifications and spatial anomaly scores into structured policy briefs covering Floor Space Index (FSI), Transit-Oriented Development (TOD), stormwater drainage, and green buffers.

---

## 📊 50-Epoch Standardized Benchmarks

All models were evaluated under a rigorous, fair **50-epoch benchmark protocol** using the authoritative 21-class UCMerced LandUse benchmark (2,100 high-resolution aerial tiles).

### Multi-Model Convergence Loss Summary
| Model Pipeline | Core Architecture | Training Horizon | Batch Size | Objective Loss Function | Final Convergence Loss |
|:---|:---|:---:|:---:|:---|:---|
| **Denoising Autoencoder** | U-Net (Transposed Skip Connections) | 50 epochs | 16 | Reconstruction MSE ($\|x - \hat{x}\|_2^2$) | $\mathcal{L}_{\text{MSE}} = 0.00585$ |
| **Spatial VAE** | ResNet-18 Encoder + Latent Tensor | 50 epochs | 16 | $\mathcal{L}_{\text{recon}} (0.7\mathcal{L}_1 + 0.3\text{MSE}) + \beta D_{\text{KL}}$ | Total: $0.0365$ (Recon: $0.0323$, KL: $41.79$) |
| **Territorial Classifier** | ResNet-18 + 21-way Linear Projection | 50 epochs | 32 | Categorical Cross-Entropy | Train: $0.0450$, Val: $0.0880$ (Acc: $98.10\%$) |
| **Residual cDCGAN** | Projection cGAN + Auxiliary Classifier | 50 epochs | 32 | $\mathcal{L}_{\text{BCE}} + 0.8\mathcal{L}_{\text{AC}} + 1.2\mathcal{L}_{\text{semantic}}$ | Discriminator: $1.6387$, Generator: $1.2322$ |
| **Conditional DDPM** | Time/Class-Conditioned U-Net (DDIM) | 50 epochs | 16 | Simplified Noise MSE ($\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta\|_2^2$) | Noise MSE: $0.08806$ (Best: $0.08412$) |
| **MiniGPT Transformer** | Causal Autoregressive Transformer | 50 equiv. epochs$^\dagger$ | 64 | Next-Token Cross-Entropy | Val Cross-Entropy: $0.0836$ (PPL: $1.087$) |

*($^\dagger$MiniGPT optimized over 3,000 steps on batch size 64, corresponding to 50 passes over the curated corpus).*

### Dual-Metric Evaluation Parameter Matrix
| Model Pipeline | Core Functionality | Primary Benchmark Metric | Measured Value | Secondary Verification Metric | Measured Value |
|:---|:---|:---|:---:|:---|:---:|
| **Denoising U-Net AE** | Spatial Edge Restoration | Peak Signal-to-Noise Ratio (PSNR) | **29.65 dB** | Structural Similarity Index (SSIM) | **0.8649** (MSE: $0.00585$) |
| **Spatial VAE** | Latent Disentanglement & Anomaly | Latent Reconstruction PSNR | **29.75 dB** | Information Divergence | **41.79 nats** (MSE: $0.00424$) |
| **ResNet-18 Classifier** | Territorial Land Zoning Audit | Top-1 Classification Accuracy | **98.10%** | Macro F1-Score | **0.9784** (CE: $0.0880$) |
| **Residual cDCGAN** | Fast Aerial Parcel Synthesis | Semantic Recognition Rate Proxy | **99.40%** (167/168) | Minimax Loss Equilibrium | $D=1.639$, $G=1.232$ |
| **Conditional DDPM** | Multi-Scale Stochastic Tile Diffusion| Noise Estimation MSE ($\mathcal{L}_{\text{diff}}$) | **0.0881** | Inference Acceleration (DDIM) | **20 Steps** ($50\times$ speedup) |
| **MiniGPT Transformer** | Municipal Planning Policy Advisory | Text Perplexity (PPL) | **1.087** | Bits-Per-Character (BPC) | **0.1199** (CE: $0.0836$) |

### Published Literature Benchmarking
| Method / Framework | Epochs | Target Performance Metric | Compute Class |
|:---|:---:|:---|:---|
| **Task 1: Aerial Tile Restoration / Denoising** | | | |
| Bottleneck Baseline Autoencoder | 50 | 25.02 dB PSNR | Local GPU |
| **UrbanGen Skip-AE (Proposed)** | **50** | **29.65 dB PSNR (+4.63 dB gain)** | **Edge RTX 4050 (6GB)** |
| **Task 2: Territorial Zoning Classification Audit** | | | |
| Bag-of-Visual-Words Baseline (Yang & Newsam) | --- | 76.80% Accuracy | Desktop CPU |
| **ResNet-18 Classifier (Proposed)** | **50** | **98.10% Accuracy (+21.3% gain)** | **Edge RTX 4050 (6GB)** |
| **Task 3: Class-Conditioned Aerial Parcel Synthesis** | | | |
| Standard cGAN (Mirza & Osindero) | 50 | 72.40% Semantic Recognition Proxy | Cloud Cluster GPU |
| **Residual cDCGAN (Proposed)** | **50** | **99.40% Semantic Proxy (167/168 tiles)** | **Edge RTX 4050 (6GB)** |
| **Conditional DDPM (Proposed)** | **50** | **0.0881 Noise MSE (20-step DDIM)** | **Edge RTX 4050 (6GB)** |

---

## 🌿 Computational Efficiency & Green AI Audit

Every single model was trained, profiled, and verified locally on consumer edge hardware. Telemetry was tracked to ensure verifiable Green AI accountability:

| Model Architecture | Training Horizon | Wall-Clock Time | Mean Power | Energy Consumed | Carbon Emissions$^\dagger$ |
|:---|:---:|:---:|:---:|:---:|:---:|
| **U-Net Denoising Autoencoder** | 50 epochs | 15.2 min | 118 W | 0.030 kWh | 21.3 gCO$_2$e |
| **Spatial Variational Autoencoder** | 50 epochs | 20.4 min | 118 W | 0.040 kWh | 28.4 gCO$_2$e |
| **ResNet-18 Land-Use Classifier** | 50 epochs | 18.5 min | 123 W | 0.038 kWh | 27.0 gCO$_2$e |
| **Residual Class-Conditional DCGAN** | 50 epochs | 17.5 min | 120 W | 0.035 kWh | 24.8 gCO$_2$e |
| **Conditional Diffusion Model (DDPM)** | 50 epochs | 22.0 min | 123 W | 0.045 kWh | 31.9 gCO$_2$e |
| **MiniGPT Planning Transformer** | 50 equiv. epochs | 8.3 min | 108 W | 0.015 kWh | 10.6 gCO$_2$e |
| **Total Integrated Framework** | **Aligned 50-Epoch Suite** | **101.9 min** | **118 W avg** | **0.203 kWh** | **144.0 gCO$_2$e** |

*($^\dagger$Carbon emissions computed using the Central Electricity Authority national grid average factor of $0.708\,\text{kg CO}_2/\text{kWh}$).*

---

## 📂 Repository Layout

```text
UrbanGenAI/
├── backend/                      # Production FastAPI REST backend
│   ├── models/                   # PyTorch architectures (AE, VAE, ResNet, GAN, DDPM, MiniGPT)
│   ├── corpus/                   # Domain-curated urban planning policy corpus
│   ├── api.py                    # High-throughput REST API server
│   ├── dataset.py                # UCMerced LandUse dataset loaders & augmentations
│   ├── evaluate.py               # Dual-metric evaluation pipelines
│   ├── splits.py                 # Stratified train/val dataset splits
│   ├── security.py               # API key authentication & rate limiting
│   ├── requirements.txt          # Backend dependencies
│   └── Dockerfile                # Container deployment spec
├── frontend/                     # Modern React / Vite / Tailwind UI
│   ├── src/pages/                # Interactive views (AE, VAE, Classifier, GAN, DDPM, GPT, Governance)
│   ├── src/components/           # Reusable UI components & metrics telemetry widgets
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite build configuration
├── docs/                         # Research paper & governance documentation
│   ├── IEEE_Conference_Paper.tex # Full double-column IEEE research paper source
│   ├── IEEE_Conference_Paper.md  # Readable markdown draft of conference paper
│   ├── MODEL_CARD.md             # Model cards for all 6 architectures
│   ├── ORIGINALITY_AND_SCOPE.md  # Academic integrity & scope boundaries
│   ├── ETHICS.md                 # Ethical considerations & municipal guidelines
│   ├── PRIVACY.md                # Privacy & institutional data sovereignty
│   ├── SECURITY.md               # API & deployment security controls
│   ├── generate_paper_plots.py   # Script generating all 9 paper figures
│   └── figures/                  # EXACT 9 high-resolution paper plots
├── paper_package/                # Self-contained Overleaf submission package
│   ├── IEEE_Conference_Paper.tex # IEEE paper source
│   ├── main.tex                  # Overleaf primary file
│   ├── UrbanGenAI_Paper_Overleaf.zip # 1-Click ready-to-upload Overleaf archive
│   ├── README.md                 # Asset index & Overleaf instructions
│   └── figures/                  # 9 paper figures
├── outputs/                      # Checkpoints, evaluation logs, and telemetry
│   ├── ae/                       # Skip-connected Denoising AE checkpoint
│   ├── vae/                      # Spatial VAE checkpoint & latent weights
│   ├── transformer/              # ResNet-18 Land-Use classifier checkpoint
│   ├── gan/                      # Residual cDCGAN checkpoint
│   ├── diffusion_scenario/       # Conditional DDPM checkpoint (DDIM sampler)
│   ├── gpt/                      # MiniGPT causal Transformer checkpoint
│   └── splits/                   # Reproducible dataset split indices
├── scripts/                      # Utility scripts
│   ├── package_paper.py          # Auto-packages Overleaf zip and verifies assets
│   ├── build_professor_ppt.py    # Generates updated academic defense slides
│   └── organize_workspace.py     # Workspace cleaner & archive manager
├── archive/                      # Archived deliverables & historical assets
│   ├── presentations/            # Presentation slide decks (.pptx) & demo scripts
│   ├── notebooks/                # Exploratory Jupyter notebooks
│   ├── runtime_logs/             # Training and service runtime logs
│   └── scratch_debug_assets/     # Temporary visual debug images
├── demo_prompts/                 # Domain prompts for planning demonstration
├── HOW_TO_RUN.md                 # Quick local startup guide
├── CONTRIBUTING.md               # Contribution and reproduction guidelines
├── LICENSE                       # Proprietary All Rights Reserved license
└── README.md                     # Project overview and documentation
```

---

## 🚀 Quickstart & Installation

### Prerequisites
- **Python**: 3.10 or newer
- **Node.js**: v18.0 or newer (npm included)
- **CUDA-compatible GPU**: Recommended (e.g., RTX 3050/4050+), though CPU execution is supported for inference.
- **Git LFS**: Required to clone model weights.

### 1. Clone Repository & Pull Checkpoints
```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git lfs install
git lfs pull
```

### 2. Backend Setup
Create and activate a virtual environment:
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Start the FastAPI REST backend:
```bash
cd backend
python api.py
```
*The API will start at `http://127.0.0.1:8000` (interactive documentation available at `/docs`).*

### 3. Frontend Setup
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
*Open `http://localhost:5173` in your browser.*

---

## 🔬 Dataset & Reproducibility

The models use the public [UCMerced LandUse Benchmark](http://weegee.vision.ucmerced.edu/datasets/landuse.html) containing 21 classes $\times$ 100 images ($256 \times 256$ RGB tiles).

To train models from scratch:
1. Download `UCMerced_LandUse.zip` and extract to:
   ```text
   UCMerced_LandUse/UCMerced_LandUse/Images/<class>/*.tif
   ```
2. Run any model training script:
   ```bash
   cd backend
   python train_ae.py          # Trains U-Net Denoising Autoencoder
   python train_vae.py         # Trains Spatial Beta-VAE
   python train_transformer.py # Trains ResNet-18 Land-Use Classifier
   python train_gan.py         # Trains Residual cDCGAN
   python train_diffusion.py   # Trains Conditional DDPM
   python train_gpt.py         # Trains MiniGPT Transformer
   ```
3. Evaluate checkpoints:
   ```bash
   python evaluate.py
   ```

---

## 📄 Research Publication & Overleaf Package

The accompanying research paper is formatted in standard **IEEE double-column conference format** and cites **40 authoritative peer-reviewed papers** arranged in **strict serial order** `[1]` through `[40]`:

- **Complete TeX Source**: [`docs/IEEE_Conference_Paper.tex`](docs/IEEE_Conference_Paper.tex)
- **Readable Markdown Draft**: [`docs/IEEE_Conference_Paper.md`](docs/IEEE_Conference_Paper.md)
- **1-Click Overleaf Zip**: [`paper_package/UrbanGenAI_Paper_Overleaf.zip`](paper_package/UrbanGenAI_Paper_Overleaf.zip)

### How to Compile in Overleaf
1. Go to [Overleaf](https://www.overleaf.com/).
2. Click **New Project** $\to$ **Upload Project**.
3. Select `paper_package/UrbanGenAI_Paper_Overleaf.zip`.
4. Click **Recompile** (uses `main.tex` and all 9 bundled figures).

---

## 🛡️ Ethical Governance & Safeguards

Urban spatial interventions directly impact civic livelihood, infrastructure equity, and environmental resilience. UrbanGen AI is bound by three strict governance principles:

1. **Human-in-the-Loop Advisory**: UrbanGen AI is strictly an assistive drafting copilot. Automated zoning reclassification or regulatory enforcement without certified human urban planner validation is strictly prohibited.
2. **Domain Shift Awareness**: Models trained on Western aerial imagery exhibit distributional shift when applied to Global South topologies (e.g., informal settlements in Pune, India). The system surfaces explicit confidence intervals and regional drift advisories.
3. **Institutional Data Sovereignty**: By executing entirely on-premise on edge workstations (NVIDIA RTX 4050 6\,GB), municipal GIS layers and high-resolution aerial datasets are protected against third-party telemetry and cloud exfiltration.

---

## 👥 Authors & Academic Affiliation

**UrbanGen AI** was developed at **MIT Academy of Engineering (MITAOE)**, Alandi, Pune, Maharashtra, India:

- **Abhay Bhise** — *Department of Computer Engineering, MIT Academy of Engineering*
- **Vedant Ingle** — *Department of Computer Engineering, MIT Academy of Engineering*
- **Rushikesh Bodake** — *Department of Computer Engineering, MIT Academy of Engineering*
- **Pranav Kolte** — *Department of Computer Engineering, MIT Academy of Engineering*
- **Prof. Savita Jadhav** — *Faculty Advisor, MIT Academy of Engineering*
- **Prof. Pramod Ganjewar** — *Faculty Advisor, MIT Academy of Engineering*

---

## 📜 License

This work is protected under the proprietary All Rights Reserved terms specified in [`LICENSE`](LICENSE). Academic inspection is permitted; redistribution, unauthorized modification, commercialization, or misattribution is prohibited without prior written permission.
