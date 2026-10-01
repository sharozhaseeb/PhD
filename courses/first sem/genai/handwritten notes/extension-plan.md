# Handwritten notes extension — Diffusion and Transformers

Scope: new Diffusion Parts 1–2 and Transformer lecture PDFs. Extend the existing 20-page set with 17 pages: 3 for Diffusion Part 1, 6 for Diffusion Part 2, 8 for Transformers. Page IDs L5/L6/L7 are the reading order, not instructor-assigned lecture numbers. Original 20 notes stay intact.

## Learning and visual format

Follow [reference attributes](reference-attributes.md): goal → defined givens → formula → substitution → intermediate values → boxed answer → interpretation/exam traps. Blue handwriting on pale ruled notebook paper, pink section highlights, green formula/result boxes, purposeful diagrams. Keep each page self-contained and concise. Use two balanced columns or a wide single column when a numerical table benefits. Wrap equations rather than shrinking the handwriting. If a page cannot remain readable, split it before delivery.

Exact text below is the generation specification. Sources use PDF page positions. Toy examples are marked practice; retain original lecture numerical inputs with corrected results. All logs are natural unless stated.

## Verification gates

The same independent reviewer checks coverage, maths, density and source issues before generation, then reads every generated PNG against the approved text. Correct any ambiguous handwritten glyphs, wrong digits/signs or misleading diagram arrows. Only reviewed final PNGs enter the index and bundle. Built-in imagegen renders each page; retain prompts and review evidence.

## Source corrections to carry through

- Forward conditional variance β_t differs from marginal variance; ‘constant variance’ needs its unit-variance assumption.
- One-shot aggregate Gaussian noise equals accumulated step noise in distribution; an arbitrary independent draw need not reproduce the same path.
- Normalize cosine signal f(t)/f(0); cap β and distinguish target and realized cumulative products.
- Dropping timestep weights intentionally changes the training objective, even when weights do not depend on θ.
- Reverse stochasticity is a DDPM sampler choice, not a requirement for all diffusion methods or a guarantee against memorization.
- Transformer slide22 attention softmax/output arithmetic is inaccurate. Recompute with the row-vector XW convention throughout.
- PE sinusoidal pair dot product demonstrates relative-position information; learned projections/content introduce additional cross terms. No extrapolation guarantee.
- Causal attention includes the current position; SOS presence must be specified. Sum and mean CE differ.

