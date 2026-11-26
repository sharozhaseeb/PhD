# A3 Viva — Questions & Answers (quick reference)

> Group 3 · Track 3 (Urdu Sentiment Corpus) · seeds 3 & 103 · XLM-R base + MuRIL base
> Key numbers: 996 tweets → 697 / 149 / 150 · max_length 43 · Full FT 0.419 F1 · QLoRA 943 MiB · MuRIL 0.222

---

## 1. The tweets — what is the dataset?
- **1,000 Urdu-script tweets**, labelled Positive / Negative / Objective. The author's TSV is pinned by commit + SHA-256.
- Removed: 1 malformed, 1 duplicate, 2 conflicting (same text, different label) → **996**.
- Cleaning: remove URLs and @mentions, unify yeh/kaf, collapse spaces. **Dedup on the cleaned text.**
- **Stratified 70/15/15** split, seed 3 → **697 / 149 / 150**. Objective is tiny: **14 / 3 / 3**.
- *Why dedup after cleaning?* Tweets that differ only by a link are the same input.
- *Why stratify?* So the ~2% Objective class appears in every split.
- *Why macro-F1?* Accuracy would hide a model that ignores Objective (only 3 of 150 test tweets).

## 2. What does the tokenizer do?
- It turns text into **ids** from a fixed vocabulary of **subword pieces**.
- Common words stay whole; rare words split into known pieces.
- **XLM-R:** SentencePiece unigram, ~250k pieces (multilingual). **MuRIL:** WordPiece (`##` = continuation), built for Indian languages.
- The vocabularies differ because each is learned from its own model's pre-training text.
- Ours: 12,208 training words → **17,105** pieces (XLM-R) vs **16,029** (MuRIL).
- *Why not whole words?* The vocabulary would be huge, and unseen words would be lost.
- *Swap tokenizers?* No. Each model only knows embeddings for its own ids.

## 3. UNK token rate
- **UNK** = the token used when the vocabulary can't represent the text. The content behind it is **lost**.
- Rate = UNK tokens ÷ all subword tokens (training split, no special tokens).
- **XLM-R: 1 / 17,105 (0.006%)** · **MuRIL: 352 / 16,029 (2.196%)**.
- *Lower fertility but more UNKs?* In WordPiece one UNK can replace a **whole word**, and it counts as one piece.
- *Did UNKs cause MuRIL's poor result?* **Not shown.** It's an association; MuRIL also differs in architecture and pre-training.
- *Which words were UNK?* Not recorded; we only counted them.

## 4. Fertility
- **Fertility = subword tokens per word** (total ÷ total, no special tokens).
- **XLM-R 17,105 ÷ 12,208 = 1.401** · **MuRIL 16,029 ÷ 12,208 = 1.313**.
- Higher fertility → longer inputs → more compute (attention ∝ length²) and more truncation.
- **Lower isn't automatically better:** MuRIL is lower but has a 2.2% UNK rate, so part of its shorter count is lost information.
- *RQ2?* MuRIL had lower fertility yet only **0.222** F1 vs XLM-R **0.419**. With two models, that's an association, not a cause.
- *Why exclude special tokens?* Every tweet gets them; they say nothing about Urdu.

## 5. What is the token length (max_length) for?
- **max_length** = the longest input the model sees; longer tweets are **truncated** (cut at the end).
- Trade-off: longer = more memory/compute; shorter = more text lost.
- Chose **43** = the larger **95th percentile, nearest rank** (position 663 of 697) of training token lengths: XLM-R 43, MuRIL 41.
- Truncation at 43: **XLM-R 4.30%** · **MuRIL 3.01%**. **Dynamic padding** per batch.
- The same 43 for both models keeps the comparison fair.
- *Why not 41?* It would cut more XLM-R tweets; 43 covers 95% for both.
- *Why the training split only?* max_length is a modelling choice; using validation/test data would **leak** information.

## 6. Main results
| XLM-R, 100% data | Macro-F1 | Peak memory | Note |
|---|---|---|---|
| Full FT | **0.419** (best) | 4,997 MiB | most accurate, most memory |
| QLoRA | 0.363 (−0.056) | **943 MiB** (−81%) | slowest, 24.4 s (dequantises every pass) |
| LoRA / IA3 | in between | in between | dominated by QLoRA on memory |
- **Rank 16 vs 8:** −0.034, inside the seed spread, so not better.
- **MuRIL:** predicts Negative for everything → **0.222** for all methods.
- **RQ3 (less data):** IA3 dropped least (−0.026) but from a low base; **Full FT is best at every size**.
- **Which to choose:** memory-bound → **QLoRA**; ~5 GB available and you want the best score → **Full FT**.
- *Why macro-F1?* MuRIL gets **0.500 accuracy** but **0.222 macro-F1**; accuracy hides the collapse.
- *How were the RQ3 configs chosen?* Best mean **validation** macro-F1, never test.
- *Significant?* With 2 seeds the results are descriptive, not tested.

## 7. Who did what?
- Group 3 has **one member: Sharoz Haseeb, 26L-9005**.
- The report states: *"AI assistance was used for code, experiment operation, analysis and drafting."*
- Handout (p. 1): assistants are allowed, but code/text you **can't explain** counts as plagiarism.
- **Own every decision.** Offer to explain any part or any line.
- *Did you write all the code?* Answer honestly and consistently with the report: "Not every line unaided, but I can explain any of it." Then walk through one part (e.g. dedup on cleaned text, max_length 43, validation-only selection).
