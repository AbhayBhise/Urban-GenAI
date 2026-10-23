import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiFetch } from '../lib/api';

export interface CurveConfig {
  key: string;
  label: string;
  color: string;
  yAxisId?: 'l' | 'r';
}

interface TrainingCurveProps {
  modelKey: 'ae' | 'vae' | 'gan' | 'gpt' | 'transformer' | 'diffusion';
  title?: string;
  description?: string;
  xKey?: string;
  curves: CurveConfig[];
}

export function TrainingCurveCard({
  modelKey,
  title = 'Empirical Training Dynamics',
  description,
  xKey = 'epoch',
  curves,
}: TrainingCurveProps) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    apiFetch(`/history/${modelKey}`)
      .then(res => res.json())
      .then(json => {
        if (Array.isArray(json)) {
          setData(json);
        }
      })
      .catch(err => {
        console.error(`Failed to fetch history for ${modelKey}:`, err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [modelKey]);

  const last = data.length > 0 ? data[data.length - 1] : null;

  return (
    <div className="card" style={{ marginBottom: 20 }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span>📈</span>
          <span>{title}</span>
        </div>
        {last && (
          <span style={{ color: 'var(--muted)', fontWeight: 400, fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
            final:&nbsp;
            {curves
              .map(c => {
                const val = last[c.key];
                if (val == null || isNaN(val)) return null;
                const formatted = c.key.includes('accuracy') || c.key.includes('rate')
                  ? `${(Number(val) * (Number(val) <= 1 ? 100 : 1)).toFixed(1)}%`
                  : Number(val).toFixed(4);
                return `${c.label}=${formatted}`;
              })
              .filter(Boolean)
              .join('  ·  ')}
          </span>
        )}
      </div>

      {description && (
        <div style={{ padding: '0 16px 12px', color: 'var(--muted)', fontSize: '0.84rem', lineHeight: 1.55 }}>
          {description}
        </div>
      )}

      {loading ? (
        <div style={{ padding: '40px 0', textAlign: 'center', color: 'var(--muted)', fontSize: '0.88rem' }}>
          Loading training loss curves…
        </div>
      ) : data.length === 0 ? (
        <div style={{ padding: '40px 0', textAlign: 'center', color: 'var(--muted)', fontSize: '0.88rem' }}>
          No training history recorded yet for this model.
        </div>
      ) : (
        <div style={{ height: 280, width: '100%', padding: '0 8px 10px 0' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
              <XAxis
                dataKey={xKey}
                stroke="var(--muted)"
                fontSize={11}
                tickLine={false}
                label={{ value: xKey === 'step' ? 'Optimization Step' : 'Epoch', position: 'insideBottom', offset: -2, fill: 'var(--muted)', fontSize: 11 }}
              />
              <YAxis
                yAxisId="l"
                stroke="var(--muted)"
                fontSize={11}
                tickLine={false}
                domain={['auto', 'auto']}
              />
              {curves.some(c => c.yAxisId === 'r') && (
                <YAxis
                  yAxisId="r"
                  orientation="right"
                  stroke="var(--accent2)"
                  fontSize={11}
                  tickLine={false}
                  domain={['auto', 'auto']}
                />
              )}
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--surface)',
                  border: '1px solid var(--border)',
                  borderRadius: 6,
                  fontSize: '0.82rem',
                }}
                itemStyle={{ fontFamily: 'var(--font-mono)' }}
              />
              <Legend wrapperStyle={{ fontSize: '0.8rem', paddingTop: 8 }} />
              {curves.map(c => (
                <Line
                  key={c.key}
                  yAxisId={c.yAxisId === 'r' ? 'r' : 'l'}
                  type="monotone"
                  dataKey={c.key}
                  name={c.yAxisId === 'r' ? `${c.label} (right axis)` : c.label}
                  stroke={c.color}
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
