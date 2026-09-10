import React from 'react';

const COLORS = {
  bg: '#080C14',
  surface: '#0F1923',
  border: '#1E2D40',
  accent: '#00D4FF',
  accent2: '#7B61FF',
  text: '#E8EDF5',
  muted: '#4A6080',
  success: '#00E676',
  warn: '#FFB84D',
  danger: '#FF5252',
};

function Box({ x, y, w, h, fill, stroke, label, sub, labelColor }: {
  x: number; y: number; w: number; h: number; fill: string; stroke: string;
  label: string; sub?: string; labelColor?: string;
}) {
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={8} fill={fill} stroke={stroke} strokeWidth={1.5} />
      <text x={x + w / 2} y={y + (sub ? h / 2 - 6 : h / 2 + 5)} textAnchor="middle"
        fontSize="12.5" fontWeight={600} fill={labelColor || COLORS.text} fontFamily="var(--font-ui)">
        {label}
      </text>
      {sub && (
        <text x={x + w / 2} y={y + h / 2 + 12} textAnchor="middle" fontSize="10.5"
          fill={COLORS.muted} fontFamily="var(--font-mono)">
          {sub}
        </text>
      )}
    </g>
  );
}

function Arrow({ x1, y1, x2, y2, color }: { x1: number; y1: number; x2: number; y2: number; color?: string }) {
  return (
    <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color || COLORS.muted} strokeWidth={1.75}
      markerEnd="url(#arrowhead)" />
  );
}

