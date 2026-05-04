# Canonical Working Copy

This project’s preferred day-to-day working copy is now a normal non-iCloud
clone:

- `~/Projects-All/sci-fi-ai-dystopian-project-working`

## Big Picture

The goal is to keep the project both:

1. editorially productive
2. operationally safe

That means:

- all normal work should happen in the non-iCloud active clone
- GitHub should remain the durable checkpoint
- iCloud should be used for intake and backup-oriented convenience only

## Use This Repo

For normal work, use:

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
```

## Main Daily Commands

Start-of-session safety check:

```bash
bash scripts/show-project-version.sh
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
python3 tools/publish_public_project.py --public-root "$HOME/Projects-All/public"
```

Bootstrap a replacement Mac:

```bash
bash scripts/bootstrap-project-macos.sh --clone-public
```

## Legacy Paths

If you still have an iCloud-backed clone or an older local folder, treat it as
legacy or intake-oriented rather than the preferred place to continue editing.

## Safety Rule

Before significant new work:

1. confirm you are in the non-iCloud active clone
2. confirm `git status` is what you expect
3. pull the latest `main` with `git pull --ff-only origin main`
4. do the work there
5. commit and push from there
