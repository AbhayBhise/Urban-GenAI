# UrbanGenAI Implementation Handbook

## Primary Engineering and Research-Maintenance Reference

This handbook is the primary technical reference for the UrbanGenAI multi-model research prototype. It documents repository architecture, reproducible setup commands, layer-by-layer tensor shapes, objective functions, evaluation protocols, API contracts, frontend routes, and empirical results.

---

## 1. Executive Project Overview

UrbanGenAI connects Earth observation imagery with multi-paradigm generative artificial intelligence to support urban analysis and planning workflows:

1. **Denoising Autoencoder (AE)**: Unsupervised feature extraction and aerial tile reconstruction with U-Net skip connections.
2. **Spatial Variational Autoencoder (VAE)**: Probabilistic latent modeling ($8 \times 8 \times 64 = 4{,}096$ spatial dimensions) for structural interpolation and reconstruction-error anomaly localization.
3. **Land-Use Classifier**: 21-class aerial zoning classification (fine-tuned ResNet18) providing automated parcel audit and class-conditional recognition.
4. **Conditional DCGAN**: Class-conditional aerial tile synthesis with residual upsampling and projection discriminator with auxiliary classifier guidance.
5. **Urban Scenario Diffusion (DDPM / DDIM)**: Source-conditioned, class-guided aerial scenario visualization reversing Gaussian noise conditioned on existing parcel morphology.
6. **MiniGPT Urban Plan Generator**: Character-level decoder-only causal Transformer trained from scratch to synthesize structured planning policies from land-use statistics.

---

## 2. Complete Directory Structure

