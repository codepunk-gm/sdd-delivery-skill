# Checkpoint Schema

Use `11-checkpoint.json` as the source of truth for recovery.

Required top-level fields:

```json
{
  "schema_version": "2.0",
  "feature": "",
  "goal": "",
  "current_phase": "",
  "active_task": "",
  "gate_status": {
    "clarify": "pending",
    "spec": "pending",
    "spec_review": "pending",
    "analyze": "pending",
    "solution": "pending",
    "solution_approval": "pending",
    "solution_review": "pending",
    "tdd": "pending",
    "per_task_review": "pending",
    "unit_test_plan": "pending",
    "test_report": "pending",
    "delivery_review": "pending"
  },
  "completed_tasks": [],
  "pending_tasks": [],
  "enabled_capabilities": [],
  "capability_executor_plan": [],
  "capabilities": {
    "frontend_template": {
      "state": "ask",
      "reason": "",
      "source": "default",
      "updated_at": ""
    }
  },
  "preferences": {
    "delivery_language": "auto",
    "comment_language": "auto",
    "team_rule_setup": "pending"
  },
  "solution_approval": {
    "status": "pending",
    "approver": "",
    "notes": "",
    "source": "",
    "time": ""
  },
  "milestones": [],
  "human_reviews": [],
  "quality_status": {},
  "decisions": [],
  "repo_facts": [],
  "changed_files": [],
  "tests_run": [],
  "metrics": {},
  "risks": [],
  "blockers": [],
  "next_action": "",
  "updated_at": ""
}
```

Capability switch object:

```json
{
  "state": "enabled|disabled|ask",
  "reason": "",
  "source": "",
  "updated_at": ""
}
```

Required capability IDs:

- `frontend_template`
- `java_modular_project`
- `mcp_component_protocol`
- `github_delivery_assets`
- `team_code_principles`

`enabled_capabilities` is kept as a compatibility index. The structured `capabilities` object is authoritative.

Capability executor plan object:

```json
{
  "id": "frontend_template",
  "state": "enabled",
  "executor": "phase-instructions",
  "phases": ["technical-solution", "implementation-tasks"],
  "reference": "references/capability-registry.md#frontend-template-module",
  "command": ""
}
```

Preferences object:

```json
{
  "delivery_language": "auto|zh|en|bilingual",
  "comment_language": "auto|zh|en|bilingual",
  "team_rule_setup": "pending|configured|skipped"
}
```

Solution approval object:

```json
{
  "status": "pending|approved|changes_requested|rejected",
  "approver": "",
  "notes": "",
  "source": "",
  "time": ""
}
```

Milestone object:

```json
{
  "id": "M1",
  "name": "需求基线",
  "status": "pending|in_review|reviewed|accepted_risk|blocked",
  "gates": ["clarify", "spec", "spec_review", "analyze"],
  "evidence": ["00-prd.md", "01-spec.md"],
  "reviewer": "",
  "updated_at": ""
}
```

Default milestones:

- `M1 需求基线` — PRD, clarification, Spec, Spec review, and analysis are ready for review.
- `M2 方案确认` — technical solution, solution approval, and solution review are ready for review.
- `M3 实现受控` — task split and implementation log show bounded progress.
- `M4 验证完成` — unit test plan and report provide verification evidence.
- `M5 交付就绪` — delivery review, checkpoint, and observability support handoff.

Human review object:

```json
{
  "time": "",
  "reviewer": "",
  "target": "M1|M2|M3|M4|M5|artifact path|task id",
  "result": "pass|changes_requested|accepted_risk|blocked",
  "notes": ""
}
```

Quality status object:

```json
{
  "progress": "pending|on_track|at_risk|blocked",
  "traceability": "pending|sufficient|gap|blocked",
  "test_evidence": "pending|sufficient|gap|blocked",
  "review_readiness": "pending|ready|changes_requested|blocked",
  "delivery_confidence": "pending|high|medium|low|blocked"
}
```

Decision object:

```json
{
  "decision": "",
  "reason": "",
  "source": ""
}
```

Repo fact object:

```json
{
  "fact": "",
  "source": "",
  "staleness": "fresh"
}
```

Test run object:

```json
{
  "command": "",
  "status": "passed|failed|skipped",
  "summary": "",
  "source": ""
}
```
