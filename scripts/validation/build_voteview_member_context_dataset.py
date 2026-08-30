#!/usr/bin/env python3
"""Build a cached Voteview member-metadata context for current roll-call rows."""

from __future__ import annotations

import argparse
import csv
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


USER_AGENT = "congress-institutional-simulator-validation/0.8"
VOTEVIEW_BASE = "https://voteview.com/static/data/out"
ROLLCALLS = Path("data/validation/raw/voteview_rollcalls.csv")
OUT_CSV = Path("data/validation/raw/voteview_member_context.csv")
OUT_METADATA = Path("data/validation/raw/voteview_member_context.metadata.md")

OUTPUT_FIELDS = [
    "congress",
    "chamber",
    "icpsr",
    "bioguide_id",
    "bioname",
    "party",
    "party_code",
    "state_abbrev",
    "district_code",
    "district_id",
    "nominate_dim1",
    "nokken_poole_dim1",
    "rollcall_rows",
    "unique_vote_ids",
    "linkage_status",
    "linkage_basis",
    "source_url",
    "claim_boundary",
]

PARTY_NAMES = {
    "100": "D",
    "200": "R",
    "328": "I",
}

CLAIM_BOUNDARY = (
    "Voteview member metadata context only; not roll-call-to-bill linkage, "
    "district public-opinion representation, sponsor effectiveness, public "
    "benefit, welfare, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def csv_rows(url: str) -> list[dict[str, str]]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=90) as response:
        text = response.read().decode("utf-8", errors="replace").splitlines()
    return list(csv.DictReader(text))


def voteview_member_url(congress: str) -> str:
    return f"{VOTEVIEW_BASE}/members/HS{congress}_members.csv"


def district_id(state: str, district: str) -> str:
    state = state.strip().upper()
    if not state or state == "USA":
        return ""
    try:
        district_number = int(district)
    except ValueError:
        return ""
    if district_number <= 0:
        return ""
    return f"{state}-{district_number:02d}"


def context_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("congress", "").strip(),
        row.get("chamber", "").strip(),
        row.get("icpsr", "").strip(),
    )


def build_rows(rollcall_rows: list[dict[str, str]], sleep_seconds: float) -> list[dict[str, str]]:
    vote_ids_by_key: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    rollcall_counts: Counter[tuple[str, str, str]] = Counter()
    congresses = sorted({row.get("congress", "").strip() for row in rollcall_rows if row.get("congress", "").strip()})
    for row in rollcall_rows:
        key = context_key(row)
        if not all(key):
            continue
        rollcall_counts[key] += 1
        if row.get("vote_id"):
            vote_ids_by_key[key].add(row["vote_id"])

    members_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    source_urls: dict[str, str] = {}
    for congress in congresses:
        url = voteview_member_url(congress)
        source_urls[congress] = url
        for member in csv_rows(url):
            key = (
                member.get("congress", "").strip(),
                member.get("chamber", "").strip(),
                member.get("icpsr", "").strip(),
            )
            if all(key) and key not in members_by_key:
                members_by_key[key] = member
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    rows: list[dict[str, str]] = []
    for key in sorted(rollcall_counts):
        congress, chamber, icpsr = key
        member = members_by_key.get(key, {})
        bioguide_id = member.get("bioguide_id", "").strip()
        state = member.get("state_abbrev", "").strip()
        district = member.get("district_code", "").strip()
        rows.append({
            "congress": congress,
            "chamber": chamber,
            "icpsr": icpsr,
            "bioguide_id": bioguide_id,
            "bioname": member.get("bioname", "").strip(),
            "party": PARTY_NAMES.get(member.get("party_code", "").strip(), member.get("party_code", "").strip()),
            "party_code": member.get("party_code", "").strip(),
            "state_abbrev": state,
            "district_code": district,
            "district_id": district_id(state, district),
            "nominate_dim1": member.get("nominate_dim1", "").strip(),
            "nokken_poole_dim1": member.get("nokken_poole_dim1", "").strip(),
            "rollcall_rows": str(rollcall_counts[key]),
            "unique_vote_ids": str(len(vote_ids_by_key[key])),
            "linkage_status": "voteview_member_metadata" if bioguide_id else "voteview_member_metadata_without_bioguide",
            "linkage_basis": "voteview_rollcalls.congress,chamber,icpsr -> Voteview HS member CSV congress,chamber,icpsr",
            "source_url": source_urls.get(congress, ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, rows: list[dict[str, str]], rollcall_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    source_urls = sorted({row["source_url"] for row in rows if row["source_url"]})
    source_lines = "\n".join(f"- {url}" for url in source_urls)
    linked_rollcall_rows = sum(
        int(row["rollcall_rows"])
        for row in rows
        if row["linkage_status"] == "voteview_member_metadata"
    )
    path.write_text(
        "# Voteview Member Metadata Context\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"{source_lines}\n"
        "- Voteview data page: https://voteview.com/data\n\n"
        "Transformation:\n\n"
        "- Reads the cached `voteview_rollcalls.csv` sample.\n"
        "- Downloads the matching Voteview HS member CSV for each Congress in that sample.\n"
        "- Joins roll-call member rows to Voteview member metadata by congress, chamber, and ICPSR ID.\n"
        "- Retains Bioguide ID, state, district, party, and ideal-point fields needed for later member-level linkage design.\n"
        "- Does not join roll calls to bills, public laws, sponsor histories, public-opinion rows, or legislative outcomes.\n\n"
        "Rows:\n\n"
        f"- Member-context rows: {len(rows)}.\n"
        f"- Raw roll-call member-vote rows represented: {len(rollcall_rows)}.\n"
        f"- Roll-call rows with Bioguide member metadata: {linked_rollcall_rows}.\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollcalls", type=Path, default=ROLLCALLS)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--sleep", type=float, default=0.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.rollcalls.exists():
        raise SystemExit(f"{args.rollcalls} is missing; run make build-core-raw-validation first.")
    rollcall_rows = read_csv(args.rollcalls)
    rows = build_rows(rollcall_rows, args.sleep)
    if not rows:
        raise SystemExit("No Voteview member rows matched the roll-call sample.")
    write_csv(rows, args.output)
    write_metadata(args.metadata, rows, rollcall_rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
