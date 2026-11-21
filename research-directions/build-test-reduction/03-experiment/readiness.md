# W3-EXP readiness — reduced build/test/benchmark validation over replayed optimization edits

**Status:** v1.1, 2026-11-21. PM sign-off on v1 was GO with musts M1–M5 and additions A1–A2 (see `pm/tpm-log.md`, `pm/advisor/review-w3-readiness.md`); v1.1 folds them in, and they are marked **[M1]** etc. where they apply. **Run status (updated 2026-11-21 17:58 PKT):**
- **Harness:** `harness/bth/` is implemented, with 144 unit tests passing.
- **networkx:** the edit list is frozen (subject rule; see the §1.3 correction). The replay is built: 18 of 20 edits applied and 2 dropped for conflicts. The WSL environment (uv, CPython 3.12.16) is being installed. No FULL oracle numbers yet.
- **bottleneck:** mining done (20 of 20 qualify); replay and build setup are in progress.
- No timing results exist yet.
**Binding inputs:** `pm/CHARTER.md` (revised RQs 2026-11-21), PM/TPM rulings 1–6 (relayed 2026-11-21), W1 `01-literature/candidate-rules.md` v0 (rule IDs B1–B5, F1–F5, P1–P6, C1–C4).
**Evidence boundary:** every number in later results will carry the command, the raw output file under `results/raw/`, the target repo SHA and the harness SHA (working-tree hash, since this checkout is not committed by W3).

---

## 0. What this experiment answers

| RQ (revised) | What W3 measures | Primary output |
|---|---|---|
| **RQ1 Cost** | Per edit: build s, tests s, benchmarks s, under FULL validation, and the cumulative curve over the edit sequence. ≥2 projects, one with a real C build. | `results/rq1_cost.csv`, stacked-bar + cumulative figure |
| **RQ2 Existing, unchanged** | Incremental build, pytest-testmon, changed-module rule, run as shipped. Savings **including their own overhead**, misses on frozen injected faults/slowdowns, and a "why missed" note per miss. | `results/rq2_*.csv`, miss table with reasons |
| **RQ3 Our policy** | Accumulated-change selection + profile/call-graph benchmark selection + full check triggered by accumulated change, vs the best existing combination **at matched cost**, with an ablation per component. | cost-vs-misses frontier figure, ablation table |
| Meeting artefact | One fully worked edit, FULL vs REDUCED step by step with a diagram. | `results/worked-edit.md` |

Out of scope: any AI in the method; claims about a real "iterative session" effect (see T1).

---

## 1. Targets

### 1.1 Repository criteria (written before choosing; applied to every candidate)

1. Python project, maintained, pytest suite that runs in < 15 min on this laptop (12 threads, 7 GB RAM in WSL).
2. An in-repo benchmark suite (asv or pyperf-style), so performance oracles are the project's own, not ours.
3. Git history with ≥ 15 commits that pass the commit-mining rule (§1.3) inside one contiguous window.
4. Buildable on CPython 3.12 + gcc 13 without system libraries we cannot install (no sudo in WSL — see BLOCKER).
5. Across targets: at least one with a real compile step (C/Cython), at least one pure-Python.

### 1.2 Chosen targets

| Role | Repo | Why | Build | Tests | Benchmarks |
|---|---|---|---|---|---|
| **Pilot**, pure Python | `networkx/networkx` | 61 mining hits since 2024 (probe below); large, fast pytest suite (268 test files); asv suite in `benchmarks/` | none beyond editable install (B1) — build share expected negligible, reported as such per ruling 1 | pytest (+xdist for FULL) | asv (`benchmarks/benchmarks/*.py`, 15 files) |
| **C extension** | `pydata/bottleneck` | ~~17 `PERF:` commits~~ (old probe of the range `2b9c661^..933b653`, which missed the 3 earlier ones from 2019-09). Frozen rule output: **20 subject matches, 20 qualifying** in the window 2019-09-01..2021-01-01 at `b0815406` (`results/raw/bottleneck_mining.txt`), from `c9168481` (2019-09-07) to `933b6537` (2020-11-24). One contiguous burst by the maintainers — the closest thing in public history to a real step-by-step optimization session; 4 C extension modules generated from templates (`bn_template.py`), so incremental build is non-trivial and has known stale-dependency risk (`depends=` lists in `setup.py`) | setuptools `build_ext --inplace`; 4 extensions; template → `.c` generation | pytest | asv (`asv_bench/`) |
| Third (**cut first**) | `tobymao/sqlglot` | pure Python, 26 `perf(...)` commits since 2025, own `benchmarks/` (parse/optimize) | none (pure-Python mode; the optional Rust tokenizer is excluded) | pytest/unittest | `benchmarks/*.py` (to wrap) |

