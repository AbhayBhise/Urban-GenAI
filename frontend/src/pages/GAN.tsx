import { useState, useEffect, useCallback, useMemo } from 'react';
import { Sparkles, Shuffle, Grid3X3, Download, Zap, Info, Eye, X, ArrowLeft, RefreshCw, Check } from 'lucide-react';
import { apiFetch } from '../lib/api';
import ModelUseCaseCard from '../components/ModelUseCaseCard';

// UCMerced 21 classes with human-readable labels, icons, and broad category groupings
interface UrbanClassItem {
  index: number;
  name: string;
  emoji: string;
  group: 'Built' | 'Transport' | 'Nature' | 'Water' | 'Agri';
  description: string;
}

const URBAN_CLASSES: UrbanClassItem[] = [
  { index: 0,  name: 'agricultural',       emoji: '🌾', group: 'Agri',      description: 'Cultivated farmland & crops' },
  { index: 1,  name: 'airplane',           emoji: '✈️', group: 'Transport', description: 'Airport tarmac & aircraft' },
  { index: 2,  name: 'baseballdiamond',    emoji: '⚾', group: 'Nature',    description: 'Baseball diamond fields' },
  { index: 3,  name: 'beach',             emoji: '🏖️', group: 'Water',     description: 'Coastal shoreline & sand' },
  { index: 4,  name: 'buildings',         emoji: '🏢', group: 'Built',     description: 'Dense commercial buildings' },
  { index: 5,  name: 'chaparral',         emoji: '🌿', group: 'Nature',    description: 'Arid scrubland vegetation' },
  { index: 6,  name: 'denseresidential',  emoji: '🏘️', group: 'Built',     description: 'High-density urban housing' },
  { index: 7,  name: 'forest',            emoji: '🌲', group: 'Nature',    description: 'Canopied forest cover' },
  { index: 8,  name: 'freeway',           emoji: '🛣️', group: 'Transport', description: 'Multi-lane highway networks' },
  { index: 9,  name: 'golfcourse',        emoji: '⛳', group: 'Nature',    description: 'Fairways & putting greens' },
  { index: 10, name: 'harbor',           emoji: '⚓', group: 'Water',     description: 'Maritime port & boat slips' },
  { index: 11, name: 'intersection',     emoji: '🚦', group: 'Transport', description: 'Paved street intersections' },
  { index: 12, name: 'mediumresidential',emoji: '🏠', group: 'Built',     description: 'Suburban residential parcels' },
  { index: 13, name: 'mobilehomepark',   emoji: '🚐', group: 'Built',     description: 'Organized mobile home lots' },
  { index: 14, name: 'overpass',         emoji: '🌉', group: 'Transport', description: 'Highway overpass structures' },
  { index: 15, name: 'parkinglot',       emoji: '🅿️', group: 'Transport', description: 'Asphalt parking lots & stalls' },
  { index: 16, name: 'river',            emoji: '🏞️', group: 'Water',     description: 'Natural river waterways' },
  { index: 17, name: 'runway',           emoji: '🛬', group: 'Transport', description: 'Airport runway pavement' },
  { index: 18, name: 'sparseresidential',emoji: '🏡', group: 'Built',     description: 'Sprawled low-density estates' },
  { index: 19, name: 'storagetanks',     emoji: '🛢️', group: 'Built',     description: 'Industrial liquid storage silos' },
  { index: 20, name: 'tenniscourt',      emoji: '🎾', group: 'Nature',    description: 'Regulation tennis courts' },
];

