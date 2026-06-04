#!/usr/bin/env python3
"""Validate SDD Delivery v2 artifact completeness and gate readiness."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FILES = [
    "00-prd.md",
    "01-spec.md",
    "02-spec-review.md",
    "03-requirement-trace.md",
    "04-tech-solution.md",
    "05-solution-review.md",
    "06-implementation-tasks.md",
    "07-implementation-log.md",
    "08-unit-test-plan.md",
    "09-unit-test-report.md",
    "10-delivery-review.md",
    "11-checkpoint.json",
    "12-observability.md",
    "events.jsonl",
]

REQUIRED_CHECKPOINT_FIELDS = [
    "schema_version",
    "feature",
    "goal",
    "current_phase",
    "active_task",
    "gate_status",
    "completed_tasks",
    "pending_tasks",
    "decisions",
    "repo_facts",
    "changed_files",
    "tests_run",
    "metrics",
    "risks",
    "blockers",
    "next_action",
    "updated_at",
]

REQUIRED_GATES = ["spec_review", "solution_review", "unit_test", "delivery_review"]


def non_empty(path: Path) -> bool:
    return path.exists() and bool(path.read_text(encoding="utf-8-sig").strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SDD Delivery v2 artifacts.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--strict", action="store_true", help="Fail if gates are not passed")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    issues, warnings, status = [], [], {}

    for name in REQUIRED_FILES:
        path = folder / name
        if not path.exists():
            issues.append(f"missing file: {name}")
            status[name] = "missing"
        elif name != "events.jsonl" and not non_empty(path):
            issues.append(f"empty file: {name}")
            status[name] = "empty"
        else:
            status[name] = "ok"

    checkpoint_path = folder / "11-checkpoint.json"
    checkpoint = {}
    if checkpoint_path.exists():
        try:
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8-sig"))
            for field in REQUIRED_CHECKPOINT_FIELDS:
                if field not in checkpoint:
                    issues.append(f"checkpoint missing field: {field}")
            gates = checkpoint.get("gate_status", {})
            for gate in REQUIRED_GATES:
                if gate not in gates:
                    issues.append(f"checkpoint missing gate: {gate}")
                elif gates.get(gate) != "passed":
                    msg = f"gate not passed: {gate}={gates.get(gate)}"
                    (issues if args.strict else warnings).append(msg)
        except json.JSONDecodeError as exc:
            issues.append(f"checkpoint invalid json: {exc}")

    result = {"folder": str(folder), "ok": not issues, "issues": issues, "warnings": warnings, "files": status}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
