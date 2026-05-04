# New Mac Handoff

This repo is now intended to follow the same migration model as
`phd-renovation`.

## Operating Model

- GitHub `sgwoods/sci-fi-ai-dystopian-project` is the durable source of truth
- `main` is the stable baseline branch
- the preferred live Git worktree is a normal folder such as
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- iCloud is for intake, backup-oriented convenience, and handoff material, not
  the preferred live Git clone
- the companion `sgwoods/public` repo should live once, canonically, in a
  normal folder such as `~/Projects-All/public`

## What The New Machine Needs

- project clone at `~/Projects-All/sci-fi-ai-dystopian-project-working`
- optional companion clone at `~/Projects-All/public`
- `git`, `python3`, and `curl`

## Recommended Bring-Up

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
bash scripts/bootstrap-project-macos.sh --clone-public
bash scripts/show-project-version.sh
```

For a normal working session:

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
bash scripts/start-codex-new-mac.sh
```

## Validation Spine

The supported proof path is:

1. `python3 tools/build_quotes_project.py`
2. `python3 tools/validate_workspace.py --public-root "$HOME/Projects-All/public"`
3. `python3 tools/review_app_server.py --port 8123`
4. `python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123`
5. `python3 tools/publish_public_project.py --public-root "$HOME/Projects-All/public" --dry-run`

## What Not To Do

- do not treat an iCloud clone as the preferred day-to-day worktree
- do not rely on `~/GitPages/public` as the long-term default companion path
- do not assume untracked local files are part of the durable project state

## Handoff Ready Means

The new Mac counts as a valid active home once the validation spine passes from
the non-iCloud clone and `main` is clean and in sync with GitHub.
