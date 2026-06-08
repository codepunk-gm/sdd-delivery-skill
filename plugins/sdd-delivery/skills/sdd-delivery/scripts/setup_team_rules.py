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
SQL_QUERY_RULE_KEYS = {
    "forbid_select_star",
    "require_parameterized_query",
    "require_limit_for_pagination",
    "require_order_by_for_pagination",
    "require_index_for_filter_columns",
    "forbid_string_concatenated_sql",
}
SQL_MIGRATION_RULE_KEYS = {
    "migration_required_for_schema_change",
    "backfill_plan_required",
    "rollback_plan_required",
    "avoid_destructive_change_without_approval",
}
SQL_TRANSACTION_RULE_KEYS = {
    "explicit_transaction_for_multi_write",
    "document_locking_strategy",
}
SQL_RULE_GROUPS = {
    "query": "query_rules",
    "query_rules": "query_rules",
    "migration": "migration_rules",
    "migration_rules": "migration_rules",
    "transaction": "transaction_rules",
    "transaction_rules": "transaction_rules",
}


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

    validate_sql_standards(data.get("sql_standards", {}), issues, warnings)

    return issues, warnings


def require_bool_fields(container: dict, keys: set[str], prefix: str, issues: list[str]) -> None:
    for key in keys:
        if key not in container:
            issues.append(f"missing {prefix}: {key}")
        elif not isinstance(container[key], bool):
            issues.append(f"{prefix} must be boolean: {key}")


