#!/usr/bin/env python3
"""Unit tests for SDD Delivery core utility functions."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts._utils import is_filled, parse_markdown_table, parse_markdown_table_file, safe_feature_name
from scripts.parse_prd_to_spec import extract_items
from scripts.scan_test_coverage import is_test_file


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


if __name__ == "__main__":
    unittest.main()
