"""Small terminal quiz using the exact saved-run facts."""

import random


CARDS = [
    ("Roll-derived values?", "R=27, seed=1327, held-out=7, digits [0,2,3,6,7,9], Blond_Hair."),
    ("AE/VAE validation MSE?", "AE 0.0066048581; VAE 0.0083013152; gap 0.0016964571."),
    ("VAE reparameterization?", "z = mu + exp(0.5*logvar)*epsilon."),
    ("VAE KL?", "0.5*sum(exp(logvar)+mu^2-1-logvar)."),
    ("Denoising PSNR?", "13.3204 to 19.4447 dB, gain about 6.124 dB."),
    ("Saturating derivative?", "-D(G(z)) with respect to the fake logit."),
    ("Non-saturating derivative?", "-(1-D(G(z))) with respect to the fake logit."),
    ("C1 death calculation?", "At 100: 7.0218186e-05; 1%=7.0218186e-07; first crossing 448."),
    ("C3 result?", "All 5000 assigned digit 3; one mode; reverse KL ln(6)=1.791759."),
    ("Coverage threshold?", "At least 1%, therefore at least 50 of 5000 samples."),
    ("D1 headline metrics?", "6 modes, reverse KL .052779, IS 4.4772, FID 39.700."),
    ("D2 headline metrics?", "6 modes, reverse KL .019803, IS 4.6190, FID 17.117."),
    ("WGAN-GP critic loss?", "mean C(fake)-mean C(real)+10*GP."),
    ("Why no critic sigmoid?", "It outputs unrestricted Wasserstein critic scores, not probabilities."),
    ("IS formula?", "exp(mean KL(p(y|x)||p(y)))."),
    ("FID feature/reference?", "128-D classifier features against 5000 real training images."),
    ("FID floor?", "1.200874 from two disjoint real test halves."),
    ("Why complex sqrtm?", "Nonsymmetric covariance product plus floating-point/singular effects."),
    ("Seed caveat?", "Documented offsets are reproducible but do not literally reset 1327 for every run."),
    ("Missing handout items?", "A4, B2, and Part F are referenced but not defined."),
]


def main():
    cards = CARDS[:]
    random.shuffle(cards)
    score = 0
    for i, (question, answer) in enumerate(cards, 1):
        input(f"\n{i}/{len(cards)}  {question}\nPress Enter to reveal...")
        print("Answer:", answer)
        result = input("Did you answer fully? [y/N] ").strip().lower()
        score += result == "y"
    print(f"\nSelf-score: {score}/{len(cards)}")


if __name__ == "__main__":
    main()
