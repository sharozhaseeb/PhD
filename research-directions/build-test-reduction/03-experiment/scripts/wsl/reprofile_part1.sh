#!/usr/bin/env bash
# Provenance check (critic 13:11): re-profile the 24 part-1 S0 cases in an ISOLATED clone at S0 (no timing; profile = functions executed).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
W=$HOME/bt-lab/exp/work/nx-prof-S0; PY=$HOME/bt-lab/exp/venvs/nx/bin/python
[ -d $W ] || git clone -q --no-hardlinks $HOME/bt-lab/exp/work/networkx-replay $W
git -C $W checkout -q -f --detach 181f295117f7f7488644c87f04699290f8e49188; git -C $W clean -fdxq
echo "$(date -Iseconds) reprofile start, tree $(git -C $W rev-parse --short HEAD)" >> $E/results/raw/networkx/profile/reprofile.log
export PYTHONPATH=$E/harness OMP_NUM_THREADS=1
timeout 2400 taskset -c 2-11 $PY -m bth.orchestrate --exp-root $E profile --config $E/configs/networkx.toml --state-dir $W --label "S0_181f2951.part1.reprofile" --python $PY --filter "^benchmark_algorithms\.UndirectedAlgorithmBenchmarks\.time_[a-l]" >> $E/results/raw/networkx/profile/reprofile.log 2>&1
rc=$?; echo "$(date -Iseconds) reprofile exit $rc, tree at end $(git -C $W rev-parse --short HEAD)" >> $E/results/raw/networkx/profile/reprofile.log
echo "$( [ $rc = 0 ] && echo DONE || echo FAIL) rc=$rc $(date -Iseconds)" > $E/results/raw/watch/reprofile.marker
