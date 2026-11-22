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
