import React from 'react';

export default function ModelComparison() {
  return (
    <div className="panel-header">
      <h1 className="panel-title">Model Comparison</h1>
      <div className="panel-desc">
        Compare the architectures, parameter counts, and inference speeds of the Autoencoder, VAE, and Transformer models side-by-side.
      </div>
      <div style={{ marginTop: '40px', color: 'var(--muted)', textAlign: 'center' }}>
        Comparison metrics will be populated here shortly...
      </div>
    </div>
  );
}
