import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Upload, CheckCircle2, AlertCircle, Cpu, FileText, Layers, Image as ImageIcon, Database, HardDrive, ShieldCheck, Sparkles, KeyRound, BookOpen } from 'lucide-react';
import DatasetExplorer from './pages/DatasetExplorer';
import SystemInformation from './pages/SystemInformation';
import ModelExplorer from './pages/ModelExplorer';
import ModelComparison from './pages/ModelComparison';
import Training from './pages/Training';
import Evaluation from './pages/Evaluation';
import Research from './pages/Research';
import PlanGenerator from './pages/PlanGenerator';
import Governance from './pages/Governance';
import GAN from './pages/GAN';
import VAEArchitecture from './pages/VAEArchitecture';
import AEArchitecture from './pages/AEArchitecture';
import GANArchitecture from './pages/GANArchitecture';
import TransformerArchitecture from './pages/TransformerArchitecture';
import ClassifierArchitecture from './pages/ClassifierArchitecture';
import Glossary from './pages/Glossary';
import { apiFetch, getApiKey, setApiKey } from './lib/api';

type ViewType = 'ae' | 'vae' | 'classifier' | 'plan-generator' | 'governance' | 'gan' | 'prediction' | 'datasets' | 'system' | 'model-explorer' | 'model-comparison' | 'training' | 'evaluation' | 'research' | 'glossary';

// Image-inference views that share the upload UI below.
const IMAGE_VIEWS = ['ae', 'vae', 'classifier'] as const;
const isImageView = (v: ViewType) => (IMAGE_VIEWS as readonly string[]).includes(v);

// classifier training history is still stored under outputs/transformer/
const HISTORY_KEY: Record<string, string> = { ae: 'ae', vae: 'vae', classifier: 'transformer' };

const MODEL_META: Record<string, {
  title: string;
  description: string;
  resultTitle: string;
  panelLabels: string[];
  sampleEndpoint: string;
  sampleHint: string;
  inferEndpoint: string;
}> = {
  ae: {
    title: 'Autoencoder (Denoising)',
    description: 'A pretrained ResNet18 encoder + CNN decoder trained on UCMerced aerial land-use tiles (21 classes). It reconstructs a clean image from a noise-corrupted input — useful for denoising and restoring degraded satellite/aerial imagery before analysis.',
    resultTitle: 'Denoising Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Noisy Input', 'Reconstructed'],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles (roads, buildings, fields, etc.) — upload a similar image, or load a real sample below.',
    inferEndpoint: '/infer/ae',
  },
  vae: {
    title: 'Variational Autoencoder — Anomaly Detection & Latent Exploration',
    description: 'Primary use in this project: flags land parcels whose reconstruction error deviates from a 294-tile normal baseline — a real anomaly-detection signal for parcels that don’t match expected patterns for their zone (informal construction, illegal land conversion, sensor artifacts). Also supports latent interpolation between two real tiles. This VAE reconstructs and blends real, encoded tiles — it does not invent new buildings or roads on arbitrary land (see architecture below for why, and what would).',
    resultTitle: 'VAE Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Reconstructed'],
    sampleEndpoint: '/sample/ucmerced/undeveloped',
    sampleHint: 'Trained on UCMerced aerial tiles (roads, buildings, fields, etc.) — upload a similar image, or load a real (undeveloped) sample below to try the urbanization projection.',
    inferEndpoint: '/infer/vae',
  },
  classifier: {
    title: 'Land-Use Classifier (ResNet18)',
    description: 'A ResNet18 CNN fine-tuned via transfer learning to classify aerial imagery into 21 UCMerced land-use zoning categories (residential density, industrial, agricultural, transport, etc.) at ~98% validation accuracy — the kind of automated check used to audit zoning or track land-use change at city scale. Note: this is a CNN; the transformer requirement is met by the Urban Plan Generator.',
    resultTitle: 'Classification',
    panelLabels: [],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles — upload a similar image, or load a real sample below.',
    inferEndpoint: '/infer/classifier',
  },
};

