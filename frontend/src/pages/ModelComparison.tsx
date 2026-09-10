import { useEffect, useState } from 'react';
import { apiFetch } from '../lib/api';

// Live numbers (with safe fallbacks) so the comparison always reflects the
// current committed checkpoints.
type Live = {
  ae?: { psnr: number; ssim: number };
  vae?: { psnr: number; ssim: number; kl: number; active: number; total: number };
  gan?: { rate: number };
  gpt?: { perplexity: number; bpc: number };
};

function useLiveMetrics(): Live {
  const [m, setM] = useState<Live>({});
  useEffect(() => {
    const grab = async (path: string) => {
      try {
        const r = await apiFetch(path);
        return r.ok ? await r.json() : null;
      } catch {
        return null;
      }
    };
    Promise.all([grab('/evaluate/ae'), grab('/evaluate/vae'), grab('/evaluate/gan'), grab('/evaluate/gpt')])
      .then(([ae, vae, gan, gpt]) => {
        const next: Live = {};
        if (ae) next.ae = { psnr: ae.psnr.mean, ssim: ae.ssim.mean };
        if (vae) next.vae = {
          psnr: vae.psnr.mean, ssim: vae.ssim.mean,
          kl: vae.kl?.mean ?? 0,
          active: vae.latent?.active_dims ?? 0, total: vae.latent?.total_dims ?? 64,
        };
        if (gan) next.gan = { rate: gan.overall_recognition_rate };
        if (gpt) next.gpt = { perplexity: gpt.perplexity, bpc: gpt.bits_per_char };
        setM(next);
      });
  }, []);
  return m;
}

const fmt = (v: number | undefined, dp: number, unit = '') =>
  v == null ? '—' : `${v.toFixed(dp)}${unit}`;

