# Code Principles

Pluggable implementation principles for SDD Delivery. Each module can be independently enabled or disabled in `references/team-rules.md`. Principles are inspired by open-source SDD patterns including superpowers, Spec-Kit, and Claude Code's internal architecture.

## How Principles Work

- **Opt-in by module.** Enable only what fits your team. No principle is forced.
- **Gate-integrated.** Enabled modules are checked at Per-Task Review (Gate 9) and Delivery Review (Gate 12).
- **Tool-agnostic.** Principles apply whether writing TypeScript, Python, Go, Rust, or any other language.
- **Override with reason.** If a principle conflicts with a specific case, state the conflict and get user confirmation.

---

## Module A: 设计模式 (Design Patterns)

Toggle: `code_principles.design_patterns: true`

### A1. Interface / Contract First

Define contracts before implementation. Write the type signature, schema, or interface first — then implement behind it.

```
Why: Contracts make boundaries explicit. Reviewers verify behavior against
the contract without reading implementation details.

Apply:
- TypeScript: define interface/type before function body
- Python: write Protocol or ABC before concrete class
- Go: define interface before struct
- REST: write OpenAPI spec before handler
- DB: write migration before model code
```

### A2. Single Responsibility

Each module, class, or function does exactly one thing. If the docstring needs "and," split it.

```
Signal you need it: Function name has "and" or "or" — "validateAndSave"
Signal over-applying: One-line wrapper functions that add no abstraction
```

### A3. Strategy / Factory for Extensibility Points

When a decision may change (auth method, payment provider, notification channel), wrap it behind a strategy interface. Inject the strategy; do not hardcode the choice.

```
Example:
- Auth: OAuth2Strategy, SAMLStrategy behind IAuthProvider
- Payment: StripeStrategy, PayPalStrategy behind IPaymentGateway
- Notification: EmailStrategy, SlackStrategy behind INotificationChannel
```

---

## Module B: 可扩展性 (Extensibility)

Toggle: `code_principles.extensibility: true`

### B1. Open-Closed Principle

Open for extension, closed for modification. New behavior = new code, not edited old code.

```
Apply:
- Add a new strategy class rather than a switch-case in existing code
- Add a new middleware rather than editing the core handler
- Add a new migration rather than editing an old one
```

### B2. Composition Over Inheritance

Prefer composing objects over deep inheritance hierarchies. Inheritance chains beyond depth 2 are a smell.

```
Signal over-applying: Every class extends a base class "just in case"
```

### B3. Feature Flags

New behavior behind a flag before it's always-on. Enables dark launching, gradual rollout, and fast rollback.

```
Minimal flag interface:
  if feature_flag("new-checkout"): return newFlow()
  return oldFlow()
```

---

## Module C: 文件与函数约束 (Size Limits)

Toggle: `code_principles.size_limits: true`

### C1. File Length

| Category | Max Lines | Action if exceeded |
|----------|-----------|-------------------|
| Single source file | 300 | Flag for split review |
| Test file | 500 | Flag for split review |
| Configuration file | 200 | Flag for split review |

### C2. Function / Method Length

| Category | Max Lines | Action if exceeded |
|----------|-----------|-------------------|
| Function / method | 50 | Extract helper or sub-function |
| Test case | 30 | Split into multiple scenarios |

### C3. Parameter Count

| Category | Max Count | Action if exceeded |
|----------|-----------|-------------------|
| Function parameters | 5 | Group into a config object / dataclass |
| Constructor dependencies | 7 | Class may have too many responsibilities |

### C4. Import Count

| Category | Max Count | Action if exceeded |
|----------|-----------|-------------------|
| Imports per file | 15 | File may be doing too much |

---

## Module D: 命名见名知意 (Meaningful Naming)

Toggle: `code_principles.naming: true`

### D1. Intent-Revealing Names

A name should answer "what does this do?" without reading the implementation. If a comment is needed to explain the name, rename it.

```
Bad:  d, data, tmp, obj, handle(), process(), doIt()
Good: userEmail, pendingOrders, parsePaymentIntent(), buildInvoice()
```

### D2. No Abbreviations Without Glossary

```
Allowed: id, url, api, db, ui (universally understood)
Not allowed: usr (user), pwd (password), amt (amount), ctx (context in public APIs)
Exception: Domain abbreviations documented in team glossary
```

### D3. Naming Conventions by Role

| Role | Convention | Example |
|------|-----------|---------|
| Boolean | `is_` / `has_` / `should_` / `can_` prefix | `isActive`, `hasPermission` |
| Function | Verb + Noun | `calculateTotal()`, `sendNotification()` |
| Event handler | `on` / `handle` prefix | `onClick`, `handleSubmit` |
| Class / Component | Noun (PascalCase) | `PaymentGateway`, `UserProfile` |
| Constant | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private member | `_` prefix or language-native | `_cache`, `#privateField` |

### D4. Units in Names

When a value has a unit, include it in the name.

```
timeoutMs, retryCount, maxWidthPx, fileSizeBytes, ageYears
```

