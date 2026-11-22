set -e
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
export PYTHONPATH=$E/harness
D=$HOME/bt-lab/exp/work
rm -rf $D/bottleneck-replay.bad
mv $D/bottleneck-replay $D/bottleneck-replay.bad
python3 $E/scripts/replay_bn.py $E 2>&1 | tee $E/results/raw/bottleneck/replay-run.txt | tail -25
git -C $D/bottleneck-replay checkout -q -f --detach 22657acaad5f27d9f692dd64362439ada8032c1b
F=$(python3 -c "import json;print([s for s in json.load(open('$E/edits/bottleneck.states.json'))['states'] if s['status']=='applied'][0]['state_sha'])")
git -C $D/bottleneck-replay diff --stat 22657ac $F | cat
git -C $D/bottleneck-replay ls-tree -r --name-only 22657ac | wc -l
