# Pre-Mortem Reasoning

Before committing to a solution, imagine it already failed — then work backward to prevent that failure.

Adapted from Don Cheli SDD Framework's `/razonar:pre-mortem` pattern.

## When to Run

1. **Before Technical Solution (phase 7):** "Assume this solution was implemented and failed in production. Why?"
2. **Before Implementation (phase 10):** "Assume this task was completed and broke something. What broke?"

## Protocol

### Step 1: Generate Failure Scenarios

Ask: "Assume the implementation is complete and it FAILED. List 3-5 reasons why."

Focus on:
- Production incidents (data loss, downtime, incorrect results)
- Integration failures (API mismatch, contract breakage)
- Performance degradation (latency spikes, resource exhaustion)
- Security vulnerabilities (data exposure, privilege escalation)
- User experience failures (confusing behavior, broken workflows)

### Step 2: Assess Current Coverage

For each failure scenario, ask:
- Does the current solution already address this?
- If yes: cite the specific design element that mitigates it.
- If no: this is a gap.

### Step 3: Define Mitigations

For each uncovered gap, define at least one mitigation:
- Design change (add validation, add fallback, add circuit breaker)
- Task addition (add a new task to handle the gap)
- Acceptance criteria addition (add a testable condition to the spec)
- Accepted risk (documented reason why mitigation is deferred)

### Step 4: Record

Add a `## Pre-Mortem` section to `04-tech-solution.md`:

```markdown
## Pre-Mortem

### Failure Scenarios

| # | Failure Scenario | Severity | Covered? | Mitigation |
|---|-----------------|----------|----------|------------|
| 1 | Rate limiter blocks legitimate traffic under peak load | HIGH | Partial | Add burst allowance (T3). Accepted risk: fine-tuning thresholds requires production data. |
| 2 | ... | ... | ... | ... |

### Gaps Requiring Attention
- [Item requiring design change or new task]
```

## Pre-Mortem Before Implementation

Before starting implementation (phase 10), run a lighter pre-mortem on the task plan:

1. "If T1 fails, which other tasks are blocked?"
2. "Which task is most likely to reveal a hidden dependency?"
3. "Which task's boundary is most likely to be violated?"

Record findings in `06-implementation-tasks.md` under `## Pre-Implementation Risks`.