```text
Urban-GenAI/
├── backend/
│   ├── corpus/
│   │   ├── build_corpus.py             # Compiles urban planning text corpus
│   │   └── urban_planning.txt          # Domain corpus for MiniGPT training
│   ├── models/
│   │   ├── autoencoder.py              # DenoisingAE with U-Net skip connections
│   │   ├── classifier.py               # UrbanClassifier (fine-tuned ResNet18)
│   │   ├── diffusion.py                # DiffusionUNet and DDPM / DDIM Sampler
│   │   ├── gan.py                      # Residual Generator & Projection Discriminator
│   │   ├── gpt.py                      # MiniGPT causal decoder-only Transformer
│   │   ├── perceptual_loss.py          # VGG-based perceptual feature loss
│   │   ├── transformer.py              # Backward-compatible shim and re-exports
│   │   └── vae.py                      # Spatial VAE with compact skip pathways
│   ├── api.py                          # FastAPI REST application & inference handlers
│   ├── dataset.py                      # PyTorch Dataset wrappers & augmentations
│   ├── evaluate.py                     # Standalone classifier evaluation script
│   ├── generate.py                     # Batch generator for evaluation
│   ├── rag_pipeline.py                 # Grounded retrieval and indicator scoring
│   ├── splits.py                       # Reproducible stratified train/val/test splits
│   ├── train_ae.py                     # Autoencoder training script
│   ├── train_classifier.py             # Classifier fine-tuning script
│   ├── train_diffusion.py              # Scenario diffusion training with GPU telemetry
│   ├── train_gan.py                    # Conditional DCGAN training script
│   ├── train_gpt.py                    # MiniGPT training script
│   ├── train_vae.py                    # Spatial VAE training script
│   ├── Dockerfile                      # Production container deployment definition
│   └── requirements.txt                # Python backend dependencies
├── demo_prompts/                       # Sample planning prompt text files
├── docs/
│   ├── figures/                        # High-resolution paper and evaluation figures
│   │   ├── fig_ae_convergence.png
│   │   ├── fig_ae_crisp_restoration.png
│   │   ├── fig_classifier_metrics.png
│   │   ├── fig_diffusion_training.png
│   │   ├── fig_energy_carbon.png
│   │   ├── fig_gan_diverse_generation.png
│   │   ├── fig_gan_dynamics.png
│   │   ├── fig_gan_synthetic_tiles.png
│   │   ├── fig_psnr_comparison.png
│   │   ├── fig_vae_interpolation.png
│   │   ├── fig_vae_matched_sampling.png
│   │   ├── fig_vae_multi_interpolation.png
│   │   ├── fig_vae_real_interpolation.png
│   │   ├── fig_vae_samples.png
│   │   └── fig_vae_tradeoff.png
│   ├── IEEE_Conference_Paper.md        # Formatted conference manuscript
│   ├── IEEE_Conference_Paper.tex       # Camera-ready IEEEtran LaTeX manuscript
│   ├── MODEL_CARD.md                   # Formal Model Card and empirical boundaries
│   └── UrbanGenAI_Implementation_Handbook.md # This operational handbook
├── frontend/
│   ├── src/
│   │   ├── components/                 # Shared UI components (charts, headers, badges)
│   │   ├── lib/
│   │   │   └── api.ts                  # Fetch client with API key and error handling
│   │   ├── pages/
│   │   │   ├── research/               # Gap analysis, literature survey, decision support
│   │   │   ├── AEArchitecture.tsx      # Interactive Autoencoder diagram
│   │   │   ├── ClassifierArchitecture.tsx # Interactive Classifier diagram
│   │   │   ├── Datasets.tsx            # UCMerced dataset visual explorer
│   │   │   ├── Diffusion.tsx           # Scenario Diffusion interactive generator
│   │   │   ├── DiffusionArchitecture.tsx # Interactive Diffusion U-Net diagram
│   │   │   ├── Evaluation.tsx          # Multi-tab empirical metrics dashboard
│   │   │   ├── FutureScope.tsx         # Academic & systems roadmap
│   │   │   ├── GANArchitecture.tsx     # Interactive GAN architecture diagram
│   │   │   ├── Glossary.tsx            # Comprehensive notation and parameter glossary
│   │   │   ├── Governance.tsx          # Safety, privacy, and regulatory documentation
│   │   │   ├── Landing.tsx             # Interactive platform overview and workflow
│   │   │   ├── ModelComparison.tsx     # Side-by-side trade-off matrix
│   │   │   ├── ModelExplorer.tsx       # Architecture hub
│   │   │   ├── SystemArchitecture.tsx  # Full end-to-end dataflow diagram
│   │   │   ├── SystemInfo.tsx          # Server runtime and hardware diagnostics
│   │   │   ├── Training.tsx            # Real persisted loss curve visualization
│   │   │   └── VAEArchitecture.tsx     # Interactive Spatial VAE diagram
│   │   ├── App.tsx                     # Main layout, router, navigation, and inference UI
│   │   └── index.css                   # Theme-aware CSS design system
│   ├── index.html                      # HTML5 root with metadata
│   ├── package.json                    # Frontend dependencies and build scripts
│   ├── tsconfig.json                   # TypeScript compiler configuration
│   └── vite.config.ts                  # Vite bundler configuration
├── outputs/
│   ├── ae/                             # Checkpoints and training history for AE
│   ├── diffusion_scenario/             # Checkpoints, telemetry, and histories for Diffusion
│   ├── gan/                            # Checkpoints, samples, and histories for GAN
│   ├── gpt/                            # Checkpoints and vocab mappings for MiniGPT
│   ├── splits/                         # Seed 42 stratified split definition
│   ├── transformer/                    # Checkpoints and history for Land-Use Classifier
│   ├── vae/                            # Checkpoints and history for Spatial VAE
│   └── system_validation_report.json   # Machine-readable validation results
├── scripts/
│   ├── build_ppt.py                    # Presentation deck generator
│   └── validate_system.py              # Automated system and model validation protocol
├── UCMerced_LandUse/
│   └── UCMerced_LandUse/
│       └── Images/                     # 21 classes x 100 images = 2,100 TIFF tiles
├── CONTRIBUTING.md                     # Contribution guidelines and GAN instructions
├── HOW_TO_RUN.md                       # Quickstart instructions
├── LICENSE                             # MIT License
└── README.md                           # Repository README
```

