#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO_URL="${PROJECT_REPO_URL:-https://github.com/sgwoods/sci-fi-ai-dystopian-project.git}"
PUBLIC_REPO_URL="${PUBLIC_REPO_URL:-https://github.com/sgwoods/public.git}"
PROJECT_ROOT="${PROJECT_ROOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project}"
PUBLIC_ROOT="${AI_DYSTOPIA_PUBLIC_ROOT:-$HOME/GitPages/public}"
PORT="${PORT:-8123}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

sync_repo() {
  local repo_url="$1"
  local target="$2"
  mkdir -p "$(dirname "$target")"
  if [[ -d "$target/.git" ]]; then
    git -C "$target" pull --ff-only origin main
  else
    git clone "$repo_url" "$target"
  fi
}

require_command git
require_command python3

sync_repo "$PROJECT_REPO_URL" "$PROJECT_ROOT"
sync_repo "$PUBLIC_REPO_URL" "$PUBLIC_ROOT"

cd "$PROJECT_ROOT"
AI_DYSTOPIA_PUBLIC_ROOT="$PUBLIC_ROOT" python3 tools/validate_workspace.py --public-root "$PUBLIC_ROOT" --port "$PORT"

cat <<EOF

Bootstrap and validation succeeded.

Canonical project workspace:
  $PROJECT_ROOT

Public publishing workspace:
  $PUBLIC_ROOT

Recommended next commands in Codex:
  cd "$PROJECT_ROOT"
  AI_DYSTOPIA_PUBLIC_ROOT="$PUBLIC_ROOT" python3 tools/review_app_server.py --port $PORT
  AI_DYSTOPIA_PUBLIC_ROOT="$PUBLIC_ROOT" python3 tools/publish_public_project.py --public-root "$PUBLIC_ROOT"
EOF
