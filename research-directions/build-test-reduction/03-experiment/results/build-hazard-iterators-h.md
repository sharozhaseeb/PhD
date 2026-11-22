# Bottleneck `iterators.h` build hazard — overnight item 3 (C8 evidence)

**Status:** measured 2026-11-22 05:10–05:30 PKT. Written up 06:00 without any re-run. PRELIMINARY.
**Question:** when a replayed optimization edits the shared header `bottleneck/src/iterators.h`, does an **incremental** `build_ext --inplace` give a different artefact or behaviour from a **clean** build?
- The historical bug: `setup.py` did not list `iterators.h` in `depends=`, so the extensions that include it were not rebuilt. It was fixed upstream in `52f6cd1` (2019-09-20), before our amended base `f51ed86`.
- So two checks were run:
  - **NATURAL:** the 3 replayed `iterators.h` edits, built with the base's fixed `setup.py`.
  - **Counterfactual PROBE:** the same edits built with `iterators.h` removed from `depends=`, i.e. the pre-fix `setup.py`.

**Driver:** `scripts/wsl/bn_hazard.sh` (via `bn_all_after1850.sh`; log `raw/bottleneck/hazard/{driver.log,<commit>.log}`). CPython 3.8.20 + numpy 1.19.5 (M4).

**Per commit, steps (a)–(g):**
- (a) Clean build of the parent state in directory `inc/`. `inc/` is then copied to `stale/`.
- (b)–(c) Check out the commit state in `inc/` and build incrementally (**INC**).
- (d) Copy `inc/` to `clean/`, run `git clean -fdx`, and build (**CLEAN**).
- PROBE: the pre-fix `setup.py` in `stale/`, then an incremental build (**STALE**).
- (e) Compare `.so` sha256, raw and `strip --strip-debug`.
- (f) Full test suite on all three.
- (g) Interleaved benchmarks, 3 repeats, CPUs 2–5, on the cases that exercise the edited code. Verdicts use the asv rule against CLEAN.

**Raw files:** `raw/bottleneck/hazard/<commit>/`.

| Commit (step) | Diff | Builds (exit code) | Rebuilt by INC / by STALE | Tests (191) INC · CLEAN · STALE | Benchmarks vs CLEAN | Load at (g), before → after |
|---|---|---|---|---|---|---|
| `c5720c8d` (2/13) "speed up median for integers" | `iterators.h` +2/−1, `reduce_template.c` +11/−2 | 0 / 0 / 0 | 4 of 4 / **only `reduce.so`** | 191 pass · 191 pass · 191 pass | INC **64/64 same**; STALE **64/64 same** (ratio range 0.946–1.087) | 1.10 → 1.38 (within M5) |
| `a638b282` (3/13) "Introduce REDUCE_CONTIGUOUS … macros" | `iterators.h` +9 only | 0 / 0 / 0 | 4 of 4 / **none** | 191 · 191 · 191 pass | INC 63 same + **1 "faster"** (`time_nanmin('int64',(1000,1000),'F',0)`, 0.878, p = 0.0012); STALE 64/64 same (same case 0.892, p = 0.10) | 1.08 → **1.65 (noisy, M5)** |
| `98b59df2` (9/13) "optimize for contiguous 2D nanmin/nanmax" | `iterators.h` +2, `reduce_template.c` +146/−20 | **1 / 1 / 1 — does not compile** | none / none | **191 pass · 8 collection errors · 191 pass** | **no verdict:** all 192 CLEAN entries (64 cases × 3) are import errors; INC and STALE ran the parent's binaries | 2.14 → 1.63 (noisy, M5) |

## 1. The `.so` hash comparison is uninformative across directories: these builds are not path-reproducible

