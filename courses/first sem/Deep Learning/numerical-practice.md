# Deep Learning — Numerical Practice for Quizzes and Midterms

Use this with the [support guide](support.md). These original practice problems develop skills in the supplied Lectures 1–5; they are **not past papers or a prediction of the exam syllabus**. Follow any scope and calculator rules announced by your instructor.

**Jump to:** [Prerequisites](#prerequisite-check) · [Lecture 1](#lecture-1--regression-and-batch-gradient-descent) · [Lecture 2](#l2--logistic-arithmetic-and-network-constructions) · [Lecture 3](#n3--learning-rules-and-a-complete-numerical-backpropagation-pass) · [Lecture 4](#n4-lecture-4--calculating-optimizer-updates) · [Assignment calculations](#assignment-related-calculation-practice) · [Lecture 5](#n6) · [Readiness check](#readiness-check-before-a-quiz-or-midterm)

## How to practise

1. Watch the relevant conceptual explanation once, then use the guide's **Numerical preparation** video or written calculation bridge. Pause before the instructor reveals each calculation.
2. Solve the worked problem yourself with the answer covered. Show the formula, substituted numbers, intermediate values, and final result.
3. Attempt the fresh **Try it** problem without looking at the solution. Explain why each operation is valid, not only how to calculate it.
4. Check the answer and diagnose the first differing intermediate value. Reattempt later from a blank page.

Use natural logarithms for BCE and retain unrounded intermediate values; printed answers are rounded. A correct method with a small rounding difference is different from an incorrect sign, missing bias, or duplicated averaging factor. Unless a question says otherwise, calculate all gradients from the old parameters and update simultaneously.

## Prerequisite check

Try these before a full neural-network calculation. If one is unfamiliar, use the named support-guide section before continuing.

| Skill | Quick question | Refresher |
| --- | --- | --- |
| Weighted sum and bias | Evaluate `[1,−2]·[3,4] + 0.5`. | §§1.6, 3.10 |
| Exponentials and natural logs | Find `σ(0)` and `−ln(σ(0))`. | §§2.1–2.2 |
| Partial derivatives | For `f(x,y)=2x²+3xy`, find both partials at `(1,2)`. | §3.7 |
| Matrix shapes | If `X` is `4×3`, `W` is `3×2`, and `b` is `1×2`, what is the shape of `XW+b`? How many trainable numbers are in `W,b`? | Assignment support B |
| Boolean logic | Evaluate `A AND NOT B` at `(A,B)=(1,0)` and `(1,1)`. | §§2.6–2.8 |
| Eigenvalues and a quadratic | For Hessian `diag(2,8)`, give its eigenvalues and the fixed learning-rate convergence interval for gradient descent on a positive-definite quadratic. | §§3.8, 4.4 |

<details>
<summary>Prerequisite answers</summary>

Weighted sum **−4.5**. Sigmoid **0.5** and negative log **0.693147**. Partials `∂f/∂x=4x+3y=10` and `∂f/∂y=3x=3`. Output shape **4×2**; parameters **8**. Boolean outputs **1, 0**. Eigenvalues **2, 8**; convergence interval **`0<α<0.25`** for the stated quadratic. Matrix multiplication is not elementwise multiplication.

</details>

## Lecture 1 — Regression and batch gradient descent

### N1.1 Two-feature regression: two batch updates

**Pairs with:** support §§1.4–1.6. **Worked video:** [StatQuest — Gradient Descent, Step-by-Step](https://www.youtube.com/watch?v=sDv4f4s2SB8) — **23:54**. The numerical sections are **5:38–14:48** for one variable and **15:48–21:55** for multiple parameters; the first span includes a short explanatory aside at 9:08–9:40. It demonstrates derivative evaluation and repeated parameter updates. Its summed squared-error scaling must be translated to the course's **half-mean-squared-error** formula below.

**Given:** two training examples `(x₁,x₂,t) = (1,0,2)` and `(0,2,1)`, `ŷ = w₁x₁+w₂x₂+b`, initial `(w₁,w₂,b)=(0,0,0)`, learning rate `α=0.1`, and

`J = (1/(2m)) Σ(ŷ−t)²`, with `m=2`.

**Task:** Compute the loss, all three gradients, and two simultaneous batch updates.

**Worked solution — first update**

1. Predictions are `(0,0)` and residuals `e=ŷ−t` are `(-2,-1)`.
2. `J₀ = [(-2)²+(-1)²]/4 = 1.25`.
3. `∂J/∂w₁ = [(-2)(1)+(-1)(0)]/2 = -1`.
4. `∂J/∂w₂ = [(-2)(0)+(-1)(2)]/2 = -1`.
5. `∂J/∂b = (-2-1)/2 = -1.5`.
6. Update together: `(w₁,w₂,b) = (0.1,0.1,0.15)`.
7. Recompute predictions using those new parameters: `(0.25,0.35)`; residuals `(-1.75,-0.65)` and `J₁ = (3.0625+0.4225)/4 = 0.87125`.

**Second update:** The gradients at the new point are `(-0.875,-0.65,-1.2)`. The next parameters are `(0.1875,0.165,0.27)`.

| Iteration, after this many updates | `w₁` | `w₂` | `b` | Predictions | Loss at these parameters |
| --- | ---: | ---: | ---: | --- | ---: |
| 0 | 0 | 0 | 0 | `(0,0)` | 1.25000000 |
| 1 | 0.1000 | 0.1000 | 0.1500 | `(0.25,0.35)` | 0.87125000 |
| 2 | 0.1875 | 0.1650 | 0.2700 | `(0.4575,0.6000)` | 0.63482656 |

**Explain:** Why is the loss denominator `4` but the gradient denominator `2`? Differentiating the square contributes a factor of two that cancels the `1/2`. If the loss were plain MSE, all gradients would be twice as large. The same numeric learning rate would then produce different updates.

**Common mistakes:** Using `t−ŷ` while still subtracting the gradient; forgetting the bias; evaluating the second gradient after updating the first weight; reporting the old loss alongside the new parameters without labeling it.

**Try it:** Use examples `(1,1,3)` and `(2,0,2)`, initial `(w₁,w₂,b)=(0.5,-0.5,0)`, `α=0.1`, and the same half-MSE definition. Compute one update. Before calculating, predict whether the bias will rise or fall.

<details>
<summary>Check your answer</summary>

Predictions `(0,1)`; residuals `(-3,-1)`; `J=2.5`; gradients `(-2.5,-1.5,-2)`. New parameters are **`(0.75,-0.35,0.2)`**. The bias rises because the mean residual is negative: predictions are too small on average.

</details>

### N1.2 Explain the setup without calculating

For the regression problem above, identify the task, experience, performance measure, features, targets, predictions, and trainable parameters. Explain why two decreasing training losses do not prove good predictions on new data.

<details>
<summary>Check your explanation</summary>

The task is predicting a real-valued target; experience is the labeled training examples. A suitable performance measure is held-out prediction error under a stated loss. The features are `(x₁,x₂)`, targets are `t`, predictions are `ŷ`, and parameters are `(w₁,w₂,b)`. The loss table measures fit to these two training samples; it gives no direct evidence about unseen inputs.

</details>

## L2 — Logistic arithmetic and network constructions

Use this with [Lecture 2 support](support.md#lecture-2--logistic-regression-and-what-networks-can-represent). The numbers below are new practice examples. Use natural logarithms, retain unrounded values internally, and report six decimal places. A batch cost is the **mean** of its example losses. Every gradient in an update is evaluated at the same old parameters.

### L2.1 — One sigmoid/BCE example, then a two-example batch

**Worked example.** Start with `w=(0.2,−0.3)`, `b=0.1`, learning rate `α=0.1`. First use only `x=(1,2), t=1`.

1. `z=0.2(1)−0.3(2)+0.1=−0.3`.
2. `p=σ(−0.3)=0.425557`; at threshold `p≥0.5` predict 0, incorrectly.
3. `ℒ=−ln(p)=0.854355`.
4. `dℒ/dp=−1/p`; `dp/dz=p(1−p)`. Their product is `δ=dℒ/dz=p−t=−0.574443`.
5. `dw1=δx1=−0.574443`, `dw2=δx2=−1.148885`, `db=δ=−0.574443`.
6. Update together: `w'=(0.257444,−0.185111)`, `b'=0.157444`.
7. Re-evaluate: `z'=0.044666`, `p'=0.511165`, `ℒ'=0.671064`.

**Now reset to the original parameters** and add `x=(−1,1), t=0`. This is one batch update, not a continuation of the single-example update.

| Example | z | p | BCE loss | δ=p−t | δx1 | δx2 | Bias contribution |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `(1,2), t=1` | −0.300000 | 0.425557 | 0.854355 | −0.574443 | −0.574443 | −1.148885 | −0.574443 |
| `(−1,1), t=0` | −0.400000 | 0.401312 | 0.513015 | 0.401312 | −0.401312 | 0.401312 | 0.401312 |
| Mean | — | — | **0.683685** | — | **−0.487877** | **−0.373786** | **−0.086565** |

For the second row, `ℒ=−ln(1−p)` and `dw1=0.401312×(−1)`. Average each gradient column once, then update:

`w'=(0.248788,−0.262621)`, `b'=0.108657`.

| Recomputed at the new parameters | z' | p' | BCE loss |
| --- | ---: | ---: | ---: |
| First example | −0.167798 | 0.458149 | 0.780562 |
| Second example | −0.402753 | 0.400651 | 0.511912 |
| Mean | — | — | **0.646237** |

**Checks that prevent common errors:** These `δ` values differentiate each example's loss. Average the parameter gradients once; do not also divide these deltas by two. Do not multiply `p−t` by another sigmoid derivative. If you use `log10` instead of `ln`, the loss **and all its derivatives** are divided by `ln(10)`; silently combining base-10 loss with the unscaled `p−t` gradient is inconsistent.

**Try it unaided.** Reset to `w=(0.1,0.2)`, `b=−0.1`, `α=0.1`. Use the batch `((2,−1),t=0)` and `((0,1),t=1)`. Calculate both forward rows, all three averaged gradients, the simultaneous update, and the new mean BCE.

<details>
<summary>Check the changed-value batch</summary>

| Example | z | p | Loss | δ | δx1 | δx2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| First | −0.100000 | 0.475021 | 0.644397 | 0.475021 | 0.950042 | −0.475021 |
| Second | 0.100000 | 0.524979 | 0.644397 | −0.475021 | 0 | −0.475021 |

`dw=(0.475021,−0.475021)`, `db=0`. Updated `w=(0.052498,0.247502)`, `b=−0.1`. New scores `−0.242506, 0.147502`; probabilities `0.439669, 0.536809`; losses `0.579227, 0.622113`; **mean 0.600670**. Both old predictions were already correct, yet BCE and gradients were nonzero: classification correctness and probability fit are different.

</details>

### L2.2 — Evaluate and differentiate the course computation graph

For `J=3(a+bc)` at `(a,b,c)=(5,3,2)`, evaluate `u=bc=6`, `v=a+u=11`, `J=3v=33`.

Going backward: `dJ/dv=3`; `dv/da=dv/du=1`, so `dJ/da=dJ/du=3`. Then `du/db=c=2` and `du/dc=b=3`, giving **`(dJ/da,dJ/db,dJ/dc)=(3,6,9)`**. No learning rate is involved: this exercise evaluates derivatives, not an update.

**Try it:** Use `(a,b,c)=(2,−1,4)`. Give all intermediate values and all three input derivatives.

<details>
<summary>Check the graph retry</summary>

`u=−4`, `v=−2`, `J=−6`; derivatives **`(3,12,−3)`**. The negative derivative with respect to `c` comes from the negative multiplier `b`, not from the sign of `J` alone.

</details>

### L2.3 — Gates and two different XOR architectures

**Convention:** `H(s)=1` when `s≥0`, otherwise 0; a threshold unit is `H(wᵀx−T)` with bias `−T`. The integer thresholds on PDF pages 54 and 58 require the inclusive comparison to reproduce the labeled gates. Boolean examples below use half-integer thresholds where possible so no input lands on a tie. This is separate from the choice of tie convention in a perceptron *learning* algorithm.

| Gate | Weights | Threshold T | Bias |
| --- | --- | ---: | ---: |
| AND(x,y) | `(1,1)` | 1.5 | −1.5 |
| OR(x,y) | `(1,1)` | 0.5 | −0.5 |
| NOT(x) | `−1` | −0.5 | 0.5 |
| Majority of three | `(1,1,1)` | 1.5 | −1.5 |

| x | y | AND | OR | NOT(x) | XOR |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 |

| xyz | Sum | Majority |
| --- | ---: | ---: |
| 000 | 0 | 0 |
| 001 | 1 | 0 |
| 010 | 1 | 0 |
| 011 | 2 | 1 |
| 100 | 1 | 0 |
| 101 | 2 | 1 |
| 110 | 2 | 1 |
| 111 | 3 | 1 |

**Three-perceptron module with adjacent-layer connections:** Let `hOR=H(x+y−0.5)`, `hAND=H(x+y−1.5)`; output `H(hOR−2hAND−0.5)`. This uses two hidden units plus one output unit, six weighted connections and three biases: nine parameters if all are counted. Its computational depth is two.

**Two-perceptron architecture on page 58, with direct input-to-output connections:** Use the slide's integer thresholds: `h=H(x+y−2)`; output `H(x+y−2h−1)`. Here the output receives `x`, `y`, **and** `h`. Five weighted connections plus two thresholds/biases give seven parameters. The longest input-to-output path still has depth two.

| xy | hOR | hAND | Three-unit output score | h (page 58) | Page-58 output score | Both outputs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 00 | 0 | 0 | −0.5 | 0 | −1 | 0 |
| 01 | 1 | 0 | 0.5 | 0 | 0 | 1 |
| 10 | 1 | 0 | 0.5 | 0 | 0 | 1 |
| 11 | 1 | 1 | −1.5 | 1 | −1 | 0 |

The zero output scores in the middle rows explain why page 58 needs `≥`. The two diagrams compare permitted connections; **three neurons is not an architecture-independent minimum for XOR**.

**Try it:** Implement “at least three of four inputs are 1,” and NAND of two inputs, using half-integer thresholds. Explain their outputs at the boundary Boolean sums.

<details>
<summary>Check the gate retry</summary>

At-least-three: weights `(1,1,1,1)`, `T=2.5`, bias `−2.5`; sums 0–2 give 0, sums 3–4 give 1. NAND: weights `(−1,−1)`, `T=−1.5`, bias `1.5`; scores for `00,01,10,11` are `1.5,0.5,0.5,−0.5`, giving `1,1,1,0`.

</details>

### L2.4 — A truth table, negative literals, and a reducible K-map

**Problem:** For inputs `(A,B,C)`, set `F=1` on `001,011,100,101` and 0 elsewhere. The canonical DNF is:

`F=(¬A∧¬B∧C)∨(¬A∧B∧C)∨(A∧¬B∧¬C)∨(A∧¬B∧C)`.

Negative literals do not require separate NOT neurons: a negative input weight and suitable threshold encode them directly.

| Hidden unit's true row | Weights for `(A,B,C)` | T |
| --- | --- | ---: |
| 001 | `(−1,−1,1)` | 0.5 |
| 011 | `(−1,1,1)` | 1.5 |
| 100 | `(1,−1,−1)` | 0.5 |
| 101 | `(1,−1,1)` | 1.5 |

Each unit fires only for its assigned row. For example, the 011 unit's score at 011 is `0+1+1−1.5=0.5`; changing any one bit lowers it by one. OR the four hidden activations with output weights `(1,1,1,1)` and `T=0.5`.

Now put the function into a K-map. Consecutive columns differ in exactly one bit, including the first/last-column wraparound:

| A \ BC | 00 | 01 | 11 | 10 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0 | **1** | **1** | 0 |
| 1 | **1** | **1** | 0 | 0 |

Group the two adjacent true cells in row `A=0`: `B` changes, leaving `¬A∧C`. Group the two in row `A=1`: `C` changes, leaving `A∧¬B`. Thus **`F=(¬A∧C)∨(A∧¬B)`**. Each group has a power-of-two size; diagonal cells cannot form a pair.

The reduced network is `h1=H(−A+C−0.5)`, `h2=H(A−B−0.5)`, `F=H(h1+h2−0.5)`.

| ABC | h1 | h2 | F |
| --- | ---: | ---: | ---: |
| 000 | 0 | 0 | 0 |
| 001 | 1 | 0 | 1 |
| 010 | 0 | 0 | 0 |
| 011 | 1 | 0 | 1 |
| 100 | 0 | 1 | 1 |
| 101 | 0 | 1 | 1 |
| 110 | 0 | 0 | 0 |
| 111 | 0 | 0 | 0 |

**Count what is being counted:** Canonical/reduced DNF have 12/4 literal occurrences and 4/2 hidden units. Including output gives 5/3 computational units. A dense `3→4→1` stores **21 parameters** including biases; dense `3→2→1` stores **11**, including its zero weights. If absent edges are omitted, the reduced sparse construction has six nonzero connections plus three biases, **nine parameters**. A zero-valued stored weight is still a parameter of a dense layer.

**Try it:** Use true rows `010,011,101,111`. Draw the same K-map, reduce the DNF, and give two hidden perceptrons and an OR output.

<details>
<summary>Check the K-map retry</summary>

Rows in Gray order are `A=0: 0,0,1,1` and `A=1: 0,1,1,0`. Horizontal pairs give **`F=(¬A∧B)∨(A∧C)`**. One answer is `h1=H(−A+B−0.5)`, `h2=H(A+C−1.5)`, `F=H(h1+h2−0.5)`. The four true inputs produce hidden outputs `10,10,01,01`; the other rows produce `00`.

</details>

### L2.5 — Parity: compare specified constructions

Odd parity outputs 1 for an odd number of true inputs. Its three-input K-map is:

| A \ BC | 00 | 01 | 11 | 10 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 |

Flipping one input changes parity. Every horizontal/vertical neighbor has the opposite output, so there are no true pairs to merge: four canonical DNF terms remain.

**Eight-input worked count.** Exactly half the `2⁸=256` input rows have odd parity. The displayed DNF construction therefore has **128 hidden units**, **129 total computational units**, and depth two. A balanced binary tree needs **seven two-input XOR modules** (`4+2+1`). Using the three-perceptron module in §L2.3 gives **21 perceptrons**, with **six computational layers** (`2×log₂8`). Inputs have depth zero. In that sparse modular implementation there are `7×6=42` weighted connections and 21 biases, 63 parameters. A dense `8→128→1` stores `8×128+128+128+1=1281` parameters including biases.

These are **construction-specific counts**, not a lower bound for every threshold circuit. For a non-power-of-two input count, an uneven balanced tree can have depth at most `2⌈log₂N⌉` using these two-layer modules; do not report a fractional layer count. Depth does not make every Boolean function compact: the slide's circuit lower bounds and Shannon counting argument retain their gate/model assumptions.

**Try it:** Repeat the DNF-versus-three-unit-XOR-tree comparison for four inputs: hidden/total units, modules, computational depth, sparse tree parameters, and dense DNF parameters.

<details>
<summary>Check the parity retry</summary>

DNF: **8 hidden, 9 total, depth 2**, `4×8+8+8+1=49` dense parameters. Tree: **3 XOR modules, 9 total perceptrons, depth 4**, 18 weighted connections plus 9 biases = **27** sparse parameters. Equal neuron totals here do not imply equal connections or depth.

</details>

### L2.6 — Construct regions and sum two pulses

**Closed rectangle** `1≤x≤3, 0≤y≤2`. Using inclusive `H`, define:

| Hidden test | Weights `(x,y)` | Bias | Meaning |
| --- | --- | ---: | --- |
| `h1=H(x−1)` | `(1,0)` | −1 | x≥1 |
| `h2=H(3−x)` | `(−1,0)` | 3 | x≤3 |
| `h3=H(y)` | `(0,1)` | 0 | y≥0 |
| `h4=H(2−y)` | `(0,−1)` | 2 | y≤2 |

AND them using `R1=H(h1+h2+h3+h4−3.5)`. If the number of satisfied tests is `0,1,2,3,4`, the output is respectively `0,0,0,0,1`: this specifies all 16 binary combinations of the four tests.

| Point | `(h1,h2,h3,h4)` | R1 |
| --- | --- | ---: |
| `(2,1)` | `(1,1,1,1)` | 1 |
| `(0,1)` | `(0,1,1,1)` | 0 |
| `(2,3)` | `(1,1,1,0)` | 0 |
| `(1,0)` | `(1,1,1,1)` | 1 |

For a second closed rectangle `5≤x≤6, 0≤y≤2`, replace the first two biases by `−5,6`, and form `R2` with the same AND rule. The union is **`U=H(R1+R2−0.5)`**. Its truth table for `R1R2=00,01,10,11` is `0,1,1,1`. Points `(2,1),(5.5,1),(4,1)` give region flags `(1,0),(0,1),(0,0)` and union outputs `1,1,0`. The final OR adds another computational layer to this particular region construction.

**Two scaled pulses.** With `H(0)=1`, the difference `H(x−a)−H(x−b)` is 1 on **`[a,b)`** and 0 elsewhere. Define

`f(x)=2[H(x)−H(x−1)]+0.5[H(x−1)−H(x−3)]`.

It has height 2 on `[0,1)` and height 0.5 on `[1,3)`. Combine the repeated boundary to implement it with three threshold hidden units: `h=(H(x),H(x−1),H(x−3))`, followed by a **linear**, unthresholded output with weights `(2,−1.5,−0.5)` and bias 0.

| x | −0.5 | 0 | 0.5 | 1 | 2 | 3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| f(x) | 0 | 2 | 2 | 0.5 | 0.5 | 0 |

The endpoint behavior is deliberate: at x=1 the first pulse ends and the second begins. This is a concrete approximation building block, not a proof that a fixed finite net exactly fits any function.

**Try it:** (a) Construct the closed rectangle `−1≤x≤1, 2≤y≤4` and classify `(−1,2),(0,3),(2,3)`. (b) Build a function of height 1.5 on `[−1,0)` and height 3 on `[0,2)`, zero elsewhere; give three hidden thresholds, output weights, and values at `−1,0,1,2`.

<details>
<summary>Check the region/pulse retry</summary>

(a) Hidden scores `x+1, 1−x, y−2, 4−y`; AND bias `−3.5`. Outputs **1,1,0**, including the lower-left corner because the rectangle is closed.

(b) Hidden units `H(x+1), H(x), H(x−2)` and linear output weights **`(1.5,1.5,−3)`**, bias 0. Values at `−1,0,1,2` are **1.5,3,3,0**.

</details>

**L2 readiness:** Close these solutions and solve the changed-value batch plus one changed truth table and region construction. Explain the label encoding, threshold equality rule, averaging, and permitted network connections without referring to the examples.

## N3 — Learning rules and a complete numerical backpropagation pass

Use natural logarithms. Round displayed results to six decimal places but retain full precision while calculating. Examples are revision exercises, not predictions of examination questions. Try the questions before expanding solutions.

<a id="n3-1"></a>
### N3.1 Ordered perceptron updates

**Question.** Use signed labels `t∈{−1,+1}`, score `s=w₁x₁+w₂x₂+b`, and predict `+1` when `s≥0`, otherwise `−1`. Initialize `(w₁,w₂,b)=(0,0,0)`, learning rate `η=1`. Process A `(1,0),+1`, B `(0,1),−1`, C `(2,0),+1` in that order repeatedly. On a mistake, use `(w₁,w₂,b)←(w₁,w₂,b)+ηt(x₁,x₂,1)`. Stop after a whole pass with no errors. Record the old score, prediction, mistake status, and new parameters.

<details>
<summary>Worked trace</summary>

| Pass/example | Old score | Prediction | Mistake? | New `(w₁,w₂,b)` |
| --- | ---: | ---: | --- | --- |
| 1/A | 0 | +1 | No | `(0,0,0)` |
| 1/B | 0 | +1 | Yes | `(0,−1,−1)` |
| 1/C | −1 | −1 | Yes | `(2,−1,0)` |
| 2/A | 2 | +1 | No | `(2,−1,0)` |
| 2/B | −1 | −1 | No | `(2,−1,0)` |
| 2/C | 4 | +1 | No | `(2,−1,0)` |

For B, subtract the augmented input: `(0,0,0)−(0,1,1)=(0,−1,−1)`. For C, add `(2,0,1)`. The second pass has no mistakes, so stop. Equality uses the stated positive tie convention.

Do not substitute BCE's `0/1` targets into this signed-label update formula.

</details>

**Retry:** Reset to zero, use `η=0.5`, and change the order to **B,A,C**. Try a complete trace.

<details>
<summary>Retry answer</summary>

After B `(0,−0.5,−0.5)`, after A `(0.5,−0.5,0)`, after C unchanged. The next pass's B/A/C scores are `−0.5,0.5,1`; there are no mistakes. Order can change the separator found.

</details>

<a id="n3-2"></a>
### N3.2 Activation derivatives and a branching chain rule

**Question A.** Find the activation and derivative for sigmoid at `z=0`, softplus at `z=0`, ReLU at `z=2` and `z=−2`, and tanh when its output is `y=0.6`. If the upstream derivative is `∂L/∂y=2` for each, compute its pre-activation delta.

**Question B.** At `x=2`, let `u=x²`, `v=3x`, and `L=uv`. Find all values and both contributions to `dL/dx`. Then repeat at `x=−1`.

<details>
<summary>Answers with intermediate checkpoints</summary>

| Activation | Output | Local derivative | Delta when upstream derivative is 2 |
| --- | ---: | ---: | ---: |
| Sigmoid, `z=0` | 0.5 | `0.5(1−0.5)=0.25` | 0.5 |
| Softplus, `z=0` | `ln2=0.693147` | `sigmoid(0)=0.5` | 1 |
| ReLU, `z=2` | 2 | 1 | 2 |
| ReLU, `z=−2` | 0 | 0 | 0 |
| Tanh, output `0.6` | 0.6 | `1−0.6²=0.64` | 1.28 |

For B: `u=4`, `v=6`, `L=24`. Through `u`, the contribution is `(∂L/∂u)(du/dx)=v·2x=6·4=24`. Through `v`, it is `(∂L/∂v)(dv/dx)=u·3=4·3=12`. **Add them:** `dL/dx=36`. Direct check: `L=3x³`, derivative `9x²=36`.

At `x=−1`, `u=1`, `v=−3`, `L=−3`; contributions are `(−3)(−2)=6` and `1·3=3`, totaling `9`. A node used along several paths needs the sum of their derivative contributions.

</details>

**Activation retry:** For sigmoid output `0.8` with upstream derivative `−3`, find the local derivative and delta. Find the tanh derivative from output `−0.8`. What additional issue arises for ReLU at exactly zero?

<details>
<summary>Activation retry answers</summary>

Sigmoid derivative `0.16`, delta `−0.48`; tanh derivative `0.36`. ReLU at zero requires a declared convention; the mathematical derivative there does not exist.

</details>

<a id="n3-3"></a>
### N3.3 Gradient, Hessian, and stationary-point classification

**Question.** For `f(x,y)=x²+xy+2y²`, calculate the gradient and Hessian, locate the stationary point, and classify it. Compare the origin for `g=x²−y²` and `h=x⁴+y⁴`.

<details>
<summary>Worked answer and retry</summary>

`∇f=[2x+y, x+4y]ᵀ`. Setting both entries to zero gives `(x,y)=(0,0)`. The Hessian is `[[2,1],[1,4]]`, with eigenvalues `3−√2` and `3+√2`, both positive. Thus the origin is a strict local minimum (and, for this positive-definite quadratic, the global minimum).

For `g`, the Hessian `diag(2,−2)` is indefinite: the origin is a saddle. For `h`, the Hessian at the origin is zero, so the second-order test is inconclusive; nevertheless `x⁴+y⁴≥0`, with equality only at the origin, proves a strict minimum.

</details>

**Retry:** Find the gradient, Hessian, stationary point, and classification for `q=−x²−2y²`.

<details>
<summary>Retry answer</summary>

Gradient `[−2x,−4y]ᵀ`, Hessian `diag(−2,−4)`, and a strict maximum at the origin. Stationarity alone does not distinguish these cases.

</details>

<a id="n3-4"></a>
### N3.4 Full 2→2→2→1 sigmoid/BCE calculation

This matches the architecture and notation of [the backpropagation handout](Backpropagation_Derivation.pdf). Every computational neuron uses sigmoid. `wᵢ,ⱼ⁽ˡ⁾` sends previous-layer neuron `i` to current-layer neuron `j`; `w₀,ⱼ⁽ˡ⁾` is its bias from constant input `1`. Use input `x=(1,2)`, target `t=1`, and learning rate `η=0.1`.

| Layer | Source→destination weights | Bias weights |
| --- | --- | --- |
| Hidden 1 | `w₁,₁=0.1`, `w₁,₂=−0.2`, `w₂,₁=0.3`, `w₂,₂=0.2` | `w₀,₁=0`, `w₀,₂=0.1` |
| Hidden 2 | `w₁,₁=0.4`, `w₁,₂=−0.3`, `w₂,₁=−0.2`, `w₂,₂=0.2` | `w₀,₁=0.1`, `w₀,₂=−0.1` |
| Output 3 | `w₁,₁=0.3`, `w₂,₁=−0.4` | `w₀,₁=0.2` |

**Attempt:** Compute every `z` and `y`, the BCE `ℓ=−[t ln y+(1−t)ln(1−y)]`, all five deltas `δⱼ⁽ˡ⁾=∂ℓ/∂zⱼ⁽ˡ⁾`, all fifteen parameter gradients, a simultaneous update, and the new loss. Keep all parameters at their old values until the backward pass is complete.

<details>
<summary>Complete worked solution</summary>

**1. Forward pass.** Start with `y₁⁽⁰⁾=1`, `y₂⁽⁰⁾=2`.

| Neuron | Affine calculation | `z` | `y=sigmoid(z)` |
| --- | --- | ---: | ---: |
| Hidden 1, neuron 1 | `0.1·1+0.3·2+0` | 0.700000 | 0.668188 |
| Hidden 1, neuron 2 | `−0.2·1+0.2·2+0.1` | 0.300000 | 0.574443 |
| Hidden 2, neuron 1 | `0.4·y₁⁽¹⁾−0.2·y₂⁽¹⁾+0.1` | 0.252387 | 0.562764 |
| Hidden 2, neuron 2 | `−0.3·y₁⁽¹⁾+0.2·y₂⁽¹⁾−0.1` | −0.185568 | 0.453741 |
| Output | `0.3·y₁⁽²⁾−0.4·y₂⁽²⁾+0.2` | 0.187333 | 0.546697 |

`ℓ=−ln(0.5466967333)=0.603861`.

**2. Output delta.** Sigmoid+BCE cancels the sigmoid factor:

`δ₁⁽³⁾ = [(y−t)/(y(1−y))]·y(1−y) = y−t = −0.453303`.

Do not multiply this simplified output delta by `y(1−y)` again.

**3. Both second-hidden-layer deltas.**

`δ₁⁽²⁾ = (−0.4533032667)(0.3)(0.5627638384)(1−0.5627638384) = −0.033462`.

`δ₂⁽²⁾ = (−0.4533032667)(−0.4)(0.4537407133)(1−0.4537407133) = 0.044942`.

**4. Both first-hidden-layer deltas: add the downstream paths.**

`δ₁⁽¹⁾ = [0.4·(−0.0334620358) + (−0.3)·0.0449423133]·0.6681877722·(1−0.6681877722) = −0.005957`.

The two contributions inside the brackets are `−0.0133848143` and `−0.0134826940`; their sum is `−0.0268675083`. Omitting either path gives an incorrect gradient.

`δ₂⁽¹⁾ = [(−0.2)·(−0.0334620358) + 0.2·0.0449423133]·0.5744425168·(1−0.5744425168) = 0.003833`.

**5. All gradients and simultaneous updates.** For an ordinary edge, gradient = source activation × destination delta. For a bias edge, the source is `1`, so the gradient equals the delta. Example: `∂ℓ/∂w₂,₁⁽¹⁾ = 2·(−0.0059568725)=−0.0119137449`; new value `0.3−0.1·(−0.0119137449)=0.3011913745`.

| Parameter | Old value | Single-example gradient | Updated value |
| --- | ---: | ---: | ---: |
| `w1,1^(1)` | 0.100000 | -0.005957 | 0.100596 |
| `w1,2^(1)` | -0.200000 | 0.003833 | -0.200383 |
| `w2,1^(1)` | 0.300000 | -0.011914 | 0.301191 |
| `w2,2^(1)` | 0.200000 | 0.007667 | 0.199233 |
| `w₀,1^(1)` (bias) | 0.000000 | -0.005957 | 0.000596 |
| `w₀,2^(1)` (bias) | 0.100000 | 0.003833 | 0.099617 |
| `w1,1^(2)` | 0.400000 | -0.022359 | 0.402236 |
| `w1,2^(2)` | -0.300000 | 0.030030 | -0.303003 |
| `w2,1^(2)` | -0.200000 | -0.019222 | -0.198078 |
| `w2,2^(2)` | 0.200000 | 0.025817 | 0.197418 |
| `w₀,1^(2)` (bias) | 0.100000 | -0.033462 | 0.103346 |
| `w₀,2^(2)` (bias) | -0.100000 | 0.044942 | -0.104494 |
| `w1,1^(3)` | 0.300000 | -0.255103 | 0.325510 |
| `w2,1^(3)` | -0.400000 | -0.205682 | -0.379432 |
| `w₀,1^(3)` (bias) | 0.200000 | -0.453303 | 0.245330 |

Use the newly updated fifteen parameters for a **fresh** forward pass. The loss becomes **0.572599**, smaller than `0.603861`. This is a check for this specific step, not a guarantee for arbitrary learning rates.

</details>

<a id="n3-5"></a>
### N3.5 Two-example batch: average exactly once

**Question.** Reset all parameters to the original table in N3.4. Example A is `(x,t)=((1,2),1)`; example B is `((−1,1),0)`. Define `J=(ℓ_A+ℓ_B)/2`. Calculate both examples at the same original parameter state, average the parameter gradients, then make **one** update with `η=0.1`.

<details>
<summary>Batch solution and checkpoints</summary>

For B, hidden-1 `z=(0.2,0.5)`, `y=(0.549834,0.622459)`; hidden-2 `z=(0.195442,−0.140458)`, `y=(0.548705,0.464943)`; output `z=0.178634`, `y=0.544540`, `ℓ_B=0.786448`. Thus initial batch mean `J=0.695154`.

B's deltas: output `0.544540`; hidden 2 `(0.040453,−0.054186)`; hidden 1 `(0.008029,−0.004448)`.

Define `δ_{i,j}⁽ˡ⁾=∂ℓ_i/∂z_{i,j}⁽ˡ⁾` **per example**, then `∂J/∂w=(g_A+g_B)/2`. In particular, output bias gradients are `−0.4533032667` and `0.5445402310`, averaging to `0.0456184821`; the batch update is `0.2−0.1·0.0456184821=0.1954381518`.

| Parameter | Gradient A | Gradient B | Mean gradient | Batch-updated value |
| --- | ---: | ---: | ---: | ---: |
| `w1,1^(1)` | -0.005957 | -0.008029 | -0.006993 | 0.100699 |
| `w1,2^(1)` | 0.003833 | 0.004448 | 0.004141 | -0.200414 |
| `w2,1^(1)` | -0.011914 | 0.008029 | -0.001943 | 0.300194 |
| `w2,2^(1)` | 0.007667 | -0.004448 | 0.001609 | 0.199839 |
| `w₀,1^(1)` (bias) | -0.005957 | 0.008029 | 0.001036 | -0.000104 |
| `w₀,2^(1)` (bias) | 0.003833 | -0.004448 | -0.000307 | 0.100031 |
| `w1,1^(2)` | -0.022359 | 0.022242 | -0.000058 | 0.400006 |
| `w1,2^(2)` | 0.030030 | -0.029793 | 0.000118 | -0.300012 |
| `w2,1^(2)` | -0.019222 | 0.025180 | 0.002979 | -0.200298 |
| `w2,2^(2)` | 0.025817 | -0.033729 | -0.003956 | 0.200396 |
| `w₀,1^(2)` (bias) | -0.033462 | 0.040453 | 0.003495 | 0.099650 |
| `w₀,2^(2)` (bias) | 0.044942 | -0.054186 | -0.004622 | -0.099538 |
| `w1,1^(3)` | -0.255103 | 0.298792 | 0.021845 | 0.297816 |
| `w2,1^(3)` | -0.205682 | 0.253180 | 0.023749 | -0.402375 |
| `w₀,1^(3)` (bias) | -0.453303 | 0.544540 | 0.045618 | 0.195438 |

A fresh forward pass on **both** examples gives new batch mean **0.694835**. The update must start from the original table, not the single-example-updated parameters in N3.4.

If instead you define a delta as `∂J/∂z_i`, it already contains `1/2`; sum its parameter contributions without another division by two. The assignment's `delta=prediction−target` followed by averaging gradients corresponds to the **per-example** convention above. Updating after A before calculating B would perform sequential SGD, not this full-batch step.

</details>

<a id="n3-6"></a>
### N3.6 Fresh full-network retry and readiness check

Reset to N3.4's original weights and keep input `(1,2)`, but change the target to **`t=0`**. Without looking at the worked backward solution, calculate all five deltas, all fifteen gradients, and one `η=0.1` update. Explain which cached forward values change, if any.

<details>
<summary>Retry answer key</summary>

The forward values do not change: targets enter the loss, not this feedforward prediction. `y=0.546697`, `ℓ=−ln(1−y)=0.791194`. Output delta is now `+0.546697`.

Deltas: hidden 1 `(0.007184, -0.004623)`; hidden 2 `(0.040356, -0.054202)`; output `0.546697`.

| Parameter | Gradient | Updated value |
| --- | ---: | ---: |
| `w1,1^(1)` | 0.007184 | 0.099282 |
| `w1,2^(1)` | -0.004623 | -0.199538 |
| `w2,1^(1)` | 0.014368 | 0.298563 |
| `w2,2^(1)` | -0.009246 | 0.200925 |
| `w₀,1^(1)` (bias) | 0.007184 | -0.000718 |
| `w₀,2^(1)` (bias) | -0.004623 | 0.100462 |
| `w1,1^(2)` | 0.026966 | 0.397303 |
| `w1,2^(2)` | -0.036217 | -0.296378 |
| `w2,1^(2)` | 0.023182 | -0.202318 |
| `w2,2^(2)` | -0.031136 | 0.203114 |
| `w₀,1^(2)` (bias) | 0.040356 | 0.095964 |
| `w₀,2^(2)` (bias) | -0.054202 | -0.094580 |
| `w1,1^(3)` | 0.307661 | 0.269234 |
| `w2,1^(3)` | 0.248059 | -0.424806 |
| `w₀,1^(3)` (bias) | 0.546697 | 0.145330 |

Every gradient is the old N3.4 gradient multiplied by `0.5466967333/(−0.4533032667)`. That shortcut is an answer check here because the same input, same parameters, same cached activations, and a single output leave every hidden derivative factor unchanged. It is not a substitute for practicing the chain rule.

**Ready for another problem when:** you can recover the five deltas, both downstream contributions at hidden layer 1, all bias gradients, and the correct old-state update without referring to the solution; and can explain the difference between per-example and mean-batch derivatives. Correct arithmetic alone is insufficient if you cannot explain the loss/activation assumptions.

</details>

**Verification:** The numerical key was calculated at full precision and checked using independent central finite differences of the scalar loss for all fifteen parameters, including the two-example objective. Maximum absolute discrepancies were below `9×10⁻¹¹`. This is a check of the educational answer key; complete Assignment 1 under its own manual-backpropagation requirements.

## N4. Lecture 4 — Calculating optimizer updates

Use these problems after the conceptual videos in [Lecture 4](support.md#lecture-4--optimization-making-learning-converge). These are original practice problems aligned with the supplied slides, not predictions of quiz questions. Write the gradient, evaluation point, and update before substituting numbers. Keep unrounded values internally; displayed decimals are rounded.

### N4.1 Why the loss changes the saturation calculation

**Slide connection:** Lecture 4 pp8–26; compare the BCE handout.

Let `p = sigmoid(z) = 0.01` and target `t = 1`: the prediction is confidently wrong. For one example:

| Loss | Derivative with respect to the logit `z` | Numerical substitution |
| --- | --- | --- |
| Half-squared-error `L = (p−t)²/2` | `(p−t)p(1−p)` | `(-0.99)(0.01)(0.99) = −0.009801` |
| BCE `L = −t ln p − (1−t) ln(1−p)` | `p−t` | `0.01−1 = −0.99` |

Both derivatives come from backpropagation. The small sigmoid derivative suppresses the first gradient; it cancels algebraically in sigmoid+BCE. Thus the sigmoid/L2 spoiler example does not show that every use of backpropagation has this exact failure. Other causes of vanishing gradients or poor optimization can still remain. For a weight feeding this output, multiply the logit derivative by its input; for the output bias, use it directly.

**Try:** Set `p = 0.9`, `t = 0`. Find both logit derivatives, then the corresponding weight gradients for input `x = 2`.

<details>
<summary>Check N4.1</summary>

Half-squared-error: `0.9×0.9×0.1 = 0.081`; BCE: `0.9`. Weight gradients: `0.162` and `1.8`. Do not multiply the already simplified BCE derivative by another sigmoid derivative.

</details>

### N4.2 Scalar convergence: distinguish parameter error from loss

**Slide connection:** pp31–36. **Worked-number video:** reuse [StatQuest's iterative gradient-descent example](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=580s), **9:40–14:48 · 5:08**; the stability calculation below is the course-specific bridge.

Let `E(w) = 2(w−1)²`, so `a = 4`, `g(w) = 4(w−1)`, and start at `w₀ = 3`. With fixed learning rate `α`,

`wₖ₊₁ = wₖ − αg(wₖ)` and `eₖ₊₁ = (1−4α)eₖ`, where `eₖ = wₖ−1`.

Iteration `0` is initialization; iteration `1` is after one update. For example, with `α = 0.1`, `g(w₀)=8`, `w₁=3−0.1×8=2.2`, then `g(w₁)=4.8`, `w₂=2.2−0.1×4.8=1.72`.

| `α` | Signed error factor `r = 1−4α` | `w₀ → w₁ → w₂` | `E₀ → E₁ → E₂` | Behavior |
| --- | --- | --- | --- | --- |
| `0.1` | `0.6` | `3 → 2.2 → 1.72` | `8 → 2.88 → 1.0368` | Monotone convergence |
| `0.25` | `0` | `3 → 1 → 1` | `8 → 0 → 0` | Exact minimum after one step |
| `0.4` | `−0.6` | `3 → −0.2 → 1.72` | `8 → 2.88 → 1.0368` | Alternating convergence |
| `0.5` | `−1` | `3 → −1 → 3` | `8 → 8 → 8` | Nonshrinking oscillation |
| `0.6` | `−1.4` | `3 → −1.8 → 4.92` | `8 → 15.68 → 30.7328` | Divergence |

The **absolute parameter-error ratio** is `|r|`; the **loss ratio** is `r²` when the previous loss is nonzero. A negative `r` changes sides, not the sign of the nonnegative loss. Constant-factor error reduction is called linear convergence even though the error decreases geometrically with iteration count.

**Try:** For `E(w) = (w+2)²`, start `w₀ = 0`. Calculate two updates and losses for `α = 0.25` and `α = 0.75`. Explain why different paths can have identical losses.

<details>
<summary>Check N4.2</summary>

Here `a=2`, minimum `w*=−2`, initial error `2`, initial loss `4`. At `α=.25`, `r=.5`, the weights are `0, −1, −1.5`; at `α=.75`, `r=−.5`, they are `0, −3, −1.5`. Both loss sequences are `4, 1, .25`. Their absolute errors match; one path alternates sides. Both have error-magnitude ratio `.5` and loss ratio `.25`.

</details>

### N4.3 Hessian, eigenvalues, gradient descent, and Newton

**Slide connection:** pp37–53. Khan Academy and mathematicalmonk in the main guide supply concepts and derivation; this section supplies a complete two-variable numerical step. An additional genuine one-dimensional application is [Holistic Numerical Methods — Newton optimization example](https://www.youtube.com/watch?v=bOyy2Vlk6RY), **14:15**, solving a gutter-angle optimization problem. The [educational project's page](https://nm.mathforcollege.com/chapter-09-02-newtons-method-for-one-dimensional-optimization-example/) identifies it as the example lesson; it is an application outside neural networks and does not replace the mixed-term calculation below.

**Diagonal warm-up:** If `H = diag(1,100)`, the condition number is `100` and the stable fixed-rate interval is `0 < α < 0.02`. With `α=.01`, error factors in the two directions are `.99` and `0`: the steep quadratic direction finishes in one step while the flat one shrinks slowly.

**Mixed-term worked example:** Let `E(x,y) = 1.5x² + xy + 1.5y²`, starting at `w₀ = (2,0)`.

1. Differentiate: `g = (3x+y, x+3y)`, `H = [[3,1],[1,3]]`. The mixed term creates the off-diagonal entries.
2. Solve `det(H−λI) = (3−λ)²−1 = 0`: eigenvalues are `2` and `4`, so `H` is positive definite. Their directions are `(1,−1)` and `(1,1)` respectively; normalization of an eigenvector does not change its direction.
3. Condition number `κ=4/2=2`; fixed-rate convergence requires `0<α<2/4=.5` for this quadratic.
4. At `(2,0)`, `g=(6,2)`. Gradient descent with `α=.1` gives `(2,0)−.1(6,2)=(1.4,−.2)`. Loss changes from `6` to `2.72`.
5. Newton solves `HΔ=−g`: `3Δx+Δy=−6`, `Δx+3Δy=−2`. Eliminate `Δy` to obtain `Δx=−2`, `Δy=0`. Thus `w₁=w₀+Δ=(0,0)`, with loss `0`.

Newton finishes this positive-definite quadratic in one exact step because its local quadratic model is the entire function. General neural-network losses do not share that guarantee.

**Classification check:** `S(x,y)=(x²−y²)/2` has gradient zero at `(0,0)` and Hessian `diag(1,−1)`, so this point is a saddle. Its Hessian is invertible: invertibility alone does not imply a minimum. For `T(x,y)=x⁴+y⁴`, the Hessian at zero is zero and its second-order test is inconclusive, although inspecting `T≥0` establishes a minimum.

**Try:** Use `E(x,y)=2x²+xy+2y²`, `w₀=(1,−1)`, and gradient-descent rate `.1`. Find the gradient, Hessian, eigenvalues, condition number, stable-rate interval, one gradient step, and one Newton step.

<details>
<summary>Check N4.3</summary>

`g=(4x+y,x+4y)`, so `g₀=(3,−3)`; `H=[[4,1],[1,4]]`; eigenvalues `3,5`; `κ=5/3`; `0<α<.4`. Gradient descent gives `(.7,−.7)` and loss `1.47` from initial loss `3`. Newton solves `HΔ=(−3,3)` with `Δ=(−1,1)`, reaching `(0,0)` and loss `0`.

</details>

### N4.4 Learning-rate decay with the slide's exact indexing

**Slide connection:** p57. The slide calls `ηₖ=η₀/(k+1)` **linear decay** and `ηₖ=η₀/(k+1)²` **quadratic decay**; these are reciprocal schedules. Do not replace the first with subtraction of a fixed amount just because of its name.

Set `η₀=.12`, let `k=0` denote the first update, and use exponential decay `ηₖ=η₀ exp(−βk)` with `β=ln 2`.

| Update index `k` | Reciprocal linear | Reciprocal quadratic | Exponential |
| --- | --- | --- | --- |
| `0` | `.12` | `.12` | `.12` |
| `1` | `.06` | `.03` | `.06` |
| `2` | `.04` | `.013333…` | `.03` |
| `3` | `.03` | `.0075` | `.015` |

For example, quadratic `η₂=.12/(2+1)²=.12/9`. A plateau-triggered schedule instead waits for the stated trigger; reducing `.12` by a factor `.1` gives `.012`, while retaining the learned parameters. A second such reduction gives `.0012`.

**Try:** With `η₀=.2`, calculate all three schedules at `k=2`, using exponential `β=ln 4`.

<details>
<summary>Check N4.4</summary>

Reciprocal linear: `.2/3=.066666…`; reciprocal quadratic: `.2/9=.022222…`; exponential: `.2×4⁻²=.0125`. The symbol `β` here is a decay constant, separate from a momentum coefficient or RProp shrink factor.

</details>

### N4.5 RProp: keep the state when an attempted step is rejected

**Slide connection:** pp64–72. The Ryan Harris video is a path animation; it is not advertised here as a worked numerical trace of this particular algorithm.

Use the slides' simplified **rollback, shrink, retry** version. Store an accepted position `w`, its derivative `prevD`, and a positive step magnitude `s`. Write the signed quantity subtracted from the parameter as `Δ = sign(prevD)s`, so a trial is `w_trial=w−Δ`. If signs agree, accept the trial, replace `prevD` with its derivative, and grow `s`. If signs reverse, restore the old position, keep its `prevD`, shrink `s`, and retry from that position on the next attempt. Here a zero derivative means stop. Apply lower/upper bounds to **positive magnitudes**, then attach the sign; the slide's signed-Δ shorthand makes its min/max lines ambiguous for negative Δ.

Let `E(w)=(w−1)²/2`, so `g=w−1`. Initialize accepted `w=0`, `prevD=−1`, `s=.6`; growth `1.2`, shrink `.5`, magnitude bounds `.01≤s≤1`.

| Attempt | Accepted start | Signed `Δ` used | Trial and its derivative | Decision | State after decision: `w, prevD, next s` |
| --- | --- | --- | --- | --- | --- |
| `1` | `0` | `−.6` | `.6`, `−.4` | Same sign: accept and grow | `.6, −.4, .72` |
| `2` | `.6` | `−.72` | `1.32`, `+.32` | Reversal: rollback to `.6`, shrink | `.6, −.4, .36` |
| `3` | `.6` | `−.36` | `.96`, `−.04` | Retry succeeds: accept and grow | `.96, −.04, .432` |

The rollback in attempt 2 is `1.32 + (−.72) = .6`. Its next trial is `.6−(−.36)=.96`. The positive derivative at the rejected trial does **not** replace `prevD`, and the algorithm does not first take a new step from `1.32`. Attempts count trial moves, so a rejected attempt does not advance the accepted position. Other RProp variants use different reversal rules; reproduce the stated convention.

**Try:** Set `E(w)=w²/2`, accepted `w=1`, `prevD=1`, and `s=.7`, with the same factors and bounds. Trace four attempts, retaining the accepted state after each decision.

<details>
<summary>Check N4.5</summary>

| Attempt | Trial | Trial derivative | Decision | State after decision: `w, prevD, next s` |
| --- | --- | --- | --- | --- |
| `1` | `.3` | `.3` | Accept, grow | `.3, .3, .84` |
| `2` | `−.54` | `−.54` | Rollback, shrink | `.3, .3, .42` |
| `3` | `−.12` | `−.12` | Rollback again, shrink | `.3, .3, .21` |
| `4` | `.09` | `.09` | Accept, grow | `.09, .09, .252` |

On a separate bound check, growing `s=.9` gives `min(1.2×.9,1)=1`; shrinking `.015` gives `max(.5×.015,.01)=.01`. Attach the derivative sign only after computing this magnitude.

</details>

### N4.6 Momentum and Nesterov: two steps from the same state

**Slide connection:** pp75–93. The Ng and Stanford clips in the main guide explain gradient history and lookahead; the following is the numerical companion.

**Convention:** `vₖ` is a **signed parameter displacement**, not an averaged gradient. With current `wₖ` and previous displacement `vₖ`:

- Momentum: `gₖ=E′(wₖ)`, `vₖ₊₁=βvₖ−αgₖ`, `wₖ₊₁=wₖ+vₖ₊₁`.
- Nesterov: `qₖ=wₖ+βvₖ`, `gₖ=E′(qₖ)`, `vₖ₊₁=βvₖ−αgₖ`, `wₖ₊₁=wₖ+vₖ₊₁`.

The lookahead is only the gradient evaluation point. Do not add `βvₖ` a second time when updating the weight. This equals an unnormalized gradient accumulator after changing sign and scaling by `α`; an EMA definition with `(1−β)g` requires a corresponding rate conversion to obtain the same trajectory.

Set `E(w)=w²/2`, `w₀=2`, `v₀=0`, `α=.1`, `β=.9`. Here `E′(w)=w`.

| Method / update | Current `wₖ` | Old `vₖ` | Point for gradient | Gradient | New `vₖ₊₁` | New `wₖ₊₁` |
| --- | --- | --- | --- | --- | --- | --- |
| Momentum / 1 | `2` | `0` | `2` | `2` | `−.2` | `1.8` |
| Nesterov / 1 | `2` | `0` | `2` | `2` | `−.2` | `1.8` |
| Momentum / 2 | `1.8` | `−.2` | `1.8` | `1.8` | `−.36` | `1.44` |
| Nesterov / 2 | `1.8` | `−.2` | `1.8+.9(−.2)=1.62` | `1.62` | `−.342` | `1.458` |

For the last row, `v₂=.9(−.2)−.1(1.62)=−.342`, then `w₂=1.8−.342=1.458`. Plain gradient descent gives `2→1.8→1.62`. The momentum methods first differ on step 2 because the initial velocity is zero; this example does not establish that one method always wins.

**Try:** Change to `E(w)=w²`, `w₀=1`, `v₀=0`, `α=.1`, `β=.5`. Calculate two steps of plain gradient descent, momentum, and Nesterov, recording the second gradient evaluation point.

<details>
<summary>Check N4.6</summary>

The derivative is now `2w`. All first steps give `w₁=.8`; both momentum methods have `v₁=−.2`. Plain GD uses second gradient `1.6` and ends at `.64`. Momentum uses point `.8`, gradient `1.6`, and `v₂=.5(−.2)−.1(1.6)=−.26`, ending at `.54`. Nesterov looks ahead to `.8+.5(−.2)=.7`, uses gradient `1.4`, and `v₂=−.24`, ending at `.56`.

</details>

**Completion check:** Redo the changed-value problems without opening their answers. Explain the gradient evaluation point, rejection state, stability assumption, and loss scaling in words. Page 53's BFGS/L-BFGS/LM overview calls for understanding their central ideas; full derivations are optional depth, not additional numerical requirements inferred from these slides.

## Assignment-related calculation practice

These skills are useful for the supplied assignment. Inclusion here does not establish that they will be examined.

### N5.1 Shapes and parameter counts

**Given:** rows are examples. For one layer, `Yprev` has shape `N×d`, `W` has shape `d×h`, and `b` has shape `1×h`.

**Work through:** `Z = Yprev W + b` and `Y = g(Z)` both have shape `N×h`. If `D` contains unaveraged per-example preactivation deltas, then `dW = Yprevᵀ D/N` has shape `d×h`, `db = sum_rows(D)/N` has shape `1×h`, and the derivative passed toward the previous layer is `D Wᵀ`, shape `N×d`. The activation derivative is multiplied **elementwise** when forming the previous layer's deltas. Do not average again if `D` was already scaled by `1/N`.

| Network | Edge weights | Biases | Total trainable parameters |
| --- | ---: | ---: | ---: |
| `2→2→2→1` | `4+4+2 = 10` | `2+2+1 = 5` | **15** |
| `784→64→32→1` | `50176+2048+32 = 52256` | `64+32+1 = 97` | **52353** |

Input features are data, not trainable biases or weights. Counting computational neurons, connections, and trainable parameters answers three different questions.

**Try it:** For `3→4→2→1` and a batch of five examples, give each `W`, `b`, and activation shape, and the total parameter count.

<details>
<summary>Check your answer</summary>

Weights: **3×4, 4×2, 2×1**. Biases: **1×4, 1×2, 1×1**. Activations after each layer: **5×4, 5×2, 5×1**. Total `(3+1)4+(4+1)2+(2+1)1 = 16+10+3 = 29`. The input batch itself has shape **5×3**.

</details>

### N5.2 Confusion matrix and classification metrics

**Pairs with:** Assignment support D. [StatQuest — Confusion Matrix](https://www.youtube.com/watch?v=Kdsp6soqA7o) — **7:12**, shows counted examples; [codebasics — Precision, Recall, F1](https://www.youtube.com/watch?v=2osIZ-dSPGE) — **11:45**, works through example labels and metric calculation. For the assignment, **digit 0 means positive class `1`**.

**Given:** targets `t=[1,0,1,0,0,1,0,0]`, probabilities `p=[0.9,0.7,0.4,0.1,0.2,0.8,0.6,0.3]`, and predict `1` when `p≥0.5`.

**Task:** Threshold the outputs, form the confusion matrix, and calculate accuracy, precision, recall, and F1.

**Worked solution:** Predictions are `[1,1,0,0,0,1,1,0]`.

| Actual \ Predicted | Positive `1` | Negative `0` |
| --- | ---: | ---: |
| Positive `1` | TP = 2 | FN = 1 |
| Negative `0` | FP = 2 | TN = 3 |

- Accuracy: `(TP+TN)/8 = 5/8 = 0.625`.
- Precision: `TP/(TP+FP) = 2/4 = 0.5`.
- Recall: `TP/(TP+FN) = 2/3 ≈ 0.666667`.
- F1: `2TP/(2TP+FP+FN) = 4/7 ≈ 0.571429`.

**Compare with always predicting negative:** TP=0, FP=0, FN=3, TN=5. Accuracy is still **0.625**, but recall and F1 are **0**. Precision is **undefined** because its denominator is zero. Software may report zero under a declared convention; distinguish that convention from the mathematical fraction. The direct F1 denominator is nonzero in this example, so its zero value is well-defined.

**Try it:** With TP=6, TN=8, FP=2, FN=4, calculate all four metrics. Which two groups of examples appear in the precision and recall denominators?

<details>
<summary>Check your answer</summary>

Accuracy **0.7**, precision **0.75**, recall **0.6**, F1 **2/3 ≈ 0.666667**. Precision conditions on **predicted positives**; recall conditions on **actual positives**.

</details>

<a id="n6"></a>

## N6. Lecture 5 — Stochastic updates, adaptive optimizers, and regularization

**Pairs with:** [Lecture 5 support](support.md#lecture-5). N5 retains its assignment numbering; N6 is the new lecture's practice. The linked short videos teach concepts and formulas; these original worked examples supply numerical traces under explicit conventions. Use them for the instructor's announced scope, not as a prediction of questions. Keep full precision internally and round only displayed answers.

<a id="n6-1"></a>

### N6.1 Full batch, SGD order, mini-batches, and update counts

**Pages:** 6–39, 77–82. Use the constant-output model `ŷ=w` and per-example loss `ℓᵢ=(w−tᵢ)²/2`, with targets `[0,2,4,6]`, initial `w₀=0`, and rate `η=.1`. The full objective is the **mean** of these four losses. A single-example gradient is `w−tᵢ`; a batch gradient is their mean, evaluated at one current `w`.

| Method | Gradients used in order | Weight after each update | Updates in this epoch |
| --- | --- | --- | --- |
| Full batch | `(0−2−4−6)/4=−3` | `.3` | `1` |
| SGD, order `[0,2,4,6]` | `0, −2, −3.8, −5.42` | `0, .2, .58, 1.122` | `4` |
| SGD, reverse order | `−6, −3.4, −1.06, 1.046` | `.6, .94, 1.046, .9414` | `4` |
| Mini-batches `[0,2]`, `[4,6]` | `−1`, then `[(.1−4)+(.1−6)]/2=−4.9` | `.1, .59` | `2` |

For example, forward-order SGD's third update is `.2−.1(.2−4)=.58`. Full batch does not use intermediate changed weights inside its gradient average. SGD order matters because each gradient is evaluated after earlier updates. The paths do not prove that the same rate gives a fair or optimal comparison for all methods.

With `103` examples, batch size `20`, and **retaining the final partial batch**, one epoch has `ceil(103/20)=6` updates: sizes `20,20,20,20,20,3`. Average the last batch over **3**, not 20. Twenty epochs give 120 mini-batch updates, 2,060 single-example SGD updates, or 20 full-batch updates.

**Try it:** Use targets `[1,3]`, `w₀=0`, and `η=.2`. Calculate one full-batch update and one epoch of SGD in both orders. Separately, for 10 examples and batch size 4, state the batch sizes and the divisor for the last mean.

<details>
<summary>Check N6.1</summary>

Full-batch gradient `−2`, final `w=.4`. Forward SGD: gradients `−1,−2.8`, weights `.2,.76`. Reverse SGD: gradients `−3,−.4`, weights `.6,.68`. Batch sizes `4,4,2`; divide the last sum by 2. If a problem instead says to drop incomplete batches, the count changes: state that policy first.

</details>

<a id="n6-2"></a>

### N6.2 Step-size conditions, rate arithmetic, and equal-work comparisons

**Pages:** 40–59, 86. These are calculations using specified theoretical models, not measured convergence predictions.

**Step-size test:** For `ηₖ=c/kᵖ`, start at `k=1`, with `c>0`. The p-series test gives `Σηₖ=∞` when `p≤1` and `Σηₖ²<∞` when `2p>1`; together, `1/2<p≤1`. Thus `p=.75` and `p=1` pass both, `p=.5` fails the square-sum condition, and `p=2` fails the divergent-sum condition. Geometric decay `c(.9)ᵏ` has a finite total sum, so merely “shrinking rapidly” does not establish both conditions. Additional objective/noise/boundedness assumptions are still needed for a convergence theorem.

**Gap bounds:** Suppose a stated bound is `gapₖ≤2/k`, and the target is `gap≤.01`. It suffices that `k≥200`. If instead `gapₖ≤2(.8)ᵏ`, solve `.8ᵏ≤.005`: `k≥ceil(ln(.005)/ln(.8))=24`. The second method uses fewer updates under these stipulated bounds, but a full-gradient update over `T` examples costs roughly `T` example-gradient calculations.

**Page 86's mini-batch expression:** Start with `O(1/√(bk)+1/k)`. If total example evaluations are `M=bk`, substitution gives `O(1/√M+b/M)`. For a numerical illustration only, set the hidden coefficients to 1, `M=10,000`, and `b=25`: `k=400`, so the expression is `.01+.0025=.0125`. With `b=100`, `k=100`, it is `.01+.01=.02`. The leading stochastic term is the same at fixed `M`; the second term differs. Neither the big-O notation nor this arithmetic establishes the slide's blanket `√b` degradation in total sample work, and parallel hardware changes wall time again.

**Try it:** Which of `p=.4,.6,1,1.1` pass both sums? Under bounds `gap≤3/k` and `gap≤3(.5)ᵏ`, how many updates suffice for `gap≤.03`? Evaluate the illustrative mini-batch expression at `M=1600,b=16`.

<details>
<summary>Check N6.2</summary>

`.6` and `1` pass both. The inverse bound needs 100 updates. The geometric bound needs `ceil(ln(.01)/ln(.5))=7` updates: six give `.046875`, seven `.0234375`. For `M=1600,b=16`, `k=100`; expression `1/40+1/100=.035`. These comparisons assume the given constants and definitions of gap.

</details>

<a id="n6-3"></a>

### N6.3 Expected risk, variance, and the batch mean

**Pages:** 60–91. Freeze the parameters. Suppose a fresh example's loss is `D=1` or `D=3`, each with probability `.5`. Then `E[D]=2` and `Var(D)=[(1−2)²+(3−2)²]/2=1`.

For two **independent** draws, the possible pairs are `(1,1),(1,3),(3,1),(3,3)`, equally likely. Their means are `1,2,2,3`, so the mean is still 2 and its variance is `(1+0+0+1)/4=.5=1/2`. Its standard deviation is `√.5≈.707107`, not `.5`.

More generally, if single-example variance is 9, independent mini-batches of size 9 have mean-loss variance `9/9=1` and standard deviation 1. A mean of 100 independent examples has variance `.09` and standard deviation `.3`.

**Sampling caveat:** If the finite dataset consists of exactly `[1,3]` and we select both **without replacement**, the mean is always 2, so variance is zero. At a fixed parameter state, a uniform size-`b` subset of a fixed dataset of size `N` has variance `σ²_pop/b × (N−b)/(N−1)`, using the dataset variance with divisor `N`. Across training updates the parameters change; do not apply this frozen-parameter enumeration as a theorem about the entire training trajectory or the test error of the selected model.

**Try it:** Loss takes values `0` and `4` with equal probability. Calculate its mean/variance and those of the mean of four independent samples. What is the variance if the entire two-value dataset is selected without replacement?

<details>
<summary>Check N6.3</summary>

Single draw: mean 2, variance 4. Four independent samples: mean 2, variance 1, standard deviation 1. Taking both members of the fixed two-example dataset without replacement: variance 0. Unbiased risk estimation at each fixed parameter value does not make minimization on that same dataset an unbiased estimate of the selected model's test performance.

</details>

<a id="n6-4"></a>

### N6.4 Momentum and Nesterov over different mini-batches

**Pages:** 93–109. Use the same constant-output model and half-squared-error as N6.1. Batch A has targets `[1,3]`, so its mean gradient at `w` is `w−2`; batch B has `[-3,−1]`, so its mean gradient is `w+2`. Process A then B, starting `w₀=0`, signed displacement `v₀=0`, `η=.1`, `β=.5`.

Momentum: `vₜ=βvₜ₋₁−ηg_batch(wₜ₋₁)`, `wₜ=wₜ₋₁+vₜ`. Nesterov instead evaluates the **current batch** at `q=wₜ₋₁+βvₜ₋₁`. These are signed displacements; no extra `(1−β)` factor is used.

| Method / batch | Gradient point | Batch gradient | New displacement | New weight |
| --- | --- | --- | --- | --- |
| Both / A | `0` | `−2` | `.2` | `.2` |
| Momentum / B | `.2` | `2.2` | `.5(.2)−.1(2.2)=−.12` | `.08` |
| Nesterov / B | `.2+.5(.2)=.3` | `2.3` | `.5(.2)−.1(2.3)=−.13` | `.07` |

Keep the displacement between batches. Reset only the temporary gradient accumulator used to average the examples in each new batch. Every example in Nesterov's current batch uses the same lookahead parameters.

**Try it:** Replace A with targets `[0,2]` and B with `[2,4]`; retain every other setting. Calculate both two-update paths.

<details>
<summary>Check N6.4</summary>

Batch means are 1 and 3. Both start with gradient `−1`, displacement `.1`, weight `.1`. Momentum's second gradient is `.1−3=−2.9`, giving displacement `.34` and weight `.44`. Nesterov's lookahead is `.15`; its second gradient is `−2.85`, displacement `.335`, weight `.435`.

</details>

<a id="n6-5"></a>

### N6.5 RMS values and two-parameter RMSProp

**Pages:** 110–118. Page 114's coordinates are `x=[1,1,2,1,1.5]`, `y=[2.5,−3,2.5,−2,1.5]`. Their mean squares are `9.25/5=1.85` and `27.75/5=5.55`; RMS values are **1.360147** and **2.355844**. The larger second RMS suggests a smaller effective rate in that coordinate. This is RMS of the listed sequence; the recursive optimizer uses exponential weighting instead of this uniform average.

**Explicit optimizer convention:** At update `t`, use already averaged mini-batch gradient `gₜ` and elementwise operations:

`sₜ=γsₜ₋₁+(1−γ)gₜ²`, `wₜ=wₜ₋₁−ηgₜ/√(sₜ+ε)`.

The slides place `ε` inside the radical. Some implementations place it outside; state the choice before calculating. Here choose `γ=.5`, `η=.1`, `s₀=(0,0)`, `w₀=(1,1)`, and **ε=0 solely for these hand calculations**, whose denominators are all positive. This is not a recommendation to remove numerical stabilization from an implementation. The supplied gradients are `g₁=(2,4)`, `g₂=(2,−4)`; they are inputs to this optimizer-state exercise, not gradients to be rederived from a fixed quadratic.

| `t` | `gₜ` | `sₜ` | Quantity subtracted `ηgₜ/√sₜ` | `wₜ` |
| --- | --- | --- | --- | --- |
| `1` | `(2,4)` | `(2,8)` | `(.141421,.141421)` | `(.858579,.858579)` |
| `2` | `(2,−4)` | `(3,12)` | `(.115470,−.115470)` | `(.743109,.974049)` |

For the second coordinate at update 2: `s=.5(8)+.5(−4)²=12`; the square does not retain the negative sign, but the parameter update does. Averaging the signed gradients and then squaring would be a different operation.

**Try it:** From `w₀=(0,0),s₀=(0,0)`, use `g₁=(1,2),g₂=(−1,2)` with the same settings. Find both states and weights. Separately, with `s=4,ε=1`, compare `√(s+ε)` and `√s+ε`.

<details>
<summary>Check N6.5</summary>

`s₁=(.5,2)`, `w₁=(−.141421,−.141421)`. `s₂=(.75,3)`, second subtracted vector `(−.115470,.115470)`, so `w₂=(−.025951,−.256891)`. The two denominators are `√5≈2.236068` and `3`; the placement matters. A second moment is also not a Hessian entry or a centered variance.

</details>

<a id="n6-6"></a>

### N6.6 Adam: corrected moments and a sign-changing gradient

**Pages:** 119–124. Define `t=1,2,…` as the global update counter; keep it and the states across epochs. The slide symbols `δ,γ` correspond here to `β₁,β₂`.

`mₜ=β₁mₜ₋₁+(1−β₁)gₜ`, `vₜ=β₂vₜ₋₁+(1−β₂)gₜ²`.

`m̂ₜ=mₜ/(1−β₁ᵗ)`, `v̂ₜ=vₜ/(1−β₂ᵗ)`, `wₜ=wₜ₋₁−ηm̂ₜ/√(v̂ₜ+ε)`.

Use the slide's inside-radical convention, `w₀=1`, `m₀=v₀=0`, `β₁=.9`, `β₂=.999`, `η=.1`, and supplied gradients `g₁=2,g₂=−1`. As in N6.5, set **ε=0 only for this nonzero-denominator arithmetic example**. The usual original-Adam formula uses `√v̂ₜ+ε` instead; neither formula removes the base learning rate.

| `t` | `gₜ` | `mₜ` | `vₜ` | `m̂ₜ` | `v̂ₜ` | Quantity subtracted | `wₜ` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `2` | `.2` | `.004` | `2` | `4` | `.1` | `.9` |
| `2` | `−1` | `.08` | `.004996` | `.421053` | `2.499250` | `.026634` | `.873366` |

At update 2, `m=.9(.2)+.1(−1)=.08`; divide by `1−.9²=.19`. Similarly, `v=.999(.004)+.001(1)=.004996`; divide by `1−.999²=.001999`. The newest gradient is negative, but the first-moment history is still positive, so this update still subtracts a positive quantity. Bias correction compensates for zero initialization; `1−βᵗ` is not `(1−β)ᵗ`.

**Try it:** Retain every setting but supply gradients `−2,−2`. Calculate raw and corrected moments and both weights.

<details>
<summary>Check N6.6</summary>

Update 1: `m=−.2,v=.004,m̂=−2,v̂=4,w=1.1`. Update 2: `m=−.38,v=.007996`; denominators `.19,.001999`, so `m̂=−2,v̂=4,w=1.2`. The negative normalized step is subtracted, increasing the weight. Without bias correction, these first updates would use different ratios. For a nonzero-epsilon spot check, with `m̂=2,v̂=4,η=.1,ε=1`, inside-radical step is `.2/√5≈.089443`, outside-radical step is `.2/3≈.066667`.

</details>

<a id="n6-7"></a>

### N6.7 L2 regularization: objective, gradients, and weight decay

**Pages:** 125–143. Use `ŷ=w₁x₁+w₂x₂+b` with one example `x=(2,1),t=1`; initialize `w=(1,−2),b=.5`. Set `λ=.2`, rate `η=.1`, and objective `J=(ŷ−t)²/2 + (λ/2)(w₁²+w₂²)`. **Bias is unpenalized** in this exercise. For multiple examples, average the data-loss term; do not divide the regularizer by batch size under this stated convention.

1. Prediction `ŷ=2−2+.5=.5`, residual `r=−.5`.
2. Data loss `.125`; penalty `(.2/2)(1+4)=.5`; total `J=.625`.
3. Data weight gradient `rx=(−1,−.5)`; penalty gradient `λw=(.2,−.4)`; combined gradient `(−.8,−.9)`. Bias gradient is `r=−.5`.
4. Simultaneous update gives `w=(1.08,−1.91)`, `b=.55`.

Equivalently, `w_new=(1−ηλ)w−ηg_data=.98w−.1g_data`. The objective's lambda and the per-update shrinkage are distinct. Page 138's boxed `1−λ` only matches this derivation if its lambda is redefined to include `η`. In Adam, a penalty contributes to the gradient moments and adaptive scaling; that is generally different from a separately applied weight decay.

**Smoothness check:** For `σ(wx)` at `x=0`, slope is `wσ(0)(1−σ(0))=w/4`. Thus weights `.5` and `5` give slopes `.125` and `1.25`, matching page 133's steepness picture. This local scalar calculation is not a general theorem that deeper networks are smoother.

**Try it:** Set `w=(2,1),b=−1,x=(1,2),t=2,λ=.1,η=.1`, using the same objective and unpenalized bias. Find prediction, loss, all gradients, and the update.

<details>
<summary>Check N6.7</summary>

Prediction `3`, residual `1`, data loss `.5`, penalty `.25`, total `.75`. Weight gradient `(1,2)+(.2,.1)=(1.2,2.1)`; bias gradient `1`. Updated `w=(1.88,.79)`, `b=−1.1`; shrink factor is `.99`, not `.9`.

</details>

<a id="n6-8"></a>

### N6.8 Dropout: a complete masked pass and inference comparison

**Pages:** 144–158. Use one scalar input `x=1`, two ReLU hidden units, and a **linear, undropped output**:

`z₁=a₁x+c₁`, `z₂=a₂x+c₂`, `hⱼ=max(0,zⱼ)`, `dⱼ=Mⱼhⱼ`, `ŷ=u₁d₁+u₂d₂+b`.

Parameters are `(a₁,a₂,c₁,c₂,u₁,u₂,b)=(1,2,1,−1,3,−2,.5)`. Target `t=1`, loss `L=(ŷ−t)²/2`, learning rate `.01`, keep probability `q=.5`. Drop **hidden activations only**; inputs, output, and bias constants are not masked. For this standard-dropout pass fix mask `M=(1,0)`, and reuse it throughout backward computation.

**Forward:** `z=(2,1)`, `h=(2,1)`, masked `d=(2,0)`. Prediction `ŷ=3(2)−2(0)+.5=6.5`; residual `r=5.5`; loss `15.125`.

**Backward:** `∂L/∂uⱼ=r dⱼ`, `∂L/∂b=r`. Hidden preactivation deltas are `δⱼ=r uⱼ Mⱼ 1[zⱼ>0]`: `δ₁=5.5×3×1=16.5`, `δ₂=5.5×(−2)×0=0`. Then `∂L/∂aⱼ=δⱼx`, `∂L/∂cⱼ=δⱼ`. Use old output weights in these deltas.

| Parameter | Old value | Gradient | Value after simultaneous update |
| --- | --- | --- | --- |
| `a₁` | `1` | `16.5` | `.835` |
| `a₂` | `2` | `0` | `2` |
| `c₁` | `1` | `16.5` | `.835` |
| `c₂` | `−1` | `0` | `−1` |
| `u₁` | `3` | `11` | `2.89` |
| `u₂` | `−2` | `0` | `−2` |
| `b` | `.5` | `5.5` | `.445` |

These are data-loss gradients; a separate L2 term could affect a dropped unit's weights. For a finite-difference check, keep the same mask for both perturbed evaluations—resampling would compare different functions.

**Inference and convention comparison, using the original parameters:**

- Standard dropout uses `qh=(1,.5)` at inference: output `3(1)−2(.5)+.5=2.5`. Equivalently scale the hidden units' outgoing weights to `(1.5,−1)` and leave output bias `.5` unchanged.
- Inverted dropout trains with `d=Mh/q`. For the same mask and original numbers, `d=(4,0)`, output `12.5`, residual `11.5`, loss `66.125`. Its gradients in the table's parameter order are `(69,0,69,0,46,0,11.5)`; the extra `1/q` appears in the backward mask multiplier too.
- Inverted dropout uses unscaled `h` at inference, giving `3(2)−2(1)+.5=4.5` for these original numbers. These are different conventions applied to fixed illustrative parameters, not two independently trained models expected to have identical parameters or outputs.

**Counting and expectation:** Two eligible units give four masks; with `q=.5` each has probability `.25` and the expected active count is 1. This does not mean four independent models were trained. Even a one-unit nonlinear example shows why mean activation is only an inference approximation: if `Z=2M` with `M~Bernoulli(.5)`, then `E[σ(Z)]=[σ(0)+σ(2)]/2≈.690399`, while `σ(E[Z])=σ(1)≈.731059`.

**Try it:** Reset to the original parameters and use standard-dropout mask `(0,1)`. Find prediction, loss, all seven gradients, and a `.01` update. Separately, with three eligible units and `q=.8`, find the number of masks, expected active count, and probability of the particular mask `(1,1,0)`.

<details>
<summary>Check N6.8</summary>

Masked activation `(0,1)`, prediction `−1.5`, residual `−2.5`, loss `3.125`. Hidden deltas `(0,5)`. Gradients in order `(a₁,a₂,c₁,c₂,u₁,u₂,b)` are `(0,5,0,5,0,−2.5,−2.5)`. Updated parameters `(1,1.95,1,−1.05,3,−1.975,.525)`. There are `2³=8` masks; expected active count `3(.8)=2.4`; the specified mask has probability `.8²(.2)=.128`. The masks are not uniformly distributed when `q≠.5`.

</details>

<a id="n6-9"></a>

### N6.9 Coordinate clipping versus norm clipping

**Page:** 161. The slide displays a positive ceiling only. For signed gradients, explicitly choose either symmetric coordinate clipping `gᵢ←max(−c,min(gᵢ,c))`, or global-norm clipping `g←g min(1,c/||g||₂)`. The second rule leaves a zero vector unchanged.

Let `g=(6,−8)`, `c=5`, starting weights `w=(1,1)`, rate `.1`.

| Rule | Clipped gradient | Updated weights |
| --- | --- | --- |
| Symmetric coordinatewise | `(5,−5)` | `(.5,1.5)` |
| Global L2 norm: `||g||=10`, scale `.5` | `(3,−4)` | `(.7,1.4)` |

Norm clipping preserves direction; coordinate clipping can change it. A one-sided `gᵢ>5` rule would leave the large `−8` untouched. Clipping gradients does not directly clip weights.

**Try it:** Clip `g=(−12,5)` with `c=6` under both rules. Starting from zero weights and rate `.1`, give the two updates.

<details>
<summary>Check N6.9</summary>

Coordinate clipping gives `(−6,5)`, so weights become `(.6,−.5)`. Norm is 13; global-norm clipping gives `(−72/13,30/13)≈(−5.538462,2.307692)`, so weights become `(36/65,−3/13)≈(.553846,−.230769)`.

</details>

<a id="n6-10"></a>

### N6.10 Input standardization and optional initialization scales

**Page:** 163. Training feature values are `[2,4,6]`. Use variance with divisor `N=3` for this preprocessing convention: `μ=4`, `σ²=(4+0+4)/3=8/3`, `σ≈1.632993`. Standardized training values `(x−μ)/σ` are `[-1.224745,0,1.224745]`; their mean is zero and their population variance is one. A held-out value `8` becomes `(8−4)/√(8/3)≈2.449490` using **training** statistics.

Dividing by variance instead of standard deviation would not give unit variance. For a constant training feature, define a safe policy such as using denominator 1 after centering; do not divide by zero. Fixed input preprocessing does not include batch normalization's full train/inference machinery.

**Try it:** Fit the transform on training values `[1,4,7]`, then transform a held-out `10`.

<details>
<summary>Check N6.10</summary>

Training mean 4, variance 6, standard deviation `√6`. Standardized training values `[-1.224745,0,1.224745]`; held-out 10 becomes `6/√6≈2.449490`. The identical normalized pattern reflects rescaling of equally spaced training values, not reuse of the earlier variance.

</details>

**Optional extension — formulas beyond the slide's named list:** If an exercise specifies Xavier normal variance `2/(fan_in+fan_out)` and He normal variance `2/fan_in`, a layer with fan-in 8 and fan-out 4 has variances `1/6` and `1/4`, respectively. The standard deviations used to scale standard-normal draws are `√(1/6)≈.408248` and `.5`; variance is not standard deviation. These formulas assume the stated versions of the initializers, not every implementation/gain setting. With fan-in 4 and fan-out 4, retry answers are Xavier variance `.25`, standard deviation `.5`; He variance `.5`, standard deviation `.707107`. Full Xavier/He/SVD derivations are not supplied in this PDF.

<a id="n6-11"></a>

### N6.11 Early stopping and selecting a run

**Pages:** 160, 162, 164. Define the rule before using it: lower validation loss is better; **any strict decrease** beats the best recorded loss; patience is two consecutive non-improving epochs; save improving checkpoints; restore the best one when stopping. No minimum improvement threshold is used in this example.

| Epoch | Training loss | Validation loss | Best checkpoint so far | Consecutive non-improvements |
| --- | --- | --- | --- | --- |
| `1` | `.65` | `.60` | `1` | `0` |
| `2` | `.50` | `.50` | `2` | `0` |
| `3` | `.42` | `.51` | `2` | `1` |
| `4` | `.35` | `.49` | `4` | `0` |
| `5` | `.30` | `.495` | `4` | `1` |
| `6` | `.25` | `.50` | `4` | `2`: stop |

Stop after epoch 6, but restore **epoch 4**. Falling training loss is not the checkpoint-selection rule. Keep the test set out of this repeated selection process. A grid of three learning rates, two regularization strengths, and two batch sizes has `3×2×2=12` configurations; three independent seeds per configuration require 36 runs, not 36 different hyperparameter settings.

**Try it:** With the same rule, validation losses are `[.4,.35,.35,.36,.30]`. At which epoch does training stop, and which checkpoint is restored? Can the listed fifth value justify continuing after the rule would already have stopped? How many runs are in a `4×3` grid with two seeds?

<details>
<summary>Check N6.11</summary>

Best checkpoint is epoch 2. Equality at epoch 3 is not a strict improvement; epoch 4 is the second consecutive non-improvement, so stop there and restore epoch 2. The fifth loss would not have been observed under this run's stopping rule; looking ahead changes the procedure. Grid size is 12 configurations and 24 seeded runs.

</details>

**Augmentation reasoning check:** Create transformations only when they preserve the target meaning; a digit rotation can change a label. Split original examples before generating related variants so augmented siblings do not leak between training and evaluation sets. Synthetic variants are correlated, so counting them does not make the independent-sample variance formulas automatically apply.

## Readiness check before a quiz or midterm

Use the instructor's announced coverage to choose the relevant items. You are ready to move on when you can solve a changed-value question **without replaying the worked solution** and explain your intermediate steps.

- [ ] Form a two-feature regression loss, calculate every gradient, and complete an update table.
- [ ] Calculate a sigmoid prediction, natural-log BCE, single-example gradients, and an averaged batch update.
- [ ] Construct and verify gates/XOR/DNF from weights, reduce a K-map, and count parity constructions under explicit assumptions.
- [ ] Trace a perceptron with stated label and tie conventions.
- [ ] Differentiate a branching graph, evaluate activation derivatives, and explain the Hessian test.
- [ ] Complete the two-hidden-layer network's forward pass, all deltas, all weight/bias gradients, and a simultaneous update.
- [ ] Compare gradient descent with Newton, classify quadratic step sizes, and trace RProp/momentum/Nesterov using their stated state variables.
- [ ] Compare full-batch, SGD, and mini-batch paths and count updates; distinguish fixed-sample variance, convergence assumptions, and sample work.
- [ ] Trace two-step RMSProp and bias-corrected Adam updates with explicit averaging, state, and epsilon conventions.
- [ ] Calculate L2 gradients, a fixed-mask dropout forward/backward pass, and the matching inference scaling.
- [ ] Compare coordinate and norm clipping; normalize with training statistics and apply a stated early-stopping rule.
- [ ] If assigned for the assessment: count network parameters and calculate classification metrics.

For a timed rehearsal, select one fresh **Try it** from each in-scope calculation family, cover all answers, and work for a time limit you choose. Record where time was lost: selecting the formula, arranging dimensions, arithmetic, or interpreting the answer. Repair that specific skill, then repeat with changed values. This is a study exercise, not an official mock paper or marking scheme.

**Answer validation:** The numerical tables were checked with local calculations; the full-network, L2-regularized, and fixed-mask dropout derivatives were also compared with central finite differences. Lecture 5 additions were checked on 16 September 2026. Displayed precision is for checking work, not a requirement to memorize decimals.
