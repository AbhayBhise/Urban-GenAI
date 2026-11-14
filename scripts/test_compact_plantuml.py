import urllib.request
import zlib
import os
from PIL import Image

def encode_plantuml(text: str) -> str:
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

GRID_PLANTUML = """@startuml
scale 3000 width
skinparam dpi 130
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam roundcorner 8
skinparam shadowing false
skinparam packageTitleAlignment left

skinparam package {
  BackgroundColor #F8FAFC
  BorderColor #94A3B8
  BorderThickness 1.5
  FontStyle bold
  FontSize 13
}

skinparam rectangle {
  BackgroundColor #FFFFFF
  BorderColor #0284C7
  BorderThickness 1.5
  FontSize 12
}

skinparam arrow {
  Color #0284C7
  Thickness 1.6
  FontSize 11
  FontStyle bold
}

' ==============================================================================
' TOP ROW: INPUT -> RESTORATION (MODEL 1) -> LATENT MANIFOLD & AUDIT (MODELS 2 & 3)
' ==============================================================================
package "Stage 1: Remote Sensing Ingestion" #F0F9FF {
  rectangle "<b>USGS UCMerced Tiles</b>\\n2,100 Tiles (256x256, 0.3m GSD)\\n21 Municipal Land-Use Classes" as RAW #E0F2FE
  rectangle "<b>Atmospheric Degradation</b>\\nSynthetic Cloud Shadow & Sensor Noise\\nCorrupted Input: x ~ N(mu, sigma=0.15)\\nRaster: 128x128x3" as NOISY #FEE2E2
  RAW -right-> NOISY : Sensor Noise
}

package "Stage 2: Signal Restoration (Model 1)" #ECFDF5 {
  rectangle "<b>Denoising Autoencoder (U-Net)</b>\\nStem -> L1(64) -> L2(128) -> L3(256) -> Bottleneck(512)\\nMulti-Scale Transposed Skip-Connections\\n<b>Loss:</b> L_AE = <b>0.00449 MSE</b> (0.00617 total)\\n<b>Output:</b> Restored High-Fidelity Tile\\n<b>Metrics:</b> 29.65 dB PSNR (+7.0 dB Gain) | SSIM: 0.8649" as DAE #DCFCE7
}
NOISY -right-> DAE : Degraded Tile (128x128x3)

package "Stage 3: Latent Manifold & Territorial Auditing (Models 2 & 3)" #F5F3FF {
  rectangle "<b>Spatial beta-VAE (Model 2)</b>\\nResNet-18 -> Spatial Latent z in R^(64x8x8)\\n4-Stage Transposed Conv Decoder\\n<b>Loss:</b> L_VAE = <b>0.0483</b> (KL: 60.72 nats)\\n<b>Outputs:</b> Reconstructed Tile (27.49 dB) & Smooth Manifold" as VAE #EDE9FE

  rectangle "<b>Unsupervised Anomaly Detector</b>\\nReconstruction Disparity Map: |x_restored - x_vae|\\nFlagging Threshold: Disparity > 3*sigma" as ANOMALY #FEF3C7

  rectangle "<b>Land-Use Classifier (Model 3)</b>\\nResNet-18 Transfer Backbone + 21-Class Head\\n<b>Loss:</b> L_CE = <b>0.0615</b> (Cross-Entropy)\\n<b>Output:</b> Verified Territorial Label y in {0..20}\\n<b>Metrics:</b> 98.10% Val Accuracy | Macro F1: 0.9784" as CLS #E0F2FE

  VAE -right-> ANOMALY : Disparity Map
}
DAE -right-> VAE : Clean Tile
DAE -right-> CLS : Clean Tile

' ==============================================================================
' BOTTOM ROW: SYNTHESIS (MODELS 4 & 5) -> POLICY (MODEL 6) -> EDGE SECURITY
' ==============================================================================
package "Stage 4: Generative Synthesis (Models 4 & 5)" #FFFBEB {
  rectangle "<b>Residual cDCGAN (Model 4)</b>\\n4x ResUpBlock Gen + Projection Disc\\nSpectral Norm + AC-GAN Auxiliary Head\\n<b>Loss:</b> Minimax Eq. (D=1.67, G=1.19)\\n<b>Output:</b> Fast Synthetic Parcel (<35ms)\\n<b>Metric:</b> 99.40% Proxy Recognition" as GAN #FEF3C7

  rectangle "<b>Conditional DDPM (Model 5)</b>\\nTime & Class Conditioned U-Net (T=1000)\\n20-Step Accelerated DDIM Sampler\\n<b>Loss:</b> 5 Losses (Noise MSE: 0.0304)\\n<b>Output:</b> Photorealistic Parcel (1.82s)\\n<b>Metric:</b> 15.6x Accelerated Sampling" as DIFF #FEE2E2
}

package "Stage 5: Grounded Policy (Model 6)" #ECFDF5 {
  rectangle "<b>Urban Plan Generator (MiniGPT)</b>\\n4-Layer Pre-LN Causal Transformer (d=256, 4 Heads)\\nContext Window T=192 | PMC Control Rules\\n<b>Loss:</b> L_causal = <b>0.1043</b> (Causal Cross-Entropy)\\n<b>Metrics:</b> 1.110 Validation Perplexity | 0.1505 BPC" as GPT #D1FAE5

  rectangle "<b>Actionable Grounded Directives</b>\\n- FSI Allocation: 1.8 - 2.4 along transit spines\\n- TOD Corridors & 15% Riverbank Green Buffer\\n- Rainwater & Solar Mandate for Plots > 1,000 m2" as BYLAWS #A7F3D0
  GPT -right-> BYLAWS : Generates Bylaws
}

package "Stage 6: Air-Gapped Edge Hardware & Security" #F8FAFC {
  rectangle "<b>FastAPI Edge Gateway</b>\\n- URBANGEN_API_KEY Authentication\\n- SlowAPI Token Bucket Rate Limiting\\n- Magic-Byte File Inspection (<10MB, 128x128)" as GATEWAY #FFFFFF
  rectangle "<b>Green AI Edge Compute</b>\\n- 100% On-Premises NVIDIA RTX 4050 6GB (75W)\\n- Total Energy: 0.133 kWh (94.8 g CO2e)\\n- Zero Cloud GIS Leakage (100% Data Sovereignty)" as HARDWARE #FFFFFF
  rectangle "<b>Human-in-the-Loop Governance</b>\\n- Strictly Advisory Decision Support\\n- Autonomous Legal Enforcement Prohibited" as GOV #FFFFFF
}

CLS -down-> GAN : Condition y
CLS -down-> DIFF : Guidance Vector
CLS -down-> GPT : Verified Label y
ANOMALY -down-> GPT : Anomaly Telemetry
BYLAWS -right-> GATEWAY : Edge Serving

@enduml
"""

