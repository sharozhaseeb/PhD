# Last-minute flashcards

| Prompt | Answer |
|---|---|
| Base facts? | R27, seed1327, held-out7, digits 0/2/3/6/7/9, Blond_Hair |
| Main run? | 20L-11327_main_v1 |
| AE/VAE setup? | latent64, Adam1e-3, batch64, 10 epochs, 27k/3k |
| AE/VAE val MSE? | .006605 / .008301; gap .001696 |
| Reparameterization? | z=mu+exp(.5 logvar)*epsilon |
| KL? | .5 sum(exp(logvar)+mu^2-1-logvar) |
| KL scaling? | divide by 3*64*64; beta remains 1 |
| PSNR? | 10 log10(1/MSE) for range 1 |
| PSNR result? | 13.3204 -> 19.4447 dB |
| Classifier accuracy? | 99.019% |
| Saturating derivative? | -D(fake) wrt fake logit |
| Non-saturating derivative? | -(1-D(fake)) |
| C1 reference? | iter100, 7.0218186e-05 |
| C1 threshold/death? | 7.0218186e-07; iter448, zero |
| C2 at 448? | first 3.83656, full 11.29571 |
| Gradient columns? | first G.fc parameter / all G parameters |
| C3 recipe? | z2, no G BN, 5G:1D, lrG.002, lrD.0002 |
| C3 result? | all digit3, 1 mode, ln6=1.791759 |
| Coverage threshold? | >=1% = >=50 of 5000 |
| D1? | 6 modes, RKL .052779, IS 4.4772, FID 39.700 |
| D2? | 6 modes, RKL .019803, IS 4.6190, FID 17.117 |
| WGAN critic loss? | E C(fake)-E C(real)+10 GP |
| WGAN G loss? | -E C(fake) |
| GP? | mean((norm grad_xhat C -1)^2) |
| Why no critic BN? | batch coupling conflicts with per-sample gradient constraint |
| IS? | exp(E KL(p(y|x)||p(y))) |
| Ideal six-class IS? | 6; collapsed/identical = 1 |
| FID features? | classifier penultimate, 128-D |
| FID reference? | 5000 real training images |
| Real IS/FID? | 5.7720 / 1.39865 |
| C1 IS/FID? | 1.0347 / 941.881 |
| C3 IS/FID? | 1.0006 / 821.241 |
| FID floor? | 1.200874, disjoint real test halves |
| Noise FID? | 0,14.144,100.552,326.750,543.036 |
| sqrtm complex? | nonsymmetric product + floating-point/singularity |
| Highest-risk honesty point? | offsets are reproducible but not literal seed1327 every run |
| Missing tasks? | A4, B2, Part F are referenced but undefined |
| Debug order? | curves -> shapes -> overfit ten -> architecture |
