# UrbanGen AI — Local startup

This guide starts the checkpoint-backed demo. It does not train models.

## 1. Clone and download checkpoints

```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git lfs install
git lfs pull
```

## 2. Install backend dependencies

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## 3. Start the API

```bash
cd backend
python api.py
```

The API listens on `http://127.0.0.1:8000` by default. Optional security and CORS settings are documented in `backend/.env.example`.

## 4. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The frontend uses `http://127.0.0.1:8000` by default. Set `VITE_API_URL` in `frontend/.env.local` when the API is hosted elsewhere.

## Dataset-dependent features

The datasets are not committed to GitHub. Dataset explorer, random-sample, evaluation, and training paths require the permitted UCMerced LandUse files at:

```text
UCMerced_LandUse/UCMerced_LandUse/Images/<class>/*.tif
```

Checkpoint-backed upload inference can run without the dataset when the selected endpoint does not require a random dataset sample.

## Optional training

Training requires the dataset and is not part of the normal startup flow. For example:

```bash
cd backend
python train_diffusion.py
```

Training writes measured checkpoints and histories under `outputs/`. Do not present a training loss as a complete image-quality evaluation.
