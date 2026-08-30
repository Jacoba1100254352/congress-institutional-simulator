#!/usr/bin/env python3
"""Build a bounded campaign-finance validation sample from OpenFEC."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SCHEDULE_A = "https://api.open.fec.gov/v1/schedules/schedule_a/"
SCHEDULE_E = "https://api.open.fec.gov/v1/schedules/schedule_e/"
USER_AGENT = "congress-institutional-simulator-validation/0.1"
OUT_CSV = Path("data/validation/raw/campaign_finance.csv")
OUT_METADATA = Path("data/validation/raw/campaign_finance.metadata.md")
MAX_RETRY_AFTER_SECONDS = 120.0


def env_values(path: Path | None) -> dict[str, str]:
    values: dict[str, str] = {}
    if path is None or not path.exists():
        return values
    for line in path.read_text(errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def api_get(url: str, params: dict[str, object], retries: int = 5) -> dict[str, object]:
    request_url = f"{url}?{urlencode(params, doseq=True)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=60) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code == 429 and attempt < retries:
                retry_after = error.headers.get("Retry-After")
                sleep_seconds = float(retry_after) if retry_after else 4.0 * attempt
                if sleep_seconds > MAX_RETRY_AFTER_SECONDS:
                    raise RuntimeError(
                        f"OpenFEC rate limit exceeded; server requested retry after {sleep_seconds:.0f} seconds. "
                        "Use a personal OPENFEC_API_KEY or retry later."
                    ) from error
                time.sleep(sleep_seconds)
                continue
            if attempt == retries:
                raise
            time.sleep(2.0 * attempt)
        except (TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(2.0 * attempt)
    raise RuntimeError("unreachable retry state")


def clean_label(value: object, fallback: str = "unknown") -> str:
    text = re.sub(r"\s+", " ", str(value or "").strip())
    return text[:80] if text else fallback


def amount(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def cycle_dates(cycle: int) -> tuple[str, str]:
    start_year = cycle - 1 if cycle % 2 == 0 else cycle
    return f"{start_year}-01-01", f"{start_year + 1}-12-31"


def with_cursor(params: dict[str, object], last_indexes: object) -> dict[str, object] | None:
    if not isinstance(last_indexes, dict) or not last_indexes:
        return None
    cursor = dict(params)
    for key, value in last_indexes.items():
        if isinstance(value, bool):
            cursor[key] = str(value).lower()
        else:
            cursor[key] = value
    return cursor


def fetch_endpoint(
    *,
    url: str,
    params: dict[str, object],
    limit: int,
    max_pages: int,
    key_field: str,
) -> tuple[list[dict[str, object]], int]:
    fetched: list[dict[str, object]] = []
    seen: set[str] = set()
    current_params = dict(params)
    pages = 0
    while len(fetched) < limit and pages < max_pages:
        current_params["per_page"] = min(100, limit - len(fetched))
        payload = api_get(url, current_params)
        pages += 1
        results = payload.get("results", [])
        if not isinstance(results, list) or not results:
            break
        added = 0
        for row in results:
            if not isinstance(row, dict):
                continue
            identifier = str(row.get(key_field) or row.get("sub_id") or row.get("transaction_id") or "")
            if identifier and identifier in seen:
                continue
            if identifier:
                seen.add(identifier)
            fetched.append(row)
            added += 1
            if len(fetched) >= limit:
                break
        if added == 0 or len(fetched) >= limit:
            break
        next_params = with_cursor(params, payload.get("pagination", {}).get("last_indexes"))
        if next_params is None or next_params == current_params:
            break
        current_params = next_params
    return fetched, pages


def receipt_industry(row: dict[str, object]) -> str:
    occupation = clean_label(row.get("contributor_occupation"), "")
    employer = clean_label(row.get("contributor_employer"), "")
    category = clean_label(row.get("category_code_full"), "")
    return occupation or employer or category or "unknown"


def expenditure_category(row: dict[str, object]) -> str:
    category = clean_label(row.get("category_code_full"), "")
    purpose = clean_label(row.get("expenditure_purpose_descrip"), "")
    support = clean_label(row.get("support_oppose_indicator"), "")
    return category or purpose or support or "independent expenditure"


def build_rows(args: argparse.Namespace, api_key: str) -> tuple[list[dict[str, str]], dict[str, int]]:
    receipt_params: dict[str, object] = {
        "api_key": api_key,
        "two_year_transaction_period": args.cycle,
        "min_date": args.start_date,
        "max_date": args.end_date,
        "is_individual": "true",
        "sort": "-contribution_receipt_date",
        "sort_hide_null": "true",
        "sort_null_only": "false",
    }
    expenditure_params: dict[str, object] = {
        "api_key": api_key,
        "cycle": args.cycle,
        "min_date": args.start_date,
        "max_date": args.end_date,
        "sort": "-expenditure_date",
        "sort_hide_null": "true",
        "sort_null_only": "false",
    }
    receipts, receipt_pages = fetch_endpoint(
        url=SCHEDULE_A,
        params=receipt_params,
        limit=args.receipts_limit,
        max_pages=args.max_pages,
        key_field="sub_id",
    )
    expenditures, expenditure_pages = fetch_endpoint(
        url=SCHEDULE_E,
        params=expenditure_params,
        limit=args.independent_limit,
        max_pages=args.max_pages,
        key_field="sub_id",
    )

    rows: list[dict[str, str]] = []
    skipped_nonpositive = 0
    for row in receipts:
        row_amount = amount(row.get("contribution_receipt_amount"))
        if row_amount <= 0.0:
            skipped_nonpositive += 1
            continue
        rows.append({
            "cycle": str(args.cycle),
            "recipient": clean_label(row.get("committee_id") or row.get("recipient_committee_id")),
            "industry": receipt_industry(row),
            "amount": f"{row_amount:.2f}",
            "independent_expenditure": "0",
            "source_schedule": "A",
            "transaction_date": clean_label(row.get("contribution_receipt_date"), ""),
            "source_id": clean_label(row.get("sub_id") or row.get("transaction_id"), ""),
        })
    for row in expenditures:
        row_amount = amount(row.get("expenditure_amount"))
        if row_amount <= 0.0:
            skipped_nonpositive += 1
            continue
        rows.append({
            "cycle": str(args.cycle),
            "recipient": clean_label(row.get("candidate_id") or row.get("committee_id")),
            "industry": expenditure_category(row),
            "amount": f"{row_amount:.2f}",
            "independent_expenditure": "1",
            "source_schedule": "E",
            "transaction_date": clean_label(row.get("expenditure_date"), ""),
            "source_id": clean_label(row.get("sub_id") or row.get("transaction_id"), ""),
        })

    stats = {
        "schedule_a_rows_fetched": len(receipts),
        "schedule_e_rows_fetched": len(expenditures),
        "schedule_a_pages": receipt_pages,
        "schedule_e_pages": expenditure_pages,
        "skipped_nonpositive_amount_rows": skipped_nonpositive,
        "normalized_rows": len(rows),
        "receipt_rows": sum(1 for row in rows if row["source_schedule"] == "A"),
        "independent_expenditure_rows": sum(1 for row in rows if row["source_schedule"] == "E"),
    }
    return rows, stats


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "cycle",
        "recipient",
        "industry",
        "amount",
        "independent_expenditure",
        "source_schedule",
        "transaction_date",
        "source_id",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, stats: dict[str, int], key_source: str) -> None:
    key_note = "OpenFEC public DEMO_KEY" if key_source == "demo" else "provided API key, not recorded"
    lines = [
        "# Campaign Finance Raw Validation Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Source:",
        "",
        "- OpenFEC API Schedule A itemized receipts endpoint.",
        "- OpenFEC API Schedule E independent expenditures endpoint.",
        "- API documentation: https://api.open.fec.gov/developers/",
        f"- API key: {key_note}.",
        f"- Election cycle: {args.cycle}.",
        f"- Date filter: {args.start_date} to {args.end_date}.",
        "",
        "Transformation:",
        "",
        "- Schedule A rows are limited to non-earmarked individual receipts with positive contribution amounts.",
        "- Schedule E rows are limited to independent-expenditure records with positive expenditure amounts.",
        "- `recipient` is a committee ID for receipts and a candidate ID when available for independent expenditures.",
        "- `industry` is a bounded occupation, employer, expenditure category, or purpose label. It is not a full industry ontology.",
        "- Contributor names, contributor street addresses, and payee names are intentionally omitted from the committed raw file.",
        "- `independent_expenditure` is `1` only for Schedule E rows.",
        "",
        "Rows:",
        "",
        f"- Schedule A rows fetched: {stats['schedule_a_rows_fetched']} across {stats['schedule_a_pages']} page(s).",
        f"- Schedule E rows fetched: {stats['schedule_e_rows_fetched']} across {stats['schedule_e_pages']} page(s).",
        f"- Positive-amount rows skipped: {stats['skipped_nonpositive_amount_rows']}.",
        f"- Normalized rows: {stats['normalized_rows']}.",
        f"- Receipt rows: {stats['receipt_rows']}.",
        f"- Independent-expenditure rows: {stats['independent_expenditure_rows']}.",
        "",
        "Claim boundary:",
        "",
        "This file supports a campaign-finance concentration and outside-spending bridge only. It does not validate bill-level influence, sponsor capture, interest-group issue targeting, committee pressure, or causal effects of money on legislative outcomes.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    default_start, default_end = cycle_dates(2024)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Optional dotenv file containing OPENFEC_API_KEY.")
    parser.add_argument("--api-key", help="OpenFEC API key. Defaults to OPENFEC_API_KEY or DEMO_KEY.")
    parser.add_argument("--cycle", type=int, default=2024)
    parser.add_argument("--start-date", default=default_start)
    parser.add_argument("--end-date", default=default_end)
    parser.add_argument("--receipts-limit", type=int, default=100)
    parser.add_argument("--independent-limit", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=3)
    args = parser.parse_args()

    if args.start_date == default_start and args.end_date == default_end and args.cycle != 2024:
        args.start_date, args.end_date = cycle_dates(args.cycle)

    values = env_values(args.env_file)
    api_key = args.api_key or os.environ.get("OPENFEC_API_KEY") or values.get("OPENFEC_API_KEY") or "DEMO_KEY"
    key_source = "demo" if api_key == "DEMO_KEY" else "provided"
    rows, stats = build_rows(args, api_key)
    if not rows:
        raise SystemExit("No positive-amount OpenFEC rows matched the requested query.")
    write_csv(rows)
    write_metadata(args, stats, key_source)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