---

## 3. Environment Setup & Execution Commands

### Prerequisites
- Python 3.10+ (tested on Python 3.11.9)
- Node.js v18+ (tested on Node v24.14.1, npm 11.11.0)
- Git & Git LFS (for large model weights)

### Step 1: Install Backend Dependencies
```powershell
# In repository root
pip install -r backend/requirements.txt
```

### Step 2: Extract & Verify Dataset
Ensure the UCMerced dataset is at `UCMerced_LandUse/UCMerced_LandUse/Images` (21 subdirectories, each containing 100 `.tif` files, 2,100 total images).

```powershell
# Run validation protocol to confirm dataset readability
python scripts/validate_system.py
```

### Step 3: Start FastAPI Backend
```powershell
# Run from repository root
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```
*Backend runs on `http://127.0.0.1:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.*

### Step 4: Start Frontend Development Server
```powershell
cd frontend
npm install
npm run dev
```
*Frontend runs on `http://localhost:5173`.*

### Step 5: Build Production Frontend
```powershell
cd frontend
npm run build
```

---

## 4. Model Architecture & Mathematical Formulations

### 4.1 Denoising Autoencoder (AE)
- **File**: `backend/models/autoencoder.py`
- **Training Script**: `backend/train_ae.py`
- **Checkpoint**: `outputs/ae/model.pth` ($3{,}869{,}635$ parameters)
- **Architecture**: Modified ResNet18 encoder with U-Net skip connections to decoder stages.
  - Encoder Stem: $128 \times 128 \times 3 \to 64 \times 64 \times 64$
  - Layer 1: $32 \times 32 \times 64$ ($s_1$ skip)
  - Layer 2: $16 \times 16 \times 128$ ($s_2$ skip)
  - Layer 3 (Bottleneck): $8 \times 8 \times 256$ ($s_3$)
  - Decoder 1: $8 \times 8 \times 256 \to 16 \times 16 \times 128$ concatenated with $s_2$ ($16 \times 16 \times 128$)
  - Decoder 2: $16 \times 16 \times 128 \to 32 \times 32 \times 64$ concatenated with $s_1$ ($32 \times 32 \times 64$)
  - Decoder 3: $32 \times 32 \times 64 \to 64 \times 64 \times 32$ concatenated with $s_0$ ($64 \times 64 \times 64$)
  - Output Stage: $64 \times 64 \times 32 \to 128 \times 128 \times 3$ with $\tanh$.
- **Loss Function**:
  $$\mathcal{L}_{\text{AE}} = \frac{1}{HW} \sum_{i,j} \|x_{i,j} - \hat{x}_{i,j}\|^2$$
- **Empirical Results**:
  - Test MSE: $0.000898$ ($30.47\text{ dB PSNR}$, $0.8322\text{ SSIM}$).
  - Convergence: Initial loss $0.1155 \to 0.00585$ across 50 epochs.

### 4.2 Spatial Variational Autoencoder (VAE)
- **File**: `backend/models/vae.py`
- **Training Script**: `backend/train_vae.py`
- **Checkpoint**: `outputs/vae/model.pth` ($3{,}844{,}931$ parameters)
- **Architecture**: Spatial latent mapping preserving $8 \times 8$ parcel arrangement with $64$ latent channels ($4{,}096$ total latent dimensions).
  - Encoder: ResNet18 backbone through Layer 3.
  - $\mu$ Head: $1 \times 1$ Conv ($256 \to 64$).
  - $\log \sigma^2$ Head: $1 \times 1$ Conv ($256 \to 64$, clamped to $[-20, 20]$).
  - Reparameterization: $z = \mu + \epsilon \odot \exp(0.5 \log \sigma^2)$, $\epsilon \sim \mathcal{N}(0, I)$.
  - Compact Skips: Narrowed projection channels ($64$ for $s_1, s_2$ and $16$ for $s_0$) to prevent posterior collapse while preserving edge fidelity.
