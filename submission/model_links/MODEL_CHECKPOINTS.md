# 🤖 Trained Model Checkpoints — UrbanGen AI

All trained PyTorch checkpoints (`model.pth`) and training logs (`history.json`) are hosted in the GitHub repository via Git LFS and are also deployed live on Render.

| Model | Checkpoint Link (GitHub) | Training History | Live API Endpoint |
| :--- | :--- | :--- | :--- |
| **1. Denoising Autoencoder (AE)** | [`outputs/ae/model.pth`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/ae/model.pth) | [`outputs/ae/history.json`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/ae/history.json) | `POST https://urban-genai.onrender.com/infer/ae` |
| **2. Spatial β-VAE** | [`outputs/vae/model.pth`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/vae/model.pth) | [`outputs/vae/history.json`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/vae/history.json) | `POST https://urban-genai.onrender.com/infer/vae` |
| **3. MiniGPT Transformer** | [`outputs/gpt/model.pth`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/gpt/model.pth) | [`outputs/gpt/history.json`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/gpt/history.json) | `POST https://urban-genai.onrender.com/generate/plan` |

### Additional Files for MiniGPT
- Vocabulary & Config Metadata: [`outputs/gpt/meta.json`](https://github.com/AbhayBhise/Urban-GenAI/blob/main/outputs/gpt/meta.json)
