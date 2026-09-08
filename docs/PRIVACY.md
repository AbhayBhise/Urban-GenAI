# UrbanGen AI — Privacy & Data Protection

_Unit 6: Policy & Law — EU GDPR, India's Digital Personal Data Protection (DPDP) Act 2023, EU AI Act._

## 1. Summary

UrbanGen AI is designed for **data minimisation by default**. It does not ask for,
receive, or store personal data. The only inputs are aerial/satellite image tiles
and free-text planning prompts supplied by the operator.

| Question | Answer |
|---|---|
| Personal data collected? | **None.** |
| Are uploads stored? | **No.** Images are decoded in memory (`backend/security.py: read_image_upload`) and discarded after inference. Nothing is written to disk. |
| Cookies / trackers? | None. |
| Browser storage? | One optional key: a locally-entered API key kept in `localStorage` for convenience. It is sent only to this project's own API, as the `X-API-Key` header. |
| Third-party processors / outbound calls? | None. No user content leaves the host. |
| Logs | Request metadata only (path, status, client address for rate-limiting). No request bodies, no image content. |

## 2. GDPR alignment

- **Lawfulness, fairness, transparency (Art. 5(1)(a))** — no personal data is
  processed; this policy and the model documentation are public.
- **Purpose limitation (Art. 5(1)(b))** — inputs are used solely to produce the
  requested inference and are not repurposed.
- **Data minimisation (Art. 5(1)(c))** — the API accepts only what a single
  inference needs and holds it only for the duration of the request.
- **Storage limitation (Art. 5(1)(e))** — zero retention; there is nothing to
  erase, rectify, or port, so Arts. 15–20 are satisfied by construction.
- **Integrity & confidentiality (Art. 5(1)(f))** — see `docs/SECURITY.md`.
- **Controller** — _[deployer to complete: organisation name, contact, DPO if applicable]_.
- If a future deployment introduces user accounts, audit trails, or dataset
  ingestion containing personal data, a DPIA must be completed before launch.

## 3. India DPDP Act 2023 alignment

- No "personal data" as defined in s.2(t) is collected, so the obligations on a
  Data Fiduciary (ss. 4–10) are not triggered in the current design.
- Should the system later process personal data of Indian principals, notice and
  consent (s. 5–6), purpose limitation, and breach notification to the Data
  Protection Board must be implemented first.

## 4. EU AI Act classification

- **Risk tier: limited risk.** The system generates content and interacts with a
  user but does not perform biometric identification, emotion recognition, social
  scoring, or safety-critical control, and is not used in any Annex III
  high-risk domain (it is explicitly out of scope for regulatory, employment,
  and essential-services decisions — see `docs/ETHICS.md §3`).
- **Transparency obligations (Art. 50)** are met: AI-generated output is clearly
  labelled as such in the UI, and users are told they are interacting with an AI
  system.

## 5. Security of processing

Authentication, transport hardening, rate limiting, and upload validation are
documented in `docs/SECURITY.md`.
