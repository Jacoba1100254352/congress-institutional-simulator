#!/usr/bin/env python3
"""Build district-opinion links to House-sponsored public-law bills."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.congress.gov/v3"
USER_AGENT = "congress-institutional-simulator-validation/0.7"
API_TIMEOUT_SECONDS = 20.0
DISTRICT_OPINION_CSV = Path("data/validation/raw/district_public_opinion.csv")
LAW_BILL_LINKAGE_CSV = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("data/validation/raw/district_public_opinion_linkage.csv")
OUT_METADATA = Path("data/validation/raw/district_public_opinion_linkage.metadata.md")
OUTPUT_FIELDS = [
    "district_id",
    "issue",
    "year",
    "support",
    "intensity",
    "turnout",
    "affected_group_share",
    "bill_id",
    "public_law_number",
    "congress",
    "bill_type",
    "bill_number",
    "policy_area",
    "sponsor_bioguide_id",
    "sponsor_name",
    "sponsor_party",
    "sponsor_state",
    "sponsor_district",
    "sponsor_chamber",
    "linkage_status",
    "linkage_basis",
    "source_url",
    "member_api_url",
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


def district_id(state_code: str, district: object) -> str:
    try:
        parsed = int(district)
    except (TypeError, ValueError):
        parsed = 0
    # At-large states may be encoded as 0 in congressional metadata; the CES
    # district aggregate stores them as the first district.
    parsed = max(1, parsed)
    return f"{state_code.upper()}-{parsed:02d}"


def matching_house_term(member: dict[str, object], congress: str) -> dict[str, object] | None:
    terms = member.get("terms")
    if not isinstance(terms, list):
        return None
    try:
        congress_number = int(congress)
    except ValueError:
        return None
    for term in terms:
        if not isinstance(term, dict):
            continue
        if term.get("congress") == congress_number and term.get("chamber") == "House of Representatives":
            return term
    return None


def member_detail(api_key: str, bioguide_id: str) -> dict[str, object]:
    payload = api_get(f"/member/{bioguide_id}", {"api_key": api_key, "format": "json"})
    member = payload.get("member")
    return member if isinstance(member, dict) else {}


def opinion_by_district(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_district: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_district.setdefault(row.get("district_id", ""), []).append(row)
    return by_district


def build_rows(
    api_key: str,
    opinion_rows: list[dict[str, str]],
    bill_rows: list[dict[str, str]],
    sleep_seconds: float,
    progress_every: int,
) -> list[dict[str, str]]:
    by_district = opinion_by_district(opinion_rows)
    member_cache: dict[str, dict[str, object]] = {}
    rows: list[dict[str, str]] = []
    bills_seen = 0
    for bill in bill_rows:
        if bill.get("linkage_status") != "bill_action_metadata":
            continue
        bioguide_id = bill.get("sponsor_bioguide_id", "").strip()
        if not bioguide_id:
            continue
        if bioguide_id not in member_cache:
            try:
                member_cache[bioguide_id] = member_detail(api_key, bioguide_id)
            except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
                member_cache[bioguide_id] = {}
            if sleep_seconds > 0.0:
                time.sleep(sleep_seconds)
        member = member_cache[bioguide_id]
        term = matching_house_term(member, bill.get("congress", ""))
        if term is None:
            continue
        state_code = str(term.get("stateCode") or bill.get("sponsor_state") or "")
        district = term.get("district")
        if not state_code or district is None:
            continue
        linked_district = district_id(state_code, district)
        district_rows = by_district.get(linked_district, [])
        if not district_rows:
            continue
        bills_seen += 1
        if progress_every > 0 and bills_seen % progress_every == 0:
            print(f"Linked district-opinion rows for {bills_seen} House-sponsored public-law bills", file=sys.stderr)
        for opinion in district_rows:
            rows.append({
                "district_id": linked_district,
                "issue": opinion.get("issue", ""),
                "year": opinion.get("year", ""),
                "support": opinion.get("support", ""),
                "intensity": opinion.get("intensity", ""),
                "turnout": opinion.get("turnout", ""),
                "affected_group_share": opinion.get("affected_group_share", ""),
                "bill_id": bill.get("bill_id", ""),
                "public_law_number": bill.get("public_law_number", ""),
                "congress": bill.get("congress", ""),
                "bill_type": bill.get("bill_type", ""),
                "bill_number": bill.get("bill_number", ""),
                "policy_area": bill.get("policy_area", ""),
                "sponsor_bioguide_id": bioguide_id,
                "sponsor_name": str(member.get("directOrderName") or ""),
                "sponsor_party": bill.get("sponsor_party", ""),
                "sponsor_state": state_code.upper(),
                "sponsor_district": str(district),
                "sponsor_chamber": "House of Representatives",
                "linkage_status": "sponsor_district_bill_metadata",
                "linkage_basis": "district_public_opinion.district_id -> Congress.gov member House district -> law_revision_bill_linkage.bill_id",
                "source_url": bill.get("source_url", ""),
                "member_api_url": f"{API_BASE}/member/{bioguide_id}",
            })
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    unique_bills = {row["bill_id"] for row in rows if row["bill_id"]}
    unique_districts = {row["district_id"] for row in rows if row["district_id"]}
    unique_opinion_keys = {(row["district_id"], row["issue"], row["year"]) for row in rows}
    issue_counts = Counter(row["issue"] for row in rows)
    issue_lines = "\n".join(f"- {issue}: {count}" for issue, count in sorted(issue_counts.items()))
    args.metadata.write_text(
        "# District Public Opinion Bill-Sponsor Metadata Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Cumulative CES district public-opinion aggregate from `district_public_opinion.csv`.\n"
        "- Congress.gov bill/action metadata from `law_revision_bill_linkage.csv`.\n"
        "- Congress.gov API v3 member endpoint for sponsor House district terms.\n"
        "- API documentation: https://api.congress.gov/\n\n"
        "Transformation:\n\n"
        "- Reads public-law bill metadata rows with sponsor Bioguide IDs.\n"
        "- Fetches Congress.gov member details and selects the House term matching the bill Congress.\n"
        "- Joins House-sponsored public-law bills to CES district-opinion rows by congressional district ID.\n"
        "- Retains public-opinion support, intensity, turnout, and affected-group-share fields as separate columns.\n"
        "- Does not infer issue-specific bill support, MRP estimates, affected-group harm, member vote choice, constituent contact, or causal representation.\n\n"
        "Rows:\n\n"
        f"- Linked district-opinion rows: {len(rows)}.\n"
        f"- Unique district-opinion row keys: {len(unique_opinion_keys)}.\n"
        f"- Unique House-sponsored public-law bills linked: {len(unique_bills)}.\n"
        f"- Unique sponsor districts linked: {len(unique_districts)}.\n\n"
        "Rows by issue:\n\n"
        f"{issue_lines}\n\n"
        "Claim boundary:\n\n"
        "This file links bounded CES district-opinion rows to House-sponsored public-law bill metadata by sponsor district. "
        "It provides district public-opinion context for bills but does not measure bill-topic support, issue-specific affected-group support or harm, representative responsiveness, welfare, or causal public-benefit validation.\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Optional dotenv file containing CONGRESS_API_KEY.")
    parser.add_argument("--api-key", help="Congress.gov API key. Defaults to CONGRESS_API_KEY.")
    parser.add_argument("--district-opinion-csv", type=Path, default=DISTRICT_OPINION_CSV)
    parser.add_argument("--law-bill-linkage-csv", type=Path, default=LAW_BILL_LINKAGE_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--sleep", type=float, default=0.03)
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    values = env_values(args.env_file)
    api_key = args.api_key or os.environ.get("CONGRESS_API_KEY") or values.get("CONGRESS_API_KEY")
    if not api_key:
        raise SystemExit("CONGRESS_API_KEY not found. Pass --env-file or export it in the environment.")
    if not args.district_opinion_csv.exists():
        raise SystemExit(f"{args.district_opinion_csv} is missing; run make build-district-public-opinion-raw first.")
    if not args.law_bill_linkage_csv.exists():
        raise SystemExit(f"{args.law_bill_linkage_csv} is missing; run make build-law-revision-bill-linkage-raw first.")
    rows = build_rows(
        api_key,
        read_csv(args.district_opinion_csv),
        read_csv(args.law_bill_linkage_csv),
        args.sleep,
        args.progress_every,
    )
    if not rows:
        raise SystemExit("No House-sponsored public-law bills matched district public-opinion rows.")
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
