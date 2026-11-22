#!/usr/bin/env bash
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
R=$E/results/raw/networkx/slowdowns/recheck9; mkdir -p $R; touch $R/driver.log
setsid nohup bash $E/scripts/wsl/stall_watch_wsl2.sh recheck9 $R/driver.log $R 650 'recheck9_nx.py|bth.benchrun' > /dev/null 2>&1 < /dev/null &
sleep 1
cd $E && PYTHONPATH=$E/harness timeout 1500 ~/bt-lab/exp/venvs/nx/bin/python scripts/recheck9_nx.py > $R/run.log 2>&1
rc=$?; [ $rc != 0 ] && echo "$(date -Iseconds) driver exit $rc (124 = 25 min cap hit)" >> $R/driver.log
