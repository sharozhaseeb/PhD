# CS5004 Assignment 2: Strict TA Grading Checklist

Student: Sharoz Haseeb, roll number 26L-9005, so **d = 5**.

- Part A classes: **5 Sandal, 8 Bag, 1 Trouser**. Fashion-MNIST **train** split only, 3 x 6,000 = **18,000** images.
- Part C settings: **448 x 448 x 3, C = 128**, patch 4, M = 7, depths 2, 2, 6, 2.
- Total: 51 marks (A1 5, A2 8, A3 8, B1 8, B2 12, C 10).

---

## 0. Global rules (each one can cost a whole part or the whole assignment)

- [ ] **Correct d everywhere.** Classes {5, 8, 1}. The digit appears in the notebook: `d = 5`, and the class list is computed or printed. Part C uses 448 / 128. Wrong settings give **zero for that part**.
- [ ] Notebook is named **`26L-9005_A2.ipynb`** (RollNo_A2.ipynb).
- [ ] No artefacts left over from an earlier digit:
  - checkpoints, `results.json` and figures must come from a run on classes {5, 8, 1}
  - the checkpoint info should record the class list, and reuse should assert it
  - the printed class list must read Sandal, Bag, Trouser
- [ ] **Every cell is executed** and the outputs are saved: plots, printed shapes, timings, metrics. If the TA has to re-run anything, expect a deduction. There should be no error tracebacks left in the outputs.
- [ ] Execution counts look sensible, and the saved outputs match the numbers in the report.
- [ ] Report is a **PDF of at most 8 pages**. Anything past page 8 may be ignored, and over-length can be penalised.
- [ ] The report contains every figure, table, discussion and **Part C working**. Part C done only in the notebook does not count; it must be in the report.
- [ ] **Google Drive link in the report.** It is shared as "anyone with the link can view" (test it in an incognito window). It contains:
  - [ ] the Part A checkpoint(s) (upload **both** linear and cosine to be safe)
  - [ ] all **100** Part B photos, organised by class
- [ ] Have the original phone photos ready for the viva (EXIF metadata, originals on the phone). The photos must be your own.
- [ ] Be able to explain every line of code and every number. Missing the viva means zero.
- [ ] No `diffusers` schedulers or pipelines anywhere: no `DDPMScheduler`, `DDIMScheduler`, `DDPMPipeline`, `add_noise`, `scheduler.step`. Only `diffusers.UNet2DModel` is allowed.
- [ ] No `from_pretrained` for the UNet. It must be built with `UNet2DModel(...)` from a config, with random init.
- [ ] Part B uses **pretrained** timm models with **no fine-tuning**. The backbones are frozen: `eval()`, `torch.no_grad()`, or `requires_grad=False`.
- [ ] Set seeds and print them (torch, numpy, random, and sklearn `random_state`).
- [ ] Print the GPU type (T4) and the library versions (torch, diffusers, timm, sklearn). The timm version matters for the stage layout.

---

## A1. Forward process and noise schedules (5 marks)

**Data prep (shared with A2)**
- [ ] Loads the Fashion-MNIST train split and filters labels to {5, 8, 1}. Prints the count **18,000** and **6,000 per class**.
- [ ] Pads 28 to 32 (2 pixels on each side) and scales to [-1, 1].
  - **Pitfall:** padding with 0 *after* scaling gives a grey border (value 0 means mid-grey). Pad with -1, or pad before scaling.
- [ ] Prints a tensor shape of (N, 1, 32, 32) and min/max of -1 and 1.

**Schedules (own PyTorch code)**
- [ ] Linear schedule: `beta = linspace(1e-4, 0.02, 1000)`, T = 1000.
- [ ] `alpha_t = 1 - beta_t` and `alpha_bar_t = cumprod(alpha)`.
- [ ] Cosine schedule (Nichol and Dhariwal 2021):
  - `f(t) = cos^2( ((t/T + s)/(1 + s)) * pi/2 )` with **s = 0.008**
  - `alpha_bar_t = f(t)/f(0)`, normalised by f(0)
  - `beta_t = 1 - alpha_bar_t / alpha_bar_{t-1}`, **clipped at 0.999**
  - Then recompute alpha_bar from the clipped betas (cumprod) so that the forward process and the sampler use the same numbers.
- [ ] Both schedules are length-1000 arrays indexed **t = 0..999**. The indexing convention is stated, and the same convention is used in A1, A2 and A3.

