#!/usr/bin/env bash
set -euo pipefail

DEFAULT_TARGET_DIR="${HOME}/Projects-All/sci-fi-ai-dystopian-project-working"
DEFAULT_PUBLIC_DIR="${HOME}/Projects-All/public"
DEFAULT_REPO_URL="https://github.com/sgwoods/sci-fi-ai-dystopian-project.git"
DEFAULT_PUBLIC_REPO_URL="https://github.com/sgwoods/public.git"

TARGET_DIR="$DEFAULT_TARGET_DIR"
PUBLIC_DIR="$DEFAULT_PUBLIC_DIR"
REPO_URL="$DEFAULT_REPO_URL"
PUBLIC_REPO_URL="$DEFAULT_PUBLIC_REPO_URL"
BRANCH="main"
PORT=8123
INSTALL_HOMEBREW=0
CLONE_PUBLIC=0
SKIP_VALIDATION=0
BRANCH_EXPLICIT=0

usage() {
  cat <<'EOF'
Usage:
  bash scripts/bootstrap-project-macos.sh [options]

Options:
  --target-dir DIR         Active non-iCloud working clone path
  --branch BRANCH          Branch to check out after cloning/updating
  --repo-url URL           Repo URL or local path to clone/update
  --public-dir DIR         Companion public repo path
  --public-repo-url URL    Companion public repo URL or local path
  --port PORT              Validation port passed to startup
  --clone-public           Clone/update the companion public repo too
  --skip-validation        Skip the final startup validation pass
  --install-homebrew       Install Homebrew first if it is missing
  --help                   Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir)
      TARGET_DIR="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      BRANCH_EXPLICIT=1
      shift 2
      ;;
    --repo-url)
      REPO_URL="$2"
      shift 2
      ;;
    --public-dir)
      PUBLIC_DIR="$2"
      shift 2
      ;;
    --public-repo-url)
      PUBLIC_REPO_URL="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --clone-public)
      CLONE_PUBLIC=1
      shift
      ;;
    --skip-validation)
      SKIP_VALIDATION=1
      shift
      ;;
    --install-homebrew)
      INSTALL_HOMEBREW=1
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

ensure_homebrew() {
  if command -v brew >/dev/null 2>&1; then
    return 0
  fi

  if [[ "$INSTALL_HOMEBREW" -ne 1 ]]; then
    echo "Homebrew is required to auto-install missing tools." >&2
    echo "Install Homebrew first or re-run with --install-homebrew." >&2
    exit 1
  fi

  echo "Installing Homebrew..."
  NONINTERACTIVE=1 /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
}

ensure_brew_package() {
  local package="$1"
  if brew list "$package" >/dev/null 2>&1; then
    echo "brew package present: $package"
    return 0
  fi

  echo "Installing brew package: $package"
  brew install "$package"
}

detect_default_branch() {
  if [[ "$BRANCH_EXPLICIT" -eq 1 ]]; then
    return 0
  fi

  if git -C "$PWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local current_branch
    current_branch="$(git -C "$PWD" branch --show-current 2>/dev/null || true)"
    if [[ -n "$current_branch" ]]; then
      BRANCH="$current_branch"
    fi
  fi
}

ensure_cmd_or_install() {
  local command_name="$1"
  local brew_package="$2"

  if command -v "$command_name" >/dev/null 2>&1; then
    return 0
  fi

  ensure_homebrew
  ensure_brew_package "$brew_package"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Command still missing after installation: $command_name" >&2
    exit 1
  fi
}

clone_or_update_repo() {
  local repo_url="$1"
  local target_dir="$2"
  local branch="$3"

  mkdir -p "$(dirname "$target_dir")"

  if [[ ! -d "$target_dir/.git" ]]; then
    echo "Cloning repo into: $target_dir"
    git clone "$repo_url" "$target_dir"
  fi

  echo "Refreshing repo: $target_dir"
  git -C "$target_dir" fetch origin
  git -C "$target_dir" checkout "$branch"
  git -C "$target_dir" merge --ff-only "origin/$branch"
}

main() {
  detect_default_branch

  echo "== Sci-Fi AI Dystopian Project macOS bootstrap =="
  echo "Target repo: $TARGET_DIR"
  echo "Branch: $BRANCH"

  ensure_cmd_or_install curl curl
  ensure_cmd_or_install git git
  ensure_cmd_or_install python3 python

  clone_or_update_repo "$REPO_URL" "$TARGET_DIR" "$BRANCH"

  if [[ "$CLONE_PUBLIC" -eq 1 ]]; then
    clone_or_update_repo "$PUBLIC_REPO_URL" "$PUBLIC_DIR" main
  fi

  local startup_args=(
    --public-dir "$PUBLIC_DIR"
    --port "$PORT"
  )

  if [[ "$SKIP_VALIDATION" -eq 1 ]]; then
    startup_args+=(--skip-validation)
  fi

  echo
  echo "Handing off to startup validation..."
  bash "$TARGET_DIR/scripts/start-codex-new-mac.sh" "${startup_args[@]}"
}

main "$@"
