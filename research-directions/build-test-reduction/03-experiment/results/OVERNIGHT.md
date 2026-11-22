# Overnight serial queue (networkx + bottleneck) — PM-approved 2026-11-21 19:24 PKT

**Driver:** `scripts/overnight.sh`, run in WSL. **Log:** `results/raw/overnight.log`, with ISO timestamps for every stage start.

**Idle gate before item 1:** WSL `loadavg(1m) ≤ 1.0` **and** Windows total CPU ≤ 20 %, for 3 consecutive 60 s checks. This waits for the other sessions (W5 rendering until about 19:40) and for this session's own latent/profile jobs to finish. Items then run strictly one after another. Each item writes its own files, so a partial night still yields results.

| # | Item | What it produces | Expected duration | Output |
|---|---|---|---|---|
| 1 | Idle re-timing, networkx | Build (`pip install -e`) + serial FULL tests for S0–S18, labelled `.idle`. Both values are reported next to the first run. | ≈ 30–35 min (19 × ~90 s) | `raw/networkx/{build,oracle-tests}/S<k>_<sha8>.idle.json` |
| 1b | Idle re-timing, bottleneck builds | Clean / null / one-template / `bottleneck.h` builds on the amended base `f51ed86`, 3 repeats | ≈ 3 min | `raw/bottleneck/retime-idle/repeat{1,2,3}.json` |
| 2 | Slowdown oracle | 10 frozen slowdowns, each measured in two parts:<br>(a) **detection within reach**: interleaved A/B (2 processes × 3 values × 3 repeats) on the benchmarks whose S0 profile or static reach includes the slowed function;<br>(b) **out-of-reach spot check** (PM 19:27, against circularity): the members of a frozen seeded sample of 10 cases (`frozen/networkx.slowdown_spotcheck.json`, seed 20261121, frozen before any measurement) that are outside that reach, 1 process × 3 values × 2 repeats.<br>Verdict: asv rule. Any out-of-reach “slower” verdict means reach-based selection is unsafe for that slowdown (C11). Reported as “within reach” + “spot check”, **never** as a plain miss rate. A plan file (`<i>.plan.json`) is written before each measurement. | ≈ 2–4 h. Dominated by the 65–71 s import of `benchmark_algorithms` per process. | `raw/networkx/slowdowns/<i>.json` (one per slowdown) |
| 3 | Bottleneck `iterators.h` hazard study | The 3 natural `iterators.h` edits: incremental vs clean `.so` sha256, full tests on both, interleaved benchmarks on both (asv rule); plus the counterfactual pre-fix `depends` probe | ≈ 30–45 min | `raw/bottleneck/hazard/<commit>/`, then `results/build-hazard-iterators-h.md` (written after the run) |
| 4 | Measured FULL benchmark pass, S0 | All 171 cases with asv's default 2 processes × 3 values, CPUs 2–5, labelled `.idle`. Replaces the import-only lower bound in the RQ1 headline. | ≈ 2–3 h (lower bound 1.78 h of imports alone) | `raw/networkx/bench/S0_181f2951.idle.json` |

**Total:** ≈ 5–8 h after the gate opens.

**What morning results.md will use:**
- **1:** the idle vs first-run timing table.
- **1b:** removes the "noisy" label from the bottleneck builds.
- **2:** slowdown detection **within reach** plus the **out-of-reach spot check** per slowdown (never a plain miss rate).
- **3:** the C8 evidence.
- **4:** a measured FULL benchmark cost per edit.

**Not in this queue:** the oracle-repeatability rule (needs item 4's protocol ×3), cap-only/additive-budget comparators, and NameRTS (post-meeting).

## Outcome (2026-11-22 06:05 PKT) — all items ran; queue done 05:58

| # | Result |
|---|---|
| 1 | Done 20:04 → results.md "RQ1 — idle re-timing" (`rq1_networkx_idle.csv`). None of the 19 re-runs is M5-clean (start load 1.54–2.95; S0–S6 overlapped profiling); S16/S17 return to ≈ 71 s. |
| 1b | Done. Clean build 4.7–5.4 s, null 0.18 s (3 repeats). Load was 1.46–2.35, so the "noisy" label stays under M5. |
| 2 | Done 05:10 → results.md "Slowdown oracle". |
| 3 | Done 05:30 → `build-hazard-iterators-h.md`. |
| 4 | Done 05:58: **1668 s** (the second slowest of 6 same-protocol passes that night; range 659–2444 s, see results.md), 171/171 cases, labelled noisy (M5). This **corrects** the "≥ 1.78 h" estimate above. The 65–71 s import figure was measured under load; the measured per-import cost is about 13 s. The "Expected duration" column above therefore over-estimated items 2 and 4. |
