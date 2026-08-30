#!/usr/bin/env python3
"""Write a bounded comparative-institution linkage report."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/comparative_institution_linkage.csv")
OUT_CSV = Path("reports/comparative-institution-linkage.csv")
OUT_MD = Path("reports/comparative-institution-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make build-comparative-institution-linkage-raw first.")
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
    matched = [row for row in rows if row["linkage_status"] == "comparative_institution_metadata"]
    chamber_counts = Counter(row["chamber_anchor"] for row in matched)
    district_counts = Counter(row["district_magnitude_band"] for row in matched)
    party_counts = Counter(row["party_system_band"] for row in matched)
    review_counts = Counter(row["judicial_review_band"] for row in matched)
    scenario_keys = {
        key
        for row in matched
        for key in split_values(row["matched_scenario_keys"])
    }
    boundary = matched[0]["claim_boundary"] if matched else (
        "Bounded comparative-institution linkage report; no simulator scenario-family metadata matches are present."
    )

    lines = [
        "# Comparative Institution Linkage Report",
        "",
        "This report links bounded QoG/OWID/V-Dem country-year institutional profiles to simulator scenario-family metadata anchors. It is a metadata bridge, not cross-national validation.",
        "",
        f"- Comparative country-year rows checked: {len(rows)}",
        f"- Rows with simulator scenario-family metadata anchors: {len(matched)}",
        f"- Countries represented: {len({row['iso3'] for row in matched if row['iso3']})}",
        f"- Unique simulator scenario anchors: {len(scenario_keys)}",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {boundary}",
        "",
        "Chamber anchors:",
    ])
    for chamber, count in sorted(chamber_counts.items()):
        lines.append(f"- {chamber}: {count}")
    lines.extend(["", "District-magnitude bands:"])
    for band, count in sorted(district_counts.items()):
        lines.append(f"- {band}: {count}")
    lines.extend(["", "Party-system bands:"])
    for band, count in sorted(party_counts.items()):
        lines.append(f"- {band}: {count}")
    lines.extend(["", "Judicial-review bands:"])
    for band, count in sorted(review_counts.items()):
        lines.append(f"- {band}: {count}")

    lines.extend([
        "",
        "| Country | Year | Chamber anchor | District band | Party band | Review band | Scenario anchors |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ])
    for row in matched[:40]:
        keys = "; ".join(split_values(row["matched_scenario_keys"])[:5])
        lines.append(
            f"| {row['country']} (`{row['iso3']}`) | {row['year']} | {row['chamber_anchor']} | "
            f"{row['district_magnitude_band']} | {row['party_system_band']} | "
            f"{row['judicial_review_band']} | {keys} |"
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
