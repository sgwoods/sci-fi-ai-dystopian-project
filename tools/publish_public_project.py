#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "tools" / "build_quotes_project.py"
LOCAL_PUBLIC_PAGE = ROOT / "site" / "ai-dystopia-quotes-public-page.html"
LOCAL_APPROVED_JSON = ROOT / "data" / "approved" / "ai-dystopia-quotes.approved.json"
DEFAULT_PUBLIC_ROOT = Path(
    os.environ.get("AI_DYSTOPIA_PUBLIC_ROOT", str(Path.home() / "GitPages" / "public"))
)

PROJECT_ID = "ai-dystopia-quotes"
PROJECT_PAGE_NAME = "ai-dystopia-quotes.html"
PROJECT_MANIFEST_NAME = "ai-dystopia-quotes.json"
APPROVED_EXPORT_NAME = "ai-dystopia-quotes.approved.json"
DISPLAY_NAME = "AI Dystopia Quotes"
DESCRIPTION = (
    "Public project page for a curated corpus of recognizable dystopian AI "
    "quotations and source metadata."
)
STATUS_LABEL = "Current stage"
STATUS_VALUE = "Active curation + publishing"
FOCUS_LABEL = "Current focus"
FOCUS_VALUE = "Growing the approved canon and widening discovery"
PUBLIC_SYNC_SUMMARY = (
    "This public page is synced from the AI Dystopia Quotes editorial project. "
    "The public-facing source of truth on this site is the approved JSON export, "
    "while the broader review workflow remains part of the underlying curation project."
)


def run(command: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str, *, dry_run: bool) -> None:
    ensure_parent(path, dry_run)
    if dry_run:
        return
    path.write_text(text, encoding="utf-8")


def build_local_outputs(skip_build: bool) -> None:
    if skip_build:
        return
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, check=True)


def resolve_repo_url(explicit: str | None) -> str:
    if explicit:
        return explicit
    remote = run(["git", "remote", "get-url", "origin"], cwd=ROOT)
    if remote.startswith("git@github.com:"):
        slug = remote.removeprefix("git@github.com:").removesuffix(".git")
        return f"https://github.com/{slug}"
    return remote.removesuffix(".git")


