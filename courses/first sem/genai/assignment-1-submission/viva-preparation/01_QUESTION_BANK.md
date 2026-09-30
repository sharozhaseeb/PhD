# Likely viva questions and answer points

Answer directly, show the equation or evidence, then add one limitation. These are answer points, not scripts.

## A. Assignment and reproducibility

### 1. What did you implement?

A same-backbone AE/VAE comparison on CelebA, VAE interpolation and prior sampling, an MNIST denoising AE, deliberate GAN gradient death and mode collapse, a working DCGAN, WGAN-GP, and classifier-based reverse KL, IS, and FID with sanity checks.

### 2. Derive your assigned values.

`R=27`; seed is last four digits `1327`; held-out digit `27 mod 10=7`; `(27+3k) mod 10` gives `7,0,3,6,9,2`, sorted to `[0,2,3,6,7,9]`; `27 mod 6=3`, selecting `Blond_Hair`.

### 3. What is the main run identity?

`20L-11327_main_v1`, executed on CUDA with PyTorch `2.11.0+cu128`. All report numbers come from this run's saved artifacts.

### 4. Did every sub-run literally use seed 1327?

The main seed is 1327, but the notebook uses documented deterministic offsets for sub-experiments, samples, and reference sets. That improves isolation and reproducibility but is not literal compliance with the handout's wording; I would state this honestly.

### 5. Why use fixed noise?

The same latent vectors across checkpoints isolate training progress. Changing `z` would confound model improvement with different random samples.

### 6. What did the preflight tests prove?

They checked wiring and capacity, not final quality: AE `.08841->.00226`, VAE reconstruction `.10547->.00240`, denoiser `.23297->.01328`, classifier `1.78433->4.09e-6` on ten images, plus finite GAN gradients over 20 steps.

### 7. What is odd about the handout numbering?

It references A4, B2, and Parts A-F without defining those tasks; the footer says Assignment 2; and it requests filename `A2_<roll>.ipynb`. I followed explicit deliverables and did not invent missing work.

### 8. Why is held-out digit 7 not used?

It appears intended for a missing anomaly task/B2. The supplied B1 is denoising, so inventing an anomaly experiment would not answer a defined question.

## B. AE and VAE

### 9. Trace the CelebA encoder.

`3x64x64 -> 32x32x32 -> 64x16x16 -> 128x8x8 -> 256x4x4 -> 4096`. The AE head outputs 64; the VAE head outputs 128 split into 64-dimensional `mu` and `logvar`.

### 10. Trace the decoder.

Latent 64 goes through a linear layer to `256x4x4`, then transposed convolutions produce `128x8x8`, `64x16x16`, `32x32x32`, and `3x64x64`, ending with sigmoid.

### 11. Derive the VAE KL term.

For one coordinate, `KL(N(mu,sigma^2)||N(0,1)) = .5*(mu^2+sigma^2-1-log(sigma^2))`. Since `logvar=log(sigma^2)`, code uses `.5*(exp(logvar)+mu^2-1-logvar)`, sums 64 dimensions, and averages the batch.

### 12. Why `exp(0.5*logvar)`?

`logvar=log(sigma^2)`, so `sigma=exp(logvar/2)`.

### 13. Why predict log variance?

It is unconstrained on the real line and exponentiation guarantees positive variance. It is also convenient for the analytic KL.

### 14. Explain reparameterization.

`z=mu+sigma*epsilon`, with `epsilon~N(0,I)`. Randomness is moved into an input independent of encoder parameters, so ordinary backpropagation reaches `mu` and `logvar`.

### 15. Why does validation decode `mu`?

It removes Monte Carlo sampling noise and produces deterministic reconstructions. Training samples `z`, and BatchNorm also changes train/eval behavior, so train and validation reconstruction numbers are not identical inference conditions.

### 16. How is the VAE loss scaled?

The code uses pixel-mean MSE plus `KL/(3*64*64)`. Multiplying by 12,288 yields per-image `SSE+KL`, so it is the beta=1 objective divided by a fixed constant, not a smaller beta.

### 17. What were the A1 results?

AE train/validation MSE `.00668376/.00660486`; VAE `.00993852/.00830132`. The validation gap is `.00169646`, about 25.7% above the AE value.

### 18. Why is the VAE blurrier?

KL trades exact reconstruction capacity for prior-compatible overlapping posteriors, and MSE favors pixel averages. The measured validation gap quantifies this run's tradeoff.

