import React from 'react';
import { Box, Arrow, ArrowheadDef, SyllabusTable, ProvenanceNote, COLORS } from '../lib/archDiagram';

export default function VAEArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <ProvenanceNote>
        This VAE was trained end-to-end on UCMerced by our own <code>train_vae.py</code> (50 epochs).
        The ResNet18 encoder starts from ImageNet-pretrained weights (transfer learning — standard
        practice, not something we're hiding) but is <strong>fine-tuned</strong> on our data
        (frozen for the first 5 epochs, then unfrozen); the decoder, the μ/log σ² heads, and the
        reparameterization path are all trained <strong>entirely from scratch</strong> by us.
        The resulting checkpoint (<code>outputs/vae/model.pth</code>) is our own, committed to the repo — not a downloaded model.
      </ProvenanceNote>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Spatial-Latent VAE with a Pretrained Encoder</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 1180 430" style={{ width: '100%', minWidth: 900, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>

            <Box x={20} y={20} w={120} h={56} fill={COLORS.surface} stroke={COLORS.border}
              label="Input Tile" sub="128×128×3" />
            <Arrow x1={140} y1={48} x2={172} y2={48} />

            <Box x={172} y={20} w={190} h={56} fill={COLORS.surface} stroke={COLORS.accent2}
              label="ResNet18 Encoder" sub="pretrained, 16× downsample" labelColor={COLORS.accent2} />
            <Arrow x1={362} y1={48} x2={394} y2={48} />

            <Box x={394} y={0} w={110} h={40} fill="#171018" stroke={COLORS.accent}
              label="μ head" sub="8×8×64" labelColor={COLORS.accent} />
            <Box x={394} y={62} w={110} h={40} fill="#171018" stroke={COLORS.accent}
              label="log σ² head" sub="8×8×64" labelColor={COLORS.accent} />
            <Arrow x1={504} y1={20} x2={536} y2={45} />
            <Arrow x1={504} y1={82} x2={536} y2={55} />

            <Box x={536} y={20} w={150} h={56} fill="#12181f" stroke={COLORS.accent}
              label="Reparameterize" sub="z = μ + σ⊙ε" labelColor={COLORS.accent} />
            <Arrow x1={686} y1={48} x2={718} y2={48} />

            <Box x={718} y={20} w={190} h={56} fill={COLORS.surface} stroke={COLORS.accent2}
              label="CNN Decoder" sub="4× ConvTranspose, 16× upsample" labelColor={COLORS.accent2} />
            <Arrow x1={908} y1={48} x2={940} y2={48} />

            <Box x={940} y={20} w={120} h={56} fill={COLORS.surface} stroke={COLORS.border}
              label="Reconstruction" sub="128×128×3" />

            <line x1={628} y1={76} x2={628} y2={112} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <line x1={1000} y1={76} x2={1000} y2={112} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <Box x={628} y={112} w={372} h={56} fill="#1a1408" stroke={COLORS.warn}
              label="Loss = 0.7·L1 + 0.3·MSE(recon, input)  +  β·KL(q(z|x) ‖ N(0,I))"
              sub="β ≈ 1e-4 (deliberately tiny — see note below)" labelColor={COLORS.warn} />

            <text x={20} y={210} fontSize="12" fontWeight={700} fill={COLORS.text}>Branch A — Anomaly Detection (this project's primary use of the VAE)</text>
            <Box x={20} y={222} w={150} h={50} fill={COLORS.surface} stroke={COLORS.border}
              label="Reconstruction Error" sub="MSE(recon, input)" />
            <Arrow x1={170} y1={247} x2={202} y2={247} />
            <Box x={202} y={222} w={190} h={50} fill={COLORS.surface} stroke={COLORS.border}
              label="Compare vs. Baseline" sub="mean/std over 294 real tiles" />
            <Arrow x1={392} y1={247} x2={424} y2={247} />
            <Box x={424} y={222} w={110} h={50} fill={COLORS.surface} stroke={COLORS.border} label="z-score" />
            <Arrow x1={534} y1={247} x2={566} y2={247} />
            <Box x={566} y={200} w={130} h={30} fill="#0a1f14" stroke={COLORS.success} label="Typical" labelColor={COLORS.success} />
            <Box x={566} y={237} w={130} h={30} fill="#1f1a08" stroke={COLORS.warn} label="Unusual" labelColor={COLORS.warn} />
            <Box x={566} y={274} w={150} h={30} fill="#1f0a0a" stroke={COLORS.danger} label="Highly Anomalous" labelColor={COLORS.danger} />
            <Arrow x1={534} y1={247} x2={562} y2={215} />
            <Arrow x1={534} y1={247} x2={562} y2={289} />

            <text x={20} y={345} fontSize="12" fontWeight={700} fill={COLORS.text}>Branch B — Latent Interpolation</text>
            <Box x={20} y={357} w={160} h={50} fill={COLORS.surface} stroke={COLORS.border}
              label="Two Real Tiles" sub="encode both → μ₀, μ₁" />
            <Arrow x1={180} y1={382} x2={212} y2={382} />
            <Box x={212} y={357} w={190} h={50} fill={COLORS.surface} stroke={COLORS.border}
              label="Linear Blend" sub="(1−α)μ₀ + αμ₁,  α: 0→1" />
            <Arrow x1={402} y1={382} x2={434} y2={382} />
            <Box x={434} y={357} w={140} h={50} fill={COLORS.surface} stroke={COLORS.border}
              label="Decode" sub="8 steps" />
            <Arrow x1={574} y1={382} x2={606} y2={382} />
            <Box x={606} y={357} w={220} h={50} fill={COLORS.surface} stroke={COLORS.accent}
              label="Smooth Land-Use Spectrum" labelColor={COLORS.accent} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">What Each Component Does</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div><strong style={{ color: 'var(--accent2)' }}>ResNet18 Encoder</strong> — pretrained on ImageNet, truncated at layer3. Downsamples the 128×128 tile 16× to an 8×8×256 feature map.</div>
            <div><strong style={{ color: 'var(--accent)' }}>μ / log σ² heads</strong> — two parallel 1×1 convolutions turn the 8×8×256 feature map into the parameters of a diagonal Gaussian posterior <em>q(z|x)</em>, kept spatial (8×8×64 each) rather than flattened to a vector.</div>
            <div><strong style={{ color: 'var(--accent)' }}>Reparameterization trick</strong> — samples <code>z = μ + σ⊙ε</code>, <code>ε ~ N(0,I)</code>, instead of sampling z directly (non-differentiable). Moving the randomness into a separate input keeps the path differentiable, so gradients reach the encoder.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>CNN Decoder</strong> — four ConvTranspose2d stages upsample the 8×8 latent back to 128×128×3.</div>
            <div><strong style={{ color: 'var(--warn)' }}>KL divergence term</strong> — penalizes the posterior for straying from N(0,I). Measured on this dataset: β≥0.02 causes full posterior collapse, β=0.05 visibly degrades reconstruction — so β is kept near-zero, prioritizing fidelity.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">How to Use This Page</div>
          <ol style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.85rem', color: 'var(--text)' }}>
            <li>Upload any UCMerced tile, or click <strong>Load Real Sample</strong>.</li>
            <li>Click <strong>Run Inference</strong> — the reconstruction and the Anomaly Check banner (Typical / Unusual / Highly Anomalous, with a percentage and a plain-language reason) appear immediately below.</li>
            <li>Click <strong>Show Land-Use Interpolation</strong> to see this tile's latent blended with a second real tile's, decoded at 8 steps.</li>
            <li><em>Optional:</em> Show Urbanization Projection — a separate style-transfer feature (not VAE-latent), see the note below.</li>
          </ol>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">Contribution to UrbanGenAI</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>1. <strong>Land-Use Classifier</strong> identifies what a tile currently is (98.1% accuracy, 21 categories).</div>
            <div>2. <strong>This VAE</strong> scores its reconstruction error against a 294-tile baseline — <em>does this parcel look typical for what it claims to be?</em> Atypical parcels (unregistered construction, illegal conversion, sensor artifacts) reconstruct worse and get flagged.</div>
            <div>3. Flagged / typical parcels feed into the <strong>MiniGPT Plan Generator</strong> for text recommendations.</div>
            <div>4. <strong>Latent interpolation</strong> separately gives a continuous, explorable spectrum between two land-use states.</div>
            <div style={{ color: 'var(--muted)', marginTop: 4 }}>
              Deliberately <em>not</em> claimed: that this VAE renders "this land, developed" with new buildings/roads. It reconstructs and interpolates between real, encoded tiles — it cannot invent geometry that isn't implied by what it has seen.
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Improvement Over the Standard Baseline</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>The original VAE (Kingma &amp; Welling, 2013) uses a small from-scratch encoder and a single flattened latent vector — fine for MNIST/CelebA-scale toy problems, but this project has only 2,100 training images across 21 visually diverse classes.</div>
            <div>We adapted the recipe for that constraint: a <strong>pretrained</strong> ResNet18 encoder instead of training visual features from scratch on a tiny dataset; a <strong>spatial</strong> 8×8×64 latent instead of one flattened vector, preserving per-region correspondence rather than one global code.</div>
            <div>On β: standard β-VAE guidance (Higgins et al., 2017) recommends a meaningful β for a disentangled, prior-matched latent. We <strong>tested that against our own data</strong> and measured it failing — β≥0.02 causes full posterior collapse here — so we deliberately deviated from the textbook default, evidenced by our own numbers, not by assumption.</div>
            <div>The anomaly-detection application itself extends the reconstruction-probability approach of An &amp; Cho (2015) to this domain, paired with a signed-percentage/plain-language explanation rather than a raw score.</div>
          </div>
        </div>
      </div>

      <SyllabusTable rows={[
        ['Encoder / Decoder structure', 'ResNet18 encoder + CNN decoder, shown above'],
        ['KL divergence', 'Computed analytically every inference and plotted (dual-axis) against reconstruction loss during training'],
        ['Reparameterization trick', 'Implemented as z = μ + σ⊙ε; explained above with the differentiability reasoning'],
        ['Latent space exploration', "Interpolation between two real tiles' encoded latents (Branch B)"],
        ['Application: Anomaly Detection', 'Reconstruction-error z-score vs. a 294-tile baseline, surfaced as Typical / Unusual / Highly Anomalous (Branch A)'],
        ['Self-study: Limitations of AEs/VAEs', 'Documented and measured: posterior collapse at β≥0.02, degraded reconstruction even at β=0.05 — a deliberate, evidence-based design choice, not an oversight'],
      ]} />
    </div>
  );
}
