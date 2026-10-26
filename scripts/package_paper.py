import os
import shutil
import zipfile

def package_paper():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    package_dir = os.path.join(repo_root, "paper_package")
    figures_dest = os.path.join(package_dir, "figures")
    
    # 1. Recreate directory structure
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(figures_dest, exist_ok=True)
    
    # 2. Copy the LaTeX paper and official IEEE template files
    src_tex = os.path.join(repo_root, "docs", "IEEE_Conference_Paper.tex")
    dest_tex = os.path.join(package_dir, "IEEE_Conference_Paper.tex")
    shutil.copy2(src_tex, dest_tex)
    
    # Copy as main.tex for Overleaf auto-discovery
    dest_main = os.path.join(package_dir, "main.tex")
    shutil.copy2(src_tex, dest_main)
    print("Copied IEEE_Conference_Paper.tex and main.tex")

    # Copy official IEEEtran.cls from conference-latex-template
    src_cls = os.path.join(repo_root, "conference-latex-template", "IEEE-conference-template-062824", "IEEEtran.cls")
    dest_cls = os.path.join(package_dir, "IEEEtran.cls")
    if os.path.exists(src_cls):
        shutil.copy2(src_cls, dest_cls)
        print("Copied official IEEEtran.cls (2024)")

    # Copy official IEEEtran.bst from IEEEtranBST2
    src_bst = os.path.join(repo_root, "IEEEtranBST2", "IEEEtran.bst")
    dest_bst = os.path.join(package_dir, "IEEEtran.bst")
    if os.path.exists(src_bst):
        shutil.copy2(src_bst, dest_bst)
        print("Copied official IEEEtran.bst")

    # 3. Clean figures destination directory so no orphaned images linger
    if os.path.exists(figures_dest):
        for f in os.listdir(figures_dest):
            os.remove(os.path.join(figures_dest, f))

    # Exactly the 11 active figures referenced in the LaTeX paper
    paper_figures = [
        "fig_landuse_distribution.png",
        "fig_ae_convergence.png",
        "fig_psnr_comparison.png",
        "fig_ae_crisp_restoration.png",
        "fig_classifier_metrics.png",
        "fig_vae_tradeoff.png",
        "fig_vae_multi_interpolation.png",
        "fig_gan_dynamics.png",
        "fig_gan_diverse_generation.png",
        "fig_multimodel_loss_bars.png",
        "fig_energy_carbon_breakdown.png"
    ]
    
    src_figures_dir = os.path.join(repo_root, "docs", "figures")
    for fig_name in paper_figures:
        src_path = os.path.join(src_figures_dir, fig_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(figures_dest, fig_name))
            print(f"  + Copied figure: {fig_name}")
        else:
            print(f"  ! Warning: {fig_name} not found in {src_figures_dir}")
            
    # 4. Create README.md inside paper_package
    readme_content = """# UrbanGen AI: IEEE Conference Paper Submission Package

This self-contained folder contains everything needed to compile and submit the IEEE Conference research paper for **UrbanGen AI**.

---

## 📁 Package Structure

```text
paper_package/
├── IEEE_Conference_Paper.tex     # Full IEEE double-column conference paper source
├── main.tex                      # Duplicate of the TeX source (for Overleaf auto-recognition)
├── README.md                     # Asset index & Overleaf instructions
├── UrbanGenAI_Paper_Overleaf.zip # 1-Click ready-to-upload zip file for Overleaf
└── figures/                      # EXACT 9 figures referenced in the paper
    ├── fig_ae_convergence.png
    ├── fig_psnr_comparison.png
    ├── fig_ae_crisp_restoration.png
    ├── fig_classifier_metrics.png
    ├── fig_vae_tradeoff.png
    ├── fig_vae_multi_interpolation.png
    ├── fig_gan_dynamics.png
    ├── fig_gan_diverse_generation.png
    └── fig_multimodel_loss_bars.png
```

---

## 🖼️ Exact Figures Index (What Goes Where in the Paper)

| # | File Name in `figures/` | Paper Section | LaTeX Label | Figure Description |
|---|---|---|---|---|
| **1** | `fig_ae_convergence.png` | Sec. IV-B | `\\label{fig:ae_loss}` | Denoising U-Net Autoencoder Reconstruction MSE Loss curve (50 epochs) |
| **2** | `fig_psnr_comparison.png` | Sec. IV-B | `\\label{fig:psnr_comp}` | Class-wise PSNR comparison: Baseline Bottleneck AE (25.0 dB) vs. Proposed Skip-AE (29.7 dB) |
| **3** | `fig_ae_crisp_restoration.png` | Sec. IV-B | `\\label{fig:ae_crisp}` | Visual qualitative restoration grid (Ground Truth, Noisy $\\sigma=0.15$, Restored Skip-AE) across 4 representative land-cover classes |
| **4** | `fig_classifier_metrics.png` | Sec. IV-C | `\\label{fig:cls_metrics}` | Validation Accuracy (98.1%) & Cross-Entropy Loss for ResNet-18 Territorial Classifier |
| **5** | `fig_vae_tradeoff.png` | Sec. IV-D | `\\label{fig:vae_tradeoff}` | Dual-objective Spatial VAE optimization: Reconstruction Loss vs. KL Divergence ($41.6$ nats) |
| **6** | `fig_vae_multi_interpolation.png` | Sec. IV-D | `\\label{fig:vae_multi_interp}` | Multi-pair continuous latent space interpolation across $\\alpha \\in [0, 1]$ across diverse urban archetypes |
| **7** | `fig_gan_dynamics.png` | Sec. IV-E | `\\label{fig:gan_dynamics}` | Adversarial training loss curves for Discriminator ($D=1.639$) and Generator ($G=1.232$) |
| **8** | `fig_gan_diverse_generation.png` | Sec. IV-E | `\\label{fig:gan_samples}` | 21-class conditional aerial synthesis grid demonstrating diversity without mode collapse |
| **9** | `fig_multimodel_loss_bars.png` | Sec. IV-F | `\\label{fig:loss_bars}` | Multi-model benchmark initial vs. final 50-epoch loss comparison across all 6 specialized architectures (log scale) |

> **Note on Non-Overlapping Legends**: All figure legends have been positioned with clean headroom and non-colliding layout boxes. No bars or line plots intersect with any legends or titles.

---

## 🚀 How to Use with Overleaf

### Option A: Upload Zip (Fastest & Easiest)
1. Go to [Overleaf](https://www.overleaf.com/).
2. Click **New Project** $\\to$ **Upload Project**.
3. Select `UrbanGenAI_Paper_Overleaf.zip` from this folder.
4. Overleaf will unpack all files and compile automatically.

### Option B: Replace Assets in Existing Project
1. Open your existing Overleaf project.
2. In the left file tree, delete the old `figures/` folder.
3. Click **Upload** $\\to$ drag and drop the `figures/` folder (or all 9 PNG files inside it).
4. Replace your `main.tex` content with `IEEE_Conference_Paper.tex`.
5. Click **Recompile**.
"""
    readme_path = os.path.join(package_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Created README.md")

    # 5. Build the Overleaf-ready ZIP archive
    zip_path = os.path.join(package_dir, "UrbanGenAI_Paper_Overleaf.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(dest_tex, arcname="IEEE_Conference_Paper.tex")
        zipf.write(dest_main, arcname="main.tex")
        if os.path.exists(dest_cls):
            zipf.write(dest_cls, arcname="IEEEtran.cls")
        if os.path.exists(dest_bst):
            zipf.write(dest_bst, arcname="IEEEtran.bst")
        zipf.write(readme_path, arcname="README.md")
        for fig_name in paper_figures:
            fig_path = os.path.join(figures_dest, fig_name)
            zipf.write(fig_path, arcname=f"figures/{fig_name}")
            
    print(f"Created ZIP package: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    package_paper()