### 19. Why interpolate means instead of samples?

Means provide stable representative endpoints. Sampled endpoints add epsilon noise and would confound the attribute path.

### 20. What happened in A2?

Both 11-frame strips stayed face-like. Smile strengthened around/after the middle and hair changed progressively, but identity and hair shape also changed, showing entanglement rather than a pure causal attribute axis.

### 21. Which A2 endpoints were saved?

Smiling used negative index 22017 and positive 2816. Blond_Hair used negative 2816 and positive 22017, recorded in `evidence/A2_endpoints.json`.

### 22. Does a VAE guarantee plausible interpolation or disentanglement?

No. KL encourages a populated continuous latent region, but it is not a proof. The observed identity changes explicitly show the direction is entangled.

### 23. Why did AE normal-prior samples fail?

The AE decoder only trained on the encoder's aggregate code distribution, which was not constrained to equal `N(0,I)`. Arbitrary normal draws are off-manifold.

### 24. How do you know the AE decoder itself works?

It decodes codes produced by its own encoder into recognizable faces. A3 shows this control beside the failed normal-prior row.

### 25. Did the AE output literally “nothing”?

No. The observed outputs were blurred brown face-like averages. I would describe my figure rather than repeat the handout's dramatic wording.

## C. Denoising and classifier

### 26. Define PSNR.

For `[0,1]` data, `PSNR=10*log10(1/MSE)`. The implementation computes per-image values and averages them.

### 27. What was the denoising result?

Mean PSNR rose from `13.3204` to `19.4447 dB`, a `6.1242 dB` gain, on one saved seeded 1,000-image test set.

### 28. Why clip noisy inputs?

MNIST is normalized to `[0,1]`; clipping `x+0.3*epsilon` keeps the corrupted image in the valid input range.

### 29. Why can an AE denoise but fail at unconditional generation?

Denoising is conditional projection from a nearby corrupted observation toward the learned digit manifold. Unconditional generation requires a known latent prior, which a plain AE lacks.

### 30. How reliable is the mode classifier?

It reached 99.019% restricted-test accuracy and has a saved confusion matrix. It is strong in-domain, but generated artifacts are out-of-distribution and may receive overconfident labels, so grids remain important.

### 31. Trace the classifier.

`1x28x28 -> conv32/pool -> 32x14x14 -> conv64/pool -> 64x7x7 -> 3136 -> 128 features -> 6 logits`. The frozen model supplies labels, IS probabilities, and FID features.

## D. C1 and C2 gradient death

### 32. Derive the saturating generator gradient.

For fake logit `a`, `D=sigmoid(a)` and `L_sat=log(1-D)=-softplus(a)`. Therefore `dL/da=-D`, which vanishes when `D` confidently rejects fakes.

### 33. Derive the non-saturating gradient.

`L_ns=-log D=softplus(-a)`, so `dL/da=-(1-D)`. When `D approximately 0`, the signal remains near `-1`.

### 34. Do the two losses have the same objective everywhere?

No. They have the same desired/Nash equilibrium but different scalar objectives and gradient fields away from equilibrium.

### 35. Why use softplus?

It expresses logistic losses stably in logit space. Explicit `log(sigmoid(a))` or `log(1-sigmoid(a))` can underflow at extreme logits.

### 36. What exactly changed from C1 to C2?

Only the generator loss branch. Seed, architecture, zdim 64, 3,000 outer iterations, five D steps, one G step, learning rates, and fixed-noise procedure were held constant.

### 37. Calculate the C1 death threshold.

At iteration 100, first-layer norm was `7.0218186e-05`; one percent is `7.0218186e-07`. Iteration 448 is the first later row below it, with a logged norm of zero.

### 38. Is the zero gradient mathematically exact?

It is exactly zero in the saved floating-point log, not a claim that the analytic derivative is identically zero. Extreme logits/probabilities can underflow numerically.

### 39. What is unusual about rows 447 and 448?

The curve has a sharp numerical excursion before the zero at 448; it is not a perfectly smooth decay. The defensible claim is the first threshold crossing defined by the CSV.

### 40. What gradient norm was used?

`g_grad_norm` is the L2 norm of the first parameter tensor in `G.fc`, after backward and before the step. `g_full_grad_norm` combines all generator parameter gradients. The threshold uses the first-layer hook; both were zero at 448.

### 41. What was C2's gradient at the matched iteration?

