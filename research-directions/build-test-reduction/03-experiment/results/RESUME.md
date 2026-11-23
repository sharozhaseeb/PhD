# RESUME — W3 queue checkpoint (updated 2026-11-22 10:11 PKT; earlier stamps 10:20/10:30 were wrong, corrected 10:12)

**Rule from now on:** every measuring driver writes a per-run checkpoint (`bth.benchrun interleave --checkpoint <file>.partial.jsonl`; harness change ≈ 10:05, unit-tested). A kill, cap or restart then loses only the run in progress. Rerunning the same command resumes from the checkpoint.

## State of each queue item

| Item | State | Raw files | What is left |
|---|---|---|---|
| Powered spot check (profile-completeness) #0, #5, #6 | **done** 06:19–07:28 | `raw/networkx/slowdowns/spotcheck_powered/{00,05,06}.json` | — |
| Spot check #7 `katz_centrality_numpy` | **cut off** by the 07:39 cap during its first run. **Partial and invalid:** nothing was saved; the runner kept results in memory. | none | **full block** |
| Spot check #9 `DiGMState.__init__` | not started. The top-up launched 09:14:56 but was still in the idle gate when the PC restarted. Nothing measured. | none | **full block** |
| Q2 A/A noise floor (26 cases) | **failed:** it measured 07:49:45–09:14:54 and hit its 1.5 h cap (exit 124) before finishing. **0 of 26 cases saved**, because `benchrun interleave` wrote output only at the end. | `raw/networkx/bench/aa/{run.log,driver.log,CONCURRENCY.md}` only | **re-run** (proposed: 23 cases, see below) |
| Q3 B1 replication by static reach | prepared: rule frozen (`frozen/q3_project_rule.md`), 3 candidate repos cloned, script `scripts/q3_count.py`. Its waiter was killed by the restart. | — | **mine + count** (no timing; cap 1 h) |

## Resume commands (WSL; check the gate first — each driver also gates by itself)

```bash
# Spot-check top-up (#7, #9; driver skips finished slowdowns; per-run checkpoint <i>.partial.jsonl)
bash /mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/scripts/wsl/spotcheck_powered.sh   # timeout 5400; for the top-up use timeout 3300 (scripts/wsl/queue_aa_topup.sh tail)
# A/A re-run (after PM approval; 23-case sample; checkpoint aa/runs.partial.jsonl)
AA_SAMPLE=frozen/networkx.aa_noise_sample_cut23.json bash .../scripts/wsl/aa_noise.sh
# Q3 (no timing)
cd $E && PYTHONPATH=$E/harness python3 scripts/q3_count.py mine && python3 scripts/q3_count.py count
```

## Why the A/A run failed and why nobody reported it at 09:14

- **Estimate vs reality:**
  - I estimated ≈ 48 min from the spot-check rates. Scaling from the item-4 pass gives ≈ 27 min.
  - The run was still going at 85 min, a 2–3× overrun. The cause is **not known**. Candidates:
    - host load from other sessions, which the gate checks only at the start (the meeting pack was refreshed around 07:53);
    - a slow or hung worker.
  - No data survived to tell which.
- **No report at 09:14:**
  - I had armed no watcher on the A/A exit.
  - This Claude session had ended before 09:14: its background tasks were later marked "stopped before the previous session ended". So nobody was notified when the cap fired.
- **Lessons, both applied now:**
  - per-run checkpoints;
  - after each driver ends, this RESUME file is updated, and the next item's watcher is armed.

## 10:11 update

- **Running:** the #7/#9 top-up, started 10:09:30 and waiting at the gate (Windows CPU 43 % at its first check).
  - Watcher and stall guard: `scripts/stall_watch.sh`, 450 s.
  - Per-run checkpoints: `spotcheck_powered/<i>.partial.jsonl`, with `t_start`/`t_end`.
- **Next, PM-approved 10:09:** the A/A re-run, `bash scripts/wsl/aa_rerun.sh` (23 cases, cap 40 min, stall guard 200 s; plan amendment 2).
- **Then Q3:** `python3 scripts/q3_count.py mine && python3 scripts/q3_count.py count` (cap 1 h, no timing).

## 10:45 update

- **#7 done** 10:44: 10 same, minimum p 0.051, peak load 1.62, so **noisy** (raw `spotcheck_powered/07.json`).
- **#9:** started by the same top-up driver after the gate. It will likely hit the 11:04:30 cap, and its runs are checkpointed in `09.partial.jsonl`.
- **Detached chain** (WSL PID 1952, `scripts/wsl/chain_aa_after_topup.sh`): it waits for `watch/topup.marker`, kills any leftover driver, then starts the **A/A re-run** (cap 55 min) and its detached watcher v2 (`stall_watch_wsl2.sh`, stall limit 200 s, marker `watch/aa.marker`).
- **After the A/A:** resume #9 from its checkpoint (`bash scripts/wsl/topup_now.sh`; the driver skips finished slowdowns, and benchrun reuses checkpointed runs), then Q3.

