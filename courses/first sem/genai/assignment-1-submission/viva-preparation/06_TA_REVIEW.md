# TA review and risk register

## Overall verdict before this package

The strict TA assessment judged the submission technically strong and approximately 40.5/41 on the visible marks. Report, notebook, logs, figures, metrics, and assigned values are mutually consistent. The viva risk is ownership and precision, not missing core experiments.

## Checks performed

- Read the complete handout and four-page report.
- Inspected the 36-cell executed notebook and matching Python source.
- Checked row counts and columns for every AE/VAE, denoising, classifier, GAN, IS, FID, and preflight log.
- Verified exact C1 rows 100 and 448 and the C2 matched row.
- Verified C3/D1/D2 counts, coverage, and reverse KL values.
- Verified all values in `metrics.json`, `E_summary.csv`, and the report.
- Checked the WGAN-GP, IS, FID, and validation code paths.
- Reviewed reproducibility metadata, fixed indices, fixed noise, and LLM declaration.

## Strengths

- Numerical claims are backed by raw saved evidence rather than generic explanations.
- Negative results are preserved and explained honestly.
- C1/C2 is a controlled one-line loss comparison.
- Both required and full-generator gradient norms are logged.
- The classifier has an accuracy gate and confusion matrix.
- IS split scores and FID diagnostics are saved.
- Preflight overfits and smoke tests demonstrate a natural debugging process.
- Report fits the four-page limit and directly uses the measured run.

## High-risk viva issues

1. Row 447-to-448 is abrupt; never describe a smooth monotone gradient death.
2. The death threshold is based on the first generator layer, not the full norm.
3. VAE KL scaling must be explained as fixed objective scaling, not beta reduction.
4. WGAN critic columns are scores, not probabilities.
5. A singular covariance warning is expected under collapse but still deserves a numerical caveat.
6. Seed offsets are reproducible but not literal compliance with resetting 1327 each run.
7. D2 is not a one-factor ablation of gradient penalty.
8. A2 is entangled and C3 lacks a quantitative temporal stopping criterion.
9. AI assistance is substantial and disclosed, so code ownership will be tested.

## Handout/starter traps

- A1-A3 sum to 8 although Part A says 12 marks.
- A4, B2, and Part F are referenced but absent.
- The footer says Assignment 2 while the title says Assignment 1.
- The requested filename is `A2_<roll>.ipynb`.
- The handout requires D BatchNorm for D1, while the starter base discriminator omitted it; the submission added it.
- The starter-compatible norm is first-layer, while the prose can sound like full-generator norm; the submission logged both.
- A built-in spectral-normalization option would violate “implement it”; the submission instead implements WGAN-GP manually.
