#!/usr/bin/env python3
"""Write a report for bounded rulemaking comment metadata."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/rulemaking_comment_metadata.csv")
OUT_CSV = Path("reports/rulemaking-comment-metadata.csv")
OUT_MD = Path("reports/rulemaking-comment-metadata.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def short(value: str, limit: int = 90) -> str:
    if not value:
        return "---"
    return value if len(value) <= limit else value[: limit - 3] + "..."


def int_value(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["comment_metadata_status"] for row in rows)
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    final_fetched = sum(1 for row in rows if row["final_detail_status"] == "federal_register_final_detail_fetched")
    final_docket_rows = sum(1 for row in rows if row["final_regulations_docket_id"])
    final_comment_count_rows = sum(1 for row in rows if row["final_regulations_comments_count"])
    final_positive_comment_rows = sum(1 for row in rows if int_value(row["final_regulations_comments_count"]) > 0)
    proposed_detail_fetches = sum(int_value(row["proposed_detail_fetch_count"]) for row in rows)
    proposed_docket_rows = sum(1 for row in rows if int_value(row["proposed_regulations_docket_count"]) > 0)
    proposed_comment_url_rows = sum(1 for row in rows if int_value(row["proposed_regulations_comment_url_count"]) > 0)
    proposed_comment_close_rows = sum(1 for row in rows if int_value(row["proposed_comments_close_date_count_refetched"]) > 0)
    proposed_comment_count_rows = sum(1 for row in rows if int_value(row["proposed_comment_count_rows"]) > 0)
    proposed_positive_comment_rows = sum(1 for row in rows if int_value(row["proposed_positive_comment_count_rows"]) > 0)
    proposed_comment_total = sum(int_value(row["proposed_comment_count_total"]) for row in rows)
    proposed_dockets = {
        docket
        for row in rows
        for docket in split_semicolon(row["proposed_regulations_docket_ids_refetched"])
    }
    proposed_comment_urls = {
        url
        for row in rows
        for url in split_semicolon(row["proposed_regulations_comments_urls_refetched"])
    }

    lines = [
        "# Rulemaking Comment Metadata",
        "",
        "This report derives bounded Federal Register-exposed Regulations.gov metadata for authority-matched final-rule rows and their matched proposed-rule records. It is a metadata review aid, not complete comment-record or implementation-outcome evidence.",
        "",
        f"- Public-law rows represented: {len(public_laws)}",
        f"- Authority-matched final-rule rows reviewed: {len(rows)}",
        f"- Rows with final Federal Register detail fetched: {final_fetched}",
        f"- Rows with final Regulations.gov docket metadata: {final_docket_rows}",
        f"- Rows with final comments-count metadata: {final_comment_count_rows}",
        f"- Rows with final positive comments counts: {final_positive_comment_rows}",
        f"- Matched proposed-rule detail records fetched: {proposed_detail_fetches}",
        f"- Rows with proposed-rule Regulations.gov docket metadata: {proposed_docket_rows}",
        f"- Unique proposed-rule Regulations.gov docket IDs: {len(proposed_dockets)}",
        f"- Rows with proposed-rule comment URLs: {proposed_comment_url_rows}",
        f"- Unique proposed-rule comment URLs: {len(proposed_comment_urls)}",
        f"- Rows with proposed-rule comment-close dates: {proposed_comment_close_rows}",
        f"- Rows with proposed-rule comments-count metadata: {proposed_comment_count_rows}",
        f"- Rows with proposed-rule positive comments counts: {proposed_positive_comment_rows}",
        f"- Proposed-rule comments counted in exposed metadata: {proposed_comment_total}",
        "",
        "Claim boundary: this report records Federal Register-exposed Regulations.gov metadata only. It is not complete comment-record evidence, commenter identity or comment-text evidence, Unified Agenda stage coverage, enforcement outcomes, appropriations capacity, exhaustive implementation coverage, public benefit, welfare, causal effects, or model validation.",
        "",
        "Comment metadata statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "| Public law | Final rule | Status | Final comments | Proposed fetches | Proposed docket metadata | Proposed comment URLs | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| `{row['public_law_number']}` | `{row['final_document_number']}` | "
            f"{row['comment_metadata_status']} | "
            f"{row['final_regulations_comments_count'] or '---'} | "
            f"{row['proposed_detail_fetch_count']} | "
            f"{row['proposed_regulations_docket_count']} | "
            f"{row['proposed_regulations_comment_url_count']} | "
            f"{short(row['missing_links'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-rulemaking-comment-metadata-raw first.")
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
