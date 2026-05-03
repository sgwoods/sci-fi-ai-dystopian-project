# Canonical Working Copy

This project now has one canonical day-to-day working copy:

- `/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`

## Big Picture

The goal is to keep this project both:

1. editorially productive
2. operationally safe

That means:

- all normal work should happen in the canonical iCloud-backed clone
- GitHub should remain the durable remote checkpoint
- the older local repo should no longer be treated as the primary workspace

## Use This Repo

For normal work, use:

```bash
cd "/Users/stevenwoods/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project"
```

## Main Daily Commands

Start of session safety check:

```bash
pwd
git status --short
git pull --ff-only origin main
```

Build generated artifacts:

```bash
python3 tools/build_quotes_project.py
```

Run the review app locally:

```bash
python3 tools/review_app_server.py --port 8123
```

Check the local UI routes:

```bash
python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123
```

Publish the approved JSON and public project page:

```bash
python3 tools/publish_public_project.py --public-root /Users/stevenwoods/GitPages/public
```

## Old Repo Status

The older local repo at:

- `/Users/stevenwoods/SciFi AI Dystopian Project`

should now be treated as:

- a transitional copy
- a fallback/archive
- not the normal place to continue editing

## Safety Rule

Before significant new work:

1. confirm you are in the canonical iCloud-backed clone
2. confirm `git status` is what you expect
3. pull the latest `main` with `git pull --ff-only origin main`
4. do the work there
5. commit and push from there

## Current Stabilization Status

As of the current checkpoint:

- GitHub has the recoverable project state
- the iCloud-backed clone has been verified
- the next work should focus on better quote sourcing and continued curation,
  not on moving the repo around again unless a new portability issue appears

## Recommended Next Steps

1. use the canonical clone for all new quote curation
2. improve `Find More Quotes` so it leans more on live source expansion
3. refill the `Candidates` lane with stronger quote options from broader
   internet sourcing
4. keep promoting strong candidates and broadening literary coverage
