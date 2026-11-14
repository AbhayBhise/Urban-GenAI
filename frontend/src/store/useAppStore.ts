import { create } from 'zustand';
import { subscribeWithSelector, persist, createJSONStorage } from 'zustand/middleware';
import { apiFetch, getApiKey, setApiKey as persistApiKey } from '../lib/api';

export type ViewType =
  | 'landing'
  | 'ae'
  | 'vae'
  | 'classifier'
  | 'diffusion'
  | 'plan-generator'
  | 'governance'
  | 'gan'
  | 'datasets'
  | 'system'
  | 'model-explorer'
  | 'model-comparison'
  | 'training'
  | 'evaluation'
  | 'research'
  | 'glossary'
  | 'future-scope'
  | 'system-architecture'
  | 'poster';

export type ThemeMode = 'dark' | 'light';

export interface ToastNotification {
  id: string;
  type: 'info' | 'success' | 'warn' | 'error';
  message: string;
  duration?: number;
}

export interface AppState {
  // Navigation & Core UI
  activeView: ViewType;
  theme: ThemeMode;
  apiKey: string;
  toasts: ToastNotification[];

  // Global Backend Status & Telemetry
  status: Record<string, string>;
  statusError: string | null;
  isStatusLoading: boolean;

  // Active Image Inference Session
  file: File | null;
  preview: string | null;
  resultData: any | null;
  metrics: any | null;
  predictions: any[] | null;
  loading: boolean;
  requestId: number;

  // VAE Interactive Sub-features
  interpImg: string | null;
  interpLoading: boolean;
  interpError: string | null;

  randomGenImg: string | null;
  randomGenLoading: boolean;
  randomGenError: string | null;

  urbanizeImg: string | null;
  urbanizeLoading: boolean;
  urbanizeError: string | null;
  urbanizeIntensity: number;
}

export interface AppActions {
  // Navigation & UI
  setActiveView: (view: ViewType) => void;
  setTheme: (theme: ThemeMode) => void;
  toggleTheme: () => void;
  setApiKey: (key: string) => void;

  // Toasts
  addToast: (toast: Omit<ToastNotification, 'id'>) => string;
  removeToast: (id: string) => void;

  // Model Status Lifecycle
  fetchStatus: () => Promise<void>;

  // Inference Actions
  setFile: (file: File | null, previewUrl?: string | null) => void;
  setLoading: (loading: boolean) => void;
  setInferenceResult: (resultData: any, metrics?: any, predictions?: any[]) => void;
  clearInference: () => void;

  // VAE Sub-features
  setInterpResult: (img: string | null, loading?: boolean, error?: string | null) => void;
  setRandomGenResult: (img: string | null, loading?: boolean, error?: string | null) => void;
  setUrbanizeResult: (img: string | null, loading?: boolean, error?: string | null) => void;
  setUrbanizeIntensity: (val: number) => void;
}

export type AppStore = AppState & AppActions;

// Safe localStorage fallback that won't throw in private windows, iframes, or quota limit
const safeStorage = {
  getItem: (key: string): string | null => {
    try {
      return typeof window !== 'undefined' ? window.localStorage.getItem(key) : null;
    } catch {
      return null;
    }
  },
  setItem: (key: string, value: string): void => {
    try {
      if (typeof window !== 'undefined') window.localStorage.setItem(key, value);
    } catch (e) {
      console.warn('Storage write failed (e.g. quota exceeded or incognito):', e);
    }
  },
  removeItem: (key: string): void => {
    try {
      if (typeof window !== 'undefined') window.localStorage.removeItem(key);
    } catch {}
  },
};

const getInitialTheme = (): ThemeMode => {
  if (typeof window === 'undefined') return 'dark';
  try {
    const saved = window.localStorage.getItem('urbangen-theme');
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  } catch {
    return 'dark';
  }
};

