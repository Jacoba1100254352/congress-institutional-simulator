#!/usr/bin/env python3
"""Write a report for the bounded Federal Register authority linkage cache."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/rulemaking_authority_linkage.csv")
OUT_CSV = Path("reports/rulemaking-authority-linkage.csv")
OUT_MD = Path("reports/rulemaking-authority-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    matched_rows = [
        row for row in rows
        if row["linkage_status"] == "federal_register_authority_match"
    ]
    verified_docs = sum(int(row["text_verified_rule_count"] or "0") for row in rows)
    searched_docs = sum(int(row.get("candidate_rule_count", "0") or "0") for row in rows)
    usc_rows = sum(1 for row in matched_rows if row["usc_citations"])
    unique_docs = {
        document.strip()
        for row in rows
        for document in row["matched_document_numbers"].split(";")
        if document.strip()
    }

    lines = [
        "# Rulemaking Authority Linkage",
        "",
        "This report derives a bounded Federal Register text-search bridge from cached public-law bill/action rows to rule documents that cite those public laws as authority. It is a join inventory, not implementation-outcome validation.",
        "",
        f"- Public-law rows searched: {len(rows)}",
        f"- Rows with text-verified Federal Register authority matches: {len(matched_rows)}",
        f"- Candidate rule documents inspected: {searched_docs}",
        f"- Unique text-verified rule documents: {len(unique_docs)}",
        f"- Text-verified matched rule documents: {verified_docs}",
        f"- Matched rows with U.S. Code citations: {usc_rows}",
        "",
        "Claim boundary: this cache verifies public-law citations in bounded Federal Register rule text. It does not prove exhaustive implementation, proposed-rule history, enforcement outcome, appropriations capacity, complete public-comment records, court review, public benefit, welfare, causal effect, or model validation.",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend([
        "",
        "| Public law | Bill | Status | Candidates | Verified rules | Verified documents | U.S.C. citations | Missing links |",
        "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ])
    for row in rows:
        documents = row["matched_document_numbers"] or "---"
        if len(documents) > 80:
            documents = documents[:77] + "..."
        uscs = row["usc_citations"] or "---"
        if len(uscs) > 100:
            uscs = uscs[:97] + "..."
        lines.append(
            f"| `{row['public_law_number']}` | `{row['bill_id']}` | {row['linkage_status']} | "
            f"{row.get('candidate_rule_count', '0')} | {row['text_verified_rule_count']} | {documents} | {uscs} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-rulemaking-authority-linkage-raw first.")
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
