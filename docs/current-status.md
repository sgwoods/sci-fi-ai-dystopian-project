# Current Status

This repository is in the stable-and-portable operating phase.

## Current Position

- project class: `Standalone GitHub repo`
- durable source of truth: `sgwoods/sci-fi-ai-dystopian-project`
- preferred active clone:
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- preferred companion public clone: `~/Projects-All/public`
- iCloud role: intake and backup-oriented convenience, not the preferred live
  Git worktree
- the quote review board currently contains `44` normalized records
- the active candidate lane currently contains `0` records
- the approved export contains `32` records
- the postponed lane contains `10` records
- the declined lane contains `2` records
- the widening-search discovery queue contains `183` source-work candidates
- the source registry contains `21` entries, the query library `19`, and the
  follow-up watchlist `10`
- the scanned-source log contains `139` entries
- the workspace validator succeeds in a normal shell environment

## Big Picture

The project goal remains straightforward:

1. keep bringing in better dystopian-AI quotes
2. let the reviewer approve or reject them quickly
3. preserve enough provenance that the approved corpus can be trusted and reused
4. keep the system operationally safe so the work can resume from GitHub and a
   normal non-iCloud clone without reconstruction work

## What Is Working Well

- the canonical review board drives the generated approved, candidate,
  postponed, declined, markdown, and public-page outputs
- a clean clone can recover the tracked corpus and research trail from GitHub
- the local review app, route checker, and publish dry-run are scriptable
- the repo now has a root-level migration and handoff set instead of relying on
  one machine-specific working-copy story
- local source snapshots are preserved as compact research captures

## Main Open Gaps

- the literary side is still lighter than the film side
- the live quote hunt still relies too heavily on curated local candidate packs
- there is not yet a second-pass editorial policy for duplicate variants and
  multiple canonical phrasings

## Next Sensible Steps

1. keep using the non-iCloud `Projects-All` clone as the preferred live worktree
2. refill the empty `Candidates` lane from broader sourcing
3. keep `sgwoods/public` in a canonical non-iCloud clone for publish checks
4. run the bootstrap path on the replacement Mac and retire the old machine
   only after that validation succeeds end to end