At 448, first-layer norm was `3.836562` and full norm `11.295707`, while its samples already resembled digits.

### 42. Why detach fake images in the D update?

The D update should not accumulate generator gradients. In the G update, D parameters are frozen but autograd still differentiates D's output with respect to its input, so gradients reach G.

### 43. Why did five D steps and higher D LR hurt C1?

D separated real and fake too quickly, driving fake logits strongly negative. The saturating derivative is proportional to `D(fake)`, so the generator lost its learning signal.

## E. Mode collapse and DCGAN

### 44. What forced C3 to collapse?

The combined recipe: zdim 2, no G BatchNorm, five G updates per D update, `lr_G=2e-3`, and `lr_D=2e-4`. Low z alone is not proven to be the sole cause.

### 45. What counts as a covered mode?

A predicted class proportion of at least 1%; with 5,000 samples that means at least 50 assignments.

### 46. Derive C3's reverse KL.

With uniform target and all mass on one class, `KL(p_gen||p_data)=1*log(1/(1/6))=log 6=1.791759`. Zero-mass generated classes contribute zero by limit.

### 47. Why call it reverse KL, and what is its blind spot?

The direction is generated-to-data. Missing real modes with `p_gen=0` contribute nothing directly; forward KL would diverge there. Concentrating mass still produces the maximum `log 6` in this six-class case.

### 48. Which class received all C3 samples?

Actual digit 3, which is remapped class index 2. Counts are `[0,0,5000,0,0,0]` for digits `[0,2,3,6,7,9]`.

### 49. What makes D1 a DCGAN-style model?

Strided convolutions, transposed convolutions, BatchNorm in G and after D's second convolution, ReLU in G, LeakyReLU(.2) in D, tanh output, Adam `2e-4` with beta1 `.5`, non-saturating loss, and 1:1 updates.

### 50. Trace the GAN shapes and ranges.

G maps `(B,64)` to `128x7x7`, `64x14x14`, then `1x28x28` in `[-1,1]`. Real images use `2x-1`; generated images use `(x+1)/2` before classifier evaluation. D ends in one logit.

### 51. What was D1's class balance?

Proportions `[.1970,.0740,.2452,.1622,.1470,.1746]`; all six modes are covered, but the distribution remains skewed. Reverse KL is `.052779`.

## F. WGAN-GP

### 52. State the WGAN-GP losses.

Critic minimizes `mean(C(fake))-mean(C(real))+lambda*GP`; generator minimizes `-mean(C(fake))`. Here lambda is 10.

### 53. Why is it called a critic?

It outputs unrestricted real scores, not probabilities, and has no sigmoid. D2's `D_x` and `D_G_z` columns are therefore critic scores.

### 54. Derive the gradient penalty.

Sample `alpha`, interpolate `x_hat=alpha*real+(1-alpha)*fake`, differentiate `C(x_hat)` with respect to `x_hat`, and penalize `(||grad C||_2-1)^2` averaged over the batch.

### 55. Why is `create_graph=True` required?

The critic loss must backpropagate through the calculated input gradient norm, so autograd needs a differentiable graph for that gradient operation.

### 56. Why enforce 1-Lipschitz behavior?

The Kantorovich-Rubinstein dual form of Wasserstein-1 requires a 1-Lipschitz critic. The penalty softly enforces this near real-fake interpolation paths.

### 57. Why no critic BatchNorm?

BatchNorm makes one sample's score depend on other batch samples, interfering with a per-sample input-gradient constraint. G still uses BatchNorm.

### 58. Why five critic steps?

They keep the critic closer to its current optimum so its score difference gives G a useful direction. This is not logistic saturation because the WGAN generator gradient has no sigmoid factor.

### 59. What were D2's results?

Proportions `[.1494,.1594,.2286,.1574,.1850,.1202]`, six modes, reverse KL `.019803`, IS `4.61896+/-0.08984`, and FID `17.11675`.

### 60. Does D2 isolate gradient penalty as the cause?

No. Relative to D1 it also changes objectives, critic-update ratio, optimizer settings, and critic BatchNorm. It demonstrates the WGAN-GP configuration's result, not a one-factor ablation.

## G. IS and FID

### 61. Derive Inception Score.

`IS=exp(E_x KL(p(y|x)||p(y))) = exp(H(p(y))-E_x H(p(y|x)))`. It rewards confident per-sample predictions and a diverse marginal.

### 62. What is the IS range here?

