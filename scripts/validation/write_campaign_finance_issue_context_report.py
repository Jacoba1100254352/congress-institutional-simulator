#!/usr/bin/env python3
"""Write a report for bounded campaign-finance issue-context joins."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


RAW_CONTEXT = Path("data/validation/raw/campaign_finance_issue_context.csv")
OUT_CSV = Path("reports/campaign-finance-issue-context.csv")
OUT_MD = Path("reports/campaign-finance-issue-context.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_amount(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["issue_context_status"] for row in rows)
    mapped = [
        row for row in rows
        if row["issue_context_status"] == "campaign_finance_issue_topic_context"
    ]
    unique_recipients = {row["recipient"] for row in mapped if row["recipient"]}
    unique_topics = {row["mapped_topic"] for row in mapped if row["mapped_topic"]}
    mapped_amount = sum(parse_amount(row["amount"]) for row in mapped)
    total_amount = sum(parse_amount(row["amount"]) for row in rows)
    topic_amounts: dict[str, float] = defaultdict(float)
    topic_rows = Counter(row["mapped_topic"] for row in mapped if row["mapped_topic"])
    for row in mapped:
        if row["mapped_topic"]:
            topic_amounts[row["mapped_topic"]] += parse_amount(row["amount"])

    lines = [
        "# Campaign-Finance Issue Context",
        "",
        "This report derives bounded issue-sector context from cached public OpenFEC transaction labels and local Congress.gov policy-area topics. It is an exposure/context inventory, not bill-level influence validation.",
        "",
        f"- Campaign-finance transaction rows inspected: {len(rows)}",
        f"- Rows with bounded issue-topic context: {len(mapped)}",
        f"- Rows left unmapped: {len(rows) - len(mapped)}",
        f"- Unique mapped topics: {len(unique_topics)}",
        f"- Recipients represented in mapped rows: {len(unique_recipients)}",
        f"- Total amount represented: {total_amount:.2f}",
        f"- Amount in mapped issue-topic rows: {mapped_amount:.2f}",
        "",
        "Claim boundary: mapped rows connect public OpenFEC transaction labels to broad policy-area topic context only. They do not identify bill-level influence, committee jurisdiction, outside-spending target beyond public FEC recipient IDs, legislative outcomes, private contributor details, causal influence, capture, public benefit, or model validation.",
        "",
        "Issue-context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "| Topic | Rows | Amount |",
        "| --- | ---: | ---: |",
    ])
    for topic, count in sorted(topic_rows.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {topic} | {count} | {topic_amounts[topic]:.2f} |")

    lines.extend([
        "",
        "| Source ID | Recipient | Label | Topic | Amount | Mapping basis | Missing links |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for row in mapped:
        lines.append(
            f"| `{row['source_id']}` | `{row['recipient']}` | {row['industry'] or '---'} | "
            f"{row['mapped_topic']} | {row['amount']} | {row['mapping_basis']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW_CONTEXT.exists():
        raise SystemExit(f"{RAW_CONTEXT} is missing; run make build-campaign-finance-issue-context-raw first.")
    rows = read_csv(RAW_CONTEXT)
    if not rows:
        raise SystemExit(f"{RAW_CONTEXT} is empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
