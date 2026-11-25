# Examiner: What Video 2 Must Cover

Examiner persona: Dr. Maryam Bashir. Student: Sharoz Haseeb, 26L-9005, d = 5 (A2). A3: Track 3, seeds 3 and 103.
Purpose: list what the student must be able to **write, explain and redraw** without notes. The numbers to memorise are in `TPM_RISK_REGISTER.md` §2. This page covers understanding.

**Notation card (show it first, keep it on screen in both parts):**
hat `x̂`, `ε̂` = the model's **estimate** of something it cannot see. bar `ᾱ` = **cumulative product** of everything up to t. θ subscript = **learned by gradient descent**; anything without θ is fixed or sampled. `⊙` = element-wise multiply, with no mixing across features. `α/r` = LoRA scale. Note that this α is **not** the diffusion α_t. Point out the clash on screen.

---

## Assignment 2

### (a) Formulas to write on the board

| Part | Formula | Understanding test | Intuition a good answer contains |
|---|---|---|---|
| A1 | `α_t = 1 − β_t`, `ᾱ_t = ∏_{s≤t} α_s` | "What is β, and what does the bar mean?" | β_t is the noise variance added at step t; ᾱ_t is the share of the original signal's variance that survives after t steps. |
| A1 | `x_t = √ᾱ_t x_0 + √(1−ᾱ_t) ε`, ε ~ N(0, I) | "Why square roots? Why can you jump to any t?" | The variances add to ᾱ + (1−ᾱ) = 1, so the scale never blows up (variance preserving). A chain of Gaussian steps is itself one Gaussian, so there is a closed form. |
| A1 | cosine: `ᾱ_t = f(t)/f(0)`, `f(t) = cos²(((t/T + s)/(1+s))·π/2)`, `β_t = 1 − ᾱ_t/ᾱ_{t−1}`, clipped at 0.999 | "Why define ᾱ first and derive β from it?" | Cosine designs the signal curve directly so that it falls slowly in the middle. β is just whatever produces that curve. The clip stops β reaching 1, because then α_t = 0 and the sampler divides by zero. |
| A2 | `L = ‖ε − ε_θ(x_t, t)‖²` | "Which symbols are random, which are learned, and why predict ε rather than x_0?" | x_0, t and ε are sampled; only θ is learned. Predicting the noise is a fixed-scale regression target at every t, and it is the simplified ELBO term from Ho et al. |
| A3 | `x_{t−1} = (1/√α_t)(x_t − (β_t/√(1−ᾱ_t)) ε_θ) + σ_t z`, `σ_t² = β_t` | "Which part removes noise and which part adds noise? Why add noise at all?" | The bracket subtracts the predicted noise and rescales to give the mean of the posterior. σ_t z keeps the sampler stochastic, so it samples the distribution instead of collapsing to one average. There is no z at t = 0. |
| A3 | `x̂_0 = (x_t − √(1−ᾱ_t) ε_θ)/√ᾱ_t` | "Derive this from the forward formula. Why is it noise near t = 999?" | It is the forward equation solved for x_0 with ε replaced by its estimate. Dividing by a tiny √ᾱ multiplies any error in ε (about 157× for linear, about 20,000× for cosine). This is also why clipping x̂_0 matters. |
| B1 | ViT `N = (224/16)² = 196`, +1 [CLS] = 197; Swin `224/4 = 56`, so 56²×96 → 28²×192 → 14²×384 → 7²×768 | "Where does token 197 come from? What does patch merging do?" | [CLS] is a learned token added after patch embedding. Merging concatenates 2×2 neighbours (4C) and projects to 2C, which halves the resolution and doubles the width, like a CNN pyramid. |
| B2 | `z = W·feat + b`, softmax, macro-F1 = mean over classes of `2PR/(P+R)` | "Why freeze the backbone? Why standardise the features?" | A frozen probe measures how linearly separable the pretrained features already are. The scaler is fitted on training data only, so test statistics do not leak into training. |
| C | `Ω(MSA) = 4hwC² + 2(hw)²C`; `Ω(W-MSA) = 4hwC² + 2M²hwC`; windows = (h/M)(w/M) | "Where does each term come from? Why is the ratio not 256?" | 4hwC² is the Q, K, V and output projections (four hw×C by C×C products). 2(hw)²C is QKᵀ plus attention×V. Windowing only shrinks the second term, from hw keys per query to M² keys. The shared projection term pulls the ratio down to 12,800/305 ≈ 41.97. |

### (b) Diagrams a weak student must be able to redraw

1. **Forward and reverse chain.** Draw x_0 → x_t → x_T on a line. Forward arrows are labelled q and fixed; backward arrows are labelled p_θ and learned. Below the chain, draw both ᾱ_t curves, with the linear curve crossing 0.5 at t ≈ 259 and the cosine curve at t ≈ 496. Shade the linear "pure noise" zone from t = 673 to 999.
2. **Training step versus sampling loop.** Put them side by side. Training is one box: sample t, make x_t, make **one** U-Net call, compute the loss. Sampling is a loop of 1000 boxes, where each output feeds the next input. The arrow between boxes is the sequential dependence.
3. **One reverse step.** Show x_t → U-Net → ε_θ. The path then splits: (i) ε_θ → x̂_0 → clamp to [−1, 1] → recompute ε; (ii) ε → mean → + σ_t z → x_{t−1}. The diagram must show that clipping happens inside the step, not after it.
4. **ViT versus Swin token maps.** ViT is one flat 14×14 grid at every depth, with [CLS] attached. Swin is a pyramid of four grids at strides 4, 8, 16 and 32, with the FPN arrows coming off each level.
5. **Global attention versus windowed attention.** Draw a 112×112 map. MSA connects one query to every token. W-MSA puts a 7×7 window around the query, and alternate blocks shift the window by M/2 so that neighbouring windows exchange information.

