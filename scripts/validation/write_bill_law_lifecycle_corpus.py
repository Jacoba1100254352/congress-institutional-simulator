#!/usr/bin/env python3
"""Assemble a bounded public-law lifecycle corpus from generated review layers."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


BILL_LAW_SPINE = Path("reports/bill-law-evidence-spine.csv")
NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
COURT_PUBLIC_LAW_DIRECT_REVIEW = Path("reports/court-public-law-direct-review.csv")
DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW = Path(
    "reports/district-public-opinion-survey-item-proxy-review.csv"
)
DISTRICT_PUBLIC_OPINION_BILL_TOPIC_SUPPORT = Path(
    "reports/district-public-opinion-bill-topic-support.csv"
)
BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW = Path(
    "reports/bill-finance-lobbying-local-context-review.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW = Path(
    "reports/bill-finance-lobbying-external-search-review.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW = Path(
    "reports/bill-finance-lobbying-external-lda-mention-review.csv"
)
BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW = Path(
    "reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv"
)
STATUTORY_LINEAGE_CODIFIED_PROGRESS = Path("reports/statutory-lineage-codified-progress.csv")
STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE = Path(
    "reports/statutory-lineage-target-lifecycle-bridge.csv"
)
RULEMAKING_COMMENT_TEXT_REVIEW = Path("reports/rulemaking-comment-text-review.csv")
OUT_CSV = Path("reports/bill-law-lifecycle-corpus.csv")
OUT_MD = Path("reports/bill-law-lifecycle-corpus.md")

CLAIM_BOUNDARY = (
    "Public-law lifecycle corpus only; rows compile generated source-review, "
    "metadata, proxy, and action-queue statuses from existing reports. The corpus "
    "does not convert historical related-issue support into exact or contemporaneous "
    "bill-topic public support, affected-group harm, bill-specific "
    "campaign-finance or lobbying influence, implementation outcomes, complete "
    "statutory lineage, direct court-review evidence beyond source-reviewed "
    "dispositions, causal effects, welfare evidence, or model validation."
)

FIELDNAMES = [
    "corpus_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "lifecycle_readiness_tier",
    "review_score",
    "corpus_packet_status",
    "publication_readiness_status",
    "next_actionable_upgrade_gate",
    "actionable_high_priority_gaps",
    "actionable_gap_count",
    "closed_review_gates",
    "closed_review_gate_count",
    "bill_history_context_status",
    "sponsor_context_status",
    "district_public_opinion_status",
    "public_opinion_proxy_review_status",
    "bill_topic_item_review_status",
    "district_estimation_status",
    "historical_related_issue_support_estimate_rows",
    "historical_related_issue_support_years",
    "historical_related_issue_support_items",
    "historical_weighted_support_min",
    "historical_weighted_support_max",
    "exact_bill_support_status",
    "affected_group_item_status",
    "finance_lobbying_review_status",
    "local_finance_lobbying_status",
    "external_lda_search_status",
    "external_lda_mention_review_packets",
    "campaign_finance_target_scope_status",
    "statutory_lineage_status",
    "target_diff_review_rows",
    "source_reviewed_target_section_diff_rows",
    "reviewed_no_target_rows",
    "target_lifecycle_bridge_rows",
    "rulemaking_implementation_status",
    "authority_rule_rows",
    "authority_text_verified_rows",
    "comment_record_docket_rows",
    "complete_comment_record_docket_rows",
    "comment_text_review_rows",
    "comment_text_available_rows",
    "comment_detail_statuses",
    "court_review_status",
    "court_direct_review_rows",
    "court_direct_review_direct_rows",
    "court_direct_review_not_direct_rows",
    "court_direct_review_temporal_exclusions",
    "court_direct_review_source_summary_rows",
    "source_reviewed_subgate_count",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require_rows(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    if not rows:
        raise SystemExit(f"{path} is missing or empty; run the lifecycle validation targets first.")
    return rows


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


def compact_status(value: str, fallback: str) -> str:
    return value.strip() if value and value.strip() else fallback


def source_artifact(path: Path) -> str:
    return str(path)


def finance_status(
    spine: dict[str, str],
    local: dict[str, str],
    external: dict[str, str],
    mention_packets: list[dict[str, str]],
    target_scope: dict[str, str],
) -> str:
    if target_scope:
        return compact_status(
            target_scope.get("target_scope_disposition", ""),
            "campaign_finance_target_scope_review_present",
        )
    if mention_packets:
        return "external_lda_mention_packets_reviewed_no_influence_evidence"
    if external:
        return compact_status(
            external.get("combined_external_review_status", ""),
            "external_bill_finance_lobbying_search_review_present",
        )
    if local:
        return compact_status(
            local.get("manual_bill_specific_gate_status", ""),
            "local_bill_finance_lobbying_review_present",
        )
    if (
        int_field(spine, "lobbying_bill_mention_rows") > 0
        or int_field(spine, "campaign_finance_sponsor_policy_context_rows") > 0
        or int_field(spine, "lobbying_policy_context_issue_rows") > 0
    ):
        return "bounded_same_policy_or_bill_identifier_context_only"
    return "no_bill_finance_lobbying_packet"


def implementation_status(
    spine: dict[str, str],
    comment_text_rows: list[dict[str, str]],
) -> str:
    text_available = sum(
        1 for row in comment_text_rows
        if row.get("comment_text_available", "").strip().lower() == "yes"
    )
    complete_records = int_field(spine, "implementation_comment_record_complete_docket_rows")
    partial_records = int_field(spine, "implementation_comment_record_partial_or_blocked_docket_rows")
    metadata_rows = int_field(spine, "implementation_comment_metadata_rows")
    authority_rows = int_field(spine, "implementation_authority_text_verified_rows")
    if text_available:
        return "sanitized_comment_detail_text_hashes_present"
    if comment_text_rows:
        return "sanitized_comment_detail_review_present_no_text_available"
    if complete_records:
        return "bounded_complete_comment_record_metadata_present_no_comment_text"
    if partial_records:
        return "partial_or_blocked_comment_record_metadata_present"
    if metadata_rows:
        return "federal_register_comment_metadata_present_no_record_text"
    if authority_rows:
        return "federal_register_authority_context_only"
    return "no_rulemaking_implementation_packet"


def publication_status(actionable_gap_count: int, source_reviewed_subgate_count: int) -> str:
    if actionable_gap_count == 0:
        return "candidate_for_claim_ledger_review"
    if source_reviewed_subgate_count:
        return "not_publication_claim_ready_source_reviewed_subgates_present"
    return "not_publication_claim_ready_metadata_or_proxy_only"


def packet_status(actionable_gap_count: int, source_reviewed_subgate_count: int) -> str:
    if actionable_gap_count == 0:
        return "lifecycle_packet_no_high_priority_actionable_gap"
    if source_reviewed_subgate_count >= 3:
        return "bounded_cross_source_packet_with_reviewed_subgates"
    if source_reviewed_subgate_count:
        return "bounded_packet_with_source_reviewed_subgate"
    return "bounded_packet_with_metadata_or_proxy_context_only"


def build_rows() -> list[dict[str, str]]:
    spine_rows = require_rows(BILL_LAW_SPINE)
    action_rows = require_rows(NEXT_ACTIONS)
    direct_review_rows = require_rows(COURT_PUBLIC_LAW_DIRECT_REVIEW)
    survey_rows = require_rows(DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW)
    historical_support_rows = require_rows(DISTRICT_PUBLIC_OPINION_BILL_TOPIC_SUPPORT)
    local_finance_rows = require_rows(BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW)
    external_search_rows = require_rows(BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW)
    mention_packet_rows = require_rows(BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW)
    target_scope_rows = require_rows(BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW)
    codified_rows = require_rows(STATUTORY_LINEAGE_CODIFIED_PROGRESS)
    target_bridge_rows = require_rows(STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE)
    comment_text_rows = require_rows(RULEMAKING_COMMENT_TEXT_REVIEW)

    spine_by_bill = by_bill(spine_rows)
    survey_by_bill = by_bill(survey_rows)
    historical_support_by_bill = group_by_bill(historical_support_rows)
    local_by_bill = by_bill(local_finance_rows)
    external_by_bill = by_bill(external_search_rows)
    target_scope_by_bill = by_bill(target_scope_rows)
    codified_by_bill = by_bill(codified_rows)
    direct_by_bill = group_by_bill(direct_review_rows)
    mentions_by_bill = group_by_bill(mention_packet_rows)
    target_bridge_by_bill = group_by_bill(target_bridge_rows)
    comment_text_by_bill = group_by_bill(comment_text_rows)

    rows: list[dict[str, str]] = []
    for action in sorted(action_rows, key=lambda row: int_field(row, "action_rank")):
        bill_id = action.get("bill_id", "").strip()
        spine = spine_by_bill.get(bill_id, {})
        survey = survey_by_bill.get(bill_id, {})
        historical_support = historical_support_by_bill.get(bill_id, [])
        local = local_by_bill.get(bill_id, {})
        external = external_by_bill.get(bill_id, {})
        mention_packets = mentions_by_bill.get(bill_id, [])
        target_scope = target_scope_by_bill.get(bill_id, {})
        codified = codified_by_bill.get(bill_id, {})
        direct_rows = direct_by_bill.get(bill_id, [])
        bridge_rows = target_bridge_by_bill.get(bill_id, [])
        text_rows = comment_text_by_bill.get(bill_id, [])

        source_reviewed_target_rows = int_field(
            codified,
            "source_reviewed_target_section_diff_rows",
        )
        reviewed_no_target_rows = int_field(
            codified,
            "reviewed_no_structured_usc_target_rows",
        )
        closed_gate_count = int_field(action, "closed_review_gate_count")
        source_reviewed_subgate_count = 0
        if source_reviewed_target_rows or reviewed_no_target_rows:
            source_reviewed_subgate_count += 1
        if closed_gate_count:
            source_reviewed_subgate_count += 1
        if local:
            source_reviewed_subgate_count += 1
        if external:
            source_reviewed_subgate_count += 1
        if mention_packets:
            source_reviewed_subgate_count += 1
        if target_scope:
            source_reviewed_subgate_count += 1
        if survey:
            source_reviewed_subgate_count += 1
        if historical_support:
            source_reviewed_subgate_count += 1
        if text_rows:
            source_reviewed_subgate_count += 1

        actionable_gap_count = int_field(action, "actionable_gap_count")
        text_available = sum(
            1 for row in text_rows
            if row.get("comment_text_available", "").strip().lower() == "yes"
        )
        direct_source_summary_rows = sum(
            1 for row in direct_rows
            if row.get("case_source_summary", "").strip()
            or row.get("public_law_source_summary", "").strip()
        )

        evidence_layers = ["bill_law_lifecycle_corpus"]
        missing_links = split_values(action.get("actionable_high_priority_gaps", ""))
        artifacts = [
            source_artifact(BILL_LAW_SPINE),
            source_artifact(NEXT_ACTIONS),
        ]
        for row in [spine, action, survey, local, external, target_scope, codified]:
            evidence_layers.extend(split_values(row.get("evidence_layers", "")))
            missing_links.extend(split_values(row.get("missing_links", "")))
        for grouped_rows, path in [
            (direct_rows, COURT_PUBLIC_LAW_DIRECT_REVIEW),
            ([survey] if survey else [], DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW),
            (historical_support, DISTRICT_PUBLIC_OPINION_BILL_TOPIC_SUPPORT),
            ([local] if local else [], BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW),
            ([external] if external else [], BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW),
            (mention_packets, BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW),
            ([target_scope] if target_scope else [], BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW),
            ([codified] if codified else [], STATUTORY_LINEAGE_CODIFIED_PROGRESS),
            (bridge_rows, STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE),
            (text_rows, RULEMAKING_COMMENT_TEXT_REVIEW),
        ]:
            if grouped_rows:
                artifacts.append(source_artifact(path))
                for row in grouped_rows:
                    evidence_layers.extend(split_values(row.get("evidence_layers", "")))
                    missing_links.extend(split_values(row.get("missing_links", "")))

        bill_history_status = (
            "bounded_congressgov_public_law_bill_action_context"
            if int_field(spine, "actions_count") > 0
            else "bill_history_context_missing"
        )
        sponsor_status = (
            "sponsor_metadata_present"
            if spine.get("sponsor_bioguide_id", "").strip()
            else "sponsor_metadata_missing"
        )
        public_opinion_status = (
            "historical_related_issue_district_support_available_not_exact_bill_support"
            if historical_support
            else
            compact_status(
                survey.get("current_proxy_review_status", ""),
                "survey_item_proxy_review_present",
            )
            if survey
            else "no_district_public_opinion_survey_packet"
        )
        statutory_status = compact_status(
            codified.get("codified_progress_status", ""),
            "no_codified_lineage_progress_row",
        )
        finance_lobbying_status = finance_status(
            spine,
            local,
            external,
            mention_packets,
            target_scope,
        )
        implementation_review_status = implementation_status(spine, text_rows)
        comment_detail_statuses = unique_join([
            row.get("detail_fetch_status", "").strip()
            for row in text_rows
            if row.get("detail_fetch_status", "").strip()
        ])

        rows.append({
            "corpus_rank": action.get("action_rank", "").strip(),
            "action_rank": action.get("action_rank", "").strip(),
            "bill_id": bill_id,
            "public_law_number": action.get("public_law_number", "").strip(),
            "policy_area": action.get("policy_area", "").strip(),
            "lifecycle_readiness_tier": action.get("lifecycle_readiness_tier", "").strip(),
            "review_score": action.get("review_score", "").strip(),
            "corpus_packet_status": packet_status(
                actionable_gap_count,
                source_reviewed_subgate_count,
            ),
            "publication_readiness_status": publication_status(
                actionable_gap_count,
                source_reviewed_subgate_count,
            ),
            "next_actionable_upgrade_gate": action.get("next_actionable_upgrade_gate", "").strip(),
            "actionable_high_priority_gaps": action.get("actionable_high_priority_gaps", "").strip(),
            "actionable_gap_count": action.get("actionable_gap_count", "").strip(),
            "closed_review_gates": action.get("closed_review_gates", "").strip(),
            "closed_review_gate_count": action.get("closed_review_gate_count", "").strip(),
            "bill_history_context_status": bill_history_status,
            "sponsor_context_status": sponsor_status,
            "district_public_opinion_status": public_opinion_status,
            "public_opinion_proxy_review_status": compact_status(
                survey.get("current_proxy_review_status", ""),
                "no_survey_proxy_review_row",
            ),
            "bill_topic_item_review_status": compact_status(
                "source_reviewed_historical_related_issue_item_alignment_available"
                if historical_support
                else survey.get("bill_topic_item_review_status", ""),
                "no_bill_topic_survey_item_review_row",
            ),
            "district_estimation_status": compact_status(
                "privacy_thresholded_historical_direct_weighted_estimate_available"
                if historical_support
                else survey.get("district_estimation_status", ""),
                "no_district_estimation_review_row",
            ),
            "historical_related_issue_support_estimate_rows": str(len(historical_support)),
            "historical_related_issue_support_years": unique_join([
                row.get("survey_year", "") for row in historical_support
            ]),
            "historical_related_issue_support_items": unique_join([
                row.get("survey_item_id", "") for row in historical_support
            ]),
            "historical_weighted_support_min": (
                f"{min(float(row['weighted_support_share']) for row in historical_support):.6f}"
                if historical_support
                else ""
            ),
            "historical_weighted_support_max": (
                f"{max(float(row['weighted_support_share']) for row in historical_support):.6f}"
                if historical_support
                else ""
            ),
            "exact_bill_support_status": (
                "not_measured_historical_related_issue_only"
                if historical_support
                else "not_measured"
            ),
            "affected_group_item_status": compact_status(
                survey.get("affected_group_item_status", ""),
                "no_affected_group_item_review_row",
            ),
            "finance_lobbying_review_status": finance_lobbying_status,
            "local_finance_lobbying_status": compact_status(
                local.get("manual_bill_specific_gate_status", ""),
                "not_in_local_finance_lobbying_review",
            ),
            "external_lda_search_status": compact_status(
                external.get("combined_external_review_status", ""),
                "not_in_external_lda_search_review",
            ),
            "external_lda_mention_review_packets": str(len(mention_packets)),
            "campaign_finance_target_scope_status": compact_status(
                target_scope.get("target_scope_disposition", ""),
                "not_in_campaign_finance_target_scope_review",
            ),
            "statutory_lineage_status": statutory_status,
            "target_diff_review_rows": codified.get("target_diff_review_rows", "0"),
            "source_reviewed_target_section_diff_rows": codified.get(
                "source_reviewed_target_section_diff_rows",
                "0",
            ),
            "reviewed_no_target_rows": codified.get("reviewed_no_structured_usc_target_rows", "0"),
            "target_lifecycle_bridge_rows": str(len(bridge_rows)),
            "rulemaking_implementation_status": implementation_review_status,
            "authority_rule_rows": spine.get("implementation_authority_rule_rows", "0"),
            "authority_text_verified_rows": spine.get(
                "implementation_authority_text_verified_rows",
                "0",
            ),
            "comment_record_docket_rows": spine.get("implementation_comment_record_docket_rows", "0"),
            "complete_comment_record_docket_rows": spine.get(
                "implementation_comment_record_complete_docket_rows",
                "0",
            ),
            "comment_text_review_rows": str(len(text_rows)),
            "comment_text_available_rows": str(text_available),
            "comment_detail_statuses": comment_detail_statuses,
            "court_review_status": action.get("court_direct_review_status", "").strip(),
            "court_direct_review_rows": action.get("court_direct_review_rows", "0").strip(),
            "court_direct_review_direct_rows": action.get("court_direct_review_direct_rows", "0").strip(),
            "court_direct_review_not_direct_rows": action.get(
                "court_direct_review_not_direct_rows",
                "0",
            ).strip(),
            "court_direct_review_temporal_exclusions": action.get(
                "court_direct_review_temporal_exclusions",
                "0",
            ).strip(),
            "court_direct_review_source_summary_rows": str(direct_source_summary_rows),
            "source_reviewed_subgate_count": str(source_reviewed_subgate_count),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(artifacts),
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
    packet_statuses = Counter(row["corpus_packet_status"] for row in rows)
    publication_statuses = Counter(row["publication_readiness_status"] for row in rows)
    next_gates = Counter(row["next_actionable_upgrade_gate"] for row in rows)
    public_opinion_proxy_rows = [
        row for row in rows
        if row["public_opinion_proxy_review_status"] != "no_survey_proxy_review_row"
    ]
    acquired_bill_topic_item_rows = [
        row for row in rows
        if row["bill_topic_item_review_status"] != "no_bill_topic_survey_item_acquired"
        and row["bill_topic_item_review_status"] != "no_bill_topic_survey_item_review_row"
    ]
    historical_issue_support_rows = [
        row for row in rows
        if int(row["historical_related_issue_support_estimate_rows"] or "0") > 0
    ]
    exact_bill_topic_item_rows = [
        row for row in rows
        if row["exact_bill_support_status"] not in {
            "not_measured",
            "not_measured_historical_related_issue_only",
        }
    ]
    target_diff_rows = [
        row for row in rows
        if int(row["source_reviewed_target_section_diff_rows"] or "0") > 0
    ]
    no_target_rows = [
        row for row in rows
        if int(row["reviewed_no_target_rows"] or "0") > 0
    ]
    finance_target_scope_rows = [
        row for row in rows
        if row["campaign_finance_target_scope_status"]
        != "not_in_campaign_finance_target_scope_review"
    ]
    direct_review_closed_rows = [
        row for row in rows
        if int(row["closed_review_gate_count"] or "0") > 0
    ]
    comment_text_rows = [
        row for row in rows
        if int(row["comment_text_review_rows"] or "0") > 0
    ]
    comment_text_available_rows = [
        row for row in rows
        if int(row["comment_text_available_rows"] or "0") > 0
    ]

    lines = [
        "# Bill-Law Lifecycle Corpus",
        "",
        "This report assembles one bounded packet per public-law row by joining the lifecycle action queue to existing source-review, metadata, proxy, and comment-detail reports. It is a corpus index and review ledger, not validation evidence.",
        "",
        f"- Public-law corpus rows: {len(rows)}",
        f"- Rows with district public-opinion proxy review attached: {len(public_opinion_proxy_rows)}",
        f"- Rows with acquired bill-topic survey items: {len(exact_bill_topic_item_rows)}",
        f"- Rows with source-reviewed bill-item or related-issue items: {len(acquired_bill_topic_item_rows)}",
        f"- Rows with privacy-thresholded historical related-issue district estimates: {len(historical_issue_support_rows)}",
        f"- Rows with source-reviewed target-section diff coverage: {len(target_diff_rows)}",
        f"- Rows with reviewed no-structured-U.S.C.-target disposition: {len(no_target_rows)}",
        f"- Rows with campaign-finance target-scope review: {len(finance_target_scope_rows)}",
        f"- Rows with closed direct court-review gates: {len(direct_review_closed_rows)}",
        f"- Rows with sanitized comment-detail review: {len(comment_text_rows)}",
        f"- Rows with public comment text available and hashed: {len(comment_text_available_rows)}",
        "",
        "Corpus packet statuses:",
    ]
    for status, count in sorted(packet_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Publication readiness statuses:"])
    for status, count in sorted(publication_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Next actionable upgrade gates:"])
    for gate, count in sorted(next_gates.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {gate}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Packet status | Next gate | Public opinion | Finance/lobbying | Statutory lineage | Implementation | Court review |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['corpus_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['corpus_packet_status']} | {row['next_actionable_upgrade_gate']} | "
            f"{row['bill_topic_item_review_status']} | {row['finance_lobbying_review_status']} | "
            f"{row['statutory_lineage_status']} | {row['rulemaking_implementation_status']} | "
            f"{row['court_review_status']} |"
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
