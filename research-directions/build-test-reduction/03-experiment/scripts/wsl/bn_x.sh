E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
export PYTHONPATH=$E/harness
~/bt-lab/exp/venvs/bn38/bin/python -c "import bth.benchrun; print('38 ok')" 2>&1 | tail -3
~/bt-lab/exp/venvs/nx/bin/python -c "import bth.stats, bth.junit, scipy; print('nx ok', bth.stats.asv_rule([1,1.01,1.02],[2,2.1,2.2]))" 2>&1 | tail -3
date; cat /proc/loadavg
