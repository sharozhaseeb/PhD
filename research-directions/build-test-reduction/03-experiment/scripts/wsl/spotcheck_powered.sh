#!/usr/bin/env bash
# Powered spot check (PM 06:10). Cap 1.5 h including gate waits.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && PYTHONPATH=$E/harness timeout 5400 ~/bt-lab/exp/venvs/nx/bin/python scripts/spotcheck_powered_nx.py
rc=$?; echo "$(date -Iseconds) driver exit $rc (124 = 1.5 h cap hit)" >> $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log
