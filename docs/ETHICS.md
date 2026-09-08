# UrbanGen AI — Ethics Statement

_Course context: Generative AI (2304422T / 2304422L), Unit 6 — Ethical, Societal, and Legal Dimensions._

UrbanGen AI generates **advisory** urban-planning material — image reconstructions,
land-use classifications, latent-space explorations, and natural-language planning
recommendations. It is a teaching / research prototype, not a decision system.

## 1. Core principles

| Principle | How it is applied here |
|---|---|
| **Human oversight** | Every output is framed in the UI as *advisory only — requires review by qualified urban planners*. No output is auto-actioned. |
| **Transparency** | Model architecture, training data, and known limits are published (`docs/MODEL_CARD.md`) and surfaced in the app's Governance page. Generated content is labelled as AI-generated (EU AI Act transparency obligation). |
| **Accountability** | Single-repository, MIT-licensed, versioned. Issues and model changes are tracked in git history. |
| **Fairness / bias mitigation** | See §2 — biases are disclosed rather than hidden, and the system is scoped to non–rights-affecting use. |
| **Privacy** | No personal data is collected or processed. See `docs/PRIVACY.md`. |
| **Sustainability** | Small models, single-GPU training. Approximate energy/carbon footprint is reported in `docs/MODEL_CARD.md`. |

## 2. Known biases and limitations

- **Geographic / distribution shift.** The Autoencoder, VAE, and classifier are
  trained on **UCMerced (United States)** and **EuroSAT (Europe)** aerial imagery.
  The planning-text model is trained on a **hand-authored English corpus**. All of
  this is then applied to **Pune, India**. Urban form, vegetation, construction
  materials, and informal settlements in Pune are under-represented or absent in
  the training data, so reconstructions, anomaly scores, and recommendations will
  be least reliable exactly where local context matters most.
- **The "RAG" assistant is keyword-based**, not a learned retrieval system, and
  answers only from a small curated Pune fact set.
- **The planning-text generator is a small char-level model** trained from
  scratch on a limited corpus. It produces plausible-sounding planning prose but
  has no factual grounding, no citations, and can contradict itself. Treat every
  sentence as a prompt for a human expert, never as a finding.
- **Anomaly detection** flags *statistical* deviation from the training
  distribution, which conflates genuine land-use change with out-of-domain
  imagery and sensor artefacts.

## 3. Misuse boundaries

- No face, person, licence-plate, or other individual-level recognition.
- No deepfake or photo-realistic synthetic-media generation of real people or places.
- Not for regulatory approval, property valuation, insurance underwriting, law
  enforcement, or any use that materially affects an individual's rights or access
  to services.
- Generated plans must not be presented to the public or to authorities as
  professional planning advice.

## 4. Societal considerations (Unit 6)

- **Misinformation:** generated text is watermarked in-context as AI-generated and
  advisory; it is not publishable as fact.
- **Job displacement:** positioned as a drafting aid for planners, not a replacement.
- **Cultural diversity / Indian context:** the bias disclosure above is explicit
  precisely because the datasets are Western; extending to Indian geospatial data
  is listed as required future work.
