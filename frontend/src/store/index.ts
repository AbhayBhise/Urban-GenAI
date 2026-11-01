export * from './useAppStore';

import { useAppStore } from './useAppStore';

// Individual selector hooks for zero unnecessary re-renders
export const useActiveView = () => useAppStore((state) => state.activeView);
export const useTheme = () => useAppStore((state) => state.theme);
export const useModelStatus = () => useAppStore((state) => state.status);
export const useStatusError = () => useAppStore((state) => state.statusError);
export const useIsStatusLoading = () => useAppStore((state) => state.isStatusLoading);
export const useInferenceFile = () => useAppStore((state) => state.file);
export const useInferencePreview = () => useAppStore((state) => state.preview);
export const useInferenceLoading = () => useAppStore((state) => state.loading);
export const useInferenceResult = () => useAppStore((state) => ({
  resultData: state.resultData,
  metrics: state.metrics,
  predictions: state.predictions,
}));
export const useToasts = () => useAppStore((state) => state.toasts);

