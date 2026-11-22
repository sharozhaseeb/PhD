# Concurrency during the A/A run
- 2026-11-22T07:50:18+05:00 Q3 clones start (git clone --filter=blob:none --no-checkout; nice 19, ionice idle, taskset CPUs 0-1; benchmarks on 2-5)
- 2026-11-22T07:50:24+05:00 Q3 clones end
- ≈ 07:49:50–07:51 (Windows): small Python text edits to `results.md` and the hazard file (string replacements, each < 1 s).
- ≈ 07:51 (WSL): `python3 -c 'import tomllib'` version check (< 1 s).
- ≈ 07:51 (WSL): started the Q3 waiter `scripts/wsl/q3_after_topup.sh`. It runs `grep` every 30 s until the top-up ends; this is negligible, but it is running for the whole A/A run.
- ≈ 07:51–07:52 (Windows): networkx static-reach count (`q3_count.count_networkx_static`, reads a 5 MB JSON, a few seconds).
- **From 07:52 (PM instruction): nothing else runs on the machine until A/A ends.** Only text edits.
- **Re-run 11:05:06–11:53:35 (amendment 2):** no other job from this session ran on the machine. In-session watchers polled the size of `runs.partial.jsonl` every 20 s from Git Bash (`wc -l`), and the detached WSL watcher ran `stat` and `tail` every 15 s; both are negligible. The critic subagent ran *after* 11:53:35.
- **Note:** the "(amendment 1)" launch line at 07:45:13 predates amendment 1's 07:47 stamp. Measurement began only at 07:49:45, after the amendment.
