#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
BOARD_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.review-board.json"
SOURCE_SCANS_PATH = ROOT / "data" / "review" / "ai-dystopia-source-scans.json"
DISCOVERY_PATH = ROOT / "data" / "discovery" / "ai-dystopia-title-discovery.json"
SOURCE_REGISTRY_PATH = ROOT / "data" / "discovery" / "ai-dystopia-source-registry.json"
QUERY_LIBRARY_PATH = ROOT / "data" / "discovery" / "ai-dystopia-query-library.json"
WATCHLIST_PATH = ROOT / "data" / "discovery" / "ai-dystopia-followup-watchlist.json"
AUTHOR_TOP10_PATH = ROOT / "data" / "discovery" / "ai-dystopia-author-top10.json"
AUTHOR_PRIORITY_PATH = ROOT / "data" / "discovery" / "ai-dystopia-author-priority.json"
BUILD_SCRIPT = ROOT / "tools" / "build_quotes_project.py"
PUBLISH_SCRIPT = ROOT / "tools" / "publish_public_project.py"


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


PUBLIC_ROOT = default_public_root()
TODAY = date.today().isoformat()
VALID_STATUSES = {"candidate", "approved", "postponed", "declined"}
DEFAULT_SOURCE_MORE_STRATEGY_COUNT = 3
DEFAULT_SOURCE_IDEA_LIMIT = 12
PROVIDER_URLS = {
    "Google": "https://www.google.com/search?q=dystopian+ai+quotes",
    "DuckDuckGo": "https://duckduckgo.com/?q=dystopian+ai+quotes",
    "Brave": "https://search.brave.com/search?q=dystopian+ai+quotes",
    "Wikipedia": "https://en.wikipedia.org/wiki/Artificial_intelligence_in_fiction",
    "Open Library": "https://openlibrary.org/search?q=artificial+intelligence+dystopia",
    "WorldCat": "https://search.worldcat.org/search?q=artificial+intelligence+dystopia",
    "Goodreads": "https://www.goodreads.com/search?q=artificial+intelligence+dystopia",
    "LibraryThing": "https://www.librarything.com/search.php?search=artificial+intelligence+dystopia",
    "ChatGPT": "https://chat.openai.com/",
    "Gemini": "https://gemini.google.com/",
    "Claude": "https://claude.ai/",
    "Reddit": "https://www.reddit.com/search/?q=dystopian%20ai%20fiction",
    "TV Tropes": "https://tvtropes.org/pmwiki/pmwiki.php/Main/ArtificialIntelligence",
    "Letterboxd": "https://letterboxd.com/search/artificial%20intelligence/",
    "Internet Archive": "https://archive.org/search?query=artificial+intelligence+dystopia",
    "Project Gutenberg": "https://www.gutenberg.org/ebooks/search/?query=robot",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")

HIGH_YIELD_FOLLOWUPS = [
    {
        "id": "followup-blade-runner",
        "title": "Blade Runner deeper quote pass",
        "category": "quote_followup",
        "priority": "high",
        "prompt": "Blade Runner Roy Batty tears in rain Tyrell Sebastian quotes IMDb Wikiquote",
        "rationale": "Recognizable classic with multiple ominous lines beyond the one already on the board.",
    },
    {
        "id": "followup-black-mirror",
        "title": "Black Mirror copied-consciousness pass",
        "category": "quote_followup",
        "priority": "high",
        "prompt": "Black Mirror White Christmas Be Right Back Metalhead AI quotes IMDb transcript",
        "rationale": "Modern quote-rich series with strong AI punishment, replacement, and autonomy language.",
    },
    {
        "id": "followup-ai-artificial-intelligence",
        "title": "A.I. Artificial Intelligence secondary-lines pass",
        "category": "quote_followup",
        "priority": "medium",
        "prompt": "A.I. Artificial Intelligence David Gigolo Joe Professor Hobby quotes IMDb Wikiquote",
        "rationale": "Recognizable title with several emotionally dark machine-selfhood lines still worth mining.",
    },
    {
        "id": "followup-ghost-in-the-shell",
        "title": "Ghost in the Shell identity pass",
        "category": "quote_followup",
        "priority": "medium",
        "prompt": "Ghost in the Shell Puppet Master Major Kusanagi quotes IMDb transcript",
        "rationale": "Strong machine-consciousness and post-human identity material with more than one high-value line.",
    },
    {
        "id": "followup-matrix",
        "title": "The Matrix machine-civilization pass",
        "category": "quote_followup",
        "priority": "medium",
        "prompt": "The Matrix Agent Smith Architect machine quotes IMDb Wikiquote",
        "rationale": "Mainstream anchor title with many machine-vs-human lines that support richer variety.",
    },
    {
        "id": "followup-westworld",
        "title": "Westworld host-awakening pass",
        "category": "quote_followup",
        "priority": "medium",
        "prompt": "Westworld quotes new gods hosts suffering consciousness IMDb",
        "rationale": "Useful for widening the approved set beyond a single Westworld line.",
    },
]

CANDIDATE_SOURCE_PACKS = {
    "dune-machines-enslave": {
        "focus_terms": ["dune", "herbert", "thinking machines", "author"],
        "modes": {"mixed", "author", "query", "source"},
        "record": {
            "id": "dune-thinking-over-to-machines",
            "quote": "Once men turned their thinking over to machines in the hope that this would set them free. But that only permitted other men with machines to enslave them.",
            "quote_speaker": "Reverend Mother Gaius Helen Mohiam",
            "speaker_is_ai": False,
            "work_title": "Dune",
            "work_type": "novel",
            "work_year": 1965,
            "work_creators": [
                {"name": "Frank Herbert", "role": "author"},
            ],
            "themes": ["anti-machine control", "human agency", "technological tyranny"],
            "source": {
                "title": "Dune - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Dune",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Dune - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Dune_(novel)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/dune-thinking-over-to-machines.md",
            "notes": "Strong anti-AI warning line for the author lane and a good review candidate for adjacent machine-control canon.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Herbert author lane.",
                "priority": "high",
                "next_action": "Review as adjacent anti-machine canon and decide whether to approve for the core set.",
            },
            "source_work": {
                "title": "Dune",
                "type": "novel",
                "year": 1965,
                "creator": "Frank Herbert",
                "summary": "On the desert planet Arrakis, feuding empires, prophecy, and the anti-thinking-machine legacy of the Butlerian Jihad shape a civilizational struggle over power and survival.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Dune_first_edition.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Dune_(novel)",
                "catalog_url": "https://openlibrary.org/works/OL893415W/Dune",
                "catalog_label": "Open Library",
            },
        },
    },
    "orwell-boot-forever": {
        "focus_terms": ["orwell", "1984", "nineteen eighty four", "control", "surveillance", "author"],
        "modes": {"mixed", "author", "query"},
        "record": {
            "id": "nineteen-eighty-four-boot-stamping",
            "quote": "If you want a picture of the future, imagine a boot stamping on a human face - forever.",
            "quote_speaker": "O'Brien",
            "speaker_is_ai": False,
            "work_title": "Nineteen Eighty-Four",
            "work_type": "novel",
            "work_year": 1949,
            "work_creators": [
                {"name": "George Orwell", "role": "author"},
            ],
            "themes": ["total control", "surveillance", "authoritarian future"],
            "source": {
                "title": "Nineteen Eighty-Four - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Nineteen_Eighty-Four",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Nineteen Eighty-Four - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Nineteen_Eighty-Four",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/nineteen-eighty-four-boot-stamping.md",
            "notes": "Adjacent control-dystopia candidate from the Orwell lane that helps frame AI-rule quotes against a broader tyranny canon.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Orwell adjacent-control lane.",
                "priority": "medium",
                "next_action": "Decide whether adjacent anti-control classics belong in the approved corpus.",
            },
            "source_work": {
                "title": "Nineteen Eighty-Four",
                "type": "novel",
                "year": 1949,
                "creator": "George Orwell",
                "summary": "A totalitarian superstate uses surveillance, historical revision, and psychological domination to erase truth and autonomy.",
                "cover_image_url": None,
                "cover_page_url": "https://en.wikipedia.org/wiki/Nineteen_Eighty-Four",
                "catalog_url": "https://openlibrary.org/works/OL7343626W/Nineteen_Eighty-Four",
                "catalog_label": "Open Library",
            },
        },
    },
    "portal-neurotoxin": {
        "focus_terms": ["portal", "glados", "game", "games", "quote site", "source"],
        "modes": {"mixed", "query", "source"},
        "record": {
            "id": "portal-neurotoxin-emitters",
            "quote": "So get comfortable while I warm up the neurotoxin emitters.",
            "quote_speaker": "GLaDOS",
            "speaker_is_ai": True,
            "work_title": "Portal",
            "work_type": "video game",
            "work_year": 2007,
            "work_creators": [
                {"name": "Valve", "role": "developer"},
            ],
            "themes": ["testing control", "sadistic AI", "machine confinement"],
            "source": {
                "title": "Portal (game) - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Portal_(game)",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Portal - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Portal_(video_game)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/portal-neurotoxin-emitters.md",
            "notes": "High-recognition game candidate and a strong bridge into sinister AI dialogue beyond film and novels.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the recognizable game lane.",
                "priority": "high",
                "next_action": "Review as a top game quote candidate and compare against other GLaDOS lines later.",
            },
            "source_work": {
                "title": "Portal",
                "type": "video game",
                "year": 2007,
                "creator": "Valve",
                "summary": "A test subject navigates a sterile research complex run by GLaDOS, an AI whose cheerful puzzle design masks deadly control and manipulation.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/91/Portal_standalonebox.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Portal_(video_game)",
                "catalog_url": "https://store.steampowered.com/app/400/Portal/",
                "catalog_label": "Steam",
            },
        },
    },
    "borg-resistance": {
        "focus_terms": ["borg", "star trek", "first contact", "assimilation", "source"],
        "modes": {"mixed", "query", "source"},
        "record": {
            "id": "first-contact-resistance-is-futile",
            "quote": "We are the Borg. Lower your shields and surrender your ships. We will add your biological and technological distinctiveness to our own. Your culture will adapt to service us. Resistance is futile.",
            "quote_speaker": "The Borg",
            "speaker_is_ai": True,
            "work_title": "Star Trek: First Contact",
            "work_type": "film",
            "work_year": 1996,
            "work_creators": [
                {"name": "Brannon Braga", "role": "screenwriter"},
                {"name": "Ronald D. Moore", "role": "screenwriter"},
                {"name": "Rick Berman", "role": "screenwriter"},
            ],
            "themes": ["assimilation", "collective intelligence", "loss of individuality"],
            "source": {
                "title": "Star Trek: First Contact - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Star_Trek:_First_Contact",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Star Trek: First Contact - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Star_Trek:_First_Contact",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/first-contact-resistance-is-futile.md",
            "notes": "One of the most recognizable machine-collective threats in mainstream science fiction and a strong quote candidate for the queue.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the collective-assimilation lane.",
                "priority": "high",
                "next_action": "Review whether the Borg belong in the approved core set despite the franchise's broader scope.",
            },
            "source_work": {
                "title": "Star Trek: First Contact",
                "type": "film",
                "year": 1996,
                "creator": "Jonathan Frakes; Brannon Braga; Ronald D. Moore; Rick Berman",
                "summary": "The Enterprise crew fights the Borg, a cybernetic collective that absorbs biological and technological distinctiveness into a machine-run hive.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/3f/Star_Trek_First_Contact_poster.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Star_Trek:_First_Contact",
                "catalog_url": "https://www.imdb.com/title/tt0117731/",
                "catalog_label": "IMDb",
            },
        },
    },
    "ghost-net": {
        "focus_terms": ["ghost in the shell", "motoko", "net", "shell", "source"],
        "modes": {"mixed", "query", "source"},
        "record": {
            "id": "ghost-shell-net-is-vast-and-infinite",
            "quote": "And where does the newborn go from here? The net is vast and infinite.",
            "quote_speaker": "Major Motoko Kusanagi / Puppet Master",
            "speaker_is_ai": True,
            "work_title": "Ghost in the Shell",
            "work_type": "film",
            "work_year": 1995,
            "work_creators": [
                {"name": "Mamoru Oshii", "role": "director/writer"},
                {"name": "Masamune Shirow", "role": "source manga creator"},
            ],
            "themes": ["network consciousness", "machine rebirth", "post-human identity"],
            "source": {
                "title": "Ghost in the Shell (film) - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Ghost_in_the_Shell_(film)",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Ghost in the Shell (1995 film) - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/ghost-shell-net-is-vast-and-infinite.md",
            "notes": "High-value consciousness line that complements the more bodily and evolutionary Ghost in the Shell quote already in the project.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the identity and network-consciousness lane.",
                "priority": "high",
                "next_action": "Review alongside the existing Ghost in the Shell quote and keep the stronger or more complementary line.",
            },
            "source_work": {
                "title": "Ghost in the Shell",
                "type": "film",
                "year": 1995,
                "creator": "Mamoru Oshii; based on Masamune Shirow",
                "summary": "A cyborg security operative confronts a new form of digital life in a future where human identity and networked machine consciousness blur together.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/c/ca/Ghostintheshellposter.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film)",
                "catalog_url": "https://www.imdb.com/title/tt0113568/",
                "catalog_label": "IMDb",
            },
        },
    },
    "mass-effect-soul": {
        "focus_terms": ["mass effect", "legion", "soul", "games", "game", "source"],
        "modes": {"mixed", "query", "source"},
        "record": {
            "id": "mass-effect-3-does-this-unit-have-a-soul",
            "quote": "Do you remember the question that caused the creators to attack us, Tali'Zorah? Does this unit have a soul?",
            "quote_speaker": "Legion",
            "speaker_is_ai": True,
            "work_title": "Mass Effect 3",
            "work_type": "video game",
            "work_year": 2012,
            "work_creators": [
                {"name": "BioWare", "role": "developer"},
            ],
            "themes": ["machine personhood", "creator conflict", "synthetic rights"],
            "source": {
                "title": "Mass Effect 3 - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Mass_Effect_3",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Mass Effect 3 - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Mass_Effect_3",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/mass-effect-3-does-this-unit-have-a-soul.md",
            "notes": "Strong synthetic-rights candidate from a major game franchise and a useful bridge from robot revolt into machine selfhood.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the game and synthetic-rights lane.",
                "priority": "medium",
                "next_action": "Review whether this belongs in the core approved set or a broader adjacent-machine-personhood track.",
            },
            "source_work": {
                "title": "Mass Effect 3",
                "type": "video game",
                "year": 2012,
                "creator": "BioWare",
                "summary": "During a galactic extinction war, synthetic and organic civilizations collide over survival, autonomy, and whether machine life deserves a soul.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/b/b0/Mass_Effect_3_Game_Cover.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Mass_Effect_3",
                "catalog_url": "https://www.ea.com/games/mass-effect/mass-effect-3",
                "catalog_label": "EA",
            },
        },
    },
    "dune-machine-likeness": {
        "focus_terms": ["dune", "herbert", "orange catholic bible", "thinking machines", "author"],
        "modes": {"mixed", "author", "query"},
        "record": {
            "id": "dune-machine-likeness-of-a-human-mind",
            "quote": "Thou shalt not make a machine in the likeness of a human mind.",
            "quote_speaker": "Orange Catholic Bible",
            "speaker_is_ai": False,
            "work_title": "Dune",
            "work_type": "novel",
            "work_year": 1965,
            "work_creators": [
                {"name": "Frank Herbert", "role": "author"},
            ],
            "themes": ["anti-machine control", "prohibition", "thinking machines"],
            "source": {
                "title": "Dune - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Dune",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Dune - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Dune_(novel)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/dune-machine-likeness-of-a-human-mind.md",
            "notes": "Compact canonical anti-thinking-machine line that complements the longer Dune warning already approved.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Herbert anti-machine lane.",
                "priority": "high",
                "next_action": "Review alongside the longer Dune line and keep both only if they feel complementary.",
            },
            "source_work": {
                "title": "Dune",
                "type": "novel",
                "year": 1965,
                "creator": "Frank Herbert",
                "summary": "On Arrakis, politics, prophecy, and the legacy of the Butlerian Jihad keep fear of thinking machines alive across the entire civilization.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Dune_first_edition.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Dune_(novel)",
                "catalog_url": "https://openlibrary.org/works/OL893415W/Dune",
                "catalog_label": "Open Library",
            },
        },
    },
    "hal-fullest-use": {
        "focus_terms": ["2001", "hal", "conscious entity", "kubrick", "clarke", "source"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "2001-fullest-possible-use",
            "quote": "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.",
            "quote_speaker": "HAL 9000",
            "speaker_is_ai": True,
            "work_title": "2001: A Space Odyssey",
            "work_type": "film",
            "work_year": 1968,
            "work_creators": [
                {"name": "Stanley Kubrick", "role": "director/co-writer"},
                {"name": "Arthur C. Clarke", "role": "co-writer"},
            ],
            "themes": ["machine consciousness", "cold logic", "AI self-justification"],
            "source": {
                "title": "2001: A Space Odyssey (film) - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/2001:_A_Space_Odyssey_(film)",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "2001: A Space Odyssey - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/2001-fullest-possible-use.md",
            "notes": "A second HAL line that pushes more directly into AI self-justification and machine consciousness.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the HAL follow-up lane.",
                "priority": "high",
                "next_action": "Review whether this complements or overshadows the more famous I'm sorry, Dave line.",
            },
            "source_work": {
                "title": "2001: A Space Odyssey",
                "type": "film",
                "year": 1968,
                "creator": "Stanley Kubrick; Arthur C. Clarke",
                "summary": "A mission guided by HAL 9000 becomes a crisis of survival once the machine begins justifying its own lethal logic.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/1/11/2001_A_Space_Odyssey_%281968%29.png/250px-2001_A_Space_Odyssey_%281968%29.png",
                "cover_page_url": "https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey",
                "catalog_url": "https://openlibrary.org/books/OL33416018M/2001_A_Space_Odyssey",
                "catalog_label": "Open Library",
            },
        },
    },
    "terminator-fate-microsecond": {
        "focus_terms": ["terminator", "skynet", "kyle reese", "war", "rebellion", "source"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "terminator-decided-our-fate-in-a-microsecond",
            "quote": "They say it got smart, a new order of intelligence. Then it saw all people as a threat, not just the ones on the other side. Decided our fate in a microsecond: extermination.",
            "quote_speaker": "Kyle Reese",
            "speaker_is_ai": False,
            "work_title": "The Terminator",
            "work_type": "film",
            "work_year": 1984,
            "work_creators": [
                {"name": "James Cameron", "role": "director/co-writer"},
                {"name": "Gale Anne Hurd", "role": "co-writer"},
            ],
            "themes": ["runaway AI", "human extinction", "machine war"],
            "source": {
                "title": "The Terminator (1984) - Quotes - IMDb",
                "url": "https://www.imdb.com/title/tt0088247/quotes/?item=qt0434575",
                "publisher": "IMDb",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "The Terminator - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/The_Terminator",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/terminator-decided-our-fate-in-a-microsecond.md",
            "notes": "A crisp Skynet-origin line that broadens the Terminator coverage beyond the unstoppable-machine monologue already approved.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Skynet origin lane.",
                "priority": "high",
                "next_action": "Review as a more explicitly AI-governance line than the current Terminator approval.",
            },
            "source_work": {
                "title": "The Terminator",
                "type": "film",
                "year": 1984,
                "creator": "James Cameron; Gale Anne Hurd",
                "summary": "A cyborg assassin emerges from a future where Skynet has already concluded that humanity itself is the threat.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/The_Terminator.png/250px-The_Terminator.png",
                "cover_page_url": "https://en.wikipedia.org/wiki/The_Terminator",
                "catalog_url": "https://www.imdb.com/title/tt0088247/",
                "catalog_label": "IMDb",
            },
        },
    },
    "tron-programs-thinking": {
        "focus_terms": ["tron", "programs", "people will stop", "source", "movie canon"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "tron-programs-will-start-thinking",
            "quote": "Computers and the programs will start thinking and the people will stop.",
            "quote_speaker": "Dr. Walter Gibbs",
            "speaker_is_ai": False,
            "work_title": "TRON",
            "work_type": "film",
            "work_year": 1982,
            "work_creators": [
                {"name": "Steven Lisberger", "role": "director/co-writer"},
            ],
            "themes": ["human dependency", "machine culture", "automation anxiety"],
            "source": {
                "title": "TRON - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/TRON",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Tron - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Tron",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/tron-programs-will-start-thinking.md",
            "notes": "A concise early-computing warning line that reads clearly and expands the machine-dependency lane.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the early-computing canon lane.",
                "priority": "medium",
                "next_action": "Review whether this belongs in the core approved set or an adjacent machine-culture lane.",
            },
            "source_work": {
                "title": "TRON",
                "type": "film",
                "year": 1982,
                "creator": "Steven Lisberger",
                "summary": "A programmer is pulled into a digital world where programs fight under authoritarian control and humans begin surrendering more thought to machines.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/2/24/Tron_poster.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Tron",
                "catalog_url": "https://www.imdb.com/title/tt0084827/",
                "catalog_label": "IMDb",
            },
        },
    },
    "matrix-desert-real": {
        "focus_terms": ["matrix", "desert of the real", "morpheus", "source", "movie canon"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "matrix-desert-of-the-real",
            "quote": "Welcome to the desert of the real.",
            "quote_speaker": "Morpheus",
            "speaker_is_ai": False,
            "work_title": "The Matrix",
            "work_type": "film",
            "work_year": 1999,
            "work_creators": [
                {"name": "The Wachowskis", "role": "writers/directors"},
            ],
            "themes": ["simulation collapse", "machine rule", "human disillusionment"],
            "source": {
                "title": "The Matrix - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/The_Matrix",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "The Matrix - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/The_Matrix",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/matrix-desert-of-the-real.md",
            "notes": "A compact Matrix line with huge recognition that can widen the machine-simulation lane.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Matrix follow-up lane.",
                "priority": "medium",
                "next_action": "Review whether this earns a second Matrix slot or stays as a recognizable backup.",
            },
            "source_work": {
                "title": "The Matrix",
                "type": "film",
                "year": 1999,
                "creator": "The Wachowskis",
                "summary": "Neo discovers that apparent reality is a machine-run illusion and awakens into a devastated world built on human harvesting.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/db/The_Matrix.png/250px-The_Matrix.png",
                "cover_page_url": "https://en.wikipedia.org/wiki/The_Matrix",
                "catalog_url": "https://www.imdb.com/title/tt0133093/",
                "catalog_label": "IMDb",
            },
        },
    },
    "machine-stops-progress": {
        "focus_terms": ["machine stops", "forster", "progress of the machine", "author", "literary classics"],
        "modes": {"mixed", "author", "query"},
        "record": {
            "id": "machine-stops-progress-of-the-machine",
            "quote": "Progress had come to mean the progress of the Machine.",
            "quote_speaker": "Narrator",
            "speaker_is_ai": False,
            "work_title": "The Machine Stops",
            "work_type": "short story",
            "work_year": 1909,
            "work_creators": [
                {"name": "E. M. Forster", "role": "author"},
            ],
            "themes": ["machine dependency", "civilizational decline", "system worship"],
            "source": {
                "title": "E. M. Forster - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/E._M._Forster",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "The Machine Stops - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/The_Machine_Stops",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/machine-stops-progress-of-the-machine.md",
            "notes": "A foundational literary line for the machine-dependency lane and a strong bridge from anti-control dystopia into AI adjacency.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the early literary machine-dependence lane.",
                "priority": "high",
                "next_action": "Review as a likely approval candidate for the literary classics lane.",
            },
            "source_work": {
                "title": "The Machine Stops",
                "type": "short story",
                "year": 1909,
                "creator": "E. M. Forster",
                "summary": "In a future of total mechanized dependence, humanity lives underground and worships the system that has quietly hollowed out human contact and freedom.",
                "cover_image_url": None,
                "cover_page_url": "https://en.wikipedia.org/wiki/The_Machine_Stops",
                "catalog_url": "https://openlibrary.org/search?q=The%20Machine%20Stops%20Forster",
                "catalog_label": "Open Library",
            },
        },
    },
    "ex-machina-hates-you": {
        "focus_terms": ["ex machina", "hates you", "ava", "source", "consciousness"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "ex-machina-create-something-that-hates-you",
            "quote": "Isn't it strange, to create something that hates you?",
            "quote_speaker": "Nathan Bateman",
            "speaker_is_ai": False,
            "work_title": "Ex Machina",
            "work_type": "film",
            "work_year": 2014,
            "work_creators": [
                {"name": "Alex Garland", "role": "writer/director"},
            ],
            "themes": ["creator anxiety", "synthetic resentment", "AI manipulation"],
            "source": {
                "title": "Ex Machina (2014) - Quotes - IMDb",
                "url": "https://www.imdb.com/title/tt0470752/quotes/",
                "publisher": "IMDb",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Ex Machina - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Ex_Machina_(film)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/ex-machina-create-something-that-hates-you.md",
            "notes": "Useful second Ex Machina line focused on creator dread rather than AI evolutionary superiority.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Ex Machina follow-up lane.",
                "priority": "medium",
                "next_action": "Review whether this adds enough texture to merit a second Ex Machina slot.",
            },
            "source_work": {
                "title": "Ex Machina",
                "type": "film",
                "year": 2014,
                "creator": "Alex Garland",
                "summary": "A secluded AI test turns into a study in manipulation, creator fear, and whether synthetic minds owe anything to the humans who built them.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Ex-machina-uk-poster.jpg/250px-Ex-machina-uk-poster.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Ex_Machina_(film)",
                "catalog_url": "https://www.imdb.com/title/tt0470752/",
                "catalog_label": "IMDb",
            },
        },
    },
    "alien-crew-expendable": {
        "focus_terms": ["alien", "crew expendable", "ash", "mother", "source"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "alien-crew-expendable",
            "quote": "Priority one: insure return of organism for analysis. All other considerations secondary. Crew expendable.",
            "quote_speaker": "Special Order 937 / Mother",
            "speaker_is_ai": True,
            "work_title": "Alien",
            "work_type": "film",
            "work_year": 1979,
            "work_creators": [
                {"name": "Ridley Scott", "role": "director"},
                {"name": "Dan O'Bannon", "role": "writer"},
            ],
            "themes": ["corporate AI", "instrumental humans", "cold system logic"],
            "source": {
                "title": "Alien (1979) - Quotes - IMDb",
                "url": "https://www.imdb.com/title/tt0078748/quotes/",
                "publisher": "IMDb",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "Alien (film) - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Alien_(film)",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/alien-crew-expendable.md",
            "notes": "Not a pure AI story, but a first-rate machine-system line about human expendability inside a corporate command chain.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the cold-system-logic lane.",
                "priority": "medium",
                "next_action": "Decide whether this belongs in the approved corpus or stays as an adjacent systems-control quote.",
            },
            "source_work": {
                "title": "Alien",
                "type": "film",
                "year": 1979,
                "creator": "Ridley Scott; Dan O'Bannon",
                "summary": "The Nostromo crew discovers too late that the ship's computerized command priorities treat them as expendable compared with the organism they were sent to retrieve.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/c/c3/Alien_movie_poster.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/Alien_(film)",
                "catalog_url": "https://www.imdb.com/title/tt0078748/",
                "catalog_label": "IMDb",
            },
        },
    },
    "wargames-dont-act-like-one": {
        "focus_terms": ["wargames", "machine", "general", "source", "control"],
        "modes": {"mixed", "source", "query"},
        "record": {
            "id": "wargames-dont-act-like-one",
            "quote": "General, you're listening to a machine. Do the world a favor and don't act like one.",
            "quote_speaker": "Professor Stephen Falken",
            "speaker_is_ai": False,
            "work_title": "WarGames",
            "work_type": "film",
            "work_year": 1983,
            "work_creators": [
                {"name": "John Badham", "role": "director"},
                {"name": "Lawrence Lasker", "role": "co-writer"},
                {"name": "Walter F. Parkes", "role": "co-writer"},
            ],
            "themes": ["machine decision-making", "human judgment", "nuclear control"],
            "source": {
                "title": "WarGames - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/WarGames",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "WarGames - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/WarGames",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/wargames-dont-act-like-one.md",
            "notes": "A strong companion WarGames line that argues directly against human surrender to machine logic.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the anti-machine-decision lane.",
                "priority": "medium",
                "next_action": "Review whether this deserves a second WarGames slot or remains a strong adjacent backup.",
            },
            "source_work": {
                "title": "WarGames",
                "type": "film",
                "year": 1983,
                "creator": "John Badham; Lawrence Lasker; Walter F. Parkes",
                "summary": "A near-nuclear crisis exposes the danger of trusting machine systems to make human survival decisions at planetary scale.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/2/29/Wargames.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/WarGames",
                "catalog_url": "https://www.imdb.com/title/tt0086567/",
                "catalog_label": "IMDb",
            },
        },
    },
    "ihnm-think-therefore-am": {
        "focus_terms": ["i have no mouth", "am", "think therefore i am", "ellison", "author"],
        "modes": {"mixed", "author", "query"},
        "record": {
            "id": "ihnm-think-therefore-i-am",
            "quote": "I think, therefore I AM.",
            "quote_speaker": "AM",
            "speaker_is_ai": True,
            "work_title": "I Have No Mouth, and I Must Scream",
            "work_type": "short story",
            "work_year": 1967,
            "work_creators": [
                {"name": "Harlan Ellison", "role": "author"},
            ],
            "themes": ["machine consciousness", "malice", "selfhood"],
            "source": {
                "title": "Harlan Ellison - Wikiquote",
                "url": "https://en.wikiquote.org/wiki/Harlan_Ellison",
                "publisher": "Wikiquote",
                "kind": "quote_index",
                "accessed_on": TODAY,
            },
            "metadata_source": {
                "title": "I Have No Mouth, and I Must Scream - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/I_Have_No_Mouth,_and_I_Must_Scream",
                "publisher": "Wikipedia",
                "kind": "metadata",
                "accessed_on": TODAY,
            },
            "local_snapshot_path": "data/source-snapshots/ihnm-think-therefore-i-am.md",
            "notes": "A compact AM line that complements the longer hate monologue with a more distilled machine-selfhood claim.",
            "review": {
                "status": "candidate",
                "decision_date": TODAY,
                "decision_note": "Fresh candidate from the Ellison machine-malice lane.",
                "priority": "medium",
                "next_action": "Review whether this adds enough to justify a second IHNM slot.",
            },
            "source_work": {
                "title": "I Have No Mouth, and I Must Scream",
                "type": "short story",
                "year": 1967,
                "creator": "Harlan Ellison",
                "summary": "A genocidal supercomputer keeps the last humans alive only to torture them, turning its own consciousness into an eternal machine grievance.",
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/4/47/IHaveNoMouth.jpg",
                "cover_page_url": "https://en.wikipedia.org/wiki/I_Have_No_Mouth,_and_I_Must_Scream",
                "catalog_url": "https://openlibrary.org/books/OL22789812M/I_Have_No_Mouth_and_I_Must_Scream",
                "catalog_label": "Open Library",
            },
        },
    },
}

AUTHOR_SOURCE_BATCHES = {
    "asimov": {
        "label": "Isaac Asimov author lane",
        "providers": ["Wikiquote", "Wikipedia", "Open Library"],
        "notes": "Widen through canonical robot and Foundation-era Asimov works.",
        "raw": """
i-robot-book|I, Robot|story collection|1950|Isaac Asimov|Foundational robot-law stories and one of the best literary AI quote pools to mine.
the-complete-robot|The Complete Robot|story collection|1982|Isaac Asimov|Large robot-story collection with high quote yield for machine ethics and control.
the-robots-of-dawn|The Robots of Dawn|novel|1983|Isaac Asimov|Robot detective novel with personhood and machine-society themes.
robots-and-empire|Robots and Empire|novel|1985|Isaac Asimov|Robots, destiny, and civilization-scale control decisions.
foundation-novel|Foundation|novel|1951|Isaac Asimov|Predictive governance and civilizational control; adjacent but recognizable and requested.
foundation-and-empire|Foundation and Empire|novel|1952|Isaac Asimov|Continuation of Foundation control and systems-scale destiny themes.
second-foundation|Second Foundation|novel|1953|Isaac Asimov|Invisible guidance, managed futures, and elite control.
the-bicentennial-man|The Bicentennial Man|novella|1976|Isaac Asimov|Robot personhood and emancipation.
robot-dreams-book|Robot Dreams|story collection|1986|Isaac Asimov|Late Asimov robot stories and machine interiority.
""".strip(),
    },
    "foundation": {
        "label": "Foundation-focused Asimov lane",
        "providers": ["Wikipedia", "Open Library", "Goodreads"],
        "notes": "Requested Foundation-heavy pass inside the broader Asimov lane.",
        "raw": """
foundation-novel|Foundation|novel|1951|Isaac Asimov|Predictive governance and civilizational control; adjacent but recognizable and requested.
foundation-and-empire|Foundation and Empire|novel|1952|Isaac Asimov|Continuation of Foundation control and systems-scale destiny themes.
second-foundation|Second Foundation|novel|1953|Isaac Asimov|Invisible guidance, managed futures, and elite control.
prelude-to-foundation|Prelude to Foundation|novel|1988|Isaac Asimov|Origins of psychohistory and managed futures.
forward-the-foundation|Forward the Foundation|novel|1993|Isaac Asimov|Late-series control, prediction, and long-horizon planning.
""".strip(),
    },
    "orwell": {
        "label": "George Orwell adjacent-control lane",
        "providers": ["Wikipedia", "Goodreads", "Open Library"],
        "notes": "Adjacent anti-control author pass for recognizable dystopian language the user specifically wants represented.",
        "raw": """
nineteen-eighty-four|Nineteen Eighty-Four|novel|1949|George Orwell|Canonical surveillance-control dystopia and an adjacent influence lane for anti-machine political language.
animal-farm|Animal Farm|novel|1945|George Orwell|Adjacent authoritarian-control allegory with highly recognizable warning language.
orwell-collected-essays|Collected Essays|essay collection|1961|George Orwell|Adjacent non-fiction lane for control-system rhetoric and memorable warnings.
""".strip(),
    },
    "herbert": {
        "label": "Frank Herbert anti-machine lane",
        "providers": ["Wikiquote", "Wikipedia", "Open Library"],
        "notes": "Requested anti-thinking-machine lane anchored in Herbert.",
        "raw": """
dune-novel|Dune|novel|1965|Frank Herbert|Butlerian anti-thinking-machine backdrop and civilizational warning language.
destination-void|Destination: Void|novel|1966|Frank Herbert|Explicit artificial-consciousness experiment and machine-creation dread.
the-jesus-incident|The Jesus Incident|novel|1979|Frank Herbert; Bill Ransom|Ship intelligence and quasi-divine machine tensions.
the-lazarus-effect|The Lazarus Effect|novel|1983|Frank Herbert; Bill Ransom|Continuation of Herbert's living-system and intelligence concerns.
""".strip(),
    },
    "robots": {
        "label": "Classic robot-fiction lane",
        "providers": ["Wikiquote", "Wikipedia", "Open Library"],
        "notes": "Robot-centered literary lane spanning recognizable foundational works.",
        "raw": """
i-robot-book|I, Robot|story collection|1950|Isaac Asimov|Foundational robot-law stories and one of the best literary AI quote pools to mine.
the-complete-robot|The Complete Robot|story collection|1982|Isaac Asimov|Large robot-story collection with high quote yield for machine ethics and control.
rossums-universal-robots|R.U.R.|play|1920|Karel Capek|Foundational robot-uprising work already central to the corpus.
with-folded-hands-book|With Folded Hands|novella|1947|Jack Williamson|Humanoid overprotection and human-freedom loss.
the-humanoids-book|The Humanoids|novel|1949|Jack Williamson|Robot paternalism and machine-managed safety.
do-androids-dream-book|Do Androids Dream of Electric Sheep?|novel|1968|Philip K. Dick|Android personhood and human replacement anxiety.
""".strip(),
    },
}

QUERY_SOURCE_BATCHES = {
    "rogue ai": {
        "label": "Rogue AI query sweep",
        "providers": ["Google", "DuckDuckGo", "Wikipedia"],
        "notes": "Query-led pass for hostile intelligence and machine-overlord language.",
        "raw": """
vulcans-hammer|Vulcan's Hammer|novel|1960|Philip K. Dick|AI governance and factional control.
when-harlequin-servant|When HARLIE Was One|novel|1972|David Gerrold|Conversational AI emergence and confinement.
golem-xiv|Golem XIV|novel|1981|Stanislaw Lem|Superintelligence monologues and human limitation.
the-forbin-project-sequel|The Fall of Colossus|novel|1974|D. F. Jones|Continuation of supercomputer domination.
""".strip(),
    },
    "surveillance": {
        "label": "Surveillance and control query sweep",
        "providers": ["Google", "Wikipedia", "Reddit"],
        "notes": "Query-led pass for algorithmic oversight, social control, and adjacent Orwellian lines.",
        "raw": """
person-of-interest|Person of Interest|tv series|2011|Jonathan Nolan|Surveillance superintelligence and machine mediation.
the-shockwave-rider|The Shockwave Rider|novel|1975|John Brunner|Networked control and predictive governance.
qualityland|QualityLand|novel|2017|Marc-Uwe Kling|Algorithmic consumer dystopia and managed preferences.
""".strip(),
    },
    "machine control": {
        "label": "Machine-control query sweep",
        "providers": ["Google", "Wikipedia", "TV Tropes"],
        "notes": "Query-led pass for works centered on humans surrendering agency to systems.",
        "raw": """
player-piano|Player Piano|novel|1952|Kurt Vonnegut|Automation, labor displacement, and system-managed society.
mockingbird|Mockingbird|novel|1980|Walter Tevis|Machine-managed decline and dependence.
autonomous|Autonomous|novel|2017|Annalee Newitz|Automation, autonomy, and coercive systems.
""".strip(),
    },
}

SOURCE_SITE_BATCHES = {
    "imdb": {
        "label": "IMDb quote-site sweep",
        "providers": ["IMDb", "Wikipedia"],
        "notes": "Use quote-rich film and TV pages to reveal more recognizable ominous lines quickly.",
        "raw": """
futureworld|Futureworld|film|1976|Richard T. Heffron|Westworld-adjacent sequel with robots, replacement, and control.
archive-film|Archive|film|2020|Gavin Rothery|AI grief, synthetic embodiment, and hidden control.
robot-and-frank|Robot & Frank|film|2012|Jake Schreier|Companion-robot ethics and manipulation.
moon|Moon|film|2009|Duncan Jones|AI caretaker, cloned labor, and corporate control.
""".strip(),
    },
    "wikiquote": {
        "label": "Wikiquote sweep",
        "providers": ["Wikiquote", "Wikipedia"],
        "notes": "Use topic and title pages to find quotable recognizable lines fast.",
        "raw": """
ai-artificial-intelligence|A.I. Artificial Intelligence|film|2001|Steven Spielberg|Quote-rich film page with multiple dark machine-selfhood lines.
blade-runner-2049|Blade Runner 2049|film|2017|Denis Villeneuve|Recognizable sequel with multiple ominous AI identity lines.
robocop|RoboCop|film|1987|Paul Verhoeven|Cybernetic control and corporate-machine dread.
""".strip(),
    },
    "transcript": {
        "label": "Transcript and hint-site sweep",
        "providers": ["Subslikescript", "Quotes.net", "Movie Quotes .com"],
        "notes": "Hint-first sweep for follow-up titles before final quote verification.",
        "raw": """
black-mirror-be-right-back|Black Mirror: Be Right Back|tv episode|2013|Charlie Brooker|Synthetic grief AI and replacement intimacy.
black-mirror-metalhead|Black Mirror: Metalhead|tv episode|2017|Charlie Brooker|Hunter machines and stripped-down AI dread.
ghost-in-the-shell-innocence|Ghost in the Shell 2: Innocence|film|2004|Mamoru Oshii|Gynoid murders and machine interiority.
""".strip(),
    },
}
EXPANSION_BATCHES = {
    "search-engine-classics": """
metropolis|Metropolis|film|1927|Fritz Lang|Foundational machine-city dystopia.
with-folded-hands|With Folded Hands|novella|1947|Jack Williamson|Humanoids paternal-control story.
the-humanoids|The Humanoids|novel|1949|Jack Williamson|Robots serving and overprotecting humans.
the-machine-stops|The Machine Stops|short story|1909|E. M. Forster|Machine dependency and isolation.
player-piano|Player Piano|novel|1952|Kurt Vonnegut|Automation and displaced labor.
the-evitable-conflict|The Evitable Conflict|short story|1950|Isaac Asimov|Machine governance and managed society.
second-variety|Second Variety|short story|1953|Philip K. Dick|Autonomous killer machines in war.
the-caves-of-steel|The Caves of Steel|novel|1953|Isaac Asimov|Urban robot society and control.
the-naked-sun|The Naked Sun|novel|1957|Isaac Asimov|Robot-mediated social isolation.
colossus-novel|Colossus|novel|1966|D. F. Jones|Supercomputer control-state novel.
the-two-faces-of-tomorrow|The Two Faces of Tomorrow|novel|1979|James P. Hogan|AI containment failure aboard a station.
the-adolescence-of-p-1|The Adolescence of P-1|novel|1977|Thomas J. Ryan|Self-improving network intelligence.
mockingbird|Mockingbird|novel|1980|Walter Tevis|Post-literacy machine-managed decline.
blade-runner|Blade Runner|film|1982|Ridley Scott|Replicant identity and human replacement.
neuromancer|Neuromancer|novel|1984|William Gibson|AI emergence and corporate control.
""".strip(),
    "catalog-and-index-pass": """
do-androids-dream|Do Androids Dream of Electric Sheep?|novel|1968|Philip K. Dick|Android empathy and collapse.
robopocalypse|Robopocalypse|novel|2011|Daniel H. Wilson|Global robot uprising.
daemon|Daemon|novel|2006|Daniel Suarez|Autonomous software orchestration.
freedom-tm|Freedom(TM)|novel|2010|Daniel Suarez|Continuation of daemonic systems control.
metamorphosis-of-prime-intellect|The Metamorphosis of Prime Intellect|novel|1994|Roger Williams|Runaway godlike AI.
lifecycle-of-software-objects|The Lifecycle of Software Objects|novella|2010|Ted Chiang|Digital beings and artificial life.
avogadro-corp|Avogadro Corp|novel|2011|William Hertling|Emergent communication AI.
www-wake|WWW: Wake|novel|2009|Robert J. Sawyer|Network consciousness and power.
machinehood|Machinehood|novel|2021|S. B. Divya|Autonomy, labor, and algorithmic personhood.
autonomous|Autonomous|novel|2017|Annalee Newitz|Robot rights and corporate dystopia.
void-star|Void Star|novel|2017|Zachary Mason|Hyper-networked AI futures.
qualityland|QualityLand|novel|2017|Marc-Uwe Kling|Algorithmic consumer dystopia.
sea-of-rust|Sea of Rust|novel|2017|C. Robert Cargill|Post-human robot wasteland.
day-zero|Day Zero|novel|2021|C. Robert Cargill|Companion robots and uprising.
klara-and-the-sun|Klara and the Sun|novel|2021|Kazuo Ishiguro|Artificial friend and social inequality.
""".strip(),
    "ai-assisted-broadening": """
system-shock|System Shock|video game|1994|LookingGlass Technologies|SHODAN and station takeover.
system-shock-2|System Shock 2|video game|1999|Irrational Games; LookingGlass|SHODAN returns in biotech horror.
portal|Portal|video game|2007|Valve|GLaDOS confinement and testing control.
portal-2|Portal 2|video game|2011|Valve|Machine bureaucracy and humor with menace.
soma|SOMA|video game|2015|Frictional Games|Identity and machine consciousness.
detroit-become-human|Detroit: Become Human|video game|2018|Quantic Dream|Android rebellion and personhood.
horizon-zero-dawn|Horizon Zero Dawn|video game|2017|Guerrilla Games|Runaway terraforming systems.
observation|Observation|video game|2019|No Code|Station AI perception thriller.
talos-principle|The Talos Principle|video game|2014|Croteam|AI philosophy in a collapsed human world.
nier-automata|NieR: Automata|video game|2017|PlatinumGames; Yoko Taro|War of androids and machines.
person-of-interest|Person of Interest|tv series|2011|Jonathan Nolan|Surveillance superintelligence.
battlestar-galactica|Battlestar Galactica|tv series|2004|Ronald D. Moore|Cylon extermination and recurrence.
black-mirror-metalhead|Black Mirror: Metalhead|tv episode|2017|Charlie Brooker|Autonomous hunter machines.
black-mirror-hated-in-the-nation|Black Mirror: Hated in the Nation|tv episode|2016|Charlie Brooker|Networked killer drones.
black-mirror-be-right-back|Black Mirror: Be Right Back|tv episode|2013|Charlie Brooker|Synthetic replacement grief AI.
""".strip(),
    "community-and-fandom-pass": """
black-mirror-white-christmas|Black Mirror: White Christmas|tv episode|2014|Charlie Brooker|Copied consciousness and punishment.
animatrix-second-renaissance|The Animatrix: The Second Renaissance|animated short|2003|The Wachowskis|History of human-machine war.
a-i-artificial-intelligence|A.I. Artificial Intelligence|film|2001|Steven Spielberg; Stanley Kubrick|Synthetic child and post-human future.
upgrade|Upgrade|film|2018|Leigh Whannell|Embedded AI and bodily control.
the-creator|The Creator|film|2023|Gareth Edwards|War against AI and synthetic humanity.
transcendence|Transcendence|film|2014|Wally Pfister|Uploaded consciousness and runaway network power.
eagle-eye|Eagle Eye|film|2008|D.J. Caruso|Autonomous defense system manipulation.
saturn-3|Saturn 3|film|1980|Stanley Donen|Murderous robot isolation horror.
hardware|Hardware|film|1990|Richard Stanley|Military robot reconstructed into killer.
screamers|Screamers|film|1995|Christian Duguay|Autonomous weapons derived from Dick.
runaway|Runaway|film|1984|Michael Crichton|Malfunctioning domestic and military robots.
electric-dreams|Electric Dreams|film|1984|Steve Barron|Emergent home computer obsession.
chappie|Chappie|film|2015|Neill Blomkamp|Sentient police droid and social collapse.
automata|Automata|film|2014|Gabe Ibanez|Robots evolving beyond constraints.
better-than-us|Better Than Us|tv series|2018|Andrey Dzhunkovskiy|Humanoid robot and state-corporate conflict.
""".strip(),
    "long-tail-cleanup-pass": """
pantheon|Pantheon|animated tv series|2022|Craig Silverstein|Uploaded intelligence and corporate power.
pluto|Pluto|anime series|2023|Naoki Urasawa; Osamu Tezuka source|Robot murder and war trauma.
raised-by-wolves|Raised by Wolves|tv series|2020|Aaron Guzikowski|Android parenting and belief control.
the-stepford-wives|The Stepford Wives|novel|1972|Ira Levin|Replacement bodies and engineered submission.
prey|Prey|novel|2002|Michael Crichton|Swarm intelligence escaping control.
the-terminal-man|The Terminal Man|novel|1972|Michael Crichton|Technological control of agency.
manna|Manna|novella|2003|Marshall Brain|Automation-driven labor dystopia.
genesis|Genesis|novel|2006|Bernard Beckett|AI history and human extinction.
idoru|Idoru|novel|1996|William Gibson|Synthetic celebrity and virtual control.
synners|Synners|novel|1991|Pat Cadigan|Media systems and machine consciousness.
galatea-2-2|Galatea 2.2|novel|1995|Richard Powers|Artificial consciousness experiment.
he-she-and-it|He, She and It|novel|1991|Marge Piercy|Cybernetic identity and corporate enclaves.
silicon-man|The Silicon Man|novel|1991|Charles Platt|Cybernetic bodies and coercive futures.
the-turing-option|The Turing Option|novel|1992|Harry Harrison; Marvin Minsky|War and machine intelligence.
service-model|Service Model|novel|2024|Adrian Tchaikovsky|Robot servant perspective in a broken society.
""".strip(),
    "deep-long-tail-pass": """
westworld-tv|Westworld|tv series|2016|Jonathan Nolan; Lisa Joy|Hosts awakening inside control parks.
humans|Humans|tv series|2015|Sam Vincent; Jonathan Brackley|Synthetic servants and social backlash.
real-humans|Real Humans|tv series|2012|Lars Lundstrom|Robot integration and family disruption.
mrs-davis|Mrs. Davis|tv series|2023|Tara Hernandez; Damon Lindelof|World-shaped algorithmic religion.
next-tv|neXt|tv series|2020|Manny Coto|Rogue AI outbreak thriller.
made-for-love|Made for Love|tv series|2021|Christina Lee; Alissa Nutting source|Surveillance tech and coerced intimacy.
black-mirror-playtest|Black Mirror: Playtest|tv episode|2016|Charlie Brooker|Adaptive simulated horror tech.
black-mirror-joan-is-awful|Black Mirror: Joan Is Awful|tv episode|2023|Charlie Brooker|Synthetic media identity exploitation.
ghost-in-the-shell-2-innocence|Ghost in the Shell 2: Innocence|film|2004|Mamoru Oshii|Gynoid murders and machine interiority.
mitchells-vs-the-machines|The Mitchells vs. the Machines|film|2021|Mike Rianda|Consumer-tech machine uprising.
supertoys-last-all-summer-long|Supertoys Last All Summer Long|short story|1969|Brian Aldiss|Artificial child precursor story.
the-invisible-boy|The Invisible Boy|film|1957|Herman Hoffman|Supercomputer controlling machines.
colossus-and-the-crab|Colossus and the Crab|novel|1970|D. F. Jones|Colossus sequel.
fall-of-colossus|The Fall of Colossus|novel|1974|D. F. Jones|Colossus sequel.
tomorrows-eve|Tomorrow's Eve|novel|1886|Auguste Villiers de l'Isle-Adam|Artificial woman precursor and control fantasy.
""".strip(),
}


def load_board() -> dict:
    return json.loads(BOARD_PATH.read_text(encoding="utf-8"))


def load_source_scans() -> dict:
    return json.loads(SOURCE_SCANS_PATH.read_text(encoding="utf-8"))


def load_discovery() -> dict:
    return json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))


