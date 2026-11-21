"""Static import/call graph for benchmark reachability (arm A5 STATIC-BENCH).

Rules: B1/B2 (incremental build), F1, W3-new "static benchmark RTS"
(STARTS-style class/module-level dependency analysis applied to benchmarks).
Purely static: ``ast`` only, nothing is imported or executed.

``build(root, package_dirs, bench_dir)`` returns ``{BenchID: frozenset[FuncID]}``
where BenchID is ``"<bench module>.<Class>.<method>"`` or
``"<bench module>.<function>"`` (module path relative to ``bench_dir``) and
FuncIDs are ``"<posix relpath from root>::<qualname>"`` or ``...::<module>``.

Resolution (superset by design):
* imports (absolute, relative, ``from x import y`` where y is a submodule or a
  symbol, re-exports through ``__init__`` incl. ``from .x import *`` honouring a
  literal ``__all__``);
* calls/references to imported or locally defined functions, ``self.m()`` /
  ``cls.m()`` resolved through the class and its in-package bases,
  ``ClassName()`` -> ``__init__``/``__new__``, ``v = Cls(); v.m()``;
* an unresolvable call on an imported package module/symbol, or
  ``getattr(<module>, name)(...)``, adds edges to *every* function of that module;
* a function gets edges to its nested functions; module-level code is a node
  (``::<module>``) and every module in the import closure of a reached module
  is reached (import-time code runs).
Known gaps: subclass overrides reached via ``self.m()``, dynamic dispatch on
values of unknown type, ``importlib``/``exec``.
"""
from __future__ import annotations

import ast
from pathlib import Path

BENCH_PREFIXES = ("time_", "timeraw_", "mem_", "peakmem_", "track_")
BENCH_SETUP = ("setup", "setup_cache", "teardown")


class _Mod:
    def __init__(self, dotted, relpath, is_pkg, tree, is_bench):
        self.dotted, self.relpath, self.is_pkg, self.tree, self.is_bench = dotted, relpath, is_pkg, tree, is_bench
        self.funcs: dict[str, tuple] = {}  # qualname -> (node, enclosing class qualname | None)
        self.classes: dict[str, ast.ClassDef] = {}  # qualname -> node
        self.top: dict[str, tuple] = {}  # name -> ("func", qual) | ("class", qual)
        self.bindings: dict[str, tuple] = {}  # name -> ("module", dotted) | ("symbol", dotted, name)
        self.stars: list[str] = []
        self.all_names: set[str] | None = None
        self.imports: set[str] = set()  # dotted names of imported modules (incl. parents), pre-closure

    def fid(self, qual):
        return f"{self.relpath}::{qual}"


