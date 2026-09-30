# Start here: viva readiness checklist

## Thirty-second description

I compared a same-backbone AE and VAE on CelebA, showed why only the VAE can sample from a normal prior, trained an MNIST denoising AE, deliberately produced vanishing gradients and mode collapse in GANs, then trained DCGAN and WGAN-GP alternatives. I evaluated the saved runs with a six-digit classifier, reverse KL, my own IS and classifier-feature FID. The key evidence is the C1 gradient dying at iteration 448, complete C3 collapse to digit 3, and D2 reaching FID 17.117 while covering all six modes.

## Facts to know without looking

| Item | Exact fact |
|---|---|
| Roll / R / seed | `20L-11327` / 27 / 1327 |
| Assigned values | held-out 7; digits `[0,2,3,6,7,9]`; `Blond_Hair` plus Smiling |
| Main run | `20L-11327_main_v1`, CUDA |
| CelebA split | 27,000 train / 3,000 validation |
| AE/VAE | latent 64, Adam 1e-3, batch 64, 10 epochs |
| AE validation MSE | 0.0066048581 |
| VAE validation MSE | 0.0083013152; gap 0.0016964571 |
| Denoising PSNR | 13.3204 -> 19.4447 dB; gain about 6.124 dB |
| Classifier | 99.0194% on the six assigned digits |
| C1 reference | iter 100 first-layer norm `7.0218186e-05` |
| C1 threshold/death | 1% = `7.0218186e-07`; first crossing iter 448, norm 0 |
| C2 at iter 448 | first-layer norm 3.83656; full norm 11.29571 |
| C3 | counts `[0,0,5000,0,0,0]`; digit 3; 1 mode; reverse KL ln(6)=1.791759 |
| D1 | 6 modes; reverse KL .052779; IS 4.4772 +/- .1080; FID 39.700 |
| D2 | 6 modes; reverse KL .019803; IS 4.6190 +/- .0898; FID 17.117 |
| Real evaluation | IS 5.7720 +/- .0262; FID 1.39865 |
| C1 / C3 FID | 941.881 / 821.241 |
| FID floor | 1.200874 |
| Noise FID | sigma 0/.1/.25/.5/1 -> 0/14.144/100.552/326.750/543.036 |

## Checklist

- [ ] Derive the VAE KL term and reparameterization without notes.
- [ ] Explain the exact loss scaling used in the code and why beta is still 1.
- [ ] Explain the A3 control: AE own codes work, normal prior codes do not.
- [ ] Derive PSNR from MSE for values in `[0,1]`.
- [ ] Derive `d log(1-D)/da = -D` and `d[-log D]/da = -(1-D)`.
- [ ] Open `evidence/C1.csv`, point to rows 100, 447, and 448, and calculate the threshold.
- [ ] Explain why the 447-to-448 transition is abrupt rather than a smooth decay.
- [ ] Distinguish `g_grad_norm` (first generator layer) from `g_full_grad_norm`.
- [ ] Recompute C3 reverse KL from the six class counts.
- [ ] State that actual digit 3 is remapped class index 2.
- [ ] Explain the 1% mode-coverage rule: at least 50 of 5,000 samples.
- [ ] Trace D1 architecture and explain `[0,1] <-> [-1,1]` scaling.
- [ ] Write the WGAN-GP critic loss, generator loss, interpolation, and penalty.
- [ ] Explain why WGAN uses critic scores, not probabilities, and no critic BatchNorm.
- [ ] Derive IS and explain its two desired properties.
- [ ] Derive FID and identify the exact feature/reference sets.
- [ ] Explain the non-zero FID floor and the sigma=0 near-zero result.
- [ ] Explain the singular-covariance warning for collapsed samples.
- [ ] Name at least three limitations without weakening valid conclusions.
- [ ] Explain the handout/starter inconsistencies without claiming extra work.
- [ ] State the disclosed AI assistance honestly and demonstrate ownership live.

## The highest-risk examiner probes

1. Why was iteration 448 selected, and is it based on the full gradient?
2. What exactly changed between C1 and C2?
3. Why does the VAE loss divide KL by the pixel count?
4. Why can a collapsed covariance make `sqrtm` numerically awkward?
5. Are D2's `D_x` and `D_G_z` probabilities?
6. Did every run literally reset to seed 1327?
7. Why are A4, B2, and Part F absent?
8. Which parts of the code can you write unaided during the viva?

## Study order

First memorize the facts table. Then do the five derivations in `02_DERIVATIONS_AND_NUMERICALS.md`. Next perform every live drill in `03_CODE_AND_EVIDENCE_WALKTHROUGH.md`. Finish with both mock rounds without reading answers.
