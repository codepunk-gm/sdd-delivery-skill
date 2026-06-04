#!/usr/bin/env python3
"""Update SDD Delivery v2 checkpoint and event log."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_checkpoint(folder: Path) -> dict:
    return {
        "schema_version": "2.0",
        "feature": folder.name,
        "goal": "",
        "current_phase": "",
        "active_task": "",
        "gate_status": {"clarify": "pending", "spec": "pending", "spec_review": "pending", "analyze": "pending", "solution": "pending", "solution_review": "pending", "tdd": "pending", "per_task_review": "pending", "unit_test_plan": "pending", "test_report": "pending", "delivery_review": "pending"},
        "completed_tasks": [],
        "pending_tasks": [],
        "decisions": [],
        "repo_facts": [],
        "changed_files": [],
        "tests_run": [],
        "metrics": {"prd_items_total": 0, "spec_items_total": 0, "trace_items_total": 0, "trace_items_tested": 0, "tasks_total": 0, "tasks_completed": 0, "checks_total": 0, "checks_passed": 0, "checks_failed": 0, "review_findings_open": 0, "review_findings_closed": 0, "checkpoints_written": 0},
        "risks": [],
        "blockers": [],
        "next_action": "",
        "updated_at": "",
    }


def checkpoint_path(folder: Path) -> Path:
    return folder / "11-checkpoint.json"


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return default_checkpoint(path.parent)


def add_unique(items: list, values: list[str]) -> None:
    for value in values:
        if value and value not in items:
            items.append(value)


def append_event(folder: Path, event: str, detail: dict) -> None:
    payload = {"time": now(), "event": event, "detail": detail}
    with (folder / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update SDD Delivery v2 checkpoint.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--phase")
    parser.add_argument("--task")
    parser.add_argument("--goal")
    parser.add_argument("--next-action")
    parser.add_argument("--gate", action="append", default=[], help="Set gate as name=status, for example spec_review=passed")
    parser.add_argument("--metric", action="append", default=[], help="Set metric as name=value")
    parser.add_argument("--complete", action="append", default=[])
    parser.add_argument("--pending", action="append", default=[])
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--test", help="Record test as command::status::summary")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    path = checkpoint_path(folder)
    data = load_json(path)

    if args.phase:
        data["current_phase"] = args.phase
    if args.task:
        data["active_task"] = args.task
    if args.goal:
        data["goal"] = args.goal
    if args.next_action:
        data["next_action"] = args.next_action

    gates = data.setdefault("gate_status", {})
    for item in args.gate:
        if "=" in item:
            key, value = item.split("=", 1)
            gates[key.strip()] = value.strip()

    metrics = data.setdefault("metrics", {})
    for item in args.metric:
        if "=" in item:
            key, value = item.split("=", 1)
            try:
                metrics[key.strip()] = int(value.strip())
            except ValueError:
                metrics[key.strip()] = value.strip()

    add_unique(data.setdefault("completed_tasks", []), args.complete)
    add_unique(data.setdefault("pending_tasks", []), args.pending)
    add_unique(data.setdefault("changed_files", []), args.changed_file)
    add_unique(data.setdefault("risks", []), args.risk)
    add_unique(data.setdefault("blockers", []), args.blocker)

    metrics["checkpoints_written"] = int(metrics.get("checkpoints_written", 0)) + 1
    metrics["tasks_completed"] = len(data.get("completed_tasks", []))
    metrics["tasks_total"] = max(int(metrics.get("tasks_total", 0)), len(data.get("completed_tasks", [])) + len(data.get("pending_tasks", [])))

    if args.test:
        parts = args.test.split("::", 2)
        command = parts[0]
        status = parts[1] if len(parts) > 1 else "skipped"
        summary = parts[2] if len(parts) > 2 else ""
        data.setdefault("tests_run", []).append({"command": command, "status": status, "summary": summary, "source": "write_checkpoint.py"})
        metrics["checks_total"] = int(metrics.get("checks_total", 0)) + 1
        if status == "passed":
            metrics["checks_passed"] = int(metrics.get("checks_passed", 0)) + 1
        elif status == "failed":
            metrics["checks_failed"] = int(metrics.get("checks_failed", 0)) + 1

    data["updated_at"] = now()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_event(folder, "checkpoint_updated", {"phase": data.get("current_phase"), "task": data.get("active_task"), "gates": gates, "next_action": data.get("next_action")})
    print(json.dumps({"checkpoint": str(path), "phase": data.get("current_phase"), "task": data.get("active_task"), "gates": gates}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
