# Approved Quotes Interface

This file is the single handoff reference for any downstream project that wants
to consume the approved AI dystopia quotes corpus.

## Canonical Consumer Rule

Consume only the approved export.

Do not read from:

- `data/review/`
- `data/candidates/`
- `data/discovery/`

Those files are editorial workflow surfaces and may change as quotes move
between `candidate`, `approved`, `postponed`, and `declined`.

## Approved Export Locations

Use one of these two paths:

- local development source:
  `/Users/stevenwoods/SciFi AI Dystopian Project/data/approved/ai-dystopia-quotes.approved.json`
- published public copy:
  `/Users/stevenwoods/GitPages/public/data/ai-dystopia-quotes.approved.json`

Source repository:

- `https://github.com/sgwoods/sci-fi-ai-dystopian-project`

## JSON Contract

The approved export is a JSON object with this top-level shape:

```json
{
  "collection": "ai-dystopia-quotes",
  "generated_at": "2026-04-03",
  "description": "Approved ingest set of dystopian AI quotes.",
  "source_board": "data/review/ai-dystopia-quotes.review-board.json",
  "records": []
}
```

Consumers should read from `records`.

Each record may include:

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
- `notes`
- `review`
- `source_work`

## Consumer Guidance

- treat each record in `records` as approved and application-safe
- use `id` as the stable identifier
- use `quote` as the display text
- use `quote_speaker`, `work_title`, and `work_year` for attribution
- use `themes` and `speaker_is_ai` for filtering or game logic
- use `source_work.summary` and `source_work.cover_image_url` for richer UI
- use `source.url` and `metadata_source.url` when you want citation or drilldown

## Refresh Rule

When this project publishes new approved content, the approved export may grow
or reorder, but downstream consumers should expect existing `id` values to
remain the stable reference key unless explicitly deprecated later.

## Publish Flow

The publishing command for this project is:

```bash
python3 tools/publish_public_project.py --public-root /Users/stevenwoods/GitPages/public
```

That command refreshes:

- the local generated approved export
- the public-site approved export
- the public project page
- the shared Steven Woods homepage manifest entry

## Recommended Instruction For Other Projects

Use this approved corpus only:

`/Users/stevenwoods/SciFi AI Dystopian Project/data/approved/ai-dystopia-quotes.approved.json`

If you need the published copy instead, use:

`/Users/stevenwoods/GitPages/public/data/ai-dystopia-quotes.approved.json`

Do not ingest from `data/review/` or `data/candidates/`.
