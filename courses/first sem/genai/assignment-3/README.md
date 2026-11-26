# Advanced GenAI Assignment 3 — preparation and run plan

The task is Urdu or Roman Urdu classification with Full Fine-Tuning, LoRA, QLoRA and IA³ on XLM-R and MuRIL. This folder prepares a solo run under the **working assumption of group 3**: Track 3, Urdu tweet sentiment, seeds 3 and 103. The instructor must confirm the solo exception and group number before submission. There are no trained-model scores, executed training notebooks or final report yet.

1. Start with [the group 3 run list](group3_run_plan.json): 32 full-data and 32 reduced-data runs. Entries marked `pending_validation_selection` require a method configuration selected from measured validation results. If the instructor assigns a different number, regenerate the plan with `python run_plan.py GROUP_NUMBER`; do not keep the group 3 splits or seeds.
2. Check [the Track 3 audit](track3_preflight.json). Run `python track3_preflight.py` with scikit-learn installed to reproduce the cleaned row counts and fixed split IDs. Add `--tokenizers` in an environment with Transformers and its dependencies to audit the pretrained tokenizers without model weights.
3. Follow [the experiment protocol](EXPERIMENT_PROTOCOL.md). Start on Colab T4 with one smoke batch per encoder and fine-tuning method, then start the full-data queue. Save each completed run separately so one runtime disconnect does not erase progress.
4. Use [the report outline](REPORT_OUTLINE.md) after training. Report only real work in the contribution statement, with the approved solo arrangement if applicable. Save and understand the specific validation and test evidence used to answer RQ1–RQ3.

### Measured preprocessing

The pinned author release yielded 996 cleaned rows: 697 training, 149 validation and 150 test. The audit stores exact split IDs and both seeds' nested 25%/50% training IDs.

| Tokenizer | Fertility | p95 length | Truncated at shared length 43 | UNK rate |
|---|---:|---:|---:|---:|
| XLM-R | 1.401 | 43 | 4.30% | 0.006% |
| MuRIL | 1.313 | 41 | 3.01% | 2.196% |

These are measured on the training split. MuRIL splits it into fewer subwords but also emits more UNK tokens. That makes it premature to infer better classification or speed from fertility alone.

No group registration, sharing, or submission was done.

### Colab execution

Open [Group3_Colab.ipynb](Group3_Colab.ipynb) on a T4. Its initial cells set up the environment and run eight short checks. Training is opt-in; use a mounted Drive evidence path before setting `RUN_FULL=True`. The runner is also readable as `train_group3.py`; `collect_results.py` verifies all 64 completed jobs, chooses by mean validation macro-F1, and computes held-out metrics from the prediction files. Report the final epoch of fixed three-epoch runs. If selecting the best epoch instead, change the protocol before full runs and use it everywhere.

Each job uses a fresh Python process; a completed result is written last. An interrupted job can restart safely, and completed jobs are skipped. If a smoke run hits OOM, choose a smaller common microbatch and run the smoke checks again in a new evidence directory. Runs sharing the same settings remain comparable; GPU allocation, dependency and runtime checks must still pass.