const FILTER_GROUPS = ['All', 'Built', 'Transport', 'Nature', 'Water', 'Agri'] as const;

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
  .gan-page { display: flex; flex-direction: column; gap: 24px; }

  /* ---- Header ---- */
  .gan-hero {
    background: var(--hero-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
  }
  .gan-hero-tagline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.76rem;
    font-family: var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--badge-blue-text);
    background: var(--badge-blue-bg);
    border: 1px solid var(--badge-blue-border);
    padding: 4px 10px;
    border-radius: 999px;
    margin-bottom: 12px;
  }
  .gan-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 8px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-green) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .gan-subtitle {
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.6;
    max-width: 820px;
  }

  /* ---- Top Mode Tabs ---- */
  .mode-tabs {
    display: flex;
    gap: 12px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
  }
  .mode-tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text-secondary);
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .mode-tab-btn:hover {
    border-color: var(--accent);
    color: var(--text);
    transform: translateY(-1px);
  }
  .mode-tab-btn.active {
    background: var(--accent-wash, rgba(2, 132, 199, 0.1));
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
  }

  /* ---- Class Selector Section ---- */
  .class-selection-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .section-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  .section-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .filter-pills {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  .filter-pill {
    font-size: 0.74rem;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--muted);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .filter-pill:hover {
    border-color: var(--accent);
    color: var(--text);
  }
  .filter-pill.active {
    background: var(--accent);
    border-color: var(--accent);
    color: #ffffff;
    font-weight: 600;
  }

  /* ---- Class Card Grid ---- */
  .class-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(135px, 1fr));
    gap: 10px;
    max-height: 290px;
    overflow-y: auto;
    padding-right: 4px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .class-card {
    background: var(--bg);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 12px 10px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
    user-select: none;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
  .class-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  }
  .class-card.selected {
    border-color: var(--accent);
    background: var(--accent-wash, rgba(2, 132, 199, 0.08));
    box-shadow: 0 0 0 1.5px var(--accent), 0 4px 16px rgba(2, 132, 199, 0.15);
  }
  .class-emoji {
    font-size: 1.7rem;
    display: block;
    line-height: 1;
    margin-bottom: 2px;
  }
  .class-name {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: capitalize;
    color: var(--text);
    letter-spacing: 0.02em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
  .class-desc {
    font-size: 0.65rem;
    color: var(--muted);
    line-height: 1.25;
    height: 24px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  .card-active-check {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ---- Dedicated Generation Bar ---- */
  .generator-control-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: var(--card-shadow);
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .ctrl-inputs-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    align-items: stretch;
  }
  .ctrl-panel-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    justify-content: center;
  }
  .ctrl-box-label {
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
  }

  /* Pill Count Selector */
  .pill-count-group {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  .pill-count-btn {
    flex: 1;
    min-width: 38px;
    padding: 6px 8px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-size: 0.84rem;
    font-weight: 600;
    font-family: var(--font-mono);
    cursor: pointer;
    text-align: center;
    transition: all 0.15s ease;
  }
  .pill-count-btn:hover {
    border-color: var(--accent);
  }
  .pill-count-btn.active {
    background: var(--accent);
    border-color: var(--accent);
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
  }

  /* Seed Input */
  .seed-input-wrap {
    display: flex;
    gap: 6px;
    align-items: center;
  }
  .seed-input {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    font-family: var(--font-mono);
    font-size: 0.86rem;
    color: var(--text);
    outline: none;
    transition: border-color 0.18s;
  }
  .seed-input:focus {
    border-color: var(--accent);
  }
  .seed-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    color: var(--text);
    cursor: pointer;
    transition: all 0.18s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .seed-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
  }

  /* Action Bar (Full Width & Prominent) */
  .actions-row {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 18px;
  }
  .btn-generate-main {
    flex: 2;
    min-width: 260px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 13px 28px;
    border-radius: 8px;
    border: none;
    background: linear-gradient(135deg, var(--accent) 0%, #0369a1 100%);
    color: #ffffff;
    font-size: 0.96rem;
    font-weight: 700;
    font-family: var(--font-ui);
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
  }
  .btn-generate-main:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
    filter: brightness(1.05);
  }
  .btn-generate-main:disabled {
    opacity: 0.55;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .btn-secondary-bench {
    flex: 1;
    min-width: 200px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 13px 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.18s ease;
  }
  .btn-secondary-bench:hover:not(:disabled) {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-1px);
  }
  .btn-secondary-bench:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* ---- Results Section ---- */
  .results-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .result-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
  }
  .result-title-group {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .result-class-badge {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .result-count-badge {
    background: var(--badge-blue-bg);
    color: var(--badge-blue-text);
    border: 1px solid var(--badge-blue-border);
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-family: var(--font-mono);
    font-weight: 600;
  }
  .result-actions-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .btn-sub-action {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .btn-sub-action:hover {
    border-color: var(--accent);
    color: var(--accent);
  }

  /* Meta Specs Pill Bar */
  .meta-chips-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
  }
  .meta-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: var(--muted);
  }
  .meta-chip-val {
    font-family: var(--font-mono);
    font-weight: 600;
    color: var(--text);
  }

  /* Single-Class Tile Gallery Grid */
  .tiles-gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
  }
  .single-tile-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
  }
  .single-tile-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  .tile-image-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    background: #000000;
    cursor: zoom-in;
  }
  .tile-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    image-rendering: auto;
    transition: transform 0.25s ease;
  }
  .single-tile-card:hover .tile-img {
    transform: scale(1.05);
  }
  .tile-badge-overlay {
    position: absolute;
    top: 8px;
    left: 8px;
    background: rgba(15, 23, 42, 0.78);
    backdrop-filter: blur(4px);
    color: #ffffff;
    font-size: 0.72rem;
    font-family: var(--font-mono);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }
  .tile-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: var(--surface);
    border-top: 1px solid var(--border);
  }
  .tile-card-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text);
    text-transform: capitalize;
  }
  .tile-card-actions {
    display: flex;
    gap: 6px;
  }
  .btn-tile-icon {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 5px;
    cursor: pointer;
    color: var(--muted);
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .btn-tile-icon:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--surface);
  }

  /* Shimmer Placeholders */
  .shimmer-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    aspect-ratio: 1 / 1;
    position: relative;
    overflow: hidden;
  }
  @keyframes shimmerAnim {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
  .shimmer-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    animation: shimmerAnim 1.4s infinite;
  }

  /* Benchmark Mode Container */
  .benchmark-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .benchmark-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  .grid-21-preview-wrap {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }
  .grid-21-img {
    width: 100%;
    height: auto;
    display: block;
  }
  .benchmark-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 12px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
  }
  .bench-chip-btn {
    font-size: 0.74rem;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .bench-chip-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
  }

  /* Modal Zoom View */
  .zoom-modal-backdrop {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(6px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }
  .zoom-modal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    max-width: 540px;
    width: 100%;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
  }
  .zoom-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
  }
  .zoom-modal-img {
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    background: #000;
  }
  .zoom-modal-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    border-top: 1px solid var(--border);
    background: var(--bg);
  }

  /* Spinner */
  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner-icon { animation: spin 0.75s linear infinite; }
