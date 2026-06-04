# Task Splitting

Good tasks are small, bounded, and verifiable. Every task must include `_Boundary:_` and `_Depends:_` annotations.

## Task Format

Each task must include:

```markdown
### T1: [P] [SpecItem] Goal summary

_Boundary:_ <files/directories this task does NOT touch>
_Depends:_ <task IDs or decisions this task requires>
_Size:_ <XS|S|M|L>
_Spec Items:_ <SPEC-1, SPEC-2, ...>

- [ ] T1 [P] [SPEC-1] Description with exact file paths

**Files:** <paths to create or modify>
**Verification:** <how to confirm this task is done>
```

**Example:**
```markdown
### T3: [P] [SPEC-1, SPEC-3] Implement AuthService

_Boundary:_ src/services/auth/ only. Do not touch src/routes/ or src/models/.
_Depends:_ T1 (database schema), T2 (user model)
_Size:_ M
_Spec Items:_ SPEC-1, SPEC-3

- [ ] T3 [P] [SPEC-1] Implement AuthService.login in src/services/auth/auth_service.py
- [ ] T3 [P] [SPEC-3] Implement AuthService.validate_session in src/services/auth/auth_service.py

**Files:** src/services/auth/auth_service.py, src/services/auth/__init__.py
**Verification:** `pytest tests/services/auth/test_auth_service.py -v`
```

## Splitting Heuristics

Split by:
- **Interface change:** API signature, protocol, or contract modification.
- **Data model change:** Schema, migration, or data access layer.
- **Implementation layer:** Service, repository, controller, view — one layer at a time.
- **Migration:** Database or config migration separate from feature code.
- **Tests:** Tests can be a separate task when the implementation task is large, but the test task must complete first (RED before GREEN).
- **Documentation:** README, API docs, changelog.

Avoid tasks that:
- Say only "implement feature" (underspecified).
- Span more than 3 modules (boundary too wide).
- Mix refactor and behavior change (two concerns).
- Have no verification path (how do you know it's done?).
- Require hidden context from chat (must be self-contained).
- Exceed 200 lines of change (L size — split first).

## Parallel Marker `[P]`

Mark tasks with `[P]` prefix when ALL of:
- No shared files with other `[P]` tasks.
- No data model dependency between them.
- Can be verified independently.

Tasks without `[P]` are sequential. The agent should suggest which tasks can be parallelized.

## Per-Task Review Protocol

After completing each task and before starting the next:

1. **Boundary check:** Are all changed files within the declared `_Boundary:_`? Violation = P0 rejection.
2. **Test check:** Do tests pass (GREEN)? Any regressions?
3. **Scope check:** Were any unrelated files modified? If yes, revert or document why.
4. **Log update:** Record the task completion in `07-implementation-log.md`.
5. **Checkpoint update:** Run `write_checkpoint.py` or manually update `11-checkpoint.json`.
6. **Learning propagation:** Add any cross-task insights to `## Implementation Notes` in `06-implementation-tasks.md`.

If the independent reviewer finds issues:
- **1st rejection:** Fix and resubmit.
- **2nd rejection:** Spawn a debug pass (investigate root cause in clean context) before attempting fix #3.

## Estimation

Assign a size to every task using `references/estimation.md`:
- **XS:** 1-10 lines (5 min review)
- **S:** 10-50 lines (15 min review)
- **M:** 50-200 lines (30 min review)
- **L:** 200-500 lines (1 hr review)
- **XL:** 500+ lines — **MUST split before implementation**

A healthy task plan: mostly S/M, a few XS, zero XL.

## Implementation Loop (Per Task)

1. Restate Context Contract with the task's specific boundary and dependencies.
2. Read only relevant artifacts and files (context-policy.md).
3. Write the test FIRST. Run it. Confirm RED.
4. Implement minimal change. Run test. Confirm GREEN.
5. Refactor while keeping green.
6. Verify no boundary violations.
7. Update task state, implementation log, and checkpoint.
