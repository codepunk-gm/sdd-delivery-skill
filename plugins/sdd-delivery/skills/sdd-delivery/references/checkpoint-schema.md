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
