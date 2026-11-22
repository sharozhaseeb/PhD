E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
mkdir -p ~/bt-lab/exp/work
cd $E && PYTHONPATH=$E/harness python3 scripts/replay_nx.py $E
