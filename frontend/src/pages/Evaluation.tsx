import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { apiFetch } from '../lib/api';

type ClassMetric = { mse: number; psnr: number; ssim: number; n: number };
type EvalMetrics = {
  n_samples: number;
  n_classes: number;
  mse: { mean: number; std: number };
  psnr: { mean: number; std: number };
  ssim: { mean: number; std: number };
  kl: { mean: number; std: number };
  kl_per_dim: { mean: number; std: number };
  latent: { total_dims: number; active_dims: number; active_fraction: number };
  per_class: Record<string, ClassMetric>;
};

const METRIC_OPTIONS = [
  { key: 'ssim', label: 'SSIM', suffix: '', higherIsBetter: true },
  { key: 'psnr', label: 'PSNR', suffix: ' dB', higherIsBetter: true },
  { key: 'mse', label: 'MSE', suffix: '', higherIsBetter: false },
] as const;

export default function Evaluation() {
  const [metrics, setMetrics] = useState<EvalMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [metricKey, setMetricKey] = useState<typeof METRIC_OPTIONS[number]['key']>('ssim');

  useEffect(() => {
    apiFetch('/evaluate/vae')
      .then(async res => {
        if (!res.ok) {
          setError(res.status === 400 ? await res.text() : `Error ${res.status}`);
          return;
        }
        setMetrics(await res.json());
      })
      .catch(err => setError(String(err)));
  }, []);

  const activeOption = METRIC_OPTIONS.find(o => o.key === metricKey)!;
  const chartData = metrics
    ? Object.entries(metrics.per_class)
        .map(([cls, m]) => ({ cls, value: m[metricKey] }))
        .sort((a, b) => (activeOption.higherIsBetter ? b.value - a.value : a.value - b.value))
    : [];

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Model Evaluation</h1>
        <div className="panel-desc">
          Reconstruction-quality and latent-health metrics for the VAE, computed once at startup
          over a held-out sample spanning all 21 UCMerced classes — the model's actual measured
          performance, not a guess.
        </div>
      </div>

      {error && (
        <div className="card" style={{ borderColor: '#FF5252', color: '#FF5252', marginBottom: 24 }}>
          {error}
        </div>
      )}

      {!metrics && !error && (
        <div className="card" style={{ color: 'var(--muted)', textAlign: 'center' }}>
          Loading evaluation metrics…
        </div>
      )}

      {metrics && (
        <>
          <div className="metrics-strip">
            <div className="metric">
              <span className="metric-label">SSIM</span>
              <span className="metric-value">{metrics.ssim.mean.toFixed(3)} ± {metrics.ssim.std.toFixed(3)}</span>
            </div>
            <div className="metric">
              <span className="metric-label">PSNR</span>
              <span className="metric-value">{metrics.psnr.mean.toFixed(2)} dB</span>
            </div>
            <div className="metric">
              <span className="metric-label">MSE</span>
              <span className="metric-value">{metrics.mse.mean.toFixed(4)}</span>
            </div>
            <div className="metric">
              <span className="metric-label">KL Divergence</span>
              <span className="metric-value" style={{ color: 'var(--accent2)' }}>{metrics.kl.mean.toFixed(1)} nats</span>
            </div>
            <div className="metric">
              <span className="metric-label">Active Latent Dims</span>
              <span className="metric-value" style={{ color: metrics.latent.active_fraction > 0.5 ? 'var(--success)' : '#FFB84D' }}>
                {metrics.latent.active_dims} / {metrics.latent.total_dims}
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Sample Size</span>
              <span className="metric-value">{metrics.n_samples} tiles, {metrics.n_classes} classes</span>
            </div>
          </div>

          <div className="card" style={{ marginBottom: 24 }}>
            <div className="card-title">What these numbers mean</div>
            <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              <p style={{ margin: '0 0 10px' }}>
                <strong style={{ color: 'var(--text)' }}>SSIM</strong> (structural similarity, 0–1) and{' '}
                <strong style={{ color: 'var(--text)' }}>PSNR</strong> (dB, higher is better) both measure how close
                the reconstruction is to the original pixel-for-pixel. An SSIM around{' '}
                {metrics.ssim.mean.toFixed(2)} and PSNR around {metrics.psnr.mean.toFixed(0)} dB confirm what the
                reconstructions visibly show: this checkpoint is genuinely soft, not just apparently so. That's a
                direct consequence of the 8×8 spatial bottleneck (4096 total latent dims compressing a 128×128
                image) — see the architecture note in <code>models/vae.py</code> — not a display bug.
              </p>
              <p style={{ margin: '0 0 10px' }}>
                <strong style={{ color: 'var(--text)' }}>Active latent dims</strong> ({metrics.latent.active_dims} of{' '}
                {metrics.latent.total_dims}) counts how many of the 64 latent channels carry a meaningful KL
                divergence from the prior (i.e. are actually encoding something, rather than having collapsed to
                just copying the prior). Most of the latent is active here — the softness is a capacity/resolution
                limit of the bottleneck, not a wasted or collapsed latent space.
              </p>
              <p style={{ margin: 0 }}>
                The chart below breaks SSIM/PSNR/MSE down by land-use class — useful for spotting which categories
                this checkpoint reconstructs well versus poorly, e.g. classes with fine repeated structure
                (buildings, parking lots) typically score lower than classes with broad, low-frequency texture
                (agricultural, beach).
              </p>
            </div>
          </div>

          <div className="card">
            <div className="card-title">
              Per-class reconstruction quality
              <div style={{ display: 'flex', gap: 6 }}>
                {METRIC_OPTIONS.map(opt => (
                  <button
                    key={opt.key}
                    onClick={() => setMetricKey(opt.key)}
                    className="btn"
                    style={{
                      width: 'auto', marginTop: 0, padding: '4px 10px', fontSize: '0.75rem',
                      background: metricKey === opt.key ? 'var(--accent)' : 'transparent',
                      color: metricKey === opt.key ? '#000' : 'var(--text)',
                      border: '1px solid var(--border)',
                    }}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
            <div style={{ height: 520, width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                  <XAxis type="number" stroke="var(--muted)" fontSize={12} />
                  <YAxis type="category" dataKey="cls" stroke="var(--muted)" fontSize={11} width={110} />
                  <Tooltip
                    formatter={(v: number) => [`${v.toFixed(activeOption.key === 'mse' ? 4 : 2)}${activeOption.suffix}`, activeOption.label]}
                    contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}
                    itemStyle={{ fontFamily: 'var(--font-mono)' }}
                    cursor={{ fill: 'rgba(255,255,255,0.04)' }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {chartData.map((_, i) => (
                      <Cell key={i} fill="var(--accent)" />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
