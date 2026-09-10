import { useState, useEffect, useCallback } from 'react';
import { Sparkles, Shuffle, Grid3X3, Download, Zap, Info } from 'lucide-react';
import { apiFetch } from '../lib/api';

// UCMerced 21 classes with human-readable labels and icons
const URBAN_CLASSES = [
  { index: 0, name: 'agricultural',       emoji: '🌾', description: 'Cultivated farmland' },
  { index: 1, name: 'airplane',           emoji: '✈️', description: 'Airport tarmac & planes' },
  { index: 2, name: 'baseballdiamond',    emoji: '⚾', description: 'Baseball fields' },
  { index: 3, name: 'beach',             emoji: '🏖️', description: 'Coastal shorelines' },
  { index: 4, name: 'buildings',         emoji: '🏢', description: 'Dense urban buildings' },
  { index: 5, name: 'chaparral',         emoji: '🌿', description: 'Scrubland vegetation' },
  { index: 6, name: 'denseresidential',  emoji: '🏘️', description: 'Dense housing areas' },
  { index: 7, name: 'forest',            emoji: '🌲', description: 'Forested land cover' },
  { index: 8, name: 'freeway',           emoji: '🛣️', description: 'Highway infrastructure' },
  { index: 9, name: 'golfcourse',        emoji: '⛳', description: 'Golf courses & greens' },
  { index: 10, name: 'harbor',           emoji: '⚓', description: 'Port & marina areas' },
  { index: 11, name: 'intersection',     emoji: '🚦', description: 'Road intersections' },
  { index: 12, name: 'mediumresidential',emoji: '🏠', description: 'Medium-density housing' },
  { index: 13, name: 'mobilehomepark',   emoji: '🚐', description: 'Mobile home communities' },
  { index: 14, name: 'overpass',         emoji: '🌉', description: 'Road overpasses & bridges' },
  { index: 15, name: 'parkinglot',       emoji: '🅿️', description: 'Surface parking lots' },
  { index: 16, name: 'river',            emoji: '🏞️', description: 'River & waterway' },
  { index: 17, name: 'runway',           emoji: '🛬', description: 'Airport runway' },
  { index: 18, name: 'sparseresidential',emoji: '🏡', description: 'Low-density housing' },
  { index: 19, name: 'storagetanks',     emoji: '🛢️', description: 'Industrial storage tanks' },
  { index: 20, name: 'tenniscourt',      emoji: '🎾', description: 'Tennis courts' },
];

interface GeneratedResult {
  grid: string;
  images: string[];
  class_index: number;
  class_name: string;
  num_generated: number;
  latent_dim: number;
  epochs_trained: number | string;
}

