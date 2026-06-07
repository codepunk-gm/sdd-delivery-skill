#!/usr/bin/env python3
"""Update SDD Delivery v2 checkpoint and event log."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import add_unique, append_event, load_json, now, write_json
except ImportError:
    from scripts._utils import add_unique, append_event, load_json, now, write_json

CAPABILITY_IDS = [
    "frontend_template",
    "java_modular_project",
    "mcp_component_protocol",
    "github_delivery_assets",
    "team_code_principles",
]

CAPABILITY_STATES = {"enabled", "disabled", "ask"}

DEFAULT_MILESTONES = [
    {
        "id": "M1",
        "name": "需求基线",
        "status": "pending",
        "gates": ["clarify", "spec", "spec_review", "analyze"],
        "evidence": ["00-prd.md", "01-spec.md", "02-spec-review.md", "03-requirement-trace.md"],
        "reviewer": "",
        "updated_at": "",
    },
    {
        "id": "M2",
        "name": "方案确认",
        "status": "pending",
        "gates": ["solution", "solution_approval", "solution_review"],
        "evidence": ["04-tech-solution.md", "05-solution-review.md"],
        "reviewer": "",
        "updated_at": "",
    },
    {
        "id": "M3",
        "name": "实现受控",
        "status": "pending",
        "gates": ["tdd", "per_task_review"],
        "evidence": ["06-implementation-tasks.md", "07-implementation-log.md"],
        "reviewer": "",
        "updated_at": "",
    },
    {
        "id": "M4",
        "name": "验证完成",
        "status": "pending",
        "gates": ["unit_test_plan", "test_report"],
        "evidence": ["08-unit-test-plan.md", "09-unit-test-report.md"],
        "reviewer": "",
        "updated_at": "",
    },
    {
        "id": "M5",
        "name": "交付就绪",
        "status": "pending",
        "gates": ["delivery_review"],
        "evidence": ["10-delivery-review.md", "11-checkpoint.json", "12-observability.md"],
        "reviewer": "",
        "updated_at": "",
    },
]

QUALITY_FIELDS = ["progress", "traceability", "test_evidence", "review_readiness", "delivery_confidence"]


def default_capabilities() -> dict:
    return {
        capability_id: {"state": "ask", "reason": "", "source": "default", "updated_at": ""}
        for capability_id in CAPABILITY_IDS
    }


def normalize_capabilities(data: dict) -> None:
    """Ensure checkpoint has structured capability switches and legacy index."""
    capabilities = data.setdefault("capabilities", default_capabilities())
    for capability_id in CAPABILITY_IDS:
        value = capabilities.get(capability_id)
        if isinstance(value, str):
            state = value if value in CAPABILITY_STATES else "ask"
            capabilities[capability_id] = {"state": state, "reason": "", "source": "legacy", "updated_at": ""}
        elif not isinstance(value, dict):
            capabilities[capability_id] = {"state": "ask", "reason": "", "source": "default", "updated_at": ""}
        else:
            state = value.get("state", "ask")
            value["state"] = state if state in CAPABILITY_STATES else "ask"
            value.setdefault("reason", "")
            value.setdefault("source", "checkpoint")
            value.setdefault("updated_at", "")

    legacy_enabled = set(data.get("enabled_capabilities", []))
    for capability_id in legacy_enabled:
        if capability_id in CAPABILITY_IDS and capabilities[capability_id]["state"] == "ask":
            capabilities[capability_id].update({"state": "enabled", "source": "legacy", "updated_at": ""})

    data["enabled_capabilities"] = [
        capability_id
        for capability_id in CAPABILITY_IDS
        if capabilities.get(capability_id, {}).get("state") == "enabled"
    ]


def default_milestones() -> list[dict]:
    return [dict(milestone) for milestone in DEFAULT_MILESTONES]


def normalize_human_coordination(data: dict) -> None:
    """Ensure checkpoint has milestone and human-review coordination fields."""
    existing = {
        item.get("id"): item
        for item in data.get("milestones", [])
        if isinstance(item, dict) and item.get("id")
    }
    milestones: list[dict] = []
    for default in DEFAULT_MILESTONES:
        merged = dict(default)
        merged.update(existing.get(default["id"], {}))
        merged.setdefault("reviewer", "")
        merged.setdefault("updated_at", "")
        milestones.append(merged)
    data["milestones"] = milestones
    if not isinstance(data.get("human_reviews"), list):
        data["human_reviews"] = []
    quality = data.setdefault("quality_status", {})
    if not isinstance(quality, dict):
        quality = {}
        data["quality_status"] = quality
    for field in QUALITY_FIELDS:
        quality.setdefault(field, "pending")


def set_milestone(data: dict, spec: str) -> None:
    """Set milestone status from id=status[:reviewer[:notes]]."""
    if "=" in spec:
        milestone_id, rest = spec.split("=", 1)
    else:
        milestone_id, rest = spec, "reviewed"
    parts = rest.split(":", 2)
    status = parts[0].strip() or "reviewed"
    reviewer = parts[1].strip() if len(parts) > 1 else ""
    notes = parts[2].strip() if len(parts) > 2 else ""
    normalize_human_coordination(data)
    for milestone in data["milestones"]:
        if milestone["id"] == milestone_id.strip():
            milestone["status"] = status
            if reviewer:
                milestone["reviewer"] = reviewer
            milestone["updated_at"] = now()
            if notes:
                data.setdefault("human_reviews", []).append({
                    "time": now(),
                    "reviewer": reviewer,
                    "target": milestone["id"],
                    "result": status,
                    "notes": notes,
                })
            return
    raise ValueError(f"unknown milestone: {milestone_id}")


def add_human_review(data: dict, spec: str) -> None:
    """Record human review as reviewer::target::result::notes."""
    parts = spec.split("::", 3)
    review = {
        "time": now(),
        "reviewer": parts[0] if len(parts) > 0 else "",
        "target": parts[1] if len(parts) > 1 else "",
        "result": parts[2] if len(parts) > 2 else "",
        "notes": parts[3] if len(parts) > 3 else "",
    }
    data.setdefault("human_reviews", []).append(review)


def set_quality(data: dict, spec: str) -> None:
    """Set quality status as field=value."""
    if "=" not in spec:
        raise ValueError("quality must be field=value")
    key, value = spec.split("=", 1)
    key = key.strip()
    if key not in QUALITY_FIELDS:
        raise ValueError(f"unknown quality field: {key}")
    data.setdefault("quality_status", {})[key] = value.strip()


def set_capability(data: dict, spec: str) -> None:
    """Set capability state from id or id=state[:reason]."""
    if "=" in spec:
        capability_id, rest = spec.split("=", 1)
        if ":" in rest:
            state, reason = rest.split(":", 1)
        else:
            state, reason = rest, ""
    else:
        capability_id, state, reason = spec, "enabled", ""
    capability_id = capability_id.strip()
    state = state.strip()
    if capability_id not in CAPABILITY_IDS:
        raise ValueError(f"unknown capability: {capability_id}")
    if state not in CAPABILITY_STATES:
        raise ValueError(f"invalid capability state for {capability_id}: {state}")
    data.setdefault("capabilities", default_capabilities())[capability_id] = {
        "state": state,
        "reason": reason.strip(),
        "source": "write_checkpoint.py",
        "updated_at": now(),
    }
    normalize_capabilities(data)


def default_checkpoint(folder: Path) -> dict:
    return {
        "schema_version": "2.0",
        "feature": folder.name,
        "goal": "",
        "current_phase": "",
        "active_task": "",
        "gate_status": {"clarify": "pending", "spec": "pending", "spec_review": "pending", "analyze": "pending", "solution": "pending", "solution_approval": "pending", "solution_review": "pending", "tdd": "pending", "per_task_review": "pending", "unit_test_plan": "pending", "test_report": "pending", "delivery_review": "pending"},
        "completed_tasks": [],
        "pending_tasks": [],
        "enabled_capabilities": [],
        "capability_executor_plan": [],
        "capabilities": default_capabilities(),
        "preferences": {"delivery_language": "auto", "comment_language": "auto", "team_rule_setup": "pending"},
        "solution_approval": {"status": "pending", "approver": "", "notes": "", "source": "", "time": ""},
        "milestones": default_milestones(),
        "human_reviews": [],
        "quality_status": {"progress": "pending", "traceability": "pending", "test_evidence": "pending", "review_readiness": "pending", "delivery_confidence": "pending"},
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


def load_checkpoint_or_default(path: Path) -> dict:
    """Load checkpoint JSON, falling back to a default template if missing."""
    data = load_json(path)
    checkpoint = data if data else default_checkpoint(path.parent)
    normalize_capabilities(checkpoint)
    normalize_human_coordination(checkpoint)
    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(description="Update SDD Delivery v2 checkpoint.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--phase")
    parser.add_argument("--task")
    parser.add_argument("--goal")
    parser.add_argument("--next-action")
    parser.add_argument("--language", choices=["auto", "zh", "en", "bilingual"], help="Set artifact and chat language preference.")
    parser.add_argument("--capability", action="append", default=[], help="Set capability switch as id or id=enabled|disabled|ask[:reason].")
    parser.add_argument("--approval", help="Record solution approval as status::approver::notes")
    parser.add_argument("--milestone", action="append", default=[], help="Set milestone as M1=status[:reviewer[:notes]].")
    parser.add_argument("--human-review", action="append", default=[], help="Record human review as reviewer::target::result::notes.")
    parser.add_argument("--quality", action="append", default=[], help="Set quality status as progress=on_track.")
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
    data = load_checkpoint_or_default(path)

    if args.phase:
        data["current_phase"] = args.phase
    if args.task:
        data["active_task"] = args.task
    if args.goal:
        data["goal"] = args.goal
    if args.next_action:
        data["next_action"] = args.next_action
    if args.language:
        data.setdefault("preferences", {})["delivery_language"] = args.language
    for capability in args.capability:
        set_capability(data, capability)
    for milestone in args.milestone:
        set_milestone(data, milestone)
    for review in args.human_review:
        add_human_review(data, review)
    for quality in args.quality:
        set_quality(data, quality)
    if args.approval:
        parts = args.approval.split("::", 2)
        approval = {
            "status": parts[0],
            "approver": parts[1] if len(parts) > 1 else "",
            "notes": parts[2] if len(parts) > 2 else "",
            "source": "write_checkpoint.py",
            "time": now(),
        }
        data["solution_approval"] = approval
        data.setdefault("decisions", []).append({
            "decision": f"solution_approval={approval['status']}",
            "reason": approval["notes"],
            "source": approval["approver"] or "user",
        })

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
    write_json(path, data)
    append_event(folder, "checkpoint_updated", {"phase": data.get("current_phase"), "task": data.get("active_task"), "gates": gates, "next_action": data.get("next_action")})
    print(json.dumps({"checkpoint": str(path), "phase": data.get("current_phase"), "task": data.get("active_task"), "gates": gates}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
