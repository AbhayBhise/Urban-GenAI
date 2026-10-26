# Contributing to UrbanGen AI 🏙️

Welcome to **UrbanGen AI**! We welcome academic and open-source contributions to our edge-deployable multi-model urban spatial analytics platform. This guide explains how to set up your development environment, run the multi-model pipeline, and contribute effectively.

---

## 🚀 Quick Setup

### Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+ (with npm)
- **Git & Git LFS**: Required for repository cloning and checkpoint management
- **GPU (Recommended)**: NVIDIA CUDA GPU (e.g. RTX 3050/4050+) for model training and high-throughput inference; CPU execution supported for testing.

### 1. Clone & Branch
```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git lfs install
git lfs pull
git checkout -b feature/your-feature-name
```

### 2. Backend Environment
```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt

# Linux / macOS
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Frontend Environment
```bash
cd frontend
npm install
npm run dev       # Starts local development server at http://localhost:5173
```

### 4. Start the FastAPI REST Backend
```bash
cd backend
python api.py     # Listens at http://127.0.0.1:8000 (OpenAPI docs at /docs)
```

---

## 🤖 The 6 Core Model Architectures

All six models are fully implemented, trained, and benchmarked under our uniform 50-epoch protocol:

| Pipeline Route | Model Family | Script | Primary Checkpoint |
|:---|:---|:---|:---|
| `/infer/ae` | U-Net Denoising Autoencoder | `backend/train_ae.py` | `outputs/ae/best_checkpoint.pth` |
| `/infer/vae` | Spatial $\beta$-VAE | `backend/train_vae.py` | `outputs/vae/best_checkpoint.pth` |
| `/infer/transformer` | ResNet-18 Land Classifier | `backend/train_transformer.py` | `outputs/transformer/best_checkpoint.pth` |
| `/infer/gan` | Residual Class-Conditional DCGAN | `backend/train_gan.py` | `outputs/gan/generator_ema.pth` |
| `/infer/diffusion` | Conditional DDPM (DDIM sampler) | `backend/train_diffusion.py` | `outputs/diffusion_scenario/best_checkpoint.pth` |
| `/generate/plan` | MiniGPT Planning Transformer | `backend/train_gpt.py` | `outputs/gpt/best_checkpoint.pth` |

---

## 🔬 Dataset Structure (UCMerced LandUse)

To re-train or benchmark models:
1. Download `UCMerced_LandUse.zip` (21 classes $\times$ 100 tiles, $256 \times 256$ RGB).
2. Extract into the repository root:
```text
UrbanGenAI/
└── UCMerced_LandUse/
    └── UCMerced_LandUse/
        └── Images/
            ├── agricultural/
            ├── airplane/
            ├── buildings/
            ├── denseresidential/
            ├── freeway/
            ├── harbor/
            └── ... (21 classes total)
```

---

## 📁 Repository Directory Structure

```text
UrbanGenAI/
├── backend/                  # FastAPI service, models, and training routines
├── frontend/                 # React / Vite / Tailwind web dashboard
├── docs/                     # IEEE paper source, figures, and governance docs
├── paper_package/            # Overleaf-ready submission archive and asset manifest
├── outputs/                  # Trained checkpoints, histories, and evaluation logs
├── scripts/                  # Packaging, slide building, and organization tools
├── archive/                  # Archived presentations, logs, and scratch assets
├── demo_prompts/             # Municipal prompt templates
├── HOW_TO_RUN.md             # Local startup instructions
└── README.md                 # Primary project overview
```

---

## 🧪 Testing & Verification

Before submitting pull requests, run:

```bash
# Verify backend syntax
cd backend
python -m py_compile api.py dataset.py evaluate.py

# Verify frontend production build
cd ../frontend
npm run build

# Package research paper and verify asset sync
cd ..
python scripts/package_paper.py
```

---

## 📝 Commit Conventions

We follow Conventional Commits:
- `feat:` New features or pipeline modules
- `fix:` Bug fixes or metric adjustments
- `docs:` Documentation or paper updates
- `refactor:` Code improvements without behavioral changes
- `chore:` Repository maintenance, dependency updates
