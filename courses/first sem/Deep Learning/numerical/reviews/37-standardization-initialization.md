# Lesson 37 TA review

## Plan discussion — approved

Use training [2,4,6], population variance and its square-root SD, all z-score substitutions and direct mean/variance checks. Freeze training statistics for held-out data. Explain wrong variance denominator, declared constant-feature policy, and difference from pixel scaling and full batch normalization. Optional Xavier/He normal formulas must be labeled beyond the named-only source, with fan counts, activation assumptions and variance versus SD. Symmetry example must declare linear output, half-squared loss and which weights train. Briefly acknowledge source SVD initialization without inventing a course numerical algorithm. Fresh [1,4,7] and new fan counts receive full separate worked answers.

Final rendered review pending.

## Final TA verdict — PASS

Visually reviewed all 17 rendered pages and actual source Lecture 5 PDF 163 plus Assignment 1 page 4. Rechecked revised 08, 11 and 12: spacing, normal-distribution notation, residual definition and symmetry-gradient factors now clear. No remaining layout findings.

Independent NumPy arithmetic confirmed both training means, population variances, standard deviations, all standardized and held-out values, and Xavier/He variances, square-root scales and sampled weights. Main variance 8/3 and fresh variance 6 produce unit training variance under divisor N. The wrong-denominator example yields .375; constant-feature handling explicitly retains zero variance.

Student/source fidelity: training statistics are frozen for held-out inputs; population versus N-1 conventions, SD versus variance, pixel scaling and batch-normalization scope are separated. Initializer formulas are labeled optional normal variants beyond the source's named-only schemes, with fan counts and assumptions. SVD scope is acknowledged. Symmetry example fixes output weights and biases, declares trainable hidden weights and gives all gradient/update factors. Fresh practice is fully worked separately.
