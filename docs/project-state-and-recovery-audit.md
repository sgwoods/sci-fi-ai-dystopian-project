# Project State And Recovery Audit

Audit date: `2026-05-04`

## Classification

- project class: `Standalone GitHub repo`
- durable source of truth: `https://github.com/sgwoods/sci-fi-ai-dystopian-project.git`
- preferred active clone:
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- companion repo:
  `https://github.com/sgwoods/public.git`
- preferred companion clone:
  `~/Projects-All/public`

## Precise Goal

This project exists to build and maintain a curated, ingestible corpus of
recognizable dystopian AI quotations while remaining recoverable from GitHub
without hidden machine-local knowledge.

## Current Data Truth

Current repo facts at audit time:

- review board records: `44`
- approved: `32`
- postponed: `10`
- declined: `2`
- active candidates: `0`
- source-work discovery leads: `183`
- source registry entries: `21`
- query library entries: `19`
- follow-up watchlist entries: `10`
- scanned-source log entries: `139`

The canonical editable data file remains:

- `data/review/ai-dystopia-quotes.review-board.json`

## Git Checkpoint Truth

Operating rule:

- the project should remain anchored on branch `main`
- GitHub is the durable baseline
- the preferred working clone is a normal non-iCloud folder
- after each substantive stabilization or curation step, local `HEAD` and
  `origin/main` should match again

Practical verification commands:

```bash
git rev-parse HEAD
git rev-parse origin/main
git status --short
```

## What Is Checked In And Recoverable

The tracked repo contains the current review board, discovery files,
source-snapshot trail, generated public artifacts, docs, and tooling needed to
resume the project.

Tracked file count after this migration-hardening step is checked in: `97`

## What Is Intentionally Not Tracked

The intended untracked files are only normal local junk or transient files,
such as:

- `.DS_Store`
- `__pycache__/`
- `*.pyc`

## Machine-Specific Assumptions Reduced

This migration step is specifically removing the strongest remaining source of
operator confusion:

- old docs treated an iCloud-backed clone as canonical
- the preferred cross-project model is now a normal `Projects-All` clone
- the companion `public` repo should also live in a normal non-iCloud path

The project still supports explicit path overrides through
`AI_DYSTOPIA_PUBLIC_ROOT` or `--public-root` when needed.

## Recovery Assessment

Current answer: **Yes, the committed project state is recoverable from GitHub
alone.**

Current answer in more detail:

- a clean clone can recreate the tracked corpus and tooling
- the validator succeeds in a normal shell environment
- publish dry-run succeeds when the companion public repo is available
- the preferred working model no longer depends on an iCloud live worktree

## Recommended Next Steps

1. continue using the non-iCloud active clone as the preferred live worktree
2. keep `sgwoods/public` in a canonical `Projects-All` clone
3. validate the same path on the replacement Mac
4. promote only a proven, clean baseline to `main`
