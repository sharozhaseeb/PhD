#!/usr/bin/env bash
# PM 06:4x: after Q2, top up the spot check for slowdowns cut off by the 07:40 stop (driver skips finished ones).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/queue_0627.log
until grep -q "Q2 exit" $L 2>/dev/null; do sleep 30; done
missing=$(for i in 00 05 06 07 09; do [ -f $E/results/raw/networkx/slowdowns/spotcheck_powered/$i.json ] || echo $i; done | tr '\n' ' ')
echo "$(date -Iseconds) top-up: missing [$missing]" >> $L
[ -z "$missing" ] && exit 0
echo "$(date -Iseconds) TOP-UP run (later run time, PM-approved) for [$missing]" >> $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log
cd $E && PYTHONPATH=$E/harness timeout 3300 ~/bt-lab/exp/venvs/nx/bin/python scripts/spotcheck_powered_nx.py
echo "$(date -Iseconds) top-up exit $?" >> $L
