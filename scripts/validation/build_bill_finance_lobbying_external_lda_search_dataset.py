#!/usr/bin/env python3
"""Build a targeted official LDA search cache for queued bill-finance gaps."""

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


LOCAL_CONTEXT_REVIEW = Path("reports/bill-finance-lobbying-local-context-review.csv")
OUT_SEARCHES = Path("data/validation/raw/bill_finance_lobbying_external_lda_searches.csv")
OUT_MENTIONS = Path("data/validation/raw/bill_finance_lobbying_external_lda_mentions.csv")
OUT_METADATA = Path("data/validation/raw/bill_finance_lobbying_external_lda_searches.metadata.md")

LDA_FILINGS_API = "https://lda.gov/api/v1/filings/"
LDA_DOCS_URL = "https://lda.gov/api/redoc/v1/"
USER_AGENT = "CongressInstitutionalSimulator/validation"

CLAIM_BOUNDARY = (
    "Official LDA external current-bill search only; exact filing activity-text "
    "bill-number mentions identify disclosed lobbying activity mentioning the "
    "reviewed bill, not support, opposition, sponsor/member targeting, "
    "committee-action influence, roll-call influence, legislative-outcome "
    "causality, public benefit, welfare, causal capture, or model validation."
)

MISSING_LINKS_AFTER_EXACT_MENTION = "; ".join([
    "source_reviewed_support_or_opposition_disposition",
    "sponsor_or_member_target_beyond_activity_text_reference",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "campaign_finance_target_or_source_linkage",
    "reviewed_outside_spending_target",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

SEARCH_FIELDNAMES = [
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
]

MENTION_FIELDNAMES = [
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "introduced_date",
    "enacted_date",
    "search_term",
    "term_variant",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page-size", type=int, default=25)
    parser.add_argument("--max-pages-per-query", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=4.2, help="seconds between LDA API requests")
    parser.add_argument("--retry-sleep", type=float, default=75.0, help="fallback seconds after HTTP 429")
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--description-limit", type=int, default=1200)
    parser.add_argument("--term-variants", default="compact,dotted")
    return parser.parse_args()


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


def parse_int(value: str | int | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def normalized_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def shortened(value: str, limit: int) -> str:
    value = normalized_text(value)
    if limit <= 0 or len(value) <= limit:
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


def bill_parts(bill_id: str) -> tuple[str, str, str]:
    parts = bill_id.split("-", 2)
    if len(parts) != 3:
        raise SystemExit(f"invalid bill_id: {bill_id}")
    return parts[0], parts[1].lower(), parts[2]


def year_from(value: str) -> int | None:
    if not value or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def filing_years(row: dict[str, str]) -> list[int]:
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
    return list(range(min(years), max(years) + 1))


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


def search_terms(bill_id: str, variants: set[str]) -> list[tuple[str, str]]:
    _, bill_type, bill_number = bill_parts(bill_id)
    prefixes = bill_type_prefixes(bill_type)
    terms: list[tuple[str, str]] = []
    for variant in ("compact", "dotted"):
        prefix = prefixes.get(variant)
        if variant in variants and prefix:
            terms.append((variant, f"{prefix} {bill_number}"))
    return terms


def bill_reference_regex(bill_id: str) -> re.Pattern[str]:
    _, bill_type, bill_number = bill_parts(bill_id)
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
    body = patterns.get(bill_type, rf"{re.escape(bill_type)}\.?\s*{escaped_number}")
    return re.compile(rf"(?<![A-Z0-9]){body}(?![0-9])", re.IGNORECASE)


def matched_refs(text: str, regex: re.Pattern[str]) -> list[str]:
    refs: list[str] = []
    for match in regex.finditer(text):
        clean = normalized_text(match.group(0))
        if clean and clean not in refs:
            refs.append(clean)
    return refs


def source_url(params: dict[str, Any]) -> str:
    return f"{LDA_FILINGS_API}?{urllib.parse.urlencode(params)}"


def fetch_json(url: str, args: argparse.Namespace) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(1, args.retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exception:
            last_error = exception
            if exception.code == 429 and attempt < args.retries:
                retry_after = exception.headers.get("Retry-After")
                sleep_seconds = float(retry_after) if retry_after else args.retry_sleep
                time.sleep(sleep_seconds)
                continue
            if attempt >= args.retries:
                raise
        except urllib.error.URLError as exception:
            last_error = exception
            if attempt >= args.retries:
                raise
            time.sleep(max(args.sleep, 2.0 * attempt))
    raise RuntimeError(f"unable to fetch {url}: {last_error}")


def query_lda(
    bill: dict[str, str],
    search_term: str,
    term_variant: str,
    filing_year: int,
    regex: re.Pattern[str],
    args: argparse.Namespace,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    params = {
        "filing_year": str(filing_year),
        "filing_specific_lobbying_issues": search_term,
        "page_size": str(args.page_size),
    }
    fetched_count = 0
    exact_rows: list[dict[str, str]] = []
    api_count = 0
    pages_fetched = 0
    api_status = "ok"
    for page in range(1, args.max_pages_per_query + 1):
        page_params = {**params, "page": str(page)}
        try:
            payload = fetch_json(source_url(page_params), args)
        except urllib.error.HTTPError as exception:
            api_status = f"http_{exception.code}"
            break
        except urllib.error.URLError as exception:
            api_status = f"url_error_{type(exception.reason).__name__}"
            break
        pages_fetched += 1
        api_count = max(api_count, parse_int(payload.get("count")))
        results = payload.get("results") or []
        fetched_count += len(results)
        for filing in results:
            for activity in filing.get("lobbying_activities") or []:
                description = normalized_text(activity.get("description", ""))
                refs = matched_refs(description, regex)
                if not refs:
                    continue
                exact_rows.append({
                    "review_rank": bill.get("review_rank", ""),
                    "bill_id": bill.get("bill_id", ""),
                    "public_law_number": bill.get("public_law_number", ""),
                    "policy_area": bill.get("policy_area", ""),
                    "introduced_date": bill.get("introduced_date", ""),
                    "enacted_date": bill.get("enacted_date", ""),
                    "search_term": search_term,
                    "term_variant": term_variant,
                    "filing_year": str(filing_year),
                    "filing_period": normalized_text(filing.get("filing_period_display") or filing.get("filing_period")),
                    "filing_uuid": normalized_text(filing.get("filing_uuid")),
                    "client_name": entity_name(filing.get("client")),
                    "registrant_name": entity_name(filing.get("registrant")),
                    "filing_document_url": normalized_text(filing.get("filing_document_url")),
                    "activity_issue": normalized_text(
                        activity.get("general_issue_code_display") or activity.get("general_issue_code")
                    ),
                    "activity_description": shortened(description, args.description_limit),
                    "matched_bill_refs": "; ".join(refs),
                    "exact_current_bill_match": "1",
                    "government_entities": list_names(activity.get("government_entities")),
                    "source_url": normalized_text(filing.get("url")) or source_url(page_params),
                    "evidence_layers": "official_lda_external_search; official_lda_filing_text_bill_identifier",
                    "missing_links": MISSING_LINKS_AFTER_EXACT_MENTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                })
        if not payload.get("next"):
            break
        time.sleep(max(args.sleep, 0.0))
    if api_status == "ok" and api_count > fetched_count:
        api_status = "partial_max_pages_exhausted"
    search_row = {
        "review_rank": bill.get("review_rank", ""),
        "bill_id": bill.get("bill_id", ""),
        "public_law_number": bill.get("public_law_number", ""),
        "policy_area": bill.get("policy_area", ""),
        "introduced_date": bill.get("introduced_date", ""),
        "enacted_date": bill.get("enacted_date", ""),
        "search_term": search_term,
        "term_variant": term_variant,
        "filing_year": str(filing_year),
        "page_size": str(args.page_size),
        "pages_fetched": str(pages_fetched),
        "api_reported_result_count": str(api_count),
        "fetched_filing_count": str(fetched_count),
        "unfetched_api_result_count": str(max(api_count - fetched_count, 0)),
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
            parse_int(row["review_rank"]),
            row["bill_id"],
            row["filing_year"],
            row["filing_period"],
            row["client_name"],
            row["filing_uuid"],
        ),
    )


def write_metadata(
    bills: list[dict[str, str]],
    search_rows: list[dict[str, str]],
    mention_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    status_counts = Counter(row["api_status"] for row in search_rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    exact_bills = {row["bill_id"] for row in mention_rows}
    OUT_METADATA.write_text(
        "# Bill Finance/Lobbying External LDA Search Cache\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        f"- U.S. Senate LDA API filings endpoint: {LDA_FILINGS_API}\n"
        f"- API documentation: {LDA_DOCS_URL}\n\n"
        "Scope:\n\n"
        f"- Queued bill-finance/lobbying public-law rows searched: {len(bills)}.\n"
        f"- LDA term/year query rows: {len(search_rows)}.\n"
        f"- Deduplicated exact activity-text current-bill mention rows: {len(mention_rows)}.\n"
        f"- Queued bills with exact LDA activity-text current-bill mentions: {len(exact_bills)}.\n"
        f"- Page size: {args.page_size}.\n"
        f"- Max pages per query: {args.max_pages_per_query}.\n"
        f"- Term variants: {args.term_variants}.\n"
        f"- Sleep seconds between API requests: {args.sleep}.\n\n"
        "API status counts:\n\n"
        f"{status_lines}\n\n"
        f"Claim boundary: {CLAIM_BOUNDARY}\n",
    )


def main() -> int:
    args = parse_args()
    variants = {part.strip() for part in args.term_variants.split(",") if part.strip()}
    bills = sorted(read_csv(LOCAL_CONTEXT_REVIEW), key=lambda row: parse_int(row.get("review_rank")))
    if not bills:
        raise SystemExit(f"{LOCAL_CONTEXT_REVIEW} has no rows.")
    search_rows: list[dict[str, str]] = []
    mention_rows: list[dict[str, str]] = []
    for bill in bills:
        regex = bill_reference_regex(bill["bill_id"])
        years = filing_years(bill)
        terms = search_terms(bill["bill_id"], variants)
        if not years or not terms:
            raise SystemExit(f"{bill['bill_id']}: missing years or search terms")
        for filing_year in years:
            for term_variant, search_term in terms:
                search_row, exact_rows = query_lda(bill, search_term, term_variant, filing_year, regex, args)
                search_rows.append(search_row)
                mention_rows.extend(exact_rows)
                time.sleep(max(args.sleep, 0.0))
    mention_rows = dedupe_mentions(mention_rows)
    write_csv(OUT_SEARCHES, search_rows, SEARCH_FIELDNAMES)
    write_csv(OUT_MENTIONS, mention_rows, MENTION_FIELDNAMES)
    write_metadata(bills, search_rows, mention_rows, args)
    print(f"Wrote {OUT_SEARCHES}")
    print(f"Wrote {OUT_MENTIONS}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
