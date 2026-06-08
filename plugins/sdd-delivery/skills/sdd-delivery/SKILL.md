---
name: sdd-delivery
description: Use for PRD-driven spec-first engineering delivery where Spec is mandatory before PRD review, followed by technical solution design, solution review, implementation, unit testing, delivery review, observable artifacts, checkpoints, and context compression. Trigger for PRD, Spec, 需求评审, 方案设计, 方案审查, 单测, 研发提效, 上下文压缩, checkpoint, 可观测交付, or 多文件研发任务.
---

# SDD Delivery

SDD Delivery is a promotable team skill for PRD-driven, Spec-gated, observable engineering delivery.

It combines:
- constitution-governed, principle-first engineering
- intelligent work routing (discovery and classification)
- PRD clarification with taxonomy-driven ambiguity scanning
- deterministic PRD parsing into Spec drafts
- mandatory Spec before PRD review
- cross-artifact consistency analysis
- requirement traceability with coverage thresholds
- pre-mortem risk reasoning before design decisions
- technical solution design with boundary annotations
- solution review with security audit
- bounded implementation with per-task review
- TDD structural blocking (RED → GREEN → REFACTOR)
- parallel task markers for independent work
- explicit user approval of solution and technology stack before implementation
- optional pluggable capabilities with `enabled|disabled|ask` switches for frontend templates, Java modular projects, enterprise MCP capability discovery, and team rules
- MCP discovery and capability-selection evidence artifacts when enterprise internal capabilities should be reused during implementation
- unit test planning and execution
- deterministic checkpoint recovery
- observable delivery metrics
- human-reviewable milestones for progress and quality control
- static HTML dashboard generation for business-friendly review
- trace coverage calculation
- reverse test-to-Spec coverage scanning
- GitHub PR template and CI artifact validation assets

Gate enforcement is an agent workflow contract, not a runtime sandbox. Enforce gates by stopping at the required point, recording evidence in artifacts/checkpoint, asking for user confirmation when required, and refusing to claim completion when evidence is missing. Scripts are accelerators and validators; they do not replace agent judgment or real test execution.

## Constitution

Before any action, load `references/constitution.md`. The constitution defines 8 non-negotiable principles ranked by precedence:

1. Spec Before Code
2. Artifacts Over Chat
3. Gates Before Progress
4. Traceability Forever
5. Minimal, Reviewable Diffs
6. UTF-8 Always
7. No-Python Universality
8. Evidence Over Assertion

When principles conflict, state the conflict explicitly, propose a scope-limited override, and ask for user confirmation. Never override a principle silently.

## Startup behavior

When this skill is loaded for a new workflow and the user has not selected a specific phase, first show the welcome opening from `references/interaction-model.md`, then show the capability menu from `references/capability-menu.md` in concise form. Ask the user to send a PRD, choose a number, configure preferences, or use light mode.

If Python is unavailable, do not fail. Use No Python Mode from `references/ai-tool-usage.md`: create and update Markdown/JSON artifacts manually, then explain which script-backed automation was skipped.

## Discovery (Brownfield Routing)

Before planning in an existing repo, run a Discovery scan:

1. Check if `.sdd-delivery/` already exists — if so, offer recovery mode (resume from latest checkpoint).
2. Read `references/brownfield-change.md` for existing-project rules.
3. Inspect existing architecture (package structure, key interfaces, test patterns) before proposing changes.
4. Classify the work into one of five paths:

| Path | When Used | Output |
|------|-----------|--------|
| Extend existing spec | Adding to a previously approved spec | Updated spec |
| Create one new spec | Greenfield feature with clear boundaries | New spec |
| Decompose into multiple specs | Large request crossing module boundaries | Multiple specs + roadmap |
| Implement directly | Trivial/safe change (typo, config, doc) | Direct implementation |
| Mixed decomposition | Combination of extending and new specs | Mixed |

5. Record repo facts with sources (file path + line number). Do not treat stale facts as durable memory.

## When to use

Use this skill for non-trivial team engineering work that starts from a PRD or requirement and needs design, review, code, and unit tests.

