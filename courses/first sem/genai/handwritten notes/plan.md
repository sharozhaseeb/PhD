# Gen AI handwritten notes — page-by-page production plan

Scope: all four lecture decks present on 1 October 2026. Phase 1 covers Lecture 1 and Lecture 2 (10 pages); Phase 2 covers GANs Parts 1 and 2 (10 pages). No new Deep Learning notes. Course outline and assignment are context, not additional lecture decks.

## Reference style and learning contract

Use the Deep Learning reference PNGs as visual/pedagogical references only. White/light cream ruled paper, legible blue handwriting, pink highlighted titles, burgundy numbered section labels, green formula/result boxes. Flat full-page composition, unclipped edges, short purposeful diagrams, ample spacing. Every page is self-contained: goal → symbol definitions/assumptions → formula → numbers/intermediate steps → boxed result → interpretation/traps. Limit to one central calculation or tightly connected examples per page. Prefer two columns only if content remains comfortably readable. Preserve minus signs, superscripts, subscripts, fractions, exact log direction and stated reductions. No dense prose or invented lecture coverage.

Exact generation content is below and in `page-manifest.json`. Original practice numbers are labeled; source examples are identified. Source numbers are PDF page positions. Core theory is integrated into the numerical pages; the first page provides a compact model-family overview rather than reproducing slide history or product timelines.

## Review and generation gates

1. Reviewer agent extracts reference attributes and independently checks the page plan against lecture PDFs, numerical arithmetic, completeness and density.
2. Incorporate required fixes; record explicit agent clearance in `review-log.md` before generation.
3. Generate each PNG with the built-in imagegen tool, one request per page, using approved exact text. Save selected files here. Keep prompts for reproducibility.
4. Root and reviewer inspect all Phase 1 PNGs for visual fidelity, completeness, text and mathematical correctness. Correct or regenerate any defects. Agent must explicitly clear Phase 1 before Phase 2 starts.
5. Generate and inspect Phase 2 likewise. Do not mark any unread/unreviewed output approved. Maintain a linked index and report unresolved issues honestly.

## Planned pages and exact content

### L1-01 — Introduction: what a generative model learns

Phase 1; source: Lecture1 Introduction.pdf, PDF pp. 3–4, 8–18, 22–28, 33–39. Output: `l1-01-introduction-what-a-generative-model-learns.png`.

```text
1) Goal
Learn pθ(x) ≈ p_data(x), then draw new samples x ~ pθ.
x = one observation; θ = learned parameters.
Density estimation scores data; sampling creates data.
An ordinary GAN samples via G(z); its density is usually not tractable.

2) Two questions
Discriminative: given x, predict y using p(y|x).
Generative: model p(x); with labels, p(x,y)=p(x|y)p(y).
Conditional generation models new x given a condition y.
Architecture alone does not decide the task: a CNN can serve either.

3) Model families
Naive Bayes: class-conditional features; GMM: mixture of Gaussians; HMM: hidden-state sequences.
AE: reconstruct through a code (no imposed sampling prior).
VAE: probabilistic encoder + decoder + prior.
GAN: generator competes with a discriminator.
Autoregressive: sample one token at a time.
Diffusion: learn to reverse a noising process.

4) Why and what can fail?
Images, text, music, video, molecules; representation and outlier detection.
Bias can persist; hallucinations, privacy and compute need evaluation.
A plausible sample does not establish truth or fairness.

Takeaway: learn the distribution, not just the decision boundary.
```

### L1-02 — Bayes: from a generative model to a spam decision

Phase 1; source: Lecture1 Introduction.pdf, PDF pp. 29. Output: `l1-02-bayes-from-a-generative-model-to-a-spam-decision.png`.

