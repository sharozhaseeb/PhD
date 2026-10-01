# Independent review — new lecture extension

Scope: Diffusion Models Part 1 (34 PDF pages), Diffusion Models Part 2 (46), and Transformer (68). The original twenty approved handwritten notes are unchanged.

## Source inspection

Independently rendered and viewed contact sheets for all 148 slides, including image-heavy formulas, examples and architecture diagrams. Cross-checked extracted text. Reviewer contact sheets are in `tmp/genai-handwritten-extension/reviewer/`.

### Essential coverage

- Diffusion Part 1: fixed forward/learned reverse process; why naive independent additive noise fails; variance-preserving coefficient derivation and its assumptions; alpha/beta/cumulative alpha; conditional Gaussian and one-shot sampling; combining independent Gaussian terms; scalar and image numerical examples.
- Diffusion Part 2: linear and normalized cosine schedules; 2×2 one-shot example; Gaussian posterior/mean/variance; noise-based clean estimate and reverse-mean derivation; ELBO terms and weighted versus simplified noise prediction; random-timestep training; U-Net/time inputs; complete stochastic reverse update and final-step exception; train/inference distinction and comparison.
- Transformer: architecture and embedding lookup; Q/K/V projections and shapes; scaled row-softmax weighted-value numerical; multihead concat/output projection; sinusoidal positional numerical and relative identity; FFN/residual/LayerNorm; causal/padding masks; decoder self-attention and cross-attention separate numericals; shifted teacher forcing, final logits/probabilities, sum/mean cross-entropy, and autoregressive inference.

### Source inconsistencies to correct in the new notes

1. Diffusion Part 1 pp.7–12: independent fresh increments give additive variance proportional to t, not the square of t. A statement using one repeated epsilon represents correlated noise and is a different process.
2. Diffusion Part 1 pp.16–21: variance stays one only under the stated unit-variance marginal assumption. Conditional variance given a fixed clean image is instead `1-alpha_bar_t`. Part 1 p.25 incorrectly conflates these and overstates a need for constant reverse variance.
3. Diffusion Part 2 p.6: cosine cumulative alpha requires normalization `f(t)/f(0)` so `alpha_bar_0=1`. Betas use ratios and clipping. Avoid claiming exact zero terminal alpha when beta is capped below one.
4. Diffusion Part 2 p.23: a timestep-dependent weight independent of theta can still change optimization by weighting timesteps; removing it yields a different simplified objective, not an algebraically identical loss.
5. Diffusion Part 2 p.31: reverse stochasticity is a DDPM sampling choice; deterministic samplers exist. Added noise does not guarantee novelty, prevent memorization, or prove generalization.
6. Transformer p.35: illustrative positional chart uses a base inconsistent with the standard 10000 formula. Use the declared base consistently.
7. Transformer p.42: dot-product expansion must have four additive terms. Its printed chain of products is incorrect. The pure unprojected positional identity gives cos of an offset; arbitrary projected content-plus-position scores need not depend only on the offset.
8. Transformer pp.38–46: being able to compute sinusoidal codes at unseen positions does not guarantee learned long-sequence generalization. Smoothness/periodicity does not uniquely identify distance from one component.
9. Transformer p.56: causal attention includes current and earlier input positions, with future positions masked before softmax. Shifted decoder inputs prevent current-target leakage. Padding masks are separate.
10. Transformer pp.65/67: sum versus mean cross-entropy conventions differ; show both with clear labels and preserve correct vocabulary indices. Softmax gives probabilities; log-softmax gives log probabilities.

## Page plan gate

**Decision: CLEARED FOR IMAGE GENERATION.** Independently reviewed all 17 exact page specifications and their source coverage: three Diffusion Part 1 pages, six Part 2 pages, eight Transformer pages. All substantial supplied learning topics and numericals are represented, including full reverse-mean algebra, complete matrix attention, all ten PE coordinates and causal/cross-attention distinctions.

Independently recomputed forward scalar/aggregate-noise values, the image noise coefficient, normalized cosine points, posterior coefficients/clean estimate, positional table, attention softmax/output, reverse sample, CE reductions and beam scores. Values are correct at the stated rounding. Important checkpoints: equivalent aggregate `.0701927033`; cosine cumulative alpha at t=1/2 `.8470121613/.4938435904`; noise coefficient at t=3 `.8637036529`; clean estimate `.5016738714`; reverse mean `.495312156`; CE sum `6.5431121654`.

Applied three small clarity corrections synchronously to `extension-plan.md` and `extension-manifest.json` before clearance:

