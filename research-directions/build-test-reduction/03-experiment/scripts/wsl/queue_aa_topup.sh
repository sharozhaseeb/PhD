#!/usr/bin/env bash
# PM 07:43: Q2 A/A (amendment 1), then the spot-check top-up (#7, #9; identical protocol incl. fixed order; cap 55 min).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/queue_0627.log
echo "$(date -Iseconds) Q2 A/A relaunch (amendment 1, 26 cases; first launch stopped in gate, nothing measured)" >> $L
bash $E/scripts/wsl/aa_noise.sh > $E/results/raw/networkx/bench/aa/run.log 2>&1; echo "$(date -Iseconds) Q2b exit $?" >> $L
echo "$(date -Iseconds) TOP-UP run (later run time, PM-approved) for missing spot-check slowdowns" >> $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log
cd $E && PYTHONPATH=$E/harness timeout 3300 ~/bt-lab/exp/venvs/nx/bin/python scripts/spotcheck_powered_nx.py
echo "$(date -Iseconds) top-up exit $?" >> $L
