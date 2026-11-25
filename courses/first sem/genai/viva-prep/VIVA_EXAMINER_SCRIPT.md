# Viva Examiner Script: A2 (DDPM / ViT / Swin) and A3 (PEFT for Urdu)

Mock examiner: Dr. Maryam Bashir, CS5004 Advanced Topics in Generative AI, FAST-NUCES Lahore.
Student: Sharoz Haseeb, 26L-9005, d = 5. A3: Group 3, Track 3, seeds 3 and 103.
Every number below was checked against `results.json`, `results.csv`, `per_class.csv`, `validation_selection.json`, the reports and the source code.

---

## 0. How this examiner works (evidence)

| Claim | Status | Evidence |
|---|---|---|
| "Explain every line of your code and every number in your report"; code you cannot explain counts as plagiarism | **Seen** | A2 handout, Instructions; A3 handout says the same about "copied code or text" |
| Personalisation is graded hard: another student's d settings "earns zero for that part" | **Seen** | A2 handout. d = 5 gives classes 5, 8, 1 (Sandal, Bag, Trouser) and Part C 448x448, C = 128 |
| Own photos "the viva will check this" | **Seen** | A2 Part B. Expect "show me the originals on your phone" |
| A3 viva is individual; "any member may be asked about any part"; marks adjusted by viva and contribution statement | **Seen** | A3 handout |
| She tests with RQs (RQ1 trade-offs, RQ2 tokenizers, RQ3 scarcity) and specific report prompts ("Is r = 16 worth its extra cost?", "How much memory does QLoRA save?") | **Seen** | A3 Part 4. Expect these exact questions |
| She favours derivations done by hand with numbers (variance-preserving derivation, posterior-mean coefficient "simplifies to 1/sqrt(alpha_t)", worked exercise x3 = 0.504 x0 + 0.864 eps, sinusoidal PE "why sin cosine") | **Seen** (lecture slide text) | Diffusion Part 1/2 and Transformer.pdf |
| She will ask you to re-derive one number on paper (Part C ratio, MuRIL 0.222) | **Inferred** | Part C is "by hand, showing all working"; her lectures use numerical exercises |
| She will open the notebook at a random cell and ask "what does this line do" | **Inferred** | Follows from the "every line" rule |
| She will notice anything that deviates from the handout (clipping x0, augmented photos, sole-member group, AI use in contribution line) | **Inferred** | Deviations are the cheapest way to detect copied work |
| Course outline covers PEFT, LoRA/QLoRA, prompt tuning, RAG, agents | **Seen** | GenAI_courseOutline MSDS.pdf topic list |

---

## 1. Assignment 2 script (about 15 min)

**Q1. Opener: "Walk me through what you did, in two minutes."**
- Follow-up: "Which part was hardest?"
- Model answer: Part A: I wrote linear and cosine schedules, the closed-form forward process, the eps-prediction training loop and the 1000-step DDPM sampler myself; only `UNet2DModel` (3,939,393 params, random init) came from diffusers. Part B: I traced shapes with forward hooks in ViT-B/16 and Swin-T and ran a frozen-feature logistic-regression probe on my own 4-class photos. Part C: Swin sizes, windows and MSA vs W-MSA cost by hand for d = 5. Hardest: the cosine sampler blowing up at t = 999, which I fixed by clamping x0.
- Red flag: "I followed the template / the AI generated it and I checked it." Never say you only checked.

**Q2. Personalisation: "What is your d and what did it change?"**
- Follow-up: "Compute your classes for me now."
- Model answer: d = 5, so classes 5, (5+3) mod 10 = 8, (5+6) mod 10 = 1: Sandal, Bag, Trouser, 18,000 images. Part C row 5 is 448 x 448 x 3 with C = 128.
- Red flag: Hesitating on (5+6) mod 10 = 1. Do the arithmetic aloud.

