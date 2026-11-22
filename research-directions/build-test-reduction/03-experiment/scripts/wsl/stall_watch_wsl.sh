#!/usr/bin/env bash
# Detached watcher + stall guard (PM 10:09/10:12). Runs in WSL under setsid nohup, independent of any Claude turn.
# Usage: stall_watch_wsl.sh <name> <driver.log> <checkpoint dir> <stall seconds> <pkill -f pattern>
# Writes results/raw/watch/<name>.status (heartbeat) and, at the end, <name>.marker with DONE / CAPPED / STALLED / ERROR.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
NAME=$1; LOG=$2; CK=$3; LIM=$4; PAT=$5
W=$E/results/raw/watch; M=$W/$NAME.marker; S=$W/$NAME.status
rm -f "$M"
echo "$(date -Iseconds) watcher pid $$ started for $NAME (stall ${LIM}s)" >> "$W/$NAME.log"
while true; do
  last=$(tail -n 1 "$LOG")
  case "$last" in
    *"driver exit 124"*) echo "CAPPED $(date -Iseconds) $last" > "$M"; exit 0 ;;
    *"driver exit 0"*|*"A/A done"*) echo "DONE $(date -Iseconds) $last" > "$M"; exit 0 ;;
    *"driver exit"*) echo "ERROR $(date -Iseconds) $last" > "$M"; exit 0 ;;
  esac
  cur=$(grep -v "gate:" "$LOG" | tail -n 1)
  newest=$(stat -c %Y "$LOG")
  for f in "$CK"/*.partial.jsonl; do [ -f "$f" ] && m=$(stat -c %Y "$f") && [ "$m" -gt "$newest" ] && newest=$m; done
  age=$(( $(date +%s) - newest ))
  echo "$(date -Iseconds) age=${age}s last=[$cur]" > "$S"
  case "$cur" in
    *"block"*"start"*|*"A/A start"*)
      if [ "$age" -gt "$LIM" ]; then
        pkill -f "$PAT"
        echo "$(date -Iseconds) STALL ABORT after ${age}s without a finished run (limit ${LIM}s)" >> "$LOG"
        echo "STALLED $(date -Iseconds) no finished run for ${age}s (limit ${LIM}s); killed [$PAT]" > "$M"; exit 0
      fi ;;
  esac
  sleep 15
done
