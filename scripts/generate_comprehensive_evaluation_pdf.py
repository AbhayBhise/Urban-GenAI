"""
UrbanGen AI - Comprehensive Model Performance Guide and Acronym Glossary PDF Generator
Generates a publication-grade, human-readable PDF document using headless Chrome.
"""

import os
import sys
import subprocess
import base64

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/svg+xml" if ext == ".svg" else "image/jpeg"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def build_html():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    figures_dir = os.path.join(workspace, "docs", "poster", "figures")
    
    logo_base64 = get_base64_image(os.path.join(figures_dir, "mit_aoe_logo.png"))
    logo_img_tag = f"<img src='{logo_base64}' alt='MIT AOE Logo' />" if logo_base64 else "<div style='font-weight:bold; font-size:13pt; color:#1e3a8a;'>MIT ACADEMY OF ENGINEERING</div>"

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>UrbanGen AI: Deep Generative Architecture Evaluation & Master Glossary</title>
<style>
  @page {
    size: A4 portrait;
    margin: 7mm 9mm 7mm 9mm;
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    line-height: 1.3;
    font-size: 7.6pt;
    margin: 0;
    padding: 0;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 3px;
    letter-spacing: -0.015em;
  }

  h1 { font-size: 13pt; line-height: 1.2; color: #1e3a8a; }
  h2 { 
    font-size: 9.8pt; 
    border-bottom: 1.5px solid #2563eb; 
    padding-bottom: 2px; 
    margin-top: 6px; 
    margin-bottom: 4px;
    color: #1e3a8a;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  h3 { font-size: 8.5pt; color: #1e293b; margin-top: 5px; margin-bottom: 2px; font-weight: 700; }
  h4 { font-size: 7.6pt; color: #334155; margin-top: 3px; margin-bottom: 2px; }

  p {
    margin: 0 0 3px 0;
    text-align: justify;
  }

  .page-container {
    height: 283mm;
    max-height: 283mm;
    position: relative;
    box-sizing: border-box;
    page-break-after: always;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }
  .page-container:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }

  .page-content {
    flex: 1;
  }

  .page-footer {
    border-top: 1px solid #cbd5e1;
    padding-top: 2px;
    font-size: 6.5pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
  }

  /* Header Card */
  .doc-header {
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 5px 8px;
    background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
    margin-bottom: 5px;
  }

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-bottom: 3px;
  }

  .logo-box img {
    height: 30px;
    object-fit: contain;
  }

  .inst-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
  }
  .inst-sub {
    font-size: 6.5pt;
    color: #475569;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: 1.3fr 1.7fr;
    gap: 5px;
    font-size: 6.8pt;
    margin-top: 2px;
  }

  .meta-col {
    background: #ffffff;
    padding: 3px 5px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }

  /* Pill badges */
  .badge {
    display: inline-block;
    padding: 1px 4px;
    font-size: 6.2pt;
    font-weight: 700;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .badge-blue { background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
  .badge-green { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
  .badge-purple { background-color: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }
  .badge-amber { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
  .badge-red { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 6.6pt;
    line-height: 1.25;
    margin-bottom: 4px;
  }
  th, td {
    padding: 2.5px 4.5px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }
  th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  /* Callout boxes */
  .callout {
    border-left: 3px solid #2563eb;
    background-color: #f8fafc;
    padding: 4px 6px;
    margin: 4px 0;
    border-radius: 0 3px 3px 0;
    font-size: 7.2pt;
  }
  .callout-warning {
    border-left-color: #dc2626;
    background-color: #fef2f2;
  }
  .callout-success {
    border-left-color: #16a34a;
    background-color: #f0fdf4;
  }
  .callout-purple {
    border-left-color: #9333ea;
    background-color: #faf5ff;
  }

  .model-card {
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 4px 6px;
    margin-bottom: 4px;
    background: #ffffff;
  }
  .model-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
    margin-bottom: 2px;
  }

  .metric-row {
    display: flex;
    gap: 3px;
    margin: 1.5px 0;
    flex-wrap: wrap;
  }
  .metric-pill {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    padding: 1px 3px;
    border-radius: 3px;
    font-size: 6.4pt;
    font-weight: 600;
  }
  .metric-pill.success { background: #dcfce7; border-color: #86efac; color: #166534; }
  .metric-pill.info { background: #dbeafe; border-color: #93c5fd; color: #1e40af; }
  .metric-pill.purple { background: #f3e8ff; border-color: #d8b4fe; color: #6b21a8; }
  .metric-pill.amber { background: #fef3c7; border-color: #fde68a; color: #92400e; }

  code {
    font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
    font-size: 6.8pt;
    background-color: #f1f5f9;
    padding: 1px 2.5px;
    border-radius: 2px;
    color: #0f172a;
  }

  .formula-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 2px 4px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 6.4pt;
    color: #1e3a8a;
    margin: 2px 0;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4px;
  }
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PAGE 1: TITLE, CRITICAL DISTINCTION & RANKING -->
<!-- ========================================== -->
<div class="page-container">
  <div class="page-content">
    <div class="doc-header">
      <div class="header-top">
        <div class="logo-box">
          __LOGO_TAG__
        </div>
        <div style="text-align: right;">
          <div class="inst-title">MIT Academy of Engineering, Pune</div>
          <div class="inst-sub">An Autonomous Institute Affiliated to Savitribai Phule Pune University &bull; Dept. of Computer Engineering</div>
          <div class="inst-sub">B.Tech Capstone Project (60 Marks) &bull; IEEE Conference Publication Track</div>
        </div>
      </div>
      <div style="text-align: center; margin: 2px 0 3px 0;">
        <h1 style="margin: 0; font-size: 12.5pt; color: #1e3a8a;">UrbanGen AI: Deep Generative Architecture Evaluation & Viva Defense Dossier</h1>
        <div style="font-size: 7.2pt; color: #475569; font-weight: 500;">
          A Multi-Model Comparative Benchmark, Architectural Dossiers & Complete Technical Acronym Encyclopedia
        </div>
      </div>
      <div class="meta-grid">
        <div class="meta-col">
          <strong>Project Guides:</strong><br>
          &bull; <strong>Prof. Savita Mane</strong> (Asst. Prof., Dept. of Computer Eng.)<br>
          &bull; <strong>Prof. Pramod Ganjewar</strong> (Asst. Prof., Dept. of Computer Eng.)
        </div>
        <div class="meta-col">
          <strong>Candidate Research Engineers:</strong><br>
          &bull; <strong>Abhay Bhise</strong> (202201040024) &bull; <strong>Disha Satpute</strong> (202201040027)<br>
          &bull; <strong>Vaishnavi Phad</strong> (202201040033) &bull; <strong>Vedant Ingle</strong> (202201040065)
        </div>
      </div>
    </div>

    <div class="callout callout-warning">
      <strong style="color: #991b1b; font-size: 7.8pt;">CRITICAL VIVA DISTINCTION: Discriminative Classifier vs. True Generative AI Models</strong><br>
      <strong>Why Model 3 (ResNet-18) is NOT our Best Generative Model:</strong><br>
      Although ResNet-18 achieves the highest numerical accuracy in the project (<strong>98.10% Validation Accuracy</strong>, Macro F1: 0.9784), ResNet-18 is a <em>standard supervised discriminative convolutional neural network</em> (He et al., 2015), <strong>NOT a Generative AI architecture</strong>. In UrbanGen AI, ResNet-18 acts strictly as an <strong>Auxiliary Frozen Semantic Auditor</strong> to verify whether synthetic satellite tiles synthesized by cDCGAN and DDPM accurately reflect intended municipal zoning geometry. If asked by an external examiner: <em>"Which of your Generative AI models performs the best?"</em>, answering ResNet-18 is technically incorrect and will result in grade penalties.
    </div>

    <h2>1. Definitive Ranking: True Generative AI Champions by Category</h2>
    <p>
      Among the 5 true Generative AI architectures evaluated (DAE, Spatial &beta;-VAE, Residual cDCGAN, Conditional DDPM, and MiniGPT), performance must be assessed across specific generative tasks. Here are the champion models ranked by their empirical results:
    </p>

    <div class="grid-2">
      <!-- cDCGAN -->
      <div class="model-card" style="border-top: 2.5px solid #16a34a;">
        <div class="model-card-header">
          <div><strong>1. Best Generative Class Fidelity & Synthesis Speed</strong></div>
          <span class="badge badge-green">Champion: cDCGAN</span>
        </div>
        <div style="font-size: 6.8pt; margin-bottom: 2px;"><strong>Architecture:</strong> Residual Conditional DCGAN (4 ResUpBlocks + Projection D)</div>
        <div class="metric-row">
          <span class="metric-pill success">&uarr; 99.40% Semantic Proxy Rec</span>
          <span class="metric-pill info">&darr; 32 ms Latency (Realtime Edge)</span>
          <span class="metric-pill">Minimax: D=1.67, G=1.19</span>
        </div>
        <p style="font-size: 6.8pt; margin-top: 2px;">
          <strong>Why it Wins:</strong> Out of 168 synthetic aerial tiles generated across all 21 zoning classes, <strong>167 were independently verified</strong> by our frozen auditor as true to class. It runs <strong>56&times; faster than diffusion</strong>, enabling real-time edge synthesis under 35 ms.
        </p>
      </div>

      <!-- DAE -->
      <div class="model-card" style="border-top: 2.5px solid #2563eb;">
        <div class="model-card-header">
          <div><strong>2. Best Quantitative Signal Restoration & Fidelity</strong></div>
          <span class="badge badge-blue">Champion: U-Net DAE</span>
        </div>
        <div style="font-size: 6.8pt; margin-bottom: 2px;"><strong>Architecture:</strong> Skip-Connected U-Net Autoencoder (Stem, L1, L2, L3)</div>
        <div class="metric-row">
          <span class="metric-pill success">&uarr; 29.65 dB PSNR (+7.0 dB Gain)</span>
          <span class="metric-pill success">&uarr; 0.8649 SSIM</span>
          <span class="metric-pill info">&darr; 0.00449 MSE Loss</span>
        </div>
        <p style="font-size: 6.8pt; margin-top: 2px;">
          <strong>Why it Wins:</strong> Lowest pixel-level reconstruction error in the suite. Transposed skip connections bypass the spatial bottleneck to restore high-frequency orthogonal road grids and parcel lines lost during atmospheric haze (&sigma;=0.15).
        </p>
      </div>
    </div>

    <div class="grid-3" style="margin-top: 3px;">
      <!-- DDPM -->
      <div class="model-card" style="border-top: 2.5px solid #dc2626;">
        <div class="model-card-header">
          <div><strong>3. Best Visual Realism</strong></div>
          <span class="badge badge-red">DDPM (Diffusion)</span>
        </div>
        <div class="metric-row">
          <span class="metric-pill info">&darr; 0.0304 Noise MSE</span>
          <span class="metric-pill">&darr; 1.82s (20e DDIM)</span>
        </div>
        <p style="font-size: 6.6pt; margin-top: 2px;">
          Highest visual sharpness and zero mode collapse. Reverse Markov chain yields pristine structural boundaries; accelerated 15.6&times; via DDIM.
        </p>
      </div>

      <!-- MiniGPT -->
      <div class="model-card" style="border-top: 2.5px solid #9333ea;">
        <div class="model-card-header">
          <div><strong>4. Best Language Precision</strong></div>
          <span class="badge badge-purple">MiniGPT Causal</span>
        </div>
        <div class="metric-row">
          <span class="metric-pill purple">&darr; 1.110 Perplexity</span>
          <span class="metric-pill info">&darr; 0.1505 Bits/Char</span>
        </div>
        <p style="font-size: 6.6pt; margin-top: 2px;">
          Near-zero uncertainty on legal municipal planning mandates. 4-layer Pre-LayerNorm Causal Transformer grounds spatial telemetry in PMC bylaws.
        </p>
      </div>

      <!-- Spatial VAE -->
      <div class="model-card" style="border-top: 2.5px solid #d97706;">
        <div class="model-card-header">
          <div><strong>5. Best Manifold & Anomaly</strong></div>
          <span class="badge badge-amber">Spatial &beta;-VAE</span>
        </div>
        <div class="metric-row">
          <span class="metric-pill info">&uarr; 27.49 dB PSNR</span>
          <span class="metric-pill">KL: 60.72 nats</span>
        </div>
        <p style="font-size: 6.6pt; margin-top: 2px;">
          Preserves 2D spatial topology in &Ropf;^(64&times;8&times;8) latent tensors. Prevents posterior collapse; detects encroachment via &gt;3&sigma; disparity.
        </p>
      </div>
    </div>

    <h2>2. Master Generative AI Performance Matrix (50 Epochs / 32 Batch)</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 17%;">Model Architecture</th>
          <th style="width: 14%;">Academic Role</th>
          <th style="width: 15%;">Primary Metric</th>
          <th style="width: 15%;">Secondary Metric</th>
          <th style="width: 15%;">Final Converged Loss</th>
          <th style="width: 24%;">Practical Advantage in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background-color: #f0fdf4;">
          <td><strong>Residual cDCGAN</strong><br><span style="font-size:6.2pt; color:#475569;">4x ResUpBlock + Proj D</span></td>
          <td>Adversarial Parcel Synthesis</td>
          <td><strong>99.40% Proxy Rec</strong> (&uarr;)</td>
          <td><strong>32 ms Latency</strong> (&darr;)</td>
          <td><code>D=1.67, G=1.19</code><br><span style="font-size:6.2pt;">Minimax Adversarial</span></td>
          <td><strong>Champion Generative Model</strong>: Fastest edge synthesis (&lt;35 ms); 99.4% class alignment without blurring.</td>
        </tr>
        <tr style="background-color: #eff6ff;">
          <td><strong>Denoising U-Net AE</strong><br><span style="font-size:6.2pt; color:#475569;">Multi-Scale Transposed Skips</span></td>
          <td>Sensor Noise Removal</td>
          <td><strong>29.65 dB PSNR</strong> (&uarr;)</td>
          <td><strong>0.8649 SSIM</strong> (&uarr;)</td>
          <td><code>0.00449 MSE</code><br><span style="font-size:6.2pt;">(Total: 0.00617)</span></td>
          <td><strong>Champion Restoration Model</strong>: +7.0 dB recovery gain over raw degraded input; crisp boundary grids.</td>
        </tr>
        <tr>
          <td><strong>Conditional DDPM</strong><br><span style="font-size:6.2pt; color:#475569;">Time- & Class-Conditioned</span></td>
          <td>Photorealistic Tile Generation</td>
          <td><strong>0.0304 Noise MSE</strong> (&darr;)</td>
          <td><strong>1.82s Sampling</strong><br><span style="font-size:6.2pt;">(20-step DDIM)</span></td>
          <td><code>0.02916 VLB</code><br><span style="font-size:6.2pt;">5-Loss Composite</span></td>
          <td><strong>Champion Photorealism</strong>: Highest structural sharpness; zero mode collapse; eliminates adversarial noise.</td>
        </tr>
        <tr>
          <td><strong>MiniGPT Causal Transf.</strong><br><span style="font-size:6.2pt; color:#475569;">4-Layer Pre-LN, T=192</span></td>
          <td>Municipal Policy Drafting</td>
          <td><strong>1.110 Perplexity</strong> (&darr;)</td>
          <td><strong>0.1505 Bits/Char</strong> (&darr;)</td>
          <td><code>0.1043 Causal CE</code><br><span style="font-size:6.2pt;">Categorical CE</span></td>
          <td><strong>Champion Text Generation</strong>: Formulates legally compliant FSI, TOD, and green-buffer mandates without hallucination.</td>
        </tr>
        <tr>
          <td><strong>Spatial &beta;-VAE</strong><br><span style="font-size:6.2pt; color:#475569;">&beta;=10^-4, 64x8x8 Latent</span></td>
          <td>Latent Space Traversal</td>
          <td><strong>27.49 dB PSNR</strong> (&uarr;)</td>
          <td><strong>60.72 nats KL</strong><br><span style="font-size:6.2pt;">(0.0148 nats/dim)</span></td>
          <td><code>0.04830 Total</code><br><span style="font-size:6.2pt;">(0.7L1 + 0.3MSE + &beta;KL)</span></td>
          <td><strong>Champion Latent Modeler</strong>: Continuous topological manifold navigation; unsupervised encroachment detection (&gt;3&sigma;).</td>
        </tr>
        <tr style="background-color: #fffbeb;">
          <td><em>Territorial ResNet-18</em><br><span style="font-size:6.2pt; color:#b45309;">(Auxiliary Evaluator)</span></td>
          <td><em>Frozen Semantic Auditor</em></td>
          <td><em>98.10% Val Acc</em> (&uarr;)</td>
          <td><em>0.9784 Macro F1</em> (&uarr;)</td>
          <td><code>0.0615 CE Loss</code><br><span style="font-size:6.2pt;">Supervised Cross-Ent.</span></td>
          <td><em>Not a GenAI model</em>. Functions purely as the independent, frozen quality judge for cDCGAN and DDPM outputs.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">
    <span>UrbanGen AI &bull; B.Tech Capstone Project 2026 &bull; MIT Academy of Engineering, Pune</span>
    <span>Page 1 of 5</span>
  </div>
</div>

<!-- ========================================== -->
<!-- PAGE 2: TECHNICAL MODEL DOSSIERS -->
<!-- ========================================== -->
<div class="page-container">
  <div class="page-content">
    <h2>3. Technical Model Dossiers: Architecture, Code Locations, Losses & Behavior</h2>

    <!-- MODEL 1 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #1e3a8a;">Model 1: Denoising Autoencoder (U-Net DAE) &bull; Signal Restoration</strong></div>
        <code>backend/models/autoencoder.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input Tensor:</strong> <code>[B, 3, 128, 128]</code> corrupted with synthetic atmospheric haze and Gaussian sensor noise (&sigma; = 0.15).</p>
          <p><strong>Architecture:</strong> ResNet-style encoder extracting hierarchical multi-scale feature maps (Stem: 64, L1: 128, L2: 256, L3: 512). These maps are bridged via direct skip connections into a 4-stage transposed convolutional decoder (512 &rarr; 256 &rarr; 128 &rarr; 64 &rarr; 32 &rarr; 3).</p>
          <div class="formula-box">
            L_AE = (1/N) &sum; || x - x_hat ||_2^2 + &lambda; &sum; ||W||_2^2 &emsp; &rarr; &emsp; <strong>Converged MSE: 0.00449</strong> (Total: 0.00617)
          </div>
        </div>
        <div>
          <p><strong>Why the Model Behaves This Way:</strong> Standard bottleneck autoencoders produce blurred aerial images (25.02 dB) because high-frequency spatial details are crushed at the bottleneck. Our U-Net skip connections allow spatial gradients to bypass the compression bottleneck, restoring razor-sharp parcel boundaries (+7.0 dB recovery gain to <strong>29.65 dB PSNR</strong> and <strong>0.8649 SSIM</strong>).</p>
          <div class="metric-row">
            <span class="metric-pill success">&uarr; PSNR: 29.65 dB (&uarr; Better)</span>
            <span class="metric-pill success">&uarr; SSIM: 0.8649 (&uarr; Better)</span>
            <span class="metric-pill info">&darr; MSE: 0.00449 (&darr; Better)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL 2 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #6b21a8;">Model 2: Spatial &beta;-VAE &bull; Latent Manifold & Anomaly Mapping</strong></div>
        <code>backend/models/vae.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input Tensor:</strong> <code>[B, 3, 128, 128]</code> normalized orthoimagery tile.</p>
          <p><strong>Architecture:</strong> Deep convolutional encoder predicting 3D spatial latent distribution parameters &mu;, log &sigma;^2 in &Ropf;^(64 &times; 8 &times; 8) to preserve 2D topological layout. Decoder features compact skips with 0.2 dropout to prevent posterior collapse.</p>
          <div class="formula-box">
            L_VAE = (0.7*L_1 + 0.3*L_MSE) + &beta; * D_KL(q(z|x) || p(z)) &emsp; (&beta; = 10^-4) &emsp; &rarr; &emsp; <strong>Final Loss: 0.04830</strong>
          </div>
        </div>
        <div>
          <p><strong>Why the Model Behaves This Way:</strong> Standard VAEs collapse (KL &rarr; 0) when trained on aerial imagery. By tuning &beta; = 10^-4, the model maintains a continuous, interpolatable latent space (<strong>KL = 60.72 nats</strong>) while reaching <strong>27.49 dB PSNR</strong>. Unsupervised illegal construction is identified whenever pixel disparity |x - x_hat| &gt; 3&sigma;.</p>
          <div class="metric-row">
            <span class="metric-pill info">&uarr; PSNR: 27.49 dB (&uarr; Better)</span>
            <span class="metric-pill">&uarr; KL: 60.72 nats (Avoids collapse)</span>
            <span class="metric-pill info">&darr; Loss: 0.04830 (&darr; Better)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL 3 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #b45309;">Model 3: Territorial Land-Use Classifier (ResNet-18) &bull; Auxiliary Evaluator</strong></div>
        <code>backend/models/classifier.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input Tensor:</strong> <code>[B, 3, 128, 128]</code> real or synthetic aerial patch.</p>
          <p><strong>Architecture:</strong> Transfer-learned ResNet-18 backbone pre-trained on ImageNet with a customized 21-class linear projection head trained via Adam (lr = 10^-4).</p>
          <div class="formula-box">
            L_CE = - &sum; y_i * log(p_i) &emsp; &rarr; &emsp; <strong>Validation Loss: 0.0615</strong> &emsp; &bull; &emsp; <strong>Val Accuracy: 98.10%</strong>
          </div>
        </div>
        <div>
          <p><strong>Why it Exists & How it is Evaluated:</strong> This model provides a frozen, objective mathematical auditor. Rather than relying on subjective human visual inspection, generated tiles from cDCGAN and DDPM are fed into this frozen classifier to calculate <strong>Semantic Proxy Recognition</strong> (99.40% for cDCGAN).</p>
          <div class="metric-row">
            <span class="metric-pill success">&uarr; Val Acc: 98.10% (&uarr; Better)</span>
            <span class="metric-pill success">&uarr; Macro F1: 0.9784 (&uarr; Better)</span>
            <span class="metric-pill info">&darr; CE Loss: 0.0615 (&darr; Better)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL 4 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #166534;">Model 4: Residual cDCGAN &bull; Class-Conditioned Adversarial Synthesis</strong></div>
        <code>backend/models/gan.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input Tensor:</strong> Latent vector z ~ N(0, I) in &Ropf;^100 concatenated with 21-class one-hot zoning condition y in [0 .. 20].</p>
          <p><strong>Architecture:</strong> 4x ResUpBlock Generator with conditional batch normalization. Discriminator employs Spectral Normalization (SN), Projection Conditioning, and an AC-GAN classification head.</p>
          <div class="formula-box">
            L_G = L_adv + 0.8*L_AC + 1.2*L_semantic &emsp; &rarr; &emsp; <strong>Minimax Equilibrium: D = 1.672, G = 1.189</strong>
          </div>
        </div>
        <div>
          <p><strong>Why the Model Behaves This Way:</strong> Aerial datasets risk severe mode collapse due to repetitive rural and forest patterns. Spectral Normalization constrains the Lipschitz constant of D, while projection conditioning forces G to generate distinct architectural features (runways, storage tanks, dense housing) in just <strong>32 ms</strong>.</p>
          <div class="metric-row">
            <span class="metric-pill success">&uarr; Proxy Rec: 99.40% (&uarr; Better)</span>
            <span class="metric-pill success">&darr; Latency: 32 ms (&darr; Better)</span>
            <span class="metric-pill">Zero Mode Collapse</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL 5 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #991b1b;">Model 5: Conditional DDPM &bull; Probabilistic Diffusion Synthesis</strong></div>
        <code>backend/models/diffusion.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input Tensor:</strong> Gaussian noise x_T ~ N(0, I) conditioned on timestep t in [1, 1000] and class label y in [0 .. 20].</p>
          <p><strong>Architecture:</strong> Time- and class-conditioned U-Net with sinusoidal positional embeddings, multi-head self-attention, and classifier guidance.</p>
          <div class="formula-box">
            L_simple(&theta;) = E_{t, x_0, &epsilon;} [ || &epsilon; - &epsilon;_&theta;(x_t, t, c) ||^2 ] &emsp; &rarr; &emsp; <strong>Noise MSE: 0.03040</strong> &emsp; &bull; &emsp; <strong>VLB Loss: 0.02916</strong>
          </div>
        </div>
        <div>
          <p><strong>Why the Model Behaves This Way:</strong> Unlike GANs that optimize an adversarial min-max game, DDPM directly learns the score of the data distribution via reverse stochastic differential equations. This eliminates artifacting, yielding pristine photorealism. Accelerated via 20-step deterministic DDIM from 28.4s down to <strong>1.82s</strong>.</p>
          <div class="metric-row">
            <span class="metric-pill info">&darr; Noise MSE: 0.0304 (&darr; Better)</span>
            <span class="metric-pill info">&darr; VLB Loss: 0.02916 (&darr; Better)</span>
            <span class="metric-pill success">&darr; DDIM: 1.82s (15.6x Speedup)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL 6 -->
    <div class="model-card">
      <div class="model-card-header">
        <div><strong style="color: #4338ca;">Model 6: Urban Plan Generator (MiniGPT) &bull; Causal Policy Drafting</strong></div>
        <code>backend/models/minigpt.py</code>
      </div>
      <div class="grid-2">
        <div>
          <p><strong>Input:</strong> Tokenized urban spatial telemetry (zoning category, FSI target, road hierarchy, green buffer constraint).</p>
          <p><strong>Architecture:</strong> 4-layer Pre-LayerNorm Causal Transformer (d_model = 256, 4 attention heads, context T = 192) trained from scratch on municipal urban planning mandates.</p>
          <div class="formula-box">
            L_causal = - &sum; log P(w_t | w_&lt;t) &emsp; &rarr; &emsp; <strong>Validation Loss: 0.1043</strong> &emsp; &bull; &emsp; <strong>Validation Perplexity: 1.110</strong>
          </div>
        </div>
        <div>
          <p><strong>Why the Model Behaves This Way:</strong> The model achieves near-theoretical perplexity (<strong>1.110 PPL</strong> and <strong>0.1505 Bits/Char</strong>) because municipal bylaws utilize rigorous, structured legal vocabularies. It reliably outputs actionable FSI calculations (1.8 to 2.4) and transit setbacks without hallucinations.</p>
          <div class="metric-row">
            <span class="metric-pill success">&darr; Perplexity: 1.110 (&darr; Better)</span>
            <span class="metric-pill success">&darr; BPC: 0.1505 (&darr; Better)</span>
            <span class="metric-pill info">&darr; CE Loss: 0.1043 (&darr; Better)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="page-footer">
    <span>UrbanGen AI &bull; B.Tech Capstone Project 2026 &bull; MIT Academy of Engineering, Pune</span>
    <span>Page 2 of 5</span>
  </div>
</div>

<!-- ========================================== -->
<!-- PAGE 3: MASTER ACRONYM GLOSSARY PART 1 -->
<!-- ========================================== -->
<div class="page-container">
  <div class="page-content">
    <h2>4. Master Acronym & Full Form Glossary with Technical Definitions (Part 1)</h2>
    <p>
      This master encyclopedia provides complete full forms, definitions, and project-specific contexts for every abbreviation in UrbanGen AI.
    </p>

    <h3>4.1 Deep Generative Models & Neural Network Architectures</h3>
    <table>
      <thead>
        <tr>
          <th style="width: 13%;">Acronym</th>
          <th style="width: 26%;">Complete Full Form</th>
          <th style="width: 36%;">Plain-English Meaning & Definition</th>
          <th style="width: 25%;">Specific Role in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>GAN</strong></td>
          <td>Generative Adversarial Network</td>
          <td>A neural framework where two networks (Generator and Discriminator) compete in a game-theoretic minimax dynamic.</td>
          <td>Foundational concept for Model 4 to synthesize realistic aerial tiles from random noise vectors.</td>
        </tr>
        <tr>
          <td><strong>DCGAN</strong></td>
          <td>Deep Convolutional Generative Adversarial Network</td>
          <td>A GAN architecture utilizing all-convolutional downsampling and transposed convolutional upsampling layers.</td>
          <td>Provides spatial stability and avoids checkerboard artifacts during aerial tile synthesis.</td>
        </tr>
        <tr>
          <td><strong>cDCGAN</strong></td>
          <td>Conditional Deep Convolutional Generative Adversarial Network</td>
          <td>A DCGAN conditioned on auxiliary label information (such as municipal zoning classes) to steer output synthesis.</td>
          <td><strong>Model 4</strong>: Generates class-specific satellite imagery tiles (e.g. airport, residential, commercial).</td>
        </tr>
        <tr>
          <td><strong>AE / DAE</strong></td>
          <td>Autoencoder / Denoising Autoencoder</td>
          <td>A self-supervised neural network trained to reconstruct uncorrupted clean inputs from noise-injected degraded inputs.</td>
          <td><strong>Model 1</strong>: Restores satellite imagery corrupted by atmospheric cloud haze and sensor noise.</td>
        </tr>
        <tr>
          <td><strong>VAE</strong></td>
          <td>Variational Autoencoder</td>
          <td>A directed probabilistic generative model that encodes inputs into a continuous statistical latent distribution (mean and variance).</td>
          <td>Enables smooth semantic interpolation between distinct land-use categories.</td>
        </tr>
        <tr>
          <td><strong>&beta;-VAE</strong></td>
          <td>Beta Variational Autoencoder</td>
          <td>A modified VAE with an adjustable hyperparameter (&beta;) balancing reconstruction fidelity against latent disentanglement.</td>
          <td><strong>Model 2</strong>: Uses &beta; = 10^-4 to maintain sharp 27.49 dB spatial reconstruction while avoiding posterior collapse.</td>
        </tr>
        <tr>
          <td><strong>DDPM</strong></td>
          <td>Denoising Diffusion Probabilistic Models</td>
          <td>A generative paradigm that generates images by learning the iterative reverse denoising steps of a Markov chain.</td>
          <td><strong>Model 5</strong>: Synthesizes high-fidelity satellite imagery with zero mode collapse and pristine boundary sharpness.</td>
        </tr>
        <tr>
          <td><strong>DDIM</strong></td>
          <td>Denoising Diffusion Implicit Models</td>
          <td>A deterministic, non-Markovian sampling acceleration technique for trained diffusion models.</td>
          <td>Accelerates Model 5 inference from 1,000 steps (28.4s) down to 20 steps (<strong>1.82s</strong>, a 15.6x speedup).</td>
        </tr>
        <tr>
          <td><strong>GPT</strong></td>
          <td>Generative Pre-trained Transformer</td>
          <td>An autoregressive causal attention-based transformer that models sequential probability distributions over tokens.</td>
          <td><strong>Model 6 (MiniGPT)</strong>: Formulates textual municipal zoning bylaws, FSI, and environmental policies.</td>
        </tr>
        <tr>
          <td><strong>CNN</strong></td>
          <td>Convolutional Neural Network</td>
          <td>A neural network that uses shift-invariant convolution filters to extract hierarchical spatial patterns from 2D images.</td>
          <td>Core spatial backbone across all vision models in the UrbanGen framework.</td>
        </tr>
        <tr>
          <td><strong>U-Net</strong></td>
          <td>U-shaped Neural Network</td>
          <td>An encoder-decoder network featuring direct multi-scale skip connections between contracting and expanding paths.</td>
          <td>Powers Model 1 (DAE) and Model 5 (DDPM) to preserve exact parcel boundaries and road vectors.</td>
        </tr>
        <tr>
          <td><strong>ResNet</strong></td>
          <td>Deep Residual Network</td>
          <td>A network architecture introducing identity shortcut connections to solve vanishing gradients in deep networks.</td>
          <td>Powers Model 3 (Land-Use Classifier) and forms the residual blocks inside cDCGAN and Spatial &beta;-VAE.</td>
        </tr>
      </tbody>
    </table>

    <h3>4.2 Mathematical Formulations & Evaluation Metrics</h3>
    <table>
      <thead>
        <tr>
          <th style="width: 13%;">Acronym</th>
          <th style="width: 26%;">Complete Full Form</th>
          <th style="width: 36%;">Plain-English Meaning & Definition</th>
          <th style="width: 25%;">Optimization Goal in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>PSNR</strong></td>
          <td>Peak Signal-to-Noise Ratio</td>
          <td>The ratio (measured in logarithmic decibels, dB) between the maximum possible pixel power and corrupting noise power.</td>
          <td><strong>&uarr; Higher is better</strong>: Model 1 achieves <strong>29.65 dB</strong> (+7.0 dB gain over degraded input).</td>
        </tr>
        <tr>
          <td><strong>SSIM</strong></td>
          <td>Structural Similarity Index Measure</td>
          <td>A perceptual metric (scale -1 to +1) evaluating luminance, contrast, and structural covariance between two images.</td>
          <td><strong>&uarr; Higher is better</strong>: Model 1 achieves <strong>0.8649</strong>, proving road networks remain orthogonal and crisp.</td>
        </tr>
        <tr>
          <td><strong>MSE</strong></td>
          <td>Mean Squared Error</td>
          <td>The average squared Euclidean difference between predicted pixel values and ground-truth values.</td>
          <td><strong>&darr; Lower is better</strong>: Model 1 minimizes reconstruction error down to <strong>0.00449</strong>.</td>
        </tr>
        <tr>
          <td><strong>KL Div.</strong></td>
          <td>Kullback-Leibler Divergence (D_KL)</td>
          <td>A statistical measure of relative entropy quantifying the divergence of the approximate posterior from the prior distribution.</td>
          <td><strong>Balanced optimization</strong>: Reaches <strong>60.72 nats</strong> in Model 2, confirming latent space is actively used.</td>
        </tr>
        <tr>
          <td><strong>VLB / ELBO</strong></td>
          <td>Variational Lower Bound / Evidence Lower Bound</td>
          <td>A mathematical lower bound on the log marginal likelihood of the data distribution optimized in VAEs and DDPM.</td>
          <td><strong>&darr; Lower is better</strong> (in negative loss form): Model 5 achieves <strong>0.02916</strong> converged VLB loss.</td>
        </tr>
        <tr>
          <td><strong>PPL</strong></td>
          <td>Perplexity</td>
          <td>The exponentiated cross-entropy of a language model, measuring its branching uncertainty when predicting the next word.</td>
          <td><strong>&darr; Lower is better</strong>: Model 6 reaches <strong>1.110</strong> (theoretical perfection is 1.0), indicating near-certain legal accuracy.</td>
        </tr>
        <tr>
          <td><strong>BPC</strong></td>
          <td>Bits Per Character</td>
          <td>The average number of binary bits required to encode each text character under the model's probability distribution.</td>
          <td><strong>&darr; Lower is better</strong>: Model 6 scores <strong>0.1505 BPC</strong>, confirming dense domain vocabulary retention.</td>
        </tr>
        <tr>
          <td><strong>CE / CCE</strong></td>
          <td>Cross-Entropy / Causal Cross-Entropy</td>
          <td>Loss function measuring the difference between true categorical probability distributions and model softmax predictions.</td>
          <td><strong>&darr; Lower is better</strong>: Minimized in Model 3 (0.0615) and Model 6 (0.1043).</td>
        </tr>
        <tr>
          <td><strong>Macro F1</strong></td>
          <td>Macro-Averaged F1 Score</td>
          <td>The unweighted harmonic mean of Precision and Recall calculated independently across all 21 classes.</td>
          <td><strong>&uarr; Higher is better</strong>: Model 3 achieves <strong>0.9784</strong>, proving minority zoning classes are classified fairly.</td>
        </tr>
        <tr>
          <td><strong>EMA</strong></td>
          <td>Exponential Moving Average</td>
          <td>A running average of neural network weights updated with an exponential decay factor (e.g. 0.999).</td>
          <td>Stabilizes generator weights in cDCGAN and DDPM, suppressing training spikes.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">
    <span>UrbanGen AI &bull; B.Tech Capstone Project 2026 &bull; MIT Academy of Engineering, Pune</span>
    <span>Page 3 of 5</span>
  </div>
</div>

<!-- ========================================== -->
<!-- PAGE 4: MASTER ACRONYM GLOSSARY PART 2 -->
<!-- ========================================== -->
<div class="page-container">
  <div class="page-content">
    <h2>4. Master Acronym & Full Form Glossary with Technical Definitions (Part 2)</h2>

    <h3>4.3 Remote Sensing, GIS & Urban Planning Terminology</h3>
    <table>
      <thead>
        <tr>
          <th style="width: 13%;">Acronym</th>
          <th style="width: 26%;">Complete Full Form</th>
          <th style="width: 36%;">Plain-English Meaning & Definition</th>
          <th style="width: 25%;">Application in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>GIS</strong></td>
          <td>Geographic Information System</td>
          <td>A computer system for capturing, storing, checking, and displaying data related to positions on Earth's surface.</td>
          <td>The spatial operational environment that consumes UrbanGen AI's restored and synthesized satellite rasters.</td>
        </tr>
        <tr>
          <td><strong>GSD</strong></td>
          <td>Ground Sample Distance</td>
          <td>The physical distance on the ground represented by the width of a single image pixel.</td>
          <td>Our benchmark dataset (UCMerced) has a <strong>0.3m GSD</strong> (1 pixel represents 30 cm &times; 30 cm on the ground).</td>
        </tr>
        <tr>
          <td><strong>USGS</strong></td>
          <td>United States Geological Survey</td>
          <td>A scientific agency that produces high-resolution public Earth observation orthophoto collections.</td>
          <td>Original aerial imagery source used in the standardized 21-class UCMerced Land-Use benchmark.</td>
        </tr>
        <tr>
          <td><strong>UCMerced</strong></td>
          <td>University of California, Merced Dataset</td>
          <td>A standardized land-use benchmark containing 2,100 aerial orthoimages divided into 21 distinct urban/rural classes.</td>
          <td>The primary ground-truth benchmark corpus across all 6 models in this capstone.</td>
        </tr>
        <tr>
          <td><strong>FSI / FAR</strong></td>
          <td>Floor Space Index / Floor Area Ratio</td>
          <td>The ratio of total built-up floor area of a building to the total gross area of the land parcel it occupies.</td>
          <td>Model 6 calculates and outputs zoning-compliant FSI recommendations (e.g., FSI 1.8 to 2.4).</td>
        </tr>
        <tr>
          <td><strong>TOD</strong></td>
          <td>Transit-Oriented Development</td>
          <td>An urban planning strategy maximizing residential and commercial space within walking distance of public transit.</td>
          <td>MiniGPT formulates specific TOD corridors and transit setbacks based on generated spatial parcel maps.</td>
        </tr>
        <tr>
          <td><strong>PMC</strong></td>
          <td>Pune Municipal Corporation</td>
          <td>The local municipal governing body responsible for urban planning and bylaws in Pune, Maharashtra.</td>
          <td>Provides the empirical legal planning bylaws on which Model 6 was specialized.</td>
        </tr>
        <tr>
          <td><strong>DEM</strong></td>
          <td>Digital Elevation Model</td>
          <td>A 3D computer graphics representation of terrain elevation surface data.</td>
          <td>Integrated in GIS pipelines to calculate watershed and runoff percolation corridors.</td>
        </tr>
      </tbody>
    </table>

    <h3>4.4 Hardware Acceleration, Green AI & Computing Infrastructure</h3>
    <table>
      <thead>
        <tr>
          <th style="width: 13%;">Acronym</th>
          <th style="width: 26%;">Complete Full Form</th>
          <th style="width: 36%;">Plain-English Meaning & Definition</th>
          <th style="width: 25%;">Application in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>TGP</strong></td>
          <td>Total Graphics Power</td>
          <td>The maximum electrical wattage that a graphics card is designed to consume under peak operational workload.</td>
          <td>Our NVIDIA RTX 4050 Laptop GPU operates under a strictly capped <strong>75W TGP</strong> envelope.</td>
        </tr>
        <tr>
          <td><strong>VRAM</strong></td>
          <td>Video Random Access Memory</td>
          <td>High-speed onboard memory dedicated exclusively to GPU tensor buffers and model parameters.</td>
          <td>UrbanGen runs all 6 models entirely within a consumer <strong>6GB VRAM</strong> limit without out-of-memory errors.</td>
        </tr>
        <tr>
          <td><strong>NVML</strong></td>
          <td>NVIDIA Management Library</td>
          <td>A C-based programmatic API for monitoring GPU hardware metrics, clock speeds, and real-time power consumption.</td>
          <td>Polled continuously during 50-epoch training to log cumulative electrical energy consumption (<strong>0.133 kWh</strong>).</td>
        </tr>
        <tr>
          <td><strong>CEA</strong></td>
          <td>Central Electricity Authority (India)</td>
          <td>Statutory body that publishes official national carbon emission factors for electrical grid generation.</td>
          <td>Supplied the national grid carbon factor (0.713 kg CO2e / kWh) to prove our total footprint is only <strong>94.8 g CO2e</strong>.</td>
        </tr>
        <tr>
          <td><strong>CO2e</strong></td>
          <td>Carbon Dioxide Equivalent</td>
          <td>Standard unit for measuring carbon footprints by expressing the climate impact of greenhouse gas emissions.</td>
          <td>Proves UrbanGen AI satisfies "Green AI" standards with 94.8 g emissions across the entire multi-model suite.</td>
        </tr>
        <tr>
          <td><strong>CUDA</strong></td>
          <td>Compute Unified Device Architecture</td>
          <td>Parallel computing platform and API model developed by NVIDIA for general computing on graphical GPUs.</td>
          <td>Enables fast tensor acceleration on our RTX 4050 GPU under CUDA 12.x.</td>
        </tr>
      </tbody>
    </table>

    <h3>4.5 Software Engineering, Web Architecture & API Security</h3>
    <table>
      <thead>
        <tr>
          <th style="width: 13%;">Acronym</th>
          <th style="width: 26%;">Complete Full Form</th>
          <th style="width: 36%;">Plain-English Meaning & Definition</th>
          <th style="width: 25%;">Application in UrbanGen AI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>REST</strong></td>
          <td>Representational State Transfer</td>
          <td>A stateless software architectural style for building networked web applications using standard HTTP verbs.</td>
          <td>Defines our backend FastAPI endpoint design (`/api/models/predict`, `/api/models/generate`).</td>
        </tr>
        <tr>
          <td><strong>API</strong></td>
          <td>Application Programming Interface</td>
          <td>A software intermediary that allows two applications to talk to each other through well-defined contracts.</td>
          <td>Connects our React/Vite frontend client to PyTorch backend model inference microservices.</td>
        </tr>
        <tr>
          <td><strong>CORS</strong></td>
          <td>Cross-Origin Resource Sharing</td>
          <td>A browser security mechanism that restricts resources from being requested from another domain outside its origin.</td>
          <td>Configured with strict whitelist domains to prevent unauthorized cross-origin requests.</td>
        </tr>
        <tr>
          <td><strong>JSON</strong></td>
          <td>JavaScript Object Notation</td>
          <td>A lightweight data-interchange format that is human-readable and easy for machines to parse and generate.</td>
          <td>Standard schema for exchanging spatial predictions, FSI telemetry, and loss metrics between frontend and backend.</td>
        </tr>
        <tr>
          <td><strong>MIME</strong></td>
          <td>Multipurpose Internet Mail Extensions</td>
          <td>An internet standard that indicates the format and media type of a document or file payload.</td>
          <td>Strict magic-byte file inspection enforces genuine image MIME types (`image/jpeg`, `image/png`) to prevent shell injection.</td>
        </tr>
        <tr>
          <td><strong>HITL</strong></td>
          <td>Human-in-the-Loop</td>
          <td>An AI design pattern requiring human review and approval before automated recommendations become actionable.</td>
          <td>UrbanGen AI serves strictly as assistive drafting support; autonomous municipal zoning enforcement is strictly prohibited.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">
    <span>UrbanGen AI &bull; B.Tech Capstone Project 2026 &bull; MIT Academy of Engineering, Pune</span>
    <span>Page 4 of 5</span>
  </div>
</div>

<!-- ========================================== -->
<!-- PAGE 5: EXTERNAL EXAMINER VIVA DEFENSE GUIDE -->
<!-- ========================================== -->
<div class="page-container">
  <div class="page-content">
    <h2>5. External Examiner Viva Voce Defense Guide (Frequently Asked Questions)</h2>

    <div class="callout callout-warning">
      <strong>Question 1: "Why do you have ResNet-18 in your project if it is not a Generative AI model?"</strong><br>
      <em>Examiner-Ready Answer:</em> "ResNet-18 is explicitly designated as an <strong>Auxiliary Evaluation Auditor</strong>, not a generative architecture. Evaluating generative models like GANs and Diffusion models solely through human visual inspection is subjective and scientifically insufficient. We freeze our 98.10% accurate ResNet-18 classifier to independently score whether synthetic tiles generated by cDCGAN and DDPM mathematically contain the spatial geometries of their conditioned class. It gives us an objective, reproducible metric (99.40% Semantic Proxy Recognition)."
    </div>

    <div class="callout callout-success">
      <strong>Question 2: "Between cDCGAN and Conditional DDPM, which one is better and why?"</strong><br>
      <em>Examiner-Ready Answer:</em> "It depends on the operational deployment requirement:
      <ul style="margin: 2px 0 2px 14px; padding: 0;">
        <li><strong>For Edge Deployment & Latency:</strong> <strong>Residual cDCGAN is our champion</strong>. It executes in <strong>32 ms</strong> (&lt;35 ms), which is <strong>56&times; faster</strong> than diffusion, while achieving 99.40% semantic recognition. It can run interactively inside a local municipal GIS web tool.</li>
        <li><strong>For Structural Sharpness & Absence of Artifacts:</strong> <strong>DDPM is superior</strong> because its reverse diffusion process avoids adversarial minimax instability, delivering zero mode collapse and pristine structural boundaries with 0.0304 noise MSE. With our 20-step DDIM acceleration, we brought its latency down from 28.4s to 1.82s."</li>
      </ul>
    </div>

    <div class="callout callout-purple">
      <strong>Question 3: "Why did U-Net DAE outperform Spatial &beta;-VAE in image reconstruction (+2.16 dB)?"</strong><br>
      <em>Examiner-Ready Answer:</em> "Autoencoders and VAEs serve fundamentally different mathematical objectives. DAE optimizes purely for pixel-level fidelity via direct transposed skip connections that preserve high-frequency orthogonal edges (achieving 29.65 dB PSNR and 0.8649 SSIM). Spatial &beta;-VAE, by contrast, must optimize a dual objective: reconstruction plus a KL divergence regularization penalty that forces the latent space into an interpolatable continuous Gaussian prior N(0, I). This trade-off slightly lowers reconstruction (27.49 dB) in exchange for continuous latent manifold traversal and unsupervised anomaly detection (&gt;3&sigma; disparity)."
    </div>

    <div class="callout">
      <strong>Question 4: "What is posterior collapse in VAEs, and how did your team prevent it?"</strong><br>
      <em>Examiner-Ready Answer:</em> "Posterior collapse occurs when a VAE's decoder ignores the latent code z because the KL divergence term dominates during training, driving KL &rarr; 0 and producing blurry, generic images. We prevented posterior collapse through two architectural innovations: (1) preserving a 3D spatial latent tensor &mu;, log &sigma;^2 in &Ropf;^(64 &times; 8 &times; 8) rather than collapsing to a 1D vector, and (2) calibrating the &beta; weighting factor to &beta; = 10^-4 with compact skip dropout (0.2). This maintained an active, expressive latent space (KL = 60.72 nats) while preserving high reconstruction sharpness."
    </div>

    <div class="callout callout-success">
      <strong>Question 5: "How does MiniGPT prevent legal hallucination in urban bylaws?"</strong><br>
      <em>Examiner-Ready Answer:</em> "Monolithic general LLMs often hallucinate inapplicable foreign zoning laws. We trained a specialized 4-layer Causal Transformer from scratch directly on Pune Municipal Corporation (PMC) bylaws, Transit-Oriented Development mandates, and the Indian National Building Code. By pairing this domain-specific vocabulary with a tight context window (T=192), the model achieved an ultra-low validation perplexity of <strong>1.110</strong> (0.1505 Bits/Char), ensuring strictly grounded, mathematically sound FSI calculations (1.8 to 2.4) and green-buffer mandates."
    </div>

    <div class="callout callout-purple">
      <strong>Question 6: "What justifies the 'Green AI' claim in your capstone project?"</strong><br>
      <em>Examiner-Ready Answer:</em> "Rather than relying on carbon-intensive cloud GPU clusters, our entire 6-model multi-architecture suite was trained and benchmarked strictly on a single consumer laptop GPU (NVIDIA RTX 4050, 6GB VRAM, 75W TGP). By sampling GPU power draw via NVML every 500 ms, we measured a cumulative electrical consumption of only <strong>0.133 kWh</strong> across 66.3 minutes of cumulative training. Applying the official Central Electricity Authority (CEA) India grid factor of 0.713 kg CO2e / kWh, our total project carbon cost was certified at only <strong>94.8 g CO2e</strong>."
    </div>

    <div style="margin-top: 8px; border: 1px solid #cbd5e1; border-radius: 4px; padding: 5px 8px; background: #f8fafc; font-size: 6.8pt;">
      <div style="font-weight: 700; color: #1e3a8a; margin-bottom: 2px;">ACADEMIC CERTIFICATION & PROJECT ATTESTATION</div>
      This comprehensive evaluation dossier and glossary represents verified, reproducible experimental data conducted under the Department of Computer Engineering, MIT Academy of Engineering, Pune. All neural weights, training checkpoints, and benchmark telemetry are logged and version-controlled.
    </div>
  </div>
  <div class="page-footer">
    <span>UrbanGen AI &bull; B.Tech Capstone Project 2026 &bull; MIT Academy of Engineering, Pune</span>
    <span>Page 5 of 5</span>
  </div>
</div>

</body>
</html>
"""
    return html_template.replace("__LOGO_TAG__", logo_img_tag)

def main():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(workspace, "docs")
    public_dir = os.path.join(workspace, "frontend", "public")
    
    html_path = os.path.join(docs_dir, "UrbanGen_AI_Model_Performance_and_Glossary.html")
    pdf_path = os.path.join(docs_dir, "UrbanGen_AI_Model_Performance_and_Glossary.pdf")
    
    public_html_path = os.path.join(public_dir, "UrbanGen_AI_Model_Performance_and_Glossary.html")
    public_pdf_path = os.path.join(public_dir, "UrbanGen_AI_Model_Performance_and_Glossary.pdf")

    print("[1/4] Generating publication-grade HTML content...")
    html_data = build_html()
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_data)
    with open(public_html_path, "w", encoding="utf-8") as f:
        f.write(html_data)
    print(f"HTML saved to: {html_path}")
    print(f"HTML copied to: {public_html_path}")

    print("[2/4] Converting HTML to PDF using Google Chrome headless engine...")
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"[3/4] PDF generated successfully ({size_kb:.1f} KB): {pdf_path}")
        
        # Copy to frontend/public for download
        with open(pdf_path, "rb") as src, open(public_pdf_path, "wb") as dst:
            dst.write(src.read())
        print(f"[4/4] PDF deployed to frontend public directory: {public_pdf_path}")
    else:
        print(f"Error generating PDF. Stderr: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
