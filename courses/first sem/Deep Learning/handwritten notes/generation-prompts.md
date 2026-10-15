# Image generation specifications

Mode: built-in imagegen, one call per distinct PNG. The original file_0000000065d881f8a5c73645cbc9bd98.png is a style reference only. Exact approved page text appears below. See review-log.md for visual corrections and approved filenames.

Shared instruction: Create one high-resolution A4-like portrait handwritten Deep Learning exam page. Use warm white faintly ruled paper, red left margin, tidy blue handwriting, pink-highlighted blue title, burgundy numbered headings, green formula/result boxes. Clean flat complete page with uncut margins; no hands, shadows or watermark. Use broad derivations or balanced two columns; keep readable handwriting and coherent reading order. Render every line faithfully, preserving numbers, signs, fractions, logs, matrix order and subscripts/superscripts. Convert plaintext to mathematical notation. Do not invent content or omit text to fit. Keep formula → substitution → result together. Diagrams only where specified; arrows must match dependencies. Final values and approximate signs must match.

## Page inputs

### DL1-01

```text
TITLE: What learning means: tasks, data and generalization
Exact approved page content:
1) Put the terms in order
Deep learning ⊂ machine learning ⊂ artificial intelligence.
ML learns a mapping from examples; DL uses multilayer neural networks.
Traditional ML often uses designed features; DL can learn representations.
Neither approach guarantees correct predictions on new data.

2) Task, experience, performance
T = task; E = experience; P = performance measure.
Learning means improving P on T using E.
Example: T = classify spam; E = labelled emails; P = held-out accuracy.
Regression predicts a real value, such as house price.
Classification predicts a category, such as benign/malignant.
Supervised learning uses (x,y); unsupervised learning finds structure in x.
Clustering groups similar inputs without supplied class targets.
Structured prediction can output related labels/locations rather than one scalar.

3) Learning as optimization
Prediction ŷ_i=f(x_i;θ); θ = weights and biases, not input data.
Empirical cost J(θ)=(1/m) Σ_i ℓ(ŷ_i,y_i).
Initialize θ → predict → compute loss → gradients → update → repeat.
Loss measures one example; cost aggregates examples under a stated convention.

4) Practice: identify the quantities
Two examples: x₁=(1,0), y₁=2; x₂=(0,2), y₂=1.
Task = regression; experience = these labelled pairs.
Model ŷ=w₁x₁+w₂x₂+b has 3 trainable parameters.
For one example, two features form x; its single target is y.
Use training data to fit; validation to choose settings; test to evaluate.
Low training loss alone does not establish generalization.
Footer: DL1-01 | Lecture 1 | PDF pp. 7–29
```

### DL1-02

```text
TITLE: Linear regression: loss, derivatives and one update
Exact approved page content:
1) Model and objective
ŷ_i=w x_i+b; residual e_i=ŷ_i−y_i; m = example count.
J(w,b)=(1/(2m)) Σ_i e_i² is HALF mean squared error.
The factor 1/2 simplifies derivatives; define it before calculating.

2) Derive the gradients
∂e_i/∂w=x_i; ∂e_i/∂b=1.
∂J/∂w=(1/m) Σ_i e_i x_i.
∂J/∂b=(1/m) Σ_i e_i.
w_new=w−η ∂J/∂w; b_new=b−η ∂J/∂b.
η>0 is learning rate; compute BOTH gradients at the old parameters.

3) Complete practice example
Data (x,y)=(1,2),(2,3); w=0, b=0, η=0.1, m=2.
Predictions=(0,0); residuals=(−2,−3).
J_old=(4+9)/4=3.25.
g_w=[(−2)(1)+(−3)(2)]/2=−4.
g_b=(−2−3)/2=−2.5.
Thus w_new=0.4; b_new=0.25.
New predictions=(0.65,1.05); residuals=(−1.35,−1.95).
J_new=(1.8225+3.8025)/4=1.40625.

4) Interpret and avoid traps
Negative gradients increase w,b when subtracted.
The cost decreased for this step; an excessive η can increase it.
Do not mix residual y−ŷ with the formula for ŷ−y.
Plain MSE doubles these gradients; the same η gives different steps.
Never update w before evaluating the old-state bias gradient.
Footer: DL1-02 | Lecture 1 | PDF pp. 30–41
```

### DL1-03

```text
TITLE: Multiple features: two simultaneous batch updates
Exact approved page content:
1) Generalize the model
ŷ_i=b+Σ_(j=1)^d w_j x_ij; d features, d+1 parameters.
Use x_i0=1 and w₀=b to absorb the intercept.
J=(1/(2m)) Σ_i (ŷ_i−y_i)².
g_j=(1/m) Σ_i (ŷ_i−y_i)x_ij; w_j←w_j−ηg_j.
All parameters update simultaneously from the same predictions.

2) Practice givens
Rows (x₁,x₂,y): (1,0,2), (0,2,1).
Initial (w₁,w₂,b)=(0,0,0); η=0.1; m=2.
ŷ=(0,0); e=(−2,−1); J₀=5/4=1.25.
g_w₁=[−2(1)−1(0)]/2=−1.
g_w₂=[−2(0)−1(2)]/2=−1.
g_b=(−2−1)/2=−1.5.
First update: (w₁,w₂,b)=(0.1,0.1,0.15).

3) Recompute before the second update
ŷ=(0.25,0.35); e=(−1.75,−0.65).
J₁=(3.0625+0.4225)/4=0.87125.
g_w₁=−0.875; g_w₂=−0.65; g_b=−1.2.
Second update: (w₁,w₂,b)=(0.1875,0.165,0.27).
New predictions=(0.4575,0.6000); J₂=0.634827.

4) Matrix check and takeaway
Row convention: X is m×d, w is d×1, predictions are m×1.
g_w=Xᵀe/m; g_b=Σ_i e_i/m.
Loss denominator is 2m; derivative denominator is m.
Compute, average once, update together, then recompute.
Footer: DL1-03 | Lecture 1 | PDF pp. 42–44
```

### DL2-01

```text
TITLE: Logistic regression: probability, boundary and BCE
Exact approved page content:
1) From a score to a probability
z=wᵀx+b; p=σ(z)=1/(1+exp(−z)).
p estimates P(y=1|x); binary label y∈{0,1}.
At threshold p≥0.5 predict 1, equivalently z≥0.
With raw features the boundary wᵀx+b=0 is affine.
Circle example: z=−1+x₁²+x₂² → boundary x₁²+x₂²=1.
At (0,0), predict0; at (1,1), z=1 → predict1 (outside circle).

2) Loss from the Bernoulli likelihood
P(y|x)=p^y(1−p)^(1−y).
ℓ=−ln P(y|x)=−y ln p−(1−y)ln(1−p).
If y=1: ℓ=−ln p; if y=0: ℓ=−ln(1−p).
Correct confident predictions have small loss; wrong confident ones large loss.
Use natural logs; J=(1/m)Σ_i ℓ_i.

3) Practice: one prediction
x=(1,2), w=(0.2,−0.3), b=0.1, y=1.
z=0.2−0.6+0.1=−0.3.
p=0.425557; predicted class=0, incorrectly.
ℓ=−ln(0.425557)=0.854355.
Boundary: 0.2x₁−0.3x₂+0.1=0.
At x=(1,1), z=0 and p=0.5.

4) What changes in training?
Learning adjusts w,b to reduce BCE, not the discrete 0–1 error directly.
A sigmoid output is a modelled probability, not certainty or automatic calibration.
Do not apply a hard threshold before computing BCE or gradients.
Stable implementation uses logits rather than taking logs of rounded 0 or 1.
Footer: DL2-01 | Lecture 2 | PDF pp. 4–26
```