const styles = `
  .gan-page { display: flex; flex-direction: column; gap: 28px; }

  /* ---- header ---- */
  .gan-header { }
  .gan-title { font-size: 1.8rem; font-weight: 700; margin-bottom: 8px;
    background: linear-gradient(135deg, #00D4FF 0%, #7B61FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .gan-subtitle { color: var(--muted); font-size: 0.95rem; line-height: 1.6; max-width: 680px; }

  /* ---- class grid ---- */
  .class-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; }
  .class-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    padding: 12px 10px; cursor: pointer; transition: all 0.18s; text-align: center; user-select: none; }
  .class-card:hover { border-color: var(--accent); background: rgba(0,212,255,0.06); transform: translateY(-2px); }
  .class-card.selected { border-color: var(--accent); background: rgba(0,212,255,0.12);
    box-shadow: 0 0 0 1px var(--accent); }
  .class-emoji { font-size: 1.8rem; display: block; margin-bottom: 6px; line-height: 1; }
  .class-name { font-size: 0.75rem; font-weight: 600; text-transform: capitalize;
    color: var(--text); letter-spacing: 0.02em; }
  .class-desc { font-size: 0.68rem; color: var(--muted); margin-top: 3px; line-height: 1.3; }

  /* ---- controls bar ---- */
  .controls-bar { display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-end;
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 18px 20px; }
  .ctrl-group { display: flex; flex-direction: column; gap: 6px; }
  .ctrl-label { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
  .ctrl-select, .ctrl-input { background: var(--bg); border: 1px solid var(--border); border-radius: 5px;
    color: var(--text); padding: 7px 10px; font-size: 0.88rem; font-family: var(--font-mono);
    outline: none; transition: border-color 0.18s; }
  .ctrl-select:focus, .ctrl-input:focus { border-color: var(--accent); }
  .ctrl-input { width: 90px; }
  .ctrl-btns { display: flex; gap: 10px; margin-left: auto; align-items: flex-end; }
  .gan-btn { display: flex; align-items: center; gap: 7px; padding: 9px 20px; border-radius: 6px;
    border: none; font-family: var(--font-ui); font-size: 0.9rem; font-weight: 600;
    cursor: pointer; transition: all 0.18s; white-space: nowrap; }
  .gan-btn-primary { background: linear-gradient(135deg, #00D4FF, #7B61FF); color: #000; }
  .gan-btn-primary:hover { opacity: 0.88; transform: translateY(-1px); }
  .gan-btn-primary:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }
  .gan-btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
  .gan-btn-outline:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
  .gan-btn-outline:disabled { opacity: 0.45; cursor: not-allowed; }

  /* ---- results area ---- */
  .results-section { display: flex; flex-direction: column; gap: 20px; }
  .result-meta { display: flex; gap: 24px; flex-wrap: wrap;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px 20px; }
  .meta-item { display: flex; flex-direction: column; gap: 3px; }
  .meta-lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
  .meta-val { font-family: var(--font-mono); font-size: 1.05rem; color: var(--accent); }

  .images-carousel { display: flex; flex-direction: column; gap: 16px; }
  .carousel-track { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 6px;
    scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
  .gen-image-wrap { position: relative; flex-shrink: 0; border-radius: 8px; overflow: hidden;
    border: 1px solid var(--border); transition: transform 0.18s, box-shadow 0.18s; cursor: pointer; }
  .gen-image-wrap:hover { transform: scale(1.03); box-shadow: 0 8px 32px rgba(0,0,0,0.4); z-index: 1; }
  .gen-image { display: block; width: 180px; height: 180px; object-fit: cover; }
  .gen-image-label { position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.75));
    font-size: 0.72rem; color: rgba(255,255,255,0.85); padding: 18px 8px 6px;
    text-align: center; font-weight: 600; text-transform: capitalize; letter-spacing: 0.04em; }
  .download-overlay { position: absolute; top: 6px; right: 6px; opacity: 0; transition: opacity 0.18s; }
  .gen-image-wrap:hover .download-overlay { opacity: 1; }
  .dl-btn { background: rgba(0,0,0,0.7); border: none; border-radius: 4px; padding: 5px;
    cursor: pointer; color: #fff; display: flex; align-items: center; justify-content: center; }
  .dl-btn:hover { background: var(--accent); color: #000; }

  .grid-view-wrap { border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }
  .grid-view-img { width: 100%; height: auto; display: block; }

  /* ---- tabs ---- */
  .view-tabs { display: flex; gap: 8px; }
  .view-tab { padding: 7px 16px; border-radius: 5px; border: 1px solid var(--border);
    background: transparent; color: var(--muted); font-family: var(--font-ui);
    font-size: 0.85rem; cursor: pointer; transition: all 0.18s; display: flex; align-items: center; gap: 6px; }
  .view-tab.active { background: rgba(0,212,255,0.1); border-color: var(--accent); color: var(--accent); }
  .view-tab:hover:not(.active) { border-color: var(--muted); color: var(--text); }

  /* ---- not-trained banner ---- */
  .not-trained-banner { background: rgba(255,183,77,0.08); border: 1px solid rgba(255,183,77,0.25);
    border-radius: 8px; padding: 20px 24px; display: flex; gap: 14px; align-items: flex-start; }
  .ntb-icon { color: #FFB74D; flex-shrink: 0; margin-top: 2px; }
  .ntb-title { font-weight: 600; color: #FFB74D; margin-bottom: 6px; }
  .ntb-body { color: var(--muted); font-size: 0.88rem; line-height: 1.6; }
  .ntb-code { background: var(--bg); border: 1px solid var(--border); border-radius: 4px;
    padding: 10px 14px; font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent);
    margin-top: 10px; display: block; overflow-x: auto; white-space: pre; }

  /* ---- spinner ---- */
  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner { width: 20px; height: 20px; border: 2px solid transparent;
    border-top-color: currentColor; border-radius: 50%; animation: spin 0.7s linear infinite; }

  /* ---- progress ---- */
  .generating-overlay { display: flex; flex-direction: column; align-items: center;
    justify-content: center; gap: 16px; padding: 60px 20px;
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px; }
  .gen-text { color: var(--muted); font-size: 0.9rem; }
  @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
  .pulse-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent);
    animation: pulse 1.2s ease-in-out infinite; }
  .pulse-dots { display: flex; gap: 8px; }
  .pulse-dot:nth-child(2) { animation-delay: 0.2s; }
  .pulse-dot:nth-child(3) { animation-delay: 0.4s; }
`;

