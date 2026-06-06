# Workflow

SDD Delivery is a PRD-driven delivery workflow with Spec as the mandatory contract before PRD review.

## Full 14-Phase Workflow

| # | Phase | Input | Output | Gate | Key Reference |
|---|-------|-------|--------|------|---------------|
| 1 | PRD Intake | User PRD | `00-prd.md` | — | capability-menu.md |
| 2 | Clarify | `00-prd.md` | `## Clarify Scan` in `00-prd.md` | Gate 1 | clarify-taxonomy.md |
| 3 | Spec Authoring | Clarified PRD | `01-spec.md` | Gate 2 | — |
| 4 | Spec Review | `01-spec.md` | `02-spec-review.md` | Gate 3 | review-rubric.md |
| 5 | Analyze | `01-spec.md`, `03-requirement-trace.md` | `## Analysis` in trace | Gate 4 | analyze-rubric.md |
| 6 | Requirement Trace | Spec items | `03-requirement-trace.md` | — | traceability.md |
| 7 | Technical Solution | Spec, trace | `04-tech-solution.md` (+ Pre-Mortem) | Gate 5 | pre-mortem.md |
| 8 | Solution Approval + Review | Tech solution | user approval + `05-solution-review.md` (+ Security Audit) | Gates 6-7 | review-rubric.md, security-audit.md |
| 9 | Implementation Tasks | Approved solution | `06-implementation-tasks.md` | Gate 5 + XL check | boundary-rules.md, task-splitting.md, estimation.md |
| 10 | Implementation | Tasks | Code + `07-implementation-log.md` | Gates 8-9 | boundary-rules.md |
| 11 | Unit Test Plan | Spec, tasks | `08-unit-test-plan.md` | Gate 10 | unit-test-policy.md |
| 12 | Unit Test Report | Test results | `09-unit-test-report.md` | Gate 11 | unit-test-policy.md |
| 13 | Delivery Review | All artifacts | `10-delivery-review.md` (+ Security Audit) | Gate 12 | review-rubric.md, security-audit.md |
| 14 | Checkpoint + Observability | All state | `11-checkpoint.json`, `12-observability.md`, `events.jsonl` | Gate 13 | context-policy.md |

## Phase Dependencies

```
PRD Intake ──→ Clarify ──→ Spec Authoring ──→ Spec Review ──→ Analyze
                                                                    │
                                                    ┌───────────────┘
                                                    ▼
                              Requirement Trace ──→ Technical Solution ──→ Solution Approval ──→ Solution Review
                                                                                │
                                                                ┌───────────────┘
                                                                ▼
                              Implementation Tasks ──→ Implementation ──→ Unit Test Plan
                                                           │
                                                           ▼
                              Unit Test Report ──→ Delivery Review ──→ Checkpoint + Observability
```

## Parallel Opportunities

- **Spec Review + Requirement Trace** can be prepared in parallel (independent reads of `01-spec.md`).
- **Unit Test Plan** can be drafted alongside Implementation (TDD: tests written first).
- **Tasks marked `[P]`** can be implemented by parallel subagents when tooling supports it.
- **Security Audit** can run in parallel with other review dimensions.

## Quick Mode vs. Full Mode

| Criteria | Quick Mode | Full DevFlow |
|----------|-----------|-------------|
| **When** | Typos, config values, docstrings, formatting | Features, bug fixes with behavior impact, refactors, interface changes |
| **Max lines changed** | ≤10 | Any (bounded by task sizes) |
| **Gates** | Bypassed (gates 1-4) | All gates enforced |
| **Artifacts** | Implementation log only | Full 14-artifact set |
| **Review** | Self-review | Per-task review |
| **User trigger** | Explicitly requested ("quick mode") | Default |

## Recovery Flow

When resuming from a checkpoint:

1. Read `11-checkpoint.json` to identify `current_phase`, `active_task`, and `gate_status`.
2. Read `12-observability.md` for metrics summary.
3. Read `events.jsonl` for the last session's events.
4. Reconstruct the Context Contract from checkpoint fields.
5. Verify that the artifacts referenced in the checkpoint still exist and are unchanged.
6. Present a recovery summary: "Resuming [feature] at phase [N], task [T]. Last action: [next_action]. Gates passed: [list]. Open blockers: [list]."
7. If the user interrupted during implementation or testing, classify the interruption as `question`, `scope_change`, `solution_change`, or `stop_request`.
8. For `question`, answer briefly, then resume the pending `next_action`.
9. For `scope_change` or `solution_change`, update the affected artifact, reset downstream gates to `pending`, and ask for solution approval again when architecture or stack changed.
10. Ask: "Continue from here, or restart from a different phase?"

## Observable Outcome

The feature folder should explain current state without chat history:

- What PRD items exist and their clarify status.
- Which Spec items cover them and their review status.
- Which solution sections implement them.
- Which tasks changed code and their review status.
- Which unit tests cover acceptance criteria.
- Which risks remain open.
- Which gates are passed, accepted-risk, or blocked.
- What the next action is.
