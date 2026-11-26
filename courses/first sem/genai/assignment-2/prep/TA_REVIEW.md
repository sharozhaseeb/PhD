# TA Review: 20L-11327_A2.ipynb + make_report.py

This review checks the code against `prep/TA_CHECKLIST.md`. Cell numbers are 0-based, in notebook order. Line numbers refer to `make_report.py`.

## Overall verdict

The core technical work is correct, and I checked all of it line by line:

- **Data and padding:** classes {7, 0, 3}, padded with 0 *before* scaling, so the border becomes -1 (black).
- **Schedules:** both are correct. The cosine schedule uses f(t)/f(0), s = 0.008, the (t+1)/t ratio, a 0.999 clip and a cumprod recompute.
- **Forward process and training:** `q_sample` broadcasts correctly. The training step predicts eps and uses MSE.
- **Sampler:**
  - It uses 1/sqrt(alpha_t), beta_t/sqrt(1-abar_t) and sigma = sqrt(beta_t).
  - It adds no noise at t = 0.
  - x0_hat is computed with the correct formula.
- **Forbidden APIs:** there are no diffusers schedulers or pipelines and no `from_pretrained`. The only "pipeline" in the notebook is sklearn's `make_pipeline`, which is allowed.
- **Photo loading and preprocessing:** `exif_transpose` is used, and each model gets its own timm transform.
- **Features and split:**
  - Hooks go on `patch_embed`, `blocks.2/5/8/11` and `layers.0-3`.
  - Features are [CLS] (after the final norm) for ViT and GAP over NHWC for Swin.
  - One stratified split is reused for both models, and the scaler is fit on the train set only (it sits inside the pipeline).
- **Part C:** all numbers match my reference exactly.

The figure layouts are exactly as required:
- 2 x 6 forward grid
- 4 x 4 sample grid per model
- 8-timestep trajectory with x0_hat underneath
- up to 3 misclassified images per model

The FPN answer is 2 sentences and the A1 answer is 3 sentences, both within the required range.

The main risks are about process and honesty, not the maths. Several written answers were drafted before any results existed, and two run-time traps could quietly break the "identical settings" requirement or load the wrong checkpoints.

---

## MUST-FIX

### M1. Stale QUICK_TEST checkpoints can be loaded silently in the real run
**Where:** Cell 4 (`OUT`, `CKPT_DIR`), Cell 16 (`REUSE_CHECKPOINTS = True`), Cell 17 (`train_model` loads `ddpm_<name>.pt` if it exists).

**Problem:** A QUICK_TEST run in Colab writes `ddpm_linear.pt` and `ddpm_cosine.pt` to the same Drive folder. If the student forgets to delete `outputs/` (the README only says to delete it), the real run loads the 20-second models. All A2 and A3 results would then be wrong, and the loss curves would be tiny.

**Fix (pick one):**
- Use `OUT = BASE / ("outputs_quick" if QUICK_TEST else "outputs")`.
- Or, in `train_model`, only reuse a checkpoint when `ckpt["info"]["epochs"] == EPOCHS` and `ckpt["info"]["train_images"] == len(X_TRAIN)`. Otherwise retrain, and print why.

### M2. "Identical settings" can break after a Colab disconnect
**Where:** Cell 16 (`EPOCHS = choose_epochs(...)` is re-timed on every run), Cell 17.

**Problem:** Suppose the linear model finished, Colab disconnected, and the cosine model is trained in a new session. `EPOCHS` is then measured again and can differ (different GPU load, timing noise). The two models would have different epoch counts, which is a direct violation of the handout bullet.

**Fix:** If any checkpoint already exists, take `EPOCHS` from its `info["epochs"]` and skip `choose_epochs`. Also assert after training that `TRAIN_INFO["linear"]["epochs"] == TRAIN_INFO["cosine"]["epochs"]` (and batch size and lr), so the executed notebook shows this check passing.

