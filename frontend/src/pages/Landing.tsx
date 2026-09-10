import { useEffect, useRef, useState } from 'react';
import { Layers, FileText, Image as ImageIcon, Sparkles, ArrowRight, CheckCircle2, Cpu } from 'lucide-react';
import { apiFetch } from '../lib/api';

// Animated background: a slowly drifting aerial-survey grid with an
// occasional scan sweep -- evokes satellite/aerial tiling (this project's
// actual subject matter) rather than a generic particle field. Respects
// prefers-reduced-motion.
function SurveyGridCanvas() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let raf = 0;
    let t = 0;
    const cell = 46;

    const resize = () => {
      canvas.width = canvas.clientWidth * devicePixelRatio;
      canvas.height = canvas.clientHeight * devicePixelRatio;
      ctx.scale(devicePixelRatio, devicePixelRatio);
    };
    resize();
    window.addEventListener('resize', resize);

    const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#00D4FF';

    const draw = () => {
      const w = canvas.clientWidth, h = canvas.clientHeight;
      ctx.clearRect(0, 0, w, h);

      const offset = reduceMotion ? 0 : (t * 6) % cell;
      ctx.strokeStyle = accent;
      ctx.globalAlpha = 0.08;
      ctx.lineWidth = 1;
      for (let x = -cell + offset; x < w + cell; x += cell) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
      }
      for (let y = -cell + offset; y < h + cell; y += cell) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }

      // A soft "scan" band sweeping left-to-right, like an aerial pass.
      if (!reduceMotion) {
        const sweepX = ((t * 90) % (w + 400)) - 200;
        const grad = ctx.createLinearGradient(sweepX - 140, 0, sweepX + 140, 0);
        grad.addColorStop(0, 'rgba(0,0,0,0)');
        grad.addColorStop(0.5, accent + '22');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.globalAlpha = 1;
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);
      }

      t += 0.016;
      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', resize); };
  }, []);

  return <canvas ref={ref} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />;
}

const PIPELINE = [
  {
    id: 'classifier', icon: Cpu, title: 'Classify', subtitle: 'ResNet18 · 98.1% accuracy',
    desc: 'Labels a land parcel into one of 21 UCMerced zoning categories.',
  },
  {
    id: 'vae', icon: FileText, title: 'Anomaly Check', subtitle: 'VAE · reconstruction scoring',
    desc: 'Flags parcels whose pattern doesn’t match what real land use looks like.',
  },
  {
    id: 'gan', icon: ImageIcon, title: 'Augment', subtitle: 'Conditional DCGAN · 100 epochs',
    desc: 'Generates class-conditional synthetic tiles for data augmentation.',
  },
  {
    id: 'plan-generator', icon: Sparkles, title: 'Recommend', subtitle: 'MiniGPT · built from scratch',
    desc: 'Drafts a planning recommendation grounded in real Pune statistics.',
  },
];

const STATS = [
  { value: '98.1%', label: 'Classifier accuracy' },
  { value: '29.7 dB', label: 'AE reconstruction PSNR' },
  { value: '4', label: 'Models, one pipeline' },
  { value: '2,100', label: 'UCMerced tiles trained on' },
];

export default function Landing({ onEnter }: { onEnter: (view: string) => void }) {
  const [allTrained, setAllTrained] = useState<boolean | null>(null);

  useEffect(() => {
    apiFetch('/status')
      .then(r => r.json())
      .then(d => setAllTrained(Object.values(d).every(v => v === 'Trained')))
      .catch(() => setAllTrained(null));
  }, []);

  return (
    <div>
      <div style={{
        position: 'relative', overflow: 'hidden', borderRadius: 10,
        border: '1px solid var(--border)', marginBottom: 32,
        padding: '64px 40px', minHeight: 380,
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        background: 'var(--surface)',
      }}>
        <SurveyGridCanvas />
        <div style={{ position: 'relative', zIndex: 1, maxWidth: 720 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: '0.78rem',
            fontFamily: 'var(--font-mono)', color: 'var(--accent)', textTransform: 'uppercase',
            letterSpacing: '0.08em', border: '1px solid var(--accent)', borderRadius: 20,
            padding: '5px 14px', marginBottom: 22, background: 'var(--active-tint)',
          }}>
            <Layers size={13} /> Generative AI &middot; Urban Planning Capstone
          </div>
          <h1 style={{
            fontSize: '3rem', fontWeight: 700, lineHeight: 1.1, margin: '0 0 18px',
            color: 'var(--text)', textWrap: 'balance' as any,
          }}>
            Four generative models,<br />one urban-planning pipeline.
          </h1>
          <p style={{ fontSize: '1.05rem', color: 'var(--muted)', lineHeight: 1.6, margin: '0 0 30px', maxWidth: 560 }}>
            UrbanGenAI classifies land use, flags anomalies against learned normal patterns,
            generates synthetic tiles for augmentation, and drafts planning recommendations —
            each model doing a distinct, justified job, trained and verified end-to-end on real data.
          </p>
          <div style={{ display: 'flex', gap: 14, alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              className="btn"
              style={{ width: 'auto', margin: 0, padding: '12px 24px', display: 'flex', alignItems: 'center', gap: 8 }}
              onClick={() => onEnter('model-explorer')}
            >
              Enter Dashboard <ArrowRight size={16} />
            </button>
            {allTrained != null && (
              <div style={{
                display: 'flex', alignItems: 'center', gap: 7, fontSize: '0.85rem',
                color: allTrained ? 'var(--success)' : 'var(--warn)', fontFamily: 'var(--font-mono)',
              }}>
                <CheckCircle2 size={15} />
                {allTrained ? 'All 5 models trained and live' : 'Some models not yet trained — see Model Explorer'}
              </div>
            )}
          </div>
        </div>
      </div>

      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32,
      }}>
        {STATS.map(s => (
          <div key={s.label} className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.6rem', fontWeight: 700, color: 'var(--accent)', marginBottom: 4 }}>
              {s.value}
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              {s.label}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 600, marginBottom: 6, color: 'var(--text)' }}>The pipeline, in order</h2>
        <p style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>Click any stage to jump straight to its page.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        {PIPELINE.map((step, i) => (
          <div
            key={step.id}
            className="card"
            style={{ cursor: 'pointer', position: 'relative', transition: 'transform 0.15s, border-color 0.15s' }}
            onClick={() => onEnter(step.id)}
            onMouseEnter={e => (e.currentTarget.style.borderColor = 'var(--accent)')}
            onMouseLeave={e => (e.currentTarget.style.borderColor = 'var(--border)')}
          >
            <div style={{
              position: 'absolute', top: 14, right: 16, fontFamily: 'var(--font-mono)',
              fontSize: '0.7rem', color: 'var(--muted)',
            }}>
              {String(i + 1).padStart(2, '0')}
            </div>
            <step.icon size={22} color="var(--accent2)" style={{ marginBottom: 12 }} />
            <div style={{ fontWeight: 600, fontSize: '1.02rem', marginBottom: 4, color: 'var(--text)' }}>{step.title}</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--accent)', marginBottom: 10 }}>{step.subtitle}</div>
            <div style={{ fontSize: '0.83rem', color: 'var(--muted)', lineHeight: 1.5 }}>{step.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