- **Loss Function**:
  $$\mathcal{L}_{\text{VAE}} = \mathcal{L}_{\text{recon}}(x, \hat{x}) + \beta D_{\text{KL}}\left(q(z|x) \parallel \mathcal{N}(0, I)\right)$$
  $$D_{\text{KL}} = -\frac{1}{2} \sum_{k=1}^K \left(1 + \log \sigma_k^2 - \mu_k^2 - \sigma_k^2\right)$$
- **Empirical Results**:
  - Test Reconstruction MSE: $0.000701$ ($31.54\text{ dB PSNR}$).
  - Active Latent KL Divergence: $11.9\text{ nats}$ ($4{,}096$ active spatial dimensions).
  - Anomaly Baseline: Calibrated on $294$ in-distribution parcels to compute parcel reconstruction z-scores.

### 4.3 Land-Use Classifier
- **File**: `backend/models/classifier.py`
- **Training Script**: `backend/train_classifier.py`
- **Checkpoint**: `outputs/transformer/model.pth` ($11{,}187{,}285$ parameters)
- **Architecture**: ResNet18 fine-tuned on UCMerced with replacement classification head:
  - Input: $224 \times 224 \times 3$, normalized using ImageNet statistics.
  - Backbone: ResNet18 ($512$ feature channels after adaptive pooling).
  - Fully Connected: $\text{Linear}(512 \to 21)$.
- **Loss Function**:
  $$\mathcal{L}_{\text{CE}} = -\sum_{c=1}^{21} y_c \log \left(\frac{\exp(z_c)}{\sum_{j=1}^{21} \exp(z_j)}\right)$$
- **Empirical Results**:
  - Held-out Test Split Accuracy: $77.46\%$ on 315 stratified test images ($244/315$ correct).
  - Validation Accuracy: $98.1\%$ during training checkpoint selection.

### 4.4 Conditional DCGAN
- **File**: `backend/models/gan.py`
- **Training Script**: `backend/train_gan.py`
- **Checkpoints**: `outputs/gan/generator_ema.pth` ($8{,}821{,}728$ params), `outputs/gan/discriminator.pth` ($6{,}971{,}926$ params).
- **Architecture**:
  - Generator: Noise $z \in \mathbb{R}^{128}$ concatenated with class embedding $e(y) \in \mathbb{R}^{64} \to$ projected to $8 \times 8 \times 512$, followed by four residual upsampling blocks ($\text{ResUpBlock}$) with nearest-neighbor interpolation and $3 \times 3$ convolutions with BatchNorm and ReLU.
  - Discriminator: Input $128 \times 128 \times 3 \to$ 4 downsampling stages with spectral normalization and LeakyReLU ($0.2$) $\to$ Projection conditioning head ($y^T V \phi(x)$) plus auxiliary classification head (AC-GAN).
- **Loss Function**:
  $$\mathcal{L}_D = -\mathbb{E}_{(x, y)} [\min(0, -1 + D(x, y))] - \mathbb{E}_{(z, y)} [\min(0, -1 - D(G(z, y), y))] + \lambda_{\text{AC}} \mathcal{L}_{\text{AC}}$$
  $$\mathcal{L}_G = -\mathbb{E}_{(z, y)} [D(G(z, y), y)] + \lambda_{\text{AC}} \mathcal{L}_{\text{AC}} + \lambda_{\text{feat}} \mathcal{L}_{\text{feat}}$$
- **Empirical Results**:
  - 120 training epochs with exponential moving average (EMA) generator weights.
  - Stable training loss dynamics ($D_{\text{loss}} \approx 1.16$, $G_{\text{loss}} \approx 1.25$).