Rejected, with reason (recorded so the choice is auditable): `PyWavelets` (only 7 hits since 2020, none perf), `msgpack-python` (0 since 2020), `cytoolz` (2), `msgspec` (single 20k-line C file → incremental build = full build, few perf commits), `shapely` (needs GEOS system lib; no sudo), `more-itertools` (no benchmark suite).

**Risk on bottleneck [M4]:** the 2019–2020 sources must build on a modern toolchain. If the base does not build on CPython 3.12 with NumPy ≥ 1.26, the repo is **not swapped**. It gets its own older interpreter (CPython 3.8 + NumPy 1.19-era, contemporary with the commits), used for every arm and every state of that repo. Getting that interpreter needs uv-managed Python or deadsnakes, which depends on the environment decision in §9. Any compatibility patch is applied identically to every state and logged (T7).

**Build cost on a heavy project [A2]:** these targets will probably show a small build share, so after the networkx draft W3 takes **one cost-only RQ1 measurement on scikit-learn** (meson-python + Cython). It records four things: a clean build; an incremental build after a one-file `.pyx` edit (a fixed, pre-chosen file); the full test time; and the full asv benchmark time. This is a measurement only, with no replay and no safety arm.

### 1.3 Commit-mining rule (frozen before any run)

Deterministic, applied by `mine.py`, output committed to `edits/<repo>.json` before tests or selection rules are tuned:

1. Non-merge commits on the default branch whose subject matches (case-insensitive)
   `(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)`
   (`optimizer` deliberately does not match; sqlglot uses the `perf(...)` prefix and the regex is restricted to `^perf` there).
2. The commit changes ≥ 1 package source file (not under `tests/`, `benchmarks/`, `asv_bench/`, `doc*/`, CI) and ≤ 200 changed source lines.
3. Window: bottleneck 2019-09-01..2020-12-31; networkx and sqlglot: the most recent 20 qualifying commits before 2026-11-21.
4. All matches in the window are taken in chronological order; no manual inclusion/exclusion. Drops happen only by rule (§2) and are logged with reason. False positives of the regex (e.g. a commit that only mentions "vectorized" in a bug fix) stay in: they are still small edits.
5. Commits marked as AI-assisted in the message (sqlglot `[CLAUDE]`/`[CODEX]`) are **kept and flagged** (`ai_authored=true`); results are reported with and without them. The method itself uses no AI.

**Deviation 2 (2026-11-21 18:15; PM-approved with TPM conditions, `pm/tpm-log.md` Note 3). Window rule added:** *the window starts after the last whole-file reformat commit preceding the burst*.
- **Definition (deterministic):** a whole-file reformat commit is a non-merge commit in the window whose subject matches `(?i)\b(STY|style|format|black|ruff|cpplint|clang-format|reformat|lint)\b` and that changes ≥ 50 % of the lines of at least one package source file it touches.
- **Reason:** whole-file reformats inside the window make every later edit's diff fail to apply on the base. For bottleneck this left 5 of 20 edits.
- **bottleneck:** ~~window 2019-09-01..2020-12-31, base `22657ac`~~ → base `f51ed862e619dcff7b7b3691e58d5fc6ead4076b` (`after = 2019-10-06`). This gives 16 qualifying and 13 applied edits, with 3 conflicts: `cd32416d`, `8b587c5c`, `f1d14dc2`.
  - **Which commit the rule identifies (`scripts/reformat_check.py`, raw `results/raw/reformat_check_bottleneck.txt`):** the only whole-file reformat is `5851c10a` ("STY: format code base with black", 2019-10-05; worst file ratio 0.71).
  - ~~The earlier text named the cpplint/brace commits `3c92be0`, `77340a3`, `08bfc99`.~~ Those stay below 0.06 per file, so they are **not** whole-file reformats under the rule. They are still the likely mechanical cause of the old conflicts.
  - The base is the parent of the first qualifying commit after `5851c10a`. This is **below the 15–20 target and is not padded**. It covers only the later part of the PERF burst (T1/T5). The frozen 5-edit replay is kept as a sensitivity row.
