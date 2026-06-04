# Estimation and Sizing

Task size estimation prevents oversized tasks from bypassing review. Assign a size to every task before implementation.

## Size Categories

| Size | Lines Changed | Review Time | Typical Scope | Example |
|------|--------------|-------------|---------------|---------|
| XS | 1-10 | 5 min | Typo, config value, docstring | Fix a misspelled variable name |
| S | 10-50 | 15 min | Single function, one test | Add a validation function + test |
| M | 50-200 | 30 min | New module, multiple tests | Implement a new service class + tests |
| L | 200-500 | 1 hr | New feature with tests + migration | Add OAuth login with DB migration |
| XL | 500+ | Split first | Too large — must decompose | Full payment system |

## The XL Rule

Any task estimated as XL **must be split** before implementation begins.

**Splitting heuristic:**
1. Identify sub-capabilities within the XL task.
2. Extract each sub-capability into its own task.
3. Mark dependencies between split tasks with `_Depends:_`.
4. Re-estimate each split task. If any is still XL, split again.

**Example:**
```
XL: "Add payment system" (800 lines)
→ M: "Add Payment model and migration" (100 lines, no deps)
→ M: "Add Stripe integration service" (150 lines, _Depends:_ Payment model)
→ M: "Add payment API endpoint" (100 lines, _Depends:_ Stripe integration)
→ S: "Add payment unit tests" (80 lines, _Depends:_ all above)
→ S: "Add payment error handling" (60 lines, _Depends:_ Stripe integration)
```

## Task Size Distribution

A healthy task plan should have:
- Mostly S and M tasks (predictable, reviewable in one sitting)
- A few XS tasks (trivial fixes)
- Zero XL tasks (always split first)
- L tasks are acceptable but should be reviewed for split opportunities

## Red Flags

- **All tasks are XS/S:** May indicate over-decomposition. Combine related tiny tasks.
- **Any XL task:** Must split. No exceptions without explicit user override.
- **No M tasks:** May indicate tasks are too granular to be independently verifiable.
- **All tasks in one file:** May indicate tasks are not properly bounded.

## Estimation in No-Python Mode

Estimation is always manual — no script is needed. For each task in `06-implementation-tasks.md`:
1. List the files that will be changed.
2. Estimate lines changed per file.
3. Sum and assign size category.
4. If XL, split before proceeding.
