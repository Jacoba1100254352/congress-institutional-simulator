#!/usr/bin/env python3
"""Build a public FEC recipient-metadata linkage for campaign-finance rows."""

from __future__ import annotations

import argparse
import csv
import io
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


USER_AGENT = "congress-institutional-simulator-validation/0.5"
RAW_CAMPAIGN_FINANCE = Path("data/validation/raw/campaign_finance.csv")
OUT_CSV = Path("data/validation/raw/campaign_finance_linkage.csv")
OUT_METADATA = Path("data/validation/raw/campaign_finance_linkage.metadata.md")

COMMITTEE_FIELDS = [
    "committee_id",
    "committee_name",
    "treasurer_name",
    "street_1",
    "street_2",
    "city",
    "state",
    "zip",
    "committee_designation",
    "committee_type",
    "party_affiliation",
    "filing_frequency",
    "organization_type",
    "connected_organization_name",
    "candidate_id",
]
CANDIDATE_FIELDS = [
    "candidate_id",
    "candidate_name",
    "party_affiliation",
    "election_year",
    "office_state",
    "office",
    "office_district",
    "incumbent_challenger_open",
    "candidate_status",
    "principal_campaign_committee_id",
    "street_1",
    "street_2",
    "city",
    "state",
    "zip",
]
CANDIDATE_COMMITTEE_FIELDS = [
    "candidate_id",
    "candidate_election_year",
    "fec_election_year",
    "committee_id",
    "committee_type",
    "committee_designation",
    "linkage_id",
]
OUTPUT_FIELDS = [
    "cycle",
    "recipient",
    "recipient_type",
    "linkage_status",
    "transaction_rows",
    "linked_transaction_rows",
    "source_schedules",
    "committee_id",
    "committee_name",
    "committee_type",
    "committee_designation",
    "party_affiliation",
    "candidate_id",
    "candidate_name",
    "candidate_office",
    "candidate_office_state",
    "candidate_office_district",
    "principal_campaign_committee_id",
    "linked_committee_ids",
    "source_urls",
]


def cycle_suffix(cycle: int) -> str:
    return str(cycle)[-2:]


def fec_bulk_url(cycle: int, file_prefix: str) -> str:
    return f"https://www.fec.gov/files/bulk-downloads/{cycle}/{file_prefix}{cycle_suffix(cycle)}.zip"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def download_zip_rows(url: str, fields: list[str]) -> list[dict[str, str]]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        if not names:
            raise RuntimeError(f"{url} did not contain a data file")
        with archive.open(names[0]) as raw_handle:
            text_handle = io.TextIOWrapper(raw_handle, encoding="latin-1", newline="")
            reader = csv.reader(text_handle, delimiter="|")
            rows: list[dict[str, str]] = []
            for values in reader:
                padded = values + [""] * max(0, len(fields) - len(values))
                rows.append({
                    field: clean_text(padded[index]) if index < len(padded) else ""
                    for index, field in enumerate(fields)
                })
    return rows


