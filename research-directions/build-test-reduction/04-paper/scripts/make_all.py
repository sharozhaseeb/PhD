#!/usr/bin/env python3
"""Compute every paper number and build every figure from raw results.

    python scripts/make_all.py              verify inputs against data-manifest.yaml, compute, write
    python scripts/make_all.py --manifest   regenerate data-manifest.yaml from the inputs read
    python scripts/make_all.py --allow-mismatch   write outputs even when a computed value differs
                                            from macro_spec.py (still exits 1)

Outputs: generated/numbers.tex, generated/figure_data.json, figures/*.pdf, data-manifest.yaml.
Stdlib + numpy + matplotlib only. Reads JSON/CSV only; runs no benchmark.
"""
import csv
import hashlib
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parent
RES = ROOT / "03-experiment" / "results"
sys.path.insert(0, str(HERE))
from macro_spec import SPEC  # noqa: E402

MANIFEST = PAPER / "data-manifest.yaml"
Z = 1.959964

# ----------------------------------------------------------------- input registry
_READ = {}      # repo-relative posix path -> (size, sha256)
_CACHE = {}
_MAN = None     # manifest dict when verifying


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def load_manifest():
    out = {}
    if not MANIFEST.exists():
        return out
    cur = None
    for line in MANIFEST.read_text(encoding="utf8").splitlines():
        m = re.match(r'\s*-\s*path:\s*"(.*)"\s*$', line)
        if m:
            cur = {"path": m.group(1)}
            out[cur["path"]] = cur
            continue
        m = re.match(r'\s+(size|sha256):\s*"?([^"]*)"?\s*$', line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2)
    return out


def _bytes(path):
    path = Path(path)
    rel = path.relative_to(ROOT).as_posix()
    if rel in _CACHE:
        return rel, _CACHE[rel]
    b = path.read_bytes()
    _CACHE[rel] = b
    _READ[rel] = (len(b), _sha(b))
    if _MAN is not None:
        ent = _MAN.get(rel)
        if ent is None:
            fail_hard("input %s is not in data-manifest.yaml (run with --manifest)" % rel)
        if ent.get("sha256") != _READ[rel][1]:
            fail_hard("input %s changed: sha256 %s != manifest %s (run with --manifest after review)"
                      % (rel, _READ[rel][1][:12], str(ent.get("sha256"))[:12]))
    return rel, b


def fail_hard(msg):
    print("FATAL: " + msg, file=sys.stderr)
    sys.exit(2)


def text(path):
    return _bytes(path)[1].decode("utf8")


def jload(path):
    return json.loads(text(path))


def csvload(path):
    return list(csv.DictReader(text(path).splitlines()))


