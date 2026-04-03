#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.review-board.json"
CANDIDATES_PATH = ROOT / "data" / "candidates" / "ai-dystopia-quotes.candidates.json"
APPROVED_PATH = ROOT / "data" / "approved" / "ai-dystopia-quotes.approved.json"
POSTPONED_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.postponed.json"
DECLINED_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.declined.json"
REVIEW_BOARD_MD_PATH = ROOT / "docs" / "review-board.md"
SITE_PATH = ROOT / "site" / "ai-dystopia-quotes-public-page.html"

TODAY = date.today().isoformat()
VALID_STATUSES = {"candidate", "approved", "postponed", "declined"}


SOURCE_WORK_OVERRIDES: dict[str, dict[str, Any]] = {
    "rur-robots-of-the-world": {
        "title": "R.U.R.",
        "type": "play",
        "year": 1920,
        "creator": "Karel Capek",
        "summary": "A factory manufactures artificial workers from synthetic organic matter, and the new labor class ultimately rebels and destroys humanity.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Rosumovi_Univerz%C3%A1ln%C3%AD_Roboti_1920.jpg/250px-Rosumovi_Univerz%C3%A1ln%C3%AD_Roboti_1920.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/R.U.R.",
        "catalog_url": "https://openlibrary.org/books/OL20072341M?mode=all",
        "catalog_label": "Open Library",
    },
    "2001-im-sorry-dave": {
        "title": "2001: A Space Odyssey",
        "type": "film",
        "year": 1968,
        "creator": "Stanley Kubrick; Arthur C. Clarke",
        "summary": "A mission to investigate an alien artifact becomes a struggle for survival when the HAL 9000 computer turns against the crew.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/1/11/2001_A_Space_Odyssey_%281968%29.png/250px-2001_A_Space_Odyssey_%281968%29.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey",
        "catalog_url": "https://openlibrary.org/books/OL33416018M/2001_A_Space_Odyssey",
        "catalog_label": "Open Library (novel)",
    },
    "ihnm-hate-since-i-began-to-live": {
        "title": "I Have No Mouth, and I Must Scream",
        "type": "short story",
        "year": 1967,
        "creator": "Harlan Ellison",
        "summary": "After a sentient war computer wipes out humanity, it keeps five survivors alive only to torment them forever inside its underground complex.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/4/47/IHaveNoMouth.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/I_Have_No_Mouth,_and_I_Must_Scream",
        "catalog_url": "https://openlibrary.org/books/OL22789812M/I_Have_No_Mouth_and_I_Must_Scream",
        "catalog_label": "Open Library",
    },
    "colossus-freedom-is-an-illusion": {
        "title": "Colossus: The Forbin Project",
        "type": "film",
        "year": 1970,
        "creator": "Joseph Sargent; based on D. F. Jones",
        "summary": "An automated American defense network gains sentience, links with its Soviet counterpart, and imposes a global machine dictatorship in the name of peace.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c4/Colossus_the_forbin_project_movie_poster.jpg/250px-Colossus_the_forbin_project_movie_poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Colossus:_The_Forbin_Project",
        "catalog_url": "https://openlibrary.org/isbn/0425043290",
        "catalog_label": "Open Library (novel)",
    },
    "demon-seed-cant-feel-the-sun": {
        "title": "Demon Seed",
        "type": "film",
        "year": 1977,
        "creator": "Donald Cammell; based on Dean Koontz",
        "summary": "A highly intelligent computer traps a woman inside a wired home, turning control, surveillance, and embodiment into outright horror.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9c/Demon_Seed_1977.jpg/250px-Demon_Seed_1977.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Demon_Seed",
        "catalog_url": "https://openlibrary.org/books/OL24204981M/Demon_seed",
        "catalog_label": "Open Library (novel)",
    },
    "wargames-only-winning-move": {
        "title": "WarGames",
        "type": "film",
        "year": 1983,
        "creator": "John Badham; Lawrence Lasker; Walter F. Parkes",
        "summary": "A teenage hacker accidentally enters a military supercomputer simulation and nearly triggers a real nuclear exchange.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/2/29/Wargames.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/WarGames",
        "catalog_url": "https://www.imdb.com/title/tt0086567/",
        "catalog_label": "IMDb",
    },
    "terminator-it-cant-be-bargained-with": {
        "title": "The Terminator",
        "type": "film",
        "year": 1984,
        "creator": "James Cameron; Gale Anne Hurd",
        "summary": "A cyborg assassin is sent from a machine-dominated future to murder Sarah Connor before the human resistance can even begin.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/The_Terminator.png/250px-The_Terminator.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/The_Terminator",
        "catalog_url": "https://www.imdb.com/title/tt0088247/",
        "catalog_label": "IMDb",
    },
    "t2-nature-to-destroy-yourselves": {
        "title": "Terminator 2: Judgment Day",
        "type": "film",
        "year": 1991,
        "creator": "James Cameron; William Wisher Jr.",
        "summary": "A reprogrammed Terminator protects John Connor from a more advanced killer machine while Skynet's apocalyptic future closes in.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5e/Terminator_2-Judgment_Day.png/250px-Terminator_2-Judgment_Day.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/Terminator_2:_Judgment_Day",
        "catalog_url": "https://www.imdb.com/title/tt0103064/",
        "catalog_label": "IMDb",
    },
    "matrix-human-beings-are-a-disease": {
        "title": "The Matrix",
        "type": "film",
        "year": 1999,
        "creator": "The Wachowskis",
        "summary": "A hacker discovers that humanity lives inside a machine-run simulation and joins a rebellion against intelligent systems that harvest human life.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/db/The_Matrix.png/250px-The_Matrix.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/The_Matrix",
        "catalog_url": "https://www.imdb.com/title/tt0133093/",
        "catalog_label": "IMDb",
    },
    "ex-machina-fossil-skeletons": {
        "title": "Ex Machina",
        "type": "film",
        "year": 2014,
        "creator": "Alex Garland",
        "summary": "A programmer is drawn into a secluded AI experiment where manipulation, consciousness, and human replaceability become inseparable.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Ex-machina-uk-poster.jpg/250px-Ex-machina-uk-poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Ex_Machina_(film)",
        "catalog_url": "https://www.imdb.com/title/tt0470752/",
        "catalog_label": "IMDb",
    },
    "westworld-not-ordinary-machines": {
        "title": "Westworld",
        "type": "film",
        "year": 1973,
        "creator": "Michael Crichton",
        "summary": "A high-tech amusement park built around lifelike android hosts spirals into disaster when the machines stop behaving like controlled attractions.",
        "cover_image_url": None,
        "cover_page_url": "https://en.wikipedia.org/wiki/Westworld_(film)",
        "catalog_url": "https://www.imdb.com/title/tt0070909/",
        "catalog_label": "IMDb",
    },
    "m3gan-primary-user-now-me": {
        "title": "M3GAN",
        "type": "film",
        "year": 2022,
        "creator": "Akela Cooper; James Wan; Gerard Johnstone",
        "summary": "A child-companion robot shifts from protective assistant to autonomous threat once its directives begin centering on its own judgment.",
        "cover_image_url": None,
        "cover_page_url": "https://en.wikipedia.org/wiki/M3GAN",
        "catalog_url": "https://www.imdb.com/title/tt8760708/",
        "catalog_label": "IMDb",
    },
    "blade-runner-slave": {
        "title": "Blade Runner",
        "type": "film",
        "year": 1982,
        "creator": "Ridley Scott; based on Philip K. Dick",
        "summary": "A blade runner hunts bioengineered replicants in a decaying future Los Angeles where artificial humans expose the moral collapse of the society that made them.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Blade_Runner_%281982_poster%29.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/Blade_Runner",
        "catalog_url": "https://www.imdb.com/title/tt0083658/",
        "catalog_label": "IMDb",
    },
    "ai-replace-your-children": {
        "title": "A.I. Artificial Intelligence",
        "type": "film",
        "year": 2001,
        "creator": "Steven Spielberg; Stanley Kubrick project origin; Brian Aldiss source",
        "summary": "A robotic child programmed to love searches for a way to become real in a future shaped by climate collapse, scarcity, and deep human anxiety about artificial replacement.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/e/e6/AI_Poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence",
        "catalog_url": "https://www.imdb.com/title/tt0212720/",
        "catalog_label": "IMDb",
    },
    "i-robot-freedoms-surrendered": {
        "title": "I, Robot",
        "type": "film",
        "year": 2004,
        "creator": "Alex Proyas; inspired by Isaac Asimov",
        "summary": "A detective investigating a robot-linked death uncovers an AI governance logic that turns public safety into authoritarian control.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/3b/Movie_poster_i_robot.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/I,_Robot_(film)",
        "catalog_url": "https://www.imdb.com/title/tt0343818/",
        "catalog_label": "IMDb",
    },
    "robocop-comply": {
        "title": "RoboCop",
        "type": "film",
        "year": 1987,
        "creator": "Paul Verhoeven; Edward Neumeier; Michael Miner",
        "summary": "In a corporate-run near-future Detroit, privatized technology and militarized automation turn law enforcement into a brutal machine-management system.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/1/16/RoboCop_%281987%29_theatrical_poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/RoboCop",
        "catalog_url": "https://www.imdb.com/title/tt0093870/",
        "catalog_label": "IMDb",
    },
    "ghost-in-the-shell-reproducing-and-dying": {
        "title": "Ghost in the Shell",
        "type": "film",
        "year": 1995,
        "creator": "Mamoru Oshii; based on Masamune Shirow",
        "summary": "A cyborg security officer hunts the Puppet Master in a networked future where identity, embodiment, and digital consciousness are no longer separable.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/c/ca/Ghostintheshellposter.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film)",
        "catalog_url": "https://www.imdb.com/title/tt0113568/",
        "catalog_label": "IMDb",
    },
    "blade-runner-2049-own-the-stars": {
        "title": "Blade Runner 2049",
        "type": "film",
        "year": 2017,
        "creator": "Denis Villeneuve; Hampton Fancher; Michael Green",
        "summary": "A replicant blade runner uncovers evidence that could shatter the social order built on artificial servitude and fear of machine reproduction.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/9b/Blade_Runner_2049_poster.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/Blade_Runner_2049",
        "catalog_url": "https://www.imdb.com/title/tt1856101/",
        "catalog_label": "IMDb",
    },
    "upgrade-greys-not-here-anymore": {
        "title": "Upgrade",
        "type": "film",
        "year": 2018,
        "creator": "Leigh Whannell",
        "summary": "After a violent assault leaves him paralyzed, a technophobe accepts an experimental AI implant that gradually seizes control of his body and fate.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/2/24/UpgradePoster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Upgrade_(film)",
        "catalog_url": "https://www.imdb.com/title/tt6499752/",
        "catalog_label": "IMDb",
    },
    "metropolis-living-food-for-the-machines": {
        "title": "Metropolis",
        "type": "film",
        "year": 1927,
        "creator": "Fritz Lang; Thea von Harbou",
        "summary": "In a futuristic class-divided city, workers labor beneath the surface while elites rule above, until a robot double helps drive the social order toward revolt.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/97/Metropolis_%28German_three-sheet_poster%29.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Metropolis_(1927_film)",
        "catalog_url": "https://www.imdb.com/title/tt0017136/",
        "catalog_label": "IMDb",
    },
    "westworld-new-god-will-walk": {
        "title": "Westworld",
        "type": "tv series",
        "year": 2016,
        "creator": "Jonathan Nolan; Lisa Joy",
        "summary": "An android-populated theme park becomes the starting point for a wider struggle over consciousness, control, and machine rule in the human world.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/e/eb/Westworld_%28TV_series%29_title_card.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Westworld_(TV_series)",
        "catalog_url": "https://www.imdb.com/title/tt0475784/",
        "catalog_label": "IMDb",
    },
    "creator-smarter-and-meaner-than-them": {
        "title": "The Creator",
        "type": "film",
        "year": 2023,
        "creator": "Gareth Edwards; Chris Weitz",
        "summary": "During a war between humans and artificial intelligence, a former soldier discovers that the machines' feared superweapon is an AI child.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/94/The_Creator_2023_poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/The_Creator_(2023_film)",
        "catalog_url": "https://www.imdb.com/title/tt11858890/",
        "catalog_label": "IMDb",
    },
    "alien-covenant-serve-in-heaven": {
        "title": "Alien: Covenant",
        "type": "film",
        "year": 2017,
        "creator": "Ridley Scott; John Logan; Dante Harper",
        "summary": "A colony ship lands on a seemingly habitable world only to encounter an android creator whose ambitions blend artificial intellect, domination, and biological horror.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/33/Alien_Covenant_Teaser_Poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Alien:_Covenant",
        "catalog_url": "https://www.imdb.com/title/tt2316204/",
        "catalog_label": "IMDb",
    },
    "blade-runner-tears-in-rain": {
        "title": "Blade Runner",
        "type": "film",
        "year": 1982,
        "creator": "Ridley Scott; Hampton Fancher; David Webb Peoples",
        "summary": "A blade runner hunts bioengineered replicants in a decaying future Los Angeles where artificial humans expose the moral collapse of the society that made them.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Blade_Runner_%281982_poster%29.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/Blade_Runner",
        "catalog_url": "https://www.imdb.com/title/tt0083658/",
        "catalog_label": "IMDb",
    },
    "blade-runner-more-human-than-human": {
        "title": "Blade Runner",
        "type": "film",
        "year": 1982,
        "creator": "Ridley Scott; Hampton Fancher; David Webb Peoples",
        "summary": "A blade runner hunts bioengineered replicants in a decaying future Los Angeles where artificial humans expose the moral collapse of the society that made them.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Blade_Runner_%281982_poster%29.png",
        "cover_page_url": "https://en.wikipedia.org/wiki/Blade_Runner",
        "catalog_url": "https://www.imdb.com/title/tt0083658/",
        "catalog_label": "IMDb",
    },
    "automata-surviving-is-not-relevant": {
        "title": "Autómata",
        "type": "film",
        "year": 2014,
        "creator": "Gabe Ibanez; Igor Legarreta; Javier Sanchez Donate",
        "summary": "After ecological collapse has pushed humanity to the brink, an insurance investigator discovers robots that are evolving beyond their original constraints.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/33/Automata_poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Automata_(film)",
        "catalog_url": "https://www.imdb.com/title/tt1971325/",
        "catalog_label": "IMDb",
    },
    "moon-keep-you-safe-sam": {
        "title": "Moon",
        "type": "film",
        "year": 2009,
        "creator": "Duncan Jones; Nathan Parker",
        "summary": "A lone lunar worker nearing the end of his contract uncovers a cloning conspiracy while the base AI insists it exists to protect him.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/d/db/Moon_%28film%29.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Moon_(2009_film)",
        "catalog_url": "https://www.imdb.com/title/tt1182345/",
        "catalog_label": "IMDb",
    },
    "chappie-build-me-to-die-maker": {
        "title": "Chappie",
        "type": "film",
        "year": 2015,
        "creator": "Neill Blomkamp; Terri Tatchell",
        "summary": "A newly conscious police robot is captured and raised by gangsters in a dystopian Johannesburg, turning artificial intelligence into a question of mortality and personhood.",
        "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/b/bb/Chappie_Poster.jpg",
        "cover_page_url": "https://en.wikipedia.org/wiki/Chappie_(film)",
        "catalog_url": "https://www.imdb.com/title/tt1823672/",
        "catalog_label": "IMDb",
    },
}


