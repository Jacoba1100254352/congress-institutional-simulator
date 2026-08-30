#!/usr/bin/env python3
"""Write a court-review statute-overlap linkage report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/court_law_linkage.csv")
OUT_CSV = Path("reports/court-law-linkage.csv")
OUT_MD = Path("reports/court-law-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make build-court-law-linkage-raw first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = part.strip()
        if clean and clean not in values:
            values.append(clean)
    return values


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    usc_rows = sum(1 for row in rows if row["court_usc_sections"])
    matched = [
        row for row in rows
        if row["linkage_status"] == "usc_section_authority_overlap"
    ]
    public_laws = {
        public_law
        for row in matched
        for public_law in split_values(row["public_law_numbers"])
    }
    bill_ids = {
        bill_id
        for row in matched
        for bill_id in split_values(row["bill_ids"])
    }
    sections = {
        section
        for row in matched
        for section in split_values(row["matched_usc_sections"])
    }
    invalidated_matched = sum(1 for row in matched if row["invalidated"] == "1")
    boundary = matched[0]["claim_boundary"] if matched else (
        "Bounded court-law linkage report; no authority-section overlaps are currently present."
    )
    lines = [
        "# Court-Law Linkage Report",
        "",
        "This report links SCDB merits-case rows to the current public-law evidence spine only through exact normalized U.S.C.-section overlaps with Federal Register authority citations. It is an authority-overlap audit, not proof that the listed case reviewed the listed public law.",
        "",
        f"- SCDB court rows checked: {len(rows)}",
        f"- Court rows with parsed U.S.C. sections: {usc_rows}",
        f"- Court rows with Federal Register authority-section overlaps: {len(matched)}",
        f"- Matched court rows coded invalidated by SCDB: {invalidated_matched}",
        f"- Public-law rows overlapped: {len(public_laws)}",
        f"- Bill IDs overlapped: {len(bill_ids)}",
        f"- Unique matched U.S.C. sections: {len(sections)}",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {boundary}",
        "",
        "| Case | Term | U.S.C. sections | Public laws | Bills | Status |",
        "| --- | ---: | --- | --- | --- | --- |",
    ])
    for row in matched[:40]:
        lines.append(
            f"| `{row['case_id']}` | {row['term'] or '---'} | "
            f"{row['matched_usc_sections'] or row['court_usc_sections'] or '---'} | "
            f"{row['public_law_numbers'] or '---'} | {row['bill_ids'] or '---'} | "
            f"{row['linkage_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} has no rows.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