### DL2-02

```text
TITLE: Logistic gradients: chain rule and batch averaging
Exact approved page content:
1) Differentiate through the graph
z=wᵀx+b → p=σ(z) → BCE ℓ.
∂ℓ/∂p=−y/p+(1−y)/(1−p).
∂p/∂z=p(1−p).
Multiply and simplify: ∂ℓ/∂z=p−y.
Thus ∇_w ℓ=(p−y)x; ∂ℓ/∂b=p−y.
For mean batch cost, average each example gradient ONCE.

2) Practice: two examples at the same old state
w=(0.2,−0.3), b=0.1; η=0.1.
Example A: x=(1,2), y=1; z=−0.3, p=0.425557.
δ_A=p−y=−0.574443; ℓ_A=0.854355.
Example B: x=(2,−1), y=0; z=0.8, p=0.689974.
δ_B=0.689974; ℓ_B=1.171101.
J=(0.854355+1.171101)/2=1.012728.
g_w₁=(−0.574443+2×0.689974)/2=0.402753.
g_w₂=(2×(−0.574443)−0.689974)/2=−0.919430.
g_b=(−0.574443+0.689974)/2=0.057766.
Update: w=(0.159725,−0.208057), b=0.094223.
Retain full precision until the final rounding.

3) A simpler lecture graph
J=3(a+bc), a=5,b=3,c=2.
u=bc=6; v=a+u=11; J=33.
∂J/∂a=3; ∂J/∂b=3c=6; ∂J/∂c=3b=9.
Reuse intermediate derivatives; bias derivatives are not weight derivatives.
The cancellation p−y is specific to sigmoid plus BCE.
Footer: DL2-02 | Lecture 2 | PDF pp. 27–31
```

### DL2-03

```text
TITLE: Neurons and depth: shapes, parameters and nonlinearities
Exact approved page content:
1) One neuron and a layer
z=wᵀx+b; a=φ(z). Bias shifts the decision boundary.
Threshold unit: H(z)=1 if z≥0, else 0 (our stated convention).
Sigmoid is a smooth squashing function; tanh and ReLU are alternatives.
Feed-forward networks compose layers without directed cycles.

2) Why a nonlinear activation matters
Two affine layers without nonlinearities collapse to one:
W₂(W₁x+b₁)+b₂=(W₂W₁)x+(W₂b₁+b₂).
Adding linear layers alone does not create nonlinear decision regions.
Hidden layers form intermediate representations; output matches the task.

3) Practice: shapes and trainable counts
Column convention: layer a_l=φ(W_l a_(l−1)+b_l).
Network widths 3→4→2; input is 3×1.
W₁:4×3; b₁:4×1; hidden a₁:4×1.
W₂:2×4; b₂:2×1; output a₂:2×1.
Layer1 parameters=4×3+4=16.
Layer2 parameters=2×4+2=10; total=26.
For m examples as columns, input X:3×m and output:2×m.
Bias broadcasts across examples; it is not multiplied by m in parameter count.

4) Count depth explicitly
Depth is the longest input-to-output path in computational layers.
3→4→2 has one hidden layer and two trainable layers.
If a source counts the input as a layer, its layer count differs by one.
Representation ability does not prove efficient learnability or generalization.
State the matrix convention; do not transpose halfway through.
Footer: DL2-03 | Lecture 2 | PDF pp. 32–53
```

### DL2-04

```text
TITLE: Threshold gates and two XOR constructions
Exact approved page content:
1) Fix the threshold convention
H(z)=1 for z≥0; otherwise 0. Inputs x₁,x₂ are Boolean.
AND=H(x₁+x₂−1.5); OR=H(x₁+x₂−0.5).
NOT(x)=H(0.5−x).
At-least-K of n inputs: H(Σ_i x_i−K+0.5).
Half-integer thresholds avoid ties for Boolean sums.

2) XOR with two hidden units and an output
h₁=OR(x₁,x₂); h₂=AND(x₁,x₂).
y=H(h₁−2h₂−0.5).
Table x₁x₂ | h₁ h₂ | y:
00 | 0 0 | 0
01 | 1 0 | 1
10 | 1 0 | 1
11 | 1 1 | 0
Three threshold units; one hidden layer; all edges go forward.

3) XOR with a skip connection
h=H(x₁+x₂−1.5).
y=H(x₁+x₂−2h−0.5).
Two computational units, but output also receives raw x₁,x₂.
At (1,1): h=1; output score=2−2−0.5=−0.5 →0.
At (1,0): h=0; output score=1−0−0.5=0.5 →1.
This architecture differs from a strictly layer-to-layer 2→1→1 network.

4) Why a single perceptron fails
XOR's positive corners cannot be separated from both negative corners by one line.
Hidden nonlinear units compose regions; one affine threshold cannot.
Footer: DL2-04 | Lecture 2 | PDF pp. 54–58, 83
```

### DL2-05

```text
TITLE: Boolean networks: minterms, negative literals and K-maps
Exact approved page content:
1) Build a network from a truth table
For each positive row, form an AND of its matching literals.
OR the positive-row detectors to obtain disjunctive normal form (DNF).
Any finite Boolean function has such an exact construction.
Universal representation may require many hidden units.

2) Encode a minterm without explicit NOT units
Let P = positive literals, N = negative literals, k=|P|.
h=H(Σ_(j∈P)x_j−Σ_(j∈N)x_j−k+0.5).
Every mismatch reduces the score by 1.
Practice row (A,B,C)=(1,0,1): h=H(A−B+C−1.5).
Matching row score=0.5 →1; row (1,1,1) score=−0.5 →0.

3) Complete simplification example
Positive rows ABC: 100,101,110,111; all other rows output 0.
DNF=A¬B¬C ∨ A¬BC ∨ AB¬C ∨ ABC.
K-map: columns BC in Gray order 00,01,11,10; rows A=0,1.
Row A=0: 0 0 0 0.
Row A=1: 1 1 1 1.
Group four adjacent ones: B,C vary, so retain only A.
Simplified output y=H(A−0.5).
Four minterm detectors can be replaced by one threshold unit here.

4) K-map rules and limitations
Groups have sizes 1,2,4,8,…; wraparound adjacency is allowed.
Adjacent cells differ in one bit; use Gray order, not ordinary binary order.
Keep literals that stay fixed; eliminate those that vary.
Simplifying DNF reduces this construction's size, not necessarily the global optimum.
Footer: DL2-05 | Lecture 2 | PDF pp. 59–75
```

### DL2-06

```text
TITLE: Parity and depth: compare specified constructions
Exact approved page content:
1) Parity is a useful stress test
N-input odd parity outputs 1 when an odd number of inputs are 1.
Exactly 2^(N−1) of the 2^N rows are positive.
Flipping one bit changes the output, so adjacent positive minterms do not merge.
The direct DNF construction uses 2^(N−1) hidden detectors plus one OR output.
This is a construction count, NOT a lower bound for all threshold networks.

2) Compose two-input XOR blocks
Use the three-unit XOR block: two hidden units then an output.
Combine N inputs using N−1 XOR blocks.
Total threshold units=3(N−1), including intermediate block outputs.
Balanced tree: at most ceil(log₂N) XOR stages.
Two trainable layers per XOR stage → depth at most 2ceil(log₂N).
For uneven trees, carry an unpaired value forward without an extra XOR block.

3) Practice: N=8
DNF positive rows=2⁷=128; total units=129.
XOR tree needs 7 blocks →21 threshold units.
Tree stages: 8→4→2→1 parity values.
Three stages ×2 layers=6 trainable layers.
Example bits 1,0,1,1,0,0,1,0 have four ones → even parity →0.
First XOR pairs=(1,0,0,1); next=(1,1); final=0.

4) What the comparison establishes
Depth can exploit compositional structure to save units in a specified design.
It does not prove every shallow architecture needs exponentially many units.
Some Boolean functions still need large circuits; depth is not universal compression.
Keep hidden-unit counts, total-unit counts and layer counts separate.
The two-unit skip-connected XOR changes the cost model; do not mix counts.
Footer: DL2-06 | Lecture 2 | PDF pp. 76–98
```

