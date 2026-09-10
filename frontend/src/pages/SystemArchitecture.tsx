import { Monitor, Server, Cpu, Activity, Database } from 'lucide-react';

// Full-project system architecture: the software stack (not the ML pipeline
// alone). Layered view + component table + request-flow table.

type Layer = {
  n: number;
  name: string;
  icon: typeof Monitor;
  color: string;
  parts: { name: string; tech: string; role: string }[];
};

const LAYERS: Layer[] = [
  {
    n: 1, name: 'Client Layer', icon: Monitor, color: 'var(--cat-a)',
    parts: [
      { name: 'React SPA (Vite)', tech: 'React + TypeScript', role: 'Landing page, one page per model, Evaluation dashboard, light/dark theme' },
      { name: 'API helper', tech: 'fetch + localStorage', role: 'Adds the operator API key (if set) to every request; nothing else leaves the browser' },
    ],
  },
  {
    n: 2, name: 'API Layer', icon: Server, color: 'var(--cat-b)',
    parts: [
      { name: 'FastAPI app', tech: 'FastAPI + Uvicorn', role: 'REST endpoints: /infer/*, /evaluate/*, /generate/plan, /sample/*, /status, /history/*' },
      { name: 'Security middleware', tech: 'slowapi, custom deps', role: 'Optional API-key auth, rate limiting, CORS allow-list, image-upload validation' },
    ],
  },
  {
    n: 3, name: 'Model Services', icon: Cpu, color: 'var(--cat-c)',
    parts: [
      { name: 'Denoising AE', tech: 'PyTorch, ResNet18 + U-Net decoder', role: 'Reconstruct a clean tile from a noisy one' },
      { name: 'Spatial VAE', tech: 'PyTorch, ResNet18 + μ/logσ² heads', role: 'Reconstruct + anomaly z-score + latent interpolation' },
      { name: 'Conditional DCGAN', tech: 'PyTorch, spectral-norm, EMA', role: 'Generate class-conditional synthetic tiles' },
      { name: 'MiniGPT', tech: 'PyTorch, 4-layer Transformer', role: 'Draft a planning recommendation from Pune stats' },
      { name: 'Land-Use Classifier', tech: 'PyTorch, ResNet18 + FC', role: 'Predict 1 of 21 zoning classes' },
    ],
  },
  {
    n: 4, name: 'Evaluation Layer', icon: Activity, color: 'var(--cat-d)',
    parts: [
      { name: 'compute_*_evaluation()', tech: 'runs once at startup', role: 'Held-out PSNR/SSIM/MSE, KL, perplexity, recognition rate, confusion matrix — cached in memory' },
      { name: '/evaluate/<model>', tech: 'GET endpoints', role: 'Serve the cached metrics to the frontend Evaluation dashboard and Model Comparison page' },
    ],
  },
  {
    n: 5, name: 'Data & Artifacts', icon: Database, color: 'var(--cat-f)',
    parts: [
      { name: 'Image datasets', tech: 'UCMerced (21×100), EuroSAT', role: 'Training + held-out evaluation tiles' },
      { name: 'Pune PMC GIS', tech: 'GeoPandas / OSM shapefiles', role: 'Buildings, roads, land-use, waterways — seed the MiniGPT prompt' },
      { name: 'Committed checkpoints', tech: 'outputs/*/model.pth + history.json', role: 'Loaded once at backend startup; the single source of truth for every claim' },
      { name: 'Text corpus', tech: 'backend/corpus/urban_planning.txt', role: 'Hand-authored MiniGPT training data (90/10 split)' },
    ],
  },
];

const FLOW: { step: string; path: string; what: string }[] = [
  { step: '1', path: 'Browser → FastAPI', what: 'User uploads a tile / picks a class / asks for a plan (multipart or JSON).' },
  { step: '2', path: 'Security middleware', what: 'API-key check (if enabled), rate-limit, CORS, validate the image. Upload is held in memory only — never written to disk.' },
  { step: '3', path: 'Router → Model Service', what: 'The endpoint dispatches to the matching model (AE / VAE / GAN / MiniGPT / Classifier).' },
  { step: '4', path: 'Model Service (in memory)', what: 'Uses the checkpoint already loaded at startup; runs one forward pass on CPU/GPU.' },
  { step: '5', path: 'Post-processing', what: 'Anomaly z-score vs baseline · PSNR/SSIM · softmax · decode generated text / image.' },
  { step: '6', path: 'FastAPI → Browser', what: 'JSON (numbers, labels) or a base64 PNG. The React page renders the result and the input→output animation.' },
  { step: '0', path: 'Startup, once', what: 'Every checkpoint is loaded and every /evaluate metric is computed and cached, so requests are fast and numbers are consistent.' },
];

