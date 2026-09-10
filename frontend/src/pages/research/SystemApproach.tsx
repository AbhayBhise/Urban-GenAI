import { useState } from 'react';
import { Layers, ArrowRight } from 'lucide-react';

export default function SystemApproach() {
  const [activeModelTab, setActiveModelTab] = useState<'ae' | 'vae' | 'gpt' | 'gan' | 'diffusion'>('ae');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Overview Banner */}
      <div className="card">
        <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={20} color="var(--accent)" />
          Geospatial Dataset Architecture &amp; The Multi-Model Generative Stack
        </div>
        <p style={{ color: 'var(--text)', fontSize: '0.92rem', lineHeight: 1.65 }}>
          Urban environments are complex socio-ecological systems. They cannot be characterized through a single data modality. UrbanGen AI builds a multi-tier pipeline designed specifically for an <strong>Urban Planner&apos;s decision workflow</strong>: first aligning diverse spatial datasets into a unified <strong>City Stack</strong>, compressing spatial features with a <strong>Denoising Autoencoder</strong>, exploring morphological variations with a <strong>Spatial VAE</strong>, and generating explainable policy drafts via a <strong>Planner Transformer (MiniGPT)</strong>.
        </p>
      </div>

      {/* Dataset Architecture: Why These Datasets? */}
      <div className="card">
        <div className="card-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Dataset Architecture: The 5-Source City Stack Concept</span>
          <span style={{ fontSize: '0.75rem', background: 'var(--accent-wash)', color: 'var(--accent)', padding: '3px 8px', borderRadius: '4px' }}>
            Spatial Alignment Pipeline
          </span>
        </div>
        <p style={{ color: 'var(--muted)', fontSize: '0.88rem', marginBottom: '20px' }}>
          Real urban planning requires harmonizing heterogeneous spatial resolutions, coordinate reference systems (CRS), and data formats into a standardized tensor representation:
        </p>

        {/* Visual City Stack Alignment Flow */}
        <div
          style={{
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: '8px',
            padding: '24px',
            marginBottom: '24px',
          }}
        >
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '14px', marginBottom: '18px' }}>
            {[
              { source: 'NASA HLS S30', role: 'Multispectral Imagery', resolution: '30m Resolution', channels: 'Spectral bands (NIR, Red, Green, SWIR)', status: 'Planned Ingestion' },
              { source: 'ESA WorldCover', role: 'Land-Cover Semantics', resolution: '10m Resolution', channels: 'Discrete classes (Tree, Built, Water, Grass)', status: 'Planned Ingestion' },
              { source: 'OpenStreetMap', role: 'Infrastructure Vectors', resolution: 'Vector Topology', channels: 'Roads, building footprints, waterways, POIs', status: 'Active (Pune Shapefiles)' },
              { source: 'NASA SRTM DEM', role: 'Topography & Slopes', resolution: '30m Resolution', channels: 'Elevation, slope, drainage watersheds', status: 'Planned Ingestion' },
              { source: 'WorldPop', role: 'Human Density Grids', resolution: '100m Resolution', channels: 'Population density counts per cell', status: 'Planned Ingestion' },
            ].map((d, i) => (
              <div
                key={i}
                style={{
                  background: 'var(--surface)',
                  border: '1px solid var(--border)',
                  borderRadius: '6px',
                  padding: '12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px',
                }}
              >
                <div style={{ color: 'var(--accent)', fontWeight: 600, fontSize: '0.85rem' }}>{d.source}</div>
                <div style={{ color: 'var(--text)', fontSize: '0.8rem', fontWeight: 500 }}>{d.role}</div>
                <div style={{ color: 'var(--muted)', fontSize: '0.74rem' }}>{d.resolution}</div>
                <div style={{ color: 'var(--muted)', fontSize: '0.72rem', marginTop: '4px', lineHeight: 1.3 }}>{d.channels}</div>
                <div style={{ marginTop: 'auto', paddingTop: '8px' }}>
                  <span style={{ fontSize: '0.7rem', color: d.status.includes('Active') ? 'var(--success)' : 'var(--warn)' }}>
                    ● {d.status}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Alignment Stage Diagram */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', padding: '12px 0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent)', fontSize: '0.82rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              <ArrowRight size={16} style={{ transform: 'rotate(90deg)' }} /> Spatial Resampling, CRS Reprojection (EPSG:3857/32643) &amp; Grid Alignment <ArrowRight size={16} style={{ transform: 'rotate(90deg)' }} />
            </div>
            <div
              style={{
                background: 'linear-gradient(90deg, var(--accent-wash) 0%, var(--accent2-wash) 100%)',
                border: '1px solid var(--accent)',
                borderRadius: '6px',
                padding: '12px 30px',
                textAlign: 'center',
                width: '100%',
                maxWidth: '680px',
              }}
            >
              <div style={{ color: 'var(--text)', fontWeight: 700, fontSize: '0.95rem', letterSpacing: '0.04em' }}>
                PUNE CITY STACK (Unified Multi-Channel Tensor: H × W × C)
              </div>
              <div style={{ color: 'var(--muted)', fontSize: '0.78rem', marginTop: '4px' }}>
                Decomposed into standardized patches (128×128 / 224×224) for Neural Network representation
              </div>
            </div>
          </div>
        </div>

        {/* Current Active Repositories & Training Datasets */}
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--accent2)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
            Active Datasets Currently Powering Committed Checkpoints:
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text)' }}>
              <strong>1. UCMerced LandUse (21 classes, 2,100 tiles)</strong>: Used to train the Denoising Autoencoder (50 epochs), Spatial VAE (50 epochs), and Land-Use Classifier (30 epochs, 98.1% val accuracy).
            </div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text)' }}>
              <strong>2. EuroSAT Sentinel-2 (10 classes)</strong>: Supported in the dataset pipeline (<code style={{ color: 'var(--accent)' }}>backend/dataset.py</code>) for multi-spectral land cover benchmarking.
            </div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text)' }}>
              <strong>3. Pune PMC GIS Shapefiles</strong>: GeoPandas ingestion (<code style={{ color: 'var(--accent)' }}>backend/rag_pipeline.py</code>) parsing buildings, roads, waterways, land-use, and natural green zones to seed planner prompts.
            </div>
          </div>
        </div>
      </div>

      {/* Model Contribution: Why Multiple Generative Models? */}
      <div className="card">
        <div className="card-title">
          Model Contribution: Why Multiple Generative Models?
        </div>
        <p style={{ color: 'var(--muted)', fontSize: '0.88rem', marginBottom: '18px' }}>
          In a comprehensive Urban Digital Twin, no single architecture satisfies all computational needs. UrbanGen AI employs a specialized multi-model stack:
        </p>

        {/* Model Tabs */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--border)', paddingBottom: '12px', marginBottom: '18px', flexWrap: 'wrap' }}>
          {[
            { id: 'ae', label: 'Autoencoder (AE)', badge: 'Implemented ✓', color: 'var(--success)' },
            { id: 'vae', label: 'Spatial VAE', badge: 'Implemented ✓', color: 'var(--success)' },
            { id: 'gpt', label: 'Transformer (MiniGPT)', badge: 'Implemented ✓', color: 'var(--success)' },
            { id: 'gan', label: 'Spectral GAN', badge: 'In Development ◐', color: 'var(--warn)' },
            { id: 'diffusion', label: 'Diffusion Model', badge: 'Planned ○', color: 'var(--muted)' },
          ].map(m => (
            <button
              key={m.id}
              onClick={() => setActiveModelTab(m.id as any)}
              style={{
                background: activeModelTab === m.id ? 'var(--accent-wash)' : 'transparent',
                color: activeModelTab === m.id ? 'var(--accent)' : 'var(--text)',
                border: `1px solid ${activeModelTab === m.id ? 'var(--accent)' : 'var(--border)'}`,
                borderRadius: '6px',
                padding: '8px 14px',
                fontSize: '0.82rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                cursor: 'pointer',
              }}
            >
              <span>{m.label}</span>
              <span style={{ fontSize: '0.7rem', color: m.color }}>{m.badge}</span>
            </button>
          ))}
        </div>

        {/* Tab Detail Panels */}
        {activeModelTab === 'ae' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Role in Urban Planning</div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Representation Learning &amp; Pre-cleaning Denoising:</strong> Satellite and aerial imagery regularly suffers from atmospheric haze, sensor noise, and cloud shadows. The Denoising AE compresses high-resolution tiles to learn invariant spatial features and reconstruct clean ground surfaces before downstream zoning analysis.
                </div>
              </div>

              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Architecture &amp; Bottleneck</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Encoder:</strong> Pretrained ResNet18 backbone (conv1 through layer3), downsampling 16× into an <code style={{ color: 'var(--accent)' }}>8×8×256</code> feature bottleneck (16,384 dims).<br />
                  <strong>Decoder:</strong> 4-stage transposed convolutions (stride 2) restoring original 128×128 dimensions.
                </div>
              </div>
            </div>

            {/* AE Flow Diagram */}
            <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Execution Pipeline (Verified Checkpoint: outputs/ae/model.pth)
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', flexWrap: 'wrap', fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--text)' }}>
                <span style={{ padding: '6px 12px', background: 'var(--surface-inset)', borderRadius: '4px' }}>Noisy Urban Tile (128×128×3)</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--accent-wash)', border: '1px solid var(--accent)', borderRadius: '4px', color: 'var(--accent)' }}>ResNet18 Encoder</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--accent2-wash)', border: '1px solid var(--accent2)', borderRadius: '4px', color: 'var(--accent2)' }}>Latent Codes (8×8×256)</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--success-wash)', border: '1px solid var(--success)', borderRadius: '4px', color: 'var(--success)' }}>Transposed-Conv Decoder</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--surface-inset)', borderRadius: '4px' }}>Denoised Tile (128×128×3)</span>
              </div>
              <div style={{ marginTop: '12px', fontSize: '0.8rem', color: 'var(--muted)' }}>
                Verified Experiment: 50 epochs on UCMerced | Initial Loss: 0.1830 → Final Train MSE: 0.01977 | PSNR calculated per request.
              </div>
            </div>
          </div>
        )}

        {activeModelTab === 'vae' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Role in Urban Planning</div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Probabilistic Scenario Generation &amp; Anomaly Auditing:</strong> Enables planners to smoothly interpolate between diverse land uses (e.g. dense residential ↔ green parkland) along a continuous spatial latent manifold. It also scores reconstruction error against an empirical baseline of 300 real tiles to identify anomalous, unplanned developments.
                </div>
              </div>

              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Architecture &amp; Loss Objective</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Latent Structure:</strong> Spatial <code style={{ color: 'var(--accent)' }}>64×8×8 = 4,096</code> dimensions preserving road grids and parcel edges.<br />
                  <strong>Objective:</strong> <code style={{ color: 'var(--accent2)' }}>0.7·L1 + 0.3·MSE + β·KL</code> with <code style={{ color: 'var(--accent)' }}>β = 1e-4</code> (deliberate reconstruction-priority trade-off documented in Model Card).
                </div>
              </div>
            </div>

            {/* VAE Flow Diagram */}
            <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Probabilistic Pipeline (Verified Checkpoint: outputs/vae/model.pth)
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', flexWrap: 'wrap', fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--text)' }}>
                <span style={{ padding: '6px 12px', background: 'var(--surface-inset)', borderRadius: '4px' }}>Input Tile (x)</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--accent-wash)', border: '1px solid var(--accent)', borderRadius: '4px', color: 'var(--accent)' }}>Encoder → μ, log(σ²)</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--accent2-wash)', border: '1px solid var(--accent2)', borderRadius: '4px', color: 'var(--accent2)' }}>z = μ + σ·ε (Reparameterize)</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--success-wash)', border: '1px solid var(--success)', borderRadius: '4px', color: 'var(--success)' }}>Spatial Decoder</span>
                <ArrowRight size={14} color="var(--accent)" />
                <span style={{ padding: '6px 12px', background: 'var(--surface-inset)', borderRadius: '4px' }}>Reconstruction &amp; Interpolation</span>
              </div>
              <div style={{ marginTop: '12px', fontSize: '0.8rem', color: 'var(--muted)' }}>
                Verified Experiment: 50 epochs | Train Recon Loss: 0.07524 | KL Divergence: 103.25 nats | Deterministic posterior mean used for inference.
              </div>
            </div>
          </div>
        )}

        {activeModelTab === 'gpt' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Role in Urban Planning</div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Advisory Planning Policy Drafting:</strong> Translates quantitative ward-level GIS metrics into structured, human-readable urban planning proposals for municipal review, covering permeable ground standards, setback mandates, and transit-oriented development (TOD).
                </div>
              </div>

              <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', textTransform: 'uppercase', marginBottom: '6px' }}>Architecture &amp; Corpus Grounding</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text)', lineHeight: 1.5 }}>
                  <strong>Model:</strong> From-scratch 4-layer Decoder-only Transformer (<code style={{ color: 'var(--accent)' }}>n_embd=256, 4 heads, block_size=192</code>).<br />
                  <strong>Training:</strong> 3,000 steps on <code style={{ color: 'var(--accent2)' }}>backend/corpus/urban_planning.txt</code> (zoning, green cover, TOD, Pune riverfront context).
                </div>
              </div>
            </div>

            <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>
                Seeded dynamically from real Pune ward statistics (<code style={{ color: 'var(--accent)' }}>PUNE_STATS</code>): dominant land-use, road length, waterways, and natural areas.
              </div>
            </div>
          </div>
        )}

        {activeModelTab === 'gan' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ background: 'var(--warn-wash)', border: '1px solid var(--warn)', borderRadius: '6px', padding: '16px' }}>
              <div style={{ color: 'var(--warn)', fontWeight: 600, fontSize: '0.9rem', marginBottom: '4px' }}>
                Status: In Development (Code Complete, Training Standby)
              </div>
              <p style={{ color: 'var(--text)', fontSize: '0.85rem', lineHeight: 1.55 }}>
                Implemented in <code style={{ color: 'var(--accent)' }}>backend/models/gan.py</code> and <code style={{ color: 'var(--accent)' }}>backend/train_gan.py</code>. Uses a class-conditional generator with spectral normalization, projection discriminator, and Exponential Moving Average (EMA) smoothing for 21 urban land-use classes. Pretrained weights are intentionally not yet committed to avoid distributing unverified checkpoints.
              </p>
            </div>
          </div>
        )}

        {activeModelTab === 'diffusion' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '6px', padding: '16px' }}>
              <div style={{ color: 'var(--muted)', fontWeight: 600, fontSize: '0.9rem', marginBottom: '4px' }}>
                Status: Planned Roadmap (Phase 14)
              </div>
              <p style={{ color: 'var(--text)', fontSize: '0.85rem', lineHeight: 1.55 }}>
                Planned for high-fidelity photorealistic future-city digital twin visualization, rendering text- and mask-guided satellite representations of planned zoning modifications.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Literature Finding -> Design Decision Matrix */}
      <div className="card">
        <div className="card-title">
          Literature Findings → Design Decisions → Code Implementation
        </div>
        <p style={{ color: 'var(--muted)', fontSize: '0.88rem', marginBottom: '18px' }}>
          How specific findings from the literature survey directly governed our architectural choices:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
          {[
            {
              finding: 'Urban planning requires heterogeneous spatial information (spectral, semantic, infrastructural).',
              decision: 'Design a unified multi-source City Stack rather than single-sensor models.',
              implementation: 'Spatially aligned HLS S30 + WorldCover + OSM + DEM + WorldPop pipeline.',
            },
            {
              finding: 'Generative design must support exploration of multiple scenario alternatives, not single rigid outputs.',
              decision: 'Utilize a continuous probabilistic latent space rather than deterministic regression.',
              implementation: 'Spatial VAE (64×8×8 bottleneck) enabling continuous tile interpolation.',
            },
            {
              finding: 'High-dimensional satellite inputs produce severe blurry reconstructions under standard flat latent VAEs.',
              decision: 'Retain spatial feature dimensions in latent bottleneck and apply reconstruction-priority β trade-off.',
              implementation: '8×8 spatial latent codes and β = 1e-4 target in train_vae.py.',
            },
            {
              finding: 'GenAI planning tools must augment planners with explainable, responsible, human-in-the-loop decision support.',
              decision: 'Ground language models in empirical municipal GIS statistics to eliminate hallucination.',
              implementation: 'MiniGPT seeded with real Pune ward land-use & road statistics in backend/api.py.',
            },
          ].map((item, i) => (
            <div
              key={i}
              style={{
                background: 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px',
              }}
            >
              <div>
                <span style={{ fontSize: '0.72rem', color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>Literature Finding</span>
                <p style={{ color: 'var(--text)', fontSize: '0.84rem', marginTop: '2px', lineHeight: 1.4 }}>{item.finding}</p>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', color: 'var(--accent2)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>Design Decision</span>
                <p style={{ color: 'var(--text)', fontSize: '0.84rem', marginTop: '2px', lineHeight: 1.4 }}>{item.decision}</p>
              </div>

              <div style={{ marginTop: 'auto', paddingTop: '8px', borderTop: '1px solid var(--border)' }}>
                <span style={{ fontSize: '0.72rem', color: 'var(--success)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>Implementation</span>
                <p style={{ color: 'var(--muted)', fontSize: '0.8rem', marginTop: '2px', lineHeight: 1.35 }}>{item.implementation}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
