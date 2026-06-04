# Checkpoint Schema

Use `11-checkpoint.json` as the source of truth for recovery.

Required top-level fields:

```json
{
  "schema_version": "1.0",
  "feature": "",
  "goal": "",
  "current_phase": "",
  "active_task": "",
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
