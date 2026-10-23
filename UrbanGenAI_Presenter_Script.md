# UrbanGenAI — Presenter Script

Read this while presenting. Plain spoken sentences, first person.
Match by **slide title** if your manual slide order differs.
Target: ~5 minutes talking. Lines marked *(skip if short on time)* are optional.

---

## Slide 1 — Title

"Good morning. Our project is **UrbanGenAI** — a multi-model generative AI system
that helps urban planners make decisions. Our case study is Pune, the PMC area,
about 516 square kilometres and 7.4 million people. It uses four generative
models on one pipeline."

---

## Slide 2 — Problem Statement

"City planning needs many things weighed at once — housing, traffic, flooding,
green cover, heat. The tools for this are split apart. The data sits in different
software. Normal GIS gives one fixed map, so planners can't compare options.
AI chat tools give ideas but aren't connected to real ground data, so they can
be wrong about a place. There is no single workspace that goes from raw data to
options to a written recommendation."

---

## Slide 3 — Objectives

"So our objective was to build one connected pipeline where each model does a
clear job. The classifier labels the land use. The autoencoder cleans the
imagery. The variational autoencoder flags unusual parcels. The GAN creates
extra training data. And a from-scratch transformer drafts the recommendation.
And — important for marking — every model is trained by us, checkpoints
committed, with live measured metrics. Nothing is downloaded or faked."

---

## Slide 4 — Expected Outcome

"The outcome is a working web app a planner can actually use. One dashboard,
one page per model with its architecture and instructions, and a live
evaluation page. Four trained models with committed weights. Honest evaluation —
real numbers plus a clear list of limitations. And it's reproducible: full
retrain is about one hour on a laptop GPU."

---

## Slide 5 & 6 — Literature Review  *(go fast — about 20 seconds total)*

"We reviewed 15 IEEE journal and magazine papers — no conference papers.
They fall into four groups: deep learning for remote-sensing classification,
which shaped our ResNet encoder choice; GAN surveys, which gave us spectral
normalisation and label smoothing; multimodal remote sensing, which supports
our multi-source data idea; and vision-transformer surveys, background for our
MiniGPT. Full list with how we use each is on the slides."

---

## Slide 7 — System Architecture (layered)

"This is the whole system as five layers. On top, the **React frontend**.
Below it, the **FastAPI backend** with security middleware — API-key check,
rate limiting, and it validates every upload. Then the **five model services**,
each holding its checkpoint in memory. Below that, an **evaluation layer** that
computes every metric once at startup and caches it. And at the bottom, the
**data and checkpoints** — the datasets, the Pune GIS, and the committed
`.pth` files, which are our single source of truth."

---

## Slide 8 — System Components  *(read 2-3 rows, not all)*

"Each component and its technology is listed here. Key point: the frontend is
React and TypeScript; the backend is FastAPI; all five models are PyTorch.
One ethical safeguard built in — uploads are processed in memory and never
written to disk, and we only use public data and open GIS."

---

## Slide 9 — Request Flow

"A request flows like this. Step zero, at startup, every checkpoint loads and
every metric is computed. Then: the browser sends a tile; security middleware
checks it; the router picks the right model; the model runs one forward pass;
we post-process — an anomaly score, or PSNR, or decoded text; and the result
goes back as JSON or an image."

---

## Slide 10 — Architecture Detail (layers, epochs, dimensions)

"This table has the exact numbers for each model. Quick highlights:
The **autoencoder** — ResNet18 encoder down to an 8-by-8-by-256 bottleneck,
then a U-Net skip decoder back to full size, 50 epochs, MSE loss on the clean
tile.
The **VAE** — same encoder, but two 1-by-1 convolutions produce mu and log-
variance, each 8-by-8-by-64, that's 4,096 latent dimensions. Loss is L1 plus
MSE plus a tiny beta times KL divergence.
The **GAN** — noise 128 plus a class embedding 64, five transposed
convolutions to a 128-pixel tile, 100 epochs, adversarial loss with label
smoothing and an EMA generator.
The **MiniGPT** — four transformer blocks, four attention heads, context of
192 characters, 3.2 million parameters, trained 3,000 steps on next-character
cross-entropy."

---

## Slide 11 — Implementation Result: modules, losses & evaluation matrix