### DL2-07

```text
TITLE: Classification regions: half-spaces, intersections and unions
Exact approved page content:
1) Geometry of a threshold unit
H(wᵀx+b) represents a half-space.
The boundary wᵀx+b=0 is a line in 2D, hyperplane in higher dimensions.
Intersect half-spaces using AND; combine distinct regions using OR.
This builds polygonal regions; finer pieces can approximate complex boundaries.

2) Practice: a closed rectangle
Wanted: 0≤x≤2 and 1≤y≤3.
h₁=H(x); h₂=H(2−x); h₃=H(y−1); h₄=H(3−y).
r=H(h₁+h₂+h₃+h₄−3.5).
All four inequalities must hold to activate r.
At (1,2): h=(1,1,1,1), r=H(0.5)=1.
At (2.5,2): h=(1,0,1,1), r=H(−0.5)=0.
At (0,1): all four indicators are 1 under H(0)=1.
Four boundary detectors plus one AND unit represent this region.

3) Union of two regions
If r₁,r₂ are Boolean membership outputs, u=H(r₁+r₂−0.5).
For (r₁,r₂)=(0,1), union score=0.5 →1.
For (0,0), score=−0.5 →0.
Construct each region, then OR their membership indicators.

4) Limits worth knowing
A finite number of straight boundaries does not exactly form every curved boundary.
More pieces can improve approximation, but cost and training difficulty grow.
Exact boundary inclusion depends on the stated threshold convention.
Architecture capacity is different from finding useful weights from samples.
Footer: DL2-07 | Lecture 2 | PDF pp. 99–113
```

### DL2-08

```text
TITLE: Function approximation: pulses, sums and the theorem
Exact approved page content:
1) From regions to a real-valued function
Threshold classifiers indicate where x lies; weighted indicators set heights.
A 1D pulse on [a,b) is I_[a,b)(x)=H(x−a)−H(x−b).
H(z)=1 if z≥0; otherwise 0.
The subtraction gives exact half-open interval membership.

2) Practice: sum two pulses
f_hat(x)=2[H(x)−H(x−1)]−[H(x−1)−H(x−3)].
For x<0: all steps 0 → f_hat=0.
For 0≤x<1: first pulse 1, second 0 → f_hat=2.
For 1≤x<3: first pulse 0, second 1 → f_hat=−1.
For x≥3: both pulses 0 → f_hat=0.
Checks: f_hat(0.5)=2; f_hat(1)=−1; f_hat(3)=0.
Three distinct threshold features can feed one linear output.

3) How approximation improves
Partition a bounded domain into small intervals/regions.
Assign a height to each indicator; sum their weighted outputs.
Smaller regions can approximate continuous functions more closely.
Higher-dimensional constructions use intersected half-spaces or related features.

4) Universal approximation: read the claim carefully
With appropriate nonlinear activations and enough width,
a feed-forward network can approximate continuous functions on compact domains
arbitrarily well under the theorem's conditions.
Approximation is not exact equality for every function everywhere.
The theorem does not promise a small network, easy optimization, or unseen-data accuracy.
Depth can express compositional functions efficiently; more depth is not automatically better.
Footer: DL2-08 | Lecture 2 | PDF pp. 114–119
```

### DL3-01

```text
TITLE: Perceptron learning: ordered updates
Exact approved page content:
1) A signed-label classifier
Use labels t∈{−1,+1}; score s=w·x+b.
Predict +1 if s≥0, otherwise −1.
On t s≤0 (mistake OR zero margin):
w←w+ηt x; b←b+ηt.
The zero-margin rule avoids an ambiguous tie.

2) Complete ordered practice pass
η=1; initial w=(0,0), b=0.
Visit A: x=(1,0),t=+1; then B: x=(0,1),t=−1.
A: s=0; t s=0 → update.
w=(0,0)+1(1,0)=(1,0); b=1.
B uses the NEW current parameters:
s=(1,0)·(0,1)+1=1; t s=−1 → update.
w=(1,0)−(0,1)=(1,−1); b=0.

3) Check the resulting separator
A score=1 → +1; B score=−1 → −1.
Next pass has no mistakes or zero margins.
Boundary x₁−x₂=0; w is its normal vector.
Bias may be a weight on constant feature x₀=1.

4) What the rule can guarantee
Finite convergence requires linearly separable finite data
and a positive fixed learning rate under the usual assumptions.
Nonseparable data may cycle; impose a stopping rule.
Hidden-unit target labels are not supplied by network labels.
The single-perceptron rule does not directly train a full MLP.
Footer: DL3-01 | Lecture 3 | PDF pp. 30–78
```

### DL3-02

```text
TITLE: Activations: outputs, slopes and probability
Exact approved page content:
1) One neuron has two operations
z=Σ_i w_i x_i+b; activation a=f(z).
Weights/bias are learned; activation defines the response.
Without nonlinear hidden activations, affine layers collapse
to a single affine map: extra depth adds no nonlinear boundary.

2) Core activation and derivative table
Sigmoid: σ(z)=1/(1+e^(−z)); σ′=a(1−a).
tanh: a=tanh z; derivative=1−a².
ReLU: a=max(0,z); derivative=0 for z<0,1 for z>0.
At z=0 ReLU is nondifferentiable; choosing derivative0 is conventional.
Softplus: a=ln(1+e^z); derivative=σ(z).
Linear: a=z; derivative=1.

3) Worked slopes at z=0 (practice)
σ(0)=1/2; σ′(0)=(1/2)(1/2)=0.25.
tanh(0)=0; tanh′(0)=1.
ReLU(0)=0; use the stated derivative0 convention.
Softplus(0)=ln2=0.693147; derivative=0.5.

4) Probability interpretation and saturation
For binary output, y=σ(z) models P(t=1|x).
P(t=0|x)=1−y; threshold0.5 corresponds to z≥0.
An output in [0,1] does not guarantee calibration.
At z=ln4: y=0.8; slope=0.8(0.2)=0.16.
As |z| grows, sigmoid slope approaches0.
Repeated small local slopes can weaken hidden gradients.
Use the activation belonging to the neuron being differentiated.
The output error formula also depends on the chosen loss.
Footer: DL3-02 | Lecture 3 | PDF pp. 73–100,154–156
```

### DL3-03

```text
TITLE: Learning from samples: empirical risk
Exact approved page content:
1) What learning minimizes
Parameters θ collect all weights and biases.
Prediction y=f(x;θ); target t comes from data.
Population risk R(θ)=E_(x,t)[L(f(x;θ),t)].
Empirical risk R̂(θ)=(1/N)Σ_n L(f(x_n;θ),t_n).
ERM fits θ using this training average.
For fixed θ and iid data, E[R̂(θ)]=R(θ).
The minimum training loss need not estimate test loss without bias.

2) Classification error and a trainable surrogate
0–1 loss=1[predicted class≠t]; often flat in parameters.
BCE=−[t ln y+(1−t)ln(1−y)] for t∈{0,1}.
Use natural logarithms (nats); y is a probability.
Smooth surrogate changes can guide optimization
even while the predicted class stays unchanged.

3) Complete two-example practice calculation
Targets=(1,0); probabilities=(0.8,0.25).
Predicted classes at threshold0.5 are (1,0).
0–1 training error=(0+0)/2=0.
L₁=−ln0.8=0.223144.
L₂=−ln(1−0.25)=−ln0.75=0.287682.
Mean BCE=(0.223144+0.287682)/2=0.255413.
Zero classification error does not imply zero BCE.

4) Capacity, optimization and generalization
Capacity: can the architecture represent the needed function?
Optimization: can training find useful parameters?
Generalization: do predictions work on unseen data?
Small training risk alone does not answer the last two questions.
Footer: DL3-03 | Lecture 3 | PDF pp. 19–29,101–110
```

