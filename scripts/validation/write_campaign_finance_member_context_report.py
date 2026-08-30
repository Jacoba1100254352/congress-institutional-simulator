#!/usr/bin/env python3
"""Write a report for bounded campaign-finance member-context joins."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW_CONTEXT = Path("data/validation/raw/campaign_finance_member_context.csv")
OUT_CSV = Path("reports/campaign-finance-member-context.csv")
OUT_MD = Path("reports/campaign-finance-member-context.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def integer_value(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["member_context_status"] for row in rows)
    matched = [row for row in rows if row["member_context_status"] == "candidate_voteview_member_context"]
    candidate_rows = [row for row in rows if row.get("candidate_id")]
    matched_transactions = sum(integer_value(row["member_context_transaction_rows"]) for row in matched)
    unique_members = {row["bioguide_id"] for row in matched if row["bioguide_id"]}

    lines = [
        "# Campaign-Finance Member Context",
        "",
        "This report derives a bounded candidate-to-member context join from cached public FEC recipient metadata and cached Voteview member metadata. It is an evidence inventory, not bill-level influence validation.",
        "",
        f"- FEC recipient metadata rows inspected: {len(rows)}",
        f"- Candidate metadata rows inspected: {len(candidate_rows)}",
        f"- Candidate rows with Voteview member context: {len(matched)}",
        f"- Campaign-finance transaction rows with Voteview member context: {matched_transactions}",
        f"- Unique Voteview/Bioguide members linked: {len(unique_members)}",
        "",
        "Claim boundary: the joined candidate subset adds public Voteview member context to public FEC recipient metadata when candidate name, chamber, state, and district evidence agree. It does not identify bill-level influence, sponsor effectiveness, committee of jurisdiction, issue targeting, legislative outcome, causal influence, capture, public benefit, private contributor details, or model validation.",
        "",
        "Member-context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Recipient | Candidate | Member | Chamber | District/state | Transactions | Match basis | Missing links |",
        "| --- | --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for row in matched:
        chamber = row["voteview_chamber"]
        district = row["district_id"] or row["member_state"]
        lines.append(
            f"| `{row['recipient']}` | {row['candidate_name'] or '---'} | "
            f"{row['bioname']} (`{row['bioguide_id']}`) | {chamber} | `{district}` | "
            f"{row['member_context_transaction_rows']} | {row['match_basis']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW_CONTEXT.exists():
        raise SystemExit(f"{RAW_CONTEXT} is missing; run make build-campaign-finance-member-context-raw first.")
    rows = read_csv(RAW_CONTEXT)
    if not rows:
        raise SystemExit(f"{RAW_CONTEXT} is empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