**Q3. Theory: "Why is the forward process sqrt(alpha_bar) x0 + sqrt(1 - alpha_bar) eps? Why the square roots?"**
- Follow-up: "What is alpha_bar_t?"
- Model answer: alpha_bar_t is the product of (1 - beta_s) up to t. The coefficients are chosen so that if x0 has unit variance, Var(x_t) = alpha_bar + (1 - alpha_bar) = 1 at every t (variance preserving), so alpha_bar is the signal's share of the variance. Composing t Gaussian steps gives one Gaussian, which is why we can jump straight to any t.
- Red flag: "Square root because of normalisation" with no variance argument.

**Q4. "Which schedule destroys the image faster? Give me your numbers."**
- Follow-up: "Why does that matter for training?"
- Model answer: Linear. Its alpha_bar falls below 0.5 at t = 259 and below 0.01 at t = 673 (alpha_bar_500 = 0.078); cosine reaches 0.5 only at t = 496 (alpha_bar_500 = 0.492) and 0.01 at t = 935. Since t is sampled uniformly, about 33% of linear training steps (t from 673 to 999) see near-pure noise and teach little; cosine spends more budget on partly noised images.
- Red flag: "Cosine is faster because cosine decays fast."

**Q5. Open notebook cell 6 (`cosine_betas`): "Explain every line."**
- Follow-up: "Why s = 0.008? Why clamp at 0.999?"
- Model answer: f(t) = cos^2(((t/T + s)/(1 + s)) * pi/2), alpha_bar(t) = f(t)/f(0), beta_t = 1 - alpha_bar(t+1)/alpha_bar(t), clamped at 0.999, then alpha_bar is recomputed with `torch.cumprod` of (1 - beta). s = 0.008 keeps beta from being tiny near t = 0 (Nichol and Dhariwal). The clamp avoids beta = 1 at the end, which would make alpha_t = 0 and the reverse step divide by zero.
- Red flag: Not knowing what `cumprod` returns.

**Q6. "Show me the training step and tell me the hyperparameters in your table."**
- Follow-up: "Why is the cosine loss (0.0502) higher than linear (0.0280)? Is cosine worse?"
- Model answer: Sample x0, t ~ U{0..999}, eps ~ N(0, I), build x_t in closed form, predict eps_theta(x_t, t), MSE to eps. Both runs: 28 epochs, batch 128, lr 5e-4, AdamW, 140 batches per epoch so 3,920 steps; linear 16.3 min (975.6 s), cosine 16.7 min (999.5 s). The losses are not comparable: at very noisy t, x_t is almost eps so predicting eps is easy, and linear has many more such t, so its average loss is lower without meaning better samples.
- Red flag: "Linear trained better because its loss is lower."

**Q7. HARD: "The handout gives you the sampling formula. Why did you clip x0? You changed my algorithm."**
- Follow-up: "Show me the evidence it was needed."
- Model answer: The step is still the handout formula; I only clamp the predicted x0 to [-1, 1] and recompute eps = (x_t - sqrt(alpha_bar) x0)/sqrt(1 - alpha_bar) before plugging it in, as the original DDPM code does. Without it the cosine model fails: alpha_999 = 0.001, so 1/sqrt(alpha_999) is about 31.6 and small eps errors explode; 62.5% of pixels end black and the mean per-pixel difference from the clipped run is 1.056. For linear (1/sqrt(alpha_999) about 1.01) the difference is only 0.051. Cell 18 runs `clip_x0=False`, the formula exactly as written, as an ablation.
- Red flag: "Clipping is standard, everyone does it." Show the ablation cell instead.

**Q8. "Why does sampling need 1000 network evaluations when training needs one?"**
- Follow-up: "Could you parallelise the 1000 steps?"
- Model answer: Training uses the closed form q(x_t | x0) to jump to a random t, and that single-t loss is an unbiased term of the full objective. At sampling x0 is unknown and each x_{t-1} depends on x_t, which came from the previous network output, so the chain is sequential and cannot be parallelised. Sampling 16 images took 15.9 s (linear) and 15.5 s (cosine).
- Red flag: "Because there are 1000 timesteps" with no mention of sequential dependence.