With six classes, ideal confident balanced predictions approach 6; identical/uninformative predictions give 1. Real data scores 5.772 rather than 6 because of classifier uncertainty and empirical imbalance.

### 63. How were IS splits computed?

Five thousand samples were divided into 10 disjoint chunks of 500. Each produces a score; NumPy mean and population standard deviation are reported. Epsilon `1e-12` prevents `log(0)`.

### 64. What is IS blind to?

It never compares against real data, depends on this classifier, can miss within-class collapse, and can reward confident unrealistic or adversarial images.

### 65. Why was C3 IS approximately 1?

Every sample had nearly the same predicted class, so `p(y|x)` and marginal `p(y)` were nearly equal and the KL was near zero.

### 66. Derive FID.

Fit Gaussians to 128-D classifier features and compute `||mu_r-mu_g||^2 + Tr(Sigma_r+Sigma_g-2*(Sigma_r*Sigma_g)^(1/2))`.

### 67. What exact FID reference was used?

Every E row uses a seeded 5,000-image real training feature set as reference. The `real` row is a 5,000-image real test set against training, so it has FID 1.39865 rather than zero.

### 68. What is the FID floor experiment?

Two disjoint halves of the restricted real test set are compared, giving 1.200874. This estimates finite-sample feature-moment variation; it is not a universal mathematical lower bound.

### 69. Why can `sqrtm` return a complex result?

The covariance product is generally nonsymmetric and floating-point/singular calculations may introduce tiny imaginary components. The code checks magnitude, optionally retries with epsilon, rejects large imaginary parts, then takes the real part.

### 70. What happened numerically in this run?

Collapsed features could trigger a singular-covariance warning, but all distances remained finite; saved diagnostics show maximum imaginary component zero and no epsilon retry. A symmetric PSD method or diagonal regularization would be more robust.

### 71. Why is sigma=0 FID not exactly zero?

Identical data/features should give zero theoretically. The saved `4.84e-09` is floating-point/square-root residue and is clamped nonnegative.

### 72. Why is the noise curve expected to be monotone here?

The assignment treats monotonicity as a required sanity check. With the same base images/noise and increasing sigma, a broadly increasing curve is expected and was observed from approximately 0 to 543.036. I would not claim universal mathematical monotonicity for every nonlinear learned feature map, clipping rule, and finite sample.

### 73. What is FID blind to?

It reduces chosen features to Gaussian first and second moments, has finite-sample bias, and can miss higher-order structure or artifacts not represented by the classifier features.

### 74. Why is C1 FID worse than fully collapsed C3?

C3's classifier-feature distribution happened to be closer to the real reference than C1's, despite having only one predicted mode. The grids suggest C3 is digit-like while C1 is high-frequency noise, but this is an interpretation consistent with the evidence, not a causal decomposition of the FID difference.

### 75. State the complete E table.

Real `5.7720+/-0.0262 / 1.399`; C1 `1.0347+/-0.0011 / 941.881`; C3 `1.0006+/-0.000025 / 821.241`; D1 `4.4772+/-0.1080 / 39.700`; D2 `4.6190+/-0.0898 / 17.117`, where each pair is IS/FID.

## H. Ownership, limitations, and debugging

### 76. What is the correct troubleshooting order?

Read saved curves, inspect shapes/ranges, overfit ten examples, run a short smoke test, and only then change architecture. The saved preflight logs show this process.

### 77. What are the main limitations?

Deterministic seed offsets rather than literal seed reuse; classifier proxies on generated/OOD data; no quantitative “samples stopped changing” criterion for C3; entangled A2 endpoints; singular-covariance risk; and no causal ablation isolating gradient penalty.

### 78. What assistance was used?

AI assistance helped inspect the handout/starter, draft standard PyTorch code, operate the Colab run, and assemble materials. It is disclosed. The measured claims come from the saved run, and ownership must be demonstrated by deriving, tracing, and modifying the code live.

### 79. What code should you be able to write unaided?

`kl_term`, reparameterization, the two generator losses, `mode_stats`, `gradient_penalty`, `inception_score`, and the FID mean/covariance calculation and checks.

### 80. What is the strongest correctness evidence?

No single result. Together: preflight overfits/smoke tests, full per-iteration logs, exact threshold row, fixed-noise comparisons, classifier confusion matrix, saved sample histograms, metric split CSVs, FID sanity checks, and agreement between report, JSON, CSVs, and figures.
