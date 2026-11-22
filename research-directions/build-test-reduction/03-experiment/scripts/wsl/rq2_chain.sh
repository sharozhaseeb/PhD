# RQ2 chain (non-timing counts), pinned to CPUs 6-11 so the timed S0 bench on CPUs 2-5 is disturbed less.
set -u
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
SRC=$HOME/bt-lab/exp/work/networkx-replay
A=$HOME/bt-lab/exp/work/networkx-aux
PY=$HOME/bt-lab/exp/venvs/nx/bin/python
export PYTHONPATH=$E/harness OMP_NUM_THREADS=1
[ -d $A ] || git clone -q --no-hardlinks $SRC $A
shas=$(python3 -c "import json;s=[x['state_sha'] for x in json.load(open('$E/edits/networkx.states.json'))['states'] if x['status']=='applied'];print(' '.join(s))")
i=1
for sha in $shas; do
  git -C $A checkout -q --detach $sha
  find $A/networkx -name __pycache__ -type d -prune -exec rm -rf {} +
  taskset -c 6-11 $PY -m bth.orchestrate --exp-root $E depmap --config $E/configs/networkx.toml --state-dir $A --label "S${i}_${sha:0:8}" --python $PY -n 5 2>&1 | tail -1
  i=$((i+1))
done
echo "=== testmon chain"; taskset -c 6-11 bash $E/scripts/testmon_nx.sh 2>&1 | tail -20
echo "=== killsets"; cd $E && taskset -c 6-11 $PY scripts/killsets_nx.py 2>&1 | tail -30
echo "=== done $(date)"
