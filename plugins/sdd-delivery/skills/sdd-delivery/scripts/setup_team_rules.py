#!/usr/bin/env python3
"""Initialize and validate SDD Delivery team rules."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from _utils import load_json, write_json
except ImportError:
    from scripts._utils import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "templates" / "team-rules.json"
VALID_LANGUAGES = {"auto", "zh", "en", "bilingual"}
PRINCIPLE_KEYS = {"design_patterns", "extensibility", "size_limits", "naming", "error_handling", "review_checklist"}
THRESHOLD_KEYS = {"max_file_lines", "max_test_file_lines", "max_function_lines", "max_test_case_lines", "max_params", "max_constructor_deps", "max_imports"}


def default_rules() -> dict:
    return load_json(TEMPLATE)


def team_rules_path(root: Path) -> Path:
    return root / ".sdd-delivery" / "team-rules.json"


def validate_rules(data: dict) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    if data.get("delivery_language") not in VALID_LANGUAGES:
        issues.append("delivery_language must be auto, zh, en, or bilingual")
    if data.get("comment_language") not in VALID_LANGUAGES:
        issues.append("comment_language must be auto, zh, en, or bilingual")

    principles = data.get("code_principles", {})
    if not isinstance(principles, dict):
        issues.append("code_principles must be an object")
    else:
        for key in PRINCIPLE_KEYS:
            if key not in principles:
                issues.append(f"missing code principle: {key}")
            elif not isinstance(principles[key], bool):
                issues.append(f"code principle must be boolean: {key}")

    thresholds = data.get("thresholds", {})
    if not isinstance(thresholds, dict):
        issues.append("thresholds must be an object")
    else:
        for key in THRESHOLD_KEYS:
            value = thresholds.get(key)
            if not isinstance(value, int) or value <= 0:
                issues.append(f"threshold must be positive integer: {key}")
        if isinstance(thresholds.get("max_file_lines"), int) and thresholds["max_file_lines"] > 500:
            warnings.append("max_file_lines is high; review may become harder")
        if isinstance(thresholds.get("max_params"), int) and thresholds["max_params"] > 8:
            warnings.append("max_params is high; consider config objects for readability")

    return issues, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or validate .sdd-delivery/team-rules.json.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--init", action="store_true", help="Create team-rules.json if missing.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing team-rules.json when used with --init.")
    parser.add_argument("--language", choices=sorted(VALID_LANGUAGES), help="Set delivery_language and comment_language.")
    parser.add_argument("--test-framework", help="Set preferred test framework.")
    parser.add_argument("--coverage-target", help="Set coverage target, for example 80% line coverage.")
    parser.add_argument("--principle", action="append", default=[], help="Set principle as name=true|false.")
    parser.add_argument("--validate", action="store_true", help="Validate team-rules.json.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    path = team_rules_path(root)
    data = load_json(path) if path.exists() else default_rules()

    if args.init:
        if path.exists() and not args.force:
            pass
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            data = default_rules()

    if args.language:
        data["delivery_language"] = args.language
        data["comment_language"] = args.language
    if args.test_framework:
        data["test_framework"] = args.test_framework
    if args.coverage_target:
        data["coverage_target"] = args.coverage_target
    for item in args.principle:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        key = key.strip()
        if key in PRINCIPLE_KEYS:
            data.setdefault("code_principles", {})[key] = value.strip().lower() == "true"

    if args.init or args.language or args.test_framework or args.coverage_target or args.principle:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, data)

    issues, warnings = validate_rules(data)
    result = {"path": str(path), "ok": not issues, "issues": issues, "warnings": warnings, "rules": data}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
