#!/usr/bin/env python3
"""Write a registry-backed empirical linkage report.

Raw source-family coverage is not the same as linked validation evidence. This
report measures the current joins that connect source families to bills, topics,
statutes, agencies, courts, sponsors, committees, or public-opinion signals.
"""

from __future__ import annotations

import csv
import json
import re
from collections.abc import Iterable
from pathlib import Path


REGISTRY = Path("data/validation/source-registry.csv")
VOTEVIEW_MEMBER_CONTEXT = Path("data/validation/raw/voteview_member_context.csv")
VOTEVIEW_BILL_LINKAGE = Path("data/validation/raw/voteview_bill_linkage.csv")
GOVINFO_BILLSTATUS_LINKAGE = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
SPONSOR_BILL_LINKAGE = Path("data/validation/raw/sponsor_bill_linkage.csv")
COMPARATIVE_INSTITUTION_LINKAGE = Path("data/validation/raw/comparative_institution_linkage.csv")
CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
CAMPAIGN_FINANCE_MEMBER_CONTEXT = Path("data/validation/raw/campaign_finance_member_context.csv")
CAMPAIGN_FINANCE_ISSUE_CONTEXT = Path("data/validation/raw/campaign_finance_issue_context.csv")
CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT = Path("reports/campaign-finance-sponsor-bill-context.csv")
DISTRICT_PUBLIC_OPINION = Path("data/validation/raw/district_public_opinion.csv")
DISTRICT_PUBLIC_OPINION_LINKAGE = Path("data/validation/raw/district_public_opinion_linkage.csv")
DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT = Path("data/validation/raw/district_public_opinion_policy_context.csv")
DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS = Path(
    "reports/district-public-opinion-bill-topic-readiness.csv"
)
DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS = Path(
    "reports/district-public-opinion-source-packets.csv"
)
DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS = Path(
    "reports/district-public-opinion-census-denominators.csv"
)
DISTRICT_PUBLIC_OPINION_ACS_CONTEXT = Path(
    "reports/district-public-opinion-acs-context.csv"
)
DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK = Path(
    "reports/district-public-opinion-survey-source-crosswalk.csv"
)
DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW = Path(
    "reports/district-public-opinion-survey-item-proxy-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-candidate-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-response-distribution-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-codebook-direction-review.csv"
)
DISTRICT_PUBLIC_OPINION_BILL_ITEM_ALIGNMENT_REVIEW = Path(
    "reports/district-public-opinion-bill-item-alignment-review.csv"
)
DISTRICT_PUBLIC_OPINION_BILL_TOPIC_SUPPORT = Path(
    "reports/district-public-opinion-bill-topic-support.csv"
)
COURT_LAW_LINKAGE = Path("data/validation/raw/court_law_linkage.csv")
RULEMAKING_IMPLEMENTATION_LINKAGE = Path("data/validation/raw/rulemaking_implementation_linkage.csv")
RULEMAKING_AUTHORITY_LINKAGE = Path("data/validation/raw/rulemaking_authority_linkage.csv")
RULEMAKING_HISTORY_LINKAGE = Path("data/validation/raw/rulemaking_history_linkage.csv")
RULEMAKING_COMMENT_RECORDS = Path("data/validation/raw/rulemaking_comment_records.csv")
RULEMAKING_COMMENT_TEXT_REVIEW = Path("data/validation/raw/rulemaking_comment_text_review.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW = Path(
    "reports/statutory-lineage-target-section-diff-review.csv"
)
STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE = Path(
    "reports/statutory-lineage-target-lifecycle-bridge.csv"
)
STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE = Path(
    "reports/statutory-lineage-complete-lineage-expansion-queue.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE = Path(
    "reports/statutory-lineage-target-packet-expansion-queue.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE = Path(
    "reports/statutory-lineage-target-packet-source-gap-queue.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW = Path(
    "reports/statutory-lineage-target-packet-source-gap-review.csv"
)
STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES = Path(
    "reports/statutory-lineage-target-reference-resolution-candidates.csv"
)
STATUTORY_LINEAGE_NO_TARGET_REVIEW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
LOBBYING_ISSUE_LINKAGE = Path("data/validation/raw/lobbying_issue_linkage.csv")
LOBBYING_BILL_POLICY_CONTEXT = Path("reports/lobbying-bill-policy-context.csv")
LOBBYING_BILL_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW = Path(
    "reports/lobbying-bill-medium-directional-packet-review.csv"
)
LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW = Path(
    "reports/lobbying-bill-medium-position-activity-packet-review.csv"
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
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT = Path(
    "reports/bill-finance-lobbying-committee-action-context.csv"
)
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-committee-action-source-review.csv"
)
BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-roll-call-source-review.csv"
)
BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW = Path(
    "reports/bill-finance-lobbying-member-vote-target-review.csv"
)
BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE = Path(
    "reports/bill-finance-lobbying-source-acquisition-queue.csv"
)
OUT_CSV = Path("reports/empirical-linkage-report.csv")
OUT_MD = Path("reports/empirical-linkage-report.md")

LINKED_STATUSES = {"linked", "metadata linked", "partially linked"}
STATUS_ORDER = {
    "linked": 0,
    "metadata linked": 1,
    "partially linked": 2,
    "not independently linked": 3,
    "not linked": 4,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def normalize(value: str | None) -> str:
    return (value or "").strip().casefold()


def plural(count: int, singular: str, plural_value: str) -> str:
    return singular if count == 1 else plural_value


def normalized_values(rows: Iterable[dict[str, str]], field: str) -> set[str]:
    return {normalize(row.get(field)) for row in rows if normalize(row.get(field))}


def count_linked_rows(rows: list[dict[str, str]], field: str, target_values: set[str]) -> int:
    return sum(1 for row in rows if normalize(row.get(field)) in target_values)


def raw_rows(raw_path: str) -> list[dict[str, str]]:
    if not raw_path:
        return []
    return read_csv(Path(raw_path))


def voteview_member_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        normalize(row.get("congress")),
        normalize(row.get("chamber")),
        normalize(row.get("icpsr")),
    )


def metadata_linked_voteview_member_keys() -> set[tuple[str, str, str]]:
    return {
        voteview_member_key(row)
        for row in read_csv(VOTEVIEW_MEMBER_CONTEXT)
        if all(voteview_member_key(row))
        and normalize(row.get("linkage_status")) == "voteview_member_metadata"
        and normalize(row.get("bioguide_id"))
    }


def count_linked_voteview_rows(rows: list[dict[str, str]]) -> int:
    linked_keys = metadata_linked_voteview_member_keys()
    if not linked_keys:
        return 0
    return sum(1 for row in rows if voteview_member_key(row) in linked_keys)


def voteview_bill_linkage_summary() -> tuple[int, int, int, int]:
    rows = read_csv(VOTEVIEW_BILL_LINKAGE)
    bill_rows = [row for row in rows if normalize(row.get("bill_id"))]
    bill_progression_rows = [
        row for row in rows
        if normalize(row.get("bill_match_status")) == "bill_progression_metadata"
    ]
    bill_member_vote_rows = 0
    bill_progression_member_vote_rows = 0
    for row in bill_rows:
        try:
            bill_member_vote_rows += int(row.get("member_vote_rows") or "0")
        except ValueError:
            continue
    for row in bill_progression_rows:
        try:
            bill_progression_member_vote_rows += int(row.get("member_vote_rows") or "0")
        except ValueError:
            continue
    return (
        len(bill_rows),
        bill_member_vote_rows,
        len(bill_progression_rows),
        bill_progression_member_vote_rows,
    )


def govinfo_billstatus_linkage_summary() -> tuple[int, int, int]:
    rows = read_csv(GOVINFO_BILLSTATUS_LINKAGE)
    metadata_rows = [
        row for row in rows
        if normalize(row.get("linkage_status")) == "govinfo_billstatus_metadata"
    ]
    action_aligned_rows = [
        row for row in metadata_rows
        if normalize(row.get("action_alignment_status")) == "aligned"
    ]
    policy_aligned_rows = [
        row for row in metadata_rows
        if normalize(row.get("policy_area_alignment_status")) == "aligned"
    ]
    return len(metadata_rows), len(action_aligned_rows), len(policy_aligned_rows)


def sponsor_bill_linkage_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(SPONSOR_BILL_LINKAGE)
    matched = [
        row for row in rows
        if normalize(row.get("linkage_status")) == "sponsor_bill_metadata"
    ]
    bill_ids = {
        normalize(bill_id)
        for row in matched
        for bill_id in row.get("matched_bill_ids", "").split(";")
        if normalize(bill_id)
    }
    public_laws = {
        normalize(public_law)
        for row in matched
        for public_law in row.get("matched_public_law_numbers", "").split(";")
        if normalize(public_law)
    }
    attached_bill_links = 0
    attached_enacted_links = 0
    for row in matched:
        try:
            attached_bill_links += int(row.get("matched_govinfo_bill_count") or "0")
            attached_enacted_links += int(row.get("matched_govinfo_enacted_count") or "0")
        except ValueError:
            continue
    return len(matched), len(bill_ids), attached_bill_links, attached_enacted_links, len(public_laws)


def comparative_institution_linkage_summary() -> tuple[int, int, int, int]:
    rows = read_csv(COMPARATIVE_INSTITUTION_LINKAGE)
    matched = [
        row for row in rows
        if normalize(row.get("linkage_status")) == "comparative_institution_metadata"
    ]
    countries = {
        normalize(row.get("iso3"))
        for row in matched
        if normalize(row.get("iso3"))
    }
    scenario_keys = {
        normalize(key)
        for row in matched
        for key in row.get("matched_scenario_keys", "").split(";")
        if normalize(key)
    }
    bicameral_rows = sum(1 for row in matched if normalize(row.get("chamber_anchor")) == "bicameral")
    return len(matched), len(countries), len(scenario_keys), bicameral_rows


def share(linked_rows: int, total_rows: int) -> str:
    if total_rows <= 0:
        return "0.000"
    return f"{linked_rows / total_rows:.3f}"


def status_for(linked_rows: int, total_rows: int, unlinked_status: str = "not linked") -> str:
    if total_rows > 0 and linked_rows == total_rows:
        return "linked"
    if linked_rows > 0:
        return "partially linked"
    return unlinked_status


def metadata_linked_recipients() -> set[str]:
    rows = read_csv(CAMPAIGN_FINANCE_LINKAGE)
    return {
        normalize(row.get("recipient"))
        for row in rows
        if normalize(row.get("recipient")) and normalize(row.get("linkage_status")) != "unmatched"
    }


def normalized_house_district(row: dict[str, str]) -> str:
    if normalize(row.get("candidate_office")) != "house":
        return ""
    state = (row.get("candidate_office_state") or "").strip().upper()
    district = (row.get("candidate_office_district") or "").strip()
    if not state or state == "US" or not district:
        return ""
    try:
        district_number = int(district)
    except ValueError:
        return ""
    if district_number <= 0:
        return ""
    return f"{state}-{district_number:02d}"


def campaign_finance_house_district_summary() -> tuple[int, int, int]:
    district_ids = {
        row.get("district_id", "").strip()
        for row in read_csv(DISTRICT_PUBLIC_OPINION)
        if row.get("district_id", "").strip()
    }
    house_rows = [
        row for row in read_csv(CAMPAIGN_FINANCE_LINKAGE)
        if normalized_house_district(row) in district_ids
    ]
    transaction_rows = 0
    for row in house_rows:
        try:
            transaction_rows += int(row.get("linked_transaction_rows") or row.get("transaction_rows") or "0")
        except ValueError:
            continue
    return len(house_rows), transaction_rows, len({normalized_house_district(row) for row in house_rows})


def campaign_finance_member_context_summary() -> tuple[int, int, int]:
    rows = read_csv(CAMPAIGN_FINANCE_MEMBER_CONTEXT)
    matched = [
        row for row in rows
        if normalize(row.get("member_context_status")) == "candidate_voteview_member_context"
    ]
    transaction_rows = 0
    for row in matched:
        try:
            transaction_rows += int(row.get("member_context_transaction_rows") or "0")
        except ValueError:
            continue
    return (
        len(matched),
        transaction_rows,
        len({normalize(row.get("bioguide_id")) for row in matched if normalize(row.get("bioguide_id"))}),
    )


def campaign_finance_issue_context_summary() -> tuple[int, int, int, float]:
    rows = read_csv(CAMPAIGN_FINANCE_ISSUE_CONTEXT)
    mapped = [
        row for row in rows
        if normalize(row.get("issue_context_status")) == "campaign_finance_issue_topic_context"
    ]
    mapped_amount = 0.0
    for row in mapped:
        try:
            mapped_amount += float(row.get("amount") or "0")
        except ValueError:
            continue
    return (
        len(mapped),
        len({normalize(row.get("mapped_topic")) for row in mapped if normalize(row.get("mapped_topic"))}),
        len({normalize(row.get("recipient")) for row in mapped if normalize(row.get("recipient"))}),
        mapped_amount,
    )


def campaign_finance_sponsor_bill_context_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT)
    matched = [
        row for row in rows
        if normalize(row.get("sponsor_bill_context_status")) == "candidate_sponsored_bill_context"
    ]
    transaction_rows = 0
    for row in matched:
        try:
            transaction_rows += int(row.get("member_context_transaction_rows") or "0")
        except ValueError:
            continue
    bill_ids = {
        normalize(bill_id)
        for row in matched
        for bill_id in row.get("matched_bill_ids", "").split(";")
        if normalize(bill_id)
    }
    enacted_bill_ids = {
        normalize(bill_id)
        for row in matched
        for bill_id in row.get("matched_enacted_bill_ids", "").split(";")
        if normalize(bill_id)
    }
    return (
        len(matched),
        transaction_rows,
        len({normalize(row.get("bioguide_id")) for row in matched if normalize(row.get("bioguide_id"))}),
        len(bill_ids),
        len(enacted_bill_ids),
    )


def statutory_target_section_diff_review_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW)
    source_reviewed = [
        row for row in rows
        if normalize(row.get("source_reviewed_target_section_diff")) == "1"
    ]
    no_exact_target = [
        row for row in rows
        if normalize(row.get("review_status")) == "reviewed_related_section_context_no_exact_target_diff"
    ]
    unresolved = [
        row for row in rows
        if normalize(row.get("source_reviewed_target_section_diff")) != "1"
        and normalize(row.get("review_status")) != "reviewed_related_section_context_no_exact_target_diff"
    ]
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in rows
        if normalize(row.get("public_law_number"))
    }
    return len(rows), len(source_reviewed), len(no_exact_target), len(unresolved), len(public_laws)


def statutory_no_target_review_summary() -> tuple[int, int]:
    rows = read_csv(STATUTORY_LINEAGE_NO_TARGET_REVIEW)
    source_reviewed = [
        row for row in rows
        if normalize(row.get("source_reviewed_no_structured_usc_target")) == "1"
    ]
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in source_reviewed
        if normalize(row.get("public_law_number"))
    }
    return len(source_reviewed), len(public_laws)


def statutory_target_lifecycle_bridge_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE)
    raw_base_rows = [
        row for row in rows
        if normalize(row.get("raw_scdb_target_base_section_overlap")) == "1"
    ]
    raw_exact_rows = [
        row for row in rows
        if normalize(row.get("raw_scdb_target_reference_overlap")) == "1"
    ]
    raw_case_ids = {
        normalize(case_id)
        for row in raw_base_rows
        for case_id in row.get("raw_scdb_target_base_section_case_ids", "").split(";")
        if normalize(case_id)
    }
    post_enactment_attachments = 0
    for row in rows:
        try:
            post_enactment_attachments += int(
                row.get("raw_scdb_target_base_section_post_enactment_case_count") or "0"
            )
        except ValueError:
            continue
    return (
        len(rows),
        len(raw_base_rows),
        len(raw_exact_rows),
        len(raw_case_ids),
        post_enactment_attachments,
    )


def statutory_complete_lineage_expansion_queue_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE)
    active_rows = [
        row for row in rows
        if normalize(row.get("complete_lineage_expansion_status"))
        != "reviewed_no_structured_usc_target_no_complete_lineage_expansion"
    ]
    no_target_rows = [
        row for row in rows
        if normalize(row.get("complete_lineage_expansion_status"))
        == "reviewed_no_structured_usc_target_no_complete_lineage_expansion"
    ]
    candidate_expansion_rows = [
        row for row in rows
        if normalize(row.get("complete_lineage_expansion_status"))
        == "source_reviewed_target_diff_attribution_reviewed_candidate_expansion_open"
    ]
    final_audit_rows = [
        row for row in rows
        if normalize(row.get("complete_lineage_expansion_status"))
        == "source_reviewed_target_diff_attribution_reviewed_complete_lineage_audit_open"
    ]

    def total(field: str) -> int:
        result = 0
        for row in rows:
            try:
                result += int(row.get(field) or "0")
            except ValueError:
                continue
        return result

    return (
        len(rows),
        len(active_rows),
        len(candidate_expansion_rows),
        len(final_audit_rows),
        len(no_target_rows),
        total("source_scan_target_candidate_count"),
        total("source_candidate_count_minus_triage_rows"),
        total("triage_to_packet_gap_rows"),
    )


def statutory_target_packet_expansion_queue_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE)
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in rows
        if normalize(row.get("public_law_number"))
    }
    note_review_rows = [
        row for row in rows
        if normalize(row.get("codification_review_status")) == "needs_olrc_us_code_note_review"
    ]
    title_only_rows = [
        row for row in rows
        if normalize(row.get("codification_review_status")) == "title_only_needs_manual_target"
    ]
    incomplete_rows = [
        row for row in rows
        if normalize(row.get("codification_review_status"))
        == "incomplete_reference_fragment_needs_manual_review"
    ]
    return len(rows), len(public_laws), len(note_review_rows), len(title_only_rows), len(incomplete_rows)


def statutory_target_packet_source_gap_queue_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE)
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in rows
        if normalize(row.get("public_law_number"))
    }
    current_no_marker_rows = [
        row for row in rows
        if normalize(row.get("source_gap_status"))
        == "current_olrc_page_fetched_without_public_law_marker_blocks_automated_packet"
    ]
    current_marker_rows = [
        row for row in rows
        if normalize(row.get("source_gap_status"))
        == "current_olrc_page_mentions_public_law_but_downstream_packet_absent"
    ]
    title_only_rows = [
        row for row in rows
        if normalize(row.get("source_gap_status"))
        == "title_only_reference_needs_section_resolution_before_packet"
    ]
    incomplete_rows = [
        row for row in rows
        if normalize(row.get("source_gap_status"))
        == "incomplete_or_nonsection_reference_needs_manual_resolution_before_packet"
    ]
    manual_review_rows = [
        row for row in rows
        if normalize(row.get("source_gap_status"))
        == "current_olrc_scan_status_needs_manual_source_gap_review"
    ]
    downstream_present_rows = [
        row for row in rows
        if normalize(row.get("historical_scan_present")) == "1"
        or normalize(row.get("annual_text_diff_present")) == "1"
        or normalize(row.get("adjudication_present")) == "1"
        or normalize(row.get("target_review_packet_present")) == "1"
    ]
    return (
        len(rows),
        len(public_laws),
        len(current_no_marker_rows),
        len(current_marker_rows),
        len(title_only_rows),
        len(incomplete_rows),
        len(manual_review_rows),
        len(downstream_present_rows),
    )