### M3. Pre-written observations about results nobody has seen yet (A3)
**Where:**
- Cell 26, the whole first paragraph: "cosine model's samples look better to me ... linear model gives more blotchy or broken shapes", and "with the linear schedule x̂0 stays a grey blur until t is quite small".
- `make_report.py` lines 32-35 (`BETTER_SCHEDULE`, `SAMPLE_OBSERVATION`) and line 168 ("Both models give recognisable sneakers, T-shirts and dresses").

**Problem:** These describe figures that do not exist yet. If the real grids disagree, the student is reporting things that are false, and the viva ("show me where the linear x̂0 is still a blur") will expose it.

**Fix:**
- In cell 26, replace the claims with a placeholder such as `<<WRITE AFTER LOOKING AT THE GRIDS>>`, and write it after the run, from the actual grids and trajectories.
- Make "Both models give recognisable ..." a setting too, because it can be false for one model.
- The trajectory claim must describe the actual `A3_trajectory_*.png` figures.

### M4. Pre-written B2 discussion in the notebook leans towards Swin and assumes near-perfect accuracy
**Where:**
- Cell 43: the Swin bullet is phrased as an advantage, the ViT bullet says "[CLS] ... can be more sensitive to clutter", and the last bullet says "both probes are close to perfect; the few errors are photos where the object is small, partly cut off ...".
- `make_report.py` line 222: the reasons for errors are hard-coded. Line 237: "both probes do well" is hard-coded.

**Problem:**
- The report picks the winner automatically, but the notebook text does not. If ViT wins (quite likely with in21k augreg weights), the notebook and the report contradict each other, which a strict TA will notice.
- The handout asks the student to "discuss which backbone gave better features ... and suggest why", which needs actual numbers.
- The reasons for errors are invented until someone has looked at the misclassified photos.
- "Close to perfect" and "do well" are unverified.

**Fix:**
- Rewrite cell 43 after the run. State the winner with its numbers (accuracy and macro-F1 for both) and note that one error is 3.3%.
- Describe the *actual* misclassified photos.
- In `make_report.py`, add an `ERROR_OBSERVATION` setting to replace line 222. Make "both probes do well" conditional, for example only when both accuracies are at least 0.9.
- Make sure the notebook and the report name the same winner.

### M5. The Drive link and the student's name are placeholders
**Where:** `make_report.py` lines 28-30.

**Problem:** A missing or unshared Drive link costs the deliverable marks for the checkpoints and photos.

**Fix:** Make `build()` raise an error if `"PASTE-YOUR-LINK-HERE"` or `"Your Name"` is still present. Then test the link in an incognito window.

### M6. The notebook must be submitted fully executed
**Status:** It is currently unexecuted. That is expected, but it is the single biggest risk. It needs:

- a full run with `QUICK_TEST = False`
- no tracebacks
- the training logs visible

If the checkpoints are reloaded (`REUSE_CHECKPOINTS`), the executed notebook shows no training log at all, only "loaded existing checkpoint".

**Fix:**
- For the final submitted run, delete the checkpoints and train in the notebook.
- Or at least print the loaded `info` (epochs, time, steps, final loss) in Cell 17's reuse branch, so the evidence is visible.

---

## SHOULD-FIX

### S1. Make the A1 numbers in cell 13 accurate, and soften the grid claims
- "falls below 0.5 at about t ≈ 250" is slightly off. ᾱ₂₅₀ = 0.521, and it first drops below 0.5 at t = **259**. Write "≈ 260".
- Cell 13 says "the garment has almost disappeared by t = 500". `make_report.py` line 123 says "the garment is gone by t = 500 under the linear schedule but still visible under the cosine one". At t = 500, the linear schedule still has sqrt(ᾱ) = 0.28 of the signal, so a faint outline may still be visible. Check the grid, then write "is barely visible" rather than "gone".
- Line 126 of the report says the cosine schedule spreads destruction "evenly". It should say "more evenly", since it is not uniform.

### S2. Explain the extreme first steps and the x̂0 values near t = 999
At t = 999:

