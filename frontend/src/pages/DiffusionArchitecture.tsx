import { Arrow, ArrowheadDef, Box, COLORS, DiagramBackground, EvidenceTable, ProvenanceNote } from '../lib/archDiagram';
import { WorkflowAnimation } from '../lib/WorkflowAnimation';
import { TrainingCurveCard } from '../components/TrainingCurveCard';

export default function DiffusionArchitecture() {
  return (
    <div style={{ marginTop: 28, marginBottom: 30 }}>
      <ProvenanceNote>
        This diagram describes the actual source-conditioned checkpoint loaded by the API: a 2.8M-parameter U-Net,
        1,000-step linear noise schedule, sinusoidal timestep embeddings, land-use class embeddings, and a configurable DDIM sampler.
        The checkpoint and training measurements are persisted under <code>outputs/diffusion_scenario/</code>.
      </ProvenanceNote>

      <WorkflowAnimation
        title="Data flow — source tile and class condition to scenario tile"
        stages={[
          { label: 'Source tile', sub: '128²×3' },
          { label: 'Add Gaussian noise', sub: 'x₀ → xₜ' },
          { label: 'Conditioned U-Net', sub: 'source + t + class' },
          { label: 'Predict noise', sub: 'εθ(xₜ,t,s,c)' },
          { label: 'DDIM reverse', sub: 'configurable steps' },
          { label: 'Scenario tile', sub: '128²×3' },
        ]}
        note="Training learns noise prediction at randomly sampled diffusion timesteps. Inference starts from noise and reverses the process while keeping the uploaded source tile and requested land-use class available to the U-Net."
      />

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Image- and Class-Conditioned DDPM U-Net</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 1180 410" style={{ width: '100%', minWidth: 900, height: 'auto' }} role="img" aria-label="Urban scenario diffusion architecture">
            <defs><ArrowheadDef /></defs>
            <DiagramBackground />

            <Box x={20} y={30} w={145} h={58} fill={COLORS.surface} stroke={COLORS.accent} label="Noisy tile xₜ" sub="128×128×3" labelColor={COLORS.accent} />
            <Arrow x1={165} y1={59} x2={205} y2={59} />
            <Box x={205} y={30} w={170} h={58} fill={COLORS.surface} stroke={COLORS.accent2} label="Condition concat" sub="xₜ + source s" labelColor={COLORS.accent2} />
            <Arrow x1={375} y1={59} x2={415} y2={59} />
            <Box x={415} y={30} w={190} h={58} fill={COLORS.surface} stroke={COLORS.accent2} label="U-Net encoder" sub="128 → 64 → 32 → 16" labelColor={COLORS.accent2} />
            <Arrow x1={605} y1={59} x2={645} y2={59} />
            <Box x={645} y={30} w={150} h={58} fill={COLORS.surface} stroke={COLORS.accent2} label="U-Net bottleneck" sub="residual blocks" labelColor={COLORS.accent2} />
            <Arrow x1={795} y1={59} x2={835} y2={59} />
            <Box x={835} y={30} w={190} h={58} fill={COLORS.surface} stroke={COLORS.accent2} label="U-Net decoder" sub="16 → 32 → 64 → 128" labelColor={COLORS.accent2} />
            <Arrow x1={1025} y1={59} x2={1065} y2={59} />
            <Box x={1065} y={30} w={95} h={58} fill={COLORS.surface} stroke={COLORS.success} label="ε̂" sub="predicted noise" labelColor={COLORS.success} />

            <Box x={260} y={145} w={180} h={56} fill="#12181f" stroke={COLORS.warn} label="Timestep embedding" sub="sinusoidal → MLP" labelColor={COLORS.warn} />
            <Arrow x1={350} y1={145} x2={520} y2={92} />
            <Box x={500} y={145} w={180} h={56} fill="#12181f" stroke={COLORS.warn} label="Class embedding" sub="21 land-use labels" labelColor={COLORS.warn} />
            <Arrow x1={590} y1={145} x2={670} y2={92} />

            <Box x={180} y={260} w={190} h={58} fill={COLORS.surface} stroke={COLORS.border} label="Forward process" sub="βₜ linear, T=1000" />
            <Arrow x1={370} y1={289} x2={410} y2={289} />
            <Box x={410} y={260} w={230} h={58} fill="#1a1408" stroke={COLORS.warn} label="Noise MSE objective" sub="||ε − ε̂θ||²" labelColor={COLORS.warn} />
            <Arrow x1={640} y1={289} x2={680} y2={289} />
            <Box x={680} y={260} w={220} h={58} fill={COLORS.surface} stroke={COLORS.accent} label="DDIM sampler" sub="η-controlled, UI-selected steps" labelColor={COLORS.accent} />
            <Arrow x1={900} y1={289} x2={940} y2={289} />
            <Box x={940} y={260} w={170} h={58} fill={COLORS.surface} stroke={COLORS.success} label="Scenario output" sub="candidate tile" labelColor={COLORS.success} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">What each component does</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 11, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div><strong style={{ color: 'var(--accent)' }}>Source condition</strong> — supplies spatial context from the uploaded tile.</div>
            <div><strong style={{ color: 'var(--warn)' }}>Timestep embedding</strong> — tells the network how much noise is present.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>Class embedding</strong> — supplies the requested one-of-21 land-use condition.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>U-Net</strong> — predicts the noise residual using encoder/decoder features and skip connections.</div>
            <div><strong style={{ color: 'var(--success)' }}>DDIM</strong> — reverses the process in the number of steps selected in the UI.</div>
          </div>
        </div>
        <div className="card">
          <div className="card-title">Measured checkpoint</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, fontSize: '0.83rem' }}>
            <div><span className="metric-label">Parameters</span><div className="metric-value">2.8M</div></div>
            <div><span className="metric-label">Training history</span><div className="metric-value">See live Evaluation</div></div>
            <div><span className="metric-label">Best / final MSE</span><div className="metric-value">See live Evaluation</div></div>
          </div>
        </div>
      </div>

      <TrainingCurveCard
        modelKey="diffusion"
        title="Diffusion Noise-Prediction Training Dynamics"
        description="Measured loss history from the persisted 50-epoch CUDA run. This is noise-prediction MSE, not a pixel reconstruction loss."
        curves={[{ key: 'loss', label: 'Noise Prediction MSE', color: 'var(--accent)' }]}
      />

      <EvidenceTable rows={[
        ['Conditioning', 'Uploaded source tile + one of 21 UCMerced land-use classes'],
        ['Forward process', '1,000-step linear Gaussian noise schedule'],
        ['Reverse model', '2.8M-parameter residual U-Net with timestep and class embeddings'],
        ['Training objective', 'Mean-squared error between injected and predicted noise'],
        ['Inference', 'UI-selected DDIM step count (default 20); η=0 is deterministic, η>0 is stochastic'],
        ['Reproducibility artifacts', 'model.pth, model_best.pth, history.json, meta.json, telemetry.json, training_metrics.png'],
      ]} />
    </div>
  );
}
