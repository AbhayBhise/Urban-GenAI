import urllib.request
import zlib
import os
from PIL import Image

def encode_plantuml(text: str) -> str:
    """Encode PlantUML text into standard 64-character encoded string."""
    mapping = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]
    
    res = []
    for i in range(0, len(compressed), 3):
        b1 = compressed[i]
        b2 = compressed[i+1] if i+1 < len(compressed) else 0
        b3 = compressed[i+2] if i+2 < len(compressed) else 0
        
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        
        res.append(mapping[c1])
        res.append(mapping[c2])
        if i + 1 < len(compressed):
            res.append(mapping[c3])
        else:
            res.append("0")
        if i + 2 < len(compressed):
            res.append(mapping[c4])
        else:
            res.append("0")
            
    return "".join(res)

PLANTUML_SOURCE = """@startuml
skinparam dpi 300
skinparam defaultFontName "Arial"
skinparam defaultFontSize 13
skinparam roundcorner 10
skinparam shadowing true
skinparam linetype ortho
skinparam packageTitleAlignment left

skinparam package {
  BackgroundColor #F8FAFC
  BorderColor #94A3B8
  BorderThickness 1.8
  FontStyle bold
  FontSize 15
}

skinparam rectangle {
  BackgroundColor #FFFFFF
  BorderColor #0284C7
  BorderThickness 1.6
  FontSize 13
}

skinparam arrow {
  Color #0284C7
  Thickness 1.8
  FontSize 12
  FontStyle bold
}

' ==============================================================================
' 1. INPUT STAGE
' ==============================================================================
package "1. Remote Sensing Input & Ingestion" #F0F9FF {
  rectangle "<b>USGS UCMerced Orthoimagery</b>\\n2,100 Aerial Tiles (256x256, 0.3m GSD)\\n21 Municipal Land-Use Classes" as RAW #E0F2FE
  rectangle "<b>Atmospheric Degradation Layer</b>\\nSynthetic Cloud Shadow & Sensor Noise\\nCorrupted Input: x ~ N(mu, sigma=0.15)\\nTile: 128x128x3" as CORRUPT #FEE2E2
  RAW -right-> CORRUPT : Sensor Attenuation
}

' ==============================================================================
' 2. RESTORATION STAGE (MODEL 1)
' ==============================================================================
package "2. Signal Restoration (Model 1: U-Net DAE)" #ECFDF5 {
  rectangle "<b>Denoising Autoencoder (U-Net)</b>\\nStem -> L1(64) -> L2(128) -> L3(256) -> Bottleneck(512)\\nMulti-Scale Transposed Skip-Connections\\n<b>Loss:</b> L_AE = (1/N) * sum ||x - x_hat||^2 = <b>0.00449 MSE</b>\\n<b>Output:</b> Restored Crisp Aerial Tile\\n<b>Metric:</b> 29.65 dB PSNR (+7.0 dB Gain) | SSIM: 0.8649" as DAE #DCFCE7
}
CORRUPT -down-> DAE : Degraded Tile (128x128x3)

' ==============================================================================
' 3. LATENT MODELING & AUDITING (MODELS 2 & 3)
' ==============================================================================
package "3. Latent Manifold & Territorial Auditing" #F5F3FF {
  rectangle "<b>Spatial beta-VAE (Model 2)</b>\\nResNet-18 Backbone -> Spatial Latent z in R^(64x8x8)\\n4-Stage Transposed Deconvolution Decoder\\n<b>Loss:</b> L_VAE = (0.7*L_1 + 0.3*L_MSE) + 10^-4 * D_KL = <b>0.0483</b>\\n<b>Outputs:</b> Reconstructed Tile (27.49 dB) & Smooth Manifold" as VAE #EDE9FE

  rectangle "<b>Unsupervised Anomaly Detector</b>\\nReconstruction Disparity Map: |x_restored - x_vae|\\nFlagging Threshold: Disparity > 3*sigma" as ANOMALY #FEF3C7

  rectangle "<b>Land-Use Classifier (Model 3)</b>\\nResNet-18 Transfer Learning Backbone + Linear Head\\n<b>Loss:</b> L_CE = -sum y_i * log(p_i) = <b>0.0615</b>\\n<b>Output:</b> Territorial Label y in {0..20}\\n<b>Metric:</b> 98.10% Val Accuracy | Macro F1: 0.9784" as CLS #E0F2FE

  VAE -right-> ANOMALY : Disparity Evaluation
}
DAE -down-> VAE : Clean Restored Tile
DAE -down-> CLS : Clean Restored Tile

' ==============================================================================
' 4. DUAL-MODALITY SYNTHESIS (MODELS 4 & 5)
' ==============================================================================
package "4. Dual-Modality Generative Parcel Synthesis" #FFFBEB {
  rectangle "<b>Residual cDCGAN (Model 4)</b>\\n4x ResUpBlock Generator + Projection Discriminator\\nSpectral Normalization + AC-GAN Auxiliary Head\\n<b>Loss:</b> L_adv(D, G) Minimax + 0.8*L_AC (D=1.67, G=1.19)\\n<b>Output:</b> High-Speed Synthetic Parcel (<35ms)\\n<b>Metric:</b> 99.40% Semantic Proxy Recognition" as GAN #FEF3C7

  rectangle "<b>Conditional DDPM (Model 5)</b>\\nTime & Class-Conditioned U-Net (T=1000 Schedule)\\n20-Step Deterministic Accelerated DDIM Sampler\\n<b>Loss:</b> 5-Loss Composite (L_simple + L_vlb + L_guide + L_sp + L_reg)\\n<b>Output:</b> Photorealistic Aerial Parcel (1.82s)\\n<b>Metric:</b> 0.0304 Noise MSE (15.6x Accelerated)" as DIFF #FEE2E2
}
CLS -down-> GAN : Condition y in {0..20}
CLS -down-> DIFF : Class Guidance Vector
VAE .down.> GAN : Latent Feature Anchor
GAN .up.> CLS : Semantic Validation Loop (99.40%)
DIFF .up.> CLS : Classifier Guidance (grad log p(y|x))

' ==============================================================================
' 5. POLICY ENGINE (MODEL 6)
' ==============================================================================
package "5. Grounded Municipal Policy Formulation (Model 6: MiniGPT)" #F0FDF4 {
  rectangle "<b>Municipal Plan Generator (MiniGPT)</b>\\n4-Layer Pre-LayerNorm Causal Transformer (d_model=256, 4 Heads)\\nContext Window T=192 | PMC Development Control Rules\\n<b>Loss:</b> L_causal = -sum log P(w_t | w_<t) = <b>0.1043</b>\\n<b>Metric:</b> 1.110 Validation Perplexity | 0.1505 Bits/Char" as GPT #D1FAE5

  rectangle "<b>Actionable Grounded Directives</b>\\n- FSI Allocation: 1.8 - 2.4 along transit spines\\n- TOD Corridors & 15% Riverbank Green Buffer\\n- Rainwater & Solar Mandate for Plots > 1,000 m2" as BYLAWS #A7F3D0
  GPT -right-> BYLAWS : Generates Bylaws
}
CLS -down-> GPT : Verified Zoning Label y
ANOMALY -down-> GPT : Anomaly Telemetry & Risk Score

' ==============================================================================
' 6. SYSTEM SECURITY & HARDWARE
' ==============================================================================
package "6. Air-Gapped Edge Hardware & System Security" #F8FAFC {
  rectangle "<b>FastAPI Edge Gateway</b>\\n- URBANGEN_API_KEY Authentication\\n- SlowAPI Token Bucket Rate Limiting\\n- Magic-Byte File Inspection (<10MB, 128x128)" as GATEWAY #FFFFFF
  rectangle "<b>Green AI Edge Compute</b>\\n- 100% On-Premises NVIDIA RTX 4050 6GB (75W)\\n- Total Energy: 0.133 kWh (94.8 g CO2e)\\n- Zero Cloud GIS Leakage (100% Data Sovereignty)" as HARDWARE #FFFFFF
  rectangle "<b>Human-in-the-Loop Governance</b>\\n- Strictly Advisory Decision Support\\n- Autonomous Legal Enforcement Prohibited" as GOV #FFFFFF
}

@enduml
"""

