#!/usr/bin/env python3
"""Synchronize curated no-target review rows with the refreshed source scan."""

from __future__ import annotations

import csv
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_no_target_review.metadata.md")

SYNC_FIELDS = {
    "source_scan_rank": "scan_rank",
    "lineage_review_rank": "lineage_review_rank",
    "action_rank": "action_rank",
    "bill_id": "bill_id",
    "public_law_number": "public_law_number",
    "govinfo_package_id": "govinfo_package_id",
    "govinfo_text_url": "govinfo_text_url",
    "source_scan_usc_reference_count": "usc_reference_count",
    "source_scan_title_code_reference_count": "title_code_reference_count",
    "source_scan_amendment_phrase_count": "amendment_phrase_count",
    "source_scan_repeal_phrase_count": "repeal_phrase_count",
    "source_scan_redesignation_phrase_count": "redesignation_phrase_count",
    "source_scan_target_section_candidate_count": "target_section_candidate_count",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            result[bill_id] = row
    return result


def synchronized_rows(raw_rows: list[dict[str, str]], source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    source_by_bill = source_rows_by_bill(source_rows)
    rows: list[dict[str, str]] = []
    for row in raw_rows:
        bill_id = row.get("bill_id", "").strip()
        source_row = source_by_bill.get(bill_id)
        if not source_row:
            raise SystemExit(f"{bill_id}: missing source-scan row.")
        updated = dict(row)
        for raw_field, source_field in SYNC_FIELDS.items():
            updated[raw_field] = source_row.get(source_field, "").strip()
        for count_field in (
            "source_scan_usc_reference_count",
            "source_scan_title_code_reference_count",
            "source_scan_amendment_phrase_count",
            "source_scan_repeal_phrase_count",
            "source_scan_redesignation_phrase_count",
            "source_scan_target_section_candidate_count",
        ):
            if updated.get(count_field, "").strip() != "0":
                raise SystemExit(
                    f"{bill_id}: curated no-target row has nonzero {count_field} "
                    "after source-scan refresh."
                )
        rows.append(updated)
    return rows


def write_metadata(rows: list[dict[str, str]]) -> None:
    OUT_METADATA.write_text(
        "\n".join([
            "# Statutory Lineage No-Target Review Metadata",
            "",
            "Curated source-reviewed no-target review rows synchronized against the refreshed official GovInfo source scan.",
            "",
            f"- Raw rows: {len(rows)}",
            f"- Source scan: `{SOURCE_SCAN}`",
            "- Network required to refresh source scan: yes.",
            "- API key required: no.",
            "",
            "Claim boundary: source-reviewed no-structured-U.S.C.-target disposition only; this file does not establish target-section text diffs, implementation outcomes, court review, welfare, causal effects, or model validation.",
        ])
        + "\n"
    )


def main() -> int:
    raw_rows = read_csv(RAW)
    if not raw_rows:
        raise SystemExit(f"{RAW} is empty.")
    source_rows = read_csv(SOURCE_SCAN)
    if not source_rows:
        raise SystemExit(f"{SOURCE_SCAN} is empty.")
    rows = synchronized_rows(raw_rows, source_rows)
    write_csv(RAW, rows, list(raw_rows[0]))
    write_metadata(rows)
    print(f"Wrote {RAW}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
