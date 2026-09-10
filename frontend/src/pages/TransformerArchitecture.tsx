// TransformerArchitecture component
import { Box, Arrow, ArrowheadDef, SyllabusTable, ProvenanceNote, DiagramBackground, COLORS } from '../lib/archDiagram';
import { WorkflowAnimation } from '../lib/WorkflowAnimation';

export default function TransformerArchitecture() {
  return (
    <div style={{ marginBottom: 30 }}>
      <ProvenanceNote>
        MiniGPT was built and trained entirely from scratch by us — <strong>no pretrained weights
        at all</strong> (unlike the AE/VAE/Classifier's ResNet18 backbones). Every parameter — token
        embeddings, positional embeddings, all four attention/MLP blocks, the output head — is
        learned from <code>backend/corpus/urban_planning.txt</code>, a corpus we hand-authored
        ourselves, via <code>train_gpt.py</code>. The checkpoint (<code>outputs/gpt/model.pth</code>) is
        entirely our own.
      </ProvenanceNote>

      <WorkflowAnimation
        title="Data flow — Pune land-use stats in, planning recommendation out"
        stages={[
          { label: 'Real Pune stats', sub: 'built-up %, roads…' },
          { label: 'Prompt string', sub: 'char-tokenized' },
          { label: 'Token + pos embed', sub: 'n_embd 256' },
          { label: '4× causal blocks', sub: 'masked self-attn' },
          { label: 'LM head', sub: 'next-char probs' },
          { label: 'Recommendation', sub: 'sampled text' },
        ]}
        note="Real ward statistics are formatted into a prompt, tokenized one character at a time, and the
        decoder-only transformer generates the recommendation character-by-character, each step attending only
        to earlier positions (causal mask). Held-out perplexity ≈ 1.09 — the corpus is small and templated by
        design, so the model reliably follows its structure (see the Evaluation page)."
      />

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Architecture — Decoder-Only Transformer (MiniGPT)</div>
        <div style={{ width: '100%', overflowX: 'auto' }}>
          <svg viewBox="0 0 980 360" style={{ width: '100%', minWidth: 880, height: 'auto' }}>
            <defs><ArrowheadDef /></defs>
            <DiagramBackground />

            <text x={20} y={12} fontSize="11" fontWeight={700} fill={COLORS.text}>MAIN PIPELINE</text>
            <Box x={20} y={20} w={130} h={56} fill={COLORS.surface} stroke={COLORS.border} label="Char Tokens" sub="context ≤192" />
            <Arrow x1={150} y1={48} x2={182} y2={48} />
            <Box x={182} y={20} w={200} h={56} fill={COLORS.surface} stroke={COLORS.accent2} label="Token + Positional Embed" sub="256-dim, summed" labelColor={COLORS.accent2} />
            <Arrow x1={382} y1={48} x2={408} y2={48} />
            <Box x={408} y={20} w={190} h={56} fill="#12181f" stroke={COLORS.accent} label="Transformer Block × 4" sub="detail below" labelColor={COLORS.accent} />
            <Arrow x1={598} y1={48} x2={624} y2={48} />
            <Box x={624} y={20} w={150} h={56} fill={COLORS.surface} stroke={COLORS.border} label="Final LayerNorm" />
            <Arrow x1={774} y1={48} x2={800} y2={48} />
            <Box x={800} y={20} w={160} h={56} fill={COLORS.surface} stroke={COLORS.success} label="LM Head" sub="weight-tied, → 128 chars" labelColor={COLORS.success} />

            <path d="M 880,76 L 880,110 Q 880,130 700,130 L 260,130 Q 100,130 100,90 L 100,80"
              fill="none" stroke={COLORS.warn} strokeWidth={1.5} strokeDasharray="4,4" markerEnd="url(#arrowhead)" />
            <text x={490} y={124} fontSize="9.5" fill={COLORS.warn} textAnchor="middle">autoregressive: sample next char (temperature=0.8, top-k=40) → append → repeat</text>

            <text x={20} y={172} fontSize="11" fontWeight={700} fill={COLORS.accent}>INSIDE EACH OF THE 4 IDENTICAL BLOCKS — pre-norm, residual</text>
            <Box x={20} y={182} w={430} h={56} fill={COLORS.surface} stroke={COLORS.accent2}
              label="LayerNorm → Causal Multi-Head Self-Attention (4 heads, masked)"
              sub="x = x + Attn(LN(x))" labelColor={COLORS.accent2} />
            <Arrow x1={450} y1={210} x2={482} y2={210} />
            <Box x={482} y={182} w={430} h={56} fill={COLORS.surface} stroke={COLORS.accent2}
              label="LayerNorm → MLP: Linear(256→1024) → GELU → Linear(1024→256)"
              sub="x = x + MLP(LN(x))" labelColor={COLORS.accent2} />

            <line x1={490} y1={254} x2={490} y2={286} stroke={COLORS.warn} strokeWidth={1.25} strokeDasharray="3,3" />
            <Box x={130} y={286} w={720} h={56} fill="#1a1408" stroke={COLORS.warn}
              label="Loss = cross-entropy(next-char logits, true next char)"
              sub="4 layers · 4 heads · 256-dim embeddings · 192-char context · ~128-char vocabulary" labelColor={COLORS.warn} />
          </svg>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">What Each Component Does</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div><strong style={{ color: 'var(--accent2)' }}>Token + Positional Embedding</strong> — each character maps to a 256-dim vector; a separate learned embedding per position (up to 192) is added, since attention alone has no notion of order.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>Causal self-attention</strong> — each position attends to itself and all earlier positions only, via a lower-triangular mask — this is what makes it a valid <em>generative</em>, left-to-right model rather than a bidirectional encoder like BERT.</div>
            <div><strong style={{ color: 'var(--accent2)' }}>MLP sub-layer</strong> — a per-position 2-layer network (256→1024→256, GELU) that processes what attention gathered.</div>
            <div><strong style={{ color: 'var(--success)' }}>Weight-tied LM head</strong> — the output projection reuses the token-embedding matrix rather than learning a separate one, halving that layer's parameters.</div>
            <div><strong style={{ color: 'var(--warn)' }}>Sampling</strong> — temperature (0.8) and top-k (40) filtering at generation time control how conservative vs. varied the drafted text is.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">How to Use This Page</div>
          <ol style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.85rem', color: 'var(--text)' }}>
            <li>Open <strong>Urban Plan Generator</strong> from the sidebar.</li>
            <li>Pick one of the preset ward contexts (built from real Pune land-use statistics), or write your own.</li>
            <li>Click <strong>Generate</strong> — MiniGPT drafts a recommendation one character at a time, conditioned on everything generated so far.</li>
            <li>Treat the output as an advisory draft for planner review, not a final decision — see Limitations.</li>
          </ol>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">Contribution to UrbanGenAI</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>This is the step that turns <em>analysis</em> into an <em>actionable recommendation</em>: the Classifier says what a parcel is, the VAE says whether it's typical, and MiniGPT drafts what a planner might actually write about it — grounded in real Pune statistics (built-up %, green cover, road network, drainage) rather than a generic template.</div>
            <div><strong>Limitation, stated plainly:</strong> a small model on a small, hand-authored corpus is fluent-sounding but has no factual grounding and can self-contradict — it is an advisory drafting aid for a human planner to review, not an autonomous decision-maker.</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Improvement Over the Standard Baseline</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: '0.85rem', color: 'var(--text)' }}>
            <div>This follows the standard decoder-only Transformer recipe (Vaswani et al., 2017, "Attention Is All You Need"; GPT/GPT-2-style causal architecture) rather than inventing a new mechanism — the honest claim here isn't architectural novelty.</div>
            <div>The deliberate choice we made is scope: rather than calling a large pretrained LLM API (which would satisfy the "transformer" requirement in name only, with none of the internals ours to explain), we built and trained every layer ourselves, small enough to fully train on a laptop GPU in minutes, so every design decision — causal masking, weight tying, the depth/width tradeoff at 4 layers × 256-dim — is something we chose and can defend, not a black box we called.</div>
            <div>We also scoped the training data deliberately: a small, hand-authored, domain-specific corpus rather than generic web text, so the model's limited capacity is spent on urban-planning vocabulary and structure specifically, not diluted across general language.</div>
          </div>
        </div>
      </div>

      <SyllabusTable rows={[
        ['Self-attention mechanism', 'Causal multi-head self-attention, implemented from scratch and diagrammed above'],
        ['Positional encoding', 'Learned positional embeddings, summed with token embeddings'],
        ['Transformer-based generative model (GPT-style)', 'Decoder-only, autoregressive, next-token cross-entropy — the architecture family GPT-2/GPT-3 belong to'],
        ['Correct model naming', 'The separate Land-Use Classifier is explicitly labeled a CNN, not a transformer — this MiniGPT is what actually satisfies the Unit 4 requirement'],
      ]} />
    </div>
  );
}
