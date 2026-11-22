# Night queue 2026-11-22 → 23 — pre-registered plan (frozen before any measurement)

**Request:** PM 15:20 (paper phase; `pm/advisor/paper-plan-advice.md` E2, E3, E6; `pm/tpm-paper-plan.md` §2.2). Written 15:22–15:32 PKT (real file times). Nothing in this queue has been measured when this file is frozen. Analysis code is frozen with it: `scripts/night_analyse.py`. Case lists: `frozen/night-2026-11-22.cases.json` (sha256 in `frozen/FROZEN.md`).

## Queue, caps and estimates

| # | Item | Plan | Cap | Estimate (inferred from earlier per-run times) |
|---|---|---|---|---|
| 1 | (b) σ / A/A for the 12 flagged verdicts | [`networkx/bench/aa_flagged/plan.md`](../networkx/bench/aa_flagged/plan.md) | **2 h** (PM) | 35–55 min |
| 2 | E3 tier 1: slowdown-oracle repeat on the 14 verdict-relevant cases | [`networkx/slowdowns/repeat/plan.md`](../networkx/slowdowns/repeat/plan.md) | **75 min** | 17–40 min |
| 3 | (d) 3 FULL networkx passes at S0, canaries, telemetry | [`networkx/bench/drift/plan.md`](../networkx/bench/drift/plan.md) | **2.5 h** (PM) | 35–125 min |
| 4 | (c) 2 FULL bottleneck asv passes at `f51ed86` | [`bottleneck/bench/plan.md`](../bottleneck/bench/plan.md) | **40 min** (PM) | ≈ 35 min (unknown: no bottleneck benchmark has been timed yet) |
| 5 | E3 tier 2: slowdown-oracle repeat on the other 157–171 cases per slowdown | same as 2 | **until the hard stop** (≤ 6 h) | 3.7 h at normal rates; up to 5.4 h if #1 runs at its recorded rate |

- **Caps total:** 6.4 h for items 1–4, plus item 5 up to the hard stop. Expected total ≈ 6–8 h after the gate opens.
- **Hard stop 06:25** (PM: 06:30). The queue never starts an item with < 10 min left, and each item's cap is cut to the time left.
- **Order differs from the PM message** (b, E3, d, c): E3 is split. Tier 1 (cheap, answers every verdict question) runs second. Tier 2 (the open-ended full-suite repeat) runs last, so (d) and (c) cannot be crowded out.

## Rules for every item

- **Gate, block level:** before each item, WSL load(1 min) ≤ 1.0 and Windows CPU ≤ 20 % for 3 × 60 s (postpones, no cap except the hard stop).
- **Gate, per run (new tonight):** before every run, `bth.benchrun.make_gate` waits while WSL load(1 min) > 1.5 or Windows CPU (latest telemetry sample, ≤ 60 s old) > 20 %. Polls every 20 s, waits ≤ 10 min, then runs anyway and records `pre_gate.ok = False`. A block is labelled **noisy** if any run has `pre_gate.ok = False` or peak run load > 1.5. Noisy blocks are reported, never dropped.
- **Checkpoints:** every run is appended to `<block>.partial.jsonl`. Re-running the queue resumes.
- **Watchers:** a detached stall watcher per item (`stall_watch_wsl2.sh`, 3 × the longest expected run): marker `results/raw/watch/night-<item>.marker`; the queue writes `watch/night.marker` at the end.
- **Telemetry (read-only, no setting changed):** `results/raw/telemetry/{win,wsl}-20261122.jsonl`, every 10 s. Windows: total CPU %, `% Processor Performance`, available MB; every 60 s, the top 5 processes by CPU seconds. WSL: load, MemAvailable; every 60 s, the top 5 processes.
- **Nothing else runs on the machine during the queue.** Other sessions are the PM's to pause. Known extra: **Docker Desktop's WSL distro is running** and is now the default WSL distro (found 15:20; not changed by me). All scripts name `Ubuntu-24.04` explicitly.
- **Protocol constants:** CPUs 2–5, `OMP_NUM_THREADS=1`, 3 values per process, 1 warm-up value, asv rule (ratio > 1.1 and two-sided MWU p < 0.002).
- **No root-cause hunting** for drift (TPM R-1). The telemetry is reported as covariates only.

## What each result can and cannot claim (fixed now)

- (b) closes deviation N8 **for the 12 flagged verdicts only**. The other 159 cases still have no σ.
- E3 reports **verdict agreement**, not a new detection rate. Tier-1 agreement is the primary E3 result. Tier 2 is complete only for slowdowns whose two repeats both finished.
- (d) gives a range over n passes and covariates. It does not explain the drift.
- (c) is one state, two passes: a cost row, not a detection result.
- **Amendment 1 (15:35 PKT, before any measurement):** the block gate's Windows-CPU probe (`SP.wincpu`, a powershell call) timed out at 60 s and returned 100, so the gate could never open. Queue killed in its first gate (no run had started) and restarted 15:35:12. Windows CPU now comes from the telemetry file (mean of samples in the last 30 s). Thresholds unchanged. New `scripts/night_nx.py` sha256 `fa04a9ae9bda800080fe74f2a3075151db337e8fa0602a28d5ab49ea379c619c`.
- **Amendment 2 (15:50 PKT; PM 15:46, after W1 read asv's source):** exact two-sided MWU is primary in `scripts/night_analyse.py`, and the earlier scipy 'auto' test is shown next to it. Thresholds and the 1 + 3σ rule are unchanged. No analysis had run; a smoke run at 15:51 was deleted. New sha256: `scripts/night_analyse.py` `0ef09fa9c06984b94787aa154ccf659ab44695ad0aef55c4436b046eedb535a5`, `harness/bth/stats.py` `e2bad4d8eb8db67b4f954ab0c6567ff89a63f7b4953d238fd83991094ffb204e` (new `mwu_p` methods; asv_rule's default is unchanged, so running drivers are unaffected).
