# Gates

A gate does not mean no progress. A gate means unresolved risk must be visible and accepted before progress.

Gates are enforced by agent behavior and artifact evidence. They are not OS-level or editor-level guards. The agent must stop at a gate, collect or create the required evidence, update the relevant artifact/checkpoint, and only proceed when the gate is `passed` or the user explicitly accepts the risk.

Bundled scripts can validate structure, calculate coverage, scan `SPEC-*` references, and refresh observability. They cannot prove product correctness, replace real test execution, or silently approve architecture and technology choices.

## Gate State Machine

```
pending → in_review → passed | accepted_risk | blocked
```

- **pending:** Gate has not been evaluated yet.
- **in_review:** Gate is currently being evaluated.
- **passed:** All criteria met. Proceed.
- **accepted_risk:** Some criteria not met, but user has explicitly accepted the risk. Record reason in the review artifact.
- **blocked:** Criteria not met and user has not accepted. Do not proceed.

## Blocked Gate Protocol

When a gate is blocked:

1. **State the finding** with severity (P0/P1/P2/P3) and detail.
2. **Offer 3 options:**
   - Fix now (resolve the issue and re-evaluate)
   - Accept risk (record in review artifact with reason and expiry)
   - Stop and checkpoint (save current state for later recovery)
3. **If accepted risk:** Record in the corresponding review artifact with:
   - What risk was accepted
   - Why it was accepted
   - Who accepted it (user confirmation)
   - When the risk expires (or "until next review")
4. **If blocked:** Set checkpoint `gate_status` to `blocked`, update next action, and wait for user direction.

## Gate Definitions

### Gate 1: Clarify

Required before Spec authoring.

**Pass criteria:**
- Taxonomy scan completed against all PRD items.
- P0 ambiguities resolved or accepted.
- P1 ambiguities resolved, accepted, or deferred (max 5 deferred).
- Clarify Scan section recorded in `00-prd.md`.

**Blockers:**
- P0 ambiguity with no resolution or acceptance.
- More than 5 deferred P1 ambiguities (too many unknowns to write a useful Spec).

### Gate 2: Spec Gate

Required before PRD review.

**Pass criteria:**
- PRD items are identified.
- Every high-priority PRD item maps to at least one Spec item.
- Spec items have acceptance criteria.
- Unknowns and non-goals are explicit.
- Boundaries (`_Boundary:_`) are declared for cross-cutting Spec items.

### Gate 3: Spec Review

Required before technical solution.

**Blockers:**
- Ambiguous behavior with no clarification recorded.
- Missing acceptance criteria for P0/P1 Spec items.
- Untestable requirement (no observable outcome).
- Conflicting PRD statements not reconciled.
- Missing edge cases for critical flows.

### Gate 4: Analyze

Required before technical solution.

**Pass criteria:**
- Four detection passes completed (duplications, ambiguities, underspecified, constitution conflicts).
- No P0 findings (or user has accepted them).
- Analysis section recorded in `03-requirement-trace.md`.

**Blockers:**
- P0 finding with no resolution.
- Constitution violation with no override recorded.

### Gate 5: Solution Gate

Required before implementation tasks.

**Pass criteria:**
- `04-tech-solution.md` exists with all required sections.
- Pre-mortem recorded.
- Design is grounded in repo evidence.

### Gate 6: Solution Approval

Required after technical solution and before implementation tasks.

**Pass criteria:**
- User has explicitly approved the proposed architecture, technology stack, and implementation direction.
- Approval, requested changes, or rejection is recorded in `11-checkpoint.json` under `solution_approval`.
- If the user requests changes, `04-tech-solution.md` is updated and this gate is re-evaluated.

**Blockers:**
- No explicit user approval for the solution.
- User rejects the approach or technology stack.
- The solution changed materially after approval and was not re-approved.

### Gate 7: Solution Review

Required before implementation.

**Blockers:**
- No repo evidence for design claims.
- Incompatible architecture with no migration plan.
- Unhandled migration or compatibility risk.
- Missing rollback or verification strategy.
- Security-sensitive change without audit (see `references/security-audit.md`).
- CRITICAL or HIGH security findings unresolved.

### Gate 8: TDD Gate

Required before writing implementation code for each task.

**Pass criteria:**
- Test file exists for the task.
- Test references the correct Spec ID (`SPEC-*`).
- Test can be run and FAILS (RED) — confirms the feature doesn't exist yet.
- Test file is committed or staged before implementation code.

**Blockers:**
- Implementation code written before test.
- Test passes before implementation (feature already exists — task may be unnecessary).

### Gate 9: Per-Task Review

Required after each task completion, before the next task.

**Pass criteria:**
- Changed files are within declared `_Boundary:_`.
- No unrelated files modified.
- Tests pass (GREEN).
- Implementation log updated.
- Checkpoint updated.

**Blockers:**
- Boundary violation (P0 rejection regardless of code quality).
- Failing tests introduced by the change.
- Unrelated file modifications.

### Gate 10: Unit Test Plan

Required before declaring implementation complete.

**Pass criteria:**
- `08-unit-test-plan.md` exists.
- Every test case maps to a Spec acceptance criterion.
- TDD order (RED → GREEN → REFACTOR) is documented.
- Coverage targets are stated.

### Gate 11: Test Report

Required before delivery.

**Pass criteria:**
- `09-unit-test-report.md` records commands run and their status.
- Uncovered Spec items are explained.
- Failed tests are either fixed or documented as blockers.
- Coverage gaps are acknowledged.

### Gate 12: Delivery Review

Required before declaring the feature ready for delivery.

**Pass criteria:**
- `10-delivery-review.md` exists and findings are severity ordered.
- Boundary verification compares declared task boundaries with changed files.
- Test report gaps are either fixed or explicitly accepted.
- Security audit summary is recorded.

**Blockers:**
- P0 delivery finding remains open.
- Critical or high security issue is unresolved and not accepted by the user.
- Changed files cannot be traced to approved tasks.

### Gate 13: Checkpoint

Required before stopping, compaction, or handoff.

**Pass criteria:**
- `11-checkpoint.json` updated with current phase, task, gate status, and metrics.
- `12-observability.md` refreshed.
- `events.jsonl` appended with a session-end event.
- Next action is clearly stated.
