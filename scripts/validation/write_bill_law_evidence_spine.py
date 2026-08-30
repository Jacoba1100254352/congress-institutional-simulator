#!/usr/bin/env python3
"""Write a bounded bill/public-law evidence spine from cached linkage files."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median


BILL_PROGRESSION = Path("data/validation/raw/bill_progression.csv")
LAW_REVISION_HISTORY = Path("data/validation/raw/law_revision_history.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
DISTRICT_PUBLIC_OPINION_LINKAGE = Path("data/validation/raw/district_public_opinion_linkage.csv")
DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT = Path("data/validation/raw/district_public_opinion_policy_context.csv")
CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT = Path("reports/campaign-finance-sponsor-bill-context.csv")
LOBBYING_BILL_POLICY_CONTEXT = Path("reports/lobbying-bill-policy-context.csv")
LOBBYING_BILL_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
RULEMAKING_AUTHORITY_LINKAGE = Path("data/validation/raw/rulemaking_authority_linkage.csv")
RULEMAKING_HISTORY_LINKAGE = Path("data/validation/raw/rulemaking_history_linkage.csv")
RULEMAKING_COMMENT_METADATA = Path("data/validation/raw/rulemaking_comment_metadata.csv")
RULEMAKING_COMMENT_RECORDS = Path("data/validation/raw/rulemaking_comment_records.csv")
STATUTORY_LINEAGE_ADJUDICATION = Path("data/validation/raw/statutory_lineage_adjudication.csv")
STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS = Path("data/validation/raw/statutory_lineage_target_review_packets.csv")
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW = Path(
    "reports/statutory-lineage-target-section-diff-review.csv"
)
STATUTORY_LINEAGE_NO_TARGET_REVIEW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
COURT_LAW_LINKAGE = Path("data/validation/raw/court_law_linkage.csv")
OUT_CSV = Path("reports/bill-law-evidence-spine.csv")
OUT_MD = Path("reports/bill-law-evidence-spine.md")

FIELDNAMES = [
    "bill_id",
    "public_law_number",
    "congress",
    "bill_type",
    "bill_number",
    "policy_area",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "introduced_date",
    "enacted_date",
    "actions_count",
    "committee_reported",
    "floor_considered",
    "bill_progression_sample_present",
    "law_revision_text_present",
    "amended",
    "reauthorized",
    "repealed",
    "expired",
    "invalidated",
    "revision_terms",
    "statutory_lineage_adjudication_rows",
    "statutory_lineage_marker_rows",
    "statutory_lineage_marker_statuses",
    "statutory_lineage_marker_strengths",
    "statutory_lineage_marker_target_references",
    "statutory_lineage_marker_pre_anchor_rows",
    "statutory_lineage_marker_post_anchor_rows",
    "statutory_lineage_marker_public_law_context_count",
    "statutory_lineage_target_review_packet_rows",
    "statutory_lineage_target_review_ready_packet_rows",
    "statutory_lineage_target_review_packet_statuses",
    "statutory_lineage_target_review_packet_strengths",
    "statutory_lineage_target_review_packet_public_law_context_count",
    "statutory_lineage_target_section_diff_review_rows",
    "statutory_lineage_target_section_diff_review_statuses",
    "statutory_lineage_target_section_diff_review_relationships",
    "statutory_lineage_source_reviewed_target_section_diff_rows",
    "statutory_lineage_no_target_review_rows",
    "statutory_lineage_no_target_review_statuses",
    "statutory_lineage_no_target_review_dispositions",
    "district_public_opinion_context_rows",
    "district_public_opinion_unique_keys",
    "district_ids",
    "district_issues",
    "district_public_opinion_policy_context_rows",
    "district_public_opinion_policy_context_unique_keys",
    "district_public_opinion_policy_areas",
    "district_public_opinion_policy_topic_introduced",
    "district_public_opinion_policy_topic_floor_considered",
    "district_public_opinion_policy_topic_enacted",
    "campaign_finance_sponsor_policy_context_rows",
    "campaign_finance_sponsor_policy_context_transaction_rows",
    "campaign_finance_sponsor_policy_context_unique_candidates",
    "campaign_finance_sponsor_policy_context_bill_ids",
    "campaign_finance_sponsor_policy_context_enacted_bill_ids",
    "lobbying_policy_context_issue_rows",
    "lobbying_policy_context_activity_rows",
    "lobbying_policy_context_total_amount",
    "lobbying_policy_context_bill_contexts",
    "lobbying_policy_context_bill_ids",
    "lobbying_policy_context_enacted_bill_ids",
    "lobbying_policy_context_issues",
    "lobbying_bill_mention_rows",
    "lobbying_bill_mention_unique_filings",
    "lobbying_bill_mention_clients",
    "lobbying_bill_mention_registrants",
    "lobbying_bill_mention_activity_issues",
    "lobbying_bill_mention_filing_years",
    "lobbying_bill_mention_document_urls",
    "lobbying_bill_mention_matched_refs",
    "implementation_authority_rule_rows",
    "implementation_authority_text_verified_rows",
    "implementation_authority_document_numbers",
    "implementation_authority_publication_dates",
    "implementation_authority_agencies",
    "implementation_authority_cfr_references",
    "implementation_authority_usc_citations",
    "implementation_history_final_rule_rows",
    "implementation_history_matched_final_rule_rows",
    "implementation_history_proposed_rule_links",
    "implementation_history_proposed_document_numbers",
    "implementation_history_proposed_comment_close_date_count",
    "implementation_history_proposed_comment_close_dates",
    "implementation_history_proposed_regulations_docket_count",
    "implementation_history_proposed_regulations_docket_ids",
    "implementation_history_proposed_comment_portal_count",
    "implementation_history_proposed_regulations_comment_urls",
    "implementation_history_shared_identifiers",
    "implementation_comment_metadata_rows",
    "implementation_comment_metadata_statuses",
    "implementation_comment_metadata_final_regulations_docket_count",
    "implementation_comment_metadata_final_regulations_docket_ids",
    "implementation_comment_metadata_final_comment_count_rows",
    "implementation_comment_metadata_final_positive_comment_count_rows",
    "implementation_comment_metadata_final_comment_count_total",
    "implementation_comment_metadata_proposed_detail_fetch_count",
    "implementation_comment_metadata_proposed_regulations_docket_count",
    "implementation_comment_metadata_proposed_regulations_docket_ids",
    "implementation_comment_metadata_proposed_comment_url_count",
    "implementation_comment_metadata_proposed_comment_urls",
    "implementation_comment_metadata_proposed_comment_count_rows",
    "implementation_comment_metadata_proposed_positive_comment_count_rows",
    "implementation_comment_metadata_proposed_comment_count_total",
    "implementation_comment_metadata_proposed_comment_close_date_count",
    "implementation_comment_metadata_proposed_comment_close_dates",
    "implementation_comment_record_docket_rows",
    "implementation_comment_record_complete_docket_rows",
    "implementation_comment_record_partial_or_blocked_docket_rows",
    "implementation_comment_record_statuses",
    "implementation_comment_record_docket_ids",
    "implementation_comment_record_expected_comment_count_total",
    "implementation_comment_record_retrieved_comment_count_total",
    "implementation_comment_record_api_total_count",
    "implementation_comment_record_ids",
    "implementation_history_final_effective_rule_rows",
    "implementation_history_final_effective_dates",
    "implementation_history_final_to_effective_delay_count",
    "implementation_history_final_to_effective_delay_min_days",
    "implementation_history_final_to_effective_delay_median_days",
    "implementation_history_final_to_effective_delay_max_days",
    "implementation_history_proposed_to_final_delay_count",
    "implementation_history_proposed_to_final_delay_min_days",
    "implementation_history_proposed_to_final_delay_median_days",
    "implementation_history_proposed_to_final_delay_max_days",
    "court_review_overlap_case_rows",
    "court_review_invalidated_case_rows",
    "court_review_case_ids",
    "court_review_usc_sections",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Derived metadata spine only; sponsor-district bill policy-area context is "
    "bounded topic-throughput context, campaign-finance sponsor context and lobbying "
    "issue context are shared-policy-area metadata, exact LDA filing-text bill mentions "
    "are bill-identifier evidence only and not bill-specific finance or lobbying "
    "influence, final-rule timing metadata is not an implementation outcome, "
    "Federal Register-exposed Regulations.gov comment metadata is not a complete "
    "public-comment record by itself, partial Regulations.gov comment-record "
    "metadata does not prove complete comment coverage, complete Regulations.gov "
    "comment-record metadata is not comment text, attachment review, commenter identity, or "
    "implementation feedback, official OLRC public-law marker adjudication and "
    "target-section review packets are not source-reviewed target-section text diffs, "
    "source-reviewed target-section diff dispositions do not establish exclusive "
    "public-law causal attribution or effective statutory text, and proposed-rule "
    "timing metadata is not a direct court-review disposition. Reviewed designation-law "
    "no-target dispositions close only the no-structured-U.S.C.-target classification "
    "gate and are not target-section diff, implementation, court-review, welfare, "
    "causal effect, or model validation evidence."
)

COMPLETE_COMMENT_RECORD_STATUSES = {
    "complete_comment_record_metadata_retrieved",
    "complete_no_comments_expected",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "").strip()
        if value and value not in result:
            result[value] = row
    return result


def issue_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("district_id", "").strip(),
        row.get("issue", "").strip(),
        row.get("year", "").strip(),
    )


def int_field(row: dict[str, str], field: str) -> int:
    try:
        return int(row.get(field, "0") or "0")
    except ValueError:
        return 0


def float_field(row: dict[str, str], field: str) -> float:
    try:
        return float(row.get(field, "0") or "0")
    except ValueError:
        return 0.0


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def parse_iso_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip()) if value.strip() else None
    except ValueError:
        return None


def days_between(start: str, end: str) -> int | None:
    start_date = parse_iso_date(start)
    end_date = parse_iso_date(end)
    if not start_date or not end_date:
        return None
    return (end_date - start_date).days


def numeric_summary(values: list[int]) -> dict[str, str]:
    if not values:
        return {
            "count": "0",
            "min": "",
            "median": "",
            "max": "",
        }
    median_value = median(values)
    if isinstance(median_value, int) or (
        isinstance(median_value, float) and median_value.is_integer()
    ):
        median_text = str(int(median_value))
    else:
        median_text = f"{median_value:.1f}"
    return {
        "count": str(len(values)),
        "min": str(min(values)),
        "median": median_text,
        "max": str(max(values)),
    }


def policy_context_topic_totals(rows: list[dict[str, str]]) -> dict[str, int]:
    """Deduplicate repeated district survey proxy rows before totaling topic counts."""
    by_policy_area: dict[str, dict[str, int]] = {}
    for row in rows:
        policy_area = row.get("policy_area", "").strip()
        if not policy_area:
            continue
        current = by_policy_area.setdefault(
            policy_area,
            {
                "topic_introduced": 0,
                "topic_floor_considered": 0,
                "topic_enacted": 0,
            },
        )
        for field in current:
            current[field] = max(current[field], int_field(row, field))
    return {
        field: sum(policy_counts[field] for policy_counts in by_policy_area.values())
        for field in ("topic_introduced", "topic_floor_considered", "topic_enacted")
    }


def missing_links(
    district_rows: list[dict[str, str]],
    policy_context_rows: list[dict[str, str]],
    campaign_context_rows: list[dict[str, str]],
    lobbying_context_rows: list[dict[str, str]],
    lobbying_bill_mention_rows: list[dict[str, str]],
    bill_progression_present: bool,
    authority_match: bool,
    history_match: bool,
    court_overlap: bool,
    codified_lineage_gap: bool,
    complete_comment_records: bool,
) -> str:
    links = [
        "bill_topic_public_opinion",
        "model_validation",
    ]
    if not lobbying_bill_mention_rows:
        links.append("bill_specific_campaign_finance_or_lobbying_to_bill")
    if codified_lineage_gap:
        links.extend([
            "codified_usc_lineage",
            "public_law_causal_attribution",
            "law_revision_effective_text",
        ])
    else:
        links.extend([
            "target_section_diff_not_applicable_designation_law",
            "public_law_causal_attribution_not_applicable_no_target",
            "law_revision_effective_text_not_applicable_no_target",
        ])
    if not campaign_context_rows:
        links.append("campaign_finance_sponsor_policy_area_context")
    if not lobbying_context_rows:
        links.append("lobbying_issue_policy_area_context")
    if court_overlap:
        links.append("direct_case_to_public_law_identifier")
        links.append("reviewed_case_disposition_to_public_law")
    else:
        links.append("court_review_or_invalidation")
    if authority_match:
        if not history_match:
            links.append("proposed_rule_history")
        if not complete_comment_records:
            links.append("complete_regulations_comments")
        links.append("unified_agenda_stage")
        links.append("implementation_outcomes_or_enforcement")
    else:
        links.append("implementation_or_rulemaking_authority")
    if not district_rows:
        links.append("sponsor_district_public_opinion_context")
    if not policy_context_rows:
        links.append("sponsor_district_bill_policy_area_context")
    if not bill_progression_present:
        links.append("full_bill_progression_census_overlap")
    return "; ".join(links)


def build_rows() -> list[dict[str, str]]:
    bill_progression_by_bill = by_key(read_csv(BILL_PROGRESSION), "bill_id")
    law_history_by_bill = by_key(read_csv(LAW_REVISION_HISTORY), "bill_id")
    law_history_by_public_law = by_key(read_csv(LAW_REVISION_HISTORY), "public_law_number")
    authority_by_public_law = by_key(read_csv(RULEMAKING_AUTHORITY_LINKAGE), "public_law_number")
    history_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(RULEMAKING_HISTORY_LINKAGE):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            history_rows_by_public_law[public_law].append(row)
    comment_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(RULEMAKING_COMMENT_METADATA):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            comment_rows_by_public_law[public_law].append(row)
    comment_record_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(RULEMAKING_COMMENT_RECORDS):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            comment_record_rows_by_public_law[public_law].append(row)
    statutory_adjudication_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(STATUTORY_LINEAGE_ADJUDICATION):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_adjudication_rows_by_public_law[public_law].append(row)
    statutory_review_packet_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_review_packet_rows_by_public_law[public_law].append(row)
    statutory_diff_review_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_diff_review_rows_by_public_law[public_law].append(row)
    statutory_no_target_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(STATUTORY_LINEAGE_NO_TARGET_REVIEW):
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_no_target_rows_by_public_law[public_law].append(row)
    bill_linkage_rows = read_csv(LAW_REVISION_BILL_LINKAGE)
    district_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(DISTRICT_PUBLIC_OPINION_LINKAGE):
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            district_rows_by_bill[bill_id].append(row)
    policy_context_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT):
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            policy_context_rows_by_bill[bill_id].append(row)
    campaign_context_rows_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT):
        for policy_area in split_values(row.get("matched_policy_areas", "")):
            campaign_context_rows_by_policy_area[policy_area].append(row)
    lobbying_context_rows_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(LOBBYING_BILL_POLICY_CONTEXT):
        if row.get("policy_context_status") != "lobbying_issue_bill_policy_context":
            continue
        topic = row.get("topic", "").strip()
        if topic:
            lobbying_context_rows_by_policy_area[topic].append(row)
    lobbying_mention_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(LOBBYING_BILL_MENTIONS):
        bill_id = row.get("bill_id", "").strip()
        if bill_id and row.get("exact_current_bill_match", "").strip() == "1":
            lobbying_mention_rows_by_bill[bill_id].append(row)
    court_rows_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(COURT_LAW_LINKAGE):
        if row.get("linkage_status") != "usc_section_authority_overlap":
            continue
        for public_law in row.get("public_law_numbers", "").split(";"):
            public_law = public_law.strip()
            if public_law:
                court_rows_by_public_law[public_law].append(row)

    rows: list[dict[str, str]] = []
    for bill in sorted(bill_linkage_rows, key=lambda row: row.get("bill_id", "")):
        bill_id = bill.get("bill_id", "").strip()
        public_law_number = bill.get("public_law_number", "").strip()
        law = law_history_by_bill.get(bill_id, law_history_by_public_law.get(public_law_number, {}))
        statutory_adjudication_rows = statutory_adjudication_rows_by_public_law.get(public_law_number, [])
        statutory_marker_rows = [
            row for row in statutory_adjudication_rows
            if row.get("codified_lineage_marker", "").strip() == "1"
        ]
        statutory_marker_statuses = sorted({
            row.get("lineage_adjudication_status", "").strip()
            for row in statutory_marker_rows
            if row.get("lineage_adjudication_status", "").strip()
        })
        statutory_marker_strengths = sorted({
            row.get("lineage_marker_strength", "").strip()
            for row in statutory_marker_rows
            if row.get("lineage_marker_strength", "").strip()
        })
        statutory_marker_targets = sorted({
            row.get("target_reference", "").strip()
            for row in statutory_marker_rows
            if row.get("target_reference", "").strip()
        })
        statutory_review_packet_rows = statutory_review_packet_rows_by_public_law.get(
            public_law_number,
            [],
        )
        statutory_review_ready_packet_rows = [
            row for row in statutory_review_packet_rows
            if row.get("target_review_packet_status", "").strip()
            != "target_section_review_packet_needs_manual_source_retrieval"
        ]
        statutory_review_packet_statuses = sorted({
            row.get("target_review_packet_status", "").strip()
            for row in statutory_review_packet_rows
            if row.get("target_review_packet_status", "").strip()
        })
        statutory_review_packet_strengths = sorted({
            row.get("target_review_packet_strength", "").strip()
            for row in statutory_review_packet_rows
            if row.get("target_review_packet_strength", "").strip()
        })
        statutory_diff_review_rows = statutory_diff_review_rows_by_public_law.get(
            public_law_number,
            [],
        )
        statutory_source_reviewed_diff_rows = [
            row for row in statutory_diff_review_rows
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        statutory_diff_review_statuses = sorted({
            row.get("review_status", "").strip()
            for row in statutory_diff_review_rows
            if row.get("review_status", "").strip()
        })
        statutory_diff_review_relationships = sorted({
            row.get("codified_lineage_relationship", "").strip()
            for row in statutory_diff_review_rows
            if row.get("codified_lineage_relationship", "").strip()
        })
        statutory_no_target_rows = statutory_no_target_rows_by_public_law.get(
            public_law_number,
            [],
        )
        statutory_no_target_statuses = sorted({
            row.get("review_status", "").strip()
            for row in statutory_no_target_rows
            if row.get("review_status", "").strip()
        })
        statutory_no_target_dispositions = sorted({
            row.get("codification_disposition", "").strip()
            for row in statutory_no_target_rows
            if row.get("codification_disposition", "").strip()
        })
        authority = authority_by_public_law.get(public_law_number, {})
        history_rows = history_rows_by_public_law.get(public_law_number, [])
        comment_rows = comment_rows_by_public_law.get(public_law_number, [])
        comment_record_rows = comment_record_rows_by_public_law.get(public_law_number, [])
        history_match_rows = [
            row for row in history_rows
            if row.get("history_status") == "proposed_rule_history_match"
        ]
        proposed_documents = sorted({
            document.strip()
            for row in history_match_rows
            for document in row.get("proposed_document_numbers", "").split(";")
            if document.strip()
        })
        proposed_comment_close_dates = sorted({
            date.strip()
            for row in history_match_rows
            for date in row.get("proposed_comment_close_dates", "").split(";")
            if date.strip()
        })
        proposed_regulations_docket_ids = sorted({
            docket_id.strip()
            for row in history_match_rows
            for docket_id in row.get("proposed_regulations_docket_ids", "").split(";")
            if docket_id.strip()
        })
        proposed_regulations_comment_urls = sorted({
            url.strip()
            for row in history_match_rows
            for url in row.get("proposed_regulations_comments_urls", "").split(";")
            if url.strip()
        })
        comment_statuses = sorted({
            row.get("comment_metadata_status", "").strip()
            for row in comment_rows
            if row.get("comment_metadata_status", "").strip()
        })
        comment_final_docket_ids = sorted({
            row.get("final_regulations_docket_id", "").strip()
            for row in comment_rows
            if row.get("final_regulations_docket_id", "").strip()
        })
        comment_final_counts = [
            int_field(row, "final_regulations_comments_count")
            for row in comment_rows
            if row.get("final_regulations_comments_count", "").strip()
        ]
        comment_proposed_docket_ids = sorted({
            docket.strip()
            for row in comment_rows
            for docket in row.get("proposed_regulations_docket_ids_refetched", "").split(";")
            if docket.strip()
        })
        comment_proposed_urls = sorted({
            url.strip()
            for row in comment_rows
            for url in row.get("proposed_regulations_comments_urls_refetched", "").split(";")
            if url.strip()
        })
        comment_proposed_close_dates = sorted({
            date.strip()
            for row in comment_rows
            for date in row.get("proposed_comments_close_dates_refetched", "").split(";")
            if date.strip()
        })
        comment_metadata_present = bool(
            comment_final_docket_ids
            or comment_final_counts
            or comment_proposed_docket_ids
            or comment_proposed_urls
            or comment_proposed_close_dates
        )
        comment_metadata_docket_ids = set(comment_final_docket_ids) | set(comment_proposed_docket_ids)
        comment_record_statuses = sorted({
            row.get("retrieval_status", "").strip()
            for row in comment_record_rows
            if row.get("retrieval_status", "").strip()
        })
        comment_record_docket_ids = sorted({
            row.get("docket_id", "").strip()
            for row in comment_record_rows
            if row.get("docket_id", "").strip()
        })
        comment_record_complete_rows = [
            row for row in comment_record_rows
            if row.get("retrieval_status", "").strip() in COMPLETE_COMMENT_RECORD_STATUSES
        ]
        comment_record_partial_or_blocked_rows = [
            row for row in comment_record_rows
            if row.get("retrieval_status", "").strip() not in COMPLETE_COMMENT_RECORD_STATUSES
        ]
        comment_record_ids = sorted({
            comment_id.strip()
            for row in comment_record_rows
            for comment_id in row.get("retrieved_comment_ids", "").split(";")
            if comment_id.strip()
        })
        partial_comment_records = any(
            "regulations_gov_partial_comment_record_metadata" in row.get("evidence_layers", "")
            for row in comment_record_rows
        )
        complete_comment_records = bool(comment_metadata_docket_ids) and (
            comment_metadata_docket_ids <= set(comment_record_docket_ids)
        ) and not [
            row for row in comment_record_rows
            if row.get("docket_id", "").strip() in comment_metadata_docket_ids
            and row.get("retrieval_status", "").strip() not in COMPLETE_COMMENT_RECORD_STATUSES
        ]
        shared_identifiers = sorted({
            identifier.strip()
            for row in history_match_rows
            for identifier in row.get("shared_identifiers", "").split(";")
            if identifier.strip()
        })
        final_effective_dates = sorted({
            row.get("final_effective_date", "").strip()
            for row in history_rows
            if row.get("final_effective_date", "").strip()
        })
        final_to_effective_delays = [
            delay
            for row in history_rows
            for delay in [
                days_between(
                    row.get("final_publication_date", ""),
                    row.get("final_effective_date", ""),
                )
            ]
            if delay is not None
        ]
        final_to_effective_summary = numeric_summary(final_to_effective_delays)
        proposed_to_final_delays = [
            int(row.get("days_from_earliest_proposed_to_final", ""))
            for row in history_match_rows
            if row.get("days_from_earliest_proposed_to_final", "").strip()
        ]
        proposed_to_final_summary = numeric_summary(proposed_to_final_delays)
        proposed_rule_links = sum(int_field(row, "matched_proposed_rule_count") for row in history_rows)
        district_rows = district_rows_by_bill.get(bill_id, [])
        district_ids = sorted({row.get("district_id", "").strip() for row in district_rows if row.get("district_id", "").strip()})
        district_issues = sorted({row.get("issue", "").strip() for row in district_rows if row.get("issue", "").strip()})
        unique_district_keys = {issue_key(row) for row in district_rows if all(issue_key(row))}
        policy_context_rows = policy_context_rows_by_bill.get(bill_id, [])
        unique_policy_context_keys = {
            issue_key(row) for row in policy_context_rows if all(issue_key(row))
        }
        policy_context_areas = sorted({
            row.get("policy_area", "").strip()
            for row in policy_context_rows
            if row.get("policy_area", "").strip()
        })
        policy_context_topic_counts = policy_context_topic_totals(policy_context_rows)
        policy_area = bill.get("policy_area", "") or law.get("policy_area", "")
        campaign_context_rows = campaign_context_rows_by_policy_area.get(policy_area, [])
        campaign_context_candidates = sorted({
            row.get("candidate_id", "").strip() or row.get("bioguide_id", "").strip()
            for row in campaign_context_rows
            if row.get("candidate_id", "").strip() or row.get("bioguide_id", "").strip()
        })
        campaign_context_bill_ids = sorted({
            bill_id
            for row in campaign_context_rows
            for bill_id in split_values(row.get("matched_bill_ids", ""))
        })
        campaign_context_enacted_bill_ids = sorted({
            bill_id
            for row in campaign_context_rows
            for bill_id in split_values(row.get("matched_enacted_bill_ids", ""))
        })
        lobbying_context_rows = lobbying_context_rows_by_policy_area.get(policy_area, [])
        lobbying_context_bill_ids = sorted({
            bill_id
            for row in lobbying_context_rows
            for bill_id in split_values(row.get("matched_bill_ids", ""))
        })
        lobbying_context_enacted_bill_ids = sorted({
            bill_id
            for row in lobbying_context_rows
            for bill_id in split_values(row.get("matched_enacted_bill_ids", ""))
        })
        lobbying_context_issues = sorted({
            row.get("lobbying_issue", "").strip()
            for row in lobbying_context_rows
            if row.get("lobbying_issue", "").strip()
        })
        lobbying_mention_rows = lobbying_mention_rows_by_bill.get(bill_id, [])
        lobbying_mention_filings = sorted({
            row.get("filing_uuid", "").strip()
            for row in lobbying_mention_rows
            if row.get("filing_uuid", "").strip()
        })
        lobbying_mention_clients = sorted({
            row.get("client_name", "").strip()
            for row in lobbying_mention_rows
            if row.get("client_name", "").strip()
        })
        lobbying_mention_registrants = sorted({
            row.get("registrant_name", "").strip()
            for row in lobbying_mention_rows
            if row.get("registrant_name", "").strip()
        })
        lobbying_mention_issues = sorted({
            row.get("activity_issue", "").strip()
            for row in lobbying_mention_rows
            if row.get("activity_issue", "").strip()
        })
        lobbying_mention_years = sorted({
            row.get("filing_year", "").strip()
            for row in lobbying_mention_rows
            if row.get("filing_year", "").strip()
        })
        lobbying_mention_document_urls = sorted({
            row.get("filing_document_url", "").strip()
            for row in lobbying_mention_rows
            if row.get("filing_document_url", "").strip()
        })
        lobbying_mention_matched_refs = sorted({
            ref.strip()
            for row in lobbying_mention_rows
            for ref in split_values(row.get("matched_bill_refs", ""))
            if ref.strip()
        })
        court_rows = court_rows_by_public_law.get(public_law_number, [])
        court_case_ids = sorted({
            row.get("case_id", "").strip()
            for row in court_rows
            if row.get("case_id", "").strip()
        })
        court_invalidated_case_ids = sorted({
            row.get("case_id", "").strip()
            for row in court_rows
            if row.get("case_id", "").strip() and row.get("invalidated") == "1"
        })
        court_usc_sections = sorted({
            section.strip()
            for row in court_rows
            for section in row.get("matched_usc_sections", "").split(";")
            if section.strip()
        })
        bill_progression_present = bill_id in bill_progression_by_bill
        authority_match = authority.get("linkage_status") == "federal_register_authority_match"
        history_match = bool(history_match_rows)
        court_overlap = bool(court_rows)
        layers = ["bill_action_metadata"]
        if law:
            layers.append("law_revision_text_proxy")
        if statutory_marker_rows:
            layers.append("official_olrc_public_law_marker_adjudication")
            layers.append("official_olrc_post_only_public_law_marker")
        if statutory_review_packet_rows:
            layers.append("statutory_lineage_target_section_review_packet")
        if statutory_diff_review_rows:
            layers.append("statutory_lineage_target_section_diff_review")
        if statutory_source_reviewed_diff_rows:
            layers.append("statutory_lineage_source_reviewed_target_section_diff")
        if statutory_no_target_rows:
            layers.append("statutory_lineage_no_target_review")
        if any(
            row.get("source_reviewed_no_structured_usc_target", "").strip() == "1"
            for row in statutory_no_target_rows
        ):
            layers.append("statutory_lineage_source_reviewed_no_structured_usc_target")
        if district_rows:
            layers.append("sponsor_district_public_opinion_metadata")
        if policy_context_rows:
            layers.append("sponsor_district_bill_policy_area_context")
        if any(
            "topic_throughput_policy_area" in row.get("evidence_layers", "")
            for row in policy_context_rows
        ):
            layers.append("topic_throughput_policy_area")
        if campaign_context_rows:
            layers.append("campaign_finance_sponsor_policy_area_context")
        if lobbying_context_rows:
            layers.append("lobbying_issue_bill_policy_area_context")
        if lobbying_mention_rows:
            layers.append("official_lda_filing_text_bill_identifier")
        if authority_match:
            layers.append("federal_register_authority_search_match")
        if int_field(authority, "text_verified_rule_count") > 0:
            layers.append("federal_register_authority_text_verified")
        if history_match:
            layers.append("federal_register_proposed_rule_history_match")
            layers.append("proposed_rule_shared_identifier_match")
        if proposed_regulations_comment_urls:
            layers.append("proposed_rule_regulations_gov_comment_portal_metadata")
        if comment_metadata_present:
            layers.append("federal_register_exposed_regulations_gov_comment_metadata")
        if complete_comment_records:
            layers.append("regulations_gov_complete_comment_record_metadata")
        elif partial_comment_records:
            layers.append("regulations_gov_partial_comment_record_metadata")
        if final_to_effective_delays:
            layers.append("federal_register_final_effective_date_timing")
        if proposed_to_final_delays:
            layers.append("federal_register_proposed_to_final_timing")
        if court_overlap:
            layers.append("court_review_usc_section_authority_overlap")
            layers.append("scdb_law_minor_usc_section")
        if bill_progression_present:
            layers.append("bill_progression_sample")

        rows.append({
            "bill_id": bill_id,
            "public_law_number": public_law_number,
            "congress": bill.get("congress", ""),
            "bill_type": bill.get("bill_type", ""),
            "bill_number": bill.get("bill_number", ""),
            "policy_area": policy_area,
            "sponsor_bioguide_id": bill.get("sponsor_bioguide_id", ""),
            "sponsor_party": bill.get("sponsor_party", ""),
            "sponsor_state": bill.get("sponsor_state", ""),
            "introduced_date": bill.get("introduced_date", ""),
            "enacted_date": bill.get("enacted_date", "") or law.get("enacted_date", ""),
            "actions_count": bill.get("actions_count", ""),
            "committee_reported": bill.get("committee_reported", ""),
            "floor_considered": bill.get("floor_considered", ""),
            "bill_progression_sample_present": "1" if bill_progression_present else "0",
            "law_revision_text_present": "1" if law else "0",
            "amended": law.get("amended", "0"),
            "reauthorized": law.get("reauthorized", "0"),
            "repealed": law.get("repealed", "0"),
            "expired": law.get("expired", "0"),
            "invalidated": law.get("invalidated", "0"),
            "revision_terms": law.get("revision_terms", ""),
            "statutory_lineage_adjudication_rows": str(len(statutory_adjudication_rows)),
            "statutory_lineage_marker_rows": str(len(statutory_marker_rows)),
            "statutory_lineage_marker_statuses": "; ".join(statutory_marker_statuses),
            "statutory_lineage_marker_strengths": "; ".join(statutory_marker_strengths),
            "statutory_lineage_marker_target_references": "; ".join(statutory_marker_targets),
            "statutory_lineage_marker_pre_anchor_rows": str(
                sum(
                    1 for row in statutory_marker_rows
                    if row.get("pre_section_anchor_status", "").strip() == "section_anchor_found"
                )
            ),
            "statutory_lineage_marker_post_anchor_rows": str(
                sum(
                    1 for row in statutory_marker_rows
                    if row.get("post_section_anchor_status", "").strip() == "section_anchor_found"
                )
            ),
            "statutory_lineage_marker_public_law_context_count": str(
                sum(int_field(row, "post_public_law_context_count") for row in statutory_marker_rows)
            ),
            "statutory_lineage_target_review_packet_rows": str(len(statutory_review_packet_rows)),
            "statutory_lineage_target_review_ready_packet_rows": str(
                len(statutory_review_ready_packet_rows)
            ),
            "statutory_lineage_target_review_packet_statuses": "; ".join(
                statutory_review_packet_statuses
            ),
            "statutory_lineage_target_review_packet_strengths": "; ".join(
                statutory_review_packet_strengths
            ),
            "statutory_lineage_target_review_packet_public_law_context_count": str(
                sum(
                    int_field(row, "post_public_law_context_count")
                    for row in statutory_review_packet_rows
                )
            ),
            "statutory_lineage_target_section_diff_review_rows": str(
                len(statutory_diff_review_rows)
            ),
            "statutory_lineage_target_section_diff_review_statuses": "; ".join(
                statutory_diff_review_statuses
            ),
            "statutory_lineage_target_section_diff_review_relationships": "; ".join(
                statutory_diff_review_relationships
            ),
            "statutory_lineage_source_reviewed_target_section_diff_rows": str(
                len(statutory_source_reviewed_diff_rows)
            ),
            "statutory_lineage_no_target_review_rows": str(len(statutory_no_target_rows)),
            "statutory_lineage_no_target_review_statuses": "; ".join(
                statutory_no_target_statuses
            ),
            "statutory_lineage_no_target_review_dispositions": "; ".join(
                statutory_no_target_dispositions
            ),
            "district_public_opinion_context_rows": str(len(district_rows)),
            "district_public_opinion_unique_keys": str(len(unique_district_keys)),
            "district_ids": "; ".join(district_ids),
            "district_issues": "; ".join(district_issues),
            "district_public_opinion_policy_context_rows": str(len(policy_context_rows)),
            "district_public_opinion_policy_context_unique_keys": str(len(unique_policy_context_keys)),
            "district_public_opinion_policy_areas": "; ".join(policy_context_areas),
            "district_public_opinion_policy_topic_introduced": str(policy_context_topic_counts["topic_introduced"]),
            "district_public_opinion_policy_topic_floor_considered": str(policy_context_topic_counts["topic_floor_considered"]),
            "district_public_opinion_policy_topic_enacted": str(policy_context_topic_counts["topic_enacted"]),
            "campaign_finance_sponsor_policy_context_rows": str(len(campaign_context_rows)),
            "campaign_finance_sponsor_policy_context_transaction_rows": str(sum(int_field(row, "member_context_transaction_rows") for row in campaign_context_rows)),
            "campaign_finance_sponsor_policy_context_unique_candidates": str(len(campaign_context_candidates)),
            "campaign_finance_sponsor_policy_context_bill_ids": "; ".join(campaign_context_bill_ids),
            "campaign_finance_sponsor_policy_context_enacted_bill_ids": "; ".join(campaign_context_enacted_bill_ids),
            "lobbying_policy_context_issue_rows": str(len(lobbying_context_rows)),
            "lobbying_policy_context_activity_rows": str(sum(int_field(row, "lobbying_rows") for row in lobbying_context_rows)),
            "lobbying_policy_context_total_amount": f"{sum(float_field(row, 'total_amount') for row in lobbying_context_rows):.2f}",
            "lobbying_policy_context_bill_contexts": str(sum(int_field(row, "matched_govinfo_bill_count") for row in lobbying_context_rows)),
            "lobbying_policy_context_bill_ids": "; ".join(lobbying_context_bill_ids),
            "lobbying_policy_context_enacted_bill_ids": "; ".join(lobbying_context_enacted_bill_ids),
            "lobbying_policy_context_issues": "; ".join(lobbying_context_issues),
            "lobbying_bill_mention_rows": str(len(lobbying_mention_rows)),
            "lobbying_bill_mention_unique_filings": str(len(lobbying_mention_filings)),
            "lobbying_bill_mention_clients": "; ".join(lobbying_mention_clients),
            "lobbying_bill_mention_registrants": "; ".join(lobbying_mention_registrants),
            "lobbying_bill_mention_activity_issues": "; ".join(lobbying_mention_issues),
            "lobbying_bill_mention_filing_years": "; ".join(lobbying_mention_years),
            "lobbying_bill_mention_document_urls": "; ".join(lobbying_mention_document_urls),
            "lobbying_bill_mention_matched_refs": "; ".join(lobbying_mention_matched_refs),
            "implementation_authority_rule_rows": authority.get("matched_rule_count", "0"),
            "implementation_authority_text_verified_rows": authority.get("text_verified_rule_count", "0"),
            "implementation_authority_document_numbers": authority.get("matched_document_numbers", ""),
            "implementation_authority_publication_dates": authority.get("matched_publication_dates", ""),
            "implementation_authority_agencies": authority.get("agency_names", ""),
            "implementation_authority_cfr_references": authority.get("cfr_references", ""),
            "implementation_authority_usc_citations": authority.get("usc_citations", ""),
            "implementation_history_final_rule_rows": str(len(history_rows)),
            "implementation_history_matched_final_rule_rows": str(len(history_match_rows)),
            "implementation_history_proposed_rule_links": str(proposed_rule_links),
            "implementation_history_proposed_document_numbers": "; ".join(proposed_documents),
            "implementation_history_proposed_comment_close_date_count": str(len(proposed_comment_close_dates)),
            "implementation_history_proposed_comment_close_dates": "; ".join(proposed_comment_close_dates),
            "implementation_history_proposed_regulations_docket_count": str(len(proposed_regulations_docket_ids)),
            "implementation_history_proposed_regulations_docket_ids": "; ".join(proposed_regulations_docket_ids),
            "implementation_history_proposed_comment_portal_count": str(len(proposed_regulations_comment_urls)),
            "implementation_history_proposed_regulations_comment_urls": "; ".join(proposed_regulations_comment_urls),
            "implementation_history_shared_identifiers": "; ".join(shared_identifiers),
            "implementation_comment_metadata_rows": str(len(comment_rows)),
            "implementation_comment_metadata_statuses": "; ".join(comment_statuses),
            "implementation_comment_metadata_final_regulations_docket_count": str(len(comment_final_docket_ids)),
            "implementation_comment_metadata_final_regulations_docket_ids": "; ".join(comment_final_docket_ids),
            "implementation_comment_metadata_final_comment_count_rows": str(len(comment_final_counts)),
            "implementation_comment_metadata_final_positive_comment_count_rows": str(sum(1 for count in comment_final_counts if count > 0)),
            "implementation_comment_metadata_final_comment_count_total": str(sum(comment_final_counts)),
            "implementation_comment_metadata_proposed_detail_fetch_count": str(sum(int_field(row, "proposed_detail_fetch_count") for row in comment_rows)),
            "implementation_comment_metadata_proposed_regulations_docket_count": str(len(comment_proposed_docket_ids)),
            "implementation_comment_metadata_proposed_regulations_docket_ids": "; ".join(comment_proposed_docket_ids),
            "implementation_comment_metadata_proposed_comment_url_count": str(len(comment_proposed_urls)),
            "implementation_comment_metadata_proposed_comment_urls": "; ".join(comment_proposed_urls),
            "implementation_comment_metadata_proposed_comment_count_rows": str(sum(int_field(row, "proposed_comment_count_rows") for row in comment_rows)),
            "implementation_comment_metadata_proposed_positive_comment_count_rows": str(sum(int_field(row, "proposed_positive_comment_count_rows") for row in comment_rows)),
            "implementation_comment_metadata_proposed_comment_count_total": str(sum(int_field(row, "proposed_comment_count_total") for row in comment_rows)),
            "implementation_comment_metadata_proposed_comment_close_date_count": str(len(comment_proposed_close_dates)),
            "implementation_comment_metadata_proposed_comment_close_dates": "; ".join(comment_proposed_close_dates),
            "implementation_comment_record_docket_rows": str(len(comment_record_rows)),
            "implementation_comment_record_complete_docket_rows": str(len(comment_record_complete_rows)),
            "implementation_comment_record_partial_or_blocked_docket_rows": str(len(comment_record_partial_or_blocked_rows)),
            "implementation_comment_record_statuses": "; ".join(comment_record_statuses),
            "implementation_comment_record_docket_ids": "; ".join(comment_record_docket_ids),
            "implementation_comment_record_expected_comment_count_total": str(sum(int_field(row, "expected_comment_count") for row in comment_record_rows)),
            "implementation_comment_record_retrieved_comment_count_total": str(sum(int_field(row, "retrieved_comment_count") for row in comment_record_rows)),
            "implementation_comment_record_api_total_count": str(sum(int_field(row, "api_total_comment_count") for row in comment_record_rows)),
            "implementation_comment_record_ids": "; ".join(comment_record_ids),
            "implementation_history_final_effective_rule_rows": str(sum(1 for row in history_rows if row.get("final_effective_date", "").strip())),
            "implementation_history_final_effective_dates": "; ".join(final_effective_dates),
            "implementation_history_final_to_effective_delay_count": final_to_effective_summary["count"],
            "implementation_history_final_to_effective_delay_min_days": final_to_effective_summary["min"],
            "implementation_history_final_to_effective_delay_median_days": final_to_effective_summary["median"],
            "implementation_history_final_to_effective_delay_max_days": final_to_effective_summary["max"],
            "implementation_history_proposed_to_final_delay_count": proposed_to_final_summary["count"],
            "implementation_history_proposed_to_final_delay_min_days": proposed_to_final_summary["min"],
            "implementation_history_proposed_to_final_delay_median_days": proposed_to_final_summary["median"],
            "implementation_history_proposed_to_final_delay_max_days": proposed_to_final_summary["max"],
            "court_review_overlap_case_rows": str(len(court_case_ids)),
            "court_review_invalidated_case_rows": str(len(court_invalidated_case_ids)),
            "court_review_case_ids": "; ".join(court_case_ids),
            "court_review_usc_sections": "; ".join(court_usc_sections),
            "evidence_layers": "; ".join(layers),
            "missing_links": missing_links(
                district_rows,
                policy_context_rows,
                campaign_context_rows,
                lobbying_context_rows,
                lobbying_mention_rows,
                bill_progression_present,
                authority_match,
                history_match,
                court_overlap,
                codified_lineage_gap=not bool(statutory_no_target_rows),
                complete_comment_records=complete_comment_records,
            ),
            "source_url": bill.get("source_url", "") or law.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    public_law_rows = len(rows)
    revision_rows = sum(1 for row in rows if row["law_revision_text_present"] == "1")
    statutory_adjudication_rows = sum(
        int(row["statutory_lineage_adjudication_rows"] or "0")
        for row in rows
    )
    statutory_marker_bill_rows = sum(
        1 for row in rows
        if int(row["statutory_lineage_marker_rows"] or "0") > 0
    )
    statutory_marker_rows = sum(
        int(row["statutory_lineage_marker_rows"] or "0")
        for row in rows
    )
    statutory_marker_targets = {
        target.strip()
        for row in rows
        for target in row["statutory_lineage_marker_target_references"].split(";")
        if target.strip()
    }
    statutory_marker_context_count = sum(
        int(row["statutory_lineage_marker_public_law_context_count"] or "0")
        for row in rows
    )
    statutory_review_packet_rows = sum(
        int(row["statutory_lineage_target_review_packet_rows"] or "0")
        for row in rows
    )
    statutory_review_ready_packet_rows = sum(
        int(row["statutory_lineage_target_review_ready_packet_rows"] or "0")
        for row in rows
    )
    statutory_review_packet_bill_rows = sum(
        1 for row in rows
        if int(row["statutory_lineage_target_review_packet_rows"] or "0") > 0
    )
    statutory_review_packet_context_count = sum(
        int(row["statutory_lineage_target_review_packet_public_law_context_count"] or "0")
        for row in rows
    )
    statutory_source_reviewed_diff_rows = sum(
        int(row["statutory_lineage_source_reviewed_target_section_diff_rows"] or "0")
        for row in rows
    )
    statutory_diff_review_rows = sum(
        int(row["statutory_lineage_target_section_diff_review_rows"] or "0")
        for row in rows
    )
    statutory_diff_review_bill_rows = sum(
        1 for row in rows
        if int(row["statutory_lineage_target_section_diff_review_rows"] or "0") > 0
    )
    statutory_no_target_review_rows = sum(
        int(row["statutory_lineage_no_target_review_rows"] or "0")
        for row in rows
    )
    statutory_no_target_review_bill_rows = sum(
        1 for row in rows
        if int(row["statutory_lineage_no_target_review_rows"] or "0") > 0
    )
    district_rows = sum(int(row["district_public_opinion_context_rows"]) for row in rows)
    district_bill_rows = sum(1 for row in rows if int(row["district_public_opinion_context_rows"]) > 0)
    policy_context_rows = sum(int(row["district_public_opinion_policy_context_rows"]) for row in rows)
    policy_context_bill_rows = sum(1 for row in rows if int(row["district_public_opinion_policy_context_rows"]) > 0)
    policy_context_areas = {
        area.strip()
        for row in rows
        for area in row["district_public_opinion_policy_areas"].split(";")
        if area.strip()
    }
    campaign_context_bill_rows = sum(1 for row in rows if int(row["campaign_finance_sponsor_policy_context_rows"]) > 0)
    campaign_context_attachments = sum(int(row["campaign_finance_sponsor_policy_context_rows"]) for row in rows)
    campaign_context_transaction_attachments = sum(
        int(row["campaign_finance_sponsor_policy_context_transaction_rows"])
        for row in rows
    )
    campaign_context_bill_ids = {
        value.strip()
        for row in rows
        for value in row["campaign_finance_sponsor_policy_context_bill_ids"].split(";")
        if value.strip()
    }
    campaign_context_enacted_bill_ids = {
        value.strip()
        for row in rows
        for value in row["campaign_finance_sponsor_policy_context_enacted_bill_ids"].split(";")
        if value.strip()
    }
    lobbying_context_bill_rows = sum(1 for row in rows if int(row["lobbying_policy_context_issue_rows"]) > 0)
    lobbying_context_issue_attachments = sum(int(row["lobbying_policy_context_issue_rows"]) for row in rows)
    lobbying_context_activity_attachments = sum(int(row["lobbying_policy_context_activity_rows"]) for row in rows)
    lobbying_context_bill_contexts = sum(int(row["lobbying_policy_context_bill_contexts"]) for row in rows)
    lobbying_context_bill_ids = {
        value.strip()
        for row in rows
        for value in row["lobbying_policy_context_bill_ids"].split(";")
        if value.strip()
    }
    lobbying_context_enacted_bill_ids = {
        value.strip()
        for row in rows
        for value in row["lobbying_policy_context_enacted_bill_ids"].split(";")
        if value.strip()
    }
    lobbying_context_issues = {
        value.strip()
        for row in rows
        for value in row["lobbying_policy_context_issues"].split(";")
        if value.strip()
    }
    lobbying_mention_bill_rows = sum(1 for row in rows if int(row["lobbying_bill_mention_rows"] or "0") > 0)
    lobbying_mention_rows = sum(int(row["lobbying_bill_mention_rows"] or "0") for row in rows)
    lobbying_mention_document_urls = {
        value.strip()
        for row in rows
        for value in row["lobbying_bill_mention_document_urls"].split(";")
        if value.strip()
    }
    lobbying_mention_clients = {
        value.strip()
        for row in rows
        for value in row["lobbying_bill_mention_clients"].split(";")
        if value.strip()
    }
    bill_progression_rows = sum(1 for row in rows if row["bill_progression_sample_present"] == "1")
    authority_rows = sum(1 for row in rows if int(row["implementation_authority_text_verified_rows"] or "0") > 0)
    authority_rule_rows = sum(int(row["implementation_authority_text_verified_rows"] or "0") for row in rows)
    history_rows = sum(1 for row in rows if int(row["implementation_history_matched_final_rule_rows"] or "0") > 0)
    history_final_rule_rows = sum(int(row["implementation_history_matched_final_rule_rows"] or "0") for row in rows)
    history_proposed_links = sum(int(row["implementation_history_proposed_rule_links"] or "0") for row in rows)
    final_effective_rule_rows = sum(int(row["implementation_history_final_effective_rule_rows"] or "0") for row in rows)
    final_to_effective_delays = [
        int(row[field])
        for row in rows
        for field in (
            "implementation_history_final_to_effective_delay_min_days",
            "implementation_history_final_to_effective_delay_median_days",
            "implementation_history_final_to_effective_delay_max_days",
        )
        if row[field].strip() and row[field].strip().lstrip("-").isdigit()
    ]
    final_to_effective_delay_count = sum(
        int(row["implementation_history_final_to_effective_delay_count"] or "0")
        for row in rows
    )
    proposed_to_final_delays = [
        int(row[field])
        for row in rows
        for field in (
            "implementation_history_proposed_to_final_delay_min_days",
            "implementation_history_proposed_to_final_delay_median_days",
            "implementation_history_proposed_to_final_delay_max_days",
        )
        if row[field].strip() and row[field].strip().lstrip("-").isdigit()
    ]
    proposed_to_final_delay_count = sum(
        int(row["implementation_history_proposed_to_final_delay_count"] or "0")
        for row in rows
    )
    court_rows = sum(1 for row in rows if int(row["court_review_overlap_case_rows"] or "0") > 0)
    court_case_links = sum(int(row["court_review_overlap_case_rows"] or "0") for row in rows)
    court_invalidated_links = sum(int(row["court_review_invalidated_case_rows"] or "0") for row in rows)
    court_cases = {
        case_id.strip()
        for row in rows
        for case_id in row["court_review_case_ids"].split(";")
        if case_id.strip()
    }
    court_sections = {
        section.strip()
        for row in rows
        for section in row["court_review_usc_sections"].split(";")
        if section.strip()
    }
    history_proposed_documents = {
        document.strip()
        for row in rows
        for document in row["implementation_history_proposed_document_numbers"].split(";")
        if document.strip()
    }
    history_comment_close_dates = {
        date.strip()
        for row in rows
        for date in row["implementation_history_proposed_comment_close_dates"].split(";")
        if date.strip()
    }
    history_regulations_dockets = {
        docket_id.strip()
        for row in rows
        for docket_id in row["implementation_history_proposed_regulations_docket_ids"].split(";")
        if docket_id.strip()
    }
    history_comment_portals = {
        url.strip()
        for row in rows
        for url in row["implementation_history_proposed_regulations_comment_urls"].split(";")
        if url.strip()
    }
    comment_metadata_rows = sum(1 for row in rows if int(row["implementation_comment_metadata_rows"] or "0") > 0)
    comment_metadata_final_docket_rows = sum(
        1 for row in rows
        if int(row["implementation_comment_metadata_final_regulations_docket_count"] or "0") > 0
    )
    comment_metadata_final_comment_count_rows = sum(
        int(row["implementation_comment_metadata_final_comment_count_rows"] or "0")
        for row in rows
    )
    comment_metadata_final_positive_comment_rows = sum(
        int(row["implementation_comment_metadata_final_positive_comment_count_rows"] or "0")
        for row in rows
    )
    comment_metadata_final_comment_total = sum(
        int(row["implementation_comment_metadata_final_comment_count_total"] or "0")
        for row in rows
    )
    comment_metadata_proposed_dockets = {
        docket.strip()
        for row in rows
        for docket in row["implementation_comment_metadata_proposed_regulations_docket_ids"].split(";")
        if docket.strip()
    }
    comment_metadata_proposed_urls = {
        url.strip()
        for row in rows
        for url in row["implementation_comment_metadata_proposed_comment_urls"].split(";")
        if url.strip()
    }
    comment_metadata_proposed_count_rows = sum(
        int(row["implementation_comment_metadata_proposed_comment_count_rows"] or "0")
        for row in rows
    )
    comment_metadata_proposed_positive_rows = sum(
        int(row["implementation_comment_metadata_proposed_positive_comment_count_rows"] or "0")
        for row in rows
    )
    comment_metadata_proposed_comment_total = sum(
        int(row["implementation_comment_metadata_proposed_comment_count_total"] or "0")
        for row in rows
    )
    comment_record_rows = sum(
        int(row["implementation_comment_record_docket_rows"] or "0")
        for row in rows
    )
    comment_record_complete_rows = sum(
        int(row["implementation_comment_record_complete_docket_rows"] or "0")
        for row in rows
    )
    comment_record_partial_or_blocked_rows = sum(
        int(row["implementation_comment_record_partial_or_blocked_docket_rows"] or "0")
        for row in rows
    )
    comment_record_complete_public_laws = sum(
        1
        for row in rows
        if "regulations_gov_complete_comment_record_metadata" in row["evidence_layers"]
    )
    comment_record_expected_total = sum(
        int(row["implementation_comment_record_expected_comment_count_total"] or "0")
        for row in rows
    )
    comment_record_retrieved_total = sum(
        int(row["implementation_comment_record_retrieved_comment_count_total"] or "0")
        for row in rows
    )
    policy_counts = Counter(row["policy_area"] or "Unclassified" for row in rows)

    lines = [
        "# Bill-Law Evidence Spine",
        "",
        "This report derives a bounded bill/public-law spine from cached local linkage files. It is a join inventory, not validation evidence.",
        "",
        f"- Public-law bill rows with Congress.gov bill/action metadata: {public_law_rows}",
        f"- Rows with law-revision text proxy fields: {revision_rows}",
        f"- Statutory-lineage adjudication rows attached: {statutory_adjudication_rows}",
        f"- Public-law rows with official OLRC post-only public-law marker evidence: {statutory_marker_bill_rows}",
        f"- Official OLRC post-only public-law marker rows attached: {statutory_marker_rows}",
        f"- Unique target references with OLRC marker evidence: {len(statutory_marker_targets)}",
        f"- Bounded OLRC public-law context snippets attached: {statutory_marker_context_count}",
        f"- Public-law rows with statutory-lineage target review packets: {statutory_review_packet_bill_rows}",
        f"- Statutory-lineage target review packet rows attached: {statutory_review_packet_rows}",
        f"- Review-ready target-section packet rows attached: {statutory_review_ready_packet_rows}",
        f"- Target review packet public-law context snippets attached: {statutory_review_packet_context_count}",
        f"- Public-law rows with statutory-lineage target-section diff review: {statutory_diff_review_bill_rows}",
        f"- Statutory-lineage target-section diff review rows attached: {statutory_diff_review_rows}",
        f"- Source-reviewed target-section diff rows attached: {statutory_source_reviewed_diff_rows}",
        f"- Public-law rows with reviewed no-structured-U.S.C.-target dispositions: {statutory_no_target_review_bill_rows}",
        f"- Reviewed no-structured-U.S.C.-target disposition rows attached: {statutory_no_target_review_rows}",
        f"- Rows with sponsor-district public-opinion metadata: {district_bill_rows}",
        f"- Sponsor-district public-opinion context rows attached: {district_rows}",
        f"- Rows with bounded sponsor-district bill policy-area context: {policy_context_bill_rows}",
        f"- Sponsor-district bill policy-area context rows attached: {policy_context_rows}",
        f"- Unique policy areas attached to sponsor-district context: {len(policy_context_areas)}",
        f"- Rows with same-policy campaign-finance sponsor context: {campaign_context_bill_rows}",
        f"- Same-policy campaign-finance sponsor context row attachments: {campaign_context_attachments}",
        f"- Same-policy campaign-finance transaction-row attachments: {campaign_context_transaction_attachments}",
        f"- Unique same-policy campaign-finance context bill IDs attached: {len(campaign_context_bill_ids)}",
        f"- Unique same-policy campaign-finance enacted bill IDs attached: {len(campaign_context_enacted_bill_ids)}",
        f"- Rows with same-policy LDA issue/bill context: {lobbying_context_bill_rows}",
        f"- Same-policy LDA issue-context row attachments: {lobbying_context_issue_attachments}",
        f"- Same-policy LDA activity-row attachments: {lobbying_context_activity_attachments}",
        f"- Same-policy LDA issue-policy bill-context attachments: {lobbying_context_bill_contexts}",
        f"- Unique same-policy LDA context bill IDs attached: {len(lobbying_context_bill_ids)}",
        f"- Unique same-policy LDA enacted bill IDs attached: {len(lobbying_context_enacted_bill_ids)}",
        f"- Unique same-policy LDA issue labels attached: {len(lobbying_context_issues)}",
        f"- Rows with exact official LDA filing-text bill mentions: {lobbying_mention_bill_rows}",
        f"- Exact official LDA filing activity bill mention rows attached: {lobbying_mention_rows}",
        f"- Unique official LDA filing document URLs attached for exact mentions: {len(lobbying_mention_document_urls)}",
        f"- Unique LDA clients attached for exact mentions: {len(lobbying_mention_clients)}",
        f"- Rows with text-verified Federal Register authority matches: {authority_rows}",
        f"- Text-verified Federal Register rule documents attached: {authority_rule_rows}",
        f"- Rows with Federal Register proposed-rule history matches: {history_rows}",
        f"- Authority-matched final-rule rows with proposed-rule histories attached: {history_final_rule_rows}",
        f"- Proposed-rule history links attached: {history_proposed_links}",
        f"- Unique proposed-rule documents attached: {len(history_proposed_documents)}",
        f"- Unique proposed-rule comment-close dates attached: {len(history_comment_close_dates)}",
        f"- Unique proposed-rule Regulations.gov dockets attached: {len(history_regulations_dockets)}",
        f"- Unique proposed-rule Regulations.gov comment portals attached: {len(history_comment_portals)}",
        f"- Public-law rows with authority-chain comment metadata attached: {comment_metadata_rows}",
        f"- Public-law rows with final-rule Regulations.gov docket metadata attached: {comment_metadata_final_docket_rows}",
        f"- Final-rule comments-count rows attached: {comment_metadata_final_comment_count_rows}",
        f"- Final-rule positive comments-count rows attached: {comment_metadata_final_positive_comment_rows}",
        f"- Final-rule comments counted in exposed metadata: {comment_metadata_final_comment_total}",
        f"- Unique proposed-rule Regulations.gov dockets refetched: {len(comment_metadata_proposed_dockets)}",
        f"- Unique proposed-rule comment URLs refetched: {len(comment_metadata_proposed_urls)}",
        f"- Proposed-rule comments-count rows attached: {comment_metadata_proposed_count_rows}",
        f"- Proposed-rule positive comments-count rows attached: {comment_metadata_proposed_positive_rows}",
        f"- Proposed-rule comments counted in exposed metadata: {comment_metadata_proposed_comment_total}",
        f"- Public-law rows with complete Regulations.gov comment-record metadata: {comment_record_complete_public_laws}",
        f"- Regulations.gov public-law/docket comment-record rows attached: {comment_record_rows}",
        f"- Complete public-law/docket comment-record rows attached: {comment_record_complete_rows}",
        f"- Partial, skipped, or blocked public-law/docket comment-record rows attached: {comment_record_partial_or_blocked_rows}",
        f"- Comment records expected from Federal Register metadata in attached dockets: {comment_record_expected_total}",
        f"- Comment record metadata rows retrieved from Regulations.gov: {comment_record_retrieved_total}",
        f"- Authority-matched final-rule rows with final effective dates attached: {final_effective_rule_rows}",
        f"- Final-to-effective delay rows attached: {final_to_effective_delay_count}",
        f"- Final-to-effective delay range attached: {min(final_to_effective_delays) if final_to_effective_delays else '---'} to {max(final_to_effective_delays) if final_to_effective_delays else '---'} days",
        f"- Proposed-to-final timing rows attached: {proposed_to_final_delay_count}",
        f"- Earliest-proposed-to-final delay range attached: {min(proposed_to_final_delays) if proposed_to_final_delays else '---'} to {max(proposed_to_final_delays) if proposed_to_final_delays else '---'} days",
        f"- Rows with SCDB/Federal Register U.S.C.-section court-review overlaps: {court_rows}",
        f"- Court-review overlap case links attached: {court_case_links}",
        f"- Court-review overlap case links coded invalidated by SCDB: {court_invalidated_links}",
        f"- Unique court-review cases attached: {len(court_cases)}",
        f"- Unique court-review U.S.C. sections attached: {len(court_sections)}",
        f"- Rows also present in the bounded bill-progression sample: {bill_progression_rows}",
        "",
        "Claim boundary: this spine records which cached public-law bills currently carry bill-action metadata, revision-text proxy fields, official OLRC post-only public-law marker adjudication, target-section review packets, bounded source-reviewed target-section diff dispositions, reviewed designation-law no-structured-U.S.C.-target dispositions, sponsor-district public-opinion context, bounded sponsor-district bill policy-area context, same-policy campaign-finance sponsor context, same-policy LDA issue/bill context, exact official LDA filing-text bill identifiers, bounded Federal Register authority-search matches, bounded proposed-rule history matches, Federal Register-exposed Regulations.gov docket/comment metadata, bounded complete, partial, or skipped Regulations.gov comment-record metadata, final-rule timing metadata, proposed-to-final timing metadata, and bounded SCDB/Federal Register U.S.C.-section court-review overlaps. It does not provide bill-topic public support, bill-specific campaign-finance or lobbying influence, public-law causal attribution for target-section diffs, complete comment coverage for partial rows, comment text, comment attachments, commenter-identity validation, implementation outcomes, direct case-to-public-law review or invalidation, welfare, causal effects, or model validation.",
        "",
        "Policy-area coverage:",
        "",
        "| Policy area | Rows |",
        "| --- | ---: |",
    ]
    for policy, count in sorted(policy_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {policy} | {count} |")

    lines.extend([
        "",
        "| Bill | Public law | Policy area | Lineage markers | Review packets | Diff review rows | Reviewed diffs | District policy ctx | CF sponsor ctx | LDA issue ctx | LDA activity rows | Exact LDA bill mentions | Authority rules | Proposed links | Comment portals | Comment metadata | Comment records | Final delay median | Proposed-final median | Court cases | Evidence layers | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| `{row['bill_id']}` | `{row['public_law_number']}` | {row['policy_area'] or '---'} | "
            f"{row['statutory_lineage_marker_rows']} | "
            f"{row['statutory_lineage_target_review_ready_packet_rows']} | "
            f"{row['statutory_lineage_target_section_diff_review_rows']} | "
            f"{row['statutory_lineage_source_reviewed_target_section_diff_rows']} | "
            f"{row['district_public_opinion_policy_context_rows']} | "
            f"{row['campaign_finance_sponsor_policy_context_rows']} | "
            f"{row['lobbying_policy_context_issue_rows']} | "
            f"{row['lobbying_policy_context_activity_rows']} | "
            f"{row['lobbying_bill_mention_rows']} | "
            f"{row['implementation_authority_text_verified_rows']} | {row['implementation_history_proposed_rule_links']} | "
            f"{row['implementation_history_proposed_comment_portal_count']} | "
            f"{row['implementation_comment_metadata_rows']} | "
            f"{row['implementation_comment_record_complete_docket_rows']}/{row['implementation_comment_record_docket_rows']} | "
            f"{row['implementation_history_final_to_effective_delay_median_days'] or '---'} | "
            f"{row['implementation_history_proposed_to_final_delay_median_days'] or '---'} | "
            f"{row['court_review_overlap_case_rows']} | "
            f"{row['evidence_layers']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{LAW_REVISION_BILL_LINKAGE} is missing or empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
