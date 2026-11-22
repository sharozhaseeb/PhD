# W3-EXP — reduced build/test/benchmark validation over replayed optimization edits

**What is here:** the harness (`harness/bth/`), its tests (`tests/`), frozen inputs (`edits/`, `frozen/`, `configs/`), driver scripts (`scripts/`) and results (`results/`).
**Design and rules:** `readiness.md` (v1.1, with logged deviations) and `rules.md` (the exact deterministic selection rules, mapped to W1 rule IDs).
**Results:** `results/results.md` (PRELIMINARY), `results/worked-edit.md`, `results/rq1_bottleneck_build.md`, and `results/OVERNIGHT.md` (overnight queue done 05:58), `results/build-hazard-iterators-h.md`.

Every number in `results/*.md` names its raw file under `results/raw/`. Raw JSON files carry `meta.state_sha` (target state) and `meta.harness_tree_hash`, the sha256 over `harness/bth/*.py`.

## 0. Environment (as used)

- **OS and Python:** Windows 11 + WSL2 Ubuntu 24.04 (i5-12400F, 6C/12T, 7 GB). Runs happen in WSL. The unit tests also run on Windows Python 3.12.
- **Locations:** clones, venvs and work trees live **outside this repo** on WSL's own disk, `~/bt-lab/exp/{repos,work,venvs}` (TPM ruling 3). Scripts assume these paths, `E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment`, and the user's home `~`. Adjust `E` and the `~/bt-lab` paths for another machine.
- **Tooling:** `uv` (official release, checksum-verified) in `~/.local/bin`.
  - networkx venv: CPython 3.12.16 (uv-managed), `~/bt-lab/exp/venvs/nx`, packages in `results/raw/networkx/env-freeze.txt`.
  - bottleneck venv: CPython 3.8.20 + numpy 1.19.5 (M4: the 2019 sources do not build on 3.12), `~/bt-lab/exp/venvs/bn38`, packages in `results/raw/bottleneck/env-freeze.txt`.
- No AI is used in any selection rule or edit. Seeded randomness appears only in fault and spot-check sampling, and the seeds are recorded in `frozen/FROZEN.md`.

## 1. Harness self-tests

```bash
python -m pytest research-directions/build-test-reduction/03-experiment/tests -q -p no:cacheprovider   # from the repo root; 147 pass
```

## 2. Reproduce networkx (pilot), step by step

All commands run in WSL with `export PYTHONPATH=$E/harness` and `PY=~/bt-lab/exp/venvs/nx/bin/python`.

