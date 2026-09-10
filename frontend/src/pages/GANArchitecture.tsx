// GANArchitecture component
import { Box, Arrow, ArrowheadDef, SyllabusTable, ProvenanceNote, DiagramBackground, COLORS } from '../lib/archDiagram';
import { WorkflowAnimation } from '../lib/WorkflowAnimation';

export default function GANArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <ProvenanceNote>
        This Conditional DCGAN was trained end-to-end on UCMerced by our own <code>train_gan.py</code>
        — 100 epochs, from a random initialization (no pretrained weights at all; unlike the AE/VAE/
        Classifier, a GAN generator has no equivalent "ImageNet head start" to build on). It was
        flagged as the top-priority untrained component in the project's own contributing guide;
        we trained it, verified the result, and committed the weights (<code>outputs/gan/generator_ema.pth</code>).
      </ProvenanceNote>

      <WorkflowAnimation
        title="Data flow — class label + noise in, synthetic tile out"
        stages={[
          { label: 'Noise z', sub: '128-dim' },
          { label: 'Class label', sub: '1 of 21 → embed' },
          { label: 'Generator', sub: '4× ConvTranspose' },
          { label: 'Synthetic tile', sub: '128²×3' },
          { label: 'Classifier check', sub: 'recognized?' },
        ]}
        note="A random vector and a chosen land-use class are fed to the generator, which paints a
        128×128 tile of that class. At inference we use the EMA generator only — the discriminator is a
        training-time critic. Generated tiles are scored by running them back through the Land-Use Classifier
        (recognition rate ≈ 15% overall at 100 epochs; strong on texture-distinctive classes, weak on
        fine grid geometry — see the Evaluation page)."
      />

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Class-Conditional DCGAN</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 940 420" style={{ width: '100%', minWidth: 840, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>
            <DiagramBackground />

            {/* ---- Generator (top) ---- */}
            <text x={20} y={12} fontSize="11" fontWeight={700} fill={COLORS.accent}>GENERATOR</text>
            <Box x={20} y={20} w={110} h={40} fill="#12181f" stroke={COLORS.accent} label="Noise z" sub="128-dim" labelColor={COLORS.accent} />
            <Box x={20} y={68} w={110} h={40} fill="#12181f" stroke={COLORS.accent} label="Class Embed" sub="64-dim" labelColor={COLORS.accent} />
            <Arrow x1={130} y1={40} x2={162} y2={55} color={COLORS.accent} />
            <Arrow x1={130} y1={88} x2={162} y2={65} color={COLORS.accent} />
            <Box x={162} y={38} w={160} h={50} fill={COLORS.surface} stroke={COLORS.accent2} label="Linear + Reshape" sub="8×8×512" labelColor={COLORS.accent2} />
            <Arrow x1={322} y1={63} x2={354} y2={63} />
            <Box x={354} y={38} w={210} h={50} fill={COLORS.surface} stroke={COLORS.accent2} label="4× ConvTranspose2d (BN+ReLU)" sub="8→16→32→64→128" labelColor={COLORS.accent2} />
            <Arrow x1={564} y1={63} x2={596} y2={63} />
            <Box x={596} y={38} w={170} h={50} fill={COLORS.surface} stroke={COLORS.success} label="Tanh → Fake Tile" sub="128×128×3" labelColor={COLORS.success} />

            <Arrow x1={681} y1={88} x2={681} y2={150} color={COLORS.success} />
            <text x={695} y={125} fontSize="9.5" fill={COLORS.success}>feeds D as "fake"</text>

            {/* ---- Discriminator (bottom) ---- */}
            <text x={20} y={144} fontSize="11" fontWeight={700} fill={COLORS.danger}>DISCRIMINATOR — spectral-normalized every layer</text>
            <Box x={20} y={152} w={150} h={40} fill="#1f0a0a" stroke={COLORS.danger} label="Real Tile" sub="from UCMerced" labelColor={COLORS.danger} />
            <Box x={190} y={152} w={150} h={40} fill="#1f0a0a" stroke={COLORS.success} label="Fake Tile" sub="from Generator" labelColor={COLORS.success} />
            <Box x={20} y={200} w={320} h={36} fill="#12181f" stroke={COLORS.warn} label="+ Class Embed → 128×128×1 map (concat)" labelColor={COLORS.warn} />
            <Arrow x1={360} y1={218} x2={392} y2={218} />
            <Box x={392} y={195} w={230} h={50} fill={COLORS.surface} stroke={COLORS.accent2} label="5× SN-Conv2d (LeakyReLU)" sub="128→64→32→16→8→4" labelColor={COLORS.accent2} />
            <Arrow x1={622} y1={220} x2={654} y2={220} />
            <Box x={654} y={195} w={170} h={50} fill={COLORS.surface} stroke={COLORS.border} label="Real / Fake Logit" sub="scalar, pre-sigmoid" />

            {/* Loss annotation */}
            <line x1={490} y1={251} x2={490} y2={286} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <Box x={130} y={286} w={720} h={60} fill="#1a1408" stroke={COLORS.warn}
              label="Adversarial loss: non-saturating BCE, label smoothing (real target 0.9, fake target 0.1)"
              sub="D trained 2 steps per G step; G's weights EMA-averaged (decay 0.999) — used for all inference" labelColor={COLORS.warn} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">What Each Component Does</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div><strong style={{ color: 'var(--accent)' }}>Class embedding</strong> — a learned 64-dim vector per land-use class, concatenated into both G and D. This is what lets one Generator produce 21 visually distinct classes instead of one blurry average.</div>
            <div><strong style={{ color: 'var(--accent2) ' }}>Generator</strong> — projects noise+class to an 8×8×512 seed, then 4 transposed-conv stages upsample to a full 128×128 RGB tile.</div>
            <div><strong style={{ color: 'var(--danger)' }}>Discriminator</strong> — the class embedding is projected to a 128×128 single-channel map and concatenated onto the image before the first conv, so it judges "is this real <em>for this specific class</em>," not just "real or fake."</div>
            <div><strong style={{ color: 'var(--accent2)' }}>Spectral normalization</strong> — applied to every Discriminator layer; constrains its Lipschitz constant, which stabilizes adversarial training and helps prevent mode collapse on a small dataset like this (21 classes × 100 images each).</div>
            <div><strong style={{ color: 'var(--success)' }}>EMA generator</strong> — an exponential moving average of the Generator's weights is kept separately and used for all inference/sample generation — smoother, higher-quality outputs than the raw, noisier training-time weights.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">How to Use This Page</div>
          <ol style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.85rem', color: 'var(--text)' }}>
            <li>Pick any of the 21 UCMerced classes from the dropdown/grid.</li>
            <li>Click <strong>Generate</strong> — no input image needed, this is unconditional-on-content generation from noise.</li>
            <li>Use <strong>Generate Grid</strong> to see one sample per class at once — a fast way to compare quality across classes.</li>
            <li>Compare texture-distinctive classes (harbor) against grid-geometry classes (freeway, intersection) — see the honest limitation note below.</li>
          </ol>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">Contribution to UrbanGenAI</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>The GAN generates <strong>synthetic tiles for any of the 21 classes on demand</strong> — a data-augmentation and scenario-exploration tool distinct from the VAE (which only reconstructs/interpolates real, encoded tiles). It can produce novel examples of a class the other models only ever see through the fixed 2,100-tile dataset.</div>
            <div><strong>Honest limitation:</strong> at 100 epochs on this dataset size, texture-distinctive classes like harbor already show real water/dock structure. Classes needing precise repeated geometry — a residential grid, a road intersection — are still color-and-texture fields rather than crisp layouts. That's expected: GANs typically need far more epochs or data to learn geometric structure than to learn texture statistics, and we report it rather than only showing the good outputs.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Improvement Over the Standard Baseline</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>The original GAN (Goodfellow et al., 2014) has no class conditioning and is notoriously unstable to train. We build on two specific, well-established extensions rather than the vanilla recipe: the DCGAN convolutional architecture (Radford et al., 2015) and class-conditioning via label embedding (Mirza &amp; Osindero, 2014, Conditional GANs).</div>
            <div>On top of that base recipe, three additions specifically target this project's failure mode — a small, 21-class dataset (100 images/class) where vanilla GANs are prone to mode collapse: <strong>spectral normalization</strong> on every Discriminator layer, <strong>label smoothing</strong> (0.9/0.1 instead of hard 1/0 targets) to prevent Discriminator overconfidence, and an <strong>EMA-averaged Generator</strong> for inference. None of these are novel research contributions — they're standard, well-documented GAN-stabilization techniques — but choosing this specific combination, for this specific small-dataset failure mode, was a deliberate design decision, not a default.</div>
          </div>
        </div>
      </div>

      <SyllabusTable rows={[
        ['Generator / Discriminator structure', 'Shown above — class-conditional DCGAN, both networks diagrammed exactly as implemented'],
        ['Adversarial loss, minimax optimization', 'Non-saturating BCE with label smoothing; D trained 2 steps per G step'],
        ['Type: Deep Convolutional GAN (DCGAN)', 'This is explicitly a DCGAN — the standard convolutional G/D recipe named in the syllabus'],
        ['Type: Conditional GAN', 'Class-conditioning via learned embeddings in both G and D'],
        ['Challenges: mode collapse', 'Spectral normalization + label smoothing specifically address this on a small (100 images/class) dataset'],
      ]} />
    </div>
  );
}
