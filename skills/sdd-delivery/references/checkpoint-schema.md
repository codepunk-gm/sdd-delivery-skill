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
    "solution_review": "pending",
    "tdd": "pending",
    "per_task_review": "pending",
    "unit_test_plan": "pending",
    "test_report": "pending",
    "delivery_review": "pending"
  },
  "completed_tasks": [],
  "pending_tasks": [],
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
