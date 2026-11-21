"""Generate and FREEZE the networkx fault candidates (readiness §4.1, §4.2): mutants and synthetic slowdowns.

Usage: python scripts/gen_faults.py <replay-clone> [--n-mutants 25] [--n-slow 10] [--seed 20261121]
Deterministic: candidate sites come from bth.faults (seeded order); selection is round-robin over steps
1..n in step order, taking each step's next site, until N are chosen. Only functions CHANGED at step s are
mutated (plus their module only for nothing else). No test or selection result is consulted here.
Writes frozen/networkx.mutants.json, frozen/networkx.slowdowns.json and their sha256 to frozen/FROZEN.md.
Kill sets / slowdown factors are measured later against FULL (a candidate stays only if FULL detects it).
"""
import hashlib, json, subprocess, sys
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import faults  # noqa: E402

clone = Path(sys.argv[1])
arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
N_MUT, N_SLOW, SEED = arg("--n-mutants", 25), arg("--n-slow", 10), arg("--seed", 20261121)

states = [s for s in json.loads((exp / "edits/networkx.states.json").read_text())["states"] if s["status"] == "applied"]
steps = json.loads((exp / "results/raw/networkx/changes/changes.json").read_text())["steps"]
show = lambda sha, path: subprocess.run(["git", "-C", str(clone), "show", f"{sha}:{path}"],
                                        capture_output=True, check=True).stdout.decode("utf-8")

per_step_mut, per_step_slow = [], []
for t, (st, ch) in enumerate(zip(states, steps), start=1):
    by_file = {}
    for fid in ch["functions"]:
        path, q = fid.split("::", 1)
        if q != "<module>":
            by_file.setdefault(path, set()).add(q)
    muts, slows = [], []
    for path, qs in sorted(by_file.items()):
        src = show(st["state_sha"], path)
        for m in faults.python_mutants(src, path, qs, seed=SEED + t):
            muts.append({"step": t, "state_sha": st["state_sha"], **m.__dict__})
        for q in sorted(qs):
            for s in faults.python_slowdowns(src, path, q):
                slows.append({"step": t, "state_sha": st["state_sha"], **s.__dict__})
    per_step_mut.append(muts); per_step_slow.append(slows)


def round_robin(per_step, n):
    out, i = [], 0
    while len(out) < n and any(i < len(x) for x in per_step):
        for x in per_step:
            if i < len(x) and len(out) < n:
                out.append(x[i])
        i += 1
    return out


mut = round_robin(per_step_mut, N_MUT)
slow = round_robin(per_step_slow, N_SLOW)
fz = exp / "frozen"; fz.mkdir(exist_ok=True)
for name, obj in (("networkx.mutants.json", mut), ("networkx.slowdowns.json", slow)):
    (fz / name).write_text(json.dumps(obj, indent=1, default=str))
lines = [f"- `{n}` sha256 `{hashlib.sha256((fz / n).read_bytes()).hexdigest()}`" for n in
         ("networkx.mutants.json", "networkx.slowdowns.json")]
note = (f"\n## networkx fault candidates (frozen by scripts/gen_faults.py, seed {SEED})\n"
        f"Sites available per step: mutants {[len(x) for x in per_step_mut]}, slowdowns {[len(x) for x in per_step_slow]}.\n"
        f"Chosen: {len(mut)} mutants, {len(slow)} slowdowns (round-robin over steps).\n" + "\n".join(lines) + "\n")
with (fz / "FROZEN.md").open("a") as f:
    f.write(note)
print(note)
