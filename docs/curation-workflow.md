# Curation Workflow

This repository follows a simple staged workflow modeled after the other local
renovation projects.

## Flow

1. Newly found material lands in `incoming/`.
2. During review, the material is checked for attribution quality, duplicate
   status, and likely long-term value.
3. If the quote is worth retaining, it is added to
   `data/review/ai-dystopia-quotes.review-board.json` with status `candidate`.
4. The quote can then move to `approved`, `postponed`, or `declined`.
5. Generated JSON exports are rebuilt from the review board.
6. The local source trail is preserved under `data/source-snapshots/`.
7. Editorial notes and policy updates live under `docs/`.

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

## Review Commands

```bash
python3 tools/review_quotes.py list
python3 tools/review_quotes.py approve <quote-id> --note "why it belongs"
python3 tools/review_quotes.py postpone <quote-id> --note "why to hold it"
python3 tools/review_quotes.py decline <quote-id> --note "why to drop it"
python3 tools/review_quotes.py candidate <quote-id> --priority high --next-action "what to decide next"
```
