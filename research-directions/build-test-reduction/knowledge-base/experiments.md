# Experiments and runs

All runs are in WSL2 Ubuntu 24.04 on one laptop (i5-12400F, 6C/12T, 7 GB). Harness: `03-experiment/harness/bth/`. Commands assume `PYTHONPATH=$E/harness` as in the [reproduce guide](../03-experiment/README.md) §2. Design: [readiness](../03-experiment/readiness.md); rules: [rules](../03-experiment/rules.md). Each raw JSON carries `meta.state_sha` and `meta.harness_tree_hash`.

Status words: **done**, **running**, **planned**, **not run**.

## Shared frozen inputs

| Input | Content | Evidence |
|---|---|---|
| networkx edit list | 20 subject-rule commits (`f618240c` … `2e0ae8ad`), base `181f2951`; 18 applied, 2 dropped (apply conflicts) | [readiness](../03-experiment/readiness.md) §1.3; [mining raw](../03-experiment/results/raw/networkx_mining_subject_rule.txt); [states](../03-experiment/edits/networkx.states.json) |
| bottleneck edit list | Base `f51ed86`, 16 qualifying, 13 applied; main result uses states 1–8 (D19); 5-edit replay on old base `22657ac` kept as sensitivity row | [readiness](../03-experiment/readiness.md) §1.3 Deviation 2; [states](../03-experiment/edits/bottleneck.states.json); [5-edit](../03-experiment/edits/bottleneck-5edit.states.json) |
| networkx mutants | 25 frozen, seed 20261121; 20 killed by FULL (N = 20) | [FROZEN](../03-experiment/frozen/FROZEN.md); [mutants](../03-experiment/frozen/networkx.mutants.json) |
| networkx slowdowns | 10 frozen (9 `double_call`, 1 list membership) | [slowdowns](../03-experiment/frozen/networkx.slowdowns.json) |
| Spot-check sample | 10 of 171 benchmark cases, seed 20261121 | [spotcheck](../03-experiment/frozen/networkx.slowdown_spotcheck.json) |

---

## E1. RQ1 cost, networkx (FULL build + serial tests)

- **Question:** what does FULL validation cost per edit, split into build, tests and benchmarks?
- **Setup:** networkx S0–S18, CPython 3.12.16. Build = `pip install -e . --no-deps --no-build-isolation`. Tests = full pytest suite, serial (M1).
- **Command:** `bash scripts/oracle_nx.sh build $(seq 0 18)`; `bash scripts/oracle_nx.sh tests <i>`; `python scripts/aggregate_rq1.py networkx`.
- **Status:** done (first runs); idle re-run done overnight and written up (E8).
- **Result:** tests median 85.7 s per edit (75.4–119.2 s, clean states), 6771 tests, all pass. Build median 1.19 s, 1.19–2.11% of test time (negligible). Session total 1700 s of serial tests.
- **Benchmarks:** first S0 pass stopped (8/171 cases in 2360 s, concurrent). The import-only lower bound (0.89 / 1.78 / 4.45 h per pass) is **superseded** (D17) by measured passes: 659–2444 s over 6 same-protocol passes, median ≈ 730 s, 8–28× build + tests (E12, findings R1, R4).
- **Caveats:** single runs; S16 noisy, S17 borderline (post-hoc rule, D07); the re-runs show both were load-affected (E8).
- **Raw:** [`raw/networkx/{build,oracle-tests}/`](../03-experiment/results/raw/networkx/); [rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv); [import times](../03-experiment/results/raw/networkx/bench/import_times_S0.txt); [results](../03-experiment/results/results.md) "RQ1".

## E2. RQ1 cost, bottleneck build probes

