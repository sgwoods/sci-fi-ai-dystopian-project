#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import urllib.request


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url) as response:  # noqa: S310
        return response.read().decode("utf-8")


def require_contains(haystack: str, needle: str, label: str) -> None:
    if needle not in haystack:
        raise AssertionError(f"Missing {label}: {needle}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8123")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")

    health = json.loads(fetch_text(f"{base}/api/health"))
    if not health.get("ok"):
        raise AssertionError("Health endpoint did not return ok=true")

    board = json.loads(fetch_text(f"{base}/api/board"))
    if not board.get("records"):
        raise AssertionError("Board endpoint returned no records")

    discovery = json.loads(fetch_text(f"{base}/api/discovery"))
    if discovery.get("target_count") != 100:
        raise AssertionError("Discovery target_count did not stay at 100")

    source_registry = json.loads(fetch_text(f"{base}/api/source-registry"))
    if not source_registry.get("records"):
        raise AssertionError("Source registry endpoint returned no records")

    query_library = json.loads(fetch_text(f"{base}/api/query-library"))
    if not query_library.get("records"):
        raise AssertionError("Query library endpoint returned no records")

    watchlist = json.loads(fetch_text(f"{base}/api/followup-watchlist"))
    if not watchlist.get("records"):
        raise AssertionError("Follow-up watchlist endpoint returned no records")

    scans = json.loads(fetch_text(f"{base}/api/source-scans"))
    if not scans.get("strategies"):
        raise AssertionError("Source scans endpoint returned no strategies")

    review_html = fetch_text(f"{base}/")
    public_html = fetch_text(f"{base}/public")
    harness_html = fetch_text(f"{base}/harness")

    require_contains(review_html, "Candidates", "review candidates tab")
    require_contains(review_html, "Approved", "review approved tab")
    require_contains(review_html, "More Quotes", "review more quotes tab")
    require_contains(review_html, "Find 6 More Quotes", "source candidates control")
    require_contains(review_html, "Refresh Lead Pool", "lead refresh control")
    require_contains(review_html, "Single Lead Refresh", "single-pass lead refresh control")
    require_contains(review_html, "Publish", "publish control")
    require_contains(review_html, "Find More Quotes", "quote-first intake explanation")
    require_contains(review_html, "What Your Declines Are Telling Me", "decline feedback section")
    require_contains(review_html, "Need Inspiration?", "inspiration section")
    require_contains(review_html, "What happens when you press Find More Quotes", "hunt explanation section")
    require_contains(review_html, "Research engine:", "research inventory summary")
    require_contains(review_html, "Current Hunt Research Plan", "hunt plan section")
    require_contains(review_html, "Source registry", "source registry section")
    require_contains(review_html, "Query library", "query library section")
    require_contains(review_html, "Follow-up watchlist", "follow-up watchlist section")
    require_contains(review_html, "Scanned at", "timestamped scan log")
    require_contains(review_html, "Outcome", "scan outcome column")
    require_contains(review_html, 'href="/public"', "public in-app route")
    require_contains(review_html, 'href="/harness"', "harness in-app route")
    require_contains(review_html, "statusButton", "inline status buttons")
    require_contains(review_html, "data-quick-decline", "quick decline buttons")
    require_contains(review_html, "Drag to reorder", "drag ordering affordance")
    require_contains(review_html, "data-move-direction", "quick reorder buttons")
    require_contains(review_html, "Open Details", "collapsed list detail toggle")
    require_contains(review_html, "save-note", "inline note save action")
    require_contains(review_html, 'href="/snapshot/', "local snapshot launch route")

    require_contains(public_html, "Approved Highlights", "public page approved section")
    require_contains(public_html, "How This Corpus Grows", "public page research section")
    require_contains(public_html, 'target="_blank"', "public page external launch links")

    require_contains(harness_html, "Run Tests", "harness runner button")
    require_contains(harness_html, "Run Live Candidate Intake", "live candidate intake button")
    require_contains(harness_html, "Review App", "harness review frame section")
    require_contains(harness_html, "Public Page", "harness public frame section")

    print("UI route checks passed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"UI route checks failed: {exc}", file=sys.stderr)
        raise
