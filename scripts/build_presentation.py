# -*- coding: utf-8 -*-
"""
UrbanGen AI Defense Presentation Generator
Generates a 28-slide, standard, classic, and technically deep PowerPoint presentation
for External Examiners at MIT Academy of Engineering / SPPU.
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
DOCS_DIR = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs"
PPTX_PATH = os.path.join(DOCS_DIR, "UrbanGen_AI_Project_Presentation.pptx")

# Asset Paths
LOGO_PATH = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\poster\figures\mit_aoe_logo.png"
FIG_4_1_1 = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\clean_project_architecture.png"
FIG_4_1_2 = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\pipeline_architecture_plantuml.png"
FIG_5_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\poster\figures\full_project_architecture_plantuml.png"
FIG_5_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_vae_tradeoff.png"
FIG_6_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_landuse_distribution.png"
FIG_6_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_ae_crisp_restoration.png"
FIG_6_3   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_gan_diverse_generation.png"
FIG_6_4   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_vae_multi_interpolation.png"
FIG_7_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_ae_convergence.png"
FIG_7_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_psnr_comparison.png"
FIG_7_3   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_classifier_metrics.png"
FIG_7_4   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_gan_dynamics.png"
FIG_7_5   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_diffusion_training.png"
FIG_7_6   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_multimodel_loss_bars.png"
FIG_7_7   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_energy_carbon_breakdown.png"
FIG_A_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\archive\turnitin_reports\Screenshot 2026-10-26 225027.png"

# Color Palette: Classic Institutional Luxury
BG_COLOR       = RGBColor(248, 250, 252) # Light Slate
NAVY_DARK      = RGBColor(15, 37, 55)    # Oxford Deep Navy
NAVY_ACCENT    = RGBColor(27, 54, 93)    # Academic Blue
GOLD           = RGBColor(184, 134, 11)  # Dark Goldenrod
GOLD_LIGHT     = RGBColor(212, 175, 55)  # Warm Gold
TEXT_DARK      = RGBColor(30, 41, 59)    # Slate Dark
TEXT_MUTED     = RGBColor(100, 116, 139) # Slate Muted
WHITE          = RGBColor(255, 255, 255)
CARD_BG        = RGBColor(255, 255, 255)
CARD_BORDER    = RGBColor(226, 232, 240)
EMERALD        = RGBColor(16, 185, 129)  # Green AI Accent
CRIMSON        = RGBColor(225, 29, 72)

FONT_SERIF = "Georgia"
FONT_SANS  = "Calibri"


def create_base_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_header(slide, tracker_text, title_text, subtitle_text=""):
    """Adds a standard classic header with category tracker and subtitle."""
    # Background fill
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.color.rgb = BG_COLOR

    # Top accent bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = GOLD
    top_bar.line.color.rgb = GOLD

    # Category Tracker
    tb_tr = slide.shapes.add_textbox(Inches(0.8), Inches(0.25), Inches(11.7), Inches(0.35))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    tf_tr.margin_left = tf_tr.margin_right = tf_tr.margin_top = tf_tr.margin_bottom = 0
    p_tr = tf_tr.paragraphs[0]
    p_tr.text = tracker_text.upper()
    p_tr.font.name = FONT_SANS
    p_tr.font.size = Pt(10)
    p_tr.font.bold = True
    p_tr.font.color.rgb = GOLD

    # Title
    tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(0.55))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_tr.margin_top = tf_tr.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_DARK

    # Subtitle
    if subtitle_text:
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.7), Inches(0.35))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_SANS
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.color.rgb = CARD_BORDER


def add_footer(slide, current_slide, total_slides=28):
    """Adds a standard academic footer."""
    # Footer Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.color.rgb = CARD_BORDER

    # Footer Left
    tb_fl = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.0), Inches(0.35))
    tf_fl = tb_fl.text_frame
    tf_fl.margin_left = tf_fl.margin_right = tf_fl.margin_top = tf_fl.margin_bottom = 0
    p_fl = tf_fl.paragraphs[0]
    p_fl.text = "UrbanGen AI • Third Year B.Tech Major Project–2 • MIT Academy of Engineering, Pune (SPPU)"
    p_fl.font.name = FONT_SANS
    p_fl.font.size = Pt(9.5)
    p_fl.font.color.rgb = TEXT_MUTED

    # Footer Right
    tb_fr = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.0), Inches(0.35))
    tf_fr = tb_fr.text_frame
    tf_fr.margin_left = tf_fr.margin_right = tf_fr.margin_top = tf_fr.margin_bottom = 0
    p_fr = tf_fr.paragraphs[0]
    p_fr.alignment = PP_ALIGN.RIGHT
    p_fr.text = f"{current_slide} / {total_slides}"
    p_fr.font.name = FONT_SANS
    p_fr.font.size = Pt(9.5)
    p_fr.font.bold = True
    p_fr.font.color.rgb = NAVY_DARK


def add_card(slide, left, top, width, height, bg_rgb=WHITE, border_rgb=CARD_BORDER):
    """Creates a classic styled card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_rgb
    card.line.color.rgb = border_rgb
    card.line.width = Pt(1)
    return card


def add_bullet_point(text_frame, title, desc, title_color=NAVY_DARK, font_size=11):
    p = text_frame.add_paragraph()
    p.space_before = Pt(4)
    p.space_after = Pt(4)
    p.line_spacing = 1.15
    run_t = p.add_run()
    run_t.text = "• " + title + ": " if title else "• "
    run_t.font.name = FONT_SANS
    run_t.font.bold = True
    run_t.font.size = Pt(font_size)
    run_t.font.color.rgb = title_color
    
    run_d = p.add_run()
    run_d.text = desc
    run_d.font.name = FONT_SANS
    run_d.font.size = Pt(font_size)
    run_d.font.color.rgb = TEXT_DARK


def add_table(slide, left, top, width, height, headers, rows, col_widths=None):
    """Adds a classic IEEE-styled table."""
    num_rows = len(rows) + 1
    num_cols = len(headers)
    tbl_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = tbl_shape.table
    
    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

    # Headers
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = h_text
        run.font.name = FONT_SANS
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        is_even = (r_idx % 2 == 0)
        row_bg = WHITE if is_even else RGBColor(241, 245, 249)
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = str(val)
            run.font.name = FONT_SANS
            run.font.size = Pt(9.5)
            run.font.color.rgb = TEXT_DARK
            if "Ours" in str(val) or "Proposed" in str(val) or "Champion" in str(val):
                run.font.bold = True
                run.font.color.rgb = NAVY_ACCENT
    return tbl_shape


# =============================================================================
# SLIDE BUILDERS (1 TO 28)
# =============================================================================

