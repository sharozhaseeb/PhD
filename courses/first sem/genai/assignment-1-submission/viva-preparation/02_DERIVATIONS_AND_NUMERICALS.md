# Derivations and numerical checks

## 1. AE and VAE objectives

For an AE, `z = encoder(x)` and `x_hat = decoder(z)`. The submitted reconstruction quantity is mean squared pixel error:

`MSE = (1 / (N*C*H*W)) * sum((x_hat-x)^2)`.

For a diagonal Gaussian posterior, the encoder returns `mu` and `logvar = log(sigma^2)`. The reparameterized sample is:

`epsilon ~ N(0,I)`, `z = mu + exp(0.5*logvar) * epsilon`.

Randomness is isolated in epsilon, while `z` remains differentiable with respect to `mu` and `logvar`.

Against `p(z)=N(0,I)`, the KL for one example is:

`KL(q||p) = 0.5 * sum(exp(logvar) + mu^2 - 1 - logvar)`.

The code averages KL across the batch and uses:

`loss = pixel_mean_MSE + KL_per_image / (3*64*64)`.

Multiplying by `3*64*64` gives per-image `SSE + KL`, so this is beta=1 ELBO scaling divided by one fixed positive constant. It changes the displayed scale, not the optimizer's minimizer.

Measured comparison: AE validation MSE `0.0066048581`; VAE `0.0083013152`; VAE reconstruction gap `0.0016964571`, about 25.7% relative to the AE value. The KL regularizes the latent distribution, trading some reconstruction sharpness for meaningful prior sampling.

## 2. Why the A3 control matters

The AE decoder succeeds on codes produced by its own encoder but fails on the same `N(0,I)` draws that produce face-like VAE samples. Therefore the AE decoder is not simply broken. The AE aggregate posterior was never constrained to match the normal prior, so arbitrary normal samples land off the learned code manifold.

VAE interpolation uses posterior means, not random posterior samples:

`z_t = (1-t)*mu_1 + t*mu_2`, for `t=0,.1,...,1`.

Using means removes sampling noise. The strips remain plausible, but smile, hair, and identity change together, so the direction is smooth but not disentangled or causal.

## 3. PSNR

For data in `[0,1]`:

`PSNR = 10*log10(1/MSE)`.

The noisy baseline was `13.3204 dB`; the denoised output was `19.4447 dB`, a gain of `6.1242 dB`. A denoiser is conditional: the corrupted input anchors the output near the data manifold. It does not need an unconditional sampling prior.

## 4. Logistic GAN losses and gradient death

Let `a` be the discriminator fake-sample logit and `D = sigmoid(a)`.

Saturating/minimax generator loss:

`L_sat = log(1-D)`.

Since `dD/da = D(1-D)`, then:

`dL_sat/da = -D`.

When a strong discriminator gives fake samples `D approximately 0`, the generator's signal vanishes.

Non-saturating loss:

`L_ns = -log(D)` and `dL_ns/da = -(1-D)`.

When `D approximately 0`, this derivative is approximately `-1`. Both objectives have the same ideal generator fixed point but very different optimization fields away from equilibrium.

The stable code forms are `-softplus(a)` for the saturating objective and `softplus(-a)` for the non-saturating objective.

### Run-specific threshold

- Iteration 100 first-layer gradient norm: `7.021818601e-05`.
- One percent: `7.021818601e-07`.
- First later row below the threshold: iteration 448.
- At 448: first-layer norm `0`, full-generator norm `0`, and `D(G(z))=0`.
- C2 at the same iteration: first-layer norm `3.836562`, full norm `11.295707`.

The trace is not a perfectly smooth decay. Row 447 has a sharp numerical excursion before row 448 reaches zero. Describe the measured first crossing, not an invented smooth story.

## 5. Gradient norm definitions

The starter hook measures the first parameter tensor in `G.fc`, while the handout wording refers more generally to the generator-gradient L2 norm:

`g_grad_norm = ||grad(first G.fc parameter)||_2`.

The submission also records:

`g_full_grad_norm = sqrt(sum_p ||grad(p)||_2^2)`.

The reported death threshold uses the starter's first-layer norm. The submission additionally logs the full-generator norm as supporting evidence; it also equals zero at iteration 448.

## 6. Mode coverage and reverse KL

With 5,000 samples, a mode is covered if its class proportion is at least 1%, meaning at least 50 samples.

For target `q_i=1/6` and generated proportions `p_i`:

`D_KL(p_gen || p_data) = sum_{i:p_i>0} p_i*log(p_i/(1/6))`.

