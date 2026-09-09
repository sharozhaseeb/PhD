#!/usr/bin/env python3
"""Audit a PhD research-direction package using local, evidence-bounded checks."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REQUIRED_DOCS = [
    "README.md",
    "01-layman-explanation.md",
    "02-research-proposal.md",
    "03-literature-novelty-map.md",
    "04-architecture-methodology.md",
    "05-advisor-questions.md",
    "06-evaluation-protocol.md",
]

PLAN_DOCS = ("07-two-year-plan.md", "07-three-year-plan.md")

CSV_SCHEMAS = {
    "claims.csv": {
        "claim_id", "claim", "claim_type", "status", "evidence_required",
        "current_evidence", "owner", "next_action",
    },
    "hypotheses.csv": {
        "hypothesis_id", "hypothesis", "rival_explanation", "discriminating_test",
        "primary_metric", "falsification_condition", "status",
    },
    "nearest_work.csv": {
        "paper_id", "year", "title", "authors", "url", "overlap",
        "claimed_difference", "status", "last_checked",
    },
    "search_log.csv": {
        "search_id", "date", "database_or_source", "query", "filters",
        "result_count", "screened_count", "included_count", "notes",
    },
    "experiments.csv": {
        "experiment_id", "name", "family", "confirmatory", "primary_outcome",
        "data_window", "status", "result_visible", "notes",
    },
    "risks.csv": {
        "risk_id", "category", "risk", "severity", "likelihood",
        "mitigation", "trigger", "status",
    },
}

REQUIRED_PROTOCOL_FLAGS = [
    "point_in_time_data_required",
    "survivorship_aware_universe_required",
    "purge_and_embargo_required",
    "frozen_test_required",
    "prospective_shadow_test_required",
    "transaction_costs_required",
    "factor_attribution_required",
    "equal_information_baselines_required",
    "identifier_date_masking_required_for_llm",
    "negative_result_path_defined",
]

# Existing packages without an explicit profile retain the original finance rules.
PROTOCOL_PROFILES = {
    "finance": REQUIRED_PROTOCOL_FLAGS,
    "software_performance": [
        "valid_workload_domain_defined",
        "original_baseline_comparison_required",
        "behavioral_validation_required",
        "noise_control_required",
        "frozen_test_required",
        "equal_information_baselines_required",
        "full_validation_cost_required",
        "negative_result_path_defined",
    ],
}


@dataclass(frozen=True)
class Finding:
    status: str
    category: str
    check: str
    detail: str


def add(findings: list[Finding], status: str, category: str, check: str, detail: str) -> None:
    findings.append(Finding(status=status, category=category, check=check, detail=detail))


def read_csv(path: Path) -> tuple[set[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        fieldnames = reader.fieldnames or []
        if len(fieldnames) != len(set(fieldnames)) or any(not name.strip() for name in fieldnames):
            raise csv.Error("Column names must be unique and nonempty")
        headers = set(fieldnames)
        rows = []
        for row in reader:
            if None in row:
                raise csv.Error(f"Row {reader.line_num} contains more fields than the header")
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return headers, rows


def missing_values(row: dict[str, str], fields: Iterable[str]) -> list[str]:
    return sorted(field for field in fields if not row.get(field, "").strip())


def audit(direction: Path) -> tuple[list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    audit_dir = direction / "audit"
    tables: dict[str, list[dict[str, str]]] = {}

    if not direction.is_dir():
        add(findings, "FAIL", "structure", "direction_exists", f"Not a directory: {direction}")
        return findings, {}

    for relative in REQUIRED_DOCS:
        path = direction / relative
        if path.is_file() and path.stat().st_size > 100:
            add(findings, "PASS", "structure", relative, "Present and non-trivial")
        elif path.is_file():
            add(findings, "WARN", "structure", relative, "Present but unusually short")
        else:
            add(findings, "FAIL", "structure", relative, "Required document is missing")

    plans = [direction / name for name in PLAN_DOCS if (direction / name).is_file()]
    if not plans:
        add(findings, "FAIL", "structure", "research_plan", f"Missing one of: {', '.join(PLAN_DOCS)}")
    elif any(path.stat().st_size > 100 for path in plans):
        add(findings, "PASS", "structure", "research_plan", f"Present: {', '.join(path.name for path in plans)}")
    else:
        add(findings, "WARN", "structure", "research_plan", "Present but unusually short")

    figures = list((direction / "figures").glob("*.mmd")) if (direction / "figures").is_dir() else []
    if len(figures) >= 3:
        add(findings, "PASS", "structure", "editable_figures", f"Found {len(figures)} Mermaid sources")
    elif figures:
        add(findings, "WARN", "structure", "editable_figures", f"Only {len(figures)} Mermaid source(s)")
    else:
        add(findings, "FAIL", "structure", "editable_figures", "No Mermaid source files found")

    project_path = audit_dir / "project.json"
    project: dict[str, object] = {}
    if not project_path.is_file():
        add(findings, "FAIL", "metadata", "project.json", "Missing project metadata")
    else:
        try:
            parsed = json.loads(project_path.read_text(encoding="utf-8-sig"))
            if not isinstance(parsed, dict):
                raise ValueError("Project metadata must be a JSON object")
            project = parsed
            add(findings, "PASS", "metadata", "project.json", "Valid JSON")
        except (OSError, ValueError) as exc:
            add(findings, "FAIL", "metadata", "project.json", f"Invalid JSON: {exc}")

    for filename, schema in CSV_SCHEMAS.items():
        path = audit_dir / filename
        if not path.is_file():
            add(findings, "FAIL", "schema", filename, "Required audit table is missing")
            continue
        try:
            headers, rows = read_csv(path)
        except (OSError, UnicodeError, csv.Error) as exc:
            add(findings, "FAIL", "schema", filename, f"Could not read CSV: {exc}")
            continue
        absent = sorted(schema - headers)
        if absent:
            add(findings, "FAIL", "schema", filename, f"Missing columns: {', '.join(absent)}")
        elif not rows:
            add(findings, "WARN", "schema", filename, "Valid columns but no records")
        else:
            add(findings, "PASS", "schema", filename, f"Valid schema with {len(rows)} record(s)")
            tables[filename] = rows

    protocol = project.get("protocol", {}) if isinstance(project, dict) else {}
    if not isinstance(protocol, dict):
        protocol = {}
    profile = project.get("audit_profile", "finance")
    if not isinstance(profile, str) or profile not in PROTOCOL_PROFILES:
        add(findings, "FAIL", "metadata", "audit_profile", f"Unknown profile: {profile!r}; choose {', '.join(PROTOCOL_PROFILES)}")
        flags = []
    else:
        label = profile if "audit_profile" in project else "finance (legacy default)"
        add(findings, "PASS", "metadata", "audit_profile", f"Using {label}")
        flags = PROTOCOL_PROFILES[profile]
    for flag in flags:
        if protocol.get(flag) is True:
            add(findings, "PASS", "protocol", flag, "Explicitly required")
        else:
            add(findings, "FAIL", "protocol", flag, "Must be explicitly set to true")

    novelty_status = str(project.get("novelty_status", ""))
    if novelty_status in {"candidate_not_established", "unresolved", "under_review"}:
        add(findings, "PASS", "claims", "novelty_language", f"Appropriately bounded: {novelty_status}")
    else:
        add(findings, "WARN", "claims", "novelty_language", "Novelty should remain unresolved until systematic search and expert review")

    claims = tables.get("claims.csv", [])
    unsupported = [r for r in claims if r.get("status", "").lower() in {"unsupported", "claimed_without_evidence"}]
    unresolved_novelty = [r for r in claims if r.get("claim_type", "").lower() == "novelty" and r.get("status", "").lower() != "established"]
    if unsupported:
        add(findings, "WARN", "claims", "unsupported_claims", f"{len(unsupported)} unsupported claim(s) require action")
    else:
        add(findings, "PASS", "claims", "unsupported_claims", "No rows use unsupported-status labels; evidence itself is not verified")
    if unresolved_novelty:
        add(findings, "WARN", "claims", "unresolved_novelty", f"{len(unresolved_novelty)} novelty claim(s) remain unresolved, as expected at this stage")

    hypotheses = tables.get("hypotheses.csv", [])
    weak_hypotheses = []
    required_h = {"rival_explanation", "discriminating_test", "primary_metric", "falsification_condition"}
    for row in hypotheses:
        if missing_values(row, required_h):
            weak_hypotheses.append(row.get("hypothesis_id", "unknown"))
    if weak_hypotheses:
        add(findings, "FAIL", "hypotheses", "falsification_ready", f"Incomplete: {', '.join(weak_hypotheses)}")
    elif hypotheses:
        add(findings, "PASS", "hypotheses", "falsification_ready", "Every hypothesis has a rival, test, metric, and falsification condition")

    nearest = tables.get("nearest_work.csv", [])
    if len(nearest) >= 8:
        add(findings, "PASS", "novelty", "nearest_work_depth", f"{len(nearest)} closest works recorded")
    elif nearest:
        add(findings, "WARN", "novelty", "nearest_work_depth", f"Only {len(nearest)} closest works recorded")
    critical_overlap = [r for r in nearest if "critical" in r.get("status", "").lower()]
    if critical_overlap:
        add(findings, "WARN", "novelty", "critical_overlap", f"{len(critical_overlap)} critical overlap record(s); contribution wording requires human review")

    searches = tables.get("search_log.csv", [])
    complete_searches = []
    invalid_searches = []
    for row in searches:
        values = [row.get(field, "") for field in ("result_count", "screened_count", "included_count")]
        if not any(values):
            continue
        try:
            result_count, screened_count, included_count = map(int, values)
            if not 0 <= included_count <= screened_count <= result_count:
                raise ValueError("Counts must be nonnegative and ordered")
        except ValueError:
            invalid_searches.append(row.get("search_id", "unknown"))
        else:
            complete_searches.append(row)
    if invalid_searches:
        add(findings, "WARN", "novelty", "search_count_values", f"Incomplete or invalid counts: {', '.join(invalid_searches)}")
    pending_searches = [r for r in searches if "pending" in (r.get("database_or_source", "") + r.get("notes", "")).lower()]
    if len(complete_searches) >= 3:
        add(findings, "PASS", "novelty", "reproducible_searches", f"{len(complete_searches)} searches have complete counts")
    else:
        add(findings, "WARN", "novelty", "reproducible_searches", "Fewer than three searches record result, screened, and included counts")
    if pending_searches:
        add(findings, "WARN", "novelty", "pending_searches", f"{len(pending_searches)} search record(s) remain pending")

    experiments = tables.get("experiments.csv", [])
    families = {r.get("family", "").lower() for r in experiments}
    required_families = {"baseline", "proposed", "ablation", "forward_test"}
    absent_families = sorted(required_families - families)
    if absent_families:
        add(findings, "FAIL", "experiments", "experiment_families", f"Missing: {', '.join(absent_families)}")
    else:
        add(findings, "PASS", "experiments", "experiment_families", "Baselines, proposed method, ablations, and forward test are registered")
    visible_confirmatory = [r for r in experiments if r.get("confirmatory", "").lower() == "true" and r.get("result_visible", "").lower() == "true"]
    if visible_confirmatory:
        add(findings, "WARN", "experiments", "confirmatory_result_visibility", f"{len(visible_confirmatory)} confirmatory experiment(s) already expose results")
    else:
        add(findings, "PASS", "experiments", "confirmatory_result_visibility", "No registered confirmatory result is marked visible")

    risks = tables.get("risks.csv", [])
    open_critical = [r for r in risks if r.get("severity", "").lower() == "critical" and r.get("status", "").lower() not in {"closed", "mitigated", "accepted"}]
    if open_critical:
        add(findings, "WARN", "risks", "open_critical_risks", f"{len(open_critical)} critical risk(s) remain open")
    elif risks:
        add(findings, "PASS", "risks", "open_critical_risks", "No unmitigated critical risks")

    summary = {
        "project_id": project.get("project_id", direction.name),
        "title": project.get("title", direction.name),
        "stage": project.get("stage", "unknown"),
        "novelty_status": project.get("novelty_status", "unknown"),
        "audit_profile": profile,
        "counts": {
            "claims": len(claims),
            "hypotheses": len(hypotheses),
            "nearest_work": len(nearest),
            "searches": len(searches),
            "experiments": len(experiments),
            "risks": len(risks),
            "open_critical_risks": len(open_critical),
        },
    }
    return findings, summary


def render_markdown(direction: Path, findings: list[Finding], summary: dict[str, object]) -> str:
    counts = {status: sum(f.status == status for f in findings) for status in ("PASS", "WARN", "FAIL")}
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        "# Generated Research Audit Report",
        "",
        f"- Direction: `{direction}`",
        f"- Generated: {now}",
        f"- Result: {counts['PASS']} pass, {counts['WARN']} warning, {counts['FAIL']} fail",
        "- Meaning: structural audit only; not scientific or advisor approval",
        "",
        "## Project summary",
        "",
        f"- Title: {summary.get('title', 'unknown')}",
        f"- Stage: {summary.get('stage', 'unknown')}",
        f"- Novelty status: {summary.get('novelty_status', 'unknown')}",
        f"- Audit profile: {summary.get('audit_profile', 'unknown')}",
        "",
        "## Findings",
        "",
        "| Status | Category | Check | Detail |",
        "|---|---|---|---|",
    ]
    for finding in findings:
        detail = finding.detail.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {finding.status} | {finding.category} | `{finding.check}` | {detail} |")
    lines.extend([
        "",
        "## Human decisions still required",
        "",
        "Warnings are intentionally retained. Novelty, domain-specific statistical validity, data licensing, and proposal approval require documented human review.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("direction", type=Path, help="Path to a research direction")
    parser.add_argument("--no-write", action="store_true", help="Print report without writing generated files")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when warnings exist")
    args = parser.parse_args()

    direction = args.direction.resolve()
    findings, summary = audit(direction)
    report = render_markdown(direction, findings, summary)
    counts = {status: sum(f.status == status for f in findings) for status in ("PASS", "WARN", "FAIL")}

    if args.no_write or not direction.is_dir():
        print(report)
    else:
        audit_dir = direction / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        md_path = audit_dir / "generated-audit-report.md"
        json_path = audit_dir / "generated-audit-report.json"
        md_path.write_text(report, encoding="utf-8")
        payload = {
            "direction": str(direction),
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "summary": summary,
            "result_counts": counts,
            "findings": [asdict(f) for f in findings],
        }
        json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {md_path}")
        print(f"Wrote {json_path}")
        print(f"Result: {counts['PASS']} pass, {counts['WARN']} warning, {counts['FAIL']} fail")

    if counts["FAIL"]:
        return 2
    if args.strict and counts["WARN"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

