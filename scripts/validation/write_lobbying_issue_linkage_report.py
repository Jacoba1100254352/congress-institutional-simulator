#!/usr/bin/env python3
"""Write a bounded lobbying issue-linkage report from cached data."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


LOBBYING_ISSUE_LINKAGE = Path("data/validation/raw/lobbying_issue_linkage.csv")
OUT_CSV = Path("reports/lobbying-issue-linkage.csv")
OUT_MD = Path("reports/lobbying-issue-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def money_total(rows: list[dict[str, str]]) -> float:
    total = 0.0
    for row in rows:
        try:
            total += float(row.get("total_amount", "0") or "0")
        except ValueError:
            continue
    return total


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    topic_counts = Counter(row["topic"] for row in rows if row.get("topic"))
    represented_rows = sum(int(row.get("lobbying_rows", "0") or "0") for row in rows)
    linked_rows = sum(
        int(row.get("lobbying_rows", "0") or "0")
        for row in rows
        if row.get("linkage_status") == "issue_topic_crosswalk"
    )
    unique_clients = sum(int(row.get("unique_clients", "0") or "0") for row in rows)
    linked_issue_rows = [row for row in rows if row.get("linkage_status") == "issue_topic_crosswalk"]

    lines = [
        "# Lobbying Issue Linkage",
        "",
        "This report derives a bounded issue-taxonomy bridge from cached Senate LDA issue labels to cached Congress.gov policy-area topic aggregates. It is issue context, not bill-level lobbying validation.",
        "",
        f"- LDA issue labels represented: {len(rows)}",
        f"- LDA activity rows represented: {represented_rows}",
        f"- LDA activity rows with issue-topic context: {linked_rows}",
        f"- Sum of issue-level unique-client counts: {unique_clients}",
        f"- Issue-level disclosed amount represented: {money_total(rows):.2f}",
        "",
        "Claim boundary: this report links public LDA issue labels to broad local policy-area topic labels. It does not link lobbying clients to bills, sponsors, committees, roll calls, legislative outcomes, public benefit, welfare, causal capture, or model validation.",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Mapped topics:"])
    for topic, count in sorted(topic_counts.items()):
        lines.append(f"- {topic}: {count}")
    lines.extend([
        "",
        "| LDA issue | Topic | Status | LDA rows | Clients | Amount | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ])
    for row in sorted(
        rows,
        key=lambda item: (-int(item.get("lobbying_rows", "0") or "0"), item.get("lobbying_issue", "")),
    ):
        topic = row["topic"] if row.get("topic") else "---"
        lines.append(
            f"| {row['lobbying_issue']} | {topic} | {row['linkage_status']} | "
            f"{row['lobbying_rows']} | {row['unique_clients']} | {row['total_amount']} | "
            f"{row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(LOBBYING_ISSUE_LINKAGE)
    if not rows:
        raise SystemExit(f"{LOBBYING_ISSUE_LINKAGE} is missing or empty; run make build-lobbying-issue-linkage-raw first.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
