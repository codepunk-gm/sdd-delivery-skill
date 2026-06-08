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


LABELS = {
    "title": "可观测面板",
    "dashboard": "交付面板",
    "metric": "指标",
    "value": "值",
    "feature": "需求",
    "goal": "目标",
    "current_phase": "当前阶段",
    "active_task": "当前任务",
    "next_action": "下一步",
    "spec_review_gate": "Spec 审查门禁",
    "solution_approval_gate": "方案确认门禁",
    "solution_review_gate": "方案审查门禁",
    "unit_test_gate": "单测门禁",
    "delivery_review_gate": "交付审查门禁",
    "prd_items_total": "PRD 条目总数",
    "spec_items_total": "Spec 条目总数",
    "trace_items_total": "追踪条目总数",
    "solution_coverage_rate": "方案覆盖率",
    "task_coverage_rate": "任务覆盖率",
    "code_coverage_rate": "代码覆盖率",
    "unit_test_coverage_rate": "单测覆盖率",
    "reverse_test_specs_found": "测试反查 Spec 数",
    "tasks_total": "任务总数",
    "tasks_completed": "已完成任务",
    "checks_total": "检查总数",
    "checks_passed": "通过检查",
    "checks_failed": "失败检查",
    "review_findings_open": "未关闭审查项",
    "review_findings_closed": "已关闭审查项",
    "checkpoints_written": "检查点写入次数",
    "mcp_capability": "MCP 能力",
    "mcp_discovery_status": "MCP 发现状态",
    "mcp_items_discovered": "MCP 发现项",
    "updated_at": "更新时间",
}

QUALITY_LABELS = {
    "progress": "进度",
    "traceability": "可追踪性",
    "test_evidence": "测试证据",
    "review_readiness": "审查就绪度",
    "delivery_confidence": "交付信心",
}


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
    mcp_items = (
        len(mcp.get("servers", []))
        + len(mcp.get("tools", []))
        + len(mcp.get("resources", []))
        + len(mcp.get("components", []))
        if mcp
        else 0
    )
    rows = [
        (LABELS["feature"], checkpoint.get("feature", folder.name)),
        (LABELS["goal"], checkpoint.get("goal", "")),
        (LABELS["current_phase"], checkpoint.get("current_phase", "")),
        (LABELS["active_task"], checkpoint.get("active_task", "")),
        (LABELS["next_action"], checkpoint.get("next_action", "")),
        (LABELS["spec_review_gate"], gates.get("spec_review", "pending")),
        (LABELS["solution_approval_gate"], gates.get("solution_approval", "pending")),
        (LABELS["solution_review_gate"], gates.get("solution_review", "pending")),
        (LABELS["unit_test_gate"], gates.get("unit_test_plan", "pending")),
        (LABELS["delivery_review_gate"], gates.get("delivery_review", "pending")),
        (LABELS["prd_items_total"], metrics.get("prd_items_total", 0)),
        (LABELS["spec_items_total"], metrics.get("spec_items_total", 0)),
        (LABELS["trace_items_total"], metrics.get("trace_items_total", 0)),
        (LABELS["solution_coverage_rate"], metrics.get("solution_coverage_rate", 0)),
        (LABELS["task_coverage_rate"], metrics.get("task_coverage_rate", 0)),
        (LABELS["code_coverage_rate"], metrics.get("code_coverage_rate", 0)),
        (LABELS["unit_test_coverage_rate"], metrics.get("unit_test_coverage_rate", 0)),
        (LABELS["reverse_test_specs_found"], metrics.get("reverse_test_specs_found", 0)),
        (LABELS["tasks_total"], metrics.get("tasks_total", 0)),
        (LABELS["tasks_completed"], metrics.get("tasks_completed", 0)),
        (LABELS["checks_total"], metrics.get("checks_total", 0)),
        (LABELS["checks_passed"], metrics.get("checks_passed", 0)),
        (LABELS["checks_failed"], metrics.get("checks_failed", 0)),
        (LABELS["review_findings_open"], metrics.get("review_findings_open", 0)),
        (LABELS["review_findings_closed"], metrics.get("review_findings_closed", 0)),
        (LABELS["checkpoints_written"], metrics.get("checkpoints_written", 0)),
        (LABELS["mcp_capability"], mcp_switch.get("state", "ask")),
        (LABELS["mcp_discovery_status"], mcp.get("status", "not_started") if mcp else "not_started"),
        (LABELS["mcp_items_discovered"], mcp_items),
        (LABELS["updated_at"], now()),
    ]

    lines = [f"# {LABELS['title']}", "", f"## {LABELS['dashboard']}", "", f"| {LABELS['metric']} | {LABELS['value']} |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rows]

    lines += [
        "",
        "## 质量状态",
        "",
        "| 范围 | 状态 |",
        "|---|---|",
    ]
    quality_rows = [
        (QUALITY_LABELS["progress"], quality_status.get("progress", "pending")),
        (QUALITY_LABELS["traceability"], quality_status.get("traceability", "pending")),
        (QUALITY_LABELS["test_evidence"], quality_status.get("test_evidence", "pending")),
        (QUALITY_LABELS["review_readiness"], quality_status.get("review_readiness", "pending")),
        (QUALITY_LABELS["delivery_confidence"], quality_status.get("delivery_confidence", "pending")),
    ]
    lines += [f"| {area} | {status} |" for area, status in quality_rows]

    lines += [
        "",
        "## MCP 证据",
        "",
        "| 字段 | 值 |",
        "|---|---|",
        f"| 能力开关 | {mcp_switch.get('state', 'ask')} |",
        f"| 发现状态 | {mcp.get('status', 'not_started') if mcp else 'not_started'} |",
        f"| 来源 | {mcp.get('source', '') if mcp else ''} |",
        f"| Server 数 | {len(mcp.get('servers', [])) if mcp else 0} |",
        f"| Tool 数 | {len(mcp.get('tools', [])) if mcp else 0} |",
        f"| Component 数 | {len(mcp.get('components', [])) if mcp else 0} |",
        f"| 不可用项 | {len(mcp.get('unavailable', [])) if mcp else 0} |",
        "| 证据文件 | `mcp-discovery.json`, `mcp-component-selection.md` |",
    ]

    lines += [
        "",
        "## 里程碑",
        "",
        "| ID | 名称 | 状态 | 门禁 | 证据 | 审查人 | 更新时间 |",
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
        "## 人工审查",
        "",
        "| 时间 | 审查人 | 对象 | 结果 | 备注 |",
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
        "## 门禁历史",
        "",
        "| 时间 | 门禁 | 状态 | 备注 |",
        "|---|---|---|---|",
    ]
    lines += [f"| {checkpoint.get('updated_at', '')} | {gate} | {status} | checkpoint |" for gate, status in gates.items()]

    lines += [
        "",
        "## 执行命令",
        "",
        "| 时间 | 命令 | 状态 | 摘要 |",
        "|---|---|---|---|",
    ]
    tests_run = checkpoint.get("tests_run", [])
    if tests_run:
        lines += [
            f"| {item.get('source', '')} | `{item.get('command', '')}` | {item.get('status', '')} | {item.get('summary', '')} |"
            for item in tests_run
        ]

    lines += ["", "## 事件", "", "详见 `events.jsonl`。"]
    (folder / "12-observability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_event(folder, "observability_synced", {"metrics": len(rows)})
    print(json.dumps({"observability": str(folder / "12-observability.md"), "metrics": len(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
