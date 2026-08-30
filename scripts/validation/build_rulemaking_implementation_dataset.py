#!/usr/bin/env python3
"""Build a normalized rulemaking implementation sample from Federal Register."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://www.federalregister.gov/api/v1/documents.json"
USER_AGENT = "congress-institutional-simulator-validation/0.1"
OUT_CSV = Path("data/validation/raw/rulemaking_implementation.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_implementation.metadata.md")


def api_get(params: list[tuple[str, object]], retries: int = 4) -> dict[str, object]:
    url = f"{API_BASE}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=60) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)
    raise RuntimeError("unreachable retry state")


def agency_names(row: dict[str, object]) -> str:
    agencies = row.get("agencies")
    if not isinstance(agencies, list):
        return ""
    names = [
        str(agency.get("name") or agency.get("raw_name") or "").strip()
        for agency in agencies
        if isinstance(agency, dict)
    ]
    return "; ".join(name for name in names if name)


def first_or_empty(value: object) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def cfr_summary(row: dict[str, object]) -> str:
    references = row.get("cfr_references")
    if not isinstance(references, list):
        return ""
    values: list[str] = []
    for ref in references:
        if not isinstance(ref, dict):
            continue
        title = ref.get("title")
        part = ref.get("part")
        if title and part:
            values.append(f"{title} CFR {part}")
    return "; ".join(values)


def capacity_from_effective_date(publication_date: str, effective_date: str) -> str:
    if not effective_date:
        return "0.50"
    try:
        published = date.fromisoformat(publication_date[:10])
        effective = date.fromisoformat(effective_date[:10])
    except ValueError:
        return "0.50"
    delay = max(0, (effective - published).days)
    if delay <= 30:
        return "1.00"
    if delay <= 90:
        return "0.75"
    if delay <= 180:
        return "0.50"
    return "0.25"


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    page = 1
    fields = [
        "document_number",
        "title",
        "type",
        "publication_date",
        "effective_on",
        "agencies",
        "regulation_id_numbers",
        "docket_ids",
        "cfr_references",
        "html_url",
        "pdf_url",
    ]
    while len(rows) < args.limit and page <= args.max_pages:
        params: list[tuple[str, object]] = [
            ("conditions[type][]", "RULE"),
            ("conditions[correction]", "0"),
            ("conditions[publication_date][gte]", args.start_date),
            ("conditions[publication_date][lte]", args.end_date),
            ("order", "newest"),
            ("per_page", min(100, args.limit)),
            ("page", page),
        ]
        for field in fields:
            params.append(("fields[]", field))
        payload = api_get(params)
        results = payload.get("results", [])
        if not isinstance(results, list) or not results:
            break
        for result in results:
            if not isinstance(result, dict):
                continue
            publication_date = str(result.get("publication_date") or "")
            effective_on = str(result.get("effective_on") or "")
            if not publication_date:
                continue
            rows.append({
                "law_id": str(result.get("document_number") or ""),
                "proposed_rule_date": "",
                "final_rule_date": publication_date,
                "effective_date": effective_on,
                "comment_count": "",
                "enforcement_capacity": capacity_from_effective_date(publication_date, effective_on),
                "nonenforced": "0",
                "underfunded": "0",
                "agency": agency_names(result),
                "regulation_id_number": first_or_empty(result.get("regulation_id_numbers")),
                "docket_id": first_or_empty(result.get("docket_ids")),
                "cfr_reference": cfr_summary(result),
                "title": str(result.get("title") or ""),
                "source_url": str(result.get("html_url") or result.get("pdf_url") or ""),
            })
            if len(rows) >= args.limit:
                break
        page += 1
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "law_id",
        "proposed_rule_date",
        "final_rule_date",
        "effective_date",
        "comment_count",
        "enforcement_capacity",
        "nonenforced",
        "underfunded",
        "agency",
        "regulation_id_number",
        "docket_id",
        "cfr_reference",
        "title",
        "source_url",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    effective_rows = sum(1 for row in rows if row["effective_date"])
    lines = [
        "# Rulemaking Implementation Raw Validation Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Source:",
        "",
        "- Federal Register API v1 document search endpoint.",
        "- API documentation: https://www.federalregister.gov/developers/documentation/api/v1",
        "- Query: final rules (`conditions[type][]=RULE`), non-corrections, newest first.",
        f"- Publication date range: {args.start_date} to {args.end_date}.",
        "",
        "Transformation:",
        "",
        "- `law_id` is the Federal Register document number.",
        "- `final_rule_date` is the Federal Register publication date.",
        "- `effective_date` is the API `effective_on` field when available.",
        "- `enforcement_capacity` is a coarse implementation-speed proxy derived from final-to-effective delay: 1.00 for 0-30 days, 0.75 for 31-90 days, 0.50 for 91-180 days or missing dates, and 0.25 for longer delays.",
        "- `proposed_rule_date` is blank because the document search response does not reliably link final rules to earlier proposed-rule publications.",
        "- `comment_count` is blank because the Federal Register document-search response used for this raw extract does not provide Regulations.gov comment totals; use `rulemaking_implementation_linkage.csv` for Federal Register-exposed docket and comment-count metadata.",
        "- `nonenforced` and `underfunded` are fixed at 0 because this source does not observe enforcement failure or appropriations capacity.",
        "",
        "Rows:",
        "",
        f"- Normalized rows: {len(rows)}",
        f"- Rows with effective date: {effective_rows}",
        "",
        "Claim boundary:",
        "",
        "This file supports a final-rule implementation-delay bridge from Federal Register publication to effective date. It does not validate public comments, enforcement capacity, nonenforcement, underfunding, or proposed-to-final rulemaking duration.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="2026-01-01")
    parser.add_argument("--end-date", default=date.today().isoformat())
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()

    rows = build_rows(args)
    if not rows:
        raise SystemExit("No Federal Register final-rule rows matched the requested query.")
    write_csv(rows)
    write_metadata(args, rows)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