"Here are the verified results, one row per module.
The **classifier** — 98.1 percent validation accuracy.
The **autoencoder** — PSNR 29.7 decibels, SSIM 0.87. That's near-lossless
denoising; training MSE fell from 0.18 to 0.02.
The **VAE** — SSIM 0.43, deliberately softer, because an 8-by-8 bottleneck
limits detail. But 63 of 64 latent dimensions are active, so the latent is
healthy.
The **GAN** — about 15 percent classifier-recognition rate.
The **MiniGPT** — perplexity 1.09, which means it predicts the next character
very confidently.
All of these are read live from the checkpoints, served at slash-evaluate."

---

## Slide 12 — Model Comparison

"Which model is best? There is no single best — it's a pipeline. But ranked by
contribution to the goal: **first, the VAE** — its anomaly score is what makes
this decision-support and not just a viewer. **Second, MiniGPT** — it produces
the recommendation a planner reads. **Third, the AE and GAN** — enabling steps.
The classifier is the most accurate model but it's a supporting CNN, not
generative. And on the one fair head-to-head — AE versus VAE, same task — the
AE wins on image fidelity, the VAE wins on being useful for planning."

---

## Slide 13 — Evaluation Parameters  *(skip if short on time)*

"This slide just explains each metric — PSNR and SSIM measure image closeness,
KL divergence measures how far the latent is from a normal prior, perplexity
measures language confidence. Each model is judged by the metric that fits it,
not one metric forced on all."

---

## Slide 14 — Output

"And this is what the planner sees for each model. The classifier gives a zone
label with confidence. The autoencoder shows original, noisy, and cleaned
side by side. The VAE shows a banner — Typical, Unusual, or Highly Anomalous —
with a percentage and a plain reason. The GAN shows a grid of generated tiles.
And MiniGPT writes a short recommendation — setbacks, permeable surface, flood
buffer, parking cap — built from that ward's real statistics."

---

## Slide 15 — Conclusion

"To conclude. UrbanGenAI shows four generative models working together on one
planning task, end to end, from an aerial tile to a written recommendation.
It's honest — every number is measured, and we state our limitations with
evidence: the GAN geometry is immature, the VAE is soft by design. Three of the
four models — the VAE decoder, the GAN, and MiniGPT — are trained fully from
scratch. And it's responsible: only public data, the planner stays in the loop,
and outputs are candidates that still need statutory and engineering checks.
Next steps are on the Future Scope page. Thank you — happy to take questions."

---

# Likely questions — quick answers

**Q: Explain the VAE loss / the maths.**
"Reconstruction term is 0.7 times L1 plus 0.3 times MSE between the output and
the input. Regularisation term is beta times the KL divergence between the
learned posterior q(z given x) and a standard normal N(0, I). We use the
reparameterization trick — z equals mu plus sigma times epsilon, epsilon from
N(0,1) — so gradients can flow through the sampling step. Beta is about 1e-4;
we measured that beta above 0.02 causes posterior collapse on our data."

**Q: Why is the GAN only 15%?**
"At 100 epochs on 21 classes with 100 images each, texture-heavy classes like
beach and forest come through, but classes needing exact repeated geometry —
road grids, intersections — need far more epochs or data. It's the expected
behaviour at this scale. We report it instead of only showing good samples."

**Q: Is the classifier your transformer?**
"No. The classifier is a CNN — ResNet18. The transformer requirement is met
separately by MiniGPT, which we built from scratch. We label it honestly."

**Q: Ethics / fairness / privacy.**
"Privacy — only public aerial imagery and open GIS, no personal data, GDPR
aligned. Fairness — we show per-class metrics, we don't hide weak classes
behind an average. Transparency — every page shows the architecture, whether
the model is pretrained or ours, and links the checkpoint. Limitation — outputs
are computational candidates, not statutory plans; they need validation against
Pune DCPR rules, engineering models, and public hearings."

**Q: Where are the models stored?**
"PyTorch `.pth` state-dict files under `outputs/<model>/model.pth`, all
committed to the repo, loaded once at backend startup. GAN uses the EMA
generator; MiniGPT also has a `meta.json` with the character vocabulary."

**Q: What did you improve over prior work?**
"AE — we measured a plain bottleneck underperforming on complex classes (7 dB
gap) and fixed it with U-Net skip connections, closing the gap to 2.6 dB.
VAE — we used a spatial latent instead of one flat vector, and tuned beta
against our own data instead of the textbook default. GAN — spectral norm,
label smoothing, and an EMA generator for stability on a small dataset."
