# Bootstrap Checklist

Use this checklist when bringing the project onto a new Mac or proving that a
fresh non-iCloud clone is truly portable.

## Project Class

- Classification: `Standalone GitHub repo`
- Durable source of truth: `https://github.com/sgwoods/sci-fi-ai-dystopian-project`
- Preferred active clone: `~/Projects-All/sci-fi-ai-dystopian-project-working`
- Companion public repo for publish validation: `~/Projects-All/public`
- Optional iCloud intake path: `~/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project-intake`

## Prerequisites

- `git`
- `python3`
- `curl`
- optional: `Homebrew` if the machine needs help installing missing commands

There is currently no repo-local package install step and no `pip`, `npm`, or
virtualenv requirement for normal validation.

## Bootstrap Sequence

1. Clone the repo into a normal non-iCloud working folder:

```bash
git clone https://github.com/sgwoods/sci-fi-ai-dystopian-project.git \
  "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
```

2. Enter the clone:

```bash
cd "$HOME/Projects-All/sci-fi-ai-dystopian-project-working"
```

3. Run the bootstrap helper:

```bash
bash scripts/bootstrap-project-macos.sh \
  --target-dir "$HOME/Projects-All/sci-fi-ai-dystopian-project-working" \
  --public-dir "$HOME/Projects-All/public" \
  --clone-public
```

4. Confirm the folder state:

```bash
bash scripts/show-project-version.sh
```

## Success Standard

The new Mac is ready when all of the following are true:

- `bash scripts/show-project-version.sh` reports the expected repo and branch
- `python3 tools/validate_workspace.py --public-root "$HOME/Projects-All/public"` succeeds
- `python3 tools/review_app_server.py --port 8123` starts locally
- `python3 tools/check_ui_routes.py --base-url http://127.0.0.1:8123` succeeds
- publish dry-run succeeds when the companion `public` repo is present

## If Something Fails

- If `python3` is missing, install it or re-run bootstrap with `--install-homebrew`
- If publish validation is skipped, clone `sgwoods/public` into `~/Projects-All/public`
- If the branch is wrong, re-run bootstrap with `--branch <name>`
- If the tree becomes dirty after validation, stop and inspect before pushing
