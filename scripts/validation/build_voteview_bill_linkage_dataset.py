#!/usr/bin/env python3
"""Build a bounded Voteview roll-call-to-bill metadata cache."""

from __future__ import annotations

import argparse
import csv
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


USER_AGENT = "congress-institutional-simulator-validation/0.8"
VOTEVIEW_BASE = "https://voteview.com/static/data/out"
ROLLCALLS = Path("data/validation/raw/voteview_rollcalls.csv")
BILL_PROGRESSION = Path("data/validation/raw/bill_progression.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("data/validation/raw/voteview_bill_linkage.csv")
OUT_METADATA = Path("data/validation/raw/voteview_bill_linkage.metadata.md")

OUTPUT_FIELDS = [
    "vote_id",
    "congress",
    "chamber",
    "rollnumber",
    "rollcall_date",
    "session",
    "clerk_rollnumber",
    "bill_number",
    "bill_id",
    "bill_id_basis",
    "bill_match_status",
    "member_vote_rows",
    "yea_count",
    "nay_count",
    "vote_result",
    "vote_question",
    "vote_desc",
    "dtl_desc",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Voteview roll-call bill metadata context only; bill-number parsing and "
    "bounded Congress.gov sample overlap do not establish public-opinion "
    "representation, sponsor effectiveness, public benefit, welfare, causal "
    "influence, or model validation."
)

BILL_PREFIXES = (
    ("HCONRES", "hconres"),
    ("SCONRES", "sconres"),
    ("HJRES", "hjres"),
    ("SJRES", "sjres"),
    ("HRES", "hres"),
    ("SRES", "sres"),
    ("HR", "hr"),
    ("S", "s"),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def csv_rows(url: str) -> list[dict[str, str]]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=90) as response:
        text = response.read().decode("utf-8", errors="replace").splitlines()
    return list(csv.DictReader(text))


def voteview_rollcall_url(congress: str) -> str:
    return f"{VOTEVIEW_BASE}/rollcalls/HS{congress}_rollcalls.csv"


def parse_rollnumber(vote_id: str) -> str:
    parts = vote_id.strip().split("-")
    return parts[-1] if len(parts) >= 3 else ""


def vote_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("congress", "").strip(),
        row.get("chamber", "").strip(),
        parse_rollnumber(row.get("vote_id", "")),
    )


def normalize_bill_number(raw: str, congress: str) -> tuple[str, str]:
    compact = re.sub(r"[^A-Za-z0-9]", "", raw or "").upper()
    if not compact:
        return "", "missing_bill_number"
    if compact.startswith("PN"):
        return "", "nomination_or_nonbill_vote"
    for prefix, bill_type in BILL_PREFIXES:
        if compact.startswith(prefix):
            number = compact[len(prefix):]
            if number.isdigit():
                return f"{congress}-{bill_type}-{number}", "voteview_bill_number"
            return "", "unparseable_bill_number"
    return "", "unparseable_bill_number"