- **Cosine:** β = 0.999, so 1/sqrt(α) = **31.6**. Any error in ε_θ at the first reverse step is amplified about 32 times.
- **x̂0 amplification:** 1/sqrt(ᾱ₉₉₉) is about **157** for linear and about **20,000** for cosine.

As a result, the x̂0 at t = 999 (and t = 900 for linear) will be clamped, saturated salt-and-pepper noise.

- **Fix:** Add one sentence under the trajectory figure, in both the notebook and the report: "x̂0 at the first timesteps is dominated by amplified noise because sqrt(ᾱ_t) ≈ 0, so it is clamped." This heads off a viva question.
- If the cosine samples look over-saturated or high-contrast, this amplification is the likely cause. Mention it in the comparison rather than switching formulas, because the handout requires its own formula.

### S3. Trajectory label: x_0 versus the final output
**Where:** Cell 25, `TRAJ_T = [..., 0]`.

The "x_0" shown is the *input* to the last reverse step (0-indexed). The final image is the output of that step. The two differ only by about 0.01·noise, so they look the same visually, but a strict TA may ask.

**Fix:** Add one line in the markdown: "with 0-indexed steps, the last panel is x_t at t = 0; the final sample is the output of that step, and is visually identical." Alternatively, add the final output as an extra panel, keeping 8 x_t panels.

### S4. Print the ViT pretrained tag to back up the in21k claim
**Where:** Cell 30.

The B2 discussion and the report (line 216) say the ViT weights were pre-trained on ImageNet-21k and then fine-tuned on 1k.

**Fix:** Print `vit.pretrained_cfg.get("tag")` and `swin.pretrained_cfg.get("tag")`, for example `augreg2_in21k_ft_in1k` and `ms_in1k`. This puts the evidence in the notebook. Mention in the discussion that Swin-T here is IN-1k only, which is a fair reason if ViT wins.

### S5. The notebook's B2 discussion needs the actual numbers inline
Cell 43 currently says only "The table above ...". The final text should quote accuracy and macro-F1 for both models, so the discussion reads on its own.

### S6. Over-claims in the Part C cell
**Where:** Cell 44.

"makes global MSA impossible at this resolution" should be "impractical" (it is about 1.5 × 10¹¹ multiply-adds per layer; expensive, but computable).

Also add the attention-only check, hw/M² = 576 = number of windows, which is already in the report. That keeps the notebook and the report consistent.

### S7. The A2 section of the report should mention mixed precision and the drop-last policy
`make_report.py` line 135 shows "+ fp16". The notebook drops the last partial batch: 140 steps per epoch, using 17,920 of 18,000 images per epoch.

Say this in one clause, in case the TA checks steps = 140 × epochs.

### S8. Hidden folders inside `photos/`
**Where:** Cell 28.

`PHOTO_CLASSES` includes any directory, including `.ipynb_checkpoints`. The assert catches it, but with a confusing message.

**Fix:** Filter with `not p.name.startswith(".")`.

---

## NICE-TO-HAVE

- **N1. HEIC orientation.** pillow-heif usually applies the rotation when it decodes the image. Check visually in the collage that no photo is sideways (Cell 29) before trusting B2.
- **N2. Misclassified display (Cell 42).** It uses `ImageOps.fit(..., 224)` for display only. Add a comment like the one in the collage cell, so a TA does not read it as "manual resizing". Showing the timm-cropped view instead (`crop_pct` 0.9) would show exactly what the model saw.
- **N3. Unnecessary timing run (Cell 16).** `choose_epochs` runs even when both checkpoints exist. M2's fix removes this.
- **N4. Seed and GPU in the report.** Add a one-line "Setup" note: Colab T4, seed 11327, library versions. Cell 3 already prints these.
- **N5. `make_pipeline` (Cell 40).** In the viva, be ready to say that `make_pipeline` is sklearn, not a diffusers pipeline.
- **N6. Training curve.** Plotting the per-epoch mean as markers on top of the moving average would make the epoch count visible on the figure.
- **N7. B1 ViT table.** Add an explicit row such as "after [CLS] concat + pos-embed: (1, 197, 768)", either computed with a hook on `model.norm_pre` or `pos_drop`, or as a note. Then the 196 → 197 step appears in the table itself and not only in the text.
- **N8. Clarity of the long sentences.** The A1 answer and the FPN answer stay within their sentence limits by using very long sentences joined with semicolons and dashes. A TA reading strictly might count clauses. Consider splitting the FPN answer into exactly 3 clean sentences and the A1 answer into exactly 4.

