import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiFetch } from '../lib/api';

// [dataKey, colour, axis] — 'r' = right-hand axis (used for KL, which is
// ~1000x larger than the reconstruction term and would otherwise flatten it).
const MODELS = [
  { key: 'ae', label: 'Autoencoder (Denoising U-Net)', x: 'epoch', lines: [['loss', 'var(--accent)', 'l']] },
  { key: 'vae', label: 'VAE — reconstruction (left axis) vs KL divergence (right axis)', x: 'epoch', lines: [['recon', 'var(--accent)', 'l'], ['kl', 'var(--accent2)', 'r']] },
 { key: 'gan', label: 'Class-Conditional DCGAN — Discriminator and Generator Objectives', x: 'epoch', lines: [['d_loss', 'var(--danger)', 'l'], ['g_loss', 'var(--accent)', 'l']] },
  { key: 'diffusion', label: 'Class-Conditional DDPM — Noise Prediction Loss', x: 'epoch', lines: [['loss', 'var(--accent)', 'l']] },
  { key: 'gpt', label: 'Urban Plan Generator (MiniGPT)', x: 'step', lines: [['loss', 'var(--accent)', 'l'], ['val_loss', 'var(--accent2)', 'l']] },
  { key: 'transformer', label: 'Land-Use Classifier', x: 'epoch', lines: [['loss', 'var(--accent)', 'l'], ['val_loss', 'var(--accent2)', 'l'], ['val_accuracy', 'var(--success)', 'l']] },
];

export default function Training() {
  const [data, setData] = useState<Record<string, any[]>>({});

  useEffect(() => {
    MODELS.forEach(m => {
      apiFetch(`/history/${m.key}`)
        .then(r => r.json())
        .then(h => setData(d => ({ ...d, [m.key]: Array.isArray(h) ? h : [] })))
        .catch(() => {});
    });
  }, []);

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Model Training Dashboard</h1>
        <div className="panel-desc">
          Training curves for every model, read live from <code>outputs/*/history.json</code>.
          Empty panels mean that checkpoint has not been trained yet.
        </div>
      </div>

      {MODELS.map(m => {
        const rows = data[m.key] || [];
        const last = rows[rows.length - 1];
        return (
          <div className="card" key={m.key} style={{ marginBottom: 24 }}>
            <div className="card-title">
              {m.label}
              {last && (
                <span style={{ color: 'var(--muted)', fontWeight: 400, fontSize: '0.78rem', marginLeft: 8 }}>
                  ({m.x === 'epoch' ? `recorded through epoch ${last[m.x]}` : `recorded through step ${last[m.x]}`})
                </span>
              )}
              {last && (
                <span style={{ color: 'var(--muted)', fontWeight: 400, fontSize: '0.8rem' }}>
                  final: {m.lines.map(([k]) => {
                    const value = Number(last[k]);
                    if (!Number.isFinite(value)) return null;
                    const formatted = k.includes('accuracy')
                      ? `${(value * (value <= 1 ? 100 : 1)).toFixed(1)}%`
                      : value.toFixed(4);
                    return `${k}=${formatted}`;
                  }).filter(Boolean).join('  ·  ')}
                </span>
              )}
            </div>
            {rows.length === 0 ? (
              <div style={{ color: 'var(--muted)', textAlign: 'center', padding: '30px 0', fontSize: '0.9rem' }}>
                Not trained yet.
              </div>
            ) : (
              <div style={{ height: 260 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={rows}>
                    <XAxis dataKey={m.x} stroke="var(--muted)" fontSize={12} />
                    <YAxis yAxisId="l" stroke="var(--muted)" fontSize={12} domain={['auto', 'auto']} />
                    {m.lines.some(l => l[2] === 'r') && (
                      <YAxis yAxisId="r" orientation="right" stroke="var(--accent2)" fontSize={12} domain={['auto', 'auto']} />
                    )}
                    <Tooltip contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }} itemStyle={{ fontFamily: 'var(--font-mono)' }} />
                    <Legend />
                    {m.lines.map(([k, c, ax]) => (
                      <Line key={k} yAxisId={ax === 'r' ? 'r' : 'l'} type="monotone" dataKey={k} name={ax === 'r' ? `${k} (right)` : k} stroke={c} strokeWidth={2} dot={false} />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
