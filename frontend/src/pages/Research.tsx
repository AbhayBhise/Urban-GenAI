import React from 'react';

const SECTIONS = [
  {
    unit: 'Unit 2 — Autoencoders & VAEs',
    body: [
      'The Autoencoder is a denoising AE: a pretrained ResNet18 encoder compresses a 128×128 tile to an 8×8×256 feature map, and a transposed-conv decoder reconstructs a clean image from a noised input. It demonstrates the AE applications from the syllabus — compression and denoising.',
      'The VAE adds a probabilistic latent: the encoder outputs μ and logσ², and the reparameterization trick z = μ + σ·ε keeps sampling differentiable. The objective is reconstruction + β·KL, where KL(q(z|x) ‖ N(0, I)) is reported per inference in the UI and plotted during training.',
      'This build prioritises reconstruction (β≈0), which powers reconstruction-error anomaly detection and clean latent interpolation between two real tiles — the working demonstration that the latent space is smooth. Under a near-zero β the KL value rises during training rather than falling (the latent grows more informative); a prior-matched checkpoint for unconditional sampling collapsed at every workable β on this encoder/decoder within the project timeframe, a documented β-VAE trade-off.',
    ],
  },
  {
    unit: 'Unit 4 — Transformer-based Generative Models',
    body: [
      'The Urban Plan Generator is a decoder-only Transformer (MiniGPT) built from scratch — no pretrained weights. It uses token + learned positional embeddings and 4 pre-norm blocks of causal multi-head self-attention + MLP, with a weight-tied language-model head.',
      'It is trained character-level on an urban-planning corpus and generates autoregressively with temperature and top-k sampling. Prompts are seeded from real Pune land-use statistics, so the model produces context-specific sustainability recommendations for planner review.',
      'The ResNet18 land-use classifier is retained as a separate tool — it is a CNN, not a transformer, and is labelled as such.',
    ],
  },
  {
    unit: 'Unit 6 — Ethical, Societal & Legal Dimensions',
    body: [
      'The deployment carries API-key authentication, a CORS allow-list, per-client rate limiting, and in-memory-only upload handling (nothing is written to disk).',
      'Governance documentation covers GDPR, the India DPDP Act 2023, and the EU AI Act (limited-risk / transparency), plus an explicit bias disclosure: the vision models are trained on US/EU imagery and applied to Pune.',
      'All generated output is labelled as AI-generated and advisory, and a model card reports each model\'s data, metrics, limitations, and approximate carbon footprint.',
    ],
  },
];

export default function Research() {
  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Research &amp; Context</h1>
        <div className="panel-desc">
          How UrbanGen AI maps to the Generative AI syllabus, and the architecture
          choices actually used in this implementation.
        </div>
      </div>

      {SECTIONS.map(s => (
        <div className="card" key={s.unit} style={{ marginBottom: 22 }}>
          <div className="card-title">{s.unit}</div>
          {s.body.map((p, i) => (
            <p key={i} style={{ color: 'var(--text)', fontSize: '0.9rem', lineHeight: 1.65, marginBottom: 12 }}>{p}</p>
          ))}
        </div>
      ))}

      <div className="card">
        <div className="card-title">Key references</div>
        <ul style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.8, paddingLeft: 20 }}>
          <li>Kingma &amp; Welling (2014), <em>Auto-Encoding Variational Bayes</em> — the VAE and reparameterization trick.</li>
          <li>Vaswani et al. (2017), <em>Attention Is All You Need</em> — the Transformer architecture.</li>
          <li>Radford et al. (2019), <em>Language Models are Unsupervised Multitask Learners</em> (GPT-2) — decoder-only LM.</li>
          <li>EU AI Act (2024); EU GDPR (2016); India DPDP Act (2023).</li>
        </ul>
      </div>
    </div>
  );
}