## 12:31 update — queue finished

- **A/A re-run:** done, 11:05–11:53, 92/92 runs (`raw/networkx/bench/aa/`); written up and critic-checked.
- **Spot check:** complete, 5/5. #9 was resumed from its checkpoint, 12:03–12:25. Result: 1 slower in 50 (#9 louvain, p = 0.0019); written up and critic-checked.
- **Q3:** mined and counted 12:27–12:28, with the bottleneck `NAME` fix and recount at about 12:30, plus a per-edit diagnosis (`q3/`). Written up; the critic pass is running.
- **Nothing is running on the machine now.**
- **Open, needs PM approval:** an ABBA re-measurement of the #9 louvain case (about 10–15 min).

## 12:58 update
- **#9 re-check (post hoc):** capped at 12:57 after 5 of 6 runs. Every comparison came back "same", so it **fails to confirm** the original verdict; the C11 flag stands. Written up.
- **Nothing is running.**

## 17:35 update — night queue 2026-11-22 (results/raw/night-2026-11-22/PLAN.md)
- **(b)** done 15:37–16:42 and written up (results.md).
- **E3 tier 1 (rep1)** is running. It may hit its 75-min cap at 17:59 because of external host load (the owner's `paras` project; CONCURRENCY.md). Finished blocks: t1_02, t1_08. #3 and #1 are checkpointed in `raw/networkx/slowdowns/repeat/t1_{03,01}.partial.jsonl`.
- **Resume later** (after the queue ends or on another night; the gate runs first):
  `cd $E && PYTHONPATH=$E/harness timeout 4500 ~/bt-lab/exp/venvs/nx/bin/python scripts/night_nx.py rep1`
  It skips finished blocks and resumes the runs in progress.
- **Then the queue continues:** drift (d) → bn (c) → rep2, hard stop 06:25. Rerunning `scripts/wsl/night_queue.sh` resumes all items.
- **18:00:** E3 tier 1 CAPPED (exit 124) as expected. Done: t1_02 (agree 8/9), t1_08 (1/1), t1_03 (3/3). **#1: 6 of 8 runs checkpointed** in t1_01.partial.jsonl; 2 runs remain (resume command above). The queue moved on to (d) drift at 18:00:28 (gate).
- **19:50:** queue STOPPED (PM ruling A); `scripts/night_waiter.py` restarts it after 10 min idle (watch/night-gate.marker). Manual restart: `setsid nohup bash scripts/wsl/night_queue.sh &` (resumes everything).

## 02:37 — morning to-do for the E3 tier-2 write-up (PM 02:37; KB N14, provisional)
1. **Floor:** apply 1 + 3σ to the 5 new non-"same" verdicts of `t2_03`: `k_core ER(100, 0.1)` slower 1.43; `harmonic directed_wheel(10)` slower 1.21; `louvain ER(100, 0.9)` faster 0.83; `to_undirected MultiDiGraph` faster 0.87; `k_factor` faster 0.86. Use σ from `aa/sigma_noise.json` or `aa_flagged` where it exists, and say where it does not.
2. **Machine state:** split the false-verdict rate, quiet A/A 0/46 against noisy block t2_03 5/168. Test whether the flips concentrate in high-load runs, using per-run load and pre_gate from `t2_03.partial.jsonl`.
3. **Paper:** one line saying that the oracle's false-verdict rate depends on machine state.
4. **Also:** the frozen analysis (`night_show_rep.py`) for all complete t2 blocks, a critic pass, then report to the PM and W6.

## 06:30 — night queue 2026-11-22 → 23 finished (queue done 06:25:22)
| Item | Outcome | results.md section |
|---|---|---|
| (b) A/A for the 12 flagged verdicts | complete; critic-checked | "(b) σ_noise for the 12 flagged verdicts" |
| E3 tier 1 | complete (#1 finished after the restart); critic-checked | "E3 tier 1" |
| (d) drift | 3 passes complete; critic-checked | "(d) Three repeated FULL networkx passes" |
| (c) bottleneck | 2 passes complete; critic-checked | "(c) Two FULL asv benchmark passes" |
| E3 tier 2 | #3, #4, #2 complete; **#8 partial** (cut at 06:25, `t2_08.partial.jsonl`), **#1 not started** | "E3 tier 2" (critic running) |

- Telemetry stopped 06:26. The gate alarm and the waiter have exited.
- **Resume E3 tier 2** on a later night: `PYTHONPATH=$E/harness timeout <cap> ~/bt-lab/exp/venvs/nx/bin/python scripts/night_nx.py rep2`. It skips #3, #4 and #2, resumes #8 from its checkpoint, then runs #1.
- **E5 (setup-cached)** is planned for the night of 23 → 24; the `measure-cached` runner still has to be built and tested first.
- **Next design question raised by tier 2:** swap clones between sides (11/499 direction-consistent off-target flips).
