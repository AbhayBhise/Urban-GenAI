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

export default function Diffusion() {
  const [metrics, setMetrics] = useState<DiffusionMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [className, setClassName] = useState('buildings');
  const [steps, setSteps] = useState(20);
  const [eta, setEta] = useState(0);
  const [image, setImage] = useState<string | null>(null);
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
    setImage(null);
    setGenerationError(null);
    const isTiff = next?.name.toLowerCase().endsWith('.tif') || next?.name.toLowerCase().endsWith('.tiff');
    if (next && next.type.startsWith('image/') && !isTiff) setPreview(URL.createObjectURL(next));
    else setPreview(null);
  };

  const generate = async () => {
    if (!file || metrics?.status !== 'trained') return;
    setGenerating(true);
    setGenerationError(null);
    setImage(null);
    try {
      const body = new FormData();
      body.append('file', file);
      body.append('class_name', className);
      body.append('steps', String(steps));
      body.append('eta', String(eta));
      const response = await apiFetch('/infer/diffusion', { method: 'POST', body });
      if (!response.ok) throw new Error(await response.text());
      const result = await response.json();
      setImage(result.image);
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
          Generate a source-conditioned aerial tile for a selected land-use class using the trained DDPM and fast DDIM sampler.
          The source tile anchors the scene; the class controls the requested land-use condition.
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
          <div className="card-title">1. Choose source tile</div>
          <label className="upload-zone" style={{ display: 'block' }}>
            <Upload className="upload-icon" />
            <p style={{ color: 'var(--text)' }}>{previewLabel}</p>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', marginTop: 10 }}>PNG, JPG, JPEG, or TIFF · resized to 128×128</p>
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
                The page is connected to the real inference endpoint, but generation is disabled until the image-conditioned diffusion model is trained on the GPU. No placeholder image is shown.
              </p>
              <code style={{ display: 'block', marginTop: 10, color: 'var(--text)' }}>python backend/train_diffusion.py</code>
              <p style={{ color: 'var(--muted)', fontSize: '0.8rem', marginTop: 6 }}>The training script selects CUDA automatically when it is available.</p>
            </div>
          </div>
        </div>
      )}

      {generationError && <div className="card" style={{ borderColor: 'var(--danger)', color: 'var(--danger)', marginBottom: 20 }}>{generationError}</div>}

      {image && (
        <div className="card">
          <div className="card-title"><span>Generated scenario tile</span><span style={{ color: 'var(--success)', fontSize: '0.78rem' }}><CheckCircle2 size={15} style={{ verticalAlign: 'middle', marginRight: 5 }} />real model output</span></div>
          <div className="grid-2" style={{ marginBottom: 0 }}>
            <div><img src={image} alt={`Generated ${className} scenario`} className="image-preview" /></div>
            <div style={{ color: 'var(--muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              <p><strong style={{ color: 'var(--text)' }}>Condition:</strong> {className}</p>
              <p><strong style={{ color: 'var(--text)' }}>Sampler:</strong> DDIM, {steps} steps, η={eta.toFixed(2)}</p>
              <p style={{ marginTop: 12 }}>This is a generated scenario visualization conditioned on the uploaded source tile. It is not a measured forecast or a substitute for planning validation.</p>
            </div>
          </div>
        </div>
      )}

      <div className="card" style={{ marginTop: 24 }}>
        <div className="card-title"><ImageIcon size={17} /> How this model works</div>
        <p style={{ color: 'var(--muted)', lineHeight: 1.6, fontSize: '0.88rem' }}>
          The model learns to predict the noise added at each point in a 1,000-step forward diffusion process. At inference, DDIM reverses that process in a smaller number of steps while receiving the source image and target class at every denoising stage. The displayed training loss is the measured noise-prediction MSE from the persisted training history; it is not fabricated when the checkpoint is unavailable.
        </p>
      </div>

      <DiffusionArchitecture />
    </div>
  );
}
