# Concurrency during the powered spot check

- **Logged event:** 2026-11-22 ≈ 06:28–06:29 PKT. This session ran the harness unit tests (`pytest tests`, 154 tests, 45 s, serial) on **Windows Python** while block 0 (`global_parameters`, started 06:19:31) was measuring in WSL on CPUs 2–5.
  - This was a lapse against "run nothing else concurrently".
  - Block 0 therefore gets the label **concurrent** for that window, whatever its WSL load samples show.
- **No other activity from this session** after that, until the driver ended.
