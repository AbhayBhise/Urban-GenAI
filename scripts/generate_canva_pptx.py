import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_professional_poster():
    prs = Presentation()
    # 24 inches wide x 36 inches high (Standard Portrait Academic Poster, A1 Aspect)
    prs.slide_width = Inches(24)
    prs.slide_height = Inches(36)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background canvas: Soft cool slate
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(24), Inches(36))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(241, 245, 249) # #F1F5F9
    bg.line.fill.background()

    # Color Palette
    NAVY = RGBColor(15, 23, 42)          # #0F172A
    NAVY_LIGHT = RGBColor(30, 41, 59)    # #1E293B
    BLUE_ACC = RGBColor(2, 132, 199)     # #0284C7
    BLUE_DARK = RGBColor(3, 105, 161)    # #0369A1
    SKY_BG = RGBColor(224, 242, 254)     # #E0F2FE
    GREEN_ACC = RGBColor(5, 150, 105)    # #059669
    GREEN_BG = RGBColor(236, 253, 245)   # #ECFDF5
    PURPLE_ACC = RGBColor(124, 58, 237)  # #7C3AED
    PURPLE_BG = RGBColor(245, 243, 255)  # #F5F3FF
    AMBER_ACC = RGBColor(217, 119, 6)    # #D97706
    AMBER_BG = RGBColor(254, 243, 199)   # #FEF3C7
    RED_ACC = RGBColor(225, 29, 72)      # #E11D48
    RED_BG = RGBColor(255, 241, 242)     # #FFF1F2
    DARK_TEXT = RGBColor(30, 41, 59)     # #1E293B
    MUTED_TEXT = RGBColor(71, 85, 105)   # #475569
    CARD_BG = RGBColor(255, 255, 255)    # #FFFFFF
    BORDER_COLOR = RGBColor(203, 213, 225)# #CBD5E1

    def add_card(left, top, width, height, title, badge_text="", border_col=BLUE_ACC, badge_bg=SKY_BG, badge_col=BLUE_ACC):
        # Card body
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        # Title bar
        t_box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.08), Inches(width - 0.3), Inches(0.4))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.name = 'Arial'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = border_col

        if badge_text:
            bw = min(2.0, len(badge_text) * 0.10 + 0.35)
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + width - bw - 0.15), Inches(top + 0.08), Inches(bw), Inches(0.28))
            badge.fill.solid()
            badge.fill.fore_color.rgb = badge_bg
            badge.line.fill.background()
            btf = badge.text_frame
            btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
            bp = btf.paragraphs[0]
            bp.alignment = PP_ALIGN.CENTER
            bp.text = badge_text
            bp.font.name = 'Arial'
            bp.font.size = Pt(7.5)
            bp.font.bold = True
            bp.font.color.rgb = badge_col

        return card

    # =========================================================================
    # 1. HEADER BANNER (Top: 0.35", Height: 2.1", Width: 23.3")
    # =========================================================================
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(0.35), Inches(23.3), Inches(2.1))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = NAVY
    hdr.line.color.rgb = BLUE_ACC
    hdr.line.width = Pt(2.0)

    # Header content
    hBox = slide.shapes.add_textbox(Inches(0.55), Inches(0.45), Inches(22.9), Inches(1.9))
    htf = hBox.text_frame
    htf.word_wrap = True
    htf.margin_top = htf.margin_bottom = htf.margin_left = htf.margin_right = 0

    p = htf.paragraphs[0]
    p.text = "MIT ACADEMY OF ENGINEERING, PUNE  |  DEPARTMENT OF COMPUTER ENGINEERING"
    p.font.name = 'Arial'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248) # Sky blue
    p.space_after = Pt(3)

    p = htf.add_paragraph()
    p.text = "UrbanGen AI: Multi-Model Deep Generative Framework for Satellite Imagery Processing & Autonomous Urban Planning"
    p.font.name = 'Arial'
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(4)

    p = htf.add_paragraph()
    p.text = (
        "Project Guides: Prof. Savita Mane & Prof. Pramod Ganjewar  |  "
        "Capstone Team: Abhay Bhise (202201040024), Disha Satpute (202201040027), Vaishnavi Phad (202201040033), Vedant Ingle (202201040065)"
    )
    p.font.name = 'Arial'
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(3)

    p = htf.add_paragraph()
    p.text = "B.Tech Capstone 2026 (60 Marks)  |  IEEE Publication Submission Track  |  Air-Gapped Edge Deployment: NVIDIA RTX 4050 6GB (0.133 kWh)"
    p.font.name = 'Arial'
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = RGBColor(52, 211, 153) # Mint green

    # =========================================================================
    # ROW 1 (y = 2.60", Height = 4.7"): Scope & Dataset + Model 1 + Model 2
    # =========================================================================
    r1_y = 2.60
    r1_h = 4.70

    # --- Col 1: Scope, Objectives & Dataset ---
    add_card(0.35, r1_y, 5.7, r1_h, "Project Statement & Benchmark Dataset", "PROBLEM & DATA", BLUE_ACC, SKY_BG, BLUE_ACC)
    tbox = slide.shapes.add_textbox(Inches(0.50), Inches(r1_y + 0.45), Inches(5.4), Inches(4.15))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p = tf.paragraphs[0]
    p.text = "• Problem: Optical remote sensing rasters suffer from cloud attenuation and atmospheric noise (sigma=0.15). Monolithic architectures cannot jointly perform multi-scale spatial denoising, topological anomaly scoring, class augmentation, and grounded municipal zoning drafting."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "• Objectives: Deploy a 6-model cooperative pipeline: (1) U-Net DAE restoration, (2) Spatial beta-VAE latent manifold, (3) ResNet-18 territorial zoning auditor, (4) Residual cDCGAN fast synthesis, (5) Class-conditioned DDPM photorealism with 5 losses, and (6) MiniGPT policy drafting."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "• UC Merced Benchmark Protocol: 2,100 high-resolution aerial orthoimagery tiles (256x256 px, 0.3m GSD) across 21 land-use categories. Uniform 50-epoch / 32-batch experimental benchmark guarantees zero gradient bias."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT

    # --- Col 2: Model 1 Denoising U-Net AE with EMBEDDED CRISP RESTORATION IMAGE ---
    add_card(6.20, r1_y, 8.6, r1_h, "Model 1: Denoising Autoencoder (U-Net)", "PSNR: 29.65 dB", GREEN_ACC, GREEN_BG, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(6.35), Inches(r1_y + 0.42), Inches(8.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: ResNet encoder-decoder with multi-scale skip connections bridging Stem, L1, L2, L3 into transposed convs (8->16->32->64->128). Minimizes MSE reconstruction loss via Adam."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Formula: x_hat = D(E(x_corrupted), {F_skip}) | Metric: 29.65 dB PSNR (+7.0 dB boost over standard bottleneck AE)"
    p.font.size = Pt(7.6)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    # Embed Real Empirical Image: fig_ae_crisp_restoration.png
    ae_img = "docs/poster/figures/fig_ae_crisp_restoration.png"
    if os.path.exists(ae_img):
        slide.shapes.add_picture(ae_img, Inches(6.35), Inches(r1_y + 1.65), Inches(8.3), Inches(2.95))

    # --- Col 3: Model 2 Spatial beta-VAE with EMBEDDED LATENT MANIFOLD IMAGE ---
    add_card(15.00, r1_y, 8.65, r1_h, "Model 2: Spatial beta-VAE (Manifold Traversal)", "KL: 60.72 nats", PURPLE_ACC, PURPLE_BG, PURPLE_ACC)
    tbox = slide.shapes.add_textbox(Inches(15.15), Inches(r1_y + 0.42), Inches(8.35), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: Modified ResNet-18 encoder preserving 2D spatial topology in latent space z in R^{64 x 8 x 8} paired with 4-stage transposed conv decoder. Unsupervised structural anomaly localization."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Formula: L_VAE = (0.7*L_L1 + 0.3*L_MSE) + 10^-4 * D_KL(q(z|x) || p(z)) | PSNR: 27.49 dB | KL: 60.72 nats"
    p.font.size = Pt(7.6)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACC

    # Embed Real Empirical Image: fig_vae_multi_interpolation.png
    vae_img = "docs/poster/figures/fig_vae_multi_interpolation.png"
    if os.path.exists(vae_img):
        slide.shapes.add_picture(vae_img, Inches(15.15), Inches(r1_y + 1.65), Inches(8.35), Inches(2.95))

    # =========================================================================
    # ROW 2 (y = 7.45", Height = 4.7"): Security + Model 3 + Model 4
    # =========================================================================
    r2_y = 7.45
    r2_h = 4.70

    # --- Col 1: System Security & Website Protection ---
    add_card(0.35, r2_y, 5.7, r2_h, "System Security & Website Protection", "HARDENED GATEWAY", RED_ACC, RED_BG, RED_ACC)
    tbox = slide.shapes.add_textbox(Inches(0.50), Inches(r2_y + 0.45), Inches(5.4), Inches(4.15))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    sec_bullets = [
        ("Guarded API Gateway", "Every FastAPI endpoint enforces URBANGEN_API_KEY header verification (dependencies=GUARDED), rejecting unauthorized bot probes."),
        ("SlowAPI Token Limiter", "Rate-limiting decorator (@limiter.limit(RATE_LIMIT)) prohibits DDoS flood attacks and GPU memory exhaustion."),
        ("Magic-Byte Sanitization", "Strict MIME magic-byte validation and 10MB ceiling reject malicious binaries; forces input clamping to 128x128 px."),
        ("Air-Gapped Sovereignty", "100% on-premises execution on NVIDIA RTX 4050 ensures sensitive municipal cadastral GIS telemetry never leaves local boundaries."),
        ("Human-in-the-Loop Limits", "Outputs serve strictly as advisory drafting support; autonomous legal municipal zoning enforcement is strictly prohibited.")
    ]
    for title, desc in sec_bullets:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"• {title}: "
        p.font.size = Pt(7.6)
        p.font.bold = True
        p.font.color.rgb = RED_ACC
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(7.4)
        run.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # --- Col 2: Model 3 ResNet-18 Classifier with EMBEDDED METRICS GRAPH ---
    add_card(6.20, r2_y, 8.6, r2_h, "Model 3: Land-Use Classifier (ResNet-18)", "ACCURACY: 98.10%", BLUE_ACC, SKY_BG, BLUE_ACC)
    tbox = slide.shapes.add_textbox(Inches(6.35), Inches(r2_y + 0.42), Inches(8.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: ImageNet pre-trained ResNet-18 backbone with 21-class linear projection head. Serves as automated territorial zoning auditor and generative semantic proxy."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Formula: L_CE = - sum(y_i * log(y_hat_i)) | Validation Accuracy: 98.10% | Macro F1: 0.9784 | Final Loss: 0.0615"
    p.font.size = Pt(7.6)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    # Embed Real Empirical Image: fig_classifier_metrics.png
    cls_img = "docs/poster/figures/fig_classifier_metrics.png"
    if os.path.exists(cls_img):
        slide.shapes.add_picture(cls_img, Inches(6.35), Inches(r2_y + 1.65), Inches(8.3), Inches(2.95))

    # --- Col 3: Model 4 cDCGAN with EMBEDDED 21-CLASS SYNTHESIS GRID ---
    add_card(15.00, r2_y, 8.65, r2_h, "Model 4: Class-Conditional DCGAN (Residual)", "PROXY REC: 99.40%", AMBER_ACC, AMBER_BG, AMBER_ACC)
    tbox = slide.shapes.add_textbox(Inches(15.15), Inches(r2_y + 0.42), Inches(8.35), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: 4x ResUpBlock Generator + Projection Discriminator with Spectral Normalization, AC-GAN auxiliary class head, and EMA. Completely prevents mode collapse."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Formula: L_G = L_adv + 0.8*L_AC + 1.2*L_sem | Minimax: D=1.67, G=1.19 | Proxy Recognition: 99.40% | Latency: <35ms"
    p.font.size = Pt(7.6)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACC

    # Embed Real Empirical Image: fig_gan_diverse_generation.png
    gan_img = "docs/poster/figures/fig_gan_diverse_generation.png"
    if os.path.exists(gan_img):
        slide.shapes.add_picture(gan_img, Inches(15.15), Inches(r2_y + 1.65), Inches(8.35), Inches(2.95))

    # =========================================================================
    # ROW 3 (y = 12.30", Height = 4.7"): Overall Ranking + Model 5 (5 Losses) + Model 6
    # =========================================================================
    r3_y = 12.30
    r3_h = 4.70

    # --- Col 1: Overall Ranking Champions ---
    add_card(0.35, r3_y, 5.7, r3_h, "Overall Ranking: Best Model per Task", "CHAMPIONS", GREEN_ACC, GREEN_BG, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(0.50), Inches(r3_y + 0.45), Inches(5.4), Inches(4.15))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    ranks = [
        ("1. Best Restorer: U-Net Skip DAE", "29.65 dB PSNR, MSE 0.00449. Skips give +7.0 dB boost over bottleneck."),
        ("2. Best Auditor: ResNet-18 Classifier", "98.10% Val Accuracy, 0.9784 Macro F1. Automated zoning audit standard."),
        ("3. Best Synthesis Proxy: Residual cDCGAN", "99.40% Class Recognition, D=1.67, G=1.19. Sub-35ms real-time augmentation."),
        ("4. Best Manifold: Spatial beta-VAE", "27.49 dB PSNR, 60.72 nats KL. Smooth topological latent interpolation."),
        ("5. Best Photorealism: DDPM (Diffusion)", "0.0304 Noise MSE. 20-step DDIM (1.8s) yields sharpest street grids."),
        ("6. Best Policy Engine: MiniGPT", "1.110 PPL, 0.1505 Bits/Char. Formulates grounded PMC municipal bylaws.")
    ]
    for title, desc in ranks:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(7.8)
        p.font.bold = True
        p.font.color.rgb = GREEN_ACC
        p = tf.add_paragraph()
        p.text = "   " + desc
        p.font.size = Pt(7.2)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # --- Col 2: Model 5 DDPM with 5 LOSS FORMULATIONS & METRICS GRAPH ---
    add_card(6.20, r3_y, 8.6, r3_h, "Model 5: Class-Conditional DDPM (5 Losses)", "NOISE MSE: 0.0304", RED_ACC, RED_BG, RED_ACC)
    tbox = slide.shapes.add_textbox(Inches(6.35), Inches(r3_y + 0.42), Inches(8.3), Inches(1.6))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: Time- & class-conditioned U-Net (T=1000 schedule) accelerated by 20-step deterministic DDIM sampler (1.8s synthesis). 5 Explicit Mathematical Loss Formulations:"
    p.font.size = Pt(7.5)
    p.font.color.rgb = DARK_TEXT
    
    diff_losses = (
        "1. L_simple = E_{t,x0,eps}[ ||eps - eps_theta(x_t, t, c)||^2 ] -> Converged to 0.0304\n"
        "2. L_vlb = sum_t D_KL( q(x_{t-1}|x_t, x_0) || p_theta(x_{t-1}|x_t) )  [Variational Lower Bound]\n"
        "3. L_guide = gamma * grad_{x_t} log p_phi(y | x_t)  [Classifier gradient class steering]\n"
        "4. L_spatial = sum_l w_l * ||Psi_l(x_0) - Psi_l(x_0_hat)||_1  [Multi-scale structural feature preservation]\n"
        "5. L_reg = sum_{i,j} sqrt((Delta_x x)^2 + (Delta_y x)^2)  [Total variation noise regularization]"
    )
    p = tf.add_paragraph()
    p.text = diff_losses
    p.font.name = 'Courier New'
    p.font.size = Pt(6.8)
    p.font.bold = True
    p.font.color.rgb = RED_ACC

    # Embed Real Empirical Image: fig_diffusion_metrics.png
    diff_img = "docs/poster/figures/fig_diffusion_metrics.png"
    if os.path.exists(diff_img):
        slide.shapes.add_picture(diff_img, Inches(6.35), Inches(r3_y + 2.15), Inches(8.3), Inches(2.45))

    # --- Col 3: Model 6 MiniGPT Policy Engine & Urban Mandates ---
    add_card(15.00, r3_y, 8.65, r3_h, "Model 6: Urban Plan Generator (MiniGPT)", "PPL: 1.110", GREEN_ACC, GREEN_BG, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(15.15), Inches(r3_y + 0.42), Inches(8.35), Inches(4.15))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Architecture: 4-layer Pre-LayerNorm Causal Transformer (d_model=256, 4 attention heads, context T=192) trained from scratch on PMC municipal planning regulations. Converts classifier spatial telemetry into actionable urban bylaws."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "Mathematical Formulation:\n  P(w_t | w_{<t}) = Softmax( (Q * K^T / sqrt(d_k) + M) * V )\n  L_LM = - (1/T) * sum_{t=1}^T log P(w_t | w_{<t})  [Perplexity: 1.110 | BPC: 0.1505]"
    p.font.name = 'Courier New'
    p.font.size = Pt(7.4)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Actionable Grounded Municipal Bylaw Outputs:"
    p.font.size = Pt(8.0)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

    bylaws = [
        ("Floor Space Index (FSI)", "Calculates base FSI 1.8 to 2.4 along designated transit corridors with density caps."),
        ("Transit-Oriented Development (TOD)", "Enforces 15% green buffer setback along riverbanks and transit spines."),
        ("Percolation Mandate", "Mandates permeable paving and solar canopy installation on commercial plots >1000m².")
    ]
    for b_title, b_desc in bylaws:
        p = tf.add_paragraph()
        p.text = f"• {b_title}: {b_desc}"
        p.font.size = Pt(7.4)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # =========================================================================
    # ROW 4 (y = 17.15", Height = 5.2"): FULL-WIDTH PLANTUML ARCHITECTURE DIAGRAM
    # =========================================================================
    r4_y = 17.15
    r4_h = 5.20
    add_card(0.35, r4_y, 23.3, r4_h, "Integrated End-to-End System Pipeline & Security Architecture (PlantUML High-Res Vector Flow)", "300 DPI VECTOR FLOW", BLUE_ACC, SKY_BG, BLUE_ACC)
    
    arch_img = "docs/poster/figures/pipeline_architecture_plantuml.png"
    if os.path.exists(arch_img):
        slide.shapes.add_picture(arch_img, Inches(0.50), Inches(r4_y + 0.45), Inches(23.0), Inches(4.65))

    # =========================================================================
    # ROW 5 (y = 22.50", Height = 10.3"): RESULTS, EVALUATION PARAMETRICS & GRAPHS
    # =========================================================================
    r5_y = 22.50
    r5_h = 10.30

    # Main Card for Evaluation & Results
    add_card(0.35, r5_y, 23.3, r5_h, "Experimental Results, Evaluation Parametrics & IEEE Research Benchmarks (Uniform 50-Epoch Protocol)", "EMPIRICAL BENCHMARKS", BLUE_ACC, SKY_BG, BLUE_ACC)

    # --- Sub-Column 1: Quantitative Tables (Left: 0.50", Width: 7.4") ---
    # Table I
    t1_box = slide.shapes.add_textbox(Inches(0.50), Inches(r5_y + 0.45), Inches(7.4), Inches(0.3))
    t1_tf = t1_box.text_frame
    t1_p = t1_tf.paragraphs[0]
    t1_p.text = "TABLE I: 50-Epoch Multi-Model Performance Verification"
    t1_p.font.name = 'Arial'
    t1_p.font.size = Pt(8.5)
    t1_p.font.bold = True
    t1_p.font.color.rgb = NAVY

    t1_shape = slide.shapes.add_table(7, 4, Inches(0.50), Inches(r5_y + 0.78), Inches(7.4), Inches(2.9))
    table1 = t1_shape.table
    table1.columns[0].width = Inches(2.3)
    table1.columns[1].width = Inches(1.7)
    table1.columns[2].width = Inches(1.7)
    table1.columns[3].width = Inches(1.7)

    t1_data = [
        ["Model Pipeline", "Primary Metric", "Secondary Metric", "Final Loss"],
        ["Denoising U-Net AE", "29.65 dB PSNR", "SSIM: 0.8649", "MSE = 0.00617"],
        ["Spatial beta-VAE", "27.49 dB PSNR", "KL: 60.72 nats", "L_total = 0.0483"],
        ["ResNet-18 Classifier", "98.10% Val Acc", "Macro F1: 0.9784", "L_CE = 0.0615"],
        ["Residual cDCGAN", "99.40% Proxy Rec", "D=1.67, G=1.19", "Minimax Eq."],
        ["Conditional DDPM", "0.0304 Noise MSE", "DDIM: 20 Steps", "Best: 0.02916"],
        ["MiniGPT Transformer", "1.110 Perplexity", "0.1505 Bits/Char", "L_CE = 0.1043"]
    ]
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = table1.cell(r_idx, c_idx)
            cell.text = val
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.font.name = 'Arial'
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(7.5)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(7.2)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # Table II
    t2_box = slide.shapes.add_textbox(Inches(0.50), Inches(r5_y + 3.85), Inches(7.4), Inches(0.3))
    t2_tf = t2_box.text_frame
    t2_p = t2_tf.paragraphs[0]
    t2_p.text = "TABLE II: Generative Synthesis & Edge Latency Benchmark"
    t2_p.font.name = 'Arial'
    t2_p.font.size = Pt(8.5)
    t2_p.font.bold = True
    t2_p.font.color.rgb = NAVY

    t2_shape = slide.shapes.add_table(6, 4, Inches(0.50), Inches(r5_y + 4.18), Inches(7.4), Inches(2.6))
    table2 = t2_shape.table
    table2.columns[0].width = Inches(2.3)
    table2.columns[1].width = Inches(1.7)
    table2.columns[2].width = Inches(1.7)
    table2.columns[3].width = Inches(1.7)

    t2_data = [
        ["Generative Model", "Visual Sharpness", "Latency / Tile", "Advantage / Trade-off"],
        ["Spatial beta-VAE", "Smooth Structural", "12 ms (RTX 4050)", "Fast manifold traversal"],
        ["Residual cDCGAN", "High Realism", "32 ms (RTX 4050)", "Instant augmentation"],
        ["DDPM (1000 Steps)", "Pristine Crispness", "28.4 s (prohibitive)", "Baseline baseline"],
        ["DDPM (20-Step DDIM)", "Photorealistic", "1.82 s (RTX 4050)", "15.6x speedup, sharp"],
        ["MiniGPT Policy", "Syntactically Sound", "45 ms (192 tokens)", "Contextual mandates"]
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = table2.cell(r_idx, c_idx)
            cell.text = val
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.font.name = 'Arial'
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(7.5)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(7.2)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # Green AI Compute Box below tables
    g_box = slide.shapes.add_textbox(Inches(0.50), Inches(r5_y + 6.95), Inches(7.4), Inches(3.1))
    gtf = g_box.text_frame
    gtf.word_wrap = True
    gtf.margin_top = gtf.margin_bottom = gtf.margin_left = gtf.margin_right = 0
    p = gtf.paragraphs[0]
    p.text = "⚡ Green AI Compute & Carbon Audit:"
    p.font.size = Pt(8.2)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    p.space_after = Pt(2)

    ga_bullets = [
        "Hardware: Single NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM, 75W TGP).",
        "Total Training Time: 66.3 Cumulative Minutes across all 6 deep models (50 epochs each).",
        "Total Energy Consumption: 0.133 kWh (Measured via continuous NVML sampling).",
        "Carbon Footprint: 94.8 g CO2e (CEA India national grid factor 0.713 kg/kWh).",
        "Democratization Impact: Proves advanced multi-model GenAI can run directly inside municipal town-planning offices without costly cloud computing clusters."
    ]
    for b in ga_bullets:
        bp = gtf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(7.3)
        bp.font.color.rgb = DARK_TEXT
        bp.space_after = Pt(1.5)

    # --- Sub-Column 2: Graphs Set 1 (Middle: 8.15", Width: 7.5") ---
    # Graph 1: fig_psnr_comparison.png (PSNR across classes)
    g1_lbl = slide.shapes.add_textbox(Inches(8.15), Inches(r5_y + 0.45), Inches(7.5), Inches(0.25))
    g1_lbl.text_frame.paragraphs[0].text = "Figure 2: Class-Wise PSNR (U-Net Skip vs Baseline AE: +7.0 dB Gain)"
    g1_lbl.text_frame.paragraphs[0].font.size = Pt(7.8)
    g1_lbl.text_frame.paragraphs[0].font.bold = True
    g1_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY

    psnr_img = "docs/poster/figures/fig_psnr_comparison.png"
    if os.path.exists(psnr_img):
        slide.shapes.add_picture(psnr_img, Inches(8.15), Inches(r5_y + 0.75), Inches(7.5), Inches(4.5))

    # Graph 2: fig_multimodel_loss_bars.png (Multi-Model 50e Loss Bars)
    g2_lbl = slide.shapes.add_textbox(Inches(8.15), Inches(r5_y + 5.35), Inches(7.5), Inches(0.25))
    g2_lbl.text_frame.paragraphs[0].text = "Figure 9: Initial vs Final 50-Epoch Loss Across All 6 Architectures"
    g2_lbl.text_frame.paragraphs[0].font.size = Pt(7.8)
    g2_lbl.text_frame.paragraphs[0].font.bold = True
    g2_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY

    bars_img = "docs/poster/figures/fig_multimodel_loss_bars.png"
    if os.path.exists(bars_img):
        slide.shapes.add_picture(bars_img, Inches(8.15), Inches(r5_y + 5.65), Inches(7.5), Inches(4.4))

    # --- Sub-Column 3: Graphs Set 2 (Right: 15.85", Width: 7.5") ---
    # Graph 3: fig_gan_dynamics.png (GAN Minimax Loss Curves)
    g3_lbl = slide.shapes.add_textbox(Inches(15.85), Inches(r5_y + 0.45), Inches(7.5), Inches(0.25))
    g3_lbl.text_frame.paragraphs[0].text = "Figure 7: cDCGAN Minimax Training Dynamics (D=1.67, G=1.19 Equilibrium)"
    g3_lbl.text_frame.paragraphs[0].font.size = Pt(7.8)
    g3_lbl.text_frame.paragraphs[0].font.bold = True
    g3_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY

    dyn_img = "docs/poster/figures/fig_gan_dynamics.png"
    if os.path.exists(dyn_img):
        slide.shapes.add_picture(dyn_img, Inches(15.85), Inches(r5_y + 0.75), Inches(7.5), Inches(4.5))

    # Graph 4: fig_energy_carbon_breakdown.png (Energy & Carbon breakdown)
    g4_lbl = slide.shapes.add_textbox(Inches(15.85), Inches(r5_y + 5.35), Inches(7.5), Inches(0.25))
    g4_lbl.text_frame.paragraphs[0].text = "Figure 10: Energy Consumption (kWh) & Carbon Footprint Breakdown"
    g4_lbl.text_frame.paragraphs[0].font.size = Pt(7.8)
    g4_lbl.text_frame.paragraphs[0].font.bold = True
    g4_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY

    ec_img = "docs/poster/figures/fig_energy_carbon_breakdown.png"
    if os.path.exists(ec_img):
        slide.shapes.add_picture(ec_img, Inches(15.85), Inches(r5_y + 5.65), Inches(7.5), Inches(4.4))


    # =========================================================================
    # 6. FOOTER BANNER (Top: 33.00", Height: 2.65", Width: 23.3")
    # =========================================================================
    ftr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(33.00), Inches(23.3), Inches(2.65))
    ftr.fill.solid()
    ftr.fill.fore_color.rgb = NAVY
    ftr.line.color.rgb = BLUE_ACC
    ftr.line.width = Pt(1.5)

    fBox = slide.shapes.add_textbox(Inches(0.55), Inches(33.10), Inches(22.9), Inches(2.45))
    ftf = fBox.text_frame
    ftf.word_wrap = True
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0

    p = ftf.paragraphs[0]
    p.text = "MIT ACADEMY OF ENGINEERING, PUNE — B.TECH CAPSTONE PROJECT DEFENSE (2025–2026)"
    p.font.name = 'Arial'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)
    p.space_after = Pt(2)

    p = ftf.add_paragraph()
    p.text = (
        "Key Scientific Takeaways: UrbanGen AI validates that a multi-model cooperative deep generative pipeline with specialized inductive biases "
        "outperforms monolithic foundation models for remote sensing satellite applications. Uniform 50-epoch benchmarking across UCMerced demonstrates "
        "reproducible gains: +7.0 dB PSNR restoration gain via skip U-Net, 98.10% territorial zoning classification, 99.40% GAN proxy fidelity, "
        "0.0304 diffusion noise MSE, and grounded 1.110 PPL municipal policy generation. Complete air-gapped execution on a consumer RTX 4050 GPU (0.133 kWh) "
        "guarantees zero municipal GIS privacy leakage."
    )
    p.font.name = 'Arial'
    p.font.size = Pt(8.2)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_after = Pt(3)

    p = ftf.add_paragraph()
    p.text = (
        "Project Guides: Prof. Savita Mane & Prof. Pramod Ganjewar  |  Department of Computer Engineering\n"
        "Project Team: Abhay Bhise (202201040024, bhiseabhay890@gmail.com)  •  Disha Satpute (202201040027, dishasatpute44@gmail.com)  •  "
        "Vaishnavi Phad (202201040033, phadvaishnavi1905@gmail.com)  •  Vedant Ingle (202201040065, vedantingle85@gmail.com)\n"
        "Affiliation: Savitribai Phule Pune University  |  Verified with Submitted IEEE Publication & GitHub Reproducibility Package"
    )
    p.font.name = 'Arial'
    p.font.size = Pt(8.0)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Save with fallback in case file is currently open in Microsoft PowerPoint
    out_docs = "docs/poster/UrbanGen_AI_Poster.pptx"
    out_docs_v2 = "docs/poster/UrbanGen_AI_Poster_v2.pptx"
    out_public = "frontend/public/poster/UrbanGen_AI_Poster.pptx"
    out_public_v2 = "frontend/public/poster/UrbanGen_AI_Poster_v2.pptx"

    saved_files = []
    for target in [out_docs, out_docs_v2]:
        try:
            prs.save(target)
            saved_files.append(target)
            print(f"Saved: {target}")
        except PermissionError:
            print(f"Warning: {target} is locked (currently open in PowerPoint). Skipped.")

    for target in [out_public, out_public_v2]:
        try:
            prs.save(target)
            saved_files.append(target)
            print(f"Saved: {target}")
        except PermissionError:
            print(f"Warning: {target} is locked. Skipped.")

    print(f"Successfully generated Canva-Ready PPTX posters: {saved_files}")

if __name__ == '__main__':
    build_professional_poster()
