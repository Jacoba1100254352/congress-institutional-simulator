#!/usr/bin/env python3
"""Write the official OLRC historical annual-edition availability scan report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_olrc_historical_scan.csv")
CURRENT_SCAN = Path("reports/statutory-lineage-olrc-current-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-olrc-historical-scan.csv")
OUT_MD = Path("reports/statutory-lineage-olrc-historical-scan.md")

CLAIM_BOUNDARY = (
    "Official OLRC annual-edition availability scan only. Rows compare hashes "
    "and public-law mentions for year-before-enactment and enactment-year "
    "U.S. Code pages, but they do not establish historical codified U.S.C. "
    "lineage, public-law causation, before/after target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def eligible_current_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row.get("public_law_reference_status") == "current_page_mentions_public_law"
        and row.get("olrc_scan_status") == "official_olrc_current_section_page_fetched"
        and row.get("normalized_title")
        and row.get("normalized_section")
    ]


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], current_rows: list[dict[str, str]]) -> None:
    review_statuses = Counter(row["historical_review_status"] for row in rows)
    hash_statuses = Counter(row["annual_text_hash_status"] for row in rows)
    public_law_statuses = Counter(row["annual_public_law_window_status"] for row in rows)
    both_fetched = [
        row
        for row in rows
        if row["historical_review_status"] == "annual_pre_post_pages_fetched_needs_manual_diff_review"
    ]
    changed_hashes = [
        row for row in rows if row["annual_text_hash_status"] == "pre_post_hash_changed"
    ]
    public_law_post_only = [
        row
        for row in rows
        if row["annual_public_law_window_status"] == "public_law_appears_in_post_edition_only"
    ]
    bytes_fetched = sum(
        int(row["pre_text_bytes"] or "0") + int(row["post_text_bytes"] or "0")
        for row in rows
    )
    represented_bills = {row["bill_id"] for row in rows if row["bill_id"]}
    eligible_rows = eligible_current_rows(current_rows)

    lines = [
        "# Statutory Lineage OLRC Historical Scan",
        "",
        "This report summarizes an official OLRC annual-edition availability scan for current-page statutory-lineage candidates whose current OLRC page mentions the queued public law. It is an annual-edition availability scan, not codified-lineage evidence.",
        "",
        f"- Historical OLRC scan rows: {len(rows)} / {len(eligible_rows)}",
        f"- Bills covered: {len(represented_bills)}",
        f"- Pre/post annual page pairs fetched: {len(both_fetched)}",
        f"- Pre/post text hashes changed: {len(changed_hashes)}",
        f"- Public laws appearing in post edition only: {len(public_law_post_only)}",
        f"- Official annual text bytes fetched: {bytes_fetched}",
        "",
        "Historical review statuses:",
    ]
    for status, count in sorted(review_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Annual text hash statuses:")
    for status, count in sorted(hash_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Annual public-law window statuses:")
    for status, count in sorted(public_law_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | Pre edition | Post edition | Review status | Hash status | Public-law window |",
            "| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in rows[:80]:
        lines.append(
            f"| {row['historical_scan_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['pre_edition']} | {row['post_edition']} | "
            f"{row['historical_review_status']} | {row['annual_text_hash_status']} | "
            f"{row['annual_public_law_window_status']} |"
        )
    if len(rows) > 80:
        lines.extend(
            [
                "",
                f"CSV contains {len(rows) - 80} additional historical OLRC scan rows not shown in the markdown table.",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(
            f"{RAW} is missing; run make build-statutory-lineage-olrc-historical-scan-raw first."
        )
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    current_rows = read_csv(CURRENT_SCAN)
    if not current_rows:
        raise SystemExit(
            f"{CURRENT_SCAN} is missing or empty; run make statutory-lineage-olrc-current-scan first."
        )
    write_csv(rows)
    write_md(rows, current_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
