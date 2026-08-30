#!/usr/bin/env python3
"""Write source-reviewed statutory-lineage target-section diff dispositions."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW_REVIEW = Path("data/validation/raw/statutory_lineage_target_section_diff_review.csv")
PACKETS = Path("reports/statutory-lineage-target-review-packets.csv")
OUT_CSV = Path("reports/statutory-lineage-target-section-diff-review.csv")
OUT_MD = Path("reports/statutory-lineage-target-section-diff-review.md")

POSITIVE_REVIEW_STATUSES = {
    "reviewed_added_target_section_diff",
    "reviewed_pre_post_target_section_diff",
}
ALLOWED_REVIEW_STATUSES = POSITIVE_REVIEW_STATUSES | {
    "reviewed_related_section_context_no_exact_target_diff",
    "reviewed_target_section_cue_insufficient",
}

CLAIM_BOUNDARY = (
    "Source-reviewed official OLRC/GovInfo target-section diff disposition only. "
    "Rows record whether a bounded target-review packet has reviewed official-source "
    "evidence of added or changed target-section text. The artifact does not establish "
    "exclusive public-law causal attribution, law-revision effective text, implementation "
    "outcomes, court review, welfare, causal effects, or model validation."
)

FIELDNAMES = [
    "review_rank",
    "target_review_packet_rank",
    "lineage_adjudication_rank",
    "text_diff_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "pre_edition",
    "post_edition",
    "review_status",
    "source_reviewed_target_section_diff",
    "codified_lineage_relationship",
    "public_law_source_url",
    "pre_olrc_url",
    "post_olrc_url",
    "pre_text_sha256",
    "post_text_sha256",
    "pre_normalized_text_sha256",
    "post_normalized_text_sha256",
    "pre_section_anchor_status",
    "post_section_anchor_status",
    "post_public_law_context_count",
    "public_law_source_summary",
    "pre_olrc_source_summary",
    "post_olrc_source_summary",
    "target_section_diff_summary",
    "public_law_causal_attribution",
    "law_revision_effective_text_reviewed",
    "source_review_notes",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def by_rank(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        rank = row.get(field, "").strip()
        if not rank:
            raise SystemExit(f"{field} is missing in review input row.")
        if rank in result:
            raise SystemExit(f"Duplicate {field}: {rank}.")
        result[rank] = row
    return result


def validate_raw(raw_rows: list[dict[str, str]], packet_by_rank: dict[str, dict[str, str]]) -> None:
    if not raw_rows:
        raise SystemExit(f"{RAW_REVIEW} is missing or empty.")
    ranks: list[int] = []
    for row in raw_rows:
        review_rank = parse_int(row.get("review_rank", ""))
        if review_rank <= 0:
            raise SystemExit(f"{RAW_REVIEW}: invalid review_rank.")
        ranks.append(review_rank)
        packet_rank = row.get("target_review_packet_rank", "").strip()
        packet = packet_by_rank.get(packet_rank)
        if not packet:
            raise SystemExit(f"{RAW_REVIEW}: packet rank {packet_rank} is not in {PACKETS}.")
        for field in ("bill_id", "public_law_number", "target_reference", "pre_olrc_url", "post_olrc_url"):
            if row.get(field, "").strip() != packet.get(field, "").strip():
                raise SystemExit(
                    f"{RAW_REVIEW}: review row {review_rank} field {field} does not match packet {packet_rank}."
                )
        status = row.get("review_status", "").strip()
        if status not in ALLOWED_REVIEW_STATUSES:
            raise SystemExit(f"{RAW_REVIEW}: review row {review_rank} has invalid status {status}.")
        reviewed = row.get("source_reviewed_target_section_diff", "").strip()
        expected_reviewed = "1" if status in POSITIVE_REVIEW_STATUSES else "0"
        if reviewed != expected_reviewed:
            raise SystemExit(
                f"{RAW_REVIEW}: review row {review_rank} source-reviewed flag should be {expected_reviewed}."
            )
        boundary = row.get("claim_boundary", "")
        if (
            "public-law causal attribution" not in boundary
            or "implementation outcome" not in boundary
            or "model validation" not in boundary
        ):
            raise SystemExit(f"{RAW_REVIEW}: review row {review_rank} claim boundary is too weak.")
    if sorted(ranks) != list(range(1, len(raw_rows) + 1)):
        raise SystemExit(f"{RAW_REVIEW}: review ranks must be contiguous.")


def build_rows() -> list[dict[str, str]]:
    packet_rows = read_csv(PACKETS)
    if not packet_rows:
        raise SystemExit(f"{PACKETS} is missing or empty; run make statutory-lineage-target-review-packets first.")
    packet_by_rank = by_rank(packet_rows, "target_review_packet_rank")
    raw_rows = read_csv(RAW_REVIEW)
    validate_raw(raw_rows, packet_by_rank)
    rows: list[dict[str, str]] = []
    for raw_row in sorted(raw_rows, key=lambda row: parse_int(row.get("review_rank", ""))):
        packet = packet_by_rank[raw_row["target_review_packet_rank"].strip()]
        evidence_layers = [
            "statutory_lineage_target_section_review_packet",
            "statutory_lineage_target_section_diff_review",
        ]
        missing_links = [
            "public_law_causal_attribution",
            "law_revision_effective_text",
            "complete_codified_usc_lineage_review",
            "implementation_outcomes",
            "court_review",
            "model_validation",
        ]
        if raw_row["source_reviewed_target_section_diff"].strip() == "1":
            evidence_layers.append("statutory_lineage_source_reviewed_target_section_diff")
        else:
            missing_links.insert(0, "source_reviewed_target_section_diff")
        rows.append({
            "review_rank": raw_row["review_rank"].strip(),
            "target_review_packet_rank": raw_row["target_review_packet_rank"].strip(),
            "lineage_adjudication_rank": packet.get("lineage_adjudication_rank", "").strip(),
            "text_diff_rank": packet.get("text_diff_rank", "").strip(),
            "bill_id": packet.get("bill_id", "").strip(),
            "public_law_number": packet.get("public_law_number", "").strip(),
            "enacted_date": packet.get("enacted_date", "").strip(),
            "target_reference": packet.get("target_reference", "").strip(),
            "target_reference_type": packet.get("target_reference_type", "").strip(),
            "normalized_title": packet.get("normalized_title", "").strip(),
            "normalized_section": packet.get("normalized_section", "").strip(),
            "pre_edition": packet.get("pre_edition", "").strip(),
            "post_edition": packet.get("post_edition", "").strip(),
            "review_status": raw_row["review_status"].strip(),
            "source_reviewed_target_section_diff": raw_row["source_reviewed_target_section_diff"].strip(),
            "codified_lineage_relationship": raw_row["codified_lineage_relationship"].strip(),
            "public_law_source_url": raw_row["public_law_source_url"].strip(),
            "pre_olrc_url": packet.get("pre_olrc_url", "").strip(),
            "post_olrc_url": packet.get("post_olrc_url", "").strip(),
            "pre_text_sha256": packet.get("pre_text_sha256", "").strip(),
            "post_text_sha256": packet.get("post_text_sha256", "").strip(),
            "pre_normalized_text_sha256": packet.get("pre_normalized_text_sha256", "").strip(),
            "post_normalized_text_sha256": packet.get("post_normalized_text_sha256", "").strip(),
            "pre_section_anchor_status": packet.get("pre_section_anchor_status", "").strip(),
            "post_section_anchor_status": packet.get("post_section_anchor_status", "").strip(),
            "post_public_law_context_count": packet.get("post_public_law_context_count", "").strip(),
            "public_law_source_summary": raw_row["public_law_source_summary"].strip(),
            "pre_olrc_source_summary": raw_row["pre_olrc_source_summary"].strip(),
            "post_olrc_source_summary": raw_row["post_olrc_source_summary"].strip(),
            "target_section_diff_summary": raw_row["target_section_diff_summary"].strip(),
            "public_law_causal_attribution": raw_row["public_law_causal_attribution"].strip(),
            "law_revision_effective_text_reviewed": raw_row["law_revision_effective_text_reviewed"].strip(),
            "source_review_notes": raw_row["source_review_notes"].strip(),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
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
    relationship_counts = Counter(row["codified_lineage_relationship"] for row in rows)
    positive_rows = [row for row in rows if row["source_reviewed_target_section_diff"] == "1"]
    negative_rows = [
        row for row in rows
        if row["review_status"] == "reviewed_related_section_context_no_exact_target_diff"
    ]
    unresolved_rows = [
        row for row in rows
        if row["source_reviewed_target_section_diff"] != "1"
        and row["review_status"] != "reviewed_related_section_context_no_exact_target_diff"
    ]
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    lines = [
        "# Statutory Lineage Target-Section Diff Review",
        "",
        "This report records a bounded source-reviewed pilot for statutory-lineage target-section diffs. It uses official GovInfo public-law text plus official OLRC annual U.S. Code pages. It is not public-law causation, effective-text, implementation, court-review, or model-validation evidence.",
        "",
        f"- Target-section review disposition rows: {len(rows)}",
        f"- Source-reviewed target-section diff rows: {len(positive_rows)}",
        f"- Reviewed public laws: {len(public_laws)}",
        f"- Reviewed related-section/no-exact-target rows: {len(negative_rows)}",
        f"- Reviewed but unresolved/insufficient rows: {len(unresolved_rows)}",
        "",
        "Review statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Codified-lineage relationships:"])
    for relationship, count in sorted(relationship_counts.items()):
        lines.append(f"- {relationship}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Packet | Bill | Public law | Target reference | Review status | Source-reviewed diff | Relationship |",
        "| ---: | ---: | --- | --- | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | {row['target_review_packet_rank']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['review_status']} | "
            f"{row['source_reviewed_target_section_diff']} | {row['codified_lineage_relationship']} |"
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
