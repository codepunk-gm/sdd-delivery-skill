# Open Source Influences

SDD Delivery combines practical ideas from several public engineering and AI-agent workflow patterns. It is not a copy of any project; it adapts the strongest design ideas into a plugin-friendly skill workflow.

## GitHub Spec Kit

Reference: https://github.com/github/spec-kit

Borrowed ideas:
- Spec-driven development as the backbone of AI-assisted engineering.
- Phase-based workflow from requirement to implementation.
- Structured artifacts instead of relying on chat history.
- Clear separation between specification, planning, and execution.

Adapted in SDD Delivery as:
- `01-spec.md` as the mandatory PRD review contract.
- gate-based flow before solution and implementation.
- traceable delivery artifacts under `.sdd-delivery/<feature>/`.

## OpenSpec

Reference: https://github.com/Fission-AI/OpenSpec

Borrowed ideas:
- Brownfield-friendly change workflow.
- Treat changes as reviewable proposals/specifications.
- Preserve project evolution through explicit artifacts.

Adapted in SDD Delivery as:
- technical solution review gate.
- requirement trace matrix.
- checkpoint and handoff artifacts for long-running changes.

## Agent Skill Patterns

Reference examples:
- Claude/Codex-style skill folders with `SKILL.md`.
- Progressive disclosure through references and templates.

Borrowed ideas:
- Keep `SKILL.md` concise.
- Move details into `references/`.
- Keep scripts optional and deterministic.

Adapted in SDD Delivery as:
- `references/` for workflow, gates, traceability, AI tool usage, and interaction model.
- `assets/templates/` for repeatable artifacts.
- No Python Mode when scripts are unavailable.

## Context Compression / Checkpoint Patterns

Borrowed ideas:
- Do not trust chat history as the only source of state.
- Write deterministic checkpoint artifacts before compaction or handoff.
- Keep current goal, phase, gates, risks, tests, and next action recoverable.

Adapted in SDD Delivery as:
- `11-checkpoint.json`.
- `12-observability.md`.
- `events.jsonl`.
- recovery mode and guided continuation.

## Traceability and Test Coverage Practices

Borrowed ideas from common software delivery practices:
- Requirement traceability matrix.
- Mapping requirements to acceptance criteria, implementation tasks, and tests.
- Using test identifiers to make coverage inspectable.

Adapted in SDD Delivery as:
- `03-requirement-trace.md`.
- `trace_coverage.py`.
- `scan_test_coverage.py` with `SPEC-*` reverse scan.

## GitHub Delivery Practices

Borrowed ideas:
- PR templates as delivery checklists.
- CI validation for required artifacts.
- Review findings as phase gates.

Adapted in SDD Delivery as:
- `generate_github_assets.py`.
- `.github/pull_request_template.md`.
- `.github/workflows/sdd-delivery-artifacts.yml`.
