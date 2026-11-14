import os
from PIL import Image, ImageDraw, ImageFont

def build_vector_diagram():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 450" width="100%" height="100%" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0284C7" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7C3AED" />
    </marker>
    <linearGradient id="grad-navy" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A192F" />
      <stop offset="100%" stop-color="#142B50" />
    </linearGradient>
  </defs>

  <!-- Border & Canvas -->
  <rect x="2" y="2" width="1596" height="446" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>

  <!-- ===================================================================== -->
  <!-- 1. STAGE 1: REMOTE SENSING INGESTION (x: 16, w: 230)                   -->
  <!-- ===================================================================== -->
  <g transform="translate(16, 16)">
    <rect width="230" height="418" rx="8" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="210" height="28" rx="5" fill="#0284C7"/>
    <text x="115" y="28" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.03em">1. REMOTE SENSING INPUT</text>

    <!-- Raw Data -->
    <rect x="12" y="48" width="206" height="150" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="70" fill="#0A192F" font-size="12" font-weight="800">USGS UCMerced Dataset</text>
    <text x="22" y="92" fill="#475569" font-size="10.5">• 2,100 Orthoimagery Tiles</text>
    <text x="22" y="110" fill="#475569" font-size="10.5">• 256×256 px, 0.3m GSD</text>
    <text x="22" y="128" fill="#475569" font-size="10.5">• 21 Urban Land-Use Classes</text>
    <text x="22" y="146" fill="#475569" font-size="10.5">• Stratified 90% Train / 10% Val</text>
    <rect x="22" y="160" width="186" height="24" rx="4" fill="#E0F2FE"/>
    <text x="115" y="176" text-anchor="middle" fill="#0369A1" font-size="10" font-weight="700">Stratified Split: 1,890 / 210</text>

    <!-- Down arrow -->
    <line x1="115" y1="205" x2="115" y2="235" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <text x="122" y="224" fill="#0284C7" font-size="9" font-weight="700">Atmosphere</text>

    <!-- Corrupted Tile -->
    <rect x="12" y="242" width="206" height="162" rx="6" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1.2"/>
    <text x="22" y="264" fill="#E11D48" font-size="12" font-weight="800">Atmospheric Corruption</text>
    <text x="22" y="286" fill="#475569" font-size="10.5">• Synthetic Cloud Shadowing</text>
    <text x="22" y="304" fill="#475569" font-size="10.5">• Gaussian Sensor Noise (σ=0.15)</text>
    <text x="22" y="322" fill="#475569" font-size="10.5">• Clamped Spatial Tensor:</text>
    <text x="22" y="342" fill="#9F1239" font-family="monospace" font-size="11" font-weight="700">  x̃ ∈ ℝ^(128×128×3)</text>
    <rect x="22" y="360" width="186" height="32" rx="4" fill="#FFE4E6"/>
    <text x="115" y="380" text-anchor="middle" fill="#BE123C" font-size="10" font-weight="800">Degraded Input (22.65 dB)</text>
  </g>

  <!-- Arrow 1 to 2 -->
  <line x1="250" y1="340" x2="278" y2="340" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- ===================================================================== -->
  <!-- 2. STAGE 2: SIGNAL RESTORATION (x: 280, w: 236)                       -->
  <!-- ===================================================================== -->
  <g transform="translate(280, 16)">
    <rect width="236" height="418" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="216" height="28" rx="5" fill="#059669"/>
    <text x="118" y="28" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.03em">2. OPTICAL RESTORATION</text>

    <!-- DAE Card -->
    <rect x="12" y="48" width="212" height="356" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="72" fill="#065F46" font-size="12.5" font-weight="800">Model 1: Denoising AE</text>
    <text x="22" y="90" fill="#047857" font-size="10.5" font-weight="700">U-Net Multi-Scale Architecture</text>
    
    <text x="22" y="115" fill="#475569" font-size="10">• Stem: 3 → 64 channels</text>
    <text x="22" y="133" fill="#475569" font-size="10">• Encoder: L1(64) → L2(128) → L3(256)</text>
    <text x="22" y="151" fill="#475569" font-size="10">• Bottleneck: 512 channels</text>
    <text x="22" y="169" fill="#475569" font-size="10">• Skip-Connections: Stem, L1, L2, L3</text>
    <text x="22" y="187" fill="#475569" font-size="10">• Transposed Conv Decoders</text>

    <!-- Formula Box -->
    <rect x="20" y="202" width="196" height="46" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-left="3px solid #059669"/>
    <text x="28" y="222" fill="#0F172A" font-family="monospace" font-size="10" font-weight="700">ℒ_AE = (1/N) ∑ ||x - x̂||²</text>
    <text x="28" y="238" fill="#059669" font-family="monospace" font-size="10.5" font-weight="800">Loss: 0.00449 MSE (0.00617)</text>

    <!-- Metrics Callout -->
    <rect x="20" y="258" width="196" height="66" rx="5" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1.2"/>
    <text x="28" y="280" fill="#065F46" font-size="12" font-weight="800">PSNR: 29.65 dB</text>
    <text x="28" y="298" fill="#047857" font-size="10.5" font-weight="700">+7.0 dB Gain over Degraded</text>
    <text x="28" y="314" fill="#065F46" font-size="10.5" font-weight="600">SSIM: 0.8649 (Crisp Grids)</text>

    <!-- Output badge -->
    <rect x="20" y="338" width="196" height="52" rx="5" fill="#F0FDF4" stroke="#BBF7D0"/>
    <text x="28" y="358" fill="#047857" font-size="10" font-weight="700">OUTPUT PRODUCT:</text>
    <text x="28" y="378" fill="#065F46" font-size="11" font-weight="800">Restored Tile x̂ (128×128×3)</text>
  </g>

  <!-- Arrow 2 to 3 -->
  <line x1="520" y1="180" x2="548" y2="180" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <line x1="520" y1="330" x2="548" y2="330" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>

  <!-- ===================================================================== -->
  <!-- 3. STAGE 3: LATENT MANIFOLD & AUDIT (x: 550, w: 250)                  -->
  <!-- ===================================================================== -->
  <g transform="translate(550, 16)">
    <rect width="250" height="418" rx="8" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="230" height="28" rx="5" fill="#7C3AED"/>
    <text x="125" y="28" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.03em">3. MANIFOLD &amp; ZONING AUDIT</text>

    <!-- Model 2: Spatial VAE -->
    <rect x="12" y="48" width="226" height="175" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="70" fill="#6D28D9" font-size="12" font-weight="800">Model 2: Spatial β-VAE</text>
    <text x="22" y="88" fill="#475569" font-size="10">• Latent: z ∈ ℝ^(64×8×8) preserves 2D</text>
    <text x="22" y="104" fill="#475569" font-size="10">• 4-Stage Transposed Conv Decoder</text>
    <text x="22" y="122" fill="#5B21B6" font-family="monospace" font-size="9.5" font-weight="700">ℒ_VAE = 0.7ℒ₁+0.3ℒ_MSE + 10⁻⁴D_KL</text>
    <text x="22" y="138" fill="#7C3AED" font-family="monospace" font-size="10" font-weight="800">Loss: 0.0483 (KL: 60.72 nats)</text>
    <rect x="20" y="148" width="210" height="65" rx="4" fill="#EDE9FE"/>
    <text x="28" y="168" fill="#5B21B6" font-size="10.5" font-weight="800">PSNR: 27.49 dB | Smooth Manifold</text>
    <text x="28" y="186" fill="#6D28D9" font-size="9.5" font-weight="700">Anomaly Detector: Disparity &gt; 3σ</text>
    <text x="28" y="202" fill="#475569" font-size="9.5">Pinpoints unpermitted land change</text>

    <!-- Model 3: Land-Use Classifier -->
    <rect x="12" y="235" width="226" height="169" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="258" fill="#0284C7" font-size="12" font-weight="800">Model 3: Land-Use Classifier</text>
    <text x="22" y="276" fill="#475569" font-size="10">• ResNet-18 Transfer Learning</text>
    <text x="22" y="292" fill="#475569" font-size="10">• 21-Category Territorial Audit Head</text>
    <text x="22" y="310" fill="#0369A1" font-family="monospace" font-size="10" font-weight="700">ℒ_CE = -∑ yᵢ log(pᵢ)</text>
    <text x="22" y="326" fill="#0284C7" font-family="monospace" font-size="10" font-weight="800">Final CE Loss: 0.06150 (Epoch 50)</text>
    <rect x="20" y="336" width="210" height="58" rx="4" fill="#E0F2FE"/>
    <text x="28" y="356" fill="#0369A1" font-size="11" font-weight="800">Val Accuracy: 98.10%</text>
    <text x="28" y="374" fill="#0284C7" font-size="10.5" font-weight="700">Macro F1: 0.9784 (21 Classes)</text>
    <text x="28" y="388" fill="#475569" font-size="9">Provides class condition vector y</text>
  </g>

  <!-- Arrow 3 to 4 -->
  <line x1="804" y1="180" x2="832" y2="180" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
  <line x1="804" y1="330" x2="832" y2="330" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- ===================================================================== -->
  <!-- 4. STAGE 4: DUAL-MODALITY SYNTHESIS (x: 834, w: 250)                  -->
  <!-- ===================================================================== -->
  <g transform="translate(834, 16)">
    <rect width="250" height="418" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="230" height="28" rx="5" fill="#D97706"/>
    <text x="125" y="28" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.03em">4. GENERATIVE SYNTHESIS</text>

    <!-- Model 4: Residual cDCGAN -->
    <rect x="12" y="48" width="226" height="175" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="70" fill="#B45309" font-size="12" font-weight="800">Model 4: Residual cDCGAN</text>
    <text x="22" y="88" fill="#475569" font-size="10">• 4x ResUpBlock Gen + Proj Disc</text>
    <text x="22" y="104" fill="#475569" font-size="10">• Spectral Norm + AC-GAN Head</text>
    <text x="22" y="122" fill="#B45309" font-family="monospace" font-size="9.5" font-weight="700">ℒ_G = ℒ_adv + 0.8ℒ_AC (EMA)</text>
    <text x="22" y="138" fill="#D97706" font-family="monospace" font-size="10" font-weight="800">Minimax: D=1.67, G=1.19</text>
    <rect x="20" y="148" width="210" height="65" rx="4" fill="#FEF3C7"/>
    <text x="28" y="168" fill="#92400E" font-size="11" font-weight="800">Proxy Rec: 99.40% (167/168)</text>
    <text x="28" y="186" fill="#B45309" font-size="10.5" font-weight="700">Edge Latency: &lt;35 ms</text>
    <text x="28" y="202" fill="#475569" font-size="9.5">Instant scenario parcel synthesis</text>

    <!-- Model 5: Conditional DDPM -->
    <rect x="12" y="235" width="226" height="169" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="258" fill="#E11D48" font-size="12" font-weight="800">Model 5: Conditional DDPM</text>
    <text x="22" y="276" fill="#475569" font-size="10">• Time/Class U-Net (T=1000)</text>
    <text x="22" y="292" fill="#475569" font-size="10">• 20-Step Deterministic DDIM</text>
    <text x="22" y="310" fill="#9F1239" font-family="monospace" font-size="9" font-weight="700">ℒ = ℒ_simple + ℒ_vlb + ℒ_guide + ...</text>
    <text x="22" y="326" fill="#E11D48" font-family="monospace" font-size="10" font-weight="800">Noise MSE: 0.0304 | VLB: 0.02916</text>
    <rect x="20" y="336" width="210" height="58" rx="4" fill="#FFE4E6"/>
    <text x="28" y="356" fill="#9F1239" font-size="11" font-weight="800">Sampling Latency: 1.82 s</text>
    <text x="28" y="374" fill="#BE123C" font-size="10.5" font-weight="700">15.6× Speedup vs 1000-Step</text>
    <text x="28" y="388" fill="#475569" font-size="9">Pristine street grid photorealism</text>
  </g>

  <!-- Arrow 4 to 5 -->
  <line x1="1088" y1="260" x2="1116" y2="260" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>

  <!-- ===================================================================== -->
  <!-- 5. STAGE 5: GROUNDED POLICY ENGINE (x: 1118, w: 236)                  -->
  <!-- ===================================================================== -->
  <g transform="translate(1118, 16)">
    <rect width="236" height="418" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="216" height="28" rx="5" fill="#047857"/>
    <text x="118" y="28" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.03em">5. GROUNDED POLICY ENGINE</text>

    <!-- MiniGPT Model Card -->
    <rect x="12" y="48" width="212" height="356" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="72" fill="#065F46" font-size="12.5" font-weight="800">Model 6: Urban Plan (MiniGPT)</text>
    <text x="22" y="90" fill="#047857" font-size="10.5" font-weight="700">Causal Transformer Architecture</text>
    
    <text x="22" y="112" fill="#475569" font-size="10">• 4 Pre-LayerNorm Transformer Blocks</text>
    <text x="22" y="128" fill="#475569" font-size="10">• d_model = 256, 4 Attention Heads</text>
    <text x="22" y="144" fill="#475569" font-size="10">• Context Window T = 192 Tokens</text>
    <text x="22" y="160" fill="#475569" font-size="10">• Pune Municipal Corp (PMC) Rules</text>

    <!-- Formula & Perplexity -->
    <rect x="20" y="174" width="196" height="46" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="28" y="194" fill="#0F172A" font-family="monospace" font-size="10" font-weight="700">ℒ_causal = -∑ log P(wₜ | w_&lt;ₜ)</text>
    <text x="28" y="210" fill="#059669" font-family="monospace" font-size="10.5" font-weight="800">Loss: 0.10430 | PPL: 1.110</text>

    <!-- Bylaw Directives Box -->
    <rect x="20" y="230" width="196" height="164" rx="5" fill="#D1FAE5" stroke="#6EE7B7" stroke-width="1.2"/>
    <text x="28" y="252" fill="#065F46" font-size="11" font-weight="800">Actionable Municipal Directives:</text>
    
    <text x="28" y="274" fill="#047857" font-size="10" font-weight="700">• FSI Allocation (1.8 – 2.4):</text>
    <text x="28" y="290" fill="#334155" font-size="9.5">  High-density transit corridors with</text>
    <text x="28" y="304" fill="#334155" font-size="9.5">  strict urban infrastructure caps.</text>

    <text x="28" y="324" fill="#047857" font-size="10" font-weight="700">• TOD &amp; Riverbank Buffers:</text>
    <text x="28" y="340" fill="#334155" font-size="9.5">  Mandates 15% green preservation zone</text>

    <text x="28" y="360" fill="#047857" font-size="10" font-weight="700">• Environmental Bylaws:</text>
    <text x="28" y="376" fill="#334155" font-size="9.5">  Rainwater &amp; solar on plots &gt;1000m²</text>
  </g>

  <!-- Arrow 5 to 6 -->
  <line x1="1358" y1="220" x2="1384" y2="220" stroke="#0F172A" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- ===================================================================== -->
  <!-- 6. STAGE 6: AIR-GAPPED EDGE SECURITY & GOVERNANCE (x: 1386, w: 198)   -->
  <!-- ===================================================================== -->
  <g transform="translate(1386, 16)">
    <rect width="198" height="418" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="178" height="28" rx="5" fill="#0A192F"/>
    <text x="99" y="28" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="800" letter-spacing="0.03em">6. SECURITY &amp; HARDWARE</text>

    <!-- Edge Gateway -->
    <rect x="10" y="48" width="178" height="110" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="18" y="68" fill="#0A192F" font-size="11" font-weight="800">FastAPI Gateway</text>
    <text x="18" y="86" fill="#475569" font-size="9.5">• URBANGEN_API_KEY</text>
    <text x="18" y="102" fill="#475569" font-size="9.5">• SlowAPI Token Bucket</text>
    <text x="18" y="118" fill="#475569" font-size="9.5">• Magic-Byte Sanitization</text>
    <text x="18" y="134" fill="#475569" font-size="9.5">• Clamped 128×128 / &lt;10MB</text>
    <text x="18" y="150" fill="#0284C7" font-size="9" font-weight="700">Hardened Against DDoS</text>

    <!-- Green AI Compute -->
    <rect x="10" y="168" width="178" height="125" rx="6" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.2"/>
    <text x="18" y="188" fill="#065F46" font-size="11" font-weight="800">Green AI Edge Compute</text>
    <text x="18" y="206" fill="#047857" font-size="9.5">• 100% On-Premises</text>
    <text x="18" y="222" fill="#334155" font-size="9.5">• NVIDIA RTX 4050 6GB</text>
    <text x="18" y="238" fill="#334155" font-size="9.5">• 0.133 kWh Total Energy</text>
    <text x="18" y="254" fill="#334155" font-size="9.5">• 94.8 g CO₂e Footprint</text>
    <text x="18" y="274" fill="#065F46" font-size="9" font-weight="800">Zero Cloud GIS Leakage</text>

    <!-- Governance -->
    <rect x="10" y="303" width="178" height="101" rx="6" fill="#FEF2F2" stroke="#FECDD3" stroke-width="1.2"/>
    <text x="18" y="323" fill="#9F1239" font-size="10.5" font-weight="800">Human-in-the-Loop</text>
    <text x="18" y="341" fill="#475569" font-size="9.5">• Advisory Planning Support</text>
    <text x="18" y="357" fill="#475569" font-size="9.5">• Autonomous Zoning</text>
    <text x="18" y="371" fill="#475569" font-size="9.5">  Enforcement Prohibited</text>
    <text x="18" y="391" fill="#BE123C" font-size="9" font-weight="700">Audit-Compliant AI</text>
  </g>