class _Graph:
    def __init__(self):
        self.mods: dict[str, _Mod] = {}
        self.edges: dict[str, set[str]] = {}
        self.fid_mod: dict[str, _Mod] = {}

    # -- loading --------------------------------------------------------
    def load(self, base: Path, root: Path, files, bench: bool, prefix: str):
        for f in files:
            rel_to_base = f.relative_to(base)
            parts = list(rel_to_base.with_suffix("").parts)
            is_pkg = parts[-1] == "__init__"
            if is_pkg:
                parts = parts[:-1]
            dotted = ".".join(([prefix] if prefix else []) + parts)
            if not dotted or (dotted in self.mods and bench):
                continue
            try:
                tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            except (SyntaxError, UnicodeDecodeError, ValueError):
                continue
            rel = f.relative_to(root).as_posix()
            self.mods[dotted] = _Mod(dotted, rel, is_pkg, tree, bench)

    # -- per-module indexing -------------------------------------------
    def index(self, m: _Mod):
        def walk(body, prefix, cls):
            for n in body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    q = prefix + n.name
                    m.funcs[q] = (n, cls)
                    if not prefix:
                        m.top[n.name] = ("func", q)
                    walk(n.body, q + ".<locals>.", None)
                elif isinstance(n, ast.ClassDef):
                    q = prefix + n.name
                    m.classes[q] = n
                    if not prefix:
                        m.top[n.name] = ("class", q)
                    walk(n.body, q + ".", q)
                else:
                    for fld in ("body", "orelse", "finalbody", "handlers"):
                        sub = getattr(n, fld, None)
                        if isinstance(sub, list) and sub and isinstance(sub[0], ast.stmt):
                            walk(sub, prefix, cls)
                        elif fld == "handlers" and isinstance(sub, list):
                            for h in sub:
                                walk(h.body, prefix, cls)

        walk(m.tree.body, "", None)
        for n in ast.walk(m.tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    self._bind_import(m, a)
            elif isinstance(n, ast.ImportFrom):
                self._bind_from(m, n)
        for n in m.tree.body:
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in n.targets):
                try:
                    v = ast.literal_eval(n.value)
                    if isinstance(v, (list, tuple)):
                        m.all_names = {x for x in v if isinstance(x, str)}
                except ValueError:
                    pass

    def _add_import_closure_edges(self, m, dotted):
        parts = dotted.split(".")
        for i in range(1, len(parts) + 1):
            d = ".".join(parts[:i])
            if d in self.mods:
                m.imports.add(d)

    def _bind_import(self, m, a):
        if a.asname:
            if a.name in self.mods:
                m.bindings[a.asname] = ("module", a.name)
        else:
            top = a.name.split(".")[0]
            if top in self.mods:
                m.bindings[top] = ("module", top)
        self._add_import_closure_edges(m, a.name)

    def _bind_from(self, m, n):
        if n.level:
            pkg = m.dotted if m.is_pkg else m.dotted.rpartition(".")[0]
            parts = pkg.split(".") if pkg else []
            drop = n.level - 1
            if drop > len(parts):
                return
            parts = parts[: len(parts) - drop]
            base = ".".join(parts + ([n.module] if n.module else []))
        else:
            base = n.module or ""
        if base not in self.mods:
            return
        self._add_import_closure_edges(m, base)
        for a in n.names:
            if a.name == "*":
                m.stars.append(base)
                continue
            sub = f"{base}.{a.name}"
            if sub in self.mods:
                m.bindings[a.asname or a.name] = ("module", sub)
                self._add_import_closure_edges(m, sub)
            else:
                m.bindings[a.asname or a.name] = ("symbol", base, a.name)

    # -- symbol resolution ---------------------------------------------
    def resolve_symbol(self, mod, name, seen=None):
        seen = seen or set()
        if (mod, name) in seen or mod not in self.mods:
            return None
        seen.add((mod, name))
        m = self.mods[mod]
        t = m.top.get(name)
        if t:
            return ("class", mod, t[1]) if t[0] == "class" else ("func", (m.fid(t[1]),))
        b = m.bindings.get(name)
        if b:
            if b[0] == "module":
                return ("module", b[1])
            r = self.resolve_symbol(b[1], b[2], seen)
            return r if r else ("unres", b[1])
        if f"{mod}.{name}" in self.mods:
            return ("module", f"{mod}.{name}")
        for s in m.stars:
            tm = self.mods.get(s)
            if tm is not None and tm.all_names is not None and name not in tm.all_names:
                continue
            r = self.resolve_symbol(s, name, seen)
            if r:
                return r
        return None

    def method_lookup(self, mod, cls_qual, attr, seen=None):
        seen = seen or set()
        if (mod, cls_qual) in seen:
            return ()
        seen.add((mod, cls_qual))
        m = self.mods[mod]
        q = f"{cls_qual}.{attr}"
        if q in m.funcs:
            return (m.fid(q),)
        node = m.classes.get(cls_qual)
        out = ()
        if node is not None:
            for b in node.bases:
                r = self.resolve_expr(b, m, {}, None)
                if r and r[0] == "class":
                    out = self.method_lookup(r[1], r[2], attr, seen)
                    if out:
                        return out
        return out

    # -- expression resolution -----------------------------------------
    def resolve_expr(self, e, m, local, self_ctx):
        """-> ("module", d) | ("func", (fids)) | ("class", mod, q) | ("inst", mod, q) | ("unres", mod) | None"""
        if isinstance(e, ast.Name):
            if e.id in local:
                return local[e.id]
            if self_ctx and e.id == self_ctx[0]:
                return ("inst", m.dotted, self_ctx[1])
            t = m.top.get(e.id)
            if t:
                return ("class", m.dotted, t[1]) if t[0] == "class" else ("func", (m.fid(t[1]),))
            b = m.bindings.get(e.id)
            if b:
                if b[0] == "module":
                    return ("module", b[1])
                r = self.resolve_symbol(b[1], b[2])
                return r if r else ("unres", b[1])
            for s in m.stars:
                r = self.resolve_symbol(s, e.id)
                if r:
                    return r
            return None
        if isinstance(e, ast.Attribute):
            base = self.resolve_expr(e.value, m, local, self_ctx)
            if base is None:
                return None
            k = base[0]
            if k == "module":
                sub = f"{base[1]}.{e.attr}"
                if sub in self.mods:
                    return ("module", sub)
                r = self.resolve_symbol(base[1], e.attr)
                return r if r else ("unres", base[1])
            if k == "unres":
                return base
            if k in ("class", "inst"):
                fids = self.method_lookup(base[1], base[2], e.attr)
                return ("func", fids) if fids else None
            return None
        if isinstance(e, ast.Call):
            f = e.func
            if isinstance(f, ast.Name) and f.id == "getattr" and e.args:
                base = self.resolve_expr(e.args[0], m, local, self_ctx)
                if base and base[0] == "module":
                    return ("unres", base[1])
                return None
            r = self.resolve_expr(f, m, local, self_ctx)
            if r and r[0] == "class":
                return ("inst", r[1], r[2])
            return None
        return None

    # -- edge extraction -----------------------------------------------
    def _all_funcs_of(self, mod):
        mm = self.mods[mod]
        return {mm.fid(q) for q in mm.funcs}

    def _ctor_fids(self, mod, cls):
        out = set()
        for nm in ("__init__", "__new__", "__post_init__"):
            out.update(self.method_lookup(mod, cls, nm))
        return out

    def extract(self, m: _Mod, qual, node, cls):
        src = m.fid(qual)
        edges = self.edges.setdefault(src, set())
        self.fid_mod[src] = m
        self_ctx = None
        if node is not None and cls and node.args.args:
            self_ctx = (node.args.args[0].arg, cls)
        local: dict = {}
        cstack: list[str] = []
        g = self

        class V(ast.NodeVisitor):
            def visit_FunctionDef(self, n):
                for d in n.decorator_list:
                    self.visit(d)
                for d in n.args.defaults + [x for x in n.args.kw_defaults if x]:
                    self.visit(d)
                if node is not None:  # nested def: the enclosing function links to it
                    inner = f"{qual}.<locals>." + "".join(c + "." for c in cstack) + n.name
                    if inner in m.funcs:
                        edges.add(m.fid(inner))

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_ClassDef(self, n):
                for d in n.decorator_list + n.bases:
                    self.visit(d)
                cstack.append(n.name)
                for s in n.body:
                    self.visit(s)
                cstack.pop()

            def _use(self, r, call):
                if not r:
                    return
                if r[0] == "func":
                    edges.update(r[1])
                elif r[0] == "class" and call:
                    edges.update(g._ctor_fids(r[1], r[2]))
                elif r[0] == "unres" and call:
                    edges.update(g._all_funcs_of(r[1]))

            def visit_Call(self, n):
                self._use(g.resolve_expr(n.func, m, local, self_ctx), True)
                f = n.func
                if isinstance(f, ast.Call) and isinstance(f.func, ast.Name) and f.func.id == "getattr" and f.args:
                    b = g.resolve_expr(f.args[0], m, local, self_ctx)
                    if b and b[0] == "module":
                        edges.update(g._all_funcs_of(b[1]))
                self.generic_visit(n)

            def visit_Attribute(self, n):
                self._use(g.resolve_expr(n, m, local, self_ctx), False)
                self.generic_visit(n)

            def visit_Name(self, n):
                if isinstance(n.ctx, ast.Load):
                    self._use(g.resolve_expr(n, m, local, self_ctx), False)

            def visit_Assign(self, n):
                self.visit(n.value)
                v = n.value
                if isinstance(v, ast.Call):
                    r = g.resolve_expr(v, m, local, self_ctx)
                    if r and r[0] == "inst":
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                local[t.id] = r
                for t in n.targets:
                    self.visit(t)

        body = m.tree.body if node is None else node.body
        v = V()
        for st in body:
            v.visit(st)


