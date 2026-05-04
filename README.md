# AI Dystopia Quotes Corpus

This repository is the starting point for a durable, reviewable corpus of
classic and high-signal quotes about the dystopia of AI, machine control,
synthetic agency, and algorithmic domination.

The goal is not only to gather quotable lines, but to preserve enough
attribution, provenance, and local source context that the collection can be
trusted, extended, and ingested by downstream applications with confidence.

Canonical working copy going forward:

- `/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`

## Project Goal

The primary goal is to build one canonical, ingestable approved dataset of
dystopian AI quotes while keeping the broader research trail visible:

1. gather candidate quotes from credible online sources
2. normalize quote text, attribution, work title, creator, and year where possible
3. preserve local source snapshots and review notes
4. promote only the strongest entries into the approved application-facing JSON
5. keep a clear boundary between approved corpus records, candidate records,
   and newly found unreviewed material
6. keep widening the source registry and query library so quote hunting keeps
   getting broader rather than more repetitive

## Current Status

This repository is now in the stable-and-safe operating phase.

Current live position:

- the canonical review board contains `44` records
- the approved export contains `32` records
- the postponed lane contains `10` records
- the declined lane contains `2` records
- the active candidate lane is currently empty, which means the next priority
  is replenishing reviewable quote candidates rather than restructuring the repo
- the discovery system contains `183` source-work leads, `21` source places,
  `19` reusable query patterns, and `10` recurring follow-up lanes
- local source snapshots are preserved as compact research captures rather
  than full third-party webpage mirrors
- the approved set spans recognizable classics from `The Machine Stops` and
  `R.U.R.` through `2001: A Space Odyssey`, `Blade Runner`, `The Matrix`,
  `Ex Machina`, and `Dune`

## Documentation Map

- [Data index](./data/README.md): canonical data directories and what each one means
- [Current status](./docs/current-status.md): concise live project snapshot
- [Canonical working copy](./docs/canonical-working-copy.md): exact repo path and daily-use commands for the canonical iCloud-backed clone
- [New machine bootstrap](./docs/new-machine-bootstrap.md): clone, validate, and start the project on a replacement Mac
- [Project state and recovery audit](./docs/project-state-and-recovery-audit.md): exact status of the current working tree, GitHub checkpoint, and portability gaps
- [Expanding plan](./docs/expanding-plan.md): current widening strategy including the active top-10 author lane
- [Initial review](./docs/initial-review.md): editorial assessment of the first-pass quote set
- [Curation workflow](./docs/curation-workflow.md): recommended quote intake, verification, and promotion flow
- [Source expansion system](./docs/source-expansion-system.md): the source registry, query library, and follow-up watchlist behind quote hunting
- [Review board](./docs/review-board.md): actionable candidate, postponed, declined, and approved views
- [Repository structure review](./docs/repository-structure-review.md): explanation of how the repo is organized and what counts as canonical
- [Incoming intake](./incoming/README.md): single landing zone for newly found material before review
- [Tools guide](./tools/README.md): build and review commands
- [Publish flow](./tools/README.md#publish-flow): sync the public page, approved JSON, and shared homepage manifest
- [Review app](./site/ai-dystopia-quotes-review-app.html): browser UI served locally by `tools/review_app_server.py`
- [UI harness](./site/ai-dystopia-quotes-ui-harness.html): in-browser non-destructive checks for the local user-facing pages

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
scripts/                   Bootstrap helpers for new-machine setup
site/                      Generated public project page
tools/                     Review and build scripts
```

## Canonical Workspace

The canonical day-to-day working copy is now:

- `/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`

Use that clone for normal editing, review, commits, and publishing.

## Near-Term Plan

Now that the repo itself is stable and recoverable, the next product work is:

1. refill the `Candidates` lane with stronger quote options from broader
   internet sourcing
2. make `Find More Quotes` behave more like a determined researcher and less
   like a local-packs shortcut
3. grow literary coverage alongside recognizable film and game coverage
4. keep publishing only the strongest approved records into the public JSON and
   public project page
5. keep the replacement-Mac bootstrap path proven so this repo no longer
   depends on the current MacBook for continuity

## Record Shape

Each normalized quote record currently includes:

- `id`
- `quote`
- `quote_speaker`
- `speaker_is_ai`
- `work_title`
- `work_type`
- `work_year`
- `work_creators`
- `themes`
- `source`
- `metadata_source`
- `local_snapshot_path`
- `approval_status`
- `notes`

## Curation Notes

- Access date for the current pass: `2026-04-02`
- Local source captures are intentionally concise. They preserve the useful
  research trail without copying full third-party pages.
- Some records currently use a film adaptation quote page as the best available
  online citation for a widely repeated line; where relevant, the notes call
  out the relationship to the underlying book or story.
- The canonical editable file is now `data/review/ai-dystopia-quotes.review-board.json`.
  The approved JSON, candidate queue, review board markdown, and public project
  page are generated from that single board.
- The widening-search workflow now includes three persistent research
  inventories under `data/discovery/`: a source registry, a query library, and
  a follow-up watchlist.
- The `Find More Quotes` action is now treated as an autonomous multi-step
  hunt: it can choose the next best direction on its own, widen supporting
  leads, and then add the strongest locally-verified quote candidates it can
  find.
- The earlier title-discovery goal of `100` candidate source works is still
  preserved as historical scaffolding, but the product goal is better quote
  candidates, not a lead-count milestone by itself.
- The repo now includes a dedicated publish script that syncs the approved
  public artifacts into the shared `GitPages/public` site and refreshes the
  Steven Woods projects index from the manifest flow rather than by hand.
