#!/usr/bin/env python3
"""Write a public-law lifecycle readiness queue from the bill-law spine."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


SPINE_CSV = Path("reports/bill-law-evidence-spine.csv")
COURT_DIRECT_REVIEW_CSV = Path("reports/court-public-law-direct-review.csv")
OUT_CSV = Path("reports/bill-law-lifecycle-readiness.csv")
OUT_MD = Path("reports/bill-law-lifecycle-readiness.md")

DIRECT_LAYERS = [
    "bill_action_metadata",
    "law_revision_text_proxy",
    "federal_register_authority_text_verified",
    "federal_register_proposed_rule_history_match",
    "proposed_rule_shared_identifier_match",
    "proposed_rule_regulations_gov_comment_portal_metadata",
    "federal_register_exposed_regulations_gov_comment_metadata",
    "regulations_gov_complete_comment_record_metadata",
    "federal_register_final_effective_date_timing",
    "federal_register_proposed_to_final_timing",
    "official_lda_filing_text_bill_identifier",
]

CONTEXT_LAYERS = [
    "sponsor_district_public_opinion_metadata",
    "sponsor_district_bill_policy_area_context",
    "topic_throughput_policy_area",
    "campaign_finance_sponsor_policy_area_context",
    "lobbying_issue_bill_policy_area_context",
    "court_review_usc_section_authority_overlap",
    "scdb_law_minor_usc_section",
]

HIGH_PRIORITY_GATES = [
    ("bill_topic_public_opinion", "bill-topic public opinion"),
    (
        "bill_specific_campaign_finance_or_lobbying_to_bill",
        "bill-specific finance/lobbying linkage",
    ),
    ("codified_usc_lineage", "codified statutory lineage"),
    ("direct_case_to_public_law_identifier", "direct case-to-public-law identifier"),
    (
        "reviewed_case_disposition_to_public_law",
        "reviewed court disposition for the public law",
    ),
    ("complete_regulations_comments", "complete Regulations.gov comments"),
    ("unified_agenda_stage", "Unified Agenda stage"),
    (
        "implementation_outcomes_or_enforcement",
        "implementation outcome or enforcement evidence",
    ),
    ("full_bill_progression_census_overlap", "full bill-progression census overlap"),
]

TIER_LABELS = {
    "tier_1_rich_lifecycle_review_candidate": "rich lifecycle review candidate",
    "tier_2_implementation_chain_candidate": "implementation chain candidate",
    "tier_3_representation_influence_context_candidate": (
        "representation/influence context candidate"
    ),
    "tier_4_single_downstream_link_candidate": "single downstream-link candidate",
    "tier_5_bill_action_context_only": "bill/action context only",
}

FIELDNAMES = [
    "review_priority_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "lifecycle_readiness_tier",
    "review_score",
    "direct_evidence_count",
    "context_evidence_count",
    "high_priority_gap_count",
    "direct_evidence_layers",
    "context_evidence_layers",
    "high_priority_gaps",
    "next_upgrade_gate",
    "next_upgrade_reason",
    "next_source_family",
    "next_source_command",
    "district_ids",
    "campaign_finance_context_bill_ids",
    "lobbying_context_bill_ids",
    "authority_document_numbers",
    "proposed_rule_document_numbers",
    "regulations_docket_ids",
    "regulations_comment_urls",
    "comment_record_docket_ids",
    "court_case_ids",
    "court_usc_sections",
    "court_direct_review_disposition_rows",
    "court_direct_review_direct_rows",
    "court_direct_review_not_direct_rows",
    "court_direct_review_temporally_excluded_rows",
    "court_direct_review_missing_date_rows",
    "court_direct_review_open_rows",
    "court_direct_review_determinations",
    "review_packet",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Readiness queue only; direct-evidence counts identify source-backed "
    "bill/action, revision-text, authority, proposed-history, comment, and "
    "timing metadata in the current spine, while context counts remain policy-area, "
    "district, finance, lobbying, or court-overlap context. This report does "
    "not add bill-topic public support, bill-specific finance/lobbying "
    "influence, complete implementation outcomes, direct court disposition, "
    "codified statutory lineage, causal effects, welfare, or model validation."
)

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
        "make build-court-law-linkage-raw",
    ),
    "reviewed_case_disposition_to_public_law": (
        "Court review and invalidation",
        "make build-court-law-linkage-raw",
    ),
    "complete_regulations_comments": (
        "Rulemaking implementation and enforcement",
        "make build-rulemaking-comment-records-raw && make rulemaking-comment-records",
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

POINTER_FIELDS = [
    ("district_ids", "district_ids"),
    (
        "campaign_finance_context_bill_ids",
        "campaign_finance_sponsor_policy_context_bill_ids",
    ),
    ("lobbying_context_bill_ids", "lobbying_policy_context_bill_ids"),
    ("authority_document_numbers", "implementation_authority_document_numbers"),
    (
        "proposed_rule_document_numbers",
        "implementation_history_proposed_document_numbers",
    ),
    (
        "regulations_docket_ids",
        "implementation_history_proposed_regulations_docket_ids",
    ),
    (
        "regulations_comment_urls",
        "implementation_history_proposed_regulations_comment_urls",
    ),
    ("comment_record_docket_ids", "implementation_comment_record_docket_ids"),
    ("court_case_ids", "court_review_case_ids"),
    ("court_usc_sections", "court_review_usc_sections"),
]


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


def int_field(row: dict[str, str], field: str) -> int:
    try:
        return int(row.get(field, "0") or "0")
    except ValueError:
        return 0


def by_public_law(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            result.setdefault(public_law, []).append(row)
    return result


def present_layers(row: dict[str, str]) -> set[str]:
    return set(split_values(row.get("evidence_layers", "")))


def missing_links(row: dict[str, str]) -> set[str]:
    return set(split_values(row.get("missing_links", "")))


def has_any(layers: set[str], candidates: set[str]) -> bool:
    return bool(layers & candidates)


def classify(layers: set[str]) -> str:
    has_authority = "federal_register_authority_text_verified" in layers
    has_history = has_any(
        layers,
        {
            "federal_register_proposed_rule_history_match",
            "proposed_rule_shared_identifier_match",
        },
    )
    has_timing = has_any(
        layers,
        {
            "federal_register_final_effective_date_timing",
            "federal_register_proposed_to_final_timing",
        },
    )
    has_court_overlap = "court_review_usc_section_authority_overlap" in layers
    has_public_context = has_any(
        layers,
        {
            "sponsor_district_public_opinion_metadata",
            "sponsor_district_bill_policy_area_context",
        },
    )
    has_influence_context = has_any(
        layers,
        {
            "campaign_finance_sponsor_policy_area_context",
            "lobbying_issue_bill_policy_area_context",
        },
    )
    if has_authority and has_history and has_timing and has_court_overlap:
        return "tier_1_rich_lifecycle_review_candidate"
    if has_authority and (has_history or has_timing):
        return "tier_2_implementation_chain_candidate"
    if has_public_context and has_influence_context:
        return "tier_3_representation_influence_context_candidate"
    if has_authority or has_court_overlap:
        return "tier_4_single_downstream_link_candidate"
    return "tier_5_bill_action_context_only"


def score(layers: set[str], high_priority_gaps: list[str]) -> int:
    direct = sum(1 for layer in DIRECT_LAYERS if layer in layers)
    context = sum(1 for layer in CONTEXT_LAYERS if layer in layers)
    value = direct * 3 + context * 2 - len(high_priority_gaps)
    if "federal_register_authority_text_verified" in layers:
        value += 3
    if "federal_register_proposed_rule_history_match" in layers:
        value += 2
    if "court_review_usc_section_authority_overlap" in layers:
        value += 2
    if "sponsor_district_public_opinion_metadata" in layers:
        value += 1
    if "campaign_finance_sponsor_policy_area_context" in layers:
        value += 1
    if "lobbying_issue_bill_policy_area_context" in layers:
        value += 1
    return value


def direct_review_summary(direct_rows: list[dict[str, str]]) -> dict[str, str]:
    determinations = [
        row.get("direct_review_determination", "").strip()
        for row in direct_rows
        if row.get("direct_review_determination", "").strip()
    ]
    direct_count = sum(
        1 for row in direct_rows
        if row.get("direct_case_to_public_law_identifier", "").strip() == "1"
    )
    not_direct_count = sum(
        1 for row in direct_rows
        if row.get("direct_review_determination", "").strip()
        == "reviewed_not_direct_public_law_review"
    )
    temporal_count = sum(
        1 for row in direct_rows
        if row.get("direct_review_determination", "").strip()
        == "temporally_excluded_before_public_law_enactment"
    )
    missing_date_count = sum(
        1 for row in direct_rows
        if row.get("direct_review_determination", "").strip()
        == "missing_date_source_review_needed"
    )
    reviewed_count = sum(
        1 for row in direct_rows
        if row.get("direct_review_determination", "").strip().startswith("reviewed_")
    )
    open_count = missing_date_count
    if not direct_rows:
        open_count = 0
    elif direct_count == 0 and reviewed_count == 0 and temporal_count == 0:
        open_count = len(direct_rows)
    return {
        "court_direct_review_disposition_rows": str(len(direct_rows)),
        "court_direct_review_direct_rows": str(direct_count),
        "court_direct_review_not_direct_rows": str(not_direct_count),
        "court_direct_review_temporally_excluded_rows": str(temporal_count),
        "court_direct_review_missing_date_rows": str(missing_date_count),
        "court_direct_review_open_rows": str(open_count),
        "court_direct_review_determinations": "; ".join(sorted(set(determinations))),
    }


def has_open_direct_review_lead(summary: dict[str, str]) -> bool:
    if int_field(summary, "court_direct_review_open_rows") > 0:
        return True
    return int_field(summary, "court_direct_review_disposition_rows") == 0


def next_upgrade_gate(
    layers: set[str],
    gaps: set[str],
    court_direct_summary: dict[str, str],
) -> tuple[str, str]:
    has_authority = "federal_register_authority_text_verified" in layers
    has_court_overlap = "court_review_usc_section_authority_overlap" in layers
    has_comment_portal = has_any(
        layers,
        {
            "proposed_rule_regulations_gov_comment_portal_metadata",
            "federal_register_exposed_regulations_gov_comment_metadata",
        },
    )
    has_public_context = has_any(
        layers,
        {
            "sponsor_district_public_opinion_metadata",
            "sponsor_district_bill_policy_area_context",
        },
    )
    has_influence_context = has_any(
        layers,
        {
            "campaign_finance_sponsor_policy_area_context",
            "lobbying_issue_bill_policy_area_context",
        },
    )
    ordered: list[tuple[str, str]] = []
    if has_court_overlap and has_open_direct_review_lead(court_direct_summary):
        ordered.extend([
            (
                "direct_case_to_public_law_identifier",
                "court overlap exists, so the next review should test direct case/statute identity",
            ),
            (
                "reviewed_case_disposition_to_public_law",
                "court overlap exists, so disposition review is the next stronger court gate",
            ),
        ])
    if has_authority:
        reason = "authority text exists, so statutory-lineage review can test codified targets"
        if has_court_overlap and not has_open_direct_review_lead(court_direct_summary):
            reason = (
                "current court-overlap leads already have direct-review dispositions, "
                "so codified statutory-lineage review is the next stronger gate"
            )
        ordered.append((
            "codified_usc_lineage",
            reason,
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
        if gate in gaps:
            return gate, reason
    if gaps:
        fallback = sorted(gaps)[0]
        return fallback, "remaining gap from the current bill-law spine"
    return "none", "no high-priority gap recorded in the current spine row"


def pointer_value(row: dict[str, str], source_field: str) -> str:
    return "; ".join(split_values(row.get(source_field, "")))


def review_packet(
    row: dict[str, str],
    gate: str,
    court_direct_summary: dict[str, str],
) -> str:
    pointers = {name: pointer_value(row, source) for name, source in POINTER_FIELDS}
    parts = [
        f"bill_id={row.get('bill_id', '')}",
        f"public_law={row.get('public_law_number', '')}",
        f"policy_area={row.get('policy_area', '')}",
        f"next_gate={gate}",
    ]
    if gate in {"direct_case_to_public_law_identifier", "reviewed_case_disposition_to_public_law"}:
        parts.extend([
            f"court_cases={pointers['court_case_ids']}",
            f"court_usc_sections={pointers['court_usc_sections']}",
            f"authority_docs={pointers['authority_document_numbers']}",
            f"direct_review_determinations={court_direct_summary['court_direct_review_determinations']}",
            f"direct_review_open_rows={court_direct_summary['court_direct_review_open_rows']}",
        ])
    elif gate == "codified_usc_lineage":
        parts.extend([
            f"authority_usc_sections={row.get('implementation_authority_usc_citations', '')}",
            f"authority_docs={pointers['authority_document_numbers']}",
            f"proposed_docs={pointers['proposed_rule_document_numbers']}",
        ])
    elif gate == "complete_regulations_comments":
        parts.extend([
            f"regulations_dockets={pointers['regulations_docket_ids']}",
            f"comment_record_dockets={pointers['comment_record_docket_ids']}",
            f"comment_urls={pointers['regulations_comment_urls']}",
            f"proposed_docs={pointers['proposed_rule_document_numbers']}",
        ])
    elif gate == "bill_specific_campaign_finance_or_lobbying_to_bill":
        parts.extend([
            f"campaign_context_bills={pointers['campaign_finance_context_bill_ids']}",
            f"lobbying_context_bills={pointers['lobbying_context_bill_ids']}",
        ])
    elif gate == "bill_topic_public_opinion":
        parts.append(f"district_ids={pointers['district_ids']}")
    return " | ".join(part for part in parts if part and not part.endswith("="))


def build_rows(
    spine_rows: list[dict[str, str]],
    direct_review_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    direct_review_by_pl = by_public_law(direct_review_rows)
    rows: list[dict[str, str]] = []
    for row in spine_rows:
        layers = present_layers(row)
        gaps = missing_links(row)
        public_law = row.get("public_law_number", "").strip()
        court_direct_summary = direct_review_summary(direct_review_by_pl.get(public_law, []))
        direct_layers = [layer for layer in DIRECT_LAYERS if layer in layers]
        context_layers = [layer for layer in CONTEXT_LAYERS if layer in layers]
        high_priority_gaps = [gate for gate, _ in HIGH_PRIORITY_GATES if gate in gaps]
        gate, reason = next_upgrade_gate(layers, gaps, court_direct_summary)
        source_family, source_command = NEXT_SOURCE_MAP.get(gate, ("not specified", "not specified"))
        pointer_columns = {
            output: pointer_value(row, source)
            for output, source in POINTER_FIELDS
        }
        rows.append({
            "review_priority_rank": "0",
            "bill_id": row.get("bill_id", ""),
            "public_law_number": row.get("public_law_number", ""),
            "policy_area": row.get("policy_area", ""),
            "lifecycle_readiness_tier": classify(layers),
            "review_score": str(score(layers, high_priority_gaps)),
            "direct_evidence_count": str(len(direct_layers)),
            "context_evidence_count": str(len(context_layers)),
            "high_priority_gap_count": str(len(high_priority_gaps)),
            "direct_evidence_layers": "; ".join(direct_layers),
            "context_evidence_layers": "; ".join(context_layers),
            "high_priority_gaps": "; ".join(high_priority_gaps),
            "next_upgrade_gate": gate,
            "next_upgrade_reason": reason,
            "next_source_family": source_family,
            "next_source_command": source_command,
            **pointer_columns,
            **court_direct_summary,
            "review_packet": review_packet(row, gate, court_direct_summary),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    rows.sort(
        key=lambda item: (
            -int(item["review_score"]),
            -int(item["direct_evidence_count"]),
            -int(item["context_evidence_count"]),
            item["bill_id"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["review_priority_rank"] = str(index)
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    tiers = Counter(row["lifecycle_readiness_tier"] for row in rows)
    gates = Counter(row["next_upgrade_gate"] for row in rows)
    source_families = Counter(row["next_source_family"] for row in rows)
    court_disposition_rows = sum(int_field(row, "court_direct_review_disposition_rows") for row in rows)
    court_direct_rows = sum(int_field(row, "court_direct_review_direct_rows") for row in rows)
    court_not_direct_rows = sum(int_field(row, "court_direct_review_not_direct_rows") for row in rows)
    court_temporal_rows = sum(
        int_field(row, "court_direct_review_temporally_excluded_rows")
        for row in rows
    )
    court_open_rows = sum(int_field(row, "court_direct_review_open_rows") for row in rows)
    lines = [
        "# Bill-Law Lifecycle Readiness",
        "",
        "This report ranks rows from `reports/bill-law-evidence-spine.csv` for the next public-law lifecycle evidence upgrades. It is a work queue, not validation evidence.",
        "",
        f"- Public-law rows ranked: {len(rows)}",
        f"- Rich lifecycle review candidates: {tiers['tier_1_rich_lifecycle_review_candidate']}",
        f"- Implementation-chain candidates: {tiers['tier_2_implementation_chain_candidate']}",
        f"- Representation/influence context candidates: {tiers['tier_3_representation_influence_context_candidate']}",
        f"- Single downstream-link candidates: {tiers['tier_4_single_downstream_link_candidate']}",
        f"- Bill/action-context-only rows: {tiers['tier_5_bill_action_context_only']}",
        f"- Court direct-review disposition row attachments: {court_disposition_rows}",
        f"- Court direct-review direct rows: {court_direct_rows}",
        f"- Court direct-review reviewed not-direct rows: {court_not_direct_rows}",
        f"- Court direct-review temporally excluded rows: {court_temporal_rows}",
        f"- Court direct-review open rows: {court_open_rows}",
        "",
        "Next upgrade gate counts:",
    ]
    for gate, count in sorted(gates.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {gate}: {count}")
    lines.extend([
        "",
        "Next source family counts:",
    ])
    for family, count in sorted(source_families.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {family}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Tier | Direct | Context | Gaps | Next upgrade gate | Source family |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        tier = TIER_LABELS.get(row["lifecycle_readiness_tier"], row["lifecycle_readiness_tier"])
        lines.append(
            f"| {row['review_priority_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | {tier} | "
            f"{row['direct_evidence_count']} | {row['context_evidence_count']} | "
            f"{row['high_priority_gap_count']} | {row['next_upgrade_gate']} | "
            f"{row['next_source_family']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    spine_rows = read_csv(SPINE_CSV)
    if not spine_rows:
        raise SystemExit(f"{SPINE_CSV} is missing or empty; run make bill-law-evidence-spine first.")
    rows = build_rows(spine_rows, read_csv(COURT_DIRECT_REVIEW_CSV))
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
