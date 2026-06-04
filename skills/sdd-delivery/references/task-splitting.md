# Task Splitting

Good tasks are small, bounded, and verifiable.

## Task format

Each task should include:
- ID
- Goal
- Scope
- Out of scope
- Files
- Dependencies
- Completion criteria
- Verification command or method

## Splitting heuristics

Split by:
- interface change
- data model change
- implementation layer
- migration
- tests
- docs

Avoid tasks that:
- say only "implement feature"
- span too many modules
- mix refactor and behavior change
- have no verification path
- require hidden context from chat

## Implementation loop

For each task:
1. Restate Context Contract.
2. Read only relevant artifacts and files.
3. Implement minimal change.
4. Verify.
5. Update task state and checkpoint.
