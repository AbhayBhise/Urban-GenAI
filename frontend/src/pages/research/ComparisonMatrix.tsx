import React, { useState } from 'react';
import { Clock, Minus, CheckCircle2, Layers, BrainCircuit, Activity, Eye, Compass, Table, LayoutGrid } from 'lucide-react';

interface MatrixRow {
  capability: string;
  category: 'Data Ingestion' | 'Neural Modeling' | 'Evaluation & Simulation' | 'Planner Explanation' | 'Digital Twin Visualization' | 'Decision Cockpit';
  literatureStatus: 'Common' | 'Partial' | 'Rare';
  literatureDetail: string;
  urbanGenStatus: 'Implemented' | 'In Development' | 'Planned';
  urbanGenDetail: string;
}

const COMPARISON_ROWS: MatrixRow[] = [
  // 1. Data Ingestion
  {
    capability: 'Multi-source geospatial data',
    category: 'Data Ingestion',
    literatureStatus: 'Partial',
    literatureDetail: 'Often restricted to 1–2 sources (e.g., imagery alone or vector GIS alone).',
    urbanGenStatus: 'In Development',
    urbanGenDetail: 'Ingests satellite, land cover, road networks, terrain DEM, and census grids.',
  },
  {
    capability: 'Satellite multispectral imagery',
    category: 'Data Ingestion',
    literatureStatus: 'Common',
    literatureDetail: 'Widely used in remote sensing for classification, index mapping, and segmentation.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Utilized in UCMerced / EuroSAT benchmarks; NASA HLS S30 planned.',
  },
  {
    capability: 'Land-cover semantics',
    category: 'Data Ingestion',
    literatureStatus: 'Common',
    literatureDetail: 'Categorical raster maps (ESA WorldCover, Dynamic World) used in isolated studies.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Integrated into ResNet18 21-class classifier; ESA WorldCover pipeline architected.',
  },
  {
    capability: 'Road & building vector networks',
    category: 'Data Ingestion',
    literatureStatus: 'Common',
    literatureDetail: 'Commonly queried via OSMnx or Shapefiles in transportation planning.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Live GeoPandas ingestion of Pune PMC OSM shapefiles (roads, buildings, waterways).',
  },
  {
    capability: 'Terrain & elevation modeling',
    category: 'Data Ingestion',
    literatureStatus: 'Partial',
    literatureDetail: 'Utilized in specialized hydrological runoff or slope hazard studies.',
    urbanGenStatus: 'Planned',
    urbanGenDetail: 'NASA SRTM 30m DEM alignment planned for watershed & flood vulnerability.',
  },
  {
    capability: 'Population density grids',
    category: 'Data Ingestion',
    literatureStatus: 'Partial',
    literatureDetail: 'Socioeconomic raster grids (WorldPop, JRC GHSL) studied in demography.',
    urbanGenStatus: 'Planned',
    urbanGenDetail: 'WorldPop 100m grid ingestion designed for per-capita infrastructure audits.',
  },
  {
    capability: 'Unified City Stack alignment',
    category: 'Data Ingestion',
    literatureStatus: 'Rare',
    literatureDetail: 'Data preparation usually done ad-hoc across separate GIS software without a standard tensor pipeline.',
    urbanGenStatus: 'In Development',
    urbanGenDetail: 'Unified H×W×C tensor pipeline aligning multi-resolution rasters & rasterized vectors.',
  },

  // 2. Neural Modeling
  {
    capability: 'Unsupervised representation learning',
    category: 'Neural Modeling',
    literatureStatus: 'Common',
    literatureDetail: 'Established in computer vision (Autoencoders, SimCLR, MAE), but seldom applied to heterogeneous urban stacks.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'ResNet18 Denoising Autoencoder (50 epochs, MSE 0.01977, 8×8×256 bottleneck).',
  },
  {
    capability: 'Probabilistic scenario generation',
    category: 'Neural Modeling',
    literatureStatus: 'Partial',
    literatureDetail: 'VAEs utilized for isolated 2D parcel shapes or floorplans; rarely on multi-source land tiles.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Spatial VAE (64×8×8 bottleneck) enabling continuous latent scenario interpolation.',
  },
  {
    capability: 'Multiple alternative exploration',
    category: 'Neural Modeling',
    literatureStatus: 'Partial',
    literatureDetail: 'Traditional GIS generates one deterministic map; generative tools often output disconnected samples.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Continuous latent space traversal allows planners to explore smooth trade-offs.',
  },
  {
    capability: 'Urban morphology texture generation',
    category: 'Neural Modeling',
    literatureStatus: 'Common',
    literatureDetail: 'Pix2Pix, CycleGAN, and StyleGAN applied to aerial texture and building facade rendering.',
    urbanGenStatus: 'In Development',
    urbanGenDetail: 'Class-Conditional Spectral-Norm GAN (backend/models/gan.py) with EMA weights.',
  },

  // 3. Evaluation & Simulation
  {
    capability: 'Multi-subsystem impact prediction',
    category: 'Evaluation & Simulation',
    literatureStatus: 'Partial',
    literatureDetail: 'Sophisticated engineering models exist (e.g. MATSim, EPA SWMM), but operate as standalone tools.',
    urbanGenStatus: 'Planned',
    urbanGenDetail: 'Surrogate neural networks planned for Traffic, AQI, Flood risk, Energy, and Water.',
  },
  {
    capability: 'Automated anomaly & zoning auditing',
    category: 'Evaluation & Simulation',
    literatureStatus: 'Rare',
    literatureDetail: 'Zoning audits performed manually; reconstruction error rarely operationalized as an anomaly score.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Empirical anomaly z-scoring against 300 real tiles + 21-class zoning verification (98.1% accuracy).',
  },

  // 4. Planner Explanation
  {
    capability: 'LLM-driven planning policy explanation',
    category: 'Planner Explanation',
    literatureStatus: 'Partial',
    literatureDetail: 'Recent studies explore LLMs, but often suffer spatial hallucination due to lack of ground GIS context.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'From-scratch MiniGPT Transformer trained on urban planning corpus & conditioned on real Pune stats.',
  },

  // 5. Digital Twin Visualization
  {
    capability: 'Photorealistic future-city visualization',
    category: 'Digital Twin Visualization',
    literatureStatus: 'Partial',
    literatureDetail: 'Diffusion models recently applied to architectural sketches; city-scale satellite diffusion is emerging.',
    urbanGenStatus: 'Planned',
    urbanGenDetail: 'Latent Diffusion Model (Phase 14 roadmap) for high-resolution future city renders.',
  },

  // 6. Decision Cockpit
  {
    capability: 'Human-in-the-loop planner decision support',
    category: 'Decision Cockpit',
    literatureStatus: 'Partial',
    literatureDetail: 'Most AI systems operate in batch mode or black-box demos without interactive governance controls.',
    urbanGenStatus: 'Implemented',
    urbanGenDetail: 'Integrated planner cockpit with real-time inference, sample loading, governance cards, and ethical guardrails.',
  },
];