**Q9. HARD: "Cosine should be better from A1. Why did linear look better?"**
- Follow-up: "Is this a measurement?"
- Model answer: In my grids linear gave a better class mix (about 4-5 sandals, 7 bags, 3 trousers) with sharp straps; cosine was dominated by over-bright bag-like blobs (2 sandals, 2 trousers). The trajectories agree with A1: cosine x0-hat has an outline already near t = 900, but the model commits to a large bright shape early, and sandal straps are decided in the last low-noise steps. With 16 samples and about 16 minutes of training this is a visual judgement, not a measurement; no FID was computed.
- Red flag: Claiming cosine is "wrong" or that linear is better in general.

**Q10. "Early panels in your x0-hat trajectory are pure noise. Is your code broken?"**
- Model answer: At t near 999, x0-hat = (x_t - sqrt(1 - alpha_bar) eps)/sqrt(alpha_bar) divides a small eps error by a tiny number: 1/sqrt(alpha_bar_999) is about 157 for linear and about 20,000 for cosine, so the clamped panels are noise. That is expected, not a bug.
- Red flag: "I don't know, it just looks like that."

**Q11. "Your ViT table shows 196 after patch_embed and 197 after pos_drop. Explain."**
- Follow-up: "Why is Swin 56x56x96 after patch embedding?"
- Model answer: 224/16 = 14, so 14 x 14 = 196 patch tokens of width 768. timm then prepends the [CLS] token and adds position embeddings (in `_pos_embed`, before `pos_drop`), giving 197, which stays constant through all 12 blocks. Swin uses 4 x 4 patches: 224/4 = 56, 3,136 tokens, C = 96; patch merging then gives 28x28x192, 14x14x384, 7x7x768 (strides 4, 8, 16, 32). In timm merging sits at the start of stages 2-4, not the end as in the paper's figure.
- Red flag: Saying 197 tokens come from the patch embedding.

**Q12. "Why can Swin feed an FPN directly but ViT cannot? Parameter counts?"**
- Model answer: An FPN needs a multi-scale pyramid like ResNet's C2-C5; Swin's four stages give exactly that. ViT has one 14 x 14 x 768 map at stride 16 at every depth, and its global attention grows quadratically with image size. ViT-B/16 has 86,567,656 params, Swin-T 28,288,354.
- Red flag: "ViT has no convolutions" as the whole answer.

**Q13. HARD: "Show me your photos. Your report says 92 real photos and 8 augmented ones. The handout says 100 of your own photos."**
- Follow-up: "Where did the augmented copies go?"
- Model answer: Have the phone gallery open. Two blurry shots were removed, so 92 real photos; I topped up short classes with 8 augmented copies (flip, small rotation, crop, brightness). They are used only in training (62 real + 8 augmented = 70); the 30 test photos are all real, chosen by stratified split over real photos only, so no augmented copy of a test photo can leak.
- Red flag: Not having the originals, or not knowing the split guarantees no leakage. Admit plainly it is 92 not 100.

**Q14. HARD: "100% accuracy for both models. What does that tell me?"**
- Follow-up: "Then which backbone is better?"
- Model answer: 30/30 correct for both (confusion matrices diagonal 8/7/8/7), so accuracy cannot separate them; with 30 test photos even a perfect score is consistent with true accuracy around 0.90 (rule of three). I compared confidence instead: test log-loss 0.011 vs 0.017, mean p(true) 0.990 vs 0.985 for ViT vs Swin, a tiny gap, so they are effectively equal on my easy, distinct classes. Features are standardised then logistic regression; [CLS] for ViT, global average pool for Swin.
- Red flag: "ViT is better because it got 100%." Also: no misclassified images exist to show; say so.

**Q15. Part C on paper: "Compute Omega(MSA), Omega(W-MSA) and the ratio for your d."**
- Follow-up: "Why is the ratio not equal to the number of windows?"
- Model answer: 448/4 = 112, hw = 12,544, C = 128. Omega(MSA) = 4hwC^2 + 2(hw)^2 C = 822,083,584 + 40,282,095,616 = 41,104,179,200. Omega(W-MSA) = 822,083,584 + 2 x 49 x 12,544 x 128 = 979,435,520. Ratio about 41.97; short form (2C + hw)/(2C + M^2) = 12,800/305. Attention terms alone give hw/M^2 = 256 = number of stage-1 windows; the shared 4hwC^2 projection term pulls the full ratio down to 42. Stages: 112x112x128, 56x56x256, 28x28x512, 14x14x1024; windows 256, 64, 16, 4.
- Red flag: Unable to produce 12,800/305 without the calculator. Practise it.

