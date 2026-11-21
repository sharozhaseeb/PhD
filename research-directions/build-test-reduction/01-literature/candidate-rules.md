# Candidate deterministic rules for reduced per-edit validation (W1 → W3)

**Status:** v1.2, 2026-11-21 (v1.1 critic fixes; v1.2 concedes rule C5 as a risk-mass-batching variant and names its baselines). This version replaces v0's "to-verify" pointers with the source locations from `notes/`; the critic pass checks them. Rule IDs from v0 are unchanged; new rules have new IDs.\
**Evidence boundary:** this project has executed none of these rules. "Safe" here means a rule is *intended* to be conservative, not shown to be. Where a rule's form comes from us rather than a source, it is marked **[I]**.\
**Labels:** [R] read in source · [F] read through a web-fetch summary · [A] abstract only · [I] inferred · [U] unknown.

Every rule is deterministic. Given the edit diff, the stored dependency, profile and history data, and the frozen configuration, it always gives the same decision. Rule families:

| Family | Covers |
|---|---|
| **B** | Build |
| **F** | Functional tests |
| **P** | Performance benchmarks |
| **C** | Checkpoints and culprit finding |

**Mapping to the RQ3 policy.**
- Part (a), *change accumulated since the last full check*: C1, C5, P5, F3.
- Part (b), *benchmark selection from profiles and call graphs*: P1, P7.
- Part (c), *a full check triggered by accumulated change*: C1, C5.

The *existing-technique baselines* for RQ2 are B1/B2 (incremental build), F1 (file-level), F6 (testmon-style) and the changed-module rule.

## B — build

| ID | Rule | Trigger → action | Source basis |
|---|---|---|---|
| B1 | Pure-Python edit | The diff touches only `*.py` files that are not imported by build scripts or code generators. → No native compile step. Run with checked-hash `.pyc` files, or clear `__pycache__` for the touched files. | [F] pep552 (invalidation modes); [R] licker2019incorrect §I (Python generator scripts are hidden build dependencies, so exclude them) |
| B2 | Native edit | The diff touches `.pyx` → re-run `cythonize` and rebuild that extension plus every extension that cimports it. The diff touches `.pxd`, `.pxi`, `.h` or `.c` → rebuild the transitive dependents. Compute dependents from a trace or compiler depfiles, or fall back to rebuilding all extensions. | [F] cythondependencies (cimport/include tracking); [F] distutilsbuildext (headers only via `depends`); [R] sotiropoulos2020buildfs, licker2019incorrect (dependency sets from traces); [R] mokhov2020buildsystems §2.1 (minimality) |
| B3 | Build-config or structure edit | The diff touches `pyproject.toml`, `setup.py/cfg`, `meson.build`, `CMakeLists.txt`, compiler flags or Cython directives, or it adds, renames or deletes a source file. → Clean build of all extensions. | [R] gallaba2020kotinos §4 (skip acceleration when the graph structure changes); [F] bazelremotecaching, sccacheREADME (flags belong in the action key); [F] mesonpythoneditable (new files need a reinstall); [F] cythondependencies (directives absent from the recompile decision) |
| B4 | Clean-vs-incremental differential | At every full checkpoint (C1/C5), build cleanly in a fresh directory. Compare normalised artifact hashes, or the test outcomes, with the incremental tree. A mismatch marks every run since the last clean point as invalid and switches B to clean-always for the session. | [R] mokhov2020buildsystems §3.6 (correct = equal to a from-scratch build); [R] bezemer2017unspecified §1 (clean build is the practical workaround); [R] licker2019incorrect §III (differential idea). **No source gives a frequency** [U]. Tying it to checkpoints is [I]. |
| B5 | Environment pinning | Lock the interpreter, compiler, Cython and dependency versions for the session. Key "unchanged" on content hashes of inputs, flags and toolchain identity, not on mtimes. Any change → B3. | [R] mokhov2020buildsystems §5.2, §8.3; [F] ccachemanual (`compiler_check`, sloppiness); [F] bazelhermeticity; [R] gallaba2020kotinos (pinned locks as a precondition) |
| B6 | Fresh-build guard *(new)* | After each reduced build, a null rebuild must do nothing. The imported module must resolve to the expected build path and ABI. Benchmark only an artifact whose input hash (B5) is recorded. | [F] bazelhermeticity (null build check); [F] mesonpythoneditable (build directory requirement); guard design [I] |

## F — functional tests

