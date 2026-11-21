"""Build static simulate inputs for a pure-Python target from the BASE state S_0 (no hindsight).

Usage: python scripts/build_inputs.py <config.toml> <state-dir-at-S0> <inputs-out-dir>
Writes modules.json (A3 name maps, module_functions) and static_reach.json (A5, STARTS-style).
Rules (rules.md §3/§4, W3-new naive baseline):
  module_of_test:  <pkg>/<sub>/tests/test_<name>.py -> <pkg>/<sub>/<name>.py if that file exists,
                   else the package dir's __init__.py-less match by stem anywhere under <pkg>/<sub>/; else None.
  module_of_bench: benchmarks/benchmark_<name>.py -> unique source file with stem <name> (or
                   <name> without a trailing 's'); None if 0 or >1 matches.
"""
import ast, json, sys, tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
from bth import staticgraph  # noqa: E402

cfg = tomllib.loads(Path(sys.argv[1]).read_text())
root = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
pkg = root / "networkx" if (root / "networkx").is_dir() else None
bench_dir = root / cfg["bench"]["dir"]

src_files = sorted(p for p in pkg.rglob("*.py") if "tests" not in p.relative_to(root).parts)
rel = lambda p: p.relative_to(root).as_posix()


def funcs_of(p):
    """FuncIDs of a module (same qualname rule as changed_fns / monitor), incl. <module>."""
    tree = ast.parse(p.read_text(encoding="utf-8"))
    ids = [f"{rel(p)}::<module>"]

    def walk(node, prefix):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                q = f"{prefix}{ch.name}"
                ids.append(f"{rel(p)}::{q}")
                walk(ch, q + ".<locals>.")
            elif isinstance(ch, ast.ClassDef):
                walk(ch, f"{prefix}{ch.name}.")
            else:
                walk(ch, prefix)
    walk(tree, "")
    return sorted(set(ids))


module_functions = {rel(p): funcs_of(p) for p in src_files}
by_stem = {}
for p in src_files:
    by_stem.setdefault(p.stem, []).append(rel(p))


def module_for_test_file(tf: Path):
    name = tf.stem[len("test_"):] if tf.stem.startswith("test_") else None
    if not name:
        return None
    cand = tf.parent.parent / f"{name}.py"
    if cand.exists():
        return rel(cand)
    under = [m for m in by_stem.get(name, []) if m.startswith(rel(tf.parent.parent) + "/")]
    return under[0] if len(under) == 1 else None


# all test node ids come from the S_0 oracle junit/depmap run, keyed by file
d0 = Path(__file__).resolve().parents[1] / "results/raw/networkx/depmap/S0_181f2951.json"
tests = sorted(json.loads(d0.read_text())["deps"])
module_of_test = {}
for t in tests:
    f = root / t.split("::")[0]
    module_of_test[t] = module_for_test_file(f) if f.exists() else None

module_of_bench, static_reach = {}, {}
reach = staticgraph.build(root, ["networkx"], cfg["bench"]["dir"])
for bid, fs in reach.items():
    static_reach[bid] = sorted(fs)
for bf in sorted(bench_dir.glob("benchmark_*.py")):
    name = bf.stem[len("benchmark_"):]
    hits = by_stem.get(name, []) or by_stem.get(name.rstrip("s"), [])
    module_of_bench[bf.stem] = hits[0] if len(hits) == 1 else None

(out / "modules.json").write_text(json.dumps({
    "module_of_test": module_of_test, "module_of_bench_file": module_of_bench,
    "module_functions": module_functions, "native_ext_funcs": {}, "header_ext": {},
    "quarantine": [], "testmon_selection": None}, indent=1))
(out / "static_reach_methods.json").write_text(json.dumps(static_reach, indent=1))
mapped = sum(v is not None for v in module_of_test.values())
print(f"tests {len(tests)}, mapped to a module {mapped}; bench files {len(module_of_bench)}, "
      f"mapped {sum(v is not None for v in module_of_bench.values())}; static_reach keys {len(static_reach)}; "
      f"modules {len(module_functions)}")
print("bench map:", module_of_bench)
