import React from 'react';
import { AlertCircle } from 'lucide-react';

// EU AI Act Art. 50 transparency: AI-generated output must be labelled.
export default function TransparencyBanner({ compact = false }: { compact?: boolean }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 10,
      background: 'rgba(255, 184, 77, 0.08)',
      border: '1px solid rgba(255, 184, 77, 0.3)',
      color: '#FFB84D', borderRadius: 6,
      padding: compact ? '8px 12px' : '12px 16px',
      fontSize: compact ? '0.8rem' : '0.85rem', lineHeight: 1.5,
    }}>
      <AlertCircle size={compact ? 14 : 16} style={{ flexShrink: 0 }} />
      <span>
        AI-generated output — advisory only. Not professional planning advice;
        requires review by qualified urban planners before any use.
      </span>
    </div>
  );
}