# ----------------------------------------------------------------- formatting
def rnd(x, dp):
    q = Decimal(1).scaleb(-dp)
    return str(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def rint(x):
    return rnd(x, 0)


def wilson(k, n, z=Z):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def sci(x, sig):
    m, e = ("%.*e" % (sig - 1, x)).split("e")
    return "%se%d" % (m, int(e))


def short(x):
    """repr-style compact float: 1.0, 0.975, 0.93."""
    return repr(round(float(x), 6))


# ----------------------------------------------------------------- data access
def D():
    d = {}
    d["rq1"] = csvload(RES / "rq1_networkx.csv")
    d["rq2"] = {r["arm"]: r for r in csvload(RES / "rq2_networkx.csv")}
    d["b1"] = jload(RES / "labelling" / "precision_b1.json")
    d["agree"] = jload(RES / "labelling" / "agreement.json")
    d["cands"] = jload(ROOT / "03-experiment" / "edits" / "networkx.candidates.json")
    d["s0"] = jload(RES / "raw/networkx/bench/S0_181f2951.idle.json")
    d["prof"] = jload(RES / "raw/networkx/profile/S0_181f2951.json")["profiles"]
    d["slow"] = {i: jload(RES / ("raw/networkx/slowdowns/%02d.json" % i)) for i in range(10)}
    d["slow_frozen"] = jload(ROOT / "03-experiment/frozen/networkx.slowdowns.json")
    d["mut_frozen"] = jload(ROOT / "03-experiment/frozen/networkx.mutants.json")
    d["kill"] = jload(RES / "raw/networkx/faults/killsets.json")
    d["latent"] = jload(RES / "raw/networkx/faults/latent.json")
    d["orderdep"] = jload(RES / "raw/networkx/order_dependent_S0pair.json")
    d["pow"] = jload(RES / "raw/stats_exact/aa_power_exact.json")
    d["share"] = jload(RES / "raw/networkx/slowdowns/share.json")  # W3 16:30, dilution check (cProfile)
    d["b1c"] = jload(RES / "q3" / "b1_construct.json")  # W3 16:30, B1 construct check (git + AST)
    d["eshare"] = jload(RES / "raw/networkx/edit_share.json")  # W3 2b, per-edit share (cProfile at parent)
    d["pow18"] = jload(RES / "raw/stats_exact/aa_power_design18.json")  # W3, power at the verdict design (18 v 18 + floor)
    d["rep"] = jload(RES / "raw/networkx/slowdowns/repeat/analysis_rep.json")  # W3 E3 tier 1
    d["drift"] = [jload(RES / ("raw/networkx/bench/drift/pass%d.json" % j)) for j in range(3)]  # W3 (d)
    d["plabels"] = jload(RES / "raw/networkx/bench/pass_labels.json")  # W3 uniform pass labels (supersedes LABELS.md 5/9)
    d["bnbench"] = jload(RES / "raw/bottleneck/bench/analysis_bn.json")  # W3 (c) bottleneck FULL passes
    d["aaflag"] = jload(RES / "raw/networkx/bench/aa_flagged/analysis_aa.json")  # W3 (b), sigma for the 12 flagged verdicts
    d["recomp"] = jload(RES / "raw/stats_exact/recompute.json")
    d["aa"] = jload(RES / "raw/networkx/bench/aa/aa_result.json")
    d["bnclean"] = [float(jload(RES / ("raw/bottleneck/retime-idle/repeat%d.json" % i))["clean_s"]) for i in (1, 2, 3)]
    return d


def passes(d):
    """The 9 measured FULL benchmark passes: S0 + base side of slowdowns 01,02,03,04,08 + 3 drift passes.
    Wall = sum of wall_s over the 171 cases of a pass; loops = sum(samples)*number; mean over the
    3 interleaved base passes of a slowdown file (as results.md 'RQ1 headline')."""
    out = []
    r = d["s0"]["results"]
    out.append({"name": "S0", "wall": sum(x["wall_s"] for x in r),
                "loops": sum(sum(x["samples"]) * x["number"] for x in r if x["samples"] and x["number"]),
                "algo": sum(x["wall_s"] for x in r if x["id"].startswith("benchmark_algorithms."))})
    for i in (1, 2, 3, 4, 8):
        w = defaultdict(float); l = defaultdict(float); a = defaultdict(float)
        for x in d["slow"][i]["raw_runs"]:
            if x["label"] != "base":
                continue
            w[x["repeat"]] += x["wall_s"]
            if x["samples"] and x["number"]:
                l[x["repeat"]] += sum(x["samples"]) * x["number"]
            if x["id"].startswith("benchmark_algorithms."):
                a[x["repeat"]] += x["wall_s"]
        reps = sorted(w)
        out.append({"name": "#%d" % i, "wall": sum(w[k] for k in reps) / len(reps),
                    "loops": sum(l[k] for k in reps) / len(reps),
                    "algo": sum(a[k] for k in reps) / len(reps)})
    # (d) three repeated FULL passes at S0 with telemetry (W3, night 22 Nov; all labelled noisy)
    for j in range(3):
        r = d["drift"][j]["raw_runs"]
        out.append({"name": "drift%d" % j, "wall": sum(x["wall_s"] for x in r),
                    "loops": sum(sum(x["samples"]) * x["number"] for x in r if x["samples"] and x["number"]),
                    "algo": sum(x["wall_s"] for x in r if x["id"].startswith("benchmark_algorithms."))})
    return out


def slowdown_classes(d):
    """Per slowdown: profile reach, flagged-slower cases on/off target (from raw verdicts)."""
    res = {}
    for i in range(10):
        s = d["slow"][i]
        fn = s["function"]
        reach = sum(1 for c, fs in d["prof"].items() if fn in fs)
        slower = [(c, v) for c, v in s["verdicts"].items() if v["status"] == "slower"]
        on = [(c, v) for c, v in slower if fn in d["prof"].get(c, [])]
        off = [(c, v) for c, v in slower if fn not in d["prof"].get(c, [])]
        if on:
            cat = "on_target"
        elif off:
            cat = "off_target"
        elif reach == 0:
            cat = "unreached"
        else:
            cat = "executed_undetected"
        res[i] = {"reach": reach, "on": on, "off": off, "cat": cat,
                  "script_class": s["class"]}
    return res


# ----------------------------------------------------------------- computed values
def compute(d):
    v = {}
    q = d["rq1"]
    pa = passes(d)
    walls = sorted(p["wall"] for p in pa)
    cl = [r for r in q if r["timing_label"] == "clean"]
    build_med = statistics.median(float(r["build_s"]) for r in q)
    tests_med = statistics.median(float(r["tests_wall_s"]) for r in cl)
    mined = sum(1 for c in d["cands"] if c["qualifies"])
    v["NxMined"] = str(mined)
    v["NxReplayed"] = str(sum(1 for r in q if int(r["step"]) >= 1))
    v["NxDropped"] = str(mined - int(v["NxReplayed"]))
    ps = d["b1"]["B1"]["per_step"]
    v["NxManualOpt"] = str(sum(1 for s in ps if s["manual"] == "OPT"))
    v["NxAgentOpt"] = str(sum(1 for s in ps if s["agents"] == "OPT"))
    v["NxStates"] = str(len(q))
    nt = {r["n_tests"] for r in q}
    v["NxNumTests"] = nt.pop() if len(nt) == 1 else "varies"
    v["NxBenchCases"] = str(len(d["s0"]["results"]))
    v["NxBenchPassMin"] = rint(walls[0])
    v["NxBenchPassMax"] = rint(walls[-1])
    v["NxBenchPassMedian"] = rint(round(statistics.median(walls) / 10) * 10)
    v["NxBenchPassSZero"] = rint(pa[0]["wall"])
    bt = round(build_med + tests_med)
    v["NxBenchRatioLo"] = rint(walls[0] / bt)
    v["NxBenchRatioHi"] = rint(walls[-1] / bt)
    v["NxAlgoCases"] = str(sum(1 for x in d["s0"]["results"] if x["id"].startswith("benchmark_algorithms.")))
    v["NxBuildMedian"] = rnd(build_med, 2)
    v["NxTestsMedianClean"] = rnd(tests_med, 1)
    v["NxTestsSession"] = rint(round(sum(float(r["tests_wall_s"]) for r in q) / 100) * 100)
    v["NxPassSpread"] = rnd(walls[-1] / walls[0], 1)
    v["NxBenchPasses"] = str(len(pa))
    v["NxBenchPassTypicalHi"] = rint(sorted(walls)[3])  # the four lowest passes, 659-751 s
    v["NxBenchRatioMedian"] = rint(statistics.median(walls) / bt)
    v["NxBenchRatioTypical"] = rint(walls[0] / bt)
    v["NxLoopsLo"] = rint(min(p["loops"] for p in pa))
    v["NxLoopsHi"] = rint(max(p["loops"] for p in pa))
    v["NxOutsideLoopsLo"] = rnd(100 * min(1 - p["loops"] / p["wall"] for p in pa), 1)
    v["NxOutsideLoopsHi"] = rnd(100 * max(1 - p["loops"] / p["wall"] for p in pa), 1)
    v["NxAlgoShareLo"] = rnd(100 * min(p["algo"] / p["wall"] for p in pa), 1)
    v["NxAlgoShareHi"] = rnd(100 * max(p["algo"] / p["wall"] for p in pa), 1)
    # noise labels of the 9 passes: uniform rule from pass_labels.json (W3, critic-checked 00:25)
    pl = d["plabels"]["passes"]
    if len(pl) != len(pa):
        fail_hard("pass_labels.json has %d passes, R1 uses %d" % (len(pl), len(pa)))
    v["PassesNoisy"] = str(sum(1 for x in pl if x["rule_label"] == "noisy"))
    v["PassesMeasured"] = str(sum(1 for x in pl if x["rule_label"] == "measured-window"))
    # bottleneck R1 (c)
    bw = [d["bnbench"][k]["sum_run_wall_s"] for k in ("pass0", "pass1")]
    v["BnBenchPassLo"] = rint(min(bw))
    v["BnBenchPassHi"] = rint(max(bw))
    v["BnBenchCases"] = str(d["bnbench"]["pass0"]["n_runs"])
    dw = [p["wall"] for p in pa if p["name"].startswith("drift")]
    v["DriftEveningHi"] = "{:,}".format(int(round(dw[0])))
    v["DriftEveningLo"] = "{:,}".format(int(round(dw[2])))
    v["DriftEveningRatio"] = rnd(dw[0] / dw[2], 2)
    dl = [p["loops"] for p in pa if p["name"].startswith("drift")]
    v["DriftLoopsLo"] = rint(min(dl))
    v["DriftLoopsHi"] = rint(max(dl))
    v["BnBuildLo"] = rnd(min(d["bnclean"]), 1)
    v["BnBuildHi"] = rnd(max(d["bnclean"]), 1)
    # B1 reach
    b1 = d["b1"]["B1"]
    def grp(prefix, key, name):
        g = b1[key]
        for meth, sfx in (("profile", ""), ("static", "Static")):
            k, n = g[meth]["k"], g[meth]["n"]
            lo, hi = wilson(k, n)
            v["BOne%s%s" % (prefix, "Unreached" if not sfx else "Static")] = str(k)
            v["BOne%s%sPct" % (prefix, sfx)] = rint(100 * k / n)
            v["BOne%s%sLo" % (prefix, sfx)] = rint(100 * lo)
            v["BOne%s%sHi" % (prefix, sfx)] = rint(100 * hi)
    grp("Agent", "agent_opt", "agents")
    grp("Manual", "manual_opt", "manual")
    grp("All", "all18", "all")
    # labelling
    a = d["agree"]
    v["LabelRows"] = str(a["n"]); v["LabelAgree"] = str(a["agree"])
    v["LabelKappa"] = rnd(a["kappa_3cat"], 3); v["LabelAdjudicated"] = str(len(a["to_adjudicate"]))
    pv = d["b1"]["precision_v1"]
    for tag, key in (("Nx", "networkx"), ("Bn", "bottleneck"), ("Gp", "geopandas"), ("Pv", "pvlib-python"), ("Pooled", "pooled")):
        k, n = pv[key]["opt"], pv[key]["qualified"]
        lo, hi = wilson(k, n)
        v["Prec" + tag] = str(k)
        v["Prec%sN" % tag] = str(n)
        v["Prec%sLo" % tag] = rint(100 * lo)
        v["Prec%sHi" % tag] = rint(100 * hi)
        if tag == "Pooled":
            v["PrecPooledPct"] = rint(100 * k / n)
    # slowdowns
    sc = slowdown_classes(d)
    v["NumSlowdowns"] = str(len(d["slow_frozen"]))
    det = sum(1 for i in range(10) if not sc[i]["script_class"].startswith("not detected"))
    v["SlowDetClassified"] = str(det)
    lo, hi = wilson(det, 10)
    v["SlowDetClassLo"] = rnd(100 * lo, 1); v["SlowDetClassHi"] = rnd(100 * hi, 1)
    ont = sum(1 for i in range(10) if sc[i]["cat"] == "on_target")
    lo, hi = wilson(ont, 10)
    v["SlowDetOnTargetLo"] = rnd(100 * lo, 1); v["SlowDetOnTargetHi"] = rnd(100 * hi, 1)
    r2 = [x[1]["ratio"] for x in sc[2]["on"]]
    v["SlowTwoRatioLo"] = rnd(min(r2), 2); v["SlowTwoRatioHi"] = rnd(max(r2), 2)
    v["SlowEightRatio"] = rnd(sc[8]["on"][0][1]["ratio"], 3)
    v["SlowOneRatio"] = rnd(sc[1]["off"][0][1]["ratio"], 3)
    fam = d["recomp"]["families"]
    p1 = [x["exact"]["p"] for x in fam["slowdown01_oracle"].values() if x["exact"]["status"] == "slower"]
    v["SlowOneExactP"] = sci(p1[0], 3)
    p9 = [x["exact"]["p"] for k, x in fam["powered09"].items() if x["exact"]["status"] == "slower"]
    v["SlowNineExactP"] = sci(p9[0], 3)
    # A/A
    cases = d["aa"]["cases"]
    comps = [c[r] for c in cases.values() for r in ("rep0", "rep1")]
    v["AAComparisons"] = str(len(comps))
    v["AAFalse"] = str(sum(1 for c in comps if c["status"] != "same"))
    v["AAUpper"] = rnd(100 * wilson(int(v["AAFalse"]), len(comps))[1], 1)
    v["AACases"] = str(len(cases))
    v["AAAlgoCases"] = str(sum(1 for k in cases if k.startswith("benchmark_algorithms.")))
    ex = d["pow"]["exact"]
    v["PowAllOneTwo"] = short(ex["median_all"]["1.2"])
    v["PowAlgoOneTwo"] = short(ex["median_algorithms"]["1.2"])
    v["PowAllTwo"] = short(ex["median_all"]["2.0"])
    v["PowAlgoTwo"] = short(ex["median_algorithms"]["2.0"])
    v["PowAllOneOneTwo"] = short(ex["median_all"]["1.12"])
    v["PowAlgoOneOneTwo"] = short(ex["median_algorithms"]["1.12"])
    rc = d["recomp"]
    v["RecomputeVerdicts"] = str(sum(len(x) for x in rc["families"].values()))
    v["RecomputeChanged"] = str(len(rc["changes"]))
    v["MinPSixSix"] = rnd(rc["min_attainable_p"]["6x6"]["exact"], 5)
    v["MinPFifteen"] = sci(rc["min_attainable_p"]["15x15"]["exact"], 2)
    v["AsvAlpha"] = short(rc["alpha"]); v["AsvFactor"] = short(rc["factor"])
    # RQ4
    r2q = d["rq2"]
    v["TestmonMeasured"] = rint(float(r2q["TESTMON"]["measured_end_to_end_s"]))
    v["FullMeasured"] = rint(float(r2q["FULL"]["measured_end_to_end_s"]))
    v["TestsRunFull"] = r2q["FULL"]["tests_run"]
    v["TestsRunTestmon"] = r2q["TESTMON"]["tests_run"]
    v["TestsRunAThree"] = r2q["CHANGED_MODULE"]["tests_run"]
    v["EstFull"] = r2q["FULL"]["est_end_to_end_s"]
    v["EstTestmon"] = r2q["TESTMON"]["est_end_to_end_s"]
    v["EstAThree"] = r2q["CHANGED_MODULE"]["est_end_to_end_s"]
    v["EstAFour"] = r2q["OURS"]["est_end_to_end_s"]
    v["EstTestmonKFive"] = r2q["PERIODIC:inner=TESTMON,k=5"]["est_end_to_end_s"]
    v["EstTestmonKThree"] = r2q["PERIODIC:inner=TESTMON,k=3"]["est_end_to_end_s"]
    v["AFourChecks"] = r2q["OURS"]["full_checks"]
    nm = len(d["mut_frozen"]); nk = sum(1 for x in d["kill"] if x["kill_tests"])
    v["MutantsFrozen"] = str(nm); v["MutantsKilled"] = str(nk); v["MutantsSurvive"] = str(nm - nk)
    miss = int(r2q["CHANGED_MODULE"]["k_missed"])
    v["AThreeMissed"] = str(miss)
    lo, hi = wilson(miss, nk)
    v["AThreeMissLo"] = rnd(100 * lo, 1); v["AThreeMissHi"] = rnd(100 * hi, 1)
    v["ZeroMissHi"] = rnd(100 * wilson(0, nk)[1], 1)
    v["LatentFound"] = str(sum(1 for x in d["latent"] if x["latent"] is not None))
    v["AccumExtraRuns"] = str(int(r2q["OURS"]["tests_run"]) - int(r2q["OURS:accumulate=False"]["tests_run"]))
    v["BTwoStatic"] = r2q["STATIC_BENCH"]["bench_cases_selected"]
    v["BTwoFull"] = r2q["FULL"]["bench_cases_selected"]
    v["BTwoStaticShare"] = rint(100 * int(v["BTwoStatic"]) / int(v["BTwoFull"]))
    v["CSevenFuncs"] = str(len(d["orderdep"]["functions"]))
    # W6 hostile-review checks (results.md section of that name)
    v["ConstructUnreached"] = str(len(d["b1c"]["summary"]["unreached_by_construction"]))
    def shares(i):
        return [c["share"] for c in d["share"][str(i)]["cases"].values()]
    v["ShareTwoLo"] = "%.2f" % min(shares(2)); v["ShareTwoHi"] = "%.2f" % max(shares(2))
    v["ShareThreeLo"] = "%.3f" % min(shares(3)); v["ShareThreeHi"] = "%.3f" % max(shares(3))
    v["ShareEight"] = "%.2f" % max(shares(8))
    # hostile review of draft 2: one definition of a miss = not detected on target
    sc = slowdown_classes(d)
    # (b) pre-registered 1 + 3 sigma floor: slowdowns with an on-target case that survives
    surv = 0
    for i in sc:
        a = d["aaflag"].get(str(i))
        if not a or not sc[i]["on"]:
            continue
        oncases = {c for c, _ in sc[i]["on"]}
        if any(a["cases"][c]["survives_rep"] for c in oncases if c in a["cases"]):
            surv += 1
    lo, hi = wilson(surv, len(sc))
    v["FloorDetect"] = str(surv)
    v["FloorDetectLo"] = "%.1f" % (100 * lo)
    v["FloorDetectHi"] = "%.1f" % (100 * hi)
    def floor_of(i, pred):
        cs = [c for c in d["aaflag"][str(i)]["cases"].items() if pred(c[0])]
        return cs[0][1]
    on8 = {c for c, _ in sc[8]["on"]}
    v["FloorEight"] = "%.2f" % floor_of(8, lambda c: c in on8)["floor_rep"]
    off1 = {c for c, _ in sc[1]["off"]}
    v["FloorOne"] = "%.2f" % floor_of(1, lambda c: c in off1)["floor_rep"]
    v["FloorNine"] = "%.3f" % list(d["aaflag"]["9"]["cases"].values())[0]["floor_rep"]
    # 2b per-edit share: edits whose expected ratio clears the asv factor (strictly above)
    es = d["eshare"]
    fac = 1.1
    v["EditsClearMid"] = str(sum(1 for r in es.values() if round(r["expected_ratio_at_1.2x"], 3) > fac))  # compared at the displayed 3 d.p., as results.md does (step 10: 1.1004 -> 1.100, "at" the factor)
    v["EditsClearHigh"] = str(sum(1 for r in es.values() if round(r["expected_ratio_at_2x"], 3) > fac))
    v["EditShareDiluted"] = "%.3f" % min(r["max_share"] for r in es.values() if r["executed_S0_profile"])
    big = [r["max_share"] for r in es.values() if r["executed_S0_profile"] and r["max_share"] > 0.1]
    v["EditShareBigLo"] = "%.2f" % min(big)
    v["EditShareBigHi"] = "%.2f" % max(big)
    # power at the verdict design, 18 v 18, exact test + 1 + 3 sigma floor
    g = lambda x: "%g" % x
    P = d["pow18"]
    v["PowDesignAllMid"] = g(P["sigma_rep"]["median_all"]["1.2"])
    v["PowDesignAlgoMid"] = g(P["sigma_rep"]["median_algorithms"]["1.2"])
    v["PowDesignAlgoMidBoot"] = g(P["sigma_boot"]["median_algorithms"]["1.2"])
    v["PowDesignAlgoOneFive"] = g(P["sigma_rep"]["median_algorithms"]["1.5"])
    v["PowDesignAlgoTwo"] = g(P["sigma_rep"]["median_algorithms"]["2.0"])
    v["PowDesignAlgoMidNoFloor"] = g(P["none"]["median_algorithms"]["1.2"])
    # E3 tier 1 (repeated slowdown oracle)
    R = d["rep"]
    R1 = {k: b for k, b in R.items() if k.startswith("t1_")}
    v["RepAgree"] = str(sum(b["agree_exact_PRIMARY"] for b in R1.values()))
    v["RepTotal"] = str(sum(b["n_complete"] for b in R1.values()))
    # E3 tier 2 (remaining cases of #2, #3, #4; #8 partial and #1 not run)
    R2 = {k: b for k, b in R.items() if k.startswith("t2_")}
    n2 = sum(b["n_complete"] for b in R2.values())
    a2 = sum(b["agree_exact_PRIMARY"] for b in R2.values())
    f2 = n2 - a2
    lo, hi = wilson(f2, n2)
    v["TwoAgree"] = str(a2)
    v["TwoTotal"] = str(n2)
    v["TwoFlips"] = str(f2)
    v["TwoFlipPct"] = "%.1f" % (100 * f2 / n2)
    v["TwoFlipLo"] = "%.1f" % (100 * lo)
    v["TwoFlipHi"] = "%.1f" % (100 * hi)
    v["TwoFaster"] = str(sum(b["transitions_exact"].get("same->faster", 0) for b in R2.values()))
    on2 = {c for c, _ in sc[2]["on"]}
    r2 = [x["ratio"] for c, x in R["t1_02"]["slower_now"].items() if c in on2]
    if len(r2) != len(on2):
        fail_hard("E3: not every #2 on-target case is still slower")
    v["RepTwoLo"] = "%.2f" % min(r2)
    v["RepTwoHi"] = "%.2f" % max(r2)
    v["RepEightRatio"] = "%.3f" % list(R["t1_08"]["slower_now"].values())[0]["ratio"]
    v["SlowUndetected"] = str(sum(1 for i in sc if sc[i]["cat"] != "on_target"))
    return v


# ----------------------------------------------------------------- numbers.tex
def tex_value(val):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)e(-?\d+)", val)
    if m:
        return r"\ensuremath{%s\times10^{%d}}" % (m.group(1), int(m.group(2)))
    return val


