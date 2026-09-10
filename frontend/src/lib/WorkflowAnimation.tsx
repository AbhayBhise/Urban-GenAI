import { useEffect, useState } from 'react';

// A small, theme-aware "data flows from input to output" animation used at
// the top of every model's Architecture page. It is deliberately schematic
// (labelled stages + a travelling pulse), not a fake render of the model's
// actual output -- it shows the *pipeline order*, which is the thing a
// viewer needs before reading the full diagram below it.
//
// Respects prefers-reduced-motion: with motion reduced it renders the
// completed pipeline (all stages lit, no pulse, solid connector) as a
// static figure.

export type WFStage = { label: string; sub?: string };

function usePrefersReducedMotion() {
  const [reduce, setReduce] = useState(
    typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const on = () => setReduce(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  return reduce;
}

export function WorkflowAnimation({
  title = 'Data flow — input to output',
  stages,
  note,
}: {
  title?: string;
  stages: WFStage[];
  note?: string;
}) {
  const reduce = usePrefersReducedMotion();
  const n = stages.length;
  // step runs 0..n : 0..n-1 light each stage in turn, n is a brief "done"
  // hold, then it wraps back to 0.
  const [step, setStep] = useState(reduce ? n - 1 : 0);

  useEffect(() => {
    if (reduce) {
      setStep(n - 1);
      return;
    }
    setStep(0);
    let s = 0;
    const id = setInterval(() => {
      s = s > n ? 0 : s + 1;
      setStep(s);
    }, 1050);
    return () => clearInterval(id);
  }, [reduce, n]);

  const active = Math.min(step, n - 1);
  const done = step >= n;
  // column centres for a row of n equal columns
  const centre = (i: number) => ((i + 0.5) / n) * 100;
  const pulseLeft = centre(active);
  const fillWidth = ((active + (done ? 0.5 : 0)) / n) * 100;

  return (
    <div className="card wfa-card" style={{ marginBottom: 20 }}>
      <style
        dangerouslySetInnerHTML={{
          __html: `
        .wfa-card .wfa-title { font-size: 0.95rem; font-weight: 600; color: var(--accent2); margin-bottom: 18px; }
        .wfa-track { position: relative; overflow-x: auto; padding: 26px 0 6px; }
        .wfa-row { display: flex; gap: 10px; min-width: 520px; }
        .wfa-stage { flex: 1 1 0; text-align: center; border: 1px solid var(--border); border-radius: 8px;
          padding: 12px 8px; background: var(--surface); transition: border-color .35s, box-shadow .35s,
          transform .35s, opacity .35s; }
        .wfa-stage[data-state="pending"] { opacity: .5; }
        .wfa-stage[data-state="visited"] { border-color: color-mix(in srgb, var(--accent2) 55%, var(--border)); }
        .wfa-stage[data-state="active"] { border-color: var(--accent);
          box-shadow: 0 0 0 3px var(--active-tint); transform: translateY(-3px); }
        .wfa-label { font-size: 0.8rem; font-weight: 600; color: var(--muted); transition: color .35s; }
        .wfa-stage[data-state="active"] .wfa-label,
        .wfa-stage[data-state="visited"] .wfa-label { color: var(--text); }
        .wfa-sub { font-size: 0.68rem; font-family: var(--font-mono); color: var(--muted); margin-top: 3px; }
        .wfa-wire { position: absolute; left: 0; right: 0; top: 14px; height: 2px; background: var(--border); }
        .wfa-wire-fill { position: absolute; left: 0; top: 14px; height: 2px; background: var(--accent);
          transition: width .7s cubic-bezier(.4,0,.2,1); }
        .wfa-pulse { position: absolute; top: 15px; width: 11px; height: 11px; border-radius: 50%;
          background: var(--accent); box-shadow: 0 0 12px var(--accent); transform: translate(-50%, -50%);
          transition: left .7s cubic-bezier(.4,0,.2,1); }
        .wfa-pulse::after { content: ''; position: absolute; inset: -5px; border-radius: 50%;
          border: 1.5px solid var(--accent); animation: wfa-ring 1.05s ease-out infinite; }
        @keyframes wfa-ring { 0% { transform: scale(.5); opacity: .9; } 100% { transform: scale(1.9); opacity: 0; } }
        .wfa-note { font-size: 0.82rem; color: var(--muted); line-height: 1.55; margin-top: 14px; }
        @media (prefers-reduced-motion: reduce) {
          .wfa-stage, .wfa-wire-fill, .wfa-pulse { transition: none; }
          .wfa-pulse { display: none; }
          .wfa-pulse::after { animation: none; }
        }
      `,
        }}
      />
      <div className="wfa-title">{title}</div>
      <div className="wfa-track">
        <div className="wfa-wire" />
        <div className="wfa-wire-fill" style={{ width: `${fillWidth}%` }} />
        {!reduce && <div className="wfa-pulse" style={{ left: `${pulseLeft}%` }} />}
        <div className="wfa-row">
          {stages.map((s, i) => {
            const state = reduce || done ? 'visited' : i === active ? 'active' : i < active ? 'visited' : 'pending';
            return (
              <div key={s.label} className="wfa-stage" data-state={state}>
                <div className="wfa-label">{s.label}</div>
                {s.sub && <div className="wfa-sub">{s.sub}</div>}
              </div>
            );
          })}
        </div>
      </div>
      {note && <div className="wfa-note">{note}</div>}
    </div>
  );
}
