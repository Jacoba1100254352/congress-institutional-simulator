#!/usr/bin/env python3
"""Write a report for the bounded Federal Register proposed-rule history cache."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/rulemaking_history_linkage.csv")
OUT_CSV = Path("reports/rulemaking-history-linkage.csv")
OUT_MD = Path("reports/rulemaking-history-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def short(value: str, limit: int = 90) -> str:
    if not value:
        return "---"
    return value if len(value) <= limit else value[: limit - 3] + "..."


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["history_status"] for row in rows)
    matched_rows = [
        row for row in rows
        if row["history_status"] == "proposed_rule_history_match"
    ]
    candidate_count = sum(int(row["candidate_proposed_rule_count"] or "0") for row in rows)
    matched_count = sum(int(row["matched_proposed_rule_count"] or "0") for row in rows)
    proposed_docs = {
        document
        for row in matched_rows
        for document in split_semicolon(row["proposed_document_numbers"])
    }
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    matched_public_laws = {row["public_law_number"] for row in matched_rows if row["public_law_number"]}

    lines = [
        "# Rulemaking History Linkage",
        "",
        "This report derives a bounded Federal Register proposed-to-final history bridge for final-rule documents that already cite cached public laws as authority. It is a join inventory, not implementation-outcome or public-comment validation.",
        "",
        f"- Public-law rows represented: {len(public_laws)}",
        f"- Authority-matched final-rule rows checked: {len(rows)}",
        f"- Final-rule rows with proposed-rule history matches: {len(matched_rows)}",
        f"- Public-law rows with at least one proposed-rule history match: {len(matched_public_laws)}",
        f"- Candidate proposed-rule documents inspected: {candidate_count}",
        f"- Matched proposed-rule links: {matched_count}",
        f"- Unique matched proposed-rule documents: {len(proposed_docs)}",
        "",
        "Claim boundary: this cache links authority-matched final rules to proposed-rule Federal Register metadata only when the records share RIN or docket identifiers and the proposed rule is not later than the final rule. It does not provide complete Regulations.gov comment records, Unified Agenda stages, enforcement outcomes, appropriations capacity, exhaustive implementation coverage, public benefit, welfare, causal effects, or model validation.",
        "",
        "History statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "| Public law | Final rule | Status | Candidates | Matched proposed rules | Shared identifiers | Earliest-to-final days | Missing links |",
        "| --- | --- | --- | ---: | ---: | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| `{row['public_law_number']}` | `{row['final_document_number']}` | "
            f"{row['history_status']} | {row['candidate_proposed_rule_count']} | "
            f"{row['matched_proposed_rule_count']} | {short(row['shared_identifiers'])} | "
            f"{row['days_from_earliest_proposed_to_final'] or '---'} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-rulemaking-history-linkage-raw first.")
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