```text
1) Goal and given values
S = spam; H = ham; W = word “win”.
P(S)=0.40; P(H)=0.60.
P(W|S)=0.60; P(W|H)=0.05.

2) Formula
P(S|W) = P(W|S)P(S) / P(W).
P(W) = P(W|S)P(S) + P(W|H)P(H).
Likelihood × prior → joint; normalize → posterior.

3) Work it out
Spam joint: 0.60 × 0.40 = 0.24.
Ham joint: 0.05 × 0.60 = 0.03.
Evidence: P(W)=0.24+0.03=0.27.
P(S|W)=0.24/0.27=0.8889.
P(H|W)=0.03/0.27=0.1111.
Check: posteriors sum to 1.
At threshold 0.5, predict spam.

4) What if “win” is absent?
P(not W|S)=0.40; P(not W|H)=0.95.
P(S|not W)=0.16/(0.16+0.57)=0.2192.
At threshold 0.5, predict ham.

Exam traps
0.24 is a joint probability, not the posterior.
P(S|not W) is NOT 1−P(S|W).
A generative classifier can classify by applying Bayes.
```

### L1-03 — Data vs model: fidelity, coverage and sampling

Phase 1; source: Lecture1 Introduction.pdf, PDF pp. 37–41. Output: `l1-03-data-vs-model-fidelity-coverage-and-sampling.png`.

```text
1) Goal
Good samples must be plausible AND cover the real possibilities.
Fidelity = samples resemble real data.
Coverage = real modes are represented.
Representation = useful high-level factors in the model.

2) Toy probability table
Region     p_data     p_model
A             0              0.2
B             0.4           0
C             0.6           0.8
Both columns sum to 1.
A: invalid model outputs; B: missing real mode; C: shared support.

3) Expected counts
For N=100 draws, expected count = N × probability.
Model: (20,0,80). Data: (0,40,60).
Expected counts need not equal one observed batch.

4) Sampling by cumulative probability
Draw u uniformly from [0,1).
A if 0 ≤ u < 0.2; C if 0.2 ≤ u < 1.
u=0.05 → A; 0.25 → C; 0.85 → C.
B has no interval: more draws cannot recover it.

Takeaways
Realistic outputs alone do not prove coverage.
Missing a mode in a small grid does not prove zero probability.
Training fits finite data; memorization is not generalization.
```

### L2-01 — Autoencoder: reconstruction and a chain-rule update

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 5–12. Output: `l2-01-autoencoder-reconstruction-and-a-chain-rule-update.png`.

```text
1) Goal and architecture
x → encoder → z → decoder → x̂.
Train x̂ to reconstruct x; the bottleneck stores useful information.
Nonlinear AEs can learn nonlinear representations; PCA is linear.

2) Tiny linear AE (practice example)
x=(1,0); z=a x₁+b x₂+c.
x̂₁=d z+f; x̂₂=e z+g.
(a,b,c,d,e,f,g)=(0.5,0.25,0.1,0.8,−0.5,0.1,0.6).
Encode: z=0.6. Decode: x̂=(0.58,0.30).

3) Reconstruction loss
Use SSE: L=Σ(x̂ᵢ−xᵢ)².
L=(−0.42)²+0.30²=0.2664.
Pixel MSE=L/2=0.1332.

4) Backpropagate to encoder weight a
∂L/∂x̂=(−0.84,0.60).
∂L/∂z=(−0.84)(0.8)+(0.60)(−0.5)=−0.972.
∂L/∂a=(∂L/∂z)x₁=−0.972.
At η=0.1: a_new=0.5−0.1(−0.972)=0.5972.

Takeaway
Add ALL decoder paths before updating the encoder.
Use the original forward-pass weights for every gradient.
SSE and MSE have different gradient scales.
```

### L2-02 — AE applications: targets, retrieval and thresholds

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 11–19. Output: `l2-02-ae-applications-targets-retrieval-and-thresholds.png`.

