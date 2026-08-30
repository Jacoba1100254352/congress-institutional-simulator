#!/usr/bin/env python3
"""Build reviewer packets for statutory-lineage target-section source review."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata


ADJUDICATION = Path("reports/statutory-lineage-adjudication.csv")
TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_target_review_packets.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_target_review_packets.metadata.md")

CLAIM_BOUNDARY = (
    "Official OLRC target-section review packet only. Rows bundle pre/post "
    "annual U.S. Code URLs, source hashes, normalized section-text signatures, "
    "post-edition public-law marker context, and first-change windows for "
    "manual source review. They do not establish source-reviewed target-section "
    "text diffs, public-law causal attribution, effective statutory text, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)

MISSING_LINKS = (
    "human_source_review_disposition",
    "source_reviewed_target_section_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "implementation_outcomes",
    "model_validation",
)

FIELDNAMES = [
    "target_review_packet_rank",
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
    "pre_text_sha256",
    "post_text_sha256",
    "pre_normalized_text_sha256",
    "post_normalized_text_sha256",
    "pre_section_anchor_status",
    "post_section_anchor_status",
    "pre_public_law_reference_hits",
    "post_public_law_reference_hits",
    "public_law_reference_hit_delta",
    "normalized_text_hash_status",
    "normalized_text_char_delta",
    "section_change_cue_status",
    "post_public_law_context_count",
    "post_public_law_context_snippets",
    "first_changed_text_pre_window",
    "first_changed_text_post_window",
    "codified_lineage_marker",
    "lineage_adjudication_status",
    "lineage_marker_strength",
    "target_section_diff_status",
    "target_review_packet_status",
    "target_review_packet_strength",
    "source_reviewed_target_section_diff",
    "source_review_disposition",
    "review_packet_components",
    "review_task_list",
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


def joined(values: list[str] | tuple[str, ...]) -> str:
    result: list[str] = []
    for value in values:
        clean = " ".join(value.split())
        if clean and clean not in result:
            result.append(clean)
    return "; ".join(result)


def packet_status(row: dict[str, str]) -> tuple[str, str, str, str]:
    marker = row.get("codified_lineage_marker", "").strip() == "1"
    has_post_context = parse_int(row.get("post_public_law_context_count", "")) > 0
    has_change_windows = bool(
        row.get("first_changed_text_pre_window", "").strip()
        and row.get("first_changed_text_post_window", "").strip()
    )
    pre_anchor = row.get("pre_section_anchor_status", "") == "section_anchor_found"
    post_anchor = row.get("post_section_anchor_status", "") == "section_anchor_found"
    changed = row.get("normalized_text_hash_status", "") == "pre_post_normalized_text_changed"

    if marker and pre_anchor and post_anchor and changed and has_change_windows and has_post_context:
        return (
            "pre_post_target_section_review_packet_ready",
            "strong_pre_post_anchor_review_packet",
            "review_packet_only_not_source_reviewed_lineage_evidence",
            "Open the pre/post OLRC annual pages; verify the target heading and post-only public-law marker; compare the first-change windows against the target section; record whether the public law amended, added, repealed, redesignated, or only annotated the target.",
        )
    if marker and post_anchor and changed and has_change_windows and has_post_context:
        return (
            "added_or_relocated_section_review_packet_ready",
            "moderate_post_anchor_review_packet",
            "review_packet_only_not_source_reviewed_lineage_evidence",
            "Open the post OLRC annual page and source public law; verify whether the target was newly added, relocated, or not anchorable in the pre-edition; record the source-reviewed disposition before using it as codified lineage.",
        )
    return (
        "target_section_review_packet_needs_manual_source_retrieval",
        "not_review_ready",
        "no_review_packet_lineage_evidence",
        "Manually retrieve the relevant U.S. Code editions or public-law text before attempting target-section diff review.",
    )


def build_rows(adjudication_rows: list[dict[str, str]], text_diff_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    text_diff_by_rank = {
        row.get("text_diff_rank", "").strip(): row
        for row in text_diff_rows
        if row.get("text_diff_rank", "").strip()
    }
    rows: list[dict[str, str]] = []
    for index, adjudication_row in enumerate(adjudication_rows, start=1):
        text_diff_row = text_diff_by_rank.get(adjudication_row.get("text_diff_rank", "").strip(), {})
        status, strength, evidence_status, tasks = packet_status(adjudication_row)
        evidence_layers = split_values(adjudication_row.get("evidence_layers", ""))
        evidence_layers.append("statutory_lineage_target_section_review_packet")
        components = [
            "pre_olrc_annual_url",
            "post_olrc_annual_url",
            "pre_post_source_hashes",
            "normalized_section_text_hashes",
            "post_public_law_context_snippets",
            "first_changed_text_windows",
        ]
        rows.append({
            "target_review_packet_rank": str(index),
            "lineage_adjudication_rank": adjudication_row.get("lineage_adjudication_rank", ""),
            "text_diff_rank": adjudication_row.get("text_diff_rank", ""),
            "historical_scan_rank": adjudication_row.get("historical_scan_rank", ""),
            "current_olrc_scan_rank": adjudication_row.get("current_olrc_scan_rank", ""),
            "triage_rank": adjudication_row.get("triage_rank", ""),
            "source_scan_rank": adjudication_row.get("source_scan_rank", ""),
            "lineage_review_rank": adjudication_row.get("lineage_review_rank", ""),
            "bill_id": adjudication_row.get("bill_id", ""),
            "public_law_number": adjudication_row.get("public_law_number", ""),
            "enacted_date": adjudication_row.get("enacted_date", ""),
            "target_reference": adjudication_row.get("target_reference", ""),
            "target_reference_type": adjudication_row.get("target_reference_type", ""),
            "normalized_title": adjudication_row.get("normalized_title", ""),
            "normalized_section": adjudication_row.get("normalized_section", ""),
            "pre_edition": adjudication_row.get("pre_edition", ""),
            "post_edition": adjudication_row.get("post_edition", ""),
            "pre_olrc_url": adjudication_row.get("pre_olrc_url", ""),
            "post_olrc_url": adjudication_row.get("post_olrc_url", ""),
            "pre_text_sha256": text_diff_row.get("pre_text_sha256", ""),
            "post_text_sha256": text_diff_row.get("post_text_sha256", ""),
            "pre_normalized_text_sha256": text_diff_row.get("pre_normalized_text_sha256", ""),
            "post_normalized_text_sha256": text_diff_row.get("post_normalized_text_sha256", ""),
            "pre_section_anchor_status": adjudication_row.get("pre_section_anchor_status", ""),
            "post_section_anchor_status": adjudication_row.get("post_section_anchor_status", ""),
            "pre_public_law_reference_hits": adjudication_row.get("pre_public_law_reference_hits", ""),
            "post_public_law_reference_hits": adjudication_row.get("post_public_law_reference_hits", ""),
            "public_law_reference_hit_delta": adjudication_row.get("public_law_reference_hit_delta", ""),
            "normalized_text_hash_status": adjudication_row.get("normalized_text_hash_status", ""),
            "normalized_text_char_delta": text_diff_row.get("normalized_text_char_delta", ""),
            "section_change_cue_status": adjudication_row.get("section_change_cue_status", ""),
            "post_public_law_context_count": adjudication_row.get("post_public_law_context_count", ""),
            "post_public_law_context_snippets": adjudication_row.get("post_public_law_context_snippets", ""),
            "first_changed_text_pre_window": adjudication_row.get("first_changed_text_pre_window", ""),
            "first_changed_text_post_window": adjudication_row.get("first_changed_text_post_window", ""),
            "codified_lineage_marker": adjudication_row.get("codified_lineage_marker", ""),
            "lineage_adjudication_status": adjudication_row.get("lineage_adjudication_status", ""),
            "lineage_marker_strength": adjudication_row.get("lineage_marker_strength", ""),
            "target_section_diff_status": adjudication_row.get("target_section_diff_status", ""),
            "target_review_packet_status": status,
            "target_review_packet_strength": strength,
            "source_reviewed_target_section_diff": "0",
            "source_review_disposition": "not_source_reviewed_review_packet_only",
            "review_packet_components": joined(components),
            "review_task_list": tasks,
            "lineage_evidence_status": evidence_status,
            "evidence_layers": joined(evidence_layers),
            "missing_links": joined(MISSING_LINKS),
            "source_review_notes": (
                "This packet is readying material for human source review. It preserves "
                "official OLRC URLs, hashes, marker context, and bounded first-change "
                "windows, but it does not itself adjudicate the target-section diff."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], path: Path, adjudication_input: Path, text_diff_input: Path) -> None:
    status_counts = Counter(row["target_review_packet_status"] for row in rows)
    strength_counts = Counter(row["target_review_packet_strength"] for row in rows)
    ready_rows = [
        row for row in rows
        if row["target_review_packet_status"] != "target_section_review_packet_needs_manual_source_retrieval"
    ]
    write_reproducible_metadata(
        path,
        "\n".join([
            "# Statutory Lineage Target Review Packet Metadata",
            "",
            f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
            f"- adjudication_input: `{adjudication_input}`",
            f"- text_diff_input: `{text_diff_input}`",
            f"- output_rows: {len(rows)}",
            f"- review_ready_packet_rows: {len(ready_rows)}",
            f"- public_laws_with_review_ready_packets: {len({row['public_law_number'] for row in ready_rows})}",
            "",
            "Review packet statuses:",
            *[f"- {status}: {count}" for status, count in sorted(status_counts.items())],
            "",
            "Review packet strengths:",
            *[f"- {strength}: {count}" for strength, count in sorted(strength_counts.items())],
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
        ])
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adjudication-input", type=Path, default=ADJUDICATION)
    parser.add_argument("--text-diff-input", type=Path, default=TEXT_DIFF)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    adjudication_rows = read_csv(args.adjudication_input)
    if not adjudication_rows:
        raise SystemExit(f"{args.adjudication_input} has no rows.")
    text_diff_rows = read_csv(args.text_diff_input)
    if not text_diff_rows:
        raise SystemExit(f"{args.text_diff_input} has no rows.")
    rows = build_rows(adjudication_rows, text_diff_rows)
    write_csv(rows, args.output)
    write_metadata(rows, args.metadata, args.adjudication_input, args.text_diff_input)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
