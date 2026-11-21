# TPM log: Study 1 (reduced build and test validation)

Owner of this file: TPM subagent. Read-only elsewhere. Newest entry first.

---

## 2026-11-21 (late): Note 3. Bottleneck window amendment and stale-build finding (FYI from PM; no NO-GO)

**Window amendment** (base f51ed86, 13 edits; the old window applied only 5 of 20 edits; the 5-edit run is kept as a sensitivity check). **Acceptable**, for three reasons:
- The trigger was apply conflicts, which are known at construction time. It was not test, benchmark or arm outcomes.
- The change was frozen before any arm ran.
- It is logged as a deviation.

Three conditions for the record:
1. **State the amendment as a rule, not a hand-picked SHA.** For example, "the window starts after the last commit that reformats more than X% of package lines". Apply the same check to networkx and sqlglot, and log whether it changes them.
2. **13 edits is below the 15-20 target.** Report n=13 as such and do not pad.
3. **Disclose the effect on representativeness.** The surviving window is the later part of the PERF burst, so it is not the full 2019-20 session. Add this to T1/T5.

**Stale-build hazard** (`iterators.h` is missing from `setup.py` `depends=`). This is a genuine RQ2 finding about incremental builds. Its evidence level depends on how it is triggered:
- If one of the 13 replayed edits touches `iterators.h`, it is a **natural** miss.
- If it is shown only by a constructed header edit, label it a **probe**, not an observed failure in the replay.

Before claiming it is an upstream defect, check the current upstream `setup.py` (it may already be fixed). Cite the file and commit.

Consequence for A4: B4 switches to clean builds, and that cost must be charged to A4.

Expected evidence (as the PM asked):
- `.so` hashes after `strip --strip-debug`, clean vs incremental;
- the test outcomes that differ;
- the benchmark ratio with its CI against the noise floor.

If the hashes differ but no test or benchmark changes, report it as "stale artefact, no observed behavioural effect". Do not report it as a missed fault.

---

## 2026-11-21 (evening): Review 2, W3 `03-experiment/readiness.md` DRAFT v1 (repo HEAD a9de702, uncommitted)

**Verdict: GO-with-musts.**

### Status of Review 1's musts against this document

| Review 1 must | Status | Where in readiness.md |
|---|---|---|
| R1 build definition | Closed | §1.2. Networkx's build share is reported as negligible. Bottleneck is a real C build, and §4.3 adds a check that the incremental build gives the same result as a clean build. |
| R2 non-circular safety | Partly closed; new bias found, see M2 | §4. Fault sets are frozen and hashed, FULL is the oracle, and results are reported with a Wilson CI. |
| R3 noise and caches | Mostly closed; gaps M1 and M5 | §5. Headline is estimated-seconds, with an A/A noise floor, `taskset` pinning, and a fixed cache policy per arm. |
| R4 fair baseline | Closed | §3. Testmon and the changed-module rule run as shipped, plus a matched-cost frontier from the k sweep. |
| R5 cherry-picking | Closed | §1.1-1.4. Criteria were written first, the regex is frozen, all hits in the window are used, and rejected repos are logged with reasons. |

The document also maps well onto the revised charter RQ1-RQ3 (§0). Threat T1 (replay is not a real session) is stated, and the doc does not claim any iterative-session effect.

### New musts

- **M1: Same parallelism in every arm.** §1.2 runs FULL with pytest-xdist. Per-test durations measured under xdist, or wall-time compared across different `-n` values, would bias the savings figures.
  - Fix: collect per-test durations from a serial run (`-p no:xdist`). Wall-time repeats use the same `-n` in every arm.
  - Cost: 0.5 h config, plus about 1 h extra machine time for the serial FULL pass.
  - Why before the meeting: every RQ1 and RQ2 number depends on it.
- **M2: Disclose the construction bias in the injected faults.** Mutants and synthetic slowdowns are placed in functions that the edit changed (§4.1-4.2), and kept only if FULL detects them. A synthetic slowdown that FULL detects must lie on some benchmark's call path. So profile/call-graph selection (P1) detects it almost by construction, and the same holds for function-level test selection (F1) with mutants. That makes RQ3(b) partly circular.
  - Fix: report RQ3 detection separately for natural reverts and for synthetic injections. State that the synthetic results measure how complete the dependency map is, not how good the selection is. Headline RQ3 on cost at equal detection, plus the misses on natural reverts.
  - Cost: 0.5 h of writing. Optional recommendation: about 5 mutants per repo in callers of changed functions or in shared state, 2 h.
  - Why before the meeting: the advisor will ask why OURS catches 100%.
