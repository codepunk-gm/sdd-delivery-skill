#!/usr/bin/env python3
"""Generate GitHub PR and CI assets for SDD Delivery."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PR_TEMPLATE = """# Summary\n\n## SDD Delivery Artifacts\n\n- Feature folder: `.op/devflow/<feature>`\n- Spec: `.op/devflow/<feature>/01-spec.md`\n- Trace: `.op/devflow/<feature>/03-requirement-trace.md`\n- Solution: `.op/devflow/<feature>/04-tech-solution.md`\n- Unit test report: `.op/devflow/<feature>/09-unit-test-report.md`\n\n## Gates\n\n- [ ] Spec Review passed or accepted risk documented\n- [ ] Solution Review passed or accepted risk documented\n- [ ] Unit Test Plan completed\n- [ ] Unit Test Report completed\n- [ ] Delivery Review completed\n\n## Verification\n\nCommands run:\n\n```text\n\n```\n\n## Risks / Follow-ups\n\n"""

WORKFLOW = """name: SDD Delivery Artifacts\n\non:\n  pull_request:\n    paths:\n      - '.op/devflow/**'\n      - '.github/scripts/validate_devflow_artifacts.py'\n\njobs:\n  validate-devflow-artifacts:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.x'\n      - name: Validate DevFlow artifact folders\n        shell: bash\n        run: |\n          set -euo pipefail\n          shopt -s nullglob\n          found=0\n          for folder in .op/devflow/*; do\n            if [ -d \"$folder\" ]; then\n              found=1\n              python .github/scripts/validate_devflow_artifacts.py \"$folder\"\n            fi\n          done\n          if [ \"$found\" -eq 0 ]; then\n            echo \"No .op/devflow artifacts found; skipping.\"\n          fi\n"""


def write(path: Path, content: str, force: bool, written: list[str]) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    written.append(str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GitHub PR template and CI workflow.")
    parser.add_argument("project_root", help="Repository root")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    written: list[str] = []
    write(root / ".github" / "pull_request_template.md", PR_TEMPLATE, args.force, written)
    write(root / ".github" / "workflows" / "sdd-delivery-artifacts.yml", WORKFLOW, args.force, written)
    validator = (ROOT / "scripts" / "validate_artifacts.py").read_text(encoding="utf-8-sig")
    write(root / ".github" / "scripts" / "validate_devflow_artifacts.py", validator, args.force, written)
    print("\n".join(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