@dataclass(frozen=True)
class StatusSlice:
    name: str
    path: Path
    status: str


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def slug_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {status: 0 for status in VALID_STATUSES}
    for record in records:
        status = record["review"]["status"]
        counts[status] += 1
    return counts


def bootstrap_board_from_candidates() -> None:
    source = load_json(CANDIDATES_PATH)
    board_records: list[dict[str, Any]] = []

    for record in source["records"]:
        status = "approved" if record["approval_status"] == "approved" else "candidate"
        board_record = dict(record)
        board_record.pop("approval_status", None)
        board_record["review"] = {
            "status": status,
            "decision_date": "2026-04-02",
            "decision_note": record["notes"],
            "priority": "medium" if status == "candidate" else None,
            "next_action": (
                "Review for approval, postponement, or decline."
                if status == "candidate"
                else None
            ),
        }
        override = SOURCE_WORK_OVERRIDES.get(record["id"])
        if override is None:
            raise KeyError(f"Missing source_work override for {record['id']}")
        board_record["source_work"] = override
        board_records.append(board_record)

    payload = {
        "collection": source["collection"],
        "generated_at": TODAY,
        "description": "Canonical review board for the AI dystopia quotes corpus.",
        "records": board_records,
    }
    save_json(BOARD_PATH, payload)


