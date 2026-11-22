#!/usr/bin/env bash
# Q3 (PM 07:50): mine (freeze lists) then count; no timing; cap 1 h; marker watch/q3.marker
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
W=$E/results/raw/watch; rm -f $W/q3.marker; mkdir -p $E/results/q3
echo "$(date -Iseconds) Q3 start; load $(cut -d' ' -f1-3 /proc/loadavg)" >> $E/results/raw/queue_0627.log
cd $E && PYTHONPATH=$E/harness timeout 3600 bash -c "~/bt-lab/exp/venvs/nx/bin/python scripts/q3_count.py mine > results/q3/mine.log 2>&1 && ~/bt-lab/exp/venvs/nx/bin/python scripts/q3_count.py count > results/q3/count.log 2>&1"
rc=$?; echo "$(date -Iseconds) Q3 exit $rc" >> $E/results/raw/queue_0627.log
echo "$( [ $rc = 0 ] && echo DONE || ([ $rc = 124 ] && echo CAPPED || echo ERROR)) $(date -Iseconds) rc=$rc" > $W/q3.marker