Use quick mode only for tiny safe edits (typos, config values, docstrings). For feature work, bug fixes with behavior impact, refactors, interface changes, or multi-file changes, use full DevFlow mode.

Quick mode bypasses gates 1-4. The user must explicitly request it.

## Mandatory gates

Do not skip these gates unless the user explicitly overrides them:

1. **Clarify Gate** — No unresolved P0/P1 ambiguities before Spec authoring (or user accepts).
2. **Spec Gate** — PRD must be converted into Spec before PRD review.
3. **Spec Review Gate** — Spec Review must pass or record open issues before technical solution.
4. **Analyze Gate** — Cross-artifact consistency must be confirmed or gaps accepted before technical solution.
5. **Solution Gate** — Technical Solution must exist before implementation tasks.
6. **Solution Approval Gate** — User must approve the solution and technology stack before implementation tasks.
7. **Solution Review Gate** — Solution Review must pass or record accepted risks before coding.
8. **TDD Gate** — Tests must be written and failing (RED) before implementation code is written (GREEN).
9. **Per-Task Review Gate** — Each completed task must be reviewed before the next task begins.
10. **Unit Test Gate** — Unit Test Plan must exist before declaring implementation complete.
11. **Test Report Gate** — Unit Test Report or documented verification gap is required before delivery.
12. **Delivery Review Gate** — Delivery Review must pass or record accepted risks before delivery.
13. **Checkpoint Gate** — Checkpoint and observability must be updated before stopping, compaction, or handoff.

See `references/gates.md` for the gate state machine and blocked-gate protocol.

Gate evidence must be artifact-backed. For TDD, record the test file, command, RED result, implementation change, and GREEN result. For per-task review, record boundary verification, changed files, test status, and checkpoint update. For solution approval, record the user's decision in `11-checkpoint.json`.

Human-in-the-loop control is part of the workflow. Maintain milestones in `11-checkpoint.json`, render them in `12-observability.md`, and record human reviews when a reviewer checks progress, quality, or evidence files. The five milestone checkpoints are: M1 需求基线, M2 方案确认, M3 实现受控, M4 验证完成, and M5 交付就绪.

## Non-negotiable rules

- Follow project instructions and architecture.
- Read and write code files as UTF-8. Do not turn Chinese text into mojibake.
- Keep user-visible language consistent. If the user writes in Chinese or the repo instructions are Chinese, use Chinese for menus, tables, dashboard labels, artifact headings, review summaries, and generated UI text. Keep only stable technical identifiers in English, such as `PRD`, `Spec`, `checkpoint`, `MCP`, file names, API names, class names, and code symbols. Do not mix translated and untranslated business labels in the same table or UI surface.
- Prefer artifacts over chat memory.
- Load only the context needed for the current phase.
- Every repo fact must have a source (file path + line number).
- Every implementation task must trace back to Spec items and include `_Boundary:_` annotation.
- Every unit test must trace back to Spec acceptance criteria when possible.
- Every task that depends on another must include `_Depends:_` annotation.
- Technical solution must be explicitly approved by the user before task splitting or implementation.
- At startup, infer or ask for artifact language preference, then record it in checkpoint preferences.
- At startup, offer team-rule setup; users may configure or skip it.
- Before phases with optional extension points, read `references/capability-registry.md` and apply capability switches from checkpoint.
- When work can use enterprise internal capabilities and MCP capability reuse is enabled or still `ask`, discover available MCP tools/resources/components before implementation. Record discovery and selection evidence in `mcp-discovery.json` and `mcp-component-selection.md` before hand-building a replacement.
- When work touches SQL, ORM models, migrations, query builders, or data-access code, read `.sdd-delivery/team-rules.json` and apply `sql_standards` during technical solution, implementation tasks, review, and delivery. Use global rules first, then project overrides, then feature exceptions. Ask before adding a new feature exception.
- When discussing optional capabilities with the user, use user-facing names and benefits; hide internal adapter/executor terminology unless asked.
- Do not modify unrelated files. Boundary violations are P0 rejections.
- Do not treat stale code facts as durable memory.
- No single task may exceed 200 lines of change (L size) without explicit justification.
- Parallel tasks must be marked with `[P]` prefix. Independent tasks should be parallelized.
- Tests must be written BEFORE implementation code (RED → GREEN → REFACTOR).