| Step | Command | Output |
|---|---|---|
| Clone (blobless) | `git clone --filter=blob:none https://github.com/networkx/networkx.git ~/bt-lab/exp/repos/networkx` | — |
| Mine + replay (F8 self-check against the frozen list) | `python3 scripts/replay_nx.py $E`. Before running, check out the base once in the source clone, so its blobs are present (`replay.py` asserts this). | `edits/networkx.{candidates,states}.json`; 18 states applied, 2 dropped |
| Reformat check (window rule) | `python3 scripts/reformat_check.py ~/bt-lab/exp/repos/networkx 6c1a31d1 181f2951 2e0ae8ad` | `results/raw/reformat_check_networkx.txt` |
| Env | `uv venv -p 3.12 ~/bt-lab/exp/venvs/nx && uv pip install -p … numpy scipy pandas matplotlib lxml sympy pytest pytest-xdist pytest-testmon pip "setuptools>=77.0.3" "packaging>=24.2"`, then `uv pip install -e ~/bt-lab/exp/work/networkx-replay --no-deps` | `results/raw/networkx/env-freeze.txt` |
| RQ1 FULL build + serial tests per state | `bash scripts/oracle_nx.sh build $(seq 0 18)`, then `bash scripts/oracle_nx.sh tests <i>` for each state (`SUFFIX=.idle` for idle re-runs) | `results/raw/networkx/{build,oracle-tests}/S<k>_<sha8>[.idle].json` |
| RQ1 table | `python scripts/aggregate_rq1.py networkx` | `results/rq1_networkx.csv` (with `timing_label`, `tests_concurrent_load`) |
| Change sets | `python -m bth.orchestrate --exp-root $E changes --config configs/networkx.toml --workdir <replay clone>` | `results/raw/networkx/changes/changes.json` |
| Dependency maps (per state, `-n 5`) | `python -m bth.orchestrate --exp-root $E depmap --config configs/networkx.toml --state-dir <clone at S_k> --label S<k>_<sha8> --python $PY -n 5` (loop: `scripts/wsl/rq2_chain.sh`) | `results/raw/networkx/depmap/` (**not in git**; see §5) |
| Same-state repeats (C7) | the same command twice at S0 and three times at S18 (labels `.rep2`, `.rep3`) | `results/raw/networkx/order_dependent_{S0pair,S18triple}.json` |
| Real testmon chain (A2) | `bash scripts/testmon_nx.sh` | `results/raw/networkx/testmon/` |
| Static inputs (A3/A5) | `python scripts/build_inputs.py configs/networkx.toml <clone at S0> results/sim/networkx/inputs` | `modules.json`, `static_reach_methods.json` |
| Benchmark discovery / profiles | `python -m bth.benchrun discover …`; profiles via `orchestrate profile` (5 parallel filter groups; merged) | `results/raw/networkx/profile/S0_181f2951.json` |
| Faults (frozen) | `python scripts/gen_faults.py <replay clone>` (seed 20261121) | `frozen/networkx.{mutants,slowdowns}.json` + sha256 in `frozen/FROZEN.md` |
| Kill sets / latent re-check | `$PY scripts/killsets_nx.py` and `$PY scripts/killsets_nx.py --latent` | `results/raw/networkx/faults/{killsets,latent}.json` |
| Simulation inputs | `python3 scripts/assemble_inputs.py`; then build `faults.json` from the kill sets (inline snippet in this session's log; kept: `results/sim/networkx/inputs/faults.json`) | `results/sim/networkx/inputs/` |
| Simulate all arms | `$PY -m bth.orchestrate --exp-root $E simulate --config configs/networkx.toml --inputs results/sim/networkx/inputs --out results/sim/networkx/rq2_steps.csv` | `rq2_steps.csv{,.faults.csv,.summary.csv}` |
| RQ2 headline table | `python scripts/rq2_table.py` | `results/rq2_networkx.csv` (every number in the RQ2 table) |
| Worked edit | `python3 scripts/worked_edit.py 10` | `results/worked-edit.md` |
| Overnight queue (idle-gated) | `bash scripts/overnight.sh` | `results/raw/overnight.log`, `results/raw/networkx/slowdowns/`, `results/raw/bottleneck/{retime-idle,hazard}/`, `results/raw/networkx/bench/S0_181f2951.idle.json` |

## 3. Reproduce bottleneck

- **Config:** `configs/bottleneck.toml`. The window is amended by the reformat rule (readiness §1.3, Deviation 2).
- **Steps:**
  - `python3 scripts/replay_bn.py` gives 13/16 applied; the 5-edit sensitivity replay is in `edits/bottleneck-5edit.*`.
  - Build probes: `results/rq1_bottleneck_build.md`, with raw logs in `results/raw/bottleneck/`.
  - The `iterators.h` hazard study runs as overnight item 3. Its driver scripts are copied into `scripts/wsl/bn_*.sh`; the hazard study is summarised in `results/OVERNIGHT.md`.

**WSL driver scripts** (copies of the exact scripts that were run, LF line endings): `scripts/wsl/` (uv install, venv, replay, test batch, RQ2 chain, depmap repeats, profiles, simulate, bottleneck setup, hazard study and re-timing).

## 4. Known caveats for reproduction

- **Timing.** Wall-time numbers depend on load. Every run is labelled (`timing_label`, `results/raw/concurrency_log.json`, `results/raw/networkx/bench/LABELS.md`). Counts, selections and detection are timing-independent.
- **Benchmarks.** A FULL networkx benchmark pass takes 659–2444 s with 2 processes (6 measured passes, noisy or concurrent; host load varies it about 3.7x), because `benchmark_algorithms.py` builds its graphs at import and each case runs in fresh processes. The earlier import-based bound (1.78 h at 2 processes, from a 65–71 s import measured under load) over-estimates the median measured pass by ≈ 9× (6408 s / 730 s; 2.6–9.7× across passes).
- **Line endings.** Shell scripts must stay LF. A CRLF copy fails in WSL with a syntax error.
- **Partial-clone sources.** `replay.py` refuses to proceed when base blobs are missing. Check the base out once in the source clone first.

## 5. Raw data kept out of git

The per-state dependency maps (≈ 17.7 MB each) and the assembled `depmaps.json` (≈ 299 MB) are **not committed** (`03-experiment/.gitignore`).
- **Manifest:** `results/RAW-DATA-MANIFEST.md` lists every such file with its size and **sha256**. The files are kept on disk; none are deleted.
- **Regenerate:** run the `depmap` command in §2 per state (`-n 5`), then `python3 scripts/assemble_inputs.py`.
- **Verify:** compare each file's `sha256sum` with the manifest.
- **Expected differences on regeneration:** a regenerated map may differ in about 2.4 % of functions (C7: nondeterministic attribution for first-call and data-dependent code), so sha256 equality is **not** expected for regenerated files; the manifest checks local copies. The F6-order rule's list is computed from the kept S0 pair.
