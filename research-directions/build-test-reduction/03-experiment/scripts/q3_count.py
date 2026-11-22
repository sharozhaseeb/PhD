"""Q3: B1 replication by static reach (frozen rule: frozen/q3_project_rule.md). No timing; git + ast only.

Usage (WSL): PYTHONPATH=harness python3 scripts/q3_count.py [phase]
  phase "mine"  : apply rules 1-3 to the candidates in order, freeze edit lists (edits/<p>.q3.candidates.json)
  phase "count" : static reach at base, changed functions per edit, counts + Wilson CIs -> results/q3_b1_static.{json,md}
"""
import fnmatch, hashlib, json, re, subprocess, sys
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import mine as M, staticgraph, changed_fns as CF  # noqa: E402
from bth.stats import wilson  # noqa: E402

HOME = Path.home()
REPOS = HOME / "bt-lab/exp/repos"
REGEX = r'(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)'
CANDIDATES = [("geopandas", "geopandas"), ("pvlib-python", "pvlib"), ("xarray", "xarray")]
OUT = exp / "results/q3"; OUT.mkdir(parents=True, exist_ok=True)


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def phase_mine():
    log = {"rule": "frozen/q3_project_rule.md", "candidates": []}
    chosen = []
    for d, pkg in CANDIDATES:
        repo = REPOS / d
        head = git(repo, "rev-parse", "HEAD").strip()
        files = git(repo, "ls-tree", "-r", "--name-only", head).splitlines()
        asv = [f for f in files if f.endswith("asv.conf.json") or f.endswith("asv.conf.jsonc")]
        rec = {"repo": d, "package": pkg, "head": head, "asv_conf": asv}
        if not asv:
            rec["fails"] = "rule 1: no asv.conf.json in repo"; log["candidates"].append(rec); continue
        conf_txt = git(repo, "show", f"{head}:{asv[0]}")
        m = re.search(r'"benchmark_dir"\s*:\s*"([^"]+)"', conf_txt)
        bdir = str((Path(asv[0]).parent / (m.group(1) if m else "benchmarks")).as_posix()).lstrip("./") or "benchmarks"
        rec["bench_dir"] = bdir
        if not any(f.startswith(bdir + "/") and f.endswith(".py") for f in files):
            rec["fails"] = f"rule 1: benchmark dir {bdir} has no .py files"; log["candidates"].append(rec); continue
        src = [f for f in files if f.startswith(pkg + "/")]
        nat = [f for f in src if f.endswith((".c", ".cpp", ".pyx", ".h", ".cc"))]
        rec["native_source_files"] = len(nat); rec["py_source_files"] = sum(f.endswith(".py") for f in src)
        if nat and len(nat) / max(1, len(src)) >= 0.10:
            rec["fails"] = f"rule 2: {len(nat)} native source files of {len(src)}"; log["candidates"].append(rec); continue
        recs = M.mine(repo, regex=REGEX, src_globs=[f"{pkg}/*.py"],
                      exclude_globs=[f"{pkg}/**/tests/**", f"{pkg}/tests/**", f"{pkg}/conftest.py"],
                      max_lines=200, before="2026-11-21", limit=20, first_parent=True, rev=head)
        q = [r for r in recs if r["qualifies"]]
        rec["n_qualifying"] = len(q)
        if len(q) < 10:
            rec["fails"] = f"rule 3: {len(q)} qualifying commits < 10"; log["candidates"].append(rec); continue
        p = exp / f"edits/{d}.q3.candidates.json"
        p.write_text(json.dumps({"repo": d, "package": pkg, "head_at_mining": head, "bench_dir": bdir,
                                 "rule": "frozen/q3_project_rule.md", "records": recs}, indent=1))
        rec["frozen"] = str(p.relative_to(exp)); rec["sha256"] = sha256(p)
        log["candidates"].append(rec); chosen.append(d)
        if len(chosen) == 2:
            break
    log["chosen"] = chosen
    (OUT / "selection.json").write_text(json.dumps(log, indent=1))
    with open(exp / "frozen/FROZEN.md", "a") as f:
        f.write("\n## Q3 edit lists (frozen before any reach was computed)\n")
        for c in log["candidates"]:
            if "sha256" in c:
                f.write(f"- `{c['frozen']}` sha256 `{c['sha256']}` ({c['n_qualifying']} qualifying; head `{c['head'][:12]}`)\n")
    print(json.dumps(log, indent=1))


def reached_any(funcs, reach_union):
    return bool(set(funcs) & reach_union)


def count_python(d):
    meta = json.loads((exp / f"edits/{d}.q3.candidates.json").read_text())
    repo, pkg, bdir = REPOS / d, meta["package"], meta["bench_dir"]
    q = [r for r in meta["records"] if r["qualifies"]]
    base = git(repo, "rev-parse", q[0]["sha"] + "^").strip()
    git(repo, "checkout", "-q", "-f", "--detach", base)
    reach = staticgraph.build(repo, [pkg], bdir)
    union = set().union(*reach.values()) if reach else set()
    rows = []
    for r in q:
        ch = CF.changed_functions(repo, r["sha"] + "^", r["sha"], CF.Config())
        fs = sorted(f for f in ch.functions if not f.endswith("::<module>"))
        rows.append({"sha": r["sha"], "subject": r["subject"], "changed_functions": fs,
                     "reached_functions": sorted(set(fs) & union), "unreached_edit": not (set(fs) & union),
                     "no_function_changed": not fs})
    return {"project": d, "base": base, "n_bench_cases": len(reach), "n_reached_funcs": len(union), "edits": rows}