BS = chr(92)


def write_oracle_table(d):
    """Per-edit oracle table (advisor review 2026-11-22; W3 2b shares). One row per
    agent-labelled optimization: reaching cases (S0 profile), largest share of a reaching
    case's time in the changed functions (cProfile at the edit's parent), and the expected
    case-level ratio if the changed code were 1.2x or 2x slower, 1 + share*(f-1).
    Bold = above asv's 1.1 factor, i.e. could be flagged before noise is considered."""
    prof = {c: set(fs) for c, fs in d["prof"].items()}
    steps = [s for s in d["b1c"]["steps"] if s["agents"] == "OPT"]
    es = d["eshare"]
    expected = {3: 8, 4: 3, 9: 4, 10: 1, 14: 1, 16: 4}  # results.md: "steps 3: 8, 4: 3, 9: 4, 10: 1, 14: 1, 16: 4"
    rows = []
    for s in steps:
        fns = {f["fn"] for f in s["functions"]}
        n = sum(1 for c in prof.values() if c & fns)
        if (n == 0) != bool(s["profile_unreached"]):
            fail_hard("oracle table: step %d reach %d disagrees with profile_unreached" % (s["step"], n))
        if s["step"] in expected and expected[s["step"]] != n:
            fail_hard("oracle table: step %d has %d reaching cases, results.md says %d" % (s["step"], n, expected[s["step"]]))
        r = es[str(s["step"])]
        if bool(r["executed_S0_profile"]) != (n > 0):
            fail_hard("oracle table: step %d executed flag disagrees with edit_share.json" % s["step"])
        names = sorted({f["fn"].split("::")[1].split(".<locals>")[0] for f in s["functions"]})
        short = names[0] + (" +%d" % (len(names) - 1) if len(names) > 1 else "")
        short = short.replace("_", BS + "_")
        def ratio(x):
            cell = "%.3f" % x
            return (BS + "textbf{" + cell + "}") if round(x, 3) > 1.1 else cell
        if n:
            cells = (str(n), "%.3f" % r["max_share"], ratio(r["expected_ratio_at_1.2x"]), ratio(r["expected_ratio_at_2x"]))
        else:
            cells = ("--", "--", "--", "--")
        rows.append("%d & " % s["step"] + BS + "texttt{" + short + "} & " + " & ".join(cells) + " " + BS + BS)
    out = ["% Generated by scripts/make_all.py (write_oracle_table). DO NOT EDIT.",
           BS + "begin{tabular}{@{}rlrrrr@{}}", BS + "toprule",
           "Step & Changed function & Cases & Max share & Ratio at $1.2" + BS + "times$ & Ratio at $2" + BS + "times$ " + BS + BS,
           BS + "midrule"] + rows + [BS + "bottomrule", BS + "end{tabular}"]
    (PAPER / "generated" / "oracle_table.tex").write_text(chr(10).join(out) + chr(10), encoding="utf8")