---

## Estimated marks

These estimates assume a full execution with QUICK_TEST = False, real photos, and the must-fix items handled.

| Part | Max | Estimate after fixes | Estimate as-is, if run without fixing M1-M4 |
|---|---|---|---|
| A1 | 5 | 5 | 4.5 (grid claim may contradict the figure) |
| A2 | 8 | 8 | 6-8 (risk of unequal epochs or stale checkpoints) |
| A3 | 8 | 8 | 6 (comparison may not match the actual grids) |
| B1 | 8 | 8 | 8 |
| B2 | 12 | 11.5-12 | 9-10 (notebook and report may disagree; invented error reasons) |
| C | 10 | 10 | 10 |
| **Total** | **51** | **50.5-51** | **about 43.5-46.5** |

The deliverables (an executed notebook, a report of at most 8 pages, and a working Drive link) are preconditions. If any of them is missing, these numbers drop sharply.

---

# Phase 3: Final check (after the full local run)

I checked these against the source files and the executed run (`scratchpad/fullrun/executed.ipynb`, its figures, and `report.pdf`).

## The four changes

1. **fp32 and the finite-loss assert: OK.**
   - `train_step` is clean.
   - The assert runs once per epoch, which is enough.
   - The report says "AdamW in float32".

2. **U-Net with attention only at 8x8, LR 5e-4: OK.**
   - It is built from a config with random init.
   - `block_out_channels=(32, 64, 128)` as suggested.
   - 3,939,393 parameters.
   - Both models: 31 epochs, 4,340 steps, 885 s / 882 s. That is identical settings with about 15 minutes each, and the executed notebook prints it.
   - The higher LR has a justification comment. Have one viva sentence ready on why 5e-4 (short budget, Adam, a small network).

3. **x̂0 clipping in the sampler: defensible, and correct.**
   - The loop takes x̂0 from ε_θ, clamps it, recomputes ε' = (x_t − √ᾱ x̂0)/√(1−ᾱ), and then applies the handout's update unchanged.
   - This is algebraically identical to the DDPM posterior mean μ̃_t(x_t, clip(x̂0)) = [√ᾱ_{t−1} β_t/(1−ᾱ_t)] x̂0 + [√α_t (1−ᾱ_{t−1})/(1−ᾱ_t)] x_t. That is Ho et al.'s `clip_denoised=True`, so it is still "DDPM sampling with σ² = β, all 1000 steps, written by me".
   - The literal formula is still in the code (`clip_x0=False`), and its failure is shown with numbers:
     - std of x_998 = 1.48
     - 81% of pixels at −1
     - a fully black grid
   - A strict TA could object only if the deviation looked hidden. It is not hidden, but phrase it as an addition, not a replacement:

     > "The reverse step is the handout formula, implemented exactly (`clip_x0=False` runs it literally). Following the reference DDPM implementation (Ho et al. 2020, `clip_denoised=True`), I additionally clamp x̂0 to [−1, 1] and form ε from the clamped x̂0 before applying the same formula. This is needed because the cosine schedule's clipped β_999 = 0.999 amplifies ε errors by 1/√α_999 ≈ 31.6 (ablation shown). Both models use the same sampler, so the comparison is fair."

   - Viva: be able to derive why ε' plugged into the formula equals μ̃_t(x_t, x̂0).

