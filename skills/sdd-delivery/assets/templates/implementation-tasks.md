# Implementation Tasks

> Instructions: Every task must include `_Boundary:_`, `_Depends:_`, `_Size:_`, and `[P]` marker if parallelizable. No XL tasks. Split tasks that exceed 200 lines. Fill findings first, then tasks.

## Tasks

### T1: [P] [SPEC-1] Implement user login endpoint

_Boundary:_ src/api/auth/ only. Do not touch src/models/ or src/services/.
_Depends:_ None
_Size:_ M

- [ ] T1 [P] [SPEC-1] Implement POST /auth/login in src/api/auth/login.py
  - **Files:** src/api/auth/login.py, src/api/auth/__init__.py
  - **Verify:** `pytest tests/api/auth/test_login.py -v`
  - **Pre-TDD:** Write test first, confirm RED, then implement

### T2: [SPEC-2] Add login rate limiting

_Boundary:_ src/middleware/rate_limit/ only. Do not touch src/api/.
_Depends:_ T1 (login endpoint)
_Size:_ S

- [ ] T2 [SPEC-2] Add rate limiter middleware in src/middleware/rate_limit/login_limiter.py
  - **Files:** src/middleware/rate_limit/login_limiter.py
  - **Verify:** `pytest tests/middleware/rate_limit/test_login_limiter.py -v`

## Implementation Notes

> Cross-task learnings. Update as you progress so later tasks benefit from earlier discoveries.

- T1: [learning]
- T2: [learning]

## Task Sizes

| Task | Size | Lines (est.) | Ready? |
|------|------|-------------|--------|
| T1 | M | ~120 | ✅ (no deps) |
| T2 | S | ~45 | ⏳ (depends on T1) |
