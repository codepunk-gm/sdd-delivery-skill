#!/usr/bin/env python3
"""Unit tests for SDD Delivery core utility functions."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Add skill directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts._utils import is_filled, parse_markdown_table, parse_markdown_table_file, safe_feature_name
from scripts.parse_prd_to_spec import extract_items
from scripts.scan_test_coverage import is_test_file
from scripts.write_checkpoint import (
    add_human_review,
    default_checkpoint,
    load_checkpoint_or_default,
    normalize_capabilities,
    set_capability,
    set_milestone,
    set_quality,
)
from scripts.manage_capabilities import executor_plan, load_registry
from scripts.generate_dashboard import render_dashboard
from scripts.record_mcp_discovery import load_discovery, parse_record, render_selection
from scripts.setup_team_rules import default_rules, validate_rules


class TestSafeFeatureName(unittest.TestCase):
    """Tests for _utils.safe_feature_name."""

    def test_simple_name(self):
        self.assertEqual(safe_feature_name("login-rate-limit"), "login-rate-limit")

    def test_name_with_spaces(self):
        self.assertEqual(safe_feature_name("add login rate limit"), "add-login-rate-limit")

    def test_name_with_special_chars(self):
        self.assertEqual(safe_feature_name("用户登录@#$%限流"), "用户登录----限流")

    def test_name_with_trailing_special(self):
        self.assertEqual(safe_feature_name("feature..."), "feature")

    def test_name_with_leading_special(self):
        self.assertEqual(safe_feature_name("___leading"), "leading")

    def test_name_with_dots_and_underscores(self):
        self.assertEqual(safe_feature_name("v1.2.3_beta"), "v1.2.3_beta")

    def test_empty_string(self):
        self.assertEqual(safe_feature_name(""), "feature")

    def test_only_special_chars(self):
        self.assertEqual(safe_feature_name("@#$%"), "feature")

    def test_whitespace_name(self):
        self.assertEqual(safe_feature_name("   "), "feature")


class TestExtractItems(unittest.TestCase):
    """Tests for parse_prd_to_spec.extract_items."""

    def test_markdown_list_items(self):
        text = """## Requirements

- User must be able to login with email
- System shall support OAuth2
- Admin must be able to reset passwords
"""
        items = extract_items(text)
        self.assertGreaterEqual(len(items), 1)
        self.assertTrue(any("login" in i.lower() for i in items))

    def test_numbered_list_items(self):
        text = """## Features

1. User 必须能够注册账号
2. 系统 需要支持短信验证
3. 接口 must return JSON
"""
        items = extract_items(text)
        self.assertGreaterEqual(len(items), 1)

    def test_empty_input(self):
        items = extract_items("")
        self.assertEqual(items, [])

    def test_no_requirement_hints(self):
        text = """## Notes
- This is a note
- Another note
"""
        items = extract_items(text)
        # Items without requirement hints may still be captured as paragraphs
        # if the text has >= 20 char paragraphs
        for item in items:
            self.assertGreaterEqual(len(item), 4)

    def test_table_lines_skipped(self):
        text = """| PRD ID | Requirement | Priority |
|--------|-------------|----------|
| PRD-1  | Login       | Must     |

- User must be able to logout
"""
        items = extract_items(text)
        # Table lines should be skipped
        for item in items:
            self.assertFalse(item.startswith("|"))

    def test_chinese_requirement_hints(self):
        text = """## 需求
- 用户 需要能够修改密码
- 系统 必须支持导出报表
"""
        items = extract_items(text)
        self.assertGreaterEqual(len(items), 1)


class TestIsFilled(unittest.TestCase):
    """Tests for _utils.is_filled."""

    def test_non_empty_string(self):
        self.assertTrue(is_filled("login.py"))

    def test_tbd_is_empty(self):
        self.assertFalse(is_filled("TBD"))

    def test_pending_is_empty(self):
        self.assertFalse(is_filled("pending"))

    def test_na_is_empty(self):
        self.assertFalse(is_filled("N/A"))

    def test_dash_is_empty(self):
        self.assertFalse(is_filled("-"))

    def test_whitespace_only(self):
        self.assertFalse(is_filled("   "))

    def test_empty_string(self):
        self.assertFalse(is_filled(""))

    def test_case_insensitive_tbd(self):
        self.assertFalse(is_filled("tbd"))


class TestParseMarkdownTableFile(unittest.TestCase):
    """Tests for _utils.parse_markdown_table_file."""

    def test_simple_table(self):
        content = """# Trace Matrix

