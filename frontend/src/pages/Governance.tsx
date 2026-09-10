import { useEffect, useState } from 'react';
import { apiFetch } from '../lib/api';
import Markdown from '../lib/Markdown';

const DOCS = [
  { id: 'ethics', label: 'Ethics' },
  { id: 'privacy', label: 'Privacy / GDPR' },
  { id: 'security', label: 'Security' },
  { id: 'model_card', label: 'Model Card' },
];

export default function Governance() {
  const [active, setActive] = useState('ethics');
  const [text, setText] = useState('Loading…');
  const [cache] = useState<Record<string, string>>({});

  useEffect(() => {
    if (cache[active]) { setText(cache[active]); return; }
    setText('Loading…');
    apiFetch(`/governance/${active}`)
      .then(r => (r.ok ? r.text() : Promise.reject(r.status)))
      .then(t => { cache[active] = t; setText(t); })
      .catch(() => setText('Could not load this document. Is the backend running?'));
  }, [active]);

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Governance</h1>
        <div className="panel-desc">
          Ethical, privacy, and security documentation for UrbanGen AI — mapped to
          the Generative AI syllabus Unit 6 (GDPR, EU AI Act, India DPDP Act, bias,
          security, sustainability). Served live from <code>docs/</code>.
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {DOCS.map(d => (
          <button
            key={d.id}
            onClick={() => setActive(d.id)}
            className="btn"
            style={{
              width: 'auto', marginTop: 0, padding: '8px 16px',
              background: active === d.id ? 'var(--accent)' : 'transparent',
              color: active === d.id ? '#000' : 'var(--text)',
              border: '1px solid var(--border)',
            }}
          >
            {d.label}
          </button>
        ))}
      </div>

      <div className="card">
        <Markdown text={text} />
      </div>
    </div>
  );
}
