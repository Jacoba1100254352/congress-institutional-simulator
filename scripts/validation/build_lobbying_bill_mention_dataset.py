#!/usr/bin/env python3
"""Build a cached official LDA filing-text bill-mention dataset."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
BILL_FINANCE_LOBBYING_QUEUE = Path("reports/bill-finance-lobbying-review-queue.csv")
OUT_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
OUT_SEARCHES = Path("data/validation/raw/lobbying_bill_mention_searches.csv")
OUT_METADATA = Path("data/validation/raw/lobbying_bill_mentions.metadata.md")

LDA_FILINGS_API = "https://lda.gov/api/v1/filings/"
LDA_DOCS_URL = "https://lda.gov/api/redoc/v1/"

CLAIM_BOUNDARY = (
    "Official LDA filing-text bill-reference search only; exact bill-number mentions "
    "in filing activity text identify disclosed lobbying activity mentioning a specific "
    "bill, not support, opposition, sponsor/member targeting, committee-action influence, "
    "roll-call influence, legislative-outcome causality, public benefit, welfare, causal "
    "capture, or model validation."
)

MENTION_FIELDNAMES = [
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
]

SEARCH_FIELDNAMES = [
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
]

MISSING_LINKS_AFTER_EXACT_MENTION = "; ".join([
    "reviewed_outside_spending_target",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Search official LDA filing activity text for exact bill-number mentions "
            "for cached public-law rows."
        )
    )
    parser.add_argument("--candidate-limit", type=int, default=0, help="maximum public-law rows to search; 0 means all")
    parser.add_argument("--page-size", type=int, default=25, help="LDA API page size")
    parser.add_argument("--max-pages-per-query", type=int, default=1, help="maximum pages to fetch for each term/year query")
    parser.add_argument("--sleep", type=float, default=4.2, help="seconds to sleep between API requests")
    parser.add_argument("--year-pad", type=int, default=0, help="extra years before introduction and after enactment")
    parser.add_argument(
        "--description-limit",
        type=int,
        default=900,
        help="maximum stored activity-description characters; 0 means store the full API text",
    )
    parser.add_argument(
        "--term-variants",
        default="compact",
        help="comma-separated bill-number query variants: compact,dotted",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def year_from(value: str) -> int | None:
    if not value or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def candidate_sort_key(row: dict[str, str], queue_rank_by_bill: dict[str, int]) -> tuple[int, int, str]:
    bill_id = row.get("bill_id", "").strip()
    queue_rank = queue_rank_by_bill.get(bill_id, 999999)
    public_law = row.get("public_law_number", "").strip()
    return (queue_rank, as_int(public_law.split("-")[-1] if "-" in public_law else "999999"), bill_id)


def public_law_candidates(limit: int) -> list[dict[str, str]]:
    law_rows = [
        row for row in read_csv(LAW_REVISION_BILL_LINKAGE)
        if row.get("bill_id", "").strip() and row.get("public_law_number", "").strip()
    ]
    if not law_rows:
        raise SystemExit(f"{LAW_REVISION_BILL_LINKAGE} is missing or empty.")
    queue_rank_by_bill = {
        row.get("bill_id", "").strip(): as_int(row.get("review_rank", "0"))
        for row in read_csv(BILL_FINANCE_LOBBYING_QUEUE)
        if row.get("bill_id", "").strip()
    }
    law_rows.sort(key=lambda row: candidate_sort_key(row, queue_rank_by_bill))
    return law_rows[:limit] if limit > 0 else law_rows


def years_for(row: dict[str, str], pad: int) -> list[int]:
    years = [
        year
        for year in (
            year_from(row.get("introduced_date", "")),
            year_from(row.get("enacted_date", "")),
        )
        if year is not None
    ]
    if not years:
        return []
    start = min(years) - max(pad, 0)
    end = max(years) + max(pad, 0)
    return list(range(start, end + 1))


def bill_type_prefixes(bill_type: str) -> dict[str, str]:
    mapping = {
        "hr": {"compact": "HR", "dotted": "H.R."},
        "s": {"compact": "S", "dotted": "S."},
        "hres": {"compact": "HRES", "dotted": "H.Res."},
        "sres": {"compact": "SRES", "dotted": "S.Res."},
        "hjres": {"compact": "HJRES", "dotted": "H.J.Res."},
        "sjres": {"compact": "SJRES", "dotted": "S.J.Res."},
        "hconres": {"compact": "HCONRES", "dotted": "H.Con.Res."},
        "sconres": {"compact": "SCONRES", "dotted": "S.Con.Res."},
    }
    return mapping.get(bill_type.lower(), {})


def search_terms(row: dict[str, str], variants: set[str]) -> list[str]:
    bill_type = row.get("bill_type", "").strip().lower()
    bill_number = row.get("bill_number", "").strip()
    prefixes = bill_type_prefixes(bill_type)
    terms: list[str] = []
    for variant in ("compact", "dotted"):
        if variant in variants and prefixes.get(variant) and bill_number:
            terms.append(f"{prefixes[variant]} {bill_number}")
    return terms


def bill_reference_regex(bill_type: str, bill_number: str) -> re.Pattern[str]:
    escaped_number = re.escape(bill_number)
    patterns = {
        "hr": rf"(?:H\.?\s*R\.?|HR)\s*{escaped_number}",
        "s": rf"S\.?\s*{escaped_number}",
        "hres": rf"(?:H\.?\s*Res\.?|HRES)\s*{escaped_number}",
        "sres": rf"(?:S\.?\s*Res\.?|SRES)\s*{escaped_number}",
        "hjres": rf"(?:H\.?\s*J\.?\s*Res\.?|HJRES)\s*{escaped_number}",
        "sjres": rf"(?:S\.?\s*J\.?\s*Res\.?|SJRES)\s*{escaped_number}",
        "hconres": rf"(?:H\.?\s*Con\.?\s*Res\.?|HCONRES)\s*{escaped_number}",
        "sconres": rf"(?:S\.?\s*Con\.?\s*Res\.?|SCONRES)\s*{escaped_number}",
    }
    body = patterns.get(bill_type.lower(), rf"{re.escape(bill_type)}\.?\s*{escaped_number}")
    return re.compile(rf"(?<![A-Z0-9]){body}(?![0-9])", re.IGNORECASE)


def normalized_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def shortened(value: str, limit: int = 900) -> str:
    value = normalized_text(value)
    if limit <= 0:
        return value
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def entity_name(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("name", "client_name", "registrant_name"):
            if value.get(key):
                return normalized_text(value.get(key))
    return normalized_text(value)


def list_names(value: Any) -> str:
    if not value:
        return ""
    values = value if isinstance(value, list) else [value]
    names: list[str] = []
    for item in values:
        if isinstance(item, dict):
            name = item.get("name") or item.get("description") or item.get("id")
        else:
            name = item
        clean = normalized_text(name)
        if clean and clean not in names:
            names.append(clean)
    return "; ".join(names)


def source_url(params: dict[str, Any]) -> str:
    return f"{LDA_FILINGS_API}?{urllib.parse.urlencode(params)}"


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "CongressInstitutionalSimulator/validation"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def matched_refs(text: str, regex: re.Pattern[str]) -> list[str]:
    refs: list[str] = []
    for match in regex.finditer(text):
        clean = normalized_text(match.group(0))
        if clean and clean not in refs:
            refs.append(clean)
    return refs


def query_lda(
    bill: dict[str, str],
    search_term: str,
    filing_year: int,
    page_size: int,
    max_pages: int,
    regex: re.Pattern[str],
    description_limit: int,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    fetched_count = 0
    exact_rows: list[dict[str, str]] = []
    api_count = 0
    api_status = "ok"
    params = {
        "filing_year": str(filing_year),
        "filing_specific_lobbying_issues": search_term,
        "page_size": str(page_size),
    }
    for page in range(1, max_pages + 1):
        page_params = {**params, "page": str(page)}
        url = source_url(page_params)
        try:
            payload = fetch_json(url)
        except urllib.error.HTTPError as exception:
            api_status = f"http_{exception.code}"
            break
        except urllib.error.URLError as exception:
            api_status = f"url_error_{type(exception.reason).__name__}"
            break
        api_count = as_int(str(payload.get("count", "0")))
        results = payload.get("results") or []
        fetched_count += len(results)
        for filing in results:
            activities = filing.get("lobbying_activities") or []
            for activity in activities:
                description = normalized_text(activity.get("description", ""))
                refs = matched_refs(description, regex)
                if not refs:
                    continue
                exact_rows.append({
                    "bill_id": bill.get("bill_id", ""),
                    "public_law_number": bill.get("public_law_number", ""),
                    "policy_area": bill.get("policy_area", ""),
                    "introduced_date": bill.get("introduced_date", ""),
                    "enacted_date": bill.get("enacted_date", ""),
                    "search_term": search_term,
                    "filing_year": str(filing_year),
                    "filing_period": normalized_text(filing.get("filing_period_display") or filing.get("filing_period")),
                    "filing_uuid": normalized_text(filing.get("filing_uuid")),
                    "client_name": entity_name(filing.get("client")),
                    "registrant_name": entity_name(filing.get("registrant")),
                    "filing_document_url": normalized_text(filing.get("filing_document_url")),
                    "activity_issue": normalized_text(activity.get("general_issue_code_display") or activity.get("general_issue_code")),
                    "activity_description": shortened(description, description_limit),
                    "matched_bill_refs": "; ".join(refs),
                    "exact_current_bill_match": "1",
                    "government_entities": list_names(activity.get("government_entities")),
                    "source_url": normalized_text(filing.get("url")) or url,
                    "evidence_layers": "official_lda_api_search; official_lda_filing_text_bill_identifier",
                    "missing_links": MISSING_LINKS_AFTER_EXACT_MENTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                })
        if not payload.get("next"):
            break
    search_row = {
        "bill_id": bill.get("bill_id", ""),
        "public_law_number": bill.get("public_law_number", ""),
        "policy_area": bill.get("policy_area", ""),
        "introduced_date": bill.get("introduced_date", ""),
        "enacted_date": bill.get("enacted_date", ""),
        "search_term": search_term,
        "filing_year": str(filing_year),
        "page_count_requested": str(max_pages),
        "api_reported_result_count": str(api_count),
        "fetched_filing_count": str(fetched_count),
        "exact_activity_match_count": str(len(exact_rows)),
        "api_status": api_status,
        "source_url": source_url(params),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return search_row, exact_rows


def dedupe_mentions(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    unique: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for row in rows:
        description_hash = hashlib.sha256(row["activity_description"].encode()).hexdigest()[:16]
        key = (
            row["bill_id"],
            row["filing_uuid"],
            row["activity_issue"],
            row["matched_bill_refs"],
            description_hash,
        )
        if key not in unique:
            unique[key] = row
    return sorted(
        unique.values(),
        key=lambda row: (
            row["bill_id"],
            row["filing_year"],
            row["filing_period"],
            row["client_name"],
            row["filing_uuid"],
        ),
    )


def write_metadata(
    candidates: list[dict[str, str]],
    search_rows: list[dict[str, str]],
    mention_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    searched_bills = {row["bill_id"] for row in search_rows}
    exact_bills = {row["bill_id"] for row in mention_rows}
    status_counts = Counter(row["api_status"] for row in search_rows)
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    ) or "- none: 0"
    OUT_METADATA.write_text(
        "# LDA Bill Mention Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        f"Candidate public-law rows considered: {len(candidates)}\n\n"
        f"Public-law rows searched: {len(searched_bills)}\n\n"
        f"LDA term/year query rows: {len(search_rows)}\n\n"
        f"Exact filing-activity bill mention rows: {len(mention_rows)}\n\n"
        f"Public-law rows with exact LDA filing-text bill mentions: {len(exact_bills)}\n\n"
        f"API page size: {args.page_size}\n\n"
        f"Max pages per query: {args.max_pages_per_query}\n\n"
        f"Search sleep seconds: {args.sleep}\n\n"
        f"Stored activity-description limit: {args.description_limit}\n\n"
        f"Term variants: {args.term_variants}\n\n"
        f"Year pad: {args.year_pad}\n\n"
        "API status counts:\n"
        f"{status_lines}\n\n"
        f"Primary API: {LDA_FILINGS_API}\n\n"
        f"API documentation: {LDA_DOCS_URL}\n\n"
        f"Claim boundary: {CLAIM_BOUNDARY}\n",
    )


def main() -> int:
    args = parse_args()
    variants = {part.strip() for part in args.term_variants.split(",") if part.strip()}
    candidates = public_law_candidates(args.candidate_limit)
    search_rows: list[dict[str, str]] = []
    mention_rows: list[dict[str, str]] = []
    total_queries = 0
    for bill in candidates:
        regex = bill_reference_regex(bill.get("bill_type", ""), bill.get("bill_number", ""))
        years = years_for(bill, args.year_pad)
        terms = search_terms(bill, variants)
        for filing_year in years:
            for term in terms:
                total_queries += 1
                search_row, exact_rows = query_lda(
                    bill,
                    term,
                    filing_year,
                    args.page_size,
                    args.max_pages_per_query,
                    regex,
                    args.description_limit,
                )
                search_rows.append(search_row)
                mention_rows.extend(exact_rows)
                if args.sleep > 0:
                    time.sleep(args.sleep)

    mention_rows = dedupe_mentions(mention_rows)
    write_csv(OUT_SEARCHES, search_rows, SEARCH_FIELDNAMES)
    write_csv(OUT_MENTIONS, mention_rows, MENTION_FIELDNAMES)
    write_metadata(candidates, search_rows, mention_rows, args)
    print(f"Searched {len(candidates)} public-law rows with {total_queries} term/year queries")
    print(f"Wrote {OUT_SEARCHES}")
    print(f"Wrote {OUT_MENTIONS}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
