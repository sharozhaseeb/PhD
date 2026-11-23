#!/usr/bin/env bash
# Gate-wait alarm for the night queue (PM 18:47). Read-only except its own files; run detached at nice 19:
#   setsid nohup nice -n 19 bash scripts/wsl/gate_alarm.sh > /dev/null 2>&1 < /dev/null &
# Every 60 s: if the queue's last line is a gate line, append "gate-watch: ... top_win=<name>" to queue.log
# (the top Windows CPU process from telemetry, name only). If no run has started (no *.partial.jsonl written) for
# >= 45 min, write results/raw/watch/night-gate.marker = "WAITING <min> min ...", and rewrite it every 60 min
# while the wait lasts. Exits when watch/night.marker exists. Changes no gate threshold.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
R=$E/results/raw; Q=$R/night-2026-11-22/queue.log; M=$R/watch/night-gate.marker
DIRS="$R/networkx/bench/aa_flagged $R/networkx/slowdowns/repeat $R/networkx/bench/drift $R/bottleneck/bench"
last_alarm=0
echo "$(date -Iseconds) gate-watch: alarm watcher pid $$ started (45 min threshold, repeat 60 min)" >> $Q
while [ ! -f $R/watch/night.marker ]; do
  newest=$(stat -c %Y $(ls $(for d in $DIRS; do echo $d/*.partial.jsonl; done) 2>/dev/null) 2>/dev/null | sort -n | tail -1)
  newest=${newest:-$(stat -c %Y $Q)}
  now=$(date +%s); wait_min=$(( (now - newest) / 60 ))
  top=$(tail -c 16384 $R/telemetry/win-*.jsonl 2>/dev/null | grep top_cpu_s_last_min | tail -1 | sed -n 's/.*"top_cpu_s_last_min":\[{"n":"\([^"]*\)","s":\([0-9.]*\).*/\1(\2s\/min)/p')
  case "$(tail -n 1 $Q)" in *"gate:"*|*"gate-watch:"*) echo "$(date -Iseconds) gate-watch: no run for ${wait_min} min; top_win=${top:-none}" >> $Q ;; esac
  if [ $wait_min -ge 45 ] && [ $(( now - last_alarm )) -ge 3600 ]; then
    echo "WAITING ${wait_min} min since $(date -d @$newest -Iseconds) (no run started); top_win=${top:-none}; at $(date -Iseconds)" > $M
    last_alarm=$now
  fi
  [ $wait_min -lt 45 ] && last_alarm=0
  sleep 60
done
echo "$(date -Iseconds) gate-watch: night.marker present, alarm watcher exits" >> $Q
