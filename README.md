# UrbanGen AI

UrbanGen AI is a local, research-oriented web application for experimenting with generative and predictive models on aerial urban image tiles. The repository contains a React/Vite interface, a FastAPI service, trained checkpoints, evaluation records, architecture views, and the accompanying conference-paper sources.

The project is an assistive research prototype. Its generated images are not planning forecasts, zoning decisions, or validated municipal interventions.

## What is implemented

The current repository contains these runnable components:

- React/Vite frontend in `frontend/` with model pages, evaluation views, architecture views, training records, governance pages, and a diffusion generator page.
- FastAPI backend in `backend/api.py` with model status, history, evaluation, image upload, inference, governance, and planning endpoints.
- Denoising autoencoder checkpoint in `outputs/ae/`.
- Spatial VAE checkpoint in `outputs/vae/`.
- ResNet-based land-use classifier checkpoint in `outputs/transformer/`.
- Class-conditional GAN checkpoints in `outputs/gan/`.
- MiniGPT checkpoint and metadata in `outputs/gpt/`.
- Image-conditioned diffusion U-Net/DDPM checkpoint with DDIM sampling in `outputs/diffusion_scenario/`.
- IEEE paper sources and figures in `docs/IEEE_Conference_Paper.tex`, `docs/IEEE_Conference_Paper.md`, and `docs/figures/`.

The checkpoints are stored with Git LFS. The training scripts are included for reproducibility, but training is not required for the normal checkpoint-backed demo.

## Important limitations

The repository does not claim capabilities that are not supported by the available data.

- The available aerial dataset is an image-classification dataset, not a paired before/after urban-intervention dataset.
- The current diffusion training objective uses the source tile as an image condition and therefore supports source-conditioned denoising/reconstruction. It must not be described as a validated conversion from one land-use class into another.
- Training loss is not the same as image-generation quality. Consult the recorded histories, evaluation endpoints, model card, and paper for the metric protocol and limitations.
- Dataset-dependent explorer, sampling, evaluation, and training paths require the dataset to be supplied locally. The dataset is intentionally not committed to this repository.
- Outputs are visual research artifacts and require independent validation before any real planning use.

## Repository layout

```text
UrbanGenAI/
├── backend/                 FastAPI service, models, datasets, and training scripts
├── frontend/                React/Vite web interface
├── outputs/                 Checkpoints, histories, telemetry, and measured artifacts
├── docs/                    Paper, model card, governance documents, and figures
├── demo_prompts/            Prompts used by the planning demonstration
├── scripts/                 Project utility scripts
├── HOW_TO_RUN.md            Short local startup guide
└── LICENSE                  Proprietary All Rights Reserved license
```

## Requirements

- Python 3.10 or newer
- Node.js and npm
- Git LFS for checkpoint download
- A CUDA-capable GPU is recommended for training and faster inference, but the API can be started on CPU with lower performance.

## Installation and local demo

Clone the repository and download the model checkpoints:

```bash
git clone https://github.com/AbhayBhise/Urban-GenAI.git
cd Urban-GenAI
git lfs install
git lfs pull
```

Create a Python environment and install backend dependencies:

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

Start the API from the backend directory:

```bash
cd backend
python api.py
```

In another terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

By default the frontend calls `http://127.0.0.1:8000`. To use another API host, create `frontend/.env.local` before building or starting Vite:

```text
VITE_API_URL=https://your-api-host.example
```

If the backend has `URBANGEN_API_KEY` configured, enter the same key in the frontend API-key field. See `backend/.env.example` and `docs/SECURITY.md` for the available controls.

## Optional dataset setup

The dataset is not part of the GitHub repository. To enable dataset-backed pages and training, obtain the permitted UCMerced LandUse files separately and place them at:

```text
UCMerced_LandUse/UCMerced_LandUse/Images/<class>/*.tif
```

The backend uses the 21 UCMerced classes defined in `backend/dataset.py`. A dataset is not required for the checkpoint-backed upload inference paths that do not select random dataset samples.

## Training

Training is optional and requires the dataset. The scripts select CUDA when available and write checkpoints and histories under `outputs/`.

```bash
cd backend
python train_diffusion.py
```

Other model training scripts are listed in `backend/`. Do not overwrite published checkpoints without recording the dataset split, configuration, metrics, runtime, device, and energy telemetry for the replacement run.

## Verification

Useful checks after setup:

```bash
# frontend
cd frontend
npm run build

# backend syntax
python -m py_compile api.py train_diffusion.py models/diffusion.py
```

With the API running, inspect `/status`, `/evaluate/summary`, and the relevant model-specific evaluation endpoints. Missing checkpoints or datasets should be reported as unavailable; they must not be replaced with fabricated metrics or placeholder outputs.

## Research documentation

- [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) — model purposes, checkpoints, metrics, and limitations.
- [`docs/IEEE_Conference_Paper.tex`](docs/IEEE_Conference_Paper.tex) — paper source with real LaTeX equations and tables.
- [`docs/IEEE_Conference_Paper.md`](docs/IEEE_Conference_Paper.md) — readable paper draft.
- `docs/figures/` — recorded plots and figures referenced by the paper.
- `docs/SECURITY.md`, `docs/PRIVACY.md`, and `docs/ETHICS.md` — governance and deployment considerations.
- [`HOW_TO_RUN.md`](HOW_TO_RUN.md) — concise startup instructions.

## License and ownership

This work is distributed under the proprietary All Rights Reserved terms in [`LICENSE`](LICENSE). The repository may be viewed, but copying, modifying, redistributing, commercializing, or presenting the work as another person's work requires prior written permission from the copyright holders.
