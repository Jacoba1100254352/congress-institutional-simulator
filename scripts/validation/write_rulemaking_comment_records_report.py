#!/usr/bin/env python3
"""Write a report for bounded Regulations.gov comment-record metadata."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/rulemaking_comment_records.csv")
OUT_CSV = Path("reports/rulemaking-comment-records.csv")
OUT_MD = Path("reports/rulemaking-comment-records.md")

COMPLETE_STATUSES = {
    "complete_comment_record_metadata_retrieved",
    "complete_no_comments_expected",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def int_value(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def short(value: str, limit: int = 90) -> str:
    if not value:
        return "---"
    return value if len(value) <= limit else value[: limit - 3] + "..."


def write_md(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["retrieval_status"] for row in rows)
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    complete_rows = [row for row in rows if row["retrieval_status"] in COMPLETE_STATUSES]
    blocked_rows = [row for row in rows if row["retrieval_status"] not in COMPLETE_STATUSES]
    expected_comments = sum(int_value(row["expected_comment_count"]) for row in rows)
    retrieved_comments = sum(int_value(row["retrieved_comment_count"]) for row in rows)
    complete_public_laws = {
        public_law
        for public_law in public_laws
        if all(
            row["retrieval_status"] in COMPLETE_STATUSES
            for row in rows
            if row["public_law_number"] == public_law
        )
    }

    lines = [
        "# Rulemaking Comment Records",
        "",
        "This report derives bounded Regulations.gov comment-record metadata for Federal Register-exposed rulemaking dockets. Complete rows mean all public comment record metadata for a docket within the configured retrieval threshold was retrieved, or the Federal Register metadata exposed zero expected comments. Partial rows preserve retrieved public metadata but do not prove completeness. It is not comment-text, attachment, commenter-identity, or implementation-outcome evidence.",
        "",
        f"- Public-law rows represented: {len(public_laws)}",
        f"- Public-law rows with all represented dockets complete: {len(complete_public_laws)}",
        f"- Public-law/docket rows reviewed: {len(rows)}",
        f"- Complete public-law/docket rows: {len(complete_rows)}",
        f"- Partial, skipped, or blocked public-law/docket rows: {len(blocked_rows)}",
        f"- Expected comments counted from Federal Register metadata: {expected_comments}",
        f"- Retrieved public comment record metadata rows: {retrieved_comments}",
        "",
        "Claim boundary: this report records bounded Regulations.gov comment-record metadata only. It does not include comment text, attachments, private submitter details, commenter-identity validation, sentiment, Unified Agenda stages, enforcement outcomes, appropriations capacity, implementation outcomes, public benefit, welfare, causal effects, or model validation.",
        "",
        "Comment-record statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "| Public law | Docket | Status | Expected | Retrieved | Context | Missing links |",
        "| --- | --- | --- | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| `{row['public_law_number']}` | `{row['docket_id']}` | "
            f"{row['retrieval_status']} | "
            f"{row['expected_comment_count'] or '---'} | "
            f"{row['retrieved_comment_count'] or '0'} | "
            f"{short(row['source_contexts'])} | "
            f"{short(row['missing_links'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-rulemaking-comment-records-raw first.")
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
