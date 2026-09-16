# Generative AI — Numerical Practice for Quizzes and Midterms

Use with the [support guide](support.md). These are original study exercises matched to the supplied lectures and assignment. They are not past papers, a marking scheme, or a prediction of assessment coverage.

**Jump to:** [Prerequisites](#prerequisites) · [Introduction](#n1) · [AE/VAE](#n2) · [GANs](#n3) · [Assignment calculations](#n4) · [GANs Part 2](#n5) · [Readiness check](#readiness)

## How to practise

Watch the conceptual explanation, then any verified worked-number video. Pause before the answer. Work on paper with the solution covered; show the formula, substituted numbers, intermediate results, and interpretation. Attempt the fresh retry before expanding its answer. Reattempt later without replaying the example.

Unless specified otherwise, `log` means the natural logarithm `ln`; losses are in nats. PSNR alone uses `log10`. Keep full precision internally and use the displayed decimals only as checkpoints. Distinguish variance `σ²`, standard deviation `σ`, and `logvar=ln(σ²)`. Every example states its sum/mean convention; changing it changes gradients and the balance between loss terms.

<a id="prerequisites"></a>
## Prerequisite check

| Skill | Try before continuing |
| --- | --- |
| Conditional probability | If `P(A)=.4`, `P(B|A)=.6`, find `P(A,B)`. Is it necessarily `P(A|B)`? |
| Natural logs | Calculate `−ln(.5)` and `ln(4)`. |
| Variance and sampling | If `logvar=ln(4)`, what are `σ²`, `σ`, and `z=μ+σε` for `μ=1, ε=−.5`? |
| Mean versus sum | Errors `.1,−.2,.3,−.4`: find summed squared error and mean squared error. |
| Chain rule | If `s=2w`, `p=σ(s)`, and `L=−ln(p)`, find `dL/dw` at `w=0`. |
| Matrix shapes | A batch `X` has shape `5×3`; `W` is `3×2` and `b` is `1×2`. Find the output shape and number of trainable values. |

<details>
<summary>Check prerequisite answers</summary>

Joint probability **.24**; a posterior needs division by `P(B)`. Logs **.693147** and **1.386294**. Variance **4**, standard deviation **2**, sample **0**. SSE **.30**, MSE **.075**. At zero, `p=.5`, so `dL/dw=(p−1)×2=−1`. Output **5×2**, parameters **8**. If the chain rule or shapes are unfamiliar, use the [Deep Learning support guide](../Deep%20Learning/support.md) before a complete VAE/GAN update.

</details>

<a id="n1"></a>
## Lecture 1 — Probability and distribution understanding

<a id="n1-1"></a>
### N1.1 The lecture's spam example, fully normalized

**Source connection:** Introduction page 29. **Video route:** [StatQuest — Naive Bayes](https://www.youtube.com/watch?v=O2L2Uv9pdDA&t=262s), **4:22–7:33 · 3:11**, supplies a worked word-count classification example. Here we use the lecture's **binary presence of one word** instead.

Let `S` mean spam, `H` ham, and `W` presence of “win.” Given `P(S)=.4`, `P(H)=.6`, `P(W|S)=.6`, `P(W|H)=.05`:

| Joint event | Calculation | Probability |
| --- | --- | ---: |
| Spam and word present | `.4×.6` | .24 |
| Ham and word present | `.6×.05` | .03 |
| Spam and word absent | `.4×.4` | .16 |
| Ham and word absent | `.6×.95` | .57 |

All four cells sum to one. The word is present with probability `.24+.03=.27`, giving

`P(S|W)=.24/.27=8/9≈.888889`, and `P(H|W)=.03/.27=1/9≈.111111`.

For absence, `P(not W)=.16+.57=.73`, so `P(S|not W)=.16/.73≈.219178`. Notice that this is **not** `1−P(S|W)`: that complement would be ham conditional on the word being present.

With equal error costs and a `.5` threshold, classify a word-present message as spam and a word-absent message as ham. This is classification derived from a generative joint model. It models one feature and a class, not a fluent language model.

**Try it:** Change only the given probabilities to `P(S)=.2`, `P(W|S)=.5`, `P(W|H)=.1`. Calculate all four joint cells, both posteriors for word presence, and the spam posterior for word absence. State the two class decisions at threshold `.5`.

<details>
<summary>Check the fresh Bayes problem</summary>

Joint cells in the same order: **.10, .08, .10, .72**. Word-presence probability **.18**. `P(S|W)=5/9≈.555556`, `P(H|W)=4/9≈.444444`; `P(S|not W)=.10/.82=5/41≈.121951`. Predict spam when present, ham when absent. The prior matters even with a relatively strong word likelihood.

</details>

<a id="n1-2"></a>
### N1.2 Fidelity, missing modes and a sampling table

**Source connection:** Introduction pages 3–4, 37–41. This discrete model is an arithmetic counterpart of the A/B/C map, not a probability table printed in the slides.

| Region | `p_data` | `p_model` | Interpretation |
| --- | ---: | ---: | --- |
| A | 0 | .2 | Model produces an invalid region |
| B | .4 | 0 | Real region omitted entirely by model |
| C | .6 | .8 | Region both distributions support, with wrong frequency |

Both columns sum to one. For **100 independent generated samples**, expected counts are **20, 0, 80**. Expected counts under the data are **0, 40, 60**. “Expected” is not a promise about a particular finite batch.

To sample the model using a uniform draw `u` from `[0,1)`, output A for `0≤u<.2`, C for `.2≤u<1`; B has an empty interval. Draws `.05,.25,.85` therefore produce **A,C,C**. Even a million samples cannot produce B under this model. Resampling cannot repair a zero-probability gap.

**Try it:** Now let `p_data=(.1,.3,.6)` and `p_model=(.25,.25,.5)` for A/B/C. State the sampling intervals and outputs for `u=.10,.30,.75`. Give expected counts in 40 generated samples. Is any region impossible? What is the probability that **four independent** generated samples contain no B?

<details>
<summary>Check the changed distribution</summary>

Intervals **A `[0,.25)`, B `[.25,.5)`, C `[.5,1)`**; outputs **A,B,C**. Expected counts **10,10,20**. All regions remain possible, although their frequencies are wrong. Probability of no B in four draws is **`(.75)^4=.31640625`**. Thus a small grid that happens to omit a region does not prove that the model assigns it zero probability. The original model, by contrast, omits B with probability one for every sample count.

</details>

<a id="n1-3"></a>
### N1.3 Explain the distinction without relying on model names

**Try:** Answer each in one or two sentences.

1. Why can a model of `p(x,y)` classify, but a classifier of `p(y|x)` alone cannot sample a new input `x`?
2. A model takes a text prompt and generates an image. Does its conditioning make it a discriminative classifier?
3. Does a GAN generator usually give an explicit, easy-to-evaluate probability density for an image?
4. Why can a convincing sample grid fail to establish coverage, privacy, or fairness?
5. Why does the statement “a CNN is discriminative” need a task/objective attached?

<details>
<summary>Answer cues</summary>

1. Normalize the joint across possible labels to obtain the posterior. The classifier has no distribution over possible inputs unless additional modeling is supplied.
2. It is conditional generation: the output is a newly sampled image, conditioned on text.
3. A standard GAN defines its distribution implicitly through transforming noise; density evaluation is a separate capability.
4. The grid may omit real modes, repeat training examples, or reflect an unrepresentative selection. Each claim needs its own evaluation.
5. Convolutional layers can appear in a classifier, encoder, generator or discriminator. Architecture alone does not determine the modeling objective.

</details>

<a id="n2"></a>

## Lecture 2 — Autoencoders and VAEs: worked calculations

The numbers below are fixed practice examples, not claims about actual quiz questions. Use natural logarithms throughout. Distinguish sums over coordinates from means over pixels or examples. Standard deviations, variances, and log-variances are different quantities.

<a id="n2-1"></a>
### N2.1 A complete tiny autoencoder: forward pass, reconstruction loss, and update

**Source connection:** Lecture 2 pp. 5–12. **Video:** [Serrano's reconstruction-loss example, 25:46–27:11](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1546s), **1:25 replay**, uses pixel numbers. The following original exercise supplies the full parameter update.

Use a **linear** two-input, one-code, two-output AE with independent encoder/decoder parameters; no nonlinear activations or tied weights in this toy example:

`x = (1,0)`; `z = a x₁ + b x₂ + c`; `x̂₁ = d z + f`; `x̂₂ = e z + g`.

Initial `(a,b,c,d,e,f,g) = (0.5,0.25,0.1,0.8,−0.5,0.1,0.6)`. The target is the original `x`. Loss is **SSE**, `L = (x̂₁−x₁)² + (x̂₂−x₂)²`, and learning rate is `0.1`.

1. **Encode:** `z = 0.5(1)+0.25(0)+0.1 = 0.6`.
2. **Decode:** `x̂ = (0.8(0.6)+0.1, −0.5(0.6)+0.6) = (0.58,0.30)`.
3. **Score:** residuals are `(−0.42,0.30)`; `L = 0.1764+0.09 = 0.2664`. Pixel MSE would be `0.1332`.
4. **Backpropagate:** output derivatives are `2(x̂−x) = (−0.84,0.60)`. Both output paths contribute to the code derivative: `∂L/∂z = (−0.84)(0.8)+(0.60)(−0.5) = −0.972`.

| Parameter | Gradient from the original forward pass | Updated value `w − 0.1 gradient` |
|---|---:|---:|
| `a` | `−0.972 × x₁ = −0.972` | 0.5972 |
| `b` | `−0.972 × x₂ = 0` | 0.25 |
| `c` | −0.972 | 0.1972 |
| `d` | `−0.84 × z = −0.504` | 0.8504 |
| `e` | `0.60 × z = 0.36` | −0.536 |
| `f` | −0.84 | 0.184 |
| `g` | 0.60 | 0.54 |

Update **all seven simultaneously**. The new code is `0.7944`, the reconstruction is `(0.85955776,0.1142016)`, and SSE is approximately **0.032766**. All seven analytic gradients agree with an independent central finite-difference check to within `5 × 10⁻¹¹`.

**Fresh problem:** reset all initial parameters; use `x = (0,1)`. Calculate `z`, reconstruction, SSE, both output derivatives, and `∂L/∂z`. Find all seven parameter gradients, update all parameters simultaneously with learning rate `0.1`, and recompute the reconstruction and SSE.

<details>
<summary>Show checked answer</summary>

`z = 0.35`, `x̂ = (0.38,0.425)`, residuals `(0.38,−0.575)`. SSE `= 0.1444+0.330625 = 0.475025`.

Output derivatives are `(0.76,−1.15)`. Code derivative `= 0.76(0.8)+(−1.15)(−0.5)=1.183`. Encoder gradients are `(0,1.183,1.183)`. The zero input makes `∂L/∂a = 0`; it does not make every encoder gradient zero.

| Parameter | Gradient from the reset forward pass | Updated value |
|---|---:|---:|
| `a` | `1.183 × 0 = 0` | 0.5 |
| `b` | `1.183 × 1 = 1.183` | 0.1317 |
| `c` | 1.183 | −0.0183 |
| `d` | `0.76 × 0.35 = 0.266` | 0.7734 |
| `e` | `−1.15 × 0.35 = −0.4025` | −0.45975 |
| `f` | 0.76 | 0.024 |
| `g` | −1.15 | 0.715 |

After this simultaneous update, `z'=0.1317−0.0183=0.1134` and `x̂'=(0.11170356,0.66286435)`. New SSE is `0.11170356²+(0.66286435−1)² ≈ 0.126138`, down from `0.475025`. Independent finite differences check all seven fresh gradients to within `7 × 10⁻¹¹`.

</details>

<a id="n2-2"></a>
### N2.2 Compression, latent retrieval, and metric choice

**Source connection:** pp. 9–14. **Video calculation:** [StatQuest cosine similarity, 6:19–10:13](https://www.youtube.com/watch?v=e9U0QAFbfLI&t=379s), **3:54**. Its word-count calculation transfers directly to nonzero image-code vectors.

**Compression calculation:** a `28 × 28` grayscale image has `784` scalar entries. A two-coordinate latent code stores `2/784 = 1/392` as many scalars, a **392:1 coordinate-count reduction**, or about **99.7449% fewer scalar entries**. This ignores decoder weights, numerical precision, metadata, and actual file compression.

**Retrieval calculation:** the query code is `q=(1,0)`; database codes are `A=(2,0)`, `B=(1,1)`, `C=(−1,0)`.

| Stored image | Euclidean distance `‖q−z‖` | Cosine similarity `(q·z)/(‖q‖‖z‖)` |
|---|---:|---:|
| A | 1 | 1 |
| B | 1 | `1/√2 ≈ 0.707107` |
| C | 2 | −1 |

Euclidean distance ties A and B; cosine prefers A. Cosine treats `(1,0)` and `(2,0)` as the same direction despite different magnitudes. Neither metric alone proves semantic similarity.

**Fresh problem:** query `q=(0,2)`, codes `D=(0,1)` and `E=(2,2)`. Compute distances and cosines. Also find the coordinate-count reduction for a `32 × 32 × 3` image encoded into 12 numbers.

<details>
<summary>Show checked answer</summary>

`distance(q,D)=1`, `cos(q,D)=1`; `distance(q,E)=2`, `cos(q,E)=1/√2≈0.707107`. Both metrics prefer D here. The image has `3072` entries; `3072/12 = 256`, giving a **256:1 coordinate-count reduction**. A zero code would make its cosine similarity undefined.

</details>

<a id="n2-3"></a>
### N2.3 Denoising targets, anomaly thresholds, and color output shapes

**Source connection:** pp. 15–19. [Serrano's denoising explanation, 10:50–18:15](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=650s), **7:25**, supplies the task intuition. Work the numbers separately.

**Denoising:** clean target `x=(1,0)`, noisy input `x̃=(0.8,0.2)`, decoder output `x̂=(0.9,0.1)`.

- Correct clean-target SSE: `(0.9−1)²+(0.1−0)² = 0.02`.
- If the model instead copies the noisy input exactly, its clean-target SSE is `(0.8−1)²+(0.2−0)² = 0.08`.
- That same copy has zero error against the **noisy input**. This is the wrong training target for the denoising task.

**Anomaly detection:** use pixel **MSE** and flag only if `error > 0.05`.

| Input | Reconstruction | MSE | Decision |
|---|---|---:|---|
| `(1,0)` | `(0.9,0.1)` | 0.01 | Do not flag |
| `(0,1)` | `(0.4,0.6)` | 0.16 | Flag |
| `(1,0)` | `(0.9,0.3)` | 0.05 | Do not flag: equality is excluded |

The threshold is given for this calculation; in a real experiment it must be chosen without tuning on the final test set. Switching from MSE to SSE without rescaling the threshold changes the detector.

**Fresh problem:** target `(0,1)`, noisy input `(0.2,0.7)`, reconstruction `(0.1,0.8)`. Find clean-target SSE and MSE, then apply `MSE > 0.02`. For a separate colorization model taking `64 × 64 × 1` grayscale inputs and predicting RGB, give its number of input and output scalars.

<details>
<summary>Show checked answer</summary>

SSE `= 0.1²+(−0.2)² = 0.05`; MSE `= 0.025`; the threshold rule flags it. This arithmetic by itself does not determine whether the image is a true anomaly. The grayscale input has `4096` scalars; the RGB target/output has `12288`. Colorization training needs the color target, not a duplicated grayscale target.

</details>

<a id="n2-4"></a>
### N2.4 The lecture's discrete KL example in both directions

**Source connection:** pp. 36–37. **Numerical video replay:** [Serrano: KL probability-bar example, 29:40–30:30](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1780s), **0:50**, after its longer loss explanation. Its values differ from this exercise; its creator corrects the middle red probability at 30:05 to **0.4**.

Use the lecture's distributions `P=(0.36,0.48,0.16)` and `Q=(1/3,1/3,1/3)`. Keep `1/3` exact until the final calculation; do not replace it by `0.333` prematurely.

| Outcome | `Pᵢ ln(Pᵢ/Qᵢ)` | `Qᵢ ln(Qᵢ/Pᵢ)` |
|---|---:|---:|
| 0 | 0.027706 | −0.025654 |
| 1 | 0.175029 | −0.121548 |
| 2 | −0.117435 | 0.244656 |
| **Sum** | **0.085300 nats** | **0.097455 nats** |

For example, the first forward term is `0.36 ln(0.36/(1/3))`; the first reverse term is `(1/3) ln((1/3)/0.36)`. Changing the order changes the weighting distribution as well as the ratio. Negative individual terms are valid; both totals are positive and unequal.

**Fresh problem:** `P=(0.75,0.25)`, `Q=(0.5,0.5)`. Calculate both directions and explain what would happen to `KL(P ‖ Q)` if `Q` became `(1,0)`.

<details>
<summary>Show checked answer</summary>

`KL(P ‖ Q) = 0.75 ln1.5 + 0.25 ln0.5 = 0.130812 nats`.

`KL(Q ‖ P) = 0.5 ln(2/3) + 0.5 ln2 = 0.143841 nats`.

With `Q=(1,0)`, the second outcome has positive P mass and zero Q mass, so `KL(P ‖ Q)=∞`. Replacing the zero with a small positive number is a numerical modification, not the exact same distribution.

</details>

<a id="n2-5"></a>
### N2.5 VAE sampling and a Gaussian KL derivation with numbers

**Source connection:** pp. 22–28, 38–45, 57–60. The [MIT prior chapter, 23:25–32:31](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1405s), **9:06**, explains the role of KL. The complete numerical Gaussian calculation is provided here.

Encoder outputs are `μ=(1,−1)`, `ℓ=(ln0.25,ln4)`, where **`ℓ = ln σ²`**. Let sampled noise be `ε=(2,−0.5)`.

| Quantity | Coordinate 1 | Coordinate 2 |
|---|---:|---:|
| Mean `μ` | 1 | −1 |
| Log-variance `ℓ` | −1.386294 | 1.386294 |
| Variance `exp ℓ` | 0.25 | 4 |
| Standard deviation `exp(ℓ/2)` | 0.5 | 2 |
| Sample `z = μ + σ ε` | `1+0.5(2)=2` | `−1+2(−0.5)=−2` |

There are four encoder-head outputs, but the decoder receives the two-dimensional sample `(2,−2)`. `ε` is standard-normal noise; these fixed values are specified to make the arithmetic reproducible.

**Derive one coordinate before substituting.** For `q=N(μ,v)`, `p=N(0,1)` with variance `v>0`:

`ln q(z) − ln p(z) = −½ ln v − (z−μ)²/(2v) + z²/2`.

Take the expectation under **q**:

1. `E[−½ ln v] = −½ ln v`.
2. `E[(z−μ)²/(2v)] = v/(2v) = ½`.
3. `E[z²/2] = (v+μ²)/2`.

Therefore `KL(q ‖ p) = ½(v+μ²−1−ln v)`. The independent-coordinate assumption lets us sum these terms.

| Coordinate | `−½ ln v` | `−½` | `(v+μ²)/2` | KL contribution |
|---|---:|---:|---:|---:|
| 1 | 0.693147 | −0.5 | 0.625 | 0.818147 |
| 2 | −0.693147 | −0.5 | 2.5 | 1.306853 |
| **Total** | | | | **2.125 nats** |

This is an **analytic expectation**, so its KL value does not depend on which `ε` happened to be sampled. The sampled reconstruction generally does depend on `ε`. The sign shown on p. 35 would incorrectly make this KL negative; pp. 38–45 give the corrected form.

**Fresh problem:** `μ=(0,2)`, `ℓ=(0,0)`, `ε=(−1,0.5)`. Find variances, standard deviations, `z`, and KL to `N(0,I)`. Separately, find KL when both means are zero and both log-variances are zero.

<details>
<summary>Show checked answer</summary>

Variances and standard deviations are both `(1,1)`. Sample `z=(−1,2.5)`. KL contributions are `(0,2)` and total KL is **2 nats**. With means `(0,0)` and log-variances `(0,0)`, the encoder distribution equals the prior, so KL is **zero**. Zero log-variance never means zero variance.

</details>

<a id="n2-6"></a>
### N2.6 Combine reconstruction and KL without mixing reductions

**Source connection:** pp. 29–35, 45, 52–53 and Assignment 1 Part A1. Start with squared-error reconstruction, as used in the course and assignment. The Bernoulli example below is an optional likelihood bridge.

#### Main course practice: pixel-MSE plus summed latent KL, then batch mean

For this exercise, use exactly these reductions for each example `i` with `D=2` pixels and `k=2` latent coordinates:

`Rᵢ = (1/D) Σₚ (x̂ᵢₚ − xᵢₚ)²`.

`Kᵢ = ½ Σⱼ (vᵢⱼ + μᵢⱼ² − 1 − ln vᵢⱼ)`, where `v` is **variance**.

`L = (1/B) Σᵢ (Rᵢ + Kᵢ)` for batch size `B=2`; the KL coefficient is one. These are explicit exercise conventions, not a claim that every implementation uses this scaling. Keep your assignment/starter's specified reductions consistent and report them.

| Example | Target `x` | Reconstruction `x̂` | Encoder mean `μ` | Variance `v` |
|---|---|---|---|---|
| A | `(1,0)` | `(0.8,0.25)` | `(1,−1)` | `(0.25,4)` |
| B | `(0,1)` | `(0.3,0.6)` | `(0,1)` | `(1,1)` |

For A, SSE is `(−0.2)²+0.25²=0.1025`, so pixel-MSE is `0.05125`. Its KL is `2.125`, from N2.5. For B, SSE is `0.3²+(−0.4)²=0.25`, giving pixel-MSE `0.125`; its two KL contributions are `0` and `½(1+1−1−ln1)=0.5`.

| Example | Pixel-MSE `Rᵢ` | Summed latent KL `Kᵢ` | `Rᵢ + Kᵢ` |
|---|---:|---:|---:|
| A | 0.05125 | 2.125 | 2.17625 |
| B | 0.125 | 0.5 | 0.625 |
| **Batch mean** | **0.088125** | **1.3125** | **1.400625** |

Thus the final objective is `(2.17625+0.625)/2 = 1.400625`. If you instead use **pixel-SSE**, the batch objective becomes `0.17625+1.3125=1.48875`: only reconstruction doubled. If you average KL across its two coordinates, the original pixel-MSE objective becomes `0.088125+0.65625=0.744375`: only KL halved. Neither change is a harmless global rescaling of the original objective; each changes the reconstruction–regularization balance.

**Fresh MSE problem:** keep the same reductions and coefficient. Example C has target `(1,0)`, reconstruction `(0.7,0.2)`, mean `(0.5,0)`, variance `(1,1)`. Example D has target `(0,1)`, reconstruction `(0.1,0.8)`, mean `(0,0)`, variance `(1,1)`. Calculate each pixel-MSE, each summed KL, each total, and the batch-mean objective.

<details>
<summary>Show checked MSE answer</summary>

For C, SSE is `0.09+0.04=0.13`; pixel-MSE is `0.065`. KL is `½(0.5²)=0.125`, so the total is `0.19`. For D, SSE is `0.01+0.04=0.05`; pixel-MSE is `0.025`. Both Gaussian coordinates equal the prior, so KL is `0` and the total is `0.025`. Batch mean is `(0.19+0.025)/2 = 0.1075`.

</details>

#### Optional likelihood bridge: Bernoulli reconstruction and ELBO

This separate exercise uses summed binary cross-entropy instead of squared error. Do not substitute it for the assignment's MSE objective or switch loss definitions midway through an answer.

Let the binary target be `x=(1,0)` and the decoder probabilities at one sampled code be `(0.8,0.25)`. Use **summed** binary cross-entropy across the two coordinates:

`R = −[ln0.8 + ln(1−0.25)] = −ln0.8−ln0.75 = 0.510826`.

Use the Gaussian KL from N2.5, `K=2.125`. With coefficient one, `L=R+K=2.635826`.

If an exercise explicitly specifies `Lβ=R+βK`, then `β=0.1` gives `0.723326`, while `β=2` gives `4.760826`. These are alternative objectives, not the same loss. A different reconstruction reduction also changes the balance: pixel-mean BCE here is `R/2 = 0.255413`, so `R/2+K = 2.380413` is **not** half of `R+K`.

**Batch reduction:** if two examples have summed reconstructions `(0.510826,0.4)` and per-example KLs `(2.125,0.5)`, their individual losses are `(2.635826,0.9)`. Batch-mean loss is `(2.635826+0.9)/2 = 1.767913`. Sum over each example's latent dimensions, then average examples when that is the required convention.

**ELBO bridge, optional theory:** define `ELBO = E_q[ln pθ(x|z)] − KL(q‖p)`. Exact negative ELBO uses the **expected** reconstruction negative log-likelihood. Our one-sample `R+K` is a Monte Carlo estimate of it, not an exact evaluation of that expectation. Calling its negative a sampled ELBO estimate does not guarantee that every single draw lies below `ln pθ(x)`.

**Fresh problem:** target `(1,0)`, decoder probabilities `(0.6,0.1)`, KL `0.4`. Compute summed BCE, loss at `β=1`, and loss at `β=0.5`.

<details>
<summary>Show checked answer</summary>

`R=−ln0.6−ln0.9=0.616186`. At `β=1`, `L=1.016186`; at `β=0.5`, `L=0.816186`. The KL remains nonnegative in both cases. Scaling its weight is different from changing its sign.

</details>

<a id="n2-7"></a>
### N2.7 Reparameterization gradients, including the KL path

**Source connection:** pp. 55–60. **Video derivation:** [MIT reparameterization, 32:31–34:36](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1951s), **2:05**. This exercise adds actual values, both gradient paths, and an update.

Use one latent dimension: `μ=0.5`, `ℓ=ln4`, `σ=exp(ℓ/2)=2`, fixed sampled `ε=0.25`. Let the toy decoder be the identity `x̂=z`, with target `x=0`. Reconstruction is explicitly **half squared error** `R=½(z−x)²`.

1. `z=μ+σε=0.5+2(0.25)=1` and `R=0.5`.
2. The upstream reconstruction derivative is `∂R/∂z = z−x = 1`.
3. Local derivatives: `∂z/∂μ=1`; `∂z/∂σ=ε=0.25`; `∂z/∂ℓ=½σε=0.25`.
4. Reconstruction-path gradients are therefore `∂R/∂μ=1`, `∂R/∂σ=0.25`, `∂R/∂ℓ=0.25`.
5. `K=½(expℓ+μ²−1−ℓ)=0.931853`. KL gradients for the **learned coordinates `(μ,ℓ)`** are `∂K/∂μ=μ=0.5`, `∂K/∂ℓ=½(expℓ−1)=1.5`.
6. Total `L=R+K=1.431853`; gradients are **`∂L/∂μ=1.5`**, **`∂L/∂ℓ=1.75`**. Add the reconstruction and KL contributions before updating.
7. With learning rate `0.1`, update simultaneously: `μ'=0.35`, `ℓ'=ln4−0.175=1.211294`; thus `σ'=exp(ℓ'/2)≈1.832438`. Holding the same ε only for the comparison, the new loss is approximately **0.961037**.

The two total gradients agree with central finite differences to within `10⁻¹⁰`. In training, new iterations typically use newly sampled noise, so an individual noisy loss need not decrease on every step. This example updates encoder outputs as standalone scalar parameters to isolate the trick; a real network backpropagates these derivatives through its encoder weights.

**Fresh problem:** `μ=1`, `ℓ=0`, `ε=−1`, target `x=1`, the same identity decoder and half-squared reconstruction, and KL coefficient one. Compute `z`, `R`, `K`, and the total gradients with respect to `(μ,ℓ)`.

<details>
<summary>Show checked answer</summary>

`σ=1`, `z=0`, `R=½(0−1)²=0.5`, `K=½(1+1−1−0)=0.5`; total loss is `1`.

The upstream derivative is `−1`. Reconstruction gradients are `∂R/∂μ=−1` and `∂R/∂ℓ=(−1)(½·1·−1)=0.5`. KL gradients are `(1,0)`. Adding paths gives **total gradients `(0,0.5)`**. The zero total mean gradient is cancellation, not absence of a differentiable path.

</details>

<a id="n2-8"></a>
### N2.8 Interpolation versus changing one coordinate

**Source connection:** pp. 54, 61–64. **Visualization:** [MIT latent perturbation, 34:36–37:40](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=2076s), **3:04**; pair the video with the two-endpoint interpolation diagrams in your slides.

Let endpoint codes be `zA=(−2,1)` and `zB=(2,3)`. Calculate `z(α)=(1−α)zA+αzB`.

| α | Latent code |
|---:|---|
| 0 | `(−2,1)` |
| 0.25 | `(−1,1.5)` |
| 0.5 | `(0,2)` |
| 0.75 | `(1,2.5)` |
| 1 | `(2,3)` |

To see why averaging codes differs from averaging outputs, use toy nonlinear decoder `d(z)=(z₁²,z₂)`. It produces endpoint outputs `(4,1)` and `(4,3)`, but decoding the midpoint gives **`(0,2)`**. The average of endpoint outputs is **`(4,2)`**. These are different.

A **coordinate traversal** from `z=(0,2)` might instead use `z=(−1,2),(0,2),(1,2)`: only the first coordinate changes. This is not the interpolation above, in which both coordinates change. A visible output change does not by itself identify a unique semantic factor.

**Fresh problem:** endpoints `zA=(1,−1)` and `zB=(3,3)`, with `α=0.25`. Find the interpolated code, its output under the same toy decoder, and the corresponding pixel-space weighted average of endpoint outputs.

<details>
<summary>Show checked answer</summary>

Interpolated code: `(1.5,0)`. Decoded output: `(2.25,0)`. Endpoint outputs are `(1,−1)` and `(9,3)`, whose weighted average is `0.75(1,−1)+0.25(9,3)=(3,0)`. The nonlinear decoding step causes the difference.

</details>

<a id="n3"></a>

## GANs Part 1 — Losses, gradients, and alternating updates

All calculations below use natural logs and rounded display values. Retain extra precision until the final update. These are practice problems based on the provided slides, not a prediction of quiz questions.

<a id="n3-1"></a>

### N3.1 Real/fake BCE and the two generator losses

**From:** GANs Part 1 pp. 30–41. **Video with actual arithmetic:** [Luis Serrano, log-loss examples](https://www.youtube.com/watch?v=8L11aMN5KY8&t=580s), **9:40–11:30 · 1:50**, full video **21:00**. The probabilities `0.1` and `0.9` are substituted into logarithmic penalties in the video. The following batch example extends that arithmetic using the course's convention.

**Problem.** The discriminator assigns real probabilities `(0.8,0.6)` to two real images and `(0.25,0.10)` to two generated images. Compute `L_D`, the minimax generator loss, and the non-saturating generator loss. Use the **sum of the real-batch mean and fake-batch mean** for `L_D`.

**Worked solution.** A real example has target 1, so it contributes `-ln(r)`. A generated example has target 0 **while training D**, so it contributes `-ln(1-q)`.

| Item | Individual penalties | Mean |
|---|---|---:|
| Real examples | `-ln .8 = .223144`; `-ln .6 = .510826` | `.366985` |
| Fake examples, D step | `-ln .75 = .287682`; `-ln .9 = .105361` | `.196521` |

Thus `L_D = .366984588 + .196521294 = .563505882`.

For the generator, average over the **generated examples only**:

`L_G,minimax = (ln .75 + ln .9)/2 = -.196521294`.

`L_G,NS = (-ln .25 - ln .10)/2 = (1.386294361+2.302585093)/2 = 1.844439727`.

The negative minimax value is expected; losses need not share a sign or scale. A BCE mean over all four discriminator examples would be `.281752941`, half the slide's convention. This constant also halves gradients, so it matters when a numerical problem fixes the learning rate.

**Equilibrium scale check.** If all real and fake probabilities are `.5`, `L_D=2 ln2=1.386294`, `L_G,minimax=-ln2=-.693147`, and `L_G,NS=ln2=.693147`. These values alone cannot prove that the discriminator is optimal or that the distributions match.

**Fresh retry.** One real example has `D(x)=.9` and one fake has `D(G(z))=.4`. Compute all three losses with the same convention. What would a concatenated mean BCE report for `D`?

<details>
<summary>Checked answer</summary>

`L_D=-ln .9-ln .6=.105360516+.510825624=.616186139`.

`L_G,minimax=ln .6=-.510825624`; `L_G,NS=-ln .4=.916290732`.

Concatenated two-example mean BCE: `.308093070`.

</details>

<a id="n3-2"></a>

### N3.2 Derive the gradient before substituting probabilities

**From:** pp. 31–40, 47. **Purpose:** distinguish derivatives with respect to a probability, a logit, and a generator parameter.

Let `q=σ(a)`, where `a` is the discriminator logit on a generated example. The sigmoid derivative is `dq/da=q(1-q)`.

For the saturating/minimax loss:

`dL_MM/dq=-1/(1-q)`.

Multiply by the sigmoid derivative: `dL_MM/da=[-1/(1-q)]q(1-q)=-q`.

For the non-saturating loss:

`dL_NS/dq=-1/q`.

Therefore `dL_NS/da=(-1/q)q(1-q)=q-1`.

| Fake real-probability `q` | `L_MM=ln(1-q)` | `L_NS=-ln q` | `dL_MM/da` | `dL_NS/da` |
|---:|---:|---:|---:|---:|
| `.01` | `-.010050` | `4.605170` | `-.01` | `-.99` |
| `.50` | `-.693147` | `.693147` | `-.50` | `-.50` |
| `.99` | `-4.605170` | `.010050` | `-.99` | `-.01` |

**Continue the chain.** Suppose at the current parameters `q=.01` and `da/dθ=2`, with a scalar generator parameter `θ=0` and learning rate `.1`. The gradients are `dL_MM/dθ=-.02` and `dL_NS/dθ=-1.98`. A descent step gives `θ_MM=.002` and `θ_NS=.198`. Each calculation starts from the same initial state; these are alternative steps, not successive updates.

This example isolates the output-loss effect. If `da/dθ=0`, both total parameter gradients are zero; switching the loss does not repair a disconnected graph or every upstream saturation problem.

**Fresh retry.** At `q=.2`, suppose `da/dθ=-3`, `θ=1`, and the learning rate is `.1`. Compute both parameter gradients and new parameters. Explain why the parameter moves downward even though G wants the discriminator logit to rise.

<details>
<summary>Checked answer</summary>

`dL_MM/da=-.2`, so `dL_MM/dθ=(-.2)(-3)=.6`; `θ_new=1-.1(.6)=.94`.

`dL_NS/da=-.8`, so `dL_NS/dθ=(-.8)(-3)=2.4`; `θ_new=1-.1(2.4)=.76`.

The local derivative `da/dθ` is negative: decreasing this parameter locally increases the logit. “Make D's output larger” does not mean “increase every generator weight.”

</details>

<a id="n3-3"></a>

### N3.3 One complete discriminator step, then one generator step

**From:** pp. 28–30, 41–44. **Video support:** [Serrano's tiny GAN and backward paths](https://www.youtube.com/watch?v=8L11aMN5KY8&t=800s), **13:20–18:10 · 4:50**. The worked example below supplies every scalar update and checks the new loss; it uses a simpler scalar generator so every derivative fits on paper.

**Setup.** `G_θ(z)=θz` and `D_w,b(x)=σ(wx+b)`. Use one real scalar example `x_real=2`, one noise value `z=2`, and initial parameters `θ=.5`, `w=1`, `b=-1`. Use learning rates `α_D=α_G=.1`, the sum-of-two-means `L_D`, and the non-saturating `L_G=-ln D(G(z))`. Each mean contains one example. Treat this as two sequential gradient-descent steps, not Adam. Bias `b` belongs to `D`; `θ` belongs to `G`.

#### Phase A: update D while G is fixed

1. Generate a fixed fake: `x_fake=θz=.5×2=1`.
2. Real logit: `a_real=1×2-1=1`; `r=σ(1)=.731058579`.
3. Fake logit: `a_fake=1×1-1=0`; `q=σ(0)=.5`.
4. Discriminator loss: `L_D=-ln r-ln(1-q)=.313261688+.693147181=1.006408868`.

For sigmoid+BCE, the logit derivative is `prediction-target`. The real target is 1 and the fake target is 0:

`δ_real=r-1=-.268941421`, `δ_fake=q-0=.5`.

Because `a=wx+b`, `da/dw=x` and `da/db=1`. Add the real and fake contributions:

`dL_D/dw=(-.268941421)(2)+(.5)(1)=-.037882843`.

`dL_D/db=-.268941421+.5=.231058579`.

Update both discriminator parameters using the same pre-update gradients:

`w_new=1-.1(-.037882843)=1.003788284`.

`b_new=-1-.1(.231058579)=-1.023105858`.

`θ` remains **`.5`**. No gradient update to G occurs in this phase.

#### Phase B: update G through the newly updated, frozen D

Use the same stated `z=2` for this hand calculation. In stochastic training, a fresh noise batch may be sampled, as on p. 43.

1. The fake remains `x_fake=1` before the G step.
2. Recompute the discriminator logit with **new** `w,b`: `a=1.003788284×1-1.023105858=-.019317574`.
3. Thus `q_G=.495170757`, and `L_G=-ln q_G=.702852613`.
4. Backpropagate through frozen D and into G:

`dL_G/dθ = (q_G-1) × (da/dx_fake) × (dx_fake/dθ)`.

`= (-.504829243) × 1.003788284 × 2 = -1.013483360`.

The middle factor is **D's current weight**, even though that weight is not being updated. It is the derivative of D's logit with respect to its input.

`θ_new=.5-.1(-1.013483360)=.601348336`.

The discriminator parameters stay `w=1.003788284`, `b=-1.023105858` throughout Phase B.

#### Recompute to verify the change

`x_fake,new=.601348336×2=1.202696672`.

`D(x_fake,new)=.545907090`; `L_G,new=-ln(.545907090)=.605306483`.

For this small step with D fixed, G's loss falls from `.702852613` to `.605306483`, and D's real-probability on the fake rises. This local check is not proof that a full GAN will converge.

**Common mistakes to diagnose:** using the old `.5` discriminator output in Phase B; updating D again during Phase B; detaching D's input during Phase B; treating the fake as target 1 during the D step; averaging the two D contributions without adjusting the declared convention; or changing `w` before computing the old-state bias gradient.

**Fresh retry.** Reset all initial parameters and learning rates above, change only the real example to `x_real=3`, and perform both phases. Report `L_D`, both D gradients and updates, the recomputed `q_G`, the G gradient/update, and the final G loss.

<details>
<summary>Checked complete answer</summary>

Initial fake remains `1`; real logit is `2`, so `r=.880797078`; `q=.5`.

`L_D=.126928011+.693147181=.820075192`.

`dL_D/dw=(.880797078-1)×3+.5×1=.142391234`.

`dL_D/db=.880797078-1+.5=.380797078`.

`w_new=.985760877`; `b_new=-1.038079708`; `θ` remains `.5`.

Recompute `q_G=σ(.985760877-1.038079708)=.486923275`; `L_G=.719648715`.

`dL_G/dθ=(.486923275-1)×.985760877×2=-1.011541925`.

`θ_new=.601154192`; fake becomes `1.202308385`; with D still fixed, `q_final=.536711033` and `L_G,final=.622295442`.

</details>

<a id="n3-4"></a>

### N3.4 Minibatch similarity: a numerical view of collapse

**From:** pp. 51–53. The slide's pairwise form is `o_i=Σ_j exp(-||M_i-M_j||_1)`. In the original construction there can be multiple learned feature projections; here use one scalar feature `M_i` per example to make the arithmetic visible. **Include the self term `j=i`**, which contributes `exp(0)=1`.

**Problem.** Compare a diverse batch with features `(0,1,2)` and a collapsed batch `(1,1,1)`.

**Worked solution.** For `(0,1,2)`, the pairwise L1 distances are

```text
       M0 M1 M2
M0      0  1  2
M1      1  0  1
M2      2  1  0
```

Apply `exp(-distance)` to each entry and sum each row:

- `o_0=1+e^-1+e^-2=1.503214724`.
- `o_1=e^-1+1+e^-1=1.735758882`.
- `o_2=e^-2+e^-1+1=1.503214724`.

For `(1,1,1)`, all distances are zero, all similarities are 1, and every `o_i=3`. The collapsed batch has **higher similarity**, not higher diversity. Concatenating this information to each image's ordinary features lets D learn to recognize repetition. These statistics are features; we have not defined an extra generator loss.

A variant excluding self terms would subtract 1 from every score for these batches. A mean instead of a sum would scale the scores by batch size. State the convention so numbers are comparable.

**Fresh retry.** Use `(0,0,2)` with the same included-self convention. Calculate all three scores, and identify which examples have a duplicate.

<details>
<summary>Checked answer</summary>

Distance rows are `(0,0,2)`, `(0,0,2)`, `(2,2,0)`.

`o_0=o_1=2+e^-2=2.135335283`; `o_2=1+2e^-2=1.270670566`.

The first two feature values are duplicates. The third is distinct in this simplified feature space. This statistic alone cannot establish whether an image is realistic or whether all modes are represented.

</details>

<a id="n3-5"></a>

### N3.5 Read the DCGAN shapes and count a layer's parameters

**From:** p. 45. This calculation extends its architecture diagram; it makes stride, padding, and bias assumptions explicit rather than inferring missing settings.

**Worked example A: projection.** A 100-component latent vector is projected to `4×4×1024=16,384` values, then reshaped. If this is a dense layer with one bias per output, it has

`100×16,384 + 16,384 = 1,654,784` trainable parameters.

Reshaping itself has no trainable parameters. For 16 generated RGB images of size `64×64`, the output batch has `16×64×64×3=196,608` scalar pixel values. Batch size changes activation count, not the number of learned layer parameters.

**Worked example B: first discriminator convolution.** The diagram has `5×5` filters and 3 input channels, with 64 output channels. Assuming one bias per output channel, parameter count is

`5×5×3×64 + 64 = 4,864`.

With the additional assumptions stride `s=2` and padding `p=2`, spatial size is `floor((64+2p-5)/s)+1=32`. This recovers the diagram's first output width.

**Worked example C: one transposed-convolution size.** For dilation 1, use

`H_out=(H_in-1)s-2p+k+output_padding`.

With `H_in=4`, `s=2`, `p=2`, `k=5`, and `output_padding=1`, obtain `H_out=3×2-4+5+1=8`. Those settings are one explicit example compatible with the displayed doubling, not settings specified by p. 45.

**Fresh retry.** A conventional `5×5` convolution takes 64 channels to 128 channels, with biases. Count its parameters. For `H_in=32`, stride 2 and padding 2, find its output width. Then find the transposed-convolution output from `H_in=8` under example C's settings.

<details>
<summary>Checked answer</summary>

`5×5×64×128+128=204,928` parameters.

Convolution width `floor((32+4-5)/2)+1=16`.

Transposed-convolution width `(8-1)×2-4+5+1=16`.

</details>

<a id="n3-6"></a>

### N3.6 Interpolation and attribute-vector arithmetic

**From:** pp. 59–65. The small vectors here are invented arithmetic examples; they do not claim to be measured latent codes for faces.

**Worked interpolation.** Let `z_A=(0,2)`, `z_B=(4,2)`. At `t=.25`,

`z(t)=(1-.25)(0,2)+.25(4,2)=(0,1.5)+(1,.5)=(1,2)`.

At `t=.5`, the midpoint is `(2,2)`. To form images, feed these latent vectors to the trained generator. Do not average output pixels and assume you obtained the same image.

**Worked attribute arithmetic.** Suppose average codes for “smiling woman,” “neutral woman,” and “neutral man” are respectively `(2,3)`, `(1,1)`, `(0,0)`. The smile direction is `(2,3)-(1,1)=(1,2)`. Adding it to the neutral-man code gives `(1,2)`. The arithmetic is exact; whether the resulting image has the intended semantic edit depends on the trained representation.

**Fresh retry.** Interpolate from `A=(2,-1)` to `B=(-2,3)` at `t=.75`. Separately compute “glasses man − man + woman” from codes `(3,1)`, `(1,2)`, and `(-1,4)`.

<details>
<summary>Checked answer</summary>

Interpolation: `.25(2,-1)+.75(-2,3)=(.5,-.25)+(-1.5,2.25)=(-1,2)`.

Attribute arithmetic: `(3,1)-(1,2)+(-1,4)=(1,3)`.

Neither calculation proves that latent directions are perfectly disentangled or that the edited image will preserve every other attribute.

</details>

<a id="n4"></a>

## Assignment calculations

These small, hypothetical examples practise the assignment's arithmetic. They are not experimental results or the user's roll number. Use natural logs for KL/IS and base-10 logs for PSNR. The videos in the support guide explain the concepts; the worked numerical bridge for these particular conventions is here.

<a id="n4-1"></a>

### N4.1 Roll mapping, interpolation and tensor shapes

**Worked example.** For a fictional roll ending in `1234`, the seed is 1234 and `R=34`. The held-out digit is `34 mod 10=4`. Compute `(34+3k) mod 10` for `k=0,…,5`: `4,7,0,3,6,9`; after sorting, the six digits are `[0,3,4,6,7,9]`. The attribute index is `34 mod 6=4` using zero-based indexing, so the second attribute is `Wearing_Hat`. The labels sent to the six-class classifier are `{0:0,3:1,4:2,6:3,7:4,9:5}`. These six residues are distinct because 3 and 10 are coprime; the starter's top-up loop is unnecessary for this formula.

For two toy VAE means `μ₁=(−2,1)`, `μ₂=(2,3)`, at `t=0.25`:

`z_t = 0.75(−2,1) + 0.25(2,3) = (−1,1.5)`.

At `t=0.5`, `z=(0,2)`; at 0 and 1 the means themselves are recovered. A real assignment strip uses 11 rows of 64 latent numbers, shape `(11,64)`, decoding to `(11,3,64,64)`. Interpolating means fixes the two latent endpoints; it does not guarantee linear changes in pixels or attributes.

The starter CelebA encoder spatial sizes are `64→32→16→8→4`. A Conv2d with kernel 4, stride 2, padding 1 and dilation 1 maps width `n` to `floor((n+2−4)/2)+1`. For a batch `B`, the final feature tensor is `(B,256,4,4)`, flattened to `(B,4096)`. The AE head returns `(B,64)`; the VAE head returns `(B,128)` split into two `(B,64)` arrays. `exp(0.5 logvar)` is standard deviation; `exp(logvar)` is variance.

For the MNIST G28, `(B,64)→(B,128,7,7)→(B,64,14,14)→(B,1,28,28)`. The transposed-convolution formula here is `(n−1)×2−2+4=2n`; it doubles each spatial dimension.

**Try without looking:** fictional suffix `1271`: find the seed, held-out digit, sorted six digits, second attribute and remapping of digit 7. Interpolate `(1,−1)` to `(5,3)` at `t=0.75`. What are classifier softmax and feature shapes for 500 generated images?

<details>
<summary>Checked answer</summary>

Seed 1271; `R=71`; held-out digit 1. Residues `1,4,7,0,3,6` sort to `[0,1,3,4,6,7]`; `71 mod 6=5`, so `Mouth_Slightly_Open`. Original digit 7 maps to class 5. Interpolation gives `(4,2)`. Shapes are `(500,6)` probabilities and `(500,128)` penultimate features.

</details>

<a id="n4-2"></a>

### N4.2 Denoising, clipping, MSE and PSNR

**Worked example.** A four-pixel clean image is `x=(0,0.5,1,0.5)`. With `ε=(−1,1,1,−1)`, adding `0.3 ε` gives `(−0.3,0.8,1.3,0.2)` and clipping gives `(0,0.8,1,0.2)`.

Noisy-image squared errors are `(0,0.09,0,0.09)`, so `MSE=0.18/4=0.045`. With data range 1:

`PSNR_noisy=10 log10(1/0.045)=13.467875 dB`.

Suppose a hypothetical denoised image is `(0.1,0.6,0.9,0.4)`. Its four squared errors are all 0.01, giving MSE 0.01 and PSNR 20 dB. Improvement is `6.532125 dB`. Noise clipping affects the actual errors, so do not simply replace noisy-image MSE by `0.3²`.

**Batch convention.** For two images with MSEs 0.01 and 0.04, their scores are 20 and 13.979400 dB. Mean per-image PSNR is `16.989700 dB`. PSNR from the average MSE would be `10 log10(1/0.025)=16.020600 dB`: a different quantity. The starter uses the first convention. When accumulating batches, weight by image count, particularly for a smaller last batch.

**Try without looking:** two normalized images have MSEs 0.0025 and 0.01. Calculate each PSNR, their mean, and PSNR from average MSE. What should happen if the same images and reconstruction errors are both multiplied by 255 and the peak is changed to 255?

<details>
<summary>Checked answer</summary>

Individual scores: 26.020600 and 20 dB; mean 23.010300 dB. Average MSE is 0.00625, giving 22.041200 dB if transformed after averaging. Consistently rescaling both the data and peak leaves each PSNR unchanged because numerator and MSE both scale by `255²`. Using peak 255 on unscaled `[0,1]` images would incorrectly add 48.130804 dB.

</details>

<a id="n4-3"></a>

### N4.3 The first strict gradient-threshold crossing

**Worked example.** Suppose the logged first-layer norm at iteration 100 is 0.8. The threshold is `0.01×0.8=0.008`. Later rows are:

| Iteration | Logged norm | Below 0.008? |
|---|---:|---|
| 101 | 0.0100 | No |
| 102 | 0.0080 | No: equality is not below |
| 103 | 0.0079 | Yes |
| 104 | 0.0060 | Yes, but not the first |

The event is iteration 103; quote reference 0.8, threshold 0.008 and event norm 0.0079. Report the named first-layer norm, not “all generator parameters,” unless you actually measured that.

To see the distinction, suppose two parameter tensors have flattened gradients `(0.3,0.4)` and `(1.2)`. The first-tensor norm is `sqrt(0.09+0.16)=0.5`. The full parameter norm is `sqrt(0.09+0.16+1.44)=1.3`. Norms of tensors are squared and summed before the final square root; adding tensor norms gives the wrong result 1.7.

**Try without looking:** reference norm 0.25 at iteration 100; rows 101–104 have `0.003,0.0025,0.0026,0.0024`. Find the event. What if every later norm stays at or above the threshold?

<details>
<summary>Checked answer</summary>

Threshold 0.0025; iteration 104 is the first strict crossing, with norm 0.0024. With no crossing, return/record no event within the observed run; do not use the last iteration as a substitute. If the reference norm is exactly zero, the strict test cannot detect a nonnegative norm below zero and needs to be reported as a degenerate reference.

</details>

<a id="n4-4"></a>

### N4.4 Mode coverage and reverse KL to six uniform classes

**Worked example.** A toy 5,000-image classifier histogram in sorted digit order is `(4500,250,200,50,0,0)`. Its proportions are `(0.9,0.05,0.04,0.01,0,0)`. At least 1% means at least 50 of the 5,000 samples, so **four modes** are covered, including the class with exactly 50 examples.

With uniform target `q_j=1/6` and the `0 log 0=0` limit:

`KL(p||q)=0.9 ln(5.4)+0.05 ln(0.3)+0.04 ln(0.24)+0.01 ln(0.06)=1.372342 nats`.

This is partial class collapse, heavily concentrated in one class. Total single-class collapse gives `ln 6=1.791759`; perfectly uniform proportions give zero. The assignment uses the uniform target even though the raw digit subset's empirical class counts need not be exactly equal. These statistics describe **predicted digit classes**, not within-class variety or image correctness.

**Try without looking:** counts `(2500,2500,0,0,0,0)`. Find proportions, coverage and reverse KL. A second histogram is `(4800,49,49,49,49,4)`; how many modes meet the threshold?

<details>
<summary>Checked answer</summary>

First: proportions `(0.5,0.5,0,0,0,0)`, two modes, `2×0.5 ln(0.5/(1/6))=ln 3=1.098612`. Second: only the first class reaches 50 samples, so one mode. Predicting six labels at least once is not the specified coverage test.

</details>

<a id="n4-5"></a>

### N4.5 Inception Score: confidence, class diversity and its blind spot

For a probability matrix `P` with one image per row, first average its rows to obtain `p(y)`. Then compute each row's KL to that marginal, average the KL values and exponentiate. These are softmax probabilities, not the hard class counts used in N4.4.

**Worked two-class examples** (small illustrations of the same six-class formula):

| Probability rows | Marginal | Mean KL | IS |
|---|---|---|---:|
| `(1,0)`, `(0,1)` | `(0.5,0.5)` | `ln 2` | 2 |
| `(1,0)`, `(1,0)` | `(1,0)` | 0 | 1 |
| `(0.5,0.5)`, `(0.5,0.5)` | `(0.5,0.5)` | 0 | 1 |
| `(0.9,0.1)`, `(0.1,0.9)` | `(0.5,0.5)` | `0.9 ln 1.8 + 0.1 ln 0.2 = 0.368064` | 1.444935 |

The first case is confident across both classes; the second confident but class-collapsed; the third uncertain for every image. A single score of 1 cannot tell the last two failure mechanisms apart. Use zero's limiting contribution when a row or marginal probability vanishes; do not literally evaluate `0×log(0/0)`.

**Six-class maximum and within-class collapse.** If a generator repeats one convincing prototype of each of the six digits equally often, and the classifier gives one-hot predictions, every example contributes `ln 6` and IS=6. This is maximal six-class IS despite only six unique images. FID can expose a feature covariance mismatch in such a run but is not guaranteed to distinguish every such failure.

**Split trap.** Ten IS splits require ten separate marginals and ten exponentiations. If four one-hot rows are ordered `(1,0),(1,0),(0,1),(0,1)`, the whole-set score is 2, but two consecutive two-row splits each score 1. Fix and document a reproducible shuffle before splitting so ordering does not create this artificial effect. For the starter's 5,000 total images, ten splits contain 500 each. The standard deviation is across the ten scores, not across individual images' KL values.

**Try without looking:** four two-class rows are `(1,0),(1,0),(1,0),(0,1)`. Find the marginal and whole-set IS. Why would repeating each image 100 times not certify novelty?

<details>
<summary>Checked answer</summary>

Marginal `(0.75,0.25)`; mean KL `0.75 ln(4/3)+0.25 ln 4=0.562335`; IS `exp(0.562335)=1.754765`. Uniformly repeating these rows leaves the full-set probability distribution and score unchanged. IS sees classifier outputs and class balance, not whether each image is new. Split effects depend on how the repetitions are allocated.

</details>

<a id="n4-6"></a>

### N4.6 FID from sample features and diagonal covariance

**Worked 1D sample calculation.** Real features are `(0,2,4)` and generated features `(1,2,3)`. Mean values are both 2. Using unbiased sample covariance (denominator `N−1=2`):

`s_r²=[(−2)²+0²+2²]/2=4`; `s_g²=[(−1)²+0²+1²]/2=1`.

`FID=(2−2)²+4+1−2sqrt(4×1)=1`.

Shift generated features to `(2,3,4)`: mean becomes 3, variance stays 1, so FID becomes `1+1=2`. Identical feature arrays instead give zero. Using denominator N consistently would give different finite-sample values; match the starter's `np.cov(...,rowvar=False)` convention.

**Worked two-dimensional diagonal case.** Suppose `μ_r=(0,1)`, `μ_g=(1,3)`, `Σ_r=diag(1,4)`, `Σ_g=diag(4,9)`.

1. Mean penalty: `(0−1)²+(1−3)²=5`.
2. Product covariance: `diag(4,36)`; its matrix square root is `diag(2,6)`.
3. Trace penalty: `(1+4−2×2)+(4+9−2×6)=1+1=2`.
4. FID is `5+2=7`.

The scalar/diagonal simplification is `Σ_j[(μ_rj−μ_gj)²+(s_rj−s_gj)²]`, where `s` denotes **standard deviation**. Do not plug variances into that final difference. General covariance matrices need a matrix square root; elementwise square roots do not perform the same operation.

**Feature normalization matters.** Multiplying every feature in both sets by 2 multiplies FID by 4: the first sample example's 1 becomes 4. Subtracting the same constant from both sets leaves it unchanged. Standardizing each set separately could erase the very mean/variance mismatch being measured, so retain one fixed feature/preprocessing definition across models.

**Moment limitation.** As theoretical feature distributions, `P=0.5δ_{−1}+0.5δ_1` and `Q=0.25δ_{−√2}+0.5δ_0+0.25δ_{√2}` both have mean 0 and variance 1. Their Gaussian-moment FID is zero although their support and probability distributions differ. This explains why a low FID is evidence about feature moments, not proof of identical distributions.

**Try without looking:** real `(−1,1)` and generated `(0,4)`. Calculate means, unbiased sample variances and 1D FID. Separately, diagonal Gaussian statistics are `μ_r=(0,0)`, `μ_g=(1,−1)`, `Σ_r=diag(1,9)`, `Σ_g=diag(4,1)`; calculate FID.

<details>
<summary>Checked answer</summary>

Sample means 0 and 2; variances 2 and 8. FID `4+2+8−2sqrt(16)=6`. Diagonal case: mean penalty 2; covariance penalty `(1−2)²+(3−1)²=5`; total 7. The square-root values in the diagonal expression are standard deviations.

</details>

**Assignment sanity checklist:** same data ranges and classifier; `(N,128)` features with variables in columns; finite float64 means/covariances; sample-size convention recorded; identical-set FID approximately zero; only tiny imaginary/negative rounding residuals treated as numerical noise. A real-test split distance will generally be positive from sampling variation. A nonlinear classifier does not supply a theorem requiring FID to rise at every Gaussian-noise scale; investigate deviations without replacing the measured curve.

<a id="n5"></a>
## GANs Part 2 — Conditioning and evaluation calculations

These exercises follow [GANs Part 2](support.md#lecture-4). `N4` remains the assignment section so existing links keep working. Here `N5` covers the newly supplied lecture. Metric probabilities and covariances below are given inputs, unless an exercise explicitly asks you to estimate them.

<a id="n5-1"></a>
### N5.1 Conditional encodings, shapes, losses and a gradient

**Source:** pp. 2–15. The parameter count is a study exercise based on the supplied architecture; count dense weights and one bias per output, with no unspecified normalization parameters.

**Worked example**

1. Three one-hot fields of lengths `2,7,2` concatenate to **11 condition values**, with three ones. If all combinations are possible, there are **28 combinations**, not 11. Adding 20 noise values gives G's input length **31**.
2. G's dense layers are `31→256→256→20`. A layer `a→b` has `(a+1)b` parameters, because each of `b` outputs has `a` weights and a bias. Thus G has `32×256 +257×256 +257×20 =8,192+65,792+5,140=79,124` parameters.
3. D sees a 20-value real **or** fake sample plus 11 condition values, so its layers are `31→256→256→1`. D has `8,192+65,792+257=74,241` parameters; combined total **153,365**. A batch of size `B` has G input `(B,31)`, fake output `(B,20)`, D input `(B,31)` and D output `(B,1)`.
4. Let matched-real probability `r=D(x,y)=.8` and generated-pair probability `q=D(G(z,y),y)=.3`. Using one real term plus one fake term, `L_D=−ln r−ln(1−q)=−ln .8−ln .7=.579818`. Practical non-saturating `L_G=−ln q=1.203973`. `y` must accompany both D inputs.
5. For fake logit `s` with `q=sigmoid(s)`, `dL_G/ds=q−1=−.7`. If, locally, `s=2θ+constant`, with the condition and D parameters held fixed, `dL_G/dθ=−1.4`. Descent with learning rate `.1` raises `θ` by `.14`. Freezing D weights does not detach its input gradient.

A mismatched real pair can be another negative only if the objective explicitly includes it. For example, with mismatch probability `.2` and equally weighted fake/mismatch negatives, `L_D=−ln .8−.5[ln .7+ln .8]=.513053`. That differs from the vanilla two-term loss; state the convention before calculating.

**Fresh retry:** noise length 8; categorical fields of lengths 3 and 4; output length 5. Use G `15→10→5`, D `12→10→1`, dense biases included. Give condition length/combinations, both parameter counts and batch shapes for `B=6`. If `r=.9,q=.4`, calculate vanilla `L_D`, non-saturating `L_G`, and `dL_G/dθ` when `ds/dθ=3`. Do not add a mismatch term.

<details>
<summary>Check N5.1 answer</summary>

Condition length **7**, two ones, **12 combinations**. G input is `8+7=15`; D input is `5+7=12`. G parameters `16×10+11×5=215`; D `13×10+11=141`. G input/output `(6,15)/(6,5)`; D input/output `(6,12)/(6,1)`. `L_D=−ln .9−ln .6=.616186`; `L_G=−ln .4=.916291`; `dL_G/dθ=(.4−1)×3=−1.8`.

</details>

<a id="n5-2"></a>
### N5.2 StackGAN conditioning augmentation and resolution

**Source:** pp. 17–21. This small CA vector is an original exercise using the slide's reparameterization, not a complete StackGAN training loss.

**Worked example:** given text-conditioned mean `μ=(1,−2)`, standard deviation `σ=(.5,2)` and fixed noise `ε=(−2,.25)`,

`ĉ=μ+σ⊙ε=(1+.5×(−2),−2+2×.25)=(0,−1.5)`.

The covariance is `diag(.25,4)`, because variances are squares of standard deviations. If the network emits `logvar`, then `σ=exp(logvar/2)`. At fixed `ε`, each coordinate has `∂ĉ/∂μ=1`, `∂ĉ/∂σ=ε`, and `∂ĉ/∂logvar=.5σε`; the last vector is **(−.5,.25)**. This is why gradients can pass through a random sample once its noise draw is held fixed.

For a local scalar downstream objective with incoming gradient `∂L/∂ĉ=(2,−4)`, the chain rule gives `∂L/∂μ=(2,−4)` and `∂L/∂logvar=(−1,−1)`. These are the CA-path derivatives only; additional objective terms would add gradients.

Stage I `64×64×3` contains **12,288** pixel-channel values. Stage II `256×256×3` contains **196,608**: each side grows fourfold, total values **16-fold**, not fourfold. Stage II has no extra separate `z`, but it can resample CA noise; see the correction in §4.3.

**Fresh retry:** `μ=(−1,3)`, `logvar=(ln4,ln.25)`, `ε=(.5,−2)`. Find variance, standard deviation, sample and `∂ĉ/∂logvar`. Incoming gradient is `(3,2)`; find the gradients with respect to `μ` and `logvar`. What is the pixel-count ratio from `32×32` to `128×128` at fixed channels?

<details>
<summary>Check N5.2 answer</summary>

Variances **(4,.25)**; standard deviations **(2,.5)**; sample **(0,2)**. `∂ĉ/∂logvar=(.5,−.5)`; `∂L/∂μ=(3,2)` and `∂L/∂logvar=(1.5,−1)`. Resolution ratio **16**.

</details>

<a id="n5-3"></a>
### N5.3 Entropy identity and the lecture's four-image Inception Score

**Source:** pp. 24–53. Use natural logs. `X` chooses one generated image uniformly; `Y` is a classifier label sampled from its prediction vector. `Pᵢc=p(Y=c|X=i)`, and `m_c=(1/N)ΣᵢPᵢc`.

**Derive before substituting:** expand the average KL:

`(1/N)ΣᵢΣ_c Pᵢc ln(Pᵢc/m_c)`

`= (1/N)ΣᵢΣ_c Pᵢc ln Pᵢc −Σ_c [(1/N)ΣᵢPᵢc] ln m_c`

`= −H(Y|X)+H(Y)=I(X;Y)`.

The marginal definition justifies the second term, and the negative sign in entropy explains the subtraction. Finally `IS=exp(I)`. Entropy with base-two logs instead measures bits; it requires `IS=2^I`, not `exp(I)`.

**Quick confidence check:** the four-class vector `(.99,.003,.002,.005)` has entropy **.066298064 nats**, versus **ln4=1.386294** for uniform probabilities. Confidence alone is insufficient: if every image has exactly the same prediction vector, conditional and marginal entropies are equal, so IS is 1.

**Worked lecture example:**

| Image | Cat | Dog | Bird |
| --- | ---: | ---: | ---: |
| 1 | .90 | .05 | .05 |
| 2 | .80 | .10 | .10 |
| 3 | .10 | .80 | .10 |
| 4 | .05 | .10 | .85 |
| Marginal (column mean) | .4625 | .2625 | .2750 |

For image 1, `KL₁=.9 ln(.9/.4625)+.05 ln(.05/.2625)+.05 ln(.05/.275)`. Do not average across classes: their probabilities already supply the weights.

| Image | Cat term | Dog term | Bird term | Sum = KL |
| --- | ---: | ---: | ---: | ---: |
| 1 | .599173 | −.082911 | −.085237 | .431025 |
| 2 | .438372 | −.096508 | −.101160 | .240704 |
| 3 | −.153148 | .891489 | −.101160 | .637181 |
| 4 | −.111231 | −.096508 | .959195 | .751456 |

Individual terms can be negative; each complete KL is nonnegative. Average the **four row sums** to get **.515091380**; exponentiate once to obtain **IS=1.673791445≈1.674**. Independently, `H(m)=1.062753285` and mean conditional entropy is `.547661906`; their difference agrees. It is reasonable that the answer lies between 1 and 3.

**Interpretation correction:** row four has the largest KL, but it is not the most confident row, nor is its predicted class the rarest marginal class. Its complete distribution has the greatest weighted log-ratio here. Do not replace a calculation with the incorrect p. 48 ranking explanation.

**Fresh retry:** three predictions over two classes are `(.9,.1),(.5,.5),(.1,.9)`. Calculate the marginal, all three KLs, both entropy quantities and IS. Then replace every row by `(.9,.1)` and recalculate IS. Explain why confidence did not rescue the second result.

<details>
<summary>Check N5.3 answer</summary>

Marginal **(.5,.5)**. KLs **(.368064207,0,.368064207)**; mean **.245376138**. Marginal entropy **.693147181**; mean conditional entropy **.447771042**; difference **.245376138**. IS **1.278101966**. With identical rows, the marginal equals every conditional, every KL is zero and **IS=1**, despite confidence .9 on each image. For an absent class with zero marginal, every row also has zero there: omit its zero contribution rather than evaluate `0/0`.

</details>

<a id="n5-4"></a>
### N5.4 IS splits, class collapse and repeated prototypes

**Source:** pp. 38–43, 54–57, 59, 69.

**Worked example:** four perfectly classified images have labels `A,A,B,B`, with prediction vectors `(1,0),(1,0),(0,1),(0,1)`.

- Whole set: marginal `(.5,.5)`, per-image KL `ln2`, hence **IS=2**.
- Two consecutive splits of two: first contains only A, second only B. Each split's own marginal equals every prediction inside it, so split scores are **1,1**, mean **1**, standard deviation **0**.
- Reorder as `A,B,A,B`: each two-image split is balanced and has IS **2**. Split mean is **2**, standard deviation **0**.

This is a small deliberate counterexample, not a claim that ordinary large random splits change by this much. Document ordering/shuffling, splits and seed. Averaging split IS values is not the same operation as computing IS on all samples once.

Now suppose the generator memorizes exactly one convincing A image and one convincing B image, and repeats them evenly. Whole-set IS still equals **2**. It measures class-confidence/diversity, not within-class novelty. If it generates only confident A images, IS becomes **1**. This corrects the lecture's “all cats/dogs scores well” claims without denying IS's other blind spots.

**Fresh retry:** two splits of three perfectly predicted images are `A,A,A` and `A,B,C`. Calculate each split's IS, the mean and population standard deviation (`ddof=0`). Calculate whole-set IS separately. Can a generator repeating one prototype of each of six classes reach IS=6 under a perfect six-class classifier?

<details>
<summary>Check N5.4 answer</summary>

Split scores **1 and 3**, mean **2**, population standard deviation **1** (sample standard deviation with `ddof=1` would be `√2`). Whole-set marginal `(4/6,1/6,1/6)` has entropy **.867563228**; every conditional entropy is zero, so whole-set IS is **2.381101578**, not 2. Yes, balanced repetition of six perfectly classified prototypes gives **IS=6** while missing within-class variation.

</details>

<a id="n5-5"></a>
### N5.5 FID: exact lecture calculation and blind spots

**Source:** pp. 62–82. The supplied matrices are covariances (variances on the diagonal), not matrices of standard deviations.

**Worked lecture example:** `μr=(1,2)`, `μg=(2,3)`, `Σr=diag(2,2)`, `Σg=diag(3,3)`.

1. Mean difference is `(-1,-1)`; squared Euclidean norm is `1+1=2`.
2. Multiply covariances: `ΣrΣg=diag(6,6)`.
3. Its matrix square root is `diag(√6,√6)`, because squaring that matrix recovers `diag(6,6)`.
4. The covariance expression is `diag(5−2√6,5−2√6)`. Its **trace sums both diagonal entries**, giving `10−4√6=.202041029`.
5. Add the mean term: **FID=12−4√6=2.202041029**.

For any diagonal covariances, the covariance contribution simplifies to `Σ_j(√variance_r,j−√variance_g,j)²`. Do not apply entrywise square roots to general covariance products; use a matrix square-root method (or its mathematically equivalent symmetric positive-semidefinite formulation).

**Separate mean/spread drills:** a one-dimensional mean change from 10 to 20 with unchanged variance contributes **100**. Equal means but standard deviations 20 versus 2 contribute **324**; their variances are 400 and 4. These are separate scenarios, not a reason to add 100 to every example.

**Counterexamples:** copying the real reference features exactly gives equal means/covariances and FID zero—so FID does not automatically detect memorization. Even different distributions can share moments: population distribution R has values `−1,+1` with probabilities `.5,.5`; G has `−√2,0,+√2` with probabilities `.25,.5,.25`. Both have mean 0 and variance 1, so Gaussian-moment FID is **0**, although their supports differ. These are population moments, not a claim about an arbitrary finite sample using `N−1` covariance.

**Fresh retry:** `μr=(0,1)`, `μg=(2,−1)`, `Σr=diag(1,9)`, `Σg=diag(4,1)`. Calculate mean, covariance and total terms. Then use exactly the same means/covariances for real and fake and explain what zero does and does not establish.

<details>
<summary>Check N5.5 answer</summary>

Mean term **8**. Covariance term `(1−2)²+(3−1)²=1+4=5`; equivalently matrix product `diag(4,9)`, root `diag(2,3)`, trace of `diag(1,4)` equals 5. Total **FID=13**. With matching moments the score is **0**; this establishes equal fitted Gaussian statistics in this feature space, not equality of arbitrary image distributions or novelty. Sample count and the reference/features/preprocessing must be fixed for meaningful empirical comparisons.

</details>

<a id="n5-6"></a>
### N5.6 Improved generative precision/recall: all radii and both directions

**Source:** pp. 83–96. Use Euclidean distance, `k=1`, exclude each point itself, and include the boundary (`distance≤radius`). Every point's radius comes from its **own** set. The test uses a union of balls, not classification labels.

**Lecture data:** real points `r1=(1,1), r2=(2,1), r3=(1.5,2), r4=(5,5), r5=(6.5,5)`; generated points `g1=(1.2,1.1), g2=(1.8,1.2), g3=(1.4,1.6), g4=(2.2,1.5), g5=(3.5,3)`.

**Step 1: build each set's balls.** For example, `d(g1,g3)=√[(.2)²+(.5)²]=√.29`; this is smaller than `d(g1,g2)=√.37`, so g3 supplies g1's radius.

| Center | Nearest other point in its own set | Radius |
| --- | --- | ---: |
| r1 | r2 | 1 |
| r2 | r1 | 1 |
| r3 | r1 or r2 (tie) | √1.25 = 1.118034 |
| r4 | r5 | 1.5 |
| r5 | r4 | 1.5 |
| g1 | g3 | √.29 = .538516 |
| g2 | g4 | .5 |
| g3 | g1 | √.29 = .538516 |
| g4 | g2 | .5 |
| g5 | g4 | √3.94 = 1.984943 |

**Step 2: precision—test each generated point against the real balls.** One covering ball proves membership; failure needs all balls to fail.

| Query | A covering real ball, or all-center failure | Covered? |
| --- | --- | --- |
| g1 | distance to r1 = √.05 = .223607 ≤ 1 | yes |
| g2 | distance to r2 = √.08 = .282843 ≤ 1 | yes |
| g3 | distance to r3 = √.17 = .412311 ≤ 1.118034 | yes |
| g4 | distance to r2 = √.29 = .538516 ≤ 1 | yes |
| g5 | distances to r1…r5 are 3.201562, 2.5, 2.236068, 2.5, 3.605551; each exceeds that center's radius | no |

Thus **precision=4/5=.8**. Correction: g5's closest real point is **r3**, not r4 as stated on p. 93; the membership conclusion still agrees.

**Step 3: recall—test each real point against the generated balls.**

| Query | A covering generated ball, or all-center failure | Covered? |
| --- | --- | --- |
| r1 | distance to g1 = .223607 ≤ .538516 | yes |
| r2 | distance to g2 = .282843 ≤ .5 | yes |
| r3 | distance to g3 = .412311 ≤ .538516 | yes |
| r4 | g1…g4 distances exceed 4; g5 distance 2.5 exceeds 1.984943 | no |
| r5 | g1…g4 distances exceed 5; g5 distance √13 = 3.605551 exceeds 1.984943 | no |

Thus **recall=3/5=.6**. The left cluster is represented but the right cluster is missed under this estimator. Do not call image quality entirely solved: one generated point is outside the estimated real support. The source's p. 88 cross-distance `r3→r4` should be `√[(3.5)²+3²]=√21.25=4.609772`, not 4.950; this does not change the nearest-neighbor radii or final scores.

**Why “nearest center only” fails:** a separate 1D reference set `{0,1,4}` has `k=1` radii `{1,1,3}`. Query `2.2` is nearest center 1 at distance 1.2, outside that center's radius 1. But center 4's ball has radius 3 and covers the query at distance 1.8. Correct union membership is **true**.

**Fresh retry:** 1D real set `{0,2,10,12}`, generated set `{0,1,2,3}`, `k=1`. List all radii, calculate precision and recall, and explain which set supplies each denominator. Then, without moving points, increase `k`: can any previously covered query become uncovered? Explain using radii, not intuition about “better models.”

<details>
<summary>Check N5.6 answer</summary>

Real radii **(2,2,2,2)**; generated radii **(1,1,1,1)**. Generated 0,1,2,3 all lie in at least one real ball (3 lies one unit from real 2), so **precision=4 generated hits/4 generated points=1**. Only real 0 and 2 lie in generated balls, so **recall=2 real hits/4 real points=.5**. At fixed centers, raising valid `k` can only enlarge or preserve radii, so coverage cannot fall. Both scores can rise from changing this tolerance without improving the generator. Feature extractor, sample count, k and reference must therefore accompany the scores.

</details>


<a id="readiness"></a>
## Readiness check before a quiz or midterm

Choose items within the announced assessment scope. Cover the solutions and complete a fresh problem, including intermediate values and a sentence interpreting the result.

- [ ] Normalize a Bayes posterior, explain a changed prior, and distinguish density estimation from sampling.
- [ ] Compute an AE reconstruction and its stated loss reduction; explain how noise changes the input/target pair in denoising.
- [ ] Convert `logvar` to variance and standard deviation, draw a fixed-noise VAE sample, and calculate discrete/Gaussian KL with the correct direction and sign.
- [ ] Relate reconstruction plus KL to the VAE objective; differentiate through reparameterization and state what is fixed.
- [ ] Compute discriminator and both generator objectives; derive their logit gradients and trace one alternating update.
- [ ] Explain why freezing discriminator parameters during a G update still allows gradients through D's input.
- [ ] Calculate spatial shapes and distinguish class coverage from within-class diversity.
- [ ] Calculate PSNR with its per-image convention, a strict gradient threshold, mode proportions and reverse KL.
- [ ] Count conditional encodings and both network inputs; calculate CA samples and distinguish standard deviation from variance.
- [ ] Derive IS from entropy, reproduce all four lecture KL rows, and explain per-split versus whole-set results.
- [ ] Work the matrix FID example and a matching-moments counterexample; distinguish the assignment's feature space.
- [ ] Build kNN radii excluding self; test any-ball membership both ways and reproduce precision .8/recall .6.
- [ ] Explain an actual run's CSV row and score/image mismatch without replacing measurements with an expected outcome.

For a timed rehearsal, choose one relevant fresh question from each mathematical family and set a realistic time limit. Record whether the difficulty was choosing a formula, arranging shapes, signs, arithmetic, or interpreting the answer. Repair that specific step before trying again. Use the [support guide](support.md) for targeted videos and optional deeper explanations.