const getInitialView = (): ViewType => {
  if (typeof window === 'undefined') return 'landing';
  const hash = window.location.hash.toLowerCase().replace(/^#\/?/, '').split('/')[0];
  if (!hash) return 'landing';
  if (hash.startsWith('research')) return 'research';
  if (hash.startsWith('governance')) return 'governance';
  if (hash.startsWith('plan')) return 'plan-generator';
  if (hash.startsWith('gan')) return 'gan';
  const valid: ViewType[] = [
    'landing', 'ae', 'vae', 'classifier', 'plan-generator', 'governance',
    'gan', 'datasets', 'system', 'model-explorer', 'model-comparison',
    'training', 'evaluation', 'diffusion', 'research', 'glossary',
    'future-scope', 'system-architecture', 'poster'
  ];
  return valid.includes(hash as ViewType) ? (hash as ViewType) : 'landing';
};

export const useAppStore = create<AppStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // State defaults
        activeView: getInitialView(),
        theme: getInitialTheme(),
        apiKey: typeof window !== 'undefined' ? getApiKey() : '',
        toasts: [],

        status: {},
        statusError: null,
        isStatusLoading: false,

        file: null,
        preview: null,
        resultData: null,
        metrics: null,
        predictions: null,
        loading: false,
        requestId: 0,

        interpImg: null,
        interpLoading: false,
        interpError: null,

        randomGenImg: null,
        randomGenLoading: false,
        randomGenError: null,

        urbanizeImg: null,
        urbanizeLoading: false,
        urbanizeError: null,
        urbanizeIntensity: 0.6,

        // Actions
        setActiveView: (view: ViewType) => {
          if (typeof window !== 'undefined') {
            window.location.hash = `#/${view}`;
          }
          set({ activeView: view });
        },

        setTheme: (theme: ThemeMode) => {
          if (typeof document !== 'undefined') {
            document.documentElement.setAttribute('data-theme', theme);
          }
          set({ theme });
        },

        toggleTheme: () => {
          const next = get().theme === 'dark' ? 'light' : 'dark';
          get().setTheme(next);
        },

        setApiKey: (key: string) => {
          persistApiKey(key);
          set({ apiKey: key });
        },

        addToast: (toast) => {
          const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
          const newToast: ToastNotification = { ...toast, id };
          set((state) => ({ toasts: [...state.toasts.slice(-4), newToast] }));
          const duration = toast.duration ?? 4000;
          if (duration > 0) {
            setTimeout(() => {
              get().removeToast(id);
            }, duration);
          }
          return id;
        },

        removeToast: (id: string) => {
          set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) }));
        },

        fetchStatus: async () => {
          set({ isStatusLoading: true });
          try {
            const res = await apiFetch('/status');
            if (res.ok) {
              const data = await res.json();
              set({ status: data, statusError: null });
            } else {
              set({ statusError: `Backend returned error status ${res.status}` });
            }
          } catch (err: any) {
            set({
              statusError: 'Backend service offline. Start API via `python api.py` from the backend directory.',
            });
          } finally {
            set({ isStatusLoading: false });
          }
        },

        setFile: (file: File | null, previewUrl?: string | null) => {
          const prevPreview = get().preview;
          // Revoke previous blob URL to prevent memory leaks in long sessions
          if (prevPreview && prevPreview.startsWith('blob:')) {
            try {
              URL.revokeObjectURL(prevPreview);
            } catch {}
          }
          set({
            file,
            preview: previewUrl !== undefined ? previewUrl : (file ? URL.createObjectURL(file) : null),
            resultData: null,
            metrics: null,
            predictions: null,
            interpImg: null,
            interpError: null,
            randomGenImg: null,
            randomGenError: null,
            urbanizeImg: null,
            urbanizeError: null,
            requestId: get().requestId + 1,
          });
        },

        setLoading: (loading: boolean) => set({ loading }),

        setInferenceResult: (resultData: any, metrics: any = null, predictions: any[] | null = null) => {
          set({
            resultData,
            metrics,
            predictions,
            loading: false,
          });
        },

        clearInference: () => {
          const prevPreview = get().preview;
          if (prevPreview && prevPreview.startsWith('blob:')) {
            try {
              URL.revokeObjectURL(prevPreview);
            } catch {}
          }
          set({
            file: null,
            preview: null,
            resultData: null,
            metrics: null,
            predictions: null,
            loading: false,
            interpImg: null,
            interpLoading: false,
            interpError: null,
            randomGenImg: null,
            randomGenLoading: false,
            randomGenError: null,
            urbanizeImg: null,
            urbanizeLoading: false,
            urbanizeError: null,
            requestId: get().requestId + 1,
          });
        },

        setInterpResult: (img, loading = false, error = null) => {
          set({ interpImg: img, interpLoading: loading, interpError: error });
        },

        setRandomGenResult: (img, loading = false, error = null) => {
          set({ randomGenImg: img, randomGenLoading: loading, randomGenError: error });
        },

        setUrbanizeResult: (img, loading = false, error = null) => {
          set({ urbanizeImg: img, urbanizeLoading: loading, urbanizeError: error });
        },

        setUrbanizeIntensity: (val: number) => set({ urbanizeIntensity: val }),
      }),
      {
        name: 'urbangen-store',
        storage: createJSONStorage(() => safeStorage),
        partialize: (state) => ({
          theme: state.theme,
          activeView: state.activeView,
          urbanizeIntensity: state.urbanizeIntensity,
        }),
      }
    )
  )
);

// Synchronize theme with DOM immediately upon load
if (typeof document !== 'undefined') {
  const currentTheme = useAppStore.getState().theme;
  document.documentElement.setAttribute('data-theme', currentTheme);
}

// React to browser hash changes (back/forward navigation & deep-linking)
if (typeof window !== 'undefined') {
  window.addEventListener('hashchange', () => {
    const nextView = getInitialView();
    if (useAppStore.getState().activeView !== nextView) {
      useAppStore.getState().setActiveView(nextView);
    }
  });
}

