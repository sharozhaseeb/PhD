E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && PYTHONPATH=$E/harness ~/bt-lab/exp/venvs/nx/bin/python -m bth.orchestrate --exp-root $E simulate --config $E/configs/networkx.toml --inputs $E/results/sim/networkx/inputs --out $E/results/sim/networkx/rq2_steps.csv 2>&1 | tail -2
