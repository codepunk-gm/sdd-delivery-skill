# Analyze Rubric

Cross-artifact consistency check. Run after Spec Review (phase 4) and after Task Splitting (phase 9). This is a read-only analysis — it does not modify artifacts, only reports findings.

Adapted from Spec-Kit's `/speckit.analyze` phase.

## When to Run

**Analysis 1 (post-Spec):** After Spec Review (phase 4), before Technical Solution (phase 7).
**Analysis 2 (post-Tasks):** After Implementation Tasks (phase 9), before Implementation (phase 10).

## Four Detection Passes

### Pass 1: Duplications

Check: Is the same requirement, acceptance criterion, or task described in two places with different wording?

| Artifacts | What to check |
|-----------|--------------|
| 00-prd.md ↔ 01-spec.md | Same PRD item mapped to two different Spec items? |
| 01-spec.md ↔ 06-implementation-tasks.md | Same behavior implemented by two different tasks? |
| 04-tech-solution.md ↔ 06-implementation-tasks.md | Same design decision described in two tasks? |

**Severity:** P2 (maintenance risk, not functional).

### Pass 2: Ambiguities

Check: Any requirement, acceptance criterion, or task description that uses vague language without concrete criteria?

Signals:
- "fast", "scalable", "robust", "user-friendly", "intuitive" (no measurable definition)
- "etc.", "and so on", "as needed" (unbounded scope)
- "should" without acceptance criteria
- Task descriptions without file paths

**Severity:** P0 (blocks implementation) if acceptance criteria are missing. P1 (degrades quality) if non-functional requirements are vague.

### Pass 3: Underspecified Items

Check: Items that reference other items without those items existing.

| Pattern | Example | Severity |
|---------|---------|----------|
| Spec item references PRD item that doesn't exist | SPEC-5 maps to PRD-99 (not found) | P0 |
| Task references Spec item that doesn't exist | T3 claims SPEC-15 (not found) | P0 |
| Task `_Depends:_` on task not in the plan | T5 depends on T99 (not found) | P0 |
| Acceptance criterion references a metric not defined | "loads in <target>ms" with no target value | P1 |
| Task has no file paths | "Implement login" with no file locations | P1 |

### Pass 4: Constitution Conflicts

Check: Any artifact content that violates a principle in `references/constitution.md`.

| Constitution Principle | What to Check |
|----------------------|--------------|
| Spec Before Code | Are there implementation tasks with no corresponding Spec items? |
| Traceability Forever | Are PRD items missing from the trace matrix? |
| Minimal Diffs | Does any task touch files outside its declared boundary? |
| Evidence Over Assertion | Are there design claims with no repo evidence? |

**Severity:** P0 if a core principle is violated. P1 if a supporting principle is weakened.

## Output Format

Add an `## Analysis` section to `03-requirement-trace.md`:

```markdown
## Analysis (post-Spec)

### Pass 1: Duplications
- [Finding or "None found"]

### Pass 2: Ambiguities
- P0: SPEC-3 acceptance criterion is "system should be fast" — no measurable target
- P1: SPEC-7 uses "etc." — unbounded scope

### Pass 3: Underspecified
- P0: SPEC-5 references PRD-99 which does not exist
- [Continue or "All references resolved"]

### Pass 4: Constitution Conflicts
- [Finding or "No constitution violations detected"]

### Summary
- P0: N | P1: N | P2: N
- Blocks Technical Solution: Yes/No
```

## Severity Thresholds

- **Blocks next phase:** Any P0 finding.
- **Warns but proceeds:** Only P1/P2 findings, or P0 findings accepted by user.
- **Clean:** No findings.

## Max Findings Rule

Report at most 20 findings per analysis pass. Triage by severity, then by impact. Remaining items go to `## Deferred Findings`.
