#!/usr/bin/env bash
# PM ruling 19:50 (option A, amendment 4): stop the night queue by recorded PID, keep all checkpoints, arm the waiter.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
Q=$E/results/raw/night-2026-11-22/queue.log
PIDS="1177 17660 17641 17661 17662 17970"
KIDS=$(ps -o pid= --ppid 17970 2>/dev/null | tr '\n' ' ')
echo "$(date -Iseconds) W3 stop (PM 19:50 ruling A): killing recorded PIDs $PIDS; benchrun children: ${KIDS:-none}" >> $Q
kill $PIDS $KIDS 2>/dev/null; sleep 2
left=$(ps -o pid= -p $(echo $PIDS $KIDS | tr ' ' ',') 2>/dev/null | tr '\n' ' ')
echo "$(date -Iseconds) W3 stop: still alive after SIGTERM: ${left:-none}" >> $Q
echo "$(date -Iseconds) driver exit 143 (drift; stopped by W3 per PM ruling A, checkpoints kept)" >> $E/results/raw/networkx/bench/drift/driver-drift.log
wc -l $E/results/raw/networkx/bench/drift/*.partial.jsonl >> $Q
cd $E && setsid nohup nice -n 19 ~/bt-lab/exp/venvs/nx/bin/python scripts/night_waiter.py > /dev/null 2>&1 < /dev/null &
sleep 3; tail -n 6 $Q