C3 counts are `[0,0,5000,0,0,0]`, so `p=[0,0,1,0,0,0]` and:

`KL = 1*log(1/(1/6)) = log(6) = 1.791759`.

Terms with `p_i=0` contribute zero by the limit `p log p -> 0`. Digit 3 is the actual digit and class index 2 in `[0,2,3,6,7,9]`.

## 7. DCGAN

The generator maps `(B,64)` to `(B,128,7,7)`, then transposed convolutions to `(B,64,14,14)` and `(B,1,28,28)`. Tanh produces `[-1,1]`, matching real images transformed by `2*x-1`.

The discriminator maps `(B,1,28,28)` to 14x14 and 7x7 feature maps, then one logit. D1 uses strided convolutions, G BatchNorm, D BatchNorm after its second convolution, ReLU in G, LeakyReLU(0.2) in D, Adam `2e-4` with beta1 `.5`, non-saturating loss, and 1:1 updates.

Fixed `z` at four checkpoints controls sample identity, so the progression shows learning rather than cherry-picking different random samples.

## 8. WGAN-GP

The critic has no sigmoid. Its outputs are unrestricted scores, so D2's `D_x` and `D_G_z` log columns are not probabilities.

Critic objective minimized by the code:

`L_C = mean(C(fake)) - mean(C(real)) + lambda*GP`.

Generator objective:

`L_G = -mean(C(fake))`.

For `alpha ~ Uniform(0,1)`:

`x_hat = alpha*x_real + (1-alpha)*x_fake`.

`GP = mean((||grad_x_hat C(x_hat)||_2 - 1)^2)`.

The run uses five critic steps, `lambda=10`, Adam `1e-4`, betas `(0,.9)`, and no critic BatchNorm. BatchNorm couples examples, making the per-example input-gradient constraint ambiguous.

D2 ties D1 at six covered modes and improves balance, IS, and FID. Say it improved the reported distribution metrics, not that it was universally superior under all possible criteria.

## 9. Inception Score

For each generated sample the six-digit classifier supplies `p(y|x)`. Within each split:

`p(y) = mean_x p(y|x)`.

`IS = exp(mean_x KL(p(y|x) || p(y)))`.

High IS requires confident conditional predictions and a diverse marginal. The implementation splits 5,000 samples into 10 groups of 500 and reports mean and population standard deviation over split scores.

C3 has IS `1.0006`: every image is assigned the same class, so `p(y|x)` is nearly equal to `p(y)` and KL is near zero. IS never compares generated images with real images, so it can miss realism failures not exposed by its classifier.

## 10. Classifier-feature FID

The classifier's 128-dimensional penultimate features give real and generated matrices of shape `(5000,128)`. For means and covariances:

`FID = ||mu_r-mu_g||^2 + Tr(Sigma_r + Sigma_g - 2*(Sigma_r*Sigma_g)^(1/2))`.

The generated sets are compared against a seeded 5,000-image real training reference. The real row in `E_summary.csv` is a separate real test subset evaluated against that training reference, so its FID is not zero.

`Sigma_r*Sigma_g` is generally nonsymmetric. `scipy.linalg.sqrtm` may return tiny imaginary components from floating-point error; the code accepts only small components, takes the real part, retries with diagonal epsilon for nonfinite or large-imaginary results, and clamps tiny negative final distances to zero.

Collapsed samples make feature covariance low-rank, which can trigger a singular-matrix warning. The values remained finite and the saved diagnostic showed zero imaginary component and no epsilon retry. A warning is not proof of correctness; diagonal regularization or a symmetric PSD formulation would be a stronger robustness check.

FID models only the first two moments of chosen features. It can miss higher-order differences and artifacts the classifier features ignore.

## 11. FID sanity checks

- Floor: two disjoint real test halves give `1.200874`, measuring finite-sample differences in empirical moments.
- Monotonicity: the same clean images plus clipped Gaussian noise give FID approximately `0,14.144,100.552,326.750,543.036` as sigma increases.
- Sigma 0 compares identical images/features, so only numerical roundoff remains: `4.84e-09`.

## 12. Complexity and reproducibility

Convolutional training cost is dominated by forward/backward convolutions and scales with batch size, spatial dimensions, kernel area, and channel products. WGAN-GP costs substantially more because it performs five critic updates per generator update and a second-order autograd graph for the input-gradient penalty.

The base seed is 1327, while documented offsets create deterministic substreams for data/noise/evaluation. This avoids accidental reuse and makes artifacts reproducible, but it is not literal compliance with “seed 1327 at the top of every run.” State this limitation plainly.
