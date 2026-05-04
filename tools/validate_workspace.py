#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def default_public_root() -> Path:
    explicit = os.environ.get("AI_DYSTOPIA_PUBLIC_ROOT")
    if explicit:
        return Path(explicit).expanduser()

    preferred = Path.home() / "Projects-All" / "public"
    legacy = Path.home() / "GitPages" / "public"
    if preferred.exists():
        return preferred
    if legacy.exists():
        return legacy
    return preferred


DEFAULT_PUBLIC_ROOT = default_public_root()
CORE_SCRIPTS = [
    "tools/build_quotes_project.py",
    "tools/review_quotes.py",
    "tools/review_app_server.py",
    "tools/check_ui_routes.py",
    "tools/publish_public_project.py",
    "tools/validate_workspace.py",
]
REQUIRED_PATHS = [
    "data/review/ai-dystopia-quotes.review-board.json",
    "data/review/ai-dystopia-source-scans.json",
    "data/discovery/ai-dystopia-title-discovery.json",
    "data/discovery/ai-dystopia-source-registry.json",
    "data/discovery/ai-dystopia-query-library.json",
    "data/discovery/ai-dystopia-followup-watchlist.json",
    "docs/current-status.md",
    "docs/project-state-and-recovery-audit.md",
    "docs/canonical-working-copy.md",
    "README.md",
]


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=True)


def assert_required_paths(project_root: Path) -> None:
    missing = [path for path in REQUIRED_PATHS if not (project_root / path).exists()]
    if missing:
        raise FileNotFoundError("Missing required project files:\n- " + "\n- ".join(missing))


def board_summary(project_root: Path) -> tuple[int, dict[str, int]]:
    board = json.loads((project_root / "data/review/ai-dystopia-quotes.review-board.json").read_text())
    counts: dict[str, int] = {}
    for record in board["records"]:
        status = record["review"]["status"]
        counts[status] = counts.get(status, 0) + 1
    return len(board["records"]), counts


def repo_status(project_root: Path) -> str:
    return run(["git", "status", "--short"], cwd=project_root).stdout.strip()


def assert_clean_after_build(project_root: Path, env: dict[str, str]) -> None:
    before_status = repo_status(project_root)
    run([sys.executable, "tools/build_quotes_project.py"], cwd=project_root, env=env)
    after_status = repo_status(project_root)
    if after_status != before_status:
        raise RuntimeError(
            "Build changed the repository state during validation.\n"
            f"Before:\n{before_status or '(clean)'}\n\nAfter:\n{after_status or '(clean)'}"
        )


def wait_for_server(base_url: str, timeout_seconds: float) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base_url, timeout=2):
                return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    raise TimeoutError(f"Timed out waiting for review server at {base_url}")


def validate_ui(project_root: Path, env: dict[str, str], port: int) -> None:
    base_url = f"http://127.0.0.1:{port}/"
    server = subprocess.Popen(
        [sys.executable, "tools/review_app_server.py", "--port", str(port)],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        wait_for_server(base_url, timeout_seconds=15)
        run(
            [sys.executable, "tools/check_ui_routes.py", "--base-url", base_url],
            cwd=project_root,
            env=env,
        )
    except Exception as exc:
        server_output = ""
        if server.poll() is not None:
            stdout, stderr = server.communicate(timeout=2)
            server_output = "\n".join(part for part in [stdout.strip(), stderr.strip()] if part)
        if server_output:
            raise RuntimeError(
                f"Review server validation failed at {base_url}.\nServer output:\n{server_output}"
            ) from exc
        raise
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)


def validate_publish(project_root: Path, env: dict[str, str], public_root: Path) -> str:
    if not public_root.exists():
        return f"Skipped publish validation because public root does not exist: {public_root}"
    if not (public_root / "tools" / "render_index.py").exists():
        return f"Skipped publish validation because render_index.py is missing under: {public_root}"
    run(
        [
            sys.executable,
            "tools/publish_public_project.py",
            "--public-root",
            str(public_root),
            "--dry-run",
        ],
        cwd=project_root,
        env=env,
    )
    return f"Validated publish dry-run against {public_root}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that this workspace is portable and runnable on a new Mac."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=ROOT,
        help="Project checkout to validate. Defaults to the current repo.",
    )
    parser.add_argument(
        "--public-root",
        type=Path,
        default=DEFAULT_PUBLIC_ROOT,
        help="Optional public-site checkout used for publish validation.",
    )
    parser.add_argument("--port", type=int, default=8123, help="Local validation port.")
    parser.add_argument(
        "--skip-ui",
        action="store_true",
        help="Skip starting the review server and checking UI routes.",
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Skip publish dry-run validation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()
    public_root = args.public_root.resolve()
    env = dict(os.environ)
    env["AI_DYSTOPIA_PUBLIC_ROOT"] = str(public_root)
    env.setdefault("PYTHONPYCACHEPREFIX", str(Path(tempfile.gettempdir()) / "ai-dystopia-pyc"))

    assert_required_paths(project_root)
    record_count, status_counts = board_summary(project_root)

    run([sys.executable, "-m", "py_compile", *CORE_SCRIPTS], cwd=project_root, env=env)
    assert_clean_after_build(project_root, env)

    if not args.skip_ui:
        validate_ui(project_root, env, args.port)

    publish_message = "Skipped publish validation by request."
    if not args.skip_publish:
        publish_message = validate_publish(project_root, env, public_root)

    print("Workspace validation succeeded.")
    print(f"Project root: {project_root}")
    print(f"Public root: {public_root}")
    print(f"Board records: {record_count}")
    print(f"Approved: {status_counts.get('approved', 0)}")
    print(f"Candidates: {status_counts.get('candidate', 0)}")
    print(f"Postponed: {status_counts.get('postponed', 0)}")
    print(f"Declined: {status_counts.get('declined', 0)}")
    print(publish_message)


if __name__ == "__main__":
    main()
