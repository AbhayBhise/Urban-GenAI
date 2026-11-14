import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def build_authentimark_pptx():
    prs = Presentation()
    # 24 inches wide x 36 inches high (Standard Academic Poster)
    prs.slide_width = Inches(24)
    prs.slide_height = Inches(36)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background Canvas: Clean subtle slate
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(24), Inches(36))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(241, 245, 249) # #F1F5F9
    bg.line.fill.background()

    # Colors
    NAVY = RGBColor(10, 25, 47)           # #0A192F (AuthentiMark Navy)
    NAVY_LIGHT = RGBColor(15, 32, 56)     # #0F2038
    GOLD = RGBColor(245, 158, 11)         # #F59E0B (AuthentiMark Gold Accent)
    BLUE_ACC = RGBColor(2, 132, 199)      # #0284C7
    CYAN_ACC = RGBColor(56, 189, 248)     # #38BDF8
    GREEN_ACC = RGBColor(5, 150, 105)     # #059669
    ROSE_ACC = RGBColor(225, 29, 72)      # #E11D48
    CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    BORDER_COLOR = RGBColor(226, 232, 240)# #E2E8F0
    DARK_TEXT = RGBColor(15, 23, 42)      # #0F172A
    MUTED_TEXT = RGBColor(71, 85, 105)    # #475569

    def add_card(left, top, width, height, title="", title_bar_color=GOLD, border_color=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.8)

        if title:
            # Gold Accent Bar
            bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.20), Inches(top + 0.16), Inches(0.10), Inches(0.38))
            bar.fill.solid()
            bar.fill.fore_color.rgb = title_bar_color
            bar.line.fill.background()

            # Title
            tbox = slide.shapes.add_textbox(Inches(left + 0.40), Inches(top + 0.12), Inches(width - 0.6), Inches(0.48))
            tf = tbox.text_frame
            tf.word_wrap = True
            tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = 'Arial'
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT

        return card

    def add_proportional_image(img_path, left, top, max_w, max_h):
        if not os.path.exists(img_path):
            return None
        im = Image.open(img_path)
        img_w, img_h = im.size
        aspect = img_w / img_h

        if max_w / max_h > aspect:
            h = max_h
            w = h * aspect
        else:
            w = max_w
            h = w / aspect

        centered_left = left + (max_w - w) / 2.0
        centered_top = top + (max_h - h) / 2.0
        return slide.shapes.add_picture(img_path, Inches(centered_left), Inches(centered_top), width=Inches(w), height=Inches(h))

    # =========================================================================
    # 1. HEADER BANNER (Top: 0.35", Height: 2.40", Width: 23.3")
    # =========================================================================
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(0.35), Inches(23.3), Inches(2.40))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = NAVY
    hdr.line.color.rgb = RGBColor(30, 58, 95)
    hdr.line.width = Pt(1.5)

    # Official MIT AOE Logo Container
    logo_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.55), Inches(4.2), Inches(1.30))
    logo_bg.fill.solid()
    logo_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
    logo_bg.line.fill.background()

    logo_path = "docs/poster/figures/mit_aoe_logo.png"
    if os.path.exists(logo_path):
        add_proportional_image(logo_path, 0.65, 0.62, 4.0, 1.15)

    # Title & Subtitle block
    t_box = slide.shapes.add_textbox(Inches(5.00), Inches(0.48), Inches(12.0), Inches(2.1))
    tf = t_box.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p = tf.paragraphs[0]
    p.text = "MIT ACADEMY OF ENGINEERING · DEPT. OF COMPUTER ENGINEERING"
    p.font.name = 'Arial'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(2)

    p = tf.add_paragraph()
    p.text = "UrbanGen AI"
    p.font.name = 'Arial Black'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(3)

    p = tf.add_paragraph()
    p.text = "Multi-Model Deep Generative Framework for Satellite Imagery Processing & Autonomous Urban Planning"
    p.font.name = 'Arial'
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Header Right (Group Members & Guide)
    r_box = slide.shapes.add_textbox(Inches(17.2), Inches(0.48), Inches(6.2), Inches(2.1))
    rtf = r_box.text_frame
    rtf.word_wrap = True
    rtf.margin_top = rtf.margin_bottom = rtf.margin_left = rtf.margin_right = 0

    p = rtf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    p.text = "GROUP MEMBERS:"
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(2)

    members = [
        "Abhay Bhise (202201040024)",
        "Disha Satpute (202201040027)",
        "Vaishnavi Phad (202201040033)",
        "Vedant Ingle (202201040065)"
    ]
    for m in members:
        p = rtf.add_paragraph()
        p.alignment = PP_ALIGN.RIGHT
        p.text = m
        p.font.name = 'Courier New'
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(241, 245, 249)

    p = rtf.add_paragraph()
    p.alignment = PP_ALIGN.RIGHT
    p.text = "GUIDES: PROF. SAVITA MANE & PROF. PRAMOD GANJEWAR"
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACC

    # =========================================================================
    # 2. ROW 1: PROBLEM STATEMENT & OBJECTIVES (Top: 2.95", Height: 2.30", Width: 23.3")
    # =========================================================================
    half_w = 11.55
    add_card(0.35, 2.95, half_w, 2.30, "Problem Statement")
    tbox = slide.shapes.add_textbox(Inches(0.55), Inches(3.48), Inches(half_w - 0.4), Inches(1.65))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Optical remote sensing rasters suffer from atmospheric cloud attenuation and sensor noise (sigma=0.15). Cadastral municipal datasets lack labeled samples for minority urban land-use categories. Monolithic foundation models cannot simultaneously restore high-frequency signal fidelity, navigate spatial latent manifolds, augment minority classes, and draft legally grounded municipal zoning bylaws."
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_TEXT

    add_card(0.35 + half_w + 0.20, 2.95, half_w, 2.30, "Key Objectives")
    tbox = slide.shapes.add_textbox(Inches(0.35 + half_w + 0.40), Inches(3.45), Inches(half_w - 0.4), Inches(1.70))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    objs = [
        "Modular Multi-Model Pipeline: Deploy 6 specialized deep neural networks (DAE, beta-VAE, Classifier, cDCGAN, DDPM, MiniGPT).",
        "Guaranteed 50-Epoch Benchmark: Benchmark all models under uniform batch size 32, eliminating batch gradient bias.",
        "Air-Gapped Edge Sovereignty: Execute 100% on-premises on consumer hardware (NVIDIA RTX 4050, 0.133 kWh), eliminating GIS data leaks.",
        "Grounded Policy Formulation: Translate spatial analytics into actionable municipal bylaws (FSI, TOD, and green buffers)."
    ]
    for idx, obj in enumerate(objs):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.text = "• " + obj
        p.font.size = Pt(11.8)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # =========================================================================
    # 3. ROW 2: FOUR HIGH-IMPACT METRIC KPI BLOCKS (Top: 5.45", Height: 1.35")
    # =========================================================================
    kpi_w = 5.67
    kpi_gap = 0.20
    kpis = [
        ("2,100", "UCMerced Aerial Imagery Tiles"),
        ("256 × 256", "0.3m GSD, 21 Zoning Classes"),
        ("1,890 / 210", "Train / Val Split (50 Epochs)"),
        ("6 Models", "RTX 4050 6GB · 0.133 kWh Green AI")
    ]
    for idx, (val, sub) in enumerate(kpis):
        kx = 0.35 + idx * (kpi_w + kpi_gap)
        k_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(kx), Inches(5.45), Inches(kpi_w), Inches(1.35))
        k_card.fill.solid()
        k_card.fill.fore_color.rgb = NAVY
        k_card.line.color.rgb = RGBColor(30, 58, 95)
        k_card.line.width = Pt(1.5)

        kt_box = slide.shapes.add_textbox(Inches(kx + 0.1), Inches(5.55), Inches(kpi_w - 0.2), Inches(1.15))
        ktf = kt_box.text_frame
        ktf.word_wrap = True
        ktf.margin_top = ktf.margin_bottom = ktf.margin_left = ktf.margin_right = 0
        kp0 = ktf.paragraphs[0]
        kp0.alignment = PP_ALIGN.CENTER
        kp0.text = val
        kp0.font.name = 'Arial Black'
        kp0.font.size = Pt(28)
        kp0.font.bold = True
        kp0.font.color.rgb = RGBColor(255, 255, 255)
        kp0.space_after = Pt(2)

        kp1 = ktf.add_paragraph()
        kp1.alignment = PP_ALIGN.CENTER
        kp1.text = sub
        kp1.font.name = 'Arial'
        kp1.font.size = Pt(12)
        kp1.font.bold = True
        kp1.font.color.rgb = CYAN_ACC

    # =========================================================================
    # 4. ROW 3: FULL-WIDTH SHARED PIPELINE & PLANTUML ARCHITECTURE (Top: 7.00", Height: 5.60")
    # =========================================================================
    add_card(0.35, 7.00, 23.3, 5.60, "Integrated End-to-End System Pipeline & PlantUML Architecture")
    arch_path = "docs/poster/figures/full_project_architecture_plantuml.png"
    add_proportional_image(arch_path, 0.55, 7.50, 22.9, 4.90)

    # =========================================================================
    # 5. ROW 4: 6 COOPERATIVE NEURAL ARCHITECTURES (Top: 12.80", Height: 9.30")
    # Organized as 3 columns x 2 rows
    # =========================================================================
    m_col_w = 7.63
    m_col_gap = 0.20
    m_r1_y = 12.80
    m_r2_y = 17.50
    m_card_h = 4.55

    # Model 1: U-Net DAE (Row 1, Col 1)
    add_card(0.35, m_r1_y, m_col_w, m_card_h, "Model 1: Denoising AE (U-Net)")
    tbox = slide.shapes.add_textbox(Inches(0.50), Inches(m_r1_y + 0.52), Inches(m_col_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "ResNet encoder-decoder with multi-scale skip connections bridging Stem, L1, L2, L3 into transposed convs (8->16->32->64->128). Minimizes MSE."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Loss: L_AE = 0.00449 MSE (0.00617 total) | PSNR: 29.65 dB (+7.0 dB Gain)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    add_proportional_image("docs/poster/figures/fig_ae_crisp_restoration.png", 0.50, m_r1_y + 1.85, m_col_w - 0.3, 2.55)

    # Model 2: Spatial beta-VAE (Row 1, Col 2)
    m2_x = 0.35 + m_col_w + m_col_gap
    add_card(m2_x, m_r1_y, m_col_w, m_card_h, "Model 2: Spatial beta-VAE (Manifold)")
    tbox = slide.shapes.add_textbox(Inches(m2_x + 0.15), Inches(m_r1_y + 0.52), Inches(m_col_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Preserves 2D spatial topology in latent space z in R^{64 x 8 x 8} with 4-stage transposed conv decoder. Smooth manifold interpolation."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Loss: L_VAE = 0.0483 (KL: 60.72 nats) | PSNR: 27.49 dB | Anomaly: >3sigma"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACC
    add_proportional_image("docs/poster/figures/fig_vae_multi_interpolation.png", m2_x + 0.15, m_r1_y + 1.85, m_col_w - 0.3, 2.55)

    # Model 3: Land-Use Classifier (Row 1, Col 3)
    m3_x = 0.35 + 2 * (m_col_w + m_col_gap)
    add_card(m3_x, m_r1_y, m_col_w, m_card_h, "Model 3: Land-Use Classifier")
    tbox = slide.shapes.add_textbox(Inches(m3_x + 0.15), Inches(m_r1_y + 0.52), Inches(m_col_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Pre-trained ResNet-18 transfer learning backbone with 21-class linear projection head. Acts as automated territorial zoning auditor."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Loss: L_CE = 0.0615 (Cross-Entropy) | Val Acc: 98.10% | Macro F1: 0.9784"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACC
    add_proportional_image("docs/poster/figures/fig_classifier_metrics.png", m3_x + 0.15, m_r1_y + 1.85, m_col_w - 0.3, 2.55)

    # Model 4: Residual cDCGAN (Row 2, Col 1)
    add_card(0.35, m_r2_y, m_col_w, m_card_h, "Model 4: Residual cDCGAN")
    tbox = slide.shapes.add_textbox(Inches(0.50), Inches(m_r2_y + 0.52), Inches(m_col_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "4x ResUpBlock Generator + Projection Discriminator with Spectral Normalization and AC-GAN auxiliary head. Prevents mode collapse."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Loss: Minimax (D=1.67, G=1.19) | Proxy Rec: 99.40% | Latency: <35ms"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD
    add_proportional_image("docs/poster/figures/fig_gan_diverse_generation.png", 0.50, m_r2_y + 1.85, m_col_w - 0.3, 2.55)

    # Model 5: Conditional DDPM (Row 2, Col 2)
    add_card(m2_x, m_r2_y, m_col_w, m_card_h, "Model 5: Conditional DDPM (5 Losses)")
    tbox = slide.shapes.add_textbox(Inches(m2_x + 0.15), Inches(m_r2_y + 0.52), Inches(m_col_w - 0.3), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Time- & class-conditioned U-Net with 20-step deterministic DDIM sampler (1.8s synthesis). 5 Explicit Losses: L_simple + L_vlb + L_guide + L_spatial + L_reg."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p = tf.add_paragraph()
    p.text = "Loss: Noise MSE 0.0304 / VLB 0.02916 | 20-Step DDIM (1.82s, 15.6x faster)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACC
    add_proportional_image("docs/poster/figures/fig_diffusion_metrics.png", m2_x + 0.15, m_r2_y + 1.85, m_col_w - 0.3, 2.55)

    # Model 6: MiniGPT Policy Engine (Row 2, Col 3)
    add_card(m3_x, m_r2_y, m_col_w, m_card_h, "Model 6: Urban Plan (MiniGPT)")
    tbox = slide.shapes.add_textbox(Inches(m3_x + 0.15), Inches(m_r2_y + 0.52), Inches(m_col_w - 0.3), Inches(3.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "4-layer Pre-LayerNorm Causal Transformer (d_model=256, 4 heads, context T=192) trained on PMC municipal planning regulations. Converts spatial rasters into grounded bylaws."
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(2)

    p = tf.add_paragraph()
    p.text = "Loss: Causal CE = 0.1043 | Perplexity: 1.110 | 0.1505 Bits/Char"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Actionable Grounded Municipal Bylaws Drafted:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

    bylaws = [
        ("Floor Space Index (FSI)", "Recommends base FSI 1.8 to 2.4 along transit spines with density caps."),
        ("Transit Buffer (TOD)", "Mandates 15% green buffer setback along riverbanks and transit spines."),
        ("Percolation Mandate", "Enforces permeable paving and solar canopy installation on plots >1000m².")
    ]
    for b_title, b_desc in bylaws:
        p = tf.add_paragraph()
        p.text = f"• {b_title}: {b_desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(1.5)

    # =========================================================================
    # 6. ROW 5: RESEARCH EVALUATION & HEROIC LARGE GRAPHS (Top: 22.35", Height: 8.35")
    # Left: Tables I & II (Width: 9.5"), Right: 4 Large Graphs (Width: 13.6")
    # =========================================================================
    add_card(0.35, 22.35, 23.3, 8.35, "Performance Metrics & Research Evaluation Graphs (Uniform 50-Epoch Protocol)")

    # Left: Tables
    t1_box = slide.shapes.add_textbox(Inches(0.55), Inches(22.80), Inches(9.0), Inches(0.32))
    t1_box.text_frame.paragraphs[0].text = "TABLE I: Multi-Model Performance Verification (50e / 32b)"
    t1_box.text_frame.paragraphs[0].font.size = Pt(11.5)
    t1_box.text_frame.paragraphs[0].font.bold = True
    t1_box.text_frame.paragraphs[0].font.color.rgb = NAVY

    t1_shape = slide.shapes.add_table(7, 4, Inches(0.55), Inches(23.15), Inches(9.0), Inches(2.35))
    table1 = t1_shape.table
    table1.columns[0].width = Inches(2.7)
    table1.columns[1].width = Inches(2.1)
    table1.columns[2].width = Inches(2.1)
    table1.columns[3].width = Inches(2.1)

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
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(10.5)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(10.0)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    t2_box = slide.shapes.add_textbox(Inches(0.55), Inches(25.65), Inches(9.0), Inches(0.32))
    t2_box.text_frame.paragraphs[0].text = "TABLE II: Synthesis & Edge Latency Benchmark"
    t2_box.text_frame.paragraphs[0].font.size = Pt(11.5)
    t2_box.text_frame.paragraphs[0].font.bold = True
    t2_box.text_frame.paragraphs[0].font.color.rgb = NAVY

    t2_shape = slide.shapes.add_table(6, 4, Inches(0.55), Inches(26.00), Inches(9.0), Inches(2.20))
    table2 = t2_shape.table
    table2.columns[0].width = Inches(2.7)
    table2.columns[1].width = Inches(2.1)
    table2.columns[2].width = Inches(2.1)
    table2.columns[3].width = Inches(2.1)

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
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(10.5)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                p.font.size = Pt(10.0)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # Green AI Callout below table II
    ec_callout = slide.shapes.add_textbox(Inches(0.55), Inches(28.35), Inches(9.0), Inches(2.0))
    ectf = ec_callout.text_frame
    ectf.word_wrap = True
    ectf.margin_top = ectf.margin_bottom = ectf.margin_left = ectf.margin_right = 0
    p = ectf.paragraphs[0]
    p.text = "⚡ Green AI Edge Audit: 0.133 kWh total energy | 66.3 min training on RTX 4050 6GB | 94.8 g CO2e carbon cost (CEA India factor). Completely air-gapped with zero cloud GIS exposure."
    p.font.size = Pt(11.0)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    # Right: 4 LARGE HEROIC GRAPHS (2x2 Grid, Width = 6.6" each, Height = 3.65" each)
    gw = 6.6
    gh = 3.55
    gx1 = 9.85
    gx2 = 16.75
    gy1 = 22.85
    gy2 = 26.85

    # Graph 1: fig_psnr_comparison.png
    g1_lbl = slide.shapes.add_textbox(Inches(gx1), Inches(gy1 - 0.32), Inches(gw), Inches(0.30))
    g1_lbl.text_frame.paragraphs[0].text = "Figure 2: Class-Wise PSNR Comparison (+7.0 dB Gain)"
    g1_lbl.text_frame.paragraphs[0].font.size = Pt(11.5)
    g1_lbl.text_frame.paragraphs[0].font.bold = True
    g1_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_psnr_comparison.png", gx1, gy1, gw, gh)

    # Graph 2: fig_multimodel_loss_bars.png
    g2_lbl = slide.shapes.add_textbox(Inches(gx2), Inches(gy1 - 0.32), Inches(gw), Inches(0.30))
    g2_lbl.text_frame.paragraphs[0].text = "Figure 9: Initial vs Final 50-Epoch Multi-Model Loss Bars"
    g2_lbl.text_frame.paragraphs[0].font.size = Pt(11.5)
    g2_lbl.text_frame.paragraphs[0].font.bold = True
    g2_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_multimodel_loss_bars.png", gx2, gy1, gw, gh)

    # Graph 3: fig_gan_dynamics.png
    g3_lbl = slide.shapes.add_textbox(Inches(gx1), Inches(gy2 - 0.32), Inches(gw), Inches(0.30))
    g3_lbl.text_frame.paragraphs[0].text = "Figure 7: cDCGAN Minimax Training Dynamics"
    g3_lbl.text_frame.paragraphs[0].font.size = Pt(11.5)
    g3_lbl.text_frame.paragraphs[0].font.bold = True
    g3_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_gan_dynamics.png", gx1, gy2, gw, gh)

    # Graph 4: fig_energy_carbon_breakdown.png
    g4_lbl = slide.shapes.add_textbox(Inches(gx2), Inches(gy2 - 0.32), Inches(gw), Inches(0.30))
    g4_lbl.text_frame.paragraphs[0].text = "Figure 10: Energy Consumption & Carbon Footprint Breakdown"
    g4_lbl.text_frame.paragraphs[0].font.size = Pt(11.5)
    g4_lbl.text_frame.paragraphs[0].font.bold = True
    g4_lbl.text_frame.paragraphs[0].font.color.rgb = NAVY
    add_proportional_image("docs/poster/figures/fig_energy_carbon_breakdown.png", gx2, gy2, gw, gh)

    # =========================================================================
    # 7. ROW 6: SECURITY & HARDENING + OVERALL RANKING (Top: 30.90", Height: 2.80")
    # =========================================================================
    sec_w = 12.0
    rank_w = 11.1
    add_card(0.35, 30.90, sec_w, 2.80, "System Security & Website Protection", ROSE_ACC, RGBColor(254, 226, 226))
    tbox = slide.shapes.add_textbox(Inches(0.55), Inches(31.35), Inches(sec_w - 0.4), Inches(2.25))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    sec_lines = [
        ("1. Guarded API Gateway", "Fast endpoints require verified URBANGEN_API_KEY header injection, rejecting unauthorized crawlers."),
        ("2. SlowAPI Rate Limiter", "Token-bucket throttler prohibits DDoS attacks, query abuse, and GPU memory saturation."),
        ("3. Magic-Byte Inspection", "Strict MIME inspection & 10MB ceiling reject malicious binaries; clamps resolution to 128x128."),
        ("4. Edge Air-Gapping", "100% on-premises execution on RTX 4050 ensures municipal GIS data never leaves local hardware."),
        ("5. Human-in-the-Loop", "Outputs serve strictly as advisory decision support; autonomous legal municipal zoning enforcement is prohibited.")
    ]
    for title, desc in sec_lines:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(11.0)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    add_card(0.35 + sec_w + 0.20, 30.90, rank_w, 2.80, "Overall Ranking: Best Model per Task", GREEN_ACC, RGBColor(220, 252, 231))
    tbox = slide.shapes.add_textbox(Inches(0.35 + sec_w + 0.40), Inches(31.35), Inches(rank_w - 0.4), Inches(2.25))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    ranks = [
        ("1. Best Restorer: U-Net Skip DAE", "29.65 dB PSNR (+7.0 dB Gain over bottleneck)"),
        ("2. Best Territorial Auditor: ResNet-18", "98.10% Val Accuracy (Macro F1: 0.9784)"),
        ("3. Best Fast Gen: Residual cDCGAN", "99.40% Classifier Proxy Recognition (<35ms)"),
        ("4. Best Latent Manifold: Spatial beta-VAE", "27.49 dB PSNR / 60.72 nats KL Divergence"),
        ("5. Best Photorealism: DDPM (20e DDIM)", "0.0304 Noise MSE (1.82s inference)"),
        ("6. Best Policy Engine: MiniGPT Transformer", "1.110 Perplexity (0.1505 Bits/Char)")
    ]
    for title, val in ranks:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"{title}: "
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = GREEN_ACC
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # =========================================================================
    # 8. FOOTER BANNER (Top: 33.90", Height: 1.70", Width: 23.3")
    # =========================================================================
    ftr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(33.90), Inches(23.3), Inches(1.70))
    ftr.fill.solid()
    ftr.fill.fore_color.rgb = NAVY
    ftr.line.color.rgb = RGBColor(30, 58, 95)
    ftr.line.width = Pt(1.5)

    fBox = slide.shapes.add_textbox(Inches(0.55), Inches(34.02), Inches(22.9), Inches(1.50))
    ftf = fBox.text_frame
    ftf.word_wrap = True
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0

    p = ftf.paragraphs[0]
    p.text = "MIT ACADEMY OF ENGINEERING, PUNE — B.TECH CAPSTONE PROJECT DEFENSE (2025–2026) · SAVITRIBAI PHULE PUNE UNIVERSITY"
    p.font.name = 'Arial'
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(3)

    p = ftf.add_paragraph()
    p.text = (
        "Academic Acknowledgment: Submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Engineering. "
        "Verified with submitted IEEE conference publication package and 100% reproducible open-source GitHub package."
    )
    p.font.name = 'Arial'
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(226, 232, 240)

    # Save to targets
    targets = [
        "docs/poster/UrbanGen_AI_Poster_AuthentiMark.pptx",
        "frontend/public/poster/UrbanGen_AI_Poster_AuthentiMark.pptx",
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

    print(f"AuthentiMark-Style Poster Generation Complete: {saved}")

if __name__ == '__main__':
    build_authentimark_pptx()
