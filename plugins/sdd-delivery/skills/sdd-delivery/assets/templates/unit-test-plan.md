# Unit Test Plan

> Instructions: Write tests BEFORE implementation (RED → GREEN → REFACTOR). Map every test to a Spec acceptance criterion. Update status as tests progress through the TDD cycle.

## Test Cases

| Test ID | Spec ID | Scenario (Given/When/Then) | Input / Setup | Expected Result | Test Target | Status |
|---|---|---|---|---|---|---|
| UT-1 | SPEC-1 | Valid login: given valid credentials, when login is called, then return token | Mock auth service, valid user in DB | HTTP 200 + JWT token | test_auth.py::test_valid_login | red |
| UT-2 | SPEC-2 | Invalid login: given wrong password, when login is called, then return error | Mock auth service, valid user in DB | HTTP 401 + error message | test_auth.py::test_invalid_login | pending |

## TDD Order

Tests should be written and executed in this order:

1. UT-1: Valid login (happy path first)
2. UT-2: Invalid credentials (error path)
3. UT-3: Missing fields (edge case)
4. ...

## Coverage Targets

- Spec items to cover: X / Y
- P0 items covered: must be 100%
- Edge cases covered: X / Y
- Accepted gaps: [list with reasons]

## Status Legend

| Status | Meaning |
|--------|---------|
| pending | Not yet written |
| red | Written, runs, and FAILS (feature not implemented yet) |
| green | Written, runs, and PASSES (implementation complete) |
| refactored | Code cleaned up while tests stay green |
| skipped | Intentionally skipped (reason documented) |
