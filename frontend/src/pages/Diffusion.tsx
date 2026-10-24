import { useEffect, useMemo, useState } from 'react';
import { AlertCircle, CheckCircle2, Image as ImageIcon, Upload } from 'lucide-react';
import { apiFetch } from '../lib/api';
import DiffusionArchitecture from './DiffusionArchitecture';

const CLASSES = [
  'agricultural', 'airplane', 'baseballdiamond', 'beach', 'buildings',
  'chaparral', 'denseresidential', 'forest', 'freeway', 'golfcourse',
  'harbor', 'intersection', 'mediumresidential', 'mobilehomepark', 'overpass',
  'parkinglot', 'river', 'runway', 'sparseresidential', 'storagetanks', 'tenniscourt',
];

type DiffusionMetrics = {
  status: 'trained' | 'unavailable' | string;
  model: string;
  dataset: string;
  timesteps: number;
  sampling_steps: number;
  final_loss: number | null;
  best_loss: number | null;
  epochs: number;
  architecture: string;
  parameters_millions: number;
};

type DiffusionResult = {
  image: string;
  class_name: string;
  verified_class_name: string;
  verified_class_confidence: number;
  conditioning_mode?: string;
  dataset_novelty?: {
    reference_count: number;
    nearest_tile_mse_32x32: number;
    is_exact_or_near_duplicate: boolean;
  } | null;
  target_class_confidence?: number;
  candidates_evaluated?: number;
  selected_seed?: number;
  selection_method?: string;
};

