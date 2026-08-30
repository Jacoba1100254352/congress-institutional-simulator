#!/usr/bin/env python3
"""Write bounded public-law attribution review for statutory-lineage target diffs."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
EFFECTIVE_TEXT_REVIEW = Path("reports/statutory-lineage-effective-text-review.csv")
OLRC_ANNUAL_TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-public-law-attribution-review.csv")
OUT_MD = Path("reports/statutory-lineage-public-law-attribution-review.md")

ATTRIBUTION_STATUS = "reviewed_target_section_diff_attributed_to_queued_public_law"

CLAIM_BOUNDARY = (
    "Target-section public-law attribution review only. Rows confirm that a "
    "source-reviewed target-section diff also has official GovInfo public-law "
    "source text, changed annual OLRC target text, a post-only public-law "
    "marker, and effective-text source review. This artifact does not "
    "establish complete codified lineage, exclusive current-section causation "
    "outside the reviewed target diff, implementation outcomes, direct "
    "target-section court review, welfare evidence, causal effects, or model "
    "validation."
)

FIELDNAMES = [
    "public_law_attribution_review_rank",
    "effective_text_review_rank",
    "review_rank",
    "target_review_packet_rank",
    "text_diff_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "codified_lineage_relationship",
    "target_section_diff_review_status",
    "source_reviewed_target_section_diff",
    "law_revision_effective_text_reviewed",
    "pre_edition",
    "post_edition",
    "public_law_source_url",
    "govinfo_package_id",
    "govinfo_text_url",
    "govinfo_details_url",
    "public_law_text_sha256",
    "public_law_text_bytes",
    "pre_olrc_url",
    "post_olrc_url",
    "current_olrc_url",
    "pre_normalized_text_sha256",
    "post_normalized_text_sha256",
    "annual_normalized_text_hash_status",
    "annual_normalized_text_char_delta",
    "annual_public_law_reference_hit_delta",
    "annual_post_public_law_context_count",
    "annual_automated_diff_cue_status",
    "annual_section_change_cue_status",
    "annual_manual_review_priority",
    "current_effective_text_review_status",
    "current_public_law_reference_status",
    "public_law_causal_attribution",
    "public_law_causal_attribution_reviewed",
    "attribution_source_basis",
    "attribution_review_summary",
    "source_review_notes",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run the upstream statutory-lineage target first.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def int_field(row: dict[str, str], field: str) -> int:
    try:
        return int(row.get(field, "0") or "0")
    except ValueError:
        return 0


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("target_reference", "").strip(),
    )


def source_key(row: dict[str, str]) -> tuple[str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
    )


def by_target_key(
    rows: list[dict[str, str]],
    source_name: str,
) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        key = row_key(row)
        if not all(key):
            raise SystemExit(f"{source_name}: row missing bill/public-law/target-reference key.")
        if key in result:
            raise SystemExit(f"{source_name}: duplicate target key {key}.")
        result[key] = row
    return result


def by_source_key(
    rows: list[dict[str, str]],
    source_name: str,
) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = source_key(row)
        if not all(key):
            raise SystemExit(f"{source_name}: row missing bill/public-law key.")
        if key in result:
            raise SystemExit(f"{source_name}: duplicate source key {key}.")
        result[key] = row
    return result


def validate_attribution_inputs(
    review_row: dict[str, str],
    effective_row: dict[str, str],
    annual_row: dict[str, str],
    source_row: dict[str, str],
) -> None:
    key = row_key(review_row)
    if review_row.get("source_reviewed_target_section_diff", "").strip() != "1":
        raise SystemExit(f"{TARGET_DIFF_REVIEW}: {key}: attribution requires source-reviewed target diff.")
    if effective_row.get("law_revision_effective_text_reviewed", "").strip() != "1":
        raise SystemExit(f"{EFFECTIVE_TEXT_REVIEW}: {key}: attribution requires effective-text review.")
    if (
        effective_row.get("current_effective_text_review_status", "").strip()
        != "reviewed_current_effective_text_source_with_public_law_note"
    ):
        raise SystemExit(f"{EFFECTIVE_TEXT_REVIEW}: {key}: current public-law note review is missing.")
    if annual_row.get("normalized_text_hash_status", "").strip() != "pre_post_normalized_text_changed":
        raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: {key}: annual target text did not change.")
    if (
        annual_row.get("section_change_cue_status", "").strip()
        != "normalized_section_changed_with_post_only_public_law_marker"
    ):
        raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: {key}: annual post-only public-law change cue is missing.")
    if (
        annual_row.get("automated_diff_cue_status", "").strip()
        != "post_only_public_law_marker_on_changed_annual_page"
    ):
        raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: {key}: annual public-law marker cue is missing.")
    if int_field(annual_row, "public_law_reference_hit_delta") <= 0:
        raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: {key}: public-law reference delta is not positive.")
    if int_field(annual_row, "post_public_law_context_count") <= 0:
        raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: {key}: post public-law context snippets are missing.")
    if source_row.get("source_review_status", "").strip() != "official_govinfo_public_law_text_scanned":
        raise SystemExit(f"{SOURCE_SCAN}: {key}: official GovInfo public-law text scan is missing.")
    if int_field(source_row, "official_text_bytes") <= 0 or not source_row.get("official_text_sha256", "").strip():
        raise SystemExit(f"{SOURCE_SCAN}: {key}: official public-law text hash/bytes are missing.")


def build_rows() -> list[dict[str, str]]:
    diff_rows = [
        row for row in read_csv(TARGET_DIFF_REVIEW)
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
    ]
    if not diff_rows:
        raise SystemExit(f"{TARGET_DIFF_REVIEW}: no source-reviewed target-section diff rows.")
    effective_by_key = by_target_key(read_csv(EFFECTIVE_TEXT_REVIEW), str(EFFECTIVE_TEXT_REVIEW))
    annual_by_key = by_target_key(read_csv(OLRC_ANNUAL_TEXT_DIFF), str(OLRC_ANNUAL_TEXT_DIFF))
    source_by_key = by_source_key(read_csv(SOURCE_SCAN), str(SOURCE_SCAN))

    rows: list[dict[str, str]] = []
    for review_row in sorted(diff_rows, key=lambda row: int_field(row, "review_rank")):
        key = row_key(review_row)
        effective_row = effective_by_key.get(key)
        annual_row = annual_by_key.get(key)
        source_row = source_by_key.get(source_key(review_row))
        if effective_row is None:
            raise SystemExit(f"{EFFECTIVE_TEXT_REVIEW}: missing effective-text row for {key}.")
        if annual_row is None:
            raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: missing annual text-diff row for {key}.")
        if source_row is None:
            raise SystemExit(f"{SOURCE_SCAN}: missing source-scan row for {key}.")
        validate_attribution_inputs(review_row, effective_row, annual_row, source_row)

        evidence_layers = [
            "statutory_lineage_source_reviewed_target_section_diff",
            "official_govinfo_public_law_text_scan",
            "official_olrc_annual_us_code_text_diff",
            "statutory_lineage_effective_text_source_review",
            "statutory_lineage_public_law_attribution_review",
        ]
        missing_links = [
            "complete_codified_usc_lineage_review",
            "implementation_outcomes",
            "direct_target_section_court_review",
            "welfare_or_public_benefit",
            "model_validation",
        ]
        rows.append({
            "public_law_attribution_review_rank": str(len(rows) + 1),
            "effective_text_review_rank": effective_row.get("effective_text_review_rank", "").strip(),
            "review_rank": review_row.get("review_rank", "").strip(),
            "target_review_packet_rank": review_row.get("target_review_packet_rank", "").strip(),
            "text_diff_rank": review_row.get("text_diff_rank", "").strip(),
            "bill_id": review_row.get("bill_id", "").strip(),
            "public_law_number": review_row.get("public_law_number", "").strip(),
            "enacted_date": review_row.get("enacted_date", "").strip(),
            "target_reference": review_row.get("target_reference", "").strip(),
            "target_reference_type": review_row.get("target_reference_type", "").strip(),
            "normalized_title": review_row.get("normalized_title", "").strip(),
            "normalized_section": review_row.get("normalized_section", "").strip(),
            "codified_lineage_relationship": review_row.get("codified_lineage_relationship", "").strip(),
            "target_section_diff_review_status": review_row.get("review_status", "").strip(),
            "source_reviewed_target_section_diff": "1",
            "law_revision_effective_text_reviewed": "1",
            "pre_edition": review_row.get("pre_edition", "").strip(),
            "post_edition": review_row.get("post_edition", "").strip(),
            "public_law_source_url": review_row.get("public_law_source_url", "").strip(),
            "govinfo_package_id": source_row.get("govinfo_package_id", "").strip(),
            "govinfo_text_url": source_row.get("govinfo_text_url", "").strip(),
            "govinfo_details_url": source_row.get("govinfo_details_url", "").strip(),
            "public_law_text_sha256": source_row.get("official_text_sha256", "").strip(),
            "public_law_text_bytes": source_row.get("official_text_bytes", "").strip(),
            "pre_olrc_url": review_row.get("pre_olrc_url", "").strip(),
            "post_olrc_url": review_row.get("post_olrc_url", "").strip(),
            "current_olrc_url": effective_row.get("current_olrc_url", "").strip(),
            "pre_normalized_text_sha256": review_row.get("pre_normalized_text_sha256", "").strip(),
            "post_normalized_text_sha256": review_row.get("post_normalized_text_sha256", "").strip(),
            "annual_normalized_text_hash_status": annual_row.get("normalized_text_hash_status", "").strip(),
            "annual_normalized_text_char_delta": annual_row.get("normalized_text_char_delta", "").strip(),
            "annual_public_law_reference_hit_delta": annual_row.get("public_law_reference_hit_delta", "").strip(),
            "annual_post_public_law_context_count": annual_row.get("post_public_law_context_count", "").strip(),
            "annual_automated_diff_cue_status": annual_row.get("automated_diff_cue_status", "").strip(),
            "annual_section_change_cue_status": annual_row.get("section_change_cue_status", "").strip(),
            "annual_manual_review_priority": annual_row.get("manual_review_priority", "").strip(),
            "current_effective_text_review_status": effective_row.get("current_effective_text_review_status", "").strip(),
            "current_public_law_reference_status": effective_row.get("current_public_law_reference_status", "").strip(),
            "public_law_causal_attribution": ATTRIBUTION_STATUS,
            "public_law_causal_attribution_reviewed": "1",
            "attribution_source_basis": (
                "source_reviewed_target_section_diff; official_govinfo_public_law_text; "
                "official_olrc_annual_pre_post_text_diff; post_only_public_law_marker; "
                "official_olrc_current_effective_text_review"
            ),
            "attribution_review_summary": (
                "Reviewed target-section diff is attributed to the queued public law because "
                "the official public-law text was scanned, annual OLRC target text changed, "
                "the post annual page introduced the queued public-law marker, and the "
                "current OLRC page retains public-law note evidence."
            ),
            "source_review_notes": (
                "Attribution is limited to the reviewed target-section diff row. It is not "
                "a complete codification history, implementation outcome, direct court "
                "review, welfare assessment, or model-validation finding."
            ),
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
    status_counts = Counter(row["public_law_causal_attribution"] for row in rows)
    relationship_counts = Counter(row["codified_lineage_relationship"] for row in rows)
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    reviewed_rows = [
        row for row in rows
        if row["public_law_causal_attribution_reviewed"] == "1"
    ]
    total_public_law_bytes = sum(int_field(row, "public_law_text_bytes") for row in rows)
    total_public_law_marker_delta = sum(
        int_field(row, "annual_public_law_reference_hit_delta")
        for row in rows
    )
    lines = [
        "# Statutory Lineage Public-Law Attribution Review",
        "",
        "This report records a bounded public-law attribution review for source-reviewed statutory-lineage target-section diff rows. It uses official GovInfo public-law text scans, official OLRC annual pre/post text-diff cues, and effective-text source review. It is not complete codified-lineage, implementation, court-review, welfare, causal-effect, or model-validation evidence.",
        "",
        f"- Public-law attribution review rows: {len(rows)}",
        f"- Public laws represented: {len(public_laws)}",
        f"- Public-law causal-attribution reviewed rows: {len(reviewed_rows)}",
        f"- Official public-law text bytes represented: {total_public_law_bytes}",
        f"- Annual public-law marker hit delta represented: {total_public_law_marker_delta}",
        "",
        "Public-law attribution statuses:",
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
        "| Rank | Bill | Public law | Target reference | Attribution status | Reviewed |",
        "| ---: | --- | --- | --- | --- | ---: |",
    ])
    for row in rows:
        lines.append(
            f"| {row['public_law_attribution_review_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['public_law_causal_attribution']} | "
            f"{row['public_law_causal_attribution_reviewed']} |"
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
