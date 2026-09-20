# Lesson 30 — Stochastic convergence and batch variance

## Plan discussion — approved

Cover the lecture's step-size summability conditions, stipulated convergence-bound arithmetic and equal-example-work comparison, then frozen-parameter gradient variance and independent mini-batch averaging. Full fresh practice changes exponents, bounds, budget and gradient distribution.

TA conditions: define infinite sums, objective gap, variance and standard deviation concretely. Derive 1/2<p<=1 with endpoint cases and retain theorem assumptions; do not assert universal neural-network convergence. Explain inequality reversal for a negative logarithm. State the illustrative rate expression and selected constants before M=bk substitution; distinguish a stipulated bound from actual runtime/performance. Define independent draws and frozen parameters before variance reduction. Without-replacement variance must use the same population convention. Final review pending.

## Final TA verdict — PASS

All 24 rendered pages reviewed; revised page 14 covariance explanation rechecked. Actual Lecture5 PDF pages 56 and 86 were visually inspected. The lesson preserves the course sums/rate expression while clearly adding assumptions and explaining why neither a universal nonconvex-minimum guarantee nor a blanket square-root-b equal-work degradation follows from those formulas alone.

Independent checks: exact-fraction geometric totals 9c and 81c^2/19; logarithmic boundary checks yield 24 and 7 updates; inverse bounds yield 200 and 100; equal-work expressions yield 0.0125, 0.02 and 0.035. Enumeration of all four main pair outcomes gives mean 2, variance 1/2; all 16 fresh four-draw outcomes give counts (1,4,6,4,1), mean 2 and variance 1. The finite-population correction agrees with selecting the full fixed dataset.

Student review: D is consistently a sampled per-example loss throughout (not silently changed to a gradient), with frozen parameters, independence, probability weights, variance and standard deviation explicit. The pair enumeration precedes the general variance formula. Covariance is now explained in plain language. Fresh practice has complete separate answers. No clipping or unresolved findings.