| ID | Rule | Trigger → action | Source basis |
|---|---|---|---|
| F1 | File-level dynamic selection (baseline) | Run the tests whose recorded set of files read (Python modules, data files, `.so`) intersects the changed files. | [R] gligoric2015ekstazi §2–3. Expected to be weak in Python: EkstaP saves 3.1% [R WangPradelLiu2026 §4.2]. Kept as the safe baseline. |
| F2 | Fallback for non-Python inputs | The changed file is not observable by the selector (native source, build file, data or config file, environment pin). → Run every test that imports the affected extension or package. If no map exists for that file, run the full suite. | [R] ShiZhaoMarinov2019 §I (class-level misses non-source files; fall back to module level); [R] gligoric2015ekstazi §2; testmon/coverage.py silent on native code [F/U]; [W2] PerfAgent §VI |
| F3 | Dependency refresh | Re-record the dependencies of selected tests after every accepted edit. Re-record *all* tests at every checkpoint, and after any edit to import-time or global code. | [R] gligoric2015ekstazi §3.3, §5 (one observed run; collection only for executed tests); [R] WangPradelLiu2026 §4.3 (pays off after about 5 commits), §5. Re-recording at checkpoints is [I]. |
| F4 | Always-run set | Always run: tests that failed in the last W edits, tests that have not run in the last W′ edits, and new tests. | [R] Elbaum2014 §4.1, Alg. 1 (failure and execution windows); [F] PytestCache (`--lf/--ff`) |
| F5 | Flaky handling | Before the session, run the full suite r times (and once in reversed order) to mark flaky and order-dependent tests. A failure of a flaky-marked test triggers r reruns before an edit is rejected. | [R] Luo2014; [R] Gruber2021 (59% order dependence in Python); [R] Lam2019iDFlakies; [R] ShiZhaoMarinov2019 (38 of 39 missed failures were flaky); [R] zhu2019rtscheck (R1 assumes no flakiness) |
| F6 | Block/name-level selection *(new; main Python selector)* | Python-only edit outside import-time code → testmon-style block-checksum selection. If the edit changes code executed at import time (module-level statements or functions called at import), use F1 or the full suite. | [F] TestmonBlog; [R] WangPradelLiu2026 §4.2 (name level −45.6% time, safe on 99.6% of commits; side-effecting import-time functions select all, 5/50 matplotlib commits) |
| F7 | Order and isolation check *(new)* | At each checkpoint, run the selected tests of the last window in reversed order. An outcome change flags order dependence created by the edits (for example, caches). | [R] Parry2021 §3.2; [R] Lam2019iDFlakies; trigger [I] |
| F8 | Check the selector *(new; harness self-test)* | Replay checks: (1) an unchanged revision selects nothing; (2) a reversed real bug fix (BugsInPy) selects a failing test; (3) compare against RetestAll on synthetic edits. | [R] zhu2019rtscheck Table I, §III (rules R1/R5; DefectsEP reversal); [R] widyasari2020bugsinpy §2 |

## P — performance benchmarks

| ID | Rule | Trigger → action | Source basis |
|---|---|---|---|
| P1 | Profile-coverage selection | Run the benchmarks whose stored profile (taken at the pre-edit state) contains any changed function, or a caller of one within depth d. Always add the edit's target benchmark. | [R] mostafa2017perfranker (call-graph impact); [R] laaber2021tcp (dynamic coverage beats static). Coverage is necessary, not sufficient [R ding2020readily]; hence P7. Selection, as opposed to ordering, has no reported miss rate [U]. |
| P2 | Interleaved A/B measurement | Measure the parent and the candidate interleaved on the same machine (fixed-seed ABBA or randomised order, or duet), with a fixed plan of processes × values × warmups. pyperf's CPython default of 20 × 3 with 1 warmup is a starting point. | [R] laaber2019cloud (same instance, random order); [R] bulej2020duet; [F] asvdocs `--interleave-rounds`; [F] pyperfdocs; [R] kalibera2013rigorous (repetitions per level) |
| P3 | Statistical acceptance | Accept the speed-up only if the 95% confidence interval of the time ratio on the target excludes 1 and the point estimate beats a pre-registered minimum effect. Reject if any selected non-target benchmark's confidence interval lies wholly above 1 + ε. | [R] georges2007rigorous §3.3; [R] kalibera2013rigorous; [A] kalibera2020effectsize; [R] ding2020readily (effect size); [F] pyperfdocs (t-test). ε comes from P6. |
| P4 | Dynamic stopping | Stop the repetitions early when the RCIW (or CV) over a sliding window falls below a fixed threshold, with a hard cap. The threshold is frozen per benchmark from the A/A run. | [A] laaber2020dynamic; [R] traini2023steady (criteria; still suboptimal); [R] japke2025uoptime (RCIW preferable for Java). No Python study exists [U]. |
| P5 | Cumulative drift guard | At every edit, compare the *selected* benchmarks with the **original** baseline as well as the parent. Reject, or force a checkpoint, if the cumulative ratio passes a threshold. At each checkpoint, run the full set against the original. | [R] daly2020changepoint §1–2. MongoDB's earlier system compared with the last stable release but still missed slow drift, raised up to 99% false positives, and was replaced by change-point detection. So P5 must use the per-benchmark noise threshold from P6, not a fixed ratio. Threshold [I]. |
| P6 | Noise calibration and layout control | Run A/A (original against original) per benchmark per machine to set ε and the minimum detectable effect. Benchmarks with a high A/A false-alarm rate become informational only. Pin `PYTHONHASHSEED`, environment size and `pyperf system tune`. For C or Cython edits, optionally repeat with a second layout, and record instruction counts as a secondary signal. | [R] laaber2019cloud §5.3 (A/A); [R] mytkowicz2009wrong; [R] curtsinger2013stabilizer; [F] pyperfdocs (system tune); [F] codspeeddocs (instruction simulation); second layout [I] |
| P7 | Sentinel set *(new)* | A small fixed set of broad benchmarks runs on every edit, whatever the coverage says. Pick it once, by historical sensitivity or as a macro workload. | [R] laaber2022searchbased (history greedy, <1% overhead); [R] grambow2022microbenchmark (application benchmark as backstop); [R] chen2017exploratory (regressions come with unrelated changes) |
| P8 | Profile refresh *(new)* | Re-profile the benchmarks touched by an accepted edit. Re-profile all benchmarks at each checkpoint. Never use a profile older than the last checkpoint. | [R] japke2025uoptime, [R] laaber2022searchbased (depend on old runs); [A] alshoaibi2019price (decay); rule [I] |

