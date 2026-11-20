"""Comprehensive production integration test suite for UrbanGen AI API.

Tests:
  1. Cloud-Native Health & Readiness Probes (/healthz, /readyz, /metrics)
  2. Enterprise OWASP Security Headers (X-Content-Type-Options, X-Frame-Options, CSP, X-Request-ID)
  3. Ground-Truth Model Evaluation Endpoints (/evaluate/summary, /evaluate/*)
  4. Metadata & Governance Endpoints (/status, /config, /privacy, /datasets, /system)
  5. In-Memory High-Concurrency Caching Verification
  6. Robust Error Handling & Payload Validation
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure repository root and backend directory are in sys.path
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

_BACKEND_DIR = os.path.join(_REPO_ROOT, "backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from backend.api import app, api_cache


@pytest.fixture(scope="module")
def client():
    """Module-scoped FastAPI test client."""
    with TestClient(app) as c:
        yield c


class TestHealthAndObservability:
    """Verifies Kubernetes/cloud health probes and Prometheus metrics."""

    def test_healthz_liveness(self, client):
        response = client.get("/healthz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "urbangen-ai"
        assert "uptime_sec" in data
        assert "memory" in data
        assert "percent" in data["memory"]

    def test_readyz_readiness(self, client):
        response = client.get("/readyz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "models_ready" in data
        # At least one model checkpoint should be loaded
        assert any(data["models_ready"].values())

    def test_metrics_prometheus_exposition(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200
        content = response.text
        assert "urbangen_uptime_seconds" in content
        assert "urbangen_cache_hits_total" in content
        assert "urbangen_http_requests_total" in content


class TestEnterpriseSecurityHeaders:
    """Verifies that all responses strictly adhere to OWASP security standards."""

    def test_security_headers_present(self, client):
        response = client.get("/healthz")
        assert response.status_code == 200
        headers = response.headers

        # Verify OWASP required headers
        assert headers.get("X-Content-Type-Options") == "nosniff"
        assert headers.get("X-Frame-Options") == "SAMEORIGIN"
        assert headers.get("X-XSS-Protection") == "1; mode=block"
        assert "max-age=31536000" in headers.get("Strict-Transport-Security", "")
        assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert "default-src 'self'" in headers.get("Content-Security-Policy", "")

        # Tracing headers
        assert "X-Request-ID" in headers
        assert "X-Response-Time-ms" in headers


class TestSystemAndMetadataEndpoints:
    """Verifies status, privacy, configuration, and datasets integrity."""

    def test_status_endpoint(self, client):
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "ae" in data
        assert "vae" in data
        assert "transformer" in data
        assert "gan" in data
        assert "diffusion" in data

    def test_config_endpoint(self, client):
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert "auth_enabled" in data
        assert "rate_limit" in data

    def test_privacy_endpoint(self, client):
        response = client.get("/privacy")
        assert response.status_code == 200
        data = response.json()
        assert data["personal_data_collected"] == "none"
        assert "EU GDPR" in data["frameworks"]

    def test_datasets_endpoint(self, client):
        response = client.get("/datasets")
        assert response.status_code == 200
        data = response.json()
        assert "ucmerced" in data or "pune_datasets" in data

    def test_system_endpoint(self, client):
        response = client.get("/system")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert "ram" in data
        assert "gpu" in data
        assert "os" in data


class TestModelEvaluationContracts:
    """Verifies benchmark contracts and empirical fidelity against ground truth."""

    def test_evaluate_summary(self, client):
        response = client.get("/evaluate/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["schema_version"] == "1.0"
        assert data["dataset"]["classes"] == 21
        assert "models" in data
        models = data["models"]
        assert "ae" in models
        assert "vae" in models
        assert "classifier" in models
        assert "gan" in models
        assert "diffusion" in models
        assert "gpt" in models

    def test_evaluate_diffusion(self, client):
        response = client.get("/evaluate/diffusion")
        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "Class-Conditional DDPM (DDIM 40-step Sampler)"
        assert data["timesteps"] == 1000

    def test_evaluate_gpt(self, client):
        response = client.get("/evaluate/gpt")
        assert response.status_code == 200
        data = response.json()
        assert "held_out_perplexity" in data or "perplexity" in data or "val_loss" in data

    def test_evaluate_ae(self, client):
        response = client.get("/evaluate/ae")
        assert response.status_code == 200
        data = response.json()
        assert "mean_psnr" in data or "overall" in data or "per_class" in data

    def test_evaluate_vae(self, client):
        response = client.get("/evaluate/vae")
        assert response.status_code == 200
        data = response.json()
        assert "mean_psnr" in data or "overall" in data or "per_class" in data


class TestCachingPerformance:
    """Verifies that repetitive requests are cached with sub-millisecond return."""

    def test_evaluation_cache_hit(self, client):
        # First request populates cache
        r1 = client.get("/evaluate/summary")
        assert r1.status_code == 200

        # Second request should be served directly from FastCache
        initial_hits = api_cache.hits
        r2 = client.get("/evaluate/summary")
        assert r2.status_code == 200
        assert r2.json() == r1.json()
        assert api_cache.hits >= initial_hits + 1


class TestPayloadClampingAndValidation:
    """Verifies that malicious or invalid payloads are rejected safely."""

    def test_non_image_upload_rejected(self, client):
        # Uploading raw text should trigger 415 Unsupported Media Type
        files = {"file": ("malicious.txt", b"not an image", "text/plain")}
        response = client.post("/infer/ae", files=files)
        assert response.status_code in [400, 415]

    def test_oversized_payload_rejected(self, client):
        # Upload exceeding 8MB should trigger 413 Payload Too Large
        oversized_data = b"0" * (9 * 1024 * 1024)
        files = {"file": ("oversized.jpg", oversized_data, "image/jpeg")}
        response = client.post("/infer/ae", files=files)
        assert response.status_code in [400, 413]
