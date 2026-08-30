#!/usr/bin/env python3
"""Write the official OLRC current U.S. Code availability scan report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_olrc_current_scan.csv")
TRIAGE = Path("reports/statutory-lineage-target-section-triage.csv")
OUT_CSV = Path("reports/statutory-lineage-olrc-current-scan.csv")
OUT_MD = Path("reports/statutory-lineage-olrc-current-scan.md")

CLAIM_BOUNDARY = (
    "Official OLRC current-section availability scan only. Rows show whether a "
    "candidate target reference has a current U.S. Code page and whether that "
    "page text mentions the queued public law; they do not establish historical "
    "codified U.S.C. lineage, before/after target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], triage_rows: list[dict[str, str]]) -> None:
    scan_statuses = Counter(row["olrc_scan_status"] for row in rows)
    mention_statuses = Counter(row["public_law_reference_status"] for row in rows)
    evidence_statuses = Counter(row["lineage_evidence_status"] for row in rows)
    fetched_rows = [
        row
        for row in rows
        if row["olrc_scan_status"] == "official_olrc_current_section_page_fetched"
    ]
    public_law_mentions = [
        row
        for row in rows
        if row["public_law_reference_status"] == "current_page_mentions_public_law"
    ]
    bytes_fetched = sum(int(row["official_text_bytes"] or "0") for row in rows)
    represented_bills = {row["bill_id"] for row in rows if row["bill_id"]}

    lines = [
        "# Statutory Lineage OLRC Current Scan",
        "",
        "This report summarizes an official OLRC current U.S. Code page availability scan for statutory-lineage target-section triage rows. It is a current-source availability scan, not codified-lineage evidence.",
        "",
        f"- OLRC scan rows: {len(rows)} / {len(triage_rows)}",
        f"- Bills covered: {len(represented_bills)}",
        f"- Current OLRC pages fetched: {len(fetched_rows)}",
        f"- Current pages mentioning queued public law: {len(public_law_mentions)}",
        f"- Official text bytes fetched: {bytes_fetched}",
        "",
        "OLRC scan statuses:",
    ]
    for status, count in sorted(scan_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Public-law mention statuses:")
    for status, count in sorted(mention_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Lineage evidence statuses:")
    for status, count in sorted(evidence_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | OLRC status | Public-law mention | Bytes |",
            "| ---: | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in rows[:80]:
        lines.append(
            f"| {row['olrc_scan_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['olrc_scan_status']} | "
            f"{row['public_law_reference_status']} | {row['official_text_bytes']} |"
        )
    if len(rows) > 80:
        lines.extend(
            [
                "",
                f"CSV contains {len(rows) - 80} additional OLRC scan rows not shown in the markdown table.",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-statutory-lineage-olrc-current-scan-raw first.")
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    triage_rows = read_csv(TRIAGE)
    if not triage_rows:
        raise SystemExit(f"{TRIAGE} is missing or empty; run make statutory-lineage-target-section-triage first.")
    write_csv(rows)
    write_md(rows, triage_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
