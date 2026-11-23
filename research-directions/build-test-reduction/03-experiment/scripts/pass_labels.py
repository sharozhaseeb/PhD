"""Single source of truth for the 9 FULL networkx passes used in R1 (PM 23:52). Compute only, reads raw files.

Usage: python scripts/pass_labels.py -> results/raw/networkx/bench/pass_labels.json (+ markdown table on stdout)
Per pass: id, raw file, kind, time span, run count, max run load (max of loadavg_before/after), runs with load > 1.5,
runs with pre_gate.ok = False, wall (sum of run wall; for the interleaved base sides, sum over the 3 base passes / 3),
rule label, and recorded label + its source.
RULE LABEL (one uniform rule, the M5 run-level rule as frozen for the night queue): a pass is "noisy" if any of its runs
has load > 1.5 or pre_gate.ok = False, else "measured-window". Recorded labels are what was written at the time; where
they differ from the rule label, the rule label is the one to cite.
"""
import json
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
RAW = exp / "results/raw/networkx"


def load(r):
    return max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0)


def summarise(pid, path, runs, kind, recorded, source, per=1):
    ts = [r.get("t_start") for r in runs if r.get("t_start")]
    return {"id": pid, "file": str(path.relative_to(exp)), "kind": kind,
            "t_first": min(ts) if ts else None, "t_last": max(ts) if ts else None,
            "n_runs": len(runs), "max_run_load": max(load(r) for r in runs),
            "runs_load_gt_1_5": sum(load(r) > 1.5 for r in runs),
            "runs_gate_not_ok": sum(1 for r in runs if r.get("pre_gate") and not r["pre_gate"].get("ok")),
            "wall_s": round(sum(r["wall_s"] for r in runs) / per, 1),
            "rule_label": "noisy" if any(load(r) > 1.5 or (r.get("pre_gate") and not r["pre_gate"].get("ok")) for r in runs)
            else "measured-window",
            "recorded_label": recorded, "recorded_source": source}


rows = []
p = RAW / "bench/S0_181f2951.idle.json"; d = json.loads(p.read_text())
rows.append(summarise("item4-S0", p, d["results"], "dedicated FULL pass, S0 (overnight item 4, 2026-11-22 05:30)",
                      "noisy", "bench/LABELS.md (load 1.63 at start)"))
for i in (1, 2, 3, 4, 8):
    p = RAW / f"slowdowns/{i:02d}.json"; d = json.loads(p.read_text())
    base = [r for r in d["raw_runs"] if r["label"] == "base"]
    rows.append(summarise(f"oracle{i:02d}-base", p, base, f"base side of slowdown #{i} oracle (3 interleaved A/B passes, 2026-11-21/22 overnight); wall = per pass",
                          "noisy" if i == 1 else "none recorded at pass level",
                          "results.md RQ1 (#1: 177/1026 runs > 1.5)" if i == 1 else "-", per=3))
for k in range(3):
    p = RAW / f"bench/drift/pass{k}.json"; d = json.loads(p.read_text())
    rows.append(summarise(f"drift-pass{k}", p, d["raw_runs"], "dedicated FULL pass, S0 (night 2026-11-22 item (d))",
                          d["m5_label"], "driver block label (night plan rule)"))
out = RAW / "bench/pass_labels.json"
out.write_text(json.dumps({"rule": __doc__.split("RULE LABEL")[1].strip(), "passes": rows}, indent=1))
print("| Pass | Kind | Runs | Max run load | Runs > 1.5 | Gate not ok | Wall (s) | Rule label | Recorded label (source) |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['id']} | {r['kind'].split(' (')[0]} | {r['n_runs']} | {r['max_run_load']:.2f} | {r['runs_load_gt_1_5']} | "
          f"{r['runs_gate_not_ok']} | {r['wall_s']:.0f} | **{r['rule_label']}** | {r['recorded_label']} ({r['recorded_source']}) |")
print("noisy by rule:", sum(r["rule_label"] == "noisy" for r in rows), "of", len(rows))
