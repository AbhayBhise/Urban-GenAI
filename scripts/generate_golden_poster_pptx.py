import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def build_golden_ratio_poster():
    prs = Presentation()
    # Standard 24 x 36 inch Portrait Poster (A1 Proportions, 1 : 1.5 ~ Golden Ratio)
    prs.slide_width = Inches(24)
    prs.slide_height = Inches(36)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background Canvas: Clean architectural slate
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(24), Inches(36))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(248, 250, 252) # #F8FAFC
    bg.line.fill.background()

    # Color Palette: Professional Academic Navy & Cobalt
    NAVY = RGBColor(11, 25, 44)           # #0B192C (MIT AOE Navy)
    NAVY_LIGHT = RGBColor(15, 23, 42)     # #0F172A
    COBALT = RGBColor(2, 132, 199)        # #0284C7 (Primary Accent)
    COBALT_DARK = RGBColor(3, 105, 161)   # #0369A1
    SKY_TINT = RGBColor(224, 242, 254)    # #E0F2FE
    GREEN_ACC = RGBColor(5, 150, 105)     # #059669
    GREEN_TINT = RGBColor(236, 253, 245)  # #ECFDF5
    PURPLE_ACC = RGBColor(124, 58, 237)   # #7C3AED
    PURPLE_TINT = RGBColor(245, 243, 255) # #F5F3FF
    AMBER_ACC = RGBColor(217, 119, 6)     # #D97706
    AMBER_TINT = RGBColor(254, 243, 199)  # #FEF3C7
    ROSE_ACC = RGBColor(225, 29, 72)      # #E11D48
    ROSE_TINT = RGBColor(255, 241, 242)   # #FFF1F2
    DARK_TEXT = RGBColor(30, 41, 59)      # #1E293B
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B
    CARD_BG = RGBColor(255, 255, 255)     # Pure White
    BORDER_SUBTLE = RGBColor(226, 232, 240)# Light slate border

    # Card Helper with refined aesthetic
    def add_card(left, top, width, height, title, badge_text="", border_col=COBALT, badge_bg=SKY_TINT, badge_col=COBALT):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        # Header title
        t_box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.08), Inches(width - 0.3), Inches(0.38))
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
            bw = min(2.4, len(badge_text) * 0.10 + 0.35)
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + width - bw - 0.15), Inches(top + 0.08), Inches(bw), Inches(0.26))
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

    # Image Helper with strict aspect ratio guarantee
    def add_proportional_image(img_path, left, top, max_w, max_h):
        if not os.path.exists(img_path):
            return None
        im = Image.open(img_path)
        img_w, img_h = im.size
        aspect = img_w / img_h

        # Compute dimensions fitting inside bounding box without distortion
        if max_w / max_h > aspect:
            # Height constrained
            h = max_h
            w = h * aspect
        else:
            # Width constrained
            w = max_w
            h = w / aspect

        # Center horizontally within target area
        centered_left = left + (max_w - w) / 2.0
        centered_top = top + (max_h - h) / 2.0
        return slide.shapes.add_picture(img_path, Inches(centered_left), Inches(centered_top), width=Inches(w), height=Inches(h))

    # =========================================================================
    # 1. HEADER BANNER (Top: 0.4", Height: 2.0", Width: 23.2")
    # =========================================================================
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.4), Inches(23.2), Inches(2.0))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = NAVY
    hdr.line.color.rgb = COBALT
    hdr.line.width = Pt(2.0)

    hBox = slide.shapes.add_textbox(Inches(0.6), Inches(0.48), Inches(22.8), Inches(1.85))
    htf = hBox.text_frame
    htf.word_wrap = True
    htf.margin_top = htf.margin_bottom = htf.margin_left = htf.margin_right = 0

    p = htf.paragraphs[0]
    p.text = "MIT ACADEMY OF ENGINEERING, PUNE  |  DEPARTMENT OF COMPUTER ENGINEERING"
    p.font.name = 'Arial'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248) # Sky blue
    p.space_after = Pt(2)

    p = htf.add_paragraph()
    p.text = "UrbanGen AI: Multi-Model Deep Generative Framework for Satellite Imagery & Urban Planning"
    p.font.name = 'Arial Black'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(3)

    p = htf.add_paragraph()
    p.text = (
        "Project Guides: Prof. Savita Mane & Prof. Pramod Ganjewar  |  "
        "Capstone Team: Abhay Bhise (202201040024), Disha Satpute (202201040027), Vaishnavi Phad (202201040033), Vedant Ingle (202201040065)"
    )
    p.font.name = 'Arial'
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(2)

    p = htf.add_paragraph()
    p.text = "B.Tech Capstone Project (60 Marks)  |  IEEE Publication Submission Track  |  Edge Air-Gapped: NVIDIA RTX 4050 6GB (0.133 kWh)"
    p.font.name = 'Arial'
    p.font.size = Pt(8.8)
    p.font.bold = True
    p.font.color.rgb = RGBColor(52, 211, 153) # Mint green

    # =========================================================================
    # GOLDEN RATIO COLUMN PARTITION (Total Width: 23.2", Gap: 0.4")
    # Left Minor Column (38.2%): Width = 8.6"
    # Right Major Column (61.8%): Width = 14.2"
    # Ratio = 14.2 / 8.6 = 1.65 ~ 1.618 (The Golden Ratio)
    # =========================================================================
    col1_left = 0.40
    col1_w = 8.60
    col2_left = 9.40
    col2_w = 14.20

    # =========================================================================
    # LEFT COLUMN: CONTEXT, GOVERNANCE, AUDIT, RANKINGS (y=2.55 to y=33.3)
    # =========================================================================
    # --- Card L1: Project Statement & Scope (Top: 2.55, Height: 4.8) ---
    add_card(col1_left, 2.55, col1_w, 4.8, "Project Statement & Scope", "PROBLEM & OBJECTIVES", COBALT, SKY_TINT, COBALT)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(2.98), Inches(col1_w - 0.3), Inches(4.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p = tf.paragraphs[0]
    p.text = "• Problem: Optical remote sensing rasters suffer from cloud attenuation and atmospheric noise (sigma=0.15). Monolithic architectures cannot jointly perform multi-scale spatial restoration, topological anomaly scoring, class augmentation, and grounded municipal zoning drafting."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "• Objectives: Deploy 6 specialized modular networks under a unified pipeline: (1) U-Net DAE signal restoration, (2) Spatial beta-VAE latent manifold traversal, (3) ResNet-18 territorial zoning auditor, (4) Residual cDCGAN fast synthesis, (5) Class-conditioned DDPM photorealism with 5 losses, and (6) MiniGPT causal policy drafting."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "• Guaranteed 50-Epoch Rigor: Uniform 50-epoch / 32-batch experimental benchmark guarantees reproducible, zero-bias comparative validation across all generative and analytical pipelines."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_TEXT

    # --- Card L2: Dataset Description & Protocol (Top: 7.50, Height: 4.4) ---
    add_card(col1_left, 7.50, col1_w, 4.4, "Dataset Description & Protocol", "UCMERCED BENCHMARK", COBALT, SKY_TINT, COBALT)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(7.93), Inches(col1_w - 0.3), Inches(3.9))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p = tf.paragraphs[0]
    p.text = "• Benchmark Corpus: USGS National Map / UC Merced Land-Use Dataset.\n• Volume & Resolution: 2,100 Orthoimagery Tiles (256x256 px, 0.3m GSD, RGB).\n• 21 Semantic Classes in 5 Urban Sectors:\n  - Built-up (8): dense/medium/sparse residential, buildings, storage tanks, mobile home park, freeway, intersection.\n  - Transport (4): runway, airplane, harbor, parking lot.\n  - Nature (4): forest, chaparral, beach, golf course.\n  - Water (3): river, harbor, beach.\n  - Agriculture (2): agricultural fields, overpass."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(2)

    p = tf.add_paragraph()
    p.text = "• Data Split: Stratified 90% Training (1,890 tiles) / 10% Validation (210 tiles).\n• Corruption Model: Additive Gaussian perturbation (sigma=0.15) simulating severe atmospheric scattering for U-Net autoencoder training."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT

    # --- Card L3: Website Security & System Protection (Top: 12.05, Height: 5.6) ---
    add_card(col1_left, 12.05, col1_w, 5.6, "System Security & Website Protection", "CYBERSECURITY & HARDENING", ROSE_ACC, ROSE_TINT, ROSE_ACC)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(12.48), Inches(col1_w - 0.3), Inches(5.1))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    sec_items = [
        ("1. Guarded API Gateway", "FastAPI endpoints require verified URBANGEN_API_KEY header injection (dependencies=GUARDED), rejecting unauthorized crawlers."),
        ("2. SlowAPI Rate Limiter", "Token-bucket throttler (@limiter.limit(RATE_LIMIT)) prohibits DDoS attacks, query flooding, and GPU memory saturation."),
        ("3. Magic-Byte Inspection", "Strict MIME magic-byte validation and 10MB ceiling reject malicious binaries; forces input resolution clamping to 128x128."),
        ("4. Air-Gapped Sovereignty", "100% on-premises execution on NVIDIA RTX 4050 ensures sensitive municipal cadastral GIS telemetry never leaves local hardware boundaries."),
        ("5. Human-in-the-Loop Limits", "Generative outputs serve strictly as advisory decision support; autonomous legal municipal zoning enforcement is prohibited.")
    ]
    for title, desc in sec_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = title + ": "
        p.font.size = Pt(7.6)
        p.font.bold = True
        p.font.color.rgb = ROSE_ACC
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(7.4)
        run.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2.5)

    # --- Card L4: Overall Ranking Champions (Top: 17.80, Height: 5.5) ---
    add_card(col1_left, 17.80, col1_w, 5.5, "Overall Ranking: Best Model per Task", "CHAMPIONS", GREEN_ACC, GREEN_TINT, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(18.23), Inches(col1_w - 0.3), Inches(5.0))
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

    # --- Card L5: Green AI Compute & Carbon Footprint (Top: 23.45, Height: 4.8) ---
    add_card(col1_left, 23.45, col1_w, 4.8, "Green AI & Hardware Efficiency Audit", "SUSTAINABLE AI", GREEN_ACC, GREEN_TINT, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(23.88), Inches(col1_w - 0.3), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = (
        "• Edge Compute Hardware: NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM, 75W TGP).\n"
        "• Total Cumulative Training: 66.3 Minutes across all 6 deep models (50 epochs each).\n"
        "• Energy & Carbon: 0.133 kWh total energy | 94.8 g CO2e footprint (CEA India factor 0.713 kg/kWh).\n"
        "• Democratization: Proves municipal offices can run GenAI without cloud clusters."
    )
    p.font.size = Pt(7.4)
    p.font.color.rgb = DARK_TEXT

    # Embed Proportional Image: fig_energy_carbon_breakdown.png (ratio 2.38:1)
    add_proportional_image("docs/poster/figures/fig_energy_carbon_breakdown.png", col1_left + 0.15, 25.75, col1_w - 0.3, 2.3)

    # --- Card L6: Ethical Governance & Scientific Takeaways (Top: 28.40, Height: 4.8) ---
    add_card(col1_left, 28.40, col1_w, 4.8, "Scientific Takeaways & Governance", "SYNTHESIS & ETHICS", COBALT, SKY_TINT, COBALT)
    tbox = slide.shapes.add_textbox(Inches(col1_left + 0.15), Inches(28.83), Inches(col1_w - 0.3), Inches(4.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    concl_text = [
        ("Modular Inductive Bias", "Proved modular specialized neural networks outperform monolithic foundation models for remote sensing satellite applications."),
        ("Reproducible 50-Epoch Benchmark", "Strictly verified all 6 architectures under identical 50-epoch / 32-batch protocols eliminating batch-dependent gradient noise."),
        ("Edge Data Sovereignty", "Local deployment safeguards sensitive GIS parcels from commercial cloud exposure."),
        ("Advisory AI Decision Boundaries", "Zoning proposals remain strictly advisory; autonomous municipal legal enforcement is prohibited.")
    ]
    for c_title, c_desc in concl_text:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"• {c_title}: "
        p.font.size = Pt(7.6)
        p.font.bold = True
        p.font.color.rgb = COBALT_DARK
        run = p.add_run()
        run.text = c_desc
        run.font.bold = False
        run.font.size = Pt(7.2)
        run.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)


    # =========================================================================
    # RIGHT COLUMN: THE 6 CORE MODELS, ARCHITECTURE FLOW & EVALUATION (y=2.55)
    # Width = 14.2", Sub-columns for 2-column model grid: 6.95" each
    # =========================================================================
    sub_w = 6.95
    sub_gap = 0.30
    sub_c1 = col2_left
    sub_c2 = col2_left + sub_w + sub_gap

    # --- SECTION 1: THE 6 CORE NEURAL MODELS (Top: 2.55, Height: 12.0) ---
    # Model 1 & Model 2 (Row 1, Top: 2.55, Height: 3.8)
    # Model 1: U-Net DAE
    add_card(sub_c1, 2.55, sub_w, 3.85, "Model 1: Denoising AE (U-Net)", "PSNR: 29.65 dB", GREEN_ACC, GREEN_TINT, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(sub_c1 + 0.15), Inches(2.95), Inches(sub_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "ResNet encoder-decoder with multi-scale skip connections bridging Stem, L1, L2, L3 into transposed convs (8->16->32->64->128). Minimizes MSE reconstruction loss via Adam."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "x_hat = D(E(x_corrupted), {F_skip}) | 29.65 dB PSNR (+7.0 dB boost over bottleneck)"
    p.font.size = Pt(7.4)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    # Embed crisp restoration image (natural ratio 0.77:1)
    add_proportional_image("docs/poster/figures/fig_ae_crisp_restoration.png", sub_c1 + 0.15, 4.30, sub_w - 0.3, 2.0)

    # Model 2: Spatial beta-VAE
    add_card(sub_c2, 2.55, sub_w, 3.85, "Model 2: Spatial beta-VAE (Manifold)", "KL: 60.72 nats", PURPLE_ACC, PURPLE_TINT, PURPLE_ACC)
    tbox = slide.shapes.add_textbox(Inches(sub_c2 + 0.15), Inches(2.95), Inches(sub_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Modified ResNet-18 preserving 2D spatial topology in latent space z in R^{64 x 8 x 8} with 4-stage transposed conv decoder. Smooth manifold interpolation and unsupervised anomaly localization."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "L_VAE = (0.7*L_L1 + 0.3*L_MSE) + 10^-4 * D_KL | PSNR: 27.49 dB | KL: 60.72"
    p.font.size = Pt(7.4)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACC
    # Embed multi-interpolation image (natural ratio 2.23:1)
    add_proportional_image("docs/poster/figures/fig_vae_multi_interpolation.png", sub_c2 + 0.15, 4.30, sub_w - 0.3, 2.0)

    # Model 3 & Model 4 (Row 2, Top: 6.55, Height: 3.85)
    # Model 3: ResNet-18 Classifier
    add_card(sub_c1, 6.55, sub_w, 3.85, "Model 3: Land-Use Classifier", "ACCURACY: 98.10%", COBALT, SKY_TINT, COBALT)
    tbox = slide.shapes.add_textbox(Inches(sub_c1 + 0.15), Inches(6.95), Inches(sub_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Pre-trained ResNet-18 transfer learning backbone with 21-class linear projection head. Acts as territorial zoning auditor and generative semantic proxy."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "L_CE = - sum(y_i * log(y_hat_i)) | 98.10% Val Accuracy | Macro F1: 0.9784 | Loss: 0.0615"
    p.font.size = Pt(7.4)
    p.font.bold = True
    p.font.color.rgb = COBALT_DARK
    # Embed classifier metrics image (natural ratio 1.79:1)
    add_proportional_image("docs/poster/figures/fig_classifier_metrics.png", sub_c1 + 0.15, 8.30, sub_w - 0.3, 2.0)

    # Model 4: Residual cDCGAN
    add_card(sub_c2, 6.55, sub_w, 3.85, "Model 4: Residual cDCGAN", "PROXY REC: 99.40%", AMBER_ACC, AMBER_TINT, AMBER_ACC)
    tbox = slide.shapes.add_textbox(Inches(sub_c2 + 0.15), Inches(6.95), Inches(sub_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "4x ResUpBlock Generator + Projection Discriminator with Spectral Normalization, AC-GAN auxiliary head, and EMA. Completely prevents mode collapse."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "L_G = L_adv + 0.8*L_AC | Minimax: D=1.67, G=1.19 | Proxy: 99.40% | Latency: <35ms"
    p.font.size = Pt(7.4)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACC
    # Embed 21-class generated samples (natural ratio 2.33:1)
    add_proportional_image("docs/poster/figures/fig_gan_diverse_generation.png", sub_c2 + 0.15, 8.30, sub_w - 0.3, 2.0)

    # Model 5 & Model 6 (Row 3, Top: 10.55, Height: 4.15)
    # Model 5: DDPM with 5 Losses
    add_card(sub_c1, 10.55, sub_w, 4.15, "Model 5: Conditional DDPM (5 Losses)", "NOISE MSE: 0.0304", ROSE_ACC, ROSE_TINT, ROSE_ACC)
    tbox = slide.shapes.add_textbox(Inches(sub_c1 + 0.15), Inches(10.95), Inches(sub_w - 0.3), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Time- & class-conditioned U-Net with 20-step deterministic DDIM sampler (1.8s synthesis). 5 Explicit Mathematical Loss Formulations:"
    p.font.size = Pt(7.4)
    p.font.color.rgb = DARK_TEXT
    
    diff_losses = (
        "1. L_simple = E_{t,x0,eps}[ ||eps - eps_theta(x_t, t, c)||^2 ] -> Converged to 0.0304\n"
        "2. L_vlb = sum_t D_KL( q(x_{t-1}|x_t, x_0) || p_theta(x_{t-1}|x_t) )  [Variational KL]\n"
        "3. L_guide = gamma * grad_{x_t} log p_phi(y | x_t)  [Classifier gradient steering]\n"
        "4. L_spatial = sum_l w_l * ||Psi_l(x_0) - Psi_l(x_0_hat)||_1  [Edge preservation]\n"
        "5. L_reg = sum_{i,j} sqrt((Delta_x x)^2 + (Delta_y x)^2)  [Total variation regularizer]"
    )
    p = tf.add_paragraph()
    p.text = diff_losses
    p.font.name = 'Courier New'
    p.font.size = Pt(6.8)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACC
    # Embed diffusion metrics curve (natural ratio 3.56:1)
    add_proportional_image("docs/poster/figures/fig_diffusion_metrics.png", sub_c1 + 0.15, 12.80, sub_w - 0.3, 1.8)

    # Model 6: MiniGPT Causal Policy Generator
    add_card(sub_c2, 10.55, sub_w, 4.15, "Model 6: Urban Plan (MiniGPT)", "PPL: 1.110", GREEN_ACC, GREEN_TINT, GREEN_ACC)
    tbox = slide.shapes.add_textbox(Inches(sub_c2 + 0.15), Inches(10.95), Inches(sub_w - 0.3), Inches(3.65))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "4-layer Pre-LayerNorm Causal Transformer (d_model=256, 4 heads, context T=192) trained on PMC municipal planning regulations. Converts spatial rasters into grounded bylaws."
    p.font.size = Pt(7.6)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(2)

    p = tf.add_paragraph()
    p.text = "P(w_t | w_{<t}) = Softmax( (QK^T / sqrt(d_k) + M) * V ) | Perplexity: 1.110 | BPC: 0.1505"
    p.font.name = 'Courier New'
    p.font.size = Pt(7.2)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "Grounded Municipal Zoning Mandates Generated:"
    p.font.size = Pt(7.8)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

    bylaws = [
        ("Floor Space Index (FSI)", "Recommends base FSI 1.8–2.4 along transit spines with density caps."),
        ("TOD Green Buffer", "Mandates 15% green buffer setback along riverbanks and transit corridors."),
        ("Percolation Law", "Enforces permeable paving and solar canopy installation on plots >1000m².")
    ]
    for b_title, b_desc in bylaws:
        p = tf.add_paragraph()
        p.text = f"• {b_title}: {b_desc}"
        p.font.size = Pt(7.3)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(1.5)

    # --- SECTION 2: FULL-WIDTH PLANTUML ARCHITECTURE DIAGRAM (Top: 14.85, Height: 6.2) ---
    add_card(col2_left, 14.85, col2_w, 6.20, "Integrated System Pipeline & Security Architecture (PlantUML High-Res Vector Flow)", "300 DPI VECTOR FLOW", COBALT, SKY_TINT, COBALT)
    # Architecture diagram has natural ratio 2.42:1. Width 13.9" -> Height 5.74"!
    add_proportional_image("docs/poster/figures/pipeline_architecture_plantuml.png", col2_left + 0.15, 15.25, col2_w - 0.3, 5.70)

    # --- SECTION 3: EMPIRICAL BENCHMARKS & EVALUATION GRAPHS (Top: 21.20, Height: 12.0) ---
    add_card(col2_left, 21.20, col2_w, 12.00, "Empirical Evaluation Parametrics & Research Graphs (Uniform 50-Epoch Protocol)", "IEEE BENCHMARK", COBALT, SKY_TINT, COBALT)

    # Left half: Tables (Width = 6.8")
    t1_box = slide.shapes.add_textbox(Inches(col2_left + 0.15), Inches(21.62), Inches(sub_w), Inches(0.28))
    t1_box.text_frame.paragraphs[0].text = "TABLE I: 50-Epoch Multi-Model Verification"
    t1_box.text_frame.paragraphs[0].font.size = Pt(8.2)
    t1_box.text_frame.paragraphs[0].font.bold = True
    t1_box.text_frame.paragraphs[0].font.color.rgb = NAVY

    t1_shape = slide.shapes.add_table(7, 4, Inches(col2_left + 0.15), Inches(21.92), Inches(sub_w), Inches(2.7))
    table1 = t1_shape.table
    table1.columns[0].width = Inches(2.15)
    table1.columns[1].width = Inches(1.6)
    table1.columns[2].width = Inches(1.6)
    table1.columns[3].width = Inches(1.6)

    t1_data = [
        ["Model Pipeline", "Primary", "Secondary", "Final Loss"],
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
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(7.2)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(7.0)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # Table II
    t2_box = slide.shapes.add_textbox(Inches(col2_left + 0.15), Inches(24.75), Inches(sub_w), Inches(0.28))
    t2_box.text_frame.paragraphs[0].text = "TABLE II: Synthesis & Edge Latency Benchmark"
    t2_box.text_frame.paragraphs[0].font.size = Pt(8.2)
    t2_box.text_frame.paragraphs[0].font.bold = True
    t2_box.text_frame.paragraphs[0].font.color.rgb = NAVY

    t2_shape = slide.shapes.add_table(6, 4, Inches(col2_left + 0.15), Inches(25.05), Inches(sub_w), Inches(2.4))
    table2 = t2_shape.table
    table2.columns[0].width = Inches(2.15)
    table2.columns[1].width = Inches(1.6)
    table2.columns[2].width = Inches(1.6)
    table2.columns[3].width = Inches(1.6)

    t2_data = [
        ["Generative Model", "Visual Sharpness", "Latency / Tile", "Advantage / Trade-off"],
        ["Spatial beta-VAE", "Smooth Structural", "12 ms (RTX 4050)", "Fast Manifold Traversal"],
        ["Residual cDCGAN", "High Realism", "32 ms (RTX 4050)", "Instant Augmentation"],
        ["DDPM (1000 Steps)", "Pristine Crispness", "28.4 s (prohibitive)", "Baseline Baseline"],
        ["DDPM (20-Step DDIM)", "Photorealistic", "1.82 s (RTX 4050)", "15.6x speedup, sharp"],
        ["MiniGPT Policy", "Syntactically Sound", "45 ms (192 tokens)", "Contextual Mandates"]
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = table2.cell(r_idx, c_idx)
            cell.text = val
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(7.2)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(7.0)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # Graph below Table II: fig_gan_dynamics.png (ratio 1.79:1)
    g3_lbl = slide.shapes.add_textbox(Inches(col2_left + 0.15), Inches(27.60), Inches(sub_w), Inches(0.25))
    g3_lbl.text_frame.paragraphs[0].text = "Figure 7: cDCGAN Minimax Equilibrium Dynamics (D=1.67, G=1.19)"
    g3_lbl.text_frame.paragraphs[0].font.size = Pt(7.6)
    g3_lbl.text_frame.paragraphs[0].font.bold = True
    g3_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_gan_dynamics.png", col2_left + 0.15, 27.90, sub_w, 5.1)

    # Right half: Graphs (Width = 6.95")
    # Graph 1: fig_psnr_comparison.png (ratio 2.0:1)
    g1_lbl = slide.shapes.add_textbox(Inches(sub_c2), Inches(21.62), Inches(sub_w), Inches(0.28))
    g1_lbl.text_frame.paragraphs[0].text = "Figure 2: Class-Wise PSNR Comparison (+7.0 dB Gain over Bottleneck)"
    g1_lbl.text_frame.paragraphs[0].font.size = Pt(7.6)
    g1_lbl.text_frame.paragraphs[0].font.bold = True
    g1_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_psnr_comparison.png", sub_c2, 21.95, sub_w, 3.4)

    # Graph 2: fig_multimodel_loss_bars.png (ratio 1.90:1)
    g2_lbl = slide.shapes.add_textbox(Inches(sub_c2), Inches(25.55), Inches(sub_w), Inches(0.28))
    g2_lbl.text_frame.paragraphs[0].text = "Figure 9: Initial vs Final 50-Epoch Loss Across All 6 Architectures"
    g2_lbl.text_frame.paragraphs[0].font.size = Pt(7.6)
    g2_lbl.text_frame.paragraphs[0].font.bold = True
    g2_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_multimodel_loss_bars.png", sub_c2, 25.85, sub_w, 3.5)

    # Graph 4: fig_vae_tradeoff.png (ratio 1.79:1)
    g4_lbl = slide.shapes.add_textbox(Inches(sub_c2), Inches(29.50), Inches(sub_w), Inches(0.28))
    g4_lbl.text_frame.paragraphs[0].text = "Figure 5: Spatial beta-VAE Reconstruction Loss vs KL Divergence Trade-off"
    g4_lbl.text_frame.paragraphs[0].font.size = Pt(7.6)
    g4_lbl.text_frame.paragraphs[0].font.bold = True
    g4_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_vae_tradeoff.png", sub_c2, 29.80, sub_w, 3.2)


    # =========================================================================
    # FOOTER BANNER (Top: 33.35", Height: 2.25", Width: 23.2")
    # =========================================================================
    ftr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(33.35), Inches(23.2), Inches(2.25))
    ftr.fill.solid()
    ftr.fill.fore_color.rgb = NAVY
    ftr.line.color.rgb = COBALT
    ftr.line.width = Pt(1.5)

    fBox = slide.shapes.add_textbox(Inches(0.6), Inches(33.42), Inches(22.8), Inches(2.1))
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
        "Project Guides: Prof. Savita Mane & Prof. Pramod Ganjewar  |  Department of Computer Engineering\n"
        "Project Team: Abhay Bhise (202201040024, bhiseabhay890@gmail.com)  •  Disha Satpute (202201040027, dishasatpute44@gmail.com)  •  "
        "Vaishnavi Phad (202201040033, phadvaishnavi1905@gmail.com)  •  Vedant Ingle (202201040065, vedantingle85@gmail.com)\n"
        "Academic Acknowledgment: Submitted in partial fulfillment of the degree of Bachelor of Technology in Computer Engineering (Savitribai Phule Pune University). "
        "Strictly verifiable against submitted IEEE conference publication benchmarks and open-source GitHub reproducibility repository."
    )
    p.font.name = 'Arial'
    p.font.size = Pt(8.2)
    p.font.color.rgb = RGBColor(226, 232, 240)

    # Save to both docs and public folders
    targets = [
        "docs/poster/UrbanGen_AI_Poster_GoldenRatio.pptx",
        "docs/poster/UrbanGen_AI_Poster_v2.pptx",
        "frontend/public/poster/UrbanGen_AI_Poster_GoldenRatio.pptx",
        "frontend/public/poster/UrbanGen_AI_Poster_v2.pptx",
        "frontend/public/poster/UrbanGen_AI_Poster.pptx"
    ]
    saved = []
    for tgt in targets:
        try:
            prs.save(tgt)
            saved.append(tgt)
            print(f"Saved: {tgt}")
        except PermissionError:
            print(f"Warning: {tgt} is locked by PowerPoint. Skipped.")

    print(f"Golden Ratio Poster Generation Complete: {saved}")

if __name__ == '__main__':
    build_golden_ratio_poster()

