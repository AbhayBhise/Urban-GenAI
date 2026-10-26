# UrbanGen AI: An Edge-Deployable Multi-Model Generative Framework for Aerial Remote Sensing and Municipal Urban Planning

**Authors:**
- **Abhay Bhise** (`abhaybhise30@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*
- **Vedant Ingle** (`vedantingle05@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*
- **Rushikesh Bodake** (`rushikeshbodake7@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*
- **Pranav Kolte** (`pranavkolte2003@gmail.com`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*
- **Prof. Savita Jadhav** (`ssjadhav@comp.mitaoe.ac.in`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*
- **Prof. Pramod Ganjewar** (`pdganjewar@comp.mitaoe.ac.in`)  
  *Department of Computer Engineering, MIT Academy of Engineering, Alandi, Pune, India*

**Target Format:** IEEE Conference Proceedings (Double Column)  
**LaTeX Master File:** [`docs/IEEE_Conference_Paper.tex`](file:///f:/PROJECTS/GEN%20AI%20PROJECT/UrbanGenAI/docs/IEEE_Conference_Paper.tex)  
**Overleaf Ready Package:** [`paper_package/UrbanGenAI_Paper_Overleaf.zip`](file:///f:/PROJECTS/GEN%20AI%20PROJECT/UrbanGenAI/paper_package/UrbanGenAI_Paper_Overleaf.zip)  
**High-Resolution Figures Directory:** [`docs/figures/`](file:///f:/PROJECTS/GEN%20AI%20PROJECT/UrbanGenAI/docs/figures)

---

### Abstract
Rapid global urbanization creates urgent challenges in zoning compliance, green cover preservation, transportation infrastructure, and spatial resilience. In this paper, we introduce **UrbanGen AI**, an edge-deployable multi-model generative framework for aerial remote sensing analysis and municipal urban planning decision support. To ensure rigorous, fair comparative benchmarking, all core models are trained under a uniform, controlled 50-epoch protocol on the UCMerced LandUse benchmark: (i) a U-Net Denoising Autoencoder achieving 29.65 dB PSNR (MSE 0.00585), (ii) a Spatial Variational Autoencoder ($\beta$-VAE) achieving 29.75 dB validation PSNR with structured latent manifold traversal, (iii) an ImageNet-adapted ResNet-18 Territorial Classifier attaining 98.10% validation accuracy, (iv) a Class-Conditional DCGAN (cDCGAN) reaching balanced adversarial equilibrium ($D=1.639, G=1.232$) with 99.40% intended-class recognition across 168 synthesized tiles, (v) a Class-Conditional Denoising Diffusion Probabilistic Model (DDPM with 20-step accelerated DDIM sampling) converging to 0.0881 noise MSE, and (vi) a domain-specific causal Transformer (MiniGPT) yielding 1.087 perplexity on municipal urban planning mandates. By delivering an end-to-end pipeline spanning signal restoration, latent anomaly mapping, multi-modal generative synthesis, and grounded policy formulation on consumer edge hardware (RTX 4050 6 GB, 0.20 kWh total training footprint), UrbanGen AI demonstrates that local municipal intelligence can operate reliably while preserving institutional data sovereignty.

**Keywords:** Generative Artificial Intelligence, Urban Planning, Remote Sensing, Denoising Autoencoder, Variational Autoencoder, Conditional GAN, Transformers, Smart Cities, Green AI.

---

## 1. Introduction
Development of modern cities involves juggling population growth, industrial growth, transit integration, and ecology preservation [1]–[3]. While cities grow, the traditional approach in municipal planning is based on the periodic and manual interpretation of satellite imagery along with static Geographic Information Systems (GIS) databases. Such an approach is characterized by high latencies, expensive labor force, and inability to model hypothetical future urban development or provide proactive policy-making.

Deep Learning (DL) and Generative Artificial Intelligence (GenAI) offer new prospects in urban analytics [4], [5]. The computer vision techniques perform well in land use and land cover (LULC) classification [6]–[9], while the generative models such as Autoencoders (AE), Variational Autoencoders (VAE), Generative Adversarial Networks (GAN), and Large Language Models (LLM) provide efficient means of signal denoising, spatial synthesis, continuous latent feature morphing, and automated policy-making. However, complex atmospheric scattering and spatial domain shift across diverse urban fabrics remain persistent obstacles [10].

There are some challenges in current generative architecture in spatial domains:
- **Noisy Sensors and Degradation of Environment:** The aerial and satellite sensors are innately exposed to atmospheric scattering, cloud shadows, and optical noise in the sensor.
- **Non-Coherent Architecture Processes:** Analytical models such as classifiers and generative models like GANs, Variational Auto Encoders, and Transformers usually work independently of each other in a disconnected manner.
- **High Compute Costs and Unfriendly Environment:** Many existing generation frameworks need vast compute clusters inside data centers which makes the framework hard to implement by municipalities.
- **Absence of Spatial Awareness in Policy Generation:** Pre-trained off-the-shelf LLMs do not have any domain-specific fine-tuning of regional municipalities and generate infeasible policy suggestions.

These issues are addressed by UrbanGen AI, a multi-modal generative intelligence platform tailored for municipal urban spatial planning applications. The model operates on a consumer NVIDIA RTX 4050 graphics card, ensures data sovereignty, and is offered as an assistive prototype rather than an autonomous zoning authority. Claims to energy and carbon savings are only made when backed up by reproducible hardware measurements.

---

## 2. Literature Review

The evolution of generative artificial intelligence and deep learning across visual and spatial domains has motivated diverse architectural strategies. In multi-modal educational resource synthesis, Mane et al. [10] introduced EduGen, an orchestrated pipeline integrating GANs for question generation, VAEs for diagram compression, LoRA-adapted Transformers for summarization, and Diffusion models for illustration synthesis. For visual restoration and synthesis benchmarks, Mane et al. [11] presented a comparative analysis across VAEs, GANs, Vision Transformers, and Denoising Diffusion Probabilistic Models (DDPMs), proving that iterative diffusion mechanisms achieve superior structural preservation and perceptual fidelity over adversarial and latent-variable baselines. In media security and digital forensics, Mane et al. [12] demonstrated a unified framework coupling generative synthesis (GANs and Diffusion) with forensic detection (VAEs and Vision Transformers), establishing that multi-model systems can bridge creation and verification within a single cohesive pipeline. Addressing domain-specific data scarcity and class imbalance, Kharkate and Mane [13] developed a hybrid generative framework employing VAE, DCGAN, and Diffusion models for synthetic visual augmentation to enhance diagnostic classification.

In Earth observation and remote sensing, convolutional neural networks have demonstrated high efficacy in territorial scene classification and semantic land-use parsing [6]–[8]. However, spatial degradation from atmospheric scattering and sensor noise impairs downstream aerial analytics [9]. Early spatial restoration frameworks relied on standard denoising autoencoders [14], while deeper residual architectures [15] and multi-scale skip connections [16], [17] have advanced feature reconstruction. In territorial classification, ImageNet-pretrained representations [18] optimized via Adam [19] and data augmentation [20] form the standard backbone for zoning validation.

For generative visual modeling, Kingma and Welling [21] established Auto-Encoding Variational Bayes, later extended to $\beta$-VAE [22] for disentangled representations, while reconstruction disparity has been adapted for anomaly detection [23], [24]. Concurrently, Generative Adversarial Networks [25] and Deep Convolutional GANs [26] enabled sharp visual synthesis, with conditional GAN formulations [27], spectral normalization [28], projection discriminators [29], and auxiliary classifiers [30] stabilizing class-conditioned generation. To overcome adversarial mode collapse, non-equilibrium thermodynamics foundations [31] led to Denoising Diffusion Probabilistic Models (DDPM) [32], with accelerated sampling enabled by DDIM [33] and classifier guidance [34]. In language modeling, causal autoregressive Transformers [35], [36] provide powerful semantic sequence generation.

**Research Gap:** While these studies explore generative architectures in isolation or within single-modality tasks, remote sensing lacks a unified, edge-deployable multi-model platform that concurrently coordinates signal restoration, continuous latent zoning exploration, class-conditioned parcel generation, automated auditing, and grounded policy formulation. UrbanGen AI bridges this gap through a consolidated, multi-model generative intelligence pipeline.

---

## 3. System Architecture and Methodology

The UrbanGen AI pipeline is made up of five unique modules that tackle different stages in the spatial intelligence life cycle: restoration, classification, latent representation, generative synthesis, and contextual advisory text generation.

### A. Denoising Autoencoder with Skip Connections (U-Net AE)
Degraded satellite imagery directly impairs automated zoning identification. We formulate an aerial tile denoising task where the input image $x \in \mathbb{R}^{3 \times 128 \times 128}$ is corrupted by zero-mean additive Gaussian noise $\eta \sim \mathcal{N}(0, \sigma^2)$ with $\sigma = 0.15$ [14]:
$$\tilde{x} = \text{clip}(x + \eta, 0, 1)$$

The first baseline model employed a deep residual learning backbone network [15] with bottleneck compression, which generated a spatial feature map of size $8 \times 8 \times 256$. Although global textures could be recovered successfully, there was a problem of blurring and loss of high-frequency structures (important for road junctions and clustered buildings).

In order to address this issue, we added multi-scale skip connections inspired by U-Net architectures [16] between the feature maps of the stem, Layer 1, Layer 2, and Layer 3 into the decoder stages via transposed convolutions:
$$\hat{x} = \mathcal{D}\Big(\mathcal{E}(\tilde{x}), \{\mathbf{F}_{\text{stem}}, \mathbf{F}_1, \mathbf{F}_2, \mathbf{F}_3\}\Big)$$

The reconstruction objective minimizes the Mean Squared Error (MSE), providing an effective residual learning formulation for aerial signal restoration [17]:
$$\mathcal{L}_{\text{AE}} = \frac{1}{N} \sum_{i=1}^N \|x^{(i)} - \hat{x}^{(i)}\|_2^2$$

### B. Deep Convolutional Land-Use Classifier
For automated municipal auditing, an ImageNet-pretrained [18] ResNet-18 architecture was adapted. The final fully-connected projection layer was replaced with a 21-dimensional linear classifier corresponding to standard land-use categories:
$$\hat{y} = \text{Softmax}(\mathbf{W}_c \cdot f_{\text{ResNet}}(x) + b_c)$$
Trained with categorical Cross-Entropy loss over 50 epochs with Adam optimization ($\text{lr} = 10^{-4}$) [19] and data augmentation strategies [20], the model performs continuous territorial zoning validation.

### C. Spatial Variational Autoencoder (Spatial VAE)
While deterministic autoencoders map inputs to isolated point vectors, sustainable planning requires navigating a continuous design space to explore transitional states (e.g., transforming industrial parcels into mixed-use eco-districts).

Our spatial VAE implements a deep convolutional encoder following Auto-Encoding Variational Bayes principles [21] that outputs parametric distribution tensors representing mean $\boldsymbol{\mu} \in \mathbb{R}^{64 \times 8 \times 8}$ and log-variance $\log \boldsymbol{\sigma}^2 \in \mathbb{R}^{64 \times 8 \times 8}$. Utilizing the reparameterization trick:
$$\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

The optimization objective balances spatial reconstruction fidelity with probabilistic latent regularisation:
$$\mathcal{L}_{\text{VAE}} = \mathcal{L}_{\text{recon}}(x, \hat{x}) + \beta \cdot D_{\text{KL}}\big(q_\phi(\mathbf{z}|x) \,\|\, p(\mathbf{z})\big)$$
Where $\mathcal{L}_{\text{recon}} = 0.7 \cdot \mathcal{L}_1 + 0.3 \cdot \mathcal{L}_{\text{MSE}}$, and $\beta = 10^{-4}$ establishes a $\beta$-VAE [22] reconstruction-priority regime, preventing over-regularization from smearing sharp parcel boundaries.

**Anomaly Detection Formulation:** UrbanGen AI exploits reconstruction error as an unsupervised spatial anomaly indicator [23]:
$$\text{Score}_{\text{anomaly}}(x) = \frac{1}{C \cdot H \cdot W} \sum_{c,h,w} |x_{c,h,w} - \hat{x}_{c,h,w}|$$
Tiles exhibiting anomaly scores exceeding three standard deviations from the empirical baseline mean are automatically flagged for physical planning inspection, mirroring semi-supervised structural anomaly frameworks [24].

### D. Class-Conditional Deep Convolutional GAN (cDCGAN)
To augment sparse aerial datasets and generate hypothetical planning scenarios on demand, we developed a class-conditional deep convolutional generative adversarial network [25] operating at $128 \times 128$ resolution.

*Architectural Taxonomy and Clarification:* Academically, this network synergistically combines two distinct paradigms:
1. **Deep Convolutional GAN (DCGAN) Architecture** [26]: Employs strided and fractionally-strided convolutional blocks with Batch Normalization in $G$, leaky rectifiers in $D$, and avoids deterministic spatial pooling layers to stabilize spatial representation learning.
2. **Conditional GAN (cGAN) Mechanism** [27]: Conditions both the generator $G(z|y)$ and discriminator $D(x|y)$ upon class label embeddings $y \in \{1, \dots, 21\}$, directing synthesis toward specific zoning categories rather than unconstrained sampling.

Hence, the model is a **Class-Conditional DCGAN (cDCGAN)**: its convolutional generator and discriminator provide class-conditioned aerial tile synthesis.

- **Generator ($G$):** Takes a latent Gaussian noise vector $\mathbf{z} \sim \mathcal{N}(0, \mathbf{I}_{128})$ concatenated with a learned class embedding $\mathbf{e}_y \in \mathbb{R}^{64}$. A dense projection block maps the 192-dimensional vector into an $8 \times 8 \times 512$ feature volume, followed by four transposed convolution blocks with Batch Normalization and LeakyReLU activations, concluding with a $\text{Tanh}$ transfer function producing $128 \times 128 \times 3$ aerial tiles.
- **Projection Discriminator ($D$):** Receives image $x$ through five convolutional layers stabilized with spectral normalization [28] yielding deep visual representation $\phi(x)$. Adopting the Miyato & Koyama projection mechanism [29], the adversarial score is formulated as $D(x, y) = \psi(\phi(x)) + y^T V \phi(x)$, directly inner-producting the class vector with deep spatial features, alongside an auxiliary classifier head [30] predicting class logits $\hat{y}$.

To ensure crisp geometric structural synthesis, Generator training is governed by composite adversarial, auxiliary classification, and deep semantic guidance from the pre-trained ResNet-18 classifier: $\mathcal{L}_G = \mathcal{L}_{\text{adv}} + 0.8\mathcal{L}_{\text{AC}} + 1.2\mathcal{L}_{\text{semantic}}$. Paired with soft label smoothing ($y_{\text{real}}=0.9, y_{\text{fake}}=0.1$) and Exponential Moving Average (EMA, decay 0.999), this formulation guarantees stable convergence ($D \approx 1.401, G \approx 1.332$) without mode collapse.

### E. Class-Conditional Denoising Diffusion Probabilistic Model (DDPM)
While GANs synthesize samples in a single forward pass via competitive adversarial games, they are vulnerable to training instability and mode dropping. Built upon non-equilibrium thermodynamics foundations [31], UrbanGen AI incorporates a class-conditional Denoising Diffusion Probabilistic Model (DDPM) [32].

The forward diffusion process progressively perturbs clean aerial imagery $\mathbf{x}_0 \in \mathbb{R}^{3 \times 128 \times 128}$ over $T=1000$ discrete timesteps via a linear variance schedule $\beta_1, \dots, \beta_T$:
$$q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}\Big(\mathbf{x}_t;\, \sqrt{\bar{\alpha}_t} \mathbf{x}_0,\, (1 - \bar{\alpha}_t)\mathbf{I}\Big)$$
where $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$. The reverse denoising network implements a lightweight U-Net parameterized by $\boldsymbol{\theta}$ conditioned on sinusoidal timestep embeddings $\mathbf{t}$ and discrete zoning class labels $c \in \{1, \dots, 21\}$. The network is optimized via the simplified noise prediction objective:
$$\mathcal{L}_{\text{diffusion}}(\boldsymbol{\theta}) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}, c}\Big[\big\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\boldsymbol{\theta}}(\mathbf{x}_t, t, c)\big\|_2^2\Big]$$

For rapid municipal decision support, synthesis accelerates via Denoising Diffusion Implicit Models (DDIM) [33], yielding sharp aerial parcels in 20 deterministic sampling steps and demonstrating the high structural fidelity of score-based diffusion over adversarial generation [34].

### F. Urban Plan Generator (MiniGPT Transformer)
To bridge quantitative visual spatial analysis with qualitative policy generation, UrbanGen AI implements a custom decoder-only autoregressive causal Transformer [35]. Adopting generative pre-training principles for causal language modeling [36], the model features 4 pre-layer-normalization Transformer blocks, 4 attention heads, embedding dimension $d_{\text{model}} = 256$, and context window length $T=192$.

Trained from scratch on a domain-curated sustainable urbanism corpus (`urban_planning.txt`) detailing transit-oriented development (TOD) paradigms, floor space index (FSI), rainwater harvesting mandates, and green buffer zoning, the model computes:
$$P(w_t | w_{<t}) = \text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}} \mathbf{V}\right)$$
Inference is executed via dynamic top-$k$ ($k=40$) and temperature-scaled sampling seeded directly with real-world municipal land-cover teleme---

## 4. Experimental Results and Discussion

### A. Experimental Setup
Models were trained using the PyTorch 2.x framework and evaluated on the UCMerced LandUse dataset [7] containing 2,100 high-resolution aerial tiles categorized into 21 different land uses. Experiments were performed locally using an NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP). To ensure rigorous experimental comparability and eliminate batch-dependent gradient variance across all generative and analytical paradigms, a uniform batch size of 32 was maintained across all trained models.

### B. Image Denoising Performance: Skip Connections vs. Bottleneck Baseline
Using skip connections of U-Net brought transformative qualitative and quantitative results compared to the standard bottleneck encoder-decoder model. Fig. 1 shows how the reconstruction loss converges throughout the 50 epochs from 0.115 to 0.0058 MSE.

| Architecture | Epochs | Avg PSNR (dB) | MSE Loss |
|:---|:---:|:---:|:---:|
| Noisy Baseline ($\sigma=0.15$) | --- | 12.04 | 0.06260 |
| Bottleneck AE (Standard Baseline) | 50 | 25.02 | 0.00790 |
| **UrbanGen Skip-AE (Proposed)** | **50** | **29.65** | **0.00449** |

- Complex land cover categories, such as residential dense, harbor, and mobile homes, achieved individual improvements of **+7.0 dB individually**.
- Performance disparity between easiest and hardest categories reduced from **7.3 dB down to 2.6 dB**.

### C. Land-Use Classification Accuracy
The ResNet-18 territorial zoning classifier converged reliably on the 90/10 train/validation split across the uniform 50-epoch protocol:
- **Validation Accuracy (Top-1):** 98.10% across all 21 classes.
- **Cross-Entropy Loss:** Final validation loss 0.0880 (training loss 0.0450).
- **Macro F1 Score:** 0.9784 with zero overlap between open green/agricultural parcels and high-density urban infrastructure.

### D. Latent Space Traversal and Anomaly Detection
For the Spatial VAE prioritizing reconstruction ($\beta=10^{-4}$), reconstruction loss decreased to 0.075, and KL divergence remained at 103 nats (41.79 nats in balanced checkpoint). Latent interpolation ($z(\alpha) = (1-\alpha)z_A + \alpha z_B$) produced continuous, topology-preserving morphing across diverse urban archetypes without semantic collapse.

### E. Conditional Generative Synthesis (Residual cDCGAN)
Under the 50-epoch protocol, the cDCGAN reached balanced equilibrium ($D=1.639, G=1.232$). Across 168 synthesized tiles spanning all 21 classes, the independent classifier attained a **99.40% intended-class recognition rate** (167/168 tiles verified), demonstrating robust semantic fidelity.

### F. Multi-Model Benchmark Parameter Matrix

| Model Pipeline | Core Architecture | Epochs | Batch Size | Objective Loss Function | Final Convergence Loss |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Denoising Autoencoder** | U-Net (Skip Connections) | 50 | 32 | MSE ($\|x - \hat{x}\|_2^2$) | $\mathcal{L}_{\text{MSE}} = 0.00585$ |
| **Spatial VAE** | ResNet-18 Encoder + Latent Tensor | 50 | 32 | $0.7\mathcal{L}_1 + 0.3\text{MSE} + \beta D_{\text{KL}}$ | Total: $0.0365$ (Recon: $0.0323$, KL: $41.79$) |
| **Territorial Classifier** | ResNet-18 + 21-way Projection | 50 | 32 | Categorical Cross-Entropy | Train: $0.0450$, Val: $0.0880$ (Acc: **98.10%**) |
| **Residual cDCGAN** | Projection cGAN + AC Head | 50 | 32 | $\mathcal{L}_{\text{BCE}} + 0.8\mathcal{L}_{\text{AC}} + 1.2\mathcal{L}_{\text{sem}}$ | $D=1.6387$, $G=1.2322$ (99.4% Proxy) |
| **Conditional DDPM** | Time/Class U-Net (DDIM) | 50 | 32 | Noise MSE ($\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta\|_2^2$) | Noise MSE: $0.08806$ (Best: $0.08412$) |
| **MiniGPT Transformer** | Causal Autoregressive | 50$^\dagger$ | 32 | Next-Token Cross-Entropy | Val CE: $0.0836$ (PPL: **1.087**) |

*Note: $^{\dagger}$MiniGPT was optimized across 3,000 steps with batch size 32, corresponding to 50 equivalent passes over the domain-curated municipal planning text corpus.*

| Model Pipeline | Core Functionality | Primary Benchmark Metric | Measured Value | Secondary Verification Metric | Measured Value |
|:---|:---|:---|:---:|:---|:---:|
| **Denoising U-Net AE** | Spatial Edge Restoration | Peak Signal-to-Noise Ratio (PSNR) | **29.65 dB** | Structural Similarity Index (SSIM) [37] | **0.8649** (MSE: $0.00585$) |
| **Spatial VAE** | Latent Disentanglement & Anomaly | Latent Reconstruction PSNR | **29.75 dB** | Information Divergence | **41.79 nats** (MSE: $0.00424$) |
| **ResNet-18 Classifier** | Territorial Land Zoning Audit | Top-1 Classification Accuracy | **98.10%** | Macro F1-Score | **0.9784** (CE: $0.0880$) |
| **Residual cDCGAN** | Fast Aerial Parcel Synthesis | Semantic Recognition Rate Proxy | **99.40%** (167/168) | Minimax Loss Equilibrium | $D=1.639$, $G=1.232$ |
| **Conditional DDPM** | Multi-Scale Stochastic Tile Diffusion| Noise Estimation MSE ($\mathcal{L}_{\text{diff}}$) | **0.0881** | Inference Acceleration (DDIM) | **20 Steps** ($50\times$ speedup) |
| **MiniGPT Transformer** | Municipal Planning Policy Advisory | Text Perplexity (PPL) | **1.087** | Bits-Per-Character (BPC) | **0.1199** (CE: $0.0836$) |

---

## 5. Green AI and Energy Footprint Analysis

In adherence to Green AI principles [38], all 6 architectures were trained locally on consumer hardware:

| Model Architecture | Training Horizon | Wall Time (min) | Mean Power (W) | Energy (kWh) | Carbon Footprint (gCO$_2$e) |
|:---|:---:|:---:|:---:|:---:|:---:|
| U-Net Denoising Autoencoder | 50 epochs | 15.2 | 118 | 0.030 | 21.3 |
| Spatial Variational Autoencoder | 50 epochs | 20.4 | 118 | 0.040 | 28.4 |
| ResNet-18 Land-Use Classifier | 50 epochs | 18.5 | 123 | 0.038 | 27.0 |
| Residual Class-Conditional DCGAN | 50 epochs | 17.5 | 120 | 0.035 | 24.8 |
| Conditional Diffusion Model (DDPM) | 50 epochs | 22.0 | 123 | 0.045 | 31.9 |
| MiniGPT Planning Transformer | 50 equiv. epochs | 8.3 | 108 | 0.015 | 10.6 |
| **Total Integrated Framework** | **Aligned 50-Epoch Suite** | **101.9 min** | **118 W avg** | **0.203 kWh** | **144.0 gCO$_2$e** |

---

## 6. Ethical Considerations and Governance

Urban spatial interventions directly affect citizen well-being, mobility networks, and equitable resource allocation. Ethical guarantees are codified into UrbanGen AI:
1. **Advisory Human in the Loop:** UrbanGen AI is designed exclusively as an assistive drafting system; automated policy or zoning enforcement without certification by a qualified urban planner is strictly prohibited.
2. **Domain Shift Awareness and Regional Drift:** Training on standardized benchmark data introduces domain shift when applied to Global South topologies and informal settlements (e.g., in Pune). The system explicitly generates confidence metrics and diagnostic disclaimers to prevent uncritical algorithmic reliance.
3. **Data Sovereignty and Privacy:** Operating locally on edge hardware guarantees the complete protection of high-resolution municipal spatial telemetry from third-party cloud leakage.

---

## 7. Conclusion and Future Work

In this paper, we presented **UrbanGen AI**, a multi-model generative intelligence framework capable of edge deployment for data-driven municipal spatial analysis. The combination of six deep neural network architectures provides an end-to-end pipeline connecting raw satellite observation with actionable municipal policy drafting. Future work will integrate 12-channel ESA Sentinel-2 multi-spectral telemetry [39], cross-modal vision-language conditioning, and Physics-Informed Neural Networks (PINNs) [40] for microclimate heat dissipation and aerodynamic wind corridor simulations.

---

## References

1. Q. Weng, "Land use change analysis in the Zhujiang Delta of China using satellite remote sensing, GIS and stochastic modelling," *Journal of Environmental Management*, vol. 64, no. 3, pp. 273–284, 2002.
2. M. Batty, *The New Science of Cities*. Cambridge, MA, USA: MIT Press, 2013.
3. J. A. Benediktsson, V. Akbari, and G. Camps-Valls, "Remote sensing for smart cities," *IEEE Geoscience and Remote Sensing Magazine*, vol. 3, no. 4, pp. 6–7, 2015.
4. Y. LeCun, Y. Bengio, and G. Hinton, "Deep learning," *Nature*, vol. 521, no. 7553, pp. 436–444, 2015.
5. X. X. Zhu et al., "Deep learning in remote sensing: A comprehensive review and list of resources," *IEEE Geoscience and Remote Sensing Magazine*, vol. 5, no. 4, pp. 8–36, 2017.
6. G. Cheng, J. Han, and X. Lu, "Remote sensing image scene classification: Benchmark and state of the art," *Proceedings of the IEEE*, vol. 105, no. 10, pp. 1865–1883, 2017.
7. Y. Yang and S. Newsam, "Bag-of-visual-words and spatial extensions for land-use classification," in *Proc. 18th ACM SIGSPATIAL Int. Conf. Adv. Geogr. Inf. Syst.*, 2010, pp. 270–279.
8. J. Long, E. Shelhamer, and T. Darrell, "Fully convolutional networks for semantic segmentation," in *Proc. IEEE CVPR*, 2015, pp. 3431–3440.
9. D. Tuia et al., "Domain adaptation in remote sensing: An overview," *IEEE Geoscience and Remote Sensing Magazine*, vol. 4, no. 2, pp. 41–57, 2016.
10. S. Mane, A. Tamboli, S. Jadhav, O. Bhutkar, S. Karne, and Y. Gunjal, "EduGen: A multi-model generative AI framework for dynamic educational resource synthesis," in *Proc. IEEE Int. Conf. Convergence Comput. Technol. (I3CTCON)*, 2026, doi: 10.1109/I3CTCON68242.2026.11507192.
11. S. Mane, S. Barve, A. Nitnaware, and A. Gapat, "Comparative analysis of generative AI models for image colorization," in *Proc. IEEE Int. Conf. Convergence Comput. Technol. (I3CTCON)*, 2026, doi: 10.1109/I3CTCON68242.2026.11507916.
12. S. Mane, S. Barve, A. Popalghat, V. Jadhav, A. Rewatkar, and M. Kapgate, "A unified generative AI system for synthetic image creation and detection," in *Proc. IEEE Int. Conf. Convergence Comput. Technol. (I3CTCON)*, 2026, doi: 10.1109/I3CTCON68242.2026.11507145.
13. S. Kharkate, P. Yerawar, N. Mahajan, K. Katare, S. Mane, and P. Ganjewar, "Generative AI-based synthetic data generation for skin disease classification using VAE, GAN, and diffusion models," in *Proc. IEEE Int. Conf. Convergence Comput. Technol. (I3CTCON)*, 2026, doi: 10.1109/I3CTCON68242.2026.11507289.
14. P. Vincent, H. Larochelle, Y. Bengio, and P.-A. Manzagol, "Extracting and composing robust features with denoising autoencoders," in *Proc. 25th Int. Conf. Mach. Learn. (ICML)*, 2008, pp. 1096–1103.
15. K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE CVPR*, 2016, pp. 770–778.
16. O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical image segmentation," in *Proc. MICCAI*, 2015, pp. 234–241.
17. K. Zhang, W. Zuo, Y. Chen, D. Meng, and L. Zhang, "Beyond a Gaussian denoiser: Residual learning of deep CNN for image denoising," *IEEE Trans. Image Process.*, vol. 26, no. 7, pp. 3142–3155, 2017.
18. A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet classification with deep convolutional neural networks," in *Advances in Neural Information Processing Systems*, vol. 25, 2012, pp. 1097–1105.
19. D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *Proc. ICLR*, 2015.
20. L. Perez and J. Wang, "The effectiveness of data augmentation in image classification using deep learning," *arXiv preprint arXiv:1712.04621*, 2017.
21. D. P. Kingma and M. Welling, "Auto-encoding variational Bayes," in *Proc. ICLR*, 2014.
22. I. Higgins et al., "$\beta$-VAE: Learning basic visual concepts with a constrained variational framework," in *Proc. ICLR*, 2017.
23. J. An and S. Cho, "Variational autoencoder based anomaly detection using reconstruction probability," *Special Lecture on IE*, vol. 2, no. 1, pp. 1–18, 2015.
24. S. Akcay, A. Atapour-Abarghouei, and T. P. Breckon, "GANomaly: Semi-supervised anomaly detection via adversarial training," in *Proc. ACCV*, 2018, pp. 622–637.
25. I. Goodfellow et al., "Generative adversarial nets," in *Advances in Neural Information Processing Systems*, vol. 27, 2014, pp. 2672–2680.
26. A. Radford, L. Metz, and S. Chintala, "Unsupervised representation learning with deep convolutional generative adversarial networks," in *Proc. ICLR*, 2016.
27. M. Mirza and S. Osindero, "Conditional generative adversarial nets," *arXiv preprint arXiv:1411.1784*, 2014.
28. T. Miyato, T. Kataoka, M. Koyama, and Y. Yoshida, "Spectral normalization for generative adversarial networks," in *Proc. ICLR*, 2018.
29. T. Miyato and M. Koyama, "cGANs with projection discriminator," in *Proc. ICLR*, 2018.
30. A. Odena, C. Olah, and J. Shlens, "Conditional image synthesis with auxiliary classifier GANs," in *Proc. ICML*, 2017, pp. 2642–2651.
31. J. Sohl-Dickstein, E. Weiss, N. Khanwalkar, and S. Ganguli, "Deep unsupervised learning using nonequilibrium thermodynamics," in *Proc. ICML*, 2015, pp. 2256–2265.
32. J. Ho, A. Jain, and P. Abbeel, "Denoising diffusion probabilistic models," in *Proc. NeurIPS*, vol. 33, 2020, pp. 6840–6851.
33. J. Song, C. Meng, and S. Ermon, "Denoising diffusion implicit models," in *Proc. ICLR*, 2021.
34. P. Dhariwal and A. Nichol, "Diffusion models beat GANs on image synthesis," in *Proc. NeurIPS*, vol. 34, 2021, pp. 8780–8794.
35. A. Vaswani et al., "Attention is all you need," in *Proc. NeurIPS*, 2017, pp. 5998–6008.
36. A. Radford et al., "Language models are unsupervised multitask learners," *OpenAI Blog*, vol. 1, no. 8, p. 9, 2019.
37. Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, "Image quality assessment: From error visibility to structural similarity," *IEEE Trans. Image Process.*, vol. 13, no. 4, pp. 600–612, 2004.
38. R. Schwartz, J. Dodge, N. A. Smith, and O. Etzioni, "Green AI," *Communications of the ACM*, vol. 63, no. 12, pp. 54–63, 2020.
39. M. Drusch et al., "Sentinel-2: ESA's optical high-resolution mission for GMES operational services," *Remote Sensing of Environment*, vol. 120, pp. 25–36, 2012.
40. M. Raissi, P. Perdikaris, and G. E. Karniadakis, "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations," *Journal of Computational Physics*, vol. 378, pp. 686–707, 2019.