def build(root, package_dirs, bench_dir):
    root = Path(root).resolve()
    g = _Graph()
    for pd in package_dirs:
        pdp = Path(pd)
        pdp = (pdp if pdp.is_absolute() else root / pdp).resolve()
        g.load(pdp.parent, root, sorted(pdp.rglob("*.py")), False, "")
    bdir = None
    if bench_dir is not None:
        bdir = Path(bench_dir)
        bdir = (bdir if bdir.is_absolute() else root / bdir).resolve()
        g.load(bdir, root, sorted(bdir.rglob("*.py")), True, "")
    for m in g.mods.values():
        g.index(m)
    for m in g.mods.values():
        g.extract(m, "<module>", None, None)
        for q, (node, cls) in m.funcs.items():
            g.extract(m, q, node, cls)
    closure_cache: dict[str, frozenset] = {}

    def closure(d):
        if d in closure_cache:
            return closure_cache[d]
        seen, stack = set(), [d]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(g.mods[x].imports - seen)
            parts = x.split(".")
            for i in range(1, len(parts)):
                stack.append(".".join(parts[:i])) if ".".join(parts[:i]) in g.mods else None
        closure_cache[d] = frozenset(seen)
        return closure_cache[d]

    def reach(starts, start_mod):
        out, mods_done, stack = set(), set(), list(starts)

        def add_mod(d):
            for c in closure(d):
                if c not in mods_done:
                    mods_done.add(c)
                    stack.append(g.mods[c].fid("<module>"))

        add_mod(start_mod)
        while stack:
            f = stack.pop()
            if f in out:
                continue
            out.add(f)
            fm = g.fid_mod.get(f)
            if fm is not None:
                add_mod(fm.dotted)
            stack.extend(g.edges.get(f, ()) - out)
        return frozenset(f for f in out if not g.fid_mod[f].is_bench) if out else frozenset()

    result: dict[str, frozenset] = {}
    for m in sorted((x for x in g.mods.values() if x.is_bench), key=lambda x: x.relpath):
        modname = m.dotted
        for q, (node, cls) in sorted(m.funcs.items()):
            name = q.rsplit(".", 1)[-1]
            if "<locals>" in q or not name.startswith(BENCH_PREFIXES):
                continue
            starts = [m.fid(q)]
            if cls is not None:
                for s in BENCH_SETUP:
                    starts.extend(g.method_lookup(m.dotted, cls, s))
            result[f"{modname}.{q}"] = reach(starts, m.dotted)
    return result
