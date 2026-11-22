# Glossary

Arm names follow [rules](../03-experiment/rules.md). Rule IDs (B, F, P, C) follow [candidate-rules](../01-literature/candidate-rules.md).

## Arms

| Term | Meaning |
|---|---|
| **FULL (A0)** | Clean rebuild, all tests, all benchmarks at every step. Also the oracle for every state. |
| **INC (A1)** | All tests, but incremental build (pure-Python edit → no compile; native edit → `build_ext --inplace`). |
| **testmon / TESTMON (A2)** | `pytest --testmon` as shipped, DB carried across steps. "PerfAgent-style per-edit RTS". All benchmarks. |
| **CHANGED_MODULE (A3)** | Tests (and benchmark files) whose file name maps to a changed module. Naive file-level baseline. |
| **STATIC-BENCH (A5)** | testmon tests, plus benchmarks whose static import/call-graph reach hits the current edit's changed functions (STARTS-style). |
| **A2+k (also A3+k, A5+k)** | The arm plus a full check every k steps (k ∈ {3, 5}) and at the last step. |
| **OURS / A4** | Function-level test selection on the **accumulated** changed set since the last green full check, profile-based benchmark selection, and a full check when score_t ≥ T (T = 10) and at the end. Ablations: −accumulation, −profile, −trigger (k = 5), −F6-order. |
| **score_t** | \|A_t\| + 5 × header edits + 5 × F2 fallbacks since the last green full check. |
| **A_t** | Accumulated changed-function set since the last green full check; module-level edits expand to all functions of the module. |

## Measurement

| Term | Meaning |
|---|---|
| **asv rule** | A benchmark is "slower" if the ratio of medians > 1.1 and a two-sided Mann-Whitney U test gives p < 0.002 ("faster" if < 1/1.1). Same in every arm. |
| **noise floor** | Per-benchmark spread σ_noise from an A/A run (same state twice). A regression must also exceed 1 + 3·σ_noise. **Not yet measured.** |
| **A/A run** | Measuring the same code against itself to estimate noise. |
| **oracle repeatability** | How often the FULL performance verdict repeats over ≥ 3 interleaved re-runs. Planned, not run. |
| **interleaved A/B** | Alternating runs of the two versions on the same machine to share interference. |
| **est. test-s** | Sum of S0 serial per-test durations of the tests an arm runs. |
| **est. end-to-end s** | est. test-s + build + 13.6 s pytest startup per step that runs ≥ 1 test. |
| **M5 / load gate** | Pre-registered rule: timing runs start only when the 1-minute load ≤ 1.5; above it a run is postponed, aborted, or kept and labelled **noisy**. |
| **noisy / clean / concurrent** | Timing labels. `timing_label` rule (post-hoc) marks a state noisy on a uniform per-test shift > 1.10 or untouched tests > 1.15×. "Concurrent" means the run shared the machine with other runs. |
| **Wilson CI** | 95% Wilson score interval for a proportion, used for "k of N missed". Never read as "safe". |

## Selection data

| Term | Meaning |
|---|---|
| **depmap** | Per-test set of functions executed, recorded with `sys.monitoring` (Python functions + native entry points), per state, with xdist `-n 5`. |
| **reach** | The benchmarks that execute (profile reach) or may execute (static reach) a given function. |
| **profile reach** | From each benchmark's S0 profile (functions executed during one call). |
| **static reach** | From the static import/call graph with conservative module edges; over-approximates. |
| **F6-order** | W3-new rule: functions whose test attribution differs between same-state depmap runs select all tests when changed. |
| **P8** | Profile refresh rule: never use a profile older than the last full check. |
| **B0** | W3-new rule (2026-11-22): a failed build is a reject in every arm. |
| **B4** | Clean-vs-incremental `.so` hash differential at full checks. Invalid as specified (build path embedded). |

## Faults

| Term | Meaning |
|---|---|
| **frozen mutants** | 25 deterministic functional mutants (seed 20261121) in functions changed at their step, frozen with sha256 before any arm ran. 20 killed by FULL (N = 20). |
| **kill set** | The tests that fail when a mutant is present. An arm detects it if its tests intersect the kill set or the step is a full check. |
| **latent fault** | A FULL survivor that becomes detectable at a later state. 0 of 5 on networkx. |
| **frozen slowdowns** | 10 synthetic slowdowns (9 call the body twice, 1 list-instead-of-set) in changed functions. Bands: strong ≥ 2×, moderate 1.2–1.5×. |
| **other-slower** | FULL flags a slowdown, but its size is outside both pre-registered bands. |
| **on target / off target** | Whether the flagged benchmark case executes the slowed function in its S0 profile. |
| **spot check** | Frozen seeded sample of 10 benchmark cases measured outside a slowdown's reach, against circularity. |
| **construction bias (M2)** | Faults placed in edited functions are caught by dependency-based selection almost by construction. |

## Study terms

| Term | Meaning |
|---|---|
| **replay** | Applying each mined historical commit's source diff onto the previous state; not a recorded optimization session (threat T1). |
| **S0, S_k** | Base state and state after k replayed edits. |
| **subject rule** | Mining regex applied to the commit subject only. |
| **reformat rule** | Window starts after the last whole-file reformat commit (≥ 50% of a file's lines). |
| **NATURAL / PROBE / STALE** | Hazard study: real replayed edits with fixed `setup.py` / counterfactual with pre-fix `depends=` / the tree built that way. |
| **C5, C7, C8, C11** | The four claimed mechanisms (native boundary, stale dependency data, incremental rebuild correctness, dropped benchmarks). See [research](research.md). |
| **B1, B2** | Results findings: edits not reached by any benchmark; profile selection collapsing to all benchmarks. Not to be confused with rules B1/B2. |
| **F1–F7 (W2)** | Practice-survey findings. Not to be confused with rules F1–F8. |
| **AI-SIM** | Label for advisor-persona output: AI-written, not the real advisor. |
