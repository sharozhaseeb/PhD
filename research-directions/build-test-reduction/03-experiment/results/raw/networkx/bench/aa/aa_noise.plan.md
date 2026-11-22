# Benchmark A/A noise floor and oracle repeatability — plan (frozen 2026-11-22 06:40 PKT, before measuring; PM 06:27 Q2)

**Purpose:** the slowdown verdicts (asv rule: ratio > 1.1 and MWU p < 0.002) need to know:
- how often the rule says "slower" or "faster" when **nothing changed** (A/A);
- how noisy each case is (CV);
- whether a verdict repeats (oracle repeatability).

**States:** S0 (`181f2951`) in two independent clones, `nx-slow-A` and `nx-slow-B`, both checked out at S0 with no patch. The comparison is A vs B.

**Cases:** the frozen stratified sample `frozen/networkx.aa_noise_sample.json`: 40 cases, seed 20261122, sha256 in `frozen/FROZEN.md`. It holds 10 `benchmark_algorithms` cases and 30 from the other 6 modules. A subset is used because of the 1.5 h cap.

**Protocol:** the same as the powered spot check, so the asv rule can reach significance.
- `bth.benchrun interleave`, 5 processes × 3 values + 1 warmup, CPUs 2–5, `OMP_NUM_THREADS=1`.
- **2 repeats** (interleaved A, B, A, B), so each case has 15 vs 15 samples per repeat. The smallest attainable p is 3.4e-6.

**Analysis (fixed now):**
1. **A/A false-verdict rate:** per repeat, apply the asv rule to A vs B for each of the 40 cases. Report the false "slower" count k/40 and the false "faster" count, each with a Wilson CI, per repeat and pooled (k/80). Also apply the rule with the two repeats' samples pooled (30 vs 30).
2. **Per-case noise:** the coefficient of variation (sd/mean) of the 30 samples per state per case, median and range, split into `benchmark_algorithms` and others. Also the A/B median ratio spread (min, max, and the fraction of cases with ratio > 1.1).
3. **Repeatability:** the cases whose verdict is not "same" in repeat 1 or repeat 2, and whether the verdict recurs in the other repeat (agreement k/40).
4. **Use:** the A/A false-"slower" rate is the noise floor against which the slowdown oracle's 3 off-target non-"same" verdicts out of ≈ 890 comparisons are read. It replaces the "in line with chance" reading.

**Idle gate:** postpone, do not label. Start only when WSL `loadavg(1m) ≤ 1.0` **and** Windows CPU ≤ 20 % for 3 consecutive 60 s checks. Load is logged before and after each repeat, and per run. A run with peak load > 1.5 is labelled noisy (M5). Nothing else runs concurrently.

**Cap:** `timeout 5400` (1.5 h, gate waits included). If it overruns, completed repeats are kept and reported as partial.