export default function SystemArchitecture() {
  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">System Architecture</h1>
        <div className="panel-desc">
          The whole project as a layered software stack — client, API, the five model services, the
          evaluation layer, and the data / checkpoint layer underneath — plus the request flow through it.
        </div>
      </div>

      {/* Layered diagram */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Layered view</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {LAYERS.map(layer => {
            const Icon = layer.icon;
            return (
              <div key={layer.n} style={{
                border: `1px solid var(--border)`, borderLeft: `4px solid ${layer.color}`,
                borderRadius: 6, background: 'var(--bg)', padding: '12px 14px',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 9, marginBottom: 10 }}>
                  <Icon size={16} color={layer.color} />
                  <span style={{ fontWeight: 700, color: 'var(--text)', fontSize: '0.92rem' }}>
                    {layer.n}. {layer.name}
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: 8 }}>
                  {layer.parts.map(pt => (
                    <div key={pt.name} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 5, padding: '9px 11px' }}>
                      <div style={{ fontWeight: 600, fontSize: '0.82rem', color: 'var(--text)' }}>{pt.name}</div>
                      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: layer.color, margin: '2px 0 4px' }}>{pt.tech}</div>
                      <div style={{ fontSize: '0.76rem', color: 'var(--muted)', lineHeight: 1.45 }}>{pt.role}</div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
        <div style={{ marginTop: 12, fontSize: '0.78rem', color: 'var(--muted)', lineHeight: 1.5 }}>
          Data flows <strong>down</strong> on a request (client → API → model → data/checkpoint) and the
          result flows back <strong>up</strong>. The Evaluation layer is populated once at startup and then
          only read.
        </div>
      </div>

      {/* Component table */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Components</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', minWidth: 820, borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ background: 'var(--surface-inset)', textAlign: 'left', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.05em', fontSize: '0.7rem' }}>
                <th style={{ padding: '10px 12px' }}>Layer</th>
                <th style={{ padding: '10px 12px' }}>Component</th>
                <th style={{ padding: '10px 12px' }}>Technology</th>
                <th style={{ padding: '10px 12px' }}>Responsibility</th>
              </tr>
            </thead>
            <tbody>
              {LAYERS.flatMap(layer => layer.parts.map((pt, i) => (
                <tr key={layer.n + pt.name} style={{ borderTop: '1px solid var(--border)', verticalAlign: 'top' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 600, color: 'var(--text)', whiteSpace: 'nowrap' }}>{i === 0 ? `${layer.n}. ${layer.name}` : ''}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--text)' }}>{pt.name}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--accent)', fontFamily: 'var(--font-mono)', fontSize: '0.74rem' }}>{pt.tech}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--muted)' }}>{pt.role}</td>
                </tr>
              )))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Flow table */}
      <div className="card">
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Request flow</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', minWidth: 780, borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ background: 'var(--surface-inset)', textAlign: 'left', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.05em', fontSize: '0.7rem' }}>
                <th style={{ padding: '10px 12px' }}>Step</th>
                <th style={{ padding: '10px 12px' }}>Path</th>
                <th style={{ padding: '10px 12px' }}>What happens</th>
              </tr>
            </thead>
            <tbody>
              {FLOW.map(f => (
                <tr key={f.step} style={{ borderTop: '1px solid var(--border)', verticalAlign: 'top', background: f.step === '0' ? 'var(--hover-overlay)' : 'transparent' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 700, color: 'var(--accent2)', fontFamily: 'var(--font-mono)' }}>{f.step}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--text)', whiteSpace: 'nowrap' }}>{f.path}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--muted)' }}>{f.what}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: 10, fontSize: '0.76rem', color: 'var(--muted)' }}>
          Ethical safeguard: uploads are processed in memory and never stored; only public data and open GIS are used.
        </div>
      </div>
    </div>
  );
}
