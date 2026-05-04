#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATUS_JSON="$ROOT_DIR/PROJECT-STATUS.json"

if [[ ! -f "$STATUS_JSON" ]]; then
  echo "Missing status source: $STATUS_JSON" >&2
  exit 1
fi

python3 - "$STATUS_JSON" "$ROOT_DIR" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

status_path = Path(sys.argv[1])
root = Path(sys.argv[2])
data = json.loads(status_path.read_text(encoding="utf-8"))


def git(*args):
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


branch = git("branch", "--show-current") or "(detached)"
head = git("rev-parse", "--short", "HEAD") or "(unknown)"
origin_main = git("rev-parse", "--short", "origin/main") or "(unknown)"
remote = git("remote", "get-url", "origin") or "(unknown)"
dirty = bool(git("status", "--short"))
metrics = data["metrics"]

rows = [
    ("Project", data["project"]),
    ("Repo id", data["repo_id"]),
    ("Project class", data["project_class"]),
    ("Published release", data["published_release"]),
    ("Current track", metrics["current_track"]["value"]),
    ("Current focus", metrics["current_focus"]["value"]),
    ("Build line", metrics["build_line"]["value"]),
    ("Canonical branch", data["canonical_branch"]),
    ("Current branch", branch),
    ("Current commit", head),
    ("origin/main", origin_main),
    ("Working tree", "dirty" if dirty else "clean"),
    ("Origin", remote),
    ("Folder", str(root)),
    ("Preferred active clone", data["preferred_active_clone"]),
    ("Preferred public clone", data["preferred_public_clone"]),
    ("Updated", metrics["updated"]["value"]),
]

width = max(len(label) for label, _ in rows)
for label, value in rows:
    print(f"{label + ':':<{width + 2}} {value}")
PY
