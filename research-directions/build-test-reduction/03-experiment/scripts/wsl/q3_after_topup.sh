#!/usr/bin/env bash
# PM 07:50 Q3: after the spot-check top-up; mine (freeze lists) then count; cap 1 h total. No timing.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/queue_0627.log
until grep -q "top-up exit" $L 2>/dev/null; do sleep 30; done
echo "$(date -Iseconds) Q3 start (mine then count; cap 1 h)" >> $L
cd $E && PYTHONPATH=$E/harness timeout 3600 bash -c "python3 scripts/q3_count.py mine > results/q3/mine.log 2>&1 && python3 scripts/q3_count.py count > results/q3/count.log 2>&1"
echo "$(date -Iseconds) Q3 exit $?" >> $L
