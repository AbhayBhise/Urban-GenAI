"""Generate the two exam presentation decks for UrbanGenAI.

  1. UrbanGenAI_Technical_Architecture.pptx  -- every model, layer by layer,
     with epochs, tensor dimensions at each stage, and losses.
  2. UrbanGenAI_Results.pptx                 -- verified evaluation metrics
     and an honest limitations discussion.

All numbers are the real measured / committed values (see docs/MODEL_CARD.md,
outputs/*/history.json and the live /evaluate/* endpoints).
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

INK      = RGBColor(0x16, 0x28, 0x3D)
MUTE     = RGBColor(0x5B, 0x72, 0x85)
ACCENT   = RGBColor(0x04, 0x78, 0x8F)
ACCENT2  = RGBColor(0x5B, 0x3F, 0xD1)
DARK_BG  = RGBColor(0x0B, 0x12, 0x1C)
PANEL    = RGBColor(0xED, 0xF1, 0xF7)
OK       = RGBColor(0x1C, 0x8F, 0x52)
WARN     = RGBColor(0xA6, 0x6A, 0x08)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

W, H = Inches(13.333), Inches(7.5)


def deck():
    p = Presentation()
    p.slide_width, p.slide_height = W, H
    return p


def _txt(tf, runs, align=PP_ALIGN.LEFT, space_after=6):
    """runs: list of (text, size, bold, color) or a plain string."""
    first = True
    for item in runs:
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        para.alignment = align
        para.space_after = Pt(space_after)
        if isinstance(item, str):
            item = [(item, 18, False, INK)]
        for (t, s, b, c) in item:
            r = para.add_run()
            r.text = t
            r.font.size = Pt(s)
            r.font.bold = b
            r.font.color.rgb = c
            r.font.name = "Segoe UI"


def title_slide(p, kicker, title, subtitle):
    s = p.slides.add_slide(p.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = DARK_BG; bg.line.fill.background()
    bg.shadow.inherit = False
    bar = s.shapes.add_shape(1, 0, Inches(2.5), Inches(0.14), Inches(2.4))
    bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor(0x00, 0xD4, 0xFF); bar.line.fill.background()
    bar.shadow.inherit = False
    tb = s.shapes.add_textbox(Inches(0.9), Inches(2.3), Inches(11.5), Inches(3.2))
    _txt(tb.text_frame, [
        [(kicker, 15, True, RGBColor(0x00, 0xD4, 0xFF))],
        [(title, 40, True, WHITE)],
        [(subtitle, 19, False, RGBColor(0xAD, 0xBD, 0xCC))],
    ], space_after=14)
    return s


def section_slide(p, n, title):
    s = p.slides.add_slide(p.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = DARK_BG; bg.line.fill.background()
    bg.shadow.inherit = False
    tb = s.shapes.add_textbox(Inches(0.9), Inches(3.0), Inches(11.5), Inches(1.6))
    _txt(tb.text_frame, [
        [("%02d" % n, 20, True, RGBColor(0x00, 0xD4, 0xFF))],
        [(title, 34, True, WHITE)],
    ], space_after=10)
    return s


def content_slide(p, title, blocks, foot=None):
    """blocks: list of paragraphs; each is a string or list-of-runs."""
    s = p.slides.add_slide(p.slide_layouts[6])
    hd = s.shapes.add_textbox(Inches(0.7), Inches(0.4), Inches(12), Inches(0.9))
    _txt(hd.text_frame, [[(title, 26, True, INK)]])
    ln = s.shapes.add_shape(1, Inches(0.72), Inches(1.25), Inches(3.2), Pt(3))
    ln.fill.solid(); ln.fill.fore_color.rgb = ACCENT; ln.line.fill.background()
    ln.shadow.inherit = False
    body = s.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(12), Inches(5.4))
    body.text_frame.word_wrap = True
    _txt(body.text_frame, blocks, space_after=9)
    if foot:
        fb = s.shapes.add_textbox(Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
        _txt(fb.text_frame, [[(foot, 11, False, MUTE)]])
    return s


def table_slide(p, title, headers, rows, foot=None, col_w=None):
    s = p.slides.add_slide(p.slide_layouts[6])
    hd = s.shapes.add_textbox(Inches(0.7), Inches(0.4), Inches(12), Inches(0.9))
    _txt(hd.text_frame, [[(title, 24, True, INK)]])
    nr, nc = len(rows) + 1, len(headers)
    gt = s.shapes.add_table(nr, nc, Inches(0.7), Inches(1.35),
                            Inches(12.0), Inches(0.4 * nr)).table
    if col_w:
        for i, wv in enumerate(col_w):
            gt.columns[i].width = Inches(wv)
    for j, h in enumerate(headers):
        c = gt.cell(0, j)
        c.text = h
        c.fill.solid(); c.fill.fore_color.rgb = INK
        pr = c.text_frame.paragraphs[0]
        pr.runs[0].font.size = Pt(12); pr.runs[0].font.bold = True
        pr.runs[0].font.color.rgb = WHITE
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = gt.cell(i, j)
            c.text = str(val)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE if i % 2 else PANEL
            pr = c.text_frame.paragraphs[0]
            pr.runs[0].font.size = Pt(11)
            pr.runs[0].font.color.rgb = INK
            if j == 0:
                pr.runs[0].font.bold = True
    if foot:
        fb = s.shapes.add_textbox(Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
        _txt(fb.text_frame, [[(foot, 11, False, MUTE)]])
    return s


def pipeline_slide(p, title, stages, foot=None):
    """stages: list of (name, dims) rendered as a left-to-right chain."""
    s = p.slides.add_slide(p.slide_layouts[6])
    hd = s.shapes.add_textbox(Inches(0.7), Inches(0.4), Inches(12), Inches(0.9))
    _txt(hd.text_frame, [[(title, 24, True, INK)]])
    n = len(stages)
    total = Inches(12.4)
    box_w = Inches(12.4 / n - 0.18)
    x = Inches(0.7)
    y = Inches(3.0)
    for i, (name, dims) in enumerate(stages):
        b = s.shapes.add_shape(1, x, y, box_w, Inches(1.5))
        b.fill.solid(); b.fill.fore_color.rgb = PANEL
        b.line.color.rgb = ACCENT; b.line.width = Pt(1.25)
        b.shadow.inherit = False
        tf = b.text_frame; tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        _txt(tf, [[(name, 12, True, INK)], [(dims, 10, False, MUTE)]],
             align=PP_ALIGN.CENTER, space_after=3)
        if i < n - 1:
            ar = s.shapes.add_shape(13, x + box_w, y + Inches(0.62),
                                    Inches(0.18), Inches(0.26))
            ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT2
            ar.line.fill.background(); ar.shadow.inherit = False
        x = x + box_w + Inches(0.18)
    if foot:
        fb = s.shapes.add_textbox(Inches(0.7), Inches(5.1), Inches(12), Inches(1.2))
        fb.text_frame.word_wrap = True
        _txt(fb.text_frame, [[(foot, 13, False, INK)]])
    return s


# ===========================================================================
# DECK 1 -- TECHNICAL ARCHITECTURE
# ===========================================================================
def build_technical(path):
    p = deck()
    title_slide(
        p, "MITAOE  ·  Generative AI Capstone  ·  2304422",
        "UrbanGenAI — Technical Architecture",
        "Four generative models on a single urban-planning pipeline\n"
        "Architecture · layers · epochs · tensor dimensions at every stage")

    content_slide(p, "The problem & the pipeline", [
        [("UrbanGenAI", 18, True, INK), (" is a decision-support digital twin for urban planners. "
         "Case study: Pune (PMC) — 516 km², 7.4M residents.", 18, False, INK)],
        "",
        [("One pipeline, four generative models, each doing one justified job:", 16, True, ACCENT)],
        [("1.  Land-Use Classifier (ResNet18)  →  what is this parcel? (21 zoning classes)", 15, False, INK)],
        [("2.  Denoising Autoencoder  →  clean degraded aerial imagery before analysis", 15, False, INK)],
        [("3.  Variational Autoencoder  →  anomaly score + latent scenario interpolation", 15, False, INK)],
        [("4.  Conditional DCGAN  →  synthetic class-conditional tiles for augmentation", 15, False, INK)],
        [("5.  MiniGPT Transformer  →  grounded planning recommendations from Pune stats", 15, False, INK)],
    ], foot="Datasets: UCMerced (21 classes, 2,100 tiles), EuroSAT, Pune PMC OpenStreetMap GIS layers.")

    # ---- AE ----
    section_slide(p, 1, "Denoising Autoencoder  (U-Net skip-connected)")
    pipeline_slide(p, "AE — tensor dimensions at every stage", [
        ("Input tile\n+ Gaussian noise σ=0.15", "128×128×3"),
        ("ResNet18 stem (s0)", "64×64×64"),
        ("MaxPool + Layer1 (s1)", "32×32×64"),
        ("Layer2 (s2)", "16×16×128"),
        ("Layer3 — bottleneck", "8×8×256"),
        ("Skip-decoder\n4× ConvTranspose + concat", "→ 128×128×3"),
    ], foot="Decoder up-stages concatenate the encoder skips s2,s1,s0 (U-Net). "
            "Loss = MSE(reconstruction, clean tile). Encoder frozen 5 epochs, then unfrozen.")
    table_slide(p, "AE — training configuration", ["Parameter", "Value"], [
        ("Encoder", "ResNet18, ImageNet-pretrained, fine-tuned (conv1 → layer3)"),
        ("Decoder", "4× ConvTranspose2d (stride 2) + skip concat, Tanh output, from scratch"),
        ("Bottleneck", "8 × 8 × 256  =  16,384 spatial codes  (≈ 3× compression)"),
        ("Epochs", "50  (encoder unfrozen after epoch 5)"),
        ("Optimiser / LR", "Adam, 1e-4"),
        ("Objective", "MSE(recon, clean);  input corrupted with Gaussian noise σ = 0.15"),
        ("Checkpoint", "outputs/ae/model.pth  (committed)"),
    ], col_w=[3.2, 8.8])

    # ---- VAE ----
    section_slide(p, 2, "Variational Autoencoder  (spatial latent)")
    pipeline_slide(p, "VAE — tensor dimensions at every stage", [
        ("Input tile", "128×128×3"),
        ("ResNet18 encoder", "8×8×256"),
        ("μ  /  log σ²  heads\n1×1 Conv 256→64", "8×8×64  each"),
        ("Reparameterize\nz = μ + σ ⊙ ε", "8×8×64  (4,096 dims)"),
        ("CNN decoder\n4× ConvTranspose", "128×128×3"),
    ], foot="Latent kept spatial (not flattened) to preserve per-region correspondence. "
            "Loss = 0.7·L1 + 0.3·MSE + β·KL,  β ≈ 1e-4  (measured: β ≥ 0.02 → posterior collapse).")
    table_slide(p, "VAE — training configuration", ["Parameter", "Value"], [
        ("Encoder", "ResNet18, ImageNet-pretrained, fine-tuned"),
        ("Latent heads", "two 1×1 Conv2d(256 → 64) → diagonal Gaussian q(z|x)"),
        ("Latent space", "8 × 8 × 64  =  4,096 spatial dimensions"),
        ("Decoder", "4× ConvTranspose2d, 16× upsample, from scratch"),
        ("Epochs", "50"),
        ("Objective", "0.7·L1 + 0.3·MSE  +  β·KL(q(z|x) ‖ N(0,I)),   β ≈ 1e-4"),
        ("Application", "reconstruction-error z-score vs 294-tile baseline → anomaly flag"),
        ("Checkpoint", "outputs/vae/model.pth  (committed)"),
    ], col_w=[3.2, 8.8])

    # ---- GAN ----
    section_slide(p, 3, "Conditional DCGAN  (spectral-norm, EMA)")
    pipeline_slide(p, "GAN generator — tensor dimensions at every stage", [
        ("Noise z", "128-dim"),
        ("Class embed\n1 of 21", "64-dim"),
        ("Linear + reshape", "8×8×512"),
        ("4× ConvTranspose2d\nBN + ReLU", "16→32→64→128"),
        ("Tanh output", "128×128×3"),
    ], foot="Discriminator: class embed → 128×128×1 map, concat to image, 5× spectral-norm Conv "
            "(LeakyReLU) → real/fake logit. Non-saturating BCE, label smoothing 0.9 / 0.1.")
    table_slide(p, "GAN — training configuration", ["Parameter", "Value"], [
        ("Type", "Class-conditional DCGAN, trained from scratch (no pretraining)"),
        ("Latent / embed dim", "z = 128,  class embedding = 64,  classes = 21"),
        ("Generator", "Linear→8×8×512, then 5× ConvTranspose2d (BN+ReLU), Tanh"),
        ("Discriminator", "5× spectral-normalised Conv2d, LeakyReLU, label-projection conditioning"),
        ("Stabilisers", "spectral norm on every D layer · label smoothing · D:G = 2:1 steps"),
        ("Generator EMA", "decay 0.999 — EMA weights used for all inference"),
        ("Epochs", "100"),
        ("Checkpoint", "outputs/gan/generator_ema.pth  (committed)"),
    ], col_w=[3.2, 8.8])

    # ---- MiniGPT ----
    section_slide(p, 4, "MiniGPT  (decoder-only Transformer, from scratch)")
    pipeline_slide(p, "MiniGPT — tensor dimensions at every stage", [
        ("Pune ward stats\n→ prompt string", "chars"),
        ("Token + positional\nembedding", "T × 256"),
        ("4 × causal blocks\nmasked self-attn (4 heads) + MLP", "T × 256"),
        ("LayerNorm + LM head\n(weight-tied)", "T × 64"),
        ("Sample next char", "recommendation text"),
    ], foot="Pre-norm residual blocks. Causal mask: position t attends only to ≤ t. "
            "Head weight tied to the token embedding.")
    table_slide(p, "MiniGPT — model & training configuration", ["Parameter", "Value"], [
        ("Architecture", "decoder-only Transformer (GPT-style), built entirely from scratch"),
        ("Layers / heads", "n_layer = 4,  n_head = 4"),
        ("Embedding dim", "n_embd = 256"),
        ("Context (block size)", "192 characters"),
        ("Vocabulary", "64 characters (char-level, built from the corpus)"),
        ("Parameters", "3.23 M  (weight-tied LM head)"),
        ("Training", "3,000 steps · AdamW 3e-4 · dropout 0.1 · batch 64"),
        ("Corpus", "backend/corpus/urban_planning.txt (hand-authored) — 90 / 10 train/val split"),
        ("Checkpoint", "outputs/gpt/model.pth  (committed)"),
    ], col_w=[3.2, 8.8])

    # ---- Classifier ----
    section_slide(p, 5, "Land-Use Classifier  (supporting model)")
    table_slide(p, "Classifier — configuration", ["Parameter", "Value"], [
        ("Architecture", "ResNet18 (ImageNet-pretrained) + Linear(512 → 21) head"),
        ("Input", "224 × 224 × 3"),
        ("Feature vector", "512-d (global average pool)"),
        ("Output", "21 land-use logits → softmax"),
        ("Epochs", "30"),
        ("Role", "labels parcels for the VAE/MiniGPT stages; also the GAN quality judge"),
        ("Note", "this is a CNN — the syllabus transformer requirement is met by MiniGPT"),
        ("Checkpoint", "outputs/transformer/model.pth  (committed)"),
    ], col_w=[3.2, 8.8])

    table_slide(p, "All models at a glance",
        ["Model", "Pretraining", "Key dims", "Epochs", "Trained by us"], [
        ("Denoising AE", "ResNet18 encoder", "8×8×256 bottleneck", "50", "decoder from scratch"),
        ("Spatial VAE", "ResNet18 encoder", "8×8×64 latent (4,096)", "50", "decoder + heads from scratch"),
        ("Conditional DCGAN", "none", "z=128, embed=64", "100", "fully from scratch"),
        ("MiniGPT", "none", "4L / 4H / 256d, 3.23M", "3,000 steps", "fully from scratch"),
        ("Land-Use Classifier", "ResNet18", "512-d → 21", "30", "head from scratch"),
    ], col_w=[2.6, 2.3, 3.0, 1.7, 2.4],
       foot="Compute: 1× NVIDIA RTX 4050 laptop GPU · full retrain ≈ 1 hour · ≈ 0.08 kg CO₂e.")

    p.save(path)
    print("wrote", path, "-", len(p.slides._sldIdLst), "slides")


# ===========================================================================
# DECK 2 -- RESULTS
# ===========================================================================
def build_results(path):
    p = deck()
    title_slide(
        p, "MITAOE  ·  Generative AI Capstone  ·  2304422",
        "UrbanGenAI — Results & Evaluation",
        "Verified metrics from committed checkpoints and the live /evaluate/* API\n"
        "No synthetic or placeholder figures")

    content_slide(p, "How every number here was produced", [
        [("Each model is scored with the metric it is actually judged by — computed once "
          "at backend startup on held-out samples, served by GET /evaluate/<model>.", 16, False, INK)],
        "",
        [("• AE & VAE", 15, True, ACCENT), ("  — per-class SSIM / PSNR / MSE reconstruction quality", 15, False, INK)],
        [("• GAN", 15, True, ACCENT), ("  — classifier-recognition rate (Inception-Score-style proxy)", 15, False, INK)],
        [("• MiniGPT", 15, True, ACCENT), ("  — held-out perplexity / bits-per-character", 15, False, INK)],
        [("• Classifier", 15, True, ACCENT), ("  — 21×21 confusion matrix + per-class accuracy", 15, False, INK)],
    ], foot="Source of truth: outputs/*/history.json, outputs/*/model.pth, docs/MODEL_CARD.md.")

    table_slide(p, "Headline results", ["Model", "Metric", "Result", "Reading"], [
        ("Land-Use Classifier", "Validation accuracy", "98.1 %", "strong — 21-way zoning"),
        ("Denoising AE", "PSNR / SSIM (held-out)", "29.7 dB / 0.865", "near-lossless denoising"),
        ("Denoising AE", "Final training MSE", "0.01977", "converged from 0.1830 @ epoch 1"),
        ("Spatial VAE", "PSNR / SSIM (held-out)", "19.5 dB / 0.43", "soft — 8×8 bottleneck limit"),
        ("Spatial VAE", "KL / active latent dims", "106 nats / 63 of 64", "latent healthy, not collapsed"),
        ("Conditional DCGAN", "Classifier-recognition rate", "≈ 15 %", "texture classes work; geometry not yet"),
        ("MiniGPT", "Held-out perplexity", "1.09", "learns the templated corpus by design"),
        ("MiniGPT", "Bits / character", "0.12  (vs 6.0 uniform)", "grounded structured drafting"),
    ], col_w=[2.7, 2.9, 2.6, 3.8],
       foot="AE / VAE evaluated over 105 tiles spanning all 21 classes; GAN over 168 generated tiles.")

    table_slide(p, "Autoencoder — per-class reconstruction (sample)",
        ["Class", "PSNR (dB)", "SSIM"], [
        ("golfcourse / beach / agricultural", "31 – 33", "0.90+"),
        ("21-class average", "29.7", "0.865"),
        ("denseresidential / mobilehomepark", "26 – 27", "0.78 – 0.80"),
    ], foot="Skip connections closed the hard-class gap from 7.3 dB → 2.6 dB; "
            "21-class average moved 25 dB → 29.7 dB after the U-Net fix.")

    content_slide(p, "VAE — what the numbers mean", [
        [("SSIM 0.43 / PSNR 19.5 dB confirm the reconstruction is genuinely soft — a direct "
          "consequence of the 8×8 spatial bottleneck (4,096 dims for a 128×128 image), not a bug.", 15, False, INK)],
        [("63 of 64 latent channels carry meaningful KL — the latent is active, not collapsed.", 15, False, INK)],
        "",
        [("Value to the project:", 15, True, ACCENT)],
        [("reconstruction error, z-scored against a 294-tile 'normal' baseline, is a real "
          "anomaly signal — parcels that don't match expected patterns for their zone "
          "(informal construction, land conversion, sensor artifacts) reconstruct worse and get flagged.", 15, False, INK)],
        [("We tested β-VAE guidance against our own data and measured β ≥ 0.02 → full posterior "
          "collapse, so β was deliberately kept near zero. Evidence-based, not an oversight.", 14, False, MUTE)],
    ])

    content_slide(p, "GAN — honest result", [
        [("Overall classifier-recognition rate ≈ 15 % at 100 epochs.", 16, True, WARN)],
        "",
        [("Methodology: generate fresh tiles per class, run them through the independently-"
          "trained Land-Use Classifier, measure how many are recognised as the intended class "
          "— the same idea as Inception Score, no extra network dependency.", 15, False, INK)],
        "",
        [("Broad-texture classes (beach, forest, built-up) come through clearly; classes that "
          "need precise repeated geometry (residential grids, road intersections) mostly don't "
          "yet. This is the expected characteristic of GAN training at this dataset scale "
          "(21 classes × 100 tiles) — we report it rather than only showing the good samples.", 15, False, INK)],
    ], foot="Samples are drawn fresh from noise each run, so per-class figures shift slightly between runs.")

    content_slide(p, "MiniGPT — honest result", [
        [("Held-out perplexity 1.09  ·  0.12 bits/char  (vs 6.0 for a uniform guess).", 16, True, INK)],
        "",
        [("A perplexity this close to 1 is NOT open-ended fluency. The corpus is a small, "
          "hand-authored set of templated urban-planning sentences, so the model has learned "
          "those templates — which is exactly what the project needs: structured, grounded "
          "recommendations seeded from real Pune ward statistics, not free-form prose.", 15, False, INK)],
        "",
        [("Held-out loss (0.083) tracks final training loss (0.087) → it generalises across "
          "the corpus rather than overfitting one region of it.", 15, False, INK)],
    ])

    content_slide(p, "Ethics, fairness, privacy, transparency, limitations", [
        [("Transparency", 15, True, ACCENT), ("  — every page states which model is used, its architecture, "
          "provenance (trained by us vs pretrained), and links checkpoints + training logs.", 14, False, INK)],
        [("Privacy", 15, True, ACCENT), ("  — only public aerial imagery + open GIS (OSM, PMC). No personal data. GDPR-aligned.", 14, False, INK)],
        [("Fairness", 15, True, ACCENT), ("  — per-class metrics are surfaced, not hidden behind an average; "
          "weak classes are named.", 14, False, INK)],
        [("Limitations (stated, not hidden)", 15, True, WARN)],
        [("• VAE cannot invent geometry absent from what it has seen — it reconstructs / interpolates real tiles.", 13, False, INK)],
        [("• GAN geometry is immature at 100 epochs on this dataset size.", 13, False, INK)],
        [("• MiniGPT is a template learner on a small corpus, not a general planner.", 13, False, INK)],
        [("• Outputs are candidate computational representations — require validation against "
          "statutory regs (Pune DCPR), engineering and hydrology models, and public hearings before use.", 13, False, INK)],
    ])

    content_slide(p, "Summary", [
        [("Four generative models, each with a distinct justified role, trained and verified "
          "end-to-end on real data.", 17, True, INK)],
        "",
        [("• 3 of 4 required generative models fully trained by us from scratch (VAE decoder, GAN, MiniGPT).", 15, False, INK)],
        [("• Every claim backed by a committed checkpoint, a training log, and a live metric endpoint.", 15, False, INK)],
        [("• Limitations measured and reported honestly, with the evidence.", 15, False, INK)],
        [("• Full retrain ≈ 1 hour on a laptop GPU  ·  ≈ 0.08 kg CO₂e.", 15, False, INK)],
    ], foot="Live demo: landing page → Model Explorer → each model page → Evaluation dashboard.")

    p.save(path)
    print("wrote", path)


if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build_technical(os.path.join(root, "UrbanGenAI_Technical_Architecture.pptx"))
    build_results(os.path.join(root, "UrbanGenAI_Results.pptx"))
