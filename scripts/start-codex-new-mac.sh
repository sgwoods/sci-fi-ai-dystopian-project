#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_PUBLIC_DIR="${HOME}/Projects-All/public"
LEGACY_PUBLIC_DIR="${HOME}/GitPages/public"
DEFAULT_ICLOUD_INTAKE="${HOME}/Library/Mobile Documents/com~apple~CloudDocs/Projects/sci-fi-ai-dystopian-project-intake"

PUBLIC_DIR="$DEFAULT_PUBLIC_DIR"
PORT=8123
SKIP_VALIDATION=0
PYTHON_CMD=""
ICLOUD_INTAKE_DIR="${ICLOUD_INTAKE_DIR:-$DEFAULT_ICLOUD_INTAKE}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/start-codex-new-mac.sh [options]

Options:
  --public-dir DIR       Companion public repo path
  --port PORT            Local review-app validation port
  --python PATH          Explicit Python interpreter to use
  --skip-validation      Skip the final workspace validation pass
  --help                 Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --public-dir)
      PUBLIC_DIR="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --python)
      PYTHON_CMD="$2"
      shift 2
      ;;
    --skip-validation)
      SKIP_VALIDATION=1
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
}

python_supported() {
  local candidate="$1"
  "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 9) else 1)
PY
}

pick_python() {
  local candidates=()

  if [[ -n "$PYTHON_CMD" ]]; then
    candidates+=("$PYTHON_CMD")
  fi

  if [[ -n "${AI_DYSTOPIA_PYTHON:-}" ]]; then
    candidates+=("$AI_DYSTOPIA_PYTHON")
  fi

  if [[ -x /opt/homebrew/bin/python3 ]]; then
    candidates+=("/opt/homebrew/bin/python3")
  fi

  if command -v python3 >/dev/null 2>&1; then
    candidates+=("$(command -v python3)")
  fi

  local candidate
  for candidate in "${candidates[@]}"; do
    if [[ -x "$candidate" ]] && python_supported "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

echo "== Sci-Fi AI Dystopian Project new-Mac startup =="
echo "Repo root: $ROOT_DIR"

require_cmd git
require_cmd curl

PYTHON_CMD="$(pick_python)" || {
  echo "No usable Python 3.9+ interpreter was found." >&2
  echo "Install python3 or pass --python /path/to/python3." >&2
  exit 1
}

echo "Using Python: $PYTHON_CMD"

if [[ ! -d "$PUBLIC_DIR" && -d "$LEGACY_PUBLIC_DIR" ]]; then
  PUBLIC_DIR="$LEGACY_PUBLIC_DIR"
fi

mkdir -p "$ICLOUD_INTAKE_DIR"
echo "Ensured optional iCloud intake path: $ICLOUD_INTAKE_DIR"

if [[ -d "$PUBLIC_DIR" ]]; then
  export AI_DYSTOPIA_PUBLIC_ROOT="$PUBLIC_DIR"
  echo "Using companion public repo: $PUBLIC_DIR"
else
  echo "Companion public repo not found at: $PUBLIC_DIR"
  echo "Publish validation will be skipped until sgwoods/public is cloned there or passed with --public-dir."
fi

export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/tmp/ai-dystopia-pyc}"

echo "Branch state:"
git -C "$ROOT_DIR" status -sb

if [[ "$SKIP_VALIDATION" -eq 0 ]]; then
  echo "== Running supported validation spine =="
  "$PYTHON_CMD" "$ROOT_DIR/tools/validate_workspace.py" --public-root "$PUBLIC_DIR" --port "$PORT"
fi

cat <<EOF

Startup complete.

Preferred active working clone:
  $ROOT_DIR

Preferred iCloud intake path:
  $ICLOUD_INTAKE_DIR

Recommended next commands:
  cd "$ROOT_DIR"
  bash scripts/show-project-version.sh
  "$PYTHON_CMD" tools/review_app_server.py --port $PORT
EOF
