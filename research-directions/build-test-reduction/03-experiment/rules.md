# Deterministic selection rules used in W3 (exact, as implemented)

**Status:** v0.1, 2026-11-21. The rules were fixed **before** any fault set was generated or any arm was run. Parameters were set a priori and are never tuned on the frozen fault sets; sensitivity is reported as curves. Rule IDs refer to W1 `01-literature/candidate-rules.md` v1.1. Rules W1 does not have are marked **W3-new**. The code is in `harness/bth/` (the module is named per rule).

No rule uses AI, learned models or randomness. Seeded randomness appears only in *fault generation* (`faults.py`, fixed seed), never in selection.

## 0. Inputs every arm may use at step t

- The change set of step t: `changed_fns.ChangeSet` (functions, files, module-level files, native files, header edits, build-config flag, unmapped native names).
- Observations from steps **< t** only: per-test dependency sets, per-benchmark profiles, test outcomes. **Hindsight rule:** an arm never reads data produced at state S_t before deciding at t (unit test `test_hindsight_decide_uses_only_earlier_observations`).
- Static data computed from the base: static import/call graph (A5), test→module and benchmark→module name maps (A3).

## 1. Change extraction (`changed_fns.py`)

| Rule | Exact definition | ID |
|---|---|---|
| Python function change | A `def` (including decorators and the class/nesting qualname) is changed if any removed old-side line or added new-side line falls in its span. Added and deleted functions count. Blank and comment-only lines are ignored. | F6 variant (function granularity) |
| Import-time change | Any changed line outside every function → `<file>::<module>`. The selector expands this to all functions of that module. | F6 import-time fallback |
| C function change | Top-level definitions found by brace scan. A macro header `NAME(pyname, …) {` maps to the first argument (bottleneck templates); a plain C header maps through the config's `native_name_regex`. The change maps to `native::<ext>.<pyname>`. Macro-only/blank lines ≤ 3 lines above a header attach to that function. | B2 / F2 support, **W3-new** (template-name mapping) |
| Header/template edit | `*.h`, template generators, and C lines outside any function → `header_edits`. These expand to every native function of the extension(s). | F2, B2 |
| Build-config edit | `setup.py`, `pyproject.toml`, `meson.build`, … → `build_config_changed`. | B3 |

## 2. Build rules

| Arm | Rule | ID |
|---|---|---|
| A0 FULL | Clean rebuild every step: delete build dirs, `.so` and `__pycache__`, then rebuild. This is the per-edit procedure of SWE-Perf, GSO and SWE-fficiency (W2). | B3-style, C3 |
| others | Pure-Python edit → no compile step. Native edit → incremental `build_ext --inplace`. Build-config edit → clean build. | B1, B2, B3 |
| A4 | Additionally, at every full check: a clean-vs-incremental differential (stripped `.so` SHA-256 + FULL test outcomes) and a null-rebuild guard. Any mismatch → clean builds for the rest of the session. | B4, B6 |

## 3. Functional test selection

| Arm | Rule | ID |
|---|---|---|
| A1 INC, A0 | All tests. | — |
| A2 TESTMON ("PerfAgent-style per-edit RTS") | `pytest --testmon` as shipped. Its DB carries over across steps; nothing is modified. | F1 / F6 (testmon) |
| A3 CHANGED-MODULE | Tests whose test file maps by name/package to a changed source module (`module_of_test`). | **W3-new** naive baseline (file level) |
| A5 STATIC-BENCH | Tests as A2. | F1 |
| A4 OURS | Select test τ iff `deps_<t(τ) ∩ A_t ≠ ∅`. `deps_<t(τ)` is the function set recorded by `sys.monitoring` the last time τ ran before t (Python functions + native entry points). A_t is the **accumulated** changed-function set since the last green full check, with module-level entries expanded to all functions of the module and header edits expanded to all native functions of the extension. | F6 variant (function level, native-aware), C7 mechanism, F3 |
| A4 always-run | ∪ tests that failed at their last run ∪ tests of the edited module (A3 map). | F4 |
| A4 native fallback | A changed native function seen in no recorded dependency set → all tests reaching `native::<ext>.*`. Unknown extension or build-config change → full check. | F2 |
| A4 order-dependent attribution | A function whose reaching-test set **differs between two depmap runs of the same state with the same `-n`** (first-call, lazy-import or cache-reset code, attributed to whichever test runs first on an xdist worker) is flagged order-dependent. If such a function is in A_t, **all tests** are selected (no full check, no reset). The list is fixed from the base/early repeats, never from S_t. *Reason:* the function-level dependency map is unreliable for these functions (C7, stale or incorrect dependency data), found 2026-11-21 on networkx. | **W3-new "F6-order"** (extends W1 F6's import-time select-all) |
| A4 flaky | Tests that changed outcome in the same-state 2-run check are quarantined. Their failures do not count as detections and do not drive F4. | F5 |
| A4 refresh | A green full check observes all tests, so every dependency set is refreshed and A_t := ∅. Tests run at step t refresh their own sets for later steps. | F3 |

## 4. Benchmark selection

| Arm | Rule | ID |
|---|---|---|
| A0, A1, A2 | All benchmarks. | — |
| A3 | Benchmark files whose name maps to a changed module. | **W3-new** naive |
| A5 | Benchmarks whose **static** reach (STARTS-style import/call graph, conservative module edges for unresolved calls) intersects the **current** edit's changed functions. | **W3-new** application of static RTS (STARTS) to benchmarks |
| A4 | Benchmarks whose stored **profile** (functions executed during one call, recorded via `sys.monitoring`) intersects A_t. Profiles are refreshed at every green full check and are never older than the last checkpoint. | P1, P8 |

## 5. Performance decision (identical in every arm)

- asv rule: ratio of medians > 1.1 (slower) or < 1/1.1 (faster), **and** two-sided Mann-Whitney U p < 0.002.
- Regression additionally needs ratio > 1 + 3·σ_noise(b) (noise floor, P6). This applies against the **original** base (P5) and against the previous accepted state.
- Measurement: separate processes, calibrated `number`, warmup discarded, interleaved A/B (P2, P3). The SWE-Perf rule is reported as a sensitivity check.

## 6. Checkpoints

| Arm | Rule | ID |
|---|---|---|
| +k arms | Full check every k steps (draft: k ∈ {3, 5}) and at the last step. | C1, C3 |
| A4 | Full check when score_t ≥ T (T = 10), and always at the last step. score_t = \|A_t\| + 5·(distinct header edits since the last green full check) + 5·(F2 fallbacks since then). | C5 (model-free risk-mass trigger), C3 |
| all | Each full check writes a window record: misses and delay of the reduced checks in the window. | C6 |
| after draft | C5 cap-only and additive-budget baselines; T ∈ {5, 20}; k ∈ {2, 8}. | C5 |

## 7. Ablations of A4 (RQ3)

- (a) −accumulation: A_t := the current edit's changes only (the score is still tracked).
- (b) −profile: benchmarks by the A3 rule.
- (c) −trigger: periodic k = 5 instead of the score trigger.
