# Current Status

This repository is in the stable-and-safe operating phase.

## Current Position

- the canonical working copy going forward is now the iCloud-backed clone at
  `/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`
- the quote review board currently contains `44` normalized records
- the active candidate lane currently contains `0` records
- the approved export contains `32` records
- the postponed lane currently contains `10` records
- the declined lane currently contains `2` records
- the widening-search discovery queue now contains `183` source-work candidates
  against the earlier exploratory goal of `100`
- the new source-expansion system now tracks `21` active source places,
  `19` reusable query patterns, and `10` recurring follow-up lanes
- the scanned-source log currently contains `139` entries
- the current approved set now stretches from `1909` to `2014`
- the first-pass local source trail is preserved under
  `data/source-snapshots/`
- the discovery pool now includes a dedicated `recognizable classics` lane to
  prioritize mainstream AI and robot works before deeper long-tail expansion
- the widening plan now includes a formal author lane, with a focused top-10
  author mining set and a wider top-25 ranked author file
- the repo now has a preserved user-supplied Gemini intake and its non-duplicate
  source works have been merged into discovery as queued leads
- the repo now has a new-machine bootstrap path and workspace validator aimed
  specifically at replacing the current MacBook safely

## Big Picture

The project goal is now straightforward:

1. keep bringing in better dystopian-AI quotes
2. let the reviewer approve or reject them quickly
3. preserve enough provenance that the approved corpus can be trusted and reused
4. keep the system operationally safe so the work can be resumed from GitHub and
   the canonical iCloud-backed clone without reconstruction work

## What Is Working Well

- the canonical iCloud-backed working copy has been established and verified
- there is now a clean ingest-ready approved JSON export
- there is now a single canonical review board driving all derived outputs
- candidate and approved states are clearly separated
- the list-based local review app now supports in-place status changes and lane
  reordering
- the quote-hunt UI now exposes the source registry, query library, follow-up
  watchlist, and scan log so the hunt is less of a black box
- the discovery strategy now distinguishes between broad widening and
  recognizability-first canon building
- the repo now has a formal author-priority lane so literary discovery can be
  widened deliberately rather than opportunistically
- the repo now has both a browser-side UI harness and a scriptable route check
- each current record has a local source snapshot path
- the approved set now has a generated public project page under `site/`
- the repo now has the same broad operating pattern as the nearby renovation
  projects: strong top-level README, `docs/`, `data/`, and `incoming/`
- there is now a dedicated recovery audit documenting how to resume the project
  safely from GitHub
- the canonical iCloud-backed clone has been verified as the day-to-day working
  copy
- the workspace can now be validated without leaving behind ambiguous build
  diffs

## Main Open Gaps

- the literary side is still lighter than the film side
- the live quote hunt still relies too heavily on curated local candidate packs
  instead of executing full live internet sourcing on every run
- there is not yet a second-pass editorial policy for handling duplicate quote
  variants, partial lines, or multiple canonical phrasings

## Next Sensible Steps

1. keep using the iCloud-backed clone as the canonical working copy and avoid
   returning to the older local copy for normal editing
2. refill the empty `Candidates` lane from broader internet sourcing so the
   next review session has real quote choices again
3. make `Find More Quotes` draw more aggressively from the source registry,
   query library, watchlist, and quote-oriented web research
4. mine the active top-10 author lane into stronger literary quote candidates
5. keep widening each sourcing phase in larger, less repetitive batches
6. decide whether the approved export should also carry retrieval-oriented
   fields such as `tone`, `threat_level`, or `voice_style`
7. decide how aggressively to add poster or cover art for records that still
   rely on fallbacks
8. run the new-machine bootstrap path on the replacement Mac and retire this
   MacBook only after that validation succeeds end to end
