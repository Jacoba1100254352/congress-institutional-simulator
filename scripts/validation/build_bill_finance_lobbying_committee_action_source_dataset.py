#!/usr/bin/env python3
"""Build govinfo committee/action source rows for finance/lobbying queue bills."""

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


COMMITTEE_ACTION_CONTEXT = Path("reports/bill-finance-lobbying-committee-action-context.csv")
OUT_CSV = Path("data/validation/raw/bill_finance_lobbying_committee_action_source.csv")
OUT_METADATA = Path("data/validation/raw/bill_finance_lobbying_committee_action_source.metadata.md")
BASE_URL = "https://www.govinfo.gov/bulkdata/BILLSTATUS"

FIELDNAMES = [
    "source_review_rank",
    "context_rank",
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "govinfo_billstatus_status",
    "govinfo_url",
    "introduced_date",
    "latest_action_date",
    "latest_action_text",
    "actions_count",
    "committee_source_status",
    "committee_count",
    "committee_names",
    "committee_activity_count",
    "committee_activity_summary",
    "committee_report_count",
    "committee_report_citations",
    "committee_action_record_status",
    "committee_action_count",
    "committee_action_dates",
    "committee_action_snippets",
    "floor_action_record_status",
    "floor_action_count",
    "floor_action_dates",
    "floor_action_snippets",
    "roll_call_reference_status",
    "roll_call_reference_count",
    "roll_call_references",
    "legislative_outcome_source_status",
    "public_law_numbers",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "external_lda_mention_packets",
    "campaign_target_scope_status",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bill finance/lobbying committee/action source review only; rows cache official "
    "govinfo BILLSTATUS committee, action, roll-call-reference, and public-law "
    "outcome metadata for queued bills. The artifact provides committee/action "
    "source context, not lobbying contact confirmation, campaign-finance target "
    "evidence, committee-action influence, roll-call influence, legislative-outcome "
    "causality, public benefit, welfare, causal capture, or model validation."
)

