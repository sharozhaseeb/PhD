#!/usr/bin/env bash
# Night 2 starter (PLAN night-2026-11-23): waits until 21:00 PKT, then starts telemetry, the gate alarm and the queue.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
mkdir -p $E/results/raw/night-2026-11-23
echo "$(date -Iseconds) starter pid $$: waiting for 21:00" >> $E/results/raw/night-2026-11-23/queue.log
while [ "$(date +%H%M)" -lt 2100 ] && [ "$(date +%H%M)" -gt 0625 ]; do sleep 60; done
bash $E/scripts/wsl/telemetry.sh start >> $E/results/raw/night-2026-11-23/queue.log 2>&1
cd $E && setsid nohup bash scripts/wsl/night2_queue.sh > /dev/null 2>&1 < /dev/null &
sleep 5; cd $E && setsid nohup nice -n 19 bash scripts/wsl/gate_alarm2.sh > /dev/null 2>&1 < /dev/null &
echo "$(date -Iseconds) starter: queue, telemetry and gate alarm launched" >> $E/results/raw/night-2026-11-23/queue.log
