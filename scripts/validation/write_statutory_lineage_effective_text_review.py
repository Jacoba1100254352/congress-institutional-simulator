#!/usr/bin/env python3
"""Write bounded effective-text source review for statutory-lineage target diffs."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
OLRC_CURRENT_SCAN = Path("reports/statutory-lineage-olrc-current-scan.csv")
OLRC_ANNUAL_TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
OUT_CSV = Path("reports/statutory-lineage-effective-text-review.csv")
OUT_MD = Path("reports/statutory-lineage-effective-text-review.md")

UNREVIEWED_CAUSATION_STATUS = "not_reviewed_for_exclusive_public_law_causation"

CLAIM_BOUNDARY = (
    "Law-revision effective-text source review only. Rows confirm official OLRC "
    "current U.S. Code source availability and current public-law note presence "
    "for source-reviewed target-section diff rows. This artifact does not "
    "establish exclusive public-law causal attribution, complete codified "
    "lineage, implementation outcomes, direct target-section court review, "
    "welfare evidence, causal effects, or model validation."
)

FIELDNAMES = [
    "effective_text_review_rank",
    "review_rank",
    "target_review_packet_rank",
    "text_diff_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "codified_lineage_relationship",
    "target_section_diff_review_status",
    "source_reviewed_target_section_diff",
    "pre_edition",
    "post_edition",
    "pre_olrc_url",
    "post_olrc_url",
    "current_olrc_url",
    "current_olrc_scan_status",
    "current_olrc_http_status",
    "current_official_text_sha256",
    "current_official_text_bytes",
    "current_section_heading",
    "current_public_law_reference_hits",
    "current_public_law_reference_status",
    "post_public_law_context_count",
    "pre_normalized_text_sha256",
    "post_normalized_text_sha256",
    "current_effective_text_review_status",
    "law_revision_effective_text_reviewed",
    "effective_text_source_basis",
    "effective_text_review_summary",
    "public_law_causal_attribution",
    "source_review_notes",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run the upstream statutory-lineage target first.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def int_field(row: dict[str, str], field: str) -> int:
    try:
        return int(row.get(field, "0") or "0")
    except ValueError:
        return 0


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("target_reference", "").strip(),
    )


def by_key(rows: list[dict[str, str]], source_name: str) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        key = row_key(row)
        if not all(key):
            raise SystemExit(f"{source_name}: row missing bill/public-law/target-reference key.")
        if key in result:
            raise SystemExit(f"{source_name}: duplicate target key {key}.")
        result[key] = row
    return result


def review_status(current: dict[str, str]) -> tuple[str, str, str]:
    if current.get("olrc_scan_status", "").strip() != "official_olrc_current_section_page_fetched":
        return (
            "current_effective_text_source_not_fetched",
            "0",
            "Official OLRC current U.S. Code page was not fetched for this target reference; effective-text review remains open.",
        )
    if int_field(current, "official_text_bytes") <= 0 or not current.get("official_text_sha256", "").strip():
        return (
            "current_effective_text_source_missing_text_hash",
            "0",
            "Official OLRC current U.S. Code page fetch lacks text/hash evidence; effective-text review remains open.",
        )
    if current.get("public_law_reference_status", "").strip() == "current_page_mentions_public_law":
        return (
            "reviewed_current_effective_text_source_with_public_law_note",
            "1",
            "Official OLRC current U.S. Code page was fetched and its current text mentions the queued public law; public-law causation remains separately unreviewed.",
        )
    return (
        "reviewed_current_effective_text_source_without_public_law_note",
        "1",
        "Official OLRC current U.S. Code page was fetched, but the current text does not mention the queued public law; public-law causation remains separately unreviewed.",
    )


def build_rows() -> list[dict[str, str]]:
    diff_rows = [
        row for row in read_csv(TARGET_DIFF_REVIEW)
        if row.get("source_reviewed_target_section_diff", "").strip() == "1"
    ]
    if not diff_rows:
        raise SystemExit(f"{TARGET_DIFF_REVIEW}: no source-reviewed target-section diff rows.")
    current_by_key = by_key(read_csv(OLRC_CURRENT_SCAN), str(OLRC_CURRENT_SCAN))
    annual_by_key = by_key(read_csv(OLRC_ANNUAL_TEXT_DIFF), str(OLRC_ANNUAL_TEXT_DIFF))

    rows: list[dict[str, str]] = []
    for review_row in sorted(diff_rows, key=lambda row: int_field(row, "review_rank")):
        key = row_key(review_row)
        current = current_by_key.get(key)
        annual = annual_by_key.get(key)
        if current is None:
            raise SystemExit(f"{OLRC_CURRENT_SCAN}: missing current-source row for {key}.")
        if annual is None:
            raise SystemExit(f"{OLRC_ANNUAL_TEXT_DIFF}: missing annual text-diff row for {key}.")
        status, reviewed, summary = review_status(current)
        missing_links = [
            "complete_codified_usc_lineage_review",
            "public_law_causal_attribution",
            "implementation_outcomes",
            "direct_target_section_court_review",
            "welfare_or_public_benefit",
            "model_validation",
        ]
        if reviewed != "1":
            missing_links.insert(0, "law_revision_effective_text")
        evidence_layers = [
            "statutory_lineage_source_reviewed_target_section_diff",
            "official_olrc_annual_us_code_text_diff",
            "official_olrc_current_us_code_page",
            "statutory_lineage_effective_text_source_review",
        ]
        rows.append({
            "effective_text_review_rank": str(len(rows) + 1),
            "review_rank": review_row.get("review_rank", "").strip(),
            "target_review_packet_rank": review_row.get("target_review_packet_rank", "").strip(),
            "text_diff_rank": review_row.get("text_diff_rank", "").strip(),
            "bill_id": review_row.get("bill_id", "").strip(),
            "public_law_number": review_row.get("public_law_number", "").strip(),
            "enacted_date": review_row.get("enacted_date", "").strip(),
            "target_reference": review_row.get("target_reference", "").strip(),
            "target_reference_type": review_row.get("target_reference_type", "").strip(),
            "normalized_title": review_row.get("normalized_title", "").strip(),
            "normalized_section": review_row.get("normalized_section", "").strip(),
            "codified_lineage_relationship": review_row.get("codified_lineage_relationship", "").strip(),
            "target_section_diff_review_status": review_row.get("review_status", "").strip(),
            "source_reviewed_target_section_diff": "1",
            "pre_edition": review_row.get("pre_edition", "").strip(),
            "post_edition": review_row.get("post_edition", "").strip(),
            "pre_olrc_url": review_row.get("pre_olrc_url", "").strip(),
            "post_olrc_url": review_row.get("post_olrc_url", "").strip(),
            "current_olrc_url": current.get("olrc_url", "").strip(),
            "current_olrc_scan_status": current.get("olrc_scan_status", "").strip(),
            "current_olrc_http_status": current.get("http_status", "").strip(),
            "current_official_text_sha256": current.get("official_text_sha256", "").strip(),
            "current_official_text_bytes": current.get("official_text_bytes", "").strip(),
            "current_section_heading": current.get("section_heading", "").strip(),
            "current_public_law_reference_hits": current.get("public_law_reference_hits", "").strip(),
            "current_public_law_reference_status": current.get("public_law_reference_status", "").strip(),
            "post_public_law_context_count": annual.get("post_public_law_context_count", "").strip(),
            "pre_normalized_text_sha256": review_row.get("pre_normalized_text_sha256", "").strip(),
            "post_normalized_text_sha256": review_row.get("post_normalized_text_sha256", "").strip(),
            "current_effective_text_review_status": status,
            "law_revision_effective_text_reviewed": reviewed,
            "effective_text_source_basis": (
                "official_olrc_current_us_code_page; "
                "official_olrc_current_public_law_note_scan; "
                "source_reviewed_target_section_diff"
            ),
            "effective_text_review_summary": summary,
            "public_law_causal_attribution": UNREVIEWED_CAUSATION_STATUS,
            "source_review_notes": (
                "Effective-text review is limited to official OLRC current source availability, "
                "current text hash/byte metadata, and current public-law note presence. It does "
                "not assign exclusive public-law causation."
            ),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["current_effective_text_review_status"] for row in rows)
    relationship_counts = Counter(row["codified_lineage_relationship"] for row in rows)
    reviewed_rows = [
        row for row in rows
        if row["law_revision_effective_text_reviewed"] == "1"
    ]
    public_law_note_rows = [
        row for row in rows
        if row["current_public_law_reference_status"] == "current_page_mentions_public_law"
    ]
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    total_current_bytes = sum(int_field(row, "current_official_text_bytes") for row in rows)
    causal_rows = [
        row for row in rows
        if row["public_law_causal_attribution"] != UNREVIEWED_CAUSATION_STATUS
    ]
    lines = [
        "# Statutory Lineage Effective-Text Review",
        "",
        "This report records a bounded effective-text source review for source-reviewed statutory-lineage target-section diff rows. It uses official OLRC current U.S. Code page metadata and current public-law note scans. It is not public-law causation, complete codified-lineage, implementation, court-review, welfare, or model-validation evidence.",
        "",
        f"- Effective-text review rows: {len(rows)}",
        f"- Public laws represented: {len(public_laws)}",
        f"- Law-revision effective-text reviewed rows: {len(reviewed_rows)}",
        f"- Current OLRC pages mentioning queued public law: {len(public_law_note_rows)}",
        f"- Official current text bytes represented: {total_current_bytes}",
        f"- Public-law causal-attribution reviewed rows: {len(causal_rows)}",
        "",
        "Effective-text review statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Codified-lineage relationships:"])
    for relationship, count in sorted(relationship_counts.items()):
        lines.append(f"- {relationship}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Target reference | Effective-text status | Public-law note | Reviewed |",
        "| ---: | --- | --- | --- | --- | --- | ---: |",
    ])
    for row in rows:
        lines.append(
            f"| {row['effective_text_review_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['current_effective_text_review_status']} | "
            f"{row['current_public_law_reference_status']} | "
            f"{row['law_revision_effective_text_reviewed']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
