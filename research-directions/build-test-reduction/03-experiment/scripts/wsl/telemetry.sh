#!/usr/bin/env bash
# Read-only machine telemetry for night 2026-11-22 (TPM plan (d)): starts the Windows logger and a WSL logger, detached.
# Usage: telemetry.sh start | stop.  Output: results/raw/telemetry/{win,wsl}-<date>.jsonl. Changes no setting.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
T=$E/results/raw/telemetry; mkdir -p $T
D=$(date +%Y%m%d); STOP=$T/STOP
WINT=$(wslpath -w $T)
case $1 in
  start)
    rm -f $STOP
    setsid nohup powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w $E/scripts/telemetry_win.ps1)" "$WINT\\win-$D.jsonl" "$WINT\\STOP" > $T/win-logger.out 2>&1 < /dev/null &
    echo $! > $T/win-logger.pid
    setsid nohup bash -c '
      i=0
      while [ ! -f "'$STOP'" ]; do
        read l1 l5 l15 _ < /proc/loadavg; ma=$(awk "/MemAvailable/{print int(\$2/1024)}" /proc/meminfo)
        top=""
        if [ $((i % 6)) -eq 0 ]; then top=$(ps -eo pcpu=,comm= --sort=-pcpu | head -5 | awk "{printf \"%s[\\\"%s\\\",%s]\", (NR>1?\",\":\"\"), \$2, \$1}"); fi
        printf "{\"ts\":\"%s\",\"epoch\":%s,\"load1\":%s,\"load5\":%s,\"memavail_mb\":%s%s}\n" "$(date -Iseconds)" "$(date +%s)" $l1 $l5 $ma "${top:+,\"top_pcpu\":[$top]}" >> "'$T/wsl-$D.jsonl'"
        i=$((i+1)); sleep 10
      done' > $T/wsl-logger.out 2>&1 < /dev/null &
    echo $! > $T/wsl-logger.pid
    echo "telemetry started: win pid $(cat $T/win-logger.pid), wsl pid $(cat $T/wsl-logger.pid)" ;;
  stop) touch $STOP; echo "stop requested" ;;
esac