---

## 2. Assignment 3 script (about 15 min)

**Q1. Opener: "Walk me through your group's work."**
- Follow-up: "Who did what?"
- Model answer: Track 3, Urdu Sentiment Corpus, Positive/Negative/Objective. 1,000 raw rows; I removed one invalid row, one duplicate and two rows with conflicting labels, giving 996 and a stratified 697/149/150 split. Two encoders (XLM-R base, MuRIL base cased) x Full FT, LoRA r8/r16/FFN, QLoRA paged/unpaged, IA3 attn/attn+FFN, two seeds, plus 25%/50% subsets: 64 runs in `results.csv`.
- Red flag: Vague "we fine-tuned some models".

**Q2. HARD (personalisation and contribution): "How did you get Track 3? And the contribution says you are the sole member and that AI was used for code, analysis and drafting. The handout says 3 to 4 students."**
- Follow-up: "So I can ask you about any line?"
- Model answer: g = 3, track = ((3 - 1) mod 4) + 1 = 3, seeds 3 and 103. I worked alone (state honestly whether this was arranged with her). Yes, I used AI assistance and declared it; I am answerable for every line and every number, ask me anything.
- Red flag: Getting defensive, or downplaying the AI disclosure you wrote yourself. Be calm and direct.

**Q3. "What cleaning did you do, and why max_length 43?"**
- Follow-up: "Define fertility and UNK rate."
- Model answer: Remove URLs and mentions, unify Arabic/Urdu yeh and kaf, collapse whitespace, deduplicate normalised text. Training-set p95 token length was 43 for XLM-R and 41 for MuRIL; I used the larger, 43, for both so length is one controlled variable. Fertility = subword tokens per word (XLM-R 1.401, MuRIL 1.313); truncation at 43 hits 4.30% and 3.01% of texts; UNK rate 0.006% vs 2.196%.
- Red flag: "Lower fertility means MuRIL is better" with no caveat about its 2.2% UNK.

**Q4. Theory: "Explain LoRA, QLoRA and IA3 in one sentence each."**
- Model answer: LoRA freezes W and learns delta W = (alpha/r) B A with B initialised to zero, rank r. QLoRA stores the frozen base in 4-bit NF4 with double quantisation, computes in FP16, and trains LoRA adapters on top. IA3 learns vectors initialised to 1 that rescale keys, values and FFN activations element-wise.
- Red flag: "QLoRA quantises the adapters." The adapters stay in higher precision.

**Q5. Open `train_group3.py`, `make_model`: "Explain this function line by line."**
- Follow-up: "Why `modules_to_save=['classifier']`? Why `llm_int8_skip_modules`?"
- Model answer: Experiments 05/06 load with `BitsAndBytesConfig(load_in_4bit, nf4, double quant, compute fp16)` and skip quantising the classifier; then `prepare_model_for_kbit_training`. LoRA targets query/value (key/value for IA3), plus `encoder.layer.N.output.dense` for 04/07b. `modules_to_save` makes the newly initialised classification head trainable, as the handout requires with SEQ_CLS. The checks raise an error if anything other than adapters and the head is trainable, or if a 4-bit base weight is trainable.
- Red flag: Not knowing what `prepare_model_for_kbit_training` does (casts norms/head to fp32, enables input grads).

**Q6. "Where does 887,811 trainable params for XLM-R LoRA r = 8 come from?"**
- Follow-up: "And MuRIL's 297,219?"
- Model answer: 12 layers x 2 modules (q, v) x r(768 + 768) = 12 x 2 x 8 x 1,536 = 294,912 adapter params, plus the XLM-R classification head (768x768 dense + 768x3 out_proj, with biases) = 592,899. MuRIL's head is a single 768x3 linear (2,307), so 294,912 + 2,307 = 297,219. r = 16 doubles the adapter part: 589,824 + 592,899 = 1,182,723.
- Red flag: "PEFT printed it." You must reconstruct it.

