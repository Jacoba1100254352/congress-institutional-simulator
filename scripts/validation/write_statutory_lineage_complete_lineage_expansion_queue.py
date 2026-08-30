#!/usr/bin/env python3
"""Write the next complete codified-lineage expansion queue."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


COMPLETION_QUEUE = Path("reports/statutory-lineage-completion-queue.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
TARGET_TRIAGE = Path("reports/statutory-lineage-target-section-triage.csv")
TARGET_REVIEW_PACKETS = Path("reports/statutory-lineage-target-review-packets.csv")
TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
EFFECTIVE_TEXT_REVIEW = Path("reports/statutory-lineage-effective-text-review.csv")
PUBLIC_LAW_ATTRIBUTION_REVIEW = Path("reports/statutory-lineage-public-law-attribution-review.csv")
OUT_CSV = Path("reports/statutory-lineage-complete-lineage-expansion-queue.csv")
OUT_MD = Path("reports/statutory-lineage-complete-lineage-expansion-queue.md")

CLAIM_BOUNDARY = (
    "Complete codified-lineage expansion queue only; rows quantify source-scan, "
    "target-triage, review-packet, source-reviewed target-section diff, "
    "effective-text, and bounded public-law attribution coverage so the next "
    "review pass can expand the U.S.C. lineage inventory. This artifact does "
    "not establish complete codified lineage, implementation outcomes, direct "
    "target-section court review, welfare evidence, causal effects, or model "
    "validation."
)

FIELDNAMES = [
    "expansion_rank",
    "completion_rank",
    "corpus_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "next_actionable_upgrade_gate",
    "completion_status",
    "complete_lineage_expansion_status",
    "expansion_priority_reason",
    "source_scan_usc_reference_count",
    "source_scan_target_candidate_count",
    "triage_rows",
    "triage_candidate_rows",
    "review_packet_rows",
    "target_diff_review_rows",
    "source_reviewed_target_section_diff_rows",
    "reviewed_no_exact_target_section_diff_rows",
    "reviewed_no_structured_usc_target_rows",
    "law_revision_effective_text_reviewed_rows",
    "public_law_causal_attribution_reviewed_rows",
    "source_candidate_count_minus_triage_rows",
    "triage_to_packet_gap_rows",
    "packet_to_positive_diff_gap_rows",
    "source_reviewed_diff_without_effective_text_rows",
    "source_reviewed_diff_without_attribution_rows",
    "target_references_with_source_review",
    "triage_references_needing_packet_review",
    "packet_references_needing_positive_source_review",
    "complete_lineage_review_scope",
    "next_complete_lineage_action",
    "remaining_completion_gates",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make statutory-lineage-completion-queue first.")
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


def by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id and bill_id not in result:
            result[bill_id] = row
    return result


def group_by_bill(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            result[bill_id].append(row)
    return result


def target_refs(rows: list[dict[str, str]]) -> list[str]:
    return [
        row.get("target_reference", "").strip()
        for row in rows
        if row.get("target_reference", "").strip()
        and row.get("target_reference", "").strip() != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
    ]


def expansion_status_and_action(
    completion_row: dict[str, str],
    source_candidate_gap: int,
    triage_packet_gap: int,
    packet_positive_gap: int,
    effective_text_gap: int,
    attribution_gap: int,
) -> tuple[str, str, str, str]:
    source_reviewed_rows = int_field(completion_row, "source_reviewed_target_section_diff_rows")
    no_target_rows = int_field(completion_row, "reviewed_no_structured_usc_target_rows")
    if no_target_rows and not source_reviewed_rows:
        return (
            "reviewed_no_structured_usc_target_no_complete_lineage_expansion",
            "reviewed designation-law/no-structured-U.S.C.-target disposition has no target-section inventory to expand",
            "Do not infer a codified U.S.C. target; pursue implementation, public-opinion, finance/lobbying, court, welfare, or model-validation evidence only where independently sourced.",
            "No structured U.S.C. target-section expansion scope is present for this reviewed designation-law disposition.",
        )
    if not source_reviewed_rows:
        return (
            "complete_lineage_expansion_waiting_for_source_reviewed_target_diff",
            "no positive source-reviewed target-section diff rows are available for complete-lineage expansion",
            "Resolve target-section diff review before attempting a complete codified-lineage inventory.",
            "Source-reviewed target-section diff review is required before a complete-lineage expansion scope can be defined.",
        )
    if effective_text_gap or attribution_gap:
        return (
            "source_reviewed_target_diff_missing_effective_text_or_attribution",
            "positive source-reviewed target-section diff rows still lack effective-text or public-law attribution coverage",
            "Finish effective-text and bounded public-law attribution review for every positive target-section diff row before expanding complete lineage.",
            "Expand only after every positive source-reviewed target-section diff has effective-text and bounded public-law attribution review.",
        )
    if source_candidate_gap > 0 or triage_packet_gap > 0:
        return (
            "source_reviewed_target_diff_attribution_reviewed_candidate_expansion_open",
            (
                f"{source_candidate_gap} GovInfo target-candidate mentions remain outside "
                f"the triage row count and {triage_packet_gap} triage references still lack "
                "review-packet coverage."
            ),
            "Expand the U.S.C. target inventory from source-scan candidates and triage rows, then build OLRC pre/post packets for any newly selected target references.",
            "Review source-scan candidate mentions, triage references without packets, OLRC pre/post sections, notes, related subsections, and cross-reference context before closing complete lineage.",
        )
    if packet_positive_gap > 0:
        return (
            "source_reviewed_target_diff_attribution_reviewed_packet_disposition_context_open",
            (
                f"{packet_positive_gap} review-packet rows are reviewed as related/no-exact-target "
                "or otherwise not positive source-reviewed target-section diffs."
            ),
            "Audit the non-positive packet dispositions and document why they do or do not belong in the complete codified-lineage inventory.",
            "Review packet-level no-exact-target dispositions, related-section context, notes, and cross-reference context before closing complete lineage.",
        )
    return (
        "source_reviewed_target_diff_attribution_reviewed_complete_lineage_audit_open",
        "positive source-reviewed target-section diff rows have effective-text and bounded public-law attribution coverage, but complete lineage still needs a final inventory audit",
        "Audit full U.S.C. lineage across notes, related subsections, amendments, repeals, redesignations, and cross-references before upgrading statutory-lineage claims.",
        "Review every positive target reference, related notes, related subsections, amendments, repeals, redesignations, and cross-reference context before closing complete lineage.",
    )


def build_rows() -> list[dict[str, str]]:
    completion_rows = read_csv(COMPLETION_QUEUE)
    source_by_bill = by_bill(read_csv(SOURCE_SCAN))
    triage_by_bill = group_by_bill(read_csv(TARGET_TRIAGE))
    packets_by_bill = group_by_bill(read_csv(TARGET_REVIEW_PACKETS))
    diff_by_bill = group_by_bill(read_csv(TARGET_DIFF_REVIEW))
    effective_by_bill = group_by_bill(read_csv(EFFECTIVE_TEXT_REVIEW))
    attribution_by_bill = group_by_bill(read_csv(PUBLIC_LAW_ATTRIBUTION_REVIEW))

    rows: list[dict[str, str]] = []
    for completion_row in sorted(
        completion_rows,
        key=lambda row: int_field(row, "completion_rank"),
    ):
        bill_id = completion_row.get("bill_id", "").strip()
        source_row = source_by_bill.get(bill_id, {})
        triage_rows = triage_by_bill.get(bill_id, [])
        packet_rows = packets_by_bill.get(bill_id, [])
        diff_rows = diff_by_bill.get(bill_id, [])
        effective_rows = [
            row for row in effective_by_bill.get(bill_id, [])
            if row.get("law_revision_effective_text_reviewed", "").strip() == "1"
        ]
        attribution_rows = [
            row for row in attribution_by_bill.get(bill_id, [])
            if row.get("public_law_causal_attribution_reviewed", "").strip() == "1"
        ]
        triage_candidates = [
            row for row in triage_rows
            if row.get("target_reference", "").strip()
            and row.get("target_reference", "").strip() != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
        ]
        source_reviewed_diff_rows = [
            row for row in diff_rows
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        no_exact_rows = [
            row for row in diff_rows
            if row.get("review_status", "").strip()
            == "reviewed_related_section_context_no_exact_target_diff"
        ]
        packet_refs = set(target_refs(packet_rows))
        source_reviewed_refs = set(target_refs(source_reviewed_diff_rows))
        triage_refs = set(target_refs(triage_candidates))
        source_candidate_count = int_field(source_row, "target_section_candidate_count")
        triage_candidate_count = len(triage_candidates)
        source_candidate_gap = max(source_candidate_count - triage_candidate_count, 0)
        triage_packet_gap = max(triage_candidate_count - len(packet_refs), 0)
        packet_positive_gap = max(len(packet_refs - source_reviewed_refs), 0)
        effective_text_gap = max(len(source_reviewed_diff_rows) - len(effective_rows), 0)
        attribution_gap = max(len(source_reviewed_diff_rows) - len(attribution_rows), 0)

        status, reason, action, scope = expansion_status_and_action(
            completion_row,
            source_candidate_gap,
            triage_packet_gap,
            packet_positive_gap,
            effective_text_gap,
            attribution_gap,
        )

        evidence_layers = ["statutory_lineage_complete_lineage_expansion_queue"]
        missing_links = split_values(completion_row.get("missing_links", ""))
        source_artifacts = [str(COMPLETION_QUEUE)]
        for source_rows, path in (
            ([source_row] if source_row else [], SOURCE_SCAN),
            (triage_rows, TARGET_TRIAGE),
            (packet_rows, TARGET_REVIEW_PACKETS),
            (diff_rows, TARGET_DIFF_REVIEW),
            (effective_rows, EFFECTIVE_TEXT_REVIEW),
            (attribution_rows, PUBLIC_LAW_ATTRIBUTION_REVIEW),
        ):
            if source_rows:
                source_artifacts.append(str(path))
                for row in source_rows:
                    evidence_layers.extend(split_values(row.get("evidence_layers", "")))
                    missing_links.extend(split_values(row.get("missing_links", "")))
        for required_gap in (
            "complete_codified_usc_lineage_review",
            "implementation_outcomes_or_enforcement",
            "direct_target_section_court_review",
            "welfare_or_public_benefit",
            "model_validation",
        ):
            if int_field(completion_row, "source_reviewed_target_section_diff_rows") > 0:
                missing_links.append(required_gap)
        if source_candidate_gap > 0 or triage_packet_gap > 0:
            missing_links.extend([
                "complete_target_reference_inventory",
                "unreviewed_source_scan_candidate_references",
            ])
        if packet_positive_gap > 0:
            missing_links.append("reviewed_packet_disposition_context_for_complete_lineage")

        rows.append({
            "expansion_rank": "0",
            "completion_rank": completion_row.get("completion_rank", "").strip(),
            "corpus_rank": completion_row.get("corpus_rank", "").strip(),
            "action_rank": completion_row.get("action_rank", "").strip(),
            "bill_id": bill_id,
            "public_law_number": completion_row.get("public_law_number", "").strip(),
            "policy_area": completion_row.get("policy_area", "").strip(),
            "next_actionable_upgrade_gate": completion_row.get("next_actionable_upgrade_gate", "").strip(),
            "completion_status": completion_row.get("completion_status", "").strip(),
            "complete_lineage_expansion_status": status,
            "expansion_priority_reason": reason,
            "source_scan_usc_reference_count": source_row.get("usc_reference_count", "0").strip(),
            "source_scan_target_candidate_count": source_row.get("target_section_candidate_count", "0").strip(),
            "triage_rows": str(len(triage_rows)),
            "triage_candidate_rows": str(triage_candidate_count),
            "review_packet_rows": str(len(packet_rows)),
            "target_diff_review_rows": str(len(diff_rows)),
            "source_reviewed_target_section_diff_rows": str(len(source_reviewed_diff_rows)),
            "reviewed_no_exact_target_section_diff_rows": str(len(no_exact_rows)),
            "reviewed_no_structured_usc_target_rows": completion_row.get(
                "reviewed_no_structured_usc_target_rows",
                "0",
            ).strip(),
            "law_revision_effective_text_reviewed_rows": str(len(effective_rows)),
            "public_law_causal_attribution_reviewed_rows": str(len(attribution_rows)),
            "source_candidate_count_minus_triage_rows": str(source_candidate_gap),
            "triage_to_packet_gap_rows": str(triage_packet_gap),
            "packet_to_positive_diff_gap_rows": str(packet_positive_gap),
            "source_reviewed_diff_without_effective_text_rows": str(effective_text_gap),
            "source_reviewed_diff_without_attribution_rows": str(attribution_gap),
            "target_references_with_source_review": unique_join(target_refs(source_reviewed_diff_rows)),
            "triage_references_needing_packet_review": unique_join(sorted(triage_refs - packet_refs)),
            "packet_references_needing_positive_source_review": unique_join(sorted(packet_refs - source_reviewed_refs)),
            "complete_lineage_review_scope": scope,
            "next_complete_lineage_action": action,
            "remaining_completion_gates": completion_row.get("remaining_completion_gates", "").strip(),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(source_artifacts),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    rows.sort(
        key=lambda row: (
            0 if row["next_actionable_upgrade_gate"] == "codified_usc_lineage" else 1,
            int(row["completion_rank"] or "999999"),
            row["bill_id"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["expansion_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["complete_lineage_expansion_status"] for row in rows)
    active_rows = [
        row for row in rows
        if row["next_actionable_upgrade_gate"] == "codified_usc_lineage"
    ]
    no_target_rows = [
        row for row in rows
        if int(row["reviewed_no_structured_usc_target_rows"] or "0") > 0
    ]
    source_reviewed_public_laws = [
        row for row in rows
        if int(row["source_reviewed_target_section_diff_rows"] or "0") > 0
    ]
    total_source_candidates = sum(
        int(row["source_scan_target_candidate_count"] or "0")
        for row in rows
    )
    total_triage_packet_gap = sum(
        int(row["triage_to_packet_gap_rows"] or "0")
        for row in rows
    )
    total_packet_positive_gap = sum(
        int(row["packet_to_positive_diff_gap_rows"] or "0")
        for row in rows
    )
    total_candidate_gap = sum(
        int(row["source_candidate_count_minus_triage_rows"] or "0")
        for row in rows
    )
    lines = [
        "# Statutory Lineage Complete Lineage Expansion Queue",
        "",
        "This report turns the open complete-codified-lineage gate into a concrete expansion queue. It joins the completion queue to source scan, target triage, review packets, source-reviewed target-section diffs, effective-text review, and bounded public-law attribution review. It remains a work queue, not complete lineage validation evidence.",
        "",
        f"- Complete-lineage expansion queue rows: {len(rows)}",
        f"- Active codified-lineage expansion rows: {len(active_rows)}",
        f"- Public laws with source-reviewed target-section diffs: {len(source_reviewed_public_laws)}",
        f"- Reviewed no-structured-U.S.C.-target rows retained: {len(no_target_rows)}",
        f"- Source-scan target candidates represented: {total_source_candidates}",
        f"- Source candidate count beyond triage rows: {total_candidate_gap}",
        f"- Triage references needing packet review: {total_triage_packet_gap}",
        f"- Packet references needing positive source-review disposition: {total_packet_positive_gap}",
        "",
        "Expansion statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Expansion status | Source candidates | Triage | Packets | Source-reviewed diffs | Candidate gap | Triage-packet gap | Next action |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['expansion_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['complete_lineage_expansion_status']} | "
            f"{row['source_scan_target_candidate_count']} | {row['triage_candidate_rows']} | "
            f"{row['review_packet_rows']} | {row['source_reviewed_target_section_diff_rows']} | "
            f"{row['source_candidate_count_minus_triage_rows']} | "
            f"{row['triage_to_packet_gap_rows']} | {row['next_complete_lineage_action']} |"
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
