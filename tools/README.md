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
- `validate_workspace.py`
  End-to-end portability validator for a clean checkout on a new or replacement
  Mac.
- `publish_public_project.py`
  Rebuilds the local project outputs, syncs the public-site copy of the page
  and approved JSON, writes the shared public manifest, and rerenders the
  shared homepage when the companion `public` repo is available.

## Canonical Source Of Truth

The canonical editable data file is:

- `data/review/ai-dystopia-quotes.review-board.json`

Everything else in the workflow is derived from that file.

The preferred live clone for running these commands is:

- `~/Projects-All/sci-fi-ai-dystopian-project-working`
- companion public repo: `~/Projects-All/public`

Bootstrap helpers:

- `scripts/bootstrap-project-macos.sh`
- `scripts/start-codex-new-mac.sh`
- `scripts/show-project-version.sh`

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
python3 tools/validate_workspace.py --public-root "$HOME/Projects-All/public"
python3 tools/publish_public_project.py --public-root "$HOME/Projects-All/public"
```

## Review App

Run:

```bash
python3 tools/review_app_server.py --port 8123
```

Recommended working directory:

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
```

Then open:

- `http://127.0.0.1:8123/` for the review workbench
- `http://127.0.0.1:8123/public` for the generated public page

## UI Harness

Two layers are available:

- browser-side harness page: `http://127.0.0.1:8123/harness`
- scriptable route check:
  `python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123`

## Generated Outputs

- `data/approved/ai-dystopia-quotes.approved.json`
- `data/candidates/ai-dystopia-quotes.candidates.json`
- `data/review/ai-dystopia-quotes.postponed.json`
- `data/review/ai-dystopia-quotes.declined.json`
- `docs/review-board.md`
- `site/ai-dystopia-quotes-public-page.html`

## Publish Flow

Recommended sequence:

```bash
python3 tools/build_quotes_project.py
python3 tools/publish_public_project.py --public-root "$HOME/Projects-All/public"
```

That flow will:

- rebuild the local approved JSON and public page
- sync the approved JSON into `public/data/`
- sync the public project page into `public/`
- write this project's shared manifest under `public/data/projects/`
- rerender the shared Steven Woods homepage

Useful flags:

- `--skip-build`
- `--skip-index`
- `--dry-run`

## New-Machine Validation

To prove the repo is ready to leave one machine behind, run:

```bash
bash scripts/bootstrap-project-macos.sh --clone-public
```
