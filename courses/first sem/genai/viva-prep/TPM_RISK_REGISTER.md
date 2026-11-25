# TPM Risk Register: A2 + A3 Viva (26L-9005)

Checked against: A2 `outputs/results.json`, A2 report PDF, A2 notebook code; A3 `summary.csv`, `results.csv` (64 rows), `per_class.csv`, `validation_selection.json`, report PDF, `source/*.py`, executed notebook outputs; both handouts.

**Bottom line:** the numbers are internally consistent. No report-vs-data mismatch was found. The main risks are about **process and honesty**, not arithmetic: (1) A3 solo/group status, (2) the A3 AI-use disclosure goes beyond the handout's "debugging only" rule, (3) A3 code is heavily engineered and hidden in a compressed blob in the notebook, and (4) explaining why MuRIL collapsed.

---

## 1. Top 10 risks (ranked by likelihood x damage)

| # | Risk | Likely question | Where to point | Honest answer (2-3 sentences) |
|---|---|---|---|---|
| 1 | **A3 group status.** The handout requires a registered group of 3-4 members, with g taken from the sheet. The submission says "sole group member"; the preflight says `"group_working_assumption": 3`; notebook cell 0 says "Provisional Group 3"; the README still contains the note "Confirm the solo exception and group number with the instructor before submitting". | "Which group are you? Who allowed you to work alone? Why Track 3?" | Report p6 contribution line; `README.md` last paragraph; `track3_preflight.py` report dict | State the facts only. Either "I was given permission on <date> by <who>" **or** "I did not get a group; I worked alone and assumed group 3, so track 3 and seeds 3/103." Do not claim you were registered as Group 3 unless you were. If you never confirmed it, say so and offer to redo it with whatever group number she assigns. **Decide your answer before the viva.** |
| 2 | **AI-use disclosure vs policy.** The handout allows AI "for debugging" only. The A3 report says AI was used "for code, experiment operation, analysis and drafting." | "You wrote AI did the code and the drafting. What did *you* do?" | Report p6 last line | Do not retract the disclosure. Say: "I disclosed it fully. I designed the protocol, ran it, and can explain every line." Then prove it by walking through `make_model` and the selection rule without notes. The penalty is for code you cannot explain, so fluency is the defence. **A2: check that your A2 position on AI use matches A3. A different story for each assignment is worse than either story.** |
| 3 | **A3 notebook hides code.** Cell 1 is a zlib+base64 blob that unpacks `train_group3.py` and the other scripts. Cells 10-11 show a crash and a "recovery" wrapper. | "Where is your training code? Why compress it? What is run_recovery?" | Notebook cells 1, 10, 11; `source/train_group3.py`; `source/run_recovery.py` | "The blob is the same files as `source/`, packed so one Colab cell recreates them. It is not obfuscation." Cell 10 crashed because a NaN grad-norm could not be written to strict JSON (`allow_nan=False`). Also, the QLoRA `optimizer_cls_and_kwargs` had no `lr`, so bnb AdamW silently used its default LR. The wrapper injects `lr=args.learning_rate` and stores the NaN grad-norm as `null` with a flag. The 3 affected QLoRA runs and 4 smoke runs were archived and rerun. Nothing was hidden: all of this is in the README. |
| 4 | **MuRIL collapsed.** Every full-data MuRIL run predicts "Negative" for every test example (F1 0.222, acc 0.500, SD 0). | "Is your MuRIL code broken? Why is the SD zero? Why didn't you fix it?" | `summary.csv` MuRIL rows; validation 0.2232 in every MuRIL run | Same code path as XLM-R, which did learn, so the pipeline works. With 3 epochs (132 optimizer steps), fixed LRs and a tiny dataset, MuRIL never left the majority class. Its loss stayed around 1.07, close to ln 3 = 1.10. The handout fixes the LR and epochs, so I did not tune them. Likely causes are too few steps, the LR, and the 2.2% UNK rate. **I did not diagnose it further.** SD = 0 because both seeds produce the identical constant prediction. Majority-class macro-F1 = (0 + 2·75/(75+150) + 0)/3 = 0.667/3 = 0.222. |
| 5 | **A2 x0-hat clipping is not the handout formula.** | "The handout gives the formula. Why did you change it?" | Notebook cell 23 `ddpm_sample` (`clip_x0`); cell 26 ablation; results `cosine_no_clip_black_fraction 0.625` | The reverse-step formula itself is unchanged. I clamp x0-hat to [-1,1] and recompute the ε that matches it, as the original DDPM code does. Without clipping, cosine β_999 = 0.999 gives 1/√α_999 ≈ 31.6, so errors blow up (std of x_998 = 1.59 against about 1 in training) and 62.5% of pixels end black. Linear without clipping changes only 0.051 per pixel. `clip_x0=False` runs the handout formula exactly, and that ablation is in the notebook. |
| 6 | **A2 photos: 92 real + 8 augmented.** The handout requires 100 of your own photos. | "Are these your photos? Show me. Why 8 augmented? The code asserts 25 per class." | Cell 30 assert (counts files incl. `_aug`); cell 42 split; collage figure | "92 are my own phone photos. I removed 2 blurry shots and topped up the short classes with 8 flipped/rotated/cropped copies, which go **only** into training (`assert not is_aug[TEST_IDX].any()`)." Have the originals on your phone with EXIF dates ready to show. Say plainly that you have 92 real photos, not 100. |
| 7 | **A3 QLoRA memory saving looks small** (943 vs 1385 MiB for LoRA r16). Also 05 and 06 give identical F1. | "Why does 4-bit save only 442 MiB? Is the paged run the same run?" | `summary.csv` rows 05/06/03 | bnb quantises only `nn.Linear`. The 250k-token word embedding (≈192M params, ≈733 MiB fp32) stays full precision, and `prepare_model_for_kbit_training` casts the other non-quantised params to fp32. Paging only moves optimizer state to CPU under memory pressure. With no pressure on a T4 the computation is identical and deterministic under the same seed, so F1 is identical; the 4.6 MiB difference is allocator noise. |
| 8 | **RQ3 conclusion "IA3 degrades least" is shaky.** IA3 is already close to the majority baseline at 100% (0.242), so it has little to lose. | "Is IA3 really most robust?" | Report p6 RQ3; summary 08 rows | "By the stated measure, yes (-0.026). But IA3 was near the floor already. Full FT keeps the highest absolute F1 at every size (0.368/0.393/0.419), so in practice Full FT is the most robust here." Concede the caveat; do not defend the headline. |
| 9 | **High variance and only 2 seeds.** XLM-R LoRA 04 0.354 ± 0.145; the LoRA 04 selection was driven by seed 3 alone (val 0.427 vs 0.244). Objective has F1 = 0 in all 64 runs (3 test examples). | "Is r=16 better than r=8? Is FFN placement better?" | `validation_selection.json`; per_class.csv | "The differences (-0.034 for rank, +0.060 for FFN) are well inside one SD with n=2, so they are descriptive, not significant." With fixed α=16, r=8 has scale α/r = 2 and r=16 has scale 1, so rank and scaling are confounded. Objective has 14 train / 3 test examples and no class weighting, so no model learns it. |
| 10 | **A2 "which schedule looks better" vs A1 theory.** | "Cosine should be better. Why is linear better?" | Report A3 comparison; trajectory figures | "In A1, cosine destroys information more slowly, and the trajectory confirms it: the cosine x0-hat has an outline at t≈900. That did not give better samples: the cosine grid is dominated by over-bright bags. With 16 samples and 16 min of training this is a visual judgement, not a measurement (no FID)." The losses are not comparable (0.028 vs 0.050) because the same t means a different noise level under each schedule. |

