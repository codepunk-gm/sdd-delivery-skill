# Traceability

Traceability connects PRD, Spec, solution, tasks, code, and unit tests.

Use `03-requirement-trace.md` as the source of truth.

## Required columns

| PRD ID | Spec ID | Acceptance Criteria | Solution Section | Task ID | Code Files | Unit Tests | Status |
|---|---|---|---|---|---|---|---|

## Status values

- pending
- specified
- reviewed
- designed
- implemented
- tested
- deferred
- blocked

## Rules

- Every high-priority PRD item must map to at least one Spec item.
- Every implementation task must map to at least one Spec item or a documented engineering task.
- Every acceptance criterion should map to a unit test or documented verification gap.
