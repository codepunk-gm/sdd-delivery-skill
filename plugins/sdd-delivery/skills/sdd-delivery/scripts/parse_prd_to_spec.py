#!/usr/bin/env python3
"""Parse a PRD markdown file into PRD, Spec, and trace artifacts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from _utils import append_event, now, write_json
except ImportError:
    from scripts._utils import append_event, now, write_json

ITEM_RE = re.compile(r"^\s*(?:[-*]\s+|\d+[.)]\s+|#{2,}\s+)(.+?)\s*$")
REQ_HINT_RE = re.compile(r"(must|should|shall|需要|必须|支持|允许|禁止|用户|系统|接口|页面|功能|验收|场景|when|given|then)", re.I)


def extract_items(text: str) -> list[str]:
    items = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("|"):
            continue
        m = ITEM_RE.match(line)
        candidate = m.group(1).strip() if m else ""
        if candidate and len(candidate) >= 4 and REQ_HINT_RE.search(candidate):
            candidate = re.sub(r"\s+", " ", candidate)
            if candidate not in items:
                items.append(candidate)
    if not items:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) >= 20]
        items = paras[:20]
    return items


def update_checkpoint(folder: Path, prd_count: int, spec_count: int) -> None:
    path = folder / "11-checkpoint.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    metrics = data.setdefault("metrics", {})
    metrics["prd_items_total"] = prd_count
    metrics["spec_items_total"] = spec_count
    metrics["trace_items_total"] = spec_count
    data["current_phase"] = "spec-authoring"
    data["updated_at"] = now()
    write_json(path, data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Spec artifacts from a PRD markdown file.")
    parser.add_argument("prd_file", help="PRD markdown file")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--force", action="store_true", help="Overwrite generated artifacts")
    args = parser.parse_args()

    prd_path = Path(args.prd_file).resolve()
    folder = Path(args.folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    text = prd_path.read_text(encoding="utf-8-sig")
    items = extract_items(text)

    prd_artifact = folder / "00-prd.md"
    spec_artifact = folder / "01-spec.md"
    trace_artifact = folder / "03-requirement-trace.md"

    if args.force or not prd_artifact.exists():
        rows = ["| PRD ID | Requirement | Priority | Notes |", "|---|---|---|---|"]
        for i, item in enumerate(items, 1):
            rows.append(f"| PRD-{i} | {item.replace('|', '/')} | Must | from {prd_path.name} |")
        prd_artifact.write_text("# PRD\n\n## Source\n\n" + str(prd_path) + "\n\n## Business Goal\n\n\n## PRD Items\n\n" + "\n".join(rows) + "\n\n## Constraints\n\n## Unknowns\n", encoding="utf-8")

    if args.force or not spec_artifact.exists():
        rows = ["| Spec ID | PRD ID | Behavior | Acceptance Criteria | Priority |", "|---|---|---|---|---|"]
        for i, item in enumerate(items, 1):
            rows.append(f"| SPEC-{i} | PRD-{i} | {item.replace('|', '/')} | TBD: observable acceptance criteria | Must |")
        spec_artifact.write_text("# Spec\n\n## Scope\n\n\n## Spec Items\n\n" + "\n".join(rows) + "\n\n## Edge Cases\n\n## Non-Goals\n\n## Open Questions\n", encoding="utf-8")

    if args.force or not trace_artifact.exists():
        rows = ["| PRD ID | Spec ID | Acceptance Criteria | Solution Section | Task ID | Code Files | Unit Tests | Status |", "|---|---|---|---|---|---|---|---|"]
        for i, _ in enumerate(items, 1):
            rows.append(f"| PRD-{i} | SPEC-{i} | TBD | | | | | specified |")
        trace_artifact.write_text("# Requirement Trace\n\n" + "\n".join(rows) + "\n", encoding="utf-8")

    update_checkpoint(folder, len(items), len(items))
    append_event(folder, "prd_parsed_to_spec", {"source": str(prd_path), "items": len(items)})
    print(json.dumps({"prd_file": str(prd_path), "folder": str(folder), "items": len(items)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
