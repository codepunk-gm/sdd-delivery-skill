# Plugin Operations Guide

This guide explains how to publish, install, update, and maintain the SDD Delivery plugin.

## Recommended repository layout

For plugin-based distribution, publish the plugin package as the GitHub repository root:

```text
sdd-delivery/
├── .codex-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── sdd-delivery/
        ├── SKILL.md
        ├── README.md
        ├── agents/
        ├── references/
        ├── scripts/
        └── assets/
```

## Publishing checklist

Before publishing:

- [ ] Repository root contains `.codex-plugin/plugin.json`.
- [ ] Repository root contains `README.md`.
- [ ] `skills/sdd-delivery/SKILL.md` exists.
- [ ] `skills/sdd-delivery/references/interaction-model.md` exists.
- [ ] `skills/sdd-delivery/references/ai-tool-usage.md` exists.
- [ ] `skills/sdd-delivery/references/open-source-influences.md` exists.
- [ ] `skills/sdd-delivery/assets/templates/` exists.
- [ ] `skills/sdd-delivery/scripts/` exists.
- [ ] README explains No Python Mode.
- [ ] README explains Codex plugin installation.
- [ ] License is selected before public promotion.

## Plugin install flow

For end users in the Codex client, use slash commands:

```text
/plugin marketplace add codepunk-gm/sdd-delivery-skill
/plugin install sdd-delivery
```

After installation, start a new Codex session and invoke:

```text
Use $sdd-delivery to turn this PRD into Spec, solution, reviewed implementation tasks, unit tests, and observable delivery artifacts.
```

For local development, the repository also includes `marketplace.json`, so a local checkout can be added as a marketplace root.

## Updating the plugin

When changing the skill:

1. Update files under `skills/sdd-delivery/`.
2. Update `.codex-plugin/plugin.json` version.
3. Update README if user-facing behavior changes.
4. Reinstall or refresh the plugin in Codex.
5. Test the startup menu and one PRD-to-Spec flow.

## Versioning recommendation

Use semantic versioning:

- patch: documentation, prompts, small template changes
- minor: new scripts or new workflow artifacts
- major: breaking artifact schema or plugin manifest changes

## Maintenance policy

Keep these stable:

- skill name: `sdd-delivery`
- artifact folder: `.sdd-delivery/<feature>/`
- core artifacts: `00-prd.md` through `12-observability.md`
- checkpoint schema fields whenever possible

Avoid requiring Python for core usage. Scripts are optional accelerators.

## Troubleshooting

### Plugin installed but skill not triggered

Ask the user to invoke explicitly:

```text
Use $sdd-delivery for this PRD.
```

### Python is unavailable

Use No Python Mode. The agent creates and updates artifacts manually.

### Trace coverage is wrong

Check `03-requirement-trace.md` table columns and ensure Spec IDs use `SPEC-1`, `SPEC-2`, etc.

### Test coverage is not detected

Make sure test files mention Spec IDs:

```python
"""Covers SPEC-1 and SPEC-2."""
```

### GitHub CI cannot find validator

Run:

```bash
python skills/sdd-delivery/scripts/generate_github_assets.py .
```

This copies the validator to `.github/scripts/validate_devflow_artifacts.py`.


## Path and escaping notes

If `/plugin marketplace add codepunk-gm/sdd-delivery-skill` reports that `marketplace.json` is missing, first verify whether the issue is a local cache or path escaping problem.

Recommended fallbacks:

```text
/plugin marketplace add https://github.com/codepunk-gm/sdd-delivery-skill.git
```

Or clone locally and use a quoted path with forward slashes on Windows:

```text
/plugin marketplace add "C:/Users/your-name/path/to/sdd-delivery-skill"
/plugin install sdd-delivery
```

Some renderers may display `C:\Users\Name\.claude` as `C:\Users\Name.claude` because `\.` is treated as an escaped dot. Check the real path from the terminal before assuming the plugin cache path is wrong.
