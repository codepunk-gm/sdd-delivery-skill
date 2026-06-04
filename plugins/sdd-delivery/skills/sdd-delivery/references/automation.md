# Automation

Bundled scripts provide deterministic support around the agent workflow.

## parse_prd_to_spec.py

Rule-based PRD parser that extracts requirement-like bullets/headings and creates:

- `00-prd.md`
- `01-spec.md`
- `03-requirement-trace.md`

The generated Spec is a draft. The agent must still review and improve acceptance criteria.

## trace_coverage.py

Reads `03-requirement-trace.md` and calculates:

- solution coverage
- task coverage
- code coverage
- unit test coverage

Updates `11-checkpoint.json` and writes `trace-coverage.json`.

## scan_test_coverage.py

Scans test files for `SPEC-*` references and writes `test-spec-coverage.json`. Use `--update-report --update-trace` to update the unit test report and requirement trace matrix.

## generate_github_assets.py

Creates a PR template and GitHub Actions workflow for artifact validation.

## sync_observability.py

Synchronizes 12-observability.md from checkpoint, trace coverage, and test coverage artifacts.

