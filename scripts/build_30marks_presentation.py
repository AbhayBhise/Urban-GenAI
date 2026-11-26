"""Generate the 30-marks UrbanGen AI presentation (AE, Spatial VAE, MiniGPT).

Designed with a custom editorial layout (matching the clean, non-AI-generated
visual hierarchy of Cognitive Mirror) using python-pptx and real training logs /
sample outputs from the repository.
"""

import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT_PPTX = ROOT / "submission" / "UrbanGen_AI_30Marks_Presentation.pptx"
ASSETS_DIR = ROOT / "submission" / "_ppt_assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Color Palette (Editorial Navy + Crisp Off-White + Muted Domain Accents)
# ---------------------------------------------------------------------------
DARK_BG = RGBColor(22, 27, 64)       # #161B40
DARK_CARD = RGBColor(29, 36, 84)     # #1D2454
LIGHT_BG = RGBColor(244, 245, 252)   # #F4F5FC
WHITE = RGBColor(255, 255, 255)
NAVY_TEXT = RGBColor(30, 41, 89)     # #1E2959
BODY_TEXT = RGBColor(51, 65, 85)     # #334155
MUTED_TEXT = RGBColor(100, 116, 139) # #64748B
LIGHT_MUTED = RGBColor(203, 213, 225)

BLUE = RGBColor(37, 99, 235)         # #2563EB
TEAL = RGBColor(13, 148, 136)        # #0D9488
PURPLE = RGBColor(124, 58, 237)      # #7C3AED
AMBER = RGBColor(217, 119, 6)        # #D97706
GOLD = RGBColor(245, 158, 11)        # #F59E0B
ROSE = RGBColor(219, 39, 119)        # #DB2777
SLATE_BORDER = RGBColor(203, 213, 225)
ZEBRA_ROW = RGBColor(248, 250, 252)
ZEBRA_ALT = RGBColor(241, 245, 249)

FONT_FAMILY = "Segoe UI"


# ---------------------------------------------------------------------------
# Chart & Visual Asset Generation (from real repo data)
# ---------------------------------------------------------------------------
def build_assets():
    assets = {}

    # 1. Top spectrum bar image (smooth gradient strip)
    bar_path = ASSETS_DIR / "top_bar.png"
    fig, ax = plt.subplots(figsize=(13.333, 0.12), dpi=150)
    import numpy as np
    grad = np.linspace(0, 1, 512).reshape(1, -1)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("spec", ["#2563EB", "#7C3AED", "#DB2777", "#D97706"])
    ax.imshow(grad, aspect="auto", cmap=cmap)
    ax.axis("off")
    plt.subplots_adjust(0, 0, 1, 1)
    fig.savefig(bar_path, dpi=150)
    plt.close(fig)
    assets["top_bar"] = str(bar_path)

    # 2. Load real training histories
    with open(ROOT / "outputs" / "ae" / "history.json", encoding="utf-8") as f:
        ae_hist = json.load(f)
    with open(ROOT / "outputs" / "vae" / "history.json", encoding="utf-8") as f:
        vae_hist = json.load(f)
    with open(ROOT / "outputs" / "gpt" / "history.json", encoding="utf-8") as f:
        gpt_hist = json.load(f)

    # Mini plot 1: AE MSE loss
    ae_plot = ASSETS_DIR / "ae_loss.png"
    fig, ax = plt.subplots(figsize=(3.8, 1.55), dpi=180)
    ax.plot([h["epoch"] for h in ae_hist], [h["loss"] for h in ae_hist], color="#0D9488", lw=2.2)
    ax.set_facecolor("#FFFFFF")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.tick_params(labelsize=7, colors="#475569")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout(pad=0.3)
    fig.savefig(ae_plot, dpi=180)
    plt.close(fig)
    assets["ae_loss"] = str(ae_plot)

    # Mini plot 2: VAE Train vs Val PSNR
    vae_plot = ASSETS_DIR / "vae_psnr.png"
    fig, ax = plt.subplots(figsize=(3.8, 1.55), dpi=180)
    ax.plot([h["epoch"] for h in vae_hist], [h["psnr"] for h in vae_hist], color="#7C3AED", lw=2.0, label="Train")
    ax.plot([h["epoch"] for h in vae_hist], [h["val"]["psnr"] for h in vae_hist], color="#2563EB", lw=1.8, ls="--", label="Val")
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    ax.set_facecolor("#FFFFFF")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.tick_params(labelsize=7, colors="#475569")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout(pad=0.3)
    fig.savefig(vae_plot, dpi=180)
    plt.close(fig)
    assets["vae_psnr"] = str(vae_plot)

    # Mini plot 3: MiniGPT Train vs Val loss
    gpt_plot = ASSETS_DIR / "gpt_loss.png"
    fig, ax = plt.subplots(figsize=(3.8, 1.55), dpi=180)
    ax.plot([h["step"] for h in gpt_hist], [h["loss"] for h in gpt_hist], color="#2563EB", lw=2.0, label="Train")
    ax.plot([h["step"] for h in gpt_hist], [h["val_loss"] for h in gpt_hist], color="#D97706", lw=1.8, ls="--", label="Val")
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_facecolor("#FFFFFF")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.tick_params(labelsize=7, colors="#475569")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout(pad=0.3)
    fig.savefig(gpt_plot, dpi=180)
    plt.close(fig)
    assets["gpt_loss"] = str(gpt_plot)

    # 3. Sample UCMerced tiles collage (for Slide 6 & Slide 9)
    sample_names = [
        "ucmerced_sample.jpg",
        "buildings_sample.jpg",
        "forest_sample.jpg",
        "ucmerced_undeveloped.jpg",
        "ucmerced_noisy.jpg",
        "ucmerced_recon.jpg",
    ]
    sample_paths = [ROOT / "frontend" / "public" / "samples" / n for n in sample_names]
    existing = [p for p in sample_paths if p.exists()]
    if existing:
        collage_path = ASSETS_DIR / "ucmerced_collage.png"
        cols = 3
        rows = 2
        w, h = 160, 160
        canvas = Image.new("RGB", (cols * w + 16, rows * h + 16), (255, 255, 255))
        for idx, p in enumerate(existing[:6]):
            im = Image.open(p).convert("RGB").resize((w, h))
            r, c = divmod(idx, cols)
            canvas.paste(im, (4 + c * (w + 4), 4 + r * (h + 4)))
        canvas.save(collage_path)
        assets["collage"] = str(collage_path)

    # 4. Crop AE epoch 50 strip (first 6 columns of noisy + recon)
    ae_ep50 = ROOT / "outputs" / "ae" / "samples" / "epoch_50.png"
    if ae_ep50.exists():
        im = Image.open(ae_ep50)
        # epoch_50.png is 8 cols x 3 rows (noisy, recon, clean); crop top 2 rows nicely
        W, H = im.size
        crop_ae = im.crop((0, 0, W, int(H * 0.67)))
        ae_strip = ASSETS_DIR / "ae_strip.png"
        crop_ae.save(ae_strip)
        assets["ae_strip"] = str(ae_strip)

    # 5. VAE latent interpolation strip
    vae_interp = ROOT / "outputs" / "vae" / "latent_interpolation_epoch_50.png"
    if vae_interp.exists():
        assets["vae_interp"] = str(vae_interp)

    # 6. VAE prior samples strip
    vae_prior = ROOT / "outputs" / "vae" / "prior_samples_epoch_50.png"
    if vae_prior.exists():
        assets["vae_prior"] = str(vae_prior)

    # 7. Bar chart comparing AE vs VAE metrics for Slide 15
    comp_chart = ASSETS_DIR / "ae_vs_vae_bars.png"
    fig, ax = plt.subplots(figsize=(4.4, 3.0), dpi=180)
    labels = ["Denoising AE\n(Val PSNR)", "Spatial VAE\n(Full Eval)", "Spatial VAE\n(Val Split)"]
    vals = [29.65, 29.75, 27.49]
    colors = ["#0D9488", "#7C3AED", "#2563EB"]
    y_pos = [2, 1, 0]
    bars = ax.barh(y_pos, vals, height=0.52, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8.5, color="#1E2959", fontweight="bold")
    ax.set_xlim(0, 35)
    ax.set_xlabel("Reconstruction PSNR (dB) — Higher is Better", fontsize=8, color="#475569")
    for b, v in zip(bars, vals):
        ax.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v:.2f} dB",
                va="center", fontsize=8.5, fontweight="bold", color="#1E2959")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    plt.tight_layout(pad=0.6)
    fig.savefig(comp_chart, dpi=180)
    plt.close(fig)
    assets["comp_chart"] = str(comp_chart)

    return assets


