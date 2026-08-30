#!/usr/bin/env python3
"""Write the statutory-lineage target-section review packet report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_target_review_packets.csv")
RAW_DIFF_REVIEW = Path("data/validation/raw/statutory_lineage_target_section_diff_review.csv")
ADJUDICATION = Path("reports/statutory-lineage-adjudication.csv")
OUT_CSV = Path("reports/statutory-lineage-target-review-packets.csv")
OUT_MD = Path("reports/statutory-lineage-target-review-packets.md")

CLAIM_BOUNDARY = (
    "Official OLRC target-section review packet plus downstream review "
    "disposition annotation only. Rows bundle pre/post annual U.S. Code URLs, "
    "source hashes, normalized section-text signatures, post-edition public-law "
    "marker context, first-change windows, and any attached curated target-section "
    "diff-review status. They do not establish public-law causal attribution, "
    "law-revision effective text, implementation outcomes, court review, welfare, "
    "causal effects, or model validation."
)

DIFF_REVIEW_FIELDS = [
    "target_section_diff_review_rank",
    "target_section_diff_review_status",
    "target_section_diff_review_relationship",
    "target_section_diff_review_notes",
]

POSITIVE_DIFF_REVIEW_STATUSES = {
    "reviewed_added_target_section_diff",
    "reviewed_pre_post_target_section_diff",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def join_values(values: list[str]) -> str:
    return "; ".join(values)


def by_packet_rank(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        rank = row.get("target_review_packet_rank", "").strip()
        if not rank:
            raise SystemExit(f"{RAW_DIFF_REVIEW}: row missing target_review_packet_rank.")
        if rank in result:
            raise SystemExit(f"{RAW_DIFF_REVIEW}: duplicate target_review_packet_rank {rank}.")
        result[rank] = row
    return result


def validate_review_match(packet: dict[str, str], review: dict[str, str]) -> None:
    for field in ("bill_id", "public_law_number", "target_reference", "pre_olrc_url", "post_olrc_url"):
        if packet.get(field, "").strip() != review.get(field, "").strip():
            raise SystemExit(
                f"{RAW_DIFF_REVIEW}: packet {packet.get('target_review_packet_rank', '')} "
                f"field {field} does not match review row {review.get('review_rank', '')}."
            )


def annotated_rows(rows: list[dict[str, str]], review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    review_by_packet = by_packet_rank(review_rows) if review_rows else {}
    annotated: list[dict[str, str]] = []
    for packet in rows:
        row = dict(packet)
        review = review_by_packet.get(row.get("target_review_packet_rank", "").strip())
        row.update({field: "" for field in DIFF_REVIEW_FIELDS})
        if review:
            validate_review_match(row, review)
            reviewed = review.get("source_reviewed_target_section_diff", "").strip()
            row["source_reviewed_target_section_diff"] = reviewed
            row["source_review_disposition"] = review.get("review_status", "").strip()
            row["target_section_diff_review_rank"] = review.get("review_rank", "").strip()
            row["target_section_diff_review_status"] = review.get("review_status", "").strip()
            row["target_section_diff_review_relationship"] = review.get(
                "codified_lineage_relationship", ""
            ).strip()
            row["target_section_diff_review_notes"] = review.get("source_review_notes", "").strip()
            evidence_layers = split_values(row.get("evidence_layers", ""))
            if "statutory_lineage_target_section_diff_review" not in evidence_layers:
                evidence_layers.append("statutory_lineage_target_section_diff_review")
            if reviewed == "1" and "statutory_lineage_source_reviewed_target_section_diff" not in evidence_layers:
                evidence_layers.append("statutory_lineage_source_reviewed_target_section_diff")
            row["evidence_layers"] = join_values(evidence_layers)

            missing_links = split_values(row.get("missing_links", ""))
            missing_links = [
                link for link in missing_links
                if link != "human_source_review_disposition"
                and not (reviewed == "1" and link == "source_reviewed_target_section_diff")
            ]
            row["missing_links"] = join_values(missing_links)
            status = review.get("review_status", "").strip()
            if reviewed == "1":
                row["lineage_evidence_status"] = "source_reviewed_target_section_diff_attached"
            elif status == "reviewed_related_section_context_no_exact_target_diff":
                row["lineage_evidence_status"] = "reviewed_related_section_no_exact_target_diff_attached"
            elif status:
                row["lineage_evidence_status"] = "reviewed_target_section_diff_unresolved_attached"
            row["source_review_notes"] = (
                "Downstream target-section diff-review disposition attached from "
                f"{RAW_DIFF_REVIEW}: {review.get('source_review_notes', '').strip()}"
            )
        row["claim_boundary"] = CLAIM_BOUNDARY
        annotated.append(row)
    return annotated


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], adjudication_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["target_review_packet_status"] for row in rows)
    strength_counts = Counter(row["target_review_packet_strength"] for row in rows)
    ready_rows = [
        row for row in rows
        if row["target_review_packet_status"] != "target_section_review_packet_needs_manual_source_retrieval"
    ]
    pre_post_ready = [
        row for row in rows
        if row["target_review_packet_status"] == "pre_post_target_section_review_packet_ready"
    ]
    added_ready = [
        row for row in rows
        if row["target_review_packet_status"] == "added_or_relocated_section_review_packet_ready"
    ]
    source_reviewed = [
        row for row in rows
        if row["source_reviewed_target_section_diff"] == "1"
    ]
    review_annotated = [
        row for row in rows
        if row.get("target_section_diff_review_rank", "").strip()
    ]
    lines = [
        "# Statutory Lineage Target Review Packets",
        "",
        "This report packages official OLRC annual-page marker rows for manual target-section source review and annotates rows that now have downstream source-review dispositions. It is review infrastructure plus disposition context, not public-law causation, effective-text, implementation, court-review, or model-validation evidence.",
        "",
        f"- Target review packet rows: {len(rows)} / {len(adjudication_rows)}",
        f"- Review-ready packet rows: {len(ready_rows)}",
        f"- Public laws with review-ready packets: {len({row['public_law_number'] for row in ready_rows})}",
        f"- Pre/post anchored review-ready packets: {len(pre_post_ready)}",
        f"- Added-or-relocated-section review-ready packets: {len(added_ready)}",
        f"- Target-section diff-review annotated rows: {len(review_annotated)}",
        f"- Source-reviewed target-section diff rows: {len(source_reviewed)}",
        "",
        "Review packet statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Review packet strengths:"])
    for strength, count in sorted(strength_counts.items()):
        lines.append(f"- {strength}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | Packet status | Packet strength | Review status | Source reviewed |",
            "| ---: | --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in rows[:100]:
        lines.append(
            f"| {row['target_review_packet_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['target_review_packet_status']} | {row['target_review_packet_strength']} | "
            f"{row.get('target_section_diff_review_status', '') or '---'} | "
            f"{row['source_reviewed_target_section_diff']} |"
        )
    if len(rows) > 100:
        lines.extend([
            "",
            f"CSV contains {len(rows) - 100} additional target-review packet rows not shown in the markdown table.",
        ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(
            f"{RAW} is missing; run make build-statutory-lineage-target-review-packets-raw first."
        )
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    adjudication_rows = read_csv(ADJUDICATION)
    if not adjudication_rows:
        raise SystemExit(
            f"{ADJUDICATION} is missing or empty; run make statutory-lineage-adjudication first."
        )
    review_rows = read_csv(RAW_DIFF_REVIEW) if RAW_DIFF_REVIEW.exists() else []
    rows = annotated_rows(rows, review_rows)
    write_csv(rows)
    write_md(rows, adjudication_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
