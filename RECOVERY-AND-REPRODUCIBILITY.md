# Recovery And Reproducibility

Audit date: `2026-05-04`

## Classification

- Project class: `Standalone GitHub repo`
- Repo remote: `https://github.com/sgwoods/sci-fi-ai-dystopian-project.git`
- Canonical branch: `main`
- Preferred active clone: `~/Projects-All/sci-fi-ai-dystopian-project-working`
- Companion repo: `https://github.com/sgwoods/public.git`
- Preferred companion clone: `~/Projects-All/public`

## Durable Source Of Truth

The durable source of truth is the tracked Git history in
`sgwoods/sci-fi-ai-dystopian-project`.

This repo does not require an iCloud-backed live worktree for continuity.
iCloud can still be used for intake and backup-oriented convenience, but the
preferred working model is a normal non-iCloud clone plus GitHub.

## Tracked Inventory

Current tracked file count after this migration-hardening step is checked in:
`97`

Tracked top-level groups:

- `data`: `61`
- `docs`: `10`
- `incoming`: `3`
- `scripts`: `4`
- `site`: `3`
- `tools`: `7`
- root docs/config files: `9`

## State Categories

Tracked source of truth:

- `data/review/ai-dystopia-quotes.review-board.json`
- `data/review/ai-dystopia-source-scans.json`
- `data/discovery/*.json`
- documentation under `README.md`, root migration docs, and `docs/`
- Python tooling under `tools/`

Tracked generated artifacts:

- `data/approved/ai-dystopia-quotes.approved.json`
- `data/candidates/ai-dystopia-quotes.candidates.json`
- `data/review/ai-dystopia-quotes.postponed.json`
- `data/review/ai-dystopia-quotes.declined.json`
- `docs/review-board.md`
- `site/ai-dystopia-quotes-public-page.html`

Generated and intentionally ignored:

- `__pycache__/`
- `*.pyc`
- `.DS_Store`

Deprecated/manual helpers:

- `scripts/bootstrap_new_mac.sh` remains only as a compatibility wrapper for
  the older bootstrap name

## External Dependencies

System tools:

- `git`
- `python3`
- `curl`

Language/runtime package managers:

- none required inside this repo for normal validation

Companion repos:

- `sgwoods/public` is required for publish dry-run and real public sync

Machine-local paths:

- optional iCloud intake path:
  `~/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project-intake`
- preferred active clone:
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- preferred public companion clone:
  `~/Projects-All/public`

## Supported Validation Path

Core validation:

```bash
python3 tools/validate_workspace.py --public-root "$HOME/Projects-All/public"
```

Review app validation:

```bash
python3 tools/review_app_server.py --port 8123
python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123
```

Publish dry-run:

```bash
python3 tools/publish_public_project.py --public-root "$HOME/Projects-All/public" --dry-run
```

## Recovery Procedure From GitHub

1. Clone the repo into `~/Projects-All/sci-fi-ai-dystopian-project-working`
2. Clone `sgwoods/public` into `~/Projects-All/public` if publish validation is needed
3. Run `bash scripts/bootstrap-project-macos.sh --clone-public`
4. Run `bash scripts/show-project-version.sh`
5. Run the validation spine

## Current Audit Result

The repo’s real validator succeeds in a normal shell environment, including
build cleanliness, review-app route checks, and publish dry-run when the
companion public repo is available.

The main migration risk before this hardening step was not data loss. It was
operator confusion caused by an iCloud-first working-copy story that no longer
matches the desired cross-project model.
