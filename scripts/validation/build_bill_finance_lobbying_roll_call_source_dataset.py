#!/usr/bin/env python3
"""Build official roll-call source rows for finance/lobbying queue bills."""

from __future__ import annotations

import argparse
import csv
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


COMMITTEE_ACTION_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-committee-action-source-review.csv"
)
OUT_CSV = Path("data/validation/raw/bill_finance_lobbying_roll_call_source.csv")
OUT_METADATA = Path("data/validation/raw/bill_finance_lobbying_roll_call_source.metadata.md")
HOUSE_CLERK_BASE_URL = "https://clerk.house.gov/evs"

FIELDNAMES = [
    "roll_call_source_rank",
    "source_review_rank",
    "context_rank",
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "roll_call_reference_status",
    "roll_call_reference_count",
    "roll_call_references",
    "floor_action_record_status",
    "floor_action_count",
    "roll_call_source_review_status",
    "chamber",
    "vote_year",
    "roll_call_number",
    "official_vote_source_url",
    "source_fetch_status",
    "official_congress",
    "official_session",
    "official_chamber",
    "official_legis_num",
    "official_vote_question",
    "official_vote_type",
    "official_vote_result",
    "official_action_date",
    "official_action_time",
    "official_vote_desc",
    "official_yea_total",
    "official_nay_total",
    "official_present_total",
    "official_not_voting_total",
    "official_party_totals",
    "member_vote_count",
    "source_bill_match_status",
    "floor_action_vote_mode_status",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bill finance/lobbying roll-call source review only; rows cache official "
    "House Clerk roll-call metadata and member-vote row counts when govinfo "
    "BILLSTATUS action text exposes a numbered House roll call, or classify "
    "floor actions without a numbered roll-call reference. The artifact provides "
    "vote-source context, not member-position influence, lobbying contact "
    "confirmation, campaign-finance target evidence, roll-call influence, "
    "legislative-outcome causality, public benefit, welfare, causal capture, or "
    "model validation."
)