**Lower-ranked but prepare:** the A3 data came from the author's GitHub TSV (pinned commit + SHA256), not HF `community-datasets/urdu_sentiment_corpus`. Answer: "same corpus; HF's script loads this file; I pinned it for reproducibility." The A2 LR of 5e-4 is above the usual 2e-4 because training was only about 15 minutes. A2 epochs were chosen by `choose_epochs` timing 30 steps.

---

## 2. Numbers to memorise (verified against data files)

### A2 (results.json = report; no mismatches)
| Item | Value |
|---|---|
| d / classes / seed | 5 / Sandal(5), Bag(8), Trouser(1) / 9005 |
| Train images, batch, steps/epoch | 18,000, 128, 140 (drop last partial) |
| Epochs, steps, LR, opt | 28, 3,920, 5e-4, AdamW fp32 |
| U-Net params | 3,939,393 |
| Train time linear / cosine | 975.6 s (16.3 min) / 999.5 s (16.7 min) |
| Last-epoch loss linear / cosine | 0.0280 / 0.0502 |
| ᾱ_500 linear / cosine | 0.078 / 0.492 |
| First t with ᾱ<0.5 | linear 259, cosine 496 |
| First t with ᾱ<0.01 | linear 673, cosine 935 (so about 33% of linear t are pure noise) |
| Sampling (16 imgs, 1000 NFE) | linear 15.95 s, cosine 15.54 s |
| No-clip diff linear / cosine | 0.0507 / 1.0557 per pixel; cosine 62.5% black; x_998 std 1.59 |
| 1/√α_999 | cosine 31.6, linear ≈1.01; 1/√ᾱ_999 ≈157 linear, ≈20,000 cosine |
| ViT-B/16 / Swin-T params | 86,567,656 / 28,288,354 (features_only 27,517,818) |
| ViT tokens | 196 after patch_embed, 197 with [CLS], 768 ch, stride 16 throughout |
| Swin stages | 56²×96 (s4), 28²×192 (s8), 14²×384 (s16), 7²×768 (s32) |
| Probe split | 70 train (62 real + 8 aug) / 30 test real (8,7,8,7) |
| Probe ViT / Swin | acc 1.0 both; log-loss 0.0113 / 0.0168; p(true) 0.990 / 0.985 |
| Part C | 448→112×112×128; 56²×256; 28²×512; 14²×1024; windows 256/64/16/4 |
| Ω(MSA) / Ω(W-MSA) / ratio | 41,104,179,200 / 979,435,520 / 41.97 = (256+12,544)/(256+49) |

