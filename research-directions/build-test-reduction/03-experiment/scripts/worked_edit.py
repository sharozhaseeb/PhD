"""Worked edit (meeting artefact): FULL vs each reduced arm for ONE replayed edit, step by step.

Usage: python3 scripts/worked_edit.py <step>   (run in WSL: needs ~/bt-lab paths and /tmp/disc.json)
Uses only observations from S0 (the last full check before the edit), so no hindsight. Writes
results/worked-edit.md. Costs = serial S0 per-test durations (M1) and S0 per-benchmark wall (FULL protocol).
"""
import json, subprocess, sys
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
raw = exp / "results/raw/networkx"
inp = exp / "results/sim/networkx/inputs"
step = int(sys.argv[1]) if len(sys.argv) > 1 else 10
STARTUP = 13.6   # median (wall - sum of durations) over 18 clean serial runs (results.md RQ2)
BUILD = 1.35     # S0 pip install -e (RQ1)

states = [s for s in json.loads((exp / "edits/networkx.states.json").read_text())["states"] if s["status"] == "applied"]
st = states[step - 1]
ch = json.loads((raw / "changes/changes.json").read_text())["steps"][step - 1]
d0 = json.loads((raw / "depmap/S0_181f2951.json").read_text())["deps"]
o0 = json.loads((raw / "oracle-tests/S0_181f2951.json").read_text())["tests"]
secs = {t: o0.get(t, {}).get("duration", 0.0) for t in d0}
mods = json.loads((inp / "modules.json").read_text())
static = json.loads((inp / "static_reach_methods.json").read_text())
bench0 = next((raw / f for f in ("bench/S0_181f2951.idle.json", "bench/S0_181f2951.json") if (raw / f).exists()), None)
bsecs = {c["id"]: c["wall_s"] for c in json.loads(bench0.read_text())["results"]} if bench0 else {}
prof0 = (raw / "profile/S0_181f2951.json") if (raw / "profile/S0_181f2951.json").exists() else None
profiles = json.loads(prof0.read_text())["profiles"] if prof0 else {}
_dj = json.loads(Path("/tmp/disc.json").read_text()) if Path("/tmp/disc.json").exists() else []
disc = _dj["cases"] if isinstance(_dj, dict) else _dj
all_bench_ids = sorted(bsecs) or sorted(c["id"] for c in disc if c["kind"] == "time")

changed = set(ch["functions"])
expanded = set(changed)
for f in changed:
    if f.endswith("::<module>"):
        expanded |= set(mods["module_functions"].get(f.split("::")[0], []))
files = set(ch["files"])

full_t = set(d0)
ours_t = {t for t, fs in d0.items() if set(fs) & expanded} | {t for t, m in mods["module_of_test"].items() if m in files}
cm_t = {t for t, m in mods["module_of_test"].items() if m in files}
static_b = {b for b in all_bench_ids if set(static.get(b.split("(")[0], [])) & expanded}
prof_b = {b for b in all_bench_ids if set(profiles.get(b, [])) & expanded} if profiles else None
cm_b = {b for b in all_bench_ids if mods["module_of_bench_file"].get(b.split(".")[0]) in files}
tm = None
for p in (raw / "testmon").glob(f"S{step}_*.junit.xml"):
    sys.path.insert(0, str(exp / "harness"))
    from bth import junit
    tm = set(junit.parse(str(p), rootdir=str(Path.home() / "bt-lab/exp/work/networkx-testmon"))) & set(d0)

T = lambda s: sum(secs.get(t, 0) for t in s)
B = lambda s: sum(bsecs.get(b, 0) for b in s) if bsecs else None
fmt = lambda x: "pending" if x is None else f"{x:.2f}"
subj = subprocess.run(["git", "-C", str(Path.home() / "bt-lab/exp/repos/networkx"), "log", "-1", "--format=%s", st["orig_sha"]],
                      capture_output=True, text=True).stdout.strip()

