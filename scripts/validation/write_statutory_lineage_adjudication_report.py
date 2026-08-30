#!/usr/bin/env python3
"""Write the statutory-lineage OLRC marker adjudication report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/statutory_lineage_adjudication.csv")
TEXT_DIFF = Path("reports/statutory-lineage-olrc-annual-text-diff.csv")
OUT_CSV = Path("reports/statutory-lineage-adjudication.csv")
OUT_MD = Path("reports/statutory-lineage-adjudication.md")

CLAIM_BOUNDARY = (
    "Official OLRC public-law marker adjudication only. Rows classify annual "
    "U.S. Code pages where the queued public law is absent from the pre-edition, "
    "present in the post-edition, and paired with a normalized section-text "
    "change. This is codified-lineage marker evidence only; it does not establish "
    "source-reviewed target-section text diffs, public-law causal attribution, "
    "effective statutory text, implementation outcomes, court review, welfare, "
    "causal effects, or model validation."
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


def write_md(rows: list[dict[str, str]], text_diff_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["lineage_adjudication_status"] for row in rows)
    strength_counts = Counter(row["lineage_marker_strength"] for row in rows)
    evidence_statuses = Counter(row["lineage_evidence_status"] for row in rows)
    marker_rows = [row for row in rows if row["codified_lineage_marker"] == "1"]
    marker_bills = {row["bill_id"] for row in marker_rows if row["bill_id"]}
    marker_public_laws = {row["public_law_number"] for row in marker_rows if row["public_law_number"]}
    pre_anchor_markers = [
        row for row in marker_rows if row["pre_section_anchor_status"] == "section_anchor_found"
    ]
    post_anchor_markers = [
        row for row in marker_rows if row["post_section_anchor_status"] == "section_anchor_found"
    ]
    lines = [
        "# Statutory Lineage Adjudication",
        "",
        "This report classifies official OLRC annual text-diff cue rows into conservative codified-lineage marker evidence. It is not a source-reviewed target-section text-diff report.",
        "",
        f"- Adjudication rows: {len(rows)} / {len(text_diff_rows)}",
        f"- Rows with codified-lineage marker evidence: {len(marker_rows)}",
        f"- Bills with codified-lineage marker evidence: {len(marker_bills)}",
        f"- Public laws with codified-lineage marker evidence: {len(marker_public_laws)}",
        f"- Marker rows with pre-edition section anchors: {len(pre_anchor_markers)}",
        f"- Marker rows with post-edition section anchors: {len(post_anchor_markers)}",
        "",
        "Lineage adjudication statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Lineage marker strengths:"])
    for strength, count in sorted(strength_counts.items()):
        lines.append(f"- {strength}: {count}")
    lines.extend(["", "Lineage evidence statuses:"])
    for status, count in sorted(evidence_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | Marker | Status | Strength | Diff status |",
            "| ---: | --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in rows[:100]:
        lines.append(
            f"| {row['lineage_adjudication_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['codified_lineage_marker']} | {row['lineage_adjudication_status']} | "
            f"{row['lineage_marker_strength']} | {row['target_section_diff_status']} |"
        )
    if len(rows) > 100:
        lines.extend([
            "",
            f"CSV contains {len(rows) - 100} additional adjudication rows not shown in the markdown table.",
        ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(
            f"{RAW} is missing; run make build-statutory-lineage-adjudication-raw first."
        )
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    text_diff_rows = read_csv(TEXT_DIFF)
    if not text_diff_rows:
        raise SystemExit(
            f"{TEXT_DIFF} is missing or empty; run make statutory-lineage-olrc-annual-text-diff first."
        )
    write_csv(rows)
    write_md(rows, text_diff_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
