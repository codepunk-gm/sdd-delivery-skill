#!/usr/bin/env python3
"""Initialize OP DevFlow v2 observable artifacts for a feature."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

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


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_feature(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "-" for c in name.strip()).strip("-._") or "feature"


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


def append_event(folder: Path, event: str, detail: dict) -> None:
    payload = {"time": now(), "event": event, "detail": detail}
    with (folder / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize OP DevFlow v2 artifacts.")
    parser.add_argument("feature", help="Feature name, for example add-login-rate-limit")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing artifacts.")
    args = parser.parse_args()

    feature = safe_feature(args.feature)
    project_root = Path(args.root).resolve()
    folder = project_root / ".op" / "devflow" / feature
    folder.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    for template_name, artifact_name in FILES:
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
