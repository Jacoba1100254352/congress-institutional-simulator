#!/usr/bin/env python3
"""Write a bounded lobbying issue-to-bill policy-context report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LOBBYING_ISSUE_LINKAGE = Path("data/validation/raw/lobbying_issue_linkage.csv")
GOVINFO_BILLSTATUS_LINKAGE = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
OUT_CSV = Path("reports/lobbying-bill-policy-context.csv")
OUT_MD = Path("reports/lobbying-bill-policy-context.md")

CLAIM_BOUNDARY = (
    "Bounded public LDA issue-label context joined to cached govinfo bill/action metadata by shared "
    "Congress.gov policy area only; not evidence that a lobbying client, registrant, or filing "
    "targeted, supported, opposed, funded, caused, influenced, or benefited any specific bill, "
    "sponsor, committee action, roll call, public law, implementation outcome, public benefit, "
    "causal capture, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def as_float(value: str) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def split_committee_codes(value: str) -> set[str]:
    codes: set[str] = set()
    for chunk in value.split(";"):
        token = chunk.strip().split(" ", maxsplit=1)[0].strip()
        if token:
            codes.add(token)
    return codes


def sort_bill(row: dict[str, str]) -> tuple[int, str, int, str]:
    return (
        as_int(row.get("congress", "")),
        row.get("bill_type", ""),
        as_int(row.get("bill_number", "")),
        row.get("bill_id", ""),
    )


def build_rows(
    lobbying_issue_rows: list[dict[str, str]],
    govinfo_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    bills_by_policy_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in govinfo_rows:
        policy_area = row.get("policy_area", "").strip()
        bill_id = row.get("bill_id", "").strip()
        if policy_area and bill_id:
            bills_by_policy_area[policy_area].append(row)

    rows: list[dict[str, str]] = []
    for issue_row in sorted(lobbying_issue_rows, key=lambda row: row.get("lobbying_issue", "")):
        issue = issue_row.get("lobbying_issue", "").strip()
        topic = issue_row.get("topic", "").strip()
        matched_bills = sorted(bills_by_policy_area.get(topic, []), key=sort_bill)
        matched_bill_ids = [row["bill_id"] for row in matched_bills]
        matched_enacted_bill_ids = [
            row["bill_id"] for row in matched_bills if row.get("enacted", "").strip() == "1"
        ]
        sponsors = {
            row.get("sponsor_bioguide_id", "").strip()
            for row in matched_bills
            if row.get("sponsor_bioguide_id", "").strip()
        }
        committee_codes = {
            code
            for row in matched_bills
            for code in split_committee_codes(row.get("committees", ""))
        }
        if issue_row.get("linkage_status") == "issue_topic_crosswalk" and matched_bills:
            status = "lobbying_issue_bill_policy_context"
            evidence_layers = (
                "senate_lda_issue_label; congress_policy_area_topic; "
                "govinfo_billstatus_policy_area_metadata; govinfo_bill_action_metadata"
            )
            missing_links = (
                "client_to_specific_bill; filing_text_bill_identifier; sponsor_or_member_target; "
                "committee_action_influence; roll_call_influence; legislative_outcome_causality; "
                "public_benefit_or_welfare_validation; causal_capture_validation; model_validation"
            )
            match_basis = "lda_issue_label_to_policy_area_to_govinfo_bill_policy_area"
        elif issue_row.get("linkage_status") == "issue_topic_crosswalk":
            status = "issue_topic_without_cached_bill_policy_context"
            evidence_layers = "senate_lda_issue_label; congress_policy_area_topic"
            missing_links = (
                "cached_bill_policy_area_context; client_to_specific_bill; filing_text_bill_identifier; "
                "sponsor_or_member_target; committee_action_influence; roll_call_influence; "
                "legislative_outcome_causality; causal_capture_validation; model_validation"
            )
            match_basis = "lda_issue_label_to_policy_area_only"
        else:
            status = "unmapped_lobbying_issue"
            evidence_layers = "senate_lda_issue_label"
            missing_links = (
                "policy_area_topic; cached_bill_policy_area_context; client_to_specific_bill; "
                "filing_text_bill_identifier; sponsor_or_member_target; committee_action_influence; "
                "roll_call_influence; legislative_outcome_causality; causal_capture_validation; "
                "model_validation"
            )
            match_basis = "no_policy_area_crosswalk"
        rows.append({
            "lobbying_issue": issue,
            "topic": topic,
            "policy_context_status": status,
            "lobbying_rows": issue_row.get("lobbying_rows", "0"),
            "unique_clients": issue_row.get("unique_clients", "0"),
            "unique_filings": issue_row.get("unique_filings", "0"),
            "total_amount": f"{as_float(issue_row.get('total_amount', '0')):.2f}",
            "matched_govinfo_bill_count": str(len(matched_bill_ids)),
            "matched_govinfo_floor_considered_count": str(
                sum(1 for row in matched_bills if row.get("floor_considered", "").strip() == "1")
            ),
            "matched_govinfo_committee_reported_count": str(
                sum(1 for row in matched_bills if row.get("committee_reported", "").strip() == "1")
            ),
            "matched_govinfo_enacted_count": str(len(matched_enacted_bill_ids)),
            "matched_sponsor_bioguide_count": str(len(sponsors)),
            "matched_committee_code_count": str(len(committee_codes)),
            "matched_bill_ids": "; ".join(matched_bill_ids),
            "matched_enacted_bill_ids": "; ".join(matched_enacted_bill_ids),
            "matched_sponsor_bioguide_ids": "; ".join(sorted(sponsors)),
            "matched_committee_codes": "; ".join(sorted(committee_codes)),
            "evidence_layers": evidence_layers,
            "missing_links": missing_links,
            "match_basis": match_basis,
            "source_url": issue_row.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["policy_context_status"] for row in rows)
    context_rows = [
        row for row in rows
        if row["policy_context_status"] == "lobbying_issue_bill_policy_context"
    ]
    represented_lobbying_rows = sum(as_int(row["lobbying_rows"]) for row in rows)
    context_lobbying_rows = sum(as_int(row["lobbying_rows"]) for row in context_rows)
    issue_bill_contexts = sum(as_int(row["matched_govinfo_bill_count"]) for row in context_rows)
    bill_ids = {
        bill_id.strip()
        for row in context_rows
        for bill_id in row["matched_bill_ids"].split(";")
        if bill_id.strip()
    }
    enacted_bill_ids = {
        bill_id.strip()
        for row in context_rows
        for bill_id in row["matched_enacted_bill_ids"].split(";")
        if bill_id.strip()
    }
    topics = {row["topic"] for row in context_rows if row["topic"]}
    lines = [
        "# Lobbying Bill Policy Context",
        "",
        "This report derives a bounded policy-area bill context join from cached Senate LDA issue labels, the documented LDA issue-to-policy-area crosswalk, and cached govinfo bill/action metadata. It is policy-area exposure context, not bill-level lobbying validation.",
        "",
        f"- LDA issue labels inspected: {len(rows)}",
        f"- LDA issue labels with cached bill policy-area context: {len(context_rows)}",
        f"- LDA activity rows represented: {represented_lobbying_rows}",
        f"- LDA activity rows with cached bill policy-area context: {context_lobbying_rows}",
        f"- Unique policy areas with bill context: {len(topics)}",
        f"- Issue-policy bill contexts: {issue_bill_contexts}",
        f"- Unique matched cached bill IDs: {len(bill_ids)}",
        f"- Unique matched enacted cached bill IDs: {len(enacted_bill_ids)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Policy-context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| LDA issue | Topic | Status | LDA rows | Matched bills | Enacted bills | Sponsors | Committees | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in sorted(
        rows,
        key=lambda item: (
            item["policy_context_status"] != "lobbying_issue_bill_policy_context",
            -as_int(item["lobbying_rows"]),
            item["lobbying_issue"],
        ),
    ):
        topic = row["topic"] or "---"
        lines.append(
            f"| {row['lobbying_issue']} | {topic} | {row['policy_context_status']} | "
            f"{row['lobbying_rows']} | {row['matched_govinfo_bill_count']} | "
            f"{row['matched_govinfo_enacted_count']} | {row['matched_sponsor_bioguide_count']} | "
            f"{row['matched_committee_code_count']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    lobbying_issue_rows = read_csv(LOBBYING_ISSUE_LINKAGE)
    govinfo_rows = read_csv(GOVINFO_BILLSTATUS_LINKAGE)
    if not lobbying_issue_rows:
        raise SystemExit(f"{LOBBYING_ISSUE_LINKAGE} is missing or empty; run make build-lobbying-issue-linkage-raw first.")
    if not govinfo_rows:
        raise SystemExit(f"{GOVINFO_BILLSTATUS_LINKAGE} is missing or empty; run make build-govinfo-billstatus-linkage-raw first.")
    rows = build_rows(lobbying_issue_rows, govinfo_rows)
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