### 4.5 Urban Scenario Diffusion
- **File**: `backend/models/diffusion.py`
- **Training Script**: `backend/train_diffusion.py`
- **Checkpoints**: `outputs/diffusion_scenario/model.pth`, `model_best.pth` ($2{,}798{,}531$ params).
- **Architecture**:
  - U-Net with base channel dimension $32$.
  - Spatial Condition: $3$ channels from source tile concatenated with $3$ noisy image channels ($6$ input channels).
  - Conditioning: Timestep sinusoidal embedding ($128$ dimensions) + Class embedding ($21$ classes) injected into every residual block.
  - Downsampling: $128 \to 64 \to 32 \to 16$ with GroupNorm ($8$ groups) and SiLU activations.
  - Upsampling: $16 \to 32 \to 64 \to 128$ with transposed convolutions and skip concatenations.
- **Sampling**:
  - DDIM deterministic/low-variance sampling with variance clamping:
    $$\sigma_t = \eta \sqrt{\frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t}} \sqrt{1 - \frac{\bar{\alpha}_t}{\bar{\alpha}_{t-1}}}$$
    $$\text{direction\_variance} = \max\left(0, 1 - \bar{\alpha}_{t-1} - \eta^2\right)$$
  - Clamping guarantees no NaN generation for any $\eta \in [0.0, 1.0]$.
- **Measured Metrics**:
  - Initial noise-prediction MSE: $0.36231$.
  - Final noise-prediction MSE: $0.00421$.
  - Best epoch noise-prediction MSE: $0.00384$.
  - Training wall time: $16.63\text{ minutes}$ ($50$ epochs).
  - Hardware Telemetry: Average GPU power $28.51\text{ W}$, peak GPU power $61.37\text{ W}$, estimated GPU-board energy $7.90\text{ Wh}$ ($476$ samples).

### 4.6 MiniGPT Urban Plan Generator
- **File**: `backend/models/gpt.py`
- **Training Script**: `backend/train_gpt.py`
- **Checkpoint**: `outputs/gpt/model.pth` ($3{,}225{,}088$ params), `outputs/gpt/meta.json`.
- **Architecture**: Character-level decoder-only causal Transformer.
  - Vocabulary Size: $64$ tokens.
  - Context Window: $192$ characters.
  - Embedding Dimension ($d_{\text{model}}$): $256$.
  - Attention Heads: $4$ ($64$ dimensions per head).
  - Layers: $4$ Transformer blocks with pre-layer normalization and causal lower-triangular masking.
- **Loss Function**:
  $$\mathcal{L}_{\text{LM}} = -\frac{1}{T} \sum_{t=1}^T \log P(x_t \mid x_{<t})$$
- **Empirical Results**:
  - Training Steps: $3{,}000$ steps on urban planning policy corpus.
  - Initial Loss: $4.238 \to$ Final Training Loss: $0.0870$.
  - Held-out Validation Loss: $0.0836$.
  - Held-out Perplexity: $1.087$.
  - Bits-Per-Character (BPC): $0.1206$.

---

## 5. API Reference & Contract Table

All guarded routes accept the `X-API-Key` header (default key configured in backend or `.env`).