### DL3-04

```text
TITLE: Calculus for learning: gradients and path sums
Exact approved page content:
1) Local change and gradient
For column θ, ΔF≈(∇F)ᵀΔθ.
Gradient points toward fastest local increase in Euclidean norm.
Descent: θ_new=θ−η∇F; sufficiently small steps can reduce F.
H_ij=∂²F/(∂θ_i∂θ_j) is the Hessian.

2) Complete curvature practice
F(u,v)=u²+2v²; ∇F=(2u,4v); H=diag(2,4).
At (u,v)=(1,−1): gradient=(2,−4), F=3.
η=0.1 → (u,v)_new=(0.8,−0.6).
F_new=0.8²+2(−0.6)²=1.36.
At (0,0), gradient0 and positive-definite H → strict minimum.
For G=u²−v², H=diag(2,−2): (0,0) is a saddle.
Zero gradient alone does not prove a minimum.
Zero eigenvalues/second derivatives can leave the test inconclusive.

3) Branching chain rule: multiply paths, then SUM
Practice graph: a=x²; b=3x; J=a b.
x influences J through BOTH a and b.
dJ/dx=(∂J/∂a)(da/dx)+(∂J/∂b)(db/dx).
At x=2: a=4,b=6,J=24.
Via a: b(2x)=6×4=24.
Via b: a(3)=4×3=12.
Total dJ/dx=24+12=36.
Check J=3x³ → derivative9x²=36.

4) Backprop connection
Cache forward values; propagate derivatives backward.
At a hidden neuron, add contributions from every outgoing path.
Backprop computes derivatives; an optimizer applies updates.
Footer: DL3-04 | Lecture 3 | PDF pp. 111–145,167–180
```

### DL3-05

```text
TITLE: A complete 2 → 2 → 1 forward pass
Exact approved page content:
1) Course indexing and complete givens (practice)
w_(i,j)^(l): previous-layer source i → current-layer target j.
w_(0,j)^(l) is bias, attached to constant input1.
Every neuron uses sigmoid; input x=(1,2); target t=1.
Hidden weights: w11=.1,w21=.2,w12=−.1,w22=.1.
Hidden biases b₁=b₂=0.
Output weights v₁=.3,v₂=−.2; output bias c=.1.
Diagram: x₁,x₂ → h₁,h₂ → y (all adjacent connections).

2) Hidden pre-activations and activations
z₁=.1(1)+.2(2)+0=.5.
z₂=−.1(1)+.1(2)+0=.1.
h₁=σ(.5)=0.622459.
h₂=σ(.1)=0.524979.

3) Output and loss
s=.3h₁−.2h₂+.1=0.181742.
y=σ(s)=0.545311.
L=−[t ln y+(1−t)ln(1−y)].
For t=1: L=−ln0.545311=0.606399 nats.
Threshold0.5 predicts class1, but confidence is limited.

4) Shapes and parameter count
Column-vector convention: z=Wᵀx+b.
W_hidden=[[.1,−.1],[.2,.1]] has shape2×2.
v has shape2×1; h and b have shape2×1.
Hidden parameters=2×2+2=6.
Output parameters=2×1+1=3; total9.
Cache z₁,z₂,h₁,h₂,s,y for backward computation.
No parameter changes during this forward pass.
Footer: DL3-05 | Lecture 3 | PDF pp. 157–162,182–200; handout1–2
```

### DL3-06

```text
TITLE: Output backprop: chain rule to a weight
Exact approved page content:
1) Repeat the complete practice givens
x=(1,2),t=1; all neurons sigmoid.
Hidden source→target weights (.1,.2) into h₁,
(−.1,.1) into h₂; hidden biases0.
h₁=0.622459,h₂=0.524979.
Output s=v₁h₁+v₂h₂+c; v=(.3,−.2),c=.1.
y=0.545311; BCE L=0.606399; learning rateη=.1.

2) General output chain rule
δ_out≡∂L/∂s=(∂L/∂y)(∂y/∂s).
∂L/∂y=−t/y+(1−t)/(1−y)=(y−t)/[y(1−y)].
∂y/∂s=y(1−y).
Sigmoid + BCE → δ_out=y−t.
Numerically δ_out=−0.454689.
Do not multiply by another sigmoid derivative after cancellation.

3) Weight path and all output gradients
v₁ → s → y → L; ∂s/∂v₁=h₁.
∂L/∂v₁=δ_out h₁=−0.283026.
∂L/∂v₂=δ_out h₂=−0.238702.
∂L/∂c=δ_out=−0.454689.

4) Output updates (apply AFTER all backward gradients)
v₁_new=.3−.1(−.283025510)=0.328303.
v₂_new=−.2−.1(−.238702346)=−0.176130.
c_new=.1−.1(−.454689160)=0.145469.
Hidden deltas must still use OLD v₁=.3,v₂=−.2.
Negative gradients make these parameters increase.
For half-SSE .5(y−t)² instead: δ=(y−t)y(1−y).
The shortcut depends on BOTH activation and loss.
Footer: DL3-06 | Lecture 3 | PDF pp. 201–227; handout2–3
```

### DL3-07

```text
TITLE: Hidden backprop and simultaneous updates
Exact approved page content:
1) Complete practice givens and old forward values
x=(1,2),t=1; sigmoid hidden/output; η=.1.
Hidden w11=.1,w21=.2,w12=−.1,w22=.1; b₁=b₂=0.
Output v₁=.3,v₂=−.2,c=.1.
h₁=.622459,h₂=.524979,y=.545311; δ_out=−.454689.
Use full-precision cached values for calculations.

2) Hidden deltas: use SAME OLD output weights
δ₁=(δ_out v₁)h₁(1−h₁)=−0.032056092.
δ₂=(δ_out v₂)h₂(1−h₂)=0.022677716.
General hidden rule: δ_j^(l)=f′(z_j^(l))
×Σ_k w_(j,k)^(l+1)δ_k^(l+1).
With several next-layer units, sum ALL their paths.

3) Hidden weight/bias gradients
∂L/∂w_(i,j)=x_i δ_j; ∂L/∂b_j=δ_j.
Into h₁: (g_w11,g_w21,g_b1)
=(−.032056092,−.064112184,−.032056092).
Into h₂: (g_w12,g_w22,g_b2)
=(.022677716,.045355433,.022677716).

4) Simultaneous update: θ_new=θ_old−.1g
w11_new=.103206; w21_new=.206411; b₁_new=.003206.
w12_new=−.102268; w22_new=.095464; b₂_new=−.002268.
Output gradients=(−.283025510,−.238702346,−.454689160).
Thus v_new=(.328303,−.176130),c_new=.145469.
All nine gradients refer to one unchanged parameter state.
Store gradients first; update only after backward pass finishes.
Bias has constant input1, so no extra feature multiplier.
Do not use a newly updated downstream weight in a hidden delta.
Footer: DL3-07 | Lecture 3 | PDF pp. 228–243; handout3
```

### DL3-08

