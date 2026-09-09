"""Small standard-library tests for the audit harness."""

from __future__ import annotations

import importlib.util
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit.py"
ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("research_audit", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class AuditTests(unittest.TestCase):
    def write_project(self, direction: Path, project: object) -> None:
        (direction / "audit").mkdir(parents=True, exist_ok=True)
        (direction / "audit" / "project.json").write_text(json.dumps(project), encoding="utf-8")

    def write_table(self, direction: Path, filename: str, rows: list[dict[str, str]]) -> None:
        (direction / "audit").mkdir(parents=True, exist_ok=True)
        with (direction / "audit" / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=sorted(AUDIT.CSV_SCHEMAS[filename]))
            writer.writeheader()
            writer.writerows(rows)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8", check=False)

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

    def test_second_finance_package_preserves_legacy_profile(self) -> None:
        findings, summary = AUDIT.audit(ROOT / "research-directions/stock-feedback-calibration")
        self.assertEqual(summary["audit_profile"], "finance")
        self.assertFalse([f for f in findings if f.status == "FAIL"])

    def test_software_package_uses_two_year_plan_and_retains_warnings(self) -> None:
        findings, summary = AUDIT.audit(ROOT / "research-directions/llm-optimization-validation")
        self.assertEqual(summary["audit_profile"], "software_performance")
        self.assertFalse([f for f in findings if f.status == "FAIL"])
        self.assertTrue(any(f.check == "research_plan" and "07-two-year-plan.md" in f.detail for f in findings))
        self.assertTrue(any(f.check == "unresolved_novelty" and f.status == "WARN" for f in findings))
        self.assertFalse(any(f.check == "transaction_costs_required" for f in findings))

    def test_profile_requires_literal_boolean_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            for value in (False, "true", 1, None):
                with self.subTest(value=value):
                    self.write_project(direction, {"audit_profile": "software_performance", "protocol": {"noise_control_required": value}})
                    findings, _ = AUDIT.audit(direction)
                    self.assertTrue(any(f.check == "noise_control_required" and f.status == "FAIL" for f in findings))

    def test_finance_profile_does_not_accept_software_flags(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            self.write_project(direction, {"protocol": dict.fromkeys(AUDIT.PROTOCOL_PROFILES["software_performance"], True)})
            findings, _ = AUDIT.audit(direction)
            self.assertTrue(any(f.check == "transaction_costs_required" and f.status == "FAIL" for f in findings))

    def test_unknown_or_invalid_profile_fails_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            for profile in ("generic", [], None):
                with self.subTest(profile=profile):
                    self.write_project(direction, {"audit_profile": profile})
                    findings, _ = AUDIT.audit(direction)
                    self.assertTrue(any(f.check == "audit_profile" and f.status == "FAIL" for f in findings))

    def test_non_object_json_fails_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            for project in ([], None, "text", 5):
                with self.subTest(project=project):
                    self.write_project(direction, project)
                    findings, _ = AUDIT.audit(direction)
                    self.assertTrue(any(f.check == "project.json" and f.status == "FAIL" for f in findings))

    def test_malformed_json_fails_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            self.write_project(direction, {})
            (direction / "audit/project.json").write_text("{", encoding="utf-8")
            findings, _ = AUDIT.audit(direction)
            self.assertTrue(any(f.check == "project.json" and f.status == "FAIL" for f in findings))

    def test_invalid_csv_is_reported_as_schema_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            self.write_project(direction, {})
            for content in ("claim_id,claim\nC1,text,overflow\n", "claim_id,claim_id\nC1,C2\n", "claim_id,\nC1,text\n", 'claim_id,claim\nC1,"unterminated'):
                with self.subTest(content=content):
                    (direction / "audit/claims.csv").write_text(content, encoding="utf-8")
                    findings, _ = AUDIT.audit(direction)
                    self.assertTrue(any(f.check == "claims.csv" and f.status == "FAIL" for f in findings))

    def test_search_counts_must_be_valid_ordered_integers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            for counts in (("unknown", "1", "1"), ("1", "2", "1"), ("-1", "-1", "-1"), ("1", "", "0")):
                with self.subTest(counts=counts):
                    rows = [dict(search_id=str(i), result_count=counts[0], screened_count=counts[1], included_count=counts[2]) for i in range(3)]
                    self.write_table(direction, "search_log.csv", rows)
                    findings, _ = AUDIT.audit(direction)
                    self.assertTrue(any(f.check == "search_count_values" and f.status == "WARN" for f in findings))
                    self.assertFalse(any(f.check == "reproducible_searches" and f.status == "PASS" for f in findings))

    def test_valid_search_counts_include_zero_result_searches(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            self.write_table(direction, "search_log.csv", [dict(search_id=str(i), result_count="0", screened_count="0", included_count="0") for i in range(3)])
            findings, _ = AUDIT.audit(direction)
            self.assertTrue(any(f.check == "reproducible_searches" and f.status == "PASS" for f in findings))

    def test_initializer_profile_and_overwrite_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp) / "direction with spaces"
            command = [sys.executable, str(SCRIPT.with_name("init_audit.py")), str(direction), "--profile", "software_performance"]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            project = json.loads((direction / "audit/project.json").read_text(encoding="utf-8"))
            self.assertEqual(project["audit_profile"], "software_performance")
            self.assertIs(project["protocol"]["noise_control_required"], False)
            self.assertNotIn("transaction_costs_required", project["protocol"])
            claims = direction / "audit/claims.csv"
            claims.write_text("preserve these records", encoding="utf-8")
            subprocess.run(command, capture_output=True, check=True)
            self.assertEqual(claims.read_text(), "preserve these records")
            subprocess.run(command + ["--force"], capture_output=True, check=True)
            self.assertTrue(claims.read_text().startswith("claim_id,"))

    def test_default_initializer_still_uses_finance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run([sys.executable, str(SCRIPT.with_name("init_audit.py")), temp], capture_output=True, check=True)
            project = json.loads((Path(temp) / "audit/project.json").read_text(encoding="utf-8"))
            self.assertEqual(project["audit_profile"], "finance")
            self.assertIs(project["protocol"]["transaction_costs_required"], False)

    def test_missing_cli_target_is_not_created(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            result = self.run_cli(str(missing))
            self.assertEqual(result.returncode, 2)
            self.assertFalse(missing.exists())
            self.assertNotIn("Traceback", result.stderr)

    def test_file_cli_target_fails_without_modifying_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file"
            path.write_text("keep")
            result = self.run_cli(str(path))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_text(), "keep")
            self.assertNotIn("Traceback", result.stderr)

    def test_no_write_and_strict_exit_status(self) -> None:
        direction = ROOT / "research-directions/llm-optimization-validation"
        outputs = [direction / f"audit/generated-audit-report.{suffix}" for suffix in ("md", "json")]
        before = [p.read_bytes() if p.exists() else None for p in outputs]
        normal = self.run_cli(str(direction), "--no-write")
        strict = self.run_cli(str(direction), "--no-write", "--strict")
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(strict.returncode, 1, strict.stderr)
        self.assertEqual(before, [p.read_bytes() if p.exists() else None for p in outputs])

    def test_writing_report_preserves_source_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            direction = Path(temp)
            self.write_project(direction, {"audit_profile": "software_performance"})
            original = (direction / "audit/project.json").read_bytes()
            result = self.run_cli(str(direction))
            self.assertEqual(result.returncode, 2)
            payload = json.loads((direction / "audit/generated-audit-report.json").read_text())
            self.assertGreater(payload["result_counts"]["FAIL"], 0)
            self.assertEqual(payload["summary"]["audit_profile"], "software_performance")
            self.assertEqual(original, (direction / "audit/project.json").read_bytes())
            self.assertTrue((direction / "audit/generated-audit-report.md").is_file())


if __name__ == "__main__":
    unittest.main()
