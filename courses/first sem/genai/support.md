# Generative AI — Support Guide for the Available Lectures

**Concise explanations first, worked calculations for quizzes and midterms, and optional longer lessons for depth.**

Based on the files available on **16 September 2026**. Page numbers below are **PDF page positions**, including title slides. Repeated slide builds are grouped. This guide supports the supplied Introduction, AE/VAE, GANs Part 1 and GANs Part 2 decks, plus Assignment 1 and its starter notebook.

**Jump to:** [Introduction](#lecture-1) · [AE and VAE](#lecture-2) · [GANs Part 1](#lecture-3) · [GANs Part 2](#lecture-4) · [Assignment support](#assignment-support) · [Numerical practice and answers](numerical-practice.md) · [Study route](#study-route)

## How to use this guide

1. Read the topic's **Study** points alongside the specified lecture pages.
2. Watch **First watch** for intuition. Short means a focused lesson or a bounded excerpt, not necessarily a vertical YouTube Short. Start links do **not** stop playback automatically; stop at the listed end time.
3. Follow **Numerical preparation** for the calculation topics. A conceptual explanation or symbolic derivation alone is not a worked-number lesson. Where a matching numerical video was not verified, use the explicitly labeled written example.
4. Cover the answer, calculate the example, then attempt the fresh question in [numerical practice](numerical-practice.md). Explain the sign, averaging, dimensions, and meaning of your answer.
5. Choose **Optional depth** if you need a fuller derivation or implementation. Reused videos need only be watched once unless you need a refresher.

### Course material and scope

| Supplied source | What it contributes |
| --- | --- |
| [Lecture 1 — Introduction](Lecture1%20Introduction.pdf) | 41 pages: generative modeling, applications, model families, Bayes example, data/model distributions |
| [Lecture 2 — AE and VAE](Lecture%202%20AE%20and%20VAE%20v2.pdf) | 71 pages: reconstruction, latent spaces, variational modeling, KL, sampling and applications |
| [GANs Part 1](Lecture%20GANs%20Part%201.pdf) | 70 pages: adversarial training, loss/gradient issues, collapse, DCGAN and examples |
| [GANs Part 2](Lecture%20GANs%20Part%202.pdf) | 97 pages: conditional GANs, StackGAN, entropy/IS, FID and improved generative precision/recall |
| [Assignment 1](Assignment%201.pdf) | 4 pages: controlled AE/VAE experiments, GAN failures/stabilization, quantitative evaluation |
| [A1 starter notebook](A1%20starter.ipynb) | Architecture and logging scaffolds; TODOs and a few discrepancies with the handout |
| [Course outline](GenAI_courseOutline%20MSDS.pdf) | 3 pages: planned semester coverage and assessment information |

The outline also schedules diffusion/DDPM, CLIP, transformers, Stable Diffusion, LLMs/Mistral, MoE, fine-tuning/LoRA/QLoRA, RAG/GraphRAG, and agents. Those later lecture decks are **not supplied yet**. Brief appearances in the Introduction are examples, not full treatments. The outline places Midterm 1 after additional topics; this guide alone therefore does not establish complete Midterm 1 coverage. Use the instructor's announced scope for each assessment.

<a id="lecture-1"></a>
## Lecture 1 — Generative modeling foundations

### 1.1 Learn a distribution, then draw a new sample

**Source:** pages 1–4, 37–39.

**Study**

- `x` is one observation, such as an image with many pixel values. A dataset contains many observations; do not confuse the number of samples with the number of features per sample.
- `p_data` is the unknown process/distribution that produced the examples. Training fits parameters `θ` of a model distribution `p_θ`, using finite data.
- **Density estimation** asks how the model distributes probability; **generation** draws samples. A model can support one operation more directly than the other.
- An ordinary GAN samples through `x=G(z)` and implicitly defines a distribution; it generally does not provide an easily evaluated `p_θ(x)`. For continuous data, density at a point is not the probability of that exact point; probabilities come from regions.

**First watch:** [StatQuest — Sampling from a Distribution](https://www.youtube.com/watch?v=XLCWeSVzHUU) — **3:48**, focused intuition about what sampling means. Then use the lecture's density-versus-samples picture to distinguish fitting from drawing.

**Numerical preparation:** [N1.2 — distributions and sampling](numerical-practice.md#n1-2) gives a small probability table, cumulative sampling intervals, expected counts, and a fresh retry. This is a written course bridge, not a claim that the video solves this exact example.

**Self-check:** If a model memorizes five training images and chooses one at random, can it generate outputs? Does that establish that it learned the wider data distribution? Explain why the answers differ.

### 1.2 Why generative models: samples, representation, debiasing and outliers

**Source:** pages 2, 5–11, 24, 35.

**Study**

- Generation can produce text, images, music, video, or candidate molecular structures. A plausible sample still needs task-specific evaluation.
- The face examples motivate latent factors such as pose and illumination. A useful representation may let us inspect underrepresented regions and improve sampling.
- **Debiasing is an objective, not an automatic property.** A generator can reproduce training imbalance. Test representation and downstream performance; do not infer fairness from a visually varied grid.
- **Outlier detection** seeks unusual observations. A low model score or large reconstruction error is a possible signal, not a universal guarantee that an example is anomalous.

**First watch:** [IBM Technology — What are Generative AI models?](https://www.youtube.com/watch?v=hfIUstzHs9A) — **8:47**, a broad introduction with an LLM/enterprise emphasis. For the bias and trust questions, [IBM — What is AI Ethics?](https://www.youtube.com/watch?v=aGwYtUzMQUk) — **6:10**. The latter is general AI ethics, not a numerical latent-space debiasing demonstration.

**Course bridge:** Connect the face grid on page 5 to the AE/VAE representation sections below. Connect the driving examples on page 6 to reconstruction-based anomaly detection. DiT, text-to-music, and Sora on pages 9–11 illustrate modalities; detailed diffusion mechanisms await later lectures.

**Self-check:** Name one benefit, one possible failure, and one observable evaluation for each of synthetic faces, generated summaries, and an outlier detector. Does generating more images necessarily fix a missing group?

### 1.3 Historical context: model ideas versus product milestones

**Source:** pages 12–13.

**Study:** Explain how latent-variable, adversarial, attention-based, and denoising approaches contributed different ways to model data. Separate the date of a research idea from later popular applications. The slide's recent product/trend timeline is context rather than a precise taxonomy of “reasoning,” “open source,” or model architecture.

**First watch:** Reuse [IBM's overview](https://www.youtube.com/watch?v=hfIUstzHs9A) — **8:47** for how the modern applications fit together. It does not reproduce every year on the slide; use the compact research timeline below for those foundations.

| Research milestone | Date and primary reference |
| --- | --- |
| Auto-Encoding Variational Bayes | 2013 preprint; [Kingma and Welling](https://arxiv.org/abs/1312.6114) |
| Generative Adversarial Networks | 2014; [Goodfellow and colleagues](https://arxiv.org/abs/1406.2661) |
| Early diffusion-based generative modeling | 2015; [Sohl-Dickstein and colleagues](https://arxiv.org/abs/1503.03585) |
| Transformer architecture | 2017; [Attention Is All You Need](https://arxiv.org/abs/1706.03762) |
| Denoising Diffusion Probabilistic Models | 2020; [Ho and colleagues](https://arxiv.org/abs/2006.11239) |

**Self-check:** Why is “diffusion was invented when image-generation products became popular” inaccurate? Which mathematical distinction separates an adversarial training game from an autoencoder reconstruction objective?

### 1.4 Challenges: hallucination, bias, deepfakes, privacy and compute

**Source:** page 14, connected to pages 5–11.

**First watch:** [IBM — Why Large Language Models Hallucinate](https://www.youtube.com/watch?v=cfqtFvWOfg0) — **9:37**, conceptual examples of plausible but incorrect outputs. Reuse [What is AI Ethics?](https://www.youtube.com/watch?v=aGwYtUzMQUk) — **6:10** for bias, transparency and trust.

**Study:** Distinguish false factual content, harmful representation, deceptive use of realistic media, exposure of sensitive training data, and resource cost. For each, identify what the failure would look like and a relevant check. Fluent output alone verifies none of these. Larger models and more sampling also require memory and computation; measure the actual workload instead of assuming a universal cost. The ethical framework is broader than image realism or reconstruction error.

**Self-check:** A generated report is grammatical but cites a nonexistent study; a face generator omits some appearances; an accurate model leaks a private example. Explain why these are three different evaluation problems. No arithmetic is required for this conceptual topic.

### 1.5 Discriminative and generative: read the conditioning carefully

**Source:** pages 15–28, 30–36.

**First watch:** [Google Cloud Tech — Introduction to Generative AI](https://www.youtube.com/watch?v=G2fqAlgmoPo&t=360s) — **clip 6:00–7:30 · 1:30**, the model-type comparison and cat classification/generation example in a **22:07** lesson. These boundaries were checked against the video's visual storyboard; rewind slightly if you need the preceding setup. The full lesson is optional.

| Question | Distribution or output | Example |
| --- | --- | --- |
| Given features, which class? | `p(y|x)` or a direct decision rule | Logistic regression, classifier CNN, SVM decision score |
| What observations resemble the data? | `p(x)` or an implicit sampler | Unconditional VAE/GAN |
| What does each labeled class look like? | `p(x,y)=p(x|y)p(y)` | A generative classifier such as Naive Bayes |
| Generate an observation given a condition | `p(x|c)` | Class-conditioned image generation |

**Important refinements to the slide tables**

- `p(x)` and `p(x,y)` describe different setups, not contradictory definitions of generative modeling. A joint model yields `p(x)` by summing over labels, and a classifier via Bayes' rule.
- The symbol after the bar says what is given. Text translation can be **conditional generation**; “conditional” does not automatically mean a discriminative classifier.
- CNNs and transformers are architectures that can appear in either family. A GAN itself contains a generative network and a discriminative network.
- A generative model does not automatically classify, handle every missing-data pattern, expose a tractable density, or learn interpretable factors. Those capabilities depend on its assumptions and training. Labeled-data efficiency and classification accuracy are comparisons to test, not universal rankings.
- The generative family slide names GMMs, HMMs and autoregressive LMs as examples; it does not teach their full training algorithms here. A GMM mixes component densities; an HMM adds latent state transitions; an autoregressive model factors a sequence into next-element conditionals.

**Numerical preparation:** [N1.1](numerical-practice.md#n1-1) turns a joint model into a classifier. [N1.3](numerical-practice.md#n1-3) checks the conceptual distinctions with answer cues.

**Self-check:** Explain why sampling a class label from a classifier does not generate a new input image. Give one task where a generative model can classify and one where a CNN can generate.

### 1.6 Spam filtering: likelihood, prior, normalization and posterior

**Source:** page 29.

**Study:** The slide gives `P(spam)=.4`, `P(win|spam)=.6`, and `P(win|ham)=.05`. Multiply each likelihood by its prior, then normalize **across both classes**. The unnormalized values `.24` and `.03` are joint probabilities, not posterior answers.

**First watch:** [StatQuest — Bayes' Theorem](https://www.youtube.com/watch?v=9wCnvr7Xw4E&t=321s) — **clip 5:21–9:12 · 3:51** for the derivation. Full lesson **13:59** if conditional probability is unfamiliar.

**Worked numerical video:** [StatQuest — Naive Bayes](https://www.youtube.com/watch?v=O2L2Uv9pdDA&t=262s) — **clip 4:22–7:33 · 3:11**, an actual “Dear Friend” classification calculation; first watch **1:08–4:22 · 3:14** if the probability tables are new. The full video is **15:12**. Its example is multinomial word-count Naive Bayes; the lecture's single binary word-presence example has a simpler likelihood model. They share the prior-times-likelihood calculation, but do not interchange their word-event definitions.

**Written calculation and fresh retry:** [N1.1 — normalized spam probabilities](numerical-practice.md#n1-1), including the complementary “word absent” case.

**Slide correction:** Logistic regression normally fits conditional likelihood/cross-entropy, rather than directly maximizing the discontinuous classification-accuracy score. A single word-presence model also generates only that modeled feature; generating a coherent email needs a richer model.

**Self-check:** Why is the answer about `.889`, rather than `.6` or `.24`? If the spam prior changes while both likelihoods stay fixed, must the posterior stay the same?

### 1.7 Data versus model: fidelity, coverage, sampling and representation

**Source:** pages 37–41.

**Study:** Revisit the map: **A** is allowed by the model but implausible under the data; **B** is a valid data region the model cannot generate; **C** is compatible with both. A model can generate attractive examples while missing much of the distribution. The lecture's desired properties are accuracy of the modeled distribution, practical sampling, and useful representation; none follows solely from a few good samples.

**First watch:** Reuse [StatQuest — Sampling from a Distribution](https://www.youtube.com/watch?v=XLCWeSVzHUU) — **3:48**. The map and [N1.2's discrete example](numerical-practice.md#n1-2) supply the exact fidelity/coverage comparison absent from that introductory video. GAN collapse and the assignment's metrics return to this distinction.

**Self-check:** Could a generator have excellent-looking individual samples yet omit a real mode? Could two models have equal classification-style accuracy and different sample coverage? Explain with A, B and C rather than slogans.

### Optional depth — Introduction

- [Google Cloud Tech — Introduction to Generative AI](https://www.youtube.com/watch?v=G2fqAlgmoPo) — **22:07**, a fuller overview of model types, uses and vocabulary. Later product/platform sections are not required for the supplied lecture math.
- [MIT 6.7960 — Generative Models: Basics, Phillip Isola](https://www.youtube.com/watch?v=hJlrAHqGOS8) — **1:21:18**. The [official course page](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/resources/mit6_7960f24_lec14_mp4/) identifies density/energy models, sampling, GANs, autoregressive models and diffusion. This is broader mathematical context, not a short prerequisite or evidence that later topics are already in your supplied decks.

<a id="lecture-2"></a>

## Lecture 2 — Autoencoders and variational autoencoders

**Source:** [Lecture 2 AE and VAE v2.pdf](Lecture%202%20AE%20and%20VAE%20v2.pdf), all 71 PDF pages. Page references below use the PDF viewer's page number.

**Two study routes:** learn the short explanation first, then work the linked calculation without looking at its answer. A video marked **intuition** explains the idea; **derivation** manipulates symbols; **worked numbers** substitutes actual values. All three help, but only the last two plus your own practice prepare you to calculate independently.

**Notation checkpoint:** this guide uses `qφ(z|x)` for the encoder's approximate posterior, `pθ(x|z)` for the decoder likelihood, and `p(z)` for the prior. Pages 29–35 use different encoder/decoder letters. Follow the role, not just the letter. Use `σ` for standard deviation, `v = σ²` for variance, and `ℓ = log v` for log-variance. **The KL expression on page 35 has the wrong sign as printed; use the corrected derivation on pages 38–45.** A KL divergence cannot be negative.

### 2.1 Latent variables and the encoder–decoder idea

**Slides:** pp. 1–8, 10; recap pp. 66–70.

A latent variable is an unobserved factor that helps explain the observations: pose helps explain face pixels. An encoder maps a large input `x` into a smaller code `z`; a decoder maps `z` into a reconstruction `x̂`. The original image supplies its own training target, so class labels are unnecessary. A learned coordinate is not automatically a named human attribute.

- **Short — intuition:** [MIT / Ava Amini: latent variables, 8:16–10:50](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=496s) — **2:34 excerpt**.
- **Short — intuition:** [IBM Technology: What are Autoencoders?](https://www.youtube.com/watch?v=qiUEgSCyY5o) — **4:59**, complete introduction.
- **Calculate:** [N2.1: trace one image through a tiny AE](numerical-practice.md#n2-1).
- **Self-check:** which component do you keep to retrieve similar images? **The encoder**, because it produces the searchable code.

### 2.2 Bottlenecks, compression, reconstruction loss, and PCA

**Slides:** pp. 7–12.

The bottleneck limits how much information passes through the network. The reconstruction objective rewards preserving useful information. The slides use squared Euclidean error `‖x − x̂‖²`: **sum** the squared coordinate errors. Mean squared error divides this by the coordinate count; state which one you use. Smaller codes can lose detail; a larger code is not a guarantee of useful generalization.

PCA gives a linear low-dimensional subspace. An AE with nonlinear activations can learn nonlinear encodings. A suitably constrained linear AE trained with squared error can recover the PCA subspace; arbitrary nonlinear AEs are not simply PCA with a new name. A 784-to-2 code is a reduction in stored coordinates, not automatically a measured file compression ratio: precision and model storage also matter.

- **Short — intuition:** [MIT: autoencoders, 10:50–17:02](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=650s) — **6:12 excerpt**.
- **Short — worked numbers/formulas:** [Luis Serrano: reconstruction loss, 25:46–27:11](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1546s) — **1:25 replay** showing small pixel arrays and squared-error/log-loss calculations. Learn the architecture first; this is a replay-sized section.
- **Optional depth:** [Serrano: dimensionality reduction, 3:35–10:50](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=215s) — **7:15 excerpt** with a small image example.
- **Calculate:** [N2.1: all seven AE parameter gradients and one simultaneous update](numerical-practice.md#n2-1); [N2.2: coordinate counts and retrieval](numerical-practice.md#n2-2).
- **Self-check:** if SSE is `0.08` for four pixels, MSE is **`0.02`**; their gradient scales differ by four.

### 2.3 Image retrieval in latent space

**Slides:** pp. 11, 13–14.

Encode and store each database image once. Encode the query, compare its code against stored codes, and rank the matches. Euclidean distance measures separation; cosine similarity measures direction and ignores positive scaling. They can produce different rankings. Reconstruction training alone does not guarantee that human notions of similarity will match these rankings.

- **Short — worked numbers:** [StatQuest: cosine equation and calculation, 6:19–10:13](https://www.youtube.com/watch?v=e9U0QAFbfLI&t=379s) — **3:54 excerpt**; its vectors are word counts. Apply the same arithmetic to image codes.
- **Optional complete lesson:** [Cosine Similarity, Clearly Explained!!!](https://www.youtube.com/watch?v=e9U0QAFbfLI) — **10:13**.
- **Course bridge:** the video supplies the distance calculation, while pp. 13–14 supply the AE retrieval pipeline. [N2.2](numerical-practice.md#n2-2) joins them in one worked image-code example.
- **Self-check:** can you calculate cosine similarity for the zero vector? **No: its norm makes the denominator zero.**

### 2.4 Denoising autoencoders

**Slides:** pp. 11, 15–17.

During training, input the corrupted image and compare the reconstruction against its **clean** target. At inference, only the noisy image is available; the decoder predicts a clean-looking reconstruction. The loss computation uses the clean target during training, but the decoder does not look up or subtract an unavailable original at inference. Denoising quality depends on the learned data and noise patterns.

- **Short — intuition with a small image example:** [Serrano: denoising autoencoders, 10:50–18:15](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=650s) — **7:25 excerpt**.
- **Calculate:** [N2.3: compare loss against clean and noisy targets](numerical-practice.md#n2-3).
- **Self-check:** a model that perfectly copies a noisy input can have zero input-copy loss while still failing the denoising task.

### 2.5 Image colorization

**Slides:** pp. 11, 18.

Train on paired grayscale inputs and color targets. The architecture predicts color information missing from the input. Multiple colors may be plausible for the same gray value, so a prediction need not recover the original real-world color uniquely.

- **Short — architecture/application:** [DigitalSreeni: image colorization, 0:40–3:00](https://www.youtube.com/watch?v=EujccFRio7o&t=40s) — **2:20 excerpt** of the task and encoder–decoder diagram.
- **Optional implementation:** [90 — Application of Autoencoders: Image colorization](https://www.youtube.com/watch?v=EujccFRio7o) — **20:51**, Python walkthrough. It uses a color-space implementation; keep your course's requested output representation when coding.
- **Self-check:** grayscale-to-grayscale training does **not** teach a model to predict the missing colors. For an RGB target of size `H × W`, the output has `3HW` values; see the fresh exercise in [N2.3](numerical-practice.md#n2-3).

### 2.6 Anomaly detection from reconstruction error

**Slides:** pp. 11, 19.

Train on representative normal data. Calculate an input's reconstruction error and compare it with a chosen threshold. High error is a warning signal, not proof of an anomaly; some unusual inputs can reconstruct well and some normal inputs poorly. Choose the threshold using validation data and evaluate false alarms as well as missed anomalies.

- **Short — application and data example:** [DigitalSreeni: anomaly detection, 1:40–4:00](https://www.youtube.com/watch?v=u1vLJBwOFC8&t=100s) — **2:20 excerpt**.
- **Optional implementation:** [88 — Applications of Autoencoders: Anomaly Detection](https://www.youtube.com/watch?v=u1vLJBwOFC8) — **18:35**, reconstruction-error detection on synthetic data; this is a coding example, not a complete hand calculation.
- **Calculate:** [N2.3: losses, threshold decisions, and the equality boundary](numerical-practice.md#n2-3).
- **Self-check:** if the rule is `error > τ`, an error **equal to** `τ` is not flagged.

### 2.7 Why a VAE encodes a distribution

**Slides:** pp. 20–28.

A plain AE learns useful codes for reconstruction but does not impose a known sampling distribution over those codes. Randomly chosen codes can land between regions it has learned to decode. A VAE encoder outputs distribution parameters for each input; a latent sample from that distribution goes into the decoder. For `k` latent dimensions, mean and log-variance heads each have `k` outputs, while the sampled code still has `k` coordinates.

- **Short — intuition:** [MIT: variational autoencoders, 17:02–23:25](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1022s) — **6:23 excerpt**.
- **Alternative — visualization:** [Serrano: autoencoders as generators, 18:15–23:36](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1095s) — **5:21 excerpt**.
- **Calculate:** [N2.5: mean, variance, log-variance, and latent samples](numerical-practice.md#n2-5).
- **Self-check:** does the decoder receive the concatenation of mean and variance? **In this standard VAE, it receives the sampled `k`-dimensional code.**

### 2.8 VAE objective, prior, and reconstruction–regularization balance

**Slides:** pp. 29–35, 46–54.

The loss combines reconstruction error with `KL(qφ(z|x) ‖ p(z))`. The usual prior is `N(0,I)`. Reconstruction keeps input-specific information; KL discourages arbitrary isolated codes with unsuitable means and variances. Optimizing only reconstruction can leave gaps; optimizing only KL can make different inputs share the same uninformative distribution. Merely adding a sampling layer is not enough.

- **Short — intuition/derivation:** [MIT: prior and regularization, 23:25–32:31](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1405s) — **9:06 excerpt**; includes the continuity/completeness motivation.
- **Short — numerical illustration:** [Serrano: VAE loss, 27:11–30:30](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1631s) — **3:19 excerpt**, including probability-bar KL arithmetic. **Creator correction:** the middle red probability at 30:05 is **0.4**, not 0.3. This is a discrete illustration, not the Gaussian closed-form calculation.
- **Calculate:** [N2.6: pixel-MSE plus summed latent KL, then a batch mean](numerical-practice.md#n2-6). It includes a full worked case and fresh retry; the later Bernoulli/ELBO example is optional likelihood context.
- **Optional mathematical bridge:** when reconstruction is a negative log-likelihood and its expectation is taken over the encoder distribution, minimizing reconstruction plus KL maximizes the **evidence lower bound (ELBO)**. A single sampled reconstruction estimates that expectation. This gives context for the reading on p. 71; it does not add a new claimed exam topic. [Original VAE paper](https://arxiv.org/abs/1312.6114).

### 2.9 Discrete KL divergence: direction and arithmetic

**Slides:** pp. 36–37.

`KL(P ‖ Q) = Σᵢ Pᵢ ln(Pᵢ/Qᵢ)`: the distribution on the **left** supplies the weights. Swapping the arguments changes both weights and ratios. Individual summands may be negative even though the total is nonnegative. Use natural logarithms for answers in nats; base-two logarithms give bits. KL is not a symmetric distance.

- **Short — worked probability example:** [Serrano: latent loss/KL, 29:40–30:30](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1780s) — **0:50 replay**, after §2.8. Apply the creator's `0.4` correction noted above.
- **Optional slower explanation:** [ritvikmath: The KL Divergence](https://www.youtube.com/watch?v=q0AkK8aYbLY) — **18:13**, develops the ratio, log, and weighting. This is explanatory math rather than a VAE parameter-update lesson.
- **Calculate:** [N2.4: reproduce the lecture's three-bin example in both directions](numerical-practice.md#n2-4), then a fresh two-bin problem.
- **Self-check:** if `Pᵢ > 0` but `Qᵢ = 0`, that term makes `KL(P ‖ Q)` infinite. Terms with `Pᵢ = 0` contribute zero by the limiting convention.

### 2.10 Gaussian KL: derive it and handle log-variance correctly

**Slides:** pp. 38–45; corrects p. 35.

For a diagonal Gaussian encoder and standard normal prior,

`KL = ½ Σⱼ (σⱼ² + μⱼ² − 1 − ln σⱼ²)`.

Derive one coordinate: subtract Gaussian log-densities, then use `E[(z−μ)²] = σ²` and `E[z²] = σ² + μ²`. Sum over independent coordinates. With encoder output `ℓ = ln σ²`, the same formula is `½ Σ(exp ℓ + μ² − 1 − ℓ)`. Sampling needs `exp(ℓ/2)`, not `exp ℓ`.

- **Video bridge — derivation/intuitive role:** revisit the [MIT prior chapter, 23:25–32:31](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1405s), **9:06**. It explains why the term is needed; it is **not** a complete worked Gaussian numerical derivation.
- **Required written derivation and arithmetic:** pp. 38–45 plus [N2.5](numerical-practice.md#n2-5) supply every expectation, a two-dimensional substitution, and checked answers. No fully verified short video covering that complete calculation was found in this review.
- **Self-check:** `μ = 0, log-variance = 0` means variance **one** and KL **zero**. The corrected positive formula gives KL `2` for `μ = 2, σ = 1`.

### 2.11 Reparameterization and gradients through the sample

**Slides:** pp. 55–60.

Draw `ε ~ N(0,I)` independently, then calculate `z = μ + σ ⊙ ε`. Randomness is carried by `ε`; the dependence on learned parameters is now explicit and differentiable for the sampled noise. In this backward pass, hold the noise value fixed. The useful local derivatives are `∂z/∂μ = 1`, `∂z/∂σ = ε`, and `∂z/∂ℓ = ½σε` for log-variance `ℓ`.

- **Short — derivation:** [MIT: reparameterization, 32:31–34:36](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=1951s) — **2:05 excerpt**.
- **Calculate:** [N2.7: sampled reconstruction gradients plus KL gradients and a simultaneous update](numerical-practice.md#n2-7).
- **Self-check:** `ε = 0` gives zero reconstruction-path derivative with respect to `σ` on that sample; the **KL gradient may still be nonzero**. This does not stop all variance learning.

### 2.12 Continuity, completeness, interpolation, and latent perturbation

**Slides:** pp. 46–54, 61–64.

Continuity means nearby codes decode similarly. Completeness is the desired property that likely latent samples decode into meaningful examples. The normal prior encourages these properties; it does not guarantee perfect images at every point in all of latent space.

For interpolation, form `z(α) = (1−α)zA + αzB`, with `0 ≤ α ≤ 1`, and decode each point. For a coordinate traversal, vary one coordinate and hold the others fixed. A diagonal Gaussian makes coordinates independent within that specified Gaussian; it does **not** guarantee that learned coordinates correspond to independent semantic attributes. Smooth-looking interpolations are a useful diagnostic, not proof of globally correct generation.

- **Short — visualization:** [MIT: latent perturbation and disentanglement, 34:36–37:40](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=2076s) — **3:04 excerpt**.
- **Use with slides:** p. 54 compares AE/VAE interpolation; p. 63 defines the two-endpoint experiment. The video focuses on coordinate changes; distinguish these experiments.
- **Calculate:** [N2.8: interpolation coordinates, decoded outputs, and a separate traversal](numerical-practice.md#n2-8).
- **Self-check:** an intermediate **latent code** is a weighted average, but a nonlinear decoder's output need not equal the same weighted average of endpoint images.

### 2.13 Debiasing and generating new examples

**Slides:** pp. 62, 65–70.

Latent representations can reveal underrepresented patterns and guide resampling or data collection. This can help with dataset imbalance, but a VAE alone does not establish fairness; evaluate the resulting model and relevant groups. For unconditional generation, sample `z` from the prior and run the decoder. For reconstruction, encode a particular `x` and sample from its encoder distribution; these are different uses.

- **Short — application:** [MIT: debiasing with VAEs, 37:40–39:37](https://www.youtube.com/watch?v=Dmm4UG-6jxA&t=2260s) — **1:57 excerpt**.
- **Short recap — intuition:** [Two Minute Papers: What is an Autoencoder?](https://www.youtube.com/watch?v=Rdpbnd0pCiI) — **3:49**, AE-to-VAE motivation and generation.
- **Self-check:** why is an encoder unnecessary when producing a fresh unconditional sample? **You already obtain `z` from the prior; the decoder converts it into an observation.**

### Optional longer route for Lecture 2

Choose one coherent lecture before replaying its short topic sections:

| Resource | Full runtime | Best use |
|---|---:|---|
| [Luis Serrano — Denoising and Variational Autoencoders](https://www.youtube.com/watch?v=SSXDkfiPs7c) | 31:46 | Small-image intuition, denoising, generation, and loss examples. Apply the documented 30:05 probability correction. |
| [MIT 6.S191 2024 — Deep Generative Modeling](https://www.youtube.com/watch?v=Dmm4UG-6jxA) | 56:18 | Course-aligned explanation; AE/VAE material runs 8:16–39:37. Later sections introduce GANs and diffusion. |
| [ritvikmath — The KL Divergence](https://www.youtube.com/watch?v=q0AkK8aYbLY) | 18:13 | A slower explanation of why KL uses a probability ratio, logarithm, and weighted average. |

**Exit standard:** draw both architectures; choose the correct training target for each application; calculate AE reconstruction error, both KL directions, Gaussian KL, a reparameterized sample and its gradients; distinguish prior sampling, reconstruction, interpolation, and a coordinate traversal. Use [N2.1–N2.8](numerical-practice.md#n2-1) to check these skills.

<a id="lecture-3"></a>

## GANs Part 1 — Learning through a generator–discriminator game

**Source:** [Lecture GANs Part 1.pdf](Lecture%20GANs%20Part%201.pdf), 70 PDF pages. Page numbers below refer to the PDF viewer, including the title page. Pages 10–27 are a visual sequence, not missing lectures.

**Two routes:** use the short explanations to understand the mechanism, then do [N3.1–N3.6](numerical-practice.md#n3-1) with a calculator and paper. The numerical route includes actual video arithmetic and fully checked written updates. Watching a loss derivation alone does not demonstrate that you can calculate a training step.

### 3.1 Why generate samples? Real and model distributions

**Slides:** pp. 3–4, 8.

Understand:

- A generative model should reproduce the structure and variety of a data distribution. One convincing image is weaker evidence than many convincing, varied samples.
- Start with a simple noise distribution, sample a latent vector `z`, and transform it with `G(z)`. Standard GAN generation provides samples without requiring an explicit, tractable probability density for each image.
- “Learn the distribution” means matching patterns across possible samples; it does not mean copying a selected training image.

**Short first — intuition:** [IBM Technology: What are GANs?](https://www.youtube.com/watch?v=TpMIssRdhco), **8:22**. A clear lightboard introduction to the two roles and the reason for their competition. This same video covers §3.2; watch it once.

**Optional depth:** [Stanford CS231n, Lecture 13: Generative Models](https://www.youtube.com/watch?v=5WoItGTWV54), **1:17:41**. Places GAN sampling alongside autoregressive models and VAEs; a broad lecture, not a short required watch.

**Check:** If a generator always produces the same excellent-looking face, has it learned the whole distribution? **Answer:** no; it may have learned one narrow mode while missing the others.

### 3.2 Generator, discriminator, and the evolving game

**Slides:** pp. 5–7, 9–27.

Understand:

- `G` maps noise to a fake example; `D(x)` estimates how likely an input is to be real. The target labels in this lecture are **real = 1, fake = 0** during discriminator training.
- Read the animation as alternating changes: first the discriminator learns to separate current real/fake samples; then the generator moves its outputs toward regions the current discriminator accepts.
- At the ideal distribution-matching equilibrium with balanced real/fake sampling, an optimal discriminator outputs `1/2` on the shared distribution. A poorly trained discriminator also can output `1/2`; that score alone does not prove successful generation.

**Short first — concrete forward calculations:** [Luis Serrano: A Friendly Introduction to GANs](https://www.youtube.com/watch?v=8L11aMN5KY8&t=250s), **4:10–9:10 · 5:00 excerpt**, full video **21:00**. Builds a tiny discriminator and generator for 2×2 images; includes explicit sigmoid outputs rather than only a block diagram. Replay the IBM introduction if the two roles are still unclear.

**Numerical preparation:** [N3.1: real/fake loss arithmetic](numerical-practice.md#n3-1); then [N3.3: a complete alternating update](numerical-practice.md#n3-3).

**Check:** Who receives a training image as an input, and who receives `z`? **Answer:** `D` receives real or generated images; `G` receives noise. In the standard unconditional GAN here, `G` does not receive a particular real image to reconstruct.

### 3.3 Frozen weights still allow a gradient to pass through

**Slides:** pp. 28–29.

| Step | Data and targets | Parameters changed | Required backward path |
|---|---|---|---|
| Train `D` | Real examples → 1; generated examples → 0 | Discriminator only | Loss → `D`; treat generated examples as fixed inputs |
| Train `G` with non-saturating loss | Generated examples should receive a high real probability from `D` | Generator only | Loss → through `D` → generated example → `G` |

Freezing `D`'s parameters in the second step does **not** mean detaching `D(G(z))` from the computation graph. We still need the derivative of `D` with respect to its **input**. Conversely, in the `D` step, detaching the generated examples is a useful implementation of the stop shown on p. 28. [Google's training explanation](https://developers.google.com/machine-learning/gan/training) provides a second description of these two phases.

**Short first — gradient-path explanation:** [Serrano, training the two networks](https://www.youtube.com/watch?v=8L11aMN5KY8&t=800s), **13:20–18:10 · 4:50 excerpt**. Follow the highlighted backward paths. The video illustrates the mechanism; the complete checked parameter arithmetic is [N3.3](numerical-practice.md#n3-3).

**Check:** If `D` is frozen in the generator phase and the gradient is stopped at its input, can `G` learn? **Answer:** no. “Do not update D” and “do not differentiate through D” are different operations.

### 3.4 Loss signs, batch averages, and non-saturating gradients

**Slides:** pp. 30–41; revisited on p. 47.

Use natural logarithms. Let `r_i = D(x_i)` for real examples and `q_i = D(G(z_i))` for generated examples. The lecture uses the **sum of two batch means**:

`L_D = -mean_real ln(r_i) - mean_fake ln(1-q_i)` — minimize with respect to `D`.

`L_G,minimax = mean_fake ln(1-q_i)` — minimize with respect to `G`.

`L_G,NS = -mean_fake ln(q_i)` — the non-saturating generator loss, also minimized.

For equal real/fake batch sizes, a single BCE mean over their concatenation is half the lecture's `L_D`; its gradients also are halved. Write the averaging convention before calculating.

**Short first — actual numerical loss examples:** [Serrano, log loss with numbers](https://www.youtube.com/watch?v=8L11aMN5KY8&t=580s), **9:40–11:30 · 1:50 excerpt**, full video **21:00**. Works through real/fake targets with probabilities such as `0.1` and `0.9` and logarithmic penalties. For the loss curves and surrounding explanation, continue to **12:30**. This is a worked arithmetic video; it does not supply the entire batch update required by the companion.

**Short derivation bridge:** with discriminator logit `a` and `q=σ(a)`, reproduce pp. 35–36:

`d ln(1-q)/da = -q`, while `d[-ln(q)]/da = q-1`.

At `q=0.01`, these are `-0.01` and `-0.99`. The relevant derivative is with respect to the **logit**, then through the remaining chain to generator parameters. A derivative with respect to `q` alone misses the sigmoid factor. The non-saturating loss improves this output-gradient signal; it cannot guarantee every upstream derivative is nonzero or prevent mode collapse.

**Slide-reading cautions:** p. 30 writes `J_G=-J_D` while dropping the real-data term. That equality is only **up to a term constant with respect to G**. The arrows on p. 41 express the desire to raise fake-sample scores; minimax and non-saturating losses have different gradients and training trajectories. For a fixed discriminator both favor higher fake-sample scores; the desired joint equilibrium is distribution matching, not a discriminator that permanently says 1 to every fake. [Google's loss discussion](https://developers.google.com/machine-learning/gan/loss) also distinguishes the original and modified objectives.

**Numerical preparation:** [N3.1: losses and averaging](numerical-practice.md#n3-1), [N3.2: derive and compare gradients](numerical-practice.md#n3-2), [N3.3: update actual parameters](numerical-practice.md#n3-3).

**Check:** Can a small minimax generator loss near zero mean poor progress? **Answer:** yes; when `q≈0`, `ln(1-q)≈0` and its logit gradient is near zero. Do not interpret raw GAN losses as image-quality scores.

### 3.5 The alternating minibatch algorithm and update ratio

**Slides:** pp. 42–44.

Read the loop in this order:

1. For each of `k` discriminator steps, sample real data and noise, generate fixed fakes, and update `D`.
2. Sample noise for the generator step, compute its loss through the current discriminator, and update `G`.
3. Repeat. The networks are trained together over time; their parameters are not necessarily updated by one undifferentiated backward pass.

The displayed algorithm **ascends** `mean ln D(real)+mean ln(1-D(fake))` for `D` and **ascends** `mean ln D(fake)` for the improved `G` objective. These are equivalent to descending the negative losses above. It uses the improved generator objective, even though the original minimax game appears earlier. The slide says there is no universally best `k`; do not memorize “always train D to completion.”

**Short first:** use [Serrano's alternating-training excerpt](https://www.youtube.com/watch?v=8L11aMN5KY8&t=800s), **13:20–18:10 · 4:50** from §3.3. **Optional implementation depth:** [Aladdin Persson: DCGAN implementation from scratch](https://www.youtube.com/watch?v=IZtv9s_Wx9I), **35:37**, particularly the creator's training chapter beginning **19:09**.

**Numerical preparation:** [N3.3](numerical-practice.md#n3-3) states which parameter values each phase must use and shows both phases completely.

**Check:** In 200 outer iterations with `k=3`, how many optimizer steps occur? **Answer:** 600 for `D`, 200 for `G`; the number of examples processed additionally depends on batch size.

### 3.6 DCGAN: turning a latent vector into an image

**Slides:** p. 45.

Follow the shapes, not just the network names:

- Generator: `100 → 4×4×1024 → 8×8×512 → 16×16×256 → 32×32×128 → 64×64×3`.
- Discriminator: `64×64×3 → 32×32×64 → 16×16×128 → 8×8×256 → 4×4×512 → 1`.
- Projection/reshape creates the initial spatial feature map. Convolution-like upsampling grows its width and height; the discriminator reduces them to a real/fake score.
- The slide's “deconv” labels mean learned upsampling/transposed convolution in this context, not an exact mathematical inverse of every earlier convolution.

**Short first — architecture:** [Aladdin Persson, DCGAN paper recap](https://www.youtube.com/watch?v=IZtv9s_Wx9I&t=26s), **0:26–4:31 · 4:05 excerpt**. These boundaries are the creator's chapter times. **Optional depth:** the full **35:37** implementation, with discriminator at **4:31** and generator at **9:38**. Its implementation choices are examples; the shapes above are your slide's diagram.

**Numerical preparation:** [N3.5: shapes and parameter counts](numerical-practice.md#n3-5). Stride/padding calculations there explicitly state extra assumptions that p. 45 does not specify.

**Check:** Are `100` input noise values a 100-class target? **Answer:** no; they are latent coordinates. The three final channels represent RGB in this example.

### 3.7 Mode collapse and minibatch discrimination

**Slides:** pp. 46, 48–53.

Understand:

- **Mode collapse:** many noise inputs produce the same or a few kinds of output. A generated sample may look plausible while the batch lacks diversity.
- The mixture-of-Gaussians pictures illustrate missing regions of the target distribution, including generators that move between modes without covering them together.
- Minibatch discrimination adds features that compare examples within a batch, giving the discriminator evidence about repetition. It does not necessarily add a separate diversity penalty to the generator's loss.
- In the pairwise similarity example, `exp(-L1 distance)` is high for similar features. A high similarity sum signals repetition; “high diversity score” and “high similarity score” must not be confused.
- The original learned pairwise feature construction and a simpler minibatch standard-deviation feature are related ways to expose batch information, not identical algorithms. The slide groups them for intuition.

**Short first — specialist explanation:** [FAU / Andreas Maier, mode collapse and minibatch discrimination](https://www.youtube.com/watch?v=4Ot22wkEdfU&t=450s), **7:30–9:40 · 2:10 excerpt**, full lecture **20:10**. The selected part shows collapse and the batch-aware remedy; later unrolled-GAN material is optional. This is a university explanation with a small audience, selected for its exact topic match rather than a claim of broad popularity. [The university's accompanying notes](https://lme.tf.fau.de/lecture-notes/lecture-notes-dl/lecture-notes-in-deep-learning-unsupervised-learning-part-4-2/) support the mechanism.

**Numerical preparation:** [N3.4: compute pairwise similarities](numerical-practice.md#n3-4). The video is conceptual; the companion supplies the checked arithmetic and a changed-value problem.

**Check:** Does minibatch discrimination guarantee that collapse disappears? **Answer:** no. It can make collapsed batches easier to detect, but training can still fail. Read “kills mode collapse” on p. 51 as the intended mechanism, not a theorem.

### 3.8 Oscillation, uninformative losses, and sensitivity

**Slides:** pp. 46–47, 54–56.

Understand each failure separately:

| Symptom | Reason to investigate | Slide-aligned response |
|---|---|---|
| Poor generator with very weak minimax gradient | `D(G(z))` close to zero | Compare non-saturating gradients (§3.4) |
| Repeated output types | Low diversity / mode collapse | Inspect batches and use batch diversity information (§3.7) |
| Oscillating losses | Both players change the other's task; updates may be too aggressive | Check learning rates, schedules, update balance, and normalization |
| Apparently improving loss but disappointing images | Loss depends on the current opponent | Inspect fixed-noise sample grids and evaluation metrics too |
| Large changes after small configuration changes | Learning rate, batch size, depth, or activation sensitivity | Change settings in controlled experiments and record them |

TTUR means **different learning rates for the two players**. The slide suggests a lower generator rate as a possible configuration; it is not a universal numerical ratio. Batch normalization and learning-rate changes are possible aids, not guaranteed convergence proofs. Likewise, oscillation alone does not diagnose one unique bug. [Google's common-problems guide](https://developers.google.com/machine-learning/gan/problems) treats these as continuing practical challenges.

**Short first:** [FAU, training heuristics](https://www.youtube.com/watch?v=4Ot22wkEdfU&t=210s), **3:30–5:40 · 2:10 excerpt**. Use the slide table above to distinguish which symptom a proposed remedy addresses. For vanishing gradients, replay [Serrano's loss explanation](https://www.youtube.com/watch?v=8L11aMN5KY8&t=580s), **9:40–12:30 · 2:50**, and do [N3.2](numerical-practice.md#n3-2).

**Check:** If generator loss falls sharply, is output diversity necessarily improving? **Answer:** no; the discriminator may have weakened or the generator may be exploiting a narrow mode. Compare outputs and distribution-level evidence.

### 3.9 Generated samples, nearest neighbors, and latent arithmetic

**Slides:** pp. 57–65.

Understand:

- The highlighted nearest training neighbors on pp. 57–58 help inspect copying; they are not a complete memorization test or a calibrated quality metric.
- Interpolation changes the latent input between two endpoints: `z(t)=(1-t)z_A+t z_B`. Generate each intermediate image as `G(z(t))`; this is not generally the same as blending the endpoint image pixels.
- Attribute arithmetic uses differences of representative/average latent codes, for example “smiling woman − neutral woman + neutral man.” It illustrates learned directions; the semantic edit is an empirical observation, not a guaranteed rule for every latent vector or model.

**Short first — matching visual demonstration:** [FAU, latent vector arithmetic](https://www.youtube.com/watch?v=4Ot22wkEdfU&t=380s), **6:20–7:40 · 1:20 excerpt**. Shows the DCGAN-style attribute examples used in these slides. The [DCGAN authors' paper](https://arxiv.org/abs/1511.06434) is the optional primary reading for interpolation and arithmetic experiments.

**Numerical preparation:** [N3.6: interpolate and edit vectors](numerical-practice.md#n3-6). Arithmetic on tiny vectors practices the operation; it does not claim those invented vectors generate real attributes.

**Check:** Does `G((z_A+z_B)/2)` have to equal `(G(z_A)+G(z_B))/2`? **Answer:** no; the generator is generally nonlinear.

### 3.10 Style mixing and progress in sample quality

**Slides:** pp. 66, 69.

Understand the displayed evidence: style-based generation can combine characteristics at different scales; the historical montage illustrates improvements in visual sample quality. It does not prove universal fidelity, diversity, or safety. The deck shows results here rather than deriving the full StyleGAN architecture.

**Short first — original authors' demonstration:** [Tero Karras / NVIDIA: A Style-Based Generator Architecture for GANs](https://www.youtube.com/watch?v=kSLJriaOumA), **6:17**. Shows controlled changes in generated appearance. The original video is linked by [NVIDIA's version index](https://nvlabs.github.io/stylegan2/versions.html). Treat this as a result/intuition video, not an arithmetic tutorial.

**Optional depth:** [the authors' StyleGAN paper and research page](https://research.nvidia.com/publication/2019-06_style-based-generator-architecture-generative-adversarial-networks). Detailed adaptive normalization, regularization, or later StyleGAN versions go beyond this deck's result slides.

**Check:** Is an attractive results grid enough to establish coverage of the training distribution? **Answer:** no; sample selection can hide failures and omitted modes.

### 3.11 Conditional generation, domain transfer, and stacked GAN results

**Slides:** outline p. 2; examples pp. 67–68.

Recognize the examples at the level presented:

- Conditional generation supplies information such as a label, source image, or text description to control output.
- Pix2pix illustrates paired image-to-image translation; CycleGAN illustrates learning translation from unpaired domain collections.
- Text-to-image examples and StackGAN/StackGAN++ show staged or multi-scale generation. Page 68 specifically attributes its grid to **StackGAN++**.
- LSGAN and BEGAN are named as examples of alternative GAN developments; their losses are not derived in this Part 1 deck.

**Short first — applications:** [Two Minute Papers: pix2pix](https://www.youtube.com/watch?v=u7kQ5lNfUfg), **4:27**, explicitly recommended on the [pix2pix authors' project page](https://phillipi.github.io/pix2pix/); and [CycleGAN authors' ICCV spotlight](https://www.youtube.com/watch?v=AxrKVfjSBiA), **3:31**, linked from their [project page](https://junyanz.github.io/CycleGAN/). These explain/show tasks and training-data distinctions; they are not numerical loss walkthroughs.

**Optional longer result demonstration:** [StackGAN authors' birds generated from text](https://www.youtube.com/watch?v=93yaf_kE0Fg), **19:17**, linked from their [repository](https://github.com/hanzhanggit/StackGAN). This is **StackGAN**, a predecessor/context for the deck's StackGAN++ examples. The newly supplied [Part 2 section](#lecture-4) now develops the two-stage StackGAN architecture and conditioning augmentation.

**Check:** Does using unpaired domain collections mean CycleGAN needs no training data? **Answer:** no; it needs examples from both domains, just not a matched target for each source image.

### 3.12 Evaluation resources and what Part 1 actually establishes

**Slides:** p. 70; motivation for evaluation also pp. 46, 57–58.

The final slide points to the original GAN paper, the Inception Score paper, and the FID/TTUR paper. It does not work through metric equations. The newly supplied [Part 2 section](#lecture-4) now develops IS, FID and generative precision/recall. Use the [assignment's IS/FID section](#assignment-metrics) for its distinct classifier and sample protocol.

**Short first:** [FAU / Andreas Maier: Unsupervised Learning, Part 3](https://www.youtube.com/watch?v=fXO1fOXnOTI), **13:19**, includes evaluation concepts; follow the focused route in the assignment section to avoid repeating it. It is a specialist university lecture, not a verified high-reception numerical walkthrough.

**Ready to move on when:** you can explain the two backward paths, state all three loss signs, calculate one complete alternating update, distinguish weak gradients from collapse, and interpret sample grids without treating discriminator loss as a quality score. The companion contains fresh questions; use those before consulting solutions.

<a id="lecture-4"></a>
## GANs Part 2 — Conditional generation and evaluating samples

**Source:** [Lecture GANs Part 2](Lecture%20GANs%20Part%202.pdf), 97 pages. Page 1 is the title and page 97 the references. The numerical routes below reproduce the lecture's examples and correct its arithmetic or interpretation where necessary.

### 4.1 Conditional GANs: the discriminator judges a matching pair

**Source:** pp. 2–3, 16.

Condition `y` can encode a class, attributes, an image, or text. Both networks receive it: `G(z,y)` makes a sample and `D(x,y)` judges the sample together with its condition. The conditional minimax objective is

`E_(x,y) ln D(x,y) + E_(z,y) ln[1−D(G(z,y),y)]`.

D maximizes this expression; G minimizes its generated term. Keep `y` in **both** discriminator calls. Mismatched real image/text pairs can be added as negatives, but this is an extra training choice, not a third term already present in that two-term equation. For practical non-saturating G training use `−E ln D(G(z,y),y)`; reuse [Part 1's gradient reasoning](numerical-practice.md#n3-2).

**First watch — implementation intuition:** [Aladdin Persson, conditional G/D modifications, 0:56–6:58](https://www.youtube.com/watch?v=Hp-jWm2SzR8&t=56s), **6:02 excerpt**. It shows how to feed labels into both networks. The surrounding implementation uses WGAN-GP; its critic loss and gradient penalty differ from this lecture's vanilla conditional GAN objective.

**Optional depth:** the same tutorial, **12:21** full, for conditional WGAN-GP implementation; compare rather than silently swap objectives. The [original conditional GAN paper](https://arxiv.org/abs/1411.1784) supplies the vanilla formulation.

**Numerical preparation:** [N5.1](numerical-practice.md#n5-1) checks concatenation, parameter counts, conditional losses, and a generator logit gradient. **Self-check:** hold `z` fixed and vary `y`; then hold `y` fixed and vary `z`. What would each test reveal about ignored conditions or lost diversity? Neither test alone proves distribution matching.

### 4.2 The tabular conditional GAN: one-hot fields and all network shapes

**Source:** pp. 4–15, including the image-only architecture builds.

The example uses **20 noise values**, **11 condition values**, and a **20-value generated sample**. The condition contains three categorical fields: 2 academic-performance values, 7 course values, and 2 semester values. Each block is one-hot, so the complete vector has three ones. It is not one 11-class one-hot label. There are `2×7×2=28` possible combinations if every combination is permitted, while the encoding still has length 11.

- G: concatenate `[z,y]` to length 31, then `31 → 256 → 256 → 20`.
- D: concatenate `[real sample,y]` **or** `[generated sample,y]` to length 31, then `31 → 256 → 256 → 1`.
- The slide's plus sign means **concatenation**, not elementwise addition. Do not concatenate both real and fake samples into one D input. The masked-vector illustration does not specify a complete imputation algorithm.

**First watch:** reuse the **6:02 conditioning excerpt** in §4.1. Its image/embedding implementation differs from these tabular dimensions; the bullet points above supply the course-specific bridge. **Optional depth:** its **12:21** full implementation. **Calculate:** [N5.1](numerical-practice.md#n5-1), including every bias. **Self-check:** why does adding another category to one field change the input dimension by one rather than multiplying it by the number of other fields?

### 4.3 StackGAN: text, two resolutions, and conditioning augmentation

**Source:** pp. 17–21; text-conditioning motivation p. 16.

Stage I uses a text embedding `φ(t)` and noise `z` to produce a **64×64** sketch of shape and color. Stage II takes that sketch and the text again, encodes the image, combines spatially repeated text features, and uses residual/upsampling blocks to produce **256×256** details. Each stage has its own conditional discriminator. Inspect the bird grid on p. 20 for what improves and what remains wrong.

**Conditioning augmentation (CA):** predict `μ` and positive standard deviations `σ` from text, then sample `ĉ=μ+σ⊙ε`, with `ε~N(0,I)`. This introduces nearby variations in text conditioning. The `σ` here is a standard deviation, not variance. Page 18's “all randomness” wording is too broad: Stage II has no separate fresh `z`, but the p. 21 diagram and [original StackGAN paper](https://arxiv.org/abs/1612.03242) include CA sampling at Stage II too. Fixing the Stage I image does not force Stage II to be deterministic when CA noise is resampled.

**First watch — conceptual architecture:** [Connor Shorten / Henry AI Labs — StackGAN](https://www.youtube.com/watch?v=s7OIHukdD0o), **4:34**, specifically introduces the two scales and CA. This is a specialist creator explanation with a small audience, not a verified worked-number lesson.

**Optional depth:** read the authors' architecture and CA equations in the paper; [the authors' bird demonstration](https://www.youtube.com/watch?v=93yaf_kE0Fg), **19:17**, compares real, Stage I and Stage II outputs across text prompts. The latter is a **results demonstration**, not a derivation video. **Calculate:** [N5.2](numerical-practice.md#n5-2) works CA, derivatives with fixed noise, and the pixel-count increase. **Self-check:** why can two images with the same text differ while still satisfying that text?

### 4.4 GAN versus VAE, and what “good generation” means

**Source:** pp. 22–23, 55–59, 81–82.

Compare fidelity (plausible samples), coverage/diversity (representing the real variation), training behavior, and ability to infer a latent representation. The lecture's sharper GAN versus smoother VAE contrast is a typical outcome of particular architectures/objectives, not a universal ranking. Both models can have continuous latent spaces. A VAE provides an evidence lower bound and ways to estimate likelihood; that does not make exact likelihood automatically tractable.

**First watch — evaluation intuition:** [FAU / Andreas Maier, evaluation and IS, 9:30–11:40](https://www.youtube.com/watch?v=fXO1fOXnOTI&t=570s), **2:10 excerpt**. Then compare to the earlier [AE/VAE video routes](#lecture-2). **Optional depth:** the same FAU lecture, **13:19** full, for GAN context, IS and FID; the [university transcript](https://lme.tf.fau.de/lecture-notes/lecture-notes-dl/lecture-notes-in-deep-learning-unsupervised-learning-part-3/) supports the metric discussion.

Scores supplement image inspection. They do not prove generalization: copying a reference set can give FID zero against that set. In particular, p. 23's suggestion that FID necessarily punishes memorization is incorrect. Compare held-out data and nearest training examples as additional evidence, while keeping the assignment's required reference protocol. **Calculate:** the counterexamples in [N5.4](numerical-practice.md#n5-4) and [N5.5](numerical-practice.md#n5-5). **Self-check:** can realistic samples and poor coverage occur together?

### 4.5 Entropy, confidence, and the marginal class distribution

**Source:** pp. 24–31, 33–37.

Feed each generated image to a **fixed pretrained classifier**. Standard IS uses its 1,000 ImageNet class probabilities `p(y|x)`. Low per-image entropy indicates classifier confidence; high entropy of the average prediction indicates class diversity. The marginal is the **mean probability vector**, `p(y)=(1/N)Σᵢp(y|xᵢ)`, not a histogram of argmax labels. `H(P)=−Σ_c P_c ln P_c`, with zero terms interpreted by their limit.

**First watch — worked-number prerequisite:** [StatQuest, entropy calculations, 9:35–15:50](https://www.youtube.com/watch?v=YtebGVx-Fxw&t=575s), **6:15 excerpt**. Visible coin/chicken probability calculations connect weighted surprise to entropy. StatQuest uses base-two logs (bits); use **natural logs (nats)** in this course's IS formula, or consistently use `2^I` for mutual information in bits. Do not insert bit entropy into `exp`.

**Optional depth:** [the full entropy lesson](https://www.youtube.com/watch?v=YtebGVx-Fxw), **16:34**; [ritvikmath's KL explanation](https://www.youtube.com/watch?v=q0AkK8aYbLY), **18:13**, revisits probability ratios and asymmetric weighting. **Calculate:** [N5.3](numerical-practice.md#n5-3). **Self-check:** a uniform classifier output on every image has a diverse marginal; why does that not imply a high IS?

### 4.6 Derive and calculate Inception Score

**Source:** pp. 32–53: KL/entropy/MI derivation, limiting examples, computation and the four-image example.

`IS=exp[(1/N)Σᵢ KL(p(y|xᵢ) || p(y))] = exp[H(Y)−H(Y|X)] = exp[I(X;Y)]`.

The subtraction rewards confident individual predictions and varied average predictions together. `X` indexes the sampled image and `Y` the classifier label. For `K` classes, `1≤IS≤K`; it is not a percentage. `IS=1` can arise from uncertain identical predictions **or** perfectly confident predictions of the same class. It is not by itself a verdict that images are bad, especially on a genuinely single-class dataset.

**First watch — conceptual metric:** reuse [FAU's 9:30–11:40 excerpt](https://www.youtube.com/watch?v=fXO1fOXnOTI&t=570s), **2:10**. For actual probability arithmetic first use §4.5's **6:15 worked entropy excerpt** and [Serrano's 29:40–30:30 discrete-KL replay](https://www.youtube.com/watch?v=SSXDkfiPs7c&t=1780s), **0:50**; apply the `0.4` correction already explained in §2.8. Neither is claimed to calculate the lecture's four-image IS.

**Numerical preparation:** [N5.3](numerical-practice.md#n5-3) derives the identity and works **all four KL rows**, the marginal, mean and exponential: **IS≈1.674**. The p. 48 explanation overstates why row four has the largest KL: its confidence `.85` is below row one's `.90`, and class three's marginal `.275` is above class two's `.2625`. Use the complete weighted log-ratio, not either ranking alone. **Optional depth:** full FAU **13:19** plus the [original improved-GAN-training paper](https://arxiv.org/abs/1606.03498), which introduced IS.

### 4.7 IS splits, uncertainty and failure cases

**Source:** pp. 38–43, 54–57; misleading single-class claims on pp. 59, 69.

Compute each split's **own marginal and IS**, then report mean and standard deviation, specifying the number of images, splits and standard-deviation convention. The lecture illustrates 50,000 images in five splits of 10,000; this is not the starter notebook's protocol. Preserve [the assignment's documented 5,000-total/ten-split interpretation and ambiguity](#assignment-metrics).

Identical confident cats/dogs give **IS=1**, correcting pp. 59 and 69. Repeating one convincing prototype per class can nevertheless give a high score because IS misses within-class duplication. Domain mismatch, classifier exploitation, and lack of a real-image reference are further limits. More samples or more splits do not fix those conceptual weaknesses.

**First watch:** §4.6's **2:10 IS excerpt**, then do [N5.4](numerical-practice.md#n5-4), which shows a split-order effect and repeated-prototype failure. **Optional depth:** full FAU **13:19** and [A Note on the Inception Score](https://arxiv.org/abs/1801.01973). **Self-check:** is the mean of exponentiated split scores equal to the score computed once on the whole dataset? Give a counterexample.

### 4.8 FID: distributions of features, means and covariance

**Source:** pp. 58–69, 80–82.

Standard FID embeds both real and generated images into fixed Inception-v3 pool features (2,048 dimensions), estimates a Gaussian for each feature set, then computes

`FID=||μr−μg||² + Tr(Σr+Σg−2(ΣrΣg)^(1/2))`.

`μ` is a mean feature vector, `Σ` a covariance matrix, and `Tr` the sum of diagonal entries. This compares **distributions of features**, not matched image pairs or softmax labels. Lower is better **under the same protocol**; values 8, 25 and 75 have no universal quality meaning across datasets or feature extractors. Same feature mean does not imply same spread: the lecture's standard deviations 20 versus 2 produce a one-dimensional covariance penalty `(20−2)²=324`.

**First watch — conceptual formula:** [FAU, FID, 12:00–12:30](https://www.youtube.com/watch?v=fXO1fOXnOTI&t=720s), **0:30 formula-focused excerpt**. It is brief; use §4.4's preceding context or the **13:19 full lecture** if the features/Gaussian idea is new. It does not work a numerical matrix example.

**Numerical preparation:** [N5.5](numerical-practice.md#n5-5) explains each term, solves the source's diagonal example and gives a fresh non-isotropic retry. **Optional depth:** [DeepLearning.AI, Build Better GANs, Week 1](https://www.coursera.org/learn/build-better-generative-adversarial-networks-gans), **“Fréchet Inception Distance (FID)” — approximately 15 minutes**, with the preceding feature/embedding lessons if needed. These are the provider's rounded durations; Coursera may require sign-in/enrollment. The full Week 1 video sequence totals approximately **66 minutes**. The [original FID paper](https://arxiv.org/abs/1706.08500) gives the definition.

### 4.9 FID arithmetic, sample bias, KID and reporting

**Source:** pp. 70–82; toy Gaussian pictures pp. 62–65.

The worked example has `μr=(1,2)`, `μg=(2,3)`, `Σr=diag(2,2)` and `Σg=diag(3,3)`. The mean term is 2; the covariance term is `10−4√6`; **FID=12−4√6≈2.202041**. The square root is a **matrix** square root. Entrywise roots work here only because these covariance matrices are diagonal. The p. 62 pictures supply no full feature data from which to independently reproduce their displayed scores.

Estimated FID depends on sample count and has finite-sample bias. A larger measured score at a smaller sample count is a tendency/estimator issue, not a guarantee for every random subsample. KID is mentioned as an alternative with an unbiased estimator of its squared kernel discrepancy; it is not numerically the same metric and does not replace required assignment FID. FID zero means matching first and second moments of the chosen features, not necessarily identical distributions or freedom from memorization. See [the KID paper](https://arxiv.org/abs/1801.01401) and [finite-sample FID analysis](https://arxiv.org/abs/1911.07023).

**First watch:** reuse §4.8's FID excerpt, then **calculate** [N5.5](numerical-practice.md#n5-5). No matching open worked-number FID video was verified; the written example provides the exact course calculation. **Optional depth:** the approximately **15-minute** DeepLearning.AI FID lesson above. Report feature network/checkpoint, real reference, transforms, sample counts, covariance convention, scores and grids. The assignment uses **128-dimensional features from its own six-digit classifier**, not standard Inception-v3; [assignment E](#assignment-metrics) explains the consequences.

### 4.10 Improved generative precision and recall: quality and coverage separately

**Source:** pp. 83–85, 95–96.

These are generative **feature-support** metrics, not a classification confusion matrix. Precision estimates the fraction of generated feature points inside the estimated real support; recall estimates the fraction of real points inside the estimated generated support. A scalar FID can hide different quality/coverage tradeoffs. High precision with low recall suggests plausible but restricted output; low precision with higher recall suggests broader but partly implausible output. These diagnoses are evidence, not unique proofs of a particular training bug.

**First watch — conceptual:** [DeepLearning.AI, Build Better GANs, Week 1: “Precision and Recall”](https://www.coursera.org/learn/build-better-generative-adversarial-networks-gans), **approximately 6 minutes** (provider-listed duration; navigate to that named lesson). Sign-in/enrollment may be required. This supplies the fidelity/coverage framing, not a verified hand-calculation of this deck's five-point example. A freely accessible, exact numerical video for the 2019 ball estimator was not verified; use the source diagram and [N5.6](numerical-practice.md#n5-6) for that calculation.

**Optional depth:** the same course's approximately **66-minute Week 1 video sequence**, then the [original 2019 paper](https://arxiv.org/abs/1904.06991) and [authors' implementation](https://github.com/kynkaat/improved-precision-and-recall-metric). Do not substitute the different 2018 precision–recall-distribution algorithm solely because it has a similar title.

### 4.11 The k-nearest-neighbor ball algorithm and the lecture's full example

**Source:** pp. 84–94.

1. Extract real and generated features in the **same** fixed feature space. The paper uses VGG16 features; the lecture's hand example is two-dimensional.
2. Within each set separately, put a ball around every point. Its radius is the distance to its `k`th nearest **other** point; exclude the point itself. The paper's example protocol uses `k=3`; the hand exercise uses `k=1`.
3. A query is covered if it lies inside **any** reference ball: some center `a` must satisfy `||query−a||≤radius(a)`. Each center has its own radius. Testing only the nearest center can give the wrong answer.
4. Precision averages the generated-in-real indicators; recall averages the real-in-generated indicators. Their denominators can differ if set sizes differ.

**First watch:** the approximately **6-minute conceptual lesson** in §4.10; then draw the circles while completing [N5.6](numerical-practice.md#n5-6). That worked calculation lists every radius, checks membership both ways, and demonstrates why the closest center alone is insufficient. The corrected source result remains **precision=.8, recall=.6**. On p. 88, `d(r3,r4)=√21.25≈4.610`, not 4.950. On p. 93, `g5` is closest to `r3` at `√5≈2.236`, not `r4` at 2.5; it is outside **all** real balls. Page 92's generated radii are consistent with `k=1`.

**Optional depth:** the 2019 paper's estimator definition and implementation linked above, plus the full Week 1 sequence. **Self-check:** build your own counterexample where a farther center has a wider ball and covers a query rejected by its nearest center.

### 4.12 Truncation, k, sample size and interpreting results

**Source:** pp. 95–96; references p. 97.

For fixed reference points, increasing `k` enlarges or preserves every radius, so estimated coverage cannot decrease. It changes the estimator's tolerance; an inflated score need not reflect better generation. Sample counts, feature representation and outliers also affect the estimated support. Fix these settings for model comparisons.

**First watch — sampling intuition:** [DeepLearning.AI, Week 1: “Sampling and Truncation”](https://www.coursera.org/learn/build-better-generative-adversarial-networks-gans), **approximately 7 minutes**, with the same access caveat as §4.10. Truncation concentrates sampling toward typical latent regions; it can trade diversity for fidelity. The original paper's model experiments show precision increasing and recall decreasing as truncation becomes stronger, but this is not a theorem about every generator. The normalization ablation is likewise model-specific.

**Numerical preparation:** [N5.6](numerical-practice.md#n5-6) interprets `.8/.6` without declaring that image quality has no problem: one of five generated points still fails the support test. **Optional depth:** the full Week 1 sequence and the authors' results table. **Self-check:** why is increasing `k` until both scores look good a change of measurement rather than a model improvement?


<a id="assignment-support"></a>

## Assignment 1 support

**Sources:** [Assignment 1.pdf](<Assignment 1.pdf>), all four pages, and [A1 starter.ipynb](<A1 starter.ipynb>), cells 0–29. This is a preparation and interpretation guide. Your trained models, CSV rows, figures and measured scores must come from your own runs.

### Read these source inconsistencies before starting

| Supplied material | Working interpretation and action |
|---|---|
| Title/starter say Assignment 1; PDF footers and submission filename say Assignment 2 / `A2_<roll>.ipynb`. | Keep the provided files intact; check the Classroom submission naming instruction before submitting. |
| Part A is worth 12 marks, but visible A1–A3 sum to 8; A3 references an absent A4. | Complete all visible A1–A3 requirements. The missing A4 measurement cannot be reconstructed from this file; obtain the missing specification from the instructor. |
| Held-out anomaly digit is assigned, and Part B says “both tasks”; only B1 denoising appears in either file. Deliverables mention A–F, but only A–E are present. | State the assigned held-out digit as requested; do not invent an anomaly experiment or Part F. Check whether a corrected handout adds them. |
| PDF asks for the generator's gradient norm; starter `grad_norm(G.fc)` measures only the first parameter tensor with a gradient. | Preserve the required hook and label it **first-layer weight gradient norm**. Also log the full-generator norm under a separate name if reporting the PDF's full norm. Use the same explicitly named norm for C1/C2 and the 1% comparison. |
| D1 says BatchNorm in both networks, but the supplied `D28` has none. `D28(spectral=True)` imports PyTorch's spectral normalization despite D2 saying implement the stabilizer yourself. | Adapt D1's discriminator to the stated recipe and describe BN placement. Implement the chosen D2 mechanism yourself; the convenience flag alone does not satisfy that requirement. |
| E3 says non-monotone noisy-image FID proves a bug. | Treat this as a diagnostic expectation, not a mathematical theorem. Audit any reversal, preserve the actual curve, and explain remaining sampling/feature effects rather than changing results to fit it. |

### A. AE versus VAE: reconstruction, interpolation and prior sampling

**Source:** PDF pp. 1–2; starter cells 10–15. Revisit the Lecture 2 AE/VAE videos first, then do [interpolation and shape practice](numerical-practice.md#n4-1).

- **Setup:** centre-crop CelebA to 148×148, resize to 64×64, use 30,000 images, latent width 64. Match architecture backbone, optimizer, batch size and epochs. The intended changes are the two VAE output heads, reparameterization and KL regularization. Keep a fixed train/validation split.
- **A1:** record final train and validation reconstruction MSE for both models and an eight-column originals/reconstructions grid (`figures/A1_recon.png`). State whether pixel losses are summed or averaged and how the batch is reduced; otherwise “MSE + KL” hides a change in relative weighting. The starter KL sums 64 latent coordinates and averages examples. Report reconstruction MSE separately from total VAE loss.
- **A2:** use encoded means, with eleven `t` values from 0 to 1 inclusive; do Smiling and your assigned second attribute. Save the first strip as `figures/A2_vae_interp.png` and give the second a distinct filename. Identify actual frames where appearance changes abruptly. A regularized latent space encourages useful interpolation; it does not guarantee every decoded point is a plausible face.
- **A3:** draw one set of sixteen `N(0,I)` vectors and feed that same set to both decoders; also show sixteen AE reconstructions from its own encoded codes. Save `figures/A3_prior_samples.png`. The plain AE objective does not force its aggregated codes to match `N(0,I)`; weak prior samples are evidence about that mismatch, not proof the decoder cannot reconstruct.
- **Interpret the run:** compare numerical reconstruction errors and actual images. The handout predicts blurrier VAE reconstructions/better VAE prior samples, but training failure or a different observed ordering must be reported honestly. A vanilla AE supplies no trained prior sampler; this does not rule out fitting a separate distribution to its codes later.

**Self-check:** Why does interpolating two fresh stochastic VAE samples confound the assignment comparison? You mix changes from sampling noise with changes along the chosen attribute direction; using the two means removes that source of randomness.

### B. Denoising and PSNR

**Source:** PDF p. 2; starter cells 16–17. Input is `clip(x + 0.3 ε, 0, 1)` with standard normal noise; the target is the **clean** image. Keep test images out of training. Reuse the same corrupted test images when comparing noisy and denoised PSNR.

**Numerical route:** [N4.2](numerical-practice.md#n4-2) calculates pixel MSE, dB values and mean per-image PSNR. This is a written worked example; a short, sufficiently reliable numerical video specific to this convention was not verified. The [MathWorks PSNR reference](https://www.mathworks.com/help/images/ref/psnr.html) supplies the formula and an executable noisy-image example.

Compute each image's MSE across its pixels, convert each to `10 log10(1/MSE)` for `[0,1]` images, then average the image scores as the starter does. Do not silently substitute PSNR of the dataset-wide mean MSE. Save the clean/noisy/denoised grid as `figures/B1_denoise.png` and both test mean scores in `metrics.json`. Exact equality has infinite mathematical PSNR; document the starter's `1e-12` numerical floor if it applies.

**Self-check:** Denoising is learned conditional reconstruction from an input containing structure. It does not require a rule for drawing new latent codes from an unconditional prior.

### C. Failure experiments: dying gradients and mode collapse

**Source:** PDF pp. 2–3; starter cells 18–25. Use only your six assigned MNIST digits at 28×28. Start from the Lecture 3 loss/gradient videos, then use [N4.3](numerical-practice.md#n4-3) to read a threshold event and [N4.4](numerical-practice.md#n4-4) to quantify collapse.

| Run | Required comparison | Evidence to retain |
|---|---|---|
| C1 | Saturating `mean log(1−D(G(z)))`; five D steps per G step; `lr_D=8e-4`, `lr_G=2e-4`; latent 64. | Every-iteration CSV, probability curves, log-scale gradient curve, exact reference value at iteration 100, first later strict crossing below 1%, 64 samples at that crossing and at the end. |
| C2 | Reset the seed and initial model/optimizer states; change only the generator loss to `−mean log D(G(z))`, preserving C1 architecture and D schedule. | Overlay gradient curves and compare grids at the same iteration (`figures/C2_overlay.png`); derive why the gradients differ when D confidently rejects fakes. |
| C3 | Five G steps per D step, G/D learning rates `2e-3`/`2e-4`, latent 2, no BatchNorm in G. Document any extra changes made to obtain full or partial collapse. | 5,000 generated samples classified with your trained six-digit classifier, class proportions, count of classes with at least 1%, reverse KL to the uniform six-class target, and a 64-sample grid. |

**Log carefully.** Keep the provided CSV fields; add fields rather than deleting the hook. Define an iteration consistently, e.g. one outer cycle ending in a G update, and count G/D optimizer steps separately when ratios differ. Record gradients after `backward()` and before `step()`, without contamination from a previous update. The starter searches **after** iteration 100. Log that exact row instead of relying on interpolation through missing rows. If the reference is zero, the strict “below 1%” test is degenerate; if there is no crossing, record that fact and the observed minimum rather than inventing an iteration. Save a checkpoint/grid when a crossing occurs, so it can be reproduced.

`D28` returns logits. For the usual logistic discriminator loss use stable logit-based expressions; logged `D(x)` and `D(G(z))` are sigmoid probabilities. With fake logit `a`, the saturating G loss is `−softplus(a)` and the non-saturating loss is `softplus(−a)`. Their derivatives with respect to `a` are `−σ(a)` and `σ(a)−1`. Do not detach generated images during the G update; detach them during the D update. See the [official PyTorch DCGAN tutorial](https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html) for the update pattern, while retaining this assignment's sizes and losses.

**Classifier and ranges:** remap the selected original digits to labels 0–5, and convert G's `tanh` samples from `[-1,1]` to `[0,1]` before the classifier. Conversely, map real MNIST to `[-1,1]` when feeding D. Measure classifier test accuracy on the held-out six-digit test subset; the starter requires at least 97% before trusting its metrics. Freeze and reuse the same classifier checkpoint in evaluation mode for every model. Six predicted classes do not prove six realistic modes: a classifier can confidently mislabel artifacts.

### D. DCGAN and one stabilizer

**Source:** PDF p. 3; starter cells 19, 25. D1 uses strided convolution, BatchNorm in both networks, LeakyReLU(0.2) in D, ReLU in G, `tanh` output, Adam `lr=2e-4, betas=(0.5,0.999)`, non-saturating G loss, and 1:1 updates. Keep one fixed set of noise vectors for early, one-third, two-thirds and final grids. Measure C3's histogram/mode coverage/KL again.

**Preparation:** the Lecture 3 DCGAN and stabilization sections cover the mechanisms. The [PyTorch tutorial](https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html) is an optional longer written implementation explanation, not a replacement for the required own training loop.

For D2 select one mechanism and implement it: WGAN-GP, spectral normalization of D, or minibatch discrimination **in D**. For the most direct study path through the supplied GAN deck, use minibatch discrimination (§3.7 and numerical practice N3.4); WGAN-GP and spectral normalization remain allowed alternatives but require additional study and implementation details beyond this guide's supplied-lecture coverage. Explain the mathematical change, its additional state/hyperparameters, and any required loss changes. WGAN-GP uses a real-valued critic rather than sigmoid/BCE losses; ordinary discriminator probability logs must not be relabeled as critic scores. Keep explicit score fields and document non-applicable probability columns. Compare C3, D1 and D2 in the required four-metric table: modes, reverse KL, IS and FID. Report improvements or failures from the actual measurements.

<a id="assignment-metrics"></a>

### E. IS, FID, and why a single score can mislead

**Source:** PDF pp. 3–4; starter cells 23–28. [GANs Part 2](#lecture-4) now supplies lecture derivations and expanded examples: [N5.3 IS](numerical-practice.md#n5-3), [N5.5 FID](numerical-practice.md#n5-5), and [N5.6 generative precision/recall](numerical-practice.md#n5-6). Precision/recall is new lecture material, not an additional required assignment deliverable. Preserve the assignment-specific features and sample budget below.

**Concise conceptual video:** [Andreas Maier / FAU — Unsupervised Learning, Part 3](https://www.youtube.com/watch?v=fXO1fOXnOTI), **13:19**. The university's [matching transcript and slides](https://lme.tf.fau.de/lecture-notes/lecture-notes-dl/lecture-notes-in-deep-learning-unsupervised-learning-part-3/) explicitly cover IS's confidence/diversity tradeoff and FID's Gaussian feature statistics. This is a focused university explanation with a small audience, not a claimed popular numerical walkthrough. Use [N4.5–N4.6](numerical-practice.md#n4-5) for checked arithmetic.

**Optional long-form:** [Ian Goodfellow — NIPS 2016 GAN tutorial](https://www.youtube.com/watch?v=AJVyzd0rqdc), **1:55:53**, for the broader training/evaluation picture. This university-linked recording is an upload by Hao Du (Alex); it predates FID and is not a FID tutorial.

- **Own classifier:** softmax outputs have shape `(N,6)` for IS; penultimate features `(N,128)` for FID. These are six-digit classifier scores in this course's feature space, not directly comparable to published ImageNet/Inception-V3 scores. Merely running a standard `pytorch-fid` package at the end cannot numerically validate this feature-space result unless the same features, preprocessing and covariance convention are used.
- **E1 IS:** generate 5,000 samples per model; following the starter, divide these into ten disjoint chunks of 500, compute each chunk's own marginal, obtain ten scores, then report mean and standard deviation with the chosen `ddof`. The handout's “10 splits of 5,000 samples” wording could instead mean 50,000 total; label the starter-consistent 5,000-total interpretation and check the instructor's intended sample budget. Evaluate real data, C1, C3, D1, D2. Use natural logarithms, handle `0 log 0` by its zero limit, and never confuse class-histogram KL with IS's average per-image KL.
- **E2 FID:** use the same real **training** reference features for all five sets. Compute sample means and covariance matrices (`rowvar=False`, normally denominator `N−1`). Use float64 and the matrix square root of the product, not elementwise square roots. Tiny imaginary residuals can arise numerically; examine their size before taking the real part. Large imaginary terms, non-finite values or materially negative distances require investigation. [SciPy's matrix-square-root documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sqrtm.html) explains the operation.
- **E3 floor:** compare two disjoint real **test** halves. A positive empirical distance reflects finite-sample differences in estimated feature moments; it is not a universal quality threshold. Identical sets should instead give approximately zero. Finite-sample bias is analyzed in [Chong & Forsyth's paper](https://arxiv.org/abs/1911.07023).
- **E3 noise:** use the same reference images, noise scale list `0,0.1,0.25,0.5,1`, fixed classifier and preprocessing; document whether noisy pixels are clipped. Fixing the base noise across scales makes comparison easier to interpret. At zero noise with identical inputs expect approximately zero. Audit any reversals through ranges, covariance orientation and numerical precision, but nonlinear features, clipping and sampling do not guarantee a strictly monotone curve. Preserve the observations.
- **E3 interpretation:** total single-class confident collapse yields IS=1, not a high score. A partial collapse across a few classes can score higher; repeated prototypes across all six classes can reach the maximum six-class IS of 6 while having no within-class variety. FID compares only first and second moments of the chosen features; equal moments can conceal different distributions. Use your scores and grids to identify which situation occurred. For limitations see [A Note on the Inception Score](https://arxiv.org/abs/1801.01973) and the [original FID paper](https://arxiv.org/abs/1706.08500).

### Submission and viva preparation

Keep the seed (last four roll digits), all three roll-derived choices, dataset splits, image transformations, optimizer settings, loss reductions, step ratios, classifier checkpoint and metric sample sizes with each run. Explicit seeds aid repeatability; exact GPU determinism is not automatic.

Every training run needs a CSV: GAN runs use the mandated GAN fields; AE/VAE/denoising/classifier runs also need meaningful loss/accuracy/MSE logs, with non-applicable GAN fields identified rather than invented. Preserve checkpoints, all cited PNGs and a `metrics.json` matching the report. The notebook should run top to bottom with saved outputs. The report is at most four pages including figures and must include two surprises, what failed, and a short LLM-use declaration. Before the viva, practise explaining a chosen CSV row, the loss-gradient mechanism, one metric calculation and one mismatch between a score and an image grid.

<a id="study-route"></a>
## A practical study route

| Session | Main work | Finish by doing without the video |
| --- | --- | --- |
| 1 | Introduction: distributions, model families and Bayes | Normalize the spam example, solve its changed-prior retry, explain A/B/C coverage |
| 2 | AE architecture and applications | Compute a reconstruction loss and explain why a plain AE has no enforced normal prior |
| 3 | VAE: distribution parameters, KL and sampling | Calculate variance, standard deviation, a reparameterized sample and the correctly signed KL |
| 4 | VAE objective and representation | Differentiate a small example; explain the reconstruction/regularization tradeoff and interpolation limits |
| 5 | GAN architecture and losses | Calculate D/G losses, compare saturating/non-saturating gradients, and trace which parameters update |
| 6 | Training failures, DCGAN and stabilization | Explain collapse versus a weak generator; work the convolution/latent and minibatch examples |
| 7 | Conditional GANs and StackGAN | Trace both conditional inputs; calculate shapes, parameters and conditioning augmentation |
| 8 | Part 2 evaluation: entropy, IS, FID and precision/recall | Reproduce the lecture's four-image IS, diagonal FID and both kNN-ball membership counts |
| 9 | Assignment metrics and evidence | Calculate PSNR, mode KL, IS and FID; explain a metric's blind spot and one logged gradient event |

Treat these as flexible study sessions, not time estimates or an official exam plan. The [numerical companion](numerical-practice.md) supplies worked examples and fresh retries. A useful checkpoint is to explain your first differing intermediate result when an answer is wrong. “I watched it” is not the same as being able to derive, calculate and interpret it.

## Selection and verification notes

- **Coverage:** Every page of all four supplied lecture decks was inventoried, with image-only material and important formulas inspected visually. The assignment and all starter-notebook cells were read. Brief examples and outline-only future topics are identified separately from developed material.
- **Short-first choices:** Prefer focused lessons or clearly bounded excerpts; give full runtimes for longer exceptions. Some exact course conventions require a written bridge. Conceptual, derivation and worked-number resources are labeled separately; a numerical video is not inferred from a mathematical title alone.
- **Reception and provenance, checked 15 September 2026:** The selected [IBM overview](https://www.youtube.com/watch?v=hfIUstzHs9A) had over 1.18 million views in public player metadata; [Google's introduction](https://www.youtube.com/watch?v=G2fqAlgmoPo) over 2.27 million; [StatQuest's Naive Bayes](https://www.youtube.com/watch?v=O2L2Uv9pdDA) over 1.40 million, with roughly 34,000 likes on its indexed creator page. These are reach/engagement signals, not a universal quality ranking. Specialist university lessons may have smaller audiences but a closer technical match. Counts change.
- **Part 2 additions, checked 16 September 2026:** StatQuest's entropy lesson had about 898,000 player-reported views (roughly 26,000 likes on its indexed creator page); Aladdin Persson's conditional tutorial about 35,000 views. The specialist StackGAN and FAU metrics explanations had about 2,800 and 1,100 views respectively; these are smaller-audience technical matches. The linked DeepLearning.AI course was rated **4.7/5 from 685 reviews** on its official Coursera page; that is a course-level reception signal, not an individual-lesson rating. Coursera lesson durations are provider-rounded and access may require enrollment. Exact lecture IS/FID/precision–recall arithmetic is supplied in the checked written examples; it is not attributed to videos without evidence.
- **Resource checks:** Video identities, authors and runtimes were checked against creator metadata or institutional pages. Clip boundaries use published chapters or inspected segments. Selected numerical-video claims were checked against visible calculations, creator transcripts or institution-provided worked-example material. Not every video was watched end to end; regional playback can differ.
- **Mathematical checks:** The written worked examples and fresh answer keys have local calculation checks. The guide distinguishes source errors, notation changes, different loss reductions, and model assumptions so that an attractive explanation does not silently teach a different calculation.
- **Assessment scope:** The course outline and handout contain some ambiguities; the relevant sections state them. The instructor's corrected files and announced quiz/midterm scope determine requirements. Extend this guide when the later lecture files arrive.
