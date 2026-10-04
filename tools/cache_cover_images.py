#!/usr/bin/env python3
"""Explicit online cache refresh; ordinary builds remain offline."""
import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "site/assets/ai-dystopia-quotes/covers"
MANIFEST = CACHE / "manifest.json"


def image_extension(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    raise ValueError("Not a supported raster image")


def cached_url(url):
    if not url or not MANIFEST.exists():
        return None
    entry = json.loads(MANIFEST.read_text()).get(url)
    if entry:
        path = CACHE / entry["file"]
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]:
            return "assets/ai-dystopia-quotes/covers/" + entry["file"]
    return None


def main():
    from build_quotes_project import SOURCE_WORK_OVERRIDES, BOARD_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Re-fetch already cached images")
    args = parser.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    records = json.loads(BOARD_PATH.read_text())["records"]
    sources = {SOURCE_WORK_OVERRIDES[r["id"]].get("cover_image_url"): SOURCE_WORK_OVERRIDES[r["id"]] for r in records}
    failures = []
    for url, work in sources.items():
        if not url or (not args.refresh and cached_url(url)):
            continue
        try:
            # curl uses the platform TLS trust store, including on macOS.
            time.sleep(1)
            with tempfile.TemporaryFile() as output:
                subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                                "--proto", "=https", "--proto-redir", "=https",
                                "--max-time", "30", "--max-filesize", "5000000", url],
                               stdout=output, check=True)
                output.seek(0)
                data = output.read(5_000_001)
            if len(data) > 5_000_000:
                raise ValueError("Image exceeds 5 MB")
            digest = hashlib.sha256(data).hexdigest()
            filename = digest + image_extension(data)
            (CACHE / filename).write_bytes(data)
            manifest[url] = {"file": filename, "sha256": digest, "source_page": work.get("cover_page_url"), "title": work["title"], "retrieved_at": datetime.now(timezone.utc).isoformat()}
            MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            print("Cached:", work["title"])
        except Exception as error:
            failures.append(url)
            print("FAILED (existing cache preserved):", work["title"], error)
    print(f"{len(manifest)} cached sources; {len(failures)} failures")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
