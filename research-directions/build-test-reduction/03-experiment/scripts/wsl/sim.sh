E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && python3 scripts/assemble_inputs.py && [ -f $E/results/sim/networkx/inputs/faults.json ] || echo "[]" > $E/results/sim/networkx/inputs/faults.json
PYTHONPATH=$E/harness ~/bt-lab/exp/venvs/nx/bin/python -m bth.orchestrate --exp-root $E simulate --config $E/configs/networkx.toml --inputs $E/results/sim/networkx/inputs --out $E/results/sim/networkx/rq2_steps.csv 2>&1 | tail -5
