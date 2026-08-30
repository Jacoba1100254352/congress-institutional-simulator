#!/usr/bin/env python3
"""Write a bounded external-search review for bill-finance/lobbying gaps."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LOCAL_CONTEXT_REVIEW = Path("reports/bill-finance-lobbying-local-context-review.csv")
LDA_SEARCHES = Path("data/validation/raw/bill_finance_lobbying_external_lda_searches.csv")
LDA_MENTIONS = Path("data/validation/raw/bill_finance_lobbying_external_lda_mentions.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-external-search-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-external-search-review.md")

CLAIM_BOUNDARY = (
    "External source-search review only; exact LDA activity-text bill mentions "
    "show disclosed lobbying activity text that mentions the reviewed current bill, "
    "and FEC source-scope triage identifies public candidate/committee/outside-spending "
    "fields needed for later review. This does not show lobbying contacts, support, "
    "opposition, campaign spending for or against a bill, sponsor/member targeting, "
    "committee-action influence, roll-call influence, legislative-outcome causality, "
    "public benefit or welfare, causal capture, or model validation."
)

FEC_SOURCE_SCOPE_BOUNDARY = (
    "Public FEC/OpenFEC source-scope triage only; public FEC records expose "
    "candidate, committee, receipt, and independent-expenditure target fields, "
    "not bill IDs or bill-specific campaign-finance influence."
)

MISSING_LINKS = "; ".join([
    "source_reviewed_support_or_opposition_disposition",
    "lobbying_contact_or_target_source",
    "sponsor_or_member_target_beyond_activity_text_reference",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "candidate_or_committee_campaign_finance_target_join",
    "reviewed_outside_spending_target",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

FIELDNAMES = [
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "introduced_date",
    "enacted_date",
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
    "lda_source_urls",
    "campaign_external_scope_status",
    "campaign_external_next_step",
    "combined_external_review_status",
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


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def join_values(values: set[str] | list[str]) -> str:
    return "; ".join(sorted(v for v in values if v))


def grouped_by_bill(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("bill_id", "")].append(row)
    return grouped


def campaign_scope_status(local_row: dict[str, str]) -> tuple[str, str]:
    expansion = local_row.get("manual_next_source_expansion", "")
    if "campaign_finance" not in expansion:
        return (
            "campaign_finance_external_search_not_in_current_row_scope",
            "No campaign-finance target/source expansion is queued for this row after the local context review.",
        )
    return (
        "fec_public_records_need_candidate_committee_or_outside_spending_target_join",
        (
            "Review public FEC/OpenFEC candidate, committee, receipt, and independent-expenditure "
            "target fields; do not infer bill-specific campaign-finance targeting from public FEC "
            "records without an external target/source document."
        ),
    )


def lda_disposition(search_rows: list[dict[str, str]], mention_rows: list[dict[str, str]]) -> str:
    if not search_rows:
        return "official_lda_external_search_missing"
    if any(row.get("api_status") != "ok" for row in search_rows):
        return "official_lda_external_search_partial_or_error"
    if sum(parse_int(row.get("unfetched_api_result_count")) for row in search_rows) > 0:
        return "official_lda_external_search_partial_unfetched_results"
    if mention_rows:
        return "official_lda_external_current_bill_activity_text_match"
    return "official_lda_external_search_no_exact_current_bill_activity_text_match"


def combined_status(lda_status: str, campaign_status: str) -> str:
    campaign_pending = campaign_status.startswith("fec_public_records_need")
    if lda_status == "official_lda_external_current_bill_activity_text_match" and campaign_pending:
        return "external_lda_bill_reference_found_campaign_target_scope_pending"
    if lda_status == "official_lda_external_current_bill_activity_text_match":
        return "external_lda_bill_reference_found"
    if campaign_pending:
        return "external_lda_no_exact_match_campaign_target_scope_pending"
    return "external_search_review_no_exact_lda_match_campaign_not_scoped"


def validate_search_coverage(local_rows: list[dict[str, str]], searches_by_bill: dict[str, list[dict[str, str]]]) -> None:
    local_bill_ids = {row.get("bill_id", "") for row in local_rows}
    search_bill_ids = {bill_id for bill_id, rows in searches_by_bill.items() if rows}
    if local_bill_ids != search_bill_ids:
        raise SystemExit(
            f"LDA external search bill mismatch: missing={sorted(local_bill_ids - search_bill_ids)}, "
            f"extra={sorted(search_bill_ids - local_bill_ids)}"
        )
    for row in local_rows:
        bill_id = row.get("bill_id", "")
        years = {
            str(year)
            for year in range(parse_int(row.get("introduced_date", "")[:4]), parse_int(row.get("enacted_date", "")[:4]) + 1)
        }
        terms = {search.get("term_variant", "") for search in searches_by_bill[bill_id]}
        searched_years = {search.get("filing_year", "") for search in searches_by_bill[bill_id]}
        if not {"compact", "dotted"} <= terms:
            raise SystemExit(f"{LDA_SEARCHES}: {bill_id}: compact and dotted term variants are required")
        if years and not years <= searched_years:
            raise SystemExit(f"{LDA_SEARCHES}: {bill_id}: missing filing years {sorted(years - searched_years)}")


def build_rows() -> list[dict[str, str]]:
    local_rows = sorted(read_csv(LOCAL_CONTEXT_REVIEW), key=lambda row: parse_int(row.get("review_rank")))
    searches = read_csv(LDA_SEARCHES)
    mentions = read_csv(LDA_MENTIONS)
    searches_by_bill = grouped_by_bill(searches)
    mentions_by_bill = grouped_by_bill(mentions)
    validate_search_coverage(local_rows, searches_by_bill)

    rows: list[dict[str, str]] = []
    for local_row in local_rows:
        bill_id = local_row["bill_id"]
        bill_searches = searches_by_bill[bill_id]
        bill_mentions = mentions_by_bill.get(bill_id, [])
        lda_status = lda_disposition(bill_searches, bill_mentions)
        campaign_status, campaign_next_step = campaign_scope_status(local_row)
        exact_filings = {row.get("filing_uuid", "") for row in bill_mentions if row.get("filing_uuid")}
        exact_clients = {row.get("client_name", "") for row in bill_mentions if row.get("client_name")}
        evidence_layers = [
            "bill_finance_lobbying_local_context_review",
            "official_lda_external_current_bill_search",
            "fec_openfec_source_scope_triage",
        ]
        if bill_mentions:
            evidence_layers.append("official_lda_filing_text_bill_identifier")
        rows.append({
            "review_rank": local_row.get("review_rank", ""),
            "bill_id": bill_id,
            "public_law_number": local_row.get("public_law_number", ""),
            "policy_area": local_row.get("policy_area", ""),
            "introduced_date": local_row.get("introduced_date", ""),
            "enacted_date": local_row.get("enacted_date", ""),
            "local_next_source_expansion": local_row.get("manual_next_source_expansion", ""),
            "lda_search_rows": str(len(bill_searches)),
            "lda_api_reported_result_count": str(sum(parse_int(row.get("api_reported_result_count")) for row in bill_searches)),
            "lda_fetched_filing_count": str(sum(parse_int(row.get("fetched_filing_count")) for row in bill_searches)),
            "lda_unfetched_api_result_count": str(sum(parse_int(row.get("unfetched_api_result_count")) for row in bill_searches)),
            "lda_exact_activity_match_rows": str(len(bill_mentions)),
            "lda_exact_activity_match_filings": str(len(exact_filings)),
            "lda_exact_activity_match_clients": str(len(exact_clients)),
            "lda_search_terms": join_values({row.get("search_term", "") for row in bill_searches}),
            "lda_search_years": join_values({row.get("filing_year", "") for row in bill_searches}),
            "lda_api_statuses": join_values({row.get("api_status", "") for row in bill_searches}),
            "lda_search_disposition": lda_status,
            "lda_source_urls": join_values({row.get("source_url", "") for row in bill_searches}),
            "campaign_external_scope_status": campaign_status,
            "campaign_external_next_step": campaign_next_step,
            "combined_external_review_status": combined_status(lda_status, campaign_status),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": MISSING_LINKS,
            "source_url": join_values({row.get("source_url", "") for row in bill_searches}),
            "claim_boundary": f"{CLAIM_BOUNDARY} {FEC_SOURCE_SCOPE_BOUNDARY}",
        })
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    exact_rows = [row for row in rows if parse_int(row["lda_exact_activity_match_rows"]) > 0]
    no_exact_rows = [
        row
        for row in rows
        if row["lda_search_disposition"] == "official_lda_external_search_no_exact_current_bill_activity_text_match"
    ]
    partial_rows = [
        row
        for row in rows
        if "partial" in row["lda_search_disposition"] or row["lda_search_disposition"].endswith("_error")
    ]
    campaign_pending_rows = [
        row for row in rows if row["campaign_external_scope_status"].startswith("fec_public_records_need")
    ]
    status_counts = Counter(row["combined_external_review_status"] for row in rows)
    lines = [
        "# Bill Finance/Lobbying External-Search Review",
        "",
        "This report reviews the 10 bill-finance/lobbying queue rows against a targeted official LDA current-bill activity-text search and records the FEC/OpenFEC source scope needed for later campaign-finance target review. It is source-search evidence, not influence or validation evidence.",
        "",
        f"- Queued public-law rows reviewed: {len(rows)}",
        f"- Rows with exact external LDA current-bill activity-text mentions: {len(exact_rows)}",
        f"- Exact external LDA activity-text mention rows: {sum(parse_int(row['lda_exact_activity_match_rows']) for row in rows)}",
        f"- Rows with complete external LDA search and no exact current-bill activity-text mention: {len(no_exact_rows)}",
        f"- Rows with partial/error LDA search status: {len(partial_rows)}",
        f"- Rows still requiring campaign-finance candidate/committee/outside-spending target-scope review: {len(campaign_pending_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY} {FEC_SOURCE_SCOPE_BOUNDARY}",
        "",
        "Combined external review statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend([
        "",
        "| Rank | Bill | Public law | LDA disposition | Exact LDA rows | Campaign scope | Combined status |",
        "| ---: | --- | --- | --- | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['lda_search_disposition']} | {row['lda_exact_activity_match_rows']} | "
            f"{row['campaign_external_scope_status']} | {row['combined_external_review_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No bill-finance/lobbying external-search review rows found.")
    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
