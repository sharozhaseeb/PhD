# Code and evidence walkthrough

## Executed notebook map

| Notebook cell | Purpose | Must explain |
|---|---|---|
| 2 | Setup and reproducibility | roll parsing, seed, device, paths |
| 4 | Evidence helpers | CSV writing, finite checks, gradient norms, preflight gates |
| 6 | Data | CelebA cache/split, digit restriction and remapping |
| 8 | AE/VAE | common backbone, reparameterization, KL scaling, training |
| 10 | A2 | endpoint selection and mean-code interpolation |
| 12 | A3 | shared prior codes and AE own-code control |
| 14 | B1 | corruption, denoiser, PSNR |
| 16 | Classifier | six-class mapping, 128-D features, accuracy gate |
| 18 | GAN core | G/D shapes, stable losses, logging, fixed z |
| 20 | C1 | saturating loss and gradient death |
| 22 | C2 | one-line loss change and matched comparison |
| 24 | Mode helpers | sample collection, histogram, coverage, reverse KL |
| 26 | C3 | forced-collapse configuration |
| 28 | D1 | DCGAN configuration and fixed progression |
| 30 | D2 | manual WGAN-GP implementation |
| 32 | E | manual IS/FID and sanity checks |
| 34 | Validator | required files, columns, finite values |

## Matching Python source map

| Lines | Topic |
|---|---|
| 45-118 | roll values, device, and seed setup |
| 138-225 | evidence helpers and checkpoint metadata |
| 270-388 | data wrappers, CelebA cache, fixed split |
| 390-490 | AE/VAE architecture, KL, reconstruction epoch |
| 520-674 | A1 training, A2 interpolation, A3 sampling |
| 681-788 | denoising AE and PSNR |
| 799-902 | six-digit classifier |
| 917-974 | G28, D28, and per-iteration logger |
| 1005-1073 | logistic GAN loop and death detection |
| 1196-1248 | classifier sampling and mode measurements |
| 1254-1280 | C3 and D1 configurations |
| 1286-1358 | WGAN-GP penalty and training loop |
| 1364-1404 | IS and FID implementations |
| 1415-1493 | evaluation sets, floor, and noise sanity check |
| 1499-1556 | package validation and final checks |

## Evidence map

| Claim | Open this file | What to point at |
|---|---|---|
| Assigned values/configs | `run_config.json` | R, seed, digits, attribute, every run setting |
| AE/VAE values | `evidence/A1_ae.csv`, `evidence/A1_vae.csv` | final epoch train/validation rows |
| A2 endpoints | `evidence/A2_endpoints.json` | saved indices and 11 t values |
| Denoising | `evidence/B1_denoise.csv`, `metrics.json` | final val MSE and both PSNR values |
| Classifier reliability | `evidence/classifier.csv`, `evidence/classifier_confusion.csv` | 99.019% and six-class errors |
| C1 death | `evidence/key_rows.csv`, `evidence/C1.csv` | rows 100, 447, 448 |
| C1/C2 mechanism | `figures/C2_overlay.png`, `evidence/C2.csv` | matched iteration 448 |
| C3 collapse | `evidence/C3_counts.csv`, `figures/C3_hist.png` | digit 3 count 5000 |
| D1 balance | `evidence/D1_counts.csv`, `figures/D1_progress.png` | all modes, fixed-z progression |
| D2 improvement | `evidence/D2_counts.csv`, `evidence/final_model_comparison.csv` | reverse KL, IS, FID |
| IS split arithmetic | `evidence/E1_split_scores.csv` | 10 scores for each of five sets |
| FID sets | `evidence/E_summary.csv` | real/C1/C3/D1/D2 rows |
| FID monotonicity | `evidence/E3_noise_fid.csv` | five increasing rows |
| Process/authenticity | `evidence/experiment-diary.md`, `preflight_*.csv` | natural checks and observations |

## Live drill 1: prove iteration 448

1. Open `evidence/C1.csv`.
2. At iteration 100 point to `g_grad_norm=7.0218186e-05`.
3. Calculate one percent: `7.0218186e-07`.
4. Search later rows and show 448 is the first value below the threshold.
5. Point to first-layer and full norms both being zero at 448.
6. Inspect row 447 so you do not falsely describe a smooth decline.
7. Open `evidence/C2.csv` at 448 and contrast `3.836562` / `11.295707`.

## Live drill 2: recompute collapse metrics

1. Open `evidence/C3_counts.csv`.
2. Map class index 2 to actual digit 3.
3. Coverage threshold is 50 samples; only one row passes.
4. Compute `log(1/(1/6))=log(6)=1.791759`.
5. Explain why zero-mass terms contribute zero.

## Live drill 3: trace one IS split

1. Generated classifier probabilities have shape `(5000,6)`.
2. Each of 10 chunks has shape `(500,6)`.
3. Its marginal has shape `(1,6)`.
4. Calculate per-sample KL, average, exponentiate.
5. Locate the corresponding saved score in `evidence/E1_split_scores.csv`.

## Live drill 4: identify FID populations

1. The classifier produces `(5000,128)` features.
2. The common reference is a seeded real training subset.
3. The `real` row is a real test subset compared with training.
4. The floor is separate: two disjoint halves of the restricted real test set.
5. The monotonicity test compares clean images with clipped noisy versions of the same images.

## Live drill 5: trace WGAN-GP line by line

In `A1_working_source.py`, explain lines 1286-1298: interpolation, `requires_grad`, critic scores, `autograd.grad`, `create_graph`, flattening, L2 norm, and squared penalty. Then explain lines 1323-1334: critic objective, five critic updates, parameter freezing, generator objective, gradient logging, and optimizer step.

## Commands that need no GPU

```text
python practice_quiz.py
python -c "import pandas as pd; d=pd.read_csv('evidence/C1.csv'); print(d[d.iter.isin([100,447,448])])"
python -c "import pandas as pd; print(pd.read_csv('evidence/final_model_comparison.csv'))"
python -c "import json; print(json.load(open('metrics.json'))['E3_fid_floor'])"
```

## Natural intermediate work already preserved

- Ten-image AE, VAE, denoiser, and classifier overfit traces.
- A 20-step GAN smoke test with finite losses and gradients.
- Printed tensor shapes/ranges in the executed notebook.
- One CSV row per outer GAN iteration with frequent file flushing.
- Fixed train/validation indices, evaluation indices, and sample seeds.
- Both first-layer and full-generator gradient norms.
- Classifier confusion matrix, raw IS split scores, and FID diagnostics.
- An experiment diary recording planned settings, observations, checks, actions, and evidence.

## Do not say

- Do not call D2 critic scores probabilities.
- Do not say C1 gradient decayed smoothly.
- Do not say D2 proves gradient penalty alone caused the improvement.
- Do not claim A2 found a disentangled or causal attribute direction.
- Do not call the FID floor a universal minimum.
- Do not say C3 obtained a respectable IS in this run.
- Do not say every sub-run literally used seed 1327.
- Do not invent the absent A4, B2, or Part F.