def latest_repo_timestamp() -> str:
    return run(["git", "log", "-1", "--format=%cI"], cwd=ROOT)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def replace_first(pattern: str, replacement: str, text: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected one match for pattern: {pattern}")
    return updated


def render_public_page(local_html: str, repo_url: str) -> str:
    hero_actions = f"""<div class="heroActions">
                <a class="button" href="index.html">Open Steven Woods Projects</a>
                <a class="button" href="data/{APPROVED_EXPORT_NAME}" target="_blank" rel="noreferrer">Open Approved JSON</a>
                <a class="button" href="{repo_url}" target="_blank" rel="noreferrer">Open Source Project</a>
                <a class="button" href="data/projects/{PROJECT_MANIFEST_NAME}">Open Project Manifest</a>
            </div>"""
    provenance_links = f"""<div class="links">
                <a class="button" href="data/{APPROVED_EXPORT_NAME}" target="_blank" rel="noreferrer">Approved JSON</a>
                <a class="button" href="data/projects/{PROJECT_MANIFEST_NAME}">Project Manifest</a>
                <a class="button" href="{repo_url}" target="_blank" rel="noreferrer">Source Project</a>
                <a class="button" href="index.html">Steven Woods Projects</a>
            </div>"""

    html = local_html
    html = replace_first(r'<div class="heroActions">.*?</div>', hero_actions, html)
    html = replace_first(
        r'(<section class="panel">\s*<h2>Project Provenance</h2>\s*<p>)(.*?)(</p>)',
        r"\1" + PUBLIC_SYNC_SUMMARY + r"\3",
        html,
    )
    html = replace_first(
        r'(<section class="panel">\s*<h2>Project Provenance</h2>.*?<p>.*?</p>\s*)(<div class="links">.*?</div>)',
        r"\1" + provenance_links,
        html,
    )
    html = html.replace(f'href="/data/approved/{APPROVED_EXPORT_NAME}"', f'href="data/{APPROVED_EXPORT_NAME}"')
    html = html.replace(f'href="/data/review/{PROJECT_ID}.review-board.json"', f'href="data/projects/{PROJECT_MANIFEST_NAME}"')
    html = html.replace('href="/"', 'href="index.html"')
    return html


def build_manifest(repo_url: str) -> dict[str, Any]:
    repo_pushed_at = latest_repo_timestamp()
    generated_at = now_utc_iso()
    return {
        "schema_version": "1.0",
        "project_id": PROJECT_ID,
        "active": True,
        "display_name": DISPLAY_NAME,
        "description": DESCRIPTION,
        "project_page_path": PROJECT_PAGE_NAME,
        "repo_url": repo_url,
        "dashboard_url": None,
        "experience_url": None,
        "repo_pushed_at": repo_pushed_at,
        "status_generated_at": generated_at,
        "status_label": STATUS_LABEL,
        "status_value": STATUS_VALUE,
        "focus_label": FOCUS_LABEL,
        "focus_value": FOCUS_VALUE,
    }


def publish_to_public(public_root: Path, repo_url: str, *, dry_run: bool, skip_index: bool) -> None:
    local_html = LOCAL_PUBLIC_PAGE.read_text(encoding="utf-8")
    local_json = LOCAL_APPROVED_JSON.read_text(encoding="utf-8")
    public_html = render_public_page(local_html, repo_url)
    manifest = build_manifest(repo_url)

    html_path = public_root / PROJECT_PAGE_NAME
    json_path = public_root / "data" / APPROVED_EXPORT_NAME
    manifest_path = public_root / "data" / "projects" / PROJECT_MANIFEST_NAME

    write_text(html_path, public_html, dry_run=dry_run)
    write_text(json_path, local_json, dry_run=dry_run)
    write_text(
        manifest_path,
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        dry_run=dry_run,
    )

    if not skip_index:
        render_index = public_root / "tools" / "render_index.py"
        if not dry_run:
            subprocess.run([sys.executable, str(render_index)], cwd=public_root, check=True)


def verify_public_output(public_root: Path) -> None:
    manifest_path = public_root / "data" / "projects" / PROJECT_MANIFEST_NAME
    public_page_path = public_root / PROJECT_PAGE_NAME
    index_path = public_root / "index.html"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["project_id"] != PROJECT_ID:
        raise ValueError("Published manifest has the wrong project_id.")
    if manifest["project_page_path"] != PROJECT_PAGE_NAME:
        raise ValueError("Published manifest has the wrong project page path.")

    public_page = public_page_path.read_text(encoding="utf-8")
    if DISPLAY_NAME not in public_page:
        raise ValueError("Public project page missing project title.")
    if PUBLIC_SYNC_SUMMARY not in public_page:
        raise ValueError("Public project page missing sync/provenance summary.")

    index_page = index_path.read_text(encoding="utf-8")
    if DISPLAY_NAME not in index_page:
        raise ValueError("Shared public homepage missing project entry.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish this project's public page, approved JSON, and shared public manifest."
    )
    parser.add_argument(
        "--public-root",
        type=Path,
        default=DEFAULT_PUBLIC_ROOT,
        help="Root of the shared public site checkout. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--repo-url",
        help="Explicit repository URL. Defaults to the local git origin remote.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip rebuilding local generated outputs before publishing.",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Skip rerendering the shared public homepage index.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute the publish outputs without writing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_url = resolve_repo_url(args.repo_url)
    build_local_outputs(args.skip_build)
    publish_to_public(args.public_root, repo_url, dry_run=args.dry_run, skip_index=args.skip_index)
    if not args.dry_run:
        verify_public_output(args.public_root)
    print(f"Published {DISPLAY_NAME} to {args.public_root}")
    print(f"Project page: {args.public_root / PROJECT_PAGE_NAME}")
    print(f"Manifest: {args.public_root / 'data' / 'projects' / PROJECT_MANIFEST_NAME}")
    print(f"Approved JSON: {args.public_root / 'data' / APPROVED_EXPORT_NAME}")


if __name__ == "__main__":
    main()
