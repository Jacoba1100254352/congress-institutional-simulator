#!/usr/bin/env python3
"""Build a conservative OLRC public-law marker adjudication dataset."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


INPUT = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_adjudication.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_adjudication.metadata.md")

CLAIM_BOUNDARY = (
    "Official OLRC public-law marker adjudication only. Rows classify annual "
    "U.S. Code pages where the queued public law is absent from the pre-edition, "
    "present in the post-edition, and paired with a normalized section-text "
    "change. This is codified-lineage marker evidence only; it does not establish "
    "source-reviewed target-section text diffs, public-law causal attribution, "
    "effective statutory text, implementation outcomes, court review, welfare, "
    "causal effects, or model validation."
)

FIELDNAMES = [
    "lineage_adjudication_rank",
    "text_diff_rank",
    "historical_scan_rank",
    "current_olrc_scan_rank",
    "triage_rank",
    "source_scan_rank",
    "lineage_review_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "pre_edition",
    "post_edition",
    "pre_olrc_url",
    "post_olrc_url",
    "pre_section_anchor_status",
    "post_section_anchor_status",
    "pre_public_law_reference_hits",
    "post_public_law_reference_hits",
    "public_law_reference_hit_delta",
    "normalized_text_hash_status",
    "section_change_cue_status",
    "post_public_law_context_count",
    "post_public_law_context_snippets",
    "first_changed_text_pre_window",
    "first_changed_text_post_window",
    "codified_lineage_marker",
    "lineage_adjudication_status",
    "lineage_marker_strength",
    "target_section_diff_status",
    "lineage_evidence_status",
    "evidence_layers",
    "missing_links",
    "source_review_notes",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


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


def joined(values: list[str]) -> str:
    result: list[str] = []
    for value in values:
        clean = " ".join(value.split())
        if clean and clean not in result:
            result.append(clean)
    return "; ".join(result)


def adjudication(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    pre_hits = parse_int(row.get("pre_public_law_reference_hits", ""))
    post_hits = parse_int(row.get("post_public_law_reference_hits", ""))
    context_count = parse_int(row.get("post_public_law_context_count", ""))
    has_marker = (
        row.get("pre_fetch_status") == "official_olrc_annual_section_page_fetched"
        and row.get("post_fetch_status") == "official_olrc_annual_section_page_fetched"
        and row.get("normalized_text_hash_status") == "pre_post_normalized_text_changed"
        and row.get("section_change_cue_status") == "normalized_section_changed_with_post_only_public_law_marker"
        and pre_hits == 0
        and post_hits > 0
        and context_count > 0
        and row.get("post_section_anchor_status") == "section_anchor_found"
    )
    if not has_marker:
        return (
            "0",
            "no_official_olrc_post_only_public_law_marker",
            "not_adjudicated",
            "no_automated_target_section_diff_cue",
            "no_codified_lineage_marker_evidence",
            "Annual text-diff row does not meet the official post-only public-law marker criteria.",
        )
    if row.get("pre_section_anchor_status") == "section_anchor_found":
        return (
            "1",
            "official_olrc_post_only_public_law_marker_with_pre_post_section_change",
            "strong_official_marker",
            "automated_pre_post_section_change_cue_needs_source_reviewed_diff",
            "official_olrc_codified_lineage_marker_evidence",
            "Official OLRC pre/post annual pages were fetched; the public-law marker is absent from the pre-edition, present in the post-edition, and paired with changed normalized section text. Treat as codified-lineage marker evidence only until target-section text diff and causal attribution are reviewed.",
        )
    return (
        "1",
        "official_olrc_post_only_public_law_marker_with_post_section_anchor_only",
        "moderate_official_marker",
        "post_section_anchor_without_pre_anchor_needs_manual_added_section_review",
        "official_olrc_codified_lineage_marker_evidence",
        "Official OLRC post annual page anchors the section and contains a post-only public-law marker, but the pre-edition section anchor was not found. Treat as codified-lineage marker evidence only until added-section or target-section text review is complete.",
    )


def build_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source_row in enumerate(source_rows, start=1):
        (
            marker,
            status,
            strength,
            diff_status,
            evidence_status,
            notes,
        ) = adjudication(source_row)
        evidence_layers = split_values(source_row.get("evidence_layers", ""))
        evidence_layers.extend([
            "statutory_lineage_olrc_annual_text_diff",
            "official_olrc_public_law_marker_adjudication",
        ])
        if marker == "1":
            evidence_layers.append("official_olrc_post_only_public_law_marker")
        missing_links = [
            "source_reviewed_target_section_diff",
            "public_law_causal_attribution",
            "law_revision_effective_text",
            "implementation_outcomes",
            "model_validation",
        ]
        rows.append({
            "lineage_adjudication_rank": str(index),
            "text_diff_rank": source_row.get("text_diff_rank", ""),
            "historical_scan_rank": source_row.get("historical_scan_rank", ""),
            "current_olrc_scan_rank": source_row.get("current_olrc_scan_rank", ""),
            "triage_rank": source_row.get("triage_rank", ""),
            "source_scan_rank": source_row.get("source_scan_rank", ""),
            "lineage_review_rank": source_row.get("lineage_review_rank", ""),
            "bill_id": source_row.get("bill_id", ""),
            "public_law_number": source_row.get("public_law_number", ""),
            "enacted_date": source_row.get("enacted_date", ""),
            "target_reference": source_row.get("target_reference", ""),
            "target_reference_type": source_row.get("target_reference_type", ""),
            "normalized_title": source_row.get("normalized_title", ""),
            "normalized_section": source_row.get("normalized_section", ""),
            "pre_edition": source_row.get("pre_edition", ""),
            "post_edition": source_row.get("post_edition", ""),
            "pre_olrc_url": source_row.get("pre_olrc_url", ""),
            "post_olrc_url": source_row.get("post_olrc_url", ""),
            "pre_section_anchor_status": source_row.get("pre_section_anchor_status", ""),
            "post_section_anchor_status": source_row.get("post_section_anchor_status", ""),
            "pre_public_law_reference_hits": source_row.get("pre_public_law_reference_hits", ""),
            "post_public_law_reference_hits": source_row.get("post_public_law_reference_hits", ""),
            "public_law_reference_hit_delta": source_row.get("public_law_reference_hit_delta", ""),
            "normalized_text_hash_status": source_row.get("normalized_text_hash_status", ""),
            "section_change_cue_status": source_row.get("section_change_cue_status", ""),
            "post_public_law_context_count": source_row.get("post_public_law_context_count", ""),
            "post_public_law_context_snippets": source_row.get("post_public_law_context_snippets", ""),
            "first_changed_text_pre_window": source_row.get("first_changed_text_pre_window", ""),
            "first_changed_text_post_window": source_row.get("first_changed_text_post_window", ""),
            "codified_lineage_marker": marker,
            "lineage_adjudication_status": status,
            "lineage_marker_strength": strength,
            "target_section_diff_status": diff_status,
            "lineage_evidence_status": evidence_status,
            "evidence_layers": joined(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "source_review_notes": notes,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], path: Path, source_input: Path) -> None:
    statuses = Counter(row["lineage_adjudication_status"] for row in rows)
    marker_rows = [row for row in rows if row["codified_lineage_marker"] == "1"]
    path.write_text(
        "\n".join([
            "# Statutory Lineage Adjudication Metadata",
            "",
            f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
            f"- source_input: `{source_input}`",
            f"- output_rows: {len(rows)}",
            f"- codified_lineage_marker_rows: {len(marker_rows)}",
            f"- public_law_rows_with_markers: {len({row['public_law_number'] for row in marker_rows})}",
            "",
            "Lineage adjudication statuses:",
            *[f"- {status}: {count}" for status, count in sorted(statuses.items())],
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
        ])
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_rows = read_csv(args.input)
    if not source_rows:
        raise SystemExit(f"{args.input} is missing or empty.")
    rows = build_rows(source_rows)
    write_csv(rows, args.output)
    write_metadata(rows, args.metadata, args.input)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