### A3 (summary.csv = report tables; all report deltas re-derived and they match)
| Item | Value |
|---|---|
| Rows | 1,000 raw → 996 (1 invalid, 1 duplicate, 2 conflicting-label rows) |
| Split (P/N/O) | train 697 (335/348/14), val 149 (71/75/3), test 150 (72/75/3); split seed 3 |
| Tokenizer XLM-R / MuRIL | fertility 1.401 / 1.313; p95 43 / 41; truncated 4.30% / 3.01%; UNK 0.006% / 2.196% |
| max_length | 43 (larger p95) |
| Training | 3 epochs, microbatch 8 × accum 2 = 16, 44 steps/epoch = 132 steps; fp16; linear decay, no warmup, clip 1.0 |
| LR | 2e-5 Full FT, 2e-4 PEFT |
| XLM-R Full FT | **0.419 ± 0.080**, acc 0.643, 20.7 s, **4,997 MiB**, 278,045,955 params |
| XLM-R LoRA 02/03/04 | 0.328 / 0.294 / 0.354; 1,380/1,385/1,429 MiB; 887,811 / 1,182,723 / 1,920,003 |
| XLM-R QLoRA 05/06 | **0.363 ± 0.004** both; **943** / 947 MiB; 24.4 / 24.2 s |
| XLM-R IA3 07a/07b | 0.242 / 0.247; 611,331 / 648,195 params |
| MuRIL (all full-data) | 0.222 / 0.500; Full FT 237,558,531 params, 4,225 MiB; QLoRA 778 MiB; IA3 07a 20,739 |
| QLoRA vs Full FT | saves 4,055 MiB (81%), costs 0.056 F1, 3.7 s slower |
| QLoRA vs LoRA 03 | -442 MiB, +0.069 F1 |
| RQ3 XLM-R 25% - 100% | Full FT -0.052, IA3 -0.026, LoRA -0.130, QLoRA -0.130 |
| Selection | best mean **validation** macro-F1, ties → first exp (XLM-R: 01, 07a, 04, 05) |
| Nonfinite grad-norm runs | xlmr_04_lora_103_100 (step 10), xlmr_08_full_ft_103_025 (step 10), xlmr_08_full_ft_3_025 (step 30) |