def generate_diagrams():
    enc = encode_plantuml(PLANTUML_SOURCE)
    
    # URLs
    svg_url = f"https://www.plantuml.com/plantuml/svg/{enc}"
    png_url = f"https://www.plantuml.com/plantuml/png/{enc}"
    
    targets = [
        "docs/poster/figures",
        "frontend/public/poster/figures"
    ]
    
    for t in targets:
        os.makedirs(t, exist_ok=True)
        
        # Save SVG
        svg_file = os.path.join(t, "full_project_architecture_plantuml.svg")
        req_svg = urllib.request.Request(svg_url, headers={"User-Agent": "UrbanGenAI/1.0"})
        print(f"Fetching SVG -> {svg_file}...")
        with urllib.request.urlopen(req_svg, timeout=30) as r:
            with open(svg_file, "wb") as f:
                f.write(r.read())
        print(f"Saved SVG: {svg_file}")
        
        # Save PNG
        png_file = os.path.join(t, "full_project_architecture_plantuml.png")
        req_png = urllib.request.Request(png_url, headers={"User-Agent": "UrbanGenAI/1.0"})
        print(f"Fetching PNG -> {png_file}...")
        with urllib.request.urlopen(req_png, timeout=30) as r:
            with open(png_file, "wb") as f:
                f.write(r.read())
        print(f"Saved PNG: {png_file}")
        
        # Also copy as pipeline_architecture_plantuml to update existing references
        pipe_png = os.path.join(t, "pipeline_architecture_plantuml.png")
        pipe_svg = os.path.join(t, "pipeline_architecture_plantuml.svg")
        with open(png_file, "rb") as src, open(pipe_png, "wb") as dst:
            dst.write(src.read())
        with open(svg_file, "rb") as src, open(pipe_svg, "wb") as dst:
            dst.write(src.read())
        print(f"Updated: {pipe_png} and {pipe_svg}")

    # Verify PNG size
    img = Image.open("docs/poster/figures/full_project_architecture_plantuml.png")
    print(f"Architecture Diagram Resolution: {img.width} x {img.height} pixels")

if __name__ == "__main__":
    generate_diagrams()