- **Question:** is the build share non-negligible for a C extension, and what do incremental builds rebuild?
- **Setup:** bottleneck base `22657ac` (old window), CPython 3.8.20 + numpy 1.19.5. `nice -n 19 python setup.py build_ext --inplace`. Probes B–G edit one file each.
- **Status:** done (noisy single runs).
- **Result:** clean 9.90 s, about 22% of clean build + tests (34.4 s, 168 pass). One template edit 1.79–2.64 s; `bottleneck.h` 4.86 s (all 4 `.so`); `iterators.h` 0.20 s, rebuilds nothing; null 0.20 s.
- **Caveats:** ran under load beside networkx timings; old base, not the amended replay base. The 22 % share is **superseded** by ≈ 16–18 % on `f51ed86` (E9).
- **Raw:** [`raw/bottleneck/incr_*`](../03-experiment/results/raw/bottleneck/); [rq1_bottleneck_build](../03-experiment/results/rq1_bottleneck_build.md).

## E3. RQ2/RQ3 arms simulation, networkx (tests only)

- **Question:** what do existing techniques and our policy cost, and what functional faults do they miss, over 18 replayed edits?
- **Setup:** 16 arms (A0 FULL, A1 INC, A2 TESTMON, A3 CHANGED_MODULE, A5 STATIC_BENCH, A2/A3/A5 + k ∈ {3,5}, A4 OURS and ablations). Inputs: per-state depmaps, real chained `pytest --testmon` selections, S0 static analysis, kill sets of the 20 mutants.
- **Command:** `python -m bth.orchestrate simulate --config configs/networkx.toml --inputs results/sim/networkx/inputs --out results/sim/networkx/rq2_steps.csv`; table by `python scripts/rq2_table.py`.
- **Status:** done (draft). Benchmark seconds and regression detection are not in the per-arm totals.
- **Result:** est. end-to-end s: FULL 1548 (1634 measured; 1413 s on the idle re-runs), A2 testmon 330 (404 measured, concurrent), A3 221, A4 655, A2 + k=5 594. testmon vs FULL measured: 3.5–4× (mixed load). Misses: 0/20 for every arm except A3 (2/20; caught at the next checkpoint with a delay of 1–2 steps when periodic full checks are added). A4 fires 5 full checks (steps 3, 5, 8, 13 + final).
- **Caveats:** mutants sit in edited functions, so selection catches them almost by construction (M2). testmon detection uses clean-replay selections, not runs with each mutant present. N = 20.
- **Raw:** [rq2_networkx.csv](../03-experiment/results/rq2_networkx.csv); [rq2_steps.csv](../03-experiment/results/sim/networkx/rq2_steps.csv); [summary](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv); [killsets](../03-experiment/results/raw/networkx/faults/killsets.json); [latent](../03-experiment/results/raw/networkx/faults/latent.json).
- **Sub-run (latent re-check):** each of the 5 FULL survivors re-applied at every later state: 0 become detectable. Pre-registered null for accumulation stands.
- **Sub-run (benchmark selection counts):** S0 profiles 171/171. A5 static reach 1893 cases; FULL 3078; A4 collapses to all benchmarks after step 3 (B2); labelled P8-violating variant gives 889. [variant](../03-experiment/results/sim/networkx/variant_stale_s0_profiles.csv); [profile](../03-experiment/results/raw/networkx/profile/S0_181f2951.json).

## E4. Worked edit (networkx step 10)

- **Question:** how does one edit flow through FULL and reduced validation?
- **Setup:** edit `c1c468d5` (`_build_paths_from_predecessors`), S9 → S10 `52b7255a`; selections from S0 data only.
- **Command:** `python3 scripts/worked_edit.py 10`.
- **Status:** done. Bench-s use the noisy 1668 s S0 pass (E12).
- **Result:** FULL 6768 tests, 85.99 s end-to-end; testmon 20 tests, 13.61 s; "A4 single-edit view (no accumulation)" 38 tests, 13.62 s, 1 benchmark case. About 6× end-to-end, not 3500×, because pytest startup (13.6 s) remains. A4 as simulated in the session runs 71 tests and 171/171 benchmarks at step 10 (B2).
- **Caveats:** one pure-Python edit; no reduced build shown. The planned bottleneck worked edit does not exist.
- **Raw:** [worked-edit](../03-experiment/results/worked-edit.md).

## E5. Depmap `-n 6` vs `-n 5` and same-state repeats (C7)

