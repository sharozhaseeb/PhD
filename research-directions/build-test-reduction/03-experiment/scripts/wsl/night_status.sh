#!/usr/bin/env bash
# Read-only status of the night queue.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
date -Iseconds; cat /proc/loadavg
pgrep -af 'night_queue|night_nx|stall_watch|telemetry' | grep -v pgrep
tail -n 5 $E/results/raw/night-2026-11-22/queue.log
for f in $E/results/raw/networkx/bench/aa_flagged/driver-aa.log $E/results/raw/networkx/slowdowns/repeat/driver-rep*.log $E/results/raw/networkx/bench/drift/driver-drift.log $E/results/raw/bottleneck/bench/driver-bn.log; do [ -f $f ] && { echo "== $f"; tail -n 3 $f; }; done
ls $E/results/raw/watch/ | grep night
