# Deep Learning — Lectures 1–4 Support Guide

**Short explanations first; worked numericals for quizzes and midterms; longer lessons for depth.**

Matched to the lecture files available on **15 September 2026**, including the backpropagation handout, linear-regression homework, and Assignment 1. Page references mean **PDF page numbers**, including title slides, rather than the sometimes different numbers printed on slides. Repeated animation/build slides are grouped together.

**Jump to:** [Lecture 1](#lecture-1--introduction-and-linear-regression) · [Lecture 2](#lecture-2--logistic-regression-and-what-networks-can-represent) · [Lecture 3](#lecture-3--learning-the-network) · [Lecture 4](#lecture-4--optimization-making-learning-converge) · [Assignment support](#assignment-and-handout-support) · [Numerical practice and answers](numerical-practice.md) · [Study route](#a-practical-study-route)

## How to use this guide

1. Open the relevant lecture pages and read the **Study** checklist.
2. Watch the **First watch** selection. Most are about 3–12 minutes; longer exceptions are labeled. A **clip** is an explicitly bounded part of a longer video, with both start and stop times. YouTube start links do not stop playback automatically.
3. For quizzes and midterms, follow **Numerical preparation** where listed. These identify worked calculations separately from intuition or symbolic derivations. Do not skip numerical practice just because the concept feels familiar.
4. Solve the linked [numerical practice and checked answers](numerical-practice.md), then try the topic's **Self-check** without the video. Show intermediate steps and explain your method.
5. Use **Optional depth** for a different explanation, fuller derivations, or implementation. You do not need to watch every alternative. Numerical skills in the supplied lectures deserve practice; the exam's actual coverage is set by your instructor.

“Short” here means a concise teaching video, not necessarily a vertical YouTube Short. Durations are at normal playback speed. Reused videos are intentional: skip them if the earlier viewing was enough.

### Course material

| Source | Scope |
| --- | --- |
| [Lecture 1 — Introduction](Lecture%201%20-%20Introduction.pdf) | 44 pages: learning setup, linear regression, gradient descent |
| [Lecture 2 — Logistic Regression + Neural Network](Lecture%202%20-%20Logistic%20Regression%20%2B%20Neural%20Network.pdf) | 119 pages: logistic regression, neurons, Boolean functions, representational power |
| [Lecture 3 — Learning Neural Network](Lecture%203%20-%20Learning%20Neural%20Network.pdf) | 245 pages: learning rules, loss, calculus, forward and backward passes |
| [Lecture 4 — Neural Network Optimization](Lecture%204%20-%20Neural%20Network%20Optimization.pdf) | 94 pages: convergence, curvature, adaptive steps, momentum |
| [Backpropagation derivation](Backpropagation_Derivation.pdf) | 3 pages: the course's notation and sigmoid/BCE derivation |
| [Linear-regression homework](Home%20work%201%20on%20Linear%20Regression.docx) | Hand calculations with two features and a bias |
| [Assignment 1](Assignment%201.pdf) | 5 pages: configurable NumPy network; MNIST “0 versus not 0” |

Lecture 1's semester outline also names CNNs, transfer learning, computer vision, sequence models, and generative learning. Those are **future outline topics**, not developed lectures in this collection. This guide covers the material supplied so far.

## Lecture 1 — Introduction and linear regression

### 1.1 AI, machine learning, and deep learning

**Pages:** 7–13. Pages 2–6 contain the outline, prerequisites, grading, and logistics; read those directly.

**Study**

- AI, ML, and DL as related fields; multilayer neural networks and learned representations.
- Hand-designed features versus learning features from data.
- Traditional programming: data + rules → outputs. Learning: examples → fitted model.
- Applications in the slides: recognition, prediction, recommendation, clustering, navigation, and generation.
- A well-posed learning problem: task **T**, experience **E**, performance measure **P**.

**First watch:** [IBM / Jeff Crume — AI, Machine Learning, Deep Learning and Generative AI Explained](https://www.youtube.com/watch?v=qYNweeDHiyU) — **10:00**. A vocabulary overview, with examples of how the fields fit together.

**Course connection:** For spam filtering, T is classifying messages, E is previously labeled messages, and P could be held-out classification performance. DL can be supervised or unsupervised; learning features does not mean labels are unnecessary.

**Self-check:** Give T, E, and P for handwriting recognition, then explain what is learned rather than explicitly programmed.

### 1.2 Supervised and unsupervised learning; classification and regression

**Pages:** 14–19, 21–23, 26–29.

**Study**

- Labeled `(x, y)` examples versus unlabeled inputs; classification versus clustering.
- Continuous targets (house prices) versus discrete classes (benign/malignant).
- Multiple input features and structured outputs, such as a parse or a detection result.
- Training examples teach the model; held-out test examples assess predictions on unseen data.

**First watch:** [IBM / Martin Keen — Supervised vs. Unsupervised Learning](https://www.youtube.com/watch?v=W01tIRP_Rqs) — **7:08**. Covers labels, learning goals, and representative tasks.

**Course connection:** A structured prediction can contain several related decisions, such as locations and labels of objects. It is still supervised when corresponding target outputs are supplied.

**Self-check:** Classify house-price prediction, grouping news articles, and tumor diagnosis by learning type and output type. Explain why testing on the training examples is insufficient.

### 1.3 Learning as optimization: inputs, parameters, predictions, and loss

**Pages:** 20, 24–25.

**Study**

- Inputs can be vectors, sequences, matrices, or graphs.
- Distinguish features `x`, parameters `θ`, target `y`, and prediction `ŷ = f(x; θ)`.
- Loss measures prediction error; learning searches for parameters that reduce aggregate loss.
- Training loop: initialize → predict → measure loss → compute an update → repeat.

**First watch:** [StatQuest — Gradient Descent, Step-by-Step: main idea](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=85s) — **clip 1:25–5:38 · 4:13**.

**Self-check:** Point to the data, the adjustable quantities, and the objective in `Σᵢ ℒ(f(xᵢ; θ), yᵢ)`. Which quantities change during training?

### 1.4 Linear regression and squared-error cost

**Pages:** 30–36.

**Study**

- Training-example notation, the hypothesis, slope, and intercept.
- Univariate model: `ŷ = θ₀ + θ₁x`.
- Residuals and squared error; the course uses `J = (1 / 2m) Σᵢ(ŷᵢ − yᵢ)²`.
- Why summing signed residuals can hide large errors; why the factor `1/2` simplifies differentiation.

**First watch:** [StatQuest — The Main Ideas of Fitting a Line to Data](https://www.youtube.com/watch?v=PaFPbb66DxQ) — **9:21**. Visual least-squares intuition.

**Then, for the course formula:** [Andrew Ng — Cost function formula](https://www.youtube.com/watch?v=CFN5zHzEuGY) — **9:05**. Use this if the notation and averaging still feel unclear; it uses `w, b` for slope and intercept.

**Self-check:** Calculate the loss for two predictions by hand. Explain why a smaller squared-error loss need not mean every individual prediction improved.

### 1.5 Gradient descent and simultaneous updates

**Pages:** 37–41.

**Study**

- Derivative as local slope; gradient as the vector of partial derivatives.
- `θⱼ ← θⱼ − α ∂J/∂θⱼ`; learning rate `α` controls step size.
- Compute all derivatives at the same old parameter values, then update together.
- Local descent intuition and why an excessively large step can increase the objective.

**First watch:** [StatQuest — Gradient Descent: one-parameter calculation](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=338s) — **clip 5:38–9:08 · 3:30**. Continue **9:40–14:48 · 5:08** for the iterative updates if needed.

**Course connection:** Page 41's `temp0/temp1` example matters: updating `θ₀` before calculating the old-point gradient for `θ₁` changes the algorithm.

**Self-check:** If the derivative is negative, which way does the parameter move? Explain the error in using a newly updated weight while calculating another update.

### 1.6 Multiple features and linear-regression homework

**Pages:** 42–44; the separate homework sheet.

**Study**

- `ŷ = θᵀx`, with the intercept represented by `x₀ = 1`, or written separately as `b`.
- One partial derivative per feature weight, plus the bias derivative.
- Average the example contributions and update all parameters together.

**First watch:** [StatQuest — Gradient Descent: two or more parameters](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=948s) — **clip 15:48–21:55 · 6:07**.

**Homework bridge:** Your sheet uses `ŷ = w₁x₁ + w₂x₂ + b`, zero initialization, and `α = 0.01`. For its half-mean-squared-error loss, each weight gradient averages `(ŷᵢ − yᵢ)xᵢⱼ`; the bias gradient averages `(ŷᵢ − yᵢ)`. Complete the iteration table using predictions and gradients from the same parameter state.

**Numerical preparation — §§1.4–1.6:** [StatQuest — Gradient Descent, Step-by-Step](https://www.youtube.com/watch?v=sDv4f4s2SB8) — **23:54**, now part of the exam-practice route rather than merely optional depth. The worked sections **5:38–14:48** and **15:48–21:55** evaluate derivatives and make repeated one-/multiple-parameter updates. If you need just the two-parameter step, the second clip is **6:07**. Distinguish its summed squared-error scaling from your course's `1/(2m)` scaling. Then solve **N1.1** in the [numerical practice companion](numerical-practice.md#n11-two-feature-regression-two-batch-updates): a fully specified two-feature problem, two checked updates, and a fresh problem with an answer key.

**Self-check:** Explain why the bias gradient has no feature multiplier. Can you calculate the first update and recompute the loss using the updated parameters?

### Optional depth — Lecture 1

- [StatQuest — Gradient Descent, Step-by-Step](https://www.youtube.com/watch?v=sDv4f4s2SB8) — **23:54**. Best full worked calculation for the homework; it expands the clips above, so you can resume rather than restart.
- [3Blue1Brown — Gradient descent, how neural networks learn](https://www.youtube.com/watch?v=IHZwWFHWa-w) — **20:33**. A visual explanation of a high-dimensional objective and gradient; useful before Lecture 3.
- [StatQuest — Linear Regression, Clearly Explained](https://www.youtube.com/watch?v=nk2CQITm_eo) — **27:26**. Broader statistical context. Its R², p-values, and F-test discussion goes beyond Lecture 1's requirements.

## Lecture 2 — Logistic regression and what networks can represent

### Numerical preparation — Lecture 2

Keep the short **First watch** explanations below for intuition. Then work [L2 numerical practice](numerical-practice.md#l2--logistic-arithmetic-and-network-constructions): fixed inputs, intermediate checkpoints, complete solutions, and changed-value retries cover the calculations the slides require.

| Calculation | Video route and what it demonstrates | Complete the local worked example |
| --- | --- | --- |
| Evaluate a computation graph | **Worked numbers:** [Ng — Computation Graph](https://www.youtube.com/watch?v=hCP1vGoCdYU), **3:34**, substitutes `(a,b,c)=(5,3,2)` and computes the intermediate values `6,11,33`. | L2.2, then its changed-value retry. |
| Differentiate that graph | **Worked derivatives:** [Ng — Derivatives With Computation Graphs](https://www.youtube.com/watch?v=nJyUyKN-XBQ), **14:34**. A longer calculation lesson showing local changes and sensitivities on the concrete graph, not just an algorithm name. | Reproduce the three input derivatives and explain each factor. |
| Sigmoid → BCE → gradients → simultaneous update | **Derivation:** [Ng — Logistic Regression Gradient Descent](https://www.youtube.com/watch?v=z_xiwjEdAC4), **6:43**; **batch formulas:** [Gradient Descent on m Examples](https://www.youtube.com/watch?v=KKfZLXcF-aE), **8:00**. These are not advertised as a complete numerical BCE training pass. | **L2.1 supplies the full numerical bridge:** one example, both-label two-example batch, all averaged gradients, update, and recomputed loss. Use natural logarithms. |
| K-map and Boolean construction | **Worked binary example:** [MIT / Silvina Hanono — Worked Examples: Karnaugh Maps](https://www.youtube.com/watch?v=tjIFsdM-hBA), **3:39**. Works from a concrete truth table/map, groups true cells, and simplifies the sum-of-products expression. | L2.3–L2.5 convert gates and negative literals into weights, compare XOR architectures, and calculate parity counts. |
| Polygon regions and scaled pulses | **Intuition:** the Welch Labs and StatQuest clips below. They are not a worked solution of the exact slide constructions. | L2.6 supplies inequalities, weights, point tests, union logic, pulse heights, and endpoint checks. |

**Completion criterion:** Solve the changed-value batch and constructions before opening their answers. Explain why `δ=p−t` needs no extra sigmoid factor, why gradients are averaged only once, and which connections each counted architecture permits. Video viewing alone is not the numerical checkpoint.

### 2.1 Binary classification, sigmoid, and decision boundaries

**Pages:** 4–15; pages 1–3 recap Lecture 1.

**Study**

- Binary labels, image features, and why an unconstrained linear output is unsuitable as a probability.
- `z = wᵀx + b`, `σ(z) = 1/(1 + exp(−z))`, and estimated probability `ŷ = σ(z)`.
- At threshold 0.5, the decision boundary is `z = 0`.
- A model linear in its parameters can have a nonlinear boundary in the original inputs when features include powers/products.

**First watch:** [Andrew Ng — Logistic Regression](https://www.youtube.com/watch?v=hjrYrynGWGA) — **5:59**.

**Course connection:** Rework the straight-line and circular examples on pages 13–14 by setting their score to zero. A sigmoid supplies a probability-shaped output; it does not by itself guarantee accurate or calibrated probabilities.

**Self-check:** Why does `σ(z) ≥ 0.5` mean `z ≥ 0`? How can squared input features produce a circle?

### 2.2 Binary cross-entropy and gradient descent

**Pages:** 16–26.

**Study**

- For target `t = 1`, loss is `−log(ŷ)`; for `t = 0`, it is `−log(1−ŷ)`.
- Combine the cases as `ℒ = −[t log(ŷ) + (1−t) log(1−ŷ)]` and average over examples.
- Distinguish loss for one example, cost over the dataset, training, and prediction.
- Update weights and bias simultaneously; the prediction formula now contains a sigmoid.

**First watch:** [Andrew Ng — Logistic Regression Cost Function](https://www.youtube.com/watch?v=SHEPb1JHw5o) — **8:12**.

**If gradient direction is still unclear:** [3Blue1Brown — Gradient descent](https://www.youtube.com/watch?v=IHZwWFHWa-w&t=415s) — **clip 6:55–12:19 · 5:24**.

**Self-check:** For a positive example, compare predictions 0.9 and 0.1. Which has greater loss, and why does a confident wrong answer receive a large penalty?

### 2.3 Computation graphs and logistic-regression derivatives

**Pages:** 27–29.

**Study**

- Break a calculation into intermediate nodes, evaluate forward, and apply the chain rule backward.
- Reproduce the slide's `J = 3(a + bc)` graph.
- Derive the sigmoid derivative and the sigmoid + BCE simplification `∂ℒ/∂z = ŷ − t`.
- Obtain each weight gradient by multiplying this error by the corresponding input; the bias gradient is the error itself.

**First watch, two short steps:**

- [Andrew Ng — Computation Graph](https://www.youtube.com/watch?v=hCP1vGoCdYU) — **3:34**, for the forward graph.
- [Andrew Ng — Logistic Regression Gradient Descent](https://www.youtube.com/watch?v=z_xiwjEdAC4) — **6:43**, for derivatives through the classifier.

**Self-check:** Differentiate `3(a + bc)` with respect to all three inputs. Then explain why the sigmoid derivative cancels part of the BCE derivative.

### 2.4 From one example to a training set

**Pages:** 30–31.

**Study:** Accumulate the example losses and gradients, divide by the example count, and make one batch update. Distinguish the sample loop from the outer optimization loop.

**First watch:** [Andrew Ng — Gradient Descent on m Examples](https://www.youtube.com/watch?v=KKfZLXcF-aE) — **8:00**.

**Self-check:** Where does the `1/m` enter? What changes if you update after each example instead of after accumulating the whole batch?

### 2.5 Perceptrons, activations, and multilayer networks

**Pages:** 32–50.

**Study**

- A network is a parameterized function; the brain analogy motivates the design.
- A hard perceptron thresholds a weighted sum; a threshold `T` becomes bias `b = −T`.
- Soft activations: sigmoid, tanh, and softplus; compare with ReLU.
- Input, hidden, and output units; Boolean or real-valued inputs and outputs.
- The slides define node depth by the **longest path** from an input; inputs have depth 0. Follow the course's layer/depth convention when counting.

**First watch:** [3Blue1Brown — Neural-network structure](https://www.youtube.com/watch?v=aircAruvnKk&t=162s) — **clip 2:42–8:38 · 5:56**.

**For activation choices:** [Andrew Ng — Activation Functions](https://www.youtube.com/watch?v=Xvg00QnyaIY) — **10:57**. It introduces sigmoid, tanh, ReLU, and leaky ReLU. For the slide's softplus, use `softplus(z) = log(1 + exp(z))`: a smooth approximation to ReLU, with derivative `σ(z)`.

**Course connection:** The visual network video uses smooth activations; separately reproduce the hard-threshold equation on pages 39–40. Layer-counting conventions vary across videos: use the course's convention, which describes at least three computational layers as deep.

**Self-check:** Turn a threshold into a bias. Draw a small network and label preactivation, activation, hidden units, and each node's depth.

### 2.6 Logic gates, majority, and XOR

**Pages:** 51–60.

**Study**

- Choose weights and thresholds to implement AND, OR, NOT, and majority.
- Why XOR's positive and negative examples cannot be separated by one line.
- How hidden units combine several linear decisions to implement XOR.

**First watch:** [The Coding Train — XOR and the hidden-layer solution](https://www.youtube.com/watch?v=188B6k_F9jU&t=260s) — **clip 4:20–11:49 · 7:29**. Conceptual section; the subsequent JavaScript coding is optional.

**If logic gates are new:** [MIT 6.004 — Useful Logic Gates](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c4/c4s2/c4s2v2/) — **5:56**.

**Threshold and architecture check:** Write `H(s)=1` for `s≥0`, else 0. The integer thresholds on pages 54 and 58 require this inclusive comparison: for example, AND with weights `(1,1)` and threshold 2 must fire at a sum of exactly 2. Half-integer thresholds avoid ties for Boolean inputs. Bias remains `b=−T`.

Page 58's **two-neuron XOR** has direct input-to-output connections: `h=H(x+y−2)`, output `H(x+y−2h−1)`. It has five weighted connections and two biases/thresholds. The later parity construction uses a **different, three-perceptron XOR module**, with two hidden units and one output. Thus three neurons is not a universal minimum for XOR when direct input-to-output connections are permitted.

**Self-check:** Construct AND using weights `(1,1)` and a suitable threshold. Verify every row of both XOR architectures using the worked tables in [L2 numerical practice](numerical-practice.md#l2--logistic-arithmetic-and-network-constructions), then explain the zero-score cases.

### 2.7 Truth tables, DNF, and universal Boolean networks

**Pages:** 61–71.

**Study**

- Convert each true row of a truth table into a conjunction of literals.
- OR those conjunctions together: **disjunctive normal form (DNF)**.
- Map each AND term to a hidden unit and the final OR to an output unit.
- A construction can exist while requiring many hidden units.

**First watch:** [TrevTutor — Disjunctive Normal Form](https://www.youtube.com/watch?v=2cgHa02s_SA&t=96s) — **clip 1:36–5:14 · 3:38**.

**Course connection:** This clip teaches the Boolean expression. Pages 61–71 supply the next step: implementing those terms with perceptrons.

**Self-check:** For a three-input truth table, write its DNF and sketch the corresponding one-hidden-layer network. Count hidden units before simplifying.

### 2.8 Karnaugh maps, parity, and simplification limits

**Pages:** 72–81; page 82 is blank in this PDF.

**Study**

- Arrange a Karnaugh map in Gray-code order and combine adjacent true cells to remove literals.
- Relate fewer Boolean terms to fewer units in the DNF construction.
- Explain the checkerboard pattern for parity: adjacent true cells cannot be merged in this construction.
- Distinguish a limit of the displayed construction from a claim about every possible neural architecture.

**First watch:** [MIT 6.004 — Karnaugh Maps](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c4/c4s2/c4s2v5/) — **10:57**.

**Short revision alternative:** [MIT — Worked example: Karnaugh maps](https://learn.mit.edu/video/7903/worked-example-karnaugh-maps?playlist=7859) — **3:39**. Use this after learning the map rules.

**Self-check:** Draw a three-bit parity map. Why do its true cells resist merging, and how many DNF terms remain?

### 2.9 Why depth can save width—and the limits of that claim

**Pages:** 83–98.

**Study**

- Compose XOR modules to calculate parity; compare a chain and a balanced tree.
- Reproduce the slide's `3(N−1)`-perceptron construction and its depth calculation.
- Compare neuron counts, connection counts, and depth rather than calling all of them “size.”
- Understand why some functions have compact deep constructions, while arbitrary Boolean functions need not.
- Preserve the gate/circuit assumptions in the slides' lower-bound and counting arguments.

**First watch:** [Welch Labs — Geometry of depth](https://www.youtube.com/watch?v=qx7hirqgfuU&t=1192s) — **clip 19:52–24:27 · 4:35**; continue [the exponential comparison](https://www.youtube.com/watch?v=qx7hirqgfuU&t=1467s) — **24:27–30:23 · 5:56** for more detail.

**Course connection:** These are geometric explanations of depth's value. They do **not** prove the lecture's exact parity bounds or circuit-counting statements. Work pages 83–98 alongside them; the CMU lecture below is the closest long-form companion.

**Concrete count, eight inputs:** The displayed DNF construction uses `2⁷=128` hidden units and **129 total** including its output. A balanced tree has **seven XOR modules**; using the specified three-perceptron module gives **21 perceptrons**, with **six computational layers** (two per XOR stage). Inputs have depth zero. These compare constructions, not all possible threshold circuits; page 58's direct connections are a different permitted architecture. For non-powers of two, an uneven balanced tree gives depth at most `2⌈log₂N⌉` in this construction.

**Self-check:** Draw the eight-input tree and distinguish modules, neurons, weights, biases, and depth. Then solve the four-input retry in [L2 numerical practice](numerical-practice.md#l2--logistic-arithmetic-and-network-constructions). Why does this example not establish that every function has a small deep network?

### 2.10 Half-spaces, polygons, and universal classifiers

**Pages:** 99–113.

**Study**

- A threshold unit describes a half-space.
- Intersections of half-spaces form polygonal regions; combining regions produces more complex boundaries.
- Relate AND/OR-style compositions to hidden layers.
- Read the slide construction carefully when comparing single-hidden-layer and deeper classifiers.

**First watch:** [Welch Labs — Universal approximation](https://www.youtube.com/watch?v=qx7hirqgfuU&t=822s) — **clip 13:42–15:45 · 2:03**, for the approximation idea. Reuse the XOR clip for why combining boundaries matters.

**Course connection:** The short clip is intuition, not the slides' polygon construction. Draw the individual inequalities on pages 100–113 and mark how their regions combine.

**Self-check:** Specify four half-space tests whose intersection is a rectangle. How would you represent a union of two separated rectangles?

### 2.11 From classification regions to function approximation

**Pages:** 114–119.

**Study**

- Build a pulse from threshold-like transitions, scale its height, and sum pulses to approximate a function.
- Extend the picture to the slides' higher-dimensional constructions.
- Separate representational capacity from finding suitable weights and generalizing to unseen inputs.
- Universal approximation is an existence/approximation result under assumptions, not exact representation of every function by any fixed small network.

**First watch:** [StatQuest — Building a function by combining curves](https://www.youtube.com/watch?v=CqOfi41LfDw&t=474s) — **clip 7:54–15:25 · 7:31**.

**Self-check:** Sketch a staircase approximation to a smooth curve. What must change if you demand a more accurate approximation? Does existence of the network guarantee that training finds it?

### Optional depth — Lecture 2

- [3Blue1Brown — But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk) — **18:40**. Full visual introduction, including weights, biases, and matrix notation.
- [Andrew Ng — Derivatives With Computation Graphs](https://www.youtube.com/watch?v=nJyUyKN-XBQ) — **14:34**. A slower derivative walkthrough if §2.3 moved too quickly.
- [The Coding Train — XOR Problem](https://www.youtube.com/watch?v=188B6k_F9jU) — **25:01**. A JavaScript implementation after the conceptual section; useful for understanding XOR rather than matching Assignment 1's required implementation.
- [Neso Academy — K Map, Part 1](https://www.youtube.com/watch?v=FPrcIhqNPVo) — **25:45**. More practice with map simplification.
- [Welch Labs — full video containing the approximation/depth sections](https://www.youtube.com/watch?v=qx7hirqgfuU) — **34:08**. Broader visual treatment; the short selections above skip its sponsor section.
- [CMU — Neural Nets As Universal Approximators](https://www.youtube.com/watch?v=bAOKjnqH1Vg) — **1:25:44**. Best extended companion for Boolean representation, depth/width, and approximation. This is CMU's own lecture numbering, not an exact copy of your local slide edition.
## Lecture 3 — Learning the network

This 245-page deck contains many build slides. Work through the topic groups below; the largest group develops one forward/backward calculation gradually.

**Two routes:** the **First watch** links explain concepts and derive formulas. For calculation practice, use the explicitly labeled **Worked numerical video** selections in §§3.4, 3.10, and 3.12, then solve [N3.4's complete handout-matching 2→2→2→1 example](numerical-practice.md#n3-4). The companion also has ordered perceptron traces, chain-rule/Hessian questions, a batch calculation, and changed-value retries with collapsible answers.

### 3.1 What learning changes; constructing a network by hand

**Pages:** 1–27.

**Study**

- Architecture specifies layers and connections; training determines weights and biases.
- A feedforward network has no feedback loops. Each neuron applies an activation to a weighted sum plus bias.
- Revisit Lecture 2's expressiveness result: being able to represent a function does not tell us how to learn it.
- The diamond example constructs a boundary from several linear half-planes. Hand construction becomes impractical for complex targets.
- Training examples provide sampled input-output pairs; fitting them does not guarantee correct predictions everywhere.

**First watch:** [UNSW — Perceptrons by Hand](https://thebox.unsw.edu.au/video/zzen9444-week-1-perceptrons-by-hand) — **about 14 minutes**. A slightly longer short lesson for choosing weights and biases geometrically. Skip if the equivalent Lecture 2 construction is already clear.

**Course connection:** Appending a constant `1` to the input folds the bias into the weight vector: `[w₁,…,w_d,b] · [x₁,…,x_d,1]`. A zero-score hyperplane passes through the origin in this expanded space; the original examples lie in the slice where the last coordinate is `1`.

**Self-check:** Identify the half-planes needed for the slide's diamond. Which quantities are selected when designing the architecture, and which are learned?

### 3.2 Perceptron learning and its convergence condition

**Pages:** 28–54.

**Study**

- Binary classification, signed labels, and the separating hyperplane `wᵀx = 0`.
- The weight vector is normal to that plane and points toward the positive side.
- Cycle over examples and update only on mistakes: add a misclassified positive input; subtract a misclassified negative input.
- The original perceptron algorithm finds a separator in finitely many updates when the data are linearly separable.
- With nonseparable data, its “repeat until no mistakes” rule cannot terminate successfully.

**First watch:** [UNSW — Perceptron Learning Algorithm](https://thebox.unsw.edu.au/video/perceptron-learning) — **about 8 minutes**. A compact explanation of the update rule.

**Numerical practice:** [N3.1 — ordered perceptron trace](numerical-practice.md#n3-1) supplies initial weights, three ordered examples, signed labels, a learning rate, the `s≥0` positive tie convention, and every update/no-update row. Reset and attempt the changed-order/rate retry before opening its answer. The UNSW clip supplies algorithm support; a full ordered numerical trace in that clip was not independently verified.

**Self-check:** Explain why changing example order can change the separator, and why the original “until no mistakes” rule cannot succeed on nonseparable data.

### 3.3 Why the same rule does not directly train hidden layers

**Pages:** 55–77.

**Study**

- Training data specify the final target, but do not specify the desired output of each hidden neuron.
- Different hidden separators must work together; trying assignments of hidden labels creates the combinatorial search discussed in the slides.
- Hard thresholds and 0/1 classification error stay unchanged under many small weight changes, giving no useful gradient direction.
- Replace both the activation and the error measure with quantities that provide useful derivatives.
- Recognize ADALINE/MADALINE as the historical approaches named on page 67; the deck does not derive their algorithms.

**First watch (conceptual):** [DeepLearning.AI — Activation Functions](https://www.youtube.com/watch?v=Xvg00QnyaIY) — **10:57**, shared with §3.4. Focus on replacing a hard threshold with a graded output. Read §3.6 next for the complementary change in loss.

**Derivation later:** Complete the derivative and chain-rule refreshers in §§3.7 and 3.11 before [3Blue1Brown — Backpropagation calculus](https://www.youtube.com/watch?v=tIeHLnjs5U8) — **10:17**, used in §3.12. Students already comfortable with calculus may preview it here.

**Course connection:** Backpropagation eventually connects the final loss to each hidden parameter through derivatives. The particular exponential-relabeling argument and ADALINE/MADALINE history remain **slide-led details**; no equally concise exact video match was verified. Read pages 55–68 alongside the video, or use CMU's optional lecture below.

**Self-check:** Why cannot you train every hidden unit against the network's final class label independently? Why does a hard threshold often hide the effect of a small weight change?

### 3.4 Continuous activations and their derivatives

**Pages:** 74–78, 97–100, 154–156.

**Study**

- Sigmoid, tanh, ReLU, and softplus; their output shapes and derivatives.
- A composition of differentiable operations allows the chain rule to connect a weight change to an output change.
- ReLU is differentiable away from zero; software uses a chosen derivative convention at its corner.

**First watch:** [DeepLearning.AI — Activation Functions](https://www.youtube.com/watch?v=Xvg00QnyaIY) — **10:57**. Then use [Derivatives of Activation Functions](https://www.youtube.com/watch?v=P7_jFxTtJEo) — **7:57** for the calculation on page 156.

**Course connection:** The videos cover sigmoid/tanh/ReLU and also leaky ReLU. The slide additionally includes **softplus**, `log(1 + exp(z))`, whose derivative is `sigmoid(z)`. For the other rows: `sigmoid′ = sigmoid·(1−sigmoid)`, `tanh′ = 1−tanh²`, and `ReLU′ = 0` for negative inputs and `1` for positive inputs. For a **worked numerical video** of softplus, use [StatQuest — constructing the hidden curves](https://www.youtube.com/watch?v=CqOfi41LfDw&t=474s) — **clip 7:54–15:25 · 7:31**. It calculates, for example, an affine value `2.14`, softplus output about `2.25`, and subsequent weighted contributions. This is a regression network; the complete sigmoid/BCE course example is in N3.4.

**Numerical practice:** [N3.2 — activation derivatives and branching chain rule](numerical-practice.md#n3-2) includes positive/negative ReLU, sigmoid, tanh, softplus, upstream gradients, and checked answers.

**Self-check:** Compute the sigmoid derivative from its output value `0.8`. Which activations have no negative outputs, and which ranges from `−1` to `1`?

### 3.5 Sigmoid outputs and logistic regression as probability estimation

**Pages:** 79–96.

**Study**

- Nonseparable examples can be described using a class probability rather than a perfect dividing line.
- The sliding-window illustration estimates the local fraction of examples belonging to class `1`.
- A sigmoid neuron models `P(y=1 | x)`; thresholding this estimate at `0.5` produces a binary decision.

**First watch:** [DeepLearning.AI — Logistic Regression](https://www.youtube.com/watch?v=hjrYrynGWGA) — **5:59**. Reuse the Lecture 2 lesson if already watched.

**Course connection:** A sigmoid output is an **estimated** probability; its numerical range alone does not guarantee that the model is accurate or calibrated. The local-proportion animation is a way to motivate what the model is trying to estimate.

**Self-check:** If the model outputs `0.7`, what is the estimated probability and what is the decision under a `0.5` threshold? Does it imply every similar example has label `1`?

### 3.6 Loss, expected risk, and empirical risk minimization

**Pages:** 19–29, 101–110.

**Study**

- Distinguish misclassification count from a differentiable proxy loss.
- Per-example divergence measures disagreement between a prediction and its target.
- Expected risk averages over the population; empirical risk averages over the observed training set.
- With the training set fixed, optimization treats the loss as a function of the parameters.

**First watch:** [DeepLearning.AI — Logistic Regression Cost Function](https://www.youtube.com/watch?v=SHEPb1JHw5o) — **8:12**. A concrete example of one-example loss and the average over training examples.

**Course connection:** For `ℓᵢ(W) = Div(f(xᵢ;W),dᵢ)`, empirical risk is `R̂(W) = (1/m)Σᵢℓᵢ(W)`. Population risk is `R(W) = E[ℓ(W)]` under the relevant data distribution. We can calculate the first from our samples; the second describes the broader goal. The short video illustrates averaging, while this expectation-versus-sample distinction comes from the slides. Low training loss does not establish good generalization.

**Self-check:** Explain why minimizing a smooth loss can help classification even though the loss is not the number of mistakes. Why do we still need unseen examples for evaluation?

### 3.7 Derivatives, partial derivatives, and gradient geometry

**Pages:** 111–120, 167–173.

**Study**

- A derivative describes the local effect of a small input change: `Δf ≈ f′(x)Δx`.
- Partial derivatives vary one coordinate at a time; the gradient collects them.
- The gradient points in the direction of steepest local increase; its negative points downhill.
- At a regular point, the gradient is perpendicular to the level curve.

**First watch:** [DeepLearning.AI — Derivatives](https://www.youtube.com/watch?v=GzphoJOVEcE) — **7:10**; then [Khan Academy — Gradient and graphs](https://www.youtube.com/watch?v=_-02ze7tf08) — **6:10** for geometry.

**Course connection:** These slides use a row-vector derivative and call its transpose the column-vector gradient. Other lessons may use “derivative” and “gradient” less distinctly. Follow the dimensions, rather than adding transposes by memory.

**Self-check:** For `f(x,y)=x²+3y²`, calculate the gradient at `(1,2)`. Answer: `[2,12]ᵀ`; `−[2,12]ᵀ` is a downhill direction. A step `Δ=(−0.002,−0.012)` has first-order predicted change `∇f·Δ=−0.148`. Use [N3.2](numerical-practice.md#n3-2) for a complete branching-derivative calculation.

### 3.8 Critical points, curvature, and the Hessian

**Pages:** 121–132.

**Study**

- Local versus global extrema; zero slope/gradient gives a candidate stationary point.
- The second derivative describes curvature; the Hessian collects second partial derivatives.
- At a stationary point, a positive-definite Hessian establishes a strict local minimum; negative-definite establishes a strict local maximum.
- Positive and negative eigenvalues together indicate a saddle; a zero/semidefinite test can be inconclusive.

**First watch:** [Khan Academy — Applying the second derivative test](https://www.khanacademy.org/v/second-derivative-test) — **6:12**; then [The Hessian matrix](https://www.youtube.com/watch?v=LbBcuZukCAw) — **6:10**.

**Course connection:** The Hessian video teaches the matrix; the arbitrary-dimensional eigenvalue classification is the slide's additional step. Use the [Khan second partial derivative test explanation](https://www.khanacademy.org/a/second-partial-derivative-test) for a worked two-variable connection. A zero second derivative does **not** by itself establish an inflection point, and zero gradient does **not** establish a minimum.

**Numerical practice:** [N3.3 — gradient, mixed-term Hessian, and classification](numerical-practice.md#n3-3) includes solved stationary-point equations, eigenvalues, a saddle, an inconclusive test, and a fresh retry.

**Self-check:** The origin for `x²+y²`, `−x²−y²`, and `x²−y²` is respectively a minimum, maximum, and saddle. Explain why, and why a zero second derivative does not settle `x⁴` at zero.

### 3.9 Gradient descent: direction, step size, and stopping

**Pages:** 133–145, 163–166.

**Study**

- Use an iterative method when solving the derivative equations directly is impractical.
- Start from an initial parameter estimate and apply `W ← W − α∇R̂(W)`.
- The direction and the step size both matter; excessive steps can increase loss.
- Stop using criteria such as a sufficiently small gradient norm or small absolute loss change.
- Understand the different guarantees for suitable convex objectives and nonconvex neural-network objectives.

**First watch:** [DeepLearning.AI — Gradient Descent](https://www.youtube.com/watch?v=uJryes5Vk1o) — **11:24**. Skip the repeated basics if Lecture 1 was enough.

**Course connection:** Convergence claims require assumptions and suitable step sizes. For neural networks, a small gradient does not certify a global minimum. Lecture 4 examines why optimization can still be difficult.

**Self-check:** Apply one step to `f(w)=w²` at `w=1` with `α=0.1`, then with `α=2`. What does this show about step size?

### 3.10 Setting up the network and computing the forward pass

**Pages:** 146–162, 181–199.

**Study**

- Input, hidden, and output layers; scalar versus vector input/target/output.
- Pre-activation `z` is an affine combination; activation `y` is the result after the nonlinear function.
- Layer, neuron, and connection indices; bias as a separate parameter or fixed-one input.
- Compute each layer from the previous layer, and save intermediate values for backpropagation.

**First watch:** [DeepLearning.AI — Computing Neural Network Output](https://www.youtube.com/watch?v=rMOdrD61IoU) — **9:58**.

**Notation bridge:** The slides' `y⁽ᵏ⁾` corresponds to Andrew Ng's activation `a^[k]`; `z` means pre-activation in both. The slides' `wᵢⱼ⁽ᵏ⁾` connects previous-layer unit `i` to current-layer unit `j`. Check the orientation before copying a matrix formula from another source. For a real-valued vector target, use as many output coordinates as its dimension.

**Worked numerical video:** [StatQuest — using the network to make a prediction](https://www.youtube.com/watch?v=CqOfi41LfDw&t=925s) — **clip 15:25–16:38 · 1:13**, a quick replay of the full forward arithmetic: input dosage `0.5` produces approximately `1.03`. For the buildup, watch **7:54–16:38 · 8:44**, or the full **18:54** lesson. It uses softplus hidden neurons and a linear regression output, so `1.03` is not a sigmoid probability.

**Numerical practice:** [N3.4 — handout-matching forward pass](numerical-practice.md#n3-4) supplies all ten weights and five biases for two hidden layers. Compute every intermediate activation before expanding the answer table.

### 3.11 Computational graphs and the multivariable chain rule

**Pages:** 167–180, 216, 228.

**Study**

- Draw how intermediate values depend on one another.
- Multiply local derivatives along a dependency path.
- When a quantity influences the loss through several paths, add their contributions.
- Distinguish a graph for computing values from the derivatives attached to its edges.

**First watch:** [DeepLearning.AI — Computation Graph](https://www.youtube.com/watch?v=hCP1vGoCdYU) — **3:34**; then [Khan Academy — Multivariable chain rule](https://www.youtube.com/watch?v=NO3AqAaAE6o) — **9:32**.

**Numerical practice:** [N3.2 — both paths with numbers](numerical-practice.md#n3-2): for `u=x²`, `v=3x`, `L=uv` at `x=2`, find `u`, `v`, `L`, the two path contributions, and their sum. Then repeat at `x=−1`; worked answers are collapsed below the question.

### 3.12 Backpropagation, bias gradients, and the full training loop

**Pages:** 163–166, 187–245; [Backpropagation derivation handout](Backpropagation_Derivation.pdf).

**Study**

- Forward pass: calculate and retain predictions and intermediate activations.
- Begin with the derivative of loss with respect to the output, then differentiate through the output activation.
- Compute each incoming weight gradient, the bias gradient, and the contribution to earlier activations.
- Sum downstream contributions for a hidden unit and repeat backward through the layers.
- Average per-example gradients for an average loss, then update parameters together.
- Backpropagation calculates gradients; the optimizer uses them to change parameters.

**First watch:** Reuse [3Blue1Brown — Backpropagation calculus](https://www.youtube.com/watch?v=tIeHLnjs5U8) — **10:17**; then [DeepLearning.AI — Forward and Backward Propagation](https://www.youtube.com/watch?v=qzPQ8cEsVK8) — **10:30** for the layer-by-layer formulas and cached values.

**Worked numerical video route:** These selections actually substitute values and update parameters; the clips above primarily teach derivation and layer formulas.

1. [StatQuest — Backpropagation Details, Part 1](https://www.youtube.com/watch?v=iyn2zdALii8&t=651s) — **clip 10:51–17:19 · 6:28** (full **18:31**). Derives output-weight gradients, then substitutes data to obtain a gradient of `2.58` and updates two weights plus the output bias. Quick arithmetic replay: **15:02–17:19 · 2:17**.
2. [StatQuest — Backpropagation Details, Part 2](https://www.youtube.com/watch?v=GKZoOHXGcLo&t=88s) — **clip 1:28–11:18 · 9:50** (full **13:08**). Extends the calculation into the hidden layer; the numeric substitution gives a hidden-weight gradient of `0.76`, followed by parameter updates. Quick replay: **9:21–11:18 · 1:57**. Watch the whole lesson if the chain-rule setup is unfamiliar.

**Loss/architecture bridge:** StatQuest uses **softplus hidden units, a linear output, and summed squared residuals** in a one-hidden-layer example. Our handout uses **two sigmoid hidden layers, a sigmoid output, and BCE**. Transfer the dependency paths and simultaneous-update procedure, but recompute local derivatives for the stated activation and loss. For sigmoid with **half-squared error**, output delta would be `(y−t)y(1−y)`; for the handout's sigmoid+BCE it is `y−t`. For an unhalved sum of squared residuals there is also a factor of `2`. The verified local solution below fills the exact course example the videos do not provide.

**Batch bridge:** [DeepLearning.AI — Gradient Descent on m Examples](https://www.youtube.com/watch?v=KKfZLXcF-aE) — **8:00**, if averaging the gradients is unclear. For `J=(1/m)Σℓᵢ`, `∇J=(1/m)Σ∇ℓᵢ`: apply the averaging factor once consistently.

**Course connection:** For example `n`, define the **per-example** pre-activation error `δₙ,ⱼ⁽ᵏ⁾ = ∂ℓₙ/∂zₙ,ⱼ⁽ᵏ⁾`. Suppress `n` while working on one example: `δⱼ⁽ᵏ⁾ = ∂ℓ/∂zⱼ⁽ᵏ⁾`. Then `∂ℓ/∂wᵢⱼ⁽ᵏ⁾ = yᵢ⁽ᵏ⁻¹⁾δⱼ⁽ᵏ⁾`, and the separate bias gradient is `δⱼ⁽ᵏ⁾`. A hidden unit combines downstream errors: `δᵢ⁽ᵏ⁾ = f′(zᵢ⁽ᵏ⁾)Σⱼwᵢⱼ⁽ᵏ⁺¹⁾δⱼ⁽ᵏ⁺¹⁾`. Follow the handout's precise definition of `δ` and loss reduction when translating notation. For sigmoid with binary cross-entropy, the output pre-activation derivative simplifies to prediction minus target for one example.

**Worked course calculation:** [N3.4 — complete 2→2→2→1 sigmoid/BCE pass](numerical-practice.md#n3-4) has all five deltas, every one of the fifteen gradients and updates, the two-path hidden sum, and loss before/after the update. Follow with [N3.5 — two-example batch](numerical-practice.md#n3-5) and [N3.6 — changed-target retry](numerical-practice.md#n3-6).

**Mean-loss convention:** When `J=(1/m)Σₙℓₙ`, average the parameter contributions from these per-example deltas **once**. If delta is instead defined as `∂J/∂zₙ`, it already contains `1/m` and must not be averaged again. The assignment's `delta=prediction−target` followed by averaging gradients uses the per-example interpretation.

**Self-check:** Complete the fresh full-network retry without the key. Explain why you must retain the old downstream weights throughout the backward pass, why each bias gradient equals its destination delta, and why the two-example batch step differs from updating after each example.

### Optional depth — Lecture 3

- **Perceptron detail:** [Sebastian Raschka — The Perceptron Learning Rule](https://www.youtube.com/watch?v=C8Uns9HEVXI) — **31:39**. Use when the geometry, update rule, or limitations need a slower explanation.
- **Learning setup, hidden-label difficulty, and ERM:** [CMU — Learning the Network, Part 1](https://www.youtube.com/watch?v=KI-dpw3pkls) — **1:32:30**. Closely related university material for the first part of this deck.
- **Optimization and training setup:** [CMU — Learning the Network: Backprop](https://www.youtube.com/watch?v=lYYkEx1Qx8s) — **1:37:43**. For more of the mathematical development. CMU's lecture numbering differs from this combined local deck.
- **Backpropagation derivation:** [CMU — Learning the Network, Part 3](https://www.youtube.com/watch?v=G_N3IS-nqYQ) — **1:28:39**. A full university explanation when the short derivation needs reinforcement.
- **Visual training intuition:** [3Blue1Brown — Gradient descent, how neural networks learn](https://www.youtube.com/watch?v=IHZwWFHWa-w) — **20:33**. Connects parameter search, loss, and learned behavior.
- **Build it in Python:** [Andrej Karpathy — Building micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0) — **2:25:52**. Build an automatic-differentiation engine and train a small MLP. Useful smaller chapters: [08:08–14:12](https://www.youtube.com/watch?v=VMj-3S1tku0&t=488s) (**6:04**, scalar derivative), [1:22:28–1:27:05](https://www.youtube.com/watch?v=VMj-3S1tku0&t=4948s) (**4:37**, accumulating gradients through reused nodes), and [2:01:12–2:14:03](https://www.youtube.com/watch?v=VMj-3S1tku0&t=7272s) (**12:51**, training by gradient descent).


## Lecture 4 — Optimization: making learning converge

**Two study routes:** Use the concise videos below for intuition and derivation, then use [N4: worked optimizer calculations](numerical-practice.md#n4-lecture-4--calculating-optimizer-updates) for paper-and-pencil practice with checked answers. The momentum/Nesterov clips and RProp animation are conceptual resources; a numerical iteration-table walkthrough for those exact slide conventions was not verified in a suitable short video. The local examples supply that bridge.

For calculation readiness, complete one scalar stability table, a mixed-term Hessian/Newton step, a decay schedule, a RProp rejection/retry trace, and two momentum/Nesterov updates from identical starting values. Each worked example has a changed-value problem with collapsible answers. Understanding the result and solving the retry matter more than finishing a video.

### 4.1 The training loop, surrogate loss, and the “spoiler” example

**Pages:** 2–26. Pages 6–7 introduce the questions and agenda.

**Study**

- Initialize parameters → forward pass → loss → backpropagation → aggregate gradients → parameter update → repeat.
- Backpropagation calculates derivatives; gradient descent uses them to update parameters.
- Classification error counts wrong decisions. A differentiable loss is a **surrogate**, or proxy, that supplies useful gradients.
- Distinguish a loss whose optimum is unsuitable from an optimizer that fails to reach that optimum.
- Reproduce the three-point and four-point examples, the bounded-weight “spoilers,” and the extension to multilayer classifiers.
- Connect sensitivity to changes in training data with the slides' bias–variance discussion.

**First watch — concepts/derivation:** Reuse [Andrew Ng — Logistic Regression Cost Function](https://www.youtube.com/watch?v=SHEPb1JHw5o) — **8:12**, if you need the loss-versus-classification foundation. The exact spoiler example needs the slide walkthrough below; this video does not reproduce it.

**Course connection:** In the four-point sigmoid/L2 example, the distant added point `(0, −t)` can be misclassified while saturation makes its gradient contribution very small near the old solution. A separating boundary exists, but training can remain near a broad local minimum. This local-optimization failure is distinct from the earlier observation that minimizing a surrogate need not minimize classification error. The bias–variance interpretation describes these examples; it is not a guarantee that every network trained with backpropagation has low variance.

**Numerical bridge:** At confidently wrong `p=.01, t=1`, sigmoid plus half-squared-error gives `dL/dz=−.009801`, while sigmoid+BCE gives `−.99`. Work through the loss-dependent chain rule and a changed-value retry in [N4.1](numerical-practice.md#n41-why-the-loss-changes-the-saturation-calculation).

**Self-check:** Draw the four points and explain how the perceptron can separate them while sigmoid/L2 training can struggle. Which part concerns representation, which concerns the chosen loss, and which concerns optimization?

### 4.2 Loss surfaces: minima, saddle points, and convexity

**Pages:** 27–30; recap on page 29.

**Study**

- Local versus global minimum; a stationary point has zero gradient but need not be a minimum.
- A saddle rises in some directions and falls in others. At a stationary point, a Hessian with both positive and negative eigenvalues establishes a saddle; degenerate cases can need further analysis.
- Convexity and contour plots; why convex optimization is useful background even though neural-network losses are generally nonconvex.
- Treat the discussion of large-network landscapes as intuition rather than a promise that optimization always succeeds.

**First watch — concepts/derivation:** [Andrew Ng — The Problem of Local Optima](https://www.youtube.com/watch?v=fODpu1-lNTw) — **5:23**.

**For convexity:** [Steve Brunton — Convexity 101](https://www.youtube.com/watch?v=9WXVgQFFsDI&t=202s) — **clip 3:22–7:07 · 3:45**. Covers convexity and its connection to local optima.

**Numerical practice:** [N4.3](numerical-practice.md#n43-hessian-eigenvalues-gradient-descent-and-newton) compares a positive-definite minimum, an indefinite saddle, and a minimum where the Hessian test is inconclusive.

**Self-check:** Sketch a minimum and a saddle. Why is “the gradient is zero” insufficient evidence that training found the desired solution?

### 4.3 Scalar convergence: step size, oscillation, and rate

**Pages:** 31–36.

**Study**

- Converging, jittering, and diverging updates.
- Convergence rate measures how quickly the error shrinks; **linear convergence** means a constant-factor reduction each iteration.
- Quadratic objectives, a second-order Taylor approximation, and the relationship between curvature and a suitable step size.

**First watch — worked updates:** [StatQuest — Gradient Descent: iterative one-parameter updates](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=580s) — **clip 9:40–14:48 · 5:08**. Reuse it for the update mechanics; the course's exact convergence argument is below.

**Course calculation:** For `E(w) = a(w − w*)²/2`, where `a > 0`, gradient descent gives `w_next − w* = (1 − αa)(w − w*)`.

| Step size | What happens |
| --- | --- |
| `0 < αa < 1` | Approaches without alternating sides |
| `αa = 1` | Reaches the quadratic's minimum in one step |
| `1 < αa < 2` | Alternates sides but converges |
| `αa = 2` | Generally oscillates without shrinking |
| `αa > 2` | Diverges unless already at the solution |

A constant-factor reduction makes the error geometric/exponential in the iteration count, despite the name “linear convergence.” For a general function, its local quadratic approximation changes as you move.

**Numerical practice:** [N4.2](numerical-practice.md#n42-scalar-convergence-distinguish-parameter-error-from-loss) gives two updates and losses for every regime above, followed by a new problem with answers. The signed parameter-error factor is `1−αa`, its magnitude controls distance to the solution, and the loss ratio is `(1−αa)²` for this quadratic when the previous loss is nonzero.

**Self-check:** Set `a = 4` and classify learning rates `0.1`, `0.25`, `0.4`, `0.5`, and `0.6`. Calculate two updates for one convergent and one divergent case.

### 4.4 Many parameters: the Hessian and difficult directions

**Pages:** 37–49.

**Study**

- The **Hessian** collects second partial derivatives; eigenvalues describe curvature along its eigenvector directions.
- Diagonal quadratics have independent coordinates and axis-aligned elliptical contours.
- The gradient is perpendicular to a contour, but one scalar learning rate must serve every coordinate.
- A rate suitable for a flat direction may be unstable in a steep one; rotated contours couple the original coordinates.
- The **condition number** `λmax/λmin` describes the curvature imbalance for a positive-definite quadratic.

**First watch — concepts/derivation:** [Khan Academy — The Hessian matrix](https://www.youtube.com/watch?v=LbBcuZukCAw) — **6:10**.

**Then see the geometry:** [Stanford CS231n — Zig-zagging during optimization](https://www.youtube.com/watch?v=_JB0AO7QxSA&t=1024s) — **clip 17:04–18:27 · 1:23**. This short illustration accompanies the slide derivation.

**Course connection:** In each eigenvector direction, the previous scalar calculation uses `a = λᵢ`. Convergence on a positive-definite quadratic therefore requires `0 < α < 2/λmax`. When `λmax/λmin` is large, the safe rate for the steep direction can be very slow in the flat direction. This is a quadratic result, not a universal fixed-rate guarantee for neural nets.

**Numerical practice:** [N4.3](numerical-practice.md#n43-hessian-eigenvalues-gradient-descent-and-newton) works from a diagonal warm-up to `H=[[3,1],[1,3]]`: calculate both eigenvalues, the stable-rate interval, one gradient step, and a Newton step.

**Self-check:** For Hessian eigenvalues `1` and `100`, find the fixed-rate stability interval. Why can the flat direction make little progress even when the updates are stable?

### 4.5 Newton's method and the cost of curvature

**Pages:** 33–36, 47–52; recap on page 59.

**Study**

- Newton's method minimizes a local quadratic approximation rather than following only the current slope.
- Its step solves `HΔ = −∇E`, often written `Δ = −H⁻¹∇E`.
- Curvature-aware updates compensate for different scales in different directions.
- A network with `100,000` parameters has `10¹⁰` Hessian entries; forming and solving with this matrix can be expensive.
- In a nonconvex region, an indefinite Hessian can point Newton's method toward an unsuitable stationary point.

**First watch — concepts/derivation:** [mathematicalmonk — Newton's method for optimization: intuition](https://www.youtube.com/watch?v=28BMpgxn_Ec) — **11:16**. Connects the one-dimensional picture with quadratic approximation in several dimensions.

**Course connection:** Newton root finding seeks `f(x) = 0`; Newton optimization applies the idea to the gradient. Finding a stationary point still requires checking whether it is the kind of solution you want. For the quadratic analysis here, assume a positive-definite Hessian; strict convexity alone does not imply a positive-definite Hessian at every point of every function.

**Worked-number route:** [Holistic Numerical Methods — Newton optimization example](https://www.youtube.com/watch?v=bOyy2Vlk6RY) — **14:15**, a genuine one-dimensional gutter-angle application, identified by the [educational project as its example lesson](https://nm.mathforcollege.com/chapter-09-02-newtons-method-for-one-dimensional-optimization-example/). For a complete two-variable calculation matching the lecture math, solve the mixed-term quadratic in [N4.3](numerical-practice.md#n43-hessian-eigenvalues-gradient-descent-and-newton). The mathematicalmonk video above supplies intuition and derivation, not a certified numerical iteration table.

**Self-check:** Why does inverse curvature appear in the Newton step? Give one computational and one geometric reason ordinary Newton updates are difficult for a large neural net.

### 4.6 Approximating curvature: BFGS, L-BFGS, and Levenberg–Marquardt

**Pages:** 53; related recap on page 59. These methods receive a conceptual overview in the slides.

**Study**

- **Quasi-Newton methods** estimate curvature using information from successive updates and gradients.
- BFGS maintains a curvature approximation; **L-BFGS** reduces memory by retaining a limited update history.
- For nonlinear least squares, **Levenberg–Marquardt (LM)** adds damping to a Jacobian-based Gauss–Newton approximation.
- Damping helps control the step; these methods do not remove all computational or nonconvexity difficulties.

**First watch — concepts/derivation:** [Stanford CS231n — Second-order optimization and L-BFGS](https://www.youtube.com/watch?v=_JB0AO7QxSA&t=2835s) — **clip 47:15–50:54 · 3:39**. A short overview, not a BFGS derivation.

**Brief LM bridge:** Gauss–Newton linearizes the residuals and uses `JᵀJ` as curvature information. LM adds a positive damping term, for example `JᵀJ + μI`, before calculating a step. Read [Cornell's LM section](https://www.cs.cornell.edu/courses/cs4220/2026sp/lec/2026-04-10.html#levenberg-marquardt) alongside page 53. For BFGS/L-BFGS, [Cornell's short optimization overview](https://cvw.cac.cornell.edu/SciML/diffsim/advanced-optimization) explains the approximation and limited history.

**Longer specialist exception:** [Stephen Boyd / Stanford ENGR108 — Levenberg–Marquardt algorithm](https://www.youtube.com/watch?v=UQsOyMj9lnI) — **20:01**. Use this when you want the LM video explanation; no verified short segment was available for this upload.

**Self-check:** Match each method to its central idea: exact Hessian, curvature estimated from gradient changes, limited history, or damped Jacobian-based least squares.

### 4.7 Learning-rate decay: moving quickly, then settling

**Pages:** 54–60.

**Study**

- Large steps can move out of some undesirable regions but can also prevent settling near a solution.
- Compare the slides' linear, quadratic, and exponential decay schedules.
- Reduce the rate when loss or held-out performance stagnates, continuing from the existing parameters.
- Decaying the learning rate changes step size; it does not guarantee the global optimum.

**First watch — concepts/derivation:** [Andrew Ng — Learning Rate Decay](https://www.youtube.com/watch?v=QzulmoOg2JE) — **6:44**.

**Course connection:** The slide's discussion of rates greater than `2` assumes a normalized curvature model. It is not a general recommendation to use a learning rate above `2` in a neural-network implementation.

**Numerical practice:** Page 57 uses `ηₖ=η₀/(k+1)`, `ηₖ=η₀/(k+1)²`, and `ηₖ=η₀ exp(−βk)`. [N4.4](numerical-practice.md#n44-learning-rate-decay-with-the-slides-exact-indexing) starts at `k=0`, calculates each schedule, and distinguishes these formulas from a plateau-triggered reduction.

**Self-check:** Sketch an exponential schedule and a plateau-triggered step schedule. Why might a rate that was useful early in training be unsuitable near the end?

### 4.8 RProp: separate step sizes from gradient magnitudes

**Pages:** 61–74.

**Study**

- **Resilient propagation (RProp)** adapts a separate step size for each parameter.
- Repeated derivative signs increase that parameter's step; a sign reversal suggests overshooting and reduces it.
- Trace the slide version's backtracking, step-size floor and ceiling, and pseudocode.
- RProp still uses derivatives obtained through backpropagation; it changes how those derivatives determine updates.

**First watch — conceptual animation, focused 15-minute exception:** [Ryan Harris — Visualize Back Propagation: RProp and iRProp+](https://www.youtube.com/watch?v=Cy2g9_hR-5Y) — **15:00**. This specialist animation is [linked by RProp inventor Martin Riedmiller](https://www.riedmiller.me/subprojects/rprop), and compares optimization paths rather than only listing formulas.

**Course connection:** RProp has variants, especially in how sign reversals and backtracking are handled. Reproduce the version on your slides for coursework. Do not confuse **RProp** with **RMSProp**: they are different algorithms.

**Numerical practice:** [N4.5](numerical-practice.md#n45-rprop-keep-the-state-when-an-attempted-step-is-rejected) shows growth, an overshoot, rollback, shrink, and retry. It preserves the previous accepted derivative on rejection and separates positive step magnitudes from signed updates so bounds apply correctly. A four-attempt retry problem includes intermediate answers.

**Self-check:** Trace a parameter with derivative signs `negative → negative → positive`. Show when its step grows, when the slide algorithm backtracks, and when the step shrinks.

### 4.9 Momentum: preserve consistent progress and reduce oscillation

**Pages:** 75–85; recap on page 93.

**Study**

- Maintain a weighted history of gradients or previous steps.
- Consistent directions accumulate; alternating directions partially cancel.
- Interpret the momentum coefficient, commonly `β = 0.9` in the examples.
- Compare the vanilla and momentum training pseudocode and the two-arrow geometric construction.

**First watch — concepts/derivation:** [Andrew Ng — Gradient Descent With Momentum](https://www.youtube.com/watch?v=k8fTYJPd3_I) — **9:20**.

**Course connection:** Some definitions use `v ← βv + (1−β)g`; others use `v ← βv + g`. The scaling can be absorbed into the learning rate, so compare conventions before copying numeric settings. Momentum often improves optimization, but does not guarantee superiority for every problem and setting.

**Numerical practice:** [N4.6](numerical-practice.md#n46-momentum-and-nesterov-two-steps-from-the-same-state) uses a signed parameter-displacement convention and calculates two updates of plain gradient descent, momentum, and Nesterov from the same initial point.

**Self-check:** Compare averaging gradients `(1,10), (1,−10), (1,10), (1,−10)` with using each gradient directly. Which component represents sustained progress?

### 4.10 Nesterov momentum: evaluate the gradient after looking ahead

**Pages:** 86–93.

**Study**

- Ordinary momentum measures the gradient at the current parameters and combines it with the previous step.
- Nesterov first predicts a position using the previous step, then measures the gradient there to correct the move.
- Follow the two geometric constructions and reproduce the training pseudocode.
- Faster convergence in particular examples is not a guarantee that every nonconvex training run reaches its global minimum.

**First watch — concepts/derivation:** [Stanford CS231n — Nesterov Momentum](https://www.youtube.com/watch?v=_JB0AO7QxSA&t=1801s) — **clip 30:01–33:14 · 3:13**.

**Alternative concise explanation:** [Marc Lelarge / Dataflowr — Nesterov accelerated gradient](https://www.youtube.com/watch?v=UvM0hK4E2dc&t=938s) — **clip 15:38–18:00 · 2:22**.

**Numerical practice:** Complete the Nesterov column in [N4.6](numerical-practice.md#n46-momentum-and-nesterov-two-steps-from-the-same-state), including the lookahead coordinate before taking its derivative. The two methods agree on the first step with zero initial velocity, so a one-step example cannot show their difference.

**Self-check:** Draw the point at which each method evaluates its gradient. What changes if you add the old velocity but continue evaluating the gradient at the original position?

### Optional depth — Lecture 4

- [CMU — Lecture 6: Convergence](https://www.youtube.com/watch?v=vL4RTAUcljY) — **1:26:25**. Closest extended companion for the surrogate-loss examples, convergence, curvature, and momentum. Its numbering and slide edition differ from your local course.
- [Stanford CS231n — Training Neural Networks II](https://www.youtube.com/watch?v=_JB0AO7QxSA) — **1:15:30**. Expands the short clips above. Later sections on ensembles, regularization, and transfer learning go beyond this lecture.
- [Stephen Boyd — Levenberg–Marquardt algorithm](https://www.youtube.com/watch?v=UQsOyMj9lnI) — **20:01**, the specialist explanation linked in §4.6. His [VMLS textbook](https://web.stanford.edu/~boyd/vmls/vmls.pdf), §18.2–18.3, develops Gauss–Newton and LM.
- [Gabriel Goh — Why Momentum Really Works](https://distill.pub/2017/momentum/) — interactive reading, not a video. Useful for connecting momentum to the eigenvalue and convergence analysis.

**Clip notes:** The Stanford excerpt boundaries above come from YouTube's platform-generated chapters; allow a small rewind if you need the preceding context. Brunton and Dataflowr publish their own chapter timestamps. Start links do not stop playback at the stated endpoint.

**Preview-only items:** RMSProp, AdaGrad, and stochastic/incremental updates appear in the agenda or coming-up slides but are not developed in this PDF. Quickprop is named on page 62 without a derivation. Page 94 also previews generalization, divergences, activations, and normalization. Treat those as later material rather than additional completed sections of Lecture 4.

## Assignment and handout support

### A. Backpropagation derivation: use the course notation

**Source:** [Backpropagation_Derivation.pdf](Backpropagation_Derivation.pdf), all 3 pages; also §3.12.

The handout uses two hidden layers and one output layer, all sigmoid. The assignment extends this to configurable depth, widths, and hidden activations.

| Symbol | Meaning in your handout | Common video equivalent |
| --- | --- | --- |
| `zⱼ⁽ˡ⁾` | Weighted sum plus bias before activation | `z` |
| `yⱼ⁽ˡ⁾` | Neuron activation; input is layer 0 | Andrew Ng's `a^[l]` |
| `wᵢⱼ⁽ˡ⁾` | Edge from previous-layer unit `i` to current-layer unit `j` | Check matrix orientation before using `W` |
| `w₀ⱼ⁽ˡ⁾` | Bias from the fixed-one input | `bⱼ` |
| `t` | True target | Frequently called `y` in videos |
| `δⱼ⁽ˡ⁾` | Derivative with respect to a neuron's preactivation | Often called `dZ` |

**First watch:** [Andrew Ng — Logistic Regression Gradient Descent](https://www.youtube.com/watch?v=z_xiwjEdAC4) — **6:43** for the output cancellation; [3Blue1Brown — Backpropagation calculus](https://www.youtube.com/watch?v=tIeHLnjs5U8) — **10:17** for propagation through earlier weights. Reuse earlier viewings.

**Work through:** Derive `δoutput = ŷ − t` for one sigmoid/BCE example, propagate the error into both hidden layers, and calculate one weight and one bias gradient at each layer. The assignment's batch loss is an average: either average in `dZ` or average the accumulated gradients, consistently. **Do not divide by the batch size twice.**

**Numerical preparation:** [N3.4 in the practice companion](numerical-practice.md#n3-4) supplies a fully specified **2→2→2→1** example matching this handout's architecture: all intermediate activations, five deltas, fifteen parameter gradients and simultaneous updates, and a new loss. Follow it with [N3.5's batch-average calculation](numerical-practice.md#n3-5) and [N3.6's changed-target retry](numerical-practice.md#n3-6). Complete the whole calculation rather than stopping after one output-layer weight. Use §3.12's worked-number video route before attempting it.

### B. NumPy shapes, vectorization, and initialization

**Source:** [Assignment 1](Assignment%201.pdf), pages 1–4. These are implementation prerequisites/extensions for the assignment.

**Study**

- Configure the network through layer sizes and hidden-activation names rather than hard-coding one architecture.
- Use NumPy matrix operations across examples; a loop over layers is allowed.
- Keep a consistent batch orientation and check every matrix and bias shape.
- Implement activation functions and their derivatives in one reusable place.
- Initialize weights randomly to break hidden-unit symmetry. **For this assignment, initialize bias vectors randomly too**, as specified in its `initialize()` requirements; generic tutorials may use zero biases instead.

**First watch, as needed:**

- [Andrew Ng — Vectorization](https://www.youtube.com/watch?v=qsIrQi0fzbY) — **8:04**.
- [Andrew Ng — Broadcasting in Python](https://www.youtube.com/watch?v=tKcLaGdvabM) — **11:06**.
- [Andrew Ng — Random Initialization](https://www.youtube.com/watch?v=6by6Xas_Kho) — **7:58**.

**Self-check:** If rows are examples, `X` is `(N, d)` and a layer has `h` outputs: what shapes let you calculate `Z = XW + b`? What happens if every hidden unit starts with identical weights and biases?

**Numerical preparation:** Work **N5.1** in the [practice companion](numerical-practice.md#n51-shapes-and-parameter-counts). It checks matrix shapes, ten weights plus five biases in the handout network, and parameter counts for the assignment architecture.

### C. MNIST preprocessing, binary output, and the training workflow

**Source:** Assignment 1, pages 1–4.

**Study**

- Flatten each `28×28` grayscale image to 784 input values and scale pixels to `[0,1]`.
- Encode **digit 0 as positive (`t=1`)** and every other digit as negative (`t=0`).
- Keep exactly one sigmoid output neuron and mean binary cross-entropy.
- Use the full training batch for each gradient-descent update, as the assignment specifies.
- Validate on a small 2D dataset with at least two configurations before training on MNIST.
- Save loss curves; compare at least two MNIST configurations and evaluate on the held-out test set.

**First watch:** Reuse [3Blue1Brown's digit-network explanation](https://www.youtube.com/watch?v=aircAruvnKk&t=162s) — **clip 2:42–8:38 · 5:56**, for pixel inputs and layers. Its example has ten digit outputs; **your assignment replaces those with one “0 versus not 0” sigmoid output**. Reuse §2.4's **8:00** batch-gradient lesson for the training update.

**Course connection:** The exact remapping and pixel scaling above come from the assignment. Follow those instructions after watching the conceptual videos. Keep a validation split within training data if you tune settings; preserve the test set for the required final evaluations.

**Optional implementation depth:** [Karpathy — Building micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0) — **2:25:52**. Excellent for understanding computational graphs and gradients. It builds automatic differentiation; your submission must implement the specified backward recursion with NumPy and **must not use an automatic-differentiation engine or framework layers/optimizers**. A dataset utility may only load the raw data. This resource teaches the mechanism rather than supplying an assignment-compatible implementation.

**Self-check:** Explain the full forward → loss → backward → update loop. Why can a ten-output tutorial or a mini-batch training loop require changes for this assignment?

### D. Confusion matrix, accuracy, precision, recall, and F1

**Source:** Assignment 1, pages 4–5.

**Study:** Identify TP, TN, FP, and FN using “digit is 0” as the positive class. Calculate all four requested metrics; explain why accuracy alone hides failure on the minority class.

**First watch:** [StatQuest — The Confusion Matrix](https://www.youtube.com/watch?v=Kdsp6soqA7o) — **7:12**; then [codebasics — Precision, Recall, F1 score, True Positive](https://www.youtube.com/watch?v=2osIZ-dSPGE) — **11:45**. The metric concepts transfer directly even though the latter belongs to a TensorFlow/Keras tutorial series.

**Quick reference:** [Google's classification-metrics lesson](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) explains the formulas and zero-denominator cases.

**Self-check:** If a model always predicts “not 0,” why might its accuracy look high while its recall for digit 0 is zero? What should your code do if it never predicts a positive and precision has a zero denominator?

**Numerical preparation:** Work **N5.2** in the [practice companion](numerical-practice.md#n52-confusion-matrix-and-classification-metrics): threshold eight probabilities, count all four cells, and calculate the metrics. Compare an all-negative predictor, then try fresh counts with checked answers.

**Submission checklist:** Runnable source plus the assignment's 2–4-page report, validation/training loss curves, test metrics, a confusion matrix for each tested configuration, and a short comparison. Follow the PDF's ZIP naming and submission instructions directly.

## A practical study route

| Session | Work through | Finish by doing |
| --- | --- | --- |
| 1 | Lecture 1; short explanations followed by its worked numerical video | Two checked multivariable updates, then a changed-value problem |
| 2 | Lecture 2, §§2.1–2.5 | Sigmoid, BCE, all gradients, and a two-example batch update |
| 3 | Lecture 2, §§2.6–2.11 | Weighted XOR/truth tables, K-map reduction, parity counts, and region/pulse constructions |
| 4 | Lecture 3, §§3.1–3.6 | An ordered perceptron trace and an explanation of empirical risk |
| 5 | Lecture 3, §§3.7–3.12; handout | A full two-hidden-layer forward/backward/update calculation, including every bias |
| 6 | Lecture 4 | Checked Hessian/Newton, convergence, RProp, momentum, and Nesterov calculations |
| 7 | Assignment support | Parameter counts and metrics by hand; then assignment implementation and experiments |

Treat these as flexible sessions. The watch time is not the total study time: pause to reproduce the mathematics. Before a quiz or midterm, use the [prerequisite check and numerical practice](numerical-practice.md), cover the solutions, and solve changed-value questions. You should be able to explain each step as well as calculate it. Worked-number lessons are part of this preparation; broader optional lectures remain optional.

## Selection and verification notes

- **Course coverage:** All four supplied lecture PDFs were inventoried, plus the handout and assignments; selected formula and diagram pages were also inspected visually. Repeated build sequences are grouped, and administrative pages and future-topic lists are identified separately. Course-specific proofs/constructions that lack an equally short video are explicitly marked and retain a slide-based exercise or written bridge.
- **Why these educators:** The core choices use 3Blue1Brown, StatQuest, Andrew Ng/DeepLearning.AI, Khan Academy, and established university teaching. The selected videos have substantial learner reach, positive engagement where visible, or direct institutional teaching use. This is a curated match to the course, not a numerical ranking of all available videos.
- **Reception evidence, checked 15 September 2026:** The official [3Blue1Brown neural-network video](https://www.youtube.com/watch?v=aircAruvnKk) had over 24 million views in public player metadata, with roughly 560,000 likes in the indexed YouTube page. [IBM's overview](https://www.youtube.com/watch?v=qYNweeDHiyU) had over 3.5 million views and roughly 76,000 indexed likes. The [DeepLearning.AI Neural Networks and Deep Learning course](https://www.coursera.org/learn/neural-networks-deep-learning) displayed **4.9/5 from over 123,000 reviews**; that is a **course-level rating**, not a rating of each free video. Counts change and indexed figures may lag.
- **Specialist choices:** [UNSW's tutorial](https://cgi.cse.unsw.edu.au/~cs9444/25T2/tut/COMP9444_Week1_Questions.html) assigns the compact perceptron videos. CMU's [Spring 2025](https://deeplearning.cs.cmu.edu/S25/), [Spring 2022](https://deeplearning.cs.cmu.edu/S22/), and [Fall 2020](https://deeplearning.cs.cmu.edu/F20/index.html) schedules establish the respective long-form topic matches. The focused RProp video is [linked by RProp co-inventor Martin Riedmiller](https://www.riedmiller.me/subprojects/rprop). These are useful teaching/provenance signals even when public popularity is lower.
- **Timing and links:** Exact YouTube runtimes were checked against public video metadata; UNSW's approximate times and some MIT/Khan times come from their course pages. Excerpts use published chapter boundaries or inspected calculation segments; the Stanford CS231n excerpts use YouTube's automatic chapter markers. The latter may benefit from a small rewind for context. Every video was not watched end to end. Playback can still vary by region or platform.
- **Numerical preparation:** Worked-video labels rely on inspected numerical content, creator transcripts, or the institution's worked-example description, rather than the title alone. Differences from the course's loss, activation, or optimizer convention are stated. Where a suitable matching walkthrough was not verified, the guide links a local worked example with a fresh retry. Arithmetic was checked programmatically, including all fifteen single-example and batch backpropagation gradients against finite differences. An independent agent reviewed conceptual and numerical readiness, and the original section authors made the revisions.

**Scope for the next update:** Extend this guide when later Deep Learning lecture files arrive, using their actual contents and preserving the short-first / optional-depth format.
