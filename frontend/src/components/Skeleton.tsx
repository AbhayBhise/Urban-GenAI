import React from 'react';
import { ViewType } from '../store';

interface ShimmerBoxProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
}

export function ShimmerBox({
  width = '100%',
  height = 20,
  borderRadius = 4,
  className = '',
  style = {},
}: ShimmerBoxProps) {
  return (
    <div
      className={`shimmer-bg ${className}`}
      style={{
        width,
        height,
        borderRadius,
        ...style,
      }}
    />
  );
}

export function SkeletonText({
  lines = 3,
  height = 14,
  gap = 10,
  lastLineWidth = '60%',
}: {
  lines?: number;
  height?: number;
  gap?: number;
  lastLineWidth?: string;
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap }}>
      {Array.from({ length: lines }).map((_, i) => (
        <ShimmerBox
          key={i}
          height={height}
          width={i === lines - 1 ? lastLineWidth : '100%'}
          borderRadius={3}
        />
      ))}
    </div>
  );
}

export function SkeletonCard({
  height,
  titleWidth = '40%',
  lines = 3,
}: {
  height?: number;
  titleWidth?: string;
  lines?: number;
}) {
  return (
    <div className="card" style={{ height, display: 'flex', flexDirection: 'column', gap: 14 }}>
      <ShimmerBox width={titleWidth} height={20} borderRadius={4} />
      <SkeletonText lines={lines} />
    </div>
  );
}

export function SkeletonMetricStrip({ count = 3 }: { count?: number }) {
  return (
    <div className="metrics-strip">
      {Array.from({ length: count }).map((_, i) => (
        <div className="metric" key={i} style={{ minWidth: 140 }}>
          <ShimmerBox width="60%" height={12} style={{ marginBottom: 6 }} />
          <ShimmerBox width="85%" height={24} borderRadius={4} />
        </div>
      ))}
    </div>
  );
}

export function SkeletonChart({ height = 280 }: { height?: number }) {
  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <ShimmerBox width="35%" height={18} />
        <ShimmerBox width="20%" height={14} />
      </div>
      <div
        style={{
          height,
          display: 'flex',
          alignItems: 'flex-end',
          gap: 12,
          padding: '20px 10px 10px',
          borderBottom: '1px solid var(--border)',
        }}
      >
        {Array.from({ length: 14 }).map((_, i) => {
          // Dynamic varying height pattern
          const h = 25 + ((i * 19) % 65);
          return (
            <div
              key={i}
              className="shimmer-bg"
              style={{
                flex: 1,
                height: `${h}%`,
                borderRadius: '4px 4px 0 0',
              }}
            />
          );
        })}
      </div>
    </div>
  );
}

export function SkeletonTable({ rows = 5, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="card" style={{ overflowX: 'auto' }}>
      <div style={{ display: 'flex', gap: 12, paddingBottom: 14, borderBottom: '1px solid var(--border)' }}>
        {Array.from({ length: cols }).map((_, i) => (
          <ShimmerBox key={i} width={`${100 / cols}%`} height={16} />
        ))}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14, paddingTop: 14 }}>
        {Array.from({ length: rows }).map((_, r) => (
          <div key={r} style={{ display: 'flex', gap: 12 }}>
            {Array.from({ length: cols }).map((_, c) => (
              <ShimmerBox key={c} width={`${100 / cols}%`} height={14} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export function PageSkeleton({ view }: { view?: ViewType }) {
  if (view === 'training') {
    return (
      <div className="page-enter" style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div className="panel-header">
          <ShimmerBox width="45%" height={32} style={{ marginBottom: 12 }} />
          <ShimmerBox width="70%" height={16} />
        </div>
        <SkeletonChart height={220} />
        <SkeletonChart height={220} />
      </div>
    );
  }

  if (view === 'evaluation' || view === 'model-comparison') {
    return (
      <div className="page-enter" style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div className="panel-header">
          <ShimmerBox width="40%" height={32} style={{ marginBottom: 12 }} />
          <ShimmerBox width="65%" height={16} />
        </div>
        <SkeletonMetricStrip count={4} />
        <SkeletonTable rows={6} cols={5} />
      </div>
    );
  }

  if (view === 'datasets' || view === 'model-explorer' || view === 'landing') {
    return (
      <div className="page-enter" style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div className="panel-header">
          <ShimmerBox width="50%" height={32} style={{ marginBottom: 12 }} />
          <ShimmerBox width="75%" height={16} />
        </div>
        <div className="grid-2">
          <SkeletonCard height={180} />
          <SkeletonCard height={180} />
          <SkeletonCard height={180} />
          <SkeletonCard height={180} />
        </div>
      </div>
    );
  }

  // Default generic high-grade page skeleton
  return (
    <div className="page-enter" style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div className="panel-header">
        <ShimmerBox width="35%" height={30} style={{ marginBottom: 10 }} />
        <ShimmerBox width="60%" height={16} />
      </div>
      <div className="grid-2">
        <SkeletonCard height={240} />
        <SkeletonCard height={240} />
      </div>
    </div>
  );
}
