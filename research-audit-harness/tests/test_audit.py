"""Small standard-library tests for the audit harness."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit.py"
SPEC = importlib.util.spec_from_file_location("research_audit", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class AuditTests(unittest.TestCase):
    def test_missing_direction_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            findings, summary = AUDIT.audit(missing)
            self.assertEqual(summary, {})
            self.assertTrue(any(f.status == "FAIL" for f in findings))

    def test_repository_stock_direction_has_no_failures(self) -> None:
        direction = Path(__file__).resolve().parents[2] / "research-directions" / "stock-selective-routing"
        findings, summary = AUDIT.audit(direction)
        self.assertEqual(summary["project_id"], "stock-selective-routing")
        self.assertFalse([f for f in findings if f.status == "FAIL"])
        self.assertTrue([f for f in findings if f.status == "WARN"])


if __name__ == "__main__":
    unittest.main()
