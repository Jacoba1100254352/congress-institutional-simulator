#!/usr/bin/env python3
"""Write a bounded campaign-finance candidate-to-sponsored-bill context report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


CAMPAIGN_MEMBER_CONTEXT = Path("data/validation/raw/campaign_finance_member_context.csv")
GOVINFO_BILLSTATUS = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
OUT_CSV = Path("reports/campaign-finance-sponsor-bill-context.csv")
OUT_MD = Path("reports/campaign-finance-sponsor-bill-context.md")

FIELDNAMES = [
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
    "bioguide_id",
    "bioname",
    "member_party",
    "member_state",
    "member_district",
    "district_id",
    "sponsor_bill_context_status",
    "matched_bill_count",
    "matched_bill_ids",
    "matched_congresses",
    "matched_policy_areas",
    "matched_committees",
    "matched_committee_reported_bill_count",
    "matched_floor_considered_bill_count",
    "matched_enacted_bill_count",
    "matched_enacted_bill_ids",
    "match_basis",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded public FEC candidate/member context joined by Bioguide ID to cached "
    "govinfo sponsored-bill metadata only; not evidence that contributions, "
    "spending, candidates, or committees funded, caused, influenced, targeted, "
    "or benefited any bill, committee decision, public law, implementation outcome, "
    "public benefit, causal capture, private contributor disclosure, or model validation."
)

MISSING_LINKS = "; ".join([
    "bill_specific_finance_or_lobbying_influence",
    "committee_action_influence",
    "reviewed_outside_spending_target",
    "private_contributor_disclosure",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_influence_or_capture_validation",
])


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def join_values(values: list[str]) -> str:
    return "; ".join(values)


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def unique_values(rows: list[dict[str, str]], field: str) -> list[str]:
    values: list[str] = []
    for row in rows:
        for value in split_values(row.get(field, "")):
            if value not in values:
                values.append(value)
    return values


def build_rows(
    campaign_rows: list[dict[str, str]],
    govinfo_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    bills_by_sponsor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in govinfo_rows:
        sponsor = row.get("sponsor_bioguide_id", "").strip()
        if sponsor and row.get("bill_id", "").strip():
            bills_by_sponsor[sponsor].append(row)

    output: list[dict[str, str]] = []
    for campaign_row in campaign_rows:
        if campaign_row.get("member_context_status") != "candidate_voteview_member_context":
            continue
        bioguide_id = campaign_row.get("bioguide_id", "").strip()
        sponsor_bills = bills_by_sponsor.get(bioguide_id, [])
        if not sponsor_bills:
            continue

        bill_ids = unique_values(sponsor_bills, "bill_id")
        enacted_bill_ids = [
            row.get("bill_id", "").strip()
            for row in sponsor_bills
            if row.get("enacted", "").strip() == "1" and row.get("bill_id", "").strip()
        ]
        source_urls = split_values(campaign_row.get("source_urls", ""))
        source_urls.extend(
            url
            for row in sponsor_bills
            for url in (row.get("source_url", ""), row.get("govinfo_url", ""))
            if url and url not in source_urls
        )
        output.append({
            "cycle": campaign_row.get("cycle", ""),
            "recipient": campaign_row.get("recipient", ""),
            "recipient_type": campaign_row.get("recipient_type", ""),
            "candidate_id": campaign_row.get("candidate_id", ""),
            "candidate_name": campaign_row.get("candidate_name", ""),
            "candidate_office": campaign_row.get("candidate_office", ""),
            "candidate_office_state": campaign_row.get("candidate_office_state", ""),
            "candidate_office_district": campaign_row.get("candidate_office_district", ""),
            "member_context_status": campaign_row.get("member_context_status", ""),
            "transaction_rows": campaign_row.get("transaction_rows", ""),
            "linked_transaction_rows": campaign_row.get("linked_transaction_rows", ""),
            "member_context_transaction_rows": campaign_row.get("member_context_transaction_rows", ""),
            "voteview_congress": campaign_row.get("voteview_congress", ""),
            "voteview_chamber": campaign_row.get("voteview_chamber", ""),
            "bioguide_id": bioguide_id,
            "bioname": campaign_row.get("bioname", ""),
            "member_party": campaign_row.get("member_party", ""),
            "member_state": campaign_row.get("member_state", ""),
            "member_district": campaign_row.get("member_district", ""),
            "district_id": campaign_row.get("district_id", ""),
            "sponsor_bill_context_status": "candidate_sponsored_bill_context",
            "matched_bill_count": str(len(bill_ids)),
            "matched_bill_ids": join_values(bill_ids),
            "matched_congresses": join_values(unique_values(sponsor_bills, "congress")),
            "matched_policy_areas": join_values(unique_values(sponsor_bills, "policy_area")),
            "matched_committees": join_values(unique_values(sponsor_bills, "committees")),
            "matched_committee_reported_bill_count": str(
                sum(1 for row in sponsor_bills if row.get("committee_reported", "") == "1")
            ),
            "matched_floor_considered_bill_count": str(
                sum(1 for row in sponsor_bills if row.get("floor_considered", "") == "1")
            ),
            "matched_enacted_bill_count": str(len(enacted_bill_ids)),
            "matched_enacted_bill_ids": join_values(enacted_bill_ids),
            "match_basis": "candidate_voteview_bioguide_to_govinfo_sponsor_bioguide",
            "evidence_layers": "; ".join([
                "fec_recipient_metadata",
                "fec_candidate_metadata",
                "voteview_member_context",
                "govinfo_billstatus_sponsor_metadata",
            ]),
            "missing_links": MISSING_LINKS,
            "source_urls": join_values(source_urls),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    return sorted(output, key=lambda row: (row["bioguide_id"], row["recipient"]))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], campaign_rows: list[dict[str, str]]) -> None:
    matched_member_rows = [
        row for row in campaign_rows
        if row.get("member_context_status") == "candidate_voteview_member_context"
    ]
    status_counts = Counter(row["sponsor_bill_context_status"] for row in rows)
    transaction_rows = sum(as_int(row.get("member_context_transaction_rows", "0")) for row in rows)
    unique_members = {row["bioguide_id"] for row in rows if row["bioguide_id"]}
    unique_bills = {
        bill_id
        for row in rows
        for bill_id in split_values(row.get("matched_bill_ids", ""))
    }
    unique_enacted = {
        bill_id
        for row in rows
        for bill_id in split_values(row.get("matched_enacted_bill_ids", ""))
    }
    unique_policy_areas = {
        policy_area
        for row in rows
        for policy_area in split_values(row.get("matched_policy_areas", ""))
    }

    lines = [
        "# Campaign-Finance Sponsor-Bill Context",
        "",
        "This report derives a bounded candidate-to-sponsored-bill context join from cached public FEC recipient/member context and cached govinfo BILLSTATUS sponsor metadata. It is a metadata inventory, not campaign-finance influence validation.",
        "",
        f"- FEC candidate rows with Voteview member context inspected: {len(matched_member_rows)}",
        f"- Candidate/member rows with sponsored-bill context: {len(rows)}",
        f"- Campaign-finance transaction rows with sponsored-bill context: {transaction_rows}",
        f"- Unique Bioguide members with sponsored-bill context: {len(unique_members)}",
        f"- Unique matched bill IDs: {len(unique_bills)}",
        f"- Unique enacted matched bill IDs: {len(unique_enacted)}",
        f"- Unique matched policy areas: {len(unique_policy_areas)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Sponsor-bill context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Recipient | Candidate/member | Transactions | Matched bills | Enacted bills | Policy areas | Missing links |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        policy_preview = "; ".join(split_values(row.get("matched_policy_areas", ""))[:3]) or "---"
        lines.append(
            f"| `{row['recipient']}` | {row['candidate_name']} / {row['bioname']} (`{row['bioguide_id']}`) | "
            f"{row['member_context_transaction_rows']} | {row['matched_bill_count']} | "
            f"{row['matched_enacted_bill_count']} | {policy_preview} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    campaign_rows = read_csv(CAMPAIGN_MEMBER_CONTEXT)
    govinfo_rows = read_csv(GOVINFO_BILLSTATUS)
    rows = build_rows(campaign_rows, govinfo_rows)
    if not rows:
        raise SystemExit(
            "No campaign-finance member-context rows share Bioguide IDs with govinfo sponsor metadata."
        )
    write_csv(rows)
    write_md(rows, campaign_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
