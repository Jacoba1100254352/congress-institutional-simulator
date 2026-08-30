#!/usr/bin/env python3
"""Write the OLRC annual text-diff cue scan report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_olrc_annual_text_diff.csv")
HISTORICAL_SCAN = Path("reports/statutory-lineage-olrc-historical-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
OUT_MD = Path("reports/statutory-lineage-olrc-annual-text-diff.md")

CLAIM_BOUNDARY = (
    "Official OLRC annual-page text-diff cue scan only. Rows preserve bounded "
    "post-edition public-law context snippets, raw-hash comparisons, normalized "
    "section-text signatures, and bounded first-change windows for annual U.S. "
    "Code pages, but they do not establish source-reviewed codified U.S.C. "
    "lineage, public-law causation, adjudicated target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], historical_rows: list[dict[str, str]]) -> None:
    cue_statuses = Counter(row["automated_diff_cue_status"] for row in rows)
    section_change_statuses = Counter(row["section_change_cue_status"] for row in rows)
    normalized_hash_statuses = Counter(row["normalized_text_hash_status"] for row in rows)
    pre_anchor_statuses = Counter(row["pre_section_anchor_status"] for row in rows)
    post_anchor_statuses = Counter(row["post_section_anchor_status"] for row in rows)
    priorities = Counter(row["manual_review_priority"] for row in rows)
    evidence_statuses = Counter(row["lineage_evidence_status"] for row in rows)
    represented_bills = {row["bill_id"] for row in rows if row["bill_id"]}
    hash_verified = [
        row
        for row in rows
        if row["pre_hash_matches_historical_scan"] == "yes"
        and row["post_hash_matches_historical_scan"] == "yes"
    ]
    post_only = [
        row
        for row in rows
        if row["automated_diff_cue_status"] == "post_only_public_law_marker_on_changed_annual_page"
    ]
    normalized_changed = [
        row
        for row in rows
        if row["normalized_text_hash_status"] == "pre_post_normalized_text_changed"
    ]
    change_window_rows = [
        row
        for row in rows
        if row["first_changed_text_pre_window"] and row["first_changed_text_post_window"]
    ]
    snippet_rows = [row for row in rows if int(row["post_public_law_context_count"] or "0") > 0]

    lines = [
        "# Statutory Lineage OLRC Annual Text-Diff Cues",
        "",
        "This report summarizes bounded text-diff cues from official OLRC annual U.S. Code pages for statutory-lineage candidates. It records post-edition public-law context snippets, raw-hash comparisons, normalized section text signatures, and bounded first-change windows, not source-reviewed codified-lineage evidence.",
        "",
        f"- Annual text-diff cue rows: {len(rows)} / {len(historical_rows)}",
        f"- Bills covered: {len(represented_bills)}",
        f"- Rows with pre/post hashes matching historical scan: {len(hash_verified)}",
        f"- Rows with normalized pre/post section text changes: {len(normalized_changed)}",
        f"- Rows with bounded first-change windows: {len(change_window_rows)}",
        f"- Rows with pre-edition target section anchors: {pre_anchor_statuses['section_anchor_found']}",
        f"- Rows with post-edition target section anchors: {post_anchor_statuses['section_anchor_found']}",
        f"- Rows with post-only public-law marker cues: {len(post_only)}",
        f"- Rows with bounded post public-law context snippets: {len(snippet_rows)}",
        "",
        "Normalized text hash statuses:",
    ]
    for status, count in sorted(normalized_hash_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "Section change cue statuses:",
        ]
    )
    for status, count in sorted(section_change_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "Pre-edition section anchor statuses:",
        ]
    )
    for status, count in sorted(pre_anchor_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "Post-edition section anchor statuses:",
        ]
    )
    for status, count in sorted(post_anchor_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "Automated diff cue statuses:",
        ]
    )
    for status, count in sorted(cue_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Manual review priorities:")
    for status, count in sorted(priorities.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Lineage evidence statuses:")
    for status, count in sorted(evidence_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | Section change status | Delta hits | First post-change window |",
            "| ---: | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in rows[:80]:
        change_window = row["first_changed_text_post_window"] or row["post_public_law_context_snippets"]
        if len(change_window) > 180:
            change_window = change_window[:177].rstrip() + "..."
        lines.append(
            f"| {row['text_diff_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['section_change_cue_status']} | "
            f"{row['public_law_reference_hit_delta']} | {change_window or '---'} |"
        )
    if len(rows) > 80:
        lines.extend(
            [
                "",
                f"CSV contains {len(rows) - 80} additional annual text-diff cue rows not shown in the markdown table.",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(
            f"{RAW} is missing; run make build-statutory-lineage-olrc-annual-text-diff-raw first."
        )
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    historical_rows = read_csv(HISTORICAL_SCAN)
    if not historical_rows:
        raise SystemExit(
            f"{HISTORICAL_SCAN} is missing or empty; run make statutory-lineage-olrc-historical-scan first."
        )
    write_csv(rows)
    write_md(rows, historical_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
