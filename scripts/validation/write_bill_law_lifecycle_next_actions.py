#!/usr/bin/env python3
"""Write a lifecycle next-action queue after court direct-review dispositions."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LIFECYCLE = Path("reports/bill-law-lifecycle-readiness.csv")
DIRECT_REVIEW = Path("reports/court-public-law-direct-review.csv")
OUT_CSV = Path("reports/bill-law-lifecycle-next-actions.csv")
OUT_MD = Path("reports/bill-law-lifecycle-next-actions.md")

DIRECT_REVIEW_GATES = {
    "direct_case_to_public_law_identifier",
    "reviewed_case_disposition_to_public_law",
}

NEXT_SOURCE_MAP = {
    "bill_topic_public_opinion": (
        "District public opinion and affected groups",
        "make build-district-public-opinion-policy-context-raw",
    ),
    "bill_specific_campaign_finance_or_lobbying_to_bill": (
        "OpenFEC campaign finance; Senate LDA lobbying disclosures",
        "make build-lobbying-bill-mentions-raw && make lobbying-bill-mention-review",
    ),
    "codified_usc_lineage": (
        "Statutory revision and law lineage",
        "make build-law-revision-bill-linkage-raw",
    ),
    "direct_case_to_public_law_identifier": (
        "Court review and invalidation",
        "make court-public-law-direct-review",
    ),
    "reviewed_case_disposition_to_public_law": (
        "Court review and invalidation",
        "make court-public-law-direct-review",
    ),
    "complete_regulations_comments": (
        "Rulemaking implementation and enforcement",
        "make build-rulemaking-comment-metadata-raw",
    ),
    "unified_agenda_stage": (
        "Rulemaking implementation and enforcement",
        "make build-rulemaking-history-linkage-raw",
    ),
    "implementation_outcomes_or_enforcement": (
        "Rulemaking implementation and enforcement",
        "make build-rulemaking-implementation-linkage-raw",
    ),
    "full_bill_progression_census_overlap": (
        "Congress.gov bill histories; govinfo bill and action records",
        "make build-govinfo-billstatus-linkage-raw",
    ),
    "none": ("none", "none"),
}

FIELDNAMES = [
    "action_rank",
    "base_review_priority_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "lifecycle_readiness_tier",
    "review_score",
    "high_priority_gaps",
    "closed_review_gates",
    "closed_review_gate_count",
    "actionable_high_priority_gaps",
    "actionable_gap_count",
    "court_direct_review_status",
    "court_direct_review_rows",
    "court_direct_review_direct_rows",
    "court_direct_review_not_direct_rows",
    "court_direct_review_temporal_exclusions",
    "next_actionable_upgrade_gate",
    "next_actionable_upgrade_reason",
    "next_source_family",
    "next_source_command",
    "action_packet",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Post-direct-review lifecycle action queue only; closed gates reflect "
    "temporal exclusions or source-reviewed not-direct dispositions for queued "
    "court/public-law overlaps. This report does not create bill-topic public "
    "support, bill-specific finance/lobbying influence, direct court-review "
    "evidence beyond the reviewed disposition, implementation outcomes, "
    "codified statutory lineage, causal effects, welfare, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def grouped_direct_review(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            grouped[bill_id].append(row)
    return grouped


def direct_review_status(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "no_queued_court_public_law_overlap"
    determinations = {row.get("direct_review_determination", "") for row in rows}
    if "missing_date_source_review_needed" in determinations:
        return "court_public_law_source_review_needed"
    if any(
        row.get("direct_review_determination") == "reviewed_direct_public_law_review"
        or row.get("direct_case_to_public_law_identifier") == "1"
        or row.get("reviewed_case_disposition_to_public_law") == "1"
        for row in rows
    ):
        return "direct_public_law_review_found"
    closed_without_direct = {
        "temporally_excluded_before_public_law_enactment",
        "reviewed_not_direct_public_law_review",
    }
    if determinations <= closed_without_direct:
        return "all_queued_court_overlaps_closed_without_direct_public_law_review"
    return "mixed_court_public_law_review_status"


def closed_review_gates(
    lifecycle_row: dict[str, str],
    direct_rows: list[dict[str, str]],
    status: str,
) -> list[str]:
    base_gaps = set(split_values(lifecycle_row.get("high_priority_gaps", "")))
    closed: set[str] = set()
    if status == "all_queued_court_overlaps_closed_without_direct_public_law_review":
        closed |= DIRECT_REVIEW_GATES & base_gaps
    elif status == "direct_public_law_review_found":
        if any(row.get("direct_case_to_public_law_identifier") == "1" for row in direct_rows):
            closed.add("direct_case_to_public_law_identifier")
        if any(row.get("reviewed_case_disposition_to_public_law") == "1" for row in direct_rows):
            closed.add("reviewed_case_disposition_to_public_law")
        closed &= base_gaps
    return sorted(closed)


def next_actionable_gate(row: dict[str, str], actionable_gaps: set[str]) -> tuple[str, str]:
    direct_layers = set(split_values(row.get("direct_evidence_layers", "")))
    context_layers = set(split_values(row.get("context_evidence_layers", "")))
    has_court_overlap = "court_review_usc_section_authority_overlap" in context_layers
    has_authority = "federal_register_authority_text_verified" in direct_layers
    has_comment_portal = bool(
        {
            "proposed_rule_regulations_gov_comment_portal_metadata",
            "federal_register_exposed_regulations_gov_comment_metadata",
        }
        & direct_layers
    )
    has_influence_context = bool(
        {
            "campaign_finance_sponsor_policy_area_context",
            "lobbying_issue_bill_policy_area_context",
        }
        & context_layers
    )
    has_public_context = bool(
        {
            "sponsor_district_public_opinion_metadata",
            "sponsor_district_bill_policy_area_context",
        }
        & context_layers
    )
    ordered: list[tuple[str, str]] = []
    if has_court_overlap:
        ordered.extend([
            (
                "direct_case_to_public_law_identifier",
                "court overlap exists and direct-review disposition remains actionable",
            ),
            (
                "reviewed_case_disposition_to_public_law",
                "court overlap exists and disposition review remains actionable",
            ),
        ])
    if has_authority:
        ordered.append((
            "codified_usc_lineage",
            "court direct-review tasks are closed or lower priority; authority text makes codified statutory lineage the next actionable gate",
        ))
    if has_comment_portal:
        ordered.append((
            "complete_regulations_comments",
            "comment-portal metadata exists, so complete comment retrieval is the next rulemaking gate",
        ))
    if has_influence_context:
        ordered.append((
            "bill_specific_campaign_finance_or_lobbying_to_bill",
            "same-policy finance or lobbying context exists, so the next gate is a bill-specific link",
        ))
    if has_public_context:
        ordered.append((
            "bill_topic_public_opinion",
            "sponsor-district context exists, so the next gate is bill-topic support or affected-group evidence",
        ))
    ordered.append((
        "full_bill_progression_census_overlap",
        "fuller bill/action coverage is required before stronger bill-flow claims",
    ))
    for gate, reason in ordered:
        if gate in actionable_gaps:
            return gate, reason
    if actionable_gaps:
        fallback = sorted(actionable_gaps)[0]
        return fallback, "remaining actionable gap after direct-review dispositions"
    return "none", "no actionable high-priority gap remains after direct-review dispositions"


def build_rows() -> list[dict[str, str]]:
    lifecycle_rows = read_csv(LIFECYCLE)
    direct_review_rows = read_csv(DIRECT_REVIEW)
    if not lifecycle_rows:
        raise SystemExit(f"{LIFECYCLE} is missing or empty; run make bill-law-lifecycle-readiness first.")
    if not direct_review_rows:
        raise SystemExit(f"{DIRECT_REVIEW} is missing or empty; run make court-public-law-direct-review first.")

    direct_by_bill = grouped_direct_review(direct_review_rows)
    rows: list[dict[str, str]] = []
    for lifecycle_row in lifecycle_rows:
        bill_id = lifecycle_row.get("bill_id", "").strip()
        direct_rows = direct_by_bill.get(bill_id, [])
        status = direct_review_status(direct_rows)
        closed = closed_review_gates(lifecycle_row, direct_rows, status)
        base_gaps = set(split_values(lifecycle_row.get("high_priority_gaps", "")))
        actionable = sorted(base_gaps - set(closed))
        next_gate, next_reason = next_actionable_gate(lifecycle_row, set(actionable))
        source_family, source_command = NEXT_SOURCE_MAP.get(next_gate, ("not specified", "not specified"))
        direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "reviewed_direct_public_law_review"
        )
        not_direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "reviewed_not_direct_public_law_review"
        )
        temporal_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "temporally_excluded_before_public_law_enactment"
        )
        action_packet = " | ".join([
            f"bill_id={bill_id}",
            f"public_law={lifecycle_row.get('public_law_number', '').strip()}",
            f"base_rank={lifecycle_row.get('review_priority_rank', '').strip()}",
            f"closed_review_gates={'; '.join(closed) if closed else 'none'}",
            f"next_actionable_gate={next_gate}",
        ])
        rows.append({
            "action_rank": "0",
            "base_review_priority_rank": lifecycle_row.get("review_priority_rank", ""),
            "bill_id": bill_id,
            "public_law_number": lifecycle_row.get("public_law_number", ""),
            "policy_area": lifecycle_row.get("policy_area", ""),
            "lifecycle_readiness_tier": lifecycle_row.get("lifecycle_readiness_tier", ""),
            "review_score": lifecycle_row.get("review_score", ""),
            "high_priority_gaps": lifecycle_row.get("high_priority_gaps", ""),
            "closed_review_gates": "; ".join(closed),
            "closed_review_gate_count": str(len(closed)),
            "actionable_high_priority_gaps": "; ".join(actionable),
            "actionable_gap_count": str(len(actionable)),
            "court_direct_review_status": status,
            "court_direct_review_rows": str(len(direct_rows)),
            "court_direct_review_direct_rows": str(direct_count),
            "court_direct_review_not_direct_rows": str(not_direct_count),
            "court_direct_review_temporal_exclusions": str(temporal_count),
            "next_actionable_upgrade_gate": next_gate,
            "next_actionable_upgrade_reason": next_reason,
            "next_source_family": source_family,
            "next_source_command": source_command,
            "action_packet": action_packet,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    rows.sort(
        key=lambda row: (
            -int(row["review_score"]),
            -int(row["closed_review_gate_count"]),
            int(row["actionable_gap_count"]),
            int(row["base_review_priority_rank"] or "999999"),
            row["bill_id"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["action_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["court_direct_review_status"] for row in rows)
    gates = Counter(row["next_actionable_upgrade_gate"] for row in rows)
    closed_gates = sum(int(row["closed_review_gate_count"]) for row in rows)
    lines = [
        "# Bill-Law Lifecycle Next Actions",
        "",
        "This report refines the lifecycle readiness queue after court/public-law direct-review dispositions. It is an action queue, not validation evidence.",
        "",
        f"- Public-law rows ranked: {len(rows)}",
        f"- Closed direct-review gates: {closed_gates}",
        "- Rows with all queued court overlaps closed without direct public-law review: "
        f"{statuses['all_queued_court_overlaps_closed_without_direct_public_law_review']}",
        "- Rows with direct public-law review found: "
        f"{statuses['direct_public_law_review_found']}",
        "- Rows still needing court/public-law source review: "
        f"{statuses['court_public_law_source_review_needed']}",
        "",
        "Actionable next upgrade gate counts:",
    ]
    for gate, count in sorted(gates.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {gate}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Action rank | Bill | Public law | Court review status | Closed gates | Actionable gaps | Next actionable gate | Source family |",
        "| ---: | --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['action_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['court_direct_review_status']}` | "
            f"{row['closed_review_gates'] or '---'} | {row['actionable_gap_count']} | "
            f"{row['next_actionable_upgrade_gate']} | {row['next_source_family']} |"
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
