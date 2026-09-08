# Applied Information Security — Lecture 1–3 Support Guide

This maps the instructor's lattice-cryptography notes to high-quality explanations. Study in order because each lecture depends on the previous one.

## Official notes

- [Instructor's lattice lecture notes](https://github.com/faisal-aslam/Lecture_Notes/tree/main/lattices)
- Quiz scope assumed here: **Lectures 1, 2, and 3**.

## Lecture 1 — Mathematical foundations and lattices

### Sets, groups, rings, and fields

Study:

- Sets, binary operations, closure, associativity, identity, and inverses
- Groups, Abelian groups, subgroups, cosets, and quotient groups
- Rings, commutative rings, units, zero divisors, integral domains, and fields
- Why `Z_p` is a field for prime `p`, but `Z_n` is generally not a field for composite `n`

Watch:

- [Socratica — What is Abstract Algebra?](https://www.youtube.com/watch?v=IP7nW_hKB7I)
- [Socratica — Group Definition](https://www.youtube.com/watch?v=g7L_r6zw4-c)
- [Socratica — Subgroup Definition](https://www.youtube.com/watch?v=TJAQNlGvfjE)
- [Socratica — Cosets and Quotient Groups](https://www.youtube.com/watch?v=vYKdh5oQ4Zw)
- [Socratica — Ring Definition](https://www.youtube.com/watch?v=j_f7O-4Rb9U)
- [Socratica — Field Definition](https://www.youtube.com/watch?v=KCSZ4QhOw0I)
- [RareSkills — Modular Arithmetic and Finite Fields](https://www.youtube.com/watch?v=0lEwgX_zKqE)

### Modular arithmetic and number theory

Study:

- Congruence modulo `n`, modular addition, and modular multiplication
- `gcd`, the Euclidean algorithm, and Extended Euclidean Algorithm (EEA)
- An element `a` is invertible modulo `n` exactly when `gcd(a,n)=1`
- Euler's totient `phi(n)` and the group of units modulo `n`
- Finding a modular inverse with EEA

Watch:

- [Christof Paar — Number Theory, EEA, and Euler's Phi Function](https://www.youtube.com/watch?v=fq6SXByItUI)

### Vector spaces and linear algebra

Study:

- Vector spaces over a field
- Linear combinations, span, linear dependence, and independence
- Basis, coordinates relative to a basis, and dimension
- Row operations, row-echelon form, pivots, and rank
- Inner product/dot product
- Norm: `||v|| = sqrt(<v,v>)`
- Unit vector: `v / ||v||`
- Orthogonal versus orthonormal vectors and bases
- Projection and Gram–Schmidt orthogonalization

Watch:

- [3Blue1Brown — Essence of Linear Algebra playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- [3Blue1Brown — Linear Combinations, Span, and Basis](https://www.youtube.com/watch?v=k7RM-ot2NWY)
- [3Blue1Brown — Dot Products and Duality](https://www.youtube.com/watch?v=LyGKycYT2v0)
- [MIT 18.06 — Gram–Schmidt Orthogonalization](https://www.youtube.com/watch?v=TRktLuAktBQ)
- [MIT OCW / Gilbert Strang — Elimination with Matrices](https://www.youtube.com/watch?v=QVKj3LADCnA)
- [Jeffrey Chasnov — Reduced Row-Echelon Form](https://www.youtube.com/watch?v=1rBU0yIyQQ8)
- [MIT 18.06 — Linear Algebra topic index](https://www.mit.edu/~18.06/)

### Lattices, bases, and geometry

Study:

- Discrete sets and a lattice as a discrete additive subgroup
- Integer combinations of independent lattice-basis vectors
- Rank, ambient dimension, full-rank, and lower-rank lattices
- Why one lattice has infinitely many bases
- Good basis: short and nearly orthogonal; bad basis: long and highly skewed
- Fundamental parallelepiped/domain
- Lattice determinant/covolume
- Unimodular matrices and equivalent lattice bases
- The first successive minimum `lambda_1(L)`
- SVP, approximate/Gap-SVP, CVP, and approximate/Gap-CVP
- Minkowski's First Theorem and the Blichfeldt-lemma proof idea
- LLL reduction: Gram–Schmidt coefficients, size reduction, Lovász condition, and guarantees
- BKZ as a stronger blockwise reduction method

Watch:

- [Chalk Talk — Lattice Cryptography: The Tricky Math of Dots](https://www.youtube.com/watch?v=QDdOoYdb748)
- [Alfred Menezes — Lattices](https://www.youtube.com/watch?v=zPa1h-gj8_A)
- [Alfred Menezes — SIS, LWE, and Lattices](https://www.youtube.com/watch?v=5QdJJWS7Umw)
- [Alfred Menezes — complete Lattice-Based Cryptography playlist](https://www.youtube.com/playlist?list=PLA1qgQLL41STNFDvPJRqrHtuz0PIEJ4a8)
- [Menezes Basis Reduction V1 — Introduction to Lattices](https://www.youtube.com/watch?v=hMUvgL0hyhg)
- [Menezes Basis Reduction V2 — Gram–Schmidt](https://www.youtube.com/watch?v=hM-NCf6B49M)
- [Menezes Basis Reduction — LLL](https://www.youtube.com/watch?v=Upg1l88Zlck)
- [Menezes Basis Reduction V6 — LLL Improvements and BKZ](https://www.youtube.com/watch?v=_oaXKSH8a5Q)
- [Lattices and Minkowski's Theorem](https://www.youtube.com/watch?v=PWhUkxrJaxo) — the first 25 minutes are the relevant theorem/proof material
- [Menezes Lattice Basis Reduction course page](https://cryptography101.ca/lattice-basis-reduction/) — use its corrected slides

The videos provide intuition; use the instructor's exact statements and constants for Minkowski, Blichfeldt, LLL, and BKZ.

## Lecture 2 — Cryptographic foundations, SIS, and LWE

### Symmetric/public-key cryptography and one-way functions

Study:

- Symmetric versus asymmetric encryption and the key-distribution problem
- Public/private keys, encryption, signatures, and key establishment
- Hybrid encryption: asymmetric setup followed by fast symmetric protection
- One-way functions: easy forward computation but hard inversion
- Factoring (RSA) and discrete logarithms (Diffie–Hellman/ECC)
- What RSA, ECC, and lattice cryptography offer
- Why quantum algorithms threaten RSA and ECC
- Worst-case versus average-case hardness and cryptographic trapdoors

Watch:

- [Alfred Menezes — Lattice-Based Cryptography: Introduction](https://www.youtube.com/watch?v=SsKfGn1YKlg)
- [Chalk Talk — Post-Quantum Cryptography after Shor's Algorithm](https://www.youtube.com/watch?v=_C5dkUiiQnw)
- [Christof Paar — RSA](https://www.youtube.com/watch?v=QSlWzKNbKrU)
- [Christof Paar — Diffie–Hellman and the Discrete Logarithm Problem](https://www.youtube.com/watch?v=aeOzBCbwxUo)
- [Christof Paar — Introduction to Elliptic Curves](https://www.youtube.com/watch?v=vnpZXJL6QCQ)
- [Christof Paar — Elliptic-Curve Cryptography](https://www.youtube.com/watch?v=zTt4gvuQ6sY)

### SIS

Study:

- Given `A` over `Z_q`, find a **nonzero short integer vector** `z` with `Az = 0 mod q`
- Meaning of parameters `n`, `m`, `q`, and bound `beta`
- Why the zero vector is excluded and why shortness matters
- SIS-based collision-resistant hashes and why a collision yields an SIS solution
- Connection between average SIS instances and worst-case lattice problems

Watch:

- [Alfred Menezes — SIS](https://www.youtube.com/watch?v=Mmqwedn__os)
- [Alfred Menezes — SIS, LWE, and Lattices](https://www.youtube.com/watch?v=5QdJJWS7Umw)

### LWE

Study:

- Samples `(a_i,b_i)` where `b_i = <a_i,s> + e_i mod q`
- Why noiseless linear equations are easy and small random errors make recovery hard
- Search-LWE versus Decision-LWE
- Error distribution `chi`, discrete Gaussians, and centered binomial distributions
- Roles of dimension, modulus, sample count, and error size
- LWE as noisy/bounded-distance decoding
- Regev's worst-case-to-average-case reduction at a conceptual level
- Work through the notes' numeric examples by hand

Watch:

- [Chalk Talk — Learning With Errors: The Unsolvable Equations](https://www.youtube.com/watch?v=K026C5YaB3A)
- [Alfred Menezes — LWE](https://www.youtube.com/watch?v=M1cq7cuonbI)
- [Alfred Menezes — SIS, LWE, and Lattices](https://www.youtube.com/watch?v=5QdJJWS7Umw)

### Ring-LWE and Module-LWE

Study:

- Why plain LWE has large keys/matrices
- Polynomial quotient ring `R_q = Z_q[x]/(x^n + 1)`
- Polynomial addition and negacyclic multiplication
- Ring-LWE samples
- Module-LWE: vectors/matrices over the polynomial ring
- Module rank `k` and the structure/efficiency trade-off
- Why Kyber/ML-KEM uses Module-LWE

Watch:

- [Alfred Menezes — Ring-SIS and Ring-LWE](https://www.youtube.com/watch?v=Y5yHl0vvF7c)
- [Alfred Menezes — Module-SIS and Module-LWE](https://www.youtube.com/watch?v=iCgX3HWTrjM)

## Lecture 3 — Kyber / ML-KEM

### Parameters, notation, and object shapes

Study:

- `R_q = Z_q[x]/(x^256 + 1)`, `n=256`, and `q=3329`
- Module rank `k=2,3,4` depending on the parameter set
- Noise parameters `eta_1` and `eta_2`
- Shapes of scalars, polynomials, polynomial vectors, and polynomial matrices
- Transpose and inner products over `R_q`
- Centered modular representatives
- Expanding public matrix `A` from a seed
- Centered-binomial sampling of secrets and errors

Watch:

- [Alfred Menezes — Kyber/Dilithium Mathematical Prerequisites](https://www.youtube.com/watch?v=h5pfTIE6slU)
- [Menezes course page — slides, videos, and corrections](https://cryptography101.ca/kyber-dilithium/)

### Compression, decompression, and encoding

Study:

- Why coefficients are compressed
- Conceptual `Compress_q(x,d)` and `Decompress_q(y,d)`
- Controlled rounding error from compression
- Encoding a bit near `0` or `q/2` and decoding by proximity
- Why total error must stay inside the decoding region

Watch:

- [Alfred Menezes — Simplified Kyber-PKE](https://www.youtube.com/watch?v=nlGjqGdkmfI)
- [Alfred Menezes — Kyber Optimizations](https://www.youtube.com/watch?v=vhbpAG1RMbI)

### Kyber.CPAPKE encryption core

Know these equations and the shape/role of every term:

- KeyGen: `t = A s + e`
- Encrypt: `u = A^T r + e_1`
- Encrypt: `v = t^T r + e_2 + Encode(m)`
- Decrypt from: `v - s^T u`

Study:

- Public, secret, ephemeral, and error values
- Fresh ephemeral secret `r`
- Decryption cancellation
- Residual noise: `epsilon = e^T r + e_2 - s^T e_1`
- Noise budget and rough correctness condition `|epsilon| < q/4`
- Both worked examples in the notes (`k=1` and `k=2`)

Watch:

- [Alfred Menezes — Simplified Kyber-PKE](https://www.youtube.com/watch?v=nlGjqGdkmfI)
- [Alfred Menezes — Full Kyber-PKE](https://www.youtube.com/watch?v=ESmQhPeWeAA)

### CPA to CCA security and KEMs

Study:

- PKE versus KEM; encapsulation versus decapsulation
- IND-CPA versus IND-CCA security
- Why active chosen-ciphertext attacks require stronger protection
- Fujisaki–Okamoto transform
- Deterministically deriving coins from the message and public-key hash
- Re-encryption check during decapsulation
- Implicit rejection/fallback secret
- Constant-time failure handling
- Hybrid deployment: ML-KEM establishes a shared secret, symmetric crypto protects data

Watch:

- [Alfred Menezes — Kyber-KEM](https://www.youtube.com/watch?v=srCXNBWsCkA)
- [Complete Kyber and Dilithium playlist](https://www.youtube.com/playlist?list=PLA1qgQLL41SSUOHlq8ADraKKzv47v2yrF)

### Lower-priority implementation material

Study if your lecturer emphasizes implementation:

- NTT for efficient polynomial multiplication
- Serialization and packing
- Constant-time code and side-channel awareness

Watch:

- [Alfred Menezes — Kyber NTT](https://www.youtube.com/watch?v=pgNZFA3yj7M)

## Recommended watch order

1. Socratica: abstract algebra → groups → cosets → rings.
2. RareSkills and Paar: modular arithmetic → EEA/Euler phi.
3. 3Blue1Brown: span/basis → dot products; then MIT Gram–Schmidt.
4. Chalk Talk: post-quantum overview → lattice dots → LWE.
5. Menezes lattice series: Introduction → Lattices → SIS → LWE → lattice connection → Ring → Module.
6. Menezes basis-reduction sequence: lattice foundations → Gram–Schmidt → LLL → BKZ; add the first 25 minutes of the Minkowski lecture.
7. Menezes Kyber series: prerequisites → simplified PKE → optimizations → full PKE → KEM.
8. Watch NTT only after the core scheme is clear or if it is explicitly examined.

## What you must be able to do without notes

### Lecture 1

- State definitions of group, ring, field, vector space, basis, lattice, and determinant.
- Find a modular inverse using EEA.
- Test independence with row reduction.
- Compute a dot product, norm, unit vector, projection, and Gram–Schmidt step.
- Distinguish orthogonal from orthonormal.
- Generate lattice points, calculate a 2D determinant, and compare good/bad bases.
- Explain equivalent bases, SVP/CVP, Minkowski's idea, and LLL's purpose.

### Lecture 2

- Compare symmetric crypto, RSA, ECC, and lattice crypto.
- Explain a one-way function using factoring and DLP examples.
- Distinguish exact/approximate and search/decision problems.
- Write and explain the SIS and LWE conditions.
- Explain why LWE error is small but essential.
- Explain LWE → Ring-LWE → Module-LWE and worst-case → average-case hardness.

### Lecture 3

- Recall `n=256`, `q=3329`, and module rank `k`.
- Track all matrix/vector/polynomial shapes.
- Write KeyGen, Encrypt, and Decrypt equations from memory.
- Expand `v-s^T u` and derive the residual noise.
- Explain compression, encoding, noise budget, and correctness.
- Compare CPA and CCA; explain FO re-encryption and implicit rejection.
- Explain how a KEM is used with symmetric encryption.

## Common traps

- A vector-space basis permits coefficients from its field; a lattice basis permits **integer** coefficients.
- Orthogonal vectors need not have length one; orthonormal vectors do.
- A bad lattice basis does not create a different lattice if the change is unimodular.
- `det(L)` measures fundamental volume, not the length of its shortest vector.
- LWE error is small and sampled from a specified distribution, not arbitrary corruption.
- Kyber's cancellation does not remove every error term; decoding succeeds only inside the noise budget.
- ML-KEM establishes a shared key; it does not directly encrypt bulk application data.
- Videos may use different row/column conventions—follow the instructor's notation on the quiz.

## Independent coverage audit

A second-agent audit compared the official Lecture 1–3 headings with every video above. It found and filled these previously weak areas:

- Subgroups
- Zero divisors, integral domains, and field axioms
- Elimination, REF/RREF, pivots, and rank
- Unimodular lattice-basis changes and determinant/covolume
- Detailed LLL and BKZ
- Minkowski's First Theorem and its Blichfeldt-style proof
- The introductory connection among post-quantum cryptography, SIS, and LWE

Lecture 3 needs no additional video source. Its main remaining work is active practice: track the shapes of `A,s,e,t,u,v`, derive the residual noise, apply the `<q/4` correctness condition, and solve the notes' `k=1` and `k=2` examples by hand.

Where a Menezes course page publishes corrections or errata, use its corrected slides rather than copying a formula directly from the recording.

## Active-study method

For every topic:

1. Watch for intuition.
2. Read the matching instructor section.
3. Write the definition and main equation from memory.
4. Solve one small example by hand.
5. Explain it aloud in 60 seconds.
6. Attempt the lecture exercises and revisit only the video segment related to each mistake.