```text
1) Compression and retrieval
28×28 grayscale = 784 values; code length 2.
784/2=392:1 coordinate reduction (not measured file compression).
Store encoder codes; compare query code with database codes.

2) Retrieval example
Query q=(1,0); A=(2,0); B=(1,1).
Euclidean d(q,z)=√Σ(qᵢ−zᵢ)².
d(q,A)=1; d(q,B)=1 → tie.
Cosine=(q·z)/(‖q‖‖z‖).
cos(q,A)=1; cos(q,B)=1/√2=0.7071 → prefer A.
Cosine is undefined for a zero vector.

3) Denoising: use a CLEAN target
Clean x=(1,0), noisy input=(0.8,0.2), output=(0.9,0.1).
Clean-target SSE=(−0.1)²+0.1²=0.02.
Copying the noisy input gives clean-target SSE=0.08.
At inference only the noisy image is available.

4) Colorization and anomalies
Colorization: grayscale input → paired RGB target.
64×64×1 input = 4096; RGB output = 12288 values.
Anomaly rule: MSE > τ=0.05.
x=(0,1), x̂=(0.4,0.6): MSE=(0.16+0.16)/2=0.16 → flag.
Error equal to τ is not flagged under this rule.
High error is a warning; validate the threshold on held-out data.
```

### L2-03 — VAE: distributions, sampling and latent meaning

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 20–28, 46–54, 61–70. Output: `l2-03-vae-distributions-sampling-and-latent-meaning-v2.png`.

```text
1) Why change the AE?
A plain AE does not impose a known prior over codes.
Random codes may fall in poorly trained gaps.
A VAE encodes a distribution rather than one fixed code.

2) Architecture
x → encoder → μ and ℓ → sample z → decoder → x̂.
qφ(z|x)=N(μ,diag(σ²)); ℓ=ln σ².
Prior p(z)=N(0,I).
For k=2, each head has 2 values; decoder receives 2 values, not 4.

3) Worked sample
μ=(1,−1); ℓ=(ln 0.25,ln 4); ε=(2,−0.5).
Variance exp ℓ=(0.25,4).
Standard deviation σ=exp(ℓ/2)=(0.5,2).
Draw ε ~ N(0,I) (standard normal noise); ⊙ = elementwise multiply.
z=μ+σ⊙ε=(1+0.5×2, −1+2×(−0.5))=(2,−2).

4) Two uses
Reconstruction: sample z from qφ(z|x) for a particular x.
New generation: sample z from p(z), then decode; no encoder needed.
Continuity: nearby codes tend to decode similarly.
Completeness: likely prior codes should decode meaningfully.
Regularization encourages both; neither is a universal guarantee.

Takeaways
Variance, standard deviation and log-variance are different.
Diagonal Gaussian coordinates do not guarantee independent semantic factors.
Latent resampling can help imbalance; test whether debiasing succeeds.
```

### L2-04 — Discrete KL: direction and weighted log-ratios

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 36–37. Output: `l2-04-discrete-kl-direction-and-weighted-log-ratios.png`.

```text
1) Meaning and formula
KL(P‖Q)=Σᵢ Pᵢ ln(Pᵢ/Qᵢ).
The LEFT distribution supplies the weights.
Use natural logs → nats.
KL≥0, and KL(P‖P)=0; it is not symmetric.

2) Lecture example
P=(0.36,0.48,0.16); Q=(1/3,1/3,1/3).
Keep 1/3 exact until the final rounding.
Term 1: 0.36 ln(0.36/(1/3))=0.027706.
Term 2: 0.48 ln(0.48/(1/3))=0.175029.
Term 3: 0.16 ln(0.16/(1/3))=−0.117435.
Sum: KL(P‖Q)=0.085300 nats.

3) Swap the direction
KL(Q‖P)=Σᵢ (1/3) ln((1/3)/Pᵢ).
Terms: −0.025654, −0.121548, 0.244656.
Sum: KL(Q‖P)=0.097455 nats.
The weights AND ratios change.

4) Checks and exam traps
A single term may be negative; the total cannot be.
If Pᵢ>0 and Qᵢ=0, KL(P‖Q)=∞.
A Pᵢ=0 term contributes zero by the limiting convention.
Do not take an unweighted average of the terms.

Takeaway: direction first → ratio → log → weight → sum.
```

