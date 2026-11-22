#!/usr/bin/env bash
# Amendment 1 (2026-11-22 15:35): kill the queue while it is still in its first gate, check the patched driver, restart.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
pkill -f night_queue.sh; pkill -f "night_nx.py"; sleep 1
echo "$(date -Iseconds) queue killed by W3 in its first gate (no run had started): SP.wincpu powershell probe timed out (60 s) and returned 100; amendment 1 = Windows CPU from telemetry" >> $E/results/raw/night-2026-11-22/queue.log
cd $E && PYTHONPATH=$E/harness:$E/scripts ~/bt-lab/exp/venvs/nx/bin/python - <<'EOF' || exit 1
import runpy, sys
src = open("scripts/night_nx.py").read().replace('item = sys.argv[1]', 'item = "check"')
import night_nx as N  # import works
ns = {}
exec(compile(src.split("    if item == \"gate\":")[0] + "    print('wincpu from telemetry:', SP.wincpu())\n", "night_nx", "exec"), {"__name__": "__main__", "__file__": str(N.__file__)})
EOF
setsid nohup bash scripts/wsl/night_queue.sh > /dev/null 2>&1 < /dev/null &
sleep 3; tail -n 3 $E/results/raw/night-2026-11-22/queue.log
