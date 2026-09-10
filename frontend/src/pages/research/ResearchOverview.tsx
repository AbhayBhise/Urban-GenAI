import { Compass, Layers, ShieldAlert, Cpu, Sparkles, BookOpen, GitFork, ArrowRight } from 'lucide-react';

interface ResearchOverviewProps {
  onNavigateTab: (tabId: any) => void;
}

export default function ResearchOverview({ onNavigateTab }: ResearchOverviewProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Planner Cockpit Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.08) 0%, rgba(123, 97, 255, 0.08) 100%)',
          border: '1px solid rgba(0, 212, 255, 0.25)',
          padding: '28px',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ maxWidth: '820px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
              <span
                style={{
                  background: 'rgba(0, 212, 255, 0.15)',
                  color: 'var(--accent)',
                  border: '1px solid rgba(0, 212, 255, 0.3)',
                  padding: '4px 10px',
                  borderRadius: '4px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  letterSpacing: '0.08em',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                }}
              >
                <Compass size={14} /> Urban Planner Persona &amp; Decision-Support
              </span>
              <span
                style={{
                  background: 'rgba(0, 230, 118, 0.1)',
                  color: 'var(--success)',
                  border: '1px solid rgba(0, 230, 118, 0.2)',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                }}
              >
                Phase 1 Active (Verified Pipeline)
              </span>
            </div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '12px', lineHeight: 1.3 }}>
              UrbanGen AI: An AI-Assisted Generative Framework for Urban Digital Twins
            </h2>
            <p style={{ color: 'var(--text)', fontSize: '0.98rem', lineHeight: 1.7, marginBottom: '14px' }}>
              In contemporary municipal planning, human planners face intricate dilemmas: accommodating population surges, mitigating Urban Heat Islands (UHI), preserving riparian buffer corridors, and maintaining transit accessibility. <strong>UrbanGen AI</strong> positions the <strong>Urban Planner</strong> at the heart of the computational loop—providing an integrated generative digital twin to explore, evaluate, and explain multiple scenario alternatives rather than enforcing single rigid master plans.
            </p>
            <p style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Case Context: <strong>Pune Metropolitan Region (PMC jurisdiction: ~516 km², 7.4M residents in 2026 → projected 10M by 2041)</strong>. The framework combines satellite observation, land-use semantics, road networks, terrain contours, and population distribution into a unified representation pipeline.
            </p>
          </div>

          <div
            style={{
              background: 'rgba(8, 12, 20, 0.75)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '16px 20px',
              minWidth: '220px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
            }}
          >
            <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Planner Core Modules
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Denoising AE</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>Trained ✓</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Spatial VAE</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>Trained ✓</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Planner MiniGPT</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>Trained ✓</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Zoning Classifier</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>98.1% Val ✓</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Pune GIS RAG</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>Active ✓</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Spectral GAN</span>
              <span style={{ color: '#FFB300', fontWeight: 600 }}>In Dev ◐</span>
            </div>
          </div>
        </div>
      </div>

      {/* The Three Pillars of Planner Decision Support */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent)', marginBottom: '12px' }}>
              <Layers size={20} />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text)' }}>1. Unified Spatial Ingestion</h3>
            </div>
            <p style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.65, marginBottom: '14px' }}>
              Planners traditionally endure fragmented workflows—switching between ArcGIS/QGIS rasters, municipal vector shapefiles, and census tables. UrbanGen AI designs a unified <strong>City Stack</strong> representation aligning spectral data (HLS S30), land-cover classes (WorldCover), infrastructural road graphs (OSM), topography (DEM), and population density.
            </p>
          </div>
          <button
            onClick={() => onNavigateTab('approach')}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--accent)',
              fontSize: '0.82rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              padding: 0,
              marginTop: '10px',
            }}
          >
            Explore System Architecture <ArrowRight size={14} />
          </button>
        </div>

        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent2)', marginBottom: '12px' }}>
              <Sparkles size={20} />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text)' }}>2. Multi-Scenario Latent Exploration</h3>
            </div>
            <p style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.65, marginBottom: '14px' }}>
              Single-output predictive models restrict urban planning creativity. UrbanGen AI employs a <strong>Spatial Variational Autoencoder (VAE)</strong> with a continuous latent manifold (64 × 8 × 8 = 4,096 spatial dimensions). Planners can interpolate between contrasting urban morphologies (e.g., dense commercial vs transit-oriented green buffer) to evaluate intermediate options.
            </p>
          </div>
          <button
            onClick={() => onNavigateTab('approach')}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--accent2)',
              fontSize: '0.82rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              padding: 0,
              marginTop: '10px',
            }}
          >
            View VAE Scenario Mechanics <ArrowRight size={14} />
          </button>
        </div>

        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--success)', marginBottom: '12px' }}>
              <Cpu size={20} />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text)' }}>3. Grounded Advisory Policy Drafting</h3>
            </div>
            <p style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.65, marginBottom: '14px' }}>
              Pixel maps alone do not form municipal proposals. Our from-scratch <strong>MiniGPT Transformer</strong> is conditioned on real Pune ward statistics (dominant land-use, road length, waterways). It drafts structured recommendations on permeable surfaces, building setbacks, floodplain reservations, and transit-oriented parking caps.
            </p>
          </div>
          <button
            onClick={() => onNavigateTab('progress')}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--success)',
              fontSize: '0.82rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              padding: 0,
              marginTop: '10px',
            }}
          >
            Review Verified Metrics <ArrowRight size={14} />
          </button>
        </div>
      </div>

      {/* Literature & Gap Callout Card */}
      <div
        className="card"
        style={{
          background: 'rgba(15, 25, 35, 0.8)',
          borderLeft: '4px solid var(--accent)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '16px',
        }}
      >
        <div>
          <div style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text)', marginBottom: '4px' }}>
            Academic Literature Survey &amp; Synthesis
          </div>
          <div style={{ color: 'var(--muted)', fontSize: '0.85rem' }}>
            Anchored in 7 landmark scoping reviews (Urban Informatics 2024, Progress in Planning 2024, Engineering 2026, Sustainable Cities and Society 2026, npj Urban Sustainability 2026, IEEE COINS 2025, AI Review).
          </div>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            className="btn"
            onClick={() => onNavigateTab('literature')}
            style={{
              width: 'auto',
              margin: 0,
              padding: '8px 16px',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <BookOpen size={15} /> Literature Table
          </button>
          <button
            className="btn"
            onClick={() => onNavigateTab('gap')}
            style={{
              width: 'auto',
              margin: 0,
              padding: '8px 16px',
              fontSize: '0.85rem',
              background: 'transparent',
              border: '1px solid var(--border)',
              color: 'var(--text)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <GitFork size={15} /> Research Gap
          </button>
        </div>
      </div>

      {/* Mandatory Scientific Disclaimer & Research Positioning */}
      <div
        className="card"
        style={{
          background: 'rgba(255, 179, 0, 0.04)',
          border: '1px solid rgba(255, 179, 0, 0.25)',
          padding: '22px 24px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#FFB300', marginBottom: '10px' }}>
          <ShieldAlert size={20} />
          <h3 style={{ fontSize: '0.98rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Scientific Positioning &amp; Professional Urban Planning Disclaimer
          </h3>
        </div>
        <p style={{ color: 'var(--text)', fontSize: '0.88rem', lineHeight: 1.7, marginBottom: '10px' }}>
          <strong>UrbanGen AI is a research prototype and decision-support framework.</strong> It is designed to augment—not replace—professional urban planning practitioners, certified GIS analysts, civil engineers, and municipal policymakers.
        </p>
        <p style={{ color: 'var(--muted)', fontSize: '0.85rem', lineHeight: 1.65 }}>
          Generated spatial scenarios and text policies are <em>candidate computational representations</em>. They require thorough empirical validation against statutory development control regulations (e.g., Pune DCPR 2017/2021), structural engineering constraints, hydraulic/drainage watershed simulations, microclimate models, and transparent public stakeholder hearings before any real-world municipal adoption.
        </p>
      </div>
    </div>
  );
}
