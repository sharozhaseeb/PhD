# FormulaCode

Status: critic-checked 2026-11-21 (10 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/formula-code/fc-eval @ c08f665e7bf3b4de225b72dc02ce9b15b7aaba2b (main, 2026-05-13; local clone `C:\Users\pc\study\bt-lab\survey\formula-code_fc-eval`, HEAD verified); https://github.com/formula-code/datasmith @ b4874d3b908c9eeab83ae66126df9a18348bb133 (main, 2026-11-04; local clone `C:\Users\pc\study\bt-lab\survey\formula-code_datasmith`, HEAD verified) · Paper: https://arxiv.org/abs/2603.16011 (critic re-read the full PDF text, incl. Appendices A, B)
Evidence labels: **[src]**, **[inf]**, **[unk]**. Paper locations are by section/appendix (the PDF text has no stable page numbers). Repo paths are relative to `adapters/formulacode/template/` in fc-eval unless stated; line numbers are file lines at the commits above.

## 1. What it is
Repo-level optimization benchmark: 957 perf bottlenecks from 70 scientific Python repos, each with an expert patch and community ASV workloads (avg 264.58/task); full agent runs on FormulaCode-V (108 tasks). [src] paper abstract, §3, Table 1, App. A.9.
The agent edits freely inside one container; the harness measures once, after the agent stops. [src] `run-tests.sh` 60-156 (post-run script).

## 2. Build / environment
- One Docker image per task, built from the repo at the PR's base state. A reflexive LLM agent refines a build shell script; for each task it first tries 10 earlier successful scripts from the same repo (nearest by commit date), then falls back to LLM synthesis. Validation = ASV profile check + pytest check. 1232 of 3181 PRs got a build for $446 total. [src] paper §3.1 Stage 3, App. A.5.
- Compiled extensions built from source; ASV, pytest and the snapshot tool installed. [src] App. A.5.
- Images published to DockerHub; adapter can pre-pull (`--pull-dockerhub`). [src] fc-eval README; datasmith README (pipeline lists "synthesize Docker images", "publish").
- Per-agent-edit rebuild: not done by the harness. `run-tests.sh` never rebuilds the package (it only checks out the ASV config and benchmark dir via `reset_repo_state`, lines 21-54, 93), and ASV runs with `environment_type: existing` / `--python=same` (profile.sh 95-98, 115). So a compiled-extension edit is measured only if the agent rebuilt it itself. [src] `run-tests.sh`, `profile.sh`. Any incremental-build advice to the agent: none found in `common_prompt.txt` (checked all 69 lines). [src]/[unk]

## 3. Correctness tests per candidate
- Paper: a modification is valid only if it passes all tests the baseline passes; two kinds: unit tests (manually validated only for FormulaCode-V) and automated snapshot tests "comparing each workload's return values to a reference" (§3.1 Stage 4); App. B.7 says snapshot tests check each workload's "local variables". [src] paper §2, §3.1, App. B.7.
- Harness correctness check is a ONE-SHOT post-run step on the agent's final tree, not a per-edit gate: (1) `snapshot-tool verify` on the ASV benchmark dir (`run-tests.sh` 111-121); (2) if `run_pytest` (default True, `adapter.py` 56): `formulacode_testrunner.py --base <base_commit>` (line 146). [src]
- Which pytest tests: NOT the full suite. `pytest_runner.py` takes `git diff --name-only <base>...HEAD` plus unstaged changes, maps each changed `.py` file to test files by name (`tests/<pkg>/test_<mod>.py`, sibling `test_<mod>.py`, etc.), and runs only those; with no `--all` or `--fallback` in the call, zero matched tests gives exit code 5 and "No tests matched". [src] `pytest_runner.py` 39-87, 107-184, 363-427, 485-540; `run-tests.sh` 146. This contradicts the researcher's guess that the full suite is run [inf -> WRONG]. Whether the paper's headline "passes all tests Code0 passes" is implemented by this changed-file heuristic or by something outside these repos is [unk]; staged-only changes are excluded by default (`include_staged=False`, line 42).
- Paper's own rule: if correctness fails, any performance gain is rolled back and the original codebase is reported (Table 16: roughly 47-56 of 108 final patches per agent/model rejected; most from pytest, fewer from snapshot). Also stated per workload: failing workload => speedup = 1. [src] paper §2.1; App. B.7 "Correctness Constraint Violations", Table 16. In the parser, `calculate_agent_advantage` has no correctness gate; snapshot results are printed separately (`parser.py` 985-1176 vs 1420-1446). Where the roll-back is applied is [unk] in these repos.
- Test selection by changed code is therefore a static filename heuristic, post hoc, once per task; the agent itself may run any tests during its session (prompt only says "Maintain functional correctness"). [src] `common_prompt.txt` 45, 55.

## 4. Performance measurement per candidate
- ASV workloads written by upstream maintainers; the prompt tells agents to run relevant ones with `asv run --python=same --bench=<regex>` and says full-suite runs are "discouraged". [src] `common_prompt.txt` 14-26.
- Final measurement (fc-eval): `asv machine --num_cpu 1 --ram 4GB`, then `asv run -a rounds=4 -a repeat=0 --python=same --append-samples` over all workloads. [src] `profile.sh` 110-121. (Datasmith's dataset-time `profile.sh` uses `rounds=1`, line 115, and a newer `measure.sh` with an "LSV" tool, lines 32-98, not analysed. [src])
- Paper's protocol: ASV warm-up + 2-40 adaptive samples per workload (defaults kept). [src] App. A.6.
- The Mann-Whitney U test (p < 0.002; 99% CI-overlap fallback for small samples) and the Holm-Bonferroni check are used in DATASET CONSTRUCTION, to keep tasks whose EXPERT patch gives a significant speed-up (35 of 957 tasks removed; none in -V). [src] App. A.6. The researcher placed it under per-candidate measurement; the paper does not say it is applied to agent patches. In the harness the agent advantage uses per-benchmark MEDIANS of ASV samples: speedup = nop_median / agent_median; the `use_stats` and `factor` arguments are explicitly "Unused". ASV's `is_different` is used only in the change-classification marks. [src] `parser.py` 985-1032, 1059-1076, 704-727. Holm-Bonferroni: the paper says "Our codebase incorporates" it, but a grep of datasmith found no occurrence. [unk]
- Metric: per-workload speedup = base / agent; overall = geometric mean; advantage = agent speedup minus expert speedup, stratified by module/class/function and also a variance-normalised version. [src] paper §2.1; `parser.py` 1004-1005, 1141-1176.
- Noise control: all runs on one AWS EC2 c5ad.large (2 vCPU, 4 GiB) for isolation; baseline (nop), expert (oracle) and each agent measured sequentially on the same instance in fresh containers. ASV's own safeguards (CPU affinity, warm-ups, repeated trials) are cited as the variance control; no extra pinning or instruction counting was added. [src] paper App. B.1, B.5, Table 12. Recommended EC2 in fc-eval README. [src]

## 5. Cost per candidate
- Environment synthesis: $446 total (1232 envs); per-task build cost not given. [src] App. A.5.
- Agent runs: no token/step budget, 6 h wall-clock cap never reached, average 38 min per task; the paper also reports token/API cost per agent in §4.5. [src] paper Table 12 and its note. (The sample `task.yaml` in the adapter template sets `max_agent_timeout_sec: 3000`, lines 52-54, which differs from the paper's 6 h; sample file only.) Per-candidate (per-edit) cost: [unk].

## 6. Iteration / cumulative re-validation
- The agent iterates on one working tree; scoring is on the final repo state vs baseline. [src] paper §2, `run-tests.sh` 60-66 (diff of the whole tree vs base is taken as the solution).
- There is no per-edit or per-iteration harness validation; correctness is checked once on the final tree. In effect this is a single cumulative-final check, and it is a changed-file test subset plus snapshot verification (see §3). [src]/[inf]

## 7. Limitations stated
- Dependence on ASV workloads (quality bounded by maintainers); evaluation on a 108-task subset for compute; hardware specificity (one AWS config); single scientific-Python domain. [src] paper App. A.9 ("Dependence on ASV workloads", "Evaluation on a subset", "Hardware specificity").

## 8. Relevance to Study 1
- [src] Closest public analogue to "repo-level, many workloads, correctness via baseline tests + snapshot outputs"; shares the ASV substrate with the asv note.
- [src] Env build is per-task and cached; the harness has no reduced or incremental rebuild per edit; compiled edits depend on the agent rebuilding. Gap Study 1 targets. [inf]
- [src] The final correctness check already uses a changed-file -> test-file mapping (name heuristic, no coverage); a useful weak baseline for per-edit test selection, with a known failure mode (no mapped tests -> zero tests run).
- [inf] Snapshot return-value tests are a cheap deterministic per-workload correctness signal worth comparing to test-suite selection.

## Sources
- arXiv 2603.16011 full PDF text: §2, §2.1, §3.1, §4.5, App. A.5, A.6, A.7, A.9, B.1, B.5, B.7 (Table 12, Table 16).
- fc-eval @ c08f665: `adapters/formulacode/template/run-tests.sh`, `profile.sh`, `pytest_runner.py`, `parser.py`, `common_prompt.txt`, `task.yaml`, `adapter.py`; README.
- datasmith @ b4874d3: grep for stats/Holm; `docker/templates/profile.sh`, `measure.sh` (headers only). Not read: datasmith synthesizer, `asv_discover_and_cover.py`, `snapshot-tester` (external repo).
