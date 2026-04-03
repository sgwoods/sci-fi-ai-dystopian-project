# Review Data

This directory holds the canonical review workflow state for the corpus.

## Main Files

- `ai-dystopia-quotes.review-board.json`
  The single editable source of truth for quote review status.
- `ai-dystopia-source-scans.json`
  Registry of scanned sources, widening search strategies, and search progress.
- `ai-dystopia-quotes.postponed.json`
  Generated slice of postponed records.
- `ai-dystopia-quotes.declined.json`
  Generated slice of declined records.

## Status Model

Each quote record on the review board should be in one of these states:

- `candidate`
- `approved`
- `postponed`
- `declined`

The source-scan registry additionally tracks widening search strategies such as
search-engine passes, catalog passes, AI-assisted broadening, and long-tail
cleanup.

## Rule Of Thumb

Edit the review board, not the generated slices.