```text
TITLE: Batch training: average once, then update
Exact approved page content:
1) Batch objective and course notation
J(θ)=(1/B)Σ_n L_n(θ); B=actual batch size.
g=(1/B)Σ_n∇L_n(θ); θ_new=θ−ηg.
Every example in a batch uses the SAME old parameters.
Course y_j^(l) is activation; z_j^(l) is pre-activation.
w_(i,j)^(l) runs source i → target j; bias is w_(0,j).

2) Complete two-example practice update
One sigmoid output: y=σ(wx+b), BCE; w=0,b=0,η=.1.
Example A: x=1,t=1 → y=.5,δ=y−t=−.5.
Gradients (g_w,g_b)=(−.5,−.5); loss=ln2.
Example B: x=2,t=0 → y=.5,δ=.5.
Gradients (g_w,g_b)=(1,.5); loss=ln2.
Mean gradients=((−.5+1)/2,(−.5+.5)/2)=(.25,0).
w_new=−.025; b_new=0; old mean loss=.693147.
Recompute: y_A=σ(−.025)=.493750;
y_B=σ(−.05)=.487503.
New mean loss=[−ln y_A−ln(1−y_B)]/2=.687092.

3) General multilayer training loop
Initialize weights/biases; choose loss and learning rate.
For a batch: zero gradient accumulators.
For each example: forward → cache → loss → backward.
Accumulate every layer's weight and bias gradients.
Divide by B ONCE; update all parameters together.
Repeat; monitor training loss and held-out performance.

4) Exam traps
Updating after each example is a different algorithm (SGD).
Backprop computes gradients; gradient descent uses them.
Small loss change is a stopping heuristic, not proof of a minimum.
Footer: DL3-08 | Lecture 3 | PDF pp. 163–166,242–245; handout1–3
```

### DL4-01

```text
TITLE: Loss and saturation: why the surrogate matters
Exact approved page content:
1) A training step has separate jobs
Forward computes predictions; loss scores mismatch.
Backprop computes derivatives; optimizer changes parameters.
For each bias use its own gradient, not the corresponding weight gradient.
Hard 0–1 error is flat almost everywhere; use a suitable differentiable surrogate.
Minimizing a surrogate need not minimize finite-sample classification error.
This is an objective/model issue; it is not a failure of chain-rule differentiation.

2) Sigmoid plus squared error
p=σ(z); y∈{0,1}; ℓ_SE=1/2(p−y)².
∂ℓ_SE/∂z=(p−y)p(1−p).
When p saturates near 0 or 1, p(1−p) is tiny.
A confidently wrong prediction may therefore learn very slowly.

3) Sigmoid plus binary cross-entropy
ℓ_BCE=−y ln p−(1−y)ln(1−p).
∂ℓ_BCE/∂z=p−y.
The output sigmoid factor cancels algebraically for this pairing.
Hidden sigmoid layers can still have small derivatives.

4) Practice: confidently wrong
z=−8; y=1; p=0.000335350.
p(1−p)=0.000335238.
ℓ_SE=0.499665; ∂ℓ_SE/∂z=−0.000335125.
ℓ_BCE=8.000335; ∂ℓ_BCE/∂z=−0.999665.
If z=w×1 and η=0.1, squared-error Δw=+0.0000335125.
For BCE, Δw=+0.0999665.
Both push the wrong score upward; their gradient magnitudes differ sharply.

5) Interpretation
Better loss geometry can speed learning without changing the forward model.
Compare derivatives under explicitly stated loss scaling and output activation.
Footer: DL4-01 | Lecture 4 | PDF pp. 1–30
```

### DL4-02

```text
TITLE: Scalar convergence: step size, oscillation and rate
Exact approved page content:
1) Analyze a quadratic exactly
E(w)=a/2(w−w*)²; a>0; gradient=a(w−w*).
w_(t+1)=w_t−ηa(w_t−w*).
Error e_t=w_t−w* obeys e_(t+1)=(1−ηa)e_t.
Thus e_t=(1−ηa)^t e₀ and E_t=(1−ηa)^(2t)E₀.
Parameter-error factor and loss factor are different.

2) Stability cases
0<ηa<1: monotone approach; ηa=1: one-step solution.
1<ηa<2: alternating signs with shrinking magnitude.
ηa=2: non-decaying oscillation (unless already optimal).
ηa>2: divergence for nonzero initial error.
η=0: no movement; convergence requires 0<η<2/a.

3) Practice: a=4, w*=1, w₀=3
η=0.1 → error factor=0.6.
w₁=1+0.6(2)=2.2; w₂=1+0.6(1.2)=1.72.
E₀=2(2²)=8; E₁=2(1.2²)=2.88; E₂=1.0368.
η=0.4 → factor=−0.6; w₁=−0.2; w₂=1.72.
Both choices shrink loss by 0.36 each step, but paths differ.
η=0.5 → factor=−1; sequence 3,−1,3,… does not converge.

4) Beyond this toy model
Here η_opt=1/a is exact because curvature is constant and scalar.
For general nonconvex neural losses, curvature varies with position.
Zero gradient can also mean a maximum, saddle or flat point.
Do not treat this quadratic proof as a universal neural-network guarantee.
Footer: DL4-02 | Lecture 4 | PDF pp. 31–36
```

### DL4-03

```text
TITLE: Hessian geometry: ill-conditioning and Newton steps
Exact approved page content:
1) Curvature in multiple directions
For a positive-definite quadratic, E(w)=1/2(w−w*)ᵀH(w−w*).
Gradient g=H(w−w*); H is the symmetric Hessian.
Along Hessian eigenvector j, error multiplies by 1−ηλ_j.
Fixed-step GD converges when 0<η<2/λ_max.
Condition number κ=λ_max/λ_min; large κ makes one shared step inefficient.

2) Practice: E(x,y)=x²+4y²
g=(2x,8y); H=diag(2,8); κ=4.
Start (x,y)=(1,1), E=5; choose η=0.2<0.25.
GD step: (1,1)−0.2(2,8)=(0.6,−0.6).
New E=0.36+4(0.36)=1.8.
At η=0.3, y-error factor=1−2.4=−1.4 → unstable.
The x direction can be stable while y diverges.

3) Newton uses curvature
Solve Hs=g, then w_new=w−s.
Here s=diag(1/2,1/8)(2,8)=(1,1).
Newton reaches (0,0) in one step for this exact quadratic.
In general use a linear solve rather than explicitly forming H inverse.

4) Costs and risks
P parameters require P² Hessian entries; P=100000 →10¹⁰ entries.
An indefinite Hessian can make a Newton direction fail to descend.
Damping or line searches can help; second order does not guarantee global optimality.
Gradient is perpendicular to a smooth level set, not generally toward the minimum.
Rescaling inputs may improve conditioning without making the loss convex.
Footer: DL4-03 | Lecture 4 | PDF pp. 37–53
```

### DL4-04

```text
TITLE: Curvature approximations and learning-rate schedules
Exact approved page content:
1) Avoid storing the full Hessian
BFGS updates a curvature approximation from parameter/gradient differences.
L-BFGS retains a limited history, reducing memory needs.
Levenberg–Marquardt uses a damped least-squares system (JᵀJ+λI)s=Jᵀr.
Here J is the residual Jacobian; damping λ is not the learning rate.
These methods differ in assumptions, memory and per-step cost.

2) Explicit schedule conventions
Use t=0 for the initial learning rate η₀.
Inverse-time: η_t=η₀/(1+t).
Inverse-quadratic (lecture formula): η_t=η₀/(1+t)².
Exponential: η_t=η₀γ^t, 0<γ<1.
Names vary; write the exact formula and index before substituting.

3) Practice: η₀=0.1, γ=0.5
t | inverse-time | inverse-quadratic | exponential
0 | 0.100000 | 0.100000 | 0.100000
1 | 0.050000 | 0.025000 | 0.050000
2 | 0.033333 | 0.011111 | 0.025000
3 | 0.025000 | 0.006250 | 0.012500
Plateau policy: if chosen validation metric stagnates, multiply η by γ.
For γ=0.1, two reductions change 0.1→0.01→0.001.
Continue from current weights; a reduction does not restart training.

4) Interpretation and limits
Large steps explore faster but may destabilize; smaller steps can settle.
Deliberate divergence is not a general prescription for escaping local minima.
Decay cannot fix wrong derivatives, unsuitable data or an insufficient model.
Validation guides scheduling; reserve the test set for final evaluation.
Footer: DL4-04 | Lecture 4 | PDF pp. 53–60
```

