import React from 'react';
import { Box, Arrow, ArrowheadDef, SyllabusTable, ProvenanceNote, COLORS } from '../lib/archDiagram';

export default function ClassifierArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <div style={{
        display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 20,
        padding: '12px 16px', borderRadius: 6, background: 'rgba(255, 184, 77, 0.06)',
        border: '1px solid rgba(255, 184, 77, 0.3)', fontSize: '0.85rem',
      }}>
        <strong style={{ color: 'var(--warn)', flexShrink: 0 }}>Not a syllabus-required model:</strong>
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

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Fine-Tuned ResNet18 Classifier</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 820 100" style={{ width: '100%', minWidth: 720, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>
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
            <div><strong>98.1% validation accuracy</strong>, val loss ≈ 0.10, over 30 epochs on a 90/10 split of UCMerced's 2,100 tiles.</div>
            <div>Transfer learning from ImageNet is standard practice for small datasets like this one (100 images/class) — training a CNN of this depth from scratch on 2,100 images would badly overfit.</div>
          </div>
        </div>
      </div>

      <SyllabusTable rows={[
        ['Not counted toward the 4-model requirement', 'Explicitly disclaimed — discriminative CNN, not one of AE/VAE/GAN/Transformer'],
        ['Supporting role in the pipeline', 'Provides the initial land-use label that the VAE and MiniGPT stages build on'],
      ]} />
    </div>
  );
}