- **M3: Fix the critical path to the meeting.** RQ1 plus RQ2 end-to-end on networkx by h20 is the go/no-go point. The full A4 combination of rules, three ablations, the k sweep beyond {3,5}, and the incremental-vs-clean build check on bottleneck (§4.3) come after the draft.
  - Cost: 0 h (reordering only).
  - Why: the highest-risk code is the A4-only work, namely the sys.monitoring calls into C, the template-to-Python name mapping, and the C hunk-to-function brace scan. Without a fixed critical path that work can starve the baseline results.
- **M4: Build bottleneck on a contemporaneous interpreter if 3.12 fails.** The current fallback in §1.2 (shapely, or dropping the safety arm) is weak. The 2019-20 sources are more likely to build on CPython 3.8 with NumPy 1.19-era wheels than on 3.12.
  - Fallback: a uv-managed CPython 3.8 (or 3.9) for bottleneck only, recorded as threat T7.
  - Cost: 1 h.
  - Why before: without it the C repo, and with it build-reduction safety, may disappear.
- **M5: Keep timing runs away from other sessions' load.** The noise-floor and wall-time runs must happen when the other sessions are idle (architect implementers, W1/W2 fetches). If the 1-minute load average exceeds 1.5, the run is aborted or labelled "noisy". Logging `uptime` alone does not protect the numbers.
  - Cost: 0 h of engineering; about 0.5 h of PM coordination.

### Other notes (not musts)

- The kill-set reuse check (T3) and the stated function-level testmon hypothesis are good.
- Ask: record harness SHAs by committing W3's working tree on its branch, rather than working-tree hashes, if the charter's branch rule allows.
- **sys.monitoring overhead.** CALL-event tracing on the whole networkx suite may run 5-10x slower than normal (inferred). It is charged to A4 as overhead, which is correct. Budget for it overnight.

### Answer to the PM: Docker or uv as the fallback

**Ranking:**
1. apt (the user runs one sudo command; distro Python, zero new trust).
2. User-space uv.
3. The `python:3.12` container.

**Why uv beats Docker:**
- uv runs on the same WSL ext4 disk where the repos already are.
- There is no extra VM or daemon, and `taskset` applies directly.
- It allows different interpreters per repo (M4).
- Its standalone CPython builds use PGO/LTO, so absolute speed differs from Ubuntu's Python. That is harmless because every arm uses the same interpreter.

**When Docker is acceptable:**
- Every arm, the noise floor and the oracle run in the same container image, pinned by digest.
- Repos live in a container volume, not a bind mount from `/mnt/c`.
- `--cpuset-cpus` is set.
- The Docker Desktop VM is not competing with WSL jobs.

**Approvals:** both uv and Docker download third-party artefacts (the Astral release binary, or the Docker Hub image). Either way the user must approve the download; it cannot be authorised by an agent.

---

## 2026-11-21: Review 1, charter (`pm/CHARTER.md`)

**Verdict: GO-with-musts.** W1-LIT and W2-PRACTICE are low-risk document work and can run as written. W3-EXP is feasible in about 40 h only if the musts below are in place before results are produced. Without them, the RQ3 numbers would not survive the advisor's first two questions: "What does 'build' mean in Python?" and "How do you know you missed nothing?"

