// AEArchitecture component
import { Box, Arrow, ArrowheadDef, SyllabusTable, ProvenanceNote, DiagramBackground, COLORS } from '../lib/archDiagram';

export default function AEArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <ProvenanceNote>
        This Autoencoder was trained end-to-end on UCMerced by our own <code>train_ae.py</code> (50
        epochs). The ResNet18 encoder starts from ImageNet-pretrained weights (transfer learning)
        but is <strong>fine-tuned</strong> on our data (frozen for the first 5 epochs, then
        unfrozen); the entire skip-connected decoder is trained <strong>entirely from scratch</strong> by
        us. The checkpoint (<code>outputs/ae/model.pth</code>) is our own, committed to the repo.
      </ProvenanceNote>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — U-Net Skip-Connected Denoising Autoencoder</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 920 380" style={{ width: '100%', minWidth: 820, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>
            <DiagramBackground />

            {/* ---- Encoder (top row, left to right = decreasing resolution) ---- */}
            <text x={20} y={12} fontSize="11" fontWeight={700} fill={COLORS.accent2}>ENCODER — pretrained ResNet18</text>
            <Box x={20} y={20} w={110} h={56} fill={COLORS.surface} stroke={COLORS.border} label="Input Tile" sub="128×128×3" />
            <Arrow x1={130} y1={48} x2={186} y2={48} />
            <Box x={186} y={20} w={144} h={56} fill={COLORS.surface} stroke={COLORS.accent2} label="Stem (s0)" sub="64×64×64" labelColor={COLORS.accent2} />
            <Arrow x1={330} y1={48} x2={356} y2={48} />
            <Box x={356} y={20} w={144} h={56} fill={COLORS.surface} stroke={COLORS.accent2} label="MaxPool + Layer1 (s1)" sub="32×32×64" labelColor={COLORS.accent2} />
            <Arrow x1={500} y1={48} x2={526} y2={48} />
            <Box x={526} y={20} w={144} h={56} fill={COLORS.surface} stroke={COLORS.accent2} label="Layer2 (s2)" sub="16×16×128" labelColor={COLORS.accent2} />
            <Arrow x1={670} y1={48} x2={696} y2={48} />
            <Box x={696} y={20} w={150} h={56} fill={COLORS.surface} stroke={COLORS.accent} label="Layer3 — Bottleneck" sub="8×8×256" labelColor={COLORS.accent} />

            {/* ---- Skip connections (dashed, vertical) ---- */}
            <line x1={258} y1={76} x2={258} y2={224} stroke={COLORS.warn} strokeWidth={1.5} strokeDasharray="4,4" markerEnd="url(#arrowhead)" />
            <line x1={428} y1={76} x2={428} y2={224} stroke={COLORS.warn} strokeWidth={1.5} strokeDasharray="4,4" markerEnd="url(#arrowhead)" />
            <line x1={598} y1={76} x2={598} y2={224} stroke={COLORS.warn} strokeWidth={1.5} strokeDasharray="4,4" markerEnd="url(#arrowhead)" />
            <text x={258} y={150} fontSize="9.5" fill={COLORS.warn} textAnchor="middle">skip s0</text>
            <text x={428} y={150} fontSize="9.5" fill={COLORS.warn} textAnchor="middle">skip s1</text>
            <text x={598} y={150} fontSize="9.5" fill={COLORS.warn} textAnchor="middle">skip s2</text>

            {/* ---- Decoder (bottom row, right to left = increasing resolution) ---- */}
            <text x={20} y={218} fontSize="11" fontWeight={700} fill={COLORS.accent}>DECODER — trained from scratch, mirrors the encoder</text>
            <Arrow x1={696} y1={252} x2={674} y2={252} color={COLORS.accent} />
            <Box x={526} y={228} w={144} h={56} fill="#12181f" stroke={COLORS.accent} label="Up1 + concat s2" sub="16×16×128" labelColor={COLORS.accent} />
            <Arrow x1={526} y1={256} x2={504} y2={256} color={COLORS.accent} />
            <Box x={356} y={228} w={144} h={56} fill="#12181f" stroke={COLORS.accent} label="Up2 + concat s1" sub="32×32×64" labelColor={COLORS.accent} />
            <Arrow x1={356} y1={256} x2={334} y2={256} color={COLORS.accent} />
            <Box x={186} y={228} w={144} h={56} fill="#12181f" stroke={COLORS.accent} label="Up3 + concat s0" sub="64×64×32" labelColor={COLORS.accent} />
            <Arrow x1={186} y1={256} x2={130} y2={256} color={COLORS.accent} />
            <Box x={20} y={228} w={110} h={56} fill={COLORS.surface} stroke={COLORS.border} label="Reconstruction" sub="128×128×3, Tanh" />

            {/* Loss annotation */}
            <line x1={490} y1={284} x2={490} y2={316} stroke={COLORS.danger} strokeWidth={1.25} strokeDasharray="3,3" />
            <Box x={230} y={316} w={520} h={50} fill="#1f0a0a" stroke={COLORS.danger}
              label="Loss = MSE(reconstruction, clean tile)"
              sub="input corrupted with Gaussian noise (σ=0.15) at both train and inference time" labelColor={COLORS.danger} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">What Each Component Does</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div><strong style={{ color: 'var(--accent2)' }}>ResNet18 Encoder (stem → layer3)</strong> — pretrained on ImageNet, downsamples the tile 16× to an 8×8×256 bottleneck, the traditional "compressed representation" of an autoencoder.</div>
            <div><strong style={{ color: 'var(--warn)' }}>Skip connections (s0, s1, s2)</strong> — the encoder's intermediate activations, copied directly and concatenated into the matching decoder stage. Without these, the decoder can only rebuild the image from the 8×8 bottleneck alone, which measurably loses fine detail on complex tiles (see below).</div>
            <div><strong style={{ color: 'var(--accent)' }}>Decoder (Up1–Up4)</strong> — four transposed-convolution stages, each concatenating the upsampled features with the corresponding skip before reducing channels back down, trained entirely from scratch.</div>
            <div><strong style={{ color: 'var(--danger)' }}>Denoising objective</strong> — Gaussian noise (σ=0.15) is added to the input; the target is the original clean tile. This forces the network to learn robust, noise-invariant features rather than an identity mapping.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">How to Use This Page</div>
          <ol style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.85rem', color: 'var(--text)' }}>
            <li>Upload any UCMerced tile, or click <strong>Load Real Sample</strong>.</li>
            <li>Click <strong>Run Inference</strong> — noise (σ=0.15) is added automatically before denoising.</li>
            <li>Compare the three panels: your original upload, the noisy input the model actually sees, and its reconstruction.</li>
            <li>Read <strong>MSE</strong> and <strong>PSNR</strong> below — higher PSNR / lower MSE means a closer reconstruction.</li>
          </ol>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">Contribution to UrbanGenAI</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>Real satellite/aerial imagery is often degraded — sensor noise, compression artifacts, atmospheric interference. This model cleans that up <strong>before</strong> it reaches the Classifier or VAE, improving the reliability of every downstream step in the pipeline.</div>
            <div>It also demonstrates the encoder/decoder + reconstruction-loss fundamentals in their cleanest form — no probabilistic latent, no adversarial loss, just compression and reconstruction — the baseline concept the VAE and GAN both build on.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Improvement Over the Standard Baseline</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>Classic denoising autoencoders (Vincent et al., 2008) use shallow, from-scratch encoders on small images. We use a pretrained ResNet18 instead — necessary here since our domain (aerial imagery) differs from ImageNet's natural photos, and we only have 2,100 training tiles to fine-tune with.</div>
            <div>We <strong>measured</strong> the bottleneck-only version of this exact model underperforming on structurally complex classes — 21dB PSNR on dense residential/harbor/mobile-home-park vs. 27–28dB on homogeneous classes like forest — and fixed it with U-Net-style skip connections (Ronneberger et al., 2015, originally proposed for biomedical segmentation, adapted here to denoising).</div>
            <div>Verified, not assumed: retraining with skip connections closed the gap from 7.3dB down to 2.6dB, with the previously-worst classes gaining <strong>over 7dB each</strong> and the 21-class average moving 25dB → 29.7dB.</div>
          </div>
        </div>
      </div>

      <SyllabusTable rows={[
        ['Encoder / Decoder structure', 'ResNet18 encoder + skip-connected CNN decoder, shown above'],
        ['Application: Denoising', 'Training objective is literally denoising — Gaussian noise added to input, clean tile as target'],
        ['Application: Data Compression', 'The 8×8×256 bottleneck is the compressed representation (~3× smaller than raw pixel count)'],
        ['Self-study: Limitations of AEs', 'We measured a real limitation (fine-detail loss on complex scenes from a single bottleneck) and fixed it with skip connections — demonstrated, not just described'],
      ]} />
    </div>
  );
}
