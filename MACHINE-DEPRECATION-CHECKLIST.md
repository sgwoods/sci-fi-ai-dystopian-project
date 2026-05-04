# Machine Deprecation Checklist

Use this before declaring the older Mac non-essential for the continued life
of this project.

## New-Machine Proof

- non-iCloud working clone exists at `~/Projects-All/sci-fi-ai-dystopian-project-working`
- `bash scripts/start-codex-new-mac.sh` succeeds there
- `bash scripts/show-project-version.sh` reports the expected branch and commit
- local review app starts and route checks pass
- publish dry-run succeeds with `~/Projects-All/public`

## GitHub Truth

- `origin` points to `https://github.com/sgwoods/sci-fi-ai-dystopian-project.git`
- the intended stable baseline is on `main`
- the new machine can `git pull --ff-only` and `git push`

## Local-State Safety

- any one-off intake material worth keeping has been moved into tracked repo
  paths or an explicit iCloud intake/archive location
- no active work depends on an old live iCloud worktree
- any legacy clone paths are labeled deprecated and not used casually

## Retirement Statement

The old machine is safe to de-prioritize only when the new Mac can recover,
validate, review, and publish from GitHub without hidden local knowledge.
