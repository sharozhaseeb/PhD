# Advanced GenAI Assignment 3 — Group 3

Sharoz Haseeb (26L-9005) · Track 3 Urdu tweet sentiment · Seeds 3 and 103

- `Group3_Assignment3_Report.pdf` contains the six-page comparison.
- `Group3_Colab_Executed.ipynb` contains the original executed T4 notebook and its saved outputs. Cell 10 records an interrupted attempt. Cell 11 archives the superseded attempts, verifies the corrected QLoRA learning rate in four smoke runs, and finishes the roster. Its last output confirms 64 completed runs and 32 paired summaries.
- `results.csv` contains all 64 configurations and seeds. `summary.csv` has the 32 paired rows. `validation_selection.json` gives validation scores and the tie rule. `per_class.csv` gives test support, precision, recall and F1 per run.
- `figures/` contains the five report plots. `Group3_T4_Complete_Evidence.zip` is the original runtime export with run configurations, logs, parameter audits, and validation and test predictions by source row ID. The ten smoke runs are under `smoke/`. The three-epoch pilot is the official XLM-R Full FT run with seed 3.
- `source/` contains the exact bootstrap bundle unpacked from the notebook, the recovery wrapper extracted from Cell 11, and the figure and report builders.

## Verify or reproduce

The executed notebook can be read without a runtime. For local verification, extract the evidence archive into a directory and run `python source/collect_results.py EVIDENCE_DIR` from the package root with scikit-learn installed. Use `python source/make_figures.py EVIDENCE_DIR` to regenerate the figures.

For a fresh T4 run, use an empty evidence directory, the pinned runtime dependencies and the source files from this package. Install `source/colab_requirements.txt` in a Colab T4 environment. Invoke `python source/run_recovery.py JOB_ID --output EVIDENCE_DIR --microbatch 8` for the jobs in `group3_run_plan.json`. Run the 32 full-data jobs first, run `collect_results.py EVIDENCE_DIR --select-only`, then run the 32 experiment 08 jobs before final aggregation. `run_recovery.py` supplies the intended optimizer learning rate and retains flags for nonfinite logged gradient norms. The historical notebook documents the actual execution sequence, including the interrupted attempt.

## Run provenance

The first QLoRA attempt fell back to the optimizer default learning rate. The measured QLoRA rows and their smoke evidence were regenerated with 0.0002. The recovery wrapper preserves three nonfinite gradient norms as `null` with `nonfinite_grad_norm: true`. All three affected runs reached epoch 3 with finite final training loss and trainable parameters. The events were step 10 in `xlmr_04_lora_103_100`, step 10 in `xlmr_08_full_ft_103_025`, and step 30 in `xlmr_08_full_ft_3_025`.

The handout calls for registered groups of 3–4 and permits AI coding assistance for debugging. The experiment used the requested solo Group 3 setup. Confirm the solo exception and group number with the instructor before submitting, and review the disclosed AI assistance against the handout.
