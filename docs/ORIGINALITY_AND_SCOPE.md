# UrbanGenAI Paper Scope and Originality Safeguards

## Syllabus boundary

The paper reports the five generative model families specified by the
Generative Artificial Intelligence syllabus:

1. Autoencoder
2. Variational Autoencoder
3. Generative Adversarial Network
4. Transformer-based generative model (MiniGPT)
5. Diffusion Model

The ResNet-18 land-use classifier is a supporting discriminative model. It
provides zoning labels and independent evaluation of generated images; it is
not presented as an additional generative model family.

No new generative architecture is to be added to the paper without an explicit
syllabus justification and a separate implementation record.

## Original writing and citation rules

- Explain the project's own implementation, data, measurements, and
  limitations in original wording.
- Cite the source paper when describing an established architecture, equation,
  benchmark, or algorithm.
- Do not copy abstracts, related-work paragraphs, figure captions, or
  benchmark descriptions from external papers.
- Keep source-specific claims separate from results measured in this
  repository.
- Record whether a statement is a measured result, an implementation fact, a
  literature fact, or a limitation.
- Preserve dataset and checkpoint provenance for every reported number.

No process can guarantee a particular plagiarism or AI-similarity score.
These safeguards are intended to prevent copied text, unsupported attribution,
and claims that cannot be reproduced from this repository.

## Diffusion claim boundary

The current UCMerced diffusion checkpoint is a source-conditioned scenario
generator. UCMerced has no paired before/after planning labels, so the paper
must not call this checkpoint a validated future-land-use forecasting model.
Any change-mask or temporal prediction experiment must use a dataset with real
change supervision and must be reported separately from the static UCMerced
baseline.
