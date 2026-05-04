# Project State And Recovery Audit

Audit date: `2026-05-03`

Canonical working copy going forward:

- `/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`

## Precise Goal

This project exists to build and maintain a curated, ingestible corpus of
recognizable dystopian AI quotations.

The repo is not only a quote list. It is meant to be a complete working system
for:

1. finding more candidate quotes
2. preserving provenance and local research snapshots
3. triaging quotes through review states
4. publishing the approved set as machine-ingestible JSON and a human-readable
   project page

## Current Data Truth

The current working-tree truth, as of this audit, is:

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

The canonical review board file is:

- `data/review/ai-dystopia-quotes.review-board.json`

## Git Checkpoint Truth

The operating rule is:

- the project should remain on branch `main`
- the canonical iCloud-backed clone should stay aligned with `origin/main`
- after each substantive stabilization or curation step, local `HEAD` and
  `origin/main` should match again

Practical verification commands:

```bash
git rev-parse HEAD
git rev-parse origin/main
git status --short
```

The desired steady state is:

- `HEAD` matches `origin/main`
- `git status --short` is empty unless new work is intentionally in progress

## What Is Checked In And Recoverable From GitHub Right Now

The GitHub recovery point now includes the current substantive working state,
including the newer source-expansion system, recovery audit, and tracked local
source snapshots.

Tracked file count after the current portability step is committed:

- total tracked files: `88`

Tracked top-level groups:

- `data`: `61`
- `docs`: `10`
- `incoming`: `3`
- `scripts`: `1`
- `site`: `3`
- `tools`: `7`
- root docs/config files: `3`

This means a clean clone of `origin/main` can recover the committed project
state, including the canonical operating guide under `docs/`.

## What Is Not Yet Checked In

At the moment, the intended substantive project artifacts are checked in.

The only files that should remain uncommitted going forward are normal local
junk or transient files, such as macOS metadata, and `.DS_Store` is now
ignored.

## Critical Recovery Gaps

The earlier critical gap was that many board-linked snapshot files and the
newer source-expansion files were only local. That gap has now been closed.

## Machine-Specific Assumptions

The project is close to portable, but not perfectly machine-agnostic yet.

Known assumptions:

- the publish and review-app tooling default to `~/GitPages/public`
  and can be overridden with `AI_DYSTOPIA_PUBLIC_ROOT` or `--public-root`
- some docs and interface notes still reference absolute local paths that are
  only correct on this machine

This does not block repo recovery, but it does mean a fresh machine will still
need either:

- the same path layout, or
- explicit path overrides when publishing and integrating downstream

## Precise Recovery Assessment

Current answer: **Yes, the committed project state is recoverable from GitHub alone.**

Current answer in more detail:

- a clean clone of `origin/main` can recreate the committed project state
- that clone has already been verified in an iCloud-backed working directory
- the iCloud-backed clone is now the canonical day-to-day working copy

## Recommended Next Steps

To keep the project at the standard of "clone on a new machine and continue
without redoing work", do this next:

1. keep using the iCloud-backed clone as the canonical working copy
2. perform future verification in another directory, preferably inside an
   iCloud-backed working area so recovery clones themselves benefit from
   machine-independent backup:
   - build outputs
   - run the review server
   - open the review UI
   - confirm the board counts match this audit
   - confirm publish still works with an explicit `--public-root`
   - use `scripts/bootstrap_new_mac.sh` and `tools/validate_workspace.py`
     as the baseline handoff path
3. optionally reduce remaining machine-specific assumptions by moving default
   public-root and consumer-path guidance into a portable config pattern

## Recommended Status Language

The correct management summary right now is:

`The project is recoverable from GitHub, and the canonical working copy is the verified iCloud-backed clone.`
