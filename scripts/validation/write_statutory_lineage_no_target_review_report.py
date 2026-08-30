#!/usr/bin/env python3
"""Write the curated statutory-lineage no-target review report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-no-target-review.csv")
OUT_MD = Path("reports/statutory-lineage-no-target-review.md")

CLAIM_BOUNDARY = (
    "Source-reviewed no-structured-U.S.C.-target disposition only. Rows close "
    "the no-target classification gate for designation laws whose official "
    "public-law text and OLRC public-law PDF expose no U.S.C. references, "
    "amendment/repeal/redesignation cues, or target-section candidates. They "
    "do not establish target-section text diffs, implementation outcomes, "
    "court review, welfare, causal effects, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["review_status"] for row in rows)
    public_laws = {
        row["public_law_number"].strip()
        for row in rows
        if row.get("public_law_number", "").strip()
    }
    source_reviewed = sum(
        1 for row in rows
        if row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
    )
    lines = [
        "# Statutory Lineage No-Target Review",
        "",
        "This report records curated source-reviewed no-target dispositions for designation laws in the codified-lineage queue. It is not target-section text-diff evidence.",
        "",
        f"- No-target review rows: {len(rows)}",
        f"- Source-reviewed no-structured-U.S.C.-target rows: {source_reviewed}",
        f"- Public laws reviewed: {len(public_laws)}",
        "",
        "Review statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Subject | Review status | Source-reviewed no target | Disposition |",
        "| ---: | --- | --- | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | {row['designation_subject']} | "
            f"{row['review_status']} | "
            f"{row['source_reviewed_no_structured_usc_target']} | "
            f"{row['codification_disposition']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def validate_against_source_scan(rows: list[dict[str, str]]) -> None:
    source_rows = {
        row.get("public_law_number", "").strip(): row
        for row in read_csv(SOURCE_SCAN)
        if row.get("public_law_number", "").strip()
    }
    for row in rows:
        public_law = row.get("public_law_number", "").strip()
        source_row = source_rows.get(public_law)
        if not source_row:
            raise SystemExit(f"{public_law}: missing source-scan row.")
        expected_pairs = {
            "source_scan_rank": "scan_rank",
            "lineage_review_rank": "lineage_review_rank",
            "action_rank": "action_rank",
            "bill_id": "bill_id",
            "govinfo_package_id": "govinfo_package_id",
            "govinfo_text_url": "govinfo_text_url",
            "source_scan_usc_reference_count": "usc_reference_count",
            "source_scan_title_code_reference_count": "title_code_reference_count",
            "source_scan_amendment_phrase_count": "amendment_phrase_count",
            "source_scan_repeal_phrase_count": "repeal_phrase_count",
            "source_scan_redesignation_phrase_count": "redesignation_phrase_count",
            "source_scan_target_section_candidate_count": "target_section_candidate_count",
        }
        for review_field, source_field in expected_pairs.items():
            if row.get(review_field, "").strip() != source_row.get(source_field, "").strip():
                raise SystemExit(
                    f"{public_law}: {review_field} does not match {SOURCE_SCAN} {source_field}."
                )


def main() -> int:
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    validate_against_source_scan(rows)
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
