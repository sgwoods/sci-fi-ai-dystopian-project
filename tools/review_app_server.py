#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
BOARD_PATH = ROOT / "data" / "review" / "ai-dystopia-quotes.review-board.json"
SOURCE_SCANS_PATH = ROOT / "data" / "review" / "ai-dystopia-source-scans.json"
DISCOVERY_PATH = ROOT / "data" / "discovery" / "ai-dystopia-title-discovery.json"
BUILD_SCRIPT = ROOT / "tools" / "build_quotes_project.py"
TODAY = date.today().isoformat()
VALID_STATUSES = {"candidate", "approved", "postponed", "declined"}
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


def save_board(board: dict) -> None:
    BOARD_PATH.write_text(json.dumps(board, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def save_source_scans(payload: dict) -> None:
    SOURCE_SCANS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def save_discovery(payload: dict) -> None:
    DISCOVERY_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def rebuild_outputs() -> None:
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, check=True)


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
                "discovery_status": "queued",
                "notes": notes,
            }
        )
    return records


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
        }

    strategy = ready_strategies[0]
    batch_records = parse_batch(strategy["id"])
    existing_ids = {record["id"] for record in discovery["records"]}
    added_records = [record for record in batch_records if record["id"] not in existing_ids]
    discovery["records"].extend(added_records)
    discovery["generated_at"] = TODAY

    strategy["status"] = "applied"
    strategy["applied_on"] = TODAY
    scans["generated_at"] = TODAY

    query_stub = strategy["label"].lower().replace(" ", "+")
    for provider in strategy["providers"]:
        scans["scanned_sources"].append(
            {
                "id": f"scan-{strategy['id']}-{provider.lower().replace(' ', '-')}",
                "label": f"{strategy['label']} / {provider}",
                "provider": provider,
                "url": PROVIDER_URLS.get(provider, "https://www.google.com/search?q=dystopian+ai+quotes"),
                "scanned_on": TODAY,
                "strategy_id": strategy["id"],
                "kind": "search_pass",
                "notes": f"Applied widening strategy via {provider}. Added {len(added_records)} discovered titles in this batch.",
            }
        )

    save_source_scans(scans)
    save_discovery(discovery)
    return {
        "ok": True,
        "message": f"Applied {strategy['label']} and added {len(added_records)} discovered titles.",
        "applied_strategy": strategy["id"],
        "added_count": len(added_records),
        "scans": scans,
        "discovery": discovery,
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
