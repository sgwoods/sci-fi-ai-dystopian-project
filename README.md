# AI Dystopia Quotes Corpus

This repository is a durable, reviewable corpus of dystopian AI, machine
control, synthetic agency, and algorithmic-domination quotes.

The point is not only to gather strong lines, but to preserve enough
attribution, provenance, review state, and local source context that the
collection can be trusted, extended, published, and recovered from GitHub on a
different machine without hidden local knowledge.

## Project Classification

- class: `Standalone GitHub repo`
- durable source of truth: `https://github.com/sgwoods/sci-fi-ai-dystopian-project`
- stable baseline branch: `main`
- preferred active working clone:
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- companion public repo for publish validation and sync:
  `~/Projects-All/public`
- iCloud role: intake and backup-oriented convenience, not the preferred live
  Git worktree

## Project Goal

The primary goal is to build one canonical, ingestible approved dataset of
dystopian AI quotes while keeping the broader research trail visible:

1. gather candidate quotes from credible sources
2. normalize quote text, attribution, work title, creator, and year
3. preserve local source snapshots and review notes
4. promote only the strongest entries into the approved application-facing JSON
5. keep a clear boundary between approved corpus records, candidate records,
   and newly found unreviewed material
6. keep widening the source registry and query library so quote hunting grows
   broader rather than more repetitive

## Current Status

Current live position:

- the canonical review board contains `44` records
- the approved export contains `32` records
- the postponed lane contains `10` records
- the declined lane contains `2` records
- the active candidate lane is currently empty
- the discovery system contains `183` source-work leads, `21` source places,
  `19` reusable query patterns, and `10` recurring follow-up lanes
- local source snapshots are preserved as compact research captures rather than
  full third-party webpage mirrors
- the repo’s validator succeeds in a normal shell environment, including build
  cleanliness, local UI route checks, and publish dry-run when the companion
  public repo is present

## Documentation Map

- [Project status](./PROJECT-STATUS.md): root-level answer to what this folder
  is supposed to represent
- [Bootstrap checklist](./BOOTSTRAP-CHECKLIST.md): clean new-Mac bring-up path
- [New Mac handoff](./NEW-MAC-HANDOFF.md): operating model and supported
  validation spine
- [Machine deprecation checklist](./MACHINE-DEPRECATION-CHECKLIST.md): when the
  old Mac can be treated as non-essential
- [Recovery and reproducibility](./RECOVERY-AND-REPRODUCIBILITY.md): tracked
  inventory, dependencies, recovery path, and portability assumptions
- [Data index](./data/README.md): canonical data directories and what they mean
- [Current status](./docs/current-status.md): concise live project snapshot
- [Working copy guide](./docs/canonical-working-copy.md): preferred clone model
  and daily-use commands
- [New machine bootstrap](./docs/new-machine-bootstrap.md): compact bridge to
  the new root-level migration docs
- [Project recovery audit](./docs/project-state-and-recovery-audit.md): longer
  audit narrative
- [Expanding plan](./docs/expanding-plan.md): current widening strategy
- [Initial review](./docs/initial-review.md): editorial assessment of the
  first-pass quote set
- [Curation workflow](./docs/curation-workflow.md): recommended intake,
  verification, and promotion flow
- [Source expansion system](./docs/source-expansion-system.md): the source
  registry, query library, and follow-up watchlist behind quote hunting
- [Review board](./docs/review-board.md): actionable candidate, postponed,
  declined, and approved views
- [Repository structure review](./docs/repository-structure-review.md):
  explanation of how the repo is organized
- [Incoming intake](./incoming/README.md): single landing zone for newly found
  material before review
- [Tools guide](./tools/README.md): build, validate, and publish commands

## Repository Structure

```text
data/
  approved/                Canonical ingest-ready JSON exports
  candidates/              Broader reviewed quote pool, including non-approved records
  discovery/               Title discovery plus the source registry, query library, and follow-up watchlist
  review/                  Canonical review board and generated postponed/declined slices
  source-snapshots/        Local source captures for each quote record
docs/                      Status, workflow, review, and structure notes
incoming/                  Single intake bucket for newly found material
scripts/                   Bootstrap, startup, and version helpers
site/                      Generated public project page
tools/                     Review, validation, and publish scripts
```

## Working Model

Use a normal non-iCloud clone for day-to-day work:

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
```

Quick health check:

```bash
bash scripts/show-project-version.sh
```

Bootstrap a new Mac or prove a clean clone:

```bash
bash scripts/bootstrap-project-macos.sh --clone-public
```

Start a normal working session:

```bash
bash scripts/start-codex-new-mac.sh
```

## External Dependencies

- required: `git`, `python3`, `curl`
- repo-local package install step: none
- companion repo for publish validation: `sgwoods/public`

## Generated Outputs

The canonical editable file is:

- `data/review/ai-dystopia-quotes.review-board.json`

Tracked generated outputs include:

- `data/approved/ai-dystopia-quotes.approved.json`
- `data/candidates/ai-dystopia-quotes.candidates.json`
- `data/review/ai-dystopia-quotes.postponed.json`
- `data/review/ai-dystopia-quotes.declined.json`
- `docs/review-board.md`
- `site/ai-dystopia-quotes-public-page.html`

## Near-Term Plan

1. refill the `Candidates` lane with stronger quote options from broader
   sourcing
2. make `Find More Quotes` behave more like a determined researcher and less
   like a local-packs shortcut
3. grow literary coverage alongside recognizable film and game coverage
4. keep publishing only the strongest approved records into the public JSON and
   public project page
5. keep the replacement-Mac bootstrap path proven so the project does not
   depend on one specific machine