def statutory_target_packet_source_gap_review_summary() -> tuple[int, int, int, int, int, int]:
    if not STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW.exists():
        return 0, 0, 0, 0, 0, 0
    rows = read_csv(STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW)
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in rows
        if normalize(row.get("public_law_number"))
    }
    temporary_rows = [
        row for row in rows
        if normalize(row.get("review_status")) == "reviewed_temporary_override_no_packet"
    ]
    appropriation_rows = [
        row for row in rows
        if normalize(row.get("review_status"))
        == "reviewed_appropriation_authority_reference_no_packet"
    ]
    cross_reference_rows = [
        row for row in rows
        if normalize(row.get("review_status")) == "reviewed_cross_reference_only_no_packet"
    ]
    table_reference_rows = [
        row for row in rows
        if normalize(row.get("review_status")) == "reviewed_table_or_prec_reference_no_packet"
    ]
    return (
        len(rows),
        len(public_laws),
        len(temporary_rows),
        len(appropriation_rows),
        len(cross_reference_rows),
        len(table_reference_rows),
    )


def statutory_target_reference_resolution_candidate_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES)
    public_laws = {
        normalize(row.get("public_law_number"))
        for row in rows
        if normalize(row.get("public_law_number"))
    }
    rows_with_candidates = 0
    candidate_references = 0
    for row in rows:
        try:
            count = int(row.get("candidate_reference_count") or "0")
        except ValueError:
            count = 0
        candidate_references += count
        if count > 0:
            rows_with_candidates += 1
    return (
        len(rows),
        len(public_laws),
        rows_with_candidates,
        candidate_references,
        len(rows) - rows_with_candidates,
    )


def linked_lobbying_issues() -> set[str]:
    return {
        normalize(row.get("lobbying_issue"))
        for row in read_csv(LOBBYING_ISSUE_LINKAGE)
        if normalize(row.get("lobbying_issue"))
        and normalize(row.get("topic"))
        and normalize(row.get("linkage_status")) == "issue_topic_crosswalk"
    }


def lobbying_issue_linkage_summary() -> tuple[int, int]:
    linked_issues = linked_lobbying_issues()
    rows = read_csv(LOBBYING_ISSUE_LINKAGE)
    linked_rows = 0
    for row in rows:
        if normalize(row.get("lobbying_issue")) not in linked_issues:
            continue
        try:
            linked_rows += int(row.get("lobbying_rows") or "0")
        except ValueError:
            continue
    return len(linked_issues), linked_rows


def lobbying_bill_policy_context_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(LOBBYING_BILL_POLICY_CONTEXT)
    matched = [
        row for row in rows
        if normalize(row.get("policy_context_status")) == "lobbying_issue_bill_policy_context"
    ]
    lobbying_rows = 0
    issue_bill_contexts = 0
    bill_ids: set[str] = set()
    enacted_bill_ids: set[str] = set()
    for row in matched:
        try:
            lobbying_rows += int(row.get("lobbying_rows") or "0")
            issue_bill_contexts += int(row.get("matched_govinfo_bill_count") or "0")
        except ValueError:
            continue
        bill_ids.update(
            normalize(bill_id)
            for bill_id in row.get("matched_bill_ids", "").split(";")
            if normalize(bill_id)
        )
        enacted_bill_ids.update(
            normalize(bill_id)
            for bill_id in row.get("matched_enacted_bill_ids", "").split(";")
            if normalize(bill_id)
        )
    return len(matched), lobbying_rows, issue_bill_contexts, len(bill_ids), len(enacted_bill_ids)


def lobbying_bill_mention_summary() -> tuple[int, int, int, int]:
    rows = [
        row for row in read_csv(LOBBYING_BILL_MENTIONS)
        if normalize(row.get("bill_id")) and row.get("exact_current_bill_match", "").strip() == "1"
    ]
    bill_ids = {normalize(row.get("bill_id")) for row in rows if normalize(row.get("bill_id"))}
    filing_ids = {
        normalize(row.get("filing_uuid"))
        for row in rows
        if normalize(row.get("filing_uuid"))
    }
    clients = {
        normalize(row.get("client_name"))
        for row in rows
        if normalize(row.get("client_name"))
    }
    return len(rows), len(bill_ids), len(filing_ids), len(clients)


def lobbying_bill_action_metadata_summary() -> tuple[int, int, int, int, int]:
    mentioned_bill_ids = {
        normalize(row.get("bill_id"))
        for row in read_csv(LOBBYING_BILL_MENTIONS)
        if normalize(row.get("bill_id")) and row.get("exact_current_bill_match", "").strip() == "1"
    }
    law_by_bill = {
        normalize(row.get("bill_id")): row
        for row in read_csv(LAW_REVISION_BILL_LINKAGE)
        if normalize(row.get("bill_id"))
    }
    matched_law_rows = [
        law_by_bill[bill_id]
        for bill_id in mentioned_bill_ids
        if bill_id in law_by_bill
    ]
    sponsor_rows = sum(1 for row in matched_law_rows if normalize(row.get("sponsor_bioguide_id")))
    committee_reported_rows = sum(1 for row in matched_law_rows if normalize(row.get("committee_reported")) == "1")
    floor_rows = sum(1 for row in matched_law_rows if normalize(row.get("floor_considered")) == "1")
    enacted_rows = sum(1 for row in matched_law_rows if normalize(row.get("enacted")) == "1")
    return len(matched_law_rows), sponsor_rows, committee_reported_rows, floor_rows, enacted_rows


LDA_SUPPORT_PATTERNS = [
    re.compile(r"\bin support of\b", re.IGNORECASE),
    re.compile(r"\bsupport for\b", re.IGNORECASE),
    re.compile(r"\bsupporting\b", re.IGNORECASE),
    re.compile(r"\bsupport passage\b", re.IGNORECASE),
    re.compile(
        r"\bsupports?\s+(?:the\s+)?(?:bill|legislation|reauthorization|"
        r"passage|provisions|funding|authorized|appropriations|research|"
        r"addressing|codification)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\badvocat(?:e|ed|ing)\s+for\b", re.IGNORECASE),
]

LDA_OPPOSITION_PATTERNS = [
    re.compile(r"\boppos(?:e|es|ed|ing)\b", re.IGNORECASE),
    re.compile(r"\bopposition to\b", re.IGNORECASE),
    re.compile(r"\bagainst\s+(?:passage|the bill|legislation)\b", re.IGNORECASE),
    re.compile(r"\bblock(?:ing)?\s+(?:passage|the bill|legislation)\b", re.IGNORECASE),
]

LDA_POSITION_PATTERNS = [
    re.compile(r"\bposition on\b", re.IGNORECASE),
    re.compile(r"\ball provisions\b", re.IGNORECASE),
    re.compile(r"\bissues? (?:and discussions? )?related to\b", re.IGNORECASE),
    re.compile(r"\brelated to\b", re.IGNORECASE),
    re.compile(r"\blobbied (?:for|on)\b", re.IGNORECASE),
    re.compile(r"\bmonitor(?:ed|ing)?\b", re.IGNORECASE),
    re.compile(r"\bregarding\b", re.IGNORECASE),
]


def lda_bill_reference_pattern(bill_id: str) -> re.Pattern[str]:
    parts = bill_id.split("-")
    if len(parts) < 3:
        return re.compile(re.escape(bill_id), re.IGNORECASE)
    bill_type = parts[1].lower()
    number = re.escape(parts[2])
    if bill_type == "hr":
        pattern = rf"(?<![A-Za-z0-9])(?:H\.?\s*R\.?|HR|H R)\s*\.?\s*{number}(?!\d)"
    elif bill_type == "s":
        pattern = rf"(?<![A-Za-z0-9])S\.?\s*{number}(?!\d)"
    else:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(bill_type)}\.?\s*{number}(?!\d)"
    return re.compile(pattern, re.IGNORECASE)


def lda_bill_reference_context(description: str, bill_id: str) -> tuple[str, bool]:
    text = " ".join((description or "").split())
    match = lda_bill_reference_pattern(bill_id).search(text)
    if not match:
        return text[:360], False
    start = max(0, match.start() - 170)
    end = min(len(text), match.end() + 170)
    return text[start:end].strip(), True


def has_pattern(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def exact_lobbying_bill_mentions() -> list[dict[str, str]]:
    return [
        row for row in read_csv(LOBBYING_BILL_MENTIONS)
        if normalize(row.get("bill_id")) and row.get("exact_current_bill_match", "").strip() == "1"
    ]


def lda_text_status(row: dict[str, str]) -> tuple[str, bool, str]:
    context, located = lda_bill_reference_context(row.get("activity_description", ""), row.get("bill_id", ""))
    if not located:
        return "matched_reference_not_located_in_stored_activity_text", False, context
    has_support_signal = has_pattern(context, LDA_SUPPORT_PATTERNS)
    has_opposition_signal = has_pattern(context, LDA_OPPOSITION_PATTERNS)
    has_position_signal = has_pattern(context, LDA_POSITION_PATTERNS)
    if has_support_signal and has_opposition_signal:
        return "exact_bill_text_with_mixed_support_opposition_signal", True, context
    if has_support_signal:
        return "exact_bill_text_with_explicit_support_signal", True, context
    if has_opposition_signal:
        return "exact_bill_text_with_explicit_opposition_signal", True, context
    if has_position_signal:
        return "exact_bill_text_with_position_or_activity_signal", True, context
    return "exact_bill_text_bill_list_or_title_only", True, context


def possible_member_or_committee_reference(context: str) -> bool:
    if re.search(r"\b(?:committee|subcommittee|chair(?:man|woman)?|ranking member)\b", context, re.IGNORECASE):
        return True
    if re.search(r"\b(?:rep\.|representative|senator)\s+[A-Z][A-Za-z'-]+", context):
        return True
    return bool(re.search(r"\bsen\.\s+[A-Z][A-Za-z'-]+", context))


def lobbying_bill_text_signal_summary() -> tuple[int, int, int, int, int, int, int]:
    visible_reference_rows = 0
    refetch_rows = 0
    support_rows = 0
    opposition_rows = 0
    mixed_rows = 0
    position_rows = 0
    list_only_rows = 0
    for row in exact_lobbying_bill_mentions():
        status, located, _context = lda_text_status(row)
        if not located:
            refetch_rows += 1
        elif status == "exact_bill_text_with_explicit_support_signal":
            visible_reference_rows += 1
            support_rows += 1
        elif status == "exact_bill_text_with_explicit_opposition_signal":
            visible_reference_rows += 1
            opposition_rows += 1
        elif status == "exact_bill_text_with_mixed_support_opposition_signal":
            visible_reference_rows += 1
            mixed_rows += 1
        elif status == "exact_bill_text_with_position_or_activity_signal":
            visible_reference_rows += 1
            position_rows += 1
        elif status == "exact_bill_text_bill_list_or_title_only":
            visible_reference_rows += 1
            list_only_rows += 1
    return (
        visible_reference_rows,
        refetch_rows,
        support_rows,
        opposition_rows,
        mixed_rows,
        position_rows,
        list_only_rows,
    )


def lobbying_bill_disposition_review_summary() -> tuple[int, int, int, int]:
    manual_rows = 0
    high_rows = 0
    medium_rows = 0
    low_rows = 0
    for row in exact_lobbying_bill_mentions():
        status, _located, context = lda_text_status(row)
        has_possible_target = possible_member_or_committee_reference(context)
        if status == "exact_bill_text_with_mixed_support_opposition_signal" or has_possible_target:
            high_rows += 1
            manual_rows += 1
        elif status in {
            "exact_bill_text_with_explicit_support_signal",
            "exact_bill_text_with_explicit_opposition_signal",
            "exact_bill_text_with_position_or_activity_signal",
        }:
            medium_rows += 1
            manual_rows += 1
        else:
            low_rows += 1
    return manual_rows, high_rows, medium_rows, low_rows


def lobbying_bill_medium_directional_review_summary() -> tuple[int, int, int, int, int, int]:
    rows = read_csv(LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW)
    support_statuses = {
        "reviewed_current_bill_support",
        "reviewed_current_bill_support_with_opposition_signal_correction",
    }
    downgraded_statuses = {
        "reviewed_direction_signal_on_other_measure",
        "reviewed_current_bill_monitoring_only_with_related_opposition",
    }
    source_rows = 0
    support_packets = 0
    opposition_packets = 0
    downgraded_packets = 0
    corrected_packets = 0
    for row in rows:
        status = row.get("manual_packet_disposition_status", "").strip()
        try:
            source_rows += int(row.get("rows_represented") or "0")
        except ValueError:
            continue
        if status in support_statuses:
            support_packets += 1
        if status == "reviewed_current_bill_opposition":
            opposition_packets += 1
        if status in downgraded_statuses:
            downgraded_packets += 1
        if status == "reviewed_current_bill_support_with_opposition_signal_correction":
            corrected_packets += 1
    return len(rows), source_rows, support_packets, opposition_packets, downgraded_packets, corrected_packets


def lobbying_bill_medium_position_activity_review_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW)
    source_rows = 0
    issue_packets = 0
    monitoring_packets = 0
    all_provisions_packets = 0
    position_packets = 0
    opposition_packets = 0
    generic_congress_packets = 0
    for row in rows:
        status = row.get("manual_activity_disposition_status", "").strip()
        try:
            source_rows += int(row.get("rows_represented") or "0")
        except ValueError:
            continue
        if status == "reviewed_current_bill_issue_or_provision_activity_without_direction":
            issue_packets += 1
        if status == "reviewed_current_bill_monitoring_or_analysis_only":
            monitoring_packets += 1
        if status == "reviewed_current_bill_all_provisions_without_direction":
            all_provisions_packets += 1
        if status == "reviewed_current_bill_position_represented_without_direction":
            position_packets += 1
        if status == "reviewed_current_bill_opposition_from_activity_text":
            opposition_packets += 1
        if row.get("manual_target_status", "").strip() == "reviewed_generic_congress_text_reference":
            generic_congress_packets += 1
    return (
        len(rows),
        source_rows,
        issue_packets,
        monitoring_packets,
        all_provisions_packets,
        position_packets,
        opposition_packets,
        generic_congress_packets,
    )


def bill_finance_lobbying_local_context_review_summary() -> tuple[int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW)
    campaign_no_match_rows = [
        row for row in rows
        if normalize(row.get("manual_campaign_context_status"))
        == "reviewed_same_policy_campaign_context_no_current_bill_match"
    ]
    lobbying_no_match_rows = [
        row for row in rows
        if normalize(row.get("manual_lobbying_context_status"))
        == "reviewed_same_policy_lobbying_context_no_current_bill_match"
    ]
    local_exact_rows = [
        row for row in rows
        if normalize(row.get("campaign_finance_current_bill_exact_match")) == "yes"
        or normalize(row.get("lobbying_current_bill_exact_match")) == "yes"
    ]
    external_expansion_rows = [
        row for row in rows
        if normalize(row.get("manual_next_source_expansion")).startswith("external_current_bill_")
    ]
    no_outcome_rows = [
        row for row in rows
        if normalize(row.get("manual_outcome_link_status")) == "no_outcome_influence_evidence"
    ]
    return (
        len(rows),
        len(campaign_no_match_rows),
        len(lobbying_no_match_rows),
        len(local_exact_rows),
        len(external_expansion_rows),
        len(no_outcome_rows),
    )


def bill_finance_lobbying_external_search_review_summary() -> tuple[int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW)
    exact_rows = [
        row for row in rows
        if int(row.get("lda_exact_activity_match_rows", "0") or "0") > 0
    ]
    no_exact_rows = [
        row for row in rows
        if normalize(row.get("lda_search_disposition"))
        == "official_lda_external_search_no_exact_current_bill_activity_text_match"
    ]
    campaign_pending_rows = [
        row for row in rows
        if normalize(row.get("campaign_external_scope_status")).startswith("fec_public_records_need")
    ]
    return (
        len(rows),
        len(exact_rows),
        sum(int(row.get("lda_exact_activity_match_rows", "0") or "0") for row in rows),
        sum(int(row.get("lda_exact_activity_match_filings", "0") or "0") for row in rows),
        sum(int(row.get("lda_exact_activity_match_clients", "0") or "0") for row in rows),
        len(no_exact_rows),
        len(campaign_pending_rows),
    )


def bill_finance_lobbying_external_lda_mention_review_summary() -> tuple[int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW)
    explicit_direction_rows = [
        row for row in rows
        if normalize(row.get("direction_status")) != "no_explicit_support_or_opposition"
    ]
    reference_rows = [
        row for row in rows
        if normalize(row.get("activity_disposition_status"))
        == "reviewed_current_bill_issue_reference_without_direction"
    ]
    advocacy_rows = [
        row for row in rows
        if normalize(row.get("activity_disposition_status"))
        == "reviewed_current_bill_issue_advocacy_without_direction"
    ]
    generic_target_rows = [
        row for row in rows
        if normalize(row.get("target_status")) == "reviewed_generic_chamber_or_agency_text_reference"
    ]
    return (
        len(rows),
        sum(int(row.get("rows_represented", "0") or "0") for row in rows),
        len(explicit_direction_rows),
        len(rows) - len(explicit_direction_rows),
        len(reference_rows),
        len(advocacy_rows),
        len(generic_target_rows),
    )


def bill_finance_lobbying_campaign_finance_target_scope_review_summary() -> tuple[int, int, int, int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW)
    unique_recipients = {
        normalize(recipient)
        for row in rows
        for recipient in row.get("campaign_scope_recipients", "").split(";")
        if normalize(recipient)
    }
    unique_transactions = {
        normalize(source_id)
        for row in rows
        for source_id in row.get("transaction_source_ids", "").split(";")
        if normalize(source_id)
    }
    candidate_target_only_rows = [
        row for row in rows
        if normalize(row.get("outside_spending_target_status"))
        == "reviewed_independent_expenditure_candidate_target_only"
    ]
    no_bill_id_rows = [
        row for row in rows
        if normalize(row.get("bill_identifier_status"))
        == "no_bill_id_field_or_current_bill_match_in_public_fec_openfec_scope"
    ]
    no_sponsor_overlap_rows = [
        row for row in rows
        if normalize(row.get("reviewed_bill_sponsor_candidate_overlap_status"))
        == "no_reviewed_bill_sponsor_candidate_overlap"
    ]
    no_committee_action_rows = [
        row for row in rows
        if normalize(row.get("committee_scope_status"))
        == "reviewed_candidate_committee_metadata_no_committee_of_jurisdiction_or_action"
    ]
    no_outcome_rows = [
        row for row in rows
        if normalize(row.get("outcome_link_status")) == "no_legislative_outcome_or_influence_evidence"
    ]
    return (
        len(rows),
        sum(int(row.get("campaign_scope_context_rows", "0") or "0") for row in rows),
        sum(int(row.get("campaign_scope_transaction_attachments", "0") or "0") for row in rows),
        len(unique_recipients),
        len(unique_transactions),
        len(candidate_target_only_rows),
        len(no_bill_id_rows),
        len(no_sponsor_overlap_rows),
        len(no_committee_action_rows),
        len(no_outcome_rows),
    )


