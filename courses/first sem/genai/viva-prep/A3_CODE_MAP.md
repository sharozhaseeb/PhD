# A3 Code Map — where is what?

Folder: `assignment-3/output/Group3_Assignment3/`. Code is in `source/`; the notebook is `Group3_Colab_Executed.ipynb`. Line numbers refer to `source/`.

## How the pieces call each other
```
Notebook (Colab)
 └─ cell 1: unpacks the source files into /content/genai_a3_code, pip installs, nvidia-smi
 └─ cell 3: invoke(script, ...) runs each script as a subprocess
     └─ train_group3.py  <job_id>  (ONE training run per call)
          └─ imports track3_preflight.audit_data()  → same cleaned data and splits
          └─ writes runs/<job_id>/result.json, trainer_log.json, prediction CSVs
     └─ collect_results.py  → validation_selection.json, results.csv, summary.csv, per_class.csv
make_figures.py  (uses collect_results)  → figures/*.png
make_report.py   (uses make_figures)     → the report PDF
run_recovery.py  = wrapper from cell 11: patches train_group3, then calls its main()
```
**Job id format:** `xlmr_05_qlora_3_100` = model · experiment · method · seed · data %. All 64 jobs are listed in `group3_run_plan.json`.

## Notebook cells
| Cell | What it does |
|---|---|
| 1 | Unpack the bundled source files, install requirements, check the GPU |
| 3 | Print the split label counts + tokenizer audit; define `invoke()` and `run_jobs()` |
| 5 | Smoke checks: one optimizer step for experiments 01/03/05/07b × both models (8 runs) |
| 7 | Verify the smokes, smoke the unpaged QLoRA (06), run the **pilot** (XLM-R Full FT), re-check its F1 |
| 9 | Zip the pilot + smoke evidence and download it |
| 10 | Full roster: 32 baseline runs → select configs → 32 reduced-data runs → collect results |
| 11 | **Recovery:** archive the bad QLoRA and crashed runs, write `run_recovery.py` (LR fix + nan grad_norm logging), re-smoke QLoRA (asserts LR = 2e-4), rerun the roster |

## "Show me where you…" → file : line
| Topic | Where |
|---|---|
| Load the pinned dataset + check its SHA-256 | `track3_preflight.py` : 34–37 (`audit_data`) |
| Clean the tweets (URLs, @mentions, yeh/kaf) | `track3_preflight.py` : 27 (`clean`) |
| Remove duplicates / conflicting labels (grouped by cleaned text) | `track3_preflight.py` : 53–59 |
| Stratified 70/15/15 split (seed 3) | `track3_preflight.py` : 63–66 |
| 50% / 25% nested subsets (RQ3) | `track3_preflight.py` : 82–86 (`reduced_subsets`) |
| Tokenizer audit: UNK count, fertility, p95 | `track3_preflight.py` : 92–115 (`audit_tokenizers`) |
| Choose max_length = 43 + truncation rates | `track3_preflight.py` : 117–121 |
| Which layers get adapters: LoRA query/value (+ output.dense in exp 04); IA3 key/value (+ FFN in 07b) | `train_group3.py` : 56–65 (`target_names`) |
| Build the model: QLoRA 4-bit (NF4) config | `train_group3.py` : 73 (`BitsAndBytesConfig`), 84 (`prepare_model_for_kbit_training`) |
| IA3 config | `train_group3.py` : 87 |
| LoRA config (r = 8 for exp 02, else 16) | `train_group3.py` : 89 |
| Tokenize with truncation at max_length | `train_group3.py` : 102–104 (`TextRows`) |
| Metrics: macro-F1 + accuracy | `train_group3.py` : 114 (`score`), 120 (`trainer_metrics`) |
| Save predictions to CSV | `train_group3.py` : 124 (`export_predictions`) |
| One full run (seed, data, training, eval) | `train_group3.py` : 158 (`run`) |
| Set the seed | `train_group3.py` : 162 |
| Use a reduced subset (50% / 25%) | `train_group3.py` : 172–173 |
| QLoRA optimizer: bnb AdamW 32-bit, paged (05) vs unpaged (06) | `train_group3.py` : 185–187 |
| TrainingArguments (final epoch, no early stopping) | `train_group3.py` : 210–211 |
| Trainer + dynamic padding | `train_group3.py` : 220–221 |
| Measure peak GPU memory + training time | `train_group3.py` : 224–230 |
| Save validation + test predictions (no test metric computed during training) | `train_group3.py` : 234–239 |
| Test metrics computed (only at aggregation, after selection) | `collect_results.py` : 107 (`aggregate`) |
| Command-line entry; RQ3 reads the validation selection | `train_group3.py` : 256 (`main`), 267 |
| Check a run is complete and valid | `collect_results.py` : 26 (`completed`) |
| **Choose the RQ3 configs by VALIDATION macro-F1** | `collect_results.py` : 66 (`select`) → `validation_selection.json` |
| Mean ± SD over the 2 seeds → CSVs | `collect_results.py` : 107 (`aggregate`), 162–164 |
| Plots: Pareto memory/time, rank, scarcity, fertility | `make_figures.py` : 19 (`plot_results`), 74–75, 98–104 |
| LR fix for QLoRA + nan grad_norm handling | `run_recovery.py` (written by notebook cell 11) |
| Build the report PDF | `make_report.py` : 26 (`build`) |

## Output files
| File | Holds |
|---|---|
| `results.csv` | One row per run (64): F1, accuracy, time, memory, params |
| `summary.csv` | Mean ± SD per model × method × experiment × data % |
| `per_class.csv` | Precision/recall/F1 per label per run |
| `validation_selection.json` | Which config was picked for RQ3, and why (validation F1) |
| `source/track3_preflight.json` | Splits, label counts, tokenizer audit, max_length |
| `Group3_T4_Complete_Evidence.zip` | Raw logs of every run |
