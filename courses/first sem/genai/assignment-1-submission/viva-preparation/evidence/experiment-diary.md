# Experiment diary - 20L-11327 / main_v1

## Preflight

- Planned settings: shape/range checks, 100-step ten-image overfits, and a 20-step GAN smoke test before the full run.
- Observation: AE loss 0.08841 to 0.00226; VAE reconstruction loss 0.10547 to 0.00240; denoiser 0.23297 to 0.01328; classifier 1.78433 to 0.00000409. GAN losses and gradients remained finite.
- Check performed: printed tensor shapes and ranges and saved the four preflight CSV traces.
- Action taken: enabled the full run without changing the architecture.
- Outcome and evidence: `logs/preflight_*.csv` and the executed notebook outputs.

## A1

- Planned settings: same-backbone AE/VAE, latent size 64, Adam 1e-3, batch 64, 10 epochs, fixed 27,000/3,000 CelebA split.
- Observation: AE validation MSE 0.006605; VAE validation MSE 0.008301. Both reconstruct identity and major colour structure, while the VAE is visibly smoother.
- Check performed: compared final train/validation rows and the same eight validation images.
- Action taken: none.
- Outcome and evidence: `logs/A1_ae.csv`, `logs/A1_vae.csv`, `figures/A1_recon.png`.

## A2

- Planned settings: 11 mean-code interpolation points for Smiling and Blond_Hair.
- Observation: both strips remain face-like. Smiling strengthens gradually after roughly the middle; hair changes from dark to blond progressively, with identity and hair shape also changing.
- Check performed: inspected labelled candidate grids and saved endpoint indices 22017 and 2816.
- Action taken: used the first clearly labelled negative/positive pair chosen by the fixed validation ordering.
- Outcome and evidence: `logs/A2_endpoints.json`, `figures/A2_vae_interp.png`.

## A3

- Planned settings: decode the same 16 N(0,I) codes with AE and VAE, plus AE codes produced by real images.
- Observation: AE prior samples are mostly brown, face-like averages, but the VAE prior produces diverse faces. The AE produces recognizable reconstructions only from its own encoder codes.
- Check performed: used the identical saved latent tensor for both prior rows.
- Action taken: none.
- Outcome and evidence: `samples/A3_shared_z.pt`, `figures/A3_prior_samples.png`.

## B1

- Planned settings: SmallAE, sigma 0.3 Gaussian corruption, clean target, Adam 1e-3, five epochs.
- Observation: validation MSE fell from 0.02427 to 0.01272. PSNR improved from 13.320 dB (noisy) to 19.445 dB (denoised).
- Check performed: used one seeded noisy test tensor for both PSNR values and inspected clean/noisy/denoised rows.
- Action taken: none.
- Outcome and evidence: `logs/B1_denoise.csv`, `figures/B1_denoise.png`, `metrics.json`.

## Classifier

- Planned settings: six assigned digits [0,2,3,6,7,9], remapped to 0..5, minimum three epochs.
- Observation: restricted test accuracy reached 0.99019 after three epochs.
- Check performed: saved the full confusion matrix and enforced the 97% gate before GAN evaluation.
- Action taken: no extra epochs were needed.
- Outcome and evidence: `logs/classifier.csv`, `logs/classifier_confusion.csv`, `ckpt/clf.pt`.

## C1

- Planned settings: saturating generator loss, five D steps per G step, lr_D 8e-4, lr_G 2e-4, 3,000 iterations.
- Observation: first-layer G gradient was 7.0218e-05 at iteration 100 and first fell below 1% of that value at iteration 448, where it was zero. Samples remained high-frequency noise.
- Check performed: opened `logs/C1.csv` rows 100 and 448 and verified `viva/key_rows.csv`.
- Action taken: none; failure was the intended result.
- Outcome and evidence: `logs/C1.csv`, `figures/C1_curves.png`, `figures/C1_samples.png`.

## C2

- Planned settings: repeat C1 with only the generator loss changed to non-saturating.
- Observation: the generator gradient stayed around order 1 to 10 instead of collapsing, and recognizable digits were already visible at the matched iteration 448.
- Check performed: overlaid both first-layer gradient traces and compared the same fixed noise at iteration 448.
- Action taken: changed only the stated one-line loss expression.
- Outcome and evidence: `logs/C2.csv`, `figures/C2_overlay.png`.

## C3

- Planned settings: zdim 2, no generator BatchNorm, five G steps per D step, lr_G 2e-3.
- Observation: complete mode collapse occurred: all 5,000 samples were classified as digit 3. Modes covered = 1; reverse KL = 1.79176.
- Check performed: inspected the final grid and `logs/C3_counts.csv`.
- Action taken: none; the prescribed failure setting already produced collapse.
- Outcome and evidence: `figures/C3_samples.png`, `figures/C3_hist.png`, `logs/C3_counts.csv`.

## D1

- Planned settings: DCGAN, one D and one G update, BatchNorm in both networks, Adam 2e-4, 5,000 iterations.
- Observation: fixed-noise outputs changed from noise to recognizable, diverse digits. All six modes were covered; reverse KL = 0.05278.
- Check performed: inspected early/one-third/two-thirds/final snapshots and the 5,000-sample histogram.
- Action taken: none.
- Outcome and evidence: `figures/D1_progress.png`, `figures/D1_hist.png`, `logs/D1_counts.csv`.

## D2

- Planned settings: WGAN-GP, five critic steps, lambda 10, Adam 1e-4, 5,000 iterations.
- Observation: all six modes were covered; reverse KL improved to 0.01980. FID improved from D1's 39.700 to 17.117 and IS improved from 4.477 to 4.619.
- Check performed: compared fixed-noise progression, counts, IS, and FID against D1.
- Action taken: none.
- Outcome and evidence: `figures/D2_progress.png`, `figures/D2_hist.png`, `logs/D2_counts.csv`, `logs/final_model_comparison.csv`.

## Part E

- Planned settings: 5,000 samples per set, 10 IS splits, classifier-feature FID, real-vs-real floor, fixed-image noise test.
- Observation: real/C1/C3/D1/D2 FIDs were 1.399/941.881/821.241/39.700/17.117. The FID floor was 1.2009. Noise FID rose monotonically from approximately 0 at sigma 0 to 543.036 at sigma 1.
- Check performed: verified `E_summary.csv`, split scores, and the five noise rows; no FID epsilon retry was needed.
- Action taken: none.
- Outcome and evidence: `logs/E_summary.csv`, `logs/E1_split_scores.csv`, `logs/E3_noise_fid.csv`, `figures/E3_noise_fid.png`.
