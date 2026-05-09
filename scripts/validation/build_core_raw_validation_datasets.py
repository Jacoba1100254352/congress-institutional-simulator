#!/usr/bin/env python3
"""Build core raw empirical validation samples from public sources.

The simulator treats raw validation inputs differently from API adapter
fixtures. This script writes small, documented source extracts under
``data/validation/raw/`` for validation-bridge work. The extracts are samples,
not complete fitted datasets, and should be described that way in the paper.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


RAW_DIR = Path("data/validation/raw")
USER_AGENT = "congress-institutional-simulator-validation/0.3"
VOTEVIEW_BASE = "https://voteview.com/static/data/out"
CONGRESS_BASE = "https://api.congress.gov/v3"
LDA_BASE = "https://lda.senate.gov/api/v1"


@dataclass(frozen=True)
class BillRef:
    congress: int
    bill_type: str
    number: str

    @property
    def bill_id(self) -> str:
        return f"{self.congress}-{self.bill_type.lower()}-{self.number}"

    @property
    def detail_url(self) -> str:
        bill_kind = self.bill_type.lower()
        return f"https://www.congress.gov/bill/{self.congress}th-congress/{bill_kind}-bill/{self.number}"


def env_values(path: Path | None) -> dict[str, str]:
    values: dict[str, str] = {}
    if path is None or not path.exists():
        return values
    for line in path.read_text(errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def api_get(url: str, params: dict[str, object] | None = None, retries: int = 4) -> dict[str, object]:
    request_url = url if not params else f"{url}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=60) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)
    raise RuntimeError("unreachable retry state")


def csv_rows(url: str) -> list[dict[str, str]]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=90) as response:
        text = response.read().decode("utf-8", errors="replace").splitlines()
    return list(csv.DictReader(text))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, title: str, lines: list[str]) -> None:
    path.write_text(
        "\n".join([
            f"# {title}",
            "",
            f"- Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
            *lines,
            "",
            "This is a curated validation sample, not a complete fitted dataset.",
            "Use it for empirical-bridge checks and rough plausibility screening only.",
        ]) + "\n"
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "passed", "enacted"}


def parse_offsets(value: str) -> list[int]:
    offsets = [int(part.strip()) for part in value.split(",") if part.strip()]
    return offsets or [0]


def build_voteview(congress: int, rollcall_limit: int) -> dict[str, int]:
    chamber_code = f"HS{congress}"
    member_url = f"{VOTEVIEW_BASE}/members/{chamber_code}_members.csv"
    vote_url = f"{VOTEVIEW_BASE}/votes/{chamber_code}_votes.csv"
    member_rows = csv_rows(member_url)
    vote_rows = csv_rows(vote_url)

    members: dict[str, dict[str, str]] = {}
    for row in member_rows:
        if row.get("chamber") == "President":
            continue
        members[row["icpsr"]] = row

    selected_rollcalls = sorted({int(row["rollnumber"]) for row in vote_rows})[:rollcall_limit]
    selected = set(selected_rollcalls)
    party_names = {"100": "D", "200": "R", "328": "I"}
    cast_map = {
        "1": "yea",
        "2": "yea",
        "3": "yea",
        "4": "nay",
        "5": "nay",
        "6": "nay",
    }
    out_rows: list[dict[str, object]] = []
    for vote in vote_rows:
        try:
            rollnumber = int(vote["rollnumber"])
        except ValueError:
            continue
        if rollnumber not in selected:
            continue
        cast = cast_map.get(vote.get("cast_code", ""))
        if cast is None:
            continue
        member = members.get(vote.get("icpsr", ""))
        if member is None:
            continue
        party = party_names.get(member.get("party_code", ""), member.get("party_code", "unknown"))
        ideology = member.get("nominate_dim1") or member.get("nokken_poole_dim1") or "0"
        out_rows.append({
            "congress": congress,
            "party": party,
            "vote_id": f"{congress}-{member.get('chamber', 'Unknown')}-{rollnumber}",
            "vote": cast,
            "ideology": ideology,
            "chamber": member.get("chamber", ""),
            "icpsr": vote.get("icpsr", ""),
        })

    write_csv(
        RAW_DIR / "voteview_rollcalls.csv",
        ["congress", "party", "vote_id", "vote", "ideology", "chamber", "icpsr"],
        out_rows,
    )
    write_metadata(
        RAW_DIR / "voteview_rollcalls.metadata.md",
        "Voteview Roll-Call Raw Validation Sample",
        [
            "- Source: Voteview static HS member and vote CSV files.",
            f"- Congress: {congress}",
            f"- Roll calls sampled: {len(selected_rollcalls)}",
            f"- Member-vote rows: {len(out_rows)}",
            "- Vote coding: Voteview cast codes 1-3 as yea, 4-6 as nay; abstentions and absences omitted.",
        ],
    )
    return {"voteview_rows": len(out_rows), "voteview_rollcalls": len(selected_rollcalls)}


def action_flag(actions: list[dict[str, object]], needles: tuple[str, ...]) -> bool:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            return True
    return False


def action_count(actions: list[dict[str, object]], needles: tuple[str, ...]) -> int:
    count = 0
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            count += 1
    return count


def bill_refs(api_key: str, congress: int, page_limit: int, offsets: list[int]) -> list[BillRef]:
    refs: dict[str, BillRef] = {}
    for offset in offsets:
        payload = api_get(
            f"{CONGRESS_BASE}/bill/{congress}",
            {"api_key": api_key, "format": "json", "limit": page_limit, "offset": offset},
        )
        bills = payload.get("bills", [])
        if not isinstance(bills, list):
            continue
        for bill in bills:
            if not isinstance(bill, dict):
                continue
            bill_type = str(bill.get("type", "")).lower()
            number = str(bill.get("number", ""))
            if not bill_type or not number:
                continue
            ref = BillRef(congress, bill_type, number)
            refs[ref.bill_id] = ref
    return list(refs.values())


def sponsor(detail: dict[str, object]) -> tuple[str, str]:
    sponsors = detail.get("sponsors") or []
    if isinstance(sponsors, list) and sponsors and isinstance(sponsors[0], dict):
        row = sponsors[0]
        return (str(row.get("bioguideId") or row.get("fullName") or "unknown"), str(row.get("party") or "unknown"))
    return ("unknown", "unknown")


def policy_area(detail: dict[str, object]) -> str:
    area = detail.get("policyArea")
    if isinstance(area, dict):
        return str(area.get("name") or "Unclassified")
    return "Unclassified"


def fetch_committees(api_key: str, ref: BillRef) -> list[dict[str, object]]:
    payload = api_get(
        f"{CONGRESS_BASE}/bill/{ref.congress}/{ref.bill_type}/{ref.number}/committees",
        {"api_key": api_key, "format": "json", "limit": 250},
    )
    committees = payload.get("committees", [])
    return committees if isinstance(committees, list) else []


def build_congress_derived(
        api_key: str,
        congress: int,
        page_limit: int,
        offsets: list[int],
        sleep_seconds: float,
        preserve_bill_progression: bool,
) -> dict[str, int]:
    refs = bill_refs(api_key, congress, page_limit, offsets)
    bill_rows: list[dict[str, object]] = []
    topic_counts: dict[str, dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "floor_considered": 0,
        "enacted": 0,
    })
    sponsor_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "enacted": 0,
    })
    committee_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {
        "referred": 0,
        "hearings": 0,
        "reported": 0,
        "amendments": 0,
        "discharged": 0,
    })

    for ref in refs:
        detail_payload = api_get(
            f"{CONGRESS_BASE}/bill/{ref.congress}/{ref.bill_type}/{ref.number}",
            {"api_key": api_key, "format": "json"},
        )
        detail = detail_payload.get("bill", {})
        if not isinstance(detail, dict):
            detail = {}
        actions_payload = api_get(
            f"{CONGRESS_BASE}/bill/{ref.congress}/{ref.bill_type}/{ref.number}/actions",
            {"api_key": api_key, "format": "json", "limit": 250},
        )
        actions = actions_payload.get("actions", [])
        if not isinstance(actions, list):
            actions = []
        committees = fetch_committees(api_key, ref)

        committee_reported = action_flag(actions, (
            "reported by",
            "reported to",
            "ordered to be reported",
            "committee discharged",
        ))
        floor_considered = action_flag(actions, (
            "passed house",
            "passed/agreed to in house",
            "passed senate",
            "passed/agreed to in senate",
            "considered under",
            "on motion to suspend the rules and pass",
            "cloture on the motion to proceed",
            "motion to proceed",
            "agreed to",
        ))
        enacted = action_flag(actions, ("became public law", "signed by president")) or bool(detail.get("laws"))
        area = policy_area(detail)
        sponsor_id, party = sponsor(detail)
        hearings = action_count(actions, ("hearing", "hearings"))
        amendments = action_count(actions, ("amendment", "amendments"))
        discharged = action_flag(actions, ("committee discharged", "discharge petition", "discharged from committee"))

        bill_rows.append({
            "bill_id": ref.bill_id,
            "introduced": "1",
            "committee_reported": "1" if committee_reported else "0",
            "floor_considered": "1" if floor_considered else "0",
            "enacted": "1" if enacted else "0",
            "congress": congress,
            "policy_area": area,
            "sponsor_id": sponsor_id,
            "sponsor_party": party,
            "committee_count": len(committees),
            "source_url": ref.detail_url,
        })
        topic_counts[area]["introduced"] += 1
        topic_counts[area]["floor_considered"] += int(floor_considered)
        topic_counts[area]["enacted"] += int(enacted)
        sponsor_counts[(sponsor_id, party)]["introduced"] += 1
        sponsor_counts[(sponsor_id, party)]["enacted"] += int(enacted)

        if committees:
            per_committee_amendments = max(0, round(amendments / len(committees)))
            for committee in committees:
                if not isinstance(committee, dict):
                    continue
                name = str(committee.get("name") or "Unknown committee")
                key = (name, area)
                committee_counts[key]["referred"] += 1
                committee_counts[key]["hearings"] += hearings
                committee_counts[key]["reported"] += int(committee_reported)
                committee_counts[key]["amendments"] += per_committee_amendments
                committee_counts[key]["discharged"] += int(discharged)
        else:
            key = ("No committee record", area)
            committee_counts[key]["referred"] += 1

        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    if not preserve_bill_progression:
        write_csv(
            RAW_DIR / "bill_progression.csv",
            [
                "bill_id",
                "introduced",
                "committee_reported",
                "floor_considered",
                "enacted",
                "congress",
                "policy_area",
                "sponsor_id",
                "sponsor_party",
                "committee_count",
                "source_url",
            ],
            bill_rows,
        )
    write_csv(
        RAW_DIR / "topic_throughput.csv",
        ["topic", "introduced", "floor_considered", "enacted"],
        [{"topic": topic, **counts} for topic, counts in sorted(topic_counts.items())],
    )
    write_csv(
        RAW_DIR / "sponsor_success.csv",
        ["sponsor_id", "party", "introduced", "enacted"],
        [
            {"sponsor_id": sponsor_id, "party": party, **counts}
            for (sponsor_id, party), counts in sorted(sponsor_counts.items())
        ],
    )
    write_csv(
        RAW_DIR / "committee_activity.csv",
        ["committee", "issue", "referred", "hearings", "reported", "amendments", "discharged"],
        [
            {"committee": committee, "issue": issue, **counts}
            for (committee, issue), counts in sorted(committee_counts.items())
        ],
    )
    introduced = len(bill_rows)
    floor = sum(int(row["floor_considered"]) for row in bill_rows)
    committee = sum(int(row["committee_reported"]) for row in bill_rows)
    enacted = sum(int(row["enacted"]) for row in bill_rows)
    write_metadata(
        RAW_DIR / "congress_derived.metadata.md",
        "Congress.gov Derived Raw Validation Samples",
        [
            "- Source: Congress.gov API v3 bill-list, bill-detail, action, and committee endpoints.",
            f"- Congress: {congress}",
            f"- List offsets: {','.join(str(offset) for offset in offsets)}",
            f"- Page limit per offset: {page_limit}",
            f"- Bill rows: {introduced}",
            f"- Topic rows: {len(topic_counts)}",
            f"- Sponsor rows: {len(sponsor_counts)}",
            f"- Committee rows: {len(committee_counts)}",
            f"- Bill progression CSV preserved from existing sample: {'yes' if preserve_bill_progression else 'no'}",
            f"- Committee reported share: {committee / introduced:.4f}" if introduced else "- Committee reported share: 0.0000",
            f"- Floor-considered share: {floor / introduced:.4f}" if introduced else "- Floor-considered share: 0.0000",
            f"- Enactment share: {enacted / introduced:.4f}" if introduced else "- Enactment share: 0.0000",
        ],
    )
    return {
        "congress_bill_rows": introduced,
        "congress_topic_rows": len(topic_counts),
        "congress_sponsor_rows": len(sponsor_counts),
        "congress_committee_rows": len(committee_counts),
    }


def bill_ref_from_row(row: dict[str, str]) -> BillRef | None:
    congress = row.get("congress", "").strip()
    bill_type = row.get("bill_type", "").strip().lower()
    number = row.get("bill_number", "").strip()
    if not congress or not bill_type or not number:
        bill_id = row.get("bill_id", "")
        parts = bill_id.split("-")
        if len(parts) >= 3:
            congress, bill_type, number = parts[0], parts[1], parts[2]
    try:
        return BillRef(int(congress), bill_type, number) if bill_type and number else None
    except ValueError:
        return None


def sponsor_from_detail(api_key: str, ref: BillRef) -> tuple[str, str]:
    detail_payload = api_get(
        f"{CONGRESS_BASE}/bill/{ref.congress}/{ref.bill_type}/{ref.number}",
        {"api_key": api_key, "format": "json"},
    )
    detail = detail_payload.get("bill", {})
    return sponsor(detail if isinstance(detail, dict) else {})


def build_congress_derived_from_existing(
        row_limit: int,
        api_key: str | None,
        sleep_seconds: float,
        sponsor_enrichment_limit: int,
        preserve_sponsor_success: bool,
) -> dict[str, int]:
    path = RAW_DIR / "bill_progression.csv"
    if not path.exists():
        raise SystemExit("data/validation/raw/bill_progression.csv is required for --derive-congress-from-bill-progression.")
    data = read_csv(path)[:row_limit]
    preserved_sponsor_rows = 0
    if preserve_sponsor_success:
        sponsor_path = RAW_DIR / "sponsor_success.csv"
        if sponsor_path.exists():
            preserved_sponsor_rows = len(read_csv(sponsor_path))
    topic_counts: dict[str, dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "floor_considered": 0,
        "enacted": 0,
    })
    sponsor_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "enacted": 0,
    })
    committee_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {
        "referred": 0,
        "hearings": 0,
        "reported": 0,
        "amendments": 0,
        "discharged": 0,
    })
    sponsor_cache: dict[str, tuple[str, str]] = {}
    api_enriched = 0
    for row_index, row in enumerate(data):
        topic = row.get("policy_area") or row.get("issue") or "Unclassified"
        party = row.get("sponsor_party") or row.get("party") or "unknown"
        sponsor = row.get("sponsor_id") or f"party:{party}"
        ref = bill_ref_from_row(row)
        if (
                not preserve_sponsor_success
                and api_key
                and ref is not None
                and row_index < sponsor_enrichment_limit
        ):
            try:
                enriched = sponsor_cache.get(ref.bill_id)
                if enriched is None:
                    enriched = sponsor_from_detail(api_key, ref)
                    sponsor_cache[ref.bill_id] = enriched
                    if sleep_seconds > 0.0:
                        time.sleep(sleep_seconds)
                if enriched[0] != "unknown":
                    sponsor, party = enriched
                    api_enriched += 1
            except (HTTPError, TimeoutError, URLError):
                pass
        floor_considered = truthy(row.get("floor_considered", ""))
        enacted = truthy(row.get("enacted", ""))
        reported = truthy(row.get("committee_reported", ""))
        introduced = truthy(row.get("introduced", "1"))
        if not introduced:
            continue
        topic_counts[topic]["introduced"] += 1
        topic_counts[topic]["floor_considered"] += int(floor_considered)
        topic_counts[topic]["enacted"] += int(enacted)
        if not preserve_sponsor_success:
            sponsor_counts[(sponsor, party)]["introduced"] += 1
            sponsor_counts[(sponsor, party)]["enacted"] += int(enacted)
        committee_counts[("Bill-action committee signal", topic)]["referred"] += 1
        committee_counts[("Bill-action committee signal", topic)]["reported"] += int(reported)

    write_csv(
        RAW_DIR / "topic_throughput.csv",
        ["topic", "introduced", "floor_considered", "enacted"],
        [{"topic": topic, **counts} for topic, counts in sorted(topic_counts.items())],
    )
    if not preserve_sponsor_success:
        write_csv(
            RAW_DIR / "sponsor_success.csv",
            ["sponsor_id", "party", "introduced", "enacted"],
            [
                {"sponsor_id": sponsor_id, "party": party, **counts}
                for (sponsor_id, party), counts in sorted(sponsor_counts.items())
            ],
        )
    write_csv(
        RAW_DIR / "committee_activity.csv",
        ["committee", "issue", "referred", "hearings", "reported", "amendments", "discharged"],
        [
            {"committee": committee, "issue": issue, **counts}
            for (committee, issue), counts in sorted(committee_counts.items())
        ],
    )
    write_metadata(
        RAW_DIR / "congress_derived.metadata.md",
        "Congress.gov Derived Raw Validation Samples",
        [
            "- Source: Existing Congress.gov bill progression/action sample.",
            f"- Input rows used: {len(data)}",
            f"- Topic rows: {len(topic_counts)}",
            f"- Sponsor rows: {'preserved existing file' if preserve_sponsor_success else len(sponsor_counts)}",
            f"- Committee rows: {len(committee_counts)}",
            f"- Sponsor IDs enriched from bill-detail endpoint: {api_enriched}",
            f"- Sponsor enrichment limit: {sponsor_enrichment_limit}",
            f"- Sponsor success CSV preserved from previous enriched sample: {'yes' if preserve_sponsor_success else 'no'}",
            "- Committee activity is derived from bill-action committee-report flags, not detailed committee hearing calendars.",
            "- Sponsor IDs fall back to party-coded groups when the bill progression sample lacks member identifiers.",
        ],
    )
    return {
        "congress_derived_input_rows": len(data),
        "congress_topic_rows": len(topic_counts),
        "congress_sponsor_rows": len(sponsor_counts) if not preserve_sponsor_success else preserved_sponsor_rows,
        "congress_committee_rows": len(committee_counts),
        "congress_sponsor_enriched_rows": api_enriched,
    }


def amount(row: dict[str, object]) -> float:
    for key in ("income", "expenses"):
        value = row.get(key)
        if value not in (None, ""):
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return 0.0


def build_lobbying(year: int, page_size: int, pages: int, sleep_seconds: float) -> dict[str, int]:
    rows: list[dict[str, object]] = []
    for page in range(1, pages + 1):
        payload = api_get(
            f"{LDA_BASE}/filings/",
            {
                "filing_year": year,
                "page": page,
                "page_size": page_size,
            },
        )
        filings = payload.get("results", [])
        if not isinstance(filings, list):
            continue
        for filing in filings:
            if not isinstance(filing, dict):
                continue
            client = filing.get("client")
            client_name = "unknown"
            if isinstance(client, dict):
                client_name = str(client.get("name") or "unknown")
            period = str(filing.get("filing_period") or "")
            spend = amount(filing)
            activities = filing.get("lobbying_activities") or []
            if not isinstance(activities, list) or not activities:
                rows.append({
                    "client": client_name,
                    "issue": "Uncoded",
                    "amount": f"{spend:.2f}",
                    "period": f"{year}-{period}",
                    "filing_uuid": filing.get("filing_uuid") or "",
                })
                continue
            for activity in activities:
                if not isinstance(activity, dict):
                    continue
                issue = str(activity.get("general_issue_code_display") or activity.get("general_issue_code") or "Uncoded")
                rows.append({
                    "client": client_name,
                    "issue": issue,
                    "amount": f"{spend:.2f}",
                    "period": f"{year}-{period}",
                    "filing_uuid": filing.get("filing_uuid") or "",
                })
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    write_csv(
        RAW_DIR / "lobbying_disclosure.csv",
        ["client", "issue", "amount", "period", "filing_uuid"],
        rows,
    )
    clients = {row["client"] for row in rows}
    issues = {row["issue"] for row in rows}
    write_metadata(
        RAW_DIR / "lobbying_disclosure.metadata.md",
        "Senate LDA Lobbying Disclosure Raw Validation Sample",
        [
            "- Source: U.S. Senate Lobbying Disclosure Act API filing endpoint.",
            f"- Filing year: {year}",
            f"- Pages sampled: {pages}",
            f"- Page size: {page_size}",
            f"- Activity rows: {len(rows)}",
            f"- Unique clients: {len(clients)}",
            f"- Unique issue labels: {len(issues)}",
            "- Amount uses disclosed income when available, otherwise expenses when available.",
        ],
    )
    return {"lobbying_rows": len(rows), "lobbying_clients": len(clients), "lobbying_issues": len(issues)}


def write_run_report(stats: dict[str, int]) -> None:
    lines = [
        "# Core Raw Validation Dataset Build",
        "",
        "This report records the current source-backed raw validation samples.",
        "",
        "| Output group | Count |",
        "| --- | ---: |",
    ]
    for key, value in stats.items():
        lines.append(f"| {key} | {value} |")
    Path("reports").mkdir(exist_ok=True)
    Path("reports/core-raw-validation-build.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=None, help="Optional .env containing CONGRESS_API_KEY.")
    parser.add_argument("--congress", type=int, default=118)
    parser.add_argument("--congress-page-limit", type=int, default=80)
    parser.add_argument("--congress-offsets", default="0,500,1500")
    parser.add_argument("--voteview-rollcall-limit", type=int, default=160)
    parser.add_argument("--lobbying-year", type=int, default=2024)
    parser.add_argument("--lobbying-page-size", type=int, default=100)
    parser.add_argument("--lobbying-pages", type=int, default=5)
    parser.add_argument("--sleep", type=float, default=0.03)
    parser.add_argument("--preserve-bill-progression", action="store_true", help="Do not overwrite an existing raw bill_progression.csv while deriving topic, sponsor, and committee samples.")
    parser.add_argument("--preserve-sponsor-success", action="store_true", help="Do not overwrite an existing raw sponsor_success.csv while deriving topic and committee samples.")
    parser.add_argument("--derive-congress-from-bill-progression", action="store_true", help="Build topic, sponsor, and committee raw samples from the existing bill_progression.csv instead of calling per-bill Congress.gov endpoints.")
    parser.add_argument("--derived-row-limit", type=int, default=1000)
    parser.add_argument("--sponsor-enrichment-limit", type=int, default=40)
    parser.add_argument("--skip-voteview", action="store_true")
    parser.add_argument("--skip-congress", action="store_true")
    parser.add_argument("--skip-lobbying", action="store_true")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    values = env_values(args.env_file)
    congress_key = values.get("CONGRESS_API_KEY")
    stats: dict[str, int] = {}

    if not args.skip_voteview:
        stats.update(build_voteview(args.congress, args.voteview_rollcall_limit))
        print(f"Wrote Voteview sample: {stats['voteview_rows']} member-vote rows.", flush=True)
    if not args.skip_congress:
        if args.derive_congress_from_bill_progression:
            stats.update(build_congress_derived_from_existing(
                args.derived_row_limit,
                congress_key,
                args.sleep,
                args.sponsor_enrichment_limit,
                args.preserve_sponsor_success,
            ))
        elif not congress_key:
            raise SystemExit("CONGRESS_API_KEY is required for Congress.gov raw validation samples.")
        else:
            stats.update(build_congress_derived(
                congress_key,
                args.congress,
                args.congress_page_limit,
                parse_offsets(args.congress_offsets),
                args.sleep,
                args.preserve_bill_progression,
            ))
        print(
            "Wrote Congress.gov derived samples: "
            f"{stats['congress_topic_rows']} topics, "
            f"{stats['congress_sponsor_rows']} sponsors, "
            f"{stats['congress_committee_rows']} committee rows.",
            flush=True,
        )
    if not args.skip_lobbying:
        stats.update(build_lobbying(args.lobbying_year, args.lobbying_page_size, args.lobbying_pages, args.sleep))
        print(f"Wrote LDA lobbying sample: {stats['lobbying_rows']} activity rows.", flush=True)

    write_run_report(stats)
    print("Wrote core raw validation datasets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