- **Question:** is the function-level dependency map deterministic?
- **Setup:** S0 depmap originally run with `-n 6`, re-run with `-n 5` for consistency; then S0 ×2 and S18 ×3 with identical settings.
- **Command:** `python -m bth.orchestrate depmap … -n 5` (labels `.rep2`, `.rep3`).
- **Status:** done.
- **Result:** 62 of 2589 functions (2.4%) at S0, and 96 across the S18 triple, map to different test sets in runs of the same code. A cruder consecutive-state comparison over-counted (176). Led to rule F6-order (D08), which changes nothing in this session.
- **Raw:** [order_dependent_S0pair](../03-experiment/results/raw/networkx/order_dependent_S0pair.json); [S18 triple](../03-experiment/results/raw/networkx/order_dependent_S18triple.json). Depmaps themselves are not in git: see [RAW-DATA-MANIFEST](../03-experiment/results/RAW-DATA-MANIFEST.md) (the `-n 6` file is kept as `S0_181f2951.n6-superseded.json.bak`).

## E6. Bottleneck replay and mining

- **Question:** build the bottleneck edit sequence.
- **Command:** `python3 scripts/replay_bn.py`; `python3 scripts/reformat_check.py …`.
- **Status:** done. 13/16 applied on base `f51ed86` (conflicts `cd32416d`, `8b587c5c`, `f1d14dc2`).
- **Later caveat:** replayed state at `98b59df2` (step 9) does not compile (E11; a replay artefact, D20), so states 9–13 are held out (D15). Main bottleneck result: amended window states 1–8; the 5-edit replay is a sensitivity row (D19).
- **Raw:** [bottleneck_mining](../03-experiment/results/raw/bottleneck_mining.txt); [reformat check](../03-experiment/results/raw/reformat_check_bottleneck.txt).

---

## Overnight queue (approved 2026-11-21 19:24)

Driver `scripts/overnight.sh`; log [overnight.log](../03-experiment/results/raw/overnight.log); plan [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md). Idle gate opened 19:37.

## E8. Item 1: networkx idle re-timing

- **Question:** do the first-run timings hold on an idle machine?
- **Status:** done 19:38–20:04; written up ~06:09 in results.md "RQ1 — idle re-timing".
- **Command:** `scripts/idle_compare.py` → `rq1_networkx_idle.csv`.
- **Result:** median serial tests 77.2 s on the re-run vs 86.1 s first run (ranges 70.7–83.8 s vs 75.4–142.2 s; first / re-run ratio 0.96–1.99). Re-run build 0.95–1.75 s; all 6771 tests pass. **S16 and S17 return to 71.5 s and 71.0 s** (first 142.2 s, 119.2 s): their first-run slowness was external load (S17 was only borderline under the timing_label rule). The other 17 states agree within 0.96–1.20×. Per-edit serial test cost ≈ 71–89 s across both runs (excluding S16/S17 first runs); headline unchanged.
- **Caveat:** **none of the 19 re-runs is M5-clean**, so all are labelled noisy: S0–S6 overlapped this session's profile job (19:38–19:46), and from S1 the start load was 1.54–2.95. Part is self-inflicted (the gate reads the 1-min average right after the previous run, adding up to ≈ 1), which does not explain 2–3; the rest is unidentified, probably other sessions. The direction holds, precise values do not.
- **Raw:** [`raw/networkx/{build,oracle-tests}/S*.idle.json`](../03-experiment/results/raw/networkx/oracle-tests/); [rq1_networkx_idle.csv](../03-experiment/results/rq1_networkx_idle.csv); [idle_compare.py](../03-experiment/scripts/idle_compare.py); [overnight.log](../03-experiment/results/raw/overnight.log); [results](../03-experiment/results/results.md) "RQ1 — idle re-timing".

## E9. Item 1b: bottleneck build re-timing