### L2-05 — Gaussian KL: derive it, then calculate

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 38–45. Output: `l2-05-gaussian-kl-derive-it-then-calculate.png`.

```text
1) Setup
One coordinate: q=N(μ,v), p=N(0,1), variance v>0.
KL(q‖p)=E_q[ln q(z)−ln p(z)].
For a diagonal Gaussian, sum independent-coordinate KLs.

2) Derive
ln q−ln p=−½ ln v−(z−μ)²/(2v)+z²/2.
E_q[(z−μ)²]=v; E_q[z²]=v+μ².
Therefore KL=−½ ln v−½+(v+μ²)/2.
KL=½(v+μ²−1−ln v).

3) Two-coordinate example
μ=(1,−1); v=(0.25,4).
K₁=½(0.25+1−1−ln 0.25)=0.818147.
K₂=½(4+1−1−ln 4)=1.306853.
Total KL=K₁+K₂=2.125.

4) Log-variance form
ℓ=ln v; v=exp ℓ.
KL=½ Σⱼ(exp ℓⱼ+μⱼ²−1−ℓⱼ).
Equivalent: −½ Σⱼ(1+ℓⱼ−μⱼ²−exp ℓⱼ).

Checks
μ=0, v=1 gives KL=0.
μ=2, v=1 gives KL=2.
Use variance inside ln; sampling uses √v.
The minus sign is correct ONLY with the matching bracket.
```

### L2-06 — VAE objective: reconstruction plus regularization

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 29–35, 46–54. Output: `l2-06-vae-objective-reconstruction-plus-regularization-v2.png`.

```text
1) Two jobs
Reconstruction preserves input-specific information.
KL(qφ(z|x)‖p(z)) discourages unsuitable latent distributions.
Too little KL can leave gaps; too much can lose information.

2) State the reductions
Practice convention: pixel-MSE per image + summed latent KL.
D = pixels per image; B = batch size; v = latent variance.
Rᵢ=(1/D)Σ_d(x̂ᵢd−xᵢd)².
Kᵢ=½Σ_j(vᵢj+μᵢj²−1−ln vᵢj).
L=(1/B)Σ_i(Rᵢ+Kᵢ), with KL coefficient 1.

3) Worked batch, B=2 and D=2
A: x=(1,0), x̂=(0.8,0.25), μ=(1,−1), v=(0.25,4).
R_A=(0.04+0.0625)/2=0.05125; K_A=2.125.
L_A=2.17625.
B: x=(0,1), x̂=(0.3,0.6), μ=(0,1), v=(1,1).
R_B=(0.09+0.16)/2=0.125; K_B=0.5.
L_B=0.625.
Batch L=(2.17625+0.625)/2=1.400625.

4) Theory bridge
ELBO=E_q[ln pθ(x|z)]−KL(q‖p).
Reconstruction NLL + KL minimizes negative ELBO.
A sampled reconstruction estimates that expectation.
MSE corresponds to a Gaussian-likelihood choice with a specified scale.

Exam trap: changing only one reduction changes the reconstruction/KL balance.
```

### L2-07 — Reparameterization: gradients and latent interpolation

Phase 1; source: Lecture 2 AE and VAE v2.pdf, PDF pp. 55–64. Output: `l2-07-reparameterization-gradients-and-latent-interpolation.png`.

