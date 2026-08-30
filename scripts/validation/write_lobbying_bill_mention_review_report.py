#!/usr/bin/env python3
"""Write an offline review report for exact LDA bill mentions."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
BILL_FINANCE_LOBBYING_QUEUE = Path("reports/bill-finance-lobbying-review-queue.csv")
RAW_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
RAW_SEARCHES = Path("data/validation/raw/lobbying_bill_mention_searches.csv")
OUT_CSV = Path("reports/lobbying-bill-mention-review.csv")
OUT_MD = Path("reports/lobbying-bill-mention-review.md")

LDA_SOURCE_URL = "https://lda.gov/api/v1/filings/"

CLAIM_BOUNDARY = (
    "Official LDA filing-text bill-reference review only; exact bill-number mentions "
    "in filing activity text identify disclosed lobbying activity mentioning a specific "
    "bill, not support, opposition, sponsor/member targeting, committee-action influence, "
    "roll-call influence, legislative-outcome causality, public benefit, welfare, causal "
    "capture, or model validation."
)

FIELDNAMES = [
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
]

MISSING_LINKS_WITH_EXACT_LDA = "; ".join([
    "reviewed_outside_spending_target",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

MISSING_LINKS_WITHOUT_EXACT_LDA = "; ".join([
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

MISSING_LINKS_NOT_SEARCHED = "; ".join([
    "official_lda_filing_text_search",
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
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: str) -> int:
    try:
        return int(value or "0")
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
    result: list[str] = []
    for value in values:
        clean = " ".join((value or "").split())
        if clean and clean not in result:
            result.append(clean)
    return "; ".join(result)


def finance_queue_rank_by_bill() -> dict[str, str]:
    return {
        row.get("bill_id", "").strip(): row.get("review_rank", "").strip()
        for row in read_csv(BILL_FINANCE_LOBBYING_QUEUE)
        if row.get("bill_id", "").strip()
    }


def searched_status(searches: list[dict[str, str]], mentions: list[dict[str, str]]) -> str:
    if mentions:
        return "exact_lda_filing_text_bill_mention_found"
    if searches:
        return "searched_no_exact_lda_filing_text_bill_mention"
    return "not_searched_in_current_lda_bill_mention_cache"


def evidence_layers(status: str) -> str:
    if status == "exact_lda_filing_text_bill_mention_found":
        return "official_lda_api_search; official_lda_filing_text_bill_identifier"
    if status == "searched_no_exact_lda_filing_text_bill_mention":
        return "official_lda_api_search; no_exact_lda_filing_text_bill_identifier_found"
    return "not_searched_by_current_cache"


def missing_links(status: str) -> str:
    if status == "exact_lda_filing_text_bill_mention_found":
        return MISSING_LINKS_WITH_EXACT_LDA
    if status == "searched_no_exact_lda_filing_text_bill_mention":
        return MISSING_LINKS_WITHOUT_EXACT_LDA
    return MISSING_LINKS_NOT_SEARCHED


def build_rows() -> list[dict[str, str]]:
    law_rows = [
        row for row in read_csv(LAW_REVISION_BILL_LINKAGE)
        if row.get("bill_id", "").strip() and row.get("public_law_number", "").strip()
    ]
    if not law_rows:
        raise SystemExit(f"{LAW_REVISION_BILL_LINKAGE} is missing or empty.")
    searches_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(RAW_SEARCHES):
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            searches_by_bill[bill_id].append(row)
    mentions_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(RAW_MENTIONS):
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            mentions_by_bill[bill_id].append(row)

    queue_rank = finance_queue_rank_by_bill()
    output: list[dict[str, str]] = []
    for law in law_rows:
        bill_id = law.get("bill_id", "").strip()
        searches = searches_by_bill.get(bill_id, [])
        mentions = mentions_by_bill.get(bill_id, [])
        status = searched_status(searches, mentions)
        output.append({
            "review_rank": "0",
            "bill_id": bill_id,
            "public_law_number": law.get("public_law_number", ""),
            "policy_area": law.get("policy_area", ""),
            "introduced_date": law.get("introduced_date", ""),
            "enacted_date": law.get("enacted_date", ""),
            "finance_lobbying_review_queue_rank": queue_rank.get(bill_id, ""),
            "searched_status": status,
            "search_query_count": str(len(searches)),
            "api_reported_result_count": str(sum(as_int(row.get("api_reported_result_count", "")) for row in searches)),
            "fetched_filing_count": str(sum(as_int(row.get("fetched_filing_count", "")) for row in searches)),
            "exact_lda_bill_mention_rows": str(len(mentions)),
            "unique_filing_uuids": unique_join([row.get("filing_uuid", "") for row in mentions]),
            "unique_clients": unique_join([row.get("client_name", "") for row in mentions]),
            "unique_registrants": unique_join([row.get("registrant_name", "") for row in mentions]),
            "activity_issues": unique_join([row.get("activity_issue", "") for row in mentions]),
            "filing_years": unique_join([row.get("filing_year", "") for row in searches + mentions]),
            "filing_periods": unique_join([row.get("filing_period", "") for row in mentions]),
            "filing_document_urls": unique_join([row.get("filing_document_url", "") for row in mentions]),
            "matched_bill_refs": unique_join([
                value
                for row in mentions
                for value in split_values(row.get("matched_bill_refs", ""))
            ]),
            "evidence_layers": evidence_layers(status),
            "missing_links": missing_links(status),
            "source_url": LDA_SOURCE_URL,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    output.sort(
        key=lambda row: (
            0 if row["searched_status"] == "exact_lda_filing_text_bill_mention_found" else 1,
            as_int(row["finance_lobbying_review_queue_rank"] or "999999"),
            as_int(row["public_law_number"].split("-")[-1] if "-" in row["public_law_number"] else "999999"),
            row["bill_id"],
        )
    )
    for index, row in enumerate(output, start=1):
        row["review_rank"] = str(index)
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["searched_status"] for row in rows)
    queue_rows = sum(1 for row in rows if row["finance_lobbying_review_queue_rank"])
    exact_rows = sum(as_int(row["exact_lda_bill_mention_rows"]) for row in rows)
    exact_bills = sum(
        1 for row in rows
        if row["searched_status"] == "exact_lda_filing_text_bill_mention_found"
    )
    searched_bills = sum(
        1 for row in rows
        if row["searched_status"] != "not_searched_in_current_lda_bill_mention_cache"
    )
    lines = [
        "# LDA Bill Mention Review",
        "",
        "This report summarizes cached official LDA filing activity-text searches for exact current-bill identifiers. It is source-review evidence for bill mentions only, not influence or validation evidence.",
        "",
        f"- Public-law rows reviewed: {len(rows)}",
        f"- Rows currently in finance/lobbying review queue: {queue_rows}",
        f"- Public-law rows searched in cached LDA bill-mention scan: {searched_bills}",
        f"- Public-law rows with exact LDA filing-text current-bill mentions: {exact_bills}",
        f"- Exact LDA filing activity rows with current-bill mentions: {exact_rows}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Review statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Rank | Bill | Public law | Queue rank | Status | Queries | Fetched filings | Exact rows | Clients | Matched refs |",
        "| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['finance_lobbying_review_queue_rank'] or '---'} | "
            f"{row['searched_status']} | {row['search_query_count']} | "
            f"{row['fetched_filing_count']} | {row['exact_lda_bill_mention_rows']} | "
            f"{row['unique_clients'] or '---'} | {row['matched_bill_refs'] or '---'} |"
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
