# Incoming

This directory is the single intake bucket for newly found material that may
be relevant to the AI dystopia quotes corpus:

- quote source pages
- scanned or archived reference material
- bibliographic notes
- copied excerpts pending review
- alternate quote phrasings
- newly found books, stories, films, or essays

## Purpose

Use `incoming/` first whenever new material arrives and its final home is not
yet settled.

Do not drop new finds directly into:

- `data/approved/`
- `data/candidates/`
- `data/source-snapshots/`
- `docs/`

until that material has been reviewed.

## Intake Workflow

1. Add the new material under any convenient subdirectory name.
2. Add a short note describing where it came from and what it appears to contain.
3. Update `incoming/INDEX.md` with one row for the intake.
4. Review the intake before promoting anything out of `incoming/`.
5. After review, move or classify it into one of these destinations:
   - `data/candidates/` for normalized reviewed quotes
   - `data/source-snapshots/` for retained local source captures
   - `docs/` for durable review or policy notes
   - `data/approved/` only after promotion-level review

## Review Outcomes

Every reviewed intake should end in one of these states:

- `pending`
- `candidate`
- `approved`
- `duplicate`
- `reference-only`

## Rule Of Thumb

If the right home or the right wording is not obvious yet, it belongs in
`incoming/` first.