```text
1) Make the random sample differentiable
ε ~ N(0,I); z=μ+exp(ℓ/2)⊙ε; hold sampled ε fixed in backprop.
∂z/∂μ=1; ∂z/∂ℓ=½σε.

2) One-dimensional practice example
μ=0.5; ℓ=ln 4; σ=2; ε=0.25; z=1.
Identity decoder x̂=z; target x=0.
R=½(z−x)²=0.5; ∂R/∂z=1.
∂R/∂μ=1; ∂R/∂ℓ=1×½×2×0.25=0.25.
K=½(exp ℓ+μ²−1−ℓ)=0.931853.
∂K/∂μ=μ=0.5; ∂K/∂ℓ=½(exp ℓ−1)=1.5.
For L=R+K: gradients (1.5,1.75).
At η=0.1: μ_new=0.35; ℓ_new=ln4−0.175=1.211294.
Add BOTH gradient paths before updating.

3) Interpolation is a different operation
z(α)=(1−α)z_A+α z_B; 0≤α≤1.
z_A=(−2,1), z_B=(2,3), α=0.25 → z=(−1,1.5).
Decode each intermediate code; nonlinear decoding is not pixel averaging.
Coordinate traversal varies one coordinate and holds the others fixed.

Takeaway: sampling enables training; interpolation probes the learned space.
```

### L3-01 — GAN: the game and loss arithmetic

Phase 2; source: Lecture GANs Part 1.pdf, PDF pp. 3–30, 40–44. Output: `l3-01-gan-the-game-and-loss-arithmetic.png`.

```text
1) Roles
Noise z → G(z) → fake image.
D(x)=probability “real”; D targets: real=1, fake=0.
min_G max_D E_real ln D(x)+E_z ln(1−D(G(z))).
For practical loss minimization, negate D's objective.

2) Loss convention
L_D=−mean_real ln D(x)−mean_fake ln(1−D(G(z))).
L_G,MM=mean_fake ln(1−D(G(z))).
L_G,NS=−mean_fake ln D(G(z)).
During the G step, target generated examples as real.

3) Worked numbers
Real scores=(0.8,0.6); fake scores=(0.25,0.10).
Real mean penalty=(0.223144+0.510826)/2=0.366985.
Fake D mean=(0.287682+0.105361)/2=0.196521.
L_D=0.563506.
L_G,MM=−0.196521.
L_G,NS=(1.386294+2.302585)/2=1.844440.

4) Equilibrium and interpretation
If p_G=p_data and D is optimal with balanced priors, D=0.5.
Then L_D=2 ln2=1.386294; L_G,NS=ln2=0.693147.
D=0.5 alone does not prove distribution matching.
GAN losses are not image-quality scores.

Trap: averaging all real+fake examples halves this L_D convention.
```

### L3-02 — GAN gradients: why non-saturating loss helps

Phase 2; source: Lecture GANs Part 1.pdf, PDF pp. 28–41, 47. Output: `l3-02-gan-gradients-why-non-saturating-loss-helps.png`.

```text
1) Goal
Get a useful learning signal when D confidently rejects G's samples.
Let q=D(G(z))=σ(a), with discriminator logit a.
dq/da=q(1−q).

2) Chain rule
Minimax: L_MM=ln(1−q).
dL_MM/da=[−1/(1−q)]q(1−q)=−q.
Non-saturating: L_NS=−ln q.
dL_NS/da=(−1/q)q(1−q)=q−1.

3) Numerical comparison
Early training: q=0.01.
Minimax logit gradient=−0.01 (weak).
Non-saturating logit gradient=−0.99 (strong).
If da/dθ_G=2, dL_MM/dθ_G=−0.02,
while dL_NS/dθ_G=−1.98.
At θ_G=0.5, η=0.1: NS update gives 0.698.

4) Freeze the right thing
D step: generated samples detached; update only D.
G step: freeze D weights, but backpropagate THROUGH D into G.
θ_G → G(z) → a → loss.
“Frozen weights” does not mean “stop all derivatives.”

Takeaways
Differentiate with respect to the logit before interpreting saturation.
Non-saturating loss improves this signal; it does not guarantee every upstream gradient or fix mode collapse.
```

### L3-03 — GAN: one complete alternating update

Phase 2; source: Lecture GANs Part 1.pdf, PDF pp. 28–29, 42–44. Output: `l3-03-gan-one-complete-alternating-update.png`.

