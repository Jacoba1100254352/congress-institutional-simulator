#!/usr/bin/env python3
"""Write the statutory-lineage official-text scan report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_source_scan.csv")
QUEUE = Path("reports/statutory-lineage-review-queue.csv")
NO_TARGET_REVIEW_RAW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
OUT_CSV = Path("reports/statutory-lineage-source-scan.csv")
OUT_MD = Path("reports/statutory-lineage-source-scan.md")

CLAIM_BOUNDARY = (
    "Official public-law text scan only. This report does not establish "
    "codified U.S.C. lineage, target-section text diffs, implementation "
    "outcomes, direct court review, welfare, causal effects, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], queue_rows: list[dict[str, str]]) -> None:
    no_target_review_rows = read_csv(NO_TARGET_REVIEW_RAW)
    reviewed_no_target_public_laws = {
        row.get("public_law_number", "").strip()
        for row in no_target_review_rows
        if row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
    }
    retained_no_target_rows = [
        row for row in rows
        if row.get("public_law_number", "").strip() in reviewed_no_target_public_laws
    ]
    statuses = Counter(row["source_review_status"] for row in rows)
    codification_statuses = Counter(row["codification_source_status"] for row in rows)
    evidence_statuses = Counter(row["lineage_evidence_status"] for row in rows)
    rows_with_usc = sum(int(row["usc_reference_count"] or "0") > 0 for row in rows)
    rows_with_amendment = sum(int(row["amendment_phrase_count"] or "0") > 0 for row in rows)
    rows_with_repeal = sum(int(row["repeal_phrase_count"] or "0") > 0 for row in rows)
    rows_with_redesignation = sum(int(row["redesignation_phrase_count"] or "0") > 0 for row in rows)
    candidate_count = sum(int(row["target_section_candidate_count"] or "0") for row in rows)
    official_bytes = sum(int(row["official_text_bytes"] or "0") for row in rows)

    lines = [
        "# Statutory Lineage Source Scan",
        "",
        "This report summarizes an official GovInfo public-law text scan for the statutory-lineage review queue. It is a source scan, not codified-lineage evidence.",
        "",
        f"- Source-scan rows retained: {len(rows)}",
        f"- Active source-review queue rows: {len(queue_rows)}",
        f"- Reviewed no-target source-scan rows retained: {len(retained_no_target_rows)}",
        f"- Rows with U.S.C. references: {rows_with_usc}",
        f"- Rows with amendment language: {rows_with_amendment}",
        f"- Rows with repeal language: {rows_with_repeal}",
        f"- Rows with redesignation language: {rows_with_redesignation}",
        f"- Candidate target-section snippets: {candidate_count}",
        f"- Official text bytes scanned: {official_bytes}",
        "",
        "Source review statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Codification source statuses:")
    for status, count in sorted(codification_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Lineage evidence statuses:")
    for status, count in sorted(evidence_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | U.S.C. refs | Amendment phrases | Repeal phrases | Redesignations | Candidate snippets | Evidence status |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['scan_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['usc_reference_count']} | {row['amendment_phrase_count']} | "
            f"{row['repeal_phrase_count']} | {row['redesignation_phrase_count']} | "
            f"{row['target_section_candidate_count']} | {row['lineage_evidence_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-statutory-lineage-source-scan-raw first.")
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    queue_rows = read_csv(QUEUE)
    if not queue_rows:
        raise SystemExit(f"{QUEUE} is missing or empty; run make statutory-lineage-review-queue first.")
    write_csv(rows)
    write_md(rows, queue_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