**Param-count derivations (a likely question):**
- XLM-R classification head = 768×768+768 + 768×3+3 = **592,899**. MuRIL (BERT) head = 768×3+3 = **2,307**.
- LoRA r8 on q,v: 12 layers × 2 × 8×(768+768) = 294,912. This gives 887,811 (XLM-R) and 297,219 (MuRIL). r16 is double: 589,824.
- LoRA 04 adds `output.dense` (3072→768), r16: 12×16×(3072+768) = 737,280.
- IA3 07a: k,v vectors 12×2×768 = 18,432 (+ head). 07b adds FFN vectors on the 3072-d input of `output.dense`: 12×3072 = 36,864.
- XLM-R is 278M parameters mostly because of its 250k-token vocabulary embedding (≈192M).
- Full FT memory ≈ 16 bytes/param (fp32 weight + grad + 2 Adam states) ≈ 4.2 GiB + activations, which matches 4,997 MiB.

---

## 3. Code the examiner may point at

### A2 (`26L-9005_A2.ipynb`)
| Cell | Line(s) | One-line explanation |
|---|---|---|
| 10 | `cosine_betas`: `f = cos(((t/T)+s)/(1+s)·π/2)²`, `alpha_bar = f/f[0]`, `betas = 1 - ab[1:]/ab[:-1]`, `.clamp(max=0.999)` | Nichol-Dhariwal; s=0.008 stops β being too small near t=0; the clamp prevents β=1 at t=999 (ᾱ_T=0). |
| 10 | `Schedule`: `alpha_bars = cumprod(alphas)` | ᾱ recomputed from the clipped β, so the two are consistent. |
| 10 | `q_sample`: `abar.view(-1,1,1,1)`; `abar.sqrt()*x0 + (1-abar).sqrt()*eps` | Closed-form q(x_t\|x_0); view broadcasts one ᾱ per image over the pixels. |
| 7 | `F.pad(x,(2,2,2,2))`, `x*2-1` | 28→32 so the U-Net can halve twice (32→16→8); scale to [-1,1] to match the N(0,1) noise scale. |
| 15 | `AttnDownBlock2D` only last, `AttnUpBlock2D` first | Attention only at 8×8, which is cheap (64 tokens). |
| 16 | `train_step` 5 lines | Uniform t, ε, x_t, predict ε, MSE; one network call per step. |
| 16 | `choose_epochs` | Times 30 steps after warm-up and `cuda.synchronize()`, then sizes epochs to about 15 min. |
| 17 | `range(0, len-BATCH+1, BATCH)`, `set_seed(SEED)` | Drops the partial batch; same init and data order for both schedules. |
| 23 | `x0_hat = (x-√(1-ᾱ)ε)/√ᾱ`; `clamp(-1,1)`; `eps = (x-√ᾱ·x0_hat)/√(1-ᾱ)` | Clip x0-hat, then the ε consistent with it. |
| 23 | `mean = (x - β/√(1-ᾱ)·ε)/√α`; `x = mean + √β·z` if t>0 | The handout formula, with σ_t²=β_t and no noise at the last step. |
| 26 | manual x_999→x_998 | Shows the 31.6× amplification without clipping. |
| 34 | `register_forward_hook(hook)` with `name=name` default arg; `h.remove()` | The default arg captures each name (avoids the late-binding closure bug); handles are removed so later runs are clean. |
| 34 | `pos_drop` = 197 tokens | Runs after [CLS] and the position embedding are added. |
| 41 | `out[:,0]` vs `out.mean(dim=(1,2))` | ViT [CLS] from (B,197,768); Swin GAP over (B,7,7,768) NHWC. |
| 42 | `is_aug`, split on `real_idx` only, `TRAIN_IDX = concat(train_real, aug_idx)` | Prevents leakage from augmented copies of test photos. |
| 42 | `make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))` | The scaler is fit on train only, inside the pipeline. |
| 48 | `proj = 4·hw·C²`; `msa = proj + 2·hw²·C`; `wmsa = proj + 2·M²·hw·C` | Swin paper Eq. (1)/(2). |

