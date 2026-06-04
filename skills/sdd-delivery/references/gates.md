# Gates

## Gate 1: PRD to Spec

Required before PRD review.

Pass criteria:
- PRD items are identified.
- Spec has acceptance criteria.
- Unknowns are explicit.
- Boundaries and non-goals are clear.

## Gate 2: Spec Review

Required before technical solution.

Blockers:
- ambiguous behavior
- missing acceptance criteria
- untestable requirement
- conflicting PRD statements
- missing edge cases for critical flows

## Gate 3: Technical Solution Review

Required before implementation.

Blockers:
- no repo evidence
- incompatible architecture
- unhandled migration or compatibility risk
- missing rollback or verification strategy
- security-sensitive change without review

## Gate 4: Unit Test Completion

Required before delivery.

Pass criteria:
- unit test plan exists
- test report records command and status
- uncovered Spec items are explained
- failed tests are either fixed or documented as blockers