def generate_and_check():
    enc = encode_plantuml(GRID_PLANTUML)
    
    out_dir = "docs/poster/figures"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_url = f"https://www.plantuml.com/plantuml/svg/{enc}"
    png_url = f"https://www.plantuml.com/plantuml/png/{enc}"
    
    png_path = os.path.join(out_dir, "full_project_architecture_plantuml.png")
    svg_path = os.path.join(out_dir, "full_project_architecture_plantuml.svg")
    
    req_png = urllib.request.Request(png_url, headers={"User-Agent": "UrbanGenAI/1.0"})
    with urllib.request.urlopen(req_png, timeout=30) as r:
        with open(png_path, "wb") as f:
            f.write(r.read())
            
    req_svg = urllib.request.Request(svg_url, headers={"User-Agent": "UrbanGenAI/1.0"})
    with urllib.request.urlopen(req_svg, timeout=30) as r:
        with open(svg_path, "wb") as f:
            f.write(r.read())
            
    im = Image.open(png_path)
    print(f"Generated PNG Resolution: {im.width} x {im.height}")
    print(f"Is Width < 4096 (unclipped)? {im.width < 4096}")
    
    # Also copy to frontend public
    pub_dir = "frontend/public/poster/figures"
    os.makedirs(pub_dir, exist_ok=True)
    with open(png_path, "rb") as s, open(os.path.join(pub_dir, "full_project_architecture_plantuml.png"), "wb") as d:
        d.write(s.read())
    with open(svg_path, "rb") as s, open(os.path.join(pub_dir, "full_project_architecture_plantuml.svg"), "wb") as d:
        d.write(s.read())
    print("Copied to frontend public.")

if __name__ == "__main__":
    generate_and_check()
