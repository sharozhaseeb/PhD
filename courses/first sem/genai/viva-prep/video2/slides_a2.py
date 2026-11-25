"""Slow, beginner-friendly narrated walkthrough of GenAI Assignment 2 (CS5004), 26L-9005, d = 5.

Format: see SPEC.md. Handout phrases come from ref/A2_handout_pages.txt, code starts from
ref/A2_notebook_cells.txt (src="A2NB"), figures use the A2F/ prefix.
"""

SLIDES = [

# =====================================================================  INTRO
dict(
    section="Intro",
    title="The rules and your personal settings",
    kind="handout",
    page=1,
    find=[
        "personalised by the last digit of your roll number",
        "explain every line of your code",
        "Train only on your three classes: d,",
        "18,000 images (6,000 per class).",
    ],
    bullets=[
        "d = 5, the last digit of 26L-9005",
        "Classes: 5 Sandal, (5+3) mod 10 = 8 Bag, (5+6) mod 10 = 1 Trouser",
        "18,000 training images, 6,000 per class",
        "Part C row for d = 5: 448 × 448 × 3 image, C = 128",
        "Viva rule: explain every line and every number",
    ],
    narration=(
        "Welcome. This is a slow walkthrough of Assignment 2. For every task we read the handout lines, explain the idea, show our code, explain the design decisions, and look at the results. "
        "Page one of the handout. Several tasks are personalised by the last digit of your roll number, "
        "and using another student's settings earns zero. So expect the examiner to start with your settings. "
        "Your digit is 5. Part A trains on classes d, d plus 3 mod 10, and d plus 6 mod 10. "
        "That is 5, Sandal. 5 plus 3 is 8, Bag. 5 plus 6 is 11, and 11 mod 10 is 1, Trouser. "
        "Practise that last one out loud. "
        "Each class has 6,000 images, so 18,000 in total. "
        "For Part C, the row for 5 gives an image of 448 by 448 by 3, with C equal to 128. "
        "And note the rule: you must explain every line of your code and every number in your report."
    ),
),

dict(
    section="Intro",
    title="Code: your personal settings cell",
    kind="code",
    src="A2NB",
    start='ROLL = "26L-9005"',
    n=16,
    hl=['d = int(ROLL[-1])', 'SEED = 9005', 'QUICK_TEST = False', 'drive.mount("/content/drive")'],
    bullets=[
        "d = int(ROLL[-1]): last character of the roll number, as a number: 5",
        "SEED = 9005: the key random draws repeat exactly",
        "QUICK_TEST = False for the real run; quick tests use a separate folder",
        "Outputs saved on Google Drive: a Colab disconnect loses nothing",
        "Saved output: d = 5 | SEED = 9005 | outputs in .../CS5004_A2/outputs",
    ],
    narration=(
        "This is the settings cell, near the top of the notebook. "
        "On line three, d equals int of ROLL, with minus one in square brackets. Minus one picks the last character of the text, which is the 5, "
        "and int turns it into the number 5. So your digit is computed from your roll number, never typed by hand, and every personalised choice later reads d. "
        "On line four, SEED is 9005, also taken from your roll number. Every key random draw in the notebook uses it: "
        "the starting weights of the U-Net, the order of the training data, the sampling noise, and the photo split in Part B. "
        "The alternative, no fixed seed, would give slightly different numbers on every run, and the report could not be reproduced. "
        "On line eight, QUICK TEST is false. When it is true, everything shrinks so the whole notebook runs in a few minutes, just to check the code, "
        "and it writes to a separate folder, so a tiny test checkpoint can never be mistaken for a real one. "
        "On line fifteen, Google Drive is mounted, and all outputs go there. A Colab session can disconnect at any time, and its local disk is then wiped. "
        "With the checkpoints on Drive, a disconnect costs nothing. "
        "The saved output of this cell printed d equals 5, SEED equals 9005, and the outputs folder on Drive."
    ),
),

dict(
    section="Intro",
    title="Loading your three Fashion-MNIST classes",
    kind="code",
    src="A2NB",
    start="MY_CLASSES = [d, (d + 3) % 10, (d + 6) % 10]",
    n=12,
    hl=["torch.isin", "F.pad(x, (2, 2, 2, 2))", "x = x * 2 - 1", "unsqueeze(1)"],
    bullets=[
        "MY_CLASSES computed from d, never typed by hand",
        "torch.isin keeps only labels 5, 8 and 1",
        "Divide by 255, pad 2 pixels each side: 28 × 28 becomes 32 × 32",
        "x * 2 − 1 maps [0, 1] to [−1, 1]",
        "unsqueeze adds the channel: shape (18000, 1, 32, 32)",
    ],
    narration=(
        "The first line computes your classes from d, so the digit is never typed by hand. "
        "The keep line makes a true or false mask: true for every image labelled 5, 8 or 1. "
        "We divide by 255, so pixels go from zero to one. "
        "F dot pad adds two black pixels on every side, so 28 by 28 becomes 32 by 32, as the handout asks. "
        "32 also halves neatly to 16 and 8, which suits the U-Net. "
        "Then x times 2 minus 1 moves the range to minus one to one. "
        "The noise we add later is centred on zero, so the image should be centred on zero too. "
        "Finally unsqueeze adds a channel. The result is 18,000 grayscale images of 32 by 32. "
        "Y TRAIN keeps the labels, but only to count the classes and to title the plots. The U-Net never sees them."
    ),
),

dict(
    section="Intro",
    title="Saved output: your training set",
    kind="output",
    src="A2OUT",
    start="My classes: [(5, 'Sandal')",
    n=3,
    hl=["My classes", "range: -1.0 to 1.0", "per class"],
    bullets=[
        "My classes: (5, Sandal), (8, Bag), (1, Trouser)",
        "18,000 images, shape (18000, 1, 32, 32)",
        "Range −1.0 to 1.0: the scaling worked",
        "6,000 per class: perfectly balanced",
    ],
    narration=(
        "This is the saved output of that cell, from the executed notebook. Nothing was re-run for this video. "
        "The first line prints your classes as pairs of label number and name: 5 Sandal, 8 Bag, and 1 Trouser. "
        "Notice the order follows the formula, d, then d plus 3, then d plus 6, not the label order. "
        "The second line has three fields. Training images, 18,000. "
        "The shape, 18,000 by 1 by 32 by 32: the number of images, one grayscale channel, then height and width after padding. "
        "And the range, minus 1.0 to 1.0. That field is a quick check that the scaling worked. "
        "If it said 0 to 1, we would have forgotten the times two minus one step, and if it said 0 to 255, we would have forgotten to divide. "
        "The last line counts each class: 6,000 sandals, 6,000 bags and 6,000 trousers. "
        "So the data is perfectly balanced, and it matches the handout's 18,000 images, 6,000 per class. "
        "If the examiner asks how you know you trained on the right classes, point at this output."
    ),
),

# =====================================================================  PART A CONCEPTS
dict(
    section="Part A",
    title="Part A · What we may use, and what we must write",
    kind="handout",
    page=1,
    find=[
        "you may use diffusers.UNet2DModel as the network",
        "must be written by you in PyTorch",
        "do not use diffusers schedulers",
    ],
    bullets=[
        "Allowed: diffusers.UNet2DModel, the neural network only",
        "Ours: noise schedules, forward process, training loop, sampling loop",
        "Not allowed: diffusers schedulers or pipelines",
        "Our U-Net is built from a config, so random weights",
    ],
    narration=(
        "Part A is worth 40 percent, and it has a clear rule. "
        "You may use one thing from the diffusers library: the U-Net network, UNet2DModel. "
        "Everything else must be your own PyTorch code: the noise schedules, the forward process, "
        "the training loop, and the sampling loop. No diffusers schedulers or pipelines, because they would do the interesting work for you. "
        "So think of the U-Net as a black box. It takes a noisy image and a timestep, and returns a guess of the noise. "
        "Everything around that box is ours. "
        "If asked what came from a library, the answer is short: only the U-Net architecture, built from a configuration with random weights."
    ),
),

dict(
    section="Part A",
    title="The big idea: two chains",
    kind="figure",
    image="DG/ddpm_chain.png",
    bullets=[
        "Forward chain x0 → x1 → … → xT: add a little noise each step",
        "Forward is fixed: nothing is learned there",
        "Reverse chain xT → … → x0: the U-Net guesses the noise, we remove part of it",
        "Training uses the forward chain; sampling walks the reverse chain",
        "DDPM = Denoising Diffusion Probabilistic Model (Ho et al., 2020)",
    ],
    narration=(
        "Before the code, the big idea, with a diagram. "
        "Along the top, from left to right, you see the forward chain. It starts at x zero, the clean image, "
        "then x one, x two, and so on, up to x T, which is pure noise. Each arrow adds a little random noise. "
        "These forward arrows are called q. They are fixed, and nothing is learned there. "
        "Along the bottom, from right to left, you see the reverse chain. It starts from pure noise. "
        "At each arrow, the U-Net looks at the noisy image and the step number, and guesses the noise inside. "
        "These backward arrows are called p theta, because they are learned. We remove part of the guess, and step by step a new image appears. "
        "That is DDPM, the denoising diffusion probabilistic model. "
        "Training only needs the top chain. Sampling has to walk the bottom chain, one step at a time."
    ),
),

dict(
    section="Part A",
    title="Notation card: hat, bar and theta",
    kind="text",
    bullets=[
        "Hat ^ = an estimate: x̂0 is the model's guess of x0, which it cannot see",
        "Bar ¯ = cumulative product: ᾱt = α0 · α1 · … · αt",
        "θ (theta) subscript = learned by gradient descent: εθ comes from the U-Net",
        "No θ = fixed or randomly drawn: β, α, ᾱ, ε, t, x0",
        "Subscript t = 'at step t'; ~ N(0, I) = drawn from a standard Gaussian",
        "Assignment 3's LoRA α is a different alpha: not the diffusion αt",
    ],
    narration=(
        "Before any formula, a notation card. Keep these three marks in mind for the rest of the video. "
        "A hat on a symbol means an estimate. x hat zero is the model's guess of the clean image, which it cannot see. "
        "A bar on top means a cumulative product. Alpha bar t is every alpha multiplied together, up to step t. "
        "A small theta underneath means learned by gradient descent. Epsilon theta comes out of the U-Net, whose weights are theta. "
        "Anything without theta is either fixed, like beta, alpha and alpha bar, or randomly drawn, like epsilon, t and the training image. "
        "A subscript t just means at step t. And the wavy sign followed by N of zero and I means drawn from a standard Gaussian. "
        "One warning: in Assignment 3, LoRA also has an alpha. That one is a scaling factor, and has nothing to do with the diffusion alpha t."
    ),
),

dict(
    section="Part A",
    title="Formula card: β, α and ᾱ",
    kind="text",
    bullets=[
        "αt = 1 − βt        ᾱt = α0 · α1 · … · αt",
        "t = 0 … 999, so our ᾱt = the paper's ᾱ(t+1); ᾱ0 = 0.9999, not 1",
        "βt (beta t) = noise variance added at step t: 0.0001 up to 0.02",
        "αt (alpha t) = 1 − βt = share of signal variance kept; image scaled by √αt",
        "ᾱt (alpha bar t) = all alphas multiplied = signal variance left after t steps",
        "The bar means 'accumulated': ᾱ near 1 = clean, near 0 = pure noise",
    ],
    narration=(
        "Our first formula card. Whenever a formula appears, we stop and read every symbol. "
        "t is the step number, from 0 to 999. Capital T is the total, 1000 steps. "
        "Beta t is how much noise variance we add at step t. It is small, between 0.0001 and 0.02. "
        "Alpha t is simply one minus beta t: the share of the signal's variance that survives that one step. "
        "If beta is 0.02, alpha is 0.98, so 98 percent of the variance survives, and the image itself is scaled by the square root of 0.98, about 0.99. "
        "Alpha bar t, with a bar on top, multiplies all the alphas from step zero up to step t. "
        "The bar means accumulated. So alpha bar tells you how much of the original signal's variance is left after t steps. "
        "Near one, the image is almost clean. Near zero, it is almost pure noise. "
        "One indexing detail. The DDPM paper counts steps from 1 to T, but our code counts from 0 to 999. "
        "So our alpha bar t is the paper's alpha bar t plus one, and our alpha bar zero already includes one step of noise. "
        "It is 0.9999 for linear and 0.99996 for cosine, very close to one, but not exactly one."
    ),
),

dict(
    section="Part A",
    title="Formula card: the closed form q(xt | x0)",
    kind="text",
    bullets=[
        "q(xt | x0):   xt = √ᾱt · x0 + √(1 − ᾱt) · ε",
        "q( · | x0) = forward process; x0 = clean image; xt = noisy image at step t",
        "ε (epsilon) = random Gaussian noise, mean 0, variance 1",
        "√ᾱt = how much image is kept; √(1 − ᾱt) = how much noise is mixed in",
        "Squared coefficients add to 1: ᾱt + (1 − ᾱt) = 1 ('variance preserving')",
        "Chain of Gaussian steps = one Gaussian: jump to any t in one go",
    ],
    narration=(
        "The most useful formula of Part A, the closed form. "
        "q of x t given x zero is the name of the forward process: the distribution of the noisy image, given the clean one. "
        "x zero is the clean image. x t is the noisy image at step t. "
        "Epsilon is random Gaussian noise, with mean zero and variance one. "
        "The formula says: x t equals the square root of alpha bar t times x zero, plus the square root of one minus alpha bar t, times epsilon. "
        "Think of a mixing desk with two sliders. The first slider keeps some of the image. The second mixes in some noise. "
        "As t grows, the image slider goes down and the noise slider goes up. "
        "The square roots make the two squared coefficients add up to exactly one. So if x zero had variance one, x t would too, at every step. That is why it is called variance preserving. "
        "Why can we jump straight to any step t? Each forward step adds Gaussian noise, and a chain of Gaussian steps is itself one Gaussian. "
        "So the whole chain collapses into this single formula."
    ),
),

# =====================================================================  A1
dict(
    section="Part A · A1",
    title="A1 · What the handout asks (1 of 2)",
    kind="handout",
    page=1,
    find=[
        "Implement the linear schedule",
        "and the cosine schedule (Nichol",
        "against t for both schedules on one figure.",
    ],
    bullets=[
        "Two noise schedules: linear and cosine",
        "Linear: beta goes evenly from 10⁻⁴ to 0.02, T = 1000",
        "Cosine: from Nichol and Dhariwal, 2021",
        "One plot of alpha bar t against t, both curves together",
    ],
    narration=(
        "A1 asks for two noise schedules. "
        "A schedule is just the list of 1000 betas, one per step. It decides how fast the image is destroyed. "
        "The linear schedule starts beta at ten to the minus four and grows it in equal steps up to 0.02. "
        "The cosine schedule, from Nichol and Dhariwal, 2021, instead chooses alpha bar to follow a smooth cosine curve, "
        "and works out the betas from that. "
        "Then plot alpha bar against t for both schedules on one figure. "
        "The instructor asks for this because the alpha bar curve is the clearest picture of how fast each schedule destroys the image."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · What the handout asks (2 of 2)",
    kind="handout",
    page=2,
    find=[
        "Take one training image and show it at",
        "using the closed form",
        "explain which schedule destroys the image faster",
    ],
    bullets=[
        "One training image at six timesteps, for each schedule: a 2 × 6 grid",
        "Use the closed form, not a loop of 1000 steps",
        "3 to 4 sentences: which schedule destroys faster, and why it matters",
    ],
    narration=(
        "A1 continues on page two. Take one training image and show it at steps 0, 100, 250, 500, 750 and 999, "
        "under each schedule. That makes a grid of two rows and six columns. "
        "Use the closed form to make the noisy images. In other words, do not add noise one step at a time in a loop. "
        "Jump straight to each step with one formula. "
        "Then write three or four sentences: which schedule destroys the image faster, and why does that matter for training? "
        "So A1 has three outputs: the alpha bar plot, the grid, and a short written answer."
    ),
),

dict(
    section="Part A · A1",
    title="Formula card: the cosine schedule",
    kind="text",
    bullets=[
        "f(t) = cos²( ((t/T) + s) / (1 + s) · π/2 )        ᾱt = f(t) / f(0)",
        "t/T = how far through the process we are, from 0 to 1",
        "s = 0.008, a small offset so the first steps are not too gentle",
        "π/2 (pi over two): cos² goes smoothly from 1 down to 0",
        "Divide by f(0): the curve starts at 1; our ᾱ0 = f(1)/f(0) = 0.99996",
        "βt = 1 − ᾱ(t+1) / ᾱ(t), clamped at 0.999",
    ],
    narration=(
        "A formula card for the cosine schedule. "
        "t over T is how far through the process we are, from zero at the start to one at the end. "
        "s is a small offset, 0.008, added so the very first steps are not too gentle. "
        "Pi over two is a quarter turn, so the cosine squared slides smoothly from one down to zero. "
        "f of t is that cosine squared curve. Dividing by f of zero makes the curve start at one, before any noise. "
        "Because our steps start at zero, our first alpha bar is f of one over f of zero, which is 0.99996. "
        "Then each beta is worked out from neighbouring alpha bars: one minus alpha bar at t plus one, over alpha bar at t. "
        "In words, the fraction of signal this one step removes. "
        "Finally beta is clamped at 0.999. "
        "Why define alpha bar first and derive beta from it? Because alpha bar is the curve we actually care about, the signal left. "
        "Cosine designs that curve directly, falling slowly at first and steadily through the middle, and beta is just whatever produces it."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Code: the two schedules",
    kind="code",
    src="A2NB",
    start="def linear_betas(T, beta_start=1e-4, beta_end=0.02):",
    n=11,
    hl=["torch.linspace(beta_start, beta_end, T)", "dtype=torch.float64", "alpha_bar = f / f[0]", "betas.clamp(max=0.999)"],
    bullets=[
        "Linear: torch.linspace, 1000 evenly spaced betas",
        "Cosine: f(t) = cos²(((t/T) + s)/(1 + s) · π/2), s = 0.008",
        "alpha bar = f / f[0]: the curve starts at 1 before any noise",
        "beta_t = 1 − ᾱ(t+1)/ᾱ(t), then clamp at 0.999",
        "float64 inside for accuracy, float32 out",
    ],
    narration=(
        "On line five, the linear schedule is one line: torch dot linspace gives T, so 1000, evenly spaced betas from ten to the minus four up to 0.02. "
        "Those two end values are the handout's values. "
        "The cosine one needs more care. On line ten we make the step numbers 0 to 1000. That is T plus one values, "
        "because each beta is a ratio of two neighbouring alpha bars, so 1001 alpha bars give 1000 betas. "
        "We use float 64, double precision, because near the end alpha bar becomes tiny, and dividing tiny numbers in single precision loses accuracy. "
        "On line eleven, f is cos squared of t over T plus s, divided by one plus s, times pi over two. s is 0.008. It stops the first betas from being almost zero. "
        "On line twelve, dividing by f of zero makes the curve start at one, before any noise is added. "
        "Line thirteen turns the curve into betas: one minus alpha bar at t plus one over alpha bar at t, the share of signal this one step removes. "
        "Line fourteen clamps beta at 0.999, then converts back to float 32. Without the clamp the final beta would be one, alpha would be zero, and the sampler would divide by zero. "
        "Remember this 0.999. It comes back in A3."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Code: alpha bar and the closed-form forward process",
    kind="code",
    src="A2NB",
    start="class Schedule:",
    n=21,
    hl=["torch.cumprod(self.alphas, dim=0)", '"cosine": Schedule("cosine", cosine_betas(T))', ".view(-1, 1, 1, 1)", "return abar.sqrt() * x0"],
    bullets=[
        "alphas = 1 − betas; alpha_bars = cumulative product",
        "ᾱ is recomputed from the clamped betas, so everything stays consistent",
        "q_sample: xt = √ᾱt · x0 + √(1 − ᾱt) · ε",
        ".view(-1, 1, 1, 1) lets one ᾱ per image broadcast over its pixels",
        "Each image in a batch can have its own t",
    ],
    narration=(
        "The Schedule class holds betas, alphas, and alpha bars, moved to the GPU once. "
        "Line 23 computes alpha as one minus beta. On line 24, alpha bars come from torch dot cumprod, the cumulative product: alpha zero, then alpha zero times alpha one, and so on. "
        "dim equals zero says multiply along the one and only axis, the time axis. "
        "Line 29 builds the cosine schedule from the clamped betas, so for cosine, alpha bar is recomputed from them, and all three always agree. "
        "Below is q sample, the forward process, written almost word for word from the closed form. "
        "It takes clean images, one timestep per image, and noise. "
        "On line 36 it looks up alpha bar for each image's own step. That gives one number per image, a shape of B. "
        "The view call reshapes it to B by 1 by 1 by 1, so one number multiplies all of that image's pixels. Without the view, PyTorch could not line up the shapes. "
        "Line 37 returns root alpha bar times x zero, plus root of one minus alpha bar, times epsilon. "
        "The alternative, adding noise in a loop of t small steps, gives the same distribution but is up to 1000 times slower. "
        "This one function serves the A1 grid and every training step in A2."
    ),
),

dict(
    section="Part A · A1",
    title="Saved output: first and last beta and alpha bar",
    kind="output",
    src="A2OUT",
    start="linear: beta[0]=",
    n=2,
    hl=["linear: beta[0]", "cosine: beta[0]"],
    bullets=[
        "[0] = first step, t = 0;  [-1] = last step, t = 999",
        "Linear: β0 = 1e-4, β999 = 0.02, ᾱ0 = 0.9999, ᾱ999 = 4.04e-05",
        "Cosine: β0 = 4.13e-05, β999 = 0.999 (the clamp), ᾱ999 = 2.43e-09",
        "Cosine ᾱ0 prints 1.0000 only from rounding: really 0.99996",
        "1/√ᾱ999: about 157 (linear), about 20,000 (cosine)",
    ],
    narration=(
        "The saved output of the schedule cell: one line per schedule, four fields each. "
        "Square bracket zero means the first step, and minus one means the last, step 999. "
        "Linear first. Beta zero is 1.00 e minus 04, so ten to the minus four, and the last beta is 0.0200. "
        "Those are exactly the two ends we asked linspace for, so the schedule is right. "
        "Alpha bar zero is 0.9999, which is one minus the first beta, as it must be, because the product so far has only one alpha in it. "
        "Alpha bar 999 is 4.04 e minus 05, about four in a hundred thousand. "
        "Now cosine. Its first beta, 4.13 e minus 05, is smaller than linear's, so cosine starts more gently. "
        "Its last beta is 0.9990. That is the clamp at work. "
        "Alpha bar zero prints as 1.0000, but only because the format keeps four decimals. "
        "The true value is 0.99996, as the next table shows, so do not say it is exactly one. "
        "And alpha bar 999 is 2.43 e minus 09, far smaller than linear's. "
        "One over its square root is about 20,000, against about 157 for linear. "
        "Those two numbers explain the noisy x hat zero panels we will meet in A3."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Code: the alpha bar plot and the crossing points",
    kind="code",
    src="A2NB",
    start="# Plot alpha_bar_t against t for both schedules on one figure.",
    n=24,
    hl=['plt.axhline(0.5', '"alpha_bar_at": {t: round(abar[t].item(), 5)', '"first_t_below_0.5": int((abar < 0.5).nonzero()[0])', '"first_t_below_0.01"'],
    bullets=[
        "One curve per schedule; dotted line at ᾱ = 0.5",
        "ᾱ at t = 0, 100, 250, 500, 750, 999, rounded to 5 decimals",
        "(abar < 0.5).nonzero()[0]: first step below one half",
        "ᾱ only decreases, so the first True is the crossing point",
        "Saved to results.json: the report reads, never retypes",
    ],
    narration=(
        "This cell makes the A1 plot and the numbers behind it. "
        "At the top, one line per schedule: plot alpha bar against t. "
        "The axhline call draws a dotted grey line at 0.5, where signal and noise variance are equal, so the eye can read where each curve crosses it. "
        "save fig writes the picture to the figures folder. "
        "A picture alone is imprecise, so the lower half measures. A1 T SHOW lists the six timesteps the handout asks for. "
        "For each schedule, alpha bar at those six steps is rounded to five decimals. "
        "Now the key line. abar less than 0.5 makes a true or false value for each of the 1000 steps. "
        "nonzero returns the positions that are true, and square bracket zero takes the first one. "
        "Because alpha bar only ever goes down, the first step below one half is the crossing point. "
        "The same trick finds the first step below 0.01, where the image is practically pure noise. "
        "The alternative, reading the crossing off the plot by eye, would be off by tens of steps. "
        "Everything goes into RESULTS, and save results writes results dot json, so the report reads these numbers instead of copying them by hand. "
        "The last line shows the table you will see next."
    ),
),

dict(
    section="Part A · A1",
    title="Saved output: alpha bar at the six timesteps",
    kind="output",
    src="A2OUT",
    start="saved A1_alpha_bar.png",
    n=5,
    hl=["linear  0.99990", "cosine  0.99996"],
    bullets=[
        "Columns: t = 0, 100, 250, 500, 750, 999",
        "t = 250: linear 0.521, cosine 0.846",
        "t = 500: linear 0.078, cosine 0.492",
        "t = 750: linear 0.0033, cosine 0.143",
        "results.json: below 0.5 at 259 vs 496; below 0.01 at 673 vs 935",
    ],
    narration=(
        "The saved output. First, saved A1 alpha bar dot png, and a note that the figure was shown in the notebook. Then the table. "
        "The columns are the six timesteps: 0, 100, 250, 500, 750 and 999. "
        "The rows are the two schedules, and each cell is alpha bar, the share of signal variance left. "
        "At step zero both are almost one: 0.9999 for linear and 0.99996 for cosine. "
        "At step 100, linear has 0.895 and cosine 0.972. "
        "At 250, linear is already down to 0.521, close to one half, while cosine still keeps 0.846. "
        "At 500 the gap is largest: linear 0.078, cosine 0.492. "
        "At 750, linear has only 0.0033, practically pure noise, while cosine keeps 0.143. "
        "And at 999, linear shows 0.00004, and cosine shows zeros, because its true value, 2.43 times ten to the minus nine, is too small for five decimals. "
        "The crossing points are not printed here. They were saved to results dot json: "
        "below one half at 259 for linear and 496 for cosine, and below 0.01 at 673 and 935. "
        "Read each column from top to bottom, and you see that linear always has less signal left."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Result: alpha bar for both schedules",
    kind="figure",
    image="A2F/A1_alpha_bar.png",
    bullets=[
        "ᾱ below 0.5: linear at t = 259, cosine at t = 496",
        "ᾱ below 0.01: linear at t = 673, cosine at t = 935",
        "At t = 500: linear 0.078, cosine 0.492",
        "Linear destroys the image much faster",
    ],
    narration=(
        "Both curves start just below one, an almost clean image, and fall to almost zero, pure noise. "
        "The dotted line is one half, where signal and noise are equally strong. "
        "The linear curve drops below one half already at step 259. The cosine curve only crosses at step 496, almost the middle. "
        "Near the bottom, linear is below 0.01 from step 673. Cosine only gets there at step 935. "
        "At step 500, linear has an alpha bar of 0.078, while cosine still has 0.492. "
        "So linear destroys the image much faster. "
        "These numbers, 259 against 496, and 673 against 935, are the backbone of your A1 answer. "
        "The code computed them and saved them to the results file."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Code: the two by six forward grid",
    kind="code",
    src="A2NB",
    start="# One training image at t = 0, 100, 250, 500, 750, 999",
    n=16,
    hl=["x0 = X_TRAIN[0:1].to(DEVICE)", "eps = torch.randn_like(x0)", "xt = q_sample(x0, torch.tensor([t], device=DEVICE), eps, s)", "set_title"],
    bullets=[
        "X_TRAIN[0:1]: a slice keeps the batch dimension (1, 1, 32, 32)",
        "ε drawn ONCE and reused in all 12 panels",
        "Same image + same noise: only the schedule differs",
        "q_sample jumps straight to each t: the closed form",
        "Titles print t and ᾱ to 3 decimals",
    ],
    narration=(
        "This cell draws the grid the handout asks for. On line three, set seed with 9005, so the same noise appears on every run. "
        "On line four, X TRAIN zero colon one takes the first training image. "
        "Using a slice, not just zero, keeps the batch dimension, so the shape is one by one by 32 by 32, which is what q sample expects. "
        "On line five, epsilon is drawn once, with randn like, and then reused for all twelve panels. That is the key design choice. "
        "Both rows see the same image and the same noise, so the only difference between them is the schedule. "
        "If we drew fresh noise for each panel, part of the difference could come from luck. "
        "Two loops follow: the outer one over the two schedules, the inner one over the six timesteps. "
        "On line ten, q sample jumps straight to step t with the closed form, exactly as the handout asks. "
        "The alternative, adding noise step by step, would need 1000 updates for the last panel, and give the same distribution. "
        "On line twelve, each panel's title prints t and alpha bar to three decimals, which is where the 0.078 and 0.492 at step 500 come from. "
        "Finally, to display maps pixels back from minus one to one into zero to one for drawing."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Result: one sandal destroyed by both schedules",
    kind="figure",
    image="A2F/A1_forward_grid.png",
    bullets=[
        "Same image, same noise ε in both rows: only the schedule differs",
        "t = 500: linear ᾱ ≈ 0.08, object barely visible; cosine ᾱ ≈ 0.49, still clear",
        "t is drawn uniformly in training",
        "Linear: about a third of steps (t ≥ 673) are near-pure noise",
        "Cosine spreads the destruction more evenly",
    ],
    narration=(
        "This is the two by six grid: linear on top, cosine below. "
        "Both rows use the same image and the same noise, so only the schedule differs. That makes the comparison fair. "
        "At step 500, the linear row has alpha bar about 0.08, and the object is barely visible. The cosine row has about 0.49, and it is still clear. "
        "Why does that matter? Training picks t uniformly from 0 to 999. "
        "Under linear, every step from 673 onwards is practically pure noise. That is about a third of all steps, with very little to learn. "
        "Cosine destroys the image more evenly, so more training time goes to partly noisy images, where real denoising is learned. "
        "That is your written A1 answer."
    ),
),

dict(
    section="Part A · A1",
    title="A1 · Viva check",
    kind="text",
    bullets=[
        "Q: Which schedule destroys faster? Linear: ᾱ < 0.5 at 259 vs 496",
        "Q: Why the square roots? Signal variance + noise variance = 1",
        "Q: Why clamp cosine beta at 0.999? β = 1 would make α = 0: divide by zero",
        "Q: Why s = 0.008? Keeps the first betas from being too tiny",
        "Q: What does cumprod return? The running product α0 · α1 · … · αt",
    ],
    narration=(
        "Viva check for A1. "
        "Which schedule destroys faster? Linear: alpha bar falls below one half at 259, against 496 for cosine. "
        "Why the square roots in the closed form? If the clean image has variance one, x t has variance alpha bar plus one minus alpha bar, "
        "which is one at every step. This is called variance preserving. "
        "Why clamp the cosine betas at 0.999? Otherwise the last beta is one, alpha is zero, and the reverse step divides by root alpha. "
        "Why s equals 0.008? It is the paper's small offset, so the first betas are not too tiny. "
        "And cumprod returns the running product of the alphas, so entry t is alpha bar t."
    ),
),

# =====================================================================  A2
dict(
    section="Part A · A2",
    title="A2 · What the handout asks",
    kind="handout",
    page=2,
    find=[
        "Use a small U-Net (suggested: block_out_channels=(32, 64, 128)).",
        "Implement the DDPM training step",
        "Train two models with identical settings",
        "Plot both training loss curves on one figure",
    ],
    bullets=[
        "Small U-Net (32, 64, 128), random weights, no from_pretrained",
        "Training step: sample x0, t, ε; build xt; predict ε; minimise ‖ε − εθ‖²",
        "Two models, identical settings: linear and cosine, about 15 minutes each",
        "Loss curves on one plot; save checkpoints",
        "Report training time, batch size, learning rate, epochs",
    ],
    narration=(
        "A2 asks for four things. "
        "One: a small U-Net with channels 32, 64 and 128, started from random weights. No pretrained weights. "
        "Two: your own training step. Sample a clean image, a timestep, and noise. Build x t. "
        "Ask the network to predict the noise, written epsilon theta. Minimise the squared difference to the true noise. "
        "Three: train two models with identical settings, one per schedule, about 15 minutes each. "
        "Identical settings mean any difference comes from the schedule alone. "
        "Four: plot both loss curves on one figure, save both checkpoints, and report training time, batch size, learning rate and epochs. "
        "The handout also says recognisable class shapes are enough."
    ),
),

dict(
    section="Part A · A2",
    title="Formula card: ε, εθ and the training loss",
    kind="text",
    bullets=[
        "L = ‖ ε − εθ(xt, t) ‖²   (mean squared error)",
        "ε (epsilon) = the true noise we added: we know it, because we drew it",
        "εθ (epsilon theta) = the U-Net's guess of that noise; θ = its weights",
        "εθ(xt, t): the guess sees the noisy image and the step number",
        "‖ · ‖² = squared difference, averaged over pixels: the MSE",
        "Random: x0, t, ε. Learned: only θ. Noise target = fixed scale, simplified ELBO",
    ],
    narration=(
        "A formula card for the training loss. "
        "Epsilon is the true noise we added. We know it exactly, because we drew it ourselves. "
        "Epsilon theta is the network's guess of that noise. The small theta means made by the network with weights theta. "
        "Epsilon theta of x t and t says the guess looks at two things: the noisy image, and the step number. "
        "The double bars squared mean the squared difference, averaged over all pixels. That is the mean squared error. "
        "So the loss asks: how far was the guess from the real noise? "
        "The network making the guess is the U-Net. It shrinks the image to see the big picture, then grows it back, so its output has the same size as the noise. "
        "Which symbols are random and which are learned? x zero, t and epsilon are all drawn at random. Only theta is learned. "
        "Why predict noise, not the clean image? Noise has the same simple scale at every step, which gives a stable target, "
        "and Ho and colleagues showed this loss is a simplified form of the proper likelihood bound, called the ELBO."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Code: building the small U-Net",
    kind="code",
    src="A2NB",
    start="def make_unet():",
    n=12,
    hl=["in_channels=1", "block_out_channels=(32, 64, 128)", "AttnDownBlock2D", "AttnUpBlock2D"],
    bullets=[
        "Built from a config, so random weights; no from_pretrained",
        "1 channel in, 1 channel out, 32 × 32",
        "Channels 32, 64, 128 at resolutions 32, 16, 8",
        "Self-attention only at 8 × 8, to keep training fast",
        "3,939,393 parameters",
    ],
    narration=(
        "We call the UNet2DModel constructor with a configuration, so every weight starts random. "
        "Sample size 32, one channel in and one out, because the images are grayscale. "
        "Two layers per block, and block out channels 32, 64, 128, as suggested. "
        "The first two down blocks are plain, at 32 by 32 and 16 by 16. The last is an attention block, at 8 by 8. The up blocks mirror that. "
        "So self-attention, where every position looks at every other, is used only at 8 by 8. "
        "That was deliberate. Attention is expensive with many positions, but 8 by 8 is only 64, so training stays fast. "
        "The alternative, attention at 32 by 32 as well, would compare 1024 positions with each other in every such layer, which costs far more for small images like ours. "
        "Notice there are only two halvings, 32 to 16 to 8. The third down block keeps 8 by 8. "
        "The timestep is not an argument here. It is passed in at every call, and the U-Net turns it into an embedding vector inside. "
        "The model has 3,939,393 parameters, about four million."
    ),
),

dict(
    section="Part A · A2",
    title="Saved output: U-Net size",
    kind="output",
    src="A2OUT",
    start="U-Net parameters: 3,939,393",
    n=1,
    hl=["U-Net parameters"],
    bullets=[
        "3,939,393 parameters, about 3.9 million",
        "Counted by summing numel() over every weight tensor",
        "float32 = 4 bytes each: about 15.8 MB; each checkpoint is 15.89 MB",
        "Compare: ViT-B/16 86.6 M, Swin-T 28.3 M",
    ],
    narration=(
        "The cell printed one line: U-Net parameters, 3,939,393. How was it counted? "
        "The line above the print builds a fresh U-Net, loops over all its weight tensors, and adds up numel, the number of elements in each. "
        "The comma inside the format braces adds thousands separators, so the number is easy to read out. "
        "So the model has about 3.9 million learnable numbers. "
        "Each is stored as a 32 bit float, four bytes, so the weights take about 15.8 megabytes. "
        "That matches the files list at the end of the notebook, where each checkpoint is 15.89 megabytes. "
        "The small extra is the saved training information, including the loss history. "
        "Is four million big? Not at all. The ViT in Part B has 86.6 million parameters and the Swin 28.3 million. "
        "A small network was the right choice here. The images are only 32 by 32 in grayscale, the budget was about 15 minutes per model, "
        "and the handout suggests a small U-Net. "
        "A wider network, for example with channels 64, 128 and 256, would do more work per step, so fewer epochs would fit into the same 15 minutes."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Code: settings and the five-line training step",
    kind="code",
    src="A2NB",
    start="BATCH_SIZE = 128",
    n=17,
    hl=["LR = 5e-4", "t = torch.randint(0, T, (x0.shape[0],)", "eps_pred = model(xt, t).sample", "loss = F.mse_loss(eps_pred, eps)"],
    bullets=[
        "Batch 128; learning rate 5 × 10⁻⁴; target about 15 minutes",
        "1) random t per image  2) random noise ε",
        "3) xt with the closed form  4) U-Net predicts ε",
        "5) MSE loss, then backward and an AdamW step",
        "LR above the usual 2 × 10⁻⁴ because training is short",
    ],
    narration=(
        "Batch size 128. Learning rate five times ten to the minus four, a bit above the common two times ten to the minus four, "
        "because we only train about 15 minutes, and slightly bigger steps learn faster in that time. "
        "Now the training step, which matches the handout one to one. "
        "One, on line ten, a random step for each image. randint with zero and T draws from 0 up to 999, because the upper end is excluded, "
        "and the shape, x0 dot shape zero, gives one timestep per image in the batch, not one for the whole batch. Two, random noise. "
        "Three, x t from q sample, the closed form. "
        "Four, on line thirteen, the U-Net's noise guess. diffusers returns an output object, and dot sample is the predicted tensor inside it. "
        "Five, on line fourteen, F dot mse loss: the squared difference between guess and true noise, averaged over every pixel of every image. "
        "Then zero the gradients, backpropagate, and take an optimiser step. "
        "Notice that no class label goes into the U-Net. The model is unconditional: it learns all three classes together, and which class a sample becomes is down to chance. "
        "We train in plain float 32, no mixed precision. It is simpler, and avoids the risk of the loss becoming not a number in half precision."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Code: choosing the number of epochs by timing",
    kind="code",
    src="A2NB",
    start="def choose_epochs(target_minutes, n_timing_steps=30):",
    n=19,
    hl=["for _ in range(5):", "torch.cuda.synchronize()", "steps_per_epoch = len(X_TRAIN) // BATCH_SIZE", "epochs = max(1, round("],
    bullets=[
        "Throwaway model; AdamW with LR 5e-4, other settings default",
        "5 warm-up steps, not timed: CUDA start-up cost",
        "synchronize(): wait until the GPU has really finished",
        "30 timed steps → seconds per step; 18,000 // 128 = 140 steps per epoch",
        "epochs = round(15 × 60 s ÷ time per epoch), at least 1",
    ],
    narration=(
        "The handout says about 15 minutes per model, so the number of epochs is measured, not guessed. "
        "choose epochs builds a throwaway model and optimiser through new training objects, which makes a fresh U-Net and torch AdamW with our learning rate, "
        "leaving the other settings at their defaults, including a weight decay of 0.01. It takes one batch of 128 images. "
        "On line 32, five warm-up steps run first and are not timed, because the first CUDA calls pay one-off start-up costs. "
        "On line 35, torch cuda synchronize waits until the GPU has really finished. "
        "GPU work is asynchronous: without the wait, the timer could stop while the GPU is still busy, and a step would look too fast. "
        "Then 30 steps are timed and divided by 30, to get seconds per step. "
        "On line 42, steps per epoch is 18,000 floor-divided by 128, which is 140. "
        "On line 43, the target, 15 minutes times 60 seconds, is divided by the time of one epoch and rounded. "
        "max of one and that number guarantees at least one epoch. "
        "Below this function, the EPOCHS line first looks for an existing checkpoint and reuses its epoch count, "
        "so both models always get the same number, even after a disconnect. In this run there was none yet, so the timing ran."
    ),
),

dict(
    section="Part A · A2",
    title="Saved output: 28 epochs",
    kind="output",
    src="A2OUT",
    start="232.8 ms/step",
    n=2,
    hl=["232.8 ms/step", "EPOCHS = 28"],
    bullets=[
        "232.8 ms per training step on a Tesla T4",
        "140 steps per epoch: about 32.6 s per epoch",
        "900 s ÷ 32.6 s ≈ 27.6, rounded to 28 epochs",
        "Both models: 28 × 140 = 3,920 steps",
        "Real runs: 16.3 and 16.7 minutes",
    ],
    narration=(
        "The saved output has two lines. The first says 232.8 milliseconds per step, 140 steps per epoch, so 28 epochs. "
        "Let us redo the arithmetic, because the examiner may ask. "
        "One epoch is 140 steps times 0.2328 seconds, about 32.6 seconds. Fifteen minutes is 900 seconds. "
        "900 divided by 32.6 is about 27.6, and rounding gives 28. "
        "The second line, EPOCHS equals 28, is the value both models then use. "
        "So each model takes 28 times 140, which is 3,920 optimiser steps, and sees each training image up to 28 times. "
        "Why not just pick a round number like 30 epochs? Because the speed depends on the GPU that Colab hands you. "
        "Timing on the actual machine keeps the run near the 15 minute budget, whatever the GPU is. "
        "This run had a Tesla T4, as the setup cell printed. "
        "The real training took a little longer than the estimate: 16.3 minutes for linear and 16.7 for cosine, as the next outputs show. "
        "The estimate only times the training steps on one fixed batch, so it is an estimate, not a promise."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Code: the training loop, identical for both models",
    kind="code",
    src="A2NB",
    start="# same seed -> same init and data order",
    n=16,
    hl=["set_seed(SEED)", "perm = torch.randperm(len(data), device=DEVICE)", "for i in range(0, len(data) - BATCH_SIZE + 1, BATCH_SIZE):", "assert np.isfinite(losses[-1])"],
    bullets=[
        "Same seed: same starting weights and same data order",
        "AdamW optimiser; whole dataset kept on the GPU",
        "Shuffle every epoch; drop the last partial batch",
        "18,000 // 128 = 140 steps per epoch; 28 epochs = 3,920 steps",
        "Epochs chosen once by timing 30 steps (choose_epochs)",
    ],
    narration=(
        "This loop runs twice, once per schedule. "
        "The same seed, 9005, from your roll number, gives both models the same starting weights and the same data order. "
        "Then a fresh model and an AdamW optimiser. The whole dataset fits on the GPU, so it moves there once. "
        "Line 19, model dot train, puts the network in training mode. "
        "Each epoch, on line 22, randperm makes a fresh random order of all 18,000 indices, made directly on the GPU. "
        "Line 23 walks through that order in batches of 128. The range stops at 18,000 minus 128 plus one, so a batch only starts if 128 images remain. "
        "That gives 140 full batches, and the last 80 images of each shuffle are skipped. Every batch has the same size, so every step is comparable. "
        "Line 26 is a safety check: if the last loss is not a finite number, the run stops at once instead of wasting fifteen minutes. "
        "Each epoch then prints the mean of its 140 losses. "
        "How many epochs? choose epochs picked 28, so both models ran 28 times 140, which is 3,920 steps."
    ),
),

dict(
    section="Part A · A2",
    title="Saved output: the linear training log",
    kind="output",
    src="A2OUT",
    start="[linear] epoch 3/28",
    n=27,
    hl=["epoch 3/28", "epoch 10/28", "epoch 28/28", "saved /content"],
    bullets=[
        "Each line: schedule, epoch k / 28, mean of its 140 step losses, minutes",
        "Epochs 1–2 (just above): 0.0986, then 0.0482, already half",
        "From epoch 3 (0.0405), a slow creep down to 0.0280 at epoch 28",
        "Small wobbles (epoch 10 > epoch 9): random t and ε",
        "Checkpoint saved to Drive after 16.3 min; cosine: 0.1425 → 0.0502, 16.7 min",
    ],
    narration=(
        "This is the saved log of the linear model's training, one line per epoch. Each line has four fields. "
        "In square brackets, the schedule name. Then epoch k of 28. "
        "Then mean loss: the average of the last 140 entries of the losses list, which are the steps of that epoch. "
        "And elapsed, the minutes since training started. "
        "The first two lines of the log sit just above this window, to make room for the end: "
        "epoch one ended at 0.0986, and epoch two already halved that, to 0.0482. "
        "This fast early drop is the network learning the basic job. "
        "From epoch three, at 0.0405, the loss creeps down slowly: 0.0333 at epoch ten, 0.0309 at epoch thirteen, and 0.0280 at epoch 28. "
        "Notice it does not fall every single epoch. Epoch ten is slightly above epoch nine, for example. "
        "That is normal, because every step draws random timesteps and random noise, so each epoch's average wobbles a little. "
        "Each epoch took a bit over half a minute, and the last line says the checkpoint was saved to Google Drive after 16.3 minutes. "
        "The cosine log, in the next cell, has the same format. It starts at 0.1425 and ends at 0.0502, after 16.7 minutes. "
        "The two loss levels are not comparable, as we will see in a moment."
    ),
),

dict(
    section="Part A · A2",
    title="Saved output: the training settings table",
    kind="output",
    src="A2OUT",
    start="saved A2_loss_curves.png",
    n=8,
    hl=["linear     28", "cosine     28", "final_loss_last_epoch"],
    bullets=[
        "Wide table wrapped by pandas: the backslash means 'continued below'",
        "Both: 28 epochs, batch 128, LR 0.0005, AdamW, 3,920 steps",
        "Time: linear 975.6 s, cosine 999.5 s",
        "Last-epoch loss: linear 0.028(0), cosine 0.0502: not comparable",
        "The code asserts the settings are identical before printing",
    ],
    narration=(
        "This table is the saved output of the cell that drew the loss curves. "
        "pandas wrapped it because it is wide. The backslash at the end of the first block means the table continues below, "
        "so final loss last epoch is just the last column. "
        "Read the linear row: 28 epochs, batch size 128, learning rate 0.0005, optimiser AdamW, 3,920 steps, and a training time of 975.6 seconds. "
        "The cosine row is identical except for the time, 999.5 seconds. "
        "This is not luck. Just before the table, the code loops over six keys, epochs, batch size, learning rate, optimiser, steps and number of training images, "
        "and asserts that they are equal for both runs. If any differed, the notebook would stop with an error. "
        "So identical settings, which the handout requires, is checked by code, not just claimed. "
        "The final column is the mean loss over the last epoch: 0.028 for linear, which is 0.0280 with the trailing zero dropped, and 0.0502 for cosine. "
        "Remember the trap. The same t is a different noise level under each schedule, so these two losses measure different tasks, "
        "and the lower linear loss does not mean better samples."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Result: loss curves and the settings table",
    kind="figure",
    image="A2F/A2_loss_curves.png",
    bullets=[
        "Both: 28 epochs, batch 128, LR 0.0005, AdamW, 3,920 steps, fp32",
        "Time on a T4: linear 16.3 min, cosine 16.7 min",
        "Last-epoch loss: linear 0.0280, cosine 0.0502",
        "Losses are NOT comparable across schedules",
        "Both checkpoints saved to the Drive folder",
    ],
    narration=(
        "Both loss curves, on a log scale. Faint lines are single steps; bold lines are a 100 step moving average. "
        "Both drop fast and then flatten, as healthy training should. "
        "Both used 28 epochs, batch 128, learning rate 0.0005, AdamW, 3,920 steps. "
        "Linear took 975.6 seconds, about 16.3 minutes. Cosine took 999.5 seconds, about 16.7 minutes. "
        "Last epoch loss: 0.028 for linear, 0.0502 for cosine. "
        "Here is a trap. Is linear better? No. The same t means a different noise level under each schedule. "
        "When the input is almost pure noise, x t is almost epsilon, so guessing it is easy. "
        "Linear has many more of those easy steps, so its loss is lower. That says nothing about sample quality."
    ),
),

dict(
    section="Part A · A2",
    title="A2 · Viva check",
    kind="text",
    bullets=[
        "Q: Explain the training step: t, ε, xt, εθ, MSE",
        "Q: Why is the cosine loss higher? Different noise levels; not comparable",
        "Q: Why LR 5 × 10⁻⁴? Short 15-minute budget",
        "Q: How were 28 epochs chosen? Timed 30 steps to fill about 15 min",
        "Q: Pretrained weights? No: built from a config, random init",
    ],
    narration=(
        "Viva check for A2. "
        "Explain the training step: random t, random noise, x t from the closed form, predict the noise, mean squared error. Say it calmly, line by line. "
        "Why is the cosine loss higher? The two are not comparable. For the same t the noise levels differ, "
        "and linear has more very noisy, easy steps. "
        "Why that learning rate? Five times ten to the minus four, above the usual, because training was only about 15 minutes. "
        "How were 28 epochs chosen? By timing 30 steps, and then both models used the same number. "
        "Pretrained weights? None. The U-Net was built from a configuration."
    ),
),

# =====================================================================  A3
dict(
    section="Part A · A3",
    title="A3 · What the handout asks",
    kind="handout",
    page=2,
    find=[
        "Implement DDPM sampling (all 1000 reverse steps) yourself",
        "Generate a 4 × 4 grid of samples",
        "show the denoising trajectory at 8 timesteps",
        "Compare the samples from the linear and cosine models.",
    ],
    bullets=[
        "Own sampler: all 1000 reverse steps, σt² = βt",
        "4 × 4 grid of samples per model, plus sampling time",
        "Trajectory: 8 timesteps from x999 to x0, with x̂0 under each",
        "Compare linear vs cosine; agree with A1?",
        "Why 1000 network calls to sample, but one per training step?",
    ],
    narration=(
        "A3 is the sampler. "
        "Write DDPM sampling yourself, all 1000 reverse steps, with the handout's formula, where the added noise has variance sigma squared equal to beta. "
        "Make a four by four grid of samples from each model, and report the sampling time. "
        "For one sample, show the trajectory at eight steps from x 999 to x zero, with the model's clean image guess, x hat zero, under each. "
        "Compare the two models. Which looks better for your classes, and does that agree with A1? "
        "And explain why sampling needs 1000 network evaluations, but one training step needs only one."
    ),
),

dict(
    section="Part A · A3",
    title="Formula card: one reverse step",
    kind="text",
    bullets=[
        "x(t−1) = (1/√αt) · ( xt − (βt / √(1 − ᾱt)) · εθ ) + σt · z",
        "xt = the current noisy image; x(t−1) = the slightly cleaner next one",
        "(βt / √(1 − ᾱt)) · εθ = the part of the guessed noise removed this step",
        "1/√αt = undoes the shrinking that the forward step did",
        "z = fresh Gaussian noise; σt = its size, with σt² = βt",
        "No z at the last step, so the final image is clean",
    ],
    narration=(
        "A formula card for the reverse step from the handout. "
        "x t is the current noisy image, and x t minus one is the slightly cleaner image we want next. "
        "Inside the bracket, we take x t and subtract a scaled part of the guessed noise, epsilon theta. "
        "The scale is beta t over the square root of one minus alpha bar t. So we only remove a small slice of the noise per step. "
        "Then one over root alpha t undoes the small shrinking that the forward step did. "
        "Finally we add fresh noise z, scaled by sigma t, where sigma t squared equals beta t. "
        "So which part removes noise? The bracket, rescaled, which gives the mean of the next step. Which part adds noise? sigma t times z. "
        "Why add noise at all? It keeps the sampler random, so it draws from the whole distribution instead of collapsing to one average image. "
        "At the very last step, no fresh noise is added."
    ),
),

dict(
    section="Part A · A3",
    title="Formula card: x̂0 and the clamp",
    kind="text",
    bullets=[
        "x̂0 = ( xt − √(1 − ᾱt) · εθ ) / √ᾱt,   then clamp to [−1, 1]",
        "The hat ^ means 'estimate': x̂0 (x hat zero) = the guess of the clean image",
        "It is the closed form solved backwards, with εθ in place of ε",
        "clamp(−1, 1): pixels below −1 become −1, above 1 become 1",
        "Then ε is recomputed to match: ε = ( xt − √ᾱt · x̂0 ) / √(1 − ᾱt)",
        "Near t = 999 √ᾱt is tiny: errors × ≈157 (linear), × ≈20,000 (cosine)",
    ],
    narration=(
        "One more card, for x hat zero. A hat on a symbol means estimate. "
        "So x hat zero is not the real clean image. It is the model's current guess of it. "
        "Where does the formula come from? Take the closed form, and solve it backwards for x zero, using the guessed noise instead of the real noise. "
        "So x hat zero equals x t minus root of one minus alpha bar t times epsilon theta, all divided by root alpha bar t. "
        "Clamp means: any pixel below minus one becomes minus one, and any pixel above one becomes one. "
        "A real image always lies in that range, so the clamp only removes impossible values. "
        "Then we recompute the noise that matches the clamped guess, by solving the closed form again, this time for epsilon. "
        "Why is x hat zero pure noise near step 999? Because we divide by root alpha bar, which is tiny there. "
        "One over root alpha bar 999 is about 157 for linear and about 20,000 for cosine, so any small error in the noise guess is blown up. "
        "That is exactly why clamping matters."
    ),
),

dict(
    section="Part A · A3",
    title="Diagram: one sampling step with clipping",
    kind="figure",
    image="DG/x0hat_clipping.png",
    bullets=[
        "εθ → x̂0 → clamp to [−1, 1] → recompute ε → x(t−1)",
        "Cosine β999 = 0.999, so 1/√α999 ≈ 31.6: errors multiplied about 32 times",
        "Unclipped cosine: x998 std about 1.6 (1.59) vs about 1 in training",
        "Unclipped cosine samples end 62.5% black; linear (1/√α ≈ 1.01) barely changes",
        "Same idea as clip_denoised in the original DDPM code",
    ],
    narration=(
        "This diagram shows one sampling step with clipping. "
        "On the left, the U-Net gives its noise guess, epsilon theta. "
        "Next, we turn it into x hat zero, the clean image guess. Then we clamp it to minus one to one. "
        "Then we recompute the matching noise, and on the right, the unchanged handout formula gives x t minus one. "
        "Why add this? The cosine schedule's last beta is 0.999, so alpha at step 999 is only 0.001, "
        "and one over its square root is about 31.6. "
        "So at the first reverse step, a small error in the noise guess is multiplied about 32 times. "
        "Without clipping, x 998 had a standard deviation of about 1.6, measured 1.59, while training always saw about one. "
        "The errors kept growing, and 62.5 percent of pixels ended black. "
        "Linear's last beta is 0.02, so its factor is about 1.01. The original DDPM code clips the same way."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Code: the 1000-step sampler",
    kind="code",
    src="A2NB",
    start="def ddpm_sample(model, sched, n, seed=SEED",
    n=21,
    hl=["gen = torch.Generator(device=DEVICE).manual_seed(seed)", "x0_hat = (x - (1 - abar).sqrt() * eps) / abar.sqrt()", "x0_hat = x0_hat.clamp(-1, 1)", "eps = (x - abar.sqrt() * x0_hat) / (1 - abar).sqrt()"],
    bullets=[
        "x999 drawn from N(0, I) with a fixed generator",
        "Loop t = 999, 998, …, 0: one U-Net call per step",
        "x̂0 computed, clamped to [−1, 1], matching ε recomputed",
        "Then the handout update formula, unchanged",
        "clip_x0=False runs the handout formula exactly",
    ],
    narration=(
        "Our sampler runs without gradients, because nothing is learned here. "
        "On line seven, a generator seeded with 9005 draws the starting noise on line eight, so results repeat exactly. "
        "The loop goes from 999 down to zero, one U-Net call per step, 1000 in total. "
        "Line eleven fills a tensor with the current t, one copy per image, because the U-Net expects one timestep per image. "
        "We read beta, alpha and alpha bar for the step, and on line fifteen compute x hat zero, the closed form solved for x zero. "
        "Here is the one unusual part. With clip x0 on, line seventeen clamps x hat zero to minus one to one, because a real image lies there. "
        "Then line eighteen turns the clamped image back into the matching noise, by solving the closed form for epsilon. "
        "That cleaned noise goes into the exact handout update, on the mean line. "
        "Fresh noise is then added, except at the last step. "
        "So the update formula is the same, but the noise fed into it has been cleaned. Be honest about this: "
        "every grid in the report uses this clipped sampler, and only the ablation cell runs the handout formula exactly, with clip x0 false."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Code: the update, the fresh noise and the last step",
    kind="code",
    src="A2NB",
    start="mean = (x - beta / (1 - abar).sqrt() * eps) / alpha.sqrt()",
    n=7,
    hl=["mean = (x - beta", "x = mean + beta.sqrt() * z", "# last step: no noise", "return x.clamp(-1, 1), trajectory"],
    bullets=[
        "mean = (1/√αt) · (xt − βt/√(1 − ᾱt) · ε): the handout formula",
        "t > 0: fresh z from the same seeded generator",
        "beta.sqrt() = σt, so σt² = βt as the handout asks",
        "t = 0: x = mean, no noise added",
        "Final clamp to [−1, 1], the legal pixel range",
    ],
    narration=(
        "The second half of the same loop. Line 22 is the handout's update, written as code. "
        "x minus beta over the square root of one minus alpha bar, times epsilon, all divided by the square root of alpha. "
        "Read it against the formula card: the bracket removes a slice of the predicted noise, and dividing by root alpha undoes the forward shrinking. "
        "The result is called mean, because it is the centre of the distribution for the next, slightly cleaner image. "
        "Line 23 checks t greater than zero. If so, line 24 draws fresh Gaussian noise z from the same seeded generator, so the whole run repeats exactly, "
        "and line 25 adds beta dot sqrt times z. The square root of beta is sigma t, so sigma squared equals beta, exactly as the handout says. "
        "The DDPM paper also allows a slightly smaller variance, called beta tilde. We used beta because the handout asks for it. "
        "Line 27 is the last step, t equal to zero. x is just the mean, with no noise added, because noise added at the very end would stay in the final image as grain. "
        "Finally, line 28 clamps the result to minus one to one, the legal pixel range, and returns it together with the recorded trajectory."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Code: timing the 4 × 4 grids",
    kind="code",
    src="A2NB",
    start="# 4 x 4 grid of samples from each model, and the sampling time.",
    n=17,
    hl=["torch.cuda.synchronize()", "start = time.time()", "ddpm_sample(MODELS[name], SCHEDULES[name], n=16)", '"network_evaluations": T'],
    bullets=[
        "synchronize before and after: time only finished GPU work",
        "n=16, default seed, default clip_x0=True",
        "16 images travel together: 1000 U-Net calls, not 16,000",
        "Seconds rounded to 2 decimals and stored in RESULTS['A3']",
        "Same seed for both models: same 16 starting noise images",
    ],
    narration=(
        "This cell makes the two grids and times them, as the handout asks. "
        "For each schedule, it first calls torch cuda synchronize, which waits for the GPU to be idle, and then starts the clock with time dot time. "
        "Line eight calls our sampler with n equal to 16, the default seed, and the default clip x0 true. "
        "The sixteen images travel through the loop together, as one batch. "
        "So each of the 1000 steps is one U-Net call on all sixteen images at once, which means 1000 network evaluations in total, not 16,000. "
        "After sampling, synchronize is called again before reading the clock. "
        "GPU work is queued and runs in the background, so without this second wait we could stop the timer before the last steps had finished, and report a time that is too short. "
        "The elapsed seconds, rounded to two decimals, and the number of network evaluations, T, are stored in RESULTS under A3. "
        "show grid then draws the sixteen images as a four by four grid and saves it. "
        "Both models use the same seed, so they start from exactly the same sixteen noise images. "
        "Any difference between the two grids therefore comes from the models and their schedules, not from different starting noise."
    ),
),

dict(
    section="Part A · A3",
    title="Saved output: sampling time",
    kind="output",
    src="A2OUT",
    start="saved A3_samples_linear.png",
    n=7,
    hl=["sampling_time_s_for_16", "15.95", "15.54"],
    bullets=[
        "16 samples: linear 15.95 s, cosine 15.54 s",
        "network_evaluations = 1000 for both (shown as 1000.0)",
        "About 16 ms per U-Net call on the batch",
        "Schedule barely matters: the cost is the 1000 U-Net calls",
        "Training: 1 call per step; sampling: 1000 sequential calls",
    ],
    narration=(
        "The saved output. First, the two grids were saved as png files. Then the timing table. "
        "Each row is a schedule, and there are two columns. "
        "Sampling time for 16 is the wall-clock seconds to generate all sixteen images: 15.95 seconds for linear and 15.54 seconds for cosine. "
        "Network evaluations is 1000 for both. It prints as 1000.0 only because pandas stored the whole table as decimal numbers. "
        "Let us read these numbers. Sixteen seconds for 1000 steps is about 16 milliseconds per U-Net call on the batch. "
        "The two schedules take almost the same time, because the schedule only changes a few numbers per step; nearly all the cost is the 1000 U-Net calls. "
        "Compare this with training. One training step needs exactly one U-Net call, because the closed form jumps straight to a random t. "
        "Sampling must walk all 1000 steps in order, since each step needs the previous output. "
        "That is the answer to the handout's last A3 question, backed by these numbers. "
        "The small difference between 15.95 and 15.54 seconds is too small to mean anything."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Code: the no-clipping ablation",
    kind="code",
    src="A2NB",
    start="NO_CLIP = {}",
    n=22,
    hl=["clip_x0=False", "diff = (NO_CLIP[name] - SAMPLES[name]).abs().mean().item()", "x998 = mean + cos.betas[-1].sqrt()", "saturated = (x_no_clip <= -0.99)"],
    bullets=[
        "Same models, same seed, clip_x0=False: the literal handout formula",
        "Mean |unclipped − clipped|: linear 0.0507, cosine 1.0557",
        "One reverse step by hand: 1/√α999 = 31.6",
        "std of x998 without clipping: about 1.6 (1.59)",
        "Pixels stuck at −1 (black): 62.5%",
    ],
    narration=(
        "We tested this with an ablation: switch one thing off and see what changes. "
        "We sample again with the same models and seed, but clip x0 false, the literal handout formula. "
        "Same seed means each unclipped image can be compared pixel by pixel with its clipped twin. "
        "For linear, the mean difference per pixel is 0.0507, on a pixel range of two. Tiny. "
        "For cosine it is 1.0557. Completely different images. "
        "The second half redoes one cosine step by hand, from x 999 to x 998. It prints 31.6 for one over root alpha, and a standard deviation of about 1.6 for x 998, measured 1.59. "
        "Then line 21 counts black pixels in the unclipped cosine samples, where black means a value at or below minus 0.99: 0.625, or 62.5 percent. "
        "If the examiner asks why you changed the algorithm, point here."
    ),
),

dict(
    section="Part A · A3",
    title="Saved output: what the ablation measured",
    kind="output",
    src="A2OUT",
    start="linear: mean |unclipped - clipped| per pixel = 0.0507",
    n=10,
    hl=["per pixel", "1/sqrt(alpha_999)", "std of x_999", "pixels stuck"],
    bullets=[
        "Mean pixel change without clipping: linear 0.0507, cosine 1.0557 (range 2)",
        "Cosine 1/√α999 = 31.6",
        "x999 std 0.99; unclipped x998 std 1.59 (training: about 1)",
        "62% of final pixels stuck at −1 (stored as 0.625)",
    ],
    narration=(
        "The saved output of the ablation, line by line. "
        "Line one: for linear, the mean absolute difference per pixel between the unclipped and clipped samples is 0.0507. "
        "Pixels run from minus one to one, a range of two, so that is a change of about two and a half percent. The images are nearly the same. "
        "Further down, the same measure for cosine is 1.0557, more than half of the whole range. The images are completely different. "
        "Next, one over the square root of alpha 999 is 31.6. That is the factor by which the first reverse step of the cosine model scales its input, "
        "because its last beta is 0.999. "
        "Next line. The starting noise x 999 has a standard deviation of 0.99, about one, as a standard Gaussian should. "
        "After a single unclipped step, x 998 has 1.59. In training, every x t had a standard deviation of about one, "
        "so the network is now fed an input unlike anything it has seen, and errors grow from there. "
        "The last line: 62 percent of the pixels in the final unclipped cosine samples are stuck at black. "
        "The format rounds to a whole percent. The stored value in results dot json is 0.625, which is the 62.5 percent quoted in the report."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Result: samples without clipping",
    kind="figure",
    image="A2F/A3_linear_no_clip.png",
    image2="A2F/A3_cosine_no_clip.png",
    bullets=[
        "Top: linear without clipping, still recognisable items",
        "Bottom: cosine without clipping, mostly black: 62.5% of pixels stuck at −1",
        "Cause: the extreme last step β999 = 0.999",
        "Fix: clamp x̂0 to [−1, 1], then use the matching ε",
    ],
    narration=(
        "Here is the ablation. "
        "Top: the linear model with the literal formula and no clipping. It still makes recognisable sandals, bags and trousers, almost the same as with clipping. "
        "Bottom: the cosine model with no clipping. It comes out mostly black: 62.5 percent of the pixels are stuck at minus one. "
        "This is not a training failure. The same cosine model makes proper images with clipping, as we see next. "
        "It is a sampling problem, caused by that one extreme last step. "
        "So the honest summary: all reported grids use the clipped sampler. It uses the handout update, but with a cleaned noise estimate. "
        "The literal formula is run only in this ablation, and both results are shown. "
        "Examiners usually respect a deviation that is explained, tested and shown openly."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Result: 16 samples from each model",
    kind="figure",
    image="A2F/A3_samples_linear.png",
    image2="A2F/A3_samples_cosine.png",
    bullets=[
        "Top: linear, a good mix: about 4–5 sandals, 7 bags, 3 trousers",
        "Bottom: cosine, mostly bright bag-like shapes, 2 sandals, 2 trousers",
        "Linear sandals show thin straps and high heels quite sharply",
        "Sampling 16 images: linear 15.95 s, cosine 15.54 s",
        "1000 U-Net evaluations per batch",
    ],
    narration=(
        "The real samples, with clipping. Linear on top, cosine below. "
        "Both make recognisable items from your three classes, which is what the handout asks. "
        "For your classes, linear looks better. It has a good mix: four or five sandals, about seven bags, three trousers. "
        "And the sandals' thin straps and high heels are quite sharp. "
        "The cosine grid is dominated by large, over-bright, bag-like shapes, with only two sandals and two trousers, "
        "and several flat white blobs. "
        "Sampling sixteen images took 15.95 seconds for linear and 15.54 for cosine, about 16 seconds each, "
        "with 1000 U-Net calls on the whole batch. "
        "Phrase it carefully: this is a visual judgement from sixteen samples, not a measurement."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Code: recording the denoising trajectory",
    kind="code",
    src="A2NB",
    start="TRAJ_T = [999, 900, 750, 600, 450, 300, 150, 0]",
    n=14,
    hl=["TRAJ_T = [999", "seed=SEED + 1, record_at=TRAJ_T", "xt, x0_hat = traj[t]"],
    bullets=[
        "8 recorded steps: 999, 900, 750, 600, 450, 300, 150, 0",
        "n=1, seed SEED + 1: a fresh sample, not one of the 16",
        "Sampler stores (xt, clamped x̂0) BEFORE each update",
        "Top row: xt; bottom row: x̂0",
        "Panel 'x0' = input to the last step, not the final sample",
    ],
    narration=(
        "This cell makes the trajectory plots. Line three lists the eight timesteps to record, from 999 down to zero, spread across the whole run. "
        "Line six calls the same sampler with n equal to one, a single image, and record at set to this list. "
        "Inside the sampler, whenever t is in the list, it stores two things: a copy of x, the current noisy image x t, "
        "and x hat zero, clamped to minus one to one for display. "
        "Note the seed: SEED plus one. That gives a different starting noise from the grids, so the trajectory is a fresh sample, not one of the sixteen we already showed. "
        "Using the same seed would also have been fine; this simply gives one more independent example. "
        "Then a two by eight grid is drawn. The top row shows x t, the bottom row x hat zero, with titles such as x 999, and x hat zero at t equals 999. "
        "One subtle point the examiner may test. The values are recorded before the update at each step. "
        "So the last top panel, labelled x zero, is x t at t equal to zero: the input to the final reverse step, not the final sample. "
        "The final step only removes about one percent of noise, so the two look the same."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Result: the denoising trajectories",
    kind="figure",
    image="A2F/A3_trajectory_linear.png",
    image2="A2F/A3_trajectory_cosine.png",
    bullets=[
        "Top row: xt at t = 999, 900, 750, 600, 450, 300, 150, 0",
        "Bottom row: x̂0, the model's guess of the final image",
        "Early x̂0 panels are noise: 1/√ᾱ999 ≈ 157 linear, ≈ 20,000 cosine",
        "Cosine x̂0 has an outline at t ≈ 900; linear only around t ≈ 750 to 600",
        "Linear: looks like a trouser at 600, then becomes a bag at 450",
    ],
    narration=(
        "The trajectories: linear first, cosine second. "
        "In each, the top row is the noisy image at eight steps, from 999 to zero. The bottom row is x hat zero, the guess of the finished image. "
        "Why are the first guesses noise? x hat zero divides by root alpha bar, which is tiny at the start. "
        "One over that is about 157 for linear and about 20,000 for cosine, so small errors become huge. Expected, not a bug. "
        "Now compare. The cosine guess already shows an outline at step 900. "
        "The linear guess is still noise at 900; a shape appears only around 750 to 600. "
        "In your run, linear even looks like a trouser at 600, then turns into a bag at 450. The model changed its mind."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Linear vs cosine, and does it agree with A1?",
    kind="text",
    bullets=[
        "Linear looked better for sandal, bag and trouser",
        "Agrees with A1 only partly",
        "Yes: cosine destroys slowly, and its x̂0 commits to a shape by t ≈ 900",
        "Hypothesis: an early big bright shape favours bags over thin sandal straps",
        "Straps are fine details, decided in the last low-noise steps",
        "16 samples and about 16 minutes: a visual judgement, not a measurement",
    ],
    narration=(
        "Does this agree with A1? Only partly. "
        "The trajectories confirm A1's picture: cosine destroys information slowly, so its model sees an outline already at step 900. "
        "But that did not give better samples for your classes. "
        "Our hypothesis, not a tested finding: the cosine model commits to a large bright shape very early, around step 900, "
        "when a big rectangle is the safest guess. And a big rectangle is a bag. "
        "Sandals are the opposite: thin straps, fine details decided in the last low-noise steps. "
        "Also, the cosine model only works with clipping. "
        "And be modest. Sixteen samples and about sixteen minutes of training give a visual judgement. Longer training could change the ranking."
    ),
),

dict(
    section="Part A · A3",
    title="A3 · Viva check",
    kind="text",
    bullets=[
        "Q: Why 1000 calls to sample but 1 to train? Training jumps to a random t",
        "Sampling is a chain: x(t−1) needs xt, which needs the previous output",
        "Q: You changed my formula? No: same formula, cleaned ε; ablation shown",
        "Q: Why are the first x̂0 panels noise? Divide by tiny √ᾱt",
        "Q: Sampling time? About 16 s for 16 images, both models",
    ],
    narration=(
        "Viva check for A3, starting with the classic. Why 1000 network calls to sample, but one per training step? "
        "In training, the closed form jumps straight to a random step, and the loss at that one step is an unbiased piece of the full objective. "
        "So training needs one U-Net call per image. "
        "In sampling we start from noise and do not know x zero, and the reverse has no closed form. "
        "Each step needs x t, which came from the previous network output. So the 1000 steps are a chain, and cannot run in parallel. "
        "If told you changed the formula: yes, the reported grids use a clipped sampler. The update is the same, the noise estimate is cleaned first, and the literal formula is in the ablation cell. "
        "Sampling took about 16 seconds for sixteen images."
    ),
),

# =====================================================================  PART B
dict(
    section="Part B",
    title="Part B · Your own dataset",
    kind="handout",
    page=2,
    find=[
        "photograph 4 classes of everyday objects around you",
        "25 photos per class, 100 photos in total,",
        "These photos must be your own;",
    ],
    bullets=[
        "4 classes of everyday objects, 25 photos each, 100 total",
        "Vary background, angle and lighting; include a collage",
        "Our classes: glasses_case, perfume, shoe, switch_board",
        "92 real phone photos + 8 augmented copies, used only in training",
        "Photos must be your own: have the originals ready on your phone",
    ],
    narration=(
        "Part B uses your own photos. Four classes of everyday objects, 25 photos each, 100 in total, taken with your phone, "
        "with varied backgrounds, angles and lighting, and a collage in the report. "
        "And the photos must be your own; the viva will check. "
        "Your classes are glasses case, perfume, shoe and switch board. "
        "Say this plainly if asked: 92 are real phone photos. Two blurry shots were removed, "
        "and the short classes were topped up to 25 with 8 augmented copies, real photos flipped, slightly rotated, cropped, and brightened. "
        "Their file names end in underscore aug, and the report says so. They only go into training, never the test set. "
        "Have the originals open on your phone."
    ),
),

dict(
    section="Part B",
    title="Part B · Code: reading the photo folders",
    kind="code",
    src="A2NB",
    start="PHOTO_EXTS = {",
    n=19,
    hl=["PHOTO_CLASSES = sorted(", "LABELS += [label] * len(files)", "assert all((LABELS == i).sum() == 25", 'ImageOps.exif_transpose(Image.open(path)).convert("RGB")'],
    bullets=[
        "One folder per class; folder name = class name",
        "sorted(): labels fixed alphabetically, 0 glasses_case … 3 switch_board",
        ".heic accepted: iPhone photos, opened via pillow-heif",
        "asserts: exactly 4 classes, 25 photos each",
        "Saved output: 4 classes, 25 photos per class",
    ],
    narration=(
        "This cell reads your photos from Google Drive. Line three lists the accepted file types. "
        "It includes dot heic, the format iPhones use, which PIL can open thanks to the pillow heif package installed at the top. "
        "Line four lists the folders inside photos and sorts them. Each folder is one class, and its name is the label. "
        "Sorting makes the order alphabetical, so the labels are fixed: 0 glasses case, 1 perfume, 2 shoe, and 3 switch board. "
        "Without sorting, the order of folders could differ between machines. "
        "The loop then lists the files of each class, also sorted, adds them to PATHS, and on line nine adds the class number once per file to LABELS. "
        "Two asserts follow: exactly four class folders, and, for the real run, exactly 25 photos in each. "
        "If a photo were missing, the notebook would stop right here instead of quietly running on 99 photos. "
        "The saved output confirms it: the four class names, and 25 photos for each. "
        "At the bottom, load photo opens a file, applies exif transpose so phone photos stand upright, and converts to RGB, three colour channels. "
        "That also removes any transparency channel a PNG might carry, so every model always sees exactly three channels."
    ),
),

dict(
    section="Part B",
    title="Part B · Models and preprocessing rules",
    kind="handout",
    page=2,
    find=[
        "pretrained vit_base_patch16_224 and swin_tiny_patch4_window7_224 from timm",
        "do not resize by hand.",
        "ImageOps.exif_transpose(Image.open(path)).convert('RGB') so phone photos are not",
    ],
    bullets=[
        "Pretrained ViT-B/16 and Swin-T from timm; no fine-tuning",
        "No resizing by hand: each model's own timm transform",
        "Transform: resize shorter side, centre-crop 224 × 224, normalise",
        "exif_transpose so phone photos are not rotated sideways",
    ],
    narration=(
        "The handout names the models: vit base patch 16 224, and swin tiny patch 4 window 7 224, pretrained, from timm. "
        "The names tell you the patch sizes, 16 and 4, Swin's window size, 7, and the input size, 224. "
        "No fine tuning; we only look inside. "
        "Do not resize by hand. Use each model's own timm transform, which resizes the shorter side, crops the centre 224 square, and normalises. "
        "And open every photo with exif transpose. A phone often saves a photo sideways, with a small note in the file, called EXIF, "
        "saying which way is up. exif transpose reads the note and rotates the photo upright."
    ),
),

dict(
    section="Part B",
    title="Part B · Code: loading the models and their own transforms",
    kind="code",
    src="A2NB",
    start='vit = timm.create_model("vit_base_patch16_224", pretrained=True)',
    n=9,
    hl=['vit = timm.create_model("vit_base_patch16_224", pretrained=True)', "resolve_model_data_config(model)", "is_training=False", 'pretrained_cfg.get("tag")'],
    bullets=[
        "timm.create_model(..., pretrained=True), then .eval()",
        "resolve_model_data_config reads each model's own settings",
        "create_transform(is_training=False): no random augmentation",
        "ViT weights use mean = std = 0.5; Swin uses ImageNet statistics",
        "So each model must get its own transform",
    ],
    narration=(
        "We load both pretrained models from timm, move them to the GPU, and set eval mode, "
        "which turns off training behaviour like dropout, so features are repeatable. "
        "For each model, resolve model data config reads its own input size, crop, and the mean and standard deviation it was trained with. "
        "create transform builds the matching pipeline, with is training false, so no random augmentation. "
        "The printout shows the two models normalise differently. timm's default ViT weights use mean and standard deviation 0.5, "
        "while Swin uses the ImageNet statistics. "
        "The handout's wording mentions ImageNet statistics, but its instruction is to use each model's own timm config, and that is what we did. "
        "A model should get exactly the normalisation it was trained with; one shared transform would feed one model colours it never saw. "
        "The print line shows each model's weights tag, read from pretrained cfg, next to its transform, so the saved output documents exactly what was used."
    ),
),

dict(
    section="Part B",
    title="Saved output: each model's own transform",
    kind="output",
    src="A2OUT",
    start="vit | weights: augreg2_in21k_ft_in1k",
    n=12,
    hl=["| weights:", "Resize(size=248", "Normalize(mean"],
    bullets=[
        "ViT weights: augreg2_in21k_ft_in1k (ImageNet-21k, then ImageNet-1k)",
        "Swin weights: ms_in1k (ImageNet-1k)",
        "Both: shorter side → 248 (bicubic), centre-crop 224 × 224",
        "ViT: mean = std = 0.5, so [0, 1] becomes [−1, 1]",
        "Swin: ImageNet mean (0.485, 0.456, 0.406), std (0.229, 0.224, 0.225)",
    ],
    narration=(
        "The saved output of the loading cell. Above these lines the raw output also has download progress bars, "
        "and a warning that we are not logged in to the Hugging Face hub. That only affects download speed and can be ignored. "
        "For each model we see its weights tag and its transform. "
        "ViT's tag is augreg2 in21k ft in1k: trained on ImageNet 21k, then fine tuned on ImageNet 1k. Swin's tag is ms in1k, trained on ImageNet 1k. "
        "Now the transform, step by step. Resize, size 248, bicubic: the shorter side of the photo becomes 248 pixels, and the other side keeps the photo's proportions. "
        "CenterCrop then cuts the central 224 by 224 square, so about ten percent of the shorter side is trimmed. "
        "MaybeToTensor turns the image into a tensor with values from zero to one. "
        "Then Normalize subtracts a mean and divides by a standard deviation, per colour channel. "
        "Here is the important difference. ViT uses mean 0.5 and standard deviation 0.5, which maps zero to one onto minus one to one. "
        "Swin uses the ImageNet statistics: mean 0.485, 0.456 and 0.406, and standard deviation 0.229, 0.224 and 0.225. "
        "So one shared transform would be wrong for one of the two models."
    ),
),

dict(
    section="Part B",
    title="Part B · Result: the dataset collage",
    kind="figure",
    image="A2F/B_dataset_collage.png",
    bullets=[
        "glasses_case, perfume, shoe, switch_board: 25 each",
        "Different objects, backgrounds, angles, lighting",
        "8 augmented copies marked _aug; file_map.csv links to originals",
        "Thumbnails here are only for the picture; models use timm transforms",
    ],
    narration=(
        "The collage: one panel per class, 25 photos each. "
        "You can see the variety the handout asked for: different objects, backgrounds, angles and lighting. "
        "These thumbnails are only for the picture. The models get the full photos through the timm transforms. "
        "In the Drive folder, photos sit in one folder per class, and file map dot csv maps every file to its original phone photo, "
        "including the eight augmented ones. "
        "If asked whether these are your photos, hold up your phone. "
        "If asked whether you have 100 real photos, say no: 92 real, and 8 augmented copies used only in training. "
        "A plain answer is safer than a vague one."
    ),
),

# =====================================================================  B1
dict(
    section="Part B · B1",
    title="B1 · What the handout asks",
    kind="handout",
    page=3,
    find=[
        "Use forward hooks to print the output shape",
        "(Swin) or every 3rd block (ViT) for one 224",
        "Report the parameter count of each model.",
        "explain why Swin's feature",
    ],
    bullets=[
        "Forward hooks: shape after patch embedding, every Swin stage, every 3rd ViT block",
        "Table: tokens, channel width, where downsampling happens",
        "Parameter count of each model",
        "2–3 sentences: why Swin can feed an FPN detector and ViT cannot",
    ],
    narration=(
        "B1 traces shapes. "
        "Use forward hooks to print the output shape after the patch embedding, then after every Swin stage, or every third ViT block, for one 224 image. "
        "Make a table of tokens, channel width, and where downsampling happens. Downsampling means the grid gets smaller. "
        "Report each model's parameter count. "
        "And explain in two or three sentences why Swin's feature maps can feed an FPN detector directly, and ViT's cannot. "
        "An FPN, or feature pyramid network, takes feature maps at several sizes, so a detector can find small and large objects. "
        "A hint above says features only equals true returns Swin's four stage outputs directly."
    ),
),

dict(
    section="Part B · B1",
    title="Diagram: how ViT turns an image into tokens",
    kind="figure",
    image="DG/vit_tokens.png",
    bullets=[
        "224 × 224 image cut into 16 × 16 patches: 14 × 14 = 196",
        "Each patch → one token of 768 numbers",
        "[CLS] token added in front: 197 × 768",
        "12 blocks, every token attends to every token; shape never changes",
    ],
    narration=(
        "Now the two models, starting with ViT, the Vision Transformer. A transformer reads a sequence of tokens, like words. "
        "On the left of the diagram you see the 224 by 224 image. "
        "Next, it is cut into small squares of 16 by 16 pixels. 224 over 16 is 14, so there are 14 by 14, which is 196 patches. "
        "Each patch becomes a token, a vector of 768 numbers. "
        "In front of them, one extra token is added, called CLS, short for classification. Its job is to collect a summary of the whole image. "
        "So we have 197 tokens of 768 numbers, and position embeddings tell the model where each patch came from. "
        "On the right, they go through twelve transformer blocks, where every token can look at every other token. "
        "The shape stays 197 by 768 all the way. ViT works at one single scale."
    ),
),

dict(
    section="Part B · B1",
    title="Formula card: ViT patches and tokens",
    kind="text",
    bullets=[
        "N = (224 / 16)² = 14² = 196 patch tokens;  + [CLS] = 197",
        "224 = input size; 16 = patch size P (the 'patch16' in the name)",
        "Each patch: 16 × 16 pixels × 3 colours = 768 values",
        "768 = D, the token width of ViT-Base, kept in every block",
        "[CLS] = an extra learned token that gathers a summary of the image",
        "Stride 16 everywhere: one token per 16 × 16 pixels",
    ],
    narration=(
        "A formula card for ViT. N, the number of patch tokens, is the image size over the patch size, squared. "
        "224 over 16 is 14, and 14 squared is 196. Add the CLS token, and you get 197. "
        "The 16 is the patch size, which is where patch 16 in the model name comes from. "
        "Each patch holds 16 by 16 pixels with 3 colours, which is 768 values. "
        "ViT base maps each patch to a token of width D equals 768, and keeps that width in every block. "
        "The CLS token is learned during pre-training. It starts the same for every image, and through attention it collects a summary. "
        "That is why, in B2, we use the CLS token as the photo's feature. "
        "Stride 16 means one token stands for a 16 by 16 square of pixels."
    ),
),

dict(
    section="Part B · B1",
    title="Diagram: Swin's four stages",
    kind="figure",
    image="DG/swin_stages.png",
    bullets=[
        "Patch partition: 4 × 4 patches → 56 × 56 tokens, 96 channels",
        "Attention only inside 7 × 7 windows; shifted windows link neighbours",
        "Patch merging: grid ÷ 2, channels × 2",
        "Stages 56 → 28 → 14 → 7; channels 96 → 192 → 384 → 768",
        "A pyramid at strides 4, 8, 16, 32, like a CNN",
    ],
    narration=(
        "Now Swin, the shifted window transformer. "
        "On the left, patch partition cuts the image into small 4 by 4 patches, so a 224 image gives 56 by 56 tokens, each 96 numbers wide. "
        "Inside each stage, attention only happens inside 7 by 7 windows, drawn as boxes on the grid. "
        "So the cost grows in a straight line with image size, not with its square. "
        "Every second block shifts the windows by three tokens, about half a window, so information can cross window borders. "
        "In timm's Swin tiny, stage 4 is a single 7 by 7 window, so there is no shift there. "
        "At the start of stages 2, 3 and 4 you see patch merging: each 2 by 2 group of neighbours is concatenated, normalised and projected, so the grid halves and the channels double. It is not pooling. "
        "Moving right, the grid goes 56, 28, 14, 7, and the channels go 96, 192, 384, 768. "
        "So Swin gives a pyramid of feature maps, just like a convolutional network."
    ),
),

dict(
    section="Part B · B1",
    title="Formula card: Swin sizes and windows",
    kind="text",
    bullets=[
        "side = H / 4;   windows = (side / M)²;   M = 7",
        "H = image size (224 here); 4 = patch size, so 224 / 4 = 56",
        "C = channels after embedding: 96 for Swin-T (128 in Part C)",
        "M = window size: attention inside each 7 × 7 = 49-token window",
        "Patch merging: concat 2 × 2 neighbours (4C), project to 2C: side ÷ 2",
        "Swin-T at 224: 64, 16, 4, 1 windows in the four stages",
    ],
    narration=(
        "A formula card for Swin. The side of the token grid is the image size H over the patch size 4. For 224, that is 56. "
        "C is the number of channels per token after the embedding. For Swin tiny it is 96. In Part C, your C is 128. "
        "M is the window size, 7, so each window holds 7 times 7, which is 49 tokens. "
        "The number of windows is the side over M, squared. At 224: 56 over 7 is 8, so 64 windows in stage one. "
        "Then 16, then 4, then 1. "
        "Patch merging, at the start of each new stage, concatenates each 2 by 2 group of neighbours into four C channels, "
        "then a linear layer projects that to two C. So the side halves and the channels double. "
        "Keep this card in mind, because Part C uses exactly these rules with a bigger image."
    ),
),

dict(
    section="Part B · B1",
    title="B1 · Code: recording shapes with forward hooks",
    kind="code",
    src="A2NB",
    start="def trace_shapes(model, module_names, image):",
    n=13,
    hl=["def hook(module, inputs, output, name=name):", "shapes[name] = tuple(output.shape)", "register_forward_hook(hook)", "h.remove()"],
    bullets=[
        "A hook = a small function PyTorch calls right after a module's forward",
        "It records output.shape without changing the model",
        "name=name freezes the loop variable inside each hook",
        "One image, no_grad; hooks removed afterwards",
        "ViT: patch_embed, pos_drop, blocks.2/5/8/11; Swin: patch_embed, layers.0–3",
    ],
    narration=(
        "A forward hook is a small function attached to a layer. PyTorch calls it right after the layer runs, with the output. "
        "We only write down the shape, so the model is unchanged. "
        "The code attaches one hook per module name we ask for. "
        "name equals name is a Python detail: it freezes the current name inside each hook. "
        "Then one image goes through, without gradients, and the hooks are removed. "
        "For ViT we hooked the patch embedding, pos drop, and blocks 2, 5, 8 and 11. Counting from zero, those are blocks 3, 6, 9 and 12. "
        "pos drop runs right after the CLS token and position embeddings are added, so it shows 196 becoming 197. "
        "For Swin: the patch embedding and the four stages, layers 0 to 3. "
        "Removing the hooks matters: otherwise every later forward pass, in B2 for example, would keep calling them."
    ),
),

dict(
    section="Part B · B1",
    title="B1 · Code: turning shapes into the table",
    kind="code",
    src="A2NB",
    start="def shape_table(shapes, input_size=224):",
    n=22,
    hl=["if len(shp) == 4:", "side = int(math.isqrt(n))", '" + 1 [CLS]" if n == side * side + 1 else ""', '"downsampling here?"'],
    bullets=[
        "4 numbers = Swin (B, H, W, C): tokens = H × W",
        "3 numbers = ViT (B, N, C): side = isqrt(N), 196 → 14",
        "N = side² + 1 means one extra [CLS] token: 197",
        "stride = 224 ÷ side; downsampling = side smaller than previous row",
        "Computed from the model, never typed",
    ],
    narration=(
        "This helper turns raw shapes into the table the handout asks for: tokens, channel width and where downsampling happens. "
        "It must handle two layouts. On line 20, a shape with four numbers is Swin's layout: batch, height, width, channels. "
        "Then the token count is height times width, and the side of the grid is the height. "
        "Otherwise the shape has three numbers, ViT's layout: batch, number of tokens, channels. "
        "ViT does not store a grid, so line 25 recovers it with the integer square root of the token count. For 196 that is 14. "
        "For 197 it is still 14, because 14 squared is 196. "
        "Line 26 then checks whether the count is one more than a perfect square. "
        "If so, the extra token is the CLS token, and the grid column says 14 by 14 plus 1 CLS. "
        "Stride versus input is 224 divided by the side, so how many pixels one token covers along each side. "
        "The last column compares the side with the previous row. If it got smaller, the table says yes, divided by the ratio; otherwise, no. "
        "The next two cells add a short note naming the layer that downsamples, and print the ViT and Swin tables. "
        "All of this is computed from the model, not typed, so the table cannot disagree with it."
    ),
),

dict(
    section="Part B · B1",
    title="Saved output: what the hooks recorded",
    kind="output",
    src="A2OUT",
    start="input to both models: (1, 3, 224, 224)",
    n=12,
    hl=["vit.patch_embed", "vit.pos_drop", "swin.patch_embed", "swin.layers.3"],
    bullets=[
        "Input: (1, 3, 224, 224) for both models",
        "ViT: patch_embed 196 tokens; pos_drop onwards 197 × 768",
        "ViT blocks.2/5/8/11 (= blocks 3, 6, 9, 12): shape never changes",
        "Swin (B, H, W, C): 56²×96 → 28²×192 → 14²×384 → 7²×768",
    ],
    narration=(
        "The raw output of the hooks, before it becomes a table. "
        "The first line confirms the input to both models: one image, three colour channels, 224 by 224, after each model's own transform. "
        "Then ViT. After patch embed: 1 by 196 by 768. One image, 196 tokens, 768 numbers each. "
        "The patch embedding is a 16 by 16 convolution with stride 16, so 224 over 16 is 14, and 14 squared is 196. "
        "After pos drop: 197. pos drop is the dropout layer that runs right after the CLS token is put in front and the position embeddings are added, "
        "so it is the first place we can see 197. We hooked it for exactly that reason. "
        "Then blocks 2, 5, 8 and 11, counted from zero, so the 3rd, 6th, 9th and 12th blocks: all 1 by 197 by 768. No block changes the shape. "
        "Swin prints four numbers, because its layout is batch, height, width, channels. "
        "After patch embed, 56 by 56 by 96. layers 0, stage one, keeps that. "
        "layers 1 is 28 by 28 by 192, layers 2 is 14 by 14 by 384, and layers 3, the last stage, is 7 by 7 by 768. "
        "Each later stage halves the grid and doubles the channels."
    ),
),

dict(
    section="Part B · B1",
    title="B1 · Code: where Swin downsamples, and features_only",
    kind="code",
    src="A2NB",
    start="for i, layer in enumerate(swin.layers):",
    n=12,
    hl=["type(layer.downsample).__name__", "features_only=True", "swin_backbone.feature_info.get_dicts()"],
    bullets=[
        "Print each stage's downsample module: PatchMerging or Identity",
        "timm: merging at the START of stages 2, 3, 4",
        "features_only=True: no head, returns all 4 stage outputs",
        "feature_info: module name, stride ('reduction'), channels",
        "Outputs are NHWC; an FPN would permute them to NCHW",
    ],
    narration=(
        "Two checks in one cell. First, where exactly does Swin downsample? "
        "We loop over the four stages in swin dot layers, and print the class name of each stage's downsample module, and the number of blocks. "
        "If it prints PatchMerging, merging happens in that stage. If it prints Identity, the module does nothing. "
        "This settles a detail that differs between implementations. In timm, merging sits at the start of stages 2, 3 and 4, "
        "while the official Microsoft code puts it at the end of a stage. Same pyramid, different bookkeeping. "
        "Second, the handout's hint. We create the same Swin model again with features only equal to true. "
        "timm then drops the classification head and returns the output of every stage, which is exactly what a detection backbone hands to an FPN. "
        "We run the same photo through it, without gradients. "
        "feature info dot get dicts tells us, for each output, the module name, the reduction, meaning the stride relative to the input, and the number of channels. "
        "We print the actual shape next to those. "
        "The comment notes the outputs are in NHWC order, channels last; a typical FPN expects channels first, so it would permute them."
    ),
),

dict(
    section="Part B · B1",
    title="Saved output: the Swin pyramid",
    kind="output",
    src="A2OUT",
    start="layers[0].downsample = Identity",
    n=9,
    hl=["= Identity", "= PatchMerging", "stride"],
    bullets=[
        "Stage 1: Identity (no merging); stages 2–4: PatchMerging",
        "Depths 2, 2, 6, 2 blocks (pairs: W-MSA then SW-MSA)",
        "Strides 4, 8, 16, 32; channels 96, 192, 384, 768",
        "The pyramid an FPN needs, like ResNet C2–C5",
    ],
    narration=(
        "The saved output. First, the four stages. layers 0 has downsample equal to Identity, so stage one does not merge. "
        "It keeps the 56 by 56 grid from the patch embedding. "
        "layers 1, 2 and 3 each have PatchMerging, so each of those stages begins by merging two by two neighbours. "
        "The depths are 2, 2, 6 and 2 blocks, the Swin tiny configuration. Blocks come in pairs: a window attention block, then a shifted window block. "
        "Next, the features only outputs, one line per stage. "
        "layers 0: shape 1 by 56 by 56 by 96, stride 4, 96 channels. layers 1: 28 by 28 by 192, stride 8. "
        "layers 2: 14 by 14 by 384, stride 16. layers 3: 7 by 7 by 768, stride 32. "
        "Stride means how many input pixels one position covers along a side: 224 divided by 56 is 4, and 224 divided by 7 is 32. "
        "This is the pyramid an FPN needs, with the same strides as a ResNet's stages C2 to C5. "
        "Fine maps at stride 4 help find small objects, and coarse maps at stride 32 help with large ones. "
        "ViT has nothing like this. All its blocks stay at stride 16."
    ),
),

dict(
    section="Part B · B1",
    title="Saved output: parameter counts",
    kind="output",
    src="A2OUT",
    start="ViT-B/16 parameters: 86,567,656",
    n=3,
    hl=["ViT-B/16 parameters", "Swin-T   parameters", "backbone only"],
    bullets=[
        "count_params = sum of numel() over all weight tensors",
        "ViT-B/16: 86,567,656 (86.6 M); Swin-T: 28,288,354 (28.3 M)",
        "ViT is about 3× larger",
        "Swin backbone only: 27,517,818; the gap is mostly the 1000-class head",
    ],
    narration=(
        "The parameter counts the handout asks for. "
        "The code is a tiny helper, count params, which sums numel, the number of elements, over every weight tensor of a model. "
        "It is the same method we used for the U-Net. "
        "ViT B 16 has 86,567,656 parameters, about 86.6 million. Swin T has 28,288,354, about 28.3 million. "
        "So ViT is roughly three times larger. "
        "Both counts include the 1000 class ImageNet classification head, because we loaded the full classification models. "
        "The third line is the features only Swin backbone: 27,517,818. "
        "The difference to the full model, about 770 thousand, is mostly that classification head, "
        "768 inputs times 1000 classes plus 1000 biases, which the backbone version drops. "
        "Why does the size gap matter for the viva? A bigger model is not automatically better, "
        "and here the bigger ViT also had its weights pre-trained on far more data. "
        "Keep that in mind in B2, when both probes get every test photo right. "
        "These numbers are also saved in results dot json, under B1, so the report reads them from there."
    ),
),

dict(
    section="Part B · B1",
    title="B1 · Result: what the hooks printed",
    kind="text",
    bullets=[
        "ViT patch_embed (1, 196, 768): 224/16 = 14, 14 × 14 = 196, downsample ÷16",
        "ViT pos_drop and blocks 3, 6, 9, 12: (1, 197, 768), no downsampling",
        "Swin patch_embed (1, 56, 56, 96): 3,136 tokens, ÷4",
        "Swin stages: 56²×96 → 28²×192 → 14²×384 → 7²×768 (strides 4, 8, 16, 32)",
        "Patch Merging at the start of stages 2, 3, 4 in timm",
        "Params: ViT-B/16 86,567,656 (86.6 M); Swin-T 28,288,354 (28.3 M)",
    ],
    narration=(
        "What the hooks printed. ViT after the patch embedding: one image, 196 tokens, 768 wide. "
        "That is ViT's only downsampling, by 16. "
        "After pos drop and every hooked block: 197 by 768. The extra one is the CLS token. No block changes the shape. "
        "Swin's layout is batch, height, width, channels. After the patch embedding: 56 by 56 by 96, so 3,136 tokens, downsampled by 4. "
        "Stage one keeps that. Stage two, 28 by 28 by 192. Stage three, 14 by 14 by 384. Stage four, 7 by 7 by 768. "
        "In timm, patch merging sits at the start of stages 2, 3 and 4. "
        "Parameters: ViT base 86,567,656, about 86.6 million. Swin tiny 28,288,354, about 28.3 million. ViT is about three times larger."
    ),
),

dict(
    section="Part B · B1",
    title="B1 · The FPN answer, and viva check",
    kind="text",
    bullets=[
        "FPN needs a pyramid of maps at several resolutions, like ResNet C2–C5",
        "Swin's 4 stages give it: 56², 28², 14², 7² at strides 4, 8, 16, 32",
        "ViT: one 14 × 14 × 768 map at stride 16 in every block",
        "ViT global attention grows quadratically with image size",
        "Q: Where do 197 tokens come from? 196 patches + 1 [CLS]",
        "Q: features_only=True? Drops the head, returns the 4 stage maps",
    ],
    narration=(
        "The FPN answer. An FPN needs a pyramid of feature maps at several resolutions, like a ResNet's stages. "
        "Swin's four stages give exactly that, at strides 4, 8, 16 and 32. "
        "ViT keeps one 14 by 14 by 768 map at stride 16 in every block, so there is no fine map for small objects and no coarse one for large objects. "
        "We would have to build the pyramid by resizing. "
        "And ViT's global attention grows with the square of the token count, costly for large detection images, while Swin's grows linearly. "
        "Two viva questions. Where do 197 tokens come from? 196 patches plus one CLS token. "
        "What does features only do? It drops the classification head and returns the four stage maps."
    ),
),

# =====================================================================  B2
dict(
    section="Part B · B2",
    title="B2 · What the handout asks",
    kind="handout",
    page=3,
    find=[
        "Freeze both backbones.",
        "Train a logistic regression classifier on each set of features",
        "Report accuracy and macro-F1, show both confusion matrices",
        "Discuss which backbone gave better features for your data",
    ],
    bullets=[
        "Freeze both backbones; one feature vector per photo",
        "ViT: [CLS] token; Swin: global average pooling",
        "Logistic regression; one stratified 70/30 split, same for both",
        "Accuracy, macro-F1, confusion matrices, up to 3 misclassified per model",
        "Which backbone gave better features, and why?",
    ],
    narration=(
        "B2, the largest task, is a linear probe. "
        "Freeze both backbones, so their weights never change. "
        "Turn each photo into one feature vector: the CLS token for ViT, global average pooling for Swin. "
        "Train logistic regression on each, with one stratified 70 30 split, the same for both. Stratified means each class keeps its share in train and test. "
        "Report accuracy and macro F1, which averages the per-class F1 scores so every class counts equally. "
        "Show both confusion matrices, and up to three misclassified photos per model. "
        "Then discuss which backbone gave better features, and why."
    ),
),

dict(
    section="Part B · B2",
    title="Diagram: the linear probe",
    kind="figure",
    image="DG/linear_probe.png",
    bullets=[
        "Frozen backbone → one 768-number feature vector per photo",
        "StandardScaler → logistic regression → class",
        "Only the logistic regression is trained",
        "Good features = classes separable by flat boundaries",
    ],
    narration=(
        "This diagram shows the linear probe. "
        "On the left, a photo goes into the frozen backbone, ViT or Swin. Frozen means its weights never change. "
        "Out comes one feature vector of 768 numbers. Think of the backbone as an expert describer, writing 768 numbers about each photo. "
        "Next, a standard scaler puts every feature on the same scale. "
        "Then logistic regression, the simplest classifier, picks one of the four classes on the right. "
        "Only that last box is trained. "
        "If such a simple classifier separates your classes, the describer already places similar photos close together. "
        "So the probe measures the backbone's features, not a clever classifier. "
        "It also suits tiny data: 70 training photos are far too few to fine tune a big model, but plenty for this."
    ),
),

dict(
    section="Part B · B2",
    title="Formula card: logistic regression",
    kind="text",
    bullets=[
        "p(k | z) = softmax(W · z + b)k;   prediction = the class with highest p",
        "z = the photo's 768 features, after StandardScaler",
        "StandardScaler: (value − mean) / std, fitted on training photos only",
        "W, b = weights and bias: the only trained part (4 × 768 + 4 numbers)",
        "softmax turns 4 scores into 4 probabilities that add up to 1",
    ],
    narration=(
        "A formula card for the probe. z is the photo's feature vector, 768 numbers, after scaling. "
        "The standard scaler subtracts each feature's mean and divides by its standard deviation, both measured on the training photos. "
        "W is a weight matrix and b a bias. W times z plus b gives one score per class, so four scores. "
        "Softmax turns the four scores into four probabilities that add up to one. "
        "p of k given z is the probability of class k for this photo, and the prediction is the class with the highest probability. "
        "W and b are the only things trained, about three thousand numbers, against tens of millions in the backbone. "
        "Why freeze the backbone? Because we want to measure how linearly separable the pretrained features already are. "
        "Why standardise? Logistic regression works best when every feature is on the same scale. "
        "And the scaler is fitted on the training photos only, so no test statistics leak into training."
    ),
),

dict(
    section="Part B · B2",
    title="Formula card: accuracy, macro-F1 and log-loss",
    kind="text",
    bullets=[
        "accuracy = correct / total;   macro-F1 = mean of the 4 per-class F1",
        "precision = of photos predicted k, the share that really are k",
        "recall = of the real k photos, the share we found",
        "F1 = 2 · precision · recall / (precision + recall)",
        "log-loss = −(1/N) · Σ log p(true class); lower = confident and right",
        "N = number of test photos (30); Σ = sum over them",
    ],
    narration=(
        "The three metrics. Accuracy is simple: correct predictions over the total. "
        "For F1, we first need precision and recall for each class. "
        "Precision asks: of the photos we called shoe, how many really are shoes? "
        "Recall asks: of the real shoes, how many did we find? "
        "F1 combines them: two times precision times recall, over their sum. "
        "Macro F1 averages the four per-class F1 scores, so every class counts equally. "
        "Log loss looks at confidence. For each test photo, take the probability given to the true class, and take its log. "
        "Average over the N photos, here 30, and flip the sign. "
        "If the model is sure and right, the probability is near one, its log near zero, so the loss is small. Lower is better."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Code: one frozen feature vector per photo",
    kind="code",
    src="A2NB",
    start="def extract_features(model, transform, kind, batch_size=16):",
    n=12,
    hl=["torch.stack([transform(load_photo(p))", "out = model.forward_features(batch)", "vec = out[:, 0]", "vec = out.mean(dim=(1, 2))"],
    bullets=[
        "torch.no_grad + eval mode: backbones stay frozen",
        "forward_features: backbone only, no classification head",
        "ViT: out[:, 0] takes the [CLS] token from (B, 197, 768)",
        "Swin: mean over H and W of (B, 7, 7, 768): global average pooling",
        "Both give 768 numbers per photo",
    ],
    narration=(
        "This runs without gradients, with the models in eval mode, so the backbones stay frozen. "
        "Photos go in batches of 16, each loaded upright and passed through that model's own transform. "
        "forward features runs only the backbone, skipping the classification head. "
        "For ViT the output is batch by 197 by 768, and out colon zero takes token zero, the CLS token. "
        "ViT was trained to classify from that token. "
        "For Swin the output is batch by 7 by 7 by 768, and we average over height and width: global average pooling, "
        "which is also how Swin's own head pools. "
        "Both give 768 numbers per photo, a fair comparison. "
        "The alternative for ViT, averaging all 196 patch tokens, would also work, but the CLS token is what this model's own classifier reads. "
        "The saved output prints vit features, 100 by 768, and swin features, 100 by 768: one row per photo, for all 100 photos."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Code: one leak-free split and the probe",
    kind="code",
    src="A2NB",
    start='is_aug = np.array([p.stem.endswith("_aug") for p in PATHS])',
    n=17,
    hl=["train_test_split(real_idx, test_size=n_test, stratify=LABELS[real_idx], random_state=SEED)", "TRAIN_IDX = np.concatenate([train_real, aug_idx])", "assert not is_aug[TEST_IDX].any()", "LogisticRegression(max_iter=5000)"],
    bullets=[
        "Test photos drawn only from REAL photos: 30 of 100, stratified",
        "All 8 augmented copies go to training: 62 real + 8 = 70",
        "assert: no augmented photo in the test set",
        "Same TRAIN_IDX / TEST_IDX for both backbones",
        "StandardScaler + LogisticRegression(max_iter=5000)",
    ],
    narration=(
        "A design decision worth explaining. "
        "If a flipped copy were in training and its original in test, the probe would be tested on a photo it has basically seen. "
        "That is leakage, and it inflates results. "
        "So the code marks augmented photos by file name, then draws the 30 test photos from real photos only. "
        "n test is 0.3 times all 100 photos, so 30. In train test split, stratify equals the labels keeps each class's share in both parts, "
        "and random state equals SEED, 9005, makes the split repeatable. "
        "All augmented photos go to training: 62 real plus 8, which is 70. "
        "The assert checks that no augmented photo reached the test set. "
        "This one split serves both backbones, so they face exactly the same photos. "
        "The probe is a pipeline: a standard scaler, then logistic regression. In a pipeline, fit learns the scaler's means only from the training photos, "
        "so no test statistics leak in. "
        "Logistic regression keeps sklearn's defaults, an L2 penalty with C equal to one, except max iter 5000. "
        "The default of 100 iterations may stop before converging on 768 features, so we allow more."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Code: fitting both probes and computing the metrics",
    kind="code",
    src="A2NB",
    start="PREDS, PROBS = {}, {}",
    n=16,
    hl=['average="macro"', "log_loss(y_test, PROBS[name], labels=range(len(PHOTO_CLASSES)))", "PROBS[name][np.arange(len(y_test)), y_test]", "confusion_matrix(y_test, pred).tolist()"],
    bullets=[
        "One probe per backbone, same split",
        "macro-F1: F1 per class, then a plain mean",
        "log_loss with labels=range(4): knows all four classes",
        "Probability of the true class: fancy indexing, then mean",
        "Confusion matrix stored as a list in results.json",
    ],
    narration=(
        "This is where the two probes are trained and scored. "
        "The loop calls linear probe once for the ViT features and once for the Swin features, with the same split, "
        "and keeps the predicted labels and the predicted probabilities. y test holds the true labels of the 30 test photos. "
        "Then, for each backbone, five numbers. Accuracy score: the share of test photos predicted correctly. "
        "f1 score with average equals macro: compute F1 for each of the four classes separately, then take the plain mean, so every class counts equally. "
        "The alternative, average equals weighted, would let bigger classes count more; the handout asks for macro. "
        "n wrong counts the mistakes. "
        "Then two confidence measures, added because they can separate models that tie on accuracy. "
        "log loss takes the probabilities, and labels equals range of four tells it there are four classes, even if a class were missing from a small test set. "
        "The mean probability of the true class uses numpy fancy indexing: for row i, it picks the column of that photo's true label, and then averages. "
        "Finally the confusion matrix, rows the true class, columns the prediction, stored as a list so it can be written to results dot json."
    ),
),

dict(
    section="Part B · B2",
    title="Saved output: the split and the scores",
    kind="output",
    src="A2OUT",
    start="real photos: 92 | augmented: 8",
    n=5,
    hl=["real photos", "test per class", "0.0113", "0.0168"],
    bullets=[
        "92 real + 8 augmented; train 70, test 30",
        "Test per class 8, 7, 8, 7; train per class 17, 18, 17, 18",
        "Both: accuracy 1.0, macro-F1 1.0, 0 wrong",
        "Log-loss: ViT 0.0113, Swin 0.0168",
        "Mean p(true class): ViT 0.9898, Swin 0.9845",
    ],
    narration=(
        "The saved output of the probe cell. Line one: 92 real photos and 8 augmented copies. "
        "Line two: 70 photos for training and 30 for testing. "
        "Test per class is 8, 7, 8 and 7, in the alphabetical class order: glasses case, perfume, shoe, switch board. "
        "Thirty is not divisible by four, so a stratified split gives two classes 8 photos and two classes 7. "
        "Train per class is 17, 18, 17 and 18, which includes the 8 augmented copies, all on the training side. "
        "Then the scores table, one row per backbone. Accuracy 1.0 and macro F1 1.0 for both: every test photo is correct. "
        "n wrong is 0.0, printed with a decimal only because pandas stores the table as decimals. "
        "Test log loss: 0.0113 for ViT and 0.0168 for Swin. Lower means more probability on the right answer. "
        "Mean probability of the true class: 0.9898 for ViT and 0.9845 for Swin. "
        "So, on average, each probe gave the correct class about 98 to 99 percent probability. "
        "Both are perfect in accuracy, and ViT is very slightly more confident. With only 30 test photos, that is a very small difference."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Result: confusion matrices and misclassified photos",
    kind="figure",
    image="A2F/B2_confusion_matrices.png",
    image2="A2F/B2_misclassified.png",
    bullets=[
        "Both probes: 30 / 30 correct; accuracy 1.000, macro-F1 1.000",
        "Diagonal 8, 7, 8, 7: test photos per class",
        "No misclassified photos to show, for either model",
        "Tie broken by test log-loss: ViT 0.0113, Swin 0.0168",
        "Mean prob. of the true class: ViT 0.990, Swin 0.985",
    ],
    narration=(
        "Both confusion matrices are perfectly diagonal. Rows are the true class, columns the prediction, "
        "and every test photo is on the diagonal: 8, 7, 8 and 7 per class. "
        "Both probes got all 30 right. Accuracy one, macro F1 one. "
        "The lower panel is where misclassified photos would go. There are none, so it says so. "
        "So which is better? Accuracy cannot tell, so we compared confidence. "
        "Test log loss measures how much probability went to the right answer; lower is better. ViT 0.0113, Swin 0.0168. "
        "Mean probability of the true class: 0.990 against 0.985. "
        "ViT is slightly more confident, but the gap is tiny. On your photos, they are effectively equally good."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Code: the comparison rule",
    kind="code",
    src="A2NB",
    start='gap = b2["vit"]["n_wrong"] - b2["swin"]["n_wrong"]',
    n=13,
    hl=['gap = b2["vit"]["n_wrong"]', 'sure = min(["vit", "swin"], key=lambda k: b2[k]["test_log_loss"])', '< 0.01:', "That gap is tiny"],
    bullets=[
        "gap = ViT errors − Swin errors",
        "gap = 0: tie on errors, broken by lower test log-loss",
        "Verdict sentence built from stored numbers, never typed",
        "Log-loss gap < 0.01: 'effectively equally good'",
        "Same rule in the report script, so notebook and report agree",
    ],
    narration=(
        "The B2 discussion asks which backbone gave better features. "
        "The answer is decided by a rule written as code, and the report script uses the same rule, so the notebook and the report always agree. "
        "Line nine: gap is ViT's number of wrong test photos minus Swin's. "
        "If the gap is zero, the two tie on mistakes, which is what happened: both made none. "
        "Then line twelve breaks the tie with confidence. min with key equal to test log loss picks the backbone with the lower log loss, "
        "the one that put more probability on the right answers. "
        "The verdict sentence is then built from the stored numbers, so no number is typed by hand. "
        "Line eighteen adds a safety check. If the log loss gap is less than 0.01, the sentence adds that the gap is tiny, "
        "and that the backbones are effectively equally good. Otherwise it would say the winner separates the classes slightly better. "
        "Further down, not shown, is the other branch. If one backbone made fewer mistakes, it wins on errors, "
        "and if the difference is only one or two photos, the text warns that it could change with a different split. "
        "So the conclusion never claims more than the numbers support."
    ),
),

dict(
    section="Part B · B2",
    title="Saved output: the B2 verdict",
    kind="output",
    src="A2OUT",
    start="ViT-B/16  accuracy 1.000",
    n=3,
    hl=["ViT-B/16  accuracy", "Swin-T    accuracy", "Both backbones made"],
    bullets=[
        "ViT: acc 1.000, macro-F1 1.000, 0/30 wrong, log-loss 0.011, p 0.990",
        "Swin: acc 1.000, macro-F1 1.000, 0/30 wrong, log-loss 0.017, p 0.985",
        "Tie on errors, broken by confidence: ViT slightly ahead",
        "Gap 0.0168 − 0.0113 = 0.0055 < 0.01: effectively equal",
    ],
    narration=(
        "The saved output of the rule. The first two lines restate each backbone's numbers in one row. "
        "ViT B 16: accuracy 1.000, macro F1 1.000, wrong 0 out of 30, log loss 0.011, and mean probability of the true class 0.990. "
        "Swin T: accuracy 1.000, macro F1 1.000, wrong 0 out of 30, log loss 0.017, and mean probability 0.985. "
        "These are the same values as before, rounded to three decimals. "
        "Then the verdict, built by the rule we just read. "
        "Both backbones made the same number of test errors, zero out of 30, so the tie was broken by confidence. "
        "ViT was more confident in the right answers: log loss 0.011 against 0.017, and mean true class probability 0.990 against 0.985. "
        "The log loss gap, 0.0168 minus 0.0113, is 0.0055. That is below the 0.01 threshold, so the last sentence was added: "
        "the gap is tiny, so on these photos the two backbones are effectively equally good. "
        "That is the sentence to say in the viva. Do not claim that ViT is clearly better. "
        "The honest answer is a tie, with ViT marginally more confident."
    ),
),

dict(
    section="Part B · B2",
    title="B2 · Why both are perfect, and viva check",
    kind="text",
    bullets=[
        "ViT-B/16: 3× larger; weights pre-trained on ImageNet-21k, then ImageNet-1k",
        "Swin-T: ImageNet-1k only; local windows mix detail with overall shape",
        "Four very different everyday objects: an easy task for both",
        "With 30 test photos, one error = 3.3% accuracy",
        "Q: 100% for both, so which is better? Tie; log-loss gap tiny",
        "To separate them: harder classes, more test photos, more splits",
    ],
    narration=(
        "Why are both so good? ViT base is about three times larger, and timm's default ViT weights were pre-trained on ImageNet 21k, "
        "about 14 million images, before ImageNet 1k fine tuning. So its CLS token carries very general features. "
        "Swin tiny saw ImageNet 1k only, but its windows and merging mix fine detail with overall shape, "
        "and averaging over 49 positions is robust when the object is off centre. "
        "And your four classes look very different, so the task is easy. "
        "Viva check. With 30 test photos, one error is already 3.3 percent, so a perfect score cannot rank them. "
        "That is why log loss broke the tie, and the gap was tiny. "
        "To separate them: harder classes, more test photos, or several splits."
    ),
),

# =====================================================================  PART C
dict(
    section="Part C",
    title="Part C · What the handout asks",
    kind="handout",
    page=3,
    find=[
        "Use the settings for your digit d:",
        "Assume patch size 4, window size M = 7",
        "Give the output size (h × w × channels)",
        "Give the number of windows in each stage.",
    ],
    bullets=[
        "d = 5: image 448 × 448 × 3, C = 128",
        "Patch size 4, window M = 7, depths 2, 2, 6, 2",
        "Output size of the linear embedding and of each stage",
        "Number of windows in each stage",
        "By hand, showing all working",
    ],
    narration=(
        "Part C is worth 20 percent, done by hand with all working. "
        "For d equals 5, the image is 448 by 448 by 3, and C, the width after embedding, is 128. "
        "Everyone uses patch size 4, window size M equals 7, and depths 2, 2, 6 and 2, the number of blocks in each stage. "
        "Give the output size, height by width by channels, of the linear embedding and each of the four stages. "
        "Then the number of windows in each stage. "
        "It is the same Swin pipeline as in B1, with a bigger image and wider channels: 448 instead of 224, and 128 instead of 96."
    ),
),

dict(
    section="Part C",
    title="Part C · The attention cost question",
    kind="handout",
    page=4,
    find=[
        "For one attention layer in stage 1, compute",
        "and the ratio between them.",
    ],
    bullets=[
        "Ω(MSA) = 4hwC² + 2(hw)²C: global attention",
        "Ω(W-MSA) = 4hwC² + 2M²hwC: window attention",
        "One attention layer in stage 1, then the ratio",
        "Ω (omega) counts multiply-adds (softmax ignored)",
    ],
    narration=(
        "The last question: for one attention layer in stage 1, compute two costs and their ratio. "
        "Omega of MSA is global attention, every token to every token: four h w C squared, plus two times h w squared times C. "
        "Omega of W-MSA is window attention, inside 7 by 7 windows only: four h w C squared, plus two M squared h w C. "
        "h and w are the stage 1 grid height and width, C the channels, M the window size. "
        "Omega counts multiply-add operations, and ignores the softmax. "
        "Notice both formulas share the first term; only the second differs. That explains a neat check later."
    ),
),

dict(
    section="Part C",
    title="Part C · Output sizes and windows",
    kind="text",
    bullets=[
        "Embedding: 448 / 4 = 112 → 112 × 112 × 128 (each 4×4×3 = 48 values → 128)",
        "Stage 1 (2 blocks, no merging): 112 × 112 × 128",
        "Stage 2: 56 × 56 × 256;  Stage 3: 28 × 28 × 512;  Stage 4: 14 × 14 × 1024",
        "Windows = (side / 7)²",
        "256 → 64 → 16 → 4; every side divides by 7, no padding",
        "Each window holds M² = 49 tokens",
    ],
    narration=(
        "The sizes. 448 over 4 is 112 patches per side. Each patch has 4 times 4 times 3, 48 values, mapped to 128. "
        "So the embedding gives 112 by 112 by 128. "
        "Stage 1 has no merging, so it stays 112 by 112 by 128. "
        "Each later stage starts with patch merging: join 2 by 2 neighbours into four C, then a linear layer to two C. Side halves, channels double. "
        "Stage 2, 56 by 56 by 256. Stage 3, 28 by 28 by 512. Stage 4, 14 by 14 by 1024. "
        "Windows are the side over 7, squared. "
        "112 over 7 is 16, squared is 256. Then 8 squared, 64. 4 squared, 16. 2 squared, 4. "
        "Every side divides by 7, so no padding."
    ),
),

dict(
    section="Part C",
    title="Formula card: Ω(MSA) and Ω(W-MSA)",
    kind="text",
    bullets=[
        "Ω(MSA) = 4hwC² + 2(hw)²C        Ω(W-MSA) = 4hwC² + 2M²hwC",
        "Ω (omega) = cost in multiply-adds; softmax and heads are ignored",
        "h, w = token grid height and width in stage 1; hw = number of tokens",
        "C = channels per token; M = 7, so M² = 49 tokens per window",
        "4hwC² = query, key, value and output projections: same in both",
        "2(hw)²C = QKᵀ + attention × V;  2M²hwC = the same, but only 49 keys per query",
    ],
    narration=(
        "Omega means cost, counted in multiply-adds. "
        "h and w are the height and width of the token grid in stage 1, so h times w is the number of tokens. "
        "C is the channels per token, and M is the window size, 7, so M squared is 49. "
        "The first term, four h w C squared, is shared. Attention makes a query, key and value for every token, plus an output projection: "
        "four C by C matrices applied to h w tokens. "
        "The second term has two parts. Q times K transposed compares every query with every key: h w times h w pairs, each costing C. "
        "Then the attention weights times V mixes the values, at the same cost. Together, two h w squared C. "
        "In window attention, each token is compared only with its 49 window neighbours: two M squared h w C. "
        "Each query now has only 49 keys, a fixed number, so window cost grows in a straight line with h w, while global cost grows with its square. "
        "What do plain windows lose? Tokens in different windows never meet. Shifted windows, moved by about half a window in alternate blocks, let neighbouring windows exchange information, at the same cost as plain windows. "
        "Like the Swin paper, these counts ignore softmax and heads."
    ),
),

dict(
    section="Part C",
    title="Part C · Computing the costs and the ratio",
    kind="text",
    bullets=[
        "hw = 112² = 12,544; C² = 16,384; M² = 49",
        "4hwC² = 822,083,584 (same in both)",
        "Ω(MSA) = 822,083,584 + 40,282,095,616 = 41,104,179,200",
        "Ω(W-MSA) = 822,083,584 + 157,351,936 = 979,435,520",
        "Ratio ≈ 41.97; check: (2C + hw)/(2C + M²) = 12,800 / 305",
        "Attention terms only: hw / M² = 256 = stage-1 windows",
    ],
    narration=(
        "The numbers. h w is 112 squared, 12,544. C squared is 16,384. M squared is 49. "
        "The shared term, four h w C squared, is 822,083,584. "
        "Global attention adds 40,282,095,616, so omega of MSA is 41,104,179,200, about 4.11 times ten to the ten. "
        "Window attention adds 157,351,936, so omega of W-MSA is 979,435,520, about 9.79 times ten to the eight. "
        "The ratio is about 41.97. Global attention costs about 42 times more. "
        "A check on paper: divide both by two h w C. The ratio becomes two C plus h w, over two C plus M squared: 12,800 over 305, again 41.97. "
        "Why is the ratio 41.97 and not 256? Comparing the attention terms alone gives h w over M squared, 256, exactly the stage 1 window count. "
        "But windowing only shrinks the second term. The projection term, 822 million, is paid in full by both, so it pulls the full ratio down to 42. "
        "A small code cell in the notebook recomputes all of this and prints the same numbers."
    ),
),

dict(
    section="Part C",
    title="Part C · Code: checking the sizes and windows",
    kind="code",
    src="A2NB",
    start="PART_C_SETTINGS = {0: (224, 64)",
    n=15,
    hl=["H, C = PART_C_SETTINGS[d]", "P, M, DEPTHS = 4, 7, (2, 2, 6, 2)", "side, ch = side // 2, ch * 2", '"windows": f"({side}/{M})² = {(side // M) ** 2}"'],
    bullets=[
        "The handout's settings table, looked up with d: (448, 128)",
        "P = 4, M = 7, depths 2, 2, 6, 2",
        "Embedding: 448 // 4 = 112, 128 channels",
        "Stages 2–4: side ÷ 2, channels × 2 (patch merging)",
        "Windows = (side // 7)²: every side divides by 7 exactly",
    ],
    narration=(
        "Part C was done by hand, and this cell checks the hand working with code. "
        "Lines two and three copy the handout's table of settings into a dictionary: one entry per digit, holding the image size and C. "
        "Line four looks up your row with d. For 5, that is 448 and 128. "
        "Because d is computed from your roll number, the cell cannot use another student's settings by mistake. "
        "Line five fixes the shared settings: patch size 4, window size M equal to 7, and depths 2, 2, 6 and 2. "
        "Line eight starts with side equal to 448 floor-divided by 4, which is 112, and 128 channels: the linear embedding. "
        "The loop then builds one row per stage. For stages after the first, line twelve is patch merging: the side is halved and the channels doubled. "
        "Stage one skips it, because stage one has no merging. "
        "The windows column divides the side by M and squares it. "
        "It uses floor division, which is safe here only because every side, 112, 56, 28 and 14, divides by 7 exactly. "
        "If a side did not divide by 7, the grid would need padding, and this simple formula would not be enough. "
        "display then shows the table, which you will see in the output in a moment."
    ),
),

dict(
    section="Part C",
    title="Part C · Code: the two costs and their ratio",
    kind="code",
    src="A2NB",
    start="hw = (H // P) ** 2",
    n=8,
    hl=["proj = 4 * hw * C ** 2", "msa = proj + 2 * hw ** 2 * C", "wmsa = proj + 2 * M ** 2 * hw * C", 'print(f"ratio'],
    bullets=[
        "hw = (448 // 4)² = 112² tokens in stage 1",
        "proj = 4hwC²: Q, K, V and output projections, shared",
        "msa = proj + 2(hw)²C;  wmsa = proj + 2M²hwC",
        "Python integers are exact: no rounding in 41 billion",
        "Only the ratio is a decimal, printed to 2 places",
    ],
    narration=(
        "The second half computes the attention costs, term by term, with the same formulas as the handout. "
        "Line 18: h w is 448 over 4, squared, so 112 squared, the number of tokens in stage one. "
        "Line 19: proj is four times h w times C squared. That is the projection term shared by both formulas: queries, keys, values and the output projection. "
        "Line 20: msa adds two times h w squared times C, the global attention term, where every token is compared with every token. "
        "Line 21: wmsa adds two times M squared times h w times C instead, where each token is compared only with the 49 tokens in its window. "
        "Keeping proj as its own variable makes the shared term visible. "
        "The prints show both parts of each sum separately, so each printed piece can be matched to a line of the hand working. "
        "Python integers have no size limit, so 41 billion is computed exactly, with no rounding, "
        "unlike a pocket calculator that might switch to scientific notation. "
        "Only the final ratio is a decimal, printed to two places. "
        "All values are also saved to results dot json under C, so the report's Part C numbers come from the same computation."
    ),
),

dict(
    section="Part C",
    title="Saved output: the Part C numbers",
    kind="output",
    src="A2OUT",
    start="layer output (h×w×c)",
    n=10,
    hl=["stage 1 (2 blocks)", "Omega(MSA)", "Omega(W-MSA)", "ratio"],
    bullets=[
        "112² × 128 → 56² × 256 → 28² × 512 → 14² × 1024",
        "Windows 256, 64, 16, 4",
        "Ω(MSA) = 822,083,584 + 40,282,095,616 = 41,104,179,200",
        "Ω(W-MSA) = 822,083,584 + 157,351,936 = 979,435,520",
        "Ratio 41.97; attention terms alone: exactly 256",
    ],
    narration=(
        "The saved output matches the hand working exactly. The table first. "
        "Linear embedding: 112 by 112 by 128, with a dash for windows, because attention has not started yet. "
        "Stage one, two blocks: 112 by 112 by 128, and 112 over 7, squared, is 256 windows. "
        "Stage two: 56 by 56 by 256, 64 windows. Stage three, six blocks: 28 by 28 by 512, 16 windows. Stage four: 14 by 14 by 1024, 4 windows. "
        "Then the cost lines. h w equals 12,544. "
        "Omega of MSA equals 822,083,584, the projection term, plus 40,282,095,616, the global attention term, giving 41,104,179,200. "
        "Omega of W-MSA equals the same 822,083,584, plus 157,351,936, giving 979,435,520. "
        "And the ratio, 41.97. "
        "Now compare the two attention terms: about 40.3 billion against about 157 million. "
        "Their ratio is exactly 256, which is h w over M squared, and also the number of stage one windows. "
        "But the shared projection term is added to both, and that pulls the full ratio down to about 42. "
        "If the examiner asks you to verify, point to this output and to the line-by-line working in the report."
    ),
),

# =====================================================================  DELIVERABLES
dict(
    section="Deliverables",
    title="Deliverables and the report",
    kind="handout",
    page=4,
    find=[
        "One Colab notebook (RollNo_A2.ipynb) with all cells executed",
        "One report (PDF, at most 8 pages)",
        "The trained Part A checkpoint and your Part B photos",
    ],
    bullets=[
        "26L-9005_A2.ipynb with every cell executed",
        "26L-9005_A2_report.pdf: 6 pages, under the 8-page limit",
        "Drive folder: ddpm_linear.pt, ddpm_cosine.pt and the photos",
        "Drive link written in the report",
        "Every report number comes from results.json",
    ],
    narration=(
        "Three deliverables. "
        "One, the Colab notebook with all cells executed, so nothing needs re-running: 26L-9005 underscore A2 dot ipynb. "
        "Two, a report of at most eight pages, with figures, tables, discussion and the Part C working. Yours is six pages. "
        "Three, the Part A checkpoints and your Part B photos in a Google Drive folder, linked in the report. "
        "Yours holds ddpm linear, ddpm cosine, and the photos folder with its file map. "
        "One design choice to mention: every part saves its figures to a folder and its numbers to results dot json, "
        "and the report was built from those files, not typed by hand. So report and notebook always agree."
    ),
),

# =====================================================================  CLOSING
dict(
    section="Closing",
    title="Viva checklist: numbers to know cold",
    kind="text",
    bullets=[
        "d = 5: Sandal, Bag, Trouser; 18,000 images; Part C 448 × 448, C = 128",
        "A1: ᾱ < 0.5 at 259 vs 496; < 0.01 at 673 vs 935",
        "A2: U-Net 3,939,393 params; AdamW, LR 5e-4, batch 128, 28 epochs, 3,920 steps",
        "A3: cosine β999 = 0.999, 1/√α ≈ 31.6; unclipped 62.5% black; ~16 s per 16",
        "B: 92 real + 8 aug (train only); both 30/30; log-loss 0.0113 vs 0.0168",
        "C: 41,104,179,200 / 979,435,520 ≈ 41.97 = 12,800 / 305",
    ],
    narration=(
        "A checklist to say out loud before the viva. "
        "Digit 5: Sandal, Bag, Trouser, 18,000 images, and for Part C a 448 image with C equals 128. "
        "A1: linear destroys faster. Below one half at 259 against 496, below 0.01 at 673 against 935. "
        "A2: a 3,939,393 parameter U-Net, random weights, AdamW, five times ten to the minus four, batch 128, 28 epochs, 3,920 steps, about 16 minutes each. "
        "Losses are not comparable across schedules. "
        "A3: cosine's last beta is 0.999, one over root alpha about 31.6, so we clip. Without it, 62.5 percent black. "
        "Part B: 92 real photos plus 8 augmented, training only. Both probes 30 out of 30, log loss 0.0113 against 0.0168. "
        "Part C: a ratio of about 42, or 12,800 over 305."
    ),
),

dict(
    section="Closing",
    title="How to handle the viva",
    kind="text",
    bullets=[
        "Start every answer from the idea, then the code, then the number",
        "Own the deviations: x̂0 clipping and the 8 augmented photos",
        "Point to the evidence: the ablation cell, the split assert, results.json",
        "Be modest about weak evidence: 16 samples, 30 test photos",
        "Have your phone photos and the notebook open",
    ],
    narration=(
        "Last tips. Answer each question in order: the idea in plain words, then the code, then the number. "
        "That shows understanding, not recitation. "
        "Two things differ from a literal reading of the handout: clipping x hat zero, and the eight augmented photos. "
        "Mention them openly, explain why, and point to the evidence: the ablation cell, and the assert that keeps augmented photos out of the test set. "
        "Be modest where evidence is thin: sixteen samples, and thirty test photos. "
        "Keep your phone and the executed notebook ready. "
        "If you do not know something, say what you do know, and reason out loud. "
        "You built every piece of this. Take your time, and good luck."
    ),
),

]


if __name__ == "__main__":
    words = sum(len(s["narration"].split()) for s in SLIDES)
    print(f"{len(SLIDES)} slides, {words} narration words, ~{words / 140:.1f} min at 140 wpm")