- **Timing:** frozen at 18:15, **before any selection arm had run on bottleneck. No bottleneck selection, test or benchmark results existed** (only the S_0 functional build/test check).
- **networkx:** the same check finds no reformat commit between base `181f2951` and the last edit `2e0ae8ad`. The two subject hits, `8ec80c76` and `4792afb8`, have file ratios of 0.01 and 0.05. The window is **unchanged** (`results/raw/reformat_check_networkx.txt`).
- **sqlglot:** the check will be run if sqlglot is replayed.

**Correction (2026-11-21 17:40), applied before any replay or run:** the first-pass shell probe used `git log --grep`, which matches the *whole message*. The rule as written above matches the *subject*. `bth.mine`, which implements the written rule, failed the F8 reproduction check against the first pass. Four first-pass commits match only in their body, and all four are feature additions: `1660ac37` (is_perfect_graph), `32e06d5b` (magnetic_laplacian_matrix), `9150d1ea` (all_node_cuts fix), `fa30c164` (Constant-Potts Model). The written rule stands.
- Subject rule at HEAD `6c1a31d1`: 110 matches, 101 qualifying.
- **Latest 20:** `f618240c` (2025-08-02) to `2e0ae8ad` (2026-11-16).
- **Base B:** `f618240c^` = `181f295117f7f7488644c87f04699290f8e49188`.
- Raw output: `results/raw/networkx_mining_subject_rule.txt`. This list is now frozen.

The struck first-pass paragraph below is kept for the record.

~~**Frozen networkx edit list (2026-11-21 17:20):**~~ the rule above, applied to `networkx` HEAD `6c1a31d1`, gives 49 qualifying commits. The **latest 20** are used, from `1660ac37` (2025-10-17) to `2e0ae8ad` (2026-11-16). Base B = `1660ac37^` = `9c89eb0a4d65931178a8581b2e33488be576dd6a`. Raw output: `results/raw/networkx_mining_firstpass.txt`, from `scripts/mine_nx.sh`. `bth.mine` must reproduce exactly this list (harness self-test F8). If fewer than 15 survive replay, the window is extended by the next 5 older qualifying commits, repeated as needed. This extension rule was fixed before any replay.

Probe outputs so far (read in source, 2026-11-21, clones at `~/bt-lab/exp/repos`, `git log` on HEAD of default branch): networkx 61 hits since 2024-01-01; bottleneck 17 `PERF` commits in `2b9c661^..933b653` (157 commits in that range); sqlglot 26 `^perf` since 2025-01-01. Commands in `scripts/mine2.sh`, `scripts/probe2.sh` (to be copied into `03-experiment/scripts/`).

### 1.4 How this avoids cherry-picking

Criteria and regex written before looking at test/bench outcomes; all hits in the window are used; drops are rule-based and published with counts; edit lists, mutant sets and slowdown sets are frozen (hash recorded in `results/frozen.md`) before any selection rule is configured; rule parameters (k, T) are fixed in `rules.md` a priori and reported as sensitivity curves, never picked against the frozen faults.

---

## 2. Iterative session = replay (and its limit)

