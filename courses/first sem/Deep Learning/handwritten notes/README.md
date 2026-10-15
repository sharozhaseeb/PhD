# Deep Learning handwritten exam notes

36 new handwritten PNG pages covering all five available lecture decks, with the backpropagation handout reconciled into the derivations. Plan and every selected PNG cleared by an independent reviewer and checked by root. Built with imagegen in two phases:11 pages for Lectures1–2, then25 for Lectures3–5.

Read in the order below. Numerical examples are original practice unless labelled otherwise. Cover the boxed answer and reproduce the formula, substitution, intermediate values and interpretation. All logs are natural unless stated. These concise revision notes accompany the lecture slides and existing numerical-practice guide.

[Page-by-page plan](plan.md) · [Reference attributes](reference-attributes.md) · [Source audit](source-audit.md) · [Review evidence](review-log.md) · [Generation prompts](generation-prompts.md) · [Exact content manifest](page-manifest.json) · [Numerical checks](numerical-checks.json)

[Download all36 approved pages and supporting documents](../DL-handwritten-notes.zip)

## Lecture 1 — Introduction and linear regression

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| DL1-01 | [What learning means: tasks, data and generalization](dl1-01-what-learning-means-tasks-data-and-generalization.png) | 7–29 |
| DL1-02 | [Linear regression: loss, derivatives and one update](dl1-02-linear-regression-loss-derivatives-and-one-update.png) | 30–41 |
| DL1-03 | [Multiple features: two simultaneous batch updates](dl1-03-multiple-features-two-simultaneous-batch-updates.png) | 42–44 |

## Lecture 2 — Logistic regression and network representation

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| DL2-01 | [Logistic regression: probability, boundary and BCE](dl2-01-logistic-regression-probability-boundary-and-bce.png) | 4–26 |
| DL2-02 | [Logistic gradients: chain rule and batch averaging](dl2-02-logistic-gradients-chain-rule-and-batch-averaging-v2.png) | 27–31 |
| DL2-03 | [Neurons and depth: shapes, parameters and nonlinearities](dl2-03-neurons-and-depth-shapes-parameters-and-nonlinearities.png) | 32–53 |
| DL2-04 | [Threshold gates and two XOR constructions](dl2-04-threshold-gates-and-two-xor-constructions.png) | 54–58, 83 |
| DL2-05 | [Boolean networks: minterms, negative literals and K-maps](dl2-05-boolean-networks-minterms-negative-literals-and-k-maps.png) | 59–75 |
| DL2-06 | [Parity and depth: compare specified constructions](dl2-06-parity-and-depth-compare-specified-constructions.png) | 76–98 |
| DL2-07 | [Classification regions: half-spaces, intersections and unions](dl2-07-classification-regions-half-spaces-intersections-and-unions.png) | 99–113 |
| DL2-08 | [Function approximation: pulses, sums and the theorem](dl2-08-function-approximation-pulses-sums-and-the-theorem.png) | 114–119 |

## Lecture 3 — Learning and backpropagation

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| DL3-01 | [Perceptron learning: ordered updates](dl3-01-perceptron-ordered-updates.png) | 30–78 |
| DL3-02 | [Activations: outputs, slopes and probability](dl3-02-activations-outputs-and-slopes.png) | 73–100,154–156 |
| DL3-03 | [Learning from samples: empirical risk](dl3-03-expected-and-empirical-risk-v2.png) | 19–29,101–110 |
| DL3-04 | [Calculus for learning: gradients and path sums](dl3-04-gradients-hessian-and-path-sums.png) | 111–145,167–180 |
| DL3-05 | [A complete 2 → 2 → 1 forward pass](dl3-05-complete-forward-pass.png) | 157–162,182–200; handout1–2 |
| DL3-06 | [Output backprop: chain rule to a weight](dl3-06-output-backprop-chain-rule.png) | 201–227; handout2–3 |
| DL3-07 | [Hidden backprop and simultaneous updates](dl3-07-hidden-backprop-simultaneous-update.png) | 228–243; handout3 |
| DL3-08 | [Batch training: average once, then update](dl3-08-batch-averaging-and-training-loop.png) | 163–166,242–245; handout1–3 |

## Lecture 4 — Neural network optimization

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| DL4-01 | [Loss and saturation: why the surrogate matters](dl4-01-loss-and-saturation-why-the-surrogate-matters.png) | 1–30 |
| DL4-02 | [Scalar convergence: step size, oscillation and rate](dl4-02-scalar-convergence-step-size-oscillation-and-rate.png) | 31–36 |
| DL4-03 | [Hessian geometry: ill-conditioning and Newton steps](dl4-03-hessian-geometry-ill-conditioning-and-newton-steps.png) | 37–53 |
| DL4-04 | [Curvature approximations and learning-rate schedules](dl4-04-curvature-approximations-and-learning-rate-schedules.png) | 53–60 |
| DL4-05 | [RProp: sign-based steps with rollback](dl4-05-rprop-sign-based-steps-with-rollback.png) | 61–74 |
| DL4-06 | [Momentum: accumulate consistent descent directions](dl4-06-momentum-accumulate-consistent-descent-directions.png) | 75–85 |
| DL4-07 | [Nesterov momentum: compute the gradient after lookahead](dl4-07-nesterov-momentum-compute-the-gradient-after-lookahead.png) | 86–94 |

## Lecture 5 — Stochastic optimization and generalization

| Page | Handwritten PNG | Source PDF pages |
| --- | --- | --- |
| DL5-01 | [Batch, SGD and mini-batches: order and update counts](dl5-01-batch-sgd-and-mini-batches-order-and-update-counts.png) | 1–55, 77–82 |
| DL5-02 | [SGD convergence: step-size conditions and fair comparisons](dl5-02-sgd-convergence-step-size-conditions-and-fair-comparisons.png) | 53–59, 86, 91 |
| DL5-03 | [Mini-batch estimates: unbiasedness, variance and monitoring](dl5-03-mini-batch-estimates-unbiasedness-variance-and-monitoring.png) | 60–91 |
| DL5-04 | [Mini-batch momentum and Nesterov: preserve the state](dl5-04-mini-batch-momentum-and-nesterov-preserve-the-state.png) | 93–109 |
| DL5-05 | [RMSProp: squared gradients set a coordinate scale](dl5-05-rmsprop-squared-gradients-set-a-coordinate-scale.png) | 110–118 |
| DL5-06 | [Adam: moments, bias correction and two updates](dl5-06-adam-moments-bias-correction-and-two-updates-v2.png) | 119–124 |
| DL5-07 | [Generalization and L2: objective, gradient and decay](dl5-07-generalization-and-l2-objective-gradient-and-decay.png) | 125–144 |
| DL5-08 | [Dropout: masked learning and both scaling conventions](dl5-08-dropout-masked-learning-and-both-scaling-conventions.png) | 145–158 |
| DL5-09 | [Gradient clipping: coordinate limits versus norm limits](dl5-09-gradient-clipping-coordinate-limits-versus-norm-limits.png) | 161 |
| DL5-10 | [Practical training: normalization, initialization and model selection](dl5-10-practical-training-normalization-initialization-and-model-selection.png) | 143, 159–160, 162–165 |

The three original reference images are retained in this folder. Superseded generated drafts are isolated in review-history/ and excluded from the study index and bundle. Selected refinements use -v2.png.
