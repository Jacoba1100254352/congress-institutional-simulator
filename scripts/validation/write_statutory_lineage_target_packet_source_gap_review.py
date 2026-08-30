#!/usr/bin/env python3
"""Write curated dispositions for reviewed target-packet source gaps."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW_REVIEW = Path("data/validation/raw/statutory_lineage_target_packet_source_gap_review.csv")
SOURCE_GAP_QUEUE = Path("reports/statutory-lineage-target-packet-source-gap-queue.csv")
OUT_CSV = Path("reports/statutory-lineage-target-packet-source-gap-review.csv")
OUT_MD = Path("reports/statutory-lineage-target-packet-source-gap-review.md")

ALLOWED_REVIEW_STATUSES = {
    "reviewed_appropriation_authority_reference_no_packet",
    "reviewed_cross_reference_only_no_packet",
    "reviewed_table_or_prec_reference_no_packet",
    "reviewed_temporary_override_no_packet",
}

CLAIM_BOUNDARY = (
    "Source-gap disposition review only. Rows classify reviewed current-OLRC "
    "no-marker blockers against official GovInfo public-law text and current "
    "OLRC pages. They do not establish codified lineage, target-section text "
    "diffs, public-law causal attribution, effective statutory text, "
    "implementation outcomes, court review, welfare evidence, causal effects, "
    "or model validation."
)

FIELDNAMES = [
    "review_rank",
    "source_gap_rank",
    "packet_expansion_rank",
    "expansion_rank",
    "completion_rank",
    "triage_rank",
    "source_scan_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "target_reference",
    "target_reference_type",
    "current_olrc_url",
    "current_public_law_reference_status",
    "review_status",
    "source_gap_reviewed",
    "public_law_source_url",
    "public_law_source_summary",
    "current_olrc_source_summary",
    "source_gap_disposition",
    "source_gap_disposition_summary",
    "next_review_action",
    "source_review_notes",
    "remaining_completion_gates",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        clean = " ".join((value or "").split())
        if clean and clean not in seen:
            seen.append(clean)
    return "; ".join(seen)


def review_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("target_reference", "").strip(),
        row.get("current_olrc_url", "").strip(),
    )


def rows_by_key(rows: list[dict[str, str]], path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = review_key(row)
        if not all(key):
            continue
        if key in result:
            raise SystemExit(f"{path}: duplicate review key {key}")
        result[key] = row
    return result


def validate_raw(review_rows: list[dict[str, str]], source_gap_by_key: dict[tuple[str, str, str, str], dict[str, str]]) -> None:
    ranks: list[int] = []
    for row in review_rows:
        rank = parse_int(row.get("review_rank", ""))
        if rank <= 0:
            raise SystemExit(f"{RAW_REVIEW}: invalid review_rank.")
        ranks.append(rank)
        status = row.get("review_status", "").strip()
        if status not in ALLOWED_REVIEW_STATUSES:
            raise SystemExit(f"{RAW_REVIEW}: review row {rank} has invalid status {status}.")
        if not source_gap_by_key.get(review_key(row)):
            raise SystemExit(
                f"{RAW_REVIEW}: review row {rank} does not match a current source-gap queue row."
            )
        boundary = row.get("claim_boundary", "")
        for phrase in (
            "not codified-lineage evidence",
            "not target-section text diff evidence",
            "not model validation",
        ):
            if phrase not in boundary:
                raise SystemExit(f"{RAW_REVIEW}: review row {rank} claim boundary is too weak.")
    if sorted(ranks) != list(range(1, len(review_rows) + 1)):
        raise SystemExit(f"{RAW_REVIEW}: review ranks must be contiguous.")


def build_rows() -> list[dict[str, str]]:
    source_gap_rows = read_csv(SOURCE_GAP_QUEUE)
    source_gap_by_key = rows_by_key(source_gap_rows, SOURCE_GAP_QUEUE)
    review_rows = read_csv(RAW_REVIEW)
    validate_raw(review_rows, source_gap_by_key)

    rows: list[dict[str, str]] = []
    for review_row in sorted(review_rows, key=lambda row: parse_int(row.get("review_rank", ""))):
        source_gap_row = source_gap_by_key[review_key(review_row)]
        evidence_layers = [
            "statutory_lineage_target_packet_source_gap_review",
            "statutory_lineage_target_packet_source_gap_queue",
        ]
        evidence_layers.extend(split_values(source_gap_row.get("evidence_layers", "")))
        missing_links = split_values(source_gap_row.get("missing_links", ""))
        for gap in (
            "complete_codified_usc_lineage_review",
            "implementation_outcomes_or_enforcement",
            "direct_target_section_court_review",
            "welfare_or_public_benefit",
            "model_validation",
        ):
            missing_links.append(gap)
        source_artifacts = [
            str(RAW_REVIEW),
            str(SOURCE_GAP_QUEUE),
            review_row.get("public_law_source_url", "").strip(),
            review_row.get("current_olrc_url", "").strip(),
        ]
        rows.append({
            "review_rank": review_row.get("review_rank", "").strip(),
            "source_gap_rank": source_gap_row.get("source_gap_rank", "").strip(),
            "packet_expansion_rank": source_gap_row.get("packet_expansion_rank", "").strip(),
            "expansion_rank": source_gap_row.get("expansion_rank", "").strip(),
            "completion_rank": source_gap_row.get("completion_rank", "").strip(),
            "triage_rank": source_gap_row.get("triage_rank", "").strip(),
            "source_scan_rank": source_gap_row.get("source_scan_rank", "").strip(),
            "bill_id": source_gap_row.get("bill_id", "").strip(),
            "public_law_number": source_gap_row.get("public_law_number", "").strip(),
            "policy_area": source_gap_row.get("policy_area", "").strip(),
            "target_reference": source_gap_row.get("target_reference", "").strip(),
            "target_reference_type": source_gap_row.get("target_reference_type", "").strip(),
            "current_olrc_url": source_gap_row.get("current_olrc_url", "").strip(),
            "current_public_law_reference_status": source_gap_row.get(
                "current_public_law_reference_status",
                "",
            ).strip(),
            "review_status": review_row.get("review_status", "").strip(),
            "source_gap_reviewed": "1",
            "public_law_source_url": review_row.get("public_law_source_url", "").strip(),
            "public_law_source_summary": review_row.get("public_law_source_summary", "").strip(),
            "current_olrc_source_summary": review_row.get("current_olrc_source_summary", "").strip(),
            "source_gap_disposition": review_row.get("source_gap_disposition", "").strip(),
            "source_gap_disposition_summary": review_row.get("source_gap_disposition_summary", "").strip(),
            "next_review_action": review_row.get("next_review_action", "").strip(),
            "source_review_notes": review_row.get("source_review_notes", "").strip(),
            "remaining_completion_gates": source_gap_row.get("remaining_completion_gates", "").strip(),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(source_artifacts),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["review_status"] for row in rows)
    disposition_counts = Counter(row["source_gap_disposition"] for row in rows)
    bill_counts = Counter(row["bill_id"] for row in rows)
    lines = [
        "# Statutory Lineage Target Packet Source-Gap Review",
        "",
        "This report records curated official-source dispositions for current-OLRC no-marker source-gap rows. It is a reviewed blocker-disposition layer, not codified-lineage or target-section diff evidence.",
        "",
        f"- Source-gap review rows: {len(rows)}",
        f"- Public laws with reviewed source-gap rows: {len(bill_counts)}",
        "- Reviewed no-packet dispositions: "
        f"{sum(status_counts.values())}",
        "",
        "Review statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Disposition categories:",
    ])
    for disposition, count in sorted(disposition_counts.items()):
        lines.append(f"- {disposition}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Review | Source-gap rank | Bill | Public law | Target reference | Review status | Disposition | Next action |",
        "| ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | {row['source_gap_rank']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['review_status']} | "
            f"{row['source_gap_disposition']} | {row['next_review_action']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
