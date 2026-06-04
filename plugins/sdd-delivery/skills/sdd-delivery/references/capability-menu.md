# Capability Menu

When starting a new SDD Delivery workflow, present this menu to the user unless they already gave a specific command.

## Supported capabilities

1. PRD to Spec
   - Parse or manually convert PRD into `00-prd.md`, `01-spec.md`, and `03-requirement-trace.md`.

2. Spec Review
   - Review whether Spec is complete, testable, and suitable as the PRD review contract.

3. Technical Solution
   - Produce `04-tech-solution.md` from approved Spec and repo evidence.

4. Solution Review
   - Review architecture, compatibility, security, performance, rollback, and verification strategy.

5. Implementation Tasks
   - Split the approved solution into bounded, traceable tasks in `06-implementation-tasks.md`.

6. Code Implementation
   - Implement one task at a time while maintaining Context Contract, trace, log, and checkpoint.

7. Unit Test Plan and Report
   - Create `08-unit-test-plan.md`, run or document tests, and update `09-unit-test-report.md`.

8. Trace and Coverage
   - Calculate or manually update PRD/Spec/solution/task/code/test coverage.

9. GitHub PR / CI Assets
   - Generate or manually provide PR template and artifact validation workflow.

10. Checkpoint / Handoff
    - Update `11-checkpoint.json`, `12-observability.md`, and next action for compaction or handoff.

## Recommended opening response

Use concise wording:

```text
I can run SDD Delivery in these modes:
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

Send a PRD or choose a number.
```
