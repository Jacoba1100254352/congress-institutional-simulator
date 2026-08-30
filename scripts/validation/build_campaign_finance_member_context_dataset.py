#!/usr/bin/env python3
"""Build a bounded OpenFEC candidate-to-Voteview member context cache."""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
VOTEVIEW_MEMBER_CONTEXT = Path("data/validation/raw/voteview_member_context.csv")
OUT_CSV = Path("data/validation/raw/campaign_finance_member_context.csv")
OUT_METADATA = Path("data/validation/raw/campaign_finance_member_context.metadata.md")

OUTPUT_FIELDS = [
    "cycle",
    "recipient",
    "recipient_type",
    "candidate_id",
    "candidate_name",
    "candidate_office",
    "candidate_office_state",
    "candidate_office_district",
    "member_context_status",
    "transaction_rows",
    "linked_transaction_rows",
    "member_context_transaction_rows",
    "voteview_congress",
    "voteview_chamber",
    "icpsr",
    "bioguide_id",
    "bioname",
    "member_party",
    "member_state",
    "member_district",
    "district_id",
    "nominate_dim1",
    "nokken_poole_dim1",
    "rollcall_rows",
    "unique_vote_ids",
    "evidence_layers",
    "missing_links",
    "match_basis",
    "source_urls",
    "claim_boundary",
]

STOP_TOKENS = {
    "dr",
    "hon",
    "jr",
    "mr",
    "mrs",
    "ms",
    "sen",
    "sr",
    "ii",
    "iii",
    "iv",
}

NICKNAME_EQUIVALENTS = {
    "bob": {"robert"},
    "brad": {"bradley"},
    "chris": {"christopher"},
    "mike": {"michael"},
    "rand": {"randal"},
    "rick": {"richard"},
    "rob": {"robert"},
    "ron": {"ronald"},
    "will": {"william"},
}
for key, values in list(NICKNAME_EQUIVALENTS.items()):
    for value in values:
        NICKNAME_EQUIVALENTS.setdefault(value, set()).add(key)

