"""Function-level call recorder on PEP 669 ``sys.monitoring`` (CPython >= 3.12).

Rules: F1* (function-granularity dependency map), F2 (native entry points are
visible only through CALL events), F3 (map is re-recorded after each edit),
W3-new (see ``harness-spec.md``).

* ``PY_START`` records ``"<posix relpath>::<co_qualname>"`` for code under
  ``root`` (excluding ``tests``/``benchmarks``/``site-packages`` directories)
  and then returns ``DISABLE``, so each code object costs one callback per
  ``reset()``.
* ``CALL`` (only when ``native_prefixes`` is non-empty) records
  ``"native::<module>.<name>"`` for C callables whose module starts with a
  prefix.  It never returns ``DISABLE``: call sites are polymorphic.
* ``reset()`` clears the recorded set and calls ``restart_events()`` so that
  locations DISABLEd earlier fire again for the next test.
"""
from __future__ import annotations

import os
import sys
import types
from pathlib import Path

_MON = sys.monitoring
_DISABLE = _MON.DISABLE
_NATIVE_TYPES = (
    types.BuiltinFunctionType,  # also bound builtin methods
    types.MethodDescriptorType,
    types.WrapperDescriptorType,
    types.MethodWrapperType,
)
DEFAULT_EXCLUDE_DIRS = ("tests", "benchmarks", "site-packages")


def _acquire_tool_id(name: str) -> int:
    """Prefer PROFILER_ID, else the first free id (0..5)."""
    order = [_MON.PROFILER_ID] + [i for i in range(6) if i != _MON.PROFILER_ID]
    for tid in order:
        try:
            _MON.use_tool_id(tid, name)
            return tid
        except ValueError:
            continue
    raise RuntimeError("no free sys.monitoring tool id")


class Recorder:
    def __init__(self, root, native_prefixes=(), exclude_dirs=DEFAULT_EXCLUDE_DIRS):
        self.root = Path(root)
        self.native_prefixes = tuple(native_prefixes)
        self.exclude_dirs = frozenset(exclude_dirs)
        self.tool_id: int | None = None
        self._seen: set[str] = set()
        self._root_prefix = os.path.normcase(os.path.abspath(self.root)).rstrip("\\/") + os.sep
        self._code_cache: dict[types.CodeType, str | None] = {}
        self._native_cache: dict[tuple, str | None] = {}

    # -- id computation -------------------------------------------------
    def _fid_for_code(self, code: types.CodeType) -> str | None:
        try:
            return self._code_cache[code]
        except KeyError:
            pass
        fid = None
        fn = code.co_filename
        norm = os.path.normcase(fn)
        if norm.startswith(self._root_prefix):
            rel = fn[len(self._root_prefix):].replace("\\", "/")
            if not (set(rel.split("/")[:-1]) & self.exclude_dirs):
                fid = f"{rel}::{code.co_qualname}" if code.co_qualname != "<module>" else f"{rel}::<module>"
        self._code_cache[code] = fid
        return fid

    def _native_id(self, c) -> str | None:
        mod = getattr(c, "__module__", None)
        name = getattr(c, "__name__", None)
        if name is None:
            return None
        if mod is None:
            owner = getattr(c, "__objclass__", None)  # method / slot descriptors
            if owner is not None:
                mod, name = owner.__module__, f"{owner.__qualname__}.{name}"
            else:
                slf = getattr(c, "__self__", None)
                if isinstance(slf, types.ModuleType):
                    mod = slf.__name__
                elif slf is not None:  # bound builtin method of an instance
                    t = type(slf)
                    mod, name = t.__module__, f"{t.__qualname__}.{name}"
        elif getattr(c, "__objclass__", None) is not None:
            owner = c.__objclass__
            name = f"{owner.__qualname__}.{name}"
        if not isinstance(mod, str):
            return None
        for p in self.native_prefixes:
            if mod.startswith(p):
                return f"native::{mod}.{name}"
        return None

    # -- callbacks ------------------------------------------------------
    def _on_py_start(self, code, offset):
        fid = self._fid_for_code(code)
        if fid is not None:
            self._seen.add(fid)
        return _DISABLE

    def _on_call(self, code, offset, callable_, arg0):
        if type(callable_) in _NATIVE_TYPES or isinstance(callable_, _NATIVE_TYPES):
            nid = self._native_id(callable_)
            if nid is not None:
                self._seen.add(nid)
        # never DISABLE: call sites are polymorphic

    # -- control --------------------------------------------------------
    def start(self) -> None:
        if self.tool_id is not None:
            return
        self._seen.clear()
        tid = _acquire_tool_id("bth.monitor")
        self.tool_id = tid
        try:
            ev = _MON.events.PY_START
            _MON.register_callback(tid, _MON.events.PY_START, self._on_py_start)
            if self.native_prefixes:
                _MON.register_callback(tid, _MON.events.CALL, self._on_call)
                ev |= _MON.events.CALL
            _MON.set_events(tid, ev)
            _MON.restart_events()  # locations DISABLEd by an earlier tool must fire again
        except BaseException:
            self._release()
            raise

    def snapshot(self) -> frozenset:
        return frozenset(self._seen)

    def reset(self) -> None:
        self._seen.clear()
        if self.tool_id is not None:
            _MON.restart_events()

    def _release(self) -> None:
        tid, self.tool_id = self.tool_id, None
        if tid is None:
            return
        try:
            _MON.set_events(tid, 0)
            _MON.register_callback(tid, _MON.events.PY_START, None)
            _MON.register_callback(tid, _MON.events.CALL, None)
        finally:
            _MON.free_tool_id(tid)

    def stop(self) -> frozenset:
        result = self.snapshot()
        self._release()
        return result
