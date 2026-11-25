import { Target, Database, Cpu } from 'lucide-react';

interface ModelUseCaseCardProps {
  datasetRole: string;
  inferenceAction: string;
  projectValue: string;
}

export default function ModelUseCaseCard({
  datasetRole,
  inferenceAction,
  projectValue,
}: ModelUseCaseCardProps) {
  return (
    <div
      className="card"
      style={{
        marginBottom: 24,
        borderLeft: '4px solid var(--accent)',
        background: 'var(--surface)',
      }}
    >
      <div className="card-title" style={{ marginBottom: 12 }}>
        What This Model Is Meant For
      </div>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 14,
          fontSize: '0.84rem',
          lineHeight: 1.55,
        }}
      >
        <div
          style={{
            padding: '10px 12px',
            borderRadius: 6,
            background: 'var(--surface-inset)',
            border: '1px solid var(--border)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 700, color: 'var(--accent)', marginBottom: 4 }}>
            <Database size={14} />
            <span>What It Learned From</span>
          </div>
          <div style={{ color: 'var(--text-secondary)' }}>{datasetRole}</div>
        </div>

        <div
          style={{
            padding: '10px 12px',
            borderRadius: 6,
            background: 'var(--surface-inset)',
            border: '1px solid var(--border)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 700, color: 'var(--accent2)', marginBottom: 4 }}>
            <Cpu size={14} />
            <span>What It Does With Your Input</span>
          </div>
          <div style={{ color: 'var(--text-secondary)' }}>{inferenceAction}</div>
        </div>

        <div
          style={{
            padding: '10px 12px',
            borderRadius: 6,
            background: 'var(--surface-inset)',
            border: '1px solid var(--border)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 700, color: 'var(--success)', marginBottom: 4 }}>
            <Target size={14} />
            <span>Why It Matters (Use Case)</span>
          </div>
          <div style={{ color: 'var(--text-secondary)' }}>{projectValue}</div>
        </div>
      </div>
    </div>
  );
}
