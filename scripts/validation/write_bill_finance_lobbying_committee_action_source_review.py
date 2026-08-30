#!/usr/bin/env python3
"""Write a report from cached committee/action source rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/bill_finance_lobbying_committee_action_source.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-committee-action-source-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-committee-action-source-review.md")

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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing. Run make build-bill-finance-lobbying-committee-action-source-raw first.")
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


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def status_rows(rows: list[dict[str, str]], field: str, expected: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get(field, "").strip() == expected]


def write_md(rows: list[dict[str, str]]) -> None:
    fetched = status_rows(rows, "govinfo_billstatus_status", "official_govinfo_billstatus_fetched")
    committee_rows = [
        row for row in rows
        if row.get("committee_source_status") == "official_govinfo_committee_names_present"
    ]
    no_direct_committee_rows = [
        row for row in rows
        if row.get("committee_source_status")
        == "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ]
    committee_action_rows = [
        row for row in rows
        if row.get("committee_action_record_status") == "official_govinfo_committee_action_records_present"
    ]
    no_direct_committee_action_rows = [
        row for row in rows
        if row.get("committee_action_record_status")
        == "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
    ]
    floor_action_rows = [
        row for row in rows
        if row.get("floor_action_record_status") == "official_govinfo_floor_action_records_present"
    ]
    roll_call_rows = [
        row for row in rows
        if parse_int(row.get("roll_call_reference_count")) > 0
    ]
    public_law_rows = [
        row for row in rows
        if row.get("legislative_outcome_source_status")
        == "official_govinfo_public_law_outcome_metadata_present_no_finance_lobbying_causality"
    ]
    lda_priority = [
        row for row in rows
        if parse_int(row.get("external_lda_mention_packets")) > 0
    ]
    campaign_priority = [
        row for row in rows
        if row.get("campaign_target_scope_status") != "not_in_campaign_finance_target_scope_review"
    ]
    status_counts = Counter(row["govinfo_billstatus_status"] for row in rows)
    unique_committees: set[str] = set()
    for row in committee_rows:
        for value in row.get("committee_names", "").split(";"):
            clean = " ".join(value.split())
            if clean:
                unique_committees.add(clean)
    lines = [
        "# Bill Finance/Lobbying Committee-Action Source Review",
        "",
        "This report caches official govinfo BILLSTATUS committee and action metadata for the queued finance/lobbying public-law bills. It is source context, not finance/lobbying influence evidence.",
        "",
        f"- Queued public-law rows: {len(rows)}",
        f"- Rows with govinfo BILLSTATUS fetched: {len(fetched)}",
        f"- Rows with official committee names: {len(committee_rows)}",
        f"- Rows source-reviewed without direct committee names: {len(no_direct_committee_rows)}",
        f"- Unique committee/subcommittee names represented: {len(unique_committees)}",
        f"- Rows with official committee action records: {len(committee_action_rows)}",
        f"- Rows source-reviewed without direct committee action records: {len(no_direct_committee_action_rows)}",
        f"- Rows with official floor action records: {len(floor_action_rows)}",
        f"- Rows with BILLSTATUS roll-call references: {len(roll_call_rows)}",
        f"- Rows with official public-law outcome metadata: {len(public_law_rows)}",
        f"- Rows with external LDA mention packets still needing target/source follow-up: {len(lda_priority)}",
        f"- Rows with campaign target-scope review still needing target/source follow-up: {len(campaign_priority)}",
        "",
        f"Claim boundary: {rows[0]['claim_boundary'] if rows else ''}",
        "",
        "govinfo fetch statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Rank | Bill | Committees | Committee actions | Floor actions | Roll-call refs | Public-law outcome |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['source_review_rank']} | `{row['bill_id']}` | "
            f"{row['committee_count']} | {row['committee_action_count']} | "
            f"{row['floor_action_count']} | {row['roll_call_reference_count']} | "
            f"{md_escape(row['legislative_outcome_source_status'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit("No committee/action source rows found.")
    missing = set(FIELDNAMES) - set(rows[0])
    if missing:
        raise SystemExit(f"{RAW}: missing columns {sorted(missing)}")
    rows = sorted(rows, key=lambda row: parse_int(row.get("source_review_rank")))
    write_csv(OUT_CSV, rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
