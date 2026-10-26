# UrbanGen AI — Local Startup Guide

This guide starts the local, checkpoint-backed demonstration system. It uses the pre-trained checkpoints in `outputs/` and does not require re-training.

---

## 1. Prerequisites
- **Python**: 3.10 or newer
- **Node.js**: v18.0 or newer (with npm)
- **Git & Git LFS**: Required for repository and checkpoint retrieval
- **GPU**: NVIDIA CUDA GPU (e.g. RTX 3050/4050+) recommended for faster inference; CPU execution is supported.

---

## 2. Clone Repository & Download Checkpoints

```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git lfs install
git lfs pull
```

---

## 3. Backend Setup

Create and activate a Python virtual environment:

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Start the FastAPI service:
```bash
cd backend
python api.py
```

The API starts on `http://127.0.0.1:8000`. You can inspect the interactive OpenAPI Swagger docs at `http://127.0.0.1:8000/docs`.

---

## 4. Frontend Setup

In a second terminal window:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173`.

By default, the frontend connects to `http://127.0.0.1:8000`. If running on a remote host, configure `frontend/.env.local`:
```text
VITE_API_URL=http://<your-host-ip>:8000
```

---

## 5. Optional: Dataset Setup & Training

The UCMerced LandUse dataset (21 classes $\times$ 100 images) is not committed to GitHub. To run dataset-dependent explorer pages or re-train models from scratch:

1. Download `UCMerced_LandUse.zip` and extract to:
   ```text
   UCMerced_LandUse/UCMerced_LandUse/Images/<class>/*.tif
   ```
2. Run any model training script:
   ```bash
   cd backend
   python train_ae.py          # U-Net Denoising Autoencoder
   python train_vae.py         # Spatial Beta-VAE
   python train_transformer.py # ResNet-18 Land-Use Classifier
   python train_gan.py         # Residual Class-Conditional DCGAN
   python train_diffusion.py   # Conditional DDPM (DDIM sampler)
   python train_gpt.py         # MiniGPT Planning Transformer
   ```
3. Evaluate model checkpoints:
   ```bash
   python evaluate.py
   ```

---

## 6. Research Paper & Overleaf Archive

The full IEEE conference paper and assets are in:
- TeX Source: [`docs/IEEE_Conference_Paper.tex`](docs/IEEE_Conference_Paper.tex)
- 1-Click Overleaf Zip: [`paper_package/UrbanGenAI_Paper_Overleaf.zip`](paper_package/UrbanGenAI_Paper_Overleaf.zip)