Inputs read: CHARTER.md (full); prior package README and `06-evaluation-protocol.md` (skimmed: measurement controls, A/A controls, comparator list). `C:\Users\pc\study\bt-lab\` does not exist yet (checked 2026-11-21).

### Charter observations

1. RQ3 combines three separate reductions (build, functional tests, benchmarks) with two failure types (functional, performance). That is six result cells. A 40 h pilot can fill about three of them credibly.
2. "Build" is not defined. Most Python code has no compile step. If no definition is fixed, the build-reduction result will be a trivial zero or will be filled by environment-install time, which nobody reduces in practice.
3. "Replaying real historical optimization edits as an iterative session" sounds like accumulated state, but historical perf commits are not adjacent. Unrelated commits sit between them. A replay at parent-to-child of each commit is honest. Calling the result a "session" overstates it.
4. The safety measurement is not specified beyond "injected faults/regressions and periodic full checks". This is where circularity can enter (see R2).
5. There is no named established baseline. "Full versus reduced" alone is an unfair comparison (see R4).
6. Rule 4 puts clones at `C:\Users\pc\study\bt-lab\`. If the experiment runs in WSL or Docker against `/mnt/c`, file I/O becomes several times slower and noisier. That distorts every timing number (see R3).

### Top risks

| # | Risk | Effect if ignored | Mitigation (smallest must) | Cost | Why before the meeting |
|---|---|---|---|---|---|
| R1 | Build dimension degenerate in pure Python | "Reduced build" claim is empty or misleading | Write a one-paragraph operational definition of build (C or Cython extension compile + editable install + bytecode; exclude dependency resolution). Measure the build share of total validation time on each target repo first. If it is under about 5%, report "build measured, negligible" and drop build reduction from RQ3 results. To keep the build claim, include at least 1 repo with a compiled extension. | 1-2 h | The advisor's first question. A wrong framing wastes the whole W3 compute budget. |
| R2 | Circular or vacuous safety evaluation | Real perf commits rarely break tests, so "0 misses" is trivially true. If faults are designed knowing the rule, the miss rate is biased. | Use an independent oracle: the full suite plus full benchmarks on every evaluated state. Inject deterministic functional mutants (operator, constant, and return mutations inside the changed functions, using a fixed seed) and synthetic perf regressions large enough to beat noise (2x or more, for example an inserted loop or a sleep proportional to input). Generate and freeze both injection sets before the selection rule is finalised. Report the miss rate with counts and an exact binomial CI, never as a bare 0%. | 4-6 h | Without this, RQ3's safety half has no number. |
| R3 | Timing noise and cache contamination on a laptop | Savings or speed-ups are artefacts of thermal state, page cache, `__pycache__`, `.pytest_cache`, testmon DB, pip cache, or `/mnt/c` I/O. | Headline savings in deterministic units: tests executed, benchmarks executed, and estimated test-seconds (per-test durations from the full run). Report wall time only as secondary, with 5 interleaved (ABAB) repeats on a subset. Fix cache policy per arm (cold or warm stated, identical for both arms, cleared in a script). Run on WSL ext4 (`~/bt-lab`), not `/mnt/c`, on AC power with no other load. Include one A/A run (same commit twice) to show the noise floor. Detect perf regressions only above the measured noise floor. | 2-3 h (plus about 0.5 h PM decision on the clone location vs Rule 4) | Advisor will ask for the noise floor. Without it no perf statement is defensible. |
| R4 | Unfair baseline (reduced vs naive full only) | Any selection looks good against "run everything". | Add at least one established deterministic RTS comparator: pytest-testmon (coverage-based, Ekstazi-like) and a simple "tests in or importing the changed module" static rule. The student's rule must be compared with these, not only with full. | 2-3 h | "Did you compare with existing RTS?" is a predictable question, and W1 will cite these tools anyway. |
| R5 | Cherry-picked repos and edits, plus feasibility | Results reflect the hand-picked cases. A large suite makes replay infeasible in time. | Pre-declare and record repo-selection criteria (pytest suite 1-10 min, an existing benchmark suite (asv or pytest-benchmark), at least 15 perf commits, Linux-buildable) and the commit-mining rule (message regex `perf\|speed\|faster\|optimi[sz]`, touches `.py`, tests pass at both parent and child). Freeze the edit list with its SHA before running any arm. Record exclusions with reasons. Run the full suite twice at a parent commit to flag flaky tests and exclude them openly. | 3-4 h | Advisor-level validity question; also determines whether the compute fits. |

Other threats, recorded but not musts for the meeting:
- **Test-order dependence.** Computing reduced-arm outcomes from the full-run oracle assumes that a test's result does not depend on the other tests in the run. Spot-check on 3 edits by actually running the reduced subset.
- **Historical speed-ups may not reproduce on this hardware.** Report the reproduction rate. Do not treat it as a failure of the method.
- **Benchmark coverage of edited code may be zero for many commits.** Report this; it is itself an RQ1/RQ4 finding.
- **Windows-only packages.** Run everything in WSL to avoid them.

### Feasibility and compute estimate (W3, inferred)

The key saving: run the full suite once per evaluated state, with per-test outcomes and durations, and compute the reduced arms' selection and safety by simulation from that run. Actually execute the reduced arms only for the wall-time subset.

Approximate compute for 2 repos:
- 2 × 20 edits × full suite at about 3 min = 2 h
- 2 × 25 mutants × full suite = 2.5 h
- 2 × 8 perf regressions × benchmarks at about 5 min = 1.3 h
- wall-time subset: 2 × 5 edits × 3 arms × 5 repeats × about 1.5 min = 2.3 h
- flaky and A/A checks = 1 h

Total about 9 h of machine time, which can run overnight. Engineering is about 15-18 h: environment 2, mining 3, harness 6, injection 4, analysis and figures 3. This fits the 40 h window only if harness work starts within the first 6 h. **Schedule risk: medium.** The fallback is 1 repo, labelled "feasibility pilot".

### Recommended minimal scope (recommendation; scope is the PM's and owner's call)

- **Repos: 2.** One pure-Python library with a benchmark suite, and one with a compiled extension so the build claim is testable. Candidates to verify, not checked: networkx (asv benchmarks), simplejson or markupsafe (optional C speedups). Fallback: 1 repo, labelled pilot.
- **Edits: 15-20 real historical perf commits per repo** (30 or more total), mined by the frozen rule.
- **Injections per repo:** about 25 functional mutants and 5-10 synthetic perf regressions, frozen before the rule is tuned.
- **Arms:**
  - full;
  - pytest-testmon;
  - static module-import rule;
  - the student's rule;
  - optionally, the student's rule plus a periodic full checkpoint every k edits (k=5) and a final full run.
- **Repeats:** deterministic metrics need 1 run, plus a 2-run flake check. Wall time: 5 interleaved repeats on a 5-edit subset per repo. Add 1 A/A control.

### Integration order

1. W1-LIT, then W2-PRACTICE. Both are docs-only in disjoint folders with no conflicts, so merge as soon as they pass the advisor-persona review.
2. W3-EXP last. Merge only the harness, configs, frozen edit list, raw outputs, and the results page; large raw logs stay in bt-lab, recorded with hashes.
3. W4-REPO: for the meeting, recommend producing only the meeting pack (an index page linking W1-W3). Defer the repository restructure until after the meeting, because moving files the day before breaks links and evidence paths (about 2-4 h of risk for no advisor value).

### Go/no-go criteria for what is shown to the advisor

- **Show:** the W1 and W2 maps; the W3 design (definitions, frozen selection rules, threat list); and W3 numbers that have a command, raw file, and SHA. Label them "pilot, n = …".
- **Do not show:** any W3 number without the A/A noise floor and the injection-based miss counts.

### Must not be claimed

- Do not claim that reduced validation is "safe" or has "no misses" as a general property. Report only "k of N injected faults missed (95% CI …) on these repos".
- Do not claim generalisation beyond the 1-2 repos, the edit sample, or the laptop hardware.
- Do not claim wall-clock speed-ups or perf-regression detection below the measured noise floor. Do not claim to have confirmed the historical commits' speed-ups unless they were re-measured.
- Do not claim build-time savings for Python unless the build was defined and measured as non-negligible.
- Do not claim novelty for RQ4 (accumulated evidence, profile-aware selection, checkpoint schedules) until W1's recorded targeted search finds no prior work.
- Do not claim a "session" or iterative accumulation effect from parent-to-child replay of non-adjacent commits.
- Make no statement about AI-based selection, which is out of scope for Study 1.

### Open items for the PM

- **Decision:** the clone location. WSL ext4 `~/bt-lab` versus the charter's `C:\Users\pc\study\bt-lab\`. Recommendation: WSL ext4, with a note in the charter.
- **Decision:** confirm a 2-repo scope, or a 1-repo pilot fallback trigger at hour 20 if the harness is not running.
- **Ask W3:** a definition of "build" and the build-share measurement as the first deliverable (within about 4 h).
