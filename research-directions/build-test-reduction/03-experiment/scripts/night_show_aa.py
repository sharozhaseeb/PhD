"""Print the frozen (b) analysis (scripts/night_analyse.analyse_aa) and save it to aa_flagged/analysis_aa.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import night_analyse as NA

r = NA.analyse_aa()
(NA.RAW / "networkx/bench/aa_flagged/analysis_aa.json").write_text(json.dumps(r, indent=1, default=str))
for i, d in r.items():
    print("block", i, d.get("m5_label"))
    for b, x in (d.get("cases") or {}).items():
        o = x["original"]
        print(f"  {b[-66:]:66s} n={x['n_repeats']} orig={o.get('status')} {o.get('ratio', 0):.3f} sd={x['sigma_rep'] or 0:.4f} "
              f"floor={x['floor_rep'] or 0:.3f} surv={x['survives_rep']} | fboot={x['floor_boot']:.3f} sboot={x['survives_boot']} "
              f"| aa={x['aa_pooled']} r={[round(v, 3) for v in x['ratios']]}")