export default function GAN({ isGanTrained }: { isGanTrained?: boolean }) {
  const [selectedClass, setSelectedClass] = useState(4); // 'buildings' default
  const [numImages, setNumImages] = useState(4);
  const [seed, setSeed] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GeneratedResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'carousel' | 'grid'>('carousel');
  const [gridImg, setGridImg] = useState<string | null>(null);
  const [gridLoading, setGridLoading] = useState(false);
  const [ganTrained, setGanTrained] = useState<boolean>(isGanTrained ?? false);

  // Check status on mount
  useEffect(() => {
    apiFetch('/status')
      .then(r => r.json())
      .then(d => setGanTrained(d.gan === 'Trained'))
      .catch(() => {});
  }, []);

  const handleGenerate = useCallback(async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await apiFetch('/infer/gan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          class_index: selectedClass,
          num_images: numImages,
          seed: seed !== '' ? parseInt(seed) : null,
        }),
      });
      if (!res.ok) {
        const msg = await res.text();
        setError(msg || `Error ${res.status}`);
      } else {
        const data: GeneratedResult = await res.json();
        setResult(data);
        setViewMode('carousel');
      }
    } catch (e: any) {
      setError(e.message || 'Network error');
    } finally {
      setLoading(false);
    }
  }, [selectedClass, numImages, seed]);

  const handleRandomSeed = () => setSeed(String(Math.floor(Math.random() * 99999)));

  const handleLoadGrid = useCallback(async () => {
    setGridLoading(true);
    setGridImg(null);
    try {
      const res = await apiFetch('/infer/gan/grid');
      if (res.ok) {
        const blob = await res.blob();
        setGridImg(URL.createObjectURL(blob));
        setViewMode('grid');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setGridLoading(false);
    }
  }, []);

  const downloadImage = (b64: string, filename: string) => {
    const link = document.createElement('a');
    link.href = `data:image/jpeg;base64,${b64}`;
    link.download = filename;
    link.click();
  };

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: styles }} />
      <div className="gan-page">
        {/* Header */}
        <div className="gan-header">
          <h1 className="gan-title">GAN — Urban Tile Generator</h1>
          <p className="gan-subtitle">
            Conditional DCGAN trained on 21 UCMerced land-use categories. Select a class,
            choose how many tiles to generate, and the Generator synthesises realistic
            128×128 aerial imagery from pure Gaussian noise — no real image required.
          </p>
        </div>

        {/* Not trained banner */}
        {!ganTrained && (
          <div className="not-trained-banner">
            <Info size={20} className="ntb-icon" />
            <div>
              <div className="ntb-title">GAN not trained yet</div>
              <div className="ntb-body">
                The Generator weights have not been found. Train the model first:
                <code className="ntb-code">
                  cd backend{'\n'}
                  python train_gan.py --epochs 100 --batch-size 32
                </code>
                Training takes ~20 min on a GPU (longer on CPU). Once done,
                restart the API server and refresh this page.
              </div>
            </div>
          </div>
        )}

        {/* Class selector */}
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--muted)', textTransform: 'uppercase',
            letterSpacing: '0.07em', marginBottom: '12px' }}>
            Select Land-Use Class to Generate
          </div>
          <div className="class-grid">
            {URBAN_CLASSES.map(cls => (
              <div
                key={cls.index}
                className={`class-card ${selectedClass === cls.index ? 'selected' : ''}`}
                onClick={() => setSelectedClass(cls.index)}
                title={cls.description}
              >
                <span className="class-emoji">{cls.emoji}</span>
                <div className="class-name">{cls.name}</div>
                <div className="class-desc">{cls.description}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Controls */}
        <div className="controls-bar">
          <div className="ctrl-group">
            <span className="ctrl-label">Images to Generate</span>
            <select
              className="ctrl-select"
              value={numImages}
              onChange={e => setNumImages(parseInt(e.target.value))}
            >
              {[1, 2, 4, 6, 8, 12, 16].map(n => (
                <option key={n} value={n}>{n} image{n !== 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>

          <div className="ctrl-group">
            <span className="ctrl-label">Random Seed (optional)</span>
            <div style={{ display: 'flex', gap: '6px' }}>
              <input
                className="ctrl-input"
                type="number"
                placeholder="auto"
                value={seed}
                onChange={e => setSeed(e.target.value)}
                min={0}
                max={99999}
              />
              <button
                className="gan-btn gan-btn-outline"
                onClick={handleRandomSeed}
                title="Pick a random seed"
                style={{ padding: '7px 10px' }}
              >
                <Shuffle size={16} />
              </button>
            </div>
          </div>

          <div className="ctrl-group" style={{ flex: 1 }}>
            <span className="ctrl-label">Selected Class</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', height: '36px' }}>
              <span style={{ fontSize: '1.5rem', lineHeight: 1 }}>
                {URBAN_CLASSES[selectedClass]?.emoji}
              </span>
              <span style={{ fontWeight: 600, textTransform: 'capitalize', color: 'var(--accent)' }}>
                {URBAN_CLASSES[selectedClass]?.name}
              </span>
              <span style={{ color: 'var(--muted)', fontSize: '0.82rem' }}>
                (class #{selectedClass})
              </span>
            </div>
          </div>

          <div className="ctrl-btns">
            <button
              className="gan-btn gan-btn-outline"
              onClick={handleLoadGrid}
              disabled={!ganTrained || gridLoading}
            >
              {gridLoading ? <div className="spinner" /> : <Grid3X3 size={16} />}
              All 21 Classes
            </button>
            <button
              className="gan-btn gan-btn-primary"
              onClick={handleGenerate}
              disabled={!ganTrained || loading}
            >
              {loading ? <div className="spinner" /> : <Sparkles size={16} />}
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div style={{ background: 'rgba(255,82,82,0.08)', border: '1px solid rgba(255,82,82,0.25)',
            borderRadius: '8px', padding: '14px 18px', color: '#FF5252', fontSize: '0.9rem' }}>
            ⚠️ {error}
          </div>
        )}

        {/* Generating spinner */}
        {loading && (
          <div className="generating-overlay">
            <div className="pulse-dots">
              <div className="pulse-dot" />
              <div className="pulse-dot" />
              <div className="pulse-dot" />
            </div>
            <div className="gen-text">
              Sampling from latent space → decoding{' '}
              <strong style={{ color: 'var(--accent)' }}>
                {URBAN_CLASSES[selectedClass]?.name}
              </strong>{' '}
              tiles…
            </div>
          </div>
        )}

        {/* Results */}
        {(result || gridImg) && !loading && (
          <div className="results-section">
            {/* Meta bar */}
            {result && (
              <div className="result-meta">
                <div className="meta-item">
                  <span className="meta-lbl">Class</span>
                  <span className="meta-val">
                    {URBAN_CLASSES[result.class_index]?.emoji} {result.class_name}
                  </span>
                </div>
                <div className="meta-item">
                  <span className="meta-lbl">Generated</span>
                  <span className="meta-val">{result.num_generated} images</span>
                </div>
                <div className="meta-item">
                  <span className="meta-lbl">Latent dim z</span>
                  <span className="meta-val">{result.latent_dim}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-lbl">Epochs trained</span>
                  <span className="meta-val">{result.epochs_trained}</span>
                </div>
                {seed && (
                  <div className="meta-item">
                    <span className="meta-lbl">Seed</span>
                    <span className="meta-val">{seed}</span>
                  </div>
                )}
              </div>
            )}

            {/* View tabs */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div className="view-tabs">
                {result && (
                  <button
                    className={`view-tab ${viewMode === 'carousel' ? 'active' : ''}`}
                    onClick={() => setViewMode('carousel')}
                  >
                    <Sparkles size={14} /> Individual
                  </button>
                )}
                {result && (
                  <button
                    className={`view-tab ${viewMode === 'grid' ? 'active' : ''}`}
                    onClick={() => { setViewMode('grid'); }}
                  >
                    <Grid3X3 size={14} /> Grid View
                  </button>
                )}
                {gridImg && (
                  <button
                    className={`view-tab ${viewMode === 'grid' && !result ? 'active' : ''}`}
                    onClick={() => setViewMode('grid')}
                  >
                    <Grid3X3 size={14} /> All-Class Grid
                  </button>
                )}
              </div>

              {result && viewMode === 'carousel' && (
                <button
                  className="gan-btn gan-btn-outline"
                  style={{ padding: '6px 14px', fontSize: '0.82rem' }}
                  onClick={() => {
                    result.images.forEach((b64, i) =>
                      downloadImage(b64, `${result.class_name}_${i + 1}.jpg`)
                    );
                  }}
                >
                  <Download size={14} /> Download All
                </button>
              )}
            </div>

            {/* Carousel view */}
            {viewMode === 'carousel' && result && (
              <div className="images-carousel">
                <div className="carousel-track">
                  {result.images.map((b64, i) => (
                    <div key={i} className="gen-image-wrap">
                      <img
                        src={`data:image/jpeg;base64,${b64}`}
                        className="gen-image"
                        alt={`Generated ${result.class_name} ${i + 1}`}
                      />
                      <div className="gen-image-label">
                        {URBAN_CLASSES[result.class_index]?.emoji} {result.class_name}
                      </div>
                      <div className="download-overlay">
                        <button
                          className="dl-btn"
                          onClick={() => downloadImage(b64, `${result.class_name}_${i + 1}.jpg`)}
                          title="Download this tile"
                        >
                          <Download size={14} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', paddingLeft: '2px' }}>
                  ↔ Scroll to see all generated tiles · Hover to download individually
                </div>
              </div>
            )}

            {/* Grid view — generated batch */}
            {viewMode === 'grid' && result && (
              <div className="grid-view-wrap">
                <img
                  src={`data:image/jpeg;base64,${result.grid}`}
                  className="grid-view-img"
                  alt={`Generated ${result.class_name} grid`}
                />
              </div>
            )}

            {/* Grid view — all-class grid */}
            {gridImg && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <Zap size={13} style={{ color: 'var(--accent)' }} />
                  One generated tile per class (21 images, 7 per row) — shows class-conditioning quality
                </div>
                <div className="grid-view-wrap">
                  <img src={gridImg} className="grid-view-img" alt="All-class generation grid" />
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-start', flexWrap: 'wrap', gap: '6px' }}>
                  {URBAN_CLASSES.map(c => (
                    <span key={c.index} style={{ fontSize: '0.72rem', color: 'var(--muted)',
                      background: 'var(--surface)', border: '1px solid var(--border)',
                      borderRadius: '4px', padding: '2px 7px' }}>
                      {c.emoji} {c.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* How it works */}
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: '8px', padding: '20px 24px' }}>
          <div style={{ fontWeight: 600, marginBottom: '12px', color: 'var(--accent2)',
            display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Info size={16} /> How the GAN Works
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px',
            fontSize: '0.88rem', color: 'var(--muted)', lineHeight: 1.65 }}>
            <div>
              <strong style={{ color: 'var(--text)' }}>Generator (G)</strong><br />
              Maps a noise vector <em>z</em> ~ N(0, I) plus a class label embedding
              through 4 ConvTranspose2d upsample stages (8×8 → 128×128).
              Uses BatchNorm + ReLU with Tanh output.
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>Discriminator (D)</strong><br />
              Scores images as real or fake using 5 strided convolutions
              with Spectral Normalisation — prevents D from overpowering G
              (mode collapse). Class embedding is projected into a per-pixel channel.
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>EMA Checkpoint</strong><br />
              Inference uses an Exponential Moving Average of G weights,
              which produces smoother and more stable images than the raw
              training checkpoint (decay = 0.999).
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>Training Details</strong><br />
              Non-saturating BCE loss, label smoothing (real=0.9 / fake=0.1),
              2 D steps per G step, Adam (lr=2e-4, β₁=0.5).
              Trained on UCMerced: 21 classes × 100 images = 2,100 tiles.
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