# ---------------------------------------------------------------------------
# Slide Helper Primitives
# ---------------------------------------------------------------------------
def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_top_bar(slide, bar_img_path):
    slide.shapes.add_picture(bar_img_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(0.08))


def add_header(slide, kicker, title, dark=False, kicker_color=BLUE):
    # Thin vertical accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(0.45), Inches(0.06), Inches(0.22))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD if dark else kicker_color
    bar.line.fill.background()

    # Kicker
    tb = slide.shapes.add_textbox(Inches(0.78), Inches(0.40), Inches(11.0), Inches(0.32))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = kicker.upper()
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD if dark else kicker_color

    # Title
    tb2 = slide.shapes.add_textbox(Inches(0.65), Inches(0.74), Inches(12.0), Inches(0.68))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(27)
    p2.font.bold = True
    p2.font.color.rgb = WHITE if dark else NAVY_TEXT


def add_footer(slide, section, page_num, dark=False):
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(7.02), Inches(10.5), Inches(0.3))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"MIT Academy of Engineering · UrbanGen AI · {section}"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10)
    p.font.color.rgb = LIGHT_MUTED if dark else MUTED_TEXT

    tb_n = slide.shapes.add_textbox(Inches(11.8), Inches(7.02), Inches(0.88), Inches(0.3))
    tf_n = tb_n.text_frame
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.text = str(page_num)
    p_n.font.name = FONT_FAMILY
    p_n.font.size = Pt(10)
    p_n.font.color.rgb = LIGHT_MUTED if dark else MUTED_TEXT


def add_card(slide, x, y, w, h, border_color=BLUE, fill_color=WHITE, border_pt=1.25):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.adjustments[0] = 0.06
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(border_pt)
    return card


def add_pill(slide, x, y, w, h, text, fill_color, text_color=WHITE, font_size=10.5):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    pill.adjustments[0] = 0.48
    pill.fill.solid()
    pill.fill.fore_color.rgb = fill_color
    pill.line.fill.background()
    tf = pill.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return pill


