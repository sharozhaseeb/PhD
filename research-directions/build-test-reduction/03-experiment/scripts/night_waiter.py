"""Amendment 4 (PM 19:50; scheduling only, no threshold change): restart the night queue automatically once the host
is idle. Runs detached at nice 19 in WSL:
  setsid nohup nice -n 19 ~/bt-lab/exp/venvs/nx/bin/python scripts/night_waiter.py > /dev/null 2>&1 < /dev/null &
Every 60 s: the block-gate test with the frozen thresholds (WSL load1 <= 1.0 and Windows CPU <= 20 %, Windows CPU =
mean of telemetry samples in the last 30 s, as amendment 1). After 10 consecutive passes (10 min) it starts
scripts/wsl/night_queue.sh detached (which resumes every item from its checkpoints, same order and caps, hard stop
06:25), writes the restart time to results/raw/watch/night-gate.marker, and exits. At the hard stop without a restart it
writes NOT RESTARTED and exits. Log: results/raw/night-2026-11-22/queue.log ("waiter:" lines).
"""
import json, subprocess, time
from datetime import datetime, timedelta
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
RAW = exp / "results/raw"
Q = RAW / "night-2026-11-22/queue.log"
M = RAW / "watch/night-gate.marker"


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def log(m):
    with open(Q, "a") as f:
        f.write(f"{now()} waiter: {m}\n")


def wincpu():
    fs = sorted(RAW.glob("telemetry/win-*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not fs:
        return 100.0
    t, xs = time.time(), []
    for ln in fs[-1].read_text(encoding="utf-8").splitlines()[-12:]:
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if "cpu" in r and t - r["epoch"] <= 30:
            xs.append(r["cpu"])
    return sum(xs) / len(xs) if xs else 100.0


d = datetime.now()
stop = d.replace(hour=6, minute=25, second=0, microsecond=0)
if d >= stop:
    stop += timedelta(days=1)
log(f"started (amendment 4): needs 10 consecutive passes of load1<=1.0 and wincpu<=20; hard stop {stop.isoformat(timespec='minutes')}")
ok = 0
while datetime.now() < stop - timedelta(minutes=10):
    l = float(Path("/proc/loadavg").read_text().split()[0]); w = wincpu()
    ok = ok + 1 if (l <= 1.0 and w <= 20) else 0
    log(f"check load1={l} wincpu={w:.1f} ok={ok}/10")
    if ok >= 10:
        subprocess.Popen(["setsid", "nohup", "bash", str(exp / "scripts/wsl/night_queue.sh")], cwd=str(exp),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        M.write_text(f"RESTARTED {now()} (10 x 60 s idle passed; queue resumes from checkpoints)\n")
        log("queue restarted")
        raise SystemExit(0)
    time.sleep(60)
M.write_text(f"NOT RESTARTED {now()}: host never idle for 10 min before the hard stop\n")
log("hard stop reached without restart")
