#!/usr/bin/env python3
"""Build Congress.gov bill-action metadata links for public-law rows."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.congress.gov/v3"
USER_AGENT = "congress-institutional-simulator-validation/0.5"
API_TIMEOUT_SECONDS = 20.0
LAW_REVISION_CSV = Path("data/validation/raw/law_revision_history.csv")
OUT_CSV = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_METADATA = Path("data/validation/raw/law_revision_bill_linkage.metadata.md")
OUTPUT_FIELDS = [
    "law_id",
    "public_law_number",
    "bill_id",
    "congress",
    "bill_type",
    "bill_number",
    "linkage_status",
    "introduced_date",
    "enacted_date",
    "policy_area",
    "sponsor_party",
    "sponsor_state",
    "sponsor_bioguide_id",
    "actions_count",
    "committee_reported",
    "floor_considered",
    "enacted",
    "source_url",
    "api_url",
]


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


def api_get(path: str, params: dict[str, object], retries: int = 3) -> dict[str, object]:
    request_url = f"{API_BASE}{path}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=API_TIMEOUT_SECONDS) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)
    raise RuntimeError("unreachable retry state")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bill_id(bill_id: str) -> tuple[int, str, str] | None:
    match = re.fullmatch(r"([0-9]+)-([a-z]+)-(.+)", bill_id.strip().lower())
    if not match:
        return None
    return int(match.group(1)), match.group(2), match.group(3)


def action_flag(actions: list[dict[str, object]], needles: tuple[str, ...]) -> bool:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            return True
    return False


def action_date(actions: list[dict[str, object]], needles: tuple[str, ...]) -> str:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            return str(action.get("actionDate") or "")
    return ""


def policy_area(detail: dict[str, object]) -> str:
    area = detail.get("policyArea")
    if isinstance(area, dict):
        return str(area.get("name") or "Unclassified")
    return "Unclassified"


def sponsor_field(detail: dict[str, object], field: str) -> str:
    sponsors = detail.get("sponsors")
    if isinstance(sponsors, list) and sponsors and isinstance(sponsors[0], dict):
        return str(sponsors[0].get(field) or "")
    return ""


def bill_source_url(congress: int, bill_type: str, bill_number: str) -> str:
    return f"https://www.congress.gov/bill/{congress}th-congress/{bill_type}-bill/{bill_number}"


def error_row(
    source: dict[str, str],
    *,
    bill_id: str,
    linkage_status: str,
    congress: int | str = "",
    bill_type: str = "",
    bill_number: str = "",
) -> dict[str, str]:
    api_url = f"{API_BASE}/bill/{congress}/{bill_type}/{bill_number}" if congress and bill_type and bill_number else ""
    return {
        "law_id": source.get("law_id", ""),
        "public_law_number": source.get("public_law_number", ""),
        "bill_id": bill_id,
        "congress": str(congress or source.get("congress", "")),
        "bill_type": bill_type,
        "bill_number": bill_number,
        "linkage_status": linkage_status,
        "introduced_date": "",
        "enacted_date": source.get("enacted_date", ""),
        "policy_area": "",
        "sponsor_party": "",
        "sponsor_state": "",
        "sponsor_bioguide_id": "",
        "actions_count": "0",
        "committee_reported": "0",
        "floor_considered": "0",
        "enacted": "0",
        "source_url": source.get("source_url", ""),
        "api_url": api_url,
    }


def build_rows(
    api_key: str,
    source_rows: list[dict[str, str]],
    sleep_seconds: float,
    progress_every: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, source in enumerate(source_rows, start=1):
        bill_id = source.get("bill_id", "")
        if not bill_id or bill_id in seen:
            continue
        seen.add(bill_id)
        if progress_every > 0 and len(seen) % progress_every == 0:
            print(f"Fetched linkage metadata for {len(seen)} public-law bill IDs", file=sys.stderr)
        parsed = parse_bill_id(bill_id)
        if parsed is None:
            rows.append(error_row(source, bill_id=bill_id, linkage_status="unmatched"))
            continue
        congress, bill_type, bill_number = parsed
        api_path = f"/bill/{congress}/{bill_type}/{bill_number}"
        try:
            detail_payload = api_get(api_path, {"api_key": api_key, "format": "json"})
            actions_payload = api_get(
                f"{api_path}/actions",
                {"api_key": api_key, "format": "json", "limit": 250},
            )
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            rows.append(error_row(
                source,
                bill_id=bill_id,
                linkage_status="api_error",
                congress=congress,
                bill_type=bill_type,
                bill_number=bill_number,
            ))
            continue
        detail = detail_payload.get("bill", {})
        if not isinstance(detail, dict):
            detail = {}
        actions = actions_payload.get("actions", [])
        if not isinstance(actions, list):
            actions = []
        committee_reported = action_flag(actions, (
            "reported by",
            "reported to",
            "ordered to be reported",
            "committee discharged",
        ))
        floor_considered = action_flag(actions, (
            "passed house",
            "passed/agreed to in house",
            "passed senate",
            "passed/agreed to in senate",
            "considered under",
            "on motion to suspend the rules and pass",
            "cloture on the motion to proceed",
            "motion to proceed",
            "agreed to",
        ))
        enacted = bool(detail.get("laws")) or action_flag(actions, ("became public law", "signed by president"))
        rows.append({
            "law_id": source.get("law_id", ""),
            "public_law_number": source.get("public_law_number", ""),
            "bill_id": bill_id,
            "congress": str(congress),
            "bill_type": bill_type,
            "bill_number": bill_number,
            "linkage_status": "bill_action_metadata" if detail else "unmatched",
            "introduced_date": str(detail.get("introducedDate") or ""),
            "enacted_date": action_date(actions, ("became public law", "signed by president")) or source.get("enacted_date", ""),
            "policy_area": policy_area(detail),
            "sponsor_party": sponsor_field(detail, "party"),
            "sponsor_state": sponsor_field(detail, "state"),
            "sponsor_bioguide_id": sponsor_field(detail, "bioguideId"),
            "actions_count": str(len(actions)),
            "committee_reported": "1" if committee_reported else "0",
            "floor_considered": "1" if floor_considered else "0",
            "enacted": "1" if enacted else "0",
            "source_url": source.get("source_url") or bill_source_url(congress, bill_type, bill_number),
            "api_url": f"{API_BASE}{api_path}",
        })
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    total = len(rows)
    linked = sum(1 for row in rows if row["linkage_status"] == "bill_action_metadata")
    status_counts = Counter(row["linkage_status"] for row in rows)
    congress_counts = Counter(row["congress"] for row in rows if row["congress"])
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    congress_lines = "\n".join(f"- {congress}: {count}" for congress, count in sorted(congress_counts.items()))
    args.metadata.write_text(
        "# Law Revision Bill Metadata Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Congress.gov API v3 bill-detail and bill-action endpoints.\n"
        "- API documentation: https://api.congress.gov/\n"
        f"- Input law-revision file: `{args.law_revision_csv}`.\n"
        f"- Row limit: {args.limit if args.limit else 'all'}.\n"
        "- API key: provided key, not recorded.\n\n"
        "Transformation:\n\n"
        "- Reads public-law rows from the cached law-revision dataset and parses `bill_id` into Congress, bill type, and bill number.\n"
        "- Fetches Congress.gov bill details and action histories for each unique public-law bill ID.\n"
        "- Retains bill/action metadata needed for linkage auditing: dates, policy area, sponsor identifiers, action count, and coarse action flags.\n"
        "- Does not fetch bill text, codified U.S. Code text, OLRC editorial notes, court-review links, implementation records, or Regulations.gov dockets.\n\n"
        "Rows:\n\n"
        f"- Unique public-law bill rows: {total}.\n"
        f"- Rows with Congress.gov bill/action metadata: {linked}.\n"
        f"- Linkage share: {(linked / total) if total else 0.0:.3f}.\n\n"
        "Rows by Congress:\n\n"
        f"{congress_lines}\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        "This file links bounded public-law revision proxy rows to official Congress.gov bill/action metadata. "
        "It does not provide codified statutory lineage, target-section diffs, observed expiration outcomes, implementation-feedback linkage, or later judicial-invalidation linkage.\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Optional dotenv file containing CONGRESS_API_KEY.")
    parser.add_argument("--api-key", help="Congress.gov API key. Defaults to CONGRESS_API_KEY.")
    parser.add_argument("--law-revision-csv", type=Path, default=LAW_REVISION_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--sleep", type=float, default=0.03)
    parser.add_argument("--limit", type=int, default=0, help="Maximum unique law-revision rows to fetch; 0 means all.")
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    values = env_values(args.env_file)
    api_key = args.api_key or os.environ.get("CONGRESS_API_KEY") or values.get("CONGRESS_API_KEY")
    if not api_key:
        raise SystemExit("CONGRESS_API_KEY not found. Pass --env-file or export it in the environment.")
    if not args.law_revision_csv.exists():
        raise SystemExit(f"{args.law_revision_csv} is missing; run make build-law-revision-raw first.")
    source_rows = read_csv(args.law_revision_csv)
    if args.limit > 0:
        source_rows = source_rows[:args.limit]
    rows = build_rows(api_key, source_rows, args.sleep, args.progress_every)
    if not rows:
        raise SystemExit("No law-revision bill IDs were available to link.")
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
