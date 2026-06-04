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


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync observability dashboard from checkpoint metrics.")
    parser.add_argument("folder", help="Feature artifact folder")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    checkpoint = load_json(folder / "11-checkpoint.json")
    trace = load_json(folder / "trace-coverage.json")
    test = load_json(folder / "test-spec-coverage.json")
    metrics = checkpoint.get("metrics", {})
    metrics.update(trace)
    if test:
        metrics["reverse_test_specs_found"] = test.get("covered_specs", 0)

    gates = checkpoint.get("gate_status", {})
    rows = [
        ("Feature", checkpoint.get("feature", folder.name)),
        ("Current phase", checkpoint.get("current_phase", "")),
        ("Active task", checkpoint.get("active_task", "")),
        ("Spec review gate", gates.get("spec_review", "pending")),
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
        ("Updated at", now()),
    ]

    lines = ["# Observability", "", "## Delivery Dashboard", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rows]
    lines += ["", "## Gate History", "", "| Time | Gate | Status | Notes |", "|---|---|---|---|", "", "## Commands Run", "", "| Time | Command | Status | Summary |", "|---|---|---|---|", "", "## Events", "", "See `events.jsonl`."]
    (folder / "12-observability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_event(folder, "observability_synced", {"metrics": len(rows)})
    print(json.dumps({"observability": str(folder / "12-observability.md"), "metrics": len(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
