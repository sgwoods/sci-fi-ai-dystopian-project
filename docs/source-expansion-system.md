# Source Expansion System

This project is now organized around a simple quote-first research model:

1. keep bringing more interesting dystopian AI quotes into the `Candidates` lane
2. keep broadening where we look so the hunt does not become repetitive
3. keep enough provenance that approvals stay trustworthy

## The Three Supporting Inventories

### Source Registry

`data/discovery/ai-dystopia-source-registry.json`

This is the maintained list of places worth searching. It includes:

- quote-rich sources like Wikiquote and IMDb quote pages
- discovery and metadata surfaces like Wikipedia, Open Library, and WorldCat
- community surfaces like `r/printSF` and `r/scifi`
- hint-only surfaces like transcript sites
- AI ideation surfaces like Gemini, ChatGPT, and Claude

The point is not that every source is equally trustworthy. The point is that
each source has a role:

- some are good for final quote verification
- some are good for finding more works
- some are good for generating new search directions

## Query Library

`data/discovery/ai-dystopia-query-library.json`

This is the reusable bank of search patterns the project can keep refining over
time. Each query record captures:

- what kind of hunt it supports
- which sources it is best suited for
- what counts as a successful result

The goal is to keep a memory of what search language works instead of starting
from scratch every time.

## Follow-up Watchlist

`data/discovery/ai-dystopia-followup-watchlist.json`

This is the recurring lane list: places, titles, authors, and communities worth
revisiting when the queue needs fresh material. It is especially useful for:

- user-requested lanes like `Blade Runner`, `Asimov`, `Herbert`, and `Orwell`
- active community surfaces that can keep surfacing new leads
- strong quote-heavy works that merit multiple passes

## How `Find More Quotes` Fits In

The user-facing action remains intentionally simple:

1. type a direction like `more Asimov`, `more robot rebellion`, or `more games`
2. press `Find More Quotes`
3. review the new candidates or the clear no-result explanation

Behind the scenes, the app now treats quote hunting as a combination of:

- current candidate packs
- source-registry matches
- query-library matches
- watchlist follow-ups

The intended product behavior is that the app acts like a determined research
assistant. The reviewer can steer the hunt, but the app should still do useful
work when the prompt is blank by choosing the next best author, title, theme,
or source lane on its own.

The quote hunt should stay simple for the reviewer while the research system
gets richer over time.

## Editorial Rule

These supporting inventories are not the product. Approved quotes are.

The source registry, query library, watchlist, scan log, and discovery pool all
exist to make it easier to keep finding better quotes and explaining what the
system did when a hunt succeeds or fails.