def build_all_slides():
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]
    
    print("Building Slide 1: Title Slide...")
    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE (Classic Academic Navy & Gold)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.color.rgb = NAVY_DARK

    # Gold Accent Top and Bottom Lines
    bar_top = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.04))
    bar_top.fill.solid()
    bar_top.fill.fore_color.rgb = GOLD
    bar_top.line.color.rgb = GOLD

    bar_bot = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.04))
    bar_bot.fill.solid()
    bar_bot.fill.fore_color.rgb = GOLD
    bar_bot.line.color.rgb = GOLD

    # Institute Logo
    if os.path.exists(LOGO_PATH):
        s1.shapes.add_picture(LOGO_PATH, Inches(1.0), Inches(0.85), width=Inches(2.4))

    # Institute Header Text
    tb_inst = s1.shapes.add_textbox(Inches(3.6), Inches(0.85), Inches(8.8), Inches(1.0))
    tf_inst = tb_inst.text_frame
    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "MIT Academy of Engineering, Alandi (D), Pune"
    p_i1.font.name = FONT_SERIF
    p_i1.font.size = Pt(17)
    p_i1.font.bold = True
    p_i1.font.color.rgb = WHITE
    p_i2 = tf_inst.add_paragraph()
    p_i2.text = "An Autonomous Institute Affiliated to Savitribai Phule Pune University (SPPU)\nDepartment of Computer Engineering • Academic Year 2025–2026"
    p_i2.font.name = FONT_SANS
    p_i2.font.size = Pt(11)
    p_i2.font.color.rgb = GOLD_LIGHT

    # Presentation Category Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.15), Inches(6.4), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(27, 54, 93)
    badge.line.color.rgb = GOLD
    p_bd = badge.text_frame.paragraphs[0]
    p_bd.text = "THIRD YEAR B.TECH MAJOR PROJECT–2 • FINAL VIVA DEFENSE"
    p_bd.font.name = FONT_SANS
    p_bd.font.size = Pt(10)
    p_bd.font.bold = True
    p_bd.font.color.rgb = GOLD_LIGHT
    p_bd.alignment = PP_ALIGN.CENTER

    # Project Title
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.3), Inches(1.6))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "UrbanGen AI: A Multi-Model Generative Framework for Satellite Imagery Processing, Land-Use Analytics, and Sustainable Urban Planning"
    p_t1.font.name = FONT_SERIF
    p_t1.font.size = Pt(24)
    p_t1.font.bold = True
    p_t1.font.color.rgb = WHITE
    p_t1.line_spacing = 1.15

    # Subtitle
    p_t2 = tf_title.add_paragraph()
    p_t2.text = "An Edge-Computable, 6-Architecture Generative Framework for Remote Sensing Restoration, Topology Preservation, Parcel Prototyping, and Grounded Municipal Bylaw Drafting"
    p_t2.font.name = FONT_SANS
    p_t2.font.size = Pt(12)
    p_t2.font.italic = True
    p_t2.font.color.rgb = RGBColor(203, 213, 225)
    p_t2.space_before = Pt(6)

    # Students & Guides Panel
    add_card(s1, Inches(1.0), Inches(4.55), Inches(6.0), Inches(2.1), bg_rgb=RGBColor(20, 45, 68), border_rgb=RGBColor(30, 60, 90))
    tb_st = s1.shapes.add_textbox(Inches(1.2), Inches(4.65), Inches(5.6), Inches(1.9))
    tf_st = tb_st.text_frame
    p_sth = tf_st.paragraphs[0]
    p_sth.text = "PROJECT CANDIDATES"
    p_sth.font.name = FONT_SANS
    p_sth.font.size = Pt(11)
    p_sth.font.bold = True
    p_sth.font.color.rgb = GOLD_LIGHT
    students_list = [
        ("Abhay Bhise", "Exam Seat No: 202402040001"),
        ("Disha Satpute", "Exam Seat No: 202402040019"),
        ("Vaishnavi Phad", "Exam Seat No: 202402040006"),
        ("Vedant Ingle", "Exam Seat No: 202402040020")
    ]
    for s_name, s_seat in students_list:
        p_s = tf_st.add_paragraph()
        p_s.text = f"• {s_name}  ({s_seat})"
        p_s.font.name = FONT_SANS
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = WHITE

    add_card(s1, Inches(7.3), Inches(4.55), Inches(5.0), Inches(2.1), bg_rgb=RGBColor(20, 45, 68), border_rgb=RGBColor(30, 60, 90))
    tb_gd = s1.shapes.add_textbox(Inches(7.5), Inches(4.65), Inches(4.6), Inches(1.9))
    tf_gd = tb_gd.text_frame
    p_gdh = tf_gd.paragraphs[0]
    p_gdh.text = "SUPERVISION & GUIDANCE"
    p_gdh.font.name = FONT_SANS
    p_gdh.font.size = Pt(11)
    p_gdh.font.bold = True
    p_gdh.font.color.rgb = GOLD_LIGHT
    
    guides_info = [
        ("Prof. Savita Mane", "Project Advisor & Assistant Professor"),
        ("Prof. Pramod Ganjewar", "Project Co-Advisor & Head of Department"),
        ("Dr. Kanchan Dhote", "Capstone Project Coordinator")
    ]
    for g_name, g_role in guides_info:
        p_g = tf_gd.add_paragraph()
        p_g.text = f"• {g_name} — {g_role}"
        p_g.font.name = FONT_SANS
        p_g.font.size = Pt(10)
        p_g.font.color.rgb = WHITE

    print("Building Slide 2: Executive Summary & Project Overview...")
    # -------------------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "EXECUTIVE SUMMARY", "Project Mission: Cooperative Multi-Model Generative AI", "Bridging the methodological divide between raw satellite remote sensing and qualitative municipal policy formulation")
    add_footer(s2, 2)

    # Mission Statement Card
    add_card(s2, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.3), bg_rgb=RGBColor(241, 245, 249))
    tb_ms = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(1.1))
    tf_ms = tb_ms.text_frame
    tf_ms.word_wrap = True
    p_msh = tf_ms.paragraphs[0]
    p_msh.text = "THE CORE ARCHITECTURAL PARADIGM"
    p_msh.font.name = FONT_SANS
    p_msh.font.size = Pt(10.5)
    p_msh.font.bold = True
    p_msh.font.color.rgb = GOLD
    p_mst = tf_ms.add_paragraph()
    p_mst.text = "Rather than relying on an isolated monolithic model, UrbanGen AI coordinates six specialized, edge-computable deep learning architectures operating under a unified 50-epoch benchmark protocol on the standardized USGS UCMerced LandUse dataset (2,100 orthoimages, 21 classes, 0.3m GSD). The framework establishes a closed-loop digital twin: restoring corrupted rasters, navigating a topology-preserving 3D latent manifold, auditing semantic fidelity, synthesizing parcels via dual adversarial/diffusion paths, and drafting legally grounded municipal bylaws."
    p_mst.font.name = FONT_SANS
    p_mst.font.size = Pt(11)
    p_mst.font.color.rgb = TEXT_DARK
    p_mst.space_before = Pt(3)

    # 6 KPIs Callouts
    kpis = [
        ("+7.0 dB PSNR", "Optical Restoration Gain", "Skip-connected U-Net vs baseline (29.65 dB)"),
        ("98.10% / 0.978", "ResNet-18 Auditor Acc", "Macro F1: 0.9784 across 21 land-use categories"),
        ("32 ms / 99.4%", "Residual cDCGAN Speed", "Edge real-time parcel generation with zero collapse"),
        ("1.82 s / 0.030", "20-Step DDIM Diffusion", "Noise MSE 0.0304 with 15.6x accelerated speedup"),
        ("1.110 PPL", "MiniGPT Causal Bylaws", "0.1505 bits/char on Pune PMC zoning directives"),
        ("0.112 kWh", "Green AI Carbon Budget", "79.1 g CO2e total training on consumer RTX 4050")
    ]
    card_w = Inches(3.75)
    card_h = Inches(1.7)
    for idx, (stat, label, detail) in enumerate(kpis):
        r_idx = idx // 3
        c_idx = idx % 3
        c_left = Inches(0.8) + c_idx * Inches(3.95)
        c_top = Inches(3.1) + r_idx * Inches(1.85)
        add_card(s2, c_left, c_top, card_w, card_h)
        tb_k = s2.shapes.add_textbox(c_left + Inches(0.15), c_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
        tf_k = tb_k.text_frame
        p_st = tf_k.paragraphs[0]
        p_st.text = stat
        p_st.font.name = FONT_SERIF
        p_st.font.size = Pt(19)
        p_st.font.bold = True
        p_st.font.color.rgb = NAVY_ACCENT
        p_lbl = tf_k.add_paragraph()
        p_lbl.text = label
        p_lbl.font.name = FONT_SANS
        p_lbl.font.size = Pt(10.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = GOLD
        p_det = tf_k.add_paragraph()
        p_det.text = detail
        p_det.font.name = FONT_SANS
        p_det.font.size = Pt(9.5)
        p_det.font.color.rgb = TEXT_MUTED

    print("Building Slide 3: Motivation & Civic Challenges...")
    # -------------------------------------------------------------------------
    # SLIDE 3: MOTIVATION & CIVIC CHALLENGES
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "PROBLEM CONTEXT", "Motivation: Real-World Smart City & Remote Sensing Challenges", "Why traditional municipal GIS workflows and monolithic vision models fail in sustainable urban governance")
    add_footer(s3, 3)

    challenges = [
        ("Atmospheric Noise & Sensor Degradation", 
         "Orbital optical sensors suffer from aerosol scattering, cloud haze, and sensor degradation. Consequently, ingested rasters lose high-frequency geometric street edges and parcel boundaries, propagating catastrophic error into automated classification and encroachment detection algorithms."),
        ("Traditional GIS Inefficiency & Static Boundaries", 
         "Municipal GIS workflows rely on manual photointerpretation by scarce expert cartographers, taking weeks to update zoning databases. Crucially, static vector maps cannot simulate speculative urban scenarios, leaving town planners reactive rather than proactive."),
        ("The Spatial-to-Policy Semantic Divide", 
         "Computer vision networks output raw pixels or categorical labels, whereas town planners operate on qualitative legal bylaws—such as Floor Space Index (FSI), Transit-Oriented Development (TOD) setbacks, and riverbank buffers. No existing system automatically bridges this divide."),
        ("Data Sovereignty & Cybersecurity in Municipal Planning", 
         "Uploading sensitive cadastral maps, property ownership records, and internal defense-zone orthoimagery to commercial cloud APIs (OpenAI, AWS) violates national data sovereignty and municipal privacy laws. Models must run 100% on-premises."),
        ("The Unsustainable Carbon Footprint of Cloud AI (Green AI)", 
         "Datacenter foundation models require multi-megawatt clusters and emit metric tons of CO2e. Municipalities cannot afford expensive recurring GPU cloud instances. There is an urgent need for edge-computable models trained on consumer-grade hardware under a strictly audited energy budget.")
    ]
    for idx, (title, desc) in enumerate(challenges):
        c_top = Inches(1.6) + idx * Inches(1.05)
        add_card(s3, Inches(0.8), c_top, Inches(11.733), Inches(0.95))
        tb_c = s3.shapes.add_textbox(Inches(1.0), c_top + Inches(0.08), Inches(11.3), Inches(0.8))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        p_ch = tf_c.paragraphs[0]
        p_ch.text = f"{idx+1}. {title}"
        p_ch.font.name = FONT_SANS
        p_ch.font.size = Pt(11)
        p_ch.font.bold = True
        p_ch.font.color.rgb = NAVY_ACCENT
        p_cd = tf_c.add_paragraph()
        p_cd.text = desc
        p_cd.font.name = FONT_SANS
        p_cd.font.size = Pt(9.5)
        p_cd.font.color.rgb = TEXT_DARK
        p_cd.space_before = Pt(2)

    print("Building Slide 4: Problem Definition & Quantified Scope...")
    # -------------------------------------------------------------------------
    # SLIDE 4: PROBLEM STATEMENT & QUANTIFIED OBJECTIVES
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "RESEARCH OBJECTIVES", "Formal Problem Definition & Quantifiable Target Metrics", "Formulating seven rigorous, verifiable engineering goals under strict edge-hardware boundaries")
    add_footer(s4, 4)

    # Left: Formal Problem Statement Card
    add_card(s4, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_ps = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.7))
    tf_ps = tb_ps.text_frame
    tf_ps.word_wrap = True
    p_ph = tf_ps.paragraphs[0]
    p_ph.text = "FORMAL PROBLEM STATEMENT"
    p_ph.font.name = FONT_SERIF
    p_ph.font.size = Pt(13)
    p_ph.font.bold = True
    p_ph.font.color.rgb = NAVY_DARK
    
    p_pt = tf_ps.add_paragraph()
    p_pt.text = "Design, develop, and benchmark an integrated, edge-computable multi-model generative artificial intelligence framework that ingests degraded satellite remote sensing orthoimagery, restores high-frequency structural parcel boundaries, navigates an explicit topology-preserving 3D latent manifold to detect unauthorized zoning encroachments, synthesizes speculative urban parcel scenarios with verified semantic fidelity via both real-time adversarial and photorealistic diffusion mechanisms, and automatically formulates legally compliant municipal development control regulations without factual hallucination—all executed under a strictly auditable, low-carbon Green AI edge budget."
    p_pt.font.name = FONT_SANS
    p_pt.font.size = Pt(10)
    p_pt.font.color.rgb = TEXT_DARK
    p_pt.space_before = Pt(8)
    p_pt.line_spacing = 1.2

    # Right: 7 Quantified Goals Grid
    goals = [
        ("1. Signal Restoration", "U-Net DAE: PSNR >= 29 dB, SSIM >= 0.85 on noisy tiles (sigma = 0.15)"),
        ("2. Topology Preservation", "Spatial beta-VAE: 3D tensor latent R^(64x8x8), calibrated beta = 10^-4"),
        ("3. Anomaly Screening", "Unsupervised disparity engine flagging unpermitted building > 3 sigma"),
        ("4. Semantic Auditing", "Frozen ResNet-18 classifier achieving >= 98% validation accuracy"),
        ("5. Real-Time Synthesis", "Residual cDCGAN: Latency <= 35 ms with >= 99% proxy recognition"),
        ("6. Diffusion Prototyping", "Conditional DDPM + 20-step DDIM sampler: <= 2.0 s, noise MSE <= 0.035"),
        ("7. Policy & Green AI", "MiniGPT: Perplexity <= 1.15; Total 6-model training energy <= 0.15 kWh")
    ]
    add_card(s4, Inches(5.5), Inches(1.6), Inches(7.033), Inches(5.1))
    tb_g = s4.shapes.add_textbox(Inches(5.7), Inches(1.8), Inches(6.6), Inches(4.7))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    p_gh = tf_g.paragraphs[0]
    p_gh.text = "SEVEN QUANTIFIABLE ENGINEERING OBJECTIVES"
    p_gh.font.name = FONT_SERIF
    p_gh.font.size = Pt(13)
    p_gh.font.bold = True
    p_gh.font.color.rgb = GOLD
    for idx, (gt, gd) in enumerate(goals):
        p_item = tf_g.add_paragraph()
        p_item.text = f"{gt}: {gd}"
        p_item.font.name = FONT_SANS
        p_item.font.size = Pt(10)
        p_item.font.color.rgb = TEXT_DARK
        p_item.space_before = Pt(6)

    print("Building Slide 5: Literature Review & Gaps...")
    # -------------------------------------------------------------------------
    # SLIDE 5: LITERATURE REVIEW & RESEARCH GAPS
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "STATE OF THE ART", "Literature Review & Research Gaps in Remote Sensing AI", "Comparative assessment of existing remote sensing techniques, generative models, and planning tools")
    add_footer(s5, 5)

    lit_cols = [Inches(2.5), Inches(4.5), Inches(4.7)]
    lit_headers = ["Domain / Paradigm", "State-of-the-Art Approaches", "Inherent Limitation / UrbanGen AI Novelty"]
    lit_rows = [
        ["Optical Restoration", "Vincent et al. (DAE) [16], Zhang et al. (DnCNN) [17], SwinIR [19]", "Standard bottleneck autoencoders oversmooth high-frequency edges; SwinIR requires 11.8M params & 142 ms latency. UrbanGen uses multi-scale skip connections in 8.4 ms."],
        ["Scene Classification", "Cheng et al. [12], He et al. (ResNet) [14], Bag-of-Visual-Words [13]", "Classifiers are typically standalone models. UrbanGen adapts a frozen ResNet-18 as an objective mathematical auditor to eliminate human bias in generative evaluation."],
        ["Adversarial Parcel Synthesis", "Goodfellow [28], Radford (DCGAN) [29], Mirza (cGAN) [30], StyleGAN2 [35]", "Standard cGANs suffer from mode collapse; StyleGAN2 requires 4.8 GB VRAM. UrbanGen stabilizes cDCGAN via Spectral Normalization and projection conditioning in 32 ms."],
        ["Diffusion Models in RS", "Ho et al. (DDPM) [37], Song (DDIM) [38], Remote-Diffusion [6]", "1,000-step ancestral DDPM requires 28.4 s per tile, prohibiting edge use. UrbanGen accelerates class-conditional diffusion via 20-step DDIM in 1.82 s with 0.0304 MSE."],
        ["Municipal Policy Modeling", "Commercial LLMs (ChatGPT, Claude), Rule-based GIS scripts", "General LLMs hallucinate regional bylaws and violate municipal data sovereignty. UrbanGen deploys an on-premises causal Transformer (1.110 perplexity) on PMC DCPR-2017."]
    ]
    add_table(s5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), lit_headers, lit_rows, lit_cols)

    print("Building Slide 6: 3-Tier System Architecture...")
    # -------------------------------------------------------------------------
    # SLIDE 6: 3-TIER SYSTEM ARCHITECTURE
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "SYSTEM ARCHITECTURE", "UrbanGen AI Three-Tier Enterprise System Architecture", "Coordinating web visualization, high-performance microservices, and edge neural inference")
    add_footer(s6, 6)

    # Embed Figure 4.1.1
    if os.path.exists(FIG_4_1_1):
        s6.shapes.add_picture(FIG_4_1_1, Inches(0.8), Inches(1.6), width=Inches(6.8))

    # Architecture Explanation Card on Right
    add_card(s6, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.1))
    tb_arc = s6.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(4.7))
    tf_arc = tb_arc.text_frame
    tf_arc.word_wrap = True
    
    p_ah = tf_arc.paragraphs[0]
    p_ah.text = "THREE-TIER MODULAR DECOUPLING"
    p_ah.font.name = FONT_SERIF
    p_ah.font.size = Pt(12)
    p_ah.font.bold = True
    p_ah.font.color.rgb = GOLD

    add_bullet_point(tf_arc, "Tier 1: Presentation Layer", "Engineered in React 18, TypeScript, Vite, and Tailwind CSS. Provides town planners with interactive dropzones, alpha-sliders for manifold morphing, live PSNR readouts, and bylaw prompts at responsive 60 FPS.", font_size=10)
    add_bullet_point(tf_arc, "Tier 2: Asynchronous Inference Engine", "Hosted via FastAPI and Uvicorn with ASGI worker pools. Directs PyTorch 2.x CUDA execution streams across all six specialized neural modules with lazy weight loading and VRAM memory pinning.", font_size=10)
    add_bullet_point(tf_arc, "Tier 3: Cadastral GIS & Persistence", "Local SQLite metadata repository, Pune Municipal GIS shapefiles, calibrated model weight checkpoints, and real-time NVML hardware telemetry polling without cloud dependencies.", font_size=10)

    print("Building Slide 7: End-to-End Operational Pipeline...")
    # -------------------------------------------------------------------------
    # SLIDE 7: OPERATIONAL PIPELINE & DATAFLOW
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "OPERATIONAL DATAFLOW", "End-to-End Multi-Model Planning Pipeline Workflow", "Sequential and parallel interactions from corrupted satellite raster ingestion to grounded policy synthesis")
    add_footer(s7, 7)

    if os.path.exists(FIG_4_1_2):
        s7.shapes.add_picture(FIG_4_1_2, Inches(0.8), Inches(1.6), width=Inches(7.2))

    # Pipeline Steps on Right
    add_card(s7, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.1))
    tb_pf = s7.shapes.add_textbox(Inches(8.4), Inches(1.8), Inches(3.9), Inches(4.7))
    tf_pf = tb_pf.text_frame
    tf_pf.word_wrap = True
    p_ph = tf_pf.paragraphs[0]
    p_ph.text = "CLOSED-LOOP EXECUTION STAGES"
    p_ph.font.name = FONT_SERIF
    p_ph.font.size = Pt(12)
    p_ph.font.bold = True
    p_ph.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_pf, "1. Ingestion & Perturbation", "Raw aerial raster received and perturbed with Gaussian sensor noise (sigma=0.15).", font_size=9.5)
    add_bullet_point(tf_pf, "2. Optical Restoration", "U-Net DAE removes atmospheric scattering in 8.4 ms with 29.65 dB PSNR.", font_size=9.5)
    add_bullet_point(tf_pf, "3. Latent Manifold & Anomaly", "Spatial beta-VAE encodes 3D latent tensor; disparity map flags >3 sigma encroachment.", font_size=9.5)
    add_bullet_point(tf_pf, "4. Autonomous Semantic Audit", "Frozen ResNet-18 verifies zoning classification (98.10% accuracy).", font_size=9.5)
    add_bullet_point(tf_pf, "5. Dual-Modality Generation", "cDCGAN generates parcel in 32 ms or DDIM diffusion delivers photorealism in 1.82 s.", font_size=9.5)
    add_bullet_point(tf_pf, "6. Causal Bylaw Formulation", "MiniGPT synthesizes localized FSI bylaws and TOD setbacks with 1.110 perplexity.", font_size=9.5)

    print("Building Slide 8: Neural Specifications Matrix...")
    # -------------------------------------------------------------------------
    # SLIDE 8: THE SIX NEURAL ARCHITECTURES
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "MODEL ARCHITECTURES", "Unified Multi-Model Neural Specifications & Edge Profiles", "Layer-by-layer specifications, parameters, and inference latency across all six specialized modules")
    add_footer(s8, 8)

    m_cols = [Inches(1.8), Inches(1.4), Inches(2.6), Inches(2.6), Inches(1.1), Inches(1.1), Inches(1.1)]
    m_headers = ["Module", "Input Dim", "Encoder / Backbone", "Decoder / Output Head", "Params", "Latency", "VRAM"]
    m_rows = [
        ["Model 1: U-Net DAE", "3 x 128 x 128", "ResNet Stem -> L1(64) -> L2(128) -> L3(256)", "4-Stage Transposed Conv + Skips", "3.87 M", "8.4 ms", "410 MB"],
        ["Model 2: Spatial beta-VAE", "3 x 128 x 128", "Deep Conv Stem -> mu, log sigma^2 in R^(64x8x8)", "4-Stage Transposed Conv (0.2 Drop)", "3.75 M", "11.2 ms", "528 MB"],
        ["Model 3: ResNet-18 Auditor", "3 x 128 x 128", "ResNet-18 (ImageNet Pretrained)", "21-Way Linear Projection Head", "11.19 M", "5.1 ms", "380 MB"],
        ["Model 4: Residual cDCGAN", "z in R^128, y in R^21", "4 x ResUpBlocks + Cond BatchNorm (G: 8.82M)", "Projection Discriminator + SN (D: 6.97M)", "15.79 M", "32.0 ms", "620 MB"],
        ["Model 5: Conditional DDPM", "3 x 128 x 128 + t + c", "Time/Class Conditioned Residual U-Net", "20-Step Deterministic DDIM Sampler", "2.80 M", "1,820 ms", "890 MB"],
        ["Model 6: MiniGPT Transformer", "Tokens in R^192", "4-Layer Pre-LN Causal Blocks (d_m = 256)", "Causal LM Projection Head (V = 64)", "3.23 M", "45.0 ms", "290 MB"]
    ]
    add_table(s8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5), m_headers, m_rows, m_cols)

    # Bottom summary card
    add_card(s8, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.75), bg_rgb=RGBColor(241, 245, 249))
    tb_msum = s8.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.65))
    tf_msum = tb_msum.text_frame
    p_msu = tf_msum.paragraphs[0]
    p_msu.text = "TOTAL INTEGRATED FRAMEWORK: 40.63 M parameters across all 6 architectures. Peak inference VRAM requirement is under 1.8 GB, permitting concurrent execution on low-cost edge hardware (NVIDIA RTX 4050 6 GB Laptop GPU) with ample headroom."
    p_msu.font.name = FONT_SANS
    p_msu.font.size = Pt(10)
    p_msu.font.bold = True
    p_msu.font.color.rgb = NAVY_ACCENT

    print("Building Slide 9: Mathematical Foundations — Stage 1: U-Net DAE...")
    # -------------------------------------------------------------------------
    # SLIDE 9: MATHEMATICAL FOUNDATIONS — STAGE 1 (U-NET DAE)
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "MATHEMATICAL FORMULATIONS", "Stage 1: Multi-Scale Skip-Connected Optical Restoration", "Overcoming bottleneck oversmoothing via hierarchical transposed skip bridges")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tb_ae1 = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_ae1 = tb_ae1.text_frame
    tf_ae1.word_wrap = True
    p_a1 = tf_ae1.paragraphs[0]
    p_a1.text = "MATHEMATICAL LOSS OBJECTIVE"
    p_a1.font.name = FONT_SERIF
    p_a1.font.size = Pt(12)
    p_a1.font.bold = True
    p_a1.font.color.rgb = GOLD

    p_eq1 = tf_ae1.add_paragraph()
    p_eq1.text = "L_AE = (1/N) * sum_{i=1}^N || x^(i) - x_hat^(i) ||_2^2 + lambda * sum_l || W_l ||_2^2"
    p_eq1.font.name = "Consolas"
    p_eq1.font.size = Pt(10)
    p_eq1.font.bold = True
    p_eq1.font.color.rgb = NAVY_DARK
    p_eq1.space_before = Pt(6)

    add_bullet_point(tf_ae1, "Pixel-Wise Reconstruction Term", "Minimizes Mean Squared Error between degraded input x_tilde and ground truth uncorrupted raster x.", font_size=10)
    add_bullet_point(tf_ae1, "L2 Weight Regularization (lambda = 10^-5)", "Prevents filter parameter divergence while preserving high-frequency spatial gradients.", font_size=10)
    add_bullet_point(tf_ae1, "The Bottleneck Dilemma", "Standard autoencoders compress features to a narrow bottleneck, irreversibly destroying fine 90-degree parcel edges and road lines.", font_size=10)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_ae2 = s9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_ae2 = tb_ae2.text_frame
    tf_ae2.word_wrap = True
    p_a2 = tf_ae2.paragraphs[0]
    p_a2.text = "MULTI-SCALE SKIP-CONNECTION ARCHITECTURE"
    p_a2.font.name = FONT_SERIF
    p_a2.font.size = Pt(12)
    p_a2.font.bold = True
    p_a2.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_ae2, "Encoder Pathway", "ResNet Stem (3 -> 64) -> Layer 1 (64) -> Layer 2 (128) -> Layer 3 (256) -> Bottleneck (512x8x8).", font_size=10)
    add_bullet_point(tf_ae2, "Decoder Pathway", "4-stage transposed convolutions (512 -> 256 -> 128 -> 64 -> 32 -> 3) with BatchNorm and LeakyReLU (alpha=0.2).", font_size=10)
    add_bullet_point(tf_ae2, "Direct Concatenation Skips", "Stem features (128x128), Layer 1 (64x64), and Layer 2 (32x32) bypass the bottleneck and concatenate directly into transposed stages.", font_size=10)
    add_bullet_point(tf_ae2, "Empirical Validation", "Achieves 29.65 dB PSNR (+7.0 dB over corrupted baseline, SSIM 0.8649), recovering sharp orthogonal parcel geometries in 8.4 ms.", font_size=10)

    print("Building Slide 10: Stage 2: Spatial beta-VAE & Anomaly Engine...")
    # -------------------------------------------------------------------------
    # SLIDE 10: STAGE 2 (SPATIAL BETA-VAE & ANOMALY DETECTION)
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "MATHEMATICAL FORMULATIONS", "Stage 2: Spatial beta-VAE & Unsupervised Anomaly Engine", "Preserving 2D spatial topology in an explicit 3D latent tensor under calibrated Pareto regularization")
    add_footer(s10, 10)

    # Embed Pareto Tradeoff Chart
    if os.path.exists(FIG_5_2):
        s10.shapes.add_picture(FIG_5_2, Inches(0.8), Inches(1.6), width=Inches(5.0))

    add_card(s10, Inches(6.0), Inches(1.6), Inches(6.533), Inches(5.1))
    tb_v = s10.shapes.add_textbox(Inches(6.2), Inches(1.8), Inches(6.1), Inches(4.7))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    p_vh = tf_v.paragraphs[0]
    p_vh.text = "THE SPATIAL 3D TENSOR INNOVATION"
    p_vh.font.name = FONT_SERIF
    p_vh.font.size = Pt(12)
    p_vh.font.bold = True
    p_vh.font.color.rgb = GOLD

    p_veq = tf_v.add_paragraph()
    p_veq.text = "L_VAE = (0.7*||x - x_hat||_1 + 0.3*||x - x_hat||_2^2) + beta * D_KL( q_phi(z|x) || p(z) )"
    p_veq.font.name = "Consolas"
    p_veq.font.size = Pt(9.5)
    p_veq.font.bold = True
    p_veq.font.color.rgb = NAVY_DARK
    p_veq.space_before = Pt(4)

    add_bullet_point(tf_v, "Topology Preservation", "Rather than collapsing features into a flat 1D vector (destroying spatial adjacency), the encoder outputs mu, log(sigma^2) in R^(64x8x8).", font_size=9.5)
    add_bullet_point(tf_v, "Pareto Calibration (beta = 10^-4)", "Standard beta=1.0 collapses latent variance (posterior collapse, blurry edges). Calibrating beta=10^-4 achieves 27.49 dB PSNR with 60.72 nats KL divergence.", font_size=9.5)
    add_bullet_point(tf_v, "Unsupervised Anomaly Formulation", "Pixel-wise disparity map D(u, v) = (1/C) * sum_c | x(c, u, v) - x_hat_VAE(c, u, v) | highlights unpermitted architectural structures.", font_size=9.5)
    add_bullet_point(tf_v, "Statistical Decision Threshold", "Parcels exceeding S_anomaly > mu_base + 3*sigma_base are flagged as unpermitted municipal violations.", font_size=9.5)

    print("Building Slide 11: Stage 3: Frozen ResNet-18 Auditor...")
    # -------------------------------------------------------------------------
    # SLIDE 11: STAGE 3 (RESNET-18 AUDITOR)
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "MATHEMATICAL FORMULATIONS", "Stage 3: Frozen Territorial Classifier as Semantic Auditor", "Autonomous mathematical verification eliminating subjective human scoring in generative evaluation")
    add_footer(s11, 11)

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_c1 = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p_c1 = tf_c1.paragraphs[0]
    p_c1.text = "INDEPENDENT EVALUATION PROTOCOL"
    p_c1.font.name = FONT_SERIF
    p_c1.font.size = Pt(12)
    p_c1.font.bold = True
    p_c1.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_c1, "Why an Independent Auditor?", "Generative vision research frequently relies on subjective human user studies or unconstrained FID scores. UrbanGen AI employs an independent neural auditor.", font_size=10)
    add_bullet_point(tf_c1, "ImageNet Pretrained Transfer", "Adapts ResNet-18 with residual shortcut connections, mitigating vanishing gradients and accelerating convergence across 21 aerial categories.", font_size=10)
    add_bullet_point(tf_c1, "Loss Formulation", "Multi-class Cross-Entropy: L_CE = - sum_{c=1}^{21} y_c log(y_hat_c) optimized via Adam (lr=10^-4, weight_decay=10^-4).", font_size=10)
    add_bullet_point(tf_c1, "Audit Role 1: DAE Verification", "Audits whether DAE restored rasters retain correct territorial zoning semantics (recovering accuracy from 31% to 98%).", font_size=10)

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1))
    tb_c2 = s11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p_c2 = tf_c2.paragraphs[0]
    p_c2.text = "EMPIRICAL AUDITING METRICS"
    p_c2.font.name = FONT_SERIF
    p_c2.font.size = Pt(12)
    p_c2.font.bold = True
    p_c2.font.color.rgb = GOLD

    add_bullet_point(tf_c2, "Validation Performance", "Achieves 98.10% Top-1 validation accuracy and 0.9784 Macro F1 score across all 21 categories.", font_size=10)
    add_bullet_point(tf_c2, "Held-out Test Performance", "Maintains 87.30% Top-1 accuracy under severe synthetic perturbation (noise sigma=0.15).", font_size=10)
    add_bullet_point(tf_c2, "Edge Efficiency", "Inference requires only 5.1 ms per tile and 380 MB VRAM, allowing real-time batch auditing.", font_size=10)
    add_bullet_point(tf_c2, "Audit Role 2: Generative Verification", "Audits whether cDCGAN and DDPM synthesized parcels match their conditioned target classes without mode collapse.", font_size=10)

    print("Building Slide 12: Stage 4: Residual cDCGAN...")
    # -------------------------------------------------------------------------
    # SLIDE 12: STAGE 4 (RESIDUAL cDCGAN)
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "MATHEMATICAL FORMULATIONS", "Stage 4: Residual Class-Conditional DCGAN (cDCGAN)", "Ultra-fast 32 ms parcel generation with Spectral Normalization and Projection Conditioning")
    add_footer(s12, 12)

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tb_g1 = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_g1 = tb_g1.text_frame
    tf_g1.word_wrap = True
    p_g1 = tf_g1.paragraphs[0]
    p_g1.text = "GENERATOR & DISCRIMINATOR DESIGN"
    p_g1.font.name = FONT_SERIF
    p_g1.font.size = Pt(12)
    p_g1.font.bold = True
    p_g1.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_g1, "Conditioned Generator (8.82 M)", "Noise vector z in R^128 concatenated with class label y in R^21 -> 4 x Residual Upsampling Blocks with Conditional BatchNorm.", font_size=10)
    add_bullet_point(tf_g1, "Projection Discriminator (6.97 M)", "Employs an inner-product conditioning mechanism: D(x, y) = psi(phi(x)) + y^T * V * phi(x).", font_size=10)
    add_bullet_point(tf_g1, "Spectral Normalization (SN)", "Applied to all discriminator convolutional layers to enforce 1-Lipschitz continuity: || W ||_SN = sigma(W) = 1, stabilizing adversarial minimax training.", font_size=10)
    add_bullet_point(tf_g1, "Composite Objective", "L_G = L_adv + 0.8 * L_AC + 1.2 * L_semantic guarantees class compliance and semantic diversity.", font_size=10)

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_g2 = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_g2 = tb_g2.text_frame
    tf_g2.word_wrap = True
    p_g2 = tf_g2.paragraphs[0]
    p_g2.text = "OPERATIONAL EDGE PROFILE"
    p_g2.font.name = FONT_SERIF
    p_g2.font.size = Pt(12)
    p_g2.font.bold = True
    p_g2.font.color.rgb = GOLD

    add_bullet_point(tf_g2, "Champion Inference Speed", "Synthesizes complete 128x128 aerial parcels in just 32 ms (31 frames per second), serving as the ideal real-time tool for interactive scenario design.", font_size=10)
    add_bullet_point(tf_g2, "Semantic Proxy Recognition", "ResNet-18 auditor correctly classifies 99.40% of synthesized parcels into their conditioned classes (167 out of 168 audited tiles).", font_size=10)
    add_bullet_point(tf_g2, "Stable Minimax Convergence", "Maintains optimal game-theoretic equilibrium at epoch 50: D_loss = 1.67, G_loss = 1.19 without gradient collapse.", font_size=10)
    add_bullet_point(tf_g2, "Zero Mode Dropping", "Conditional BatchNorm across all four residual stages enforces intra-class structural diversity.", font_size=10)

    print("Building Slide 13: Stage 5: Conditional DDPM/DDIM...")
    # -------------------------------------------------------------------------
    # SLIDE 13: STAGE 5 (CONDITIONAL DDPM / DDIM)
    # -------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "MATHEMATICAL FORMULATIONS", "Stage 5: Photorealistic Diffusion Prototyping (DDPM / DDIM)", "Reversing stochastic Markovian noise trajectories accelerated via 20-step deterministic DDIM sampling")
    add_footer(s13, 13)

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_d1 = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    p_d1 = tf_d1.paragraphs[0]
    p_d1.text = "FORWARD & REVERSE DIFFUSION PROCESS"
    p_d1.font.name = FONT_SERIF
    p_d1.font.size = Pt(12)
    p_d1.font.bold = True
    p_d1.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_d1, "Forward Stochastic Noise Injection", "Gradually destroys image structure over T=1000 timesteps via Gaussian Markov chain: q(x_t | x_{t-1}) = N(x_t; sqrt(1-beta_t) x_{t-1}, beta_t I).", font_size=9.5)
    add_bullet_point(tf_d1, "Conditional Residual U-Net (2.80 M)", "Predicts injected noise epsilon_theta(x_t, t, c) conditioned on continuous sinusoidal time embeddings and class vector c.", font_size=9.5)
    add_bullet_point(tf_d1, "Denoising Score Matching Loss", "L_simple = E_{t, x_0, epsilon} [ || epsilon - epsilon_theta(x_t, t, c) ||_2^2 ]. Evaluated model achieves 0.0304 noise MSE.", font_size=9.5)
    add_bullet_point(tf_d1, "Superior Photorealism", "Diffusion models avoid the adversarial artifacts and mode drops inherent in GANs, yielding crisp textures for dense residential parcels.", font_size=9.5)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1))
    tb_d2 = s13.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True
    p_d2 = tf_d2.paragraphs[0]
    p_d2.text = "ACCELERATED 20-STEP DDIM SAMPLER"
    p_d2.font.name = FONT_SERIF
    p_d2.font.size = Pt(12)
    p_d2.font.bold = True
    p_d2.font.color.rgb = GOLD

    p_deq = tf_d2.add_paragraph()
    p_deq.text = "x_{t-1} = sqrt(alpha_bar_{t-1}) * [ (x_t - sqrt(1-alpha_bar_t) * epsilon_theta) / sqrt(alpha_bar_t) ] + sqrt(1-alpha_bar_{t-1}) * epsilon_theta"
    p_deq.font.name = "Consolas"
    p_deq.font.size = Pt(9)
    p_deq.font.bold = True
    p_deq.font.color.rgb = NAVY_DARK
    p_deq.space_before = Pt(4)

    add_bullet_point(tf_d2, "Non-Markovian Trajectory", "DDIM formulates deterministic sub-sequences sharing the same marginal distribution as DDPM, eliminating random noise injection during sampling.", font_size=9.5)
    add_bullet_point(tf_d2, "15.6x Inference Acceleration", "Reduces synthesis duration from 28.4 seconds (1,000 steps) to 1.82 seconds (20 steps) per tile.", font_size=9.5)
    add_bullet_point(tf_d2, "Edge Feasibility", "Operates entirely within 890 MB VRAM, achieving 98.60% semantic proxy fidelity without mode collapse.", font_size=9.5)

    print("Building Slide 14: Stage 6: MiniGPT Causal Transformer...")
    # -------------------------------------------------------------------------
    # SLIDE 14: STAGE 6 (MINIGPT CAUSAL TRANSFORMER)
    # -------------------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "MATHEMATICAL FORMULATIONS", "Stage 6: Causal Autoregressive Bylaw Formulation (MiniGPT)", "Translating visual zoning classifications into legally grounded Floor Space Index (FSI) directives")
    add_footer(s14, 14)

    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tb_m1 = s14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    p_m1 = tf_m1.paragraphs[0]
    p_m1.text = "CAUSAL LANGUAGE MODELING"
    p_m1.font.name = FONT_SERIF
    p_m1.font.size = Pt(12)
    p_m1.font.bold = True
    p_m1.font.color.rgb = GOLD

    add_bullet_point(tf_m1, "Transformer Architecture (3.23 M)", "4-layer Pre-LayerNorm Causal Transformer (d_model=256, 4 attention heads, T=192 context window).", font_size=10)
    add_bullet_point(tf_m1, "Domain-Curated Legal Corpus", "Trained on Pune Municipal Corporation (PMC) DCPR-2017 bylaws, Transit-Oriented Development circulars, and the Indian National Building Code (NBC).", font_size=10)
    add_bullet_point(tf_m1, "Cross-Entropy Training Objective", "L_causal = - sum_{t=1}^T log P(w_t | w_{<t}) achieves near-theoretical 1.110 perplexity (0.1505 bits/char).", font_size=10)
    add_bullet_point(tf_m1, "Zero Cloud Hallucination", "Unlike commercial LLMs which fabricate bylaws, domain-specialized MiniGPT operates strictly within municipal regulatory bounds.", font_size=10)

    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_m2 = s14.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    p_m2 = tf_m2.paragraphs[0]
    p_m2.text = "VISION-SEEDED ACTIONABLE DIRECTIVES"
    p_m2.font.name = FONT_SERIF
    p_m2.font.size = Pt(12)
    p_m2.font.bold = True
    p_m2.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_m2, "Vision Grounding", "Inference is guided via top-p nucleus sampling (p=0.9, tau=0.7) seeded directly with visual zoning classifications from ResNet-18.", font_size=10)
    add_bullet_point(tf_m2, "Floor Space Index (FSI) Directives", "Automatically calculates permissible FSI (1.8 to 2.4) based on parcel road width and residential density classifications.", font_size=10)
    add_bullet_point(tf_m2, "Transit-Oriented Development (TOD)", "Enforces 15% riverbank green-buffer setbacks and commercial transit corridor density bonuses.", font_size=10)
    add_bullet_point(tf_m2, "Rainwater & Solar Mandates", "Specifies mandatory on-site percolation tanks and rooftop solar arrays for commercial plots exceeding 1,000 m^2.", font_size=10)

    print("Building Slide 15: Benchmark Dataset & Setup...")
    # -------------------------------------------------------------------------
    # SLIDE 15: DATASET DESCRIPTION & PREPROCESSING
    # -------------------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "DATASET & EXPERIMENTAL SETUP", "USGS UCMerced LandUse Benchmark & Preprocessing", "2,100 high-resolution aerial orthoimages across 21 municipal land-use categories")
    add_footer(s15, 15)

    if os.path.exists(FIG_6_1):
        s15.shapes.add_picture(FIG_6_1, Inches(0.8), Inches(1.6), width=Inches(5.4))

    add_card(s15, Inches(6.5), Inches(1.6), Inches(6.033), Inches(5.1))
    tb_ds = s15.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.6), Inches(4.7))
    tf_ds = tb_ds.text_frame
    tf_ds.word_wrap = True
    p_dsh = tf_ds.paragraphs[0]
    p_dsh.text = "BENCHMARK SPECIFICATIONS"
    p_dsh.font.name = FONT_SERIF
    p_dsh.font.size = Pt(12)
    p_dsh.font.bold = True
    p_dsh.font.color.rgb = GOLD

    add_bullet_point(tf_ds, "USGS UCMerced LandUse Benchmark", "2,100 high-resolution aerial orthoimages (256x256 pixels, 0.3 m Ground Sample Distance) extracted from USGS National Map orthophotos.", font_size=10)
    add_bullet_point(tf_ds, "21 Municipal Land-Use Classes", "Agricultural, airplane, baseball diamond, beach, buildings, chaparral, dense residential, forest, freeway, golf course, harbor, intersection, medium residential, mobile home park, overpass, parking lot, river, runway, sparse residential, storage tanks, tennis court.", font_size=9.5)
    add_bullet_point(tf_ds, "Stratified Split Protocol", "Strict 90/10 train/validation split (1,890 training tiles, 210 validation tiles) held constant across all six models for absolute experimental fairness.", font_size=10)
    add_bullet_point(tf_ds, "Synthetic Atmospheric Perturbation", "Tiles normalized to [-1, 1] and corrupted with additive Gaussian noise (sigma = 0.15) to emulate severe orbital haze and atmospheric aerosol scattering.", font_size=10)

    print("Building Slide 16: Results — Case 1: Optical Restoration...")
    # -------------------------------------------------------------------------
    # SLIDE 16: CASE STUDY 1: RESTORATION BENCHMARK
    # -------------------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "EXPERIMENTAL EVALUATION", "Case 1: Optical Remote Sensing Restoration Benchmark", "Skip-connected U-Net DAE delivers +7.0 dB PSNR gain over corrupted baseline at 119 FPS")
    add_footer(s16, 16)

    # Embed Figure 6.2 (DAE Crisp Restoration Grid)
    if os.path.exists(FIG_6_2):
        s16.shapes.add_picture(FIG_6_2, Inches(0.8), Inches(1.6), width=Inches(4.4))

    # Table 7.1 Comparison
    t_c1_cols = [Inches(2.5), Inches(1.0), Inches(1.2), Inches(1.1), Inches(1.2)]
    t_c1_h = ["Method", "Params", "PSNR (dB)", "SSIM", "Latency"]
    t_c1_r = [
        ["Degraded Baseline", "---", "12.04", "0.3412", "---"],
        ["Bottleneck AE", "2.1 M", "25.02", "0.7210", "6.2 ms"],
        ["DnCNN [17]", "0.56 M", "27.84", "0.8120", "14.8 ms"],
        ["RIDNet [21]", "1.49 M", "28.62", "0.8390", "28.5 ms"],
        ["SwinIR [19]", "11.8 M", "29.82", "0.8710", "142.0 ms"],
        ["UrbanGen DAE (Ours)", "2.45 M", "29.65", "0.8649", "8.4 ms"]
    ]
    add_table(s16, Inches(5.4), Inches(1.6), Inches(7.133), Inches(3.2), t_c1_h, t_c1_r, t_c1_cols)

    # Embed PSNR Chart
    if os.path.exists(FIG_7_2):
        s16.shapes.add_picture(FIG_7_2, Inches(5.4), Inches(5.0), width=Inches(7.133))

    print("Building Slide 17: Results — Case 2: Territorial Zoning...")
    # -------------------------------------------------------------------------
    # SLIDE 17: CASE STUDY 2: CLASSIFICATION AUDITOR
    # -------------------------------------------------------------------------
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "EXPERIMENTAL EVALUATION", "Case 2: Territorial Zoning Classification Accuracy", "Frozen ResNet-18 achieves 98.10% accuracy and 0.9784 Macro F1 score on 21 land-use categories")
    add_footer(s17, 17)

    # Embed Classifier Metrics Chart
    if os.path.exists(FIG_7_3):
        s17.shapes.add_picture(FIG_7_3, Inches(0.8), Inches(1.6), width=Inches(5.6))

    # Table 7.2
    t_c2_cols = [Inches(2.5), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.0)]
    t_c2_h = ["Model", "Params", "Top-1 Acc", "Macro F1", "Latency"]
    t_c2_r = [
        ["BoVW [13]", "---", "76.80%", "0.7410", "320 ms"],
        ["VGG-16", "138.4 M", "94.20%", "0.9380", "22.4 ms"],
        ["MobileNetV3", "5.4 M", "96.40%", "0.9590", "4.2 ms"],
        ["DenseNet-121", "8.0 M", "97.60%", "0.9710", "9.8 ms"],
        ["ResNet-50", "25.6 M", "98.30%", "0.9800", "11.5 ms"],
        ["ResNet-18 (Ours)", "11.19 M", "98.10%", "0.9784", "5.1 ms"]
    ]
    add_table(s17, Inches(6.6), Inches(1.6), Inches(5.933), Inches(3.2), t_c2_h, t_c2_r, t_c2_cols)

    # Bottom Takeaway Card
    add_card(s17, Inches(6.6), Inches(5.0), Inches(5.933), Inches(1.7), bg_rgb=RGBColor(241, 245, 249))
    tb_c2t = s17.shapes.add_textbox(Inches(6.8), Inches(5.1), Inches(5.5), Inches(1.5))
    tf_c2t = tb_c2t.text_frame
    p_c2h = tf_c2t.paragraphs[0]
    p_c2h.text = "KEY AUDITOR FINDINGS"
    p_c2h.font.name = FONT_SERIF
    p_c2h.font.size = Pt(11)
    p_c2h.font.bold = True
    p_c2h.font.color.rgb = NAVY_ACCENT
    p_c2b = tf_c2t.add_paragraph()
    p_c2b.text = "ResNet-18 achieves virtually identical accuracy to ResNet-50 (98.10% vs 98.30%) with less than half the parameters (11.19M vs 25.6M) and half the latency (5.1 ms vs 11.5 ms). In auditing mode, it proves that DAE restoration successfully recovers zoning class semantics from 31% to 98%."
    p_c2b.font.name = FONT_SANS
    p_c2b.font.size = Pt(9.5)
    p_c2b.font.color.rgb = TEXT_DARK
    p_c2b.space_before = Pt(3)

    print("Building Slide 18: Results — Case 3: Generative Parcel Synthesis...")
    # -------------------------------------------------------------------------
    # SLIDE 18: CASE STUDY 3: GENERATIVE PARCEL SYNTHESIS
    # -------------------------------------------------------------------------
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "EXPERIMENTAL EVALUATION", "Case 3: Generative Synthesis: cDCGAN vs. DDPM Diffusion", "Residual cDCGAN achieves champion speed (32 ms); Accelerated DDIM achieves champion photorealism")
    add_footer(s18, 18)

    # Embed Figure 6.3 (GAN Diverse Generation Grid)
    if os.path.exists(FIG_6_3):
        s18.shapes.add_picture(FIG_6_3, Inches(0.8), Inches(1.6), width=Inches(5.6))

    # Table 7.3
    t_c3_cols = [Inches(2.1), Inches(1.3), Inches(1.1), Inches(1.2), Inches(1.1)]
    t_c3_h = ["Architecture", "Sampling", "Semantic Proxy", "Latency", "Edge Status"]
    t_c3_r = [
        ["Vanilla DCGAN [29]", "1-Step Direct", "68.20%", "24 ms", "Severe Mode Drop"],
        ["cGAN (Mirza) [30]", "1-Step Direct", "72.40%", "26 ms", "Edge Real-Time"],
        ["WGAN-GP [34]", "1-Step Direct", "81.50%", "28 ms", "Edge Real-Time"],
        ["StyleGAN2-ADA [35]", "1-Step Direct", "91.20%", "68 ms", "High VRAM (4.8GB)"],
        ["Standard DDPM [37]", "1000 Ancestral", "96.80%", "28.4 s", "Impractical at Edge"],
        ["cDCGAN (Ours)", "1-Step Residual", "99.40%", "32 ms", "Champion Speed"],
        ["DDPM (Ours)", "20-Step DDIM", "98.60%", "1.82 s", "Champion Fidelity"]
    ]
    add_table(s18, Inches(6.6), Inches(1.6), Inches(5.933), Inches(3.6), t_c3_h, t_c3_r, t_c3_cols)

    # Explanation Card below Table
    add_card(s18, Inches(6.6), Inches(5.35), Inches(5.933), Inches(1.35), bg_rgb=RGBColor(241, 245, 249))
    tb_gex = s18.shapes.add_textbox(Inches(6.8), Inches(5.45), Inches(5.5), Inches(1.15))
    tf_gex = tb_gex.text_frame
    p_gex = tf_gex.paragraphs[0]
    p_gex.text = "OPERATIONAL COMPLEMENTARITY"
    p_gex.font.name = FONT_SERIF
    p_gex.font.size = Pt(11)
    p_gex.font.bold = True
    p_gex.font.color.rgb = GOLD
    p_geb = tf_gex.add_paragraph()
    p_geb.text = "Rather than forcing an either/or choice, UrbanGen AI offers dual operational frontiers: cDCGAN provides 32 ms real-time interactive prototyping (56x faster than diffusion), while 20-step DDIM diffusion provides photorealistic final renders with zero mode collapse."
    p_geb.font.name = FONT_SANS
    p_geb.font.size = Pt(9.5)
    p_geb.font.color.rgb = TEXT_DARK
    p_geb.space_before = Pt(2)

    print("Building Slide 19: Latent Space Exploration — Spatial Morphing...")
    # -------------------------------------------------------------------------
    # SLIDE 19: SPATIAL MANIFOLD MORPHING
    # -------------------------------------------------------------------------
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "LATENT SPACE EXPLORATION", "Continuous Latent Manifold Morphing & Interpolation", "Smooth topological deformations across complex municipal land-use archetypes via Spatial beta-VAE")
    add_footer(s19, 19)

    # Embed Figure 6.4 (VAE Multi Interpolation)
    if os.path.exists(FIG_6_4):
        s19.shapes.add_picture(FIG_6_4, Inches(0.8), Inches(1.6), width=Inches(11.733))

    add_card(s19, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.35), bg_rgb=RGBColor(241, 245, 249))
    tb_vi = s19.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.15))
    tf_vi = tb_vi.text_frame
    p_vih = tf_vi.paragraphs[0]
    p_vih.text = "CONTINUOUS GEOSPATIAL INTERPOLATION TRAJECTORIES"
    p_vih.font.name = FONT_SERIF
    p_vih.font.size = Pt(11)
    p_vih.font.bold = True
    p_vih.font.color.rgb = NAVY_ACCENT
    p_vib = tf_vi.add_paragraph()
    p_vib.text = "Trajectory 1 (Top): Agricultural Field -> Dense Commercial Buildings (simulating industrial zoning expansion). Trajectory 2 (Middle): Golf Course Green Cover -> Coastal Harbor Marina. Trajectory 3 (Bottom): Sandy Beach -> Multilane Freeway Corridor. Retaining the 3D tensor R^(64x8x8) ensures smooth topological blending without semantic tearing or posterior collapse."
    p_vib.font.name = FONT_SANS
    p_vib.font.size = Pt(9.5)
    p_vib.font.color.rgb = TEXT_DARK
    p_vib.space_before = Pt(2)

    print("Building Slide 20: Training Loss Dynamics & Convergence...")
    # -------------------------------------------------------------------------
    # SLIDE 20: TRAINING DYNAMICS & CONVERGENCE
    # -------------------------------------------------------------------------
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "MODEL CONVERGENCE", "Training Loss Dynamics & Equilibrium Verification", "Empirical proof of numerical stability across reconstruction, adversarial minimax, and diffusion trajectories")
    add_footer(s20, 20)

    # 3 Charts across
    if os.path.exists(FIG_7_1):
        s20.shapes.add_picture(FIG_7_1, Inches(0.8), Inches(1.6), width=Inches(3.7))
    if os.path.exists(FIG_7_4):
        s20.shapes.add_picture(FIG_7_4, Inches(4.8), Inches(1.6), width=Inches(3.7))
    if os.path.exists(FIG_7_5):
        s20.shapes.add_picture(FIG_7_5, Inches(8.8), Inches(1.6), width=Inches(3.7))

    # Explanatory Card below
    add_card(s20, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.35))
    tb_td = s20.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.15))
    tf_td = tb_td.text_frame
    p_tdh = tf_td.paragraphs[0]
    p_tdh.text = "CONVERGENCE VERIFICATION"
    p_tdh.font.name = FONT_SERIF
    p_tdh.font.size = Pt(11)
    p_tdh.font.bold = True
    p_tdh.font.color.rgb = GOLD
    p_tdb = tf_td.add_paragraph()
    p_tdb.text = "Left: U-Net DAE converges monotonically within 15 epochs, demonstrating stable MSE reduction without filter overfitting. Center: Residual cDCGAN maintains stable minimax equilibrium (D_loss = 1.67, G_loss = 1.19) prevented from exploding or vanishing by Spectral Normalization. Right: Conditional DDPM exhibits smooth reverse denoising score matching MSE decay, stabilizing at 0.0304."
    p_tdb.font.name = FONT_SANS
    p_tdb.font.size = Pt(9.5)
    p_tdb.font.color.rgb = TEXT_DARK
    p_tdb.space_before = Pt(2)

    print("Building Slide 21: Green AI Hardware & Carbon Audit...")
    # -------------------------------------------------------------------------
    # SLIDE 21: GREEN AI & HARDWARE ENERGY AUDIT
    # -------------------------------------------------------------------------
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "GREEN AI AUDIT", "Hardware Feasibility & Computational Carbon Footprint", "In strict adherence to Green AI principles: 100% trained on consumer edge hardware")
    add_footer(s21, 21)

    # Embed Figure 7.7 (Energy Carbon Breakdown)
    if os.path.exists(FIG_7_7):
        s21.shapes.add_picture(FIG_7_7, Inches(0.8), Inches(1.6), width=Inches(5.4))

    # Table 7.5
    t_n_cols = [Inches(2.5), Inches(0.9), Inches(0.9), Inches(1.0), Inches(0.9)]
    t_n_h = ["Model Pipeline", "Time (m)", "Power (W)", "Energy", "CO2e (g)"]
    t_n_r = [
        ["U-Net Denoising AE", "15.2", "118", "0.030 kWh", "21.2 g"],
        ["Spatial beta-VAE", "6.7", "118", "0.013 kWh", "9.2 g"],
        ["ResNet-18 Land-Use", "14.2", "123", "0.029 kWh", "20.5 g"],
        ["Residual cDCGAN", "15.0", "120", "0.030 kWh", "21.2 g"],
        ["Conditional DDPM", "16.6", "28.5 (avg)", "0.008 kWh", "5.6 g"],
        ["MiniGPT Transformer", "1.2", "108", "0.002 kWh", "1.4 g"],
        ["Total Integrated Suite", "68.9 min", "103 W avg", "0.112 kWh", "79.1 g"]
    ]
    add_table(s21, Inches(6.4), Inches(1.6), Inches(6.133), Inches(3.6), t_n_h, t_n_r, t_n_cols)

    # Green AI Callout Card
    add_card(s21, Inches(6.4), Inches(5.35), Inches(6.133), Inches(1.35), bg_rgb=RGBColor(241, 245, 249))
    tb_nrg = s21.shapes.add_textbox(Inches(6.6), Inches(5.45), Inches(5.7), Inches(1.15))
    tf_nrg = tb_nrg.text_frame
    p_nh = tf_nrg.paragraphs[0]
    p_nh.text = "HARDWARE PLATFORM & EMISSION AUDIT"
    p_nh.font.name = FONT_SERIF
    p_nh.font.size = Pt(11)
    p_nh.font.bold = True
    p_nh.font.color.rgb = EMERALD
    p_nb = tf_nrg.add_paragraph()
    p_nb.text = "NVIDIA RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP). Real-time telemetry polled via PyNVML at 500 ms. Total carbon emitted (79.1 g CO2e) is equivalent to driving an average petrol car for less than 400 meters, proving state-of-the-art municipal AI can operate sustainably."
    p_nb.font.name = FONT_SANS
    p_nb.font.size = Pt(9.5)
    p_nb.font.color.rgb = TEXT_DARK
    p_nb.space_before = Pt(2)

    print("Building Slide 22: Consolidated Multi-Model Evaluation Matrix...")
    # -------------------------------------------------------------------------
    # SLIDE 22: CONSOLIDATED MULTI-MODEL MATRIX
    # -------------------------------------------------------------------------
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "PERFORMANCE VERIFICATION", "Consolidated Multi-Model Evaluation Parameter Matrix", "Standardized quantitative verification metrics across all six specialized architectures")
    add_footer(s22, 22)

    # Embed Figure 7.6 (Multi-Model Loss Bars)
    if os.path.exists(FIG_7_6):
        s22.shapes.add_picture(FIG_7_6, Inches(0.8), Inches(1.6), width=Inches(5.0))

    # Table 7.4
    t_ev_cols = [Inches(1.8), Inches(1.3), Inches(1.1), Inches(1.3), Inches(1.1)]
    t_ev_h = ["Model Pipeline", "Primary Metric", "Value", "Secondary Metric", "Value"]
    t_ev_r = [
        ["Denoising U-Net AE", "PSNR", "29.65 dB", "SSIM", "0.8649"],
        ["Spatial beta-VAE", "Recon PSNR", "27.49 dB", "KL Divergence", "60.72 nats"],
        ["ResNet-18 Classifier", "Top-1 Accuracy", "98.10%", "Macro F1", "0.9784"],
        ["Residual cDCGAN", "Proxy Recognition", "99.40%", "Minimax Score", "D=1.67, G=1.19"],
        ["Conditional DDPM", "Noise MSE", "0.0304", "DDIM Speed", "20 Steps (1.82 s)"],
        ["MiniGPT Transformer", "Perplexity", "1.110", "Bits Per Char", "0.1505"]
    ]
    add_table(s22, Inches(6.0), Inches(1.6), Inches(6.533), Inches(3.4), t_ev_h, t_ev_r, t_ev_cols)

    # Summary Card
    add_card(s22, Inches(6.0), Inches(5.2), Inches(6.533), Inches(1.5), bg_rgb=RGBColor(241, 245, 249))
    tb_msm = s22.shapes.add_textbox(Inches(6.2), Inches(5.3), Inches(6.1), Inches(1.3))
    tf_msm = tb_msm.text_frame
    p_mh = tf_msm.paragraphs[0]
    p_mh.text = "RESEARCH QUESTIONS RESOLVED"
    p_mh.font.name = FONT_SERIF
    p_mh.font.size = Pt(11)
    p_mh.font.bold = True
    p_mh.font.color.rgb = GOLD
    p_mb = tf_msm.add_paragraph()
    p_mb.text = "RQ1 (Restoration): Multi-scale skips resolve bottleneck smearing (+7.0 dB gain). RQ2 (Topology): 3D spatial latents preserve geospatial adjacency and power >3 sigma anomaly detection. RQ3 (Synthesis): cDCGAN and DDIM establish the optimal speed-fidelity Pareto frontier. RQ4 (Bylaws): Causal domain curation eliminates legal hallucination (1.110 PPL)."
    p_mb.font.name = FONT_SANS
    p_mb.font.size = Pt(9.5)
    p_mb.font.color.rgb = TEXT_DARK
    p_mb.space_before = Pt(2)

    print("Building Slide 23: Cybersecurity & Data Sovereignty...")
    # -------------------------------------------------------------------------
    # SLIDE 23: CYBERSECURITY & DATA SOVEREIGNTY
    # -------------------------------------------------------------------------
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "SECURITY & GOVERNANCE", "System Cybersecurity, Data Sovereignty & Closed-Loop Governance", "Guaranteeing air-gapped protection of municipal cadastral records and responsible AI decision support")
    add_footer(s23, 23)

    gov_cards = [
        ("Air-Gapped Edge Hardware & Data Sovereignty",
         "100% On-Premises Execution: All inference, training, and database storage execute on local edge infrastructure. Complete Data Sovereignty: Prevents sensitive cadastral vectors, property ownership records, and internal civic survey data from leaking to third-party public cloud endpoints.",
         RGBColor(241, 245, 249)),
        ("Guarded API Gateway & File Sanitization",
         "Header Injection Protection: Strict API token headers required for internal REST calls. SlowAPI Token-Bucket Rate Limiting: Prevents buffer saturation and Denial-of-Service attacks. Magic-Byte Inspection: Strictly validates image headers (<10 MB) to block malicious payload injections.",
         WHITE),
        ("Closed-Loop Human-in-the-Loop Governance",
         "Advisory Decision Support: UrbanGen AI serves strictly as an assistive drafting tool for licensed town planners. Autonomous Penalties Prohibited: Automated building demolition or zoning fines are restricted by design. Uncertainty Flagging: Out-of-distribution rasters flag high disparity alerts.",
         RGBColor(241, 245, 249))
    ]
    for idx, (title, desc, bg) in enumerate(gov_cards):
        c_left = Inches(0.8) + idx * Inches(3.95)
        add_card(s23, c_left, Inches(1.6), Inches(3.75), Inches(5.1), bg_rgb=bg)
        tb_g = s23.shapes.add_textbox(c_left + Inches(0.2), Inches(1.8), Inches(3.35), Inches(4.7))
        tf_g = tb_g.text_frame
        tf_g.word_wrap = True
        p_gh = tf_g.paragraphs[0]
        p_gh.text = title
        p_gh.font.name = FONT_SERIF
        p_gh.font.size = Pt(13)
        p_gh.font.bold = True
        p_gh.font.color.rgb = NAVY_ACCENT
        p_gd = tf_g.add_paragraph()
        p_gd.text = desc
        p_gd.font.name = FONT_SANS
        p_gd.font.size = Pt(10)
        p_gd.font.color.rgb = TEXT_DARK
        p_gd.space_before = Pt(8)
        p_gd.line_spacing = 1.25

    print("Building Slide 24: Interactive Planner Dashboard...")
    # -------------------------------------------------------------------------
    # SLIDE 24: USER INTERFACE & LIVE DEMO WALKTHROUGH
    # -------------------------------------------------------------------------
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "SYSTEM DEMONSTRATION", "Interactive Town Planner Web Dashboard (Live UI Walkthrough)", "Four integrated operational views built with React 18, Vite, and Tailwind CSS")
    add_footer(s24, 24)

    ui_cards = [
        ("View 1: Optical Restoration Dropzone", 
         "Planners upload degraded aerial rasters. Side-by-side interactive curtain slider provides instantaneous visual comparison between corrupted input, DAE restored output, and ground truth, displaying live PSNR and SSIM fidelity readouts in 8.4 ms."),
        ("View 2: Spatial Latent Manifold Explorer", 
         "Continuous alpha-blending slider navigates the topology-preserving 3D latent space, enabling smooth archetype transitions. An unsupervised disparity overlay highlights structural encroachment anomalies exceeding 3 sigma."),
        ("View 3: Dual-Modality Scenario Generator", 
         "Provides one-click switching between real-time 32 ms cDCGAN prototyping for rapid exploratory meetings and 1.82 s 20-step DDIM reverse diffusion for photorealistic digital twin presentation graphics."),
        ("View 4: Municipal Bylaw Policy Terminal", 
         "Translates visual zoning classifications and parcel metrics into legally compliant Floor Space Index (FSI 1.8 to 2.4), Transit-Oriented Development (TOD) setbacks, and mandatory percolation directives in real time.")
    ]
    for idx, (title, desc) in enumerate(ui_cards):
        r_i = idx // 2
        c_i = idx % 2
        c_left = Inches(0.8) + c_i * Inches(5.95)
        c_top = Inches(1.6) + r_i * Inches(2.6)
        add_card(s24, c_left, c_top, Inches(5.75), Inches(2.4))
        tb_u = s24.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.2), Inches(5.35), Inches(2.0))
        tf_u = tb_u.text_frame
        tf_u.word_wrap = True
        p_uh = tf_u.paragraphs[0]
        p_uh.text = title
        p_uh.font.name = FONT_SERIF
        p_uh.font.size = Pt(13)
        p_uh.font.bold = True
        p_uh.font.color.rgb = GOLD
        p_ub = tf_u.add_paragraph()
        p_ub.text = desc
        p_ub.font.name = FONT_SANS
        p_ub.font.size = Pt(10)
        p_ub.font.color.rgb = TEXT_DARK
        p_ub.space_before = Pt(6)
        p_ub.line_spacing = 1.2

    print("Building Slide 25: Academic Authenticity & Plagiarism...")
    # -------------------------------------------------------------------------
    # SLIDE 25: PLAGIARISM & AUTHENTICITY VERIFICATION
    # -------------------------------------------------------------------------
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "ACADEMIC INTEGRITY", "Originality & Plagiarism Authenticity Verification", "Verified through Turnitin plagiarism detection under MIT Academy of Engineering guidelines")
    add_footer(s25, 25)

    if os.path.exists(FIG_A_1):
        s25.shapes.add_picture(FIG_A_1, Inches(0.8), Inches(1.6), width=Inches(6.4))

    add_card(s25, Inches(7.4), Inches(1.6), Inches(5.133), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_pl = s25.shapes.add_textbox(Inches(7.6), Inches(1.8), Inches(4.7), Inches(4.7))
    tf_pl = tb_pl.text_frame
    tf_pl.word_wrap = True
    p_plh = tf_pl.paragraphs[0]
    p_plh.text = "ACADEMIC AUTHENTICITY STATEMENT"
    p_plh.font.name = FONT_SERIF
    p_plh.font.size = Pt(12)
    p_plh.font.bold = True
    p_plh.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_pl, "Institutional Compliance", "In strict accordance with Savitribai Phule Pune University (SPPU) and MIT AOE guidelines, the manuscript and mathematical formulations were audited using Turnitin.", font_size=10)
    add_bullet_point(tf_pl, "Similarity Index Threshold", "Recorded similarity index is strictly below institutional tolerance thresholds, confirming the originality of all architectural and empirical findings.", font_size=10)
    add_bullet_point(tf_pl, "Authentic Research Execution", "All six neural network architectures were developed, trained, and benchmarked directly by the student team on departmental workstations.", font_size=10)
    add_bullet_point(tf_pl, "Peer-Reviewed Citations", "All prior work from IEEE, CVPR, and ACM is formally cited in the bibliography ([1] through [45]).", font_size=10)

    print("Building Slide 26: Defense Viva Questions & Answers (Part 1)...")
    # -------------------------------------------------------------------------
    # SLIDE 26: EXAMINER Q&A (PART 1)
    # -------------------------------------------------------------------------
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "VIVA VOCE PREPARATION", "Anticipated Examiner Defense Questions & Answers (Part 1)", "Addressing key architectural and mathematical decisions")
    add_footer(s26, 26)

    add_card(s26, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.4))
    tb_q1 = s26.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(2.1))
    tf_q1 = tb_q1.text_frame
    tf_q1.word_wrap = True
    p_q1h = tf_q1.paragraphs[0]
    p_q1h.text = "Q1: Why deploy six specialized deep learning models instead of fine-tuning a single monolithic foundation model (e.g., CLIP, SAM, or GPT-4V)?"
    p_q1h.font.name = FONT_SERIF
    p_q1h.font.size = Pt(12)
    p_q1h.font.bold = True
    p_q1h.font.color.rgb = NAVY_ACCENT
    p_q1a = tf_q1.add_paragraph()
    p_q1a.text = "Answer: Monolithic vision-language models fail in edge municipal planning due to three critical bottlenecks: (1) Extreme VRAM Footprint: Foundation models require 24GB-80GB datacenter GPUs (A100/H100), exceeding municipal hardware budgets. UrbanGen AI's modular suite fits comfortably in 6 GB VRAM. (2) Modular Auditability: By decoupling restoration (DAE), anomaly detection (VAE), auditing (ResNet-18), and generation (cDCGAN/DDPM), each stage is mathematically inspectable and verifiable by civil engineers. (3) Data Sovereignty: Fine-tuning commercial APIs leaks proprietary municipal cadastral boundaries to third-party clouds."
    p_q1a.font.name = FONT_SANS
    p_q1a.font.size = Pt(9.5)
    p_q1a.font.color.rgb = TEXT_DARK
    p_q1a.space_before = Pt(4)

    add_card(s26, Inches(0.8), Inches(4.25), Inches(11.733), Inches(2.5), bg_rgb=RGBColor(241, 245, 249))
    tb_q2 = s26.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(11.3), Inches(2.2))
    tf_q2 = tb_q2.text_frame
    tf_q2.word_wrap = True
    p_q2h = tf_q2.paragraphs[0]
    p_q2h.text = "Q2: Why preserve an explicit 3D tensor latent R^(64x8x8) in Spatial beta-VAE rather than the standard 1D vector R^d?"
    p_q2h.font.name = FONT_SERIF
    p_q2h.font.size = Pt(12)
    p_q2h.font.bold = True
    p_q2h.font.color.rgb = GOLD
    p_q2a = tf_q2.add_paragraph()
    p_q2a.text = "Answer: Standard VAEs flatten convolutional features into a 1D vector (e.g., z in R^128), which irreversibly destroys spatial adjacency and geospatial topology. In aerial remote sensing, neighboring parcels and road connectivity are fundamentally 2D topological phenomena. By retaining an explicit 3D distribution tensor mu, log(sigma^2) in R^(64x8x8), spatial coordinate relationships are preserved throughout reparameterization. This enables: (1) smooth topological manifold morphing without semantic tearing, and (2) pixel-aligned reconstruction disparity maps D(u, v) for precise municipal encroachment anomaly localization."
    p_q2a.font.name = FONT_SANS
    p_q2a.font.size = Pt(9.5)
    p_q2a.font.color.rgb = TEXT_DARK
    p_q2a.space_before = Pt(4)

    print("Building Slide 27: Defense Viva Questions & Answers (Part 2)...")
    # -------------------------------------------------------------------------
    # SLIDE 27: EXAMINER Q&A (PART 2)
    # -------------------------------------------------------------------------
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "VIVA VOCE PREPARATION", "Anticipated Examiner Defense Questions & Answers (Part 2)", "Addressing generative synthesis trade-offs and language model hallucination")
    add_footer(s27, 27)

    add_card(s27, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.4), bg_rgb=RGBColor(241, 245, 249))
    tb_q3 = s27.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(2.1))
    tf_q3 = tb_q3.text_frame
    tf_q3.word_wrap = True
    p_q3h = tf_q3.paragraphs[0]
    p_q3h.text = "Q3: Why provide both cDCGAN and DDPM? Isn't diffusion strictly superior to generative adversarial networks?"
    p_q3h.font.name = FONT_SERIF
    p_q3h.font.size = Pt(12)
    p_q3h.font.bold = True
    p_q3h.font.color.rgb = NAVY_ACCENT
    p_q3a = tf_q3.add_paragraph()
    p_q3a.text = "Answer: While diffusion models achieve higher structural sharpness and avoid mode collapse, they suffer from substantial inference latency (1.82 s even with 20-step DDIM acceleration, and 28.4 s with 1,000 steps). In a live town planning session, planners require instant feedback as they manipulate zoning sliders. Residual cDCGAN generates parcels in 32 ms (31 FPS) with 99.40% proxy fidelity, enabling fluid interactive exploration. Once an exploratory layout is chosen, the DDIM diffusion model generates the publication-grade photorealistic parcel (0.0304 MSE), establishing operational complementarity."
    p_q3a.font.name = FONT_SANS
    p_q3a.font.size = Pt(9.5)
    p_q3a.font.color.rgb = TEXT_DARK
    p_q3a.space_before = Pt(4)

    add_card(s27, Inches(0.8), Inches(4.25), Inches(11.733), Inches(2.5))
    tb_q4 = s27.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(11.3), Inches(2.2))
    tf_q4 = tb_q4.text_frame
    tf_q4.word_wrap = True
    p_q4h = tf_q4.paragraphs[0]
    p_q4h.text = "Q4: How do you mathematically guarantee that MiniGPT does not hallucinate arbitrary or illegal zoning bylaws?"
    p_q4h.font.name = FONT_SERIF
    p_q4h.font.size = Pt(12)
    p_q4h.font.bold = True
    p_q4h.font.color.rgb = GOLD
    p_q4a = tf_q4.add_paragraph()
    p_q4a.text = "Answer: General-purpose LLMs hallucinate because they are trained on uncurated internet text and rely on stochastic generation. MiniGPT eliminates hallucination through three architectural constraints: (1) Highly Curated Domain Corpus: The training corpus is restricted exclusively to Pune Municipal Corporation (PMC DCPR-2017) bylaws, TOD circulars, and the NBC. (2) Near-Theoretical Perplexity: MiniGPT achieves 1.110 perplexity (0.1505 bits/character), confirming near-exact memorization of legal clauses. (3) Deterministic Visual Seeding: Autoregressive decoding is seeded directly with discrete class tokens from the audited vision models."
    p_q4a.font.name = FONT_SANS
    p_q4a.font.size = Pt(9.5)
    p_q4a.font.color.rgb = TEXT_DARK
    p_q4a.space_before = Pt(4)

    print("Building Slide 28: Conclusion & Future Scope...")
    # -------------------------------------------------------------------------
    # SLIDE 28: CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------------------
    s28 = prs.slides.add_slide(blank_layout)
    add_header(s28, "CONCLUSION & OUTLOOK", "Scientific Contributions & Future Research Directions", "Empirical proof of edge-computable, low-carbon municipal generative intelligence")
    add_footer(s28, 28)

    add_card(s28, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1), bg_rgb=RGBColor(241, 245, 249))
    tb_c1 = s28.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p_c1h = tf_c1.paragraphs[0]
    p_c1h.text = "KEY SCIENTIFIC CONTRIBUTIONS"
    p_c1h.font.name = FONT_SERIF
    p_c1h.font.size = Pt(12)
    p_c1h.font.bold = True
    p_c1h.font.color.rgb = NAVY_ACCENT

    add_bullet_point(tf_c1, "Skip-Connected Restoration", "U-Net DAE eliminates atmospheric aerosol scattering (+7.0 dB gain, 29.65 dB PSNR, SSIM 0.8649) in 8.4 ms.", font_size=9.5)
    add_bullet_point(tf_c1, "3D Latent Manifold & Anomaly", "Spatial beta-VAE preserves 2D topology in R^(64x8x8), enabling continuous morphing and unsupervised >3 sigma encroachment detection.", font_size=9.5)
    add_bullet_point(tf_c1, "Autonomous Semantic Auditor", "Frozen ResNet-18 achieves 98.10% accuracy, providing objective verification without human bias.", font_size=9.5)
    add_bullet_point(tf_c1, "Dual Generative Frontiers", "cDCGAN achieves 32 ms real-time speed (99.40% proxy acc); 20-step DDIM diffusion achieves 0.0304 MSE photorealism.", font_size=9.5)
    add_bullet_point(tf_c1, "Vision-Grounded Bylaws", "MiniGPT achieves 1.110 perplexity, synthesizing legally compliant FSI and TOD directives.", font_size=9.5)
    add_bullet_point(tf_c1, "Green AI Certified", "Trains in 68.9 minutes, consuming 0.112 kWh (79.1 g CO2e) on consumer edge hardware while preserving 100% data sovereignty.", font_size=9.5)

    add_card(s28, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1))
    tb_c2 = s28.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p_c2h = tf_c2.paragraphs[0]
    p_c2h.text = "FUTURE RESEARCH DIRECTIONS"
    p_c2h.font.name = FONT_SERIF
    p_c2h.font.size = Pt(12)
    p_c2h.font.bold = True
    p_c2h.font.color.rgb = GOLD

    add_bullet_point(tf_c2, "1. Multi-Spectral Satellite Ingestion", "Expanding from 3-band RGB to 12-band ESA Sentinel-2 and NASA Landsat surface reflectance streams, incorporating NDVI and thermal bands for urban heat island mitigation.", font_size=10)
    add_bullet_point(tf_c2, "2. Cross-Modal Vision-Language Diffusion", "Implementing cross-attention conditioning in the diffusion backbone to enable planners to guide scenario generation interactively via joint natural language prompts and cadastral GIS shapefiles.", font_size=10)
    add_bullet_point(tf_c2, "3. Physics-Informed Microclimate Modeling", "Integrating Physics-Informed Neural Networks (PINNs) and CFD surrogates to evaluate urban wind corridors and localized thermal dissipation across synthesized structural layouts.", font_size=10)

    # Thank you footer inside card
    p_ty = tf_c2.add_paragraph()
    p_ty.text = "\nThank you! We welcome questions from the External Examiner."
    p_ty.font.name = FONT_SERIF
    p_ty.font.size = Pt(11)
    p_ty.font.bold = True
    p_ty.font.italic = True
    p_ty.font.color.rgb = NAVY_DARK

    prs.save(PPTX_PATH)
    print(f"SUCCESS: Generated 28-slide presentation at: {PPTX_PATH}")


if __name__ == "__main__":
    build_all_slides()