def write_numbers(spec_values):
    rf = _READ_REL("03-experiment/results/results.md")
    kf = _READ_REL("knowledge-base/findings.md")
    lines = ["% Generated by scripts/make_all.py. DO NOT EDIT.",
             "%% results.md sha256:%s  findings.md sha256:%s" % (rf[:12], kf[:12]), ""]
    for name, val, kind, anchor, source in SPEC:
        if anchor.startswith("FILE:"):
            # FILE:<path relative to build-test-reduction>::<literal text>
            rel = anchor[5:].split("::", 1)[0]
            a, aname = _READ_REL(rel), rel.rsplit("/", 1)[-1]
        else:
            a = kf if anchor.startswith("KB:") else rf
            aname = "findings.md" if anchor.startswith("KB:") else "results.md"
        lines.append("%% %s = %s | %s | %s | %s sha256:%s" % (name, spec_values[name], kind, source.replace("\n", " "), aname, a[:12]))
        lines.append(r"\newcommand{\%s}{%s}" % (name, tex_value(spec_values[name])))
    (PAPER / "generated").mkdir(exist_ok=True)
    (PAPER / "generated" / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf8")


def _READ_REL(rel):
    _bytes(ROOT / rel)
    return _READ[rel][1]


def write_manifest():
    lines = ["# Inputs read by scripts/make_all.py. Regenerate with: python scripts/make_all.py --manifest",
             "# Paths are relative to the repository folder research-directions/build-test-reduction/.",
             "inputs:"]
    for rel in sorted(_READ):
        size, sha = _READ[rel]
        lines += ['  - path: "%s"' % rel, '    size: %d' % size, '    sha256: "%s"' % sha]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf8")


# ----------------------------------------------------------------- figures
OI = {"black": "#000000", "orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73",
      "yellow": "#F0E442", "blue": "#0072B2", "verm": "#D55E00", "purple": "#CC79A7", "grey": "#999999"}


def figures(d, fd):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "sans-serif", "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5, "legend.fontsize": 6, "axes.linewidth": 0.6, "pdf.fonttype": 42,
        "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "lines.linewidth": 1.0,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.03, "pdf.compression": 6,
    })
    out = PAPER / "figures"
    out.mkdir(exist_ok=True)
    if "--png" in sys.argv:
        pngdir = Path(sys.argv[sys.argv.index("--png") + 1])
        _orig = matplotlib.figure.Figure.savefig
        def _both(self, fname, *a, **k):
            _orig(self, fname, *a, **k)
            _orig(self, pngdir / (Path(fname).stem + ".png"), *a, dpi=200, **k)
        matplotlib.figure.Figure.savefig = _both
    pa = passes(d)
    walls = [p["wall"] for p in pa]

    # ---- fig_cost
    q = d["rq1"]
    cl = [r for r in q if r["timing_label"] == "clean"]
    bmed = statistics.median(float(r["build_s"]) for r in q)
    tmed = statistics.median(float(r["tests_wall_s"]) for r in cl)
    # whisker: first-run range over clean states, excluding S16/S17 (noisy / borderline first runs)
    tvals = [float(r["tests_wall_s"]) for r in cl if not r["state"].startswith(("S16_", "S17_"))]
    wmed = statistics.median(walls)
    lmed = statistics.median(p["loops"] for p in pa)
    segs = [("Build (median)", bmed, OI["blue"]), ("Serial tests (median)", tmed, OI["sky"]),
            ("Benchmark timing loops", lmed, OI["green"]),
            ("Benchmark, outside timing loops", wmed - lmed, OI["orange"])]
    fd["cost"] = {"build_median_s": bmed, "tests_median_clean_s": tmed, "tests_range_clean_s": [min(tvals), max(tvals)],
                  "pass_wall_median_s": wmed, "loops_median_s": lmed, "passes": pa}
    fig, ax = plt.subplots(figsize=(3.4, 2.3))
    left = 0
    for lab, w, c in segs:
        ax.barh(1, w, left=left, color=c, edgecolor="white", linewidth=0.4, height=0.5, label="%s, %s s" % (lab, ("%.1f" % w) if w < 100 else ("%.0f" % w)))
        left += w
    x0 = bmed + tmed
    ax.errorbar([x0 - tmed / 2 + tmed / 2], [1.0], xerr=[[tmed - min(tvals)], [max(tvals) - tmed]], fmt="none",
                ecolor="black", elinewidth=0.8, capsize=2, capthick=0.8)
    ax.text(x0 + 60, 0.62, "tests, clean states: %.0f to %.0f s" % (min(tvals), max(tvals)), fontsize=6, va="top", ha="left")
    ax.set_yticks([1, 0]); ax.set_yticklabels(["Median pass,\nper edit", "6 measured\nbenchmark passes"])
    ax.plot([min(walls), max(walls)], [0, 0], color=OI["grey"], lw=1.2, zorder=1)
    ax.scatter(walls, [0] * len(walls), s=14, color=OI["verm"], zorder=3, edgecolor="white", linewidth=0.3)
    ax.text(min(walls), -0.28, "%.0f s" % min(walls), ha="center", fontsize=6, va="top")
    ax.text(max(walls), -0.28, "%.0f s" % max(walls), ha="center", fontsize=6, va="top")
    ax.set_ylim(-0.7, 2.3)
    ax.set_xlabel("Wall-clock time per validated edit (s)")
    ax.set_xlim(0, 2600)
    ax.legend(loc="upper right", frameon=False, handlelength=1.0, borderaxespad=0.0, bbox_to_anchor=(1.02, 1.02))
    fig.savefig(out / "fig_cost.pdf"); plt.close(fig)

    # ---- fig_coverage
    b1 = d["b1"]["B1"]
    rows = [("Agent-labelled optimizations", "agent_opt"), ("Subject-only labelled optimizations", "manual_opt"),
            ("All 18 replayed edits", "all18")]
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    y = 0.0; ticks = []; labels = []
    cov = {}
    for name, key in rows:
        for meth, mk, col, lab in (("profile", "o", OI["blue"], "Measured profile"), ("static", "s", OI["verm"], "Static call graph")):
            k, n = b1[key][meth]["k"], b1[key][meth]["n"]
            lo, hi = wilson(k, n)
            ax.errorbar(100 * k / n, y, xerr=[[100 * (k / n - lo)], [100 * (hi - k / n)]], fmt=mk, color=col,
                        ms=4, mfc=col if meth == "profile" else "white", capsize=2, elinewidth=0.9,
                        label=lab if key == "agent_opt" else None)
            ax.text(101.5, y, "%d/%d" % (k, n), va="center", fontsize=6)
            cov["%s/%s" % (key, meth)] = [k, n, 100 * lo, 100 * hi]
            y += 1
        ticks.append(y - 1.5); labels.append(name); y += 0.6
    ax.axhline(y - 0.3, color=OI["grey"], lw=0.6, ls="--")
    ax.text(50, y + 0.55, "replication projects (pending)", ha="center", va="center", fontsize=6.5,
            color=OI["grey"], style="italic")
    ax.plot([0, 100], [y + 0.55] * 2, color=OI["grey"], lw=0.6, ls=(0, (2, 3)), alpha=0.0)
    ticks.append(y + 0.55); labels.append("")
    ax.set_yticks(ticks[:-1]); ax.set_yticklabels(labels[:-1])
    ax.set_ylim(y + 1.3, -0.7)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Edits unreached by the benchmark suite (%, 95% Wilson CI)")
    ax.legend(loc="lower center", frameon=False, bbox_to_anchor=(0.45, 1.0), ncol=2, handletextpad=0.3)
    fd["coverage"] = cov
    fig.savefig(out / "fig_coverage.pdf"); plt.close(fig)

    # ---- fig_slowdowns
    sc = slowdown_classes(d)
    cats = [("unreached", "Not executed by any\nbenchmark (profile reach 0)", OI["grey"]),
            ("executed_undetected", "Executed, not detected", OI["yellow"]),
            ("off_target", "Flagged off target\n(judged false positive)", OI["purple"]),
            ("on_target", "Detected on target", OI["green"])]
    fig, ax = plt.subplots(figsize=(3.4, 1.7))
    fdslow = {}
    for j, (key, lab, col) in enumerate(cats):
        ids = [i for i in range(10) if sc[i]["cat"] == key]
        ax.barh(j, len(ids), color=col, edgecolor="black", linewidth=0.4, height=0.6)
        ax.text(len(ids) + 0.12, j, "#" + ", #".join(str(i) for i in ids), va="center", fontsize=6)
        fdslow[key] = ids
    ax.set_yticks(range(len(cats))); ax.set_yticklabels([c[1] for c in cats])
    ax.set_xlim(0, 10); ax.set_xticks(range(0, 8))
    ax.invert_yaxis()
    ax.set_xlabel("Frozen slowdowns (count, of 10)")
    fd["slowdowns"] = fdslow
    fig.savefig(out / "fig_slowdowns.pdf"); plt.close(fig)

    # ---- fig_power
    per = d["pow"]["exact"]["per_case"]
    xs = ["1.12", "1.2", "1.5", "2.0"]
    xf = [float(x) for x in xs]
    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    first = True
    for k, vals in per.items():
        algo = k.startswith("benchmark_algorithms.")
        if algo:
            continue
        ax.plot(xf, [vals[x] for x in xs], color=OI["sky"], lw=0.5, alpha=0.7, label="20 other A/A cases" if first else None)
        first = False
    first = True
    for k, vals in per.items():
        if k.startswith("benchmark_algorithms."):
            ax.plot(xf, [vals[x] for x in xs], color=OI["verm"], lw=1.0, label="3 benchmark_algorithms cases" if first else None)
            first = False
    ax.plot(xf, [d["pow"]["exact"]["median_all"][x] for x in xs], color="black", lw=1.4, marker="o", ms=3,
            label="Median, all 23 cases")
    ax.axhline(0.8, color=OI["grey"], lw=0.7, ls="--")
    ax.text(2.13, 0.8, "0.8", fontsize=6, va="center", color=OI["grey"])
    ax.set_xticks(xf); ax.set_xticklabels(xs); ax.set_xlim(1.1, 2.18); ax.set_ylim(-0.02, 1.04)
    ax.set_xlabel("True slowdown factor"); ax.set_ylabel("Detection probability")
    ax.legend(loc="lower right", frameon=False, bbox_to_anchor=(1.0, 0.02))
    fd["power"] = {"median_all": d["pow"]["exact"]["median_all"], "median_algorithms": d["pow"]["exact"]["median_algorithms"]}
    fig.savefig(out / "fig_power.pdf"); plt.close(fig)

    # ---- fig_precision
    pv = d["b1"]["precision_v1"]
    order = [("networkx", "networkx"), ("bottleneck", "bottleneck"), ("geopandas", "geopandas"),
             ("pvlib-python", "pvlib-python"), ("pooled", "Pooled")]
    fig, ax = plt.subplots(figsize=(3.4, 1.7))
    for j, (key, lab) in enumerate(order):
        k, n = pv[key]["opt"], pv[key]["qualified"]
        lo, hi = wilson(k, n)
        col = OI["black"] if key == "pooled" else OI["blue"]
        ax.errorbar(100 * k / n, j, xerr=[[100 * (k / n - lo)], [100 * (hi - k / n)]], fmt="D" if key == "pooled" else "o",
                    color=col, ms=4, capsize=2, elinewidth=0.9)
        ax.text(101.5, j, "%d/%d" % (k, n), va="center", fontsize=6)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([o[1] for o in order])
    ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel("Mined commits that are real optimizations (%, 95% Wilson CI)")
    fig.savefig(out / "fig_precision.pdf"); plt.close(fig)



