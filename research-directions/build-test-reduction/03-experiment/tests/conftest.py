"""Minimal shared pytest setup: put harness/ on sys.path and register markers."""
import sys
from pathlib import Path

_HARNESS = Path(__file__).resolve().parents[1] / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))


def pytest_configure(config):
    config.addinivalue_line("markers", "wsl: needs gcc/git/WSL; skipped when the tool is missing")