export default function VAEArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <div style={{
        display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 20,
        padding: '12px 16px', borderRadius: 6, background: 'rgba(0, 230, 118, 0.06)',
        border: '1px solid rgba(0, 230, 118, 0.25)', fontSize: '0.85rem',
      }}>
        <strong style={{ color: 'var(--success)', flexShrink: 0 }}>Trained by us:</strong>
        <span style={{ color: 'var(--text)' }}>
          This VAE was trained end-to-end on UCMerced by our own <code>train_vae.py</code> (50 epochs).
          The ResNet18 encoder starts from ImageNet-pretrained weights (transfer learning — standard
          practice, not something we're hiding) but is <strong>fine-tuned</strong> on our data
          (frozen for the first 5 epochs, then unfrozen); the decoder, the μ/log σ² heads, and the
          reparameterization path are all trained <strong>entirely from scratch</strong> by us.
          The resulting checkpoint (<code>outputs/vae/model.pth</code>) is our own, committed to the repo — not a downloaded model.
        </span>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Spatial-Latent VAE with a Pretrained Encoder</div>

        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 1180 430" style={{ width: '100%', minWidth: 900, height: 'auto' }}>
            <defs>
              <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
                <path d="M0,0 L8,4 L0,8 Z" fill={COLORS.muted} />
              </marker>
            </defs>

            {/* ---- Row 1: main encode/decode pipeline ---- */}
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

            {/* Loss annotation */}
            <line x1={628} y1={76} x2={628} y2={112} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <line x1={1000} y1={76} x2={1000} y2={112} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <Box x={628} y={112} w={372} h={56} fill="#1a1408" stroke={COLORS.warn}
              label="Loss = 0.7·L1 + 0.3·MSE(recon, input)  +  β·KL(q(z|x) ‖ N(0,I))"
              sub="β ≈ 1e-4 (deliberately tiny — see note below)" labelColor={COLORS.warn} />

            {/* ---- Row 2: two downstream branches ---- */}
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
            <div><strong style={{ color: 'var(--accent2)' }}>ResNet18 Encoder</strong> — pretrained on ImageNet, truncated at layer3. Downsamples the 128×128 tile 16× to an 8×8×256 feature map. Reused (not retrained from scratch) so the model starts with real visual features instead of random weights.</div>
            <div><strong style={{ color: 'var(--accent)' }}>μ / log σ² heads</strong> — two parallel 1×1 convolutions turn the 8×8×256 feature map into the parameters of a diagonal Gaussian posterior <em>q(z|x)</em>, kept spatial (8×8×64 each) rather than flattened to a vector, to preserve where in the tile each latent value corresponds to.</div>
            <div><strong style={{ color: 'var(--accent)' }}>Reparameterization trick</strong> — samples <code>z = μ + σ⊙ε</code> with <code>ε ~ N(0,I)</code> instead of sampling z directly. Sampling directly is non-differentiable (you can't backpropagate through a random draw); rewriting the randomness as a separate input <code>ε</code> makes the whole path from input to loss differentiable, so gradients can reach the encoder.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>CNN Decoder</strong> — four ConvTranspose2d stages upsample the 8×8 latent back to 128×128×3, mirroring the encoder's downsampling.</div>
            <div><strong style={{ color: 'var(--warn)' }}>KL divergence term</strong> — <code>KL(q(z|x) ‖ N(0,I)) = -½Σ(1+logσ²-μ²-σ²)</code> penalizes the posterior for straying from a standard normal prior. Measured directly on this dataset: a meaningful KL weight (β≥0.02) causes full posterior collapse, and even β=0.05 visibly degrades reconstruction — so β is kept near-zero (~1e-4), prioritizing reconstruction fidelity. The KL value is still computed and displayed every inference specifically so this tradeoff stays visible rather than hidden.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Pipeline — How This Fits the Project</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>1. <strong>Land-Use Classifier</strong> identifies what a tile currently is (98% accuracy, 21 UCMerced zoning categories).</div>
            <div>2. <strong>This VAE</strong> reconstructs the same tile and scores its reconstruction error against a baseline built from 294 real tiles — <em>does this parcel look typical for what it claims to be?</em> Atypical parcels (unregistered construction, illegal land conversion, sensor artifacts) reconstruct worse and get flagged.</div>
            <div>3. Flagged / typical parcels feed into the <strong>MiniGPT Plan Generator</strong>, which drafts text recommendations conditioned on real Pune land-use statistics.</div>
            <div>4. Separately, <strong>latent interpolation</strong> between two real tiles gives planners a continuous, explorable spectrum between two land-use states — distinct from the classifier's hard categorical label.</div>
            <div style={{ color: 'var(--muted)', marginTop: 4 }}>
              Deliberately <em>not</em> claimed: that this VAE renders "this land, developed" with new buildings/roads. A VAE reconstructs and interpolates between real, encoded tiles — it cannot invent geometry that isn't implied by what it has actually seen. That capability (photorealistic scenario rendering) would need a differently-conditioned generative model (e.g. ControlNet-style diffusion) as future work, not this VAE.
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Syllabus Alignment — Unit 2: Autoencoders &amp; Variational Autoencoders</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--muted)', textAlign: 'left' }}>
                <th style={{ padding: '8px 12px' }}>Syllabus requirement</th>
                <th style={{ padding: '8px 12px' }}>Where it's demonstrated here</th>
              </tr>
            </thead>
            <tbody>
              {[
                ['Encoder / Decoder structure', 'ResNet18 encoder + CNN decoder, shown above'],
                ['KL divergence', 'Computed analytically every inference and plotted (dual-axis) against reconstruction loss during training'],
                ['Reparameterization trick', 'Implemented as z = μ + σ⊙ε; explained above with the differentiability reasoning'],
                ['Latent space exploration', 'Interpolation between two real tiles\' encoded latents (Branch B)'],
                ['Application: Anomaly Detection', 'Reconstruction-error z-score vs. a 294-tile baseline, surfaced as Typical / Unusual / Highly Anomalous (Branch A)'],
                ['Self-study: Limitations of AEs/VAEs', 'Documented and measured: posterior collapse at β≥0.02, degraded reconstruction even at β=0.05 — a deliberate, evidence-based design choice, not an oversight'],
              ].map(([req, where]) => (
                <tr key={req} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '8px 12px', fontWeight: 600 }}>{req}</td>
                  <td style={{ padding: '8px 12px', color: 'var(--muted)' }}>{where}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