### (c) Five "why" questions that expose students who did not do the work

1. Why does one training step need one network call while sampling needs 1000, and why can't the 1000 steps run in parallel?
2. Why is your cosine loss (0.050) higher than your linear loss (0.028), and why does that not mean that linear trained better?
3. Why did the cosine sampler break without x̂_0 clipping? Answer using 1/√α_999 ≈ 31.6, not "it is standard".
4. Why can Swin feed an FPN detector while ViT cannot? The answer must mention the multi-scale pyramid and the quadratic cost of global attention, not "Swin has convolutions".
5. Why does windowed attention make the cost linear in hw, and what does the shifted window recover that plain windows lose?

---

## Assignment 3

### (a) Formulas to write on the board

| Part | Formula | Understanding test | Intuition a good answer contains |
|---|---|---|---|
| 1 | fertility = subword tokens / words; max_length = p95 of token lengths (43) | "Why does high fertility cost accuracy and money?" | One word split into many pieces makes longer sequences, more truncation and attention cost that grows with length². The model also sees fragments instead of units of meaning. |
| 2 | LoRA: `h = W₀x + (α/r)·B A x`, with `B ∈ ℝ^{d×r}` initialised to 0, `A ∈ ℝ^{r×k}` random, and W₀ frozen | "What are the shapes? Why is B zero? What does α/r do?" | The update is forced to have rank r. B = 0 means ΔW = 0 at step 0, so training starts exactly at the pretrained model. α/r fixes the update size so that changing r does not rescale it. With α = 16 held fixed, r = 8 gives scale 2 and r = 16 gives scale 1, which confounds the rank comparison. |
| 2 | LoRA params = `r(d + k)` per module, so 12 × 2 × 8 × 1536 = 294,912 | "Rebuild 887,811 for me." | The adapters account for 294,912 parameters. The XLM-R classification head (768×768 + 768×3, with biases) is trainable and adds 592,899. |
| 2 | QLoRA: W₀ stored in NF4 (4-bit) plus double quantisation; compute `dequant(W₀)·x` in fp16, plus the LoRA path in higher precision | "What is in 4-bit and what is not? Why is it slower?" | Only the frozen base Linear weights are 4-bit. The adapters, the head, the LayerNorms and the embeddings are not. Weights are dequantised on every forward and backward pass, which saves memory but costs compute. |
| 2 | IA³: `K′ = l_k ⊙ K`, `V′ = l_v ⊙ V`, `h_ff′ = l_ff ⊙ γ(W₁x)`, with the l vectors initialised to 1 | "What does ⊙ mean, and why start at 1?" | Each feature channel is rescaled by its own number (above 1 amplifies, below 1 inhibits), and no new matrices are added. Starting at 1 is the identity, so step 0 is the pretrained model. That gives 12 × 2 × 768 = 18,432 parameters plus the head. |
| 3 | Memory for full fine-tuning ≈ 16 bytes/param (weight + grad + 2 Adam moments, all fp32) | "Why does Full FT need 4,997 MiB and QLoRA 943 MiB?" | Optimiser state exists only for trainable parameters. PEFT removes almost all gradients and Adam states, and QLoRA also shrinks the frozen weights. |
| 3/4 | macro-F1 = (F1_P + F1_N + F1_O)/3; SD with n = 2 is `|a−b|/√2` | "Derive MuRIL's 0.222." | Predicting all-Negative gives F1_N = 2/3 and 0 for the other two classes, so (2/3)/3 = 0.222. Macro averaging punishes ignoring a class even when that class is tiny. |

### (b) Diagrams a weak student must be able to redraw

1. **LoRA (required).** Draw a frozen W₀ block (grey, with a lock). Beside it draw a trainable bypass: x → A (d → r, narrow) → B (r → d) → ×α/r → ⊕ with the W₀x output. Label the shapes and "B = 0 at init". Add a second panel showing where it sits in one encoder layer: query and value (exp 02/03), plus output.dense in the FFN (exp 04).
2. **QLoRA (required).** Draw a memory stack. At the bottom is the base W₀ in **NF4 4-bit**, with double-quantised scale constants. An arrow labelled "dequantise per layer, per pass" leads to fp16 compute. On top sit the LoRA A and B and the head, in higher precision and trainable. To the side, the paged AdamW state is drawn with a dotted arrow to CPU RAM labelled "only under GPU pressure". Add a small bar comparing 4,997 MiB, 1,385 MiB and 943 MiB.
3. **IA³.** Show the same encoder layer with three small vectors l_k, l_v and l_ff multiplying via ⊙ on K, V and the FFN hidden activation. Make it visually obvious that IA³ adds vectors where LoRA adds matrices.
4. **Pareto plot.** Plot macro-F1 against peak memory with Full FT, LoRA, QLoRA and IA³ as points, and draw the frontier. The student should be able to say which points are dominated.
5. **Tokenisation.** Take one Urdu word and split it under XLM-R and under MuRIL, showing the fertility count and an [UNK] example.

### (c) Five "why" questions that expose students who did not do the work

1. Why is B initialised to zero rather than A? (If A were zero, B would receive no gradient at step 0, and the learning dynamics would differ.)
2. Why does QLoRA save memory yet run slower than LoRA, and why do paged and unpaged runs give identical F1?
3. Why does IA³ train 0.22% of the parameters when the handout says about 0.05%? (The trainable classification head is included.)
4. Why did you select the RQ3 configurations on validation and not on test? Is "IA³ degrades least" a real robustness result? (It started near the floor, at 0.242.)
5. Why is r = 16 not evidence of anything over r = 8 here? (α/r changed as well, and the gap is inside the two-seed SD.)