export default function Diffusion() {
  const [metrics, setMetrics] = useState<DiffusionMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [className, setClassName] = useState('buildings');
  const [steps, setSteps] = useState(40);
  const [eta, setEta] = useState(0);
  const [result, setResult] = useState<DiffusionResult | null>(null);
  const [generating, setGenerating] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch('/evaluate/diffusion')
      .then(async response => {
        if (!response.ok) throw new Error(await response.text());
        setMetrics(await response.json());
      })
      .catch(err => setError(String(err)));
  }, []);

  const statusText = metrics?.status === 'trained' ? 'Checkpoint ready' : 'GPU training required';
  const previewLabel = useMemo(() => file?.name ?? 'Choose a source tile', [file]);

  const selectFile = (next: File | null) => {
    setFile(next);
    setResult(null);
    setGenerationError(null);
    const isTiff = next?.name.toLowerCase().endsWith('.tif') || next?.name.toLowerCase().endsWith('.tiff');
    if (next && next.type.startsWith('image/') && !isTiff) setPreview(URL.createObjectURL(next));
    else setPreview(null);
  };

  const generate = async () => {
    if (!file || metrics?.status !== 'trained') return;
    setGenerating(true);
    setGenerationError(null);
    setResult(null);
    try {
      const body = new FormData();
      body.append('file', file);
      body.append('class_name', className);
      body.append('steps', String(steps));
      body.append('eta', String(eta));
      const response = await apiFetch('/infer/diffusion', { method: 'POST', body });
      if (!response.ok) throw new Error(await response.text());
      const result = await response.json();
      setResult(result);
    } catch (err) {
      setGenerationError(String(err));
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Urban Scenario Diffusion</h1>
        <div className="panel-desc">
          Generate a new target-class aerial tile using the trained class-conditional DDPM and fast
          DDIM sampler. The uploaded file is retained for the existing upload workflow, but is not
          passed to the generator or blended into the result.
        </div>
      </div>

      {error && <div className="card" style={{ borderColor: 'var(--danger)', color: 'var(--danger)', marginBottom: 20 }}>{error}</div>}

      <div className="metrics-strip">
        <div className="metric"><span className="metric-label">Model status</span><span className="metric-value" style={{ color: metrics?.status === 'trained' ? 'var(--success)' : 'var(--warn)' }}>{statusText}</span></div>
        <div className="metric"><span className="metric-label">Training loss</span><span className="metric-value">{metrics?.final_loss == null ? '—' : metrics.final_loss.toFixed(5)}</span></div>
        <div className="metric"><span className="metric-label">Sampler</span><span className="metric-value">{metrics ? `${metrics.sampling_steps} DDIM steps` : '—'}</span></div>
        <div className="metric"><span className="metric-label">Parameters</span><span className="metric-value">{metrics ? `${metrics.parameters_millions}M` : '—'}</span></div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">1. Upload a tile to enable generation</div>
          <label className="upload-zone" style={{ display: 'block' }}>
            <Upload className="upload-icon" />
            <p style={{ color: 'var(--text)' }}>{previewLabel}</p>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', marginTop: 10 }}>PNG, JPG, JPEG, or TIFF · currently used only to validate the request</p>
            <input type="file" accept="image/*,.tif,.tiff" hidden onChange={e => selectFile(e.target.files?.[0] ?? null)} />
          </label>
          {preview ? <img src={preview} alt="Selected source tile" className="image-preview" style={{ marginTop: 15 }} /> : file && <div className="image-preview" style={{ marginTop: 15, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontSize: '0.85rem', textAlign: 'center', padding: 16 }}>TIFF selected<br />Preview unavailable in browser<br /><strong style={{ color: 'var(--text)', marginTop: 6 }}>{file.name}</strong></div>}
        </div>

        <div className="card">
          <div className="card-title">2. Set scenario condition</div>
          <label style={{ display: 'block', color: 'var(--muted)', fontSize: '0.82rem', marginBottom: 7 }} htmlFor="diffusion-class">Target land-use class</label>
          <select id="diffusion-class" value={className} onChange={e => setClassName(e.target.value)} style={{ width: '100%', padding: 11, background: 'var(--surface)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 5 }}>
            {CLASSES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <label style={{ display: 'block', color: 'var(--muted)', fontSize: '0.82rem', marginTop: 18 }} htmlFor="diffusion-steps">DDIM sampling steps: <strong style={{ color: 'var(--text)' }}>{steps}</strong></label>
          <input id="diffusion-steps" type="range" min={5} max={50} value={steps} onChange={e => setSteps(Number(e.target.value))} style={{ width: '100%', accentColor: 'var(--accent)' }} />
          <label style={{ display: 'block', color: 'var(--muted)', fontSize: '0.82rem', marginTop: 18 }} htmlFor="diffusion-eta">Stochasticity (η): <strong style={{ color: 'var(--text)' }}>{eta.toFixed(2)}</strong></label>
          <input id="diffusion-eta" type="range" min={0} max={1} step={0.05} value={eta} onChange={e => setEta(Number(e.target.value))} style={{ width: '100%', accentColor: 'var(--accent)' }} />
          <button className="btn" onClick={generate} disabled={!file || generating || metrics?.status !== 'trained'}>
            {generating ? 'Sampling diffusion process…' : metrics?.status === 'trained' ? 'Generate scenario tile' : 'Training required before generation'}
          </button>
        </div>
      </div>

      {metrics?.status !== 'trained' && (
        <div className="card" style={{ borderColor: 'var(--warn)', background: 'var(--warn-wash)', marginBottom: 24 }}>
          <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
            <AlertCircle size={20} style={{ color: 'var(--warn)', flexShrink: 0 }} />
            <div>
              <strong>Diffusion checkpoint unavailable.</strong>
              <p style={{ color: 'var(--muted)', lineHeight: 1.55, marginTop: 7 }}>
                The page is connected to the real inference endpoint, but generation is disabled until the class-conditional diffusion model is trained on the GPU. No placeholder image is shown.
              </p>
              <code style={{ display: 'block', marginTop: 10, color: 'var(--text)' }}>python backend/train_diffusion.py</code>
              <p style={{ color: 'var(--muted)', fontSize: '0.8rem', marginTop: 6 }}>The training script selects CUDA automatically when it is available.</p>
            </div>
          </div>
        </div>
      )}

      {generationError && <div className="card" style={{ borderColor: 'var(--danger)', color: 'var(--danger)', marginBottom: 20 }}>{generationError}</div>}

      {result && (
        <div className="card">
          <div className="card-title"><span>Generated class-conditional tile</span><span style={{ color: 'var(--success)', fontSize: '0.78rem' }}><CheckCircle2 size={15} style={{ verticalAlign: 'middle', marginRight: 5 }} />real model output</span></div>
          <div className="grid-2" style={{ marginBottom: 0 }}>
            <div>
              <img src={result.image} alt={`Generated ${className} tile`} className="image-preview" />
              <div style={{ marginTop: 10, padding: 10, borderRadius: 6, background: 'var(--warn-wash)', color: 'var(--muted)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong style={{ color: 'var(--warn)' }}>Visual-quality notice:</strong> This is a research checkpoint output. The classifier can recognize the requested class even when the tile is blurry or noisy; classifier confidence is not a visual-quality or planning-validity score.
              </div>
            </div>
            <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              <p><strong style={{ color: 'var(--text)' }}>Requested class:</strong> {className}</p>
              <p><strong style={{ color: 'var(--text)' }}>Classifier result:</strong> {result.verified_class_name} ({(result.verified_class_confidence * 100).toFixed(1)}%)</p>
              {result.target_class_confidence != null && (
                <p><strong style={{ color: 'var(--text)' }}>Classifier probability for request:</strong> {(result.target_class_confidence * 100).toFixed(1)}%</p>
              )}
              <p><strong style={{ color: 'var(--text)' }}>Sampler:</strong> DDIM, {steps} steps, η={eta.toFixed(2)}</p>
              {result.candidates_evaluated != null && (
                <p><strong style={{ color: 'var(--text)' }}>Candidate search:</strong> {result.candidates_evaluated} independent seeds; selected seed {result.selected_seed}</p>
              )}
              {result.dataset_novelty && (
                <p>
                  <strong style={{ color: 'var(--text)' }}>Reference-tile distance:</strong>{' '}
                  nearest of {result.dataset_novelty.reference_count} UCMerced tiles has
                  {' '}{result.dataset_novelty.nearest_tile_mse_32x32.toFixed(4)} MSE
                  {' '}at 32×32 comparison; this is an audit signal, not proof of originality
                </p>
              )}
              {result.selection_method && (
                <p style={{ fontSize: '0.78rem' }}><strong style={{ color: 'var(--text)' }}>Selection:</strong> {result.selection_method}</p>
              )}
              <p style={{ marginTop: 12, paddingTop: 10, borderTop: '1px solid var(--border)' }}><strong style={{ color: 'var(--text)' }}>What this means:</strong> {result.conditioning_mode ?? 'Class-conditional diffusion from Gaussian noise.'} It generates a new tile for the selected class. It does not preserve the uploaded tile’s layout, predict future development, or replace planning validation.</p>
            </div>
          </div>
        </div>
      )}

      <div className="card" style={{ marginTop: 24 }}>
        <div className="card-title"><ImageIcon size={17} /> How this model works</div>
        <p style={{ color: 'var(--muted)', lineHeight: 1.6, fontSize: '0.88rem' }}>
          The model learns to predict noise added to real UCMerced tiles over a 1,000-step forward diffusion process. At inference, DDIM starts from Gaussian noise and reverses that process in 40 steps using the selected land-use class. A restrained classifier-guidance signal and four seeded candidates help target the requested class without using the uploaded tile. The displayed training loss is the measured noise-prediction MSE from the persisted training history; it is not a visual-quality score.
        </p>
      </div>

      <DiffusionArchitecture />
    </div>
  );
}