- L5-01: included independent naive-additive variance `Var(x0)+t c²` and lack of signal-mean attenuation.
- L7-01: explicitly defined original embedding scale as `sqrt(d_model)`.
- L7-04: included the correct four additive projected content/position dot-product terms, correcting the slide's erroneous expansion.

Density: most pages have 25–29 short lines; L7-04 has 31 including its full PE table and corrected expansion. Use a wide table and deliberate two-column theory layout; do not shrink glyphs or omit any term. L7-02, L7-04, L7-06 and L6-05 have notation-heavy content and require close final PNG checks. No further plan corrections required.

## Generated PNG review

Completed: all 17 selected extension PNGs were independently inspected in full against the cleared manifest for mathematical validity, content completeness, notation and readability. All 17 pass. No PNG revision was required in this extension. The original 20 approved notes were not changed.

| Page | Decision | Independent PNG checks |
| --- | --- | --- |
| L5-01 | PASS | Full approved content retained; variance assumptions, independent additive-noise correction, conditional Gaussian, coefficient squares/square roots and scalar arithmetic correct. Readable layout and complete source footer. |
| L5-02 | PASS | Alpha/product definitions, independent Gaussian combination, variance simplification, conditional Gaussian and scalar numerical correct. Aggregate/last-noise distinction and forward-vs-generation caution complete. |
| L5-03 | PASS | Both sequential steps, equivalent aggregate calculation and recovery formula correctly rendered; same-sample versus same-distribution distinction complete and readable. |
| L6-01 | PASS | Linear/cosine formulas, f(0) normalization, beta cap, all displayed schedule numbers and realized-product caution correct. Signal-coefficient interpretation and compatible-sampler caveat complete. |
| L6-02 | PASS | All matrix entries, cumulative table, exact noise coefficient and four elementwise calculations correct and readable; no clipping or step-noise confusion. |
| L6-03 | PASS | Variational bound structure, equal-covariance KL, noise-error weighting coefficient and numeric KL accurate. Correct distinction between weighted bound and intentionally simplified unweighted objective retained. |
| L6-04 | PASS | Training inputs/target and random timestep logic complete; U-Net role, mean-loss derivatives and scalar weight update correct and readable. |
| L6-05 | PASS | Posterior coefficients/variance, clean estimate substitution, both coefficient simplifications and final reverse mean correct; full numerical check retained with precise subscripts. |
| L6-06 | PASS | Generation loop/final-noise exception, reverse mean, posterior variance choice, standard deviation and stochastic sample correct. Deterministic-sampler/memorization caveat and model comparison complete. |
| L7-01 | PASS | Embedding scaling/lookup/count, encoder/decoder block order and Q/K/V sourcing, score-shape complexity and positional equivariance distinction correct and readable. |
| L7-02 | PASS | All given and projected matrix entries, robot raw/scaled scores, stable softmax and corrected weighted output exact; row convention and rounding caveats complete. |
| L7-03 | PASS | Per-head/concatenated shapes, output projection, FFN, post-norm residual rule and token-wise normalization example correct; epsilon denominator readable and intact. |
| L7-04 | PASS | All five denominator/angle rows, full ten-coordinate PE vector, radian convention and pairwise cosine example correct. Four additive projected content/position dot-product terms and extrapolation limitation complete and readable. |
| L7-05 | PASS | Causal mask includes current position, excludes future positions before softmax, and distinguishes padding. Masked weights/output and first-position projected value numerical correct; shifted-input/SOS explanation retained. |
| L7-06 | PASS | Decoder query and encoder key/value roles, all raw/scaled scores, cross-attention weights, weighted output and matrix shapes correct. Source attention and row-wise softmax explanations complete and readable. |
| L7-07 | PASS | Vocabulary projection, shifted teacher-forcing inputs/targets, causal/padding treatment, all five true-token losses, sentence sum/token mean and softmax-logit derivative correct. Reduction and log-base cautions complete and legible. |
| L7-08 | PASS | Generation loop, cumulative log score and beam approximation correct. Tree branches match every conditional probability; all four joint probabilities, greedy/beam choices and two log scores correct. Length comparison and inference distinction retained. |

## Final extension clearance

**CLEARED for delivery:** all 17 final selected PNGs in `extension-manifest.json` (L5-01–03, L6-01–06, L7-01–08). Final file inventory confirms all 17 manifest filenames exist. Each PNG has received independent full-page visual and mathematical review; no unresolved correction or pending review remains. This clearance covers the three new lecture decks only.