4. **Rewritten discussions: mostly good.**
   - The A1 answer is now exactly 4 sentences, with exact numbers (259 / 673 / 496 / 935).
   - The B2 verdict is computed by the same rule in the notebook (cell 46) and in `make_report.py`, so they cannot disagree.
   - The tag print (`augreg2_in21k_ft_in1k` / `ms_in1k`) backs up the in21k claim.
   - The B1 table now has the `pos_drop` row (196 → 197).
   - The report is 6 pages and has the placeholder guard.

## Remaining MUST-FIX

### P3-M1. Back up "the linear model is almost unchanged by clipping"
**Where:** cell 22, cell 26; `make_report.py` (A3 paragraph, "the linear model … is almost unchanged").

**Problem:** The ablation only shows the cosine model, so this claim has no evidence in the notebook.

**Fix:** In cell 26, also run `ddpm_sample(MODELS["linear"], ..., clip_x0=False)` with the same seed and show its 4x4 grid. Print a number too, for example the mean |clipped − unclipped| per pixel. Mention it in one clause in the report.

This also covers you if a TA insists on the literal formula: the linear model is then shown with the exact handout sampler.

### P3-M2. The A3 observations must be rewritten from the Colab run's figures
**Where:** cell 28 and `make_report.py` (`SAMPLE_OBSERVATION`, and the `agree` text: "linear x̂0 is still noise until about t ≈ 600").

**Problem:** These sentences describe the local GTX 1660 run. The Colab T4 run will choose a different epoch count and produce different samples, so the text has to be re-checked against the new figures.

Even against the current figures, two phrases are slightly off:
- The linear x̂0 at **t = 600 already shows a blurry sneaker**. It is pure noise only at t = 750 and above. Write "x̂0 is still noise at t = 750 and the shape first appears around t = 600".
- "every sample in its grid is clearly one of my three classes" over-claims, since a few cosine samples are T-shirt/dress hybrids. Soften it to "almost every sample".
- Also be ready for the viva: the cosine trajectory sample is an odd vase-like garment.

### P3-M3. The submitted notebook must show training actually happening
**Where:** cells 18 and 19.

**Problem:** The executed local run shows "loaded existing checkpoint" for both models. There are no per-epoch logs, so a TA cannot see that training ran in this notebook.

**Fix:** For the Colab run that gets submitted, start with an empty `outputs/ckpt/` so cells 18-19 print the 31-ish epoch logs. If Colab disconnects mid-way, the reuse path plus the printed info is acceptable, but a full log is safer.

### P3-M4. Re-run Part B with the real photos and check the B2 text
**Problem:** The fake photos gave 100% / 100%, a tie.

**Fix:** With real photos, re-read the confusion matrices and misclassified images. Fill `B2_ERROR_NOTE` with what the errors actually look like.

**Should-fix (high):** if the real run is also a tie, "which backbone gave better features" is answered only by "equally good". A strict TA may take about 1 mark. Add one tie-breaker measured on the same split, such as the test log-loss or the mean predicted probability of the true class (`predict_proba`), and say which backbone is more confident. This is cheap and stays within the handout.

## Minor

- Page 3 of the report is half empty. That is fine at 6 of 8 pages, but you have room to add the linear no-clip grid (P3-M1) beside the cosine one.
- Cell 26 uses `torch.randn_like` without the generator for z in the one-step check. That is fine; the std is a statistic, not tied to a seed.

## Updated mark estimate

| Part | Max | Estimate |
|---|---|---|
| A1 | 5 | 5 |
| A2 | 8 | 8 |
| A3 | 8 | 7.5-8 (8 once P3-M1/M2 are done and the clipping is phrased as above) |
| B1 | 8 | 8 |
| B2 | 12 | 11-12 (12 with the real-photo discussion plus a tie-breaker if tied) |
| C | 10 | 10 |
| **Total** | **51** | **49.5-51** |

These marks assume an executed Colab submission, real photos, the Drive link filled in and shared, and a good viva.
