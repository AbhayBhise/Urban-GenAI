# UrbanGen AI — How to Run

## 1. Install backend dependencies
```
cd backend
pip install -r requirements.txt
```

## 2. Train models (run in order, each takes ~10-20 min on RTX 4050)
```
cd backend
python train_ae.py
python train_vae.py
python train_transformer.py
```

## 3. Start API server
```
cd backend
python api.py
```

## 4. Start frontend
```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173
