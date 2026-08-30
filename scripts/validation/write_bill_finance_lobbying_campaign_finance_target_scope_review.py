#!/usr/bin/env python3
"""Write a bounded FEC/OpenFEC target-scope review for queued bill-finance rows."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LOCAL_CONTEXT_REVIEW = Path("reports/bill-finance-lobbying-local-context-review.csv")
EXTERNAL_SEARCH_REVIEW = Path("reports/bill-finance-lobbying-external-search-review.csv")
CAMPAIGN_FINANCE_RAW = Path("data/validation/raw/campaign_finance.csv")
CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
CAMPAIGN_FINANCE_MEMBER_CONTEXT = Path("reports/campaign-finance-member-context.csv")
CAMPAIGN_FINANCE_DISTRICT_CONTEXT = Path("reports/campaign-finance-district-context.csv")
CAMPAIGN_FINANCE_ISSUE_CONTEXT = Path("reports/campaign-finance-issue-context.csv")
CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT = Path("reports/campaign-finance-sponsor-bill-context.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-campaign-finance-target-scope-review.md")

CLAIM_BOUNDARY = (
    "Public FEC/OpenFEC target-scope review only; reviewed rows show candidate, "
    "committee, receipt or independent-expenditure metadata and same-policy "
    "candidate sponsored-bill context where cached. The review does not expose "
    "bill IDs in public FEC/OpenFEC records, reviewed external campaign target "
    "documents, campaign spending for or against a bill, reviewed outside-spending "
    "targets beyond public FEC candidate IDs, committees of jurisdiction, "
    "committee-action influence, roll-call influence, legislative-outcome "
    "causality, private contributor details, public benefit or welfare, causal "
    "capture, or model validation."
)

MISSING_LINKS = "; ".join([
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
])

FIELDNAMES = [
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
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def parse_float(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def by_key(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row.get(field, "").strip()
        if not key:
            continue
        if key in result:
            raise SystemExit(f"duplicate {field}={key}")
        result[key] = row
    return result


def by_recipient(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        recipient = row.get("recipient", "").strip()
        if recipient:
            result[recipient].append(row)
    return result


def candidate_context_rows_for_policy(
    sponsor_context_rows: list[dict[str, str]],
    policy_area: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in sponsor_context_rows:
        if policy_area in split_values(row.get("matched_policy_areas", "")):
            rows.append(row)
    return rows


def unique_raw_rows(rows_by_recipient: dict[str, list[dict[str, str]]], recipients: list[str]) -> list[dict[str, str]]:
    seen: set[str] = set()
    rows: list[dict[str, str]] = []
    for recipient in recipients:
        for row in rows_by_recipient.get(recipient, []):
            key = row.get("source_id", "").strip() or "|".join([
                row.get("cycle", ""),
                row.get("recipient", ""),
                row.get("transaction_date", ""),
                row.get("amount", ""),
            ])
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def unique_context_rows(
    rows_by_recipient: dict[str, list[dict[str, str]]],
    recipients: list[str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    for recipient in recipients:
        for row in rows_by_recipient.get(recipient, []):
            key = (recipient, tuple(sorted(row.items())))
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def validate_pending_rows(
    external_rows: list[dict[str, str]],
    local_by_bill: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    pending = [
        row for row in external_rows
        if row.get("campaign_external_scope_status", "") ==
        "fec_public_records_need_candidate_committee_or_outside_spending_target_join"
    ]
    if len(pending) != 4:
        raise SystemExit(f"{EXTERNAL_SEARCH_REVIEW}: expected 4 campaign-finance target-scope rows")
    for row in pending:
        bill_id = row.get("bill_id", "").strip()
        local = local_by_bill.get(bill_id)
        if local is None:
            raise SystemExit(f"{EXTERNAL_SEARCH_REVIEW}: no local-context row for {bill_id}")
        if parse_int(local.get("campaign_finance_context_rows")) <= 0:
            raise SystemExit(f"{LOCAL_CONTEXT_REVIEW}: {bill_id}: expected campaign-finance context rows")
        if local.get("campaign_finance_current_bill_exact_match", "") != "no":
            raise SystemExit(f"{LOCAL_CONTEXT_REVIEW}: {bill_id}: expected no current-bill exact match")
    return pending


def build_rows() -> list[dict[str, str]]:
    local_rows = read_csv(LOCAL_CONTEXT_REVIEW)
    external_rows = read_csv(EXTERNAL_SEARCH_REVIEW)
    raw_rows_by_recipient = by_recipient(read_csv(CAMPAIGN_FINANCE_RAW))
    linkage_by_recipient = by_key(read_csv(CAMPAIGN_FINANCE_LINKAGE), "recipient")
    member_by_recipient = by_key(read_csv(CAMPAIGN_FINANCE_MEMBER_CONTEXT), "recipient")
    district_by_recipient = by_key(read_csv(CAMPAIGN_FINANCE_DISTRICT_CONTEXT), "recipient")
    issue_rows_by_recipient = by_recipient(read_csv(CAMPAIGN_FINANCE_ISSUE_CONTEXT))
    sponsor_context_rows = read_csv(CAMPAIGN_FINANCE_SPONSOR_BILL_CONTEXT)
    local_by_bill = by_key(local_rows, "bill_id")

    pending = validate_pending_rows(external_rows, local_by_bill)
    output: list[dict[str, str]] = []
    for rank, external_row in enumerate(pending, start=1):
        bill_id = external_row.get("bill_id", "").strip()
        reviewed_congress = bill_id.split("-", 1)[0] if "-" in bill_id else ""
        local = local_by_bill[bill_id]
        policy_area = local.get("policy_area", "").strip()
        context_rows = candidate_context_rows_for_policy(sponsor_context_rows, policy_area)
        context_recipients = [row.get("recipient", "").strip() for row in context_rows if row.get("recipient", "").strip()]
        if parse_int(local.get("campaign_finance_context_rows")) != len(context_rows):
            raise SystemExit(
                f"{OUT_CSV}: {bill_id}: campaign context row count mismatch "
                f"local={local.get('campaign_finance_context_rows')} derived={len(context_rows)}"
            )
        expected_context_bill_ids = set(split_values(local.get("campaign_finance_context_bill_ids", "")))
        actual_context_bill_ids = {
            bill
            for row in context_rows
            for bill in split_values(row.get("matched_bill_ids", ""))
        }
        if expected_context_bill_ids != actual_context_bill_ids:
            raise SystemExit(
                f"{OUT_CSV}: {bill_id}: campaign context bill ID mismatch "
                f"local={sorted(expected_context_bill_ids)} derived={sorted(actual_context_bill_ids)}"
            )

        raw_rows = unique_raw_rows(raw_rows_by_recipient, context_recipients)
        issue_rows = unique_context_rows(issue_rows_by_recipient, context_recipients)
        member_rows = [member_by_recipient[r] for r in context_recipients if r in member_by_recipient]
        district_rows = [district_by_recipient[r] for r in context_recipients if r in district_by_recipient]
        linkage_rows = [linkage_by_recipient[r] for r in context_recipients if r in linkage_by_recipient]
        raw_ids = {row.get("source_id", "").strip() for row in raw_rows if row.get("source_id", "").strip()}
        issue_raw_ids = {row.get("source_id", "").strip() for row in issue_rows if row.get("source_id", "").strip()}
        if raw_ids != issue_raw_ids:
            raise SystemExit(
                f"{OUT_CSV}: {bill_id}: issue-context rows do not represent the same raw transaction IDs"
            )

        independent_rows = [
            row for row in raw_rows
            if row.get("independent_expenditure", "").strip() == "1"
        ]
        receipt_rows = [
            row for row in raw_rows
            if row.get("independent_expenditure", "").strip() != "1"
        ]
        context_bill_ids = [
            bill
            for row in context_rows
            for bill in split_values(row.get("matched_bill_ids", ""))
        ]
        context_bill_congresses = sorted({
            bill.split("-", 1)[0]
            for bill in context_bill_ids
            if "-" in bill
        })
        same_congress = reviewed_congress in context_bill_congresses
        candidate_bioguides = [
            row.get("bioguide_id", "").strip()
            for row in context_rows
            if row.get("bioguide_id", "").strip()
        ]
        sponsor_overlap = local.get("sponsor_bioguide_id", "").strip() in set(candidate_bioguides)
        source_urls = []
        for row in [local, external_row, *context_rows, *linkage_rows, *member_rows, *district_rows]:
            source_urls.extend(split_values(row.get("source_urls", "")))
            source_urls.extend(split_values(row.get("source_url", "")))

        output.append({
            "target_scope_review_rank": str(rank),
            "external_review_rank": external_row.get("review_rank", ""),
            "bill_id": bill_id,
            "public_law_number": local.get("public_law_number", ""),
            "policy_area": policy_area,
            "sponsor_bioguide_id": local.get("sponsor_bioguide_id", ""),
            "sponsor_party": local.get("sponsor_party", ""),
            "sponsor_state": local.get("sponsor_state", ""),
            "introduced_date": local.get("introduced_date", ""),
            "enacted_date": local.get("enacted_date", ""),
            "campaign_scope_context_rows": str(len(context_rows)),
            "campaign_scope_transaction_attachments": str(sum(parse_int(row.get("member_context_transaction_rows")) for row in context_rows)),
            "campaign_scope_unique_recipients": str(len(set(context_recipients))),
            "campaign_scope_recipients": join_values(context_recipients),
            "candidate_ids": join_values(row.get("candidate_id", "") for row in linkage_rows),
            "candidate_names": join_values(row.get("candidate_name", "") for row in linkage_rows),
            "candidate_offices": join_values(row.get("candidate_office", "") for row in linkage_rows),
            "candidate_states": join_values(row.get("candidate_office_state", "") for row in linkage_rows),
            "candidate_districts": join_values(row.get("candidate_office_district", "") for row in linkage_rows),
            "member_bioguide_ids": join_values(candidate_bioguides),
            "member_context_statuses": join_values(row.get("member_context_status", "") for row in member_rows),
            "district_context_statuses": join_values(row.get("district_context_status", "") for row in district_rows),
            "district_ids": join_values(row.get("district_id", "") for row in district_rows),
            "principal_campaign_committee_ids": join_values(row.get("principal_campaign_committee_id", "") for row in linkage_rows),
            "linked_committee_ids": join_values(
                committee
                for row in linkage_rows
                for committee in split_values(row.get("linked_committee_ids", ""))
            ),
            "source_schedules": join_values(row.get("source_schedule", "") for row in raw_rows),
            "unique_raw_transaction_rows": str(len(raw_rows)),
            "transaction_source_ids": join_values(row.get("source_id", "") for row in raw_rows),
            "transaction_dates": join_values(row.get("transaction_date", "") for row in raw_rows),
            "transaction_labels": join_values(row.get("industry", "") for row in raw_rows),
            "receipt_rows": str(len(receipt_rows)),
            "receipt_amount": f"{sum(parse_float(row.get('amount')) for row in receipt_rows):.2f}",
            "independent_expenditure_rows": str(len(independent_rows)),
            "independent_expenditure_amount": f"{sum(parse_float(row.get('amount')) for row in independent_rows):.2f}",
            "issue_context_statuses": join_values(row.get("issue_context_status", "") for row in issue_rows),
            "mapped_topics": join_values(row.get("mapped_topic", "") for row in issue_rows),
            "sponsor_context_bill_ids": join_values(context_bill_ids),
            "sponsor_context_bill_congresses": join_values(context_bill_congresses),
            "sponsor_context_policy_areas": join_values(
                policy
                for row in context_rows
                for policy in split_values(row.get("matched_policy_areas", ""))
            ),
            "sponsor_context_enacted_bill_count": str(sum(parse_int(row.get("matched_enacted_bill_count")) for row in context_rows)),
            "current_bill_exact_match_status": "reviewed_no_current_bill_id_in_campaign_finance_context",
            "same_congress_context_status": (
                "same_congress_sponsored_bill_context_present"
                if same_congress
                else "no_same_congress_sponsored_bill_context"
            ),
            "reviewed_bill_sponsor_candidate_overlap_status": (
                "reviewed_bill_sponsor_candidate_overlap"
                if sponsor_overlap
                else "no_reviewed_bill_sponsor_candidate_overlap"
            ),
            "public_fec_target_scope_status": "reviewed_public_fec_openfec_candidate_target_fields_only",
            "outside_spending_target_status": (
                "reviewed_independent_expenditure_candidate_target_only"
                if independent_rows
                else "no_independent_expenditure_rows_in_reviewed_scope"
            ),
            "committee_scope_status": "reviewed_candidate_committee_metadata_no_committee_of_jurisdiction_or_action",
            "bill_identifier_status": "no_bill_id_field_or_current_bill_match_in_public_fec_openfec_scope",
            "outcome_link_status": "no_legislative_outcome_or_influence_evidence",
            "target_scope_disposition": "reviewed_public_fec_openfec_scope_no_bill_specific_campaign_finance_link",
            "next_review_action": (
                "Pursue external campaign target/source documents, committees of jurisdiction, "
                "committee-action records, roll-call context, and legislative outcomes before "
                "making any bill-specific campaign-finance influence claim."
            ),
            "evidence_layers": "; ".join([
                "bill_finance_lobbying_external_search_review",
                "bill_finance_lobbying_local_context_review",
                "campaign_finance_raw_schedule_e",
                "campaign_finance_recipient_metadata",
                "campaign_finance_member_context",
                "campaign_finance_district_context",
                "campaign_finance_issue_context",
                "campaign_finance_sponsor_bill_context",
            ]),
            "missing_links": MISSING_LINKS,
            "source_urls": join_values(source_urls),
            "source_url": local.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["target_scope_disposition"] for row in rows)
    unique_recipients = {
        recipient
        for row in rows
        for recipient in split_values(row.get("campaign_scope_recipients", ""))
    }
    unique_transactions = {
        source_id
        for row in rows
        for source_id in split_values(row.get("transaction_source_ids", ""))
    }
    context_attachments = sum(parse_int(row.get("campaign_scope_context_rows")) for row in rows)
    transaction_attachments = sum(parse_int(row.get("campaign_scope_transaction_attachments")) for row in rows)
    rows_with_candidate_target = sum(
        1 for row in rows
        if row.get("outside_spending_target_status") == "reviewed_independent_expenditure_candidate_target_only"
    )
    lines = [
        "# Bill Finance/Lobbying Campaign-Finance Target-Scope Review",
        "",
        "This report source-reviews the FEC/OpenFEC target scope for the queued bill-finance rows marked by `reports/bill-finance-lobbying-external-search-review.*`. It records only public candidate, committee, receipt/independent-expenditure, member, district, issue-label, and same-policy sponsored-bill context already present in the cached validation files.",
        "",
        f"- Queued campaign-finance public-law rows reviewed: {len(rows)}",
        f"- Candidate/recipient context attachments reviewed: {context_attachments}",
        f"- Campaign-finance transaction attachments represented: {transaction_attachments}",
        f"- Unique public FEC candidate recipients represented: {len(unique_recipients)}",
        f"- Unique raw OpenFEC transactions represented: {len(unique_transactions)}",
        f"- Rows with independent-expenditure candidate target fields only: {rows_with_candidate_target}",
        "- Rows with current-bill IDs in public FEC/OpenFEC scope: 0",
        "- Rows with reviewed bill sponsor/candidate overlap: 0",
        "- Rows with committee-of-jurisdiction or committee-action evidence: 0",
        "- Rows with legislative-outcome or influence evidence: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Target-scope dispositions:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "By bill:",
        "",
        "| Rank | Bill | Public law | Candidate recipients | Transactions | IE amount | Disposition |",
        "| ---: | --- | --- | --- | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            "| {rank} | `{bill}` | `{law}` | {recipients} | {transactions} | {amount} | {status} |".format(
                rank=row["target_scope_review_rank"],
                bill=row["bill_id"],
                law=row["public_law_number"],
                recipients=row["campaign_scope_recipients"],
                transactions=row["unique_raw_transaction_rows"],
                amount=row["independent_expenditure_amount"],
                status=row["target_scope_disposition"],
            )
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