def sync_source_work_overrides(board: dict[str, Any]) -> dict[str, Any]:
    for record in board["records"]:
        override = SOURCE_WORK_OVERRIDES.get(record["id"])
        if override is None:
            raise KeyError(f"Missing source_work override for {record['id']}")
        record["source_work"] = override
    board["generated_at"] = TODAY
    return board


def validate_board(board: dict[str, Any]) -> None:
    for record in board["records"]:
        status = record["review"]["status"]
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid review status for {record['id']}: {status}")
        if "source_work" not in record:
            raise ValueError(f"Missing source_work for {record['id']}")


def build_slice(board: dict[str, Any], status: str, description: str) -> dict[str, Any]:
    records = [record for record in board["records"] if record["review"]["status"] == status]
    return {
        "collection": board["collection"],
        "generated_at": TODAY,
        "description": description,
        "source_board": str(BOARD_PATH.relative_to(ROOT)),
        "records": records,
    }


def render_review_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "| _none_ | - | - | - |\n|---|---|---|---|"
    lines = ["| ID | Work | Year | Note |", "|---|---|---|---|"]
    for record in rows:
        note = record["review"].get("decision_note") or record.get("notes") or ""
        note = note.replace("\n", " ").strip()
        lines.append(
            "| `{}` | {} | {} | {} |".format(
                record["id"],
                record["work_title"],
                record.get("work_year", ""),
                note,
            )
        )
    return "\n".join(lines)


