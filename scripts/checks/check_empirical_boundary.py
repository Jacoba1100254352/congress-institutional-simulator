#!/usr/bin/env python3
"""Check empirical-boundary reports for source-family consistency."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import median


REGISTRY = Path("data/validation/source-registry.csv")
INVENTORY = Path("reports/empirical-data-inventory.csv")
GAP = Path("reports/empirical-validation-gap-report.csv")
GAP_MD = Path("reports/empirical-validation-gap-report.md")
HELDOUT = Path("reports/empirical-flow-heldout.csv")
HELDOUT_MD = Path("reports/empirical-flow-heldout.md")
LINKAGE = Path("reports/empirical-linkage-report.csv")
LINKAGE_MD = Path("reports/empirical-linkage-report.md")
ROADMAP = Path("reports/empirical-linkage-roadmap.csv")
ROADMAP_MD = Path("reports/empirical-linkage-roadmap.md")
RAW_SOURCE_MANIFEST = Path("reports/raw-source-manifest.csv")
RAW_SOURCE_MANIFEST_MD = Path("reports/raw-source-manifest.md")
BILL_PROGRESSION = Path("data/validation/raw/bill_progression.csv")
GOVINFO_BILLSTATUS_LINKAGE_RAW = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
GOVINFO_BILLSTATUS_LINKAGE = Path("reports/govinfo-billstatus-linkage.csv")
GOVINFO_BILLSTATUS_LINKAGE_MD = Path("reports/govinfo-billstatus-linkage.md")
SPONSOR_SUCCESS = Path("data/validation/raw/sponsor_success.csv")
SPONSOR_BILL_LINKAGE_RAW = Path("data/validation/raw/sponsor_bill_linkage.csv")
SPONSOR_BILL_LINKAGE = Path("reports/sponsor-bill-linkage.csv")
SPONSOR_BILL_LINKAGE_MD = Path("reports/sponsor-bill-linkage.md")
COMPARATIVE_INSTITUTIONS = Path("data/validation/raw/comparative_institutions.csv")
COMPARATIVE_INSTITUTION_LINKAGE_RAW = Path("data/validation/raw/comparative_institution_linkage.csv")
COMPARATIVE_INSTITUTION_LINKAGE = Path("reports/comparative-institution-linkage.csv")
COMPARATIVE_INSTITUTION_LINKAGE_MD = Path("reports/comparative-institution-linkage.md")
VOTEVIEW_ROLLCALLS = Path("data/validation/raw/voteview_rollcalls.csv")
VOTEVIEW_MEMBER_CONTEXT_RAW = Path("data/validation/raw/voteview_member_context.csv")
VOTEVIEW_MEMBER_CONTEXT = Path("reports/voteview-member-context.csv")
VOTEVIEW_MEMBER_CONTEXT_MD = Path("reports/voteview-member-context.md")
VOTEVIEW_BILL_LINKAGE_RAW = Path("data/validation/raw/voteview_bill_linkage.csv")
VOTEVIEW_BILL_LINKAGE = Path("reports/voteview-bill-linkage.csv")
VOTEVIEW_BILL_LINKAGE_MD = Path("reports/voteview-bill-linkage.md")
LOBBYING_DISCLOSURE = Path("data/validation/raw/lobbying_disclosure.csv")
LOBBYING_ISSUE_LINKAGE_RAW = Path("data/validation/raw/lobbying_issue_linkage.csv")
LOBBYING_ISSUE_LINKAGE = Path("reports/lobbying-issue-linkage.csv")
LOBBYING_ISSUE_LINKAGE_MD = Path("reports/lobbying-issue-linkage.md")
LOBBYING_BILL_POLICY_CONTEXT = Path("reports/lobbying-bill-policy-context.csv")
LOBBYING_BILL_POLICY_CONTEXT_MD = Path("reports/lobbying-bill-policy-context.md")
LOBBYING_BILL_MENTIONS_RAW = Path("data/validation/raw/lobbying_bill_mentions.csv")
LOBBYING_BILL_MENTION_SEARCHES_RAW = Path("data/validation/raw/lobbying_bill_mention_searches.csv")
LOBBYING_BILL_MENTION_REVIEW = Path("reports/lobbying-bill-mention-review.csv")
LOBBYING_BILL_MENTION_REVIEW_MD = Path("reports/lobbying-bill-mention-review.md")
LOBBYING_BILL_ACTION_CONTEXT = Path("reports/lobbying-bill-action-context.csv")
LOBBYING_BILL_ACTION_CONTEXT_MD = Path("reports/lobbying-bill-action-context.md")
LOBBYING_BILL_TEXT_REVIEW = Path("reports/lobbying-bill-text-review.csv")
LOBBYING_BILL_TEXT_REVIEW_MD = Path("reports/lobbying-bill-text-review.md")
LOBBYING_BILL_DISPOSITION_REVIEW = Path("reports/lobbying-bill-disposition-review.csv")
LOBBYING_BILL_DISPOSITION_REVIEW_MD = Path("reports/lobbying-bill-disposition-review.md")
LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW = Path(
    "data/validation/raw/lobbying_bill_manual_disposition_review.csv"
)
LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW = Path(
    "reports/lobbying-bill-manual-disposition-review.csv"
)
LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_MD = Path(
    "reports/lobbying-bill-manual-disposition-review.md"
)
LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS = Path(
    "reports/lobbying-bill-medium-disposition-packets.csv"
)
LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS_MD = Path(
    "reports/lobbying-bill-medium-disposition-packets.md"
)
LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW = Path(
    "data/validation/raw/lobbying_bill_medium_directional_packet_review.csv"
)
LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW = Path(
    "reports/lobbying-bill-medium-directional-packet-review.csv"
)
LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_MD = Path(
    "reports/lobbying-bill-medium-directional-packet-review.md"
)
LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW = Path(
    "data/validation/raw/lobbying_bill_medium_position_activity_packet_review.csv"
)
LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW = Path(
    "reports/lobbying-bill-medium-position-activity-packet-review.csv"
)
LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_MD = Path(
    "reports/lobbying-bill-medium-position-activity-packet-review.md"
)
TOPIC_THROUGHPUT = Path("data/validation/raw/topic_throughput.csv")
COURT_REVIEW = Path("data/validation/raw/court_review.csv")
COURT_LAW_LINKAGE_RAW = Path("data/validation/raw/court_law_linkage.csv")
COURT_LAW_LINKAGE = Path("reports/court-law-linkage.csv")
COURT_LAW_LINKAGE_MD = Path("reports/court-law-linkage.md")
BILL_LAW_SPINE = Path("reports/bill-law-evidence-spine.csv")
BILL_LAW_SPINE_MD = Path("reports/bill-law-evidence-spine.md")
BILL_LAW_LIFECYCLE_READINESS = Path("reports/bill-law-lifecycle-readiness.csv")
BILL_LAW_LIFECYCLE_READINESS_MD = Path("reports/bill-law-lifecycle-readiness.md")
BILL_LAW_LIFECYCLE_NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
BILL_LAW_LIFECYCLE_NEXT_ACTIONS_MD = Path("reports/bill-law-lifecycle-next-actions.md")
BILL_LAW_LIFECYCLE_CORPUS = Path("reports/bill-law-lifecycle-corpus.csv")
BILL_LAW_LIFECYCLE_CORPUS_MD = Path("reports/bill-law-lifecycle-corpus.md")
BILL_FINANCE_LOBBYING_REVIEW_QUEUE = Path("reports/bill-finance-lobbying-review-queue.csv")
BILL_FINANCE_LOBBYING_REVIEW_QUEUE_MD = Path("reports/bill-finance-lobbying-review-queue.md")
BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW = Path(
    "data/validation/raw/bill_finance_lobbying_local_context_review.csv"
)
BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW = Path(
    "reports/bill-finance-lobbying-local-context-review.csv"
)
BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-local-context-review.md"
)
BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW = Path(
    "data/validation/raw/bill_finance_lobbying_external_lda_searches.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW = Path(
    "data/validation/raw/bill_finance_lobbying_external_lda_mentions.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW = Path(
    "reports/bill-finance-lobbying-external-search-review.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-external-search-review.md"
)
BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW = Path(
    "reports/bill-finance-lobbying-external-lda-mention-review.csv"
)
BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-external-lda-mention-review.md"
)
BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW = Path(
    "reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv"
)
BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-campaign-finance-target-scope-review.md"
)
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT = Path(
    "reports/bill-finance-lobbying-committee-action-context.csv"
)
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT_MD = Path(
    "reports/bill-finance-lobbying-committee-action-context.md"
)
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-committee-action-source-review.csv"
)
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-committee-action-source-review.md"
)
BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-roll-call-source-review.csv"
)
BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-roll-call-source-review.md"
)
BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_RAW = Path(
    "data/validation/raw/bill_finance_lobbying_roll_call_source.csv"
)
BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_RAW = Path(
    "data/validation/raw/bill_finance_lobbying_member_vote_targets.csv"
)
BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW = Path(
    "reports/bill-finance-lobbying-member-vote-target-review.csv"
)
BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW_MD = Path(
    "reports/bill-finance-lobbying-member-vote-target-review.md"
)
BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE = Path(
    "reports/bill-finance-lobbying-source-acquisition-queue.csv"
)
BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE_MD = Path(
    "reports/bill-finance-lobbying-source-acquisition-queue.md"
)
STATUTORY_LINEAGE_REVIEW_QUEUE = Path("reports/statutory-lineage-review-queue.csv")
STATUTORY_LINEAGE_REVIEW_QUEUE_MD = Path("reports/statutory-lineage-review-queue.md")
STATUTORY_LINEAGE_SOURCE_SCAN_RAW = Path("data/validation/raw/statutory_lineage_source_scan.csv")
STATUTORY_LINEAGE_SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
STATUTORY_LINEAGE_SOURCE_SCAN_MD = Path("reports/statutory-lineage-source-scan.md")
STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE = Path("reports/statutory-lineage-target-section-triage.csv")
STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE_MD = Path("reports/statutory-lineage-target-section-triage.md")
STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_RAW = Path("data/validation/raw/statutory_lineage_olrc_current_scan.csv")
STATUTORY_LINEAGE_OLRC_CURRENT_SCAN = Path("reports/statutory-lineage-olrc-current-scan.csv")
STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_MD = Path("reports/statutory-lineage-olrc-current-scan.md")
STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_RAW = Path("data/validation/raw/statutory_lineage_olrc_historical_scan.csv")
STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN = Path("reports/statutory-lineage-olrc-historical-scan.csv")
STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD = Path("reports/statutory-lineage-olrc-historical-scan.md")
STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_RAW = Path("data/validation/raw/statutory_lineage_olrc_annual_text_diff.csv")
STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD = Path("reports/statutory-lineage-olrc-annual-text-diff.md")
STATUTORY_LINEAGE_ADJUDICATION_RAW = Path("data/validation/raw/statutory_lineage_adjudication.csv")
STATUTORY_LINEAGE_ADJUDICATION = Path("reports/statutory-lineage-adjudication.csv")
STATUTORY_LINEAGE_ADJUDICATION_MD = Path("reports/statutory-lineage-adjudication.md")
STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW = Path("data/validation/raw/statutory_lineage_target_review_packets.csv")
STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS = Path("reports/statutory-lineage-target-review-packets.csv")
STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD = Path("reports/statutory-lineage-target-review-packets.md")
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW = Path(
    "data/validation/raw/statutory_lineage_target_section_diff_review.csv"
)
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW = Path(
    "reports/statutory-lineage-target-section-diff-review.csv"
)
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MD = Path(
    "reports/statutory-lineage-target-section-diff-review.md"
)
STATUTORY_LINEAGE_NO_TARGET_REVIEW_RAW = Path(
    "data/validation/raw/statutory_lineage_no_target_review.csv"
)
STATUTORY_LINEAGE_NO_TARGET_REVIEW = Path("reports/statutory-lineage-no-target-review.csv")
STATUTORY_LINEAGE_NO_TARGET_REVIEW_MD = Path("reports/statutory-lineage-no-target-review.md")
STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE = Path(
    "reports/statutory-lineage-target-lifecycle-bridge.csv"
)
STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE_MD = Path(
    "reports/statutory-lineage-target-lifecycle-bridge.md"
)
STATUTORY_LINEAGE_CODIFIED_PROGRESS = Path("reports/statutory-lineage-codified-progress.csv")
STATUTORY_LINEAGE_CODIFIED_PROGRESS_MD = Path("reports/statutory-lineage-codified-progress.md")
STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW = Path("reports/statutory-lineage-effective-text-review.csv")
STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW_MD = Path("reports/statutory-lineage-effective-text-review.md")
STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW = Path(
    "reports/statutory-lineage-public-law-attribution-review.csv"
)
STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW_MD = Path(
    "reports/statutory-lineage-public-law-attribution-review.md"
)
STATUTORY_LINEAGE_COMPLETION_QUEUE = Path("reports/statutory-lineage-completion-queue.csv")
STATUTORY_LINEAGE_COMPLETION_QUEUE_MD = Path("reports/statutory-lineage-completion-queue.md")
STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE = Path(
    "reports/statutory-lineage-complete-lineage-expansion-queue.csv"
)
STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE_MD = Path(
    "reports/statutory-lineage-complete-lineage-expansion-queue.md"
)
STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE = Path(
    "reports/statutory-lineage-target-packet-expansion-queue.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE_MD = Path(
    "reports/statutory-lineage-target-packet-expansion-queue.md"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE = Path(
    "reports/statutory-lineage-target-packet-source-gap-queue.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE_MD = Path(
    "reports/statutory-lineage-target-packet-source-gap-queue.md"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW = Path(
    "reports/statutory-lineage-target-packet-source-gap-review.csv"
)
STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW_MD = Path(
    "reports/statutory-lineage-target-packet-source-gap-review.md"
)
STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES = Path(
    "reports/statutory-lineage-target-reference-resolution-candidates.csv"
)
STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES_MD = Path(
    "reports/statutory-lineage-target-reference-resolution-candidates.md"
)
COURT_PUBLIC_LAW_REVIEW_QUEUE = Path("reports/court-public-law-review-queue.csv")
COURT_PUBLIC_LAW_REVIEW_QUEUE_MD = Path("reports/court-public-law-review-queue.md")
COURT_PUBLIC_LAW_TEMPORAL_TRIAGE = Path("reports/court-public-law-temporal-triage.csv")
COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD = Path("reports/court-public-law-temporal-triage.md")
COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW = Path("data/validation/raw/court_public_law_direct_review.csv")
COURT_PUBLIC_LAW_DIRECT_REVIEW = Path("reports/court-public-law-direct-review.csv")
COURT_PUBLIC_LAW_DIRECT_REVIEW_MD = Path("reports/court-public-law-direct-review.md")
RULEMAKING_AUTHORITY_LINKAGE_RAW = Path("data/validation/raw/rulemaking_authority_linkage.csv")
RULEMAKING_AUTHORITY_LINKAGE = Path("reports/rulemaking-authority-linkage.csv")
RULEMAKING_AUTHORITY_LINKAGE_MD = Path("reports/rulemaking-authority-linkage.md")
RULEMAKING_HISTORY_LINKAGE_RAW = Path("data/validation/raw/rulemaking_history_linkage.csv")
RULEMAKING_HISTORY_LINKAGE = Path("reports/rulemaking-history-linkage.csv")
RULEMAKING_HISTORY_LINKAGE_MD = Path("reports/rulemaking-history-linkage.md")
RULEMAKING_COMMENT_METADATA_RAW = Path("data/validation/raw/rulemaking_comment_metadata.csv")
RULEMAKING_COMMENT_METADATA = Path("reports/rulemaking-comment-metadata.csv")
RULEMAKING_COMMENT_METADATA_MD = Path("reports/rulemaking-comment-metadata.md")
RULEMAKING_COMMENT_RECORDS_RAW = Path("data/validation/raw/rulemaking_comment_records.csv")
RULEMAKING_COMMENT_RECORDS = Path("reports/rulemaking-comment-records.csv")
RULEMAKING_COMMENT_RECORDS_MD = Path("reports/rulemaking-comment-records.md")
RULEMAKING_COMMENT_TEXT_REVIEW_RAW = Path("data/validation/raw/rulemaking_comment_text_review.csv")
RULEMAKING_COMMENT_TEXT_REVIEW = Path("reports/rulemaking-comment-text-review.csv")
RULEMAKING_COMMENT_TEXT_REVIEW_MD = Path("reports/rulemaking-comment-text-review.md")
CAMPAIGN_FINANCE_DISTRICT_CONTEXT = Path("reports/campaign-finance-district-context.csv")
CAMPAIGN_FINANCE_DISTRICT_CONTEXT_MD = Path("reports/campaign-finance-district-context.md")
CAMPAIGN_FINANCE = Path("data/validation/raw/campaign_finance.csv")
CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
CAMPAIGN_FINANCE_MEMBER_CONTEXT_RAW = Path("data/validation/raw/campaign_finance_member_context.csv")
CAMPAIGN_FINANCE_MEMBER_CONTEXT = Path("reports/campaign-finance-member-context.csv")
CAMPAIGN_FINANCE_MEMBER_CONTEXT_MD = Path("reports/campaign-finance-member-context.md")
CAMPAIGN_FINANCE_ISSUE_CONTEXT_RAW = Path("data/validation/raw/campaign_finance_issue_context.csv")
CAMPAIGN_FINANCE_ISSUE_CONTEXT = Path("reports/campaign-finance-issue-context.csv")
CAMPAIGN_FINANCE_ISSUE_CONTEXT_MD = Path("reports/campaign-finance-issue-context.md")
CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT = Path("reports/campaign-finance-sponsor-bill-context.csv")
CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT_MD = Path("reports/campaign-finance-sponsor-bill-context.md")
DISTRICT_PUBLIC_OPINION = Path("data/validation/raw/district_public_opinion.csv")
LAW_REVISION_HISTORY = Path("data/validation/raw/law_revision_history.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
DISTRICT_PUBLIC_OPINION_LINKAGE = Path("data/validation/raw/district_public_opinion_linkage.csv")
DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT_RAW = Path("data/validation/raw/district_public_opinion_policy_context.csv")
DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT = Path("reports/district-public-opinion-policy-context.csv")
DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT_MD = Path("reports/district-public-opinion-policy-context.md")
DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS = Path(
    "reports/district-public-opinion-bill-topic-readiness.csv"
)
DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS_MD = Path(
    "reports/district-public-opinion-bill-topic-readiness.md"
)
DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS_MD = Path("reports/district-public-opinion-source-packets.md")
DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW = Path(
    "data/validation/raw/district_public_opinion_census_denominators.csv"
)
DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS = Path(
    "reports/district-public-opinion-census-denominators.csv"
)
DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_MD = Path(
    "reports/district-public-opinion-census-denominators.md"
)
DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW = Path(
    "data/validation/raw/district_public_opinion_acs_context.csv"
)
DISTRICT_PUBLIC_OPINION_ACS_CONTEXT = Path("reports/district-public-opinion-acs-context.csv")
DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_MD = Path("reports/district-public-opinion-acs-context.md")
DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK = Path(
    "reports/district-public-opinion-survey-source-crosswalk.csv"
)
DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK_MD = Path(
    "reports/district-public-opinion-survey-source-crosswalk.md"
)
DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW = Path(
    "reports/district-public-opinion-survey-item-proxy-review.csv"
)
DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW_MD = Path(
    "reports/district-public-opinion-survey-item-proxy-review.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_candidates.metadata.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-candidate-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW_MD = Path(
    "reports/district-public-opinion-ces-policy-item-candidate-review.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.metadata.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-response-distribution-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW_MD = Path(
    "reports/district-public-opinion-ces-policy-item-response-distribution-review.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.metadata.md"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-codebook-direction-review.csv"
)
DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW_MD = Path(
    "reports/district-public-opinion-ces-policy-item-codebook-direction-review.md"
)
GAP_TEX = Path("paper/figures/empirical_validation_gap_table.tex")
LINKAGE_STATUSES = {"linked", "metadata linked", "partially linked", "not linked", "not independently linked"}
LINKED_STATUSES = {"linked", "metadata linked", "partially linked"}
ROADMAP_REQUIRED_FIELDS = {
    "blockingGap",
    "requiredJoinKeys",
    "targetSourceFamilies",
    "minimumViableDataset",
    "acceptanceGate",
    "futureTarget",
    "claimUpgradeBoundary",
}
LIFECYCLE_DIRECT_LAYERS = [
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
LIFECYCLE_CONTEXT_LAYERS = [
    "sponsor_district_public_opinion_metadata",
    "sponsor_district_bill_policy_area_context",
    "topic_throughput_policy_area",
    "campaign_finance_sponsor_policy_area_context",
    "lobbying_issue_bill_policy_area_context",
    "court_review_usc_section_authority_overlap",
    "scdb_law_minor_usc_section",
]
LIFECYCLE_HIGH_PRIORITY_GATES = [
    "bill_topic_public_opinion",
    "bill_specific_campaign_finance_or_lobbying_to_bill",
    "codified_usc_lineage",
    "direct_case_to_public_law_identifier",
    "reviewed_case_disposition_to_public_law",
    "complete_regulations_comments",
    "unified_agenda_stage",
    "implementation_outcomes_or_enforcement",
    "full_bill_progression_census_overlap",
]
LIFECYCLE_DIRECT_REVIEW_GATES = {
    "direct_case_to_public_law_identifier",
    "reviewed_case_disposition_to_public_law",
}
LIFECYCLE_TIERS = {
    "tier_1_rich_lifecycle_review_candidate",
    "tier_2_implementation_chain_candidate",
    "tier_3_representation_influence_context_candidate",
    "tier_4_single_downstream_link_candidate",
    "tier_5_bill_action_context_only",
}
LIFECYCLE_POINTER_FIELDS = {
    "district_ids": "district_ids",
    "campaign_finance_context_bill_ids": "campaign_finance_sponsor_policy_context_bill_ids",
    "lobbying_context_bill_ids": "lobbying_policy_context_bill_ids",
    "authority_document_numbers": "implementation_authority_document_numbers",
    "proposed_rule_document_numbers": "implementation_history_proposed_document_numbers",
    "regulations_docket_ids": "implementation_history_proposed_regulations_docket_ids",
    "regulations_comment_urls": "implementation_history_proposed_regulations_comment_urls",
    "comment_record_docket_ids": "implementation_comment_record_docket_ids",
    "court_case_ids": "court_review_case_ids",
    "court_usc_sections": "court_review_usc_sections",
}
STATUTORY_LINEAGE_SOURCE_REVIEW_TARGETS = {
    "public_law_text",
    "us_code_notes",
    "olrc_us_code_classification",
    "govinfo_uslm_or_statutes_at_large",
    "ecfr_or_cfr_authority_if_applicable",
}
STATUTORY_LINEAGE_MISSING_LINKS = {
    "codified_usc_lineage",
    "amended_section_identifier",
    "target_section_diff",
    "law_revision_effective_text",
    "source_reviewed_statutory_lineage",
    "model_validation",
}
STATUTORY_REVISION_FLAG_FIELDS = {
    "amended",
    "reauthorized",
    "repealed",
    "expired",
    "invalidated",
}
STATUTORY_LINEAGE_SOURCE_SCAN_MISSING_LINKS = {
    "olrc_us_code_classification",
    "codified_usc_lineage",
    "target_section_diff",
    "law_revision_effective_text",
    "model_validation",
}
STATUTORY_LINEAGE_OLRC_HISTORICAL_MISSING_LINKS = {
    "manual_olrc_classification_review",
    "codified_usc_lineage_adjudication",
    "source_reviewed_text_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "model_validation",
}
STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MISSING_LINKS = {
    "manual_olrc_classification_review",
    "codified_usc_lineage_adjudication",
    "source_reviewed_target_section_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "model_validation",
}
STATUTORY_LINEAGE_ADJUDICATION_MISSING_LINKS = {
    "source_reviewed_target_section_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "implementation_outcomes",
    "model_validation",
}
STATUTORY_LINEAGE_TARGET_REVIEW_PACKET_MISSING_LINKS = {
    "human_source_review_disposition",
    "source_reviewed_target_section_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "implementation_outcomes",
    "model_validation",
}
STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MISSING_LINKS = {
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "complete_codified_usc_lineage_review",
    "implementation_outcomes",
    "court_review",
    "model_validation",
}
STATUTORY_LINEAGE_NO_TARGET_REVIEW_MISSING_LINKS = {
    "target_section_diff_not_applicable_designation_law",
    "public_law_causal_attribution_not_applicable_no_target",
    "law_revision_effective_text_not_applicable_no_target",
    "implementation_outcomes_or_enforcement",
    "complete_regulations_comments",
    "direct_target_section_court_review_not_applicable_no_target",
    "welfare_or_public_benefit",
    "model_validation",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def csv_fieldnames(path: Path) -> set[str]:
    with path.open(newline="") as handle:
        return set(csv.DictReader(handle).fieldnames or [])


def csv_row_count(path: Path) -> int:
    if not path.exists() or path.is_dir():
        return -1
    with path.open(newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def by_field(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(field, "")
        if value in result:
            raise ValueError(f"duplicate {field}: {value}")
        result[value] = row
    return result


def tex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(replacements.get(char, char) for char in text)


def house_district_from_campaign_linkage(row: dict[str, str]) -> str:
    if row.get("candidate_office", "").strip().casefold() != "house":
        return ""
    state = row.get("candidate_office_state", "").strip().upper()
    district = row.get("candidate_office_district", "").strip()
    if not state or state == "US" or not district:
        return ""
    try:
        district_number = int(district)
    except ValueError:
        return ""
    if district_number <= 0:
        return ""
    return f"{state}-{district_number:02d}"


def bill_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("congress", "").strip(),
        row.get("bill_type", "").strip(),
        row.get("bill_number", "").strip(),
    )


def voteview_member_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("congress", "").strip(),
        row.get("chamber", "").strip(),
        row.get("icpsr", "").strip(),
    )


def voteview_vote_id(row: dict[str, str]) -> str:
    if row.get("vote_id"):
        return row["vote_id"].strip()
    congress = row.get("congress", "").strip()
    chamber = row.get("chamber", "").strip()
    rollnumber = row.get("rollnumber", "").strip()
    return f"{congress}-{chamber}-{rollnumber}" if congress and chamber and rollnumber else ""


def campaign_transaction_key(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    return (
        row.get("cycle", "").strip(),
        row.get("recipient", "").strip(),
        row.get("source_id", "").strip(),
        row.get("source_schedule", "").strip(),
        row.get("transaction_date", "").strip(),
        row.get("amount", "").strip(),
    )


def district_policy_context_key(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        row.get("district_id", "").strip(),
        row.get("issue", "").strip(),
        row.get("year", "").strip(),
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
    )


def district_policy_topic_totals(rows: list[dict[str, str]]) -> dict[str, int]:
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
            try:
                value = int(row.get(field, "0") or "0")
            except ValueError:
                value = 0
            current[field] = max(current[field], value)
    return {
        field: sum(policy_counts[field] for policy_counts in by_policy_area.values())
        for field in ("topic_introduced", "topic_floor_considered", "topic_enacted")
    }


def split_semicolon_values(row: dict[str, str], field: str) -> set[str]:
    return {
        value.strip()
        for value in row.get(field, "").split(";")
        if value.strip()
    }


def normalize_space(value: str) -> str:
    return " ".join((value or "").split())


def lda_text_review_fingerprint(row: dict[str, str]) -> str:
    fields = [
        "bill_id",
        "filing_uuid",
        "client_name",
        "registrant_name",
        "activity_issue",
        "activity_description",
        "matched_bill_refs",
    ]
    source = "\x1f".join(row.get(field, "") for field in fields)
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


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


def lda_bill_reference_located(row: dict[str, str]) -> bool:
    bill_id = row.get("bill_id", "").strip()
    description = normalize_space(row.get("activity_description", ""))
    return bool(bill_id and lda_bill_reference_pattern(bill_id).search(description))


def committee_codes(value: str) -> set[str]:
    codes: set[str] = set()
    for chunk in value.split(";"):
        code = chunk.strip().split(" ", maxsplit=1)[0].strip()
        if code:
            codes.add(code)
    return codes


def parse_iso_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip()) if value.strip() else None
    except ValueError:
        return None


def parse_report_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    parsed = parse_iso_date(value)
    if parsed:
        return parsed
    try:
        return datetime.strptime(value, "%m/%d/%Y").date()
    except ValueError:
        return None


def days_between(start: str, end: str) -> int | None:
    start_date = parse_iso_date(start)
    end_date = parse_iso_date(end)
    if not start_date or not end_date:
        return None
    return (end_date - start_date).days


def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def finance_lobbying_review_status(
    campaign_exact_match: bool,
    lobbying_exact_match: bool,
    campaign_context_rows: int,
    lobbying_context_rows: int,
) -> str:
    if campaign_exact_match or lobbying_exact_match:
        return "candidate_exact_bill_match_needs_source_review"
    if campaign_context_rows > 0 and lobbying_context_rows > 0:
        return "same_policy_finance_and_lobbying_context_needs_bill_specific_review"
    if campaign_context_rows > 0:
        return "same_policy_campaign_finance_context_needs_bill_specific_review"
    if lobbying_context_rows > 0:
        return "same_policy_lobbying_context_needs_bill_specific_review"
    return "no_current_finance_or_lobbying_context_needs_source_expansion"


def summary_value(values: list[int], field: str) -> str:
    if not values:
        return ""
    if field == "min":
        return str(min(values))
    if field == "max":
        return str(max(values))
    if field == "median":
        median_value = median(values)
        if isinstance(median_value, int) or (
            isinstance(median_value, float) and median_value.is_integer()
        ):
            return str(int(median_value))
        return f"{median_value:.1f}"
    raise ValueError(f"unknown summary field {field}")


def summary_count(path: Path, label: str) -> tuple[int, int] | None:
    if not path.exists():
        return None
    pattern = re.compile(rf"^- {re.escape(label)}:\s+([0-9]+)\s*/\s*([0-9]+)\s*$", re.MULTILINE)
    match = pattern.search(path.read_text())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def heldout_pass_summary(path: Path) -> tuple[int, int] | None:
    if not path.exists():
        return None
    match = re.search(
        r"^- Targeted held-out checks passing:\s+([0-9]+)\s*/\s*([0-9]+)\s*$",
        path.read_text(),
        re.MULTILINE,
    )
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def check() -> list[str]:
    failures: list[str] = []
    try:
        registry = read_csv(REGISTRY)
        inventory = read_csv(INVENTORY)
        gap = read_csv(GAP)
        heldout = read_csv(HELDOUT)
        linkage = read_csv(LINKAGE)
        roadmap = read_csv(ROADMAP)
        raw_manifest = read_csv(RAW_SOURCE_MANIFEST)
        govinfo_billstatus_linkage = read_csv(GOVINFO_BILLSTATUS_LINKAGE)
        sponsor_bill_linkage = read_csv(SPONSOR_BILL_LINKAGE)
        comparative_institution_linkage = read_csv(COMPARATIVE_INSTITUTION_LINKAGE)
        voteview_member_context = read_csv(VOTEVIEW_MEMBER_CONTEXT)
        voteview_bill_linkage = read_csv(VOTEVIEW_BILL_LINKAGE)
        lobbying_issue_linkage = read_csv(LOBBYING_ISSUE_LINKAGE)
        lobbying_bill_policy_context = read_csv(LOBBYING_BILL_POLICY_CONTEXT)
        lobbying_bill_mention_review = read_csv(LOBBYING_BILL_MENTION_REVIEW)
        lobbying_bill_action_context = read_csv(LOBBYING_BILL_ACTION_CONTEXT)
        lobbying_bill_text_review = read_csv(LOBBYING_BILL_TEXT_REVIEW)
        lobbying_bill_disposition_review = read_csv(LOBBYING_BILL_DISPOSITION_REVIEW)
        lobbying_bill_manual_disposition_review_raw = read_csv(
            LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW
        )
        lobbying_bill_manual_disposition_review = read_csv(
            LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW
        )
        lobbying_bill_medium_disposition_packets = read_csv(
            LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS
        )
        lobbying_bill_medium_directional_packet_review_raw = read_csv(
            LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW
        )
        lobbying_bill_medium_directional_packet_review = read_csv(
            LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW
        )
        lobbying_bill_medium_position_activity_packet_review_raw = read_csv(
            LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW
        )
        lobbying_bill_medium_position_activity_packet_review = read_csv(
            LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW
        )
        court_law_linkage = read_csv(COURT_LAW_LINKAGE)
        bill_law_spine = read_csv(BILL_LAW_SPINE)
        bill_law_lifecycle_readiness = read_csv(BILL_LAW_LIFECYCLE_READINESS)
        bill_law_lifecycle_next_actions = read_csv(BILL_LAW_LIFECYCLE_NEXT_ACTIONS)
        bill_law_lifecycle_corpus = read_csv(BILL_LAW_LIFECYCLE_CORPUS)
        bill_finance_lobbying_review_queue = read_csv(BILL_FINANCE_LOBBYING_REVIEW_QUEUE)
        bill_finance_lobbying_local_context_review_raw = read_csv(
            BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW
        )
        bill_finance_lobbying_local_context_review = read_csv(
            BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW
        )
        bill_finance_lobbying_external_lda_searches_raw = read_csv(
            BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW
        )
        bill_finance_lobbying_external_lda_mentions_raw = read_csv(
            BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW
        )
        bill_finance_lobbying_external_search_review = read_csv(
            BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW
        )
        bill_finance_lobbying_external_lda_mention_review = read_csv(
            BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW
        )
        bill_finance_lobbying_campaign_finance_target_scope_review = read_csv(
            BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW
        )
        bill_finance_lobbying_committee_action_context = read_csv(
            BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT
        )
        bill_finance_lobbying_committee_action_source_review = read_csv(
            BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW
        )
        bill_finance_lobbying_roll_call_source_review = read_csv(
            BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW
        )
        bill_finance_lobbying_member_vote_target_review = read_csv(
            BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW
        )
        bill_finance_lobbying_source_acquisition_queue = read_csv(
            BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE
        )
        statutory_lineage_review_queue = read_csv(STATUTORY_LINEAGE_REVIEW_QUEUE)
        statutory_lineage_source_scan = read_csv(STATUTORY_LINEAGE_SOURCE_SCAN)
        statutory_lineage_target_section_triage = read_csv(STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE)
        statutory_lineage_olrc_current_scan = read_csv(STATUTORY_LINEAGE_OLRC_CURRENT_SCAN)
        statutory_lineage_olrc_historical_scan = read_csv(STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN)
        statutory_lineage_olrc_annual_text_diff = read_csv(STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF)
        statutory_lineage_adjudication = read_csv(STATUTORY_LINEAGE_ADJUDICATION)
        statutory_lineage_target_review_packets = read_csv(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS)
        statutory_lineage_target_section_diff_review = read_csv(
            STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW
        )
        statutory_lineage_no_target_review = read_csv(STATUTORY_LINEAGE_NO_TARGET_REVIEW)
        statutory_lineage_target_lifecycle_bridge = read_csv(
            STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE
        )
        statutory_lineage_codified_progress = read_csv(STATUTORY_LINEAGE_CODIFIED_PROGRESS)
        statutory_lineage_effective_text_review = read_csv(
            STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW
        )
        statutory_lineage_public_law_attribution_review = read_csv(
            STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW
        )
        statutory_lineage_completion_queue = read_csv(STATUTORY_LINEAGE_COMPLETION_QUEUE)
        statutory_lineage_complete_lineage_expansion_queue = read_csv(
            STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE
        )
        statutory_lineage_target_packet_expansion_queue = read_csv(
            STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE
        )
        statutory_lineage_target_packet_source_gap_queue = read_csv(
            STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE
        )
        statutory_lineage_target_packet_source_gap_review = read_csv(
            STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW
        )
        statutory_lineage_target_reference_resolution_candidates = read_csv(
            STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES
        )
        court_public_law_review_queue = read_csv(COURT_PUBLIC_LAW_REVIEW_QUEUE)
        court_public_law_temporal_triage = read_csv(COURT_PUBLIC_LAW_TEMPORAL_TRIAGE)
        court_public_law_direct_review_raw = read_csv(COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW)
        court_public_law_direct_review = read_csv(COURT_PUBLIC_LAW_DIRECT_REVIEW)
        rulemaking_authority_linkage = read_csv(RULEMAKING_AUTHORITY_LINKAGE)
        rulemaking_history_linkage = read_csv(RULEMAKING_HISTORY_LINKAGE)
        rulemaking_comment_metadata = read_csv(RULEMAKING_COMMENT_METADATA)
        rulemaking_comment_records = read_csv(RULEMAKING_COMMENT_RECORDS)
        rulemaking_comment_text_review = read_csv(RULEMAKING_COMMENT_TEXT_REVIEW)
        campaign_finance_district_context = read_csv(CAMPAIGN_FINANCE_DISTRICT_CONTEXT)
        campaign_finance_member_context = read_csv(CAMPAIGN_FINANCE_MEMBER_CONTEXT)
        campaign_finance_issue_context = read_csv(CAMPAIGN_FINANCE_ISSUE_CONTEXT)
        campaign_finance_sponsor_bill_context = read_csv(CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT)
        district_public_opinion_policy_context = read_csv(DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT)
        district_public_opinion_bill_topic_readiness = read_csv(
            DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS
        )
        district_public_opinion_source_packets = read_csv(DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS)
        district_public_opinion_census_denominators = read_csv(
            DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS
        )
        district_public_opinion_acs_context_raw = read_csv(DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW)
        district_public_opinion_acs_context = read_csv(DISTRICT_PUBLIC_OPINION_ACS_CONTEXT)
        district_public_opinion_survey_source_crosswalk = read_csv(
            DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK
        )
        district_public_opinion_survey_item_proxy_review = read_csv(
            DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW
        )
        district_public_opinion_ces_policy_item_candidates_raw = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW
        )
        district_public_opinion_ces_policy_item_candidate_review = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW
        )
        district_public_opinion_ces_policy_item_response_distributions_raw = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW
        )
        district_public_opinion_ces_policy_item_response_distribution_review = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW
        )
        district_public_opinion_ces_policy_item_codebook_direction_raw = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW
        )
        district_public_opinion_ces_policy_item_codebook_direction_review = read_csv(
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW
        )
    except FileNotFoundError as exception:
        return [f"missing required empirical-boundary artifact: {exception.filename}"]
    except ValueError as exception:
        return [str(exception)]

    if not registry:
        failures.append(f"{REGISTRY}: no rows")
    if not inventory:
        failures.append(f"{INVENTORY}: no rows")
    if not gap:
        failures.append(f"{GAP}: no rows")
    if not heldout:
        failures.append(f"{HELDOUT}: no rows")
    if not linkage:
        failures.append(f"{LINKAGE}: no rows")
    if not roadmap:
        failures.append(f"{ROADMAP}: no rows")
    if not raw_manifest:
        failures.append(f"{RAW_SOURCE_MANIFEST}: no rows")
    if not govinfo_billstatus_linkage:
        failures.append(f"{GOVINFO_BILLSTATUS_LINKAGE}: no rows")
    if not sponsor_bill_linkage:
        failures.append(f"{SPONSOR_BILL_LINKAGE}: no rows")
    if not comparative_institution_linkage:
        failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: no rows")
    if not voteview_member_context:
        failures.append(f"{VOTEVIEW_MEMBER_CONTEXT}: no rows")
    if not voteview_bill_linkage:
        failures.append(f"{VOTEVIEW_BILL_LINKAGE}: no rows")
    if not lobbying_issue_linkage:
        failures.append(f"{LOBBYING_ISSUE_LINKAGE}: no rows")
    if not lobbying_bill_policy_context:
        failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: no rows")
    if not lobbying_bill_mention_review:
        failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: no rows")
    if not lobbying_bill_action_context:
        failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: no rows")
    if not lobbying_bill_text_review:
        failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: no rows")
    if not court_law_linkage:
        failures.append(f"{COURT_LAW_LINKAGE}: no rows")
    if not bill_law_spine:
        failures.append(f"{BILL_LAW_SPINE}: no rows")
    if not bill_law_lifecycle_readiness:
        failures.append(f"{BILL_LAW_LIFECYCLE_READINESS}: no rows")
    if not bill_law_lifecycle_next_actions:
        failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: no rows")
    if not bill_law_lifecycle_corpus:
        failures.append(f"{BILL_LAW_LIFECYCLE_CORPUS}: no rows")
    if not bill_finance_lobbying_review_queue:
        failures.append(f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: no rows")
    if not bill_finance_lobbying_local_context_review_raw:
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW}: no rows")
    if not bill_finance_lobbying_local_context_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: no rows")
    if not bill_finance_lobbying_external_lda_searches_raw:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: no rows")
    if not bill_finance_lobbying_external_lda_mentions_raw:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: no rows")
    if not bill_finance_lobbying_external_search_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: no rows")
    if not bill_finance_lobbying_external_lda_mention_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: no rows")
    if not bill_finance_lobbying_campaign_finance_target_scope_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: no rows")
    if not bill_finance_lobbying_committee_action_context:
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: no rows")
    if not bill_finance_lobbying_committee_action_source_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: no rows")
    if not bill_finance_lobbying_roll_call_source_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: no rows")
    if not bill_finance_lobbying_member_vote_target_review:
        failures.append(f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: no rows")
    if not bill_finance_lobbying_source_acquisition_queue:
        failures.append(f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: no rows")
    if not statutory_lineage_review_queue:
        failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: no rows")
    if not statutory_lineage_source_scan:
        failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: no rows")
    if not statutory_lineage_target_section_triage:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: no rows")
    if not statutory_lineage_olrc_current_scan:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: no rows")
    if not statutory_lineage_olrc_historical_scan:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: no rows")
    if not statutory_lineage_olrc_annual_text_diff:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: no rows")
    if not statutory_lineage_adjudication:
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: no rows")
    if not statutory_lineage_target_review_packets:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: no rows")
    if not statutory_lineage_target_section_diff_review:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: no rows")
    if not statutory_lineage_no_target_review:
        failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: no rows")
    if not statutory_lineage_target_lifecycle_bridge:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: no rows")
    if not statutory_lineage_codified_progress:
        failures.append(f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: no rows")
    if not statutory_lineage_effective_text_review:
        failures.append(f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: no rows")
    if not statutory_lineage_public_law_attribution_review:
        failures.append(f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: no rows")
    if not statutory_lineage_completion_queue:
        failures.append(f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: no rows")
    if not statutory_lineage_complete_lineage_expansion_queue:
        failures.append(f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: no rows")
    if not statutory_lineage_target_packet_expansion_queue:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: no rows")
    if not statutory_lineage_target_packet_source_gap_queue:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: no rows")
    if not court_public_law_review_queue:
        failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: no rows")
    if not court_public_law_temporal_triage:
        failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: no rows")
    if not court_public_law_direct_review_raw:
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: no rows")
    if not court_public_law_direct_review:
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: no rows")
    if not rulemaking_authority_linkage:
        failures.append(f"{RULEMAKING_AUTHORITY_LINKAGE}: no rows")
    if not rulemaking_history_linkage:
        failures.append(f"{RULEMAKING_HISTORY_LINKAGE}: no rows")
    if not rulemaking_comment_metadata:
        failures.append(f"{RULEMAKING_COMMENT_METADATA}: no rows")
    if not rulemaking_comment_records:
        failures.append(f"{RULEMAKING_COMMENT_RECORDS}: no rows")
    if not rulemaking_comment_text_review:
        failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: no rows")
    if not campaign_finance_district_context:
        failures.append(f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: no rows")
    if not campaign_finance_member_context:
        failures.append(f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: no rows")
    if not campaign_finance_issue_context:
        failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: no rows")
    if not campaign_finance_sponsor_bill_context:
        failures.append(f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: no rows")
    if not district_public_opinion_policy_context:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: no rows")
    if not district_public_opinion_bill_topic_readiness:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: no rows")
    if not district_public_opinion_source_packets:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: no rows")
    if not district_public_opinion_census_denominators:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: no rows")
    if not district_public_opinion_acs_context_raw:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: no rows")
    if not district_public_opinion_acs_context:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: no rows")
    if not district_public_opinion_survey_source_crosswalk:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: no rows")
    if not district_public_opinion_survey_item_proxy_review:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: no rows")
    if not district_public_opinion_ces_policy_item_candidates_raw:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: no rows")
    if not district_public_opinion_ces_policy_item_candidate_review:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: no rows")
    if not district_public_opinion_ces_policy_item_response_distributions_raw:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: no rows")
    if not district_public_opinion_ces_policy_item_response_distribution_review:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: no rows")
    if not district_public_opinion_ces_policy_item_codebook_direction_raw:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: no rows")
    if not district_public_opinion_ces_policy_item_codebook_direction_review:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: no rows")
    if failures:
        return failures

    try:
        registry_by_family = by_field(registry, "source_family")
        inventory_by_family = by_field(inventory, "sourceFamily")
        gap_by_family = by_field(gap, "sourceFamily")
        linkage_by_family = by_field(linkage, "sourceFamily")
        roadmap_by_family = by_field(roadmap, "sourceFamily")
        raw_manifest_by_family = by_field(raw_manifest, "sourceFamily")
    except ValueError as exception:
        return [str(exception)]

    registry_families = set(registry_by_family)
    inventory_families = set(inventory_by_family)
    gap_families = set(gap_by_family)
    linkage_families = set(linkage_by_family)
    roadmap_families = set(roadmap_by_family)
    raw_manifest_families = set(raw_manifest_by_family)
    if registry_families != inventory_families:
        failures.append(
            "registry/inventory source-family mismatch: "
            f"missing from inventory={sorted(registry_families - inventory_families)}, "
            f"extra={sorted(inventory_families - registry_families)}"
        )
    if registry_families != gap_families:
        failures.append(
            "registry/gap source-family mismatch: "
            f"missing from gap={sorted(registry_families - gap_families)}, "
            f"extra={sorted(gap_families - registry_families)}"
        )
    if registry_families != linkage_families:
        failures.append(
            "registry/linkage source-family mismatch: "
            f"missing from linkage={sorted(registry_families - linkage_families)}, "
            f"extra={sorted(linkage_families - registry_families)}"
        )
    roadmap_required_families = {
        row.get("sourceFamily", "")
        for row in linkage
        if row.get("linkageStatus") != "linked"
    }
    if roadmap_families != roadmap_required_families:
        failures.append(
            "linkage/roadmap source-family mismatch: "
            f"missing from roadmap={sorted(roadmap_required_families - roadmap_families)}, "
            f"extra={sorted(roadmap_families - roadmap_required_families)}"
        )
    if registry_families != raw_manifest_families:
        failures.append(
            "registry/raw-source-manifest source-family mismatch: "
            f"missing from manifest={sorted(registry_families - raw_manifest_families)}, "
            f"extra={sorted(raw_manifest_families - registry_families)}"
        )
    if statutory_lineage_target_packet_expansion_queue:
        for report_path, report_row in (
            (LINKAGE, linkage_by_family.get("Statutory revision and law lineage", {})),
            (GAP, gap_by_family.get("Statutory revision and law lineage", {})),
        ):
            boundary = report_row.get("linkageBoundary", "")
            for phrase in (
                "target-packet expansion queue",
                "target-packet source-gap queue",
                "source-gap disposition review",
                "direct U.S.C. note-review",
                "title-only manual-target",
                "incomplete-fragment manual-review",
                "current OLRC pages without a public-law marker",
                "public-law marker but no downstream packet",
                "manual current-scan source-gap review",
                "target-reference resolution candidate report",
                "bounded concrete U.S.C.",
                "without bounded source-scan candidates",
            ):
                if phrase not in boundary:
                    failures.append(
                        f"{report_path}: Statutory revision and law lineage boundary "
                        f"must mention packet expansion detail {phrase!r}"
                    )
            next_step = report_row.get("nextLinkStep", "")
            for phrase in (
                "target-reference resolution candidate report",
                "bounded concrete U.S.C.",
                "ambiguous packet blockers",
                "target-packet source-gap queue",
                "source-gap disposition review",
                "current OLRC pages without public-law markers",
                "current pages with public-law markers",
                "current-scan source-gap rows",
            ):
                if phrase not in next_step:
                    failures.append(
                        f"{report_path}: Statutory revision and law lineage next step "
                        f"must prioritize packet source-gap detail {phrase!r}"
                    )
        statutory_roadmap_row = roadmap_by_family.get("Statutory revision and law lineage", {})
        if statutory_roadmap_row:
            roadmap_text = " ".join(
                statutory_roadmap_row.get(field, "")
                for field in (
                    "blockingGap",
                    "minimumViableDataset",
                    "acceptanceGate",
                    "claimUpgradeBoundary",
                )
            )
            for phrase in (
                "target-packet expansion queue",
                "target-packet source-gap queue",
                "source-gap disposition review",
                "concrete U.S.C. note-review",
                "manual source-gap review",
                "current OLRC pages without public-law markers",
                "current pages with public-law markers",
                "target-reference resolution candidate report",
                "concrete U.S.C. candidates",
                "no-candidate",
            ):
                if phrase not in roadmap_text:
                    failures.append(
                        f"{ROADMAP}: Statutory revision and law lineage roadmap "
                        f"must mention packet expansion detail {phrase!r}"
                    )
            if (
                statutory_roadmap_row.get("futureTarget", "")
                != "make statutory-lineage-target-reference-resolution-candidates"
            ):
                failures.append(
                    f"{ROADMAP}: Statutory revision and law lineage future target "
                    "must point to the target-reference resolution candidate report"
                )

    bill_progression_rows = read_csv(BILL_PROGRESSION)
    govinfo_billstatus_raw = read_csv(GOVINFO_BILLSTATUS_LINKAGE_RAW)
    sponsor_success_rows = read_csv(SPONSOR_SUCCESS)
    sponsor_bill_linkage_raw = read_csv(SPONSOR_BILL_LINKAGE_RAW)
    comparative_institution_rows = read_csv(COMPARATIVE_INSTITUTIONS)
    comparative_institution_linkage_raw = read_csv(COMPARATIVE_INSTITUTION_LINKAGE_RAW)
    law_revision_rows = read_csv(LAW_REVISION_HISTORY)
    law_bill_rows = read_csv(LAW_REVISION_BILL_LINKAGE)
    rulemaking_authority_raw = read_csv(RULEMAKING_AUTHORITY_LINKAGE_RAW)
    rulemaking_history_raw = read_csv(RULEMAKING_HISTORY_LINKAGE_RAW)
    rulemaking_comment_metadata_raw = read_csv(RULEMAKING_COMMENT_METADATA_RAW)
    rulemaking_comment_records_raw = read_csv(RULEMAKING_COMMENT_RECORDS_RAW)
    rulemaking_comment_text_review_raw = read_csv(RULEMAKING_COMMENT_TEXT_REVIEW_RAW)
    district_linkage_rows = read_csv(DISTRICT_PUBLIC_OPINION_LINKAGE)
    voteview_rollcall_rows = read_csv(VOTEVIEW_ROLLCALLS)
    voteview_member_context_raw = read_csv(VOTEVIEW_MEMBER_CONTEXT_RAW)
    voteview_bill_linkage_raw = read_csv(VOTEVIEW_BILL_LINKAGE_RAW)
    lobbying_issue_linkage_raw = read_csv(LOBBYING_ISSUE_LINKAGE_RAW)
    lobbying_bill_mentions_raw = read_csv(LOBBYING_BILL_MENTIONS_RAW)
    lobbying_bill_mention_searches_raw = read_csv(LOBBYING_BILL_MENTION_SEARCHES_RAW)
    campaign_linkage_rows = read_csv(CAMPAIGN_FINANCE_LINKAGE)
    campaign_member_context_raw = read_csv(CAMPAIGN_FINANCE_MEMBER_CONTEXT_RAW)
    campaign_finance_rows = read_csv(CAMPAIGN_FINANCE)
    campaign_issue_context_raw = read_csv(CAMPAIGN_FINANCE_ISSUE_CONTEXT_RAW)
    district_policy_context_raw = read_csv(DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT_RAW)
    district_census_denominators_raw = read_csv(DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW)
    district_opinion_rows = read_csv(DISTRICT_PUBLIC_OPINION)
    statutory_lineage_source_scan_raw = read_csv(STATUTORY_LINEAGE_SOURCE_SCAN_RAW)
    statutory_lineage_olrc_current_scan_raw = read_csv(STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_RAW)
    statutory_lineage_olrc_historical_scan_raw = read_csv(STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_RAW)
    statutory_lineage_olrc_annual_text_diff_raw = read_csv(STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_RAW)
    statutory_lineage_adjudication_raw = read_csv(STATUTORY_LINEAGE_ADJUDICATION_RAW)
    statutory_lineage_target_review_packets_raw = read_csv(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW)
    statutory_lineage_target_section_diff_review_raw = read_csv(
        STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW
    )
    statutory_lineage_no_target_review_raw = read_csv(STATUTORY_LINEAGE_NO_TARGET_REVIEW_RAW)
    bill_finance_lobbying_roll_call_source_raw = read_csv(BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_RAW)
    bill_finance_lobbying_member_vote_target_raw = read_csv(BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_RAW)
    court_review_rows = read_csv(COURT_REVIEW)
    court_law_linkage_raw = read_csv(COURT_LAW_LINKAGE_RAW)
    lobbying_disclosure_rows = read_csv(LOBBYING_DISCLOSURE)
    topic_throughput_rows = read_csv(TOPIC_THROUGHPUT)
    spine_bill_ids = {row.get("bill_id", "") for row in bill_law_spine if row.get("bill_id")}
    law_bill_ids = {row.get("bill_id", "") for row in law_bill_rows if row.get("bill_id")}
    required_govinfo_columns = {
        "bill_id",
        "congress",
        "bill_type",
        "bill_number",
        "linkage_status",
        "introduced_date",
        "latest_action_date",
        "actions_count",
        "policy_area",
        "committee_reported",
        "floor_considered",
        "enacted",
        "action_alignment_status",
        "policy_area_alignment_status",
        "evidence_layers",
        "missing_links",
        "govinfo_url",
        "claim_boundary",
    }
    missing_govinfo_columns = required_govinfo_columns - set(govinfo_billstatus_linkage[0])
    if missing_govinfo_columns:
        failures.append(
            f"{GOVINFO_BILLSTATUS_LINKAGE}: missing columns {sorted(missing_govinfo_columns)}"
        )
    govinfo_report_keys = {bill_key(row) for row in govinfo_billstatus_linkage}
    govinfo_raw_keys = {bill_key(row) for row in govinfo_billstatus_raw}
    bill_progression_keys = {bill_key(row) for row in bill_progression_rows}
    if govinfo_report_keys != govinfo_raw_keys:
        failures.append(
            "govinfo BILLSTATUS report/raw mismatch: "
            f"missing from report={sorted(govinfo_raw_keys - govinfo_report_keys)}, "
            f"extra={sorted(govinfo_report_keys - govinfo_raw_keys)}"
        )
    if govinfo_raw_keys != bill_progression_keys:
        failures.append(
            "govinfo BILLSTATUS/bill-progression key mismatch: "
            f"missing from govinfo={sorted(bill_progression_keys - govinfo_raw_keys)[:10]}, "
            f"extra={sorted(govinfo_raw_keys - bill_progression_keys)[:10]}"
        )
    govinfo_metadata_rows = [
        row for row in govinfo_billstatus_linkage
        if row.get("linkage_status") == "govinfo_billstatus_metadata"
    ]
    if not govinfo_metadata_rows:
        failures.append(f"{GOVINFO_BILLSTATUS_LINKAGE}: expected at least one govinfo metadata row")
    govinfo_linkage_row = linkage_by_family.get("govinfo bill and action records", {})
    if govinfo_linkage_row:
        try:
            govinfo_linked_rows = int(govinfo_linkage_row.get("linkedRows", "0") or "0")
        except ValueError:
            failures.append(f"{LINKAGE}: govinfo bill and action records: linkedRows is not an integer")
        else:
            if govinfo_linked_rows != len(govinfo_metadata_rows):
                failures.append(
                    f"{LINKAGE}: govinfo linkedRows {govinfo_linked_rows} "
                    f"does not match {GOVINFO_BILLSTATUS_LINKAGE} metadata rows {len(govinfo_metadata_rows)}"
                )
            if govinfo_metadata_rows and govinfo_linkage_row.get("linkageStatus") == "not independently linked":
                failures.append(
                    f"{LINKAGE}: govinfo should not remain not independently linked when BILLSTATUS rows are present"
                )
    valid_action_statuses = {"aligned", "flag_difference", "unavailable"}
    valid_policy_statuses = {"aligned", "different", "unavailable"}
    for row in govinfo_billstatus_linkage:
        key = bill_key(row)
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "public-opinion" not in boundary
            or "full bill census" not in boundary
        ):
            failures.append(
                f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: "
                "claim_boundary must reject full-census, public-opinion, and model-validation claims"
            )
        expected_id = "-".join(key)
        if row.get("bill_id", "") != expected_id:
            failures.append(
                f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: bill_id {row.get('bill_id')!r} "
                f"does not match key {expected_id!r}"
            )
        if not row.get("govinfo_url", "").startswith("https://www.govinfo.gov/bulkdata/BILLSTATUS/"):
            failures.append(f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: invalid govinfo_url")
        if row.get("action_alignment_status") not in valid_action_statuses:
            failures.append(
                f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: invalid action_alignment_status "
                f"{row.get('action_alignment_status')!r}"
            )
        if row.get("policy_area_alignment_status") not in valid_policy_statuses:
            failures.append(
                f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: invalid policy_area_alignment_status "
                f"{row.get('policy_area_alignment_status')!r}"
            )
        if row.get("linkage_status") == "govinfo_billstatus_metadata":
            if "govinfo_billstatus_metadata" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: metadata row missing evidence layer"
                )
            try:
                int(row.get("actions_count", "0") or "0")
            except ValueError:
                failures.append(f"{GOVINFO_BILLSTATUS_LINKAGE}: {key}: actions_count is not an integer")
    required_sponsor_bill_columns = {
        "sponsor_id",
        "party",
        "introduced",
        "enacted",
        "linkage_status",
        "matched_govinfo_bill_count",
        "matched_govinfo_enacted_count",
        "matched_public_law_bill_count",
        "matched_bill_ids",
        "matched_public_law_numbers",
        "matched_policy_areas",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_sponsor_bill_columns = required_sponsor_bill_columns - set(sponsor_bill_linkage[0])
    if missing_sponsor_bill_columns:
        failures.append(
            f"{SPONSOR_BILL_LINKAGE}: missing columns {sorted(missing_sponsor_bill_columns)}"
        )
    if not SPONSOR_BILL_LINKAGE_MD.exists():
        failures.append(f"{SPONSOR_BILL_LINKAGE_MD}: missing markdown report")
    sponsor_ids = {row.get("sponsor_id", "").strip() for row in sponsor_success_rows if row.get("sponsor_id", "").strip()}
    sponsor_raw_ids = {row.get("sponsor_id", "").strip() for row in sponsor_bill_linkage_raw if row.get("sponsor_id", "").strip()}
    sponsor_report_ids = {row.get("sponsor_id", "").strip() for row in sponsor_bill_linkage if row.get("sponsor_id", "").strip()}
    if sponsor_report_ids != sponsor_raw_ids:
        failures.append(
            "sponsor-bill linkage report/raw mismatch: "
            f"missing from report={sorted(sponsor_raw_ids - sponsor_report_ids)}, "
            f"extra={sorted(sponsor_report_ids - sponsor_raw_ids)}"
        )
    if sponsor_raw_ids != sponsor_ids:
        failures.append(
            "sponsor-bill linkage/sponsor-success mismatch: "
            f"missing from linkage={sorted(sponsor_ids - sponsor_raw_ids)}, "
            f"extra={sorted(sponsor_raw_ids - sponsor_ids)}"
        )
    govinfo_bills_by_sponsor: dict[str, set[str]] = defaultdict(set)
    govinfo_enacted_by_sponsor: dict[str, set[str]] = defaultdict(set)
    for row in govinfo_billstatus_raw:
        sponsor_id = row.get("sponsor_bioguide_id", "").strip()
        bill_id = row.get("bill_id", "").strip()
        if not sponsor_id or not bill_id:
            continue
        govinfo_bills_by_sponsor[sponsor_id].add(bill_id)
        if row.get("enacted", "").strip() == "1":
            govinfo_enacted_by_sponsor[sponsor_id].add(bill_id)
    public_laws_by_sponsor: dict[str, set[str]] = defaultdict(set)
    for row in law_bill_rows:
        sponsor_id = row.get("sponsor_bioguide_id", "").strip()
        public_law = row.get("public_law_number", "").strip()
        if sponsor_id and public_law:
            public_laws_by_sponsor[sponsor_id].add(public_law)
    sponsor_matched_rows = [
        row for row in sponsor_bill_linkage
        if row.get("linkage_status") == "sponsor_bill_metadata"
    ]
    if not sponsor_matched_rows:
        failures.append(f"{SPONSOR_BILL_LINKAGE}: expected at least one sponsor bill-metadata row")
    sponsor_linkage_row = linkage_by_family.get("Center for Effective Lawmaking and sponsor histories", {})
    if sponsor_linkage_row:
        try:
            sponsor_linked_rows = int(sponsor_linkage_row.get("linkedRows", "0") or "0")
        except ValueError:
            failures.append(f"{LINKAGE}: Center for Effective Lawmaking and sponsor histories: linkedRows is not an integer")
        else:
            if sponsor_linked_rows != len(sponsor_matched_rows):
                failures.append(
                    f"{LINKAGE}: sponsor linkedRows {sponsor_linked_rows} "
                    f"does not match {SPONSOR_BILL_LINKAGE} matched rows {len(sponsor_matched_rows)}"
                )
            if sponsor_matched_rows and sponsor_linkage_row.get("linkageStatus") == "not linked":
                failures.append(f"{LINKAGE}: sponsor history should not remain not linked when sponsor-bill rows are present")
    for row in sponsor_bill_linkage:
        sponsor_id = row.get("sponsor_id", "").strip()
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "full Center for Effective Lawmaking" not in boundary
            or "legislative quality" not in boundary
        ):
            failures.append(
                f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: "
                "claim_boundary must reject CEL, legislative-quality, and model-validation claims"
            )
        try:
            matched_bills = int(row.get("matched_govinfo_bill_count", "0") or "0")
            matched_enacted = int(row.get("matched_govinfo_enacted_count", "0") or "0")
            matched_public_laws = int(row.get("matched_public_law_bill_count", "0") or "0")
        except ValueError:
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: counts must be integers")
            continue
        expected_bills = govinfo_bills_by_sponsor.get(sponsor_id, set())
        expected_enacted = govinfo_enacted_by_sponsor.get(sponsor_id, set())
        expected_public_laws = public_laws_by_sponsor.get(sponsor_id, set())
        actual_bills = {bill.strip() for bill in row.get("matched_bill_ids", "").split(";") if bill.strip()}
        actual_public_laws = {law.strip() for law in row.get("matched_public_law_numbers", "").split(";") if law.strip()}
        if actual_bills != expected_bills:
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched bill set does not match govinfo sponsor metadata")
        if actual_public_laws != expected_public_laws:
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: public-law set does not match law-revision sponsor metadata")
        if matched_bills != len(expected_bills):
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched bill count does not match govinfo sponsor metadata")
        if matched_enacted != len(expected_enacted):
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched enacted count does not match govinfo sponsor metadata")
        if matched_public_laws != len(expected_public_laws):
            failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: public-law count does not match law-revision sponsor metadata")
        if row.get("linkage_status") == "sponsor_bill_metadata":
            if matched_bills <= 0 or not actual_bills:
                failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched row missing bill IDs")
            if "govinfo_billstatus_sponsor_metadata" not in row.get("evidence_layers", ""):
                failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched row missing evidence layer")
            if "public_bill_metadata_match" in row.get("missing_links", ""):
                failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: matched row still lists bill metadata as missing")
        else:
            if matched_bills or actual_bills:
                failures.append(f"{SPONSOR_BILL_LINKAGE}: {sponsor_id}: unmatched row should not carry bill IDs")
    required_comparative_columns = {
        "iso3",
        "country",
        "year",
        "chambers",
        "district_magnitude",
        "party_fragmentation",
        "judicial_review",
        "legislative_constraint_proxy",
        "linkage_status",
        "matched_institution_family",
        "matched_scenario_keys",
        "matched_scenario_count",
        "chamber_anchor",
        "district_magnitude_band",
        "party_system_band",
        "judicial_review_band",
        "legislative_constraint_band",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_comparative_columns = required_comparative_columns - set(comparative_institution_linkage[0])
    if missing_comparative_columns:
        failures.append(
            f"{COMPARATIVE_INSTITUTION_LINKAGE}: missing columns {sorted(missing_comparative_columns)}"
        )
    if not COMPARATIVE_INSTITUTION_LINKAGE_MD.exists():
        failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE_MD}: missing markdown report")
    comparative_keys = {
        (row.get("iso3", "").strip(), row.get("year", "").strip())
        for row in comparative_institution_rows
        if row.get("iso3", "").strip() and row.get("year", "").strip()
    }
    comparative_raw_keys = {
        (row.get("iso3", "").strip(), row.get("year", "").strip())
        for row in comparative_institution_linkage_raw
        if row.get("iso3", "").strip() and row.get("year", "").strip()
    }
    comparative_report_keys = {
        (row.get("iso3", "").strip(), row.get("year", "").strip())
        for row in comparative_institution_linkage
        if row.get("iso3", "").strip() and row.get("year", "").strip()
    }
    if comparative_report_keys != comparative_raw_keys:
        failures.append(
            "comparative-institution linkage report/raw mismatch: "
            f"missing from report={sorted(comparative_raw_keys - comparative_report_keys)}, "
            f"extra={sorted(comparative_report_keys - comparative_raw_keys)}"
        )
    if comparative_raw_keys != comparative_keys:
        failures.append(
            "comparative-institution linkage/source mismatch: "
            f"missing from linkage={sorted(comparative_keys - comparative_raw_keys)[:10]}, "
            f"extra={sorted(comparative_raw_keys - comparative_keys)[:10]}"
        )
    comparative_matched_rows = [
        row for row in comparative_institution_linkage
        if row.get("linkage_status") == "comparative_institution_metadata"
    ]
    if not comparative_matched_rows:
        failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: expected at least one metadata row")
    comparative_linkage_row = linkage_by_family.get("QoG and V-Dem comparative institutions", {})
    if comparative_linkage_row:
        try:
            comparative_linked_rows = int(comparative_linkage_row.get("linkedRows", "0") or "0")
        except ValueError:
            failures.append(f"{LINKAGE}: QoG and V-Dem comparative institutions: linkedRows is not an integer")
        else:
            if comparative_linked_rows != len(comparative_matched_rows):
                failures.append(
                    f"{LINKAGE}: comparative linkedRows {comparative_linked_rows} "
                    f"does not match {COMPARATIVE_INSTITUTION_LINKAGE} metadata rows {len(comparative_matched_rows)}"
                )
            if comparative_matched_rows and comparative_linkage_row.get("linkageStatus") == "not linked":
                failures.append(f"{LINKAGE}: comparative institutions should not remain not linked when metadata rows are present")
    valid_chamber_anchors = {"unicameral", "bicameral", "no_effective_chamber"}
    valid_district_bands = {
        "single_member_or_near_single_member",
        "moderate_magnitude",
        "high_magnitude",
    }
    valid_party_bands = {
        "two_party_or_low_fragmentation",
        "moderate_multipartism",
        "high_fragmentation",
    }
    valid_review_bands = {
        "weak_judicial_constraints",
        "moderate_judicial_constraints",
        "strong_judicial_constraints",
    }
    valid_constraint_bands = {
        "low_legislative_constraints",
        "moderate_legislative_constraints",
        "high_legislative_constraints",
    }
    for row in comparative_institution_linkage:
        key = (row.get("iso3", "").strip(), row.get("year", "").strip())
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "observed law-output" not in boundary
            or "institutional fit" not in boundary
        ):
            failures.append(
                f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: "
                "claim_boundary must reject observed-output, institutional-fit, and model-validation claims"
            )
        if row.get("chamber_anchor") not in valid_chamber_anchors:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: invalid chamber_anchor")
        if row.get("district_magnitude_band") not in valid_district_bands:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: invalid district_magnitude_band")
        if row.get("party_system_band") not in valid_party_bands:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: invalid party_system_band")
        if row.get("judicial_review_band") not in valid_review_bands:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: invalid judicial_review_band")
        if row.get("legislative_constraint_band") not in valid_constraint_bands:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: invalid legislative_constraint_band")
        scenario_keys = [value for value in row.get("matched_scenario_keys", "").split(";") if value]
        try:
            matched_scenario_count = int(row.get("matched_scenario_count", "0") or "0")
        except ValueError:
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: matched_scenario_count must be an integer")
            continue
        if matched_scenario_count != len(scenario_keys):
            failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: matched_scenario_count does not match scenario key list")
        if row.get("linkage_status") == "comparative_institution_metadata":
            if not scenario_keys or matched_scenario_count <= 0:
                failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: metadata row missing scenario anchors")
            if "simulator_scenario_family_anchor" not in row.get("evidence_layers", ""):
                failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: metadata row missing evidence layer")
            if "observed_law_output" not in row.get("missing_links", ""):
                failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: metadata row must keep observed output missing")
        else:
            if scenario_keys:
                failures.append(f"{COMPARATIVE_INSTITUTION_LINKAGE}: {key}: unmatched row should not carry scenario keys")
    required_lobbying_issue_columns = {
        "lobbying_issue",
        "topic",
        "linkage_status",
        "lobbying_rows",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_lobbying_issue_columns = required_lobbying_issue_columns - set(lobbying_issue_linkage[0])
    if missing_lobbying_issue_columns:
        failures.append(
            f"{LOBBYING_ISSUE_LINKAGE}: missing columns {sorted(missing_lobbying_issue_columns)}"
        )
    issue_counts = Counter(row.get("issue", "").strip() for row in lobbying_disclosure_rows)
    issue_counts.pop("", None)
    issue_report_keys = {row.get("lobbying_issue", "").strip() for row in lobbying_issue_linkage}
    issue_raw_keys = {row.get("lobbying_issue", "").strip() for row in lobbying_issue_linkage_raw}
    if issue_report_keys != issue_raw_keys:
        failures.append(
            "lobbying issue-linkage report/raw mismatch: "
            f"missing from report={sorted(issue_raw_keys - issue_report_keys)}, "
            f"extra={sorted(issue_report_keys - issue_raw_keys)}"
        )
    if issue_report_keys != set(issue_counts):
        failures.append(
            "lobbying issue-linkage report/LDA sample mismatch: "
            f"missing from report={sorted(set(issue_counts) - issue_report_keys)}, "
            f"extra={sorted(issue_report_keys - set(issue_counts))}"
        )
    topic_values = {
        row.get("topic", "").strip()
        for row in topic_throughput_rows
        if row.get("topic", "").strip()
    }
    exact_topic_matches = {issue for issue in issue_counts if issue in topic_values}
    crosswalk_topics = {
        row.get("topic", "").strip()
        for row in lobbying_issue_linkage
        if row.get("linkage_status") == "issue_topic_crosswalk"
    }
    if not crosswalk_topics:
        failures.append(f"{LOBBYING_ISSUE_LINKAGE}: expected at least one issue-topic crosswalk row")
    if not crosswalk_topics <= topic_values:
        failures.append(
            f"{LOBBYING_ISSUE_LINKAGE}: mapped topics not present in topic throughput: "
            f"{sorted(crosswalk_topics - topic_values)}"
        )
    mapped_issue_rows = {
        row.get("lobbying_issue", "").strip()
        for row in lobbying_issue_linkage
        if row.get("linkage_status") == "issue_topic_crosswalk"
    }
    if len(mapped_issue_rows) <= len(exact_topic_matches):
        failures.append(
            f"{LOBBYING_ISSUE_LINKAGE}: crosswalk does not improve on exact topic-label coverage"
        )
    for row in lobbying_issue_linkage:
        issue = row.get("lobbying_issue", "").strip()
        boundary = row.get("claim_boundary", "")
        if "model validation" not in boundary or "bill-level" not in boundary or "causal capture" not in boundary:
            failures.append(
                f"{LOBBYING_ISSUE_LINKAGE}: {issue}: "
                "claim_boundary must reject bill-level lobbying influence, causal capture, and model validation"
            )
        try:
            row_count = int(row.get("lobbying_rows", "0") or "0")
        except ValueError:
            failures.append(f"{LOBBYING_ISSUE_LINKAGE}: {issue}: lobbying_rows is not an integer")
            continue
        if row_count != issue_counts.get(issue, 0):
            failures.append(
                f"{LOBBYING_ISSUE_LINKAGE}: {issue}: lobbying_rows {row_count} "
                f"does not match {LOBBYING_DISCLOSURE} count {issue_counts.get(issue, 0)}"
            )
        if row.get("linkage_status") == "issue_topic_crosswalk" and not row.get("topic", "").strip():
            failures.append(f"{LOBBYING_ISSUE_LINKAGE}: {issue}: crosswalk row missing topic")
        if row.get("linkage_status") != "issue_topic_crosswalk" and row.get("topic", "").strip():
            failures.append(f"{LOBBYING_ISSUE_LINKAGE}: {issue}: unmatched row should not carry topic")

    required_lobbying_bill_policy_columns = {
        "lobbying_issue",
        "topic",
        "policy_context_status",
        "lobbying_rows",
        "unique_clients",
        "unique_filings",
        "total_amount",
        "matched_govinfo_bill_count",
        "matched_govinfo_floor_considered_count",
        "matched_govinfo_committee_reported_count",
        "matched_govinfo_enacted_count",
        "matched_sponsor_bioguide_count",
        "matched_committee_code_count",
        "matched_bill_ids",
        "matched_enacted_bill_ids",
        "matched_sponsor_bioguide_ids",
        "matched_committee_codes",
        "evidence_layers",
        "missing_links",
        "match_basis",
        "claim_boundary",
    }
    missing_lobbying_bill_policy_columns = (
        required_lobbying_bill_policy_columns - set(lobbying_bill_policy_context[0])
    )
    if missing_lobbying_bill_policy_columns:
        failures.append(
            f"{LOBBYING_BILL_POLICY_CONTEXT}: missing columns {sorted(missing_lobbying_bill_policy_columns)}"
        )
    if not LOBBYING_BILL_POLICY_CONTEXT_MD.exists():
        failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT_MD}: missing markdown report")
    bill_policy_report_keys = {
        row.get("lobbying_issue", "").strip()
        for row in lobbying_bill_policy_context
        if row.get("lobbying_issue", "").strip()
    }
    if bill_policy_report_keys != issue_raw_keys:
        failures.append(
            "lobbying bill-policy context report/raw mismatch: "
            f"missing from report={sorted(issue_raw_keys - bill_policy_report_keys)}, "
            f"extra={sorted(bill_policy_report_keys - issue_raw_keys)}"
        )
    lobbying_issue_raw_by_issue = {
        row.get("lobbying_issue", "").strip(): row
        for row in lobbying_issue_linkage_raw
        if row.get("lobbying_issue", "").strip()
    }
    govinfo_bills_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in govinfo_billstatus_raw:
        policy_area = row.get("policy_area", "").strip()
        bill_id = row.get("bill_id", "").strip()
        if policy_area and bill_id:
            govinfo_bills_by_policy_area[policy_area].append(row)
    bill_policy_context_rows = [
        row for row in lobbying_bill_policy_context
        if row.get("policy_context_status") == "lobbying_issue_bill_policy_context"
    ]
    if not bill_policy_context_rows:
        failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: expected at least one bill policy-context row")
    lda_linkage_row = linkage_by_family.get("Senate LDA lobbying disclosures", {})
    if lda_linkage_row:
        boundary = lda_linkage_row.get("linkageBoundary", "")
        if (
            "issue-policy bill contexts" not in boundary
            or "bill/action context" not in boundary
            or "stored activity-text position signals" not in boundary
            or "support/opposition" not in boundary
            or "client-to-specific-bill" not in boundary
            or "local no-current-match" not in boundary
            or "member-vote target-scope review" not in boundary
        ):
            failures.append(
                f"{LINKAGE}: Senate LDA lobbying disclosures boundary must mention bounded bill-policy context "
                "and bill/action/text-signal/local no-current-match/member-vote target-scope context while "
                "rejecting support/opposition and client-to-specific-bill linkage"
            )
        if bill_finance_lobbying_committee_action_context:
            for phrase in (
                "committee-action context report",
                "cached public bill-action metadata",
                "committee-of-jurisdiction names",
            ):
                if phrase not in boundary:
                    failures.append(
                        f"{LINKAGE}: Senate LDA lobbying disclosures boundary must mention {phrase!r}"
                    )
        next_step = lda_linkage_row.get("nextLinkStep", "")
        if (
            "external LDA mention review" not in next_step
            or "independent contact" not in next_step
            or "campaign-finance target-scope review" not in next_step
            or "direct member target documents" not in next_step
            or "external campaign-finance source documents" not in next_step
        ):
            failures.append(
                f"{LINKAGE}: Senate LDA lobbying disclosures next step should require external LDA mention review "
                "and campaign-finance/member target/source follow-up after target-scope review"
            )
    valid_lobbying_policy_statuses = {
        "lobbying_issue_bill_policy_context",
        "issue_topic_without_cached_bill_policy_context",
        "unmapped_lobbying_issue",
    }
    for row in lobbying_bill_policy_context:
        issue = row.get("lobbying_issue", "").strip()
        source_row = lobbying_issue_raw_by_issue.get(issue, {})
        source_status = source_row.get("linkage_status", "")
        topic = row.get("topic", "").strip()
        status = row.get("policy_context_status", "")
        boundary = row.get("claim_boundary", "")
        if status not in valid_lobbying_policy_statuses:
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: invalid policy_context_status {status!r}")
        if (
            "policy area" not in boundary
            or "specific bill" not in boundary
            or "causal capture" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: "
                "claim_boundary must reject specific-bill lobbying, causal capture, and model validation"
            )
        if row.get("lobbying_rows", "").strip() != source_row.get("lobbying_rows", "").strip():
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: lobbying_rows does not match raw issue linkage"
            )
        expected_bills = govinfo_bills_by_policy_area.get(topic, []) if source_status == "issue_topic_crosswalk" else []
        expected_bill_ids = {bill.get("bill_id", "").strip() for bill in expected_bills if bill.get("bill_id", "").strip()}
        expected_enacted_ids = {
            bill.get("bill_id", "").strip()
            for bill in expected_bills
            if bill.get("bill_id", "").strip() and bill.get("enacted", "").strip() == "1"
        }
        expected_sponsors = {
            bill.get("sponsor_bioguide_id", "").strip()
            for bill in expected_bills
            if bill.get("sponsor_bioguide_id", "").strip()
        }
        expected_committees = {
            code
            for bill in expected_bills
            for code in committee_codes(bill.get("committees", ""))
        }
        actual_bill_ids = split_semicolon_values(row, "matched_bill_ids")
        actual_enacted_ids = split_semicolon_values(row, "matched_enacted_bill_ids")
        actual_sponsors = split_semicolon_values(row, "matched_sponsor_bioguide_ids")
        actual_committees = split_semicolon_values(row, "matched_committee_codes")
        try:
            matched_bill_count = int(row.get("matched_govinfo_bill_count", "0") or "0")
            floor_count = int(row.get("matched_govinfo_floor_considered_count", "0") or "0")
            committee_reported_count = int(row.get("matched_govinfo_committee_reported_count", "0") or "0")
            enacted_count = int(row.get("matched_govinfo_enacted_count", "0") or "0")
            sponsor_count = int(row.get("matched_sponsor_bioguide_count", "0") or "0")
            committee_count = int(row.get("matched_committee_code_count", "0") or "0")
        except ValueError:
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: policy context counts must be integers")
            continue
        if actual_bill_ids != expected_bill_ids:
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: matched bill set does not match govinfo policy-area metadata"
            )
        if actual_enacted_ids != expected_enacted_ids:
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: enacted bill set does not match govinfo policy-area metadata"
            )
        if actual_sponsors != expected_sponsors:
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: sponsor set does not match govinfo policy-area metadata"
            )
        if actual_committees != expected_committees:
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: committee-code set does not match govinfo policy-area metadata"
            )
        if matched_bill_count != len(expected_bill_ids):
            failures.append(
                f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: matched bill count does not match govinfo policy-area metadata"
            )
        if floor_count != sum(1 for bill in expected_bills if bill.get("floor_considered", "").strip() == "1"):
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: floor-considered count mismatch")
        if committee_reported_count != sum(1 for bill in expected_bills if bill.get("committee_reported", "").strip() == "1"):
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: committee-reported count mismatch")
        if enacted_count != len(expected_enacted_ids):
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: enacted count mismatch")
        if sponsor_count != len(expected_sponsors):
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: sponsor count mismatch")
        if committee_count != len(expected_committees):
            failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: committee-code count mismatch")
        if status == "lobbying_issue_bill_policy_context":
            if not expected_bill_ids:
                failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: context row missing expected bill IDs")
            if "govinfo_billstatus_policy_area_metadata" not in row.get("evidence_layers", ""):
                failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: context row missing govinfo evidence layer")
            if "client_to_specific_bill" not in row.get("missing_links", ""):
                failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: context row must keep client-to-specific-bill missing")
        else:
            if actual_bill_ids or matched_bill_count:
                failures.append(f"{LOBBYING_BILL_POLICY_CONTEXT}: {issue}: non-context row should not carry matched bills")

    required_lobbying_bill_mention_search_columns = {
        "bill_id",
        "public_law_number",
        "policy_area",
        "introduced_date",
        "enacted_date",
        "search_term",
        "filing_year",
        "page_count_requested",
        "api_reported_result_count",
        "fetched_filing_count",
        "exact_activity_match_count",
        "api_status",
        "source_url",
        "claim_boundary",
    }
    required_lobbying_bill_mention_columns = {
        "bill_id",
        "public_law_number",
        "policy_area",
        "introduced_date",
        "enacted_date",
        "search_term",
        "filing_year",
        "filing_period",
        "filing_uuid",
        "client_name",
        "registrant_name",
        "filing_document_url",
        "activity_issue",
        "activity_description",
        "matched_bill_refs",
        "exact_current_bill_match",
        "government_entities",
        "source_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    required_lobbying_bill_mention_review_columns = {
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "introduced_date",
        "enacted_date",
        "finance_lobbying_review_queue_rank",
        "searched_status",
        "search_query_count",
        "api_reported_result_count",
        "fetched_filing_count",
        "exact_lda_bill_mention_rows",
        "unique_filing_uuids",
        "unique_clients",
        "unique_registrants",
        "activity_issues",
        "filing_years",
        "filing_periods",
        "filing_document_urls",
        "matched_bill_refs",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    required_lobbying_bill_action_context_columns = {
        "bill_id",
        "public_law_number",
        "policy_area",
        "introduced_date",
        "enacted_date",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "actions_count",
        "committee_reported",
        "floor_considered",
        "enacted",
        "exact_lda_bill_mention_rows",
        "unique_lda_filings",
        "unique_lda_clients",
        "unique_lda_registrants",
        "lda_activity_issues",
        "lda_government_entities",
        "lda_filing_years",
        "lda_filing_periods",
        "lda_matched_bill_refs",
        "lda_filing_document_urls",
        "bill_action_context_status",
        "match_basis",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_text_review_columns = {
        "review_rank",
        "source_row_fingerprint",
        "bill_id",
        "public_law_number",
        "policy_area",
        "filing_uuid",
        "filing_year",
        "filing_period",
        "client_name",
        "registrant_name",
        "activity_issue",
        "matched_bill_refs",
        "stored_activity_text_bill_reference_status",
        "bill_reference_context",
        "bill_reference_context_chars",
        "support_text_signal",
        "opposition_text_signal",
        "position_or_activity_text_signal",
        "text_review_status",
        "specific_bill_text_disposition",
        "government_entity_scope",
        "possible_member_or_committee_reference",
        "source_reviewed_exact_bill_text",
        "evidence_layers",
        "missing_links",
        "filing_document_url",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_disposition_review_columns = {
        "review_rank",
        "source_row_fingerprint",
        "review_priority",
        "manual_review_needed",
        "manual_review_reason",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "committee_reported",
        "floor_considered",
        "enacted",
        "filing_uuid",
        "filing_year",
        "filing_period",
        "client_name",
        "registrant_name",
        "activity_issue",
        "matched_bill_refs",
        "text_review_status",
        "preliminary_text_disposition",
        "support_text_signal",
        "opposition_text_signal",
        "position_or_activity_text_signal",
        "government_entity_scope",
        "possible_member_or_committee_reference",
        "target_review_status",
        "bill_reference_context",
        "recommended_next_review",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_manual_disposition_raw_columns = {
        "source_row_fingerprint",
        "reviewed_bill_id",
        "reviewed_public_law_number",
        "manual_review_source",
        "reviewed_source_url",
        "reviewed_source_text",
        "manual_disposition_status",
        "manual_disposition",
        "manual_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "claim_boundary",
    }
    required_lobbying_bill_manual_disposition_review_columns = {
        "manual_review_rank",
        "queue_review_rank",
        "source_row_fingerprint",
        "bill_id",
        "public_law_number",
        "policy_area",
        "filing_uuid",
        "client_name",
        "registrant_name",
        "activity_issue",
        "text_review_status",
        "queue_review_priority",
        "queue_manual_review_reason",
        "queue_target_review_status",
        "manual_review_source",
        "manual_disposition_status",
        "manual_disposition",
        "manual_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "reviewed_source_text",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_medium_disposition_packet_columns = {
        "packet_rank",
        "packet_fingerprint",
        "review_priority",
        "packet_review_status",
        "direction_signal_summary",
        "rows_represented",
        "source_row_fingerprints",
        "queue_review_ranks",
        "bill_id",
        "public_law_number",
        "policy_area",
        "client_name",
        "registrant_name",
        "activity_issue",
        "text_review_status",
        "manual_review_reason",
        "target_review_status",
        "filing_uuids",
        "filing_years",
        "filing_periods",
        "support_text_signals",
        "opposition_text_signals",
        "position_or_activity_text_signals",
        "distinct_context_count",
        "bill_reference_context_samples",
        "disposition_next_step",
        "target_next_step",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_medium_directional_packet_raw_columns = {
        "packet_fingerprint",
        "reviewed_packet_rank",
        "reviewed_bill_id",
        "reviewed_public_law_number",
        "manual_review_source",
        "manual_packet_disposition_status",
        "manual_packet_disposition",
        "manual_packet_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "claim_boundary",
    }
    required_lobbying_bill_medium_directional_packet_review_columns = {
        "manual_packet_review_rank",
        "packet_rank",
        "packet_fingerprint",
        "bill_id",
        "public_law_number",
        "policy_area",
        "client_name",
        "registrant_name",
        "activity_issue",
        "packet_review_status",
        "direction_signal_summary",
        "rows_represented",
        "source_row_fingerprints",
        "queue_review_ranks",
        "support_text_signals",
        "opposition_text_signals",
        "manual_review_source",
        "manual_packet_disposition_status",
        "manual_packet_disposition",
        "manual_packet_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "bill_reference_context_samples",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    required_lobbying_bill_medium_position_activity_packet_raw_columns = {
        "packet_fingerprint",
        "reviewed_packet_rank",
        "reviewed_bill_id",
        "reviewed_public_law_number",
        "manual_review_source",
        "manual_activity_disposition_status",
        "manual_activity_disposition",
        "manual_activity_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
    }
    required_lobbying_bill_medium_position_activity_packet_review_columns = {
        "manual_packet_review_rank",
        "packet_rank",
        "packet_fingerprint",
        "bill_id",
        "public_law_number",
        "policy_area",
        "client_name",
        "registrant_name",
        "activity_issue",
        "packet_review_status",
        "direction_signal_summary",
        "rows_represented",
        "source_row_fingerprints",
        "queue_review_ranks",
        "position_or_activity_text_signals",
        "support_text_signals",
        "opposition_text_signals",
        "manual_review_source",
        "manual_activity_disposition_status",
        "manual_activity_disposition",
        "manual_activity_disposition_basis",
        "manual_target_status",
        "manual_target_type",
        "manual_target_text",
        "manual_target_basis",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "bill_reference_context_samples",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    if not lobbying_bill_mention_searches_raw:
        failures.append(f"{LOBBYING_BILL_MENTION_SEARCHES_RAW}: no rows")
    else:
        missing_search_columns = (
            required_lobbying_bill_mention_search_columns - set(lobbying_bill_mention_searches_raw[0])
        )
        if missing_search_columns:
            failures.append(
                f"{LOBBYING_BILL_MENTION_SEARCHES_RAW}: missing columns {sorted(missing_search_columns)}"
            )
    if not lobbying_bill_mentions_raw:
        failures.append(f"{LOBBYING_BILL_MENTIONS_RAW}: no exact bill mention rows")
    else:
        missing_mention_columns = (
            required_lobbying_bill_mention_columns - set(lobbying_bill_mentions_raw[0])
        )
        if missing_mention_columns:
            failures.append(
                f"{LOBBYING_BILL_MENTIONS_RAW}: missing columns {sorted(missing_mention_columns)}"
            )
    missing_mention_review_columns = (
        required_lobbying_bill_mention_review_columns - set(lobbying_bill_mention_review[0])
    )
    if missing_mention_review_columns:
        failures.append(
            f"{LOBBYING_BILL_MENTION_REVIEW}: missing columns {sorted(missing_mention_review_columns)}"
        )
    missing_action_context_columns = (
        required_lobbying_bill_action_context_columns - set(lobbying_bill_action_context[0])
    )
    if missing_action_context_columns:
        failures.append(
            f"{LOBBYING_BILL_ACTION_CONTEXT}: missing columns {sorted(missing_action_context_columns)}"
        )
    missing_text_review_columns = (
        required_lobbying_bill_text_review_columns - set(lobbying_bill_text_review[0])
    )
    if missing_text_review_columns:
        failures.append(
            f"{LOBBYING_BILL_TEXT_REVIEW}: missing columns {sorted(missing_text_review_columns)}"
        )
    missing_disposition_review_columns = (
        required_lobbying_bill_disposition_review_columns - set(lobbying_bill_disposition_review[0])
    )
    if missing_disposition_review_columns:
        failures.append(
            f"{LOBBYING_BILL_DISPOSITION_REVIEW}: missing columns {sorted(missing_disposition_review_columns)}"
        )
    if not lobbying_bill_manual_disposition_review_raw:
        failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: no rows")
    else:
        missing_manual_disposition_raw_columns = (
            required_lobbying_bill_manual_disposition_raw_columns
            - set(lobbying_bill_manual_disposition_review_raw[0])
        )
        if missing_manual_disposition_raw_columns:
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: "
                f"missing columns {sorted(missing_manual_disposition_raw_columns)}"
            )
    if not lobbying_bill_manual_disposition_review:
        failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: no rows")
    else:
        missing_manual_disposition_review_columns = (
            required_lobbying_bill_manual_disposition_review_columns
            - set(lobbying_bill_manual_disposition_review[0])
        )
        if missing_manual_disposition_review_columns:
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: "
                f"missing columns {sorted(missing_manual_disposition_review_columns)}"
            )
    if not lobbying_bill_medium_disposition_packets:
        failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: no rows")
    else:
        missing_medium_disposition_packet_columns = (
            required_lobbying_bill_medium_disposition_packet_columns
            - set(lobbying_bill_medium_disposition_packets[0])
        )
        if missing_medium_disposition_packet_columns:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: "
                f"missing columns {sorted(missing_medium_disposition_packet_columns)}"
            )
    if not lobbying_bill_medium_directional_packet_review_raw:
        failures.append(f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: no rows")
    else:
        missing_medium_directional_packet_raw_columns = (
            required_lobbying_bill_medium_directional_packet_raw_columns
            - set(lobbying_bill_medium_directional_packet_review_raw[0])
        )
        if missing_medium_directional_packet_raw_columns:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: "
                f"missing columns {sorted(missing_medium_directional_packet_raw_columns)}"
            )
    if not lobbying_bill_medium_directional_packet_review:
        failures.append(f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: no rows")
    else:
        missing_medium_directional_packet_review_columns = (
            required_lobbying_bill_medium_directional_packet_review_columns
            - set(lobbying_bill_medium_directional_packet_review[0])
        )
        if missing_medium_directional_packet_review_columns:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: "
                f"missing columns {sorted(missing_medium_directional_packet_review_columns)}"
            )
    if not lobbying_bill_medium_position_activity_packet_review_raw:
        failures.append(f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: no rows")
    else:
        missing_medium_position_activity_packet_raw_columns = (
            required_lobbying_bill_medium_position_activity_packet_raw_columns
            - set(lobbying_bill_medium_position_activity_packet_review_raw[0])
        )
        if missing_medium_position_activity_packet_raw_columns:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: "
                f"missing columns {sorted(missing_medium_position_activity_packet_raw_columns)}"
            )
    if not lobbying_bill_medium_position_activity_packet_review:
        failures.append(f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: no rows")
    else:
        missing_medium_position_activity_packet_review_columns = (
            required_lobbying_bill_medium_position_activity_packet_review_columns
            - set(lobbying_bill_medium_position_activity_packet_review[0])
        )
        if missing_medium_position_activity_packet_review_columns:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: "
                f"missing columns {sorted(missing_medium_position_activity_packet_review_columns)}"
            )
    if not LOBBYING_BILL_MENTION_REVIEW_MD.exists():
        failures.append(f"{LOBBYING_BILL_MENTION_REVIEW_MD}: missing markdown report")
    else:
        mention_review_md = LOBBYING_BILL_MENTION_REVIEW_MD.read_text()
        for phrase in (
            "Public-law rows reviewed",
            "Public-law rows searched in cached LDA bill-mention scan",
            "Public-law rows with exact LDA filing-text current-bill mentions",
            "Claim boundary",
        ):
            if phrase not in mention_review_md:
                failures.append(
                    f"{LOBBYING_BILL_MENTION_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_ACTION_CONTEXT_MD.exists():
        failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT_MD}: missing markdown report")
    else:
        action_context_md = LOBBYING_BILL_ACTION_CONTEXT_MD.read_text()
        for phrase in (
            "Public-law bills with exact LDA filing-text bill mentions",
            "Rows with cached bill/action metadata",
            "Rows with enacted public-law outcome metadata",
            "Claim boundary",
        ):
            if phrase not in action_context_md:
                failures.append(
                    f"{LOBBYING_BILL_ACTION_CONTEXT_MD}: missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_TEXT_REVIEW_MD.exists():
        failures.append(f"{LOBBYING_BILL_TEXT_REVIEW_MD}: missing markdown report")
    else:
        text_review_md = LOBBYING_BILL_TEXT_REVIEW_MD.read_text()
        for phrase in (
            "Cached exact LDA activity-text match rows represented",
            "Rows with bill reference located in stored activity text",
            "Rows needing full activity-text refetch before text review",
            "Rows with explicit support text signal",
            "Claim boundary",
        ):
            if phrase not in text_review_md:
                failures.append(
                    f"{LOBBYING_BILL_TEXT_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_DISPOSITION_REVIEW_MD.exists():
        failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW_MD}: missing markdown report")
    else:
        disposition_review_md = LOBBYING_BILL_DISPOSITION_REVIEW_MD.read_text()
        for phrase in (
            "Exact LDA bill-text rows represented",
            "Rows needing manual disposition or target review",
            "High-priority review rows",
            "Claim boundary",
        ):
            if phrase not in disposition_review_md:
                failures.append(
                    f"{LOBBYING_BILL_DISPOSITION_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_MD.exists():
        failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_MD}: missing markdown report")
    else:
        manual_disposition_review_md = LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_MD.read_text()
        for phrase in (
            "High-priority queue rows reviewed",
            "Confirmed current-bill support rows",
            "Rows with support plus opposition to amendments or related measures",
            "Rows with no outcome influence evidence",
            "Claim boundary",
        ):
            if phrase not in manual_disposition_review_md:
                failures.append(
                    f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS_MD.exists():
        failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS_MD}: missing markdown report")
    else:
        medium_disposition_packets_md = LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS_MD.read_text()
        for phrase in (
            "Medium-priority queue rows represented",
            "Medium-priority source-review packets",
            "Rows collapsed by grouping",
            "Explicit support rows represented",
            "Position/activity rows represented",
            "Claim boundary",
        ):
            if phrase not in medium_disposition_packets_md:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_MD.exists():
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_MD}: missing markdown report"
        )
    else:
        medium_directional_packet_review_md = (
            LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_MD.read_text()
        )
        for phrase in (
            "Directional medium-priority packets reviewed",
            "Packets confirming current-bill support",
            "Packets confirming current-bill opposition",
            "Directional packets downgraded",
            "Opposition packets reclassified",
            "Claim boundary",
        ):
            if phrase not in medium_directional_packet_review_md:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    if not LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_MD.exists():
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_MD}: missing markdown report"
        )
    else:
        medium_position_activity_packet_review_md = (
            LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_MD.read_text()
        )
        for phrase in (
            "Position/activity medium-priority packets reviewed",
            "Source rows represented by reviewed position/activity packets",
            "Packets confirming current-bill issue/provision activity without direction",
            "Packets confirming current-bill monitoring or analysis only",
            "Packets listing all provisions without direction",
            "Packets with generic Congress text reference",
            "Packets upgraded to current-bill opposition",
            "Packets with no outcome influence evidence",
            "Claim boundary",
        ):
            if phrase not in medium_position_activity_packet_review_md:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    law_bill_ids_for_lda = {
        row.get("bill_id", "").strip()
        for row in law_bill_rows
        if row.get("bill_id", "").strip()
    }
    lda_review_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in lobbying_bill_mention_review
        if row.get("bill_id", "").strip()
    }
    if set(lda_review_by_bill) != law_bill_ids_for_lda:
        failures.append(
            "LDA bill-mention review/law-linkage mismatch: "
            f"missing from review={sorted(law_bill_ids_for_lda - set(lda_review_by_bill))}, "
            f"extra={sorted(set(lda_review_by_bill) - law_bill_ids_for_lda)}"
        )
    lda_searches_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lobbying_bill_mention_searches_raw:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            lda_searches_by_bill[bill_id].append(row)
        if "not support" not in row.get("claim_boundary", "") or "model validation" not in row.get("claim_boundary", ""):
            failures.append(f"{LOBBYING_BILL_MENTION_SEARCHES_RAW}: {bill_id}: claim boundary is too broad")
    lda_mentions_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lobbying_bill_mentions_raw:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            lda_mentions_by_bill[bill_id].append(row)
        if row.get("exact_current_bill_match", "").strip() != "1":
            failures.append(f"{LOBBYING_BILL_MENTIONS_RAW}: {bill_id}: exact_current_bill_match must be 1")
        if "official_lda_filing_text_bill_identifier" not in row.get("evidence_layers", ""):
            failures.append(f"{LOBBYING_BILL_MENTIONS_RAW}: {bill_id}: missing exact LDA evidence layer")
        if (
            "legislative_outcome_causality" not in row.get("missing_links", "")
            or "causal_capture_validation" not in row.get("missing_links", "")
            or "model_validation" not in row.get("missing_links", "")
        ):
            failures.append(f"{LOBBYING_BILL_MENTIONS_RAW}: {bill_id}: missing causal/validation boundaries")
        if "not support" not in row.get("claim_boundary", "") or "model validation" not in row.get("claim_boundary", ""):
            failures.append(f"{LOBBYING_BILL_MENTIONS_RAW}: {bill_id}: claim boundary is too broad")
    for bill_id, review_row in lda_review_by_bill.items():
        searches = lda_searches_by_bill.get(bill_id, [])
        mentions = lda_mentions_by_bill.get(bill_id, [])
        expected_status = (
            "exact_lda_filing_text_bill_mention_found"
            if mentions else
            "searched_no_exact_lda_filing_text_bill_mention"
            if searches else
            "not_searched_in_current_lda_bill_mention_cache"
        )
        if review_row.get("searched_status", "") != expected_status:
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: searched_status mismatch")
        if parse_int(review_row.get("search_query_count", "")) != len(searches):
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: search_query_count mismatch")
        expected_api_count = sum(parse_int(row.get("api_reported_result_count", "0")) or 0 for row in searches)
        if parse_int(review_row.get("api_reported_result_count", "")) != expected_api_count:
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: api_reported_result_count mismatch")
        expected_fetched_count = sum(parse_int(row.get("fetched_filing_count", "0")) or 0 for row in searches)
        if parse_int(review_row.get("fetched_filing_count", "")) != expected_fetched_count:
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: fetched_filing_count mismatch")
        if parse_int(review_row.get("exact_lda_bill_mention_rows", "")) != len(mentions):
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: exact row-count mismatch")
        if mentions:
            if "official_lda_filing_text_bill_identifier" not in review_row.get("evidence_layers", ""):
                failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: missing exact evidence layer")
            if "filing_text_bill_identifier" in review_row.get("missing_links", ""):
                failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: exact row still lists filing-text identifier as missing")
        else:
            if "official_lda_filing_text_bill_identifier" in review_row.get("evidence_layers", ""):
                failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: non-exact row should not carry exact evidence layer")
        if "not support" not in review_row.get("claim_boundary", "") or "model validation" not in review_row.get("claim_boundary", ""):
            failures.append(f"{LOBBYING_BILL_MENTION_REVIEW}: {bill_id}: claim boundary is too broad")

    law_bill_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in law_bill_rows
        if row.get("bill_id", "").strip()
    }
    action_context_bill_ids = [
        row.get("bill_id", "").strip()
        for row in lobbying_bill_action_context
        if row.get("bill_id", "").strip()
    ]
    action_context_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in lobbying_bill_action_context
        if row.get("bill_id", "").strip()
    }
    if len(action_context_bill_ids) != len(lobbying_bill_action_context):
        failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: blank bill_id rows are not allowed")
    if len(action_context_by_bill) != len(action_context_bill_ids):
        failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: duplicate bill_id rows are not allowed")
    expected_action_bill_ids = set(lda_mentions_by_bill)
    if set(action_context_by_bill) != expected_action_bill_ids:
        failures.append(
            "LDA bill-action context/exact-mention mismatch: "
            f"missing from context={sorted(expected_action_bill_ids - set(action_context_by_bill))}, "
            f"extra={sorted(set(action_context_by_bill) - expected_action_bill_ids)}"
        )

    def expected_lda_values(rows: list[dict[str, str]], field: str) -> set[str]:
        return {
            value
            for mention in rows
            for value in split_semicolon_values(mention, field)
        }

    for bill_id, action_row in sorted(action_context_by_bill.items()):
        mentions = lda_mentions_by_bill.get(bill_id, [])
        law_row = law_bill_by_bill.get(bill_id, {})
        expected_status = (
            "exact_lda_bill_mention_with_bill_action_metadata"
            if law_row else
            "exact_lda_bill_mention_without_cached_bill_action_metadata"
        )
        if action_row.get("bill_action_context_status", "") != expected_status:
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: status mismatch")
        if (parse_int(action_row.get("exact_lda_bill_mention_rows", "")) or 0) != len(mentions):
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: exact LDA row-count mismatch")
        if (parse_int(action_row.get("unique_lda_filings", "")) or 0) != len(expected_lda_values(mentions, "filing_uuid")):
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: unique filing count mismatch")
        if (parse_int(action_row.get("unique_lda_clients", "")) or 0) != len(expected_lda_values(mentions, "client_name")):
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: unique client count mismatch")
        if (parse_int(action_row.get("unique_lda_registrants", "")) or 0) != len(expected_lda_values(mentions, "registrant_name")):
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: unique registrant count mismatch")
        expected_sets = {
            "lda_activity_issues": expected_lda_values(mentions, "activity_issue"),
            "lda_government_entities": expected_lda_values(mentions, "government_entities"),
            "lda_filing_years": expected_lda_values(mentions, "filing_year"),
            "lda_filing_periods": expected_lda_values(mentions, "filing_period"),
            "lda_matched_bill_refs": expected_lda_values(mentions, "matched_bill_refs"),
            "lda_filing_document_urls": expected_lda_values(mentions, "filing_document_url"),
        }
        for output_field, expected_values in expected_sets.items():
            if split_semicolon_values(action_row, output_field) != expected_values:
                failures.append(
                    f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: {output_field} set mismatch"
                )
        expected_source_urls = (
            expected_lda_values(mentions, "filing_document_url")
            | expected_lda_values(mentions, "source_url")
        )
        if law_row:
            expected_source_urls |= {
                url
                for url in (
                    law_row.get("source_url", "").strip(),
                    law_row.get("api_url", "").strip(),
                )
                if url
            }
        if split_semicolon_values(action_row, "source_urls") != expected_source_urls:
            failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: source URL set mismatch")
        if law_row:
            for field in (
                "public_law_number",
                "policy_area",
                "introduced_date",
                "enacted_date",
                "sponsor_bioguide_id",
                "sponsor_party",
                "sponsor_state",
                "actions_count",
                "committee_reported",
                "floor_considered",
                "enacted",
            ):
                if action_row.get(field, "") != law_row.get(field, ""):
                    failures.append(
                        f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: {field} does not match law linkage"
                    )
            evidence_layers = split_semicolon_values(action_row, "evidence_layers")
            for layer in (
                "congressgov_bill_action_metadata",
                "congressgov_public_law_outcome_metadata",
                "congressgov_sponsor_metadata",
            ):
                if layer not in evidence_layers:
                    failures.append(f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: missing {layer}")
        missing_links = split_semicolon_values(action_row, "missing_links")
        for missing_link in (
            "sponsor_or_member_target",
            "legislative_outcome_causality",
            "public_benefit_or_welfare_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(
                    f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: missing boundary link {missing_link}"
                )
        boundary = action_row.get("claim_boundary", "")
        for phrase in (
            "not show support",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_ACTION_CONTEXT}: {bill_id}: claim boundary missing {phrase!r}"
                )

    raw_mentions_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_mention_fingerprints: set[str] = set()
    for mention in lobbying_bill_mentions_raw:
        fingerprint = lda_text_review_fingerprint(mention)
        if fingerprint in raw_mentions_by_fingerprint:
            duplicate_mention_fingerprints.add(fingerprint)
        raw_mentions_by_fingerprint[fingerprint] = mention
    if duplicate_mention_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MENTIONS_RAW}: duplicate text-review fingerprints "
            f"{sorted(duplicate_mention_fingerprints)}"
        )
    text_review_by_fingerprint = {
        row.get("source_row_fingerprint", "").strip(): row
        for row in lobbying_bill_text_review
        if row.get("source_row_fingerprint", "").strip()
    }
    if len(text_review_by_fingerprint) != len(lobbying_bill_text_review):
        failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: blank or duplicate source_row_fingerprint rows are not allowed")
    if set(text_review_by_fingerprint) != set(raw_mentions_by_fingerprint):
        failures.append(
            "LDA bill-text review/raw mention mismatch: "
            f"missing from text review={sorted(set(raw_mentions_by_fingerprint) - set(text_review_by_fingerprint))[:10]}, "
            f"extra={sorted(set(text_review_by_fingerprint) - set(raw_mentions_by_fingerprint))[:10]}"
        )
    valid_text_review_statuses = {
        "exact_bill_text_with_explicit_support_signal",
        "exact_bill_text_with_explicit_opposition_signal",
        "exact_bill_text_with_mixed_support_opposition_signal",
        "exact_bill_text_with_position_or_activity_signal",
        "exact_bill_text_bill_list_or_title_only",
        "matched_reference_not_located_in_stored_activity_text",
    }
    expected_source_reviewed_rows = 0
    expected_refetch_rows = 0
    support_signal_rows = 0
    for fingerprint, text_row in sorted(text_review_by_fingerprint.items()):
        mention = raw_mentions_by_fingerprint.get(fingerprint, {})
        bill_id = text_row.get("bill_id", "").strip()
        status = text_row.get("text_review_status", "").strip()
        stored_status = text_row.get("stored_activity_text_bill_reference_status", "").strip()
        if status not in valid_text_review_statuses:
            failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: invalid status {status!r}")
        for field in (
            "bill_id",
            "filing_uuid",
            "filing_year",
            "filing_period",
            "client_name",
            "registrant_name",
            "activity_issue",
            "matched_bill_refs",
            "filing_document_url",
        ):
            if text_row.get(field, "") != mention.get(field, ""):
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: {field} does not match raw mention")
        action_row = action_context_by_bill.get(bill_id, {})
        for field in ("public_law_number", "policy_area"):
            expected = action_row.get(field, mention.get(field, ""))
            if text_row.get(field, "") != expected:
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: {field} context mismatch")
        located_reference = lda_bill_reference_located(mention)
        if located_reference:
            expected_source_reviewed_rows += 1
            if stored_status != "bill_reference_located_in_stored_activity_text":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: stored reference status mismatch")
            if text_row.get("source_reviewed_exact_bill_text", "") != "1":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: located row must be source-reviewed")
            if status == "matched_reference_not_located_in_stored_activity_text":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: located row has refetch status")
            if (parse_int(text_row.get("bill_reference_context_chars", "")) or 0) <= 0:
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: empty bill-reference context")
        else:
            expected_refetch_rows += 1
            if stored_status != "matched_reference_not_located_in_stored_activity_text":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: truncated row missing refetch status")
            if text_row.get("source_reviewed_exact_bill_text", "") != "0":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: truncated row must not be source-reviewed")
            if status != "matched_reference_not_located_in_stored_activity_text":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: truncated row has non-refetch status")
            for field in ("support_text_signal", "opposition_text_signal", "position_or_activity_text_signal"):
                if text_row.get(field, "") != "none_detected":
                    failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: truncated row should not carry {field}")
        if status == "exact_bill_text_with_explicit_support_signal":
            support_signal_rows += 1
            if text_row.get("support_text_signal", "") == "none_detected":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: support status without support signal")
        if status == "exact_bill_text_with_explicit_opposition_signal":
            if text_row.get("opposition_text_signal", "") == "none_detected":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: opposition status without opposition signal")
        if status == "exact_bill_text_with_position_or_activity_signal":
            if text_row.get("position_or_activity_text_signal", "") == "none_detected":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: position status without position signal")
            if text_row.get("support_text_signal", "") != "none_detected" or text_row.get("opposition_text_signal", "") != "none_detected":
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: position-only row carries direction signal")
        if status == "exact_bill_text_bill_list_or_title_only":
            for field in ("support_text_signal", "opposition_text_signal", "position_or_activity_text_signal"):
                if text_row.get(field, "") != "none_detected":
                    failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: list-only row carries {field}")
        evidence_layers = split_semicolon_values(text_row, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "deterministic_activity_text_position_signal",
        ):
            if layer not in evidence_layers:
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(text_row, "missing_links")
        required_text_missing_links = [
            "manual_source_review_confirmation",
            "sponsor_or_member_target",
            "legislative_outcome_causality",
            "model_validation",
        ]
        if not located_reference:
            required_text_missing_links.append("full_activity_text_refetch_for_truncated_rows")
        elif "full_activity_text_refetch_for_truncated_rows" in missing_links:
            failures.append(
                f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: located row still lists full-text refetch as missing"
            )
        for missing_link in required_text_missing_links:
            if missing_link not in missing_links:
                failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: missing link {missing_link}")
        expected_source_urls = {
            mention.get("filing_document_url", "").strip(),
            mention.get("source_url", "").strip(),
        }
        expected_source_urls.update(
            url for url in split_semicolon_values(action_row, "source_urls")
            if "congress.gov" in url
        )
        expected_source_urls = {url for url in expected_source_urls if url}
        if not expected_source_urls.issubset(split_semicolon_values(text_row, "source_urls")):
            failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: source URLs missing row/source context")
        boundary = text_row.get("claim_boundary", "")
        for phrase in (
            "Official LDA activity-text review",
            "do not show sponsor/member targeting",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_TEXT_REVIEW}: {fingerprint}: claim boundary missing {phrase!r}"
                )
    if expected_source_reviewed_rows == 0:
        failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: expected at least one located bill-reference row")
    if support_signal_rows == 0:
        failures.append(f"{LOBBYING_BILL_TEXT_REVIEW}: expected at least one explicit support text-signal row")

    disposition_review_by_fingerprint = {
        row.get("source_row_fingerprint", "").strip(): row
        for row in lobbying_bill_disposition_review
        if row.get("source_row_fingerprint", "").strip()
    }
    if not lobbying_bill_disposition_review:
        failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: no rows")
    if len(disposition_review_by_fingerprint) != len(lobbying_bill_disposition_review):
        failures.append(
            f"{LOBBYING_BILL_DISPOSITION_REVIEW}: blank or duplicate source_row_fingerprint rows are not allowed"
        )
    if set(disposition_review_by_fingerprint) != set(text_review_by_fingerprint):
        failures.append(
            "LDA bill-disposition review/text-review mismatch: "
            f"missing from disposition review={sorted(set(text_review_by_fingerprint) - set(disposition_review_by_fingerprint))[:10]}, "
            f"extra={sorted(set(disposition_review_by_fingerprint) - set(text_review_by_fingerprint))[:10]}"
        )
    status_to_preliminary_disposition = {
        "exact_bill_text_with_explicit_support_signal": "support_signal_needs_manual_confirmation",
        "exact_bill_text_with_explicit_opposition_signal": "opposition_signal_needs_manual_confirmation",
        "exact_bill_text_with_mixed_support_opposition_signal": "mixed_support_opposition_signal_needs_manual_confirmation",
        "exact_bill_text_with_position_or_activity_signal": "position_or_activity_signal_needs_manual_confirmation",
        "exact_bill_text_bill_list_or_title_only": "bill_reference_without_disposition_signal",
        "matched_reference_not_located_in_stored_activity_text": "stored_excerpt_needs_full_activity_text_refetch",
    }
    disposition_priorities = Counter()
    manual_disposition_rows = 0
    high_priority_rows = 0
    for fingerprint, disposition_row in sorted(disposition_review_by_fingerprint.items()):
        text_row = text_review_by_fingerprint.get(fingerprint, {})
        bill_id = disposition_row.get("bill_id", "").strip()
        action_row = action_context_by_bill.get(bill_id, {})
        status = text_row.get("text_review_status", "").strip()
        possible_target = (
            text_row.get("possible_member_or_committee_reference", "").strip()
            != "not_detected_in_activity_text"
        )
        if status == "exact_bill_text_with_mixed_support_opposition_signal" or possible_target:
            expected_priority = "high"
        elif status in {
            "exact_bill_text_with_explicit_support_signal",
            "exact_bill_text_with_explicit_opposition_signal",
            "exact_bill_text_with_position_or_activity_signal",
        }:
            expected_priority = "medium"
        else:
            expected_priority = "low"
        if disposition_row.get("review_priority", "") not in {"high", "medium", "low"}:
            failures.append(
                f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: invalid priority "
                f"{disposition_row.get('review_priority', '')!r}"
            )
        if disposition_row.get("review_priority", "") != expected_priority:
            failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: review priority mismatch")
        disposition_priorities[expected_priority] += 1
        expected_manual_needed = "yes" if expected_priority in {"high", "medium"} else "no"
        if disposition_row.get("manual_review_needed", "") != expected_manual_needed:
            failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: manual review flag mismatch")
        if expected_manual_needed == "yes":
            manual_disposition_rows += 1
        if expected_priority == "high":
            high_priority_rows += 1
        expected_reason_fragments: list[str] = []
        if status == "exact_bill_text_with_mixed_support_opposition_signal":
            expected_reason_fragments.append("mixed_support_opposition_signal")
        elif status == "exact_bill_text_with_explicit_support_signal":
            expected_reason_fragments.append("support_signal")
        elif status == "exact_bill_text_with_explicit_opposition_signal":
            expected_reason_fragments.append("opposition_signal")
        elif status == "exact_bill_text_with_position_or_activity_signal":
            expected_reason_fragments.append("position_or_activity_signal")
        elif status == "matched_reference_not_located_in_stored_activity_text":
            expected_reason_fragments.append("full_activity_text_refetch_needed")
        if possible_target:
            expected_reason_fragments.append("possible_member_or_committee_reference")
        if not expected_reason_fragments:
            expected_reason_fragments.append("bill_reference_only_no_disposition_or_target_signal")
        for fragment in expected_reason_fragments:
            if fragment not in disposition_row.get("manual_review_reason", ""):
                failures.append(
                    f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: manual review reason missing {fragment}"
                )
        expected_preliminary = status_to_preliminary_disposition.get(status, "")
        if disposition_row.get("preliminary_text_disposition", "") != expected_preliminary:
            failures.append(
                f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: preliminary disposition mismatch"
            )
        expected_target_status = "possible_member_or_committee_reference_needs_manual_target_review"
        scope = text_row.get("government_entity_scope", "").strip()
        if not possible_target:
            if scope in {
                "house_senate_and_agency_entities_disclosed",
                "house_and_senate_entities_disclosed",
                "single_chamber_entity_disclosed",
            }:
                expected_target_status = "chamber_entity_context_only_no_specific_target_detected"
            elif scope == "agency_entities_only_disclosed":
                expected_target_status = "agency_entity_context_only_no_specific_target_detected"
            else:
                expected_target_status = "no_government_entity_context_or_specific_target_detected"
        if disposition_row.get("target_review_status", "") != expected_target_status:
            failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: target status mismatch")
        for field in (
            "bill_id",
            "public_law_number",
            "policy_area",
            "filing_uuid",
            "filing_year",
            "filing_period",
            "client_name",
            "registrant_name",
            "activity_issue",
            "matched_bill_refs",
            "text_review_status",
            "support_text_signal",
            "opposition_text_signal",
            "position_or_activity_text_signal",
            "government_entity_scope",
            "possible_member_or_committee_reference",
            "bill_reference_context",
            "source_urls",
        ):
            if disposition_row.get(field, "") != text_row.get(field, ""):
                failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: {field} mismatch")
        for field in ("sponsor_bioguide_id", "committee_reported", "floor_considered", "enacted"):
            if disposition_row.get(field, "") != action_row.get(field, ""):
                failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: {field} action-context mismatch")
        evidence_layers = split_semicolon_values(disposition_row, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "deterministic_activity_text_position_signal",
            "disposition_target_review_queue",
            "congressgov_bill_action_metadata_context",
        ):
            if layer not in evidence_layers:
                failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(disposition_row, "missing_links")
        for missing_link in (
            "manual_disposition_confirmation",
            "sponsor_or_member_target",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: missing link {missing_link}")
        boundary = disposition_row.get("claim_boundary", "")
        for phrase in (
            "LDA disposition/target source-review queue",
            "not manual disposition confirmation",
            "sponsor/member targeting evidence",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: claim boundary missing {phrase!r}"
                )
        if "manual" not in disposition_row.get("recommended_next_review", "").casefold():
            if expected_priority in {"high", "medium"}:
                failures.append(
                    f"{LOBBYING_BILL_DISPOSITION_REVIEW}: {fingerprint}: manual review row missing manual next step"
                )
    if high_priority_rows == 0:
        failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: expected at least one high-priority row")
    if manual_disposition_rows == 0:
        failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: expected manual disposition/target review rows")
    for priority in ("high", "medium", "low"):
        if disposition_priorities[priority] == 0:
            failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: expected at least one {priority}-priority row")
    disposition_statuses = Counter(
        row.get("text_review_status", "").strip()
        for row in lobbying_bill_disposition_review
    )
    for status in (
        "exact_bill_text_with_explicit_support_signal",
        "exact_bill_text_with_explicit_opposition_signal",
        "exact_bill_text_with_position_or_activity_signal",
        "exact_bill_text_bill_list_or_title_only",
    ):
        if disposition_statuses[status] == 0:
            failures.append(f"{LOBBYING_BILL_DISPOSITION_REVIEW}: expected at least one {status} row")

    high_priority_disposition_fingerprints = {
        fingerprint
        for fingerprint, row in disposition_review_by_fingerprint.items()
        if row.get("review_priority", "").strip() == "high"
    }
    raw_manual_disposition_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_raw_manual_disposition_fingerprints: set[str] = set()
    for raw_row in lobbying_bill_manual_disposition_review_raw:
        fingerprint = raw_row.get("source_row_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: blank source_row_fingerprint row")
            continue
        if fingerprint in raw_manual_disposition_by_fingerprint:
            duplicate_raw_manual_disposition_fingerprints.add(fingerprint)
        raw_manual_disposition_by_fingerprint[fingerprint] = raw_row
    if duplicate_raw_manual_disposition_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: duplicate fingerprints "
            f"{sorted(duplicate_raw_manual_disposition_fingerprints)}"
        )

    manual_disposition_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_manual_disposition_fingerprints: set[str] = set()
    for manual_row in lobbying_bill_manual_disposition_review:
        fingerprint = manual_row.get("source_row_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: blank source_row_fingerprint row")
            continue
        if fingerprint in manual_disposition_by_fingerprint:
            duplicate_manual_disposition_fingerprints.add(fingerprint)
        manual_disposition_by_fingerprint[fingerprint] = manual_row
    if duplicate_manual_disposition_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: duplicate fingerprints "
            f"{sorted(duplicate_manual_disposition_fingerprints)}"
        )
    if set(raw_manual_disposition_by_fingerprint) != high_priority_disposition_fingerprints:
        failures.append(
            "LDA manual-disposition raw/high-priority queue mismatch: "
            f"missing from raw={sorted(high_priority_disposition_fingerprints - set(raw_manual_disposition_by_fingerprint))}, "
            f"extra={sorted(set(raw_manual_disposition_by_fingerprint) - high_priority_disposition_fingerprints)}"
        )
    if set(manual_disposition_by_fingerprint) != high_priority_disposition_fingerprints:
        failures.append(
            "LDA manual-disposition report/high-priority queue mismatch: "
            f"missing from report={sorted(high_priority_disposition_fingerprints - set(manual_disposition_by_fingerprint))}, "
            f"extra={sorted(set(manual_disposition_by_fingerprint) - high_priority_disposition_fingerprints)}"
        )
    if set(manual_disposition_by_fingerprint) != set(raw_manual_disposition_by_fingerprint):
        failures.append(
            "LDA manual-disposition report/raw mismatch: "
            f"missing from report={sorted(set(raw_manual_disposition_by_fingerprint) - set(manual_disposition_by_fingerprint))}, "
            f"extra={sorted(set(manual_disposition_by_fingerprint) - set(raw_manual_disposition_by_fingerprint))}"
        )

    valid_manual_disposition_statuses = {
        "reviewed_current_bill_support",
        "reviewed_current_bill_support_with_related_opposition",
        "reviewed_bill_reference_only",
    }
    valid_manual_target_statuses = {
        "reviewed_named_member_or_chair_text_reference",
        "reviewed_no_specific_member_or_committee_target_in_activity_text",
        "reviewed_committee_context_text_reference",
    }
    expected_manual_status_by_text_status = {
        "exact_bill_text_with_explicit_support_signal": "reviewed_current_bill_support",
        "exact_bill_text_with_mixed_support_opposition_signal": (
            "reviewed_current_bill_support_with_related_opposition"
        ),
        "exact_bill_text_bill_list_or_title_only": "reviewed_bill_reference_only",
    }
    manual_disposition_statuses = Counter()
    manual_target_statuses = Counter()
    no_outcome_manual_rows = 0
    manual_boundary_phrases = (
        "do not show lobbying contact",
        "sponsor/member targeting beyond the text reference",
        "legislative-outcome causality",
        "model validation",
    )
    for fingerprint, manual_row in sorted(manual_disposition_by_fingerprint.items()):
        raw_row = raw_manual_disposition_by_fingerprint.get(fingerprint, {})
        queue_row = disposition_review_by_fingerprint.get(fingerprint, {})
        text_status = queue_row.get("text_review_status", "").strip()
        if manual_row.get("queue_review_priority", "").strip() != "high":
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: queue priority must be high")
        if manual_row.get("queue_review_rank", "") != queue_row.get("review_rank", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: queue_review_rank mismatch")
        for field in (
            "bill_id",
            "public_law_number",
            "policy_area",
            "filing_uuid",
            "client_name",
            "registrant_name",
            "activity_issue",
            "text_review_status",
            "source_urls",
        ):
            if manual_row.get(field, "") != queue_row.get(field, ""):
                failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: {field} mismatch")
        if manual_row.get("queue_manual_review_reason", "") != queue_row.get("manual_review_reason", ""):
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: manual review reason mismatch"
            )
        if manual_row.get("queue_target_review_status", "") != queue_row.get("target_review_status", ""):
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: target queue status mismatch"
            )
        if raw_row.get("reviewed_bill_id", "") != queue_row.get("bill_id", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: {fingerprint}: reviewed bill mismatch")
        if raw_row.get("reviewed_public_law_number", "") != queue_row.get("public_law_number", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: {fingerprint}: reviewed public law mismatch")
        if raw_row.get("reviewed_source_text", "") != queue_row.get("bill_reference_context", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: {fingerprint}: source text mismatch")
        if manual_row.get("reviewed_source_text", "") != raw_row.get("reviewed_source_text", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: reviewed_source_text raw mismatch")
        if raw_row.get("reviewed_source_url", "") and raw_row.get("reviewed_source_url", "") not in manual_row.get("source_urls", ""):
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: reviewed source URL missing")
        for field in (
            "manual_review_source",
            "manual_disposition_status",
            "manual_disposition",
            "manual_disposition_basis",
            "manual_target_status",
            "manual_target_type",
            "manual_target_text",
            "manual_target_basis",
            "manual_outcome_link_status",
            "manual_reviewer_note",
            "claim_boundary",
        ):
            if manual_row.get(field, "") != raw_row.get(field, ""):
                failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: {field} raw mismatch")
        manual_status = manual_row.get("manual_disposition_status", "").strip()
        manual_target_status = manual_row.get("manual_target_status", "").strip()
        if manual_status not in valid_manual_disposition_statuses:
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                f"invalid manual disposition status {manual_status!r}"
            )
        if manual_target_status not in valid_manual_target_statuses:
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                f"invalid manual target status {manual_target_status!r}"
            )
        expected_manual_status = expected_manual_status_by_text_status.get(text_status)
        if expected_manual_status and manual_status != expected_manual_status:
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                f"manual status does not match text-review status"
            )
        possible_target = (
            queue_row.get("possible_member_or_committee_reference", "").strip()
            != "not_detected_in_activity_text"
        )
        if possible_target and manual_target_status == "reviewed_no_specific_member_or_committee_target_in_activity_text":
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                "possible target row lost target-reference review"
            )
        if not possible_target and manual_target_status != "reviewed_no_specific_member_or_committee_target_in_activity_text":
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                "non-target row gained target-reference evidence"
            )
        if manual_target_status == "reviewed_named_member_or_chair_text_reference" and not manual_row.get("manual_target_text", "").strip():
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: member/chair target text missing")
        if (
            manual_status == "reviewed_bill_reference_only"
            and manual_row.get("manual_disposition", "") != "bill_reference_without_support_or_opposition_signal"
        ):
            failures.append(
                f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                "bill-reference row claims a directional disposition"
            )
        if manual_row.get("manual_outcome_link_status", "") == "no_outcome_influence_evidence":
            no_outcome_manual_rows += 1
        else:
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: outcome status is too broad")
        evidence_layers = split_semicolon_values(manual_row, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "disposition_target_review_queue",
            "manual_high_priority_disposition_review",
        ):
            if layer not in evidence_layers:
                failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(manual_row, "missing_links")
        for missing_link in (
            "lobbying_contact_confirmation",
            "sponsor_or_member_target_beyond_activity_text_reference",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "causal_capture_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: missing link {missing_link}")
        for phrase in manual_boundary_phrases:
            if phrase not in manual_row.get("claim_boundary", ""):
                failures.append(
                    f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: {fingerprint}: "
                    f"claim boundary missing {phrase!r}"
                )
            if phrase not in raw_row.get("claim_boundary", ""):
                failures.append(
                    f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW_RAW}: {fingerprint}: "
                    f"claim boundary missing {phrase!r}"
                )
        manual_disposition_statuses[manual_status] += 1
        manual_target_statuses[manual_target_status] += 1
    if len(manual_disposition_by_fingerprint) != len(high_priority_disposition_fingerprints):
        failures.append(
            f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: expected one row per high-priority queue row"
        )
    if no_outcome_manual_rows != len(manual_disposition_by_fingerprint):
        failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: every row must preserve no-outcome boundary")
    for status in (
        "reviewed_current_bill_support",
        "reviewed_current_bill_support_with_related_opposition",
        "reviewed_bill_reference_only",
    ):
        if manual_disposition_statuses[status] == 0:
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: expected at least one {status} row")
    for status in (
        "reviewed_named_member_or_chair_text_reference",
        "reviewed_committee_context_text_reference",
        "reviewed_no_specific_member_or_committee_target_in_activity_text",
    ):
        if manual_target_statuses[status] == 0:
            failures.append(f"{LOBBYING_BILL_MANUAL_DISPOSITION_REVIEW}: expected at least one {status} row")

    medium_packet_status_by_text_status = {
        "exact_bill_text_with_explicit_support_signal": (
            "medium_support_disposition_packet_needs_confirmation"
        ),
        "exact_bill_text_with_explicit_opposition_signal": (
            "medium_opposition_disposition_packet_needs_confirmation"
        ),
        "exact_bill_text_with_position_or_activity_signal": (
            "medium_position_activity_packet_needs_direction_review"
        ),
    }
    medium_packet_signal_by_text_status = {
        "exact_bill_text_with_explicit_support_signal": (
            "support_text_signal_needs_manual_confirmation"
        ),
        "exact_bill_text_with_explicit_opposition_signal": (
            "opposition_text_signal_needs_manual_confirmation"
        ),
        "exact_bill_text_with_position_or_activity_signal": (
            "position_or_activity_text_signal_needs_direction_review"
        ),
    }

    def medium_packet_key(row: dict[str, str]) -> tuple[str, ...]:
        return (
            row.get("bill_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("policy_area", "").strip(),
            row.get("client_name", "").strip(),
            row.get("registrant_name", "").strip(),
            row.get("activity_issue", "").strip(),
            row.get("text_review_status", "").strip(),
            row.get("manual_review_reason", "").strip(),
            row.get("target_review_status", "").strip(),
        )

    def medium_packet_fingerprint(key: tuple[str, ...]) -> str:
        return hashlib.sha256("|".join(key).encode("utf-8")).hexdigest()[:16]

    medium_queue_rows = [
        row for row in lobbying_bill_disposition_review
        if row.get("review_priority", "").strip() == "medium"
    ]
    expected_medium_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in medium_queue_rows:
        key = medium_packet_key(row)
        expected_medium_groups[medium_packet_fingerprint(key)].append(row)
    medium_packets_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_medium_packet_fingerprints: set[str] = set()
    for packet in lobbying_bill_medium_disposition_packets:
        packet_fingerprint = packet.get("packet_fingerprint", "").strip()
        if not packet_fingerprint:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: blank packet_fingerprint row")
            continue
        if packet_fingerprint in medium_packets_by_fingerprint:
            duplicate_medium_packet_fingerprints.add(packet_fingerprint)
        medium_packets_by_fingerprint[packet_fingerprint] = packet
    if duplicate_medium_packet_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: duplicate packet fingerprints "
            f"{sorted(duplicate_medium_packet_fingerprints)}"
        )
    if set(medium_packets_by_fingerprint) != set(expected_medium_groups):
        failures.append(
            "LDA medium packet/disposition queue mismatch: "
            f"missing from packets={sorted(set(expected_medium_groups) - set(medium_packets_by_fingerprint))}, "
            f"extra={sorted(set(medium_packets_by_fingerprint) - set(expected_medium_groups))}"
        )
    represented_medium_fingerprints: set[str] = set()
    total_medium_rows_represented = 0
    medium_packet_statuses = Counter()
    for packet_fingerprint, packet in sorted(medium_packets_by_fingerprint.items()):
        grouped_rows = expected_medium_groups.get(packet_fingerprint, [])
        if not grouped_rows:
            continue
        first = sorted(grouped_rows, key=lambda row: parse_int(row.get("review_rank", "")) or 999999)[0]
        source_fingerprints = {
            row.get("source_row_fingerprint", "").strip()
            for row in grouped_rows
            if row.get("source_row_fingerprint", "").strip()
        }
        represented_medium_fingerprints.update(split_semicolon_values(packet, "source_row_fingerprints"))
        total_medium_rows_represented += parse_int(packet.get("rows_represented", "")) or 0
        status = first.get("text_review_status", "").strip()
        if packet.get("review_priority", "").strip() != "medium":
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: priority must be medium")
        if packet.get("packet_review_status", "") != medium_packet_status_by_text_status.get(status, ""):
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: packet status mismatch")
        if packet.get("direction_signal_summary", "") != medium_packet_signal_by_text_status.get(status, ""):
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: direction signal mismatch")
        if (parse_int(packet.get("rows_represented", "")) or 0) != len(grouped_rows):
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: row count mismatch")
        if split_semicolon_values(packet, "source_row_fingerprints") != source_fingerprints:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: source fingerprints mismatch")
        expected_review_ranks = {
            row.get("review_rank", "").strip()
            for row in grouped_rows
            if row.get("review_rank", "").strip()
        }
        if split_semicolon_values(packet, "queue_review_ranks") != expected_review_ranks:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: queue ranks mismatch")
        for field in (
            "bill_id",
            "public_law_number",
            "policy_area",
            "client_name",
            "registrant_name",
            "activity_issue",
            "text_review_status",
            "manual_review_reason",
            "target_review_status",
        ):
            if packet.get(field, "") != first.get(field, ""):
                failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: {field} mismatch")
        expected_sets = {
            "filing_uuids": {
                row.get("filing_uuid", "").strip()
                for row in grouped_rows
                if row.get("filing_uuid", "").strip()
            },
            "filing_years": {
                row.get("filing_year", "").strip()
                for row in grouped_rows
                if row.get("filing_year", "").strip()
            },
            "filing_periods": {
                row.get("filing_period", "").strip()
                for row in grouped_rows
                if row.get("filing_period", "").strip()
            },
            "support_text_signals": {
                value
                for row in grouped_rows
                for value in split_semicolon_values(row, "support_text_signal")
            },
            "opposition_text_signals": {
                value
                for row in grouped_rows
                for value in split_semicolon_values(row, "opposition_text_signal")
            },
            "position_or_activity_text_signals": {
                value
                for row in grouped_rows
                for value in split_semicolon_values(row, "position_or_activity_text_signal")
            },
        }
        for field, expected_values in expected_sets.items():
            if split_semicolon_values(packet, field) != expected_values:
                failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: {field} mismatch")
        expected_source_urls = {
            url
            for row in grouped_rows
            for url in split_semicolon_values(row, "source_urls")
        }
        if split_semicolon_values(packet, "source_urls") != expected_source_urls:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: source URLs mismatch")
        distinct_contexts = {
            row.get("bill_reference_context", "").strip()
            for row in grouped_rows
            if row.get("bill_reference_context", "").strip()
        }
        if (parse_int(packet.get("distinct_context_count", "")) or 0) != len(distinct_contexts):
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: context count mismatch")
        if distinct_contexts and not packet.get("bill_reference_context_samples", "").strip():
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: missing context sample")
        if (
            "confirm" not in packet.get("disposition_next_step", "").casefold()
            and status != "exact_bill_text_with_position_or_activity_signal"
        ):
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: missing confirmation next step")
        evidence_layers = split_semicolon_values(packet, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "deterministic_activity_text_position_signal",
            "disposition_target_review_queue",
            "medium_disposition_review_packet",
        ):
            if layer not in evidence_layers:
                failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(packet, "missing_links")
        for missing_link in (
            "manual_disposition_confirmation",
            "lobbying_contact_confirmation",
            "sponsor_or_member_target",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "causal_capture_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: missing link {missing_link}")
        boundary = packet.get("claim_boundary", "")
        for phrase in (
            "Medium-priority LDA disposition source-review packets",
            "not manual disposition confirmation",
            "lobbying-contact evidence",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: {packet_fingerprint}: "
                    f"claim boundary missing {phrase!r}"
                )
        medium_packet_statuses[packet.get("packet_review_status", "")] += 1
    expected_medium_fingerprints = {
        row.get("source_row_fingerprint", "").strip()
        for row in medium_queue_rows
        if row.get("source_row_fingerprint", "").strip()
    }
    if represented_medium_fingerprints != expected_medium_fingerprints:
        failures.append(
            "LDA medium packet represented-row mismatch: "
            f"missing={sorted(expected_medium_fingerprints - represented_medium_fingerprints)[:10]}, "
            f"extra={sorted(represented_medium_fingerprints - expected_medium_fingerprints)[:10]}"
        )
    if total_medium_rows_represented != len(medium_queue_rows):
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: represented row total "
            f"{total_medium_rows_represented} does not match medium queue {len(medium_queue_rows)}"
        )
    if expected_medium_fingerprints & set(manual_disposition_by_fingerprint):
        failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: overlaps high-priority manual review rows")
    for packet_status in (
        "medium_support_disposition_packet_needs_confirmation",
        "medium_opposition_disposition_packet_needs_confirmation",
        "medium_position_activity_packet_needs_direction_review",
    ):
        if medium_packet_statuses[packet_status] == 0:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DISPOSITION_PACKETS}: expected at least one {packet_status}")

    directional_medium_packet_statuses = {
        "medium_support_disposition_packet_needs_confirmation",
        "medium_opposition_disposition_packet_needs_confirmation",
    }
    valid_medium_directional_review_statuses = {
        "reviewed_current_bill_support",
        "reviewed_current_bill_support_with_opposition_signal_correction",
        "reviewed_current_bill_opposition",
        "reviewed_direction_signal_on_other_measure",
        "reviewed_current_bill_monitoring_only_with_related_opposition",
    }
    medium_directional_support_statuses = {
        "reviewed_current_bill_support",
        "reviewed_current_bill_support_with_opposition_signal_correction",
    }
    medium_directional_opposition_statuses = {
        "reviewed_current_bill_opposition",
    }
    medium_directional_downgraded_statuses = {
        "reviewed_direction_signal_on_other_measure",
        "reviewed_current_bill_monitoring_only_with_related_opposition",
    }
    valid_medium_directional_target_statuses = {
        "reviewed_named_member_or_chair_text_reference",
        "reviewed_no_specific_member_or_committee_target_in_activity_text",
    }
    expected_medium_directional_fingerprints = {
        fingerprint
        for fingerprint, packet in medium_packets_by_fingerprint.items()
        if packet.get("packet_review_status", "").strip() in directional_medium_packet_statuses
    }
    raw_medium_directional_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_raw_medium_directional_fingerprints: set[str] = set()
    for raw_row in lobbying_bill_medium_directional_packet_review_raw:
        fingerprint = raw_row.get("packet_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: blank packet_fingerprint row")
            continue
        if fingerprint in raw_medium_directional_by_fingerprint:
            duplicate_raw_medium_directional_fingerprints.add(fingerprint)
        raw_medium_directional_by_fingerprint[fingerprint] = raw_row
    if duplicate_raw_medium_directional_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: duplicate packet fingerprints "
            f"{sorted(duplicate_raw_medium_directional_fingerprints)}"
        )

    medium_directional_review_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_medium_directional_review_fingerprints: set[str] = set()
    for review_row in lobbying_bill_medium_directional_packet_review:
        fingerprint = review_row.get("packet_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: blank packet_fingerprint row")
            continue
        if fingerprint in medium_directional_review_by_fingerprint:
            duplicate_medium_directional_review_fingerprints.add(fingerprint)
        medium_directional_review_by_fingerprint[fingerprint] = review_row
    if duplicate_medium_directional_review_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: duplicate packet fingerprints "
            f"{sorted(duplicate_medium_directional_review_fingerprints)}"
        )
    if set(raw_medium_directional_by_fingerprint) != expected_medium_directional_fingerprints:
        failures.append(
            "LDA medium-directional raw/packet mismatch: "
            f"missing from raw={sorted(expected_medium_directional_fingerprints - set(raw_medium_directional_by_fingerprint))}, "
            f"extra={sorted(set(raw_medium_directional_by_fingerprint) - expected_medium_directional_fingerprints)}"
        )
    if set(medium_directional_review_by_fingerprint) != expected_medium_directional_fingerprints:
        failures.append(
            "LDA medium-directional report/packet mismatch: "
            f"missing from report={sorted(expected_medium_directional_fingerprints - set(medium_directional_review_by_fingerprint))}, "
            f"extra={sorted(set(medium_directional_review_by_fingerprint) - expected_medium_directional_fingerprints)}"
        )
    if set(medium_directional_review_by_fingerprint) != set(raw_medium_directional_by_fingerprint):
        failures.append(
            "LDA medium-directional report/raw mismatch: "
            f"missing from report={sorted(set(raw_medium_directional_by_fingerprint) - set(medium_directional_review_by_fingerprint))}, "
            f"extra={sorted(set(medium_directional_review_by_fingerprint) - set(raw_medium_directional_by_fingerprint))}"
        )

    medium_directional_statuses = Counter()
    medium_directional_target_statuses = Counter()
    medium_directional_source_fingerprints: set[str] = set()
    medium_directional_total_rows = 0
    medium_directional_support_rows = 0
    medium_directional_opposition_rows = 0
    medium_directional_no_outcome_rows = 0
    for fingerprint, review_row in sorted(medium_directional_review_by_fingerprint.items()):
        raw_row = raw_medium_directional_by_fingerprint.get(fingerprint, {})
        packet = medium_packets_by_fingerprint.get(fingerprint, {})
        status = review_row.get("manual_packet_disposition_status", "").strip()
        target_status = review_row.get("manual_target_status", "").strip()
        rows_represented = parse_int(review_row.get("rows_represented", "")) or 0
        medium_directional_statuses[status] += 1
        medium_directional_target_statuses[target_status] += 1
        medium_directional_total_rows += rows_represented
        medium_directional_source_fingerprints.update(
            split_semicolon_values(review_row, "source_row_fingerprints")
        )
        if status in medium_directional_support_statuses:
            medium_directional_support_rows += rows_represented
        if status in medium_directional_opposition_statuses:
            medium_directional_opposition_rows += rows_represented
        if review_row.get("manual_outcome_link_status", "").strip() == "no_outcome_influence_evidence":
            medium_directional_no_outcome_rows += 1
        if status not in valid_medium_directional_review_statuses:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                f"invalid manual packet disposition status {status!r}"
            )
        if target_status not in valid_medium_directional_target_statuses:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                f"invalid manual target status {target_status!r}"
            )
        if review_row.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                "manual outcome status is too broad"
            )
        if raw_row.get("reviewed_packet_rank", "") != packet.get("packet_rank", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed packet rank mismatch"
            )
        if raw_row.get("reviewed_bill_id", "") != packet.get("bill_id", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed bill mismatch"
            )
        if raw_row.get("reviewed_public_law_number", "") != packet.get("public_law_number", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed public law mismatch"
            )
        for field in (
            "manual_review_source",
            "manual_packet_disposition_status",
            "manual_packet_disposition",
            "manual_packet_disposition_basis",
            "manual_target_status",
            "manual_target_type",
            "manual_target_text",
            "manual_target_basis",
            "manual_outcome_link_status",
            "manual_reviewer_note",
            "claim_boundary",
        ):
            if review_row.get(field, "") != raw_row.get(field, ""):
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                    f"{field} raw mismatch"
                )
        for field in (
            "packet_rank",
            "bill_id",
            "public_law_number",
            "policy_area",
            "client_name",
            "registrant_name",
            "activity_issue",
            "packet_review_status",
            "direction_signal_summary",
            "rows_represented",
            "source_row_fingerprints",
            "queue_review_ranks",
            "support_text_signals",
            "opposition_text_signals",
            "bill_reference_context_samples",
            "source_urls",
        ):
            if review_row.get(field, "") != packet.get(field, ""):
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                    f"{field} packet mismatch"
                )
        evidence_layers = split_semicolon_values(review_row, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "deterministic_activity_text_position_signal",
            "disposition_target_review_queue",
            "medium_disposition_review_packet",
            "manual_medium_directional_packet_review",
        ):
            if layer not in evidence_layers:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                    f"missing evidence layer {layer}"
                )
        missing_links = split_semicolon_values(review_row, "missing_links")
        for missing_link in (
            "lobbying_contact_confirmation",
            "sponsor_or_member_target_beyond_activity_text_reference",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                    f"missing link {missing_link}"
                )
        boundary = review_row.get("claim_boundary", "")
        for phrase in (
            "Manual medium-priority LDA directional packet source review only",
            "do not show lobbying contact",
            "sponsor/member targeting beyond text references",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: {fingerprint}: "
                    f"claim boundary missing {phrase!r}"
                )
    if len(medium_directional_review_by_fingerprint) != 28:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 28 reviewed packets"
        )
    if medium_directional_total_rows != 48:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 48 represented rows"
        )
    if sum(medium_directional_statuses[status] for status in medium_directional_support_statuses) != 20:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 20 support packets"
        )
    if medium_directional_support_rows != 32:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 32 support rows"
        )
    if sum(medium_directional_statuses[status] for status in medium_directional_opposition_statuses) != 1:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 1 opposition packet"
        )
    if medium_directional_opposition_rows != 1:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 1 opposition row"
        )
    if sum(medium_directional_statuses[status] for status in medium_directional_downgraded_statuses) != 7:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected 7 downgraded packets"
        )
    if medium_directional_statuses["reviewed_current_bill_support_with_opposition_signal_correction"] != 1:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected one corrected opposition packet"
        )
    if medium_directional_target_statuses["reviewed_named_member_or_chair_text_reference"] != 1:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected one named-member text reference"
        )
    if medium_directional_no_outcome_rows != len(medium_directional_review_by_fingerprint):
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: expected every packet to have no outcome influence evidence"
        )
    if medium_directional_source_fingerprints & set(manual_disposition_by_fingerprint):
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_DIRECTIONAL_PACKET_REVIEW}: overlaps high-priority manual review rows"
        )

    position_activity_medium_packet_statuses = {
        "medium_position_activity_packet_needs_direction_review",
    }
    valid_medium_position_activity_review_statuses = {
        "reviewed_current_bill_issue_or_provision_activity_without_direction",
        "reviewed_current_bill_monitoring_or_analysis_only",
        "reviewed_current_bill_all_provisions_without_direction",
        "reviewed_current_bill_position_represented_without_direction",
        "reviewed_current_bill_lobbied_on_without_direction",
        "reviewed_current_bill_opposition_from_activity_text",
    }
    medium_position_activity_issue_statuses = {
        "reviewed_current_bill_issue_or_provision_activity_without_direction",
    }
    medium_position_activity_monitoring_statuses = {
        "reviewed_current_bill_monitoring_or_analysis_only",
    }
    medium_position_activity_all_provisions_statuses = {
        "reviewed_current_bill_all_provisions_without_direction",
    }
    medium_position_activity_position_statuses = {
        "reviewed_current_bill_position_represented_without_direction",
    }
    medium_position_activity_lobbied_on_statuses = {
        "reviewed_current_bill_lobbied_on_without_direction",
    }
    medium_position_activity_opposition_statuses = {
        "reviewed_current_bill_opposition_from_activity_text",
    }
    valid_medium_position_activity_target_statuses = {
        "reviewed_no_specific_member_or_committee_target_in_activity_text",
        "reviewed_generic_congress_text_reference",
    }
    expected_medium_position_activity_fingerprints = {
        fingerprint
        for fingerprint, packet in medium_packets_by_fingerprint.items()
        if packet.get("packet_review_status", "").strip() in position_activity_medium_packet_statuses
    }
    raw_medium_position_activity_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_raw_medium_position_activity_fingerprints: set[str] = set()
    for raw_row in lobbying_bill_medium_position_activity_packet_review_raw:
        fingerprint = raw_row.get("packet_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: blank packet_fingerprint row")
            continue
        if fingerprint in raw_medium_position_activity_by_fingerprint:
            duplicate_raw_medium_position_activity_fingerprints.add(fingerprint)
        raw_medium_position_activity_by_fingerprint[fingerprint] = raw_row
    if duplicate_raw_medium_position_activity_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: duplicate packet fingerprints "
            f"{sorted(duplicate_raw_medium_position_activity_fingerprints)}"
        )

    medium_position_activity_review_by_fingerprint: dict[str, dict[str, str]] = {}
    duplicate_medium_position_activity_review_fingerprints: set[str] = set()
    for review_row in lobbying_bill_medium_position_activity_packet_review:
        fingerprint = review_row.get("packet_fingerprint", "").strip()
        if not fingerprint:
            failures.append(f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: blank packet_fingerprint row")
            continue
        if fingerprint in medium_position_activity_review_by_fingerprint:
            duplicate_medium_position_activity_review_fingerprints.add(fingerprint)
        medium_position_activity_review_by_fingerprint[fingerprint] = review_row
    if duplicate_medium_position_activity_review_fingerprints:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: duplicate packet fingerprints "
            f"{sorted(duplicate_medium_position_activity_review_fingerprints)}"
        )
    if set(raw_medium_position_activity_by_fingerprint) != expected_medium_position_activity_fingerprints:
        failures.append(
            "LDA medium-position/activity raw/packet mismatch: "
            f"missing from raw={sorted(expected_medium_position_activity_fingerprints - set(raw_medium_position_activity_by_fingerprint))}, "
            f"extra={sorted(set(raw_medium_position_activity_by_fingerprint) - expected_medium_position_activity_fingerprints)}"
        )
    if set(medium_position_activity_review_by_fingerprint) != expected_medium_position_activity_fingerprints:
        failures.append(
            "LDA medium-position/activity report/packet mismatch: "
            f"missing from report={sorted(expected_medium_position_activity_fingerprints - set(medium_position_activity_review_by_fingerprint))}, "
            f"extra={sorted(set(medium_position_activity_review_by_fingerprint) - expected_medium_position_activity_fingerprints)}"
        )
    if set(medium_position_activity_review_by_fingerprint) != set(raw_medium_position_activity_by_fingerprint):
        failures.append(
            "LDA medium-position/activity report/raw mismatch: "
            f"missing from report={sorted(set(raw_medium_position_activity_by_fingerprint) - set(medium_position_activity_review_by_fingerprint))}, "
            f"extra={sorted(set(medium_position_activity_review_by_fingerprint) - set(raw_medium_position_activity_by_fingerprint))}"
        )

    medium_position_activity_statuses = Counter()
    medium_position_activity_rows_by_status = Counter()
    medium_position_activity_target_statuses = Counter()
    medium_position_activity_source_fingerprints: set[str] = set()
    medium_position_activity_total_rows = 0
    medium_position_activity_no_outcome_rows = 0
    for fingerprint, review_row in sorted(medium_position_activity_review_by_fingerprint.items()):
        raw_row = raw_medium_position_activity_by_fingerprint.get(fingerprint, {})
        packet = medium_packets_by_fingerprint.get(fingerprint, {})
        status = review_row.get("manual_activity_disposition_status", "").strip()
        target_status = review_row.get("manual_target_status", "").strip()
        rows_represented = parse_int(review_row.get("rows_represented", "")) or 0
        medium_position_activity_statuses[status] += 1
        medium_position_activity_rows_by_status[status] += rows_represented
        medium_position_activity_target_statuses[target_status] += 1
        medium_position_activity_total_rows += rows_represented
        medium_position_activity_source_fingerprints.update(
            split_semicolon_values(review_row, "source_row_fingerprints")
        )
        if review_row.get("manual_outcome_link_status", "").strip() == "no_outcome_influence_evidence":
            medium_position_activity_no_outcome_rows += 1
        if status not in valid_medium_position_activity_review_statuses:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                f"invalid manual activity disposition status {status!r}"
            )
        if target_status not in valid_medium_position_activity_target_statuses:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                f"invalid manual target status {target_status!r}"
            )
        if review_row.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                "manual outcome status is too broad"
            )
        if raw_row.get("reviewed_packet_rank", "") != packet.get("packet_rank", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed packet rank mismatch"
            )
        if raw_row.get("reviewed_bill_id", "") != packet.get("bill_id", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed bill mismatch"
            )
        if raw_row.get("reviewed_public_law_number", "") != packet.get("public_law_number", ""):
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW_RAW}: {fingerprint}: "
                "reviewed public law mismatch"
            )
        for field in (
            "manual_review_source",
            "manual_activity_disposition_status",
            "manual_activity_disposition",
            "manual_activity_disposition_basis",
            "manual_target_status",
            "manual_target_type",
            "manual_target_text",
            "manual_target_basis",
            "manual_outcome_link_status",
            "manual_reviewer_note",
        ):
            if review_row.get(field, "") != raw_row.get(field, ""):
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    f"{field} raw mismatch"
                )
        for field in (
            "packet_rank",
            "bill_id",
            "public_law_number",
            "policy_area",
            "client_name",
            "registrant_name",
            "activity_issue",
            "packet_review_status",
            "direction_signal_summary",
            "rows_represented",
            "source_row_fingerprints",
            "queue_review_ranks",
            "position_or_activity_text_signals",
            "support_text_signals",
            "opposition_text_signals",
            "bill_reference_context_samples",
            "source_urls",
        ):
            if review_row.get(field, "") != packet.get(field, ""):
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    f"{field} packet mismatch"
                )
        if target_status == "reviewed_generic_congress_text_reference":
            if review_row.get("manual_target_text", "").strip().casefold() != "congress":
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    "generic Congress target text missing"
                )
        evidence_layers = split_semicolon_values(review_row, "evidence_layers")
        for layer in (
            "official_lda_filing_text_bill_identifier",
            "official_lda_activity_text_source_review",
            "deterministic_activity_text_position_signal",
            "disposition_target_review_queue",
            "medium_disposition_review_packet",
            "manual_medium_position_activity_packet_review",
        ):
            if layer not in evidence_layers:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    f"missing evidence layer {layer}"
                )
        missing_links = split_semicolon_values(review_row, "missing_links")
        for missing_link in (
            "lobbying_contact_confirmation",
            "sponsor_or_member_target_beyond_activity_text_reference",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if missing_link not in missing_links:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    f"missing link {missing_link}"
                )
        boundary = review_row.get("claim_boundary", "")
        for phrase in (
            "Manual medium-priority LDA position/activity packet source review only",
            "do not show lobbying contact",
            "sponsor/member targeting beyond text references",
            "legislative-outcome causality",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: {fingerprint}: "
                    f"claim boundary missing {phrase!r}"
                )
    if len(medium_position_activity_review_by_fingerprint) != 74:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: expected 74 reviewed packets"
        )
    if medium_position_activity_total_rows != 104:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: expected 104 represented rows"
        )
    if len(medium_position_activity_source_fingerprints) != 104:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: expected 104 source row fingerprints"
        )

    def assert_position_activity_status_count(
        statuses: set[str],
        expected_packets: int,
        expected_rows: int,
        label: str,
    ) -> None:
        packet_total = sum(medium_position_activity_statuses[status] for status in statuses)
        row_total = sum(medium_position_activity_rows_by_status[status] for status in statuses)
        if packet_total != expected_packets:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: "
                f"expected {expected_packets} {label} packets"
            )
        if row_total != expected_rows:
            failures.append(
                f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: "
                f"expected {expected_rows} {label} rows"
            )

    assert_position_activity_status_count(
        medium_position_activity_issue_statuses,
        59,
        73,
        "issue/provision activity",
    )
    assert_position_activity_status_count(
        medium_position_activity_monitoring_statuses,
        5,
        5,
        "monitoring/analysis",
    )
    assert_position_activity_status_count(
        medium_position_activity_all_provisions_statuses,
        7,
        18,
        "all-provisions",
    )
    assert_position_activity_status_count(
        medium_position_activity_position_statuses,
        2,
        6,
        "position-represented",
    )
    assert_position_activity_status_count(
        medium_position_activity_lobbied_on_statuses,
        0,
        0,
        "lobbied-on-only",
    )
    assert_position_activity_status_count(
        medium_position_activity_opposition_statuses,
        1,
        2,
        "upgraded opposition",
    )
    if medium_position_activity_target_statuses["reviewed_generic_congress_text_reference"] != 2:
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: expected two generic Congress text references"
        )
    if medium_position_activity_no_outcome_rows != len(medium_position_activity_review_by_fingerprint):
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: expected every packet to have no outcome influence evidence"
        )
    if medium_position_activity_source_fingerprints & set(manual_disposition_by_fingerprint):
        failures.append(
            f"{LOBBYING_BILL_MEDIUM_POSITION_ACTIVITY_PACKET_REVIEW}: overlaps high-priority manual review rows"
        )

    required_court_law_columns = {
        "case_id",
        "case_name",
        "term",
        "issue",
        "invalidated",
        "law_minor",
        "court_usc_sections",
        "linkage_status",
        "candidate_usc_section_count",
        "matched_usc_section_count",
        "matched_authority_overlap_count",
        "matched_public_law_count",
        "public_law_numbers",
        "bill_ids",
        "matched_usc_sections",
        "authority_document_numbers",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_court_law_columns = required_court_law_columns - set(court_law_linkage[0])
    if missing_court_law_columns:
        failures.append(
            f"{COURT_LAW_LINKAGE}: missing columns {sorted(missing_court_law_columns)}"
        )
    if not COURT_LAW_LINKAGE_MD.exists():
        failures.append(f"{COURT_LAW_LINKAGE_MD}: missing markdown report")
    court_case_ids = {row.get("case_id", "").strip() for row in court_review_rows if row.get("case_id", "").strip()}
    court_raw_case_ids = {row.get("case_id", "").strip() for row in court_law_linkage_raw if row.get("case_id", "").strip()}
    court_report_case_ids = {row.get("case_id", "").strip() for row in court_law_linkage if row.get("case_id", "").strip()}
    if court_report_case_ids != court_raw_case_ids:
        failures.append(
            "court-law linkage report/raw mismatch: "
            f"missing from report={sorted(court_raw_case_ids - court_report_case_ids)[:10]}, "
            f"extra={sorted(court_report_case_ids - court_raw_case_ids)[:10]}"
        )
    if court_raw_case_ids != court_case_ids:
        failures.append(
            "court-law linkage/court-review case mismatch: "
            f"missing from linkage={sorted(court_case_ids - court_raw_case_ids)[:10]}, "
            f"extra={sorted(court_raw_case_ids - court_case_ids)[:10]}"
        )
    court_matched_rows = [
        row for row in court_law_linkage
        if row.get("linkage_status") == "usc_section_authority_overlap"
    ]
    if not court_matched_rows:
        failures.append(f"{COURT_LAW_LINKAGE}: expected at least one U.S.C.-section authority overlap")
    court_linkage_row = linkage_by_family.get("Court review and invalidation", {})
    if court_linkage_row:
        try:
            linked_rows = int(court_linkage_row.get("linkedRows", "0") or "0")
        except ValueError:
            failures.append(f"{LINKAGE}: Court review and invalidation: linkedRows is not an integer")
        else:
            if linked_rows != len(court_matched_rows):
                failures.append(
                    f"{LINKAGE}: Court review linkedRows {linked_rows} "
                    f"does not match {COURT_LAW_LINKAGE} overlaps {len(court_matched_rows)}"
                )
            if court_matched_rows and court_linkage_row.get("linkageStatus") == "not linked":
                failures.append(f"{LINKAGE}: Court review should not remain not linked when overlaps are present")
    for row in court_law_linkage:
        case_id = row.get("case_id", "").strip()
        boundary = row.get("claim_boundary", "")
        if (
            "not proof" not in boundary
            or "emergency-order" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{COURT_LAW_LINKAGE}: {case_id}: "
                "claim_boundary must reject direct-review, emergency-order, and model-validation claims"
            )
        try:
            candidate_sections = int(row.get("candidate_usc_section_count", "0") or "0")
            matched_sections = int(row.get("matched_usc_section_count", "0") or "0")
            overlap_count = int(row.get("matched_authority_overlap_count", "0") or "0")
            public_law_count = int(row.get("matched_public_law_count", "0") or "0")
        except ValueError:
            failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: linkage counts must be integers")
            continue
        if matched_sections > candidate_sections:
            failures.append(
                f"{COURT_LAW_LINKAGE}: {case_id}: matched sections exceed candidate sections"
            )
        if row.get("linkage_status") == "usc_section_authority_overlap":
            if candidate_sections <= 0 or matched_sections <= 0 or overlap_count <= 0 or public_law_count <= 0:
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: overlap row has nonpositive counts")
            if not row.get("public_law_numbers", "").strip() or not row.get("matched_usc_sections", "").strip():
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: overlap row missing public laws or U.S.C. sections")
            if "federal_register_authority_usc_overlap" not in row.get("evidence_layers", ""):
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: overlap row missing evidence layer")
            if "public_law_or_rule_authority_overlap" in row.get("missing_links", ""):
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: overlap row still lists authority overlap as missing")
        else:
            if row.get("public_law_numbers", "").strip() or row.get("bill_ids", "").strip():
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: non-overlap row should not carry public laws or bills")
            if row.get("linkage_status") == "no_usc_section" and candidate_sections != 0:
                failures.append(f"{COURT_LAW_LINKAGE}: {case_id}: no_usc_section row has candidate sections")

    if spine_bill_ids != law_bill_ids:
        failures.append(
            "bill-law spine/law-revision linkage bill mismatch: "
            f"missing from spine={sorted(law_bill_ids - spine_bill_ids)}, "
            f"extra={sorted(spine_bill_ids - law_bill_ids)}"
        )
    required_spine_columns = {
        "bill_id",
        "public_law_number",
        "implementation_authority_rule_rows",
        "implementation_authority_text_verified_rows",
        "implementation_authority_document_numbers",
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
        "claim_boundary",
    }
    missing_spine_columns = required_spine_columns - set(bill_law_spine[0])
    if missing_spine_columns:
        failures.append(f"{BILL_LAW_SPINE}: missing columns {sorted(missing_spine_columns)}")
    district_context_rows = sum(
        int(row.get("district_public_opinion_context_rows", "0") or "0")
        for row in bill_law_spine
    )
    if district_context_rows != len(district_linkage_rows):
        failures.append(
            f"{BILL_LAW_SPINE}: district context rows {district_context_rows} "
            f"do not match {DISTRICT_PUBLIC_OPINION_LINKAGE} rows {len(district_linkage_rows)}"
        )
    try:
        district_policy_context_rows = sum(
            int(row.get("district_public_opinion_policy_context_rows", "0") or "0")
            for row in bill_law_spine
        )
    except ValueError:
        failures.append(f"{BILL_LAW_SPINE}: district policy-context row counts must be integers")
    else:
        if district_policy_context_rows != len(district_public_opinion_policy_context):
            failures.append(
                f"{BILL_LAW_SPINE}: district policy-context rows {district_policy_context_rows} "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT} rows "
                f"{len(district_public_opinion_policy_context)}"
            )
    if not BILL_LAW_SPINE_MD.exists():
        failures.append(f"{BILL_LAW_SPINE_MD}: missing markdown report")
    else:
        spine_md = BILL_LAW_SPINE_MD.read_text()
        if "bounded sponsor-district bill policy-area context" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize bounded sponsor-district bill policy-area context"
            )
        if "same-policy campaign-finance sponsor context" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize same-policy campaign-finance sponsor context"
            )
        if "same-policy LDA issue/bill context" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize same-policy LDA issue/bill context"
            )
        if "Regulations.gov comment portals" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize proposed-rule Regulations.gov comment portals"
            )
        if "authority-chain comment metadata" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize authority-chain comment metadata"
            )
        if "comment-record metadata" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize Regulations.gov comment-record metadata"
            )
        if "official OLRC post-only public-law marker evidence" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize official OLRC public-law marker evidence"
            )
        if "Review-ready target-section packet rows" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize statutory-lineage target review packets"
            )
        if "target-section diff review rows" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize statutory-lineage target-section diff review"
            )
        if "final effective dates" not in spine_md or "Final-to-effective delay" not in spine_md:
            failures.append(
                f"{BILL_LAW_SPINE_MD}: must summarize final-rule effective-date timing metadata"
            )
    if any("model validation" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must explicitly reject model validation")
    if any("timing metadata" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must explicitly describe timing evidence as metadata")
    if any("implementation outcome" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must explicitly reject implementation-outcome evidence")
    if any("shared-policy-area metadata" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must identify finance/lobbying context as shared-policy-area metadata")
    if any("bill-specific finance or lobbying influence" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must reject bill-specific finance or lobbying influence")
    if any("public-law causal attribution" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must reject public-law causal attribution claims")
    if any("comment text" not in row.get("claim_boundary", "") for row in bill_law_spine):
        failures.append(f"{BILL_LAW_SPINE}: claim_boundary must reject comment-text claims")

    required_lifecycle_columns = {
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
        "review_packet",
        "claim_boundary",
    }
    missing_lifecycle_columns = required_lifecycle_columns - set(bill_law_lifecycle_readiness[0])
    if missing_lifecycle_columns:
        failures.append(
            f"{BILL_LAW_LIFECYCLE_READINESS}: missing columns {sorted(missing_lifecycle_columns)}"
        )
    if not BILL_LAW_LIFECYCLE_READINESS_MD.exists():
        failures.append(f"{BILL_LAW_LIFECYCLE_READINESS_MD}: missing markdown report")
    else:
        lifecycle_md = BILL_LAW_LIFECYCLE_READINESS_MD.read_text()
        if "work queue" not in lifecycle_md or "Claim boundary" not in lifecycle_md:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS_MD}: must describe the report as a bounded work queue"
            )
        if "Next upgrade gate counts" not in lifecycle_md:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS_MD}: must summarize next upgrade gate counts"
            )
        if "Next source family counts" not in lifecycle_md:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS_MD}: must summarize next source family counts"
            )
    try:
        lifecycle_by_bill = by_field(bill_law_lifecycle_readiness, "bill_id")
    except ValueError as exception:
        failures.append(str(exception))
        lifecycle_by_bill = {}
    spine_by_bill = {row.get("bill_id", ""): row for row in bill_law_spine if row.get("bill_id", "")}
    lifecycle_bill_ids = set(lifecycle_by_bill)
    if lifecycle_bill_ids != set(spine_by_bill):
        failures.append(
            "bill-law lifecycle readiness/spine bill mismatch: "
            f"missing from readiness={sorted(set(spine_by_bill) - lifecycle_bill_ids)}, "
            f"extra={sorted(lifecycle_bill_ids - set(spine_by_bill))}"
        )
    ranks: list[int] = []
    for row in bill_law_lifecycle_readiness:
        rank = parse_int(row.get("review_priority_rank", ""))
        score = parse_int(row.get("review_score", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {row.get('bill_id', '')}: invalid review_priority_rank"
            )
        else:
            ranks.append(rank)
        if score is None:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {row.get('bill_id', '')}: invalid review_score"
            )
    if sorted(ranks) != list(range(1, len(bill_law_lifecycle_readiness) + 1)):
        failures.append(f"{BILL_LAW_LIFECYCLE_READINESS}: review ranks must be contiguous")
    for bill_id, lifecycle_row in lifecycle_by_bill.items():
        spine_row = spine_by_bill.get(bill_id)
        if not spine_row:
            continue
        layers = split_semicolon_values(spine_row, "evidence_layers")
        missing = split_semicolon_values(spine_row, "missing_links")
        expected_direct = {layer for layer in LIFECYCLE_DIRECT_LAYERS if layer in layers}
        expected_context = {layer for layer in LIFECYCLE_CONTEXT_LAYERS if layer in layers}
        expected_gaps = {gate for gate in LIFECYCLE_HIGH_PRIORITY_GATES if gate in missing}
        actual_direct = split_semicolon_values(lifecycle_row, "direct_evidence_layers")
        actual_context = split_semicolon_values(lifecycle_row, "context_evidence_layers")
        actual_gaps = split_semicolon_values(lifecycle_row, "high_priority_gaps")
        if actual_direct != expected_direct:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: direct layer set does not match spine"
            )
        if actual_context != expected_context:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: context layer set does not match spine"
            )
        if actual_gaps != expected_gaps:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: high-priority gap set does not match spine"
            )
        direct_count = parse_int(lifecycle_row.get("direct_evidence_count", ""))
        context_count = parse_int(lifecycle_row.get("context_evidence_count", ""))
        gap_count = parse_int(lifecycle_row.get("high_priority_gap_count", ""))
        if direct_count != len(expected_direct):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: direct_evidence_count mismatch"
            )
        if context_count != len(expected_context):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: context_evidence_count mismatch"
            )
        if gap_count != len(expected_gaps):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: high_priority_gap_count mismatch"
            )
        if lifecycle_row.get("lifecycle_readiness_tier", "") not in LIFECYCLE_TIERS:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: invalid lifecycle_readiness_tier"
            )
        gate = lifecycle_row.get("next_upgrade_gate", "")
        if gate != "none" and gate not in missing:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: next_upgrade_gate {gate!r} "
                "is not a current spine missing link"
            )
        if not lifecycle_row.get("next_source_family", "").strip():
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: missing next_source_family"
            )
        if not lifecycle_row.get("next_source_command", "").strip():
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: missing next_source_command"
            )
        for output_field, spine_field in LIFECYCLE_POINTER_FIELDS.items():
            expected_pointer = split_semicolon_values(spine_row, spine_field)
            actual_pointer = split_semicolon_values(lifecycle_row, output_field)
            if actual_pointer != expected_pointer:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: {output_field} "
                    f"does not match {BILL_LAW_SPINE} {spine_field}"
                )
        review_packet = lifecycle_row.get("review_packet", "")
        if f"bill_id={bill_id}" not in review_packet or f"next_gate={gate}" not in review_packet:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: review_packet must name bill and next gate"
            )
        boundary = lifecycle_row.get("claim_boundary", "")
        if "model validation" not in boundary or "bill-specific finance/lobbying influence" not in boundary:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: claim boundary must reject model validation and bill-specific influence claims"
            )
        if not lifecycle_row.get("next_upgrade_reason", "").strip():
            failures.append(
                f"{BILL_LAW_LIFECYCLE_READINESS}: {bill_id}: missing next_upgrade_reason"
            )

    required_court_queue_columns = {
        "review_queue_rank",
        "lifecycle_review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "case_id",
        "case_name",
        "term",
        "decision_date",
        "matched_usc_sections",
        "court_usc_sections",
        "authority_document_numbers",
        "authority_agencies",
        "scdb_invalidated",
        "signed_opinion",
        "vote_margin",
        "direct_review_status",
        "review_question",
        "review_search_terms",
        "review_sources_needed",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_court_queue_columns = required_court_queue_columns - set(court_public_law_review_queue[0])
    if missing_court_queue_columns:
        failures.append(
            f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: missing columns {sorted(missing_court_queue_columns)}"
        )
    if not COURT_PUBLIC_LAW_REVIEW_QUEUE_MD.exists():
        failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE_MD}: missing markdown report")
    else:
        court_queue_md = COURT_PUBLIC_LAW_REVIEW_QUEUE_MD.read_text()
        if "not direct court-review evidence" not in court_queue_md:
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE_MD}: must label the queue as not direct court-review evidence"
            )
        if "Rows coded invalidated by SCDB" not in court_queue_md:
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE_MD}: must summarize SCDB invalidation coding"
            )
    expected_court_queue_rows: dict[tuple[str, str, str], dict[str, str]] = {}
    for court_row in court_matched_rows:
        case_id = court_row.get("case_id", "").strip()
        public_laws = sorted(split_semicolon_values(court_row, "public_law_numbers")) or [""]
        bill_ids = sorted(split_semicolon_values(court_row, "bill_ids")) or [""]
        for public_law in public_laws:
            matching_bill_ids = [
                bill_id for bill_id in bill_ids
                if lifecycle_by_bill.get(bill_id, {}).get("public_law_number", "") == public_law
            ]
            if not matching_bill_ids:
                matching_bill_ids = bill_ids
            for bill_id in matching_bill_ids:
                expected_court_queue_rows[(case_id, public_law, bill_id)] = court_row
    actual_court_queue_rows = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        for row in court_public_law_review_queue
    }
    if actual_court_queue_rows != set(expected_court_queue_rows):
        failures.append(
            "court/public-law review queue mismatch: "
            f"missing from queue={sorted(set(expected_court_queue_rows) - actual_court_queue_rows)[:10]}, "
            f"extra={sorted(actual_court_queue_rows - set(expected_court_queue_rows))[:10]}"
        )
    queue_ranks: list[int] = []
    for row in court_public_law_review_queue:
        key = (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        source_row = expected_court_queue_rows.get(key, {})
        lifecycle_row = lifecycle_by_bill.get(row.get("bill_id", "").strip(), {})
        rank = parse_int(row.get("review_queue_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: invalid review_queue_rank")
        else:
            queue_ranks.append(rank)
        lifecycle_rank = row.get("lifecycle_review_rank", "").strip()
        expected_lifecycle_rank = lifecycle_row.get("review_priority_rank", "").strip()
        if lifecycle_rank != expected_lifecycle_rank:
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: lifecycle_review_rank does not match "
                f"{BILL_LAW_LIFECYCLE_READINESS}"
            )
        if row.get("policy_area", "").strip() != lifecycle_row.get("policy_area", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: policy_area does not match lifecycle queue"
            )
        if row.get("direct_review_status") != "needs_direct_case_to_public_law_review":
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: invalid direct_review_status")
        if row.get("matched_usc_sections", "").strip() != source_row.get("matched_usc_sections", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: matched_usc_sections does not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("court_usc_sections", "").strip() != source_row.get("court_usc_sections", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: court_usc_sections does not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("authority_document_numbers", "").strip() != source_row.get("authority_document_numbers", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: authority documents do not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("authority_agencies", "").strip() != source_row.get("authority_agencies", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: authority agencies do not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("scdb_invalidated", "").strip() != source_row.get("invalidated", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: scdb_invalidated does not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("signed_opinion", "").strip() != source_row.get("signed_opinion", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: signed_opinion does not match "
                f"{COURT_LAW_LINKAGE}"
            )
        if row.get("vote_margin", "").strip() != source_row.get("vote_margin", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: vote_margin does not match "
                f"{COURT_LAW_LINKAGE}"
            )
        review_question = row.get("review_question", "")
        if key[0] not in review_question or key[1] not in review_question or key[2] not in review_question:
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: review_question must name case, public law, and bill"
            )
        if not row.get("review_sources_needed", "").strip():
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: missing review_sources_needed")
        if "court_public_law_review_queue" not in row.get("evidence_layers", ""):
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: missing queue evidence layer")
        if "direct_case_to_public_law_identifier" not in row.get("missing_links", ""):
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: missing direct-case gap")
        if "model_validation" not in row.get("missing_links", ""):
            failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: missing model-validation gap")
        boundary = row.get("claim_boundary", "")
        if "does not prove" not in boundary or "model-validation" not in boundary:
            failures.append(
                f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: {key}: claim_boundary must reject proof and model-validation claims"
            )
    if sorted(queue_ranks) != list(range(1, len(court_public_law_review_queue) + 1)):
        failures.append(f"{COURT_PUBLIC_LAW_REVIEW_QUEUE}: review ranks must be contiguous")

    required_temporal_triage_columns = {
        "triage_rank",
        "review_queue_rank",
        "bill_id",
        "public_law_number",
        "case_id",
        "case_name",
        "decision_date",
        "enacted_date",
        "days_after_enactment",
        "matched_usc_sections",
        "temporal_status",
        "direct_review_status_after_temporal_screen",
        "next_review_action",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_temporal_triage_columns = (
        required_temporal_triage_columns - set(court_public_law_temporal_triage[0])
    )
    if missing_temporal_triage_columns:
        failures.append(
            f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: missing columns "
            f"{sorted(missing_temporal_triage_columns)}"
        )
    if not COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD.exists():
        failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD}: missing markdown report")
    else:
        temporal_md = COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD.read_text()
        if "date screen" not in temporal_md or "does not prove direct court review" not in temporal_md:
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD}: must describe temporal screening and reject direct-review proof"
            )
        if "Pre-enactment rows ruled out" not in temporal_md:
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE_MD}: must summarize pre-enactment exclusions"
            )
    queue_by_key = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        ): row
        for row in court_public_law_review_queue
    }
    temporal_keys = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        for row in court_public_law_temporal_triage
    }
    if temporal_keys != set(queue_by_key):
        failures.append(
            "court/public-law temporal triage mismatch: "
            f"missing from triage={sorted(set(queue_by_key) - temporal_keys)[:10]}, "
            f"extra={sorted(temporal_keys - set(queue_by_key))[:10]}"
        )
    triage_ranks: list[int] = []
    for row in court_public_law_temporal_triage:
        key = (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        queue_row = queue_by_key.get(key, {})
        spine_row = spine_by_bill.get(row.get("bill_id", "").strip(), {})
        triage_rank = parse_int(row.get("triage_rank", ""))
        if triage_rank is None or triage_rank <= 0:
            failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: invalid triage_rank")
        else:
            triage_ranks.append(triage_rank)
        if row.get("review_queue_rank", "").strip() != queue_row.get("review_queue_rank", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: review_queue_rank does not match queue"
            )
        if row.get("decision_date", "").strip() != queue_row.get("decision_date", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: decision_date does not match queue"
            )
        if row.get("matched_usc_sections", "").strip() != queue_row.get("matched_usc_sections", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: matched_usc_sections does not match queue"
            )
        if row.get("enacted_date", "").strip() != spine_row.get("enacted_date", "").strip():
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: enacted_date does not match spine"
            )
        decision_date = parse_report_date(row.get("decision_date", ""))
        enacted_date = parse_report_date(row.get("enacted_date", ""))
        if decision_date and enacted_date:
            expected_days = (decision_date - enacted_date).days
            expected_status = (
                "pre_enactment_impossible_direct_review_of_listed_public_law"
                if expected_days < 0
                else "post_enactment_possible_needs_direct_source_review"
            )
            expected_direct_status = (
                "temporally_excluded_for_listed_public_law"
                if expected_days < 0
                else "post_enactment_source_review_needed"
            )
            if row.get("days_after_enactment", "") != str(expected_days):
                failures.append(
                    f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: days_after_enactment mismatch"
                )
        else:
            expected_status = "missing_date_needs_source_review"
            expected_direct_status = "date_screen_inconclusive"
            if row.get("days_after_enactment", ""):
                failures.append(
                    f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: missing-date row should not have day offset"
                )
        if row.get("temporal_status", "") != expected_status:
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: temporal_status mismatch"
            )
        if row.get("direct_review_status_after_temporal_screen", "") != expected_direct_status:
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: direct-review status mismatch"
            )
        if not row.get("next_review_action", "").strip():
            failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: missing next_review_action")
        if "court_public_law_temporal_triage" not in row.get("evidence_layers", ""):
            failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: missing temporal triage layer")
        if "direct_case_to_public_law_identifier" not in row.get("missing_links", ""):
            failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: missing direct-case gap")
        boundary = row.get("claim_boundary", "")
        if "Temporal triage only" not in boundary or "does not prove" not in boundary or "model-validation" not in boundary:
            failures.append(
                f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: {key}: claim_boundary must reject direct-review proof and model-validation claims"
            )
    if sorted(triage_ranks) != list(range(1, len(court_public_law_temporal_triage) + 1)):
        failures.append(f"{COURT_PUBLIC_LAW_TEMPORAL_TRIAGE}: triage ranks must be contiguous")

    required_direct_review_raw_columns = {
        "case_id",
        "public_law_number",
        "bill_id",
        "review_status",
        "direct_case_to_public_law_identifier",
        "direct_case_to_bill_identifier",
        "reviewed_case_disposition_to_public_law",
        "usc_section_relationship",
        "case_source_url",
        "public_law_source_url",
        "case_source_summary",
        "public_law_source_summary",
        "source_review_notes",
        "claim_boundary",
    }
    missing_direct_review_raw_columns = (
        required_direct_review_raw_columns - set(court_public_law_direct_review_raw[0])
    )
    if missing_direct_review_raw_columns:
        failures.append(
            f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: missing columns "
            f"{sorted(missing_direct_review_raw_columns)}"
        )
    required_direct_review_columns = {
        "review_rank",
        "triage_rank",
        "review_queue_rank",
        "bill_id",
        "public_law_number",
        "case_id",
        "case_name",
        "decision_date",
        "enacted_date",
        "days_after_enactment",
        "matched_usc_sections",
        "direct_review_determination",
        "direct_case_to_public_law_identifier",
        "direct_case_to_bill_identifier",
        "reviewed_case_disposition_to_public_law",
        "usc_section_relationship",
        "case_source_url",
        "public_law_source_url",
        "case_source_summary",
        "public_law_source_summary",
        "source_review_notes",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_direct_review_columns = (
        required_direct_review_columns - set(court_public_law_direct_review[0])
    )
    if missing_direct_review_columns:
        failures.append(
            f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: missing columns "
            f"{sorted(missing_direct_review_columns)}"
        )
    if not COURT_PUBLIC_LAW_DIRECT_REVIEW_MD.exists():
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_MD}: missing markdown report")
    else:
        direct_review_md = COURT_PUBLIC_LAW_DIRECT_REVIEW_MD.read_text()
        for phrase in (
            "Direct public-law review rows: 0",
            "Source-reviewed not-direct rows: 1",
            "Remaining source-review-needed rows: 0",
            "## Source Evidence",
            "## Temporal Exclusion Summary",
            "Claim boundary",
        ):
            if phrase not in direct_review_md:
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
        if "not model-validation evidence" not in direct_review_md:
            failures.append(
                f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_MD}: must reject model-validation evidence"
            )
    direct_review_raw_by_key = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        ): row
        for row in court_public_law_direct_review_raw
    }
    if len(direct_review_raw_by_key) != len(court_public_law_direct_review_raw):
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: duplicate review keys")
    post_enactment_keys = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        for row in court_public_law_temporal_triage
        if row.get("temporal_status", "") == "post_enactment_possible_needs_direct_source_review"
    }
    if set(direct_review_raw_by_key) != post_enactment_keys:
        failures.append(
            "court/public-law direct-review raw mismatch: "
            f"missing from raw={sorted(post_enactment_keys - set(direct_review_raw_by_key))}, "
            f"extra={sorted(set(direct_review_raw_by_key) - post_enactment_keys)}"
        )
    valid_direct_review_statuses = {
        "reviewed_not_direct_public_law_review",
        "reviewed_direct_public_law_review",
    }
    for raw_key, row in direct_review_raw_by_key.items():
        if row.get("review_status", "") not in valid_direct_review_statuses:
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: invalid review_status")
        flag_fields = (
            "direct_case_to_public_law_identifier",
            "direct_case_to_bill_identifier",
            "reviewed_case_disposition_to_public_law",
        )
        if any(row.get(field, "").strip() not in {"0", "1"} for field in flag_fields):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: direct-review flags must be 0/1")
        if row.get("review_status", "") != "reviewed_direct_public_law_review":
            if any(row.get(field, "").strip() != "0" for field in flag_fields):
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: not-direct source review should not carry direct-review flags"
                )
        if not row.get("case_source_url", "").startswith("https://www.supremecourt.gov/"):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: case source must be official Supreme Court")
        if not row.get("public_law_source_url", "").startswith("https://www.govinfo.gov/"):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: public-law source must be official GovInfo")
        notes = row.get("source_review_notes", "")
        if "directly challenged" not in notes or "shared 38 U.S.C. 5110 metadata only" not in notes:
            failures.append(
                f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: notes must explain no direct review and shared-section basis"
            )
        boundary = row.get("claim_boundary", "")
        if "Manual source review" not in boundary or "model-validation" not in boundary:
            failures.append(
                f"{COURT_PUBLIC_LAW_DIRECT_REVIEW_RAW}: {raw_key}: claim boundary must identify manual source review and reject model validation"
            )
    direct_review_by_key = {
        (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        ): row
        for row in court_public_law_direct_review
    }
    if len(direct_review_by_key) != len(court_public_law_direct_review):
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: duplicate review keys")
    if set(direct_review_by_key) != temporal_keys:
        failures.append(
            "court/public-law direct-review report mismatch: "
            f"missing from report={sorted(temporal_keys - set(direct_review_by_key))[:10]}, "
            f"extra={sorted(set(direct_review_by_key) - temporal_keys)[:10]}"
        )
    direct_review_ranks: list[int] = []
    direct_public_law_review_count = 0
    source_reviewed_not_direct_count = 0
    for row in court_public_law_direct_review:
        direct_key = (
            row.get("case_id", "").strip(),
            row.get("public_law_number", "").strip(),
            row.get("bill_id", "").strip(),
        )
        triage_row = next(
            (
                triage
                for triage in court_public_law_temporal_triage
                if (
                    triage.get("case_id", "").strip(),
                    triage.get("public_law_number", "").strip(),
                    triage.get("bill_id", "").strip(),
                ) == direct_key
            ),
            {},
        )
        review_rank = parse_int(row.get("review_rank", ""))
        if review_rank is None or review_rank <= 0:
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: invalid review_rank")
        else:
            direct_review_ranks.append(review_rank)
        for field in (
            "triage_rank",
            "review_queue_rank",
            "case_name",
            "decision_date",
            "enacted_date",
            "days_after_enactment",
            "matched_usc_sections",
        ):
            if row.get(field, "").strip() != triage_row.get(field, "").strip():
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: {field} does not match temporal triage"
                )
        flag_fields = (
            "direct_case_to_public_law_identifier",
            "direct_case_to_bill_identifier",
            "reviewed_case_disposition_to_public_law",
        )
        if any(row.get(field, "").strip() not in {"0", "1"} for field in flag_fields):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: direct-review flags must be 0/1")
        determination = row.get("direct_review_determination", "")
        if determination == "reviewed_direct_public_law_review":
            direct_public_law_review_count += 1
        if determination == "reviewed_not_direct_public_law_review":
            source_reviewed_not_direct_count += 1
        if triage_row.get("temporal_status", "") == "pre_enactment_impossible_direct_review_of_listed_public_law":
            if determination != "temporally_excluded_before_public_law_enactment":
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: pre-enactment row should be temporally excluded"
                )
            if any(row.get(field, "").strip() != "0" for field in flag_fields):
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: temporal exclusion should carry zero direct-review flags"
                )
            if row.get("usc_section_relationship", "") != "temporal_exclusion":
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: temporal exclusion relationship mismatch"
                )
        elif triage_row.get("temporal_status", "") == "post_enactment_possible_needs_direct_source_review":
            raw_row = direct_review_raw_by_key.get(direct_key, {})
            if determination != raw_row.get("review_status", ""):
                failures.append(
                    f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: determination does not match raw source review"
                )
            for field in (
                "direct_case_to_public_law_identifier",
                "direct_case_to_bill_identifier",
                "reviewed_case_disposition_to_public_law",
                "usc_section_relationship",
                "case_source_url",
                "public_law_source_url",
                "case_source_summary",
                "public_law_source_summary",
                "source_review_notes",
            ):
                if row.get(field, "").strip() != raw_row.get(field, "").strip():
                    failures.append(
                        f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: {field} does not match raw source review"
                    )
            if determination != "reviewed_direct_public_law_review":
                if any(row.get(field, "").strip() != "0" for field in flag_fields):
                    failures.append(
                        f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: not-direct review should carry zero direct-review flags"
                    )
                if row.get("usc_section_relationship", "") != "shared_usc_section_reference_only":
                    failures.append(
                        f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: expected shared-section relationship"
                    )
        if "court_public_law_direct_review_disposition" not in row.get("evidence_layers", ""):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: missing direct-review evidence layer")
        if "model_validation" not in row.get("missing_links", ""):
            failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: missing model-validation gap")
        boundary = row.get("claim_boundary", "")
        if "Source-reviewed direct-review disposition only" not in boundary or "model-validation" not in boundary:
            failures.append(
                f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: {direct_key}: claim boundary must reject direct-review overclaiming and model validation"
            )
    if sorted(direct_review_ranks) != list(range(1, len(court_public_law_direct_review) + 1)):
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: review ranks must be contiguous")
    if direct_public_law_review_count != 0:
        failures.append(f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: expected no direct public-law review rows")
    if source_reviewed_not_direct_count != len(direct_review_raw_by_key):
        failures.append(
            f"{COURT_PUBLIC_LAW_DIRECT_REVIEW}: source-reviewed not-direct count does not match raw review rows"
        )

    required_lifecycle_next_action_columns = {
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
    }
    missing_lifecycle_next_action_columns = (
        required_lifecycle_next_action_columns - set(bill_law_lifecycle_next_actions[0])
    )
    if missing_lifecycle_next_action_columns:
        failures.append(
            f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: missing columns "
            f"{sorted(missing_lifecycle_next_action_columns)}"
        )
    if not BILL_LAW_LIFECYCLE_NEXT_ACTIONS_MD.exists():
        failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS_MD}: missing markdown report")
    else:
        next_actions_md = BILL_LAW_LIFECYCLE_NEXT_ACTIONS_MD.read_text()
        for phrase in (
            "Closed direct-review gates: 18",
            "Rows with all queued court overlaps closed without direct public-law review: 9",
            "Rows with direct public-law review found: 0",
            "Rows still needing court/public-law source review: 0",
            "Actionable next upgrade gate counts",
            "Claim boundary",
        ):
            if phrase not in next_actions_md:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS_MD}: missing summary phrase {phrase!r}"
                )
    lifecycle_next_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_law_lifecycle_next_actions
        if row.get("bill_id", "").strip()
    }
    if len(lifecycle_next_by_bill) != len(bill_law_lifecycle_next_actions):
        failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: duplicate bill_id rows")
    if set(lifecycle_next_by_bill) != set(lifecycle_by_bill):
        failures.append(
            "bill-law lifecycle next-actions/readiness bill mismatch: "
            f"missing from next-actions={sorted(set(lifecycle_by_bill) - set(lifecycle_next_by_bill))}, "
            f"extra={sorted(set(lifecycle_next_by_bill) - set(lifecycle_by_bill))}"
        )
    direct_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in court_public_law_direct_review:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            direct_rows_by_bill[bill_id].append(row)

    next_action_ranks: list[int] = []
    closed_gate_total = 0
    closed_without_direct_rows = 0
    direct_found_rows = 0
    source_review_needed_rows = 0
    for bill_id, action_row in lifecycle_next_by_bill.items():
        lifecycle_row = lifecycle_by_bill.get(bill_id, {})
        action_rank = parse_int(action_row.get("action_rank", ""))
        if action_rank is None or action_rank <= 0:
            failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: invalid action_rank")
        else:
            next_action_ranks.append(action_rank)
        for field_pair in (
            ("base_review_priority_rank", "review_priority_rank"),
            ("public_law_number", "public_law_number"),
            ("policy_area", "policy_area"),
            ("lifecycle_readiness_tier", "lifecycle_readiness_tier"),
            ("review_score", "review_score"),
            ("high_priority_gaps", "high_priority_gaps"),
        ):
            output_field, lifecycle_field = field_pair
            if action_row.get(output_field, "").strip() != lifecycle_row.get(lifecycle_field, "").strip():
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: {output_field} "
                    f"does not match {BILL_LAW_LIFECYCLE_READINESS} {lifecycle_field}"
                )
        direct_rows = direct_rows_by_bill.get(bill_id, [])
        determinations = {
            row.get("direct_review_determination", "")
            for row in direct_rows
        }
        if not direct_rows:
            expected_status = "no_queued_court_public_law_overlap"
        elif "missing_date_source_review_needed" in determinations:
            expected_status = "court_public_law_source_review_needed"
        elif any(
            row.get("direct_review_determination") == "reviewed_direct_public_law_review"
            or row.get("direct_case_to_public_law_identifier") == "1"
            or row.get("reviewed_case_disposition_to_public_law") == "1"
            for row in direct_rows
        ):
            expected_status = "direct_public_law_review_found"
        elif determinations <= {
            "temporally_excluded_before_public_law_enactment",
            "reviewed_not_direct_public_law_review",
        }:
            expected_status = "all_queued_court_overlaps_closed_without_direct_public_law_review"
        else:
            expected_status = "mixed_court_public_law_review_status"
        if action_row.get("court_direct_review_status", "") != expected_status:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: court_direct_review_status mismatch"
            )
        if expected_status == "all_queued_court_overlaps_closed_without_direct_public_law_review":
            closed_without_direct_rows += 1
        if expected_status == "direct_public_law_review_found":
            direct_found_rows += 1
        if expected_status == "court_public_law_source_review_needed":
            source_review_needed_rows += 1
        expected_direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "reviewed_direct_public_law_review"
        )
        expected_not_direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "reviewed_not_direct_public_law_review"
        )
        expected_temporal_count = sum(
            1 for row in direct_rows
            if row.get("direct_review_determination") == "temporally_excluded_before_public_law_enactment"
        )
        count_checks = {
            "court_direct_review_rows": len(direct_rows),
            "court_direct_review_direct_rows": expected_direct_count,
            "court_direct_review_not_direct_rows": expected_not_direct_count,
            "court_direct_review_temporal_exclusions": expected_temporal_count,
        }
        for field, expected in count_checks.items():
            if parse_int(action_row.get(field, "")) != expected:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: {field} mismatch"
                )
        base_gaps = split_semicolon_values(lifecycle_row, "high_priority_gaps")
        expected_closed: set[str] = set()
        if expected_status == "all_queued_court_overlaps_closed_without_direct_public_law_review":
            expected_closed = LIFECYCLE_DIRECT_REVIEW_GATES & base_gaps
        elif expected_status == "direct_public_law_review_found":
            if any(row.get("direct_case_to_public_law_identifier") == "1" for row in direct_rows):
                expected_closed.add("direct_case_to_public_law_identifier")
            if any(row.get("reviewed_case_disposition_to_public_law") == "1" for row in direct_rows):
                expected_closed.add("reviewed_case_disposition_to_public_law")
            expected_closed &= base_gaps
        actual_closed = split_semicolon_values(action_row, "closed_review_gates")
        if actual_closed != expected_closed:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: closed_review_gates mismatch"
            )
        closed_count = parse_int(action_row.get("closed_review_gate_count", ""))
        if closed_count != len(expected_closed):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: closed_review_gate_count mismatch"
            )
        closed_gate_total += len(expected_closed)
        expected_actionable = base_gaps - expected_closed
        actual_actionable = split_semicolon_values(action_row, "actionable_high_priority_gaps")
        if actual_actionable != expected_actionable:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: actionable_high_priority_gaps mismatch"
            )
        if parse_int(action_row.get("actionable_gap_count", "")) != len(expected_actionable):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: actionable_gap_count mismatch"
            )
        next_gate = action_row.get("next_actionable_upgrade_gate", "")
        if expected_actionable:
            if next_gate not in expected_actionable:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: next_actionable_upgrade_gate is not actionable"
                )
        elif next_gate != "none":
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: expected no next actionable gate"
            )
        if expected_closed and next_gate in expected_closed:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: next gate repeats a closed direct-review gate"
            )
        if bill_id == "117-s-3373":
            if expected_closed != LIFECYCLE_DIRECT_REVIEW_GATES:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: expected both direct-review gates closed"
                )
            if next_gate != "codified_usc_lineage":
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: expected codified_usc_lineage after Arellano source review"
                )
        packet = action_row.get("action_packet", "")
        if (
            f"bill_id={bill_id}" not in packet
            or f"base_rank={lifecycle_row.get('review_priority_rank', '')}" not in packet
            or f"next_actionable_gate={next_gate}" not in packet
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: action_packet must name bill, base rank, and next gate"
            )
        boundary = action_row.get("claim_boundary", "")
        if "Post-direct-review lifecycle action queue only" not in boundary or "model validation" not in boundary:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: {bill_id}: claim boundary must reject validation claims"
            )
    if sorted(next_action_ranks) != list(range(1, len(bill_law_lifecycle_next_actions) + 1)):
        failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: action ranks must be contiguous")
    if closed_gate_total != 18:
        failures.append(f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: expected 18 closed direct-review gates")
    if closed_without_direct_rows != 9 or direct_found_rows != 0 or source_review_needed_rows != 0:
        failures.append(
            f"{BILL_LAW_LIFECYCLE_NEXT_ACTIONS}: court direct-review status summary mismatch"
        )

    required_lifecycle_corpus_columns = {
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
    }
    missing_lifecycle_corpus_columns = (
        required_lifecycle_corpus_columns - set(bill_law_lifecycle_corpus[0])
    )
    if missing_lifecycle_corpus_columns:
        failures.append(
            f"{BILL_LAW_LIFECYCLE_CORPUS}: missing columns "
            f"{sorted(missing_lifecycle_corpus_columns)}"
        )
    if not BILL_LAW_LIFECYCLE_CORPUS_MD.exists():
        failures.append(f"{BILL_LAW_LIFECYCLE_CORPUS_MD}: missing markdown report")
    else:
        lifecycle_corpus_md = BILL_LAW_LIFECYCLE_CORPUS_MD.read_text()
        for phrase in (
            "one bounded packet per public-law row",
            "not validation evidence",
            "Rows with acquired bill-topic survey items",
            "Rows with source-reviewed target-section diff coverage",
            "Rows with campaign-finance target-scope review",
            "Rows with public comment text available and hashed",
            "Claim boundary",
        ):
            if phrase not in lifecycle_corpus_md:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_CORPUS_MD}: missing summary phrase {phrase!r}"
                )
    lifecycle_corpus_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_law_lifecycle_corpus
        if row.get("bill_id", "").strip()
    }
    if len(lifecycle_corpus_by_bill) != len(bill_law_lifecycle_corpus):
        failures.append(f"{BILL_LAW_LIFECYCLE_CORPUS}: duplicate bill_id rows")
    if set(lifecycle_corpus_by_bill) != set(lifecycle_next_by_bill):
        failures.append(
            "bill-law lifecycle corpus/next-actions bill mismatch: "
            f"missing from corpus={sorted(set(lifecycle_next_by_bill) - set(lifecycle_corpus_by_bill))}, "
            f"extra={sorted(set(lifecycle_corpus_by_bill) - set(lifecycle_next_by_bill))}"
        )
    corpus_ranks: list[int] = []
    for bill_id, corpus_row in lifecycle_corpus_by_bill.items():
        action_row = lifecycle_next_by_bill.get(bill_id, {})
        spine_row = spine_by_bill.get(bill_id, {})
        corpus_rank = parse_int(corpus_row.get("corpus_rank", ""))
        if corpus_rank is None or corpus_rank <= 0:
            failures.append(f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: invalid corpus_rank")
        else:
            corpus_ranks.append(corpus_rank)
        for field in (
            "action_rank",
            "public_law_number",
            "policy_area",
            "lifecycle_readiness_tier",
            "review_score",
            "next_actionable_upgrade_gate",
            "actionable_high_priority_gaps",
            "actionable_gap_count",
            "closed_review_gates",
            "closed_review_gate_count",
        ):
            if corpus_row.get(field, "").strip() != action_row.get(field, "").strip():
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: {field} "
                    f"does not match {BILL_LAW_LIFECYCLE_NEXT_ACTIONS}"
                )
        if corpus_row.get("corpus_rank", "").strip() != action_row.get("action_rank", "").strip():
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: corpus_rank must match action_rank"
            )
        if int(spine_row.get("actions_count", "0") or "0") > 0:
            if corpus_row.get("bill_history_context_status") != (
                "bounded_congressgov_public_law_bill_action_context"
            ):
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: bill history status mismatch"
                )
        if spine_row.get("sponsor_bioguide_id", "").strip():
            if corpus_row.get("sponsor_context_status") != "sponsor_metadata_present":
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: sponsor status mismatch"
                )
        direct_rows = direct_rows_by_bill.get(bill_id, [])
        expected_source_summary_rows = sum(
            1 for row in direct_rows
            if row.get("case_source_summary", "").strip()
            or row.get("public_law_source_summary", "").strip()
        )
        if parse_int(corpus_row.get("court_direct_review_source_summary_rows", "")) != (
            expected_source_summary_rows
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: court source-summary count mismatch"
            )
        if corpus_row.get("court_review_status", "") != action_row.get("court_direct_review_status", ""):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: court_review_status mismatch"
            )
        actionable_gap_count = parse_int(corpus_row.get("actionable_gap_count", "")) or 0
        if actionable_gap_count > 0 and (
            corpus_row.get("publication_readiness_status", "")
            == "candidate_for_claim_ledger_review"
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: publication status overstates open gaps"
            )
        if actionable_gap_count > 0 and not corpus_row.get("publication_readiness_status", "").startswith(
            "not_publication_claim_ready"
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: publication status must preserve open-gap boundary"
            )
        if parse_int(corpus_row.get("source_reviewed_subgate_count", "")) is None:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: invalid source_reviewed_subgate_count"
            )
        artifacts = split_semicolon_values(corpus_row, "source_artifacts")
        for required_artifact in (
            str(BILL_LAW_SPINE),
            str(BILL_LAW_LIFECYCLE_NEXT_ACTIONS),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: missing source artifact {required_artifact}"
                )
        if (
            corpus_row.get("public_opinion_proxy_review_status", "")
            != "no_survey_proxy_review_row"
            and str(DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW) not in artifacts
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: missing survey proxy source artifact"
            )
        if (
            corpus_row.get("campaign_finance_target_scope_status", "")
            != "not_in_campaign_finance_target_scope_review"
            and str(BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW) not in artifacts
        ):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: missing campaign target-scope source artifact"
            )
        if "bill_law_lifecycle_corpus" not in split_semicolon_values(corpus_row, "evidence_layers"):
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: missing corpus evidence layer"
            )
        boundary = corpus_row.get("claim_boundary", "")
        if "Public-law lifecycle corpus only" not in boundary or "model validation" not in boundary:
            failures.append(
                f"{BILL_LAW_LIFECYCLE_CORPUS}: {bill_id}: claim boundary must reject validation claims"
            )
    if sorted(corpus_ranks) != list(range(1, len(bill_law_lifecycle_corpus) + 1)):
        failures.append(f"{BILL_LAW_LIFECYCLE_CORPUS}: corpus ranks must be contiguous")

    required_bill_finance_lobbying_columns = {
        "review_rank",
        "action_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "introduced_date",
        "enacted_date",
        "lifecycle_readiness_tier",
        "review_score",
        "actionable_gap_count",
        "campaign_finance_context_rows",
        "campaign_finance_context_transaction_rows",
        "campaign_finance_unique_candidates",
        "campaign_finance_context_bill_ids",
        "campaign_finance_context_enacted_bill_ids",
        "campaign_finance_current_bill_exact_match",
        "lobbying_context_issue_rows",
        "lobbying_context_activity_rows",
        "lobbying_context_total_amount",
        "lobbying_context_bill_contexts",
        "lobbying_context_bill_ids",
        "lobbying_context_enacted_bill_ids",
        "lobbying_context_issues",
        "lobbying_current_bill_exact_match",
        "review_status",
        "recommended_review_sources",
        "review_packet",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_bill_finance_lobbying_columns = (
        required_bill_finance_lobbying_columns - set(bill_finance_lobbying_review_queue[0])
    )
    if missing_bill_finance_lobbying_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: missing columns "
            f"{sorted(missing_bill_finance_lobbying_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_REVIEW_QUEUE_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE_MD}: missing markdown report")
    else:
        finance_lobbying_md = BILL_FINANCE_LOBBYING_REVIEW_QUEUE_MD.read_text()
        for phrase in (
            "Queued public-law rows",
            "Rows with current bill ID in campaign-finance context",
            "Rows with current bill ID in lobbying context",
            "Claim boundary",
        ):
            if phrase not in finance_lobbying_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE_MD}: missing summary phrase {phrase!r}"
                )
    expected_finance_lobbying_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_law_lifecycle_next_actions
        if row.get("next_actionable_upgrade_gate", "") == "bill_specific_campaign_finance_or_lobbying_to_bill"
        and row.get("bill_id", "").strip()
    }
    finance_lobbying_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_review_queue
        if row.get("bill_id", "").strip()
    }
    if len(finance_lobbying_by_bill) != len(bill_finance_lobbying_review_queue):
        failures.append(f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: duplicate bill_id rows")
    if set(finance_lobbying_by_bill) != set(expected_finance_lobbying_by_bill):
        failures.append(
            "finance/lobbying queue/lifecycle next-actions mismatch: "
            f"missing from queue={sorted(set(expected_finance_lobbying_by_bill) - set(finance_lobbying_by_bill))}, "
            f"extra={sorted(set(finance_lobbying_by_bill) - set(expected_finance_lobbying_by_bill))}"
        )
    finance_lobbying_ranks: list[int] = []
    for bill_id, queue_row in finance_lobbying_by_bill.items():
        action_row = expected_finance_lobbying_by_bill.get(bill_id, {})
        spine_row = spine_by_bill.get(bill_id, {})
        review_rank = parse_int(queue_row.get("review_rank", ""))
        if review_rank is None or review_rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: invalid review_rank")
        else:
            finance_lobbying_ranks.append(review_rank)
        for field in (
            "action_rank",
            "public_law_number",
            "policy_area",
            "lifecycle_readiness_tier",
            "review_score",
            "actionable_gap_count",
        ):
            if queue_row.get(field, "").strip() != action_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: {field} "
                    f"does not match {BILL_LAW_LIFECYCLE_NEXT_ACTIONS}"
                )
        for field in (
            "sponsor_bioguide_id",
            "sponsor_party",
            "sponsor_state",
            "introduced_date",
            "enacted_date",
            "source_url",
        ):
            if queue_row.get(field, "").strip() != spine_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: {field} "
                    f"does not match {BILL_LAW_SPINE}"
                )
        spine_to_queue_fields = {
            "campaign_finance_sponsor_policy_context_rows": "campaign_finance_context_rows",
            "campaign_finance_sponsor_policy_context_transaction_rows": "campaign_finance_context_transaction_rows",
            "campaign_finance_sponsor_policy_context_unique_candidates": "campaign_finance_unique_candidates",
            "campaign_finance_sponsor_policy_context_enacted_bill_ids": "campaign_finance_context_enacted_bill_ids",
            "lobbying_policy_context_issue_rows": "lobbying_context_issue_rows",
            "lobbying_policy_context_activity_rows": "lobbying_context_activity_rows",
            "lobbying_policy_context_bill_contexts": "lobbying_context_bill_contexts",
            "lobbying_policy_context_enacted_bill_ids": "lobbying_context_enacted_bill_ids",
            "lobbying_policy_context_issues": "lobbying_context_issues",
        }
        for spine_field, queue_field in spine_to_queue_fields.items():
            if queue_row.get(queue_field, "").strip() != spine_row.get(spine_field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: {queue_field} "
                    f"does not match {BILL_LAW_SPINE} {spine_field}"
                )
        expected_lobbying_total = f"{parse_float(spine_row.get('lobbying_policy_context_total_amount', '0')) or 0.0:.2f}"
        if queue_row.get("lobbying_context_total_amount", "").strip() != expected_lobbying_total:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: lobbying total mismatch"
            )
        campaign_bill_ids = split_semicolon_values(
            spine_row,
            "campaign_finance_sponsor_policy_context_bill_ids",
        )
        lobbying_bill_ids = split_semicolon_values(spine_row, "lobbying_policy_context_bill_ids")
        if split_semicolon_values(queue_row, "campaign_finance_context_bill_ids") != campaign_bill_ids:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: campaign bill-id context mismatch"
            )
        if split_semicolon_values(queue_row, "lobbying_context_bill_ids") != lobbying_bill_ids:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: lobbying bill-id context mismatch"
            )
        campaign_exact = bill_id in campaign_bill_ids
        lobbying_exact = bill_id in lobbying_bill_ids
        if queue_row.get("campaign_finance_current_bill_exact_match", "") != yes_no(campaign_exact):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: campaign exact-match flag mismatch"
            )
        if queue_row.get("lobbying_current_bill_exact_match", "") != yes_no(lobbying_exact):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: lobbying exact-match flag mismatch"
            )
        campaign_context_rows = parse_int(spine_row.get("campaign_finance_sponsor_policy_context_rows", "")) or 0
        lobbying_context_rows = parse_int(spine_row.get("lobbying_policy_context_issue_rows", "")) or 0
        expected_status = finance_lobbying_review_status(
            campaign_exact,
            lobbying_exact,
            campaign_context_rows,
            lobbying_context_rows,
        )
        if queue_row.get("review_status", "") != expected_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: review_status mismatch"
            )
        recommended_sources = queue_row.get("recommended_review_sources", "")
        if "OpenFEC" not in recommended_sources or "Senate LDA" not in recommended_sources:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: missing recommended finance/LDA sources"
            )
        packet = queue_row.get("review_packet", "")
        for expected_packet_part in (
            f"bill_id={bill_id}",
            f"public_law={queue_row.get('public_law_number', '')}",
            f"campaign_exact_match={yes_no(campaign_exact)}",
            f"lobbying_exact_match={yes_no(lobbying_exact)}",
        ):
            if expected_packet_part not in packet:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: review_packet "
                    f"missing {expected_packet_part!r}"
                )
        expected_layers = {
            "bill_law_lifecycle_next_actions",
            "bill_law_evidence_spine",
        }
        if campaign_context_rows > 0:
            expected_layers.add("same_policy_campaign_finance_context")
        if lobbying_context_rows > 0:
            expected_layers.add("same_policy_lobbying_issue_bill_context")
        if campaign_exact:
            expected_layers.add("candidate_current_bill_campaign_context")
        if lobbying_exact:
            expected_layers.add("candidate_current_bill_lobbying_context")
        actual_layers = split_semicolon_values(queue_row, "evidence_layers")
        missing_layers = expected_layers - actual_layers
        if missing_layers:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: missing evidence layers "
                f"{sorted(missing_layers)}"
            )
        missing_links = queue_row.get("missing_links", "")
        for required_gap in (
            "bill_specific_campaign_finance_or_lobbying_to_bill",
            "client_to_specific_bill",
            "filing_text_bill_identifier",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: missing gap {required_gap!r}"
                )
        boundary = queue_row.get("claim_boundary", "")
        if "source-review queue only" not in boundary or "not evidence" not in boundary or "model validation" not in boundary:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: {bill_id}: claim boundary must reject evidence and validation claims"
            )
    if sorted(finance_lobbying_ranks) != list(range(1, len(bill_finance_lobbying_review_queue) + 1)):
        failures.append(f"{BILL_FINANCE_LOBBYING_REVIEW_QUEUE}: review ranks must be contiguous")

    required_bill_finance_lobbying_local_raw_columns = {
        "reviewed_queue_rank",
        "reviewed_bill_id",
        "reviewed_public_law_number",
        "manual_review_source",
        "manual_campaign_context_status",
        "manual_campaign_context_disposition",
        "manual_campaign_context_basis",
        "manual_lobbying_context_status",
        "manual_lobbying_context_disposition",
        "manual_lobbying_context_basis",
        "manual_bill_specific_gate_status",
        "manual_next_source_expansion",
        "manual_outcome_link_status",
        "manual_reviewer_note",
    }
    missing_bill_finance_lobbying_local_raw_columns = (
        required_bill_finance_lobbying_local_raw_columns
        - set(bill_finance_lobbying_local_context_review_raw[0])
    )
    if missing_bill_finance_lobbying_local_raw_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW}: missing columns "
            f"{sorted(missing_bill_finance_lobbying_local_raw_columns)}"
        )
    required_bill_finance_lobbying_local_columns = {
        "manual_review_rank",
        "review_rank",
        "action_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "introduced_date",
        "enacted_date",
        "lifecycle_readiness_tier",
        "review_score",
        "actionable_gap_count",
        "campaign_finance_context_rows",
        "campaign_finance_context_transaction_rows",
        "campaign_finance_unique_candidates",
        "campaign_finance_context_bill_ids",
        "campaign_finance_context_enacted_bill_ids",
        "campaign_finance_current_bill_exact_match",
        "lobbying_context_issue_rows",
        "lobbying_context_activity_rows",
        "lobbying_context_total_amount",
        "lobbying_context_bill_contexts",
        "lobbying_context_bill_ids",
        "lobbying_context_enacted_bill_ids",
        "lobbying_context_issues",
        "lobbying_current_bill_exact_match",
        "queue_review_status",
        "manual_review_source",
        "manual_campaign_context_status",
        "manual_campaign_context_disposition",
        "manual_campaign_context_basis",
        "manual_lobbying_context_status",
        "manual_lobbying_context_disposition",
        "manual_lobbying_context_basis",
        "manual_bill_specific_gate_status",
        "manual_next_source_expansion",
        "manual_outcome_link_status",
        "manual_reviewer_note",
        "recommended_review_sources",
        "review_packet",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_bill_finance_lobbying_local_columns = (
        required_bill_finance_lobbying_local_columns
        - set(bill_finance_lobbying_local_context_review[0])
    )
    if missing_bill_finance_lobbying_local_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: missing columns "
            f"{sorted(missing_bill_finance_lobbying_local_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_MD}: missing markdown report")
    else:
        local_review_md = BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_MD.read_text()
        for phrase in (
            "Bill-finance/lobbying queue rows reviewed",
            "Rows with same-policy campaign-finance context and no current-bill match",
            "Rows with no local campaign-finance context",
            "Rows with same-policy lobbying context and no current-bill match",
            "Rows with no local lobbying context",
            "Rows with local current-bill finance/lobbying exact match",
            "Rows still requiring external target/source expansion",
            "Rows with no outcome influence evidence",
            "Claim boundary",
        ):
            if phrase not in local_review_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    local_raw_by_rank: dict[str, dict[str, str]] = {}
    for raw_row in bill_finance_lobbying_local_context_review_raw:
        rank = raw_row.get("reviewed_queue_rank", "").strip()
        if rank in local_raw_by_rank:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW}: duplicate reviewed_queue_rank {rank}"
            )
        local_raw_by_rank[rank] = raw_row
    local_review_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_local_context_review
        if row.get("bill_id", "").strip()
    }
    if len(local_review_by_bill) != len(bill_finance_lobbying_local_context_review):
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: duplicate bill_id rows")
    queue_ranks = {row.get("review_rank", "").strip() for row in bill_finance_lobbying_review_queue}
    if set(local_raw_by_rank) != queue_ranks:
        failures.append(
            "bill-finance/lobbying local raw/queue rank mismatch: "
            f"missing from raw={sorted(queue_ranks - set(local_raw_by_rank))}, "
            f"extra={sorted(set(local_raw_by_rank) - queue_ranks)}"
        )
    if set(local_review_by_bill) != set(finance_lobbying_by_bill):
        failures.append(
            "bill-finance/lobbying local review/queue bill mismatch: "
            f"missing from local review={sorted(set(finance_lobbying_by_bill) - set(local_review_by_bill))}, "
            f"extra={sorted(set(local_review_by_bill) - set(finance_lobbying_by_bill))}"
        )
    local_ranks: list[int] = []
    campaign_no_match_count = 0
    campaign_absent_count = 0
    lobbying_no_match_count = 0
    lobbying_absent_count = 0
    local_exact_match_count = 0
    external_expansion_count = 0
    no_outcome_count = 0
    for bill_id, local_row in local_review_by_bill.items():
        queue_row = finance_lobbying_by_bill.get(bill_id, {})
        raw_row = local_raw_by_rank.get(local_row.get("manual_review_rank", "").strip(), {})
        rank = parse_int(local_row.get("manual_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: invalid manual_review_rank"
            )
        else:
            local_ranks.append(rank)
        if local_row.get("manual_review_rank", "").strip() != local_row.get("review_rank", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: manual rank must match queue rank"
            )
        if raw_row:
            if raw_row.get("reviewed_bill_id", "").strip() != bill_id:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW}: {bill_id}: raw bill mismatch"
                )
            if raw_row.get("reviewed_public_law_number", "").strip() != local_row.get("public_law_number", "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW_RAW}: {bill_id}: raw public-law mismatch"
                )
            for field in (
                "manual_review_source",
                "manual_campaign_context_status",
                "manual_campaign_context_disposition",
                "manual_campaign_context_basis",
                "manual_lobbying_context_status",
                "manual_lobbying_context_disposition",
                "manual_lobbying_context_basis",
                "manual_bill_specific_gate_status",
                "manual_next_source_expansion",
                "manual_outcome_link_status",
                "manual_reviewer_note",
            ):
                if local_row.get(field, "").strip() != raw_row.get(field, "").strip():
                    failures.append(
                        f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: "
                        f"{field} does not match raw review"
                    )
        if not local_row.get("manual_review_source", "").strip():
            failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: missing review source")
        if not local_row.get("manual_reviewer_note", "").strip():
            failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: missing reviewer note")
        for field in (
            "review_rank",
            "action_rank",
            "public_law_number",
            "policy_area",
            "sponsor_bioguide_id",
            "sponsor_party",
            "sponsor_state",
            "introduced_date",
            "enacted_date",
            "lifecycle_readiness_tier",
            "review_score",
            "actionable_gap_count",
            "campaign_finance_context_rows",
            "campaign_finance_context_transaction_rows",
            "campaign_finance_unique_candidates",
            "campaign_finance_context_bill_ids",
            "campaign_finance_context_enacted_bill_ids",
            "campaign_finance_current_bill_exact_match",
            "lobbying_context_issue_rows",
            "lobbying_context_activity_rows",
            "lobbying_context_total_amount",
            "lobbying_context_bill_contexts",
            "lobbying_context_bill_ids",
            "lobbying_context_enacted_bill_ids",
            "lobbying_context_issues",
            "lobbying_current_bill_exact_match",
            "recommended_review_sources",
            "review_packet",
            "source_url",
        ):
            if local_row.get(field, "").strip() != queue_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: {field} "
                    f"does not match {BILL_FINANCE_LOBBYING_REVIEW_QUEUE}"
                )
        if local_row.get("queue_review_status", "").strip() != queue_row.get("review_status", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: queue status mismatch"
            )
        if (
            local_row.get("campaign_finance_current_bill_exact_match", "").strip() == "yes"
            or local_row.get("lobbying_current_bill_exact_match", "").strip() == "yes"
        ):
            local_exact_match_count += 1
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: local review contains exact current-bill match"
            )
        campaign_context_rows = parse_int(local_row.get("campaign_finance_context_rows", "")) or 0
        lobbying_context_rows = parse_int(local_row.get("lobbying_context_issue_rows", "")) or 0
        if campaign_context_rows > 0:
            expected_campaign = (
                "reviewed_same_policy_campaign_context_no_current_bill_match",
                "local_campaign_context_available_no_current_bill_id",
                "same_policy_candidate_sponsor_bill_context_has_no_reviewed_bill_id",
            )
            campaign_no_match_count += 1
        else:
            expected_campaign = (
                "reviewed_no_local_campaign_context_available",
                "local_campaign_context_absent",
                "zero_local_campaign_context_rows_in_queue",
            )
            campaign_absent_count += 1
        actual_campaign = (
            local_row.get("manual_campaign_context_status", "").strip(),
            local_row.get("manual_campaign_context_disposition", "").strip(),
            local_row.get("manual_campaign_context_basis", "").strip(),
        )
        if actual_campaign != expected_campaign:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: campaign review status mismatch"
            )
        if lobbying_context_rows > 0:
            expected_lobbying = (
                "reviewed_same_policy_lobbying_context_no_current_bill_match",
                "local_lobbying_context_available_no_current_bill_id",
                "same_policy_lobbying_issue_bill_context_has_no_reviewed_bill_id",
            )
            lobbying_no_match_count += 1
        else:
            expected_lobbying = (
                "reviewed_no_local_lobbying_context_available",
                "local_lobbying_context_absent",
                "zero_local_lobbying_context_rows_in_queue",
            )
            lobbying_absent_count += 1
        actual_lobbying = (
            local_row.get("manual_lobbying_context_status", "").strip(),
            local_row.get("manual_lobbying_context_disposition", "").strip(),
            local_row.get("manual_lobbying_context_basis", "").strip(),
        )
        if actual_lobbying != expected_lobbying:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: lobbying review status mismatch"
            )
        if (
            local_row.get("manual_bill_specific_gate_status", "").strip()
            != "reviewed_local_context_no_current_bill_specific_finance_or_lobbying_match"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: invalid bill-specific gate status"
            )
        if campaign_context_rows > 0 and lobbying_context_rows > 0:
            expected_expansion = "external_current_bill_lobbying_and_campaign_finance_target_search_needed"
        elif campaign_context_rows > 0:
            expected_expansion = "external_current_bill_campaign_finance_target_search_needed"
        elif lobbying_context_rows > 0:
            expected_expansion = "external_current_bill_lobbying_target_search_needed"
        else:
            expected_expansion = "external_current_bill_campaign_finance_and_lobbying_source_search_needed"
        if local_row.get("manual_next_source_expansion", "").strip() != expected_expansion:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: next source-expansion status mismatch"
            )
        if local_row.get("manual_next_source_expansion", "").startswith("external_current_bill_"):
            external_expansion_count += 1
        if local_row.get("manual_outcome_link_status", "").strip() == "no_outcome_influence_evidence":
            no_outcome_count += 1
        else:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: invalid outcome link status"
            )
        expected_layers = {
            "bill_law_lifecycle_next_actions",
            "bill_law_evidence_spine",
            "bill_finance_lobbying_review_queue",
            "manual_bill_finance_lobbying_local_context_review",
        }
        if campaign_context_rows > 0:
            expected_layers.add("local_campaign_finance_sponsor_policy_context_review")
        if lobbying_context_rows > 0:
            expected_layers.add("local_lobbying_issue_bill_context_review")
        actual_layers = split_semicolon_values(local_row, "evidence_layers")
        if not expected_layers <= actual_layers:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: missing evidence layers "
                f"{sorted(expected_layers - actual_layers)}"
            )
        missing_links = local_row.get("missing_links", "")
        for required_gap in (
            "external_current_bill_campaign_finance_target_search",
            "external_current_bill_lobbying_search",
            "reviewed_outside_spending_target",
            "client_to_specific_bill",
            "sponsor_or_member_target_beyond_activity_text_reference",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = local_row.get("claim_boundary", "")
        for phrase in (
            "Manual bill-finance/lobbying local-context review only",
            "do not contain the reviewed current bill ID",
            "does not show absence",
            "committee-action influence",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(local_ranks) != list(range(1, len(bill_finance_lobbying_local_context_review) + 1)):
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: review ranks must be contiguous")
    expected_campaign_no_match_count = sum(
        1
        for row in bill_finance_lobbying_review_queue
        if (parse_int(row.get("campaign_finance_context_rows", "")) or 0) > 0
        and row.get("campaign_finance_current_bill_exact_match", "") == "no"
    )
    expected_campaign_absent_count = sum(
        1
        for row in bill_finance_lobbying_review_queue
        if (parse_int(row.get("campaign_finance_context_rows", "")) or 0) == 0
    )
    expected_lobbying_no_match_count = sum(
        1
        for row in bill_finance_lobbying_review_queue
        if (parse_int(row.get("lobbying_context_issue_rows", "")) or 0) > 0
        and row.get("lobbying_current_bill_exact_match", "") == "no"
    )
    expected_lobbying_absent_count = sum(
        1
        for row in bill_finance_lobbying_review_queue
        if (parse_int(row.get("lobbying_context_issue_rows", "")) or 0) == 0
    )
    if campaign_no_match_count != expected_campaign_no_match_count:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: campaign no-match count mismatch"
        )
    if campaign_absent_count != expected_campaign_absent_count:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: campaign absent count mismatch"
        )
    if lobbying_no_match_count != expected_lobbying_no_match_count:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: lobbying no-match count mismatch"
        )
    if lobbying_absent_count != expected_lobbying_absent_count:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: lobbying absent count mismatch"
        )
    if local_exact_match_count != 0:
        failures.append(f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: exact local match count must stay zero")
    if external_expansion_count != len(bill_finance_lobbying_local_context_review):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: all rows must require external expansion"
        )
    if no_outcome_count != len(bill_finance_lobbying_local_context_review):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_LOCAL_CONTEXT_REVIEW}: all rows must keep no-outcome-influence status"
        )

    required_external_lda_search_columns = {
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "introduced_date",
        "enacted_date",
        "search_term",
        "term_variant",
        "filing_year",
        "page_size",
        "pages_fetched",
        "api_reported_result_count",
        "fetched_filing_count",
        "unfetched_api_result_count",
        "exact_activity_match_count",
        "api_status",
        "source_url",
        "claim_boundary",
    }
    if bill_finance_lobbying_external_lda_searches_raw and (
        missing_columns := required_external_lda_search_columns
        - set(bill_finance_lobbying_external_lda_searches_raw[0])
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: missing columns "
            f"{sorted(missing_columns)}"
        )
    required_external_lda_mention_columns = {
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "search_term",
        "term_variant",
        "filing_year",
        "filing_uuid",
        "client_name",
        "registrant_name",
        "activity_description",
        "matched_bill_refs",
        "exact_current_bill_match",
        "source_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    if bill_finance_lobbying_external_lda_mentions_raw and (
        missing_columns := required_external_lda_mention_columns
        - set(bill_finance_lobbying_external_lda_mentions_raw[0])
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: missing columns "
            f"{sorted(missing_columns)}"
        )
    required_external_search_review_columns = {
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "local_next_source_expansion",
        "lda_search_rows",
        "lda_api_reported_result_count",
        "lda_fetched_filing_count",
        "lda_unfetched_api_result_count",
        "lda_exact_activity_match_rows",
        "lda_exact_activity_match_filings",
        "lda_exact_activity_match_clients",
        "lda_search_terms",
        "lda_search_years",
        "lda_api_statuses",
        "lda_search_disposition",
        "campaign_external_scope_status",
        "campaign_external_next_step",
        "combined_external_review_status",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    if bill_finance_lobbying_external_search_review and (
        missing_columns := required_external_search_review_columns
        - set(bill_finance_lobbying_external_search_review[0])
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: missing columns "
            f"{sorted(missing_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW_MD}: missing markdown report")
    else:
        external_review_md = BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW_MD.read_text()
        for phrase in (
            "Rows with exact external LDA current-bill activity-text mentions: 2",
            "Exact external LDA activity-text mention rows: 55",
            "Rows with complete external LDA search and no exact current-bill activity-text mention: 8",
            "Rows still requiring campaign-finance candidate/committee/outside-spending target-scope review: 4",
            "not bill IDs or bill-specific campaign-finance influence",
        ):
            if phrase not in external_review_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    required_campaign_target_scope_review_columns = {
        "target_scope_review_rank",
        "external_review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "introduced_date",
        "enacted_date",
        "campaign_scope_context_rows",
        "campaign_scope_transaction_attachments",
        "campaign_scope_unique_recipients",
        "campaign_scope_recipients",
        "candidate_ids",
        "candidate_names",
        "candidate_offices",
        "candidate_states",
        "candidate_districts",
        "member_bioguide_ids",
        "member_context_statuses",
        "district_context_statuses",
        "district_ids",
        "principal_campaign_committee_ids",
        "linked_committee_ids",
        "source_schedules",
        "unique_raw_transaction_rows",
        "transaction_source_ids",
        "transaction_dates",
        "transaction_labels",
        "receipt_rows",
        "receipt_amount",
        "independent_expenditure_rows",
        "independent_expenditure_amount",
        "issue_context_statuses",
        "mapped_topics",
        "sponsor_context_bill_ids",
        "sponsor_context_bill_congresses",
        "sponsor_context_policy_areas",
        "sponsor_context_enacted_bill_count",
        "current_bill_exact_match_status",
        "same_congress_context_status",
        "reviewed_bill_sponsor_candidate_overlap_status",
        "public_fec_target_scope_status",
        "outside_spending_target_status",
        "committee_scope_status",
        "bill_identifier_status",
        "outcome_link_status",
        "target_scope_disposition",
        "next_review_action",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "source_url",
        "claim_boundary",
    }
    missing_campaign_target_scope_review_columns = (
        required_campaign_target_scope_review_columns
        - set(bill_finance_lobbying_campaign_finance_target_scope_review[0])
    )
    if missing_campaign_target_scope_review_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: missing columns "
            f"{sorted(missing_campaign_target_scope_review_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW_MD.exists():
        failures.append(
            f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW_MD}: missing markdown report"
        )
    else:
        target_scope_md = BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW_MD.read_text()
        for phrase in (
            "Queued campaign-finance public-law rows reviewed: 4",
            "Candidate/recipient context attachments reviewed: 5",
            "Campaign-finance transaction attachments represented: 5",
            "Unique public FEC candidate recipients represented: 2",
            "Unique raw OpenFEC transactions represented: 2",
            "Rows with independent-expenditure candidate target fields only: 4",
            "Rows with current-bill IDs in public FEC/OpenFEC scope: 0",
            "Rows with reviewed bill sponsor/candidate overlap: 0",
            "Rows with committee-of-jurisdiction or committee-action evidence: 0",
            "Rows with legislative-outcome or influence evidence: 0",
            "Claim boundary",
        ):
            if phrase not in target_scope_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    campaign_target_pending_external_rows = [
        row for row in bill_finance_lobbying_external_search_review
        if row.get("campaign_external_scope_status", "").strip()
        == "fec_public_records_need_candidate_committee_or_outside_spending_target_join"
    ]
    target_scope_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_campaign_finance_target_scope_review
        if row.get("bill_id", "").strip()
    }
    if len(target_scope_by_bill) != len(bill_finance_lobbying_campaign_finance_target_scope_review):
        failures.append(f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: duplicate bill_id rows")
    expected_target_scope_bills = {
        row.get("bill_id", "").strip()
        for row in campaign_target_pending_external_rows
        if row.get("bill_id", "").strip()
    }
    if set(target_scope_by_bill) != expected_target_scope_bills:
        failures.append(
            "campaign-finance target-scope review/external-search bill mismatch: "
            f"missing from target review={sorted(expected_target_scope_bills - set(target_scope_by_bill))}, "
            f"extra={sorted(set(target_scope_by_bill) - expected_target_scope_bills)}"
        )
    campaign_sponsor_context_by_policy: dict[str, list[dict[str, str]]] = defaultdict(list)
    for sponsor_row in campaign_finance_sponsor_bill_context:
        for policy_area in split_semicolon_values(sponsor_row, "matched_policy_areas"):
            campaign_sponsor_context_by_policy[policy_area].append(sponsor_row)
    target_scope_ranks: list[int] = []
    target_scope_context_attachments = 0
    target_scope_transaction_attachments = 0
    target_scope_unique_recipients: set[str] = set()
    target_scope_unique_transactions: set[str] = set()
    target_scope_candidate_target_rows = 0
    target_scope_no_bill_id_rows = 0
    target_scope_no_sponsor_overlap_rows = 0
    target_scope_no_committee_action_rows = 0
    target_scope_no_outcome_rows = 0
    for bill_id, target_row in target_scope_by_bill.items():
        local_row = local_review_by_bill.get(bill_id, {})
        external_row = next(
            (row for row in campaign_target_pending_external_rows if row.get("bill_id", "").strip() == bill_id),
            {},
        )
        rank = parse_int(target_row.get("target_scope_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: invalid rank"
            )
        else:
            target_scope_ranks.append(rank)
        if target_row.get("external_review_rank", "").strip() != external_row.get("review_rank", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: external rank mismatch"
            )
        for field in (
            "public_law_number",
            "policy_area",
            "sponsor_bioguide_id",
            "sponsor_party",
            "sponsor_state",
            "introduced_date",
            "enacted_date",
        ):
            if target_row.get(field, "").strip() != local_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                    f"{field} does not match local review"
                )
        context_rows = campaign_sponsor_context_by_policy.get(target_row.get("policy_area", "").strip(), [])
        context_recipients = {
            context_row.get("recipient", "").strip()
            for context_row in context_rows
            if context_row.get("recipient", "").strip()
        }
        context_bill_ids = {
            bill
            for context_row in context_rows
            for bill in split_semicolon_values(context_row, "matched_bill_ids")
        }
        expected_local_bill_ids = split_semicolon_values(local_row, "campaign_finance_context_bill_ids")
        expected_context_count = len(context_rows)
        expected_transaction_attachments = sum(
            parse_int(context_row.get("member_context_transaction_rows", "")) or 0
            for context_row in context_rows
        )
        if parse_int(target_row.get("campaign_scope_context_rows", "")) != expected_context_count:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "campaign context row count mismatch"
            )
        if parse_int(target_row.get("campaign_scope_transaction_attachments", "")) != expected_transaction_attachments:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "transaction attachment count mismatch"
            )
        if parse_int(target_row.get("campaign_scope_unique_recipients", "")) != len(context_recipients):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "unique recipient count mismatch"
            )
        if split_semicolon_values(target_row, "campaign_scope_recipients") != context_recipients:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "recipient set mismatch"
            )
        if split_semicolon_values(target_row, "sponsor_context_bill_ids") != context_bill_ids:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "sponsor context bill set mismatch"
            )
        if context_bill_ids != expected_local_bill_ids:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "sponsor context bill set does not match local review"
            )
        if target_row.get("current_bill_exact_match_status", "") != "reviewed_no_current_bill_id_in_campaign_finance_context":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid current-bill exact-match status"
            )
        if target_row.get("same_congress_context_status", "") != "no_same_congress_sponsored_bill_context":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "same-congress context should remain absent"
            )
        if (
            target_row.get("reviewed_bill_sponsor_candidate_overlap_status", "")
            != "no_reviewed_bill_sponsor_candidate_overlap"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "sponsor/candidate overlap should remain absent"
            )
        if (
            target_row.get("public_fec_target_scope_status", "")
            != "reviewed_public_fec_openfec_candidate_target_fields_only"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid public FEC target-scope status"
            )
        if (
            target_row.get("outside_spending_target_status", "")
            != "reviewed_independent_expenditure_candidate_target_only"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid outside-spending target status"
            )
        if (
            target_row.get("committee_scope_status", "")
            != "reviewed_candidate_committee_metadata_no_committee_of_jurisdiction_or_action"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid committee scope status"
            )
        if (
            target_row.get("bill_identifier_status", "")
            != "no_bill_id_field_or_current_bill_match_in_public_fec_openfec_scope"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid bill-identifier status"
            )
        if target_row.get("outcome_link_status", "") != "no_legislative_outcome_or_influence_evidence":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid outcome-link status"
            )
        if (
            target_row.get("target_scope_disposition", "")
            != "reviewed_public_fec_openfec_scope_no_bill_specific_campaign_finance_link"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                "invalid target-scope disposition"
            )
        for required_gap in (
            "external_campaign_target_source_document",
            "bill_id_in_public_fec_openfec_record",
            "reviewed_outside_spending_target_beyond_candidate_id",
            "reviewed_bill_sponsor_candidate_overlap",
            "committee_of_jurisdiction",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "private_contributor_disclosure",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if required_gap not in target_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = target_row.get("claim_boundary", "")
        for phrase in (
            "Public FEC/OpenFEC target-scope review only",
            "does not expose bill IDs",
            "campaign spending for or against a bill",
            "committee-action influence",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
        target_scope_context_attachments += parse_int(target_row.get("campaign_scope_context_rows", "")) or 0
        target_scope_transaction_attachments += (
            parse_int(target_row.get("campaign_scope_transaction_attachments", "")) or 0
        )
        target_scope_unique_recipients.update(split_semicolon_values(target_row, "campaign_scope_recipients"))
        target_scope_unique_transactions.update(split_semicolon_values(target_row, "transaction_source_ids"))
        if target_row.get("outside_spending_target_status") == "reviewed_independent_expenditure_candidate_target_only":
            target_scope_candidate_target_rows += 1
        if (
            target_row.get("bill_identifier_status")
            == "no_bill_id_field_or_current_bill_match_in_public_fec_openfec_scope"
        ):
            target_scope_no_bill_id_rows += 1
        if (
            target_row.get("reviewed_bill_sponsor_candidate_overlap_status")
            == "no_reviewed_bill_sponsor_candidate_overlap"
        ):
            target_scope_no_sponsor_overlap_rows += 1
        if (
            target_row.get("committee_scope_status")
            == "reviewed_candidate_committee_metadata_no_committee_of_jurisdiction_or_action"
        ):
            target_scope_no_committee_action_rows += 1
        if target_row.get("outcome_link_status") == "no_legislative_outcome_or_influence_evidence":
            target_scope_no_outcome_rows += 1
    if sorted(target_scope_ranks) != list(
        range(1, len(bill_finance_lobbying_campaign_finance_target_scope_review) + 1)
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: review ranks must be contiguous"
        )
    if len(bill_finance_lobbying_campaign_finance_target_scope_review) != 4:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: expected 4 rows"
        )
    expected_target_counts = (
        target_scope_context_attachments,
        target_scope_transaction_attachments,
        len(target_scope_unique_recipients),
        len(target_scope_unique_transactions),
        target_scope_candidate_target_rows,
        len(bill_finance_lobbying_campaign_finance_target_scope_review) - target_scope_no_bill_id_rows,
        len(bill_finance_lobbying_campaign_finance_target_scope_review) - target_scope_no_sponsor_overlap_rows,
        len(bill_finance_lobbying_campaign_finance_target_scope_review) - target_scope_no_committee_action_rows,
        len(bill_finance_lobbying_campaign_finance_target_scope_review) - target_scope_no_outcome_rows,
    )
    if expected_target_counts != (5, 5, 2, 2, 4, 0, 0, 0, 0):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_CAMPAIGN_FINANCE_TARGET_SCOPE_REVIEW}: "
            f"unexpected summary counts {expected_target_counts}"
        )
    external_searches_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in bill_finance_lobbying_external_lda_searches_raw:
        bill_id = row.get("bill_id", "")
        external_searches_by_bill[bill_id].append(row)
        if row.get("api_status", "") != "ok":
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: {bill_id}: non-ok API status")
        if parse_int(row.get("unfetched_api_result_count", "")) != 0:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: {bill_id}: unfetched API results remain"
            )
        boundary = row.get("claim_boundary", "")
        if "Official LDA external current-bill search only" not in boundary or "model validation" not in boundary:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: {bill_id}: weak claim boundary"
            )
    external_mentions_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in bill_finance_lobbying_external_lda_mentions_raw:
        bill_id = row.get("bill_id", "")
        external_mentions_by_bill[bill_id].append(row)
        if row.get("exact_current_bill_match", "") != "1":
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: {bill_id}: exact match flag must be 1")
        if "official_lda_filing_text_bill_identifier" not in row.get("evidence_layers", ""):
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: {bill_id}: missing LDA identifier layer")
        if "committee_action_influence" not in row.get("missing_links", ""):
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: {bill_id}: missing committee-action gap")
    external_review_by_bill = {
        row.get("bill_id", ""): row
        for row in bill_finance_lobbying_external_search_review
    }
    if set(external_review_by_bill) != set(local_review_by_bill):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: bill IDs must match local-context review"
        )
    if set(external_searches_by_bill) != set(local_review_by_bill):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: bill IDs must match local-context review"
        )
    if len({row.get("bill_id") for row in bill_finance_lobbying_external_lda_mentions_raw}) != 2:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: expected exact mentions for 2 queued bills")
    if len(bill_finance_lobbying_external_lda_mentions_raw) != 55:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTIONS_RAW}: expected 55 exact mention rows")
    campaign_external_pending_count = 0
    external_exact_bill_count = 0
    external_no_exact_complete_count = 0
    for bill_id, local_row in local_review_by_bill.items():
        report_row = external_review_by_bill.get(bill_id)
        if not report_row:
            continue
        search_rows = external_searches_by_bill.get(bill_id, [])
        mention_rows = external_mentions_by_bill.get(bill_id, [])
        year_start = parse_int(local_row.get("introduced_date", "")[:4])
        year_end = parse_int(local_row.get("enacted_date", "")[:4])
        expected_search_rows = (year_end - year_start + 1) * 2 if year_start and year_end else 0
        if len(search_rows) != expected_search_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: {bill_id}: "
                f"expected {expected_search_rows} compact/dotted term-year rows, found {len(search_rows)}"
            )
        if {"compact", "dotted"} - {row.get("term_variant", "") for row in search_rows}:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_SEARCHES_RAW}: {bill_id}: missing term variant")
        expected_report_values = {
            "review_rank": local_row.get("review_rank", ""),
            "public_law_number": local_row.get("public_law_number", ""),
            "policy_area": local_row.get("policy_area", ""),
            "local_next_source_expansion": local_row.get("manual_next_source_expansion", ""),
            "lda_search_rows": str(len(search_rows)),
            "lda_api_reported_result_count": str(sum(parse_int(row.get("api_reported_result_count", "")) for row in search_rows)),
            "lda_fetched_filing_count": str(sum(parse_int(row.get("fetched_filing_count", "")) for row in search_rows)),
            "lda_unfetched_api_result_count": str(sum(parse_int(row.get("unfetched_api_result_count", "")) for row in search_rows)),
            "lda_exact_activity_match_rows": str(len(mention_rows)),
            "lda_exact_activity_match_filings": str(len({row.get("filing_uuid", "") for row in mention_rows if row.get("filing_uuid")})),
            "lda_exact_activity_match_clients": str(len({row.get("client_name", "") for row in mention_rows if row.get("client_name")})),
        }
        for field, expected_value in expected_report_values.items():
            if report_row.get(field, "") != expected_value:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: "
                    f"{field} mismatch; expected {expected_value!r}, found {report_row.get(field, '')!r}"
                )
        if mention_rows:
            expected_lda_status = "official_lda_external_current_bill_activity_text_match"
            external_exact_bill_count += 1
        else:
            expected_lda_status = "official_lda_external_search_no_exact_current_bill_activity_text_match"
            external_no_exact_complete_count += 1
        if report_row.get("lda_search_disposition", "") != expected_lda_status:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: LDA disposition mismatch")
        campaign_pending = "campaign_finance" in local_row.get("manual_next_source_expansion", "")
        if campaign_pending:
            campaign_external_pending_count += 1
            expected_campaign_status = "fec_public_records_need_candidate_committee_or_outside_spending_target_join"
        else:
            expected_campaign_status = "campaign_finance_external_search_not_in_current_row_scope"
        if report_row.get("campaign_external_scope_status", "") != expected_campaign_status:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: campaign scope status mismatch")
        layers = split_semicolon_values(report_row, "evidence_layers")
        required_layers = {
            "bill_finance_lobbying_local_context_review",
            "official_lda_external_current_bill_search",
            "fec_openfec_source_scope_triage",
        }
        if mention_rows:
            required_layers.add("official_lda_filing_text_bill_identifier")
        if not required_layers <= layers:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: "
                f"missing evidence layers {sorted(required_layers - layers)}"
            )
        for required_gap in (
            "source_reviewed_support_or_opposition_disposition",
            "lobbying_contact_or_target_source",
            "committee_action_influence",
            "candidate_or_committee_campaign_finance_target_join",
            "reviewed_outside_spending_target",
            "legislative_outcome_causality",
            "model_validation",
        ):
            if required_gap not in report_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: missing gap {required_gap!r}"
                )
        boundary = report_row.get("claim_boundary", "")
        for phrase in (
            "External source-search review only",
            "FEC source-scope triage",
            "not bill IDs or bill-specific campaign-finance influence",
            "committee-action influence",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if external_exact_bill_count != 2:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: expected 2 rows with exact LDA mentions")
    if external_no_exact_complete_count != 8:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: expected 8 complete no-exact LDA rows")
    if campaign_external_pending_count != 4:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_SEARCH_REVIEW}: expected 4 campaign external-scope rows")

    required_external_lda_mention_review_columns = {
        "packet_review_rank",
        "packet_id",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "client_name",
        "registrant_name",
        "filing_uuid",
        "filing_year",
        "filing_period",
        "rows_represented",
        "activity_issue_count",
        "activity_issues",
        "matched_bill_refs",
        "direction_status",
        "activity_disposition_status",
        "activity_disposition_basis",
        "target_status",
        "target_type",
        "target_text",
        "government_entity_count",
        "government_entities",
        "committee_action_status",
        "roll_call_status",
        "outcome_link_status",
        "activity_description_samples",
        "source_urls",
        "filing_document_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    if bill_finance_lobbying_external_lda_mention_review and (
        missing_columns := required_external_lda_mention_review_columns
        - set(bill_finance_lobbying_external_lda_mention_review[0])
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: missing columns "
            f"{sorted(missing_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW_MD}: missing markdown report")
    else:
        mention_review_md = BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW_MD.read_text()
        for phrase in (
            "External LDA filing packets reviewed: 19",
            "Exact activity-text mention rows represented: 55",
            "Packets with explicit support/opposition text: 0",
            "reviewed_current_bill_issue_reference_without_direction: 16",
            "reviewed_current_bill_issue_advocacy_without_direction: 3",
            "Packets with named sponsor/member/committee target beyond generic entity text: 0",
            "Packets with committee-action influence evidence: 0",
            "Packets with roll-call influence evidence: 0",
            "Packets with legislative-outcome causality evidence: 0",
        ):
            if phrase not in mention_review_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    raw_mentions_by_packet: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in bill_finance_lobbying_external_lda_mentions_raw:
        raw_mentions_by_packet[(
            row.get("bill_id", ""),
            row.get("filing_uuid", ""),
            row.get("client_name", ""),
            row.get("registrant_name", ""),
        )].append(row)
    mention_review_by_packet: dict[tuple[str, str, str, str], dict[str, str]] = {}
    mention_review_ranks: list[int] = []
    represented_raw_rows = 0
    for row in bill_finance_lobbying_external_lda_mention_review:
        key = (
            row.get("bill_id", ""),
            row.get("filing_uuid", ""),
            row.get("client_name", ""),
            row.get("registrant_name", ""),
        )
        if key in mention_review_by_packet:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: duplicate packet {key}")
        mention_review_by_packet[key] = row
        rank = parse_int(row.get("packet_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: invalid packet rank for {key}")
        else:
            mention_review_ranks.append(rank)
        raw_packet_rows = raw_mentions_by_packet.get(key, [])
        represented_raw_rows += parse_int(row.get("rows_represented", "")) or 0
        if not raw_packet_rows:
            failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: no raw mention rows for {key}")
            continue
        if (parse_int(row.get("rows_represented", "")) or 0) != len(raw_packet_rows):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: rows_represented mismatch"
            )
        expected_activity_issues = {
            raw_row.get("activity_issue", "")
            for raw_row in raw_packet_rows
            if raw_row.get("activity_issue", "")
        }
        if split_semicolon_values(row, "activity_issues") != expected_activity_issues:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: activity issue mismatch"
            )
        if row.get("direction_status", "") != "no_explicit_support_or_opposition":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: unexpected explicit direction status"
            )
        if row.get("target_status", "") != "reviewed_generic_chamber_or_agency_text_reference":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: target status should remain generic"
            )
        if row.get("committee_action_status", "") != "no_committee_action_influence_evidence":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: committee-action status is too broad"
            )
        if row.get("roll_call_status", "") != "no_roll_call_influence_evidence":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: roll-call status is too broad"
            )
        if row.get("outcome_link_status", "") != "no_outcome_influence_evidence":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: outcome status is too broad"
            )
        layers = split_semicolon_values(row, "evidence_layers")
        required_layers = {
            "bill_finance_lobbying_external_search_review",
            "official_lda_external_current_bill_search",
            "official_lda_filing_text_bill_identifier",
            "external_lda_activity_text_source_review",
        }
        if not required_layers <= layers:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: "
                f"missing evidence layers {sorted(required_layers - layers)}"
            )
        for required_gap in (
            "lobbying_contact_confirmation",
            "explicit_support_or_opposition_if_not_stated",
            "sponsor_or_member_target_beyond_activity_text_reference",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "candidate_or_committee_campaign_finance_target_join",
            "reviewed_outside_spending_target",
            "causal_capture_validation",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = row.get("claim_boundary", "")
        for phrase in (
            "External LDA current-bill mention source review only",
            "support or opposition unless explicitly stated",
            "committee-action influence",
            "roll-call influence",
            "model validation",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: {key}: "
                    f"claim boundary missing {phrase!r}"
                )
    if set(mention_review_by_packet) != set(raw_mentions_by_packet):
        failures.append(
            "external LDA mention review/raw packet mismatch: "
            f"missing from review={sorted(set(raw_mentions_by_packet) - set(mention_review_by_packet))[:10]}, "
            f"extra={sorted(set(mention_review_by_packet) - set(raw_mentions_by_packet))[:10]}"
        )
    if sorted(mention_review_ranks) != list(range(1, len(bill_finance_lobbying_external_lda_mention_review) + 1)):
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: packet ranks must be contiguous")
    mention_dispositions = Counter(
        row.get("activity_disposition_status", "")
        for row in bill_finance_lobbying_external_lda_mention_review
    )
    if len(bill_finance_lobbying_external_lda_mention_review) != 19:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: expected 19 filing packets")
    if represented_raw_rows != len(bill_finance_lobbying_external_lda_mentions_raw):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: represented raw row count mismatch"
        )
    if mention_dispositions.get("reviewed_current_bill_issue_reference_without_direction", 0) != 16:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: expected 16 reference-only packets")
    if mention_dispositions.get("reviewed_current_bill_issue_advocacy_without_direction", 0) != 3:
        failures.append(f"{BILL_FINANCE_LOBBYING_EXTERNAL_LDA_MENTION_REVIEW}: expected 3 advocacy-without-direction packets")

    required_committee_action_context_columns = {
        "context_rank",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "introduced_date",
        "enacted_date",
        "actions_count",
        "committee_reported",
        "floor_considered",
        "bill_action_context_status",
        "committee_name_context_status",
        "floor_action_context_status",
        "local_review_status",
        "external_lda_search_disposition",
        "external_lda_exact_activity_match_rows",
        "external_lda_mention_packets",
        "external_lda_mention_rows_represented",
        "external_lda_committee_action_statuses",
        "campaign_target_scope_status",
        "campaign_target_scope_disposition",
        "committee_action_influence_status",
        "roll_call_influence_status",
        "legislative_outcome_causality_status",
        "next_review_action",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "source_url",
        "claim_boundary",
    }
    missing_committee_action_context_columns = (
        required_committee_action_context_columns
        - set(bill_finance_lobbying_committee_action_context[0])
    )
    if missing_committee_action_context_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: missing columns "
            f"{sorted(missing_committee_action_context_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT_MD}: missing markdown report")
    else:
        committee_action_context_md = BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT_MD.read_text()
        for phrase in (
            "Queued public-law rows reviewed: 10",
            "Rows with cached committee-reported flag: 8",
            "Rows with cached floor-considered flag: 10",
            "Rows with committee-of-jurisdiction names in current cache: 0",
            "Rows with finance/lobbying committee-action influence evidence: 0",
            "Rows with finance/lobbying roll-call influence evidence: 0",
            "Rows with finance/lobbying legislative-outcome causality evidence: 0",
            "not influence evidence",
            "Claim boundary",
        ):
            if phrase not in committee_action_context_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    committee_context_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_committee_action_context
        if row.get("bill_id", "").strip()
    }
    if len(committee_context_by_bill) != len(bill_finance_lobbying_committee_action_context):
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: duplicate bill_id rows")
    if set(committee_context_by_bill) != set(finance_lobbying_by_bill):
        failures.append(
            "bill-finance/lobbying committee-action context/queue bill mismatch: "
            f"missing from context={sorted(set(finance_lobbying_by_bill) - set(committee_context_by_bill))}, "
            f"extra={sorted(set(committee_context_by_bill) - set(finance_lobbying_by_bill))}"
        )
    committee_action_law_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in law_bill_rows
        if row.get("bill_id", "").strip()
    }
    committee_mention_review_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for mention_review_row in bill_finance_lobbying_external_lda_mention_review:
        bill_id = mention_review_row.get("bill_id", "").strip()
        if bill_id:
            committee_mention_review_by_bill[bill_id].append(mention_review_row)
    committee_context_ranks: list[int] = []
    committee_context_reported_rows = 0
    committee_context_floor_rows = 0
    committee_context_name_rows = 0
    committee_context_action_influence_rows = 0
    committee_context_roll_call_rows = 0
    committee_context_outcome_rows = 0
    for bill_id, context_row in committee_context_by_bill.items():
        queue_row = finance_lobbying_by_bill.get(bill_id, {})
        local_row = local_review_by_bill.get(bill_id, {})
        external_row = external_review_by_bill.get(bill_id, {})
        law_row = committee_action_law_by_bill.get(bill_id, {})
        target_row = target_scope_by_bill.get(bill_id, {})
        rank = parse_int(context_row.get("context_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: invalid context_rank")
        else:
            committee_context_ranks.append(rank)
        if context_row.get("context_rank", "").strip() != context_row.get("review_rank", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: context_rank must match review_rank"
            )
        if context_row.get("review_rank", "").strip() != queue_row.get("review_rank", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: review_rank does not match queue"
            )
        for field in (
            "public_law_number",
            "policy_area",
            "sponsor_bioguide_id",
            "sponsor_party",
            "sponsor_state",
            "introduced_date",
            "enacted_date",
        ):
            if context_row.get(field, "").strip() != queue_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                    f"{field} does not match queue"
                )
        for field in ("public_law_number", "policy_area", "introduced_date", "enacted_date"):
            if context_row.get(field, "").strip() != law_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                    f"{field} does not match law revision bill metadata"
                )
        if context_row.get("actions_count", "").strip() != law_row.get("actions_count", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: actions_count mismatch"
            )
        expected_committee_reported = yes_no((parse_int(law_row.get("committee_reported", "")) or 0) > 0)
        expected_floor_considered = yes_no((parse_int(law_row.get("floor_considered", "")) or 0) > 0)
        if context_row.get("committee_reported", "") != expected_committee_reported:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: committee_reported mismatch"
            )
        if context_row.get("floor_considered", "") != expected_floor_considered:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: floor_considered mismatch"
            )
        if context_row.get("local_review_status", "") != local_row.get("manual_bill_specific_gate_status", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: local review status mismatch"
            )
        if context_row.get("local_review_status", "") != (
            "reviewed_local_context_no_current_bill_specific_finance_or_lobbying_match"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: local review status must stay no-current-match"
            )
        if context_row.get("external_lda_search_disposition", "") != external_row.get("lda_search_disposition", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: external LDA disposition mismatch"
            )
        raw_mention_rows = external_mentions_by_bill.get(bill_id, [])
        mention_review_rows = committee_mention_review_by_bill.get(bill_id, [])
        if parse_int(context_row.get("external_lda_exact_activity_match_rows", "")) != len(raw_mention_rows):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: external LDA exact-row count mismatch"
            )
        if parse_int(context_row.get("external_lda_mention_packets", "")) != len(mention_review_rows):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: external LDA packet count mismatch"
            )
        represented_mentions = sum(parse_int(row.get("rows_represented", "")) or 0 for row in mention_review_rows)
        if parse_int(context_row.get("external_lda_mention_rows_represented", "")) != represented_mentions:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: represented mention count mismatch"
            )
        expected_committee_action_statuses = {
            row.get("committee_action_status", "").strip()
            for row in mention_review_rows
            if row.get("committee_action_status", "").strip()
        } or {"not_in_external_lda_mention_review"}
        if split_semicolon_values(context_row, "external_lda_committee_action_statuses") != expected_committee_action_statuses:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                "external LDA committee-action status mismatch"
            )
        if target_row:
            expected_campaign_status = target_row.get("public_fec_target_scope_status", "")
            expected_campaign_disposition = target_row.get("target_scope_disposition", "")
        else:
            expected_campaign_status = "not_in_campaign_finance_target_scope_review"
            expected_campaign_disposition = "not_in_campaign_finance_target_scope_review"
        if context_row.get("campaign_target_scope_status", "") != expected_campaign_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: campaign target status mismatch"
            )
        if context_row.get("campaign_target_scope_disposition", "") != expected_campaign_disposition:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: campaign target disposition mismatch"
            )
        if context_row.get("bill_action_context_status", "") not in {
            "public_bill_action_metadata_committee_reported_and_floor_considered",
            "public_bill_action_metadata_floor_considered_without_committee_reported_flag",
        }:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: invalid bill-action context status"
            )
        if context_row.get("floor_action_context_status", "") != "public_bill_action_metadata_floor_considered_flag_present":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: floor action flag should be present"
            )
        if (
            context_row.get("committee_name_context_status", "")
            != "no_committee_name_or_jurisdiction_source_in_current_cache"
        ):
            committee_context_name_rows += 1
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                "committee names are not supported by the current cache"
            )
        if (
            context_row.get("committee_action_influence_status", "")
            != "no_finance_or_lobbying_committee_action_influence_evidence"
        ):
            committee_context_action_influence_rows += 1
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                "committee-action influence status is too broad"
            )
        if (
            context_row.get("roll_call_influence_status", "")
            != "no_finance_or_lobbying_roll_call_influence_evidence"
        ):
            committee_context_roll_call_rows += 1
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                "roll-call influence status is too broad"
            )
        if context_row.get("legislative_outcome_causality_status", "") != (
            "enacted_public_law_metadata_only_no_finance_or_lobbying_outcome_causality"
        ):
            committee_context_outcome_rows += 1
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                "legislative-outcome causality status is too broad"
            )
        if context_row.get("committee_reported", "") == "yes":
            committee_context_reported_rows += 1
        if context_row.get("floor_considered", "") == "yes":
            committee_context_floor_rows += 1
        required_layers = {
            "bill_finance_lobbying_review_queue",
            "manual_bill_finance_lobbying_local_context_review",
            "bill_finance_lobbying_external_search_review",
            "law_revision_bill_action_metadata",
        }
        if raw_mention_rows:
            required_layers.add("external_lda_activity_text_mention_review")
        if target_row:
            required_layers.add("campaign_finance_target_scope_review")
        layers = split_semicolon_values(context_row, "evidence_layers")
        if not required_layers <= layers:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                f"missing evidence layers {sorted(required_layers - layers)}"
            )
        for required_gap in (
            "committee_of_jurisdiction",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "bill_specific_campaign_finance_influence",
            "bill_specific_lobbying_influence",
            "external_campaign_target_source_document",
            "lobbying_contact_or_target_source",
            "reviewed_outside_spending_target_beyond_candidate_id",
            "public_benefit_or_welfare_validation",
            "causal_capture_validation",
            "model_validation",
        ):
            if required_gap not in context_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        if "congress.gov" not in context_row.get("source_url", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: missing Congress.gov source_url"
            )
        if context_row.get("source_url", "") not in context_row.get("source_urls", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: source_urls missing primary source"
            )
        next_action = context_row.get("next_review_action", "")
        for phrase in ("committee-of-jurisdiction", "committee action records", "roll-call context"):
            if phrase not in next_action:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                    f"next action missing {phrase!r}"
                )
        boundary = context_row.get("claim_boundary", "")
        for phrase in (
            "committee/action context only",
            "not evidence",
            "committee-of-jurisdiction names",
            "model result",
        ):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(committee_context_ranks) != list(
        range(1, len(bill_finance_lobbying_committee_action_context) + 1)
    ):
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: context ranks must be contiguous")
    committee_context_counts = (
        len(bill_finance_lobbying_committee_action_context),
        committee_context_reported_rows,
        committee_context_floor_rows,
        committee_context_name_rows,
        committee_context_action_influence_rows,
        committee_context_roll_call_rows,
        committee_context_outcome_rows,
    )
    if committee_context_counts != (10, 8, 10, 0, 0, 0, 0):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_CONTEXT}: "
            f"unexpected summary counts {committee_context_counts}"
        )

    required_committee_action_source_columns = {
        "source_review_rank",
        "context_rank",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "govinfo_billstatus_status",
        "govinfo_url",
        "introduced_date",
        "latest_action_date",
        "latest_action_text",
        "actions_count",
        "committee_source_status",
        "committee_count",
        "committee_names",
        "committee_activity_count",
        "committee_activity_summary",
        "committee_report_count",
        "committee_report_citations",
        "committee_action_record_status",
        "committee_action_count",
        "committee_action_dates",
        "committee_action_snippets",
        "floor_action_record_status",
        "floor_action_count",
        "floor_action_dates",
        "floor_action_snippets",
        "roll_call_reference_status",
        "roll_call_reference_count",
        "roll_call_references",
        "legislative_outcome_source_status",
        "public_law_numbers",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "external_lda_mention_packets",
        "campaign_target_scope_status",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_committee_action_source_columns = (
        required_committee_action_source_columns
        - set(bill_finance_lobbying_committee_action_source_review[0])
    )
    if missing_committee_action_source_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: missing columns "
            f"{sorted(missing_committee_action_source_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW_MD}: missing markdown report")
    else:
        committee_action_source_md = BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW_MD.read_text()
        for phrase in (
            "Queued public-law rows: 10",
            "Rows with govinfo BILLSTATUS fetched: 10",
            "Rows with official committee names: 9",
            "Rows source-reviewed without direct committee names: 1",
            "Unique committee/subcommittee names represented: 12",
            "Rows with official committee action records: 9",
            "Rows source-reviewed without direct committee action records: 1",
            "Rows with official floor action records: 10",
            "Rows with BILLSTATUS roll-call references: 8",
            "Rows with official public-law outcome metadata: 10",
            "not finance/lobbying influence evidence",
            "Claim boundary",
        ):
            if phrase not in committee_action_source_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    source_review_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_committee_action_source_review
        if row.get("bill_id", "").strip()
    }
    if len(source_review_by_bill) != len(bill_finance_lobbying_committee_action_source_review):
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: duplicate bill_id rows")
    if set(source_review_by_bill) != set(committee_context_by_bill):
        failures.append(
            "bill-finance/lobbying committee-action source/context bill mismatch: "
            f"missing from source={sorted(set(committee_context_by_bill) - set(source_review_by_bill))}, "
            f"extra={sorted(set(source_review_by_bill) - set(committee_context_by_bill))}"
        )
    source_review_ranks: list[int] = []
    source_review_fetched_rows = 0
    source_review_committee_rows = 0
    source_review_committee_action_rows = 0
    source_review_floor_action_rows = 0
    source_review_roll_call_rows = 0
    source_review_outcome_rows = 0
    unique_source_committees: set[str] = set()
    for bill_id, source_row in source_review_by_bill.items():
        context_row = committee_context_by_bill.get(bill_id, {})
        rank = parse_int(source_row.get("source_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: invalid rank")
        else:
            source_review_ranks.append(rank)
        for field in ("context_rank", "review_rank", "bill_id", "public_law_number", "policy_area"):
            if source_row.get(field, "").strip() != context_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    f"{field} does not match committee/action context"
                )
        if "govinfo.gov/bulkdata/BILLSTATUS/" not in source_row.get("govinfo_url", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: missing govinfo URL"
            )
        if source_row.get("govinfo_billstatus_status", "") != "official_govinfo_billstatus_fetched":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: source fetch status mismatch"
            )
        else:
            source_review_fetched_rows += 1
        committee_count = parse_int(source_row.get("committee_count", "")) or 0
        if committee_count > 0:
            source_review_committee_rows += 1
            if source_row.get("committee_source_status", "") != "official_govinfo_committee_names_present":
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    "committee status should report official names"
                )
            for committee_name in source_row.get("committee_names", "").split(";"):
                clean_name = " ".join(committee_name.split())
                if clean_name:
                    unique_source_committees.add(clean_name)
        elif source_row.get("committee_source_status", "") != (
            "official_govinfo_billstatus_reviewed_without_direct_committee_names"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                "missing committee status mismatch"
            )
        if source_row.get("committee_action_record_status", "") == (
            "official_govinfo_committee_action_records_present"
        ):
            source_review_committee_action_rows += 1
        elif source_row.get("committee_action_record_status", "") != (
            "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                "committee action source status mismatch"
            )
        if source_row.get("floor_action_record_status", "") != "official_govinfo_floor_action_records_present":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                "floor action source status mismatch"
            )
        else:
            source_review_floor_action_rows += 1
        if parse_int(source_row.get("roll_call_reference_count", "")) > 0:
            source_review_roll_call_rows += 1
            if source_row.get("roll_call_reference_status", "") != "official_billstatus_roll_call_references_present":
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    "roll-call reference status mismatch"
                )
        elif source_row.get("roll_call_reference_status", "") != "official_billstatus_without_roll_call_references":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                "missing roll-call reference status mismatch"
            )
        if source_row.get("legislative_outcome_source_status", "") != (
            "official_govinfo_public_law_outcome_metadata_present_no_finance_lobbying_causality"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                "outcome metadata status must reject causality"
            )
        else:
            source_review_outcome_rows += 1
        for required_layer in (
            "bill_finance_lobbying_committee_action_context",
            "official_govinfo_billstatus_committee_source",
            "official_govinfo_billstatus_action_source",
        ):
            if required_layer not in split_semicolon_values(source_row, "evidence_layers"):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer!r}"
                )
        for required_gap in (
            "lobbying_contact_or_target_source",
            "external_campaign_target_source_document",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "model_validation",
        ):
            if required_gap not in source_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = source_row.get("claim_boundary", "")
        for phrase in ("committee/action source review only", "not lobbying contact", "model validation"):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(source_review_ranks) != list(
        range(1, len(bill_finance_lobbying_committee_action_source_review) + 1)
    ):
        failures.append(f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: ranks must be contiguous")
    source_review_counts = (
        len(bill_finance_lobbying_committee_action_source_review),
        source_review_fetched_rows,
        source_review_committee_rows,
        source_review_committee_action_rows,
        source_review_floor_action_rows,
        source_review_roll_call_rows,
        source_review_outcome_rows,
        len(unique_source_committees),
    )
    if source_review_counts != (10, 10, 9, 9, 10, 8, 10, 12):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW}: "
            f"unexpected summary counts {source_review_counts}"
        )

    required_roll_call_source_columns = {
        "roll_call_source_rank",
        "source_review_rank",
        "context_rank",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "roll_call_reference_status",
        "roll_call_reference_count",
        "roll_call_references",
        "floor_action_record_status",
        "floor_action_count",
        "roll_call_source_review_status",
        "chamber",
        "vote_year",
        "roll_call_number",
        "official_vote_source_url",
        "source_fetch_status",
        "official_congress",
        "official_session",
        "official_chamber",
        "official_legis_num",
        "official_vote_question",
        "official_vote_type",
        "official_vote_result",
        "official_action_date",
        "official_action_time",
        "official_vote_desc",
        "official_yea_total",
        "official_nay_total",
        "official_present_total",
        "official_not_voting_total",
        "official_party_totals",
        "member_vote_count",
        "source_bill_match_status",
        "floor_action_vote_mode_status",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_roll_call_source_columns = (
        required_roll_call_source_columns
        - set(bill_finance_lobbying_roll_call_source_review[0])
    )
    if missing_roll_call_source_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: missing columns "
            f"{sorted(missing_roll_call_source_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW_MD}: missing markdown report")
    else:
        roll_call_source_md = BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW_MD.read_text()
        for phrase in (
            "Source-review rows: 10",
            "Official House Clerk roll-call XML rows fetched: 8",
            "Fetched rows whose official legis-num matches bill_id: 8",
            "Floor-action rows reviewed without numbered roll-call references: 2",
            "Member vote rows represented: 3435",
            "not finance/lobbying roll-call influence evidence",
            "Claim boundary",
        ):
            if phrase not in roll_call_source_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    roll_call_source_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_roll_call_source_review
        if row.get("bill_id", "").strip()
    }
    if len(roll_call_source_by_bill) != len(bill_finance_lobbying_roll_call_source_review):
        failures.append(f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: duplicate bill_id rows")
    if set(roll_call_source_by_bill) != set(source_review_by_bill):
        failures.append(
            "bill-finance/lobbying roll-call/source-review bill mismatch: "
            f"missing from roll-call={sorted(set(source_review_by_bill) - set(roll_call_source_by_bill))}, "
            f"extra={sorted(set(roll_call_source_by_bill) - set(source_review_by_bill))}"
        )
    roll_call_source_ranks: list[int] = []
    roll_call_source_fetched_rows = 0
    roll_call_source_bill_match_rows = 0
    roll_call_source_no_numbered_rows = 0
    roll_call_source_member_vote_rows = 0
    for bill_id, roll_row in roll_call_source_by_bill.items():
        source_row = source_review_by_bill.get(bill_id, {})
        rank = parse_int(roll_row.get("roll_call_source_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: invalid rank")
        else:
            roll_call_source_ranks.append(rank)
        for field in ("source_review_rank", "context_rank", "review_rank", "bill_id", "public_law_number", "policy_area"):
            if roll_row.get(field, "").strip() != source_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    f"{field} does not match committee/action source review"
                )
        member_vote_count = parse_int(roll_row.get("member_vote_count", "")) or 0
        roll_call_source_member_vote_rows += member_vote_count
        if parse_int(source_row.get("roll_call_reference_count", "")) > 0:
            if roll_row.get("roll_call_source_review_status", "") != "official_house_clerk_roll_call_source_reviewed":
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "numbered roll-call row should be source-reviewed"
                )
            if roll_row.get("source_fetch_status", "") != "official_house_clerk_roll_call_xml_fetched":
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "House Clerk XML fetch status mismatch"
                )
            else:
                roll_call_source_fetched_rows += 1
            if roll_row.get("source_bill_match_status", "") != "official_vote_legis_num_matches_bill_id":
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "official legis-num should match bill_id"
                )
            else:
                roll_call_source_bill_match_rows += 1
            if not roll_row.get("official_vote_source_url", "").startswith("https://clerk.house.gov/evs/"):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "missing official House Clerk URL"
                )
            if member_vote_count <= 0:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "member vote count should be positive for numbered roll-call rows"
                )
        else:
            if roll_row.get("roll_call_source_review_status", "") != (
                "official_floor_action_reviewed_without_numbered_roll_call"
            ):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "non-numbered floor action status mismatch"
                )
            else:
                roll_call_source_no_numbered_rows += 1
            if member_vote_count != 0:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    "non-numbered floor action should not have member vote rows"
                )
        for required_layer in (
            "bill_finance_lobbying_committee_action_source_review",
        ):
            if required_layer not in split_semicolon_values(roll_row, "evidence_layers"):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer!r}"
                )
        for required_gap in (
            "member_level_vote_target_join_to_finance_lobbying_source",
            "roll_call_influence",
            "legislative_outcome_causality",
            "model_validation",
        ):
            if required_gap not in roll_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = roll_row.get("claim_boundary", "")
        for phrase in ("roll-call source review only", "not member-position influence", "model validation"):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(roll_call_source_ranks) != list(
        range(1, len(bill_finance_lobbying_roll_call_source_review) + 1)
    ):
        failures.append(f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: ranks must be contiguous")
    roll_call_source_counts = (
        len(bill_finance_lobbying_roll_call_source_review),
        roll_call_source_fetched_rows,
        roll_call_source_bill_match_rows,
        roll_call_source_no_numbered_rows,
        roll_call_source_member_vote_rows,
    )
    if roll_call_source_counts != (10, 8, 8, 2, 3435):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW}: "
            f"unexpected summary counts {roll_call_source_counts}"
        )

    required_member_vote_target_columns = {
        "member_vote_target_rank",
        "roll_call_source_rank",
        "source_review_rank",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "vote_year",
        "roll_call_number",
        "official_vote_source_url",
        "source_fetch_status",
        "official_congress",
        "official_chamber",
        "official_legis_num",
        "official_vote_result",
        "official_action_date",
        "member_vote_source_position",
        "voter_bioguide_id",
        "voter_name",
        "voter_party",
        "voter_state",
        "voter_vote",
        "same_bill_campaign_target_bioguide_ids",
        "same_bill_campaign_target_candidate_names",
        "same_bill_campaign_target_scope_status",
        "same_bill_campaign_target_match_status",
        "broad_campaign_member_context_status",
        "broad_campaign_candidate_ids",
        "broad_campaign_candidate_names",
        "broad_campaign_transaction_rows",
        "member_vote_target_scope_status",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "source_url",
        "claim_boundary",
    }
    missing_member_vote_target_columns = (
        required_member_vote_target_columns
        - set(bill_finance_lobbying_member_vote_target_review[0])
    )
    if missing_member_vote_target_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: missing columns "
            f"{sorted(missing_member_vote_target_columns)}"
        )
    raw_member_vote_keys = {
        (
            row.get("member_vote_target_rank", ""),
            row.get("bill_id", ""),
            row.get("voter_bioguide_id", ""),
            row.get("member_vote_source_position", ""),
        )
        for row in bill_finance_lobbying_member_vote_target_raw
    }
    report_member_vote_keys = {
        (
            row.get("member_vote_target_rank", ""),
            row.get("bill_id", ""),
            row.get("voter_bioguide_id", ""),
            row.get("member_vote_source_position", ""),
        )
        for row in bill_finance_lobbying_member_vote_target_review
    }
    if raw_member_vote_keys != report_member_vote_keys:
        failures.append(
            "bill-finance/lobbying member-vote target raw/report mismatch: "
            f"missing from report={sorted(raw_member_vote_keys - report_member_vote_keys)[:10]}, "
            f"extra={sorted(report_member_vote_keys - raw_member_vote_keys)[:10]}"
        )
    if not BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW_MD}: missing markdown report")
    else:
        member_vote_target_md = BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW_MD.read_text()
        for phrase in (
            "Member-vote rows reviewed: 3435",
            "Numbered roll calls reviewed: 8",
            "Floor-action rows without numbered roll calls excluded: 2",
            "Rows with same-bill reviewed campaign target Bioguide overlap: 0",
            "Rows with broad public FEC candidate/member-context overlap:",
            "not finance/lobbying roll-call influence evidence",
            "Claim boundary",
        ):
            if phrase not in member_vote_target_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    member_vote_target_ranks: list[int] = []
    member_vote_rows_by_bill: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    member_vote_rows_by_roll_call: defaultdict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    member_vote_same_bill_overlap_rows = 0
    member_vote_broad_context_rows = 0
    for row in bill_finance_lobbying_member_vote_target_review:
        bill_id = row.get("bill_id", "").strip()
        rank = parse_int(row.get("member_vote_target_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: invalid rank")
        else:
            member_vote_target_ranks.append(rank)
        member_vote_rows_by_bill[bill_id].append(row)
        member_vote_rows_by_roll_call[
            (bill_id, row.get("vote_year", "").strip(), row.get("roll_call_number", "").strip())
        ].append(row)
        roll_row = roll_call_source_by_bill.get(bill_id, {})
        for field in (
            "roll_call_source_rank",
            "source_review_rank",
            "review_rank",
            "bill_id",
            "public_law_number",
            "policy_area",
            "vote_year",
            "roll_call_number",
            "official_vote_source_url",
            "source_fetch_status",
            "official_congress",
            "official_chamber",
            "official_legis_num",
            "official_vote_result",
            "official_action_date",
        ):
            if row.get(field, "").strip() != roll_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                    f"{field} does not match roll-call source review"
                )
        if roll_row.get("roll_call_source_review_status") != "official_house_clerk_roll_call_source_reviewed":
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "member rows should only exist for official House Clerk source-reviewed roll calls"
            )
        if not row.get("official_vote_source_url", "").startswith("https://clerk.house.gov/evs/"):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "missing official House Clerk member-vote URL"
            )
        if not row.get("voter_bioguide_id", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: missing voter Bioguide ID"
            )
        if not row.get("voter_vote", "").strip():
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: missing vote choice"
            )
        if (parse_int(row.get("member_vote_source_position", "")) or 0) <= 0:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: invalid vote source position"
            )
        target_row = target_scope_by_bill.get(bill_id)
        expected_target_ids = (
            split_semicolon_values(target_row, "member_bioguide_ids") if target_row else set()
        )
        report_target_ids = split_semicolon_values(row, "same_bill_campaign_target_bioguide_ids")
        if report_target_ids != expected_target_ids:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "same-bill target Bioguide IDs do not match campaign target-scope review"
            )
        voter_bioguide = row.get("voter_bioguide_id", "").strip()
        if voter_bioguide in expected_target_ids:
            member_vote_same_bill_overlap_rows += 1
            expected_match = "same_bill_campaign_target_bioguide_overlap"
        elif expected_target_ids:
            expected_match = "no_same_bill_campaign_target_bioguide_overlap"
        else:
            expected_match = "not_applicable_no_same_bill_campaign_target_scope_row"
        if row.get("same_bill_campaign_target_match_status", "") != expected_match:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "same-bill target match status mismatch"
            )
        broad_context_present = (
            row.get("broad_campaign_member_context_status")
            == "broad_public_fec_candidate_member_context_present"
        )
        if broad_context_present:
            member_vote_broad_context_rows += 1
            if (parse_int(row.get("broad_campaign_transaction_rows", "")) or 0) <= 0:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                    "broad campaign member context should carry transaction rows"
                )
        for required_layer in (
            "bill_finance_lobbying_roll_call_source_review",
            "official_house_clerk_member_vote_source",
            "bill_finance_lobbying_member_vote_target_scope_review",
        ):
            if required_layer not in split_semicolon_values(row, "evidence_layers"):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer!r}"
                )
        if target_row and "bill_finance_lobbying_campaign_finance_target_scope_review" not in split_semicolon_values(row, "evidence_layers"):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "missing campaign target-scope evidence layer"
            )
        if broad_context_present and "campaign_finance_member_context" not in split_semicolon_values(row, "evidence_layers"):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "missing broad campaign member-context evidence layer"
            )
        for required_gap in (
            "direct_member_vote_target_document",
            "roll_call_influence",
            "legislative_outcome_causality",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        boundary = row.get("claim_boundary", "")
        for phrase in ("member-vote target-scope review only", "not lobbying contact", "roll-call influence", "model validation"):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(member_vote_target_ranks) != list(
        range(1, len(bill_finance_lobbying_member_vote_target_review) + 1)
    ):
        failures.append(f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: ranks must be contiguous")
    expected_member_vote_bills = {
        bill_id
        for bill_id, row in roll_call_source_by_bill.items()
        if row.get("roll_call_source_review_status") == "official_house_clerk_roll_call_source_reviewed"
    }
    if set(member_vote_rows_by_bill) != expected_member_vote_bills:
        failures.append(
            "bill-finance/lobbying member-vote target/roll-call bill mismatch: "
            f"missing from member-vote={sorted(expected_member_vote_bills - set(member_vote_rows_by_bill))}, "
            f"extra={sorted(set(member_vote_rows_by_bill) - expected_member_vote_bills)}"
        )
    for bill_id in expected_member_vote_bills:
        expected_member_rows = parse_int(roll_call_source_by_bill[bill_id].get("member_vote_count", "")) or 0
        if len(member_vote_rows_by_bill.get(bill_id, [])) != expected_member_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: {bill_id}: "
                "member-vote row count does not match roll-call source review"
            )
    member_vote_target_counts = (
        len(bill_finance_lobbying_member_vote_target_review),
        len(member_vote_rows_by_roll_call),
        member_vote_same_bill_overlap_rows,
    )
    if member_vote_target_counts != (roll_call_source_member_vote_rows, 8, 0):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW}: "
            f"unexpected summary counts {member_vote_target_counts}"
        )

    required_source_acquisition_columns = {
        "acquisition_rank",
        "review_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_bioguide_id",
        "sponsor_party",
        "sponsor_state",
        "introduced_date",
        "enacted_date",
        "committee_reported",
        "floor_considered",
        "external_lda_exact_activity_match_rows",
        "external_lda_mention_packets",
        "campaign_target_scope_status",
        "local_govinfo_committee_row_status",
        "local_govinfo_committees",
        "local_voteview_roll_call_rows",
        "official_member_vote_rows",
        "member_vote_target_scope_status",
        "same_bill_campaign_target_member_vote_overlap_rows",
        "broad_campaign_member_context_overlap_rows",
        "committee_jurisdiction_acquisition_status",
        "committee_action_record_acquisition_status",
        "roll_call_acquisition_status",
        "lobbying_target_source_acquisition_status",
        "campaign_target_source_acquisition_status",
        "legislative_outcome_source_status",
        "priority_score",
        "next_review_action",
        "required_join_keys",
        "official_committee_source_url",
        "official_actions_source_url",
        "official_roll_call_source_urls",
        "official_api_committee_url",
        "official_api_actions_url",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "source_url",
        "claim_boundary",
    }
    missing_source_acquisition_columns = (
        required_source_acquisition_columns
        - set(bill_finance_lobbying_source_acquisition_queue[0])
    )
    if missing_source_acquisition_columns:
        failures.append(
            f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: missing columns "
            f"{sorted(missing_source_acquisition_columns)}"
        )
    if not BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE_MD.exists():
        failures.append(f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE_MD}: missing markdown report")
    else:
        source_acquisition_md = BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE_MD.read_text()
        for phrase in (
            "Queued public-law rows: 10",
            "Rows with official govinfo committee names: 9",
            "Rows source-reviewed without direct committee names: 1",
            "Rows with local Voteview roll-call context: 0",
            "Rows with official House Clerk roll-call source review: 8",
            "Rows with official member-vote target-scope review: 8",
            "Official member-vote rows reviewed for target scope: 3435",
            "Member-vote rows with same-bill reviewed campaign target Bioguide overlap: 0",
            "Member-vote rows with broad public FEC member-context overlap:",
            "Rows reviewed as floor actions without numbered roll calls: 2",
            "Rows needing official roll-call source acquisition: 0",
            "Rows needing official committee-of-jurisdiction acquisition: 0",
            "Rows with external LDA mention packets to prioritize: 2",
            "Rows with campaign target-scope review to prioritize: 4",
            "not finance/lobbying influence evidence",
            "Claim boundary",
        ):
            if phrase not in source_acquisition_md:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    source_acquisition_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_finance_lobbying_source_acquisition_queue
        if row.get("bill_id", "").strip()
    }
    if len(source_acquisition_by_bill) != len(bill_finance_lobbying_source_acquisition_queue):
        failures.append(f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: duplicate bill_id rows")
    if set(source_acquisition_by_bill) != set(committee_context_by_bill):
        failures.append(
            "bill-finance/lobbying source-acquisition/committee-context bill mismatch: "
            f"missing from acquisition={sorted(set(committee_context_by_bill) - set(source_acquisition_by_bill))}, "
            f"extra={sorted(set(source_acquisition_by_bill) - set(committee_context_by_bill))}"
        )
    voteview_counts_by_bill_id: Counter[str] = Counter(
        row.get("bill_id", "").strip()
        for row in voteview_bill_linkage
        if row.get("bill_id", "").strip()
    )

    def expected_congress_bill_base_url(bill_id: str) -> str:
        parts = bill_id.split("-")
        if len(parts) != 3:
            return ""
        congress, bill_type, number = parts
        congress_number = parse_int(congress) or 0
        suffix = "th" if 10 <= congress_number % 100 <= 20 else {
            1: "st",
            2: "nd",
            3: "rd",
        }.get(congress_number % 10, "th")
        bill_type_path = "hr-bill" if bill_type == "hr" else "s-bill" if bill_type == "s" else f"{bill_type}-bill"
        return f"https://www.congress.gov/bill/{congress_number}{suffix}-congress/{bill_type_path}/{number}"

    def expected_congress_api_base_url(bill_id: str) -> str:
        parts = bill_id.split("-")
        if len(parts) != 3:
            return ""
        congress, bill_type, number = parts
        return f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{number}"

    source_acquisition_ranks: list[int] = []
    source_acquisition_govinfo_committee_rows = 0
    source_acquisition_voteview_rows = 0
    source_acquisition_official_roll_call_rows = 0
    source_acquisition_no_numbered_roll_call_rows = 0
    source_acquisition_member_vote_review_rows = 0
    source_acquisition_member_vote_rows = 0
    source_acquisition_same_bill_member_vote_overlap_rows = 0
    source_acquisition_broad_campaign_member_context_rows = 0
    source_acquisition_roll_call_followup_rows = 0
    source_acquisition_committee_followup_rows = 0
    source_acquisition_lda_priority_rows = 0
    source_acquisition_campaign_priority_rows = 0
    for bill_id, acquisition_row in source_acquisition_by_bill.items():
        context_row = committee_context_by_bill.get(bill_id, {})
        source_row = source_review_by_bill.get(bill_id, {})
        roll_call_row = roll_call_source_by_bill.get(bill_id, {})
        rank = parse_int(acquisition_row.get("acquisition_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: invalid rank")
        else:
            source_acquisition_ranks.append(rank)
        if acquisition_row.get("review_rank", "") != context_row.get("review_rank", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: review_rank mismatch"
            )
        for field in (
            "public_law_number",
            "policy_area",
            "sponsor_bioguide_id",
            "sponsor_party",
            "sponsor_state",
            "introduced_date",
            "enacted_date",
            "committee_reported",
            "floor_considered",
            "external_lda_exact_activity_match_rows",
            "external_lda_mention_packets",
            "campaign_target_scope_status",
        ):
            if acquisition_row.get(field, "").strip() != context_row.get(field, "").strip():
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"{field} does not match committee/action context"
                )
        expected_govinfo_committees = source_row.get("committee_names", "").strip()
        if parse_int(source_row.get("committee_count", "")) > 0 and expected_govinfo_committees:
            expected_govinfo_status = "official_govinfo_committee_source_review_present"
        elif source_row.get("committee_source_status") == (
            "official_govinfo_billstatus_reviewed_without_direct_committee_names"
        ):
            expected_govinfo_status = "official_govinfo_billstatus_reviewed_without_direct_committee_names"
            expected_govinfo_committees = ""
        elif source_row.get("govinfo_billstatus_status") == "official_govinfo_billstatus_fetched":
            expected_govinfo_status = "official_govinfo_billstatus_source_review_without_committee_names"
            expected_govinfo_committees = ""
        else:
            expected_govinfo_status = "official_govinfo_committee_action_source_review_unavailable"
            expected_govinfo_committees = ""
        if acquisition_row.get("local_govinfo_committee_row_status", "") != expected_govinfo_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "local govinfo committee status mismatch"
            )
        if acquisition_row.get("local_govinfo_committees", "") != expected_govinfo_committees:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "local govinfo committee names mismatch"
            )
        if expected_govinfo_committees:
            source_acquisition_govinfo_committee_rows += 1
        expected_voteview_rows = voteview_counts_by_bill_id.get(bill_id, 0)
        if parse_int(acquisition_row.get("local_voteview_roll_call_rows", "")) != expected_voteview_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "local Voteview roll-call count mismatch"
            )
        if expected_voteview_rows:
            source_acquisition_voteview_rows += 1
        expected_member_vote_rows = len(member_vote_rows_by_bill.get(bill_id, []))
        expected_same_bill_member_vote_overlap_rows = sum(
            1 for row in member_vote_rows_by_bill.get(bill_id, [])
            if row.get("same_bill_campaign_target_match_status")
            == "same_bill_campaign_target_bioguide_overlap"
        )
        expected_broad_member_context_rows = sum(
            1 for row in member_vote_rows_by_bill.get(bill_id, [])
            if row.get("broad_campaign_member_context_status")
            == "broad_public_fec_candidate_member_context_present"
        )
        if parse_int(acquisition_row.get("official_member_vote_rows", "")) != expected_member_vote_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "official member-vote row count mismatch"
            )
        if parse_int(acquisition_row.get("same_bill_campaign_target_member_vote_overlap_rows", "")) != expected_same_bill_member_vote_overlap_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "same-bill campaign target member-vote overlap count mismatch"
            )
        if parse_int(acquisition_row.get("broad_campaign_member_context_overlap_rows", "")) != expected_broad_member_context_rows:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "broad campaign member-context overlap count mismatch"
            )
        if roll_call_row.get("roll_call_source_review_status") == (
            "official_floor_action_reviewed_without_numbered_roll_call"
        ):
            expected_member_vote_status = "not_applicable_floor_action_without_numbered_member_vote_rows"
        elif roll_call_row.get("roll_call_source_review_status") != "official_house_clerk_roll_call_source_reviewed":
            expected_member_vote_status = "needs_official_member_vote_source_before_target_scope_review"
        elif expected_member_vote_rows == 0:
            expected_member_vote_status = "official_roll_call_source_reviewed_needs_member_vote_target_scope_review"
        elif expected_same_bill_member_vote_overlap_rows > 0:
            expected_member_vote_status = (
                "official_member_vote_rows_joined_to_same_bill_campaign_target_scope_no_influence_evidence"
            )
        else:
            expected_member_vote_status = "official_member_vote_rows_reviewed_no_same_bill_campaign_target_overlap"
        if acquisition_row.get("member_vote_target_scope_status", "") != expected_member_vote_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "member-vote target-scope status mismatch"
            )
        if expected_member_vote_rows > 0:
            source_acquisition_member_vote_review_rows += 1
            source_acquisition_member_vote_rows += expected_member_vote_rows
            source_acquisition_same_bill_member_vote_overlap_rows += expected_same_bill_member_vote_overlap_rows
            source_acquisition_broad_campaign_member_context_rows += expected_broad_member_context_rows
        expected_score = 0
        direct_committee_source = (
            parse_int(source_row.get("committee_count", "")) > 0
            or source_row.get("committee_action_record_status")
            == "official_govinfo_committee_action_records_present"
        )
        if acquisition_row.get("committee_reported") == "yes" and direct_committee_source:
            expected_score += 2
        if acquisition_row.get("floor_considered") == "yes":
            expected_score += 2
        if parse_int(acquisition_row.get("external_lda_mention_packets", "")) > 0:
            expected_score += 3
            source_acquisition_lda_priority_rows += 1
        if acquisition_row.get("campaign_target_scope_status") != "not_in_campaign_finance_target_scope_review":
            expected_score += 2
            source_acquisition_campaign_priority_rows += 1
        if expected_voteview_rows == 0 and acquisition_row.get("floor_considered") == "yes":
            expected_score += 1
        if parse_int(acquisition_row.get("priority_score", "")) != expected_score:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: priority score mismatch"
            )
        if parse_int(source_row.get("committee_count", "")) > 0:
            expected_committee_status = "official_committee_of_jurisdiction_source_reviewed"
        elif source_row.get("committee_source_status") == (
            "official_govinfo_billstatus_reviewed_without_direct_committee_names"
        ):
            expected_committee_status = "official_govinfo_billstatus_reviewed_without_direct_committee_referral"
        else:
            expected_committee_status = (
                "official_govinfo_billstatus_reviewed_without_committee_names_needs_committee_source_followup"
            )
        if expected_committee_status not in {
            "official_committee_of_jurisdiction_source_reviewed",
            "official_govinfo_billstatus_reviewed_without_direct_committee_referral",
        }:
            source_acquisition_committee_followup_rows += 1
        if acquisition_row.get("committee_jurisdiction_acquisition_status", "") != expected_committee_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "committee jurisdiction status mismatch"
            )
        expected_committee_action_status = (
            "official_committee_action_records_reviewed_no_influence_evidence"
            if source_row.get("committee_action_record_status")
            == "official_govinfo_committee_action_records_present"
            else "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
            if source_row.get("committee_action_record_status")
            == "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
            else ""
        )
        if (
            not expected_committee_action_status
            or acquisition_row.get("committee_action_record_acquisition_status", "")
            != expected_committee_action_status
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "committee action source status mismatch"
            )
        if acquisition_row.get("legislative_outcome_source_status", "") != (
            "official_govinfo_public_law_outcome_source_reviewed_no_finance_lobbying_causality_source"
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "outcome source status must reject causality"
            )
        if roll_call_row.get("roll_call_source_review_status") == "official_house_clerk_roll_call_source_reviewed":
            expected_roll_call_status = (
                "official_house_clerk_roll_call_source_reviewed_no_finance_lobbying_influence_evidence"
            )
            source_acquisition_official_roll_call_rows += 1
        elif roll_call_row.get("roll_call_source_review_status") == (
            "official_floor_action_reviewed_without_numbered_roll_call"
        ):
            expected_roll_call_status = "official_floor_action_reviewed_without_numbered_roll_call"
            source_acquisition_no_numbered_roll_call_rows += 1
        elif parse_int(source_row.get("roll_call_reference_count", "")) > 0:
            expected_roll_call_status = "official_billstatus_roll_call_references_present_needs_vote_source_join"
            source_acquisition_roll_call_followup_rows += 1
        elif parse_int(source_row.get("floor_action_count", "")) > 0:
            expected_roll_call_status = "floor_action_source_reviewed_needs_official_roll_call_vote_source"
            source_acquisition_roll_call_followup_rows += 1
        elif acquisition_row.get("floor_considered") == "yes":
            expected_roll_call_status = "floor_considered_flag_without_local_voteview_match_needs_official_roll_call_source"
            source_acquisition_roll_call_followup_rows += 1
        else:
            expected_roll_call_status = "no_floor_flag_and_no_local_roll_call_context"
        if acquisition_row.get("roll_call_acquisition_status", "") != expected_roll_call_status:
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "unexpected roll-call acquisition status"
            )
        base_url = expected_congress_bill_base_url(bill_id)
        api_base_url = expected_congress_api_base_url(bill_id)
        expected_urls = {
            "official_committee_source_url": f"{base_url}/committees",
            "official_actions_source_url": f"{base_url}/all-actions",
            "official_api_committee_url": f"{api_base_url}/committees",
            "official_api_actions_url": f"{api_base_url}/actions",
        }
        for field, expected_url in expected_urls.items():
            if acquisition_row.get(field, "") != expected_url:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"{field} mismatch"
                )
            if expected_url not in acquisition_row.get("source_urls", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"source_urls missing {field}"
                )
        roll_call_urls = acquisition_row.get("official_roll_call_source_urls", "")
        for required_url in ("https://clerk.house.gov/Votes", "https://www.senate.gov/legislative/votes_new.htm"):
            if required_url not in roll_call_urls:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"roll-call source URLs missing {required_url}"
                )
        for required_layer in (
            "bill_finance_lobbying_committee_action_context",
            "bill_finance_lobbying_committee_action_source_review",
            "bill_finance_lobbying_roll_call_source_review",
            "local_govinfo_billstatus_linkage_coverage_check",
            "local_voteview_bill_linkage_coverage_check",
            "official_source_acquisition_targets",
        ):
            if required_layer not in split_semicolon_values(acquisition_row, "evidence_layers"):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"missing evidence layer {required_layer!r}"
                )
        if expected_member_vote_rows > 0 and (
            "bill_finance_lobbying_member_vote_target_scope_review"
            not in split_semicolon_values(acquisition_row, "evidence_layers")
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "missing member-vote target-scope evidence layer"
            )
        required_gaps = [
            "lobbying_contact_or_target_source",
            "external_campaign_target_source_document",
            "committee_action_influence",
            "roll_call_influence",
            "legislative_outcome_causality",
            "model_validation",
        ]
        if parse_int(source_row.get("committee_count", "")) == 0 and source_row.get("committee_source_status") != (
            "official_govinfo_billstatus_reviewed_without_direct_committee_names"
        ):
            required_gaps.append("committee_of_jurisdiction")
        if roll_call_row.get("roll_call_source_review_status") == "official_house_clerk_roll_call_source_reviewed":
            if expected_member_vote_rows > 0:
                required_gaps.append("direct_member_vote_target_document")
            else:
                required_gaps.append("member_level_vote_target_join_to_finance_lobbying_source")
        elif roll_call_row.get("roll_call_source_review_status") == (
            "official_floor_action_reviewed_without_numbered_roll_call"
        ):
            pass
        elif parse_int(source_row.get("roll_call_reference_count", "")) > 0:
            required_gaps.append("official_roll_call_vote_source_join")
        else:
            required_gaps.append("official_roll_call_context")
        for required_gap in required_gaps:
            if required_gap not in acquisition_row.get("missing_links", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"missing gap {required_gap!r}"
                )
        if parse_int(source_row.get("committee_count", "")) > 0 and (
            "committee_of_jurisdiction" in acquisition_row.get("missing_links", "")
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "committee gap should be cleared by official source review"
            )
        if "source_reviewed_committee_action_record" in acquisition_row.get("missing_links", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "committee action source-review gap should be cleared"
            )
        if roll_call_row.get("roll_call_source_review_status") == "official_house_clerk_roll_call_source_reviewed" and (
            "official_roll_call_vote_source_join" in acquisition_row.get("missing_links", "")
        ):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "roll-call vote-source gap should be cleared by official source review"
            )
        if roll_call_row.get("roll_call_source_review_status") == (
            "official_floor_action_reviewed_without_numbered_roll_call"
        ) and "official_roll_call_context" in acquisition_row.get("missing_links", ""):
            failures.append(
                f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                "roll-call context gap should be cleared for reviewed non-numbered floor action"
            )
        for required_key in ("committee_name", "action_date", "roll_call_id", "filing_uuid", "candidate_id"):
            if required_key not in acquisition_row.get("required_join_keys", ""):
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"required join keys missing {required_key!r}"
                )
        boundary = acquisition_row.get("claim_boundary", "")
        for phrase in ("source-acquisition queue only", "does not provide", "model validation"):
            if phrase not in boundary:
                failures.append(
                    f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: {bill_id}: "
                    f"claim boundary missing {phrase!r}"
                )
    if sorted(source_acquisition_ranks) != list(
        range(1, len(bill_finance_lobbying_source_acquisition_queue) + 1)
    ):
        failures.append(f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: ranks must be contiguous")
    source_acquisition_counts = (
        len(bill_finance_lobbying_source_acquisition_queue),
        source_acquisition_govinfo_committee_rows,
        source_acquisition_voteview_rows,
        source_acquisition_official_roll_call_rows,
        source_acquisition_no_numbered_roll_call_rows,
        source_acquisition_member_vote_review_rows,
        source_acquisition_member_vote_rows,
        source_acquisition_same_bill_member_vote_overlap_rows,
        source_acquisition_broad_campaign_member_context_rows,
        source_acquisition_roll_call_followup_rows,
        source_acquisition_committee_followup_rows,
        source_acquisition_lda_priority_rows,
        source_acquisition_campaign_priority_rows,
    )
    if source_acquisition_counts != (
        10,
        9,
        0,
        8,
        2,
        8,
        3435,
        0,
        member_vote_broad_context_rows,
        0,
        0,
        2,
        4,
    ):
        failures.append(
            f"{BILL_FINANCE_LOBBYING_SOURCE_ACQUISITION_QUEUE}: "
            f"unexpected summary counts {source_acquisition_counts}"
        )

    required_statutory_lineage_columns = {
        "lineage_review_rank",
        "action_rank",
        "base_review_priority_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "enacted_date",
        "bill_title",
        "revision_flags",
        "revision_terms",
        "law_revision_summary_count",
        "law_revision_title_count",
        "bill_actions_count",
        "committee_reported",
        "floor_considered",
        "authority_document_count",
        "authority_document_numbers",
        "authority_usc_citation_count",
        "authority_usc_citations",
        "proposed_rule_document_count",
        "proposed_rule_document_numbers",
        "regulations_docket_count",
        "regulations_docket_ids",
        "court_case_count",
        "court_case_ids",
        "court_usc_section_count",
        "court_usc_sections",
        "court_direct_review_status",
        "closed_review_gates",
        "lineage_review_status",
        "source_review_targets",
        "next_review_action",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_statutory_lineage_columns = (
        required_statutory_lineage_columns - set(statutory_lineage_review_queue[0])
    )
    if missing_statutory_lineage_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: missing columns "
            f"{sorted(missing_statutory_lineage_columns)}"
        )
    if not STATUTORY_LINEAGE_REVIEW_QUEUE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE_MD}: missing markdown report")
    else:
        lineage_md = STATUTORY_LINEAGE_REVIEW_QUEUE_MD.read_text()
        for phrase in (
            "source-review queue",
            "not statutory-lineage evidence",
            "Claim boundary",
            "Rows with authority U.S.C. citations",
        ):
            if phrase not in lineage_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE_MD}: missing summary phrase {phrase!r}"
                )
    expected_lineage_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in bill_law_lifecycle_next_actions
        if row.get("next_actionable_upgrade_gate", "") == "codified_usc_lineage"
        and row.get("bill_id", "").strip()
    }
    lineage_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in statutory_lineage_review_queue
        if row.get("bill_id", "").strip()
    }
    if len(lineage_by_bill) != len(statutory_lineage_review_queue):
        failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: duplicate bill_id rows")
    if set(lineage_by_bill) != set(expected_lineage_by_bill):
        failures.append(
            "statutory-lineage queue/lifecycle next-actions mismatch: "
            f"missing from queue={sorted(set(expected_lineage_by_bill) - set(lineage_by_bill))}, "
            f"extra={sorted(set(lineage_by_bill) - set(expected_lineage_by_bill))}"
        )
    if STATUTORY_LINEAGE_REVIEW_QUEUE_MD.exists():
        lineage_md = STATUTORY_LINEAGE_REVIEW_QUEUE_MD.read_text()
        expected_phrase = f"Lineage review rows: {len(expected_lineage_by_bill)}"
        if expected_phrase not in lineage_md:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE_MD}: missing summary phrase {expected_phrase!r}"
            )

    try:
        law_history_by_public_law = by_field(law_revision_rows, "public_law_number")
        law_linkage_by_bill = by_field(law_bill_rows, "bill_id")
    except ValueError as exception:
        failures.append(str(exception))
        law_history_by_public_law = {}
        law_linkage_by_bill = {}

    lineage_ranks: list[int] = []
    for bill_id, lineage_row in lineage_by_bill.items():
        action_row = expected_lineage_by_bill.get(bill_id, {})
        spine_row = spine_by_bill.get(bill_id, {})
        public_law = lineage_row.get("public_law_number", "").strip()
        history_row = law_history_by_public_law.get(public_law, {})
        linkage_row = law_linkage_by_bill.get(bill_id, {})
        rank = parse_int(lineage_row.get("lineage_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: invalid lineage_review_rank")
        else:
            lineage_ranks.append(rank)
        for field in (
            "action_rank",
            "base_review_priority_rank",
            "public_law_number",
            "policy_area",
            "court_direct_review_status",
            "closed_review_gates",
        ):
            if lineage_row.get(field, "").strip() != action_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: {field} "
                    f"does not match {BILL_LAW_LIFECYCLE_NEXT_ACTIONS}"
                )
        if lineage_row.get("lineage_review_status", "") != "needs_codified_usc_lineage_source_review":
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: invalid lineage_review_status"
            )
        if not history_row:
            failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: missing law revision history row")
        if not linkage_row:
            failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: missing law revision bill-linkage row")
        for output_field, history_field in (
            ("enacted_date", "enacted_date"),
            ("bill_title", "bill_title"),
            ("revision_terms", "revision_terms"),
            ("law_revision_summary_count", "summary_count"),
            ("law_revision_title_count", "title_count"),
        ):
            if lineage_row.get(output_field, "").strip() != history_row.get(history_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: {output_field} "
                    f"does not match {LAW_REVISION_HISTORY} {history_field}"
                )
        expected_revision_flags = {
            field for field in STATUTORY_REVISION_FLAG_FIELDS
            if history_row.get(field, "").strip() == "1"
        } or {"none"}
        if split_semicolon_values(lineage_row, "revision_flags") != expected_revision_flags:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: revision_flags mismatch"
            )
        for output_field, linkage_field in (
            ("bill_actions_count", "actions_count"),
            ("committee_reported", "committee_reported"),
            ("floor_considered", "floor_considered"),
        ):
            if lineage_row.get(output_field, "").strip() != linkage_row.get(linkage_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: {output_field} "
                    f"does not match {LAW_REVISION_BILL_LINKAGE} {linkage_field}"
                )
        pointer_fields = {
            "authority_document_numbers": "implementation_authority_document_numbers",
            "authority_usc_citations": "implementation_authority_usc_citations",
            "proposed_rule_document_numbers": "implementation_history_proposed_document_numbers",
            "regulations_docket_ids": "implementation_history_proposed_regulations_docket_ids",
            "court_case_ids": "court_review_case_ids",
            "court_usc_sections": "court_review_usc_sections",
        }
        count_fields = {
            "authority_document_count": "authority_document_numbers",
            "authority_usc_citation_count": "authority_usc_citations",
            "proposed_rule_document_count": "proposed_rule_document_numbers",
            "regulations_docket_count": "regulations_docket_ids",
            "court_case_count": "court_case_ids",
            "court_usc_section_count": "court_usc_sections",
        }
        for output_field, spine_field in pointer_fields.items():
            actual_values = split_semicolon_values(lineage_row, output_field)
            expected_values = split_semicolon_values(spine_row, spine_field)
            if actual_values != expected_values:
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: {output_field} "
                    f"does not match {BILL_LAW_SPINE} {spine_field}"
                )
        for count_field, value_field in count_fields.items():
            if parse_int(lineage_row.get(count_field, "")) != len(split_semicolon_values(lineage_row, value_field)):
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: {count_field} mismatch"
                )
        targets = split_semicolon_values(lineage_row, "source_review_targets")
        if not STATUTORY_LINEAGE_SOURCE_REVIEW_TARGETS <= targets:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: missing source review targets"
            )
        missing_links = split_semicolon_values(lineage_row, "missing_links")
        if not STATUTORY_LINEAGE_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: missing statutory-lineage gap markers"
            )
        evidence_layers = split_semicolon_values(lineage_row, "evidence_layers")
        for layer in (
            "statutory_lineage_review_queue",
            "bill_law_lifecycle_next_actions",
            "bill_law_evidence_spine",
        ):
            if layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: missing evidence layer {layer}"
                )
        next_action = lineage_row.get("next_review_action", "")
        if "Review public-law text" not in next_action or "OLRC/govinfo" not in next_action:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: next_review_action must name source review"
            )
        boundary = lineage_row.get("claim_boundary", "")
        if (
            "Statutory-lineage source-review queue only" not in boundary
            or "not statutory-lineage evidence" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: claim boundary must reject statutory-lineage overclaiming"
            )
        expected_source_url = history_row.get("source_url", "") or linkage_row.get("source_url", "")
        if lineage_row.get("source_url", "").strip() != expected_source_url:
            failures.append(
                f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: {bill_id}: source_url mismatch"
            )
    if sorted(lineage_ranks) != list(range(1, len(statutory_lineage_review_queue) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_REVIEW_QUEUE}: lineage review ranks must be contiguous")

    required_source_scan_columns = {
        "scan_rank",
        "lineage_review_rank",
        "action_rank",
        "bill_id",
        "public_law_number",
        "govinfo_package_id",
        "govinfo_text_url",
        "govinfo_details_url",
        "source_review_status",
        "official_text_sha256",
        "official_text_bytes",
        "bill_title",
        "revision_flags",
        "usc_reference_count",
        "unique_usc_references",
        "title_code_reference_count",
        "amendment_phrase_count",
        "repeal_phrase_count",
        "redesignation_phrase_count",
        "target_section_candidate_count",
        "target_section_candidates",
        "codification_source_status",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_source_scan_raw:
        failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN_RAW}: no rows")
    missing_source_scan_raw_columns = (
        required_source_scan_columns - set(statutory_lineage_source_scan_raw[0])
    ) if statutory_lineage_source_scan_raw else required_source_scan_columns
    missing_source_scan_columns = (
        required_source_scan_columns - set(statutory_lineage_source_scan[0])
    )
    if missing_source_scan_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_SOURCE_SCAN_RAW}: missing columns "
            f"{sorted(missing_source_scan_raw_columns)}"
        )
    if missing_source_scan_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_SOURCE_SCAN}: missing columns "
            f"{sorted(missing_source_scan_columns)}"
        )
    if not STATUTORY_LINEAGE_SOURCE_SCAN_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN_MD}: missing markdown report")
    else:
        source_scan_md = STATUTORY_LINEAGE_SOURCE_SCAN_MD.read_text()
        for phrase in (
            "official GovInfo public-law text scan",
            "source scan, not codified-lineage evidence",
            "Claim boundary",
        ):
            if phrase not in source_scan_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_SOURCE_SCAN_MD}: missing summary phrase {phrase!r}"
                )
        for expected_scan_summary in (
            f"Source-scan rows retained: {len(statutory_lineage_source_scan)}",
            f"Active source-review queue rows: {len(lineage_by_bill)}",
        ):
            if expected_scan_summary not in source_scan_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_SOURCE_SCAN_MD}: missing summary phrase {expected_scan_summary!r}"
                )
    if statutory_lineage_source_scan != statutory_lineage_source_scan_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_SOURCE_SCAN}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_SOURCE_SCAN_RAW}"
        )
    source_scan_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in statutory_lineage_source_scan
        if row.get("bill_id", "").strip()
    }
    if len(source_scan_by_bill) != len(statutory_lineage_source_scan):
        failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: duplicate bill_id rows")
    reviewed_no_target_bills = {
        row.get("bill_id", "").strip()
        for row in statutory_lineage_no_target_review
        if row.get("bill_id", "").strip()
    }
    expected_source_scan_bills = set(lineage_by_bill) | reviewed_no_target_bills
    if set(source_scan_by_bill) != expected_source_scan_bills:
        failures.append(
            "statutory-lineage source scan/review queue mismatch: "
            f"missing from scan={sorted(expected_source_scan_bills - set(source_scan_by_bill))}, "
            f"extra={sorted(set(source_scan_by_bill) - expected_source_scan_bills)}"
        )
    source_scan_ranks: list[int] = []
    for bill_id, scan_row in source_scan_by_bill.items():
        queue_row = lineage_by_bill.get(bill_id, {})
        scan_rank = parse_int(scan_row.get("scan_rank", ""))
        if scan_rank is None or scan_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: invalid scan_rank")
        else:
            source_scan_ranks.append(scan_rank)
        if queue_row:
            for field in (
                "bill_id",
                "public_law_number",
                "bill_title",
                "revision_flags",
            ):
                if scan_row.get(field, "").strip() != queue_row.get(field, "").strip():
                    failures.append(
                        f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: {field} "
                        f"does not match {STATUTORY_LINEAGE_REVIEW_QUEUE}"
                    )
        elif bill_id not in reviewed_no_target_bills:
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: scan row is neither active queue nor reviewed no-target"
            )
        public_law = scan_row.get("public_law_number", "")
        try:
            congress, law_number = public_law.split("-", maxsplit=1)
            expected_package = f"PLAW-{congress}publ{int(law_number)}"
        except ValueError:
            expected_package = ""
        package_id = scan_row.get("govinfo_package_id", "")
        if package_id != expected_package:
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: govinfo_package_id mismatch"
            )
        expected_text_url = f"https://www.govinfo.gov/content/pkg/{package_id}/html/{package_id}.htm"
        expected_details_url = f"https://www.govinfo.gov/app/details/{package_id}"
        if scan_row.get("govinfo_text_url", "") != expected_text_url:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: text URL mismatch")
        if scan_row.get("govinfo_details_url", "") != expected_details_url:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: details URL mismatch")
        if scan_row.get("source_review_status", "") != "official_govinfo_public_law_text_scanned":
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: invalid source_review_status")
        if scan_row.get("codification_source_status", "") != "govinfo_public_law_text_only_needs_olrc_or_us_code_notes":
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: invalid codification source status")
        if scan_row.get("lineage_evidence_status", "") != "source_text_scan_not_codified_lineage_evidence":
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: invalid lineage evidence status")
        text_bytes = parse_int(scan_row.get("official_text_bytes", ""))
        if text_bytes is None or text_bytes <= 0:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: official_text_bytes must be positive")
        source_hash = scan_row.get("official_text_sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", source_hash):
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: invalid official_text_sha256")
        for field in (
            "usc_reference_count",
            "title_code_reference_count",
            "amendment_phrase_count",
            "repeal_phrase_count",
            "redesignation_phrase_count",
            "target_section_candidate_count",
        ):
            value = parse_int(scan_row.get(field, ""))
            if value is None or value < 0:
                failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: {field} must be nonnegative")
        if parse_int(scan_row.get("usc_reference_count", "0")) == 0:
            if scan_row.get("unique_usc_references", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: zero U.S.C. count should not list references"
                )
        elif not scan_row.get("unique_usc_references", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: positive U.S.C. count should list references"
            )
        if parse_int(scan_row.get("target_section_candidate_count", "0")) == 0:
            if scan_row.get("target_section_candidates", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: zero candidate count should not list snippets"
                )
        elif not scan_row.get("target_section_candidates", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: positive candidate count should list snippets"
            )
        evidence_layers = split_semicolon_values(scan_row, "evidence_layers")
        if "govinfo_public_law_text_scan" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: missing GovInfo scan layer")
        if "statutory_lineage_review_queue" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: missing queue layer")
        missing_links = split_semicolon_values(scan_row, "missing_links")
        if not STATUTORY_LINEAGE_SOURCE_SCAN_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: missing source-scan gap markers"
            )
        notes = scan_row.get("source_review_notes", "")
        if "OLRC" not in notes or "target-section lineage" not in notes:
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: source_review_notes must name OLRC target-section follow-up"
            )
        boundary = scan_row.get("claim_boundary", "")
        if (
            "Official public-law text scan only" not in boundary
            or "codified U.S.C. lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_SOURCE_SCAN}: {bill_id}: claim boundary must reject lineage overclaiming"
            )
    if sorted(source_scan_ranks) != list(range(1, len(statutory_lineage_source_scan) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_SOURCE_SCAN}: source scan ranks must be contiguous")

    required_no_target_review_columns = {
        "review_rank",
        "source_scan_rank",
        "lineage_review_rank",
        "action_rank",
        "bill_id",
        "public_law_number",
        "govinfo_package_id",
        "govinfo_text_url",
        "olrc_public_law_pdf_url",
        "designation_subject",
        "review_status",
        "source_reviewed_no_structured_usc_target",
        "source_scan_usc_reference_count",
        "source_scan_title_code_reference_count",
        "source_scan_amendment_phrase_count",
        "source_scan_repeal_phrase_count",
        "source_scan_redesignation_phrase_count",
        "source_scan_target_section_candidate_count",
        "codification_disposition",
        "evidence_sources",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    missing_no_target_raw_columns = (
        required_no_target_review_columns - set(statutory_lineage_no_target_review_raw[0])
    ) if statutory_lineage_no_target_review_raw else required_no_target_review_columns
    missing_no_target_columns = (
        required_no_target_review_columns - set(statutory_lineage_no_target_review[0])
    ) if statutory_lineage_no_target_review else required_no_target_review_columns
    if missing_no_target_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW_RAW}: missing columns "
            f"{sorted(missing_no_target_raw_columns)}"
        )
    if missing_no_target_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: missing columns "
            f"{sorted(missing_no_target_columns)}"
        )
    if not STATUTORY_LINEAGE_NO_TARGET_REVIEW_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW_MD}: missing markdown report")
    else:
        no_target_md = STATUTORY_LINEAGE_NO_TARGET_REVIEW_MD.read_text()
        for phrase in (
            "curated source-reviewed no-target dispositions",
            "not target-section text-diff evidence",
            "Claim boundary",
        ):
            if phrase not in no_target_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    if statutory_lineage_no_target_review != statutory_lineage_no_target_review_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW_RAW}"
        )
    no_target_review_by_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_no_target_review
        if row.get("review_rank", "").strip()
    }
    if len(no_target_review_by_rank) != len(statutory_lineage_no_target_review):
        failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: duplicate review_rank rows")
    no_target_review_ranks: list[int] = []
    for review_row in statutory_lineage_no_target_review:
        review_rank = parse_int(review_row.get("review_rank", ""))
        bill_id = review_row.get("bill_id", "").strip()
        public_law = review_row.get("public_law_number", "").strip()
        if review_rank is None or review_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: invalid review_rank")
        else:
            no_target_review_ranks.append(review_rank)
        source_row = source_scan_by_bill.get(bill_id, {})
        for review_field, source_field in {
            "source_scan_rank": "scan_rank",
            "lineage_review_rank": "lineage_review_rank",
            "action_rank": "action_rank",
            "bill_id": "bill_id",
            "public_law_number": "public_law_number",
            "govinfo_package_id": "govinfo_package_id",
            "govinfo_text_url": "govinfo_text_url",
            "source_scan_usc_reference_count": "usc_reference_count",
            "source_scan_title_code_reference_count": "title_code_reference_count",
            "source_scan_amendment_phrase_count": "amendment_phrase_count",
            "source_scan_repeal_phrase_count": "repeal_phrase_count",
            "source_scan_redesignation_phrase_count": "redesignation_phrase_count",
            "source_scan_target_section_candidate_count": "target_section_candidate_count",
        }.items():
            if review_row.get(review_field, "").strip() != source_row.get(source_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: {review_field} "
                    f"does not match {STATUTORY_LINEAGE_SOURCE_SCAN} {source_field}"
                )
        if review_row.get("review_status", "") != "reviewed_designation_law_no_structured_usc_target":
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: invalid review_status")
        if review_row.get("source_reviewed_no_structured_usc_target", "") != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: source-reviewed no-target flag must be 1"
            )
        if review_row.get("codification_disposition", "") != "designation_law_no_codified_usc_target_in_public_law_text":
            failures.append(
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: invalid codification disposition"
            )
        for field in (
            "source_scan_usc_reference_count",
            "source_scan_title_code_reference_count",
            "source_scan_amendment_phrase_count",
            "source_scan_repeal_phrase_count",
            "source_scan_redesignation_phrase_count",
            "source_scan_target_section_candidate_count",
        ):
            if review_row.get(field, "").strip() != "0":
                failures.append(
                    f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: {field} must be 0"
                )
        expected_pdf_url = f"https://uscode.house.gov/download/bills/{public_law.split('-', maxsplit=1)[0]}-2/{public_law}.pdf" if "-" in public_law else ""
        if review_row.get("olrc_public_law_pdf_url", "") != expected_pdf_url:
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: OLRC PDF URL mismatch")
        evidence_layers = split_semicolon_values(review_row, "evidence_layers")
        if "statutory_lineage_no_target_review" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: missing no-target review layer")
        if "govinfo_public_law_text_scan" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: missing GovInfo scan layer")
        if "official_olrc_public_law_pdf" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: missing OLRC PDF layer")
        missing_links = split_semicolon_values(review_row, "missing_links")
        if not STATUTORY_LINEAGE_NO_TARGET_REVIEW_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: missing no-target gap markers"
            )
        boundary = review_row.get("claim_boundary", "")
        if (
            "no-structured-U.S.C.-target disposition" not in boundary
            or "target-section text diffs" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: {bill_id}: claim boundary must reject overclaiming"
            )
    if sorted(no_target_review_ranks) != list(range(1, len(statutory_lineage_no_target_review) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}: review ranks must be contiguous")

    required_target_triage_columns = {
        "triage_rank",
        "source_scan_rank",
        "lineage_review_rank",
        "bill_id",
        "public_law_number",
        "target_reference",
        "target_reference_type",
        "candidate_snippet_count",
        "amendment_snippet_count",
        "repeal_snippet_count",
        "redesignation_snippet_count",
        "incomplete_fragment_count",
        "example_snippets",
        "govinfo_text_url",
        "codification_review_status",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "next_review_action",
        "claim_boundary",
    }
    missing_target_triage_columns = (
        required_target_triage_columns - set(statutory_lineage_target_section_triage[0])
    )
    if missing_target_triage_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: missing columns "
            f"{sorted(missing_target_triage_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE_MD}: missing markdown report")
    else:
        target_triage_md = STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE_MD.read_text()
        for phrase in (
            "candidate U.S.C. target references",
            "review queue, not codified-lineage evidence",
            "Claim boundary",
        ):
            if phrase not in target_triage_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE_MD}: missing summary phrase {phrase!r}"
                )
    target_triage_bill_ids = {
        row.get("bill_id", "").strip()
        for row in statutory_lineage_target_section_triage
        if row.get("bill_id", "").strip()
    }
    if target_triage_bill_ids != set(source_scan_by_bill):
        failures.append(
            "statutory-lineage target-section triage/source scan mismatch: "
            f"missing from triage={sorted(set(source_scan_by_bill) - target_triage_bill_ids)}, "
            f"extra={sorted(target_triage_bill_ids - set(source_scan_by_bill))}"
        )
    target_triage_ranks: list[int] = []
    allowed_target_triage_statuses = {
        "needs_olrc_us_code_note_review",
        "title_only_needs_manual_target",
        "incomplete_reference_fragment_needs_manual_review",
        "mixed_target_reference_needs_manual_review",
        "source_scan_needs_manual_target_extraction",
        "source_scan_has_no_structured_usc_target",
    }
    for triage_row in statutory_lineage_target_section_triage:
        bill_id = triage_row.get("bill_id", "").strip()
        source_row = source_scan_by_bill.get(bill_id, {})
        triage_rank = parse_int(triage_row.get("triage_rank", ""))
        if triage_rank is None or triage_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: invalid triage_rank")
        else:
            target_triage_ranks.append(triage_rank)
        for field in ("source_scan_rank", "lineage_review_rank", "bill_id", "public_law_number", "govinfo_text_url"):
            source_field = "scan_rank" if field == "source_scan_rank" else field
            if triage_row.get(field, "").strip() != source_row.get(source_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_SOURCE_SCAN}"
                )
        target_reference = triage_row.get("target_reference", "").strip()
        reference_type = triage_row.get("target_reference_type", "").strip()
        if not target_reference:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: empty target_reference")
        if reference_type != "no_structured_target" and " USC " not in target_reference:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: structured target_reference must be U.S.C.-normalized"
            )
        for field in (
            "candidate_snippet_count",
            "amendment_snippet_count",
            "repeal_snippet_count",
            "redesignation_snippet_count",
            "incomplete_fragment_count",
        ):
            value = parse_int(triage_row.get(field, ""))
            if value is None or value < 0:
                failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: {field} must be nonnegative")
        snippet_count = parse_int(triage_row.get("candidate_snippet_count", "0")) or 0
        if snippet_count > 0 and not triage_row.get("example_snippets", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: positive snippet count must include examples"
            )
        status = triage_row.get("codification_review_status", "")
        if status not in allowed_target_triage_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: invalid codification_review_status"
            )
        if triage_row.get("lineage_evidence_status", "") != "target_section_triage_not_codified_lineage_evidence":
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: invalid lineage evidence status"
            )
        evidence_layers = split_semicolon_values(triage_row, "evidence_layers")
        if "target_section_candidate_triage" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: missing triage evidence layer"
            )
        if "statutory_lineage_source_scan" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: missing source-scan layer"
            )
        missing_links = split_semicolon_values(triage_row, "missing_links")
        if not STATUTORY_LINEAGE_SOURCE_SCAN_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: missing source-scan gap markers"
            )
        next_action = triage_row.get("next_review_action", "")
        if "OLRC" not in next_action or "before/after text" not in next_action:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: next_review_action must require OLRC before/after review"
            )
        boundary = triage_row.get("claim_boundary", "")
        if (
            "Target-section triage" not in boundary
            or "do not establish codified U.S.C. lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: {bill_id}: claim boundary must reject lineage overclaiming"
            )
    if sorted(target_triage_ranks) != list(range(1, len(statutory_lineage_target_section_triage) + 1)):
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: target-section triage ranks must be contiguous"
        )

    required_olrc_current_scan_columns = {
        "olrc_scan_rank",
        "triage_rank",
        "source_scan_rank",
        "lineage_review_rank",
        "bill_id",
        "public_law_number",
        "target_reference",
        "target_reference_type",
        "normalized_title",
        "normalized_section",
        "olrc_granule_id",
        "olrc_url",
        "olrc_scan_status",
        "http_status",
        "official_text_sha256",
        "official_text_bytes",
        "section_heading",
        "public_law_reference_hits",
        "public_law_reference_status",
        "codification_review_status",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_olrc_current_scan_raw:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_RAW}: no rows")
    missing_olrc_raw_columns = (
        required_olrc_current_scan_columns - set(statutory_lineage_olrc_current_scan_raw[0])
    ) if statutory_lineage_olrc_current_scan_raw else required_olrc_current_scan_columns
    missing_olrc_columns = (
        required_olrc_current_scan_columns - set(statutory_lineage_olrc_current_scan[0])
    )
    if missing_olrc_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_RAW}: missing columns "
            f"{sorted(missing_olrc_raw_columns)}"
        )
    if missing_olrc_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: missing columns "
            f"{sorted(missing_olrc_columns)}"
        )
    if not STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_MD}: missing markdown report")
    else:
        olrc_scan_md = STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_MD.read_text()
        for phrase in (
            "official OLRC current U.S. Code page availability scan",
            "not codified-lineage evidence",
            "Claim boundary",
        ):
            if phrase not in olrc_scan_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_MD}: missing summary phrase {phrase!r}"
                )
    if statutory_lineage_olrc_current_scan != statutory_lineage_olrc_current_scan_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN_RAW}"
        )
    triage_by_rank = {
        row.get("triage_rank", "").strip(): row
        for row in statutory_lineage_target_section_triage
        if row.get("triage_rank", "").strip()
    }
    olrc_by_triage_rank = {
        row.get("triage_rank", "").strip(): row
        for row in statutory_lineage_olrc_current_scan
        if row.get("triage_rank", "").strip()
    }
    if len(olrc_by_triage_rank) != len(statutory_lineage_olrc_current_scan):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: duplicate triage_rank rows")
    if set(olrc_by_triage_rank) != set(triage_by_rank):
        failures.append(
            "statutory-lineage OLRC current scan/target triage mismatch: "
            f"missing from OLRC scan={sorted(set(triage_by_rank) - set(olrc_by_triage_rank))}, "
            f"extra={sorted(set(olrc_by_triage_rank) - set(triage_by_rank))}"
        )
    allowed_olrc_statuses = {
        "official_olrc_current_section_page_fetched",
        "official_olrc_current_section_page_http_error",
        "official_olrc_current_section_page_fetch_error",
        "title_only_not_fetched",
        "no_structured_target_not_fetched",
        "unparseable_target_not_fetched",
        "incomplete_or_nonsection_target_not_fetched",
        "dry_run_not_fetched",
    }
    allowed_public_law_statuses = {
        "current_page_mentions_public_law",
        "current_page_no_public_law_mention",
        "not_checked_no_current_page_text",
    }
    olrc_scan_ranks: list[int] = []
    fetched_olrc_rows = 0
    public_law_mention_rows = 0
    for olrc_row in statutory_lineage_olrc_current_scan:
        triage_rank = olrc_row.get("triage_rank", "").strip()
        triage_row = triage_by_rank.get(triage_rank, {})
        bill_id = olrc_row.get("bill_id", "").strip()
        olrc_rank = parse_int(olrc_row.get("olrc_scan_rank", ""))
        if olrc_rank is None or olrc_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid olrc_scan_rank")
        else:
            olrc_scan_ranks.append(olrc_rank)
        for field in (
            "triage_rank",
            "source_scan_rank",
            "lineage_review_rank",
            "bill_id",
            "public_law_number",
            "target_reference",
            "target_reference_type",
        ):
            if olrc_row.get(field, "").strip() != triage_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}"
                )
        status = olrc_row.get("olrc_scan_status", "")
        if status not in allowed_olrc_statuses:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid OLRC scan status")
        public_law_status = olrc_row.get("public_law_reference_status", "")
        if public_law_status not in allowed_public_law_statuses:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid public-law mention status")
        text_bytes = parse_int(olrc_row.get("official_text_bytes", ""))
        if text_bytes is None or text_bytes < 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: official_text_bytes must be nonnegative")
        public_law_hits = parse_int(olrc_row.get("public_law_reference_hits", ""))
        if public_law_hits is None or public_law_hits < 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: public_law_reference_hits must be nonnegative")
        if status == "official_olrc_current_section_page_fetched":
            fetched_olrc_rows += 1
            if olrc_row.get("http_status", "") != "200":
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: fetched rows must have HTTP 200")
            if text_bytes is None or text_bytes <= 0:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: fetched rows must have positive text bytes")
            if not re.fullmatch(r"[0-9a-f]{64}", olrc_row.get("official_text_sha256", "")):
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: fetched rows must have a source hash")
            if not olrc_row.get("section_heading", "").strip():
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: fetched rows must include section text")
            if public_law_status == "current_page_mentions_public_law":
                public_law_mention_rows += 1
                if public_law_hits is None or public_law_hits <= 0:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: public-law mention status requires positive hit count"
                    )
        else:
            if text_bytes not in (0, None):
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: non-fetched rows should not have text bytes")
            if olrc_row.get("official_text_sha256", "").strip():
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: non-fetched rows should not have source hash")
        url = olrc_row.get("olrc_url", "").strip()
        granule_id = olrc_row.get("olrc_granule_id", "").strip()
        if url:
            if "uscode.house.gov/view.xhtml" not in url or "USC-prelim-title" not in url:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid OLRC URL")
            if not granule_id or granule_id not in url:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: OLRC URL/granule mismatch")
        elif status == "official_olrc_current_section_page_fetched":
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: fetched rows require OLRC URL")
        if olrc_row.get("codification_review_status", "") != "current_olrc_page_availability_only":
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid codification review status")
        if olrc_row.get("lineage_evidence_status", "") != "current_olrc_scan_not_codified_lineage_evidence":
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: invalid lineage evidence status")
        evidence_layers = split_semicolon_values(olrc_row, "evidence_layers")
        if "statutory_lineage_target_section_triage" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: missing triage evidence layer")
        if "official_olrc_current_us_code_page" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: missing OLRC evidence layer")
        missing_links = split_semicolon_values(olrc_row, "missing_links")
        for marker in (
            "olrc_classification_review",
            "historical_us_code_version",
            "codified_usc_lineage",
            "target_section_diff",
            "model_validation",
        ):
            if marker not in missing_links:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: missing gap marker {marker}")
        boundary = olrc_row.get("claim_boundary", "")
        if (
            "Official OLRC current-section availability scan only" not in boundary
            or "do not establish historical codified U.S.C. lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: {bill_id}: claim boundary must reject OLRC overclaiming"
            )
    if sorted(olrc_scan_ranks) != list(range(1, len(statutory_lineage_olrc_current_scan) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: OLRC scan ranks must be contiguous")
    if fetched_olrc_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: no current OLRC pages fetched")
    if public_law_mention_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: no current OLRC pages mention queued public laws")

    required_olrc_historical_scan_columns = {
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
        "pre_olrc_granule_id",
        "pre_olrc_url",
        "pre_fetch_status",
        "pre_http_status",
        "pre_text_sha256",
        "pre_text_bytes",
        "pre_public_law_reference_hits",
        "post_olrc_granule_id",
        "post_olrc_url",
        "post_fetch_status",
        "post_http_status",
        "post_text_sha256",
        "post_text_bytes",
        "post_public_law_reference_hits",
        "annual_text_hash_status",
        "annual_public_law_window_status",
        "historical_review_status",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_olrc_historical_scan_raw:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_RAW}: no rows")
    missing_olrc_historical_raw_columns = (
        required_olrc_historical_scan_columns - set(statutory_lineage_olrc_historical_scan_raw[0])
    ) if statutory_lineage_olrc_historical_scan_raw else required_olrc_historical_scan_columns
    missing_olrc_historical_columns = (
        required_olrc_historical_scan_columns - set(statutory_lineage_olrc_historical_scan[0])
    )
    if missing_olrc_historical_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_RAW}: missing columns "
            f"{sorted(missing_olrc_historical_raw_columns)}"
        )
    if missing_olrc_historical_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: missing columns "
            f"{sorted(missing_olrc_historical_columns)}"
        )
    current_rows_eligible_for_historical_scan = [
        row
        for row in statutory_lineage_olrc_current_scan
        if row.get("public_law_reference_status") == "current_page_mentions_public_law"
        and row.get("olrc_scan_status") == "official_olrc_current_section_page_fetched"
        and row.get("normalized_title")
        and row.get("normalized_section")
    ]
    if not STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD}: missing markdown report")
    else:
        olrc_historical_md = STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD.read_text()
        for phrase in (
            "official OLRC annual-edition availability scan",
            "not codified-lineage evidence",
            "Claim boundary",
        ):
            if phrase not in olrc_historical_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD}: missing summary phrase {phrase!r}"
                )
        expected_historical_summary = (
            "Historical OLRC scan rows: "
            f"{len(statutory_lineage_olrc_historical_scan)} / "
            f"{len(current_rows_eligible_for_historical_scan)}"
        )
        if expected_historical_summary not in olrc_historical_md:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_MD}: missing summary phrase "
                f"{expected_historical_summary!r}"
            )
    if statutory_lineage_olrc_historical_scan != statutory_lineage_olrc_historical_scan_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN_RAW}"
        )
    current_by_olrc_rank = {
        row.get("olrc_scan_rank", "").strip(): row
        for row in statutory_lineage_olrc_current_scan
        if row.get("olrc_scan_rank", "").strip()
    }
    expected_historical_current_ranks = {
        row.get("olrc_scan_rank", "").strip()
        for row in current_rows_eligible_for_historical_scan
        if row.get("olrc_scan_rank", "").strip()
    }
    historical_by_current_rank = {
        row.get("current_olrc_scan_rank", "").strip(): row
        for row in statutory_lineage_olrc_historical_scan
        if row.get("current_olrc_scan_rank", "").strip()
    }
    if len(historical_by_current_rank) != len(statutory_lineage_olrc_historical_scan):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: duplicate current_olrc_scan_rank rows")
    if set(historical_by_current_rank) != expected_historical_current_ranks:
        failures.append(
            "statutory-lineage OLRC historical scan/current scan mismatch: "
            f"missing from historical scan={sorted(expected_historical_current_ranks - set(historical_by_current_rank))}, "
            f"extra={sorted(set(historical_by_current_rank) - expected_historical_current_ranks)}"
        )
    enacted_by_bill_law = {
        (row.get("bill_id", "").strip(), row.get("public_law_number", "").strip()): row.get("enacted_date", "").strip()
        for row in statutory_lineage_review_queue
    }
    allowed_annual_fetch_statuses = {
        "official_olrc_annual_section_page_fetched",
        "official_olrc_annual_section_page_http_error",
        "official_olrc_annual_section_page_fetch_error",
        "dry_run_not_fetched",
    }
    allowed_annual_hash_statuses = {
        "pre_post_hash_unavailable",
        "pre_post_hash_same",
        "pre_post_hash_changed",
    }
    allowed_annual_public_law_statuses = {
        "public_law_appears_in_post_edition_only",
        "public_law_mentions_in_pre_and_post_editions",
        "public_law_mentions_in_pre_edition_only",
        "public_law_mentions_absent_from_pre_and_post_editions",
    }
    allowed_historical_review_statuses = {
        "annual_pre_post_pages_fetched_needs_manual_diff_review",
        "pre_annual_page_only_needs_manual_followup",
        "post_annual_page_only_needs_manual_followup",
        "annual_pages_not_fetched_needs_manual_followup",
    }
    olrc_historical_ranks: list[int] = []
    historical_pre_post_pairs_fetched = 0
    for historical_row in statutory_lineage_olrc_historical_scan:
        current_rank = historical_row.get("current_olrc_scan_rank", "").strip()
        current_row = current_by_olrc_rank.get(current_rank, {})
        bill_id = historical_row.get("bill_id", "").strip()
        historical_rank = parse_int(historical_row.get("historical_scan_rank", ""))
        if historical_rank is None or historical_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid historical_scan_rank")
        else:
            olrc_historical_ranks.append(historical_rank)
        for historical_field, current_field in (
            ("current_olrc_scan_rank", "olrc_scan_rank"),
            ("triage_rank", "triage_rank"),
            ("source_scan_rank", "source_scan_rank"),
            ("lineage_review_rank", "lineage_review_rank"),
            ("bill_id", "bill_id"),
            ("public_law_number", "public_law_number"),
            ("target_reference", "target_reference"),
            ("target_reference_type", "target_reference_type"),
            ("normalized_title", "normalized_title"),
            ("normalized_section", "normalized_section"),
        ):
            if historical_row.get(historical_field, "").strip() != current_row.get(current_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: {historical_field} "
                    f"does not match {STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}"
                )
        enacted_date = enacted_by_bill_law.get(
            (historical_row.get("bill_id", "").strip(), historical_row.get("public_law_number", "").strip()),
            "",
        )
        if historical_row.get("enacted_date", "").strip() != enacted_date:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: enacted_date mismatch")
        enacted = parse_iso_date(enacted_date)
        if not enacted:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid enacted_date")
        else:
            if historical_row.get("pre_edition", "") != str(enacted.year - 1):
                failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: pre_edition mismatch")
            if historical_row.get("post_edition", "") != str(enacted.year):
                failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: post_edition mismatch")
        for prefix in ("pre", "post"):
            status = historical_row.get(f"{prefix}_fetch_status", "")
            if status not in allowed_annual_fetch_statuses:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid {prefix}_fetch_status"
                )
            text_bytes = parse_int(historical_row.get(f"{prefix}_text_bytes", ""))
            if text_bytes is None or text_bytes < 0:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: {prefix}_text_bytes must be nonnegative"
                )
            hits = parse_int(historical_row.get(f"{prefix}_public_law_reference_hits", ""))
            if hits is None or hits < 0:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: "
                    f"{prefix}_public_law_reference_hits must be nonnegative"
                )
            edition = historical_row.get(f"{prefix}_edition", "")
            title = historical_row.get("normalized_title", "")
            section = historical_row.get("normalized_section", "")
            expected_granule = f"USC-{edition}-title{title}-section{section}"
            if historical_row.get(f"{prefix}_olrc_granule_id", "") != expected_granule:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: {prefix}_olrc_granule_id mismatch"
                )
            url = historical_row.get(f"{prefix}_olrc_url", "")
            if (
                "uscode.house.gov/view.xhtml" not in url
                or f"edition={edition}" not in url
                or expected_granule not in url
            ):
                failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid {prefix}_olrc_url")
            if status == "official_olrc_annual_section_page_fetched":
                if historical_row.get(f"{prefix}_http_status", "") != "200":
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: fetched {prefix} rows must have HTTP 200"
                    )
                if text_bytes is None or text_bytes <= 0:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: fetched {prefix} rows must have positive text bytes"
                    )
                if not re.fullmatch(r"[0-9a-f]{64}", historical_row.get(f"{prefix}_text_sha256", "")):
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: fetched {prefix} rows must have a source hash"
                    )
            elif status in {"dry_run_not_fetched", "official_olrc_annual_section_page_fetch_error"}:
                if text_bytes not in (0, None):
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: "
                        f"{prefix} non-fetched rows should not have text bytes"
                    )
                if historical_row.get(f"{prefix}_text_sha256", "").strip():
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: "
                        f"{prefix} non-fetched rows should not have source hash"
                    )
        pre_fetched = historical_row.get("pre_fetch_status", "") == "official_olrc_annual_section_page_fetched"
        post_fetched = historical_row.get("post_fetch_status", "") == "official_olrc_annual_section_page_fetched"
        if pre_fetched and post_fetched:
            historical_pre_post_pairs_fetched += 1
            expected_hash_status = (
                "pre_post_hash_same"
                if historical_row.get("pre_text_sha256", "") == historical_row.get("post_text_sha256", "")
                else "pre_post_hash_changed"
            )
        else:
            expected_hash_status = "pre_post_hash_unavailable"
        if historical_row.get("annual_text_hash_status", "") not in allowed_annual_hash_statuses:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid annual_text_hash_status")
        elif historical_row.get("annual_text_hash_status", "") != expected_hash_status:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: annual_text_hash_status mismatch")
        pre_hits = parse_int(historical_row.get("pre_public_law_reference_hits", "0")) or 0
        post_hits = parse_int(historical_row.get("post_public_law_reference_hits", "0")) or 0
        if pre_hits == 0 and post_hits > 0:
            expected_public_law_status = "public_law_appears_in_post_edition_only"
        elif pre_hits > 0 and post_hits > 0:
            expected_public_law_status = "public_law_mentions_in_pre_and_post_editions"
        elif pre_hits > 0 and post_hits == 0:
            expected_public_law_status = "public_law_mentions_in_pre_edition_only"
        else:
            expected_public_law_status = "public_law_mentions_absent_from_pre_and_post_editions"
        if historical_row.get("annual_public_law_window_status", "") not in allowed_annual_public_law_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid annual_public_law_window_status"
            )
        elif historical_row.get("annual_public_law_window_status", "") != expected_public_law_status:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: annual_public_law_window_status mismatch"
            )
        if pre_fetched and post_fetched:
            expected_review_status = "annual_pre_post_pages_fetched_needs_manual_diff_review"
        elif pre_fetched:
            expected_review_status = "pre_annual_page_only_needs_manual_followup"
        elif post_fetched:
            expected_review_status = "post_annual_page_only_needs_manual_followup"
        else:
            expected_review_status = "annual_pages_not_fetched_needs_manual_followup"
        if historical_row.get("historical_review_status", "") not in allowed_historical_review_statuses:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid historical_review_status")
        elif historical_row.get("historical_review_status", "") != expected_review_status:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: historical_review_status mismatch")
        if historical_row.get("lineage_evidence_status", "") != "historical_edition_scan_not_codified_lineage_or_text_diff_evidence":
            failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: invalid lineage evidence status")
        evidence_layers = split_semicolon_values(historical_row, "evidence_layers")
        for layer in (
            "statutory_lineage_olrc_current_scan",
            "official_olrc_annual_us_code_page",
            "historical_edition_availability_scan",
        ):
            if layer not in evidence_layers:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(historical_row, "missing_links")
        if not STATUTORY_LINEAGE_OLRC_HISTORICAL_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: missing historical-scan gap markers"
            )
        notes = historical_row.get("source_review_notes", "")
        if "manual classification" not in notes or "text-diff" not in notes:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: source_review_notes must require manual diff review"
            )
        boundary = historical_row.get("claim_boundary", "")
        if (
            "Official OLRC annual-edition availability scan only" not in boundary
            or "do not establish historical codified U.S.C. lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: {bill_id}: claim boundary must reject OLRC overclaiming"
            )
    if sorted(olrc_historical_ranks) != list(range(1, len(statutory_lineage_olrc_historical_scan) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: historical scan ranks must be contiguous")
    if historical_pre_post_pairs_fetched == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}: no annual pre/post page pairs fetched")

    required_olrc_annual_text_diff_columns = {
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
        "pre_fetch_status",
        "pre_http_status",
        "pre_text_sha256",
        "pre_text_bytes",
        "pre_hash_matches_historical_scan",
        "pre_section_anchor_status",
        "pre_normalized_text_chars",
        "pre_normalized_text_sha256",
        "pre_public_law_reference_hits",
        "post_fetch_status",
        "post_http_status",
        "post_text_sha256",
        "post_text_bytes",
        "post_hash_matches_historical_scan",
        "post_section_anchor_status",
        "post_normalized_text_chars",
        "post_normalized_text_sha256",
        "post_public_law_reference_hits",
        "normalized_text_hash_status",
        "normalized_text_char_delta",
        "first_changed_text_pre_window",
        "first_changed_text_post_window",
        "public_law_reference_hit_delta",
        "post_public_law_context_count",
        "post_public_law_context_snippets",
        "automated_diff_cue_status",
        "section_change_cue_status",
        "manual_review_priority",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_olrc_annual_text_diff_raw:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_RAW}: no rows")
    missing_olrc_annual_text_diff_raw_columns = (
        required_olrc_annual_text_diff_columns - set(statutory_lineage_olrc_annual_text_diff_raw[0])
    ) if statutory_lineage_olrc_annual_text_diff_raw else required_olrc_annual_text_diff_columns
    missing_olrc_annual_text_diff_columns = (
        required_olrc_annual_text_diff_columns - set(statutory_lineage_olrc_annual_text_diff[0])
    )
    if missing_olrc_annual_text_diff_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_RAW}: missing columns "
            f"{sorted(missing_olrc_annual_text_diff_raw_columns)}"
        )
    if missing_olrc_annual_text_diff_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: missing columns "
            f"{sorted(missing_olrc_annual_text_diff_columns)}"
        )
    if not STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD}: missing markdown report")
    else:
        annual_text_diff_md = STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD.read_text()
        for phrase in (
            "bounded text-diff cues",
            "normalized section text signatures",
            "Rows with normalized pre/post section text changes",
            "Rows with post-edition target section anchors",
            "not source-reviewed codified-lineage evidence",
            "Claim boundary",
        ):
            if phrase not in annual_text_diff_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD}: missing summary phrase {phrase!r}"
                )
        expected_text_diff_summary = (
            f"Annual text-diff cue rows: {len(statutory_lineage_olrc_annual_text_diff)} / "
            f"{len(statutory_lineage_olrc_historical_scan)}"
        )
        if expected_text_diff_summary not in annual_text_diff_md:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MD}: missing summary phrase "
                f"{expected_text_diff_summary!r}"
            )
    if statutory_lineage_olrc_annual_text_diff != statutory_lineage_olrc_annual_text_diff_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_RAW}"
        )
    historical_by_rank = {
        row.get("historical_scan_rank", "").strip(): row
        for row in statutory_lineage_olrc_historical_scan
        if row.get("historical_scan_rank", "").strip()
    }
    annual_text_diff_by_historical_rank = {
        row.get("historical_scan_rank", "").strip(): row
        for row in statutory_lineage_olrc_annual_text_diff
        if row.get("historical_scan_rank", "").strip()
    }
    if len(annual_text_diff_by_historical_rank) != len(statutory_lineage_olrc_annual_text_diff):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: duplicate historical_scan_rank rows")
    if set(annual_text_diff_by_historical_rank) != set(historical_by_rank):
        failures.append(
            "statutory-lineage OLRC annual text-diff/historical scan mismatch: "
            f"missing from text-diff scan={sorted(set(historical_by_rank) - set(annual_text_diff_by_historical_rank))}, "
            f"extra={sorted(set(annual_text_diff_by_historical_rank) - set(historical_by_rank))}"
        )
    allowed_text_diff_cue_statuses = {
        "post_only_public_law_marker_on_changed_annual_page",
        "public_law_marker_present_in_pre_and_post_annual_pages",
        "annual_pages_fetched_without_post_only_public_law_marker",
        "partial_annual_text_available_needs_manual_followup",
        "annual_text_not_available_needs_manual_followup",
    }
    allowed_normalized_hash_statuses = {
        "pre_post_normalized_text_changed",
        "pre_post_normalized_text_same",
        "partial_normalized_text_available",
        "pre_post_normalized_text_unavailable",
    }
    allowed_section_anchor_statuses = {
        "section_anchor_found",
        "section_anchor_not_found",
        "section_anchor_unavailable",
    }
    allowed_section_change_cue_statuses = {
        "normalized_section_changed_with_post_only_public_law_marker",
        "normalized_section_changed_without_post_only_public_law_marker",
        "normalized_section_unchanged_with_post_only_public_law_marker",
        "normalized_section_unchanged_without_post_only_public_law_marker",
        "partial_annual_text_available_needs_manual_followup",
        "annual_text_not_available_needs_manual_followup",
    }
    allowed_manual_review_priorities = {
        "priority_1_review_post_public_law_context_and_target_section",
        "priority_1_review_section_text_change_without_public_law_marker",
        "priority_2_review_post_annual_text",
        "priority_3_refetch_or_manual_olrc_lookup",
    }
    annual_text_diff_ranks: list[int] = []
    post_only_text_diff_cues = 0
    hash_verified_text_diff_rows = 0
    normalized_text_change_rows = 0
    first_change_window_rows = 0
    for text_diff_row in statutory_lineage_olrc_annual_text_diff:
        historical_rank = text_diff_row.get("historical_scan_rank", "").strip()
        historical_row = historical_by_rank.get(historical_rank, {})
        bill_id = text_diff_row.get("bill_id", "").strip()
        text_diff_rank = parse_int(text_diff_row.get("text_diff_rank", ""))
        if text_diff_rank is None or text_diff_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid text_diff_rank")
        else:
            annual_text_diff_ranks.append(text_diff_rank)
        for field in (
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
        ):
            if text_diff_row.get(field, "").strip() != historical_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN}"
                )
        for prefix in ("pre", "post"):
            status = text_diff_row.get(f"{prefix}_fetch_status", "")
            if status not in allowed_annual_fetch_statuses:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid {prefix}_fetch_status"
                )
            if status == "official_olrc_annual_section_page_fetched":
                if text_diff_row.get(f"{prefix}_http_status", "") != "200":
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched {prefix} rows must have HTTP 200"
                    )
                if not re.fullmatch(r"[0-9a-f]{64}", text_diff_row.get(f"{prefix}_text_sha256", "")):
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched {prefix} rows must have source hash"
                    )
                hash_match_flag = text_diff_row.get(f"{prefix}_hash_matches_historical_scan", "")
                if hash_match_flag not in {"yes", "no"}:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid {prefix} hash comparison flag"
                    )
                anchor_status = text_diff_row.get(f"{prefix}_section_anchor_status", "")
                if anchor_status not in allowed_section_anchor_statuses:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid {prefix} section anchor status"
                    )
                if prefix == "post" and anchor_status != "section_anchor_found":
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched post rows must anchor normalized section text"
                    )
                if (
                    hash_match_flag == "yes"
                    and text_diff_row.get(f"{prefix}_text_sha256", "") != historical_row.get(f"{prefix}_text_sha256", "")
                ):
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: {prefix} hash comparison flag mismatch"
                    )
                text_bytes = parse_int(text_diff_row.get(f"{prefix}_text_bytes", ""))
                if text_bytes is None or text_bytes <= 0:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched {prefix} rows must have text bytes"
                    )
                text_chars = parse_int(text_diff_row.get(f"{prefix}_normalized_text_chars", ""))
                if text_chars is None or text_chars <= 0:
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched {prefix} rows need normalized text"
                    )
                if not re.fullmatch(r"[0-9a-f]{64}", text_diff_row.get(f"{prefix}_normalized_text_sha256", "")):
                    failures.append(
                        f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: fetched {prefix} rows must have normalized text hash"
                    )
            hits = parse_int(text_diff_row.get(f"{prefix}_public_law_reference_hits", ""))
            historical_hits = parse_int(historical_row.get(f"{prefix}_public_law_reference_hits", ""))
            historical_status = historical_row.get(f"{prefix}_fetch_status", "")
            if hits is None or hits < 0:
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: "
                    f"{prefix}_public_law_reference_hits must be nonnegative"
                )
            if (
                historical_status == "official_olrc_annual_section_page_fetched"
                and historical_hits is not None
                and hits != historical_hits
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: {prefix} public-law hit mismatch"
                )
        if (
            text_diff_row.get("pre_hash_matches_historical_scan") == "yes"
            and text_diff_row.get("post_hash_matches_historical_scan") == "yes"
        ):
            hash_verified_text_diff_rows += 1
        pre_fetched = text_diff_row.get("pre_fetch_status") == "official_olrc_annual_section_page_fetched"
        post_fetched = text_diff_row.get("post_fetch_status") == "official_olrc_annual_section_page_fetched"
        normalized_hash_status = text_diff_row.get("normalized_text_hash_status", "")
        if normalized_hash_status not in allowed_normalized_hash_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid normalized text hash status"
            )
        if pre_fetched and post_fetched:
            if text_diff_row.get("pre_normalized_text_sha256") == text_diff_row.get("post_normalized_text_sha256"):
                expected_normalized_hash_status = "pre_post_normalized_text_same"
            else:
                expected_normalized_hash_status = "pre_post_normalized_text_changed"
        elif pre_fetched or post_fetched:
            expected_normalized_hash_status = "partial_normalized_text_available"
        else:
            expected_normalized_hash_status = "pre_post_normalized_text_unavailable"
        if normalized_hash_status != expected_normalized_hash_status:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: normalized hash status mismatch"
            )
        pre_hits = parse_int(text_diff_row.get("pre_public_law_reference_hits", "0")) or 0
        post_hits = parse_int(text_diff_row.get("post_public_law_reference_hits", "0")) or 0
        hit_delta = parse_int(text_diff_row.get("public_law_reference_hit_delta", ""))
        if hit_delta is None or hit_delta != post_hits - pre_hits:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: hit delta mismatch")
        pre_chars = parse_int(text_diff_row.get("pre_normalized_text_chars", "0")) or 0
        post_chars = parse_int(text_diff_row.get("post_normalized_text_chars", "0")) or 0
        char_delta = parse_int(text_diff_row.get("normalized_text_char_delta", ""))
        if char_delta is None or char_delta != post_chars - pre_chars:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: normalized text char delta mismatch")
        cue_status = text_diff_row.get("automated_diff_cue_status", "")
        if cue_status not in allowed_text_diff_cue_statuses:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid automated diff cue status")
        if pre_hits == 0 and post_hits > 0:
            expected_cue_status = "post_only_public_law_marker_on_changed_annual_page"
            post_only_text_diff_cues += 1
        elif pre_hits > 0 and post_hits > 0:
            expected_cue_status = "public_law_marker_present_in_pre_and_post_annual_pages"
        else:
            expected_cue_status = "annual_pages_fetched_without_post_only_public_law_marker"
        if (
            text_diff_row.get("pre_fetch_status") == "official_olrc_annual_section_page_fetched"
            and text_diff_row.get("post_fetch_status") == "official_olrc_annual_section_page_fetched"
            and cue_status != expected_cue_status
        ):
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: cue status mismatch")
        section_change_status = text_diff_row.get("section_change_cue_status", "")
        if section_change_status not in allowed_section_change_cue_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid section change cue status"
            )
        if pre_fetched and post_fetched:
            normalized_changed = normalized_hash_status == "pre_post_normalized_text_changed"
            if normalized_changed and pre_hits == 0 and post_hits > 0:
                expected_section_change_status = "normalized_section_changed_with_post_only_public_law_marker"
            elif normalized_changed:
                expected_section_change_status = "normalized_section_changed_without_post_only_public_law_marker"
            elif pre_hits == 0 and post_hits > 0:
                expected_section_change_status = "normalized_section_unchanged_with_post_only_public_law_marker"
            else:
                expected_section_change_status = "normalized_section_unchanged_without_post_only_public_law_marker"
        elif pre_fetched or post_fetched:
            expected_section_change_status = "partial_annual_text_available_needs_manual_followup"
        else:
            expected_section_change_status = "annual_text_not_available_needs_manual_followup"
        if section_change_status != expected_section_change_status:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: section change cue status mismatch"
            )
        if normalized_hash_status == "pre_post_normalized_text_changed":
            normalized_text_change_rows += 1
            if not text_diff_row.get("first_changed_text_pre_window", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: missing pre first-change window"
                )
            if not text_diff_row.get("first_changed_text_post_window", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: missing post first-change window"
                )
        if (
            text_diff_row.get("first_changed_text_pre_window", "").strip()
            and text_diff_row.get("first_changed_text_post_window", "").strip()
        ):
            first_change_window_rows += 1
        context_count = parse_int(text_diff_row.get("post_public_law_context_count", ""))
        if context_count is None or context_count < 0:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid context count")
        if post_hits > 0:
            if context_count is None or context_count <= 0:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: missing post public-law context")
            snippets = text_diff_row.get("post_public_law_context_snippets", "")
            if text_diff_row.get("public_law_number", "") not in snippets:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: snippets must include public law number")
        priority = text_diff_row.get("manual_review_priority", "")
        if priority not in allowed_manual_review_priorities:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid manual review priority")
        if (
            section_change_status == "normalized_section_changed_with_post_only_public_law_marker"
            and priority != "priority_1_review_post_public_law_context_and_target_section"
        ):
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: priority mismatch")
        if (
            section_change_status == "normalized_section_changed_without_post_only_public_law_marker"
            and priority != "priority_1_review_section_text_change_without_public_law_marker"
        ):
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: priority mismatch")
        if text_diff_row.get("lineage_evidence_status", "") != "annual_text_diff_cue_scan_not_codified_lineage_evidence":
            failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: invalid lineage evidence status")
        evidence_layers = split_semicolon_values(text_diff_row, "evidence_layers")
        for layer in (
            "statutory_lineage_olrc_historical_scan",
            "official_olrc_annual_us_code_page",
            "bounded_annual_text_diff_cue_scan",
        ):
            if layer not in evidence_layers:
                failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: missing evidence layer {layer}")
        missing_links = split_semicolon_values(text_diff_row, "missing_links")
        if not STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: missing annual text-diff gap markers"
            )
        notes = text_diff_row.get("source_review_notes", "")
        if (
            "Automated annual text cue only" not in notes
            or "normalized text signatures" not in notes
            or "target-section text changes" not in notes
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: source_review_notes must require manual adjudication"
            )
        boundary = text_diff_row.get("claim_boundary", "")
        if (
            "Official OLRC annual-page text-diff cue scan only" not in boundary
            or "normalized section-text signatures" not in boundary
            or "do not establish source-reviewed codified U.S.C. lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: {bill_id}: claim boundary must reject text-diff overclaiming"
            )
    if sorted(annual_text_diff_ranks) != list(range(1, len(statutory_lineage_olrc_annual_text_diff) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: annual text-diff ranks must be contiguous")
    if post_only_text_diff_cues == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: no post-only public-law marker cues")
    if normalized_text_change_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: no normalized annual section text changes")
    if first_change_window_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}: no bounded first-change windows")

    required_statutory_adjudication_columns = {
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
        "pre_section_anchor_status",
        "post_section_anchor_status",
        "pre_public_law_reference_hits",
        "post_public_law_reference_hits",
        "public_law_reference_hit_delta",
        "normalized_text_hash_status",
        "section_change_cue_status",
        "post_public_law_context_count",
        "post_public_law_context_snippets",
        "first_changed_text_pre_window",
        "first_changed_text_post_window",
        "codified_lineage_marker",
        "lineage_adjudication_status",
        "lineage_marker_strength",
        "target_section_diff_status",
        "lineage_evidence_status",
        "evidence_layers",
        "missing_links",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_adjudication_raw:
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION_RAW}: no rows")
    missing_adjudication_raw_columns = (
        required_statutory_adjudication_columns - set(statutory_lineage_adjudication_raw[0])
    ) if statutory_lineage_adjudication_raw else required_statutory_adjudication_columns
    missing_adjudication_columns = (
        required_statutory_adjudication_columns - set(statutory_lineage_adjudication[0])
    )
    if missing_adjudication_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_ADJUDICATION_RAW}: missing columns "
            f"{sorted(missing_adjudication_raw_columns)}"
        )
    if missing_adjudication_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_ADJUDICATION}: missing columns "
            f"{sorted(missing_adjudication_columns)}"
        )
    if statutory_lineage_adjudication != statutory_lineage_adjudication_raw:
        failures.append(
            f"{STATUTORY_LINEAGE_ADJUDICATION}: report CSV must mirror "
            f"{STATUTORY_LINEAGE_ADJUDICATION_RAW}"
        )
    if not STATUTORY_LINEAGE_ADJUDICATION_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION_MD}: missing markdown report")
    else:
        adjudication_md = STATUTORY_LINEAGE_ADJUDICATION_MD.read_text()
        for phrase in (
            "codified-lineage marker evidence",
            "not a source-reviewed target-section text-diff report",
            "Rows with codified-lineage marker evidence",
            "Claim boundary",
        ):
            if phrase not in adjudication_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_ADJUDICATION_MD}: missing summary phrase {phrase!r}"
                )
        expected_adjudication_summary = (
            f"Adjudication rows: {len(statutory_lineage_adjudication)} / "
            f"{len(statutory_lineage_olrc_annual_text_diff)}"
        )
        if expected_adjudication_summary not in adjudication_md:
            failures.append(
                f"{STATUTORY_LINEAGE_ADJUDICATION_MD}: missing summary phrase "
                f"{expected_adjudication_summary!r}"
            )
    text_diff_by_rank = {
        row.get("text_diff_rank", "").strip(): row
        for row in statutory_lineage_olrc_annual_text_diff
        if row.get("text_diff_rank", "").strip()
    }
    adjudication_by_text_diff_rank = {
        row.get("text_diff_rank", "").strip(): row
        for row in statutory_lineage_adjudication
        if row.get("text_diff_rank", "").strip()
    }
    if len(adjudication_by_text_diff_rank) != len(statutory_lineage_adjudication):
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: duplicate text_diff_rank rows")
    if set(adjudication_by_text_diff_rank) != set(text_diff_by_rank):
        failures.append(
            "statutory-lineage adjudication/text-diff mismatch: "
            f"missing from adjudication={sorted(set(text_diff_by_rank) - set(adjudication_by_text_diff_rank))}, "
            f"extra={sorted(set(adjudication_by_text_diff_rank) - set(text_diff_by_rank))}"
        )
    allowed_adjudication_statuses = {
        "official_olrc_post_only_public_law_marker_with_pre_post_section_change",
        "official_olrc_post_only_public_law_marker_with_post_section_anchor_only",
        "no_official_olrc_post_only_public_law_marker",
    }
    allowed_marker_strengths = {
        "strong_official_marker",
        "moderate_official_marker",
        "not_adjudicated",
    }
    allowed_target_diff_statuses = {
        "automated_pre_post_section_change_cue_needs_source_reviewed_diff",
        "post_section_anchor_without_pre_anchor_needs_manual_added_section_review",
        "no_automated_target_section_diff_cue",
    }
    adjudication_ranks: list[int] = []
    marker_rows = 0
    marker_public_laws: set[str] = set()
    for adjudication_row in statutory_lineage_adjudication:
        rank = parse_int(adjudication_row.get("lineage_adjudication_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: invalid lineage_adjudication_rank")
        else:
            adjudication_ranks.append(rank)
        text_diff_row = text_diff_by_rank.get(adjudication_row.get("text_diff_rank", "").strip(), {})
        bill_id = adjudication_row.get("bill_id", "").strip()
        for field in (
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
            "pre_section_anchor_status",
            "post_section_anchor_status",
            "pre_public_law_reference_hits",
            "post_public_law_reference_hits",
            "public_law_reference_hit_delta",
            "normalized_text_hash_status",
            "section_change_cue_status",
            "post_public_law_context_count",
            "post_public_law_context_snippets",
            "first_changed_text_pre_window",
            "first_changed_text_post_window",
        ):
            if adjudication_row.get(field, "").strip() != text_diff_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}"
                )
        pre_hits = parse_int(adjudication_row.get("pre_public_law_reference_hits", "0")) or 0
        post_hits = parse_int(adjudication_row.get("post_public_law_reference_hits", "0")) or 0
        context_count = parse_int(adjudication_row.get("post_public_law_context_count", "0")) or 0
        expected_marker = (
            text_diff_row.get("pre_fetch_status") == "official_olrc_annual_section_page_fetched"
            and text_diff_row.get("post_fetch_status") == "official_olrc_annual_section_page_fetched"
            and adjudication_row.get("normalized_text_hash_status") == "pre_post_normalized_text_changed"
            and adjudication_row.get("section_change_cue_status") == "normalized_section_changed_with_post_only_public_law_marker"
            and pre_hits == 0
            and post_hits > 0
            and context_count > 0
            and adjudication_row.get("post_section_anchor_status") == "section_anchor_found"
        )
        marker = adjudication_row.get("codified_lineage_marker", "")
        if marker not in {"0", "1"}:
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: invalid codified_lineage_marker")
        if marker != ("1" if expected_marker else "0"):
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: marker flag mismatch")
        status = adjudication_row.get("lineage_adjudication_status", "")
        strength = adjudication_row.get("lineage_marker_strength", "")
        target_diff_status = adjudication_row.get("target_section_diff_status", "")
        if status not in allowed_adjudication_statuses:
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: invalid lineage_adjudication_status")
        if strength not in allowed_marker_strengths:
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: invalid lineage_marker_strength")
        if target_diff_status not in allowed_target_diff_statuses:
            failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: invalid target_section_diff_status")
        if marker == "1":
            marker_rows += 1
            marker_public_laws.add(adjudication_row.get("public_law_number", "").strip())
            expected_status = (
                "official_olrc_post_only_public_law_marker_with_pre_post_section_change"
                if adjudication_row.get("pre_section_anchor_status") == "section_anchor_found"
                else "official_olrc_post_only_public_law_marker_with_post_section_anchor_only"
            )
            expected_strength = (
                "strong_official_marker"
                if adjudication_row.get("pre_section_anchor_status") == "section_anchor_found"
                else "moderate_official_marker"
            )
            if status != expected_status:
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: adjudication status mismatch")
            if strength != expected_strength:
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: marker strength mismatch")
            if adjudication_row.get("lineage_evidence_status") != "official_olrc_codified_lineage_marker_evidence":
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: marker row has invalid evidence status")
            evidence_layers = split_semicolon_values(adjudication_row, "evidence_layers")
            for layer in (
                "official_olrc_public_law_marker_adjudication",
                "official_olrc_post_only_public_law_marker",
            ):
                if layer not in evidence_layers:
                    failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: missing evidence layer {layer}")
        else:
            if status != "no_official_olrc_post_only_public_law_marker":
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: non-marker status mismatch")
            if strength != "not_adjudicated":
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: non-marker strength mismatch")
            if adjudication_row.get("lineage_evidence_status") != "no_codified_lineage_marker_evidence":
                failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: non-marker evidence status mismatch")
        missing_links = split_semicolon_values(adjudication_row, "missing_links")
        if not STATUTORY_LINEAGE_ADJUDICATION_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: missing adjudication gap markers"
            )
        boundary = adjudication_row.get("claim_boundary", "")
        if (
            "Official OLRC public-law marker adjudication only" not in boundary
            or "source-reviewed target-section text diffs" not in boundary
            or "public-law causal attribution" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_ADJUDICATION}: {bill_id}: claim boundary must reject lineage overclaims"
            )
    if sorted(adjudication_ranks) != list(range(1, len(statutory_lineage_adjudication) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: adjudication ranks must be contiguous")
    if marker_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: no official OLRC marker rows")
    if not marker_public_laws:
        failures.append(f"{STATUTORY_LINEAGE_ADJUDICATION}: no public-law rows with marker evidence")

    required_target_review_packet_raw_columns = {
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
    }
    required_target_review_packet_columns = required_target_review_packet_raw_columns | {
        "target_section_diff_review_rank",
        "target_section_diff_review_status",
        "target_section_diff_review_relationship",
        "target_section_diff_review_notes",
    }
    if not statutory_lineage_target_review_packets_raw:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW}: no rows")
    missing_target_packet_raw_columns = (
        required_target_review_packet_raw_columns - set(statutory_lineage_target_review_packets_raw[0])
    ) if statutory_lineage_target_review_packets_raw else required_target_review_packet_raw_columns
    missing_target_packet_columns = (
        required_target_review_packet_columns - set(statutory_lineage_target_review_packets[0])
    )
    if missing_target_packet_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW}: missing columns "
            f"{sorted(missing_target_packet_raw_columns)}"
        )
    if missing_target_packet_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: missing columns "
            f"{sorted(missing_target_packet_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD}: missing markdown report")
    else:
        target_packet_md = STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD.read_text()
        expected_review_annotations = len(statutory_lineage_target_section_diff_review_raw)
        expected_source_reviewed_packet_rows = sum(
            1 for row in statutory_lineage_target_section_diff_review_raw
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        )
        for phrase in (
            "review infrastructure plus disposition context",
            "Review-ready packet rows",
            f"Target-section diff-review annotated rows: {expected_review_annotations}",
            f"Source-reviewed target-section diff rows: {expected_source_reviewed_packet_rows}",
            "Claim boundary",
        ):
            if phrase not in target_packet_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD}: missing summary phrase {phrase!r}"
                )
        expected_packet_summary = (
            f"Target review packet rows: {len(statutory_lineage_target_review_packets)} / "
            f"{len(statutory_lineage_adjudication)}"
        )
        if expected_packet_summary not in target_packet_md:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_MD}: missing summary phrase "
                f"{expected_packet_summary!r}"
            )
    adjudication_by_rank = {
        row.get("lineage_adjudication_rank", "").strip(): row
        for row in statutory_lineage_adjudication
        if row.get("lineage_adjudication_rank", "").strip()
    }
    target_packet_by_adjudication_rank = {
        row.get("lineage_adjudication_rank", "").strip(): row
        for row in statutory_lineage_target_review_packets
        if row.get("lineage_adjudication_rank", "").strip()
    }
    raw_target_packet_by_rank = {
        row.get("target_review_packet_rank", "").strip(): row
        for row in statutory_lineage_target_review_packets_raw
        if row.get("target_review_packet_rank", "").strip()
    }
    raw_diff_review_by_packet_rank = {
        row.get("target_review_packet_rank", "").strip(): row
        for row in statutory_lineage_target_section_diff_review_raw
        if row.get("target_review_packet_rank", "").strip()
    }
    if len(target_packet_by_adjudication_rank) != len(statutory_lineage_target_review_packets):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: duplicate lineage_adjudication_rank rows")
    if len(raw_target_packet_by_rank) != len(statutory_lineage_target_review_packets_raw):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW}: duplicate target_review_packet_rank rows")
    if len(raw_diff_review_by_packet_rank) != len(statutory_lineage_target_section_diff_review_raw):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW}: duplicate target_review_packet_rank rows")
    if {row.get("target_review_packet_rank", "").strip() for row in statutory_lineage_target_review_packets} != set(raw_target_packet_by_rank):
        failures.append(
            "statutory-lineage target-review packet raw/report mismatch: "
            f"missing from report={sorted(set(raw_target_packet_by_rank) - {row.get('target_review_packet_rank', '').strip() for row in statutory_lineage_target_review_packets})}, "
            f"extra={sorted({row.get('target_review_packet_rank', '').strip() for row in statutory_lineage_target_review_packets} - set(raw_target_packet_by_rank))}"
        )
    if set(target_packet_by_adjudication_rank) != set(adjudication_by_rank):
        failures.append(
            "statutory-lineage target-review/adjudication mismatch: "
            f"missing from packets={sorted(set(adjudication_by_rank) - set(target_packet_by_adjudication_rank))}, "
            f"extra={sorted(set(target_packet_by_adjudication_rank) - set(adjudication_by_rank))}"
        )
    target_packet_ranks: list[int] = []
    review_ready_packet_rows = 0
    source_reviewed_diff_rows = 0
    allowed_packet_statuses = {
        "pre_post_target_section_review_packet_ready",
        "added_or_relocated_section_review_packet_ready",
        "target_section_review_packet_needs_manual_source_retrieval",
    }
    allowed_packet_strengths = {
        "strong_pre_post_anchor_review_packet",
        "moderate_post_anchor_review_packet",
        "not_review_ready",
    }
    for packet_row in statutory_lineage_target_review_packets:
        rank = parse_int(packet_row.get("target_review_packet_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: invalid target_review_packet_rank")
        else:
            target_packet_ranks.append(rank)
        rank_key = packet_row.get("target_review_packet_rank", "").strip()
        raw_packet_row = raw_target_packet_by_rank.get(rank_key, {})
        review_input_row = raw_diff_review_by_packet_rank.get(rank_key, {})
        adjudication_row = adjudication_by_rank.get(
            packet_row.get("lineage_adjudication_rank", "").strip(),
            {},
        )
        bill_id = packet_row.get("bill_id", "").strip()
        text_diff_row = text_diff_by_rank.get(packet_row.get("text_diff_rank", "").strip(), {})
        for field in (
            required_target_review_packet_raw_columns
            - {
                "source_reviewed_target_section_diff",
                "source_review_disposition",
                "lineage_evidence_status",
                "evidence_layers",
                "missing_links",
                "source_review_notes",
                "claim_boundary",
            }
        ):
            if packet_row.get(field, "").strip() != raw_packet_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS_RAW}"
                )
        for field in (
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
            "pre_section_anchor_status",
            "post_section_anchor_status",
            "pre_public_law_reference_hits",
            "post_public_law_reference_hits",
            "public_law_reference_hit_delta",
            "normalized_text_hash_status",
            "section_change_cue_status",
            "post_public_law_context_count",
            "post_public_law_context_snippets",
            "first_changed_text_pre_window",
            "first_changed_text_post_window",
            "codified_lineage_marker",
            "lineage_adjudication_status",
            "lineage_marker_strength",
            "target_section_diff_status",
        ):
            if packet_row.get(field, "").strip() != adjudication_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_ADJUDICATION}"
                )
        for field in (
            "pre_text_sha256",
            "post_text_sha256",
            "pre_normalized_text_sha256",
            "post_normalized_text_sha256",
            "normalized_text_char_delta",
        ):
            if packet_row.get(field, "").strip() != text_diff_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}"
                )
        expected_reviewed = review_input_row.get("source_reviewed_target_section_diff", "0").strip() or "0"
        expected_disposition = (
            review_input_row.get("review_status", "").strip()
            if review_input_row
            else "not_source_reviewed_review_packet_only"
        )
        if packet_row.get("source_reviewed_target_section_diff", "").strip() != expected_reviewed:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: "
                "source-reviewed packet flag must match diff-review input"
            )
        if packet_row.get("source_review_disposition", "").strip() != expected_disposition:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: invalid source_review_disposition"
            )
        if review_input_row:
            expected_review_fields = {
                "target_section_diff_review_rank": review_input_row.get("review_rank", "").strip(),
                "target_section_diff_review_status": review_input_row.get("review_status", "").strip(),
                "target_section_diff_review_relationship": review_input_row.get(
                    "codified_lineage_relationship", ""
                ).strip(),
                "target_section_diff_review_notes": review_input_row.get("source_review_notes", "").strip(),
            }
        else:
            expected_review_fields = {
                "target_section_diff_review_rank": "",
                "target_section_diff_review_status": "",
                "target_section_diff_review_relationship": "",
                "target_section_diff_review_notes": "",
            }
        for field, expected in expected_review_fields.items():
            if packet_row.get(field, "").strip() != expected:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: {field} "
                    "does not match diff-review annotation"
                )
        if packet_row.get("source_reviewed_target_section_diff", "") == "1":
            source_reviewed_diff_rows += 1
        has_post_context = (parse_int(packet_row.get("post_public_law_context_count", "0")) or 0) > 0
        has_change_windows = bool(
            packet_row.get("first_changed_text_pre_window", "").strip()
            and packet_row.get("first_changed_text_post_window", "").strip()
        )
        marker = packet_row.get("codified_lineage_marker", "") == "1"
        pre_anchor = packet_row.get("pre_section_anchor_status", "") == "section_anchor_found"
        post_anchor = packet_row.get("post_section_anchor_status", "") == "section_anchor_found"
        changed = packet_row.get("normalized_text_hash_status", "") == "pre_post_normalized_text_changed"
        if marker and pre_anchor and post_anchor and changed and has_change_windows and has_post_context:
            expected_status = "pre_post_target_section_review_packet_ready"
            expected_strength = "strong_pre_post_anchor_review_packet"
        elif marker and post_anchor and changed and has_change_windows and has_post_context:
            expected_status = "added_or_relocated_section_review_packet_ready"
            expected_strength = "moderate_post_anchor_review_packet"
        else:
            expected_status = "target_section_review_packet_needs_manual_source_retrieval"
            expected_strength = "not_review_ready"
        if packet_row.get("target_review_packet_status", "") not in allowed_packet_statuses:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: invalid packet status")
        if packet_row.get("target_review_packet_strength", "") not in allowed_packet_strengths:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: invalid packet strength")
        if packet_row.get("target_review_packet_status", "") != expected_status:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: packet status mismatch")
        if packet_row.get("target_review_packet_strength", "") != expected_strength:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: packet strength mismatch")
        if expected_status != "target_section_review_packet_needs_manual_source_retrieval":
            review_ready_packet_rows += 1
            if expected_reviewed == "1":
                expected_lineage_evidence_status = "source_reviewed_target_section_diff_attached"
            elif (
                review_input_row
                and review_input_row.get("review_status", "").strip()
                == "reviewed_related_section_context_no_exact_target_diff"
            ):
                expected_lineage_evidence_status = "reviewed_related_section_no_exact_target_diff_attached"
            elif review_input_row:
                expected_lineage_evidence_status = "reviewed_target_section_diff_unresolved_attached"
            else:
                expected_lineage_evidence_status = "review_packet_only_not_source_reviewed_lineage_evidence"
            if packet_row.get("lineage_evidence_status", "") != expected_lineage_evidence_status:
                failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: invalid ready evidence status")
        evidence_layers = split_semicolon_values(packet_row, "evidence_layers")
        if "statutory_lineage_target_section_review_packet" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: missing packet evidence layer")
        if review_input_row and "statutory_lineage_target_section_diff_review" not in evidence_layers:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: missing diff-review evidence layer")
        if expected_reviewed == "1" and "statutory_lineage_source_reviewed_target_section_diff" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: "
                "missing source-reviewed target-section diff evidence layer"
            )
        packet_components = split_semicolon_values(packet_row, "review_packet_components")
        for component in (
            "pre_olrc_annual_url",
            "post_olrc_annual_url",
            "pre_post_source_hashes",
            "normalized_section_text_hashes",
            "post_public_law_context_snippets",
            "first_changed_text_windows",
        ):
            if component not in packet_components:
                failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: missing packet component {component}")
        missing_links = split_semicolon_values(packet_row, "missing_links")
        required_packet_missing_links = set(STATUTORY_LINEAGE_TARGET_REVIEW_PACKET_MISSING_LINKS)
        if review_input_row:
            required_packet_missing_links.discard("human_source_review_disposition")
        if expected_reviewed == "1":
            required_packet_missing_links.discard("source_reviewed_target_section_diff")
        if not required_packet_missing_links <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: missing packet gap markers"
            )
        boundary = packet_row.get("claim_boundary", "")
        if (
            "Official OLRC target-section review packet plus downstream review disposition annotation only" not in boundary
            or "curated target-section diff-review status" not in boundary
            or "public-law causal attribution" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: {bill_id}: claim boundary must reject packet overclaims"
            )
    if sorted(target_packet_ranks) != list(range(1, len(statutory_lineage_target_review_packets) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: packet ranks must be contiguous")
    if review_ready_packet_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: expected at least one review-ready packet")
    expected_source_reviewed_packet_rows = sum(
        1 for row in statutory_lineage_target_section_diff_review_raw
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
    )
    if source_reviewed_diff_rows != expected_source_reviewed_packet_rows:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}: source-reviewed diff rows "
            f"{source_reviewed_diff_rows} != expected {expected_source_reviewed_packet_rows}"
        )

    required_target_section_diff_review_columns = {
        "review_rank",
        "target_review_packet_rank",
        "lineage_adjudication_rank",
        "text_diff_rank",
        "bill_id",
        "public_law_number",
        "enacted_date",
        "target_reference",
        "target_reference_type",
        "normalized_title",
        "normalized_section",
        "pre_edition",
        "post_edition",
        "review_status",
        "source_reviewed_target_section_diff",
        "codified_lineage_relationship",
        "public_law_source_url",
        "pre_olrc_url",
        "post_olrc_url",
        "pre_text_sha256",
        "post_text_sha256",
        "pre_normalized_text_sha256",
        "post_normalized_text_sha256",
        "pre_section_anchor_status",
        "post_section_anchor_status",
        "post_public_law_context_count",
        "public_law_source_summary",
        "pre_olrc_source_summary",
        "post_olrc_source_summary",
        "target_section_diff_summary",
        "public_law_causal_attribution",
        "law_revision_effective_text_reviewed",
        "source_review_notes",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    required_target_section_diff_review_raw_columns = {
        "review_rank",
        "target_review_packet_rank",
        "bill_id",
        "public_law_number",
        "target_reference",
        "review_status",
        "source_reviewed_target_section_diff",
        "codified_lineage_relationship",
        "public_law_source_url",
        "pre_olrc_url",
        "post_olrc_url",
        "public_law_source_summary",
        "pre_olrc_source_summary",
        "post_olrc_source_summary",
        "target_section_diff_summary",
        "public_law_causal_attribution",
        "law_revision_effective_text_reviewed",
        "source_review_notes",
        "claim_boundary",
    }
    if not statutory_lineage_target_section_diff_review_raw:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW}: no rows")
    missing_diff_review_raw_columns = (
        required_target_section_diff_review_raw_columns
        - set(statutory_lineage_target_section_diff_review_raw[0])
    ) if statutory_lineage_target_section_diff_review_raw else required_target_section_diff_review_raw_columns
    missing_diff_review_columns = (
        required_target_section_diff_review_columns
        - set(statutory_lineage_target_section_diff_review[0])
    )
    if missing_diff_review_raw_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW}: missing columns "
            f"{sorted(missing_diff_review_raw_columns)}"
        )
    if missing_diff_review_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: missing columns "
            f"{sorted(missing_diff_review_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MD}: missing markdown report")
    else:
        diff_review_md = STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MD.read_text()
        for phrase in (
            "bounded source-reviewed pilot",
            "Source-reviewed target-section diff rows",
            "Reviewed but unresolved/insufficient rows",
            "Claim boundary",
        ):
            if phrase not in diff_review_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    packet_by_rank = {
        row.get("target_review_packet_rank", "").strip(): row
        for row in statutory_lineage_target_review_packets
        if row.get("target_review_packet_rank", "").strip()
    }
    raw_diff_review_by_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_target_section_diff_review_raw
        if row.get("review_rank", "").strip()
    }
    report_diff_review_by_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_target_section_diff_review
        if row.get("review_rank", "").strip()
    }
    if len(raw_diff_review_by_rank) != len(statutory_lineage_target_section_diff_review_raw):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_RAW}: duplicate review_rank rows")
    if len(report_diff_review_by_rank) != len(statutory_lineage_target_section_diff_review):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: duplicate review_rank rows")
    if set(raw_diff_review_by_rank) != set(report_diff_review_by_rank):
        failures.append(
            "statutory-lineage target-section diff review raw/report mismatch: "
            f"missing from report={sorted(set(raw_diff_review_by_rank) - set(report_diff_review_by_rank))}, "
            f"extra={sorted(set(report_diff_review_by_rank) - set(raw_diff_review_by_rank))}"
        )
    allowed_diff_review_statuses = {
        "reviewed_added_target_section_diff",
        "reviewed_pre_post_target_section_diff",
        "reviewed_related_section_context_no_exact_target_diff",
        "reviewed_target_section_cue_insufficient",
    }
    positive_diff_review_statuses = {
        "reviewed_added_target_section_diff",
        "reviewed_pre_post_target_section_diff",
    }
    diff_review_ranks: list[int] = []
    diff_review_positive_rows = 0
    diff_review_non_positive_rows = 0
    for review_row in statutory_lineage_target_section_diff_review:
        rank = parse_int(review_row.get("review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: invalid review_rank")
        else:
            diff_review_ranks.append(rank)
        raw_row = raw_diff_review_by_rank.get(review_row.get("review_rank", "").strip(), {})
        packet_row = packet_by_rank.get(review_row.get("target_review_packet_rank", "").strip(), {})
        if not packet_row:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: {review_row.get('review_rank', '')}: "
                "target_review_packet_rank not found"
            )
            continue
        for field in (
            "target_review_packet_rank",
            "bill_id",
            "public_law_number",
            "target_reference",
            "pre_olrc_url",
            "post_olrc_url",
            "review_status",
            "source_reviewed_target_section_diff",
            "codified_lineage_relationship",
            "public_law_source_url",
            "public_law_source_summary",
            "pre_olrc_source_summary",
            "post_olrc_source_summary",
            "target_section_diff_summary",
            "public_law_causal_attribution",
            "law_revision_effective_text_reviewed",
            "source_review_notes",
        ):
            if review_row.get(field, "").strip() != raw_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                    f"{review_row.get('review_rank', '')}: {field} does not match raw review input"
                )
        for field in (
            "lineage_adjudication_rank",
            "text_diff_rank",
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
            "post_public_law_context_count",
        ):
            if review_row.get(field, "").strip() != packet_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                    f"{review_row.get('review_rank', '')}: {field} does not match review packet"
                )
        status = review_row.get("review_status", "").strip()
        if status not in allowed_diff_review_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: invalid review_status"
            )
        expected_reviewed = "1" if status in positive_diff_review_statuses else "0"
        if review_row.get("source_reviewed_target_section_diff", "").strip() != expected_reviewed:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: source-reviewed flag mismatch"
            )
        if expected_reviewed == "1":
            diff_review_positive_rows += 1
        else:
            diff_review_non_positive_rows += 1
            if "source_reviewed_target_section_diff" not in review_row.get("missing_links", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                    f"{review_row.get('review_rank', '')}: non-positive row must preserve diff gap"
                )
        evidence_layers = split_semicolon_values(review_row, "evidence_layers")
        if "statutory_lineage_target_section_diff_review" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: missing diff review evidence layer"
            )
        if expected_reviewed == "1" and "statutory_lineage_source_reviewed_target_section_diff" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: missing source-reviewed diff evidence layer"
            )
        missing_links = split_semicolon_values(review_row, "missing_links")
        if not STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW_MISSING_LINKS <= missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: missing diff-review gap markers"
            )
        boundary = review_row.get("claim_boundary", "")
        if (
            "Source-reviewed official OLRC/GovInfo target-section diff disposition only" not in boundary
            or "exclusive public-law causal attribution" not in boundary
            or "law-revision effective text" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: "
                f"{review_row.get('review_rank', '')}: claim boundary must reject review overclaims"
            )
    if sorted(diff_review_ranks) != list(range(1, len(statutory_lineage_target_section_diff_review) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: review ranks must be contiguous")
    if diff_review_positive_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: expected at least one source-reviewed diff")
    if diff_review_non_positive_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}: expected at least one non-positive reviewed row")

    required_target_lifecycle_bridge_columns = {
        "bridge_rank",
        "review_rank",
        "target_review_packet_rank",
        "bill_id",
        "public_law_number",
        "enacted_date",
        "target_reference",
        "target_reference_type",
        "target_section_key",
        "target_base_section_key",
        "target_subsection",
        "target_reference_key",
        "normalized_title",
        "normalized_section",
        "target_is_note",
        "review_status",
        "source_reviewed_target_section_diff",
        "codified_lineage_relationship",
        "target_lifecycle_status",
        "bridge_evidence_grade",
        "authority_base_section_match",
        "authority_base_section_citations",
        "authority_exact_target_reference_match",
        "authority_exact_target_reference_citations",
        "public_law_authority_rule_rows",
        "public_law_authority_text_verified_rows",
        "public_law_authority_document_numbers",
        "public_law_authority_usc_citation_count",
        "implementation_history_final_rule_rows",
        "implementation_history_matched_final_rule_rows",
        "implementation_history_proposed_rule_links",
        "implementation_history_proposed_document_numbers",
        "implementation_comment_metadata_rows",
        "implementation_comment_metadata_statuses",
        "implementation_comment_metadata_final_comment_count_rows",
        "implementation_comment_metadata_final_comment_count_total",
        "implementation_comment_metadata_proposed_comment_url_count",
        "implementation_comment_metadata_proposed_comment_urls",
        "court_base_section_overlap",
        "court_base_section_overlap_case_count",
        "court_base_section_overlap_case_ids",
        "court_base_section_overlap_usc_sections",
        "court_exact_target_reference_overlap",
        "court_exact_target_reference_case_count",
        "court_exact_target_reference_case_ids",
        "raw_scdb_target_base_section_overlap",
        "raw_scdb_target_base_section_case_count",
        "raw_scdb_target_base_section_case_ids",
        "raw_scdb_target_base_section_usc_sections",
        "raw_scdb_target_base_section_pre_enactment_case_count",
        "raw_scdb_target_base_section_post_enactment_case_count",
        "raw_scdb_target_base_section_missing_date_case_count",
        "raw_scdb_target_base_section_decision_range",
        "raw_scdb_target_reference_overlap",
        "raw_scdb_target_reference_case_count",
        "raw_scdb_target_reference_case_ids",
        "raw_scdb_target_reference_post_enactment_case_count",
        "public_law_court_overlap_case_count",
        "public_law_court_overlap_case_ids",
        "public_law_court_overlap_usc_sections",
        "public_law_direct_review_rows",
        "public_law_direct_review_direct_rows",
        "public_law_direct_review_not_direct_rows",
        "public_law_direct_review_determinations",
        "spine_evidence_layers",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_target_lifecycle_columns = (
        required_target_lifecycle_bridge_columns - set(statutory_lineage_target_lifecycle_bridge[0])
    )
    if missing_target_lifecycle_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: missing columns "
            f"{sorted(missing_target_lifecycle_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE_MD}: missing markdown report")
    else:
        lifecycle_bridge_md = STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE_MD.read_text()
        for phrase in (
            "Target-section bridge rows",
            "Rows with public-law lifecycle context",
            "Rows with authority base U.S.C. section overlap",
            "Rows with exact authority target-reference overlap",
            "Rows with exact court target-reference overlap",
            "Rows with raw SCDB target base-section overlap",
            "Raw SCDB post-enactment target base-section case attachments",
            "Claim boundary",
        ):
            if phrase not in lifecycle_bridge_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE_MD}: missing summary phrase {phrase!r}"
                )
    bridge_by_review_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_target_lifecycle_bridge
        if row.get("review_rank", "").strip()
    }
    if len(bridge_by_review_rank) != len(statutory_lineage_target_lifecycle_bridge):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: duplicate review_rank rows")
    if set(bridge_by_review_rank) != set(report_diff_review_by_rank):
        failures.append(
            "statutory-lineage target lifecycle bridge/diff review mismatch: "
            f"missing from bridge={sorted(set(report_diff_review_by_rank) - set(bridge_by_review_rank))}, "
            f"extra={sorted(set(bridge_by_review_rank) - set(report_diff_review_by_rank))}"
        )
    allowed_lifecycle_statuses = {
        "reviewed_related_section_context_no_exact_target_diff",
        "reviewed_target_diff_unresolved",
        "target_diff_with_exact_authority_and_court_target_reference_context",
        "target_diff_with_exact_authority_target_reference_context",
        "target_diff_with_exact_court_target_reference_overlap",
        "target_diff_with_authority_and_court_base_section_context",
        "target_diff_with_authority_base_section_context",
        "target_diff_with_court_base_section_context",
        "target_diff_with_public_law_lifecycle_context_only",
        "target_diff_without_lifecycle_context",
    }
    allowed_bridge_grades = {
        "exact_target_reference_context",
        "base_section_context",
        "public_law_context_only",
        "reviewed_no_exact_target_diff",
        "unresolved_review",
        "no_lifecycle_context",
    }
    bridge_ranks: list[int] = []
    bridge_base_context_rows = 0
    bridge_public_law_context_rows = 0
    for bridge_row in statutory_lineage_target_lifecycle_bridge:
        rank = parse_int(bridge_row.get("bridge_rank", ""))
        if rank is None or rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: invalid bridge_rank")
        else:
            bridge_ranks.append(rank)
        review_rank = bridge_row.get("review_rank", "").strip()
        review_row = report_diff_review_by_rank.get(review_rank, {})
        for field in (
            "review_rank",
            "target_review_packet_rank",
            "bill_id",
            "public_law_number",
            "enacted_date",
            "target_reference",
            "target_reference_type",
            "normalized_title",
            "normalized_section",
            "review_status",
            "source_reviewed_target_section_diff",
            "codified_lineage_relationship",
        ):
            if bridge_row.get(field, "").strip() != review_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    f"{field} does not match target-section diff review"
                )
        status = bridge_row.get("target_lifecycle_status", "")
        grade = bridge_row.get("bridge_evidence_grade", "")
        if status not in allowed_lifecycle_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: invalid lifecycle status"
            )
        if grade not in allowed_bridge_grades:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: invalid bridge evidence grade"
            )
        authority_base = bridge_row.get("authority_base_section_match", "")
        authority_exact = bridge_row.get("authority_exact_target_reference_match", "")
        court_base = bridge_row.get("court_base_section_overlap", "")
        court_exact = bridge_row.get("court_exact_target_reference_overlap", "")
        raw_scdb_base = bridge_row.get("raw_scdb_target_base_section_overlap", "")
        raw_scdb_exact = bridge_row.get("raw_scdb_target_reference_overlap", "")
        if (
            authority_base not in {"0", "1"}
            or authority_exact not in {"0", "1"}
            or court_base not in {"0", "1"}
            or court_exact not in {"0", "1"}
            or raw_scdb_base not in {"0", "1"}
            or raw_scdb_exact not in {"0", "1"}
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: overlap flags must be 0/1"
            )
        if authority_base == "1":
            bridge_base_context_rows += 1
            if not bridge_row.get("authority_base_section_citations", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority base-section match missing citation pointer"
                )
            if "target_base_section_authority_usc_overlap" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority base-section match missing evidence layer"
                )
        elif bridge_row.get("authority_base_section_citations", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "authority base-section citation pointer present without base-section flag"
            )
        if authority_exact == "1":
            if authority_base != "1":
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority exact target-reference match must also have a base-section match"
                )
            if not bridge_row.get("authority_exact_target_reference_citations", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority exact target-reference match missing citation pointer"
                )
            if "target_reference_authority_usc_overlap" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority exact target-reference match missing evidence layer"
                )
        elif bridge_row.get("authority_exact_target_reference_citations", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "authority exact target-reference pointer present without exact-match flag"
            )
        if court_base == "1":
            bridge_base_context_rows += 1
            if parse_int(bridge_row.get("court_base_section_overlap_case_count", "0")) in {None, 0}:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court base-section match missing case count"
                )
            if not bridge_row.get("court_base_section_overlap_case_ids", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court base-section match missing case pointers"
                )
            if "target_base_section_court_usc_overlap" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court base-section match missing evidence layer"
                )
        elif bridge_row.get("court_base_section_overlap_case_ids", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "court base-section case pointers present without base-section flag"
            )
        if court_exact == "1":
            if court_base != "1":
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court exact target-reference match must also have a base-section match"
                )
            if parse_int(bridge_row.get("court_exact_target_reference_case_count", "0")) in {None, 0}:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court exact target-reference match missing case count"
                )
            if not bridge_row.get("court_exact_target_reference_case_ids", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court exact target-reference match missing case pointers"
                )
            if "target_reference_court_usc_overlap" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "court exact target-reference match missing evidence layer"
                )
        elif bridge_row.get("court_exact_target_reference_case_ids", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "court exact target-reference case pointers present without exact-match flag"
            )
        if raw_scdb_base == "1":
            if parse_int(bridge_row.get("raw_scdb_target_base_section_case_count", "0")) in {None, 0}:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB base-section overlap missing case count"
                )
            if not bridge_row.get("raw_scdb_target_base_section_case_ids", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB base-section overlap missing case pointers"
                )
            if not bridge_row.get("raw_scdb_target_base_section_usc_sections", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB base-section overlap missing section pointers"
                )
            if "raw_scdb_target_base_section_overlap_context" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB base-section overlap missing evidence layer"
                )
            if "source_reviewed_raw_scdb_target_section_disposition" not in split_semicolon_values(
                bridge_row, "missing_links"
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB overlap missing source-review gap marker"
                )
        elif (
            bridge_row.get("raw_scdb_target_base_section_case_ids", "").strip()
            or bridge_row.get("raw_scdb_target_base_section_usc_sections", "").strip()
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "raw SCDB base-section pointers present without base-section flag"
            )
        if raw_scdb_exact == "1":
            if raw_scdb_base != "1":
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB exact target-reference overlap must also have a raw base-section overlap"
                )
            if parse_int(bridge_row.get("raw_scdb_target_reference_case_count", "0")) in {None, 0}:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB exact target-reference overlap missing case count"
                )
            if not bridge_row.get("raw_scdb_target_reference_case_ids", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB exact target-reference overlap missing case pointers"
                )
            if "raw_scdb_target_reference_overlap_context" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "raw SCDB exact target-reference overlap missing evidence layer"
                )
        elif bridge_row.get("raw_scdb_target_reference_case_ids", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "raw SCDB exact target-reference case pointers present without exact flag"
            )
        if grade == "exact_target_reference_context" and authority_exact != "1" and court_exact != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "exact_target_reference_context grade needs an exact authority or court flag"
            )
        if grade == "base_section_context" and authority_base != "1" and court_base != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "base_section_context grade needs a base authority or court flag"
            )
        if grade == "public_law_context_only":
            bridge_public_law_context_rows += 1
        if bridge_row.get("source_reviewed_target_section_diff", "") != "1":
            if bridge_row.get("review_status", "").strip() == "reviewed_related_section_context_no_exact_target_diff":
                if (
                    status != "reviewed_related_section_context_no_exact_target_diff"
                    or grade != "reviewed_no_exact_target_diff"
                ):
                    failures.append(
                        f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                        "reviewed no-exact-target row should preserve no-exact-target bridge status"
                    )
            elif status != "reviewed_target_diff_unresolved" or grade != "unresolved_review":
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "unreviewed diff row should stay unresolved"
                )
        for field in (
            "public_law_authority_rule_rows",
            "public_law_authority_text_verified_rows",
            "public_law_authority_usc_citation_count",
            "implementation_history_final_rule_rows",
            "implementation_history_matched_final_rule_rows",
            "implementation_history_proposed_rule_links",
            "implementation_comment_metadata_rows",
            "implementation_comment_metadata_final_comment_count_rows",
            "implementation_comment_metadata_final_comment_count_total",
            "implementation_comment_metadata_proposed_comment_url_count",
            "court_base_section_overlap_case_count",
            "court_exact_target_reference_case_count",
            "raw_scdb_target_base_section_case_count",
            "raw_scdb_target_base_section_pre_enactment_case_count",
            "raw_scdb_target_base_section_post_enactment_case_count",
            "raw_scdb_target_base_section_missing_date_case_count",
            "raw_scdb_target_reference_case_count",
            "raw_scdb_target_reference_post_enactment_case_count",
            "public_law_court_overlap_case_count",
            "public_law_direct_review_rows",
            "public_law_direct_review_direct_rows",
            "public_law_direct_review_not_direct_rows",
        ):
            value = parse_int(bridge_row.get(field, "0"))
            if value is None or value < 0:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    f"{field} must be a nonnegative integer"
                )
        if int(bridge_row.get("public_law_authority_text_verified_rows", "0") or "0") > 0:
            if "public_law_federal_register_authority_context" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "authority context missing evidence layer"
                )
        if int(bridge_row.get("public_law_direct_review_rows", "0") or "0") > 0:
            if "court_public_law_direct_review_disposition" not in bridge_row.get("evidence_layers", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "direct-review disposition context missing evidence layer"
                )
        raw_post_count = parse_int(bridge_row.get("raw_scdb_target_base_section_post_enactment_case_count", "0"))
        if raw_post_count is not None and raw_post_count > 0:
            evidence_layers = bridge_row.get("evidence_layers", "")
            missing_links_for_post = split_semicolon_values(bridge_row, "missing_links")
            if "raw_scdb_post_enactment_target_section_overlap_needs_source_review" not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "post-enactment raw SCDB overlap missing review-needed evidence layer"
                )
            if "source_reviewed_post_enactment_target_section_court_disposition" not in missing_links_for_post:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    "post-enactment raw SCDB overlap missing source-review gap marker"
                )
        missing_links = split_semicolon_values(bridge_row, "missing_links")
        for required_gap in (
            "public_law_causal_attribution",
            "law_revision_effective_text",
            "implementation_outcomes_or_enforcement",
            "direct_court_review_of_target_section",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                    f"missing bridge gap marker {required_gap}"
                )
        if authority_exact == "0" and "exact_target_reference_implementation_authority" not in missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "missing exact target-reference implementation-authority gap marker"
            )
        if court_exact == "0" and "exact_target_reference_court_overlap" not in missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "missing exact target-reference court-overlap gap marker"
            )
        boundary = bridge_row.get("claim_boundary", "")
        if (
            "Target-section lifecycle bridge only" not in boundary
            or "base U.S.C. section overlaps are metadata context" not in boundary
            or "not exact target-reference or subsection evidence" not in boundary
            or "Raw SCDB target-section overlaps are date-screened section-citation context" not in boundary
            or "Public-law-level rows remain context" not in boundary
            or "implementation outcomes" not in boundary
            or "direct court review of the target section" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: {review_rank}: "
                "claim boundary must reject lifecycle bridge overclaims"
            )
    if sorted(bridge_ranks) != list(range(1, len(statutory_lineage_target_lifecycle_bridge) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: bridge ranks must be contiguous")
    if bridge_base_context_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: expected at least one base-section context row")
    if bridge_public_law_context_rows == 0:
        failures.append(f"{STATUTORY_LINEAGE_TARGET_LIFECYCLE_BRIDGE}: expected at least one public-law context-only row")

    required_codified_progress_columns = {
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
    }
    missing_codified_progress_columns = (
        required_codified_progress_columns - set(statutory_lineage_codified_progress[0])
    )
    if missing_codified_progress_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: missing columns "
            f"{sorted(missing_codified_progress_columns)}"
        )
    if not STATUTORY_LINEAGE_CODIFIED_PROGRESS_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS_MD}: missing markdown report")
    else:
        codified_progress_md = STATUTORY_LINEAGE_CODIFIED_PROGRESS_MD.read_text()
        for phrase in (
            "Codified-lineage progress rows",
            "Public laws with source-reviewed target-section diff rows",
            "Reviewed no-structured-U.S.C.-target designation rows",
            "Claim boundary",
        ):
            if phrase not in codified_progress_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS_MD}: missing summary phrase {phrase!r}"
                )
    codified_progress_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in statutory_lineage_codified_progress
        if row.get("bill_id", "").strip()
    }
    if len(codified_progress_by_bill) != len(statutory_lineage_codified_progress):
        failures.append(f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: duplicate bill_id rows")
    progress_ranks: list[int] = []
    target_diff_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_section_diff_review:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            target_diff_rows_by_bill[bill_id].append(row)
    bridge_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_lifecycle_bridge:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            bridge_rows_by_bill[bill_id].append(row)
    for bill_id, progress_row in codified_progress_by_bill.items():
        progress_rank = parse_int(progress_row.get("progress_rank", ""))
        if progress_rank is None or progress_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: invalid progress_rank")
        else:
            progress_ranks.append(progress_rank)
        diff_rows_for_bill = target_diff_rows_by_bill.get(bill_id, [])
        bridge_rows_for_bill = bridge_rows_by_bill.get(bill_id, [])
        source_reviewed_count = sum(
            1 for row in diff_rows_for_bill
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        )
        no_exact_count = sum(
            1 for row in diff_rows_for_bill
            if row.get("review_status", "").strip()
            == "reviewed_related_section_context_no_exact_target_diff"
        )
        if parse_int(progress_row.get("target_diff_review_rows", "")) != len(diff_rows_for_bill):
            failures.append(
                f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: target diff row count mismatch"
            )
        if parse_int(progress_row.get("source_reviewed_target_section_diff_rows", "")) != source_reviewed_count:
            failures.append(
                f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: source-reviewed target diff count mismatch"
            )
        if parse_int(progress_row.get("reviewed_no_exact_target_section_diff_rows", "")) != no_exact_count:
            failures.append(
                f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: no-exact target diff count mismatch"
            )
        if parse_int(progress_row.get("target_lifecycle_bridge_rows", "")) != len(bridge_rows_for_bill):
            failures.append(
                f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: lifecycle bridge row count mismatch"
            )
        boundary = progress_row.get("claim_boundary", "")
        if (
            "Codified-lineage progress status only" not in boundary
            or "full codified lineage" not in boundary
            or "law-revision effective text" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: {bill_id}: "
                "claim boundary must reject full-lineage and validation claims"
            )
    if sorted(progress_ranks) != list(range(1, len(statutory_lineage_codified_progress) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_CODIFIED_PROGRESS}: progress ranks must be contiguous")

    required_effective_text_columns = {
        "effective_text_review_rank",
        "review_rank",
        "target_review_packet_rank",
        "text_diff_rank",
        "bill_id",
        "public_law_number",
        "enacted_date",
        "target_reference",
        "target_reference_type",
        "normalized_title",
        "normalized_section",
        "codified_lineage_relationship",
        "target_section_diff_review_status",
        "source_reviewed_target_section_diff",
        "pre_edition",
        "post_edition",
        "pre_olrc_url",
        "post_olrc_url",
        "current_olrc_url",
        "current_olrc_scan_status",
        "current_olrc_http_status",
        "current_official_text_sha256",
        "current_official_text_bytes",
        "current_section_heading",
        "current_public_law_reference_hits",
        "current_public_law_reference_status",
        "post_public_law_context_count",
        "pre_normalized_text_sha256",
        "post_normalized_text_sha256",
        "current_effective_text_review_status",
        "law_revision_effective_text_reviewed",
        "effective_text_source_basis",
        "effective_text_review_summary",
        "public_law_causal_attribution",
        "source_review_notes",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_effective_text_columns = (
        required_effective_text_columns - set(statutory_lineage_effective_text_review[0])
    )
    if missing_effective_text_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: missing columns "
            f"{sorted(missing_effective_text_columns)}"
        )
    if not STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW_MD}: missing markdown report")
    else:
        effective_text_md = STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW_MD.read_text()
        for phrase in (
            "Effective-text review rows",
            "Law-revision effective-text reviewed rows",
            "Current OLRC pages mentioning queued public law",
            "Public-law causal-attribution reviewed rows",
            "Claim boundary",
        ):
            if phrase not in effective_text_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    source_reviewed_diff_by_review_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_target_section_diff_review
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        and row.get("review_rank", "").strip()
    }
    effective_text_by_review_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_effective_text_review
        if row.get("review_rank", "").strip()
    }
    if len(effective_text_by_review_rank) != len(statutory_lineage_effective_text_review):
        failures.append(f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: duplicate review_rank rows")
    if set(effective_text_by_review_rank) != set(source_reviewed_diff_by_review_rank):
        failures.append(
            "statutory-lineage effective-text/source-reviewed diff mismatch: "
            f"missing from effective={sorted(set(source_reviewed_diff_by_review_rank) - set(effective_text_by_review_rank))[:10]}, "
            f"extra={sorted(set(effective_text_by_review_rank) - set(source_reviewed_diff_by_review_rank))[:10]}"
        )
    effective_text_review_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    effective_text_ranks: list[int] = []
    causal_attribution_review_rows = 0
    for review_rank, effective_row in effective_text_by_review_rank.items():
        diff_row = source_reviewed_diff_by_review_rank.get(review_rank, {})
        rank = parse_int(effective_row.get("effective_text_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: invalid rank"
            )
        else:
            effective_text_ranks.append(rank)
        bill_id = effective_row.get("bill_id", "").strip()
        if bill_id:
            effective_text_review_rows_by_bill[bill_id].append(effective_row)
        for field in (
            "target_review_packet_rank",
            "text_diff_rank",
            "bill_id",
            "public_law_number",
            "target_reference",
            "target_reference_type",
            "normalized_title",
            "normalized_section",
            "codified_lineage_relationship",
            "pre_edition",
            "post_edition",
            "pre_olrc_url",
            "post_olrc_url",
            "pre_normalized_text_sha256",
            "post_normalized_text_sha256",
        ):
            if effective_row.get(field, "").strip() != diff_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                    f"{field} does not match {STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}"
                )
        if effective_row.get("target_section_diff_review_status", "").strip() != diff_row.get("review_status", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "target-section diff status mismatch"
            )
        if effective_row.get("source_reviewed_target_section_diff", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "must only cover source-reviewed target-section diff rows"
            )
        if effective_row.get("law_revision_effective_text_reviewed", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "expected law-revision effective-text reviewed flag"
            )
        if (
            effective_row.get("current_olrc_scan_status", "").strip()
            != "official_olrc_current_section_page_fetched"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "current OLRC source must be fetched"
            )
        if effective_row.get("current_olrc_http_status", "").strip() != "200":
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "current OLRC source must have HTTP 200 status"
            )
        if parse_int(effective_row.get("current_official_text_bytes", "")) in {None, 0}:
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "current OLRC source must carry text bytes"
            )
        if not effective_row.get("current_official_text_sha256", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "current OLRC source must carry a text hash"
            )
        if (
            effective_row.get("current_public_law_reference_status", "").strip()
            != "current_page_mentions_public_law"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "expected current public-law note presence"
            )
        if parse_int(effective_row.get("current_public_law_reference_hits", "")) in {None, 0}:
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "expected positive current public-law reference hits"
            )
        if (
            effective_row.get("current_effective_text_review_status", "").strip()
            != "reviewed_current_effective_text_source_with_public_law_note"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "unexpected effective-text review status"
            )
        causal_status = effective_row.get("public_law_causal_attribution", "").strip()
        if causal_status != "not_reviewed_for_exclusive_public_law_causation":
            causal_attribution_review_rows += 1
        missing_links = split_semicolon_values(effective_row, "missing_links")
        for required_gap in (
            "complete_codified_usc_lineage_review",
            "public_law_causal_attribution",
            "implementation_outcomes",
            "direct_target_section_court_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                    f"missing gap marker {required_gap}"
                )
        if "law_revision_effective_text" in missing_links:
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "reviewed rows should not retain law-revision effective-text as a missing link"
            )
        if "statutory_lineage_effective_text_source_review" not in split_semicolon_values(effective_row, "evidence_layers"):
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "missing effective-text evidence layer"
            )
        boundary = effective_row.get("claim_boundary", "")
        if (
            "Law-revision effective-text source review only" not in boundary
            or "current public-law note presence" not in boundary
            or "does not establish exclusive public-law causal attribution" not in boundary
            or "complete codified lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: review {review_rank}: "
                "claim boundary must reject effective-text overclaims"
            )
    if sorted(effective_text_ranks) != list(range(1, len(statutory_lineage_effective_text_review) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: ranks must be contiguous")
    if causal_attribution_review_rows != 0:
        failures.append(
            f"{STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW}: causal-attribution reviews should remain zero"
        )

    required_public_law_attribution_columns = {
        "public_law_attribution_review_rank",
        "effective_text_review_rank",
        "review_rank",
        "target_review_packet_rank",
        "text_diff_rank",
        "bill_id",
        "public_law_number",
        "enacted_date",
        "target_reference",
        "target_reference_type",
        "normalized_title",
        "normalized_section",
        "codified_lineage_relationship",
        "target_section_diff_review_status",
        "source_reviewed_target_section_diff",
        "law_revision_effective_text_reviewed",
        "pre_edition",
        "post_edition",
        "public_law_source_url",
        "govinfo_package_id",
        "govinfo_text_url",
        "govinfo_details_url",
        "public_law_text_sha256",
        "public_law_text_bytes",
        "pre_olrc_url",
        "post_olrc_url",
        "current_olrc_url",
        "pre_normalized_text_sha256",
        "post_normalized_text_sha256",
        "annual_normalized_text_hash_status",
        "annual_normalized_text_char_delta",
        "annual_public_law_reference_hit_delta",
        "annual_post_public_law_context_count",
        "annual_automated_diff_cue_status",
        "annual_section_change_cue_status",
        "annual_manual_review_priority",
        "current_effective_text_review_status",
        "current_public_law_reference_status",
        "public_law_causal_attribution",
        "public_law_causal_attribution_reviewed",
        "attribution_source_basis",
        "attribution_review_summary",
        "source_review_notes",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_public_law_attribution_columns = (
        required_public_law_attribution_columns
        - set(statutory_lineage_public_law_attribution_review[0])
    )
    if missing_public_law_attribution_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: missing columns "
            f"{sorted(missing_public_law_attribution_columns)}"
        )
    if not STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW_MD}: missing markdown report")
    else:
        public_law_attribution_md = STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW_MD.read_text()
        for phrase in (
            "Public-law attribution review rows",
            "Public-law causal-attribution reviewed rows",
            "Official public-law text bytes represented",
            "Annual public-law marker hit delta represented",
            "Claim boundary",
        ):
            if phrase not in public_law_attribution_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    public_law_attribution_by_review_rank = {
        row.get("review_rank", "").strip(): row
        for row in statutory_lineage_public_law_attribution_review
        if row.get("review_rank", "").strip()
    }
    if len(public_law_attribution_by_review_rank) != len(statutory_lineage_public_law_attribution_review):
        failures.append(f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: duplicate review_rank rows")
    if set(public_law_attribution_by_review_rank) != set(source_reviewed_diff_by_review_rank):
        failures.append(
            "statutory-lineage public-law-attribution/source-reviewed diff mismatch: "
            f"missing from attribution={sorted(set(source_reviewed_diff_by_review_rank) - set(public_law_attribution_by_review_rank))[:10]}, "
            f"extra={sorted(set(public_law_attribution_by_review_rank) - set(source_reviewed_diff_by_review_rank))[:10]}"
        )
    annual_by_text_diff_rank = {
        row.get("text_diff_rank", "").strip(): row
        for row in statutory_lineage_olrc_annual_text_diff
        if row.get("text_diff_rank", "").strip()
    }
    source_scan_by_bill_public_law = {
        (
            row.get("bill_id", "").strip(),
            row.get("public_law_number", "").strip(),
        ): row
        for row in statutory_lineage_source_scan
        if row.get("bill_id", "").strip()
        and row.get("public_law_number", "").strip()
    }
    public_law_attribution_review_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    public_law_attribution_ranks: list[int] = []
    for review_rank, attribution_row in public_law_attribution_by_review_rank.items():
        diff_row = source_reviewed_diff_by_review_rank.get(review_rank, {})
        effective_row = effective_text_by_review_rank.get(review_rank, {})
        annual_row = annual_by_text_diff_rank.get(attribution_row.get("text_diff_rank", "").strip(), {})
        source_row = source_scan_by_bill_public_law.get((
            attribution_row.get("bill_id", "").strip(),
            attribution_row.get("public_law_number", "").strip(),
        ), {})
        rank = parse_int(attribution_row.get("public_law_attribution_review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: invalid rank"
            )
        else:
            public_law_attribution_ranks.append(rank)
        bill_id = attribution_row.get("bill_id", "").strip()
        if bill_id:
            public_law_attribution_review_rows_by_bill[bill_id].append(attribution_row)
        for field in (
            "target_review_packet_rank",
            "text_diff_rank",
            "bill_id",
            "public_law_number",
            "enacted_date",
            "target_reference",
            "target_reference_type",
            "normalized_title",
            "normalized_section",
            "codified_lineage_relationship",
            "pre_edition",
            "post_edition",
            "public_law_source_url",
            "pre_olrc_url",
            "post_olrc_url",
            "pre_normalized_text_sha256",
            "post_normalized_text_sha256",
        ):
            if attribution_row.get(field, "").strip() != diff_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                    f"{field} does not match {STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}"
                )
        if attribution_row.get("target_section_diff_review_status", "").strip() != diff_row.get("review_status", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "target-section diff status mismatch"
            )
        if attribution_row.get("effective_text_review_rank", "").strip() != effective_row.get("effective_text_review_rank", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "effective-text review rank mismatch"
            )
        if attribution_row.get("source_reviewed_target_section_diff", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "must only cover source-reviewed target-section diff rows"
            )
        if attribution_row.get("law_revision_effective_text_reviewed", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected effective-text reviewed flag"
            )
        if (
            attribution_row.get("current_effective_text_review_status", "").strip()
            != "reviewed_current_effective_text_source_with_public_law_note"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected current effective-text source review status"
            )
        if (
            attribution_row.get("current_public_law_reference_status", "").strip()
            != "current_page_mentions_public_law"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected current public-law note presence"
            )
        if attribution_row.get("current_olrc_url", "").strip() != effective_row.get("current_olrc_url", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "current OLRC URL must match effective-text review"
            )
        if source_row.get("source_review_status", "").strip() != "official_govinfo_public_law_text_scanned":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "official GovInfo public-law source scan is required"
            )
        if attribution_row.get("govinfo_package_id", "").strip() != source_row.get("govinfo_package_id", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "GovInfo package id mismatch"
            )
        if attribution_row.get("govinfo_text_url", "").strip() != source_row.get("govinfo_text_url", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "GovInfo text URL mismatch"
            )
        if attribution_row.get("govinfo_details_url", "").strip() != source_row.get("govinfo_details_url", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "GovInfo details URL mismatch"
            )
        if attribution_row.get("public_law_text_sha256", "").strip() != source_row.get("official_text_sha256", "").strip():
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "public-law text hash mismatch"
            )
        if parse_int(attribution_row.get("public_law_text_bytes", "")) in {None, 0}:
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "public-law text bytes must be positive"
            )
        for output_field, annual_field in (
            ("annual_normalized_text_hash_status", "normalized_text_hash_status"),
            ("annual_normalized_text_char_delta", "normalized_text_char_delta"),
            ("annual_public_law_reference_hit_delta", "public_law_reference_hit_delta"),
            ("annual_post_public_law_context_count", "post_public_law_context_count"),
            ("annual_automated_diff_cue_status", "automated_diff_cue_status"),
            ("annual_section_change_cue_status", "section_change_cue_status"),
            ("annual_manual_review_priority", "manual_review_priority"),
        ):
            if attribution_row.get(output_field, "").strip() != annual_row.get(annual_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                    f"{output_field} does not match {STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF}"
                )
        if attribution_row.get("annual_normalized_text_hash_status", "").strip() != "pre_post_normalized_text_changed":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected changed annual normalized text"
            )
        if (
            attribution_row.get("annual_automated_diff_cue_status", "").strip()
            != "post_only_public_law_marker_on_changed_annual_page"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected post-only public-law marker cue"
            )
        if (
            attribution_row.get("annual_section_change_cue_status", "").strip()
            != "normalized_section_changed_with_post_only_public_law_marker"
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected target-section change cue"
            )
        if parse_int(attribution_row.get("annual_public_law_reference_hit_delta", "")) in {None, 0}:
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "annual public-law reference delta must be positive"
            )
        if parse_int(attribution_row.get("annual_post_public_law_context_count", "")) in {None, 0}:
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "annual post public-law context count must be positive"
            )
        if attribution_row.get("public_law_causal_attribution", "").strip() != "reviewed_target_section_diff_attributed_to_queued_public_law":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "unexpected public-law attribution status"
            )
        if attribution_row.get("public_law_causal_attribution_reviewed", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "expected public-law attribution reviewed flag"
            )
        missing_links = split_semicolon_values(attribution_row, "missing_links")
        for required_gap in (
            "complete_codified_usc_lineage_review",
            "implementation_outcomes",
            "direct_target_section_court_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                    f"missing gap marker {required_gap}"
                )
        for closed_gap in ("law_revision_effective_text", "public_law_causal_attribution"):
            if closed_gap in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                    f"reviewed rows should not retain {closed_gap} as a missing link"
                )
        evidence_layers = split_semicolon_values(attribution_row, "evidence_layers")
        for required_layer in (
            "statutory_lineage_public_law_attribution_review",
            "official_govinfo_public_law_text_scan",
            "official_olrc_annual_us_code_text_diff",
            "statutory_lineage_effective_text_source_review",
        ):
            if required_layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                    f"missing evidence layer {required_layer}"
                )
        boundary = attribution_row.get("claim_boundary", "")
        if (
            "Target-section public-law attribution review only" not in boundary
            or "does not establish complete codified lineage" not in boundary
            or "exclusive current-section causation" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: review {review_rank}: "
                "claim boundary must reject attribution overclaims"
            )
    if sorted(public_law_attribution_ranks) != list(range(1, len(statutory_lineage_public_law_attribution_review) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW}: ranks must be contiguous")

    required_completion_queue_columns = {
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
    }
    missing_completion_queue_columns = (
        required_completion_queue_columns - set(statutory_lineage_completion_queue[0])
    )
    if missing_completion_queue_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: missing columns "
            f"{sorted(missing_completion_queue_columns)}"
        )
    if not STATUTORY_LINEAGE_COMPLETION_QUEUE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_COMPLETION_QUEUE_MD}: missing markdown report")
    else:
        completion_md = STATUTORY_LINEAGE_COMPLETION_QUEUE_MD.read_text()
        for phrase in (
            "Completion queue rows",
            "Active codified-lineage next-gate rows",
            "Public laws with law-revision effective text reviewed",
            "Public laws with public-law causal attribution reviewed",
            "Claim boundary",
        ):
            if phrase not in completion_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE_MD}: missing summary phrase {phrase!r}"
                )
    completion_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in statutory_lineage_completion_queue
        if row.get("bill_id", "").strip()
    }
    if len(completion_by_bill) != len(statutory_lineage_completion_queue):
        failures.append(f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: duplicate bill_id rows")
    if set(completion_by_bill) != set(codified_progress_by_bill):
        failures.append(
            "statutory-lineage completion/progress bill mismatch: "
            f"missing from completion={sorted(set(codified_progress_by_bill) - set(completion_by_bill))}, "
            f"extra={sorted(set(completion_by_bill) - set(codified_progress_by_bill))}"
        )
    completion_ranks: list[int] = []
    effective_text_reviewed_public_laws = 0
    causal_attribution_reviewed_public_laws = 0
    for bill_id, completion_row in completion_by_bill.items():
        progress_row = codified_progress_by_bill.get(bill_id, {})
        corpus_row = lifecycle_corpus_by_bill.get(bill_id, {})
        completion_rank = parse_int(completion_row.get("completion_rank", ""))
        if completion_rank is None or completion_rank <= 0:
            failures.append(f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: invalid completion_rank")
        else:
            completion_ranks.append(completion_rank)
        for field in (
            "action_rank",
            "public_law_number",
            "policy_area",
            "codified_progress_status",
            "target_diff_review_rows",
            "source_reviewed_target_section_diff_rows",
            "reviewed_no_exact_target_section_diff_rows",
            "reviewed_no_structured_usc_target_rows",
            "target_lifecycle_bridge_rows",
            "authority_exact_target_reference_rows",
            "authority_base_section_rows",
            "court_exact_target_reference_rows",
            "court_base_section_rows",
            "court_direct_review_status",
        ):
            if completion_row.get(field, "").strip() != progress_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: {field} "
                    f"does not match {STATUTORY_LINEAGE_CODIFIED_PROGRESS}"
                )
        if corpus_row:
            if completion_row.get("corpus_rank", "").strip() != corpus_row.get("corpus_rank", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: corpus_rank mismatch"
                )
            if (
                completion_row.get("next_actionable_upgrade_gate", "").strip()
                != corpus_row.get("next_actionable_upgrade_gate", "").strip()
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: next gate mismatch"
                )
        diff_rows_for_bill = target_diff_rows_by_bill.get(bill_id, [])
        source_reviewed_rows = [
            row for row in diff_rows_for_bill
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        effective_text_rows = [
            row for row in effective_text_review_rows_by_bill.get(bill_id, [])
            if row.get("law_revision_effective_text_reviewed", "").strip() == "1"
        ]
        causal_rows = [
            row for row in public_law_attribution_review_rows_by_bill.get(bill_id, [])
            if row.get("public_law_causal_attribution_reviewed", "").strip() == "1"
            and row.get("public_law_causal_attribution", "").strip()
            and row.get("public_law_causal_attribution", "").strip()
            != "not_reviewed_for_exclusive_public_law_causation"
        ]
        if causal_rows and len(causal_rows) != len([
            row for row in public_law_attribution_review_rows_by_bill.get(bill_id, [])
            if row.get("public_law_causal_attribution", "").strip()
            and row.get("public_law_causal_attribution", "").strip()
            != "not_reviewed_for_exclusive_public_law_causation"
        ]):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                "causal attribution reviewed flag mismatch"
            )
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
        if parse_int(completion_row.get("law_revision_effective_text_reviewed_rows", "")) != len(effective_text_rows):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: effective-text reviewed count mismatch"
            )
        if parse_int(completion_row.get("public_law_causal_attribution_reviewed_rows", "")) != len(causal_rows):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: causal attribution count mismatch"
            )
        if parse_int(completion_row.get("added_target_section_rows", "")) != len(added_rows):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: added target count mismatch"
            )
        if parse_int(completion_row.get("amended_existing_target_section_rows", "")) != len(amended_rows):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: amended target count mismatch"
            )
        if parse_int(completion_row.get("effective_date_note_rows", "")) != len(effective_date_note_rows):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: effective-date note count mismatch"
            )
        if effective_text_rows:
            effective_text_reviewed_public_laws += 1
        if causal_rows:
            causal_attribution_reviewed_public_laws += 1
        target_refs = {
            row.get("target_reference", "").strip()
            for row in diff_rows_for_bill
            if row.get("target_reference", "").strip()
        }
        if split_semicolon_values(completion_row, "target_references") != target_refs:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: target references mismatch"
            )
        relationship_values = {
            row.get("codified_lineage_relationship", "").strip()
            for row in diff_rows_for_bill
            if row.get("codified_lineage_relationship", "").strip()
        }
        if split_semicolon_values(completion_row, "codified_lineage_relationships") != relationship_values:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: relationship set mismatch"
            )
        remaining_gates = split_semicolon_values(completion_row, "remaining_completion_gates")
        if source_reviewed_rows:
            for required_gate in ("complete_codified_usc_lineage_review", "model_validation"):
                if required_gate not in remaining_gates:
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                        f"remaining gates should retain {required_gate}"
                    )
            if len(effective_text_rows) < len(source_reviewed_rows):
                if "law_revision_effective_text" not in remaining_gates:
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                        "remaining gates should retain law_revision_effective_text until every reviewed diff row has effective-text review"
                    )
                if "effective_text" not in completion_row.get("completion_status", ""):
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                        "completion status should flag missing effective text for reviewed diffs"
                    )
            else:
                if "law_revision_effective_text" in remaining_gates:
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                        "remaining gates should not retain law_revision_effective_text after full effective-text review"
                    )
                if len(causal_rows) < len(source_reviewed_rows):
                    if "public_law_causal_attribution" not in remaining_gates:
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "remaining gates should retain public-law attribution until every reviewed diff row has attribution review"
                        )
                    status = completion_row.get("completion_status", "")
                    if "causation_unreviewed" not in status and "partial_public_law_attribution" not in status:
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "completion status should flag missing or partial public-law attribution"
                        )
                    if "causal attribution" not in completion_row.get("next_completion_action", ""):
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "next action should point to causal-attribution review"
                        )
                else:
                    if "public_law_causal_attribution" in remaining_gates:
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "remaining gates should not retain public-law attribution after full attribution review"
                        )
                    if "public_law_attribution_reviewed" not in completion_row.get("completion_status", ""):
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "completion status should flag reviewed public-law attribution"
                        )
                    if "public-law attribution" not in completion_row.get("completion_priority_reason", ""):
                        failures.append(
                            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                            "completion priority should note public-law attribution review"
                        )
            if len(effective_text_rows) != len(source_reviewed_rows):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                    "effective-text reviewed row count should match source-reviewed target diff rows"
                )
            if len(causal_rows) != len(source_reviewed_rows):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                    "public-law attribution row count should match source-reviewed target diff rows"
                )
        if parse_int(completion_row.get("reviewed_no_structured_usc_target_rows", "")) not in {None, 0}:
            if "public_law_non_target_status_claim_boundary" not in remaining_gates:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                    "no-target rows should retain non-target claim-boundary gate"
                )
        artifacts = split_semicolon_values(completion_row, "source_artifacts")
        for required_artifact in (
            str(BILL_LAW_LIFECYCLE_CORPUS),
            str(STATUTORY_LINEAGE_CODIFIED_PROGRESS),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: missing source artifact {required_artifact}"
                )
        if source_reviewed_rows and str(STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW) not in artifacts:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: missing target-diff source artifact"
            )
        if source_reviewed_rows and str(STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW) not in artifacts:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: missing effective-text source artifact"
            )
        if source_reviewed_rows and str(STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW) not in artifacts:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: missing public-law attribution source artifact"
            )
        if "statutory_lineage_completion_queue" not in split_semicolon_values(completion_row, "evidence_layers"):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: missing completion evidence layer"
            )
        boundary = completion_row.get("claim_boundary", "")
        if (
            "Codified-lineage completion queue only" not in boundary
            or "not complete codified lineage" not in boundary
            or "public-law attribution pilots" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: {bill_id}: "
                "claim boundary must reject completion overclaims"
            )
    if sorted(completion_ranks) != list(range(1, len(statutory_lineage_completion_queue) + 1)):
        failures.append(f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: completion ranks must be contiguous")
    expected_effective_text_public_laws = {
        row.get("bill_id", "").strip()
        for row in statutory_lineage_target_section_diff_review
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
    }
    if effective_text_reviewed_public_laws != len(expected_effective_text_public_laws):
        failures.append(
            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: expected effective-text reviews for "
            f"{len(expected_effective_text_public_laws)} source-reviewed public-law rows"
        )
    if causal_attribution_reviewed_public_laws != len(expected_effective_text_public_laws):
        failures.append(
            f"{STATUTORY_LINEAGE_COMPLETION_QUEUE}: expected public-law attribution reviews for "
            f"{len(expected_effective_text_public_laws)} source-reviewed public-law rows"
        )

    required_complete_lineage_expansion_columns = {
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
    }
    missing_complete_lineage_expansion_columns = (
        required_complete_lineage_expansion_columns
        - set(statutory_lineage_complete_lineage_expansion_queue[0])
    )
    if missing_complete_lineage_expansion_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: missing columns "
            f"{sorted(missing_complete_lineage_expansion_columns)}"
        )
    if not STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE_MD}: missing markdown report")
    else:
        complete_lineage_expansion_md = STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE_MD.read_text()
        for phrase in (
            "Complete-lineage expansion queue rows",
            "Active codified-lineage expansion rows",
            "Source-scan target candidates represented",
            "Triage references needing packet review",
            "Claim boundary",
        ):
            if phrase not in complete_lineage_expansion_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    complete_lineage_expansion_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in statutory_lineage_complete_lineage_expansion_queue
        if row.get("bill_id", "").strip()
    }
    if len(complete_lineage_expansion_by_bill) != len(statutory_lineage_complete_lineage_expansion_queue):
        failures.append(f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: duplicate bill_id rows")
    if set(complete_lineage_expansion_by_bill) != set(completion_by_bill):
        failures.append(
            "statutory-lineage complete-lineage expansion/completion bill mismatch: "
            f"missing from expansion={sorted(set(completion_by_bill) - set(complete_lineage_expansion_by_bill))}, "
            f"extra={sorted(set(complete_lineage_expansion_by_bill) - set(completion_by_bill))}"
        )
    triage_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_section_triage:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            triage_rows_by_bill[bill_id].append(row)
    packet_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_review_packets:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            packet_rows_by_bill[bill_id].append(row)

    expansion_ranks: list[int] = []
    for bill_id, expansion_row in complete_lineage_expansion_by_bill.items():
        completion_row = completion_by_bill.get(bill_id, {})
        source_row = source_scan_by_bill.get(bill_id, {})
        triage_rows_for_bill = triage_rows_by_bill.get(bill_id, [])
        packet_rows_for_bill = packet_rows_by_bill.get(bill_id, [])
        diff_rows_for_bill = target_diff_rows_by_bill.get(bill_id, [])
        source_reviewed_rows = [
            row for row in diff_rows_for_bill
            if row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        no_exact_rows = [
            row for row in diff_rows_for_bill
            if row.get("review_status", "").strip()
            == "reviewed_related_section_context_no_exact_target_diff"
        ]
        effective_text_rows = [
            row for row in effective_text_review_rows_by_bill.get(bill_id, [])
            if row.get("law_revision_effective_text_reviewed", "").strip() == "1"
        ]
        causal_rows = [
            row for row in public_law_attribution_review_rows_by_bill.get(bill_id, [])
            if row.get("public_law_causal_attribution_reviewed", "").strip() == "1"
            and row.get("public_law_causal_attribution", "").strip()
            and row.get("public_law_causal_attribution", "").strip()
            != "not_reviewed_for_exclusive_public_law_causation"
        ]
        triage_candidate_refs = {
            row.get("target_reference", "").strip()
            for row in triage_rows_for_bill
            if row.get("target_reference", "").strip()
            and row.get("target_reference", "").strip() != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
        }
        packet_refs = {
            row.get("target_reference", "").strip()
            for row in packet_rows_for_bill
            if row.get("target_reference", "").strip()
            and row.get("target_reference", "").strip() != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
        }
        source_reviewed_refs = {
            row.get("target_reference", "").strip()
            for row in source_reviewed_rows
            if row.get("target_reference", "").strip()
        }
        source_candidate_count = parse_int(source_row.get("target_section_candidate_count", "0")) or 0
        source_candidate_gap = max(source_candidate_count - len(triage_candidate_refs), 0)
        triage_packet_gap = max(len(triage_candidate_refs - packet_refs), 0)
        packet_positive_gap = max(len(packet_refs - source_reviewed_refs), 0)
        effective_text_gap = max(len(source_reviewed_rows) - len(effective_text_rows), 0)
        attribution_gap = max(len(source_reviewed_rows) - len(causal_rows), 0)
        rank = parse_int(expansion_row.get("expansion_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: invalid expansion_rank"
            )
        else:
            expansion_ranks.append(rank)
        for field in (
            "completion_rank",
            "corpus_rank",
            "action_rank",
            "public_law_number",
            "policy_area",
            "next_actionable_upgrade_gate",
            "completion_status",
            "reviewed_no_structured_usc_target_rows",
            "remaining_completion_gates",
        ):
            if expansion_row.get(field, "").strip() != completion_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    f"{field} does not match {STATUTORY_LINEAGE_COMPLETION_QUEUE}"
                )
        for output_field, source_field in (
            ("source_scan_usc_reference_count", "usc_reference_count"),
            ("source_scan_target_candidate_count", "target_section_candidate_count"),
        ):
            if expansion_row.get(output_field, "").strip() != source_row.get(source_field, "0").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    f"{output_field} does not match {STATUTORY_LINEAGE_SOURCE_SCAN}"
                )
        expected_count_fields = {
            "triage_rows": len(triage_rows_for_bill),
            "triage_candidate_rows": len(triage_candidate_refs),
            "review_packet_rows": len(packet_rows_for_bill),
            "target_diff_review_rows": len(diff_rows_for_bill),
            "source_reviewed_target_section_diff_rows": len(source_reviewed_rows),
            "reviewed_no_exact_target_section_diff_rows": len(no_exact_rows),
            "law_revision_effective_text_reviewed_rows": len(effective_text_rows),
            "public_law_causal_attribution_reviewed_rows": len(causal_rows),
            "source_candidate_count_minus_triage_rows": source_candidate_gap,
            "triage_to_packet_gap_rows": triage_packet_gap,
            "packet_to_positive_diff_gap_rows": packet_positive_gap,
            "source_reviewed_diff_without_effective_text_rows": effective_text_gap,
            "source_reviewed_diff_without_attribution_rows": attribution_gap,
        }
        for field, expected_value in expected_count_fields.items():
            if parse_int(expansion_row.get(field, "")) != expected_value:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    f"{field} expected {expected_value}"
                )
        if split_semicolon_values(expansion_row, "target_references_with_source_review") != source_reviewed_refs:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                "source-reviewed target reference set mismatch"
            )
        if split_semicolon_values(expansion_row, "triage_references_needing_packet_review") != (
            triage_candidate_refs - packet_refs
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                "triage references needing packet review mismatch"
            )
        if split_semicolon_values(expansion_row, "packet_references_needing_positive_source_review") != (
            packet_refs - source_reviewed_refs
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                "packet references needing positive source-review mismatch"
            )
        no_target_rows = parse_int(completion_row.get("reviewed_no_structured_usc_target_rows", "")) or 0
        if no_target_rows and not source_reviewed_rows:
            expected_status = "reviewed_no_structured_usc_target_no_complete_lineage_expansion"
            if expected_status != expansion_row.get("complete_lineage_expansion_status", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    "no-target row has unexpected expansion status"
                )
            if "Do not infer a codified U.S.C. target" not in expansion_row.get("next_complete_lineage_action", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    "no-target action must reject target inference"
                )
            if "public_law_non_target_status_claim_boundary" not in split_semicolon_values(expansion_row, "remaining_completion_gates"):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    "no-target row must retain non-target claim-boundary gate"
                )
        elif source_reviewed_rows:
            if effective_text_gap or attribution_gap:
                expected_status = "source_reviewed_target_diff_missing_effective_text_or_attribution"
            elif source_candidate_gap > 0 or triage_packet_gap > 0:
                expected_status = "source_reviewed_target_diff_attribution_reviewed_candidate_expansion_open"
            elif packet_positive_gap > 0:
                expected_status = "source_reviewed_target_diff_attribution_reviewed_packet_disposition_context_open"
            else:
                expected_status = "source_reviewed_target_diff_attribution_reviewed_complete_lineage_audit_open"
            if expansion_row.get("complete_lineage_expansion_status", "").strip() != expected_status:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    f"unexpected expansion status, expected {expected_status}"
                )
            remaining_gates = split_semicolon_values(expansion_row, "remaining_completion_gates")
            for required_gate in (
                "complete_codified_usc_lineage_review",
                "implementation_outcomes_or_enforcement",
                "direct_target_section_court_review",
                "welfare_or_public_benefit",
                "model_validation",
            ):
                if required_gate not in remaining_gates:
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                        f"remaining gates should retain {required_gate}"
                    )
            if effective_text_gap or attribution_gap:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    "current complete-lineage expansion queue should only run after full effective-text and attribution review"
                )
            if (source_candidate_gap > 0 or triage_packet_gap > 0) and (
                "complete_target_reference_inventory"
                not in split_semicolon_values(expansion_row, "missing_links")
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    "candidate-expansion rows should retain complete target-inventory gap"
                )
        artifacts = split_semicolon_values(expansion_row, "source_artifacts")
        for required_artifact in (
            str(STATUTORY_LINEAGE_COMPLETION_QUEUE),
            str(STATUTORY_LINEAGE_SOURCE_SCAN),
            str(STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                    f"missing source artifact {required_artifact}"
                )
        if source_reviewed_rows:
            for required_artifact in (
                str(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS),
                str(STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW),
                str(STATUTORY_LINEAGE_EFFECTIVE_TEXT_REVIEW),
                str(STATUTORY_LINEAGE_PUBLIC_LAW_ATTRIBUTION_REVIEW),
            ):
                if required_artifact not in artifacts:
                    failures.append(
                        f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                        f"missing source artifact {required_artifact}"
                    )
        evidence_layers = split_semicolon_values(expansion_row, "evidence_layers")
        if "statutory_lineage_complete_lineage_expansion_queue" not in evidence_layers:
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                "missing complete-lineage expansion evidence layer"
            )
        boundary = expansion_row.get("claim_boundary", "")
        if (
            "Complete codified-lineage expansion queue only" not in boundary
            or "does not establish complete codified lineage" not in boundary
            or "implementation outcomes" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                "claim boundary must reject complete-lineage expansion overclaims"
            )
    if sorted(expansion_ranks) != list(
        range(1, len(statutory_lineage_complete_lineage_expansion_queue) + 1)
    ):
        failures.append(
            f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: expansion ranks must be contiguous"
        )

    required_target_packet_expansion_columns = {
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
        "candidate_snippet_count",
        "amendment_snippet_count",
        "repeal_snippet_count",
        "redesignation_snippet_count",
        "incomplete_fragment_count",
        "example_snippets",
        "govinfo_text_url",
        "complete_lineage_expansion_status",
        "source_scan_target_candidate_count",
        "triage_to_packet_gap_rows",
        "remaining_completion_gates",
        "next_packet_expansion_action",
        "evidence_layers",
        "missing_links",
        "source_artifacts",
        "claim_boundary",
    }
    missing_target_packet_expansion_columns = (
        required_target_packet_expansion_columns
        - set(statutory_lineage_target_packet_expansion_queue[0])
    )
    if missing_target_packet_expansion_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: missing columns "
            f"{sorted(missing_target_packet_expansion_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE_MD}: missing markdown report")
    else:
        target_packet_expansion_md = STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE_MD.read_text()
        for phrase in (
            "Target packet expansion queue rows",
            "Public laws with packet-expansion tasks",
            "Direct U.S.C. note-review tasks",
            "Title-only manual-target tasks",
            "Claim boundary",
        ):
            if phrase not in target_packet_expansion_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    packet_keys_for_expansion = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        )
        for row in statutory_lineage_target_review_packets
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    expected_packet_expansion_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for triage_row in statutory_lineage_target_section_triage:
        bill_id = triage_row.get("bill_id", "").strip()
        target_reference = triage_row.get("target_reference", "").strip()
        expansion_row = complete_lineage_expansion_by_bill.get(bill_id, {})
        if not expansion_row:
            continue
        if expansion_row.get("next_actionable_upgrade_gate", "").strip() != "codified_usc_lineage":
            continue
        if not target_reference or target_reference == "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN":
            continue
        key = (bill_id, target_reference)
        if key in packet_keys_for_expansion:
            continue
        if key in expected_packet_expansion_by_key:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}: duplicate packet-expansion key {key}"
            )
        expected_packet_expansion_by_key[key] = triage_row
        if target_reference not in split_semicolon_values(expansion_row, "triage_references_needing_packet_review"):
            failures.append(
                f"{STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id}: "
                f"{target_reference} missing from triage packet-gap field"
            )
    packet_expansion_by_key = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        ): row
        for row in statutory_lineage_target_packet_expansion_queue
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    if len(packet_expansion_by_key) != len(statutory_lineage_target_packet_expansion_queue):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: duplicate bill/target rows")
    if set(packet_expansion_by_key) != set(expected_packet_expansion_by_key):
        failures.append(
            "statutory-lineage target packet expansion/triage gap mismatch: "
            f"missing from expansion={sorted(set(expected_packet_expansion_by_key) - set(packet_expansion_by_key))[:10]}, "
            f"extra={sorted(set(packet_expansion_by_key) - set(expected_packet_expansion_by_key))[:10]}"
        )
    expected_packet_gap_total = sum(
        parse_int(row.get("triage_to_packet_gap_rows", "")) or 0
        for row in statutory_lineage_complete_lineage_expansion_queue
        if row.get("next_actionable_upgrade_gate", "").strip() == "codified_usc_lineage"
    )
    if len(statutory_lineage_target_packet_expansion_queue) != expected_packet_gap_total:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: expected "
            f"{expected_packet_gap_total} rows from complete-lineage triage packet gaps"
        )
    packet_expansion_ranks: list[int] = []
    for key, packet_expansion_row in packet_expansion_by_key.items():
        bill_id, target_reference = key
        triage_row = expected_packet_expansion_by_key.get(key, {})
        expansion_row = complete_lineage_expansion_by_bill.get(bill_id, {})
        source_row = source_scan_by_bill.get(bill_id, {})
        rank = parse_int(packet_expansion_row.get("packet_expansion_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: invalid rank"
            )
        else:
            packet_expansion_ranks.append(rank)
        for output_field, expansion_field in (
            ("expansion_rank", "expansion_rank"),
            ("completion_rank", "completion_rank"),
            ("policy_area", "policy_area"),
            ("complete_lineage_expansion_status", "complete_lineage_expansion_status"),
            ("triage_to_packet_gap_rows", "triage_to_packet_gap_rows"),
            ("remaining_completion_gates", "remaining_completion_gates"),
        ):
            if packet_expansion_row.get(output_field, "").strip() != expansion_row.get(expansion_field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                    f"{output_field} does not match {STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE}"
                )
        for field in (
            "triage_rank",
            "source_scan_rank",
            "bill_id",
            "public_law_number",
            "target_reference",
            "target_reference_type",
            "codification_review_status",
            "candidate_snippet_count",
            "amendment_snippet_count",
            "repeal_snippet_count",
            "redesignation_snippet_count",
            "incomplete_fragment_count",
            "example_snippets",
            "govinfo_text_url",
        ):
            if packet_expansion_row.get(field, "").strip() != triage_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                    f"{field} does not match {STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE}"
                )
        if (
            packet_expansion_row.get("source_scan_target_candidate_count", "").strip()
            != source_row.get("target_section_candidate_count", "0").strip()
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "source candidate count mismatch"
            )
        if packet_expansion_row.get("packet_gap_status", "").strip() != "triaged_reference_needs_olrc_target_review_packet":
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "unexpected packet gap status"
            )
        status = packet_expansion_row.get("codification_review_status", "").strip()
        action = packet_expansion_row.get("next_packet_expansion_action", "")
        if status == "title_only_needs_manual_target" and "title-only" not in action:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "title-only rows should require manual target resolution"
            )
        if status == "incomplete_reference_fragment_needs_manual_review" and "incomplete" not in action:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "incomplete rows should require fragment resolution"
            )
        if status == "needs_olrc_us_code_note_review" and "official OLRC pre/post" not in action:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "direct rows should require OLRC pre/post packet construction"
            )
        artifacts = split_semicolon_values(packet_expansion_row, "source_artifacts")
        for required_artifact in (
            str(STATUTORY_LINEAGE_COMPLETE_LINEAGE_EXPANSION_QUEUE),
            str(STATUTORY_LINEAGE_TARGET_SECTION_TRIAGE),
            str(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS),
            str(STATUTORY_LINEAGE_SOURCE_SCAN),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                    f"missing source artifact {required_artifact}"
                )
        evidence_layers = split_semicolon_values(packet_expansion_row, "evidence_layers")
        for required_layer in (
            "statutory_lineage_target_packet_expansion_queue",
            "statutory_lineage_complete_lineage_expansion_queue",
            "target_section_candidate_triage",
            "statutory_lineage_source_scan",
        ):
            if required_layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                    f"missing evidence layer {required_layer}"
                )
        missing_links = split_semicolon_values(packet_expansion_row, "missing_links")
        for required_gap in (
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "complete_codified_usc_lineage_review",
            "implementation_outcomes_or_enforcement",
            "direct_target_section_court_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                    f"missing gap marker {required_gap}"
                )
        boundary = packet_expansion_row.get("claim_boundary", "")
        if (
            "Target packet expansion queue only" not in boundary
            or "does not establish codified lineage" not in boundary
            or "target-section text diffs" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: {bill_id} {target_reference}: "
                "claim boundary must reject packet-expansion overclaims"
            )
    if sorted(packet_expansion_ranks) != list(
        range(1, len(statutory_lineage_target_packet_expansion_queue) + 1)
    ):
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}: ranks must be contiguous"
        )

    required_target_packet_source_gap_columns = {
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
    }
    missing_target_packet_source_gap_columns = (
        required_target_packet_source_gap_columns
        - set(statutory_lineage_target_packet_source_gap_queue[0])
    )
    if missing_target_packet_source_gap_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: missing columns "
            f"{sorted(missing_target_packet_source_gap_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE_MD}: missing markdown report")
    else:
        target_packet_source_gap_md = STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE_MD.read_text()
        for phrase in (
            "Target packet source-gap queue rows",
            "Current OLRC pages fetched without public-law marker",
            "Title-only references needing section resolution",
            "Incomplete or nonsection references needing manual resolution",
            "Claim boundary",
        ):
            if phrase not in target_packet_source_gap_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE_MD}: "
                    f"missing summary phrase {phrase!r}"
                )

    current_scan_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for current_row in statutory_lineage_olrc_current_scan:
        key = (
            current_row.get("bill_id", "").strip(),
            current_row.get("target_reference", "").strip(),
        )
        if not all(key):
            continue
        if key in current_scan_by_key:
            failures.append(f"{STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}: duplicate bill/target key {key}")
        else:
            current_scan_by_key[key] = current_row
    historical_scan_keys = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        )
        for row in statutory_lineage_olrc_historical_scan
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    annual_text_diff_keys = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        )
        for row in statutory_lineage_olrc_annual_text_diff
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    adjudication_keys = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        )
        for row in statutory_lineage_adjudication
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    target_review_packet_keys = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        )
        for row in statutory_lineage_target_review_packets
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    target_packet_source_gap_by_key = {
        (
            row.get("bill_id", "").strip(),
            row.get("target_reference", "").strip(),
        ): row
        for row in statutory_lineage_target_packet_source_gap_queue
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }
    if len(target_packet_source_gap_by_key) != len(statutory_lineage_target_packet_source_gap_queue):
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: duplicate bill/target rows")
    if set(target_packet_source_gap_by_key) != set(packet_expansion_by_key):
        failures.append(
            "statutory-lineage target packet source-gap/packet-expansion mismatch: "
            f"missing from source-gap={sorted(set(packet_expansion_by_key) - set(target_packet_source_gap_by_key))[:10]}, "
            f"extra={sorted(set(target_packet_source_gap_by_key) - set(packet_expansion_by_key))[:10]}"
        )

    source_gap_ranks: list[int] = []
    for key, source_gap_row in target_packet_source_gap_by_key.items():
        bill_id, target_reference = key
        packet_expansion_row = packet_expansion_by_key.get(key, {})
        current_row = current_scan_by_key.get(key, {})
        rank = parse_int(source_gap_row.get("source_gap_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: invalid rank"
            )
        else:
            source_gap_ranks.append(rank)
        for field in (
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
            "remaining_completion_gates",
        ):
            if source_gap_row.get(field, "").strip() != packet_expansion_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                    f"{field} does not match {STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE}"
                )
        if not current_row:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                f"missing current OLRC scan row in {STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}"
            )
        else:
            for output_field, current_field in (
                ("current_olrc_scan_rank", "olrc_scan_rank"),
                ("current_olrc_scan_status", "olrc_scan_status"),
                ("current_olrc_http_status", "http_status"),
                ("current_olrc_url", "olrc_url"),
                ("current_public_law_reference_status", "public_law_reference_status"),
                ("current_public_law_reference_hits", "public_law_reference_hits"),
            ):
                if source_gap_row.get(output_field, "").strip() != current_row.get(current_field, "").strip():
                    failures.append(
                        f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                        f"{output_field} does not match {STATUTORY_LINEAGE_OLRC_CURRENT_SCAN}"
                    )
        presence_expectations = {
            "historical_scan_present": key in historical_scan_keys,
            "annual_text_diff_present": key in annual_text_diff_keys,
            "adjudication_present": key in adjudication_keys,
            "target_review_packet_present": key in target_review_packet_keys,
        }
        for field, expected_present in presence_expectations.items():
            expected_value = "1" if expected_present else "0"
            if source_gap_row.get(field, "").strip() != expected_value:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                    f"{field} should be {expected_value}"
                )
        current_status = current_row.get("olrc_scan_status", "").strip()
        public_law_status = current_row.get("public_law_reference_status", "").strip()
        if presence_expectations["target_review_packet_present"]:
            expected_source_gap_status = "target_review_packet_already_present_reconcile_expansion_queue"
            expected_action_phrase = "Regenerate the expansion queue"
            expected_reason_phrase = "target-review packet layer already contains"
        elif (
            presence_expectations["historical_scan_present"]
            or presence_expectations["annual_text_diff_present"]
            or presence_expectations["adjudication_present"]
        ):
            expected_source_gap_status = "downstream_source_layer_present_without_target_review_packet"
            expected_action_phrase = "Reconcile historical"
            expected_reason_phrase = "downstream OLRC source layer exists"
        elif not current_row:
            expected_source_gap_status = "current_olrc_scan_missing_blocks_source_gap_review"
            expected_action_phrase = "Regenerate current OLRC scans"
            expected_reason_phrase = "No current OLRC scan row"
        elif (
            current_status == "official_olrc_current_section_page_fetched"
            and public_law_status == "current_page_no_public_law_mention"
        ):
            expected_source_gap_status = "current_olrc_page_fetched_without_public_law_marker_blocks_automated_packet"
            expected_action_phrase = "Manually review current and historical OLRC notes"
            expected_reason_phrase = "does not mention the queued public law"
        elif current_status == "title_only_not_fetched":
            expected_source_gap_status = "title_only_reference_needs_section_resolution_before_packet"
            expected_action_phrase = "Resolve the title-only reference"
            expected_reason_phrase = "title-only"
        elif current_status == "incomplete_or_nonsection_target_not_fetched":
            expected_source_gap_status = "incomplete_or_nonsection_reference_needs_manual_resolution_before_packet"
            expected_action_phrase = "Resolve the incomplete or nonsection target"
            expected_reason_phrase = "incomplete or nonsectional"
        elif (
            current_status == "official_olrc_current_section_page_fetched"
            and public_law_status == "current_page_mentions_public_law"
        ):
            expected_source_gap_status = "current_olrc_page_mentions_public_law_but_downstream_packet_absent"
            expected_action_phrase = "Regenerate historical OLRC"
            expected_reason_phrase = "mentions the queued public law"
        else:
            expected_source_gap_status = "current_olrc_scan_status_needs_manual_source_gap_review"
            expected_action_phrase = "Manually inspect the current OLRC scan row"
            expected_reason_phrase = "not covered by the automated"
        if source_gap_row.get("source_gap_status", "").strip() != expected_source_gap_status:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                "source gap status mismatch"
            )
        if expected_action_phrase not in source_gap_row.get("next_source_gap_action", ""):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                "next action does not match source gap status"
            )
        if expected_reason_phrase not in source_gap_row.get("source_gap_reason", ""):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                "source gap reason does not match source gap status"
            )
        artifacts = split_semicolon_values(source_gap_row, "source_artifacts")
        for required_artifact in (
            str(STATUTORY_LINEAGE_TARGET_PACKET_EXPANSION_QUEUE),
            str(STATUTORY_LINEAGE_OLRC_CURRENT_SCAN),
            str(STATUTORY_LINEAGE_OLRC_HISTORICAL_SCAN),
            str(STATUTORY_LINEAGE_OLRC_ANNUAL_TEXT_DIFF),
            str(STATUTORY_LINEAGE_ADJUDICATION),
            str(STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                    f"missing source artifact {required_artifact}"
                )
        evidence_layers = split_semicolon_values(source_gap_row, "evidence_layers")
        for required_layer in (
            "statutory_lineage_target_packet_source_gap_queue",
            "statutory_lineage_target_packet_expansion_queue",
        ):
            if required_layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                    f"missing evidence layer {required_layer}"
                )
        if (
            current_status == "official_olrc_current_section_page_fetched"
            and "official_olrc_current_us_code_page" not in evidence_layers
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                "fetched current OLRC rows must retain official current-page evidence layer"
            )
        missing_links = split_semicolon_values(source_gap_row, "missing_links")
        for required_gap in (
            "manual_source_resolution_for_packet_gap",
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "complete_codified_usc_lineage_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                    f"missing gap marker {required_gap}"
                )
        boundary = source_gap_row.get("claim_boundary", "")
        if (
            "Target packet source-gap queue only" not in boundary
            or "did not advance" not in boundary
            or "does not establish codified lineage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: {bill_id} {target_reference}: "
                "claim boundary must reject source-gap overclaims"
            )
    if sorted(source_gap_ranks) != list(
        range(1, len(statutory_lineage_target_packet_source_gap_queue) + 1)
    ):
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}: ranks must be contiguous"
        )

    required_target_packet_source_gap_review_columns = {
        "review_rank",
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
        "current_olrc_url",
        "current_public_law_reference_status",
        "review_status",
        "source_gap_reviewed",
        "public_law_source_url",
        "public_law_source_summary",
        "current_olrc_source_summary",
        "source_gap_disposition",
        "source_gap_disposition_summary",
        "next_review_action",
        "source_review_notes",
        "remaining_completion_gates",
        "evidence_layers",
        "missing_links",
        "source_artifacts",
        "claim_boundary",
    }
    missing_target_packet_source_gap_review_columns = (
        required_target_packet_source_gap_review_columns
        - (
            set(statutory_lineage_target_packet_source_gap_review[0])
            if statutory_lineage_target_packet_source_gap_review
            else csv_fieldnames(STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW)
        )
    )
    if missing_target_packet_source_gap_review_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: missing columns "
            f"{sorted(missing_target_packet_source_gap_review_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW_MD}: missing markdown report")
    else:
        target_packet_source_gap_review_md = (
            STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW_MD.read_text()
        )
        for phrase in (
            "Source-gap review rows",
            "Reviewed no-packet dispositions",
            "Disposition categories",
            "Claim boundary",
        ):
            if phrase not in target_packet_source_gap_review_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )

    allowed_source_gap_review_statuses = {
        "reviewed_appropriation_authority_reference_no_packet",
        "reviewed_cross_reference_only_no_packet",
        "reviewed_table_or_prec_reference_no_packet",
        "reviewed_temporary_override_no_packet",
    }
    reviewed_source_gap_by_key: dict[tuple[str, str], dict[str, str]] = {}
    source_gap_review_ranks: list[int] = []
    for review_row in statutory_lineage_target_packet_source_gap_review:
        key = (
            review_row.get("bill_id", "").strip(),
            review_row.get("target_reference", "").strip(),
        )
        if not all(key):
            failures.append(f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: row missing bill/target key")
            continue
        if key in reviewed_source_gap_by_key:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: duplicate bill/target row {key}"
            )
        reviewed_source_gap_by_key[key] = review_row
        source_gap_row = target_packet_source_gap_by_key.get(key, {})
        if not source_gap_row:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                f"missing source-gap queue row in {STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}"
            )
            continue
        rank = parse_int(review_row.get("review_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: invalid review rank"
            )
        else:
            source_gap_review_ranks.append(rank)
        for field in (
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
            "current_olrc_url",
            "current_public_law_reference_status",
            "remaining_completion_gates",
        ):
            if review_row.get(field, "").strip() != source_gap_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                    f"{field} does not match {STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}"
                )
        if review_row.get("source_gap_reviewed", "").strip() != "1":
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                "reviewed rows must set source_gap_reviewed=1"
            )
        if review_row.get("review_status", "").strip() not in allowed_source_gap_review_statuses:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: invalid review status"
            )
        for field in (
            "public_law_source_url",
            "public_law_source_summary",
            "current_olrc_source_summary",
            "source_gap_disposition",
            "source_gap_disposition_summary",
            "next_review_action",
            "source_review_notes",
        ):
            if not review_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                    f"{field} must be populated"
                )
        artifacts = split_semicolon_values(review_row, "source_artifacts")
        for required_artifact in (
            "data/validation/raw/statutory_lineage_target_packet_source_gap_review.csv",
            str(STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE),
            review_row.get("public_law_source_url", "").strip(),
            review_row.get("current_olrc_url", "").strip(),
        ):
            if required_artifact and required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                    f"missing source artifact {required_artifact}"
                )
        evidence_layers = split_semicolon_values(review_row, "evidence_layers")
        for required_layer in (
            "statutory_lineage_target_packet_source_gap_review",
            "statutory_lineage_target_packet_source_gap_queue",
        ):
            if required_layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                    f"missing evidence layer {required_layer}"
                )
        missing_links = split_semicolon_values(review_row, "missing_links")
        for required_gap in (
            "complete_codified_usc_lineage_review",
            "implementation_outcomes_or_enforcement",
            "direct_target_section_court_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                    f"missing gap marker {required_gap}"
                )
        boundary = review_row.get("claim_boundary", "")
        if (
            "Source-gap disposition review only" not in boundary
            or "do not establish codified lineage" not in boundary
            or "target-section text diffs" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: {key}: "
                "claim boundary must reject source-gap review overclaims"
            )
    if sorted(source_gap_review_ranks) != list(
        range(1, len(statutory_lineage_target_packet_source_gap_review) + 1)
    ):
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_REVIEW}: ranks must be contiguous"
        )

    required_target_reference_resolution_columns = {
        "resolution_rank",
        "source_gap_rank",
        "packet_expansion_rank",
        "expansion_rank",
        "completion_rank",
        "triage_rank",
        "source_scan_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "unresolved_target_reference",
        "unresolved_target_reference_type",
        "codification_review_status",
        "source_gap_status",
        "resolution_candidate_status",
        "candidate_reference_count",
        "candidate_target_references",
        "strongest_candidate_reference",
        "candidate_basis",
        "candidate_context_snippets",
        "next_resolution_action",
        "remaining_completion_gates",
        "evidence_layers",
        "missing_links",
        "source_artifacts",
        "claim_boundary",
    }
    missing_target_reference_resolution_columns = (
        required_target_reference_resolution_columns
        - (
            set(statutory_lineage_target_reference_resolution_candidates[0])
            if statutory_lineage_target_reference_resolution_candidates
            else csv_fieldnames(STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES)
        )
    )
    if missing_target_reference_resolution_columns:
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: missing columns "
            f"{sorted(missing_target_reference_resolution_columns)}"
        )
    if not STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES_MD.exists():
        failures.append(f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES_MD}: missing markdown report")
    else:
        target_reference_resolution_md = (
            STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES_MD.read_text()
        )
        for phrase in (
            "Ambiguous packet-blocker rows reviewed",
            "Rows with bounded candidate references",
            "Candidate concrete U.S.C. references suggested",
            "Rows still without bounded source-scan candidates",
            "Claim boundary",
        ):
            if phrase not in target_reference_resolution_md:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES_MD}: missing summary phrase {phrase!r}"
                )

    ambiguous_source_gap_statuses = {
        "title_only_reference_needs_section_resolution_before_packet",
        "incomplete_or_nonsection_reference_needs_manual_resolution_before_packet",
    }
    ambiguous_source_gap_by_key = {
        key: row
        for key, row in target_packet_source_gap_by_key.items()
        if row.get("source_gap_status", "").strip() in ambiguous_source_gap_statuses
    }
    target_reference_resolution_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in statutory_lineage_target_reference_resolution_candidates:
        key = (
            row.get("bill_id", "").strip(),
            row.get("unresolved_target_reference", "").strip(),
        )
        if not all(key):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: row missing bill/reference key"
            )
            continue
        if key in target_reference_resolution_by_key:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: duplicate bill/reference row {key}"
            )
        target_reference_resolution_by_key[key] = row
    if set(target_reference_resolution_by_key) != set(ambiguous_source_gap_by_key):
        failures.append(
            "statutory-lineage target-reference resolution/source-gap mismatch: "
            f"missing from candidates={sorted(set(ambiguous_source_gap_by_key) - set(target_reference_resolution_by_key))[:10]}, "
            f"extra={sorted(set(target_reference_resolution_by_key) - set(ambiguous_source_gap_by_key))[:10]}"
        )

    resolution_ranks: list[int] = []
    rows_with_candidates = 0
    rows_without_candidates = 0
    for key, resolution_row in target_reference_resolution_by_key.items():
        bill_id, unresolved_target_reference = key
        source_gap_row = ambiguous_source_gap_by_key.get(key, {})
        rank = parse_int(resolution_row.get("resolution_rank", ""))
        if rank is None or rank <= 0:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: invalid rank"
            )
        else:
            resolution_ranks.append(rank)
        for field in (
            "source_gap_rank",
            "packet_expansion_rank",
            "expansion_rank",
            "completion_rank",
            "triage_rank",
            "source_scan_rank",
            "bill_id",
            "public_law_number",
            "policy_area",
            "codification_review_status",
            "source_gap_status",
            "remaining_completion_gates",
        ):
            if resolution_row.get(field, "").strip() != source_gap_row.get(field, "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: {field} does not match "
                    f"{STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE}"
                )
        if (
            resolution_row.get("unresolved_target_reference", "").strip()
            != source_gap_row.get("target_reference", "").strip()
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: unresolved reference does not match source-gap target"
            )
        if (
            resolution_row.get("unresolved_target_reference_type", "").strip()
            != source_gap_row.get("target_reference_type", "").strip()
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: unresolved reference type does not match source-gap target type"
            )
        candidate_references = [
            value.strip()
            for value in resolution_row.get("candidate_target_references", "").split(";")
            if value.strip()
        ]
        candidate_reference_count = parse_int(resolution_row.get("candidate_reference_count", ""))
        if candidate_reference_count is None or candidate_reference_count < 0:
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: invalid candidate reference count"
            )
            candidate_reference_count = 0
        if candidate_reference_count != len(candidate_references):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: candidate reference count does not match candidate list"
            )
        if candidate_reference_count > 0:
            rows_with_candidates += 1
            if resolution_row.get("strongest_candidate_reference", "").strip() != candidate_references[0]:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: strongest candidate should be the first candidate"
                )
            if (
                resolution_row.get("resolution_candidate_status", "").strip()
                != "bounded_govinfo_adjacent_snippet_candidate_identified"
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: candidate status mismatch"
                )
            if not resolution_row.get("candidate_basis", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: candidate rows must keep a basis"
                )
            if not resolution_row.get("candidate_context_snippets", "").strip():
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: candidate rows must keep context snippets"
                )
            if "Manually verify" not in resolution_row.get("next_resolution_action", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: candidate rows must require manual verification"
                )
        else:
            rows_without_candidates += 1
            for field in ("strongest_candidate_reference", "candidate_basis", "candidate_context_snippets"):
                if resolution_row.get(field, "").strip():
                    failures.append(
                        f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                        f"{unresolved_target_reference}: no-candidate rows should leave {field} empty"
                    )
            if (
                resolution_row.get("resolution_candidate_status", "").strip()
                != "no_bounded_resolution_candidate_from_source_scan"
            ):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: no-candidate status mismatch"
                )
            if "Manually review" not in resolution_row.get("next_resolution_action", ""):
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: no-candidate rows must require manual review"
                )
        evidence_layers = split_semicolon_values(resolution_row, "evidence_layers")
        for required_layer in (
            "statutory_lineage_target_reference_resolution_candidates",
            "statutory_lineage_target_packet_source_gap_queue",
            "statutory_lineage_source_scan",
        ):
            if required_layer not in evidence_layers:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: missing evidence layer {required_layer}"
                )
        missing_links = split_semicolon_values(resolution_row, "missing_links")
        for required_gap in (
            "manual_source_review_to_confirm_candidate_reference",
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "complete_codified_usc_lineage_review",
            "model_validation",
        ):
            if required_gap not in missing_links:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: missing gap marker {required_gap}"
                )
        artifacts = split_semicolon_values(resolution_row, "source_artifacts")
        for required_artifact in (
            str(STATUTORY_LINEAGE_TARGET_PACKET_SOURCE_GAP_QUEUE),
            str(STATUTORY_LINEAGE_SOURCE_SCAN),
        ):
            if required_artifact not in artifacts:
                failures.append(
                    f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                    f"{unresolved_target_reference}: missing source artifact {required_artifact}"
                )
        boundary = resolution_row.get("claim_boundary", "")
        if (
            "Target-reference resolution candidates only" not in boundary
            or "does not confirm the target section" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: {bill_id} "
                f"{unresolved_target_reference}: claim boundary must reject target-resolution overclaims"
            )
    if sorted(resolution_ranks) != list(
        range(1, len(statutory_lineage_target_reference_resolution_candidates) + 1)
    ):
        failures.append(
            f"{STATUTORY_LINEAGE_TARGET_REFERENCE_RESOLUTION_CANDIDATES}: ranks must be contiguous"
        )
    required_district_policy_columns = {
        "district_id",
        "issue",
        "year",
        "support",
        "intensity",
        "turnout",
        "affected_group_share",
        "bill_id",
        "public_law_number",
        "policy_area",
        "topic_introduced",
        "topic_floor_considered",
        "topic_enacted",
        "policy_context_status",
        "linkage_status",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
        "source_url",
    }
    missing_district_policy_columns = (
        required_district_policy_columns - set(district_public_opinion_policy_context[0])
    )
    if missing_district_policy_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: missing columns "
            f"{sorted(missing_district_policy_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT_MD}: missing markdown report")
    if len(district_public_opinion_policy_context) != len(district_linkage_rows):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: row count "
            f"{len(district_public_opinion_policy_context)} does not match "
            f"{DISTRICT_PUBLIC_OPINION_LINKAGE} row count {len(district_linkage_rows)}"
        )
    district_policy_report_keys = {
        district_policy_context_key(row)
        for row in district_public_opinion_policy_context
    }
    district_policy_raw_keys = {
        district_policy_context_key(row)
        for row in district_policy_context_raw
    }
    district_policy_source_keys = {
        district_policy_context_key(row)
        for row in district_linkage_rows
    }
    if district_policy_report_keys != district_policy_raw_keys:
        failures.append(
            "district public-opinion policy context/report raw mismatch: "
            f"missing from report={sorted(district_policy_raw_keys - district_policy_report_keys)[:10]}, "
            f"extra={sorted(district_policy_report_keys - district_policy_raw_keys)[:10]}"
        )
    if district_policy_raw_keys != district_policy_source_keys:
        failures.append(
            "district public-opinion policy context/source linkage mismatch: "
            f"missing from context={sorted(district_policy_source_keys - district_policy_raw_keys)[:10]}, "
            f"extra={sorted(district_policy_raw_keys - district_policy_source_keys)[:10]}"
        )
    mapped_policy_rows = [
        row for row in district_public_opinion_policy_context
        if row.get("policy_context_status") == "sponsor_district_bill_policy_context"
    ]
    if not mapped_policy_rows:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: expected at least one mapped policy-context row")
    district_linkage_row = linkage_by_family.get("District public opinion and affected groups", {})
    if district_linkage_row:
        boundary = district_linkage_row.get("linkageBoundary", "")
        if mapped_policy_rows and "policy-area context" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention policy-area context")
        next_step = district_linkage_row.get("nextLinkStep", "")
        if "MRP" not in next_step or "affected-population" not in next_step:
            failures.append(f"{LINKAGE}: district public opinion next step should require MRP and affected-population joins")
    for row in district_public_opinion_policy_context:
        key = district_policy_context_key(row)
        boundary = row.get("claim_boundary", "")
        if (
            "bill-topic support" not in boundary
            or "MRP" not in boundary
            or "affected-group" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: "
                "claim_boundary must reject bill-topic support, MRP, affected-group harm, and model validation"
            )
        status = row.get("policy_context_status", "")
        policy_area = row.get("policy_area", "")
        if status == "sponsor_district_bill_policy_context":
            if policy_area not in topic_values:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: policy area "
                    f"{policy_area!r} is not present in topic throughput"
                )
            if "topic_throughput_policy_area" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: mapped row missing topic evidence layer"
                )
            for required_missing in ("MRP_or_small_area_estimate", "ACS_affected_population", "affected_group_harm"):
                if required_missing not in row.get("missing_links", ""):
                    failures.append(
                        f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: "
                        f"missing_links should retain {required_missing}"
                    )
            for count_field in ("topic_introduced", "topic_floor_considered", "topic_enacted"):
                try:
                    int(row.get(count_field, "0") or "0")
                except ValueError:
                    failures.append(f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: {count_field} must be an integer")
        elif status == "unmapped_sponsor_district_policy_area":
            if row.get("topic_introduced") or row.get("topic_floor_considered") or row.get("topic_enacted"):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: unmapped row should not carry topic counts"
                )
        else:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}: {key}: invalid policy_context_status {status!r}"
            )

    required_district_readiness_columns = {
        "readiness_rank",
        "action_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "proxy_row_count",
        "proxy_issue_count",
        "proxy_issues",
        "mean_support",
        "mean_affected_group_proxy",
        "issue_specific_support_rows",
        "mrp_or_small_area_rows",
        "affected_group_support_rows",
        "bill_topic_public_opinion_status",
        "mrp_or_small_area_status",
        "affected_group_status",
        "next_review_sources",
        "review_packet",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_district_readiness_columns = (
        required_district_readiness_columns - set(district_public_opinion_bill_topic_readiness[0])
    )
    if missing_district_readiness_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: missing columns "
            f"{sorted(missing_district_readiness_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS_MD}: missing markdown report")
    policy_rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in district_public_opinion_policy_context:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            policy_rows_by_bill[bill_id].append(row)
    readiness_by_bill = by_field(district_public_opinion_bill_topic_readiness, "bill_id")
    if set(readiness_by_bill) != set(policy_rows_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}"
        )
    for bill_id, row in readiness_by_bill.items():
        expected_policy_rows = policy_rows_by_bill.get(bill_id, [])
        expected_issues = {
            policy_row.get("issue", "").strip()
            for policy_row in expected_policy_rows
            if policy_row.get("issue", "").strip()
        }
        expected_policy_areas = {
            policy_row.get("policy_area", "").strip()
            for policy_row in expected_policy_rows
            if policy_row.get("policy_area", "").strip()
        }
        try:
            proxy_row_count = int(row.get("proxy_row_count", "0") or "0")
            proxy_issue_count = int(row.get("proxy_issue_count", "0") or "0")
            issue_specific_support_rows = int(row.get("issue_specific_support_rows", "0") or "0")
            mrp_rows = int(row.get("mrp_or_small_area_rows", "0") or "0")
            affected_group_rows = int(row.get("affected_group_support_rows", "0") or "0")
        except ValueError:
            failures.append(f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: count fields must be integers")
            proxy_row_count = proxy_issue_count = issue_specific_support_rows = mrp_rows = affected_group_rows = 0
        if proxy_row_count != len(expected_policy_rows):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: proxy rows "
                f"{proxy_row_count} do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT} "
                f"rows {len(expected_policy_rows)}"
            )
        if proxy_issue_count != len(expected_issues):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: proxy issue count "
                f"{proxy_issue_count} does not match policy context issues {len(expected_issues)}"
            )
        readiness_issues = {
            value.strip()
            for value in row.get("proxy_issues", "").split(";")
            if value.strip()
        }
        if readiness_issues != expected_issues:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: proxy issues "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}"
            )
        readiness_policy_areas = {
            value.strip()
            for value in row.get("policy_area", "").split(";")
            if value.strip()
        }
        if readiness_policy_areas != expected_policy_areas:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: policy areas "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}"
            )
        for numeric_field in ("mean_support", "mean_affected_group_proxy"):
            try:
                float(row.get(numeric_field, "0") or "0")
            except ValueError:
                failures.append(f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: {numeric_field} must be numeric")
        if issue_specific_support_rows != 0 or mrp_rows != 0 or affected_group_rows != 0:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: current readiness rows "
                "must not claim issue-specific, MRP, or affected-group support evidence"
            )
        if row.get("bill_topic_public_opinion_status") != "proxy_only_missing_issue_specific_bill_support":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                "expected proxy-only bill-topic status"
            )
        if row.get("mrp_or_small_area_status") != "missing_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                "expected missing MRP/small-area status"
            )
        if row.get("affected_group_status") != "missing_issue_specific_affected_group_support_or_harm":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                "expected missing affected-group support/harm status"
            )
        for required_layer in (
            "sponsor_district_bill_policy_area_context",
            "topic_throughput_policy_area",
            "bill_topic_public_opinion_readiness_queue",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "bill-topic public support" not in boundary
            or "MRP" not in boundary
            or "affected-group support or harm" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}: {bill_id}: "
                "claim_boundary must reject bill-topic support, MRP, affected-group evidence, and model validation"
            )
    required_district_source_packet_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "proxy_issues",
        "proxy_row_count",
        "current_proxy_status",
        "target_issue_construct",
        "bill_topic_survey_source",
        "district_estimation_source",
        "affected_population_source",
        "affected_support_or_harm_source",
        "required_join_keys",
        "acquisition_status",
        "next_action",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_district_source_packet_columns = (
        required_district_source_packet_columns - set(district_public_opinion_source_packets[0])
    )
    if missing_district_source_packet_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: missing columns "
            f"{sorted(missing_district_source_packet_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS_MD}: missing markdown report")
    source_packets_by_bill = by_field(district_public_opinion_source_packets, "bill_id")
    if set(source_packets_by_bill) != set(readiness_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}"
        )
    for bill_id, row in source_packets_by_bill.items():
        readiness_row = readiness_by_bill.get(bill_id, {})
        for field in (
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "proxy_issues",
            "proxy_row_count",
        ):
            if row.get(field, "") != readiness_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_BILL_TOPIC_READINESS}"
                )
        if row.get("current_proxy_status") != readiness_row.get("bill_topic_public_opinion_status", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                "current_proxy_status does not match readiness status"
            )
        if row.get("acquisition_status") != "source_packet_only_no_external_dataset_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                "source packets must not claim an acquired external dataset"
            )
        for required_text_field in (
            "target_issue_construct",
            "bill_topic_survey_source",
            "district_estimation_source",
            "affected_population_source",
            "affected_support_or_harm_source",
            "next_action",
        ):
            if not row.get(required_text_field, "").strip():
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                    f"{required_text_field} must be populated"
                )
        for required_key in (
            "bill_id",
            "district_id",
            "survey_item_id",
            "mrp_estimate_id",
            "affected_group",
            "affected_population_denominator",
        ):
            if required_key not in row.get("required_join_keys", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                    f"required_join_keys should include {required_key}"
                )
        if "public_opinion_source_acquisition_packet" not in row.get("evidence_layers", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                "missing source-packet evidence layer"
            )
        for required_gap in (
            "bill_topic_public_opinion",
            "survey_item_crosswalk",
            "MRP_or_small_area_estimate",
            "affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not acquired bill-topic support data" not in boundary
            or "not MRP" not in boundary
            or "not affected-population denominators" not in boundary
            or "not affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}: {bill_id}: "
                "claim_boundary must reject acquired support, MRP, affected-population, affected-group, and model-validation evidence"
            )
    required_district_denominator_raw_columns = {
        "district_id",
        "state",
        "state_fips",
        "congressional_district",
        "tigerweb_layer",
        "cd_session",
        "geoid",
        "name",
        "pop100",
        "hu100",
        "arealand_sq_m",
        "areawater_sq_m",
        "land_area_sq_km",
        "population_density_per_sq_km",
        "denominator_status",
        "linkage_basis",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    if not district_census_denominators_raw:
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: no rows")
    else:
        missing_raw_denominator_columns = (
            required_district_denominator_raw_columns - set(district_census_denominators_raw[0])
        )
        if missing_raw_denominator_columns:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: missing columns "
                f"{sorted(missing_raw_denominator_columns)}"
            )
    if not DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_MD}: missing markdown report")
    required_district_denominator_columns = {
        "packet_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "denominator_district_count",
        "matched_denominator_districts",
        "missing_denominator_districts",
        "total_pop100",
        "total_hu100",
        "total_land_area_sq_km",
        "mean_population_density_per_sq_km",
        "denominator_status",
        "denominator_source",
        "evidence_layers",
        "missing_links",
        "source_url",
        "claim_boundary",
    }
    missing_denominator_columns = (
        required_district_denominator_columns - set(district_public_opinion_census_denominators[0])
    )
    if missing_denominator_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: missing columns "
            f"{sorted(missing_denominator_columns)}"
        )
    raw_denominators_by_district = by_field(district_census_denominators_raw, "district_id")
    expected_denominator_districts = {
        value.strip()
        for row in district_public_opinion_source_packets
        for value in row.get("sponsor_districts", "").split(";")
        if value.strip()
    }
    if set(raw_denominators_by_district) != expected_denominator_districts:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: district set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
        )
    for district_id, row in raw_denominators_by_district.items():
        if row.get("denominator_status") != "official_tigerweb_population_housing_denominator":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                "unexpected denominator_status"
            )
        for numeric_field in ("pop100", "hu100", "arealand_sq_m"):
            value = parse_int(row.get(numeric_field, ""))
            if value is None or value <= 0:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                    f"{numeric_field} must be positive"
                )
        if row.get("cd_session") != "116":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                "expected 116th congressional-district layer for 117th Congress queue"
            )
        if "census_tigerweb_116th_district_population_housing_denominator" not in row.get("evidence_layers", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                "missing Census TIGERweb evidence layer"
            )
        for required_gap in (
            "ACS_veteran_population",
            "ACS_income_poverty_employment",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "issue_specific_affected_population_denominator",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not ACS" not in boundary
            or "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not issue-specific affected-group" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS_RAW}: {district_id}: "
                "claim_boundary must reject ACS detail, bill-topic support, MRP, affected-group, and model-validation evidence"
            )
    denominators_by_bill = by_field(district_public_opinion_census_denominators, "bill_id")
    if set(denominators_by_bill) != set(source_packets_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
        )
    for bill_id, row in denominators_by_bill.items():
        packet_row = source_packets_by_bill.get(bill_id, {})
        for field in ("packet_rank", "public_law_number", "policy_area", "sponsor_districts"):
            if row.get(field, "") != packet_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
                )
        expected_districts = {
            value.strip()
            for value in packet_row.get("sponsor_districts", "").split(";")
            if value.strip()
        }
        matched_districts = {
            value.strip()
            for value in row.get("matched_denominator_districts", "").split(";")
            if value.strip()
        }
        missing_districts = {
            value.strip()
            for value in row.get("missing_denominator_districts", "").split(";")
            if value.strip()
        }
        if matched_districts != expected_districts:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "matched denominator districts do not match source-packet sponsor districts"
            )
        if missing_districts:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                f"unexpected missing denominator districts {sorted(missing_districts)}"
            )
        try:
            denominator_district_count = int(row.get("denominator_district_count", "0") or "0")
        except ValueError:
            failures.append(f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: denominator_district_count must be integer")
            denominator_district_count = 0
        if denominator_district_count != len(expected_districts):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "denominator district count does not match sponsor district count"
            )
        expected_pop = sum(
            parse_int(raw_denominators_by_district.get(district, {}).get("pop100", "")) or 0
            for district in expected_districts
        )
        expected_hu = sum(
            parse_int(raw_denominators_by_district.get(district, {}).get("hu100", "")) or 0
            for district in expected_districts
        )
        actual_pop = parse_int(row.get("total_pop100", ""))
        actual_hu = parse_int(row.get("total_hu100", ""))
        if actual_pop != expected_pop or actual_hu != expected_hu:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "population/housing totals do not match raw denominator rows"
            )
        if row.get("denominator_status") != "official_tigerweb_population_housing_denominator":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "unexpected denominator_status"
            )
        if "census_tigerweb_116th_district_population_housing_denominator" not in row.get("evidence_layers", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "missing Census TIGERweb evidence layer"
            )
        for required_gap in (
            "bill_topic_public_opinion",
            "survey_item_crosswalk",
            "MRP_or_small_area_estimate",
            "ACS_policy_specific_affected_population_denominator",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not ACS policy-specific affected-population detail" not in boundary
            or "not issue-specific affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CENSUS_DENOMINATORS}: {bill_id}: "
                "claim_boundary must reject bill-topic support, MRP, ACS detail, affected-group, and model-validation evidence"
            )

    required_district_acs_raw_columns = {
        "district_id",
        "state",
        "state_fips",
        "congressional_district",
        "acs_geoid",
        "acs_name",
        "acs_dataset",
        "acs_vintage",
        "congressional_district_session",
        "acs_context_status",
        "race_total_population_est",
        "civilian_population_18_plus_est",
        "veterans_est",
        "nativity_citizenship_total_population_est",
        "not_us_citizen_est",
        "language_population_5_plus_est",
        "non_english_home_language_est",
        "disability_universe_est",
        "with_disability_est",
        "poverty_ratio_universe_est",
        "below_poverty_est",
        "households_est",
        "no_internet_access_est",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_acs_raw_columns = (
        required_district_acs_raw_columns - set(district_public_opinion_acs_context_raw[0])
    )
    if missing_acs_raw_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: missing columns "
            f"{sorted(missing_acs_raw_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_MD}: missing markdown report")
    raw_acs_by_district = by_field(district_public_opinion_acs_context_raw, "district_id")
    if set(raw_acs_by_district) != expected_denominator_districts:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: district set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
        )
    acs_special_values = {
        "-222222222",
        "-333333333",
        "-555555555",
        "-666666666",
        "-777777777",
        "-888888888",
        "-999999999",
    }
    for district_id, row in raw_acs_by_district.items():
        if row.get("acs_context_status") != "official_acs_2017_2021_5yr_district_context":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                "unexpected acs_context_status"
            )
        if row.get("congressional_district_session") != "116":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                "expected 116th congressional-district ACS geography"
            )
        if row.get("acs_vintage") != "2017-2021":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                "expected ACS vintage 2017-2021"
            )
        for field, value in row.items():
            if (field.endswith("_est") or field.endswith("_moe")) and value in acs_special_values:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                    f"{field} still contains ACS special sentinel value"
                )
        for numeric_field in (
            "race_total_population_est",
            "civilian_population_18_plus_est",
            "nativity_citizenship_total_population_est",
            "language_population_5_plus_est",
            "disability_universe_est",
            "poverty_ratio_universe_est",
            "households_est",
        ):
            value = parse_int(row.get(numeric_field, ""))
            if value is None or value <= 0:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                    f"{numeric_field} must be positive"
                )
        for numeric_field in (
            "veterans_est",
            "not_us_citizen_est",
            "non_english_home_language_est",
            "with_disability_est",
            "below_poverty_est",
            "no_internet_access_est",
        ):
            value = parse_int(row.get(numeric_field, ""))
            if value is None or value < 0:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                    f"{numeric_field} must be a nonnegative integer"
                )
        if "acs_2017_2021_5yr_116th_congressional_district_context" not in row.get("evidence_layers", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                "missing ACS district-context evidence layer"
            )
        for required_gap in (
            "bill_topic_public_opinion",
            "survey_item_crosswalk",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not bill-text-specific affected-population" not in boundary
            or "not issue-specific affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT_RAW}: {district_id}: "
                "claim_boundary must reject bill-topic support, MRP, bill-text-specific affected population, affected-group, and model-validation evidence"
            )

    required_district_acs_columns = {
        "packet_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "acs_context_district_count",
        "matched_acs_context_districts",
        "missing_acs_context_districts",
        "total_acs_population_est",
        "total_veterans_est",
        "total_not_us_citizen_est",
        "total_below_poverty_est",
        "total_households_est",
        "total_no_internet_access_est",
        "selected_acs_context_fields",
        "still_missing_policy_specific_fields",
        "acs_context_status",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    missing_acs_columns = required_district_acs_columns - set(district_public_opinion_acs_context[0])
    if missing_acs_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: missing columns {sorted(missing_acs_columns)}"
        )
    acs_by_bill = by_field(district_public_opinion_acs_context, "bill_id")
    if set(acs_by_bill) != set(source_packets_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
        )
    acs_total_mappings = {
        "total_acs_population_est": "race_total_population_est",
        "total_veterans_est": "veterans_est",
        "total_not_us_citizen_est": "not_us_citizen_est",
        "total_below_poverty_est": "below_poverty_est",
        "total_households_est": "households_est",
        "total_no_internet_access_est": "no_internet_access_est",
    }
    for bill_id, row in acs_by_bill.items():
        packet_row = source_packets_by_bill.get(bill_id, {})
        for field in ("packet_rank", "public_law_number", "policy_area", "sponsor_districts"):
            if row.get(field, "") != packet_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
                )
        expected_districts = {
            value.strip()
            for value in packet_row.get("sponsor_districts", "").split(";")
            if value.strip()
        }
        matched_districts = split_semicolon_values(row, "matched_acs_context_districts")
        missing_districts = split_semicolon_values(row, "missing_acs_context_districts")
        if matched_districts != expected_districts:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "matched ACS districts do not match source-packet sponsor districts"
            )
        if missing_districts:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                f"unexpected missing ACS districts {sorted(missing_districts)}"
            )
        acs_count = parse_int(row.get("acs_context_district_count", ""))
        if acs_count != len(expected_districts):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "ACS district count does not match sponsor district count"
            )
        for report_field, raw_field in acs_total_mappings.items():
            expected_total = sum(
                parse_int(raw_acs_by_district.get(district, {}).get(raw_field, "")) or 0
                for district in expected_districts
            )
            actual_total = parse_int(row.get(report_field, ""))
            if actual_total != expected_total:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                    f"{report_field} does not match raw ACS district rows"
                )
        if row.get("acs_context_status") != "official_acs_2017_2021_5yr_district_context":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "unexpected acs_context_status"
            )
        if not row.get("selected_acs_context_fields", "").strip():
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "selected_acs_context_fields must be populated"
            )
        if not row.get("still_missing_policy_specific_fields", "").strip():
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "still_missing_policy_specific_fields must be populated"
            )
        for required_layer in (
            "public_opinion_source_acquisition_packet",
            "census_tigerweb_116th_district_population_housing_denominator",
            "acs_2017_2021_5yr_116th_congressional_district_context",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "bill_topic_public_opinion",
            "survey_item_crosswalk",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not bill-text-specific affected-population" not in boundary
            or "not issue-specific affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_ACS_CONTEXT}: {bill_id}: "
                "claim_boundary must reject bill-topic support, MRP, bill-text-specific affected population, affected-group, and model-validation evidence"
            )

    required_district_survey_crosswalk_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "target_issue_construct",
        "primary_survey_source_family",
        "primary_survey_source_url",
        "secondary_survey_source_families",
        "secondary_survey_source_urls",
        "source_access_notes",
        "candidate_item_constructs",
        "candidate_item_search_terms",
        "district_estimation_requirement",
        "poststratification_frame",
        "affected_population_requirement",
        "affected_support_or_harm_requirement",
        "survey_crosswalk_status",
        "next_action",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    missing_crosswalk_columns = (
        required_district_survey_crosswalk_columns - set(district_public_opinion_survey_source_crosswalk[0])
    )
    if missing_crosswalk_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: missing columns "
            f"{sorted(missing_crosswalk_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK_MD}: missing markdown report")
    survey_crosswalk_by_bill = by_field(district_public_opinion_survey_source_crosswalk, "bill_id")
    if set(survey_crosswalk_by_bill) != set(source_packets_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
        )
    for bill_id, row in survey_crosswalk_by_bill.items():
        packet_row = source_packets_by_bill.get(bill_id, {})
        for field in (
            "packet_rank",
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "target_issue_construct",
        ):
            if row.get(field, "") != packet_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_SOURCE_PACKETS}"
                )
        if row.get("survey_crosswalk_status") != "survey_source_crosswalk_no_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "survey crosswalk rows must not claim acquired items or estimates"
            )
        for required_text_field in (
            "primary_survey_source_family",
            "primary_survey_source_url",
            "secondary_survey_source_families",
            "secondary_survey_source_urls",
            "source_access_notes",
            "candidate_item_constructs",
            "candidate_item_search_terms",
            "district_estimation_requirement",
            "poststratification_frame",
            "affected_population_requirement",
            "affected_support_or_harm_requirement",
            "next_action",
        ):
            if not row.get(required_text_field, "").strip():
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                    f"{required_text_field} must be populated"
                )
        if not row.get("primary_survey_source_url", "").startswith("https://"):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "primary_survey_source_url must be an https URL"
            )
        if row.get("primary_survey_source_url", "") not in row.get("source_urls", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "source_urls must include the primary survey source URL"
            )
        if bill_id not in row.get("candidate_item_search_terms", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "candidate_item_search_terms should include the bill ID"
            )
        if row.get("public_law_number", "") not in row.get("candidate_item_search_terms", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "candidate_item_search_terms should include the public-law number"
            )
        if "ACS" not in row.get("poststratification_frame", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "poststratification_frame should retain the ACS frame"
            )
        for required_layer in (
            "public_opinion_source_acquisition_packet",
            "census_tigerweb_116th_district_population_housing_denominator",
            "acs_2017_2021_5yr_116th_congressional_district_context",
            "public_opinion_survey_source_crosswalk",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "bill_topic_public_opinion",
            "survey_item_id",
            "survey_item_crosswalk",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "not acquired survey item" not in boundary
            or "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not bill-text-specific affected-population" not in boundary
            or "not affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}: {bill_id}: "
                "claim_boundary must reject acquired items, bill-topic support, MRP, affected-population, affected-group, and model-validation evidence"
            )

    required_district_survey_item_proxy_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "target_issue_construct",
        "primary_survey_source_family",
        "current_proxy_source_family",
        "current_proxy_dataset_doi",
        "current_proxy_dataset_version",
        "current_proxy_distribution_date",
        "current_proxy_survey_year",
        "current_proxy_variable_ids",
        "current_proxy_signal_names",
        "current_proxy_review_status",
        "bill_topic_candidate_constructs",
        "acquired_bill_topic_item_ids",
        "acquired_bill_topic_item_years",
        "bill_topic_item_review_status",
        "district_estimation_status",
        "affected_group_item_status",
        "required_next_action",
        "evidence_layers",
        "missing_links",
        "source_urls",
        "claim_boundary",
    }
    missing_item_proxy_columns = (
        required_district_survey_item_proxy_columns
        - set(district_public_opinion_survey_item_proxy_review[0])
    )
    if missing_item_proxy_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: missing columns "
            f"{sorted(missing_item_proxy_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW_MD}: missing markdown report")
    item_proxy_by_bill = by_field(district_public_opinion_survey_item_proxy_review, "bill_id")
    if set(item_proxy_by_bill) != set(survey_crosswalk_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}"
        )
    required_proxy_variables = {
        "approval_rep",
        "intent_pres_party",
        "intent_rep_party",
        "voted_turnout_self",
        "intent_turnout_self",
        "no_healthins",
        "cd",
        "weight",
        "year",
    }
    for bill_id, row in item_proxy_by_bill.items():
        crosswalk_row = survey_crosswalk_by_bill.get(bill_id, {})
        for field in (
            "packet_rank",
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "target_issue_construct",
            "primary_survey_source_family",
        ):
            if row.get(field, "") != crosswalk_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}"
                )
        if row.get("current_proxy_source_family") != "Cumulative CES Common Content":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "current_proxy_source_family must be Cumulative CES Common Content"
            )
        if row.get("current_proxy_review_status") != "exact_current_ces_proxy_variables_reviewed_no_bill_topic_item":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "proxy review status must not claim bill-topic item acquisition"
            )
        if row.get("bill_topic_item_review_status") != "no_bill_topic_survey_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "bill-topic item status must remain no_bill_topic_survey_item_acquired"
            )
        if row.get("district_estimation_status") != "no_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "district_estimation_status must not claim MRP/small-area estimates"
            )
        if row.get("affected_group_item_status") != "no_bill_text_specific_affected_group_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "affected_group_item_status must not claim bill-text-specific affected-group items"
            )
        if row.get("acquired_bill_topic_item_ids", "").strip():
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "acquired_bill_topic_item_ids must remain empty until sourced"
            )
        proxy_variables = set(split_semicolon_values(row, "current_proxy_variable_ids"))
        if not required_proxy_variables.issubset(proxy_variables):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "current_proxy_variable_ids must include the exact CES proxy variables"
            )
        for required_signal in (
            "house_representative_approval",
            "presidential_democratic_preference",
            "house_democratic_preference",
            "turnout",
            "uninsured_share_vulnerability_proxy",
        ):
            if required_signal not in row.get("current_proxy_signal_names", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                    f"current_proxy_signal_names must include {required_signal}"
                )
        for required_layer in (
            "public_opinion_survey_source_crosswalk",
            "cumulative_ces_source_variable_review",
            "cumulative_ces_district_aggregate",
            "sponsor_district_bill_policy_area_context",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "bill_topic_public_opinion",
            "acquired_bill_topic_survey_item_id",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        if "10.7910/DVN/II2DB6" not in row.get("current_proxy_dataset_doi", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "current_proxy_dataset_doi must identify the CES Dataverse DOI"
            )
        if "https://dataverse.harvard.edu/" not in row.get("source_urls", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "source_urls must include the CES Dataverse source"
            )
        boundary = row.get("claim_boundary", "")
        if (
            "exact current CES proxy variables" not in boundary
            or "not acquired bill-topic survey item" not in boundary
            or "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not bill-text-specific affected-population" not in boundary
            or "not affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_SURVEY_ITEM_PROXY_REVIEW}: {bill_id}: "
                "claim_boundary must keep proxy-variable, bill-topic item, MRP, affected-group, and model-validation boundaries explicit"
            )

    required_ces_policy_item_raw_columns = {
        "source_family",
        "source_name",
        "dataset_doi",
        "dataset_version",
        "dataset_release_time",
        "dataset_license",
        "data_file_id",
        "data_file_label",
        "data_file_md5",
        "guide_file_id",
        "guide_file_label",
        "guide_file_md5",
        "variable_id",
        "issue_area",
        "short_label",
        "policy_area_targets",
        "candidate_construct_terms",
        "official_header_present",
        "source_url",
        "api_url",
        "data_download_url",
        "guide_download_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_item_raw_columns = (
        required_ces_policy_item_raw_columns
        - set(district_public_opinion_ces_policy_item_candidates_raw[0])
    )
    if missing_ces_policy_item_raw_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: missing columns "
            f"{sorted(missing_ces_policy_item_raw_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_METADATA.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_METADATA}: missing metadata")
    else:
        ces_policy_item_metadata = DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_METADATA.read_text()
        for phrase in (
            "Official policy variables reviewed: 54",
            "Local policy areas with at least one candidate item: 9",
            "Claim boundary",
        ):
            if phrase not in ces_policy_item_metadata:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_METADATA}: missing metadata phrase {phrase!r}"
                )
    ces_policy_raw_by_variable = by_field(
        district_public_opinion_ces_policy_item_candidates_raw,
        "variable_id",
    )
    expected_policy_variables = {
        "abortion_20weeks",
        "abortion_always",
        "abortion_conditional",
        "abortion_coverage",
        "abortion_expenditures",
        "abortion_prohibition",
        "abortion_scale",
        "enviro_airwateracts",
        "enviro_carbon",
        "enviro_mpg_raise",
        "enviro_renewable",
        "enviro_scale",
        "enviro_vs_jobs",
        "guns_assaultban",
        "guns_bgchecks",
        "guns_names",
        "guns_permits",
        "guns_scale",
        "healthcare_aca",
        "healthcare_acamandate",
        "healthcare_medicare",
        "healthcare_medicareage",
        "immig_border",
        "immig_deport",
        "immig_employer",
        "immig_legalize",
        "immig_police",
        "immig_reduce",
        "immig_report",
        "immig_services",
        "immig_wall",
        "military_democracy",
        "military_genocide",
        "military_helpun",
        "military_oil",
        "military_protectallies",
        "military_terroristcamp",
        "affirmativeaction",
        "affirmativeaction_scale",
        "gaymarriage_ban",
        "gaymarriage_legalize",
        "gaymarriage_scale",
        "incometax_vs_salestax",
        "spending_cuts_least",
        "spending_cuts_most",
        "spending_education",
        "spending_healthcare",
        "spending_infrastructure",
        "spending_police",
        "spending_vs_tax",
        "spending_welfare",
        "trade_canmex_except",
        "trade_canmex_include",
        "trade_china",
    }
    if set(ces_policy_raw_by_variable) != expected_policy_variables:
        failures.append(
            "CES policy item candidate raw variable set mismatch: "
            f"missing={sorted(expected_policy_variables - set(ces_policy_raw_by_variable))}, "
            f"extra={sorted(set(ces_policy_raw_by_variable) - expected_policy_variables)}"
        )
    ces_policy_items_by_area: dict[str, set[str]] = defaultdict(set)
    for variable_id, row in ces_policy_raw_by_variable.items():
        if row.get("source_name") != "Cumulative CES Policy Preferences":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "source_name must be Cumulative CES Policy Preferences"
            )
        if row.get("dataset_doi") != "10.7910/DVN/OSXDQO":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "dataset DOI must identify Cumulative CES Policy Preferences"
            )
        if row.get("data_file_id") != "6898233" or row.get("guide_file_id") != "6898232":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "Dataverse file IDs must match the official data and guide files"
            )
        if row.get("official_header_present") != "1":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "official_header_present must be 1"
            )
        if "official_dataverse_policy_preferences_metadata" not in row.get("evidence_layers", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "missing Dataverse metadata evidence layer"
            )
        if "bill_topic_public_opinion" not in row.get("missing_links", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "missing bill-topic public-opinion gap"
            )
        boundary = row.get("claim_boundary", "")
        if (
            "item-candidate metadata only" not in boundary
            or "not bill-topic public support" not in boundary
            or "not MRP" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATES_RAW}: {variable_id}: "
                "claim boundary must preserve candidate-only, support, MRP, and model-validation limits"
            )
        for policy_area in split_semicolon_values(row, "policy_area_targets"):
            ces_policy_items_by_area[policy_area].add(variable_id)

    required_ces_policy_candidate_review_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "target_issue_construct",
        "primary_survey_source_family",
        "policy_preference_source_name",
        "policy_preference_dataset_doi",
        "policy_preference_dataset_version",
        "policy_preference_dataset_release_time",
        "candidate_policy_preference_item_ids",
        "candidate_policy_preference_item_count",
        "candidate_policy_preference_issue_areas",
        "candidate_policy_preference_short_labels",
        "candidate_item_review_status",
        "exact_bill_topic_support_status",
        "district_estimation_status",
        "affected_group_item_status",
        "required_next_action",
        "source_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_candidate_review_columns = (
        required_ces_policy_candidate_review_columns
        - set(district_public_opinion_ces_policy_item_candidate_review[0])
    )
    if missing_ces_policy_candidate_review_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: missing columns "
            f"{sorted(missing_ces_policy_candidate_review_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW_MD.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW_MD}: missing markdown report")
    else:
        ces_policy_candidate_md = DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW_MD.read_text()
        for phrase in (
            "Rows with official CES policy-preference candidate item IDs: 18",
            "Rows without a candidate item in this CES policy-preferences source: 4",
            "Unique candidate variable IDs attached to packets: 43",
            "Rows with exact bill-topic support estimates: 0",
            "Rows with MRP or small-area district estimates: 0",
            "Claim boundary",
        ):
            if phrase not in ces_policy_candidate_md:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW_MD}: missing summary phrase {phrase!r}"
                )
    ces_policy_candidate_by_bill = by_field(
        district_public_opinion_ces_policy_item_candidate_review,
        "bill_id",
    )
    if set(ces_policy_candidate_by_bill) != set(survey_crosswalk_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}"
        )
    candidate_found_rows = 0
    candidate_missing_rows = 0
    unique_attached_candidates: set[str] = set()
    for bill_id, row in ces_policy_candidate_by_bill.items():
        crosswalk_row = survey_crosswalk_by_bill.get(bill_id, {})
        for field in (
            "packet_rank",
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "target_issue_construct",
            "primary_survey_source_family",
        ):
            if row.get(field, "") != crosswalk_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_SURVEY_SOURCE_CROSSWALK}"
                )
        policy_area = row.get("policy_area", "")
        expected_items = ces_policy_items_by_area.get(policy_area, set())
        actual_items = split_semicolon_values(row, "candidate_policy_preference_item_ids")
        if actual_items != expected_items:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                f"candidate items do not match raw policy-area targets for {policy_area}"
            )
        unique_attached_candidates.update(actual_items)
        expected_count = len(expected_items)
        if parse_int(row.get("candidate_policy_preference_item_count", "")) != expected_count:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                "candidate_policy_preference_item_count mismatch"
            )
        if expected_items:
            candidate_found_rows += 1
            if row.get("candidate_item_review_status") != (
                "official_ces_policy_preference_candidate_items_found_no_bill_support_estimate"
            ):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    "candidate status should mark broad CES policy-preference candidates"
                )
            if row.get("policy_preference_source_name") != "Cumulative CES Policy Preferences":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    "policy_preference_source_name mismatch"
                )
            if row.get("policy_preference_dataset_doi") != "10.7910/DVN/OSXDQO":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    "policy-preference DOI mismatch"
                )
            if "https://dataverse.harvard.edu/" not in row.get("source_urls", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    "source_urls must include Dataverse URLs when candidates are present"
                )
        else:
            candidate_missing_rows += 1
            if row.get("candidate_item_review_status") != (
                "no_official_ces_policy_preference_candidate_item_for_policy_area"
            ):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    "candidate status should mark no candidate item for this policy area"
                )
        if row.get("exact_bill_topic_support_status") != "no_exact_bill_topic_support_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                "exact_bill_topic_support_status must not claim support estimates"
            )
        if row.get("district_estimation_status") != "no_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                "district_estimation_status must not claim MRP/small-area estimates"
            )
        if row.get("affected_group_item_status") != "no_bill_text_specific_affected_group_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                "affected_group_item_status must not claim affected-group items"
            )
        for required_layer in (
            "public_opinion_survey_source_crosswalk",
            "official_dataverse_policy_preferences_metadata",
            "official_policy_preferences_tabular_header",
            "ces_policy_preferences_guide_candidate_item_review",
            "district_public_opinion_ces_policy_item_candidate_review",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "exact_bill_topic_item_wording_review",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "item-candidate review only" not in boundary
            or "not source-reviewed exact bill-topic support items" not in boundary
            or "not district support estimates" not in boundary
            or "not MRP" not in boundary
            or "not bill-text-specific affected-population" not in boundary
            or "not affected-group support or harm" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: {bill_id}: "
                "claim_boundary must keep candidate-only, exact-support, MRP, affected-group, and model-validation limits explicit"
            )
    if candidate_found_rows != 18 or candidate_missing_rows != 4 or len(unique_attached_candidates) != 43:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}: summary count mismatch"
        )

    required_ces_policy_response_raw_columns = {
        "source_family",
        "source_name",
        "dataset_doi",
        "dataset_version",
        "dataset_release_time",
        "dataset_license",
        "data_file_id",
        "data_file_label",
        "data_file_md5",
        "variable_id",
        "issue_area",
        "short_label",
        "year",
        "response_scope",
        "total_source_rows",
        "response_nonmissing_count",
        "response_blank_count",
        "observed_response_code_count",
        "observed_response_codes",
        "response_code_counts",
        "response_distribution_status",
        "source_url",
        "data_download_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_response_raw_columns = (
        required_ces_policy_response_raw_columns
        - set(district_public_opinion_ces_policy_item_response_distributions_raw[0])
    )
    if missing_ces_policy_response_raw_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: missing columns "
            f"{sorted(missing_ces_policy_response_raw_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_METADATA.exists():
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_METADATA}: missing metadata"
        )
    else:
        ces_policy_response_metadata = (
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_METADATA.read_text()
        )
        for phrase in (
            "Official source rows streamed: 557456",
            "Official policy variables summarized: 54",
            "Variables with at least one observed response: 54",
            "Source years represented: 16",
            "Source year range: 2006-2021",
            "Variable-year distribution rows: 864",
            "Claim boundary",
            "Response codes are not recoded into support/opposition direction here.",
        ):
            if phrase not in ces_policy_response_metadata:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_METADATA}: "
                    f"missing metadata phrase {phrase!r}"
                )
    response_variables = {
        row.get("variable_id", "")
        for row in district_public_opinion_ces_policy_item_response_distributions_raw
        if row.get("year") == "all"
    }
    if response_variables != expected_policy_variables:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
            "overall variable set must match official candidate variables"
        )
    response_years = {
        row.get("year", "")
        for row in district_public_opinion_ces_policy_item_response_distributions_raw
        if row.get("year") != "all"
    }
    if response_years != {str(year) for year in range(2006, 2022)}:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
            "year set must be 2006-2021"
        )
    if len(district_public_opinion_ces_policy_item_response_distributions_raw) != 918:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
            "expected 918 rows (54 overall rows plus 864 variable-year rows)"
        )
    raw_all_nonmissing_total = 0
    for row in district_public_opinion_ces_policy_item_response_distributions_raw:
        variable_id = row.get("variable_id", "")
        if variable_id not in expected_policy_variables:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                f"unexpected variable {variable_id}"
            )
        if row.get("source_name") != "Cumulative CES Policy Preferences":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: {variable_id}: "
                "source_name must be Cumulative CES Policy Preferences"
            )
        if row.get("dataset_doi") != "10.7910/DVN/OSXDQO" or row.get("data_file_id") != "6898233":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: {variable_id}: "
                "must preserve official dataset DOI and data file ID"
            )
        nonmissing_count = parse_int(row.get("response_nonmissing_count", "")) or 0
        blank_count = parse_int(row.get("response_blank_count", "")) or 0
        total_rows = parse_int(row.get("total_source_rows", "")) or 0
        if nonmissing_count + blank_count != total_rows:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                f"{variable_id}/{row.get('year', '')}: nonmissing plus blank count must equal total rows"
            )
        if row.get("year") == "all":
            raw_all_nonmissing_total += nonmissing_count
            if total_rows != 557456:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: {variable_id}: "
                    "overall total_source_rows must be 557456"
                )
            if nonmissing_count <= 0:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: {variable_id}: "
                    "overall row must have observed responses"
                )
        if nonmissing_count > 0 and row.get("response_distribution_status") != (
            "official_raw_response_code_distribution_available"
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                f"{variable_id}/{row.get('year', '')}: status should mark available distribution"
            )
        if nonmissing_count == 0 and row.get("response_distribution_status") != (
            "official_variable_present_no_nonmissing_responses_in_scope"
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                f"{variable_id}/{row.get('year', '')}: status should mark no nonmissing responses"
            )
        for required_layer in (
            "official_dataverse_policy_preferences_metadata",
            "official_policy_preferences_tabular_header",
            "official_policy_preferences_raw_response_code_distribution",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                    f"{variable_id}: missing evidence layer {required_layer}"
                )
        for required_gap in (
            "response_codebook_direction_review",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "respondent_geography_merge",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                    f"{variable_id}: missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "raw response-code distribution only" not in boundary
            or "not normalized support directions" not in boundary
            or "not bill-topic public support" not in boundary
            or "not district support estimates" not in boundary
            or "not MRP" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
                f"{variable_id}: claim boundary must preserve raw-code, support, district, MRP, and model limits"
            )
    if raw_all_nonmissing_total != 13242351:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTIONS_RAW}: "
            "overall nonmissing response observation total mismatch"
        )

    required_ces_policy_response_review_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "target_issue_construct",
        "candidate_policy_preference_item_ids",
        "candidate_policy_preference_item_count",
        "candidate_items_with_response_distribution_count",
        "candidate_item_year_distribution_rows",
        "source_item_response_observation_count",
        "source_item_blank_observation_count",
        "observed_response_years",
        "observed_response_year_count",
        "response_distribution_status",
        "exact_bill_topic_support_status",
        "support_direction_status",
        "district_estimation_status",
        "affected_group_item_status",
        "required_next_action",
        "source_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_response_review_columns = (
        required_ces_policy_response_review_columns
        - set(district_public_opinion_ces_policy_item_response_distribution_review[0])
    )
    if missing_ces_policy_response_review_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: missing columns "
            f"{sorted(missing_ces_policy_response_review_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW_MD.exists():
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW_MD}: missing markdown report"
        )
    else:
        ces_policy_response_review_md = (
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW_MD.read_text()
        )
        for phrase in (
            "Rows with candidate raw response distributions: 18",
            "Rows without candidate raw response distributions: 4",
            "Unique candidate variable IDs with raw response distributions attached to packets: 43",
            "Aggregate attached source item-response observations: 32667671",
            "Rows with exact bill-topic support estimates: 0",
            "Rows with directionally recoded support/opposition estimates: 0",
            "Rows with MRP or small-area district estimates: 0",
            "Claim boundary",
        ):
            if phrase not in ces_policy_response_review_md:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    response_review_by_bill = by_field(
        district_public_opinion_ces_policy_item_response_distribution_review,
        "bill_id",
    )
    if set(response_review_by_bill) != set(ces_policy_candidate_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}"
        )
    response_found_rows = 0
    response_missing_rows = 0
    unique_response_candidates: set[str] = set()
    attached_response_observations = 0
    raw_overall_by_variable = {
        row.get("variable_id", ""): row
        for row in district_public_opinion_ces_policy_item_response_distributions_raw
        if row.get("year") == "all"
    }
    raw_year_rows_by_variable: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in district_public_opinion_ces_policy_item_response_distributions_raw:
        if row.get("year") != "all":
            raw_year_rows_by_variable[row.get("variable_id", "")].append(row)
    for bill_id, row in response_review_by_bill.items():
        candidate_row = ces_policy_candidate_by_bill.get(bill_id, {})
        for field in (
            "packet_rank",
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "target_issue_construct",
        ):
            if row.get(field, "") != candidate_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CANDIDATE_REVIEW}"
                )
        candidate_items = split_semicolon_values(row, "candidate_policy_preference_item_ids")
        if candidate_items != split_semicolon_values(candidate_row, "candidate_policy_preference_item_ids"):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "candidate item IDs must match candidate-item review"
            )
        expected_distribution_items = {
            item
            for item in candidate_items
            if item in raw_overall_by_variable
            and (parse_int(raw_overall_by_variable[item].get("response_nonmissing_count", "")) or 0) > 0
        }
        actual_distribution_count = (
            parse_int(row.get("candidate_items_with_response_distribution_count", "")) or 0
        )
        if actual_distribution_count != len(expected_distribution_items):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "candidate_items_with_response_distribution_count mismatch"
            )
        expected_observations = sum(
            parse_int(raw_overall_by_variable[item].get("response_nonmissing_count", "")) or 0
            for item in expected_distribution_items
        )
        observed_observations = parse_int(row.get("source_item_response_observation_count", "")) or 0
        if observed_observations != expected_observations:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "source_item_response_observation_count mismatch"
            )
        attached_response_observations += observed_observations
        expected_year_rows = sum(len(raw_year_rows_by_variable.get(item, [])) for item in candidate_items)
        if (parse_int(row.get("candidate_item_year_distribution_rows", "")) or 0) != expected_year_rows:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "candidate_item_year_distribution_rows mismatch"
            )
        if expected_distribution_items:
            response_found_rows += 1
            unique_response_candidates.update(candidate_items)
            if row.get("response_distribution_status") != (
                "official_ces_policy_preference_raw_response_distributions_available_no_support_direction"
            ):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                    "status should mark raw response-code distributions available"
                )
        else:
            response_missing_rows += 1
            if row.get("response_distribution_status") != "no_candidate_item_response_distribution_available":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                    "status should mark no candidate response distribution"
                )
        if row.get("exact_bill_topic_support_status") != "no_exact_bill_topic_support_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "must not claim exact bill-topic support estimates"
            )
        if row.get("support_direction_status") != "raw_response_codes_not_directionally_recoded":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "must not claim directionally recoded support"
            )
        if row.get("district_estimation_status") != "no_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "must not claim MRP/small-area estimates"
            )
        if row.get("affected_group_item_status") != "no_bill_text_specific_affected_group_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "must not claim affected-group items"
            )
        for required_layer in (
            "district_public_opinion_ces_policy_item_candidate_review",
            "official_policy_preferences_raw_response_code_distribution",
            "district_public_opinion_ces_policy_item_response_distribution_review",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "response_codebook_direction_review",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "respondent_geography_merge",
            "bill_text_specific_affected_population_denominator",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "response-distribution review only" not in boundary
            or "not recoded support/opposition" not in boundary
            or "not source-reviewed exact bill-topic support items" not in boundary
            or "not district support estimates" not in boundary
            or "not MRP" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: {bill_id}: "
                "claim_boundary must keep raw-code, support, district, MRP, and model-validation limits explicit"
            )
    if (
        response_found_rows != 18
        or response_missing_rows != 4
        or len(unique_response_candidates) != 43
        or attached_response_observations != 32667671
    ):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}: summary count mismatch"
        )

    required_ces_policy_codebook_raw_columns = {
        "source_family",
        "source_name",
        "dataset_doi",
        "dataset_version",
        "dataset_release_time",
        "dataset_license",
        "guide_file_id",
        "guide_file_label",
        "guide_file_md5",
        "variable_id",
        "issue_area",
        "short_label",
        "guide_section_heading",
        "guide_item_description",
        "guide_years_in_data",
        "guide_year_count",
        "observed_response_code_count",
        "observed_response_codes",
        "guide_response_label_count",
        "guide_response_labels",
        "codebook_code_label_map",
        "code_label_map_status",
        "unmapped_observed_codes",
        "codebook_direction_type",
        "item_support_codes",
        "item_oppose_codes",
        "ordered_low_code",
        "ordered_low_label",
        "ordered_high_code",
        "ordered_high_label",
        "continuous_low_code",
        "continuous_low_label",
        "continuous_high_code",
        "continuous_high_label",
        "direction_review_status",
        "exact_bill_topic_support_status",
        "bill_text_direction_alignment_status",
        "district_estimation_status",
        "source_url",
        "guide_download_url",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_codebook_raw_columns = (
        required_ces_policy_codebook_raw_columns
        - set(district_public_opinion_ces_policy_item_codebook_direction_raw[0])
    )
    if missing_ces_policy_codebook_raw_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: missing columns "
            f"{sorted(missing_ces_policy_codebook_raw_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_METADATA.exists():
        failures.append(f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_METADATA}: missing metadata")
    else:
        ces_policy_codebook_metadata = (
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_METADATA.read_text()
        )
        for phrase in (
            "Official policy variables reviewed: 54",
            "Variables with guide response labels or endpoint labels: 54",
            "Variables with unmapped observed special/raw codes after guide endpoint review: 2",
            "binary_item_support_oppose: 38",
            "continuous_policy_tradeoff_scale: 2",
            "Claim boundary",
        ):
            if phrase not in ces_policy_codebook_metadata:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_METADATA}: "
                    f"missing metadata phrase {phrase!r}"
                )
    ces_policy_codebook_by_variable = by_field(
        district_public_opinion_ces_policy_item_codebook_direction_raw,
        "variable_id",
    )
    if set(ces_policy_codebook_by_variable) != expected_policy_variables:
        failures.append(
            "CES policy item codebook raw variable set mismatch: "
            f"missing={sorted(expected_policy_variables - set(ces_policy_codebook_by_variable))}, "
            f"extra={sorted(set(ces_policy_codebook_by_variable) - expected_policy_variables)}"
        )
    if len(district_public_opinion_ces_policy_item_codebook_direction_raw) != 54:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: expected 54 rows"
        )
    direction_type_counts = Counter(
        row.get("codebook_direction_type", "")
        for row in district_public_opinion_ces_policy_item_codebook_direction_raw
    )
    expected_direction_type_counts = {
        "binary_item_support_oppose": 38,
        "categorical_budget_choice": 2,
        "continuous_policy_tradeoff_scale": 2,
        "ordered_access_scale": 1,
        "ordered_policy_scale": 3,
        "ordered_spending_increase_decrease": 5,
        "ordered_support_opposition_scale": 3,
    }
    if dict(direction_type_counts) != expected_direction_type_counts:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: "
            f"direction type counts mismatch {dict(direction_type_counts)}"
        )
    continuous_special_code_rows = 0
    for variable_id, row in ces_policy_codebook_by_variable.items():
        candidate_row = ces_policy_raw_by_variable.get(variable_id, {})
        distribution_row = raw_overall_by_variable.get(variable_id, {})
        if row.get("source_name") != "Cumulative CES Policy Preferences":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "source_name must be Cumulative CES Policy Preferences"
            )
        if row.get("dataset_doi") != "10.7910/DVN/OSXDQO":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "dataset DOI must identify Cumulative CES Policy Preferences"
            )
        if row.get("guide_file_id") != "6898232" or row.get("guide_file_md5") != "f333bdead4cb56481772eed51029e2ae":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "guide file ID/MD5 must match the official guide"
            )
        for field in ("issue_area", "short_label"):
            if row.get(field, "") != candidate_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    f"{field} must match candidate raw metadata"
                )
        if row.get("observed_response_codes", "") != distribution_row.get("observed_response_codes", ""):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "observed_response_codes must match overall raw response distribution"
            )
        if (parse_int(row.get("guide_response_label_count", "")) or 0) <= 0:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "guide_response_label_count must be positive"
            )
        try:
            code_label_map = json.loads(row.get("codebook_code_label_map", "[]") or "[]")
        except json.JSONDecodeError:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "codebook_code_label_map is not valid JSON"
            )
            code_label_map = []
        direction_type = row.get("codebook_direction_type", "")
        if direction_type == "continuous_policy_tradeoff_scale":
            continuous_special_code_rows += 1 if row.get("unmapped_observed_codes", "").strip() else 0
            if row.get("code_label_map_status") != "continuous_scale_endpoint_labels_only_special_codes_unresolved":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "continuous scales should preserve special raw-code endpoint-only status"
                )
            endpoint_codes = {entry.get("code") for entry in code_label_map if isinstance(entry, dict)}
            if endpoint_codes != {"0.0", "100.0"}:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "continuous scales should map only 0.0 and 100.0 endpoint codes"
                )
            if not row.get("continuous_low_label", "") or not row.get("continuous_high_label", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "continuous scales must keep endpoint labels"
                )
        else:
            observed_codes = split_semicolon_values(row, "observed_response_codes")
            if row.get("code_label_map_status") != "all_observed_discrete_codes_labelled_from_guide":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "discrete variables should have all observed codes labelled from the guide"
                )
            if len(code_label_map) != len(observed_codes):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "code-label map length must match observed discrete code count"
                )
            if row.get("unmapped_observed_codes", "").strip():
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    "discrete variables should not carry unmapped observed codes"
                )
            if direction_type == "binary_item_support_oppose":
                if row.get("item_support_codes") != "1" or row.get("item_oppose_codes") != "2":
                    failures.append(
                        f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                        "binary support/oppose items should map support=1 and oppose=2"
                    )
            if direction_type.startswith("ordered_"):
                if not row.get("ordered_low_code", "") or not row.get("ordered_high_code", ""):
                    failures.append(
                        f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                        "ordered scales must keep low/high code labels"
                    )
        if row.get("exact_bill_topic_support_status") != "no_exact_bill_topic_support_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "must not claim exact bill-topic support estimates"
            )
        if row.get("bill_text_direction_alignment_status") != "no_bill_text_direction_alignment_review":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "must not claim bill-text direction alignment"
            )
        if row.get("district_estimation_status") != "no_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "must not claim MRP/small-area estimates"
            )
        for required_layer in (
            "official_policy_preferences_raw_response_code_distribution",
            "official_policy_preferences_guide_response_codebook_direction",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "exact_bill_topic_item_wording_review",
            "bill_text_direction_alignment_review",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "guide/codebook response-direction review only" not in boundary
            or "not bill-text-aligned support directions" not in boundary
            or "not bill-topic public support estimates" not in boundary
            or "not district support estimates" not in boundary
            or "not MRP" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: {variable_id}: "
                "claim_boundary must keep codebook-only, bill-text, support, district, MRP, and model limits explicit"
            )
    if continuous_special_code_rows != 2:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_RAW}: "
            "expected two continuous endpoint rows with unresolved special raw codes"
        )

    required_ces_policy_codebook_review_columns = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
        "target_issue_construct",
        "candidate_policy_preference_item_ids",
        "candidate_policy_preference_item_count",
        "candidate_items_with_codebook_direction_count",
        "candidate_items_with_binary_item_direction_count",
        "candidate_item_direction_types",
        "candidate_item_support_code_summary",
        "candidate_item_oppose_code_summary",
        "candidate_item_codebook_label_summary",
        "guide_codebook_direction_status",
        "support_direction_status",
        "exact_bill_topic_support_status",
        "bill_text_direction_alignment_status",
        "district_estimation_status",
        "affected_group_item_status",
        "required_next_action",
        "source_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_ces_policy_codebook_review_columns = (
        required_ces_policy_codebook_review_columns
        - set(district_public_opinion_ces_policy_item_codebook_direction_review[0])
    )
    if missing_ces_policy_codebook_review_columns:
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: missing columns "
            f"{sorted(missing_ces_policy_codebook_review_columns)}"
        )
    if not DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW_MD.exists():
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW_MD}: missing markdown report"
        )
    else:
        ces_policy_codebook_review_md = (
            DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW_MD.read_text()
        )
        for phrase in (
            "Rows with candidate codebook direction review: 18",
            "Rows without candidate codebook direction review: 4",
            "Rows with at least one binary item-wording support/oppose direction: 14",
            "Unique candidate variable IDs with codebook directions attached to packets: 43",
            "Unique attached binary support/oppose candidate variable IDs: 28",
            "Rows with bill-text direction alignment: 0",
            "Rows with exact bill-topic support estimates: 0",
            "Rows with MRP or small-area district estimates: 0",
            "Claim boundary",
        ):
            if phrase not in ces_policy_codebook_review_md:
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW_MD}: "
                    f"missing summary phrase {phrase!r}"
                )
    codebook_review_by_bill = by_field(
        district_public_opinion_ces_policy_item_codebook_direction_review,
        "bill_id",
    )
    if set(codebook_review_by_bill) != set(response_review_by_bill):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: bill set does not match "
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}"
        )
    codebook_found_rows = 0
    codebook_missing_rows = 0
    codebook_binary_rows = 0
    unique_codebook_candidates: set[str] = set()
    unique_codebook_binary_candidates: set[str] = set()
    for bill_id, row in codebook_review_by_bill.items():
        response_row = response_review_by_bill.get(bill_id, {})
        for field in (
            "packet_rank",
            "readiness_rank",
            "public_law_number",
            "policy_area",
            "sponsor_districts",
            "target_issue_construct",
            "candidate_policy_preference_item_ids",
        ):
            if row.get(field, "") != response_row.get(field, ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    f"{field} does not match {DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_RESPONSE_DISTRIBUTION_REVIEW}"
                )
        candidate_items = split_semicolon_values(row, "candidate_policy_preference_item_ids")
        expected_direction_items = {
            item
            for item in candidate_items
            if item in ces_policy_codebook_by_variable
        }
        expected_binary_items = {
            item
            for item in expected_direction_items
            if ces_policy_codebook_by_variable[item].get("codebook_direction_type")
            == "binary_item_support_oppose"
        }
        if (parse_int(row.get("candidate_items_with_codebook_direction_count", "")) or 0) != len(expected_direction_items):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "candidate_items_with_codebook_direction_count mismatch"
            )
        if (parse_int(row.get("candidate_items_with_binary_item_direction_count", "")) or 0) != len(expected_binary_items):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "candidate_items_with_binary_item_direction_count mismatch"
            )
        try:
            label_summary_rows = json.loads(row.get("candidate_item_codebook_label_summary", "[]") or "[]")
        except json.JSONDecodeError:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "candidate_item_codebook_label_summary is not valid JSON"
            )
            label_summary_rows = []
        label_summary_ids = {
            summary_row.get("variable_id", "")
            for summary_row in label_summary_rows
            if isinstance(summary_row, dict)
        }
        if label_summary_ids != expected_direction_items:
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "label summary variable IDs must match candidate codebook direction items"
            )
        if expected_direction_items:
            codebook_found_rows += 1
            unique_codebook_candidates.update(candidate_items)
            if row.get("guide_codebook_direction_status") != (
                "official_ces_policy_preference_codebook_direction_review_available_no_bill_mapping"
            ):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    "status should mark codebook direction review available"
                )
        else:
            codebook_missing_rows += 1
            if row.get("guide_codebook_direction_status") != "no_candidate_item_codebook_direction_available":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    "status should mark no candidate codebook direction"
                )
        if expected_binary_items:
            codebook_binary_rows += 1
            unique_codebook_binary_candidates.update(expected_binary_items)
            if row.get("support_direction_status") != (
                "guide_item_wording_support_oppose_codes_available_no_bill_text_alignment"
            ):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    "support_direction_status should mark guide item-wording support/oppose codes only"
                )
        elif expected_direction_items:
            if row.get("support_direction_status") != "guide_codebook_labels_available_no_binary_support_direction":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    "support_direction_status should mark non-binary guide labels only"
                )
        else:
            if row.get("support_direction_status") != "no_candidate_item_codebook_direction_available":
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    "support_direction_status should mark no codebook direction"
                )
        if row.get("exact_bill_topic_support_status") != "no_exact_bill_topic_support_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "must not claim exact bill-topic support estimates"
            )
        if row.get("bill_text_direction_alignment_status") != "no_bill_text_direction_alignment_review":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "must not claim bill-text direction alignment"
            )
        if row.get("district_estimation_status") != "no_mrp_or_small_area_estimate":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "must not claim MRP/small-area estimates"
            )
        if row.get("affected_group_item_status") != "no_bill_text_specific_affected_group_item_acquired":
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "must not claim affected-group items"
            )
        for required_layer in (
            "district_public_opinion_ces_policy_item_response_distribution_review",
            "official_policy_preferences_guide_response_codebook_direction",
            "district_public_opinion_ces_policy_item_codebook_direction_review",
        ):
            if required_layer not in row.get("evidence_layers", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    f"missing evidence layer {required_layer}"
                )
        for required_gap in (
            "exact_bill_topic_item_wording_review",
            "bill_text_direction_alignment_review",
            "bill_topic_public_opinion",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "model_validation",
        ):
            if required_gap not in row.get("missing_links", ""):
                failures.append(
                    f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                    f"missing_links should retain {required_gap}"
                )
        boundary = row.get("claim_boundary", "")
        if (
            "codebook-direction packet review only" not in boundary
            or "survey-item wording direction only" not in boundary
            or "not bill-text-aligned support directions" not in boundary
            or "not exact bill-topic public support estimates" not in boundary
            or "not district support estimates" not in boundary
            or "not MRP" not in boundary
            or "not model validation" not in boundary
        ):
            failures.append(
                f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: {bill_id}: "
                "claim_boundary must keep codebook, bill-text, support, district, MRP, and model limits explicit"
            )
    if (
        codebook_found_rows != 18
        or codebook_missing_rows != 4
        or codebook_binary_rows != 14
        or len(unique_codebook_candidates) != 43
        or len(unique_codebook_binary_candidates) != 28
    ):
        failures.append(
            f"{DISTRICT_PUBLIC_OPINION_CES_POLICY_ITEM_CODEBOOK_DIRECTION_REVIEW}: summary count mismatch"
        )

    if district_linkage_row:
        boundary = district_linkage_row.get("linkageBoundary", "")
        next_step = district_linkage_row.get("nextLinkStep", "")
        if "readiness report queues" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention readiness queue")
        if "source packets" not in next_step:
            failures.append(f"{LINKAGE}: district public opinion next step must point to source packets")
        if "population-housing denominators" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention Census population-housing denominators")
        if "ACS context layer" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention ACS context layer")
        if "survey-source crosswalk" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention survey-source crosswalk")
        if "proxy-review layer" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention survey item proxy-review layer")
        if "CES policy-preference candidate-item review" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention CES policy-preference candidate-item review")
        if "raw response-distribution review" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention raw response-distribution review")
        if "codebook response-direction review" not in boundary:
            failures.append(f"{LINKAGE}: district public opinion boundary must mention codebook response-direction review")
        if (
            "survey-source crosswalk" not in next_step
            or "ACS district-context" not in next_step
            or "proxy review" not in next_step
            or "candidate-item review" not in next_step
            or "response-code" not in next_step
            or "codebook" not in next_step
            or "bill text" not in next_step
            or "bill-text-specific" not in next_step
            or "MRP" not in next_step
        ):
            failures.append(
                f"{LINKAGE}: district public opinion next step must keep survey-source crosswalk, proxy review, candidate-item review, response-code review, codebook, ACS context, bill text, MRP, and bill-text-specific gaps"
            )

    required_rulemaking_authority_columns = {
        "public_law_number",
        "bill_id",
        "linkage_status",
        "candidate_rule_count",
        "matched_rule_count",
        "text_verified_rule_count",
        "matched_document_numbers",
        "usc_citations",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_authority_columns = required_rulemaking_authority_columns - set(rulemaking_authority_linkage[0])
    if missing_authority_columns:
        failures.append(
            f"{RULEMAKING_AUTHORITY_LINKAGE}: missing columns {sorted(missing_authority_columns)}"
        )
    authority_report_keys = {
        row.get("public_law_number", "").strip()
        for row in rulemaking_authority_linkage
        if row.get("public_law_number", "").strip()
    }
    authority_raw_keys = {
        row.get("public_law_number", "").strip()
        for row in rulemaking_authority_raw
        if row.get("public_law_number", "").strip()
    }
    law_public_law_keys = {
        row.get("public_law_number", "").strip()
        for row in law_bill_rows
        if row.get("public_law_number", "").strip()
    }
    if authority_report_keys != authority_raw_keys:
        failures.append(
            "rulemaking authority report/raw mismatch: "
            f"missing from report={sorted(authority_raw_keys - authority_report_keys)}, "
            f"extra={sorted(authority_report_keys - authority_raw_keys)}"
        )
    if authority_report_keys != law_public_law_keys:
        failures.append(
            "rulemaking authority/law-revision public-law mismatch: "
            f"missing from authority={sorted(law_public_law_keys - authority_report_keys)}, "
            f"extra={sorted(authority_report_keys - law_public_law_keys)}"
        )
    authority_by_public_law = {
        row.get("public_law_number", "").strip(): row
        for row in rulemaking_authority_linkage
        if row.get("public_law_number", "").strip()
    }
    authority_match_rows = [
        row for row in rulemaking_authority_linkage
        if row.get("linkage_status") == "federal_register_authority_match"
    ]
    if not authority_match_rows:
        failures.append(f"{RULEMAKING_AUTHORITY_LINKAGE}: expected at least one authority match")
    for row in rulemaking_authority_linkage:
        public_law = row.get("public_law_number", "").strip()
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "enforcement outcome" not in boundary
            or "exhaustive implementation" not in boundary
        ):
            failures.append(
                f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: "
                "claim_boundary must reject implementation outcome, exhaustive implementation, and model-validation claims"
            )
        try:
            candidate_count = int(row.get("candidate_rule_count", "0") or "0")
            matched_count = int(row.get("matched_rule_count", "0") or "0")
            verified_count = int(row.get("text_verified_rule_count", "0") or "0")
        except ValueError:
            failures.append(f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: rule counts must be integers")
            continue
        if verified_count != matched_count:
            failures.append(
                f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: "
                f"text_verified_rule_count {verified_count} does not match matched_rule_count {matched_count}"
            )
        if matched_count > candidate_count:
            failures.append(
                f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: "
                f"matched_rule_count {matched_count} exceeds candidate_rule_count {candidate_count}"
            )
        if row.get("linkage_status") == "federal_register_authority_match":
            if matched_count <= 0 or not row.get("matched_document_numbers", "").strip():
                failures.append(
                    f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: authority match missing verified documents"
                )
            if "public_law_authority_text_match" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: authority match missing evidence layer"
                )
        else:
            if matched_count != 0 or row.get("matched_document_numbers", "").strip() or row.get("usc_citations", "").strip():
                failures.append(
                    f"{RULEMAKING_AUTHORITY_LINKAGE}: {public_law}: unmatched row should not carry verified documents or U.S.C. citations"
                )

    required_rulemaking_history_columns = {
        "public_law_number",
        "bill_id",
        "final_document_number",
        "history_status",
        "candidate_proposed_rule_count",
        "matched_proposed_rule_count",
        "proposed_document_numbers",
        "shared_identifiers",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_history_columns = required_rulemaking_history_columns - set(rulemaking_history_linkage[0])
    if missing_history_columns:
        failures.append(
            f"{RULEMAKING_HISTORY_LINKAGE}: missing columns {sorted(missing_history_columns)}"
        )
    history_report_keys = {
        (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip())
        for row in rulemaking_history_linkage
        if row.get("public_law_number", "").strip() and row.get("final_document_number", "").strip()
    }
    history_raw_keys = {
        (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip())
        for row in rulemaking_history_raw
        if row.get("public_law_number", "").strip() and row.get("final_document_number", "").strip()
    }
    authority_document_keys = {
        (row.get("public_law_number", "").strip(), document.strip())
        for row in rulemaking_authority_linkage
        if row.get("linkage_status") == "federal_register_authority_match"
        for document in row.get("matched_document_numbers", "").split(";")
        if row.get("public_law_number", "").strip() and document.strip()
    }
    if history_report_keys != history_raw_keys:
        failures.append(
            "rulemaking history report/raw mismatch: "
            f"missing from report={sorted(history_raw_keys - history_report_keys)}, "
            f"extra={sorted(history_report_keys - history_raw_keys)}"
        )
    if history_report_keys != authority_document_keys:
        failures.append(
            "rulemaking history/authority final-document mismatch: "
            f"missing from history={sorted(authority_document_keys - history_report_keys)}, "
            f"extra={sorted(history_report_keys - authority_document_keys)}"
        )
    history_match_rows = [
        row for row in rulemaking_history_linkage
        if row.get("history_status") == "proposed_rule_history_match"
    ]
    if not history_match_rows:
        failures.append(f"{RULEMAKING_HISTORY_LINKAGE}: expected at least one proposed-rule history match")
    history_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rulemaking_history_linkage:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            history_by_public_law[public_law].append(row)
        boundary = row.get("claim_boundary", "")
        if (
            "complete public-comment records" not in boundary
            or "enforcement outcomes" not in boundary
            or "exhaustive implementation coverage" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: "
                "claim_boundary must reject complete comments, enforcement, exhaustive implementation, and model-validation claims"
            )
        try:
            candidate_count = int(row.get("candidate_proposed_rule_count", "0") or "0")
            matched_count = int(row.get("matched_proposed_rule_count", "0") or "0")
        except ValueError:
            failures.append(f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: proposed-rule counts must be integers")
            continue
        if matched_count > candidate_count:
            failures.append(
                f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: "
                f"matched_proposed_rule_count {matched_count} exceeds candidate count {candidate_count}"
            )
        if row.get("history_status") == "proposed_rule_history_match":
            if matched_count <= 0 or not row.get("proposed_document_numbers", "").strip():
                failures.append(
                    f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: history match missing proposed documents"
                )
            if not row.get("shared_identifiers", "").strip():
                failures.append(
                    f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: history match missing shared identifiers"
                )
            if "proposed_rule_shared_identifier_match" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: history match missing evidence layer"
                )
            if "proposed_rule_history" in row.get("missing_links", ""):
                failures.append(
                    f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: matched history row still lists proposed history as missing"
                )
        elif row.get("proposed_document_numbers", "").strip():
            failures.append(
                f"{RULEMAKING_HISTORY_LINKAGE}: {public_law}: unmatched history row should not carry proposed documents"
            )

    required_rulemaking_comment_columns = {
        "public_law_number",
        "bill_id",
        "final_document_number",
        "history_status",
        "matched_proposed_rule_count",
        "proposed_document_numbers",
        "proposed_comment_close_dates",
        "proposed_regulations_docket_ids",
        "proposed_regulations_comments_urls",
        "final_detail_status",
        "final_regulations_docket_id",
        "final_regulations_document_id",
        "final_regulations_agency_id",
        "final_regulations_comments_count",
        "final_regulations_supporting_documents_count",
        "final_regulations_checked_at",
        "final_regulations_comments_url",
        "final_comment_url",
        "final_comments_close_on",
        "proposed_detail_fetch_count",
        "proposed_regulations_docket_count",
        "proposed_regulations_docket_ids_refetched",
        "proposed_regulations_comment_url_count",
        "proposed_regulations_comments_urls_refetched",
        "proposed_comment_count_rows",
        "proposed_comment_count_total",
        "proposed_positive_comment_count_rows",
        "proposed_comments_close_date_count_refetched",
        "proposed_comments_close_dates_refetched",
        "comment_metadata_status",
        "source_urls",
        "api_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_comment_columns = required_rulemaking_comment_columns - set(rulemaking_comment_metadata[0])
    if missing_comment_columns:
        failures.append(
            f"{RULEMAKING_COMMENT_METADATA}: missing columns {sorted(missing_comment_columns)}"
        )
    comment_report_keys = {
        (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip())
        for row in rulemaking_comment_metadata
        if row.get("public_law_number", "").strip() and row.get("final_document_number", "").strip()
    }
    comment_raw_keys = {
        (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip())
        for row in rulemaking_comment_metadata_raw
        if row.get("public_law_number", "").strip() and row.get("final_document_number", "").strip()
    }
    if comment_report_keys != comment_raw_keys:
        failures.append(
            "rulemaking comment metadata report/raw mismatch: "
            f"missing from report={sorted(comment_raw_keys - comment_report_keys)}, "
            f"extra={sorted(comment_report_keys - comment_raw_keys)}"
        )
    if rulemaking_comment_metadata != rulemaking_comment_metadata_raw:
        failures.append(f"{RULEMAKING_COMMENT_METADATA}: report must mirror raw comment-metadata rows exactly")
    if comment_report_keys != history_report_keys:
        failures.append(
            "rulemaking comment metadata/history final-document mismatch: "
            f"missing from comment metadata={sorted(history_report_keys - comment_report_keys)}, "
            f"extra={sorted(comment_report_keys - history_report_keys)}"
        )
    history_by_key = {
        (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip()): row
        for row in rulemaking_history_linkage
        if row.get("public_law_number", "").strip() and row.get("final_document_number", "").strip()
    }
    allowed_comment_statuses = {
        "final_and_proposed_comment_metadata",
        "proposed_comment_metadata_only",
        "final_comment_metadata_only",
        "no_comment_metadata",
        "final_detail_error",
    }
    allowed_final_detail_statuses = {
        "federal_register_final_detail_fetched",
        "federal_register_final_detail_error",
    }
    comment_integer_fields = {
        "matched_proposed_rule_count",
        "proposed_detail_fetch_count",
        "proposed_regulations_docket_count",
        "proposed_regulations_comment_url_count",
        "proposed_comment_count_rows",
        "proposed_comment_count_total",
        "proposed_positive_comment_count_rows",
        "proposed_comments_close_date_count_refetched",
    }
    copied_history_fields = {
        "public_law_number",
        "bill_id",
        "final_document_number",
        "history_status",
        "matched_proposed_rule_count",
        "proposed_document_numbers",
        "proposed_comment_close_dates",
        "proposed_regulations_docket_ids",
        "proposed_regulations_comments_urls",
        "shared_identifiers",
        "days_from_earliest_proposed_to_final",
    }
    proposed_metadata_rows = 0
    proposed_comment_close_rows = 0
    for row in rulemaking_comment_metadata:
        key = (row.get("public_law_number", "").strip(), row.get("final_document_number", "").strip())
        public_law = key[0]
        history_row = history_by_key.get(key, {})
        for field in copied_history_fields:
            if row.get(field, "") != history_row.get(field, ""):
                failures.append(
                    f"{RULEMAKING_COMMENT_METADATA}: {public_law}: copied field {field} "
                    f"does not match {RULEMAKING_HISTORY_LINKAGE}"
                )
        if row.get("final_detail_status") not in allowed_final_detail_statuses:
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: invalid final_detail_status "
                f"{row.get('final_detail_status')!r}"
            )
        if row.get("comment_metadata_status") not in allowed_comment_statuses:
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: invalid comment_metadata_status "
                f"{row.get('comment_metadata_status')!r}"
            )
        for field in comment_integer_fields:
            try:
                value = int(row.get(field, "0") or "0")
            except ValueError:
                failures.append(f"{RULEMAKING_COMMENT_METADATA}: {public_law}: {field} must be an integer")
                continue
            if value < 0:
                failures.append(f"{RULEMAKING_COMMENT_METADATA}: {public_law}: {field} must be nonnegative")
        for optional_count_field in (
            "final_regulations_comments_count",
            "final_regulations_supporting_documents_count",
        ):
            if row.get(optional_count_field, "").strip():
                try:
                    value = int(row.get(optional_count_field, "0") or "0")
                except ValueError:
                    failures.append(
                        f"{RULEMAKING_COMMENT_METADATA}: {public_law}: {optional_count_field} must be an integer when present"
                    )
                    continue
                if value < 0:
                    failures.append(
                        f"{RULEMAKING_COMMENT_METADATA}: {public_law}: {optional_count_field} must be nonnegative"
                    )
        final_metadata = any(
            row.get(field, "").strip()
            for field in (
                "final_regulations_docket_id",
                "final_regulations_document_id",
                "final_regulations_comments_count",
                "final_regulations_comments_url",
                "final_comment_url",
                "final_comments_close_on",
            )
        )
        proposed_metadata = any(
            row.get(field, "").strip()
            for field in (
                "proposed_regulations_docket_ids_refetched",
                "proposed_regulations_comments_urls_refetched",
                "proposed_comments_close_dates_refetched",
            )
        ) or any(
            int(row.get(field, "0") or "0") > 0
            for field in (
                "proposed_regulations_docket_count",
                "proposed_regulations_comment_url_count",
                "proposed_comment_count_rows",
                "proposed_comments_close_date_count_refetched",
            )
        )
        if proposed_metadata:
            proposed_metadata_rows += 1
        if row.get("proposed_comments_close_dates_refetched", "").strip():
            proposed_comment_close_rows += 1
        if row.get("final_detail_status") == "federal_register_final_detail_error":
            expected_status = "final_detail_error"
        elif final_metadata and proposed_metadata:
            expected_status = "final_and_proposed_comment_metadata"
        elif proposed_metadata:
            expected_status = "proposed_comment_metadata_only"
        elif final_metadata:
            expected_status = "final_comment_metadata_only"
        else:
            expected_status = "no_comment_metadata"
        if row.get("comment_metadata_status") != expected_status:
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: comment_metadata_status "
                f"{row.get('comment_metadata_status')!r} does not match expected {expected_status!r}"
            )
        boundary = row.get("claim_boundary", "")
        if (
            "complete Regulations.gov comment-record evidence" not in boundary
            or "enforcement outcomes" not in boundary
            or "model validation" not in boundary
        ):
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: "
                "claim_boundary must reject complete comments, enforcement, and model-validation claims"
            )
        if (
            (final_metadata or proposed_metadata)
            and "federal_register_exposed_regulations_gov_comment_metadata" not in row.get("evidence_layers", "")
        ):
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: metadata row missing comment-metadata evidence layer"
            )
        if "complete_regulations_comments" not in row.get("missing_links", ""):
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA}: {public_law}: comment metadata must preserve complete-comments gap"
            )
    if proposed_metadata_rows == 0:
        failures.append(f"{RULEMAKING_COMMENT_METADATA}: expected at least one proposed-rule comment metadata row")
    if proposed_comment_close_rows == 0:
        failures.append(f"{RULEMAKING_COMMENT_METADATA}: expected at least one proposed-rule comment-close metadata row")
    if not RULEMAKING_COMMENT_METADATA_MD.exists():
        failures.append(f"{RULEMAKING_COMMENT_METADATA_MD}: missing markdown report")
    else:
        comment_md = RULEMAKING_COMMENT_METADATA_MD.read_text()
        if "Federal Register-exposed Regulations.gov metadata" not in comment_md:
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA_MD}: must summarize Federal Register-exposed Regulations.gov metadata"
            )
        if "not complete comment-record" not in comment_md:
            failures.append(
                f"{RULEMAKING_COMMENT_METADATA_MD}: must preserve the incomplete-comment-record boundary"
            )

    required_comment_record_columns = {
        "public_law_number",
        "bill_id",
        "docket_id",
        "source_contexts",
        "final_document_numbers",
        "proposed_document_numbers",
        "expected_comment_count",
        "expected_comment_count_source",
        "retrieval_status",
        "retrieval_detail",
        "api_key_mode",
        "api_total_comment_count",
        "retrieved_comment_count",
        "retrieved_comment_ids",
        "retrieved_comment_document_types",
        "retrieved_comment_posted_dates",
        "withdrawn_comment_count",
        "api_urls",
        "source_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_comment_record_columns = required_comment_record_columns - set(rulemaking_comment_records[0])
    if missing_comment_record_columns:
        failures.append(
            f"{RULEMAKING_COMMENT_RECORDS}: missing columns {sorted(missing_comment_record_columns)}"
        )
    comment_record_report_keys = {
        (row.get("public_law_number", "").strip(), row.get("docket_id", "").strip())
        for row in rulemaking_comment_records
        if row.get("public_law_number", "").strip() and row.get("docket_id", "").strip()
    }
    comment_record_raw_keys = {
        (row.get("public_law_number", "").strip(), row.get("docket_id", "").strip())
        for row in rulemaking_comment_records_raw
        if row.get("public_law_number", "").strip() and row.get("docket_id", "").strip()
    }
    if comment_record_report_keys != comment_record_raw_keys:
        failures.append(
            "rulemaking comment records report/raw mismatch: "
            f"missing from report={sorted(comment_record_raw_keys - comment_record_report_keys)}, "
            f"extra={sorted(comment_record_report_keys - comment_record_raw_keys)}"
        )
    if rulemaking_comment_records != rulemaking_comment_records_raw:
        failures.append(f"{RULEMAKING_COMMENT_RECORDS}: report must mirror raw comment-record rows exactly")
    allowed_comment_record_statuses = {
        "complete_comment_record_metadata_retrieved",
        "complete_no_comments_expected",
        "skipped_high_volume_comment_docket",
        "api_key_required",
        "partial_comment_record_metadata_retrieved",
        "partial_comment_record_metadata_api_error",
        "comment_record_count_mismatch",
        "comment_record_api_error",
        "expected_comment_count_unknown",
    }
    complete_comment_record_statuses = {
        "complete_comment_record_metadata_retrieved",
        "complete_no_comments_expected",
    }
    for row in rulemaking_comment_records:
        key = (row.get("public_law_number", "").strip(), row.get("docket_id", "").strip())
        if row.get("retrieval_status") not in allowed_comment_record_statuses:
            failures.append(
                f"{RULEMAKING_COMMENT_RECORDS}: {key}: invalid retrieval_status "
                f"{row.get('retrieval_status')!r}"
            )
        for field in (
            "expected_comment_count",
            "api_total_comment_count",
            "retrieved_comment_count",
            "withdrawn_comment_count",
        ):
            if row.get(field, "").strip():
                value = parse_int(row.get(field, ""))
                if value is None or value < 0:
                    failures.append(f"{RULEMAKING_COMMENT_RECORDS}: {key}: {field} must be a nonnegative integer when present")
        expected_count = parse_int(row.get("expected_comment_count", ""))
        retrieved_count = parse_int(row.get("retrieved_comment_count", "")) or 0
        api_total = parse_int(row.get("api_total_comment_count", ""))
        retrieved_ids = split_semicolon_values(row, "retrieved_comment_ids")
        row_is_complete = row.get("retrieval_status") in complete_comment_record_statuses
        if row.get("retrieval_status") == "complete_comment_record_metadata_retrieved":
            if expected_count is None:
                failures.append(f"{RULEMAKING_COMMENT_RECORDS}: {key}: complete retrieved row needs an expected count")
            elif retrieved_count != expected_count or api_total != expected_count:
                failures.append(
                    f"{RULEMAKING_COMMENT_RECORDS}: {key}: complete row count mismatch "
                    f"expected={expected_count} retrieved={retrieved_count} api_total={api_total}"
                )
            if len(retrieved_ids) != retrieved_count:
                failures.append(
                    f"{RULEMAKING_COMMENT_RECORDS}: {key}: retrieved_comment_ids count "
                    f"{len(retrieved_ids)} does not match retrieved count {retrieved_count}"
                )
        if row.get("retrieval_status") == "complete_no_comments_expected":
            if expected_count != 0 or retrieved_count != 0:
                failures.append(
                    f"{RULEMAKING_COMMENT_RECORDS}: {key}: zero-comment complete row must have expected/retrieved counts of 0"
                )
        if row_is_complete:
            if "regulations_gov_complete_comment_record_metadata" not in row.get("evidence_layers", ""):
                failures.append(f"{RULEMAKING_COMMENT_RECORDS}: {key}: complete row missing complete comment-record evidence layer")
            if "complete_regulations_comments" in row.get("missing_links", ""):
                failures.append(f"{RULEMAKING_COMMENT_RECORDS}: {key}: complete row must not preserve complete-comments gap")
        elif "complete_regulations_comments" not in row.get("missing_links", ""):
            failures.append(f"{RULEMAKING_COMMENT_RECORDS}: {key}: incomplete row must preserve complete-comments gap")
        if retrieved_count > 0 and not row_is_complete:
            if "regulations_gov_partial_comment_record_metadata" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{RULEMAKING_COMMENT_RECORDS}: {key}: incomplete row with retrieved records "
                    "must carry partial comment-record evidence layer"
                )
            if len(retrieved_ids) != retrieved_count:
                failures.append(
                    f"{RULEMAKING_COMMENT_RECORDS}: {key}: retrieved_comment_ids count "
                    f"{len(retrieved_ids)} does not match retrieved count {retrieved_count}"
                )
        if retrieved_count == 0 and not row_is_complete and "regulations_gov_partial_comment_record_metadata" in row.get("evidence_layers", ""):
            failures.append(
                f"{RULEMAKING_COMMENT_RECORDS}: {key}: zero-retrieval incomplete row "
                "must not carry partial comment-record evidence layer"
            )
        boundary = row.get("claim_boundary", "")
        if (
            "comment-text" not in boundary
            or "commenter-identity" not in boundary
            or "implementation-outcome" not in boundary
            or "model-validation" not in boundary
        ):
            failures.append(
                f"{RULEMAKING_COMMENT_RECORDS}: {key}: "
                "claim_boundary must reject comment text, identity, implementation, and model-validation claims"
            )
    if not RULEMAKING_COMMENT_RECORDS_MD.exists():
        failures.append(f"{RULEMAKING_COMMENT_RECORDS_MD}: missing markdown report")
    else:
        records_md = RULEMAKING_COMMENT_RECORDS_MD.read_text()
        if "comment-record metadata" not in records_md or "Claim boundary" not in records_md:
            failures.append(
                f"{RULEMAKING_COMMENT_RECORDS_MD}: must summarize comment-record metadata and claim boundary"
            )

    required_comment_text_columns = {
        "public_law_number",
        "bill_id",
        "docket_id",
        "comment_id",
        "comment_record_retrieval_status",
        "comment_detail_review_scope",
        "source_retrieved_comment_count",
        "source_expected_comment_count",
        "detail_fetch_status",
        "api_key_mode",
        "document_type",
        "posted_date",
        "receive_date",
        "modify_date",
        "withdrawn",
        "comment_on_document_id",
        "comment_text_available",
        "comment_text_character_count",
        "comment_text_word_count",
        "comment_text_sha256",
        "implementation_timing_cue",
        "cost_or_burden_cue",
        "compliance_or_standard_cue",
        "safety_or_security_cue",
        "program_design_cue",
        "cue_terms",
        "attachment_count",
        "attachment_detail_status",
        "omitted_fields",
        "api_urls",
        "source_urls",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_comment_text_columns = required_comment_text_columns - set(rulemaking_comment_text_review[0])
    if missing_comment_text_columns:
        failures.append(
            f"{RULEMAKING_COMMENT_TEXT_REVIEW}: missing columns {sorted(missing_comment_text_columns)}"
        )
    if rulemaking_comment_text_review != rulemaking_comment_text_review_raw:
        failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: report must mirror raw comment-text review rows exactly")
    forbidden_comment_text_columns = {
        "comment",
        "comment_body",
        "firstName",
        "lastName",
        "address1",
        "address2",
        "city",
        "stateProvinceRegion",
        "zip",
        "email",
        "phone",
        "fax",
        "organization",
        "trackingNbr",
    }
    leaked_columns = forbidden_comment_text_columns & set(rulemaking_comment_text_review[0])
    if leaked_columns:
        failures.append(
            f"{RULEMAKING_COMMENT_TEXT_REVIEW}: must not expose body/submitter columns {sorted(leaked_columns)}"
        )
    comment_detail_sources: dict[tuple[str, str, str], dict[str, str]] = {}
    for record_row in rulemaking_comment_records:
        for comment_id in split_semicolon_values(record_row, "retrieved_comment_ids"):
            comment_detail_sources[
                (
                    record_row.get("public_law_number", "").strip(),
                    record_row.get("docket_id", "").strip(),
                    comment_id,
                )
            ] = record_row
    complete_scope_rows = 0
    partial_scope_rows = 0
    expected_scopes = {
        "complete_comment_record_metadata_retrieved": "complete_docket_detail",
    }
    expected_layers = {
        "complete_docket_detail": "regulations_gov_complete_comment_record_metadata",
        "partial_docket_sample_detail": "regulations_gov_partial_comment_record_metadata",
    }
    for row in rulemaking_comment_text_review:
        scope = row.get("comment_detail_review_scope", "")
        if scope == "complete_docket_detail":
            complete_scope_rows += 1
        elif scope == "partial_docket_sample_detail":
            partial_scope_rows += 1
        else:
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW}: "
                f"{(row.get('public_law_number', ''), row.get('docket_id', ''), row.get('comment_id', ''))}: "
                "comment_detail_review_scope must be complete_docket_detail or partial_docket_sample_detail"
            )
    if complete_scope_rows == 0:
        failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: expected at least one complete-docket detail row")
    if partial_scope_rows == 0:
        failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: expected at least one partial-docket sampled detail row")
    text_available_rows = 0
    for row in rulemaking_comment_text_review:
        key = (
            row.get("public_law_number", "").strip(),
            row.get("docket_id", "").strip(),
            row.get("comment_id", "").strip(),
        )
        source_record = comment_detail_sources.get(key)
        if source_record is None:
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: row must derive from a comment-record metadata row with a retrieved comment ID"
            )
        else:
            source_status = source_record.get("retrieval_status", "")
            expected_scope = expected_scopes.get(source_status, "partial_docket_sample_detail")
            if row.get("comment_record_retrieval_status") != source_status:
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: source retrieval status must mirror comment-record source"
                )
            if row.get("comment_detail_review_scope") != expected_scope:
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: review scope must match source retrieval status"
                )
            if row.get("source_retrieved_comment_count") != source_record.get("retrieved_comment_count", ""):
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: source_retrieved_comment_count must mirror comment-record source"
                )
            if row.get("source_expected_comment_count") != source_record.get("expected_comment_count", ""):
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: source_expected_comment_count must mirror comment-record source"
                )
            evidence_layers = row.get("evidence_layers", "")
            expected_layer = expected_layers.get(row.get("comment_detail_review_scope", ""))
            if expected_layer and expected_layer not in evidence_layers:
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: missing source evidence layer {expected_layer}"
                )
            if row.get("comment_detail_review_scope") == "partial_docket_sample_detail":
                if "complete_regulations_comments" not in row.get("missing_links", ""):
                    failures.append(
                        f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: partial sampled rows must preserve complete-comment-coverage gap"
                    )
        if row.get("detail_fetch_status") != "comment_detail_fetched":
            if "complete_public_comment_detail" not in row.get("missing_links", ""):
                failures.append(
                    f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: incomplete detail fetch must preserve detail gap"
                )
        for field in (
            "comment_text_character_count",
            "comment_text_word_count",
            "attachment_count",
        ):
            value = parse_int(row.get(field, ""))
            if value is None or value < 0:
                failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: {field} must be a nonnegative integer")
        for cue_field in (
            "implementation_timing_cue",
            "cost_or_burden_cue",
            "compliance_or_standard_cue",
            "safety_or_security_cue",
            "program_design_cue",
        ):
            if row.get(cue_field) not in {"yes", "no"}:
                failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: {cue_field} must be yes/no")
        if row.get("comment_text_available") == "yes":
            text_available_rows += 1
            if len(row.get("comment_text_sha256", "")) != 64:
                failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: available text must have sha256 hash")
            if (parse_int(row.get("comment_text_character_count", "")) or 0) <= 0:
                failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: available text must have positive length")
            if "sanitized_comment_text_availability_hash" not in row.get("evidence_layers", ""):
                failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: available text missing sanitized hash evidence layer")
        elif row.get("comment_text_available") != "no":
            failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: comment_text_available must be yes/no")
        if "regulations_gov_public_comment_detail_metadata" not in row.get("evidence_layers", "") and row.get("detail_fetch_status") == "comment_detail_fetched":
            failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: fetched detail row missing detail metadata evidence layer")
        omitted_fields = row.get("omitted_fields", "")
        if "comment_body" not in omitted_fields or "email" not in omitted_fields or "trackingNbr" not in omitted_fields:
            failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: omitted_fields must document body/contact omissions")
        boundary = row.get("claim_boundary", "")
        if (
            "full comment-text corpus" not in boundary
            or "commenter-identity validation" not in boundary
            or "Partial sample rows do not prove complete docket coverage" not in boundary
            or "implementation-outcome" not in boundary
            or "model-validation" not in boundary
        ):
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: "
                "claim_boundary must reject corpus, identity, implementation, and model-validation claims"
            )
        if (
            "full_comment_text_corpus" not in row.get("missing_links", "")
            or "commenter_identity_review" not in row.get("missing_links", "")
            or "model_validation" not in row.get("missing_links", "")
        ):
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW}: {key}: missing_links must preserve corpus, identity, and validation gaps"
            )
    if text_available_rows == 0:
        if not all(row.get("detail_fetch_status", "").startswith("comment_detail_api_error:") for row in rulemaking_comment_text_review):
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW}: zero text-available rows require explicit API-error statuses"
            )
    if not RULEMAKING_COMMENT_TEXT_REVIEW_MD.exists():
        failures.append(f"{RULEMAKING_COMMENT_TEXT_REVIEW_MD}: missing markdown report")
    else:
        text_review_md = RULEMAKING_COMMENT_TEXT_REVIEW_MD.read_text()
        if "sanitized Regulations.gov public comment-detail review" not in text_review_md:
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW_MD}: must summarize sanitized public comment-detail review"
            )
        if "does not include the full comment body" not in text_review_md:
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW_MD}: must preserve no-full-comment-body boundary"
            )
        if "Partial sample rows do not prove complete docket coverage" not in text_review_md:
            failures.append(
                f"{RULEMAKING_COMMENT_TEXT_REVIEW_MD}: must preserve partial-sample boundary"
            )

    comment_metadata_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rulemaking_comment_metadata:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            comment_metadata_by_public_law[public_law].append(row)
    comment_records_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rulemaking_comment_records:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            comment_records_by_public_law[public_law].append(row)
    statutory_adjudication_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_adjudication:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_adjudication_by_public_law[public_law].append(row)
    statutory_review_packets_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_review_packets:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_review_packets_by_public_law[public_law].append(row)
    statutory_diff_review_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_target_section_diff_review:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_diff_review_by_public_law[public_law].append(row)
    statutory_no_target_review_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statutory_lineage_no_target_review:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            statutory_no_target_review_by_public_law[public_law].append(row)

    court_by_public_law: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in court_law_linkage:
        if row.get("linkage_status") != "usc_section_authority_overlap":
            continue
        for public_law in row.get("public_law_numbers", "").split(";"):
            public_law = public_law.strip()
            if public_law:
                court_by_public_law[public_law].append(row)

    district_policy_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for policy_row in district_public_opinion_policy_context:
        bill_id = policy_row.get("bill_id", "").strip()
        if bill_id:
            district_policy_by_bill[bill_id].append(policy_row)
    campaign_context_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for campaign_context_row in campaign_finance_sponsor_bill_context:
        for policy_area in split_semicolon_values(campaign_context_row, "matched_policy_areas"):
            campaign_context_by_policy_area[policy_area].append(campaign_context_row)
    lobbying_context_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for lobbying_context_row in lobbying_bill_policy_context:
        if lobbying_context_row.get("policy_context_status") != "lobbying_issue_bill_policy_context":
            continue
        policy_area = lobbying_context_row.get("topic", "").strip()
        if policy_area:
            lobbying_context_by_policy_area[policy_area].append(lobbying_context_row)

    for row in bill_law_spine:
        bill_id = row.get("bill_id", "").strip()
        public_law = row.get("public_law_number", "").strip()
        policy_area = row.get("policy_area", "").strip()
        expected_adjudication_rows = statutory_adjudication_by_public_law.get(public_law, [])
        expected_marker_rows = [
            adjudication_row for adjudication_row in expected_adjudication_rows
            if adjudication_row.get("codified_lineage_marker", "") == "1"
        ]
        expected_marker_statuses = {
            adjudication_row.get("lineage_adjudication_status", "").strip()
            for adjudication_row in expected_marker_rows
            if adjudication_row.get("lineage_adjudication_status", "").strip()
        }
        expected_marker_strengths = {
            adjudication_row.get("lineage_marker_strength", "").strip()
            for adjudication_row in expected_marker_rows
            if adjudication_row.get("lineage_marker_strength", "").strip()
        }
        expected_marker_targets = {
            adjudication_row.get("target_reference", "").strip()
            for adjudication_row in expected_marker_rows
            if adjudication_row.get("target_reference", "").strip()
        }
        expected_packet_rows = statutory_review_packets_by_public_law.get(public_law, [])
        expected_ready_packet_rows = [
            packet_row for packet_row in expected_packet_rows
            if packet_row.get("target_review_packet_status", "").strip()
            != "target_section_review_packet_needs_manual_source_retrieval"
        ]
        expected_packet_statuses = {
            packet_row.get("target_review_packet_status", "").strip()
            for packet_row in expected_packet_rows
            if packet_row.get("target_review_packet_status", "").strip()
        }
        expected_packet_strengths = {
            packet_row.get("target_review_packet_strength", "").strip()
            for packet_row in expected_packet_rows
            if packet_row.get("target_review_packet_strength", "").strip()
        }
        expected_packet_context_count = sum(
            parse_int(packet_row.get("post_public_law_context_count", "0")) or 0
            for packet_row in expected_packet_rows
        )
        expected_packet_source_reviewed_rows = sum(
            1 for packet_row in expected_packet_rows
            if packet_row.get("source_reviewed_target_section_diff", "").strip() == "1"
        )
        expected_diff_review_rows = statutory_diff_review_by_public_law.get(public_law, [])
        expected_diff_review_source_reviewed_rows = [
            review_row for review_row in expected_diff_review_rows
            if review_row.get("source_reviewed_target_section_diff", "").strip() == "1"
        ]
        expected_diff_review_statuses = {
            review_row.get("review_status", "").strip()
            for review_row in expected_diff_review_rows
            if review_row.get("review_status", "").strip()
        }
        expected_diff_review_relationships = {
            review_row.get("codified_lineage_relationship", "").strip()
            for review_row in expected_diff_review_rows
            if review_row.get("codified_lineage_relationship", "").strip()
        }
        expected_no_target_review_rows = statutory_no_target_review_by_public_law.get(public_law, [])
        expected_no_target_review_statuses = {
            review_row.get("review_status", "").strip()
            for review_row in expected_no_target_review_rows
            if review_row.get("review_status", "").strip()
        }
        expected_no_target_review_dispositions = {
            review_row.get("codification_disposition", "").strip()
            for review_row in expected_no_target_review_rows
            if review_row.get("codification_disposition", "").strip()
        }
        try:
            spine_adjudication_rows = int(row.get("statutory_lineage_adjudication_rows", "0") or "0")
            spine_marker_rows = int(row.get("statutory_lineage_marker_rows", "0") or "0")
            spine_marker_pre_anchor_rows = int(row.get("statutory_lineage_marker_pre_anchor_rows", "0") or "0")
            spine_marker_post_anchor_rows = int(row.get("statutory_lineage_marker_post_anchor_rows", "0") or "0")
            spine_marker_context_count = int(
                row.get("statutory_lineage_marker_public_law_context_count", "0") or "0"
            )
            spine_packet_rows = int(row.get("statutory_lineage_target_review_packet_rows", "0") or "0")
            spine_ready_packet_rows = int(
                row.get("statutory_lineage_target_review_ready_packet_rows", "0") or "0"
            )
            spine_packet_context_count = int(
                row.get("statutory_lineage_target_review_packet_public_law_context_count", "0") or "0"
            )
            spine_diff_review_rows = int(
                row.get("statutory_lineage_target_section_diff_review_rows", "0") or "0"
            )
            spine_source_reviewed_diff_rows = int(
                row.get("statutory_lineage_source_reviewed_target_section_diff_rows", "0") or "0"
            )
            spine_no_target_review_rows = int(
                row.get("statutory_lineage_no_target_review_rows", "0") or "0"
            )
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage marker counts must be integers")
            spine_adjudication_rows = 0
            spine_marker_rows = 0
            spine_marker_pre_anchor_rows = 0
            spine_marker_post_anchor_rows = 0
            spine_marker_context_count = 0
            spine_packet_rows = 0
            spine_ready_packet_rows = 0
            spine_packet_context_count = 0
            spine_diff_review_rows = 0
            spine_source_reviewed_diff_rows = 0
            spine_no_target_review_rows = 0
        if spine_adjudication_rows != len(expected_adjudication_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage adjudication rows "
                f"{spine_adjudication_rows} do not match {STATUTORY_LINEAGE_ADJUDICATION} "
                f"rows {len(expected_adjudication_rows)}"
            )
        if spine_marker_rows != len(expected_marker_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage marker rows "
                f"{spine_marker_rows} do not match {STATUTORY_LINEAGE_ADJUDICATION} "
                f"rows {len(expected_marker_rows)}"
            )
        if split_semicolon_values(row, "statutory_lineage_marker_statuses") != expected_marker_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage marker statuses do not match "
                f"{STATUTORY_LINEAGE_ADJUDICATION}"
            )
        if split_semicolon_values(row, "statutory_lineage_marker_strengths") != expected_marker_strengths:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage marker strengths do not match "
                f"{STATUTORY_LINEAGE_ADJUDICATION}"
            )
        if split_semicolon_values(row, "statutory_lineage_marker_target_references") != expected_marker_targets:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage marker targets do not match "
                f"{STATUTORY_LINEAGE_ADJUDICATION}"
            )
        expected_pre_anchor_rows = sum(
            1 for adjudication_row in expected_marker_rows
            if adjudication_row.get("pre_section_anchor_status", "") == "section_anchor_found"
        )
        expected_post_anchor_rows = sum(
            1 for adjudication_row in expected_marker_rows
            if adjudication_row.get("post_section_anchor_status", "") == "section_anchor_found"
        )
        expected_marker_context_count = sum(
            parse_int(adjudication_row.get("post_public_law_context_count", "0")) or 0
            for adjudication_row in expected_marker_rows
        )
        if spine_marker_pre_anchor_rows != expected_pre_anchor_rows:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage pre-anchor row mismatch")
        if spine_marker_post_anchor_rows != expected_post_anchor_rows:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage post-anchor row mismatch")
        if spine_marker_context_count != expected_marker_context_count:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage context count mismatch")
        if spine_packet_rows != len(expected_packet_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage packet rows "
                f"{spine_packet_rows} do not match {STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS} "
                f"rows {len(expected_packet_rows)}"
            )
        if spine_ready_packet_rows != len(expected_ready_packet_rows):
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage ready packet row mismatch")
        if split_semicolon_values(row, "statutory_lineage_target_review_packet_statuses") != expected_packet_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage packet statuses do not match "
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}"
            )
        if split_semicolon_values(row, "statutory_lineage_target_review_packet_strengths") != expected_packet_strengths:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage packet strengths do not match "
                f"{STATUTORY_LINEAGE_TARGET_REVIEW_PACKETS}"
            )
        if spine_packet_context_count != expected_packet_context_count:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage packet context count mismatch")
        if expected_packet_source_reviewed_rows != len(expected_diff_review_source_reviewed_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: review packet source-reviewed annotations "
                f"{expected_packet_source_reviewed_rows} do not match diff-review source-reviewed rows "
                f"{len(expected_diff_review_source_reviewed_rows)}"
            )
        if spine_diff_review_rows != len(expected_diff_review_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage diff review rows "
                f"{spine_diff_review_rows} do not match {STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW} "
                f"rows {len(expected_diff_review_rows)}"
            )
        if split_semicolon_values(row, "statutory_lineage_target_section_diff_review_statuses") != expected_diff_review_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage diff review statuses do not match "
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}"
            )
        if split_semicolon_values(row, "statutory_lineage_target_section_diff_review_relationships") != expected_diff_review_relationships:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage diff review relationships do not match "
                f"{STATUTORY_LINEAGE_TARGET_SECTION_DIFF_REVIEW}"
            )
        if spine_source_reviewed_diff_rows != len(expected_diff_review_source_reviewed_rows):
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage source-reviewed diff count mismatch")
        if spine_no_target_review_rows != len(expected_no_target_review_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage no-target review rows "
                f"{spine_no_target_review_rows} do not match {STATUTORY_LINEAGE_NO_TARGET_REVIEW} "
                f"rows {len(expected_no_target_review_rows)}"
            )
        if split_semicolon_values(row, "statutory_lineage_no_target_review_statuses") != expected_no_target_review_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage no-target review statuses do not match "
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}"
            )
        if split_semicolon_values(row, "statutory_lineage_no_target_review_dispositions") != expected_no_target_review_dispositions:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: statutory-lineage no-target dispositions do not match "
                f"{STATUTORY_LINEAGE_NO_TARGET_REVIEW}"
            )
        if expected_marker_rows:
            if "official_olrc_public_law_marker_adjudication" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: missing OLRC marker adjudication evidence layer"
                )
            if "official_olrc_post_only_public_law_marker" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: missing OLRC post-only marker evidence layer"
                )
            if "codified_usc_lineage" not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: OLRC marker evidence must preserve codified-lineage gap"
                )
        else:
            if "official_olrc_public_law_marker_adjudication" in row.get("evidence_layers", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: row without marker evidence should not carry OLRC marker layer"
                )
        if expected_packet_rows:
            if "statutory_lineage_target_section_review_packet" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing target review packet evidence layer")
            if "codified_usc_lineage" not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: target review packets must preserve codified-lineage gap"
                )
        elif "statutory_lineage_target_section_review_packet" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: row without packets should not carry target review packet layer"
            )
        if expected_diff_review_rows:
            if "statutory_lineage_target_section_diff_review" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing target-section diff review evidence layer")
            if expected_diff_review_source_reviewed_rows and "statutory_lineage_source_reviewed_target_section_diff" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing source-reviewed target-section diff evidence layer")
            if "public_law_causal_attribution" not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: diff review must preserve public-law causal attribution gap"
                )
        elif "statutory_lineage_target_section_diff_review" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: row without diff review should not carry diff review layer"
            )
        if expected_no_target_review_rows:
            if "statutory_lineage_no_target_review" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing no-target review evidence layer")
            if "statutory_lineage_source_reviewed_no_structured_usc_target" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing source-reviewed no-structured-target layer")
            if "codified_usc_lineage" in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: reviewed designation no-target row should close codified_usc_lineage gate"
                )
            for required_gap in (
                "target_section_diff_not_applicable_designation_law",
                "public_law_causal_attribution_not_applicable_no_target",
                "law_revision_effective_text_not_applicable_no_target",
                "model_validation",
            ):
                if required_gap not in row.get("missing_links", ""):
                    failures.append(
                        f"{BILL_LAW_SPINE}: {bill_id}: no-target row missing {required_gap}"
                    )
        elif "statutory_lineage_no_target_review" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: row without no-target review should not carry no-target layer"
            )
        expected_policy_rows = district_policy_by_bill.get(bill_id, [])
        expected_policy_keys = {
            (
                policy_row.get("district_id", "").strip(),
                policy_row.get("issue", "").strip(),
                policy_row.get("year", "").strip(),
            )
            for policy_row in expected_policy_rows
            if (
                policy_row.get("district_id", "").strip()
                and policy_row.get("issue", "").strip()
                and policy_row.get("year", "").strip()
            )
        }
        expected_policy_areas = {
            policy_row.get("policy_area", "").strip()
            for policy_row in expected_policy_rows
            if policy_row.get("policy_area", "").strip()
        }
        expected_policy_topic_totals = district_policy_topic_totals(expected_policy_rows)
        spine_policy_areas = {
            policy_area.strip()
            for policy_area in row.get("district_public_opinion_policy_areas", "").split(";")
            if policy_area.strip()
        }
        try:
            spine_policy_rows = int(row.get("district_public_opinion_policy_context_rows", "0") or "0")
            spine_policy_keys = int(row.get("district_public_opinion_policy_context_unique_keys", "0") or "0")
            spine_policy_introduced = int(row.get("district_public_opinion_policy_topic_introduced", "0") or "0")
            spine_policy_floor = int(row.get("district_public_opinion_policy_topic_floor_considered", "0") or "0")
            spine_policy_enacted = int(row.get("district_public_opinion_policy_topic_enacted", "0") or "0")
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: district policy-context counts must be integers")
            spine_policy_rows = 0
            spine_policy_keys = 0
            spine_policy_introduced = 0
            spine_policy_floor = 0
            spine_policy_enacted = 0
        if spine_policy_rows != len(expected_policy_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: district policy-context rows {spine_policy_rows} "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT} rows {len(expected_policy_rows)}"
            )
        if spine_policy_keys != len(expected_policy_keys):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: district policy-context unique keys {spine_policy_keys} "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT} keys {len(expected_policy_keys)}"
            )
        if spine_policy_areas != expected_policy_areas:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: district policy-area set does not match "
                f"{DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT}"
            )
        expected_introduced = expected_policy_topic_totals["topic_introduced"]
        expected_floor = expected_policy_topic_totals["topic_floor_considered"]
        expected_enacted = expected_policy_topic_totals["topic_enacted"]
        if (
            spine_policy_introduced != expected_introduced
            or spine_policy_floor != expected_floor
            or spine_policy_enacted != expected_enacted
        ):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: district policy topic counts "
                f"({spine_policy_introduced}, {spine_policy_floor}, {spine_policy_enacted}) "
                f"do not match {DISTRICT_PUBLIC_OPINION_POLICY_CONTEXT} "
                f"({expected_introduced}, {expected_floor}, {expected_enacted})"
            )
        if expected_policy_rows:
            if "sponsor_district_bill_policy_area_context" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing policy-context evidence layer")
            if "topic_throughput_policy_area" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing topic-throughput evidence layer")
            if "sponsor_district_bill_policy_area_context" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: mapped row still lists policy context as missing")
            if "bill_topic_public_opinion" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: policy context must not remove bill-topic opinion gap")
            if "policy-area context" not in row.get("claim_boundary", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: claim boundary must mention policy-area context")
        else:
            if "sponsor_district_bill_policy_area_context" in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should not carry policy-context evidence")
            if "sponsor_district_bill_policy_area_context" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should list policy context as missing")
        expected_campaign_context_rows = campaign_context_by_policy_area.get(policy_area, [])
        expected_campaign_bill_ids = {
            value
            for campaign_context_row in expected_campaign_context_rows
            for value in split_semicolon_values(campaign_context_row, "matched_bill_ids")
        }
        expected_campaign_enacted_bill_ids = {
            value
            for campaign_context_row in expected_campaign_context_rows
            for value in split_semicolon_values(campaign_context_row, "matched_enacted_bill_ids")
        }
        expected_campaign_candidates = {
            campaign_context_row.get("candidate_id", "").strip()
            or campaign_context_row.get("bioguide_id", "").strip()
            for campaign_context_row in expected_campaign_context_rows
            if (
                campaign_context_row.get("candidate_id", "").strip()
                or campaign_context_row.get("bioguide_id", "").strip()
            )
        }
        try:
            spine_campaign_context_rows = int(row.get("campaign_finance_sponsor_policy_context_rows", "0") or "0")
            spine_campaign_transaction_rows = int(
                row.get("campaign_finance_sponsor_policy_context_transaction_rows", "0") or "0"
            )
            spine_campaign_unique_candidates = int(
                row.get("campaign_finance_sponsor_policy_context_unique_candidates", "0") or "0"
            )
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance policy-context counts must be integers")
            spine_campaign_context_rows = 0
            spine_campaign_transaction_rows = 0
            spine_campaign_unique_candidates = 0
        expected_campaign_transaction_rows = sum(
            parse_int(campaign_context_row.get("member_context_transaction_rows", "0")) or 0
            for campaign_context_row in expected_campaign_context_rows
        )
        if spine_campaign_context_rows != len(expected_campaign_context_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance policy-context rows "
                f"{spine_campaign_context_rows} do not match {CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT} "
                f"rows {len(expected_campaign_context_rows)}"
            )
        if spine_campaign_transaction_rows != expected_campaign_transaction_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance transaction rows "
                f"{spine_campaign_transaction_rows} do not match expected "
                f"{expected_campaign_transaction_rows}"
            )
        if spine_campaign_unique_candidates != len(expected_campaign_candidates):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance unique candidates "
                f"{spine_campaign_unique_candidates} do not match expected "
                f"{len(expected_campaign_candidates)}"
            )
        if split_semicolon_values(row, "campaign_finance_sponsor_policy_context_bill_ids") != expected_campaign_bill_ids:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance policy-context bill set "
                f"does not match {CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}"
            )
        if (
            split_semicolon_values(row, "campaign_finance_sponsor_policy_context_enacted_bill_ids")
            != expected_campaign_enacted_bill_ids
        ):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: campaign-finance policy-context enacted bill set "
                f"does not match {CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}"
            )
        if expected_campaign_context_rows:
            if "campaign_finance_sponsor_policy_area_context" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing campaign-finance policy-context evidence layer")
            if "campaign_finance_sponsor_policy_area_context" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: mapped row still lists campaign-finance policy context as missing")
        else:
            if "campaign_finance_sponsor_policy_area_context" in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should not carry campaign-finance policy context")
            if "campaign_finance_sponsor_policy_area_context" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should list campaign-finance policy context as missing")

        expected_lobbying_context_rows = lobbying_context_by_policy_area.get(policy_area, [])
        expected_lobbying_bill_ids = {
            value
            for lobbying_context_row in expected_lobbying_context_rows
            for value in split_semicolon_values(lobbying_context_row, "matched_bill_ids")
        }
        expected_lobbying_enacted_bill_ids = {
            value
            for lobbying_context_row in expected_lobbying_context_rows
            for value in split_semicolon_values(lobbying_context_row, "matched_enacted_bill_ids")
        }
        expected_lobbying_issues = {
            lobbying_context_row.get("lobbying_issue", "").strip()
            for lobbying_context_row in expected_lobbying_context_rows
            if lobbying_context_row.get("lobbying_issue", "").strip()
        }
        try:
            spine_lobbying_issue_rows = int(row.get("lobbying_policy_context_issue_rows", "0") or "0")
            spine_lobbying_activity_rows = int(row.get("lobbying_policy_context_activity_rows", "0") or "0")
            spine_lobbying_bill_contexts = int(row.get("lobbying_policy_context_bill_contexts", "0") or "0")
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: lobbying policy-context counts must be integers")
            spine_lobbying_issue_rows = 0
            spine_lobbying_activity_rows = 0
            spine_lobbying_bill_contexts = 0
        expected_lobbying_activity_rows = sum(
            parse_int(lobbying_context_row.get("lobbying_rows", "0")) or 0
            for lobbying_context_row in expected_lobbying_context_rows
        )
        expected_lobbying_total_amount = f"{sum(parse_float(lobbying_context_row.get('total_amount', '0')) or 0 for lobbying_context_row in expected_lobbying_context_rows):.2f}"
        expected_lobbying_bill_contexts = sum(
            parse_int(lobbying_context_row.get("matched_govinfo_bill_count", "0")) or 0
            for lobbying_context_row in expected_lobbying_context_rows
        )
        if spine_lobbying_issue_rows != len(expected_lobbying_context_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA policy-context issue rows "
                f"{spine_lobbying_issue_rows} do not match {LOBBYING_BILL_POLICY_CONTEXT} "
                f"rows {len(expected_lobbying_context_rows)}"
            )
        if spine_lobbying_activity_rows != expected_lobbying_activity_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA activity rows "
                f"{spine_lobbying_activity_rows} do not match expected "
                f"{expected_lobbying_activity_rows}"
            )
        if row.get("lobbying_policy_context_total_amount", "") != expected_lobbying_total_amount:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA total amount "
                f"{row.get('lobbying_policy_context_total_amount', '')!r} does not match "
                f"expected {expected_lobbying_total_amount!r}"
            )
        if spine_lobbying_bill_contexts != expected_lobbying_bill_contexts:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA bill contexts "
                f"{spine_lobbying_bill_contexts} do not match expected "
                f"{expected_lobbying_bill_contexts}"
            )
        if split_semicolon_values(row, "lobbying_policy_context_bill_ids") != expected_lobbying_bill_ids:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA policy-context bill set "
                f"does not match {LOBBYING_BILL_POLICY_CONTEXT}"
            )
        if split_semicolon_values(row, "lobbying_policy_context_enacted_bill_ids") != expected_lobbying_enacted_bill_ids:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA policy-context enacted bill set "
                f"does not match {LOBBYING_BILL_POLICY_CONTEXT}"
            )
        if split_semicolon_values(row, "lobbying_policy_context_issues") != expected_lobbying_issues:
            failures.append(
                f"{BILL_LAW_SPINE}: {bill_id}: LDA issue set does not match "
                f"{LOBBYING_BILL_POLICY_CONTEXT}"
            )
        if expected_lobbying_context_rows:
            if "lobbying_issue_bill_policy_area_context" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing LDA policy-context evidence layer")
            if "lobbying_issue_policy_area_context" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: mapped row still lists LDA policy context as missing")
        else:
            if "lobbying_issue_bill_policy_area_context" in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should not carry LDA policy context")
            if "lobbying_issue_policy_area_context" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: unmatched row should list LDA policy context as missing")
        expected_lda_mentions = lda_mentions_by_bill.get(bill_id, [])
        expected_lda_filings = {
            mention.get("filing_uuid", "").strip()
            for mention in expected_lda_mentions
            if mention.get("filing_uuid", "").strip()
        }
        expected_lda_clients = {
            mention.get("client_name", "").strip()
            for mention in expected_lda_mentions
            if mention.get("client_name", "").strip()
        }
        expected_lda_registrants = {
            mention.get("registrant_name", "").strip()
            for mention in expected_lda_mentions
            if mention.get("registrant_name", "").strip()
        }
        expected_lda_issues = {
            mention.get("activity_issue", "").strip()
            for mention in expected_lda_mentions
            if mention.get("activity_issue", "").strip()
        }
        expected_lda_years = {
            mention.get("filing_year", "").strip()
            for mention in expected_lda_mentions
            if mention.get("filing_year", "").strip()
        }
        expected_lda_urls = {
            mention.get("filing_document_url", "").strip()
            for mention in expected_lda_mentions
            if mention.get("filing_document_url", "").strip()
        }
        expected_lda_refs = {
            ref
            for mention in expected_lda_mentions
            for ref in split_semicolon_values(mention, "matched_bill_refs")
        }
        if (parse_int(row.get("lobbying_bill_mention_rows", "")) or 0) != len(expected_lda_mentions):
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA bill-mention row count mismatch")
        if (parse_int(row.get("lobbying_bill_mention_unique_filings", "")) or 0) != len(expected_lda_filings):
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA filing count mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_clients") != expected_lda_clients:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA client set mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_registrants") != expected_lda_registrants:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA registrant set mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_activity_issues") != expected_lda_issues:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA activity-issue set mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_filing_years") != expected_lda_years:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA filing-year set mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_document_urls") != expected_lda_urls:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA filing URL set mismatch")
        if split_semicolon_values(row, "lobbying_bill_mention_matched_refs") != expected_lda_refs:
            failures.append(f"{BILL_LAW_SPINE}: {bill_id}: exact LDA matched-ref set mismatch")
        if expected_lda_mentions:
            if "official_lda_filing_text_bill_identifier" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: missing exact LDA filing-text evidence layer")
            if "bill_specific_campaign_finance_or_lobbying_to_bill" in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: exact LDA filing-text bill mention should close the bill-specific identifier gap"
                )
        else:
            if "official_lda_filing_text_bill_identifier" in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {bill_id}: row without exact LDA mention carries exact evidence layer")
            if "bill_specific_campaign_finance_or_lobbying_to_bill" not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {bill_id}: row without exact LDA mention should preserve bill-specific finance/lobbying gap"
                )
        authority = authority_by_public_law.get(public_law)
        if not authority:
            continue
        try:
            spine_verified = int(row.get("implementation_authority_text_verified_rows", "0") or "0")
            authority_verified = int(authority.get("text_verified_rule_count", "0") or "0")
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: authority counts must be integers")
            continue
        if spine_verified != authority_verified:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: authority count {spine_verified} "
                f"does not match {RULEMAKING_AUTHORITY_LINKAGE} count {authority_verified}"
            )
        if authority.get("linkage_status") == "federal_register_authority_match":
            if "federal_register_authority_search_match" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing authority evidence layer")
            if "implementation_or_rulemaking_authority" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: matched row still lists authority as missing")
        elif "implementation_or_rulemaking_authority" not in row.get("missing_links", ""):
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: unmatched row should list authority as missing")
        history_rows = history_by_public_law.get(public_law, [])
        try:
            spine_history_final_rows = int(row.get("implementation_history_final_rule_rows", "0") or "0")
            spine_history_matched_rows = int(row.get("implementation_history_matched_final_rule_rows", "0") or "0")
            spine_history_links = int(row.get("implementation_history_proposed_rule_links", "0") or "0")
            spine_comment_close_date_count = int(
                row.get("implementation_history_proposed_comment_close_date_count", "0") or "0"
            )
            spine_regulations_docket_count = int(
                row.get("implementation_history_proposed_regulations_docket_count", "0") or "0"
            )
            spine_comment_portal_count = int(
                row.get("implementation_history_proposed_comment_portal_count", "0") or "0"
            )
            spine_final_effective_rule_rows = int(
                row.get("implementation_history_final_effective_rule_rows", "0") or "0"
            )
            spine_final_to_effective_delay_count = int(
                row.get("implementation_history_final_to_effective_delay_count", "0") or "0"
            )
            spine_proposed_to_final_delay_count = int(
                row.get("implementation_history_proposed_to_final_delay_count", "0") or "0"
            )
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: history counts must be integers")
            continue
        matched_history_rows = [
            history_row for history_row in history_rows
            if history_row.get("history_status") == "proposed_rule_history_match"
        ]
        expected_history_matched_rows = sum(
            1 for history_row in matched_history_rows
        )
        expected_history_links = sum(
            int(history_row.get("matched_proposed_rule_count", "0") or "0")
            for history_row in history_rows
        )
        expected_comment_close_dates = {
            value
            for history_row in matched_history_rows
            for value in split_semicolon_values(history_row, "proposed_comment_close_dates")
        }
        expected_regulations_dockets = {
            value
            for history_row in matched_history_rows
            for value in split_semicolon_values(history_row, "proposed_regulations_docket_ids")
        }
        expected_comment_portals = {
            value
            for history_row in matched_history_rows
            for value in split_semicolon_values(history_row, "proposed_regulations_comments_urls")
        }
        expected_final_effective_dates = {
            history_row.get("final_effective_date", "").strip()
            for history_row in history_rows
            if history_row.get("final_effective_date", "").strip()
        }
        expected_final_effective_rule_rows = sum(
            1 for history_row in history_rows
            if history_row.get("final_effective_date", "").strip()
        )
        expected_final_to_effective_delays = [
            delay
            for history_row in history_rows
            for delay in [
                days_between(
                    history_row.get("final_publication_date", ""),
                    history_row.get("final_effective_date", ""),
                )
            ]
            if delay is not None
        ]
        expected_proposed_to_final_delays = [
            delay
            for history_row in matched_history_rows
            for delay in [
                parse_int(history_row.get("days_from_earliest_proposed_to_final", ""))
            ]
            if delay is not None
        ]
        spine_comment_close_dates = split_semicolon_values(
            row, "implementation_history_proposed_comment_close_dates"
        )
        spine_regulations_dockets = split_semicolon_values(
            row, "implementation_history_proposed_regulations_docket_ids"
        )
        spine_comment_portals = split_semicolon_values(
            row, "implementation_history_proposed_regulations_comment_urls"
        )
        spine_final_effective_dates = split_semicolon_values(
            row, "implementation_history_final_effective_dates"
        )
        if spine_history_final_rows != len(history_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: history final-rule rows {spine_history_final_rows} "
                f"do not match {RULEMAKING_HISTORY_LINKAGE} rows {len(history_rows)}"
            )
        if spine_history_matched_rows != expected_history_matched_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: history matched rows {spine_history_matched_rows} "
                f"do not match {RULEMAKING_HISTORY_LINKAGE} rows {expected_history_matched_rows}"
            )
        if spine_history_links != expected_history_links:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed-rule links {spine_history_links} "
                f"do not match {RULEMAKING_HISTORY_LINKAGE} links {expected_history_links}"
            )
        if spine_comment_close_date_count != len(expected_comment_close_dates):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment-close date count "
                f"{spine_comment_close_date_count} does not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {len(expected_comment_close_dates)}"
            )
        if spine_regulations_docket_count != len(expected_regulations_dockets):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed Regulations.gov docket count "
                f"{spine_regulations_docket_count} does not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {len(expected_regulations_dockets)}"
            )
        if spine_comment_portal_count != len(expected_comment_portals):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed Regulations.gov comment portal count "
                f"{spine_comment_portal_count} does not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {len(expected_comment_portals)}"
            )
        if spine_comment_close_dates != expected_comment_close_dates:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment-close date set "
                f"does not match {RULEMAKING_HISTORY_LINKAGE}"
            )
        if spine_regulations_dockets != expected_regulations_dockets:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed Regulations.gov docket set "
                f"does not match {RULEMAKING_HISTORY_LINKAGE}"
            )
        if spine_comment_portals != expected_comment_portals:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed Regulations.gov comment portal set "
                f"does not match {RULEMAKING_HISTORY_LINKAGE}"
            )
        if spine_final_effective_rule_rows != expected_final_effective_rule_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final effective-date rows "
                f"{spine_final_effective_rule_rows} do not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {expected_final_effective_rule_rows}"
            )
        if spine_final_effective_dates != expected_final_effective_dates:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final effective-date set "
                f"does not match {RULEMAKING_HISTORY_LINKAGE}"
            )
        if spine_final_to_effective_delay_count != len(expected_final_to_effective_delays):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final-to-effective delay count "
                f"{spine_final_to_effective_delay_count} does not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {len(expected_final_to_effective_delays)}"
            )
        for output_field, summary_field in (
            ("implementation_history_final_to_effective_delay_min_days", "min"),
            ("implementation_history_final_to_effective_delay_median_days", "median"),
            ("implementation_history_final_to_effective_delay_max_days", "max"),
        ):
            expected_value = summary_value(expected_final_to_effective_delays, summary_field)
            if row.get(output_field, "") != expected_value:
                failures.append(
                    f"{BILL_LAW_SPINE}: {public_law}: {output_field} "
                    f"{row.get(output_field, '')!r} does not match expected {expected_value!r}"
                )
        if spine_proposed_to_final_delay_count != len(expected_proposed_to_final_delays):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed-to-final delay count "
                f"{spine_proposed_to_final_delay_count} does not match "
                f"{RULEMAKING_HISTORY_LINKAGE} count {len(expected_proposed_to_final_delays)}"
            )
        for output_field, summary_field in (
            ("implementation_history_proposed_to_final_delay_min_days", "min"),
            ("implementation_history_proposed_to_final_delay_median_days", "median"),
            ("implementation_history_proposed_to_final_delay_max_days", "max"),
        ):
            expected_value = summary_value(expected_proposed_to_final_delays, summary_field)
            if row.get(output_field, "") != expected_value:
                failures.append(
                    f"{BILL_LAW_SPINE}: {public_law}: {output_field} "
                    f"{row.get(output_field, '')!r} does not match expected {expected_value!r}"
                )
        if expected_history_matched_rows:
            if "federal_register_proposed_rule_history_match" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing proposed-history evidence layer")
            if "proposed_rule_history" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: matched row still lists proposed history as missing")
        elif authority.get("linkage_status") == "federal_register_authority_match":
            if "proposed_rule_history" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: authority match without history should list proposed history as missing")
        if expected_comment_portals:
            if "proposed_rule_regulations_gov_comment_portal_metadata" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing proposed comment-portal evidence layer")
            if (
                "complete_regulations_comments" not in row.get("missing_links", "")
                and "regulations_gov_complete_comment_record_metadata" not in row.get("evidence_layers", "")
            ):
                failures.append(
                    f"{BILL_LAW_SPINE}: {public_law}: comment portal metadata must preserve complete-comments gap"
                )
        elif "proposed_rule_regulations_gov_comment_portal_metadata" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: unmatched row should not carry proposed comment-portal metadata"
            )
        comment_rows = comment_metadata_by_public_law.get(public_law, [])
        expected_comment_statuses = {
            comment_row.get("comment_metadata_status", "").strip()
            for comment_row in comment_rows
            if comment_row.get("comment_metadata_status", "").strip()
        }
        expected_comment_final_dockets = {
            comment_row.get("final_regulations_docket_id", "").strip()
            for comment_row in comment_rows
            if comment_row.get("final_regulations_docket_id", "").strip()
        }
        expected_comment_final_counts = [
            parsed
            for comment_row in comment_rows
            for parsed in [parse_int(comment_row.get("final_regulations_comments_count", ""))]
            if parsed is not None
        ]
        expected_comment_proposed_dockets = {
            value
            for comment_row in comment_rows
            for value in split_semicolon_values(comment_row, "proposed_regulations_docket_ids_refetched")
        }
        expected_comment_proposed_urls = {
            value
            for comment_row in comment_rows
            for value in split_semicolon_values(comment_row, "proposed_regulations_comments_urls_refetched")
        }
        expected_comment_proposed_close_dates = {
            value
            for comment_row in comment_rows
            for value in split_semicolon_values(comment_row, "proposed_comments_close_dates_refetched")
        }
        try:
            spine_comment_rows = int(row.get("implementation_comment_metadata_rows", "0") or "0")
            spine_comment_final_docket_count = int(
                row.get("implementation_comment_metadata_final_regulations_docket_count", "0") or "0"
            )
            spine_comment_final_count_rows = int(
                row.get("implementation_comment_metadata_final_comment_count_rows", "0") or "0"
            )
            spine_comment_final_positive_rows = int(
                row.get("implementation_comment_metadata_final_positive_comment_count_rows", "0") or "0"
            )
            spine_comment_final_total = int(
                row.get("implementation_comment_metadata_final_comment_count_total", "0") or "0"
            )
            spine_comment_proposed_fetch_count = int(
                row.get("implementation_comment_metadata_proposed_detail_fetch_count", "0") or "0"
            )
            spine_comment_proposed_docket_count = int(
                row.get("implementation_comment_metadata_proposed_regulations_docket_count", "0") or "0"
            )
            spine_comment_proposed_url_count = int(
                row.get("implementation_comment_metadata_proposed_comment_url_count", "0") or "0"
            )
            spine_comment_proposed_count_rows = int(
                row.get("implementation_comment_metadata_proposed_comment_count_rows", "0") or "0"
            )
            spine_comment_proposed_positive_rows = int(
                row.get("implementation_comment_metadata_proposed_positive_comment_count_rows", "0") or "0"
            )
            spine_comment_proposed_total = int(
                row.get("implementation_comment_metadata_proposed_comment_count_total", "0") or "0"
            )
            spine_comment_proposed_close_count = int(
                row.get("implementation_comment_metadata_proposed_comment_close_date_count", "0") or "0"
            )
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: comment metadata counts must be integers")
            spine_comment_rows = 0
            spine_comment_final_docket_count = 0
            spine_comment_final_count_rows = 0
            spine_comment_final_positive_rows = 0
            spine_comment_final_total = 0
            spine_comment_proposed_fetch_count = 0
            spine_comment_proposed_docket_count = 0
            spine_comment_proposed_url_count = 0
            spine_comment_proposed_count_rows = 0
            spine_comment_proposed_positive_rows = 0
            spine_comment_proposed_total = 0
            spine_comment_proposed_close_count = 0
        expected_comment_proposed_fetch_count = sum(
            parse_int(comment_row.get("proposed_detail_fetch_count", "")) or 0
            for comment_row in comment_rows
        )
        expected_comment_proposed_count_rows = sum(
            parse_int(comment_row.get("proposed_comment_count_rows", "")) or 0
            for comment_row in comment_rows
        )
        expected_comment_proposed_positive_rows = sum(
            parse_int(comment_row.get("proposed_positive_comment_count_rows", "")) or 0
            for comment_row in comment_rows
        )
        expected_comment_proposed_total = sum(
            parse_int(comment_row.get("proposed_comment_count_total", "")) or 0
            for comment_row in comment_rows
        )
        if spine_comment_rows != len(comment_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment metadata rows {spine_comment_rows} "
                f"do not match {RULEMAKING_COMMENT_METADATA} rows {len(comment_rows)}"
            )
        if split_semicolon_values(row, "implementation_comment_metadata_statuses") != expected_comment_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment metadata statuses do not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_final_docket_count != len(expected_comment_final_dockets):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final comment docket count "
                f"{spine_comment_final_docket_count} does not match {len(expected_comment_final_dockets)}"
            )
        if split_semicolon_values(row, "implementation_comment_metadata_final_regulations_docket_ids") != expected_comment_final_dockets:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final comment docket set does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_final_count_rows != len(expected_comment_final_counts):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final comment count rows "
                f"{spine_comment_final_count_rows} do not match {len(expected_comment_final_counts)}"
            )
        if spine_comment_final_positive_rows != sum(1 for count in expected_comment_final_counts if count > 0):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final positive comment-count rows do not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_final_total != sum(expected_comment_final_counts):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: final comment-count total does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_fetch_count != expected_comment_proposed_fetch_count:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed detail fetch count does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_docket_count != len(expected_comment_proposed_dockets):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment docket count does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if split_semicolon_values(row, "implementation_comment_metadata_proposed_regulations_docket_ids") != expected_comment_proposed_dockets:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment docket set does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_url_count != len(expected_comment_proposed_urls):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment URL count does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if split_semicolon_values(row, "implementation_comment_metadata_proposed_comment_urls") != expected_comment_proposed_urls:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment URL set does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_count_rows != expected_comment_proposed_count_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment count rows do not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_positive_rows != expected_comment_proposed_positive_rows:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed positive comment-count rows do not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_total != expected_comment_proposed_total:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment-count total does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if spine_comment_proposed_close_count != len(expected_comment_proposed_close_dates):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment-close count does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        if split_semicolon_values(row, "implementation_comment_metadata_proposed_comment_close_dates") != expected_comment_proposed_close_dates:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: proposed comment-close set does not match "
                f"{RULEMAKING_COMMENT_METADATA}"
            )
        expected_comment_metadata_present = bool(
            expected_comment_final_dockets
            or expected_comment_final_counts
            or expected_comment_proposed_dockets
            or expected_comment_proposed_urls
            or expected_comment_proposed_close_dates
        )
        expected_comment_metadata_dockets = expected_comment_final_dockets | expected_comment_proposed_dockets
        comment_record_rows = comment_records_by_public_law.get(public_law, [])
        expected_comment_record_statuses = {
            record_row.get("retrieval_status", "").strip()
            for record_row in comment_record_rows
            if record_row.get("retrieval_status", "").strip()
        }
        expected_comment_record_dockets = {
            record_row.get("docket_id", "").strip()
            for record_row in comment_record_rows
            if record_row.get("docket_id", "").strip()
        }
        expected_comment_record_ids = {
            value
            for record_row in comment_record_rows
            for value in split_semicolon_values(record_row, "retrieved_comment_ids")
        }
        expected_comment_record_complete_rows = [
            record_row for record_row in comment_record_rows
            if record_row.get("retrieval_status", "").strip() in complete_comment_record_statuses
        ]
        expected_comment_record_partial_rows = [
            record_row for record_row in comment_record_rows
            if record_row.get("retrieval_status", "").strip() not in complete_comment_record_statuses
        ]
        expected_complete_comment_records = bool(expected_comment_metadata_dockets) and (
            expected_comment_metadata_dockets <= expected_comment_record_dockets
        ) and not [
            record_row for record_row in comment_record_rows
            if record_row.get("docket_id", "").strip() in expected_comment_metadata_dockets
            and record_row.get("retrieval_status", "").strip() not in complete_comment_record_statuses
        ]
        expected_partial_comment_records = any(
            "regulations_gov_partial_comment_record_metadata" in record_row.get("evidence_layers", "")
            for record_row in comment_record_rows
        )
        try:
            spine_comment_record_rows = int(row.get("implementation_comment_record_docket_rows", "0") or "0")
            spine_comment_record_complete_rows = int(row.get("implementation_comment_record_complete_docket_rows", "0") or "0")
            spine_comment_record_partial_rows = int(row.get("implementation_comment_record_partial_or_blocked_docket_rows", "0") or "0")
            spine_comment_record_expected_total = int(row.get("implementation_comment_record_expected_comment_count_total", "0") or "0")
            spine_comment_record_retrieved_total = int(row.get("implementation_comment_record_retrieved_comment_count_total", "0") or "0")
            spine_comment_record_api_total = int(row.get("implementation_comment_record_api_total_count", "0") or "0")
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: comment record counts must be integers")
            spine_comment_record_rows = 0
            spine_comment_record_complete_rows = 0
            spine_comment_record_partial_rows = 0
            spine_comment_record_expected_total = 0
            spine_comment_record_retrieved_total = 0
            spine_comment_record_api_total = 0
        if spine_comment_record_rows != len(comment_record_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record rows {spine_comment_record_rows} "
                f"do not match {RULEMAKING_COMMENT_RECORDS} rows {len(comment_record_rows)}"
            )
        if spine_comment_record_complete_rows != len(expected_comment_record_complete_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: complete comment-record rows do not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if spine_comment_record_partial_rows != len(expected_comment_record_partial_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: partial/blocked comment-record rows do not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if split_semicolon_values(row, "implementation_comment_record_statuses") != expected_comment_record_statuses:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record statuses do not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if split_semicolon_values(row, "implementation_comment_record_docket_ids") != expected_comment_record_dockets:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record docket set does not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if split_semicolon_values(row, "implementation_comment_record_ids") != expected_comment_record_ids:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record ID set does not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if spine_comment_record_expected_total != sum(parse_int(record_row.get("expected_comment_count", "")) or 0 for record_row in comment_record_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record expected total does not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if spine_comment_record_retrieved_total != sum(parse_int(record_row.get("retrieved_comment_count", "")) or 0 for record_row in comment_record_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record retrieved total does not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if spine_comment_record_api_total != sum(parse_int(record_row.get("api_total_comment_count", "")) or 0 for record_row in comment_record_rows):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: comment-record API total does not match "
                f"{RULEMAKING_COMMENT_RECORDS}"
            )
        if expected_comment_metadata_present:
            if "federal_register_exposed_regulations_gov_comment_metadata" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing comment metadata evidence layer")
            if expected_complete_comment_records:
                if "regulations_gov_complete_comment_record_metadata" not in row.get("evidence_layers", ""):
                    failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing complete comment-record evidence layer")
                if "complete_regulations_comments" in row.get("missing_links", ""):
                    failures.append(
                        f"{BILL_LAW_SPINE}: {public_law}: complete comment records should close complete-comments gap"
                    )
            else:
                if expected_partial_comment_records and "regulations_gov_partial_comment_record_metadata" not in row.get("evidence_layers", ""):
                    failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing partial comment-record evidence layer")
                if not expected_partial_comment_records and "regulations_gov_partial_comment_record_metadata" in row.get("evidence_layers", ""):
                    failures.append(f"{BILL_LAW_SPINE}: {public_law}: unexpected partial comment-record evidence layer")
                if "complete_regulations_comments" not in row.get("missing_links", ""):
                    failures.append(
                        f"{BILL_LAW_SPINE}: {public_law}: comment metadata must preserve complete-comments gap"
                    )
        elif "federal_register_exposed_regulations_gov_comment_metadata" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: unmatched row should not carry comment metadata evidence"
            )
        if expected_final_to_effective_delays:
            if "federal_register_final_effective_date_timing" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing final effective-date timing layer")
            if "implementation_outcomes_or_enforcement" not in row.get("missing_links", ""):
                failures.append(
                    f"{BILL_LAW_SPINE}: {public_law}: timing metadata must preserve implementation-outcomes gap"
                )
        elif "federal_register_final_effective_date_timing" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: unmatched row should not carry final effective-date timing"
            )
        if expected_proposed_to_final_delays:
            if "federal_register_proposed_to_final_timing" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing proposed-to-final timing layer")
            if (
                "complete_regulations_comments" not in row.get("missing_links", "")
                and not expected_complete_comment_records
            ):
                failures.append(
                    f"{BILL_LAW_SPINE}: {public_law}: proposed timing must preserve complete-comments gap"
                )
        elif "federal_register_proposed_to_final_timing" in row.get("evidence_layers", ""):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: unmatched row should not carry proposed-to-final timing"
            )
        court_rows = court_by_public_law.get(public_law, [])
        expected_court_case_ids = {
            court_row.get("case_id", "").strip()
            for court_row in court_rows
            if court_row.get("case_id", "").strip()
        }
        expected_court_invalidated_case_ids = {
            court_row.get("case_id", "").strip()
            for court_row in court_rows
            if court_row.get("case_id", "").strip() and court_row.get("invalidated") == "1"
        }
        expected_court_sections = {
            section.strip()
            for court_row in court_rows
            for section in court_row.get("matched_usc_sections", "").split(";")
            if section.strip()
        }
        try:
            spine_court_cases = int(row.get("court_review_overlap_case_rows", "0") or "0")
            spine_court_invalidated = int(row.get("court_review_invalidated_case_rows", "0") or "0")
        except ValueError:
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: court-review counts must be integers")
            continue
        if spine_court_cases != len(expected_court_case_ids):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: court case rows {spine_court_cases} "
                f"do not match {COURT_LAW_LINKAGE} cases {len(expected_court_case_ids)}"
            )
        if spine_court_invalidated != len(expected_court_invalidated_case_ids):
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: invalidated court cases {spine_court_invalidated} "
                f"do not match {COURT_LAW_LINKAGE} cases {len(expected_court_invalidated_case_ids)}"
            )
        spine_case_ids = {
            case_id.strip()
            for case_id in row.get("court_review_case_ids", "").split(";")
            if case_id.strip()
        }
        spine_sections = {
            section.strip()
            for section in row.get("court_review_usc_sections", "").split(";")
            if section.strip()
        }
        if spine_case_ids != expected_court_case_ids:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: court case-id set does not match court-law linkage"
            )
        if spine_sections != expected_court_sections:
            failures.append(
                f"{BILL_LAW_SPINE}: {public_law}: court U.S.C. section set does not match court-law linkage"
            )
        if expected_court_case_ids:
            if "court_review_usc_section_authority_overlap" not in row.get("evidence_layers", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: missing court-overlap evidence layer")
            if "court_review_or_invalidation" in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: matched row still lists broad court review as missing")
            if "direct_case_to_public_law_identifier" not in row.get("missing_links", ""):
                failures.append(f"{BILL_LAW_SPINE}: {public_law}: court-overlap row must preserve direct-case missing boundary")
        elif "court_review_or_invalidation" not in row.get("missing_links", ""):
            failures.append(f"{BILL_LAW_SPINE}: {public_law}: unmatched row should list court review as missing")

    required_voteview_context_columns = {
        "congress",
        "chamber",
        "icpsr",
        "bioguide_id",
        "rollcall_rows",
        "unique_vote_ids",
        "linkage_status",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_voteview_context_columns = required_voteview_context_columns - set(voteview_member_context[0])
    if missing_voteview_context_columns:
        failures.append(
            f"{VOTEVIEW_MEMBER_CONTEXT}: missing columns {sorted(missing_voteview_context_columns)}"
        )
    rollcall_counts = Counter(voteview_member_key(row) for row in voteview_rollcall_rows)
    rollcall_counts.pop(("", "", ""), None)
    context_keys = {voteview_member_key(row) for row in voteview_member_context}
    raw_context_keys = {voteview_member_key(row) for row in voteview_member_context_raw}
    if context_keys != raw_context_keys:
        failures.append(
            "Voteview member-context report/raw mismatch: "
            f"missing from report={sorted(raw_context_keys - context_keys)}, "
            f"extra={sorted(context_keys - raw_context_keys)}"
        )
    if not context_keys:
        failures.append(f"{VOTEVIEW_MEMBER_CONTEXT}: no member-context keys")
    missing_rollcall_keys = set(rollcall_counts) - context_keys
    if missing_rollcall_keys:
        failures.append(
            f"{VOTEVIEW_MEMBER_CONTEXT}: missing roll-call member keys "
            f"{sorted(missing_rollcall_keys)[:10]}"
        )
    for row in voteview_member_context:
        key = voteview_member_key(row)
        boundary = row.get("claim_boundary", "")
        if "model validation" not in boundary or "roll-call-to-bill" not in boundary:
            failures.append(
                f"{VOTEVIEW_MEMBER_CONTEXT}: {key}: "
                "claim_boundary must reject roll-call-to-bill linkage and model validation"
            )
        try:
            context_rollcall_rows = int(row.get("rollcall_rows", "0") or "0")
        except ValueError:
            failures.append(f"{VOTEVIEW_MEMBER_CONTEXT}: {key}: rollcall_rows is not an integer")
            continue
        if rollcall_counts.get(key, 0) != context_rollcall_rows:
            failures.append(
                f"{VOTEVIEW_MEMBER_CONTEXT}: {key}: rollcall_rows {context_rollcall_rows} "
                f"does not match {VOTEVIEW_ROLLCALLS} count {rollcall_counts.get(key, 0)}"
            )

    required_voteview_bill_columns = {
        "vote_id",
        "congress",
        "chamber",
        "rollnumber",
        "bill_id",
        "bill_match_status",
        "member_vote_rows",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_voteview_bill_columns = required_voteview_bill_columns - set(voteview_bill_linkage[0])
    if missing_voteview_bill_columns:
        failures.append(
            f"{VOTEVIEW_BILL_LINKAGE}: missing columns {sorted(missing_voteview_bill_columns)}"
        )
    vote_counts = Counter(row.get("vote_id", "").strip() for row in voteview_rollcall_rows)
    vote_counts.pop("", None)
    bill_report_keys = {voteview_vote_id(row) for row in voteview_bill_linkage}
    bill_raw_keys = {voteview_vote_id(row) for row in voteview_bill_linkage_raw}
    if bill_report_keys != bill_raw_keys:
        failures.append(
            "Voteview bill-linkage report/raw mismatch: "
            f"missing from report={sorted(bill_raw_keys - bill_report_keys)}, "
            f"extra={sorted(bill_report_keys - bill_raw_keys)}"
        )
    if bill_report_keys != set(vote_counts):
        failures.append(
            "Voteview bill-linkage report/vote sample mismatch: "
            f"missing from report={sorted(set(vote_counts) - bill_report_keys)[:10]}, "
            f"extra={sorted(bill_report_keys - set(vote_counts))[:10]}"
        )
    bill_progression_overlap = [
        row for row in voteview_bill_linkage
        if row.get("bill_match_status") == "bill_progression_metadata"
    ]
    if not bill_progression_overlap:
        failures.append(f"{VOTEVIEW_BILL_LINKAGE}: expected at least one cached bill-progression overlap")
    for row in voteview_bill_linkage:
        vote_id = voteview_vote_id(row)
        boundary = row.get("claim_boundary", "")
        if "model validation" not in boundary or "public-opinion" not in boundary:
            failures.append(
                f"{VOTEVIEW_BILL_LINKAGE}: {vote_id}: "
                "claim_boundary must reject public-opinion claims and model validation"
            )
        try:
            member_vote_rows = int(row.get("member_vote_rows", "0") or "0")
        except ValueError:
            failures.append(f"{VOTEVIEW_BILL_LINKAGE}: {vote_id}: member_vote_rows is not an integer")
            continue
        if vote_counts.get(vote_id, 0) != member_vote_rows:
            failures.append(
                f"{VOTEVIEW_BILL_LINKAGE}: {vote_id}: member_vote_rows {member_vote_rows} "
                f"does not match {VOTEVIEW_ROLLCALLS} count {vote_counts.get(vote_id, 0)}"
            )

    required_campaign_context_columns = {
        "cycle",
        "recipient",
        "district_context_status",
        "raw_transaction_rows",
        "district_public_opinion_context_rows",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_campaign_context_columns = (
        required_campaign_context_columns - set(campaign_finance_district_context[0])
    )
    if missing_campaign_context_columns:
        failures.append(
            f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: missing columns "
            f"{sorted(missing_campaign_context_columns)}"
        )
    context_keys = {
        (row.get("cycle", ""), row.get("recipient", ""))
        for row in campaign_finance_district_context
    }
    campaign_linkage_keys = {
        (row.get("cycle", ""), row.get("recipient", ""))
        for row in campaign_linkage_rows
    }
    if context_keys != campaign_linkage_keys:
        failures.append(
            "campaign-finance district context/linkage recipient mismatch: "
            f"missing from context={sorted(campaign_linkage_keys - context_keys)}, "
            f"extra={sorted(context_keys - campaign_linkage_keys)}"
        )
    district_ids = {
        row.get("district_id", "")
        for row in district_opinion_rows
        if row.get("district_id")
    }
    expected_house_context_keys = {
        (row.get("cycle", ""), row.get("recipient", ""))
        for row in campaign_linkage_rows
        if house_district_from_campaign_linkage(row) in district_ids
    }
    actual_house_context_keys = {
        (row.get("cycle", ""), row.get("recipient", ""))
        for row in campaign_finance_district_context
        if row.get("district_context_status") == "house_candidate_district_public_opinion_context"
    }
    if actual_house_context_keys != expected_house_context_keys:
        failures.append(
            "campaign-finance House district-context mismatch: "
            f"expected={sorted(expected_house_context_keys)}, actual={sorted(actual_house_context_keys)}"
        )
    opinion_rows_by_district = Counter(row.get("district_id", "") for row in district_opinion_rows)
    for row in campaign_finance_district_context:
        boundary = row.get("claim_boundary", "")
        if "model validation" not in boundary or "bill-level influence" not in boundary:
            failures.append(
                f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: {row.get('recipient')}: "
                "claim_boundary must reject bill-level influence and model validation"
            )
        district_id = row.get("district_id", "")
        try:
            context_count = int(row.get("district_public_opinion_context_rows", "0") or "0")
        except ValueError:
            failures.append(
                f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: {row.get('recipient')}: "
                "district_public_opinion_context_rows is not an integer"
            )
            continue
        if row.get("district_context_status") == "house_candidate_district_public_opinion_context":
            if context_count != opinion_rows_by_district[district_id]:
                failures.append(
                    f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: {row.get('recipient')}: "
                    f"context rows {context_count} do not match district opinion rows "
                    f"{opinion_rows_by_district[district_id]} for {district_id}"
                )
        elif context_count != 0:
            failures.append(
                f"{CAMPAIGN_FINANCE_DISTRICT_CONTEXT}: {row.get('recipient')}: "
                "non-House context row should not attach district opinion rows"
            )

    required_campaign_member_columns = {
        "cycle",
        "recipient",
        "candidate_id",
        "member_context_status",
        "member_context_transaction_rows",
        "voteview_chamber",
        "bioguide_id",
        "evidence_layers",
        "missing_links",
        "match_basis",
        "claim_boundary",
    }
    missing_campaign_member_columns = (
        required_campaign_member_columns - set(campaign_finance_member_context[0])
    )
    if missing_campaign_member_columns:
        failures.append(
            f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: missing columns "
            f"{sorted(missing_campaign_member_columns)}"
        )
    campaign_member_report_keys = {
        (row.get("cycle", ""), row.get("recipient", ""), row.get("candidate_id", ""))
        for row in campaign_finance_member_context
    }
    campaign_member_raw_keys = {
        (row.get("cycle", ""), row.get("recipient", ""), row.get("candidate_id", ""))
        for row in campaign_member_context_raw
    }
    if campaign_member_report_keys != campaign_member_raw_keys:
        failures.append(
            "campaign-finance member context/report raw mismatch: "
            f"missing from report={sorted(campaign_member_raw_keys - campaign_member_report_keys)}, "
            f"extra={sorted(campaign_member_report_keys - campaign_member_raw_keys)}"
        )
    campaign_member_recipient_keys = {
        (row.get("cycle", ""), row.get("recipient", ""))
        for row in campaign_finance_member_context
    }
    if campaign_member_recipient_keys != campaign_linkage_keys:
        failures.append(
            "campaign-finance member context/linkage recipient mismatch: "
            f"missing from context={sorted(campaign_linkage_keys - campaign_member_recipient_keys)}, "
            f"extra={sorted(campaign_member_recipient_keys - campaign_linkage_keys)}"
        )
    voteview_bioguide_ids = {
        row.get("bioguide_id", "")
        for row in voteview_member_context_raw
        if row.get("bioguide_id")
    }
    member_matched_rows = [
        row for row in campaign_finance_member_context
        if row.get("member_context_status") == "candidate_voteview_member_context"
    ]
    if not member_matched_rows:
        failures.append(f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: expected at least one candidate member-context match")
    for row in campaign_finance_member_context:
        recipient = row.get("recipient", "")
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "bill-level influence" not in boundary
            or "causal capture" not in boundary
            or "private contributor" not in boundary
        ):
            failures.append(
                f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                "claim_boundary must reject bill-level influence, causal capture, private contributor disclosure, and model validation"
            )
        try:
            member_transactions = int(row.get("member_context_transaction_rows", "0") or "0")
            linked_transactions = int(row.get("linked_transaction_rows", "0") or "0")
        except ValueError:
            failures.append(
                f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                "member_context_transaction_rows or linked_transaction_rows is not an integer"
            )
            continue
        matched = row.get("member_context_status") == "candidate_voteview_member_context"
        if matched:
            bioguide_id = row.get("bioguide_id", "")
            if not bioguide_id or bioguide_id not in voteview_bioguide_ids:
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    f"matched bioguide_id {bioguide_id!r} is not in Voteview member context"
                )
            if "voteview_member_context" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    "matched row missing voteview_member_context evidence layer"
                )
            if not row.get("match_basis", "").startswith("candidate_name_state_district"):
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    "matched row must record conservative name/state/district match basis"
                )
            if member_transactions != linked_transactions:
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    f"member_context_transaction_rows {member_transactions} "
                    f"does not match linked_transaction_rows {linked_transactions}"
                )
            candidate_office = row.get("candidate_office", "")
            candidate_state = row.get("candidate_office_state", "").strip().upper()
            member_state = row.get("member_state", "").strip().upper()
            if candidate_office == "House":
                if candidate_state != member_state:
                    failures.append(
                        f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                        "House candidate/member states do not match"
                    )
                if row.get("district_id") != house_district_from_campaign_linkage(row):
                    failures.append(
                        f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                        "House candidate/member districts do not match"
                    )
            elif candidate_office == "Senate" and candidate_state != member_state:
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    "Senate candidate/member states do not match"
                )
        else:
            if member_transactions != 0:
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    "unmatched row should not carry member-context transaction rows"
                )
            if row.get("bioguide_id"):
                failures.append(
                    f"{CAMPAIGN_FINANCE_MEMBER_CONTEXT}: {recipient}: "
                    "unmatched row should not carry bioguide_id"
                )

    required_campaign_sponsor_bill_columns = {
        "cycle",
        "recipient",
        "candidate_id",
        "member_context_status",
        "member_context_transaction_rows",
        "bioguide_id",
        "sponsor_bill_context_status",
        "matched_bill_count",
        "matched_bill_ids",
        "matched_policy_areas",
        "matched_committees",
        "matched_committee_reported_bill_count",
        "matched_floor_considered_bill_count",
        "matched_enacted_bill_count",
        "matched_enacted_bill_ids",
        "match_basis",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_campaign_sponsor_bill_columns = (
        required_campaign_sponsor_bill_columns - set(campaign_finance_sponsor_bill_context[0])
    )
    if missing_campaign_sponsor_bill_columns:
        failures.append(
            f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: missing columns "
            f"{sorted(missing_campaign_sponsor_bill_columns)}"
        )
    if not CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT_MD.exists():
        failures.append(f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT_MD}: missing markdown report")
    govinfo_bills_by_sponsor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in govinfo_billstatus_raw:
        sponsor_bioguide = row.get("sponsor_bioguide_id", "")
        if sponsor_bioguide and row.get("bill_id", ""):
            govinfo_bills_by_sponsor[sponsor_bioguide].append(row)
    expected_sponsor_bill_keys = {
        (
            row.get("cycle", ""),
            row.get("recipient", ""),
            row.get("candidate_id", ""),
            row.get("bioguide_id", ""),
        )
        for row in campaign_member_context_raw
        if row.get("member_context_status") == "candidate_voteview_member_context"
        and row.get("bioguide_id", "") in govinfo_bills_by_sponsor
    }
    campaign_sponsor_bill_keys = {
        (
            row.get("cycle", ""),
            row.get("recipient", ""),
            row.get("candidate_id", ""),
            row.get("bioguide_id", ""),
        )
        for row in campaign_finance_sponsor_bill_context
    }
    if campaign_sponsor_bill_keys != expected_sponsor_bill_keys:
        failures.append(
            "campaign-finance sponsor-bill context/raw join mismatch: "
            f"missing from report={sorted(expected_sponsor_bill_keys - campaign_sponsor_bill_keys)}, "
            f"extra={sorted(campaign_sponsor_bill_keys - expected_sponsor_bill_keys)}"
        )
    campaign_member_by_sponsor_key = {
        (
            row.get("cycle", ""),
            row.get("recipient", ""),
            row.get("candidate_id", ""),
            row.get("bioguide_id", ""),
        ): row
        for row in campaign_member_context_raw
        if row.get("member_context_status") == "candidate_voteview_member_context"
    }
    if not campaign_finance_sponsor_bill_context:
        failures.append(f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: expected at least one candidate sponsored-bill context row")
    for row in campaign_finance_sponsor_bill_context:
        key = (
            row.get("cycle", ""),
            row.get("recipient", ""),
            row.get("candidate_id", ""),
            row.get("bioguide_id", ""),
        )
        source_row = campaign_member_by_sponsor_key.get(key, {})
        sponsor_bills = govinfo_bills_by_sponsor.get(row.get("bioguide_id", ""), [])
        bill_ids = {
            bill_id.strip()
            for source in sponsor_bills
            for bill_id in source.get("bill_id", "").split(";")
            if bill_id.strip()
        }
        report_bill_ids = {
            bill_id.strip()
            for bill_id in row.get("matched_bill_ids", "").split(";")
            if bill_id.strip()
        }
        enacted_bill_ids = {
            source.get("bill_id", "")
            for source in sponsor_bills
            if source.get("enacted", "") == "1" and source.get("bill_id", "")
        }
        report_enacted_bill_ids = {
            bill_id.strip()
            for bill_id in row.get("matched_enacted_bill_ids", "").split(";")
            if bill_id.strip()
        }
        if row.get("sponsor_bill_context_status") != "candidate_sponsored_bill_context":
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: invalid sponsor_bill_context_status"
            )
        if row.get("member_context_status") != "candidate_voteview_member_context":
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: expected matched member context status"
            )
        if not source_row:
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: missing source campaign member row"
            )
        elif row.get("member_context_transaction_rows", "") != source_row.get("member_context_transaction_rows", ""):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: transaction count does not match member context"
            )
        if report_bill_ids != bill_ids:
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: matched_bill_ids do not match govinfo sponsor rows"
            )
        try:
            matched_bill_count = int(row.get("matched_bill_count", "0") or "0")
            committee_reported_count = int(row.get("matched_committee_reported_bill_count", "0") or "0")
            floor_count = int(row.get("matched_floor_considered_bill_count", "0") or "0")
            enacted_count = int(row.get("matched_enacted_bill_count", "0") or "0")
        except ValueError:
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: matched counts must be integers"
            )
            continue
        if matched_bill_count != len(bill_ids):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: matched_bill_count mismatch"
            )
        if committee_reported_count != sum(1 for source in sponsor_bills if source.get("committee_reported", "") == "1"):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: committee-reported count mismatch"
            )
        if floor_count != sum(1 for source in sponsor_bills if source.get("floor_considered", "") == "1"):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: floor-considered count mismatch"
            )
        if enacted_count != len(enacted_bill_ids) or report_enacted_bill_ids != enacted_bill_ids:
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: enacted bill metadata mismatch"
            )
        if row.get("match_basis") != "candidate_voteview_bioguide_to_govinfo_sponsor_bioguide":
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: unexpected match basis"
            )
        evidence_layers = row.get("evidence_layers", "")
        if "voteview_member_context" not in evidence_layers or "govinfo_billstatus_sponsor_metadata" not in evidence_layers:
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: missing member or sponsor-bill evidence layer"
            )
        missing_links = row.get("missing_links", "")
        if (
            "reviewed_outside_spending_target" not in missing_links
            or "private_contributor_disclosure" not in missing_links
            or "causal_influence_or_capture_validation" not in missing_links
        ):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: missing links must preserve target, private contributor, and causal influence gaps"
            )
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "causal capture" not in boundary
            or "private contributor" not in boundary
            or "influenced" not in boundary
        ):
            failures.append(
                f"{CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT}: {key}: claim boundary must reject influence, causal capture, private contributor disclosure, and model validation"
            )

    required_campaign_issue_columns = {
        "cycle",
        "recipient",
        "source_id",
        "source_schedule",
        "transaction_date",
        "industry",
        "amount",
        "recipient_type",
        "recipient_linkage_status",
        "issue_context_status",
        "mapped_topic",
        "topic_introduced",
        "topic_floor_considered",
        "topic_enacted",
        "mapping_basis",
        "evidence_layers",
        "missing_links",
        "claim_boundary",
    }
    missing_campaign_issue_columns = (
        required_campaign_issue_columns - set(campaign_finance_issue_context[0])
    )
    if missing_campaign_issue_columns:
        failures.append(
            f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: missing columns "
            f"{sorted(missing_campaign_issue_columns)}"
        )
    if not CAMPAIGN_FINANCE_ISSUE_CONTEXT_MD.exists():
        failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT_MD}: missing markdown report")
    campaign_issue_report_keys = {
        campaign_transaction_key(row)
        for row in campaign_finance_issue_context
    }
    campaign_issue_raw_keys = {
        campaign_transaction_key(row)
        for row in campaign_issue_context_raw
    }
    campaign_source_keys = {
        campaign_transaction_key(row)
        for row in campaign_finance_rows
    }
    if campaign_issue_report_keys != campaign_issue_raw_keys:
        failures.append(
            "campaign-finance issue context/report raw mismatch: "
            f"missing from report={sorted(campaign_issue_raw_keys - campaign_issue_report_keys)[:10]}, "
            f"extra={sorted(campaign_issue_report_keys - campaign_issue_raw_keys)[:10]}"
        )
    if campaign_issue_raw_keys != campaign_source_keys:
        failures.append(
            "campaign-finance issue context/source transaction mismatch: "
            f"missing from context={sorted(campaign_source_keys - campaign_issue_raw_keys)[:10]}, "
            f"extra={sorted(campaign_issue_raw_keys - campaign_source_keys)[:10]}"
        )
    campaign_linkage_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in campaign_linkage_rows:
        cycles = [value.strip() for value in row.get("cycle", "").split(";") if value.strip()]
        if not cycles:
            cycles = [""]
        for cycle in cycles:
            campaign_linkage_by_key[(cycle, row.get("recipient", ""))] = row
    mapped_issue_rows = [
        row for row in campaign_finance_issue_context
        if row.get("issue_context_status") == "campaign_finance_issue_topic_context"
    ]
    if not mapped_issue_rows:
        failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: expected at least one mapped issue-topic row")
    finance_linkage_row = linkage_by_family.get("OpenFEC campaign finance", {})
    if finance_linkage_row:
        boundary = finance_linkage_row.get("linkageBoundary", "")
        if mapped_issue_rows and "issue-topic context" not in boundary:
            failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention issue-topic context")
        if campaign_finance_sponsor_bill_context and "sponsored-bill context" not in boundary:
            failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention sponsored-bill context")
        if bill_finance_lobbying_local_context_review and "local no-current-match" not in boundary:
            failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention local no-current-match context")
        if (
            bill_finance_lobbying_campaign_finance_target_scope_review
            and "target-scope review" not in boundary
        ):
            failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention target-scope review")
        if (
            bill_finance_lobbying_member_vote_target_review
            and "member-vote target-scope review" not in boundary
        ):
            failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention member-vote target-scope review")
        if bill_finance_lobbying_committee_action_context:
            for phrase in (
                "committee-action context report",
                "cached public bill-action metadata",
                "committee-of-jurisdiction names",
            ):
                if phrase not in boundary:
                    failures.append(f"{LINKAGE}: OpenFEC campaign finance boundary must mention {phrase!r}")
        next_step = finance_linkage_row.get("nextLinkStep", "")
        if (
            "external campaign target/source documents" not in next_step
            or "direct member target documents" not in next_step
            or "committee/no-direct-committee source dispositions" not in next_step
            or "legislative outcomes" not in next_step
        ):
            failures.append(
                f"{LINKAGE}: OpenFEC campaign finance next step should require external campaign source, "
                "direct member target, committee source-disposition, and outcome follow-up"
            )
    for row in campaign_finance_issue_context:
        key = campaign_transaction_key(row)
        boundary = row.get("claim_boundary", "")
        if (
            "model validation" not in boundary
            or "bill-level influence" not in boundary
            or "causal capture" not in boundary
            or "private contributor" not in boundary
        ):
            failures.append(
                f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: "
                "claim_boundary must reject bill-level influence, causal capture, private contributor disclosure, and model validation"
            )
        linkage_row = campaign_linkage_by_key.get((row.get("cycle", ""), row.get("recipient", "")), {})
        if linkage_row:
            if row.get("recipient_type") != linkage_row.get("recipient_type", ""):
                failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: recipient_type mismatch")
            if row.get("recipient_linkage_status") != linkage_row.get("linkage_status", ""):
                failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: recipient_linkage_status mismatch")
        status = row.get("issue_context_status", "")
        mapped_topic = row.get("mapped_topic", "")
        if status == "campaign_finance_issue_topic_context":
            if mapped_topic not in topic_values:
                failures.append(
                    f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: mapped topic {mapped_topic!r} "
                    "is not present in topic throughput"
                )
            if "topic_throughput_policy_area" not in row.get("evidence_layers", ""):
                failures.append(
                    f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: mapped row missing topic evidence layer"
                )
            if "bill_id" not in row.get("missing_links", "") or "committee_of_jurisdiction" not in row.get("missing_links", ""):
                failures.append(
                    f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: mapped row must keep bill and committee links missing"
                )
            for count_field in ("topic_introduced", "topic_floor_considered", "topic_enacted"):
                try:
                    int(row.get(count_field, "0") or "0")
                except ValueError:
                    failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: {count_field} must be an integer")
        elif status == "unmapped_campaign_finance_label":
            if mapped_topic or row.get("topic_introduced") or row.get("topic_floor_considered") or row.get("topic_enacted"):
                failures.append(
                    f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: unmapped row should not carry topic fields"
                )
        else:
            failures.append(f"{CAMPAIGN_FINANCE_ISSUE_CONTEXT}: {key}: invalid issue_context_status {status!r}")

    heldout_by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in heldout:
        heldout_by_family[row.get("sourceFamily", "")].append(row)
    heldout_families = set(heldout_by_family)
    registry_heldout = {
        row["source_family"]
        for row in registry
        if row.get("boundary_category") == "held-out benchmark"
    }
    if heldout_families != registry_heldout:
        failures.append(
            "held-out source-family mismatch: "
            f"registry={sorted(registry_heldout)}, heldout_report={sorted(heldout_families)}"
        )

    target_rows = [row for row in heldout if row.get("heldoutTargetStatus") != "reported"]
    pass_rows = [row for row in target_rows if row.get("heldoutTargetStatus") == "pass"]
    bad_statuses = [
        row for row in heldout
        if row.get("heldoutTargetStatus") not in {"pass", "reported"}
    ]
    for row in bad_statuses:
        failures.append(
            f"{HELDOUT}: {row.get('sourceFamily')} / {row.get('metric')} "
            f"status is {row.get('heldoutTargetStatus')!r}"
        )
    for family in sorted(heldout_families):
        family_rows = heldout_by_family[family]
        if not any(row.get("heldoutTargetStatus") == "pass" for row in family_rows):
            failures.append(f"{HELDOUT}: held-out family {family!r} has no passing targeted check")
        total_rows_by_metric = {row.get("metric"): row for row in family_rows}
        for metric, row in total_rows_by_metric.items():
            try:
                total_rows = int(row["totalRows"])
                calibration_rows = int(row["calibrationRows"])
                heldout_rows_count = int(row["heldoutRows"])
                total_units = int(row["totalUnits"])
                calibration_units = int(row["calibrationUnits"])
                heldout_units = int(row["heldoutUnits"])
            except (KeyError, ValueError) as exception:
                failures.append(f"{HELDOUT}: {family} / {metric}: invalid split counts ({exception})")
                continue
            if calibration_rows + heldout_rows_count != total_rows:
                failures.append(f"{HELDOUT}: {family} / {metric}: row split does not sum to total")
            if calibration_units + heldout_units != total_units:
                failures.append(f"{HELDOUT}: {family} / {metric}: unit split does not sum to total")

    for source in registry:
        family = source["source_family"]
        inventory_row = inventory_by_family.get(family, {})
        gap_row = gap_by_family.get(family, {})
        linkage_row = linkage_by_family.get(family, {})
        roadmap_row = roadmap_by_family.get(family, {})
        raw_manifest_row = raw_manifest_by_family.get(family, {})
        boundary = source.get("boundary_category", "")
        if not boundary:
            failures.append(f"{REGISTRY}: {family}: missing boundary_category")
        if inventory_row and inventory_row.get("boundaryCategory") != boundary:
            failures.append(f"{INVENTORY}: {family}: boundary does not match registry")
        if gap_row and gap_row.get("boundaryCategory") != boundary:
            failures.append(f"{GAP}: {family}: boundary does not match registry")
        if gap_row and gap_row.get("dataset") != source.get("dataset"):
            failures.append(f"{GAP}: {family}: dataset does not match registry")
        if inventory_row and inventory_row.get("dataset") != source.get("dataset"):
            failures.append(f"{INVENTORY}: {family}: dataset does not match registry")
        if linkage_row:
            if linkage_row.get("dataset") != source.get("dataset"):
                failures.append(f"{LINKAGE}: {family}: dataset does not match registry")
            if linkage_row.get("boundaryCategory") != boundary:
                failures.append(f"{LINKAGE}: {family}: boundary does not match registry")
            if gap_row and gap_row.get("linkageStatus") != linkage_row.get("linkageStatus"):
                failures.append(f"{GAP}: {family}: linkageStatus does not match linkage report")
            linkage_status = linkage_row.get("linkageStatus", "")
            if linkage_status not in LINKAGE_STATUSES:
                failures.append(f"{LINKAGE}: {family}: invalid linkageStatus {linkage_status!r}")
            try:
                linked_rows = int(linkage_row.get("linkedRows", ""))
                total_linkage_rows = int(linkage_row.get("totalRows", ""))
                linked_share = float(linkage_row.get("linkedShare", ""))
            except ValueError as exception:
                failures.append(f"{LINKAGE}: {family}: invalid linkage counts ({exception})")
            else:
                if linked_rows < 0 or total_linkage_rows < 0:
                    failures.append(f"{LINKAGE}: {family}: linkage counts must be nonnegative")
                if linked_rows > total_linkage_rows:
                    failures.append(f"{LINKAGE}: {family}: linkedRows exceeds totalRows")
                expected_share = 0.0 if total_linkage_rows == 0 else round(linked_rows / total_linkage_rows, 3)
                if round(linked_share, 3) != expected_share:
                    failures.append(
                        f"{LINKAGE}: {family}: linkedShare {linked_share:.3f} "
                        f"does not match {linked_rows}/{total_linkage_rows}"
                    )
                if linkage_status == "linked" and linked_rows != total_linkage_rows:
                    failures.append(f"{LINKAGE}: {family}: linked status should cover all rows")
                if linkage_status == "metadata linked" and linked_rows <= 0:
                    failures.append(f"{LINKAGE}: {family}: metadata linked status needs positive row coverage")
                if linkage_status == "partially linked" and not (0 < linked_rows < total_linkage_rows):
                    failures.append(f"{LINKAGE}: {family}: partially linked status needs partial row coverage")
                if linkage_status in LINKED_STATUSES:
                    if not linkage_row.get("linkedTo"):
                        failures.append(f"{LINKAGE}: {family}: linked row needs linkedTo")
                    if linkage_row.get("linkKey") in {"", "none"}:
                        failures.append(f"{LINKAGE}: {family}: linked row needs linkKey")
                elif linked_rows != 0:
                    failures.append(f"{LINKAGE}: {family}: unlinked status should have zero linkedRows")
        if roadmap_row:
            if roadmap_row.get("dataset") != source.get("dataset"):
                failures.append(f"{ROADMAP}: {family}: dataset does not match registry")
            if roadmap_row.get("priority") != source.get("priority"):
                failures.append(f"{ROADMAP}: {family}: priority does not match registry")
            if linkage_row and roadmap_row.get("currentLinkageStatus") != linkage_row.get("linkageStatus"):
                failures.append(f"{ROADMAP}: {family}: currentLinkageStatus does not match linkage report")
            if roadmap_row.get("currentLinkageStatus") == "linked":
                failures.append(f"{ROADMAP}: {family}: fully linked source family should not be in roadmap")
            for field in sorted(ROADMAP_REQUIRED_FIELDS):
                value = roadmap_row.get(field, "").strip()
                if not value or value == "not specified":
                    failures.append(f"{ROADMAP}: {family}: missing required roadmap field {field}")
        if raw_manifest_row:
            if raw_manifest_row.get("dataset") != source.get("dataset"):
                failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: dataset does not match registry")
            if raw_manifest_row.get("boundaryCategory") != boundary:
                failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: boundary does not match registry")
            if raw_manifest_row.get("rawPath") != source.get("raw_path"):
                failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: rawPath does not match registry")
        if boundary == "held-out benchmark":
            if gap_row.get("paperStatus") != "held-out benchmark":
                failures.append(f"{GAP}: {family}: paperStatus should be held-out benchmark")
            if "held-out benchmark" not in inventory_row.get("evidenceStatus", ""):
                failures.append(f"{INVENTORY}: {family}: evidenceStatus should name held-out benchmark")
        raw_path = source.get("raw_path", "")
        if raw_path:
            row_count = csv_row_count(Path(raw_path))
            if row_count >= 0 and linkage_row:
                try:
                    linkage_total_rows = int(linkage_row.get("totalRows", "-1"))
                except ValueError:
                    linkage_total_rows = -1
                if linkage_total_rows != row_count:
                    failures.append(
                        f"{LINKAGE}: {family}: totalRows {linkage_row.get('totalRows')} "
                        f"does not match raw rows {row_count}"
                    )
        if source.get("offline_status") == "raw_cached" and raw_path:
            if row_count < 0:
                failures.append(f"{REGISTRY}: {family}: raw_path is missing: {raw_path}")
            elif inventory_row.get("rowCount") and int(inventory_row["rowCount"]) != row_count:
                failures.append(
                    f"{INVENTORY}: {family}: rowCount {inventory_row['rowCount']} "
                    f"does not match raw rows {row_count}"
                )
            elif raw_manifest_row.get("rowCount") and int(raw_manifest_row["rowCount"]) != row_count:
                failures.append(
                    f"{RAW_SOURCE_MANIFEST}: {family}: rowCount {raw_manifest_row['rowCount']} "
                    f"does not match raw rows {row_count}"
                )
            if raw_manifest_row:
                if raw_manifest_row.get("rawStatus") != "present":
                    failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: rawStatus should be present")
                if raw_manifest_row.get("metadataStatus") != "present":
                    failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: metadataStatus should be present")
                raw_file = Path(raw_path)
                if raw_file.exists() and raw_manifest_row.get("rawSha256") != sha256(raw_file):
                    failures.append(f"{RAW_SOURCE_MANIFEST}: {family}: rawSha256 does not match current file")

    inventory_boundary_counts = Counter(row.get("boundaryCategory", "") for row in inventory)
    registry_boundary_counts = Counter(row.get("boundary_category", "") for row in registry)
    if inventory_boundary_counts != registry_boundary_counts:
        failures.append(
            f"inventory boundary counts {dict(inventory_boundary_counts)} "
            f"do not match registry {dict(registry_boundary_counts)}"
        )

    gap_summary = summary_count(GAP_MD, "Held-out benchmark families")
    if gap_summary is None:
        failures.append(f"{GAP_MD}: missing held-out benchmark summary")
    elif gap_summary != (len(registry_heldout), len(registry)):
        failures.append(
            f"{GAP_MD}: held-out summary {gap_summary[0]} / {gap_summary[1]} "
            f"does not match registry {len(registry_heldout)} / {len(registry)}"
        )
    heldout_summary = heldout_pass_summary(HELDOUT_MD)
    if heldout_summary is None:
        failures.append(f"{HELDOUT_MD}: missing targeted-pass summary")
    elif heldout_summary != (len(pass_rows), len(target_rows)):
        failures.append(
            f"{HELDOUT_MD}: pass summary {heldout_summary[0]} / {heldout_summary[1]} "
            f"does not match CSV {len(pass_rows)} / {len(target_rows)}"
        )

    linked_family_count = sum(1 for row in linkage if row.get("linkageStatus") in LINKED_STATUSES)
    linkage_summary = summary_count(LINKAGE_MD, "Linked, metadata-linked, or partially linked source families")
    if linkage_summary is None:
        failures.append(f"{LINKAGE_MD}: missing linked-family summary")
    elif linkage_summary != (linked_family_count, len(linkage)):
        failures.append(
            f"{LINKAGE_MD}: linked summary {linkage_summary[0]} / {linkage_summary[1]} "
            f"does not match CSV {linked_family_count} / {len(linkage)}"
        )
    gap_linkage_summary = summary_count(GAP_MD, "Linked, metadata-linked, or partially linked source families")
    if gap_linkage_summary is None:
        failures.append(f"{GAP_MD}: missing linked-family summary")
    elif gap_linkage_summary != (linked_family_count, len(linkage)):
        failures.append(
            f"{GAP_MD}: linked summary {gap_linkage_summary[0]} / {gap_linkage_summary[1]} "
            f"does not match CSV {linked_family_count} / {len(linkage)}"
        )

    roadmap_required_count = len(roadmap_required_families)
    roadmap_summary = summary_count(ROADMAP_MD, "Source families needing linkage upgrades")
    if roadmap_summary is None:
        failures.append(f"{ROADMAP_MD}: missing roadmap family summary")
    elif roadmap_summary != (roadmap_required_count, len(registry)):
        failures.append(
            f"{ROADMAP_MD}: roadmap summary {roadmap_summary[0]} / {roadmap_summary[1]} "
            f"does not match CSV {roadmap_required_count} / {len(registry)}"
        )
    high_priority_roadmap_rows = sum(1 for row in roadmap if row.get("priority") == "high")
    roadmap_high_summary = summary_count(ROADMAP_MD, "High-priority linkage upgrades")
    if roadmap_high_summary is None:
        failures.append(f"{ROADMAP_MD}: missing high-priority roadmap summary")
    elif roadmap_high_summary != (high_priority_roadmap_rows, len(roadmap)):
        failures.append(
            f"{ROADMAP_MD}: high-priority summary {roadmap_high_summary[0]} / "
            f"{roadmap_high_summary[1]} does not match CSV {high_priority_roadmap_rows} / {len(roadmap)}"
        )

    raw_summary = summary_count(RAW_SOURCE_MANIFEST_MD, "Present raw files")
    if raw_summary is None:
        failures.append(f"{RAW_SOURCE_MANIFEST_MD}: missing present raw file summary")
    else:
        present_rows = sum(1 for row in raw_manifest if row.get("rawStatus") == "present")
        if raw_summary != (present_rows, len(raw_manifest)):
            failures.append(
                f"{RAW_SOURCE_MANIFEST_MD}: present raw summary {raw_summary[0]} / {raw_summary[1]} "
                f"does not match CSV {present_rows} / {len(raw_manifest)}"
            )

    if not GAP_TEX.exists():
        failures.append(f"{GAP_TEX}: missing")
    else:
        tex = GAP_TEX.read_text()
        for family in sorted(registry_heldout):
            if tex_escape(family) not in tex or "held-out benchmark" not in tex:
                failures.append(f"{GAP_TEX}: missing held-out table row for {family}")

    return failures


def main() -> int:
    failures = check()
    if failures:
        print("Empirical boundary check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("Empirical boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
