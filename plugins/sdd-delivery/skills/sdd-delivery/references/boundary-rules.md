# Boundary Rules

Boundaries are not overhead. They are what lets you move freely inside while protecting the outside.

— Adapted from cc-sdd design philosophy

## Boundary Annotation (`_Boundary:_`)

Marks what a task, decision, or section explicitly does NOT include. Every implementation task must declare its boundary.

**Format:** `_Boundary:_ <files, directories, or concerns explicitly excluded>`

**Examples:**
```
_Boundary:_ src/services/auth/ only. Do not touch src/routes/ or src/models/.

_Boundary:_ Frontend login form component only. API contract and backend auth logic are out of scope.

_Boundary:_ Read-only analysis. No code changes.
```

**Where to use:**
- Every task in `06-implementation-tasks.md`
- Spec items that scope a specific subsystem
- Review findings that are intentionally deferred

## Dependency Annotation (`_Depends:_`)

Marks what must exist or be decided before this item can proceed.

**Format:** `_Depends:_ <task ID, decision, or artifact>`

**Examples:**
```
_Depends:_ T1 (database schema), T2 (user model)

_Depends:_ SPEC-3 acceptance criteria clarification

_Depends:_ 04-tech-solution.md section 3 (API contract)
```

## Parallel Marker (`[P]`)

Marks tasks that can run concurrently because they:
- Touch different files with no overlap
- Have no data model dependency between them
- Can be verified independently

**Format:** `- [ ] T[N] [P] [SpecItem] Description with file path`

**Example:**
```
- [ ] T3 [P] [SPEC-1] Implement AuthService in src/services/auth/auth_service.py
- [ ] T4 [P] [SPEC-2] Implement UserProfile in src/services/user/profile_service.py
```

## Enforcement

### At Task Creation (phase 9)
- Every task must include `_Boundary:_`. Missing boundary = task is underspecified.
- Every task that depends on another must include `_Depends:_`.
- Tasks without shared dependencies should be marked `[P]`.

### At Per-Task Review (phase 10)
- **Boundary violation is a P0 rejection.** If a task modifies files outside its declared boundary, reject regardless of code quality. The task must be split or the boundary updated.
- **Missing dependency check.** If a task's `_Depends:_` prerequisite is incomplete, block until resolved.

### At Delivery Review (phase 13)
- Verify all task boundaries are satisfied. Cross-reference changed files in `07-implementation-log.md` with declared boundaries.
- Flag any boundary expansion that was not explicitly reviewed.

## Boundary Philosophy

A boundary is not a limitation — it is a contract:
- **For the implementer:** You can change anything inside the boundary freely.
- **For the reviewer:** You only need to verify that the outside is untouched.
- **For the team:** You know exactly what was changed and what was not.
