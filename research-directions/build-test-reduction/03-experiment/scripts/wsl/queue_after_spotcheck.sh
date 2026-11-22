#!/usr/bin/env bash
# PM 06:27 queue: strictly one at a time after the powered spot check: Q1 C5 simulation, then Q2 A/A (gated).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/queue_0627.log
until grep -q "driver exit" $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log 2>/dev/null; do sleep 30; done
echo "$(date -Iseconds) spot check ended; Q1 C5 simulation start" >> $L
bash $E/scripts/wsl/c5_sim.sh > $E/results/sim/networkx/c5_run.log 2>&1; echo "$(date -Iseconds) Q1 exit $?" >> $L
echo "$(date -Iseconds) Q2 A/A start (gated)" >> $L
bash $E/scripts/wsl/aa_noise.sh > $E/results/raw/networkx/bench/aa/run.log 2>&1; echo "$(date -Iseconds) Q2 exit $?" >> $L
