#!/usr/bin/env bash
# Read-only status of the night-2 queue.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
R=$E/results/raw
date -Iseconds; cat /proc/loadavg
ps -eo pid,ppid,etimes,args | grep -E 'night2|bth.benchrun|stall_watch|gate_alarm|telemetry|powershell' | grep -v -E 'grep|night2_status' | cut -c1-180
echo "--- queue.log (non gate-watch, last 15)"; grep -v "gate-watch" $R/night-2026-11-23/queue.log | tail -n 15
echo "--- gate-watch last 3"; grep "gate-watch" $R/night-2026-11-23/queue.log | tail -n 3
ls -la $R/networkx/bench/dir_aa/ 2>/dev/null
tail -n 3 $R/networkx/bench/dir_aa/driver-diraa.log 2>/dev/null
tail -n 2 $R/telemetry/win-*.jsonl 2>/dev/null | cut -c1-200