### DL4-05

```text
TITLE: RProp: sign-based steps with rollback
Exact approved page content:
1) State the variant before calculating
RProp maintains a separate step magnitude for each parameter.
The lecture's simplified variant retries after undoing a sign-flipping step.
Let s>0 be step magnitude, d=sign(old gradient), trial=w−sd.
Compute the gradient at trial BEFORE accepting that trial.
Same sign: accept trial and grow next s by α>1 (up to s_max).
Sign flip: reject trial, restore old w, shrink s by β<1 (down to s_min).
Retry from restored w in the old descent direction.
Other RProp variants handle reversals differently; do not mix their rules.

2) Practice with E(w)=1/2(w−1)²
Gradient g(w)=w−1; start w=0; s=0.6.
α=1.2; β=0.5; bounds do not bind; initial sign d=−1.
Trial1: 0−0.6(−1)=0.6; g=−0.4, same sign.
Accept w=0.6; next s=0.72.
Trial2: 0.6−0.72(−1)=1.32; g=+0.32, sign flip.
Reject 1.32; restore w=0.6; shrink s=0.36.
Retry: 0.6−0.36(−1)=0.96; g=−0.04, same sign.
Accept w=0.96; next s=0.432.
Errors E(0.6)=0.08; E(0.96)=0.0008.

3) Why bookkeeping matters
Rejected trials do not become the accepted parameter state.
Keep the previous accepted sign during a rollback retry.
Gradient magnitude does not set the displacement; sign and stored step do.
Treat a zero gradient explicitly (stop this scalar example at w=1).
Sign changes can reflect stochastic noise; this variant is illustrated with full loss.
Footer: DL4-05 | Lecture 4 | PDF pp. 61–74
```

### DL4-06

```text
TITLE: Momentum: accumulate consistent descent directions
Exact approved page content:
1) Define a displacement convention
v_t=μv_(t−1)−ηg(w_t); w_(t+1)=w_t+v_t.
Here v is a signed parameter displacement, not a raw gradient average.
0≤μ<1 retains part of the previous displacement.
Some books use gradient EMA with (1−μ); translate formulas before comparing η.
Consistent signs reinforce; alternating signs partly cancel.

2) Practice: E(w)=1/2w², g(w)=w
w₀=2; v_(−1)=0; μ=0.9; η=0.1.
Step1: g₀=2.
v₀=0.9(0)−0.1(2)=−0.2; w₁=1.8.
Step2: g₁=1.8.
v₁=0.9(−0.2)−0.1(1.8)=−0.36; w₂=1.44.
Plain GD with the same η: w₁=1.8; w₂=1.62.
Loss after two steps: momentum=1.0368; plain GD=1.3122.
This example improves faster; that is not a universal guarantee.

3) Persistent gradients
If g is constant and v initially zero,
v_t=−ηg(1+μ+⋯+μ^t).
As t grows, v approaches −ηg/(1−μ).
For μ=0.9 the limiting displacement is 10 times one plain-gradient step.
Thus η and μ must be chosen together; momentum can overshoot.

4) Full-network use
Keep one velocity tensor per parameter tensor, including trainable biases.
Compute all current gradients before updating parameters.
Velocity carries across steps and mini-batches; do not reset each batch.
Footer: DL4-06 | Lecture 4 | PDF pp. 75–85
```

### DL4-07

```text
TITLE: Nesterov momentum: compute the gradient after lookahead
Exact approved page content:
1) Reverse the order of the two operations
Momentum evaluates the gradient at the current parameter.
Nesterov first looks ahead along the old velocity.
u_t=w_t+μv_(t−1).
v_t=μv_(t−1)−ηg(u_t); w_(t+1)=w_t+v_t.
Use one consistent displacement convention for both methods.

2) Practice: E(w)=1/2w²; g(w)=w
w₀=2; v_(−1)=0; μ=0.9; η=0.1.
Step1 lookahead u₀=2; g(u₀)=2.
v₀=−0.2; w₁=1.8.
Step2 lookahead u₁=1.8+0.9(−0.2)=1.62.
g(u₁)=1.62.
v₁=0.9(−0.2)−0.1(1.62)=−0.342.
w₂=1.8−0.342=1.458.

3) Compare the same starting state
Plain GD: w₂=1.62.
Classical momentum: w₂=1.44.
Nesterov: w₂=1.458.
Nesterov's second gradient is 1.62, not 1.8.
Do not add the lookahead displacement twice.
This toy result does not rank the methods for every loss.

4) Interpretation
Lookahead lets the gradient react to the motion momentum is about to create.
For a network, forward and backward must use the lookahead parameters.
The temporary u is used to evaluate the gradient; w_new=w_old+v_new.
In mini-batch training, compute the lookahead gradient on the CURRENT batch.
Footer: DL4-07 | Lecture 4 | PDF pp. 86–94
```

### DL5-01

```text
TITLE: Batch, SGD and mini-batches: order and update counts
Exact approved page content:
1) Three ways to estimate a gradient
J(w)=(1/N)Σ_i ℓ_i(w); full-batch g=(1/N)Σ_i ∇ℓ_i(w).
SGD uses one selected example; mini-batch averages B current examples.
One epoch visits the training set once; one update is one optimizer step.
Shuffle between epochs; different orders can change the SGD trajectory.

2) Practice: full batch versus sequential updates
Two examples have losses ℓ₁=1/2(w−1)² and ℓ₂=1/2(w−3)².
Start w=0; η=0.1; gradients g₁=w−1, g₂=w−3.
Full batch: mean gradient=(−1−3)/2=−2 → w=0.2.
SGD order 1 then 2: w=0.1; next g₂=0.1−3=−2.9 →w=0.39.
Reverse order: w=0.3; next g₁=−0.7 →w=0.37.
Full batch computes both gradients at ONE state; SGD's second state changed.

3) Practice: count computational work
N=103 examples; batch size B=20; keep the final partial batch.
Mini-batch updates per epoch=ceil(103/20)=6.
Final batch has 3 examples; average its gradient by 3, not by 20.
Ten epochs: 60 mini-batch updates, 1030 SGD updates, or 10 full-batch updates.
All visit 1030 examples, but overhead and parallelism differ.

4) What the comparison means
SGD gets more, noisier updates for the same number of visited examples.
More updates do not guarantee a better solution at equal time or equal work.
Keep shuffle, batch size, loss reduction and update count explicit.
Do not call every mini-batch update an epoch.
Footer: DL5-01 | Lecture 5 | PDF pp. 1–55, 77–82
```

### DL5-02

