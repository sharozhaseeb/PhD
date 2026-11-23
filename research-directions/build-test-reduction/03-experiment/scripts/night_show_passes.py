"""Print the frozen (d)/(c) pass analysis (scripts/night_analyse.analyse_passes) and save it next to the raw files."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import night_analyse as NA

which = sys.argv[1] if len(sys.argv) > 1 else "drift"
if which == "drift":
    r = NA.analyse_passes("networkx/bench/drift", ["canary0", "pass0", "canary1", "pass1", "canary2", "pass2", "canary3"])
    out = NA.RAW / "networkx/bench/drift/analysis_drift.json"
else:
    r = NA.analyse_passes("bottleneck/bench", ["pass0", "pass1"])
    out = NA.RAW / "bottleneck/bench/analysis_bn.json"
out.write_text(json.dumps(r, indent=1, default=str))
for k, v in r.items():
    if v.get("status") == "missing":
        print(k, "missing"); continue
    print(k, {x: v[x] for x in ("n_runs", "sum_run_wall_s", "wall_s", "m5_label")}, v["telemetry"])
    if v.get("per_case_s"):
        print("   ", v["per_case_s"])
    else:
        print("   ", v["per_module_s"])