- **Every** `.so` differs between INC and CLEAN, raw and stripped, for all 3 commits (`e_compare.txt`). But **parent vs CLEAN differs too**, for every file, including the 3 extensions whose code the commit cannot have changed. So "INC ≠ CLEAN" says nothing about staleness here.
- **Cause, checked:** the build directory's absolute path is embedded in the binary. `strings` finds the `inc/` path 3 times in the INC `reduce.so` and the `clean/` path 3 times in the CLEAN one, for `a638b282` (06:00 check, read-only). `--strip-debug` does not remove it.
- **Within one directory the builds are byte-identical.** In `a638b282`, INC recompiled all 4 extensions and produced **byte-identical** files to the parent build: the 9 added macro lines change no machine code. In `c5720c8d`, INC's `move.so`, `nonreduce.so` and `nonreduce_axis.so` are byte-identical to the parent's; only `reduce.so` changed.
- **Consequence for rule B4 (A4, rules.md §2).** A4 compares the stripped `.so` SHA-256 of a clean build against the incremental build at every full check, and falls back to clean builds on any mismatch. **On this toolchain, done in separate directories, B4 always reports a mismatch.** A4 would switch to clean builds at its first full check, and that clean-build cost is charged to OURS.
  - On these edits the charge is small: INC already recompiles all 4 extensions after a header edit, 5.2–6.0 s vs CLEAN 5.3–5.9 s (single runs, noisy).
  - **Fix proposed, not applied (post-meeting, PM 05:50):** build clean and incremental at the same path, or compile with `-ffile-prefix-map`, then re-validate B4. Until then B4 cannot tell a stale artefact from a path difference; rules.md §2 marks it invalid.

## 2. NATURAL edits: the hazard did not reproduce

With the base's fixed `setup.py`, INC rebuilt all 4 extensions after each compilable `iterators.h` edit (`c_rebuilt.txt`). Tests were identical everywhere: 191/191 pass in INC, CLEAN and STALE for `c5720c8d` and `a638b282`, with 0 outcome differences (`f_test_diff.txt`).

**Benchmarks.**
- `c5720c8d`: 64/64 cases "same" for both INC and STALE.
- `a638b282`: one INC case is "faster" (`nanmin` int64 F-order, 0.878, p = 0.0012). **We treat it as a noise-level outlier, not a build effect:**
  - INC's and STALE's `reduce.so` are **byte-identical**: both equal the parent build, which STALE simply kept. Yet STALE measured the same case at 0.892 with p = 0.10, "same". So the INC verdict cannot come from a stale-vs-fresh build difference.
  - What both show is a ~11–12 % gap between CLEAN and the two identical binaries on this one case. CLEAN's binary differs only by its embedded path. This is either noise or a code-layout effect of that path; we did not test which.
  - With 128 verdicts at α = 0.002, about 0.26 false positives are expected by chance; one is not surprising. p = 0.0012 is near the threshold, and the load rose to 1.65 during the run (M5: noisy).

**Verdict on the natural edits: "no hazard reproduced"** — not even a stale artefact, because the fixed `setup.py` rebuilds everything.

## 3. Counterfactual PROBE (pre-fix `setup.py`): the stale artefact appears, with no observed behavioural effect

- **`c5720c8d`:** STALE rebuilt **only `reduce.so`**, the one whose `.c` changed. `move.so`, `nonreduce.so` and `nonreduce_axis.so` were left from the parent: **the 2019 hazard mechanism reproduces.** But those 3 stale files are **byte-identical** to what the correct INC rebuild produced in the same tree, so the stale artefacts equal the correct ones. Tests 191/191 same; benchmarks 64/64 same.
- **`a638b282`:** STALE rebuilt **nothing**, so all 4 extensions are stale. Again they are byte-identical to the correct INC rebuild (the macros added are not yet used). Tests and benchmarks are the same.
- **Label: PROBE, "stale artefact, no observed behavioural effect".** For these two edits, the header change does not alter the code of the extensions it fails to rebuild, so the stale build was harmless by construction. This is luck of the edit, not safety of the build. A header edit that changed an inlined iterator would have been missed with the pre-fix `setup.py`. No such edit exists in the window.

## 4. `98b59df2` (step 9 of 13): the replayed state does not compile, and an incremental tree hides it

