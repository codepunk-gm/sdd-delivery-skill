# AI Tool Usage Guide

SDD Delivery is designed to work across AI coding tools. The skill is strongest in Codex because it can be packaged as a Codex skill/plugin, but the workflow artifacts are plain Markdown and JSON, so other tools can use them too.

## Codex

Recommended invocation:

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

Chinese invocation:

```text
使用 sdd-delivery，把这个 PRD 转成 Spec、技术方案、审查清单、实现任务、单测计划和可观测交付产物。
```

Codex behavior:
- Load `SKILL.md`.
- Show the capability menu if the user is starting a new workflow.
- Use scripts when Python is available.
- Fall back to natural-language artifact editing when Python is not available.

## Claude Code

Place the skill folder in a repository-accessible location and ask Claude Code to read `SKILL.md` first:

```text
Read sdd-delivery-skill/SKILL.md and follow the SDD Delivery workflow for this PRD. If Python is unavailable, create and update the artifacts manually.
```

Recommended follow-up:

```text
Start with option 1: PRD to Spec. Then run Spec Review before writing the technical solution.
```

Claude Code does not need the scripts to understand the workflow. Scripts are optional accelerators.

## Cursor

Add `SKILL.md` or the relevant references to Cursor context, then prompt:

```text
Follow the SDD Delivery workflow in SKILL.md. Create .sdd-delivery/<feature> artifacts and maintain the requirement trace matrix.
```

Recommended Cursor usage:
- Keep `01-spec.md`, `03-requirement-trace.md`, and `04-tech-solution.md` pinned or in context.
- Ask Cursor to update trace rows whenever code or tests change.

## GitHub Copilot Chat

Use the repository artifacts directly:

```text
Follow the SDD Delivery workflow. Use .sdd-delivery/<feature>/01-spec.md as the source of truth and update 03-requirement-trace.md when implementation or tests change.
```

For PR review:

```text
Review this PR against .sdd-delivery/<feature>/01-spec.md, 03-requirement-trace.md, 04-tech-solution.md, and 09-unit-test-report.md. Findings first.
```

## Windsurf / Continue / Other Agents

Use the plain artifact workflow:

```text
Read sdd-delivery-skill/SKILL.md. If scripts are unavailable, manually create the required .sdd-delivery/<feature> artifacts from the templates and update them as you work.
```

## No Python Mode

If Python is unavailable, do not fail. The agent should perform the same workflow using Markdown/JSON editing:

1. Create `.sdd-delivery/<feature>/`.
2. Copy or recreate the artifact templates.
3. Parse PRD manually into `00-prd.md` and `01-spec.md`.
4. Maintain `03-requirement-trace.md` manually.
5. Record gate status in `11-checkpoint.json`.
6. Update `12-observability.md` manually.
7. Append a short event line to `events.jsonl` when useful.

Scripts improve determinism, but the workflow must remain usable without them.
