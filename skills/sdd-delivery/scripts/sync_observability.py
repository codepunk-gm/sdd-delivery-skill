#!/usr/bin/env python3
"""Sync 12-observability.md from checkpoint and coverage artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import append_event, load_json, now
except ImportError:
    from scripts._utils import append_event, load_json, now


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync observability dashboard from checkpoint metrics.")
    parser.add_argument("folder", help="Feature artifact folder")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    checkpoint = load_json(folder / "11-checkpoint.json")
    trace = load_json(folder / "trace-coverage.json")
    test = load_json(folder / "test-spec-coverage.json")
    mcp = load_json(folder / "mcp-discovery.json")
    metrics = checkpoint.get("metrics", {})
    metrics.update(trace)
    if test:
        metrics["reverse_test_specs_found"] = test.get("covered_specs", 0)

    gates = checkpoint.get("gate_status", {})
    milestones = checkpoint.get("milestones", [])
    human_reviews = checkpoint.get("human_reviews", [])
    quality_status = checkpoint.get("quality_status", {})
    capabilities = checkpoint.get("capabilities", {})
    mcp_switch = capabilities.get("mcp_component_protocol", {}) if isinstance(capabilities, dict) else {}
    mcp_items = len(mcp.get("servers", [])) + len(mcp.get("tools", [])) + len(mcp.get("components", [])) if mcp else 0
    rows = [
        ("Feature", checkpoint.get("feature", folder.name)),
        ("Goal", checkpoint.get("goal", "")),
        ("Current phase", checkpoint.get("current_phase", "")),
        ("Active task", checkpoint.get("active_task", "")),
        ("Next action", checkpoint.get("next_action", "")),
        ("Spec review gate", gates.get("spec_review", "pending")),
        ("Solution approval gate", gates.get("solution_approval", "pending")),
        ("Solution review gate", gates.get("solution_review", "pending")),
        ("Unit test gate", gates.get("unit_test_plan", "pending")),
        ("Delivery review gate", gates.get("delivery_review", "pending")),
        ("PRD items total", metrics.get("prd_items_total", 0)),
        ("Spec items total", metrics.get("spec_items_total", 0)),
        ("Trace items total", metrics.get("trace_items_total", 0)),
        ("Solution coverage rate", metrics.get("solution_coverage_rate", 0)),
        ("Task coverage rate", metrics.get("task_coverage_rate", 0)),
        ("Code coverage rate", metrics.get("code_coverage_rate", 0)),
        ("Unit test coverage rate", metrics.get("unit_test_coverage_rate", 0)),
        ("Reverse test specs found", metrics.get("reverse_test_specs_found", 0)),
        ("Tasks total", metrics.get("tasks_total", 0)),
        ("Tasks completed", metrics.get("tasks_completed", 0)),
        ("Checks total", metrics.get("checks_total", 0)),
        ("Checks passed", metrics.get("checks_passed", 0)),
        ("Checks failed", metrics.get("checks_failed", 0)),
        ("Review findings open", metrics.get("review_findings_open", 0)),
        ("Review findings closed", metrics.get("review_findings_closed", 0)),
        ("Checkpoints written", metrics.get("checkpoints_written", 0)),
        ("MCP capability", mcp_switch.get("state", "ask")),
        ("MCP discovery status", mcp.get("status", "not_started") if mcp else "not_started"),
        ("MCP items discovered", mcp_items),
        ("Updated at", now()),
    ]

    lines = ["# Observability", "", "## Delivery Dashboard", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rows]

    lines += [
        "",
        "## Quality Status",
        "",
        "| Area | Status |",
        "|---|---|",
    ]
    quality_rows = [
        ("Progress", quality_status.get("progress", "pending")),
        ("Traceability", quality_status.get("traceability", "pending")),
        ("Test evidence", quality_status.get("test_evidence", "pending")),
        ("Review readiness", quality_status.get("review_readiness", "pending")),
        ("Delivery confidence", quality_status.get("delivery_confidence", "pending")),
    ]
    lines += [f"| {area} | {status} |" for area, status in quality_rows]

    lines += [
        "",
        "## MCP Evidence",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Capability | {mcp_switch.get('state', 'ask')} |",
        f"| Discovery status | {mcp.get('status', 'not_started') if mcp else 'not_started'} |",
        f"| Source | {mcp.get('source', '') if mcp else ''} |",
        f"| Servers | {len(mcp.get('servers', [])) if mcp else 0} |",
        f"| Tools | {len(mcp.get('tools', [])) if mcp else 0} |",
        f"| Components | {len(mcp.get('components', [])) if mcp else 0} |",
        f"| Unavailable | {len(mcp.get('unavailable', [])) if mcp else 0} |",
        "| Evidence files | `mcp-discovery.json`, `mcp-component-selection.md` |",
    ]

    lines += [
        "",
        "## Milestones",
        "",
        "| ID | Name | Status | Gates | Evidence | Reviewer | Updated At |",
        "|---|---|---|---|---|---|---|",
    ]
    if milestones:
        for milestone in milestones:
            lines.append(
                "| {id} | {name} | {status} | {gates} | {evidence} | {reviewer} | {updated_at} |".format(
                    id=milestone.get("id", ""),
                    name=milestone.get("name", ""),
                    status=milestone.get("status", "pending"),
                    gates=format_list(milestone.get("gates", [])),
                    evidence=format_list(milestone.get("evidence", [])),
                    reviewer=milestone.get("reviewer", ""),
                    updated_at=milestone.get("updated_at", ""),
                )
            )
    else:
        lines.append("| - | - | pending | - | - | - | - |")

    lines += [
        "",
        "## Human Reviews",
        "",
        "| Time | Reviewer | Target | Result | Notes |",
        "|---|---|---|---|---|",
    ]
    if human_reviews:
        for review in human_reviews:
            lines.append(
                "| {time} | {reviewer} | {target} | {result} | {notes} |".format(
                    time=review.get("time", ""),
                    reviewer=review.get("reviewer", ""),
                    target=review.get("target", ""),
                    result=review.get("result", ""),
                    notes=review.get("notes", ""),
                )
            )
    else:
        lines.append("| - | - | - | - | - |")

    lines += [
        "",
        "## Gate History",
        "",
        "| Time | Gate | Status | Notes |",
        "|---|---|---|---|",
    ]
    lines += [f"| {checkpoint.get('updated_at', '')} | {gate} | {status} | checkpoint |" for gate, status in gates.items()]

    lines += [
        "",
        "## Commands Run",
        "",
        "| Time | Command | Status | Summary |",
        "|---|---|---|---|",
    ]
    tests_run = checkpoint.get("tests_run", [])
    if tests_run:
        lines += [
            f"| {item.get('source', '')} | `{item.get('command', '')}` | {item.get('status', '')} | {item.get('summary', '')} |"
            for item in tests_run
        ]

    lines += ["", "## Events", "", "See `events.jsonl`."]
    (folder / "12-observability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_event(folder, "observability_synced", {"metrics": len(rows)})
    print(json.dumps({"observability": str(folder / "12-observability.md"), "metrics": len(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
