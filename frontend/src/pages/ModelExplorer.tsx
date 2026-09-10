// ModelExplorer component
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

        <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} onClick={() => setActiveView('plan-generator')}>
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Cpu size={24} color="#00E676" />
            Transformer (Urban Plan Generator)
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '20px' }}>
            A from-scratch decoder-only Transformer: causal self-attention + positional embeddings, generating urban-planning recommendations from land-use statistics.
          </p>
          <button className="btn" style={{ background: 'transparent', border: '1px solid #00E676', color: '#00E676', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            Explore Transformer <ArrowRight size={16} />
          </button>
        </div>

        <div className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} onClick={() => setActiveView('classifier')}>
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Cpu size={24} color="var(--accent)" />
            Land-Use Classifier (ResNet18)
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '20px' }}>
            Transfer-learned CNN that classifies aerial tiles into 21 zoning categories for automated land-use auditing.
          </p>
          <button className="btn" style={{ background: 'transparent', border: '1px solid var(--accent)', color: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            Explore Classifier <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* Research Progress Cockpit Integration */}
      <div
        className="card"
        style={{
          marginTop: '30px',
          background: 'linear-gradient(135deg, rgba(15, 25, 35, 0.9) 0%, rgba(8, 12, 20, 0.95) 100%)',
          border: '1px solid rgba(0, 212, 255, 0.3)',
          padding: '24px',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '16px' }}>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600, marginBottom: '4px' }}>
              Academic &amp; Systems Roadmap
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#FFF' }}>
              Research &amp; Innovation Progress
            </h2>
          </div>
          <button
            className="btn"
            onClick={() => setActiveView('research')}
            style={{
              width: 'auto',
              margin: 0,
              padding: '10px 22px',
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            Explore Research &amp; Innovation <ArrowRight size={16} />
          </button>
        </div>

        <p style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6, marginBottom: '18px' }}>
          UrbanGen AI connects multi-source Earth observation with generative AI models for urban planning decision support. Real models are verified against committed checkpoints and empirical loss curves:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px' }}>
          {[
            { label: 'Data Pipeline', status: '✓ Active', color: 'var(--success)', bg: 'rgba(0, 230, 118, 0.1)' },
            { label: 'Autoencoder', status: '✓ Trained', color: 'var(--success)', bg: 'rgba(0, 230, 118, 0.1)' },
            { label: 'Spatial VAE', status: '✓ Trained', color: 'var(--success)', bg: 'rgba(0, 230, 118, 0.1)' },
            { label: 'Spectral GAN', status: '◐ In Dev', color: '#FFB300', bg: 'rgba(255, 179, 0, 0.1)' },
            { label: 'Prediction', status: '○ Planned', color: 'var(--muted)', bg: 'rgba(74, 96, 128, 0.1)' },
            { label: 'MiniGPT Planner', status: '✓ Trained', color: 'var(--success)', bg: 'rgba(0, 230, 118, 0.1)' },
            { label: 'Diffusion Vis', status: '○ Planned', color: 'var(--muted)', bg: 'rgba(74, 96, 128, 0.1)' },
          ].map((item, idx) => (
            <div
              key={idx}
              style={{
                background: item.bg,
                border: `1px solid ${item.color}33`,
                borderRadius: '6px',
                padding: '10px 12px',
                textAlign: 'center',
              }}
            >
              <div style={{ fontSize: '0.74rem', color: 'var(--text)', marginBottom: '4px' }}>{item.label}</div>
              <div style={{ fontSize: '0.82rem', fontWeight: 600, color: item.color, fontFamily: 'var(--font-mono)' }}>
                {item.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

