# Gates

A gate does not mean no progress. A gate means unresolved risk must be visible and accepted before progress.

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

### Gate 6: Solution Review

Required before implementation.

**Blockers:**
- No repo evidence for design claims.
- Incompatible architecture with no migration plan.
- Unhandled migration or compatibility risk.
- Missing rollback or verification strategy.
- Security-sensitive change without audit (see `references/security-audit.md`).
- CRITICAL or HIGH security findings unresolved.

### Gate 7: TDD Gate

Required before writing implementation code for each task.

**Pass criteria:**
- Test file exists for the task.
- Test references the correct Spec ID (`SPEC-*`).
- Test can be run and FAILS (RED) — confirms the feature doesn't exist yet.
- Test file is committed or staged before implementation code.

**Blockers:**
- Implementation code written before test.
- Test passes before implementation (feature already exists — task may be unnecessary).

### Gate 8: Per-Task Review

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

### Gate 9: Unit Test Plan

Required before declaring implementation complete.

**Pass criteria:**
- `08-unit-test-plan.md` exists.
- Every test case maps to a Spec acceptance criterion.
- TDD order (RED → GREEN → REFACTOR) is documented.
- Coverage targets are stated.

### Gate 10: Test Report

Required before delivery.

**Pass criteria:**
- `09-unit-test-report.md` records commands run and their status.
- Uncovered Spec items are explained.
- Failed tests are either fixed or documented as blockers.
- Coverage gaps are acknowledged.

### Gate 11: Checkpoint

Required before stopping, compaction, or handoff.

**Pass criteria:**
- `11-checkpoint.json` updated with current phase, task, gate status, and metrics.
- `12-observability.md` refreshed.
- `events.jsonl` appended with a session-end event.
- Next action is clearly stated.
