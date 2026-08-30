#!/usr/bin/env python3
"""Write the next codified-lineage completion queue from reviewed pilot rows."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LIFECYCLE_CORPUS = Path("reports/bill-law-lifecycle-corpus.csv")
CODIFIED_PROGRESS = Path("reports/statutory-lineage-codified-progress.csv")
TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
TARGET_LIFECYCLE_BRIDGE = Path("reports/statutory-lineage-target-lifecycle-bridge.csv")
EFFECTIVE_TEXT_REVIEW = Path("reports/statutory-lineage-effective-text-review.csv")
PUBLIC_LAW_ATTRIBUTION_REVIEW = Path("reports/statutory-lineage-public-law-attribution-review.csv")
OUT_CSV = Path("reports/statutory-lineage-completion-queue.csv")
OUT_MD = Path("reports/statutory-lineage-completion-queue.md")

CLAIM_BOUNDARY = (
    "Codified-lineage completion queue only; rows rank remaining source-review "
    "tasks after the bounded target-section diff, effective-text, and "
    "public-law attribution pilots. These artifacts are not complete codified "
    "lineage, implementation outcomes, direct target-section court review, "
    "welfare evidence, causal effects, or model validation."
)

FIELDNAMES = [
    "completion_rank",
    "corpus_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "next_actionable_upgrade_gate",
    "codified_progress_status",
    "completion_status",
    "completion_priority_reason",
    "target_diff_review_rows",
    "source_reviewed_target_section_diff_rows",
    "reviewed_no_exact_target_section_diff_rows",
    "reviewed_no_structured_usc_target_rows",
    "target_references",
    "codified_lineage_relationships",
    "added_target_section_rows",
    "amended_existing_target_section_rows",
    "effective_date_note_rows",
    "law_revision_effective_text_reviewed_rows",
    "public_law_causal_attribution_reviewed_rows",
    "target_lifecycle_bridge_rows",
    "authority_exact_target_reference_rows",
    "authority_base_section_rows",
    "court_exact_target_reference_rows",
    "court_base_section_rows",
    "court_direct_review_status",
    "remaining_completion_gates",
    "next_completion_action",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]

UNREVIEWED_CAUSATION_STATUS = "not_reviewed_for_exclusive_public_law_causation"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make statutory-lineage-codified-progress first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


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


def remaining_gates(
    source_reviewed_rows: int,
    no_target_rows: int,
    effective_text_rows: int,
    causal_attribution_rows: int,
    court_exact_rows: int,
) -> list[str]:
    if no_target_rows and not source_reviewed_rows:
        return [
            "implementation_or_comment_evidence_if_applicable",
            "direct_court_review_if_applicable",
            "public_law_non_target_status_claim_boundary",
            "model_validation",
        ]
    gates = [
        "complete_codified_usc_lineage_review",
        "law_revision_effective_text",
        "public_law_causal_attribution",
        "implementation_outcomes_or_enforcement",
        "direct_target_section_court_review",
        "welfare_or_public_benefit",
        "model_validation",
    ]
    if source_reviewed_rows <= 0:
        gates.insert(0, "source_reviewed_target_section_diff")
    if source_reviewed_rows > 0 and effective_text_rows >= source_reviewed_rows:
        gates.remove("law_revision_effective_text")
    if source_reviewed_rows > 0 and causal_attribution_rows >= source_reviewed_rows:
        gates.remove("public_law_causal_attribution")
    if court_exact_rows > 0:
        gates.remove("direct_target_section_court_review")
    return gates


def status_and_action(
    progress: dict[str, str],
    source_reviewed_rows: int,
    no_target_rows: int,
    effective_text_rows: int,
    causal_attribution_rows: int,
) -> tuple[str, str, str]:
    status = progress.get("codified_progress_status", "").strip()
    if no_target_rows and not source_reviewed_rows:
        return (
            "reviewed_no_structured_usc_target_lineage_not_applicable",
            "reviewed designation-law no-target disposition closes target-section diff review for this row",
            "Do not infer a codified U.S.C. target; pursue implementation, comment, opinion, finance/lobbying, or court evidence only where separately sourced.",
        )
    if source_reviewed_rows and effective_text_rows == 0 and causal_attribution_rows == 0:
        return (
            "source_reviewed_target_diff_present_effective_text_and_causation_unreviewed",
            "source-reviewed target-section diff rows exist, but every row still lacks effective-text and public-law causal-attribution review",
            "Review current/effective U.S. Code text and source notes for each target reference; then separately code public-law causal attribution and any implementation or court links.",
        )
    if source_reviewed_rows and effective_text_rows == 0:
        return (
            "source_reviewed_target_diff_present_effective_text_unreviewed",
            "source-reviewed target-section diff rows exist, but law-revision effective text has not been reviewed",
            "Review effective text and current codified text for each target reference before making stronger statutory-lineage claims.",
        )
    if source_reviewed_rows and effective_text_rows >= source_reviewed_rows and causal_attribution_rows == 0:
        return (
            "source_reviewed_target_diff_and_effective_text_present_causation_unreviewed",
            "source-reviewed target-section diff rows and effective-text source review rows exist, but public-law causal attribution has not been reviewed",
            "Review source notes and statutory history for exclusive public-law causal attribution; then separately code implementation outcomes and any direct target-section court links.",
        )
    if (
        source_reviewed_rows
        and effective_text_rows >= source_reviewed_rows
        and causal_attribution_rows >= source_reviewed_rows
    ):
        return (
            "source_reviewed_target_diff_effective_text_and_public_law_attribution_reviewed_completion_gates_open",
            "source-reviewed target-section diff, effective-text source review, and bounded public-law attribution review rows exist, but completion, implementation, court, welfare, and model-validation gates remain open",
            "Audit complete codified U.S.C. lineage, implementation outcomes, direct target-section court links, welfare/public-benefit evidence, and model-validation boundaries before upgrading paper claims.",
        )
    if source_reviewed_rows and causal_attribution_rows > 0:
        return (
            "source_reviewed_target_diff_present_partial_public_law_attribution_review",
            "some source-reviewed target-section diff rows have public-law attribution review, but the bill is not complete",
            "Complete public-law attribution review for every source-reviewed target-section diff row before moving to implementation, direct court links, and model-validation boundaries.",
        )
    if source_reviewed_rows:
        return (
            "source_reviewed_target_diff_present_needs_completion_audit",
            "target-section diff rows exist but remaining completion gates still need audit",
            "Audit public-law causation, implementation outcomes, court review, and claim boundaries before upgrading any paper claim.",
        )
    if status:
        return (
            "codified_lineage_completion_not_started_or_unresolved",
            "codified progress row exists but no positive source-reviewed target-section diff is attached",
            progress.get("next_codified_lineage_action", "").strip()
            or "Resolve source-review dispositions before treating this row as statutory-lineage evidence.",
        )
    return (
        "codified_lineage_completion_missing_progress_row",
        "no codified-progress row is attached",
        "Regenerate statutory-lineage progress artifacts before reviewing this row.",
    )


def build_rows() -> list[dict[str, str]]:
    corpus_rows = read_csv(LIFECYCLE_CORPUS)
    progress_rows = read_csv(CODIFIED_PROGRESS)
    diff_rows = read_csv(TARGET_DIFF_REVIEW)
    bridge_rows = read_csv(TARGET_LIFECYCLE_BRIDGE)
    effective_text_review_rows = read_csv(EFFECTIVE_TEXT_REVIEW)
    public_law_attribution_review_rows = read_csv(PUBLIC_LAW_ATTRIBUTION_REVIEW)
    if not corpus_rows or not progress_rows:
        raise SystemExit("Lifecycle corpus and codified progress rows are required.")

    corpus_by_bill = by_bill(corpus_rows)
    diffs_by_bill = group_by_bill(diff_rows)
    bridge_by_bill = group_by_bill(bridge_rows)
    effective_text_review_by_bill = group_by_bill(effective_text_review_rows)
    public_law_attribution_review_by_bill = group_by_bill(public_law_attribution_review_rows)

    rows: list[dict[str, str]] = []
    for progress in sorted(progress_rows, key=lambda row: int_field(row, "progress_rank")):
        bill_id = progress.get("bill_id", "").strip()
        corpus = corpus_by_bill.get(bill_id, {})
        bill_diffs = diffs_by_bill.get(bill_id, [])
        bill_bridge = bridge_by_bill.get(bill_id, [])
        bill_effective_text_review = effective_text_review_by_bill.get(bill_id, [])
        bill_public_law_attribution_review = public_law_attribution_review_by_bill.get(bill_id, [])
        source_reviewed_rows = [
            row for row in bill_diffs
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        no_exact_rows = [
            row for row in bill_diffs
            if row.get("review_status", "").strip()
            == "reviewed_related_section_context_no_exact_target_diff"
        ]
        effective_text_rows = [
            row for row in bill_effective_text_review
            if row.get("law_revision_effective_text_reviewed", "").strip() == "1"
        ]
        causal_attribution_rows = [
            row for row in bill_public_law_attribution_review
            if row.get("public_law_causal_attribution_reviewed", "").strip() == "1"
            and row.get("public_law_causal_attribution", "").strip()
            and row.get("public_law_causal_attribution", "").strip() != UNREVIEWED_CAUSATION_STATUS
        ]
        relationships = [
            row.get("codified_lineage_relationship", "").strip()
            for row in bill_diffs
            if row.get("codified_lineage_relationship", "").strip()
        ]
        target_refs = [
            row.get("target_reference", "").strip()
            for row in bill_diffs
            if row.get("target_reference", "").strip()
        ]
        added_rows = [
            row for row in source_reviewed_rows
            if row.get("codified_lineage_relationship", "").startswith("added_target_section")
        ]
        amended_rows = [
            row for row in source_reviewed_rows
            if row.get("codified_lineage_relationship", "").startswith("amended_existing_target_section")
        ]
        effective_date_note_rows = [
            row for row in source_reviewed_rows
            if "effective_date_note" in row.get("codified_lineage_relationship", "")
        ]
        no_target_rows = int_field(progress, "reviewed_no_structured_usc_target_rows")
        court_exact_rows = int_field(progress, "court_exact_target_reference_rows")
        completion_status, priority_reason, next_action = status_and_action(
            progress,
            len(source_reviewed_rows),
            no_target_rows,
            len(effective_text_rows),
            len(causal_attribution_rows),
        )
        gates = remaining_gates(
            len(source_reviewed_rows),
            no_target_rows,
            len(effective_text_rows),
            len(causal_attribution_rows),
            court_exact_rows,
        )
        evidence_layers = ["statutory_lineage_completion_queue"]
        missing_links = list(gates)
        source_artifacts = [
            str(LIFECYCLE_CORPUS),
            str(CODIFIED_PROGRESS),
        ]
        for source_rows, path in (
            ([corpus] if corpus else [], LIFECYCLE_CORPUS),
            ([progress], CODIFIED_PROGRESS),
            (bill_diffs, TARGET_DIFF_REVIEW),
            (bill_bridge, TARGET_LIFECYCLE_BRIDGE),
            (bill_effective_text_review, EFFECTIVE_TEXT_REVIEW),
            (bill_public_law_attribution_review, PUBLIC_LAW_ATTRIBUTION_REVIEW),
        ):
            if source_rows:
                source_artifacts.append(str(path))
                for row in source_rows:
                    evidence_layers.extend(split_values(row.get("evidence_layers", "")))
                    missing_links.extend(split_values(row.get("missing_links", "")))

        rows.append({
            "completion_rank": "0",
            "corpus_rank": corpus.get("corpus_rank", ""),
            "action_rank": progress.get("action_rank", ""),
            "bill_id": bill_id,
            "public_law_number": progress.get("public_law_number", ""),
            "policy_area": progress.get("policy_area", ""),
            "next_actionable_upgrade_gate": corpus.get("next_actionable_upgrade_gate", ""),
            "codified_progress_status": progress.get("codified_progress_status", ""),
            "completion_status": completion_status,
            "completion_priority_reason": priority_reason,
            "target_diff_review_rows": str(len(bill_diffs)),
            "source_reviewed_target_section_diff_rows": str(len(source_reviewed_rows)),
            "reviewed_no_exact_target_section_diff_rows": str(len(no_exact_rows)),
            "reviewed_no_structured_usc_target_rows": str(no_target_rows),
            "target_references": unique_join(target_refs),
            "codified_lineage_relationships": unique_join(relationships),
            "added_target_section_rows": str(len(added_rows)),
            "amended_existing_target_section_rows": str(len(amended_rows)),
            "effective_date_note_rows": str(len(effective_date_note_rows)),
            "law_revision_effective_text_reviewed_rows": str(len(effective_text_rows)),
            "public_law_causal_attribution_reviewed_rows": str(len(causal_attribution_rows)),
            "target_lifecycle_bridge_rows": str(len(bill_bridge)),
            "authority_exact_target_reference_rows": progress.get("authority_exact_target_reference_rows", "0"),
            "authority_base_section_rows": progress.get("authority_base_section_rows", "0"),
            "court_exact_target_reference_rows": progress.get("court_exact_target_reference_rows", "0"),
            "court_base_section_rows": progress.get("court_base_section_rows", "0"),
            "court_direct_review_status": progress.get("court_direct_review_status", ""),
            "remaining_completion_gates": unique_join(gates),
            "next_completion_action": next_action,
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(source_artifacts),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    rows.sort(
        key=lambda row: (
            0 if row["next_actionable_upgrade_gate"] == "codified_usc_lineage" else 1,
            int(row["corpus_rank"] or row["action_rank"] or "999999"),
            row["bill_id"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["completion_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["completion_status"] for row in rows)
    active_codified_rows = [
        row for row in rows
        if row["next_actionable_upgrade_gate"] == "codified_usc_lineage"
    ]
    source_reviewed_laws = [
        row for row in rows
        if int(row["source_reviewed_target_section_diff_rows"] or "0") > 0
    ]
    no_target_rows = [
        row for row in rows
        if int(row["reviewed_no_structured_usc_target_rows"] or "0") > 0
    ]
    effective_text_laws = [
        row for row in rows
        if int(row["law_revision_effective_text_reviewed_rows"] or "0") > 0
    ]
    causal_laws = [
        row for row in rows
        if int(row["public_law_causal_attribution_reviewed_rows"] or "0") > 0
    ]
    total_source_reviewed_diff_rows = sum(
        int(row["source_reviewed_target_section_diff_rows"] or "0")
        for row in rows
    )
    total_effective_date_notes = sum(
        int(row["effective_date_note_rows"] or "0")
        for row in rows
    )
    lines = [
        "# Statutory Lineage Completion Queue",
        "",
        "This report ranks the current codified-lineage candidates for the next completion pass. It starts from the lifecycle corpus and codified-progress classifier, then records whether source-reviewed target-section diffs still lack effective-text or public-law attribution review. It is a work queue, not complete statutory-lineage validation evidence.",
        "",
        f"- Completion queue rows: {len(rows)}",
        f"- Active codified-lineage next-gate rows: {len(active_codified_rows)}",
        f"- Public laws with source-reviewed target-section diffs: {len(source_reviewed_laws)}",
        f"- Source-reviewed target-section diff rows represented: {total_source_reviewed_diff_rows}",
        f"- Public laws with reviewed no-structured-U.S.C.-target disposition: {len(no_target_rows)}",
        f"- Source-reviewed diff rows with effective-date note relationship: {total_effective_date_notes}",
        f"- Public laws with law-revision effective text reviewed: {len(effective_text_laws)}",
        f"- Public laws with public-law causal attribution reviewed: {len(causal_laws)}",
        "",
        "Completion statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Completion status | Source-reviewed diffs | Effective text reviewed | Causal attribution reviewed | Remaining gates |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['completion_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['completion_status']} | {row['source_reviewed_target_section_diff_rows']} | "
            f"{row['law_revision_effective_text_reviewed_rows']} | "
            f"{row['public_law_causal_attribution_reviewed_rows']} | "
            f"{row['remaining_completion_gates']} |"
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
