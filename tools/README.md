# Tools

This repository keeps the review workflow and public project page in sync
through a small generated-data toolchain.

## Main Scripts

- `build_quotes_project.py`
  Builds the derived JSON exports, the review-board markdown, and the public
  project page from the canonical review board.
- `review_quotes.py`
  Updates a quote's review status and then rebuilds all derived outputs.
- `review_app_server.py`
  Runs the local browser-based review workbench and API.
- `check_ui_routes.py`
  Scriptable local route check for the review app, public page, harness page,
  and key launch controls.

## Canonical Source Of Truth

The canonical editable data file is:

- `data/review/ai-dystopia-quotes.review-board.json`

Everything else in the workflow is derived from that file.

## Common Commands

```bash
python3 tools/build_quotes_project.py
python3 tools/review_quotes.py list
python3 tools/review_quotes.py candidate westworld-not-ordinary-machines --priority high --note "Strong systems-opacity line." --next-action "Approve if we want a stronger systems-opacity lane."
python3 tools/review_quotes.py approve westworld-not-ordinary-machines --note "Strong systems-opacity line."
python3 tools/review_quotes.py postpone m3gan-primary-user-now-me --note "Keep for modern pass."
python3 tools/review_quotes.py decline some-quote-id --note "Too generic."
python3 tools/review_app_server.py --port 8123
python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123
```

## Review App

Run:

```bash
python3 tools/review_app_server.py --port 8123
```

Then open:

- `http://127.0.0.1:8123/` for the review workbench
- `http://127.0.0.1:8123/public` for the generated public page

The review app lets you:

- switch between `candidate`, `approved`, `postponed`, and `declined`
- move any quote into any other status
- move declined items back whenever you want
- edit the review note, priority, and next action
- reorder items within each lane
- inspect scanned sources and widening strategies
- apply `Expand Search` to add the next title-discovery batch
- view the generated public page and the UI harness in-app

## UI Harness

Two layers are now available:

- Browser-side harness page: `http://127.0.0.1:8123/harness`
- Scriptable route check: `python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123`

The browser harness runs non-destructive DOM checks against the local pages,
while the route checker verifies the key routes and launch-link markup from the
command line.

## Generated Outputs

- `data/approved/ai-dystopia-quotes.approved.json`
- `data/candidates/ai-dystopia-quotes.candidates.json`
- `data/review/ai-dystopia-quotes.postponed.json`
- `data/review/ai-dystopia-quotes.declined.json`
- `docs/review-board.md`
- `site/ai-dystopia-quotes-public-page.html`
