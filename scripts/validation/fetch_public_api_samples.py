#!/usr/bin/env python3
"""Fetch small public API validation samples.

This script is intentionally optional. It reads API keys from the current
environment or from an explicit env file, writes normalized CSVs for the
existing validation adapters, and never writes secrets to disk.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


RAW_DIR = Path("data/validation/raw")
REPORT = Path("reports/public-api-sample-fetch.md")
USER_AGENT = "congress-institutional-simulator-validation/0.1"


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


def api_get(url: str, params: dict[str, object], retries: int = 3) -> dict[str, object]:
    request_url = f"{url}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def truth_from_actions(actions: list[dict[str, object]], needles: tuple[str, ...]) -> bool:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            return True
    return False


def bill_id(bill: dict[str, object]) -> str:
    return f"{bill.get('congress')}-{str(bill.get('type', '')).lower()}-{bill.get('number')}"


def sponsor_id(detail: dict[str, object]) -> tuple[str, str]:
    sponsors = detail.get("sponsors") or []
    if not isinstance(sponsors, list) or not sponsors:
        return ("unknown", "unknown")
    sponsor = sponsors[0]
    if not isinstance(sponsor, dict):
        return ("unknown", "unknown")
    identifier = str(sponsor.get("bioguideId") or sponsor.get("fullName") or "unknown")
    party = str(sponsor.get("party") or "unknown")
    return (identifier, party)


def fetch_congress_samples(api_key: str, congress: int, limit: int, law_limit: int, sleep_seconds: float) -> dict[str, int]:
    list_payload = api_get(
        f"https://api.congress.gov/v3/bill/{congress}",
        {"api_key": api_key, "format": "json", "limit": limit, "offset": 0},
    )
    bills = list_payload.get("bills", [])
    if not isinstance(bills, list):
        bills = []
    law_payload = api_get(
        f"https://api.congress.gov/v3/law/{congress}/pub",
        {"api_key": api_key, "format": "json", "limit": law_limit, "offset": 0},
    )
    laws = law_payload.get("bills", [])
    if not isinstance(laws, list):
        laws = []
    unique_bills: dict[str, dict[str, object]] = {}
    for bill in [*bills, *laws]:
        if isinstance(bill, dict):
            unique_bills[bill_id(bill)] = bill

    bill_rows: list[dict[str, object]] = []
    topic_counts: dict[str, dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "floor_considered": 0,
        "enacted": 0,
    })
    sponsor_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {
        "introduced": 0,
        "enacted": 0,
    })

    for bill in unique_bills.values():
        if not isinstance(bill, dict):
            continue
        bill_type = str(bill.get("type", "")).lower()
        number = str(bill.get("number", ""))
        if not bill_type or not number:
            continue
        detail_payload = api_get(
            f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{number}",
            {"api_key": api_key, "format": "json"},
        )
        detail = detail_payload.get("bill", {})
        if not isinstance(detail, dict):
            detail = {}
        action_payload = api_get(
            f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{number}/actions",
            {"api_key": api_key, "format": "json", "limit": 250},
        )
        actions = action_payload.get("actions", [])
        if not isinstance(actions, list):
            actions = []

        committee_reported = truth_from_actions(actions, ("reported", "ordered to be reported"))
        floor_considered = truth_from_actions(actions, ("floor", "passed", "agreed to", "considered"))
        enacted = truth_from_actions(actions, ("became public law", "signed by president"))
        if bill.get("laws"):
            enacted = True
        policy_area = detail.get("policyArea")
        if isinstance(policy_area, dict):
            topic = str(policy_area.get("name") or "Unclassified")
        else:
            topic = "Unclassified"
        sponsor, party = sponsor_id(detail)

        row = {
            "bill_id": bill_id(bill),
            "introduced": "1",
            "committee_reported": "1" if committee_reported else "0",
            "floor_considered": "1" if floor_considered else "0",
            "enacted": "1" if enacted else "0",
        }
        bill_rows.append(row)
        topic_counts[topic]["introduced"] += 1
        topic_counts[topic]["floor_considered"] += int(floor_considered)
        topic_counts[topic]["enacted"] += int(enacted)
        sponsor_counts[(sponsor, party)]["introduced"] += 1
        sponsor_counts[(sponsor, party)]["enacted"] += int(enacted)
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    write_csv(RAW_DIR / "bill_progression.csv", ["bill_id", "introduced", "committee_reported", "floor_considered", "enacted"], bill_rows)
    write_csv(
        RAW_DIR / "topic_throughput.csv",
        ["topic", "introduced", "floor_considered", "enacted"],
        [{"topic": topic, **counts} for topic, counts in sorted(topic_counts.items())],
    )
    write_csv(
        RAW_DIR / "sponsor_success.csv",
        ["sponsor_id", "party", "introduced", "enacted"],
        [
            {"sponsor_id": sponsor, "party": party, **counts}
            for (sponsor, party), counts in sorted(sponsor_counts.items())
        ],
    )
    return {
        "bills": len(bill_rows),
        "topics": len(topic_counts),
        "sponsors": len(sponsor_counts),
    }


def coarse_industry(row: dict[str, object]) -> str:
    occupation = str(row.get("contributor_occupation") or row.get("category_code_full") or "").strip()
    employer = str(row.get("contributor_employer") or "").strip()
    value = occupation or employer or "unknown"
    value = re.sub(r"\s+", " ", value)
    return value[:80]


def fetch_fec_samples(api_key: str, cycle: int, limit: int) -> dict[str, int]:
    rows: list[dict[str, object]] = []
    schedule_a = api_get(
        "https://api.open.fec.gov/v1/schedules/schedule_a/",
        {
            "api_key": api_key,
            "per_page": limit,
            "two_year_transaction_period": cycle,
            "is_individual": "true",
            "sort_hide_null": "false",
            "sort_null_only": "false",
        },
    ).get("results", [])
    if isinstance(schedule_a, list):
        for row in schedule_a:
            if not isinstance(row, dict):
                continue
            rows.append({
                "cycle": cycle,
                "recipient": row.get("committee_id") or "unknown",
                "industry": coarse_industry(row),
                "amount": row.get("contribution_receipt_amount") or 0,
                "independent_expenditure": "0",
            })

    schedule_e = api_get(
        "https://api.open.fec.gov/v1/schedules/schedule_e/",
        {
            "api_key": api_key,
            "per_page": limit,
            "two_year_transaction_period": cycle,
            "sort_hide_null": "false",
            "sort_null_only": "false",
        },
    ).get("results", [])
    if isinstance(schedule_e, list):
        for row in schedule_e:
            if not isinstance(row, dict):
                continue
            rows.append({
                "cycle": cycle,
                "recipient": row.get("candidate_id") or row.get("committee_id") or "unknown",
                "industry": coarse_industry(row),
                "amount": row.get("expenditure_amount") or 0,
                "independent_expenditure": "1",
            })

    write_csv(RAW_DIR / "campaign_finance.csv", ["cycle", "recipient", "industry", "amount", "independent_expenditure"], rows)
    return {"campaign_finance_rows": len(rows)}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(congress_stats: dict[str, int] | None, fec_stats: dict[str, int] | None) -> None:
    lines = [
        "# Public API Validation Sample Fetch",
        "",
        "This report records the shape of locally fetched public API samples. It does not contain API keys and does not claim empirical validation.",
        "",
        "| Source | Output | Rows/groups |",
        "| --- | --- | ---: |",
    ]
    if congress_stats:
        lines.extend([
            f"| Congress.gov | `bill_progression.csv` | {congress_stats['bills']} |",
            f"| Congress.gov | `topic_throughput.csv` | {congress_stats['topics']} |",
            f"| Congress.gov | `sponsor_success.csv` | {congress_stats['sponsors']} |",
        ])
    else:
        lines.append("| Congress.gov | skipped | 0 |")
    if fec_stats:
        lines.append(f"| OpenFEC | `campaign_finance.csv` | {fec_stats['campaign_finance_rows']} |")
    else:
        lines.append("| OpenFEC | skipped | 0 |")
    lines.extend([
        "",
        "Interpretation: these files are adapter smoke-test samples for bill attrition, topic throughput, sponsor success, and campaign-finance concentration. They are too small and too lightly cleaned to validate the simulator.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Optional dotenv file containing CONGRESS_API_KEY and/or OPENFEC_API_KEY.")
    parser.add_argument("--congress", type=int, default=118)
    parser.add_argument("--bill-limit", type=int, default=80)
    parser.add_argument("--law-limit", type=int, default=25)
    parser.add_argument("--fec-cycle", type=int, default=2024)
    parser.add_argument("--fec-limit", type=int, default=100)
    parser.add_argument("--sleep", type=float, default=0.05, help="Delay between Congress.gov bill-detail requests.")
    parser.add_argument("--skip-congress", action="store_true")
    parser.add_argument("--skip-fec", action="store_true")
    args = parser.parse_args()

    values = env_values(args.env_file)
    congress_key = values.get("CONGRESS_API_KEY")
    fec_key = values.get("OPENFEC_API_KEY")

    congress_stats = None
    fec_stats = None
    if not args.skip_congress and congress_key:
        congress_stats = fetch_congress_samples(congress_key, args.congress, args.bill_limit, args.law_limit, args.sleep)
    if not args.skip_fec and fec_key:
        fec_stats = fetch_fec_samples(fec_key, args.fec_cycle, args.fec_limit)
    write_report(congress_stats, fec_stats)
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
