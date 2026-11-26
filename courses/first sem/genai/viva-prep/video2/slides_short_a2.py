# Condensed viva-questions video for Assignment 2 (about 12 minutes).
# Every fact is taken from slides_q_a2.py; visual slides reuse its exact fields.

SLIDES = [
    dict(
        section="Intro",
        title="Nine viva questions, short version",
        kind="text",
        bullets=[
            "Nine real viva questions, in the order they were asked",
            "Each: one key visual, then a spoken model answer",
            "Bar ¯ = running product: ᾱt = α0 · α1 · … · αt",
            "Hat ^ = an estimate: x̂0 is the model's guess of the clean image",
        ],
        narration=(
            "Welcome. This is the short version of the Assignment 2 viva questions. "
            "For each of the nine questions, we look at one key visual, then hear a short model answer "
            "and the most likely follow-up. Two symbols first. A bar on top means a running product, so alpha bar t is "
            "alpha zero times alpha one, all the way up to alpha t. And a hat means an estimate, so x hat zero "
            "is the model's guess of the clean image."
        ),
    ),
    # ---------------- Q1
    dict(
        section="Q1 · Beta vs alpha",
        title="Q1 · Code: betas in, alphas and alpha bars out",
        kind="code",
        src="A2NB",
        start="class Schedule:",
        n=14,
        hl=["self.betas = betas.to(DEVICE)", "self.alphas = 1.0 - self.betas",
            "torch.cumprod(self.alphas, dim=0)", '"linear": Schedule("linear", linear_betas(T))'],
        bullets=[
            "We only ever choose betas; everything else is derived",
            "alphas = 1 − betas, element by element",
            "alpha_bars = torch.cumprod: the running product of the alphas",
        ],
        narration=(
            "Question one: what is the difference between beta and alpha? Our Schedule class shows it in "
            "three lines. First, we store the betas. These are the only numbers we actually choose, one per step. "
            "Next, alphas equals one minus betas, element by element. Then alpha bars come from torch dot cumprod, "
            "the running product of the alphas. So beta is the noise you add, alpha is the signal you keep, "
            "and beta fully decides the other two."
        ),
    ),
    dict(
        section="Q1 · Beta vs alpha",
        title="Q: What is the difference between β and α? · model answer",
        kind="text",
        bullets=[
            "βt = noise variance added at step t; αt = 1 − βt = signal variance kept",
            "β, α: per step; ᾱt = product of all α up to t (cumulative)",
            "We choose β (linear: 10⁻⁴ → 0.02); α and ᾱ are derived in code",
            "Follow-up: 'Why must β stay below 1?' β = 1 → α = 0 → divide by zero",
        ],
        narration=(
            "A model answer. Beta t is the variance of the noise we add at one step t. Alpha t is one minus "
            "beta t, the share of the signal's variance that survives that step. So the two add up to one. "
            "Beta and alpha describe one step only. Alpha bar t is the cumulative one: the product of all the "
            "alphas up to t. In our code we only choose the betas, from ten to the minus four to 0.02 for linear. "
            "A likely follow-up: why must beta stay below one? If beta were one, alpha would be zero, and the "
            "sampler divides by root alpha, so it would divide by zero."
        ),
    ),
    # ---------------- Q2
    dict(
        section="Q2 · Alpha bar t",
        title="Q2 · Saved output: our printed ᾱt values",
        kind="output",
        src="A2OUT",
        start="saved A1_alpha_bar.png",
        n=5,
        hl=["linear  0.99990", "cosine  0.99996"],
        bullets=[
            "Columns t = 0, 100, 250, 500, 750, 999",
            "t = 250: linear 0.521, cosine 0.846",
            "t = 500: linear 0.078, cosine 0.492",
            "t = 750: linear 0.0033, cosine 0.143",
        ],
        narration=(
            "Question two: what is alpha bar t? Here are our actual values, from the saved output. "
            "Each number is the share of the clean image's variance still left at that step. Both start "
            "almost at one. At step 250, linear keeps 0.521 and cosine 0.846. At step 500, linear keeps only "
            "0.078, while cosine still keeps 0.492. By 750, linear is practically pure noise."
        ),
    ),
    dict(
        section="Q2 · Alpha bar t",
        title="Q: What is ᾱt (alpha bar t)? · model answer",
        kind="text",
        bullets=[
            "ᾱt = α0 · α1 · … · αt: the running product of the alphas",
            "It is the share of the clean image's variance left in xt",
            "Closed form: xt = √ᾱt x0 + √(1 − ᾱt) ε, so we jump to any t at once",
            "Follow-up: 'Why square roots?' ᾱ + (1 − ᾱ) = 1: variance preserving",
        ],
        narration=(
            "A model answer. Alpha bar t is the running product of the alphas, alpha zero times alpha one up to "
            "alpha t. It tells us what share of the clean image's variance is still left in x t. Near one, almost "
            "clean. Near zero, almost pure noise. It gives us the closed form: x t equals root alpha bar t times "
            "x zero, plus root of one minus alpha bar t times epsilon, the Gaussian noise."
            " A likely follow-up: why the square roots? So the signal variance and the noise "
            "variance add up to one at every step. That is called variance preserving."
        ),
    ),
    # ---------------- Q3
    dict(
        section="Q3 · Linear vs cosine",
        title="Q3 · Result: where the ᾱ curves differ",
        kind="figure",
        image="A2F/A1_alpha_bar.png",
        bullets=[
            "x-axis: timestep t, 0 to 999; y-axis: ᾱt; dotted line at 0.5",
            "Linear falls fast: ᾱ < 0.5 at t = 259, < 0.01 at t = 673",
            "Cosine falls slowly and steadily: < 0.5 at t = 496, < 0.01 at t = 935",
        ],
        narration=(
            "Question three: linear versus cosine. This figure is the heart of the answer. The horizontal axis "
            "is the step t, the vertical axis is alpha bar t, and the dotted line marks one half. Linear falls "
            "fast. It crosses one half at step 259, and is below 0.01 from step 673. Cosine falls slowly and "
            "steadily, crossing one half at 496, and reaching 0.01 only at 935."
        ),
    ),
    dict(
        section="Q3 · Linear vs cosine",
        title="Q: Linear vs cosine schedule? · model answer",
        kind="text",
        bullets=[
            "Linear sets β directly (10⁻⁴ → 0.02); cosine sets the ᾱ curve, β is derived",
            "Linear destroys faster: ᾱ < 0.5 at t = 259 vs 496 for cosine",
            "Cosine β is clipped at 0.999, so it needs x̂0 clipping",
            "Follow-up: 'Cosine loss 0.050 > linear 0.028?' Not comparable",
        ],
        narration=(
            "A model answer. The linear schedule chooses beta directly, evenly from ten to the minus four to 0.02. "
            "The cosine schedule chooses alpha bar directly, as a smooth cosine curve, and derives each beta from it. "
            "Linear destroys the image faster; cosine spreads the noise levels more evenly. "
            "Cosine's last beta is clipped at 0.999, which makes the last reverse step extreme, so our cosine model "
            "needs x hat zero clipping. A likely follow-up: the cosine loss was 0.050 and linear 0.028, so is linear "
            "better? No. The same t means a different noise level in each schedule, so the losses are not comparable."
        ),
    ),
    # ---------------- Q4
    dict(
        section="Q4 · Sampling",
        title="Q4 · Diagram: one reverse step with x̂0 clipping",
        kind="figure",
        image="DG/x0hat_clipping.png",
        bullets=[
            "U-Net gives εθ → compute x̂0 → clamp to [−1, 1]",
            "Recompute ε from the clamped x̂0, then the unchanged handout update",
            "Clipping happens INSIDE every step, not after sampling",
        ],
        narration=(
            "Question four: explain sampling. This diagram is one reverse step. The U-Net looks at x t and t, and "
            "gives epsilon theta, its guess of the noise. We turn that into x hat zero, the guess of the clean image, "
            "and clamp it to the range minus one to one. Then we recompute the matching noise "
            "and use the unchanged handout update. The clamp sits inside every step, not once at the end."
        ),
    ),
    dict(
        section="Q4 · Sampling",
        title="Q: Explain the sampling step · model answer",
        kind="text",
        bullets=[
            "Start from pure noise x999; for t = 999 … 0, the U-Net predicts εθ(xt, t)",
            "Remove a slice βt/√(1 − ᾱt) of it, rescale by 1/√αt: the mean",
            "Add fresh noise √βt · z, except at t = 0",
            "Follow-up: 'Why add noise?' Keeps it stochastic: samples the whole distribution",
        ],
        narration=(
            "A model answer. Sampling starts from pure Gaussian noise, x 999, and runs t from 999 down to zero. "
            "At each step the U-Net predicts the noise, epsilon theta. We remove a small slice of it, beta t over "
            "the root of one minus alpha bar t, and rescale by one over root alpha t, which undoes the shrinking of "
            "the forward step. That gives the mean. Then we add fresh noise of size root beta t, except at the last "
            "step. "
            "A likely follow-up: why add noise at all? Without it, the sampler would collapse towards one blurry "
            "average image."
        ),
    ),
    # ---------------- Q5
    dict(
        section="Q5 · Why the timestep",
        title="Q5 · Diagram: t is used twice in every reverse step",
        kind="figure",
        image="DG/sampling_t.png",
        bullets=[
            "t is INPUT to the U-Net: the time embedding says how noisy xt is",
            "t LOOKS UP αt, ᾱt, βt, σt from the schedule",
            "Wrong t or skipped steps: wrong noise guess and wrong coefficients",
        ],
        narration=(
            "Question five: why do we depend on the timestep when sampling? The diagram shows that t is used twice "
            "in every step. First, it is an input to the U-Net, turned into a time embedding that tells the network "
            "how noisy x t is. Second, it looks up the coefficients, alpha t, alpha bar t, beta t and sigma t, from "
            "the schedule. A wrong t gives a wrong noise guess and wrong coefficients."
        ),
    ),
    dict(
        section="Q5 · Why the timestep",
        title="Q: Why depend on the timestep when sampling? · model answer",
        kind="text",
        bullets=[
            "Use 1: t is a network INPUT: one shared U-Net, told the noise level",
            "Use 2: t LOOKS UP the coefficients 1/√αt, βt/√(1 − ᾱt) and σt",
            "Each step removes only a little noise and needs the previous output",
            "Follow-up: '1000 calls to sample, 1 to train?' Training jumps to a random t",
        ],
        narration=(
            "A model answer. The noise level is different at every step, and t does two jobs. One U-Net is shared "
            "by all 1000 noise levels, so it is told t, and then it can scale its noise guess correctly. And t looks "
            "up the coefficients: one over root alpha t, beta t over root of one minus alpha bar t, and sigma t. We "
            "must go in order, because each step only removes a little noise and needs the previous step's output. "
            "A likely follow-up: why 1000 calls to sample but one to train? In training, the closed form jumps "
            "straight to a random t. Sampling has no closed form backwards, so it is a chain."
        ),
    ),
    # ---------------- Q6
    dict(
        section="Q6 · The plots",
        title="Q6 · Plot: sixteen samples from each model",
        kind="figure",
        image="A2F/A3_samples_linear.png",
        image2="A2F/A3_samples_cosine.png",
        bullets=[
            "Top: linear model; bottom: cosine model; 4 × 4 grid each, clipped sampler",
            "Same seed: both start from the same 16 noise images",
            "Linear: a good mix, about 4–5 sandals, 7 bags, 3 trousers",
            "Cosine: mostly bright bag-like shapes, 2 sandals, 2 trousers",
        ],
        narration=(
            "Question six: walk me through your plots. For each plot, name the axes, say what to notice, and give "
            "the conclusion. The alpha bar curves you saw in question three. Next, the sample grids: linear on top, "
            "cosine below, both from the same seed, with all 1000 steps. Linear gives a good mix of sandals, bags "
            "and trousers. Cosine is dominated by bright, bag-like shapes. So for our classes, linear looks better, "
            "but that is a visual judgement from sixteen samples."
        ),
    ),
    dict(
        section="Q6 · The plots",
        title="Q6 · Plot: the no-clipping ablation",
        kind="figure",
        image="A2F/A3_linear_no_clip.png",
        image2="A2F/A3_cosine_no_clip.png",
        bullets=[
            "Literal handout formula, no x̂0 clipping; same models and seed",
            "Top: linear, still recognisable (mean change 0.0507 per pixel)",
            "Bottom: cosine, black: 62.5% of pixels stuck at −1",
            "Cause: β999 = 0.999 → 1/√α999 = 31.6 at the first step",
        ],
        narration=(
            "The ablation: we switched off x hat zero clipping and ran the literal handout formula. Linear still makes "
            "recognisable items; the mean change per pixel is only 0.0507. Cosine comes out black, with 62.5 percent "
            "of pixels stuck at minus one. It is a sampling problem, not a training failure: at step 999, beta is "
            "0.999, so the first step multiplies errors by 31.6."
        ),
    ),
    dict(
        section="Q6 · The plots",
        title="Q: Walk me through your plots · model answer",
        kind="text",
        bullets=[
            "For each plot: name the axes, say what to notice, give the conclusion",
            "ᾱ curves: linear destroys faster (259 vs 496)",
            "Samples: linear looks better; no-clip ablation: cosine needs x̂0 clipping",
            "Follow-up: 'Why is the first x̂0 panel noise?' Divide by tiny √ᾱt",
        ],
        narration=(
            "A model answer. The alpha bar curves show linear destroys the image faster, crossing one half at step "
            "259 against 496. "
            "The sample grids show recognisable items from both, and linear looks better to us. The ablation shows "
            "our cosine model needs x hat zero clipping, while linear barely changes. And in Part B, both confusion "
            "matrices are diagonal, 30 out of 30. A likely follow-up: why is the first x hat zero panel in the "
            "trajectory just noise? Because x hat zero divides by root alpha bar, which is tiny at step 999."
        ),
    ),
    # ---------------- Q7
    dict(
        section="Q7 · Linear probing",
        title="Q7 · Diagram: the linear probe",
        kind="figure",
        image="DG/linear_probe.png",
        bullets=[
            "Frozen backbone → one 768-number feature vector per photo",
            "StandardScaler → logistic regression → one of 4 classes",
            "Only the logistic regression is trained: about 3,000 numbers",
        ],
        narration=(
            "Question seven: what is linear probing? A photo goes into the frozen backbone, ViT or Swin, and comes out "
            "as one feature vector of 768 numbers. A standard scaler puts every "
            "feature on the same scale, and logistic regression picks one of the four classes. Only that last box is "
            "trained, roughly three thousand numbers."
        ),
    ),
    dict(
        section="Q7 · Linear probing",
        title="Q: What is linear probing, and why use it? · model answer",
        kind="text",
        bullets=[
            "Freeze the backbone, extract one feature vector, train only a linear classifier",
            "Measures how linearly separable the PRETRAINED features are",
            "Ours: both 30/30; log-loss ViT 0.0113 vs Swin 0.0168",
            "Follow-up: 'Why not fine-tune?' 70 photos: too few; it changes the backbone",
        ],
        narration=(
            "A model answer. Linear probing means we freeze a pretrained backbone, turn each image into one feature "
            "vector, and train only a linear classifier on top, here logistic regression. Frozen, it tells us how "
            "linearly separable the pretrained features already are. Both backbones get the same probe and the same "
            "split. Both got all 30 test photos right. ViT was very "
            "slightly more confident, with a log loss of 0.0113 against 0.0168, so they are effectively equal. A likely "
            "follow-up: why not fine tune? With only 70 training photos it would overfit, and it would change the very "
            "features we want to compare."
        ),
    ),
    # ---------------- Q8
    dict(
        section="Q8 · Swin vs ViT",
        title="Q8 · Swin: windows, shifted windows, and four stages",
        kind="figure",
        image="DG/swin_stages.png",
        bullets=[
            "4 × 4 patches: 56 × 56 tokens, 96 channels",
            "Attention only inside 7 × 7 windows (49 tokens)",
            "Every 2nd block shifts windows: neighbours exchange information",
            "Patch merging: grid ÷ 2, channels × 2 → 56, 28, 14, 7",
        ],
        narration=(
            "Question eight: Swin versus ViT. This is Swin. It cuts the image into small 4 by 4 patches, so 56 by 56 "
            "tokens. Attention happens only inside 7 by 7 windows, 49 tokens each. Every second block shifts the "
            "windows, so neighbouring windows exchange information. Patch merging then halves the grid and doubles "
            "the channels, giving four stages, 56, 28, 14 and 7 per side, like a convolutional network."
        ),
    ),
    dict(
        section="Q8 · Swin vs ViT",
        title="Q: Swin vs ViT? · model answer",
        kind="text",
        bullets=[
            "ViT: 16×16 patches, 197 tokens, global attention, one scale (stride 16)",
            "Swin: 4×4 patches, 7×7 shifted windows, 4 stages at strides 4–32",
            "Cost: ViT grows with (hw)², Swin linearly; Part C: 42× cheaper, not 256×",
            "Follow-up: 'What does the shift do?' Lets windows exchange information",
        ],
        narration=(
            "A model answer. ViT cuts the image into 16 by 16 patches, adds a CLS token to get 197 tokens, and uses "
            "global attention, where every token attends to every token, at one single scale, stride 16. Swin uses "
            "4 by 4 patches, attention inside 7 by 7 windows, and four stages at strides 4, 8, 16 and 32. The big "
            "difference is cost. Global attention grows quadratically with the number of tokens. In a window each "
            "query sees only 49 keys, so Swin grows linearly. In my Part C, window attention was about 42 times cheaper, "
            "not 256. A likely follow-up: what does the shift do? "
            "Without it, tokens in different windows never meet."
        ),
    ),
    # ---------------- Q9
    dict(
        section="Q9 · FPN and detection",
        title="Q9 · Diagram: Swin stages → FPN → detection heads",
        kind="figure",
        image="DG/swin_fpn.png",
        bullets=[
            "Left: Swin stages 1–4, strides 4, 8, 16, 32 (features_only=True)",
            "Middle: FPN, 1×1 lateral convs + top-down ×2 upsample-and-add → P2–P5",
            "Right: ViT gives one 14 × 14 map at stride 16: nothing to combine",
            "Our A2: classification + feature probing only",
        ],
        narration=(
            "Question nine: what is an FPN, and how is Swin used for detection? On the left, Swin's four stages, at "
            "strides 4, 8, 16 and 32. In the middle, the feature pyramid network: one by one lateral convolutions, then "
            "a top-down path that upsamples each coarser map by two and adds it in, giving P2 to P5."
            " On the right, ViT has one 14 by 14 map at stride 16, so there is nothing to combine."
        ),
    ),
    dict(
        section="Q9 · FPN and detection",
        title="Q: What is an FPN, and how is Swin used for detection? · model answer",
        kind="text",
        bullets=[
            "Detection needs features at several scales: small and large objects",
            "Top-down brings meaning to fine maps; lateral brings high-resolution detail",
            "Swin's 4 stages plug straight in; ViT needs adapters (e.g. ViTDet)",
            "Follow-up: 'Did you train a detector?' No: features_only gave the 4 maps",
        ],
        narration=(
            "A model answer. Detection must find objects of very different sizes, so it needs feature maps at several "
            "scales. An FPN takes the backbone's stages, applies a one by one lateral convolution to each, then goes "
            "top down, upsampling the coarser map and adding it to the finer one. The top-down path brings meaning to "
            "the fine maps; the lateral path brings back detail. Swin's four stages are exactly "
            "that pyramid, like a ResNet's C2 to C5, so they plug straight in. A plain ViT has one stride 16 map, so it "
            "needs an adapter, such as ViTDet. A likely follow-up: did you train a detector? No. Features only gave us "
            "the four maps, but we built no FPN and trained no detector."
        ),
    ),
]
