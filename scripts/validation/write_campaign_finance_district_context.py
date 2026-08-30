#!/usr/bin/env python3
"""Write bounded campaign-finance district-context joins from cached files."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


CAMPAIGN_FINANCE = Path("data/validation/raw/campaign_finance.csv")
CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
DISTRICT_PUBLIC_OPINION = Path("data/validation/raw/district_public_opinion.csv")
DISTRICT_PUBLIC_OPINION_LINKAGE = Path("data/validation/raw/district_public_opinion_linkage.csv")
OUT_CSV = Path("reports/campaign-finance-district-context.csv")
OUT_MD = Path("reports/campaign-finance-district-context.md")

FIELDNAMES = [
    "cycle",
    "recipient",
    "recipient_type",
    "linkage_status",
    "candidate_id",
    "candidate_name",
    "candidate_office",
    "candidate_office_state",
    "candidate_office_district",
    "district_id",
    "district_context_status",
    "transaction_rows",
    "linked_transaction_rows",
    "raw_transaction_rows",
    "source_schedules",
    "total_amount",
    "outside_spending_rows",
    "outside_spending_amount",
    "district_public_opinion_context_rows",
    "district_public_opinion_issues",
    "district_public_opinion_support_mean",
    "district_public_opinion_turnout_mean",
    "affected_group_share_mean",
    "sponsor_public_law_context_rows",
    "sponsor_public_law_bill_ids",
    "sponsor_public_law_policy_areas",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded FEC recipient/candidate district-context inventory only; not "
    "candidate-to-sponsor identity resolution, bill-level influence, causal "
    "capture validation, private contributor disclosure, public-benefit evidence, "
    "or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def decimal_value(value: str) -> Decimal:
    try:
        return Decimal((value or "0").strip())
    except InvalidOperation:
        return Decimal("0")


def decimal_mean(values: list[str]) -> str:
    cleaned = [decimal_value(value) for value in values if (value or "").strip()]
    if not cleaned:
        return ""
    return format(sum(cleaned) / Decimal(len(cleaned)), ".6f")


def money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def normalized_district_id(office: str, state: str, district: str) -> str:
    if office.strip().casefold() != "house":
        return ""
    state = state.strip().upper()
    district = district.strip()
    if not state or not district or state == "US":
        return ""
    try:
        district_number = int(district)
    except ValueError:
        return ""
    if district_number <= 0:
        return ""
    return f"{state}-{district_number:02d}"


def build_rows() -> list[dict[str, str]]:
    finance_rows = read_csv(CAMPAIGN_FINANCE)
    linkage_rows = read_csv(CAMPAIGN_FINANCE_LINKAGE)
    opinion_rows = read_csv(DISTRICT_PUBLIC_OPINION)
    public_law_context_rows = read_csv(DISTRICT_PUBLIC_OPINION_LINKAGE)

    finance_by_key: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in finance_rows:
        finance_by_key[(row.get("cycle", "").strip(), row.get("recipient", "").strip())].append(row)

    opinion_by_district: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in opinion_rows:
        district_id = row.get("district_id", "").strip()
        if district_id:
            opinion_by_district[district_id].append(row)

    public_law_by_district: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in public_law_context_rows:
        district_id = row.get("district_id", "").strip()
        if district_id:
            public_law_by_district[district_id].append(row)

    rows: list[dict[str, str]] = []
    for linkage in sorted(linkage_rows, key=lambda row: (row.get("cycle", ""), row.get("recipient", ""))):
        cycle = linkage.get("cycle", "").strip()
        recipient = linkage.get("recipient", "").strip()
        transactions = finance_by_key.get((cycle, recipient), [])
        district_id = normalized_district_id(
            linkage.get("candidate_office", ""),
            linkage.get("candidate_office_state", ""),
            linkage.get("candidate_office_district", ""),
        )
        district_context = opinion_by_district.get(district_id, []) if district_id else []
        public_law_context = public_law_by_district.get(district_id, []) if district_id else []

        if district_context:
            context_status = "house_candidate_district_public_opinion_context"
        elif district_id:
            context_status = "house_candidate_without_district_public_opinion_context"
        elif linkage.get("candidate_id", "").strip():
            context_status = "candidate_metadata_without_house_district_context"
        elif linkage.get("linkage_status", "").strip() == "unmatched":
            context_status = "unmatched_recipient"
        else:
            context_status = "committee_metadata_without_house_district_context"

        total_amount = sum((decimal_value(row.get("amount", "")) for row in transactions), Decimal("0"))
        outside_rows = [
            row for row in transactions
            if decimal_value(row.get("independent_expenditure", "")) != Decimal("0")
        ]
        outside_amount = sum((decimal_value(row.get("amount", "")) for row in outside_rows), Decimal("0"))
        source_schedules = sorted({
            value
            for row in transactions
            for value in [row.get("source_schedule", "").strip()]
            if value
        } | {
            value.strip()
            for value in linkage.get("source_schedules", "").split(";")
            if value.strip()
        })

        district_issues = sorted({row.get("issue", "").strip() for row in district_context if row.get("issue", "").strip()})
        bill_ids = sorted({row.get("bill_id", "").strip() for row in public_law_context if row.get("bill_id", "").strip()})
        policy_areas = sorted({
            row.get("policy_area", "").strip()
            for row in public_law_context
            if row.get("policy_area", "").strip()
        })

        evidence_layers = []
        if linkage.get("linkage_status", "").strip() != "unmatched":
            evidence_layers.append("fec_recipient_metadata")
        if linkage.get("candidate_id", "").strip():
            evidence_layers.append("candidate_office_metadata")
        if transactions:
            evidence_layers.append("campaign_finance_transaction_aggregate")
        if district_context:
            evidence_layers.append("house_candidate_district_public_opinion_context")
        if public_law_context:
            evidence_layers.append("sponsor_district_public_law_metadata")

        missing_links = [
            "candidate_to_sitting_member_or_sponsor",
            "bill_id_or_issue_topic",
            "committee_of_jurisdiction",
            "legislative_outcome_or_public_law",
            "causal_influence_or_capture_validation",
        ]
        if not district_context:
            missing_links.append("house_district_public_opinion_context")

        rows.append({
            "cycle": cycle,
            "recipient": recipient,
            "recipient_type": linkage.get("recipient_type", ""),
            "linkage_status": linkage.get("linkage_status", ""),
            "candidate_id": linkage.get("candidate_id", ""),
            "candidate_name": linkage.get("candidate_name", ""),
            "candidate_office": linkage.get("candidate_office", ""),
            "candidate_office_state": linkage.get("candidate_office_state", ""),
            "candidate_office_district": linkage.get("candidate_office_district", ""),
            "district_id": district_id,
            "district_context_status": context_status,
            "transaction_rows": linkage.get("transaction_rows", ""),
            "linked_transaction_rows": linkage.get("linked_transaction_rows", ""),
            "raw_transaction_rows": str(len(transactions)),
            "source_schedules": "; ".join(source_schedules),
            "total_amount": money(total_amount),
            "outside_spending_rows": str(len(outside_rows)),
            "outside_spending_amount": money(outside_amount),
            "district_public_opinion_context_rows": str(len(district_context)),
            "district_public_opinion_issues": "; ".join(district_issues),
            "district_public_opinion_support_mean": decimal_mean([row.get("support", "") for row in district_context]),
            "district_public_opinion_turnout_mean": decimal_mean([row.get("turnout", "") for row in district_context]),
            "affected_group_share_mean": decimal_mean([row.get("affected_group_share", "") for row in district_context]),
            "sponsor_public_law_context_rows": str(len(public_law_context)),
            "sponsor_public_law_bill_ids": "; ".join(bill_ids),
            "sponsor_public_law_policy_areas": "; ".join(policy_areas),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "source_urls": linkage.get("source_urls", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["district_context_status"] for row in rows)
    house_context_rows = [
        row for row in rows
        if row["district_context_status"] == "house_candidate_district_public_opinion_context"
    ]
    candidate_rows = [row for row in rows if row["candidate_id"]]
    transaction_rows = sum(int(row["raw_transaction_rows"] or "0") for row in rows)
    house_transaction_rows = sum(int(row["raw_transaction_rows"] or "0") for row in house_context_rows)
    district_context_count = sum(int(row["district_public_opinion_context_rows"] or "0") for row in house_context_rows)
    sponsor_context_count = sum(int(row["sponsor_public_law_context_rows"] or "0") for row in house_context_rows)

    lines = [
        "# Campaign-Finance District Context",
        "",
        "This report derives a bounded district-context join from cached OpenFEC recipient metadata and cached district public-opinion aggregates. It is an evidence inventory, not bill-level influence validation.",
        "",
        f"- FEC recipient metadata rows inspected: {len(rows)}",
        f"- Candidate metadata rows inspected: {len(candidate_rows)}",
        f"- Campaign-finance transaction rows represented: {transaction_rows}",
        f"- House candidate-recipient rows with district public-opinion context: {len(house_context_rows)}",
        f"- Campaign-finance transaction rows with House district context: {house_transaction_rows}",
        f"- District public-opinion context rows attached: {district_context_count}",
        f"- Sponsor-district public-law metadata rows sharing those House districts: {sponsor_context_count}",
        "",
        "Claim boundary: the joined House-candidate subset adds district-level public-opinion context to public FEC recipient metadata. It does not identify a sitting sponsor, bill, committee of jurisdiction, issue topic, legislative outcome, causal influence, capture, public benefit, or model validation.",
        "",
        "Context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Recipient | Candidate | District | Transactions | Outside amount | District opinion rows | Sponsor-law rows | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in house_context_rows:
        lines.append(
            f"| `{row['recipient']}` | {row['candidate_name'] or '---'} | `{row['district_id']}` | "
            f"{row['raw_transaction_rows']} | {row['outside_spending_amount']} | "
            f"{row['district_public_opinion_context_rows']} | {row['sponsor_public_law_context_rows']} | "
            f"{row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{CAMPAIGN_FINANCE_LINKAGE} is missing or empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