```text
TITLE: SGD convergence: step-size conditions and fair comparisons
Exact approved page content:
1) Classical diminishing-step conditions
For positive steps η_t, standard stochastic-approximation conditions include
Σ_(t=1)^∞ η_t=∞ and Σ_(t=1)^∞ η_t²<∞.
They accompany assumptions on smoothness, noise and bounded iterates.
They alone do not guarantee a local/global minimum for every neural network.
Convexity/strong convexity and the chosen estimator affect the theorem and rate.

2) Practice: η_t=c/t^p, c>0
Σ 1/t^p diverges when p≤1.
Σ 1/t^(2p) converges when 2p>1.
Both conditions hold for 1/2<p≤1.
p=1: yes; p=0.75: yes; p=0.5: square-sum diverges.
p=1.2: step-sum is finite; constant steps fail the square-sum condition.
These are asymptotic conditions, not a finite-epoch accuracy certificate.

3) Distinguish iterations from work
Illustrative rate models: batch error Cρ^t, 0<ρ<1; SGD error D/t.
Their constants and assumptions matter; neither is a universal nonconvex rate.
Practice C=D=1, ρ=0.9, target error≤0.01.
Batch needs t≥ln(0.01)/ln(0.9), so 44 updates.
SGD needs t≥100, so 100 single-example updates.
If N=1000, batch visits 44000 examples versus SGD's 100.
This arithmetic compares the stated models, not guaranteed real training times.

4) Practical reading
Constant learning rates often keep noisy motion near a solution.
Decay can reduce that motion; monitor overall/validation metrics.
A noisy batch loss can rise even while overall progress improves.
Footer: DL5-02 | Lecture 5 | PDF pp. 53–59, 86, 91
```

### DL5-03

```text
TITLE: Mini-batch estimates: unbiasedness, variance and monitoring
Exact approved page content:
1) Fix the parameter before taking expectations
At fixed w, let G=∇ℓ_I(w), where I is uniformly sampled from N examples.
E[G|w]=(1/N)Σ_i ∇ℓ_i(w)=∇J(w).
For i.i.d. population examples, sample risk estimates population risk.
Uniform finite-dataset sampling estimates empirical risk; distinguish the two.
Mean of B independent draws: Var(G_bar|w)=Var(G|w)/B.
Without replacement, sampling from a finite set needs a finite-population correction.

2) Practice: scalar gradient values at one fixed w
Possible gradients=(−2,0,2,4), each with probability 1/4.
Mean=(−2+0+2+4)/4=1.
Population variance=[(−3)²+(−1)²+1²+3²]/4=5.
B=4 with replacement: variance of batch mean=5/4=1.25.
For a size2 sample without replacement from N=4:
Var(mean)=(5/2)×(4−2)/(4−1)=5/3=1.666667.
For B=4 without replacement, every example is used →variance=0.

3) Loss monitoring
An average of comparable per-example losses is meaningful.
To combine unequal batches, weight each batch mean by its example count.
Practice batch sizes 20 and 3 with mean losses 0.5 and 1:
Overall loss=(20×0.5+3×1)/23=13/23=0.565217.
An unweighted mean of the two batch means gives 0.75, incorrectly.

4) Interpret
Larger batches reduce sampling variance but change update frequency and compute cost.
Do not average gradients evaluated at different w and call that a fixed-w estimate.
Monitor training progress and held-out generalization separately.
Footer: DL5-03 | Lecture 5 | PDF pp. 60–91
```

### DL5-04

```text
TITLE: Mini-batch momentum and Nesterov: preserve the state
Exact approved page content:
1) Same optimizer, changing loss sample
Batch A and batch B can point in different directions.
Keep velocity between batches, but use the current batch gradient.
Momentum: v=μv_old−ηg_batch(w); w_new=w+v.
Nesterov: u=w+μv_old; v=μv_old−ηg_batch(u); w_new=w+v.

2) Practice givens
Batch A loss=1/2(w−1)²; batch B loss=1/2(w−3)².
w₀=0; v_old=0; μ=0.9; η=0.1.
For batch A, g_A(0)=−1.
Both methods: v₁=0.1; w₁=0.1.

3) Momentum on batch B
g_B(w₁)=0.1−3=−2.9.
v₂=0.9(0.1)−0.1(−2.9)=0.38.
w₂=0.1+0.38=0.48.

4) Nesterov on batch B
u₂=0.1+0.9(0.1)=0.19.
g_B(u₂)=0.19−3=−2.81.
v₂=0.09−0.1(−2.81)=0.371.
w₂=0.1+0.371=0.471.
Plain sequential SGD on A then B would end at 0.39.

5) Implementation and interpretation
Velocity smooths directions over time; it does not remove all sampling noise.
Do not reset it at every batch or silently change the loss reduction.
Do not evaluate Nesterov's second gradient on the previous batch A.
All parameter tensors need synchronized lookahead for the batch pass.
Footer: DL5-04 | Lecture 5 | PDF pp. 93–109
```

### DL5-05

```text
TITLE: RMSProp: squared gradients set a coordinate scale
Exact approved page content:
1) Define the convention
For each coordinate: s_t=ρs_(t−1)+(1−ρ)g_t².
w_t=w_(t−1)−ηg_t/(√s_t+ε).
Here ε is OUTSIDE the square root; use this convention throughout.
The slides use √(s+ε); this page declares the outside-root variant.
Square, average over time, then square-root: this is an RMS scale.
s is not a Hessian and is not the squared mean gradient.

2) Practice: two coordinates, two supplied gradients
w₀=(1,1), s₀=(0,0), η=0.1, ρ=0.9, ε=10⁻⁸.
g₁=(2,0.5); g₂=(−1,0.5) are given batch gradients.
s₁=0.1(4,0.25)=(0.4,0.025).
√s₁=(0.632456,0.158114).
First displacement≈(−0.316228,−0.316228).
w₁≈(0.683772,0.683772).
s₂=0.9(0.4,0.025)+0.1(1,0.25)=(0.46,0.0475).
√s₂=(0.678233,0.217945).
Second displacement≈(+0.147442,−0.229416).
w₂≈(0.831214,0.454357).
Compute with unrounded s and ε; displayed values are rounded.

3) Why this helps
Large recent gradient magnitudes enlarge the denominator, reducing effective steps.
A persistent sign flip still leaves squared gradients positive.
Initial zero state can make first effective steps large; η remains important.
Maintain one s tensor for each parameter tensor, including trained biases.
RMSProp adapts scales; it does not itself add a first-moment momentum average.
Footer: DL5-05 | Lecture 5 | PDF pp. 110–118
```

### DL5-06

```text
TITLE: Adam: moments, bias correction and two updates
Exact approved page content:
1) Track both moments
m_t=β₁m_(t−1)+(1−β₁)g_t.
v_t=β₂v_(t−1)+(1−β₂)g_t².
m_hat_t=m_t/(1−β₁^t); v_hat_t=v_t/(1−β₂^t).
w_t=w_(t−1)−η m_hat_t/(√v_hat_t+ε).
Initialize m₀=v₀=0; t counts optimizer updates starting at 1.
ε is outside the square root; v is the uncentered second moment.
This is the outside-root variant; the slides place ε under the root.

2) Practice: a changing gradient
w₀=1; η=0.1; β₁=0.9; β₂=0.99; ε=10⁻⁸.
Given g₁=2, then g₂=−1.
At t=1: m₁=0.2; v₁=0.04.
m_hat₁=0.2/0.1=2; v_hat₁=0.04/0.01=4.
Displacement≈−0.1; w₁≈0.9.
At t=2: m₂=0.9(0.2)+0.1(−1)=0.08.
v₂=0.99(0.04)+0.01(1)=0.0496.
m_hat₂=0.08/(1−0.9²)=0.421053.
v_hat₂=0.0496/(1−0.99²)=2.492462.
Displacement≈−0.026670; w₂≈0.873330.

3) Interpret the sign
Although current g₂ is negative, corrected momentum is still positive.
Adam can continue moving downward because its first moment retains history.
The corrections compensate for initialization at zero; they are not batch averaging.
Adam still has a learning rate and hyperparameters to choose.
Do not reset the update counter each epoch or omit either correction.
AdaGrad accumulates all past squared gradients; RMSProp exponentially discounts them.
The slides also name AdaDelta and AdaMax; they are distinct adaptive variants.
Adaptive scaling is not a universal convergence or generalization guarantee.
Footer: DL5-06 | Lecture 5 | PDF pp. 119–124
```

