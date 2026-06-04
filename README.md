# SDD Delivery Plugin

This Codex plugin packages the `sdd-delivery` skill for plugin-based installation.


## Visual Overview

> Add generated images to `assets/images/` using the filenames below. The README will render them automatically on GitHub.

### Hero

![SDD Delivery Hero](assets/images/sdd-delivery-hero.png)

`SDD Delivery` is a PRD-driven, Spec-first delivery workflow for AI coding agents. It emphasizes traceability, review gates, and observable delivery.

### Workflow Diagram

![SDD Delivery Workflow](assets/images/workflow-diagram.png)

The workflow connects every delivery stage:

```text
PRD → Spec → Spec Review → Trace Matrix → Technical Solution → Solution Review → Implementation Tasks → Code → Unit Tests → Delivery Review → Checkpoint & Observability
```

### Friendly Guided Interaction

![Friendly Guided Interaction](assets/images/interaction-demo.png)

The skill is designed for guided interaction in Codex and other AI coding clients. Users can send a PRD, choose a number, use quick mode, or continue from a checkpoint.

## What it does

SDD Delivery guides PRD-driven engineering work through:

```text
PRD → Spec → Spec Review → Trace → Tech Solution → Solution Review → Tasks → Code → Unit Tests → Delivery Review → Checkpoint / Observability
```

## Friendly guided interaction

When the skill starts, users get a simple menu:

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

## Install

Install this plugin from a GitHub repository or local path using Codex plugin installation.

After installation, invoke:

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

## Operations

Operational docs are included in:

```text
skills/sdd-delivery/references/plugin-operations.md
```

Use that guide for publishing, versioning, troubleshooting, and update policy.

## Open-source influences

Design references are documented in:

```text
skills/sdd-delivery/references/open-source-influences.md
```

The workflow combines ideas from Spec Kit, OpenSpec-style brownfield changes, Agent Skill progressive disclosure, checkpoint-based context recovery, traceability matrices, and GitHub delivery practices.

## No Python Mode

Python scripts are optional accelerators. If Python is unavailable, the agent should continue by manually creating and updating Markdown/JSON artifacts.

## Included Skill

- `skills/sdd-delivery`: PRD-driven, Spec-first delivery workflow with traceability, tests, checkpoints, observability, and friendly guided interaction.



