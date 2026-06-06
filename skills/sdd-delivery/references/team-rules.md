# Team Rules

Customize this file for your team. The defaults below apply to all teams. Add team-specific conventions at the bottom.

## How to Customize

1. Keep the default rules (they encode SDD Delivery principles).
2. Add team-specific sections for: coding standards, test frameworks, file organization, review expectations.
3. If a team rule contradicts a default rule, state the override explicitly and provide rationale.
4. Version this file alongside your project. Review it quarterly.

## Startup Setup

At the beginning of a new workflow, ask whether the user wants to configure team rules:

```text
是否现在配置团队规则？
1. 使用默认规则（推荐）
2. 快速配置：语言、测试框架、代码原则
3. 跳过，后续再配置
```

Record the result in `11-checkpoint.json` under `preferences.team_rule_setup`.

When scripts are available, initialize or validate structured team rules:

```bash
python scripts/setup_team_rules.py --root . --init
python scripts/setup_team_rules.py --root . --language zh --test-framework pytest --coverage-target 80%
python scripts/setup_team_rules.py --root . --validate
```

The generated file is `.sdd-delivery/team-rules.json`. It is the project-level configuration for language, test framework, code principle modules, thresholds, naming glossary, and review defaults.

If the user chooses quick configuration, ask at most 3 questions:

1. Artifact/comment language: `auto`, `zh`, `en`, or `bilingual`.
2. Test framework and coverage target.
3. Code principle modules to enable from `references/code-principles.md`.

Do not block the workflow if the user skips setup. Use the default rules below.

## Default Rules (All Teams)

- Preserve Chinese text and use UTF-8. Never introduce mojibake.
- Follow the repository architecture. New code should match existing patterns.
- Keep diffs minimal and reviewable. One concern per PR.
- Do not make unrelated formatting-only changes in functional PRs.
- Do not lower test quality to pass checks.
- Spec is mandatory before PRD review (Constitution Principle 1).
- Technical solution must be approved and reviewed before implementation (Gates 6-7).
- Unit test plan and report are required for delivery (Gates 10-11).
- Keep DevFlow artifacts under `.sdd-delivery/<feature>/`.
- Write tests BEFORE implementation code (RED → GREEN → REFACTOR).

## Customization Points

### Code Principles (Pluggable Modules)

Enable or disable implementation-level principles from `references/code-principles.md`. Each module can be independently toggled. Enabled modules are checked at Per-Task Review and Delivery Review.

```markdown
## Team Code Principles

code_principles:
  design_patterns: true    # A: 设计模式（Interface First, Single Responsibility, Strategy）
  extensibility: true      # B: 可扩展性（Open-Closed, 组合优于继承, Feature Flags）
  size_limits: true        # C: 文件/函数/参数长度约束（300行/50行/5参数）
  naming: true             # D: 命名见名知意（No 缩写, 单位后缀, 动词+名词）
  error_handling: true     # E: 错误处理（Typed Errors, Never Swallow, Errors as Values）
  review_checklist: true   # F: 代码审查清单（Correctness/Design/Tests/Naming/Size/Boundary/Errors）
```

**To disable a module:** set it to `false`. The module's checks are skipped at review gates.

**To customize a threshold:** override the specific value:

```markdown
code_principles:
  size_limits:
    max_file_lines: 400     # default: 300
    max_function_lines: 60  # default: 50
    max_params: 6           # default: 5
```

**To add team-specific naming rules:**

```markdown
code_principles:
  naming:
    allowed_abbreviations: [ctx, cfg, repo, svc]  # team glossary
    boolean_prefix: [is, has, should, can, allow]  # custom prefixes
```

### Code Style
- Language-specific conventions (PEP 8, ESLint, gofmt, etc.)
- Naming conventions (camelCase, snake_case, PascalCase)
- Comment language (English, Chinese, or bilingual)

### Language Preference
- Artifact language: auto-detect by default.
- Prefer the user's language from the current request when clear.
- If the repo has `AGENTS.md`, README, or existing `.sdd-delivery` artifacts in a dominant language, use that language.
- Do not use network location as the primary signal. Network region may be wrong; it can only be a weak fallback when no better evidence exists.
- Record the chosen language in `11-checkpoint.json` under `preferences.delivery_language`.

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
