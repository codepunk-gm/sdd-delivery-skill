# Traceability

Traceability connects PRD, Spec, solution, tasks, code, and unit tests. Use `03-requirement-trace.md` as the source of truth.

## Required Columns

| PRD ID | Spec ID | Acceptance Criteria | Solution Section | Task ID | Code Files | Unit Tests | Status |
|---|---|---|---|---|---|---|---|

## Status Values

| Status | Meaning | When to Set |
|--------|---------|-------------|
| pending | Not yet processed | Initial state |
| specified | Spec item created | After Spec Authoring (phase 3) |
| reviewed | Spec item reviewed | After Spec Review (phase 4) |
| designed | Solution section exists | After Technical Solution (phase 7) |
| implemented | Code written, tests pass | After Implementation (phase 10) |
| tested | Unit test report complete | After Unit Test Report (phase 12) |
| deferred | Intentionally postponed | When accepted as out of scope for this iteration |
| blocked | Cannot proceed | When `_Depends:_` is unresolved |

## Rules

- Every P0/P1 PRD item must map to at least one Spec item.
- Every implementation task must map to at least one Spec item or a documented engineering task.
- Every acceptance criterion must map to a unit test or documented verification gap.
- When code files change, update the trace row's Code Files column.
- When tests are written, update the trace row's Unit Tests column.
- When a row's status changes, update the Status column.

## Auto-Update Triggers

When the agent performs these actions, check if the trace needs updating:

| Action | Trace Update |
|--------|-------------|
| New Spec item written | Add row, set status = specified |
| Spec item reviewed | Set status = reviewed |
| Solution section written | Add Solution Section, set status = designed |
| Task completed | Add Task ID + Code Files, set status = implemented |
| Test written for Spec item | Add Unit Tests |
| Test report completed | Set status = tested |
| New code file created | Add to Code Files for relevant row |
| Spec item scope reduced | Set status = deferred, add reason |

## Coverage Calculation

Run `python scripts/trace_coverage.py .sdd-delivery/<feature>` to calculate:

- **Solution Coverage:** % of Spec items with a Solution Section.
- **Task Coverage:** % of Spec items with a Task ID.
- **Code Coverage:** % of Spec items with Code Files.
- **Unit Test Coverage:** % of Spec items with Unit Tests.

In No-Python mode, count manually from `03-requirement-trace.md`.

## Coverage Thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Solution Coverage | 100% of P0 items | ≥90% of all items |
| Task Coverage | 100% | 100% |
| Code Coverage | 100% of implemented items | ≥95% |
| Unit Test Coverage | 100% of P0 items | ≥80% of all items |

## Gap Handling

When an acceptance criterion cannot have a unit test:

1. **Integration/existing test:** Cite the existing test that covers it (file + test name).
2. **Manual verification:** Document the manual verification steps in `09-unit-test-report.md`.
3. **Accepted gap:** Record in trace with status = deferred and a reason in `## Accepted Gaps`.

The sum of direct tests + integration references + manual verifications + accepted gaps must equal 100% of acceptance criteria.

## Reverse Trace

Run `python scripts/scan_test_coverage.py . .sdd-delivery/<feature>` to find all tests that reference `SPEC-*` IDs. This confirms that tests trace back to Spec. Tests without SPEC-* references are flagged as untraced.

In No-Python mode: `grep -r "SPEC-" tests/` and cross-reference with trace rows.
