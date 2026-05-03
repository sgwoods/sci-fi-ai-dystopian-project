# Curation Workflow

This repository follows a simple staged workflow modeled after the other local
renovation projects.

The product goal is simple:

- keep finding more interesting quotes
- review them quickly
- publish only the approved set

The supporting research system exists to make that quote hunt broader over
time without forcing the reviewer to manage the machinery directly.

## Flow

1. New source places, query patterns, and follow-up lanes are maintained under
   `data/discovery/`.
2. Newly found material lands in `incoming/`.
3. During review, the material is checked for attribution quality, duplicate
   status, and likely long-term value.
4. If the quote is worth retaining, it is added to
   `data/review/ai-dystopia-quotes.review-board.json` with status `candidate`.
5. The quote can then move to `approved`, `postponed`, or `declined`.
6. Generated JSON exports are rebuilt from the review board.
7. The local source trail is preserved under `data/source-snapshots/`.
8. Once approved content is ready for public consumption, the publish flow syncs
   the approved JSON, public project page, and shared homepage manifest into
   `GitPages/public`.
9. Editorial notes and policy updates live under `docs/`.

## Research Inventories

The widening system now has three persistent inputs:

- `data/discovery/ai-dystopia-source-registry.json`
  Active places to search or revisit
- `data/discovery/ai-dystopia-query-library.json`
  Reusable search patterns and prompt templates
- `data/discovery/ai-dystopia-followup-watchlist.json`
  Recurring author, title, and community lanes worth revisiting

These inventories are supporting inputs to quote hunting, not the product
surface themselves.

## Promotion Standard

A record is a good approval candidate when:

- the quote text is stable enough to cite confidently
- the work title is clear
- the creator or author is identifiable
- the year is known or responsibly left null
- the source page is reasonably credible for quote verification
- the line is strong enough to matter as a reusable dystopian-AI quote, not
  merely a plot line or generic dialogue fragment

## Review Outcomes

Every new quote or source find should end in one of these states:

- `candidate`
- `approved`
- `postponed`
- `duplicate`
- `reference-only`
- `pending`

## Rule Of Thumb

If the source quality, wording, or attribution is not clear yet, keep it out
of `approved/` and hold it in `incoming/` or on the review board as a
`candidate` until the picture is better.

If an AI model, Reddit thread, transcript page, or fan list suggests a
promising line, treat that as a lead, not as final verification.

## Review Commands

```bash
python3 tools/review_quotes.py list
python3 tools/review_quotes.py approve <quote-id> --note "why it belongs"
python3 tools/review_quotes.py postpone <quote-id> --note "why to hold it"
python3 tools/review_quotes.py decline <quote-id> --note "why to drop it"
python3 tools/review_quotes.py candidate <quote-id> --priority high --next-action "what to decide next"
python3 tools/publish_public_project.py --public-root /Users/stevenwoods/GitPages/public
```