| Route | Method | Purpose | Input / Parameters | Response Contract |
|---|---|---|---|---|
| `/status` | `GET` | System checkpoint readiness | None | `{"models": {...}, "overall": str}` |
| `/history/{model_name}` | `GET` | Persisted training history | `ae`, `vae`, `transformer`, `gan`, `diffusion`, `gpt` | Array of step/epoch metric dicts |
| `/evaluate/summary` | `GET` | Aggregated model metrics | None | Keyed summary of all validated metrics |
| `/evaluate/ae` | `GET` | Autoencoder evaluation metrics | None | `{status, psnr, mse, ssim}` |
| `/evaluate/vae` | `GET` | VAE evaluation metrics | None | `{status, psnr, mse, ssim, kl}` |
| `/evaluate/classifier` | `GET` | Classifier evaluation metrics | None | `{status, accuracy, val_loss}` |
| `/evaluate/gan` | `GET` | GAN evaluation metrics | None | `{status, epochs, generator_params}` |
| `/evaluate/diffusion` | `GET` | Scenario diffusion metrics | None | `{status, final_loss, best_loss, parameters_millions}` |
| `/evaluate/gpt` | `GET` | MiniGPT evaluation metrics | None | `{status, val_loss, perplexity}` |
| `/infer/ae` | `POST` | Denoising AE reconstruction | `file` (UploadFile) | `{"reconstructed": b64, "mse": float, "psnr": float, "ssim": float}` |
| `/infer/vae` | `POST` | Spatial VAE reconstruction & anomaly score | `file` (UploadFile) | `{"reconstructed": b64, "anomaly_score": float, "z_score": float, "is_anomaly": bool}` |
| `/infer/vae/interpolate` | `POST` | Latent space interpolation | `file` (UploadFile), `steps` (int) | `{"frames": [b64, ...]}` |
| `/infer/vae/urbanize` | `POST` | Style-guided urbanization projection | `file` (UploadFile), `intensity` (float) | `{"urbanized": b64}` |
| `/generate/vae/random` | `POST` | Latent prior random generation | `temperature` (float) | `{"generated": b64}` |
| `/infer/classifier` | `POST` | Aerial land-use classification | `file` (UploadFile) | `{"predictions": [{"class": str, "confidence": float}, ...]}` |
| `/infer/transformer` | `POST` | Backward-compatible alias for `/infer/classifier` | `file` (UploadFile) | `{"predictions": [...]}` |
| `/infer/gan` | `POST` | Class-conditional GAN generation | `class_index` (int), `seed` (int) | `{"image": b64, "class": str}` |
| `/infer/diffusion` | `POST` | Source-conditioned scenario diffusion | `file` (UploadFile), `class_name` (str), `steps` (int), `eta` (float) | `{"image": b64, "class": str, "steps": int, "eta": float}` |
| `/generate/plan` | `POST` | MiniGPT urban policy synthesis | `prompt` (str), `file` (optional text prompt) | `{"recommendation": str, "source": "MiniGPT"}` |
| `/system` | `GET` | Hardware & memory diagnostics | None | `{os, python, pytorch, cuda, vram}` |
| `/datasets` | `GET` | Dataset folder audit | None | `{ucmerced: {path, exists, classes, images}}` |

---

## 6. Frontend Navigation & Page Mapping

The frontend is a theme-aware single-page application with deep-link hash routing:

| Navigation Item | View ID | Primary Component | Backend Dependency |
|---|---|---|---|
| Overview | `landing` | `Landing.tsx` | Static overview & workflow animations |
| Model Explorer | `model-explorer` | `ModelExplorer.tsx` | Links to individual architecture views |
| Model Comparison | `model-comparison` | `ModelComparison.tsx` | Cross-model trade-off matrix |
| Autoencoder | `ae` | `App.tsx` + `AEArchitecture.tsx` | `/infer/ae`, `/history/ae` |
| Spatial VAE | `vae` | `App.tsx` + `VAEArchitecture.tsx` | `/infer/vae`, `/infer/vae/interpolate`, `/generate/vae/random` |
| Diffusion Generator | `diffusion` | `Diffusion.tsx` + `DiffusionArchitecture.tsx` | `/infer/diffusion`, `/evaluate/diffusion` |
| Urban Plan Generator | `plan-generator` | `App.tsx` | `/generate/plan`, `/generate/plan/presets` |
| Land-Use Classifier | `classifier` | `App.tsx` + `ClassifierArchitecture.tsx` | `/infer/classifier`, `/infer/transformer` |
| GAN Generator | `gan` | `App.tsx` + `GANArchitecture.tsx` | `/infer/gan`, `/infer/gan/classes` |
| Training | `training` | `Training.tsx` | `/history/{model_name}` |
| Evaluation | `evaluation` | `Evaluation.tsx` | `/evaluate/summary`, `/evaluate/{model}` |
| Research & Innovation | `research` | `pages/research/*` | Literature survey & planner decision support |
| System Architecture | `system-architecture` | `SystemArchitecture.tsx` | Full-pipeline dataflow diagrams |
| Dataset Explorer | `datasets` | `Datasets.tsx` | `/datasets` |
| System Info | `system` | `SystemInfo.tsx` | `/system`, `/status` |

