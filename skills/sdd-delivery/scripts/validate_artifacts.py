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
    "enabled_capabilities",
    "capability_executor_plan",
    "capabilities",
    "preferences",
    "solution_approval",
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

REQUIRED_CAPABILITIES = [
    "frontend_template",
    "java_modular_project",
    "mcp_component_protocol",
    "github_delivery_assets",
    "team_code_principles",
]

CAPABILITY_STATES = {"enabled", "disabled", "ask"}

REQUIRED_GATES = [
    "clarify",
    "spec",
    "spec_review",
    "analyze",
    "solution",
    "solution_approval",
    "solution_review",
    "tdd",
    "per_task_review",
    "unit_test_plan",
    "test_report",
    "delivery_review",
]


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
            capabilities = checkpoint.get("capabilities", {})
            if not isinstance(capabilities, dict):
                issues.append("checkpoint capabilities must be an object")
            else:
                for capability_id in REQUIRED_CAPABILITIES:
                    capability = capabilities.get(capability_id)
                    if not isinstance(capability, dict):
                        issues.append(f"checkpoint missing capability switch: {capability_id}")
                        continue
                    state = capability.get("state")
                    if state not in CAPABILITY_STATES:
                        issues.append(f"invalid capability state: {capability_id}={state}")
                enabled_index = checkpoint.get("enabled_capabilities", [])
                if not isinstance(enabled_index, list):
                    issues.append("checkpoint enabled_capabilities must be a list")
                else:
                    structured_enabled = sorted(
                        capability_id
                        for capability_id, capability in capabilities.items()
                        if isinstance(capability, dict) and capability.get("state") == "enabled"
                    )
                    if sorted(enabled_index) != structured_enabled:
                        warnings.append("enabled_capabilities index does not match capabilities states")
        except json.JSONDecodeError as exc:
            issues.append(f"checkpoint invalid json: {exc}")

    result = {"folder": str(folder), "ok": not issues, "issues": issues, "warnings": warnings, "files": status}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