```text
1) Toy setup (one real and one fake)
x_real=1; z=1; G(z)=g z; g=0.
D(x)=σ(w x+b); σ(a)=1/(1+exp(−a)).
w=1; b=0; η=0.1.
L_D=−ln D(real)−ln(1−D(fake)).
Use the sum of separate one-example means.

2) D step: freeze G
Fake x=0; real score=σ(1)=0.731059; fake score=0.5.
BCE logit derivative = prediction−target.
∂L_D/∂w=(0.731059−1)×1+(0.5−0)×0=−0.268941.
∂L_D/∂b=(0.731059−1)+0.5=0.231059.
Simultaneously update:
w_new=1.026894; b_new=−0.023106.

3) G step: use the NEW, frozen D
At g=0: a=−0.023106; q=σ(a)=0.494224.
Use L_G=−ln q.
∂L_G/∂g=(q−1)w_new z
=(−0.505776)(1.026894)(1)=−0.519379.
g_new=0−0.1(−0.519379)=0.051938.

4) Algorithm reminder
Repeat k D updates, then one G update; choose k experimentally.
200 outer iterations with k=3 → 600 D and 200 G steps.
Do not reuse the old D in the G phase.
The updated parameters are not the gradients.
```

### L3-04 — DCGAN: shapes and parameter counts

Phase 2; source: Lecture GANs Part 1.pdf, PDF pp. 45. Output: `l3-04-dcgan-shapes-and-parameter-counts.png`.

```text
1) Follow the generator shapes (H×W×C)
100 → 4×4×1024 → 8×8×512 → 16×16×256
→ 32×32×128 → 64×64×3.
Project and reshape, then learn spatial upsampling.
100 = noise coordinates, not class labels; 3 = RGB channels.

2) Discriminator shapes
64×64×3 → 32×32×64 → 16×16×128
→ 8×8×256 → 4×4×512 → 1 real/fake score.

3) Output-size arithmetic (practice; dilation=1)
Convolution: H_out=floor((H_in+2p−k)/s)+1.
H_in=64, k=4, s=2, p=1:
H_out=floor((64+2−4)/2)+1=32.
Transposed convolution, dilation=1 and output padding=0:
H_out=(H_in−1)s−2p+k.
H_in=4, k=4, s=2, p=1 → H_out=8.

4) Count trainable convolution parameters
Parameters=k² C_in C_out+C_out, when bias is enabled.
k=4, C_in=3, C_out=64:
16×3×64+64=3136.
No bias → 3072 parameters.
Weight sharing means spatial positions do not multiply this count.

Takeaway: “deconvolution” here means transposed convolution, not an exact inverse.
```

### L3-05 — GAN failures, diagnostics and latent arithmetic

Phase 2; source: Lecture GANs Part 1.pdf, PDF pp. 46–70. Output: `l3-05-gan-failures-diagnostics-and-latent-arithmetic.png`.

```text
1) Recognize the failure
Mode collapse: different z values produce too few output types.
Vanishing gradient: G receives a weak learning signal.
Oscillation: two changing players fail to settle.
Loss values alone do not establish sample quality or coverage.

2) Match a response to the problem
Non-saturating loss: stronger early output gradient.
Minibatch discrimination: give D cross-sample similarity information.
Balance update rates; inspect gradients and fixed-noise sample grids.
DCGAN architecture can help stability; no method guarantees success.
Nearest-neighbor checks can reveal copying, but cannot prove novelty alone.

3) Tiny diversity calculation (illustrative)
Two batch features h₁=0, h₂=2.
Similarity exp(−|h₁−h₂|)=exp(−2)=0.1353.
Collapsed pair h₁=h₂=0 gives exp(0)=1.
High similarity can expose repeated outputs to a batch-aware D.
This is a simplified similarity example, not the full learned minibatch layer.

4) Latent operations
Interpolation: z(α)=(1−α)z_A+αz_B.
Attribute direction: d=z_smile−z_neutral.
z_neutral=(1,0), z_smile=(3,1): d=(2,1).
Apply to z_other=(0,2): z_other+d=(2,3).
Decode and check: arithmetic does not guarantee a semantic edit.

Takeaway: evaluate realism, diversity and novelty separately.
```

