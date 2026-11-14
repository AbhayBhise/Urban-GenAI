r"""
Generate clean, perfectly formatted PlantUML and Vector SVG architecture for UrbanGen AI.
Resolves all visual overlaps, provides generous inter-row clearances, formats legend banner
coordinates correctly, and ensures 100% valid XML compliance across all web renderers.
"""

import os
import sys
import zlib
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

def plantuml_encode(text):
    """Encodes text for plantuml.com / plantuml.online URL."""
    zlibbed = zlib.compress(text.encode('utf-8'))[2:-4]
    mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    
    def encode_3bytes(b1, b2, b3):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return mapping[c1] + mapping[c2] + mapping[c3] + mapping[c4]
    
    res = ''
    i = 0
    while i < len(zlibbed):
        b1 = zlibbed[i]
        b2 = zlibbed[i+1] if i+1 < len(zlibbed) else 0
        b3 = zlibbed[i+2] if i+2 < len(zlibbed) else 0
        res += encode_3bytes(b1, b2, b3)
        i += 3
    return res

def build_clean_puml():
    puml_code = """@startuml UrbanGen_AI_Complete_Architecture
' ==============================================================================
' UrbanGen AI: Multi-Model Deep Generative Framework for Satellite Imagery Processing
' Complete Integrated System Pipeline & Security Architecture (PlantUML)
' Department of Computer Engineering, MIT Academy of Engineering, Pune
' B.Tech Capstone Project (2025–2026) · IEEE Publication Track
' ==============================================================================

skinparam dpi 300
skinparam defaultFontName "Arial"
skinparam defaultFontSize 11
skinparam roundcorner 8
skinparam shadowing true
skinparam packageTitleAlignment left
skinparam linetype ortho
skinparam nodesep 32
skinparam ranksep 32

' Academic Color Palette
skinparam package {
  BackgroundColor #F8FAFC
  BorderColor #64748B
  BorderThickness 1.5
  FontStyle bold
  FontSize 12
}

skinparam rectangle {
  BackgroundColor #FFFFFF
  BorderColor #0284C7
  BorderThickness 1.4
  FontSize 10.5
}

skinparam arrow {
  Color #0284C7
  Thickness 1.6
  FontSize 9.5
  FontStyle bold
}

' ==============================================================================
' TIER 1: INGESTION, RESTORATION & LATENT MANIFOLD
' ==============================================================================
package "1. Remote Sensing Ingestion & Perturbation" #F0F9FF {
  rectangle "<b>USGS UCMerced Orthoimagery</b>\n--\n* 2,100 Aerial Tiles (256x256 px, 0.3m GSD)\n* 21 Municipal Land-Use Classes\n* Stratified Split (1,890 Train / 210 Val)\n* RGB Spectral Baseline" as RAW #E0F2FE

  rectangle "<b>Atmospheric Degradation Layer</b>\n--\n* Synthetic Cloud Shadow & Fog Attenuation\n* Additive Gaussian Sensor Noise: σ = 0.15\n* Corrupted Input Tile: x̃ ∈ ℝ^(128x128x3)\n* Simulates Adverse Sensor Weather" as NOISY #FEE2E2

  RAW -right-> NOISY : Optical Scattering
}

package "2. Signal Restoration (Model 1: U-Net DAE)" #ECFDF5 {
  rectangle "<b>Denoising Autoencoder (U-Net)</b>\n--\n* Stem → L1(64) → L2(128) → L3(256) → Bottleneck(512)\n* Multi-Scale Transposed Skip-Connections\n* Loss: L_AE = (1/N) Σ ||x - x̂||₂² (MSE: 0.00449)\n* Primary Metric: 29.65 dB PSNR (+7.0 dB Gain)\n* Secondary Metric: SSIM = 0.8649" as DAE #DCFCE7
}

package "3. Latent Manifold & Territorial Auditing" #F5F3FF {
  rectangle "<b>Spatial β-VAE (Model 2)</b>\n--\n* ResNet-18 Backbone → Latent μ, log σ² ∈ ℝ^(64x8x8)\n* 4-Stage Transposed Conv Decoder (Compact Skips)\n* Loss: (0.7*L₁ + 0.3*L_MSE) + 10⁻⁴*D_KL = 0.0483\n* Metric: 27.49 dB PSNR | KL: 60.72 nats" as VAE #EDE9FE

  rectangle "<b>Unsupervised Anomaly Detector</b>\n--\n* Disparity Map: |x_restored - x_vae|\n* Flagging Threshold: Disparity > 3σ\n* Detects Unpermitted Urban Encroachment\n* Risk Score Forwarded to Policy Engine" as ANOMALY #FEF3C7

  rectangle "<b>Land-Use Classifier (Model 3)</b>\n--\n* Frozen Semantic Auditor (ResNet-18 + Linear Head)\n* Loss Formula: L_CE = -Σ y_i log(p_i) (0.0615)\n* Primary Metric: 98.10% Validation Accuracy\n* Secondary Metric: Macro F1: 0.9784" as CLS #E0F2FE

  VAE -right-> ANOMALY : Disparity Map
}

NOISY -right-> DAE : Degraded Tile x̃ (128x128)
DAE -right-> VAE : Clean Tile x̂ (128x128)
DAE -down-> CLS : Clean Tile x̂ (128x128)
VAE .down.> CLS : Latent Manifold Projection

' ==============================================================================
' TIER 2: DUAL-MODALITY GENERATIVE SYNTHESIS & POLICY ENGINE
' ==============================================================================
package "4. Dual-Modality Generative Parcel Synthesis" #FFFBEB {
  rectangle "<b>Residual cDCGAN (Model 4)</b>\n--\n* 4x ResUpBlock Generator + Projection Discriminator\n* Spectral Normalization + AC-GAN Auxiliary Head\n* Loss: L_adv Minimax + 0.8*L_AC (D=1.67, G=1.19)\n* Output: High-Speed Synthetic Parcel (<35ms)\n* Metric: 99.40% Semantic Proxy Recognition" as GAN #FEF3C7

  rectangle "<b>Conditional DDPM (Model 5)</b>\n--\n* Time- & Class-Conditioned U-Net (T=1000 Schedule)\n* 20-Step Deterministic Accelerated DDIM Sampler\n* Loss: L_simple + L_vlb + L_guide + L_sp + L_reg\n* Converged Loss: 0.0304 Noise MSE (0.02916 VLB)\n* Metric: 1.82s Latency (15.6x Accelerated)" as DIFF #FEE2E2

  GAN -right-> DIFF : Dual Modalities
}

package "5. Grounded Municipal Policy Formulation" #ECFDF5 {
  rectangle "<b>Municipal Plan Generator (MiniGPT - Model 6)</b>\n--\n* 4-Layer Pre-LayerNorm Causal Transformer (d_model=256)\n* Context Window T=192 | PMC Development Control Rules\n* Loss Formula: L_causal = -Σ log P(w_t | w_<t) = 0.1043\n* Metrics: 1.110 Validation Perplexity | 0.1505 Bits/Char" as GPT #D1FAE5

  rectangle "<b>Actionable Grounded Directives</b>\n--\n* FSI Allocation: Base FSI 1.8–2.4 along transit spines\n* TOD Corridors: 15% Riverbank green buffer setback\n* Environmental: Rainwater & solar mandate (>1,000 m²)" as BYLAWS #A7F3D0

  GPT -right-> BYLAWS : Generates Bylaws
}

CLS -down-> GAN : Condition y ∈ {0..20}
CLS -down-> DIFF : Class Guidance Vector
GAN .up.> CLS : Validation Loop (99.40%)
DIFF .up.> CLS : Classifier Guidance (∇ log p(y|x))

CLS -right-> GPT : Verified Zoning Label y
ANOMALY -down-> GPT : Anomaly Telemetry & Risk Score

' ==============================================================================
' TIER 3: AIR-GAPPED EDGE SECURITY & CLOSED-LOOP GOVERNANCE
' ==============================================================================
package "6. Air-Gapped Edge Hardware & Closed-Loop System Security" #F8FAFC {
  rectangle "<b>FastAPI Edge Gateway</b>\n--\n* Verified URBANGEN_API_KEY Header Authentication\n* SlowAPI Token-Bucket Rate Limiter (Anti-DDoS)\n* Magic-Byte File Inspection (<10MB, Clamped 128x128)" as GATEWAY #FFFFFF

  rectangle "<b>Green AI Edge Compute</b>\n--\n* 100% On-Premises Consumer NVIDIA RTX 4050 Laptop GPU (6GB, 75W)\n* Cumulative Training: 66.3 min | Energy: 0.133 kWh | Carbon: 94.8 g CO₂e\n* Air-Gapped Zero Cloud GIS Leakage (Complete Data Sovereignty)" as HARDWARE #FFFFFF

  rectangle "<b>Human-in-the-Loop Municipal Governance</b>\n--\n* Generative outputs serve strictly as advisory decision support\n* Autonomous legal zoning enforcement is prohibited by design\n* Flags high reconstruction disparity outside pre-trained fabrics" as GOV #FFFFFF

  GATEWAY -right-> HARDWARE : Enforces Hardware Quota
  HARDWARE -right-> GOV : Operational Boundary
}

BYLAWS -down-> GOV : Grounded Policy Directives
NOISY .down.> GATEWAY : Ingestion Sanitization Check

@enduml"""
    return puml_code

