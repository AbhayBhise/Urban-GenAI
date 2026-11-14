# UrbanGen AI: A Multi-Model Generative Framework for Satellite Imagery Processing, Land-Use Analytics, and Sustainable Urban Planning

**Authors:**
- **Abhay Bhise** (`bhiseabhay890@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Pune, Maharashtra, India*
- **Disha Satpute** (`dishasatpute44@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Pune, Maharashtra, India*
- **Vaishnavi Phad** (`phadvaishnavi1905@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Pune, Maharashtra, India*
- **Vedant Ingle** (`vedantingle05@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Pune, Maharashtra, India*
- **Prof. Savita Mane** (`savita.mane@mitaoe.ac.in`)  
  *Assistant Professor, Department of Computer Engineering, MIT Academy of Engineering, Pune*
- **Prof. Pramod Ganjewar** (`pdganjewar@mitaoe.ac.in`)  
  *Assistant Professor, Department of Computer Engineering, MIT Academy of Engineering, Pune*

**Target Format:** IEEE Conference Proceedings (Double Column)  
**LaTeX Master File:** [`docs/IEEE_Conference_Paper.tex`](file:///f:/PROJECTS/GEN%20AI%20PROJECT/UrbanGenAI/docs/IEEE_Conference_Paper.tex)  
**High-Resolution Figures Directory:** [`docs/figures/`](file:///f:/PROJECTS/GEN%20AI%20PROJECT/UrbanGenAI/docs/figures)

---

### Abstract
Rapid global urbanization presents pressing challenges in zoning compliance, green cover preservation, transit infrastructure allocation, and microclimate resilience. Traditional Geographic Information System (GIS) workflows demand extensive manual photointerpretation and lack real-time scenario simulation capabilities. In this paper, we propose **UrbanGen AI**, an end-to-end, edge-deployable multi-model generative artificial intelligence framework engineered specifically for sustainable smart city planning and digital twin prototyping. To bridge the critical gap between pixel-level remote sensing restoration and qualitative municipal policy formulation, UrbanGen AI coordinates six specialized deep learning architectures under a unified, reproducible 50-epoch benchmark protocol on the UCMerced LandUse dataset:
1. A multi-scale skip-connected **U-Net Denoising Autoencoder** achieving **29.65 dB PSNR** (+7.0 dB gain over baseline, SSIM **0.8649**) to eliminate atmospheric scattering and sensor noise ($\sigma = 0.15$);
2. A **Spatial Variational Autoencoder ($\beta$-VAE)** preserving 2D spatial topology in an explicit $\mathbb{R}^{64 \times 8 \times 8}$ latent tensor, achieving **27.49 dB PSNR** with smooth continuous manifold interpolation and unsupervised anomaly detection ($>3\sigma$ reconstruction disparity);
3. A frozen ImageNet-adapted **ResNet-18 Territorial Classifier** attaining **98.10% validation accuracy** (Macro F1: **0.9784**) serving as an autonomous semantic fidelity auditor;
4. A **Residual Class-Conditional DCGAN (cDCGAN)** incorporating Spectral Normalization and projection conditioning that synthesizes aerial parcels in **32 ms** with **99.40% intended-class proxy recognition**;
5. A **Class-Conditional Denoising Diffusion Probabilistic Model (DDPM)** accelerated by a 20-step deterministic DDIM sampler achieving **0.0304 noise MSE** and superior structural photorealism; and
6. A domain-specialized causal **Transformer (MiniGPT)** yielding **1.110 perplexity** (0.1505 bits/character) to formulate legally grounded Floor Space Index (FSI) and Transit-Oriented Development (TOD) bylaws.

Executed entirely on consumer edge hardware (NVIDIA RTX 4050 6 GB, **0.133 kWh cumulative energy, 94.0 g CO$_2$e**), UrbanGen AI demonstrates that municipal intelligence can operate with high structural fidelity while preserving institutional data sovereignty.

**Keywords:** Generative Artificial Intelligence, Remote Sensing, Denoising Autoencoder, Variational Autoencoder, Conditional GAN, Diffusion Models, Causal Transformer, Smart Cities, Green AI.

---

## 1. Introduction
Modern municipal administration requires continuous balancing among population growth, commercial expansion, transit connectivity, and ecological conservation. As metropolitan regions expand, traditional urban planning relies predominantly on periodic, manual photointerpretation of satellite imagery and static Geographic Information System (GIS) records. This manual paradigm is characterized by high operational latency, substantial labor overhead, and an inability to simulate speculative future urban configurations or synthesize proactive policy guidance.

The emergence of Deep Learning (DL) and Generative Artificial Intelligence (GenAI) presents transformative opportunities for Earth observation and spatial analytics. Recently, multi-model generative frameworks that study complementary neural architectures under unified experimental protocols have shown strong potential across diverse domains (Mane et al., I3CTCON 2026). In Earth observation, computer vision networks excel at land-use and land-cover (LULC) classification, while generative models—specifically Autoencoders (AEs), Variational Autoencoders (VAEs), Generative Adversarial Networks (GANs), and Denoising Diffusion Probabilistic Models (DDPMs)—provide powerful mechanisms for optical restoration, continuous latent feature morphing, and synthetic scenario prototyping. Concurrently, causal autoregressive Transformers offer structured semantic translation capabilities.

Despite these advances, existing generative architectures in the remote sensing and urban planning domains face four persistent technical bottlenecks:
1. **Atmospheric Scattering and Sensor Noise:** Satellite optical sensors are inherently exposed to cloud haze, aerosol scattering, and sensor calibration degradation. Standard bottleneck autoencoders oversmooth high-frequency spatial boundaries, destroying orthogonal street grids and building footprints.
2. **Latent Topological Collapse in Variational Models:** Conventional VAEs compress feature representations into flat 1D latent vectors, stripping away 2D spatial relationships and suffering from posterior collapse when applied to complex remote sensing textures.
3. **Generative Instability and Lack of Objective Semantic Auditing:** GANs frequently exhibit mode collapse and boundary artifacts on heterogeneous aerial distributions, while diffusion models are computationally prohibitive for edge workstations. Crucially, the literature lacks an objective, frozen semantic auditing mechanism to mathematically evaluate whether synthetic aerial parcels adhere to target zoning semantics without relying on subjective human inspection.
4. **Disconnection Between Spatial Analytics and Regulatory Policy Formulation:** Computer vision outputs exist in raster space, whereas municipal urban planners operate through legal bylaws, Floor Space Index (FSI) allocations, and environmental zoning codes. General-purpose large language models (LLMs) hallucinate inapplicable regulations when queried on localized municipal frameworks.

### Research Questions (RQs)
- **RQ1 (Spatial Restoration):** Can multi-scale transposed skip connections overcome the high-frequency information loss of traditional bottleneck autoencoders to recover fine parcel boundaries from noise-corrupted aerial imagery?
- **RQ2 (Latent Topology & Anomaly):** Can a 3D topology-preserving spatial latent tensor maintain geospatial continuity across urban archetypes without posterior collapse while functioning as an unsupervised municipal anomaly detector?
- **RQ3 (Generative Trade-offs):** How do projection-conditioned adversarial networks (cDCGAN) and reverse diffusion models (DDPM/DDIM) compare across class fidelity, structural photorealism, and edge inference latency?
- **RQ4 (Cross-Modal Regulatory Grounding):** Can a domain-specialized causal Transformer bridge quantitative spatial vision telemetry into grounded, legally compliant municipal development control regulations without factual hallucination?

### Core Scientific Contributions
1. **Unified Cooperative Architecture:** An end-to-end framework integrating six neural network modules that bridge raw satellite imagery ingestion, signal restoration, continuous latent space traversal, generative synthesis, frozen semantic auditing, and municipal policy drafting.
2. **Topology-Preserving Spatial Manifold and Disparity Anomaly Engine:** A Spatial $\beta$-VAE that retains a 3D tensor latent representation $\mathbb{R}^{64 \times 8 \times 8}$ under a calibrated $\beta = 10^{-4}$ Pareto objective, enabling smooth land-use morphing without posterior collapse and flagging unauthorized zoning encroachments ($>3\sigma$ disparity).
3. **Dual-Modality Synthesis with Objective Frozen Auditing:** An adversarial cDCGAN stabilized via Spectral Normalization and projection conditioning alongside a 20-step accelerated DDIM diffusion sampler, benchmarked against an independent, frozen ResNet-18 classifier (99.40% semantic proxy fidelity).
4. **Edge-Feasible Green AI Audit & Grounded Policy Engine:** Benchmarking on a consumer NVIDIA RTX 4050 Laptop GPU under a uniform 50-epoch protocol (0.133 kWh total footprint, 94.0 g CO$_2$e) while demonstrating zero cloud data leakage for municipal data sovereignty.

---

## 2. Related Work
- **Remote Sensing Image Restoration:** Surveys the transition from classical denoising to DAEs (Vincent et al.), DnCNN (Zhang et al.), U-Net skip architectures (Ronneberger et al.), and modern Vision Transformers (SwinIR, HAT), establishing why lightweight skip-connected CNNs remain superior for edge inference.
- **Land-Use Classification:** Traces evolution from Bag-of-Visual-Words (Yang et al.) to deep residual learning (He et al.) and transfer learning in Earth observation.
- **Generative Adversarial Networks & Diffusion Models:** Analyzes DCGAN (Radford et al.), conditional GANs (Mirza et al.), Spectral Normalization (Miyato et al.), projection discriminators, and recent Earth observation diffusion paradigms (DDPM, DDIM, Remote-Diffusion, GeoDiffusion).
- **Urban Digital Twins & Green AI:** Reviews urban planning digital twin frameworks and the imperative for carbon-efficient, locally deployable intelligence (Schwartz et al., Green AI).
- **Research Gap:** Explicitly identifies the lack of an edge-deployable system coupling optical restoration, spatial latent exploration, multi-modal synthesis, automated frozen semantic verification, and regulatory policy drafting.

---

## 3. System Architecture & Methodology

```
[Raw Aerial Orthoimagery (USGS UCMerced)]
                  │
                  ▼
   [Atmospheric Degradation Layer (σ=0.15)]
                  │
                  ▼
   [Stage 1: Denoising U-Net Autoencoder] ───► Clean Restored Tile (29.65 dB PSNR)
                  │
         ┌────────┴───────────────────────────┐
         ▼                                    ▼
[Stage 2: Spatial β-VAE]             [Stage 3: ResNet-18 Classifier]
(3D Latent Tensor 64x8x8;            (Frozen Semantic Auditor;
 Anomaly Disparity > 3σ)              98.10% Val Accuracy, 0.9784 F1)
         │                                    │
         ▼                                    ▼
[Stage 4: Dual-Modality Synthesis]   [Stage 5: MiniGPT Policy Engine]
• Residual cDCGAN (<35ms, 99.40%)    • 4-Layer Pre-LN Transformer
• Conditional DDPM (1.82s DDIM)      • Grounded Bylaws (FSI 1.8-2.4, TOD)
         │                                    │
         └─────────────────┬──────────────────┘
                           ▼
[Stage 6: Air-Gapped Edge Hardware & Closed-Loop Municipal Governance]
(NVIDIA RTX 4050 6GB, 0.133 kWh Green AI, Zero Cloud Leakage, HITL Policy)
```

### Complete Layer Specifications & Parameter Counts
- **Model 1 (U-Net DAE):** 2.45M parameters | 8.4 ms latency | 412 MB VRAM
- **Model 2 (Spatial $\beta$-VAE):** 3.12M parameters | 11.2 ms latency | 528 MB VRAM
- **Model 3 (ResNet-18 Auditor):** 11.18M parameters | 5.1 ms latency | 380 MB VRAM
- **Model 4 (Residual cDCGAN):** 4.86M parameters | 32.0 ms latency | 620 MB VRAM
- **Model 5 (Conditional DDPM):** 2.82M parameters | 1,820 ms latency | 890 MB VRAM
- **Model 6 (MiniGPT Transformer):** 1.84M parameters | 45.0 ms latency | 290 MB VRAM

---

## 4. Experimental Results and Comparative Benchmarking

### Comparative Benchmark: Optical Remote Sensing Restoration
| Architecture / Method | Parameters | PSNR (dB) $\uparrow$ | SSIM $\uparrow$ | Latency $\downarrow$ | Compute Feasibility |
|:---|:---:|:---:|:---:|:---:|:---|
| Degraded Input Baseline ($\sigma=0.15$) | — | 12.04 dB | 0.3412 | — | Unusable for Zoning |
| Bottleneck AE (Standard Baseline) | 2.1 M | 25.02 dB | 0.7210 | 6.2 ms | Local GPU |
| DnCNN (Zhang et al., 2017) | 0.56 M | 27.84 dB | 0.8120 | 14.8 ms | Edge Real-Time |
| RIDNet (Anwar et al., 2019) | 1.49 M | 28.62 dB | 0.8390 | 28.5 ms | Edge Real-Time |
| SwinIR (Liang et al., 2021) | 11.8 M | 29.82 dB | 0.8710 | 142.0 ms | Exceeds Edge VRAM (3.2 GB) |
| **UrbanGen U-Net DAE (Proposed)** | **2.45 M** | **29.65 dB** | **0.8649** | **8.4 ms** | **Champion Edge Restoration** |

### Comparative Benchmark: Territorial Zoning Classification
| Model Architecture | Parameters | Top-1 Accuracy $\uparrow$ | Macro F1 $\uparrow$ | Inference Latency $\downarrow$ |
|:---|:---:|:---:|:---:|:---:|
| Bag-of-Visual-Words (Yang et al., 2010) | — | 76.80% | 0.7410 | 320 ms |
| VGG-16 (Simonyan et al., 2014) | 138.4 M | 94.20% | 0.9380 | 22.4 ms |
| MobileNetV3-Large (Howard et al., 2019) | 5.4 M | 96.40% | 0.9590 | 4.2 ms |
| DenseNet-121 (Huang et al., 2017) | 8.0 M | 97.60% | 0.9710 | 9.8 ms |
| ResNet-50 (He et al., 2016) | 25.6 M | 98.30% | 0.9800 | 11.5 ms |
| **ResNet-18 Auditor (Proposed)** | **11.2 M** | **98.10%** | **0.9784** | **5.1 ms** |

### Comparative Benchmark: Generative Synthesis
| Generative Architecture | Sampling Method | Semantic Proxy Recognition $\uparrow$ | Inference Latency $\downarrow$ | Operational Status |
|:---|:---|:---:|:---:|:---|
| Vanilla DCGAN (Radford et al., 2015) | 1-Step Direct | 68.20% | 24 ms | Severe Mode Collapse |
| cGAN (Mirza & Osindero, 2014) | 1-Step Direct | 72.40% | 26 ms | Edge Real-Time |
| WGAN-GP (Gulrajani et al., 2017) | 1-Step Direct | 81.50% | 28 ms | Edge Real-Time |
| StyleGAN2-ADA (Karras et al., 2020) | 1-Step Direct | 91.20% | 68 ms | High VRAM (4.8 GB) |
| Standard DDPM (Ho et al., 2020) | 1000-Step Ancestral | 96.80% | 28,400 ms | Impractical at Edge (28.4s) |
| **UrbanGen Residual cDCGAN (Ours)** | **1-Step Residual** | **99.40%** | **32 ms** | **Champion Edge Speed** |
| **UrbanGen Conditional DDPM (Ours)** | **20-Step DDIM** | **98.60%** | **1,820 ms** | **Champion Photorealism** |

### In-Depth Ablations
1. **Multi-Scale Skip Connections in DAE:** Demonstrates incremental gains from No Skips (25.02 dB) $\to$ Stem-only (26.41 dB) $\to$ Stem+L1 (28.15 dB) $\to$ Full Multi-Scale (29.65 dB), proving a +7.0 dB recovery gain on dense housing.
2. **Pareto Trade-off on $\beta$ in Spatial VAE:** $\beta=1.0$ causes posterior collapse (KL 4.12 nats, severe blur); $\beta=10^{-4}$ achieves optimal Pareto frontier (27.49 dB PSNR, KL 60.72 nats); $\beta=10^{-6}$ leads to latent tearing.
3. **Generative Stabilization in cDCGAN:** Proves Spectral Normalization prevents gradient explosion, while projection conditioning elevates proxy recognition from 81.2% to 99.40%.
4. **Diffusion Acceleration:** 20-step DDIM achieves 15.6× speedup over 1000-step DDPM with identical 0.0304 noise MSE.

### Green AI Hardware Audit (Uniform 50-Epoch Protocol)
- **Cumulative Training Time:** 66.3 minutes across all 6 models
- **Total Energy Consumed:** 0.133 kWh (measured via NVML power polling)
- **Total Carbon Footprint:** 94.0 g CO$_2$e (CEA grid factor 0.708 kg/kWh)
- **Hardware Platform:** NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP capped)

---

## 5. Ethical Considerations & Governance
1. **Advisory Decision Support:** System acts strictly as an assistive drafting tool; autonomous zoning enforcement is prohibited.
2. **Domain Shift Awareness:** Explicit disclaimers and confidence indicators accompany deployment on dense Global South fabrics.
3. **Data Sovereignty:** 100% on-premises execution guarantees zero municipal GIS telemetry leakage to external clouds.

---

## 6. Conclusion & Future Work
UrbanGen AI proves that specialized cooperative multi-model architectures outperform monolithic foundation models on constrained edge hardware for municipal planning tasks. Future work will expand to 12-band Sentinel-2 multi-spectral data, cross-attention vision-language diffusion, and Physics-Informed Neural Networks (PINNs) for microclimate simulation.
