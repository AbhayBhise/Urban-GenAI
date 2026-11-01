import { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class LazyErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('LazyErrorBoundary caught an error in dynamic view:', error, errorInfo);
    this.setState({ error, errorInfo });
  }

  private handleRetry = () => {
    // If it's a dynamic module import error (common after redeployments or network drops),
    // a quick reload or state reset resolves the stale asset cache.
    this.setState({ hasError: false, error: null, errorInfo: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  private handleGoHome = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    if (typeof window !== 'undefined') {
      window.location.hash = '#/landing';
      window.location.reload();
    }
  };

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      const isChunkError =
        this.state.error?.message?.includes('fetch dynamically imported module') ||
        this.state.error?.message?.includes('Loading chunk') ||
        this.state.error?.name === 'ChunkLoadError';

      return (
        <div
          className="card page-enter"
          style={{
            maxWidth: 640,
            margin: '40px auto',
            padding: '30px',
            border: '1px solid var(--danger)',
            background: 'var(--surface)',
            borderRadius: 8,
            boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <div
              style={{
                width: 42,
                height: 42,
                borderRadius: '50%',
                background: 'var(--danger-wash)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--danger)',
              }}
            >
              <AlertTriangle size={24} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.15rem', color: 'var(--text)', fontWeight: 600 }}>
                {isChunkError ? 'Component Load Interrupted' : 'Interface Error in View'}
              </h2>
              <div style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
                {isChunkError
                  ? 'A network timeout or updated application bundle prevented this page module from loading.'
                  : 'An unhandled rendering exception occurred in this view.'}
              </div>
            </div>
          </div>

          <div
            style={{
              padding: '12px 14px',
              background: 'var(--surface-inset)',
              borderRadius: 6,
              border: '1px solid var(--border)',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.78rem',
              color: 'var(--danger)',
              marginBottom: 20,
              overflowX: 'auto',
              maxHeight: 120,
            }}
          >
            {this.state.error?.toString() || 'Unknown runtime error'}
          </div>

          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <button
              className="btn"
              onClick={this.handleRetry}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                flex: '1 1 auto',
                justifyContent: 'center',
              }}
            >
              <RefreshCw size={16} /> Retry View
            </button>
            <button
              className="btn"
              onClick={this.handleGoHome}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                background: 'transparent',
                border: '1px solid var(--border)',
                color: 'var(--text)',
                flex: '1 1 auto',
                justifyContent: 'center',
              }}
            >
              <Home size={16} /> Return to Overview
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