### A3 (`source/train_group3.py`, ≈330 lines)
| Location | Code | One-line explanation |
|---|---|---|
| `target_names` (~l.55) | `("key","value") if exp.startswith("07") else ("query","value")`; regex `encoder.layer.N.output.dense` | Finds module names by printing `named_modules()`. LoRA uses q,v; IA3 uses k,v; FFN = output.dense. Asserts 24 attention + 12 FFN modules. |
| `make_model` (~l.67) | `BitsAndBytesConfig(load_in_4bit, nf4, double_quant, compute_dtype=float16, llm_int8_skip_modules=["classifier"])` | NF4 base weights; double quant also quantises the scale constants; fp16 compute because the T4 lacks bf16; the head stays unquantised so it can train. |
| same | `prepare_model_for_kbit_training(model, use_gradient_checkpointing=False)` | Freezes the base, casts non-quantised params (LayerNorm etc.) to fp32 for stability, enables input grads. |
| same | `common = dict(task_type="SEQ_CLS", target_modules=..., modules_to_save=["classifier"])` | SEQ_CLS makes PEFT keep the classification head trainable and saved. |
| same | `IA3Config(**common, feedforward_modules=ffn)` | IA3 scales the **input** of modules listed as feedforward and the **output** of the others (k,v). Vectors start at 1. |
| same | `LoraConfig(r=8 if exp=="02" else 16, lora_alpha=16, lora_dropout=0.0, bias="none")` | ΔW = (α/r)·B·A, with B initialised to 0 so training starts at the pretrained model. |
| same | `Params4bit` requires_grad check | Asserts no packed 4-bit weight is trainable. |
| `run` (~l.205) | `bnb AdamW optim_bits=32, is_paged = exp=="05"` | 05 = paged, 06 = unpaged (the only difference). |
| `run` | `gradient_accumulation_steps=16//microbatch` | 8×2 = effective batch 16. |
| `run` | `torch.cuda.synchronize(); reset_peak_memory_stats(); ... max_memory_allocated()` | Peak *allocated* (not reserved) memory measured over training only; synchronize so timing is accurate. |
| `run` | `eval_strategy="no", save_strategy="no"` + "Final epoch only" | No early stopping and no test-based selection. |
| `export_predictions` | writes val + test predictions; the selector reads validation only | Test metrics are computed afterwards in `collect_results.py`. |
| `score` | `f1_score(..., average="macro", labels=range(3), zero_division=0)` | Includes Objective even when it is never predicted, which is why it scores 0. |
| `track3_preflight.py clean()` | URL / @mention regex; `ي→ی`, `ك→ک` | Arabic yeh/kaf unified to the Urdu forms. |
| preflight | two `train_test_split(..., stratify)`, 0.30 then 0.5, random_state=3 | 70/15/15 stratified. Reduced subsets are nested (25% ⊂ 50%) per seed. |
| `run_recovery.py` | `RepairedTrainer` injects `lr`; `write_json` NaN→null | See risk 3. |

---

## 4. Honesty traps (state plainly, do not over-claim)

1. **Group/solo (A3):** say exactly what happened. If no instructor permission exists, do not imply it. "Group 3" was a working assumption (the code itself says `group_working_assumption`).
2. **AI use:** the A3 report discloses AI for code, operation, analysis and drafting. Stand by the disclosure; do not minimise it to "debugging only". Make sure your A2 account of AI use is consistent with it. Expect "explain this line" drilling on anything engineered: SHA checks, bundle hash, `smoke_reload`.
3. **Recovery/reruns (A3):** first QLoRA runs used the bnb default LR (bug). Cell 10 crashed on a NaN grad-norm. Superseded runs were archived and redone at 2e-4. Three runs carry a flagged nonfinite grad-norm but finished with finite loss. Say: "a bug, found, fixed, rerun, disclosed."
4. **MuRIL:** "it collapsed to the majority class; I did not find the cause." Do not claim it was the tokenizer.
5. **Augmented photos (A2):** 92 real, 8 augmented, train-only. Not 100 real.
6. **x0 clipping (A2):** a deliberate, ablated deviation from the literal sampler. The formula is unchanged and `clip_x0=False` reproduces the handout exactly.
7. **"Linear looks better" and "IA3 most robust":** both are qualitative or small-n. Say "descriptive, 16 samples / 2 seeds".
8. **A3 Objective class:** 0 F1 everywhere. Do not describe the models as 3-class classifiers in any real sense.
9. **A3 data source:** GitHub author TSV pinned by SHA, not the HF loader. Same corpus.