def bill_finance_lobbying_committee_action_context_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT)
    committee_reported_rows = [
        row for row in rows
        if normalize(row.get("committee_reported")) == "yes"
    ]
    floor_considered_rows = [
        row for row in rows
        if normalize(row.get("floor_considered")) == "yes"
    ]
    committee_name_rows = [
        row for row in rows
        if normalize(row.get("committee_name_context_status"))
        != "no_committee_name_or_jurisdiction_source_in_current_cache"
    ]
    committee_action_influence_rows = [
        row for row in rows
        if normalize(row.get("committee_action_influence_status"))
        != "no_finance_or_lobbying_committee_action_influence_evidence"
    ]
    roll_call_influence_rows = [
        row for row in rows
        if normalize(row.get("roll_call_influence_status"))
        != "no_finance_or_lobbying_roll_call_influence_evidence"
    ]
    outcome_causality_rows = [
        row for row in rows
        if normalize(row.get("legislative_outcome_causality_status"))
        != "enacted_public_law_metadata_only_no_finance_or_lobbying_outcome_causality"
    ]
    external_lda_rows = [
        row for row in rows
        if int(row.get("external_lda_exact_activity_match_rows", "0") or "0") > 0
    ]
    campaign_target_rows = [
        row for row in rows
        if normalize(row.get("campaign_target_scope_status"))
        != "not_in_campaign_finance_target_scope_review"
    ]
    return (
        len(rows),
        len(committee_reported_rows),
        len(floor_considered_rows),
        len(committee_name_rows),
        len(committee_action_influence_rows),
        len(roll_call_influence_rows),
        len(outcome_causality_rows),
        len(external_lda_rows) + len(campaign_target_rows),
    )


def bill_finance_lobbying_committee_action_source_review_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW)
    fetched_rows = [
        row for row in rows
        if normalize(row.get("govinfo_billstatus_status")) == "official_govinfo_billstatus_fetched"
    ]
    committee_rows = [
        row for row in rows
        if normalize(row.get("committee_source_status")) == "official_govinfo_committee_names_present"
    ]
    committee_action_rows = [
        row for row in rows
        if normalize(row.get("committee_action_record_status"))
        == "official_govinfo_committee_action_records_present"
    ]
    floor_action_rows = [
        row for row in rows
        if normalize(row.get("floor_action_record_status")) == "official_govinfo_floor_action_records_present"
    ]
    roll_call_rows = [
        row for row in rows
        if int(row.get("roll_call_reference_count", "0") or "0") > 0
    ]
    public_law_rows = [
        row for row in rows
        if normalize(row.get("legislative_outcome_source_status"))
        == "official_govinfo_public_law_outcome_metadata_present_no_finance_lobbying_causality"
    ]
    unique_committees: set[str] = set()
    for row in committee_rows:
        for value in row.get("committee_names", "").split(";"):
            clean = " ".join(value.split())
            if clean:
                unique_committees.add(clean)
    return (
        len(rows),
        len(fetched_rows),
        len(committee_rows),
        len(committee_action_rows),
        len(floor_action_rows),
        len(roll_call_rows),
        len(public_law_rows),
        len(unique_committees),
    )


