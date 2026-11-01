import React, { useState, useEffect, useRef, lazy, Suspense } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {
  Upload,
  CheckCircle2,
  AlertCircle,
  Cpu,
  FileText,
  Layers,
  Image as ImageIcon,
  Database,
  HardDrive,
  ShieldCheck,
  Sparkles,
  KeyRound,
  BookOpen,
  Sun,
  Moon,
  Loader2,
  X,
} from 'lucide-react';
import { apiFetch } from './lib/api';
import { useAppStore, ViewType } from './store';
import { PageSkeleton, ShimmerBox } from './components/Skeleton';
import { LazyErrorBoundary } from './components/LazyErrorBoundary';

// -----------------------------------------------------------------------------
// Industry-Grade Code Splitting: Lazy-Loaded Page Components
// -----------------------------------------------------------------------------
const Landing = lazy(() => import('./pages/Landing'));
const DatasetExplorer = lazy(() => import('./pages/DatasetExplorer'));
const SystemInformation = lazy(() => import('./pages/SystemInformation'));
const ModelExplorer = lazy(() => import('./pages/ModelExplorer'));
const ModelComparison = lazy(() => import('./pages/ModelComparison'));
const Training = lazy(() => import('./pages/Training'));
const Evaluation = lazy(() => import('./pages/Evaluation'));
const Research = lazy(() => import('./pages/Research'));
const PlanGenerator = lazy(() => import('./pages/PlanGenerator'));
const Governance = lazy(() => import('./pages/Governance'));
const GAN = lazy(() => import('./pages/GAN'));
const Diffusion = lazy(() => import('./pages/Diffusion'));
const Glossary = lazy(() => import('./pages/Glossary'));
const FutureScope = lazy(() => import('./pages/FutureScope'));
const SystemArchitecture = lazy(() => import('./pages/SystemArchitecture'));

// Architecture Deep-Dive Pages
const VAEArchitecture = lazy(() => import('./pages/VAEArchitecture'));
const AEArchitecture = lazy(() => import('./pages/AEArchitecture'));
const GANArchitecture = lazy(() => import('./pages/GANArchitecture'));
const TransformerArchitecture = lazy(() => import('./pages/TransformerArchitecture'));
const ClassifierArchitecture = lazy(() => import('./pages/ClassifierArchitecture'));

// Intelligent Preloader Map: Prefetch modules on user hover for instant transitions
const PRELOAD_MAP: Partial<Record<ViewType, () => Promise<any>>> = {
  landing: () => import('./pages/Landing'),
  evaluation: () => import('./pages/Evaluation'),
  diffusion: () => import('./pages/Diffusion'),
  gan: () => import('./pages/GAN'),
  'plan-generator': () => import('./pages/PlanGenerator'),
  training: () => import('./pages/Training'),
  'model-comparison': () => import('./pages/ModelComparison'),
  'model-explorer': () => import('./pages/ModelExplorer'),
  research: () => import('./pages/Research'),
  datasets: () => import('./pages/DatasetExplorer'),
  system: () => import('./pages/SystemInformation'),
};

const preloadView = (view: ViewType) => {
  const loader = PRELOAD_MAP[view];
  if (loader) {
    loader().catch(() => {});
  }
};

// Image-inference views that share the interactive parcel inspection workflow
const IMAGE_VIEWS = ['ae', 'vae', 'classifier'] as const;
const isImageView = (v: ViewType) => (IMAGE_VIEWS as readonly string[]).includes(v);

// Classifier training history is stored under outputs/transformer/
const HISTORY_KEY: Record<string, string> = { ae: 'ae', vae: 'vae', classifier: 'transformer' };

const MODEL_META: Record<
  string,
  {
    title: string;
    description: string;
    resultTitle: string;
    panelLabels: string[];
    sampleEndpoint: string;
    sampleHint: string;
    inferEndpoint: string;
  }
> = {
  ae: {
    title: 'Autoencoder (Denoising U-Net)',
    description:
      'A pretrained ResNet18 encoder with skip-connected transposed-CNN decoder trained on UCMerced aerial land-use tiles (21 classes, 50 epochs, batch size 32). Reconstructs crisp structural edges from sensor noise with 29.65 dB PSNR and 0.8649 SSIM.',
    resultTitle: 'Denoising Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Corrupted Input (σ=0.15)', 'Reconstructed Output'],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint:
      'Trained on UCMerced aerial tiles (roads, buildings, agricultural, etc.) — upload an aerial image, or load a verified real benchmark sample below.',
    inferEndpoint: '/infer/ae',
  },
  vae: {
    title: 'Variational Autoencoder — Anomaly Detection & Latent Manifold Traversal',
    description:
      'Flags land parcels whose reconstruction error deviates from normal spatial baseline (z-score anomaly detection) and enables continuous latent interpolation between diverse zoning states (e.g. dense residential to parkland) along a 64×8×8 spatial manifold.',
    resultTitle: 'VAE Generation & Reconstruction',
    panelLabels: ['Original Input', 'Generated Latent Variation', 'Reconstruction'],
    sampleEndpoint: '/sample/ucmerced/undeveloped',
    sampleHint:
      'Trained on UCMerced aerial tiles — upload an image, or load an undeveloped real benchmark sample below to test the urbanization projection.',
    inferEndpoint: '/infer/vae',
  },
  classifier: {
    title: 'Land-Use Territorial Classifier (ResNet-18)',
    description:
      'A ResNet-18 CNN fine-tuned via transfer learning to classify aerial imagery into 21 municipal zoning categories at 98.10% validation accuracy (Macro F1: 0.9784, Validation Loss: 0.0615). Note: this is a discriminative CNN; generative language tasks are handled separately by MiniGPT.',
    resultTitle: 'Territorial Classification',
    panelLabels: [],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles — upload a parcel image, or load a benchmark sample below.',
    inferEndpoint: '/infer/classifier',
  },
};

