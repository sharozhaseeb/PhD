#!/usr/bin/env bash
# Night queue 2026-11-22 (PM 15:20; plan results/raw/night-2026-11-22/PLAN.md). Run detached:
#   setsid nohup bash scripts/wsl/night_queue.sh > /dev/null 2>&1 < /dev/null &
# Items in order, each: block-level idle gate (no cap, but never past the hard stop), then the item under
# timeout min(cap, time left before 06:25), with a detached stall watcher (marker results/raw/watch/night-<item>.marker).
# The queue writes results/raw/watch/night.marker at the end. Resume after a kill: rerun this script (finished
# blocks are skipped, unfinished ones resume from their checkpoints).
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
PY=$HOME/bt-lab/exp/venvs/nx/bin/python
Q=$E/results/raw/night-2026-11-22; mkdir -p $Q $E/results/raw/watch
QL=$Q/queue.log
log() { echo "$(date -Iseconds) $*" >> $QL; }
STOP_AT=$(date -d "tomorrow 06:25" +%s); [ $(date +%H) -lt 6 ] && STOP_AT=$(date -d "today 06:25" +%s)
rm -f $E/results/raw/watch/night.marker
log "queue start pid $$; hard stop $(date -d @$STOP_AT -Iseconds)"
# item  cap_s  stall_s  out_dir
ITEMS="aa:7200:700:networkx/bench/aa_flagged rep1:4500:450:networkx/slowdowns/repeat drift:9000:450:networkx/bench/drift bn:2400:300:bottleneck/bench rep2:21600:450:networkx/slowdowns/repeat"
for spec in $ITEMS; do
  IFS=: read item cap stall dir <<< "$spec"
  left=$(( STOP_AT - $(date +%s) ))
  [ $left -lt 600 ] && { log "skip $item: ${left}s left before the hard stop"; continue; }
  log "$item: gate"
  ( cd $E && PYTHONPATH=$E/harness timeout $left $PY scripts/night_nx.py gate ) || { log "gate not open before the hard stop"; break; }
  left=$(( STOP_AT - $(date +%s) )); c=$(( cap < left ? cap : left ))
  DL=$E/results/raw/$dir/driver-$item.log; mkdir -p $(dirname $DL); touch $DL
  setsid nohup bash $E/scripts/wsl/stall_watch_wsl2.sh night-$item $DL $E/results/raw/$dir $stall "night_nx.py $item" > /dev/null 2>&1 < /dev/null &
  sleep 2
  log "$item: start, cap ${c}s (planned ${cap}s), stall ${stall}s"
  ( cd $E && PYTHONPATH=$E/harness timeout $c $PY scripts/night_nx.py $item >> $DL 2>&1 )
  rc=$?
  echo "$(date -Iseconds) driver exit $rc ($item; 124 = cap ${c}s hit)" >> $DL
  log "$item: driver exit $rc"
  sleep 20
done
log "queue done"
echo "DONE $(date -Iseconds)" > $E/results/raw/watch/night.marker
