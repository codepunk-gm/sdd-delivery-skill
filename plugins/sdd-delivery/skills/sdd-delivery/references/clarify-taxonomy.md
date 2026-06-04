# Clarify Taxonomy

Run a taxonomy scan against the PRD before writing Spec. Flag unresolved ambiguities, present findings, and ask before proceeding. Max 5 questions per session — triage on highest impact.

## When to Run

After PRD Intake (phase 1), before Spec Authoring (phase 3). Also re-run if the PRD is updated mid-workflow.

## Ambiguity Categories

Scan each PRD item against these categories:

| # | Category | Signal | Required Action | Example |
|---|----------|--------|-----------------|---------|
| 1 | Missing Actor | No user/system role specified | Name the actor | "When clicked" → "When the admin clicks Submit" |
| 2 | Missing Constraint | No performance, capacity, or security limit | Define the limit | "List items" → "List up to 50 items, paginated" |
| 3 | Missing Edge Case | No error, empty, timeout, or race condition behavior | Define the fallback | "Show result" → "Show result or 'No matching records' empty state" |
| 4 | Vague Verb | Non-deterministic action (process, handle, manage, support) | Define the concrete behavior | "Process payment" → "Validate amount, charge via Stripe, record transaction" |
| 5 | Missing Acceptance Criteria | No observable, testable outcome | Define acceptance criteria | "Fast loading" → "Page loads in <2s at p95 with 100 concurrent users" |
| 6 | Conflicting Priority | Two must-haves that cannot both ship in the same iteration | Resolve priority ordering | "Must support both MySQL and PostgreSQL in v1" when only one can ship |
| 7 | Missing Scope Boundary | No explicit in-scope/out-of-scope declaration | Declare what is NOT included | "Add login" → "Add email+password login. SSO and OAuth are out of scope." |
| 8 | Undefined Data Shape | Field names, types, or relationships unspecified | Define the data model | "User profile" → "User {id: uuid, name: string, email: string, role: enum}" |
| 9 | Missing Integration | External system interaction unspecified | Define the contract | "Send notification" → "POST to /api/notifications with {userId, title, body}" |
| 10 | Unclear Completion Signal | No definition of "done" | Define the completion criteria | "Improve search" → "Search returns results in <500ms, relevancy score ≥0.8" |

## Question Format

For each unresolved category, present findings in one of two formats:

**Multiple-Choice (2-5 discrete options):**
```
**Q1: [Category]** [Question]

Recommended: Option B — [brief reasoning]

| Option | Description |
|--------|-------------|
| A | [description] |
| B | [description] |
```

**Short-Answer (no obvious options):**
```
**Q1: [Category]** [Question]

Suggested: [proposed answer] — [brief reasoning]
Format: Short answer (≤5 words).
```

## Resolution

1. Present findings grouped by severity: P0 (blocks Spec), P1 (degrades Spec quality), P2 (nice to clarify).
2. After user answers, record resolutions in `00-prd.md` under `## Clarify Scan`.
3. Unresolved P0/P1 items become gate blockers at Spec Authoring.
4. Overrides (user accepts ambiguity) are recorded as accepted risks in `01-spec.md`.

## Max Questions Rule

Present at most 5 questions per session. Triage: P0 questions first, then highest-impact P1 questions. Remaining items are documented as `## Deferred Clarifications` for the next session.