MISSING_LINKS = "; ".join([
    "lobbying_contact_or_target_source",
    "external_campaign_target_source_document",
    "reviewed_outside_spending_target_beyond_candidate_id",
    "official_roll_call_vote_source_join",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

COMMITTEE_ACTION_NEEDLES = (
    "committee",
    "reported by",
    "reported to",
    "ordered to be reported",
    "discharged from",
    "markup",
)
FLOOR_ACTION_NEEDLES = (
    "passed/agreed to",
    "passed house",
    "passed senate",
    "considered",
    "on motion to suspend",
    "motion to proceed",
    "agreed to by",
)
ROLL_CALL_PATTERN = re.compile(
    r"(Roll No\.?\s*\d+|Record Vote Number:\s*\d+|Vote Number:\s*\d+|Yea-Nay Vote\.\s*\d+)",
    re.IGNORECASE,
)
PROCEDURAL_RULE_NEEDLES = (
    "rules committee resolution",
    "rule provides for consideration",
)


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


def clean(value: str) -> str:
    return " ".join((value or "").split())


def join_values(values: list[str] | set[str], *, limit: int | None = None) -> str:
    ordered: list[str] = []
    for value in values:
        cleaned = clean(str(value or ""))
        if cleaned and cleaned not in ordered:
            ordered.append(cleaned)
    if limit is not None:
        ordered = ordered[:limit]
    return "; ".join(ordered)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def bill_parts(bill_id: str) -> tuple[str, str, str]:
    parts = bill_id.split("-")
    if len(parts) != 3:
        raise SystemExit(f"invalid bill_id={bill_id}")
    return parts[0], parts[1], parts[2]


def billstatus_url(bill_id: str) -> str:
    congress, bill_type, number = bill_parts(bill_id)
    return f"{BASE_URL}/{congress}/{bill_type}/BILLSTATUS-{congress}{bill_type}{number}.xml"


def fetch_xml(url: str, timeout: float) -> ET.Element:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/finance-lobbying-source-review"},
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
    return clean(" ".join(piece for piece in pieces if piece))


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


def action_matches(action: ET.Element, needles: tuple[str, ...]) -> bool:
    text = action_text(action).casefold()
    return any(needle in text for needle in needles)


def is_procedural_rule_action(action: ET.Element) -> bool:
    text = action_text(action).casefold()
    return any(needle in text for needle in PROCEDURAL_RULE_NEEDLES)


def action_dates(actions: list[ET.Element]) -> list[str]:
    return [text_at(action, "actionDate") for action in actions if text_at(action, "actionDate")]


def action_snippets(actions: list[ET.Element], *, limit: int = 6) -> list[str]:
    snippets: list[str] = []
    for action in actions[:limit]:
        text = action_text(action)
        if len(text) > 280:
            text = text[:277].rstrip() + "..."
        snippets.append(text)
    return snippets


def committee_activity_items(committee: ET.Element) -> list[str]:
    activities: list[str] = []
    committee_name = text_at(committee, "name")
    chamber = text_at(committee, "chamber")
    for activity in children(at(committee, "activities"), "item"):
        name = text_at(activity, "name")
        date = text_at(activity, "date")[:10]
        activities.append(clean(f"{chamber} {committee_name}: {name} {date}"))
    for subcommittee in children(at(committee, "subcommittees"), "item"):
        sub_name = text_at(subcommittee, "name")
        for activity in children(at(subcommittee, "activities"), "item"):
            name = text_at(activity, "name")
            date = text_at(activity, "date")[:10]
            activities.append(clean(f"{chamber} {committee_name} / {sub_name}: {name} {date}"))
    return activities


def committee_names(committee_rows: list[ET.Element]) -> list[str]:
    names: list[str] = []
    for committee in committee_rows:
        chamber = text_at(committee, "chamber")
        name = text_at(committee, "name")
        if name:
            names.append(clean(f"{chamber} {name}"))
        for subcommittee in children(at(committee, "subcommittees"), "item"):
            sub_name = text_at(subcommittee, "name")
            if sub_name:
                names.append(clean(f"{chamber} {sub_name} Subcommittee"))
    return names


def committee_report_citations(bill: ET.Element) -> list[str]:
    citations: list[str] = []
    for report in children(at(bill, "committeeReports"), "committeeReport"):
        citation = text_at(report, "citation")
        if citation:
            citations.append(citation)
    return citations


def public_law_numbers(bill: ET.Element) -> list[str]:
    laws: list[str] = []
    for law in children(at(bill, "laws"), "item"):
        law_type = text_at(law, "type")
        law_number = text_at(law, "number")
        if law_type and law_number:
            laws.append(clean(f"{law_type} {law_number}"))
    return laws


def roll_call_refs(actions: list[ET.Element]) -> list[str]:
    refs: list[str] = []
    for action in actions:
        for match in ROLL_CALL_PATTERN.findall(action_text(action)):
            refs.append(clean(match))
    return refs


def status_from_count(count: int, present_status: str, missing_status: str) -> str:
    return present_status if count > 0 else missing_status


def error_row(context: dict[str, str], status: str, url: str, message: str) -> dict[str, str]:
    return {
        "source_review_rank": context.get("context_rank", ""),
        "context_rank": context.get("context_rank", ""),
        "review_rank": context.get("review_rank", ""),
        "bill_id": context.get("bill_id", ""),
        "public_law_number": context.get("public_law_number", ""),
        "policy_area": context.get("policy_area", ""),
        "govinfo_billstatus_status": status,
        "govinfo_url": url,
        "introduced_date": "",
        "latest_action_date": "",
        "latest_action_text": message[:500],
        "actions_count": "0",
        "committee_source_status": "govinfo_committee_source_unavailable",
        "committee_count": "0",
        "committee_names": "",
        "committee_activity_count": "0",
        "committee_activity_summary": "",
        "committee_report_count": "0",
        "committee_report_citations": "",
        "committee_action_record_status": "govinfo_committee_action_source_unavailable",
        "committee_action_count": "0",
        "committee_action_dates": "",
        "committee_action_snippets": "",
        "floor_action_record_status": "govinfo_floor_action_source_unavailable",
        "floor_action_count": "0",
        "floor_action_dates": "",
        "floor_action_snippets": "",
        "roll_call_reference_status": "govinfo_roll_call_reference_source_unavailable",
        "roll_call_reference_count": "0",
        "roll_call_references": "",
        "legislative_outcome_source_status": "govinfo_public_law_outcome_source_unavailable",
        "public_law_numbers": "",
        "sponsor_bioguide_id": "",
        "sponsor_party": "",
        "sponsor_state": "",
        "external_lda_mention_packets": context.get("external_lda_mention_packets", ""),
        "campaign_target_scope_status": context.get("campaign_target_scope_status", ""),
        "evidence_layers": "bill_finance_lobbying_committee_action_context",
        "missing_links": "govinfo_billstatus_committee_action_source; " + MISSING_LINKS,
        "source_url": url,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_row(context: dict[str, str], root: ET.Element, url: str) -> dict[str, str]:
    bill = at(root, "bill")
    if bill is None:
        return error_row(context, "govinfo_parse_error", url, "missing bill element")
    actions = action_items(bill)
    latest_date, latest_text = latest_action(actions)
    committees = children(at(bill, "committees"), "item")
    names = committee_names(committees)
    activity_summary: list[str] = []
    for committee in committees:
        activity_summary.extend(committee_activity_items(committee))
    reports = committee_report_citations(bill)
    committee_actions = [
        action for action in actions
        if action_matches(action, COMMITTEE_ACTION_NEEDLES)
        and not is_procedural_rule_action(action)
    ]
    floor_actions = [
        action for action in actions
        if action_matches(action, FLOOR_ACTION_NEEDLES)
    ]
    roll_refs = roll_call_refs(actions)
    laws = public_law_numbers(bill)
    sponsors = children(at(bill, "sponsors"), "item")
    sponsor = sponsors[0] if sponsors else None
    evidence_layers = [
        "bill_finance_lobbying_committee_action_context",
        "official_govinfo_billstatus_committee_source",
        "official_govinfo_billstatus_action_source",
    ]
    if reports:
        evidence_layers.append("official_committee_report_citation_metadata")
    if roll_refs:
        evidence_layers.append("official_billstatus_roll_call_reference")
    if laws:
        evidence_layers.append("official_govinfo_public_law_outcome_metadata")
    return {
        "source_review_rank": context.get("context_rank", ""),
        "context_rank": context.get("context_rank", ""),
        "review_rank": context.get("review_rank", ""),
        "bill_id": context.get("bill_id", ""),
        "public_law_number": context.get("public_law_number", ""),
        "policy_area": context.get("policy_area", ""),
        "govinfo_billstatus_status": "official_govinfo_billstatus_fetched",
        "govinfo_url": url,
        "introduced_date": text_at(bill, "introducedDate"),
        "latest_action_date": latest_date,
        "latest_action_text": latest_text,
        "actions_count": str(len(actions)),
        "committee_source_status": status_from_count(
            len(names),
            "official_govinfo_committee_names_present",
            "official_govinfo_billstatus_reviewed_without_direct_committee_names",
        ),
        "committee_count": str(len(names)),
        "committee_names": join_values(names),
        "committee_activity_count": str(len(activity_summary)),
        "committee_activity_summary": join_values(activity_summary, limit=12),
        "committee_report_count": str(len(reports)),
        "committee_report_citations": join_values(reports),
        "committee_action_record_status": status_from_count(
            len(committee_actions) + len(activity_summary),
            "official_govinfo_committee_action_records_present",
            "official_govinfo_billstatus_reviewed_without_direct_committee_action_records",
        ),
        "committee_action_count": str(len(committee_actions)),
        "committee_action_dates": join_values(action_dates(committee_actions)),
        "committee_action_snippets": join_values(action_snippets(committee_actions)),
        "floor_action_record_status": status_from_count(
            len(floor_actions),
            "official_govinfo_floor_action_records_present",
            "official_govinfo_billstatus_without_floor_action_records",
        ),
        "floor_action_count": str(len(floor_actions)),
        "floor_action_dates": join_values(action_dates(floor_actions)),
        "floor_action_snippets": join_values(action_snippets(floor_actions)),
        "roll_call_reference_status": status_from_count(
            len(roll_refs),
            "official_billstatus_roll_call_references_present",
            "official_billstatus_without_roll_call_references",
        ),
        "roll_call_reference_count": str(len(roll_refs)),
        "roll_call_references": join_values(roll_refs),
        "legislative_outcome_source_status": status_from_count(
            len(laws),
            "official_govinfo_public_law_outcome_metadata_present_no_finance_lobbying_causality",
            "official_govinfo_billstatus_without_public_law_outcome_metadata",
        ),
        "public_law_numbers": join_values(laws),
        "sponsor_bioguide_id": text_at(sponsor, "bioguideId"),
        "sponsor_party": text_at(sponsor, "party"),
        "sponsor_state": text_at(sponsor, "state"),
        "external_lda_mention_packets": context.get("external_lda_mention_packets", ""),
        "campaign_target_scope_status": context.get("campaign_target_scope_status", ""),
        "evidence_layers": "; ".join(evidence_layers),
        "missing_links": MISSING_LINKS,
        "source_url": url,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    context_rows = sorted(
        read_csv(args.input_csv),
        key=lambda row: parse_int(row.get("context_rank")),
    )
    selected = context_rows[:args.limit] if args.limit and args.limit > 0 else context_rows
    rows: list[dict[str, str]] = []
    for index, context in enumerate(selected, start=1):
        url = billstatus_url(context.get("bill_id", ""))
        try:
            root = fetch_xml(url, args.timeout)
            rows.append(build_row(context, root, url))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as exception:
            rows.append(error_row(context, "govinfo_fetch_error", url, str(exception)))
        if args.progress_every and index % args.progress_every == 0:
            print(f"Fetched {index} / {len(selected)} bill-finance/lobbying committee/action rows")
        if args.sleep > 0:
            time.sleep(args.sleep)
    for index, row in enumerate(rows, start=1):
        row["source_review_rank"] = str(index)
    return rows


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["govinfo_billstatus_status"] for row in rows)
    fetched_rows = [
        row for row in rows
        if row["govinfo_billstatus_status"] == "official_govinfo_billstatus_fetched"
    ]
    committee_rows = [
        row for row in fetched_rows
        if parse_int(row.get("committee_count")) > 0
    ]
    no_direct_committee_rows = [
        row for row in fetched_rows
        if row.get("committee_source_status")
        == "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ]
    action_rows = [
        row for row in fetched_rows
        if row.get("committee_action_record_status")
        == "official_govinfo_committee_action_records_present"
    ]
    no_direct_action_rows = [
        row for row in fetched_rows
        if row.get("committee_action_record_status")
        == "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
    ]
    floor_rows = [
        row for row in fetched_rows
        if parse_int(row.get("floor_action_count")) > 0
    ]
    roll_call_rows = [
        row for row in fetched_rows
        if parse_int(row.get("roll_call_reference_count")) > 0
    ]
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    args.metadata.write_text(
        "# Bill Finance/Lobbying Committee-Action Source Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- Input queue context: `{args.input_csv}`.\n"
        f"- govinfo BILLSTATUS bulk XML URL pattern: `{BASE_URL}/<congress>/<bill_type>/BILLSTATUS-<congress><bill_type><bill_number>.xml`.\n"
        "- govinfo BILLSTATUS feature page: `https://www.govinfo.gov/features/bill-status-xml-bulk-data`.\n\n"
        "Transformation:\n\n"
        "- Fetches one public govinfo BILLSTATUS XML record per queued finance/lobbying bill.\n"
        "- Joins records only by congress, bill type, and bill number parsed from local bill_id.\n"
        "- Extracts official committee names, committee activities, committee report citations, bounded action snippets, roll-call references when exposed in action text, and public-law outcome metadata.\n"
        "- Preserves finance/lobbying influence, roll-call influence, outcome-causality, welfare, capture, and model-validation gaps as explicit missing links.\n\n"
        "Rows:\n\n"
        f"- Queue rows inspected: {len(rows)}.\n"
        f"- Rows with govinfo BILLSTATUS fetched: {len(fetched_rows)}.\n"
        f"- Rows with official committee names: {len(committee_rows)}.\n"
        f"- Rows source-reviewed without direct committee names: {len(no_direct_committee_rows)}.\n"
        f"- Rows with committee action snippets: {len(action_rows)}.\n"
        f"- Rows source-reviewed without direct committee action records: {len(no_direct_action_rows)}.\n"
        f"- Rows with floor action snippets: {len(floor_rows)}.\n"
        f"- Rows with roll-call references in BILLSTATUS action text: {len(roll_call_rows)}.\n\n"
        "Status counts:\n\n"
        f"{status_lines}\n\n"
        f"Claim boundary: {CLAIM_BOUNDARY}\n",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=COMMITTEE_ACTION_CONTEXT)
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
        raise SystemExit("No committee/action source rows built.")
    write_csv(args.output, rows)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