- **What fails:** at the replayed commit state, every build fails with exit code 1 within 0.3 s: `reduce_template.c:567: error: 'DTYPE1' undeclared` (in `nanmin_one_*` / `nanmax_one_*`; `c_build_incremental.log`, `d_build_clean.log`).
- **This is a replay-validity problem, not a header hazard.** The upstream commit has the same 2-file diff (`git show --stat 98b59df2`). It most likely relies on a template-generator change from a commit outside the replayed edit list. That is **not diagnosed further** (no extra runs).
- **Why the benchmark data are not a pass:** CLEAN has no `.so`, so its tests hit 8 collection errors and all 192 CLEAN benchmark entries are `ImportError` ("bottleneck modules failed to import"). The verdict script then stopped on an empty sample (`98b59df2.log`). So there is **no benchmark verdict** for this commit, and the 192 entries are not counted as "same".
- **H1, a harness/replay lesson, not a finding about reduced builds (advisor review 07:50): an incremental tree masks a failed compile, and RTS then passes** (observed on a replayed, non-compiling state). Rule B0 is kept; any harness rejects failed builds.
  - **Observed:** after the failed compile, the INC tree (and the STALE tree) still held the parent's `.so` files, byte-identical to the parent (`c_incremental_so.txt` = `a_parent_so.txt`). The full suite then **passed 191/191** (`f_test_inc.log`). The clean tree, with no `.so`, failed with 8 collection errors (`f_test_clean.log`).
  - **So an incremental in-place workflow accepts an edit that does not compile.** This holds whenever the build's exit code is not checked, whether the tests are run in full or selected by RTS (testmon, PerfAgent-style). The tests exercise binaries from *before* the edit. Only a clean build, or checking the exit code, reveals it.
  - **Scope (wording corrected after critic review):** this is a replayed edit, not an injected fault, but the non-compiling state is a **replay artefact**. A prerequisite commit is missing, so this state never existed upstream. It is 1 of the 3 `iterators.h` commits and 1 of 13 replayed bottleneck edits. The RTS part is inferred from the full suite passing on stale binaries; testmon was not run on bottleneck.
- **Rule adopted (PM 05:50, rules.md §2 "B0"):** a failed build is a reject, whatever the tests say, in every arm. It costs nothing, since the exit code is already recorded (`bth.orchestrate._run` → `exit_code`).
- **Consequence for the bottleneck replay (PM ruling 05:50):** states 9–13 inherit the uncompilable `reduce_template.c` unless a later edit repairs it, which is not checked. They are **held out of all benchmark runs and of the headline.**
  - **The main bottleneck result is the amended pre-registered window (base `f51ed86`) truncated to states 1–8**, before the uncompilable state (PM clarification 06:10, superseding the 05:50 "5-edit window" wording). The 5-edit replay (`edits/bottleneck-5edit.*`) stays a sensitivity row. Limitation: the bottleneck evidence covers 8 edits.

## 5. Summary for C8

| Check | Result |
|---|---|
| NATURAL `iterators.h` edits (2 compilable) | **Hazard did not reproduce.** The fixed `setup.py` rebuilds all 4 extensions; tests and benchmarks are the same, apart from one noise-level outlier on byte-identical code. |
| PROBE (pre-fix `depends=`) | Stale artefacts reproduce (3 of 4 extensions, then 4 of 4), but they are byte-identical to the correct rebuild: **stale artefact, no observed behavioural effect**. |
| `.so` hash differential (B4) | **Uninformative across directories:** the build path is embedded. **B4 as specified is invalid** (noted in rules.md §2). It always fires, so A4 pays clean builds from its first full check. Fix (same path or `-ffile-prefix-map`) is a post-meeting item. |
| Uncompilable replayed state (`98b59df2`) | **Measured false pass:** after a failed compile, the incremental tree keeps the old binaries and passes 191/191 tests. Rule B0 (failed build = reject) was adopted. States 9–13 are held out; the main bottleneck result is the amended window (base `f51ed86`) truncated to states 1–8 (PM 06:10); the 5-edit replay is a sensitivity row. |

**Not done (no re-runs, per PM):** confirming that the `nanmin` outlier is noise (oracle repeatability), building at a fixed path to re-test B4, and diagnosing the missing prerequisite for `98b59df2`.
