# AI Dystopia Quotes Corpus

This repository is the starting point for a durable, reviewable corpus of
classic and high-signal quotes about the dystopia of AI, machine control,
synthetic agency, and algorithmic domination.

The goal is not only to gather quotable lines, but to preserve enough
attribution, provenance, and local source context that the collection can be
trusted, extended, and ingested by downstream applications with confidence.

## Project Goal

The primary goal is to build one canonical, ingestable approved dataset of
dystopian AI quotes while keeping the broader research trail visible:

1. gather candidate quotes from credible online sources
2. normalize quote text, attribution, work title, creator, and year where possible
3. preserve local source snapshots and review notes
4. promote only the strongest entries into the approved application-facing JSON
5. keep a clear boundary between approved corpus records, candidate records,
   and newly found unreviewed material

## Current Status

This repository is in the initial corpus bootstrap phase.

Current first-pass position:

- the candidate corpus contains `12` records
- the approved export contains `10` records
- the current approved set is centered on classic works such as `R.U.R.`,
  `2001: A Space Odyssey`, `I Have No Mouth, and I Must Scream`,
  `Colossus: The Forbin Project`, `WarGames`, `The Terminator`,
  `The Matrix`, and `Ex Machina`
- local source snapshots are preserved as compact research captures rather
  than full third-party webpage mirrors

## Documentation Map

- [Data index](./data/README.md): canonical data directories and what each one means
- [Current status](./docs/current-status.md): concise live project snapshot
- [Initial review](./docs/initial-review.md): editorial assessment of the first-pass quote set
- [Curation workflow](./docs/curation-workflow.md): recommended quote intake, verification, and promotion flow
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
  discovery/               Widening-search title discovery queue and target progress
  review/                  Canonical review board and generated postponed/declined slices
  source-snapshots/        Local source captures for each quote record
docs/                      Status, workflow, review, and structure notes
incoming/                  Single intake bucket for newly found material
site/                      Generated public project page
tools/                     Review and build scripts
```

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
- The widening-search workflow now tracks a title-discovery goal of `100`
  candidate source works under `data/discovery/`.
- The repo now includes a dedicated publish script that syncs the approved
  public artifacts into the shared `GitPages/public` site and refreshes the
  Steven Woods projects index from the manifest flow rather than by hand.
