import { useState, useEffect } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import { Activity } from 'lucide-react';
import { apiFetch } from '../../lib/api';

interface TimelineStep {
  step: string;
  title: string;
  status: 'implemented' | 'in_development' | 'planned';
  statusLabel: string;
  description: string;
  verification: string;
}

const TIMELINE: TimelineStep[] = [
  {
    step: '01',
    title: 'Literature & Problem Definition',
    status: 'implemented',
    statusLabel: 'Verified ✓',
    description: 'Scoping review of 7 foundational publications spanning urban digital twins, generative design, and LLM-assisted urban planning.',
    verification: 'Documented in frontend Research section, README.md, and docs/MODEL_CARD.md.',
  },
  {
    step: '02',
    title: 'Pune Data Acquisition',
    status: 'implemented',
    statusLabel: 'Verified ✓',
    description: 'Ingestion of Pune PMC spatial vectors (OSM buildings, land-use, roads, waterways, and natural areas).',
    verification: 'GeoPandas shapefile pipeline in backend/rag_pipeline.py parsing 5 Pune layers.',
  },
  {
    step: '03',
    title: 'Multi-source Data Alignment',
    status: 'in_development',
    statusLabel: 'In Development ◐',
    description: 'Coordinate reference system normalization (EPSG:3857) and spatial rasterization scaffolding.',
    verification: 'CRS conversion active in rag_pipeline.py; full automated multi-raster resampler in progress.',
  },
  {
    step: '04',
    title: 'City Stack Tensor Construction',
    status: 'planned',
    statusLabel: 'Planned Roadmap ○',
    description: '5-source raster-vector tensor stacking (HLS + WorldCover + OSM + DEM + WorldPop) into H×W×C array.',
    verification: 'Architectural specifications detailed in README.md (Phases 1–8).',
  },
  {
    step: '05',
    title: 'Multi-Channel Patch Extraction',
    status: 'planned',
    statusLabel: 'Planned Roadmap ○',
    description: 'Automated sliding-window patch extraction across aligned City Stack with train/val/test splits.',
    verification: 'Tile processing pipeline stubs in src/urbangen/patches/.',
  },
  {
    step: '06',
    title: 'Convolutional Autoencoder (AE)',
    status: 'implemented',
    statusLabel: 'Verified ✓',
    description: 'ResNet18 backbone encoder compressing 128×128 tiles to 8×8×256 spatial latent codes for denoising.',
    verification: '50 epochs trained; weights committed in outputs/ae/model.pth; final loss: 0.01977 MSE.',
  },
  {
    step: '07',
    title: 'Spatial Variational Autoencoder (VAE)',
    status: 'implemented',
    statusLabel: 'Verified ✓',
    description: 'Probabilistic spatial latent space (64×8×8 = 4,096 dims) with reparameterization trick and beta-VAE trade-off.',
    verification: '50 epochs trained; outputs/vae/model.pth; final recon loss: 0.07524, KL: 103.25 nats.',
  },
  {
    step: '08',
    title: 'Scenario Evaluation & Anomaly Scoring',
    status: 'in_development',
    statusLabel: 'In Development ◐',
    description: 'Empirical reconstruction-error z-scoring against 300 real tiles + ResNet18 21-class zoning verification.',
    verification: 'Z-score anomaly calculation active in backend/api.py; multi-criteria sustainability metrics planned.',
  },
  {
    step: '09',
    title: 'LLM Planning & Explanation Layer',
    status: 'implemented',
    statusLabel: 'Verified ✓',
    description: 'From-scratch 4-layer Transformer (MiniGPT) trained on sustainable urban planning corpus & seeded from Pune stats.',
    verification: '3,000 steps trained; outputs/gpt/model.pth; interactive generation served via /generate/plan.',
  },
  {
    step: '10',
    title: 'Diffusion Model Visualization',
    status: 'planned',
    statusLabel: 'Planned Roadmap ○',
    description: 'Latent Diffusion Model (LDM) generating photorealistic satellite renderings of future zoning scenarios.',
    verification: 'Phase 14 development roadmap.',
  },
  {
    step: '11',
    title: 'Integrated Urban Digital Twin Cockpit',
    status: 'planned',
    statusLabel: 'Planned Roadmap ○',
    description: 'Real-time multi-agent digital twin uniting live sensor streams, generative alternatives, and municipal policy checks.',
    verification: 'Phase 15 development roadmap.',
  },
];

