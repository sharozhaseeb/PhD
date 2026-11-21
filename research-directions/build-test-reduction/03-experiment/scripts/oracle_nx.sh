#!/usr/bin/env bash
# FULL oracle for networkx replay states (WSL). Usage: oracle_nx.sh <what> <idx>...
#   what = build | tests | depmap | bench | profile | all
#   idx  = 0 (base S_0) or 1..n (applied states in edits/networkx.states.json order)
# Every output goes to results/raw/networkx/<sub>/S<idx>_<sha8>.json via bth.orchestrate (meta block has sha + harness hash).
set -euo pipefail
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
W=$HOME/bt-lab/exp/work/networkx-replay
PY=$HOME/bt-lab/exp/venvs/nx/bin/python
export PYTHONPATH=$E/harness
what=$1; shift
sha_of() {
  if [ "$1" = 0 ]; then python3 -c "import tomllib;print(tomllib.load(open('$E/configs/networkx.toml','rb'))['replay']['base'])"
  else python3 -c "import json;s=[x for x in json.load(open('$E/edits/networkx.states.json'))['states'] if x['status']=='applied'];print(s[$1-1]['state_sha'])"; fi
}
gate() {  # M5 load gate (WSL loadavg only; Windows-side load is logged by the caller)
  read l1 _ < /proc/loadavg; echo "loadavg=$l1"
  awk -v l="$l1" 'BEGIN{exit !(l<=1.5)}' || { echo "LOAD GATE: $l1 > 1.5 — label noisy"; }
}
for i in "$@"; do
  sha=$(sha_of $i); lab="S${i}_${sha:0:8}${SUFFIX:-}"
  git -C $W checkout -q --detach $sha
  find $W/networkx -name __pycache__ -type d -prune -exec rm -rf {} +
  gate
  case $what in
    build|all)  # FULL build procedure of existing benchmarks: pip install -e per candidate (W2)
      mkdir -p $E/results/raw/networkx/build
      s=$(date +%s.%N); $PY -m pip install -q -e $W --no-deps --no-build-isolation; e=$(date +%s.%N)
      echo "{\"label\":\"$lab\",\"state_sha\":\"$sha\",\"cmd\":\"pip install -e --no-deps --no-build-isolation\",\"wall_s\":$(python3 -c "print(round($e - $s, 3))")}" > $E/results/raw/networkx/build/$lab.json ;;&
    tests|all)   $PY -m bth.orchestrate --exp-root $E oracle-tests --config $E/configs/networkx.toml --state-dir $W --label $lab --python $PY --junit ;;&
    depmap|all)  $PY -m bth.orchestrate --exp-root $E depmap --config $E/configs/networkx.toml --state-dir $W --label $lab --python $PY -n 6 ;;&
    bench|all)   $PY -m bth.orchestrate --exp-root $E bench --config $E/configs/networkx.toml --state-dir $W --label $lab --python $PY --cpus 2-5 ${BENCH_ARGS:-} ;;&
    profile|all) $PY -m bth.orchestrate --exp-root $E profile --config $E/configs/networkx.toml --state-dir $W --label $lab --python $PY ;;
  esac
  gate
done
