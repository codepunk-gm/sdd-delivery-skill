#!/usr/bin/env python3
"""Summarize command or tool output for safer context loading."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ERROR_PATTERNS = [
    re.compile(r"error", re.I),
    re.compile(r"failed", re.I),
    re.compile(r"exception", re.I),
    re.compile(r"traceback", re.I),
    re.compile(r"panic", re.I),
]


def read_input(path: str) -> str:
    if path == "-":
        import sys
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def pick_lines(lines: list[str], limit: int) -> list[str]:
    selected = []
    seen = set()

    def add(index: int) -> None:
        if 0 <= index < len(lines) and index not in seen:
            seen.add(index)
            selected.append((index, lines[index]))

    for i, line in enumerate(lines):
        if any(p.search(line) for p in ERROR_PATTERNS):
            for j in range(i - 2, i + 6):
                add(j)

    if not selected:
        for i in range(min(len(lines), limit)):
            add(i)

    selected = sorted(selected, key=lambda item: item[0])[:limit]
    return [f"L{idx + 1}: {line}" for idx, line in selected]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize large output for context use.")
    parser.add_argument("input", help="Input file or '-' for stdin")
    parser.add_argument("--type", choices=["test", "build", "search", "diff", "log", "generic"], default="generic")
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()

    text = read_input(args.input)
    lines = text.splitlines()
    selected = pick_lines(lines, args.limit)

    print(f"# Tool Output Summary")
    print(f"")
    print(f"Type: {args.type}")
    print(f"Total lines: {len(lines)}")
    print(f"Selected lines: {len(selected)}")
    print(f"")
    print("## Relevant Output")
    for line in selected:
        print(line[:1000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
