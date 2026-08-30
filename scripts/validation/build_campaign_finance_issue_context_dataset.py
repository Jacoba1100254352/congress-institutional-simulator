#!/usr/bin/env python3
"""Build a bounded campaign-finance issue-context bridge.

The raw OpenFEC sample intentionally omits contributor names and addresses, but
it preserves a bounded occupation/employer/expenditure-purpose label in the
`industry` column. This builder maps high-confidence labels to the local
Congress.gov policy-area topic sample. The output is issue-sector context only,
not bill-level influence evidence.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


CAMPAIGN_FINANCE = Path("data/validation/raw/campaign_finance.csv")
CAMPAIGN_FINANCE_LINKAGE = Path("data/validation/raw/campaign_finance_linkage.csv")
TOPIC_THROUGHPUT = Path("data/validation/raw/topic_throughput.csv")
OUT_CSV = Path("data/validation/raw/campaign_finance_issue_context.csv")
OUT_METADATA = Path("data/validation/raw/campaign_finance_issue_context.metadata.md")

CLAIM_BOUNDARY = (
    "Bounded public OpenFEC transaction-label to broad policy-topic context only; "
    "not bill-level influence, committee jurisdiction, outside-spending target "
    "beyond public FEC recipient IDs, legislative outcome, private contributor "
    "disclosure, causal capture validation, public benefit, or model validation."
)

MISSING_LINKS = (
    "bill_id; committee_of_jurisdiction; outside_spending_target_review; "
    "legislative_outcome; complete_issue_ontology; private_contributor_details; "
    "causal_influence_or_capture_validation; model_validation"
)

TOPIC_KEYWORDS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    (
        "Health",
        (
            "registered nurse",
            "nursing aide",
            "nursing",
            "nurse",
            "home health",
            "physician",
            "dentist",
            "mri technologist",
            "dietary aide",
            "medical",
            "health",
        ),
        "health occupation label",
    ),
    (
        "Finance and Financial Sector",
        (
            "finance",
            "investor",
            "accountant",
        ),
        "finance occupation label",
    ),
    (
        "Transportation and Public Works",
        (
            "transporter",
            "airline agent",
        ),
        "transportation occupation label",
    ),
    (
        "Science, Technology, Communications",
        (
            "information systems",
            "technology",
            "communications",
        ),
        "technology occupation label",
    ),
    (
        "Law",
        (
            "attorney",
        ),
        "legal occupation label",
    ),
    (
        "Crime and Law Enforcement",
        (
            "security",
        ),
        "security occupation label",
    ),
    (
        "Commerce",
        (
            "warehouse",
        ),
        "commerce or logistics occupation label",
    ),
    (
        "Education",
        (
            "student",
        ),
        "education-status label",
    ),
)

FIELDNAMES = [
    "cycle",
    "recipient",
    "source_id",
    "source_schedule",
    "transaction_date",
    "independent_expenditure",
    "industry",
    "amount",
    "recipient_type",
    "recipient_linkage_status",
    "candidate_id",
    "candidate_name",
    "committee_id",
    "committee_name",
    "issue_context_status",
    "mapped_topic",
    "topic_introduced",
    "topic_floor_considered",
    "topic_enacted",
    "mapping_basis",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def norm(value: str | None) -> str:
    return clean(value).casefold()


def parse_amount(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def by_recipient(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        cycles = [value.strip() for value in row.get("cycle", "").split(";") if value.strip()]
        if not cycles:
            cycles = [""]
        recipient = row.get("recipient", "").strip()
        for cycle in cycles:
            result[(cycle, recipient)] = row
    return result


def topic_by_name(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("topic", "").strip(): row for row in rows if row.get("topic", "").strip()}


def topic_for_label(label: str, available_topics: set[str]) -> tuple[str, str]:
    normalized = norm(label)
    if not normalized:
        return "", "empty_label"
    for topic, keywords, basis in TOPIC_KEYWORDS:
        if topic not in available_topics:
            continue
        if any(keyword in normalized for keyword in keywords):
            return topic, basis
    return "", "unmapped_or_too_generic_label"


def build_rows() -> list[dict[str, str]]:
    campaign_rows = read_csv(CAMPAIGN_FINANCE)
    linkage_by_recipient = by_recipient(read_csv(CAMPAIGN_FINANCE_LINKAGE))
    topics = topic_by_name(read_csv(TOPIC_THROUGHPUT))
    available_topics = set(topics)
    rows: list[dict[str, str]] = []
    for campaign in campaign_rows:
        cycle = campaign.get("cycle", "").strip()
        recipient = campaign.get("recipient", "").strip()
        linkage = linkage_by_recipient.get((cycle, recipient), {})
        mapped_topic, mapping_basis = topic_for_label(campaign.get("industry", ""), available_topics)
        topic = topics.get(mapped_topic, {})
        mapped = bool(mapped_topic)
        rows.append({
            "cycle": cycle,
            "recipient": recipient,
            "source_id": campaign.get("source_id", ""),
            "source_schedule": campaign.get("source_schedule", ""),
            "transaction_date": campaign.get("transaction_date", ""),
            "independent_expenditure": campaign.get("independent_expenditure", ""),
            "industry": campaign.get("industry", ""),
            "amount": campaign.get("amount", ""),
            "recipient_type": linkage.get("recipient_type", ""),
            "recipient_linkage_status": linkage.get("linkage_status", ""),
            "candidate_id": linkage.get("candidate_id", ""),
            "candidate_name": linkage.get("candidate_name", ""),
            "committee_id": linkage.get("committee_id", ""),
            "committee_name": linkage.get("committee_name", ""),
            "issue_context_status": "campaign_finance_issue_topic_context" if mapped else "unmapped_campaign_finance_label",
            "mapped_topic": mapped_topic,
            "topic_introduced": topic.get("introduced", ""),
            "topic_floor_considered": topic.get("floor_considered", ""),
            "topic_enacted": topic.get("enacted", ""),
            "mapping_basis": mapping_basis,
            "evidence_layers": (
                "openfec_transaction_label; campaign_finance_recipient_metadata; "
                "topic_throughput_policy_area"
                if mapped
                else "openfec_transaction_label; campaign_finance_recipient_metadata"
            ),
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    mapped_rows = [
        row for row in rows
        if row["issue_context_status"] == "campaign_finance_issue_topic_context"
    ]
    status_counts = Counter(row["issue_context_status"] for row in rows)
    topic_counts = Counter(row["mapped_topic"] for row in mapped_rows)
    mapped_amount = sum(parse_amount(row.get("amount")) for row in mapped_rows)
    total_amount = sum(parse_amount(row.get("amount")) for row in rows)
    topic_lines = "\n".join(
        f"- {topic}: {count}"
        for topic, count in sorted(topic_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    status_lines = "\n".join(
        f"- {status}: {count}" for status, count in sorted(status_counts.items())
    )
    OUT_METADATA.write_text(
        "# Campaign-Finance Issue-Context Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- Campaign-finance transaction sample: `{CAMPAIGN_FINANCE}`.\n"
        f"- FEC recipient metadata cache: `{CAMPAIGN_FINANCE_LINKAGE}`.\n"
        f"- Local Congress.gov policy-area topic throughput: `{TOPIC_THROUGHPUT}`.\n\n"
        "Transformation:\n\n"
        "- Preserves one output row per cached campaign-finance transaction.\n"
        "- Maps high-confidence occupation, employer, or expenditure-purpose labels to broad policy-area topics using a deterministic local keyword table.\n"
        "- Requires the mapped topic to exist in the local topic-throughput sample.\n"
        "- Leaves generic roles, support/oppose flags, unknown labels, and campaign-administrative labels unmapped.\n"
        "- Adds no contributor names, contributor addresses, payee names, or private contact information.\n\n"
        "Rows:\n\n"
        f"- Campaign-finance transaction rows inspected: {len(rows)}.\n"
        f"- Rows with bounded issue-topic context: {len(mapped_rows)}.\n"
        f"- Rows left unmapped: {len(rows) - len(mapped_rows)}.\n"
        f"- Unique mapped topics: {len(topic_counts)}.\n"
        f"- Total amount represented: {total_amount:.2f}.\n"
        f"- Amount in mapped issue-topic rows: {mapped_amount:.2f}.\n\n"
        "Statuses:\n\n"
        f"{status_lines}\n\n"
        "Mapped topics:\n\n"
        f"{topic_lines if topic_lines else '- none'}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def main() -> int:
    for path in (CAMPAIGN_FINANCE, CAMPAIGN_FINANCE_LINKAGE, TOPIC_THROUGHPUT):
        if not path.exists():
            raise SystemExit(f"{path} is missing; build prerequisite raw data first.")
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{CAMPAIGN_FINANCE} is empty.")
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
