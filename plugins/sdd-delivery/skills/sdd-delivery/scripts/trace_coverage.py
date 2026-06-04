#!/usr/bin/env python3
"""Calculate requirement trace coverage and update checkpoint metrics."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import is_filled, now, parse_markdown_table_file, write_json
except ImportError:
    from scripts._utils import is_filled, now, parse_markdown_table_file, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate SDD trace coverage.")
    parser.add_argument("folder", help="Feature artifact folder")
    parser.add_argument("--json", action="store_true", help="Only print JSON")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    trace = folder / "03-requirement-trace.md"
    rows = parse_markdown_table_file(trace)
    total = len(rows)
    solution = sum(1 for r in rows if is_filled(r.get("Solution Section", "")))
    tasks = sum(1 for r in rows if is_filled(r.get("Task ID", "")))
    code = sum(1 for r in rows if is_filled(r.get("Code Files", "")))
    tests = sum(1 for r in rows if is_filled(r.get("Unit Tests", "")))
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
        write_json(checkpoint, data)

    out = folder / "trace-coverage.json"
    write_json(out, result)
    if not args.json:
        print("# Trace Coverage")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
