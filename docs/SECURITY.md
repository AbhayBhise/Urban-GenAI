# UrbanGen AI — Security

_Unit 6: Security & Sustainability — misuse prevention, secure deployment._

## 1. Threat model

| Asset | Threat | Control |
|---|---|---|
| API availability | Request flooding / accidental loops | Per-client rate limiting (`slowapi`, `URBANGEN_RATE_LIMIT`, default `30/minute`) |
| Compute resources | Oversized / malformed uploads (decompression bombs) | Size cap (`URBANGEN_MAX_UPLOAD_MB`, default 8 MB) + content-type check + guarded decode in `read_image_upload` |
| Unauthorised use | Open endpoint on a shared network | Optional API-key auth (`URBANGEN_API_KEY`) enforced on all `/infer/*` and `/generate/*` routes via `require_api_key`; constant-time comparison |
| Cross-origin abuse | Malicious web page calling the API from a user's browser | CORS allow-list (`URBANGEN_ALLOWED_ORIGINS`) — no wildcard |
| Data exposure | Leaked user content | Uploads never persisted; no request bodies logged; no outbound calls with user content |
| Supply chain | Compromised dependency | Pinned minimum versions in `requirements.txt`; small dependency surface |

## 2. Controls in this repository

- **Authentication** — set `URBANGEN_API_KEY` in `.env`; clients send `X-API-Key`.
  Unset in development for zero friction; **must be set for any non-localhost deployment**.
- **CORS** — `backend/security.py` builds `allow_origins` from env; the previous
  `allow_origins=["*"]` has been removed.
- **Rate limiting** — `limiter` keyed by remote address; `/infer/*`, `/generate/*`,
  `/transformer/query` decorated with the configured limit; 429 on breach.
- **Upload validation** — `read_image_upload` enforces MIME prefix `image/`,
  the size cap (413), and a safe decode (415 on failure). All image endpoints
  route through it; nothing is written to disk.
- **No secrets in code** — all configuration via environment / `.env` (git-ignored;
  only `.env.example` is committed).

## 3. Production deployment checklist

- [ ] `URBANGEN_API_KEY` set to a long random value; distributed out of band.
- [ ] `URBANGEN_ALLOWED_ORIGINS` restricted to the real frontend origin(s).
- [ ] Terminate TLS in front of the app (reverse proxy / load balancer); never
      serve the API over plain HTTP.
- [ ] Run `uvicorn` bound to `127.0.0.1` behind the proxy, not `0.0.0.0`
      (the `__main__` block's `0.0.0.0` is for local LAN demo only).
- [ ] Run as a non-root user in a container with a read-only root filesystem.
- [ ] Set a sensible worker count and body-size limit at the proxy.
- [ ] Keep dependencies patched (`pip list --outdated`); rebuild on CVE advisories.
- [ ] Forward only request metadata to logs; scrub client IPs per retention policy.

## 4. Reporting a vulnerability

Report privately to _[deployer to complete: security contact email]_.
Please do not open a public issue for undisclosed vulnerabilities.