MISSING_LINKS = "; ".join([
    "lobbying_contact_or_target_source",
    "external_campaign_target_source_document",
    "reviewed_outside_spending_target_beyond_candidate_id",
    "member_level_vote_target_join_to_finance_lobbying_source",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

ROLL_CALL_PATTERN = re.compile(r"Roll no\.?\s*(\d+)", re.IGNORECASE)
DATE_PATTERN = re.compile(r"\b(20\d{2})-\d{2}-\d{2}\b")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def clean(value: str | None) -> str:
    return " ".join((value or "").split())


def split_values(value: str | None) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        cleaned = clean(part)
        if cleaned and cleaned not in values:
            values.append(cleaned)
    return values


def join_values(values: list[str]) -> str:
    result: list[str] = []
    for value in values:
        cleaned = clean(value)
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return "; ".join(result)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(element: ET.Element | None, name: str) -> list[ET.Element]:
    if element is None:
        return []
    return [child for child in element if local_name(child.tag) == name]


def child(element: ET.Element | None, name: str) -> ET.Element | None:
    if element is None:
        return None
    for candidate in element:
        if local_name(candidate.tag) == name:
            return candidate
    return None


def text_at(element: ET.Element | None, *path: str) -> str:
    current = element
    for part in path:
        current = child(current, part)
        if current is None:
            return ""
    return clean(current.text)


def clerk_url(year: str, roll_number: str) -> str:
    return f"{HOUSE_CLERK_BASE_URL}/{year}/roll{parse_int(roll_number):03d}.xml"


def fetch_xml(url: str, timeout: float) -> ET.Element:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/finance-lobbying-roll-call-review"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return ET.fromstring(response.read())


def find_roll_call_actions(row: dict[str, str]) -> list[tuple[str, str]]:
    refs = [ROLL_CALL_PATTERN.search(value) for value in split_values(row.get("roll_call_references"))]
    roll_numbers = [match.group(1) for match in refs if match]
    snippets = split_values(row.get("floor_action_snippets"))
    results: list[tuple[str, str]] = []
    for roll_number in roll_numbers:
        year = ""
        for snippet in snippets:
            if f"Roll no. {roll_number}" in snippet or f"Roll No. {roll_number}" in snippet:
                date_match = DATE_PATTERN.search(snippet)
                if date_match:
                    year = date_match.group(1)
                    break
        if not year:
            for snippet in snippets:
                date_match = DATE_PATTERN.search(snippet)
                if date_match:
                    year = date_match.group(1)
                    break
        results.append((year, roll_number))
    return results


def expected_legis_num(bill_id: str) -> str:
    parts = bill_id.split("-")
    if len(parts) != 3:
        return ""
    _congress, bill_type, number = parts
    if bill_type == "hr":
        return f"H R {parse_int(number)}"
    if bill_type == "s":
        return f"S {parse_int(number)}"
    return f"{bill_type.upper()} {parse_int(number)}"


def party_totals(metadata: ET.Element | None) -> str:
    totals: list[str] = []
    for row in children(child(metadata, "vote-totals"), "totals-by-party"):
        party = text_at(row, "party")
        if not party:
            continue
        totals.append(
            f"{party}: yea={text_at(row, 'yea-total')}, nay={text_at(row, 'nay-total')}, "
            f"present={text_at(row, 'present-total')}, not_voting={text_at(row, 'not-voting-total')}"
        )
    return "; ".join(totals)


def build_vote_row(context: dict[str, str], year: str, roll_number: str, root: ET.Element, url: str) -> dict[str, str]:
    metadata = child(root, "vote-metadata")
    totals = child(child(metadata, "vote-totals"), "totals-by-vote")
    official_legis = text_at(metadata, "legis-num")
    expected_legis = expected_legis_num(context.get("bill_id", ""))
    return {
        "roll_call_source_rank": "",
        "source_review_rank": context.get("source_review_rank", ""),
        "context_rank": context.get("context_rank", ""),
        "review_rank": context.get("review_rank", ""),
        "bill_id": context.get("bill_id", ""),
        "public_law_number": context.get("public_law_number", ""),
        "policy_area": context.get("policy_area", ""),
        "roll_call_reference_status": context.get("roll_call_reference_status", ""),
        "roll_call_reference_count": context.get("roll_call_reference_count", ""),
        "roll_call_references": context.get("roll_call_references", ""),
        "floor_action_record_status": context.get("floor_action_record_status", ""),
        "floor_action_count": context.get("floor_action_count", ""),
        "roll_call_source_review_status": "official_house_clerk_roll_call_source_reviewed",
        "chamber": "House",
        "vote_year": year,
        "roll_call_number": str(parse_int(roll_number)),
        "official_vote_source_url": url,
        "source_fetch_status": "official_house_clerk_roll_call_xml_fetched",
        "official_congress": text_at(metadata, "congress"),
        "official_session": text_at(metadata, "session"),
        "official_chamber": text_at(metadata, "chamber"),
        "official_legis_num": official_legis,
        "official_vote_question": text_at(metadata, "vote-question"),
        "official_vote_type": text_at(metadata, "vote-type"),
        "official_vote_result": text_at(metadata, "vote-result"),
        "official_action_date": text_at(metadata, "action-date"),
        "official_action_time": text_at(metadata, "action-time"),
        "official_vote_desc": text_at(metadata, "vote-desc"),
        "official_yea_total": text_at(totals, "yea-total"),
        "official_nay_total": text_at(totals, "nay-total"),
        "official_present_total": text_at(totals, "present-total"),
        "official_not_voting_total": text_at(totals, "not-voting-total"),
        "official_party_totals": party_totals(metadata),
        "member_vote_count": str(len(children(child(root, "vote-data"), "recorded-vote"))),
        "source_bill_match_status": (
            "official_vote_legis_num_matches_bill_id"
            if clean(official_legis).casefold() == expected_legis.casefold()
            else "official_vote_legis_num_mismatch_needs_manual_review"
        ),
        "floor_action_vote_mode_status": "numbered_house_roll_call_vote_source_reviewed",
        "evidence_layers": (
            "bill_finance_lobbying_committee_action_source_review; "
            "official_house_clerk_roll_call_source"
        ),
        "missing_links": MISSING_LINKS,
        "source_url": url,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def error_vote_row(
    context: dict[str, str],
    year: str,
    roll_number: str,
    url: str,
    message: str,
) -> dict[str, str]:
    row = no_numbered_roll_call_row(context)
    row.update({
        "roll_call_source_review_status": "official_house_clerk_roll_call_source_unavailable",
        "chamber": "House",
        "vote_year": year,
        "roll_call_number": str(parse_int(roll_number)),
        "official_vote_source_url": url,
        "source_fetch_status": "official_house_clerk_roll_call_fetch_error",
        "official_vote_desc": clean(message)[:500],
        "floor_action_vote_mode_status": "numbered_house_roll_call_reference_needs_source_followup",
        "source_url": url,
    })
    return row


def no_numbered_roll_call_row(context: dict[str, str]) -> dict[str, str]:
    return {
        "roll_call_source_rank": "",
        "source_review_rank": context.get("source_review_rank", ""),
        "context_rank": context.get("context_rank", ""),
        "review_rank": context.get("review_rank", ""),
        "bill_id": context.get("bill_id", ""),
        "public_law_number": context.get("public_law_number", ""),
        "policy_area": context.get("policy_area", ""),
        "roll_call_reference_status": context.get("roll_call_reference_status", ""),
        "roll_call_reference_count": context.get("roll_call_reference_count", ""),
        "roll_call_references": context.get("roll_call_references", ""),
        "floor_action_record_status": context.get("floor_action_record_status", ""),
        "floor_action_count": context.get("floor_action_count", ""),
        "roll_call_source_review_status": "official_floor_action_reviewed_without_numbered_roll_call",
        "chamber": "",
        "vote_year": "",
        "roll_call_number": "",
        "official_vote_source_url": "",
        "source_fetch_status": "not_applicable_no_numbered_roll_call_reference",
        "official_congress": "",
        "official_session": "",
        "official_chamber": "",
        "official_legis_num": "",
        "official_vote_question": "",
        "official_vote_type": "",
        "official_vote_result": "",
        "official_action_date": "",
        "official_action_time": "",
        "official_vote_desc": "",
        "official_yea_total": "",
        "official_nay_total": "",
        "official_present_total": "",
        "official_not_voting_total": "",
        "official_party_totals": "",
        "member_vote_count": "0",
        "source_bill_match_status": "not_applicable_no_numbered_roll_call_reference",
        "floor_action_vote_mode_status": "floor_actions_reviewed_as_voice_vote_or_unanimous_consent_no_numbered_roll_call",
        "evidence_layers": "bill_finance_lobbying_committee_action_source_review",
        "missing_links": MISSING_LINKS,
        "source_url": context.get("govinfo_url", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    source_rows = sorted(read_csv(args.input_csv), key=lambda row: parse_int(row.get("source_review_rank")))
    selected = source_rows[:args.limit] if args.limit and args.limit > 0 else source_rows
    rows: list[dict[str, str]] = []
    for index, context in enumerate(selected, start=1):
        roll_refs = find_roll_call_actions(context)
        if not roll_refs:
            rows.append(no_numbered_roll_call_row(context))
        for year, roll_number in roll_refs:
            url = clerk_url(year, roll_number) if year else ""
            if not url:
                rows.append(error_vote_row(context, year, roll_number, url, "missing roll-call action year"))
                continue
            try:
                root = fetch_xml(url, args.timeout)
                rows.append(build_vote_row(context, year, roll_number, root, url))
            except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as exception:
                rows.append(error_vote_row(context, year, roll_number, url, str(exception)))
            if args.sleep > 0:
                time.sleep(args.sleep)
        if args.progress_every and index % args.progress_every == 0:
            print(f"Reviewed {index} / {len(selected)} bill-finance/lobbying roll-call source rows")
    for index, row in enumerate(rows, start=1):
        row["roll_call_source_rank"] = str(index)
    return rows


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["roll_call_source_review_status"] for row in rows)
    fetched = [
        row for row in rows
        if row["source_fetch_status"] == "official_house_clerk_roll_call_xml_fetched"
    ]
    no_numbered = [
        row for row in rows
        if row["roll_call_source_review_status"] == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    args.metadata.write_text(
        "# Bill Finance/Lobbying Roll-Call Source Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- Input source review: `{args.input_csv}`.\n"
        f"- House Clerk XML pattern: `{HOUSE_CLERK_BASE_URL}/<year>/roll<roll-number>.xml`.\n\n"
        "Rows:\n\n"
        f"- Source-review rows inspected: {len(rows)}.\n"
        f"- Official House Clerk roll-call XML rows fetched: {len(fetched)}.\n"
        f"- Floor-action rows without numbered roll-call references: {len(no_numbered)}.\n"
        f"- Member vote rows represented: {sum(parse_int(row.get('member_vote_count')) for row in rows)}.\n\n"
        "Status counts:\n\n"
        f"{status_lines}\n\n"
        f"Claim boundary: {CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=COMMITTEE_ACTION_SOURCE_REVIEW)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--progress-every", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = build_rows(args)
    if not rows:
        raise SystemExit("No bill-finance/lobbying roll-call source rows built.")
    write_csv(args.output, rows)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
