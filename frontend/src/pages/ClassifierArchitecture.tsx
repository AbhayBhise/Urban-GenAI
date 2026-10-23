import { Box, Arrow, ArrowheadDef, EvidenceTable, ProvenanceNote, DiagramBackground, COLORS } from '../lib/archDiagram';
import { WorkflowAnimation } from '../lib/WorkflowAnimation';
import { TrainingCurveCard } from '../components/TrainingCurveCard';

export default function ClassifierArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <div style={{
        display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 20,
        padding: '12px 16px', borderRadius: 6, background: 'rgba(255, 184, 77, 0.06)',
        border: '1px solid rgba(255, 184, 77, 0.3)', fontSize: '0.85rem',
      }}>
        <strong style={{ color: 'var(--warn)', flexShrink: 0 }}>Supporting model:</strong>
        <span style={{ color: 'var(--text)' }}>
          This is a discriminative CNN, kept because automated zoning classification is genuinely
          useful project work — it is <strong>not</strong> a substitute for the transformer
          requirement, which is satisfied separately by MiniGPT (see the Urban Plan Generator page).
          We label it honestly rather than calling a CNN a transformer.
        </span>
      </div>

      <ProvenanceNote>
        Trained end-to-end on UCMerced by our own <code>train_transformer.py</code> (30 epochs).
        The ResNet18 backbone starts from ImageNet-pretrained weights but is fine-tuned entirely on
        our data; the final classification layer is trained from scratch by us.
      </ProvenanceNote>

      <WorkflowAnimation
        title="Data flow — land tile in, zoning label out"
        stages={[
          { label: 'Input tile', sub: '224²×3' },
          { label: 'ResNet18 backbone', sub: 'fine-tuned' },
          { label: 'Global avg pool', sub: '→ 512-d' },
          { label: 'Linear head', sub: '512 → 21' },
          { label: 'Zoning label', sub: 'softmax, 1 of 21' },
        ]}
        note="A discriminative pass: the fine-tuned backbone extracts a 512-d feature vector, the from-scratch
        linear head maps it to 21 land-use logits, and softmax gives the predicted zoning class. This label is
        what the VAE and MiniGPT stages downstream act on. Measured performance is shown in the live Evaluation view."
      />

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Fine-Tuned ResNet18 Classifier</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 820 100" style={{ width: '100%', minWidth: 720, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>
            <DiagramBackground />
            <Box x={20} y={20} w={130} h={56} fill={COLORS.surface} stroke={COLORS.border} label="Input Tile" sub="224×224×3" />
            <Arrow x1={150} y1={48} x2={182} y2={48} />
            <Box x={182} y={20} w={220} h={56} fill={COLORS.surface} stroke={COLORS.accent2} label="ResNet18 (fine-tuned)" sub="ImageNet-pretrained backbone" labelColor={COLORS.accent2} />
            <Arrow x1={402} y1={48} x2={434} y2={48} />
            <Box x={434} y={20} w={170} h={56} fill={COLORS.surface} stroke={COLORS.accent} label="FC Head" sub="512 → 21 classes" labelColor={COLORS.accent} />
            <Arrow x1={604} y1={48} x2={636} y2={48} />
            <Box x={636} y={20} w={160} h={56} fill={COLORS.surface} stroke={COLORS.success} label="Softmax" sub="top-5 predictions" labelColor={COLORS.success} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">How to Use / Contribution</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>Upload any UCMerced-style tile and click <strong>Run Classification</strong> — the top-5 predicted zoning categories with confidence percentages appear immediately.</div>
            <div>This is the first stage of the project's pipeline: it labels what a parcel currently is, before the VAE checks whether that pattern looks typical and MiniGPT drafts a recommendation.</div>
          </div>
        </div>
        <div className="card">
          <div className="card-title">Result &amp; Why ResNet18</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>Training history and the live representative evaluation are shown in the Training and Evaluation views; they are reported separately because they use different protocols.</div>
            <div>Transfer learning from ImageNet is standard practice for small datasets like this one (100 images/class) — training a CNN of this depth from scratch on 2,100 images would badly overfit.</div>
          </div>
        </div>
      </div>

      <TrainingCurveCard
        modelKey="transformer"
        title="Land-Use Classifier Training Dynamics (30 Epochs)"
        description="Training loss (cross-entropy), validation loss, and validation accuracy across 30 fine-tuning epochs on UCMerced. Use only with the persisted fixed validation split; representative runtime samples are diagnostic."
        curves={[
          { key: 'loss', label: 'Train Loss', color: 'var(--accent)' },
          { key: 'val_loss', label: 'Validation Loss', color: 'var(--accent2)' },
          { key: 'val_accuracy', label: 'Validation Accuracy', color: 'var(--success)' },
        ]}
      />

      <EvidenceTable rows={[
        ['Supporting model boundary', 'Discriminative CNN used for land-use verification and GAN recognition evaluation'],
        ['Supporting role in the pipeline', 'Provides the initial land-use label that the VAE and MiniGPT stages build on'],
      ]} />
    </div>
  );
}