Primary verification references: [DDPM](https://arxiv.org/html/2006.11239), [Improved DDPM](https://arxiv.org/html/2102.09672), [Attention Is All You Need](https://arxiv.org/html/1706.03762). Scope remains the supplied lecture decks, not an expansion to all topics in these papers.

### L5-01 — Forward diffusion: why the square roots matter

Source: Lecture Diffusion Models Part 1.pdf, PDF pp. 1–23. Output: `l5-01-forward-diffusion-why-the-square-roots-matter.png`.

```text
1) Goal and notation
x₀ = clean data; x_t = noisy data at step t.
Forward q is fixed; reverse pθ is learned.
x₀ → x₁ → … → x_T ≈ Gaussian noise.
Generation starts from noise and denoises step by step.

2) Derive the forward rule
Let x_t=a x_(t−1)+b ε_t, with independent ε_t~N(0,I).
For one coordinate with Var(x_(t−1))=1:
Var(x_t)=a²+b². Choose b²=β_t and a²=1−β_t.
Thus x_t=√(1−β_t)x_(t−1)+√β_t ε_t.
q(x_t|x_(t−1))=N(√(1−β_t)x_(t−1),β_t I).

3) Worked scalar step (practice)
β_t=0.19; x_(t−1)=0.8; ε_t=1.
Signal coefficient=√0.81=0.9; noise coefficient=√0.19=0.435890.
x_t=0.9(0.8)+0.435890(1)=1.155890.
A noisy value can exceed the clean-data range [−1,1].

4) Understand the variance
Naive x_t=x_(t−1)+c ε_t with fresh independent noise
gives Var(x_t)=Var(x₀)+t c²; the signal mean is not attenuated.
Conditional variance is β_t, not 1.
Across data: Var(x_t)=(1−β_t)Var(x_(t−1))+β_t.
Variance stays 1 only if the previous variance is 1.
β=0 preserves the sample; β=1 replaces it with noise.
Square roots multiply samples because variance scales by coefficient².
```

### L5-02 — Closed-form noising: derive any timestep

Source: Lecture Diffusion Models Part 1.pdf, PDF pp. 24–34. Output: `l5-02-closed-form-noising-derive-any-timestep.png`.

```text
1) Definitions
α_t=1−β_t; ᾱ_t=∏_(s=1)^t α_s; ᾱ₀=1.
Fresh step noises are independent standard Gaussians.

2) Expand two steps
x₂=√α₂(√α₁ x₀+√β₁ ε₁)+√β₂ ε₂.
=√(α₁α₂)x₀+√(α₂β₁)ε₁+√β₂ ε₂.
Noise variance=α₂β₁+β₂
=α₂(1−α₁)+(1−α₂)=1−α₁α₂.
Combine the Gaussian noises into one ε~N(0,I).

3) General result
x_t=√ᾱ_t x₀+√(1−ᾱ_t)ε.
q(x_t|x₀)=N(√ᾱ_t x₀,(1−ᾱ_t)I).
Signal shrinks and noise variance approaches 1 as ᾱ_t→0.

4) Worked one-shot example (practice)
β₁=0.19; β₂=0.36.
α₁=0.81; α₂=0.64; ᾱ₂=0.5184.
For x₀=0.8 and ε=−0.5:
x₂=0.72(0.8)+√0.4816(−0.5)=0.229013.
Compute any x_t directly without simulating all earlier steps.

Trap: aggregate ε is not the last step's noise draw.
One-shot noising is forward sampling, not one-step image generation.
```

### L5-03 — Sequential vs one-shot: matching the noise correctly

Source: Lecture Diffusion Models Part 1.pdf, PDF pp. 26–34. Output: `l5-03-sequential-vs-one-shot-matching-the-noise-correctly.png`.

```text
1) Same schedule, same clean value
Practice: x₀=0.8; β₁=0.19; β₂=0.36.
α₁=0.81; α₂=0.64; ᾱ₂=0.5184.
Step draws ε₁=1 and ε₂=−0.5.

2) Sequential route
x₁=0.9(0.8)+√0.19(1)=1.155890.
x₂=0.8 x₁+0.6(−0.5)=0.624712.

3) Find the equivalent aggregate draw
Combined noise=0.8√0.19 ε₁+0.6 ε₂.
Aggregate ε=(0.8√0.19−0.3)/√0.4816=0.070193.
One-shot x₂=0.72(0.8)+√0.4816(0.070193)=0.624712.
Use full precision until the final rounding.

4) Recover noise when clean x₀ is known
ε=(x_t−√ᾱ_t x₀)/√(1−ᾱ_t).
Here ε=(0.624712−0.576)/√0.4816≈0.070193.

Takeaways
A new independent aggregate draw has the same distribution,
but need not give the same numerical sample.
At generation time clean x₀ is unknown; a network predicts ε.
Gaussian marginalization justifies the one-shot formula,
not setting every step's random draw equal.
```

### L6-01 — Noise schedules: linear vs normalized cosine

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 2–10. Output: `l6-01-noise-schedules-linear-vs-normalized-cosine.png`.

```text
1) Schedule controls signal and noise
α_t=1−β_t; ᾱ_t=∏_(s=1)^t α_s.
Signal coefficient=√ᾱ_t; noise coefficient=√(1−ᾱ_t).
β_t is a variance contribution, not a standard deviation.

2) Linear schedule
β_t=β_start+(t−1)(β_end−β_start)/(T−1).
Practice T=3, β_start=0.10, β_end=0.30.
β=(0.10,0.20,0.30); α=(0.90,0.80,0.70).
ᾱ=(0.90,0.72,0.504); final signal √0.504=0.709930.
Linear β does not mean linear signal decay.

3) Cosine schedule
f(t)=cos²(((t/T+s)/(1+s))π/2), s=0.008.
ᾱ_t=f(t)/f(0); this normalization makes ᾱ₀=1.
β_t=min(1−f(t)/f(t−1),0.999).
Practice T=4:
t=0: ᾱ₀=1.
t=1: ᾱ₁=0.847012; β₁=0.152988.
t=2: ᾱ₂=0.493844; β₂=0.416958.
After capping β, recompute realized ᾱ using the product.

Takeaway
Cosine preserves signal longer than the lecture's linear schedule.
√ᾱ is a coefficient, not a literal percentage of preserved pixels.
Choose a compatible sampler; do not arbitrarily replace schedules at inference.
```

### L6-02 — Forward diffusion: the lecture's 2×2 numerical

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 11–14. Output: `l6-02-forward-diffusion-the-lecture-s-2-2-numerical.png`.

```text
1) Given matrices
Clean x₀=[[0.8,−0.6],[0.4,1.0]].
Aggregate ε=[[1.0,−0.5],[0.5,−1.0]].
β=(0.19,0.36,0.51); α_t=1−β_t.
Each matrix entry is treated elementwise.

2) Build the schedule table
t        α_t        ᾱ_t        √ᾱ_t
1        0.81       0.81        0.900
2        0.64       0.5184      0.720
3        0.49       0.254016    0.504
√ᾱ₃=0.9×0.8×0.7=0.504.
Noise coefficient=√(1−0.254016)=0.863704.

3) Substitute into x₃=√ᾱ₃ x₀+√(1−ᾱ₃)ε
Top-left: 0.504(0.8)+0.863704(1)=1.266904.
Top-right: 0.504(−0.6)+0.863704(−0.5)=−0.734252.
Bottom-left: 0.504(0.4)+0.863704(0.5)=0.633452.
Bottom-right: 0.504(1)+0.863704(−1)=−0.359704.
x₃=[[1.266904,−0.734252],[0.633452,−0.359704]].

Checks
Keep ᾱ₃=0.254016 until final rounding.
A noisy sample can exceed [−1,1]; do not silently clip.
The supplied aggregate ε is separate from the three step-noise matrices.
This exercise does not require iterating through x₁ and x₂.
```

### L6-03 — DDPM objective: from Gaussian KL to noise error

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 15–24. Output: `l6-03-ddpm-objective-from-gaussian-kl-to-noise-error.png`.

```text
1) Variational learning
Reverse model: pθ(x₀:T)=p(x_T)∏_t pθ(x_(t−1)|x_t).
Training uses an upper bound on expected negative log-likelihood.
Bound = endpoint KL + Σ_(t>1) posterior KL + reconstruction NLL.
Endpoint KL compares q(x_T|x₀) to p(x_T)=N(0,I).

2) Why squared mean error?
For q=N(m_q,σ²I), p=N(m_p,σ²I):
KL(q‖p)=‖m_q−m_p‖²/(2σ²).
Practice: m_q=0.5, m_p=0.3, σ²=0.2.
KL=(0.5−0.3)²/(2×0.2)=0.1.
This formula requires equal covariances.

3) Replace mean prediction by noise prediction
For fixed reverse variance σ_t², the θ-dependent term is
w_t‖ε−εθ(x_t,t)‖²,
w_t=β_t²/[2σ_t²α_t(1−ᾱ_t)].
The endpoint term is constant when the forward schedule is fixed.
The reconstruction term at t=1 is handled separately in the bound.

4) Simplified training loss
L_simple=E_(t,x₀,ε)[‖ε−εθ(x_t,t)‖²], with uniform t.
Dropping w_t changes weighting ACROSS timesteps.
It is an intentional objective simplification, not identical optimization.
The target is aggregate corruption noise, not x_t−x_(t−1).
```

### L6-04 — Noise prediction training: a loss and gradient update

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 24–26, 32–35, 38–39. Output: `l6-04-noise-prediction-training-a-loss-and-gradient-update.png`.

```text
1) Training loop
Sample clean x₀, random t~Uniform{1,…,T}, and ε~N(0,I).
Construct x_t=√ᾱ_t x₀+√(1−ᾱ_t)ε.
Network input=(x_t,t); target=ε.
Update network weights from the noise-prediction error.
Do not run a full reverse sampling chain for each training image.

2) U-Net's job
Noisy image → downsample blocks → bottleneck → upsample blocks.
Skip connections retain spatial information.
Time embedding conditions blocks on the noise level.
One network is reused across timesteps; output matches image shape.

3) Worked loss (practice: mean over two coordinates)
True ε=(1,−0.5); prediction ε̂=(0.8,−0.2).
L=[(0.8−1)²+(−0.2+0.5)²]/2
=(0.04+0.09)/2=0.065.
∂L/∂ε̂=(−0.2,0.3).

4) Isolate one trainable scalar
Toy ε̂₁=w x_t,1; x_t,1=0.5; w=1.6.
∂L/∂w=(−0.2)(0.5)=−0.1.
η=0.1 → w_new=1.6−0.1(−0.1)=1.61.
The real U-Net backpropagates through all its layers.

Takeaway: random t provides an efficient estimate over noise levels;
the network must receive t to interpret the corruption.
```

### L6-05 — Reverse mean: derive the noise-prediction formula

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 20–23, 43–46. Output: `l6-05-reverse-mean-derive-the-noise-prediction-formula.png`.

```text
1) True posterior (clean x₀ known)
q(x_(t−1)|x_t,x₀)=N(A x₀+B x_t,β̃_t I).
A=√ᾱ_(t−1) β_t/(1−ᾱ_t).
B=√α_t(1−ᾱ_(t−1))/(1−ᾱ_t).
β̃_t=β_t(1−ᾱ_(t−1))/(1−ᾱ_t).

2) At inference, estimate clean x₀
x̂₀=[x_t−√(1−ᾱ_t)εθ(x_t,t)]/√ᾱ_t.
Substitute x̂₀ into A x₀+B x_t:
μθ=(A/√ᾱ_t+B)x_t
−[A√(1−ᾱ_t)/√ᾱ_t]εθ.

3) Simplify the coefficients
ᾱ_t=α_t ᾱ_(t−1); β_t=1−α_t.
A/√ᾱ_t+B=1/√α_t.
A√(1−ᾱ_t)/√ᾱ_t
=β_t/[√α_t√(1−ᾱ_t)].
Thus μθ=(1/√α_t)[x_t−β_t εθ/√(1−ᾱ_t)].

4) Numerical check (practice, t=2)
β_t=0.36; α_t=0.64; ᾱ_(t−1)=0.81; ᾱ_t=0.5184.
x_t=0.5; εθ=0.2.
x̂₀=0.501674; A=0.672757; B=0.315615.
A x̂₀+B x_t=0.495312.
Direct formula gives the SAME μθ=0.495312.

Takeaway: generation needs x_t and predicted noise; true clean x₀ is unavailable.
```

### L6-06 — Reverse sampling: a full stochastic step

Source: Lecture Diffusion Models Part 2.pdf, PDF pp. 27–31, 35–40. Output: `l6-06-reverse-sampling-a-full-stochastic-step.png`.

```text
1) Generation loop
Start x_T~N(0,I).
For t=T,…,1: predict εθ(x_t,t), compute μθ,
then sample x_(t−1)=μθ+σ_t z.
z~N(0,I) for t>1; z=0 for the final t=1 step.
μθ=[x_t−β_t εθ/√(1−ᾱ_t)]/√α_t.

2) Worked reverse step (practice, t=2)
β_t=0.36; α_t=0.64; ᾱ_(t−1)=0.81; ᾱ_t=0.5184.
x_t=0.5; predicted εθ=0.2; draw z=0.3.
μθ=[0.5−(0.36/√0.4816)(0.2)]/0.8=0.495312.
Choose posterior variance σ_t²=β̃_t:
β̃_t=0.36(1−0.81)/(1−0.5184)=0.142027.
σ_t=√0.142027=0.376864.
x_(t−1)=0.495312+0.376864(0.3)=0.608371.

3) Understand the randomness
The noise term samples uncertainty in the reverse transition.
Use standard deviation σ_t, not variance σ_t², to multiply z.
Fixed β_t or β̃_t are variance choices; state which is used.
Deterministic samplers also exist; stochasticity is not mandatory
for every diffusion sampler and does not guarantee no memorization.

4) Model comparison
DDPM: repeated denoising calls; usually slower sampling.
GAN: direct generator pass, but adversarial training can be unstable.
VAE: encode/decode with a prior; likelihood choice may blur outputs.
Training order is random t; generation order runs backward.
```

### L7-01 — Transformer: tokens, embeddings and the architecture

Source: Transformer.pdf, PDF pp. 1–13, 53–56, 59–60. Output: `l7-01-transformer-tokens-embeddings-and-the-architecture.png`.

```text
1) Why attention?
RNNs process sequentially and struggle with long dependencies.
Self-attention lets each token access other positions directly.
Training positions can be processed in parallel with correct masks.
Autoregressive generation still produces successive tokens.

2) Input representation
Token ID selects a row of a learned embedding table.
A token ID is not a numerical measure of word meaning.
Original Transformer input = √d_model × embedding + positional encoding.
Practice: 3 tokens, d_model=4 → input shape 3×4.
Vocabulary 10 → embedding table 10×4=40 trainable values.

3) Encoder and decoder blocks
Encoder: self-attention → Add & Norm → FFN → Add & Norm.
Decoder: masked self-attention → Add & Norm
→ encoder–decoder attention → Add & Norm → FFN → Add & Norm.
Decoder Q comes from decoder; cross-attention K,V come from encoder.
Linear vocabulary projection → softmax → next-token probabilities.
Blocks share structure; their learned weights need not be identical.

4) Key dimensions
Self-attention score matrix for n tokens has shape n×n.
For n=3: 9 scores per head; n=6: 36 scores per head.
Doubling sequence length quadruples the score count.
Position info supplies order; unmasked attention alone is permutation equivariant.

Takeaway: embeddings represent tokens; attention builds context;
the vocabulary head chooses the next token.
```

### L7-02 — Self-attention: the lecture's robot calculation

Source: Transformer.pdf, PDF pp. 14–22. Output: `l7-02-self-attention-the-lecture-s-robot-calculation.png`.

```text
1) Rule (ROW-vector convention)
Q=XW_Q; K=XW_K; V=XW_V.
Attention(Q,K,V)=softmax(QKᵀ/√d_k)V.
Softmax is over keys in each query's row.
Query asks; keys determine relevance; values provide output content.

2) Given lecture matrices, d_k=2
X=[[2,1.5],[1.5,0.5],[0.8,0]] (smart, robot, quickly).
W_Q=[[0,0.7],[2.5,1.6]].
W_K=[[0.8,0.7],[0,0.5]].
W_V=[[2,0.5],[1.5,1]].

3) Project and score robot
q_robot=(1.5,0.5)W_Q=(1.25,1.85).
K=[[1.6,2.15],[1.2,1.3],[0.64,0.56]].
V=[[6.25,2.5],[3.75,1.25],[1.6,0.4]].
Raw qKᵀ=(5.9775,3.905,1.836).
Divide by √2 → s=(4.226731,2.761252,1.298248).

4) Normalize and sum values
a_j=exp(s_j−max s)/Σ_k exp(s_k−max s).
Weights=(0.778546,0.179819,0.041635); sum=1.
Output=0.778546(6.25,2.5)+0.179819(3.75,1.25)
+0.041635(1.6,0.4)=(5.606850,2.187793).

Trap: do not transpose the supplied weights midway.
The corrected output follows exact scores, not rounded slide softmax values.
```

### L7-03 — Multi-head attention, FFN and Add & Norm

Source: Transformer.pdf, PDF pp. 23–29, 53–54. Output: `l7-03-multi-head-attention-ffn-and-add-norm.png`.

```text
1) Several representation subspaces
head_i=Attention(XW_Q^i,XW_K^i,XW_V^i).
MultiHead=Concat(head₁,…,head_h)W_O.
Heads can learn different relationships; their roles are not prescribed.

2) Shape calculation
Practice: n=3, d_model=512, h=8, d_k=d_v=64.
Each Q,K,V has shape 3×64; each score matrix is 3×3.
Each head output: 3×64.
Concatenate eight heads → 3×512.
W_O: 512×512 → final 3×512.

3) Position-wise FFN
FFN(x)=ReLU(xW₁+b₁)W₂+b₂.
Same FFN weights at every position within one block.
512 → 2048 → 512 preserves the residual width.
Attention mixes positions; FFN transforms each position's features.

4) Add & Norm (lecture's post-norm convention)
y=LayerNorm(x+Sublayer(x)).
For one token, normalize across its feature coordinates.
Practice: x=(1,3), sublayer=(1,1) → u=(2,4).
Mean=3; variance=[(−1)²+1²]/2=1.
With γ=1, shift=0: normalized u≈(−1,1).
Actual denominator is √(variance+ε), with small ε>0.
Residual addition requires matching shapes.

Takeaway: heads are concatenated, not averaged;
LayerNorm is not normalization across all batch tokens.
```

### L7-04 — Positional encoding: the full d=10 example

Source: Transformer.pdf, PDF pp. 30–52. Output: `l7-04-positional-encoding-the-full-d-10-example.png`.

```text
1) Add order without recurrence
PE(pos,2i)=sin(pos/10000^(2i/d_model)).
PE(pos,2i+1)=cos(pos/10000^(2i/d_model)).
Use zero-based indices and angles in RADIANS.
Position vectors have the same width as token embeddings.

2) Lecture exercise: pos=3, d_model=10
i     denominator       angle      sin        cos
0     1                 3.000000   0.141120   −0.989992
1     6.309573          0.475468   0.457755    0.889079
2     39.810717         0.075357   0.075285    0.997162
3     251.188643        0.011943   0.011943    0.999929
4     1584.893192       0.001893   0.001893    0.999998
Interleave each sin/cos pair:
PE₃=(0.141120,−0.989992,0.457755,0.889079,
0.075285,0.997162,0.011943,0.999929,0.001893,0.999998).

3) Relative-position intuition
For an unprojected single-frequency pair:
[sin i,cos i]·[sin j,cos j]=cos(i−j).
For i=3,j=1: cos2≈−0.416147.
This is a relative-position signal, not a unique distance decoder.
Let Q_i=c_i+p_i and K_j=d_j+r_j (projected content + position).
Q_i·K_j=c_i·d_j+c_i·r_j+p_i·d_j+p_i·r_j.
All FOUR terms matter; learned scores need not depend only on i−j.

4) Frequency and limits
High frequencies vary quickly; low frequencies change slowly.
Fixed sinusoidal PE has no learned parameters.
It is computable at unseen positions; performance at longer lengths
is not guaranteed merely because the formula can be evaluated.
```

### L7-05 — Decoder self-attention: mask future tokens

Source: Transformer.pdf, PDF pp. 55–57. Output: `l7-05-decoder-self-attention-mask-future-tokens.png`.

```text
1) Causal rule
Scores=QKᵀ/√d_k+M.
M_ij=0 when j≤i; M_ij=−∞ when j>i.
Apply the mask BEFORE row-wise softmax.
A decoder token may attend to itself and earlier positions.
Padding masks remove padding separately.

2) Complete masking numerical (practice)
Current query scores=(1,2,3), but only first two keys are allowed.
Masked scores=(1,2,−∞).
Weights=(e¹/(e¹+e²),e²/(e¹+e²),0)
=(0.268941,0.731059,0).
Values v₁=(1,0), v₂=(0,2), v₃=(9,9).
Output=0.268941(1,0)+0.731059(0,2)=(0.268941,1.462117).
The future value contributes exactly zero.

3) Lecture's first-position simplification
If only the first provided target position is visible, its weight is 1.
Row embedding x=(0.3,2);
W_V=[[2,0.5],[1.5,1]].
Value xW_V=(3.6,2.15); self-attention output=(3.6,2.15).
If an SOS key is also included, it must be supplied and accounted for.

Takeaway
Causal masking prevents target leakage during parallel training.
Zeroing a weight AFTER ordinary softmax without renormalizing
does not implement the same attention distribution.
```

### L7-06 — Cross-attention: the lecture's translation numerical

Source: Transformer.pdf, PDF pp. 56, 58. Output: `l7-06-cross-attention-the-lecture-s-translation-numerical.png`.

```text
1) Which side supplies what?
Query comes from decoder state; keys and values from encoder output.
Cross-attention connects the generated prefix to the source sentence.
Source positions are not masked as future target tokens.

2) Given rows (birds, can, fly, high)
Decoder row d=(0.3,2); W_Q=[[0,0.7],[2.5,1.6]].
K=[[1,0],[1.5,0.5],[2,1],[1,1]].
V=[[3,1],[1,0.5],[4,1.5],[0,2]].
d_k=2; q=dW_Q=(5,3.41).

3) Scores and weights
Raw qKᵀ=(5,9.205,13.41,8.41).
Scaled scores=(3.535534,6.508918,9.482302,5.946768).
Subtract max score for stable softmax.
Weights=(0.002414,0.047216,0.923457,0.026912).

4) Weighted value output
o₁=3(0.002414)+1(0.047216)+4(0.923457)+0(0.026912)
≈3.748287.
o₂=1(0.002414)+0.5(0.047216)+1.5(0.923457)+2(0.026912)
≈1.465033.
Output=(3.748287,1.465033).
Use unrounded weights for the final numbers.

Shape check
For m target queries and n source tokens:
Q: m×d_k; K: n×d_k; scores: m×n; output: m×d_v.
Takeaway: weights select source information; output is not a word probability yet.
```

### L7-07 — Transformer training: teacher forcing and cross-entropy

Source: Transformer.pdf, PDF pp. 59–63, 65–67. Output: `l7-07-transformer-training-teacher-forcing-and-cross-entropy.png`.

```text
1) From decoder state to vocabulary
Logits=hW_vocab+b; probabilities=softmax(logits).
Vocab head maps d_model features to |V| scores.
Use the probability of the TRUE next token, not the argmax.

2) Teacher forcing and causal masks
Decoder input: SOS, y₁,…,y_(N−1).
Targets: y₁,…,y_N (include EOS when supplied).
Ground-truth previous tokens enable parallel training.
Causal masking still prevents access to future targets.
Ignore padding when averaging token losses.

3) Lecture sentence numerical
Correct-token indices are ONE-based: (3,8,5,7,4).
Given predicted probabilities at those indices:
p_correct=(0.4,0.2,0.2,0.3,0.3).
CE_t=−Σ_v y_t,v ln p_t,v=−ln p_t,correct.
Per-token losses=(0.916291,1.609438,1.609438,1.203973,1.203973).
Sentence SUM=6.543112 nats.
Token MEAN=6.543112/5=1.308622 nats.

4) Gradient and traps
For softmax logits, ∂CE/∂logit_v=p_v−y_v.
If correct p=0.4: gradient for its logit=0.4−1=−0.6.
Mean over N tokens divides token gradients by N.
Natural logs give nats; log base 2 gives bits.
The lecture uses both sum and mean: state your chosen reduction.
```

### L7-08 — Generation: greedy decoding vs beam search

Source: Transformer.pdf, PDF pp. 55, 59, 64. Output: `l7-08-generation-greedy-decoding-vs-beam-search.png`.

```text
1) Autoregressive generation
Start with SOS; predict the next-token distribution.
Choose a token, append it, and repeat until EOS or the length limit.
Inference uses the generated prefix, unlike teacher forcing.
The source encoder output can be reused.

2) Greedy vs beam
Greedy keeps the highest-probability next token at each step.
Beam width B keeps B candidate prefixes by cumulative log score.
Score(sequence)=Σ_t ln p(token_t|prefix,source).
Beam search is an approximation, not a guarantee of the best sequence.

3) Complete two-token numerical (practice)
First step: P(A)=0.6, P(B)=0.4.
After A: P(X|A)=0.51, P(Y|A)=0.49.
After B: P(X|B)=0.99, P(Y|B)=0.01.
Joint scores:
AX=0.6×0.51=0.306; AY=0.294.
BX=0.4×0.99=0.396; BY=0.004.
Greedy chooses AX; beam width 2 keeps A and B initially,
then finds BX with probability 0.396 > 0.306.
Equal-length log scores: ln0.306=−1.184170; ln0.396=−0.926341.

4) Interpretation
Beam considers sequences, not independent token argmaxes.
Length penalties may be needed when comparing different lengths.
Wider beams cost more; decoding choices affect outputs.
The softmax head is a distribution; greedy and beam are selection rules.
```