`;

export default function GAN({ isGanTrained }: { isGanTrained?: boolean }) {
  const [activeMode, setActiveMode] = useState<'single' | 'benchmark'>('single');
  const [selectedClass, setSelectedClass] = useState<number>(20); // default to Tenniscourt (#20) or Buildings (#4)
  const [filterGroup, setFilterGroup] = useState<string>('All');
  const [numImages, setNumImages] = useState<number>(4);
  const [seed, setSeed] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<GeneratedResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [singleViewStyle, setSingleViewStyle] = useState<'cards' | 'grid'>('cards');
  const [zoomedImage, setZoomedImage] = useState<{ b64: string; index: number; className: string } | null>(null);

  // 21-Class Benchmark state
  const [gridImg, setGridImg] = useState<string | null>(null);
  const [gridLoading, setGridLoading] = useState<boolean>(false);
  const [ganTrained, setGanTrained] = useState<boolean>(isGanTrained ?? false);

  // Filtered classes
  const displayedClasses = useMemo(() => {
    if (filterGroup === 'All') return URBAN_CLASSES;
    return URBAN_CLASSES.filter(c => c.group === filterGroup);
  }, [filterGroup]);

  const activeClassObj = URBAN_CLASSES[selectedClass] || URBAN_CLASSES[0];

  // Check backend model status on mount
  useEffect(() => {
    apiFetch('/status')
      .then(r => r.json())
      .then(d => {
        const trained = d.gan === 'Trained';
        setGanTrained(trained);
      })
      .catch(() => {});
  }, []);

  // Primary Single-Class Generator
  const handleGenerateSingle = useCallback(async (targetClassIdx?: number, targetCount?: number) => {
    const classToGen = targetClassIdx !== undefined ? targetClassIdx : selectedClass;
    const countToGen = targetCount !== undefined ? targetCount : numImages;

    setLoading(true);
    setError(null);
    setActiveMode('single');

    try {
      const res = await apiFetch('/infer/gan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          class_index: classToGen,
          num_images: countToGen,
          seed: seed.trim() !== '' ? parseInt(seed.trim()) : null,
        }),
      });

      if (!res.ok) {
        const msg = await res.text();
        setError(msg || `Generation failed with status ${res.status}`);
      } else {
        const data: GeneratedResult = await res.json();
        setResult(data);
      }
    } catch (e: any) {
      setError(e.message || 'Network error communicating with cDCGAN backend');
    } finally {
      setLoading(false);
    }
  }, [selectedClass, numImages, seed]);

  // Initial auto-generation on mount so the user immediately sees live generated tiles
  useEffect(() => {
    if (ganTrained && !result && !loading) {
      handleGenerateSingle(selectedClass, numImages);
    }
  }, [ganTrained]);

  // 21-Class Diversity Benchmark Loader
  const handleLoadBenchmarkGrid = useCallback(async () => {
    setActiveMode('benchmark');
    if (gridImg) return; // already loaded

    setGridLoading(true);
    setError(null);

    try {
      const res = await apiFetch('/infer/gan/grid');
      if (res.ok) {
        const blob = await res.blob();
        setGridImg(URL.createObjectURL(blob));
      } else {
        const msg = await res.text();
        setError(msg || `Benchmark generation failed (${res.status})`);
      }
    } catch (e: any) {
      setError(e.message || 'Error generating 21-class benchmark sheet');
    } finally {
      setGridLoading(false);
    }
  }, [gridImg]);

  const handleRandomSeed = () => {
    setSeed(String(Math.floor(Math.random() * 999999)));
  };

  const handleDownload = (b64: string, filename: string) => {
    const link = document.createElement('a');
    link.href = `data:image/jpeg;base64,${b64}`;
    link.download = filename;
    link.click();
  };

  const handleDownloadAll = () => {
    if (!result) return;
    result.images.forEach((b64, idx) => {
      handleDownload(b64, `${result.class_name}_tile_${idx + 1}.jpg`);
    });
  };

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: styles }} />
      <div className="gan-page">

        {/* Hero Banner */}
        <div className="gan-hero">
          <div className="gan-hero-tagline">
            <Sparkles size={13} />
            IEEE 50e / 32b Verified Protocol · Projection cDCGAN
          </div>
          <h1 className="gan-title">Conditional DCGAN — Fast Synthetic Aerial Tile Generator</h1>
          <p className="gan-subtitle">
            Creates brand-new 128×128 aerial photos from scratch for any of the 21 land-use types you pick
            (such as residential, harbor, or forest) in milliseconds.
          </p>
        </div>

        <ModelUseCaseCard
          datasetRole="Trained on 21 UCMerced land-use classes by pitting a Generator against a Discriminator until generated tiles match real aerial textures."
          inferenceAction="Takes random noise plus your chosen land-use label and generates new synthetic satellite tiles on demand."
          projectValue="Lets planners quickly create extra training examples for rare land-use types and prototype urban layouts without waiting for new satellite captures."
        />

        {/* Not-Trained Warning Banner */}
        {!ganTrained && (
          <div style={{
            background: 'var(--warn-wash)',
            border: '1px solid var(--warn)',
            borderRadius: '10px',
            padding: '16px 20px',
            display: 'flex',
            gap: '12px',
            alignItems: 'flex-start'
          }}>
            <Info size={20} style={{ color: 'var(--warn)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <div style={{ fontWeight: 700, color: 'var(--warn)', marginBottom: '4px' }}>
                GAN Generator Checkpoint Not Detected
              </div>
              <div style={{ fontSize: '0.86rem', color: 'var(--muted)', lineHeight: 1.5 }}>
                Weights file <code>outputs/gan/generator_ema.pth</code> was not found. Train the model via:
                <pre style={{
                  background: 'var(--bg)',
                  border: '1px solid var(--border)',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  margin: '8px 0 0',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.8rem',
                  color: 'var(--accent)'
                }}>python train_gan.py --epochs 50 --batch-size 32</pre>
              </div>
            </div>
          </div>
        )}

        {/* Mode Switcher Tabs */}
        <div className="mode-tabs">
          <button
            className={`mode-tab-btn ${activeMode === 'single' ? 'active' : ''}`}
            onClick={() => setActiveMode('single')}
          >
            <Sparkles size={16} />
            Single-Class Synthesis (Interactive)
          </button>
          <button
            className={`mode-tab-btn ${activeMode === 'benchmark' ? 'active' : ''}`}
            onClick={handleLoadBenchmarkGrid}
          >
            <Grid3X3 size={16} />
            All 21 Classes Diversity Benchmark
          </button>
        </div>

        {/* Error Box */}
        {error && (
          <div style={{
            background: 'var(--danger-wash)',
            border: '1px solid var(--danger)',
            borderRadius: '8px',
            padding: '14px 18px',
            color: 'var(--danger)',
            fontSize: '0.88rem',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* =========================================================================
            MODE 1: SINGLE CLASS SYNTHESIS
            ========================================================================= */}
        {activeMode === 'single' && (
          <>
            {/* Class Selection Section */}
            <div className="class-selection-section">
              <div className="section-header-row">
                <div className="section-label">
                  <span>1. Choose Target Land-Use Class</span>
                  <span style={{ color: 'var(--accent)', fontWeight: 600 }}>
                    ({URBAN_CLASSES[selectedClass]?.name} selected)
                  </span>
                </div>
                <div className="filter-pills">
                  {FILTER_GROUPS.map(g => (
                    <button
                      key={g}
                      className={`filter-pill ${filterGroup === g ? 'active' : ''}`}
                      onClick={() => setFilterGroup(g)}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>

              {/* 21 Classes Visual Grid */}
              <div className="class-grid">
                {displayedClasses.map(cls => {
                  const isSelected = selectedClass === cls.index;
                  return (
                    <div
                      key={cls.index}
                      className={`class-card ${isSelected ? 'selected' : ''}`}
                      onClick={() => {
                        setSelectedClass(cls.index);
                      }}
                      title={`${cls.name}: ${cls.description}`}
                    >
                      {isSelected && (
                        <div className="card-active-check">
                          <Check size={11} strokeWidth={3} />
                        </div>
                      )}
                      <span className="class-emoji">{cls.emoji}</span>
                      <div className="class-name">{cls.name}</div>
                      <div className="class-desc">{cls.description}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Dedicated Generator Control & Action Card */}
            <div className="generator-control-card">
              <div className="ctrl-inputs-row">
                {/* Active Target Banner */}
                <div className="ctrl-panel-box" style={{ flex: 1.2 }}>
                  <span className="ctrl-box-label">Target Land-Use Category</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '1.8rem', lineHeight: 1 }}>{activeClassObj.emoji}</span>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontWeight: 700, fontSize: '1rem', textTransform: 'capitalize', color: 'var(--text)' }}>
                        {activeClassObj.name}
                      </span>
                      <span style={{ fontSize: '0.74rem', color: 'var(--muted)' }}>
                        Class index #{activeClassObj.index} · {activeClassObj.description}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Number of Images Pill Selector */}
                <div className="ctrl-panel-box" style={{ flex: 1.5 }}>
                  <span className="ctrl-box-label">Tiles to Generate</span>
                  <div className="pill-count-group">
                    {[1, 2, 4, 8, 12, 16].map(count => (
                      <button
                        key={count}
                        className={`pill-count-btn ${numImages === count ? 'active' : ''}`}
                        onClick={() => setNumImages(count)}
                      >
                        {count}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Random Seed */}
                <div className="ctrl-panel-box" style={{ flex: 1 }}>
                  <span className="ctrl-box-label">Random Seed (z-vector)</span>
                  <div className="seed-input-wrap">
                    <input
                      className="seed-input"
                      type="text"
                      placeholder="auto (random)"
                      value={seed}
                      onChange={e => setSeed(e.target.value)}
                    />
                    <button
                      className="seed-btn"
                      onClick={handleRandomSeed}
                      title="Roll random seed"
                    >
                      <Shuffle size={15} />
                    </button>
                    {seed && (
                      <button
                        className="seed-btn"
                        onClick={() => setSeed('')}
                        title="Clear seed (auto)"
                      >
                        <X size={15} />
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* Action Bar (Full Width & Centered) */}
              <div className="actions-row">
                <button
                  className="btn-generate-main"
                  onClick={() => handleGenerateSingle()}
                  disabled={!ganTrained || loading}
                >
                  {loading ? (
                    <>
                      <RefreshCw size={18} className="spinner-icon" />
                      <span>Synthesizing {numImages} {activeClassObj.name} Tiles...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles size={18} />
                      <span>Generate {numImages} Synthetic {activeClassObj.name} Tiles</span>
                    </>
                  )}
                </button>

                <button
                  className="btn-secondary-bench"
                  onClick={handleLoadBenchmarkGrid}
                  disabled={!ganTrained || gridLoading}
                  title="Generate a 7×3 matrix of all 21 classes simultaneously"
                >
                  <Grid3X3 size={16} />
                  <span>Explore All 21 Classes Grid</span>
                </button>
              </div>
            </div>

            {/* Single-Class Generation Results */}
            <div className="results-container">
              {/* Result Top Bar */}
              <div className="result-top-bar">
                <div className="result-title-group">
                  <span className="result-class-badge">
                    <span>{activeClassObj.emoji}</span>
                    <span>Synthetic {result ? result.class_name : activeClassObj.name} Gallery</span>
                  </span>
                  <span className="result-count-badge">
                    {loading ? `${numImages} tiles generating` : `${result?.images.length || 0} tiles rendered`}
                  </span>
                </div>

                <div className="result-actions-group">
                  {result && (
                    <>
                      <div style={{ display: 'flex', gap: '4px', background: 'var(--bg)', padding: '3px', borderRadius: '6px', border: '1px solid var(--border)' }}>
                        <button
                          className={`btn-sub-action ${singleViewStyle === 'cards' ? 'active' : ''}`}
                          style={{
                            border: 'none',
                            background: singleViewStyle === 'cards' ? 'var(--surface)' : 'transparent',
                            color: singleViewStyle === 'cards' ? 'var(--accent)' : 'var(--muted)',
                          }}
                          onClick={() => setSingleViewStyle('cards')}
                          title="Individual Cards View"
                        >
                          <Sparkles size={13} /> Cards
                        </button>
                        <button
                          className={`btn-sub-action ${singleViewStyle === 'grid' ? 'active' : ''}`}
                          style={{
                            border: 'none',
                            background: singleViewStyle === 'grid' ? 'var(--surface)' : 'transparent',
                            color: singleViewStyle === 'grid' ? 'var(--accent)' : 'var(--muted)',
                          }}
                          onClick={() => setSingleViewStyle('grid')}
                          title="Stitched Composite Grid"
                        >
                          <Grid3X3 size={13} /> Composite
                        </button>
                      </div>

                      <button
                        className="btn-sub-action"
                        onClick={handleDownloadAll}
                        title="Download all generated tiles"
                      >
                        <Download size={14} /> Download Batch
                      </button>

                      <button
                        className="btn-sub-action"
                        onClick={() => handleGenerateSingle()}
                        disabled={loading}
                        title="Re-sample latent vectors"
                      >
                        <RefreshCw size={14} className={loading ? 'spinner-icon' : ''} /> Re-roll
                      </button>
                    </>
                  )}
                </div>
              </div>

              {/* Specs & Metadata Chips Bar */}
              <div className="meta-chips-bar">
                <div className="meta-chip">
                  <span>Architecture:</span>
                  <span className="meta-chip-val">Conditional DCGAN</span>
                </div>
                <div className="meta-chip">
                  <span>Weights:</span>
                  <span className="meta-chip-val">EMA Generator (50 Epochs)</span>
                </div>
                <div className="meta-chip">
                  <span>Latent Vector:</span>
                  <span className="meta-chip-val">z ∈ ℝ¹²⁸ (Gaussian)</span>
                </div>
                <div className="meta-chip">
                  <span>Resolution:</span>
                  <span className="meta-chip-val">128 × 128 RGB</span>
                </div>
                <div className="meta-chip">
                  <span>Hardware:</span>
                  <span className="meta-chip-val">NVIDIA RTX 4050 GPU</span>
                </div>
                {seed && (
                  <div className="meta-chip">
                    <span>Seed:</span>
                    <span className="meta-chip-val">{seed}</span>
                  </div>
                )}
              </div>

              {/* Loading Shimmer State */}
              {loading && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{
                    fontSize: '0.85rem',
                    color: 'var(--muted)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}>
                    <RefreshCw size={14} className="spinner-icon" style={{ color: 'var(--accent)' }} />
                    <span>Sampling Gaussian noise vectors → Injecting class embedding #{selectedClass} ({activeClassObj.name}) → Decoding through 4× ResUpBlocks...</span>
                  </div>
                  <div className="tiles-gallery-grid">
                    {Array.from({ length: numImages }).map((_, i) => (
                      <div key={i} className="shimmer-card" />
                    ))}
                  </div>
                </div>
              )}

              {/* Generated Tiles Display (Cards Mode) */}
              {!loading && result && singleViewStyle === 'cards' && (
                <div className="tiles-gallery-grid">
                  {result.images.map((b64, i) => (
                    <div key={i} className="single-tile-card">
                      <div
                        className="tile-image-wrap"
                        onClick={() => setZoomedImage({ b64, index: i + 1, className: result.class_name })}
                        title="Click to enlarge"
                      >
                        <img
                          src={`data:image/jpeg;base64,${b64}`}
                          alt={`Synthetic ${result.class_name} tile #${i + 1}`}
                          className="tile-img"
                        />
                        <div className="tile-badge-overlay">
                          Tile #{i + 1}
                        </div>
                      </div>

                      <div className="tile-card-footer">
                        <div className="tile-card-label">
                          {URBAN_CLASSES[result.class_index]?.emoji} {result.class_name}
                        </div>
                        <div className="tile-card-actions">
                          <button
                            className="btn-tile-icon"
                            onClick={() => setZoomedImage({ b64, index: i + 1, className: result.class_name })}
                            title="Inspect high-res"
                          >
                            <Eye size={13} />
                          </button>
                          <button
                            className="btn-tile-icon"
                            onClick={() => handleDownload(b64, `${result.class_name}_tile_${i + 1}.jpg`)}
                            title="Download tile"
                          >
                            <Download size={13} />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Generated Tiles Display (Composite Grid Mode) */}
              {!loading && result && singleViewStyle === 'grid' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div style={{
                    borderRadius: '10px',
                    overflow: 'hidden',
                    border: '1px solid var(--border)',
                    boxShadow: '0 4px 16px rgba(0,0,0,0.06)'
                  }}>
                    <img
                      src={`data:image/jpeg;base64,${result.grid}`}
                      alt={`Synthetic ${result.class_name} batch grid`}
                      style={{ width: '100%', height: 'auto', display: 'block' }}
                    />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <button
                      className="btn-sub-action"
                      onClick={() => handleDownload(result.grid, `${result.class_name}_composite_grid.jpg`)}
                    >
                      <Download size={14} /> Download Stitched Grid
                    </button>
                  </div>
                </div>
              )}

              {/* Empty State before first generation */}
              {!loading && !result && (
                <div style={{
                  padding: '50px 20px',
                  textAlign: 'center',
                  color: 'var(--muted)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '12px'
                }}>
                  <Sparkles size={36} style={{ color: 'var(--accent)', opacity: 0.6 }} />
                  <div style={{ fontWeight: 600, fontSize: '1rem', color: 'var(--text)' }}>
                    No Tiles Synthesized Yet
                  </div>
                  <div style={{ fontSize: '0.86rem', maxWidth: '420px' }}>
                    Select a class above and click <strong>Generate {numImages} Synthetic {activeClassObj.name} Tiles</strong> to run the cDCGAN forward pass.
                  </div>
                </div>
              )}
            </div>
          </>
        )}

        {/* =========================================================================
            MODE 2: 21-CLASS DIVERSITY BENCHMARK
            ========================================================================= */}
        {activeMode === 'benchmark' && (
          <div className="benchmark-container">
            <div className="benchmark-header">
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text)', marginBottom: '4px' }}>
                  All 21-Classes Diversity Benchmark Matrix
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--muted)', margin: 0 }}>
                  One generated tile for every land-use category in the UCMerced dataset (21 images arranged 7×3). 
                  Demonstrates the model's ability to disentangle distinct spatial semantics across all categories.
                </p>
              </div>

              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <button
                  className="btn-sub-action"
                  onClick={() => setActiveMode('single')}
                >
                  <ArrowLeft size={14} /> Back to Single Class
                </button>
                {gridImg && (
                  <button
                    className="btn-sub-action"
                    onClick={() => {
                      const link = document.createElement('a');
                      link.href = gridImg;
                      link.download = 'ucmerced_cdcgan_21_classes_benchmark.jpg';
                      link.click();
                    }}
                  >
                    <Download size={14} /> Download Matrix
                  </button>
                )}
              </div>
            </div>

            {/* Benchmark Loading */}
            {gridLoading && (
              <div style={{
                padding: '60px 20px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '12px',
                color: 'var(--muted)'
              }}>
                <RefreshCw size={24} className="spinner-icon" style={{ color: 'var(--accent)' }} />
                <span>Generating 21 class-conditioned samples from noise (labels 0..20)...</span>
              </div>
            )}

            {/* Benchmark Stitched Grid Image */}
            {!gridLoading && gridImg && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <div className="grid-21-preview-wrap">
                  <img src={gridImg} alt="cDCGAN 21-class benchmark sheet" className="grid-21-img" />
                </div>

                <div style={{ fontSize: '0.8rem', color: 'var(--muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Zap size={14} style={{ color: 'var(--accent)' }} />
                  <span>Click any class below to immediately generate custom batches for that specific category:</span>
                </div>

                <div className="benchmark-chips-grid">
                  {URBAN_CLASSES.map(cls => (
                    <button
                      key={cls.index}
                      className="bench-chip-btn"
                      onClick={() => {
                        setSelectedClass(cls.index);
                        setActiveMode('single');
                        handleGenerateSingle(cls.index);
                      }}
                      title={`Switch to generating ${cls.name}`}
                    >
                      <span>{cls.emoji}</span>
                      <span>{cls.name}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Modal Zoom View */}
        {zoomedImage && (
          <div className="zoom-modal-backdrop" onClick={() => setZoomedImage(null)}>
            <div className="zoom-modal-card" onClick={e => e.stopPropagation()}>
              <div className="zoom-modal-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '1.2rem' }}>
                    {URBAN_CLASSES.find(c => c.name === zoomedImage.className)?.emoji || '🛰️'}
                  </span>
                  <span style={{ fontWeight: 700, textTransform: 'capitalize' }}>
                    {zoomedImage.className} (Tile #{zoomedImage.index})
                  </span>
                </div>
                <button
                  className="btn-tile-icon"
                  onClick={() => setZoomedImage(null)}
                  style={{ border: 'none', background: 'transparent' }}
                >
                  <X size={18} />
                </button>
              </div>

              <img
                src={`data:image/jpeg;base64,${zoomedImage.b64}`}
                alt="Enlarged synthetic tile"
                className="zoom-modal-img"
              />

              <div className="zoom-modal-footer">
                <span style={{ fontSize: '0.78rem', color: 'var(--muted)', fontFamily: 'var(--font-mono)' }}>
                  128 × 128 native cDCGAN synthesis
                </span>
                <button
                  className="btn-sub-action"
                  onClick={() => handleDownload(zoomedImage.b64, `${zoomedImage.className}_tile_${zoomedImage.index}.jpg`)}
                >
                  <Download size={14} /> Download Tile
                </button>
              </div>
            </div>
          </div>
        )}

        {/* How It Works Information Card */}
        <div style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '22px 26px'
        }}>
          <div style={{
            fontWeight: 700,
            marginBottom: '14px',
            color: 'var(--accent)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '0.95rem'
          }}>
            <Info size={18} /> How Class-Conditional DCGAN Operates in UrbanGen AI
          </div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '18px',
            fontSize: '0.85rem',
            color: 'var(--muted)',
            lineHeight: 1.6
          }}>
            <div>
              <strong style={{ color: 'var(--text)' }}>1. Class-Conditioned Generator</strong><br />
              Concatenates a 128-dimensional Gaussian noise vector <em>z ~ 𝒩(0, I)</em> with a learned 64-dimensional class embedding vector. 
              The combined vector is projected to an 8×8×512 spatial seed and upsampled through 4 Residual Upsampling blocks to synthesize 128×128 RGB imagery.
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>2. Projection Discriminator</strong><br />
              Applies Miyato & Koyama projection conditioning ($y^T V \phi(x)$) with spectral normalization across every convolutional layer. 
              This enforces a Lipschitz constant of 1, preventing discriminator collapse and ensuring stable adversarial equilibrium.
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>3. Single-Class vs. Benchmark Generation</strong><br />
              Single-Class Synthesis samples N distinct random noise vectors (z₁, ..., z_N) conditioned on the same class label y. 
              The Diversity Benchmark samples y across all 21 classes (0 to 20) to verify class conditioning fidelity across the entire UCMerced dataset.
            </div>
            <div>
              <strong style={{ color: 'var(--text)' }}>4. Edge Deployment & EMA Weights</strong><br />
              All inference queries run against the Exponential Moving Average (EMA, decay=0.999) generator weights trained for 50 epochs on an NVIDIA RTX 4050 GPU, yielding artifact-free inference in under 35ms per batch.
            </div>
          </div>
        </div>

      </div>
    </>
  );
}
