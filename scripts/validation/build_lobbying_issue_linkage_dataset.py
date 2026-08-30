#!/usr/bin/env python3
"""Build a bounded LDA issue-to-policy-area linkage cache."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


LOBBYING = Path("data/validation/raw/lobbying_disclosure.csv")
TOPICS = Path("data/validation/raw/topic_throughput.csv")
OUT_CSV = Path("data/validation/raw/lobbying_issue_linkage.csv")
OUT_METADATA = Path("data/validation/raw/lobbying_issue_linkage.metadata.md")

CLAIM_BOUNDARY = (
    "Bounded LDA issue-to-policy-area taxonomy bridge only; not bill-level "
    "lobbying influence, sponsor linkage, committee-of-jurisdiction evidence, "
    "causal capture validation, public benefit, welfare, or model validation."
)

ISSUE_TO_TOPIC = {
    "Aerospace": "Armed Forces and National Security",
    "Agriculture": "Agriculture and Food",
    "Automotive Industry": "Commerce",
    "Aviation/Airlines/Airports": "Transportation and Public Works",
    "Banking": "Finance and Financial Sector",
    "Beverage Industry": "Commerce",
    "Budget/Appropriations": "Economics and Public Finance",
    "Chemicals/Chemical Industry": "Commerce",
    "Clean Air and Water (quality)": "Environmental Protection",
    "Computer Industry": "Science, Technology, Communications",
    "Consumer Issues/Safety/Products": "Commerce",
    "Defense": "Armed Forces and National Security",
    "Disaster Planning/Emergencies": "Emergency Management",
    "Economics/Economic Development": "Economics and Public Finance",
    "Education": "Education",
    "Energy/Nuclear": "Energy",
    "Environment/Superfund": "Environmental Protection",
    "Financial Institutions/Investments/Securities": "Finance and Financial Sector",
    "Food Industry (safety, labeling, etc.)": "Agriculture and Food",
    "Foreign Relations": "International Affairs",
    "Fuel/Gas/Oil": "Energy",
    "Government Issues": "Government Operations and Politics",
    "Health Issues": "Health",
    "Housing": "Housing and Community Development",
    "Indian/Native American Affairs": "Native Americans",
    "Insurance": "Finance and Financial Sector",
    "Intelligence": "Armed Forces and National Security",
    "Law Enforcement/Crime/Criminal Justice": "Crime and Law Enforcement",
    "Manufacturing": "Commerce",
    "Marine/Maritime/Boating/Fisheries": "Transportation and Public Works",
    "Media (information/publishing)": "Science, Technology, Communications",
    "Medicare/Medicaid": "Health",
    "Natural Resources": "Public Lands and Natural Resources",
    "Pharmacy": "Health",
    "Railroads": "Transportation and Public Works",
    "Roads/Highway": "Transportation and Public Works",
    "Science/Technology": "Science, Technology, Communications",
    "Small Business": "Commerce",
    "Taxation/Internal Revenue Code": "Taxation",
    "Telecommunications": "Science, Technology, Communications",
    "Tobacco": "Commerce",
    "Trade (domestic/foreign)": "Commerce",
    "Transportation": "Transportation and Public Works",
    "Travel/Tourism": "Commerce",
    "Utilities": "Energy",
    "Veterans": "Armed Forces and National Security",
    "Welfare": "Social Welfare",
}

FIELDNAMES = [
    "lobbying_issue",
    "topic",
    "linkage_status",
    "lobbying_rows",
    "unique_clients",
    "unique_filings",
    "total_amount",
    "topic_introduced",
    "topic_floor_considered",
    "topic_enacted",
    "evidence_layers",
    "missing_links",
    "crosswalk_basis",
    "source_url",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run the core raw validation builder first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def decimal_value(value: str) -> Decimal:
    try:
        return Decimal((value or "0").strip())
    except InvalidOperation:
        return Decimal("0")


def money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def build_rows() -> list[dict[str, str]]:
    lobbying_rows = read_csv(LOBBYING)
    topic_rows = read_csv(TOPICS)
    topics = {row["topic"]: row for row in topic_rows if row.get("topic")}

    unknown_topics = sorted({topic for topic in ISSUE_TO_TOPIC.values() if topic not in topics})
    if unknown_topics:
        raise SystemExit(f"{TOPICS} is missing mapped topics: {unknown_topics}")

    by_issue: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lobbying_rows:
        issue = (row.get("issue") or "").strip()
        if issue:
            by_issue[issue].append(row)

    rows: list[dict[str, str]] = []
    for issue in sorted(by_issue):
        issue_rows = by_issue[issue]
        topic = ISSUE_TO_TOPIC.get(issue, "")
        topic_row = topics.get(topic, {})
        if topic:
            status = "issue_topic_crosswalk"
            evidence_layers = "senate_lda_issue_label; congress_policy_area_topic"
            missing_links = (
                "bill_id; sponsor_or_member_id; committee_of_jurisdiction; "
                "legislative_outcome; causal_capture_validation; model_validation"
            )
            basis = "manual deterministic crosswalk from Senate LDA issue label to local Congress.gov policy-area topic label"
        else:
            status = "unmatched_issue"
            evidence_layers = "senate_lda_issue_label"
            missing_links = (
                "topic_policy_area; bill_id; sponsor_or_member_id; committee_of_jurisdiction; "
                "legislative_outcome; causal_capture_validation; model_validation"
            )
            basis = "no policy-area assignment; leave unmatched rather than inferring from uncoded or ambiguous label"
        rows.append({
            "lobbying_issue": issue,
            "topic": topic,
            "linkage_status": status,
            "lobbying_rows": str(len(issue_rows)),
            "unique_clients": str(len({row.get("client", "").strip() for row in issue_rows if row.get("client", "").strip()})),
            "unique_filings": str(len({row.get("filing_uuid", "").strip() for row in issue_rows if row.get("filing_uuid", "").strip()})),
            "total_amount": money(sum((decimal_value(row.get("amount", "")) for row in issue_rows), Decimal("0"))),
            "topic_introduced": topic_row.get("introduced", ""),
            "topic_floor_considered": topic_row.get("floor_considered", ""),
            "topic_enacted": topic_row.get("enacted", ""),
            "evidence_layers": evidence_layers,
            "missing_links": missing_links,
            "crosswalk_basis": basis,
            "source_url": "https://lda.senate.gov/api/v1/filings/",
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_metadata(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    represented_rows = sum(int(row["lobbying_rows"]) for row in rows)
    linked_rows = sum(
        int(row["lobbying_rows"])
        for row in rows
        if row["linkage_status"] == "issue_topic_crosswalk"
    )
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    OUT_METADATA.write_text(
        "# Lobbying Issue Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- `{LOBBYING}`\n"
        f"- `{TOPICS}`\n"
        "- Senate LDA filings API: https://lda.senate.gov/api/v1/filings/\n\n"
        "Transformation:\n\n"
        "- Groups cached Senate LDA rows by public issue label.\n"
        "- Applies a deterministic issue-label to Congress.gov policy-area topic crosswalk.\n"
        "- Preserves unmatched ambiguous labels rather than inferring hidden topics.\n"
        "- Attaches topic-throughput aggregate counts when the mapped policy area exists locally.\n\n"
        f"Issue rows represented: {len(rows)}\n\n"
        f"Lobbying rows represented: {represented_rows}\n\n"
        f"Lobbying rows with issue-topic context: {linked_rows}\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary: this cache links public LDA issue labels to broad local policy-area "
        "topic labels. It does not link lobbying clients to bills, sponsors, committees, "
        "roll calls, legislative outcomes, public benefit, welfare, causal capture, or model validation.\n"
    )


def main() -> int:
    rows = build_rows()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
