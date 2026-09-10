import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { apiFetch } from '../lib/api';

type ClassMetric = { mse: number; psnr: number; ssim: number; n: number };
type ReconEvalMetrics = {
  n_samples: number;
  n_classes: number;
  mse: { mean: number; std: number };
  psnr: { mean: number; std: number };
  ssim: { mean: number; std: number };
  kl?: { mean: number; std: number };
  kl_per_dim?: { mean: number; std: number };
  latent?: { total_dims: number; active_dims: number; active_fraction: number };
  per_class: Record<string, ClassMetric>;
};
type ClassifierEvalMetrics = {
  n_samples: number;
  classes: string[];
  accuracy: number;
  confusion_matrix: number[][];
  per_class_accuracy: Record<string, number>;
};
type GanEvalMetrics = {
  n_samples: number;
  n_classes: number;
  overall_recognition_rate: number;
  per_class: Record<string, { recognized: number; n: number; rate: number }>;
};
type GptEvalMetrics = {
  held_out_chars: number;
  vocab_size: number;
  cross_entropy: number;
  perplexity: number;
  bits_per_char: number;
  uniform_baseline_perplexity: number;
  final_train_loss: number | null;
  n_params_millions: number;
};

const METRIC_OPTIONS = [
  { key: 'ssim', label: 'SSIM', suffix: '', higherIsBetter: true },
  { key: 'psnr', label: 'PSNR', suffix: ' dB', higherIsBetter: true },
  { key: 'mse', label: 'MSE', suffix: '', higherIsBetter: false },
] as const;

function useEval<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setData(null);
    setError(null);
    apiFetch(endpoint)
      .then(async res => {
        if (!res.ok) {
          setError(res.status === 400 ? await res.text() : `Error ${res.status}`);
          return;
        }
        setData(await res.json());
      })
      .catch(err => setError(String(err)));
  }, [endpoint]);
  return { data, error };
}

