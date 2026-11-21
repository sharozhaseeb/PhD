"""Assemble bth.orchestrate `simulate` inputs for networkx from raw oracle outputs.

Usage: python scripts/assemble_inputs.py [--faults FILE]
Reads results/raw/networkx/{oracle-tests,depmap,bench,profile,testmon,build,changes} and the static
inputs written by build_inputs.py; writes results/sim/networkx/inputs/{changes,durations,depmaps,
profiles,static_reach,modules,faults}.json.

Cost basis (readiness §5, M1): per-test seconds = serial S_0 oracle durations; per-benchmark seconds =
S_0 FULL bench wall per case; build = measured pip install -e at S_0 (FULL procedure) and 0 for the
incremental arms (pure Python, B1). Tests absent from S_0 junit get duration 0 (logged).
"""
import json, re, statistics, sys
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
raw = exp / "results/raw/networkx"
inp = exp / "results/sim/networkx/inputs"
inp.mkdir(parents=True, exist_ok=True)
step_of = lambda p: int(re.match(r"S(\d+)_", p.name).group(1))


def by_step(sub, pattern="S*_*.json"):
    return {step_of(p): json.loads(p.read_text()) for p in sorted((raw / sub).glob(pattern))
            if not p.name.endswith(".outcomes.json") and re.match(r"S\d+_[0-9a-f]{8}\.json$", p.name)}


ch = json.loads((raw / "changes/changes.json").read_text())
(inp / "changes.json").write_text(json.dumps({"steps": ch["steps"]}, indent=1))

dep = by_step("depmap")
(inp / "depmaps.json").write_text(json.dumps({str(k): v["deps"] for k, v in dep.items()}))
tests0 = by_step("oracle-tests")[0]["tests"]
all_tests = sorted(dep[0]["deps"])
test_secs = {t: float(tests0.get(t, {}).get("duration", 0.0)) for t in all_tests}
missing = [t for t in all_tests if t not in tests0]

bench = by_step("bench")
bench_secs = {}
BENCH_PENDING = 0 not in bench
if BENCH_PENDING:   # S0 bench not finished: counts only; every case gets 0 s and est. bench seconds are NOT valid
    import subprocess
    disc = Path("/tmp/disc.json")
    cases = json.loads(disc.read_text()) if disc.exists() else []
    cases = cases["cases"] if isinstance(cases, dict) else cases
    bench_secs = {c["id"]: 0.0 for c in cases if c["kind"] == "time"}
if 0 in bench:
    for c in bench[0]["results"]:
        if not c.get("skipped") and not c.get("error"):
            bench_secs[c["id"]] = float(c["wall_s"])
prof = by_step("profile")
(inp / "profiles.json").write_text(json.dumps({str(k): {b: f for b, f in v["profiles"].items() if b in bench_secs}
                                               for k, v in prof.items()}))

build0 = json.loads((raw / "build/S0_181f2951.json").read_text())["wall_s"]   # first (non-.idle) run, exact file
(inp / "durations.json").write_text(json.dumps({
    "tests": test_secs, "benches": bench_secs,
    "build": {"clean": build0, "incremental": 0.0, "none": 0.0}, "overhead": {}}, indent=1))

# static reach is per bench method; expand to every parametrised case of that method
sr = json.loads((inp / "static_reach_methods.json").read_text())
sr_cases = {b: sr.get(b.split("(")[0], []) for b in bench_secs}
mods = json.loads((inp / "modules.json").read_text())
mods["module_of_bench"] = {b: mods.get("module_of_bench_file", {}).get(b.split(".")[0]) for b in bench_secs}

tm = {}
for p in sorted((raw / "testmon").glob("S*_*.junit.xml")):
    k = step_of(p)
    if k == 0:
        continue
    sys.path.insert(0, str(exp / "harness"))
    from bth import junit
    tm[str(k)] = sorted(set(junit.parse(str(p), rootdir=str(Path.home() / "bt-lab/exp/work/networkx-testmon"))) & set(all_tests))  # drop 3 skipped-module pseudo-ids (0 s)
mods["testmon_selection"] = tm or None
(inp / "modules.json").write_text(json.dumps(mods, indent=1))
(inp / "static_reach.json").write_text(json.dumps(sr_cases))

print(f"BENCH_PENDING={BENCH_PENDING} steps {len(ch['steps'])}; depmaps at {sorted(dep)}; tests {len(all_tests)} "
      f"(no S0 duration: {len(missing)}); benches timed {len(bench_secs)}; profiles at {sorted(prof)}; "
      f"testmon steps {sorted(map(int, tm))}; build clean {build0}s")
