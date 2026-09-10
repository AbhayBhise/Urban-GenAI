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
            c = gt.cell(i, j)
            c.text = str(val) if str(val) else " "
            c.fill.solid(); c.fill.fore_color.rgb = WHITE if i % 2 else PANEL
            runs = c.text_frame.paragraphs[0].runs
            if not runs:
                continue
            r = runs[0]
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


def layered_arch_slide(p, title, layers, foot):
    """layers: list of (band_label, [component strings]).  Drawn top-to-bottom
    as stacked bands, with a down-arrow between bands."""
    s = blank(p); header(s, title)
    n = len(layers)
    top = Inches(1.45)
    band_h = Inches((6.9 - 1.45) / n - 0.14)
    gap = Inches(0.14)
    y = top
    for li, (label, comps) in enumerate(layers):
        band = s.shapes.add_shape(1, Inches(0.6), y, Inches(12.1), band_h)
        band.fill.solid(); band.fill.fore_color.rgb = PANEL
        band.line.color.rgb = ACCENT; band.line.width = Pt(1); band.shadow.inherit = False
        lb = s.shapes.add_textbox(Inches(0.75), y + Inches(0.06), Inches(2.5), band_h)
        lb.text_frame.word_wrap = True
        _txt(lb.text_frame, [[(label, 11.5, True, ACCENT2)]])
        cx = Inches(3.15)
        cw = Inches((12.1 - 2.7) / max(len(comps), 1) - 0.12)
        for c in comps:
            cb = s.shapes.add_shape(1, cx, y + Inches(0.1), cw, band_h - Inches(0.2))
            cb.fill.solid(); cb.fill.fore_color.rgb = WHITE
            cb.line.color.rgb = MUTE; cb.line.width = Pt(0.75); cb.shadow.inherit = False
            tf = cb.text_frame; tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            _txt(tf, [[(c, 9.5, False, INK)]], align=PP_ALIGN.CENTER, space_after=0)
            cx = cx + cw + Inches(0.12)
        if li < n - 1:
            ar = s.shapes.add_shape(13, Inches(6.55), y + band_h - Inches(0.02),
                                    Inches(0.22), gap + Inches(0.04))
            ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT2
            ar.line.fill.background(); ar.shadow.inherit = False
        y = y + band_h + gap
    fb = s.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12.1), Inches(0.4))
    _txt(fb.text_frame, [[(foot, 10.5, False, MUTE)]])
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
    layered_arch_slide(p, "System Architecture  (full project, layered)", [
        ("1. Client", ["React SPA (Vite + TypeScript)", "API helper (adds operator key)"]),
        ("2. API", ["FastAPI + Uvicorn — /infer, /evaluate, /generate, /status",
                    "Security: API-key, rate-limit, CORS, upload validation"]),
        ("3. Model services", ["Denoising AE", "Spatial VAE", "Conditional GAN", "MiniGPT", "Land-Use Classifier"]),
        ("4. Evaluation", ["compute_*_evaluation() at startup", "/evaluate/<model> GET endpoints (cached)"]),
        ("5. Data & artifacts", ["UCMerced / EuroSAT tiles", "Pune PMC GIS (GeoPandas)",
                                 "outputs/*/model.pth + history.json", "corpus/urban_planning.txt"]),
    ], foot="A request flows down (client -> API -> model -> data/checkpoint) and the result flows back up. "
            "The evaluation layer is filled once at startup, then only read.")

    table_slide(p, "System Architecture — components",
        ["Layer", "Component", "Technology", "Responsibility"], [
        ("1. Client", "React SPA", "React + TypeScript (Vite)",
         "Landing page, one page per model, Evaluation and Comparison dashboards, light/dark theme"),
        ("", "API helper", "fetch + localStorage",
         "Adds the operator API key to each request; nothing else leaves the browser"),
        ("2. API", "FastAPI app", "FastAPI + Uvicorn",
         "REST endpoints: /infer/*, /evaluate/*, /generate/plan, /sample/*, /status, /history/*"),
        ("", "Security middleware", "slowapi + custom deps",
         "Optional API-key auth, rate limiting, CORS allow-list, image-upload validation"),
        ("3. Model services", "5 PyTorch models", "PyTorch (torch, torchvision)",
         "AE, VAE, GAN, MiniGPT, Classifier — each loads its checkpoint at startup, one forward pass per request"),
        ("4. Evaluation", "compute_*_evaluation()", "runs once at startup",
         "Held-out PSNR/SSIM/MSE, KL, perplexity, recognition rate, confusion matrix — cached in memory"),
        ("5. Data & artifacts", "Datasets + GIS + checkpoints", "UCMerced, EuroSAT, GeoPandas/OSM, .pth",
         "Training and held-out data; Pune GIS seeds the MiniGPT prompt; committed checkpoints are the source of truth"),
    ], col_w=[1.55, 2.15, 2.75, 5.9], fs=9, title_fs=19,
       foot="Uploads are processed in memory only and never written to disk; only public data and open GIS are used.")

    table_slide(p, "System Architecture — request flow",
        ["Step", "Path", "What happens"], [
        ("0", "Startup (once)", "Every checkpoint is loaded and every /evaluate metric is computed and cached."),
        ("1", "Browser  ->  FastAPI", "User uploads a tile / picks a class / asks for a plan (multipart or JSON)."),
        ("2", "Security middleware", "API-key check (if enabled), rate-limit, CORS, validate image. Upload stays in memory."),
        ("3", "Router  ->  model service", "The endpoint dispatches to the matching model (AE / VAE / GAN / MiniGPT / Classifier)."),
        ("4", "Model service (in memory)", "Uses the pre-loaded checkpoint; runs one forward pass on CPU/GPU."),
        ("5", "Post-processing", "Anomaly z-score vs baseline; PSNR/SSIM; softmax; decode generated text or image."),
        ("6", "FastAPI  ->  Browser", "JSON (numbers, labels) or a base64 PNG; the React page renders the result."),
    ], col_w=[0.7, 2.9, 8.75], fs=10, title_fs=19)

    table_slide(p, "Architecture detail — model layers, epochs, dimensions",
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
    table_slide(p, "Implementation Result — modules, losses & evaluation matrix",
        ["Module", "Objective / loss function", "Final training loss",
         "Evaluation metric (sample)", "Measured result", "Reading"], [
        ("Denoising AE",
         "MSE(recon, clean tile); input corrupted with Gaussian noise sigma = 0.15",
         "0.01977 MSE  (from 0.1830 at epoch 1)",
         "PSNR / SSIM / MSE  — 105 held-out tiles",
         "29.7 dB / 0.865 / 0.0045",
         "Near-lossless"),
        ("Spatial VAE",
         "0.7 L1 + 0.3 MSE  +  beta KL(q(z|x) || N(0,I)),  beta ~ 1e-4",
         "recon 0.07524  ·  KL 103.25 nats",
         "PSNR / SSIM / KL / active latent dims",
         "19.5 dB / 0.43 / 106 nats / 63 of 64",
         "Soft by design; latent healthy"),
        ("Conditional GAN",
         "Non-saturating BCE  +  label smoothing 0.9 / 0.1;  EMA generator 0.999",
         "adversarial min-max — no single value",
         "Classifier-recognition rate  — 168 generated tiles",
         "~ 15 % overall",
         "Texture OK; geometry immature"),
        ("MiniGPT Transformer",
         "Next-character cross-entropy (causal LM)",
         "train 0.087  ·  held-out 0.083",
         "Perplexity / bits-per-char  — 23,616 chars",
         "1.09  /  0.12 bpc  (vs 6.0 random)",
         "Learns corpus; generalises"),
        ("Land-Use Classifier",
         "Cross-entropy over 21 classes",
         "0.1032 validation loss",
         "Top-1 accuracy + 21x21 confusion matrix",
         "98.1 % validation accuracy",
         "Reliable; feeds VAE + GPT"),
    ], col_w=[1.7, 3.0, 1.95, 2.35, 1.9, 1.45], fs=8.5, title_fs=19,
       foot="All values are read live from committed checkpoints / training logs and served at /evaluate/<module>.")

    table_slide(p, "Model Comparison — which model is better, and for what",
        ["Model", "Domain / task", "Accuracy / best result", "Main error / limitation",
         "Verdict — it is the better choice for..."], [
        ("Denoising AE",
         "Image restoration of aerial tiles",
         "PSNR 29.7 dB, SSIM 0.865",
         "Slight residual blur on very fine texture",
         "Cleaning noisy imagery. U-Net skips beat a plain bottleneck: 25 -> 29.7 dB."),
        ("Spatial VAE",
         "Anomaly detection + latent scenario exploration",
         "SSIM 0.43; 63 of 64 latent dims active",
         "Reconstruction is soft (8x8 bottleneck)",
         "Answering 'is this parcel normal for its zone?' — gives a probabilistic score the AE cannot."),
        ("Conditional GAN",
         "Generating new synthetic tiles per class",
         "~15% recognised; beach / forest / built-up high",
         "Grid-geometry classes near 0% at 100 epochs",
         "Augmenting texture-rich classes. Not yet reliable for geometric classes — needs more epochs / data."),
        ("MiniGPT",
         "Text — planning recommendations",
         "Perplexity 1.09, 0.12 bits/char",
         "Narrow: templated corpus, not a general planner",
         "Structured, grounded drafting from real ward statistics. Not for open-ended writing."),
        ("Land-Use Classifier",
         "Discriminative classification (21 zones)",
         "98.1% validation accuracy",
         "Some dense- vs medium-residential confusion",
         "Most accurate model overall; a CNN (not generative) — it labels parcels for the other stages."),
    ], col_w=[1.55, 2.5, 2.15, 2.6, 3.55], fs=8.5, title_fs=18,
       foot="Head-to-head (same task, 128x128 tiles): AE beats VAE on fidelity (skips, no KL constraint); "
            "VAE beats AE on giving an anomaly score + smooth interpolation. The five models are complementary, not competitors.")

    table_slide(p, "Evaluation parameters — what each one means",
        ["Parameter", "What it measures", "Better is", "Used for"], [
        ("PSNR (dB)", "Pixel closeness of the reconstruction to the target image", "higher", "AE, VAE"),
        ("SSIM (0-1)", "Structural similarity (edges, texture) to the target", "higher (-> 1)", "AE, VAE"),
        ("MSE", "Mean squared pixel error", "lower", "AE, VAE"),
        ("KL divergence (nats)", "How far the learned latent is from a standard Normal prior", "balanced — not 0, not huge", "VAE"),
        ("Active latent dims", "Latent channels that carry real information (out of 64)", "higher", "VAE"),
        ("Classifier-recognition rate", "Share of generated tiles the classifier recognises as their class", "higher", "GAN"),
        ("Perplexity", "Effective number of choices per character (1 = perfect)", "lower (-> 1)", "MiniGPT"),
        ("Bits per character", "Information per character vs 6.0 bits for a random guess", "lower", "MiniGPT"),
        ("Top-1 accuracy", "Share of tiles given the correct land-use label", "higher", "Classifier"),
    ], col_w=[2.7, 5.0, 2.65, 2.0], fs=10, title_fs=20,
       foot="Each model is scored with the metric that model is actually judged by — not one metric forced onto all.")

    # 8 -----------------------------------------------------------------
    table_slide(p, "Output — input and result for each module",
        ["Module", "Input", "Output shown to the planner"], [
        ("Land-Use Classifier", "One aerial tile (224x224)",
         "Predicted zone (e.g. 'dense residential') + confidence + full 21-class bar"),
        ("Denoising AE", "Aerial tile + added noise",
         "Three panels: original  |  noisy input  |  cleaned reconstruction  (+ PSNR / SSIM)"),
        ("Spatial VAE", "One aerial tile",
         "Anomaly banner — Typical / Unusual / Highly Anomalous — with a % and a plain reason; "
         "plus latent interpolation between two tiles"),
        ("Conditional GAN", "A chosen class (1 of 21) + random noise",
         "A grid of freshly generated 128x128 tiles for that class"),
        ("MiniGPT Transformer", "Real Pune ward statistics (built-up %, road length, waterways)",
         "A short written recommendation: setbacks, permeable surface, flood buffer, transit parking cap"),
    ], col_w=[2.2, 3.4, 6.75], fs=10, title_fs=21,
       foot="Every output is on its own model page in the app, with an animated input-to-output flow above it.")

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