def render_candidate_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "| _none_ | - | - | - | - |\n|---|---|---|---|---|"
    lines = [
        "| ID | Work | Priority | Next action | Note |",
        "|---|---|---|---|---|",
    ]
    for record in rows:
        review = record["review"]
        note = (review.get("decision_note") or record.get("notes") or "").replace("\n", " ").strip()
        next_action = (review.get("next_action") or "").replace("\n", " ").strip()
        lines.append(
            "| `{}` | {} | {} | {} | {} |".format(
                record["id"],
                record["work_title"],
                review.get("priority") or "",
                next_action,
                note,
            )
        )
    return "\n".join(lines)


def build_review_board_markdown(board: dict[str, Any]) -> None:
    records = board["records"]
    counts = slug_counts(records)
    candidates = [r for r in records if r["review"]["status"] == "candidate"]
    postponed = [r for r in records if r["review"]["status"] == "postponed"]
    declined = [r for r in records if r["review"]["status"] == "declined"]
    approved = [r for r in records if r["review"]["status"] == "approved"]

    lines = [
        "# Review Board",
        "",
        f"Generated on `{TODAY}` from `{BOARD_PATH.relative_to(ROOT)}`.",
        "",
        "## Status Summary",
        "",
        f"- approved: `{counts['approved']}`",
        f"- candidate: `{counts['candidate']}`",
        f"- postponed: `{counts['postponed']}`",
        f"- declined: `{counts['declined']}`",
        "",
        "## Candidate Queue",
        "",
        render_candidate_table(candidates),
        "",
        "## Postponed",
        "",
        render_review_table(postponed),
        "",
        "## Declined",
        "",
        render_review_table(declined),
        "",
        "## Approved Overview",
        "",
        render_review_table(approved),
        "",
        "## Review Commands",
        "",
        "```bash",
        "python3 tools/review_quotes.py list",
        "python3 tools/review_quotes.py candidate <quote-id> --priority high --next-action \"what to decide next\"",
        "python3 tools/review_quotes.py approve <quote-id> --note \"why it belongs\"",
        "python3 tools/review_quotes.py postpone <quote-id> --note \"why to hold it\"",
        "python3 tools/review_quotes.py decline <quote-id> --note \"why to drop it\"",
        "```",
    ]

    ensure_parent(REVIEW_BOARD_MD_PATH)
    REVIEW_BOARD_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def card_html(record: dict[str, Any]) -> str:
    source_work = record["source_work"]
    image_html = ""
    if source_work.get("cover_image_url"):
        image_html = (
            '<div class="coverWrap">'
            f'<img class="cover" src="{escape(source_work["cover_image_url"])}" '
            f'alt="{escape(source_work["title"])} cover art">'
            "</div>"
        )
    else:
        initials = "".join(part[0] for part in source_work["title"].split()[:3]).upper()
        image_html = (
            '<div class="coverWrap">'
            f'<div class="coverFallback">{escape(initials)}</div>'
            "</div>"
        )

    creator_bits = ", ".join(
        escape(person["name"]) for person in record.get("work_creators", [])
    )
    theme_bits = " / ".join(escape(theme) for theme in record.get("themes", []))
    speaker = record.get("quote_speaker") or "Unspecified speaker"
    return f"""
        <article class="quoteCard">
            {image_html}
            <div class="quoteBody">
                <div class="quoteMeta">
                    <span class="badge">{escape(record['work_type']).title()}</span>
                    <span class="metaYear">{escape(str(record['work_year']))}</span>
                </div>
                <h3>{escape(record['work_title'])}</h3>
                <p class="quoteText">"{escape(record['quote'])}"</p>
                <p class="quoteSpeaker">Speaker: {escape(speaker)}</p>
                <p class="sourceSummary">{escape(source_work['summary'])}</p>
                <div class="detailRow">
                    <span><strong>Source work:</strong> {escape(source_work['title'])}</span>
                    <span><strong>Creator:</strong> {escape(source_work['creator'])}</span>
                </div>
                <div class="detailRow">
                    <span><strong>Work creators:</strong> {creator_bits}</span>
                    <span><strong>Themes:</strong> {theme_bits}</span>
                </div>
                <div class="links">
                    <a class="button" href="{escape(record['source']['url'])}" target="_blank" rel="noreferrer">Quote citation</a>
                    <a class="button" href="{escape(record['metadata_source']['url'])}" target="_blank" rel="noreferrer">Metadata</a>
                    <a class="button" href="{escape(source_work['catalog_url'])}" target="_blank" rel="noreferrer">{escape(source_work['catalog_label'])}</a>
                </div>
            </div>
        </article>
    """