def count_bottleneck(states_n):
    import tomllib
    cfg = tomllib.loads((exp / "configs/bottleneck.toml").read_text())
    n = cfg.get("native", {})
    ccfg = CF.Config(native_sources=dict(n.get("sources", {})), native_headers=list(n.get("headers", [])),
                     build_config=list(n.get("build_config", [])), native_name_regex=n.get("name_regex"))
    repo = REPOS / "bottleneck"
    st = [s for s in json.loads((exp / "edits/bottleneck.states.json").read_text())["states"] if s["status"] == "applied"]
    base = json.loads((exp / "edits/bottleneck.states.json").read_text())["base"]
    git(repo, "checkout", "-q", "-f", "--detach", base)
    bdir = cfg["bench"]["dir"]
    reach = staticgraph.build(repo, ["bottleneck"], bdir)
    union = set().union(*reach.values()) if reach else set()
    bench_src = "\n".join(p.read_text(errors="replace") for p in (repo / bdir).rglob("*.py"))
    names = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", bench_src))   # identifiers, attributes and string-literal words
    native_names = set()
    for glob in ccfg.native_sources:
        for src in repo.glob(glob):
            spans, _ = CF._c_functions(src.read_text(errors="replace"), ccfg.native_name_regex)
            native_names |= {sp[0] for sp in spans if sp[0]}
    rows = []
    for s in st[:states_n]:
        ch = CF.changed_functions(repo, s["orig_sha"] + "^", s["orig_sha"], ccfg)
        fs = sorted(f for f in ch.functions if not f.endswith("::<module>"))
        py_hit = set(fs) & union
        nat = [f for f in fs if f.startswith("native::")]
        nat_hit = {f for f in nat if f.rsplit(".", 1)[-1] in names}
        # generic template body (python name "NAME", expanded per function by bn_template) -> like a header edit:
        # reached if any native function name of the package is referenced (fix ≈ 12:30, after the first count)
        nat_hit |= {f for f in nat if f.rsplit(".", 1)[-1] == "NAME" and (names & (native_names - {"NAME"}))}
        hdr = sorted(ch.header_edits)
        # header edit -> reached if any native function of an extension it feeds is referenced by name
        # (bottleneck's *.h are included by every extension template, so: any native function name of the package)
        hdr_hit = bool(hdr) and bool(names & native_names)
        rows.append({"sha": s["orig_sha"], "changed_functions": fs, "header_edits": hdr, "py_reached": sorted(py_hit),
                     "native_reached_by_name": sorted(nat_hit), "header_reached": hdr_hit,
                     "unreached_edit": not (py_hit or nat_hit or hdr_hit), "no_function_changed": not fs and not hdr})
    return {"project": f"bottleneck (states 1-{states_n})", "base": base, "n_bench_cases": len(reach),
            "reach": "static Python + W3-new name-based native", "native_names_at_base": sorted(native_names), "edits": rows}


def count_networkx_static():
    ch = json.loads((exp / "results/raw/networkx/changes/changes.json").read_text())["steps"]
    sr = json.loads((exp / "results/sim/networkx/inputs/static_reach_methods.json").read_text())
    union = set().union(*map(set, sr.values()))
    rows = []
    for i, s in enumerate(ch, start=1):
        fs = sorted(f for f in s["functions"] if not f.endswith("::<module>"))
        rows.append({"step": i, "changed_functions": fs, "unreached_edit": not (set(fs) & union), "no_function_changed": not fs})
    return {"project": "networkx (static reach, S0; replayed diffs)", "edits": rows}


def phase_count():
    sel = json.loads((OUT / "selection.json").read_text())
    res = [count_networkx_static()] + [count_python(d) for d in sel["chosen"]] + [count_bottleneck(8), count_bottleneck(13)]
    summary = []
    for r in res:
        n = len(r["edits"]); k = sum(e["unreached_edit"] for e in r["edits"]); z = sum(e["no_function_changed"] for e in r["edits"])
        lo, hi = wilson(k, n)
        summary.append({"project": r["project"], "k_unreached": k, "n": n, "wilson95": [lo, hi], "edits_with_no_function_changed": z})
    out = {"rule": "frozen/q3_project_rule.md", "networkx_profile_reference": {"k_unreached": 12, "n": 18, "wilson95": list(wilson(12, 18)),
                                                                            "source": "results.md finding B1 (S0 profile reach, measured)"},
           "summary": summary, "detail": res}
    (OUT / "q3_b1_static.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({"summary": summary, "ref": out["networkx_profile_reference"]}, indent=1))


if __name__ == "__main__":
    {"mine": phase_mine, "count": phase_count}[sys.argv[1] if len(sys.argv) > 1 else "count"]()
