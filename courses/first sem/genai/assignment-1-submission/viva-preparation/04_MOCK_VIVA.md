# Mock viva

Use a timer. Give the direct answer first, then equation/evidence, then one limitation. Score each answer 0-2: 0 incorrect, 1 conceptually right but unsupported, 2 correct and tied to this run.

## Round 1: core concepts, 12 minutes

1. In 30 seconds, describe the complete assignment.
2. Derive the VAE KL expression from `mu` and `logvar`.
3. Why is the KL divided by 12,288 in your code?
4. Why does the AE decode its own codes but fail on normal draws?
5. Derive both logistic generator gradients with respect to the fake logit.
6. Why do the objectives share an equilibrium but behave differently early in training?
7. Derive reverse KL and the `ln 6` result.
8. State the WGAN-GP critic and generator objectives.
9. Derive IS and express it using entropies.
10. Explain every term in FID and two things it can miss.

Target: at least 18/20 with no missing equation.

## Round 2: evidence challenge, 12 minutes

1. Prove your roll-derived values from R=27.
2. Open the exact C1 row used as the reference.
3. Calculate its 1% threshold and prove row 448 is the first crossing.
4. What happened at row 447, and why does it matter to your wording?
5. Show whether the reported threshold used the first-layer or full gradient.
6. Recompute C3's number of modes and reverse KL from raw counts.
7. Point to D1 and D2 proportions and describe their remaining imbalance.
8. Show one saved IS split and identify its tensor shapes.
9. Distinguish the real-training FID reference, the real row, and the floor.
10. Point to the preflight trace that best demonstrates natural debugging.

Target: all files opened in under 30 seconds each and at least 18/20.

## Round 3: code ownership, 15 minutes

Write or explain without looking:

1. VAE reparameterization and KL.
2. Stable saturating and non-saturating loss lines.
3. `mode_stats`, including zero KL terms and the 1% rule.
4. WGAN-GP interpolation and penalty.
5. IS for one split.
6. FID means, covariances, `sqrtm`, imaginary check, and epsilon retry.
7. Why `fake.detach()` and parameter freezing occur in different phases.
8. Why `create_graph=True` is necessary.

Target: no sign error and no confusion between probability/logit/critic score.

## Round 4: hostile examiner follow-ups

### “Your validation VAE loss is lower than training. Is that suspicious?”

Training reconstructs sampled `z`, while validation decodes `mu`; BatchNorm modes also differ. The train/validation reconstruction values therefore are not under identical stochastic conditions. The fair AE/VAE comparison uses the validation reconstruction values.

### “You violated the seed rule.”

The base seed is 1327, and every offset is recorded. Offsets create deterministic independent substreams, but the approach is not literal compliance with resetting 1327 for every run. This is a reproducibility limitation, not something to hide.

### “Your FID code produced a singular warning. Why trust it?”

Total collapse makes covariance low-rank. The result remained finite, the imaginary component was zero, and two sanity checks behaved correctly. Still, adding diagonal regularization proactively or using a symmetric PSD formulation would be a stronger implementation.

### “WGAN-GP improved FID. Prove the gradient penalty caused it.”

I cannot isolate that cause: objectives, critic steps, learning rate/betas, and critic BatchNorm also changed. The defensible conclusion is that the complete WGAN-GP configuration performed better in this fixed run.

### “Why should I trust a classifier judging GAN samples?”

It achieved 99.019% on in-domain held-out digits and its confusion matrix is saved, but artifacts are OOD and can receive confident labels. Therefore I combine classifier statistics with sample grids and FID; none is sufficient alone.

### “Did your C3 samples objectively stop changing?”

No quantitative temporal stopping metric was logged. The run ended after 3,000 outer iterations and showed complete final collapse by grid and 5,000-sample histogram. I should not claim more than that evidence.

### “Why is real FID not zero?”

The real row is a real test subset compared with a separate real training reference. The floor is another comparison between two disjoint test halves. Only the sigma=0 sanity check compares an image set with itself.

### “Why are A4 and B2 missing?”

They are referenced but not defined in the supplied handout. I completed every explicit technical task and did not invent requirements.

## Readiness standard

You are ready when you can complete all rounds twice on different days, score at least 90%, make no loss-sign or set-identity error, and open each evidence file without searching the entire folder.