def validate_sql_standards(sql: object, issues: list[str], warnings: list[str]) -> None:
    if not isinstance(sql, dict):
        issues.append("sql_standards must be an object")
        return
    if "enabled" not in sql:
        issues.append("sql_standards missing field: enabled")
    elif not isinstance(sql["enabled"], bool):
        issues.append("sql_standards.enabled must be boolean")

    scope_order = sql.get("scope_order", [])
    if not isinstance(scope_order, list) or scope_order != ["global", "project", "feature_exception"]:
        issues.append("sql_standards.scope_order must be ['global', 'project', 'feature_exception']")

    global_rules = sql.get("global", {})
    if not isinstance(global_rules, dict):
        issues.append("sql_standards.global must be an object")
    else:
        query_rules = global_rules.get("query_rules", {})
        migration_rules = global_rules.get("migration_rules", {})
        transaction_rules = global_rules.get("transaction_rules", {})
        if not isinstance(query_rules, dict):
            issues.append("sql_standards.global.query_rules must be an object")
        else:
            require_bool_fields(query_rules, SQL_QUERY_RULE_KEYS, "sql query rule", issues)
        if not isinstance(migration_rules, dict):
            issues.append("sql_standards.global.migration_rules must be an object")
        else:
            require_bool_fields(migration_rules, SQL_MIGRATION_RULE_KEYS, "sql migration rule", issues)
        if not isinstance(transaction_rules, dict):
            issues.append("sql_standards.global.transaction_rules must be an object")
        else:
            require_bool_fields(transaction_rules, SQL_TRANSACTION_RULE_KEYS, "sql transaction rule", issues)

    project_overrides = sql.get("project_overrides", {})
    if not isinstance(project_overrides, dict):
        issues.append("sql_standards.project_overrides must be an object")
    else:
        allowed_legacy = project_overrides.get("allowed_legacy_exceptions", [])
        if not isinstance(allowed_legacy, list):
            issues.append("sql_standards.project_overrides.allowed_legacy_exceptions must be a list")

    feature_exceptions = sql.get("feature_exceptions", [])
    if not isinstance(feature_exceptions, list):
        issues.append("sql_standards.feature_exceptions must be a list")
    else:
        for index, exception in enumerate(feature_exceptions, start=1):
            if not isinstance(exception, dict):
                issues.append(f"sql_standards.feature_exceptions[{index}] must be an object")
                continue
            for field in ["rule", "reason", "approver", "expires"]:
                if not exception.get(field):
                    issues.append(f"sql_standards.feature_exceptions[{index}] missing field: {field}")
            if not exception.get("scope"):
                warnings.append(f"sql_standards.feature_exceptions[{index}] missing scope; keep exceptions narrow")


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on", "enabled"}:
        return True
    if normalized in {"false", "0", "no", "off", "disabled"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def ensure_sql_standards(data: dict) -> dict:
    sql = data.setdefault("sql_standards", {})
    if not isinstance(sql, dict):
        sql = default_rules()["sql_standards"]
        data["sql_standards"] = sql
    template = default_rules()["sql_standards"]
    sql.setdefault("enabled", template["enabled"])
    sql.setdefault("scope_order", template["scope_order"])
    sql.setdefault("global", template["global"])
    sql.setdefault("project_overrides", template["project_overrides"])
    sql.setdefault("feature_exceptions", template["feature_exceptions"])
    return sql


def parse_sql_rule(item: str) -> tuple[str, str, bool]:
    if "=" not in item:
        raise argparse.ArgumentTypeError("expected group.rule=true|false")
    target, raw_value = item.split("=", 1)
    if "." not in target:
        raise argparse.ArgumentTypeError("expected group.rule=true|false")
    group_alias, key = target.split(".", 1)
    group = SQL_RULE_GROUPS.get(group_alias.strip())
    if not group:
        raise argparse.ArgumentTypeError("unknown SQL rule group")
    expected = {
        "query_rules": SQL_QUERY_RULE_KEYS,
        "migration_rules": SQL_MIGRATION_RULE_KEYS,
        "transaction_rules": SQL_TRANSACTION_RULE_KEYS,
    }[group]
    key = key.strip()
    if key not in expected:
        raise argparse.ArgumentTypeError(f"unknown SQL rule: {key}")
    return group, key, parse_bool(raw_value)


def parse_legacy_exception(item: str) -> dict:
    parts = [part.strip() for part in item.split("::")]
    if len(parts) != 3 or not all(parts):
        raise argparse.ArgumentTypeError("expected object::rule::reason")
    return {"object": parts[0], "rule": parts[1], "reason": parts[2]}


def parse_feature_exception(item: str) -> dict:
    parts = [part.strip() for part in item.split("::")]
    if len(parts) != 5 or not all(parts):
        raise argparse.ArgumentTypeError("expected rule::scope::reason::approver::expires")
    return {
        "rule": parts[0],
        "scope": parts[1],
        "reason": parts[2],
        "approver": parts[3],
        "expires": parts[4],
    }


def apply_sql_updates(data: dict, args: argparse.Namespace) -> bool:
    changed = False
    sql = ensure_sql_standards(data)

    if args.sql_enabled is not None:
        sql["enabled"] = args.sql_enabled
        changed = True

    project_overrides = sql.setdefault("project_overrides", {})
    for attr, key in [
        ("sql_dialect", "dialect"),
        ("sql_schema", "schema"),
        ("sql_table_prefix", "table_prefix"),
        ("sql_migration_tool", "migration_tool"),
    ]:
        value = getattr(args, attr)
        if value is not None:
            project_overrides[key] = value
            changed = True

    global_rules = sql.setdefault("global", {})
    for group, key, value in args.sql_rule:
        global_rules.setdefault(group, {})[key] = value
        changed = True

    if args.sql_allow_legacy:
        project_overrides.setdefault("allowed_legacy_exceptions", []).extend(args.sql_allow_legacy)
        changed = True

    if args.sql_feature_exception:
        sql.setdefault("feature_exceptions", []).extend(args.sql_feature_exception)
        changed = True

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or validate .sdd-delivery/team-rules.json.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--init", action="store_true", help="Create team-rules.json if missing.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing team-rules.json when used with --init.")
    parser.add_argument("--language", choices=sorted(VALID_LANGUAGES), help="Set delivery_language and comment_language.")
    parser.add_argument("--test-framework", help="Set preferred test framework.")
    parser.add_argument("--coverage-target", help="Set coverage target, for example 80% line coverage.")
    parser.add_argument("--principle", action="append", default=[], help="Set principle as name=true|false.")
    parser.add_argument("--sql-enabled", type=parse_bool, help="Enable or disable SQL standards.")
    parser.add_argument("--sql-dialect", help="Set project SQL dialect, for example postgresql, mysql, sqlite, or oracle.")
    parser.add_argument("--sql-schema", help="Set project SQL schema or database namespace.")
    parser.add_argument("--sql-table-prefix", help="Set project SQL table prefix.")
    parser.add_argument("--sql-migration-tool", help="Set project migration tool, for example alembic, flyway, liquibase, or prisma.")
    parser.add_argument("--sql-rule", action="append", default=[], type=parse_sql_rule, help="Set a global SQL boolean rule as group.rule=true|false. Groups: query, migration, transaction.")
    parser.add_argument("--sql-allow-legacy", action="append", default=[], type=parse_legacy_exception, help="Add a project legacy exception as object::rule::reason.")
    parser.add_argument("--sql-feature-exception", action="append", default=[], type=parse_feature_exception, help="Add a feature SQL exception as rule::scope::reason::approver::expires.")
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
    sql_changed = apply_sql_updates(data, args)

    if args.init or args.language or args.test_framework or args.coverage_target or args.principle or sql_changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, data)

    issues, warnings = validate_rules(data)
    result = {"path": str(path), "ok": not issues, "issues": issues, "warnings": warnings, "rules": data}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
