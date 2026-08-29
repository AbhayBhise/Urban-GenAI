import React from 'react';
import { Layers, FileText, Cpu, ArrowRight } from 'lucide-react';

interface ModelExplorerProps {
  setActiveView: (view: any) => void;
}

export default function ModelExplorer({ setActiveView }: ModelExplorerProps) {
  return (
    <div className="panel-header">
      <h1 className="panel-title">Model Explorer Hub</h1>
      <div className="panel-desc">
        Select a model architecture below to explore its internal mechanics, layers, and processing pipeline.
      </div>
      
      <div className="grid-2" style={{ marginTop: '30px' }}>
        <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} onClick={() => setActiveView('ae')}>
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Layers size={24} color="var(--accent)" />
            Autoencoder (AE)
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '20px' }}>
            Learn how the autoencoder compresses urban imagery into a dense latent representation and reconstructs it.
          </p>
          <button className="btn" style={{ background: 'transparent', border: '1px solid var(--accent)', color: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            Explore Autoencoder <ArrowRight size={16} />
          </button>
        </div>

        <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} onClick={() => setActiveView('vae')}>
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileText size={24} color="var(--accent2)" />
            Variational Autoencoder (VAE)
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '20px' }}>
            Explore the probabilistic latent space used for generating smooth interpolations of urban features.
          </p>
          <button className="btn" style={{ background: 'transparent', border: '1px solid var(--accent2)', color: 'var(--accent2)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            Explore VAE <ArrowRight size={16} />
          </button>
        </div>

        <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} onClick={() => setActiveView('transformer')}>
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Cpu size={24} color="#00E676" />
            Transformer (UrbanViT)
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '20px' }}>
            Visualize how self-attention mechanisms classify urban land-use patterns into distinct categories.
          </p>
          <button className="btn" style={{ background: 'transparent', border: '1px solid #00E676', color: '#00E676', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            Explore Transformer <ArrowRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
