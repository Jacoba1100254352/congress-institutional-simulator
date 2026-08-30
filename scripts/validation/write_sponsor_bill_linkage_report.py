#!/usr/bin/env python3
"""Write a sponsor-to-bill metadata linkage report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/sponsor_bill_linkage.csv")
OUT_CSV = Path("reports/sponsor-bill-linkage.csv")
OUT_MD = Path("reports/sponsor-bill-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make build-sponsor-bill-linkage-raw first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = part.strip()
        if clean and clean not in values:
            values.append(clean)
    return values


def as_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    matched = [row for row in rows if row["linkage_status"] == "sponsor_bill_metadata"]
    bill_ids = {
        bill_id
        for row in matched
        for bill_id in split_values(row["matched_bill_ids"])
    }
    public_laws = {
        public_law
        for row in matched
        for public_law in split_values(row["matched_public_law_numbers"])
    }
    policy_areas = {
        policy_area
        for row in matched
        for policy_area in split_values(row["matched_policy_areas"])
    }
    attached_bill_links = sum(as_int(row["matched_govinfo_bill_count"]) for row in matched)
    attached_enacted_links = sum(as_int(row["matched_govinfo_enacted_count"]) for row in matched)
    boundary = matched[0]["claim_boundary"] if matched else (
        "Bounded sponsor-bill linkage report; no sponsor bill-metadata matches are currently present."
    )
    lines = [
        "# Sponsor-Bill Linkage Report",
        "",
        "This report links sponsor aggregate rows to bounded public bill metadata by Bioguide sponsor ID. It is a metadata linkage audit, not proof of sponsor effectiveness or legislative quality.",
        "",
        f"- Sponsor rows checked: {len(rows)}",
        f"- Sponsor rows with bill metadata matches: {len(matched)}",
        f"- Unique matched bill IDs: {len(bill_ids)}",
        f"- Matched govinfo bill links attached: {attached_bill_links}",
        f"- Matched govinfo enacted bill links attached: {attached_enacted_links}",
        f"- Unique matched public laws: {len(public_laws)}",
        f"- Unique matched policy areas: {len(policy_areas)}",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {boundary}",
        "",
        "| Sponsor | Party | Aggregate bills | Matched bills | Public laws | Policy areas | Status |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for row in matched[:40]:
        policy_preview = "; ".join(split_values(row["matched_policy_areas"])[:3]) or "---"
        lines.append(
            f"| `{row['sponsor_id']}` | {row['party'] or '---'} | {row['introduced'] or '0'} | "
            f"{row['matched_govinfo_bill_count'] or '0'} | {row['matched_public_law_bill_count'] or '0'} | "
            f"{policy_preview} | {row['linkage_status']} |"
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
