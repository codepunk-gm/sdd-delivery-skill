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

Synchronizes `12-observability.md` from checkpoint, trace coverage, and test coverage artifacts.

## init_artifacts.py

Initializes a feature artifact directory under `.sdd-delivery/<feature>/` by copying all templates from `assets/templates/`. Creates the `events.jsonl` file and writes an initialization event.

Usage: `python scripts/init_artifacts.py <feature-name> [--root .] [--force]`

The agent should run this once per feature before any other artifact work. In No-Python mode, create the directory and template files manually.

## write_checkpoint.py

Updates `11-checkpoint.json` with structured field changes. Supports `--phase`, `--task`, `--gate`, `--metric`, `--complete`, `--pending`, `--changed-file`, `--risk`, `--blocker`, and `--test` flags.

Usage: `python scripts/write_checkpoint.py .sdd-delivery/<feature> --phase implementation --task T1`

In No-Python mode, edit `11-checkpoint.json` directly with the same field updates.

## validate_artifacts.py

Validates a feature artifact folder for required files, content presence, and checkpoint field completeness. With `--strict`, fails if any gate has not passed.

Usage: `python scripts/validate_artifacts.py .sdd-delivery/<feature> [--strict]`

In No-Python mode, manually check each required file and field against `references/artifact-schema.md`.

## summarize_tool_output.py

Summarizes large command output (build logs, test results, lint output) for context-aware inclusion. Extracts errors, warnings, and key lines while fitting within a context window.

Usage: `python scripts/summarize_tool_output.py output.log --type test`

In No-Python mode, manually identify error lines and summarize the rest.

