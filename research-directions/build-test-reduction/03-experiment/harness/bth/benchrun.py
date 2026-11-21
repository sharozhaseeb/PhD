"""asv-compatible benchmark runner (readiness 5; rules P1, P5, P6, W3-new).

We do not depend on asv; this module owns the timing protocol.  The harness process never
imports target code: discovery, timing and profiling all run in worker subprocesses
(`python -m bth.benchrun _worker ...`) started with ``--python`` and ``PYTHONPATH=<harness>``.

Conventions
* Benchmarks are module functions / class methods named ``time_*`` (timed), ``track_*``,
  ``mem_*``, ``peakmem_*`` (listed, ``kind != "time"``, never timed).
* ``params``/``param_names``/``timeout``/``setup``/``teardown`` are read from the function
  attribute first, then the class attribute.  ``params`` as in asv: a flat list = one
  parameter; a list of lists/tuples = cartesian product.  Setup and the benchmark both
  receive the parameter values positionally.
* Bench modules are imported by file stem with the bench dir (and the state dir) on
  ``sys.path``; BenchID = ``stem.Class.method(p1, p2)`` or ``stem.func`` using ``repr`` of values.
* Every BenchCase is one parameter combination (``param_index`` indexes the product).

CLI: ``python -m bth.benchrun discover|measure|profile|interleave --state DIR --python EXE
--bench-dir REL [--filter REGEX] --out JSON`` (see ``main``).
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

_MARK = "@@BTH@@"
_KINDS = (("time_", "time"), ("track_", "track"), ("peakmem_", "peakmem"), ("mem_", "mem"))
DEFAULT_TIMEOUT = 60.0
HARNESS_DIR = str(Path(__file__).resolve().parents[1])


@dataclass
class BenchCase:
    id: str
    module: str
    cls: str | None
    name: str
    params: list = field(default_factory=list)       # reprs of this combination's values
    param_names: list = field(default_factory=list)
    timeout: float = DEFAULT_TIMEOUT
    kind: str = "time"
    param_index: int = 0
    bench_dir: str = "."

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "BenchCase":
        names = {f for f in BenchCase.__dataclass_fields__}
        return BenchCase(**{k: v for k, v in d.items() if k in names})


# ----------------------------------------------------------------------------- parent side
def _env(extra_path_first: str | None = None) -> dict:
    env = dict(os.environ)
    parts = [HARNESS_DIR] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    env["PYTHONPATH"] = os.pathsep.join(parts)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _worker_cmd(python, op, payload, cpus=None):
    cmd = [str(python), "-m", "bth.benchrun", "_worker", op, json.dumps(payload)]
    if cpus and shutil.which("taskset"):
        cmd = ["taskset", "-c", str(cpus)] + cmd
    return cmd


def _run_worker(python, op, payload, state_dir, timeout, cpus=None) -> dict:
    """Run a worker; returns its JSON result or {"error": ...}. Never raises on worker failure."""
    try:
        r = subprocess.run(_worker_cmd(python, op, payload, cpus), cwd=str(state_dir), env=_env(),
                           stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"timeout after {timeout}s"}
    out = r.stdout.decode("utf-8", "replace")
    for line in reversed(out.splitlines()):
        if line.startswith(_MARK):
            return json.loads(line[len(_MARK):])
    tail = (r.stderr.decode("utf-8", "replace") or out).strip().splitlines()[-5:]
    return {"error": f"worker exit {r.returncode}: " + " | ".join(tail)}


def discover(bench_dir, state_dir=None, python=None, timeout: float = 300.0) -> list:
    """List BenchCases. `bench_dir` is relative to `state_dir` (or absolute)."""
    state_dir = Path(state_dir if state_dir is not None else ".").resolve()
    python = python or sys.executable
    res = _run_worker(python, "discover", {"state": str(state_dir), "bench_dir": str(bench_dir)},
                      state_dir, timeout)
    if "error" in res:
        raise RuntimeError(f"discovery failed: {res['error']}")
    return [BenchCase.from_dict(c) for c in res["cases"]]


def _loadavg():
    try:
        return float(Path("/proc/loadavg").read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def measure(case, state_dir, python, processes=2, values=5, min_value_time=0.01,
            warmup_values=1, cpus=None) -> dict:
    case = case if isinstance(case, BenchCase) else BenchCase.from_dict(case)
    state_dir = Path(state_dir).resolve()
    t0 = time.perf_counter()
    res = {"id": case.id, "samples": [], "number": None, "wall_s": 0.0,
           "loadavg_before": _loadavg(), "loadavg_after": None, "skipped": False, "error": None}
    number = None
    for _ in range(processes):
        payload = {"state": str(state_dir), "case": case.to_dict(), "number": number,
                   "values": values, "warmup": warmup_values, "min_value_time": min_value_time}
        out = _run_worker(python, "measure", payload, state_dir, case.timeout, cpus)
        if out.get("error"):
            res["error"] = out["error"]
            break
        if out.get("skipped"):
            res["skipped"] = True
            break
        number = out["number"]
        res["samples"].extend(out["samples"])
    res["number"] = number
    res["wall_s"] = time.perf_counter() - t0
    res["loadavg_after"] = _loadavg()
    return res


def profile(case, state_dir, python, root=None, native_prefixes=()) -> frozenset:
    """FuncIDs reached by one call of the benchmark (after setup), via bth.monitor.Recorder."""
    case = case if isinstance(case, BenchCase) else BenchCase.from_dict(case)
    state_dir = Path(state_dir).resolve()
    payload = {"state": str(state_dir), "case": case.to_dict(),
               "root": str(Path(root).resolve() if root else state_dir),
               "native_prefixes": list(native_prefixes)}
    out = _run_worker(python, "profile", payload, state_dir, case.timeout)
    if out.get("error"):
        raise RuntimeError(f"profile {case.id}: {out['error']}")
    return frozenset(out["funcs"])


def run_interleaved(cases, states, repeats, **measure_kw) -> list:
    """states: [(label, state_dir, python)]. For each repeat, each case, each state (rotated)."""
    out = []
    n = len(states)
    for r in range(repeats):
        order = states[r % n:] + states[:r % n] if n else []
        for case in cases:
            for label, sd, py in order:
                res = measure(case, sd, py, **measure_kw)
                res.update({"label": label, "repeat": r, "state_dir": str(sd)})
                out.append(res)
    return out


# ----------------------------------------------------------------------------- worker side
def _emit(obj) -> None:
    sys.stdout.write("\n" + _MARK + json.dumps(obj) + "\n")
    sys.stdout.flush()


def _attr(func, owner, name, default=None):
    for o in (func, owner):
        if o is not None and hasattr(o, name):
            return getattr(o, name)
    return default


def _combos(params):
    if not params:
        return [()]
    if not isinstance(params[0], (list, tuple)):
        params = [params]
    return list(itertools.product(*params))


def _kind(name):
    for pfx, kind in _KINDS:
        if name.startswith(pfx):
            return kind
    return None


def _import_module(stem, state, bench_dir):
    """asv semantics: a bench dir with ``__init__.py`` is a package (``<dirname>.<stem>``), imported
    with its parent on sys.path, so intra-suite imports like ``benchmarks.utils`` work (networkx).
    Otherwise the module is imported by stem. BenchIDs stay stem-based either way."""
    bench_dir = Path(bench_dir)
    is_pkg = (bench_dir / "__init__.py").exists()
    for p in ((str(bench_dir.parent),) if is_pkg else (str(bench_dir),)) + (str(state),):
        if p not in sys.path:
            sys.path.insert(0, p)
    import importlib
    return importlib.import_module(f"{bench_dir.name}.{stem}" if is_pkg else stem)


def _bench_dir_abs(state, bench_dir) -> Path:
    p = Path(bench_dir)
    return p if p.is_absolute() else Path(state) / p


def _w_discover(a):
    state, bdir = a["state"], _bench_dir_abs(a["state"], a["bench_dir"])
    cases = []
    for f in sorted(bdir.glob("*.py")):
        if f.name.startswith("_"):
            continue
        stem = f.stem
        mod = _import_module(stem, state, bdir)
        modname = mod.__name__
        items = []
        for name in sorted(vars(mod)):
            obj = getattr(mod, name)
            if callable(obj) and not isinstance(obj, type) and getattr(obj, "__module__", None) == modname \
                    and _kind(name):
                items.append((None, None, name, obj))
            elif isinstance(obj, type) and obj.__module__ == modname:
                for mname in sorted(vars(obj)):
                    m = getattr(obj, mname)
                    if callable(m) and _kind(mname):
                        items.append((name, obj, mname, m))
        for cname, cobj, mname, m in items:
            params = _attr(m, cobj, "params", [])
            pnames = list(_attr(m, cobj, "param_names", []) or [])
            timeout = float(_attr(m, cobj, "timeout", DEFAULT_TIMEOUT))
            base = f"{stem}.{cname}.{mname}" if cname else f"{stem}.{mname}"
            for idx, combo in enumerate(_combos(params)):
                reprs = [repr(v) for v in combo]
                bid = base + ("(" + ", ".join(reprs) + ")" if combo else "")
                cases.append(BenchCase(bid, stem, cname, mname, reprs, pnames, timeout,
                                       _kind(mname), idx, str(a["bench_dir"])).to_dict())
    _emit({"cases": cases})


def _prepare(a):
    """Import, instantiate, setup. Returns (call, teardown) or None if setup skipped."""
    c = a["case"]
    state = a["state"]
    mod = _import_module(c["module"], state, _bench_dir_abs(state, c["bench_dir"]))
    if c["cls"]:
        cobj = getattr(mod, c["cls"])
        inst = cobj()
        fn = getattr(inst, c["name"])
        owner = cobj
        setup = getattr(inst, "setup", None)
        teardown = getattr(inst, "teardown", None)
    else:
        fn, owner = getattr(mod, c["name"]), None
        setup, teardown = getattr(fn, "setup", None), getattr(fn, "teardown", None)
    raw = getattr(fn, "__func__", fn)
    combo = _combos(_attr(raw, owner, "params", []))[c["param_index"]]
    if setup is not None:
        try:
            setup(*combo)
        except NotImplementedError:
            return None
    return (lambda: fn(*combo)), (lambda: teardown(*combo) if teardown else None)


def _w_measure(a):
    import gc
    prep = _prepare(a)
    if prep is None:
        _emit({"skipped": True})
        return
    call, teardown = prep
    pc = time.perf_counter

    def timed(n):
        gc_was = gc.isenabled()
        gc.disable()
        try:
            t = pc()
            for _ in range(n):
                call()
            return pc() - t
        finally:
            if gc_was:
                gc.enable()

    number = a["number"]
    if not number:
        number = 1
        for mult in itertools.cycle((2, 2.5, 2)):         # 1,2,5,10,20,50,...
            if timed(number) >= a["min_value_time"]:
                break
            number = int(round(number * mult))
    for _ in range(a["warmup"]):
        timed(number)
    samples = [timed(number) / number for _ in range(a["values"])]
    teardown()
    _emit({"number": number, "samples": samples, "skipped": False})


def _w_profile(a):
    prep = _prepare(a)
    if prep is None:
        _emit({"funcs": []})
        return
    call, teardown = prep
    from bth.monitor import Recorder
    rec = Recorder(Path(a["root"]), tuple(a["native_prefixes"]))
    rec.start()
    try:
        call()
    finally:
        funcs = rec.stop()
    teardown()
    _emit({"funcs": sorted(funcs)})


def _worker(op, payload):
    try:
        {"discover": _w_discover, "measure": _w_measure, "profile": _w_profile}[op](json.loads(payload))
    except BaseException as exc:  # report, never hang the parent
        _emit({"error": f"{type(exc).__name__}: {exc}"})


# ----------------------------------------------------------------------------- CLI
def _parse_states(items, default_python):
    out = []
    for i, s in enumerate(items):
        m = re.match(r"^([A-Za-z0-9_.-]+)=(.+)$", s)
        label, path = (m.group(1), m.group(2)) if m else (f"s{i}", s)
        out.append((label, path, default_python))
    return out


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "_worker":
        _worker(argv[1], argv[2])
        return 0
    ap = argparse.ArgumentParser(prog="bth.benchrun")
    ap.add_argument("op", choices=["discover", "measure", "profile", "interleave"])
    ap.add_argument("--state", action="append", required=True,
                    help="state dir; for interleave repeat as LABEL=DIR")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--bench-dir", required=True, help="relative to the state dir")
    ap.add_argument("--filter", default=None, help="regex on BenchID")
    ap.add_argument("--out", required=True)
    ap.add_argument("--processes", type=int, default=2)
    ap.add_argument("--values", type=int, default=5)
    ap.add_argument("--min-value-time", type=float, default=0.01)
    ap.add_argument("--warmup-values", type=int, default=1)
    ap.add_argument("--cpus", default=None)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--root", default=None, help="profile: source root for FuncIDs (default state)")
    ap.add_argument("--native-prefix", action="append", default=[])
    ap.add_argument("--include-non-time", action="store_true")
    a = ap.parse_args(argv)

    states = _parse_states(a.state, a.python)
    first = states[0][1]
    cases = discover(a.bench_dir, first, a.python)
    if not a.include_non_time:
        cases = [c for c in cases if c.kind == "time"] if a.op != "discover" else cases
    if a.filter:
        rx = re.compile(a.filter)
        cases = [c for c in cases if rx.search(c.id)]
    mkw = dict(processes=a.processes, values=a.values, min_value_time=a.min_value_time,
               warmup_values=a.warmup_values, cpus=a.cpus)
    if a.op == "discover":
        res = [c.to_dict() for c in cases]
    elif a.op == "measure":
        res = [measure(c, first, a.python, **mkw) for c in cases]
    elif a.op == "profile":
        res = {c.id: sorted(profile(c, first, a.python, a.root, a.native_prefix)) for c in cases}
    else:
        res = run_interleaved(cases, states, a.repeats, **mkw)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"{a.op}: {len(res)} entries -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
