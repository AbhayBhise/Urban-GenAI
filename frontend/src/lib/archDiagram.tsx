import React from 'react';

// Shared visual primitives for the per-model "Architecture" pages
// (AEArchitecture, VAEArchitecture, GANArchitecture, TransformerArchitecture).
// Kept in one place so every model's diagram uses the same box/arrow/color
// language instead of four slightly-different hand-rolled versions.

export const COLORS = {
  bg: '#080C14',
  surface: '#0F1923',
  border: '#1E2D40',
  accent: '#00D4FF',
  accent2: '#7B61FF',
  text: '#E8EDF5',
  muted: '#4A6080',
  success: '#00E676',
  warn: '#FFB84D',
  danger: '#FF5252',
};

export function Box({ x, y, w, h, fill, stroke, label, sub, labelColor }: {
  x: number; y: number; w: number; h: number; fill: string; stroke: string;
  label: string; sub?: string; labelColor?: string;
}) {
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={8} fill={fill} stroke={stroke} strokeWidth={1.5} />
      <text x={x + w / 2} y={y + (sub ? h / 2 - 6 : h / 2 + 5)} textAnchor="middle"
        fontSize="12.5" fontWeight={600} fill={labelColor || COLORS.text} fontFamily="var(--font-ui)">
        {label}
      </text>
      {sub && (
        <text x={x + w / 2} y={y + h / 2 + 12} textAnchor="middle" fontSize="10.5"
          fill={COLORS.muted} fontFamily="var(--font-mono)">
          {sub}
        </text>
      )}
    </g>
  );
}

export function Arrow({ x1, y1, x2, y2, color }: { x1: number; y1: number; x2: number; y2: number; color?: string }) {
  return (
    <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color || COLORS.muted} strokeWidth={1.75}
      markerEnd="url(#arrowhead)" />
  );
}

/** Every diagram SVG must include this once in its <defs>. */
export function ArrowheadDef() {
  return (
    <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill={COLORS.muted} />
    </marker>
  );
}

export function SyllabusTable({ rows }: { rows: [string, string][] }) {
  return (
    <div className="card">
      <div className="card-title">Syllabus Alignment</div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--muted)', textAlign: 'left' }}>
              <th style={{ padding: '8px 12px' }}>Syllabus requirement</th>
              <th style={{ padding: '8px 12px' }}>Where it's demonstrated here</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(([req, where]) => (
              <tr key={req} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '8px 12px', fontWeight: 600 }}>{req}</td>
                <td style={{ padding: '8px 12px', color: 'var(--muted)' }}>{where}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function ProvenanceNote({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 20,
      padding: '12px 16px', borderRadius: 6, background: 'rgba(0, 230, 118, 0.06)',
      border: '1px solid rgba(0, 230, 118, 0.25)', fontSize: '0.85rem',
    }}>
      <strong style={{ color: 'var(--success)', flexShrink: 0 }}>Trained by us:</strong>
      <span style={{ color: 'var(--text)' }}>{children}</span>
    </div>
  );
}