rows = [
    ("A0 FULL", "clean `pip install -e`", len(full_t), T(full_t), len(all_bench_ids), B(set(all_bench_ids))),
    ("A2 testmon (PerfAgent-style)", "none (pure Python, B1)", None if tm is None else len(tm), None if tm is None else T(tm), len(all_bench_ids), B(set(all_bench_ids))),
    ("A3 changed-module", "none", len(cm_t), T(cm_t), len(cm_b), B(cm_b)),
    ("A5 static-bench (+testmon tests)", "none", None if tm is None else len(tm), None if tm is None else T(tm), len(static_b), B(static_b)),
    ("A4 single-edit view (no accumulation; S0 depmap + S0 profile)", "none", len(ours_t), T(ours_t), None if prof_b is None else len(prof_b), None if prof_b is None else B(prof_b)),
]
L = [f"# Worked edit — step {step}: FULL vs reduced validation (PRELIMINARY)", "",
     f"**Edit:** `{st['orig_sha'][:8]}` — {subj}", f"**State:** S{step-1} → S{step} (`{st['state_sha'][:8]}`); replayed source diff only (readiness §2).",
     f"**Changed functions (bth.changed_fns):** " + ", ".join(f"`{f}`" for f in sorted(changed)), "",
     "**Evidence boundary:** every selection below uses only data observed at S0 (before this edit), so there is no hindsight. "
     "This is a **single-edit view**: it applies each rule to this one edit with S0 data. It is not the session simulation, where A4 accumulates changed functions since its last full check and uses checkpoint data.",
     "- Costs are *estimated seconds*: per-test serial durations and per-benchmark FULL-protocol wall time, both from S0 (readiness §5).",
     "- End-to-end adds the build and the measured median pytest startup.",
     "- Raw inputs: `raw/networkx/{depmap,oracle-tests,bench,profile,changes,testmon}/` and `sim/networkx/inputs/`.", "",
     "## Step by step", "",
     "1. **Diff → changed functions.** `bth.changed_fns` parses old/new ASTs; a function is changed if a changed line falls in its span (rules.md §1).",
     "2. **Build.** FULL runs `pip install -e` (about 1.35 s; RQ1). This is a pure-Python edit, so the reduced arms skip the build (B1).",
     "3. **Test selection.** Each arm applies its rule (rules.md §3) to the S0 observations.",
     "4. **Benchmark selection.** Each arm applies its rule (rules.md §4).",
     "5. **Decision.** Tests pass/fail, plus the asv rule on the selected benchmarks (rules.md §5).", "",
     "```mermaid", "flowchart LR", f'  E["edit {st["orig_sha"][:8]}<br/>changes {len(changed)} function(s)"] --> CF["changed_fns"]',
     '  CF --> FULL["FULL: build + all tests + all benchmarks"]', '  CF --> RED["REDUCED (ours): no build; tests reaching changed fns; benchmarks whose profile reaches them"]',
     '  FULL --> D1{"accept?"}', '  RED --> D2{"accept?"}', '  D2 -. "every k / score >= T / final" .-> FULL', "```", "",
     "## Selections and estimated cost for this edit", "",
     "| Arm | Build | Tests run | Est. test s | **Est. end-to-end tests s** (+ build + 13.6 s pytest startup) | Benchmarks run | Est. bench s |",
     "|---|---|---|---|---|---|---|"]
for a, b, nt, ts, nb, bs in rows:
    e2e = None if ts is None else ts + (STARTUP if nt else 0) + (BUILD if b.startswith("clean") else 0)
    L.append(f"| {a} | {b} | {'pending' if nt is None else nt} | {fmt(ts)} | {fmt(e2e)} | {'pending' if nb is None else nb} | {fmt(bs)} |")
L += ["", f"Tests selected by A4 that are not in A3: {len(ours_t - cm_t)}. Tests in A3 that are not in A4: {len(cm_t - ours_t)}.",
      f"Static reach (A5) selects {len(static_b)}/{len(all_bench_ids)} benchmark cases. Profile reach (A4) selects "
      f"{'pending' if prof_b is None else len(prof_b)}.", "",
      "**Reading:** test *execution* drops from about 71 s to about 0.02 s. End-to-end, though, the reduced arms still pay about 13.6 s of pytest startup, "
      "so the drop is about 86 s to about 14 s (about 6x), not 3500x. Benchmarks dominate: one FULL benchmark pass costs 659–2444 s (median about 730 s) across 6 measured passes "
      "(2 processes; noisy or concurrent; results.md, RQ1 headline). Benchmark seconds in the table are from the noisy S0 pass (item 4).", "",
      "**A4 as simulated in the session** (`sim/networkx/rq2_steps.csv`, arm OURS, step 10): its last full check was step 8, so it runs **71 tests** "
      "(accumulated since step 8) and **171/171 benchmark cases**, because profiles older than the last checkpoint count as unknown under P8 (finding B2). "
      "The single-edit row above matches the ablation without accumulation (`OURS:accumulate=False`: 38 tests).", "",
      "**Caveat.** This is one edit, shown to explain the mechanism. Costs and misses over the whole session are in `results.md` (RQ2/RQ3)."]
(exp / "results/worked-edit.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[-16:]))
