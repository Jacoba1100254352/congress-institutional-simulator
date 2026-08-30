#!/usr/bin/env python3
"""Write a local-context review for bill-specific finance/lobbying gaps."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW_REVIEW = Path("data/validation/raw/bill_finance_lobbying_local_context_review.csv")
QUEUE = Path("reports/bill-finance-lobbying-review-queue.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-local-context-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-local-context-review.md")

CLAIM_BOUNDARY = (
    "Manual bill-finance/lobbying local-context review only; reviewed rows show "
    "that current cached same-policy campaign-finance sponsor context and LDA "
    "issue/bill context do not contain the reviewed current bill ID. This does "
    "not show absence of campaign spending, outside-spending targets, lobbying "
    "activity, lobbying contacts, sponsor/member targeting, committee-action "
    "influence, roll-call influence, legislative-outcome causality, public "
    "benefit or welfare, causal capture, or model validation."
)

MISSING_LINKS = "; ".join([
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
])

FIELDNAMES = [
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
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def by_rank(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        rank = row.get("review_rank", "").strip()
        if rank in result:
            raise SystemExit(f"duplicate review_rank in {QUEUE}: {rank}")
        result[rank] = row
    return result


def expected_campaign_status(campaign_rows: int) -> tuple[str, str, str]:
    if campaign_rows > 0:
        return (
            "reviewed_same_policy_campaign_context_no_current_bill_match",
            "local_campaign_context_available_no_current_bill_id",
            "same_policy_candidate_sponsor_bill_context_has_no_reviewed_bill_id",
        )
    return (
        "reviewed_no_local_campaign_context_available",
        "local_campaign_context_absent",
        "zero_local_campaign_context_rows_in_queue",
    )


def expected_lobbying_status(lobbying_rows: int) -> tuple[str, str, str]:
    if lobbying_rows > 0:
        return (
            "reviewed_same_policy_lobbying_context_no_current_bill_match",
            "local_lobbying_context_available_no_current_bill_id",
            "same_policy_lobbying_issue_bill_context_has_no_reviewed_bill_id",
        )
    return (
        "reviewed_no_local_lobbying_context_available",
        "local_lobbying_context_absent",
        "zero_local_lobbying_context_rows_in_queue",
    )


def expected_next_source_expansion(campaign_rows: int, lobbying_rows: int) -> str:
    if campaign_rows > 0 and lobbying_rows > 0:
        return "external_current_bill_lobbying_and_campaign_finance_target_search_needed"
    if campaign_rows > 0:
        return "external_current_bill_campaign_finance_target_search_needed"
    if lobbying_rows > 0:
        return "external_current_bill_lobbying_target_search_needed"
    return "external_current_bill_campaign_finance_and_lobbying_source_search_needed"


def evidence_layers(campaign_rows: int, lobbying_rows: int) -> str:
    layers = [
        "bill_law_lifecycle_next_actions",
        "bill_law_evidence_spine",
        "bill_finance_lobbying_review_queue",
        "manual_bill_finance_lobbying_local_context_review",
    ]
    if campaign_rows > 0:
        layers.append("local_campaign_finance_sponsor_policy_context_review")
    if lobbying_rows > 0:
        layers.append("local_lobbying_issue_bill_context_review")
    return "; ".join(layers)


def validate_review_row(raw: dict[str, str], queue_row: dict[str, str]) -> None:
    rank = raw.get("reviewed_queue_rank", "").strip()
    bill_id = raw.get("reviewed_bill_id", "").strip()
    public_law = raw.get("reviewed_public_law_number", "").strip()
    if bill_id != queue_row.get("bill_id", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: bill ID does not match queue")
    if public_law != queue_row.get("public_law_number", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: public law does not match queue")
    if queue_row.get("campaign_finance_current_bill_exact_match", "").strip() != "no":
        raise SystemExit(f"{QUEUE}: rank {rank}: campaign exact match is not a local no-match row")
    if queue_row.get("lobbying_current_bill_exact_match", "").strip() != "no":
        raise SystemExit(f"{QUEUE}: rank {rank}: lobbying exact match is not a local no-match row")

    campaign_rows = parse_int(queue_row.get("campaign_finance_context_rows", ""))
    lobbying_rows = parse_int(queue_row.get("lobbying_context_issue_rows", ""))
    expected_campaign = expected_campaign_status(campaign_rows)
    actual_campaign = (
        raw.get("manual_campaign_context_status", "").strip(),
        raw.get("manual_campaign_context_disposition", "").strip(),
        raw.get("manual_campaign_context_basis", "").strip(),
    )
    if actual_campaign != expected_campaign:
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: campaign review status does not match queue context")
    expected_lobbying = expected_lobbying_status(lobbying_rows)
    actual_lobbying = (
        raw.get("manual_lobbying_context_status", "").strip(),
        raw.get("manual_lobbying_context_disposition", "").strip(),
        raw.get("manual_lobbying_context_basis", "").strip(),
    )
    if actual_lobbying != expected_lobbying:
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: lobbying review status does not match queue context")
    if (
        raw.get("manual_bill_specific_gate_status", "").strip()
        != "reviewed_local_context_no_current_bill_specific_finance_or_lobbying_match"
    ):
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: invalid bill-specific gate status")
    if raw.get("manual_next_source_expansion", "").strip() != expected_next_source_expansion(
        campaign_rows,
        lobbying_rows,
    ):
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: next source expansion does not match context")
    if raw.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
        raise SystemExit(f"{RAW_REVIEW}: rank {rank}: invalid outcome link status")


def build_rows(raw_rows: list[dict[str, str]], queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    queue_by_rank = by_rank(queue_rows)
    if len(raw_rows) != len(queue_rows):
        raise SystemExit(f"{RAW_REVIEW}: expected {len(queue_rows)} review rows; found {len(raw_rows)}")
    output: list[dict[str, str]] = []
    for raw in raw_rows:
        rank = raw.get("reviewed_queue_rank", "").strip()
        queue_row = queue_by_rank.get(rank)
        if queue_row is None:
            raise SystemExit(f"{RAW_REVIEW}: rank {rank}: no matching queue row")
        validate_review_row(raw, queue_row)
        campaign_rows = parse_int(queue_row.get("campaign_finance_context_rows", ""))
        lobbying_rows = parse_int(queue_row.get("lobbying_context_issue_rows", ""))
        output.append({
            "manual_review_rank": rank,
            "review_rank": queue_row.get("review_rank", ""),
            "action_rank": queue_row.get("action_rank", ""),
            "bill_id": queue_row.get("bill_id", ""),
            "public_law_number": queue_row.get("public_law_number", ""),
            "policy_area": queue_row.get("policy_area", ""),
            "sponsor_bioguide_id": queue_row.get("sponsor_bioguide_id", ""),
            "sponsor_party": queue_row.get("sponsor_party", ""),
            "sponsor_state": queue_row.get("sponsor_state", ""),
            "introduced_date": queue_row.get("introduced_date", ""),
            "enacted_date": queue_row.get("enacted_date", ""),
            "lifecycle_readiness_tier": queue_row.get("lifecycle_readiness_tier", ""),
            "review_score": queue_row.get("review_score", ""),
            "actionable_gap_count": queue_row.get("actionable_gap_count", ""),
            "campaign_finance_context_rows": queue_row.get("campaign_finance_context_rows", ""),
            "campaign_finance_context_transaction_rows": queue_row.get("campaign_finance_context_transaction_rows", ""),
            "campaign_finance_unique_candidates": queue_row.get("campaign_finance_unique_candidates", ""),
            "campaign_finance_context_bill_ids": queue_row.get("campaign_finance_context_bill_ids", ""),
            "campaign_finance_context_enacted_bill_ids": queue_row.get("campaign_finance_context_enacted_bill_ids", ""),
            "campaign_finance_current_bill_exact_match": queue_row.get("campaign_finance_current_bill_exact_match", ""),
            "lobbying_context_issue_rows": queue_row.get("lobbying_context_issue_rows", ""),
            "lobbying_context_activity_rows": queue_row.get("lobbying_context_activity_rows", ""),
            "lobbying_context_total_amount": queue_row.get("lobbying_context_total_amount", ""),
            "lobbying_context_bill_contexts": queue_row.get("lobbying_context_bill_contexts", ""),
            "lobbying_context_bill_ids": queue_row.get("lobbying_context_bill_ids", ""),
            "lobbying_context_enacted_bill_ids": queue_row.get("lobbying_context_enacted_bill_ids", ""),
            "lobbying_context_issues": queue_row.get("lobbying_context_issues", ""),
            "lobbying_current_bill_exact_match": queue_row.get("lobbying_current_bill_exact_match", ""),
            "queue_review_status": queue_row.get("review_status", ""),
            "manual_review_source": raw.get("manual_review_source", ""),
            "manual_campaign_context_status": raw.get("manual_campaign_context_status", ""),
            "manual_campaign_context_disposition": raw.get("manual_campaign_context_disposition", ""),
            "manual_campaign_context_basis": raw.get("manual_campaign_context_basis", ""),
            "manual_lobbying_context_status": raw.get("manual_lobbying_context_status", ""),
            "manual_lobbying_context_disposition": raw.get("manual_lobbying_context_disposition", ""),
            "manual_lobbying_context_basis": raw.get("manual_lobbying_context_basis", ""),
            "manual_bill_specific_gate_status": raw.get("manual_bill_specific_gate_status", ""),
            "manual_next_source_expansion": raw.get("manual_next_source_expansion", ""),
            "manual_outcome_link_status": raw.get("manual_outcome_link_status", ""),
            "manual_reviewer_note": raw.get("manual_reviewer_note", ""),
            "recommended_review_sources": queue_row.get("recommended_review_sources", ""),
            "review_packet": queue_row.get("review_packet", ""),
            "evidence_layers": evidence_layers(campaign_rows, lobbying_rows),
            "missing_links": MISSING_LINKS,
            "source_url": queue_row.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return sorted(output, key=lambda row: parse_int(row["manual_review_rank"]))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    campaign_no_match = [
        row for row in rows
        if row["manual_campaign_context_status"] == "reviewed_same_policy_campaign_context_no_current_bill_match"
    ]
    campaign_absent = [
        row for row in rows
        if row["manual_campaign_context_status"] == "reviewed_no_local_campaign_context_available"
    ]
    lobbying_no_match = [
        row for row in rows
        if row["manual_lobbying_context_status"] == "reviewed_same_policy_lobbying_context_no_current_bill_match"
    ]
    lobbying_absent = [
        row for row in rows
        if row["manual_lobbying_context_status"] == "reviewed_no_local_lobbying_context_available"
    ]
    local_exact = [
        row for row in rows
        if row["campaign_finance_current_bill_exact_match"] == "yes"
        or row["lobbying_current_bill_exact_match"] == "yes"
    ]
    external_expansion = [
        row for row in rows
        if row["manual_next_source_expansion"].startswith("external_current_bill_")
    ]
    no_outcome = [
        row for row in rows
        if row["manual_outcome_link_status"] == "no_outcome_influence_evidence"
    ]
    expansion_counts = Counter(row["manual_next_source_expansion"] for row in rows)
    lines = [
        "# Bill Finance/Lobbying Local-Context Review",
        "",
        "This report source-reviews the bill-finance/lobbying queue against current local same-policy campaign-finance sponsor context and LDA issue/bill context. It is a local context review, not validation evidence.",
        "",
        f"- Bill-finance/lobbying queue rows reviewed: {len(rows)}",
        f"- Rows with same-policy campaign-finance context and no current-bill match: {len(campaign_no_match)}",
        f"- Rows with no local campaign-finance context: {len(campaign_absent)}",
        f"- Rows with same-policy lobbying context and no current-bill match: {len(lobbying_no_match)}",
        f"- Rows with no local lobbying context: {len(lobbying_absent)}",
        f"- Rows with local current-bill finance/lobbying exact match: {len(local_exact)}",
        f"- Rows still requiring external target/source expansion: {len(external_expansion)}",
        f"- Rows with no outcome influence evidence: {len(no_outcome)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Next source-expansion statuses:",
    ]
    for status, count in sorted(expansion_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Rank | Bill | Public law | Policy area | Campaign local review | Lobbying local review | Next source expansion |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['manual_review_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['policy_area']} | {row['manual_campaign_context_status']} | "
            f"{row['manual_lobbying_context_status']} | {row['manual_next_source_expansion']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    raw_rows = read_csv(RAW_REVIEW)
    queue_rows = read_csv(QUEUE)
    rows = build_rows(raw_rows, queue_rows)
    if not rows:
        raise SystemExit("No bill-finance/lobbying local-context review rows found.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
