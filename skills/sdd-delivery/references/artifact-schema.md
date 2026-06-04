# Artifact Schema

Field-level schema for each SDD Delivery artifact. Use this reference when creating or validating artifacts.

## 00-prd.md

Required sections:
- `# PRD` — title
- `## Source` — where the PRD came from (URL, file, or user message)
- `## Business Goal` — what problem this solves
- `## PRD Items` — numbered table: PRD ID, Requirement, Priority, Notes
- `## Constraints` — technical, business, or timeline constraints
- `## Unknowns` — explicitly flagged gaps
- `## Clarify Scan` — (added in phase 2) taxonomy scan results

## 01-spec.md

Required sections:
- `# Spec` — title
- `## Scope` — what this spec covers
- `## Spec Items` — numbered table: Spec ID, PRD ID, Behavior, Acceptance Criteria, Priority, `_Depends:_`
- `## Edge Cases` — error, empty, race, timeout scenarios
- `## Non-Goals` — explicitly out of scope
- `## Open Questions` — deferred decisions

## 02-spec-review.md

Required sections:
- `## Findings` — severity-ordered table: #, Severity, Category, Finding, Suggestion
- `## Gate Result` — passed | accepted_risk | blocked
- `## Accepted Risks` — (if any) what was accepted and why

## 03-requirement-trace.md

Required table:
| PRD ID | Spec ID | Acceptance Criteria | Solution Section | Task ID | Code Files | Unit Tests | Status |

Status values: pending | specified | reviewed | designed | implemented | tested | deferred | blocked

Required section (added in phase 5):
- `## Analysis` — cross-artifact consistency findings

## 04-tech-solution.md

Required sections:
- `## Current System Findings` — repo evidence (file paths, patterns, constraints)
- `## Proposed Design` — architecture, data flow, component interactions
- `## Affected Modules` — files and directories changed
- `## Interfaces` — API contracts, data shapes, protocols
- `## Data Model` — schema changes, migrations
- `## Error Handling` — failure modes and responses
- `## Compatibility` — backward compatibility, migration path
- `## Security` — auth, data exposure, input validation
- `## Performance` — expected impact, bottlenecks
- `## Rollback` — how to undo this change
- `## Verification Strategy` — how to confirm the solution works
- `## Pre-Mortem` — (added in phase 7) failure scenarios and mitigations

## 05-solution-review.md

Required sections:
- `## Findings` — severity-ordered: #, Severity, Category, Finding, Suggestion
- `## Security Audit` — (added in phase 8) OWASP-style checklist results
- `## Gate Result` — passed | accepted_risk | blocked
- `## Accepted Risks` — (if any) what was accepted and why

## 06-implementation-tasks.md

Each task entry must include:
```
### T[N]: [P?] [SpecItem] Goal
_Boundary:_ ...
_Depends:_ ...
_Size:_ XS|S|M|L|XL
- [ ] T[N] [P] [SPEC-X] Description with file path
**Files:** ...
**Verification:** ...
```

Required section:
- `## Implementation Notes` — cross-task learnings (updated as implementation progresses)

## 07-implementation-log.md

Required table:
| Time | Task | Change | Files | Reviewer | Review Status | Notes |

## 08-unit-test-plan.md

Required table:
| Test ID | Spec ID | Scenario | Input / Setup | Expected Result | Test Target | Status |

Status values: pending → red → green → refactored

## 09-unit-test-report.md

Required sections:
- `## Test Command`
- `## Results` — per-test status table
- `## Failed Tests` — details
- `## Uncovered Spec Items` — with reason
- `## Coverage Summary` — metric or "manual assessment"

## 10-delivery-review.md

Required sections:
- `## Findings` — severity-ordered
- `## Security Audit` — (added in phase 13) post-implementation security check
- `## Boundary Verification` — cross-reference changed files vs. declared boundaries
- `## Trace Coverage` — PRD → Spec → Task → Code → Test coverage summary
- `## Gate Result` — passed | accepted_risk | blocked

## 11-checkpoint.json

Required fields:
```json
{
  "schema_version": "2.0",
  "feature": "",
  "goal": "",
  "current_phase": "",
  "active_task": "",
  "completed_tasks": [],
  "pending_tasks": [],
  "decisions": [{"decision": "", "reason": "", "source": ""}],
  "repo_facts": [{"fact": "", "source": "", "staleness": "fresh"}],
  "changed_files": [],
  "tests_run": [{"command": "", "status": "passed|failed|skipped", "summary": "", "source": ""}],
  "gate_status": {
    "clarify": "pending",
    "spec": "pending",
    "spec_review": "pending",
    "analyze": "pending",
    "solution": "pending",
    "solution_review": "pending",
    "tdd": "pending",
    "per_task_review": "pending",
    "unit_test_plan": "pending",
    "test_report": "pending",
    "delivery_review": "pending"
  },
  "metrics": {},
  "risks": [],
  "blockers": [],
  "next_action": "",
  "updated_at": ""
}
```

## 12-observability.md

Required sections:
- `## Dashboard` — metrics table (PRD items, Spec items, tasks, tests, coverage, risks, blockers)
- `## Gate History` — chronological list of gate evaluations
- `## Commands Run` — significant commands and their outcomes
- `## Current Status` — brief summary and next action

## events.jsonl

Format: one JSON object per line:
```json
{"time": "ISO-8601 UTC", "event": "event_name", "detail": {...}}
```

Append-only. Never modify existing lines.
