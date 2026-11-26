# Assignment 3 experiment protocol

## 1. Data and tokenizer analysis

| Track | Dataset | Tasks | Train fractions |
|---|---|---|---|
| 1 | [Roman Urdu](https://huggingface.co/datasets/community-datasets/roman_urdu) | sentiment | 10%, 30%, 100% |
| 2 | [Roman Urdu hate speech](https://huggingface.co/datasets/community-datasets/roman_urdu_hate_speech) | coarse and fine; keep provided splits | 10%, 30%, 100% |
| 3 | [Urdu Sentiment Corpus](https://huggingface.co/datasets/community-datasets/urdu_sentiment_corpus) | tweet sentiment | 25%, 50%, 100% |
| 4 | [Urdu Fake News](https://huggingface.co/datasets/community-datasets/urdu_fake_news) | binary fake news | 25%, 50%, 100% |

- Record the dataset revision, fields, original counts and label names. Track 3's Hub repository has a legacy loader; inspect the dataset card and obtain a documented data file from its linked source if ordinary loading fails. Do not enable arbitrary remote Python execution just to make a dataset load.
- Track 3 verification: the [legacy loader](https://huggingface.co/datasets/community-datasets/urdu_sentiment_corpus/blob/main/urdu_sentiment_corpus.py) reads the [author's TSV](https://github.com/MuhammadYaseenKhan/Urdu-Sentiment-Corpus) and reverses each row's text. The checked TSV already stores Urdu in logical reading order, so the diagnostic uses the pinned TSV directly and preserves character order. The author file contains 1,000 records after the header, including one unlabelled/malformed record. After cleaning, one duplicate and two rows sharing identical text but conflicting labels were removed. This leaves 996 rows; the saved test split has only three Objective examples, so quote class support and avoid treating macro-F1 differences as high-confidence evidence.
- Remove null/empty rows, URLs and user mentions; for Urdu script map Arabic yeh and kaf to the corresponding Urdu forms. Normalize whitespace and drop rows left empty. Preserve meaningful punctuation and script. Audit exact duplicates before and after normalization, and log conflicting labels rather than silently choosing one.
- For tracks 1/3/4, pool the dataset rows as needed and create one fixed stratified 70/15/15 split with seed `g` after cleaning. Both training seeds use those same splits, so variability describes training rather than changes to the test set. For track 2 take the provided split membership for each task; log overlapping normalized texts and apply a documented duplicate policy that never moves examples between splits (retain the held-out copy in case of cross-split overlap). Save stable IDs and label counts.
- On training text only, calculate unpadded, untruncated lengths with special tokens for each tokenizer. Use the larger rounded-up p95 as the shared max_length across both models and all runs (both Track 2 tasks if applicable), clipping to the smaller supported model limit if needed. Document the cap and resulting truncation. Compute fertility as total subword tokens excluding special tokens divided by the number of whitespace-delimited words; UNK rate as unknown IDs divided by those subword tokens; truncation rate as fraction exceeding max_length before padding. Record the split and denominators. A two-model fertility plot is descriptive, not proof of causality.

## 2–3. Implementation and experiments

Use Hugging Face Trainer, PEFT, xlm-roberta-base and google/muril-base-cased. Fixed: 3 epochs, effective batch 16, LR 2e-5 Full FT or 2e-4 PEFT, shared maximum length and matched splits. Use FP16 for NF4 computation on T4. Save the actual microbatch and gradient accumulation steps; ideally keep both fixed within matched comparisons. Record environment and model revisions. If a run OOMs, keep its status, document the fix and rerun the comparison with an explicit memory policy.

| Exp | Concrete queue row | Comparison |
|---|---|---|
| 01 | Full FT | baseline |
| 02 | LoRA rank 8, alpha 16, query/value | versus 03 |
| 03 | LoRA rank 16, alpha 16, query/value | rank-16 attention-only control for 04 |
| 04 | LoRA rank 16, alpha 16, query/value plus an FFN projection | versus 03 |
| 05 | QLoRA rank 16, NF4 + double quantization, paged AdamW | versus 06 |
| 06 | same QLoRA settings with equivalent non-paged AdamW | versus 05 |
| 07a | IA³ key/value only | versus 07b |
| 07b | IA³ key/value + FFN output projection, marked as feedforward in PEFT | versus 07a |
| 08 | per model/task/method, pick best full-data configuration by mean validation macro-F1; rerun it on smaller fractions at both seeds | reuse the exact full-data runs as 100% |

- Inspect model module names before setting targets. Do not match a generic `dense` suffix that unintentionally selects attention projections or the classifier. Log the exact matched modules. For 05/06 keep the same targets and alpha, ideally matching 03 so the LoRA vs QLoRA memory comparison is easier to interpret; keep optimizer state precision matched between 05 and 06. Rank at fixed alpha also changes alpha/r, so mention that when interpreting 02 vs 03.
- Confirm PEFT adapters and the classification head are trainable, including IA³. Verify QLoRA order: load with BitsAndBytesConfig then prepare_model_for_kbit_training then add LoRA. Check that the quantized base stays frozen. Record trainable parameter counts without treating packed 4-bit storage size as the logical number of weights.
- Smoke-test one forward/backward batch per method on both encoders, with the same input shapes as the full run. Check finite loss, logits shape, labels, trainable names, GPU type and ability to save/reload. Only full 3-epoch runs count in the results.
- Freeze validation winners before looking at test results. Use the same nested stratified subsets per task and seed across encoders/methods, from the training split only. Save subset IDs/counts and ensure rare labels are represented when feasible. Hold validation/test fixed. Use both seeds, and report sample SD (ddof=1), labelled as such; two seeds describe variability but are not evidence of statistical significance.
- Run comparisons in isolated Colab processes or sessions so memory readings are attributable. Reset CUDA peak after model load, before training; synchronize around timing and record peak allocated bytes over the same training window (including validation only if done within that window in every run). Record GPU, time in seconds and peak in MiB. Measure final test outside the timing window. Log failed/OOM runs distinctly rather than recording zeros.

There are 32 full-data jobs and 32 reduced-data jobs per task, for 64 distinct runs (128 for Track 2). Exp 03 supplies the control for Exp 04. The 100% point in Exp 08 references existing runs, not new jobs. For a group of 3–4, distribute queue entries by encoder or method. Run paged/non-paged pairs on comparable T4 environments to reduce resource-comparison noise. Long tracks may require multiple sessions; back up evidence after each job.

## Evidence to retain

One row per run: group, track, task, experiment, model and revision, seed, method, data fraction and count, subset hash, epochs, max_length, microbatch, accumulation, LR, adapter rank/alpha/targets, NF4/double-quantization, optimizer, GPU and package versions, validation macro-F1, test macro-F1, test accuracy, wall seconds, peak allocated bytes, trainable params and status. Keep split IDs, per-run configs and logs, validation selection and raw test predictions separately. Do not put raw tweets or credentials in a public repository.

Before packaging: check both seeds and models for every condition; verify the fixed settings, clean split isolation, subset coverage, trainable layers, and metrics against the recorded predictions. Commit to one reporting convention and preserve the underlying run rows for both successes and failures.