### L4-01 — Conditional GAN: pairs, encodings and losses

Phase 2; source: Lecture GANs Part 2.pdf, PDF pp. 2–16. Output: `l4-01-conditional-gan-pairs-encodings-and-losses.png`.

```text
1) Goal and architecture
Request an output type by supplying condition y.
[z,y] → G → x̂; [x,y] → D → real-and-matching score.
y can be a class, an image or a text embedding.
D must judge the pair, not only the image or label.

2) Shape example (practice values)
Noise z has length 4; three-class one-hot y=(0,1,0).
Generator input length=4+3=7.
If generated x has 20 values, D input length=20+3=23.
A one-hot has one active entry; concatenated field encodings can have several.

3) Conditional loss arithmetic
Real matching score r=0.8; generated conditioned score q=0.25.
L_D=−ln r−ln(1−q)=0.223144+0.287682=0.510826.
L_G,NS=−ln q=1.386294.
For q=σ(a), ∂L_G/∂a=q−1=−0.75.
Both networks receive y.

4) What can go wrong?
G ignores y: hold z fixed and sweep y to check outputs change appropriately.
D ignores x: label checks alone do not enforce realistic images.
Mismatched real pairs may be used as negatives; state the training scheme.
Conditioning improves control; it does not automatically solve training instability.

Takeaway: unconditional asks “real?”; conditional asks “real and matching?”
```

### L4-02 — StackGAN: sketch, refine and conditioning augmentation

Phase 2; source: Lecture GANs Part 2.pdf, PDF pp. 17–22. Output: `l4-02-stackgan-sketch-refine-and-conditioning-augmentation-v2.png`.

```text
1) Two stages
Text t → embedding φ(t) → conditioning augmentation ĉ.
Stage I: [z,ĉ] → 64×64 RGB sketch (shape and colour).
Stage II: [sketch,text condition] → 256×256 RGB details.
Each stage has a conditioned discriminator.
Stage II has no extra separate z; it may resample conditioning noise.

2) Conditioning augmentation (CA)
ĉ=μ(φ)+σ(φ)⊙ε; ε ~ N(0,I).
ℓ=ln σ²; σ=exp(ℓ/2).
Regularize the conditioning Gaussian toward N(0,I) with KL.
Smooth conditioning helps sparse text embeddings.

3) Worked CA sample (practice)
μ=(1,−1); ℓ=(ln0.25,ln4); ε=(2,−0.5).
σ=(0.5,2); ĉ=(2,−2).
∂ĉ/∂ℓ=½σ⊙ε=(0.5,−0.5).
Use the same variance conventions as the VAE.

4) Resolution calculation
64×64×3=12288 values.
256×256×3=196608 values.
Each side grows 4×; total pixel-channel values grow 16×.

Theory comparison
GANs often give sharper images but can be unstable or collapse.
VAEs offer a probabilistic encoder and reconstruction objective,
but simple likelihood choices can produce blur.
These are tendencies, not guarantees about every model.
```

### L4-03 — Inception Score: entropy, KL and a worked example

Phase 2; source: Lecture GANs Part 2.pdf, PDF pp. 24–57. Output: `l4-03-inception-score-entropy-kl-and-a-worked-example.png`.

