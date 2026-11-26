# 📦 UrbanGen AI — Practical Submission Package (Moodle / IA & CA)

**Course:** Generative Artificial Intelligence (`2304422L`)  
**Department:** Computer Engineering, MIT Academy of Engineering, Pune  
**Project Title:** UrbanGen AI — Edge-Deployable Multi-Model Generative Framework for Aerial Remote Sensing and Municipal Urban Planning  

| Student Name | PRN Number |
| :--- | :--- |
| **Abhay Bhise** | `202402040016` |
| **Vedant Ingle** | `202402040031` |
| **Disha** | `202402040019` |
| **Vaishnavi** | `202402040006` |

- **GitHub Repository:** https://github.com/AbhayBhise/Urban-GenAI  
- **Live Frontend (Vercel):** https://urbangen-ai.vercel.app  
- **Live Backend API (Render):** https://urban-genai.onrender.com  
- **Presentation (PPT):** [`../UrbanGen_AI_External_Exam_Phase1_Presentation.pptx`](../UrbanGen_AI_External_Exam_Phase1_Presentation.pptx)

---

## 📁 Folder Contents

| Item | Path | Purpose |
| :--- | :--- | :--- |
| **AE Colab Notebook** | [`notebooks/01_Denoising_Autoencoder_AE.ipynb`](notebooks/01_Denoising_Autoencoder_AE.ipynb) | Data loading, training (50 epochs), PSNR/MSE evaluation, anomaly maps |
| **VAE Colab Notebook** | [`notebooks/02_Spatial_VAE.ipynb`](notebooks/02_Spatial_VAE.ipynb) | Data loading, β-VAE ELBO training, latent interpolation, MSE anomaly heatmap |
| **MiniGPT Colab Notebook** | [`notebooks/03_MiniGPT_Transformer.ipynb`](notebooks/03_MiniGPT_Transformer.ipynb) | Corpus prep, char-level Transformer training, loss curves, policy generation |
| **Comparative Analysis** | [`COMPARATIVE_ANALYSIS.md`](COMPARATIVE_ANALYSIS.md) | 3-module comparison (AE, VAE, MiniGPT) + 2-model quantitative table for PPT |
| **Dataset Links & Corpus** | [`dataset_info/DATASET_LINKS.md`](dataset_info/DATASET_LINKS.md) | UCMerced LandUse (Hugging Face / Kaggle) + local `urban_planning.txt` (241 KB) |
| **Model Checkpoint Links** | [`model_links/MODEL_CHECKPOINTS.md`](model_links/MODEL_CHECKPOINTS.md) | Direct links to trained `model.pth` weights on GitHub (Git LFS) |

---

## 📄 How to Export `.ipynb` to `.pdf` for Moodle Upload

The submission instructions require both `.ipynb` and `.pdf` formats for each notebook:

1. Open [Google Colab](https://colab.research.google.com/) → **File → Upload notebook** → select each `.ipynb` from `submission/notebooks/`.
2. *(Optional)* Select **Runtime → Change runtime type → T4 GPU** and click **Runtime → Run all** to populate cell outputs.
3. Click **File → Print** (or `Ctrl + P`) → set **Destination** to **Save as PDF** → save alongside the `.ipynb` file.
4. Upload both the `.ipynb` and `.pdf` files to Moodle.
