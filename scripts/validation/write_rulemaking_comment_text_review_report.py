#!/usr/bin/env python3
"""Write the sanitized rulemaking comment text-review report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/rulemaking_comment_text_review.csv")
OUT_CSV = Path("reports/rulemaking-comment-text-review.csv")
OUT_MD = Path("reports/rulemaking-comment-text-review.md")

CUE_FIELDS = [
    "implementation_timing_cue",
    "cost_or_burden_cue",
    "compliance_or_standard_cue",
    "safety_or_security_cue",
    "program_design_cue",
]

REQUIRED_FIELDS = {
    "public_law_number",
    "docket_id",
    "comment_id",
    "comment_record_retrieval_status",
    "comment_detail_review_scope",
    "source_retrieved_comment_count",
    "source_expected_comment_count",
    "detail_fetch_status",
    "comment_text_available",
    "comment_text_character_count",
    "comment_text_sha256",
    "attachment_count",
    "missing_links",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def validate_schema(rows: list[dict[str, str]]) -> None:
    missing = sorted(REQUIRED_FIELDS.difference(rows[0]))
    if missing:
        raise SystemExit(
            f"{RAW} is missing columns {missing}; "
            "run make build-rulemaking-comment-text-review-raw to refresh the sanitized raw cache."
        )


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


def short_hash(value: str) -> str:
    return value[:12] if value else "---"


def short(value: str, limit: int = 70) -> str:
    if not value:
        return "---"
    return value if len(value) <= limit else value[: limit - 3] + "..."


def write_md(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["detail_fetch_status"] for row in rows)
    scopes = Counter(row["comment_detail_review_scope"] for row in rows)
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    dockets = {row["docket_id"] for row in rows if row["docket_id"]}
    text_rows = [row for row in rows if row["comment_text_available"] == "yes"]
    attachment_rows = [row for row in rows if int_value(row["attachment_count"]) > 0]
    cue_counts = Counter(
        cue_field
        for row in rows
        for cue_field in CUE_FIELDS
        if row.get(cue_field) == "yes"
    )

    lines = [
        "# Rulemaking Comment Text Review",
        "",
        "This report summarizes a sanitized Regulations.gov public comment-detail review for complete bounded comment-record rows and bounded partial-docket samples. It records text availability, normalized text hashes, lengths, attachment counts, source comment-record status, and coarse implementation-related cue flags while omitting the full comment body and submitter/contact fields.",
        "",
        f"- Public-law rows represented: {len(public_laws)}",
        f"- Dockets represented: {len(dockets)}",
        f"- Public comment-detail rows reviewed: {len(rows)}",
        f"- Rows with public comment text available and hashed: {len(text_rows)}",
        f"- Rows with attachment relationships: {len(attachment_rows)}",
        "",
        "Claim boundary: this report records sanitized public comment-detail availability and hash/cue metadata only. Partial sample rows do not prove complete docket coverage. It does not include the full comment body, attachment text, private submitter details, commenter-identity validation, sentiment or position coding, representativeness evidence, Unified Agenda stages, enforcement outcomes, appropriations capacity, implementation outcomes, public benefit, welfare, causal effects, or model validation.",
        "",
        "Review scopes:",
    ]
    for scope, count in sorted(scopes.items()):
        lines.append(f"- {scope}: {count}")
    lines.extend([
        "",
        "Detail statuses:",
    ])
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Cue counts:"])
    for cue_field in CUE_FIELDS:
        lines.append(f"- {cue_field}: {cue_counts.get(cue_field, 0)}")

    lines.extend([
        "",
        "| Public law | Docket | Comment | Scope | Status | Text chars | Text hash | Cue terms | Attachments | Missing links |",
        "| --- | --- | --- | --- | --- | ---: | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| `{row['public_law_number']}` | `{row['docket_id']}` | "
            f"`{row['comment_id']}` | {row['comment_detail_review_scope']} | "
            f"{row['detail_fetch_status']} | "
            f"{row['comment_text_character_count']} | `{short_hash(row['comment_text_sha256'])}` | "
            f"{short(row['cue_terms'])} | {row['attachment_count']} | "
            f"{short(row['missing_links'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-rulemaking-comment-text-review-raw first.")
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    validate_schema(rows)
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