## C — checkpoints and culprit finding

| ID | Rule | Trigger → action | Source basis |
|---|---|---|---|
| C1 | Periodic full checkpoint | Full clean build, full tests and full benchmarks every k accepted edits. Start at k = 4. Recalibrate k from the observed per-edit failure and noise rates with Najafi's cost model: about 1 + P(window fails)·2·log2 k runs per window (Najafi's 2·log2 n + 1 already includes the first batch run), plus the Eq. 7 flake term. | [R] najafi2019bisecting §2, §4–5, Eq. 7–8 (most savings by 4); [A] beheshtian2022batch; [R] memon2017taming (milestones). Moving from commit batches to edit batches is [I]. |
| C2 | Culprit finding | When a checkpoint fails, bisect over **prefixes** of the edits since the last green checkpoint. An unbuildable probe counts as SKIP. For performance failures, repeat each probe r times and use a ratio threshold, or a Bayesian noisy search. Allow "no culprit". | [R] najafi2019bisecting §2; [F] gitbisect (skip, run exit codes); [F] asvcommands (`find`, monotonic caveat); [R] henderson2023flake §III (noisy search, NONE outcome); [R] zeller1999yesterday §5 (UNRESOLVED) |
| C3 | Final full validation | The session's final version always gets a full clean build, full tests and full benchmarks against the **original** baseline. | Precedents: [W2] SysLLMatic final rebuild and re-measure; [W2] Meta full runs on master; [R] grambow2022microbenchmark daily backstop. Final-run rule [I]. |
| C4 | Revert semantics | Revert the culprit together with the later edits that depend on it, then re-validate the rest as a fresh window. If bisection is inconsistent (the culprit passes alone, or the failure disappears on rerun), use delta debugging over the window, or revert the whole window. | [R] zeller1999yesterday §1, §4–5 (interference, dd); [R] ananthanarayanan2019keeping §2.1 (real conflicts); [R] henderson2023flake §IV-C (verification by reruns) |
| C5 | Change-triggered checkpoint *(new; RQ3 part c)* | Start a full checkpoint before k is reached when an accumulated-change score since the last green checkpoint passes a threshold θ. The score counts changed lines and functions, F2 fallbacks, B2/B3 native or config edits, and the P5 cumulative-drift ratio. | Risk-guided testing [R] najafi2019bisecting §3 (risk models), [R] memon2017taming (frequently edited files break more); **Conceded prior art:** this is a deterministic variant of risk-mass batching. Sayedsalehi 2026 "-la" flushes when a cumulative (learned) risk sum passes a threshold, with time caps [R §VI-A]. Fallahzadeh 2025 studies variable, queue-driven batching [R §4.5]. Our score is model-free, and it sits on top of a per-edit reduced check. Required baselines: fixed-k (FSB), cap-only, and additive-budget at matched cost. Score and θ [I]. |
| C6 | Window record *(new; measurement)* | Each checkpoint records which misses the reduced checks made in the window and the delay in edits. These are the data RQ2 and RQ3 report. | [R] shi2018evaluating §3 (loss on future failures from a reduction point); [F] jin2021helped (missed or delayed failure observation); delay metric [I] |

## What W3 measures for each rule (see `review.md` §4)

- **End-to-end time, including overhead.** Build, selection analysis, dependency and profile collection, test run and benchmark run, against full validation. Report it both with and without collection (offline and online). [R] gligoric2015ekstazi; legunsen2016static
- **Safety.** Missed functional failures per edit against a shadow full run, using RTSCheck rule R1 and Legunsen's violation rate. Missed injected slowdowns, split into not selected / below noise / not covered, as Peass does. [R] zhu2019rtscheck; legunsen2016static; reichelt2023peass
- **Detection delay.** In edits, up to the catching checkpoint. Defined by us; no standard metric was found (G7).
- **Fault seeding.** Mutants both on and *off* the changed lines [A ojdanic2021evolving]. Reversed real Python bugs [R widyasari2020bugsinpy]. Optimization-specific faults (stale cache, float32, view instead of copy, removed lock) [I].