def clean_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def by_key(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row.get(field, "")
        if key and key not in result:
            result[key] = row
    return result


def recipient_type(recipient: str) -> str:
    if recipient.startswith("C"):
        return "committee"
    if recipient.startswith(("H", "S", "P")):
        return "candidate"
    return "unknown"


def office_label(candidate: dict[str, str]) -> str:
    office = candidate.get("office", "")
    if office == "H":
        return "House"
    if office == "S":
        return "Senate"
    if office == "P":
        return "President"
    return office


def candidate_committee_index(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        committee_id = row.get("committee_id", "")
        if candidate_id and committee_id:
            result[candidate_id].add(committee_id)
    return result


def build_linkage_rows(
    *,
    campaign_rows: list[dict[str, str]],
    committee_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    candidate_committee_rows: list[dict[str, str]],
    source_urls: list[str],
) -> list[dict[str, str]]:
    committees = by_key(committee_rows, "committee_id")
    candidates = by_key(candidate_rows, "candidate_id")
    candidate_committees = candidate_committee_index(candidate_committee_rows)
    transaction_counts = Counter(row["recipient"] for row in campaign_rows if row.get("recipient"))
    schedules: dict[str, set[str]] = defaultdict(set)
    cycles: dict[str, set[str]] = defaultdict(set)
    for row in campaign_rows:
        recipient = row.get("recipient", "")
        if not recipient:
            continue
        if row.get("source_schedule"):
            schedules[recipient].add(row["source_schedule"])
        if row.get("cycle"):
            cycles[recipient].add(row["cycle"])

    source_url_text = "; ".join(source_urls)
    output_rows: list[dict[str, str]] = []
    for recipient in sorted(transaction_counts):
        kind = recipient_type(recipient)
        committee = committees.get(recipient, {}) if kind == "committee" else {}
        candidate_id = recipient if kind == "candidate" else committee.get("candidate_id", "")
        candidate = candidates.get(candidate_id, {}) if candidate_id else {}
        linked_committee_ids = sorted(candidate_committees.get(candidate_id, set()))
        linked = bool(committee or candidate)
        if kind == "committee" and committee and candidate:
            status = "committee_candidate_metadata"
        elif kind == "committee" and committee:
            status = "committee_metadata"
        elif kind == "candidate" and candidate and linked_committee_ids:
            status = "candidate_committee_metadata"
        elif kind == "candidate" and candidate:
            status = "candidate_metadata"
        else:
            status = "unmatched"
        count = transaction_counts[recipient]
        output_rows.append({
            "cycle": ";".join(sorted(cycles.get(recipient, set()))),
            "recipient": recipient,
            "recipient_type": kind,
            "linkage_status": status,
            "transaction_rows": str(count),
            "linked_transaction_rows": str(count if linked else 0),
            "source_schedules": ";".join(sorted(schedules.get(recipient, set()))),
            "committee_id": committee.get("committee_id", ""),
            "committee_name": committee.get("committee_name", ""),
            "committee_type": committee.get("committee_type", ""),
            "committee_designation": committee.get("committee_designation", ""),
            "party_affiliation": committee.get("party_affiliation") or candidate.get("party_affiliation", ""),
            "candidate_id": candidate_id,
            "candidate_name": candidate.get("candidate_name", ""),
            "candidate_office": office_label(candidate),
            "candidate_office_state": candidate.get("office_state", ""),
            "candidate_office_district": candidate.get("office_district", ""),
            "principal_campaign_committee_id": candidate.get("principal_campaign_committee_id", ""),
            "linked_committee_ids": ";".join(linked_committee_ids),
            "source_urls": source_url_text,
        })
    return output_rows


def write_metadata(
    *,
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    source_urls: list[str],
) -> None:
    total_transactions = sum(int(row["transaction_rows"]) for row in rows)
    linked_transactions = sum(int(row["linked_transaction_rows"]) for row in rows)
    status_counts = Counter(row["linkage_status"] for row in rows)
    type_counts = Counter(row["recipient_type"] for row in rows)
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    type_lines = "\n".join(
        f"- {kind}: {count}" for kind, count in sorted(type_counts.items())
    )
    url_lines = "\n".join(f"- {url}" for url in source_urls)
    path.write_text(
        "# Campaign Finance Recipient-Metadata Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"{url_lines}\n"
        "- FEC browse-data page: https://www.fec.gov/data/browse-data/\n\n"
        "Transformation:\n\n"
        f"- Reads `{args.campaign_finance_csv}` and groups rows by `recipient`.\n"
        "- Matches committee IDs to the FEC committee master file.\n"
        "- Matches House, Senate, and presidential candidate IDs to the FEC candidate master file.\n"
        "- Adds candidate-to-committee IDs from the FEC candidate-committee linkage file when available.\n"
        "- Retains public committee and candidate-office metadata needed for later join design.\n"
        "- Omits treasurer names, street addresses, contributor names, contributor addresses, payee names, and raw contribution records.\n\n"
        "Rows:\n\n"
        f"- Recipient rows: {len(rows)}.\n"
        f"- Raw campaign-finance transaction rows represented: {total_transactions}.\n"
        f"- Transactions with recipient metadata linkage: {linked_transactions}.\n"
        f"- Recipient linkage share: {(linked_transactions / total_transactions) if total_transactions else 0.0:.3f}.\n\n"
        "Recipient types:\n\n"
        f"{type_lines}\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        "This file links the bounded campaign-finance sample to public FEC recipient metadata only. "
        "It does not link money to bills, sponsors, member offices, public-opinion issues, committees of jurisdiction, "
        "outside-spending targets beyond FEC candidate IDs, or legislative outcomes, and it does not support causal influence or capture claims.\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", type=int, default=2024, help="FEC two-year cycle, default: 2024.")
    parser.add_argument("--campaign-finance-csv", type=Path, default=RAW_CAMPAIGN_FINANCE)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.campaign_finance_csv.exists():
        raise SystemExit(f"{args.campaign_finance_csv} is missing; run make build-campaign-finance-raw first.")
    source_urls = [
        fec_bulk_url(args.cycle, "cm"),
        fec_bulk_url(args.cycle, "cn"),
        fec_bulk_url(args.cycle, "ccl"),
    ]
    campaign_rows = read_csv(args.campaign_finance_csv)
    committee_rows = download_zip_rows(source_urls[0], COMMITTEE_FIELDS)
    candidate_rows = download_zip_rows(source_urls[1], CANDIDATE_FIELDS)
    candidate_committee_rows = download_zip_rows(source_urls[2], CANDIDATE_COMMITTEE_FIELDS)
    rows = build_linkage_rows(
        campaign_rows=campaign_rows,
        committee_rows=committee_rows,
        candidate_rows=candidate_rows,
        candidate_committee_rows=candidate_committee_rows,
        source_urls=source_urls,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_metadata(path=args.metadata, args=args, rows=rows, source_urls=source_urls)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
