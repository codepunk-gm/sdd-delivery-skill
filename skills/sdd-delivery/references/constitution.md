# Constitution

Non-negotiable principles that govern all SDD Delivery phases. Load this at startup. When principles conflict, state the conflict explicitly and ask for user direction. Never override a principle silently.

## Core Principles

Ranked by precedence. Higher principles win on conflict.

### 1. Spec Before Code

No implementation before reviewed Spec. The Spec is the reviewable contract for what will be built.

**Applies to:** PRD intake through implementation.
**Exception:** The user may override for trivial fixes (typos, config values, formatting). Explicit override required.

### 2. Artifacts Over Chat

Structured files over conversation memory. Every decision, finding, and status must live in a `.sdd-delivery/<feature>/` artifact. Chat is for interaction, not for durable state.

**Applies to:** All phases.
**Exception:** None. Even trivial interactions should update a checkpoint before the session ends.

### 3. Gates Before Progress

Unresolved risk must be visible and accepted before the next phase. A gate does not mean "stop work." It means "make the risk visible, then decide."

**Applies to:** All phase transitions.
**Exception:** Quick Mode (user explicitly requests bypass).

### 4. Traceability Forever

Every high-priority PRD item maps to at least one Spec item. Every implementation task traces to a Spec item or documented engineering task. Every acceptance criterion maps to a unit test or documented verification gap.

**Applies to:** Spec through Delivery Review.
**Exception:** Engineering tasks (refactors, tooling) may document their own rationale.

### 5. Minimal, Reviewable Diffs

Do not modify unrelated files. Do not make formatting-only changes in functional PRs. Keep diffs small enough to review in one session.

**Applies to:** Implementation.
**Exception:** Explicitly requested reformatting or migration PRs.

### 6. UTF-8 Always

Read and write all files as UTF-8. Never corrupt CJK characters or other encodings. Never introduce mojibake.

**Applies to:** All file I/O.
**Exception:** None.

### 7. No-Python Universality

Scripts are accelerators, not requirements. The entire workflow must be executable by an agent using only Markdown and JSON editing. If Python is unavailable, do not fail — describe what the script would have done and do it manually.

**Applies to:** All automation.
**Exception:** None.

### 8. Evidence Over Assertion

Every repo fact must have a source (file path + line number or command output). "I think" is not evidence. Stale repo facts must be re-verified before use.

**Applies to:** Technical Solution, Implementation.
**Exception:** User-provided constraints and team rules are accepted as given.

## Principle Precedence

When two principles conflict, the higher-ranked principle wins, but the conflict must be:

1. Stated explicitly: "Principle X (Spec Before Code) conflicts with Principle Y (Minimal Diffs) because..."
2. Resolved with a proposed scope: "I propose limiting Spec to items 1-5 only."
3. Confirmed by the user before proceeding.

## Amendment Process

1. Propose change with rationale.
2. Record in constitution amendment log.
3. Bump constitution version (MAJOR: principle removed/changed, MINOR: principle added, PATCH: wording).

**Version:** 1.0.0 | **Ratified:** 2025-06-04