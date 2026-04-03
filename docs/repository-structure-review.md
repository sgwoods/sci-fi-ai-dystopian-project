# Repository Structure Review

This note explains the intended meaning of the main repository areas so the
corpus stays understandable as it grows.

## Primary Areas

| Path | Meaning |
|---|---|
| `data/approved/` | Canonical application-facing quote exports |
| `data/candidates/` | Reviewed working corpus that is broader than the approved set |
| `data/review/` | Canonical review board plus generated status slices |
| `data/source-snapshots/` | Compact local provenance captures for individual quote records |
| `docs/` | Status notes, review notes, workflow, and structure guidance |
| `incoming/` | Single intake bucket for newly found material that has not been reviewed yet |
| `site/` | Generated public-facing project page |
| `tools/` | Workflow scripts that keep derived artifacts synchronized |

## What Counts As Canonical

- `data/approved/` is the canonical application ingest surface.
- `data/review/ai-dystopia-quotes.review-board.json` is the canonical editable
  review source of truth.
- `data/candidates/` is canonical for reviewed-but-not-fully-promoted quote
  records.
- `data/source-snapshots/` is canonical for the local provenance trail tied to
  those reviewed records.

## What Does Not Yet Count As Canonical

- anything newly dropped into `incoming/`
- unreviewed copied source pages
- ad hoc notes left outside `docs/`
- manual edits to the generated site or derived status slices

## Structural Guidance

- Prefer adding repo-level notes under `docs/` rather than inventing new
  top-level folders.
- Prefer adding reviewed quote artifacts under `data/` rather than scattering
  JSON and markdown across the root.
- Prefer `incoming/` first for new raw finds when the final home is not yet
  obvious.
