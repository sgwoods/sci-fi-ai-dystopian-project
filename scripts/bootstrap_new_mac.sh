#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARGS=()

if [[ -n "${PROJECT_ROOT:-}" ]]; then
  ARGS+=(--target-dir "$PROJECT_ROOT")
fi

if [[ -n "${PUBLIC_ROOT:-}" ]]; then
  ARGS+=(--public-dir "$PUBLIC_ROOT" --clone-public)
fi

if [[ -n "${PORT:-}" ]]; then
  ARGS+=(--port "$PORT")
fi

exec bash "$ROOT_DIR/scripts/bootstrap-project-macos.sh" "${ARGS[@]}" "$@"
