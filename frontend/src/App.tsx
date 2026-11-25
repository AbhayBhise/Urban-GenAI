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
  Presentation,
  Menu,
} from 'lucide-react';
import { apiFetch, b64ToBlob } from './lib/api';
import { SAMPLE_TILES } from './lib/sampleData';
import { TRAINING_HISTORIES } from './lib/trainingHistoryData';
import InferenceTrace from './components/InferenceTrace';
import ModelUseCaseCard from './components/ModelUseCaseCard';
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
const Poster = lazy(() => import('./pages/Poster'));

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
  poster: () => import('./pages/Poster'),
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
    datasetRole: string;
    inferenceAction: string;
    projectValue: string;
  }
> = {
  ae: {
    title: 'Denoising Autoencoder — Satellite Image Cleaner',
    description:
      'Cleans noisy or grainy satellite photos so roads, roofs, and trees look sharp again before other models analyze them (29.65 dB PSNR, 0.8649 SSIM).',
    resultTitle: 'Denoising Reconstruction',
    panelLabels: ['Original (Your Upload)', 'Noisy Input (σ=0.15)', 'Cleaned Output'],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint:
      'Trained on UCMerced aerial tiles (roads, buildings, farms, etc.) — upload an aerial photo or load a real sample below.',
    inferEndpoint: '/infer/ae',
    datasetRole:
      'Learned from 2,100 real aerial photos (21 land-use types) with added static/sensor noise so it knows how to remove grain while keeping real buildings and roads intact.',
    inferenceAction:
      'Adds simulated sensor noise to your image, compresses it, and rebuilds a clean version — then shows the reconstruction error (MSE) and clarity score (PSNR).',
    projectValue:
      'Acts as the cleanup step in UrbanGen AI so blurry or noisy satellite tiles are restored before land-use classification or planning.',
  },
  vae: {
    title: 'Spatial β-VAE — Anomaly Detector & Land-Use Explorer',
    description:
      'Checks whether a satellite tile looks normal or unusual compared to 294 real land-use tiles, and lets you blend tiles or preview how undeveloped land could look when urbanized.',
    resultTitle: 'VAE Reconstruction & Anomaly Check',
    panelLabels: ['Original Input', 'Blended Variation', 'VAE Reconstruction'],
    sampleEndpoint: '/sample/ucmerced/undeveloped',
    sampleHint:
      'Trained on UCMerced aerial tiles — upload an image or load an undeveloped land sample below to test anomaly detection and urbanization preview.',
    inferEndpoint: '/infer/vae',
    datasetRole:
      'Learned what "normal" aerial tiles look like across 21 land-use categories, setting a 294-tile baseline for normal vs. unusual terrain.',
    inferenceAction:
      'Rebuilds your uploaded tile, scores how unusual it is (Typical, Unusual, or Highly Anomalous), and lets you blend it with other tiles or preview urbanization.',
    projectValue:
      'Helps city planners quickly spot unexpected changes (like irregular construction or unusual terrain) and preview gradual land-use transitions.',
  },
  classifier: {
    title: 'Land-Use Classifier — Automatic Zoning Detector',
    description:
      'Identifies what type of land is shown in an aerial photo (such as dense residential, forest, highway, or industrial) with 98.10% validation accuracy.',
    resultTitle: 'Land-Use Classification',
    panelLabels: [],
    sampleEndpoint: '/sample/ucmerced',
    sampleHint: 'Trained on UCMerced aerial tiles — upload an aerial photo or load a real sample below.',
    inferEndpoint: '/infer/classifier',
    datasetRole:
      'Trained on 21 real municipal land-use categories from the UCMerced dataset so it can recognize roads, houses, farms, water, and factories from above.',
    inferenceAction:
      'Scans your uploaded aerial photo and ranks the top 5 most likely land-use categories with confidence percentages.',
    projectValue:
      'Automates land-use mapping for city surveys and independently checks whether images created by our GAN and Diffusion models actually match the requested zone.',
  },
};

