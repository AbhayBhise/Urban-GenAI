import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Upload, CheckCircle2, XCircle, AlertCircle, Cpu, FileText, Layers, Image as ImageIcon, Database, HardDrive } from 'lucide-react';
import DatasetExplorer from './pages/DatasetExplorer';
import SystemInformation from './pages/SystemInformation';
import ModelExplorer from './pages/ModelExplorer';
import ModelComparison from './pages/ModelComparison';
import Training from './pages/Training';
import Evaluation from './pages/Evaluation';
import Research from './pages/Research';

const API_URL = 'http://127.0.0.1:8000';

type ViewType = 'ae' | 'vae' | 'transformer' | 'gan' | 'prediction' | 'datasets' | 'system' | 'model-explorer' | 'model-comparison' | 'training' | 'evaluation' | 'research';

const MODEL_META: Record<string, {
  title: string;
  description: string;
  resultTitle: string;
  panelLabels: string[];
  sampleEndpoint: string;
  sampleHint: string;
}> = {
  ae: {
    title: 'Autoencoder (Denoising)',
    description: 'A pretrained ResNet18 encoder + CNN decoder trained on UCMerced aerial land-use tiles (21 classes). It reconstructs a clean image from a noise-corrupted input — useful for denoising and restoring degraded satellite/aerial imagery before analysis.',
    resultTitle: 'Denoising Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Noisy Input', 'Reconstructed'],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles (roads, buildings, fields, etc.) — upload a similar image, or load a real sample below.',
  },
  vae: {
    title: 'Variational Autoencoder',
    description: 'A pretrained ResNet18 encoder feeding a probabilistic spatial latent (mu, logvar; encoder->reparameterize->decoder), trained on the same UCMerced aerial tiles as the Autoencoder, prioritizing reconstruction fidelity over textbook prior-sampling behavior. Enables smooth interpolation between two real land-use tiles and reconstruction-error-based anomaly detection.',
    resultTitle: 'VAE Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Reconstructed'],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles (roads, buildings, fields, etc.) — upload a similar image, or load a real sample below.',
  },
  transformer: {
    title: 'Transformer (ResNet18 Classifier)',
    description: 'A ResNet18 CNN fine-tuned via transfer learning to classify aerial imagery into 21 UCMerced land-use zoning categories (residential density, industrial, agricultural, transport, etc.) at ~98% validation accuracy — the kind of automated check used to audit zoning or track land-use change at city scale.',
    resultTitle: 'Classification',
    panelLabels: [],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles — upload a similar image, or load a real sample below.',
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

  const [metrics, setMetrics] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${API_URL}/status`)
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    if (activeView === 'ae' || activeView === 'vae' || activeView === 'transformer') {
      fetch(`${API_URL}/history/${activeView}`)
        .then(res => res.json())
        .then(data => setHistory(data))
        .catch(err => console.error(err));
    }
  }, [activeView]);

  // Reset per-image state when switching model tabs so stale results/labels
  // from a different model never linger on screen.
  useEffect(() => {
    setFile(null);
    setPreview(null);
    setResultData(null);
    setInterpImg(null);
    setMetrics(null);
    setPredictions(null);
  }, [activeView]);

  const clearSelection = () => {
    setFile(null);
    setPreview(null);
    setResultData(null);
    setInterpImg(null);
    setMetrics(null);
    setPredictions(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setFile(f);
      if (f.name.toLowerCase().endsWith('.tif') || f.name.toLowerCase().endsWith('.tiff')) {
        setPreview(''); // Don't try to render TIFF natively (browsers can't display it)
      } else {
        setPreview(URL.createObjectURL(f));
      }
      setResultData(null);
      setInterpImg(null);
      setMetrics(null);
      setPredictions(null);
    }
  };

  const handleLoadSample = async () => {
    const meta = MODEL_META[activeView];
    if (!meta) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}${meta.sampleEndpoint}`);
      const blob = await res.blob();
      const cls = res.headers.get('X-Class') || 'sample';
      const f = new File([blob], `${cls}.jpg`, { type: 'image/jpeg' });
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResultData(null);
      setInterpImg(null);
      setMetrics(null);
      setPredictions(null);
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
      const res = await fetch(`${API_URL}/infer/${activeView}`, {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        if (activeView === 'transformer') {
          setPredictions(data.predictions);
        } else {
          setResultData(data);
          if (activeView === 'ae') {
            setMetrics({ mse: data.mse, psnr: data.psnr });
          } else if (activeView === 'vae') {
            setMetrics({ mu: data.mu, logvar: data.logvar, mse: data.mse, anomalyScore: data.anomaly_score, anomalyLevel: data.anomaly_level });
          }
        }
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
      const res = await fetch(`${API_URL}/infer/vae/interpolate`, { method: 'POST', body: formData });
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

  const navItems = [
    { id: 'model-explorer', label: 'Model Explorer', icon: Layers, active: true },
    { id: 'model-comparison', label: 'Model Comparison', icon: FileText, active: true },
    { id: 'ae', label: 'Autoencoder', icon: Layers, active: true },
    { id: 'vae', label: 'VAE', icon: FileText, active: true },
    { id: 'transformer', label: 'Transformer', icon: Cpu, active: true },
    { id: 'training', label: 'Training', icon: Cpu, active: true },
    { id: 'evaluation', label: 'Evaluation', icon: FileText, active: true },
    { id: 'research', label: 'Research', icon: Layers, active: true },
    { id: 'datasets', label: 'Dataset Explorer', icon: Database, active: true },
    { id: 'system', label: 'System Info', icon: HardDrive, active: true },
    { id: 'gan', label: 'GAN', icon: ImageIcon, active: false, badge: 'Soon' },
    { id: 'prediction', label: 'Prediction Engine', icon: CheckCircle2, active: false, badge: 'Soon' },
  ];

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
        .sidebar { width: 240px; background-color: var(--surface); border-right: 1px solid var(--border); padding: 20px 0; display: flex; flex-direction: column; }
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
        .panel-desc { color: var(--muted); font-size: 0.95rem; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 20px; }
        .card-title { font-size: 1rem; font-weight: 500; margin-bottom: 15px; color: var(--accent2); display: flex; justify-content: space-between; }
        
        .upload-zone { border: 2px dashed var(--border); border-radius: 6px; padding: 40px 20px; text-align: center; cursor: pointer; transition: all 0.2s; background: rgba(30, 45, 64, 0.2); }
        .upload-zone:hover { border-color: var(--accent); background: rgba(0, 212, 255, 0.05); }
        .upload-icon { color: var(--accent); margin-bottom: 10px; width: 32px; height: 32px; }
        
        .image-preview { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 4px; border: 1px solid var(--border); }
        .btn { background: var(--accent); color: #000; border: none; padding: 10px 20px; border-radius: 4px; font-family: var(--font-ui); font-weight: 600; cursor: pointer; width: 100%; margin-top: 15px; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .metrics-strip { display: flex; gap: 20px; background: var(--surface); border: 1px solid var(--border); padding: 15px 20px; border-radius: 6px; margin-bottom: 30px; }
        .metric { display: flex; flex-direction: column; gap: 4px; }
        .metric-label { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-value { font-family: var(--font-mono); font-size: 1.2rem; color: var(--accent); }
        
        .chart-container { height: 300px; width: 100%; }
        
        .predictions-list { display: flex; flex-direction: column; gap: 10px; }
        .pred-item { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 45, 64, 0.3); padding: 10px 15px; border-radius: 4px; }
        .pred-class { font-weight: 500; text-transform: capitalize; }
        .pred-prob { font-family: var(--font-mono); color: var(--accent); }
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
        </div>
        
        <div className="main-content">
          <div className="topbar">
            <div style={{ color: 'var(--muted)' }}>Terminal / {activeView}</div>
            {status[activeView] ? (
              <div className={`status-chip ${status[activeView] === 'Trained' ? '' : 'error'}`}>
                {status[activeView] === 'Trained' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
                {status[activeView] === 'Trained' ? 'Trained ✓' : 'Not trained yet — run backend script'}
              </div>
            ) : null}
          </div>
          
          <div className="content-body">
            {(activeView === 'ae' || activeView === 'vae' || activeView === 'transformer') && (
              <div className="panel-header">
                <h1 className="panel-title">{MODEL_META[activeView].title}</h1>
                <div className="panel-desc">{MODEL_META[activeView].description}</div>
              </div>
            )}

            {activeView === 'datasets' && <DatasetExplorer />}
            {activeView === 'system' && <SystemInformation />}
            {activeView === 'model-explorer' && <ModelExplorer setActiveView={setActiveView} />}
            {activeView === 'model-comparison' && <ModelComparison />}
            {activeView === 'training' && <Training />}
            {activeView === 'evaluation' && <Evaluation />}
            {activeView === 'research' && <Research />}

            {(activeView === 'ae' || activeView === 'vae' || activeView === 'transformer') && (
              <>
            <div className="card" style={{ marginBottom: '30px' }}>
              <div className="card-title">
                {resultData || predictions
                  ? MODEL_META[activeView].resultTitle
                  : activeView === 'transformer' ? 'Classify Land-Use' : 'Upload Image'}
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
                    {loading ? 'Loading...' : 'Load Real Sample (UCMerced)'}
                  </button>
                </div>
              ) : (
                <div>
                  {!resultData && !(activeView === 'transformer' && predictions) ? (
                    <div className="grid-2" style={{ marginBottom: 0 }}>
                      {preview ? (
                        <img src={preview} className="image-preview" alt="Input" />
                      ) : (
                        <div className="image-preview" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: 'var(--muted)', fontSize: '0.85rem', padding: '10px' }}>
                          {file.name}<br />(preview unavailable for this format)
                        </div>
                      )}
                      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '15px' }}>
                        <button className="btn" onClick={handleUpload} disabled={loading || status[activeView] !== 'Trained'}>
                          {loading ? 'Processing...' : activeView === 'transformer' ? 'Run Classification' : 'Run Inference'}
                        </button>
                        <button className="btn" onClick={clearSelection} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}>Clear Selection</button>
                      </div>
                    </div>
                  ) : activeView === 'transformer' ? (
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
                        {/* First panel is always the user's own uploaded file, rendered client-side at
                            full resolution — NOT a resized/renormalized round-trip copy from the backend,
                            which can look meaningfully different from what was actually uploaded. */}
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

                      <button className="btn" onClick={clearSelection} style={{ maxWidth: '200px', margin: '0 auto' }}>Upload Another</button>
                    </div>
                  )}
                </div>
              )}
              <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept="image/*,.tif,.tiff" onChange={handleFileChange} />
            </div>

            {activeView === 'transformer' && (
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
                        const res = await fetch(`${API_URL}/transformer/query`, {
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
                        const res = await fetch(`${API_URL}/transformer/stats`);
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

            {(activeView === 'ae' || activeView === 'vae') && metrics && (
              <div className="metrics-strip">
                {activeView === 'ae' ? (
                  <>
                    <div className="metric"><span className="metric-label">MSE Loss</span><span className="metric-value">{Number(metrics.mse).toFixed(5)}</span></div>
                    <div className="metric"><span className="metric-label">PSNR</span><span className="metric-value">{Number(metrics.psnr).toFixed(2)} dB</span></div>
                  </>
                ) : (
                  <>
                    <div className="metric"><span className="metric-label">μ Mean</span><span className="metric-value">{Number(metrics.mu).toFixed(5)}</span></div>
                    <div className="metric"><span className="metric-label">log(var) Mean</span><span className="metric-value">{Number(metrics.logvar).toFixed(5)}</span></div>
                    {metrics.anomalyLevel && (
                      <div className="metric">
                        <span className="metric-label">Anomaly Check</span>
                        <span
                          className="metric-value"
                          style={{
                            color: metrics.anomalyLevel === 'Typical' ? 'var(--success)'
                              : metrics.anomalyLevel === 'Unusual' ? '#FFB84D' : '#FF5252'
                          }}
                        >
                          {metrics.anomalyLevel} (z={Number(metrics.anomalyScore).toFixed(2)})
                        </span>
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
            {activeView === 'vae' && metrics?.anomalyLevel && (
              <div style={{ color: 'var(--muted)', fontSize: '0.8rem', marginTop: '-20px', marginBottom: '30px', padding: '0 5px' }}>
                Anomaly Check compares this tile's reconstruction error against a baseline computed from 300 real UCMerced tiles.
                A land-use pattern the VAE reconstructs far worse than that baseline is one that doesn't match patterns it learned from
                real data — a candidate signal for unexpected land-cover change, informal construction, or an out-of-domain image.
              </div>
            )}

            {history.length > 0 && (
              <div className="card">
                <div className="card-title">Training Loss Curve</div>
                <div className="chart-container">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={history}>
                      <XAxis dataKey="epoch" stroke="var(--muted)" fontSize={12} />
                      <YAxis stroke="var(--muted)" fontSize={12} domain={['auto', 'auto']} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '6px' }}
                        itemStyle={{ color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}
                      />
                      <Line type="monotone" dataKey="loss" stroke="var(--accent)" strokeWidth={2} dot={{ r: 4, fill: 'var(--surface)', stroke: 'var(--accent)' }} activeDot={{ r: 6 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
            
            {history.length === 0 && status[activeView] === 'Trained' && (
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