- **Setup:** base `f51ed86`, 3 repeats: clean, null, one template, `bottleneck.h`.
- **Status:** done 20:03.
- **Result:** clean 4.72–5.41 s; null 0.18 s; one template 2.17–2.20 s; `bottleneck.h` 2.78–2.88 s.
- **Use (results.md RQ1 headline):** with the ≈ 24 s full suite (191 tests) on `f51ed86`, the build is **≈ 16–18 % of clean build + full tests** before benchmarks; replaces E2's 22 %.
- **Caveat:** load averages at the samples were 1.46–2.35, so by M5 these are not clean either. The base differs from E2 (`22657ac`), so the 9.90 s clean build in E2 is not directly comparable.
- **Raw:** [retime-idle](../03-experiment/results/raw/bottleneck/retime-idle/).

## E10. Item 2: slowdown oracle (networkx)

- **Question:** does FULL detect the frozen slowdowns, and does reach-based benchmark selection miss any?
- **Setup:** each slowdown at its state, patched vs unpatched clone, interleaved A/B, CPUs 2–5. Within reach (S0 profile ∪ static reach): 2 processes × 3 values × 3 repeats. Out-of-reach spot check: 1 × 3 × 2. asv rule.
- **Command:** `scripts/slowdowns_nx.py` (plans written first as `<i>.plan.json`).
- **Status:** done 20:04–05:10.
- **Result:** FULL detects 3/10 as classified (Wilson 10.8–60.3%), 2/10 on target (#2 at 1.81–1.90× on 8/8 profiled cases; #8 at 1.116×). #1 (1.245×, off target, p = 0.0018) judged noise. 5 slowdowns (#0, 5, 6, 7, 9) have zero reaching benchmarks. Primary result (D13): regression safety not measurable on networkx with the frozen set.
- **Spot check: withdrawn as evidence (no power).** 50 out-of-reach comparisons gave "0 slower", but 1 × 3 × 2 = 6 vs 6 samples cannot reach p < 0.002 (minimum exact MWU p 0.00216; smallest observed 0.015), so the result holds by construction. Protocol deviation (readiness §5: ≥ 5 processes). Powered re-run approved (D18), pending.
- **Caveats:** 410 of 5330 runs (7.7%) had load > 1.5. Static reach covered all 171 cases for 5 slowdowns, so nothing was left to spot-check there. Per-arm regression simulation not run. The unpatched base sides double as 5 benchmark-pass cost samples (659–2444 s; E12).
- **Raw:** [`raw/networkx/slowdowns/0?.json`](../03-experiment/results/raw/networkx/slowdowns/); [results](../03-experiment/results/results.md) "Slowdown oracle".

## E11. Item 3: bottleneck `iterators.h` hazard study

- **Question:** does an incremental build after an `iterators.h` edit differ from a clean build in artefact or behaviour?
- **Setup:** 3 natural edits `c5720c8d`, `a638b282`, `98b59df2`. Arms INC (incremental), CLEAN, STALE (counterfactual pre-fix `depends=`). `.so` sha256 raw and stripped; 191 tests; 64 benchmark cases × 3, asv rule vs CLEAN.
- **Command:** `scripts/wsl/bn_hazard.sh` (via `bn_all_after1850.sh`).
- **Status:** done 05:10–05:30.
- **Result:** hash comparison uninformative (build path embedded; parent vs clean differ too). Natural edits: hazard did not reproduce; tests identical; `c5720c8d` 64/64 same; `a638b282` 63 same + 1 "faster" outlier on byte-identical code. Probe: stale artefacts appear but are byte-identical to the correct rebuild. `98b59df2`: does not compile in any arm (`DTYPE1` undeclared); INC and STALE kept the parent `.so` and passed 191/191; CLEAN had 8 collection errors; its 192 benchmark entries are import errors (no verdict).
- **Caveats:** single runs; load rose to 1.65 at `a638b282` and was 2.14 → 1.63 at `98b59df2` (noisy). Missing prerequisite for `98b59df2` not diagnosed. The `98b59df2` false pass is a **replay artefact** (state never existed upstream): a hazard mechanism, not a natural-edit event (D20); the RTS part is inferred (testmon not run on bottleneck).
- **Raw:** [`raw/bottleneck/hazard/`](../03-experiment/results/raw/bottleneck/hazard/); [build-hazard-iterators-h](../03-experiment/results/build-hazard-iterators-h.md).

## E12. Item 4: measured FULL benchmark pass at S0

- **Question:** measured per-pass FULL benchmark cost (replaces the import-only lower bound).
- **Setup:** all 171 cases, asv default 2 processes × 3 values, CPUs 2–5.
- **Status:** done 05:30–05:58. Labelled **noisy in advance** (load 1.63 > 1.5 at start; the gate labels but does not postpone, a logged deviation).
- **Result:** 1668 s, 171/171 cases, 0 errors; `benchmark_algorithms` 1570 s of it. With the 5 slowdown-oracle base sides (E10: 659, 665, 708, 751, 2444 s) there are **6 same-protocol passes: 659–2444 s, median ≈ 730 s, 8–28× build + tests**. The ≈ 3.7× spread is a cost-noise finding (R4); likely host-side Windows load, not measured.
- **Use:** per-pass cost and case weights only; not for regression decisions, noise floor or oracle repeatability. Re-run needs PM approval.
- **Raw:** [`raw/networkx/bench/S0_181f2951.idle.json`](../03-experiment/results/raw/networkx/bench/S0_181f2951.idle.json); [LABELS](../03-experiment/results/raw/networkx/bench/LABELS.md); [results](../03-experiment/results/results.md) "RQ1 headline".

---

## Planned but not run

| Item | What | Why it matters | Source |
|---|---|---|---|
| Powered spot-check re-run (approved D18) | Out-of-reach spot check at ≥ 5 processes, ≥ 15 vs 15 samples; postponing idle gate; 1.5 h cap | The original spot check had no power and is withdrawn; no reach-safety evidence exists until this runs | [decisions](decisions.md) D18; [results](../03-experiment/results/results.md) "Safety of reach-based selection" |
| Oracle repeatability | Re-run the FULL asv-rule decision ≥ 3 times, interleaved, on S0, steps 5, 10, 15 and 2 slowdown states | Needed before any miss is counted; would settle #1 and the `nanmin` outlier | [readiness](../03-experiment/readiness.md) §5; [OVERNIGHT](../03-experiment/results/OVERNIGHT.md) |
| A/A benchmark noise floor | Same state twice, interleaved, 5 repeats → σ_noise per benchmark | Required by the TPM show rule for any perf claim | [readiness](../03-experiment/readiness.md) §5; [03-results-summary](../meeting-2026-11-advisor/03-results-summary.md) |
| Cap-only and additive-budget comparators | C5 baselines; T ∈ {5, 20}; k ∈ {2, 8} | Matched-cost comparison for the A4 trigger | [rules](../03-experiment/rules.md) §6 |
| NameRTS comparator | Run the public replication package | Strongest Python RTS found | [W1 README](../01-literature/README.md); agenda A7 |
| Checkpoint re-profiling | Profiles at S3, S5, S8, S13 | Without it A4's P8 rule selects all benchmarks (B2) | [results](../03-experiment/results/results.md) "B2" |
| Per-arm regression simulation | Feed slowdown verdicts into the arm simulator | Not run | [results](../03-experiment/results/results.md) |
| Caller faults (class 2) | Mutants in callers or shared state | Gives accumulation a chance to matter | [readiness](../03-experiment/readiness.md) §4.1b |
| Real testmon runs with mutants | Run testmon with each mutant present | Detection is currently simulated | [results](../03-experiment/results/results.md) "testmon caveat" |
| B4 at a fixed path / `-ffile-prefix-map` | Re-validate the hash differential | B4 invalid as specified | [hazard](../03-experiment/results/build-hazard-iterators-h.md) §1 |
| scikit-learn cost-only measurement | Heavy-build cost | Not reported in any results file | [readiness](../03-experiment/readiness.md) §8 |
| sqlglot | Third subject | Cut first if late | [readiness](../03-experiment/readiness.md) §8 |
