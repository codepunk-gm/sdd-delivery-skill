#!/usr/bin/env python3
"""Record MCP discovery and capability-selection evidence for SDD Delivery."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import append_event, load_json, now, write_json
    from write_checkpoint import checkpoint_path, load_checkpoint_or_default, set_capability
except ImportError:
    from scripts._utils import append_event, load_json, now, write_json
    from scripts.write_checkpoint import checkpoint_path, load_checkpoint_or_default, set_capability


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
DISCOVERY_FILE = "mcp-discovery.json"
SELECTION_FILE = "mcp-component-selection.md"


def default_discovery(feature: str) -> dict:
    return {
        "schema_version": "1.0",
        "feature": feature,
        "status": "not_started",
        "discovered_at": "",
        "source": "",
        "query_intent": "",
        "servers": [],
        "tools": [],
        "resources": [],
        "components": [],
        "unavailable": [],
        "notes": "",
    }


def load_discovery(folder: Path) -> dict:
    data = load_json(folder / DISCOVERY_FILE)
    if not data:
        data = default_discovery(folder.name)
    for key in ["servers", "tools", "resources", "components", "unavailable"]:
        if not isinstance(data.get(key), list):
            data[key] = []
    data.setdefault("feature", folder.name)
    data.setdefault("schema_version", "1.0")
    data.setdefault("status", "not_started")
    data.setdefault("source", "")
    data.setdefault("query_intent", "")
    data.setdefault("notes", "")
    data.setdefault("discovered_at", "")
    return data


def append_unique(items: list[dict], item: dict) -> None:
    key = (item.get("name", ""), item.get("source", ""))
    for existing in items:
        if (existing.get("name", ""), existing.get("source", "")) == key:
            existing.update({k: v for k, v in item.items() if v})
            return
    items.append(item)


def parse_record(spec: str, kind: str) -> dict:
    parts = spec.split("::", 3)
    return {
        "name": parts[0].strip(),
        "source": parts[1].strip() if len(parts) > 1 else "",
        "status": parts[2].strip() if len(parts) > 2 else "available",
        "notes": parts[3].strip() if len(parts) > 3 else "",
        "recorded_at": now(),
        "type": kind,
    }


def render_selection(discovery: dict, existing_text: str = "") -> str:
    lines = [
        "# MCP 组件选择记录",
        "",
        "> 使用说明：启用“企业 MCP 能力复用”后维护本文件。实现前先通过 MCP 查询企业内部可复用能力，记录发现到的 server/tool/resource/component、选择理由、使用约束、fallback 决策和验证证据。不要只在聊天里说明。",
        "",
        "## 发现摘要",
        "",
        "| 类型 | 名称 | 来源 | 状态 | 说明 |",
        "|---|---|---|---|---|",
    ]
    for kind, key in [("server", "servers"), ("tool", "tools"), ("resource", "resources"), ("component", "components")]:
        for item in discovery.get(key, []):
            lines.append(
                f"| {kind} | {item.get('name', '')} | {item.get('source', '')} | {item.get('status', '')} | {item.get('notes', '')} |"
            )
    for item in discovery.get("unavailable", []):
        lines.append(
            f"| unavailable | {item.get('name', '')} | {item.get('source', '')} | {item.get('status', '')} | {item.get('notes', '')} |"
        )
    if len(lines) == 7:
        lines.append("| - | - | - | pending | - |")

    preserved_sections = ["## 选择决策", "## 使用约束", "## Fallback 记录", "## 集成验证"]
    if existing_text:
        for section in preserved_sections:
            start = existing_text.find(section)
            if start != -1:
                lines.extend(["", existing_text[start:].strip()])
                return "\n".join(lines) + "\n"

    template = (TEMPLATES / SELECTION_FILE).read_text(encoding="utf-8-sig")
    for section in preserved_sections:
        start = template.find(section)
        if start != -1:
            lines.extend(["", template[start:].strip()])
            break
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Record enterprise MCP capability discovery evidence for an SDD Delivery feature.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--source", default="", help="Where the discovery came from, for example Codex MCP tools or user-provided output.")
    parser.add_argument("--query-intent", default="", help="What enterprise capability the agent tried to discover.")
    parser.add_argument("--status", choices=["not_started", "available", "partial", "unavailable"], default="available")
    parser.add_argument("--server", action="append", default=[], help="Record server as name::source::status::notes.")
    parser.add_argument("--tool", action="append", default=[], help="Record tool as name::source::status::notes.")
    parser.add_argument("--resource", action="append", default=[], help="Record resource as name::source::status::notes.")
    parser.add_argument("--component", action="append", default=[], help="Record component as name::source::status::notes.")
    parser.add_argument("--unavailable", action="append", default=[], help="Record unavailable MCP capability as name::source::status::notes.")
    parser.add_argument("--notes", default="")
    parser.add_argument("--enable-capability", action="store_true", help="Set mcp_component_protocol=enabled in checkpoint.")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    discovery = load_discovery(folder)
    discovery["status"] = args.status
    discovery["source"] = args.source or discovery.get("source", "")
    discovery["query_intent"] = args.query_intent or discovery.get("query_intent", "")
    discovery["notes"] = args.notes or discovery.get("notes", "")
    discovery["discovered_at"] = now()

    for spec in args.server:
        append_unique(discovery["servers"], parse_record(spec, "server"))
    for spec in args.tool:
        append_unique(discovery["tools"], parse_record(spec, "tool"))
    for spec in args.resource:
        append_unique(discovery["resources"], parse_record(spec, "resource"))
    for spec in args.component:
        append_unique(discovery["components"], parse_record(spec, "component"))
    for spec in args.unavailable:
        append_unique(discovery["unavailable"], parse_record(spec, "unavailable"))

    write_json(folder / DISCOVERY_FILE, discovery)

    selection_path = folder / SELECTION_FILE
    existing_text = selection_path.read_text(encoding="utf-8-sig") if selection_path.exists() else ""
    selection_path.write_text(render_selection(discovery, existing_text), encoding="utf-8")

    checkpoint = load_checkpoint_or_default(checkpoint_path(folder))
    if args.enable_capability:
        set_capability(checkpoint, "mcp_component_protocol=enabled:MCP capability discovery evidence recorded")
    checkpoint.setdefault("changed_files", [])
    for name in [DISCOVERY_FILE, SELECTION_FILE]:
        if name not in checkpoint["changed_files"]:
            checkpoint["changed_files"].append(name)
    checkpoint.setdefault("metrics", {})["mcp_items_discovered"] = (
        len(discovery.get("servers", [])) + len(discovery.get("tools", [])) + len(discovery.get("resources", [])) + len(discovery.get("components", []))
    )
    checkpoint["updated_at"] = now()
    write_json(checkpoint_path(folder), checkpoint)

    append_event(folder, "mcp_discovery_recorded", {
        "status": discovery["status"],
        "servers": len(discovery["servers"]),
        "tools": len(discovery["tools"]),
        "resources": len(discovery["resources"]),
        "components": len(discovery["components"]),
        "unavailable": len(discovery["unavailable"]),
    })
    print(json.dumps({
        "discovery": str(folder / DISCOVERY_FILE),
        "selection": str(selection_path),
        "status": discovery["status"],
        "items": checkpoint["metrics"]["mcp_items_discovered"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
