# S0 benchmark profiles (P1 input; not a timing). Parallel by filter on CPUs 6-11 after the RQ2 chain.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
W=$HOME/bt-lab/exp/work/networkx-replay; PY=$HOME/bt-lab/exp/venvs/nx/bin/python
export PYTHONPATH=$E/harness OMP_NUM_THREADS=1
git -C $W checkout -q --detach 181f295117f7f7488644c87f04699290f8e49188
P() { taskset -c 6-11 $PY -m bth.orchestrate --exp-root $E profile --config $E/configs/networkx.toml --state-dir $W --label "S0_181f2951.part$1" --python $PY --filter "$2" 2>&1 | tail -1; }
P 1 "^benchmark_algorithms\.UndirectedAlgorithmBenchmarks\.time_[a-l]" &
P 2 "^benchmark_algorithms\.UndirectedAlgorithmBenchmarks\.time_[m-z]" &
P 3 "^benchmark_algorithms\.DirectedAlgorithmBenchmarks" &
P 4 "^benchmark_algorithms\.(AlgorithmBenchmarksConnectedGraphsOnly|ReachabilityBenchmark)" &
P 5 "^(?!benchmark_algorithms)" &
wait
python3 - <<'PY'
import json, glob
E = "/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/networkx/profile"
parts = sorted(glob.glob(E + "/S0_181f2951.part*.json"))
out = {"meta": json.load(open(parts[0]))["meta"], "parts": [p.split("/")[-1] for p in parts], "profiles": {}, "errors": {}}
for p in parts:
    d = json.load(open(p)); out["profiles"].update(d.get("profiles", {})); out["errors"].update(d.get("errors", {}) or {})
json.dump(out, open(E + "/S0_181f2951.json", "w"))
print("merged profiles", len(out["profiles"]), "errors", len(out["errors"]))
PY
