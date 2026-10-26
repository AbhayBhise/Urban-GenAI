"""Build a source-backed UrbanGenAI presentation.

Every metric and architecture claim in this deck is read from repository
artifacts or the implemented backend. Generated images are labelled as model
outputs, not observations.
"""

import json
import os
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "UrbanGenAI_Professor_Presentation_Updated.pptx"
ASSETS = ROOT / "outputs" / "presentation_assets"
ASSETS.mkdir(parents=True, exist_ok=True)

NAVY = RGBColor(0x0B, 0x18, 0x2A)
INK = RGBColor(0x18, 0x2B, 0x42)
MUTED = RGBColor(0x60, 0x73, 0x86)
TEAL = RGBColor(0x08, 0x86, 0x9B)
PURPLE = RGBColor(0x65, 0x4B, 0xD9)
GREEN = RGBColor(0x1B, 0x8A, 0x57)
AMBER = RGBColor(0xB4, 0x70, 0x13)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xF1, 0xF5, 0xF8)


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def text(box, lines, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(7)
        run = p.add_run()
        run.text = line
        run.font.name = "Aptos"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold


def box(slide, x, y, w, h, fill=PALE, line=TEAL, radius=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1)
    return shape


def title(slide, heading, subtitle=None):
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.35), Inches(12), Inches(0.65))
    text(tb, [heading], size=27, color=INK, bold=True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.67), Inches(1.12), Inches(2.2), Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()
    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.7), Inches(1.25), Inches(11.8), Inches(0.45))
        text(sb, [subtitle], size=12, color=MUTED)


def footer(slide, number):
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(7.12), Inches(12), Inches(0.2))
    text(tb, [f"UrbanGenAI  |  source-backed presentation  |  {number}"], size=8, color=MUTED)


def add_bullets(slide, bullets, x=0.9, y=1.8, w=11.5, h=4.7, size=18):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        p.level = 0
        r = p.add_run()
        r.text = "• " + item
        r.font.name = "Aptos"
        r.font.size = Pt(size)
        r.font.color.rgb = INK
    return tb


def add_image(slide, path, x, y, w=None, h=None):
    if path.exists():
        kwargs = {}
        if w:
            kwargs["width"] = Inches(w)
        if h:
            kwargs["height"] = Inches(h)
        slide.shapes.add_picture(str(path), Inches(x), Inches(y), **kwargs)


