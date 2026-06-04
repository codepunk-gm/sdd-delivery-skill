#!/usr/bin/env python3
"""Sync the canonical skills/ directory to the plugin mirror at plugins/sdd-delivery/skills/.

Edit files under plugins/sdd-delivery/skills/sdd-delivery/, then run this script
to sync changes to skills/sdd-delivery/ at the repo root.

Usage: python scripts/sync_mirror.py [--check] [--from-canonical]
  --check           Only report differences, don't sync.
  --from-canonical  Sync from skills/ → plugin/ (default: plugin/ → skills/).
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SKILL = REPO_ROOT / "plugins" / "sdd-delivery" / "skills" / "sdd-delivery"
CANONICAL = REPO_ROOT / "skills" / "sdd-delivery"

EXCLUDE_DIRS = {"__pycache__", ".git", ".idea"}


def iter_files(root: Path) -> list[Path]:
    """List all files under root, excluding generated/cache dirs."""
    files = []
    for path in root.rglob("*"):
        if any(d in path.parts for d in EXCLUDE_DIRS):
            continue
        if path.is_file():
            files.append(path.relative_to(root))
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync plugin mirror ↔ canonical skill directory.")
    parser.add_argument("--check", action="store_true", help="Only report differences.")
    parser.add_argument("--from-canonical", action="store_true", help="Sync from skills/ → plugin/ (default: plugin/ → skills/).")
    args = parser.parse_args()

    if not PLUGIN_SKILL.exists():
        print(f"Plugin skill not found: {PLUGIN_SKILL}")
        return 1

    plugin_files = set(iter_files(PLUGIN_SKILL))
    canon_files = set(iter_files(CANONICAL))

    only_plugin = plugin_files - canon_files
    only_canon = canon_files - plugin_files
    common = plugin_files & canon_files
    diffs = {
        f for f in common
        if not filecmp.cmp(
            PLUGIN_SKILL / f, CANONICAL / f,
            shallow=False,
        )
    }

    if only_plugin:
        print(f"Only in plugin/: {sorted(str(f) for f in only_plugin)}")
    if only_canon:
        print(f"Only in skills/: {sorted(str(f) for f in only_canon)}")
    if diffs:
        print(f"Differ: {sorted(str(f) for f in diffs)}")

    if args.check:
        changes = len(only_plugin) + len(only_canon) + len(diffs)
        print(f"\n{changes} change(s) detected.")
        return 1 if changes else 0

    if args.from_canonical:
        src_root, dst_root = CANONICAL, PLUGIN_SKILL
        src_label, dst_label = "skills/", "plugin/"
        src_only, _ = only_canon, only_plugin
        # For canonical→plugin: also sync diffs from canonical to plugin
        sync_from_src = diffs | only_canon
        sync_from_dst = only_plugin
    else:
        src_root, dst_root = PLUGIN_SKILL, CANONICAL
        src_label, dst_label = "plugin/", "skills/"
        src_only, _ = only_plugin, only_canon
        sync_from_src = diffs | only_plugin
        sync_from_dst = only_canon

    for f in sync_from_src:
        src = src_root / f
        dst = dst_root / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  {src_label} → {dst_label}: {f}")

    for f in sync_from_dst:
        src = dst_root / f
        dst = src_root / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  {dst_label} → {src_label}: {f}")

    if not (diffs or only_plugin or only_canon):
        print("Already in sync.")
    else:
        direction = "skills → plugin" if args.from_canonical else "plugin → skills"
        print(f"\nSync complete ({direction}).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
