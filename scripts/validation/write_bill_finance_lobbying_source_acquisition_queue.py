#!/usr/bin/env python3
"""Write source-acquisition targets for finance/lobbying queue gaps."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


COMMITTEE_ACTION_CONTEXT = Path("reports/bill-finance-lobbying-committee-action-context.csv")
BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-committee-action-source-review.csv"
)
BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW = Path(
    "reports/bill-finance-lobbying-roll-call-source-review.csv"
)
BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW = Path(
    "reports/bill-finance-lobbying-member-vote-target-review.csv"
)
GOVINFO_BILLSTATUS_LINKAGE = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
VOTEVIEW_BILL_LINKAGE = Path("reports/voteview-bill-linkage.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-source-acquisition-queue.csv")
OUT_MD = Path("reports/bill-finance-lobbying-source-acquisition-queue.md")

CLAIM_BOUNDARY = (
    "Finance/lobbying source-acquisition queue only; rows name official source "
    "families, source-reviewed govinfo committee/no-direct-committee action "
    "dispositions, reviewed member-vote target scope where applicable, and "
    "remaining coverage gaps for direct member target documents, legislative-outcome causality, and "
    "independent target document review. The "
    "queue does not provide lobbying contact confirmation, campaign-spending "
    "target evidence, support or opposition evidence, committee-action influence, "
    "roll-call influence, legislative-outcome causality, public benefit, welfare, "
    "causal capture, or model validation."
)

BASE_MISSING_LINKS = [
    "lobbying_contact_or_target_source",
    "external_campaign_target_source_document",
    "reviewed_outside_spending_target_beyond_candidate_id",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
]

FIELDNAMES = [
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
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def split_values(value: str | None) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def join_values(values: list[str] | set[str]) -> str:
    ordered: list[str] = []
    for value in values:
        clean = " ".join(str(value or "").split())
        if clean and clean not in ordered:
            ordered.append(clean)
    return "; ".join(ordered)


def bill_parts(bill_id: str) -> tuple[str, str, str]:
    parts = bill_id.split("-")
    if len(parts) != 3:
        raise SystemExit(f"invalid bill_id={bill_id}")
    return parts[0], parts[1], parts[2]


def ordinal_congress(congress: str) -> str:
    number = parse_int(congress)
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}-congress"


def congress_bill_type_path(bill_type: str) -> str:
    if bill_type == "hr":
        return "hr-bill"
    if bill_type == "s":
        return "s-bill"
    return f"{bill_type}-bill"


def congress_bill_base_url(bill_id: str) -> str:
    congress, bill_type, number = bill_parts(bill_id)
    return (
        f"https://www.congress.gov/bill/{ordinal_congress(congress)}/"
        f"{congress_bill_type_path(bill_type)}/{number}"
    )


def congress_api_base_url(bill_id: str) -> str:
    congress, bill_type, number = bill_parts(bill_id)
    return f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{number}"


def by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            result[bill_id] = row
    return result


def voteview_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if not bill_id:
            continue
        counts[bill_id] = counts.get(bill_id, 0) + 1
    return counts


def member_vote_target_summary(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if not bill_id:
            continue
        entry = summary.setdefault(
            bill_id,
            {
                "member_vote_rows": 0,
                "same_bill_campaign_target_overlap_rows": 0,
                "broad_campaign_member_context_overlap_rows": 0,
            },
        )
        entry["member_vote_rows"] += 1
        if row.get("same_bill_campaign_target_match_status") == (
            "same_bill_campaign_target_bioguide_overlap"
        ):
            entry["same_bill_campaign_target_overlap_rows"] += 1
        if row.get("broad_campaign_member_context_status") == (
            "broad_public_fec_candidate_member_context_present"
        ):
            entry["broad_campaign_member_context_overlap_rows"] += 1
    return summary


def source_review_status(source_row: dict[str, str] | None) -> tuple[str, str]:
    if not source_row:
        return "no_official_govinfo_committee_action_source_review_row", ""
    committees = source_row.get("committee_names", "").strip()
    if parse_int(source_row.get("committee_count")) > 0 and committees:
        return "official_govinfo_committee_source_review_present", committees
    if source_row.get("committee_source_status") == (
        "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ):
        return "official_govinfo_billstatus_reviewed_without_direct_committee_names", ""
    if source_row.get("govinfo_billstatus_status") == "official_govinfo_billstatus_fetched":
        return "official_govinfo_billstatus_source_review_without_committee_names", ""
    return "official_govinfo_committee_action_source_review_unavailable", ""


def committee_jurisdiction_status(source_row: dict[str, str] | None) -> str:
    if source_row and parse_int(source_row.get("committee_count")) > 0:
        return "official_committee_of_jurisdiction_source_reviewed"
    if source_row and source_row.get("committee_source_status") == (
        "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ):
        return "official_govinfo_billstatus_reviewed_without_direct_committee_referral"
    if source_row and source_row.get("govinfo_billstatus_status") == "official_govinfo_billstatus_fetched":
        return "official_govinfo_billstatus_reviewed_without_committee_names_needs_committee_source_followup"
    return "needs_official_committee_source_acquisition"


def committee_action_status(row: dict[str, str], source_row: dict[str, str] | None) -> str:
    if source_row and source_row.get("committee_action_record_status") == (
        "official_govinfo_committee_action_records_present"
    ):
        return "official_committee_action_records_reviewed_no_influence_evidence"
    if source_row and source_row.get("committee_action_record_status") == (
        "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
    ):
        return "official_govinfo_billstatus_reviewed_without_direct_committee_action_records"
    if row.get("committee_reported") == "yes":
        return "committee_reported_flag_needs_source_reviewed_committee_record"
    return "no_committee_reported_flag_still_needs_committee_jurisdiction_review"


def roll_call_status(
    row: dict[str, str],
    local_vote_rows: int,
    source_row: dict[str, str] | None,
    roll_call_row: dict[str, str] | None,
) -> str:
    if local_vote_rows > 0:
        return "local_voteview_roll_call_context_present_needs_source_review"
    if roll_call_row and roll_call_row.get("roll_call_source_review_status") == (
        "official_house_clerk_roll_call_source_reviewed"
    ):
        return "official_house_clerk_roll_call_source_reviewed_no_finance_lobbying_influence_evidence"
    if roll_call_row and roll_call_row.get("roll_call_source_review_status") == (
        "official_floor_action_reviewed_without_numbered_roll_call"
    ):
        return "official_floor_action_reviewed_without_numbered_roll_call"
    if source_row and parse_int(source_row.get("roll_call_reference_count")) > 0:
        return "official_billstatus_roll_call_references_present_needs_vote_source_join"
    if source_row and parse_int(source_row.get("floor_action_count")) > 0:
        return "floor_action_source_reviewed_needs_official_roll_call_vote_source"
    if row.get("floor_considered") == "yes":
        return "floor_considered_flag_without_local_voteview_match_needs_official_roll_call_source"
    return "no_floor_flag_and_no_local_roll_call_context"


def legislative_outcome_status(source_row: dict[str, str] | None) -> str:
    if source_row and source_row.get("legislative_outcome_source_status") == (
        "official_govinfo_public_law_outcome_metadata_present_no_finance_lobbying_causality"
    ):
        return "official_govinfo_public_law_outcome_source_reviewed_no_finance_lobbying_causality_source"
    return "enacted_public_law_metadata_present_no_finance_lobbying_causality_source"


def lobbying_target_status(row: dict[str, str]) -> str:
    if parse_int(row.get("external_lda_mention_packets")) > 0:
        return "external_lda_current_bill_mentions_need_independent_contact_or_target_source_review"
    if parse_int(row.get("external_lda_exact_activity_match_rows")) > 0:
        return "external_lda_current_bill_rows_need_packet_review"
    return "no_external_lda_current_bill_mention_needs_broader_lobbying_target_source"


def campaign_target_status(row: dict[str, str]) -> str:
    status = row.get("campaign_target_scope_status", "")
    if status == "not_in_campaign_finance_target_scope_review":
        return "not_in_campaign_finance_target_scope_review"
    return "public_fec_openfec_target_scope_reviewed_no_bill_specific_target_source"


def member_vote_target_scope_status(
    roll_call_row: dict[str, str] | None,
    member_summary: dict[str, int] | None,
) -> str:
    if roll_call_row and roll_call_row.get("roll_call_source_review_status") == (
        "official_floor_action_reviewed_without_numbered_roll_call"
    ):
        return "not_applicable_floor_action_without_numbered_member_vote_rows"
    if not roll_call_row or roll_call_row.get("roll_call_source_review_status") != (
        "official_house_clerk_roll_call_source_reviewed"
    ):
        return "needs_official_member_vote_source_before_target_scope_review"
    if not member_summary or member_summary.get("member_vote_rows", 0) == 0:
        return "official_roll_call_source_reviewed_needs_member_vote_target_scope_review"
    if member_summary.get("same_bill_campaign_target_overlap_rows", 0) > 0:
        return "official_member_vote_rows_joined_to_same_bill_campaign_target_scope_no_influence_evidence"
    return "official_member_vote_rows_reviewed_no_same_bill_campaign_target_overlap"


def priority_score(
    row: dict[str, str],
    local_vote_rows: int,
    source_row: dict[str, str] | None = None,
) -> int:
    score = 0
    direct_committee_source = bool(
        source_row
        and (
            parse_int(source_row.get("committee_count")) > 0
            or source_row.get("committee_action_record_status")
            == "official_govinfo_committee_action_records_present"
        )
    )
    if row.get("committee_reported") == "yes" and (source_row is None or direct_committee_source):
        score += 2
    if row.get("floor_considered") == "yes":
        score += 2
    if parse_int(row.get("external_lda_mention_packets")) > 0:
        score += 3
    if row.get("campaign_target_scope_status") != "not_in_campaign_finance_target_scope_review":
        score += 2
    if local_vote_rows == 0 and row.get("floor_considered") == "yes":
        score += 1
    return score


def missing_links(source_row: dict[str, str] | None) -> str:
    return missing_links_for_sources(source_row, None)


def missing_links_for_sources(
    source_row: dict[str, str] | None,
    roll_call_row: dict[str, str] | None,
    member_summary: dict[str, int] | None = None,
) -> str:
    links = list(BASE_MISSING_LINKS)
    source_reviewed_no_direct_committee = bool(
        source_row
        and source_row.get("committee_source_status")
        == "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    )
    committee_action_status_value = (
        source_row.get("committee_action_record_status") if source_row else ""
    )
    if not source_row:
        links.insert(0, "committee_of_jurisdiction")
    if committee_action_status_value not in {
        "official_govinfo_committee_action_records_present",
        "official_govinfo_billstatus_reviewed_without_direct_committee_action_records",
    }:
        links.insert(0, "source_reviewed_committee_action_record")
    if source_row and parse_int(source_row.get("committee_count")) == 0 and not source_reviewed_no_direct_committee:
        links.insert(0, "committee_of_jurisdiction")
    if roll_call_row and roll_call_row.get("roll_call_source_review_status") == (
        "official_house_clerk_roll_call_source_reviewed"
    ):
        if member_summary and member_summary.get("member_vote_rows", 0) > 0:
            links.insert(0, "direct_member_vote_target_document")
        else:
            links.insert(0, "member_level_vote_target_join_to_finance_lobbying_source")
    elif roll_call_row and roll_call_row.get("roll_call_source_review_status") == (
        "official_floor_action_reviewed_without_numbered_roll_call"
    ):
        pass
    elif not source_row or parse_int(source_row.get("roll_call_reference_count")) == 0:
        links.insert(0, "official_roll_call_context")
    else:
        links.insert(0, "official_roll_call_vote_source_join")
    return join_values(links)


def build_rows() -> list[dict[str, str]]:
    context_rows = sorted(
        read_csv(COMMITTEE_ACTION_CONTEXT),
        key=lambda row: parse_int(row.get("context_rank")),
    )
    source_review_by_bill = by_bill(read_csv(BILL_FINANCE_LOBBYING_COMMITTEE_ACTION_SOURCE_REVIEW))
    roll_call_review_by_bill = by_bill(read_csv(BILL_FINANCE_LOBBYING_ROLL_CALL_SOURCE_REVIEW))
    member_vote_summary_by_bill = member_vote_target_summary(
        read_csv(BILL_FINANCE_LOBBYING_MEMBER_VOTE_TARGET_REVIEW)
    )
    govinfo_by_bill = by_bill(read_csv(GOVINFO_BILLSTATUS_LINKAGE))
    vote_counts = voteview_counts(read_csv(VOTEVIEW_BILL_LINKAGE))
    rows: list[dict[str, str]] = []
    for context in context_rows:
        bill_id = context["bill_id"]
        source_review = source_review_by_bill.get(bill_id)
        roll_call_review = roll_call_review_by_bill.get(bill_id)
        member_vote_summary = member_vote_summary_by_bill.get(bill_id)
        gov_status, committees = source_review_status(source_review)
        local_vote_rows = vote_counts.get(bill_id, 0)
        base_url = congress_bill_base_url(bill_id)
        api_base_url = congress_api_base_url(bill_id)
        score = priority_score(context, local_vote_rows, source_review)
        source_urls = split_values(context.get("source_urls"))
        source_urls.extend([
            f"{base_url}/committees",
            f"{base_url}/all-actions",
            f"{api_base_url}/committees",
            f"{api_base_url}/actions",
            "https://clerk.house.gov/Votes",
            "https://www.senate.gov/legislative/votes_new.htm",
        ])
        if source_review:
            source_urls.extend([
                source_review.get("govinfo_url", ""),
                source_review.get("source_url", ""),
            ])
        if roll_call_review:
            source_urls.extend([
                roll_call_review.get("official_vote_source_url", ""),
                roll_call_review.get("source_url", ""),
            ])
        member_vote_status = member_vote_target_scope_status(roll_call_review, member_vote_summary)
        evidence_layers = [
            "bill_finance_lobbying_committee_action_context",
            "bill_finance_lobbying_committee_action_source_review",
            "bill_finance_lobbying_roll_call_source_review",
            "local_govinfo_billstatus_linkage_coverage_check",
            "local_voteview_bill_linkage_coverage_check",
            "official_source_acquisition_targets",
        ]
        if member_vote_summary and member_vote_summary.get("member_vote_rows", 0) > 0:
            evidence_layers.append("bill_finance_lobbying_member_vote_target_scope_review")
        if source_review:
            evidence_layers.extend(split_values(source_review.get("evidence_layers")))
        if roll_call_review:
            evidence_layers.extend(split_values(roll_call_review.get("evidence_layers")))
        rows.append({
            "acquisition_rank": str(len(rows) + 1),
            "review_rank": context.get("review_rank", ""),
            "bill_id": bill_id,
            "public_law_number": context.get("public_law_number", ""),
            "policy_area": context.get("policy_area", ""),
            "sponsor_bioguide_id": context.get("sponsor_bioguide_id", ""),
            "sponsor_party": context.get("sponsor_party", ""),
            "sponsor_state": context.get("sponsor_state", ""),
            "introduced_date": context.get("introduced_date", ""),
            "enacted_date": context.get("enacted_date", ""),
            "committee_reported": context.get("committee_reported", ""),
            "floor_considered": context.get("floor_considered", ""),
            "external_lda_exact_activity_match_rows": context.get("external_lda_exact_activity_match_rows", ""),
            "external_lda_mention_packets": context.get("external_lda_mention_packets", ""),
            "campaign_target_scope_status": context.get("campaign_target_scope_status", ""),
            "local_govinfo_committee_row_status": gov_status,
            "local_govinfo_committees": committees,
            "local_voteview_roll_call_rows": str(local_vote_rows),
            "official_member_vote_rows": str(
                member_vote_summary.get("member_vote_rows", 0) if member_vote_summary else 0
            ),
            "member_vote_target_scope_status": member_vote_status,
            "same_bill_campaign_target_member_vote_overlap_rows": str(
                member_vote_summary.get("same_bill_campaign_target_overlap_rows", 0)
                if member_vote_summary
                else 0
            ),
            "broad_campaign_member_context_overlap_rows": str(
                member_vote_summary.get("broad_campaign_member_context_overlap_rows", 0)
                if member_vote_summary
                else 0
            ),
            "committee_jurisdiction_acquisition_status": committee_jurisdiction_status(source_review),
            "committee_action_record_acquisition_status": committee_action_status(context, source_review),
            "roll_call_acquisition_status": roll_call_status(
                context,
                local_vote_rows,
                source_review,
                roll_call_review,
            ),
            "lobbying_target_source_acquisition_status": lobbying_target_status(context),
            "campaign_target_source_acquisition_status": campaign_target_status(context),
            "legislative_outcome_source_status": legislative_outcome_status(source_review),
            "priority_score": str(score),
            "next_review_action": (
                "Use the official govinfo committee/action and House Clerk roll-call source "
                "reviews plus the member-vote target-scope review as context, then acquire "
                "independent finance/lobbying target documents, "
                "direct member target documents where numbered roll calls exist, and direct influence or "
                "causality evidence before any influence claim."
            ),
            "required_join_keys": (
                "bill_id; public_law_number; congress; bill_type; bill_number; "
                "committee_name; action_date; roll_call_id; filing_uuid; candidate_id; "
                "independent_target_document_id"
            ),
            "official_committee_source_url": f"{base_url}/committees",
            "official_actions_source_url": f"{base_url}/all-actions",
            "official_roll_call_source_urls": join_values([
                f"{base_url}/all-actions",
                "https://clerk.house.gov/Votes",
                "https://www.senate.gov/legislative/votes_new.htm",
            ]),
            "official_api_committee_url": f"{api_base_url}/committees",
            "official_api_actions_url": f"{api_base_url}/actions",
            "evidence_layers": join_values(evidence_layers),
            "missing_links": missing_links_for_sources(source_review, roll_call_review, member_vote_summary),
            "source_urls": join_values(source_urls),
            "source_url": context.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    rows.sort(key=lambda row: (-parse_int(row["priority_score"]), parse_int(row["review_rank"])))
    for index, row in enumerate(rows, start=1):
        row["acquisition_rank"] = str(index)
    return rows


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def write_md(rows: list[dict[str, str]]) -> None:
    govinfo_with_committees = [
        row for row in rows
        if row["local_govinfo_committee_row_status"] == "official_govinfo_committee_source_review_present"
    ]
    govinfo_no_direct_committees = [
        row for row in rows
        if row["local_govinfo_committee_row_status"]
        == "official_govinfo_billstatus_reviewed_without_direct_committee_names"
    ]
    voteview_rows = [
        row for row in rows
        if parse_int(row["local_voteview_roll_call_rows"]) > 0
    ]
    official_roll_call_rows = [
        row for row in rows
        if row["roll_call_acquisition_status"]
        == "official_house_clerk_roll_call_source_reviewed_no_finance_lobbying_influence_evidence"
    ]
    member_vote_target_rows = [
        row for row in rows
        if row["member_vote_target_scope_status"]
        in {
            "official_member_vote_rows_joined_to_same_bill_campaign_target_scope_no_influence_evidence",
            "official_member_vote_rows_reviewed_no_same_bill_campaign_target_overlap",
        }
    ]
    member_vote_rows = sum(parse_int(row["official_member_vote_rows"]) for row in rows)
    same_bill_member_vote_overlap_rows = sum(
        parse_int(row["same_bill_campaign_target_member_vote_overlap_rows"]) for row in rows
    )
    broad_campaign_member_context_overlap_rows = sum(
        parse_int(row["broad_campaign_member_context_overlap_rows"]) for row in rows
    )
    no_numbered_roll_call_rows = [
        row for row in rows
        if row["roll_call_acquisition_status"]
        == "official_floor_action_reviewed_without_numbered_roll_call"
    ]
    roll_call_acquisition_rows = [
        row for row in rows
        if row["roll_call_acquisition_status"] in {
            "official_billstatus_roll_call_references_present_needs_vote_source_join",
            "floor_action_source_reviewed_needs_official_roll_call_vote_source",
            "floor_considered_flag_without_local_voteview_match_needs_official_roll_call_source",
        }
    ]
    committee_acquisition_rows = [
        row for row in rows
        if row["committee_jurisdiction_acquisition_status"]
        not in {
            "official_committee_of_jurisdiction_source_reviewed",
            "official_govinfo_billstatus_reviewed_without_direct_committee_referral",
        }
    ]
    lda_priority_rows = [
        row for row in rows
        if parse_int(row["external_lda_mention_packets"]) > 0
    ]
    campaign_priority_rows = [
        row for row in rows
        if row["campaign_target_scope_status"] != "not_in_campaign_finance_target_scope_review"
    ]
    status_counts = Counter(row["roll_call_acquisition_status"] for row in rows)
    lines = [
        "# Bill Finance/Lobbying Source-Acquisition Queue",
        "",
        "This report turns the committee/action context gap into official source-acquisition targets. It is a review queue, not finance/lobbying influence evidence.",
        "",
        f"- Queued public-law rows: {len(rows)}",
        f"- Rows with official govinfo committee names: {len(govinfo_with_committees)}",
        f"- Rows source-reviewed without direct committee names: {len(govinfo_no_direct_committees)}",
        f"- Rows with local Voteview roll-call context: {len(voteview_rows)}",
        f"- Rows with official House Clerk roll-call source review: {len(official_roll_call_rows)}",
        f"- Rows with official member-vote target-scope review: {len(member_vote_target_rows)}",
        f"- Official member-vote rows reviewed for target scope: {member_vote_rows}",
        f"- Member-vote rows with same-bill reviewed campaign target Bioguide overlap: {same_bill_member_vote_overlap_rows}",
        f"- Member-vote rows with broad public FEC member-context overlap: {broad_campaign_member_context_overlap_rows}",
        f"- Rows reviewed as floor actions without numbered roll calls: {len(no_numbered_roll_call_rows)}",
        f"- Rows needing official roll-call source acquisition: {len(roll_call_acquisition_rows)}",
        f"- Rows needing official committee-of-jurisdiction acquisition: {len(committee_acquisition_rows)}",
        f"- Rows with external LDA mention packets to prioritize: {len(lda_priority_rows)}",
        f"- Rows with campaign target-scope review to prioritize: {len(campaign_priority_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Roll-call acquisition statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Rank | Bill | Priority | Committee source | Action source | Roll-call status | LDA packets | Campaign scope |",
        "| ---: | --- | ---: | --- | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['acquisition_rank']} | `{row['bill_id']}` | {row['priority_score']} | "
            f"{row['official_committee_source_url']} | {row['official_actions_source_url']} | "
            f"{md_escape(row['roll_call_acquisition_status'])} | "
            f"{row['external_lda_mention_packets']} | {md_escape(row['campaign_target_scope_status'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No bill-finance/lobbying source-acquisition rows found.")
    write_csv(OUT_CSV, rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