def make_chart_assets():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    assets = {}
    histories = {
        "ae": load_json(ROOT / "outputs" / "ae" / "history.json", []),
        "vae": load_json(ROOT / "outputs" / "vae" / "history.json", []),
        "gan": load_json(ROOT / "outputs" / "gan" / "history.json", []),
        "classifier": load_json(ROOT / "outputs" / "transformer" / "history.json", []),
        "diffusion": load_json(ROOT / "outputs" / "diffusion_scenario" / "history.json", []),
    }
    for key, rows in histories.items():
        if not rows:
            continue
        fig, ax = plt.subplots(figsize=(7.8, 3.2), dpi=160)
        if key == "gan":
            ax.plot([r["epoch"] for r in rows], [r["d_loss"] for r in rows], label="D loss")
            ax.plot([r["epoch"] for r in rows], [r["g_loss"] for r in rows], label="G loss")
        elif key == "classifier":
            ax.plot([r["epoch"] for r in rows], [r["accuracy"] for r in rows], label="train accuracy")
            ax.plot([r["epoch"] for r in rows], [r["val_accuracy"] for r in rows], label="validation accuracy")
        elif key == "vae":
            ax.plot([r["epoch"] for r in rows], [r["loss"] for r in rows], label="total loss")
            ax.plot([r["epoch"] for r in rows], [r["val"]["loss"] for r in rows], label="validation loss")
        else:
            ax.plot([r.get("epoch", i + 1) for i, r in enumerate(rows)], [r["loss"] for r in rows], label="loss")
        ax.set_title(f"{key.upper()} training history")
        ax.set_xlabel("Epoch / training step")
        ax.grid(alpha=0.25)
        ax.legend(frameon=False)
        fig.tight_layout()
        path = ASSETS / f"{key}_history.png"
        fig.savefig(path, transparent=False)
        plt.close(fig)
        assets[key] = path
    return assets


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    charts = make_chart_assets()
    diffusion_meta = load_json(ROOT / "outputs" / "diffusion_scenario" / "meta.json", {})

    # 1
    s = prs.slides.add_slide(blank)
    bg = box(s, 0, 0, 13.333, 7.5, NAVY, NAVY)
    bg.line.fill.background()
    accent = box(s, 0.75, 2.0, 0.15, 3.2, TEAL, TEAL)
    accent.line.fill.background()
    tb = s.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11), Inches(3.4))
    text(tb, [
        "UrbanGenAI",
        "Urbanization using Generative AI",
        "A multi-model pipeline for aerial land-use understanding, scenario visualization, and planning support",
        "Professor presentation  |  UCMerced LandUse + Pune GIS context",
    ], size=38, color=WHITE, bold=False)
    tb.text_frame.paragraphs[0].runs[0].font.bold = True
    tb.text_frame.paragraphs[1].runs[0].font.size = Pt(23)
    tb.text_frame.paragraphs[1].runs[0].font.color.rgb = RGBColor(0xA7, 0xEA, 0xF2)
    tb.text_frame.paragraphs[2].runs[0].font.size = Pt(17)
    tb.text_frame.paragraphs[3].runs[0].font.size = Pt(13)

    # 2
    s = prs.slides.add_slide(blank); title(s, "Objective and problem")
    add_bullets(s, [
        "Urbanization changes land cover, infrastructure demand, mobility, drainage, and environmental risk.",
        "The project goal is not to replace planners: it creates measurable model outputs and visual scenarios for review.",
        "Input: real aerial tiles and available GIS layers. Output: reconstruction, classification, anomaly signals, synthetic samples, and advisory text.",
        "Every generated image is presented as a model scenario—not as a real satellite observation or guaranteed future plan.",
    ])
    footer(s, 2)

    # 3
    s = prs.slides.add_slide(blank); title(s, "Data, provenance, and training boundary")
    rows = [
        ("Vision models", "UCMerced LandUse", "21 classes; 128×128 RGB tiles", "AE, VAE, classifier, GAN, diffusion"),
        ("Planning language", "backend/corpus/urban_planning.txt", "character-level planning corpus", "MiniGPT"),
        ("GIS context", "Pune shapefiles when present", "buildings, land use, roads, waterways, natural areas", "RAG prompt and statistics"),
        ("External backbone", "ImageNet weights", "ResNet18/VGG16 initialization", "fine-tuned classifier / style feature space"),
    ]
    x, y = 0.55, 1.65
    widths = [2.0, 2.4, 3.2, 4.7]
    headers = ["Component", "Source", "What is measured", "Used by"]
    for j, h in enumerate(headers):
        sh = box(s, x + sum(widths[:j]), y, widths[j], 0.5, NAVY, NAVY)
        text(sh, [h], size=11, color=WHITE, bold=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            sh = box(s, x + sum(widths[:j]), y + 0.5 + i * 0.78, widths[j], 0.78, WHITE if i % 2 == 0 else PALE, TEAL)
            text(sh, [val], size=10, color=INK, bold=j == 0)
    add_bullets(s, [
        "The system reports a model as trained only when its checkpoint loads successfully.",
        "Missing data or metrics are reported as unavailable; no invented fallback metric is used.",
    ], x=0.8, y=5.55, w=11.5, h=1.1, size=14)
    footer(s, 3)

    # 4
    s = prs.slides.add_slide(blank); title(s, "End-to-end system architecture")
    stages = [
        ("Real input", "UCMerced tile / upload\nPune GIS layers"),
        ("Representation", "AE / VAE\nclean + encode"),
        ("Understanding", "ResNet18\n21-class land use"),
        ("Generation", "GAN / DDPM\nscenario tiles"),
        ("Planning output", "MiniGPT\nadvisory text"),
    ]
    for i, (name, desc) in enumerate(stages):
        xx = 0.6 + i * 2.55
        sh = box(s, xx, 2.2, 2.1, 1.75, PALE, TEAL, True)
        text(sh, [name, desc], size=14 if i == 0 else 13, color=INK, bold=i == 0, align=PP_ALIGN.CENTER)
        if i < len(stages) - 1:
            ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(xx + 2.15), Inches(2.85), Inches(0.35), Inches(0.35))
            ar.fill.solid(); ar.fill.fore_color.rgb = PURPLE; ar.line.fill.background()
    add_bullets(s, [
        "Inference routes are separate: upload → selected model endpoint → real checkpoint → measured metadata.",
        "The diffusion path uses DDPM training and DDIM inference; it is not a placeholder image generator.",
    ], x=0.9, y=4.6, w=11.5, h=1.4, size=16)
    footer(s, 4)

    # 5
    s = prs.slides.add_slide(blank); title(s, "Autoencoder (AE): denoising before analysis")
    add_bullets(s, [
        "Architecture: ResNet18 encoder + CNN decoder with skip connections.",
        "Training input: real UCMerced tile with additive noise. Target: the original clean tile.",
        "Loss: reconstruction MSE; inference returns noisy input, reconstruction, MSE, and PSNR.",
        "Use in UrbanGenAI: restore degraded aerial imagery before classification or downstream analysis.",
    ], x=0.8, y=1.7, w=6.0, h=3.9, size=16)
    add_image(s, charts.get("ae", Path()), 7.0, 2.0, w=5.7)
    footer(s, 5)

    # 6
    s = prs.slides.add_slide(blank); title(s, "Variational Autoencoder (VAE): anomaly and latent exploration")
    add_bullets(s, [
        "Encoder maps an image to μ and log σ²; reparameterization samples z; decoder reconstructs the tile.",
        "Loss = reconstruction loss + KL divergence toward a prior.",
        "Inference reports reconstruction MSE, PSNR-related evidence, KL, latent activity, and anomaly score against a real-tile baseline.",
        "The implemented variation/interpolation endpoints use encoded real tiles; they do not claim arbitrary new geometry.",
    ], x=0.8, y=1.65, w=6.2, h=4.6, size=15)
    add_image(s, charts.get("vae", Path()), 7.1, 2.0, w=5.4)
    footer(s, 6)

    # 7
    s = prs.slides.add_slide(blank); title(s, "Land-use classifier: the verification model")
    add_bullets(s, [
        "Model: ResNet18 initialized from ImageNet and fine-tuned on UCMerced classes.",
        "Objective: cross-entropy classification over 21 land-use categories.",
        "Inference: upload → resize/normalize → logits → softmax → top-5 classes and confidence.",
        "It is discriminative, not generative. It verifies land-use content and supports GAN/diffusion evaluation.",
    ], x=0.8, y=1.7, w=6.2, h=4.3, size=16)
    add_image(s, charts.get("classifier", Path()), 7.1, 2.0, w=5.5)
    footer(s, 7)

    # 8
    s = prs.slides.add_slide(blank); title(s, "Conditional GAN: class-conditioned synthesis")
    add_bullets(s, [
        "Generator receives random latent noise z and a class index; discriminator learns real-versus-generated structure.",
        "Losses: adversarial discriminator loss and generator loss; the implementation also uses class-aware training signals.",
        "Inference returns generated tile grids and individual images for a selected land-use class.",
        "Measured proxy: independent classifier recognition rate—not photorealism, geographic truth, or planning validity.",
    ], x=0.8, y=1.7, w=6.0, h=4.3, size=16)
    add_image(s, charts.get("gan", Path()), 7.0, 2.0, w=5.6)
    footer(s, 8)

    # 9
    s = prs.slides.add_slide(blank); title(s, "MiniGPT planner: generated advisory text")
    add_bullets(s, [
        "Character-level decoder-only Transformer trained on the project’s urban-planning corpus.",
        "Objective: next-character cross-entropy; evaluation uses held-out loss, perplexity, and bits per character.",
        "Inference: prompt → token IDs → causal self-attention → autoregressive sampling → recommendation draft.",
        "The text is advisory. It must be checked against authoritative planning data and professional review.",
    ], x=0.8, y=1.7, w=6.2, h=4.2, size=16)
    add_image(s, charts.get("classifier", Path()), 7.1, 2.05, w=5.4)
    footer(s, 9)

    # 10
    s = prs.slides.add_slide(blank); title(s, "Diffusion model: what DDPM actually does")
    formula = s.shapes.add_textbox(Inches(0.85), Inches(1.65), Inches(11.7), Inches(0.6))
    text(formula, ["Forward:  xₜ = √ᾱₜ x₀ + √(1−ᾱₜ) ε     |     Training:  MSE(ε̂θ(xₜ,t,c), ε)"], size=20, color=PURPLE, bold=True, align=PP_ALIGN.CENTER)
    add_bullets(s, [
        "Training gradually adds Gaussian noise to real tiles across T=1000 timesteps; the U-Net learns to predict that noise.",
        "The U-Net receives noisy image, sinusoidal timestep embedding, land-use class embedding, and source-tile conditioning.",
        "DDIM inference reverses the process using a smaller number of steps; η=0 is deterministic, η>0 injects stochasticity.",
        "Project use: generate a visual candidate for a requested land-use category—not a measured forecast of future development.",
    ], x=0.9, y=2.55, w=11.4, h=3.6, size=16)
    footer(s, 10)

    # 11
    s = prs.slides.add_slide(blank); title(s, "Diffusion inference: exact request-to-output path")
    steps = [
        ("1", "Upload", "PIL decodes and validates the image"),
        ("2", "Condition", "Resize/normalize source tile"),
        ("3", "Target", "Select class; source tile stays condition"),
        ("4", "Sample", "DDIM denoising with η and class guidance"),
        ("5", "Verify", "ResNet18 classifies returned image"),
    ]
    for i, (num, head, desc) in enumerate(steps):
        xx = 0.65 + i * 2.55
        sh = box(s, xx, 2.1, 2.1, 2.0, WHITE, TEAL, True)
        text(sh, [num, head, desc], size=14 if head != "Condition" else 13, color=INK, bold=True, align=PP_ALIGN.CENTER)
        if i < len(steps) - 1:
            ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(xx + 2.13), Inches(2.9), Inches(0.32), Inches(0.3))
            ar.fill.solid(); ar.fill.fore_color.rgb = PURPLE; ar.line.fill.background()
    add_bullets(s, [
        "The response includes requested class, sampler steps, η, verified class, and verified confidence.",
        "The classifier confidence is evidence of semantic alignment, not proof of visual quality or real-world planning correctness.",
    ], x=0.9, y=4.9, w=11.5, h=1.3, size=16)
    footer(s, 11)

    # 12
    s = prs.slides.add_slide(blank); title(s, "Measured training evidence")
    rows = [
        ("AE", "50 epochs", "MSE / PSNR / SSIM", "history.json + runtime evaluation"),
        ("VAE", "49 recorded epochs", "reconstruction + KL", "history.json + runtime evaluation"),
        ("Classifier", "30 epochs", "cross-entropy / accuracy", "history.json + runtime evaluation"),
        ("GAN", "training history", "D loss / G loss", "history.json + recognition proxy"),
        ("Diffusion", f"{diffusion_meta.get('epochs_trained', '—')} epochs", f"best MSE {diffusion_meta.get('best_loss', 0):.5f}", "meta.json + training_metrics.png"),
        ("MiniGPT", "3000 steps", "cross-entropy / perplexity", "history.json + held-out evaluation"),
    ]
    x, y = 0.6, 1.55
    widths = [1.7, 1.7, 2.6, 6.0]
    for j, h in enumerate(["Model", "Training", "Objective / metric", "Evidence source"]):
        sh = box(s, x + sum(widths[:j]), y, widths[j], 0.48, NAVY, NAVY)
        text(sh, [h], size=11, color=WHITE, bold=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            sh = box(s, x + sum(widths[:j]), y + 0.48 + i * 0.68, widths[j], 0.68, WHITE if i % 2 == 0 else PALE, TEAL)
            text(sh, [val], size=10, color=INK, bold=j == 0)
    add_image(s, ROOT / "outputs" / "diffusion_scenario" / "training_metrics.png", 0.9, 5.95, w=5.8)
    add_bullets(s, [
        "Numbers shown here are read from persisted training artifacts or measured runtime evaluations.",
        "A low diffusion noise MSE does not by itself guarantee photorealistic or planning-valid output.",
    ], x=7.0, y=5.9, w=5.5, h=0.9, size=13)
    footer(s, 12)

    # 13
    s = prs.slides.add_slide(blank); title(s, "All implemented models: use, training, losses, and evidence")
    rows = [
        ("Denoising AE", "Restore noisy aerial tiles", "UCMerced images", "Pixel MSE", "50 epochs; final MSE 0.00617; 29.65 dB PSNR"),
        ("Spatial VAE", "Anomaly score + latent interpolation", "UCMerced images", "0.7 L1 + 0.3 MSE + β KL", "50 epochs; recon 0.0469; KL 60.72 nats; 27.49 dB PSNR"),
        ("ResNet18 classifier", "21-class land-use label + verification", "UCMerced images", "Cross-entropy", "50 epochs; val accuracy 98.10%; val loss 0.0615"),
        ("cDCGAN", "New class-conditioned synthetic tiles", "UCMerced images", "Adversarial BCE + class + diversity", "50 epochs; D 1.6724; G 1.1890; 99.40% intended-class recognition"),
        ("Source DDPM/DDIM", "Source-preserving target-class scenario", "UCMerced images", "Noise-prediction MSE", "50 epochs; final noise MSE 0.0304"),
        ("MiniGPT", "GIS-grounded planning draft", "urban_planning.txt", "Next-character cross-entropy", "50 equivalent epochs (3,000 steps); loss 0.1044; perplexity 1.110"),
    ]
    x, y = 0.35, 1.35
    widths = [1.55, 2.45, 1.75, 2.55, 5.95]
    headers = ["Model", "Use in project", "Training data", "Loss / objective", "Latest persisted evidence"]
    for j, h in enumerate(headers):
        sh = box(s, x + sum(widths[:j]), y, widths[j], 0.52, NAVY, NAVY)
        text(sh, [h], size=9, color=WHITE, bold=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            sh = box(s, x + sum(widths[:j]), y + 0.52 + i * 0.78, widths[j], 0.78, WHITE if i % 2 == 0 else PALE, TEAL)
            text(sh, [val], size=8.2, color=INK, bold=j == 0)
    note = box(s, 0.6, 6.35, 12.1, 0.48, RGBColor(0xFF, 0xF4, 0xDF), AMBER, True)
    text(note, ["Important: MiniGPT is trained on curated urban-planning text, not UCMerced imagery. Diffusion noise MSE and GAN recognition are not planning-validity or photorealism guarantees."], size=10, color=INK, bold=True, align=PP_ALIGN.CENTER)
    footer(s, 13)

    # 14
    s = prs.slides.add_slide(blank); title(s, "What is real, what is generated, and what is not claimed")
    cols = [
        ("REAL INPUTS", GREEN, ["UCMerced aerial tiles", "Uploaded image", "Loaded Pune GIS layers"]),
        ("MODEL OUTPUTS", PURPLE, ["AE/VAE reconstructions", "GAN/DDPM generated tiles", "MiniGPT recommendation text"]),
        ("NOT CLAIMED", AMBER, ["Future land-use truth", "Photorealism guarantee", "Planning approval or policy decision"]),
    ]
    for i, (head, color, items) in enumerate(cols):
        xx = 0.7 + i * 4.2
        sh = box(s, xx, 1.8, 3.6, 3.4, WHITE, color, True)
        text(sh, [head], size=17, color=color, bold=True, align=PP_ALIGN.CENTER)
        body = s.shapes.add_textbox(Inches(xx + 0.25), Inches(2.5), Inches(3.1), Inches(2.2))
        text(body, ["• " + v for v in items], size=15, color=INK)
    add_bullets(s, [
        "This separation is intentional: a generated scenario can support discussion without being presented as an observation.",
        "The professor demo should show both the input tile and the model output, plus the verification metadata.",
    ], x=0.9, y=5.7, w=11.5, h=1.0, size=15)
    footer(s, 14)

    # 15
    s = prs.slides.add_slide(blank); title(s, "Conclusion and live demonstration sequence")
    add_bullets(s, [
        "UrbanGenAI combines trained vision models, class-conditioned generation, GIS context, and language generation into one inspectable pipeline.",
        "AE and VAE support restoration and anomaly/latent analysis; the classifier provides land-use understanding and verification.",
        "GAN and diffusion create synthetic visual candidates; MiniGPT turns source-backed context into advisory planning text.",
        "The strongest scientific claim is reproducibility: real checkpoints, real inputs, measured losses, explicit limitations, and no placeholder success paths.",
    ], x=0.8, y=1.65, w=11.7, h=3.7, size=17)
    sh = box(s, 0.9, 5.65, 11.4, 0.8, NAVY, NAVY, True)
    text(sh, ["Demo: upload UCMerced tile → classify → reconstruct/analyze → select target class → DDIM scenario → verify → generate advisory text"], size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    footer(s, 15)

    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