- **Base B** = parent of the oldest selected commit. Tests and benchmarks are **frozen at B** (perf edits are behaviour-preserving, so B's tests are a valid oracle; this also removes tests written with hindsight of the edit).
- **Step i** applies only the package-source part of commit *c_i* (`git diff c_i^ c_i -- <src>`) onto state *S_{i-1}* with `git apply --3way` in a scratch worktree under `~/bt-lab/exp/work/`; each state is committed there, giving a stable state SHA.
- **Drop rules** (construction time, before any arm runs): (a) apply conflict; (b) FULL tests fail at *S_i* (edit depended on an un-replayed change); (c) build fails. Each drop is logged. Target 15–20 surviving edits per repo (ruling 5).
- No edit is generated by any model; replay order = history order.
- **Limitation (ruling 6):** this is a sequence of independent historical commits re-based onto one tree, not a recorded optimization session. We claim nothing about how real sessions differ (edit locality, revisits). Named as T1.

---

## 3. Arms compared per step (mapped to W1 rule IDs)

Every arm sees the same state sequence *S_0..S_n*. The **oracle** for every state is FULL (ruling 2).

| Arm | Build | Tests | Benchmarks | Checkpoint | Rule IDs |
|---|---|---|---|---|---|
| **A0 FULL** | clean rebuild per edit, the procedure existing benchmarks use: `pip install -e .` / `build_ext` in SWE-Perf, GSO and SWE-fficiency (per W2 `02-practice-survey/`) | all | all | every step | B3-style clean, C3 |
| **A1 INC** | incremental (B1 for `.py`, B2 for native) | all | all | — | B1, B2 |
| **A2 TESTMON — "PerfAgent-style per-edit RTS"** (existing, unchanged) | incremental | `pytest --testmon` as shipped. PerfAgent already uses this per edit (arXiv 2607.19653 §III-D, via W2), so **per-edit RTS is not our contribution**. Our contribution is the build side, benchmark selection and the accumulation/checkpoint policy. | all | — | B1, B2, F1 (testmon) |
| **A3 CHANGED-MODULE** (naive, existing) | incremental | test files named after / in the package dir of changed modules | benchmark files named after changed modules | — | B1, B2, W3-new "naive name rule" |
| **A5 STATIC-BENCH** (existing idea, **[A1]**) | incremental | testmon (as A2) | benchmarks reachable from the **current edit's** changed functions in a **static** import/call graph of the package (STARTS-style class/module-level dependency analysis, applied to benchmarks instead of tests) | — | B1, B2, F1, W3-new "static benchmark RTS" (STARTS: Legunsen et al. 2016/2017, to-verify by W1) |
| **A2/A3/A5 + k** | as above | as above | as above | full every *k* steps, *k* ∈ {3,5} for the draft; {2,8} after it **[M3]** | + C1 (periodic), C3 |
| **A4 OURS** | incremental + B4 differential at checkpoints | function-level dependency selection on the **accumulated** changed-function set since the last green full check, + F2 native fallback, + F4 always-run, + F5 flaky quarantine | profile/call-graph selection: benchmarks whose stored profile reaches an accumulated changed function (P1), measured P2/P3 | full check when accumulated-change score ≥ T (C1-triggered), and final (C3); on failure culprit bisection (C2) | B1, B2, B4, F1*, F2, F3, F4, F5, P1, P2, P3, P5, C1, C2, C3 |
| **A4 − accum** | | current-edit changed set only | current-edit only | same trigger | ablation (a) |
| **A4 − profile** | | as A4 | changed-module benchmark rule | | ablation (b) |
| **A4 − trigger** | | as A4 | as A4 | fixed period *k* = 5 instead of score trigger | ablation (c) |

\* F1 at **function** granularity (W3-new refinement of F1): dependency map = per test, the set of functions (Python *and* native entry points) it calls, recorded with `sys.monitoring` (PEP 669, CPython 3.12) `PY_START`/`CALL` events. Native entry points appear as C callables (e.g. `bottleneck.reduce.nansum`), which coverage-based tools (testmon) cannot see — this is a stated hypothesis, measured, not assumed. A 2026 preprint, "NameRTS", reports that file-level Python test selection saves little (≈3 % in their setting) and that name/function-level selection saves much more (via W1, **unverified**). Our functional selection is therefore function-level, and A3 stays as the file-level naive baseline. If NameRTS publishes usable code, it becomes an existing function-level comparator after the draft; otherwise it is cited once W1 verifies it.

**Changed-function extraction** (deterministic): Python — AST of pre/post file, qualname of every `def` whose line span overlaps a hunk; module-level hunk → all functions of the module (conservative). C — hunk → enclosing C function by brace scan of the template/source; template name → Python name by the project's naming rule (`nansum_all_DTYPE0` → `nansum`); edit to a header/macro → all functions of every extension that includes it (F2-style).

**Mapping to W1 candidate-rules v1.1 (2026-11-21):**
- **Test selection:** A4's function-level selection is a **variant of F6**. It uses function granularity from `sys.monitoring`, not testmon's block checksums, and it also sees native entry points. An edit to import-time/module-level code expands to every function of the module, which is F6's import-time fallback (F6 select-all applies only to side-effecting import-time code, per v1.1).
- **RQ3 components:** (a) accumulation = C1/C5/P5/F3; (b) profile-based benchmark selection = P1 + **P8** (profile refresh at each green full check, never older than the last checkpoint; the optional P7 sentinel set is not in the draft); (c) triggered full check = **C5**, framed as a model-free variant of risk-mass batching (via W1). Every checkpoint writes a **C6** window record (misses and delay).
- **Supporting rules:** **B6** (null-rebuild guard) is added to B4 for bottleneck. **F8** is covered by the §7 harness self-tests (an unchanged revision selects nothing; mine reproduces the frozen list). **C7**, stale dependency data, is exercised by the §4.1b latent-fault class.
- **P5 and the noise floor:** P5's comparison against the original **uses the P6/§5 noise threshold** (the 1 + 3·σ_noise condition in §4.2). MongoDB dropped its stable-release comparison after up to 99 % false positives (via W1).
- **Cost model:** the C1 cost formula (1 + P·2·log2 k, W1) is used to state the expected checkpoint + bisection cost next to the measured one.
- **Matched-cost comparators:** fixed-k is in the draft. The C5 **cap-only** and **additive-budget** baselines come after the networkx draft and are cut first.
- **NameRTS** (github.com/ZJU-CTAG/NameRTS, Python 3.13) is a **planned post-meeting comparator**, not run before the meeting because of the slow network.

**Precedents for checkpoints (C1/C3), via W2:** SysLLMatic does a final rebuild and re-measure (C3-like). Meta and Google run periodic full runs on master (C1-like). Cumulative re-checks across edits are otherwise rare in optimization systems. Exact citations will be taken from W2's notes.

**Accumulated-change score** (A4, fixed a priori): `score = |changed functions since last green full check| + 5 × (native-header edits) + 5 × (F2 fallbacks)`; trigger at T = 10; sensitivity T ∈ {5, 10, 20} reported as curve only.

**Matched cost (RQ3):** the best existing combination is the best of A2, A3 and A5, each with a periodic full check every *k* steps. Sweeping *k* gives a cost-vs-detection frontier. No parameter is tuned on the frozen fault sets.

**Headline for RQ3 [M2]: cost at equal detection.** Injected faults sit in edited functions and are filtered by FULL, so any sound selector tends to catch them at the injection step almost by construction. Miss counts on that class therefore separate the arms poorly. The headline is: *estimated seconds needed by each arm to reach the detection level of FULL on the frozen set*, with misses reported alongside. Profile-based benchmark selection (P1) must beat **A5**, the existing static dependency rule, not only the file-name rule A3. The A4 bundle has many rules, so results also report which few rules drive each saving or miss (per-rule attribution from the ablations and the per-miss "why").

---

## 4. Safety measurement

### 4.1 Frozen injected faults (functional)
- ~25 mutants per repo, each placed **in a function changed by edit *s*** (so it is plausibly what a bad optimization would introduce), with a deterministic operator list (relational flip, ±1 constant, `+`↔`-`, `and`↔`or`, drop `return` value; C: same operators on the template) and a fixed seed for site choice. Generated once, frozen, hashed.
- A mutant enters the set only if FULL tests kill it at *S_s* (≥ 1 failing test, not a quarantined flaky test). Survivors are counted and reported (they are undetectable by the oracle, not "missed").
- **Kill set** K(m) = failing tests under FULL at *S_s*+m. Detection for an arm at step *t* ≥ *s*: `selected_tests_arm(t) ∩ K(m) ≠ ∅`, or a full check runs at *t*. The mutant persists until detected (it is in the code). **Detection delay** = *t* − *s*; undetected by end ⇒ caught by C3 final check (delay = n − s) for arms with C3, else **missed**.
- Validity check of the kill-set reuse assumption: for 5 mutants per repo, re-run FULL at *S_{s+3}* and compare K(m) (reported).
- testmon is not simulated at the injection step: we run it for real at *S_s*+m (its own DB state from the clean replay); later steps use its real clean-replay selections ∩ K(m).

### 4.1b Latent faults (≈ 5 per repo) — makes accumulation testable [M2b]

**Mechanism under test.** Accumulated selection (A4) re-selects the tests of every function changed since the last green full check. Current-edit selection (A4 − accum) selects only the tests of edit *t*. The two differ only when a fault introduced at step *s* is **not** detectable at *S_s* but **becomes** detectable at a later state *S_t* (*t* > *s*). For example, edit *t* changes a caller's control flow or input shapes so that the faulty path in *f_s* is now exercised by tests. Accumulation then still selects *f_s*'s tests at *t*, while current-edit selection selects only *f_t*'s tests.

**Construction (deterministic, frozen with the other sets).** Two sources:
1. **Delayed-visible mutants:** take mutants of §4.1's operator list placed in functions changed at *s* (and in their direct callers, one call-graph hop) that **survive** FULL at *S_s*. Re-check them at every later state *S_{s+1}..S_n*; this re-check runs only the tests whose dependency map reaches the mutated function at that state. A mutant whose kill set first becomes non-empty at *t* > *s* is latent, with visibility step *t*.
2. **Caller faults:** mutants in a direct caller *g* of a function changed at *s*, where *g* is not itself in edit *s*. These test whether the selection rule's dependency reach includes callers.

Up to 5 per repo are taken in a fixed order: by step, then by seeded site order.

**Detection** is checked again at each step from *t* on: an arm catches a latent fault at step *u* ≥ *t* if its selected tests at *u* intersect K(m, *S_u*).

**Pre-registration.** If fewer than 3 latent faults per repo exist, the accumulation ablation (a) is **expected to show no effect**, because every frozen fault is visible in the step that introduces it. It is reported as such, not as evidence for or against accumulation.

### 4.2 Frozen injected performance regressions
- 5–10 per repo, each ≥ 2× slower on ≥ 1 benchmark under FULL (ruling 2), plus 3 per repo of **moderate** strength, 1.2–1.5×, near the threshold. Only the moderate class can show misses that come from benchmark selection rather than from the measurement threshold (advisor review). **Natural reverts are reported separately from synthetic slowdowns [M2].** (i) **natural** — revert of an earlier replayed speed-up whose FULL effect is ≥ 2×; (ii) **synthetic, deterministic algorithmic** — in a function changed by edit *s*: list instead of set/dict membership, repeated recomputation of a pure sub-result, `sorted()` copy inside a loop; C: an extra full pass over the array. Frozen and hashed like mutants.
- **Speed-up/regression decision (fixed before runs; a published rule, applied identically in every arm):** the **asv rule**. Benchmark *b* changed significantly if the ratio time(*t*)/time(ref) is > 1.1 (regression) or < 1/1.1 (speed-up), **and** the Mann-Whitney U test on the raw samples gives p < 0.002. These are asv's `compare` defaults (`--factor 1.1`; statistical test in `asv.statistics`), to be verified against the asv source by file and commit. asv is chosen over the SWE-Perf rule (3 warmups + 20 reps, IQR filter, MWU p < 0.1, ≥ 5 %) because both main targets ship asv suites. The SWE-Perf rule is reported as a sensitivity check. The rule is applied for ref = **original base B** and, separately, ref = **previous accepted state**. As a further condition, the ratio must exceed the noise floor: 1 + 3·σ_noise(b), with σ_noise(b) from the §5 control. Cases where the asv rule fires but are below the noise floor are counted and reported.
- Detection by an arm at *t*: a benchmark it runs satisfies the definition. Delay and misses as in 4.1.

### 4.3 Reduced-build correctness (B4)
For bottleneck at every step: incremental vs clean build — (a) SHA-256 of each `.so` after `strip --strip-debug` (and of the generated `.c` files); (b) FULL test outcomes on both; (c) a targeted probe: a header-only / template-only edit, checking whether `build_ext` recompiles the dependent extensions. Any mismatch is a finding and switches A4 to clean builds (B4 rule). For pure Python: stale-`.pyc` check by running with `PYTHONDONTWRITEBYTECODE`/hash-based pycs vs default.

### 4.4 Reporting
"k of N missed" with a Wilson 95 % CI per arm and repo; never "0 misses = safe" (ruling 2). Every miss gets a one-line *why* (e.g. "native change invisible to coverage", "test reached function only through module-level import", "benchmark profile taken before the call path existed").

---

## 5. Metrics and timing protocol

**Headline (deterministic, ruling 3):** the headline metrics are tests run, benchmarks run and **estimated seconds**. Estimated seconds sum four parts:
- per-test durations from a **serial** FULL run (no xdist), median over repeats **[M1]**;
- per-benchmark durations from the FULL runs;
- measured build time;
- measured selection overhead (map collection, profiling, diffing). This is charged to the arm that uses it and amortised over the steps it serves.

**Secondary (measured wall time):** 5 edits per repo × 5 interleaved repeats per arm, with the arm order rotated each repeat. Every arm uses the **same `pytest -n`** setting **[M1]**. The cache policy is fixed per arm: A0 always deletes `build/`, `.so`, `__pycache__` and the testmon DB, and the incremental arms keep them.

**Noise-floor control:** the same state is measured twice (S_0 vs S_0), with FULL benchmarks interleaved and 5 repeats. This gives a per-benchmark ratio distribution and σ_noise(b). A same-commit-twice FULL test run is also done as the flaky check (F5, ruling 5).

**Oracle repeatability (PM must, from W2 F8):** FULL's performance decision is itself noisy. arXiv 2607.01211 reports that reference patches pass their own benchmark's speed-up rule in all 12 cross-machine replays only 39/102 (GSO), 11/140 (SWE-Perf) and 411/498 (SWE-fficiency). So the full asv-rule decision is re-run **≥ 3 times, interleaved,** on a fixed subset: S_0, three states fixed in advance (steps 5, 10, 15) and 2 injected-slowdown states.
- Per (state, benchmark), the agreement rate is the fraction of repeats in which the verdict (faster/slower/same vs ref) matches the majority.
- A reduced arm's regression "miss" on a (state, benchmark) where FULL's verdict flips across repeats is labelled **oracle-unstable** and not counted as a miss. It is reported separately.
- Budget: ≈ 1 h of machine time for networkx. If the full asv suite makes it longer, the subset of benchmarks is fixed in advance (those reaching any edited function, plus 10 chosen by seeded draw) and the PM is told.

**Idle-machine gate [M5]:** noise-floor and wall-time runs start only if the 1-minute load average (`/proc/loadavg`) is ≤ 1.5 and no other heavy process is visible (`top -bn1`), sampled before and after each run. Above 1.5 at start, the run is postponed. If the load goes above 1.5 during a run, the run is aborted, or kept and labelled **noisy**. Count-based and estimated-seconds metrics are not gated.

**Environment:** WSL2 Ubuntu 24.04, CPython 3.12.3, gcc 13.3, i5-12400F (6C/12T). CPU governor **cannot be pinned** (no cpufreq in WSL, no sudo) → mitigations: `taskset -c 2-5` for benchmark processes, AC power, no other experiment running concurrently (other sessions' load is logged with `uptime` before/after each run), benchmarks with fixed warmup + ≥ 5 processes × ≥ 3 values (pyperf-style), raw samples kept. Every reported time is labelled **measured** (CI width < 10 %) or **noisy**.

**Per-step and cumulative metrics:** wall/estimated time per step (build, select, test, bench); cumulative session time; missed failures; missed regressions; detection delay; **speed-up estimation error** = |log(speed-up from arm's selected benchmarks) − log(speed-up from FULL benchmarks)| for each edit's intended effect.

---

## 6. Threats to validity

- **T1 Replay ≠ session.** Independent historical commits re-based on one tree; real sessions may revisit the same functions (which would *favour* accumulation). No iterative-session effect is claimed.
- **T2 Injected ≠ real faults.** Mutants and synthetic slowdowns may be easier/harder than real optimization bugs; mitigated by placing them in changed functions and including natural reverts.
- **T3 Kill-set reuse** across steps (4.1) — checked on a sample.
- **T4 Noisy laptop timing**, no governor pinning — counts/estimated seconds are the headline; wall time secondary and labelled.
- **T5 Target selection** — 2–3 repos, pure Python + one C template project; not generalisable to C++/Rust/meson-heavy builds.
- **T6 Frozen-at-B tests** may under-test code paths added by later edits (benchmarks too); FULL oracle shares this limit.
- **T7 Old toolchain drift** (bottleneck 2019–20 on NumPy 1.26/2.x) may force patches; any compatibility patch is applied to every state identically and logged.
- **T8 AI-flagged sqlglot commits** — reported separately.
- **T9 Our harness bugs** — mitigated by §7 test matrix and the critic pass.

---

## 7. Test matrix for the harness itself (tests first)

| Unit | Cases |
|---|---|
| `mine.py` | regex hits/non-hits golden list (incl. "optimizer" non-hit); path filter; line cap; deterministic output (run twice → identical JSON) |
| `replay.py` | clean apply; conflict → drop logged; FULL-fail → drop; state SHAs stable across runs |
| `changed_fns.py` | Python: add/modify/delete function, method in class, decorator line, module-level edit → all; C: hunk inside function, header edit → all ext functions, template name mapping |
| `depmap.py` | toy package: test → called functions incl. a C builtin; refresh after edit (F3) |
| `select.py` | each arm's rule on toy data; accumulation reset only on **green** full check; trigger fires at T; F4 always-run; F5 quarantine |
| `safety.py` | detection/delay simulation on hand-built kill matrix (caught at s, at checkpoint, at final, missed); latent fault visible only from step t (accumulating arm catches at t, current-edit arm does not); Wilson CI values vs reference |
| `staticgraph.py` (A5) | toy package: benchmark → module → function reachability via imports and direct calls; changed function reached only through a call chain of length 2 |
| `bench.py` | ratio + bootstrap CI on synthetic samples with known 1.0×/2.0× effect; regression definition both refs |
| `cost.py` | estimated-seconds accounting sums; overhead charged once and amortised |
| `buildcheck.py` | differential detects a deliberately stale `.so` on a toy C ext |
| End-to-end | toy repo (2 modules, 1 C ext, 6 tests, 3 benchmarks), 4 edits, 1 planted mutant + 1 planted slowdown: FULL catches both; A3 misses the planted cross-module one; numbers match hand calculation |

---

## 8. Schedule (from sign-off ≈ h0 = 2026-11-21 17:30 PKT) and cut order

| Hours | Work |
|---|---|
| 0–2 | Environment (BLOCKER below); try building the bottleneck base on 3.12, with an older Python if it fails **[M4]**; time one serial FULL run per repo (first RQ1 numbers) |
| 2–8 | Harness core via Sonnet implementers, tests first: mine, replay, changed_fns, depmap, select (incl. A5 static graph), cost |
| 8–10 | Freeze edits, mutants, latent faults and slowdowns for networkx; flaky 2-run check; noise floor (idle-gated) |
| 10–12 | Critic subagent (diff + this doc; blocking: wrong/misattributed number, unsafe measurement, hindsight leakage) → fixes |
| 12–20 | **networkx end-to-end: RQ1 + RQ2** (overnight FULL oracle + kill sets). **Go/no-go at h20 [M3]** |
| 20–24 | First RQ3 on networkx (A4 vs A5/A2 + k ∈ {3,5}); **draft results.md** at h24 |
| 24–32 | Bottleneck end-to-end; after the draft **[M3]**: ablations, k ∈ {2,8}, B4 build check, scikit-learn cost-only measurement **[A2]**, wall-time repeats |
| 32–36 | rules.md, README, worked edit (bottleneck, per advisor) + diagram, final results.md; sqlglot only if time |

**Cut first if late:** (1) sqlglot; (2) wall-time repeats (the estimated-seconds headline stays); (3) bottleneck mutants 25 → 15; (4) ablation (c) and k ∈ {2,8}; (5) the B4 build check; (6) at h20, if networkx RQ1+RQ2 is not running end-to-end: networkx only, labelled **pilot** (TPM fallback).

---

## 9. BLOCKER and ASK

WSL Ubuntu has **no `pip`, no `python3.12-venv` (ensurepip missing), no `Python.h` (python3.12-dev)**, and `sudo` needs a password, so no virtualenv and no C-extension build is possible yet. Options (one needed):

1. **(Preferred)** The user runs once in WSL: `sudo apt install -y python3.12-venv python3.12-dev python3-pip`.
2. W3 installs `uv` (official Astral release binary from GitHub, user-space `~/.local/bin`, ~15 MB) and uses uv-managed CPython 3.12 (includes headers). This needs explicit approval because it downloads a binary. It also covers M4: uv can supply an older CPython (e.g. 3.8) for bottleneck without sudo. With option 1, M4 would instead need deadsnakes (`sudo add-apt-repository ppa:deadsnakes/ppa`).

No install happens until the user's choice is relayed (PM instruction, 2026-11-21).

Low-risk setup already done: blobless clones of candidates in `~/bt-lab/exp/repos` (WSL disk, per ruling 3); toolchain check (gcc 13.3, git, taskset present; ccache absent; cpufreq absent).
