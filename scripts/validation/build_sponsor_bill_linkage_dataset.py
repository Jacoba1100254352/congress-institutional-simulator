#!/usr/bin/env python3
"""Build a bounded sponsor-to-bill metadata linkage cache."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


SPONSOR_SUCCESS = Path("data/validation/raw/sponsor_success.csv")
GOVINFO_BILLSTATUS_LINKAGE = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("data/validation/raw/sponsor_bill_linkage.csv")
OUT_METADATA = Path("data/validation/raw/sponsor_bill_linkage.metadata.md")

FIELDNAMES = [
    "sponsor_id",
    "party",
    "introduced",
    "enacted",
    "linkage_status",
    "matched_govinfo_bill_count",
    "matched_govinfo_enacted_count",
    "matched_public_law_bill_count",
    "matched_bill_ids",
    "matched_public_law_numbers",
    "matched_policy_areas",
    "matched_congresses",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded sponsor aggregate to public bill-metadata linkage only; not full Center for "
    "Effective Lawmaking data, not a complete sponsor history, not bill effectiveness, "
    "not legislative quality, not campaign-finance or lobbying influence, not public-opinion, "
    "welfare, causal-effect, or model validation evidence."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; build the prerequisite cache first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = part.strip()
        if clean and clean not in values:
            values.append(clean)
    return values


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def bill_index(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        sponsor_id = row.get("sponsor_bioguide_id", "").strip()
        bill_id = row.get("bill_id", "").strip()
        if not sponsor_id or not bill_id:
            continue
        key = (sponsor_id, bill_id)
        if key in seen:
            continue
        seen.add(key)
        indexed[sponsor_id].append(row)
    return indexed


def public_law_index(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        sponsor_id = row.get("sponsor_bioguide_id", "").strip()
        bill_id = row.get("bill_id", "").strip()
        public_law = row.get("public_law_number", "").strip()
        if not sponsor_id or not bill_id or not public_law:
            continue
        key = (sponsor_id, bill_id, public_law)
        if key in seen:
            continue
        seen.add(key)
        indexed[sponsor_id].append(row)
    return indexed


def missing_links(status: str) -> str:
    links = [
        "complete_sponsor_history",
        "licensed_cel_effectiveness_scores",
        "committee_or_issue_jurisdiction",
        "roll_call_to_sponsor_bill",
        "district_or_public_opinion_to_sponsor_action",
        "campaign_finance_or_lobbying_to_sponsor_action",
        "legislative_quality_or_welfare_outcome",
        "model_validation",
    ]
    if status == "no_bill_metadata_match":
        links.insert(0, "public_bill_metadata_match")
    return "; ".join(links)


def build_rows() -> list[dict[str, str]]:
    sponsors = read_csv(SPONSOR_SUCCESS)
    govinfo_by_sponsor = bill_index(read_csv(GOVINFO_BILLSTATUS_LINKAGE))
    public_law_by_sponsor = public_law_index(read_csv(LAW_REVISION_BILL_LINKAGE))
    output: list[dict[str, str]] = []
    for sponsor in sponsors:
        sponsor_id = sponsor.get("sponsor_id", "").strip()
        govinfo_matches = govinfo_by_sponsor.get(sponsor_id, [])
        public_law_matches = public_law_by_sponsor.get(sponsor_id, [])
        bill_ids = sorted({row.get("bill_id", "").strip() for row in govinfo_matches if row.get("bill_id", "").strip()})
        public_laws = sorted({
            row.get("public_law_number", "").strip()
            for row in public_law_matches
            if row.get("public_law_number", "").strip()
        })
        policy_areas = sorted({
            row.get("policy_area", "").strip()
            for row in govinfo_matches + public_law_matches
            if row.get("policy_area", "").strip()
        })
        congresses = sorted({
            row.get("congress", "").strip()
            for row in govinfo_matches + public_law_matches
            if row.get("congress", "").strip()
        })
        enacted_count = sum(1 for row in govinfo_matches if row.get("enacted", "").strip() == "1")
        if govinfo_matches:
            status = "sponsor_bill_metadata"
            layers = ["sponsor_aggregate", "govinfo_billstatus_sponsor_metadata"]
            if public_law_matches:
                layers.append("public_law_bill_action_metadata")
        else:
            status = "no_bill_metadata_match"
            layers = ["sponsor_aggregate"]
        output.append({
            "sponsor_id": sponsor_id,
            "party": sponsor.get("party", "").strip(),
            "introduced": sponsor.get("introduced", "").strip(),
            "enacted": sponsor.get("enacted", "").strip(),
            "linkage_status": status,
            "matched_govinfo_bill_count": str(len(bill_ids)),
            "matched_govinfo_enacted_count": str(enacted_count),
            "matched_public_law_bill_count": str(len(public_laws)),
            "matched_bill_ids": "; ".join(bill_ids),
            "matched_public_law_numbers": "; ".join(public_laws),
            "matched_policy_areas": "; ".join(policy_areas),
            "matched_congresses": "; ".join(congresses),
            "evidence_layers": "; ".join(layers),
            "missing_links": missing_links(status),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    matched = [row for row in rows if row["linkage_status"] == "sponsor_bill_metadata"]
    matched_bill_ids = {
        bill_id
        for row in matched
        for bill_id in split_values(row["matched_bill_ids"])
    }
    public_laws = {
        public_law
        for row in matched
        for public_law in split_values(row["matched_public_law_numbers"])
    }
    govinfo_bill_count = sum(as_int(row["matched_govinfo_bill_count"]) for row in matched)
    govinfo_enacted_count = sum(as_int(row["matched_govinfo_enacted_count"]) for row in matched)
    lines = [
        "# Sponsor-Bill Linkage Raw Dataset",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Inputs:",
        "",
        f"- `{SPONSOR_SUCCESS}`",
        f"- `{GOVINFO_BILLSTATUS_LINKAGE}`",
        f"- `{LAW_REVISION_BILL_LINKAGE}`",
        "",
        "Transformation:",
        "",
        "- Joins sponsor aggregate rows to bounded govinfo BILLSTATUS rows by Bioguide sponsor ID.",
        "- Adds public-law bill/action overlap when the same sponsor ID appears in the bounded public-law linkage cache.",
        "- Keeps unmatched sponsor rows in the output so the sponsor denominator remains explicit.",
        "",
        "Rows:",
        "",
        f"- Sponsor rows checked: {len(rows)}",
        f"- Sponsor rows with bill metadata matches: {len(matched)}",
        f"- Unique matched bill IDs: {len(matched_bill_ids)}",
        f"- Matched govinfo bill links attached: {govinfo_bill_count}",
        f"- Matched govinfo enacted bill links attached: {govinfo_enacted_count}",
        f"- Unique matched public laws: {len(public_laws)}",
        "",
        "Claim boundary:",
        "",
        CLAIM_BOUNDARY,
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No sponsor rows were available for linkage.")
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
