---
name: sdd-delivery
description: Use for PRD-driven spec-first engineering delivery where Spec is mandatory before PRD review, followed by technical solution design, solution review, implementation, unit testing, delivery review, observable artifacts, checkpoints, and context compression. Trigger for PRD, Spec, 需求评审, 方案设计, 方案审查, 单测, 研发提效, 上下文压缩, checkpoint, 可观测交付, or 多文件研发任务.
---

# SDD Delivery

SDD Delivery is a promotable team skill for PRD-driven, Spec-gated, observable engineering delivery.

It combines:
- deterministic PRD parsing into Spec drafts
- PRD normalization
- mandatory Spec before PRD review
- requirement traceability
- technical solution design
- solution review gates
- bounded implementation
- unit test planning and execution
- deterministic checkpoint recovery
- observable delivery metrics
- trace coverage calculation
- reverse test-to-Spec coverage scanning
- GitHub PR template and CI artifact validation assets

## Startup behavior

When this skill is loaded for a new workflow and the user has not selected a specific phase, show the capability menu from 
references/capability-menu.md in concise form. Ask the user to send a PRD or choose a number.

If Python is unavailable, do not fail. Use No Python Mode from 
references/ai-tool-usage.md: create and update Markdown/JSON artifacts manually, then explain which script-backed automation was skipped.

## When to use

Use this skill for non-trivial team engineering work that starts from a PRD or requirement and needs design, review, code, and unit tests.

Use quick mode only for tiny safe edits. For feature work, bug fixes with behavior impact, refactors, interface changes, or multi-file changes, use full DevFlow mode.

## Mandatory gates

Do not skip these gates unless the user explicitly overrides them:

1. PRD must be converted into Spec before PRD review.
2. Spec Review must pass or record open issues before technical solution.
3. Technical Solution must exist before implementation tasks.
4. Solution Review must pass or record accepted risks before coding.
5. Unit Test Plan must exist before declaring implementation complete.
6. Unit Test Report or documented verification gap is required before delivery.
7. Checkpoint and observability must be updated before stopping, compaction, or handoff.

## Non-negotiable rules

- Follow project instructions and architecture.
- Read and write code files as UTF-8.
- Do not turn Chinese text into mojibake.
- Prefer artifacts over chat memory.
- Load only the context needed for the current phase.
- Every repo fact must have a source.
- Every implementation task should trace back to Spec items.
- Every unit test should trace back to Spec acceptance criteria when possible.
- Do not modify unrelated files.
- Do not treat stale code facts as durable memory.

## Full workflow

1. PRD Intake
   - Save or summarize the PRD in `00-prd.md`.
   - Identify requirement items and unknowns.

2. Spec Authoring
   - Convert PRD into `01-spec.md`.
   - Spec is the reviewable contract for PRD quality.

3. Spec Review
   - Review clarity, completeness, acceptance criteria, boundaries, and testability in `02-spec-review.md`.
   - Do not continue when P0/P1 review blockers are unresolved unless the user accepts the risk.

4. Requirement Trace
   - Maintain `03-requirement-trace.md` mapping PRD items to Spec items, solution sections, tasks, code, and unit tests.

5. Technical Solution
   - Write `04-tech-solution.md` with repo-grounded design and verification strategy.

6. Solution Review
   - Review architecture, compatibility, security, performance, scope, and testability in `05-solution-review.md`.

7. Implementation Tasks
   - Write `06-implementation-tasks.md` with bounded, verifiable tasks.

8. Implementation
   - Work one task at a time.
   - Maintain `07-implementation-log.md`.
   - Update checkpoint after meaningful changes.

9. Unit Test Plan
   - Write `08-unit-test-plan.md` before completion.
   - Map test cases to Spec acceptance criteria.

10. Unit Test Report
    - Record commands, status, failures, and coverage gaps in `09-unit-test-report.md`.

11. Delivery Review
    - Final review in `10-delivery-review.md`, findings first.

12. Checkpoint and Observability
    - Update `11-checkpoint.json`, `12-observability.md`, and `events.jsonl` before stop, compact, or handoff.

## Required artifacts

```text
.sdd-delivery/<feature>/
├── 00-prd.md
├── 01-spec.md
├── 02-spec-review.md
├── 03-requirement-trace.md
├── 04-tech-solution.md
├── 05-solution-review.md
├── 06-implementation-tasks.md
├── 07-implementation-log.md
├── 08-unit-test-plan.md
├── 09-unit-test-report.md
├── 10-delivery-review.md
├── 11-checkpoint.json
├── 12-observability.md
└── events.jsonl
```

## Context Contract

Before implementation, state or update:

```markdown
## Context Contract

Feature:
Active phase:
Active task:
Spec items:
In scope:
Out of scope:
Relevant files:
Verification:
Stop conditions:
```

## Reference loading

- Read `references/workflow.md` for the full process.
- Read `references/gates.md` before moving between phases.
- Read `references/traceability.md` when updating requirement mapping.
- Read `references/context-policy.md` before broad repo exploration, compaction, or recovery.
- Read `references/review-rubric.md` before Spec Review, Solution Review, or Delivery Review.
- Read `references/unit-test-policy.md` before unit test planning.
- Read `references/team-rules.md` for organization-specific conventions.
- Read `references/capability-menu.md` when starting a new workflow.
- Read `references/interaction-model.md` for guided, friendly, Codex-client-oriented interaction.
- Read `references/ai-tool-usage.md` when the user asks about Codex, Claude Code, Cursor, Copilot, Windsurf, Continue, plugin install, or no-Python usage.
- Read `references/plugin-operations.md` when publishing, installing, updating, or troubleshooting the plugin.
- Read `references/open-source-influences.md` when explaining design references or open-source inspiration.
- Read `references/automation.md` before using bundled automation scripts.
- Read `references/github-integration.md` before generating GitHub PR/CI assets.

## Script usage

Prefer bundled scripts:

```bash
python scripts/init_artifacts.py <feature-name>
python scripts/parse_prd_to_spec.py prd.md .sdd-delivery/<feature-name> --force
python scripts/trace_coverage.py .sdd-delivery/<feature-name>
python scripts/scan_test_coverage.py . .sdd-delivery/<feature-name> --update-report --update-trace
python scripts/sync_observability.py .sdd-delivery/<feature-name>
python scripts/generate_github_assets.py .
python scripts/write_checkpoint.py .sdd-delivery/<feature-name> --phase implementation --task T1
python scripts/validate_artifacts.py .sdd-delivery/<feature-name>
python scripts/summarize_tool_output.py output.log --type test
```

## Final response expectations

For substantial work, report:
- current phase
- artifacts updated
- gates passed or open blockers
- implementation status
- unit test status
- observability/checkpoint status
- next action










