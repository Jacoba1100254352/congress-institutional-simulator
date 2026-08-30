#!/usr/bin/env python3
"""Write a report from cached member-vote target-scope rows."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


RAW = Path("data/validation/raw/bill_finance_lobbying_member_vote_targets.csv")
ROLL_CALL_SOURCE_REVIEW = Path("reports/bill-finance-lobbying-roll-call-source-review.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-member-vote-target-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-member-vote-target-review.md")

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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(
            f"{path} is missing. Run make build-bill-finance-lobbying-member-vote-target-raw first."
        )
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


def vote_count_summary(rows: list[dict[str, str]]) -> str:
    counts = Counter(row.get("voter_vote", "") for row in rows)
    parts = []
    for label in ("Yea", "Aye", "Nay", "No", "Present", "Not Voting"):
        if counts.get(label):
            parts.append(f"{label}={counts[label]}")
    remaining = [
        f"{label}={count}"
        for label, count in sorted(counts.items())
        if label and label not in {"Yea", "Aye", "Nay", "No", "Present", "Not Voting"}
    ]
    parts.extend(remaining)
    return ", ".join(parts) if parts else "none"


def write_md(rows: list[dict[str, str]]) -> None:
    source_rows = read_csv(ROLL_CALL_SOURCE_REVIEW)
    no_numbered = [
        row for row in source_rows
        if row.get("roll_call_source_review_status")
        == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    roll_call_keys = {
        (row["bill_id"], row["vote_year"], row["roll_call_number"])
        for row in rows
        if row["roll_call_number"]
    }
    unique_voters = {row["voter_bioguide_id"] for row in rows if row["voter_bioguide_id"]}
    same_bill_overlap = [
        row for row in rows
        if row["same_bill_campaign_target_match_status"] == "same_bill_campaign_target_bioguide_overlap"
    ]
    broad_context = [
        row for row in rows
        if row["broad_campaign_member_context_status"]
        == "broad_public_fec_candidate_member_context_present"
    ]
    statuses = Counter(row["member_vote_target_scope_status"] for row in rows)
    by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_bill[row["bill_id"]].append(row)
    lines = [
        "# Bill Finance/Lobbying Member-Vote Target Review",
        "",
        "This report joins official House Clerk member-vote rows for queued finance/lobbying public-law bills to reviewed public FEC/OpenFEC candidate/member target-scope context by Bioguide. It is target-scope context, not finance/lobbying roll-call influence evidence.",
        "",
        f"- Member-vote rows reviewed: {len(rows)}",
        f"- Numbered roll calls reviewed: {len(roll_call_keys)}",
        f"- Unique voting Bioguide IDs reviewed: {len(unique_voters)}",
        f"- Floor-action rows without numbered roll calls excluded: {len(no_numbered)}",
        f"- Rows with same-bill reviewed campaign target Bioguide overlap: {len(same_bill_overlap)}",
        f"- Rows with broad public FEC candidate/member-context overlap: {len(broad_context)}",
        "",
        f"Claim boundary: {rows[0]['claim_boundary'] if rows else ''}",
        "",
        "Member-vote target-scope statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Bill | Roll call | Member rows | Same-bill target overlaps | Broad FEC member-context overlaps | Vote counts |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ])
    for bill_id, bill_rows in sorted(
        by_bill.items(),
        key=lambda item: parse_int(item[1][0].get("roll_call_source_rank")),
    ):
        same_bill_rows = [
            row for row in bill_rows
            if row["same_bill_campaign_target_match_status"] == "same_bill_campaign_target_bioguide_overlap"
        ]
        broad_rows = [
            row for row in bill_rows
            if row["broad_campaign_member_context_status"]
            == "broad_public_fec_candidate_member_context_present"
        ]
        roll_label = "; ".join(
            sorted({row["roll_call_number"] for row in bill_rows if row["roll_call_number"]})
        )
        lines.append(
            f"| `{bill_id}` | {md_escape(roll_label)} | {len(bill_rows)} | "
            f"{len(same_bill_rows)} | {len(broad_rows)} | {md_escape(vote_count_summary(bill_rows))} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit("No bill-finance/lobbying member-vote target rows found.")
    missing = set(FIELDNAMES) - set(rows[0])
    if missing:
        raise SystemExit(f"{RAW}: missing columns {sorted(missing)}")
    rows = sorted(rows, key=lambda row: parse_int(row.get("member_vote_target_rank")))
    write_csv(OUT_CSV, rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
