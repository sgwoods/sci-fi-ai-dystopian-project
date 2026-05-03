# Project State And Recovery Audit

Audit date: `2026-05-03`

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

The current pushed recovery point is:

- branch: `main`
- local HEAD: `1f7e1b9c1c4df66ff6c3c030d08aa15ec8ebe4a4`
- remote `origin/main`: `1f7e1b9c1c4df66ff6c3c030d08aa15ec8ebe4a4`

This means the repository is **not ahead of origin by commits**.

However, the working tree is **not clean**. There are important local changes
that are not committed or pushed yet.

## What Is Checked In And Recoverable From GitHub Right Now

The GitHub recovery point currently includes the earlier tracked repository
shape and the last pushed commit, but it does **not** include the local working
tree changes listed below.

Tracked file count at the current recovery point:

- total tracked files: `57`

Tracked top-level groups:

- `data`: `38`
- `docs`: `5`
- `incoming`: `2`
- `site`: `3`
- `tools`: `6`
- root docs/config files: `3`

This means a clean clone of `origin/main` would recover the older committed
state, not the current local state.

## What Is Not Yet Checked In

### Modified tracked files still only local

- `README.md`
- `data/approved/ai-dystopia-quotes.approved.json`
- `data/candidates/ai-dystopia-quotes.candidates.json`
- `data/discovery/README.md`
- `data/discovery/ai-dystopia-title-discovery.json`
- `data/review/ai-dystopia-quotes.declined.json`
- `data/review/ai-dystopia-quotes.postponed.json`
- `data/review/ai-dystopia-quotes.review-board.json`
- `data/review/ai-dystopia-source-scans.json`
- `docs/curation-workflow.md`
- `docs/current-status.md`
- `docs/review-board.md`
- `incoming/INDEX.md`
- `site/ai-dystopia-quotes-public-page.html`
- `site/ai-dystopia-quotes-review-app.html`
- `site/ai-dystopia-quotes-ui-harness.html`
- `tools/README.md`
- `tools/build_quotes_project.py`
- `tools/check_ui_routes.py`
- `tools/review_app_server.py`

### Untracked substantive files still only local

- `data/discovery/ai-dystopia-author-priority.json`
- `data/discovery/ai-dystopia-author-top10.json`
- `data/discovery/ai-dystopia-followup-watchlist.json`
- `data/discovery/ai-dystopia-query-library.json`
- `data/discovery/ai-dystopia-source-registry.json`
- `docs/expanding-plan.md`
- `docs/source-expansion-system.md`
- `incoming/gemini-100-candidates-2026-04-03/`
- `data/source-snapshots/2001-fullest-possible-use.md`
- `data/source-snapshots/alien-crew-expendable.md`
- `data/source-snapshots/dune-machine-likeness-of-a-human-mind.md`
- `data/source-snapshots/dune-thinking-over-to-machines.md`
- `data/source-snapshots/ex-machina-create-something-that-hates-you.md`
- `data/source-snapshots/first-contact-resistance-is-futile.md`
- `data/source-snapshots/ghost-shell-net-is-vast-and-infinite.md`
- `data/source-snapshots/her-not-tethered-to-time-and-space.md`
- `data/source-snapshots/ihnm-think-therefore-i-am.md`
- `data/source-snapshots/machine-stops-progress-of-the-machine.md`
- `data/source-snapshots/mass-effect-3-does-this-unit-have-a-soul.md`
- `data/source-snapshots/matrix-desert-of-the-real.md`
- `data/source-snapshots/nineteen-eighty-four-boot-stamping.md`
- `data/source-snapshots/portal-neurotoxin-emitters.md`
- `data/source-snapshots/terminator-decided-our-fate-in-a-microsecond.md`
- `data/source-snapshots/tron-programs-will-start-thinking.md`
- `data/source-snapshots/wargames-dont-act-like-one.md`
- `data/source-snapshots/white-christmas-job-not-a-jail.md`

### Untracked junk files

- `.DS_Store`
- `data/.DS_Store`

## Critical Recovery Gaps

If this local directory vanished right now and we only recloned
`origin/main`, we would **not** be able to continue from the current state
without redoing work.

The main reasons are:

1. The canonical board and derived JSON slices have local-only modifications.
2. The new source-expansion system files are untracked.
3. The current review app and server behavior are only local, not committed.
4. The current docs describing the newer workflow are only local.
5. The board currently references snapshot files that are not checked in.

Board records currently pointing to untracked snapshot files: `16`

- `dune-thinking-over-to-machines`
- `her-not-tethered-to-time-and-space`
- `first-contact-resistance-is-futile`
- `white-christmas-job-not-a-jail`
- `portal-neurotoxin-emitters`
- `nineteen-eighty-four-boot-stamping`
- `dune-machine-likeness-of-a-human-mind`
- `machine-stops-progress-of-the-machine`
- `2001-fullest-possible-use`
- `ex-machina-create-something-that-hates-you`
- `ihnm-think-therefore-i-am`
- `tron-programs-will-start-thinking`
- `matrix-desert-of-the-real`
- `wargames-dont-act-like-one`
- `ghost-shell-net-is-vast-and-infinite`
- `mass-effect-3-does-this-unit-have-a-soul`

Until those files are committed, the repo is not a full-fidelity recovery
point.

## Machine-Specific Assumptions

The project is close to portable, but not perfectly machine-agnostic yet.

Known assumptions:

- the publish script defaults to `/Users/stevenwoods/GitPages/public`
  although it can be overridden with `--public-root`
- some docs and interface notes still reference absolute local paths that are
  only correct on this machine

This does not block repo recovery, but it does mean a fresh machine will still
need either:

- the same path layout, or
- explicit path overrides when publishing and integrating downstream

## Precise Recovery Assessment

Current answer: **No, we are not yet 100% recoverable from GitHub alone.**

Current answer in more detail:

- a local working copy can continue the work
- a clean clone of `origin/main` cannot recreate the exact current state
- the missing state is mostly in uncommitted tracked changes plus important
  untracked data and docs

## Recommended Next Steps

To reach the standard of "clone on a new machine and continue without redoing
work", do this next:

1. stage every substantive local file listed above
2. remove or ignore junk files such as `.DS_Store`
3. commit the current working tree as a recovery checkpoint
4. push that checkpoint to `origin/main`
5. perform a fresh-clone verification on another directory, preferably inside
   an iCloud-backed working area so the recovery clone itself benefits from
   machine-independent backup:
   - build outputs
   - run the review server
   - open the review UI
   - confirm the board counts match this audit
   - confirm publish still works with an explicit `--public-root`
6. optionally reduce remaining machine-specific assumptions by moving default
   public-root and consumer-path guidance into a portable config pattern

## Recommended Status Language

The correct management summary right now is:

`The project has a strong local working state, but it is not yet at a fully recoverable remote checkpoint.`
