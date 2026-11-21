# Harness spec (W3) — contracts for implementers

The design and rationale are in `../readiness.md` (v1.1). This file fixes the code contracts: package `bth` lives in `03-experiment/harness/bth/` and tests live in `03-experiment/tests/`. Python 3.12, standard library first; allowed dependencies are numpy, scipy, pytest. **No AI and no randomness without a fixed seed. Every function is deterministic.**

Unit tests must run on Windows with `python -m pytest research-directions/build-test-reduction/03-experiment/tests -q` (from the repo root). Tests that need gcc, git or WSL are marked `@pytest.mark.wsl` and skipped when the tool is missing.

## Identifiers

- **FuncID** (str):
  - Python function: `"<posix relpath from repo root>::<qualname>"`, e.g. `"networkx/algorithms/shortest_paths/generic.py::_build_paths_from_predecessors"`. Nested functions use the `co_qualname` style (`outer.<locals>.inner`).
  - Module level of a file: `"<relpath>::<module>"`.
  - Native callable: `"native::<module>.<name>"`, e.g. `"native::bottleneck.reduce.nansum"`.
- **TestID**: the pytest nodeid. **BenchID**: `"<bench module>.<Class>.<method>"` or `"<bench module>.<function>"`, plus `"(<param repr>, ...)"` when parametrised.

## Modules and owners (disjoint files — do not edit files you do not own)

### Implementer 1 — `mine.py`, `replay.py`, `changed_fns.py`

**`mine.py`**
- `mine(repo, *, regex, src_globs, exclude_globs, max_lines, before, after=None, limit=None, first_parent=True) -> list[dict]`, with keys `sha, date, subject, files, src_lines, ai_authored, qualifies, reason`.
- Uses `git log` and `git diff --numstat` through `subprocess`, with no shell.
- `ai_authored` is true when the subject or body contains `[CLAUDE]`, `[CODEX]` or a `Co-authored-by:` trailer naming an AI tool.
- Output is chronological (oldest first) and identical across runs.
- CLI: `python -m bth.mine --config configs/networkx.toml --out edits/networkx.candidates.json`.

