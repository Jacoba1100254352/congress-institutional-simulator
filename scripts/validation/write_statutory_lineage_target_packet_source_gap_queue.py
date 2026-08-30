#!/usr/bin/env python3
"""Write source-gap blockers for target-packet expansion rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PACKET_EXPANSION_QUEUE = Path("reports/statutory-lineage-target-packet-expansion-queue.csv")
OLRC_CURRENT_SCAN = Path("reports/statutory-lineage-olrc-current-scan.csv")
OLRC_HISTORICAL_SCAN = Path("reports/statutory-lineage-olrc-historical-scan.csv")
OLRC_ANNUAL_TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
ADJUDICATION = Path("reports/statutory-lineage-adjudication.csv")
TARGET_REVIEW_PACKETS = Path("reports/statutory-lineage-target-review-packets.csv")
OUT_CSV = Path("reports/statutory-lineage-target-packet-source-gap-queue.csv")
OUT_MD = Path("reports/statutory-lineage-target-packet-source-gap-queue.md")

CLAIM_BOUNDARY = (
    "Target packet source-gap queue only; rows classify why already-triaged "
    "packet-expansion references did not advance into historical OLRC, annual "
    "text-diff, adjudication, or target-review packet layers. This artifact "
    "does not establish codified lineage, target-section text diffs, effective "
    "statutory text, public-law attribution, implementation outcomes, direct "
    "court review, welfare evidence, causal effects, or model validation."
)

FIELDNAMES = [
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
    "codification_review_status",
    "packet_gap_status",
    "current_olrc_scan_rank",
    "current_olrc_scan_status",
    "current_olrc_http_status",
    "current_olrc_url",
    "current_public_law_reference_status",
    "current_public_law_reference_hits",
    "historical_scan_present",
    "annual_text_diff_present",
    "adjudication_present",
    "target_review_packet_present",
    "source_gap_status",
    "source_gap_reason",
    "next_source_gap_action",
    "remaining_completion_gates",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make statutory-lineage-target-packet-expansion-queue first.")
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


def key_for(row: dict[str, str]) -> tuple[str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("target_reference", "").strip(),
    )


def rows_by_key(
    rows: list[dict[str, str]],
    path: Path,
) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = key_for(row)
        if not all(key):
            continue
        if key in result:
            raise SystemExit(f"{path}: duplicate bill/target key {key}")
        result[key] = row
    return result


def key_set(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {key for row in rows if all((key := key_for(row)))}


def source_gap_classification(
    current_row: dict[str, str],
    historical_present: bool,
    annual_present: bool,
    adjudication_present: bool,
    packet_present: bool,
) -> tuple[str, str, str]:
    current_status = current_row.get("olrc_scan_status", "").strip()
    public_law_status = current_row.get("public_law_reference_status", "").strip()
    if packet_present:
        return (
            "target_review_packet_already_present_reconcile_expansion_queue",
            "The target-review packet layer already contains this bill/reference key.",
            "Regenerate the expansion queue and reconcile stale packet-gap membership before further source review.",
        )
    if historical_present or annual_present or adjudication_present:
        return (
            "downstream_source_layer_present_without_target_review_packet",
            "At least one downstream OLRC source layer exists, but the target-review packet artifact is still absent.",
            "Reconcile historical, annual-diff, adjudication, and packet artifacts before treating this row as an open packet-construction task.",
        )
    if not current_row:
        return (
            "current_olrc_scan_missing_blocks_source_gap_review",
            "No current OLRC scan row is available for this packet-expansion reference.",
            "Regenerate current OLRC scans from target-section triage before building historical or packet layers.",
        )
    if (
        current_status == "official_olrc_current_section_page_fetched"
        and public_law_status == "current_page_no_public_law_mention"
    ):
        return (
            "current_olrc_page_fetched_without_public_law_marker_blocks_automated_packet",
            "The current OLRC section page was fetched, but the current page does not mention the queued public law.",
            "Manually review current and historical OLRC notes plus GovInfo public-law source text; do not build an annual pre/post packet unless the target is confirmed by an independent source or public-law marker.",
        )
    if current_status == "title_only_not_fetched":
        return (
            "title_only_reference_needs_section_resolution_before_packet",
            "The target reference is title-only, so there is no concrete OLRC section page to fetch.",
            "Resolve the title-only reference to a concrete section, note, or no-target disposition before OLRC packet construction.",
        )
    if current_status == "incomplete_or_nonsection_target_not_fetched":
        return (
            "incomplete_or_nonsection_reference_needs_manual_resolution_before_packet",
            "The target reference is incomplete or nonsectional, so automated current OLRC section lookup was not attempted.",
            "Resolve the incomplete or nonsection target against GovInfo public-law text before current, historical, or packet work.",
        )
    if (
        current_status == "official_olrc_current_section_page_fetched"
        and public_law_status == "current_page_mentions_public_law"
    ):
        return (
            "current_olrc_page_mentions_public_law_but_downstream_packet_absent",
            "The current OLRC page mentions the queued public law, but no historical scan, adjudication, or packet row exists.",
            "Regenerate historical OLRC, annual text-diff, adjudication, and target-review packet layers for this current-page candidate.",
        )
    return (
        "current_olrc_scan_status_needs_manual_source_gap_review",
        "The current OLRC scan status is not covered by the automated packet-source-gap categories.",
        "Manually inspect the current OLRC scan row and decide whether this reference needs section resolution, source review, or packet reconciliation.",
    )


def build_rows() -> list[dict[str, str]]:
    expansion_rows = read_csv(PACKET_EXPANSION_QUEUE)
    current_rows = read_csv(OLRC_CURRENT_SCAN)
    historical_rows = read_csv(OLRC_HISTORICAL_SCAN)
    annual_rows = read_csv(OLRC_ANNUAL_TEXT_DIFF)
    adjudication_rows = read_csv(ADJUDICATION)
    packet_rows = read_csv(TARGET_REVIEW_PACKETS)

    current_by_key = rows_by_key(current_rows, OLRC_CURRENT_SCAN)
    historical_keys = key_set(historical_rows)
    annual_keys = key_set(annual_rows)
    adjudication_keys = key_set(adjudication_rows)
    packet_keys = key_set(packet_rows)

    rows: list[dict[str, str]] = []
    for expansion_row in sorted(
        expansion_rows,
        key=lambda row: int_field(row, "packet_expansion_rank"),
    ):
        key = key_for(expansion_row)
        current_row = current_by_key.get(key, {})
        historical_present = key in historical_keys
        annual_present = key in annual_keys
        adjudication_present = key in adjudication_keys
        packet_present = key in packet_keys
        source_gap_status, source_gap_reason, next_action = source_gap_classification(
            current_row=current_row,
            historical_present=historical_present,
            annual_present=annual_present,
            adjudication_present=adjudication_present,
            packet_present=packet_present,
        )

        evidence_layers = [
            "statutory_lineage_target_packet_source_gap_queue",
            "statutory_lineage_target_packet_expansion_queue",
        ]
        missing_links = [
            "manual_source_resolution_for_packet_gap",
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "complete_codified_usc_lineage_review",
            "model_validation",
        ]
        for source_row in (expansion_row, current_row):
            evidence_layers.extend(split_values(source_row.get("evidence_layers", "")))
            missing_links.extend(split_values(source_row.get("missing_links", "")))

        source_artifacts = [
            str(PACKET_EXPANSION_QUEUE),
            str(OLRC_CURRENT_SCAN),
            str(OLRC_HISTORICAL_SCAN),
            str(OLRC_ANNUAL_TEXT_DIFF),
            str(ADJUDICATION),
            str(TARGET_REVIEW_PACKETS),
        ]

        rows.append({
            "source_gap_rank": "0",
            "packet_expansion_rank": expansion_row.get("packet_expansion_rank", "").strip(),
            "expansion_rank": expansion_row.get("expansion_rank", "").strip(),
            "completion_rank": expansion_row.get("completion_rank", "").strip(),
            "triage_rank": expansion_row.get("triage_rank", "").strip(),
            "source_scan_rank": expansion_row.get("source_scan_rank", "").strip(),
            "bill_id": expansion_row.get("bill_id", "").strip(),
            "public_law_number": expansion_row.get("public_law_number", "").strip(),
            "policy_area": expansion_row.get("policy_area", "").strip(),
            "target_reference": expansion_row.get("target_reference", "").strip(),
            "target_reference_type": expansion_row.get("target_reference_type", "").strip(),
            "codification_review_status": expansion_row.get("codification_review_status", "").strip(),
            "packet_gap_status": expansion_row.get("packet_gap_status", "").strip(),
            "current_olrc_scan_rank": current_row.get("olrc_scan_rank", "").strip(),
            "current_olrc_scan_status": current_row.get("olrc_scan_status", "").strip(),
            "current_olrc_http_status": current_row.get("http_status", "").strip(),
            "current_olrc_url": current_row.get("olrc_url", "").strip(),
            "current_public_law_reference_status": current_row.get("public_law_reference_status", "").strip(),
            "current_public_law_reference_hits": current_row.get("public_law_reference_hits", "").strip(),
            "historical_scan_present": "1" if historical_present else "0",
            "annual_text_diff_present": "1" if annual_present else "0",
            "adjudication_present": "1" if adjudication_present else "0",
            "target_review_packet_present": "1" if packet_present else "0",
            "source_gap_status": source_gap_status,
            "source_gap_reason": source_gap_reason,
            "next_source_gap_action": next_action,
            "remaining_completion_gates": expansion_row.get("remaining_completion_gates", "").strip(),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(source_artifacts),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    rows.sort(
        key=lambda row: (
            int(row["packet_expansion_rank"] or "999999"),
            row["target_reference"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["source_gap_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["source_gap_status"] for row in rows)
    bill_counts = Counter(row["bill_id"] for row in rows)
    lines = [
        "# Statutory Lineage Target Packet Source-Gap Queue",
        "",
        "This report classifies why target-packet expansion rows have not advanced into downstream historical OLRC, annual text-diff, adjudication, or target-review packet layers. It is a blocker queue, not codified-lineage evidence.",
        "",
        f"- Target packet source-gap queue rows: {len(rows)}",
        f"- Public laws with source-gap rows: {len(bill_counts)}",
        "- Current OLRC pages fetched without public-law marker: "
        f"{status_counts.get('current_olrc_page_fetched_without_public_law_marker_blocks_automated_packet', 0)}",
        "- Title-only references needing section resolution: "
        f"{status_counts.get('title_only_reference_needs_section_resolution_before_packet', 0)}",
        "- Incomplete or nonsection references needing manual resolution: "
        f"{status_counts.get('incomplete_or_nonsection_reference_needs_manual_resolution_before_packet', 0)}",
        "",
        "Source-gap statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Packet rank | Bill | Public law | Target reference | Source-gap status | Current OLRC status | Next action |",
        "| ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['source_gap_rank']} | {row['packet_expansion_rank']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['source_gap_status']} | "
            f"{row['current_olrc_scan_status']} / {row['current_public_law_reference_status']} | "
            f"{row['next_source_gap_action']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No target packet source-gap rows were generated.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