def bill_finance_lobbying_roll_call_source_review_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW)
    fetched_rows = [
        row for row in rows
        if normalize(row.get("source_fetch_status")) == "official_house_clerk_roll_call_xml_fetched"
    ]
    bill_match_rows = [
        row for row in rows
        if normalize(row.get("source_bill_match_status")) == "official_vote_legis_num_matches_bill_id"
    ]
    no_numbered_rows = [
        row for row in rows
        if normalize(row.get("roll_call_source_review_status"))
        == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    member_vote_rows = sum(int(row.get("member_vote_count", "0") or "0") for row in rows)
    return (
        len(rows),
        len(fetched_rows),
        len(bill_match_rows),
        len(no_numbered_rows),
        member_vote_rows,
    )


def bill_finance_lobbying_member_vote_target_review_summary() -> tuple[int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW)
    roll_call_keys = {
        (
            normalize(row.get("bill_id")),
            normalize(row.get("vote_year")),
            normalize(row.get("roll_call_number")),
        )
        for row in rows
        if normalize(row.get("bill_id")) and normalize(row.get("roll_call_number"))
    }
    unique_voters = {
        normalize(row.get("voter_bioguide_id"))
        for row in rows
        if normalize(row.get("voter_bioguide_id"))
    }
    bill_ids = {
        normalize(row.get("bill_id"))
        for row in rows
        if normalize(row.get("bill_id"))
    }
    same_bill_target_rows = [
        row for row in rows
        if normalize(row.get("same_bill_campaign_target_match_status"))
        == "same_bill_campaign_target_bioguide_overlap"
    ]
    broad_context_rows = [
        row for row in rows
        if normalize(row.get("broad_campaign_member_context_status"))
        == "broad_public_fec_candidate_member_context_present"
    ]
    return (
        len(rows),
        len(roll_call_keys),
        len(unique_voters),
        len(same_bill_target_rows),
        len(broad_context_rows),
        len(bill_ids),
    )


def bill_finance_lobbying_source_acquisition_queue_summary() -> tuple[int, int, int, int, int, int, int, int, int, int]:
    rows = read_csv(BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE)
    govinfo_committee_rows = [
        row for row in rows
        if normalize(row.get("local_govinfo_committee_row_status"))
        == "official_govinfo_committee_source_review_present"
    ]
    govinfo_no_direct_committee_rows = [
        row for row in rows
        if normalize(row.get("local_govinfo_committee_row_status"))
        == "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ]
    voteview_roll_call_rows = [
        row for row in rows
        if int(row.get("local_voteview_roll_call_rows", "0") or "0") > 0
    ]
    official_roll_call_rows = [
        row for row in rows
        if normalize(row.get("roll_call_acquisition_status"))
        == "official_house_clerk_roll_call_source_reviewed_no_finance_lobbying_influence_evidence"
    ]
    no_numbered_roll_call_rows = [
        row for row in rows
        if normalize(row.get("roll_call_acquisition_status"))
        == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    roll_call_acquisition_rows = [
        row for row in rows
        if normalize(row.get("roll_call_acquisition_status")) in {
            "official_billstatus_roll_call_references_present_needs_vote_source_join",
            "floor_action_source_reviewed_needs_official_roll_call_vote_source",
            "floor_considered_flag_without_local_voteview_match_needs_official_roll_call_source",
        }
    ]
    committee_acquisition_rows = [
        row for row in rows
        if normalize(row.get("committee_jurisdiction_acquisition_status")) not in {
            "official_committee_of_jurisdiction_source_reviewed",
            "official_govinfo_billstatus_reviewed_without_direct_committee_referral",
        }
    ]
    lda_priority_rows = [
        row for row in rows
        if int(row.get("external_lda_mention_packets", "0") or "0") > 0
    ]
    campaign_priority_rows = [
        row for row in rows
        if normalize(row.get("campaign_target_scope_status"))
        != "not_in_campaign_finance_target_scope_review"
    ]
    return (
        len(rows),
        len(govinfo_committee_rows),
        len(govinfo_no_direct_committee_rows),
        len(voteview_roll_call_rows),
        len(official_roll_call_rows),
        len(no_numbered_roll_call_rows),
        len(roll_call_acquisition_rows),
        len(committee_acquisition_rows),
        len(lda_priority_rows),
        len(campaign_priority_rows),
    )


def metadata_linked_law_bill_ids() -> set[str]:
    rows = read_csv(LAW_REVISION_BILL_LINKAGE)
    return {
        normalize(row.get("bill_id"))
        for row in rows
        if normalize(row.get("bill_id")) and normalize(row.get("linkage_status")) == "bill_action_metadata"
    }


def metadata_linked_rulemaking_document_numbers() -> set[str]:
    rows = read_csv(RULEMAKING_IMPLEMENTATION_LINKAGE)
    return {
        normalize(row.get("document_number") or row.get("law_id"))
        for row in rows
        if normalize(row.get("document_number") or row.get("law_id"))
        and normalize(row.get("linkage_status")) == "federal_register_document_metadata"
    }


def rulemaking_authority_summary() -> tuple[int, int, int]:
    rows = read_csv(RULEMAKING_AUTHORITY_LINKAGE)
    matched = [
        row for row in rows
        if normalize(row.get("linkage_status")) == "federal_register_authority_match"
    ]
    verified_docs = 0
    for row in matched:
        try:
            verified_docs += int(row.get("text_verified_rule_count") or "0")
        except ValueError:
            continue
    return len(matched), len(rows), verified_docs


def rulemaking_history_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(RULEMAKING_HISTORY_LINKAGE)
    matched = [
        row for row in rows
        if normalize(row.get("history_status")) == "proposed_rule_history_match"
    ]
    proposed_links = 0
    proposed_docs: set[str] = set()
    public_laws: set[str] = set()
    for row in matched:
        public_law = normalize(row.get("public_law_number"))
        if public_law:
            public_laws.add(public_law)
        try:
            proposed_links += int(row.get("matched_proposed_rule_count") or "0")
        except ValueError:
            continue
        proposed_docs.update(
            normalize(document)
            for document in row.get("proposed_document_numbers", "").split(";")
            if normalize(document)
        )
    return len(matched), len(rows), proposed_links, len(proposed_docs), len(public_laws)


def rulemaking_comment_record_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(RULEMAKING_COMMENT_RECORDS)
    complete_statuses = {
        "complete_comment_record_metadata_retrieved",
        "complete_no_comments_expected",
    }
    complete_rows = [
        row for row in rows
        if normalize(row.get("retrieval_status")) in complete_statuses
    ]
    partial_rows = [
        row for row in rows
        if normalize(row.get("retrieval_status")) not in complete_statuses
        and normalize(row.get("retrieved_comment_count"))
        and normalize(row.get("retrieved_comment_count")) != "0"
    ]
    complete_public_laws = {
        row.get("public_law_number", "").strip()
        for row in rows
        if row.get("public_law_number", "").strip()
        and all(
            normalize(other.get("retrieval_status")) in complete_statuses
            for other in rows
            if other.get("public_law_number", "").strip()
            == row.get("public_law_number", "").strip()
        )
    }
    retrieved_comments = 0
    for row in rows:
        try:
            retrieved_comments += int(row.get("retrieved_comment_count") or "0")
        except ValueError:
            continue
    return len(rows), len(complete_rows), len(partial_rows), len(complete_public_laws), retrieved_comments


def rulemaking_comment_text_review_summary() -> tuple[int, int, int, int, int, int, int, int]:
    rows = read_csv(RULEMAKING_COMMENT_TEXT_REVIEW)
    fetched_rows = [
        row for row in rows
        if normalize(row.get("detail_fetch_status")) == "comment_detail_fetched"
    ]
    complete_scope_rows = [
        row for row in rows
        if normalize(row.get("comment_detail_review_scope")) == "complete_docket_detail"
    ]
    partial_scope_rows = [
        row for row in rows
        if normalize(row.get("comment_detail_review_scope")) == "partial_docket_sample_detail"
    ]
    text_rows = [
        row for row in rows
        if normalize(row.get("comment_text_available")) == "yes"
    ]
    public_laws = {
        row.get("public_law_number", "").strip()
        for row in rows
        if row.get("public_law_number", "").strip()
    }
    attachment_rows = [
        row for row in rows
        if (int(row.get("attachment_count") or "0") if row.get("attachment_count", "").isdigit() else 0) > 0
    ]
    text_characters = 0
    for row in text_rows:
        try:
            text_characters += int(row.get("comment_text_character_count") or "0")
        except ValueError:
            continue
    return (
        len(rows),
        len(fetched_rows),
        len(text_rows),
        len(public_laws),
        len(complete_scope_rows),
        len(partial_scope_rows),
        len(attachment_rows),
        text_characters,
    )


def court_law_linkage_summary() -> tuple[int, int, int, int, int]:
    rows = read_csv(COURT_LAW_LINKAGE)
    usc_rows = [
        row for row in rows
        if normalize(row.get("court_usc_sections"))
    ]
    matched = [
        row for row in rows
        if normalize(row.get("linkage_status")) == "usc_section_authority_overlap"
    ]
    public_laws = {
        normalize(public_law)
        for row in matched
        for public_law in row.get("public_law_numbers", "").split(";")
        if normalize(public_law)
    }
    bill_ids = {
        normalize(bill_id)
        for row in matched
        for bill_id in row.get("bill_ids", "").split(";")
        if normalize(bill_id)
    }
    sections = {
        normalize(section)
        for row in matched
        for section in row.get("matched_usc_sections", "").split(";")
        if normalize(section)
    }
    return len(matched), len(usc_rows), len(public_laws), len(bill_ids), len(sections)


def district_opinion_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (normalize(row.get("district_id")), normalize(row.get("issue")), normalize(row.get("year")))


def metadata_linked_district_opinion_keys() -> set[tuple[str, str, str]]:
    rows = read_csv(DISTRICT_PUBLIC_OPINION_LINKAGE)
    return {
        district_opinion_key(row)
        for row in rows
        if all(district_opinion_key(row)) and normalize(row.get("linkage_status")) == "sponsor_district_bill_metadata"
    }


def count_linked_district_opinion_rows(rows: list[dict[str, str]]) -> int:
    linked_keys = metadata_linked_district_opinion_keys()
    if not linked_keys:
        return 0
    return sum(1 for row in rows if district_opinion_key(row) in linked_keys)


def district_opinion_policy_context_summary() -> tuple[int, int, int, int]:
    rows = read_csv(DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT)
    mapped = [
        row for row in rows
        if normalize(row.get("policy_context_status")) == "sponsor_district_bill_policy_context"
    ]
    return (
        len(mapped),
        len({district_opinion_key(row) for row in mapped if all(district_opinion_key(row))}),
        len({normalize(row.get("bill_id")) for row in mapped if normalize(row.get("bill_id"))}),
        len({normalize(row.get("policy_area")) for row in mapped if normalize(row.get("policy_area"))}),
    )


def district_opinion_bill_topic_readiness_summary() -> tuple[int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS.exists():
        return 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS)
    proxy_only = [
        row for row in rows
        if normalize(row.get("bill_topic_public_opinion_status"))
        == "proxy_only_missing_issue_specific_bill_support"
    ]
    issue_specific_rows = 0
    affected_group_rows = 0
    for row in rows:
        try:
            issue_specific_rows += int(row.get("issue_specific_support_rows") or "0")
            affected_group_rows += int(row.get("affected_group_support_rows") or "0")
        except ValueError:
            continue
    return len(rows), len(proxy_only), issue_specific_rows, affected_group_rows


def district_opinion_source_packet_summary() -> tuple[int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS.exists():
        return 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS)
    packet_only = [
        row for row in rows
        if normalize(row.get("acquisition_status"))
        == "source_packet_only_no_external_dataset_acquired"
    ]
    policy_areas = {
        normalize(row.get("policy_area"))
        for row in rows
        if normalize(row.get("policy_area"))
    }
    return len(rows), len(packet_only), len(policy_areas)


def district_opinion_census_denominator_summary() -> tuple[int, int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS.exists():
        return 0, 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS)
    matched = [
        row for row in rows
        if normalize(row.get("denominator_status"))
        == "official_tigerweb_population_housing_denominator"
    ]
    districts = {
        value.strip()
        for row in matched
        for value in row.get("matched_denominator_districts", "").split(";")
        if value.strip()
    }
    total_pop = 0
    total_hu = 0
    for row in matched:
        try:
            total_pop += int(row.get("total_pop100") or "0")
            total_hu += int(row.get("total_hu100") or "0")
        except ValueError:
            continue
    return len(rows), len(matched), len(districts), total_pop, total_hu


def district_opinion_acs_context_summary() -> tuple[int, int, int, int, int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_ACS_CONTEXT.exists():
        return 0, 0, 0, 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_ACS_CONTEXT)
    matched = [
        row for row in rows
        if normalize(row.get("acs_context_status"))
        == "official_acs_2017_2021_5yr_district_context"
    ]
    districts = {
        value.strip()
        for row in matched
        for value in row.get("matched_acs_context_districts", "").split(";")
        if value.strip()
    }

    def total(field: str) -> int:
        result = 0
        for row in matched:
            try:
                result += int(float(row.get(field) or "0"))
            except ValueError:
                continue
        return result

    return (
        len(rows),
        len(matched),
        len(districts),
        total("total_acs_population_est"),
        total("total_veterans_est"),
        total("total_not_us_citizen_est"),
        total("total_below_poverty_est"),
        total("total_no_internet_access_est"),
    )


def district_opinion_survey_source_crosswalk_summary() -> tuple[int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK.exists():
        return 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK)
    no_item_rows = [
        row for row in rows
        if normalize(row.get("survey_crosswalk_status"))
        == "survey_source_crosswalk_no_item_acquired"
    ]
    source_families = {
        normalize(source)
        for row in rows
        for source in (
            [row.get("primary_survey_source_family", "")]
            + row.get("secondary_survey_source_families", "").split(";")
        )
        if normalize(source)
    }
    return len(rows), len(no_item_rows), len(source_families)


def district_opinion_survey_item_proxy_review_summary() -> tuple[int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW.exists():
        return 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW)
    proxy_reviewed = [
        row for row in rows
        if normalize(row.get("current_proxy_review_status"))
        == "exact_current_ces_proxy_variables_reviewed_no_bill_topic_item"
    ]
    bill_topic_items = [
        row for row in rows
        if normalize(row.get("acquired_bill_topic_item_ids"))
    ]
    policy_areas = {
        normalize(row.get("policy_area"))
        for row in rows
        if normalize(row.get("policy_area"))
    }
    return len(rows), len(proxy_reviewed), len(bill_topic_items), len(policy_areas)


def district_opinion_ces_policy_item_candidate_review_summary() -> tuple[int, int, int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW.exists():
        return 0, 0, 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW)
    rows_with_candidates = [
        row for row in rows
        if normalize(row.get("candidate_item_review_status"))
        == "official_ces_policy_preference_candidate_items_found_no_bill_support_estimate"
    ]
    rows_without_candidates = [
        row for row in rows
        if normalize(row.get("candidate_item_review_status"))
        == "no_official_ces_policy_preference_candidate_item_for_policy_area"
    ]
    unique_items = {
        normalize(item)
        for row in rows
        for item in row.get("candidate_policy_preference_item_ids", "").split(";")
        if normalize(item)
    }
    policy_areas = {
        normalize(row.get("policy_area"))
        for row in rows
        if normalize(row.get("policy_area"))
    }
    source_variables = {
        normalize(item)
        for row in rows
        for item in row.get("candidate_policy_preference_item_ids", "").split(";")
        if normalize(item)
    }
    return (
        len(rows),
        len(rows_with_candidates),
        len(rows_without_candidates),
        len(unique_items),
        len(policy_areas),
        len(source_variables),
    )


def district_opinion_ces_policy_item_response_distribution_summary() -> tuple[int, int, int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW.exists():
        return 0, 0, 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW)
    rows_with_distributions = [
        row for row in rows
        if normalize(row.get("response_distribution_status"))
        == "official_ces_policy_preference_raw_response_distributions_available_no_support_direction"
    ]
    rows_without_distributions = [
        row for row in rows
        if normalize(row.get("response_distribution_status"))
        == "no_candidate_item_response_distribution_available"
    ]
    unique_items = {
        normalize(item)
        for row in rows
        for item in row.get("candidate_policy_preference_item_ids", "").split(";")
        if normalize(item)
    }
    distribution_years = {
        normalize(year)
        for row in rows
        for year in row.get("observed_response_years", "").split(";")
        if normalize(year)
    }
    attached_observations = sum(
        int(row.get("source_item_response_observation_count") or "0")
        for row in rows_with_distributions
    )
    return (
        len(rows),
        len(rows_with_distributions),
        len(rows_without_distributions),
        len(unique_items),
        len(distribution_years),
        attached_observations,
    )


def district_opinion_ces_policy_item_codebook_direction_summary() -> tuple[int, int, int, int, int, int, int]:
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW.exists():
        return 0, 0, 0, 0, 0, 0, 0
    rows = read_csv(DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW)
    rows_with_direction = [
        row for row in rows
        if normalize(row.get("guide_codebook_direction_status"))
        == "official_ces_policy_preference_codebook_direction_review_available_no_bill_mapping"
    ]
    rows_without_direction = [
        row for row in rows
        if normalize(row.get("guide_codebook_direction_status"))
        == "no_candidate_item_codebook_direction_available"
    ]
    rows_with_binary_direction = [
        row for row in rows_with_direction
        if int(row.get("candidate_items_with_binary_item_direction_count") or "0") > 0
    ]
    unique_items = {
        normalize(item)
        for row in rows_with_direction
        for item in row.get("candidate_policy_preference_item_ids", "").split(";")
        if normalize(item)
    }
    binary_items = set()
    for row in rows_with_direction:
        try:
            label_summary = json.loads(row.get("candidate_item_codebook_label_summary", "[]") or "[]")
        except json.JSONDecodeError:
            label_summary = []
        binary_items.update(
            normalize(item.get("variable_id", ""))
            for item in label_summary
            if item.get("direction_type") == "binary_item_support_oppose"
            and normalize(item.get("variable_id", ""))
        )
    direction_types = {
        normalize(direction_type)
        for row in rows_with_direction
        for direction_type in row.get("candidate_item_direction_types", "").split(";")
        if normalize(direction_type)
    }
    return (
        len(rows),
        len(rows_with_direction),
        len(rows_without_direction),
        len(rows_with_binary_direction),
        len(unique_items),
        len(binary_items),
        len(direction_types),
    )


def district_opinion_bill_item_support_summary() -> tuple[int, int, int, int, int, int, int, int, int]:
    alignment_rows = read_csv(DISTRICT_PUBLIC_OPINION_BILL_ITEM_ALIGNMENT_REVIEW)
    support_rows = read_csv(DISTRICT_PUBLIC_OPINION_BILL_TOPIC_SUPPORT)
    positive_alignments = [
        row for row in alignment_rows
        if normalize(row.get("manual_alignment_status"))
        == "reviewed_aligned_historical_issue_item"
    ]
    published_support = [
        row for row in support_rows
        if normalize(row.get("weighted_support_share"))
        and normalize(row.get("historical_related_issue_support_status"))
        == "privacy_thresholded_direct_weighted_district_estimate_available"
    ]
    respondents = sum(
        int(row.get("response_respondents") or "0") for row in published_support
    )
    return (
        len(alignment_rows),
        len(positive_alignments),
        len(alignment_rows) - len(positive_alignments),
        len(published_support),
        len({normalize(row.get("bill_id")) for row in published_support}),
        len({normalize(row.get("sponsor_district_id")) for row in published_support}),
        len({normalize(row.get("survey_item_id")) for row in published_support}),
        len({normalize(row.get("survey_year")) for row in published_support}),
        respondents,
    )


def build_row(
    source: dict[str, str],
    rows: list[dict[str, str]],
    linked_rows: int,
    linkage_status: str,
    linked_to: str,
    link_key: str,
    linkage_boundary: str,
    next_link_step: str | None = None,
) -> dict[str, str]:
    total_rows = len(rows)
    return {
        "sourceFamily": source["source_family"],
        "sourceName": source["source_name"],
        "dataset": source["dataset"],
        "priority": source["priority"],
        "boundaryCategory": source["boundary_category"],
        "linkageStatus": linkage_status,
        "linkedTo": linked_to,
        "linkKey": link_key,
        "linkedRows": str(linked_rows),
        "totalRows": str(total_rows),
        "linkedShare": share(linked_rows, total_rows),
        "linkageBoundary": linkage_boundary,
        "nextLinkStep": next_link_step if next_link_step is not None else source["next_step"],
    }


def linkage_rows(registry: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_dataset: dict[str, list[dict[str, str]]] = {
        source["dataset"]: raw_rows(source.get("raw_path", ""))
        for source in registry
    }
    bill_rows = rows_by_dataset.get("bill_progression.csv", [])
    topic_rows = rows_by_dataset.get("topic_throughput.csv", [])
    law_rows = rows_by_dataset.get("law_revision_history.csv", [])

    topic_values = normalized_values(topic_rows, "topic")
    bill_id_values = normalized_values(bill_rows, "bill_id")
    public_law_values = normalized_values(law_rows, "public_law_number")
    authority_matched_rows, authority_total_rows, authority_verified_docs = rulemaking_authority_summary()
    (
        sponsor_matched_rows,
        sponsor_unique_bills,
        sponsor_attached_bill_links,
        sponsor_attached_enacted_links,
        sponsor_public_laws,
    ) = sponsor_bill_linkage_summary()
    (
        comparative_matched_rows,
        comparative_countries,
        comparative_scenario_keys,
        comparative_bicameral_rows,
    ) = comparative_institution_linkage_summary()
    (
        history_matched_final_rows,
        history_total_final_rows,
        history_proposed_links,
        history_unique_proposed_docs,
        history_public_laws,
    ) = rulemaking_history_summary()
    (
        comment_record_docket_rows,
        complete_comment_record_docket_rows,
        partial_comment_record_docket_rows,
        complete_comment_record_public_laws,
        retrieved_comment_record_rows,
    ) = rulemaking_comment_record_summary()
    (
        comment_text_review_rows,
        fetched_comment_text_review_rows,
        text_available_comment_rows,
        comment_text_public_laws,
        complete_comment_text_review_rows,
        partial_comment_text_review_rows,
        comment_text_attachment_rows,
        comment_text_characters,
    ) = rulemaking_comment_text_review_summary()
    (
        court_authority_overlap_rows,
        court_usc_rows,
        court_public_laws,
        court_bill_ids,
        court_usc_sections,
    ) = court_law_linkage_summary()
    (
        target_diff_review_rows,
        source_reviewed_target_diff_rows,
        no_exact_target_diff_review_rows,
        unresolved_target_diff_review_rows,
        target_diff_review_public_laws,
    ) = statutory_target_section_diff_review_summary()
    (
        no_structured_target_review_rows,
        no_structured_target_review_public_laws,
    ) = statutory_no_target_review_summary()
    (
        target_lifecycle_bridge_rows,
        raw_scdb_target_base_rows,
        raw_scdb_target_exact_rows,
        raw_scdb_target_cases,
        raw_scdb_target_post_enactment_attachments,
    ) = statutory_target_lifecycle_bridge_summary()
    (
        complete_lineage_expansion_rows,
        complete_lineage_active_rows,
        complete_lineage_candidate_expansion_rows,
        complete_lineage_final_audit_rows,
        complete_lineage_no_target_rows,
        complete_lineage_source_candidates,
        complete_lineage_source_candidate_gap,
        complete_lineage_triage_packet_gap,
    ) = statutory_complete_lineage_expansion_queue_summary()
    (
        target_packet_expansion_rows,
        target_packet_expansion_public_laws,
        target_packet_note_review_rows,
        target_packet_title_only_rows,
        target_packet_incomplete_rows,
    ) = statutory_target_packet_expansion_queue_summary()
    (
        target_packet_source_gap_rows,
        target_packet_source_gap_public_laws,
        target_packet_current_no_marker_rows,
        target_packet_current_marker_rows,
        target_packet_source_gap_title_only_rows,
        target_packet_source_gap_incomplete_rows,
        target_packet_manual_source_gap_rows,
        target_packet_downstream_present_rows,
    ) = statutory_target_packet_source_gap_queue_summary()
    (
        target_packet_source_gap_review_rows,
        target_packet_source_gap_review_public_laws,
        target_packet_source_gap_review_temporary_rows,
        target_packet_source_gap_review_appropriation_rows,
        target_packet_source_gap_review_cross_reference_rows,
        target_packet_source_gap_review_table_rows,
    ) = statutory_target_packet_source_gap_review_summary()
    (
        target_reference_resolution_rows,
        target_reference_resolution_public_laws,
        target_reference_resolution_candidate_rows,
        target_reference_resolution_candidate_count,
        target_reference_resolution_unresolved_rows,
    ) = statutory_target_reference_resolution_candidate_summary()

    result: list[dict[str, str]] = []
    for source in registry:
        family = source["source_family"]
        rows = rows_by_dataset.get(source["dataset"], [])

        if family == "Congress.gov bill histories":
            linked = count_linked_rows(rows, "policy_area", topic_values)
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Comparative Agendas topic throughput",
                "bill_progression.policy_area -> topic_throughput.topic",
                "Bills can be joined to the current topic-throughput aggregate by Congress.gov policy area; this is not an independent CAP-coded topic or public-opinion link.",
            ))
        elif family == "govinfo bill and action records":
            linked, action_aligned, policy_aligned = govinfo_billstatus_linkage_summary()
            if linked > 0:
                result.append(build_row(
                    source,
                    rows,
                    linked,
                    "metadata linked" if linked == len(rows) else "partially linked",
                    "govinfo BILLSTATUS bulkdata",
                    "bill_progression.congress,bill_type,bill_number -> govinfo_billstatus_linkage.congress,bill_type,bill_number",
                    f"Govinfo BILLSTATUS rows independently cross-check the cached Congress.gov bill universe by congress, bill type, and bill number for {linked} bills; {action_aligned} rows align with the local coarse action flags and {policy_aligned} rows align on policy area. This remains bounded to the cached sample and does not provide a full bill census, public-opinion evidence, campaign-finance or lobbying influence, implementation or court outcomes, public benefit, welfare, or model validation.",
                    "Expand the govinfo BILLSTATUS cross-check beyond the current bounded sample into a full bill/action census and review action-text differences before using it for stronger bill-flow claims.",
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not independently linked",
                "Congress.gov bill histories",
                "shared bill_progression.csv raw cache",
                "This source-family row is represented through the Congress.gov-derived bill sample and calibration notes, so it cannot yet independently cross-check bill actions.",
                "Build the govinfo BILLSTATUS linkage cache and join it to Congress.gov bills by congress, bill type, and bill number.",
            ))
        elif family == "Voteview roll-call data":
            metadata_linked = count_linked_voteview_rows(rows)
            if metadata_linked > 0:
                (
                    bill_rollcall_rows,
                    bill_member_vote_rows,
                    bill_progression_rollcall_rows,
                    bill_progression_member_vote_rows,
                ) = voteview_bill_linkage_summary()
                bill_context = ""
                linked_to = "Voteview HS member metadata file"
                link_key = "voteview_rollcalls.congress,chamber,icpsr -> voteview_member_context.congress,chamber,icpsr"
                next_step = "Add roll-call-to-bill/action metadata and use member identifiers for sponsor, district, and bill-topic joins."
                if bill_rollcall_rows:
                    linked_to = (
                        "Voteview HS member metadata and bounded Voteview roll-call bill metadata"
                    )
                    link_key = (
                        "voteview_rollcalls.congress,chamber,icpsr -> voteview_member_context.congress,chamber,icpsr; "
                        "voteview_rollcalls.vote_id -> voteview_bill_linkage.vote_id"
                    )
                    bill_context = (
                        f" The bounded bill-linkage cache parses bill IDs for {bill_rollcall_rows} roll-call metadata rows "
                        f"covering {bill_member_vote_rows} member-vote rows; {bill_progression_rollcall_rows} of those "
                        f"roll calls covering {bill_progression_member_vote_rows} member-vote rows overlap the cached "
                        "Congress.gov bill-progression sample."
                    )
                    next_step = (
                        "Expand roll-call-to-bill/action coverage beyond the current bounded crosswalk and join bill IDs "
                        "to topics, district public opinion, sponsor histories, public laws, implementation, or court outcomes."
                    )
                result.append(build_row(
                    source,
                    rows,
                    metadata_linked,
                    "metadata linked",
                    linked_to,
                    link_key,
                    "Roll-call rows now join to public Voteview member metadata with Bioguide, party, state, district, and ideal-point fields."
                    + bill_context
                    + " They still do not provide complete roll-call-to-bill coverage, public-law/statute linkage, issue-topic public-opinion rows, sponsor-effectiveness rows, implementation/court outcomes, or legislative-outcome validation.",
                    next_step,
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "Roll-call rows lack bill IDs, public laws, districts, topics, member-context rows, or public-opinion rows in the current extract.",
                "Add the Voteview member-context cache plus roll-call-to-bill/action metadata for sponsor, district, and bill-topic joins.",
            ))
        elif family == "Comparative Agendas topic throughput":
            linked = count_linked_rows(rows, "topic", normalized_values(bill_rows, "policy_area"))
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Congress.gov bill histories",
                "topic_throughput.topic -> bill_progression.policy_area",
                "The current topic rows join to sampled bill policy areas, but they remain Congress.gov policy areas rather than full CAP-coded topic evidence.",
            ))
        elif family == "QoG and V-Dem comparative institutions":
            if comparative_matched_rows > 0:
                result.append(build_row(
                    source,
                    rows,
                    comparative_matched_rows,
                    "metadata linked" if comparative_matched_rows == len(rows) else "partially linked",
                    "bounded simulator chamber, party-system, district-magnitude, and review scenario-family metadata",
                    "comparative_institutions.iso3,year -> comparative_institution_linkage.iso3,year -> simulator scenarioKey anchors",
                    f"Country-year comparative institution rows now map to bounded simulator scenario-family metadata anchors for {comparative_matched_rows} / {len(rows)} rows across {comparative_countries} countries, {comparative_scenario_keys} simulator scenario keys, and {comparative_bicameral_rows} bicameral country-year profiles. This is comparative-institution metadata only; it is not observed law-output productivity, bicameral disagreement evidence, country-level institutional fit, adoption evidence, welfare, causal inference, or model validation.",
                    "Add IPU/ParlGov chamber identifiers, observed country-year legislative-output rows, and bicameral disagreement data before making comparative institutional-fit or productivity claims.",
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "Country-year comparative institution rows are not joined to observed chamber-level bill outputs or simulator institution specifications in this run.",
                "Run make build-comparative-institution-linkage-raw for bounded simulator scenario-family metadata, then add IPU/ParlGov chamber identifiers and observed legislative-output data.",
            ))
        elif family == "Senate LDA lobbying disclosures":
            crosswalk_issues = linked_lobbying_issues()
            linked = count_linked_rows(rows, "issue", crosswalk_issues)
            if linked > 0:
                issue_count, linked_lobbying_rows = lobbying_issue_linkage_summary()
                (
                    policy_context_issues,
                    policy_context_lobbying_rows,
                    issue_bill_contexts,
                    policy_context_bills,
                    policy_context_enacted_bills,
                ) = lobbying_bill_policy_context_summary()
                bill_policy_sentence = ""
                bill_mention_sentence = ""
                local_review_sentence = ""
                linked_to = "Documented LDA issue-to-Congress.gov policy-area crosswalk and Comparative Agendas topic throughput"
                link_key = "lobbying_disclosure.issue -> lobbying_issue_linkage.lobbying_issue -> topic_throughput.topic"
                next_step = "Add client-to-bill, bill-topic, sponsor/member, and committee-of-jurisdiction joins for LDA filings while preserving the no-causal-capture boundary."
                if policy_context_issues > 0:
                    linked_to = (
                        "Documented LDA issue-to-Congress.gov policy-area crosswalk, "
                        "Comparative Agendas topic throughput, and cached govinfo bill/action metadata by shared policy area"
                    )
                    link_key = (
                        "lobbying_disclosure.issue -> lobbying_issue_linkage.lobbying_issue -> "
                        "topic_throughput.topic; lobbying_issue_linkage.topic -> "
                        "lobbying_bill_policy_context.topic -> govinfo_billstatus_linkage.policy_area"
                    )
                    bill_policy_sentence = (
                        f" The bounded bill-policy context report maps {policy_context_lobbying_rows} activity rows "
                        f"across {policy_context_issues} issue labels to {issue_bill_contexts} issue-policy bill contexts, "
                        f"{policy_context_bills} unique cached bill IDs, and {policy_context_enacted_bills} unique enacted cached bill IDs by shared policy area."
                    )
                    next_step = (
                        "Extend exact filing-text bill-identifier review, then add sponsor/member targets, "
                        "committee-of-jurisdiction review, roll-call exposure, or legislative-outcome metadata while "
                        "preserving the no-causal-capture boundary."
                    )
                mention_rows, mention_bills, mention_filings, mention_clients = lobbying_bill_mention_summary()
                if mention_rows > 0:
                    (
                        action_context_bills,
                        action_context_sponsors,
                        action_context_committee_reported,
                        action_context_floor,
                        action_context_enacted,
                    ) = lobbying_bill_action_metadata_summary()
                    (
                        visible_text_rows,
                        text_refetch_rows,
                        support_text_rows,
                        opposition_text_rows,
                        mixed_text_rows,
                        position_text_rows,
                        list_only_text_rows,
                    ) = lobbying_bill_text_signal_summary()
                    (
                        manual_disposition_rows,
                        high_disposition_rows,
                        medium_disposition_rows,
                        low_disposition_rows,
                    ) = lobbying_bill_disposition_review_summary()
                    (
                        directional_packets,
                        directional_rows,
                        directional_support_packets,
                        directional_opposition_packets,
                        directional_downgraded_packets,
                        directional_corrected_packets,
                    ) = lobbying_bill_medium_directional_review_summary()
                    (
                        position_activity_packets,
                        position_activity_rows,
                        position_activity_issue_packets,
                        position_activity_monitoring_packets,
                        position_activity_all_provisions_packets,
                        position_activity_position_packets,
                        position_activity_opposition_packets,
                        position_activity_generic_congress_packets,
                    ) = lobbying_bill_medium_position_activity_review_summary()
                    linked_to += (
                        ", exact official LDA filing-text bill identifiers for a bounded public-law subset, "
                        "cached Congress.gov public-law bill/action metadata for those identifiers, "
                        "bounded stored activity-text position-signal review, "
                        "and a disposition/target source-review queue"
                    )
                    link_key += (
                        "; lobbying_bill_mentions.bill_id -> law_revision_bill_linkage.bill_id; "
                        "lobbying_bill_mentions.activity_description -> stored bill-reference text context; "
                        "lobbying_bill_text_review.source_row_fingerprint -> "
                        "lobbying_bill_disposition_review.source_row_fingerprint; "
                        "lobbying_bill_medium_disposition_packets.packet_fingerprint -> "
                        "lobbying_bill_medium_position_activity_packet_review.packet_fingerprint"
                    )
                    bill_mention_sentence = (
                        f" A bounded official filing-text scan adds {mention_rows} exact activity-text bill mention rows "
                        f"across {mention_bills} cached public-law bill IDs, {mention_filings} filing IDs, "
                        f"and {mention_clients} clients."
                    )
                    if action_context_bills > 0:
                        bill_mention_sentence += (
                            f" Those exact bill IDs join to cached Congress.gov public-law bill/action metadata for "
                            f"{action_context_bills} bills, including sponsor metadata for {action_context_sponsors}, "
                            f"committee-reported flags for {action_context_committee_reported}, floor-considered flags "
                            f"for {action_context_floor}, and enacted public-law outcome metadata for {action_context_enacted}."
                        )
                    if visible_text_rows > 0:
                        bill_mention_sentence += (
                            f" Stored LDA activity-text review locates the bill reference in {visible_text_rows} "
                            f"rows, classifying {support_text_rows} explicit support text-signal rows, "
                            f"{opposition_text_rows} explicit opposition text-signal rows, "
                            f"{mixed_text_rows} mixed support/opposition rows, {position_text_rows} "
                            f"position/activity text-signal rows without direction, and {list_only_text_rows} "
                            "bill-list or title-only rows."
                        )
                        if text_refetch_rows > 0:
                            bill_mention_sentence += (
                                f" {text_refetch_rows} cached exact-match rows need full activity-text refetch "
                                "because the stored excerpt is truncated before the reference."
                            )
                        else:
                            bill_mention_sentence += (
                                " No cached exact-match rows remain blocked by local activity-text truncation."
                            )
                    if manual_disposition_rows > 0:
                        bill_mention_sentence += (
                            f" A disposition/target source-review queue marks {manual_disposition_rows} "
                            f"rows for manual review, including {high_disposition_rows} high-priority rows "
                            f"and {medium_disposition_rows} medium-priority rows, while retaining "
                            f"{low_disposition_rows} low-priority bill-reference-only rows."
                        )
                    if directional_packets > 0:
                        bill_mention_sentence += (
                            f" A medium-priority directional packet review source-reviews "
                            f"{directional_packets} support/opposition packets representing "
                            f"{directional_rows} rows, confirming {directional_support_packets} "
                            f"current-bill support packets and {directional_opposition_packets} "
                            "current-bill opposition packet while downgrading "
                            f"{directional_downgraded_packets} packets to other-measure direction "
                            "or monitoring/reference context and correcting "
                            f"{directional_corrected_packets} opposition packet to current-bill support."
                        )
                    if position_activity_packets > 0:
                        bill_mention_sentence += (
                            f" A medium-priority position/activity packet review source-reviews "
                            f"{position_activity_packets} packets representing {position_activity_rows} rows, "
                            f"classifying {position_activity_issue_packets} current-bill issue/provision "
                            f"activity packets, {position_activity_monitoring_packets} monitoring/analysis "
                            f"packets, {position_activity_all_provisions_packets} all-provisions packets, "
                            f"{position_activity_position_packets} position-represented packets, and "
                            f"{position_activity_opposition_packets} current-bill opposition packet found "
                            f"in the position/activity queue, with "
                        f"{position_activity_generic_congress_packets} generic Congress text-reference packets."
                        )
                    next_step = (
                        "Use the reviewed LDA packet reports to add sponsor/member target beyond activity-text "
                        "references, committee-action, roll-call exposure, legislative-outcome source review, "
                        "and campaign-finance target review while "
                        "preserving the no-causal-capture boundary."
                    )
                (
                    local_review_rows,
                    local_review_campaign_no_match_rows,
                    local_review_lobbying_no_match_rows,
                    local_review_exact_rows,
                    local_review_external_rows,
                    local_review_no_outcome_rows,
                ) = bill_finance_lobbying_local_context_review_summary()
                (
                    external_review_rows,
                    external_review_exact_bill_rows,
                    external_review_exact_activity_rows,
                    external_review_exact_filing_rows,
                    external_review_exact_client_rows,
                    external_review_no_exact_rows,
                    external_review_campaign_pending_rows,
                ) = bill_finance_lobbying_external_search_review_summary()
                (
                    external_mention_packets,
                    external_mention_rows,
                    external_mention_direction_packets,
                    external_mention_no_direction_packets,
                    external_mention_reference_packets,
                    external_mention_advocacy_packets,
                    external_mention_generic_target_packets,
                ) = bill_finance_lobbying_external_lda_mention_review_summary()
                (
                    target_scope_review_rows,
                    target_scope_context_attachments,
                    target_scope_transaction_attachments,
                    target_scope_unique_recipients,
                    target_scope_unique_transactions,
                    target_scope_candidate_target_rows,
                    target_scope_no_bill_id_rows,
                    target_scope_no_sponsor_overlap_rows,
                    target_scope_no_committee_action_rows,
                    target_scope_no_outcome_rows,
                ) = bill_finance_lobbying_campaign_finance_target_scope_review_summary()
                (
                    committee_context_rows,
                    committee_context_reported_rows,
                    committee_context_floor_rows,
                    committee_context_name_rows,
                    committee_context_action_influence_rows,
                    committee_context_roll_call_rows,
                    committee_context_outcome_rows,
                    _committee_context_reviewed_source_rows,
                ) = bill_finance_lobbying_committee_action_context_summary()
                (
                    source_review_rows,
                    source_review_fetched_rows,
                    source_review_committee_rows,
                    source_review_committee_action_rows,
                    source_review_floor_action_rows,
                    source_review_roll_call_rows,
                    source_review_public_law_rows,
                    source_review_unique_committees,
                ) = bill_finance_lobbying_committee_action_source_review_summary()
                (
                    roll_call_source_rows,
                    roll_call_source_fetched_rows,
                    roll_call_source_bill_match_rows,
                    roll_call_source_no_numbered_rows,
                    roll_call_source_member_vote_rows,
                ) = bill_finance_lobbying_roll_call_source_review_summary()
                (
                    member_vote_target_rows,
                    member_vote_target_roll_calls,
                    member_vote_target_unique_voters,
                    member_vote_same_bill_overlap_rows,
                    member_vote_broad_context_rows,
                    member_vote_target_bill_rows,
                ) = bill_finance_lobbying_member_vote_target_review_summary()
                (
                    source_acquisition_rows,
                    source_acquisition_govinfo_committee_rows,
                    source_acquisition_govinfo_no_direct_committee_rows,
                    source_acquisition_voteview_rows,
                    source_acquisition_official_roll_call_rows,
                    source_acquisition_no_numbered_roll_call_rows,
                    source_acquisition_roll_call_rows,
                    source_acquisition_committee_rows,
                    source_acquisition_lda_priority_rows,
                    source_acquisition_campaign_priority_rows,
                ) = bill_finance_lobbying_source_acquisition_queue_summary()
                if local_review_rows > 0:
                    linked_to += (
                        ", and local bill-finance/lobbying no-current-match review for queued public-law rows"
                    )
                    link_key += (
                        "; bill_finance_lobbying_review_queue.bill_id -> "
                        "bill_finance_lobbying_local_context_review.bill_id"
                    )
                    local_review_sentence = (
                        f" A bill-finance/lobbying local-context review source-reviews "
                        f"{local_review_rows} queued public-law rows, confirming that "
                        f"{local_review_campaign_no_match_rows} rows with same-policy "
                        "campaign-finance context and "
                        f"{local_review_lobbying_no_match_rows} rows with same-policy "
                        "lobbying context have no current-bill exact match in the local context; "
                        f"{local_review_exact_rows} rows carry a local current-bill finance/lobbying exact match, "
                        f"{local_review_external_rows} rows still require external target/source expansion, "
                        f"and {local_review_no_outcome_rows} rows preserve no-outcome-influence status."
                    )
                    next_step = (
                        "Use the reviewed LDA packet reports and bill-finance/lobbying local-context review "
                        "to add external current-bill target/source expansion, sponsor/member targets beyond "
                        "activity-text references, committee-action, roll-call exposure, and legislative-outcome "
                        "source review while preserving the no-causal-capture boundary."
                    )
                external_review_sentence = ""
                if external_review_rows > 0:
                    linked_to += (
                        ", and external LDA current-bill activity-text search for queued public-law rows"
                    )
                    link_key += (
                        "; bill_finance_lobbying_local_context_review.bill_id -> "
                        "bill_finance_lobbying_external_search_review.bill_id"
                    )
                    external_review_sentence = (
                        f" A targeted external LDA search review covers {external_review_rows} queued "
                        f"public-law rows using compact and dotted current-bill terms, finding "
                        f"{external_review_exact_activity_rows} exact activity-text current-bill mention rows "
                        f"across {external_review_exact_bill_rows} bills, {external_review_exact_filing_rows} filings, "
                        f"and {external_review_exact_client_rows} clients, with "
                        f"{external_review_no_exact_rows} rows retaining complete no-exact-match LDA search status "
                        f"and {external_review_campaign_pending_rows} rows marked for FEC/OpenFEC "
                        "candidate, committee, or outside-spending target-scope review."
                    )
                    next_step = (
                        "Run the external LDA mention-review packet target for support/opposition, "
                        "sponsor/member target, committee-action, roll-call, and outcome context, then run "
                        "FEC/OpenFEC candidate, committee, or outside-spending target-scope review for the "
                        "campaign-finance rows while preserving the no-causal-capture boundary."
                    )
                external_mention_review_sentence = ""
                if external_mention_packets > 0:
                    linked_to += (
                        ", and external LDA current-bill mention source review"
                    )
                    link_key += (
                        "; bill_finance_lobbying_external_search_review.bill_id -> "
                        "bill_finance_lobbying_external_lda_mention_review.bill_id"
                    )
                    external_mention_review_sentence = (
                        f" The external LDA mention review source-reviews "
                        f"{external_mention_packets} filing packets representing "
                        f"{external_mention_rows} exact activity-text current-bill mention rows, "
                        f"classifying {external_mention_direction_packets} packets with explicit "
                        f"support/opposition text, {external_mention_no_direction_packets} packets "
                        f"without explicit support/opposition text, {external_mention_reference_packets} "
                        f"current-bill issue-reference packets without direction, and "
                        f"{external_mention_advocacy_packets} current-bill issue-advocacy packets "
                        f"without direction; {external_mention_generic_target_packets} packets carry "
                        "generic chamber or agency text references, with no named sponsor/member/committee "
                        "target, committee-action influence, roll-call influence, or outcome-causality evidence."
                    )
                    next_step = (
                        "Use the external LDA mention review to pursue any needed independent contact, "
                        "target, committee-action, roll-call, outcome, and external campaign-finance "
                        "source documents while preserving the no-causal-capture boundary."
                    )
                target_scope_sentence = ""
                if target_scope_review_rows > 0:
                    linked_to += (
                        ", and campaign-finance FEC/OpenFEC target-scope source review"
                    )
                    link_key += (
                        "; bill_finance_lobbying_external_search_review.bill_id -> "
                        "bill_finance_lobbying_campaign_finance_target_scope_review.bill_id"
                    )
                    target_scope_sentence = (
                        f" The bill-finance/lobbying campaign-finance target-scope review covers "
                        f"{target_scope_review_rows} queued public-law rows, "
                        f"{target_scope_context_attachments} candidate/recipient context attachments, "
                        f"{target_scope_transaction_attachments} campaign-finance transaction attachments, "
                        f"{target_scope_unique_recipients} unique public FEC candidate recipients, and "
                        f"{target_scope_unique_transactions} unique raw OpenFEC transactions; "
                        f"all {target_scope_candidate_target_rows} reviewed rows remain public "
                        "candidate/committee/outside-spending scope only, with "
                        f"{target_scope_review_rows - target_scope_no_bill_id_rows} public FEC/OpenFEC "
                        "current-bill ID matches, "
                        f"{target_scope_review_rows - target_scope_no_sponsor_overlap_rows} reviewed bill "
                        "sponsor/candidate overlaps, "
                        f"{target_scope_review_rows - target_scope_no_committee_action_rows} "
                        "committee-of-jurisdiction or committee-action links, and "
                        f"{target_scope_review_rows - target_scope_no_outcome_rows} legislative-outcome or "
                        "influence links."
                    )
                    next_step = (
                        "Use the external LDA mention review and the campaign-finance target-scope review "
                        "to pursue independent contact, target, committee-action, roll-call, outcome, and "
                        "external campaign-finance source documents while preserving the no-causal-capture boundary."
                    )
                committee_action_context_sentence = ""
                if committee_context_rows > 0:
                    linked_to += (
                        ", and queued bill-action committee/floor metadata context"
                    )
                    link_key += (
                        "; bill_finance_lobbying_review_queue.bill_id -> "
                        "bill_finance_lobbying_committee_action_context.bill_id -> "
                        "law_revision_bill_linkage.bill_id"
                    )
                    committee_action_context_sentence = (
                        f" A bill-finance/lobbying committee-action context report joins "
                        f"{committee_context_rows} queued public-law rows to cached public "
                        f"bill-action metadata, including {committee_context_reported_rows} rows "
                        f"with committee-reported flags and {committee_context_floor_rows} rows "
                        f"with floor-considered flags. A follow-on govinfo BILLSTATUS source "
                        f"review fetches {source_review_fetched_rows} official source rows, "
                        f"records committee names for {source_review_committee_rows} rows "
                        f"across {source_review_unique_committees} unique committee/subcommittee "
                        f"names, committee-action records for {source_review_committee_action_rows} "
                        f"rows, floor-action records for {source_review_floor_action_rows} rows, "
                        f"roll-call references for {source_review_roll_call_rows} rows, and "
                        f"public-law outcome metadata for {source_review_public_law_rows} rows. "
                        f"A House Clerk roll-call source review covers {roll_call_source_rows} "
                        f"rows, fetches official roll-call XML for {roll_call_source_fetched_rows} "
                        f"rows with {roll_call_source_bill_match_rows} bill-ID matches, classifies "
                        f"{roll_call_source_no_numbered_rows} rows as floor actions without numbered "
                        f"roll calls, and represents {roll_call_source_member_vote_rows} member-vote "
                        f"rows as source context; "
                        f"it still records {committee_context_action_influence_rows} rows with "
                        "finance/lobbying committee-action influence evidence, "
                        f"{committee_context_roll_call_rows} rows with roll-call influence evidence, "
                        f"and {committee_context_outcome_rows} rows with legislative-outcome causality evidence."
                    )
                    next_step = (
                        "Use the external LDA mention review, campaign-finance target-scope review, "
                        "committee/action context report, and official govinfo source review to "
                        "preserve committee/no-direct-committee source dispositions, pursue direct member target documents, independent "
                        "contact and target documents, outcome-causality evidence, and external "
                        "campaign-finance source documents while preserving the no-causal-capture boundary."
                    )
                member_vote_target_sentence = ""
                if member_vote_target_rows > 0:
                    linked_to += (
                        ", and official member-vote target-scope review"
                    )
                    link_key += (
                        "; bill_finance_lobbying_roll_call_source_review.official_vote_source_url -> "
                        "bill_finance_lobbying_member_vote_target_review.official_vote_source_url; "
                        "bill_finance_lobbying_member_vote_target_review.voter_bioguide_id -> "
                        "campaign_finance_member_context.bioguide_id"
                    )
                    member_vote_target_sentence = (
                        f" A member-vote target-scope review joins {member_vote_target_rows} "
                        f"official House Clerk member-vote rows across {member_vote_target_roll_calls} "
                        f"numbered roll calls and {member_vote_target_bill_rows} queued bills to "
                        "reviewed public FEC/OpenFEC candidate/member target-scope context by Bioguide; "
                        f"it covers {member_vote_target_unique_voters} unique voting Bioguide IDs, "
                        f"records {member_vote_same_bill_overlap_rows} same-bill reviewed campaign "
                        "target Bioguide overlaps, "
                        f"{member_vote_broad_context_rows} broad public FEC candidate/member-context "
                        "overlaps, and still records 0 influence/causality rows."
                    )
                    next_step = (
                        "Use the member-vote target-scope review, source-acquisition queue, and "
                        "external packet reviews to acquire direct member target documents, independent "
                        "contact and target sources, external campaign-finance source documents, and "
                        "outcome-causality evidence while preserving the no-causal-capture boundary."
                    )
                source_acquisition_sentence = ""
                if source_acquisition_rows > 0:
                    linked_to += (
                        ", and a source-acquisition queue for committee/no-direct-committee dispositions, direct member target, outcome, and target-source gaps"
                    )
                    link_key += (
                        "; bill_finance_lobbying_committee_action_context.bill_id -> "
                        "bill_finance_lobbying_source_acquisition_queue.bill_id"
                    )
                    source_acquisition_sentence = (
                        f" A bill-finance/lobbying source-acquisition queue ranks "
                        f"{source_acquisition_rows} queued public-law rows for official "
                        "committee/action, direct member target, outcome, and independent "
                        "target-source follow-up while carrying closed roll-call source-review status; "
                        f"it records {source_acquisition_govinfo_committee_rows} official govinfo "
                        f"committee-name rows, {source_acquisition_govinfo_no_direct_committee_rows} "
                        "official no-direct-committee source-reviewed rows, "
                        f"{source_acquisition_voteview_rows} local Voteview "
                        f"roll-call context rows, {source_acquisition_official_roll_call_rows} official House "
                        f"Clerk roll-call source rows, {source_acquisition_no_numbered_roll_call_rows} "
                        f"floor-action rows without numbered roll calls, {source_acquisition_roll_call_rows} "
                        f"{plural(source_acquisition_roll_call_rows, 'row still needs', 'rows still need')} "
                        f"roll-call source acquisition, {source_acquisition_committee_rows} "
                        f"{plural(source_acquisition_committee_rows, 'row still needs', 'rows still need')} "
                        "committee-of-jurisdiction names/source follow-up, "
                        f"{source_acquisition_lda_priority_rows} rows with external LDA mention "
                        f"packets to prioritize, and {source_acquisition_campaign_priority_rows} "
                        "rows with campaign target-scope review to prioritize."
                    )
                    next_step = (
                        "Use the source-acquisition queue, external LDA mention review, and "
                        "campaign-finance target-scope review to preserve committee/no-direct-committee "
                        "source dispositions, acquire direct member target documents, independent contact "
                        "and target sources, external campaign-finance source documents, and "
                        "outcome-causality evidence while preserving the no-causal-capture boundary."
                    )
                result.append(build_row(
                    source,
                    rows,
                    linked,
                    status_for(linked, len(rows)),
                    linked_to,
                    link_key,
                    f"LDA rows now join to broad local policy-area topic context for {linked_lobbying_rows} rows across {issue_count} issue labels via a documented issue-label crosswalk.{bill_policy_sentence}{bill_mention_sentence}{local_review_sentence}{external_review_sentence}{external_mention_review_sentence}{target_scope_sentence}{committee_action_context_sentence}{member_vote_target_sentence}{source_acquisition_sentence} Stored support/opposition evidence, manual medium directional packet review evidence, manual medium position/activity packet review evidence, disposition/target queue evidence, bill-finance/lobbying local no-current-match review evidence, external LDA current-bill search evidence, external LDA mention-review evidence, campaign-finance target-scope review evidence, committee/action context evidence, member-vote target-scope review evidence, and source-acquisition queue evidence are limited to deterministic stored activity-text signals, source-reviewed activity-text dispositions, source-review priorities, local same-policy no-current-bill-match dispositions, exact activity-text bill-reference evidence, bounded external activity-text packet dispositions, public FEC/OpenFEC candidate/committee/independent-expenditure target fields, cached bill-action flags, official member-vote rows, and official source targets, and there is still no client-to-specific-bill influence linkage, sponsor/member target beyond activity-text references or public target-scope overlaps, committee-action influence, roll-call influence, legislative-outcome causality, or causal influence join; exact filing-text bill mentions, stored activity-text position signals, cached bill/action context, source-reviewed packet dispositions, source-review queues, external LDA search rows, external LDA mention-review rows, FEC/OpenFEC target-scope rows, committee/action context rows, member-vote target-scope rows, and source-acquisition queue rows are identifier, text-signal, metadata, activity-text disposition, local no-current-match, bill-reference, bounded activity-text packet, public candidate target-scope, bill-action-flag, member-vote target-scope, and acquisition-target evidence only, not influence evidence.",
                    next_step,
                ))
                continue
            linked = count_linked_rows(rows, "issue", topic_values)
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Comparative Agendas topic throughput",
                "lobbying_disclosure.issue -> topic_throughput.topic",
                "Fallback linkage uses only identical LDA issue and topic labels; there is no client-to-specific-bill, sponsor, or committee join.",
            ))
        elif family == "OpenFEC campaign finance":
            linked_recipients = metadata_linked_recipients()
            linked = count_linked_rows(rows, "recipient", linked_recipients)
            if linked > 0:
                house_context_rows, house_context_transactions, house_context_districts = (
                    campaign_finance_house_district_summary()
                )
                member_context_rows, member_context_transactions, member_context_members = (
                    campaign_finance_member_context_summary()
                )
                issue_context_rows, issue_context_topics, issue_context_recipients, issue_context_amount = (
                    campaign_finance_issue_context_summary()
                )
                sponsor_context_rows, sponsor_context_transactions, sponsor_context_members, sponsor_context_bills, sponsor_context_enacted = (
                    campaign_finance_sponsor_bill_context_summary()
                )
                (
                    local_review_rows,
                    local_review_campaign_no_match_rows,
                    local_review_lobbying_no_match_rows,
                    local_review_exact_rows,
                    local_review_external_rows,
                    _local_review_no_outcome_rows,
                ) = bill_finance_lobbying_local_context_review_summary()
                (
                    external_review_rows,
                    _external_review_exact_bill_rows,
                    _external_review_exact_activity_rows,
                    _external_review_exact_filing_rows,
                    _external_review_exact_client_rows,
                    _external_review_no_exact_rows,
                    external_review_campaign_pending_rows,
                ) = bill_finance_lobbying_external_search_review_summary()
                (
                    target_scope_review_rows,
                    target_scope_context_attachments,
                    target_scope_transaction_attachments,
                    target_scope_unique_recipients,
                    target_scope_unique_transactions,
                    target_scope_candidate_target_rows,
                    target_scope_no_bill_id_rows,
                    target_scope_no_sponsor_overlap_rows,
                    target_scope_no_committee_action_rows,
                    target_scope_no_outcome_rows,
                ) = bill_finance_lobbying_campaign_finance_target_scope_review_summary()
                (
                    committee_context_rows,
                    committee_context_reported_rows,
                    committee_context_floor_rows,
                    committee_context_name_rows,
                    committee_context_action_influence_rows,
                    committee_context_roll_call_rows,
                    committee_context_outcome_rows,
                    _committee_context_reviewed_source_rows,
                ) = bill_finance_lobbying_committee_action_context_summary()
                (
                    source_review_rows,
                    source_review_fetched_rows,
                    source_review_committee_rows,
                    source_review_committee_action_rows,
                    source_review_floor_action_rows,
                    source_review_roll_call_rows,
                    source_review_public_law_rows,
                    source_review_unique_committees,
                ) = bill_finance_lobbying_committee_action_source_review_summary()
                (
                    roll_call_source_rows,
                    roll_call_source_fetched_rows,
                    roll_call_source_bill_match_rows,
                    roll_call_source_no_numbered_rows,
                    roll_call_source_member_vote_rows,
                ) = bill_finance_lobbying_roll_call_source_review_summary()
                (
                    member_vote_target_rows,
                    member_vote_target_roll_calls,
                    member_vote_target_unique_voters,
                    member_vote_same_bill_overlap_rows,
                    member_vote_broad_context_rows,
                    member_vote_target_bill_rows,
                ) = bill_finance_lobbying_member_vote_target_review_summary()
                (
                    source_acquisition_rows,
                    source_acquisition_govinfo_committee_rows,
                    source_acquisition_govinfo_no_direct_committee_rows,
                    source_acquisition_voteview_rows,
                    source_acquisition_official_roll_call_rows,
                    source_acquisition_no_numbered_roll_call_rows,
                    source_acquisition_roll_call_rows,
                    source_acquisition_committee_rows,
                    source_acquisition_lda_priority_rows,
                    source_acquisition_campaign_priority_rows,
                ) = bill_finance_lobbying_source_acquisition_queue_summary()
                linked_to = "FEC committee/candidate metadata and bounded House-candidate district public-opinion context"
                link_key = "campaign_finance.recipient -> campaign_finance_linkage.recipient; candidate_office_state/candidate_office_district -> district_public_opinion.district_id"
                member_sentence = ""
                member_next_step = "Add candidate-to-member/sponsor, issue-topic, committee-of-jurisdiction, outside-spending-target, and bill-outcome joins without exposing private contributor information."
                linkage_status = "metadata linked"
                issue_sentence = ""
                sponsor_sentence = ""
                local_review_sentence = ""
                external_review_sentence = ""
                target_scope_sentence = ""
                committee_action_context_sentence = ""
                member_vote_target_sentence = ""
                if member_context_rows > 0:
                    linked_to = (
                        "FEC committee/candidate metadata, bounded Voteview member context, "
                        "and bounded House-candidate district public-opinion context"
                    )
                    link_key = (
                        "campaign_finance.recipient -> campaign_finance_linkage.recipient; "
                        "campaign_finance_linkage.candidate_id -> campaign_finance_member_context.candidate_id -> voteview_member_context.bioguide_id; "
                        "candidate_office_state/candidate_office_district -> district_public_opinion.district_id"
                    )
                    member_sentence = (
                        f" A bounded candidate subset also joins to Voteview member context for {member_context_transactions} "
                        f"transaction rows across {member_context_rows} candidate recipients and {member_context_members} Bioguide members."
                    )
                    member_next_step = "Add issue-topic, committee-of-jurisdiction, outside-spending-target, bill-identifier, and legislative-outcome joins without exposing private contributor information."
                    linkage_status = "partially linked"
                if issue_context_rows > 0:
                    linked_to = (
                        "FEC committee/candidate metadata, bounded transaction-label issue-topic context, "
                        "bounded Voteview member context, and bounded House-candidate district public-opinion context"
                    )
                    link_key = (
                        link_key
                        + "; campaign_finance.source_id -> campaign_finance_issue_context.source_id "
                        "-> topic_throughput.topic"
                    )
                    issue_sentence = (
                        f" A bounded transaction-label subset maps to broad local policy-area topic context for "
                        f"{issue_context_rows} transaction rows across {issue_context_topics} topics and "
                        f"{issue_context_recipients} recipients, representing {issue_context_amount:.2f} in sampled "
                        "transaction amount; this is issue-topic context only."
                    )
                    member_next_step = "Add bill identifiers, committees of jurisdiction, reviewed outside-spending targets, and legislative-outcome joins without exposing private contributor information."
                    linkage_status = "partially linked"
                if sponsor_context_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and bounded candidate-to-sponsored-bill context"
                    )
                    link_key = (
                        link_key
                        + "; campaign_finance_member_context.bioguide_id -> "
                        "campaign_finance_sponsor_bill_context.bioguide_id -> "
                        "govinfo_billstatus_linkage.sponsor_bioguide_id"
                    )
                    sponsor_sentence = (
                        f" A bounded candidate-to-sponsored-bill subset joins to cached govinfo bill metadata for "
                        f"{sponsor_context_transactions} transaction rows across {sponsor_context_rows} candidate "
                        f"recipients, {sponsor_context_members} Bioguide members, {sponsor_context_bills} bill IDs, "
                        f"and {sponsor_context_enacted} enacted bill IDs; this is sponsored-bill context only."
                    )
                    member_next_step = (
                        "Scale bill identifiers beyond the bounded candidate/sponsor overlap, add reviewed "
                        "outside-spending targets and committees of jurisdiction, and distinguish committee metadata from committee-action "
                        "influence without exposing private contributor information."
                    )
                    linkage_status = "partially linked"
                if local_review_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and local bill-finance/lobbying no-current-match review for queued public-law rows"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_review_queue.bill_id -> "
                        "bill_finance_lobbying_local_context_review.bill_id"
                    )
                    local_review_sentence = (
                        f" The bill-finance/lobbying local-context review covers {local_review_rows} queued "
                        f"public-law rows, including {local_review_campaign_no_match_rows} rows with same-policy "
                        "campaign-finance context and no current-bill exact match, "
                        f"{local_review_lobbying_no_match_rows} rows with same-policy lobbying context and no "
                        "current-bill exact match, "
                        f"{local_review_exact_rows} local current-bill exact matches, and "
                        f"{local_review_external_rows} rows still requiring external target/source expansion; "
                        "this is local no-current-match context only."
                    )
                    member_next_step = (
                        "Run external current-bill campaign-finance and lobbying target/source expansion for the "
                        "reviewed no-current-match queue, then add reviewed outside-spending targets, committees "
                        "of jurisdiction, and legislative-outcome context without exposing private contributor information."
                    )
                if external_review_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and FEC/OpenFEC source-scope triage for queued bill-finance rows"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_local_context_review.bill_id -> "
                        "bill_finance_lobbying_external_search_review.bill_id"
                    )
                    external_review_sentence = (
                        f" The external-search review marks {external_review_campaign_pending_rows} queued rows "
                        "for campaign-finance candidate/committee/outside-spending target-scope review and records "
                        "that public FEC/OpenFEC records expose candidate, committee, receipt, and independent-expenditure "
                        "target fields, not bill IDs or bill-specific campaign-finance influence."
                    )
                    member_next_step = (
                        "Use the bill-finance/lobbying external-search review to run public FEC/OpenFEC "
                        "candidate, committee, and outside-spending target-scope review for the queued "
                        "campaign-finance rows, then add committees of jurisdiction and legislative-outcome "
                        "context without exposing private contributor information."
                    )
                if target_scope_review_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and FEC/OpenFEC target-scope source review for queued bill-finance rows"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_external_search_review.bill_id -> "
                        "bill_finance_lobbying_campaign_finance_target_scope_review.bill_id"
                    )
                    target_scope_sentence = (
                        f" The bill-finance/lobbying campaign-finance target-scope review covers "
                        f"{target_scope_review_rows} queued public-law rows, "
                        f"{target_scope_context_attachments} candidate/recipient context attachments, "
                        f"{target_scope_transaction_attachments} campaign-finance transaction attachments, "
                        f"{target_scope_unique_recipients} unique public FEC candidate recipients, and "
                        f"{target_scope_unique_transactions} unique raw OpenFEC transactions; "
                        f"all {target_scope_candidate_target_rows} reviewed rows remain public "
                        "candidate/committee/outside-spending scope only, with "
                        f"{target_scope_review_rows - target_scope_no_bill_id_rows} public FEC/OpenFEC "
                        "current-bill ID matches, "
                        f"{target_scope_review_rows - target_scope_no_sponsor_overlap_rows} reviewed bill "
                        "sponsor/candidate overlaps, "
                        f"{target_scope_review_rows - target_scope_no_committee_action_rows} "
                        "committee-of-jurisdiction or committee-action links, and "
                        f"{target_scope_review_rows - target_scope_no_outcome_rows} legislative-outcome or "
                        "influence links."
                    )
                    member_next_step = (
                        "Pursue external campaign target/source documents, committees of jurisdiction, "
                        "committee-action records, roll-call context, and legislative outcomes before making "
                        "any bill-specific campaign-finance influence claim."
                    )
                if committee_context_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and queued public-law bill-action committee/floor metadata context"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_review_queue.bill_id -> "
                        "bill_finance_lobbying_committee_action_context.bill_id -> "
                        "law_revision_bill_linkage.bill_id"
                    )
                    committee_action_context_sentence = (
                        f" A bill-finance/lobbying committee-action context report joins "
                        f"{committee_context_rows} queued public-law rows to cached public "
                        f"bill-action metadata, including {committee_context_reported_rows} rows "
                        f"with committee-reported flags and {committee_context_floor_rows} rows "
                        f"with floor-considered flags. A follow-on govinfo BILLSTATUS source "
                        f"review fetches {source_review_fetched_rows} official source rows, "
                        f"records committee names for {source_review_committee_rows} rows "
                        f"across {source_review_unique_committees} unique committee/subcommittee "
                        f"names, committee-action records for {source_review_committee_action_rows} "
                        f"rows, floor-action records for {source_review_floor_action_rows} rows, "
                        f"roll-call references for {source_review_roll_call_rows} rows, and "
                        f"public-law outcome metadata for {source_review_public_law_rows} rows. "
                        f"A House Clerk roll-call source review covers {roll_call_source_rows} "
                        f"rows, fetches official roll-call XML for {roll_call_source_fetched_rows} "
                        f"rows with {roll_call_source_bill_match_rows} bill-ID matches, classifies "
                        f"{roll_call_source_no_numbered_rows} rows as floor actions without numbered "
                        f"roll calls, and represents {roll_call_source_member_vote_rows} member-vote "
                        f"rows as source context; "
                        f"it still records {committee_context_action_influence_rows} rows with "
                        "campaign-finance or lobbying committee-action influence evidence, "
                        f"{committee_context_roll_call_rows} rows with roll-call influence evidence, "
                        f"and {committee_context_outcome_rows} rows with legislative-outcome causality evidence."
                    )
                    member_next_step = (
                        "Use the committee/action context report and official govinfo source review "
                        "to preserve committee/no-direct-committee source dispositions, acquire "
                        "direct member target documents, legislative outcomes and outcome-"
                        "causality evidence, external campaign target/source documents, and "
                        "independent finance/lobbying target documents before making any bill-"
                        "specific campaign-finance influence claim."
                    )
                if member_vote_target_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and official member-vote target-scope review"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_roll_call_source_review.official_vote_source_url -> "
                        "bill_finance_lobbying_member_vote_target_review.official_vote_source_url; "
                        "bill_finance_lobbying_member_vote_target_review.voter_bioguide_id -> "
                        "campaign_finance_member_context.bioguide_id"
                    )
                    member_vote_target_sentence = (
                        f" A member-vote target-scope review joins {member_vote_target_rows} "
                        f"official House Clerk member-vote rows across {member_vote_target_roll_calls} "
                        f"numbered roll calls and {member_vote_target_bill_rows} queued bills to "
                        "reviewed public FEC/OpenFEC candidate/member target-scope context by Bioguide; "
                        f"it covers {member_vote_target_unique_voters} unique voting Bioguide IDs, "
                        f"records {member_vote_same_bill_overlap_rows} same-bill reviewed campaign "
                        "target Bioguide overlaps, "
                        f"{member_vote_broad_context_rows} broad public FEC candidate/member-context "
                        "overlaps, and still records 0 influence/causality rows."
                    )
                    member_next_step = (
                        "Use the member-vote target-scope review and source-acquisition queue to "
                        "acquire direct member target documents, external campaign target/source "
                        "documents, independent lobbying target/contact sources, and legislative "
                        "outcomes and outcome-causality evidence before making any bill-specific "
                        "campaign-finance influence claim."
                    )
                source_acquisition_sentence = ""
                if source_acquisition_rows > 0:
                    linked_to = (
                        linked_to
                        + ", and source-acquisition targets for committee/no-direct-committee dispositions, direct member target, outcome, and target-source gaps"
                    )
                    link_key = (
                        link_key
                        + "; bill_finance_lobbying_committee_action_context.bill_id -> "
                        "bill_finance_lobbying_source_acquisition_queue.bill_id"
                    )
                    source_acquisition_sentence = (
                        f" A bill-finance/lobbying source-acquisition queue ranks "
                        f"{source_acquisition_rows} queued public-law rows for official "
                        "committee/action, direct member target, outcome, and independent "
                        "target-source follow-up while carrying closed roll-call source-review status; "
                        f"it records {source_acquisition_govinfo_committee_rows} official govinfo "
                        f"committee-name rows, {source_acquisition_govinfo_no_direct_committee_rows} "
                        "official no-direct-committee source-reviewed rows, "
                        f"{source_acquisition_voteview_rows} local Voteview "
                        f"roll-call context rows, {source_acquisition_official_roll_call_rows} official House "
                        f"Clerk roll-call source rows, {source_acquisition_no_numbered_roll_call_rows} "
                        f"floor-action rows without numbered roll calls, {source_acquisition_roll_call_rows} "
                        f"{plural(source_acquisition_roll_call_rows, 'row still needs', 'rows still need')} "
                        f"roll-call source acquisition, {source_acquisition_committee_rows} "
                        f"{plural(source_acquisition_committee_rows, 'row still needs', 'rows still need')} "
                        "committee-of-jurisdiction names/source follow-up, "
                        f"{source_acquisition_lda_priority_rows} rows with external LDA mention "
                        f"packets to prioritize, and {source_acquisition_campaign_priority_rows} "
                        "rows with campaign target-scope review to prioritize."
                    )
                    member_next_step = (
                        "Use the source-acquisition queue to preserve committee/no-direct-committee "
                        "source dispositions and acquire direct member target documents, external "
                        "campaign target/source documents, independent lobbying target/contact "
                        "sources, and legislative outcomes and outcome-causality evidence before making any bill-specific campaign-finance "
                        "influence claim."
                    )
                result.append(build_row(
                    source,
                    rows,
                    linked,
                    linkage_status,
                    linked_to,
                    link_key,
                    "Recipient IDs now join to public FEC committee or candidate metadata, and a bounded House-candidate subset "
                    f"({house_context_transactions} transaction rows across {house_context_rows} recipients and {house_context_districts} districts) "
                    "joins to district public-opinion context."
                    f"{member_sentence}{issue_sentence}{sponsor_sentence}{local_review_sentence}{external_review_sentence}{target_scope_sentence}{committee_action_context_sentence}{member_vote_target_sentence}{source_acquisition_sentence} These rows still do not prove campaign-finance influence, bill-specific campaign-finance targeting, lobbying influence, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, or causal capture.",
                    member_next_step,
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "Campaign-finance rows have recipient and industry fields but no bill, sponsor, committee, district, or issue join in the current extract.",
                "Link committees and candidates to sponsors, districts, issues, outside-spending targets, and bill outcomes.",
            ))
        elif family == "Center for Effective Lawmaking and sponsor histories":
            if sponsor_matched_rows > 0:
                result.append(build_row(
                    source,
                    rows,
                    sponsor_matched_rows,
                    "metadata linked" if sponsor_matched_rows == len(rows) else "partially linked",
                    "govinfo BILLSTATUS sponsor metadata and bounded Congress.gov public-law bill/action metadata",
                    "sponsor_success.sponsor_id -> sponsor_bill_linkage.sponsor_id -> govinfo_billstatus_linkage.sponsor_bioguide_id",
                    f"Sponsor aggregate rows now join by Bioguide sponsor ID to bounded public bill metadata for {sponsor_matched_rows} / {len(rows)} sponsor rows, covering {sponsor_unique_bills} unique matched bill IDs, {sponsor_attached_bill_links} attached bill links, {sponsor_attached_enacted_links} attached enacted bill links, and {sponsor_public_laws} public-law overlaps. This is sponsor-to-bill metadata only; it is not full Center for Effective Lawmaking data, complete sponsor histories, legislative effectiveness, bill quality, public benefit, welfare, causal influence, or model validation evidence.",
                    "Replace the bounded sponsor aggregate with complete sponsor histories or licensed CEL-style effectiveness data, and connect sponsor bills to roll calls, committees, issues, district opinion, finance, lobbying, and outcomes.",
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "Sponsor-success rows have sponsor IDs, but the bounded sponsor-bill linkage cache is not present in this run, so no member-to-bill metadata join is available.",
                "Run make build-sponsor-bill-linkage-raw for the bounded metadata cache, then replace the aggregate with complete sponsor histories that preserve member and bill identifiers.",
            ))
        elif family == "District public opinion and affected groups":
            linked = count_linked_rows(rows, "issue", topic_values)
            if linked <= 0:
                metadata_linked = count_linked_district_opinion_rows(rows)
                if metadata_linked > 0:
                    policy_context_rows, policy_context_keys, policy_context_bills, policy_context_topics = (
                        district_opinion_policy_context_summary()
                    )
                    readiness_rows, readiness_proxy_only, readiness_issue_rows, readiness_affected_rows = (
                        district_opinion_bill_topic_readiness_summary()
                    )
                    source_packet_rows, source_packet_only_rows, source_packet_policy_areas = (
                        district_opinion_source_packet_summary()
                    )
                    (
                        denominator_packet_rows,
                        denominator_matched_packets,
                        denominator_districts,
                        denominator_population,
                        denominator_housing_units,
                    ) = district_opinion_census_denominator_summary()
                    (
                        acs_packet_rows,
                        acs_matched_packets,
                        acs_districts,
                        acs_population,
                        acs_veterans,
                        acs_noncitizens,
                        acs_below_poverty,
                        acs_no_internet,
                    ) = district_opinion_acs_context_summary()
                    (
                        survey_crosswalk_rows,
                        survey_crosswalk_no_item_rows,
                        survey_crosswalk_source_families,
                    ) = district_opinion_survey_source_crosswalk_summary()
                    (
                        survey_item_proxy_review_rows,
                        survey_item_proxy_reviewed_rows,
                        survey_item_proxy_bill_topic_item_rows,
                        survey_item_proxy_policy_areas,
                    ) = district_opinion_survey_item_proxy_review_summary()
                    (
                        ces_policy_candidate_rows,
                        ces_policy_candidate_found_rows,
                        ces_policy_candidate_missing_rows,
                        ces_policy_candidate_unique_items,
                        ces_policy_candidate_policy_areas,
                        _ces_policy_candidate_source_variables,
                    ) = district_opinion_ces_policy_item_candidate_review_summary()
                    (
                        ces_policy_distribution_rows,
                        ces_policy_distribution_found_rows,
                        ces_policy_distribution_missing_rows,
                        ces_policy_distribution_unique_items,
                        ces_policy_distribution_years,
                        ces_policy_distribution_observations,
                    ) = district_opinion_ces_policy_item_response_distribution_summary()
                    (
                        ces_policy_codebook_rows,
                        ces_policy_codebook_found_rows,
                        ces_policy_codebook_missing_rows,
                        ces_policy_codebook_binary_rows,
                        ces_policy_codebook_unique_items,
                        ces_policy_codebook_binary_items,
                        ces_policy_codebook_direction_types,
                    ) = district_opinion_ces_policy_item_codebook_direction_summary()
                    (
                        bill_item_review_rows,
                        bill_item_positive_alignments,
                        bill_item_negative_dispositions,
                        bill_topic_support_rows,
                        bill_topic_support_bills,
                        bill_topic_support_districts,
                        bill_topic_support_items,
                        bill_topic_support_years,
                        bill_topic_support_respondents,
                    ) = district_opinion_bill_item_support_summary()
                    linked_to = "Congress.gov member endpoint and public-law bill sponsor metadata"
                    link_key = "district_public_opinion.district_id -> district_public_opinion_linkage.district_id; district_public_opinion_linkage.bill_id -> law_revision_bill_linkage.bill_id"
                    policy_sentence = ""
                    readiness_sentence = ""
                    source_packet_sentence = ""
                    denominator_sentence = ""
                    acs_sentence = ""
                    survey_crosswalk_sentence = ""
                    survey_item_proxy_sentence = ""
                    ces_policy_candidate_sentence = ""
                    ces_policy_distribution_sentence = ""
                    ces_policy_codebook_sentence = ""
                    bill_item_support_sentence = ""
                    next_step = "Add bill-topic public-opinion mapping, MRP or small-area estimates where needed, and ACS or comparable affected-population joins."
                    if policy_context_rows > 0:
                        linked_to = (
                            "Congress.gov member endpoint, public-law bill sponsor metadata, "
                            "and bounded bill policy-area topic context"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_linkage.policy_area -> "
                            "district_public_opinion_policy_context.policy_area -> topic_throughput.topic"
                        )
                        policy_sentence = (
                            f" A bounded policy-context report maps {policy_context_rows} sponsor-district "
                            f"public-law context rows, representing {policy_context_keys} unique district-opinion "
                            f"row keys and {policy_context_bills} public-law bills, to {policy_context_topics} "
                            "local bill policy areas. These are bill policy-area context rows only, not "
                            "issue-specific public-support estimates."
                        )
                        next_step = (
                            "Add issue-specific bill-support mapping, MRP or small-area estimates where needed, "
                            "and ACS or comparable affected-population joins."
                        )
                    if readiness_rows > 0:
                        linked_to = (
                            linked_to
                            + ", with bill-topic public-opinion and affected-group readiness queue"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_policy_context.bill_id -> "
                            "district_public_opinion_bill_topic_readiness.bill_id"
                        )
                        readiness_sentence = (
                            f" A bill-topic readiness report queues {readiness_rows} public-law bills, "
                            f"including {readiness_proxy_only} still proxy-only for bill-topic support, "
                            f"{readiness_issue_rows} issue-specific support rows, and "
                            f"{readiness_affected_rows} affected-group support or harm rows."
                        )
                        next_step = (
                            "Use the district public-opinion bill-topic readiness queue to add issue-specific "
                            "bill-support mapping, MRP or small-area estimates where needed, and ACS or "
                            "comparable affected-population joins."
                        )
                    if source_packet_rows > 0:
                        linked_to = linked_to + ", and public-opinion source-acquisition packets"
                        link_key = (
                            link_key
                            + "; district_public_opinion_bill_topic_readiness.bill_id -> "
                            "district_public_opinion_source_packets.bill_id"
                        )
                        source_packet_sentence = (
                            f" A source-packet report maps those rows to {source_packet_rows} "
                            f"source-acquisition packets across {source_packet_policy_areas} policy areas, "
                            f"with {source_packet_only_rows} packets still carrying no acquired external "
                            "bill-topic dataset."
                        )
                        next_step = (
                            "Use the district public-opinion source packets to acquire or build issue-specific "
                            "survey-item crosswalks, MRP or small-area estimates where needed, and ACS or "
                            "comparable affected-population joins."
                        )
                    if denominator_packet_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and Census/TIGERweb population-housing denominators"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_source_packets.sponsor_districts -> "
                            "district_public_opinion_census_denominators.district_id"
                        )
                        denominator_sentence = (
                            f" A Census population-housing denominators layer joins "
                            f"{denominator_matched_packets} / {denominator_packet_rows} source packets "
                            f"to 2020 TIGERweb population and housing-unit denominators across "
                            f"{denominator_districts} unique "
                            f"sponsor districts, summing to {denominator_population} packet-level "
                            f"population denominator and {denominator_housing_units} packet-level "
                            "housing-unit denominator counts."
                        )
                        next_step = (
                            "Use the district public-opinion source packets with the Census district "
                            "denominator layer as the sponsor-district frame, then add ACS "
                            "policy-specific affected-population detail, issue-specific survey-item "
                            "crosswalks, and MRP or small-area estimates where needed."
                        )
                    if acs_packet_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and ACS 2017-2021 broad district context"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_source_packets.sponsor_districts -> "
                            "district_public_opinion_acs_context.matched_acs_context_districts"
                        )
                        acs_sentence = (
                            f" An ACS context layer joins {acs_matched_packets} / {acs_packet_rows} "
                            f"source packets to official 2017-2021 ACS 5-year broad demographic, "
                            f"economic, citizenship, language, disability, internet, and veteran "
                            f"context across {acs_districts} unique sponsor districts, with "
                            f"packet-level context totals of {acs_population} population, "
                            f"{acs_veterans} veterans, {acs_noncitizens} noncitizens, "
                            f"{acs_below_poverty} below poverty, and {acs_no_internet} "
                            "households without internet access. This is broad district context only, "
                            "not bill-topic support, MRP, bill-text-specific affected-population "
                            "definitions, affected-group support or harm, or model validation."
                        )
                        next_step = (
                            "Use the district public-opinion source packets plus the Census denominator "
                            "and ACS district-context layers as the sponsor-district frame, then add "
                            "issue-specific survey-item crosswalks, MRP or small-area estimates where "
                            "needed, and bill-text-specific affected-population, support, and harm sources."
                        )
                    if survey_crosswalk_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and official survey-source crosswalk planning"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_source_packets.bill_id -> "
                            "district_public_opinion_survey_source_crosswalk.bill_id"
                        )
                        survey_crosswalk_sentence = (
                            f" A survey-source crosswalk maps {survey_crosswalk_rows} source packets "
                            f"to official survey/source families and candidate item-search terms "
                            f"across {survey_crosswalk_source_families} source families, with "
                            f"{survey_crosswalk_no_item_rows} rows still carrying no acquired survey "
                            "item IDs, MRP estimates, or bill-topic support values."
                        )
                        next_step = (
                            "Use the district public-opinion source packets and survey-source crosswalk "
                            "with the Census denominator and ACS district-context layers to acquire exact "
                            "questionnaires, survey years, item IDs, and microdata, then build or import "
                            "MRP/small-area estimates and bill-text-specific affected-population, support, "
                            "and harm sources."
                        )
                    if survey_item_proxy_review_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and exact current CES proxy-variable review"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_survey_source_crosswalk.bill_id -> "
                            "district_public_opinion_survey_item_proxy_review.bill_id"
                        )
                        survey_item_proxy_sentence = (
                            f" A survey item proxy-review layer attaches exact current CES proxy "
                            f"variable IDs to {survey_item_proxy_review_rows} queued packet rows "
                            f"across {survey_item_proxy_policy_areas} policy areas; "
                            f"{survey_item_proxy_reviewed_rows} rows document current proxy variables, "
                            f"while {survey_item_proxy_bill_topic_item_rows} rows carry acquired "
                            "bill-topic survey item IDs."
                        )
                        next_step = (
                            "Use the district public-opinion source packets, survey-source crosswalk, "
                            "Census denominator layer, ACS district-context layer, and survey item "
                            "proxy review to distinguish existing exact CES proxy variables from "
                            "missing bill-topic survey items, then acquire exact questionnaires, "
                            "survey years, bill-topic item IDs, microdata, MRP/small-area estimates, "
                            "and bill-text-specific affected-population, support, and harm sources."
                        )
                    if ces_policy_candidate_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and official CES policy-preference candidate-item review"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_survey_source_crosswalk.policy_area -> "
                            "district_public_opinion_ces_policy_item_candidate_review.policy_area"
                        )
                        ces_policy_candidate_sentence = (
                            f" An official CES policy-preference candidate-item review maps "
                            f"{ces_policy_candidate_found_rows} / {ces_policy_candidate_rows} "
                            "queued packet rows to exact Cumulative CES Policy Preferences "
                            f"variable IDs across {ces_policy_candidate_policy_areas} policy areas, "
                            f"attaching {ces_policy_candidate_unique_items} unique candidate variable IDs "
                            f"and leaving {ces_policy_candidate_missing_rows} packet rows without a "
                            "candidate item in that source; it still records 0 exact bill-topic support "
                            "estimates and 0 MRP/small-area estimates."
                        )
                        next_step = (
                            "Use the district public-opinion source packets, survey-source crosswalk, "
                            "Census denominator layer, ACS district-context layer, survey item proxy "
                            "review, and CES policy-preference candidate-item review to source-review "
                            "candidate variable wording against bill text, then acquire exact "
                            "questionnaires, respondent geography, microdata, MRP/small-area estimates, "
                            "and bill-text-specific affected-population, support, and harm sources."
                        )
                    if ces_policy_distribution_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and official CES policy-preference raw response-code distribution review"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_ces_policy_item_candidate_review.bill_id -> "
                            "district_public_opinion_ces_policy_item_response_distribution_review.bill_id"
                        )
                        ces_policy_distribution_sentence = (
                            " A raw response-distribution review joins "
                            f"{ces_policy_distribution_found_rows} / {ces_policy_distribution_rows} "
                            "queued packet rows to unweighted Cumulative CES Policy Preferences "
                            f"response-code distributions across {ces_policy_distribution_unique_items} "
                            f"candidate variable IDs and {ces_policy_distribution_years} source years, "
                            f"with {ces_policy_distribution_observations} packet-level attached "
                            "item-response observations; shared candidate variables are counted once "
                            "per packet. It still records 0 exact bill-topic support estimates, "
                            "0 directionally recoded support/opposition estimates, and 0 "
                            "MRP/small-area estimates."
                        )
                        next_step = (
                            "Use the district public-opinion source packets, survey-source crosswalk, "
                            "Census denominator layer, ACS district-context layer, survey item proxy "
                            "review, CES policy-preference candidate-item review, and raw response-code "
                            "distribution review to source-review candidate wording and codebook "
                            "response-code direction against bill text, then acquire respondent geography, "
                            "microdata, MRP/small-area estimates, and bill-text-specific "
                            "affected-population, support, and harm sources."
                        )
                    if ces_policy_codebook_rows > 0:
                        linked_to = (
                            linked_to
                            + ", and official CES policy-preference codebook response-direction review"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_ces_policy_item_response_distribution_review.bill_id -> "
                            "district_public_opinion_ces_policy_item_codebook_direction_review.bill_id"
                        )
                        ces_policy_codebook_sentence = (
                            " A codebook response-direction review joins "
                            f"{ces_policy_codebook_found_rows} / {ces_policy_codebook_rows} "
                            "queued packet rows to official Cumulative CES Policy Preferences guide "
                            f"response labels across {ces_policy_codebook_unique_items} attached "
                            f"candidate variable IDs and {ces_policy_codebook_direction_types} "
                            "direction types, including "
                            f"{ces_policy_codebook_binary_rows} packet rows and "
                            f"{ces_policy_codebook_binary_items} unique candidate variables with "
                            "item-wording support/oppose code labels; "
                            f"{ces_policy_codebook_missing_rows} packet rows still have no candidate "
                            "item in that source. It still records 0 bill-text direction-alignment "
                            "rows, 0 exact bill-topic support estimates, and 0 MRP/small-area "
                            "estimates."
                        )
                        next_step = (
                            "Use the district public-opinion source packets, survey-source crosswalk, "
                            "Census denominator layer, ACS district-context layer, survey item proxy "
                            "review, CES policy-preference candidate-item review, raw response-code "
                            "distribution review, and codebook response-direction review to source-review "
                            "candidate item wording and item direction against bill text, then acquire "
                            "respondent geography, microdata, MRP/small-area estimates, and "
                            "bill-text-specific affected-population, support, and harm sources."
                        )
                    if bill_topic_support_rows > 0:
                        linked_to = (
                            linked_to
                            + ", source-reviewed official bill-text alignment, and privacy-thresholded historical district issue support"
                        )
                        link_key = (
                            link_key
                            + "; district_public_opinion_bill_item_alignment_review.bill_id + "
                            "selected_variable_ids -> district_public_opinion_bill_topic_support.bill_id + survey_item_id; "
                            "sponsor_districts -> sponsor_district_id"
                        )
                        bill_item_support_sentence = (
                            f" An official bill-text review covers {bill_item_review_rows} public-law "
                            f"packets, retains {bill_item_positive_alignments} historical related-issue "
                            f"alignment, and preserves {bill_item_negative_dispositions} negative "
                            "dispositions against forced policy-area matches. The retained alignment "
                            f"produces {bill_topic_support_rows} privacy-thresholded annual direct-weighted "
                            f"district estimates across {bill_topic_support_bills} bill, "
                            f"{bill_topic_support_districts} district, {bill_topic_support_items} item, "
                            f"and {bill_topic_support_years} years, representing "
                            f"{bill_topic_support_respondents} published aggregate responses. "
                            "The item is directionally related to the bill but predates enactment and "
                            "does not use the bill wording."
                        )
                        next_step = (
                            "Use the source packets, survey-source crosswalk, ACS district-context, proxy review, "
                            "candidate-item review, response-code distribution review, codebook review, official "
                            "bill text, and retained historical related-issue estimates as the bounded frame; then "
                            "add exact or closer contemporaneous bill-topic questions, design-based uncertainty or "
                            "MRP where needed, and bill-text-specific affected-population, support, and harm evidence."
                        )
                    result.append(build_row(
                        source,
                        rows,
                        metadata_linked,
                        "partially linked" if bill_topic_support_rows > 0 else "metadata linked",
                        linked_to,
                        link_key,
                        "District public-opinion rows now join to House-sponsored public-law bill metadata by sponsor district, with support and affected-group-share fields kept separate."
                        + policy_sentence
                        + readiness_sentence
                        + source_packet_sentence
                        + denominator_sentence
                        + acs_sentence
                        + survey_crosswalk_sentence
                        + survey_item_proxy_sentence
                        + ces_policy_candidate_sentence
                        + ces_policy_distribution_sentence
                        + ces_policy_codebook_sentence
                        + bill_item_support_sentence
                        + " The historical related-issue estimates are not exact or contemporaneous bill support, MRP, design-based uncertainty estimates, bill-text-specific affected-population detail, affected-group harm, representative responsiveness, public-benefit validation, or model validation.",
                        next_step,
                    ))
                    continue
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Comparative Agendas topic throughput",
                "district_public_opinion.issue -> topic_throughput.topic",
                "Current district-opinion issue labels are broad survey proxies and do not join to bill topics, bill IDs, affected groups, or sponsors.",
                "Add issue-to-bill mapping, MRP/small-area estimates where needed, and ACS affected-population joins.",
            ))
        elif family == "Committee hearing markup referral and discharge records":
            linked = count_linked_rows(rows, "issue", topic_values)
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Comparative Agendas topic throughput",
                "committee_activity.issue -> topic_throughput.topic",
                "Committee rows join to the current topic labels, but the source is still a thin Congress.gov-derived summary without independent hearing, markup, or amendment records.",
            ))
        elif family == "Court review and invalidation":
            if court_authority_overlap_rows > 0:
                result.append(build_row(
                    source,
                    rows,
                    court_authority_overlap_rows,
                    status_for(court_authority_overlap_rows, len(rows)),
                    "SCDB lawMinor U.S.C. sections and Federal Register authority-search public-law metadata",
                    "court_review.usc_sections -> court_law_linkage.matched_usc_sections -> rulemaking_authority_linkage.usc_citations",
                    f"SCDB merits-case rows now preserve lawType/lawSupp/lawMinor metadata; {court_usc_rows} rows have parsed U.S.C. sections, and {court_authority_overlap_rows} rows overlap Federal Register authority U.S.C. citations attached to {court_public_laws} cached public-law rows and {court_bill_ids} bill IDs across {court_usc_sections} normalized sections. This is statute-section authority-overlap metadata only; it is not proof that the case directly challenged, reviewed, or invalidated the listed public law, bill, agency rule, or implementation chain.",
                    "Add direct case-to-statute/public-law identifiers, lower-court or emergency-order coding, and reviewed links from challenged laws to bill and implementation records.",
                ))
                continue
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "SCDB rows use case-centered issue codes and are not joined to public laws, bills, agencies, emergency orders, or implementation records.",
                "Add public-law/statute identifiers, lower-court or emergency-order coding, and links from challenged laws to bill and implementation records.",
            ))
        elif family == "Rulemaking implementation and enforcement":
            linked = count_linked_rows(rows, "law_id", public_law_values)
            if linked <= 0:
                metadata_linked = count_linked_rows(rows, "law_id", metadata_linked_rulemaking_document_numbers())
                if metadata_linked > 0:
                    result.append(build_row(
                        source,
                        rows,
                        metadata_linked,
                        "metadata linked",
                        "Federal Register single-document endpoint, Federal Register-exposed Regulations.gov metadata, bounded public-law authority search, bounded proposed-rule history search, bounded Regulations.gov comment-record metadata, and sanitized public comment-detail review",
                        "rulemaking_implementation.law_id -> rulemaking_implementation_linkage.document_number; rulemaking_authority_linkage.matched_document_numbers -> rulemaking_history_linkage.final_document_number; rulemaking_comment_records.docket_id -> rulemaking_comment_metadata final/proposed docket IDs; rulemaking_comment_text_review.comment_id -> rulemaking_comment_records.retrieved_comment_ids",
                        f"Final-rule rows now join to official Federal Register document metadata, including docket IDs, RINs, CFR references, agency identifiers, and Federal Register-exposed Regulations.gov docket or comment-count metadata when present. A separate Federal Register authority-search cache text-verifies public-law mentions for {authority_matched_rows} / {authority_total_rows} cached public-law rows across {authority_verified_docs} rule documents; the proposed-history cache links {history_matched_final_rows} / {history_total_final_rows} authority-matched final-rule rows to {history_proposed_links} proposed-rule records ({history_unique_proposed_docs} unique documents) when RIN or docket identifiers match. The comment-record cache classifies {comment_record_docket_rows} public-law/docket rows, including {complete_comment_record_docket_rows} complete bounded or zero-comment docket rows, {partial_comment_record_docket_rows} partial retrieved-metadata {plural(partial_comment_record_docket_rows, 'docket row', 'docket rows')}, {complete_comment_record_public_laws} public-law row with all represented dockets complete, and {retrieved_comment_record_rows} retrieved public comment-record metadata rows. The sanitized public comment-detail review adds {comment_text_review_rows} detail {plural(comment_text_review_rows, 'row', 'rows')} across {comment_text_public_laws} public-law {plural(comment_text_public_laws, 'row', 'rows')}, including {complete_comment_text_review_rows} complete-docket detail {plural(complete_comment_text_review_rows, 'row', 'rows')} and {partial_comment_text_review_rows} partial-docket sampled detail {plural(partial_comment_text_review_rows, 'row', 'rows')}, with {text_available_comment_rows} fetched text-available {plural(text_available_comment_rows, 'row', 'rows')} hashed over {comment_text_characters} normalized characters and {comment_text_attachment_rows} attachment-bearing {plural(comment_text_attachment_rows, 'row', 'rows')}; it omits full comment bodies and submitter/contact fields. These links are authority, Federal Register history, timing, bounded comment-record metadata, and sanitized text-availability/hash cues only; partial detail rows do not prove complete docket coverage, and the layer still does not provide a full comment-text corpus, attachment text, commenter-identity validation, sentiment or position coding, enforcement outcomes, appropriations capacity, Unified Agenda stage coverage, or exhaustive implementation coverage.",
                        "Add higher-volume Regulations.gov comment-record retrieval, broader sanitized comment-detail sampling with explicit partial-coverage flags, attachment review where needed, Unified Agenda stages, agency enforcement rows, appropriations capacity, and reviewed statute-to-rule coverage beyond bounded authority and proposed-history metadata.",
                    ))
                    continue
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Statutory revision and law lineage",
                "rulemaking_implementation.law_id -> law_revision_history.public_law_number",
                f"Federal Register document numbers do not directly join to public-law numbers in the final-rule extract, but the separate authority-search cache text-verifies public-law mentions for {authority_matched_rows} / {authority_total_rows} cached public-law rows across {authority_verified_docs} rule documents, the proposed-history cache links {history_matched_final_rows} authority-matched final-rule rows to Federal Register proposed-rule records, the comment-record cache classifies {comment_record_docket_rows} public-law/docket rows with {complete_comment_record_docket_rows} complete bounded or zero-comment rows and {partial_comment_record_docket_rows} partial retrieved-metadata rows, and the sanitized comment-detail review records {text_available_comment_rows} text-available hashed comment-detail {plural(text_available_comment_rows, 'row', 'rows')} including {partial_comment_text_review_rows} partial-docket sampled detail {plural(partial_comment_text_review_rows, 'row', 'rows')}. It still does not provide complete comment coverage for partial rows, a full comment-text corpus, enforcement outcomes, or exhaustive implementation coverage.",
                "Add higher-volume Regulations.gov docket comments, broader sanitized comment-detail sampling with explicit partial-coverage flags, Unified Agenda stages, agency enforcement rows, appropriations capacity, and reviewed law/public-law authority coverage linked to final rules.",
            ))
        elif family == "Statutory revision and law lineage":
            linked = count_linked_rows(rows, "bill_id", bill_id_values)
            if linked <= 0:
                metadata_linked = count_linked_rows(rows, "bill_id", metadata_linked_law_bill_ids())
                if metadata_linked > 0:
                    court_clause = (
                        f", and {court_authority_overlap_rows} SCDB merits-case rows overlap current "
                        f"Federal Register authority U.S.C. sections across {court_public_laws} public-law rows"
                        if court_authority_overlap_rows > 0
                        else ""
                    )
                    no_exact_review_word = "row" if no_exact_target_diff_review_rows == 1 else "rows"
                    unresolved_review_word = "row" if unresolved_target_diff_review_rows == 1 else "rows"
                    unresolved_clause = (
                        f"; {unresolved_target_diff_review_rows} reviewed {unresolved_review_word} remain unresolved"
                        if unresolved_target_diff_review_rows > 0
                        else ""
                    )
                    diff_review_clause = (
                        f", and a bounded statutory target-section diff review pilot records "
                        f"{source_reviewed_target_diff_rows} source-reviewed target-section diff rows "
                        f"across {target_diff_review_public_laws} public-law "
                        f"{'row' if target_diff_review_public_laws == 1 else 'rows'} "
                        f"({no_exact_target_diff_review_rows} reviewed related-section/no-exact-target "
                        f"{no_exact_review_word}{unresolved_clause})"
                        if target_diff_review_rows > 0
                        else ""
                    )
                    no_target_clause = (
                        f", plus {no_structured_target_review_rows} reviewed "
                        f"designation-law no-structured-U.S.C.-target dispositions "
                        f"across {no_structured_target_review_public_laws} public-law "
                        f"{'row' if no_structured_target_review_public_laws == 1 else 'rows'}"
                        if no_structured_target_review_rows > 0
                        else ""
                    )
                    target_lifecycle_bridge_clause = (
                        f", and the target-lifecycle bridge date-screens raw SCDB "
                        f"target-section citations across {target_lifecycle_bridge_rows} "
                        f"target rows, finding {raw_scdb_target_base_rows} raw base-section "
                        f"overlap {plural(raw_scdb_target_base_rows, 'row', 'rows')}, "
                        f"{raw_scdb_target_exact_rows} exact target-reference "
                        f"{plural(raw_scdb_target_exact_rows, 'row', 'rows')}, "
                        f"{raw_scdb_target_cases} unique SCDB "
                        f"{plural(raw_scdb_target_cases, 'case', 'cases')}, and "
                        f"{raw_scdb_target_post_enactment_attachments} post-enactment "
                        f"target base-section case "
                        f"{plural(raw_scdb_target_post_enactment_attachments, 'attachment', 'attachments')}"
                        if target_lifecycle_bridge_rows > 0
                        else ""
                    )
                    complete_lineage_expansion_clause = (
                        f", and a complete-lineage expansion queue ranks "
                        f"{complete_lineage_expansion_rows} current codified-lineage "
                        f"{plural(complete_lineage_expansion_rows, 'candidate', 'candidates')}, "
                        f"including {complete_lineage_active_rows} active expansion "
                        f"{plural(complete_lineage_active_rows, 'row', 'rows')}, "
                        f"{complete_lineage_candidate_expansion_rows} candidate-expansion "
                        f"{plural(complete_lineage_candidate_expansion_rows, 'row', 'rows')}, "
                        f"{complete_lineage_final_audit_rows} final-audit "
                        f"{plural(complete_lineage_final_audit_rows, 'row', 'rows')}, "
                        f"{complete_lineage_no_target_rows} reviewed no-structured-target "
                        f"{plural(complete_lineage_no_target_rows, 'row', 'rows')}, "
                        f"{complete_lineage_source_candidates} source-scan target candidates, "
                        f"{complete_lineage_source_candidate_gap} source candidates beyond "
                        f"triage rows, and {complete_lineage_triage_packet_gap} triage "
                        f"{plural(complete_lineage_triage_packet_gap, 'reference', 'references')} "
                        f"still needing packet review"
                        if complete_lineage_expansion_rows > 0
                        else ""
                    )
                    target_packet_expansion_clause = (
                        f", and a target-packet expansion queue decomposes the "
                        f"triage-to-packet gap into {target_packet_expansion_rows} "
                        f"row-level packet "
                        f"{plural(target_packet_expansion_rows, 'task', 'tasks')} "
                        f"across {target_packet_expansion_public_laws} public "
                        f"{plural(target_packet_expansion_public_laws, 'law', 'laws')}, "
                        f"including {target_packet_note_review_rows} direct U.S.C. "
                        f"note-review {plural(target_packet_note_review_rows, 'task', 'tasks')}, "
                        f"{target_packet_title_only_rows} title-only manual-target "
                        f"{plural(target_packet_title_only_rows, 'task', 'tasks')}, and "
                        f"{target_packet_incomplete_rows} incomplete-fragment manual-review "
                        f"{plural(target_packet_incomplete_rows, 'task', 'tasks')}"
                        if target_packet_expansion_rows > 0
                        else ""
                    )
                    target_packet_source_gap_clause = (
                        f", while a target-packet source-gap queue classifies "
                        f"{target_packet_source_gap_rows} packet-expansion "
                        f"{plural(target_packet_source_gap_rows, 'row', 'rows')} "
                        f"across {target_packet_source_gap_public_laws} public "
                        f"{plural(target_packet_source_gap_public_laws, 'law', 'laws')} "
                        f"as {target_packet_current_no_marker_rows} fetched current "
                        f"OLRC pages without a public-law marker, "
                        f"{target_packet_current_marker_rows} fetched current OLRC "
                        f"{plural(target_packet_current_marker_rows, 'page', 'pages')} "
                        f"with a public-law marker but no downstream packet, "
                        f"{target_packet_source_gap_title_only_rows} title-only "
                        f"{plural(target_packet_source_gap_title_only_rows, 'reference', 'references')} "
                        f"needing section resolution, "
                        f"{target_packet_source_gap_incomplete_rows} incomplete or "
                        f"nonsection {plural(target_packet_source_gap_incomplete_rows, 'reference', 'references')} "
                        f"needing manual resolution, and "
                        f"{target_packet_manual_source_gap_rows} manual current-scan "
                        f"source-gap review {plural(target_packet_manual_source_gap_rows, 'row', 'rows')}; "
                        f"{target_packet_downstream_present_rows} "
                        f"{plural(target_packet_downstream_present_rows, 'row', 'rows')} "
                        f"already have downstream historical, annual, adjudication, or packet coverage"
                        if target_packet_source_gap_rows > 0
                        else ""
                    )
                    target_packet_source_gap_review_clause = (
                        f", and a target-packet source-gap disposition review "
                        f"source-reviews {target_packet_source_gap_review_rows} "
                        f"current-OLRC no-marker "
                        f"{plural(target_packet_source_gap_review_rows, 'blocker', 'blockers')} "
                        f"across {target_packet_source_gap_review_public_laws} public "
                        f"{plural(target_packet_source_gap_review_public_laws, 'law', 'laws')}, "
                        f"classifying {target_packet_source_gap_review_temporary_rows} temporary "
                        f"override {plural(target_packet_source_gap_review_temporary_rows, 'row', 'rows')}, "
                        f"{target_packet_source_gap_review_appropriation_rows} appropriation or "
                        f"program-authority reference "
                        f"{plural(target_packet_source_gap_review_appropriation_rows, 'row', 'rows')}, "
                        f"{target_packet_source_gap_review_cross_reference_rows} cross-reference-only "
                        f"{plural(target_packet_source_gap_review_cross_reference_rows, 'row', 'rows')}, "
                        f"and {target_packet_source_gap_review_table_rows} table or preceding-section "
                        f"{plural(target_packet_source_gap_review_table_rows, 'row', 'rows')} as no-packet dispositions"
                        if target_packet_source_gap_review_rows > 0
                        else ""
                    )
                    target_reference_resolution_clause = (
                        f", and a target-reference resolution candidate report reviews "
                        f"{target_reference_resolution_rows} ambiguous packet "
                        f"{plural(target_reference_resolution_rows, 'blocker', 'blockers')} "
                        f"across {target_reference_resolution_public_laws} public "
                        f"{plural(target_reference_resolution_public_laws, 'law', 'laws')}, "
                        f"suggesting {target_reference_resolution_candidate_count} bounded "
                        f"concrete U.S.C. {plural(target_reference_resolution_candidate_count, 'candidate', 'candidates')} "
                        f"for {target_reference_resolution_candidate_rows} "
                        f"{plural(target_reference_resolution_candidate_rows, 'row', 'rows')} and leaving "
                        f"{target_reference_resolution_unresolved_rows} "
                        f"{plural(target_reference_resolution_unresolved_rows, 'row', 'rows')} "
                        f"without bounded source-scan candidates"
                        if target_reference_resolution_rows > 0
                        else (
                            ", and a target-reference resolution candidate report confirms "
                            "0 ambiguous packet blockers, 0 bounded concrete U.S.C. candidates "
                            "requiring confirmation, and 0 rows without bounded source-scan candidates"
                        )
                    )
                    target_reference_resolution_next_step = (
                        f"Use the target-reference resolution candidate report to manually confirm the "
                        f"{target_reference_resolution_candidate_count} bounded concrete U.S.C. "
                        f"{plural(target_reference_resolution_candidate_count, 'candidate', 'candidates')} "
                        f"and manually review the {target_reference_resolution_unresolved_rows} "
                        f"unresolved ambiguous packet "
                        f"{plural(target_reference_resolution_unresolved_rows, 'blocker', 'blockers')}, then "
                        if target_reference_resolution_rows > 0
                        else (
                            "Use the target-reference resolution candidate report to confirm that no "
                            "ambiguous packet blockers currently require bounded concrete U.S.C. "
                            "candidate confirmation and 0 unresolved ambiguous packet blockers remain, then "
                        )
                    )
                    result.append(build_row(
                        source,
                        rows,
                        metadata_linked,
                        "metadata linked",
                        "Congress.gov bill-detail/action endpoints and bounded Federal Register public-law authority search",
                        "law_revision_history.bill_id -> law_revision_bill_linkage.bill_id; law_revision_bill_linkage.public_law_number -> rulemaking_authority_linkage.public_law_number -> rulemaking_history_linkage.public_law_number",
                        f"Public-law rows now join to official Congress.gov bill/action metadata, {authority_matched_rows} / {authority_total_rows} public-law rows have text-verified Federal Register authority-search matches across {authority_verified_docs} rule documents, {history_public_laws} public-law rows have at least one bounded proposed-rule history match, the comment-record cache has {complete_comment_record_public_laws} public-law row with all represented dockets complete, and the sanitized comment-detail review has {text_available_comment_rows} hashed text-available comment-detail {plural(text_available_comment_rows, 'row', 'rows')} and {partial_comment_text_review_rows} partial-docket sampled detail {plural(partial_comment_text_review_rows, 'row', 'rows')}{court_clause}{diff_review_clause}{no_target_clause}{target_lifecycle_bridge_clause}{complete_lineage_expansion_clause}{target_packet_expansion_clause}{target_packet_source_gap_clause}{target_packet_source_gap_review_clause}{target_reference_resolution_clause}. These rows still do not provide full codified statutory lineage for target-section laws, full comment-text corpus coverage, complete comment coverage for partial rows, enforcement outcomes, direct court-review disposition, direct target-section court-review disposition, complete public-law causal attribution, complete effective statutory text, welfare evidence, causal effects, or model validation.",
                        f"{target_reference_resolution_next_step}use the target-packet source-gap queue and source-gap disposition review to resolve current OLRC pages without public-law markers, build downstream packets for current pages with public-law markers, and expand source-reviewed no-packet dispositions for current-scan source-gap rows before treating queued rows as packet-ready; then use the target-packet expansion queue and complete-lineage expansion queue to expand the U.S.C. target inventory from source-scan candidates, audit related subsections, notes, amendments, repeals, redesignations, and cross-references, source-review any post-enactment raw SCDB target-section overlaps, and add higher-volume comment-record retrieval, broader sanitized comment-detail sampling with explicit partial-coverage flags, enforcement records, appropriations capacity, and direct court-review identifiers.",
                    ))
                    continue
            result.append(build_row(
                source,
                rows,
                linked,
                status_for(linked, len(rows)),
                "Congress.gov bill histories",
                "law_revision_history.bill_id -> bill_progression.bill_id",
                "Public-law rows include bill IDs, but none overlap the current bounded bill-progression sample; codified-text lineage and later court-review joins are also absent.",
                "Add OLRC or govinfo statutory-lineage records and align public laws to bill, implementation, and court-review identifiers.",
            ))
        else:
            result.append(build_row(
                source,
                rows,
                0,
                "not linked",
                "",
                "none",
                "No linkage rule is defined for this source family.",
                source["next_step"],
            ))

    return result


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = {status: 0 for status in STATUS_ORDER}
    for row in rows:
        status_counts[row["linkageStatus"]] = status_counts.get(row["linkageStatus"], 0) + 1
    linked_count = sum(1 for row in rows if row["linkageStatus"] in LINKED_STATUSES)
    high_unlinked = [
        row["sourceFamily"]
        for row in rows
        if row["priority"] == "high" and row["linkageStatus"] not in LINKED_STATUSES
    ]
    lines = [
        "# Empirical Linkage Report",
        "",
        "This report separates source-family coverage from linked validation evidence. It is generated from the source registry and current raw CSVs, and it counts only explicit joins present in the local cached data.",
        "",
        f"- Source families inventoried: {len(rows)}",
        f"- Linked, metadata-linked, or partially linked source families: {linked_count} / {len(rows)}",
        f"- High-priority unlinked source families: {', '.join(high_unlinked) if high_unlinked else 'none'}",
        "",
        "Linkage statuses:",
    ]
    for status in sorted(status_counts, key=lambda item: STATUS_ORDER.get(item, 99)):
        lines.append(f"- {status}: {status_counts[status]}")
    lines.extend([
        "",
        "| Source family | Dataset | Linkage status | Linked rows | Linked to | Link key | Boundary |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ])
    for row in rows:
        linked_to = row["linkedTo"] if row["linkedTo"] else "---"
        lines.append(
            f"| {row['sourceFamily']} | `{row['dataset']}` | {row['linkageStatus']} | "
            f"{row['linkedRows']} / {row['totalRows']} ({row['linkedShare']}) | "
            f"{linked_to} | `{row['linkKey']}` | {row['linkageBoundary']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    registry = read_csv(REGISTRY)
    if not registry:
        raise SystemExit(f"{REGISTRY} is missing or empty.")
    rows = linkage_rows(registry)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
