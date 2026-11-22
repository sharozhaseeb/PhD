# Same-state depmap repeats (order-dependence measurement) + S0 re-run with -n 5 (consistency), aux clone, CPUs 6-11.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
A=$HOME/bt-lab/exp/work/networkx-aux; PY=$HOME/bt-lab/exp/venvs/nx/bin/python
export PYTHONPATH=$E/harness OMP_NUM_THREADS=1
run() { git -C $A checkout -q --detach $1; find $A/networkx -name __pycache__ -type d -prune -exec rm -rf {} +
  taskset -c 6-11 $PY -m bth.orchestrate --exp-root $E depmap --config $E/configs/networkx.toml --state-dir $A --label $2 --python $PY -n 5 2>&1 | tail -1; }
S18=$(python3 -c "import json;s=[x['state_sha'] for x in json.load(open('$E/edits/networkx.states.json'))['states'] if x['status']=='applied'];print(s[-1])")
mv $E/results/raw/networkx/depmap/S0_181f2951.json $E/results/raw/networkx/depmap/S0_181f2951.n6-superseded.json.bak
run 181f295117f7f7488644c87f04699290f8e49188 S0_181f2951
run 181f295117f7f7488644c87f04699290f8e49188 S0_181f2951.rep2
run $S18 S18_${S18:0:8}.rep2
run $S18 S18_${S18:0:8}.rep3
echo "=== depmap_repeat done"
