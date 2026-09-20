# Lesson35 — Dropout

## Plan discussion — approved

Use a seven-parameter two-hidden-ReLU network to work standard dropout forward, every parameter derivative, simultaneous update and a fixed-mask diagnostic re-forward. Explicitly map course alpha to keep probability q. Then reset original parameters for standard inference, inverted-dropout comparison and mask ensemble enumeration. Fresh opposite-mask practice must have full gradient/update/re-forward answers.

TA conditions: use the same cached mask during a forward/backward pair; explain later training masks are resampled according to the stated policy, while the post-update fixed-mask calculation is diagnostic. Mask hidden activations only; do not directly mask bias constants, and count each bias once. A dropped hidden unit's incoming bias gradient can nevertheless be zero through its masked path. Inference uses either activation scaling or outgoing-weight scaling, never both. Distinguish standard/inverted conventions and reset original parameters explicitly for comparisons. Independent Bernoulli masks justify probabilities/counts. Linear-output expectation equality is limited to that example; include the nonlinear counterexample supporting the lecture's approximate model-averaging statement. Full rendered review pending.

## Final TA verdict — PASS

Visually reviewed all30 pages and actual source153–156. Rechecked07,08,17 after negative-zero and subtitle-spacing fixes; the latest16,24,25,26 already showed corrected zero gradients. No unresolved layout or numerical findings.

Independent fixed-mask central differences checked all seven parameters for main standard dropout, inverted comparison and fresh opposite-mask practice (21 checks, tolerance1e-7). Main gradient(16.5,0,16.5,0,11,0,5.5) gives diagnostic loss15.125 to9.122001845. Inverted gradient(69,0,69,0,46,0,11.5) matches its distinct scaling. Fresh gradient(0,5,0,5,0,-2.5,-2.5) gives3.125 to2.536878125. Four-mask output enumeration(.5,-1.5,6.5,4.5) averages2.5; sigmoid nonlinear counterexample gives.690398539 versus.731058579. Three-unit ordered-mask probability.128 and expected active count2.4 are correct.

Student/source checks: linear output and half-squared loss are declared before predictions exceeding1. Same mask is cached for forward/backward; later sampling and diagnostic fixed-mask re-forward are distinguished. Input/output/bias eligibility is explicit, and a hidden bias can have zero derivative through a dropped path without directly masking its constant. Every inference/comparison resets original parameters; standard scaling and inverted scaling remain separate, without double scaling or bias scaling. The exact linear expectation is not generalized to nonlinear networks; masks share parameters and are not independently trained models. Ready for Lesson36 plan.
