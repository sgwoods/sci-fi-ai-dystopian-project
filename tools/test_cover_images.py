"""Offline regression checks for cover caching, links, and export assets."""
import hashlib
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.request import urlopen

import cache_cover_images as cache
import build_quotes_project as build
import publish_public_project as publish
from review_app_server import ReviewAppHandler


class CoverTests(unittest.TestCase):
    def test_cache_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = b"\x89PNG\r\n\x1a\nfixture"
            (root / "cover.png").write_bytes(data)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"https://example.com/image": {
                "file": "cover.png", "sha256": hashlib.sha256(data).hexdigest()}}))
            with patch.object(cache, "CACHE", root), patch.object(cache, "MANIFEST", manifest):
                self.assertTrue(cache.cached_url("https://example.com/image"))
                (root / "cover.png").write_bytes(b"corrupt")
                self.assertIsNone(cache.cached_url("https://example.com/image"))
                self.assertIsNone(cache.cached_url("https://example.com/missing"))

    def test_reject_html(self):
        with self.assertRaises(ValueError):
            cache.image_extension(b"<html>Error</html>")

    def test_failed_refresh_preserves_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            manifest.write_text('{"existing": {"file": "cover.png"}}\n')
            (root / "cover.png").write_bytes(b"existing bytes")
            before = manifest.read_bytes()
            with patch.object(cache, "CACHE", root), patch.object(cache, "MANIFEST", manifest), \
                 patch("sys.argv", ["cache_cover_images.py", "--refresh"]), \
                 patch.object(cache.time, "sleep"), \
                 patch.object(cache.subprocess, "run", side_effect=OSError("offline")), \
                 patch("builtins.print"):
                self.assertTrue(cache.main())
            self.assertEqual(manifest.read_bytes(), before)
            self.assertEqual((root / "cover.png").read_bytes(), b"existing bytes")

    def test_image_routes(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), ReviewAppHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for entry in json.loads(cache.MANIFEST.read_text()).values():
                with urlopen(f"http://127.0.0.1:{server.server_port}/assets/ai-dystopia-quotes/covers/{entry['file']}") as response:
                    self.assertTrue(response.headers["Content-Type"].startswith("image/"))
                    self.assertEqual(hashlib.sha256(response.read()).hexdigest(), entry["sha256"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_board_links_and_cache(self):
        board = build.sync_source_work_overrides(json.loads(build.BOARD_PATH.read_text()))
        for record in board["records"]:
            work = record["source_work"]
            if work["type"] in {"film", "tv series", "tv episode", "video game"}:
                self.assertTrue(work["catalog_url"].startswith("https://www.imdb.com/title/"), work["title"])
            else:
                self.assertTrue(work["catalog_url"].startswith("https://www.amazon.ca/"), work["title"])
            if work["cover_source_url"]:
                self.assertIsNotNone(work["cover_image_url"], work["title"])
                self.assertTrue((build.ROOT / "site" / work["cover_image_url"]).is_file())

    def test_public_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(publish, "build_manifest", return_value={}):
                publish.publish_to_public(root, build.PROJECT_REPO_URL, dry_run=False, skip_index=True)
            data = json.loads((root / "data" / publish.APPROVED_EXPORT_NAME).read_text())
            page = (root / publish.PROJECT_PAGE_NAME).read_text()
            for record in data["records"]:
                image = record["source_work"].get("cover_image_url")
                if image:
                    self.assertIn(f'src="{image}"', page)
                    self.assertEqual((root / image).read_bytes(), (build.ROOT / "site" / image).read_bytes())
            self.assertNotIn('src="https://', page)


if __name__ == "__main__":
    unittest.main()