**Q7. HARD: "Handout says IA3 trains about 0.05%. Your XLM-R IA3 trains 611,331 of 278M, 0.22%. Explain."**
- Model answer: The IA3 vectors themselves are tiny: 12 layers x (768 key + 768 value) = 18,432, about 0.007% of 278,045,955. The rest, 592,899, is the trainable XLM-R classification head. MuRIL's 20,739 = 18,432 + 2,307. Adding FFN (07b) adds 12 x 3,072 = 36,864, giving 57,603 for MuRIL and 648,195 for XLM-R.
- Red flag: "PEFT counted it wrong."

**Q8. "Main results: RQ1. Which method gives the best trade-off?"**
- Follow-up: "How much does QLoRA save, and at what cost?"
- Model answer: On XLM-R, Full FT is best at 0.419 +/- 0.080 macro-F1 but uses 4,997 MiB. Paged QLoRA: 0.363 +/- 0.004, 943 MiB (saves 4,055 MiB, 81%) but 24.4 s vs 20.7 s, so it costs 0.056 F1 and is slower. LoRA with FFN (04) gets 0.354 at 1,429 MiB and 15.8 s. With SDs this large relative to the gaps, I would only claim Full FT is ahead; the PEFT ordering is not reliable with two seeds.
- Red flag: Ranking PEFT methods confidently by their means.

**Q9. HARD: "QLoRA saves memory, so why is it slower than LoRA (24.4 s vs 13.2 s)?"**
- Follow-up: "Why do paged on and off give identical F1?"
- Model answer: Every forward and backward pass dequantises NF4 weights to FP16 on the fly, which is extra compute; on a tiny 43-token model the overhead dominates. Paging only moves optimizer state to CPU memory when GPU memory runs out; the update math is the same and memory never ran out here, so F1 is identical (0.363) and allocation nearly identical (943 vs 947 MiB).
- Red flag: "Quantised models are always faster."

**Q10. HARD: "Every MuRIL row is 0.222 macro-F1 and 0.500 accuracy. Derive 0.222."**
- Follow-up: "Is MuRIL's tokenizer to blame?"
- Model answer: All full-data MuRIL models predict Negative for all 150 test examples (`per_class.csv`: Negative P = 0.5, R = 1.0). Negative F1 = 2(0.5)(1)/1.5 = 2/3; Positive and Objective F1 = 0; macro = (2/3)/3 = 0.222; accuracy = 75/150 = 0.500. Validation is 0.2232 for the same reason (75/149). I cannot attribute it to the tokenizer alone: MuRIL has higher UNK (2.2%), but architecture, pretraining and lr also differ; the likely cause is collapse to the majority class with 3 epochs on 697 examples.
- Red flag: "MuRIL is bad at Urdu" stated as a finding.

**Q11. HARD: "Is macro-F1 0.419 meaningful when Objective has 3 test examples?"**
- Model answer: Objective was never predicted in any of the 64 runs, so its F1 is always 0 and macro-F1 is capped near 0.667. With 3 test examples that class's F1 is extremely noisy anyway. So 0.419 is mostly the average of Positive and Negative F1 divided by 3; I report it because the handout makes macro-F1 the main metric, but I would read per-class F1 alongside it.
- Red flag: Not knowing the Objective count (14 train / 3 val / 3 test).

**Q12. HARD: "Is r = 16 worth it over r = 8? Your rank 16 is worse."**
- Model answer: On XLM-R r = 8 gave 0.328 +/- 0.108 and r = 16 gave 0.294 +/- 0.074 (difference -0.034), with 294,912 more params. But alpha was fixed at 16 by the handout, so the scaling alpha/r falls from 2 to 1: rank and update size changed together, and the gap is well inside the seed SD. So no evidence r = 16 is worth it here, and no evidence it is worse.
- Red flag: "Higher rank overfits" as a conclusion.

**Q13. "You report mean +/- SD over two seeds. What is that SD?"**
- Follow-up: "Why does LoRA-FFN have SD 0.145?"
- Model answer: Sample SD with n = 2 equals |a - b|/sqrt(2). XLM-R 04: seed 3 gave 0.456, seed 103 gave 0.252, so SD 0.145. Two seeds give a descriptive spread, not a confidence interval; seed alone moved F1 by 0.2.
- Red flag: Calling it a confidence interval or significance.