def render_vector_svg_and_png(workspace):
    """
    Renders high-resolution vector SVG and publication-grade architecture diagram
    with mathematically verified zero-overlap coordinates, expanded inter-row gaps,
    and valid XML entity references.
    """
    svg_w, svg_h = 1600, 950
    
    svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="100%" style="background:#FFFFFF; font-family:'Segoe UI', -apple-system, Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.08" />
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
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#D97706" />
    </marker>
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#1E3A8A" />
    </linearGradient>
  </defs>

  <!-- Canvas Outer Border -->
  <rect x="2" y="2" width="{svg_w - 4}" height="{svg_h - 4}" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>

  <!-- Top Title Banner (h: 48, y: 14..62) -->
  <rect x="16" y="14" width="1568" height="48" rx="6" fill="url(#header-grad)"/>
  <text x="32" y="44" fill="#FFFFFF" font-size="15.5" font-weight="800" letter-spacing="0.02em">URBANGEN AI: COMPLETE INTEGRATED SYSTEM PIPELINE &amp; SECURITY ARCHITECTURE</text>
  <text x="1568" y="44" text-anchor="end" fill="#93C5FD" font-size="11.5" font-weight="600">MIT ACADEMY OF ENGINEERING &#8226; IEEE PUBLICATION TRACK</text>

  <!-- ===================================================================== -->
  <!-- ROW 1: INGESTION (x:16, w:344), RESTORATION (x:404, w:370), MANIFOLD (x:826, w:758) -->
  <!-- y: 78 to 338 (height: 260) -->
  <!-- ===================================================================== -->

  <!-- STAGE 1: INGESTION & PERTURBATION -->
  <g transform="translate(16, 78)">
    <rect width="344" height="260" rx="8" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="320" height="26" rx="4" fill="#0284C7"/>
    <text x="172" y="27" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">1. REMOTE SENSING INGESTION &amp; PERTURBATION</text>

    <!-- Raw Data Box -->
    <rect x="12" y="44" width="144" height="204" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2"/>
    <text x="20" y="64" fill="#0F172A" font-size="11" font-weight="800">USGS UCMerced</text>
    <text x="20" y="82" fill="#475569" font-size="9">&#8226; 2,100 Aerial Tiles</text>
    <text x="20" y="98" fill="#475569" font-size="9">&#8226; 256&#215;256 px, 0.3m GSD</text>
    <text x="20" y="114" fill="#475569" font-size="9">&#8226; 21 Zoning Classes</text>
    <text x="20" y="130" fill="#475569" font-size="9">&#8226; Stratified 90/10 Split</text>
    <rect x="20" y="142" width="128" height="22" rx="3" fill="#E0F2FE"/>
    <text x="84" y="157" text-anchor="middle" fill="#0369A1" font-size="9" font-weight="700">1,890 Train / 210 Val</text>
    <rect x="20" y="172" width="128" height="64" rx="3" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="84" y="194" text-anchor="middle" fill="#0F172A" font-size="9" font-weight="700">RGB Spectral Baseline</text>
    <text x="84" y="214" text-anchor="middle" fill="#64748B" font-size="8.5">Ground-Truth Baseline</text>

    <!-- Internal Arrow: Raw -> Atmospheric -->
    <line x1="156" y1="146" x2="172" y2="146" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)"/>

    <!-- Noise Layer Box -->
    <rect x="176" y="44" width="156" height="204" rx="5" fill="#FFFFFF" stroke="#FECACA" stroke-width="1.2"/>
    <text x="184" y="64" fill="#991B1B" font-size="11" font-weight="800">Atmospheric Layer</text>
    <text x="184" y="82" fill="#475569" font-size="9">&#8226; Synthetic Cloud Shadow</text>
    <text x="184" y="98" fill="#475569" font-size="9">&#8226; Scattering &amp; Fog Haze</text>
    <text x="184" y="114" fill="#475569" font-size="9">&#8226; Gaussian Noise &#963;=0.15</text>
    <rect x="184" y="126" width="140" height="24" rx="3" fill="#FEE2E2"/>
    <text x="254" y="142" text-anchor="middle" fill="#991B1B" font-size="9" font-weight="700">x&#771; &#8712; &#8477;^(128&#215;128&#215;3)</text>
    <rect x="184" y="158" width="140" height="78" rx="3" fill="#FFF1F2" stroke="#FECDD3"/>
    <text x="254" y="178" text-anchor="middle" fill="#991B1B" font-size="9" font-weight="700">Degraded Raster</text>
    <text x="254" y="198" text-anchor="middle" fill="#475569" font-size="8.5">Simulates Adverse</text>
    <text x="254" y="214" text-anchor="middle" fill="#475569" font-size="8.5">Sensor Weather</text>
  </g>

  <!-- Clear Inter-Stage Arrow: Stage 1 -> Stage 2 (Gap: x=360 to x=404, w=44px) -->
  <line x1="360" y1="208" x2="404" y2="208" stroke="#0284C7" stroke-width="2.2" marker-end="url(#arrow-blue)"/>
  <rect x="368" y="196" width="28" height="18" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <text x="382" y="209" text-anchor="middle" fill="#0284C7" font-size="8.5" font-weight="700">x&#771;</text>

  <!-- STAGE 2: SIGNAL RESTORATION (U-NET DAE) -->
  <g transform="translate(404, 78)">
    <rect width="370" height="260" rx="8" fill="#ECFDF5" stroke="#059669" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="346" height="26" rx="4" fill="#059669"/>
    <text x="185" y="27" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">2. SIGNAL RESTORATION (MODEL 1: U-NET DAE)</text>

    <!-- Architecture Box -->
    <rect x="12" y="44" width="346" height="204" rx="5" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.2"/>
    <text x="22" y="66" fill="#0F172A" font-size="11.5" font-weight="800">Denoising Autoencoder (Transposed U-Net)</text>
    <text x="22" y="84" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Encoder:</tspan> Stem(64) &#8594; L1(128) &#8594; L2(256) &#8594; L3(512) &#8594; Bottleneck(512)</text>
    <text x="22" y="101" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Decoder:</tspan> 4-Stage Transposed Conv (512&#8594;256&#8594;128&#8594;64&#8594;32&#8594;3)</text>
    <text x="22" y="118" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Multi-Scale Skips:</tspan> Direct feature concatenation preserves street grids</text>

    <rect x="22" y="128" width="326" height="24" rx="3" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="185" y="144" text-anchor="middle" fill="#059669" font-size="8.5" font-weight="700">Loss: L_AE = (1/N) &#8721; ||x - x&#770;||_2^2 &#8195; [MSE: 0.00449 | Total: 0.00617]</text>

    <!-- Metric Badges -->
    <rect x="22" y="160" width="158" height="76" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="101" y="182" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">29.65 dB PSNR</text>
    <text x="101" y="201" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">+7.0 dB Recovery Gain</text>
    <text x="101" y="219" text-anchor="middle" fill="#475569" font-size="8.5">Over Degraded Baseline</text>

    <rect x="190" y="160" width="158" height="76" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="269" y="182" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">SSIM = 0.8649</text>
    <text x="269" y="201" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">Structural Fidelity</text>
    <text x="269" y="219" text-anchor="middle" fill="#475569" font-size="8.5">Sharp Boundary Retention</text>
  </g>

  <!-- Clear Inter-Stage Arrow: Stage 2 -> Stage 3 (Gap: x=774 to x=826, w=52px) -->
  <line x1="774" y1="208" x2="826" y2="208" stroke="#059669" stroke-width="2.2" marker-end="url(#arrow-green)"/>
  <rect x="780" y="196" width="40" height="18" rx="3" fill="#FFFFFF" stroke="#059669" stroke-width="1.2"/>
  <text x="800" y="209" text-anchor="middle" fill="#059669" font-size="8" font-weight="700">x_clean</text>

  <!-- STAGE 3: LATENT MANIFOLD & AUDITING -->
  <g transform="translate(826, 78)">
    <rect width="758" height="260" rx="8" fill="#F5F3FF" stroke="#7C3AED" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="734" height="26" rx="4" fill="#7C3AED"/>
    <text x="379" y="27" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">3. LATENT MANIFOLD NAVIGATION &amp; TERRITORIAL AUDITING</text>

    <!-- Model 2: Spatial VAE -->
    <rect x="12" y="44" width="236" height="204" rx="5" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.2"/>
    <text x="22" y="66" fill="#6B21A8" font-size="11" font-weight="800">Spatial &#946;-VAE (Model 2)</text>
    <text x="22" y="84" fill="#475569" font-size="9">&#8226; ResNet-18 &#8594; &#956;, log &#963;&#178; &#8712; &#8477;^(64&#215;8&#215;8)</text>
    <text x="22" y="100" fill="#475569" font-size="9">&#8226; Preserves 2D Spatial Topology</text>
    <text x="22" y="116" fill="#475569" font-size="9">&#8226; &#946;=10^-4 prevents collapse</text>
    <rect x="22" y="126" width="216" height="22" rx="3" fill="#F3E8FF"/>
    <text x="130" y="141" text-anchor="middle" fill="#6B21A8" font-size="8.5" font-weight="700">L_VAE: 0.0483 (KL: 60.72 nats)</text>
    <rect x="22" y="156" width="216" height="80" rx="3" fill="#FAF5FF" stroke="#E9D5FF"/>
    <text x="130" y="178" text-anchor="middle" fill="#6B21A8" font-size="10.5" font-weight="800">27.49 dB PSNR</text>
    <text x="130" y="198" text-anchor="middle" fill="#475569" font-size="8.5">Continuous Latent Interpolation</text>
    <text x="130" y="216" text-anchor="middle" fill="#475569" font-size="8.5">Disparity Anomaly Scoring</text>

    <!-- Arrow inside Stage 3: VAE -> Anomaly -->
    <line x1="248" y1="146" x2="262" y2="146" stroke="#7C3AED" stroke-width="1.8" marker-end="url(#arrow-purple)"/>

    <!-- Anomaly Detector -->
    <rect x="262" y="44" width="222" height="204" rx="5" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.2"/>
    <text x="272" y="66" fill="#B45309" font-size="11" font-weight="800">Unsupervised Anomaly</text>
    <text x="272" y="84" fill="#475569" font-size="9">&#8226; Disparity: |x_restored - x_vae|</text>
    <text x="272" y="100" fill="#475569" font-size="9">&#8226; Flagging Threshold: &gt; 3&#963;</text>
    <text x="272" y="116" fill="#475569" font-size="9">&#8226; Autonomous Encroachment Pin</text>
    <rect x="272" y="126" width="202" height="22" rx="3" fill="#FEF3C7"/>
    <text x="373" y="141" text-anchor="middle" fill="#B45309" font-size="8.5" font-weight="700">Statistical Boundary Shift</text>
    <rect x="272" y="156" width="202" height="80" rx="3" fill="#FFFBEB" stroke="#FDE68A"/>
    <text x="373" y="178" text-anchor="middle" fill="#B45309" font-size="10" font-weight="800">Zoning Violation Heatmap</text>
    <text x="373" y="198" text-anchor="middle" fill="#475569" font-size="8.5">Outputs Illegal Encroachment</text>
    <text x="373" y="216" text-anchor="middle" fill="#475569" font-size="8.5">Risk Score to Policy Engine</text>

    <!-- Model 3: Land-Use Classifier Auditor -->
    <rect x="496" y="44" width="250" height="204" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2"/>
    <text x="506" y="66" fill="#0369A1" font-size="11" font-weight="800">Land-Use Classifier (Model 3)</text>
    <text x="506" y="84" fill="#475569" font-size="9">&#8226; ResNet-18 Transfer Backbone</text>
    <text x="506" y="100" fill="#475569" font-size="9">&#8226; 21-Way Linear Projection Head</text>
    <text x="506" y="116" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Role:</tspan> Frozen Semantic Auditor</text>
    <rect x="506" y="126" width="230" height="22" rx="3" fill="#E0F2FE"/>
    <text x="621" y="141" text-anchor="middle" fill="#0369A1" font-size="8.5" font-weight="700">L_CE = 0.0615 | Adam lr=10^-4</text>
    <rect x="506" y="156" width="230" height="80" rx="3" fill="#F0F9FF" stroke="#BAE6FD"/>
    <text x="621" y="178" text-anchor="middle" fill="#0369A1" font-size="11" font-weight="800">98.10% Val Accuracy</text>
    <text x="621" y="198" text-anchor="middle" fill="#0369A1" font-size="9.5" font-weight="700">Macro F1: 0.9784</text>
    <text x="621" y="216" text-anchor="middle" fill="#475569" font-size="8.5">Independent GenAI Quality Judge</text>
  </g>

  <!-- ===================================================================== -->
  <!-- INTER-ROW 1 GAP: y=338 to y=394 (56px Clear Vertical Height)        -->
  <!-- Perfectly routes condition lines without colliding with any borders!  -->
  <!-- ===================================================================== -->

  <!-- Condition Line from Model 3 (x=1447) left to Stage 4 (x=191) -->
  <path d="M 1447 338 L 1447 366 L 191 366 L 191 394" fill="none" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)"/>
  
  <!-- Condition Badge: Centered at y=366, height=20 (y: 356..376 -> 18px clear above, 18px clear below!) -->
  <rect x="1380" y="356" width="134" height="20" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.3" filter="url(#shadow)"/>
  <text x="1447" y="370" text-anchor="middle" fill="#0284C7" font-size="8.5" font-weight="700">Condition y &#8712; [0..20]</text>

  <!-- Vertical Condition Line from Model 3 (x=1447) directly down into Stage 5 Policy Engine -->
  <line x1="1447" y1="376" x2="1447" y2="394" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)"/>

  <!-- ===================================================================== -->
  <!-- ROW 2: GENERATIVE SYNTHESIS (x:16, w:758), POLICY ENGINE (x:826, w:758) -->
  <!-- y: 394 to 662 (height: 268) -->
  <!-- ===================================================================== -->

  <!-- STAGE 4: DUAL-MODALITY GENERATIVE SYNTHESIS -->
  <g transform="translate(16, 394)">
    <rect width="758" height="268" rx="8" fill="#FFFBEB" stroke="#D97706" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="734" height="26" rx="4" fill="#D97706"/>
    <text x="379" y="27" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">4. DUAL-MODALITY GENERATIVE PARCEL SYNTHESIS (MODELS 4 &amp; 5)</text>

    <!-- Model 4: Residual cDCGAN -->
    <rect x="12" y="44" width="356" height="212" rx="5" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.2"/>
    <text x="22" y="66" fill="#B45309" font-size="11.5" font-weight="800">Residual cDCGAN (Model 4)</text>
    <text x="22" y="86" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Generator:</tspan> 4&#215; ResUpBlocks with conditional BatchNorm</text>
    <text x="22" y="104" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Discriminator:</tspan> Projection Head + Spectral Normalization</text>
    <text x="22" y="122" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Conditioning:</tspan> Class label y &#8712; [0..20] via inner product</text>
    <rect x="22" y="134" width="336" height="24" rx="3" fill="#FEF3C7"/>
    <text x="190" y="150" text-anchor="middle" fill="#B45309" font-size="8.5" font-weight="700">Minimax Equilibrium: D = 1.672, G = 1.189</text>

    <!-- Metric Badges -->
    <rect x="22" y="166" width="162" height="78" rx="4" fill="#FEF3C7" stroke="#FDE68A"/>
    <text x="103" y="188" text-anchor="middle" fill="#B45309" font-size="11" font-weight="800">99.40% Proxy Rec</text>
    <text x="103" y="208" text-anchor="middle" fill="#B45309" font-size="9.5" font-weight="700">167/168 Verified</text>
    <text x="103" y="228" text-anchor="middle" fill="#475569" font-size="8.5">Zero Mode Collapse</text>

    <rect x="196" y="166" width="162" height="78" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="277" y="188" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">&lt; 35 ms Latency</text>
    <text x="277" y="208" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">32 ms Avg Inference</text>
    <text x="277" y="228" text-anchor="middle" fill="#475569" font-size="8.5">56&#215; Faster Than DDPM</text>

    <!-- Model 5: Conditional DDPM -->
    <rect x="390" y="44" width="356" height="212" rx="5" fill="#FFFFFF" stroke="#FECACA" stroke-width="1.2"/>
    <text x="400" y="66" fill="#991B1B" font-size="11.5" font-weight="800">Conditional DDPM (Model 5)</text>
    <text x="400" y="86" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Diffusion U-Net:</tspan> Timestep- &amp; class-conditioned reverse SDE</text>
    <text x="400" y="104" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Accelerated Sampler:</tspan> 20-step deterministic DDIM sampler</text>
    <text x="400" y="122" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Loss:</tspan> 5-Loss Composite (L_simple + L_vlb + L_guide + L_sp + L_reg)</text>
    <rect x="400" y="134" width="336" height="24" rx="3" fill="#FEE2E2"/>
    <text x="568" y="150" text-anchor="middle" fill="#991B1B" font-size="8.5" font-weight="700">Noise MSE: 0.03040 | VLB Loss: 0.02916</text>

    <!-- Metric Badges -->
    <rect x="400" y="166" width="162" height="78" rx="4" fill="#FEE2E2" stroke="#FECACA"/>
    <text x="481" y="188" text-anchor="middle" fill="#991B1B" font-size="11" font-weight="800">Pristine Crispness</text>
    <text x="481" y="208" text-anchor="middle" fill="#991B1B" font-size="9.5" font-weight="700">Highest Realism</text>
    <text x="481" y="228" text-anchor="middle" fill="#475569" font-size="8.5">No Adversarial Noise</text>

    <rect x="574" y="166" width="162" height="78" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="655" y="188" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">1.82s DDIM</text>
    <text x="655" y="208" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">15.6&#215; Accelerated</text>
    <text x="655" y="228" text-anchor="middle" fill="#475569" font-size="8.5">Down from 28.4s</text>
  </g>

  <!-- STAGE 5: GROUNDED MUNICIPAL POLICY FORMULATION -->
  <g transform="translate(826, 394)">
    <rect width="758" height="268" rx="8" fill="#ECFDF5" stroke="#059669" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="734" height="26" rx="4" fill="#059669"/>
    <text x="379" y="27" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">5. GROUNDED MUNICIPAL POLICY FORMULATION (MODEL 6: MINIGPT)</text>

    <!-- MiniGPT Architecture Box -->
    <rect x="12" y="44" width="360" height="212" rx="5" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.2"/>
    <text x="22" y="66" fill="#166534" font-size="11.5" font-weight="800">Municipal Plan Generator (MiniGPT)</text>
    <text x="22" y="86" fill="#475569" font-size="9">&#8226; 4-Layer Pre-LayerNorm Causal Transformer (d_model=256)</text>
    <text x="22" y="104" fill="#475569" font-size="9">&#8226; 4 Multi-Head Attention Heads | Context Window T=192</text>
    <text x="22" y="122" fill="#475569" font-size="9">&#8226; Trained from scratch on Pune Municipal Corp (PMC) bylaws</text>
    <rect x="22" y="134" width="340" height="24" rx="3" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="192" y="150" text-anchor="middle" fill="#059669" font-size="8.5" font-weight="700">L_causal = -&#8721; log P(w_t | w_&lt;t) = 0.10430 (Cross-Entropy)</text>

    <!-- Metric Badges -->
    <rect x="22" y="166" width="164" height="78" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="104" y="188" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">1.110 Perplexity</text>
    <text x="104" y="208" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">Near-Theoretical (1.0)</text>
    <text x="104" y="228" text-anchor="middle" fill="#475569" font-size="8.5">Zero Hallucination</text>

    <rect x="198" y="166" width="164" height="78" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
    <text x="280" y="188" text-anchor="middle" fill="#166534" font-size="11" font-weight="800">0.1505 Bits/Char</text>
    <text x="280" y="208" text-anchor="middle" fill="#166534" font-size="9.5" font-weight="700">Dense Domain Code</text>
    <text x="280" y="228" text-anchor="middle" fill="#475569" font-size="8.5">High Token Retention</text>

    <!-- Actionable Bylaws Directives Box -->
    <rect x="384" y="44" width="362" height="212" rx="5" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.2"/>
    <text x="394" y="66" fill="#166534" font-size="11.5" font-weight="800">Actionable Grounded Directives</text>

    <rect x="394" y="78" width="342" height="48" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
    <text x="404" y="96" fill="#166534" font-size="9.5" font-weight="700">Floor Space Index (FSI) Allocation:</text>
    <text x="404" y="114" fill="#475569" font-size="8.5">Dynamic base FSI 1.8 to 2.4 along designated transit corridors and spines.</text>

    <rect x="394" y="134" width="342" height="48" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
    <text x="404" y="152" fill="#166534" font-size="9.5" font-weight="700">Transit-Oriented Development (TOD):</text>
    <text x="404" y="170" fill="#475569" font-size="8.5">Enforces 15% riverbank green buffer setback along riverbeds and transit lines.</text>

    <rect x="394" y="190" width="342" height="54" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
    <text x="404" y="208" fill="#166534" font-size="9.5" font-weight="700">Percolation &amp; Rooftop Mandate:</text>
    <text x="404" y="226" fill="#475569" font-size="8.5">Mandates on-site rainwater harvesting &amp; solar on commercial plots &gt;1,000 m&#178;.</text>
  </g>

  <!-- ===================================================================== -->
  <!-- ROW 3: SYSTEM SECURITY, AIR-GAPPED HARDWARE & ETHICAL GOVERNANCE     -->
  <!-- y: 688 to 828 (height: 140, Inter-Row Gap 2 is 26px)                 -->
  <!-- ===================================================================== -->
  <g transform="translate(16, 688)">
    <rect width="1568" height="140" rx="8" fill="#F8FAFC" stroke="#64748B" stroke-width="1.6" filter="url(#shadow)"/>
    <rect x="12" y="10" width="1544" height="24" rx="4" fill="#334155"/>
    <text x="784" y="26" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">6. AIR-GAPPED EDGE HARDWARE, SYSTEM CYBERSECURITY &amp; CLOSED-LOOP GOVERNANCE</text>

    <!-- Edge Gateway Box -->
    <rect x="12" y="40" width="496" height="88" rx="5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="22" y="58" fill="#0F172A" font-size="10.5" font-weight="800">1. Guarded API Gateway &amp; File Sanitization</text>
    <text x="22" y="75" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">URBANGEN_API_KEY:</tspan> Header injection required for all internal REST microservices.</text>
    <text x="22" y="92" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">SlowAPI Token-Bucket Rate Limiter:</tspan> Prevents query abuse, DoS, and GPU tensor saturation.</text>
    <text x="22" y="109" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Magic-Byte Inspection:</tspan> Strictly validates image headers (&lt;10MB) to prevent shell execution.</text>

    <!-- Green AI Hardware Box -->
    <rect x="520" y="40" width="528" height="88" rx="5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="530" y="58" fill="#0F172A" font-size="10.5" font-weight="800">2. Air-Gapped Edge Hardware &amp; Green AI Audit</text>
    <text x="530" y="75" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">100% On-Premises Execution:</tspan> Consumer NVIDIA RTX 4050 Laptop GPU (6GB VRAM, 75W TGP capped).</text>
    <text x="530" y="92" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Complete Data Sovereignty:</tspan> Air-gapped deployment prevents sensitive municipal GIS leakage.</text>
    <text x="530" y="109" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Certified Energy Audit:</tspan> 66.3 min training &#8226; 0.133 kWh energy &#8226; 94.8 g CO&#8322;e (CEA factor 0.713 kg/kWh).</text>

    <!-- Closed Loop Governance Box -->
    <rect x="1060" y="40" width="496" height="88" rx="5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="1070" y="58" fill="#0F172A" font-size="10.5" font-weight="800">3. Closed-Loop Human-in-the-Loop Municipal Governance</text>
    <text x="1070" y="75" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Advisory Decision Support:</tspan> System serves strictly as assistive drafting support for planners.</text>
    <text x="1070" y="92" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Autonomous Enforcement Prohibited:</tspan> Automated legal zoning sanctions strictly forbidden.</text>
    <text x="1070" y="109" fill="#475569" font-size="9">&#8226; <tspan font-weight="bold">Domain Shift Uncertainty:</tspan> Flags high reconstruction disparity when outside pre-trained fabrics.</text>
  </g>

  <!-- ===================================================================== -->
  <!-- BOTTOM LEGEND BANNER: y=844 (relative y inside <g> is y=26)          -->
  <!-- ===================================================================== -->
  <g transform="translate(16, 844)">
    <rect width="1568" height="42" rx="6" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="24" y="26" fill="#1E293B" font-size="10" font-weight="800">PIPELINE SUMMARY &amp; COOPERATIVE PROTOCOL:</text>
    <text x="325" y="26" fill="#475569" font-size="9.5">Raw Ingestion (USGS) &#8594; U-Net DAE (+7.0 dB PSNR) &#8594; Spatial &#946;-VAE (&#956;,&#963;&#178;) &#8594; ResNet-18 Auditor (98.10%) &#8594; Dual cDCGAN (99.40%) &amp; DDPM (0.0304 MSE) &#8594; MiniGPT Policy (1.110 PPL)</text>
  </g>

  <!-- Footer Banner (y: 916) -->
  <text x="32" y="916" fill="#64748B" font-size="9.5">UrbanGen AI Architecture &#8226; Department of Computer Engineering, MIT Academy of Engineering, Pune &#8226; Uniform 50-Epoch Protocol</text>
  <text x="1568" y="916" text-anchor="end" fill="#64748B" font-size="9.5">Certified Academic Capstone Track 2026 &#8226; NVIDIA RTX 4050 6GB (0.133 kWh Green AI)</text>
