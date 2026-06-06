#!/usr/bin/env python3
"""Manage SDD Delivery capability adapter/executor switches."""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path

try:
    from _utils import append_event, load_json, now, write_json
    from write_checkpoint import CAPABILITY_IDS, CAPABILITY_STATES, checkpoint_path, default_capabilities, load_checkpoint_or_default, normalize_capabilities, set_capability
except ImportError:
    from scripts._utils import append_event, load_json, now, write_json
    from scripts.write_checkpoint import CAPABILITY_IDS, CAPABILITY_STATES, checkpoint_path, default_capabilities, load_checkpoint_or_default, normalize_capabilities, set_capability


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_CONFIG = ROOT / "assets" / "capabilities.json"


def load_registry() -> dict:
    registry = load_json(CAPABILITY_CONFIG)
    return registry.get("capabilities", {})


def signal_matches(project_root: Path, signal: str) -> bool:
    if signal.startswith("."):
        return (project_root / signal).exists()
    if any(ch in signal for ch in "*?[]"):
        return any(fnmatch.fnmatch(str(path.relative_to(project_root)), signal) for path in project_root.rglob("*"))
    return (project_root / signal).exists() or any(path.name == signal for path in project_root.rglob(signal) if path.exists())


def detect_capabilities(project_root: Path, registry: dict) -> list[dict]:
    detected: list[dict] = []
    for capability_id, config in registry.items():
        adapter = config.get("adapter", {})
        signals = adapter.get("signals", [])
        matches = [signal for signal in signals if signal_matches(project_root, signal)]
        if matches:
            detected.append({"id": capability_id, "adapter": adapter.get("type", ""), "signals": matches})
    return detected


def executor_plan(checkpoint: dict, registry: dict) -> list[dict]:
    normalize_capabilities(checkpoint)
    plan: list[dict] = []
    for capability_id, switch in checkpoint.get("capabilities", {}).items():
        if switch.get("state") != "enabled":
            continue
        executor = registry.get(capability_id, {}).get("executor", {})
        plan.append({
            "id": capability_id,
            "state": "enabled",
            "executor": executor.get("type", ""),
            "phases": executor.get("phases", []),
            "reference": executor.get("reference", ""),
            "command": executor.get("command", ""),
        })
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect, configure, and plan SDD Delivery capabilities.")
    parser.add_argument("folder", help="Feature artifact folder containing 11-checkpoint.json")
    parser.add_argument("--project-root", default=".", help="Project root to scan for capability signals.")
    parser.add_argument("--detect", action="store_true", help="Detect matching capability adapters from project files.")
    parser.add_argument("--set", action="append", default=[], help="Set capability as id=enabled|disabled|ask[:reason].")
    parser.add_argument("--plan", action="store_true", help="Print enabled executor plan.")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    project_root = Path(args.project_root).resolve()
    registry = load_registry()
    checkpoint = load_checkpoint_or_default(checkpoint_path(folder))

    for spec in args.set:
        try:
            set_capability(checkpoint, spec)
        except ValueError as exc:
            print(json.dumps({"ok": False, "error": str(exc), "spec": spec}, ensure_ascii=False, indent=2))
            return 2

    detected = detect_capabilities(project_root, registry) if args.detect else []
    normalize_capabilities(checkpoint)
    checkpoint["capability_executor_plan"] = executor_plan(checkpoint, registry)
    checkpoint["updated_at"] = now()
    write_json(checkpoint_path(folder), checkpoint)
    append_event(folder, "capabilities_updated", {"set": args.set, "detected": detected, "plan": checkpoint["capability_executor_plan"]})

    result = {
        "folder": str(folder),
        "project_root": str(project_root),
        "detected": detected,
        "capabilities": checkpoint.get("capabilities", {}),
        "enabled_capabilities": checkpoint.get("enabled_capabilities", []),
    }
    if args.plan:
        result["executor_plan"] = checkpoint["capability_executor_plan"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