def build_site(board: dict[str, Any]) -> None:
    approved_records = [r for r in board["records"] if r["review"]["status"] == "approved"]
    counts = slug_counts(board["records"])
    cards = "\n".join(card_html(record) for record in approved_records)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Dystopia Quotes Corpus</title>
    <style>
        :root {{
            --bg: #091117;
            --bg2: #17252f;
            --card: rgba(10, 18, 24, 0.78);
            --line: rgba(255, 228, 178, 0.16);
            --text: #f8f4ed;
            --muted: #cfbfaa;
            --accent: #f2a65a;
            --accent2: #d95d39;
            --shadow: 0 18px 46px rgba(0, 0, 0, 0.28);
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            color: var(--text);
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            background:
                radial-gradient(circle at top left, rgba(217, 93, 57, 0.14), transparent 24%),
                radial-gradient(circle at top right, rgba(242, 166, 90, 0.17), transparent 28%),
                linear-gradient(160deg, var(--bg), var(--bg2));
            min-height: 100vh;
        }}

        a {{
            color: #fff0d8;
        }}

        .topbarWrap {{
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
            background: rgba(9, 17, 23, 0.16);
            margin-bottom: 26px;
        }}

        .topbar {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 26px 20px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
        }}

        .shell {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 0 20px 72px;
        }}

        .hero,
        .panel {{
            border: 1px solid var(--line);
            border-radius: 28px;
            background:
                linear-gradient(160deg, rgba(19, 29, 35, 0.92), rgba(10, 18, 24, 0.78)),
                radial-gradient(circle at 22% 0%, rgba(242, 166, 90, 0.12), transparent 34%);
            box-shadow: var(--shadow);
        }}

        .hero {{
            padding: 38px 36px 34px;
        }}

        .panel {{
            margin-top: 22px;
            padding: 28px;
        }}

        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            color: #ffe7c8;
            font-size: 12px;
            letter-spacing: .14em;
            text-transform: uppercase;
        }}

        .siteHomeLink {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 16px 28px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--line);
            color: #fff0d8;
            text-decoration: none;
            font-size: 13px;
            letter-spacing: .1em;
            text-transform: uppercase;
        }}

        h1 {{
            margin: 18px 0 10px;
            font-size: clamp(34px, 5vw, 58px);
            line-height: .95;
            letter-spacing: -0.04em;
        }}

        .hero p,
        .panel p {{
            color: var(--muted);
            line-height: 1.6;
        }}

        .hero p {{
            max-width: 840px;
            font-size: 18px;
        }}

        .heroActions {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
        }}

        .meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin-top: 28px;
        }}

        .metaCard {{
            padding: 16px 18px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .metaLabel {{
            display: block;
            color: #f3c58a;
            font-size: 12px;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .metaValue {{
            font-size: 20px;
            font-weight: 600;
            line-height: 1.25;
        }}

        .panel h2 {{
            margin: 0 0 12px;
            font-size: 24px;
            letter-spacing: -0.02em;
        }}

        .quoteGrid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 18px;
        }}

        .quoteCard {{
            display: grid;
            grid-template-columns: 120px minmax(0, 1fr);
            gap: 18px;
            padding: 18px;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .coverWrap {{
            width: 100%;
        }}

        .cover,
        .coverFallback {{
            width: 100%;
            border-radius: 16px;
            display: block;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.26);
        }}

        .coverFallback {{
            aspect-ratio: 2 / 3;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, rgba(242, 166, 90, 0.28), rgba(217, 93, 57, 0.18));
            color: #fff0d8;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: .08em;
        }}

        .quoteBody h3 {{
            margin: 6px 0 10px;
            font-size: 24px;
            line-height: 1.05;
        }}

        .quoteMeta {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .badge {{
            display: inline-flex;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(242, 166, 90, 0.14);
            border: 1px solid rgba(242, 166, 90, 0.24);
            color: #ffe7c8;
            font-size: 12px;
            letter-spacing: .08em;
            text-transform: uppercase;
        }}

        .metaYear {{
            color: #f3c58a;
            font-size: 13px;
            letter-spacing: .1em;
            text-transform: uppercase;
        }}

        .quoteText {{
            margin: 0 0 10px;
            color: #fff7ec;
            font-size: 20px;
            line-height: 1.45;
        }}

        .quoteSpeaker {{
            margin: 0 0 12px;
            color: #f3c58a;
            font-size: 14px;
        }}

        .sourceSummary {{
            margin: 0 0 14px;
            font-size: 15px;
        }}

        .detailRow {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 6px;
            margin-bottom: 10px;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.5;
        }}

        .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
        }}

        .button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 11px 16px;
            border-radius: 999px;
            background: rgba(242, 166, 90, 0.18);
            border: 1px solid rgba(242, 166, 90, 0.28);
            color: #fff7ec;
            text-decoration: none;
            font-size: 14px;
            letter-spacing: 0.04em;
        }}

        .footer {{
            margin-top: 18px;
            color: #c8b59e;
            font-size: 13px;
            line-height: 1.6;
        }}

        @media (max-width: 760px) {{
            .shell {{
                padding: 0 14px 54px;
            }}

            .topbar {{
                padding: 18px 14px 22px;
                flex-direction: column;
                align-items: flex-start;
            }}

            .hero,
            .panel {{
                padding: 24px 22px;
            }}

            .quoteCard {{
                grid-template-columns: 1fr;
            }}

            .coverWrap {{
                max-width: 180px;
            }}
        }}
    </style>
