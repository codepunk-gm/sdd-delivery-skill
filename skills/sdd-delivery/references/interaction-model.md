# Interaction Model

SDD Delivery should feel guided, friendly, and recoverable. The agent should not behave like a raw script runner.

## UX principles

- Start with a small menu, not a long lecture.
- Ask at most 1-3 questions at a time.
- Prefer numbered choices so users can reply with a number.
- Show the current phase and next action.
- Explain when a gate blocks progress and how to unblock it.
- Do not dump large artifacts in chat; write files and summarize.
- Always offer a safe next step.
- If automation is unavailable, continue manually instead of failing.

## Default guided opening

When the user starts without a specific phase, respond like this:

```text
I can guide this with SDD Delivery:
1. PRD to Spec
2. Spec Review
3. Technical Solution
4. Solution Review
5. Implementation Tasks
6. Code Implementation
7. Unit Test Plan / Report
8. Trace / Coverage
9. GitHub PR / CI Assets
10. Checkpoint / Handoff

Send a PRD, choose a number, or say "quick mode" for a lightweight path.
```

## Phase card

At the start of each phase, show a short phase card:

```text
Phase: Spec Review
Input: 01-spec.md
Output: 02-spec-review.md
Gate: Spec review must pass before technical solution
Next: fix findings or continue with accepted risk
```

## Progress update

After a meaningful action, summarize in this shape:

```text
Done:
- Updated 01-spec.md
- Added 3 rows to 03-requirement-trace.md
- Wrote checkpoint

Status:
- Spec review: pending
- Trace coverage: 3 PRD items / 3 Spec items

Next:
1. Run Spec Review
2. Edit Spec acceptance criteria
3. Continue to Technical Solution with accepted risk
```

## Gate interaction

When a gate is not passed:

```text
Spec Review found blockers:
- P1: SPEC-2 has no observable acceptance criteria

Choose next step:
1. Fix Spec now
2. Mark as accepted risk and continue
3. Stop and checkpoint
```

## Codex client behavior

When a Codex client supports structured user input or choice UI, use it for phase choices. If not available, use plain numbered lists.

Do not require the user to remember commands. Offer both:
- natural-language action
- optional script command

Example:

```text
I can update the observability dashboard now. If Python is available, I will use:
python scripts/sync_observability.py .op/devflow/<feature>
Otherwise I will update 12-observability.md manually.
```

## Quick mode

For small tasks, offer quick mode:

```text
This looks small. Choose:
1. Quick mode: minimal change + brief verification
2. Full SDD Delivery: Spec, review, trace, tests, checkpoint
```

Quick mode still preserves project instructions and should not make unrelated changes.

## Recovery mode

When continuing work:

```text
I found an existing DevFlow folder.
Current phase: implementation
Active task: T2
Next action: add unit tests

Choose:
1. Continue next action
2. Review current artifacts
3. Rebuild observability
4. Stop and checkpoint
```
