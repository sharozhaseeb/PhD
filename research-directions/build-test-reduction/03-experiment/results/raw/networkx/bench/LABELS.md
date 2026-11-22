# Timing labels for networkx benchmark runs

| Run | Label | Why | Usable for |
|---|---|---|---|
| `S0_181f2951.json` (started 18:35 PKT) | **concurrent (CPU-pinned)** | Bench on CPUs 2-5 while the RQ2 chain (depmaps, testmon, kill sets) ran on CPUs 6-11 from 18:52; shared cache, memory bandwidth and thermals (`../../concurrency_log.json`) | Selection counts; *provisional* per-benchmark cost weights. **Not** for regression decisions, noise floor or oracle repeatability. |

Rule (PM, 18:52): this run is re-run on an idle machine before any regression decision or the oracle-repeatability analysis uses it. The idle re-run will be stored as `S0_181f2951.idle.json`.

## `S0_181f2951.idle.json` (overnight item 4, started 2026-11-22 05:30:18 PKT) — label: **noisy** (decided before the result exists)

- **What happened:** at start, `oracle_nx.sh` logged `LOAD GATE: 1.63 > 1.5 — label noisy` (`../../overnight.log`).
- **The pre-registered rule (readiness §5, M5):** "Above 1.5 at start, the run is postponed. If the load goes above 1.5 during a run, the run is aborted, or kept and labelled **noisy**."
- **Deviation (logged):** the start gate in `scripts/oracle_nx.sh` only labels and does not postpone, so the run started anyway. Under M5 the run therefore cannot be labelled *measured*. It is kept and labelled **noisy**.
- **Cause of the 1.63:** the 1-minute average was still decaying from item 3's own benchmark processes. The 98b59df2 hazard run logged 1.63 as its after-load at the same moment (`../../bottleneck/hazard/98b59df2/g_loadavg_after.txt`). It was not another session. Load was 0.36 at 05:40 (PM). This explains the label; it does not change it.
- **Usable for:** the per-pass FULL benchmark cost in the RQ1 headline (wall time; order of magnitude), and per-case cost weights. Each case also carries its own `loadavg_before/after`.
- **Not usable for:** regression decisions, the noise floor or oracle repeatability.
- **Re-run:** only with PM approval.

## Slowdown oracle — post-hoc exploratory label (PM ruling 2026-11-22 05:50)

- **Raw files:** `../slowdowns/02.json` (#2, `_dijkstra_multisource`, max 1.90×) and `../slowdowns/08.json` (#8, `_build_paths_from_predecessors`, max 1.12×).
- **Status:** on-target FULL detections whose strength falls outside the pre-registered bands (≥ 2× strong, 1.2–1.5× moderate).
- **Label: POST-HOC EXPLORATORY.** They are reported separately and never merged into the headline. The primary pre-registered result is "regression safety not measurable on networkx with the frozen set".
- **#1** (`01.json`, 1.245×, off target, p = 0.0018) is judged an oracle false positive and is in neither set.

## Slowdown out-of-reach spot check — withdrawn as evidence (critic review 2026-11-22 06:06)

- **Files:** the `spotcheck_*` fields in `../slowdowns/0{0,5,6,7,9}.json`.
- **Problem:** 1 process × 3 values × 2 repeats gives 6 vs 6 samples. The smallest possible exact two-sided Mann-Whitney p for 6 vs 6 is 2/924 = 0.00216, above α = 0.002, so no "slower" verdict is possible.
- **Label: NO POWER.** Not usable as safety evidence. A powered re-run needs PM approval.

## PM clarification (2026-11-22 06:10): bottleneck main window

- **Main bottleneck result:** the amended pre-registered window (base `f51ed86`), truncated to states 1–8, before the uncompilable replay state `98b59df2`.
- **Sensitivity row:** the 5-edit replay (`edits/bottleneck-5edit.*`, base `22657ac`).
- **Supersedes:** the PM's 05:50 wording "5-edit window", which was imprecise.
- **Held out:** states 9–13.

## A/A run (Q2, started measuring 07:49:45) — concurrent windows (PM 07:52)

- **Prep run during the measurement**, as listed in `aa/CONCURRENCY.md`:
  - Q3 clones 07:50:18–07:50:24 (WSL, CPUs 0–1, nice 19, ionice idle);
  - Python text edits ≈ 07:49:50–07:51 (Windows);
  - WSL version check ≈ 07:51;
  - networkx static-reach count ≈ 07:51–07:52 (Windows).
  - The Q3 waiter (a 30 s `grep` loop) runs throughout.
- **Label:** the A/A cases whose runs overlap 07:49:45–07:52:30 are **concurrent**. They are identified from the per-run timestamps once A/A ends, and are reported with and without those cases.
- **After 07:52** nothing else ran (PM instruction).

## A/A run (Q2) — FAILED, no data (2026-11-22)

- **What happened:** it measured 07:49:45–09:14:54 and hit its 1.5 h cap (exit 124). **0 of 26 cases were saved**, because `benchrun interleave` wrote output only at the end.
- **PC restart:** it came after the cap (≈ 09:57–10:00). It interrupted only the #7/#9 spot-check top-up, which had launched at 09:14:56 and was still in the idle gate; nothing was measured.
- **Fix:** per-run checkpoint, `--checkpoint` (harness ≈ 10:05).
- **Re-run:** proposed to the PM as a frozen 23-case subset (`frozen/networkx.aa_noise_sample_cut23.json`); not run without approval.
- **Concurrent-window labels:** they cannot be applied, because no runs exist.

## S0 profile provenance — part 1 contaminated by a shared work tree (found 13:11 by critic; under check)

- **What:** `profile/S0_181f2951.part1.json` (the 24 `UndirectedAlgorithmBenchmarks.time_[a-l]` cases, louvain and connected_components among them) ran 19:23:27–19:46:28 PKT in `~/bt-lab/exp/work/networkx-replay`.
- **The overlap:** from 19:38 the overnight idle re-timing (item 1) checked out **the same work tree** through S0–S18 (builds), then S0–S6 (tests).
- **Evidence:** part 1's `meta.state_sha` is `2aa848c0` (S6), read at its end. Parts 2–5 ended before 19:38 and record `181f2951`.
- **Consequence:** cases profiled after ≈ 19:38 may have executed later states' code, which is **a hindsight leak into "S0" profiles.** The merged `S0_181f2951.json` inherits part 1's profiles and its S6 meta.
- **Check (running):** these 24 cases are being re-profiled in an isolated clone at S0 (`scripts/wsl/reprofile_part1.sh`, label `S0_181f2951.part1.reprofile`) and diffed against part 1.
- **Result (13:28):** the isolated re-profile at S0 (`S0_181f2951.part1.reprofile.json`, meta `181f2951`, 24/24 cases, 0 errors) is **identical** to part 1 for **all 24 cases**: the same executed-function sets.
  - **The shared-tree overlap did not change any profile content**, so the B1, #1, #3 and #9 reach claims are unaffected.
  - **Only the provenance metadata was wrong:** part 1's and the merged file's `meta.state_sha` say S6. The merged file is left as written, and the re-profile file is the clean evidence.