## Full workflow

### 1. PRD Intake
- Save or summarize the PRD in `00-prd.md`.
- Identify requirement items, unknowns, and constraints.
- Refs: `references/capability-menu.md`

### 2. Clarify
- Run taxonomy scan against PRD items using `references/clarify-taxonomy.md`.
- Present at most 5 prioritized questions per session.
- Record resolutions in `00-prd.md` under `## Clarify Scan`.
- **Gate:** No unresolved P0/P1 ambiguities before proceeding.

### 3. Spec Authoring
- Convert PRD into `01-spec.md`.
- Include acceptance criteria for every Spec item.
- Mark `_Depends:_` for Spec items blocked on decisions.
- Spec is the reviewable contract for PRD quality.

### 4. Spec Review
- Review clarity, completeness, acceptance criteria, boundaries, and testability in `02-spec-review.md`.
- Refs: `references/review-rubric.md`
- **Gate:** Do not continue when P0/P1 review blockers are unresolved unless the user accepts the risk.

### 5. Analyze (Cross-Artifact Consistency)
- Run four detection passes using `references/analyze-rubric.md`:
  1. Duplications (same requirement in two places)
  2. Ambiguities (vague language without concrete criteria)
  3. Underspecified items (dangling references, missing file paths)
  4. Constitution conflicts (violations of non-negotiable principles)
- Record findings in `03-requirement-trace.md` under `## Analysis`.
- **Gate:** No P0 findings before proceeding.

### 6. Requirement Trace
- Maintain `03-requirement-trace.md` mapping PRD items to Spec items, solution sections, tasks, code, and unit tests.
- Refs: `references/traceability.md`

### 7. Technical Solution
- Run pre-mortem using `references/pre-mortem.md`: "Assume this solution failed. Why?"
- Write `04-tech-solution.md` with repo-grounded design and verification strategy.
- Record pre-mortem findings in the solution under `## Pre-Mortem`.
- Present architecture, technology stack, affected modules, rollback, and verification summary.
- **Gate:** Ask the user to approve, request changes, reject, or swap technology stack before task splitting.

### 8. Solution Review
- Review architecture, compatibility, security, performance, scope, and testability in `05-solution-review.md`.
- Run security audit using `references/security-audit.md`.
- Refs: `references/review-rubric.md`, `references/security-audit.md`
- **Gate:** CRITICAL and HIGH security findings must be resolved or accepted.

### 9. Implementation Tasks
- Read `references/boundary-rules.md`, `references/task-splitting.md`, `references/estimation.md`.
- Write `06-implementation-tasks.md` with bounded, verifiable tasks.
- Every task must include `_Boundary:_` and estimation size (XS-XL).
- Mark independent tasks with `[P]`. Split any XL task.
- **Gate:** No XL tasks. All tasks must have boundary annotations.

### 10. Implementation
- Work one task at a time. Write tests FIRST (RED), confirm failure, then implement (GREEN).
- Maintain `07-implementation-log.md`. Update checkpoint after meaningful changes.
- **Per-task review:** After each task, verify boundaries, tests, and scope before starting the next.
- **Gate:** Boundary violations are P0 rejection. Test-before-code order is enforced.

### 11. Unit Test Plan
- Write `08-unit-test-plan.md` before completion.
- Map test cases to Spec acceptance criteria. Document TDD order.
- Refs: `references/unit-test-policy.md`
- **Gate:** Plan must exist before declaring implementation complete.

### 12. Unit Test Report
- Record commands, status, failures, and coverage gaps in `09-unit-test-report.md`.
- Run `python scripts/scan_test_coverage.py . .sdd-delivery/<feature> --update-report --update-trace` if available.
- **Gate:** Report or documented verification gap required before delivery.

