# UrbanGenAI: Project Status & Handover

This document outlines the current state of the UrbanGenAI project, verifying the authenticity of the implemented models, tracking progress against the course syllabus, and providing dataset resources. This is intended to help teammates seamlessly pick up the work and build the next features.

## 1. Is the Code Real or Fake (Mocked)?

**The core implementation is REAL.** 

The backend does **not** return fake or mocked machine learning responses. It uses genuine PyTorch model architectures and pre-trained weights (`.pth` files) for inference. 
Specifically:
- The **Autoencoder (AE)** genuinely performs denoising by injecting noise into tensors and running them through convolutional layers.
- The **Variational Autoencoder (VAE)** actually encodes images into a latent space (calculating `mu` and `logvar`), computes MSE, and determines an anomaly score based on a real statistical baseline. Interpolation happens mathematically in the latent space.
- The **Transformer (Vision Transformer)** performs actual classification on urban images.
- The **Frontend** connects to these real FastAPI endpoints (`/infer/ae`, `/infer/vae`, etc.). Some UI components might have static fallback text for layout purposes, but the core ML loop is fully functional and authentic.

---

## 2. Progress vs. Syllabus (2304422T Generative AI)

Here is exactly where the project stands according to your MIT Academy of Engineering course syllabus:

### ✅ IMPLEMENTED (Units 1, 2, 4, 6)
* **Unit 1 (Intro to GenAI):** Basic project setup, API structuring, and environment configurations are complete.
* **Unit 2 (Autoencoders & VAEs):** 
  * **Autoencoder (AE):** Implemented for Denoising (`models/autoencoder.py`).
  * **VAE:** Implemented with Reparameterization trick, KL divergence, and latent space interpolation (`models/vae.py`).
* **Unit 4 (Transformer-based Generative Models):**
  * **Vision Transformer (ViT):** Implemented as an urban land-use classifier using attention mechanisms (`models/transformer.py`).
* **Unit 6 (Ethical, Societal, Legal):** 
  * A **RAG pipeline** (`rag_pipeline.py`) has been set up to discuss data statistics, environmental/sustainability context (Pune datasets), and potential biases, fulfilling the societal application context.

### ⏳ REMAINING TO BUILD (Units 3 & 5)
For the teammate taking over, your immediate next steps are to implement the following to complete the syllabus requirements:

* **Unit 3 (Generative Adversarial Networks - GANs) & PRACT 3:**
  * **Task:** Implement a DCGAN (Deep Convolutional GAN) or cGAN.
  * **Goal:** Generate entirely synthetic/original image data (e.g., fake urban satellite tiles).
  * **Requirements:** You need to build a Generator and Discriminator, implement Adversarial loss (Minimax), and handle training challenges like mode collapse.
* **Unit 5 (Diffusion Models) & PRACT 5:**
  * **Task:** Implement a Denoising Diffusion Probabilistic Model (DDPM).
  * **Goal:** Build the forward diffusion process (adding noise) and reverse process (denoising/generation) to generate diverse outputs, potentially from text prompts.

---

## 3. Datasets Used

The project currently relies on two well-known remote sensing datasets. If you are cloning the repo on a new machine, you will need to download and place these in the parent directory (relative to the `backend/` folder).

### Dataset 1: UC Merced Land Use Dataset
* **Used for:** Autoencoder (Denoising) and Transformer (Classification).
* **Details:** 21 classes of urban/land-use images (e.g., agricultural, airplane, buildings, freeway).
* **Direct Download Link:** [http://weegee.vision.ucmerced.edu/datasets/landuse.html](http://weegee.vision.ucmerced.edu/datasets/landuse.html) (Download the ZIP file and extract it so the path `../UCMerced_LandUse/Images` exists).

### Dataset 2: EuroSAT
* **Used for:** Variational Autoencoder (VAE).
* **Details:** 10 classes of Sentinel-2 satellite images.
* **Direct Download Link:** [https://github.com/phelber/EuroSAT](https://github.com/phelber/EuroSAT) (RGB version). Can also be downloaded directly via Torchvision `torchvision.datasets.EuroSAT`.

---

## 4. Next Steps for the Teammate

1. **Download Datasets:** Use the links above and place them in the root folder alongside `backend` and `frontend`.
2. **Review Existing Models:** Check `backend/models/` to see how the PyTorch modules are structured.
3. **Start on GANs:** Create a new file `backend/models/gan.py` to start implementing the DCGAN required for Unit 3.
4. **Wire up the UI:** Once the GAN is trained, add an endpoint in `api.py` and create a frontend page to visualize the Generator's fake image outputs.