export default function ModelComparison() {
  const live = useLiveMetrics();

  const rows: { model: string; task: string; syllabus: string; metric: string; error: string; verdict: string }[] = [
    {
      model: 'Denoising Autoencoder',
      task: 'Clean degraded aerial imagery before analysis',
      syllabus: 'Autoencoder + reconstruction loss',
      metric: `PSNR ${fmt(live.ae?.psnr, 1, ' dB')} · SSIM ${fmt(live.ae?.ssim, 3)}`,
      error: 'Small residual blur on very fine texture',
      verdict: 'Best for image restoration. U-Net skip connections beat a plain bottleneck (25 → 29.7 dB).',
    },
    {
      model: 'Variational Autoencoder',
      task: 'Score how far a parcel is from "normal" + latent scenario blending',
      syllabus: 'VAE, KL divergence, reparameterization trick',
      metric: `SSIM ${fmt(live.vae?.ssim, 2)} · KL ${fmt(live.vae?.kl, 0, ' nats')} · ${live.vae?.active ?? '—'}/${live.vae?.total ?? 64} dims active`,
      error: 'Reconstruction is soft — the 8×8 spatial bottleneck limits detail',
      verdict: 'Best for anomaly detection. Gives a probabilistic score + interpolation the AE cannot.',
    },
    {
      model: 'Conditional DCGAN',
      task: 'Generate synthetic class-conditional tiles for data augmentation',
      syllabus: 'GAN, adversarial (min–max) loss',
      metric: `Recognition rate ${live.gan ? (live.gan.rate * 100).toFixed(0) + ' %' : '—'}`,
      error: 'Grid-geometry classes near 0 % at 100 epochs',
      verdict: 'Best for augmenting texture-rich classes. Not yet reliable for geometric classes — needs more epochs / data.',
    },
    {
      model: 'MiniGPT Transformer',
      task: 'Draft a planning recommendation grounded in real Pune statistics',
      syllabus: 'Transformer, self-attention, cross-entropy LM loss',
      metric: `Perplexity ${fmt(live.gpt?.perplexity, 2)} · ${fmt(live.gpt?.bpc, 2, ' bpc')}`,
      error: 'Narrow — trained on a small templated corpus, not a general planner',
      verdict: 'Best for structured, grounded drafting from statistics. Delivers the final planner-facing output.',
    },
    {
      model: 'Land-Use Classifier (ResNet18)',
      task: 'Label a parcel into one of 21 zoning classes',
      syllabus: 'Supporting CNN — not one of the 4 required generative models',
      metric: '98.1 % validation accuracy',
      error: 'Some dense- vs medium-residential confusion',
      verdict: 'Most accurate model overall. It is discriminative (not generative) — it feeds the VAE and MiniGPT stages.',
    },
  ];

  const best = [
    { crit: 'Pixel fidelity / restoration', winner: 'Denoising AE', why: 'Highest PSNR & SSIM; skip connections keep fine detail.' },
    { crit: 'Anomaly detection (project’s primary generative use)', winner: 'Spatial VAE', why: 'Only model that outputs a calibrated “how unusual is this parcel” score.' },
    { crit: 'Creating new training samples', winner: 'Conditional GAN', why: 'Only model that generates novel tiles from noise + a class label.' },
    { crit: 'The planner-facing recommendation', winner: 'MiniGPT', why: 'Turns numbers into readable, grounded planning text — the pipeline’s output.' },
    { crit: 'Raw predictive accuracy', winner: 'Land-Use Classifier', why: '98.1 % — but discriminative, so it supports rather than replaces the generative models.' },
  ];

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Model Comparison</h1>
        <div className="panel-desc">
          Five models, each measured on the metric it is actually judged by. The question this page answers:
          <strong style={{ color: 'var(--text)' }}> which model matters most for UrbanGenAI’s goal — urban-planning decision support?</strong>
        </div>
      </div>

      {/* Bottom line */}
      <div className="card" style={{ marginBottom: 24, borderLeft: '4px solid var(--accent)' }}>
        <div className="card-title" style={{ justifyContent: 'flex-start', gap: 10 }}>Bottom line for this project</div>
        <div style={{ fontSize: '0.9rem', color: 'var(--text)', lineHeight: 1.65 }}>
          <p style={{ margin: '0 0 8px' }}>
            There is <strong>no single “best” model</strong> — the project’s objective is a <em>pipeline</em> where each
            model does one justified job. But ranked by contribution to the stated goal:
          </p>
          <p style={{ margin: '0 0 6px' }}>
            <strong style={{ color: 'var(--accent2)' }}>1. Spatial VAE</strong> — the core generative contribution:
            it produces the anomaly signal that makes the tool a <em>decision-support</em> system, not just a viewer.
          </p>
          <p style={{ margin: '0 0 6px' }}>
            <strong style={{ color: 'var(--accent2)' }}>2. MiniGPT</strong> — converts the analysis into the written
            recommendation a planner actually reads and acts on.
          </p>
          <p style={{ margin: 0 }}>
            <strong style={{ color: 'var(--accent2)' }}>3. Denoising AE</strong> &amp;
            <strong style={{ color: 'var(--accent2)' }}> Conditional GAN</strong> — enabling steps: cleaner inputs and
            more training data make every downstream stage more reliable. The <strong>Classifier</strong> is the most
            accurate model but is a supporting CNN, not a generative one.
          </p>
        </div>
      </div>

      {/* Main matrix */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Comparison matrix</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', minWidth: 900, borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ background: 'var(--surface-inset)', textAlign: 'left', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.05em', fontSize: '0.7rem' }}>
                <th style={{ padding: '10px 12px' }}>Model</th>
                <th style={{ padding: '10px 12px' }}>Job in the pipeline</th>
                <th style={{ padding: '10px 12px' }}>Syllabus concept</th>
                <th style={{ padding: '10px 12px' }}>Live result</th>
                <th style={{ padding: '10px 12px' }}>Main limitation</th>
                <th style={{ padding: '10px 12px' }}>Verdict — best for…</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, i) => (
                <tr key={r.model} style={{ borderTop: '1px solid var(--border)', background: i % 2 ? 'var(--hover-overlay)' : 'transparent', verticalAlign: 'top' }}>
                  <td style={{ padding: '12px', fontWeight: 600, color: 'var(--text)' }}>{r.model}</td>
                  <td style={{ padding: '12px', color: 'var(--muted)' }}>{r.task}</td>
                  <td style={{ padding: '12px', color: 'var(--muted)' }}>{r.syllabus}</td>
                  <td style={{ padding: '12px', color: 'var(--accent)', fontFamily: 'var(--font-mono)', fontSize: '0.76rem' }}>{r.metric}</td>
                  <td style={{ padding: '12px', color: 'var(--warn)' }}>{r.error}</td>
                  <td style={{ padding: '12px', color: 'var(--text)' }}>{r.verdict}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: 10, fontSize: '0.75rem', color: 'var(--muted)' }}>
          Live results are fetched from <code>/evaluate/&lt;model&gt;</code> at page load; “—” means the endpoint was unavailable.
        </div>
      </div>

      {/* Best by criterion */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Which model wins on each criterion</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 12 }}>
          {best.map(b => (
            <div key={b.crit} style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, padding: '12px 14px' }}>
              <div style={{ fontSize: '0.74rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 4 }}>{b.crit}</div>
              <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: 4 }}>{b.winner}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--muted)', lineHeight: 1.5 }}>{b.why}</div>
            </div>
          ))}
        </div>
      </div>

      {/* AE vs VAE head to head */}
      <div className="card">
        <div className="card-title" style={{ justifyContent: 'flex-start' }}>Head-to-head: Autoencoder vs. Variational Autoencoder</div>
        <div style={{ fontSize: '0.86rem', color: 'var(--text)', lineHeight: 1.6 }}>
          <p style={{ margin: '0 0 10px' }}>
            These two are the only fair like-for-like comparison — both reconstruct a 128×128 tile from a compressed code.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, padding: 14 }}>
              <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: 6 }}>AE wins on fidelity</div>
              <div style={{ fontSize: '0.82rem', color: 'var(--muted)', lineHeight: 1.55 }}>
                PSNR {fmt(live.ae?.psnr, 1, ' dB')} vs {fmt(live.vae?.psnr, 1, ' dB')}. It has U-Net skip connections and
                no KL constraint pulling the latent toward a prior, so it can copy fine detail straight through.
              </div>
            </div>
            <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, padding: 14 }}>
              <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: 6 }}>VAE wins on usefulness for planning</div>
              <div style={{ fontSize: '0.82rem', color: 'var(--muted)', lineHeight: 1.55 }}>
                Its probabilistic latent gives a reconstruction-error <em>z-score</em> against a 294-tile baseline — a real
                “is this parcel unusual?” signal — plus smooth interpolation between land-use states. The AE has neither.
              </div>
            </div>
          </div>
          <p style={{ margin: '10px 0 0', color: 'var(--muted)', fontSize: '0.8rem' }}>
            Conclusion: we keep both. The AE cleans the image; the VAE reasons about it.
          </p>
        </div>
      </div>
    </div>
  );
}
