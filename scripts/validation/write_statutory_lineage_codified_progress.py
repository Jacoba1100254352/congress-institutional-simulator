#!/usr/bin/env python3
"""Write codified-lineage progress status for lifecycle candidates."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
NO_TARGET_REVIEW = Path("reports/statutory-lineage-no-target-review.csv")
TARGET_TRIAGE = Path("reports/statutory-lineage-target-section-triage.csv")
TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
TARGET_LIFECYCLE_BRIDGE = Path("reports/statutory-lineage-target-lifecycle-bridge.csv")
OUT_CSV = Path("reports/statutory-lineage-codified-progress.csv")
OUT_MD = Path("reports/statutory-lineage-codified-progress.md")

CLAIM_BOUNDARY = (
    "Codified-lineage progress status only; rows classify whether the current "
    "lifecycle candidate has source-reviewed target-section diff rows, reviewed "
    "related-section/no-exact-target dispositions, unresolved target-section "
    "review rows, reviewed designation-law no-structured-U.S.C.-target "
    "dispositions, or an unresolved official public-law source scan with no "
    "structured U.S.C. target. This report does not establish full codified "
    "lineage, public-law causal attribution, law-revision effective text, "
    "implementation outcomes, direct court review, welfare, causal effects, or "
    "model validation."
)

FIELDNAMES = [
    "progress_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "codified_progress_status",
    "codified_progress_summary",
    "revision_flags",
    "source_scan_usc_reference_count",
    "source_scan_target_candidate_count",
    "source_scan_no_structured_usc_target",
    "reviewed_no_structured_usc_target_rows",
    "triage_rows",
    "triage_no_structured_target_rows",
    "triage_candidate_rows",
    "target_diff_review_rows",
    "source_reviewed_target_section_diff_rows",
    "reviewed_no_exact_target_section_diff_rows",
    "unresolved_target_section_review_rows",
    "target_lifecycle_bridge_rows",
    "authority_exact_target_reference_rows",
    "authority_base_section_rows",
    "court_exact_target_reference_rows",
    "court_base_section_rows",
    "court_direct_review_status",
    "closed_review_gates",
    "next_codified_lineage_action",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make validation-gap-report first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def rows_by_public_law(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            grouped[public_law].append(row)
    return grouped


def first_by_public_law(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("public_law_number", "").strip(): row
        for row in rows
        if row.get("public_law_number", "").strip()
    }


def status_for(
    source_scan: dict[str, str],
    no_target_review_rows: list[dict[str, str]],
    triage_rows: list[dict[str, str]],
    diff_rows: list[dict[str, str]],
) -> tuple[str, str, str]:
    source_reviewed = [
        row for row in diff_rows
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
    ]
    no_exact_target = [
        row for row in diff_rows
        if row.get("review_status", "").strip() == "reviewed_related_section_context_no_exact_target_diff"
    ]
    unresolved = [
        row for row in diff_rows
        if row.get("source_reviewed_target_section_diff", "").strip() != "1"
        and row.get("review_status", "").strip() != "reviewed_related_section_context_no_exact_target_diff"
    ]
    no_structured_target = (
        parse_int(source_scan.get("usc_reference_count", "0")) == 0
        and parse_int(source_scan.get("target_section_candidate_count", "0")) == 0
    )
    no_target_triage = [
        row for row in triage_rows
        if row.get("target_reference", "").strip() == "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
    ]

    reviewed_no_structured = [
        row for row in no_target_review_rows
        if row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
    ]

    if source_reviewed:
        status = "source_reviewed_target_section_diff_pilot_present"
        summary = (
            f"{len(source_reviewed)} source-reviewed target-section diff rows "
            f"attached; {len(no_exact_target)} reviewed no-exact-target rows and "
            f"{len(unresolved)} unresolved rows also attached."
        )
        action = (
            "Expand from source-reviewed target-section diffs to complete "
            "codified-lineage review, effective text, and causal-attribution "
            "checks before making stronger statutory-lineage claims."
        )
    elif diff_rows:
        if no_exact_target and not unresolved:
            status = "reviewed_related_section_context_no_exact_target_diff_only"
            summary = (
                f"{len(no_exact_target)} target-section review rows exist, but "
                "each is a reviewed related-section/no-exact-target disposition."
            )
            action = (
                "Treat as reviewed context only unless later OLRC notes or public-law "
                "text identify a direct target-section diff."
            )
        else:
            status = "target_section_diff_review_unresolved_only"
            summary = (
                f"{len(diff_rows)} target-section review rows exist, but none are "
                "currently source-reviewed positive diffs."
            )
            action = (
                "Resolve target-section cue review before treating this public law "
                "as codified-lineage evidence."
            )
    elif reviewed_no_structured:
        status = "reviewed_designation_law_no_structured_usc_target"
        summary = (
            f"{len(reviewed_no_structured)} source-reviewed no-structured-U.S.C.-target "
            "designation-law disposition rows attached; no target-section diff is applicable."
        )
        action = (
            "Treat target-section diff review as not applicable for the reviewed "
            "designation law; pursue remaining implementation, comments, public-opinion, "
            "finance/lobbying, court, or model-validation gaps without inferring a "
            "U.S.C. target."
        )
    elif no_structured_target or no_target_triage:
        status = "official_source_scan_no_structured_usc_target"
        summary = (
            "Official GovInfo public-law scan and target triage expose no "
            "structured U.S.C. target reference for this candidate."
        )
        action = (
            "Review OLRC classification or U.S. Code notes for a no-target or "
            "designation-law disposition; do not infer target-section text diffs "
            "from Federal Register authority overlap."
        )
    elif triage_rows:
        status = "target_section_triage_ready_needs_diff_review"
        summary = (
            f"{len(triage_rows)} target-triage rows exist but no source-reviewed "
            "target-section diff disposition is attached."
        )
        action = (
            "Build official OLRC pre/post target-section packets and attach "
            "source-reviewed diff dispositions."
        )
    else:
        status = "codified_lineage_review_not_started"
        summary = "No source-scan, triage, or target-section diff review rows were found."
        action = "Run statutory-lineage source scan and target-section triage first."
    return status, summary, action


def build_rows() -> list[dict[str, str]]:
    next_action_rows = read_csv(NEXT_ACTIONS)
    no_target_review_rows = read_csv(NO_TARGET_REVIEW)
    reviewed_no_target_public_laws = {
        row.get("public_law_number", "").strip()
        for row in no_target_review_rows
        if row.get("public_law_number", "").strip()
        and row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
    }
    actions = [
        row for row in next_action_rows
        if row.get("next_actionable_upgrade_gate", "").strip() == "codified_usc_lineage"
        or row.get("public_law_number", "").strip() in reviewed_no_target_public_laws
    ]
    if not actions:
        raise SystemExit(
            f"{NEXT_ACTIONS} has no codified_usc_lineage action rows and "
            f"{NO_TARGET_REVIEW} has no reviewed no-target rows."
        )
    source_by_pl = first_by_public_law(read_csv(SOURCE_SCAN))
    no_target_by_pl = rows_by_public_law(no_target_review_rows)
    triage_by_pl = rows_by_public_law(read_csv(TARGET_TRIAGE))
    diff_by_pl = rows_by_public_law(read_csv(TARGET_DIFF_REVIEW))
    bridge_by_pl = rows_by_public_law(read_csv(TARGET_LIFECYCLE_BRIDGE))

    rows: list[dict[str, str]] = []
    for index, action in enumerate(
        sorted(actions, key=lambda row: parse_int(row.get("action_rank", ""))),
        start=1,
    ):
        public_law = action.get("public_law_number", "").strip()
        source_scan = source_by_pl.get(public_law, {})
        no_target_review_rows = no_target_by_pl.get(public_law, [])
        triage_rows = triage_by_pl.get(public_law, [])
        diff_rows = diff_by_pl.get(public_law, [])
        bridge_rows = bridge_by_pl.get(public_law, [])
        status, summary, next_action = status_for(
            source_scan,
            no_target_review_rows,
            triage_rows,
            diff_rows,
        )
        source_reviewed = [
            row for row in diff_rows
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        no_exact_target = [
            row for row in diff_rows
            if row.get("review_status", "").strip() == "reviewed_related_section_context_no_exact_target_diff"
        ]
        unresolved = [
            row for row in diff_rows
            if row.get("source_reviewed_target_section_diff", "").strip() != "1"
            and row.get("review_status", "").strip() != "reviewed_related_section_context_no_exact_target_diff"
        ]
        no_target_triage = [
            row for row in triage_rows
            if row.get("target_reference", "").strip() == "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
        ]
        source_scan_no_structured_target = (
            parse_int(source_scan.get("usc_reference_count", "0")) == 0
            and parse_int(source_scan.get("target_section_candidate_count", "0")) == 0
        )
        reviewed_no_structured = [
            row for row in no_target_review_rows
            if row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
        ]
        candidate_triage = [
            row for row in triage_rows
            if row.get("target_reference", "").strip() != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
        ]
        authority_exact = [
            row for row in bridge_rows
            if row.get("authority_exact_target_reference_match", "").strip() == "1"
        ]
        authority_base = [
            row for row in bridge_rows
            if row.get("authority_base_section_match", "").strip() == "1"
        ]
        court_exact = [
            row for row in bridge_rows
            if row.get("court_exact_target_reference_overlap", "").strip() == "1"
        ]
        court_base = [
            row for row in bridge_rows
            if row.get("court_base_section_overlap", "").strip() == "1"
        ]
        evidence_layers = [
            "bill_law_lifecycle_next_actions",
            "statutory_lineage_source_scan",
            "statutory_lineage_codified_progress_status",
        ]
        if triage_rows:
            evidence_layers.append("statutory_lineage_target_section_triage")
        if no_target_review_rows:
            evidence_layers.append("statutory_lineage_no_target_review")
        if reviewed_no_structured:
            evidence_layers.append("statutory_lineage_source_reviewed_no_structured_usc_target")
        if diff_rows:
            evidence_layers.append("statutory_lineage_target_section_diff_review")
        if source_reviewed:
            evidence_layers.append("statutory_lineage_source_reviewed_target_section_diff")
        if bridge_rows:
            evidence_layers.append("statutory_lineage_target_lifecycle_bridge_context")
        if reviewed_no_structured:
            missing_links = [
                "target_section_diff_not_applicable_designation_law",
                "public_law_causal_attribution_not_applicable_no_target",
                "law_revision_effective_text_not_applicable_no_target",
                "implementation_outcomes_or_enforcement",
                "complete_regulations_comments",
                "direct_target_section_court_review_not_applicable_no_target",
                "welfare_or_public_benefit",
                "model_validation",
            ]
        else:
            missing_links = [
                "complete_codified_usc_lineage_review",
                "public_law_causal_attribution",
                "law_revision_effective_text",
                "implementation_outcomes_or_enforcement",
                "complete_regulations_comments",
                "direct_target_section_court_review",
                "welfare_or_public_benefit",
                "model_validation",
            ]
        if status == "official_source_scan_no_structured_usc_target":
            missing_links.insert(0, "olrc_no_target_classification_review")
        elif no_exact_target and not source_reviewed:
            missing_links.insert(0, "exact_target_section_text_diff")
        elif not source_reviewed:
            missing_links.insert(0, "source_reviewed_target_section_diff")
        rows.append({
            "progress_rank": str(index),
            "action_rank": action.get("action_rank", "").strip(),
            "bill_id": action.get("bill_id", "").strip(),
            "public_law_number": public_law,
            "policy_area": action.get("policy_area", "").strip(),
            "codified_progress_status": status,
            "codified_progress_summary": summary,
            "revision_flags": source_scan.get("revision_flags", "").strip(),
            "source_scan_usc_reference_count": source_scan.get("usc_reference_count", "0").strip(),
            "source_scan_target_candidate_count": source_scan.get("target_section_candidate_count", "0").strip(),
            "source_scan_no_structured_usc_target": (
                "1" if source_scan_no_structured_target or no_target_triage else "0"
            ),
            "reviewed_no_structured_usc_target_rows": str(len(reviewed_no_structured)),
            "triage_rows": str(len(triage_rows)),
            "triage_no_structured_target_rows": str(len(no_target_triage)),
            "triage_candidate_rows": str(len(candidate_triage)),
            "target_diff_review_rows": str(len(diff_rows)),
            "source_reviewed_target_section_diff_rows": str(len(source_reviewed)),
            "reviewed_no_exact_target_section_diff_rows": str(len(no_exact_target)),
            "unresolved_target_section_review_rows": str(len(unresolved)),
            "target_lifecycle_bridge_rows": str(len(bridge_rows)),
            "authority_exact_target_reference_rows": str(len(authority_exact)),
            "authority_base_section_rows": str(len(authority_base)),
            "court_exact_target_reference_rows": str(len(court_exact)),
            "court_base_section_rows": str(len(court_base)),
            "court_direct_review_status": action.get("court_direct_review_status", "").strip(),
            "closed_review_gates": action.get("closed_review_gates", "").strip(),
            "next_codified_lineage_action": next_action,
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
    status_counts = Counter(row["codified_progress_status"] for row in rows)
    source_reviewed_public_laws = [
        row for row in rows
        if parse_int(row["source_reviewed_target_section_diff_rows"]) > 0
    ]
    no_target_rows = [
        row for row in rows
        if row["codified_progress_status"] == "official_source_scan_no_structured_usc_target"
    ]
    reviewed_no_structured_rows = [
        row for row in rows
        if parse_int(row["reviewed_no_structured_usc_target_rows"]) > 0
    ]
    total_diff_rows = sum(parse_int(row["target_diff_review_rows"]) for row in rows)
    total_source_reviewed = sum(
        parse_int(row["source_reviewed_target_section_diff_rows"])
        for row in rows
    )
    total_no_exact_target = sum(
        parse_int(row["reviewed_no_exact_target_section_diff_rows"])
        for row in rows
    )
    total_unresolved = sum(
        parse_int(row["unresolved_target_section_review_rows"])
        for row in rows
    )
    lines = [
        "# Statutory Lineage Codified Progress",
        "",
        "This report classifies codified-lineage progress for the current lifecycle candidates. It separates source-reviewed target-section diff coverage from reviewed designation-law no-structured-U.S.C.-target dispositions and unresolved official public-law scans that expose no structured U.S.C. target. It is progress tracking, not full codified-lineage evidence.",
        "",
        f"- Codified-lineage progress rows: {len(rows)}",
        f"- Public laws with source-reviewed target-section diff rows: {len(source_reviewed_public_laws)}",
        f"- Target-section diff-review rows attached: {total_diff_rows}",
        f"- Source-reviewed target-section diff rows attached: {total_source_reviewed}",
        f"- Reviewed no-exact-target target-section rows: {total_no_exact_target}",
        f"- Reviewed no-structured-U.S.C.-target designation rows: {len(reviewed_no_structured_rows)}",
        f"- Reviewed but unresolved target-section rows: {total_unresolved}",
        f"- Unresolved official source scans with no structured U.S.C. target: {len(no_target_rows)}",
        "",
        "Codified progress statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Progress status | Source-reviewed diffs | No-exact-target | Reviewed no target | Unresolved | Source scan no target | Next codified-lineage action |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['progress_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | {row['codified_progress_status']} | "
            f"{row['source_reviewed_target_section_diff_rows']} | "
            f"{row['reviewed_no_exact_target_section_diff_rows']} | "
            f"{row['reviewed_no_structured_usc_target_rows']} | "
            f"{row['unresolved_target_section_review_rows']} | "
            f"{row['source_scan_no_structured_usc_target']} | "
            f"{row['next_codified_lineage_action']} |"
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
