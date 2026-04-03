#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.review-board.json"
BUILD_SCRIPT = ROOT / "tools" / "build_quotes_project.py"
TODAY = date.today().isoformat()
VALID_TARGET_STATUSES = {"candidate", "approved", "postponed", "declined"}


def load_board() -> dict[str, Any]:
    return json.loads(BOARD_PATH.read_text(encoding="utf-8"))


def save_board(board: dict[str, Any]) -> None:
    BOARD_PATH.write_text(json.dumps(board, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def find_record(board: dict[str, Any], quote_id: str) -> dict[str, Any]:
    for record in board["records"]:
        if record["id"] == quote_id:
            return record
    raise KeyError(f"Unknown quote id: {quote_id}")


def find_record_index(board: dict[str, Any], quote_id: str) -> int:
    for index, record in enumerate(board["records"]):
        if record["id"] == quote_id:
            return index
    raise KeyError(f"Unknown quote id: {quote_id}")


def move_record_to_status_lane_end(board: dict[str, Any], record_index: int, target_status: str) -> int:
    records = board["records"]
    record = records.pop(record_index)
    record["review"]["status"] = target_status
    insert_at = len(records)
    for idx, candidate in enumerate(records):
        if candidate["review"]["status"] == target_status:
            insert_at = idx + 1
    records.insert(insert_at, record)
    return insert_at


def rebuild_outputs() -> None:
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, check=True)


def update_status(
    status: str,
    quote_id: str,
    note: str | None,
    priority: str | None,
    next_action: str | None,
) -> None:
    if status not in VALID_TARGET_STATUSES:
        raise ValueError(f"Unsupported status: {status}")
    board = load_board()
    record_index = find_record_index(board, quote_id)
    original_status = board["records"][record_index]["review"]["status"]
    if status != original_status:
        record_index = move_record_to_status_lane_end(board, record_index, status)
    record = board["records"][record_index]
    record["review"]["decision_date"] = TODAY
    if note is not None:
        record["review"]["decision_note"] = note
    if status == "candidate":
        record["review"]["priority"] = priority or record["review"].get("priority") or "medium"
        record["review"]["next_action"] = (
            next_action
            or record["review"].get("next_action")
            or "Review for approval, postponement, or decline."
        )
    else:
        record["review"]["priority"] = None
        record["review"]["next_action"] = None
    save_board(board)
    rebuild_outputs()


def print_list(status: str | None) -> None:
    board = load_board()
    records = board["records"]
    if status:
        records = [record for record in records if record["review"]["status"] == status]
    records = sorted(records, key=lambda item: (item["review"]["status"], item["work_year"], item["work_title"]))
    for record in records:
        review = record["review"]
        print(
            f"{record['id']}\t{review['status']}\t{record['work_year']}\t{record['work_title']}\t"
            f"{review.get('decision_note', '')}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=sorted(VALID_TARGET_STATUSES))

    for command, status in (
        ("approve", "approved"),
        ("postpone", "postponed"),
        ("decline", "declined"),
        ("candidate", "candidate"),
    ):
        sub = subparsers.add_parser(command)
        sub.add_argument("quote_id")
        sub.add_argument("--note")
        if status == "candidate":
            sub.add_argument("--priority", choices=["high", "medium", "low"])
            sub.add_argument("--next-action")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "list":
        print_list(args.status)
        return
    if args.command == "approve":
        update_status("approved", args.quote_id, args.note, None, None)
        return
    if args.command == "postpone":
        update_status("postponed", args.quote_id, args.note, None, None)
        return
    if args.command == "decline":
        update_status("declined", args.quote_id, args.note, None, None)
        return
    if args.command == "candidate":
        update_status("candidate", args.quote_id, args.note, args.priority, args.next_action)
        return


if __name__ == "__main__":
    main()
