#!/usr/bin/env python3
"""Write a report from cached bill-finance/lobbying roll-call source rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/bill_finance_lobbying_roll_call_source.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-roll-call-source-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-roll-call-source-review.md")

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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing. Run make build-bill-finance-lobbying-roll-call-source-raw first.")
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


def write_md(rows: list[dict[str, str]]) -> None:
    fetched = [
        row for row in rows
        if row.get("source_fetch_status") == "official_house_clerk_roll_call_xml_fetched"
    ]
    no_numbered = [
        row for row in rows
        if row.get("roll_call_source_review_status") == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    bill_matches = [
        row for row in fetched
        if row.get("source_bill_match_status") == "official_vote_legis_num_matches_bill_id"
    ]
    statuses = Counter(row["roll_call_source_review_status"] for row in rows)
    lines = [
        "# Bill Finance/Lobbying Roll-Call Source Review",
        "",
        "This report caches official House Clerk roll-call source metadata for queued finance/lobbying public-law bills when govinfo BILLSTATUS action text exposes a numbered House roll call. It is vote-source context, not finance/lobbying roll-call influence evidence.",
        "",
        f"- Source-review rows: {len(rows)}",
        f"- Official House Clerk roll-call XML rows fetched: {len(fetched)}",
        f"- Fetched rows whose official legis-num matches bill_id: {len(bill_matches)}",
        f"- Floor-action rows reviewed without numbered roll-call references: {len(no_numbered)}",
        f"- Member vote rows represented: {sum(parse_int(row.get('member_vote_count')) for row in rows)}",
        "",
        f"Claim boundary: {rows[0]['claim_boundary'] if rows else ''}",
        "",
        "Roll-call source-review statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Rank | Bill | Roll call | Source status | Vote result | Totals | Member rows |",
        "| ---: | --- | --- | --- | --- | --- | ---: |",
    ])
    for row in rows:
        totals = "voice/UC/no numbered roll call"
        if row.get("official_yea_total") or row.get("official_nay_total"):
            totals = (
                f"{row.get('official_yea_total', '0')}-"
                f"{row.get('official_nay_total', '0')}"
            )
            if parse_int(row.get("official_present_total")) > 0:
                totals += f", {row.get('official_present_total')} present"
        roll_label = row.get("roll_call_number") or "none"
        lines.append(
            f"| {row['roll_call_source_rank']} | `{row['bill_id']}` | {roll_label} | "
            f"{md_escape(row['roll_call_source_review_status'])} | "
            f"{md_escape(row.get('official_vote_result', '') or row.get('floor_action_vote_mode_status', ''))} | "
            f"{md_escape(totals)} | {row.get('member_vote_count', '0')} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit("No roll-call source rows found.")
    missing = set(FIELDNAMES) - set(rows[0])
    if missing:
        raise SystemExit(f"{RAW}: missing columns {sorted(missing)}")
    rows = sorted(rows, key=lambda row: parse_int(row.get("roll_call_source_rank")))
    write_csv(OUT_CSV, rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
