#!/usr/bin/env python3
"""Build member-vote target-scope rows for finance/lobbying queue bills."""

from __future__ import annotations

import argparse
import csv
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata


ROLL_CALL_SOURCE_REVIEW = Path("reports/bill-finance-lobbying-roll-call-source-review.csv")
CAMPAIGN_TARGET_SCOPE_REVIEW = Path(
    "reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv"
)
CAMPAIGN_MEMBER_CONTEXT = Path("reports/campaign-finance-member-context.csv")
OUT_CSV = Path("data/validation/raw/bill_finance_lobbying_member_vote_targets.csv")
OUT_METADATA = Path("data/validation/raw/bill_finance_lobbying_member_vote_targets.metadata.md")

FIELDNAMES = [
    "member_vote_target_rank",
    "roll_call_source_rank",
    "source_review_rank",
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "vote_year",
    "roll_call_number",
    "official_vote_source_url",
    "source_fetch_status",
    "official_congress",
    "official_chamber",
    "official_legis_num",
    "official_vote_result",
    "official_action_date",
    "member_vote_source_position",
    "voter_bioguide_id",
    "voter_name",
    "voter_party",
    "voter_state",
    "voter_vote",
    "same_bill_campaign_target_bioguide_ids",
    "same_bill_campaign_target_candidate_names",
    "same_bill_campaign_target_scope_status",
    "same_bill_campaign_target_match_status",
    "broad_campaign_member_context_status",
    "broad_campaign_candidate_ids",
    "broad_campaign_candidate_names",
    "broad_campaign_transaction_rows",
    "member_vote_target_scope_status",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bill finance/lobbying member-vote target-scope review only; rows join "
    "official House Clerk member-vote metadata to reviewed public FEC/OpenFEC "
    "candidate/member target-scope context by Bioguide where available. The "
    "artifact provides vote/member target-scope context only, not lobbying "
    "contact confirmation, campaign spending for or against the bill, direct "
    "member target documents, roll-call influence, legislative-outcome "
    "causality, capture, public benefit, welfare, or model validation."
)

BASE_MISSING_LINKS = [
    "lobbying_contact_or_target_source",
    "external_campaign_target_source_document",
    "reviewed_outside_spending_target_beyond_candidate_id",
    "direct_member_vote_target_document",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
]


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


def join_values(values: list[str] | set[str]) -> str:
    result: list[str] = []
    for value in values:
        cleaned = clean(str(value or ""))
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


def fetch_xml(url: str, timeout: float) -> ET.Element:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/member-vote-target-review"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return ET.fromstring(response.read())


def aggregate_campaign_member_context(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, dict[str, object]] = {}
    for row in rows:
        bioguide = clean(row.get("bioguide_id"))
        if not bioguide:
            continue
        entry = grouped.setdefault(
            bioguide,
            {
                "candidate_ids": [],
                "candidate_names": [],
                "statuses": [],
                "transaction_rows": 0,
                "source_urls": [],
            },
        )
        for field, target in (
            ("candidate_id", "candidate_ids"),
            ("candidate_name", "candidate_names"),
            ("member_context_status", "statuses"),
        ):
            value = clean(row.get(field))
            values = entry[target]
            if isinstance(values, list) and value and value not in values:
                values.append(value)
        entry["transaction_rows"] = int(entry["transaction_rows"]) + parse_int(
            row.get("member_context_transaction_rows") or row.get("transaction_rows")
        )
        source_urls = entry["source_urls"]
        if isinstance(source_urls, list):
            for url in split_values(row.get("source_urls"))[:4]:
                if url and url not in source_urls:
                    source_urls.append(url)
    result: dict[str, dict[str, str]] = {}
    for bioguide, entry in grouped.items():
        result[bioguide] = {
            "candidate_ids": join_values(entry["candidate_ids"]),  # type: ignore[arg-type]
            "candidate_names": join_values(entry["candidate_names"]),  # type: ignore[arg-type]
            "statuses": join_values(entry["statuses"]),  # type: ignore[arg-type]
            "transaction_rows": str(entry["transaction_rows"]),
            "source_urls": join_values(entry["source_urls"]),  # type: ignore[arg-type]
        }
    return result


def campaign_targets_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = clean(row.get("bill_id"))
        if not bill_id:
            continue
        result[bill_id] = {
            "bioguide_ids": join_values(split_values(row.get("member_bioguide_ids"))),
            "candidate_names": join_values(split_values(row.get("candidate_names"))),
            "target_scope_status": clean(row.get("public_fec_target_scope_status")),
            "source_url": clean(row.get("source_url")),
        }
    return result


