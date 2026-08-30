#!/usr/bin/env python3
"""Build a bounded govinfo BILLSTATUS cross-check for cached bill rows."""

from __future__ import annotations

import argparse
import csv
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


BILL_PROGRESSION = Path("data/validation/raw/bill_progression.csv")
OUT_CSV = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
OUT_METADATA = Path("data/validation/raw/govinfo_billstatus_linkage.metadata.md")
BASE_URL = "https://www.govinfo.gov/bulkdata/BILLSTATUS"

FIELDNAMES = [
    "bill_id",
    "congress",
    "bill_type",
    "bill_number",
    "linkage_status",
    "introduced_date",
    "latest_action_date",
    "latest_action_text",
    "actions_count",
    "policy_area",
    "title",
    "committees",
    "subjects",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "sponsor_district",
    "committee_reported",
    "floor_considered",
    "enacted",
    "bill_progression_introduced",
    "bill_progression_committee_reported",
    "bill_progression_floor_considered",
    "bill_progression_enacted",
    "bill_progression_policy_area",
    "action_alignment_status",
    "policy_area_alignment_status",
    "evidence_layers",
    "missing_links",
    "source_url",
    "govinfo_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded govinfo BILLSTATUS to Congress.gov bill-sample cross-check only; "
    "not a full bill census, public-opinion evidence, lobbying or campaign-finance "
    "influence, implementation or court outcome linkage, public benefit, welfare, "
    "or model validation."
)

