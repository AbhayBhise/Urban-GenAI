"""Generate the single combined UrbanGenAI exam presentation.

Slide sequence (as requested):
  1. Project title
  2. Problem statement
  3. Objectives
  4. Outcome
  5. Literature review table (IEEE journal papers)
  6. System architecture diagram (+ layer / epoch / dimension detail)
  7. Implementation result display (verified metrics)
  8. Output (example model outputs)
  9. Conclusion

Plain English. All numbers are the real committed / measured values.
Output: UrbanGenAI_Presentation.pptx  (in the project root)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

INK     = RGBColor(0x16, 0x28, 0x3D)
MUTE    = RGBColor(0x5B, 0x72, 0x85)
ACCENT  = RGBColor(0x04, 0x78, 0x8F)
ACCENT2 = RGBColor(0x5B, 0x3F, 0xD1)
DARK_BG = RGBColor(0x0B, 0x12, 0x1C)
PANEL   = RGBColor(0xED, 0xF1, 0xF7)
OK      = RGBColor(0x1C, 0x8F, 0x52)
WARN    = RGBColor(0xA6, 0x6A, 0x08)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
CYAN    = RGBColor(0x00, 0xD4, 0xFF)

W, H = Inches(13.333), Inches(7.5)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(
    os.environ.get("TEMP", "/tmp"),
    "claude", "f--PROJECTS-GEN-AI-PROJECT-UrbanGenAI",
    "13b7bb0d-700a-48e4-8f72-30d6a5074cea", "scratchpad")


def _txt(tf, blocks, align=PP_ALIGN.LEFT, space_after=8):
    first = True
    for item in blocks:
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


def header(s, title):
    hd = s.shapes.add_textbox(Inches(0.7), Inches(0.38), Inches(12), Inches(0.9))
    _txt(hd.text_frame, [[(title, 26, True, INK)]])
    ln = s.shapes.add_shape(1, Inches(0.72), Inches(1.22), Inches(3.0), Pt(3))
    ln.fill.solid(); ln.fill.fore_color.rgb = ACCENT; ln.line.fill.background()
    ln.shadow.inherit = False


def blank(p):
    return p.slides.add_slide(p.slide_layouts[6])


def title_slide(p):
    s = blank(p)
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = DARK_BG; bg.line.fill.background()
    bg.shadow.inherit = False
    bar = s.shapes.add_shape(1, 0, Inches(2.35), Inches(0.16), Inches(2.7))
    bar.fill.solid(); bar.fill.fore_color.rgb = CYAN; bar.line.fill.background()
    bar.shadow.inherit = False
    tb = s.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(11.6), Inches(3.6))
    _txt(tb.text_frame, [
        [("GENERATIVE AI CAPSTONE  ·  MIT ACADEMY OF ENGINEERING  ·  2304422", 14, True, CYAN)],
        [("UrbanGenAI", 46, True, WHITE)],
        [("A Multi-Model Generative AI System for Urban-Planning Decision Support", 20, False, RGBColor(0xC5, 0xD2, 0xDE))],
        [("Case study: Pune (PMC area) — 516 km2, 7.4 million residents", 15, False, RGBColor(0x8F, 0xA3, 0xB5))],
    ], space_after=14)
    return s


def bullet_slide(p, title, intro, bullets, foot=None):
    s = blank(p); header(s, title)
    body = s.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(12), Inches(5.4))
    body.text_frame.word_wrap = True
    blocks = []
    if intro:
        blocks.append([(intro, 17, False, INK)])
        blocks.append("")
    for b in bullets:
        if isinstance(b, tuple):
            lead, rest = b
            blocks.append([("•  " + lead + "  ", 16, True, ACCENT), (rest, 16, False, INK)])
        else:
            blocks.append([("•  " + b, 16, False, INK)])
    _txt(body.text_frame, blocks, space_after=10)
    if foot:
        fb = s.shapes.add_textbox(Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
        _txt(fb.text_frame, [[(foot, 11, False, MUTE)]])
    return s


def table_slide(p, title, headers, rows, foot=None, col_w=None, fs=11, title_fs=22):
    s = blank(p)
    hd = s.shapes.add_textbox(Inches(0.55), Inches(0.32), Inches(12.3), Inches(0.8))
    _txt(hd.text_frame, [[(title, title_fs, True, INK)]])
    nr, nc = len(rows) + 1, len(headers)
    gt = s.shapes.add_table(nr, nc, Inches(0.5), Inches(1.15),
                            Inches(12.35), Inches(0.34 * nr)).table
    if col_w:
        for i, wv in enumerate(col_w):
            gt.columns[i].width = Inches(wv)
    for j, h in enumerate(headers):
        c = gt.cell(0, j); c.text = h
        c.fill.solid(); c.fill.fore_color.rgb = INK
        r = c.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(fs + 1); r.font.bold = True; r.font.color.rgb = WHITE
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = gt.cell(i, j); c.text = str(val)
            c.fill.solid(); c.fill.fore_color.rgb = WHITE if i % 2 else PANEL
            r = c.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(fs); r.font.color.rgb = INK
            if j == 0:
                r.font.bold = True
    if foot:
        fb = s.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.4))
        _txt(fb.text_frame, [[(foot, 10, False, MUTE)]])
    return s


def pipeline_slide(p, title, stages, foot):
    s = blank(p); header(s, title)
    n = len(stages)
    box_w = Inches(12.4 / n - 0.16)
    x, y = Inches(0.7), Inches(2.7)
    for i, (name, dims) in enumerate(stages):
        b = s.shapes.add_shape(1, x, y, box_w, Inches(1.7))
        b.fill.solid(); b.fill.fore_color.rgb = PANEL
        b.line.color.rgb = ACCENT; b.line.width = Pt(1.25); b.shadow.inherit = False
        tf = b.text_frame; tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        _txt(tf, [[(name, 12, True, INK)], [(dims, 10, False, MUTE)]],
             align=PP_ALIGN.CENTER, space_after=3)
        if i < n - 1:
            ar = s.shapes.add_shape(13, x + box_w, y + Inches(0.72), Inches(0.16), Inches(0.26))
            ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT2
            ar.line.fill.background(); ar.shadow.inherit = False
        x = x + box_w + Inches(0.16)
    fb = s.shapes.add_textbox(Inches(0.7), Inches(4.9), Inches(12), Inches(1.9))
    fb.text_frame.word_wrap = True
    _txt(fb.text_frame, [[(foot, 13, False, INK)]])
    return s


def image_slide(p, title, img, caption):
    s = blank(p); header(s, title)
    if os.path.exists(img):
        s.shapes.add_picture(img, Inches(0.7), Inches(1.45), height=Inches(5.2))
    cap = s.shapes.add_textbox(Inches(0.7), Inches(6.8), Inches(12), Inches(0.5))
    _txt(cap.text_frame, [[(caption, 12, False, MUTE)]])
    return s


def build():
    p = Presentation()
    p.slide_width, p.slide_height = W, H

    # 1 -----------------------------------------------------------------
    title_slide(p)

    # 2 -----------------------------------------------------------------
    bullet_slide(p, "Problem Statement",
        "City planners have to weigh many things at once — new housing, traffic, flooding, "
        "green cover, heat — and today the tools for this are split apart.",
        [
            ("Data is scattered.", "Satellite images, land-cover maps, road networks, terrain and "
             "population all sit in different software and formats."),
            ("Tools give one fixed answer.", "Normal GIS produces a single map. Planners cannot easily "
             "see and compare alternative options."),
            ("AI chat tools guess.", "Language models suggest ideas but are not connected to real "
             "ground data, so they can be wrong about a place."),
            ("No single workspace.", "There is no one place that goes from raw data to generated "
             "options to a written recommendation a planner can act on."),
        ],
        foot="Study area: Pune Municipal Corporation, India.")

    # 3 -----------------------------------------------------------------
    bullet_slide(p, "Objectives",
        "Build one connected pipeline where four generative AI models each do a clear, useful job.",
        [
            ("Classify land use", "— label an aerial tile into one of 21 zoning categories (ResNet18 CNN)."),
            ("Clean the imagery", "— use a Denoising Autoencoder to remove noise before analysis."),
            ("Flag unusual parcels", "— use a Variational Autoencoder to score how far a parcel is from normal."),
            ("Create training data", "— use a class-conditional GAN to generate synthetic tiles per class."),
            ("Draft the recommendation", "— use a from-scratch Transformer (MiniGPT) seeded with real Pune statistics."),
            ("Prove every claim", "— train each model ourselves, commit the weights, and show live measured metrics."),
        ])

    # 4 -----------------------------------------------------------------
    bullet_slide(p, "Expected Outcome",
        "A working, verifiable web application that a planner can actually use.",
        [
            ("A single dashboard", "— landing page, one page per model with architecture and instructions, "
             "and a live Evaluation page."),
            ("Four trained models", "— checkpoints committed to the repository, not downloaded."),
            ("Honest evaluation", "— real numbers for every model, plus a clear list of current limitations."),
            ("Reproducible", "— full retrain takes about 1 hour on a laptop GPU (about 0.08 kg CO2)."),
            ("Syllabus coverage", "— autoencoder, VAE, GAN and Transformer all demonstrated with working demos, "
             "loss maths and an ethics discussion."),
        ])

    # 5 -----------------------------------------------------------------
    lit = [
        ("1", "2016", "IEEE Geoscience & Remote Sensing Magazine",
         "Tutorial on deep learning for remote-sensing data.",
         "Covers autoencoders and CNNs for land-cover tasks; basis for our encoder choice."),
        ("2", "2017", "Proceedings of the IEEE",
         "Benchmark and review of remote-sensing scene classification.",
         "Introduces standard datasets (incl. UC Merced) and CNN baselines we compare against."),
        ("3", "2017", "IEEE Geoscience & Remote Sensing Magazine",
         "Comprehensive review of deep learning in remote sensing.",
         "Maps which DL methods suit classification, detection and generation."),
        ("4", "2017", "IEEE Geoscience & Remote Sensing Letters",
         "Deep learning classification of land cover and crop types.",
         "Multi-level CNN for LULC; supports our 21-class classifier design."),
        ("5", "2014", "IEEE J. Selected Topics in Applied Earth Obs. & Remote Sensing",
         "Stacked autoencoders for hyperspectral image classification.",
         "Early proof that autoencoder features help land classification."),
        ("6", "2016", "IEEE Transactions on Geoscience and Remote Sensing",
         "CNN-based deep feature extraction and classification of images.",
         "Design guidance for the fine-tuned ResNet backbone we use."),
        ("7", "2018", "IEEE Transactions on Geoscience and Remote Sensing",
         "Discriminative CNNs (metric learning) for scene classification.",
         "Motivates transfer learning on small remote-sensing datasets like ours."),
        ("8", "2018", "IEEE Signal Processing Magazine",
         "Overview of Generative Adversarial Networks.",
         "Architectures and training tricks; guided our spectral-norm + EMA GAN."),
        ("9", "2019", "IEEE Access",
         "Survey of recent progress on GANs.",
         "Catalogue of conditional-GAN variants; basis for our class-conditional design."),
        ("10", "2019", "IEEE Transactions on Geoscience and Remote Sensing",
         "Overview of deep learning for hyperspectral image classification.",
         "Compares autoencoders, CNNs and GANs on the same task."),
        ("11", "2021", "IEEE Transactions on Knowledge and Data Engineering",
         "Review of GANs: algorithms, theory and applications.",
         "Explains mode collapse and label smoothing, which we apply."),
        ("12", "2021", "IEEE Transactions on Geoscience and Remote Sensing",
         "Multimodal deep learning for remote-sensing classification.",
         "Supports our multi-source City Stack idea (imagery + land cover + roads + terrain)."),
        ("13", "2021", "IEEE Access",
         "Survey of digital twins from smart manufacturing to smart cities.",
         "Frames UrbanGenAI as a decision-support digital twin."),
        ("14", "2022", "IEEE Geoscience & Remote Sensing Magazine",
         "Review of self-supervised learning in remote sensing.",
         "Backs training our own encoders/decoders rather than only using labels."),
        ("15", "2023", "IEEE Transactions on Pattern Analysis and Machine Intelligence",
         "Survey on Vision Transformers.",
         "Background for the decoder-only Transformer (MiniGPT) we build from scratch."),
    ]
    _hdr = ["Sr.", "Year", "Publisher (IEEE journal)", "What the paper contains", "How we use it"]
    _cw = [0.5, 0.7, 3.5, 4.0, 3.65]
    table_slide(p, "Literature Review  (IEEE journals / magazines) — 1 of 2",
        _hdr, lit[:8], col_w=_cw, fs=10, title_fs=19,
        foot="All entries are IEEE journal or magazine articles — no conference papers.")
    table_slide(p, "Literature Review  (IEEE journals / magazines) — 2 of 2",
        _hdr, lit[8:], col_w=_cw, fs=10, title_fs=19,
        foot="Verify each DOI against IEEE Xplore before final submission.")

    # 6 -----------------------------------------------------------------
    pipeline_slide(p, "System Architecture  (end-to-end pipeline)", [
        ("Aerial tile\n+ Pune GIS", "128x128x3"),
        ("Land-Use\nClassifier (CNN)", "-> 1 of 21 classes"),
        ("Denoising\nAutoencoder", "clean tile"),
        ("Variational\nAutoencoder", "anomaly score"),
        ("Conditional\nGAN", "synthetic tiles"),
        ("MiniGPT\nTransformer", "plan text"),
        ("Planner\ndashboard", "decision support"),
    ], foot="One shared pipeline. The classifier says what a parcel is; the AE cleans the image; the VAE "
            "flags parcels that do not look normal for their zone; the GAN creates extra training data; "
            "MiniGPT turns the numbers into a written recommendation grounded in real Pune statistics.")

    table_slide(p, "Architecture detail — layers, epochs, dimensions at each stage",
        ["Model", "Structure (layers)", "Key dimensions", "Epochs", "Loss"], [
        ("Denoising AE", "ResNet18 encoder + 4 ConvTranspose decoder with U-Net skips",
         "input 128x128x3 -> 8x8x256 bottleneck -> 128x128x3", "50", "MSE(recon, clean), noise sigma 0.15"),
        ("Spatial VAE", "ResNet18 encoder + two 1x1 conv heads + 4 ConvTranspose decoder",
         "8x8x256 -> mu / log-var 8x8x64 -> z (4,096) -> 128x128x3", "50", "0.7 L1 + 0.3 MSE + beta KL (beta ~ 1e-4)"),
        ("Conditional GAN", "G: Linear->8x8x512 + 5 ConvTranspose;  D: 5 spectral-norm Conv",
         "z 128 + class embed 64 -> 128x128x3", "100", "non-saturating BCE, label smoothing 0.9/0.1, EMA 0.999"),
        ("MiniGPT", "4 pre-norm Transformer blocks, 4 attention heads, causal mask, weight-tied head",
         "context 192 chars, n_embd 256, vocab 64, 3.23M params", "3,000 steps", "next-character cross-entropy"),
        ("Classifier", "ResNet18 backbone + Linear(512 -> 21)",
         "224x224x3 -> 512-d -> 21 logits", "30", "cross-entropy"),
    ], col_w=[1.7, 4.0, 4.0, 1.1, 2.5], fs=9, title_fs=19,
       foot="Encoders start from ImageNet weights and are fine-tuned; all decoders, the GAN and MiniGPT are trained from scratch.")

    # 7 -----------------------------------------------------------------
    table_slide(p, "Implementation Result — verified metrics",
        ["Model", "Metric", "Result", "Plain-English reading"], [
        ("Land-Use Classifier", "Validation accuracy", "98.1 %", "Reliable at naming the 21 zone types."),
        ("Denoising AE", "PSNR / SSIM", "29.7 dB / 0.865", "Reconstruction is almost identical to the clean tile."),
        ("Denoising AE", "Final training MSE", "0.01977", "Fell from 0.1830 at epoch 1 — clear convergence."),
        ("Spatial VAE", "PSNR / SSIM", "19.5 dB / 0.43", "Deliberately soft — the 8x8 bottleneck limits detail."),
        ("Spatial VAE", "Active latent dims", "63 of 64", "Latent space is healthy, not collapsed."),
        ("Conditional GAN", "Classifier recognition rate", "~ 15 %", "Texture classes work; grid-geometry classes need more epochs."),
        ("MiniGPT", "Held-out perplexity", "1.09", "Learns the templated corpus well (that is the intended job)."),
        ("MiniGPT", "Bits per character", "0.12  (vs 6.0 random)", "Very confident next-character prediction."),
    ], col_w=[2.7, 2.7, 2.5, 4.4], fs=10.5, title_fs=21,
       foot="Computed once at backend startup and served live at /evaluate/<model>. AE/VAE over 105 held-out tiles across all 21 classes.")

    image_slide(p, "Implementation Result — live Evaluation dashboard",
        os.path.join(SHOT, "ppt_eval.png"),
        "Evaluation page: one tab per model, each showing the metric it is judged by, computed on held-out data.")

    # 8 -----------------------------------------------------------------
    image_slide(p, "Output — a model page (Autoencoder)",
        os.path.join(SHOT, "ppt_ae.png"),
        "Each model has its own page: animated input-to-output flow, labelled architecture diagram, "
        "how-to-use steps, and how it fits the project.")

    bullet_slide(p, "Output — what the user sees",
        "Every model produces a concrete result the planner can read:",
        [
            ("Classifier", "— the predicted zone, e.g. 'dense residential', with confidence."),
            ("Denoising AE", "— three panels: original, noisy input, cleaned reconstruction."),
            ("VAE", "— a banner: Typical / Unusual / Highly Anomalous, with a percentage and a reason."),
            ("GAN", "— a grid of freshly generated tiles, one per land-use class."),
            ("MiniGPT", "— a short written recommendation (setbacks, permeable surface, flood buffer, parking cap) "
             "built from that ward's real statistics."),
        ])

    # 9 -----------------------------------------------------------------
    bullet_slide(p, "Conclusion",
        "UrbanGenAI shows four generative models working together on one urban-planning task.",
        [
            ("It works end to end", "— from an aerial tile and GIS data to a written, grounded recommendation."),
            ("It is honest", "— every number is measured live; limitations (GAN geometry, VAE softness) are "
             "stated with evidence, not hidden."),
            ("It is ours", "— the VAE decoder, the GAN and MiniGPT are trained fully from scratch; checkpoints are committed."),
            ("It is responsible", "— only public data, planner stays in the loop, outputs are candidates that "
             "still need statutory and engineering checks."),
            ("Next steps", "— full 5-source City Stack, a diffusion model for photoreal renders, and surrogate "
             "models for traffic, air quality and flood risk (see the Future Scope page)."),
        ],
        foot="Live demo order: Landing -> Model Explorer -> each model page -> Evaluation -> Future Scope.")

    out = os.path.join(ROOT, "UrbanGenAI_Presentation.pptx")
    p.save(out)
    print("wrote", out, "-", len(p.slides._sldIdLst), "slides")


if __name__ == "__main__":
    build()