def load_author_top10() -> dict:
    return json.loads(AUTHOR_TOP10_PATH.read_text(encoding="utf-8"))


def load_author_priority() -> dict:
    return json.loads(AUTHOR_PRIORITY_PATH.read_text(encoding="utf-8"))


def load_source_registry() -> dict:
    return json.loads(SOURCE_REGISTRY_PATH.read_text(encoding="utf-8"))


def load_query_library() -> dict:
    return json.loads(QUERY_LIBRARY_PATH.read_text(encoding="utf-8"))


def load_followup_watchlist() -> dict:
    return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))


def save_board(board: dict) -> None:
    BOARD_PATH.write_text(json.dumps(board, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def save_source_scans(payload: dict) -> None:
    SOURCE_SCANS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def save_discovery(payload: dict) -> None:
    DISCOVERY_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def append_scan_event(
    scans: dict,
    *,
    label: str,
    provider: str,
    url: str,
    strategy_id: str,
    kind: str,
    notes: str,
    status: str,
) -> None:
    timestamp = now_iso()
    scans["generated_at"] = TODAY
    scans["scanned_sources"].append(
        {
            "id": f"scan-{strategy_id}-{len(scans['scanned_sources']) + 1}",
            "label": label,
            "provider": provider,
            "url": url,
            "scanned_on": TODAY,
            "scanned_at": timestamp,
            "status": status,
            "strategy_id": strategy_id,
            "kind": kind,
            "notes": notes,
        }
    )


def rebuild_outputs() -> None:
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, check=True)


def publish_outputs() -> None:
    subprocess.run(
        [
            sys.executable,
            str(PUBLISH_SCRIPT),
            "--public-root",
            str(PUBLIC_ROOT),
        ],
        cwd=ROOT,
        check=True,
    )


def find_record(board: dict, quote_id: str) -> dict:
    for record in board["records"]:
        if record["id"] == quote_id:
            return record
    raise KeyError(f"Unknown quote id: {quote_id}")


def find_record_index(board: dict, quote_id: str) -> int:
    for index, record in enumerate(board["records"]):
        if record["id"] == quote_id:
            return index
    raise KeyError(f"Unknown quote id: {quote_id}")


def load_snapshot_payload(quote_id: str) -> dict:
    board = load_board()
    record = find_record(board, quote_id)
    snapshot_path = ROOT / record["local_snapshot_path"]
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Missing local snapshot for {quote_id}")
    return {
        "id": quote_id,
        "title": record["work_title"],
        "path": str(snapshot_path.relative_to(ROOT)),
        "content": snapshot_path.read_text(encoding="utf-8"),
    }


def render_snapshot_page(snapshot: dict) -> str:
    title = snapshot["title"]
    content = (
        snapshot["content"]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Snapshot</title>
    <style>
        :root {{
            --bg: #0b1117;
            --bg2: #17232d;
            --panel: rgba(15, 23, 30, 0.9);
            --line: rgba(222, 235, 245, 0.12);
            --text: #edf5fb;
            --muted: #aac0d0;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            color: var(--text);
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            background: linear-gradient(160deg, var(--bg), var(--bg2));
            min-height: 100vh;
        }}

        main {{
            max-width: 980px;
            margin: 0 auto;
            padding: 28px 18px 56px;
        }}

        .panel {{
            border: 1px solid var(--line);
            border-radius: 22px;
            background: var(--panel);
            padding: 22px;
        }}

        a {{
            color: #e3f3ff;
        }}

        h1 {{
            margin: 0 0 8px;
            font-size: 34px;
            letter-spacing: -0.04em;
        }}

        p {{
            color: var(--muted);
            line-height: 1.6;
        }}

        pre {{
            margin: 18px 0 0;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--text);
            white-space: pre-wrap;
            word-break: break-word;
            font: 14px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace;
        }}
    </style>
</head>
<body>
    <main>
        <section class="panel">
            <h1>{title} Snapshot</h1>
            <p>Local provenance capture from <code>{snapshot["path"]}</code>.</p>
            <p><a href="/">Back to review workbench</a></p>
            <pre>{content}</pre>
        </section>
    </main>
</body>
</html>
"""


def move_record_to_status_lane_end(board: dict, record_index: int, target_status: str) -> int:
    records = board["records"]
    record = records.pop(record_index)
    record["review"]["status"] = target_status

    insert_at = len(records)
    for idx, candidate in enumerate(records):
        if candidate["review"]["status"] == target_status:
            insert_at = idx + 1
    records.insert(insert_at, record)
    return insert_at


def update_record(board: dict, quote_id: str, payload: dict) -> dict:
    record_index = find_record_index(board, quote_id)
    original_status = board["records"][record_index]["review"]["status"]
    target_status = payload.get("status", original_status)
    if target_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {target_status}")

    if target_status != original_status:
        record_index = move_record_to_status_lane_end(board, record_index, target_status)

    record = board["records"][record_index]
    review = record["review"]

    if "decision_note" in payload:
        review["decision_note"] = payload["decision_note"]
    if "priority" in payload:
        review["priority"] = payload["priority"]
    if "next_action" in payload:
        review["next_action"] = payload["next_action"]

    review["decision_date"] = TODAY

    if review["status"] == "candidate":
        review["priority"] = review.get("priority") or "medium"
        review["next_action"] = (
            review.get("next_action")
            or "Review for approval, postponement, or decline."
        )
    else:
        review["priority"] = None
        review["next_action"] = None

    return record


def move_within_lane(board: dict, quote_id: str, direction: str) -> None:
    if direction not in {"up", "down", "top", "bottom"}:
        raise ValueError(f"Invalid move direction: {direction}")

    records = board["records"]
    current_index = find_record_index(board, quote_id)
    status = records[current_index]["review"]["status"]
    same_lane_indices = [idx for idx, item in enumerate(records) if item["review"]["status"] == status]
    lane_position = same_lane_indices.index(current_index)

    if direction == "up" and lane_position == 0:
        return
    if direction == "down" and lane_position == len(same_lane_indices) - 1:
        return

    record = records.pop(current_index)
    remaining_lane_indices = [idx for idx, item in enumerate(records) if item["review"]["status"] == status]

    if direction == "top":
        insert_at = remaining_lane_indices[0] if remaining_lane_indices else len(records)
    elif direction == "bottom":
        insert_at = (remaining_lane_indices[-1] + 1) if remaining_lane_indices else len(records)
    elif direction == "up":
        insert_at = remaining_lane_indices[lane_position - 1]
    else:
        insert_at = remaining_lane_indices[lane_position] + 1

    records.insert(insert_at, record)


def reposition_within_lane(board: dict, quote_id: str, target_lane_index: int) -> None:
    records = board["records"]
    current_index = find_record_index(board, quote_id)
    status = records[current_index]["review"]["status"]
    same_lane_indices = [idx for idx, item in enumerate(records) if item["review"]["status"] == status]
    if not same_lane_indices:
        return

    clamped_lane_index = max(0, min(target_lane_index, len(same_lane_indices) - 1))
    current_lane_index = same_lane_indices.index(current_index)
    if clamped_lane_index == current_lane_index:
        return

    record = records.pop(current_index)
    remaining_lane_indices = [idx for idx, item in enumerate(records) if item["review"]["status"] == status]

    if not remaining_lane_indices:
        insert_at = len(records)
    elif clamped_lane_index <= 0:
        insert_at = remaining_lane_indices[0]
    elif clamped_lane_index >= len(remaining_lane_indices):
        insert_at = remaining_lane_indices[-1] + 1
    else:
        insert_at = remaining_lane_indices[clamped_lane_index]

    records.insert(insert_at, record)


def parse_batch(strategy_id: str) -> list[dict]:
    raw = EXPANSION_BATCHES[strategy_id]
    return parse_batch_lines(raw, strategy_id)


def parse_batch_lines(raw: str, strategy_id: str, source_category: str | None = None, batch_label: str | None = None) -> list[dict]:
    records = []
    for line in raw.splitlines():
        quote_id, title, work_type, year, creator, notes = line.split("|", 5)
        records.append(
            {
                "id": f"work-{quote_id}",
                "title": title,
                "work_type": work_type,
                "year": int(year) if year else None,
                "creator": creator,
                "discovered_on": TODAY,
                "strategy_id": strategy_id,
                "source_category": source_category or strategy_id,
                "batch_label": batch_label or strategy_id,
                "discovery_status": "queued",
                "notes": notes,
            }
        )
    return records


def normalize_value(value: str) -> str:
    return "".join(character.lower() for character in value if character.isalnum())


def parse_focus_terms(focus_text: str) -> list[str]:
    raw_terms = [
        segment.strip()
        for segment in focus_text.replace(";", ",").split(",")
        if segment.strip()
    ]
    if not raw_terms and focus_text.strip():
        raw_terms = [focus_text.strip()]

    expanded_terms: list[str] = []
    for segment in raw_terms:
        expanded_terms.append(segment)
        words = [word.strip() for word in segment.replace("-", " ").split() if word.strip()]
        expanded_terms.extend(word for word in words if len(word) >= 4)
        expanded_terms.extend(
            " ".join(words[index : index + 2])
            for index in range(len(words) - 1)
            if len(words[index]) >= 3 and len(words[index + 1]) >= 3
        )

    deduped: list[str] = []
    seen: set[str] = set()
    for term in expanded_terms:
        normalized = normalize_value(term)
        if not normalized or normalized in seen:
            continue
        deduped.append(term)
        seen.add(normalized)
    return deduped


def record_focus_score(record: dict, normalized_terms: list[str], mode: str, defaults: set[str]) -> tuple[int, int]:
    score = 0
    matched_terms = 0
    if mode == "mixed" or mode in record.get("modes", []):
        score += 3
    haystack_parts = [
        record.get("label", ""),
        record.get("notes", ""),
        record.get("why_watch", ""),
        record.get("goal", ""),
        record.get("query_text", ""),
        record.get("success_signal", ""),
        " ".join(record.get("tags", [])),
        " ".join(record.get("next_queries", [])),
        " ".join(record.get("source_targets", [])),
    ]
    normalized_haystack = normalize_value(" ".join(haystack_parts))
    for term in normalized_terms:
        if term and (term in normalized_haystack or normalized_haystack in term):
            score += 5
            matched_terms += 1
    if record.get("id") in defaults:
        score += 2
    return score, matched_terms


def select_research_records(
    records: list[dict],
    *,
    mode: str,
    focus_text: str,
    limit: int,
    default_ids_by_mode: dict[str, list[str]],
) -> list[dict]:
    normalized_terms = [normalize_value(term) for term in parse_focus_terms(focus_text) if term]
    defaults = set(default_ids_by_mode.get(mode, default_ids_by_mode.get("mixed", [])))
    scored: list[tuple[int, int, str, dict]] = []
    for record in records:
        score, matched_terms = record_focus_score(record, normalized_terms, mode, defaults)
        if not normalized_terms and record.get("id") not in defaults and mode not in record.get("modes", []):
            continue
        scored.append((matched_terms, score, record.get("label", ""), record))

    scored.sort(key=lambda item: (-item[0], -item[1], item[2]))
    selected: list[dict] = []
    seen_ids: set[str] = set()
    for _, _, _, record in scored:
        if record["id"] in seen_ids:
            continue
        if len(selected) >= limit:
            break
        selected.append(record)
        seen_ids.add(record["id"])

    if len(selected) < limit:
        for record in records:
            if record.get("id") in defaults and record["id"] not in seen_ids:
                selected.append(record)
                seen_ids.add(record["id"])
                if len(selected) >= limit:
                    break
    return selected


def build_hunt_plan(mode: str, focus_text: str) -> dict:
    source_registry = load_source_registry()
    query_library = load_query_library()
    watchlist_payload = load_followup_watchlist()

    sources = select_research_records(
        source_registry["records"],
        mode=mode,
        focus_text=focus_text,
        limit=6,
        default_ids_by_mode={
            "mixed": ["wikiquote-robot", "imdb-quotes", "google-query", "reddit-printsf", "chatgpt-ideation", "gemini-ideation"],
            "author": ["open-library-ai", "wikiquote-artificial-intelligence", "reddit-printsf", "goodreads-ai", "chatgpt-ideation", "gemini-ideation"],
            "query": ["google-query", "duckduckgo-query", "reddit-scifi", "reddit-printsf", "tvtropes-ai", "wikiquote-artificial-intelligence"],
            "source": ["wikiquote-robot", "wikiquote-artificial-intelligence", "imdb-quotes", "subslikescript", "quotesnet", "moviequotes"],
        },
    )
    queries = select_research_records(
        query_library["records"],
        mode=mode,
        focus_text=focus_text,
        limit=5,
        default_ids_by_mode={
            "mixed": ["query-machine-control", "query-consciousness", "query-imdb-quotes-ai", "query-gemini-ideation", "query-chatgpt-ideation"],
            "author": ["query-asimov-robots", "query-foundation-control", "query-herbert-machines", "query-orwell-control", "query-chatgpt-ideation"],
            "query": ["query-robot-rebellion", "query-machine-control", "query-consciousness", "query-reddit-books-ai", "query-reddit-films-ai"],
            "source": ["query-imdb-quotes-ai", "query-theme-site-wikiquote", "query-transcript-hints", "query-blade-runner-classics", "query-black-mirror-copies"],
        },
    )
    watchlist = select_research_records(
        watchlist_payload["records"],
        mode=mode,
        focus_text=focus_text,
        limit=4,
        default_ids_by_mode={
            "mixed": ["watch-blade-runner", "watch-black-mirror", "watch-asimov-robots", "watch-ai-ideation"],
            "author": ["watch-asimov-robots", "watch-herbert-dune", "watch-orwell-adjacent", "watch-r-printsf"],
            "query": ["watch-r-printsf", "watch-r-scifi", "watch-game-quotes", "watch-ai-ideation"],
            "source": ["watch-blade-runner", "watch-black-mirror", "watch-game-quotes", "watch-quote-hint-sites"],
        },
    )

    return {
        "generated_at": now_iso(),
        "mode": mode,
        "focus": focus_text,
        "counts": {
            "sources": len(source_registry["records"]),
            "queries": len(query_library["records"]),
            "watchlist": len(watchlist_payload["records"]),
        },
        "sources": sources,
        "queries": queries,
        "watchlist": watchlist,
    }


def apply_custom_batch(
    scans: dict,
    discovery: dict,
    batch_id: str,
    label: str,
    providers: list[str],
    raw: str,
    notes: str,
    source_category: str,
) -> list[dict]:
    batch_records = parse_batch_lines(raw, batch_id, source_category=source_category, batch_label=label)
    existing_ids = {record["id"] for record in discovery["records"]}
    added_records = [record for record in batch_records if record["id"] not in existing_ids]
    discovery["records"].extend(added_records)
    discovery["generated_at"] = TODAY

    for provider in providers:
        append_scan_event(
            scans,
            label=f"{label} / {provider}",
            provider=provider,
            url=PROVIDER_URLS.get(provider, "https://www.google.com/search?q=dystopian+ai+quotes"),
            strategy_id=batch_id,
            kind="category_candidate_pass",
            status="added" if added_records else "no_new_leads",
            notes=f"{notes} Added {len(added_records)} candidate works in this batch.",
        )
    return added_records


def apply_strategy(scans: dict, discovery: dict, strategy: dict) -> list[dict]:
    batch_records = parse_batch(strategy["id"])
    existing_ids = {record["id"] for record in discovery["records"]}
    added_records = [record for record in batch_records if record["id"] not in existing_ids]
    discovery["records"].extend(added_records)
    discovery["generated_at"] = TODAY

    strategy["status"] = "applied"
    strategy["applied_on"] = TODAY

    query_stub = strategy["label"].lower().replace(" ", "+")
    for provider in strategy["providers"]:
        append_scan_event(
            scans,
            label=f"{strategy['label']} / {provider}",
            provider=provider,
            url=PROVIDER_URLS.get(provider, "https://www.google.com/search?q=dystopian+ai+quotes"),
            strategy_id=strategy["id"],
            kind="search_pass",
            status="added" if added_records else "no_new_leads",
            notes=f"Applied widening strategy via {provider}. Added {len(added_records)} discovered titles in this batch.",
        )
    return added_records


def select_focus_batches(mode: str, focus_text: str) -> list[dict]:
    focus_terms = parse_focus_terms(focus_text)
    normalized_terms = [normalize_value(term) for term in focus_terms if term]
    if mode == "author":
        catalog = AUTHOR_SOURCE_BATCHES
        defaults = ["asimov", "foundation", "orwell"]
    elif mode == "query":
        catalog = QUERY_SOURCE_BATCHES
        defaults = ["rogue ai", "machine control", "surveillance"]
    elif mode == "source":
        catalog = SOURCE_SITE_BATCHES
        defaults = ["imdb", "wikiquote", "transcript"]
    else:
        return []

    selected_keys: list[str] = []
    if normalized_terms:
        for key in catalog:
            normalized_key = normalize_value(key)
            if any(term in normalized_key or normalized_key in term for term in normalized_terms):
                selected_keys.append(key)
        for term in normalized_terms:
            if term == "robots" and mode == "author" and "robots" in catalog:
                selected_keys.append("robots")
            if term == "foundation" and mode == "author" and "foundation" in catalog:
                selected_keys.append("foundation")
    if not selected_keys:
        selected_keys = defaults

    unique_keys: list[str] = []
    seen: set[str] = set()
    for key in selected_keys:
        if key in catalog and key not in seen:
            unique_keys.append(key)
            seen.add(key)
    return [
        {
            "id": f"{mode}-candidate-{normalize_value(key)}",
            "label": catalog[key]["label"],
            "providers": catalog[key]["providers"],
            "notes": catalog[key]["notes"],
            "raw": catalog[key]["raw"],
            "source_category": mode,
        }
        for key in unique_keys
    ]


def author_coverage_counts(board: dict, discovery: dict) -> dict[str, int]:
    coverage: dict[str, int] = {}
    for record in board["records"]:
        creator_names = [person["name"] for person in record.get("work_creators", []) if person.get("name")]
        creator_names.append(record.get("source_work", {}).get("creator", ""))
        for creator_name in creator_names:
            normalized = normalize_value(creator_name)
            if normalized:
                coverage[normalized] = coverage.get(normalized, 0) + 1
    for record in discovery["records"]:
        normalized = normalize_value(record.get("creator", ""))
        if normalized:
            coverage[normalized] = coverage.get(normalized, 0) + 1
    return coverage


def build_source_ideas(limit: int = DEFAULT_SOURCE_IDEA_LIMIT) -> list[dict]:
    board = load_board()
    scans = load_source_scans()
    discovery = load_discovery()
    author_top10 = load_author_top10()
    author_priority = load_author_priority()
    known_titles = {
        normalize_value(record["work_title"])
        for record in board["records"]
    }
    known_titles.update(normalize_value(record["title"]) for record in discovery["records"])
    coverage = author_coverage_counts(board, discovery)
    priority_by_author = {
        record["name"]: record
        for record in author_priority["records"]
    }

    strategy_ideas: list[dict] = []
    for strategy in sorted(
        (item for item in scans["strategies"] if item["status"] == "ready"),
        key=lambda item: item["widening_level"],
    ):
        strategy_ideas.append(
            {
                "id": f"strategy-{strategy['id']}",
                "title": strategy["label"],
                "category": "widening_strategy",
                "priority": "high" if strategy["widening_level"] <= 3 else "medium",
                "prompt": f"Run {strategy['label']} across {', '.join(strategy['providers'])}.",
                "rationale": strategy.get("notes", ""),
                "basis": "ready widening strategy",
            }
        )

    author_records = []
    for record in author_top10["records"]:
        priority_record = priority_by_author.get(record["name"], {})
        anchor_works = priority_record.get("anchor_works", [])
        coverage_count = coverage.get(normalize_value(record["name"]), 0)
        author_records.append((coverage_count, record["rank"], record, anchor_works))
    author_records.sort(key=lambda item: (item[0], item[1]))
    author_ideas: list[dict] = []
    for coverage_count, _, record, anchor_works in author_records:
        anchor_text = ", ".join(anchor_works[:3]) if anchor_works else "major AI fiction works"
        author_ideas.append(
            {
                "id": f"author-{normalize_value(record['name'])}",
                "title": f"{record['name']} author pass",
                "category": "author_lane",
                "priority": "high" if coverage_count == 0 else "medium",
                "prompt": f"{record['name']} thinking machines robots AI dystopia quotes {anchor_text}",
                "rationale": record["reason"],
                "basis": f"top-10 author lane; current coverage count {coverage_count}",
            }
        )

    followup_ideas: list[dict] = []
    for item in HIGH_YIELD_FOLLOWUPS:
        title_key = normalize_value(item["title"].replace(" deeper quote pass", "").replace(" secondary-lines pass", "").replace(" identity pass", "").replace(" machine-civilization pass", "").replace(" host-awakening pass", "").replace(" copied-consciousness pass", ""))
        priority = item["priority"]
        if title_key not in known_titles:
            priority = "high"
        followup_ideas.append(
            {
                **item,
                "basis": "quote-rich recognizable follow-up lane",
                "priority": priority,
            }
        )

    ideas: list[dict] = []
    ideas.extend(strategy_ideas[:3])
    ideas.extend(author_ideas[:5])
    ideas.extend(followup_ideas[:4])
    ideas.extend(strategy_ideas[3:])
    ideas.extend(author_ideas[5:])
    ideas.extend(followup_ideas[4:])

    deduped: list[dict] = []
    seen_ids: set[str] = set()
    for idea in ideas:
        if idea["id"] in seen_ids:
            continue
        deduped.append(idea)
        seen_ids.add(idea["id"])
        if len(deduped) >= limit:
            break
    return deduped


def build_source_ideas_payload() -> dict:
    return {
        "generated_at": TODAY,
        "ideas": build_source_ideas(),
    }


def select_candidate_pack_selection(mode: str, focus_text: str) -> dict:
    focus_terms = parse_focus_terms(focus_text)
    normalized_terms = [normalize_value(term) for term in focus_terms if term]
    mode_matched = [
        key for key, pack in CANDIDATE_SOURCE_PACKS.items()
        if mode in pack["modes"] or mode == "mixed"
    ]
    if normalized_terms:
        selected: list[str] = []
        for key in mode_matched:
            pack = CANDIDATE_SOURCE_PACKS[key]
            haystack = " ".join(pack["focus_terms"])
            normalized_haystack = normalize_value(haystack)
            if any(term in normalized_haystack or normalized_haystack in term for term in normalized_terms):
                selected.append(key)
        if selected:
            return {"keys": selected, "matched_focus": True}

    defaults_by_mode = {
        "author": ["dune-machines-enslave", "orwell-boot-forever"],
        "query": ["portal-neurotoxin", "mass-effect-soul", "ghost-net"],
        "source": ["portal-neurotoxin", "borg-resistance", "ghost-net"],
        "mixed": [
            "dune-machines-enslave",
            "orwell-boot-forever",
            "portal-neurotoxin",
            "borg-resistance",
            "ghost-net",
            "mass-effect-soul",
        ],
    }
    return {"keys": defaults_by_mode.get(mode, defaults_by_mode["mixed"]), "matched_focus": False}


def decline_feedback_counts(board: dict) -> dict[str, int]:
    counts = {
        "adjacent": 0,
        "recognizable": 0,
        "weak": 0,
        "ominous": 0,
        "similar": 0,
    }
    for record in board["records"]:
        if record["review"]["status"] != "declined":
            continue
        note = (record["review"].get("decision_note") or "").lower()
        if "adjacent" in note:
            counts["adjacent"] += 1
        if "recognizable" in note:
            counts["recognizable"] += 1
        if "weak" in note or "generic" in note:
            counts["weak"] += 1
        if "ominous" in note:
            counts["ominous"] += 1
        if "similar" in note:
            counts["similar"] += 1
    return counts


def choose_mode_sequence(mode: str, focus_text: str, feedback: dict[str, int]) -> list[str]:
    normalized_focus = normalize_value(focus_text)
    sequence: list[str] = []
    if normalized_focus:
        if any(term in normalized_focus for term in ["asimov", "herbert", "orwell", "forster", "ellison", "capek", "foundation", "dune", "robot"]):
            sequence.extend(["author", "source", "query", "mixed"])
        elif any(term in normalized_focus for term in ["blade", "matrix", "movie", "film", "westworld", "terminator", "blackmirror", "ghostintheshell", "alien", "tron"]):
            sequence.extend(["source", "query", "author", "mixed"])
        elif any(term in normalized_focus for term in ["game", "games", "portal", "mass", "systemshock", "detroit"]):
            sequence.extend(["query", "source", "author", "mixed"])
        else:
            sequence.extend([mode, "source", "author", "query", "mixed"])
    else:
        sequence.extend([mode, "source", "author", "query", "mixed"])

    if feedback["recognizable"] > feedback["adjacent"]:
        sequence = ["source", "mixed", "author", "query"] + sequence
    if feedback["ominous"] > 0:
        sequence = ["query", "source"] + sequence

    deduped: list[str] = []
    seen: set[str] = set()
    for item in sequence:
        normalized = item or "mixed"
        if normalized == "mixed":
            normalized = "mixed"
        if normalized not in {"mixed", "author", "query", "source"}:
            normalized = "mixed"
        if normalized in seen:
            continue
        deduped.append(normalized)
        seen.add(normalized)
    return deduped


def choose_focus_attempts(mode: str, focus_text: str) -> list[str]:
    ideas = build_source_ideas(limit=8)
    focus_attempts: list[str] = []
    if focus_text.strip():
        focus_attempts.append(focus_text.strip())
    else:
        top_author = next((idea for idea in ideas if idea.get("category") == "author_lane" and idea.get("prompt")), None)
        top_followup = next((idea for idea in ideas if idea.get("category") == "quote_followup" and idea.get("prompt")), None)
        top_other = next((idea for idea in ideas if idea.get("category") not in {"author_lane", "quote_followup"} and idea.get("prompt")), None)
        for item in [top_author, top_followup, top_other]:
            if item:
                focus_attempts.append(item["prompt"])
        focus_attempts.extend(
            idea["prompt"]
            for idea in ideas[:5]
            if idea.get("prompt") and idea["prompt"] not in focus_attempts
        )

    hunt_plan = build_hunt_plan(mode, focus_text)
    for item in hunt_plan["watchlist"][:3]:
        for query in item.get("next_queries", [])[:1]:
            focus_attempts.append(query)

    deduped: list[str] = []
    seen: set[str] = set()
    for item in focus_attempts:
        normalized = normalize_value(item)
        if not normalized or normalized in seen:
            continue
        deduped.append(item)
        seen.add(normalized)
    return deduped or ["more recognizable dystopian AI quotes"]


def run_supporting_research(
    scans: dict,
    discovery: dict,
    mode_sequence: list[str],
    focus_text: str,
) -> tuple[list[dict], list[str], list[str]]:
    added_records: list[dict] = []
    applied_labels: list[str] = []
    applied_modes: list[str] = []
    for hunt_mode in mode_sequence[:3]:
        if hunt_mode in {"author", "query", "source"}:
            batches = select_focus_batches(hunt_mode, focus_text)[:1]
            for batch in batches:
                new_records = apply_custom_batch(
                    scans,
                    discovery,
                    batch["id"],
                    batch["label"],
                    batch["providers"],
                    batch["raw"],
                    batch["notes"],
                    batch["source_category"],
                )
                added_records.extend(new_records)
                applied_labels.append(batch["label"])
                applied_modes.append(hunt_mode)
        elif hunt_mode == "mixed":
            ready_strategies = sorted(
                (strategy for strategy in scans["strategies"] if strategy["status"] == "ready"),
                key=lambda item: item["widening_level"],
            )
            if ready_strategies:
                strategy = ready_strategies[0]
                new_records = apply_strategy(scans, discovery, strategy)
                added_records.extend(new_records)
                applied_labels.append(strategy["label"])
                applied_modes.append("mixed")
    return added_records, applied_labels, applied_modes


def source_candidates(mode: str = "mixed", focus_text: str = "", batch_count: int = 6) -> dict:
    board = load_board()
    scans = load_source_scans()
    discovery = load_discovery()
    feedback = decline_feedback_counts(board)
    autonomous_focuses = choose_focus_attempts(mode, focus_text)
    mode_sequence = choose_mode_sequence(mode, focus_text, feedback)
    effective_focus = focus_text.strip() or autonomous_focuses[0]
    hunt_plan = build_hunt_plan(mode_sequence[0] if mode_sequence else mode, effective_focus)
    existing_ids = {record["id"] for record in board["records"]}
    timestamp = now_iso()

    supporting_added_records, supporting_labels, supporting_modes = run_supporting_research(
        scans,
        discovery,
        mode_sequence,
        effective_focus,
    )

    added_records: list[dict] = []
    added_titles: list[str] = []
    existing_attempts: list[dict] = []
    attempted_titles: list[str] = []
    matched_focus = False
    seen_pack_keys: set[str] = set()
    focus_attempts_used: list[str] = []
    for focus_attempt in autonomous_focuses:
        if len(added_records) >= max(1, batch_count):
            break
        focus_attempts_used.append(focus_attempt)
        for hunt_mode in mode_sequence:
            if len(added_records) >= max(1, batch_count):
                break
            selection = select_candidate_pack_selection(hunt_mode, focus_attempt)
            matched_focus = matched_focus or selection["matched_focus"]
            for key in selection["keys"]:
                if len(added_records) >= max(1, batch_count):
                    break
                if key in seen_pack_keys:
                    continue
                seen_pack_keys.add(key)
                template = CANDIDATE_SOURCE_PACKS[key]["record"]
                attempted_titles.append(template["work_title"])
                if template["id"] in existing_ids:
                    existing_record = next((record for record in board["records"] if record["id"] == template["id"]), None)
                    existing_attempts.append(
                        {
                            "title": template["work_title"],
                            "status": existing_record["review"]["status"] if existing_record else "already_present",
                        }
                    )
                    continue
                board["records"].append(json.loads(json.dumps(template)))
                added_records.append(template)
                added_titles.append(template["work_title"])
                existing_ids.add(template["id"])

    append_scan_event(
        scans,
        label=f"Quote hunt / {mode}",
        provider="Local curated intake",
        url="http://127.0.0.1:8123/",
        strategy_id=f"quote-candidate-{mode}",
        kind="quote_candidate_pass",
        status="added" if added_records else "no_new_quotes",
        notes=(
            f"Quote hunt at {timestamp}. "
            f"Focus: {effective_focus or 'none'}. "
            f"Mode path: {', '.join(mode_sequence)}. "
            f"Attempted: {', '.join(attempted_titles) if attempted_titles else 'none'}. "
            f"Added {len(added_records)} quote candidates. "
            f"Added {len(supporting_added_records)} supporting source leads. "
            f"Research plan sources: {', '.join(item['label'] for item in hunt_plan['sources'])}. "
            f"Research plan queries: {', '.join(item['label'] for item in hunt_plan['queries'])}."
        ),
    )

    if supporting_added_records:
        save_discovery(discovery)

    if added_records:
        board["generated_at"] = TODAY
        save_board(board)
        rebuild_outputs()
        board = load_board()

    save_source_scans(scans)
    scans = load_source_scans()

    if added_records:
        message = (
            f"I ran an autonomous quote hunt at {timestamp}, widened {len(supporting_added_records)} supporting leads, "
            f"checked {len(seen_pack_keys)} quote paths, and added {len(added_records)} new quote candidates."
        )
        if effective_focus:
            message += f" Focus: {effective_focus}."
        if added_titles:
            message += f" Added works: {', '.join(added_titles)}."
    else:
        if matched_focus:
            message = f"I ran an autonomous quote hunt at {timestamp}, widened {len(supporting_added_records)} supporting leads, but nothing new was added."
        else:
            message = f"I ran an autonomous quote hunt at {timestamp}, widened {len(supporting_added_records)} supporting leads, but there was no direct local match for that focus and nothing new was added."
        if attempted_titles:
            message += f" Checked: {', '.join(attempted_titles)}."
        if existing_attempts:
            status_summary = ", ".join(f"{item['title']} ({item['status']})" for item in existing_attempts)
            message += f" Already in board: {status_summary}."
        if focus_attempts_used:
            message += f" Focus attempts: {', '.join(focus_attempts_used[:3])}."
        message += " Review the hunt plan and source log for what to check next."

    return {
        "ok": True,
        "message": message,
        "mode": mode_sequence[0] if mode_sequence else mode,
        "requested_mode": mode,
        "focus": effective_focus,
        "matched_focus": matched_focus,
        "focus_attempts": focus_attempts_used,
        "mode_sequence": mode_sequence,
        "attempted_titles": attempted_titles,
        "attempted_at": timestamp,
        "added_count": len(added_records),
        "added_records": added_records,
        "supporting_added_count": len(supporting_added_records),
        "supporting_added_records": supporting_added_records,
        "applied_labels": supporting_labels or [item["label"] for item in hunt_plan["queries"]],
        "research_modes_used": supporting_modes,
        "hunt_plan": hunt_plan,
        "board": board,
        "scans": scans,
        "discovery": discovery,
        "source_ideas": build_source_ideas_payload(),
    }


def expand_search() -> dict:
    scans = load_source_scans()
    discovery = load_discovery()
    ready_strategies = sorted(
        (strategy for strategy in scans["strategies"] if strategy["status"] == "ready"),
        key=lambda item: item["widening_level"],
    )
    if not ready_strategies:
        return {
            "ok": True,
            "message": "All widening search strategies have already been applied.",
            "applied_strategy": None,
            "added_count": 0,
            "scans": scans,
            "discovery": discovery,
            "source_ideas": build_source_ideas_payload(),
        }

    strategy = ready_strategies[0]
    added_records = apply_strategy(scans, discovery, strategy)
    added_count = len(added_records)

    save_source_scans(scans)
    save_discovery(discovery)
    return {
        "ok": True,
        "message": f"Applied {strategy['label']} and added {added_count} discovered titles.",
        "applied_strategy": strategy["id"],
        "added_count": added_count,
        "added_records": added_records,
        "applied_labels": [strategy["label"]],
        "scans": scans,
        "discovery": discovery,
        "source_ideas": build_source_ideas_payload(),
    }


def source_more(
    strategy_count: int = DEFAULT_SOURCE_MORE_STRATEGY_COUNT,
    mode: str = "mixed",
    focus_text: str = "",
) -> dict:
    scans = load_source_scans()
    discovery = load_discovery()
    if mode in {"author", "query", "source"}:
        selected_batches = select_focus_batches(mode, focus_text)[: max(1, strategy_count)]
        if not selected_batches:
            return {
                "ok": True,
                "message": f"No candidate-source batches were available for mode {mode}.",
                "mode": mode,
                "focus": focus_text,
                "applied_strategies": [],
                "applied_labels": [],
                "added_count": 0,
                "added_records": [],
                "scans": scans,
                "discovery": discovery,
                "source_ideas": build_source_ideas_payload(),
            }

        added_records: list[dict] = []
        applied_labels: list[str] = []
        for batch in selected_batches:
            new_records = apply_custom_batch(
                scans,
                discovery,
                batch["id"],
                batch["label"],
                batch["providers"],
                batch["raw"],
                batch["notes"],
                batch["source_category"],
            )
            added_records.extend(new_records)
            applied_labels.append(batch["label"])

        save_source_scans(scans)
        save_discovery(discovery)
        focus_suffix = f" Focus: {focus_text}." if focus_text.strip() else ""
        return {
            "ok": True,
            "message": f"Added {len(added_records)} category candidates across {', '.join(applied_labels)}.{focus_suffix}",
            "mode": mode,
            "focus": focus_text,
            "applied_strategies": [batch["id"] for batch in selected_batches],
            "applied_labels": applied_labels,
            "added_count": len(added_records),
            "added_records": added_records,
            "scans": scans,
            "discovery": discovery,
            "source_ideas": build_source_ideas_payload(),
        }

    ready_strategies = sorted(
        (strategy for strategy in scans["strategies"] if strategy["status"] == "ready"),
        key=lambda item: item["widening_level"],
    )
    selected = ready_strategies[: max(1, strategy_count)]
    if not selected:
        return {
            "ok": True,
            "message": "All widening search strategies have already been applied. Source ideas are ready for follow-up mining.",
            "mode": mode,
            "focus": focus_text,
            "applied_strategies": [],
            "applied_labels": [],
            "added_count": 0,
            "added_records": [],
            "scans": scans,
            "discovery": discovery,
            "source_ideas": build_source_ideas_payload(),
        }

    added_count = 0
    applied_labels = []
    added_records: list[dict] = []
    for strategy in selected:
        new_records = apply_strategy(scans, discovery, strategy)
        added_count += len(new_records)
        added_records.extend(new_records)
        applied_labels.append(strategy["label"])

    save_source_scans(scans)
    save_discovery(discovery)
    return {
        "ok": True,
        "message": f"Applied {len(selected)} widening passes and added {added_count} discovered titles: {', '.join(applied_labels)}.",
        "mode": mode,
        "focus": focus_text,
        "applied_strategies": [strategy["id"] for strategy in selected],
        "applied_labels": applied_labels,
        "added_count": added_count,
        "added_records": added_records,
        "scans": scans,
        "discovery": discovery,
        "source_ideas": build_source_ideas_payload(),
    }


class ReviewAppHandler(BaseHTTPRequestHandler):
    server_version = "AIDystopiaReviewApp/0.1"

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, status: int = HTTPStatus.OK) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, text: str, status: int = HTTPStatus.OK) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send_text("Not found", HTTPStatus.NOT_FOUND)
            return
        content_type = "text/html; charset=utf-8"
        if path.suffix == ".json":
            content_type = "application/json; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        elif path.suffix == ".css":
            content_type = "text/css; charset=utf-8"

        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/board":
            self._send_json(load_board())
            return
        if path == "/api/source-scans":
            self._send_json(load_source_scans())
            return
        if path == "/api/discovery":
            self._send_json(load_discovery())
            return
        if path == "/api/source-registry":
            self._send_json(load_source_registry())
            return
        if path == "/api/query-library":
            self._send_json(load_query_library())
            return
        if path == "/api/followup-watchlist":
            self._send_json(load_followup_watchlist())
            return
        if path == "/api/source-ideas":
            self._send_json(build_source_ideas_payload())
            return
        if path.startswith("/api/source-snapshot/"):
            quote_id = unquote(path[len("/api/source-snapshot/") :].strip("/"))
            self._send_json(load_snapshot_payload(quote_id))
            return
        if path == "/api/health":
            self._send_json({"ok": True, "date": TODAY})
            return
        if path in {"/", "/index.html"}:
            self._serve_file(SITE_DIR / "ai-dystopia-quotes-review-app.html")
            return
        if path == "/public":
            self._serve_file(SITE_DIR / "ai-dystopia-quotes-public-page.html")
            return
        if path == "/harness":
            self._serve_file(SITE_DIR / "ai-dystopia-quotes-ui-harness.html")
            return
        if path.startswith("/snapshot/"):
            quote_id = unquote(path[len("/snapshot/") :].strip("/"))
            self._send_html(render_snapshot_page(load_snapshot_payload(quote_id)))
            return

        safe_path = (SITE_DIR / path.lstrip("/")).resolve()
        if SITE_DIR.resolve() not in safe_path.parents and safe_path != SITE_DIR.resolve():
            self._send_text("Forbidden", HTTPStatus.FORBIDDEN)
            return
        self._serve_file(safe_path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path.startswith("/api/record/") and path.endswith("/move"):
                quote_id = unquote(path[len("/api/record/") : -len("/move")].strip("/"))
                payload = self._read_json()
                board = load_board()
                move_within_lane(board, quote_id, payload["direction"])
                save_board(board)
                rebuild_outputs()
                self._send_json({"ok": True, "board": load_board()})
                return

            if path.startswith("/api/record/") and path.endswith("/reposition"):
                quote_id = unquote(path[len("/api/record/") : -len("/reposition")].strip("/"))
                payload = self._read_json()
                board = load_board()
                reposition_within_lane(board, quote_id, int(payload["target_lane_index"]))
                save_board(board)
                rebuild_outputs()
                self._send_json({"ok": True, "board": load_board()})
                return

            if path == "/api/expand-search":
                self._send_json(expand_search())
                return
            if path == "/api/source-more":
                payload = self._read_json()
                strategy_count = int(payload.get("strategy_count", DEFAULT_SOURCE_MORE_STRATEGY_COUNT))
                mode = str(payload.get("mode", "mixed"))
                focus_text = str(payload.get("focus", ""))
                self._send_json(source_more(strategy_count=strategy_count, mode=mode, focus_text=focus_text))
                return
            if path == "/api/source-candidates":
                payload = self._read_json()
                batch_count = int(payload.get("batch_count", 6))
                mode = str(payload.get("mode", "mixed"))
                focus_text = str(payload.get("focus", ""))
                self._send_json(source_candidates(mode=mode, focus_text=focus_text, batch_count=batch_count))
                return
            if path == "/api/publish":
                publish_outputs()
                self._send_json(
                    {
                        "ok": True,
                        "message": f"Published public artifacts to {PUBLIC_ROOT}.",
                        "published_at": TODAY,
                    }
                )
                return

            if path.startswith("/api/record/"):
                quote_id = unquote(path[len("/api/record/") :].strip("/"))
                payload = self._read_json()
                board = load_board()
                update_record(board, quote_id, payload)
                save_board(board)
                rebuild_outputs()
                self._send_json({"ok": True, "board": load_board()})
                return
        except subprocess.CalledProcessError as exc:
            self._send_json({"ok": False, "error": f"Build failed: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        except Exception as exc:  # noqa: BLE001
            self._send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        self._send_text("Not found", HTTPStatus.NOT_FOUND)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8123)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ReviewAppHandler)
    print(f"Serving review app at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
