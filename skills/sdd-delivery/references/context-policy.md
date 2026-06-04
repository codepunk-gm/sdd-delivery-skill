# Context Policy

## Context layers

Long-term:
- team rules
- review standards
- test policy

Feature-level:
- PRD, Spec, reviews, trace matrix, solution, tasks, checkpoint, observability

Task-level:
- active task
- relevant Spec items
- relevant files
- targeted command output

## Loading rules

- Load current phase artifacts before searching broadly.
- Prefer trace matrix to rediscovering requirement context.
- Prefer relevant file reads over whole-repo scans.
- Summarize large command output before adding it to context.
- Mark repo facts with sources.

## Compaction rules

Before compaction, update:
- `11-checkpoint.json`
- `12-observability.md`
- `events.jsonl`

Retain:
- active phase and task
- gate status
- open blockers
- PRD/Spec coverage status
- changed files
- tests run
- next action

Do not retain:
- large logs
- full source files
- duplicate summaries
- unverified guesses
