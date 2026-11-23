"""Print the frozen E3 analysis (scripts/night_analyse.analyse_rep) for tier-1/2 blocks; save repeat/analysis_rep.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import night_analyse as NA

r = NA.analyse_rep()
(NA.RAW / "networkx/slowdowns/repeat/analysis_rep.json").write_text(json.dumps(r, indent=1, default=str))
for k, v in r.items():
    print(k, {x: v[x] for x in ("slowdown", "tier", "m5_label", "n_cases", "n_complete", "agree", "agree_exact_PRIMARY",
                                 "transitions", "transitions_exact", "pairs_agree_with_each_other")})
