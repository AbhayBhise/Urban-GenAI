// Central API helper with enterprise resilience.
// Injects the locally-stored API key (if the operator has set one) as the
// X-API-Key header on every request.
//
// Production Features:
//   * Automatic exponential backoff retries on transient errors (502/503/504/429/network drop)
//   * AbortController timeout guards (default 20s, configurable)
//   * Structured ApiError with status and response diagnostics
//   * Real-time backend liveness / readiness health check helper

export const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

const API_KEY_STORAGE = 'urbangen_api_key';

export class ApiError extends Error {
  public status: number;
  public statusText: string;
  public data?: any;

  constructor(message: string, status: number, statusText: string, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.statusText = statusText;
    this.data = data;
  }
}

export function getApiKey(): string {
  try {
    return localStorage.getItem(API_KEY_STORAGE) || '';
  } catch {
    return '';
  }
}

export function setApiKey(value: string) {
  try {
    if (value) localStorage.setItem(API_KEY_STORAGE, value);
    else localStorage.removeItem(API_KEY_STORAGE);
  } catch {
    /* storage unavailable — ignore */
  }
}

export interface ApiFetchOptions extends RequestInit {
  timeoutMs?: number;
  retries?: number;
  retryDelayMs?: number;
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function isTransientError(status: number): boolean {
  return status === 429 || status === 502 || status === 503 || status === 504;
}

export async function apiFetch(path: string, options: ApiFetchOptions = {}): Promise<Response> {
  const {
    timeoutMs = 25000,
    retries = 2,
    retryDelayMs = 400,
    ...fetchInit
  } = options;

  const url = `${API_URL}${path}`;
  const key = getApiKey();
  const headers = new Headers(fetchInit.headers || {});
  if (key) {
    headers.set('X-API-Key', key);
  }

  let attempt = 0;
  let lastError: any = null;

  while (attempt <= retries) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    // Chain with external signal if provided
    let abortListener: (() => void) | null = null;
    if (fetchInit.signal) {
      if (fetchInit.signal.aborted) {
        controller.abort();
      } else {
        abortListener = () => controller.abort();
        fetchInit.signal.addEventListener('abort', abortListener);
      }
    }

    try {
      const response = await fetch(url, {
        ...fetchInit,
        headers,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      if (abortListener && fetchInit.signal) {
        fetchInit.signal.removeEventListener('abort', abortListener);
      }

      // If status is transient (e.g. 502 Bad Gateway while restarting / cold booting), retry
      if (!response.ok && isTransientError(response.status) && attempt < retries) {
        attempt++;
        const jitter = Math.random() * 200;
        const delay = retryDelayMs * Math.pow(2, attempt - 1) + jitter;
        await sleep(delay);
        continue;
      }

      return response;
    } catch (err: any) {
      clearTimeout(timeoutId);
      if (abortListener && fetchInit.signal) {
        fetchInit.signal.removeEventListener('abort', abortListener);
      }

      lastError = err;

      // Only retry if network dropped or timed out and we have attempts remaining
      if (attempt < retries && (err.name === 'AbortError' || err.message?.includes('fetch') || err.message?.includes('network'))) {
        attempt++;
        const jitter = Math.random() * 200;
        const delay = retryDelayMs * Math.pow(2, attempt - 1) + jitter;
        await sleep(delay);
        continue;
      }

      throw err;
    }
  }

  throw lastError || new Error(`apiFetch failed after ${retries} retries`);
}

/**
 * Cloud-native health probe check utility for status bars and degradation banners.
 */
export async function checkBackendHealth(): Promise<{
  healthy: boolean;
  ready: boolean;
  latencyMs: number;
  data?: any;
}> {
  const t0 = performance.now();
  try {
    const res = await apiFetch('/healthz', { timeoutMs: 4000, retries: 1 });
    const latencyMs = Math.round(performance.now() - t0);
    if (!res.ok) {
      return { healthy: false, ready: false, latencyMs };
    }
    const data = await res.json();
    return {
      healthy: data.status === 'healthy',
      ready: true,
      latencyMs,
      data,
    };
  } catch {
    return {
      healthy: false,
      ready: false,
      latencyMs: Math.round(performance.now() - t0),
    };
  }
}
