# Deep Learning: visual worked-example roadmap

An ordered checklist for turning the material in Lectures 1–5, the backpropagation handout, and assignment support into readable visual lessons. Follow prerequisite order within each group. Open the [numerical collection](numerical/README.md) for lesson PDFs, illustrated notes, and current review status.

## Format for every lesson

- Show the exact lecture formula and its PDF page reference, then explain each symbol. If simpler symbols help, show their mapping to the notes.
- Use a small dataset or network. State all inputs, labels, starting parameters, and conventions.
- For every calculation: show the formula, substitute numbers, work through the arithmetic, and explain the result.
- Explain why the step is needed; distinguish a prediction, loss, gradient, and parameter update.
- Use typeset PDF pages and images embedded in Obsidian. Keep one main stage per page.
- Finish with a short independent practice question, its worked answer, and common mistakes.
- Check arithmetic and have an agent review student understanding; fix findings and review again.

Unchecked items are not yet complete. Items 4 and 5 are covered by the expanded logistic-regression lesson. Checkmarks require the final TA review to pass.

## 1. Foundations — Lecture 1

- [x] **1. Single-feature linear regression:** three (x, y) pairs; predictions, residuals, squared-error loss, and mean cost, using the lecture's scaling convention.
- [x] **2. Linear-regression gradient descent:** derive weight and bias gradients, substitute all three examples, average, update simultaneously, and recompute loss.
- [x] **3. Multiple-feature linear regression:** two inputs per example; expand the dot product; compute each weight gradient and the bias gradient; perform two updates. Connect to the homework.

## 2. Logistic regression — Lecture 2

- [x] **4. Single-feature logistic regression:** three points; sigmoid, binary cross-entropy, derivatives, mean gradients, simultaneous update, and new loss. [Open the visual lesson](Logistic%20regression%20-%20visual%20walkthrough.md).
- [x] **5. Align and extend the completed lesson:** add the notes-to-walkthrough symbol mapping and slide references; add an independent practice question with a worked answer.
- [x] **6. Multiple-feature logistic regression and decision boundaries:** expand the score, calculate probabilities and labels, and plot the boundary; show how adding a transformed feature changes its shape.
- [x] **7. Computation graphs and the chain rule:** work through the lecture's graph node by node; show forward values, local derivatives, and backward contributions, including a branching path.

## 3. What a network can represent — Lecture 2

- [x] **8. A neuron and logic gates:** weighted sum, bias, threshold convention; verify AND, OR, NOT, and majority on truth tables.
- [x] **9. XOR with a hidden layer:** evaluate every input pair through the hidden and output neurons; compare the architectures used in the notes.
- [x] **10. Truth table to Boolean network:** build terms, handle negated inputs, combine them, and verify every row; work through one Karnaugh-map simplification.
- [x] **11. Parity and depth versus width:** build small examples and count neurons and connections for the specified constructions.
- [x] **12. Geometric classification and function approximation:** calculate half-space tests, combine them into a region, then construct and add simple pulses.

## 4. Learning a neural network — Lecture 3 and the handout

- [x] **13. Perceptron learning:** process examples in a stated order, identify mistakes, update parameters, and repeat an epoch.
- [x] **14. Activation functions and derivatives:** calculate sigmoid, tanh, ReLU, and the other activations shown in the notes at selected inputs; explain saturation and the convention at a kink.
- [x] **15. Loss and risk:** distinguish one-example loss, empirical mean loss, and expected loss using a tiny dataset and a simple probability table.
- [x] **16. Network shapes and parameter counts:** label every weight matrix, bias, input, and output; expand a small matrix multiplication into scalar sums.
- [x] **17. Full network forward pass:** calculate every hidden activation and output, then the loss, using a small network with fixed numbers.
- [x] **18. Output-layer backpropagation:** compute output errors and every output weight and bias gradient using the same network.
- [x] **19. Hidden-layer backpropagation:** trace contributions backward, sum paths correctly, and calculate all hidden weight and bias gradients.
- [x] **20. A complete batch training step:** use two examples, average gradients once, update all parameters together, and check the new loss; finish with a fresh full-network practice problem.

## 5. Optimization — Lectures 3–4

- [x] **21. Gradient, Hessian, and stationary points:** differentiate small functions; classify minima, maxima, and saddles; connect curvature to directions of movement.
- [x] **22. Learning rate and convergence:** compare small, oscillating, and diverging steps on a quadratic; distinguish parameter error from loss and calculate convergence rates.
- [x] **23. Saturation and choice of loss:** compare sigmoid with squared error and with cross-entropy using the same predictions and labels.
- [x] **24. Newton's method:** compute gradient, Hessian, inverse or linear solve, and parameter update; compare with gradient descent from the same point.
- [x] **25. Learning-rate schedules:** substitute iteration numbers into the lecture's decay formulas, checking indexing carefully.
- [x] **26. RProp:** track signs, individual step sizes, accepted or rejected moves, and the state carried to the next step.
- [x] **27. Momentum and Nesterov:** calculate at least two steps side by side; label velocity, look-ahead point, gradient location, and sign convention.
- [x] **28. Curvature approximations — conceptual companion:** explain BFGS, L-BFGS, and Levenberg–Marquardt visually. Add numerical calculations only for formulas actually supplied in the lecture, clearly separating any optional extension.

## 6. Stochastic and adaptive optimization — Lecture 5

- [x] **29. Batch, SGD, and mini-batch updates:** run the same small dataset through each method; show order effects, epochs, batches, and number of updates.
- [x] **30. SGD rates and batch variance:** work through the notes' step-size conditions, rate calculations, equal-work comparisons, and variance of a batch mean, stating assumptions.
- [x] **31. Momentum with changing mini-batches:** carry optimizer state across different batches and compare ordinary momentum with Nesterov.
- [x] **32. RMSProp:** square gradients, update moving averages, take square roots, and compute updates for two parameters over multiple steps.
- [x] **33. Adam:** calculate both moments, bias corrections, denominators, and parameter updates, including a gradient sign change.

## 7. Generalization and practical calculations — Lecture 5 and assignment

- [x] **34. L2 regularization and weight decay:** calculate the penalized objective, extra gradient, and update using the lecture's convention; state which parameters are penalized.
- [x] **35. Dropout:** use a fixed mask, calculate retained activations and a forward/backward pass, then compare training and inference scaling conventions.
- [x] **36. Gradient clipping:** apply coordinate clipping and norm clipping to the same vector; compare the resulting update.
- [x] **37. Standardization and initialization:** compute training-set means and standard deviations, transform inputs, and reuse those statistics on new data; calculate initialization scales where covered.
- [x] **38. Early stopping and model selection:** read a training/validation table, apply a stated stopping rule, and identify the checkpoint to restore. Use small diagrams for bagging and augmentation concepts.
- [x] **39. Classification metrics:** build a confusion matrix from predictions, then calculate accuracy, precision, recall, and F1 with the positive class explicitly defined.

## Where to start next

For study, begin with **items 1–3**, then the logistic lesson covering **items 4–5**, and continue with **item 6 onward**. Follow the [numerical index](numerical/README.md) for completed lessons. This is a learning sequence, not a prediction of quiz or midterm coverage.

Scope: Deep Learning material currently available. GenAI should have its own ordered roadmap. Future syllabus topics such as CNNs and sequence models can be added when their lecture material arrives.