---

## Module E: 错误处理 (Error Handling)

Toggle: `code_principles.error_handling: true`

### E1. Typed Errors

Throw or return typed errors. Never return a generic "something went wrong" without context.

```
Good: throw new ValidationError("email is required", {field: "email"})
Bad:  throw new Error("invalid")
```

### E2. Errors as Values at Boundaries

At module / API boundaries, return errors as values rather than throwing across the boundary.

```
Pattern: Either<Success, Error> or Result<T, E>
Benefits: Caller must handle the error case. No uncaught exceptions at boundaries.
```

### E3. Never Swallow

Catch only when you can recover. If you catch and re-throw, add context. Never silently swallow.

```
Bad:
  try { ... } catch(e) {}  // swallowed

Good:
  try { ... } catch(e) { throw new PaymentError("Stripe charge failed", {cause: e}) }
```

### E4. Error Language

Error messages in the team's primary language. Technical details in English (for searchability).

---

## Module F: 代码审查 (Review Checklist)

Toggle: `code_principles.review_checklist: true`

Enabled when this module is active, Per-Task Review checks:

- [ ] **Correctness** — Does the code do what the task says?
- [ ] **Design** — Is the approach consistent with existing patterns?
- [ ] **Tests** — Are tests present, passing, and covering edge cases?
- [ ] **Naming** — Are names intent-revealing? (Module D)
- [ ] **Size** — Are file/function/param limits respected? (Module C)
- [ ] **Boundary** — Are changed files within declared `_Boundary:_`?
- [ ] **Error handling** — Are errors typed and never swallowed? (Module E)

---

## Module G: SQL 规范 (SQL Standards)

Toggle: `sql_standards.enabled: true`

SQL standards live in `.sdd-delivery/team-rules.json`, not in ad hoc chat instructions. They support global rules, project overrides, and feature-level exceptions.

### G1. Global Rules

Default global SQL rules:

- no `SELECT *` in production queries
- all user or external inputs use parameterized queries
- no string-concatenated SQL
- pagination requires `LIMIT` and deterministic `ORDER BY`
- filter and join columns need an index plan
- schema changes require migrations
- destructive changes require explicit approval, backfill plan, and rollback plan
- multi-write operations need explicit transaction boundaries

### G2. Project Overrides

Use `sql_standards.project_overrides` for project-specific facts:

- database dialect, such as PostgreSQL, MySQL, SQLite, Oracle
- schema name or tenant layout
- table prefix or legacy naming pattern
- migration tool
- allowed legacy exceptions

Project overrides should explain existing constraints. They should not silently weaken global rules.

### G3. Feature Exceptions

Use `sql_standards.feature_exceptions` for temporary exceptions. Each exception must include:

- `rule`
- `scope`
- `reason`
- `approver`
- `expires`

Feature exceptions are reviewed at Solution Review and Delivery Review.

### G4. Review Checklist

When SQL files, migrations, query builders, ORM models, or data-access code change, check:

- [ ] Query uses parameters rather than string concatenation
- [ ] No production `SELECT *`
- [ ] Pagination has deterministic ordering
- [ ] New filters / joins have an index plan or accepted reason
- [ ] Schema changes have migration, backfill, rollback, and compatibility notes
- [ ] Transaction boundaries are explicit for multi-write flows
- [ ] Project overrides and feature exceptions are recorded in team rules

---

## Per-Language Quick Reference

### TypeScript
```
Interface first → implement behind it
Zod schema at API boundaries → derive types
Max 300 lines / file, 50 lines / function, 5 params
isLoading, hasError for booleans; handleSubmit, fetchUser for functions
throw new DomainError(...); never return error shapes
```

### Python
```
Protocol / ABC first → implement behind it
Pydantic at API boundaries → derive types
Max 300 lines / file, 50 lines / function, 5 params
is_active, has_permission for booleans; calculate_total for functions
raise DomainError(...); return Result at module boundaries
```

### Go
```
Interface first (consumer-side) → implement behind it
Max 300 lines / file, 50 lines / function, 5 params
isActive, hasPermission for booleans; CalculateTotal for functions
Return (T, error); wrap errors with fmt.Errorf("context: %w", err)
```

---

## Integration with SDD Delivery

- **Per-Task Review (Gate 9):** Enabled modules are checked. Boundary + Size violations are P0.
- **Delivery Review (Gate 12):** Full code principles audit against enabled modules.
- **Team Rules:** Toggle modules in `references/team-rules.md`. Add team-specific overrides. SQL standards are maintained in `.sdd-delivery/team-rules.json` with global rules, project overrides, and feature exceptions.

## Design References

- Superpowers (obra/superpowers): TDD, subagent review, auto-trigger composable skills
- Claude Code Superpowers (TechyMT): Schema-first, typed errors, system boundaries
- GitHub Spec-Kit: Constitution-driven gates, artifact-first workflow
- Clean Code (Robert C. Martin): Naming, function size, single responsibility
