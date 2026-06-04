# GitHub Integration

The skill can generate repository assets for GitHub-based delivery.

## Pull request template

`generate_github_assets.py` creates `.github/pull_request_template.md` with DevFlow artifact links and gate checklist.

## CI workflow

`generate_github_assets.py` creates `.github/workflows/sdd-delivery-artifacts.yml` to validate `.sdd-delivery/*` folders on pull requests.

## Review comment workflow

When review comments are available through GitHub or `gh`, map actionable comments back to:

- Spec item
- solution section
- task ID
- test gap
- delivery review finding

Do not resolve a review finding unless the related artifact is updated.
