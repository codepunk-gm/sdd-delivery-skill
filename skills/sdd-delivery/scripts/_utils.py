#!/usr/bin/env python3
"""Shared utilities for SDD Delivery scripts. No side-effects on import."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    """Read and parse a JSON file. Returns empty dict if missing or invalid."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return {}


def write_json(path: Path, data: dict) -> None:
    """Write a dict as UTF-8 JSON with standard formatting."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_event(folder: Path, event: str, detail: dict) -> None:
    """Append a structured event line to events.jsonl."""
    payload = {"time": now(), "event": event, "detail": detail}
    with (folder / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def add_unique(items: list, values: list[str]) -> None:
    """Extend list with non-empty, non-duplicate string values."""
    for value in values:
        if value and value not in items:
            items.append(value)


def parse_markdown_table(lines: list[str]) -> tuple[list[str], list[dict]]:
    """Parse a markdown table from a list of lines.

    Returns (header, rows) where rows is a list of dicts keyed by header names.
    Lines not starting with '|' and separator lines ('---') are skipped.
    """
    header: list[str] = []
    rows: list[dict] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not header:
            header = cells
        elif len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return header, rows


def parse_markdown_table_file(path: Path) -> list[dict]:
    """Parse a markdown table from a file. Returns list of row dicts."""
    _, rows = parse_markdown_table(path.read_text(encoding="utf-8-sig").splitlines())
    return rows


def is_filled(value: str) -> bool:
    """Return True if value is non-empty and not a placeholder."""
    return bool(value and value.strip() and value.strip().lower() not in {"tbd", "pending", "n/a", "-"})


def safe_feature_name(name: str) -> str:
    """Sanitize a feature name for use as a filesystem directory."""
    return "".join(c if c.isalnum() or c in "._-" else "-" for c in name.strip()).strip("-._") or "feature"
