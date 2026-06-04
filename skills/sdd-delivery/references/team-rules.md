# Team Rules

Customize this file for your team. The defaults below apply to all teams. Add team-specific conventions at the bottom.

## How to Customize

1. Keep the default rules (they encode SDD Delivery principles).
2. Add team-specific sections for: coding standards, test frameworks, file organization, review expectations.
3. If a team rule contradicts a default rule, state the override explicitly and provide rationale.
4. Version this file alongside your project. Review it quarterly.

## Default Rules (All Teams)

- Preserve Chinese text and use UTF-8. Never introduce mojibake.
- Follow the repository architecture. New code should match existing patterns.
- Keep diffs minimal and reviewable. One concern per PR.
- Do not make unrelated formatting-only changes in functional PRs.
- Do not lower test quality to pass checks.
- Spec is mandatory before PRD review (Constitution Principle 1).
- Technical solution must be reviewed before implementation (Gate 6).
- Unit test plan and report are required for delivery (Gates 9-10).
- Keep DevFlow artifacts under `.sdd-delivery/<feature>/`.
- Write tests BEFORE implementation code (RED → GREEN → REFACTOR).

## Customization Points

### Code Style
- Language-specific conventions (PEP 8, ESLint, gofmt, etc.)
- Naming conventions (camelCase, snake_case, PascalCase)
- Comment language (English, Chinese, or bilingual)

### Test Framework
- Preferred test framework (pytest, Jest, Go testing, etc.)
- Test file naming convention (test_*.py, *.test.ts, *_test.go)
- Coverage tool and minimum threshold

### Review Expectations
- Review turnaround SLA (e.g., "within 4 business hours")
- Required reviewers per PR
- Severity definitions (customize P0-P3 if needed)

### File Organization
- Feature module structure
- Test file location (co-located vs. separate test directory)

## Example: Python Team

```markdown
## Team-specific rules

### Code Style
- Follow PEP 8. Max line length: 100.
- Use type hints for all function signatures.
- Docstrings in Google style.

### Test Framework
- Use pytest. Test files named test_*.py alongside source.
- Coverage minimum: 80% line coverage.
- Run `pytest --cov` before committing.

### Review
- At least one reviewer per PR.
- Review within 1 business day.
- P0 findings block merge. P1 should be fixed or tracked.
```

## Example: TypeScript Team

```markdown
## Team-specific rules

### Code Style
- Use ESLint with Prettier. No semicolons.
- Prefer `interface` over `type` for object shapes.
- Use Zod for runtime validation at API boundaries.

### Test Framework
- Use Vitest. Test files named *.test.ts alongside source.
- Coverage minimum: 85% branch coverage.
- Run `vitest --coverage` before committing.

### Review
- At least one reviewer per PR. Use conventional commits.
- Review within 4 business hours.
- Every PR must include a screenshot or GIF for UI changes.
```
