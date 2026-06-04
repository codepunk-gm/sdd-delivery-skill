# Spec Review

> Instructions: Fill findings first (severity-ordered P0→P3). Check each category. Do not resolve a finding without updating the related artifact. Then record gate result.

## Gate Result

Status: pending (pending | in_review | passed | accepted_risk | blocked)

## Findings

| # | Severity | Category | Finding | Related Item | Suggestion | Status |
|---|---|---|---|---|---|---|---|
| 1 | P0 | Missing AC | SPEC-3 has no acceptance criteria | SPEC-3 | Add "User receives email within 30 seconds" | Open |

## Coverage Check

- [ ] Every P0/P1 PRD item has a corresponding Spec item
- [ ] Every Spec item has acceptance criteria
- [ ] Non-goals are explicitly listed
- [ ] Boundaries (`_Boundary:_`) declared for cross-cutting items

## Clarity Check

- [ ] No ambiguous verbs (process, handle, manage, support) without concrete definition
- [ ] No vague adjectives (fast, scalable, robust) without measurable criteria
- [ ] No "etc.", "and so on", or unbounded scope markers

## Testability Check

- [ ] Every acceptance criterion describes an observable outcome
- [ ] Edge cases (error, empty, race, timeout) are covered
- [ ] Test framework and approach are feasible for this Spec

## Constitution Check

- [ ] Spec Before Code: No implementation details in Spec
- [ ] Evidence Over Assertion: Spec claims are grounded in PRD evidence
- [ ] Traceability Forever: Spec items can be mapped to code

## Decision

- [ ] Proceed to Technical Solution (gate passed)
- [ ] Proceed with accepted risks (list below)
- [ ] Blocked (P0 issues must be resolved first)

### Accepted Risks

| Risk | Reason | Accepted By | Expiry |
|------|--------|-------------|--------|
