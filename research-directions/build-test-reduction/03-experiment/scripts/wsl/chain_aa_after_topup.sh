#!/usr/bin/env bash
# Detached chain (PM 10:43): when the top-up ends (marker), start the A/A re-run and its own detached watcher (stall 420 s).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
W=$E/results/raw/watch; L=$E/results/raw/queue_0627.log
until [ -f $W/topup.marker ]; do sleep 15; done
# make sure no driver is left from the top-up before measuring
pkill -f "spotcheck_powered_nx.py|bth.benchrun"; sleep 5
echo "$(date -Iseconds) chain: top-up ended [$(cat $W/topup.marker)]; starting A/A re-run (23 cases, cap 55 min)" >> $L
setsid nohup bash $E/scripts/wsl/stall_watch_wsl2.sh aa $E/results/raw/networkx/bench/aa/driver.log $E/results/raw/networkx/bench/aa 420 'aa_noise_nx.py|bth.benchrun' > /dev/null 2>&1 < /dev/null &
sleep 1
bash $E/scripts/wsl/aa_rerun.sh > $E/results/raw/networkx/bench/aa/run2.log 2>&1
echo "$(date -Iseconds) chain: A/A driver returned" >> $L