# ----------------------------------------------------------------- main
def main():
    global _MAN
    args = sys.argv[1:]
    regen = "--manifest" in args
    allow = "--allow-mismatch" in args
    if not regen:
        _MAN = load_manifest()
        if not _MAN:
            fail_hard("data-manifest.yaml missing or empty; run with --manifest first")
    d = D()
    vals = compute(d)
    bad = []
    spec_values = {}
    names = set()
    for name, val, kind, anchor, source in SPEC:
        if name in names:
            fail_hard("duplicate macro " + name)
        names.add(name)
        spec_values[name] = val
        if kind == "computed":
            if name not in vals:
                bad.append("%s: kind=computed but make_all.py has no computation (source: %s)" % (name, source))
            elif vals[name] != val:
                bad.append("%s: spec %r != computed %r (source: %s)" % (name, val, vals[name], source))
    # slowdown counts cross-checks for quoted entries that are cheap to verify
    sc = slowdown_classes(d)
    cross = {"SlowDetOnTarget": str(sum(1 for i in sc if sc[i]["cat"] == "on_target")),
             "SlowUnreachedProfile": str(sum(1 for i in sc if sc[i]["reach"] == 0)),
             "SlowMissed": str(sum(1 for i in sc if sc[i]["cat"] in ("unreached", "executed_undetected"))),
             "SlowTwoCases": str(len(sc[2]["on"]))}
    for k, c in cross.items():
        if spec_values.get(k) != c:
            bad.append("%s (quoted): spec %r != cross-check from raw %r" % (k, spec_values.get(k), c))
    fd = {}
    rf = _READ_REL("03-experiment/results/results.md")
    kf = _READ_REL("knowledge-base/findings.md")
    figures(d, fd)
    (PAPER / "generated").mkdir(exist_ok=True)
    write_oracle_table(d)
    (PAPER / "generated" / "figure_data.json").write_text(json.dumps(fd, indent=1, default=str), encoding="utf8")
    if bad:
        print("VALUE DISCREPANCIES (spec vs computed):", file=sys.stderr)
        for b in bad:
            print("  " + b, file=sys.stderr)
        if not allow and not regen:
            print("numbers.tex NOT written. Use --allow-mismatch to write the spec values anyway.", file=sys.stderr)
            sys.exit(1)
    if regen or not bad or allow:
        write_numbers(spec_values)
    if regen:
        write_manifest()
        print("manifest written: %d inputs" % len(_READ))
    else:
        unused = set(_MAN) - set(_READ)
        if unused:
            print("note: manifest lists unread inputs: %s" % sorted(unused))
    print("ok: %d macros, figures in figures/" % len(SPEC))
    if bad:
        sys.exit(1)
    if "--pdf" in args:
        build_pdf()