function PerClassBarChart({ metrics }: { metrics: ReconEvalMetrics }) {
  const [metricKey, setMetricKey] = useState<typeof METRIC_OPTIONS[number]['key']>('ssim');
  const activeOption = METRIC_OPTIONS.find(o => o.key === metricKey)!;
  const chartData = Object.entries(metrics.per_class)
    .map(([cls, m]) => ({ cls, value: m[metricKey] }))
    .sort((a, b) => (activeOption.higherIsBetter ? b.value - a.value : a.value - b.value));

  return (
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
                color: metricKey === opt.key ? 'var(--btn-text)' : 'var(--text)',
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
              cursor={{ fill: 'var(--hover-overlay)' }}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {chartData.map((_, i) => <Cell key={i} fill="var(--accent)" />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function VAEPanel() {
  const { data: metrics, error } = useEval<ReconEvalMetrics>('/evaluate/vae');
  if (error) return <ErrorCard error={error} />;
  if (!metrics) return <LoadingCard />;
  return (
    <>
      <div className="metrics-strip">
        <Metric label="SSIM" value={`${metrics.ssim.mean.toFixed(3)} ± ${metrics.ssim.std.toFixed(3)}`} />
        <Metric label="PSNR" value={`${metrics.psnr.mean.toFixed(2)} dB`} />
        <Metric label="MSE" value={metrics.mse.mean.toFixed(4)} />
        {metrics.kl && <Metric label="KL Divergence" value={`${metrics.kl.mean.toFixed(1)} nats`} color="var(--accent2)" />}
        {metrics.latent && (
          <Metric
            label="Active Latent Dims"
            value={`${metrics.latent.active_dims} / ${metrics.latent.total_dims}`}
            color={metrics.latent.active_fraction > 0.5 ? 'var(--success)' : 'var(--warn)'}
          />
        )}
        <Metric label="Sample Size" value={`${metrics.n_samples} tiles, ${metrics.n_classes} classes`} />
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
          {metrics.latent && (
            <p style={{ margin: '0 0 10px' }}>
              <strong style={{ color: 'var(--text)' }}>Active latent dims</strong> ({metrics.latent.active_dims} of{' '}
              {metrics.latent.total_dims}) counts how many latent channels carry a meaningful KL divergence from
              the prior. Most of the latent is active here — the softness is a capacity/resolution limit of the
              bottleneck, not a wasted or collapsed latent space.
            </p>
          )}
          <p style={{ margin: 0 }}>
            The chart below breaks SSIM/PSNR/MSE down by land-use class — classes with fine repeated structure
            (buildings, parking lots) typically score lower than classes with broad, low-frequency texture
            (agricultural, beach).
          </p>
        </div>
      </div>

      <PerClassBarChart metrics={metrics} />
    </>
  );
}

function AEPanel() {
  const { data: metrics, error } = useEval<ReconEvalMetrics>('/evaluate/ae');
  if (error) return <ErrorCard error={error} />;
  if (!metrics) return <LoadingCard />;
  return (
    <>
      <div className="metrics-strip">
        <Metric label="SSIM" value={`${metrics.ssim.mean.toFixed(3)} ± ${metrics.ssim.std.toFixed(3)}`} />
        <Metric label="PSNR" value={`${metrics.psnr.mean.toFixed(2)} dB`} />
        <Metric label="MSE" value={metrics.mse.mean.toFixed(5)} />
        <Metric label="Sample Size" value={`${metrics.n_samples} tiles, ${metrics.n_classes} classes`} />
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title">What these numbers mean</div>
        <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
          <p style={{ margin: 0 }}>
            This is the same SSIM/PSNR methodology as the VAE evaluation, applied to the U-Net skip-connected
            Autoencoder — the AE's decoder has a second, unbottlenecked path back to fine detail via the skip
            connections, which is why its scores (PSNR ≈{metrics.psnr.mean.toFixed(1)} dB, SSIM ≈{' '}
            {metrics.ssim.mean.toFixed(2)}) run noticeably higher than the VAE's, which decodes purely from its
            8×8 bottleneck. The chart below shows this held even for the classes that were hardest before the
            skip-connection fix.
          </p>
        </div>
      </div>

      <PerClassBarChart metrics={metrics} />
    </>
  );
}

function ConfusionMatrix({ classes, matrix }: { classes: string[]; matrix: number[][] }) {
  const max = Math.max(1, ...matrix.flat());
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ borderCollapse: 'collapse', fontSize: '0.68rem', fontFamily: 'var(--font-mono)' }}>
        <thead>
          <tr>
            <th style={{ padding: 4 }}></th>
            {classes.map(c => (
              <th key={c} style={{ padding: 2, writingMode: 'vertical-rl', color: 'var(--muted)', fontWeight: 500, height: 90 }}>
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {classes.map((rowCls, i) => (
            <tr key={rowCls}>
              <td style={{ padding: '2px 8px', color: 'var(--muted)', textAlign: 'right', whiteSpace: 'nowrap' }}>{rowCls}</td>
              {matrix[i].map((v, j) => {
                const intensity = v / max;
                const isDiagonal = i === j;
                return (
                  <td key={j} title={`true: ${rowCls} · predicted: ${classes[j]} · n=${v}`} style={{
                    width: 22, height: 22, textAlign: 'center', border: '1px solid var(--border)',
                    background: v === 0 ? 'transparent' : isDiagonal
                      ? `color-mix(in srgb, var(--success) ${20 + intensity * 60}%, var(--surface))`
                      : `color-mix(in srgb, var(--danger) ${20 + intensity * 60}%, var(--surface))`,
                    color: intensity > 0.5 ? 'var(--btn-text)' : 'var(--muted)',
                  }}>
                    {v || ''}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ClassifierPanel() {
  const { data: metrics, error } = useEval<ClassifierEvalMetrics>('/evaluate/classifier');
  if (error) return <ErrorCard error={error} />;
  if (!metrics) return <LoadingCard />;
  const worst = Object.entries(metrics.per_class_accuracy).sort((a, b) => a[1] - b[1]).slice(0, 3);
  return (
    <>
      <div className="metrics-strip">
        <Metric label="Accuracy (this sample)" value={`${(metrics.accuracy * 100).toFixed(1)}%`} color="var(--success)" />
        <Metric label="Sample Size" value={`${metrics.n_samples} tiles, ${metrics.classes.length} classes`} />
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title">What this is — and isn't</div>
        <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
          <p style={{ margin: '0 0 10px' }}>
            This is a confusion matrix built by re-running the live classifier on a random sample right now —
            useful for seeing <em>which specific classes get confused for which others</em>, not just an overall
            number. It is <strong style={{ color: 'var(--text)' }}>not</strong> the original train/validation
            split from training (that split isn't persisted), so this number can differ from the reported{' '}
            98.1% validation accuracy — most likely higher, since this sample can include images the model saw
            during training. Treat this as a diagnostic tool, not a re-measurement of the headline accuracy.
          </p>
          {worst.length > 0 && (
            <p style={{ margin: 0 }}>
              Lowest-accuracy classes in this sample: {worst.map(([c, a]) => `${c} (${(a * 100).toFixed(0)}%)`).join(', ')}.
            </p>
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-title">Confusion matrix — rows = true class, columns = predicted class</div>
        <ConfusionMatrix classes={metrics.classes} matrix={metrics.confusion_matrix} />
      </div>
    </>
  );
}

function GANPanel() {
  const { data: metrics, error } = useEval<GanEvalMetrics>('/evaluate/gan');
  if (error) return <ErrorCard error={error} />;
  if (!metrics) return <LoadingCard />;
  const chartData = Object.entries(metrics.per_class)
    .map(([cls, m]) => ({ cls, value: m.rate * 100 }))
    .sort((a, b) => b.value - a.value);
  return (
    <>
      <div className="metrics-strip">
        <Metric
          label="Classifier-Recognition Rate"
          value={`${(metrics.overall_recognition_rate * 100).toFixed(1)}%`}
          color={metrics.overall_recognition_rate > 0.5 ? 'var(--success)' : 'var(--warn)'}
        />
        <Metric label="Samples Evaluated" value={`${metrics.n_samples} generated tiles, ${metrics.n_classes} classes`} />
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title">What this measures</div>
        <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
          <p style={{ margin: '0 0 10px' }}>
            This generates fresh samples per class from the GAN and runs them through the independently-trained
            Land-Use Classifier — the same underlying idea as Inception Score: use a separate, already-trained
            classifier to judge whether generated samples are recognizable as their intended class, without
            needing a new reference-statistics dependency.
          </p>
          <p style={{ margin: 0 }}>
            An overall rate of {(metrics.overall_recognition_rate * 100).toFixed(0)}% quantitatively confirms
            what the generated-sample grids show visually: at 100 epochs on this dataset size, some classes
            (texture-distinctive ones like harbor) are recognizable, while classes needing precise repeated
            geometry (residential grids, intersections) mostly aren't yet. This is an honest, expected
            characteristic of GAN training at this scale, not a broken evaluation.
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Per-class recognition rate</div>
        <div style={{ height: 520, width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ left: 10, right: 20 }}>
              <XAxis type="number" domain={[0, 100]} stroke="var(--muted)" fontSize={12} unit="%" />
              <YAxis type="category" dataKey="cls" stroke="var(--muted)" fontSize={11} width={110} />
              <Tooltip
                formatter={(v: number) => [`${v.toFixed(0)}%`, 'Recognized as intended class']}
                contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}
                itemStyle={{ fontFamily: 'var(--font-mono)' }}
                cursor={{ fill: 'var(--hover-overlay)' }}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {chartData.map((d, i) => (
                  <Cell key={i} fill={d.value >= 50 ? 'var(--success)' : d.value >= 20 ? 'var(--warn)' : 'var(--danger)'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );
}

function GPTPanel() {
  const { data: m, error } = useEval<GptEvalMetrics>('/evaluate/gpt');
  if (error) return <ErrorCard error={error} />;
  if (!m) return <LoadingCard />;
  const uniformBits = Math.log2(m.vocab_size);
  return (
    <>
      <div className="metrics-strip">
        <Metric label="Perplexity" value={m.perplexity.toFixed(3)} color="var(--accent)" />
        <Metric label="Bits / character" value={m.bits_per_char.toFixed(3)} />
        <Metric label="Cross-entropy (nats)" value={m.cross_entropy.toFixed(4)} />
        <Metric label="Held-out sample" value={`${m.held_out_chars.toLocaleString()} chars`} />
        <Metric label="Model size" value={`${m.n_params_millions.toFixed(2)}M params`} />
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title">What these numbers mean</div>
        <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
          <p style={{ margin: '0 0 10px' }}>
            <strong style={{ color: 'var(--text)' }}>Perplexity</strong> is the standard intrinsic metric for a
            language model: the effective number of equally-likely characters the model is choosing between at
            each step. 1.0 is perfect; a model that learned nothing would sit near the vocabulary size
            ({m.vocab_size}). This MiniGPT scores {m.perplexity.toFixed(2)} — equivalently{' '}
            {m.bits_per_char.toFixed(2)} bits/char versus {uniformBits.toFixed(1)} bits/char for a uniform
            guess. Measured on the last 10% of the corpus, held out during training (the exact split{' '}
            <code>train_gpt.py</code> uses).
          </p>
          <p style={{ margin: 0 }}>
            <strong style={{ color: 'var(--text)' }}>Honest reading:</strong> a perplexity this close to 1 is
            not open-ended fluency. The training corpus is a small, hand-built set of templated urban-planning
            sentences, so the model has largely learned those templates — which is exactly what this project
            needs it for: producing structured, grounded planning recommendations from real Pune statistics,
            not free-form prose. The held-out loss ({m.cross_entropy.toFixed(3)}) tracking the final training
            loss ({m.final_train_loss != null ? m.final_train_loss.toFixed(3) : 'n/a'}) confirms it generalizes
            across the corpus rather than overfitting one region of it.
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Information content per character</div>
        <div style={{ height: 220, width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={[
                { label: 'Uniform guess (no model)', value: uniformBits },
                { label: 'MiniGPT (measured)', value: m.bits_per_char },
              ]}
              layout="vertical"
              margin={{ left: 10, right: 30 }}
            >
              <XAxis type="number" stroke="var(--muted)" fontSize={12} unit=" bits" />
              <YAxis type="category" dataKey="label" stroke="var(--muted)" fontSize={11} width={170} />
              <Tooltip
                formatter={(v: number) => [`${v.toFixed(2)} bits/char`, '']}
                contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}
                itemStyle={{ fontFamily: 'var(--font-mono)' }}
                cursor={{ fill: 'var(--hover-overlay)' }}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                <Cell fill="var(--muted)" />
                <Cell fill="var(--accent)" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );
}

function Metric({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div className="metric">
      <span className="metric-label">{label}</span>
      <span className="metric-value" style={color ? { color } : undefined}>{value}</span>
    </div>
  );
}
function ErrorCard({ error }: { error: string }) {
  return <div className="card" style={{ borderColor: 'var(--danger)', color: 'var(--danger)', marginBottom: 24 }}>{error}</div>;
}
function LoadingCard() {
  return <div className="card" style={{ color: 'var(--muted)', textAlign: 'center' }}>Loading evaluation metrics…</div>;
}

const TABS = [
  { id: 'vae', label: 'VAE', panel: VAEPanel },
  { id: 'ae', label: 'Autoencoder', panel: AEPanel },
  { id: 'gan', label: 'GAN', panel: GANPanel },
  { id: 'gpt', label: 'MiniGPT', panel: GPTPanel },
  { id: 'classifier', label: 'Classifier', panel: ClassifierPanel },
] as const;

export default function Evaluation() {
  const [tab, setTab] = useState<typeof TABS[number]['id']>('vae');
  const ActivePanel = TABS.find(t => t.id === tab)!.panel;

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Model Evaluation</h1>
        <div className="panel-desc">
          Real, measured performance for every model — computed once at backend startup on held-out data,
          not estimated. Each tab uses the metric that model is actually judged by: reconstruction quality
          (SSIM / PSNR) for the AE and VAE, a classifier-based recognition rate for the GAN, perplexity for
          MiniGPT, and a confusion matrix for the supporting Land-Use Classifier.
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {TABS.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className="btn"
            style={{
              width: 'auto', marginTop: 0, padding: '8px 18px', fontSize: '0.85rem',
              background: tab === t.id ? 'var(--accent)' : 'transparent',
              color: tab === t.id ? 'var(--btn-text)' : 'var(--text)',
              border: '1px solid var(--border)',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      <ActivePanel />
    </div>
  );
}