**Q14. HARD: "For RQ3 you chose configurations by validation. Why not test? And which method is most robust?"**
- Model answer: Choosing by test score would leak the test set into model selection and bias the reported number upward. Rule: highest mean validation macro-F1, ties to the first experiment (`validation_selection.json`; XLM-R picks 01, 07a, 04, 05). 25% minus 100% drops on XLM-R: Full FT -0.052, IA3 -0.026, LoRA -0.130, QLoRA -0.130. IA3 drops least, but it started low (0.242), while Full FT still has the best absolute 25% F1 (0.368).
- Red flag: "IA3 is best with little data." It degraded least from a low base.

**Q15. "Three runs had a nonfinite gradient norm. Explain."**
- Model answer: FP16 training with gradient clipping at 1.0: an overflow in one step gives an inf/NaN norm; the AMP grad scaler skips that step and lowers the scale. Flagged runs: `xlmr_04_lora_103_100` step 10, `xlmr_08_full_ft_103_025` step 10, `xlmr_08_full_ft_3_025` step 30; all finished with finite loss and weights. Separately, the first QLoRA attempt used the custom AdamW's default lr; the reported QLoRA rows use the corrected 2e-4.
- Red flag: Hiding it. You put it in the report, so own it.

---

## 3. Rapid-fire theory round (one line each)

1. **beta_t vs alpha_bar_t?** beta_t is per-step noise variance; alpha_bar_t is the product of (1 - beta) up to t, the remaining signal share.
2. **What does the DDPM network predict and what loss?** The added noise eps, trained with MSE ||eps - eps_theta(x_t, t)||^2.
3. **How does the U-Net know t?** A sinusoidal timestep embedding added into the residual blocks.
4. **Why does ViT need position embeddings?** Self-attention is permutation-invariant, so without them patch order is lost.
5. **What does Swin's shifted window do?** Shifts windows by M/2 in alternate blocks so information flows between neighbouring windows.
6. **Patch merging?** Concatenate 2x2 neighbours (4C) then linear to 2C: halves resolution, doubles channels.
7. **Why is B initialised to zero in LoRA?** So delta W = 0 at the start and training begins exactly from the pretrained model.
8. **What is NF4?** 4-bit NormalFloat, quantisation levels at quantiles of a normal distribution, suited to normally distributed weights; double quantisation also quantises the scale constants.
9. **Can LoRA and IA3 be merged after training?** Yes: W + (alpha/r)BA for LoRA, and the scaling vectors fold into the weight matrices for IA3, so inference has no extra latency.
10. **Fertility and why it matters?** Subwords per word; higher fertility means longer sequences, more truncation and more compute (attention is quadratic in length).

---

## 4. How to behave with this examiner (inferred unless marked)

- **Lead with the number, then the reason.** Her report prompts are numeric ("how much memory", "is r = 16 worth it"), so start answers with your figure. (Inferred from Seen prompts.)
- **Open the evidence file yourself.** Have the notebook, `results.json`, `results.csv`, `per_class.csv` and `validation_selection.json` open before she asks. (Inferred.)
- **Name deviations before she does:** clipped x0 (with ablation), 92 real + 8 augmented photos, sole group member, AI assistance declared. Hiding them reads as copying. (Inferred.)
- **Bring your phone with the original photos and EXIF dates.** (Seen: "the viva will check this.")
- **Do one derivation on paper without notes**, e.g. 12,800/305 = 41.97 or (2/3)/3 = 0.222. (Inferred from lecture style, which is Seen.)
- **Say "I don't know, but here is how I would find out"** rather than guessing; failure to explain is treated as plagiarism, so a wrong confident answer is worse than an honest gap. (Seen rule, inferred tactic.)
- **Do not over-claim.** 16 samples, 30 test photos, 3 Objective examples and two seeds do not support strong rankings. Say "descriptive". (Inferred.)
- **Keep answers to about 30 seconds**; she has around 15 minutes per assignment. (Seen time budget, inferred pacing.)
