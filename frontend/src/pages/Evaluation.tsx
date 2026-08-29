import React from 'react';

export default function Evaluation() {
  return (
    <div className="panel-header">
      <h1 className="panel-title">Model Evaluation</h1>
      <div className="panel-desc">
        Evaluate model performance using metrics such as PSNR, SSIM, KL Divergence, and analyze confusion matrices.
      </div>
      <div style={{ marginTop: '40px', color: 'var(--muted)', textAlign: 'center' }}>
        Evaluation results coming soon...
      </div>
    </div>
  );
}
