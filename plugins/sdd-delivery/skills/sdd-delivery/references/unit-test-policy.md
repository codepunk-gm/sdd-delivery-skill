# Unit Test Policy

Unit tests are part of delivery, not an afterthought. Tests must be written BEFORE implementation code.

## TDD Structural Blocking

SDD Delivery enforces test-first ordering:

| Step | What Happens | Blocked If... |
|------|-------------|---------------|
| 1. RED | Write the test from Spec acceptance criteria. Run it. It MUST fail. | Test passes (feature already exists — task may be unnecessary) |
| 2. GREEN | Write minimal production code to make the test pass. | Implementation code written before test exists |
| 3. REFACTOR | Clean up code while keeping tests green. | Refactor introduces failing tests |

**Key rules:**
- Write the test before the implementation code. No exceptions without explicit user override.
- Run the test and confirm it FAILS (RED) before writing code.
- Implement minimal code to make it PASS (GREEN).
- Do not proceed to the next task until current task tests pass.
- If a test cannot be written first (e.g., UI snapshot, integration with external service), document the reason in `08-unit-test-plan.md` and record as accepted risk.

## Test File Convention

- Test files must reference SPEC-* IDs in docstrings or comments.
- Test files must be created alongside source files, not after.
- Test file location: co-located with source or in a mirror test directory (team preference, set in `references/team-rules.md`).

Example:
```python
# test_auth_service.py
"""Tests for AuthService.
SPEC-3: User login with valid credentials
SPEC-4: Invalid credentials error handling
"""

def test_login_with_valid_credentials():
    """SPEC-3: User can log in with valid credentials."""
    ...
```

## Unit Test Plan

Each test case in `08-unit-test-plan.md` must include:
- Test ID (UT-1, UT-2, ...)
- Spec ID (SPEC-*)
- Scenario (given/when/then)
- Inputs
- Expected result
- Mock or fixture strategy
- File or test target
- Status (pending → red → green → refactored)

## Unit Test Report

Record in `09-unit-test-report.md`:
- Test command and framework
- For each test case: status (passed/failed/skipped)
- Failed test details (expected vs. actual)
- Uncovered Spec items with reason
- Coverage metric (if tooling available)

## Coverage Rule

Every Spec acceptance criterion must have one of:
- **Direct unit test:** Test written, passing, with SPEC-* reference.
- **Integration or existing test reference:** Test exists elsewhere that covers this criterion. Cite the test location.
- **Documented manual verification:** Automated test impractical. Document manual verification steps.
- **Accepted gap with reason:** Cannot test. Reason recorded. User accepted.

## Coverage Thresholds

- **Minimum:** 100% of P0 Spec items must have a documented test or accepted gap.
- **Target:** ≥80% of all Spec items have direct unit tests.
- **Below target:** Must explain in `09-unit-test-report.md` why coverage is lower and what is planned.

## Reverse Coverage Scan

Run `python scripts/scan_test_coverage.py . .sdd-delivery/<feature>` to find tests that reference SPEC-* IDs. This confirms that tests trace back to Spec. In No-Python mode, grep for `SPEC-` in test files manually.
