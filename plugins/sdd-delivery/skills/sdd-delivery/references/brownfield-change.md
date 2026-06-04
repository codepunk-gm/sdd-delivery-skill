# Brownfield Change

Existing projects require repo-grounded planning.

## Required behavior

- Inspect existing architecture before proposing changes.
- Prefer current patterns over new abstractions.
- Identify compatibility and migration concerns.
- Keep refactors separate from behavior changes.
- Do not rename or reorganize files without explicit need.

## Current system findings

Record findings as:

| Fact | Source | Confidence |
|---|---|---|

Confidence values:
- high: direct code or test evidence
- medium: inferred from multiple sources
- low: hypothesis requiring verification

## Risk scan

Check:
- API compatibility
- data migration
- auth and permissions
- concurrency
- performance
- tests and fixtures
- deployment or config impact