</svg>
"""

    targets = [
        "docs/poster/figures",
        "frontend/public/poster/figures"
    ]

    for t in targets:
        os.makedirs(t, exist_ok=True)
        svg_file = os.path.join(t, "full_project_architecture_plantuml.svg")
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Saved SVG: {svg_file}")

        # Also save as pipeline_architecture_plantuml.svg
        pipe_svg = os.path.join(t, "pipeline_architecture_plantuml.svg")
        with open(pipe_svg, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Saved SVG: {pipe_svg}")

    # Now render a 300 DPI PNG (2400 x 675) using PIL with crisp text and boxes
    png_w = 2400
    png_h = 675
    im = Image.new("RGB", (png_w, png_h), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Outer border
    draw.rounded_rectangle([(3, 3), (png_w - 4, png_h - 4)], radius=15, fill=(255, 255, 255), outline=(226, 232, 240), width=3)

    # Let's draw the 6 stages onto the PNG image
    stages = [
        {"x": 24, "w": 345, "title": "1. REMOTE SENSING INPUT", "hdr_bg": (2, 132, 199), "card_bg": (240, 249, 255), "border": (186, 230, 253)},
        {"x": 393, "w": 354, "title": "2. SIGNAL RESTORATION", "hdr_bg": (5, 150, 105), "card_bg": (236, 253, 245), "border": (167, 243, 208)},
        {"x": 771, "w": 375, "title": "3. MANIFOLD & AUDIT", "hdr_bg": (124, 58, 237), "card_bg": (245, 243, 255), "border": (221, 214, 254)},
        {"x": 1170, "w": 375, "title": "4. GENERATIVE SYNTHESIS", "hdr_bg": (217, 119, 6), "card_bg": (255, 251, 235), "border": (253, 230, 138)},
        {"x": 1569, "w": 354, "title": "5. GROUNDED POLICY ENGINE", "hdr_bg": (4, 120, 87), "card_bg": (236, 253, 245), "border": (167, 243, 208)},
        {"x": 1947, "w": 429, "title": "6. SECURITY & HARDWARE", "hdr_bg": (10, 25, 47), "card_bg": (248, 250, 252), "border": (203, 213, 225)}
    ]

    for s in stages:
        sx = s["x"]
        sy = 24
        sw = s["w"]
        sh = png_h - 48
        draw.rounded_rectangle([(sx, sy), (sx + sw, sy + sh)], radius=12, fill=s["card_bg"], outline=s["border"], width=2)
        # Header bar
        draw.rounded_rectangle([(sx + 15, sy + 15), (sx + sw - 15, sy + 58)], radius=8, fill=s["hdr_bg"])
        draw.text((sx + sw / 2, sy + 25), s["title"], fill=(255, 255, 255), anchor="mt")

    # Stage 1 Content
    draw.rounded_rectangle([(39, 90), (354, 310)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((54, 105), "USGS UCMerced Dataset", fill=(10, 25, 47))
    draw.text((54, 135), "• 2,100 Orthoimagery Tiles\n• 256x256 px, 0.3m GSD\n• 21 Urban Land-Use Classes\n• Stratified 90% Train / 10% Val", fill=(71, 85, 105))
    draw.rounded_rectangle([(54, 250), (339, 295)], radius=6, fill=(224, 242, 254))
    draw.text((196, 262), "Split: 1,890 / 210", fill=(3, 105, 161), anchor="mt")

    draw.rounded_rectangle([(39, 325), (354, png_h - 40)], radius=8, fill=(255, 241, 242), outline=(254, 205, 211), width=2)
    draw.text((54, 340), "Atmospheric Noise (sigma=0.15)", fill=(225, 29, 72))
    draw.text((54, 370), "• Synthetic Cloud Shadowing\n• Corrupted x in R^(128x128x3)\n• Degraded Baseline: 22.65 dB", fill=(71, 85, 105))

    # Stage 2 Content
    draw.rounded_rectangle([(408, 90), (732, png_h - 40)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((423, 105), "Model 1: Denoising AE (U-Net)", fill=(6, 95, 70))
    draw.text((423, 135), "• Multi-Scale Skip Connections\n• Stem -> L1 -> L2 -> L3 -> Bottleneck\n• Transposed Conv Decoders", fill=(71, 85, 105))
    draw.rounded_rectangle([(423, 220), (717, 290)], radius=6, fill=(248, 250, 252), outline=(226, 232, 240))
    draw.text((438, 235), "L_AE = (1/N) * sum ||x - x_hat||^2\nLoss: 0.00449 MSE (0.00617)", fill=(5, 150, 105))
    draw.rounded_rectangle([(423, 310), (717, 430)], radius=8, fill=(220, 252, 231), outline=(134, 239, 172))
    draw.text((438, 325), "PSNR: 29.65 dB (+7.0 dB Gain)\nSSIM: 0.8649 (Crisp Boundaries)\nOutput: Restored Tile (128x128x3)", fill=(6, 95, 70))

    # Stage 3 Content
    draw.rounded_rectangle([(786, 90), (1131, 335)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((801, 105), "Model 2: Spatial beta-VAE", fill=(109, 40, 217))
    draw.text((801, 135), "• Latent z in R^(64x8x8) preserves 2D\n• 4-Stage Transposed Conv Decoder\n• L_VAE: 0.0483 (KL: 60.72 nats)\n• PSNR: 27.49 dB | Smooth Manifold", fill=(71, 85, 105))
    draw.rounded_rectangle([(801, 245), (1116, 315)], radius=6, fill=(237, 233, 254))
    draw.text((816, 258), "Anomaly Detector: Disparity > 3sigma\nIdentifies unpermitted urban sprawl", fill=(91, 33, 182))

    draw.rounded_rectangle([(786, 350), (1131, png_h - 40)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((801, 365), "Model 3: Land-Use Classifier", fill=(2, 132, 199))
    draw.text((801, 395), "• ResNet-18 Backbone (21 Classes)\n• L_CE: 0.0615 | Val Acc: 98.10% | F1: 0.9784\n• Provides verified class condition y", fill=(71, 85, 105))

    # Stage 4 Content
    draw.rounded_rectangle([(1185, 90), (1530, 335)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((1200, 105), "Model 4: Residual cDCGAN", fill=(180, 83, 9))
    draw.text((1200, 135), "• 4x ResUpBlock Gen + Proj Disc\n• Spectral Norm + AC-GAN Head\n• Minimax Eq: D=1.67, G=1.19\n• Proxy Recognition: 99.40%", fill=(71, 85, 105))
    draw.rounded_rectangle([(1200, 245), (1515, 315)], radius=6, fill=(254, 243, 199))
    draw.text((1215, 260), "Edge Latency: <35 ms\nFast Generative Augmentation", fill=(146, 64, 14))

    draw.rounded_rectangle([(1185, 350), (1530, png_h - 40)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((1200, 365), "Model 5: Conditional DDPM", fill=(225, 29, 72))
    draw.text((1200, 395), "• Time/Class U-Net (20-Step DDIM)\n• 5 Losses (Noise MSE: 0.0304)\n• 1.82s Latency (15.6x Accelerated)", fill=(71, 85, 105))

    # Stage 5 Content
    draw.rounded_rectangle([(1584, 90), (1908, png_h - 40)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((1599, 105), "Model 6: Urban Plan (MiniGPT)", fill=(6, 95, 70))
    draw.text((1599, 135), "• 4-Layer Causal Transformer\n• d_model=256, 4 Heads, Context T=192\n• PMC Development Control Rules\n• L_causal: 0.10430 | PPL: 1.110 | 0.1505 BPC", fill=(71, 85, 105))
    draw.rounded_rectangle([(1599, 250), (1893, png_h - 55)], radius=8, fill=(209, 250, 229), outline=(110, 231, 183))
    draw.text((1614, 265), "Grounded Municipal Directives:\n• Base FSI 1.8-2.4 along transit spines\n• 15% Riverbank Green Buffer (TOD)\n• Mandatory Solar/Rainwater (>1000m²)", fill=(6, 95, 70))

    # Stage 6 Content
    draw.rounded_rectangle([(1962, 90), (2361, 230)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((1977, 105), "FastAPI Edge Gateway", fill=(10, 25, 47))
    draw.text((1977, 135), "• URBANGEN_API_KEY Authentication\n• SlowAPI Token Bucket Rate Limiting\n• Magic-Byte File Inspection (<10MB)\n• Input Clamped to 128x128 px", fill=(71, 85, 105))

    draw.rounded_rectangle([(1962, 245), (2361, 440)], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=2)
    draw.text((1977, 260), "Air-Gapped Green AI Edge Compute", fill=(6, 95, 70))
    draw.text((1977, 290), "• 100% On-Premises RTX 4050 6GB\n• 0.133 kWh Total Energy (94.8 g CO2e)\n• Zero Cloud GIS Leakage (Sovereign)", fill=(71, 85, 105))

    draw.rounded_rectangle([(1962, 455), (2361, png_h - 40)], radius=8, fill=(254, 242, 242), outline=(254, 205, 211), width=2)
    draw.text((1977, 470), "Human-in-the-Loop Governance: Advisory only. Autonomous enforcement prohibited.", fill=(159, 18, 57))

    for t in targets:
        png_file = os.path.join(t, "full_project_architecture_plantuml.png")
        pipe_png = os.path.join(t, "pipeline_architecture_plantuml.png")
        im.save(png_file, "PNG")
        im.save(pipe_png, "PNG")
        print(f"Saved PNG: {png_file} and {pipe_png} ({im.width} x {im.height})")

if __name__ == "__main__":
    build_vector_diagram()

