# A2 Viva — Questions & Answers (quick reference)

> 26L-9005 · Part A DDPM · Part B ViT/Swin · Part C attention cost
> Key numbers: T = 1000 steps · linear β 10⁻⁴ → 0.02 · ᾱ < 0.5 at t = 259 (linear) vs 496 (cosine) · probes 30/30

---

## 1. β vs α — what's the difference?
- **β_t** = noise variance added at step t. **α_t = 1 − β_t** = signal variance kept at step t.
- One step: x_t = √α_t · x_{t−1} + √β_t · ε (the two variances add to 1).
- β and α are **per step**. **ᾱ_t** = product of all α up to t, so it is **cumulative**.
- We only choose β; α and ᾱ are computed from it in code.
- *Is ᾱ₀ = 1?* No. Steps are 0-indexed, so ᾱ₀ = α₀ = 0.9999 (linear).
- *Why β < 1?* β = 1 → α = 0, and the sampler divides by √α.

## 2. What is ᾱ_t (alpha bar t)?
- ᾱ_t = α₀ · α₁ · … · α_t, the **share of the clean image's variance still left** in x_t.
- Near 1 the image is almost clean; near 0 it is almost pure noise.
- Closed form: **x_t = √ᾱ_t · x₀ + √(1 − ᾱ_t) · ε**, so training jumps to any t in one go.
- Ours at t = 500: linear **0.078**, cosine **0.492**.
- *Why square roots?* So ᾱ + (1 − ᾱ) = 1, which keeps the variance fixed ("variance preserving").
- *Why can we jump?* A chain of Gaussian steps is itself one Gaussian.

## 3. Linear vs cosine schedule
- **Linear** sets β directly (10⁻⁴ → 0.02). **Cosine** sets the ᾱ curve, and β is derived from it.
- Linear destroys the image faster: ᾱ < 0.5 at **t = 259** vs **496** for cosine.
- Cosine spreads the noise levels evenly, so fewer steps are wasted on near-pure noise.
- Cosine β is clipped at **0.999**. The last step then multiplies by 1/√α ≈ 31.6, so cosine **needs x̂₀ clipping**.
- *Loss 0.028 (linear) < 0.050 (cosine), so linear is better?* No. The same t means a different noise level in each schedule, so the losses aren't comparable.
- *Better samples?* Linear, visually, for our classes. That is a judgement from 16 samples.

## 4. Sampling — explain one step
- Start from pure noise x₉₉₉ ~ N(0, I) and loop t = 999 → 0.
- The U-Net predicts the noise ε_θ(x_t, t).
- **Mean** = (x_t − β_t/√(1 − ᾱ_t) · ε_θ) / √α_t.
- Then add fresh noise **σ_t · z** (none at t = 0).
- Ours: compute **x̂₀**, clamp it to [−1, 1], recompute ε, then update.
- *Why add noise?* To sample the whole distribution; without it everything collapses to a blurry average.
- *Did you change the formula?* Same update, but the ε estimate is cleaned first. The no-clip ablation is in the report.

## 5. Why does sampling depend on the timestep t?
- **Use 1 — network input:** one U-Net is shared by all 1000 noise levels. The time embedding tells it how noisy x_t is.
- **Use 2 — lookup:** t selects the coefficients 1/√α_t, β_t/√(1 − ᾱ_t) and σ_t from the schedule.
- Each step removes only a little noise and needs the previous output, so the steps go **in order** and can't run in parallel.
- Wrong t or skipped steps → wrong noise guess and wrong coefficients → worse samples.
- *1000 calls to sample but 1 to train?* Training jumps to a random t (closed form); going backwards has no closed form.
- *Faster sampling?* Yes, with DDIM-style samplers, without retraining. We used plain DDPM.

## 6. Walk me through your plots
*(For each: the axes → what to notice → the conclusion.)*
- **ᾱ curves + forward grid:** linear destroys faster (259 vs 496).
- **Loss curves:** both converge; 0.028 vs 0.050 are not comparable.
- **Sample grids:** recognisable items from both; linear looks better.
- **Trajectories:** cosine commits to a shape earlier (about t = 900).
- **No-clip ablation:** cosine without x̂₀ clipping → mostly black (62.5% of pixels at −1); linear barely changes.
- **Part B confusion matrices:** both diagonal, **30/30**.
- *Why is the first x̂₀ panel noise?* x̂₀ divides by √ᾱ_t, which is tiny at t = 999, so errors are multiplied by about 157 (linear) or about 20,000 (cosine).

## 7. Linear probing — what and why?
- **Freeze** the backbone, extract one feature vector per image, and train **only a linear classifier** (logistic regression).
- **Why frozen:** it measures the *pretrained* features (how linearly separable they are), not features adapted to our photos.
- Same probe and same split for both backbones, so any difference comes from the features.
- Ours: ViT [CLS] vs Swin global average pooling, both 768-d. Both **30/30**; log-loss **0.0113 vs 0.0168**.
- *Why standardise?* To put features on the same scale; the scaler is fitted on train only (no leak).
- *Why not fine-tune?* 70 photos is too few (it would overfit), and fine-tuning changes the features we want to compare.

## 8. Swin vs ViT
| | ViT-B/16 | Swin-T |
|---|---|---|
| Patches | 16×16 → 196 tokens + [CLS] = 197 | 4×4 → 56×56 = 3136 tokens |
| Attention | global: every token ↔ every token | inside 7×7 windows (49 keys) + shifted windows |
| Scales | one, stride 16 | 4 stages: stride 4, 8, 16, 32 (patch merging) |
| Cost in tokens | **quadratic** | **linear** |
| Normalisation | mean/std 0.5 | ImageNet mean/std |
| Params | 86.6 M | 28.3 M |
- Part C: at 12,544 tokens, window attention is **≈42× cheaper**. Not 256×, because the Q/K/V/output projections cost the same in both.
- *What does the shift do?* It lets neighbouring windows exchange information at no extra cost.

## 9. FPN — and how Swin is used for detection
- Detection needs features at **several scales**, for small and large objects.
- **FPN:** a 1×1 **lateral** conv per stage → **top-down** ×2 upsample + add → 3×3 smoothing → outputs **P2–P5**.
- The top-down path brings **meaning** to the fine maps; the lateral path brings **high-resolution detail**.
- Swin's 4 stages (strides 4/8/16/32) plug straight in, like ResNet's C2–C5 (the Swin paper uses Cascade Mask R-CNN).
- ViT has one stride-16 map and quadratic attention, so it needs an adapter (e.g. ViTDet's simple pyramid).
- *Did you train a detector?* No. We did classification + probing only; `features_only=True` returned the 4 maps an FPN would receive.

## Extra: why the [−1, 1] pixel range?
- It **matches the noise**: ε has mean 0, and so does the image in [−1, 1], so x_T really looks like N(0, I).
- The **scale fits** the variance-preserving math (pixels are not squashed into [0, 1]).
- It gives the **x̂₀ clamp** a clear target: a real image lies in [−1, 1].
- It is the original DDPM convention. Display uses `(x + 1)/2`. ViT's mean/std of 0.5 is the same mapping.
