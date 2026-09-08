# UrbanGen AI — Model Card

One document covering every model shipped in the app. Metrics are from the
committed training runs (`outputs/*/history.json`); re-training will vary.

Common properties:
- **Framework:** PyTorch. **Hardware:** single NVIDIA RTX 4050 Laptop GPU (~75 W).
- **Intended use:** teaching / research prototype for AI-assisted, *advisory*
  urban-planning drafting.
- **Out-of-scope use:** see `docs/ETHICS.md §3` (no regulatory, rights-affecting,
  biometric, or synthetic-media-of-real-people use).
- **Shared limitation:** trained on Western datasets / an English corpus, applied
  to Pune — expect degraded reliability on local urban form (`docs/ETHICS.md §2`).

---

## 1. Denoising Autoencoder (`ae`)

| | |
|---|---|
| Architecture | Pretrained ResNet18 encoder (to layer3) + 4-stage transposed-conv decoder, 128×128 RGB |
| Training data | UCMerced LandUse (21 classes, US aerial imagery) |
| Objective | Reconstruct clean tile from Gaussian-noised input (MSE) |
| Result | train MSE ≈ 0.0198 (50 epochs); PSNR reported per-image in the UI |
| Purpose in project | Pre-clean degraded satellite/aerial imagery before downstream analysis |
| Limitations | Learns denoising for this domain only; not a super-resolution model |

## 2. Variational Autoencoder (`vae`)

| | |
|---|---|
| Architecture | ResNet18 encoder → 64×8×8 spatial latent (`mu`, `logvar`) → reparameterize `z = mu + σ·ε` → transposed-conv decoder |
| Training data | UCMerced LandUse |
| Objective | `0.7·L1 + 0.3·MSE` reconstruction + `β·KL`, **β = 1e-4** (reconstruction-priority) |
| Result | train recon ≈ 0.075, KL ≈ 103 nats (50 epochs) |
| Purpose in project | High-fidelity reconstruction; latent **interpolation** between two real encoded tiles (the latent-space demo); reconstruction-error **anomaly scoring** against a baseline over 300 real tiles |
| KL divergence | Reported per inference and plotted in the Training tab. With β ≈ 0 it is **not minimised** — it rises during training as the latent grows more informative. This is expected for a reconstruction-priority VAE. Sampling straight from the prior is therefore not meaningful on this model (a known β-VAE trade-off); interpolation between real tiles is used instead. A genuinely prior-matched checkpoint was attempted but collapsed at every workable β on this encoder/decoder within the project timeframe |
| Limitations | Latent does not match N(0,1); soft 8×8 spatial bottleneck |

## 3. Urban Plan Generator — MiniGPT (`gpt`)

| | |
|---|---|
| Architecture | Decoder-only Transformer built from scratch: char-level embedding + learned positional embedding, 4 pre-norm blocks (causal multi-head self-attention + MLP), weight-tied LM head. ~n_embd 256, 4 heads, block size 192 |
| Training data | `backend/corpus/urban_planning.txt` — hand-authored sustainable-planning corpus (zoning, green cover, transit-oriented development, stormwater, Pune context) |
| Objective | Next-character cross-entropy; temperature + top-k sampling at inference |
| Purpose in project | Given a prompt seeded from real Pune land-use statistics (`PUNE_STATS`), generate draft sustainability recommendations for planner review |
| Limitations | Small model, small corpus, char-level: fluent-sounding but **no factual grounding, no citations, can self-contradict**. Advisory drafting aid only |
| Train it | `python train_gpt.py` (~5–10 min) |

## 4. Land-Use Classifier (`transformer` route, ResNet18)

| | |
|---|---|
| Architecture | ResNet18, ImageNet-pretrained, fine-tuned; final FC → 21 classes |
| Training data | UCMerced LandUse (90/10 split) |
| Result | val accuracy ≈ 98.1%, val loss ≈ 0.10 (30 epochs) |
| Purpose in project | Automated land-use / zoning audit and land-use-change tracking at city scale |
| Note | This is a **CNN**, not a transformer. It is kept because it does useful project work; the transformer requirement is met by MiniGPT (§3). The API route name `transformer` is retained for backward compatibility |
| Limitations | 21 fixed classes from US imagery; single-label per tile |

---

## Sustainability / carbon footprint (Unit 6)

Rough estimate for a full retrain of all models on the reference RTX 4050 laptop:

| Model | Approx. train time | Approx. energy |
|---|---|---|
| AE (50 ep) | ~15 min | ~0.03 kWh |
| VAE (50 ep) | ~20 min | ~0.04 kWh |
| MiniGPT (3k steps) | ~8 min | ~0.015 kWh |
| Classifier (30 ep) | ~15 min | ~0.03 kWh |
| **Total** | **~1 h** | **~0.12 kWh** (≈ 0.08 kg CO₂e at ~0.7 kg/kWh grid intensity) |

Design choices that keep this low: pretrained backbones (transfer learning),
small from-scratch transformer, single-GPU, modest datasets. Inference is CPU-viable.