const toImageSrc = (b64?: string): string => {
  if (!b64) return '';
  if (b64.startsWith('data:') || b64.startsWith('blob:') || b64.startsWith('http')) {
    return b64;
  }
  return `data:image/jpeg;base64,${b64}`;
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
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [inferenceStep, setInferenceStep] = useState(0);
  const [inferenceExecutionInfo, setInferenceExecutionInfo] = useState<{
    status: 'success' | 'error';
    latencyMs?: number;
    method?: string;
    errorMessage?: string;
  } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Close mobile navigation drawer on resize to desktop or on Escape key
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 900 && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [mobileMenuOpen]);

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
        .then((data) => setHistory(Array.isArray(data) && data.length > 0 ? data : (TRAINING_HISTORIES[key] || [])))
        .catch(() => setHistory(TRAINING_HISTORIES[key] || []));
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
      const cls = res.headers.get('X-Class') || (activeView === 'vae' ? 'agricultural' : 'denseresidential');
      const f = new File([blob], `${cls}.jpg`, { type: 'image/jpeg' });
      setFile(f);
      addToast({ type: 'success', message: `Loaded benchmark sample (${cls})` });
    } catch (err: any) {
      try {
        const defaultSample = activeView === 'vae' ? SAMPLE_TILES.ucmerced_undeveloped : SAMPLE_TILES.ucmerced_sample;
        const defaultClass = activeView === 'vae' ? 'agricultural' : 'denseresidential';
        const blob = b64ToBlob(defaultSample);
        const f = new File([blob], `${defaultClass}.jpg`, { type: 'image/jpeg' });
        setFile(f);
        addToast({ type: 'success', message: `Loaded benchmark sample (${defaultClass})` });
      } catch (fallbackErr) {
        addToast({ type: 'error', message: 'Failed to load real sample image.' });
      }
    } finally {
      setLoading(false);
    }
  };

  // Clear inference trace when switching views
  useEffect(() => {
    setInferenceExecutionInfo(null);
    setInferenceStep(0);
  }, [activeView]);

  // Run neural model inference (strictly live PyTorch backend — zero fake outputs)
  const handleUpload = async () => {
    if (!file) return;
    const targetView = activeView;
    const reqId = useAppStore.getState().requestId;
    setLoading(true);
    setInferenceExecutionInfo(null);
    setInferenceStep(0);
    const t0 = performance.now();

    const stepTimer1 = window.setTimeout(() => setInferenceStep(1), 180);
    const stepTimer2 = window.setTimeout(() => setInferenceStep(2), 450);

    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await apiFetch(MODEL_META[targetView].inferEndpoint, {
        method: 'POST',
        body: formData,
        timeoutMs: 25000,
      });

      if (useAppStore.getState().activeView !== targetView || useAppStore.getState().requestId !== reqId) {
        return;
      }

      setInferenceStep(3);

      if (!res.ok) {
        const errText = res.status === 401
          ? 'API key required — configure URBANGEN_API_KEY in sidebar.'
          : `Backend returned HTTP ${res.status}: ${await res.text()}`;
        setInferenceResult(null, { error: errText });
        setInferenceExecutionInfo({ status: 'error', errorMessage: errText });
        addToast({ type: 'error', message: errText });
        return;
      }

      const data = await res.json();
      const elapsedMs = typeof data.latency_ms === 'number' ? data.latency_ms : (performance.now() - t0);

      if (activeView === 'classifier') {
        setInferenceResult(null, null, data.predictions);
        setInferenceExecutionInfo({
          status: 'success',
          latencyMs: elapsedMs,
          method: 'ResNet-18 (outputs/transformer/model.pth) → 224×224 RGB → Softmax 21-class probabilities',
        });
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
        setInferenceExecutionInfo({
          status: 'success',
          latencyMs: elapsedMs,
          method: activeView === 'ae'
            ? 'DenoisingAE U-Net (outputs/ae/model.pth) → σ=0.15 noise → 128×128 reconstruction'
            : (data.generation_method || 'Spatial Beta-VAE (outputs/vae/model.pth) → μ/logvar latent manifold + z-score anomaly check'),
        });
        addToast({ type: 'success', message: 'Reconstruction inference complete.' });
      }
    } catch (err: any) {
      const msg = err?.message || String(err);
      setInferenceResult(null, { error: msg });
      setInferenceExecutionInfo({ status: 'error', errorMessage: msg });
      addToast({ type: 'error', message: 'Inference service unavailable.' });
    } finally {
      window.clearTimeout(stepTimer1);
      window.clearTimeout(stepTimer2);
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
      const res = await apiFetch('/infer/vae/interpolate', { method: 'POST', body: formData, timeoutMs: 60000 });
      if (res.ok) {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const data = await res.json();
          setInterpResult(toImageSrc(data.image || data.strip || data.interpolated), false, null);
        } else {
          const blob = await res.blob();
          setInterpResult(URL.createObjectURL(blob), false, null);
        }
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
    if (!file) {
      addToast({ type: 'info', message: 'Please upload an image or click "Load Real Sample (Undeveloped)" first.' });
      return;
    }
    setUrbanizeResult(null, true, null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('alpha', String(urbanizeIntensity));
    try {
      const res = await apiFetch('/infer/vae/urbanize', { method: 'POST', body: formData, timeoutMs: 60000 });
      if (!res.ok) {
        const err = res.status === 401 ? 'API key required — configure in sidebar.' : await res.text();
        setUrbanizeResult(null, false, err);
        addToast({ type: 'error', message: err });
        return;
      }
      const data = await res.json();
      setUrbanizeResult(toImageSrc(data.urbanized || data.image), false, null);
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
      setRandomGenResult(toImageSrc(data.generated || data.image), false, null);
      addToast({ type: 'success', message: 'Learned-manifold sample generated.' });
    } catch (err: any) {
      setRandomGenResult(null, false, String(err));
    }
  };

  const navSections = [
    {
      title: 'WORKSPACE & REFERENCE',
      items: [
        { id: 'landing' as ViewType, label: 'Home Dashboard', icon: Sparkles },
        { id: 'poster' as ViewType, label: 'Academic Poster', icon: Presentation, badge: '60M' },
        { id: 'glossary' as ViewType, label: 'Urban AI Glossary', icon: BookOpen, badge: 'Glossary' },
        { id: 'system-architecture' as ViewType, label: 'System Architecture', icon: Layers },
      ],
    },
    {
      title: 'NEURAL GENERATIVE MODELS',
      items: [
        { id: 'ae' as ViewType, label: 'Denoising Autoencoder', icon: Layers, badge: '29.6 dB' },
        { id: 'vae' as ViewType, label: 'Spatial β-VAE', icon: Layers, badge: 'Anomaly' },
        { id: 'classifier' as ViewType, label: 'Land-Use Classifier', icon: Cpu, badge: '98.1%' },
        { id: 'gan' as ViewType, label: 'Conditional DCGAN', icon: ImageIcon, badge: 'cDCGAN' },
        { id: 'diffusion' as ViewType, label: 'Diffusion Generator', icon: Sparkles, badge: 'DDPM' },
        { id: 'plan-generator' as ViewType, label: 'Urban Plan Generator', icon: FileText, badge: 'MiniGPT' },
      ],
    },
    {
      title: 'BENCHMARKS & ARCHITECTURE',
      items: [
        { id: 'model-comparison' as ViewType, label: 'Model Comparison', icon: FileText },
        { id: 'model-explorer' as ViewType, label: 'Model Explorer', icon: Layers },
        { id: 'training' as ViewType, label: 'Training Curves (50e)', icon: Cpu },
        { id: 'evaluation' as ViewType, label: 'Quantitative Evaluation', icon: FileText },
      ],
    },
    {
      title: 'MUNICIPAL & POLICY',
      items: [
        { id: 'datasets' as ViewType, label: 'Dataset Explorer', icon: Database },
        { id: 'system' as ViewType, label: 'System Hardware', icon: HardDrive },
        { id: 'governance' as ViewType, label: 'Governance & Ethics', icon: ShieldCheck },
        { id: 'research' as ViewType, label: 'Research & Innovation', icon: BookOpen, badge: 'Paper' },
        { id: 'future-scope' as ViewType, label: 'Future Scope', icon: Sparkles },
      ],
    },
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
      case 'poster':
        return <Poster />;
      default:
        return <Landing onEnter={(v) => setActiveView(v as ViewType)} />;
    }
  };

  // Shared Upload & Inference Workspace for AE, VAE, and Classifier
  const renderSharedInferenceUI = () => (
    <>
      <ModelUseCaseCard
        datasetRole={MODEL_META[activeView].datasetRole}
        inferenceAction={MODEL_META[activeView].inferenceAction}
        projectValue={MODEL_META[activeView].projectValue}
      />
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
                        objectFit: 'cover',
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
                  {activeView === 'ae' && (resultData?.noisy || resultData?.corrupted) && (
                    <img
                      src={toImageSrc(resultData.noisy || resultData.corrupted)}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                        objectFit: 'cover',
                      }}
                      alt="Corrupted Input"
                    />
                  )}
                  {activeView === 'vae' && resultData?.generated && (
                    <img
                      src={toImageSrc(resultData.generated)}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                        objectFit: 'cover',
                      }}
                      alt="Generated VAE variation"
                    />
                  )}
                  {(resultData?.reconstructed || (activeView === 'ae' && resultData?.image)) && (
                    <img
                      src={toImageSrc(resultData.reconstructed || resultData.image)}
                      style={{
                        flex: 1,
                        width: 0,
                        minWidth: 0,
                        height: 'auto',
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                        objectFit: 'cover',
                      }}
                      alt="Reconstructed Output"
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
                    <div style={{ fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--muted)', marginBottom: 6 }}>
                      VAE Anomaly Detection Verdict (vs. 294-Tile UCMerced Baseline)
                    </div>
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
                        {metrics.anomalyScore != null && (
                          <div className="metric">
                            <span className="metric-label">Anomaly z-Score</span>
                            <span className="metric-value">{Number(metrics.anomalyScore).toFixed(2)}σ</span>
                          </div>
                        )}
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
            <InferenceTrace
              isRunning={loading}
              endpoint={MODEL_META[activeView]?.inferEndpoint || ''}
              activeStepIndex={inferenceStep}
              executionInfo={inferenceExecutionInfo}
              pipelineSteps={
                activeView === 'ae'
                  ? [
                      'Uploading aerial parcel to PyTorch FastAPI backend',
                      'Resizing to 128×128 RGB & injecting Gaussian sensor noise (σ=0.15)',
                      'Running DenoisingAE skip-UNet forward pass (outputs/ae/model.pth)',
                      'Computing empirical MSE/PSNR & decoding reconstructed tile',
                    ]
                  : activeView === 'vae'
                  ? [
                      'Uploading aerial parcel to PyTorch FastAPI backend',
                      'Encoding 128×128 RGB tensor into 64×8×8 latent posterior (μ, log σ²)',
                      'Reparameterizing latent sample & decoding reconstruction (outputs/vae/model.pth)',
                      'Computing KL divergence, MSE & z-score anomaly against baseline',
                    ]
                  : [
                      'Uploading aerial parcel to PyTorch FastAPI backend',
                      'Resizing & normalizing image to 224×224 RGB tensor',
                      'Running ResNet-18 classifier forward pass (outputs/transformer/model.pth)',
                      'Computing 21-class Softmax probabilities & top-5 predictions',
                    ]
              }
            />
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
            Samples a novel aerial variation from the learned spatial latent manifold using stochastic latent perturbation
            on an empirical parcel anchor, synthesizing a coherent unseen land-use sample without crossfade or double-exposure artifacts.
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
      <div className="app-container">
        {/* Mobile Backdrop Overlay */}
        {mobileMenuOpen && (
          <div
            className="sidebar-backdrop"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />
        )}

        {/* Left Navigation Sidebar (Responsive Off-Canvas on Mobile) */}
        <aside className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
          <div className="logo-area" onClick={() => { setActiveView('landing'); setMobileMenuOpen(false); }}>
            <div className="logo-emblem">UG</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="logo-title">UrbanGen AI</div>
              <div className="logo-subtitle">Edge Remote Sensing & GenAI</div>
            </div>
            <button
              className="mobile-close-sidebar-btn"
              onClick={(e) => {
                e.stopPropagation();
                setMobileMenuOpen(false);
              }}
              aria-label="Close Navigation"
            >
              <X size={18} />
            </button>
          </div>

          <nav className="nav-links">
            {navSections.map((sec) => (
              <div key={sec.title} style={{ marginBottom: 6 }}>
                <div className="nav-section-title">{sec.title}</div>
                {sec.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeView === item.id;
                  return (
                    <button
                      key={item.id}
                      className={`nav-item ${isActive ? 'active' : ''}`}
                      onClick={() => {
                        setActiveView(item.id);
                        setMobileMenuOpen(false);
                      }}
                      onMouseEnter={() => preloadView(item.id)}
                    >
                      <Icon size={16} />
                      <span style={{ flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {item.label}
                      </span>
                      {item.badge && <span className="nav-badge">{item.badge}</span>}
                    </button>
                  );
                })}
              </div>
            ))}
          </nav>

          {/* Sidebar Footer: Hardware & API Gateway Key */}
          <div className="sidebar-footer">
            <div className="hardware-pill">
              <span>⚡ RTX 4050 6GB</span>
              <span style={{ color: 'var(--success)', fontWeight: 600 }}>0.133 kWh</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--muted)' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                  <KeyRound size={12} /> Edge Gateway Key
                </span>
                {apiKeyInput ? <span style={{ color: 'var(--success)', fontSize: '0.68rem', fontWeight: 600 }}>Active</span> : null}
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
                  background: 'var(--surface-inset)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: 6,
                  padding: '6px 8px',
                  fontSize: '0.75rem',
                  fontFamily: 'var(--font-mono)',
                }}
              />
            </div>
          </div>
        </aside>

        {/* Main Content View Area */}
        <div className="main-content">
          {/* Top Bar with Live Model State & Theme Switcher */}
          <header className="topbar">
            <div className="topbar-left" style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
              <button
                className="mobile-menu-toggle"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label={mobileMenuOpen ? 'Close Navigation Menu' : 'Open Navigation Menu'}
              >
                {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>

              <div className="topbar-breadcrumbs">
                <span className="breadcrumb-root" style={{ color: 'var(--muted)', fontSize: '0.8rem' }}>UrbanGen AI</span>
                <span className="breadcrumb-separator" style={{ color: 'var(--border-subtle)' }}>/</span>
                <span className="breadcrumb-sub" style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>Pipeline</span>
                <span className="breadcrumb-separator" style={{ color: 'var(--border-subtle)' }}>/</span>
                <span className="topbar-badge">
                  {isImageView(activeView) ? MODEL_META[activeView].title : activeView.toUpperCase()}
                </span>
              </div>
            </div>

            <div className="topbar-right" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              {/* MIT AOE Academic Defense badge */}
              <div
                className="defense-badge"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  fontSize: '0.74rem',
                  fontFamily: 'var(--font-mono)',
                  color: 'var(--muted)',
                  padding: '4px 10px',
                  borderRadius: 6,
                  background: 'var(--surface-inset)',
                  border: '1px solid var(--border)',
                }}
              >
                <span>MIT AOE, Pune</span>
                <span style={{ color: 'var(--border-subtle)' }}>|</span>
                <span style={{ color: 'var(--accent)', fontWeight: 600 }}>60M Capstone</span>
              </div>

              {/* One-Click Urban AI Glossary Quick Access */}
              <button
                onClick={() => setActiveView('glossary')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 5,
                  fontSize: '0.74rem',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600,
                  color: activeView === 'glossary' ? 'var(--accent)' : 'var(--text)',
                  background: activeView === 'glossary' ? 'var(--active-tint)' : 'var(--surface-inset)',
                  border: `1px solid ${activeView === 'glossary' ? 'var(--accent)' : 'var(--border)'}`,
                  borderRadius: 6,
                  padding: '4px 10px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
                title="Open Urban AI Mathematical Symbols & Terms Glossary"
              >
                <BookOpen size={13} style={{ color: 'var(--accent)' }} />
                <span>Glossary</span>
              </button>

              {statusKey in status ? (
                <div className={`status-badge ${status[statusKey] === 'Trained' ? 'trained' : 'nottrained'}`}>
                  <span
                    className={`status-dot ${status[statusKey] === 'Trained' ? 'status-badge-active' : ''}`}
                  />
                  <span>
                    {status[statusKey] === 'Trained' ? '50e Checkpoint Active' : 'Model Not Trained'}
                  </span>
                </div>
              ) : isStatusLoading ? (
                <div style={{ fontSize: '0.78rem', color: 'var(--muted)', fontFamily: 'var(--font-mono)' }}>
                  Probing weights...
                </div>
              ) : null}

              <button
                className="theme-toggle"
                onClick={toggleTheme}
                title={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
                aria-label="Toggle visual theme"
              >
                {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
              </button>
            </div>
          </header>

          {/* Dynamic Content Body with Error Boundary & Lazy Suspense */}
          <main className="content-body">
            {statusError && typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && (
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