export default function App() {
  // Global Industry-Grade Zustand Store Subscriptions
  const activeView = useAppStore((state) => state.activeView);
  const setActiveView = useAppStore((state) => state.setActiveView);
  const theme = useAppStore((state) => state.theme);
  const toggleTheme = useAppStore((state) => state.toggleTheme);
  const status = useAppStore((state) => state.status);
  const statusError = useAppStore((state) => state.statusError);
  const isStatusLoading = useAppStore((state) => state.isStatusLoading);
  const fetchStatus = useAppStore((state) => state.fetchStatus);
  const toasts = useAppStore((state) => state.toasts);
  const addToast = useAppStore((state) => state.addToast);
  const removeToast = useAppStore((state) => state.removeToast);

  // Active Inference State
  const file = useAppStore((state) => state.file);
  const preview = useAppStore((state) => state.preview);
  const resultData = useAppStore((state) => state.resultData);
  const metrics = useAppStore((state) => state.metrics);
  const predictions = useAppStore((state) => state.predictions);
  const loading = useAppStore((state) => state.loading);
  const setLoading = useAppStore((state) => state.setLoading);
  const setFile = useAppStore((state) => state.setFile);
  const setInferenceResult = useAppStore((state) => state.setInferenceResult);
  const clearSelection = useAppStore((state) => state.clearInference);

  // VAE Interactive Sub-features
  const interpImg = useAppStore((state) => state.interpImg);
  const interpLoading = useAppStore((state) => state.interpLoading);
  const setInterpResult = useAppStore((state) => state.setInterpResult);

  const randomGenImg = useAppStore((state) => state.randomGenImg);
  const randomGenLoading = useAppStore((state) => state.randomGenLoading);
  const randomGenError = useAppStore((state) => state.randomGenError);
  const setRandomGenResult = useAppStore((state) => state.setRandomGenResult);

  const urbanizeImg = useAppStore((state) => state.urbanizeImg);
  const urbanizeLoading = useAppStore((state) => state.urbanizeLoading);
  const urbanizeError = useAppStore((state) => state.urbanizeError);
  const urbanizeIntensity = useAppStore((state) => state.urbanizeIntensity);
  const setUrbanizeResult = useAppStore((state) => state.setUrbanizeResult);
  const setUrbanizeIntensity = useAppStore((state) => state.setUrbanizeIntensity);

  // Local component states
  const [history, setHistory] = useState<any[]>([]);
  const [apiKeyInput, setApiKeyInput] = useState(useAppStore.getState().apiKey);
  const [ragLoading, setRagLoading] = useState(false);
  const [ragResponse, setRagResponse] = useState<string | null>(null);
  const [puneStats, setPuneStats] = useState<any | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Keep theme attribute in sync with document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Initial and periodic health-check polling
  useEffect(() => {
    fetchStatus();
    const timer = window.setInterval(fetchStatus, 8000);
    return () => window.clearInterval(timer);
  }, [fetchStatus]);

  // Load model training curves when active image view changes
  useEffect(() => {
    const key = HISTORY_KEY[activeView];
    if (key) {
      apiFetch(`/history/${key}`)
        .then((res) => (res.ok ? res.json() : []))
        .then((data) => setHistory(Array.isArray(data) ? data : []))
        .catch(() => setHistory([]));
    }
  }, [activeView]);

  // Handle local file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      if (f.name.toLowerCase().endsWith('.tif') || f.name.toLowerCase().endsWith('.tiff')) {
        setFile(f, '');
      } else {
        setFile(f);
      }
      addToast({ type: 'info', message: `Loaded file: ${f.name}` });
    }
  };

  // Load verified benchmark sample from dataset
  const handleLoadSample = async () => {
    const meta = MODEL_META[activeView];
    if (!meta) return;
    setLoading(true);
    try {
      const res = await apiFetch(meta.sampleEndpoint);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const cls = res.headers.get('X-Class') || 'sample';
      const f = new File([blob], `${cls}.jpg`, { type: 'image/jpeg' });
      setFile(f);
      addToast({ type: 'success', message: `Loaded benchmark sample (${cls})` });
    } catch (err: any) {
      addToast({ type: 'error', message: 'Failed to load real sample image.' });
    } finally {
      setLoading(false);
    }
  };

  // Run neural model inference
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiFetch(MODEL_META[activeView].inferEndpoint, {
        method: 'POST',
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        if (activeView === 'classifier') {
          setInferenceResult(null, null, data.predictions);
          addToast({ type: 'success', message: 'Territorial classification complete.' });
        } else {
          let metricObj: any = null;
          if (activeView === 'ae') {
            metricObj = { mse: data.mse, psnr: data.psnr };
          } else if (activeView === 'vae') {
            metricObj = {
              mu: data.mu,
              logvar: data.logvar,
              kl: data.kl,
              klPerDim: data.kl_per_dim,
              mse: data.mse,
              generatedMse: data.generated_mse_vs_input,
              generationAlpha: data.generation_alpha,
              anomalyScore: data.anomaly_score,
              anomalyLevel: data.anomaly_level,
              anomalyPercentDiff: data.anomaly_percent_diff,
              anomalyReason: data.anomaly_reason,
            };
          }
          setInferenceResult(data, metricObj);
          addToast({ type: 'success', message: 'Reconstruction inference complete.' });
        }
      } else {
        const errMsg = res.status === 401 ? 'API key required — configure in sidebar.' : await res.text();
        setInferenceResult(null, { error: errMsg });
        addToast({ type: 'error', message: errMsg });
      }
    } catch (err: any) {
      setInferenceResult(null, { error: String(err) });
      addToast({ type: 'error', message: 'Inference request failed. Is backend online?' });
    } finally {
      setLoading(false);
    }
  };

  // VAE Latent Traversal Interpolation
  const handleInterpolate = async () => {
    if (!file) return;
    setInterpResult(null, true, null);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await apiFetch('/infer/vae/interpolate', { method: 'POST', body: formData });
      if (res.ok) {
        const blob = await res.blob();
        setInterpResult(URL.createObjectURL(blob), false, null);
        addToast({ type: 'success', message: 'Latent interpolation generated.' });
      } else {
        const err = await res.text();
        setInterpResult(null, false, err);
        addToast({ type: 'error', message: 'Interpolation failed.' });
      }
    } catch (err: any) {
      setInterpResult(null, false, String(err));
    }
  };

  // VAE Scenario Urbanization Projection
  const handleUrbanize = async () => {
    if (!file) return;
    setUrbanizeResult(null, true, null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('alpha', String(urbanizeIntensity));
    try {
      const res = await apiFetch('/infer/vae/urbanize', { method: 'POST', body: formData });
      if (!res.ok) {
        const err = res.status === 401 ? 'API key required — configure in sidebar.' : await res.text();
        setUrbanizeResult(null, false, err);
        addToast({ type: 'error', message: err });
        return;
      }
      const data = await res.json();
      setUrbanizeResult(`data:image/jpeg;base64,${data.urbanized}`, false, null);
      addToast({ type: 'success', message: 'Urbanization projection generated.' });
    } catch (err: any) {
      setUrbanizeResult(null, false, String(err));
    }
  };

  // VAE Random Learned-Manifold Sample Generation
  const handleGenerateRandom = async () => {
    setRandomGenResult(null, true, null);
    try {
      const res = await apiFetch('/generate/vae/random', { method: 'POST' });
      if (!res.ok) {
        const err = res.status === 401 ? 'API key required — configure in sidebar.' : await res.text();
        setRandomGenResult(null, false, err);
        addToast({ type: 'error', message: err });
        return;
      }
      const data = await res.json();
      setRandomGenResult(`data:image/jpeg;base64,${data.generated}`, false, null);
      addToast({ type: 'success', message: 'Learned-manifold sample generated.' });
    } catch (err: any) {
      setRandomGenResult(null, false, String(err));
    }
  };

  const navItems = [
    { id: 'landing' as ViewType, label: 'Home', icon: Sparkles },
    { id: 'model-explorer' as ViewType, label: 'Model Explorer', icon: Layers },
    { id: 'model-comparison' as ViewType, label: 'Model Comparison', icon: FileText },
    { id: 'system-architecture' as ViewType, label: 'System Architecture', icon: Layers },
    { id: 'ae' as ViewType, label: 'Autoencoder', icon: Layers },
    { id: 'vae' as ViewType, label: 'VAE', icon: FileText },
    { id: 'diffusion' as ViewType, label: 'Diffusion Generator', icon: Sparkles },
    { id: 'plan-generator' as ViewType, label: 'Urban Plan Generator', icon: Sparkles },
    { id: 'classifier' as ViewType, label: 'Land-Use Classifier', icon: Cpu },
    { id: 'training' as ViewType, label: 'Training', icon: Cpu },
    { id: 'evaluation' as ViewType, label: 'Evaluation', icon: FileText },
    { id: 'research' as ViewType, label: 'Research & Innovation', icon: BookOpen, badge: 'Scoping' },
    { id: 'glossary' as ViewType, label: 'Glossary', icon: FileText },
    { id: 'future-scope' as ViewType, label: 'Future Scope', icon: Sparkles },
    { id: 'governance' as ViewType, label: 'Governance', icon: ShieldCheck },
    { id: 'datasets' as ViewType, label: 'Dataset Explorer', icon: Database },
    { id: 'system' as ViewType, label: 'System Info', icon: HardDrive },
    { id: 'gan' as ViewType, label: 'GAN Generator', icon: ImageIcon },
  ];

  const statusKey =
    activeView === 'plan-generator' ? 'gpt' : activeView === 'classifier' ? 'transformer' : activeView;

  // View dispatcher rendered inside LazyErrorBoundary and Suspense
  const renderCurrentView = () => {
    switch (activeView) {
      case 'landing':
        return <Landing onEnter={(v) => setActiveView(v as ViewType)} />;
      case 'ae':
        return (
          <>
            <AEArchitecture />
            {renderSharedInferenceUI()}
          </>
        );
      case 'vae':
        return (
          <>
            <VAEArchitecture />
            {renderSharedInferenceUI()}
          </>
        );
      case 'classifier':
        return (
          <>
            <ClassifierArchitecture />
            {renderSharedInferenceUI()}
          </>
        );
      case 'diffusion':
        return <Diffusion />;
      case 'gan':
        return (
          <>
            <GANArchitecture />
            <GAN isGanTrained={status['gan'] === 'Trained'} />
          </>
        );
      case 'plan-generator':
        return (
          <>
            <TransformerArchitecture />
            <PlanGenerator />
          </>
        );
      case 'training':
        return <Training />;
      case 'evaluation':
        return <Evaluation />;
      case 'model-comparison':
        return <ModelComparison />;
      case 'model-explorer':
        return <ModelExplorer setActiveView={setActiveView} />;
      case 'system-architecture':
        return <SystemArchitecture />;
      case 'datasets':
        return <DatasetExplorer />;
      case 'system':
        return <SystemInformation />;
      case 'governance':
        return <Governance />;
      case 'research':
        return <Research />;
      case 'glossary':
        return <Glossary />;
      case 'future-scope':
        return <FutureScope />;
      default:
        return <Landing onEnter={(v) => setActiveView(v as ViewType)} />;
    }
  };

  // Shared Upload & Inference Workspace for AE, VAE, and Classifier
  const renderSharedInferenceUI = () => (
    <>
      <div className="card" style={{ marginBottom: '30px' }}>
        <div className="card-title">
          {resultData || predictions
            ? MODEL_META[activeView].resultTitle
            : activeView === 'classifier'
            ? 'Classify Land-Use'
            : 'Upload Image'}
        </div>
        {!file ? (
          <div>
            <div className="upload-zone" onClick={() => fileInputRef.current?.click()}>
              <Upload className="upload-icon" />
              <p style={{ color: 'var(--text)' }}>Click or drag aerial tile to inspect</p>
              <p style={{ color: 'var(--muted)', fontSize: '0.85rem', marginTop: '10px' }}>
                {MODEL_META[activeView].sampleHint}
              </p>
            </div>
            <button
              className="btn"
              style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}
              onClick={handleLoadSample}
              disabled={loading}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                  <Loader2 size={16} className="animate-spin" /> Fetching Benchmark Sample...
                </span>
              ) : activeView === 'vae' ? (
                'Load Real Sample (Undeveloped)'
              ) : (
                'Load Real Sample (UCMerced)'
              )}
            </button>
          </div>
        ) : (
          <div>
            {!resultData && !(activeView === 'classifier' && predictions) ? (
              <div className="grid-2" style={{ marginBottom: 0 }}>
                {preview ? (
                  <img src={preview} className="image-preview" alt="Input Tile" />
                ) : (
                  <div
                    className="image-preview"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      textAlign: 'center',
                      color: 'var(--muted)',
                      fontSize: '0.85rem',
                      padding: '10px',
                    }}
                  >
                    {file.name}
                    <br />
                    (preview unavailable for raw format)
                  </div>
                )}
                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '15px' }}>
                  <button
                    className="btn"
                    onClick={handleUpload}
                    disabled={loading || status[statusKey] === 'Not trained'}
                  >
                    {loading ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                        <Loader2 size={16} className="animate-spin" /> Running Neural Inference...
                      </span>
                    ) : activeView === 'classifier' ? (
                      'Run Classification'
                    ) : (
                      'Run Inference'
                    )}
                  </button>
                  <button
                    className="btn"
                    onClick={clearSelection}
                    style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}
                  >
                    Clear Selection
                  </button>
                </div>
              </div>
            ) : activeView === 'classifier' ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div className="grid-2" style={{ marginBottom: 0 }}>
                  {preview ? (
                    <img src={preview} className="image-preview" alt="Input" />
                  ) : (
                    <div
                      className="image-preview"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--muted)',
                        fontSize: '0.85rem',
                      }}
                    >
                      {file.name}
                    </div>
                  )}
                  <div className="predictions-list">
                    {Array.isArray(predictions) &&
                      predictions.map((p: any, i: number) => (
                        <div className="pred-item" key={i}>
                          <span className="pred-class">{p.class}</span>
                          <span className="pred-prob">{Number(p.confidence).toFixed(2)}%</span>
                        </div>
                      ))}
                  </div>
                </div>
                <button
                  className="btn"
                  onClick={clearSelection}
                  style={{ maxWidth: '200px', margin: '0 auto' }}
                >
                  Classify Another
                </button>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    padding: '0 10px',
                    color: 'var(--muted)',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}
                >
                  {MODEL_META[activeView].panelLabels.map((label, i) => (
                    <div key={i} style={{ flex: 1, textAlign: 'center' }}>
                      {label}
                    </div>
                  ))}
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  {preview ? (
                    <img
                      src={preview}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                      }}
                      alt="Original"
                    />
                  ) : (
                    <div
                      style={{
                        flex: 1,
                        aspectRatio: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        textAlign: 'center',
                        color: 'var(--muted)',
                        fontSize: '0.8rem',
                        padding: '10px',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                      }}
                    >
                      {file?.name}
                      <br />
                      (preview unavailable)
                    </div>
                  )}
                  {activeView === 'ae' && resultData?.noisy && (
                    <img
                      src={`data:image/jpeg;base64,${resultData.noisy}`}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                      }}
                      alt="Noisy"
                    />
                  )}
                  {activeView === 'vae' && resultData?.generated && (
                    <img
                      src={`data:image/jpeg;base64,${resultData.generated}`}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                      }}
                      alt="Generated VAE variation"
                    />
                  )}
                  {resultData?.reconstructed && (
                    <img
                      src={`data:image/jpeg;base64,${resultData.reconstructed}`}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                      }}
                      alt="Reconstructed"
                    />
                  )}
                </div>

                {/* VAE Anomaly Detection Callout */}
                {activeView === 'vae' && metrics?.anomalyLevel && (
                  <div
                    style={{
                      padding: '18px 22px',
                      borderRadius: 8,
                      background:
                        metrics.anomalyLevel === 'Typical'
                          ? 'var(--success-wash)'
                          : metrics.anomalyLevel === 'Unusual'
                          ? 'var(--warn-wash)'
                          : 'var(--danger-wash)',
                      border: `1px solid ${
                        metrics.anomalyLevel === 'Typical'
                          ? 'var(--success)'
                          : metrics.anomalyLevel === 'Unusual'
                          ? 'var(--warn)'
                          : 'var(--danger)'
                      }`,
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: 14, flexWrap: 'wrap', marginBottom: 8 }}>
                      <span
                        style={{
                          fontSize: '1.3rem',
                          fontWeight: 700,
                          fontFamily: 'var(--font-mono)',
                          color:
                            metrics.anomalyLevel === 'Typical'
                              ? 'var(--success)'
                              : metrics.anomalyLevel === 'Unusual'
                              ? 'var(--warn)'
                              : 'var(--danger)',
                        }}
                      >
                        {metrics.anomalyLevel === 'Typical' ? '✓' : '⚠'} {metrics.anomalyLevel.toUpperCase()}
                      </span>
                      {metrics.anomalyPercentDiff != null && (
                        <span style={{ fontSize: '1.1rem', fontFamily: 'var(--font-mono)', color: 'var(--text)' }}>
                          {metrics.anomalyPercentDiff > 0 ? '+' : ''}
                          {Number(metrics.anomalyPercentDiff).toFixed(0)}% reconstruction error vs. normal
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

                {/* Quantitative Metric Strip */}
                {metrics && (
                  <div className="metrics-strip">
                    {activeView === 'ae' ? (
                      <>
                        <div className="metric">
                          <span className="metric-label">MSE Loss</span>
                          <span className="metric-value">{Number(metrics.mse).toFixed(5)}</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">PSNR</span>
                          <span className="metric-value">{Number(metrics.psnr).toFixed(2)} dB</span>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="metric">
                          <span className="metric-label">μ Mean</span>
                          <span className="metric-value">{Number(metrics.mu).toFixed(4)}</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">log(σ²) Mean</span>
                          <span className="metric-value">{Number(metrics.logvar).toFixed(4)}</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">KL Divergence</span>
                          <span className="metric-value">{Number(metrics.kl).toFixed(2)} nats</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">Recon MSE</span>
                          <span className="metric-value">{Number(metrics.mse).toFixed(5)}</span>
                        </div>
                      </>
                    )}
                  </div>
                )}
                <button
                  className="btn"
                  onClick={clearSelection}
                  style={{ maxWidth: '200px', margin: '10px auto 0' }}
                >
                  Reset Parcel Selection
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* VAE Latent Traversal Controls */}
      {activeView === 'vae' && file && resultData && (
        <div className="grid-2">
          <div className="card">
            <div className="card-title">Latent Space Interpolation</div>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', lineHeight: 1.5, marginBottom: '15px' }}>
              Samples an alternate parcel from the dataset, encodes both into the 64×8×8 spatial latent space,
              and renders a continuous 7-frame transition along the learned manifold.
            </p>
            <button
              className="btn"
              onClick={handleInterpolate}
              disabled={interpLoading || status[statusKey] === 'Not trained'}
            >
              {interpLoading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                  <Loader2 size={16} className="animate-spin" /> Interpolating Latent Vectors...
                </span>
              ) : (
                'Generate Latent Interpolation'
              )}
            </button>
            {interpLoading && <ShimmerBox height={140} style={{ marginTop: 15 }} />}
            {interpImg && (
              <div style={{ marginTop: '15px' }}>
                <img
                  src={interpImg}
                  style={{ width: '100%', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }}
                  alt="Interpolation Sequence"
                />
              </div>
            )}
          </div>

          <div className="card">
            <div className="card-title">Scenario Urbanization Projection</div>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', lineHeight: 1.5, marginBottom: '15px' }}>
              Blends the uploaded tile’s latent code with an empirical developed-urban direction vector.
            </p>
            <div style={{ marginBottom: '15px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--muted)' }}>Urbanization Intensity (α)</span>
                <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent)' }}>
                  {urbanizeIntensity.toFixed(2)}
                </span>
              </div>
              <input
                type="range"
                min="0.1"
                max="1.5"
                step="0.05"
                value={urbanizeIntensity}
                onChange={(e) => setUrbanizeIntensity(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent)' }}
              />
            </div>
            <button
              className="btn"
              onClick={handleUrbanize}
              disabled={urbanizeLoading || status[statusKey] === 'Not trained'}
            >
              {urbanizeLoading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                  <Loader2 size={16} className="animate-spin" /> Projecting Urban Development...
                </span>
              ) : (
                'Project Development Scenario'
              )}
            </button>
            {urbanizeLoading && <ShimmerBox height={160} style={{ marginTop: 15 }} />}
            {urbanizeError && (
              <div
                style={{
                  border: '1px solid var(--danger)',
                  color: 'var(--danger)',
                  borderRadius: '4px',
                  padding: '10px 12px',
                  marginTop: '15px',
                  fontSize: '0.85rem',
                }}
              >
                {urbanizeError}
              </div>
            )}
            {urbanizeImg && (
              <div style={{ marginTop: '15px' }}>
                <img
                  src={urbanizeImg}
                  style={{ width: '100%', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }}
                  alt="Urbanized Projection"
                />
              </div>
            )}
          </div>
        </div>
      )}

      {/* VAE Random Manifold Sampler */}
      {activeView === 'vae' && (
        <div className="card" style={{ marginBottom: '30px' }}>
          <div className="card-title">Generate Random Learned-Manifold Sample</div>
          <p style={{ color: 'var(--muted)', fontSize: '0.85rem', lineHeight: 1.5, marginBottom: '15px' }}>
            Encodes two real UCMerced tiles, interpolates their learned spatial latent codes, and decodes the
            representation. This avoids prior collapse while guaranteeing identifiable geometric roads and parcels.
          </p>
          <button
            className="btn"
            style={{ maxWidth: '320px' }}
            onClick={handleGenerateRandom}
            disabled={randomGenLoading || status[statusKey] === 'Not trained'}
          >
            {randomGenLoading ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                <Loader2 size={16} className="animate-spin" /> Sampling Manifold...
              </span>
            ) : (
              'Generate Random Sample'
            )}
          </button>
          {randomGenLoading && <ShimmerBox height={180} style={{ marginTop: 15, maxWidth: 320 }} />}
          {randomGenError && (
            <div
              style={{
                border: '1px solid var(--danger)',
                color: 'var(--danger)',
                borderRadius: '4px',
                padding: '10px 12px',
                marginTop: '15px',
                fontSize: '0.85rem',
              }}
            >
              {randomGenError}
            </div>
          )}
          {randomGenImg && (
            <div style={{ marginTop: '15px', maxWidth: '320px' }}>
              <img
                src={randomGenImg}
                style={{ width: '100%', height: 'auto', borderRadius: '4px', border: '1px solid var(--border)' }}
                alt="Random learned-manifold sample"
              />
            </div>
          )}
        </div>
      )}

      {/* Classifier RAG Query Sandbox */}
      {activeView === 'classifier' && (
        <div className="grid-2">
          <div className="card">
            <div className="card-title">RAG Spatial Query Sandbox</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <textarea
                style={{
                  width: '100%',
                  minHeight: '100px',
                  background: 'var(--bg)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  padding: '10px',
                  fontFamily: 'var(--font-ui)',
                }}
                placeholder="Ask about Pune's ward land-use statistics..."
                id="rag-query-input"
              />
              <button
                className="btn"
                disabled={ragLoading}
                onClick={async () => {
                  const query = (document.getElementById('rag-query-input') as HTMLTextAreaElement)?.value;
                  if (!query) return;
                  setRagLoading(true);
                  try {
                    const res = await apiFetch('/transformer/query', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ query }),
                    });
                    const data = await res.json();
                    setRagResponse(data.response);
                    addToast({ type: 'success', message: 'RAG spatial query completed.' });
                  } catch (e) {
                    addToast({ type: 'error', message: 'RAG query failed.' });
                  } finally {
                    setRagLoading(false);
                  }
                }}
              >
                {ragLoading ? (
                  <span style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
                    <Loader2 size={16} className="animate-spin" /> Querying Domain Knowledge...
                  </span>
                ) : (
                  'Ask RAG Knowledge Base'
                )}
              </button>
              {ragResponse && (
                <div
                  style={{
                    padding: '15px',
                    background: 'var(--active-tint)',
                    border: '1px solid var(--accent)',
                    borderRadius: '4px',
                    color: 'var(--text)',
                  }}
                >
                  <strong>RAG Response:</strong> {ragResponse}
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <div className="card-title">Municipal Ground Truth (PUNE_STATS)</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <button
                className="btn"
                style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text)' }}
                onClick={async () => {
                  try {
                    const res = await apiFetch('/transformer/stats');
                    const data = await res.json();
                    setPuneStats(data);
                    addToast({ type: 'info', message: 'Loaded Pune municipal statistics.' });
                  } catch (e) {
                    addToast({ type: 'error', message: 'Failed to load stats.' });
                  }
                }}
              >
                Load Pune Ward Stats
              </button>
              {puneStats && (
                <pre
                  style={{
                    background: 'var(--bg)',
                    padding: '10px',
                    borderRadius: '4px',
                    overflowX: 'auto',
                    fontSize: '0.82rem',
                    fontFamily: 'var(--font-mono)',
                    maxHeight: 220,
                  }}
                >
                  {JSON.stringify(puneStats, null, 2)}
                </pre>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Model Training Curve Display */}
      {history.length > 0 && (
        <div className="card">
          <div className="card-title">Training {activeView === 'classifier' ? 'Metrics' : 'Loss'} Curve (50 Epochs)</div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <XAxis dataKey="epoch" stroke="var(--muted)" fontSize={12} />
                <YAxis yAxisId="left" stroke="var(--muted)" fontSize={12} domain={['auto', 'auto']} />
                {activeView === 'vae' && (
                  <YAxis
                    yAxisId="right"
                    orientation="right"
                    stroke="var(--accent2)"
                    fontSize={12}
                    domain={['auto', 'auto']}
                  />
                )}
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--surface)',
                    border: '1px solid var(--border)',
                    borderRadius: '6px',
                  }}
                  itemStyle={{ fontFamily: 'var(--font-mono)' }}
                />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey={activeView === 'vae' ? 'recon' : 'loss'}
                  name={activeView === 'vae' ? 'reconstruction (left)' : 'loss'}
                  stroke="var(--accent)"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 6 }}
                />
                {activeView === 'vae' && (
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="kl"
                    name="KL divergence (right)"
                    stroke="var(--accent2)"
                    strokeWidth={2}
                    dot={false}
                  />
                )}
                {activeView === 'classifier' && (
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="val_loss"
                    name="val loss"
                    stroke="var(--accent2)"
                    strokeWidth={2}
                    dot={false}
                  />
                )}
                {activeView === 'classifier' && (
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="val_accuracy"
                    name="val accuracy"
                    stroke="var(--success)"
                    strokeWidth={2}
                    dot={false}
                  />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </>
  );

  return (
    <>
      <style
        dangerouslySetInnerHTML={{
          __html: `
        :root {
          --bg: #F4F7FB;
          --surface: #FFFFFF;
          --border: #D7E0EA;
          --accent: #04788F;
          --accent2: #5B3FD1;
          --text: #16283D;
          --muted: #5B7285;
          --success: #1C8F52;
          --warn: #A66A08;
          --danger: #BB3636;
          --btn-text: #FFFFFF;
          --hover-overlay: rgba(10, 35, 60, 0.05);
          --active-tint: rgba(4, 120, 143, 0.10);
          --accent-wash-light: rgba(4, 120, 143, 0.06);
          --accent-wash: rgba(4, 120, 143, 0.12);
          --success-wash: rgba(28, 143, 82, 0.10);
          --warn-wash: rgba(166, 106, 8, 0.10);
          --danger-wash: rgba(187, 54, 54, 0.10);
          --accent2-wash: rgba(91, 63, 209, 0.10);
          --surface-inset: #EDF1F7;
          --cat-a: #0E7C9B;
          --cat-b: #6941C6;
          --cat-c: #1C8F52;
          --cat-d: #A66A08;
          --cat-e: #C2185B;
          --cat-f: #0F8A8A;
          --font-ui: 'Space Grotesk', sans-serif;
          --font-mono: 'JetBrains Mono', monospace;
        }
        :root[data-theme="dark"] {
          --bg: #080C14;
          --surface: #0F1923;
          --border: #1E2D40;
          --accent: #00D4FF;
          --accent2: #7B61FF;
          --text: #E8EDF5;
          --muted: #4A6080;
          --success: #00E676;
          --warn: #FFB84D;
          --danger: #FF5252;
          --btn-text: #000000;
          --hover-overlay: rgba(255, 255, 255, 0.05);
          --active-tint: rgba(0, 212, 255, 0.10);
          --accent-wash-light: rgba(0, 212, 255, 0.06);
          --accent-wash: rgba(0, 212, 255, 0.12);
          --success-wash: rgba(0, 230, 118, 0.10);
          --warn-wash: rgba(255, 184, 77, 0.10);
          --danger-wash: rgba(255, 82, 82, 0.10);
          --accent2-wash: rgba(123, 97, 255, 0.14);
          --surface-inset: #0A0F17;
          --cat-a: #00D4FF;
          --cat-b: #9D85FF;
          --cat-c: #00E676;
          --cat-d: #FFB300;
          --cat-e: #FF4081;
          --cat-f: #26C6DA;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg); color: var(--text); font-family: var(--font-ui); }
        .app-container { display: flex; height: 100vh; overflow: hidden; }
        .sidebar { width: 260px; background-color: var(--surface); border-right: 1px solid var(--border); display: flex; flexDirection: column; }
        .logo-area { padding: 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; cursor: pointer; }
        .logo-title { font-weight: 700; font-size: 1.15rem; letter-spacing: -0.02em; }
        .logo-subtitle { font-size: 0.75rem; color: var(--muted); }
        .nav-links { flex: 1; overflow-y: auto; padding: 15px 10px; display: flex; flex-direction: column; gap: 4px; }
        .nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 6px; color: var(--muted); cursor: pointer; font-size: 0.9rem; font-weight: 500; text-decoration: none; border: none; background: transparent; width: 100%; text-align: left; }
        .nav-item:hover { color: var(--text); background-color: var(--hover-overlay); }
        .nav-item.active { color: var(--accent); background-color: var(--active-tint); font-weight: 600; }
        .nav-badge { margin-left: auto; font-size: 0.68rem; padding: 2px 6px; border-radius: 4px; background: var(--accent2-wash); color: var(--accent2); font-weight: 600; text-transform: uppercase; }
        .main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; position: relative; }
        .topbar { padding: 15px 30px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background-color: var(--surface); }
        .status-badge { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; padding: 6px 12px; border-radius: 20px; font-weight: 500; }
        .status-badge.trained { background-color: var(--success-wash); color: var(--success); }
        .status-badge.nottrained { background-color: var(--warn-wash); color: var(--warn); }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; background-color: currentColor; }
        .theme-toggle { background: transparent; border: 1px solid var(--border); color: var(--text); padding: 7px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .theme-toggle:hover { background-color: var(--hover-overlay); }
        .content-body { padding: 30px; max-width: 1200px; margin: 0 auto; width: 100%; flex: 1; }
        .panel-header { margin-bottom: 30px; }
        .panel-title { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 8px; }
        .panel-desc { color: var(--muted); font-size: 0.95rem; line-height: 1.5; }
        .card { background-color: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-bottom: 24px; }
        .card-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
        @media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
        .upload-zone { border: 2px dashed var(--border); border-radius: 8px; padding: 40px; text-align: center; cursor: pointer; background: var(--bg); transition: border-color 0.2s, background-color 0.2s; margin-bottom: 16px; }
        .upload-zone:hover { border-color: var(--accent); background-color: var(--hover-overlay); }
        .upload-icon { width: 44px; height: 44px; color: var(--accent); margin: 0 auto 12px; }
        .btn { width: 100%; background-color: var(--accent); color: var(--btn-text); border: none; border-radius: 6px; padding: 11px 18px; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.15s ease; margin-top: 10px; }
        .btn:hover:not(:disabled) { opacity: 0.92; transform: translateY(-1px); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .image-preview { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 6px; border: 1px solid var(--border); }
        .metrics-strip { display: flex; gap: 16px; flex-wrap: wrap; background: var(--surface-inset); border: 1px solid var(--border); padding: 14px 18px; border-radius: 6px; margin-top: 15px; }
        .metric { display: flex; flex-direction: column; }
        .metric-label { font-size: 0.72rem; text-transform: uppercase; color: var(--muted); letter-spacing: 0.05em; margin-bottom: 4px; }
        .metric-value { font-family: var(--font-mono); font-size: 1.25rem; font-weight: 700; color: var(--text); }
        .chart-container { height: 300px; width: 100%; }
        .predictions-list { display: flex; flex-direction: column; gap: 8px; justify-content: center; }
        .pred-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--surface-inset); border-radius: 4px; border: 1px solid var(--border); }
        .pred-class { font-weight: 500; font-size: 0.9rem; }
        .pred-prob { font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--accent); }
      `,
        }}
      />

      <div className="app-container">
        {/* Left Navigation Sidebar */}
        <aside className="sidebar">
          <div className="logo-area" onClick={() => setActiveView('landing')}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: 6,
                background: 'var(--accent)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--btn-text)',
                fontWeight: 700,
              }}
            >
              UG
            </div>
            <div>
              <div className="logo-title">UrbanGen AI</div>
              <div className="logo-subtitle">Multi-Model Remote Sensing</div>
            </div>
          </div>

          <nav className="nav-links">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              return (
                <button
                  key={item.id}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                  onClick={() => setActiveView(item.id)}
                  onMouseEnter={() => preloadView(item.id)}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                  {item.badge && <span className="nav-badge">{item.badge}</span>}
                </button>
              );
            })}
          </nav>

          {/* Sidebar Footer: API Key Configuration */}
          <div style={{ padding: '15px', borderTop: '1px solid var(--border)', fontSize: '0.8rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8, color: 'var(--muted)' }}>
              <KeyRound size={14} />
              <span>Edge API Gateway Key</span>
            </div>
            <input
              type="password"
              placeholder="URBANGEN_API_KEY"
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              onBlur={() => {
                useAppStore.getState().setApiKey(apiKeyInput);
                addToast({ type: 'info', message: 'API key preference updated.' });
              }}
              style={{
                width: '100%',
                background: 'var(--bg)',
                color: 'var(--text)',
                border: '1px solid var(--border)',
                borderRadius: 4,
                padding: '6px 8px',
                fontSize: '0.78rem',
                fontFamily: 'var(--font-mono)',
              }}
            />
          </div>
        </aside>

        {/* Main Content View Area */}
        <div className="main-content">
          {/* Top Bar with Live Model State & Theme Switcher */}
          <header className="topbar">
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>Active Pipeline:</span>
              <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                {isImageView(activeView) ? MODEL_META[activeView].title : activeView.toUpperCase()}
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              {statusKey in status ? (
                <div className={`status-badge ${status[statusKey] === 'Trained' ? 'trained' : 'nottrained'}`}>
                  <span
                    className={`status-dot ${status[statusKey] === 'Trained' ? 'status-badge-active' : ''}`}
                  />
                  <span>
                    {status[statusKey] === 'Trained' ? 'Model Checkpoint Active' : 'Model Not Trained'}
                  </span>
                </div>
              ) : isStatusLoading ? (
                <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Checking hardware status...</div>
              ) : null}

              <button
                className="theme-toggle"
                onClick={toggleTheme}
                title={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
                aria-label="Toggle visual theme"
              >
                {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
              </button>
            </div>
          </header>

          {/* Dynamic Content Body with Error Boundary & Lazy Suspense */}
          <main className="content-body">
            {statusError && (
              <div
                style={{
                  border: '1px solid var(--danger)',
                  color: 'var(--danger)',
                  background: 'var(--danger-wash)',
                  borderRadius: '6px',
                  padding: '12px 16px',
                  marginBottom: '20px',
                  fontSize: '0.85rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                }}
              >
                <AlertCircle size={18} />
                <span>{statusError}</span>
              </div>
            )}

            {isImageView(activeView) && (
              <div className="panel-header">
                <h1 className="panel-title">{MODEL_META[activeView].title}</h1>
                <div className="panel-desc">{MODEL_META[activeView].description}</div>
              </div>
            )}

            {/* Error-guarded & Code-split Page Rendering */}
            <LazyErrorBoundary onReset={() => setActiveView('landing')}>
              <Suspense fallback={<PageSkeleton view={activeView} />}>
                <div className="page-enter" key={activeView}>
                  {renderCurrentView()}
                </div>
              </Suspense>
            </LazyErrorBoundary>
          </main>
        </div>
      </div>

      {/* Hidden File Input for Native File Dialogs */}
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        accept="image/*,.tif,.tiff"
        onChange={handleFileChange}
      />

      {/* Floating Reactive Toast Notifications */}
      {toasts.length > 0 && (
        <aside
          style={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            zIndex: 9999,
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
            maxWidth: 380,
          }}
          aria-live="polite"
        >
          {toasts.map((t) => (
            <div
              key={t.id}
              className="toast-item"
              onClick={() => removeToast(t.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '12px 16px',
                borderRadius: 6,
                background: 'var(--surface)',
                color: 'var(--text)',
                border: `1px solid ${
                  t.type === 'success'
                    ? 'var(--success)'
                    : t.type === 'error'
                    ? 'var(--danger)'
                    : t.type === 'warn'
                    ? 'var(--warn)'
                    : 'var(--accent)'
                }`,
                boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
                fontSize: '0.85rem',
                cursor: 'pointer',
              }}
            >
              {t.type === 'success' ? (
                <CheckCircle2 size={16} color="var(--success)" />
              ) : t.type === 'error' ? (
                <AlertCircle size={16} color="var(--danger)" />
              ) : (
                <Sparkles size={16} color="var(--accent)" />
              )}
              <span style={{ flex: 1 }}>{t.message}</span>
              <X size={14} color="var(--muted)" />
            </div>
          ))}
        </aside>
      )}
    </>
  );
}