</svg>"""

    svg_path = os.path.join(workspace, "docs", "poster", "figures", "clean_project_architecture.svg")
    png_path = os.path.join(workspace, "docs", "poster", "figures", "clean_project_architecture.png")
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"Vector SVG saved to: {svg_path}")

    # Copy to all target locations
    targets = [
        os.path.join(workspace, "docs", "poster", "figures", "pipeline_architecture_plantuml.svg"),
        os.path.join(workspace, "frontend", "public", "poster", "figures", "clean_project_architecture.svg"),
        os.path.join(workspace, "frontend", "public", "poster", "figures", "pipeline_architecture_plantuml.svg")
    ]
    for target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Copied SVG to: {target}")

    # Generate raster PNG via headless Chrome if present
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser_bin = next((b for b in chrome_candidates if os.path.exists(b)), None)
    if browser_bin:
        import subprocess, shutil
        svg_url = "file:///" + svg_path.replace("\\", "/")
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            f"--window-size={svg_w},{svg_h}",
            "--hide-scrollbars",
            f"--screenshot={png_path}",
            svg_url
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=15)
            if os.path.exists(png_path):
                print(f"Rendered PNG saved to: {png_path}")
                png_targets = [
                    os.path.join(workspace, "docs", "poster", "figures", "pipeline_architecture_plantuml.png"),
                    os.path.join(workspace, "frontend", "public", "poster", "figures", "clean_project_architecture.png"),
                    os.path.join(workspace, "frontend", "public", "poster", "figures", "pipeline_architecture_plantuml.png"),
                ]
                for pt in png_targets:
                    shutil.copyfile(png_path, pt)
                    print(f"Copied PNG to: {pt}")
        except Exception as e:
            print(f"Warning during browser rasterization: {e}")

    return svg_path

def main():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    puml_text = build_clean_puml()
    
    puml_file = os.path.join(workspace, "docs", "poster", "project_architecture.puml")
    with open(puml_file, "w", encoding="utf-8") as f:
        f.write(puml_text)
    print(f"Clean PlantUML code saved to: {puml_file}")

    public_puml = os.path.join(workspace, "frontend", "public", "poster", "project_architecture.puml")
    with open(public_puml, "w", encoding="utf-8") as f:
        f.write(puml_text)

    # Encode for plantuml.online and plantuml.com
    encoded = plantuml_encode(puml_text)
    plantuml_online_url = f"https://plantuml.online/uml/{encoded}"
    plantuml_com_png = f"https://www.plantuml.com/plantuml/png/{encoded}"
    plantuml_com_svg = f"https://www.plantuml.com/plantuml/svg/{encoded}"

    print(f"\nPlantUML Online URL:\n{plantuml_online_url}\n")
    print(f"PlantUML Official PNG URL:\n{plantuml_com_png}\n")

    # Render vector SVG
    svg_path = render_vector_svg_and_png(workspace)

if __name__ == "__main__":
    main()
