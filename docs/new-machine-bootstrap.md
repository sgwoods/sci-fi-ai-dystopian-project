# New Machine Bootstrap

This file is the short bridge to the repo’s root-level migration docs.

## Preferred Layout

- active project clone:
  `~/Projects-All/sci-fi-ai-dystopian-project-working`
- companion public clone:
  `~/Projects-All/public`
- optional iCloud intake path:
  `~/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project-intake`

The preferred live Git worktree is now a normal non-iCloud folder. iCloud is
for intake and backup-oriented convenience, not the canonical working clone.

## One-Command Bootstrap

From inside a clone of this repo:

```bash
bash scripts/bootstrap-project-macos.sh --clone-public
```

## Daily Startup

```bash
bash scripts/start-codex-new-mac.sh
```

## Full Handoff Docs

- [Bootstrap checklist](../BOOTSTRAP-CHECKLIST.md)
- [New Mac handoff](../NEW-MAC-HANDOFF.md)
- [Recovery and reproducibility](../RECOVERY-AND-REPRODUCIBILITY.md)
- [Machine deprecation checklist](../MACHINE-DEPRECATION-CHECKLIST.md)
