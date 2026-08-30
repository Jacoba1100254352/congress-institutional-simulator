#!/usr/bin/env python3
"""Write a bounded Voteview roll-call bill-linkage report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROLLCALLS = Path("data/validation/raw/voteview_rollcalls.csv")
BILL_LINKAGE = Path("data/validation/raw/voteview_bill_linkage.csv")
OUT_CSV = Path("reports/voteview-bill-linkage.csv")
OUT_MD = Path("reports/voteview-bill-linkage.md")

FIELDNAMES = [
    "vote_id",
    "congress",
    "chamber",
    "rollnumber",
    "rollcall_date",
    "bill_number",
    "bill_id",
    "bill_match_status",
    "member_vote_rows",
    "evidence_layers",
    "missing_links",
    "vote_result",
    "vote_question",
    "vote_desc",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Voteview bill-linkage context only; not full roll-call-to-bill coverage, "
    "public-opinion representation, sponsor effectiveness, public benefit, "
    "welfare, causal influence, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def evidence_layers(row: dict[str, str]) -> list[str]:
    layers = ["voteview_rollcall_metadata"]
    if row.get("bill_id"):
        layers.append("voteview_bill_number")
    if row.get("bill_match_status") == "bill_progression_metadata":
        layers.append("congressgov_bill_progression_overlap")
    if row.get("bill_match_status") == "law_revision_bill_metadata":
        layers.append("congressgov_public_law_bill_metadata_overlap")
    return layers


def missing_links(row: dict[str, str]) -> list[str]:
    missing = [
        "district_public_opinion_issue",
        "sponsor_success_or_member_effectiveness",
        "public_law_or_statute_for_most_rows",
        "implementation_or_court_outcome",
        "model_validation",
    ]
    if row.get("bill_match_status") != "bill_progression_metadata":
        missing.insert(0, "cached_bill_progression_overlap")
    return missing


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(BILL_LINKAGE):
        rows.append({
            "vote_id": row.get("vote_id", ""),
            "congress": row.get("congress", ""),
            "chamber": row.get("chamber", ""),
            "rollnumber": row.get("rollnumber", ""),
            "rollcall_date": row.get("rollcall_date", ""),
            "bill_number": row.get("bill_number", ""),
            "bill_id": row.get("bill_id", ""),
            "bill_match_status": row.get("bill_match_status", ""),
            "member_vote_rows": row.get("member_vote_rows", ""),
            "evidence_layers": "; ".join(evidence_layers(row)),
            "missing_links": "; ".join(missing_links(row)),
            "vote_result": row.get("vote_result", ""),
            "vote_question": row.get("vote_question", ""),
            "vote_desc": row.get("vote_desc", ""),
            "source_url": row.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    member_vote_rows = sum(int(row["member_vote_rows"] or "0") for row in rows)
    bill_rows = [row for row in rows if row["bill_id"]]
    bill_member_vote_rows = sum(int(row["member_vote_rows"] or "0") for row in bill_rows)
    bill_progression_rows = [row for row in rows if row["bill_match_status"] == "bill_progression_metadata"]
    bill_progression_member_vote_rows = sum(int(row["member_vote_rows"] or "0") for row in bill_progression_rows)
    status_counts = Counter(row["bill_match_status"] or "unknown" for row in rows)
    chamber_counts = Counter(row["chamber"] or "Unknown" for row in rows)

    lines = [
        "# Voteview Bill Linkage",
        "",
        "This report derives a bounded vote-level bill-number crosswalk from cached Voteview roll-call rows and cached Voteview roll-call metadata. It is a linkage inventory, not bill-level roll-call validation.",
        "",
        f"- Voteview roll-call metadata rows represented: {len(rows)}",
        f"- Roll-call member-vote rows represented: {member_vote_rows}",
        f"- Voteview roll-call rows with normalized bill IDs: {len(bill_rows)}",
        f"- Member-vote rows on roll calls with normalized bill IDs: {bill_member_vote_rows}",
        f"- Voteview roll-call rows matching cached Congress.gov bill-progression rows: {len(bill_progression_rows)}",
        f"- Member-vote rows matching cached Congress.gov bill-progression rows: {bill_progression_member_vote_rows}",
        "",
        "Claim boundary: this context attaches Voteview roll-call metadata and parsed bill numbers to sampled roll-call IDs. It does not provide complete roll-call-to-bill coverage, district public-opinion support, sponsor-effectiveness evidence, public-law/statute lineage for most rows, implementation or court outcomes, public benefit, welfare, causal influence, or model validation.",
        "",
        "Bill match statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Chambers:")
    for chamber, count in sorted(chamber_counts.items()):
        lines.append(f"- {chamber}: {count}")
    lines.extend([
        "",
        "| Vote | Bill | Status | Member-vote rows | Question | Missing links |",
        "| --- | --- | --- | ---: | --- | --- |",
    ])
    def sort_key(row: dict[str, str]) -> tuple[int, int, str]:
        status_rank = 0 if row["bill_match_status"] == "bill_progression_metadata" else 1
        return (status_rank, -int(row["member_vote_rows"] or "0"), row["vote_id"])

    for row in sorted(rows, key=sort_key)[:20]:
        bill = row["bill_id"] or row["bill_number"] or "---"
        question = (row["vote_question"] or row["vote_desc"] or "---").replace("|", "/")
        lines.append(
            f"| `{row['vote_id']}` | `{bill}` | {row['bill_match_status']} | "
            f"{row['member_vote_rows']} | {question} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{BILL_LINKAGE} is missing or empty; run make build-voteview-bill-linkage-raw first.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
