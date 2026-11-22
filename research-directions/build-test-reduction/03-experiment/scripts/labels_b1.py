"""Agent labels (D26, PM 15:55) -> v1 mining-rule precision, reconciliation with the earlier manual reading, and B1 restated.

Usage: python scripts/labels_b1.py -> results/labelling/precision_b1.json (+ printed summary). Compute only.
Precision: rule-qualified rows whose final label is OPT / rule-qualified rows, per project and pooled, Wilson 95 %.
Manual reading (results.md L316 and "networkx edit sets"): networkx non-OPT = steps 8, 13, 17 among the 18 replayed
(both dropped mined commits were read as OPT); geopandas 19/20 (the one non-OPT is not recorded by sha in results.md).
B1: S0 profile reach (union over the 171 profiled cases) and S0 static reach (q3_b1_static.json), module-level excluded.
"""
import json, math
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
L = exp / "results/labelling"


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 3), round((c + h) / d, 3)]


final = {r["sha"]: r for r in map(json.loads, open(L / "final_labels.jsonl", encoding="utf-8"))}
sheet = {r["sha"]: r for r in map(json.loads, open(exp / "frozen/labelling/sheet.jsonl", encoding="utf-8"))}
r1 = {r["sha"]: r for r in map(json.loads, open(L / "rater1.jsonl", encoding="utf-8"))}
SRC = {"networkx": "edits/networkx.candidates.json", "bottleneck": "edits/bottleneck.candidates.json",
       "geopandas": "edits/geopandas.q3.candidates.json", "pvlib-python": "edits/pvlib-python.q3.candidates.json"}
res = {"precision_v1": {}, "label_counts_all_rows": {}}
K = N = 0
for proj, f in SRC.items():
    d = json.loads((exp / f).read_text()); recs = d["records"] if isinstance(d, dict) else d
    q = [r for r in recs if r.get("qualifies")]
    k = sum(final[r["sha"]]["final_label"] == "OPT" for r in q)
    res["precision_v1"][proj] = {"opt": k, "qualified": len(q), "precision": round(k / len(q), 3), "wilson95": wilson(k, len(q))}
    res["label_counts_all_rows"][proj] = {lab: sum(final[r["sha"]]["final_label"] == lab for r in recs) for lab in ("OPT", "NOT_OPT", "UNSURE")}
    K += k; N += len(q)
res["precision_v1"]["pooled"] = {"opt": K, "qualified": N, "precision": round(K / N, 3), "wilson95": wilson(K, N)}

# networkx: replayed steps -> sha, manual vs agent
st = json.loads((exp / "edits/networkx.states.json").read_text())["states"]
applied = [s for s in st if s["status"] == "applied"]
manual_not = {8, 13, 17}
nx_rows = []
for i, s in enumerate(applied, 1):
    lab = final[s["orig_sha"]]["final_label"]
    nx_rows.append({"step": i, "sha": s["orig_sha"][:10], "id": sheet[s["orig_sha"]]["id"], "subject": sheet[s["orig_sha"]]["subject"][:80],
                    "manual": "NOT_OPT" if i in manual_not else "OPT", "agents": lab})
dropped = [{"sha": s["orig_sha"][:10], "id": sheet[s["orig_sha"]]["id"], "manual": "OPT", "agents": final[s["orig_sha"]]["final_label"]}
           for s in st if s["status"] != "applied"]
nx_recs = json.loads((exp / SRC["networkx"]).read_text())
nx_recs = nx_recs["records"] if isinstance(nx_recs, dict) else nx_recs
mined_shas = {r["sha"] for r in nx_recs if r.get("qualifies")}
extra = [{"sha": r["sha"][:10], "id": sheet[r["sha"]]["id"], "qualifies": r.get("qualifies"), "agents": final[r["sha"]]["final_label"],
          "subject": r["subject"][:80]} for r in nx_recs if r["sha"] not in {s["orig_sha"] for s in st}]
res["networkx_reconcile"] = {"replayed": nx_rows, "dropped_on_apply": dropped, "not_in_states": extra,
                             "disagreements": [r for r in nx_rows if r["manual"] != r["agents"]] + [r for r in dropped if r["manual"] != r["agents"]]}
geo = json.loads((exp / SRC["geopandas"]).read_text())["records"]
res["geopandas_agent_not_opt_among_qualified"] = [{"sha": r["sha"][:10], "id": sheet[r["sha"]]["id"], "subject": r["subject"][:90],
                                                    "agents": final[r["sha"]]["final_label"], "reason_r1": r1.get(r["sha"], {}).get("reason")}
                                                   for r in geo if r.get("qualifies") and final[r["sha"]]["final_label"] != "OPT"]

# B1 restated
stat = json.loads((exp / "results/q3/q3_b1_static.json").read_text())["detail"][0]
prof = json.loads((exp / "results/raw/networkx/profile/S0_181f2951.json").read_text())["profiles"]
reached = set().union(*map(set, prof.values()))
b1 = []
for e, row in zip(stat["edits"], nx_rows):
    fns = [f for f in e["changed_functions"] if not f.endswith("::<module>")]
    b1.append({"step": row["step"], "agents": row["agents"], "manual": row["manual"],
               "profile_unreached": not any(f in reached for f in fns), "static_unreached": e["unreached_edit"]})
def count(sel, key):
    rows = [r for r in b1 if sel(r)]; k = sum(r[key] for r in rows)
    return {"k": k, "n": len(rows), "share": round(k / len(rows), 3) if rows else None, "wilson95": wilson(k, len(rows))}
res["B1"] = {"per_step": b1,
             "all18": {"profile": count(lambda r: True, "profile_unreached"), "static": count(lambda r: True, "static_unreached")},
             "manual_opt": {"profile": count(lambda r: r["manual"] == "OPT", "profile_unreached"), "static": count(lambda r: r["manual"] == "OPT", "static_unreached")},
             "agent_opt": {"profile": count(lambda r: r["agents"] == "OPT", "profile_unreached"), "static": count(lambda r: r["agents"] == "OPT", "static_unreached")}}
(L / "precision_b1.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ("precision_v1", "label_counts_all_rows")}, indent=0))
print("nx disagreements:", res["networkx_reconcile"]["disagreements"])
print("nx not in states:", extra)
print("geopandas qualified non-OPT:", res["geopandas_agent_not_opt_among_qualified"])
print("B1:", json.dumps({k: v for k, v in res["B1"].items() if k != "per_step"}))
