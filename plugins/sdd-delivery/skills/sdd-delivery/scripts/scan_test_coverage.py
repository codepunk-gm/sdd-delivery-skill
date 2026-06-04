#!/usr/bin/env python3
"""Scan test files for Spec IDs and optionally update trace/report artifacts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SPEC_RE = re.compile(r"SPEC-\d+", re.I)
TEST_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".cs", ".rb", ".php"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_test_file(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in TEST_EXTS and ("test" in name or "spec" in name or "__tests__" in str(path).lower())


def scan(root: Path) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for path in root.rglob("*"):
        if ".git" in path.parts or ".sdd-delivery" in path.parts or ".github" in path.parts:
            continue
        if not path.is_file() or not is_test_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for match in sorted(set(m.upper() for m in SPEC_RE.findall(text))):
            mapping.setdefault(match, []).append(str(path.relative_to(root)))
    return mapping


def update_report(folder: Path, mapping: dict[str, list[str]]) -> None:
    report = folder / "09-unit-test-report.md"
    lines = ["# Unit Test Report", "", "## Commands", "", "| Time | Command | Status | Summary |", "|---|---|---|---|", "", "## Reverse Spec Coverage From Test Files", "", "| Spec ID | Test Files |", "|---|---|"]
    for spec_id, files in sorted(mapping.items()):
        lines.append(f"| {spec_id} | {'<br>'.join(files)} |")
    lines.extend(["", "## Failed Tests", "", "## Coverage Gaps", "", "| Spec ID | Reason | Accepted By |", "|---|---|---|"])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_table(lines: list[str]) -> tuple[list[str], list[dict], list[str]]:
    header: list[str] = []
    rows: list[dict] = []
    other: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            other.append(line)
            continue
        if "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not header:
            header = cells
        elif len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return header, rows, other


def update_trace(folder: Path, mapping: dict[str, list[str]]) -> None:
    trace = folder / "03-requirement-trace.md"
    if not trace.exists():
        return
    header, rows, _ = parse_table(trace.read_text(encoding="utf-8-sig").splitlines())
    if not header or not rows:
        return
    if "Unit Tests" not in header:
        header.append("Unit Tests")
    if "Status" not in header:
        header.append("Status")
    for row in rows:
        spec_id = row.get("Spec ID", "").strip().upper()
        if spec_id in mapping:
            row["Unit Tests"] = "<br>".join(mapping[spec_id])
            if row.get("Status", "").strip().lower() in {"", "pending", "specified", "implemented"}:
                row["Status"] = "tested"
    out = ["# Requirement Trace", "", "| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(row.get(col, "") for col in header) + " |")
    trace.write_text("\n".join(out) + "\n", encoding="utf-8")


def update_checkpoint(folder: Path, mapping: dict[str, list[str]]) -> None:
    checkpoint = folder / "11-checkpoint.json"
    if not checkpoint.exists():
        return
    data = json.loads(checkpoint.read_text(encoding="utf-8-sig"))
    metrics = data.setdefault("metrics", {})
    metrics["reverse_test_specs_found"] = len(mapping)
    metrics["trace_items_tested"] = len(mapping)
    data["updated_at"] = now()
    checkpoint.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_event(folder: Path, mapping: dict[str, list[str]]) -> None:
    with (folder / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"time": now(), "event": "test_coverage_scanned", "detail": {"covered_specs": len(mapping)}}, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan test files for SPEC-* references.")
    parser.add_argument("project_root", help="Project root to scan")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--update-report", action="store_true")
    parser.add_argument("--update-trace", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    folder = Path(args.folder).resolve()
    mapping = scan(root)
    result = {"project_root": str(root), "covered_specs": len(mapping), "mapping": mapping}
    (folder / "test-spec-coverage.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.update_report:
        update_report(folder, mapping)
    if args.update_trace:
        update_trace(folder, mapping)
    update_checkpoint(folder, mapping)
    append_event(folder, mapping)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
