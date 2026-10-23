// Central API helper. Injects the locally-stored API key (if the operator
// has set one) as the X-API-Key header on every request. The key never
// leaves the browser except as a header to this project's own backend.

// Set VITE_API_URL in the deployment environment for the hosted backend.
// Keep localhost as the development default so local runs remain zero-config.
export const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

const API_KEY_STORAGE = 'urbangen_api_key';

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

export function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers || {});
  const key = getApiKey();
  if (key) headers.set('X-API-Key', key);
  return fetch(`${API_URL}${path}`, { ...init, headers });
}
