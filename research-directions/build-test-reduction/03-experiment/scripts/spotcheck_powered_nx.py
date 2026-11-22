"""Powered out-of-reach spot check (PM 2026-11-22 06:10). Plan: results/raw/networkx/slowdowns/spotcheck_powered.plan.md.

Usage (WSL, idle machine): ~/bt-lab/exp/venvs/nx/bin/python scripts/spotcheck_powered_nx.py
For the 5 frozen slowdowns with empty reach (#0, 5, 6, 7, 9), measure the frozen 10-case spot-check sample,
interleaved base vs slowed, 5 processes x 3 values x 1 repeat (15 vs 15 samples), CPUs 2-5, asv rule.
Idle gate that POSTPONES: before each block, WSL loadavg(1m) <= 1.0 and Windows CPU <= 20 % for 3 consecutive 60 s checks.
"""
import json, os, re, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

HOME = Path.home()
SRC = HOME / "bt-lab/exp/work/networkx-replay"
PY = str(HOME / "bt-lab/exp/venvs/nx/bin/python")
out = exp / "results/raw/networkx/slowdowns/spotcheck_powered"; out.mkdir(parents=True, exist_ok=True)
LOG = out / "driver.log"
slows = json.loads((exp / "frozen/networkx.slowdowns.json").read_text())
spot = json.loads((exp / "frozen/networkx.slowdown_spotcheck.json").read_text())["sample"]
TARGETS = [0, 5, 6, 7, 9]
A, B = HOME / "bt-lab/exp/work/nx-slow-A", HOME / "bt-lab/exp/work/nx-slow-B"


def log(msg):
    line = f"{datetime.now().astimezone().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def load1():
    return float(Path("/proc/loadavg").read_text().split()[0])


def wincpu():
    try:
        r = subprocess.run(["powershell.exe", "-NoProfile", "-c",
                            "[math]::Round(((Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 2 -MaxSamples 3)"
                            ".CounterSamples | Measure-Object CookedValue -Average).Average)"],
                           capture_output=True, text=True, timeout=60)
        return float(re.sub(r"[^0-9.]", "", r.stdout) or 100)
    except Exception:
        return 100.0


def gate():
    ok = 0
    while ok < 3:
        l, w = load1(), wincpu()
        ok = ok + 1 if (l <= 1.0 and w <= 20) else 0
        log(f"gate: loadavg={l} wincpu={w} ok={ok}/3")
        if ok < 3:
            time.sleep(60)
    return {"loadavg": load1(), "wincpu": wincpu()}


def clone(dst, sha, patch=None):
    if not dst.exists():
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(dst)], check=True)
    subprocess.run(["git", "-C", str(dst), "checkout", "-q", "-f", "--detach", sha], check=True)
    subprocess.run(["git", "-C", str(dst), "clean", "-fdxq"], check=True)
    if patch:
        r = subprocess.run(["git", "-C", str(dst), "apply", "-"], input=patch.encode(), capture_output=True)
        if r.returncode:
            raise RuntimeError(r.stderr.decode())


def measure(benches, checkpoint=None):
    filt = "^(" + "|".join(re.escape(b) for b in benches) + ")$"
    with tempfile.TemporaryDirectory() as td:
        o = Path(td) / "i.json"
        env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
        subprocess.run([PY, "-m", "bth.benchrun", "interleave", "--state", f"base={A}", "--state", f"slow={B}",
                        "--python", PY, "--bench-dir", "benchmarks/benchmarks", "--filter", filt, "--repeats", "1",
                        "--processes", "5", "--values", "3", "--cpus", "2-5", "--out", str(o)]
                       + (["--checkpoint", str(checkpoint)] if checkpoint else []), env=env, check=True)
        runs = json.loads(o.read_text())
    runs = runs.get("results", runs) if isinstance(runs, dict) else runs
    samples, verdicts = {}, {}
    for r in runs:
        samples.setdefault(r["id"], {}).setdefault(r.get("state") or r.get("label"), []).extend(r.get("samples") or [])
    for b, d in samples.items():
        if d.get("base") and d.get("slow"):
            v = stats.asv_rule(d["base"], d["slow"])
            verdicts[b] = {"ratio": v.ratio, "p": v.p, "status": v.status, "n_base": len(d["base"]), "n_slow": len(d["slow"])}
    return verdicts, runs


def main():
    log(f"start; targets {TARGETS}; protocol 5 processes x 3 values x 1 repeat")
    for i in TARGETS:
        res_p = out / f"{i:02d}.json"
        if res_p.exists():
            continue
        sd = slows[i]
        clone(A, sd["state_sha"]); clone(B, sd["state_sha"], sd["patch"])
        g = gate()
        l0 = load1(); t0 = time.time()
        log(f"block {i} start: {sd['relpath']}::{sd['qualname']} load={l0}")
        verdicts, runs = measure(spot, out / f"{i:02d}.partial.jsonl")
        l1 = load1()
        peak = max([max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0) for r in runs] or [0])
        rec = {"slowdown": {k: sd[k] for k in ("step", "relpath", "qualname", "kind")},
               "plan": "results/raw/networkx/slowdowns/spotcheck_powered.plan.md",
               "protocol": {"processes": 5, "values": 3, "repeats": 1, "warmup_values": 1, "cpus": "2-5"},
               "gate_at_start": g, "load_before": l0, "load_after": l1, "peak_run_load": peak,
               "m5_label": "noisy" if peak > 1.5 else "measured-window", "wall_s": time.time() - t0,
               "cases": spot, "verdicts": verdicts,
               "slower": [b for b, v in verdicts.items() if v["status"] == "slower"],
               "reach_selection_unsafe_for_this_slowdown": any(v["status"] == "slower" for v in verdicts.values()),
               "raw_runs": runs}
        res_p.write_text(json.dumps(rec, indent=1))
        c = {}
        for v in verdicts.values():
            c[v["status"]] = c.get(v["status"], 0) + 1
        log(f"block {i} done in {rec['wall_s']:.0f}s: {c}; min p {min(v['p'] for v in verdicts.values()):.2e}; peak load {peak}")
    log("done")


if __name__ == "__main__":
    main()
