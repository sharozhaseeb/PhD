#!/usr/bin/env bash
# Watcher + stall guard (PM 10:09). Usage: stall_watch.sh <driver.log> <checkpoint dir> <stall seconds> <wsl pkill pattern>
# Emits: block start/done lines, gate summaries every ~10 min, driver exit, STALL (and kills the driver).
LOG=$1; CK=$2; LIM=$3; PAT=$4
seen=$(wc -l < "$LOG"); lastgate=0
while true; do
  n=$(wc -l < "$LOG")
  if [ "$n" -gt "$seen" ]; then
    tail -n +$((seen+1)) "$LOG" | head -n $((n-seen)) | while IFS= read -r l; do
      case "$l" in
        *gate:*) now=$(date +%s); [ $((now-lastgate)) -gt 600 ] && echo "GATE $l" ;;
        *) echo "$l" ;;
      esac
    done
    seen=$n
  fi
  last=$(tail -n 1 "$LOG")
  case "$last" in *"driver exit"*|*"A/A done"*) echo "END $last"; exit 0 ;; esac
  # measuring = last non-gate line is a block/A-A start, not a done
  cur=$(grep -v "gate:" "$LOG" | tail -n 1)
  case "$cur" in
    *"block"*"start"*|*"A/A start"*|*"start; targets"*)
      newest=$(stat -c %Y "$LOG")
      for f in "$CK"/*.partial.jsonl; do [ -f "$f" ] && m=$(stat -c %Y "$f") && [ "$m" -gt "$newest" ] && newest=$m; done
      age=$(( $(date +%s) - newest ))
      if [ "$age" -gt "$LIM" ] && ! echo "$cur" | grep -q "start; targets"; then
        echo "STALL: no run finished for ${age}s (limit ${LIM}s); killing driver ($PAT)"
        powershell -c "wsl -d Ubuntu-24.04 -- pkill -f '$PAT'" >/dev/null 2>&1
        echo "$(date -Iseconds) STALL ABORT after ${age}s without a finished run (limit ${LIM}s)" >> "$LOG"
        exit 1
      fi ;;
  esac
  sleep 15
done
