# UrbanGen AI — How to Run

## 1. Install backend dependencies
```
cd backend
pip install -r requirements.txt
cp .env.example .env          # optional: set URBANGEN_API_KEY etc. for a locked-down deployment
```

## 2. Train models (run in order, each takes ~5-20 min on RTX 4050)
```
cd backend
python train_ae.py
python train_vae.py                     # VAE -> outputs/vae/  (reconstruction, KL, anomaly, interpolation)
python train_transformer.py             # ResNet18 land-use classifier
python corpus/build_corpus.py           # (re)build the urban-planning corpus
python train_gpt.py                     # MiniGPT transformer -> outputs/gpt/  (plan generation)
```

## 3. Start API server
```
cd backend
python api.py
```

If `URBANGEN_API_KEY` is set in `.env`, enter the same value in the "API key"
field in the app sidebar so the frontend can call the guarded endpoints.
See `docs/SECURITY.md`, `docs/PRIVACY.md`, `docs/ETHICS.md`, `docs/MODEL_CARD.md`.

## 4. Start frontend
```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173
