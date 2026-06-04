#!/usr/bin/env python3
"""Calculate requirement trace coverage and update checkpoint metrics."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_table(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    rows = []
    header = []
    for line in lines:
        if not line.strip().startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not header:
            header = cells
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def filled(value: str) -> bool:
    return bool(value and value.strip() and value.strip().lower() not in {"tbd", "pending", "n/a", "-"})


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate SDD trace coverage.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--json", action="store_true", help="Only print JSON")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    trace = folder / "03-requirement-trace.md"
    rows = parse_table(trace)
    total = len(rows)
    solution = sum(1 for r in rows if filled(r.get("Solution Section", "")))
    tasks = sum(1 for r in rows if filled(r.get("Task ID", "")))
    code = sum(1 for r in rows if filled(r.get("Code Files", "")))
    tests = sum(1 for r in rows if filled(r.get("Unit Tests", "")))
    tested_status = sum(1 for r in rows if r.get("Status", "").strip().lower() == "tested")
    result = {
        "trace_items_total": total,
        "solution_covered": solution,
        "task_covered": tasks,
        "code_covered": code,
        "test_covered": tests,
        "tested_status": tested_status,
        "solution_coverage_rate": round(solution / total, 4) if total else 0,
        "task_coverage_rate": round(tasks / total, 4) if total else 0,
        "code_coverage_rate": round(code / total, 4) if total else 0,
        "unit_test_coverage_rate": round(tests / total, 4) if total else 0,
    }

    checkpoint = folder / "11-checkpoint.json"
    if checkpoint.exists():
        data = json.loads(checkpoint.read_text(encoding="utf-8-sig"))
        metrics = data.setdefault("metrics", {})
        metrics.update(result)
        metrics["trace_items_tested"] = tests
        data["updated_at"] = now()
        checkpoint.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    out = folder / "trace-coverage.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not args.json:
        print("# Trace Coverage")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