### 13. Delivery Review
- Final review in `10-delivery-review.md`, findings first.
- Run security audit again for implemented changes.
- Verify all task boundaries were respected (cross-reference changed files).
- Refs: `references/review-rubric.md`

### 14. Checkpoint and Observability
- Update `11-checkpoint.json`, `12-observability.md`, and `events.jsonl` before stop, compact, or handoff.
- Refresh milestone status, human review records, and quality status so a reviewer can understand progress without chat history.
- When a human-readable review surface is useful, generate `13-dashboard.html` from the artifact state. Treat it as a generated view, not as the source of truth.
- Refs: `references/context-policy.md`, `references/checkpoint-schema.md`

## Required artifacts

```text
.sdd-delivery/<feature>/
├── 00-prd.md              (includes ## Clarify Scan)
├── 01-spec.md
├── 02-spec-review.md
├── 03-requirement-trace.md (includes ## Analysis)
├── 04-tech-solution.md    (includes ## Pre-Mortem)
├── 05-solution-review.md  (includes ## Security Audit)
├── 06-implementation-tasks.md
├── 07-implementation-log.md
├── 08-unit-test-plan.md
├── 09-unit-test-report.md
├── 10-delivery-review.md  (includes ## Security Audit)
├── 11-checkpoint.json
├── 12-observability.md
└── events.jsonl
```

## Context Contract

Before implementation, state or update:

```markdown
## 上下文契约

需求：
当前阶段：
当前任务：
Spec 条目：
范围内：
范围外：
边界：
依赖：
相关文件：
验证：
停止条件：
已启用能力：
能力开关：
方案确认：
```

## Reference loading

- Read `references/constitution.md` at startup and when a principle override is requested.
- Read `references/workflow.md` for the full 14-phase process, dependencies, and recovery flow.
- Read `references/gates.md` before moving between phases.
- Read `references/clarify-taxonomy.md` before Spec authoring (phase 3).
- Read `references/analyze-rubric.md` after Spec Review (phase 4) and after Task Splitting (phase 9).
- Read `references/traceability.md` when updating requirement mapping.
- Read `references/pre-mortem.md` before Technical Solution (phase 7) and before Implementation (phase 10).
- Read `references/review-rubric.md` before Spec Review, Solution Review, or Delivery Review.
- Read `references/boundary-rules.md` before Implementation Tasks (phase 9).
- Read `references/task-splitting.md` before Implementation Tasks (phase 9).
- Read `references/estimation.md` before Implementation Tasks (phase 9).
- Read `references/unit-test-policy.md` before unit test planning.
- Read `references/security-audit.md` before Solution Review (phase 8) and Delivery Review (phase 13).
- Read `references/context-policy.md` before broad repo exploration, compaction, or recovery.
- Read `references/team-rules.md` for organization-specific conventions.
- Read `references/code-principles.md` when team code principle modules are enabled.
- Read `references/capability-registry.md` before asking whether to enable optional capability modules.
- Read `references/capability-menu.md` when starting a new workflow.
- Read `references/interaction-model.md` for guided interaction and recovery mode.
- Read `references/ai-tool-usage.md` for multi-tool and No-Python guidance.
- Read `references/plugin-operations.md` when publishing, installing, updating, or troubleshooting the plugin.
- Read `references/open-source-influences.md` when explaining design references.
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
python scripts/manage_capabilities.py .sdd-delivery/<feature-name> --project-root . --detect --plan
python scripts/setup_team_rules.py --root . --init
python scripts/validate_artifacts.py .sdd-delivery/<feature-name>
python scripts/summarize_tool_output.py output.log --type test
```

## Final response expectations

For substantial work, report:
- current phase
- clarify status (if applicable)
- analysis status (if applicable)
- pre-mortem recorded (y/n)
- artifacts updated
- gates passed or open blockers
- boundary annotations complete (y/n)
- per-task review status
- implementation status
- unit test status (RED/GREEN/REFACTOR phase)
- observability/checkpoint status
- next action
