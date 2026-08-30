#!/usr/bin/env python3
"""Write a source-review queue for bill-specific finance/lobbying gaps."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
SPINE = Path("reports/bill-law-evidence-spine.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-review-queue.csv")
OUT_MD = Path("reports/bill-finance-lobbying-review-queue.md")

TARGET_GATE = "bill_specific_campaign_finance_or_lobbying_to_bill"
CLAIM_BOUNDARY = (
    "Finance/lobbying source-review queue only; same-policy campaign-finance "
    "and lobbying rows are context for targeted review, not evidence that money, "
    "clients, registrants, candidates, committees, or lobbyists targeted, funded, "
    "caused, influenced, supported, opposed, or benefited any specific bill, "
    "committee action, roll call, public law, implementation outcome, public "
    "benefit, welfare, causal capture, or model validation."
)

FIELDNAMES = [
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
]

MISSING_LINKS = "; ".join([
    "bill_specific_campaign_finance_or_lobbying_to_bill",
    "reviewed_outside_spending_target",
    "filing_text_bill_identifier",
    "client_to_specific_bill",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    result: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in result:
            result.append(clean)
    return result


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def as_float(value: str) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def by_public_law(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("public_law_number", "").strip(): row
        for row in rows
        if row.get("public_law_number", "").strip()
    }


def review_status(
    current_bill_campaign_match: bool,
    current_bill_lobbying_match: bool,
    campaign_rows: int,
    lobbying_rows: int,
) -> str:
    if current_bill_campaign_match or current_bill_lobbying_match:
        return "candidate_exact_bill_match_needs_source_review"
    if campaign_rows > 0 and lobbying_rows > 0:
        return "same_policy_finance_and_lobbying_context_needs_bill_specific_review"
    if campaign_rows > 0:
        return "same_policy_campaign_finance_context_needs_bill_specific_review"
    if lobbying_rows > 0:
        return "same_policy_lobbying_context_needs_bill_specific_review"
    return "no_current_finance_or_lobbying_context_needs_source_expansion"


def build_rows(
    next_action_rows: list[dict[str, str]],
    spine_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    spine_by_public_law = by_public_law(spine_rows)
    target_rows = [
        row for row in next_action_rows
        if row.get("next_actionable_upgrade_gate", "").strip() == TARGET_GATE
    ]
    output: list[dict[str, str]] = []
    for index, action in enumerate(target_rows, start=1):
        public_law = action.get("public_law_number", "").strip()
        spine = spine_by_public_law.get(public_law)
        if spine is None:
            raise SystemExit(f"missing spine row for public law {public_law}")
        bill_id = action.get("bill_id", "").strip()
        campaign_bill_ids = split_values(spine.get("campaign_finance_sponsor_policy_context_bill_ids", ""))
        lobbying_bill_ids = split_values(spine.get("lobbying_policy_context_bill_ids", ""))
        campaign_exact = bill_id in set(campaign_bill_ids)
        lobbying_exact = bill_id in set(lobbying_bill_ids)
        campaign_rows = as_int(spine.get("campaign_finance_sponsor_policy_context_rows", ""))
        lobbying_rows = as_int(spine.get("lobbying_policy_context_issue_rows", ""))
        layers = ["bill_law_lifecycle_next_actions", "bill_law_evidence_spine"]
        if campaign_rows > 0:
            layers.append("same_policy_campaign_finance_context")
        if lobbying_rows > 0:
            layers.append("same_policy_lobbying_issue_bill_context")
        if campaign_exact:
            layers.append("candidate_current_bill_campaign_context")
        if lobbying_exact:
            layers.append("candidate_current_bill_lobbying_context")
        status = review_status(campaign_exact, lobbying_exact, campaign_rows, lobbying_rows)
        recommended_sources = [
            "OpenFEC independent-expenditure communication/target records",
            "FEC committee and candidate transaction detail",
            "Senate LDA filing text and bill-number mentions",
            "committee-of-jurisdiction and action records",
            "Congress.gov bill and public-law metadata",
        ]
        output.append({
            "review_rank": str(index),
            "action_rank": action.get("action_rank", ""),
            "bill_id": bill_id,
            "public_law_number": public_law,
            "policy_area": action.get("policy_area", ""),
            "sponsor_bioguide_id": spine.get("sponsor_bioguide_id", ""),
            "sponsor_party": spine.get("sponsor_party", ""),
            "sponsor_state": spine.get("sponsor_state", ""),
            "introduced_date": spine.get("introduced_date", ""),
            "enacted_date": spine.get("enacted_date", ""),
            "lifecycle_readiness_tier": action.get("lifecycle_readiness_tier", ""),
            "review_score": action.get("review_score", ""),
            "actionable_gap_count": action.get("actionable_gap_count", ""),
            "campaign_finance_context_rows": spine.get("campaign_finance_sponsor_policy_context_rows", ""),
            "campaign_finance_context_transaction_rows": spine.get("campaign_finance_sponsor_policy_context_transaction_rows", ""),
            "campaign_finance_unique_candidates": spine.get("campaign_finance_sponsor_policy_context_unique_candidates", ""),
            "campaign_finance_context_bill_ids": "; ".join(campaign_bill_ids),
            "campaign_finance_context_enacted_bill_ids": spine.get("campaign_finance_sponsor_policy_context_enacted_bill_ids", ""),
            "campaign_finance_current_bill_exact_match": yes_no(campaign_exact),
            "lobbying_context_issue_rows": spine.get("lobbying_policy_context_issue_rows", ""),
            "lobbying_context_activity_rows": spine.get("lobbying_policy_context_activity_rows", ""),
            "lobbying_context_total_amount": f"{as_float(spine.get('lobbying_policy_context_total_amount', '0')):.2f}",
            "lobbying_context_bill_contexts": spine.get("lobbying_policy_context_bill_contexts", ""),
            "lobbying_context_bill_ids": "; ".join(lobbying_bill_ids),
            "lobbying_context_enacted_bill_ids": spine.get("lobbying_policy_context_enacted_bill_ids", ""),
            "lobbying_context_issues": spine.get("lobbying_policy_context_issues", ""),
            "lobbying_current_bill_exact_match": yes_no(lobbying_exact),
            "review_status": status,
            "recommended_review_sources": "; ".join(recommended_sources),
            "review_packet": " | ".join([
                f"bill_id={bill_id}",
                f"public_law={public_law}",
                f"policy_area={action.get('policy_area', '')}",
                f"campaign_exact_match={yes_no(campaign_exact)}",
                f"lobbying_exact_match={yes_no(lobbying_exact)}",
                f"campaign_context_bills={'; '.join(campaign_bill_ids)}",
                f"lobbying_context_bills={'; '.join(lobbying_bill_ids)}",
            ]),
            "evidence_layers": "; ".join(layers),
            "missing_links": MISSING_LINKS,
            "source_url": spine.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["review_status"] for row in rows)
    campaign_context_rows = [
        row for row in rows
        if as_int(row.get("campaign_finance_context_rows", "")) > 0
    ]
    lobbying_context_rows = [
        row for row in rows
        if as_int(row.get("lobbying_context_issue_rows", "")) > 0
    ]
    exact_campaign_rows = [
        row for row in rows
        if row.get("campaign_finance_current_bill_exact_match") == "yes"
    ]
    exact_lobbying_rows = [
        row for row in rows
        if row.get("lobbying_current_bill_exact_match") == "yes"
    ]
    total_lobbying_activity = sum(as_int(row.get("lobbying_context_activity_rows", "")) for row in rows)
    total_campaign_transactions = sum(as_int(row.get("campaign_finance_context_transaction_rows", "")) for row in rows)
    lines = [
        "# Bill Finance/Lobbying Review Queue",
        "",
        "This report isolates public-law rows whose next actionable lifecycle gate is bill-specific campaign-finance or lobbying evidence. It is a source-review queue, not validation evidence.",
        "",
        f"- Queued public-law rows: {len(rows)}",
        f"- Rows with same-policy campaign-finance context: {len(campaign_context_rows)}",
        f"- Rows with same-policy lobbying context: {len(lobbying_context_rows)}",
        f"- Rows with current bill ID in campaign-finance context: {len(exact_campaign_rows)}",
        f"- Rows with current bill ID in lobbying context: {len(exact_lobbying_rows)}",
        f"- Campaign-finance context transaction rows represented: {total_campaign_transactions}",
        f"- LDA activity rows represented by same-policy context: {total_lobbying_activity}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Review statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Rank | Bill | Public law | Policy area | Campaign exact | Lobbying exact | Campaign rows | LDA rows | Review status |",
        "| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['policy_area']} | {row['campaign_finance_current_bill_exact_match']} | "
            f"{row['lobbying_current_bill_exact_match']} | "
            f"{row['campaign_finance_context_transaction_rows'] or '0'} | "
            f"{row['lobbying_context_activity_rows'] or '0'} | {row['review_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    next_action_rows = read_csv(NEXT_ACTIONS)
    spine_rows = read_csv(SPINE)
    rows = build_rows(next_action_rows, spine_rows)
    if not rows:
        raise SystemExit("No bill-specific finance/lobbying lifecycle rows found.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
