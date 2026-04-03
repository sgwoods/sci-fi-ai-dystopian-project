# Current Status

This repository is in the initial corpus bootstrap phase.

## Current Position

- the quote review board currently contains `17` normalized records
- the active candidate lane currently contains `5` records
- the approved export contains `8` records
- the postponed lane currently contains `4` records
- the widening-search discovery queue now contains `33` source-work candidates
  toward a goal of `100`
- the current approved set is anchored around classic works from `1920` to
  `2014`
- the first-pass local source trail is preserved under
  `data/source-snapshots/`
- the discovery pool now includes a dedicated `recognizable classics` lane to
  prioritize mainstream AI and robot works before deeper long-tail expansion

## What Is Working Well

- there is now a clean ingest-ready approved JSON export
- there is now a single canonical review board driving all derived outputs
- candidate and approved states are clearly separated
- the list-based local review app now supports in-place status changes and lane
  reordering
- the sources tab now tracks scanned sources, widening strategies, and
  discovery progress
- the discovery strategy now distinguishes between broad widening and
  recognizability-first canon building
- the repo now has both a browser-side UI harness and a scriptable route check
- each current record has a local source snapshot path
- the approved set now has a generated public project page under `site/`
- the repo now has the same broad operating pattern as the nearby renovation
  projects: strong top-level README, `docs/`, `data/`, and `incoming/`

## Main Open Gaps

- the literary side is still lighter than the film side
- there is not yet a larger intake of raw newly found source material in
  `incoming/`
- there is not yet a second-pass editorial policy for handling duplicate quote
  variants, partial lines, or multiple canonical phrasings

## Next Sensible Steps

1. widen the literary and story-based quote coverage
2. mine the new recognizable-classics discovery lane into quote-level
   candidates before widening too far into less familiar material
3. keep applying widening search passes until the discovery queue crosses the
   `100`-title mark
4. add intake items for newly found source pages or scans before review
5. decide whether the approved export should also carry retrieval-oriented
   fields such as `tone`, `threat_level`, or `voice_style`
6. decide how aggressively to add poster or cover art for records that still
   rely on fallbacks
