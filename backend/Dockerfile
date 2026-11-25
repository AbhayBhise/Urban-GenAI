# ==============================================================================
# Multi-Stage Enterprise Production Dockerfile for UrbanGen AI Backend
# ==============================================================================

# Stage 1: Build & Dependency Resolution
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --index-url https://download.pytorch.org/whl/cpu torch torchvision && \
    pip install --user -r requirements.txt

# Stage 2: Hardened Non-Root Production Runtime
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    WEB_CONCURRENCY=4 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Install curl for cloud healthcheck probes
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged system group & user (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code and verified artifacts
COPY backend /app/backend
COPY outputs /app/outputs
COPY docs /app/docs

# Set ownership to unprivileged user
RUN chown -R appuser:appgroup /app /home/appuser

USER appuser

WORKDIR /app/backend
EXPOSE 8000

# Cloud-native health check
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/healthz || exit 1

# Launch production server with 1 worker to fit Render Free Tier (512MB RAM)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --proxy-headers --forwarded-allow-ips '*'"]
