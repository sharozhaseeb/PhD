# Gen AI handwritten exam notes

37 handwritten PNG pages covering all seven available Gen AI lecture decks. Built with imagegen, with independent plan and per-page visual/mathematical review. All phases are cleared. The new extension adds 3 Diffusion Part 1 pages, 6 Diffusion Part 2 pages and 8 Transformer pages.

Read in the order below. For numerical pages, cover the answer and reproduce the formula, substitution and interpretation. Original toy examples are marked as practice; lecture example sources use PDF page positions. These pages are concise revision notes, alongside the lecture decks and the existing numerical-practice guide.

[Page-by-page plan](plan.md) · [Reference attributes](reference-attributes.md) · [Review evidence](review-log.md) · [Prompt set](generation-prompts.md) · [Exact content manifest](page-manifest.json)

## Lecture 1 — Introduction

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L1-01 | [Introduction: what a generative model learns](l1-01-introduction-what-a-generative-model-learns.png) | 3–4, 8–18, 22–28, 33–39 |
| L1-02 | [Bayes: from a generative model to a spam decision](l1-02-bayes-from-a-generative-model-to-a-spam-decision.png) | 29 |
| L1-03 | [Data vs model: fidelity, coverage and sampling](l1-03-data-vs-model-fidelity-coverage-and-sampling.png) | 37–41 |

## Lecture 2 — Autoencoders and VAEs

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L2-01 | [Autoencoder: reconstruction and a chain-rule update](l2-01-autoencoder-reconstruction-and-a-chain-rule-update.png) | 5–12 |
| L2-02 | [AE applications: targets, retrieval and thresholds](l2-02-ae-applications-targets-retrieval-and-thresholds.png) | 11–19 |
| L2-03 | [VAE: distributions, sampling and latent meaning](l2-03-vae-distributions-sampling-and-latent-meaning-v2.png) | 20–28, 46–54, 61–70 |
| L2-04 | [Discrete KL: direction and weighted log-ratios](l2-04-discrete-kl-direction-and-weighted-log-ratios.png) | 36–37 |
| L2-05 | [Gaussian KL: derive it, then calculate](l2-05-gaussian-kl-derive-it-then-calculate.png) | 38–45 |
| L2-06 | [VAE objective: reconstruction plus regularization](l2-06-vae-objective-reconstruction-plus-regularization-v2.png) | 29–35, 46–54 |
| L2-07 | [Reparameterization: gradients and latent interpolation](l2-07-reparameterization-gradients-and-latent-interpolation.png) | 55–64 |

## Lecture 3 — GANs Part 1

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L3-01 | [GAN: the game and loss arithmetic](l3-01-gan-the-game-and-loss-arithmetic.png) | 3–30, 40–44 |
| L3-02 | [GAN gradients: why non-saturating loss helps](l3-02-gan-gradients-why-non-saturating-loss-helps.png) | 28–41, 47 |
| L3-03 | [GAN: one complete alternating update](l3-03-gan-one-complete-alternating-update.png) | 28–29, 42–44 |
| L3-04 | [DCGAN: shapes and parameter counts](l3-04-dcgan-shapes-and-parameter-counts.png) | 45 |
| L3-05 | [GAN failures, diagnostics and latent arithmetic](l3-05-gan-failures-diagnostics-and-latent-arithmetic.png) | 46–70 |

## Lecture 4 — GANs Part 2

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L4-01 | [Conditional GAN: pairs, encodings and losses](l4-01-conditional-gan-pairs-encodings-and-losses.png) | 2–16 |
| L4-02 | [StackGAN: sketch, refine and conditioning augmentation](l4-02-stackgan-sketch-refine-and-conditioning-augmentation-v2.png) | 17–22 |
| L4-03 | [Inception Score: entropy, KL and a worked example](l4-03-inception-score-entropy-kl-and-a-worked-example.png) | 24–57 |
| L4-04 | [FID: means, covariances and a worked calculation](l4-04-fid-means-covariances-and-a-worked-calculation.png) | 58–82 |
| L4-05 | [Generative precision & recall: quality vs coverage](l4-05-generative-precision-recall-quality-vs-coverage.png) | 83–96 |

Corrected final pages use `-v2.png`. Earlier drafts are isolated in `review-history/` and excluded from the approved study set. No Deep Learning notes were created or edited.


[Extension page plan](extension-plan.md) · [Extension review](extension-review-log.md) · [Extension prompts](extension-generation-prompts.md) · [Numerical checks](extension-numerical-checks.json)

## Lecture 5 — Diffusion Models Part 1

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L5-01 | [Forward diffusion: why the square roots matter](l5-01-forward-diffusion-why-the-square-roots-matter.png) | 1–23 |
| L5-02 | [Closed-form noising: derive any timestep](l5-02-closed-form-noising-derive-any-timestep.png) | 24–34 |
| L5-03 | [Sequential vs one-shot: matching the noise correctly](l5-03-sequential-vs-one-shot-matching-the-noise-correctly.png) | 26–34 |

## Lecture 6 — Diffusion Models Part 2

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L6-01 | [Noise schedules: linear vs normalized cosine](l6-01-noise-schedules-linear-vs-normalized-cosine.png) | 2–10 |
| L6-02 | [Forward diffusion: the lecture's 2×2 numerical](l6-02-forward-diffusion-the-lecture-s-2-2-numerical.png) | 11–14 |
| L6-03 | [DDPM objective: from Gaussian KL to noise error](l6-03-ddpm-objective-from-gaussian-kl-to-noise-error.png) | 15–24 |
| L6-04 | [Noise prediction training: a loss and gradient update](l6-04-noise-prediction-training-a-loss-and-gradient-update.png) | 24–26, 32–35, 38–39 |
| L6-05 | [Reverse mean: derive the noise-prediction formula](l6-05-reverse-mean-derive-the-noise-prediction-formula.png) | 20–23, 43–46 |
| L6-06 | [Reverse sampling: a full stochastic step](l6-06-reverse-sampling-a-full-stochastic-step.png) | 27–31, 35–40 |

## Lecture 7 — Transformers

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| L7-01 | [Transformer: tokens, embeddings and the architecture](l7-01-transformer-tokens-embeddings-and-the-architecture.png) | 1–13, 53–56, 59–60 |
| L7-02 | [Self-attention: the lecture's robot calculation](l7-02-self-attention-the-lecture-s-robot-calculation.png) | 14–22 |
| L7-03 | [Multi-head attention, FFN and Add & Norm](l7-03-multi-head-attention-ffn-and-add-norm.png) | 23–29, 53–54 |
| L7-04 | [Positional encoding: the full d=10 example](l7-04-positional-encoding-the-full-d-10-example.png) | 30–52 |
| L7-05 | [Decoder self-attention: mask future tokens](l7-05-decoder-self-attention-mask-future-tokens.png) | 55–57 |
| L7-06 | [Cross-attention: the lecture's translation numerical](l7-06-cross-attention-the-lecture-s-translation-numerical.png) | 56, 58 |
| L7-07 | [Transformer training: teacher forcing and cross-entropy](l7-07-transformer-training-teacher-forcing-and-cross-entropy.png) | 59–63, 65–67 |
| L7-08 | [Generation: greedy decoding vs beam search](l7-08-generation-greedy-decoding-vs-beam-search.png) | 55, 59, 64 |

Lecture numbers in this index denote deck reading order. The extension covers the three newly copied PDFs, including corrected source arithmetic and clearly labelled practice examples.

[Download all 37 pages and review documents](../GenAI-handwritten-notes-v2.zip)