**Not done:** oracle repeatability of the two on-target slowdown verdicts (#2, #8). That needs the slowdown clones and would exceed the cap. It is listed as remaining work.

**Outputs:** `aa/repeat{1,2}.json` (raw runs), `aa/aa_result.json`, `aa/driver.log`. Driver: `scripts/aa_noise_nx.py` via `scripts/wsl/aa_noise.sh`.

## AMENDMENT 1 — 2026-11-22 07:47 PKT, before any measurement (PM 07:43)

**Status of the first launch:** it started at 07:40:52, but was still waiting at the idle gate (1/3) when it was stopped at 07:43:54. **Nothing was measured**, and `driver.log` shows only gate lines.

**Changes:**
1. **Order arm.** `bth.benchrun.run_interleaved` rotates the state order per repeat:
   - repeat 0 runs **A then B** for every case. That is the oracle's fixed base-first order.
   - repeat 1 runs **B then A**.

   So the 2 repeats already give a fixed-order arm (repeat 0 alone, exactly as in the spot check) and an alternated ABBA arm (both repeats, pooled). No code change is needed. Analysis added:
   - **Order effect:** per case, ratio(B/A) in repeat 0 vs in repeat 1. If running first is slower, repeat 0 gives B/A < 1 and repeat 1 gives B/A > 1. Report the median "first / second" ratio and its sign test across cases.
   - **Verdicts per arm:** the false-verdict count under the fixed order (repeat 0, 15 vs 15) and under ABBA (pooled, 30 vs 30).
   - **First case of the run:** whether the first case shows a larger effect than the rest (cold start).
2. **Spread of "same" verdicts:** the empirical ratio distribution (min, 5th–95th percentile, max) of all A/A verdicts labelled "same", per arm.
3. **Power from measured noise:** for each case and each shift s ∈ {1.12, 1.2, 1.5, 2.0}:
   - draw 15 of that case's A samples and 15 of its B samples, both with replacement, and multiply the B draw by s;
   - apply the asv rule; repeat 200 times with seed 20261122.
   - Report the fraction "slower" (median over cases, plus the `benchmark_algorithms` vs other split). This replaces the assumed 5 % noise.
4. **Cases cut to 26** to fit the 1.5 h cap (arms kept): `frozen/networkx.aa_noise_sample_cut26.json`, sha256 in `frozen/FROZEN.md`. These are the first 6 `benchmark_algorithms` draws and the first 20 other draws of the same seeded draws.

Everything else is unchanged: protocol 5 × 3, 2 repeats, CPUs 2–5, the postponing gate, `timeout 5400`.

## AMENDMENT 2 — 2026-11-22 10:10 PKT (file time; first written with a wrong "10:25" stamp, corrected 10:12), before the re-run (PM approval 10:09)

**Reason:** the amendment-1 run (26 cases) measured 07:49:45–09:14:54 and hit its 1.5 h cap. **0 cases were saved**: the runner wrote output only at the end. That is 2–3× over the 27–48 min estimate, for an unknown cause.

**Changes (the rest of amendment 1 stands — order arm, spread, power from measured noise):**
1. **Sample:** `frozen/networkx.aa_noise_sample_cut23.json`, frozen 10:08, sha256 in `frozen/FROZEN.md`. It holds the first 3 `benchmark_algorithms` draws and the first 20 other draws of the same seeded draws, and **replaces the 26-case sample.**
2. **Cap:** 40 min (`timeout 2400`).
3. **Checkpoint:** every run is appended at once to `aa/runs.partial.jsonl`, with `t_start`, `t_end`, `wall_s` and load before and after.
4. **Stall guard:** if no run finishes within **3 × its expected time**, the run is aborted and reported, not left to the cap.
   - Expected time per run comes from the item-4 pass: `wall_s` for 2 processes × 2.5 for 5 processes.
   - In practice the guard fires when nothing is appended to the checkpoint for **200 s** while a measurement is in progress. That is 3 × the slowest expected run in the sample: 2.5 × 27 s ≈ 67 s, from the item-4 pass. Gate-waiting phases are excluded. (The spot-check top-up uses 450 s = 3 × 149 s.)
5. **Timing comparison (PM):** the write-up compares each case's measured run time with this expectation. A repeat overrun is reported as a finding.
- **2026-11-22 10:43 PKT (PM ruling 10:43), before the re-run starts:** cap raised from 40 min to **55 min** (`timeout 3300`). Reason: the slowdown seen this morning has come back, 1.2–2× per run (block #7 of the spot-check top-up), so 13–25 min becomes ≈ 26–50 min.
- **2026-11-22 10:45 PKT (PM check), before the re-run starts:** the stall limit changes from 200 s to **420 s**. Basis:
  - The longest expected A/A run in the 23-case sample is 2.5 × 27 s ≈ 67 s, from the item-4 pass.
  - Today's runs take up to 2.0× (median 1.6×) the item-4-based expectation: block #7 maxes at 239 s against 149 s expected.
  - So the longest run expected today is ≈ 134 s, and 3 × 134 s ≈ 402 s, rounded up to 420 s.