CLAIM_BOUNDARY = (
    "Bounded public FEC candidate/committee recipient to Voteview member-context "
    "inventory only; not bill-level influence, sponsor effectiveness, committee "
    "jurisdiction, issue targeting, private contributor disclosure, causal capture "
    "validation, public benefit, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(value: str) -> str:
    ascii_text = (
        unicodedata.normalize("NFKD", value or "")
        .encode("ascii", "ignore")
        .decode("ascii")
        .casefold()
    )
    ascii_text = re.sub(r"\([^)]*\)", " ", ascii_text)
    ascii_text = re.sub(r"[^a-z0-9, ]", " ", ascii_text)
    return " ".join(ascii_text.split())


def name_parts(value: str) -> tuple[str, str]:
    normalized = normalize_text(value)
    if not normalized:
        return "", ""
    if "," in normalized:
        last_part, first_part = normalized.split(",", 1)
    else:
        pieces = normalized.split()
        if len(pieces) < 2:
            return normalized, ""
        first_part = pieces[0]
        last_part = pieces[-1]
    last_tokens = [token for token in last_part.split() if token not in STOP_TOKENS]
    first_tokens = [token for token in first_part.split() if token not in STOP_TOKENS]
    last = " ".join(last_tokens)
    first = first_tokens[0] if first_tokens else ""
    return last, first


def first_name_score(candidate_first: str, member_first: str) -> int:
    if not candidate_first or not member_first:
        return 0
    if candidate_first == member_first:
        return 4
    if len(candidate_first) >= 4 and member_first.startswith(candidate_first):
        return 3
    if len(member_first) >= 4 and candidate_first.startswith(member_first):
        return 3
    if member_first in NICKNAME_EQUIVALENTS.get(candidate_first, set()):
        return 2
    if candidate_first in NICKNAME_EQUIVALENTS.get(member_first, set()):
        return 2
    if candidate_first[0] == member_first[0]:
        return 1
    return 0


def district_code(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        parsed = int(value)
    except ValueError:
        return ""
    return str(parsed)


def candidate_chamber(row: dict[str, str]) -> str:
    office = (row.get("candidate_office") or "").strip().casefold()
    if office == "house":
        return "House"
    if office == "senate":
        return "Senate"
    return ""


def candidate_pool(
    candidate: dict[str, str],
    member_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    chamber = candidate_chamber(candidate)
    state = (candidate.get("candidate_office_state") or "").strip().upper()
    district = district_code(candidate.get("candidate_office_district", ""))
    if not chamber or not state or state == "US":
        return []
    pool: list[dict[str, str]] = []
    for member in member_rows:
        if member.get("chamber") != chamber:
            continue
        if (member.get("state_abbrev") or "").strip().upper() != state:
            continue
        if chamber == "House" and district_code(member.get("district_code", "")) != district:
            continue
        pool.append(member)
    return pool


def match_member(
    candidate: dict[str, str],
    member_rows: list[dict[str, str]],
) -> tuple[dict[str, str] | None, str]:
    candidate_last, candidate_first = name_parts(candidate.get("candidate_name", ""))
    if not candidate_last or not candidate_first:
        return None, "candidate_name_missing_or_unparseable"
    matches: list[tuple[int, dict[str, str]]] = []
    for member in candidate_pool(candidate, member_rows):
        member_last, member_first = name_parts(member.get("bioname", ""))
        if candidate_last != member_last:
            continue
        score = first_name_score(candidate_first, member_first)
        if score <= 0:
            continue
        matches.append((score, member))
    if not matches:
        return None, "no_name_state_district_member_match"
    matches.sort(key=lambda item: (-item[0], item[1].get("bioguide_id", "")))
    best_score = matches[0][0]
    best_matches = [member for score, member in matches if score == best_score]
    if len(best_matches) > 1:
        return None, "ambiguous_name_state_district_member_match"
    return best_matches[0], "candidate_name_state_district_voteview_member_match"


def integer_value(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def source_urls(candidate: dict[str, str], member: dict[str, str] | None) -> str:
    urls = {
        url.strip()
        for url in (candidate.get("source_urls") or "").split(";")
        if url.strip()
    }
    if member is not None and member.get("source_url"):
        urls.add(member["source_url"])
    return "; ".join(sorted(urls))


def build_rows(
    campaign_linkage_rows: list[dict[str, str]],
    member_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for candidate in sorted(campaign_linkage_rows, key=lambda row: (row.get("cycle", ""), row.get("recipient", ""))):
        member, match_basis = match_member(candidate, member_rows)
        candidate_id = candidate.get("candidate_id", "").strip()
        candidate_office = candidate.get("candidate_office", "").strip()
        if member is not None:
            status = "candidate_voteview_member_context"
        elif candidate_id and candidate_chamber(candidate):
            status = "candidate_without_voteview_member_match"
        elif candidate_id:
            status = "candidate_metadata_noncongressional_office"
        elif (candidate.get("linkage_status") or "").strip() == "unmatched":
            status = "unmatched_recipient"
        else:
            status = "recipient_without_candidate_metadata"

        linked_transactions = integer_value(
            candidate.get("linked_transaction_rows") or candidate.get("transaction_rows")
        )
        member_context_transactions = linked_transactions if member is not None else 0
        evidence_layers = []
        if (candidate.get("linkage_status") or "").strip() != "unmatched":
            evidence_layers.append("fec_recipient_metadata")
        if candidate_id:
            evidence_layers.append("fec_candidate_metadata")
        if member is not None:
            evidence_layers.append("voteview_member_context")
        missing_links = [
            "bill_id_or_issue_topic",
            "committee_of_jurisdiction",
            "outside_spending_target",
            "legislative_outcome_or_public_law",
            "causal_influence_or_capture_validation",
        ]
        if member is None:
            missing_links.insert(0, "candidate_to_voteview_member_context")

        rows.append({
            "cycle": candidate.get("cycle", ""),
            "recipient": candidate.get("recipient", ""),
            "recipient_type": candidate.get("recipient_type", ""),
            "candidate_id": candidate_id,
            "candidate_name": candidate.get("candidate_name", ""),
            "candidate_office": candidate_office,
            "candidate_office_state": candidate.get("candidate_office_state", ""),
            "candidate_office_district": candidate.get("candidate_office_district", ""),
            "member_context_status": status,
            "transaction_rows": candidate.get("transaction_rows", ""),
            "linked_transaction_rows": candidate.get("linked_transaction_rows", ""),
            "member_context_transaction_rows": str(member_context_transactions),
            "voteview_congress": member.get("congress", "") if member is not None else "",
            "voteview_chamber": member.get("chamber", "") if member is not None else "",
            "icpsr": member.get("icpsr", "") if member is not None else "",
            "bioguide_id": member.get("bioguide_id", "") if member is not None else "",
            "bioname": member.get("bioname", "") if member is not None else "",
            "member_party": member.get("party", "") if member is not None else "",
            "member_state": member.get("state_abbrev", "") if member is not None else "",
            "member_district": member.get("district_code", "") if member is not None else "",
            "district_id": member.get("district_id", "") if member is not None else "",
            "nominate_dim1": member.get("nominate_dim1", "") if member is not None else "",
            "nokken_poole_dim1": member.get("nokken_poole_dim1", "") if member is not None else "",
            "rollcall_rows": member.get("rollcall_rows", "") if member is not None else "",
            "unique_vote_ids": member.get("unique_vote_ids", "") if member is not None else "",
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "match_basis": match_basis,
            "source_urls": source_urls(candidate, member),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["member_context_status"] for row in rows)
    matched = [row for row in rows if row["member_context_status"] == "candidate_voteview_member_context"]
    matched_transactions = sum(integer_value(row["member_context_transaction_rows"]) for row in matched)
    candidate_rows = [row for row in rows if row["candidate_id"]]
    unique_members = {row["bioguide_id"] for row in matched if row["bioguide_id"]}
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    args.metadata.write_text(
        "# Campaign-Finance Member-Context Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- FEC recipient metadata cache: `{args.campaign_finance_linkage}`.\n"
        f"- Voteview member-context cache: `{args.voteview_member_context}`.\n"
        "- Voteview member source URLs are retained row-by-row from the member-context cache.\n\n"
        "Transformation:\n\n"
        "- Reads public FEC recipient/candidate metadata and Voteview member metadata.\n"
        "- For House candidates, requires matching chamber, state, district, last name, and compatible first name or initial.\n"
        "- For Senate candidates, requires matching chamber, state, last name, and compatible first name or initial.\n"
        "- Leaves challengers, presidential candidates, noncandidate committees, and ambiguous rows unmatched.\n"
        "- Does not infer identity from district alone.\n\n"
        "Rows:\n\n"
        f"- Recipient rows inspected: {len(rows)}.\n"
        f"- Candidate metadata rows inspected: {len(candidate_rows)}.\n"
        f"- Candidate rows with Voteview member context: {len(matched)}.\n"
        f"- Campaign-finance transaction rows with Voteview member context: {matched_transactions}.\n"
        f"- Unique Voteview/Bioguide members linked: {len(unique_members)}.\n\n"
        "Rows by member-context status:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign-finance-linkage", type=Path, default=CAMPAIGN_FINANCE_LINKAGE)
    parser.add_argument("--voteview-member-context", type=Path, default=VOTEVIEW_MEMBER_CONTEXT)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.campaign_finance_linkage.exists():
        raise SystemExit(
            f"{args.campaign_finance_linkage} is missing; run make build-campaign-finance-linkage-raw first."
        )
    if not args.voteview_member_context.exists():
        raise SystemExit(
            f"{args.voteview_member_context} is missing; run make build-voteview-member-context-raw first."
        )
    rows = build_rows(
        read_csv(args.campaign_finance_linkage),
        read_csv(args.voteview_member_context),
    )
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
