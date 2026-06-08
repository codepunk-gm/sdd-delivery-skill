#!/usr/bin/env python3
"""Initialize SDD Delivery v2 observable artifacts for a feature."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import append_event, now, safe_feature_name
except ImportError:
    from scripts._utils import append_event, now, safe_feature_name

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"

FILES = [
    ("prd.md", "00-prd.md"),
    ("spec.md", "01-spec.md"),
    ("spec-review.md", "02-spec-review.md"),
    ("requirement-trace.md", "03-requirement-trace.md"),
    ("tech-solution.md", "04-tech-solution.md"),
    ("solution-review.md", "05-solution-review.md"),
    ("implementation-tasks.md", "06-implementation-tasks.md"),
    ("implementation-log.md", "07-implementation-log.md"),
    ("unit-test-plan.md", "08-unit-test-plan.md"),
    ("unit-test-report.md", "09-unit-test-report.md"),
    ("delivery-review.md", "10-delivery-review.md"),
    ("checkpoint.json", "11-checkpoint.json"),
    ("observability.md", "12-observability.md"),
]

MCP_FILES = [
    ("mcp-discovery.json", "mcp-discovery.json"),
    ("mcp-component-selection.md", "mcp-component-selection.md"),
]


def copy_template(src: Path, dst: Path, feature: str, force: bool) -> bool:
    if dst.exists() and not force:
        return False
    text = src.read_text(encoding="utf-8-sig")
    if dst.name == "11-checkpoint.json":
        data = json.loads(text)
        data["feature"] = feature
        data["updated_at"] = now()
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    dst.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize SDD Delivery v2 artifacts.")
    parser.add_argument("feature", help="Feature name, for example add-login-rate-limit")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing artifacts.")
    parser.add_argument("--with-mcp", action="store_true", help="Also create MCP discovery and capability-selection evidence artifacts.")
    args = parser.parse_args()

    feature = safe_feature_name(args.feature)
    project_root = Path(args.root).resolve()
    folder = project_root / ".sdd-delivery" / feature
    folder.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    files = FILES + (MCP_FILES if args.with_mcp else [])
    for template_name, artifact_name in files:
        did_create = copy_template(TEMPLATES / template_name, folder / artifact_name, feature, args.force)
        (created if did_create else skipped).append(artifact_name)

    events = folder / "events.jsonl"
    if not events.exists() or args.force:
        events.write_text("", encoding="utf-8")
    append_event(folder, "artifacts_initialized", {"feature": feature, "version": "2.0", "created": created, "skipped": skipped})

    print(json.dumps({"feature": feature, "folder": str(folder), "created": created, "skipped": skipped}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
