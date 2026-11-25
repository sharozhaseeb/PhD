# Viva prep: GenAI Assignments 2 and 3

Use this order. It fits in about 1.5 hours.

1. **Watch the video:** `video/out/GenAI_A2_A3_Viva_Walkthrough.mp4`. It is about 39 minutes (about 31 at 1.25×). Chapters are in `video/out/chapters.txt`, and the full narration is in `video/out/transcript.txt`.
2. **Do a mock viva out loud:** `VIVA_EXAMINER_SCRIPT.md`. It has 15 questions per assignment, each with a follow-up, a model answer and a "red flag" answer to avoid, plus a rapid-fire round.
3. **Memorise the numbers and code lines:** `TPM_RISK_REGISTER.md`, sections 2 and 3.
4. **Decide your three honest answers before you walk in.** See below and the TPM register's section 4.

## Three honest answers to decide now

1. **A3 group:** the handout requires a registered group of 3–4. Your report lists you as the only member, and the submitted README still says to confirm the solo exception. Know exactly what you will say about your group number, and whether working alone was agreed with the instructor.
2. **AI use:** the A3 report discloses AI help with code, analysis and drafting; the handout allows it for debugging only. Keep what you say consistent with what you wrote, and show ownership by explaining the code fluently.
3. **Unusual items:** raise these yourself.
   - **A2:** the x̂0 clipping (plus its `clip_x0=False` ablation), and the 8 augmented photos, which are used only for training.
   - **A3:** the MuRIL collapse (its cause was never diagnosed), the QLoRA learning-rate fix and rerun in notebook cells 10–11, and the training code stored compressed in cell 1 (open `source/train_group3.py` instead).

## Ten numbers to say without looking

| | |
|---|---|
| A2 d = 5 | Sandal / Bag / Trouser; Part C: 448×448, C = 128 |
| A1 | ᾱ < 0.5 at t = 259 (linear) vs 496 (cosine) |
| A2 | 28 epochs, LR 5e-4, batch 128, ~16 min/model, U-Net 3,939,393 params |
| A3 (DDPM) | clipping needed: β999 = 0.999 → 1/√α ≈ 31.6; unclipped cosine 62% black pixels |
| B1 | ViT 196 → 197 tokens, 86.6 M; Swin 56→28→14→7, 96→768, 28.3 M |
| B2 | both 30/30; log-loss ViT 0.011 vs Swin 0.017 → tie |
| C | Ω ratio 12,800/305 ≈ 41.97; windows 256/64/16/4 |
| A3 data | 996 rows, 697/149/150, max_length 43, test has only 3 Objective |
| A3 XLM-R | Full FT 0.419 (4,997 MiB) · QLoRA 0.363 (943 MiB) · LoRA r8 0.328 / r16 0.294 / +FFN 0.354 · IA3 ≈ 0.24 |
| A3 MuRIL | 0.222 = (2/3)/3, always predicts Negative |