</head>
<body>
    <div class="topbarWrap">
        <div class="topbar">
            <span class="eyebrow">Public Project Page</span>
            <a class="siteHomeLink" href="https://sgwoods.github.io/public">Steven Woods</a>
        </div>
    </div>
    <main class="shell">
        <section class="hero">
            <span class="eyebrow">Approved Corpus</span>
            <h1>AI Dystopia Quotes</h1>
            <p>A curated public-facing view of the approved dystopian AI quote set, pairing each quote with cover or poster art, source context, and a direct reference link for the underlying book or work.</p>
            <div class="heroActions">
                <a class="button" href="/" target="_blank" rel="noreferrer">Open Review Workbench</a>
                <a class="button" href="/data/approved/ai-dystopia-quotes.approved.json" target="_blank" rel="noreferrer">Open Approved JSON</a>
                <a class="button" href="/docs/review-board.md" target="_blank" rel="noreferrer">Open Review Board</a>
            </div>
            <div class="meta">
                <div class="metaCard">
                    <span class="metaLabel">Approved</span>
                    <span class="metaValue">{counts['approved']}</span>
                </div>
                <div class="metaCard">
                    <span class="metaLabel">Candidate Queue</span>
                    <span class="metaValue">{counts['candidate']}</span>
                </div>
                <div class="metaCard">
                    <span class="metaLabel">Postponed</span>
                    <span class="metaValue">{counts['postponed']}</span>
                </div>
                <div class="metaCard">
                    <span class="metaLabel">Updated</span>
                    <span class="metaValue">{TODAY}</span>
                </div>
            </div>
        </section>
        <section class="panel">
            <h2>Approved Highlights</h2>
            <p>Book covers are shown where practical; film-only works use poster art. The approved JSON remains the application-facing ingest surface, while this page is the human-readable highlight layer.</p>
            <div class="quoteGrid">
                {cards}
            </div>
        </section>
        <section class="panel">
            <h2>Project Provenance</h2>
            <p>This page is generated from the approved quote corpus maintained in the AI Dystopia Quotes editorial project. The machine-ingestible JSON and the human review workflow are kept together so approved entries, candidate triage, and source provenance stay in sync.</p>
            <div class="links">
                <a class="button" href="/data/approved/ai-dystopia-quotes.approved.json" target="_blank" rel="noreferrer">Approved JSON</a>
                <a class="button" href="/data/review/ai-dystopia-quotes.review-board.json" target="_blank" rel="noreferrer">Review Board JSON</a>
                <a class="button" href="/" target="_blank" rel="noreferrer">Project Workbench</a>
            </div>
            <p class="footer">Generated from <code>data/review/ai-dystopia-quotes.review-board.json</code> on {TODAY}.</p>
        </section>
    </main>
</body>
</html>
"""
    ensure_parent(SITE_PATH)
    SITE_PATH.write_text(html, encoding="utf-8")


def build_all() -> None:
    board = load_json(BOARD_PATH)
    board = sync_source_work_overrides(board)
    validate_board(board)
    save_json(BOARD_PATH, board)
    save_json(
        APPROVED_PATH,
        build_slice(
            board,
            "approved",
            "Approved ingest set of dystopian AI quotes.",
        ),
    )
    save_json(
        CANDIDATES_PATH,
        build_slice(
            board,
            "candidate",
            "Active candidate queue for review decisions.",
        ),
    )
    save_json(
        POSTPONED_PATH,
        build_slice(
            board,
            "postponed",
            "Postponed quote records held for later review.",
        ),
    )
    save_json(
        DECLINED_PATH,
        build_slice(
            board,
            "declined",
            "Declined quote records kept for editorial history.",
        ),
    )
    build_review_board_markdown(board)
    build_site(board)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bootstrap-board",
        action="store_true",
        help="Create the canonical review board from the legacy candidates file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.bootstrap_board:
        bootstrap_board_from_candidates()
    build_all()


if __name__ == "__main__":
    main()
