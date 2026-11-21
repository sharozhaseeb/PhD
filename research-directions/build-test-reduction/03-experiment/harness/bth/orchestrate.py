"""Experiment orchestrator CLI (readiness 2-5; rules W3-new).

    python -m bth.orchestrate [--exp-root DIR] <subcommand> --config C ...

Subcommands (all write ``<exp-root>/results/raw/<repo>/<subcommand>/...`` unless noted; every
output JSON carries ``meta = {repo, state_sha, harness_tree_hash, cmd, python, platform,
started, ended}``; ``repo`` is the config file stem):

  states       --config C --workdir W [--edits F] [--repo PATH] [--out F]
               replay.build_states with check=None; edits default ``edits/<repo>.candidates.json``
               (qualifying entries only); writes ``edits/<repo>.states.json``.
  changes      --config C --workdir W [--states F]
               ChangeSet per applied step -> ``changes/changes.json``.
  oracle-tests --config C --state-dir D --label L [--python EXE] [--junit] [--timeout S]
               serial ``tests.cmd`` + ``--junitxml``; no xdist -> ``oracle-tests/L.json``
               (``--junit`` keeps the raw XML next to it).
  depmap       --config C --state-dir D --label L [-n N] [--python EXE] [--timeout S]
               ``tests.cmd`` + ``-p bth.depmap_plugin`` (PYTHONPATH gets harness/ prepended);
               xdist worker files ``OUT.gwN`` are merged -> ``depmap/L.json``
               (``deps``, ``outcomes``).
  bench        --config C --state-dir D --label L [--filter RE] [--processes N] [--values N]
               [--min-value-time S] [--warmup-values N] [--cpus LIST] [--python EXE]
               -> ``bench/L.json`` (``results`` = benchrun.measure dicts).
  profile      --config C --state-dir D --label L [--filter RE] [--python EXE]
               -> ``profile/L.json`` (``profiles`` {BenchID: [FuncID]}, ``errors``).
  simulate     --config C --inputs DIR --out CSV
               see ``simulate`` below.

Config keys used: ``[tests] cmd`` (first element ``python`` is replaced by --python/sys.executable),
``[bench] dir``, ``[native] sources/headers/build_config/name_regex``,
``[replay] base/src_pathspec``, ``[repo] clone``, optional ``[simulate] arms``.

simulate input files (in --inputs DIR; all JSON; missing optional ones default to empty):
  changes.json     required.  {"steps": [{"functions": [FuncID], "files": [relpath],
                   "module_level_files": [], "native_files": [], "header_edits": [],
                   "build_config_changed": false, "unmapped_native": []}, ...]}  (step t = index+1)
                   -- exactly the output of ``changes`` (extra keys ignored).
  durations.json   required.  {"tests": {TestID: secs}, "benches": {BenchID: secs},
                   "build": {"clean": s, "incremental": s, "none": 0},
                   "overhead": {<arm label>: secs per step}}.  all_tests/all_benches are the sorted keys.
  depmaps.json     {"<k>": {TestID: [FuncID]}}  dependency sets recorded at state S_k (k=0 baseline).
  profiles.json    {"<k>": {BenchID: [FuncID]}}  same, for benchmarks.
  static_reach.json {BenchID: [FuncID]}.
  modules.json     {"module_of_test": {TestID: relpath}, "module_of_bench": {BenchID: relpath},
                   "module_functions": {relpath: [FuncID]}, "native_ext_funcs": {ext: [FuncID]},
                   "header_ext": {header: [ext]}, "quarantine": [TestID],
                   "testmon_selection": {"<t>": [TestID]} | null}.
  faults.json      [{"id", "kind", "step", "visible_from"?, "extra_changed": [FuncID],
                   "kill_tests": [TestID] | {"<step>": [TestID]},
                   "regress_benches": [BenchID] | {"<step>": [BenchID]}}, ...]
Arms: ``[simulate] arms`` list of ``NAME`` or ``NAME:k=v,k=v``; NAME in FULL, INC, TESTMON,
CHANGED_MODULE, STATIC_BENCH, OURS (keys accumulate, profile, T, k, w_header, w_fallback; ``k``
selects the periodic trigger, else score trigger T), PERIODIC (keys inner=<NAME>, k).
Default: FULL, INC, TESTMON, CHANGED_MODULE, STATIC_BENCH, OURS.
Outputs: ``--out`` (per-step: arm, step, decision, cost parts, cumulative), ``<out>.faults.csv``
(per arm x fault) and ``<out>.summary.csv`` (per arm: safety.summarise + total cost).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_EXP_ROOT = HARNESS_DIR.parent
TAIL = 3000


# ------------------------------------------------------------------ shared helpers
def harness_tree_hash() -> str:
    """sha256 over sorted (relative path, sha256(content)) pairs of harness/bth/*.py."""
    h = hashlib.sha256()
    for p in sorted((HARNESS_DIR / "bth").glob("*.py")):
        h.update(f"{p.name}\0{hashlib.sha256(p.read_bytes()).hexdigest()}\n".encode())
    return h.hexdigest()


def load_config(path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def repo_name(config_path) -> str:
    return Path(config_path).stem


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def git_head(cwd) -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(cwd), capture_output=True, text=True)
    except (OSError, ValueError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def make_meta(repo, state_dir, argv, started, python=None) -> dict:
    return {"repo": repo, "state_sha": git_head(state_dir) if state_dir else None,
            "harness_tree_hash": harness_tree_hash(), "cmd": list(argv),
            "python": python or sys.executable, "platform": platform.platform(),
            "started": started, "ended": _now()}


def _write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=False), encoding="utf-8")
    return path


def _out_dir(args, sub) -> Path:
    return Path(args.exp_root) / "results" / "raw" / repo_name(args.config) / sub


def test_command(cfg: dict, python: str) -> list:
    cmd = list(cfg["tests"]["cmd"])
    if cmd and cmd[0] in ("python", "python3"):
        cmd[0] = python
    return cmd


def _run(cmd, cwd, env=None, timeout=None) -> dict:
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=timeout)
        code, out, err = r.returncode, r.stdout, r.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        code, out, err, timed_out = None, exc.stdout or b"", exc.stderr or b"", True
    return {"exit_code": code, "timed_out": timed_out, "wall_s": time.perf_counter() - t0,
            "stdout_tail": out.decode("utf-8", "replace")[-TAIL:],
            "stderr_tail": err.decode("utf-8", "replace")[-TAIL:]}


def _env_with_harness() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(HARNESS_DIR)] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    return env


def native_cfg(cfg: dict):
    from bth.changed_fns import Config
    n = cfg.get("native", {})
    return Config(native_sources=dict(n.get("sources", {})), native_headers=list(n.get("headers", [])),
                  build_config=list(n.get("build_config", [])), native_name_regex=n.get("name_regex"))


def native_prefixes(cfg: dict) -> list:
    return sorted(set(cfg.get("native", {}).get("sources", {}).values()) |
                  set(cfg.get("depmap", {}).get("native_prefixes", [])))


# ------------------------------------------------------------------ states / changes
def cmd_states(args, argv, started):
    from bth import replay
    cfg = load_config(args.config)
    repo = repo_name(args.config)
    edits_path = Path(args.edits) if args.edits else Path(args.exp_root) / "edits" / f"{repo}.candidates.json"
    cands = json.loads(edits_path.read_text(encoding="utf-8"))
    edits = [e for e in cands if e.get("qualifies", True)]
    src = Path(args.repo or os.path.expanduser(cfg["repo"]["clone"]))
    base = cfg["replay"]["base"]
    recs = replay.build_states(src, args.workdir, base, edits, cfg["replay"]["src_pathspec"], None)
    out = Path(args.out) if args.out else Path(args.exp_root) / "edits" / f"{repo}.states.json"
    _write_json(out, {"meta": make_meta(repo, args.workdir, argv, started), "base": base,
                      "workdir": str(args.workdir), "records": recs})
    print(f"states: {sum(r['status'] == 'applied' for r in recs)}/{len(recs)} applied -> {out}")
    return 0


def cmd_changes(args, argv, started):
    from bth.changed_fns import changed_functions
    cfg = load_config(args.config)
    repo = repo_name(args.config)
    sp = Path(args.states) if args.states else Path(args.exp_root) / "edits" / f"{repo}.states.json"
    st = json.loads(sp.read_text(encoding="utf-8"))
    ncfg = native_cfg(cfg)
    prev, steps = st["base"], []
    for rec in st["records"]:
        if rec["status"] != "applied":
            continue
        cs = changed_functions(args.workdir, prev, rec["state_sha"], ncfg)
        steps.append({"step": len(steps) + 1, "orig_sha": rec["orig_sha"], "from": prev,
                      "to": rec["state_sha"],
                      "functions": sorted(cs.functions), "files": sorted(cs.files),
                      "module_level_files": sorted(cs.module_level_files),
                      "native_files": sorted(cs.native_files), "header_edits": sorted(cs.header_edits),
                      "build_config_changed": cs.build_config_changed,
                      "unmapped_native": sorted(cs.unmapped_native)})
        prev = rec["state_sha"]
    out = _out_dir(args, "changes") / "changes.json"
    _write_json(out, {"meta": make_meta(repo, args.workdir, argv, started), "base": st["base"], "steps": steps})
    print(f"changes: {len(steps)} steps -> {out}")
    return 0


# ------------------------------------------------------------------ tests / depmap
def cmd_oracle_tests(args, argv, started):
    from bth import junit
    cfg = load_config(args.config)
    sd = Path(args.state_dir).resolve()
    outd = _out_dir(args, "oracle-tests")
    outd.mkdir(parents=True, exist_ok=True)
    xml = outd / f"{args.label}.junit.xml"
    cmd = test_command(cfg, args.python) + [f"--junitxml={xml}"]
    res = _run(cmd, sd, timeout=args.timeout)
    tests = junit.parse(xml, rootdir=sd) if xml.exists() else {}
    if xml.exists() and not args.junit:
        xml.unlink()
    rec = {"meta": make_meta(repo_name(args.config), sd, argv, started, args.python),
           "label": args.label, "test_cmd": cmd, **res, "tests": tests}
    out = _write_json(outd / f"{args.label}.json", rec)
    print(f"oracle-tests: exit {res['exit_code']}, {len(tests)} tests, {res['wall_s']:.1f}s -> {out}")
    return 0


def merge_depmap_parts(out: Path):
    """Merge `out` and xdist worker parts `out.<worker>` -> (deps, outcomes)."""
    deps, outcomes = {}, {}
    for p in sorted(out.parent.glob(out.name + "*")):
        suffix = p.name[len(out.name):]
        if suffix == "" or (suffix.startswith(".") and not suffix.endswith(".outcomes.json")):
            deps.update(json.loads(p.read_text(encoding="utf-8")))
        elif suffix.endswith(".outcomes.json"):
            outcomes.update(json.loads(p.read_text(encoding="utf-8")))
    return dict(sorted(deps.items())), dict(sorted(outcomes.items()))


def cmd_depmap(args, argv, started):
    cfg = load_config(args.config)
    sd = Path(args.state_dir).resolve()
    outd = _out_dir(args, "depmap")
    parts = outd / f"{args.label}.parts"
    parts.mkdir(parents=True, exist_ok=True)
    for old in parts.iterdir():
        old.unlink()
    plug = parts / "depmap.json"
    cmd = test_command(cfg, args.python) + ["-p", "bth.depmap_plugin", "--bth-depmap-out", str(plug),
                                            "--bth-root", str(sd)]
    for pfx in native_prefixes(cfg):
        cmd += ["--bth-native-prefix", pfx]
    if args.n:
        cmd += ["-n", str(args.n)]
    res = _run(cmd, sd, env=_env_with_harness(), timeout=args.timeout)
    deps, outcomes = merge_depmap_parts(plug)
    for p in parts.iterdir():
        p.unlink()
    parts.rmdir()
    rec = {"meta": make_meta(repo_name(args.config), sd, argv, started, args.python),
           "label": args.label, "test_cmd": cmd, **res, "deps": deps, "outcomes": outcomes}
    out = _write_json(outd / f"{args.label}.json", rec)
    print(f"depmap: exit {res['exit_code']}, {len(deps)} tests, {res['wall_s']:.1f}s -> {out}")
    return 0


# ------------------------------------------------------------------ bench / profile
def _time_cases(args, cfg):
    import re
    from bth import benchrun
    cases = [c for c in benchrun.discover(cfg["bench"]["dir"], args.state_dir, args.python) if c.kind == "time"]
    if args.filter:
        rx = re.compile(args.filter)
        cases = [c for c in cases if rx.search(c.id)]
    return cases


def cmd_bench(args, argv, started):
    from bth import benchrun
    cfg = load_config(args.config)
    cases = _time_cases(args, cfg)
    results = [benchrun.measure(c, args.state_dir, args.python, processes=args.processes, values=args.values,
                                min_value_time=args.min_value_time, warmup_values=args.warmup_values,
                                cpus=args.cpus) for c in cases]
    rec = {"meta": make_meta(repo_name(args.config), args.state_dir, argv, started, args.python),
           "label": args.label, "protocol": {"processes": args.processes, "values": args.values,
                                              "min_value_time": args.min_value_time,
                                              "warmup_values": args.warmup_values, "cpus": args.cpus},
           "results": results}
    out = _write_json(_out_dir(args, "bench") / f"{args.label}.json", rec)
    print(f"bench: {len(results)} cases -> {out}")
    return 0


def cmd_profile(args, argv, started):
    from bth import benchrun
    cfg = load_config(args.config)
    profiles, errors = {}, {}
    for c in _time_cases(args, cfg):
        try:
            profiles[c.id] = sorted(benchrun.profile(c, args.state_dir, args.python, args.state_dir,
                                                     native_prefixes(cfg)))
        except RuntimeError as exc:
            errors[c.id] = str(exc)
    rec = {"meta": make_meta(repo_name(args.config), args.state_dir, argv, started, args.python),
           "label": args.label, "profiles": profiles, "errors": errors}
    out = _write_json(_out_dir(args, "profile") / f"{args.label}.json", rec)
    print(f"profile: {len(profiles)} benchmarks ({len(errors)} errors) -> {out}")
    return 0


# ------------------------------------------------------------------ simulate
ARM_DEFAULT = ["FULL", "INC", "TESTMON", "CHANGED_MODULE", "STATIC_BENCH", "OURS"]


def _val(s: str):
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    for conv in (int, float):
        try:
            return conv(s)
        except ValueError:
            pass
    return s


def parse_arm(spec: str):
    """'NAME[:k=v,...]' -> (label, factory(ctx))."""
    from bth import select as S
    name, _, rest = spec.partition(":")
    kw = {k: _val(v) for k, v in (kv.split("=", 1) for kv in rest.split(",") if kv)}
    simple = {"FULL": S.Full, "INC": S.Inc, "TESTMON": S.Testmon, "CHANGED_MODULE": S.ChangedModule,
              "STATIC_BENCH": S.StaticBench}
    if name in simple:
        return spec, simple[name]
    if name == "OURS":
        k, T = kw.pop("k", None), kw.pop("T", 10)
        trig = ("periodic", k) if k is not None else ("score", T)
        return spec, lambda ctx: S.Ours(ctx, trigger=trig, **kw)
    if name == "PERIODIC":
        inner, k = kw.get("inner", "INC"), kw["k"]
        _, ifac = parse_arm(inner)
        return spec, lambda ctx: S.Periodic(ifac(ctx), k)
    raise ValueError(f"unknown arm {spec!r}")


def _load(d: Path, name, default=None):
    p = d / name
    if not p.exists():
        if default is None:
            raise FileNotFoundError(p)
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _kv_set(d):
    return {k: frozenset(v) for k, v in d.items()}


def _step_dep(maps):
    ms = {int(k): _kv_set(v) for k, v in maps.items()}
    return lambda key, k: ms.get(k, {}).get(key)


def load_sim_inputs(d):
    """Build (Context, steps, durations, faults) from an inputs dir (format in module docstring)."""
    from bth.changed_fns import ChangeSet
    from bth.safety import Fault
    from bth.select import Context
    d = Path(d)
    ch = _load(d, "changes.json")
    ch = ch["steps"] if isinstance(ch, dict) else ch
    steps = [ChangeSet(functions=frozenset(s.get("functions", ())), files=frozenset(s.get("files", ())),
                       module_level_files=frozenset(s.get("module_level_files", ())),
                       native_files=frozenset(s.get("native_files", ())),
                       header_edits=frozenset(s.get("header_edits", ())),
                       build_config_changed=bool(s.get("build_config_changed", False)),
                       unmapped_native=frozenset(s.get("unmapped_native", ()))) for s in ch]
    dur = _load(d, "durations.json")
    mods = _load(d, "modules.json", {})
    tm = mods.get("testmon_selection")
    ctx = Context(
        all_tests=sorted(dur["tests"]), all_benches=sorted(dur.get("benches", {})),
        depmap_at=_step_dep(_load(d, "depmaps.json", {})),
        bench_profile_at=_step_dep(_load(d, "profiles.json", {})),
        static_reach=_kv_set(_load(d, "static_reach.json", {})),
        module_of_test=dict(mods.get("module_of_test", {})), module_of_bench=dict(mods.get("module_of_bench", {})),
        module_functions=_kv_set(mods.get("module_functions", {})),
        native_ext_funcs=_kv_set(mods.get("native_ext_funcs", {})),
        header_ext=_kv_set(mods.get("header_ext", {})),
        quarantine=frozenset(mods.get("quarantine", ())),
        order_dependent=frozenset(mods.get("order_dependent", ())),
        testmon_selection=None if tm is None else {int(k): frozenset(v) for k, v in tm.items()},
        last_step=len(steps))

    def spec(v):
        return {int(k): frozenset(x) for k, x in v.items()} if isinstance(v, dict) else frozenset(v)
    faults = [Fault(id=f["id"], kind=f["kind"], step=int(f["step"]), visible_from=f.get("visible_from"),
                    extra_changed=frozenset(f.get("extra_changed", ())), kill_tests=spec(f.get("kill_tests", [])),
                    regress_benches=spec(f.get("regress_benches", []))) for f in _load(d, "faults.json", [])]
    return ctx, steps, dur, faults


def _write_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def simulate(inputs, out, arms=None):
    """Run every arm over the steps (cost) and every fault (safety). Returns the three CSV paths."""
    from bth import cost, safety
    from bth.select import Outcome
    ctx, steps, dur, faults = load_sim_inputs(inputs)
    build = {"clean": 0.0, "incremental": 0.0, "none": 0.0, **dur.get("build", {})}
    overhead = dur.get("overhead", {})
    out = Path(out)
    step_rows, fault_rows, sum_rows = [], [], []
    for spec in arms or ARM_DEFAULT:
        label, factory = parse_arm(spec)
        arm = factory(ctx)
        st = arm.new_state()
        cum = 0.0
        for t, ch in enumerate(steps, start=1):
            d = arm.decide(t, ch, st)
            c = cost.estimate(d, dur["tests"], dur.get("benches", {}), build, overhead.get(label, 0.0))
            cum += c["total"]
            step_rows.append([label, t, d.build, len(d.tests), len(d.benches), int(d.full_check),
                              ";".join(d.fallback_reasons), c["build"], c["tests"], c["benches"],
                              c["overhead"], c["total"], cum])
            arm.observe(t, d, Outcome(green=True), st)
        dets = []
        for f in faults:
            det = safety.simulate(factory, steps, ctx, f)
            dets.append(det)
            fault_rows.append([label, f.id, f.kind, f.step, f.v, det.step if det.step is not None else "",
                               det.delay if det.delay is not None else "", det.by])
        s = safety.summarise(dets)
        sum_rows.append([label, s["n"], s["k_missed"], s["wilson"][0], s["wilson"][1],
                         "" if s["mean_delay"] is None else s["mean_delay"],
                         "" if s["median_delay"] is None else s["median_delay"],
                         s["by"]["selection"], s["by"]["full_check"], s["by"]["final"], s["by"]["missed"], cum])
    paths = (out, out.with_name(out.name + ".faults.csv"), out.with_name(out.name + ".summary.csv"))
    _write_csv(paths[0], ["arm", "step", "build", "n_tests", "n_benches", "full_check", "fallback_reasons",
                          "build_s", "tests_s", "benches_s", "overhead_s", "total_s", "cumulative_s"], step_rows)
    _write_csv(paths[1], ["arm", "fault_id", "kind", "step", "visible_from", "detected_step", "delay", "by"],
               fault_rows)
    _write_csv(paths[2], ["arm", "n_faults", "k_missed", "wilson_lo", "wilson_hi", "mean_delay", "median_delay",
                          "by_selection", "by_full_check", "by_final", "by_missed", "total_cost_s"], sum_rows)
    return paths


def cmd_simulate(args, argv, started):
    arms = None
    if args.config:
        arms = load_config(args.config).get("simulate", {}).get("arms")
    paths = simulate(args.inputs, args.out, arms)
    print("simulate -> " + ", ".join(str(p) for p in paths))
    return 0


# ------------------------------------------------------------------ CLI
def build_parser():
    ap = argparse.ArgumentParser(prog="bth.orchestrate")
    ap.add_argument("--exp-root", default=str(DEFAULT_EXP_ROOT), help="dir holding results/ and edits/")
    sub = ap.add_subparsers(dest="sub", required=True)

    def add(name, fn, config=True):
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)
        if config:
            p.add_argument("--config", required=True)
        return p

    def state_opts(p):
        p.add_argument("--state-dir", required=True)
        p.add_argument("--label", required=True)
        p.add_argument("--python", default=sys.executable)

    p = add("states", cmd_states)
    p.add_argument("--workdir", required=True)
    p.add_argument("--edits")
    p.add_argument("--repo")
    p.add_argument("--out")
    p = add("changes", cmd_changes)
    p.add_argument("--workdir", required=True)
    p.add_argument("--states")
    p = add("oracle-tests", cmd_oracle_tests)
    state_opts(p)
    p.add_argument("--junit", action="store_true", help="keep the raw junit XML")
    p.add_argument("--timeout", type=float)
    p = add("depmap", cmd_depmap)
    state_opts(p)
    p.add_argument("-n", type=int, default=None, help="pytest-xdist workers")
    p.add_argument("--timeout", type=float)
    p = add("bench", cmd_bench)
    state_opts(p)
    p.add_argument("--filter")
    p.add_argument("--processes", type=int, default=5)
    p.add_argument("--values", type=int, default=3)
    p.add_argument("--min-value-time", type=float, default=0.01)
    p.add_argument("--warmup-values", type=int, default=1)
    p.add_argument("--cpus", default=None)
    p = add("profile", cmd_profile)
    state_opts(p)
    p.add_argument("--filter")
    p = add("simulate", cmd_simulate, config=False)
    p.add_argument("--config", default=None)
    p.add_argument("--inputs", required=True)
    p.add_argument("--out", required=True)
    return ap


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    if getattr(args, "state_dir", None):
        args.state_dir = str(Path(args.state_dir).resolve())
    return args.fn(args, ["bth.orchestrate", *argv], _now())


if __name__ == "__main__":
    raise SystemExit(main())