### DL5-07

```text
TITLE: Generalization and L2: objective, gradient and decay
Exact approved page content:
1) Diagnose overfitting
Training loss falls while validation loss worsens: fit may be memorizing detail.
More data, suitable architecture and regularization can reduce overfitting.
Depth or small training error alone does not guarantee good held-out performance.
L1 encourages sparsity; L2 penalizes squared weight magnitudes.

2) State the regularized objective
J_total(w,b)=J_data(w,b)+(λ/2)||w||²; λ≥0.
Here J_data is mean loss and biases are NOT penalized.
∇_w J_total=∇_w J_data+λw.
For plain SGD: w_new=(1−ηλ)w−η∇_w J_data.
b_new=b−η∂J_data/∂b.
Scaling the penalty by 1/N would change λ's numerical meaning.

3) Complete practice update
w=(2,−1), b=0.5; J_data=0.8; λ=0.2; η=0.1.
Given data gradient g_w=(0.4,−0.3), g_b=0.2.
Penalty=(0.2/2)(4+1)=0.5; J_total=1.3.
Regularization gradient=0.2(2,−1)=(0.4,−0.2).
Total g_w=(0.8,−0.5).
w_new=(2,−1)−0.1(0.8,−0.5)=(1.92,−0.95).
b_new=0.5−0.1(0.2)=0.48.
Decay form: 0.98(2,−1)−0.1(0.4,−0.3) gives the same weights.

4) Important limitation
The equivalence above is for plain SGD with this convention.
Adding λw inside Adam's adaptive gradient is not generally decoupled weight decay.
Choose λ using validation data; the penalty does not automatically enforce smoothness everywhere.
Footer: DL5-07 | Lecture 5 | PDF pp. 125–144
```

### DL5-08

```text
TITLE: Dropout: masked learning and both scaling conventions
Exact approved page content:
1) Idea and assumptions
Bagging trains models on resampled data and averages predictions.
Dropout samples subnetworks that SHARE parameters; it discourages co-adaptation.
For each dropped layer, sample r_j~Bernoulli(q), q=keep probability.
Masks change across training examples/passes; typically leave output units intact.
With n droppable units there are 2^n binary masks, not 2^n separately stored models.

2) Inverted dropout (used in this practice)
Training activation h_tilde=(r⊙h)/q; inference uses h unchanged.
E[h_tilde|h]=h; backprop multiplies upstream gradients by r/q.
Practice h=(2,4), q=0.5, r=(1,0), output weights u=(1,0.5), b=1.
h_tilde=(4,0); output z=uᵀh_tilde+b=5.
For target y=3 and loss 1/2(z−y)²: loss=2; δ=z−y=2.
Gradient to u: δh_tilde=(8,0); bias gradient=2.
Gradient to h: δu⊙r/q=(4,0).
The dropped coordinate receives zero gradient in this masked data pass.
At inference z=uᵀh+b=2+2+1=5.

3) Ordinary dropout convention
Training uses r⊙h without dividing by q.
Inference uses qh, or multiplies outgoing weights by q.
For the same h,u,b: ordinary-convention inference z=0.5(2+2)+1=3.
Scale outgoing weights of dropped units, not the bias or every weight indiscriminately.
Do not apply both inverted training scaling and ordinary test scaling.

4) Interpret carefully
Expected activations match under the chosen convention.
Nonlinear full-network inference is generally an approximation to averaging subnetworks.
Dropout is a training regularizer; disable random masks for ordinary evaluation.
Footer: DL5-08 | Lecture 5 | PDF pp. 145–158
```

### DL5-09

```text
TITLE: Gradient clipping: coordinate limits versus norm limits
Exact approved page content:
1) Why clip?
Large gradients can cause very large parameter steps.
Clip the computed gradient before the optimizer uses it.
Clipping controls the update input; it does not repair the source of instability.
Negative gradients must be bounded too; positive-only clipping is incomplete.

2) Coordinate clipping
g_clip,j=min(c,max(−c,g_j)), c>0.
Practice g=(6,−8), c=5.
Coordinate result=(5,−5); norm=√50=7.071068.
Each coordinate is within [−5,5], but the vector norm can exceed 5.
The direction generally changes because coordinates scale differently.

3) Global norm clipping
g_clip=g×min(1,c/||g||₂).
For g=(6,−8), ||g||₂=10 and c=5.
Scale=0.5; clipped result=(3,−4); norm=5.
The original direction is preserved when the vector is scaled.
For ||g||₂≤c, leave the gradient unchanged; zero vector stays zero.

4) Compare SGD updates
w=(1,1); η=0.1.
No clipping: w_new=(1,1)−0.1(6,−8)=(0.4,1.8).
Coordinate clipping: w_new=(0.5,1.5).
Norm clipping: w_new=(0.7,1.4).
Same threshold c gives different rules and different new parameters.

5) Keep the scope explicit
Global norm can be over all parameter gradients, not one arbitrary tensor.
Clipping interacts with momentum/adaptive state; specify where it is applied.
Footer: DL5-09 | Lecture 5 | PDF pp. 161
```

### DL5-10

```text
TITLE: Practical training: normalization, initialization and model selection
Exact approved page content:
1) Standardize using training statistics
x'_j=(x_j−μ_train,j)/σ_train,j.
Practice training feature values (1,3,5): μ=3, population variance=8/3.
σ=1.632993; normalized values=(−1.224745,0,1.224745).
A test value 7 transforms to (7−3)/1.632993=2.449490.
Do not recompute μ,σ on test data; handle constant features explicitly.
Input standardization is not the same operation as batch normalization.
Batch norm uses batch statistics during training and stored statistics for evaluation.

2) Initialize to break symmetry
Identical hidden units initialized identically can receive identical updates.
This assumes identical deterministic treatment; independent dropout can break symmetry.
Use suitable random weight scales; a common bias initialization is zero.
Optional scale examples: Xavier normal SD=√[2/(fan_in+fan_out)].
He normal SD=√(2/fan_in), often paired with ReLU.
For fan_in=4, fan_out=2: Xavier SD=0.577350; He SD=0.707107.
These are activation-dependent starting choices, not guarantees.

3) Early stopping and run selection
Practice epochs 1,2,3,4: validation losses=(0.7,0.5,0.4,0.45).
Best saved checkpoint is epoch3, even if training loss keeps falling.
With patience1 and no improvement at epoch4, stop and restore epoch3.
State patience/minimum improvement rules; choose architecture and η on validation.
Evaluate the selected model on the untouched test set.

4) Augment and monitor
Use label-preserving training transformations, such as suitable image translations.
Not every flip/crop preserves every task's label.
Log loss, relevant task metrics, learning rate, batch size and random seed.
Use correct output/loss pairs and inspect gradients before tuning more settings.
Footer: DL5-10 | Lecture 5 | PDF pp. 143, 159–160, 162–165
```

## Targeted corrections

DL2-02-v2: edit only the batch mean equation to visibly render J=(0.854355+1.171101)/2=1.012728, as a fraction with denominator2. Preserve every other value, line and style. Root and independent reviewer recheck the full page.

DL3-03-v2: clarify the empirical-risk input subscript as x_n to match sum_n and t_n, preserving the full page.

DL5-06-v2: clarify Adam denominator as (sqrt(v_hat_t)+epsilon), with a short radical bar over v_hat_t only and epsilon clearly outside. Preserve all other equations, numericals and text.
