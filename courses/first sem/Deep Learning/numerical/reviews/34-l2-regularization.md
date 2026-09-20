# Lesson34 — L2 regularization and weight decay

## Plan discussion — approved

Use mean half-squared data loss plus lambda/2 times the sum of selected weight squares; explicitly exclude biases for this exercise and do not divide the penalty again by batch size. Work main and fresh examples through prediction, residual, both objective terms, every data/penalty/total derivative, simultaneous update and recomputed total objective.

TA conditions: preserve lambda as the objective coefficient; derive shrink factor1-eta*lambda and explain source138's boxed1-lambda only with a separately named decay coefficient or as the missing learning-rate factor. Explain why total data-plus-penalty update can increase a weight despite penalty-only shrinkage. Define matrix Frobenius squared norm as sum of entries squared. The sigmoid smoothness derivative is with respect to input x, not the training parameter; restrict its interpretation to the illustrated scalar neuron. Distinguish Adam with an L2 gradient from decoupled decay. Full rendered review pending.

## Final TA verdict — PASS

Visually reviewed all19 pages and actual source images133,137,138. Layout, plot labels, substituted arithmetic and independent practice are readable, with no unresolved findings.

Independent central finite differences checked all three total-objective derivatives in both problems within1e-8. Main gradient(-.8,-.9,-.5) updates parameters to(1.08,-1.91,.55) and objective.625 to.50145. Fresh gradient(1.2,2.1,1) gives(1.88,.79,-1.1) and objective.75 to.272725. Both alternative shrink-factor updates agree. Sigmoid input slopes at zero are.125 and1.25.

Source fidelity/student checks: mean data term and once-only weight penalty are separated, Frobenius norm explained, unpenalized bias policy declared, negative-weight derivatives retain their sign, and simultaneous updates use the old residual. The source138 boxed-factor discrepancy is explicitly reconciled using separate per-step decay d=eta*lambda, retaining the original objective lambda. Total updates may increase a weight despite penalty-only shrinkage. The input-sensitivity illustration is separated from parameter gradients and is not generalized to all deep networks. Adam L2-gradient and decoupled decay distinction is explicit. Ready for Lesson35 plan.
