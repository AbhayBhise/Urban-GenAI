"""Deployment security + privacy controls for the UrbanGen AI API.

Everything here is configured through environment variables (loaded from a
local ``.env`` via python-dotenv) so the same code runs frictionless in
development and locked-down in a shared/production deployment:

    URBANGEN_API_KEY          if set, every inference/generation endpoint
                              requires a matching ``X-API-Key`` header
    URBANGEN_ALLOWED_ORIGINS  comma-separated CORS allow-list
    URBANGEN_MAX_UPLOAD_MB    reject image uploads larger than this
    URBANGEN_RATE_LIMIT       slowapi rate-limit string, e.g. "30/minute"

Design intent (see docs/PRIVACY.md, docs/SECURITY.md):
  * uploaded images are read straight into memory and never written to disk
  * no personal data is requested, logged, or persisted
  * no outbound network calls are made with user-supplied content
"""

import io
import os
import hmac

from dotenv import load_dotenv
from fastapi import Header, HTTPException, UploadFile
from PIL import Image
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv()

API_KEY = os.getenv("URBANGEN_API_KEY", "").strip()

_DEFAULT_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("URBANGEN_ALLOWED_ORIGINS", _DEFAULT_ORIGINS).split(",")
    if o.strip()
]

MAX_UPLOAD_MB = float(os.getenv("URBANGEN_MAX_UPLOAD_MB", "8"))
MAX_UPLOAD_BYTES = int(MAX_UPLOAD_MB * 1024 * 1024)

RATE_LIMIT = os.getenv("URBANGEN_RATE_LIMIT", "30/minute")

# Keyed by client address. Endpoints opt in with @limiter.limit(RATE_LIMIT).
limiter = Limiter(key_func=get_remote_address, default_limits=[])

AUTH_ENABLED = bool(API_KEY)


def require_api_key(x_api_key: str = Header(default="")):
    """FastAPI dependency. No-op unless URBANGEN_API_KEY is configured."""
    if not AUTH_ENABLED:
        return
    if not x_api_key or not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid X-API-Key header.",
        )


async def read_image_upload(file: UploadFile) -> Image.Image:
    """Validate and decode an uploaded image entirely in memory.

    Raises 413 if the payload exceeds the configured size limit and 415 if
    it is not a decodable image. The bytes are discarded as soon as this
    function returns its PIL image — nothing touches the filesystem.
    """
    content_type = (file.content_type or "").lower()
    if content_type and not content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload must be an image.")

    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Image exceeds the {MAX_UPLOAD_MB:g} MB upload limit.",
        )
    try:
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img.load()
    except Exception:
        raise HTTPException(status_code=415, detail="Could not decode image.")
    return img


def privacy_policy() -> dict:
    """Machine-readable summary served at GET /privacy."""
    return {
        "personal_data_collected": "none",
        "uploads": "processed in memory, never written to disk, discarded after inference",
        "retention": "no user content is retained",
        "cookies": "none",
        "client_storage": "only a locally-entered API key in browser localStorage (never transmitted to third parties)",
        "third_party_sharing": "none; no outbound calls are made with user content",
        "logging": "request metadata only (no image content, no request bodies)",
        "auth_enabled": AUTH_ENABLED,
        "frameworks": ["EU GDPR", "India DPDP Act 2023", "EU AI Act (limited-risk / transparency)"],
        "docs": ["/governance/privacy", "/governance/ethics", "/governance/security", "/governance/model_card"],
    }