export default function App() {
  const [activeView, setActiveView] = useState<ViewType>('ae');
  const [status, setStatus] = useState<any>({});

  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [resultData, setResultData] = useState<any>(null);
  const [interpImg, setInterpImg] = useState<string | null>(null);
  const [interpLoading, setInterpLoading] = useState(false);
  const [predictions, setPredictions] = useState<any[] | null>(null);
  const [randomGenImg, setRandomGenImg] = useState<string | null>(null);
  const [randomGenLoading, setRandomGenLoading] = useState(false);
  const [randomGenError, setRandomGenError] = useState<string | null>(null);
  const [urbanizeImg, setUrbanizeImg] = useState<string | null>(null);
  const [urbanizeLoading, setUrbanizeLoading] = useState(false);
  const [urbanizeError, setUrbanizeError] = useState<string | null>(null);
  const [urbanizeIntensity, setUrbanizeIntensity] = useState(0.6);

  const [metrics, setMetrics] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKeyState] = useState(getApiKey());
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    apiFetch('/status')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    const key = HISTORY_KEY[activeView];
    if (key) {
      apiFetch(`/history/${key}`)
        .then(res => res.json())
        .then(data => setHistory(data))
        .catch(err => console.error(err));
    }
  }, [activeView]);

  useEffect(() => {
    setFile(null);
    setPreview(null);
    setResultData(null);
    setInterpImg(null);
    setMetrics(null);
    setPredictions(null);
    setUrbanizeImg(null);
    setUrbanizeError(null);
  }, [activeView]);

  const clearSelection = () => {
    setFile(null);
    setPreview(null);
    setResultData(null);
    setInterpImg(null);
    setMetrics(null);
    setPredictions(null);
    setUrbanizeImg(null);
    setUrbanizeError(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setFile(f);
      if (f.name.toLowerCase().endsWith('.tif') || f.name.toLowerCase().endsWith('.tiff')) {
        setPreview('');
      } else {
        setPreview(URL.createObjectURL(f));
      }
      setResultData(null);
      setInterpImg(null);
      setMetrics(null);
      setPredictions(null);
      setUrbanizeImg(null);
      setUrbanizeError(null);
    }
  };

  const handleLoadSample = async () => {
    const meta = MODEL_META[activeView];
    if (!meta) return;
    setLoading(true);
    try {
      const res = await apiFetch(meta.sampleEndpoint);
      const blob = await res.blob();
      const cls = res.headers.get('X-Class') || 'sample';
      const f = new File([blob], `${cls}.jpg`, { type: 'image/jpeg' });
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResultData(null);
      setInterpImg(null);
      setMetrics(null);
      setPredictions(null);
      setUrbanizeImg(null);
      setUrbanizeError(null);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiFetch(MODEL_META[activeView].inferEndpoint, { method: 'POST', body: formData });

      if (res.ok) {
        const data = await res.json();
        if (activeView === 'classifier') {
          setPredictions(data.predictions);
        } else {
          setResultData(data);
          if (activeView === 'ae') {
            setMetrics({ mse: data.mse, psnr: data.psnr });
          } else if (activeView === 'vae') {
            setMetrics({
              mu: data.mu, logvar: data.logvar, kl: data.kl, klPerDim: data.kl_per_dim, mse: data.mse,
              anomalyScore: data.anomaly_score, anomalyLevel: data.anomaly_level,
              anomalyPercentDiff: data.anomaly_percent_diff, anomalyReason: data.anomaly_reason,
            });
          }
        }
      } else {
        setMetrics({ error: res.status === 401 ? 'API key required — set it in the sidebar.' : await res.text() });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInterpolate = async () => {
    if (!file) return;
    setInterpLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await apiFetch('/infer/vae/interpolate', { method: 'POST', body: formData });
      if (res.ok) {
        const blob = await res.blob();
        setInterpImg(URL.createObjectURL(blob));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setInterpLoading(false);
    }
  };

  const handleUrbanize = async () => {
    if (!file) return;
    setUrbanizeLoading(true);
    setUrbanizeError(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('alpha', String(urbanizeIntensity));
    try {
      const res = await apiFetch('/infer/vae/urbanize', { method: 'POST', body: formData });
      if (!res.ok) {
        setUrbanizeError(res.status === 401 ? 'API key required — set it in the sidebar.' : await res.text());
        return;
      }
      const data = await res.json();
      setUrbanizeImg(`data:image/jpeg;base64,${data.urbanized}`);
    } catch (err) {
      setUrbanizeError(String(err));
    } finally {
      setUrbanizeLoading(false);
    }
  };

  const handleGenerateRandom = async () => {
    setRandomGenLoading(true);
    setRandomGenError(null);
    try {
      const res = await apiFetch('/generate/vae/random', { method: 'POST' });
      if (!res.ok) {
        setRandomGenError(res.status === 401 ? 'API key required — set it in the sidebar.' : await res.text());
        return;
      }
      const data = await res.json();
      setRandomGenImg(`data:image/jpeg;base64,${data.generated}`);
    } catch (err) {
      setRandomGenError(String(err));
    } finally {
      setRandomGenLoading(false);
    }
  };

  const saveKey = (v: string) => {
    setApiKeyState(v);
    setApiKey(v);
  };

  const navItems: any[] = [
    { id: 'model-explorer', label: 'Model Explorer', icon: Layers, active: true },
    { id: 'model-comparison', label: 'Model Comparison', icon: FileText, active: true },
    { id: 'ae', label: 'Autoencoder', icon: Layers, active: true },
    { id: 'vae', label: 'VAE', icon: FileText, active: true },
    { id: 'plan-generator', label: 'Urban Plan Generator', icon: Sparkles, active: true },
    { id: 'classifier', label: 'Land-Use Classifier', icon: Cpu, active: true },
    { id: 'training', label: 'Training', icon: Cpu, active: true },
    { id: 'evaluation', label: 'Evaluation', icon: FileText, active: true },
    { id: 'research', label: 'Research', icon: Layers, active: true },
    { id: 'glossary', label: 'Glossary', icon: BookOpen, active: true },
    { id: 'governance', label: 'Governance', icon: ShieldCheck, active: true },
    { id: 'datasets', label: 'Dataset Explorer', icon: Database, active: true },
    { id: 'system', label: 'System Info', icon: HardDrive, active: true },
    { id: 'gan', label: 'GAN Generator', icon: ImageIcon, active: true },
    { id: 'prediction', label: 'Prediction Engine', icon: CheckCircle2, active: false, badge: 'Soon' },
  ];

  const statusKey = activeView === 'plan-generator' ? 'gpt' : activeView;

  return (
    <>
      <style dangerouslySetInnerHTML={{__html: `
        :root {
          --bg: #080C14;
          --surface: #0F1923;
          --border: #1E2D40;
          --accent: #00D4FF;
          --accent2: #7B61FF;
          --text: #E8EDF5;
          --muted: #4A6080;
          --success: #00E676;
          --font-ui: 'Space Grotesk', sans-serif;
          --font-mono: 'JetBrains Mono', monospace;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg); color: var(--text); font-family: var(--font-ui); }
        .app-container { display: flex; height: 100vh; overflow: hidden; }
        .sidebar { width: 240px; background-color: var(--surface); border-right: 1px solid var(--border); padding: 20px 0; display: flex; flex-direction: column; overflow-y: auto; }
        .logo-area { padding: 0 20px 20px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
        .logo-text { font-size: 1.25rem; font-weight: 700; color: var(--accent); letter-spacing: 0.05em; display: flex; align-items: center; gap: 10px; }
        .nav-list { display: flex; flex-direction: column; gap: 5px; padding: 0 10px; }
        .nav-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 15px; border-radius: 6px; cursor: pointer; transition: all 0.2s; color: var(--text); font-size: 0.9rem; }
        .nav-item:hover:not(.disabled) { background-color: rgba(255,255,255,0.05); }
        .nav-item.active { background-color: rgba(0, 212, 255, 0.1); color: var(--accent); border-left: 3px solid var(--accent); }
        .nav-item.disabled { color: var(--muted); cursor: not-allowed; }
        .nav-item-content { display: flex; align-items: center; gap: 10px; }
        .badge { background: var(--border); color: var(--muted); font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; }

        .main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
        .topbar { padding: 15px 30px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: var(--surface); }
        .status-chip { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; padding: 6px 12px; border-radius: 6px; background: rgba(0, 230, 118, 0.1); color: var(--success); border: 1px solid rgba(0, 230, 118, 0.2); }
        .status-chip.error { background: rgba(255, 82, 82, 0.1); color: #FF5252; border-color: rgba(255, 82, 82, 0.2); }

        .content-body { padding: 30px; max-width: 1200px; margin: 0 auto; width: 100%; }
        .panel-header { margin-bottom: 30px; }
        .panel-title { font-size: 1.8rem; font-weight: 600; margin-bottom: 8px; }
        .panel-desc { color: var(--muted); font-size: 0.95rem; line-height: 1.55; }

        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 20px; }
        .card-title { font-size: 1rem; font-weight: 500; margin-bottom: 15px; color: var(--accent2); display: flex; justify-content: space-between; gap: 12px; }

        .upload-zone { border: 2px dashed var(--border); border-radius: 6px; padding: 40px 20px; text-align: center; cursor: pointer; transition: all 0.2s; background: rgba(30, 45, 64, 0.2); }
        .upload-zone:hover { border-color: var(--accent); background: rgba(0, 212, 255, 0.05); }
        .upload-icon { color: var(--accent); margin-bottom: 10px; width: 32px; height: 32px; }

        .image-preview { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 4px; border: 1px solid var(--border); }
        .btn { background: var(--accent); color: #000; border: none; padding: 10px 20px; border-radius: 4px; font-family: var(--font-ui); font-weight: 600; cursor: pointer; width: 100%; margin-top: 15px; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }

        .metrics-strip { display: flex; gap: 20px; flex-wrap: wrap; background: var(--surface); border: 1px solid var(--border); padding: 15px 20px; border-radius: 6px; margin-bottom: 30px; }
        .metric { display: flex; flex-direction: column; gap: 4px; }
        .metric-label { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-value { font-family: var(--font-mono); font-size: 1.2rem; color: var(--accent); }

        .chart-container { height: 300px; width: 100%; }

        .predictions-list { display: flex; flex-direction: column; gap: 10px; }
        .pred-item { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 45, 64, 0.3); padding: 10px 15px; border-radius: 4px; }
        .pred-class { font-weight: 500; text-transform: capitalize; }
        .pred-prob { font-family: var(--font-mono); color: var(--accent); }

        .key-field { display: flex; align-items: center; gap: 6px; margin: 14px 10px 0; padding: 8px 10px; border: 1px solid var(--border); border-radius: 6px; }
        .key-field input { background: var(--bg); border: 1px solid var(--border); border-radius: 4px; color: var(--text); padding: 5px 7px; font-family: var(--font-mono); font-size: 0.75rem; width: 100%; }
      `}} />

      <div className="app-container">
        <div className="sidebar">
          <div className="logo-area">
            <div className="logo-text">
              <Layers size={24} /> UrbanGen AI
            </div>
          </div>
          <div className="nav-list">
            {navItems.map(item => (
              <div
                key={item.id}
                className={`nav-item ${activeView === item.id ? 'active' : ''} ${!item.active ? 'disabled' : ''}`}
                onClick={() => item.active && setActiveView(item.id as ViewType)}
              >
                <div className="nav-item-content">
                  <item.icon size={18} />
                  {item.label}
                </div>
                {item.badge && <span className="badge">{item.badge}</span>}
              </div>
            ))}
          </div>
          <div className="key-field" title="Stored only in this browser; sent as X-API-Key to the local API. Leave blank if the backend has no key configured.">
            <KeyRound size={14} style={{ color: 'var(--muted)', flexShrink: 0 }} />
            <input
              type="password"
              placeholder="API key (optional)"
              value={apiKey}
              onChange={e => saveKey(e.target.value)}
            />
          </div>
        </div>

        <div className="main-content">
          <div className="topbar">
            <div style={{ color: 'var(--muted)' }}>Terminal / {activeView}</div>
            {status[statusKey] ? (
              <div className={`status-chip ${status[statusKey] === 'Trained' ? '' : 'error'}`}>
                {status[statusKey] === 'Trained' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
                {status[statusKey] === 'Trained' ? 'Trained ✓' : 'Not trained yet — run backend script'}
              </div>
            ) : null}
          </div>

          <div className="content-body">
            {isImageView(activeView) && (
              <div className="panel-header">
                <h1 className="panel-title">{MODEL_META[activeView].title}</h1>
                <div className="panel-desc">{MODEL_META[activeView].description}</div>
              </div>
            )}

            {activeView === 'ae' && <AEArchitecture />}
            {activeView === 'vae' && <VAEArchitecture />}
            {activeView === 'classifier' && <ClassifierArchitecture />}

            {activeView === 'datasets' && <DatasetExplorer />}
            {activeView === 'system' && <SystemInformation />}
            {activeView === 'model-explorer' && <ModelExplorer setActiveView={setActiveView} />}
            {activeView === 'model-comparison' && <ModelComparison />}
            {activeView === 'training' && <Training />}
            {activeView === 'evaluation' && <Evaluation />}
            {activeView === 'research' && <Research />}
            {activeView === 'glossary' && <Glossary />}
            {activeView === 'plan-generator' && <TransformerArchitecture />}
            {activeView === 'plan-generator' && <PlanGenerator />}
            {activeView === 'governance' && <Governance />}
            {activeView === 'gan' && <GANArchitecture />}
            {activeView === 'gan' && <GAN isGanTrained={status['gan'] === 'Trained'} />}

            {isImageView(activeView) && (
              <>
            <div className="card" style={{ marginBottom: '30px' }}>
              <div className="card-title">
                {resultData || predictions
                  ? MODEL_META[activeView].resultTitle
                  : activeView === 'classifier' ? 'Classify Land-Use' : 'Upload Image'}
              </div>
              {!file ? (
                <div>
                  <div className="upload-zone" onClick={() => fileInputRef.current?.click()}>
                    <Upload className="upload-icon" />
                    <p style={{ color: 'var(--text)' }}>Click or drag image to upload</p>
                    <p style={{ color: 'var(--muted)', fontSize: '0.85rem', marginTop: '10px' }}>{MODEL_META[activeView].sampleHint}</p>
                  </div>
                  <button
                    className="btn"
                    style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}
                    onClick={handleLoadSample}
                    disabled={loading}
                  >
                    {loading ? 'Loading...' : activeView === 'vae' ? 'Load Real Sample (Undeveloped)' : 'Load Real Sample (UCMerced)'}
                  </button>
                </div>
              ) : (
                <div>
                  {!resultData && !(activeView === 'classifier' && predictions) ? (
                    <div className="grid-2" style={{ marginBottom: 0 }}>
                      {preview ? (
                        <img src={preview} className="image-preview" alt="Input" />
                      ) : (
                        <div className="image-preview" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: 'var(--muted)', fontSize: '0.85rem', padding: '10px' }}>
                          {file.name}<br />(preview unavailable for this format)
                        </div>
                      )}
                      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '15px' }}>
                        <button className="btn" onClick={handleUpload} disabled={loading || status[statusKey] !== 'Trained'}>
                          {loading ? 'Processing...' : activeView === 'classifier' ? 'Run Classification' : 'Run Inference'}
                        </button>
                        <button className="btn" onClick={clearSelection} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}>Clear Selection</button>
                      </div>
                    </div>
                  ) : activeView === 'classifier' ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                      <div className="grid-2" style={{ marginBottom: 0 }}>
                        {preview ? <img src={preview} className="image-preview" alt="Input" /> : (
                          <div className="image-preview" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontSize: '0.85rem' }}>{file.name}</div>
                        )}
                        <div className="predictions-list">
                          {Array.isArray(predictions) && predictions.map((p: any, i: number) => (
                            <div className="pred-item" key={i}>
                              <span className="pred-class">{p.class}</span>
                              <span className="pred-prob">{Number(p.confidence).toFixed(2)}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                      <button className="btn" onClick={clearSelection} style={{ maxWidth: '200px', margin: '0 auto' }}>Classify Another</button>
                    </div>
                  ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0 10px', color: 'var(--muted)', fontSize: '0.9rem', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                        {MODEL_META[activeView].panelLabels.map((label, i) => (
                          <div key={i} style={{ flex: 1, textAlign: 'center' }}>{label}</div>
                        ))}
                      </div>
                      <div style={{ display: 'flex', gap: '10px' }}>
                        {preview ? (
                          <img src={preview} style={{ flex: 1, width: 0, minWidth: 0, height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Original" />
                        ) : (
                          <div style={{ flex: 1, aspectRatio: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: 'var(--muted)', fontSize: '0.8rem', padding: '10px', borderRadius: '4px', border: '1px solid var(--border)' }}>
                            {file?.name}<br />(preview unavailable)
                          </div>
                        )}
                        {activeView === 'ae' && resultData?.noisy && (
                          <img src={`data:image/jpeg;base64,${resultData.noisy}`} style={{ flex: 1, width: 0, minWidth: 0, height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Noisy" />
                        )}
                        {resultData?.reconstructed && (
                          <img src={`data:image/jpeg;base64,${resultData.reconstructed}`} style={{ flex: 1, width: 0, minWidth: 0, height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Reconstructed" />
                        )}
                      </div>

                      {/* Anomaly result: the headline output of the VAE in this project — a
                          large, standalone banner with a plain-language reason and a percentage,
                          not just a raw z-score buried in a metrics row. Shown immediately after
                          the reconstruction, before interpolation/urbanization/random-sample. */}
                      {activeView === 'vae' && metrics?.anomalyLevel && (
                        <div style={{
                          padding: '18px 22px', borderRadius: 8,
                          background: metrics.anomalyLevel === 'Typical' ? 'rgba(0, 230, 118, 0.08)'
                            : metrics.anomalyLevel === 'Unusual' ? 'rgba(255, 184, 77, 0.08)' : 'rgba(255, 82, 82, 0.08)',
                          border: `1px solid ${metrics.anomalyLevel === 'Typical' ? 'rgba(0, 230, 118, 0.35)'
                            : metrics.anomalyLevel === 'Unusual' ? 'rgba(255, 184, 77, 0.35)' : 'rgba(255, 82, 82, 0.35)'}`,
                        }}>
                          <div style={{ display: 'flex', alignItems: 'baseline', gap: 14, flexWrap: 'wrap', marginBottom: 8 }}>
                            <span style={{
                              fontSize: '1.3rem', fontWeight: 700, fontFamily: 'var(--font-mono)',
                              color: metrics.anomalyLevel === 'Typical' ? 'var(--success)'
                                : metrics.anomalyLevel === 'Unusual' ? '#FFB84D' : '#FF5252',
                            }}>
                              {metrics.anomalyLevel === 'Typical' ? '✓' : '⚠'} {metrics.anomalyLevel.toUpperCase()}
                            </span>
                            {metrics.anomalyPercentDiff != null && (
                              <span style={{ fontSize: '1.1rem', fontFamily: 'var(--font-mono)', color: 'var(--text)' }}>
                                {metrics.anomalyPercentDiff > 0 ? '+' : ''}{Number(metrics.anomalyPercentDiff).toFixed(0)}% reconstruction error vs. normal
                              </span>
                            )}
                            <span style={{ fontSize: '0.8rem', color: 'var(--muted)', fontFamily: 'var(--font-mono)' }}>
                              (z = {Number(metrics.anomalyScore).toFixed(2)})
                            </span>
                          </div>
                          <div style={{ fontSize: '0.88rem', color: 'var(--text)', lineHeight: 1.55 }}>
                            {metrics.anomalyReason}
                          </div>
                        </div>
                      )}

                      {metrics && (
                        <div className="metrics-strip">
                          {activeView === 'ae' ? (
                            <>
                              <div className="metric"><span className="metric-label">MSE Loss</span><span className="metric-value">{Number(metrics.mse).toFixed(5)}</span></div>
                              <div className="metric"><span className="metric-label">PSNR</span><span className="metric-value">{Number(metrics.psnr).toFixed(2)} dB</span></div>
                            </>
                          ) : (
                            <>
                              <div className="metric"><span className="metric-label">μ Mean</span><span className="metric-value">{Number(metrics.mu).toFixed(4)}</span></div>
                              <div className="metric"><span className="metric-label">log(var) Mean</span><span className="metric-value">{Number(metrics.logvar).toFixed(4)}</span></div>
                              {metrics.kl != null && (
                                <div className="metric">
                                  <span className="metric-label">KL Divergence</span>
                                  <span className="metric-value" style={{ color: 'var(--accent2)' }}>{Number(metrics.kl).toFixed(2)} nats</span>
                                </div>
                              )}
                              {metrics.klPerDim != null && (
                                <div className="metric"><span className="metric-label">KL / latent dim</span><span className="metric-value">{Number(metrics.klPerDim).toFixed(4)}</span></div>
                              )}
                            </>
                          )}
                        </div>
                      )}
                      {activeView === 'vae' && metrics?.kl != null && (
                        <div style={{ color: 'var(--muted)', fontSize: '0.8rem', marginTop: '-10px', marginBottom: '10px', padding: '0 5px', lineHeight: 1.55 }}>
                          <strong>KL divergence</strong> (shown above, in nats) measures how far the encoder's posterior q(z|x) sits from the
                          prior N(0, I). The reparameterization trick z = μ + σ·ε makes this term differentiable so it can be trained.
                          The objective is <code>reconstruction + β·KL</code>; this checkpoint uses a near-zero β to keep reconstructions sharp,
                          so KL is reported but not minimised (it rises during training as the latent grows more informative — expected for a
                          reconstruction-priority VAE).
                        </div>
                      )}

                      {activeView === 'vae' && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center' }}>
                          <button className="btn" style={{ maxWidth: '320px', background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }} onClick={handleInterpolate} disabled={interpLoading}>
                            {interpLoading ? 'Interpolating...' : 'Show Land-Use Interpolation'}
                          </button>
                          {interpImg && (
                            <div style={{ width: '100%' }}>
                              <div style={{ color: 'var(--muted)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px', textAlign: 'center' }}>
                                Latent-space blend: this image &rarr; a random real land-cover tile
                              </div>
                              <img src={interpImg} style={{ width: '100%', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Latent Interpolation" />
                            </div>
                          )}
                        </div>
                      )}

                      {activeView === 'vae' && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center', borderTop: '1px solid var(--border)', paddingTop: '15px' }}>
                          <p style={{ color: 'var(--muted)', fontSize: '0.8rem', lineHeight: 1.5, textAlign: 'center', maxWidth: '480px' }}>
                            Neural style transfer (VGG16 features, optimized per request — not a VAE
                            technique): starts from <strong>this exact uploaded image</strong> and
                            textures it toward a randomly picked real developed/built-up tile, while
                            a content loss keeps it anchored to the original layout. This is the same
                            land — its boundaries and structure come from your upload, not from the
                            style tile — with a "more built-up" material/texture applied. It can't
                            invent new roads or buildings beyond what the layout already implies.
                            Optimized natively at 512×512 on GPU — takes about 15 seconds.
                          </p>
                          <label style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
                            Style strength: <span style={{ color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}>{Math.round(urbanizeIntensity * 100)}%</span>
                            <input type="range" min={0.1} max={1} step={0.05} value={urbanizeIntensity}
                              onChange={e => setUrbanizeIntensity(parseFloat(e.target.value))}
                              style={{ display: 'block', width: 220, marginTop: 4 }} />
                          </label>
                          <button className="btn" style={{ maxWidth: '320px', background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }} onClick={handleUrbanize} disabled={urbanizeLoading}>
                            {urbanizeLoading ? 'Projecting… (~15s)' : 'Show Urbanization Projection'}
                          </button>
                          {urbanizeError && (
                            <div style={{
                              border: '1px solid #FF5252', color: '#FF5252', borderRadius: '4px',
                              padding: '10px 12px', fontSize: '0.85rem', width: '100%',
                            }}>
                              {urbanizeError}
                            </div>
                          )}
                          {urbanizeImg && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                              <div style={{ color: 'var(--muted)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px', textAlign: 'center' }}>
                                Same land, urbanization projection ({Math.round(urbanizeIntensity * 100)}% style strength)
                              </div>
                              {/* Output is natively 512x512 — cap display at that so the browser
                                  never upscales it past its real resolution (which is what made it
                                  look blurrier the more this was zoomed/stretched). */}
                              <img src={urbanizeImg} style={{ width: '100%', maxWidth: '512px', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Urbanization Projection" />
                            </div>
                          )}
                        </div>
                      )}

                      <button className="btn" onClick={clearSelection} style={{ maxWidth: '200px', margin: '0 auto' }}>Upload Another</button>
                    </div>
                  )}
                </div>
              )}
              <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept="image/*,.tif,.tiff" onChange={handleFileChange} />
            </div>

            {activeView === 'vae' && (
              <div className="card" style={{ marginBottom: '30px' }}>
                <div className="card-title">Generate Random Sample</div>
                <p style={{ color: 'var(--muted)', fontSize: '0.85rem', lineHeight: 1.5, marginBottom: '15px' }}>
                  Samples a latent z ~ N(0, I) directly from the prior — with no input image — and
                  decodes it. This is the VAE's defining generative capability, distinct from
                  reconstruction (above) and interpolation (which both decode real, encoded
                  images). This checkpoint was trained to prioritize reconstruction fidelity over
                  matching the prior exactly, so a pure prior sample can look more abstract than a
                  reconstruction — that's an expected trade-off, not a bug.
                </p>
                <button className="btn" style={{ maxWidth: '320px' }} onClick={handleGenerateRandom} disabled={randomGenLoading || status[statusKey] !== 'Trained'}>
                  {randomGenLoading ? 'Generating...' : 'Generate Random Sample'}
                </button>
                {randomGenError && (
                  <div style={{
                    border: '1px solid #FF5252', color: '#FF5252', borderRadius: '4px',
                    padding: '10px 12px', marginTop: '15px', fontSize: '0.85rem',
                  }}>
                    {randomGenError}
                  </div>
                )}
                {randomGenImg && (
                  <div style={{ marginTop: '15px', maxWidth: '320px' }}>
                    <div style={{ color: 'var(--muted)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px', textAlign: 'center' }}>
                      Generated from N(0, I)
                    </div>
                    <img src={randomGenImg} style={{ width: '100%', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }} alt="Random prior sample" />
                  </div>
                )}
              </div>
            )}

            {activeView === 'classifier' && (
              <div className="grid-2">
                <div className="card">
                  <div className="card-title">RAG Query</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <textarea
                      style={{ width: '100%', minHeight: '100px', background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: '4px', padding: '10px' }}
                      placeholder="Ask about Pune's urban stats..."
                      id="rag-query-input"
                    />
                    <button className="btn" onClick={async () => {
                      const query = (document.getElementById('rag-query-input') as HTMLTextAreaElement).value;
                      if (!query) return;
                      setLoading(true);
                      try {
                        const res = await apiFetch('/transformer/query', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ query })
                        });
                        const data = await res.json();
                        setMetrics({ response: data.response });
                      } catch (e) {
                        console.error(e);
                      } finally {
                        setLoading(false);
                      }
                    }}>
                      {loading ? 'Querying...' : 'Ask RAG'}
                    </button>
                    {metrics && metrics.response && (
                      <div style={{ padding: '15px', background: 'rgba(0, 212, 255, 0.1)', border: '1px solid var(--accent)', borderRadius: '4px', color: 'var(--text)' }}>
                        <strong>Response:</strong> {metrics.response}
                      </div>
                    )}
                  </div>
                </div>

                <div className="card">
                  <div className="card-title">Urban Stats (PUNE_STATS)</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <button className="btn" style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }} onClick={async () => {
                      try {
                        const res = await apiFetch('/transformer/stats');
                        const data = await res.json();
                        setMetrics((prev: any) => ({ ...prev, stats: data }));
                      } catch (e) {
                        console.error(e);
                      }
                    }}>Load Stats</button>
                    {metrics && metrics.stats && (
                      <pre style={{ background: 'var(--bg)', padding: '10px', borderRadius: '4px', overflowX: 'auto', fontSize: '0.85rem' }}>
                        {JSON.stringify(metrics.stats, null, 2)}
                      </pre>
                    )}
                  </div>
                </div>
              </div>
            )}


            {history.length > 0 && (
              <div className="card">
                <div className="card-title">Training {activeView === 'classifier' ? 'Metrics' : 'Loss'} Curve</div>
                <div className="chart-container">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={history}>
                      <XAxis dataKey="epoch" stroke="var(--muted)" fontSize={12} />
                      <YAxis yAxisId="left" stroke="var(--muted)" fontSize={12} domain={['auto', 'auto']} />
                      {activeView === 'vae' && (
                        <YAxis yAxisId="right" orientation="right" stroke="var(--accent2)" fontSize={12} domain={['auto', 'auto']} />
                      )}
                      <Tooltip
                        contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}
                        itemStyle={{ fontFamily: 'var(--font-mono)' }}
                      />
                      <Legend />
                      <Line yAxisId="left" type="monotone" dataKey={activeView === 'vae' ? 'recon' : 'loss'} name={activeView === 'vae' ? 'reconstruction (left)' : 'loss'} stroke="var(--accent)" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
                      {activeView === 'vae' && <Line yAxisId="right" type="monotone" dataKey="kl" name="KL divergence (right)" stroke="var(--accent2)" strokeWidth={2} dot={false} />}
                      {activeView === 'classifier' && <Line yAxisId="left" type="monotone" dataKey="val_loss" name="val loss" stroke="var(--accent2)" strokeWidth={2} dot={false} />}
                      {activeView === 'classifier' && <Line yAxisId="left" type="monotone" dataKey="val_accuracy" name="val accuracy" stroke="var(--success)" strokeWidth={2} dot={false} />}
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {history.length === 0 && status[statusKey] === 'Trained' && (
              <div className="card">
                <div className="card-title">Training History</div>
                <div style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0' }}>
                  History file not found in outputs directory.
                </div>
              </div>
            )}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