| PRD ID | Spec ID | Status |
|--------|---------|--------|
| PRD-1  | SPEC-1  | tested |
| PRD-2  | SPEC-2  | implemented |
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            rows = parse_markdown_table_file(temp_path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["PRD ID"], "PRD-1")
            self.assertEqual(rows[0]["Spec ID"], "SPEC-1")
            self.assertEqual(rows[0]["Status"], "tested")
            self.assertEqual(rows[1]["PRD ID"], "PRD-2")
        finally:
            temp_path.unlink()

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            rows = parse_markdown_table_file(temp_path)
            self.assertEqual(rows, [])
        finally:
            temp_path.unlink()

    def test_no_table(self):
        content = """# Just a heading

Some text without a table.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            rows = parse_markdown_table_file(temp_path)
            self.assertEqual(rows, [])
        finally:
            temp_path.unlink()


class TestIsTestFile(unittest.TestCase):
    """Tests for scan_test_coverage.is_test_file."""

    def test_python_test_file(self):
        self.assertTrue(is_test_file(Path("test_login.py")))

    def test_python_spec_file(self):
        self.assertTrue(is_test_file(Path("login_spec.py")))

    def test_typescript_test_file(self):
        self.assertTrue(is_test_file(Path("auth.test.ts")))

    def test_javascript_test_file(self):
        self.assertTrue(is_test_file(Path("utils.spec.js")))

    def test_in_tests_dir(self):
        # Path contains __tests__ so is_test_file should catch it
        self.assertTrue(is_test_file(Path("__tests__/login.ts")))

    def test_non_test_file(self):
        self.assertFalse(is_test_file(Path("login.py")))

    def test_non_test_extension(self):
        self.assertFalse(is_test_file(Path("test_config.yaml")))

    def test_non_code_file(self):
        self.assertFalse(is_test_file(Path("README.md")))

    def test_go_test_file(self):
        self.assertTrue(is_test_file(Path("handler_test.go")))

    def test_rust_test_file(self):
        self.assertTrue(is_test_file(Path("lib_spec.rs")))

    def test_java_test_file(self):
        self.assertTrue(is_test_file(Path("ServiceTest.java")))


class TestCheckpointDefaults(unittest.TestCase):
    """Tests for write_checkpoint checkpoint loading defaults."""

    def test_missing_checkpoint_returns_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir) / "feature-a"
            folder.mkdir()
            checkpoint = load_checkpoint_or_default(folder / "11-checkpoint.json")

        self.assertEqual(checkpoint["feature"], "feature-a")
        self.assertEqual(checkpoint["gate_status"]["solution_approval"], "pending")
        self.assertEqual(checkpoint["preferences"]["delivery_language"], "auto")
        self.assertEqual(checkpoint["solution_approval"]["status"], "pending")
        self.assertEqual(checkpoint["capabilities"]["frontend_template"]["state"], "ask")

    def test_default_checkpoint_has_capability_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint = default_checkpoint(Path(temp_dir) / "feature-b")

        self.assertIn("enabled_capabilities", checkpoint)
        self.assertIn("capabilities", checkpoint)
        self.assertIn("preferences", checkpoint)
        self.assertIn("solution_approval", checkpoint)

    def test_default_checkpoint_has_human_coordination_fields(self):
        checkpoint = default_checkpoint(Path("feature-human-review"))

        self.assertEqual([item["id"] for item in checkpoint["milestones"]], ["M1", "M2", "M3", "M4", "M5"])
        self.assertIn("human_reviews", checkpoint)
        self.assertEqual(checkpoint["quality_status"]["progress"], "pending")
        self.assertEqual(checkpoint["quality_status"]["delivery_confidence"], "pending")

    def test_human_review_updates_checkpoint(self):
        checkpoint = default_checkpoint(Path("feature-human-review"))

        set_milestone(checkpoint, "M2=reviewed:老板:方案可进入实现")
        add_human_review(checkpoint, "老板::M2::pass::方案和风险已确认")
        set_quality(checkpoint, "review_readiness=ready")

        milestone = next(item for item in checkpoint["milestones"] if item["id"] == "M2")
        self.assertEqual(milestone["status"], "reviewed")
        self.assertEqual(milestone["reviewer"], "老板")
        self.assertTrue(any(review["target"] == "M2" for review in checkpoint["human_reviews"]))
        self.assertEqual(checkpoint["quality_status"]["review_readiness"], "ready")

    def test_legacy_enabled_capabilities_migrate_to_structured_switches(self):
        checkpoint = default_checkpoint(Path("feature-c"))
        checkpoint["enabled_capabilities"] = ["frontend_template"]
        checkpoint.pop("capabilities")

        normalize_capabilities(checkpoint)

        self.assertEqual(checkpoint["capabilities"]["frontend_template"]["state"], "enabled")
        self.assertEqual(checkpoint["enabled_capabilities"], ["frontend_template"])

    def test_set_capability_disabled_updates_structured_switch(self):
        checkpoint = default_checkpoint(Path("feature-d"))

        set_capability(checkpoint, "mcp_component_protocol=disabled:not used by this repo")

        self.assertEqual(checkpoint["capabilities"]["mcp_component_protocol"]["state"], "disabled")
        self.assertEqual(checkpoint["capabilities"]["mcp_component_protocol"]["reason"], "not used by this repo")
        self.assertNotIn("mcp_component_protocol", checkpoint["enabled_capabilities"])

    def test_set_capability_without_state_enables_legacy_style(self):
        checkpoint = default_checkpoint(Path("feature-e"))

        set_capability(checkpoint, "java_modular_project")

        self.assertEqual(checkpoint["capabilities"]["java_modular_project"]["state"], "enabled")
        self.assertIn("java_modular_project", checkpoint["enabled_capabilities"])


class TestCapabilityRegistry(unittest.TestCase):
    """Tests for capability adapter/executor registry."""

    def test_registry_has_executor_config(self):
        registry = load_registry()

        self.assertIn("frontend_template", registry)
        self.assertEqual(registry["frontend_template"]["executor"]["type"], "phase-instructions")

    def test_executor_plan_uses_enabled_capabilities_only(self):
        checkpoint = default_checkpoint(Path("feature-f"))
        registry = load_registry()
        set_capability(checkpoint, "frontend_template=enabled")
        set_capability(checkpoint, "mcp_component_protocol=disabled")

        plan = executor_plan(checkpoint, registry)

        self.assertEqual([item["id"] for item in plan], ["frontend_template"])


class TestMcpDiscovery(unittest.TestCase):
    """Tests for MCP discovery evidence helpers."""

    def test_parse_record_supports_name_source_status_notes(self):
        record = parse_record("DataTable::design-system::available::Use for dashboard", "component")

        self.assertEqual(record["name"], "DataTable")
        self.assertEqual(record["source"], "design-system")
        self.assertEqual(record["status"], "available")
        self.assertEqual(record["notes"], "Use for dashboard")
        self.assertEqual(record["type"], "component")

    def test_load_discovery_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir) / "feature-mcp"
            folder.mkdir()
            discovery = load_discovery(folder)

        self.assertEqual(discovery["feature"], "feature-mcp")
        self.assertEqual(discovery["status"], "not_started")
        self.assertEqual(discovery["servers"], [])

    def test_render_selection_includes_discovered_component(self):
        discovery = {
            "servers": [],
            "tools": [],
            "components": [parse_record("DataTable::design-system::available::Use for dashboard", "component")],
            "unavailable": [],
        }

        text = render_selection(discovery)

        self.assertIn("DataTable", text)
        self.assertIn("## 选择决策", text)


class TestDashboardGeneration(unittest.TestCase):
    """Tests for static dashboard generation."""

    def test_dashboard_renders_checkpoint_and_escapes_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir) / "feature-dashboard"
            folder.mkdir()
            checkpoint = default_checkpoint(folder)
            checkpoint["feature"] = "feature-dashboard"
            checkpoint["goal"] = "<script>alert(1)</script>"
            checkpoint["current_phase"] = "technical-solution"
            checkpoint["next_action"] = "Review solution"
            (folder / "11-checkpoint.json").write_text(
                __import__("json").dumps(checkpoint, ensure_ascii=False),
                encoding="utf-8",
            )

            html = render_dashboard(folder)

        self.assertIn("SDD Delivery Dashboard", html)
        self.assertIn("feature-dashboard", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_dashboard_includes_mcp_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir) / "feature-dashboard-mcp"
            folder.mkdir()
            checkpoint = default_checkpoint(folder)
            set_capability(checkpoint, "mcp_component_protocol=enabled")
            (folder / "11-checkpoint.json").write_text(
                __import__("json").dumps(checkpoint, ensure_ascii=False),
                encoding="utf-8",
            )
            (folder / "mcp-discovery.json").write_text(
                __import__("json").dumps({
                    "status": "available",
                    "source": "test",
                    "servers": [{"name": "design-system"}],
                    "tools": [],
                    "components": [{"name": "DataTable"}],
                    "unavailable": [],
                }, ensure_ascii=False),
                encoding="utf-8",
            )

            html = render_dashboard(folder)

        self.assertIn("MCP Evidence", html)
        self.assertIn("available", html)
        self.assertIn("2", html)


class TestTeamRules(unittest.TestCase):
    """Tests for structured team rule setup and validation."""

    def test_default_rules_are_valid(self):
        issues, warnings = validate_rules(default_rules())

        self.assertEqual(issues, [])

    def test_invalid_threshold_is_rejected(self):
        rules = default_rules()
        rules["thresholds"]["max_params"] = 0

        issues, _ = validate_rules(rules)

        self.assertTrue(any("max_params" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