def build_rows(rollcall_rows: list[dict[str, str]], sleep_seconds: float) -> list[dict[str, str]]:
    member_vote_counts = Counter(vote_key(row) for row in rollcall_rows)
    member_vote_counts.pop(("", "", ""), None)
    congresses = sorted({key[0] for key in member_vote_counts if key[0]})
    bill_progression_ids = {row.get("bill_id", "").strip() for row in read_csv(BILL_PROGRESSION)}
    law_revision_bill_ids = {row.get("bill_id", "").strip() for row in read_csv(LAW_REVISION_BILL_LINKAGE)}

    metadata_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    source_urls: dict[str, str] = {}
    for congress in congresses:
        url = voteview_rollcall_url(congress)
        source_urls[congress] = url
        for row in csv_rows(url):
            key = (
                row.get("congress", "").strip(),
                row.get("chamber", "").strip(),
                row.get("rollnumber", "").strip(),
            )
            if all(key) and key not in metadata_by_key:
                metadata_by_key[key] = row
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    rows: list[dict[str, str]] = []
    for key in sorted(member_vote_counts, key=lambda item: (int(item[0]), item[1], int(item[2]))):
        congress, chamber, rollnumber = key
        metadata = metadata_by_key.get(key, {})
        bill_id, bill_id_basis = normalize_bill_number(metadata.get("bill_number", ""), congress)
        if not metadata:
            bill_match_status = "missing_rollcall_metadata"
        elif bill_id and bill_id in bill_progression_ids:
            bill_match_status = "bill_progression_metadata"
        elif bill_id and bill_id in law_revision_bill_ids:
            bill_match_status = "law_revision_bill_metadata"
        elif bill_id:
            bill_match_status = "voteview_bill_number_only"
        else:
            bill_match_status = bill_id_basis
        rows.append({
            "vote_id": f"{congress}-{chamber}-{rollnumber}",
            "congress": congress,
            "chamber": chamber,
            "rollnumber": rollnumber,
            "rollcall_date": metadata.get("date", ""),
            "session": metadata.get("session", ""),
            "clerk_rollnumber": metadata.get("clerk_rollnumber", ""),
            "bill_number": metadata.get("bill_number", ""),
            "bill_id": bill_id,
            "bill_id_basis": bill_id_basis,
            "bill_match_status": bill_match_status,
            "member_vote_rows": str(member_vote_counts[key]),
            "yea_count": metadata.get("yea_count", ""),
            "nay_count": metadata.get("nay_count", ""),
            "vote_result": metadata.get("vote_result", ""),
            "vote_question": metadata.get("vote_question", ""),
            "vote_desc": metadata.get("vote_desc", ""),
            "dtl_desc": metadata.get("dtl_desc", ""),
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
    status_counts = Counter(row["bill_match_status"] for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    source_urls = sorted({row["source_url"] for row in rows if row["source_url"]})
    source_lines = "\n".join(f"- {url}" for url in source_urls)
    bill_rows = [row for row in rows if row["bill_id"]]
    bill_progression_rows = [row for row in rows if row["bill_match_status"] == "bill_progression_metadata"]
    bill_member_vote_rows = sum(int(row["member_vote_rows"]) for row in bill_rows)
    bill_progression_member_vote_rows = sum(int(row["member_vote_rows"]) for row in bill_progression_rows)
    path.write_text(
        "# Voteview Roll-Call Bill Linkage Context\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"{source_lines}\n"
        "- Voteview data page: https://voteview.com/data\n"
        f"- Cached roll-call rows: {ROLLCALLS}\n"
        f"- Optional Congress.gov bill sample: {BILL_PROGRESSION}\n"
        f"- Optional public-law bill metadata cache: {LAW_REVISION_BILL_LINKAGE}\n\n"
        "Transformation:\n\n"
        "- Reads the cached `voteview_rollcalls.csv` member-vote sample.\n"
        "- Downloads the matching Voteview HS roll-call metadata CSV for each Congress in that sample.\n"
        "- Joins sampled vote IDs to roll-call metadata by congress, chamber, and roll number.\n"
        "- Normalizes Voteview bill numbers into bounded `congress-bill_type-number` bill IDs when possible.\n"
        "- Flags whether normalized bill IDs overlap the cached Congress.gov bill-progression sample or public-law bill metadata cache.\n"
        "- Preserves member-vote row counts for each roll call but does not infer public support or bill outcomes.\n\n"
        "Rows:\n\n"
        f"- Voteview roll-call metadata rows represented: {len(rows)}.\n"
        f"- Raw roll-call member-vote rows represented: {len(rollcall_rows)}.\n"
        f"- Voteview roll-call metadata rows with normalized bill IDs: {len(bill_rows)}.\n"
        f"- Member-vote rows on roll calls with normalized bill IDs: {bill_member_vote_rows}.\n"
        f"- Voteview roll-call metadata rows matching cached bill progression rows: {len(bill_progression_rows)}.\n"
        f"- Member-vote rows matching cached bill progression rows: {bill_progression_member_vote_rows}.\n\n"
        "Bill match statuses:\n\n"
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
        raise SystemExit("No Voteview roll-call metadata rows matched the roll-call sample.")
    write_csv(rows, args.output)
    write_metadata(args.metadata, rows, rollcall_rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
