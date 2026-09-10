import { Rocket, Database, Cpu, Activity, Layers, Globe } from 'lucide-react';

// Future Scope — the committed roadmap beyond the four working models.
// Content is drawn from README.md phases, docs/MODEL_CARD.md, and the
// "Planned" rows already shown in Research → Capability Matrix.

type Item = { title: string; detail: string; horizon: 'Near-term' | 'Mid-term' | 'Long-term' };

const TRACKS: { name: string; icon: typeof Rocket; items: Item[] }[] = [
  {
    name: 'Data — the full 5-source City Stack',
    icon: Database,
    items: [
      { title: 'NASA HLS S30 multispectral ingestion', detail: '30 m harmonised Landsat/Sentinel-2 surface reflectance (NIR, Red, Green, SWIR) for vegetation and impervious-surface indices.', horizon: 'Near-term' },
      { title: 'ESA WorldCover land-cover pipeline', detail: '10 m categorical raster (tree, built, water, grass) aligned into the tensor instead of used in isolation.', horizon: 'Near-term' },
      { title: 'NASA SRTM 30 m DEM alignment', detail: 'Terrain, slope and drainage for watershed and flood-vulnerability analysis (Mula-Mutha).', horizon: 'Mid-term' },
      { title: 'WorldPop 100 m density grids', detail: 'Per-capita infrastructure audits — water, transit, green space per resident.', horizon: 'Mid-term' },
    ],
  },
  {
    name: 'Pipeline — unified spatial representation',
    icon: Layers,
    items: [
      { title: 'Automated multi-raster resampler', detail: 'CRS normalisation (EPSG:3857 / 32643) and grid alignment across all five resolutions — currently partial in rag_pipeline.py.', horizon: 'Near-term' },
      { title: 'City Stack tensor construction', detail: 'Rasterise vectors and stack all sources into one H×W×C array (README phases 1–8).', horizon: 'Near-term' },
      { title: 'Multi-channel patch extraction', detail: 'Sliding-window patches across the aligned stack with train/val/test splits.', horizon: 'Mid-term' },
    ],
  },
  {
    name: 'Models — generation & simulation',
    icon: Cpu,
    items: [
      { title: 'GAN geometry maturation', detail: 'More epochs + augmented data to lift the classifier-recognition rate on grid-geometry classes (freeway, intersection, dense-residential) beyond the current ~15%.', horizon: 'Near-term' },
      { title: 'Latent Diffusion Model (LDM)', detail: 'Photorealistic satellite renderings of future zoning scenarios — replaces the schematic VAE/GAN preview with high-resolution imagery.', horizon: 'Long-term' },
      { title: 'Surrogate impact networks', detail: 'Fast neural approximations of Traffic (MATSim), Air Quality, Flood risk (SWMM), Energy and Water demand for multi-criteria scenario scoring.', horizon: 'Long-term' },
    ],
  },
  {
    name: 'Evaluation & governance',
    icon: Activity,
    items: [
      { title: 'Multi-criteria sustainability scoring', detail: 'Combine anomaly z-score, zoning compliance, green-cover %, and flood exposure into a single planner-facing scenario score.', horizon: 'Mid-term' },
      { title: 'Statutory compliance checks', detail: 'Automated validation of generated scenarios against Pune DCPR 2017/2021 development-control rules.', horizon: 'Long-term' },
    ],
  },
  {
    name: 'Product — the digital twin cockpit',
    icon: Globe,
    items: [
      { title: 'Integrated Urban Digital Twin Cockpit', detail: 'One workspace uniting live sensor streams, generative alternatives, and municipal policy checks with human-in-the-loop controls.', horizon: 'Long-term' },
      { title: 'Real-time multi-agent twin', detail: 'Continuous ingestion + agent-based negotiation between planning objectives (housing, mobility, ecology).', horizon: 'Long-term' },
    ],
  },
];

const HORIZON_COLOR: Record<Item['horizon'], string> = {
  'Near-term': 'var(--success)',
  'Mid-term': 'var(--warn)',
  'Long-term': 'var(--muted)',
};

export default function FutureScope() {
  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Future Scope</h1>
        <div className="panel-desc">
          The four generative models in this build are the working core of a larger roadmap.
          Below is what is designed and scoped but not yet trained — grouped by track, each item
          tagged by time horizon. Nothing here is claimed as done.
        </div>
      </div>

      <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', marginBottom: 24 }}>
        {(['Near-term', 'Mid-term', 'Long-term'] as const).map(h => (
          <div key={h} style={{ display: 'flex', alignItems: 'center', gap: 7, fontSize: '0.82rem', color: 'var(--muted)' }}>
            <span style={{ width: 10, height: 10, borderRadius: 3, background: HORIZON_COLOR[h], display: 'inline-block' }} />
            {h}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        {TRACKS.map(track => {
          const Icon = track.icon;
          return (
            <div key={track.name} className="card">
              <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 10, justifyContent: 'flex-start' }}>
                <Icon size={18} color="var(--accent)" />
                {track.name}
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 12 }}>
                {track.items.map(it => (
                  <div key={it.title} style={{
                    background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6,
                    padding: '12px 14px', borderLeft: `3px solid ${HORIZON_COLOR[it.horizon]}`,
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 8, marginBottom: 4 }}>
                      <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text)' }}>{it.title}</span>
                      <span style={{ fontSize: '0.68rem', color: HORIZON_COLOR[it.horizon], fontFamily: 'var(--font-mono)', whiteSpace: 'nowrap' }}>{it.horizon}</span>
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--muted)', lineHeight: 1.5 }}>{it.detail}</div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div className="card" style={{ marginTop: 20, borderLeft: '4px solid var(--accent)' }}>
        <div className="card-title" style={{ justifyContent: 'flex-start', gap: 10 }}>
          <Rocket size={18} color="var(--accent)" /> What stays true across the roadmap
        </div>
        <ul style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.86rem', color: 'var(--text)', lineHeight: 1.5 }}>
          <li>Every model is trained and verified against a committed checkpoint before it is claimed.</li>
          <li>Outputs remain decision-support candidates — validated against statutory regulations, engineering and hydrology models, and public hearings before any real-world use.</li>
          <li>The planner stays in the loop; the system explores and explains alternatives, it does not enforce a master plan.</li>
        </ul>
      </div>
    </div>
  );
}