def member_vote_rows(root: ET.Element) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, vote_row in enumerate(children(child(root, "vote-data"), "recorded-vote"), start=1):
        legislator = child(vote_row, "legislator")
        rows.append({
            "position": str(index),
            "bioguide_id": clean(legislator.attrib.get("name-id") if legislator is not None else ""),
            "name": clean(
                legislator.attrib.get("unaccented-name")
                if legislator is not None
                else ""
            ) or clean(legislator.text if legislator is not None else ""),
            "party": clean(legislator.attrib.get("party") if legislator is not None else ""),
            "state": clean(legislator.attrib.get("state") if legislator is not None else ""),
            "vote": text_at(vote_row, "vote"),
        })
    return rows


def member_target_status(
    same_bill_target_ids: set[str],
    voter_bioguide_id: str,
    broad_context: dict[str, str] | None,
) -> tuple[str, str, str]:
    if same_bill_target_ids and voter_bioguide_id in same_bill_target_ids:
        return (
            "same_bill_campaign_target_bioguide_overlap",
            "member_vote_overlaps_reviewed_same_bill_public_fec_candidate_target_scope_no_influence_evidence",
            "same_bill_campaign_target_scope_present",
        )
    if same_bill_target_ids:
        return (
            "no_same_bill_campaign_target_bioguide_overlap",
            "reviewed_same_bill_campaign_target_scope_no_member_vote_overlap",
            "same_bill_campaign_target_scope_present",
        )
    if broad_context:
        return (
            "not_applicable_no_same_bill_campaign_target_scope_row",
            "member_vote_overlaps_broad_public_fec_candidate_context_not_current_bill_target",
            "no_same_bill_campaign_target_scope_row",
        )
    return (
        "not_applicable_no_same_bill_campaign_target_scope_row",
        "no_public_fec_campaign_member_target_context_overlap",
        "no_same_bill_campaign_target_scope_row",
    )


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    roll_call_rows = sorted(
        read_csv(args.roll_call_source_review),
        key=lambda row: parse_int(row.get("roll_call_source_rank")),
    )
    targets_by_bill = campaign_targets_by_bill(read_csv(args.campaign_target_scope_review))
    member_context_by_bioguide = aggregate_campaign_member_context(read_csv(args.campaign_member_context))
    rows: list[dict[str, str]] = []
    selected = roll_call_rows[:args.limit] if args.limit and args.limit > 0 else roll_call_rows
    for source_index, source_row in enumerate(selected, start=1):
        if source_row.get("source_fetch_status") != "official_house_clerk_roll_call_xml_fetched":
            continue
        url = clean(source_row.get("official_vote_source_url"))
        if not url:
            raise SystemExit(f"{args.roll_call_source_review}: missing House Clerk URL")
        try:
            root = fetch_xml(url, args.timeout)
        except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as exception:
            raise SystemExit(f"{url}: failed to fetch/parse official member votes: {exception}") from exception
        metadata = child(root, "vote-metadata")
        target_context = targets_by_bill.get(source_row.get("bill_id", ""), {})
        same_bill_target_ids = set(split_values(target_context.get("bioguide_ids")))
        for vote in member_vote_rows(root):
            voter_bioguide = vote["bioguide_id"]
            broad_context = member_context_by_bioguide.get(voter_bioguide)
            same_bill_match_status, target_scope_status, same_bill_scope_status = member_target_status(
                same_bill_target_ids,
                voter_bioguide,
                broad_context,
            )
            evidence_layers = [
                "bill_finance_lobbying_roll_call_source_review",
                "official_house_clerk_member_vote_source",
                "bill_finance_lobbying_member_vote_target_scope_review",
            ]
            source_urls = [url, clean(target_context.get("source_url"))]
            if target_context:
                evidence_layers.append("bill_finance_lobbying_campaign_finance_target_scope_review")
            if broad_context:
                evidence_layers.append("campaign_finance_member_context")
                source_urls.extend(split_values(broad_context.get("source_urls")))
            rows.append({
                "member_vote_target_rank": "",
                "roll_call_source_rank": source_row.get("roll_call_source_rank", ""),
                "source_review_rank": source_row.get("source_review_rank", ""),
                "review_rank": source_row.get("review_rank", ""),
                "bill_id": source_row.get("bill_id", ""),
                "public_law_number": source_row.get("public_law_number", ""),
                "policy_area": source_row.get("policy_area", ""),
                "vote_year": source_row.get("vote_year", ""),
                "roll_call_number": source_row.get("roll_call_number", ""),
                "official_vote_source_url": url,
                "source_fetch_status": source_row.get("source_fetch_status", ""),
                "official_congress": text_at(metadata, "congress") or source_row.get("official_congress", ""),
                "official_chamber": text_at(metadata, "chamber") or source_row.get("official_chamber", ""),
                "official_legis_num": text_at(metadata, "legis-num") or source_row.get("official_legis_num", ""),
                "official_vote_result": text_at(metadata, "vote-result") or source_row.get("official_vote_result", ""),
                "official_action_date": text_at(metadata, "action-date") or source_row.get("official_action_date", ""),
                "member_vote_source_position": vote["position"],
                "voter_bioguide_id": voter_bioguide,
                "voter_name": vote["name"],
                "voter_party": vote["party"],
                "voter_state": vote["state"],
                "voter_vote": vote["vote"],
                "same_bill_campaign_target_bioguide_ids": target_context.get("bioguide_ids", ""),
                "same_bill_campaign_target_candidate_names": target_context.get("candidate_names", ""),
                "same_bill_campaign_target_scope_status": same_bill_scope_status,
                "same_bill_campaign_target_match_status": same_bill_match_status,
                "broad_campaign_member_context_status": (
                    "broad_public_fec_candidate_member_context_present"
                    if broad_context
                    else "no_public_fec_candidate_member_context_overlap"
                ),
                "broad_campaign_candidate_ids": broad_context.get("candidate_ids", "") if broad_context else "",
                "broad_campaign_candidate_names": broad_context.get("candidate_names", "") if broad_context else "",
                "broad_campaign_transaction_rows": (
                    broad_context.get("transaction_rows", "0") if broad_context else "0"
                ),
                "member_vote_target_scope_status": target_scope_status,
                "evidence_layers": join_values(evidence_layers),
                "missing_links": join_values(BASE_MISSING_LINKS),
                "source_urls": join_values(source_urls),
                "source_url": url,
                "claim_boundary": CLAIM_BOUNDARY,
            })
        if args.sleep > 0:
            time.sleep(args.sleep)
        if args.progress_every and source_index % args.progress_every == 0:
            print(f"Reviewed {source_index} / {len(selected)} roll-call source rows")
    for index, row in enumerate(rows, start=1):
        row["member_vote_target_rank"] = str(index)
    return rows


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    source_rows = read_csv(args.roll_call_source_review)
    no_numbered = [
        row for row in source_rows
        if row.get("roll_call_source_review_status")
        == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    same_bill_overlap_rows = [
        row for row in rows
        if row["same_bill_campaign_target_match_status"] == "same_bill_campaign_target_bioguide_overlap"
    ]
    broad_context_rows = [
        row for row in rows
        if row["broad_campaign_member_context_status"]
        == "broad_public_fec_candidate_member_context_present"
    ]
    statuses = Counter(row["member_vote_target_scope_status"] for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    roll_call_keys = {
        (row["bill_id"], row["vote_year"], row["roll_call_number"])
        for row in rows
        if row["roll_call_number"]
    }
    write_reproducible_metadata(
        args.metadata,
        "# Bill Finance/Lobbying Member-Vote Target-Scope Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- Input roll-call source review: `{args.roll_call_source_review}`.\n"
        f"- Input campaign target-scope review: `{args.campaign_target_scope_review}`.\n"
        f"- Input campaign member context: `{args.campaign_member_context}`.\n\n"
        "Rows:\n\n"
        f"- Member-vote rows reviewed: {len(rows)}.\n"
        f"- Numbered roll calls reviewed: {len(roll_call_keys)}.\n"
        f"- Unique voting Bioguide IDs reviewed: {len({row['voter_bioguide_id'] for row in rows if row['voter_bioguide_id']})}.\n"
        f"- Floor-action rows without numbered roll calls excluded: {len(no_numbered)}.\n"
        f"- Rows with same-bill reviewed campaign target Bioguide overlap: {len(same_bill_overlap_rows)}.\n"
        f"- Rows with broad public FEC candidate/member-context overlap: {len(broad_context_rows)}.\n\n"
        "Status counts:\n\n"
        f"{status_lines}\n\n"
        f"Claim boundary: {CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roll-call-source-review", type=Path, default=ROLL_CALL_SOURCE_REVIEW)
    parser.add_argument("--campaign-target-scope-review", type=Path, default=CAMPAIGN_TARGET_SCOPE_REVIEW)
    parser.add_argument("--campaign-member-context", type=Path, default=CAMPAIGN_MEMBER_CONTEXT)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--progress-every", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = build_rows(args)
    if not rows:
        raise SystemExit("No bill-finance/lobbying member-vote target rows built.")
    write_csv(args.output, rows)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