def add_text_in_box(slide, x, y, w, h, lines, align=PP_ALIGN.LEFT):
    """lines: list of (text, size_pt, bold, color, space_after_pt)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    for idx, item in enumerate(lines):
        txt, sz, bld, col, sp = item
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.text = txt
        p.font.name = FONT_FAMILY
        p.font.size = Pt(sz)
        p.font.bold = bld
        p.font.color.rgb = col
        p.space_after = Pt(sp)
    return tb


def style_table(table, col_widths, headers, rows, font_size=10.5, header_bg=NAVY_TEXT):
    for i, w in enumerate(col_widths):
        table.columns[i].width = Inches(w)

    # Header row
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Inches(0.10)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.06)
        cell.margin_bottom = Inches(0.06)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = WHITE

    # Data rows
    for r_idx, row in enumerate(rows, start=1):
        bg = ZEBRA_ROW if r_idx % 2 == 1 else ZEBRA_ALT
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_FAMILY
            p.font.size = Pt(font_size - 0.5)
            p.font.bold = (c_idx == 0)
            p.font.color.rgb = NAVY_TEXT if c_idx == 0 else BODY_TEXT


# ---------------------------------------------------------------------------
# Build All 18 Slides
# ---------------------------------------------------------------------------
def build_presentation():
    assets = build_assets()
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1 — Title (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_bg(s1, DARK_BG)
    add_top_bar(s1, assets["top_bar"])

    # MIT Badge
    badge = add_card(s1, 0.65, 0.45, 3.15, 0.62, border_color=RGBColor(71, 85, 145), fill_color=DARK_CARD, border_pt=1.0)
    add_text_in_box(s1, 0.80, 0.53, 2.90, 0.48, [
        ("MIT  |  Academy of Engineering", 12, True, WHITE, 1),
        ("Autonomous Institute · SPPU Pune · Course 2304422L", 8, False, LIGHT_MUTED, 0),
    ])

    # Kicker + Title
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(1.42), Inches(0.06), Inches(0.22))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()
    add_text_in_box(s1, 0.78, 1.38, 8.0, 0.30, [
        ("GENERATIVE AI PRACTICAL SUBMISSION · 30 MARKS", 11, True, GOLD, 0),
    ])
    add_text_in_box(s1, 0.65, 1.72, 11.8, 1.45, [
        ("UrbanGen AI", 48, True, WHITE, 4),
        ("Edge-Deployable Multi-Model Generative Framework for Aerial Remote Sensing\nand Municipal Urban Planning", 17, False, LIGHT_MUTED, 0),
    ])

    # Group Members & Guide cards
    add_card(s1, 0.65, 3.65, 6.45, 1.90, border_color=GOLD, fill_color=DARK_CARD, border_pt=1.4)
    add_text_in_box(s1, 0.90, 3.82, 6.0, 1.65, [
        ("GROUP MEMBERS (PRN)", 10.5, True, GOLD, 6),
        ("Abhay Bhise · PRN 202402040016", 12.5, False, WHITE, 3),
        ("Vedant Ingle · PRN 202402040031", 12.5, False, WHITE, 3),
        ("Disha Satpute · PRN 202402040019", 12.5, False, WHITE, 3),
        ("Vaishnavi Phad · PRN 202402040006", 12.5, False, WHITE, 0),
    ])

    add_card(s1, 7.35, 3.65, 5.33, 1.90, border_color=BLUE, fill_color=DARK_CARD, border_pt=1.4)
    add_text_in_box(s1, 7.60, 3.82, 4.9, 1.65, [
        ("PROJECT GUIDE", 10.5, True, RGBColor(147, 197, 253), 6),
        ("Dr. Savita Mane", 15, True, WHITE, 4),
        ("Department of Computer Engineering", 12, False, LIGHT_MUTED, 4),
        ("MIT Academy of Engineering, Pune", 11.5, False, LIGHT_MUTED, 0),
    ])

    # 3 Model Pills
    add_pill(s1, 0.65, 5.82, 2.05, 0.36, "Denoising Autoencoder", TEAL)
    add_pill(s1, 2.85, 5.82, 1.85, 0.36, "Spatial β-VAE", PURPLE)
    add_pill(s1, 4.85, 5.82, 2.15, 0.36, "MiniGPT Transformer", BLUE)

    add_text_in_box(s1, 0.65, 6.90, 9.0, 0.3, [
        ("MIT Academy of Engineering · Affiliated to Savitribai Phule Pune University", 10, False, LIGHT_MUTED, 0),
    ])
    add_text_in_box(s1, 10.0, 6.90, 2.68, 0.3, [
        ("Academic Year 2026-27", 10, False, LIGHT_MUTED, 0),
    ], align=PP_ALIGN.RIGHT)

    # =========================================================================
    # SLIDE 2 — Index (Light)
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_bg(s2, LIGHT_BG)
    add_top_bar(s2, assets["top_bar"])
    add_header(s2, "INDEX", "What this presentation covers")
    add_footer(s2, "Index", 2)

    idx_items = [
        ("01", "Problem statement", "Slide 3", BLUE),
        ("02", "Literature survey", "Slide 4", BLUE),
        ("03", "Objectives, outcomes, limits", "Slides 5–7", BLUE),
        ("04", "System design", "Slide 8", PURPLE),
        ("05", "Practical implementation", "Slides 9–12", PURPLE),
        ("06", "Demonstration & comparison", "Slides 13–15", PURPLE),
        ("07", "Challenges faced", "Slide 16", AMBER),
        ("08", "Conclusion", "Slide 17", AMBER),
        ("09", "References", "Slide 18", AMBER),
    ]
    for i, (num, title, sl, col) in enumerate(idx_items):
        r, c = divmod(i, 3)
        x = 0.65 + c * 4.08
        y = 1.65 + r * 1.68
        add_card(s2, x, y, 3.85, 1.42, border_color=col, fill_color=WHITE, border_pt=1.35)
        add_text_in_box(s2, x + 0.22, y + 0.16, 3.4, 1.12, [
            (num, 20, True, col, 4),
            (title, 13.5, True, NAVY_TEXT, 2),
            (sl, 10.5, False, MUTED_TEXT, 0),
        ])

    # =========================================================================
    # SLIDE 3 — Problem Statement (Dark Navy)
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_bg(s3, DARK_BG)
    add_top_bar(s3, assets["top_bar"])
    add_header(s3, "PROBLEM STATEMENT", "Can one edge-ready system restore tiles, detect\nanomalies, and draft urban planning policies?", dark=True)
    add_footer(s3, "Problem statement", 3, dark=True)

    add_text_in_box(s3, 0.65, 1.72, 11.8, 0.85, [
        ("Municipal planners rely on manual satellite inspection and static GIS layers that cannot repair noisy imagery, flag subtle structural anomalies, or draft ward-level sustainability policies on consumer hardware.", 14, False, LIGHT_MUTED, 0),
    ])

    prob_cards = [
        ("01", "Degraded Imagery", "Sensor noise (σ=0.15) obscures road junctions and parcel edges; plain bottleneck AEs lose ~7 dB of fine spatial detail."),
        ("02", "No Anomaly Baseline", "Visual inspection misses unusual land-use structures; a calibrated latent space is needed for unsupervised anomaly scoring."),
        ("03", "Static Policy Drafting", "GIS statistics sit unused without a domain-grounded Transformer to convert ward land-use counts into actionable advisories."),
    ]
    for i, (num, head, desc) in enumerate(prob_cards):
        x = 0.65 + i * 4.08
        add_card(s3, x, 2.95, 3.85, 2.75, border_color=GOLD, fill_color=DARK_CARD, border_pt=1.4)
        add_text_in_box(s3, x + 0.24, 3.20, 3.38, 2.30, [
            (num, 22, True, GOLD, 6),
            (head, 15, True, WHITE, 6),
            (desc, 11.5, False, LIGHT_MUTED, 0),
        ])

    # =========================================================================
    # SLIDE 4 — Literature Survey (Light)
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_bg(s4, LIGHT_BG)
    add_top_bar(s4, assets["top_bar"])
    add_header(s4, "LITERATURE SURVEY", "Eight foundational works this project builds on")
    add_footer(s4, "Literature survey", 4)

    lit_headers = ["#", "Authors (Year)", "Technique", "Key Contribution", "Used in UrbanGen AI"]
    lit_rows = [
        ["1", "Yang & Newsam (2010)", "UCMerced LandUse", "21-class aerial remote sensing benchmark (2,100 tiles)", "Vision training & evaluation dataset"],
        ["2", "Ronneberger et al. (2015)", "U-Net Skip Connections", "Encoder-decoder skips preserve fine spatial edges", "Denoising AE & Spatial VAE decoder"],
        ["3", "He et al. (2016)", "ResNet-18 Backbone", "Residual blocks enable stable transfer learning", "Pretrained feature extractor (AE & VAE)"],
        ["4", "Kingma & Welling (2014)", "Variational Autoencoder", "Reparameterization trick + ELBO latent space", "Spatial β-VAE probabilistic latent"],
        ["5", "Higgins et al. (2017)", "β-VAE", "Weighted KL term balances reconstruction & disentanglement", "Controlled β=1e-4 + free-bits training"],
        ["6", "Vaswani et al. (2017)", "Transformer", "Scaled dot-product self-attention replaces recurrence", "MiniGPT causal attention blocks"],
        ["7", "Radford et al. (2019)", "GPT (Decoder-Only)", "Autoregressive next-token LM with pre-norm blocks", "MiniGPT urban policy generator"],
        ["8", "Wang et al. (2004)", "PSNR & MSE Metrics", "Quantitative fidelity benchmarking for image restoration", "AE vs. VAE comparative evaluation"],
    ]
    tbl_shape = s4.shapes.add_table(len(lit_rows) + 1, 5, Inches(0.65), Inches(1.62), Inches(12.03), Inches(5.05))
    style_table(tbl_shape.table, [0.45, 2.25, 2.25, 4.18, 2.90], lit_headers, lit_rows, font_size=10.5)

    # =========================================================================
    # SLIDE 5 — Objectives (Light)
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_bg(s5, LIGHT_BG)
    add_top_bar(s5, assets["top_bar"])
    add_header(s5, "OBJECTIVES", "Five goals for UrbanGen AI (30-Marks Scope)")
    add_footer(s5, "Objectives", 5)

    objs = [
        ("01", "Image denoising:", "restore degraded 128×128 aerial tiles with a ResNet-18 U-Net Denoising Autoencoder.", BLUE),
        ("02", "Probabilistic latent & anomalies:", "build a Spatial β-VAE (8×8×64) for smooth tile morphing and z-score anomaly detection.", TEAL),
        ("03", "Policy text generation:", "train a 4-layer MiniGPT causal Transformer from scratch on Pune urban planning text.", AMBER),
        ("04", "Model comparison:", "benchmark AE, Spatial β-VAE, and MiniGPT fairly on MSE, PSNR, KL, loss, and perplexity.", ROSE),
        ("05", "Responsible edge deployment:", "ship a live React + FastAPI app with clear advisory disclaimers and 512 MB cloud safety.", PURPLE),
    ]
    for i, (num, lead, rest, col) in enumerate(objs):
        y = 1.65 + i * 0.98
        add_card(s5, 0.65, y, 12.03, 0.80, border_color=col, fill_color=WHITE, border_pt=1.4)
        tb = s5.shapes.add_textbox(Inches(0.88), Inches(y + 0.16), Inches(11.55), Inches(0.50))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        r0 = p.add_run(); r0.text = f"{num}   "; r0.font.name = FONT_FAMILY; r0.font.size = Pt(17); r0.font.bold = True; r0.font.color.rgb = col
        r1 = p.add_run(); r1.text = lead + " "; r1.font.name = FONT_FAMILY; r1.font.size = Pt(13); r1.font.bold = True; r1.font.color.rgb = NAVY_TEXT
        r2 = p.add_run(); r2.text = rest; r2.font.name = FONT_FAMILY; r2.font.size = Pt(13); r2.font.bold = False; r2.font.color.rgb = BODY_TEXT

    # =========================================================================
    # SLIDE 6 — Outcomes (Light)
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_bg(s6, LIGHT_BG)
    add_top_bar(s6, assets["top_bar"])
    add_header(s6, "OUTCOMES", "What the three core modules delivered")
    add_footer(s6, "Outcomes", 6)

    kpis = [
        ("DENOISING AE · PSNR", "29.65 dB", "MSE 0.00585 (+7.0 dB vs bottleneck)", TEAL),
        ("SPATIAL β-VAE · RECON", "27.49 dB", "Val PSNR (29.75 dB full eval)", PURPLE),
        ("SPATIAL β-VAE · KL", "60.72 nats", "Active 8×8×64 latent, no collapse", BLUE),
        ("MINIGPT · PERPLEXITY", "1.087", "Val loss 0.1043 · BPC 0.1199", AMBER),
        ("EDGE FOOTPRINT", "50 epochs", "Trained on single RTX 4050 (6 GB)", ROSE),
        ("LIVE WEB PLATFORM", "React + API", "Vercel UI + Render FastAPI backend", NAVY_TEXT),
    ]
    for i, (lbl, big, sub, col) in enumerate(kpis):
        r, c = divmod(i, 2)
        x = 0.65 + c * 3.72
        y = 1.68 + r * 1.65
        add_card(s6, x, y, 3.52, 1.45, border_color=col, fill_color=WHITE, border_pt=1.35)
        add_text_in_box(s6, x + 0.20, y + 0.16, 3.15, 1.15, [
            (lbl, 9.5, True, col, 3),
            (big, 24, True, NAVY_TEXT, 3),
            (sub, 10, False, MUTED_TEXT, 0),
        ])

    # Right side real sample image card
    add_card(s6, 8.20, 1.68, 4.48, 3.45, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    if "collage" in assets:
        s6.shapes.add_picture(assets["collage"], Inches(8.34), Inches(1.82), width=Inches(4.20))
    add_text_in_box(s6, 8.25, 5.24, 4.38, 1.25, [
        ("Real UCMerced LandUse tiles (top) alongside noisy input (σ=0.15) and Denoising AE reconstruction (bottom right). Both AE and VAE operate on 128×128 RGB patches.", 11, False, BODY_TEXT, 0),
    ])

    # =========================================================================
    # SLIDE 7 — Limitations (Light)
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    set_bg(s7, LIGHT_BG)
    add_top_bar(s7, assets["top_bar"])
    add_header(s7, "LIMITATIONS", "Where the current system falls short")
    add_footer(s7, "Limitations", 7)

    lims = [
        ("128×128 RESOLUTION", "Aerial tiles are resized from 256×256 to 128×128 to fit a 6 GB laptop GPU, softening sub-meter building details."),
        ("SHORT TEXT CONTEXT", "MiniGPT uses character-level tokens with a 192-char window, limiting long multi-paragraph policy memory."),
        ("STATIC DATASET", "UCMerced covers 21 fixed US/benchmark classes without multi-temporal before/after urban change pairs."),
        ("NO REAL-WORLD METERS", "Anomaly z-scores flag statistical reconstruction outliers relative to UCMerced, not legal zoning violations."),
        ("ADVISORY-ONLY TEXT", "Generated FSI, TOD, and drainage policies must be reviewed by human municipal planners before adoption."),
        ("FREE-TIER CLOUD RAM", "Render's 512 MB limit requires sequential single-model swapping in production via _MODEL_LOCK."),
    ]
    for i, (head, desc) in enumerate(lims):
        r, c = divmod(i, 3)
        x = 0.65 + c * 4.08
        y = 1.72 + r * 2.25
        add_card(s7, x, y, 3.85, 1.98, border_color=AMBER, fill_color=WHITE, border_pt=1.35)
        add_text_in_box(s7, x + 0.22, y + 0.20, 3.42, 1.60, [
            (head, 11, True, AMBER, 8),
            (desc, 11.5, False, BODY_TEXT, 0),
        ])

    # =========================================================================
    # SLIDE 8 — System Design (Light)
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    set_bg(s8, LIGHT_BG)
    add_top_bar(s8, assets["top_bar"])
    add_header(s8, "SYSTEM DESIGN", "End-to-end multimodal workflow")
    add_footer(s8, "System design", 8)

    col_labels = [(0.65, "INPUT"), (2.95, "PREPROCESS"), (5.35, "MODEL"), (7.85, "EVALUATE"), (10.25, "INTERFACE")]
    for lx, ltxt in col_labels:
        add_text_in_box(s8, lx, 1.62, 2.0, 0.25, [(ltxt, 10, True, MUTED_TEXT, 0)])

    # Row 1: Text (MiniGPT)
    add_card(s8, 0.65, 1.98, 2.0, 1.05, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 0.78, 2.18, 1.75, 0.7, [("Pune GIS Stats\n& Corpus (241 KB)", 11.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_card(s8, 2.95, 1.98, 2.05, 1.05, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 3.05, 2.18, 1.85, 0.7, [("Char Tokenize\nblock_size = 192", 11.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_pill(s8, 5.35, 2.04, 2.15, 0.92, "MiniGPT Transformer\n4 Layers · 4 Heads", BLUE, font_size=11)

    add_card(s8, 7.85, 1.98, 2.05, 1.05, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 7.95, 2.18, 1.85, 0.7, [("Val Loss · PPL\nBPC (0.1199)", 11.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    # Row 2: Images (AE + VAE)
    add_card(s8, 0.65, 3.35, 2.0, 2.65, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 0.78, 4.15, 1.75, 1.1, [("Aerial Tiles\nUCMerced\n2,100 RGB", 12, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_card(s8, 2.95, 3.35, 2.05, 2.65, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 3.05, 4.10, 1.85, 1.2, [("Resize 128×128\nNorm [-1, 1]\nNoise σ=0.15", 11.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_pill(s8, 5.35, 3.55, 2.15, 1.02, "Denoising AE\nResNet18 + U-Net", TEAL, font_size=11)
    add_pill(s8, 5.35, 4.78, 2.15, 1.02, "Spatial β-VAE\n64×8×8 Latent", PURPLE, font_size=11)

    add_card(s8, 7.85, 3.35, 2.05, 2.65, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s8, 7.95, 4.10, 1.85, 1.2, [("MSE · PSNR\nKL Divergence\nAnomaly z-score", 11.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    # Interface block
    add_card(s8, 10.25, 1.98, 2.43, 4.02, border_color=NAVY_TEXT, fill_color=DARK_BG, border_pt=1.0)
    add_text_in_box(s8, 10.42, 2.45, 2.10, 3.20, [
        ("Live Web App", 14, True, WHITE, 8),
        ("React + FastAPI", 11.5, True, GOLD, 10),
        ("• Tile Denoising (AE)", 10.5, False, LIGHT_MUTED, 5),
        ("• Anomaly Map (VAE)", 10.5, False, LIGHT_MUTED, 5),
        ("• Latent Morph (VAE)", 10.5, False, LIGHT_MUTED, 5),
        ("• Plan Draft (MiniGPT)", 10.5, False, LIGHT_MUTED, 5),
        ("• Ethics & Model Cards", 10.5, False, LIGHT_MUTED, 0),
    ])

    # Connector arrows
    for ax_x, ay_y in [(2.69, 2.44), (5.04, 2.44), (7.54, 2.44), (9.94, 2.44),
                       (2.69, 4.62), (5.04, 4.00), (5.04, 5.22), (7.54, 4.00), (7.54, 5.22), (9.94, 4.62)]:
        add_text_in_box(s8, ax_x, ay_y - 0.08, 0.28, 0.28, [("→", 14, True, MUTED_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_text_in_box(s8, 0.65, 6.28, 12.0, 0.4, [
        ("Checkpoints (model.pth) and training histories (history.json) are persisted via Git LFS and served through FastAPI on Render.", 11, False, BODY_TEXT, 0),
    ])

    # =========================================================================
    # SLIDE 9 — Implementation 1 of 4: Problem Definition & Data Collection
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    set_bg(s9, LIGHT_BG)
    add_top_bar(s9, assets["top_bar"])
    add_header(s9, "IMPLEMENTATION 1 OF 4 · PROBLEM DEFINITION AND DATA COLLECTION", "Two domain datasets, sized for edge training")
    add_footer(s9, "Implementation", 9)

    ds_cards = [
        ("UCMERCED LANDUSE · VISION", "2,100", "RGB aerial tiles across 21 urban classes (100/class). Stratified train/val/test split (seed 42), resized to 128×128.", BLUE),
        ("PUNE URBAN CORPUS · TEXT", "241,400", "characters of curated urban planning rules (FSI, TOD, SuDS drainage, green buffers). 90% train / 10% validation split.", AMBER),
        ("ANOMALY BASELINE · CALIBRATION", "294", "validation tiles used to calibrate Spatial β-VAE reconstruction MSE (mean 0.00675, std 0.00450) for z-score ranking.", PURPLE),
    ]
    for i, (lbl, big, desc, col) in enumerate(ds_cards):
        x = 0.65 + i * 4.08
        add_card(s9, x, 1.65, 3.85, 2.25, border_color=col, fill_color=WHITE, border_pt=1.35)
        add_text_in_box(s9, x + 0.22, 1.82, 3.42, 1.95, [
            (lbl, 10, True, col, 4),
            (big, 32, True, NAVY_TEXT, 4),
            (desc, 10.5, False, BODY_TEXT, 0),
        ])

    add_card(s9, 0.65, 4.18, 5.20, 2.52, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    if "collage" in assets:
        s9.shapes.add_picture(assets["collage"], Inches(0.80), Inches(4.30), width=Inches(4.90), height=Inches(2.28))

    add_text_in_box(s9, 6.15, 4.45, 6.50, 2.0, [
        ("Task: restore & inspect tiles, then draft ward policy", 16, True, NAVY_TEXT, 8),
        ("UCMerced trains both the Denoising Autoencoder (with σ=0.15 noise) and Spatial β-VAE. Real Pune OpenStreetMap land-use counts prompt MiniGPT at inference time to draft localized sustainability recommendations.", 12.5, False, BODY_TEXT, 0),
    ])

    # =========================================================================
    # SLIDE 10 — Implementation 2 of 4: Preprocessing & Model Selection
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    set_bg(s10, LIGHT_BG)
    add_top_bar(s10, assets["top_bar"])
    add_header(s10, "IMPLEMENTATION 2 OF 4 · PREPROCESSING AND MODEL SELECTION", "From raw data to the right architecture")
    add_footer(s10, "Implementation", 10)

    add_text_in_box(s10, 0.65, 1.56, 4.0, 0.25, [("IMAGE PIPELINE (AE & VAE)", 10, True, BLUE, 0)])
    img_steps = ["Raw .tif Tile", "Resize 128×128", "Flip Augmentation", "Normalize [-1, 1]", "Noise σ=0.15 (AE)"]
    for i, st in enumerate(img_steps):
        x = 0.65 + i * 2.48
        add_card(s10, x, 1.86, 2.15, 0.50, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
        add_text_in_box(s10, x + 0.08, 1.98, 1.99, 0.30, [(st, 10.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)
        if i < 4:
            add_text_in_box(s10, x + 2.17, 1.94, 0.30, 0.35, [("→", 13, True, MUTED_TEXT, 0)], align=PP_ALIGN.CENTER)

    add_text_in_box(s10, 0.65, 2.54, 4.0, 0.25, [("TEXT PIPELINE (MINIGPT)", 10, True, PURPLE, 0)])
    txt_steps = ["urban_planning.txt", "Char Vocab (stoi)", "90/10 Train/Val", "Chunk block_size=192", "Next-Char Target"]
    for i, st in enumerate(txt_steps):
        x = 0.65 + i * 2.48
        add_card(s10, x, 2.84, 2.15, 0.50, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
        add_text_in_box(s10, x + 0.08, 2.96, 1.99, 0.30, [(st, 10.5, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)
        if i < 4:
            add_text_in_box(s10, x + 2.17, 2.92, 0.30, 0.35, [("→", 13, True, MUTED_TEXT, 0)], align=PP_ALIGN.CENTER)

    sel_headers = ["Task", "Model Chosen", "Architectural Rationale"]
    sel_rows = [
        ["Restore degraded tiles", "Denoising AE (ResNet-18 + U-Net)", "Full multi-scale skip connections preserve fine roads & parcel edges (+7 dB vs bottleneck)."],
        ["Anomaly & latent morph", "Spatial β-VAE (64×8×8 latent)", "Compact projected skips + skip dropout prevent KL collapse while keeping latent spatial."],
        ["Draft urban policies", "MiniGPT (4-layer causal LM)", "Built from scratch (1.3M params); lightweight enough for CPU/free-tier cloud inference."],
    ]
    tbl10 = s10.shapes.add_table(4, 3, Inches(0.65), Inches(3.68), Inches(12.03), Inches(2.70))
    style_table(tbl10.table, [2.40, 3.40, 6.23], sel_headers, sel_rows, font_size=11)

    # =========================================================================
    # SLIDE 11 — Implementation 3 of 4: Training, Fine-Tuning & Evaluation
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    set_bg(s11, LIGHT_BG)
    add_top_bar(s11, assets["top_bar"])
    add_header(s11, "IMPLEMENTATION 3 OF 4 · TRAINING, FINE-TUNING AND EVALUATION", "Three models, measured training logs")
    add_footer(s11, "Implementation", 11)

    tr_headers = ["Model", "Training Setup", "Headline Result"]
    tr_rows = [
        ["Denoising AE", "50 epochs, batch 32, encoder frozen 5 epochs, Adam lr=1e-4, σ=0.15", "PSNR 29.65 dB · MSE 0.00585"],
        ["Spatial β-VAE", "50 epochs, β=1e-4, KL warmup 2 epochs, free bits 0.01, 0.7·L1+0.3·MSE", "Val PSNR 27.49 dB · KL 60.72 nats"],
        ["MiniGPT", "1,000 steps, batch 32, block 192, AdamW lr=3e-4, grad clip 1.0", "Val loss 0.1043 · PPL 1.087"],
    ]
    tbl11 = s11.shapes.add_table(4, 3, Inches(0.65), Inches(1.62), Inches(12.03), Inches(2.15))
    style_table(tbl11.table, [2.10, 6.43, 3.50], tr_headers, tr_rows, font_size=11)

    charts_info = [
        ("Denoising AE MSE loss", "ae_loss", "Smooth convergence to 0.00617 train MSE"),
        ("Spatial β-VAE PSNR (dB)", "vae_psnr", "Purple train, dashed blue val (27.49 dB)"),
        ("MiniGPT cross-entropy loss", "gpt_loss", "Blue train (0.147), dashed amber val (0.104)"),
    ]
    for i, (ctitle, ckey, ccap) in enumerate(charts_info):
        x = 0.65 + i * 4.08
        add_text_in_box(s11, x, 4.00, 3.85, 0.28, [(ctitle, 11.5, True, NAVY_TEXT, 0)])
        add_card(s11, x, 4.30, 3.85, 1.95, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
        if ckey in assets:
            s11.shapes.add_picture(assets[ckey], Inches(x + 0.08), Inches(4.36), width=Inches(3.69), height=Inches(1.82))
        add_text_in_box(s11, x, 6.32, 3.85, 0.30, [(ccap, 10, False, MUTED_TEXT, 0)])

    # =========================================================================
    # SLIDE 12 — Implementation 4 of 4: Testing, Deployment, Ethics & Safety
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    set_bg(s12, LIGHT_BG)
    add_top_bar(s12, assets["top_bar"])
    add_header(s12, "IMPLEMENTATION 4 OF 4 · TESTING, DEPLOYMENT, ETHICS AND SAFETY", "From Colab notebooks to a responsible live interface")
    add_footer(s12, "Implementation", 12)

    q_cards = [
        ("TESTING AND ITERATION", BLUE, [
            "• Stratified seed-42 split guarantees zero overlap between train and validation tiles.",
            "• Pre-computed 294-tile VAE anomaly baseline (mean=0.00675, std=0.00450) for cloud parity.",
            "• Low-memory lock (_MODEL_LOCK) verified across all endpoints without 512 MB OOM crashes.",
        ]),
        ("DEPLOYMENT · REACT + FASTAPI", PURPLE, [
            "• Live React/Vite frontend on Vercel connected to FastAPI + PyTorch on Render.",
            "• Dedicated interactive tabs: Denoising AE, Spatial β-VAE, Urban Plan Generator, Governance.",
            "• Three standalone Colab notebooks (.ipynb + .pdf) packaged in submission/ for reproducibility.",
        ]),
        ("ETHICS AND BIAS", AMBER, [
            "• Geographic bias: UCMerced reflects US urban layouts; outputs may not generalize directly to Indian cities.",
            "• Data privacy: only public open-access satellite tiles and municipal GIS aggregates are processed.",
            "• Corpus transparency: MiniGPT corpus is curated locally without unverified web scraping.",
        ]),
        ("RESPONSIBLE AI AND SAFETY", ROSE, [
            "• All AI-generated plans and anomaly flags are explicitly labeled Advisory Only.",
            "• Outputs support human urban planners and never automate zoning or enforcement decisions.",
            "• Full governance documentation (ETHICS.md, PRIVACY.md, MODEL_CARD.md) surfaced in-app.",
        ]),
    ]
    for i, (qtitle, qcol, bullets) in enumerate(q_cards):
        r, c = divmod(i, 2)
        x = 0.65 + c * 6.15
        y = 1.68 + r * 2.58
        add_card(s12, x, y, 5.88, 2.34, border_color=qcol, fill_color=WHITE, border_pt=1.4)
        lines = [(qtitle, 11, True, qcol, 8)] + [(b, 11, False, BODY_TEXT, 6) for b in bullets]
        add_text_in_box(s12, x + 0.24, y + 0.20, 5.40, 1.98, lines)

    # =========================================================================
    # SLIDE 13 — Demonstration 1 of 2: Autoencoder vs VAE
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    set_bg(s13, LIGHT_BG)
    add_top_bar(s13, assets["top_bar"])
    add_header(s13, "DEMONSTRATION 1 OF 2 · AUTOENCODER VS VAE", "Reconstruction fidelity against latent structure")
    add_footer(s13, "Demonstration", 13)

    # Left visuals
    add_card(s13, 0.65, 1.65, 5.45, 2.05, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    if "ae_strip" in assets:
        s13.shapes.add_picture(assets["ae_strip"], Inches(0.75), Inches(1.75), width=Inches(5.25))
    add_text_in_box(s13, 0.65, 3.76, 5.45, 0.28, [("AE: noisy tiles (top) restored cleanly below (29.65 dB PSNR)", 10.5, False, BODY_TEXT, 0)])

    add_card(s13, 0.65, 4.15, 5.45, 1.15, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    if "vae_prior" in assets:
        s13.shapes.add_picture(assets["vae_prior"], Inches(0.75), Inches(4.28), width=Inches(5.25))
    add_text_in_box(s13, 0.65, 5.34, 5.45, 0.28, [("VAE: novel tiles sampled directly from Gaussian prior N(0, I)", 10.5, False, BODY_TEXT, 0)])

    add_card(s13, 0.65, 5.68, 5.45, 1.00, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    if "vae_interp" in assets:
        s13.shapes.add_picture(assets["vae_interp"], Inches(0.75), Inches(5.78), width=Inches(5.25))
    add_text_in_box(s13, 0.65, 6.72, 5.45, 0.28, [("VAE: smooth latent interpolation between two urban parcels", 10.5, False, BODY_TEXT, 0)])

    # Right table + takeaway
    av_headers = ["Metric", "Denoising AE", "Spatial β-VAE"]
    av_rows = [
        ["Latent shape", "8×8×256 (deterministic)", "8×8×64 (μ, log σ²)"],
        ["Skip connections", "Full U-Net skips", "Compact (16 ch + 0.2 drop)"],
        ["MSE (lower better)", "0.00585 (eval)", "0.00713 (val)"],
        ["PSNR (higher better)", "29.65 dB", "27.49 dB (val) / 29.75 dB"],
        ["KL divergence", "None", "60.72 nats (val)"],
        ["Latent interpolation", "Not regularized", "Smooth continuous morph"],
        ["Anomaly scoring", "Pixel residual only", "Calibrated z-score map"],
    ]
    tbl13 = s13.shapes.add_table(8, 3, Inches(6.35), Inches(1.65), Inches(6.33), Inches(3.55))
    style_table(tbl13.table, [2.15, 2.09, 2.09], av_headers, av_rows, font_size=10.5)

    add_card(s13, 6.35, 5.40, 6.33, 1.32, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    tb13 = s13.shapes.add_textbox(Inches(6.55), Inches(5.55), Inches(5.95), Inches(1.05))
    tf13 = tb13.text_frame; tf13.word_wrap = True
    p13 = tf13.paragraphs[0]
    r_a = p13.add_run(); r_a.text = "Takeaway: "; r_a.font.name = FONT_FAMILY; r_a.font.size = Pt(12); r_a.font.bold = True; r_a.font.color.rgb = NAVY_TEXT
    r_b = p13.add_run(); r_b.text = "the Denoising Autoencoder restores noisy satellite edges sharpest, while only the Spatial β-VAE provides a regular Gaussian latent space for sampling, morphing, and calibrated anomaly ranking."; r_b.font.name = FONT_FAMILY; r_b.font.size = Pt(12); r_b.font.color.rgb = BODY_TEXT

    # =========================================================================
    # SLIDE 14 — Demonstration 2 of 2: Transformer vs Autoencoder Family
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    set_bg(s14, LIGHT_BG)
    add_top_bar(s14, assets["top_bar"])
    add_header(s14, "DEMONSTRATION 2 OF 2 · TRANSFORMER VS AUTOENCODER FAMILY", "Causal attention over text, convolution over tiles")
    add_footer(s14, "Demonstration", 14)

    flow_rows = [
        ("MiniGPT", BLUE, ["Char Tokens", "Causal Self-Attn ×4", "Linear LM Head", "Policy Text"]),
        ("Denoising AE", TEAL, ["Noisy Tile", "ResNet-18 Encoder", "8×8×256 + Skips", "Clean Tile"]),
        ("Spatial β-VAE", PURPLE, ["Clean Tile", "ResNet-18 Encoder", "μ, σ → z (64×8×8)", "Recon + Anomaly"]),
    ]
    for r_i, (rname, rcol, boxes) in enumerate(flow_rows):
        y = 1.65 + r_i * 0.78
        add_pill(s14, 0.65, y, 1.75, 0.56, rname, rcol, font_size=11.5)
        for b_i, btxt in enumerate(boxes):
            bx = 2.68 + b_i * 2.58
            add_text_in_box(s14, bx - 0.25, y + 0.12, 0.24, 0.30, [("→", 13, True, MUTED_TEXT, 0)], align=PP_ALIGN.CENTER)
            add_card(s14, bx, y, 2.25, 0.56, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
            add_text_in_box(s14, bx + 0.08, y + 0.14, 2.09, 0.32, [(btxt, 11, True, NAVY_TEXT, 0)], align=PP_ALIGN.CENTER)

    fam_headers = ["Aspect", "MiniGPT Transformer", "Denoising Autoencoder", "Spatial β-VAE"]
    fam_rows = [
        ["Input", "Urban context prompt (≤192 chars)", "128×128 noisy RGB tile (σ=0.15)", "128×128 clean RGB tile"],
        ["Task", "Autoregressive policy drafting", "Denoise & restore fine edges", "Reconstruct, sample, detect anomalies"],
        ["Loss Function", "Cross-Entropy (next-char)", "Pixel MSE", "ELBO (0.7·L1 + 0.3·MSE + β·KL)"],
        ["Demo Output", "FSI/TOD/SuDS bullets (PPL 1.087)", "Restored tile (29.65 dB PSNR)", "Anomaly z-score + latent morph"],
    ]
    tbl14 = s14.shapes.add_table(5, 4, Inches(0.65), Inches(4.15), Inches(12.03), Inches(2.50))
    style_table(tbl14.table, [2.00, 3.45, 3.29, 3.29], fam_headers, fam_rows, font_size=11)

    # =========================================================================
    # SLIDE 15 — Comparative Analysis: Two GenAI Models
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    set_bg(s15, LIGHT_BG)
    add_top_bar(s15, assets["top_bar"])
    add_header(s15, "COMPARATIVE ANALYSIS · TWO GENAI MODELS", "Denoising AE vs Spatial β-VAE, side by side")
    add_footer(s15, "Comparative analysis", 15)

    comp_headers = ["Metric", "Denoising AE", "Spatial β-VAE"]
    comp_rows = [
        ["Generative family", "Deterministic U-Net AE", "Probabilistic β-VAE"],
        ["Parameters", "11.4M (ResNet-18)", "12.1M (ResNet-18 + heads)"],
        ["Training data", "UCMerced (2,100 tiles)", "UCMerced (2,100 tiles)"],
        ["Final train loss (ep 50)", "0.00617 (MSE)", "0.08220 (ELBO)"],
        ["Eval / Val MSE", "0.00585 (eval)", "0.00713 (val)"],
        ["Eval / Val PSNR", "29.65 dB", "27.49 dB (val) / 29.75 dB"],
        ["KL divergence", "not applicable", "60.72 nats (val)"],
        ["Sampling from prior", "not supported", "supported (N(0, I))"],
        ["Anomaly z-score", "uncalibrated", "calibrated (mean 0.00675)"],
    ]
    tbl15 = s15.shapes.add_table(10, 3, Inches(0.65), Inches(1.62), Inches(7.05), Inches(4.35))
    style_table(tbl15.table, [2.35, 2.35, 2.35], comp_headers, comp_rows, font_size=10.5)

    add_card(s15, 7.95, 1.62, 4.73, 4.35, border_color=SLATE_BORDER, fill_color=WHITE, border_pt=1.0)
    add_text_in_box(s15, 8.15, 1.78, 4.35, 0.65, [
        ("Reconstruction PSNR Comparison", 13.5, True, NAVY_TEXT, 2),
        ("Higher is better. Both models exceed 27 dB.", 10.5, False, MUTED_TEXT, 0),
    ])
    if "comp_chart" in assets:
        s15.shapes.add_picture(assets["comp_chart"], Inches(8.08), Inches(2.50), width=Inches(4.48))

    add_text_in_box(s15, 0.65, 6.20, 12.03, 0.45, [
        ("Both vision models share the ResNet-18 encoder: Denoising AE maximizes pure pixel restoration under noise, whereas Spatial β-VAE adds a structured latent distribution for generation and anomaly detection.", 11.5, False, BODY_TEXT, 0),
    ])

    # =========================================================================
    # SLIDE 16 — Challenges Faced
    # =========================================================================
    s16 = prs.slides.add_slide(blank)
    set_bg(s16, LIGHT_BG)
    add_top_bar(s16, assets["top_bar"])
    add_header(s16, "CHALLENGES FACED", "Six problems and how we handled them")
    add_footer(s16, "Challenges", 16)

    chals = [
        ("BOTTLENECK BLUR IN AE", "Plain 8×8×256 bottleneck lost dense residential details (~21 dB). Fix: added U-Net multi-scale skip connections (+7 dB)."),
        ("POSTERIOR KL COLLAPSE", "Full skips let the VAE decoder ignore the latent. Fix: compact 16-ch skips, 0.2 skip dropout, KL warmup & free bits (0.01)."),
        ("CHAR-LEVEL REPETITION", "MiniGPT repeated phrases at low temperature. Fix: top-k=40 sampling, temperature=0.8, and grad clipping at 1.0."),
        ("CLOUD 512 MB OOM", "Loading multiple PyTorch models crashed Render Free Tier. Fix: _MODEL_LOCK + single-model swap + pretrained=False."),
        ("MISSING CLOUD BASELINE", "Render lacked raw UCMerced tiles for VAE z-scores. Fix: pre-computed 294-tile baseline embedded in api.py."),
        ("502 MASKED AS CORS", "OOM crashes dropped HTTP headers, looking like CORS errors. Fix: serialized model swaps and chunked batch memory."),
    ]
    for i, (head, desc) in enumerate(chals):
        r, c = divmod(i, 3)
        x = 0.65 + c * 4.08
        y = 1.72 + r * 2.25
        add_card(s16, x, y, 3.85, 1.98, border_color=AMBER, fill_color=WHITE, border_pt=1.35)
        add_text_in_box(s16, x + 0.22, y + 0.20, 3.42, 1.60, [
            (head, 11, True, AMBER, 8),
            (desc, 11.5, False, BODY_TEXT, 0),
        ])

    # =========================================================================
    # SLIDE 17 — Conclusion (Dark Navy)
    # =========================================================================
    s17 = prs.slides.add_slide(blank)
    set_bg(s17, DARK_BG)
    add_top_bar(s17, assets["top_bar"])
    add_header(s17, "CONCLUSION", "Verdict: the right generative family for each task", dark=True)
    add_footer(s17, "Conclusion", 17, dark=True)

    conc = [
        ("DENOISING TILES (AE)", "PSNR 29.65 dB", "ResNet-18 + U-Net skips restore noisy satellite imagery with sharp road and parcel edges."),
        ("LATENT & ANOMALIES (VAE)", "PSNR 27.49 dB", "Spatial β-VAE (64×8×8) enables smooth parcel morphing and calibrated z-score anomaly detection."),
        ("POLICY DRAFTING (MINIGPT)", "PPL 1.087", "From-scratch 4-layer Transformer turns Pune GIS ward counts into structured advisory recommendations."),
    ]
    for i, (lbl, big, desc) in enumerate(conc):
        x = 0.65 + i * 4.08
        add_card(s17, x, 1.68, 3.85, 2.38, border_color=GOLD, fill_color=DARK_CARD, border_pt=1.4)
        add_text_in_box(s17, x + 0.24, 1.88, 3.38, 2.00, [
            (lbl, 10.5, True, GOLD, 4),
            (big, 26, True, WHITE, 6),
            (desc, 11.5, False, LIGHT_MUTED, 0),
        ])

    add_text_in_box(s17, 0.65, 4.45, 12.0, 1.05, [
        ("NEXT STEPS", 10.5, True, GOLD, 4),
        ("Integrate subword BPE tokenization for longer MiniGPT context, fine-tune on Indian municipal satellite tiles (Pune/NRSC), and pair with human-in-the-loop planner sign-off.", 13, False, LIGHT_MUTED, 0),
    ])

    add_text_in_box(s17, 0.65, 5.58, 12.0, 0.30, [
        ("30-MARKS CORE MODULE SUMMARY", 10, True, GOLD, 0),
    ])
    add_pill(s17, 0.65, 5.92, 3.80, 0.42, "Denoising AE · 29.65 dB PSNR", TEAL, font_size=11)
    add_pill(s17, 4.76, 5.92, 3.80, 0.42, "Spatial β-VAE · 60.72 nats KL", PURPLE, font_size=11)
    add_pill(s17, 8.88, 5.92, 3.80, 0.42, "MiniGPT · 1.087 Perplexity", BLUE, font_size=11)

    # =========================================================================
    # SLIDE 18 — References (Light)
    # =========================================================================
    s18 = prs.slides.add_slide(blank)
    set_bg(s18, LIGHT_BG)
    add_top_bar(s18, assets["top_bar"])
    add_header(s18, "REFERENCES", "Sources, papers, and datasets")
    add_footer(s18, "References", 18)

    refs_left = [
        '[1] Vaswani, A. et al. "Attention Is All You Need." NeurIPS, 2017.',
        '[2] Kingma, D. P., Welling, M. "Auto-Encoding Variational Bayes." ICLR, 2014.',
        '[3] Higgins, I. et al. "beta-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework." ICLR, 2017.',
        '[4] Ronneberger, O., Fischer, P., Brox, T. "U-Net: Convolutional Networks for Biomedical Image Segmentation." MICCAI, 2015.',
        '[5] He, K. et al. "Deep Residual Learning for Image Recognition." CVPR, 2016.',
        '[6] Radford, A. et al. "Language Models are Unsupervised Multitask Learners (GPT-2)." OpenAI, 2019.',
    ]
    refs_right = [
        '[7] Yang, Y., Newsam, S. "Bag-of-Visual-Words and Spatial Extensions for Land-Use Classification (UCMerced)." ACM GIS, 2010.',
        '[8] Wang, Z. et al. "Image Quality Assessment: From Error Visibility to Structural Similarity." IEEE TIP, 2004.',
        '[9] Vincent, P. et al. "Extracting and Composing Robust Features with Denoising Autoencoders." ICML, 2008.',
        '[10] Paszke, A. et al. "PyTorch: An Imperative Style, High-Performance Deep Learning Library." NeurIPS, 2019.',
        '[11] GitHub Repository: https://github.com/AbhayBhise/Urban-GenAI',
        '[12] Colab Notebooks: submission/notebooks/ (01_Denoising_Autoencoder_AE, 02_Spatial_VAE, 03_MiniGPT_Transformer).',
    ]
    add_text_in_box(s18, 0.65, 1.72, 5.75, 4.90, [(r, 11.5, False, BODY_TEXT, 14) for r in refs_left])
    add_text_in_box(s18, 6.85, 1.72, 5.83, 4.90, [(r, 11.5, False, BODY_TEXT, 14) for r in refs_right])

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Saved presentation ({len(prs.slides)} slides) -> {OUT_PPTX}")


if __name__ == "__main__":
    build_presentation()
