#!/usr/bin/env bash
# Night 2 amendment 1 (21:50 on 23 Nov): night2_queue.sh had CRLF line endings (made by Git Bash sed), so it died at
# 21:00:30 before logging. Stop the starter and the old gate alarm by recorded PID, then launch the LF-fixed queue and
# the fixed gate alarm. Telemetry (pids 4884/4886) keeps running.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
Q=$E/results/raw/night-2026-11-23/queue.log
kill 4903 4905 2>/dev/null; sleep 1
echo "$(date -Iseconds) W3 amendment 1: queue never started (night2_queue.sh had CRLF line endings); starter 4903 and gate alarm 4905 stopped; relaunching LF-fixed queue and fixed alarm" >> $Q
cd $E && setsid nohup bash scripts/wsl/night2_queue.sh > $E/results/raw/night-2026-11-23/queue.stderr 2>&1 < /dev/null &
sleep 4
cd $E && setsid nohup nice -n 19 bash scripts/wsl/gate_alarm2.sh > /dev/null 2>&1 < /dev/null &
sleep 3
grep -v gate-watch $Q | tail -n 4; cat $E/results/raw/night-2026-11-23/queue.stderr
ps -eo pid,args | grep -E 'night2_queue|night2_nx|gate_alarm2' | grep -v grep | cut -c1-120