**Figures**
- [ ] **One figure** plots alpha_bar_t against t for both schedules, with a legend, axis labels and a title.
- [ ] A **2 x 6 grid**: row 1 is linear, row 2 is cosine. Columns are **t = 0, 100, 250, 500, 750, 999**.
  - [ ] It uses the **same training image** and the **same epsilon** for both rows, so the comparison is fair.
  - [ ] It uses the closed form `x_t = sqrt(abar_t) x0 + sqrt(1 - abar_t) eps`. There must be no iterative noising.
  - [ ] Display is clipped or rescaled from [-1, 1] to [0, 1]. Rows are labelled with the schedule name and columns with t.

**Discussion (exactly 3 to 4 sentences)**
- [ ] It says the **linear schedule destroys the image faster**.
- [ ] It explains why: alpha_bar falls steeply and is near 0 by t of about 600-700. The last roughly 30% of steps are almost pure noise and carry little training signal.
- [ ] It explains the cosine schedule: alpha_bar decays roughly linearly through the middle and flattens near both ends, so information is lost more gradually.
- [ ] It explains why this matters for training: the uniform t sampling wastes fewer steps, the model learns more useful mid-noise denoising, and this matters most at low resolution such as 32 x 32 (Nichol and Dhariwal's observation).

**Reference values to cross-check** (0-indexed, cosine uses the betas_for_alpha_bar convention with clipping)

| t | linear alpha_bar | cosine alpha_bar | linear sqrt(abar) | cosine sqrt(abar) |
|---|---|---|---|---|
| 0 | 0.9999 | 0.99996 | 0.9999 | 1.0000 |
| 100 | 0.8951 | 0.9716 | 0.946 | 0.986 |
| 250 | 0.5214 | 0.8459 | 0.722 | 0.920 |
| 500 | 0.0778 | 0.4923 | 0.279 | 0.702 |
| 750 | 0.0033 | 0.1432 | 0.057 | 0.378 |
| 999 | 4.0e-5 | 2.4e-9 | 0.0064 | ~0 |

- Linear alpha_bar first drops below 0.01 at t = 673. Cosine does so at t = 935.
- If the student uses `alpha_bar_t = f(t)/f(0)` directly at index t (not t+1), the values differ slightly (for example 0.494 at t = 500). That is fine if it is consistent.
- At t = 0 the image is very slightly noised (one step, since beta_0 > 0). This is expected with 0-indexing.

---

## A2. Training with the epsilon-prediction loss (8 marks)

- [ ] Builds `UNet2DModel` with `sample_size=32`, `in_channels=1`, `out_channels=1`, `block_out_channels=(32, 64, 128)`. There are 3 down and 3 up block types to match `block_out_channels`.
- [ ] Random init, no `from_pretrained`. Ideally prints the UNet parameter count.
- [ ] The training step is written by the student:
  1. Sample a batch x0.
  2. Sample `t ~ Uniform{0..999}` per example, as integers on the device.
  3. Sample `eps ~ N(0, I)`.
  4. Build `x_t = sqrt(abar[t]) x0 + sqrt(1 - abar[t]) eps`. abar is broadcast to (B, 1, 1, 1).
  5. Compute `eps_hat = model(x_t, t).sample`.
  6. Compute `loss = MSE(eps_hat, eps)`. The target is **eps, not x0**.
  7. Run the optimiser step.
- [ ] The timestep passed to the UNet uses the same convention (integer 0..999) in training and in sampling.
- [ ] **Two models with identical settings**: same architecture, optimiser, lr, batch size, epochs or time budget, data, and preferably the same seed. Only the schedule differs.
- [ ] Each model trains for **about 15 minutes** on a Colab T4. The measured wall-clock time is printed for each.
- [ ] **One figure** shows both loss curves (linear and cosine). A per-step curve with smoothing or a per-epoch average is fine. It has labels and a legend.
- [ ] **Both checkpoints saved** (`.pt` state_dict) and uploaded to Drive.
- [ ] The report states the following, for both models (a table works well):
  - [ ] training time
  - [ ] **batch size**
  - [ ] **learning rate**
  - [ ] **number of epochs** (state fractional epochs if training was time-capped)
  - [ ] optimiser, and steps or iterations (good practice)
- [ ] There is no data leakage concern, but the model is **unconditional**. Samples are a mix of the 3 classes, with no class label input.
- **Pitfall:** the loss values of the two schedules are not directly comparable as quality measures, because a different t distribution gives a different difficulty. Do not claim "lower loss means better samples."

---

## A3. Sampling with DDPM (8 marks)

- [ ] Own sampling loop over **all 1000 steps**, t = 999 down to 0. There is no step skipping and no DDIM.
- [ ] Starts from `x_999 ~ N(0, I)` (shape (16, 1, 32, 32)).
- [ ] Update rule: `x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (beta_t / sqrt(1 - abar_t)) * eps_hat) + sigma_t z`, with **sigma_t^2 = beta_t**, so sigma_t = sqrt(beta_t).
  - [ ] **z = 0 at the last step** (t = 0 in 0-indexing). No noise is added to the final output.
  - [ ] It uses alpha_t and abar_t from the **same schedule** the model was trained with.
  - [ ] It runs under `torch.no_grad()` with the model in `eval()`.
- [ ] Final images are clamped to [-1, 1] and shown as **two 4 x 4 grids**, one per model. Each grid has a label.
- [ ] **Sampling time** is reported for each model: the time for 16 images x 1000 steps, measured with `torch.cuda.synchronize()` or something equivalent.
- [ ] **Trajectory figure** for one sample:
  - [ ] **8 timesteps** from x_999 to x_0, including both endpoints (for example 999, 857, 714, 571, 428, 285, 142, 0).
  - [ ] **x0_hat under each x_t**, giving a 2 x 8 layout. `x0_hat = (x_t - sqrt(1 - abar_t) eps_hat) / sqrt(abar_t)`.
  - [ ] x0_hat is clamped to [-1, 1] for display. It is noisy and unbounded near t = 999 because sqrt(abar) is about 0.
  - [ ] It states which model the trajectory is from. Showing both is a bonus.
- [ ] **Discussion:**
  - [ ] Says which model looks better for Sandal / Bag / Trouser, with evidence (sharpness, class-likeness, variety).
  - Class-specific things to look for with d = 5:
    - sandals are thin straps with a lot of background, so they are the hardest to generate and blur easily
    - bags are large, mostly filled blobs, often with a handle
    - trousers are two vertical legs, so check that the legs are separated
  - [ ] Says whether this agrees with A1. Either answer is acceptable if it is honest and reasoned. Cosine usually helps at 32 x 32, but with about 15 minutes of training the linear model can look comparable or better.
  - [ ] Explains **1000 NFEs versus 1 per training step**. Training uses the closed form q(x_t | x0), so any t can be reached in one shot and one random t is trained per example. Sampling must invert a Markov chain sequentially: each x_{t-1} needs eps_hat(x_t, t), so there are 1000 dependent network evaluations.
- [ ] Samples are recognisable and class-like. Perfection is not required, but noise blobs suggest a bug.

**Common A3 bugs:**
- Using sqrt(beta_t) where beta_t / sqrt(1 - abar_t) belongs.
- Dividing by sqrt(abar_t) instead of sqrt(alpha_t).
- Adding noise at the final step.
- Off-by-one between abar index and model t.
- Using the linear schedule to sample from the cosine model.

---

## B1. Trace the shapes (8 marks)

**Dataset and preprocessing (shared with B2; the collage counts in the report)**
- [ ] 4 classes x 25 photos = **100** of the student's own photos, with varied background, angle and lighting.
- [ ] **Collage** of the dataset in the report (all 100 thumbnails, or a clear per-class sample).
- [ ] Loads each photo with `ImageOps.exif_transpose(Image.open(path)).convert('RGB')`.
- [ ] Uses `cfg = timm.data.resolve_model_data_config(model)` and `transform = timm.data.create_transform(**cfg, is_training=False)`, **separately for each model**.
  - Pitfall: the ViT augreg weights use mean and std of 0.5, while Swin uses ImageNet mean and std. Reusing one transform for both is wrong.
- [ ] No manual `resize` / `thumbnail` / cv2 resizing of the photos.

**Hooks**
- [ ] Uses `register_forward_hook` (not just printing `model.forward_features` shapes) for one real 224 x 224 transformed image.
- [ ] **ViT** (`vit_base_patch16_224`, pretrained): hooks `patch_embed` and blocks **3, 6, 9, 12** (indices 2, 5, 8, 11).
- [ ] **Swin** (`swin_tiny_patch4_window7_224`, pretrained; `features_only=True` is fine): hooks `patch_embed` and all 4 stages (`layers.0`..`layers.3`, or `layers_0`.. in the features_only wrapper).
- [ ] Hooks are removed afterwards (good practice).

**Expected shapes (batch 1)**

| Model | Hook point | Raw output shape | Tokens | Channels | Grid / stride | Downsampling |
|---|---|---|---|---|---|---|
| ViT | patch_embed | (1, 196, 768) | 196 | 768 | 14 x 14 / 16 | Yes, here only: 16 x 16 conv, stride 16 |
| ViT | after adding [CLS] + pos | (1, 197, 768) | 197 | 768 | - | - |
| ViT | block 3 / 6 / 9 / 12 | (1, 197, 768) | 197 | 768 | 14 x 14 + CLS | None |
| Swin | patch_embed | (1, 56, 56, 96) NHWC | 3136 | 96 | 56 x 56 / 4 | Yes: 4 x 4 patch, stride 4 |
| Swin | stage 1 | (1, 56, 56, 96) | 3136 | 96 | stride 4 | None |
| Swin | stage 2 | (1, 28, 28, 192) | 784 | 192 | stride 8 | PatchMerging at start of stage 2 |
| Swin | stage 3 | (1, 14, 14, 384) | 196 | 384 | stride 16 | PatchMerging at start of stage 3 |
| Swin | stage 4 | (1, 7, 7, 768) | 49 | 768 | stride 32 | PatchMerging at start of stage 4 |

- [ ] The table includes token count, channel width, and **where downsampling happens**.
- [ ] Notes that timm Swin outputs are **NHWC** (B, H, W, C), so tokens = H x W. With `features_only`, the output format is also NHWC, and it must be permuted to NCHW for an FPN.
- [ ] Notes that in recent timm (0.9 and later), `PatchMerging` is the **downsample at the start of stages 2-4**, which matches the paper. Older timm put it at the end of stages 1-3, which shifts the shapes by one stage. Print `timm.__version__`.
- [ ] Notes that the ViT patch_embed hook shows 196 tokens. The [CLS] token is concatenated after it (in `_pos_embed`), giving **197**.
- [ ] **Parameter counts**, computed with `sum(p.numel() for p in model.parameters())`:
  - ViT-B/16: about **86.6 M** (86,567,656 with the 1000-class head).
  - Swin-T: about **28.3 M** (28,288,354 with the head).
  - A `features_only` Swin has no head, so it is about 27.5 M.
  - State which variant was counted. Counting both with heads, or both without, is clearest.
- [ ] **FPN explanation (exactly 2 to 3 sentences)**:
  - Swin is hierarchical. It outputs 4 multi-scale maps at strides **4, 8, 16, 32** (56², 28², 14², 7²) with growing channels, like a ResNet's C2-C5, so an FPN can take them directly.
  - ViT keeps a single-scale stride-16 14 x 14 map at constant width through every block, with no pyramid. It would need extra up and down sampling (as in ViTDet's simple pyramid).
  - Bonus: windowed attention keeps the cost linear in image size, which suits high-resolution detection inputs.

---

## B2. Linear probe on your photos (12 marks)

- [ ] Backbones frozen, in eval mode, under `no_grad`. There is no fine-tuning.
- [ ] Features:
  - **ViT** uses the **[CLS] token**: `forward_features(x)[:, 0]` (after the final norm), or `num_classes=0` with `global_pool='token'`. The result is 768-d.
  - **Swin** uses **global average pooling** over the 7 x 7 x 768 map: `forward_head(forward_features(x), pre_logits=True)`, `num_classes=0`, or the mean over H and W of stage 4. The result is 768-d.
  - [ ] Prints the feature matrix shapes: (100, 768) each.
  - Using mean-pooled ViT tokens, or a flattened Swin map, loses marks.
- [ ] A **single stratified 70/30 split** (`train_test_split(..., test_size=0.3, stratify=y, random_state=...)`) on **indices**, reused for both models. That gives 70 train and 30 test, with 7-8 test images per class.
  - The split is computed once and both feature sets are indexed with it. Two separate calls with different seeds count as different splits, which is a deduction.
- [ ] Logistic regression (sklearn) with enough iterations to converge (no ConvergenceWarning left in the outputs).
  - If a scaler is used, it is fit on the train set only. Same classifier hyperparameters for both models.
- [ ] **Accuracy and macro-F1** for both models, in a table (`f1_score(average='macro')`). Note that one test error equals 3.3% accuracy.
- [ ] **Two confusion matrices** (4 x 4) with class names on the axes.
- [ ] **3 misclassified test images per model** (or all if fewer), showing the original photo with its true and predicted labels.
  - If a model has 0 errors, say so explicitly.
- [ ] **Discussion:**
  - [ ] Says which backbone gave better features, and by how much. With 30 test images, small differences are within noise, so acknowledge that.
  - [ ] Gives plausible reasons. For example:
    - pretraining data (the ViT augreg weights use IN-21k pretraining, so they are more general)
    - [CLS] versus GAP pooling
    - Swin's local inductive bias and multi-scale features
    - centre-crop effects
    - class confusions that match the visual similarity of the objects
- [ ] Ideally the class names and the photo-to-label mapping are printed.

---

## C. Working by hand, d = 5 (10 marks)

**Interpretation (state it in the report):** the "linear embedding" output is the token grid right after the 4 x 4 patch partition and the linear projection to C. "Stage 1" is the output of the 2 Swin blocks that follow, which keep the resolution. Stages 2-4 each begin with patch merging (h/2, w/2, 2C), as in the Swin paper. A student who writes "the linear embedding is part of stage 1" and gives one line is still correct, provided the numbers below appear.

**Sizes**

- Patch partition: 448 / 4 = 112, so each patch is 4·4·3 = 48-d.
- Linear embedding: **112 x 112 x 128** (12,544 tokens)

| Stage | h x w x channels | Tokens | Windows (h/7 · w/7) |
|---|---|---|---|
| Stage 1 | **112 x 112 x 128** | 12,544 | 16 x 16 = **256** |
| Stage 2 | **56 x 56 x 256** | 3,136 | 8 x 8 = **64** |
| Stage 3 | **28 x 28 x 512** | 784 | 4 x 4 = **16** |
| Stage 4 | **14 x 14 x 1024** | 196 | 2 x 2 = **4** |

- Every size is divisible by 7, so no padding is needed.
- Each window has M² = 49 tokens.
- Shifted windows (SW-MSA) keep the same window count thanks to cyclic shift and masking. A naive shift would give (16+1)² = 289 windows in stage 1.

**Costs for one stage-1 attention layer** (h = w = 112, hw = 12,544, C = 128, M = 7)

- C² = 16,384.
- 4hwC² = 4 · 12,544 · 16,384 = **822,083,584**
- (hw)² = 157,351,936, so 2(hw)²C = 2 · 157,351,936 · 128 = **40,282,095,616**
- 2M²hwC = 2 · 49 · 12,544 · 128 = **157,351,936**
  - This equals (hw)² by coincidence, because 2·49·128 = 12,544 = hw.

| Quantity | Exact value | Approx. |
|---|---|---|
| **Omega(MSA)** = 4hwC² + 2(hw)²C | **41,104,179,200** | 4.110 x 10^10 |
| **Omega(W-MSA)** = 4hwC² + 2M²hwC | **979,435,520** | 9.794 x 10^8 |
| **Ratio** MSA / W-MSA | (4C + 2hw)/(4C + 2M²) = 25,600 / 610 = **2,560 / 61** (= 12,800 / 305) | **≈ 41.97** |

Cross-checks:
- Factor out hwC = 1,605,632. Then MSA = hwC · 25,600 and W-MSA = hwC · 610.
- The attention-term-only ratio is 2(hw)²C / 2M²hwC = hw/M² = **256** (the number of stage-1 windows).
- The projection term 4hwC² is identical in both, which is why the full ratio (about 42) is much smaller than 256.
- The (hw)² term is 98.0% of Omega(MSA).
- The units are multiply-adds (FLOPs as defined in the Swin paper), ignoring softmax.
- Bonus: SW-MSA in the second stage-1 block costs the same as W-MSA. A full stage-1 MSA versus W-MSA comparison over 2 blocks gives the same ratio.

**Marking points:**
- [ ] Linear embedding size.
- [ ] All 4 stage sizes.
- [ ] All 4 window counts.
- [ ] Both Omega values with the intermediate terms shown.
- [ ] The ratio.
- [ ] The working is shown step by step in the report.
- [ ] Watch for the common errors:
  - using 224/56 by mistake
  - forgetting C doubles per stage
  - using the window count instead of tokens in the formulas
  - squaring hw incorrectly
  - writing the ratio upside down

---

## Viva question bank (short model answers)

### A1
1. **Why can we jump straight to x_t?** The Gaussian steps compose: q(x_t | x0) = N(sqrt(abar_t) x0, (1 - abar_t) I), with abar_t the product of alpha_s.
2. **What is the role of s = 0.008?** It keeps beta_t from being too small near t = 0, so there is still enough noise early for the network to predict eps there. It prevents a singular start.
3. **Why clip beta at 0.999?** Near t = T, f(t) goes to 0, so beta goes to 1, which causes singularities (division by sqrt(alpha_t) blows up) at the end.
4. **Why normalise by f(0)?** So that abar_0 is exactly 1 at t = 0, meaning a clean image.
5. **What does SNR(t) = abar/(1 - abar) look like for each schedule?** Linear SNR collapses early. Cosine log-SNR falls roughly linearly through the middle.

### A2
1. **Why predict eps rather than x0?** It is the reparameterisation of the ELBO from Ho et al. The "simple" loss is a reweighted VLB, and it trains more stably with a unit-variance target.
2. **Why sample t uniformly?** It is an unbiased Monte-Carlo estimate over all timesteps, and one network shares all of them.
3. **How does the UNet know t?** Through sinusoidal timestep embedding, then an MLP, added inside the ResNet blocks.
4. **Why is the model unconditional, and how would you add class control?** It gets no label input. Add a class embedding (`num_class_embeds`) or use classifier-free guidance.
5. **What did you change between the two runs?** Only the beta schedule. Everything else was identical.

### A3
1. **Derive the mean of the update.** mu_theta = (1/sqrt(alpha_t)) (x_t - beta_t / sqrt(1 - abar_t) · eps_hat), from the posterior q(x_{t-1} | x_t, x0) with x0 replaced by x0_hat.
2. **sigma² = beta_t versus beta-tilde_t?** These are the two DDPM choices, the upper and lower bounds on the reverse variance. Both give similar samples.
3. **Why no noise at the last step?** The output should be the mean estimate of x0. Adding noise would leave grain in the image.
4. **Why does x0_hat look blurry early?** It is the posterior-mean (MMSE) estimate, which averages over many plausible images when noise is high.
5. **How can sampling be sped up?** DDIM (deterministic, fewer steps), strided sampling, or distillation.

### B1
1. **Why 197 tokens?** (224/16)² = 196 patches plus 1 [CLS].
2. **What does PatchMerging do?** It concatenates 2 x 2 neighbouring tokens (giving 4C) and applies a linear layer to 2C. That halves the resolution and doubles the channels.
3. **Where is ViT's positional information?** In a learned absolute position embedding added after the CLS token is concatenated. Swin uses a relative position bias inside each window.
4. **Why is ViT's cost quadratic, while Swin's is linear in image size?** Global attention costs (hw)². Windowed attention costs M²·hw.
5. **What does `features_only=True` return?** The 4 stage outputs (NHWC) without the norm, pool or head, which is what a backbone for Cascade Mask R-CNN or UperNet needs.

### B2
1. **Why a linear probe?** It measures the quality of the frozen representation and avoids overfitting with only 100 images.
2. **Why [CLS] for ViT but GAP for Swin?** ViT was trained to classify from [CLS]. Swin's classification head uses global average pooling, so that is its native pooled feature.
3. **Why stratify, and why use the same split?** Stratifying keeps the classes balanced. The same split makes the comparison fair, so only the features differ.
4. **Why macro-F1 alongside accuracy?** It averages per-class F1 so each class counts equally. It is robust if the classes become imbalanced.
5. **Why does exif_transpose matter?** Phone photos store their orientation in EXIF. Without it, images are fed sideways, the centre crop takes the wrong area, and the features degrade.

### C
1. **Why is C doubled at each merge?** To keep compute per stage roughly constant as the token count drops by 4x.
2. **What does the ratio depend on?** On hw/M². It grows linearly with image area, so it is largest at high resolution and in stage 1.
3. **Why is 4hwC² the same in both?** The QKV and output projections are per-token. Only the attention term changes.
4. **What if h is not divisible by M?** Pad the feature map to a multiple of M (and mask).
5. **How does SW-MSA connect windows without extra cost?** A cyclic shift by M/2 plus an attention mask keeps the window count at 256 (stage 1, d = 5), not the naive 289.