*Note: The unbacked "Prediction Engine" navigation item has been completely removed in accordance with project governance rules.*

---

## 7. Conference Paper Figure Mapping

All nine figures referenced in `docs/IEEE_Conference_Paper.tex` are persisted in `docs/figures/` and verified:

| Figure Tag | File Path | Content | Source |
|---|---|---|---|
| `fig:ae_convergence` | `docs/figures/fig_ae_convergence.png` | Reconstruction loss curve over 50 epochs | `outputs/ae/history.json` |
| `fig:psnr_comparison` | `docs/figures/fig_psnr_comparison.png` | PSNR comparison across homogeneous vs complex parcel classes | Controlled UCMerced test split evaluation |
| `fig:ae_restoration` | `docs/figures/fig_ae_crisp_restoration.png` | Denoised visual reconstruction comparison | Autoencoder test run |
| `fig:classifier_metrics` | `docs/figures/fig_classifier_metrics.png` | Accuracy and loss curves across fine-tuning epochs | `outputs/transformer/history.json` |
| `fig:vae_tradeoff` | `docs/figures/fig_vae_tradeoff.png` | $\beta$-VAE trade-off between reconstruction MSE and KL divergence | `outputs/vae/history.json` |
| `fig:vae_multi_interpolation` | `docs/figures/fig_vae_multi_interpolation.png` | Manifold traversals between pairs of real aerial parcels | `backend/models/vae.py` manifold sampling |
| `fig:gan_dynamics` | `docs/figures/fig_gan_dynamics.png` | Generator and Discriminator loss dynamics over 120 epochs | `outputs/gan/history.json` |
| `fig:gan_samples` | `docs/figures/fig_gan_diverse_generation.png` | Class-conditional generated aerial tiles | `outputs/gan/generator_ema.pth` |
| `fig:diffusion_training` | `docs/figures/fig_diffusion_training.png` | Measured noise-prediction MSE, elapsed wall time, and GPU power | `outputs/diffusion_scenario/telemetry.json` |

---

## 8. Common Failure Modes & Troubleshooting

1. **TIFF Uploads in Web Browsers**:
   - Web browsers cannot natively render TIFF format images.
   - Solution: The UI detects TIFF extensions and renders an informational file badge rather than attempting native preview; the backend PIL pipeline handles TIFF decoding natively and returns standard PNG/JPEG base64 data.
2. **DDIM Sampler Stochasticity ($\eta > 0$)**:
   - At the final reverse step where $\bar{\alpha}_{\text{prev}} = 1.0$, unclamped variance formulas evaluate $(1 - \bar{\alpha}_{\text{prev}} - \eta^2) < 0$, emitting `NaN`s that produce black images.
   - Solution: Handled by `direction_variance = torch.clamp(1.0 - alpha_bar_prev - eta**2, min=0.0)` in `backend/models/diffusion.py`.
3. **VAE Skip Channel Dimension Mismatch**:
   - The trained VAE checkpoint was trained with `skip_channels=64, skip0_channels=16`. Instantiating with default parameters will cause a state dictionary shape mismatch on `skip2.weight`.
   - Solution: Always instantiate with `VAE(latent_channels=64, skip_channels=64, skip0_channels=16)`.
4. **Git LFS Pointers**:
   - If large model files are cloned without Git LFS, PyTorch will fail with an invalid header error.
   - Solution: Run `git lfs pull` to replace pointer files with binary model weights.
5. **No Temporal Prediction Claims**:
   - The system performs single-frame land-use analysis, structural reconstruction, and source-conditioned diffusion simulation. It does not perform future land-use prediction because the UCMerced dataset does not contain paired longitudinal before/after imagery.

---

## 9. Verification Protocol Command

To execute the automated end-to-end verification protocol:
```powershell
python scripts/validate_system.py
```
This produces `outputs/system_validation_report.json` and logs status across all 6 models.
