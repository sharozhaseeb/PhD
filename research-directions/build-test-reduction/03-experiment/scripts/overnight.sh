#!/usr/bin/env bash
# Overnight serial queue (PM-approved 2026-11-21 19:24). Idle machine only; each item writes its own files.
# Gate: start only when WSL loadavg(1m) <= 1.0 AND Windows total CPU <= 20 % for 3 consecutive 60 s checks.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
LOG=$E/results/raw/overnight.log
log() { echo "$(date -Iseconds) $*" | tee -a $LOG; }
wincpu() { powershell.exe -NoProfile -c "[math]::Round(((Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 3).CounterSamples | Measure-Object CookedValue -Average).Average)" 2>/dev/null | tr -dc '0-9.'; }
ok=0
while [ $ok -lt 3 ]; do
  l=$(cut -d' ' -f1 /proc/loadavg); w=$(wincpu); w=${w:-100}
  if awk -v l="$l" -v w="$w" 'BEGIN{exit !(l<=1.0 && w<=20)}'; then ok=$((ok+1)); else ok=0; fi
  log "gate: loadavg=$l wincpu=$w ok=$ok/3"; sleep 60
done
log "=== 1. idle re-timing (networkx S0..S18 build + serial tests; label .idle)"
SUFFIX=.idle bash $E/scripts/oracle_nx.sh build $(seq 0 18) >> $LOG 2>&1
for i in $(seq 0 18); do SUFFIX=.idle bash $E/scripts/oracle_nx.sh tests $i >> $LOG 2>&1; done
log "=== 1b. bottleneck build re-timing (idle)"
[ -f /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_retime.sh ] && bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_retime.sh >> $LOG 2>&1
log "=== 2. slowdown oracle"
cd $E && PYTHONPATH=$E/harness ~/bt-lab/exp/venvs/nx/bin/python scripts/slowdowns_nx.py >> $LOG 2>&1
log "=== 3. bottleneck iterators.h hazard study"
[ -f /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_all_after1850.sh ] && grep -v -- '-lt 1850' /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_all_after1850.sh > /tmp/bn_all_now.sh && bash /tmp/bn_all_now.sh >> $LOG 2>&1
log "=== 4. measured FULL benchmark pass at S0 (asv default 2 processes x 3 values; label .idle)"
cd $E && SUFFIX=.idle BENCH_ARGS="--processes 2 --values 3" bash $E/scripts/oracle_nx.sh bench 0 >> $LOG 2>&1
log "=== overnight done"
