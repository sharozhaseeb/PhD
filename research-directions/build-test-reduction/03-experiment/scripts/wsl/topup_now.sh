#!/usr/bin/env bash
# 2026-11-22 after restart: spot-check top-up (#7, #9); same protocol incl. fixed base-first order; per-run checkpoint; cap 55 min.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/queue_0627.log
echo "$(date -Iseconds) TOP-UP (after PC restart) start, cap 3300 s" >> $L
echo "$(date -Iseconds) TOP-UP run (later run time, PM-approved; after PC restart) for missing spot-check slowdowns" >> $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log
cd $E && PYTHONPATH=$E/harness timeout 3300 ~/bt-lab/exp/venvs/nx/bin/python scripts/spotcheck_powered_nx.py
rc=$?; echo "$(date -Iseconds) top-up exit $rc" >> $L
echo "$(date -Iseconds) driver exit $rc (top-up)" >> $E/results/raw/networkx/slowdowns/spotcheck_powered/driver.log