export default function ResearchProgress() {
  const [aeHistory, setAeHistory] = useState<any[]>([]);
  const [vaeHistory, setVaeHistory] = useState<any[]>([]);

  useEffect(() => {
    Promise.all([
      apiFetch('/history/ae').then(r => r.json()).catch(() => []),
      apiFetch('/history/vae').then(r => r.json()).catch(() => []),
    ]).then(([ae, vae]) => {
      setAeHistory(Array.isArray(ae) ? ae : []);
      setVaeHistory(Array.isArray(vae) ? vae : []);
    });
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Verified Repository Metrics */}
      <div className="card">
        <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={20} color="var(--accent)" />
          Verified Project Metrics &amp; Empirical Baselines
        </div>
        <p style={{ color: 'var(--muted)', fontSize: '0.88rem', marginBottom: '18px' }}>
          All values below are verified directly from committed checkpoints (<code style={{ color: 'var(--accent)' }}>outputs/*/model.pth</code>), training logs (<code style={{ color: 'var(--accent)' }}>outputs/*/history.json</code>), and documentation (<code style={{ color: 'var(--accent)' }}>docs/MODEL_CARD.md</code>). No synthetic or placeholder figures are displayed.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px' }}>
          {[
            { label: 'Target Urban AOI', value: 'Pune (PMC Bounds)', sub: '516 km² | 7.4M Residents' },
            { label: 'Spatial Resolution', value: '128 × 128 px', sub: 'Aerial Tiles (UCMerced)' },
            { label: 'Land-Use Classes', value: '21 Classes', sub: 'Residential, Commercial, River, etc.' },
            { label: 'AE Training Run', value: '50 Epochs', sub: 'Final MSE: 0.01977 (Clean)' },
            { label: 'AE Feature Bottleneck', value: '8 × 8 × 256', sub: '16,384 Spatial Codes' },
            { label: 'VAE Training Run', value: '50 Epochs', sub: 'Recon: 0.07524 | KL: 103.25' },
            { label: 'VAE Latent Space', value: '64 × 8 × 8', sub: '4,096 Spatial Dimensions' },
            { label: 'Zoning Classifier Val Acc', value: '98.1%', sub: 'Val Loss: 0.1032 (ResNet18)' },
            { label: 'MiniGPT Transformer', value: '4 Layers / 4 Heads', sub: '3,000 Steps | 192 Block Size' },
            { label: 'Training Hardware', value: 'NVIDIA RTX 4050', sub: 'Laptop GPU (~75 W)' },
            { label: 'Total Retrain Budget', value: '~1.0 Hour', sub: 'All Models (~0.12 kWh)' },
            { label: 'Estimated Carbon Footprint', value: '~0.08 kg CO₂e', sub: 'At ~0.7 kg/kWh Grid Intensity' },
          ].map((m, i) => (
            <div
              key={i}
              style={{
                background: 'rgba(8, 12, 20, 0.65)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                padding: '14px',
                display: 'flex',
                flexDirection: 'column',
                gap: '3px',
              }}
            >
              <div style={{ fontSize: '0.74rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {m.label}
              </div>
              <div style={{ fontSize: '1.15rem', fontWeight: 600, color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}>
                {m.value}
              </div>
              <div style={{ fontSize: '0.74rem', color: 'var(--text)', opacity: 0.8 }}>
                {m.sub}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Verified Loss Curves from Live Outputs */}
      <div className="card">
        <div className="card-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Empirical Training Convergence (Read from outputs/*/history.json)</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--muted)' }}>50 Committed Epochs</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', marginTop: '16px' }}>
          {/* AE Loss Chart */}
          <div style={{ background: 'rgba(8, 12, 20, 0.5)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent)', marginBottom: '8px' }}>
              Autoencoder Denoising Loss (MSE vs. Epoch)
            </div>
            <div style={{ height: '240px', width: '100%' }}>
              {aeHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={aeHistory}>
                    <XAxis dataKey="epoch" stroke="var(--muted)" fontSize={11} />
                    <YAxis stroke="var(--muted)" fontSize={11} domain={[0, 0.2]} />
                    <Tooltip contentStyle={{ background: '#0F1923', border: '1px solid #1E2D40', fontSize: '11px' }} />
                    <Line type="monotone" dataKey="loss" stroke="#00D4FF" dot={false} strokeWidth={2} name="Train MSE" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontSize: '0.85rem' }}>
                  Loading AE history...
                </div>
              )}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--muted)', textAlign: 'center', marginTop: '6px' }}>
              Loss falls rapidly from 0.1830 (Epoch 1) to 0.01977 (Epoch 50). Unfreezing encoder at Epoch 5.
            </div>
          </div>

          {/* VAE Loss Chart */}
          <div style={{ background: 'rgba(8, 12, 20, 0.5)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent2)', marginBottom: '8px' }}>
              Spatial VAE Reconstruction &amp; KL Convergence
            </div>
            <div style={{ height: '240px', width: '100%' }}>
              {vaeHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={vaeHistory}>
                    <XAxis dataKey="epoch" stroke="var(--muted)" fontSize={11} />
                    <YAxis stroke="var(--muted)" fontSize={11} domain={[0, 0.25]} />
                    <Tooltip contentStyle={{ background: '#0F1923', border: '1px solid #1E2D40', fontSize: '11px' }} />
                    <Line type="monotone" dataKey="recon" stroke="#7B61FF" dot={false} strokeWidth={2} name="Recon Loss" />
                    <Line type="monotone" dataKey="loss" stroke="#00E676" dot={false} strokeWidth={1.5} strokeDasharray="3 3" name="Total Loss" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)', fontSize: '0.85rem' }}>
                  Loading VAE history...
                </div>
              )}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--muted)', textAlign: 'center', marginTop: '6px' }}>
              Recon loss drops to 0.07524; KL rises to 103.25 nats (informational latent under β = 1e-4).
            </div>
          </div>
        </div>
      </div>

      {/* 11-Stage Development Progress Timeline */}
      <div className="card">
        <div className="card-title" style={{ marginBottom: '18px' }}>
          Project Progress Timeline: 11 Development Stages
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {TIMELINE.map((t) => (
            <div
              key={t.step}
              style={{
                display: 'flex',
                gap: '18px',
                background: 'rgba(8, 12, 20, 0.5)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                padding: '16px 20px',
                alignItems: 'flex-start',
              }}
            >
              <div
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  color: t.status === 'implemented' ? 'var(--success)' : t.status === 'in_development' ? '#FFB300' : 'var(--muted)',
                  minWidth: '32px',
                  paddingTop: '2px',
                }}
              >
                {t.step}
              </div>

              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', marginBottom: '4px' }}>
                  <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text)' }}>
                    {t.title}
                  </div>
                  <div>
                    {t.status === 'implemented' && (
                      <span style={{ background: 'rgba(0, 230, 118, 0.15)', color: 'var(--success)', border: '1px solid rgba(0, 230, 118, 0.3)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600 }}>
                        {t.statusLabel}
                      </span>
                    )}
                    {t.status === 'in_development' && (
                      <span style={{ background: 'rgba(255, 179, 0, 0.15)', color: '#FFB300', border: '1px solid rgba(255, 179, 0, 0.3)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600 }}>
                        {t.statusLabel}
                      </span>
                    )}
                    {t.status === 'planned' && (
                      <span style={{ background: 'rgba(74, 96, 128, 0.15)', color: 'var(--muted)', border: '1px solid var(--border)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600 }}>
                        {t.statusLabel}
                      </span>
                    )}
                  </div>
                </div>

                <p style={{ color: 'var(--text)', fontSize: '0.85rem', lineHeight: 1.5, marginBottom: '6px' }}>
                  {t.description}
                </p>
                <div style={{ color: 'var(--muted)', fontSize: '0.78rem' }}>
                  <strong>Verification:</strong> {t.verification}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
