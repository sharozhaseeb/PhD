# C5 batching comparators — pre-registered plan (written 2026-11-22 ≈ 06:29 PKT [file time 06:29:51; the header originally said 06:35 in error], before any C5 simulation output exists)

**Request:** PM 06:27, Q1. **Source of the comparators:** W1 `01-literature/candidate-rules.md` C5 ("Required baselines: fixed-k (FSB), cap-only, and additive-budget at matched cost") and `01-literature/notes/R2-batching-threats-fullread.md` (Sayedsalehi 2026 "-la", FSB, TWB-like cap).

## What the comparators are

They are pure **batching** policies. Edits accumulate, and **nothing is built or run between full checks**. That is how batch CI works: individual commits in a batch get no test of their own. Implemented as `bth.select.Batch` with unit tests in `tests/test_batch.py`.

| Comparator | Rule | Literature analogue |
|---|---|---|
| **cap-only** `BATCH:cap=k` | Full check when k edits have accumulated since the last full check, and at the last step. | FSB / TWB time cap. In a sequential edit stream with one edit per step, a time cap and a size cap coincide. |
| **additive-budget** `BATCH:budget=T` | Full check when OURS' additive score (\|A_t\| + 5·headers + 5·F2 fallbacks, the same code as A4) reaches T, and at the last step. | Risk-mass "-la" batching, with the learned per-commit risk r_i replaced by our measured score. |
| additive-budget with cap `BATCH:budget=10,cap=5` | Either trigger. | "-la" with a time cap. |

Both also inherit A4's mandatory full checks (build-config edit, unknown native extension). There are none on networkx.

## Arms (fixed now)

- **Comparators:** `BATCH:cap=2`, `BATCH:cap=3`, `BATCH:cap=5`, `BATCH:cap=8`, `BATCH:budget=5`, `BATCH:budget=10`, `BATCH:budget=20`, `BATCH:budget=10,cap=5`.
- **References:**
  - A4 `OURS` (T = 10, pre-registered), plus the pre-registered sensitivity values `OURS:T=5` and `OURS:T=20` (rules.md §6).
  - Fixed-k with the per-edit tier: `PERIODIC:inner=TESTMON,k=2|3|5|8`, `TESTMON`, `FULL`.
- **Inputs:** frozen, `results/sim/networkx/inputs/`, the same 18 steps, the same 25 frozen mutants (20 detectable by FULL).

## Metrics (fixed now)

- **Primary cost:** estimated end-to-end seconds without benchmarks, as in the draft RQ2 table: Σ build_s + est. test-s + 13.6 s pytest start-up per step that runs ≥ 1 test.
- **Secondary cost:** the same plus benchmark seconds, using per-case weights from the measured S0 pass (`raw/networkx/bench/S0_181f2951.idle.json`, labelled noisy). Reported separately, because benchmark cost varies ≈ 3.7× between passes.
- **Detection** on the 20 functional mutants:
  - missed k/N, with Wilson CI;
  - **caught at the injection step** (delay 0) k/N;
  - mean delay in steps;
  - **localisation window:** the number of edits in the window where the fault was found. This is 1 for a per-edit selection hit. For a full-check hit it is the number of edits since the previous full check. It is the number of candidate culprits a batch failure leaves to bisect.
- **Regression detection:** not evaluated. It is not measurable on networkx with the frozen slowdowns (results.md, primary pre-registered result).

## Comparison (fixed now)

- **Matched cost:** for each comparator family (cap-only over k; additive-budget over T), interpolate mean delay, caught-at-injection and mean window linearly at **A4's primary cost**, then compare with A4's values.
  - If A4's cost lies outside a family's cost range, report "no matched point" and give the nearest point. Do not extrapolate.
- **Equal detection:** the cheapest member of each family that reaches A4's caught-at-injection count, if any.
- **No retuning:** T and k are not tuned on the outcome. Every arm above is reported, whatever the result.
- **Expectation, stated so it can fail:** none is pre-registered as a hypothesis. Batching saves the per-edit start-up cost but delays detection and widens the culprit window. Which effect dominates at A4's cost is the result.

## Outputs

`results/sim/networkx/c5_steps.csv{,.faults.csv,.summary.csv}` (`bth.orchestrate simulate` with the arm list above) and `results/sim/networkx/c5_compare.csv` + `c5_compare.json` (`scripts/c5_compare.py`). The existing `rq2_steps.csv*` files are not overwritten.

**Run:** after the powered spot check ends (simulation only, no timing; it is still run alone to keep the machine idle).
