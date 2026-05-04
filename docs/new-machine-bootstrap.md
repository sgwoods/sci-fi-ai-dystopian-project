# New Machine Bootstrap

This project now has a machine-handoff path designed to survive the retirement
of the current MacBook.

## Big Picture

The goal is not only to keep the quote corpus in GitHub, but to make sure a
new Mac can:

1. clone the project into the canonical iCloud-backed location
2. validate that the project runs cleanly
3. bring up the review workbench without guesswork
4. publish to the companion public-site checkout when needed

## Canonical Paths

Recommended project checkout:

- `~/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project`

Recommended public-site checkout:

- `~/GitPages/public`

The public-site checkout is only required for publish validation and public
artifact sync. Core quote review and local validation work without it.

## Minimum Dependencies

The project currently depends on:

- `git`
- `python3`

The Python tooling in `tools/` is standard-library only. There is no separate
package install step at the moment.

## One-Script Bootstrap

From any machine that has `git` and `python3`, the simplest path is:

```bash
git clone https://github.com/sgwoods/sci-fi-ai-dystopian-project.git
cd sci-fi-ai-dystopian-project
./scripts/bootstrap_new_mac.sh
```

What that script does:

1. clones or fast-forwards the project repo into the canonical iCloud-backed location
2. clones or fast-forwards the public-site repo into `~/GitPages/public`
3. validates the workspace with `tools/validate_workspace.py`
4. prints the exact commands to continue in Codex

## Validation Standard

`tools/validate_workspace.py` currently proves that:

- required project files exist
- the core Python scripts compile
- a rebuild stays clean instead of creating mystery diffs
- the review server can start locally
- the UI route harness passes
- publish dry-run works when the public-site checkout is available

## Recommended Codex Start

After bootstrap succeeds on the new Mac:

```bash
cd "~/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project"
AI_DYSTOPIA_PUBLIC_ROOT="$HOME/GitPages/public" python3 tools/review_app_server.py --port 8123
```

## Current Portability Notes

- The project repo itself is recoverable from GitHub.
- The canonical working copy is the iCloud-backed clone.
- The public publish flow depends on the companion repo at
  `https://github.com/sgwoods/public`.
- `AI_DYSTOPIA_PUBLIC_ROOT` can now override the public-site path on any
  machine.

## Safe Retirement Standard For This MacBook

This MacBook can be treated as deprecated once all of the following are true on
the replacement Mac:

1. the bootstrap script succeeds
2. `tools/validate_workspace.py` succeeds
3. the review UI opens and works locally
4. a publish dry-run succeeds against the public-site checkout
5. the new Mac is the one being used for normal commits and pushes