```text
1) What IS measures
A classifier gives p(y|x) for each generated image.
Confident images → low conditional entropy.
Varied predicted classes → high marginal entropy.
H(p)=−Σ_c p_c ln p_c; use natural logs.

2) Formula and derivation
m_c=(1/N)Σ_i p(c|x_i).
ln IS=(1/N)Σ_i KL(p(y|x_i)‖m)
=H(m)−mean_i H(p(y|x_i)).
IS=exp(mean KL); higher is better under the same protocol.
Compute the marginal FIRST, then each weighted KL.

3) Lecture example: four images, cat/dog/bird
p₁=(0.90,0.05,0.05); p₂=(0.80,0.10,0.10).
p₃=(0.10,0.80,0.10); p₄=(0.05,0.10,0.85).
m=(0.4625,0.2625,0.2750).
KL₁=0.9 ln(0.9/0.4625)+0.05 ln(0.05/0.2625)
+0.05 ln(0.05/0.275)=0.431025.
Row KLs=(0.431025,0.240704,0.637181,0.751456).
Mean KL=0.515091; IS=exp(0.515091)=1.673791.

4) Blind spots
All identical predictions → IS=1, even if confident.
Balanced repeated prototypes can score highly without novelty.
IS uses generated predictions, not your real reference data.
Split scores depend on split composition; report the protocol.
```

### L4-04 — FID: means, covariances and a worked calculation

Phase 2; source: Lecture GANs Part 2.pdf, PDF pp. 58–82. Output: `l4-04-fid-means-covariances-and-a-worked-calculation.png`.

```text
1) Goal and formula
Compare real and generated distributions in a fixed feature space.
Fit Gaussian moments: means μ_r, μ_g; covariances Σ_r, Σ_g.
FID=‖μ_r−μ_g‖²+Tr[Σ_r+Σ_g−2(Σ_rΣ_g)^(1/2)].
Lower is better under the same evaluation protocol.

2) Lecture example
μ_r=(1,2), μ_g=(2,3).
Σ_r=diag(2,2), Σ_g=diag(3,3).
Mean term=(1−2)²+(2−3)²=2.
Product Σ_rΣ_g=diag(6,6).
Matrix square root=diag(√6,√6).
Covariance expression=diag(5−2√6,5−2√6).
Trace=10−4√6=0.202041.
FID=2+0.202041=2.202041.

3) Reading the result
Most of this gap is in the centres.
For diagonal covariances, spread term=Σ_j(√v_rj−√v_gj)².
Diagonal entries are VARIANCES, not standard deviations.
Entrywise square roots work here because the matrices are diagonal.

4) Limits and fair comparison
FID=0 means matching moments, not proof of identical true distributions.
Copying can also match moments; check novelty separately.
Fix feature extractor, preprocessing, reference and sample count.
Finite-sample FID is biased; KID offers an unbiased estimator.
IS reads class predictions; FID compares feature moments against real data.
```

### L4-05 — Generative precision & recall: quality vs coverage

Phase 2; source: Lecture GANs Part 2.pdf, PDF pp. 83–96. Output: `l4-05-generative-precision-recall-quality-vs-coverage.png`.

```text
1) Build manifolds from feature points
Each point gets radius = distance to its k-th nearest OTHER point
in its OWN set. The manifold is the union of all these balls.
A query is inside if ANY centre covers it: distance ≤ that centre's radius.

2) Two directions
Precision = generated points inside real balls / number generated.
Recall = real points inside generated balls / number real.
Precision tracks quality; recall tracks coverage.
Use feature-space membership, not classification confusion matrices.

3) Complete small 1D example (practice), k=1
Real R={0,2,10,12}; generated G={0,1,2,3}.
Own-set real radii=(2,2,2,2).
Own-set generated radii=(1,1,1,1).
Real balls cover [−2,4] and [8,14].
Generated balls cover [−1,4].
All generated points are in real balls: precision=4/4=1.
Only real 0 and 2 are in generated balls: recall=2/4=0.5.
Good local fidelity; the far real mode is missing.

4) Exam traps
Check the UNION; nearest centre alone can fail.
Self-distance does not count as a neighbour.
The boundary is included; denominators differ.
Larger k enlarges balls and can raise scores without better generation.
Truncation often trades higher precision for lower recall.
Report feature space, k and sample count.
```
