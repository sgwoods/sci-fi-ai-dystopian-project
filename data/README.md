# Data Directory

Master index for the canonical data artifacts in the AI dystopia quotes
corpus. This directory holds the reviewed quote datasets and the local source
captures that support them.

## Canonical Data Sets

| Directory | Purpose | Description |
|---|---|---|
| [approved/](./approved/) | Application ingest | Canonical ingest-ready JSON exports containing only approved quote records |
| [candidates/](./candidates/) | Reviewed working corpus | Broader reviewed quote pool, including records still under editorial consideration |
| [discovery/](./discovery/) | Widening search queue | Title-level discovery pool used to widen the quote-mining frontier toward the current candidate goal |
| [review/](./review/) | Workflow state | Canonical review board plus generated postponed and declined slices |
| [source-snapshots/](./source-snapshots/) | Local provenance captures | Compact local source records preserving the quote, attribution, URLs, and verification notes |

## Directory Meanings

- `approved/` means application-facing, intentionally curated, and suitable for
  downstream ingest.
- `candidates/` means reviewed enough to normalize, but not necessarily
  promoted into the main approved export.
- `discovery/` means title-level search and expansion work that is broader than
  the quote board itself.
- `review/` means the canonical review workflow state, including the single
  editable review board and any generated status slices.
- `source-snapshots/` means local preservation of the research trail. These are
  concise captures rather than full-page mirrors.

## Current Canonical Files

- [approved/ai-dystopia-quotes.approved.json](./approved/ai-dystopia-quotes.approved.json)
- [candidates/ai-dystopia-quotes.candidates.json](./candidates/ai-dystopia-quotes.candidates.json)
- [discovery/ai-dystopia-title-discovery.json](./discovery/ai-dystopia-title-discovery.json)
- [review/ai-dystopia-quotes.review-board.json](./review/ai-dystopia-quotes.review-board.json)

## Rule Of Thumb

If a quote has not been normalized and reviewed yet, it should not be added
directly into `approved/`. It belongs in `incoming/` first, then into the
`review/` board as a `candidate`, and only later in `approved/` once the
attribution and source quality look strong enough.