COMMITTEE_NEEDLES = (
    "reported by",
    "reported to",
    "ordered to be reported",
    "committee discharged",
    "committee report",
)
FLOOR_NEEDLES = (
    "passed/agreed to in house",
    "passed/agreed to in senate",
    "passed house",
    "passed senate",
    "on motion to suspend",
    "motion to proceed to measure considered",
    "considered under",
    "considered in senate",
    "agreed to without objection",
    "agreed to by",
)
ENACTED_NEEDLES = (
    "became public law",
    "signed by president",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(element: ET.Element | None, name: str) -> ET.Element | None:
    if element is None:
        return None
    for candidate in element:
        if local_name(candidate.tag) == name:
            return candidate
    return None


def children(element: ET.Element | None, name: str) -> list[ET.Element]:
    if element is None:
        return []
    return [candidate for candidate in element if local_name(candidate.tag) == name]


def at(element: ET.Element | None, *path: str) -> ET.Element | None:
    current = element
    for part in path:
        current = child(current, part)
        if current is None:
            return None
    return current


def text_at(element: ET.Element | None, *path: str) -> str:
    found = at(element, *path)
    if found is None or found.text is None:
        return ""
    return " ".join(found.text.split())


def item_texts(element: ET.Element | None, *path: str) -> list[str]:
    parent = at(element, *path)
    values: list[str] = []
    for item in children(parent, "item"):
        value = " ".join(" ".join(item.itertext()).split())
        if value:
            values.append(value)
    return values


def billstatus_url(congress: str, bill_type: str, bill_number: str) -> str:
    normalized_type = bill_type.strip().lower()
    return (
        f"{BASE_URL}/{congress.strip()}/{normalized_type}/"
        f"BILLSTATUS-{congress.strip()}{normalized_type}{bill_number.strip()}.xml"
    )


def fetch_xml(url: str, timeout: float) -> ET.Element:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CongressInstitutionalSimulator/empirical-boundary-check"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return ET.fromstring(response.read())


def action_items(bill: ET.Element) -> list[ET.Element]:
    return children(at(bill, "actions"), "item")


def action_text(action: ET.Element) -> str:
    pieces = [
        text_at(action, "actionDate"),
        text_at(action, "type"),
        text_at(action, "text"),
    ]
    return " ".join(piece for piece in pieces if piece)


def latest_action(actions: list[ET.Element]) -> tuple[str, str]:
    dated: list[tuple[str, int, ET.Element]] = []
    for index, action in enumerate(actions):
        action_date = text_at(action, "actionDate")
        if action_date:
            dated.append((action_date, index, action))
    if not dated:
        return "", ""
    _, _, latest = max(dated, key=lambda item: (item[0], item[1]))
    return text_at(latest, "actionDate"), text_at(latest, "text")


def has_action(actions: list[ET.Element], needles: tuple[str, ...]) -> bool:
    haystack = "\n".join(action_text(action).casefold() for action in actions)
    return any(needle in haystack for needle in needles)


def flag(value: bool) -> str:
    return "1" if value else "0"


def boolish(value: str) -> bool:
    return (value or "").strip() == "1"


def normalized(value: str) -> str:
    return " ".join((value or "").split()).casefold()


def alignment_status(row: dict[str, str], committee: bool, floor: bool, enacted: bool) -> str:
    expected = (
        boolish(row.get("committee_reported", "")),
        boolish(row.get("floor_considered", "")),
        boolish(row.get("enacted", "")),
    )
    actual = (committee, floor, enacted)
    return "aligned" if expected == actual else "flag_difference"


def policy_alignment(row: dict[str, str], policy_area: str) -> str:
    expected = normalized(row.get("policy_area", ""))
    actual = normalized(policy_area)
    if not expected or not actual:
        return "unavailable"
    return "aligned" if expected == actual else "different"


def evidence_layers(action_alignment: str, policy_status: str) -> str:
    layers = ["govinfo_billstatus_metadata", "bill_progression_sample_overlap"]
    if action_alignment == "aligned":
        layers.append("action_flag_alignment")
    if policy_status == "aligned":
        layers.append("policy_area_alignment")
    return "; ".join(layers)


def missing_links() -> str:
    return "; ".join([
        "full_congress_census",
        "district_public_opinion",
        "campaign_finance_or_lobbying_to_bill",
        "implementation_or_court_outcomes",
        "model_validation",
    ])


def error_row(row: dict[str, str], status: str, url: str, message: str) -> dict[str, str]:
    return {
        "bill_id": row.get("bill_id", ""),
        "congress": row.get("congress", ""),
        "bill_type": row.get("bill_type", ""),
        "bill_number": row.get("bill_number", ""),
        "linkage_status": status,
        "introduced_date": "",
        "latest_action_date": "",
        "latest_action_text": message[:500],
        "actions_count": "0",
        "policy_area": "",
        "title": "",
        "committees": "",
        "subjects": "",
        "sponsor_bioguide_id": "",
        "sponsor_party": "",
        "sponsor_state": "",
        "sponsor_district": "",
        "committee_reported": "",
        "floor_considered": "",
        "enacted": "",
        "bill_progression_introduced": row.get("introduced", ""),
        "bill_progression_committee_reported": row.get("committee_reported", ""),
        "bill_progression_floor_considered": row.get("floor_considered", ""),
        "bill_progression_enacted": row.get("enacted", ""),
        "bill_progression_policy_area": row.get("policy_area", ""),
        "action_alignment_status": "unavailable",
        "policy_area_alignment_status": "unavailable",
        "evidence_layers": "bill_progression_sample_overlap",
        "missing_links": "govinfo_billstatus_metadata; " + missing_links(),
        "source_url": row.get("source_url", ""),
        "govinfo_url": url,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_row(row: dict[str, str], root: ET.Element, url: str) -> dict[str, str]:
    bill = at(root, "bill")
    if bill is None:
        return error_row(row, "govinfo_parse_error", url, "missing bill element")

    congress = text_at(bill, "congress")
    bill_type = text_at(bill, "type").lower()
    bill_number = text_at(bill, "number")
    input_key = (row.get("congress", ""), row.get("bill_type", ""), row.get("bill_number", ""))
    govinfo_key = (congress, bill_type, bill_number)
    status = "govinfo_billstatus_metadata" if input_key == govinfo_key else "govinfo_identifier_mismatch"

    actions = action_items(bill)
    latest_date, latest_text = latest_action(actions)
    committee = has_action(actions, COMMITTEE_NEEDLES)
    floor = has_action(actions, FLOOR_NEEDLES)
    laws = children(at(bill, "laws"), "item")
    enacted = has_action(actions, ENACTED_NEEDLES) or bool(laws)
    policy_area = text_at(bill, "policyArea", "name")
    action_status = alignment_status(row, committee, floor, enacted) if status == "govinfo_billstatus_metadata" else "unavailable"
    policy_status = policy_alignment(row, policy_area) if status == "govinfo_billstatus_metadata" else "unavailable"
    sponsors = children(at(bill, "sponsors"), "item")
    sponsor = sponsors[0] if sponsors else None

    return {
        "bill_id": row.get("bill_id", ""),
        "congress": row.get("congress", ""),
        "bill_type": row.get("bill_type", ""),
        "bill_number": row.get("bill_number", ""),
        "linkage_status": status,
        "introduced_date": text_at(bill, "introducedDate"),
        "latest_action_date": latest_date,
        "latest_action_text": latest_text,
        "actions_count": str(len(actions)),
        "policy_area": policy_area,
        "title": text_at(bill, "title"),
        "committees": "; ".join(item_texts(bill, "committees")),
        "subjects": "; ".join(item_texts(bill, "subjects", "legislativeSubjects")),
        "sponsor_bioguide_id": text_at(sponsor, "bioguideId"),
        "sponsor_party": text_at(sponsor, "party"),
        "sponsor_state": text_at(sponsor, "state"),
        "sponsor_district": text_at(sponsor, "district"),
        "committee_reported": flag(committee),
        "floor_considered": flag(floor),
        "enacted": flag(enacted),
        "bill_progression_introduced": row.get("introduced", ""),
        "bill_progression_committee_reported": row.get("committee_reported", ""),
        "bill_progression_floor_considered": row.get("floor_considered", ""),
        "bill_progression_enacted": row.get("enacted", ""),
        "bill_progression_policy_area": row.get("policy_area", ""),
        "action_alignment_status": action_status,
        "policy_area_alignment_status": policy_status,
        "evidence_layers": evidence_layers(action_status, policy_status) if status == "govinfo_billstatus_metadata" else "bill_progression_sample_overlap",
        "missing_links": missing_links(),
        "source_url": row.get("source_url", ""),
        "govinfo_url": url,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_rows(args: argparse.Namespace, bill_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = bill_rows[:args.limit] if args.limit and args.limit > 0 else bill_rows
    rows: list[dict[str, str]] = []
    for index, row in enumerate(selected, start=1):
        url = billstatus_url(row.get("congress", ""), row.get("bill_type", ""), row.get("bill_number", ""))
        try:
            root = fetch_xml(url, args.timeout)
            rows.append(build_row(row, root, url))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as exception:
            rows.append(error_row(row, "govinfo_fetch_error", url, str(exception)))
        if args.progress_every and index % args.progress_every == 0:
            print(f"Fetched {index} / {len(selected)} govinfo BILLSTATUS rows")
        if args.sleep > 0:
            time.sleep(args.sleep)
    return rows


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    metadata_rows = [
        row for row in rows
        if row["linkage_status"] == "govinfo_billstatus_metadata"
    ]
    aligned_rows = [
        row for row in metadata_rows
        if row["action_alignment_status"] == "aligned"
    ]
    policy_rows = [
        row for row in metadata_rows
        if row["policy_area_alignment_status"] == "aligned"
    ]
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    args.metadata.write_text(
        "# govinfo BILLSTATUS Linkage Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- Input bill sample: `{args.bill_progression_csv}`.\n"
        f"- govinfo BILLSTATUS bulk XML URL pattern: `{BASE_URL}/<congress>/<bill_type>/BILLSTATUS-<congress><bill_type><bill_number>.xml`.\n"
        "- govinfo BILLSTATUS feature page: `https://www.govinfo.gov/features/bill-status-xml-bulk-data`.\n\n"
        "Transformation:\n\n"
        "- Fetches one public govinfo BILLSTATUS XML record per cached bill-progression row.\n"
        "- Joins records only by congress, bill type, and bill number.\n"
        "- Extracts bill identifiers, titles, policy area, actions, committees, subjects, sponsor metadata, and coarse action-stage flags.\n"
        "- Compares coarse govinfo action flags and policy area to the cached Congress.gov bill-progression sample.\n\n"
        "Rows:\n\n"
        f"- Bill rows inspected: {len(rows)}.\n"
        f"- Rows with govinfo BILLSTATUS metadata: {len(metadata_rows)}.\n"
        f"- Rows with aligned coarse action flags: {len(aligned_rows)}.\n"
        f"- Rows with aligned policy area: {len(policy_rows)}.\n\n"
        "Rows by linkage status:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bill-progression-csv", type=Path, default=BILL_PROGRESSION)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int, default=0, help="Maximum bills to fetch; 0 means all rows.")
    parser.add_argument("--sleep", type=float, default=0.02, help="Seconds to sleep between govinfo requests.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds.")
    parser.add_argument("--progress-every", type=int, default=25)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.bill_progression_csv.exists():
        raise SystemExit(f"{args.bill_progression_csv} is missing; run make build-bill-progression-raw first.")
    bill_rows = read_csv(args.bill_progression_csv)
    if not bill_rows:
        raise SystemExit(f"{args.bill_progression_csv} is empty.")
    rows = build_rows(args, bill_rows)
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