**`replay.py`**
- `build_states(repo, workdir, base_sha, edits, src_pathspec, check: Callable[[Path], tuple[bool,str]] | None) -> list[dict]`.
- Creates a fresh **separate clone** at `workdir` (never touches `repo`'s working tree, never force-pushes, never resets `repo`), then checks out `base_sha` on branch `bth-replay`.
- For each edit, computes `git diff sha^ sha -- <src_pathspec>` and applies it with `git apply --3way --index`. On conflict it runs `git checkout -- . ; git reset -q` **inside workdir only**, logs `dropped: conflict`, and continues.
- On success it calls `check(workdir)`. If `check` returns `(False, msg)`, it reverts that step (`git reset --hard HEAD`, inside workdir) and logs `dropped: check failed: msg`. Otherwise it commits with message `bth step i: <orig sha>`.
- Returns per-edit records `orig_sha, status, state_sha, reason`. State SHAs are stable across runs: commit with fixed author/committer name, email and date taken from env vars (`GIT_AUTHOR_DATE` = the original commit date).

**`changed_fns.py`**
- `changed_functions(workdir, rev_a, rev_b, cfg) -> ChangeSet`. `ChangeSet` is a frozen dataclass with fields:
  - `functions: frozenset[FuncID]`
  - `files: frozenset[str]`
  - `module_level_files: frozenset[str]`
  - `native_files: frozenset[str]`
  - `header_edits: frozenset[str]`
  - `build_config_changed: bool`
  - `unmapped_native: frozenset[str]`
- **Python rule.** Parse the old and new file with `ast`. Collect every `FunctionDef`/`AsyncFunctionDef` (with class/nesting qualname) and its line span, including decorators. A function is changed if any removed line (old-side span) or added line (new-side span) falls inside its span; deleted and added functions count too.
  - Hunk lines outside every function (imports, module constants, class bodies outside methods): add `<relpath>::<module>` to functions and the file to `module_level_files`.
  - Blank and comment-only lines are ignored.
  - Expansion to "all functions of the module" is done by the selector, not here.
- **C rule** (files matched by `cfg.native_sources`, a mapping glob → extension module name, e.g. `"bottleneck/src/reduce_template.c" → "bottleneck.reduce"`):
  - Find top-level function definitions by brace scan.
    - A definition header is a line at column 0 that is either a macro-style header `^[A-Z_][A-Z0-9_]*\(\s*(\w+)\s*,` followed by `{` on the same or next line (Python name = the first macro argument, e.g. `REDUCE_ALL(nansum, DTYPE0) {` → `nansum`),
    - or a plain C header `^[\w\s\*]+?\b(\w+)\s*\([^;]*\)\s*\{?$`, mapped to a Python name with `cfg.native_name_regex` (first group); if that does not match, record the name in `unmapped_native`.
  - The span runs from the header to the matching closing brace. Changed lines inside a span → `native::<ext>.<pyname>`.
  - Changed lines outside any span: if they are within 3 lines before a header and are macro-only or blank (e.g. `BN_OPT_3`), attach them to that function. Otherwise the file counts as a header-like edit → add to `header_edits`.
  - Files matched by `cfg.native_headers` (e.g. `*.h`, `bn_template.py`) → `header_edits`.
  - Files matched by `cfg.build_config` (e.g. `setup.py`, `pyproject.toml`, `meson.build`) → `build_config_changed = True`.
- Fixtures: `tests/fixtures/bn_0819d3a.diff`, `bn_reduce_template_before.c`, `bn_reduce_template_after.c`. Expected result: `native::bottleneck.reduce.nansum` only, because the `BN_OPT_3` line attaches to the following function. `nx_7f7afab1.diff` with `nx_generic_before.py`: expected `networkx/algorithms/shortest_paths/generic.py::_build_paths_from_predecessors` only. Build the after-file in the test by applying the diff, or construct it with `difflib`.
- Also expose `parse_unified_diff(text) -> dict[path, (old_changed_lines:set[int], new_changed_lines:set[int])]`.

### Implementer 2 — `select.py`, `safety.py`, `cost.py`, `stats.py`

**`stats.py`**
- `asv_rule(ref: Sequence[float], new: Sequence[float], factor=1.1, alpha=0.002) -> Verdict(ratio, p, status in {"faster","slower","same"})`.
  - ratio = median(new)/median(ref).
  - "slower" iff ratio > factor and two-sided Mann-Whitney U p < alpha (`scipy.stats.mannwhitneyu`, method="auto").
  - "faster" iff ratio < 1/factor and p < alpha.
- `sweperf_rule(ref, new)`: drop samples outside [Q1 − 1.5·IQR, Q3 + 1.5·IQR] per side, then MWU p < 0.1 and relative change ≥ 5 %.
- `noise_sigma(pairs: list[tuple[list,list]]) -> float`: std of log(median ratio) across same-state pairs.
- `regressed(ref, new, sigma) -> bool`: asv_rule says "slower" **and** ratio > 1 + 3·sigma.
- `wilson(k, n, z=1.96) -> (lo, hi)`.

**`select.py`** — the arms. Pure functions over data; no I/O.
- Inputs bundle `Context`:
  - `all_tests: list[TestID]`, `all_benches: list[BenchID]`
  - `depmap_at: Callable[[TestID, int], frozenset[FuncID] | None]`: the dependency set this arm last observed for that test **at a step < t**. The arm keeps its own observation history: see `ArmState.observed`.
  - `bench_profile_at` (same, for benchmarks)
  - `static_reach: dict[BenchID, frozenset[FuncID]]`
  - `module_of_test: dict[TestID, str]` (A3's mapping test → source module relpath), `module_of_bench: dict[BenchID, str]`
  - `module_functions: dict[relpath, frozenset[FuncID]]` (for module-level expansion)
  - `native_ext_funcs: dict[ext, frozenset[FuncID]]`
  - `quarantine: frozenset[TestID]`
  - `testmon_selection: dict[int, frozenset[TestID]] | None` (observed real testmon selections per step, for A2/A5)
- `Decision(build: "clean"|"incremental", tests: frozenset[TestID], benches: frozenset[BenchID], full_check: bool, fallback_reasons: tuple[str,...])`. When `full_check`, tests and benches are all of them.
- Arms (classes with `decide(t, changes: ChangeSet, st: ArmState) -> Decision` and `observe(t, decision, outcome) -> None`; `outcome.green: bool`; the observed deps are recorded in `st` from what was actually run):
  - `Full` (clean build, all, all, full_check=True every step).
  - `Inc` (incremental, all, all, full_check=False).
  - `Testmon` (tests = `testmon_selection[t]`, benches = all).
  - `ChangedModule`: tests whose `module_of_test` is in `changes.files`; benches whose `module_of_bench` is in `changes.files`.
  - `StaticBench`: tests = testmon; benches whose `static_reach` intersects the **current** change functions (module-level entries expanded via `module_functions`).
  - `Ours(accumulate=True, profile=True, trigger=("score", T=10) | ("periodic", k), w_header=5, w_fallback=5)`:
    - accumulated set A = union of change functions since the last **green** full check (current only if `accumulate=False`); module-level entries are expanded; header edits → all `native_ext_funcs` of the extension(s) whose source includes them (if unknown: all native funcs).
    - Tests = {t : `depmap_at(t)` ∩ A ≠ ∅} ∪ F4 (tests that failed at their last run ∪ tests with `module_of_test` in `changes.files`) − quarantine for decision purposes (quarantined tests are still run if selected; the flag only matters to `safety`).
    - **F2 fallback:** a changed native FuncID that appears in no observed depmap → tests that reach any `native::<same ext>.*`; if the extension is unknown or the build config changed → all tests (and set `full_check=True`).
    - Benches: if `profile`, {b : `bench_profile_at(b)` ∩ A ≠ ∅}; else the ChangedModule bench rule.
    - Score = |A| + w_header·|header edits since last green full| + w_fallback·(F2 fallbacks since last green full). Full check at t when the score is ≥ T (or t % k == 0 for periodic) **or t is the last step** (C3).
    - After a green full check: A := ∅, the score resets, and all deps are refreshed (F3), because the full check observes every test and benchmark.
  - `Periodic(inner_arm, k)`: wrapper adding a full check every k steps and at the last step.
- **Hindsight rule (blocking):** a decision at step t may use only observations from steps < t plus the change set of step t. Write a test that would fail if `decide` read a step-t depmap.

**`safety.py`**
- `simulate(arm_factory, steps: list[ChangeSet], ctx, fault) -> Detection(step|None, delay|None, by in {"selection","full_check","final","missed"})`.
  - Fault = `{id, kind in {"mutant","latent","caller","slowdown"}, step s, visible_from v (= s unless latent), extra_changed: frozenset[FuncID], kill_tests: dict[int, frozenset[TestID]] | frozenset, regress_benches: same shape}`.
  - The simulation replays the arm over all steps with the fault's `extra_changed` merged into step s's change set.
  - Detection happens at the first u ≥ v where the decision's tests ∩ kill_tests(u) ≠ ∅, or the benches ∩ regress_benches(u) ≠ ∅, or `full_check` is true.
  - A full check at u < v is green (it resets the accumulator).
  - Quarantined tests never count as detection.
  - "final" means detected by the C3 last-step full check; "missed" means not detected by the end.
- `summarise(detections) -> dict` with k_missed, n, wilson CI, mean/median delay, counts by `by`.

**`cost.py`**
- `estimate(decision, test_secs: dict, bench_secs: dict, build_secs: {"clean": x, "incremental": y, "none": 0}, overhead_secs: float) -> dict(build, tests, benches, overhead, total)`.
- `session_cost(per_step) -> cumulative list`.
- `matched_cost(frontier: list[(cost, detected_fraction)], cost) -> interpolated detected_fraction`, and `cost_at_detection(frontier, level) -> interpolated cost`.

### Implementer 3 — `monitor.py`, `depmap_plugin.py`, `staticgraph.py`

**`monitor.py`**
- `Recorder(root: Path, native_prefixes: tuple[str,...])` using `sys.monitoring` (tool id `sys.monitoring.PROFILER_ID`, or a free id with fallback).
  - `PY_START`: if `code.co_filename` is under `root` and not under excluded dirs (tests, benchmarks, site-packages), record `"<relpath>::<co_qualname>"`, then return `sys.monitoring.DISABLE`.
  - `CALL` (only when `native_prefixes` is non-empty): if the callable is a builtin/method-descriptor whose `__module__` (or `__self__.__name__` for module-level builtins) starts with a prefix, record `"native::<module>.<name>"`. Do **not** return DISABLE for CALL: call sites are polymorphic.
  - `start()`, `stop() -> frozenset[FuncID]`, `reset()`. `reset()` calls `sys.monitoring.restart_events()` so that DISABLE'd locations fire again for the next test.
  - Module-level code: `co_qualname == "<module>"` → `"<relpath>::<module>"`.
- Tests: a toy package in `tests/fixtures/toypkg/` (functions, a class method, a nested function, a call to `math.sqrt` with prefix `math` to stand in for a native module).

**`depmap_plugin.py`**
- A pytest plugin loaded with `-p bth.depmap_plugin`. Options: `--bth-depmap-out PATH`, `--bth-root PATH`, `--bth-native-prefix` (repeatable).
- For each test (setup + call + teardown) it records the set via `Recorder` and writes JSON `{nodeid: sorted list}` at session end.
- It also records per-test outcome and duration (`call` phase plus setup/teardown, as reported by pytest) to `PATH.outcomes.json`.
- Overhead (plugin vs plain) must be measurable: write nothing per test except into memory.

**`staticgraph.py`** (A5; STARTS-style, purely static, no execution)
- `build(root, package_dirs, bench_dir) -> dict[BenchID-module-or-func, frozenset[FuncID]]`.
- Uses `ast` for every `.py` under `package_dirs` and `bench_dir`:
  - **Imports:** module → imported modules within the package (resolve relative imports, `from x import y` where y is a submodule or a function).
  - **Calls:** inside each function, calls to names bound by import or defined in the same module (`foo()`, `mod.foo()`, `self.foo()` resolved within the class) → edges FuncID → FuncID.
  - **Reach for a benchmark function/method:** BFS over the call edges. Any unresolved attribute call on an imported package module (e.g. `nx.foo()`) resolves through the package's `__init__` re-exports (follow `from .x import *` and `__all__` where present). If unresolvable, add **module-level edges to every function of the imported module** (conservative, like STARTS' class-level analysis).
- Granularity is reported per bench **function/method**; params do not matter (static).
- Tests: toy package with a two-hop call chain, a re-export through `__init__`, and an unresolvable dynamic call (→ conservative module edge).

### Implementer 4 — `benchrun.py`, `junit.py`, `orchestrate.py`

**`benchrun.py`** is an asv-compatible runner. We do not depend on asv: it is not installable fast enough on this network, and owning the runner keeps the timing protocol under our control.
- `discover(bench_dir) -> list[BenchCase]`. BenchCase has `id, module, cls, name, params, param_names, timeout`.
  - Benchmarks are module functions and class methods with prefix `time_`. `track_`, `mem_` and `peakmem_` are listed but marked `kind != "time"` and not timed.
  - `params`: a single list means one parameter. A list or tuple of lists means the cartesian product. They are read from the class attribute or the function attribute (`time_k_factor.params = (...)`).
  - BenchID = `module.Class.method(p1, p2)`, using `repr` of each param value.
  - `timeout` comes from the attribute, default 60 s.
  - Discovery imports bench modules in a **subprocess** with the state on `sys.path`, so the harness process never imports target code.
- `measure(case, state_dir, python, processes=2, values=5, min_value_time=0.01, warmup_values=1, cpus=None) -> dict`.
  - Runs `processes` separate subprocesses, each with this sequence:
    - import the module, instantiate the class, call `setup(*params)` if present; `NotImplementedError` from setup means skip;
    - calibrate `number` once (timeit-style autorange until one value ≥ `min_value_time`) in the first process and reuse it in the others;
    - take `warmup_values` discarded values, then `values` values of `perf_counter` time per call;
    - call `teardown`.
  - Returns `{"id", "samples": [...], "number", "wall_s", "loadavg_before", "loadavg_after", "skipped": bool, "error": str|None}`. `wall_s` is the total wall time of measuring this case, used for cost. Load average comes from `/proc/loadavg` when present, else None.
  - `cpus` → `taskset -c` prefix on Linux when available.
  - Timeout → kill the subprocess and record the error.
- `profile(case, state_dir, python, root, native_prefixes) -> frozenset[FuncID]`: one call of the benchmark (after setup) under `bth.monitor.Recorder` in a subprocess, printed as JSON.
- `run_interleaved(cases, states: list[(label, state_dir, python)], repeats) -> list[dict]`: for each repeat, for each case, measure on each state, rotating the order of states each repeat. This serves the noise-floor, oracle-repeatability and A/B runs.
- CLI: `python -m bth.benchrun discover|measure|profile|interleave --state DIR --python EXE --bench-dir REL [--filter REGEX] --out JSON`.

**`junit.py`**: `parse(junit_xml) -> dict[nodeid, {"outcome", "duration"}]`. pytest junitxml `classname` + `name` → nodeid. Test the mapping on a real junit file produced by an inner pytester run with a test in a subdirectory, a class test and a parametrised test.

**`orchestrate.py`** is a CLI with subcommands. Each writes to `results/raw/<repo>/<subcommand>/...`, and each output JSON includes `{"repo", "state_sha", "harness_tree_hash", "cmd", "python", "platform", "started", "ended"}`. The harness tree hash is the sha256 over the sorted (path, sha256) pairs of `harness/bth/*.py`.
- `states --config C --workdir W`: wraps `replay.build_states`, check=None, and writes `edits/<repo>.states.json`.
- `oracle-tests --config C --state-dir D --label L [--junit]`: serial plain `python -m pytest <cfg tests> -p no:cacheprovider --junitxml=...`, then junit → JSON. Records exit code and wall time. **No xdist.**
- `depmap --config C --state-dir D --label L`: same test command plus `-p bth.depmap_plugin --bth-depmap-out ...`. `PYTHONPATH` gets `harness/` prepended. With pytest-xdist present and `-n` given, each worker writes `PATH.<worker_id>` and the orchestrator merges them. **Implement this in `depmap_plugin.py`**: a minimal change allowed to Implementer 4, keyed on the `PYTEST_XDIST_WORKER` env var.
- `bench --config C --state-dir D --label L [--filter] [--processes --values]` and `profile --config C --state-dir D --label L`: wrap benchrun.
- `changes --config C --workdir W`: writes the ChangeSet per step (via `changed_fns`) to JSON.
- `simulate --config C --inputs DIR --out CSV`: loads states, changes, depmaps, profiles, durations, static reach and fault matrices, builds `select.Context`, runs every arm through `safety.simulate` and `cost.estimate`, and writes per-step and per-fault CSVs. The arm list comes from the config.
- Tests: orchestration of `oracle-tests` and `depmap` on a toy repo created in tmp_path (pure Python, 3 tests), with a toy asv bench dir for `bench`/`profile`/`discover`. Use small `processes=1, values=2` in tests.

### Implementer 5 — `faults.py`

- `python_mutants(src_text, relpath, funcs: set[qualname], seed) -> list[Mutant]`. `Mutant` has `id, relpath, qualname, op, line, col, before, after, patch` (unified diff).
  - Operators: relational flip (`<`↔`<=`, `>`↔`>=`, `==`↔`!=`), int constant ±1 (not on `0`/`1` used as indices? no: keep all, deterministic), `+`↔`-`, `and`↔`or`, `return <expr>` → `return None`.
  - Edits are **in-place text edits** at exact token positions (use `tokenize` to find operator tokens inside the function's span). Never reformat the file. The patch must apply with `git apply` and change exactly one token or one expression.
  - Sites are enumerated in source order; the seeded `random.Random(seed)` shuffle picks the order. All sites are returned, and callers take a prefix.
- `c_mutants(src_text, relpath, func_spans, seed)`: the same operators on C tokens (regex tokenizer good enough for `<`, `<=`, `+`, `-`, `&&`, `||`, integer literals) within the given spans.
- `python_slowdowns(src_text, relpath, qualname) -> list[Slowdown]` (patch):
  - (a) `double_call`: rename `def f` → `def _bth_orig_f` and append a wrapper `def f(*a, **k): _bth_orig_f(*a, **k); return _bth_orig_f(*a, **k)`, with decorators kept on the wrapper. Only for non-generator, non-async functions.
  - (b) `list_membership`: inside f, each `x in <Name>` / `x not in <Name>` comparison where Name is assigned from `set(...)`, a set literal/comprehension or `dict` within the same function → `x in list(<Name>)`.
  - (c) `sorted_copy`: in the first `for` loop of f, insert as first statement `_bth_tmp = sorted(range(<len of loop iterable if it is a Name with len()>))`. Skip if not applicable.
  - Each slowdown records its `kind`.
- `revert_patch(repo_workdir, step_state_sha) -> patch`: the reverse of a replayed edit's source diff (natural regression).
- Determinism test: same inputs → byte-identical patches. Every generated patch applies cleanly to the given source (test with `git apply --check` in tmp_path) and the mutated file still parses.

## Conventions
- No network, no writes outside `03-experiment/` and the given `workdir`.
- Run every git command with `cwd` set to the target, and **never** in the PhD repo. Never use `reset --hard`, `clean` or `checkout --` outside the replay workdir.
- Each module gets a short docstring citing its rule IDs (B*, F*, P*, C*, W3-new) from `01-literature/candidate-rules.md`.
