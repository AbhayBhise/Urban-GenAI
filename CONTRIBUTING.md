# Contributing to Urban-GenAI 🏙️

Welcome! Urban-GenAI is an open-source AI-assisted urban planning platform. This guide helps you set up the project and contribute effectively.

---

## 🚀 Quick Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone & Branch
```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git checkout -b feature/your-feature-name
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev       # starts at http://localhost:5173
```

### 4. Start the API
```bash
cd backend
uvicorn api:app --reload --port 8000
```

---

## 🤖 Training the GAN (HIGH PRIORITY for teammates)

> **⚠️ The GAN (Phase 11) has been implemented but NOT yet trained.**
> **A teammate with a GPU machine should run this ASAP.**

### Step 1 — Download UCMerced Dataset (~340 MB)
```
http://weegee.vision.ucmerced.edu/datasets/UCMerced_LandUse.zip
```
Extract it so the path looks like:
```
Urban-GenAI/
└── UCMerced_LandUse/
    └── UCMerced_LandUse/
        └── Images/
            ├── agricultural/   ← 100 .tif files each
            ├── airplane/
            ├── buildings/
            └── ...            (21 class folders total)
```

### Step 2 — Train the GAN
```bash
cd backend

# GPU machine (recommended) — ~20-30 min
python train_gan.py --epochs 100 --batch-size 32

# CPU only — ~2-3 hours
python train_gan.py --epochs 100 --batch-size 8
```

**CLI Options:**
| Flag | Default | Description |
|------|---------|-------------|
| `--epochs` | 100 | Total training epochs |
| `--batch-size` | 32 | Batch size (reduce to 8 on CPU) |
| `--lr` | 2e-4 | Learning rate |
| `--d-steps` | 2 | Discriminator updates per G step |
| `--save-every` | 10 | Save sample grid every N epochs |
| `--resume` | off | Resume from existing checkpoint |

### Step 3 — Commit the trained weights
```bash
# After training completes, commit the weights
git add outputs/gan/generator_ema.pth outputs/gan/meta.json outputs/gan/history.json
git commit -m "feat: add trained GAN weights (100 epochs)"
git push origin feature/gan-training
```

### What gets saved
| File | Description |
|------|-------------|
| `outputs/gan/generator_ema.pth` | **EMA Generator** — used by `/infer/gan` API |
| `outputs/gan/generator.pth` | Raw Generator checkpoint |
| `outputs/gan/discriminator.pth` | Discriminator checkpoint |
| `outputs/gan/history.json` | Per-epoch D-loss & G-loss |
| `outputs/gan/meta.json` | Hyperparameter record |
| `outputs/gan/samples/epoch_XXXX.png` | Visual sample grids |

---

## 📁 Project Structure

```
Urban-GenAI/
├── backend/
│   ├── api.py                  ← FastAPI routes
│   ├── models/
│   │   ├── autoencoder.py      ← DenoisingAE
│   │   ├── vae.py              ← VAE
│   │   ├── classifier.py       ← ResNet18 classifier
│   │   ├── gpt.py              ← MiniGPT
│   │   └── gan.py              ← ✅ NEW: Conditional DCGAN
│   ├── train_ae.py
│   ├── train_vae.py
│   ├── train_transformer.py
│   ├── train_gpt.py
│   └── train_gan.py            ← ✅ NEW: GAN training script
├── frontend/
│   └── src/
│       ├── App.tsx
│       └── pages/
│           ├── GAN.tsx         ← ✅ NEW: GAN generation UI
│           └── ...
└── outputs/                    ← Trained model weights
    ├── ae/
    ├── vae/
    ├── gpt/
    ├── transformer/
    └── gan/                    ← ✅ NEW: GAN outputs dir
```

---

## 🔌 New API Endpoints (GAN)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/infer/gan` | Generate tiles for a class |
| `GET` | `/infer/gan/classes` | List all 21 UCMerced classes |
| `GET` | `/infer/gan/grid` | Generate one tile per class (21-image grid) |

**Example request:**
```bash
curl -X POST http://localhost:8000/infer/gan \
  -H "Content-Type: application/json" \
  -d '{"class_index": 4, "num_images": 4}'
```

---

## 🌿 Branch Naming Convention

```
feature/   → new feature       e.g. feature/multi-city-support
fix/       → bug fix           e.g. fix/vae-anomaly-baseline
docs/      → documentation     e.g. docs/update-readme
train/     → model weights     e.g. train/gan-weights-100ep
```

---

## 📋 Open Tasks (Good First Issues)

| Task | Difficulty | Notes |
|------|------------|-------|
| **Train GAN on GPU** | 🟡 Medium | Run `train_gan.py`, commit weights |
| Multi-city RAG support | 🟡 Medium | Extend `rag_pipeline.py` beyond Pune |
| Evaluation page | 🟡 Medium | `pages/Evaluation.tsx` is a stub |
| Docker setup | 🟡 Medium | `Dockerfile` + `docker-compose.yml` |
| Unit tests | 🟢 Easy | `pytest` is in requirements, no `tests/` folder yet |
| Map integration (Leaflet) | 🔴 Hard | Add interactive map to PlanGenerator |

---

## 🤝 Pull Request Process

1. Fork / create a branch from `main`
2. Make your changes
3. Test locally (backend + frontend)
4. `git push origin your-branch`
5. Open a PR on GitHub with a clear description

---

## 📬 Questions?

Open a GitHub Issue or reach out to the maintainer [@AbhayBhise](https://github.com/AbhayBhise).