# Tectonic 0.17.0 in its own conda env (owner-approved 2026-11-22). Override with $TECTONIC.
# Opt-in (--pdf) on purpose: another workstream times benchmarks on this machine,
# so compile only when needed, never in a loop.
TECTONIC_DEFAULT = r"C:\Users\pc\miniconda3\envs\tectonic\Library\bin\tectonic.exe"


def build_pdf():
    import os
    import subprocess
    rc = subprocess.call([sys.executable, str(PAPER / "scripts" / "check.py")])
    if rc != 0:
        fail_hard("check.py failed; PDF not built")
    exe = os.environ.get("TECTONIC", TECTONIC_DEFAULT)
    (PAPER / "build").mkdir(exist_ok=True)
    rc = subprocess.call([exe, "-X", "compile", "main.tex", "--outdir", "build", "--keep-logs"], cwd=str(PAPER))
    if rc != 0:
        fail_hard("tectonic failed (exit %d); see build/main.log" % rc)
    log = (PAPER / "build" / "main.log").read_text(encoding="utf8", errors="replace")
    over = log.count("Overfull \\hbox") + log.count("Overfull \\vbox")
    undef = sum(1 for l in log.splitlines() if "undefined" in l and ("Citation" in l or "Reference" in l))
    print("pdf: build/main.pdf; overfull boxes: %d; undefined citations/references: %d" % (over, undef))
    if over or undef:
        sys.exit(1)


if __name__ == "__main__":
    main()
