import React, { useEffect, useRef, useState } from 'react';
import { apiFetch } from '../lib/api';
import TransparencyBanner from '../lib/TransparencyBanner';

export default function PlanGenerator() {
  const [presets, setPresets] = useState<string[]>([]);
  const [prompt, setPrompt] = useState('');
  const [temperature, setTemperature] = useState(0.8);
  const [maxTokens, setMaxTokens] = useState(320);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [attachedFileName, setAttachedFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    apiFetch('/generate/plan/presets')
      .then(r => r.json())
      .then(d => {
        setPresets(d.presets || []);
        if (d.presets?.length) setPrompt(d.presets[0]);
      })
      .catch(() => {});
  }, []);

  const generate = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await apiFetch('/generate/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, max_new_tokens: maxTokens, temperature }),
      });
      if (!res.ok) {
        setError(res.status === 401 ? 'API key required — set it in the sidebar.' : await res.text());
        return;
      }
      setResult(await res.json());
    } catch (e: any) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  const label = (p: string) => {
    const m = p.match(/Context:\s*(.+?)(?:\s+with|\.)/);
    return m ? m[1] : p.slice(0, 40);
  };

  const handleFileSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    e.target.value = '';
    if (!f) return;
    setError(null);
    const reader = new FileReader();
    reader.onload = () => {
      setPrompt(String(reader.result ?? ''));
      setAttachedFileName(f.name);
    };
    reader.onerror = () => setError('Could not read the selected file.');
    reader.readAsText(f);
  };

  const clearAttachedFile = () => {
    setAttachedFileName(null);
  };

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Urban Plan Generator</h1>
        <div className="panel-desc">
          A decoder-only <strong>Transformer</strong> (MiniGPT) built from scratch —
          multi-head causal self-attention, learned positional embeddings, autoregressive
          sampling — trained on an urban-planning corpus. Prompted with real Pune land-use
          statistics, it drafts sustainability recommendations for planner review.
        </div>
      </div>

      <div style={{ marginBottom: 20 }}><TransparencyBanner /></div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title">Prompt</div>

        {presets.length > 0 && (
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
            {presets.map((p, i) => (
              <button
                key={i}
                onClick={() => { setPrompt(p); setAttachedFileName(null); }}
                className="btn"
                style={{
                  width: 'auto', marginTop: 0, padding: '6px 12px', fontSize: '0.8rem',
                  background: prompt === p ? 'var(--accent)' : 'transparent',
                  color: prompt === p ? 'var(--btn-text)' : 'var(--text)',
                  border: '1px solid var(--border)',
                }}
              >
                {i === 0 ? '★ From Pune stats' : label(p)}
              </button>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn"
            style={{
              width: 'auto', marginTop: 0, padding: '6px 12px', fontSize: '0.8rem',
              background: 'transparent', color: 'var(--text)', border: '1px solid var(--border)',
            }}
          >
            📎 Attach text file
          </button>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            accept=".txt,text/plain"
            onChange={handleFileSelected}
          />
          {attachedFileName && (
            <span style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>
              Loaded from <strong style={{ color: 'var(--text)' }}>{attachedFileName}</strong>
              {' '}
              <button
                onClick={clearAttachedFile}
                style={{
                  background: 'none', border: 'none', color: 'var(--muted)',
                  cursor: 'pointer', textDecoration: 'underline', fontSize: '0.8rem', padding: 0,
                }}
              >
                clear
              </button>
            </span>
          )}
        </div>

        <textarea
          value={prompt}
          onChange={e => { setPrompt(e.target.value); setAttachedFileName(null); }}
          style={{
            width: '100%', minHeight: 120, background: 'var(--bg)', color: 'var(--text)',
            border: '1px solid var(--border)', borderRadius: 4, padding: 12,
            fontFamily: 'var(--font-mono)', fontSize: '0.85rem', lineHeight: 1.5,
          }}
        />

        <div style={{ display: 'flex', gap: 24, alignItems: 'center', marginTop: 14, flexWrap: 'wrap' }}>
          <label style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
            Temperature: <span style={{ color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}>{temperature.toFixed(2)}</span>
            <input type="range" min={0.2} max={1.5} step={0.05} value={temperature}
              onChange={e => setTemperature(parseFloat(e.target.value))}
              style={{ display: 'block', width: 200, marginTop: 4 }} />
          </label>
          <label style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
            Max new tokens: <span style={{ color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}>{maxTokens}</span>
            <input type="range" min={64} max={400} step={16} value={maxTokens}
              onChange={e => setMaxTokens(parseInt(e.target.value))}
              style={{ display: 'block', width: 200, marginTop: 4 }} />
          </label>
        </div>

        <button className="btn" onClick={generate} disabled={loading || !prompt.trim()}>
          {loading ? 'Generating…' : 'Generate Recommendations'}
        </button>
      </div>

      {error && (
        <div className="card" style={{ borderColor: 'var(--danger)', color: 'var(--danger)', marginBottom: 24 }}>
          {error}
        </div>
      )}

      {result && (
        <div className="card">
          <div className="card-title">
            Generated draft
            <span style={{ color: 'var(--muted)', fontWeight: 400 }}>
              {result.num_tokens} tokens · T={result.temperature}
            </span>
          </div>
          <pre style={{
            whiteSpace: 'pre-wrap', fontFamily: 'var(--font-mono)', fontSize: '0.85rem',
            lineHeight: 1.6, color: 'var(--text)', margin: 0,
          }}>
            <span style={{ color: 'var(--muted)' }}>{result.prompt}</span>
            <span>{result.continuation}</span>
          </pre>
        </div>
      )}

      <div className="card" style={{ marginTop: 24 }}>
        <div className="card-title">How it works</div>
        <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
          Each character is embedded and added to a <em>learned positional embedding</em> so
          the model knows token order. Four pre-norm blocks apply <em>causal multi-head
          self-attention</em> (each position attends only to earlier positions) followed by an
          MLP. A weight-tied head predicts the next character; sampling with temperature and
          top-k repeats this autoregressively. Trained from scratch — no pretrained weights.
        </div>
      </div>
    </div>
  );
}
