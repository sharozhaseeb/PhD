#!/usr/bin/env bash
# Low-priority unit tests of bth.stats in the nx venv (CPUs 0-1; never on the benchmark CPUs 2-5).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && PYTHONPATH=$E/harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python -c 'import scipy, sys; print("scipy", scipy.__version__, sys.version.split()[0])'
cd $E && PYTHONPATH=$E/harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python -m pytest -q -p no:cacheprovider tests/test_stats.py 2>&1 | tail -3