const CATEGORY_META = {
  'Data Ingestion': { label: '01. Data Ingestion & Spatial Stacking', icon: Layers, color: '#00D4FF' },
  'Neural Modeling': { label: '02. Neural Representation & Generation', icon: BrainCircuit, color: '#9D85FF' },
  'Evaluation & Simulation': { label: '03. Impact Auditing & Anomaly Scoring', icon: Activity, color: '#00E676' },
  'Planner Explanation': { label: '04. Natural Language Policy Explanation', icon: Compass, color: '#FFB300' },
  'Digital Twin Visualization': { label: '05. Photorealistic Digital Twin Rendering', icon: Eye, color: '#FF4081' },
  'Decision Cockpit': { label: '06. Human-in-the-Loop Governance', icon: CheckCircle2, color: '#26C6DA' },
};

export default function ComparisonMatrix() {
  const [statusFilter, setStatusFilter] = useState<'All' | 'Implemented' | 'In Development' | 'Planned'>('All');
  const [viewMode, setViewMode] = useState<'grouped' | 'cards'>('grouped');

  const filteredRows = COMPARISON_ROWS.filter(r => {
    if (statusFilter === 'All') return true;
    return r.urbanGenStatus === statusFilter;
  });

  const categories = Object.keys(CATEGORY_META) as (keyof typeof CATEGORY_META)[];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
      {/* Header & Controls */}
      <div className="card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px', marginBottom: '12px' }}>
          <div className="card-title" style={{ margin: 0 }}>
            Capability Matrix: Existing Academic Literature vs. UrbanGen AI
          </div>

          {/* View Toggle */}
          <div style={{ display: 'flex', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '3px' }}>
            <button
              onClick={() => setViewMode('grouped')}
              style={{
                background: viewMode === 'grouped' ? 'rgba(0, 212, 255, 0.15)' : 'transparent',
                color: viewMode === 'grouped' ? 'var(--accent)' : 'var(--muted)',
                border: 'none',
                borderRadius: '4px',
                padding: '6px 12px',
                fontSize: '0.8rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
              }}
            >
              <Table size={14} /> Grouped Matrix
            </button>
            <button
              onClick={() => setViewMode('cards')}
              style={{
                background: viewMode === 'cards' ? 'rgba(0, 212, 255, 0.15)' : 'transparent',
                color: viewMode === 'cards' ? 'var(--accent)' : 'var(--muted)',
                border: 'none',
                borderRadius: '4px',
                padding: '6px 12px',
                fontSize: '0.8rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
              }}
            >
              <LayoutGrid size={14} /> Side-by-Side Cards
            </button>
          </div>
        </div>

        <p style={{ color: 'var(--text)', fontSize: '0.92rem', lineHeight: 1.65, marginBottom: '16px' }}>
          Structured comparison of 16 core urban planning capabilities. The goal is to highlight how UrbanGen AI synthesizes historically isolated algorithms into an integrated, planner-facing decision workspace.
        </p>

        {/* Status Filter Buttons */}
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'center' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Filter by Status:</span>
          {(['All', 'Implemented', 'In Development', 'Planned'] as const).map(status => {
            const isSelected = statusFilter === status;
            return (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                style={{
                  background: isSelected ? 'var(--accent)' : 'rgba(30, 45, 64, 0.4)',
                  color: isSelected ? '#000' : 'var(--text)',
                  border: `1px solid ${isSelected ? 'var(--accent)' : 'var(--border)'}`,
                  borderRadius: '4px',
                  padding: '5px 12px',
                  fontSize: '0.76rem',
                  fontWeight: isSelected ? 700 : 400,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                {status === 'All' ? 'All (16 Capabilities)' : status}
              </button>
            );
          })}
        </div>
      </div>

      {/* VIEW 1: GROUPED MATRIX TABLE (With section headers, crystal clear column widths) */}
      {viewMode === 'grouped' && (
        <div style={{ overflowX: 'auto', borderRadius: '8px', border: '1px solid var(--border)', background: 'var(--surface)' }}>
          <table style={{ width: '100%', minWidth: '1100px', borderCollapse: 'collapse', fontSize: '0.86rem' }}>
            <thead>
              <tr style={{ background: 'rgba(8, 12, 20, 0.95)', borderBottom: '2px solid var(--border)', textAlign: 'left', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontSize: '0.73rem', position: 'sticky', top: 0, zIndex: 2 }}>
                <th style={{ padding: '16px 20px', width: '28%' }}>Urban Planning Capability</th>
                <th style={{ padding: '16px 20px', width: '36%' }}>Existing Literature Landscape</th>
                <th style={{ padding: '16px 20px', width: '36%' }}>UrbanGen AI Implementation &amp; Status</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(cat => {
                const rowsInCat = filteredRows.filter(r => r.category === cat);
                if (rowsInCat.length === 0) return null;
                const meta = CATEGORY_META[cat];
                const Icon = meta.icon;

                return (
                  <React.Fragment key={cat}>
                    {/* Category Divider Row */}
                    <tr style={{ background: 'rgba(15, 25, 35, 0.95)', borderTop: '2px solid var(--border)', borderBottom: '1px solid var(--border)' }}>
                      <td colSpan={3} style={{ padding: '12px 20px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: meta.color, fontWeight: 700, fontSize: '0.82rem', letterSpacing: '0.04em' }}>
                          <Icon size={16} />
                          <span>{meta.label}</span>
                          <span style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: 400 }}>
                            ({rowsInCat.length} {rowsInCat.length === 1 ? 'capability' : 'capabilities'})
                          </span>
                        </div>
                      </td>
                    </tr>

                    {/* Data Rows */}
                    {rowsInCat.map((row, idx) => (
                      <tr
                        key={idx}
                        style={{
                          borderBottom: '1px solid var(--border)',
                          background: idx % 2 === 0 ? 'transparent' : 'rgba(255, 255, 255, 0.012)',
                          verticalAlign: 'top',
                        }}
                      >
                        {/* Capability Name */}
                        <td style={{ padding: '16px 20px', fontWeight: 600, color: '#FFF' }}>
                          <div style={{ lineHeight: 1.4 }}>{row.capability}</div>
                        </td>

                        {/* Existing Literature */}
                        <td style={{ padding: '16px 20px', lineHeight: 1.5 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                            <span
                              style={{
                                background: row.literatureStatus === 'Common' ? 'rgba(0, 230, 118, 0.1)' : row.literatureStatus === 'Partial' ? 'rgba(255, 179, 0, 0.1)' : 'rgba(255, 82, 82, 0.1)',
                                color: row.literatureStatus === 'Common' ? 'var(--success)' : row.literatureStatus === 'Partial' ? '#FFB300' : '#FF5252',
                                border: `1px solid ${row.literatureStatus === 'Common' ? 'rgba(0, 230, 118, 0.25)' : row.literatureStatus === 'Partial' ? 'rgba(255, 179, 0, 0.25)' : 'rgba(255, 82, 82, 0.25)'}`,
                                padding: '1px 6px',
                                borderRadius: '3px',
                                fontSize: '0.68rem',
                                fontWeight: 600,
                              }}
                            >
                              {row.literatureStatus}
                            </span>
                          </div>
                          <div style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>
                            {row.literatureDetail}
                          </div>
                        </td>

                        {/* UrbanGen AI Implementation */}
                        <td style={{ padding: '16px 20px', lineHeight: 1.5 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                            {row.urbanGenStatus === 'Implemented' && (
                              <span style={{ background: 'rgba(0, 230, 118, 0.15)', color: 'var(--success)', border: '1px solid rgba(0, 230, 118, 0.3)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                <CheckCircle2 size={12} /> Verified Implemented
                              </span>
                            )}
                            {row.urbanGenStatus === 'In Development' && (
                              <span style={{ background: 'rgba(255, 179, 0, 0.15)', color: '#FFB300', border: '1px solid rgba(255, 179, 0, 0.3)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                <Clock size={12} /> In Development
                              </span>
                            )}
                            {row.urbanGenStatus === 'Planned' && (
                              <span style={{ background: 'rgba(74, 96, 128, 0.15)', color: 'var(--muted)', border: '1px solid var(--border)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                <Minus size={12} /> Planned Roadmap
                              </span>
                            )}
                          </div>
                          <div style={{ fontSize: '0.83rem', color: 'var(--text)' }}>
                            {row.urbanGenDetail}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* VIEW 2: SIDE-BY-SIDE CARD VIEW */}
      {viewMode === 'cards' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '16px' }}>
          {filteredRows.map((row, idx) => {
            const meta = CATEGORY_META[row.category];
            const Icon = meta.icon;
            return (
              <div
                key={idx}
                style={{
                  background: 'var(--surface)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                  padding: '18px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: meta.color, fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                    <Icon size={14} /> {row.category}
                  </div>
                  {row.urbanGenStatus === 'Implemented' && (
                    <span style={{ background: 'rgba(0, 230, 118, 0.15)', color: 'var(--success)', border: '1px solid rgba(0, 230, 118, 0.3)', padding: '2px 6px', borderRadius: '4px', fontSize: '0.68rem', fontWeight: 600 }}>
                      ✓ Implemented
                    </span>
                  )}
                  {row.urbanGenStatus === 'In Development' && (
                    <span style={{ background: 'rgba(255, 179, 0, 0.15)', color: '#FFB300', border: '1px solid rgba(255, 179, 0, 0.3)', padding: '2px 6px', borderRadius: '4px', fontSize: '0.68rem', fontWeight: 600 }}>
                      ◐ In Dev
                    </span>
                  )}
                  {row.urbanGenStatus === 'Planned' && (
                    <span style={{ background: 'rgba(74, 96, 128, 0.15)', color: 'var(--muted)', border: '1px solid var(--border)', padding: '2px 6px', borderRadius: '4px', fontSize: '0.68rem', fontWeight: 600 }}>
                      ○ Planned
                    </span>
                  )}
                </div>

                <h4 style={{ fontSize: '0.98rem', fontWeight: 600, color: '#FFF', margin: 0 }}>
                  {row.capability}
                </h4>

                <div style={{ background: 'rgba(8, 12, 20, 0.5)', border: '1px solid var(--border)', borderRadius: '6px', padding: '10px 12px' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '2px' }}>
                    Existing Literature:
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--muted)', lineHeight: 1.45 }}>
                    {row.literatureDetail}
                  </div>
                </div>

                <div style={{ background: 'rgba(0, 212, 255, 0.04)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '6px', padding: '10px 12px', marginTop: 'auto' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--accent)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '2px' }}>
                    UrbanGen AI Approach:
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text)', lineHeight: 1.45 }}>
                    {row.urbanGenDetail}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
