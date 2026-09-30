# Generative AI Assignment 1 viva package

This package is tied to the executed run `20L-11327_main_v1` for roll `20L-11327`. It is designed for evidence-based viva preparation: every experimental claim points to a CSV, JSON row, figure, or notebook cell.

## Recommended order

1. `00_START_HERE.md` - the facts and actions that must be automatic.
2. `02_DERIVATIONS_AND_NUMERICALS.md` - VAE, GAN, WGAN-GP, reverse-KL, IS, FID, and PSNR.
3. `03_CODE_AND_EVIDENCE_WALKTHROUGH.md` - notebook cell map and live evidence drills.
4. `01_QUESTION_BANK.md` - likely questions with concise answer points.
5. `04_MOCK_VIVA.md` - conceptual and evidence-based practice rounds.
6. `05_FLASHCARDS.md` or `practice_quiz.py` - last-minute recall.
7. `VIVA_HANDBOOK.pdf` - printable compilation.

## Included evidence

- Executed notebook and matching Python source.
- Submitted four-page report, metrics, run configuration, and LLM declaration.
- All training/evaluation CSVs, including preflight traces and full GAN logs.
- Every final figure.
- Saved C1/C2 fixed-noise tensors for the matched comparison.
- Fixed train/validation/evaluation index arrays used by the run.
- Experiment diary and key C1 rows.
- Original handout and starter notebook under `reference/`.

## Important cautions

- Full marks cannot be guaranteed. The package maximizes readiness, but the student must derive and trace the work without reading a script.
- The handout contains numbering gaps: A4, B2, and Part F are referenced but not defined. Do not invent them.
- The run uses deterministic seed offsets for sub-experiments. This is reproducible but is not a literal use of seed 1327 at the top of every run; admit that clearly if asked.
- AI assistance was disclosed. Expect line-by-line questions on WGAN-GP, IS/FID, and the training loops.

## Live setup

Open this folder and keep `A2_20L-11327.ipynb`, `evidence/`, `figures/`, `metrics.json`, and `run_config.json` visible. The evidence drills do not require retraining or a GPU.
