#!/usr/bin/env python3
"""Build a bounded comparative-institution to simulator-spec linkage cache."""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


RAW = Path("data/validation/raw/comparative_institutions.csv")
OUT_CSV = Path("data/validation/raw/comparative_institution_linkage.csv")
OUT_METADATA = Path("data/validation/raw/comparative_institution_linkage.metadata.md")

CLAIM_BOUNDARY = (
    "Bounded comparative-institution profile to simulator scenario-family metadata only; "
    "not observed law-output productivity, not bicameral disagreement evidence, not "
    "country-level institutional fit, not adoption evidence, not welfare, causal-effect, "
    "or model validation evidence."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make build-comparative-institutions-raw first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], field: str) -> float:
    try:
        return float(row.get(field, "") or "0")
    except ValueError:
        return 0.0


def as_int(row: dict[str, str], field: str) -> int:
    try:
        return int(float(row.get(field, "") or "0"))
    except ValueError:
        return 0


def district_magnitude_band(value: float) -> str:
    if value <= 1.5:
        return "single_member_or_near_single_member"
    if value < 6.0:
        return "moderate_magnitude"
    return "high_magnitude"


def party_system_band(value: float) -> str:
    if value <= 2.5:
        return "two_party_or_low_fragmentation"
    if value <= 4.5:
        return "moderate_multipartism"
    return "high_fragmentation"


def judicial_review_band(value: float) -> str:
    if value < 0.4:
        return "weak_judicial_constraints"
    if value < 0.7:
        return "moderate_judicial_constraints"
    return "strong_judicial_constraints"


def legislative_constraint_band(value: float) -> str:
    if value < 0.4:
        return "low_legislative_constraints"
    if value < 0.7:
        return "moderate_legislative_constraints"
    return "high_legislative_constraints"


def chamber_anchor(chambers: int) -> str:
    if chambers >= 2:
        return "bicameral"
    if chambers == 1:
        return "unicameral"
    return "no_effective_chamber"


def scenario_keys(
    chamber: str,
    district_band: str,
    party_band: str,
    review_band: str,
    constraint_band: str,
) -> list[str]:
    keys: list[str] = []
    if chamber == "bicameral":
        keys.extend(["bicameral-majority", "current-system"])
        if constraint_band == "high_legislative_constraints":
            keys.append("upper-absolute-veto")
        elif constraint_band == "moderate_legislative_constraints":
            keys.append("suspensive-veto-upper")
        else:
            keys.append("lower-override-upper")
    elif chamber == "unicameral":
        keys.extend(["simple-majority", "equal-population-unicameral"])
    else:
        keys.append("principles-resolution-routing")

    if district_band == "high_magnitude":
        keys.append("proportional-house-majority")
    elif district_band == "single_member_or_near_single_member":
        keys.append("equal-population-unicameral")

    if party_band == "high_fragmentation":
        keys.append("limited-navette-upper" if chamber == "bicameral" else "committee-priority-queue-majority")

    if review_band == "strong_judicial_constraints":
        keys.extend(["exante-clearance-majority", "independent-insulation-majority"])
    elif review_band == "moderate_judicial_constraints":
        keys.append("exante-advisory-majority")

    deduped: list[str] = []
    for key in keys:
        if key not in deduped:
            deduped.append(key)
    return deduped


def family_label(chamber: str, district_band: str, party_band: str, review_band: str) -> str:
    return ";".join([chamber, district_band, party_band, review_band])


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in rows:
        chambers = as_int(row, "chambers")
        district_magnitude = as_float(row, "district_magnitude")
        party_fragmentation = as_float(row, "party_fragmentation")
        judicial_review = as_float(row, "judicial_review")
        legislative_constraint_proxy = as_float(row, "legislative_productivity")
        chamber = chamber_anchor(chambers)
        district_band = district_magnitude_band(district_magnitude)
        party_band = party_system_band(party_fragmentation)
        review_band = judicial_review_band(judicial_review)
        constraint_band = legislative_constraint_band(legislative_constraint_proxy)
        keys = scenario_keys(chamber, district_band, party_band, review_band, constraint_band)
        output.append({
            "iso3": row.get("iso3", "").strip(),
            "country": row.get("country", "").strip(),
            "year": row.get("year", "").strip(),
            "chambers": row.get("chambers", "").strip(),
            "district_magnitude": row.get("district_magnitude", "").strip(),
            "party_fragmentation": row.get("party_fragmentation", "").strip(),
            "judicial_review": row.get("judicial_review", "").strip(),
            "legislative_constraint_proxy": row.get("legislative_productivity", "").strip(),
            "linkage_status": "comparative_institution_metadata" if keys else "unmatched",
            "matched_institution_family": family_label(chamber, district_band, party_band, review_band),
            "matched_scenario_keys": ";".join(keys),
            "matched_scenario_count": str(len(keys)),
            "chamber_anchor": chamber,
            "district_magnitude_band": district_band,
            "party_system_band": party_band,
            "judicial_review_band": review_band,
            "legislative_constraint_band": constraint_band,
            "evidence_layers": (
                "qog_des_polcon_country_year_profile;"
                "owid_vdem_country_year_profile;"
                "simulator_scenario_family_anchor"
            ),
            "missing_links": (
                "observed_law_output;ipu_or_parlgov_chamber_identifier;"
                "bicameral_disagreement;country_year_bill_census"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return sorted(output, key=lambda item: (item["country"], item["year"], item["iso3"]))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(source_rows: list[dict[str, str]], output_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in output_rows)
    chamber_counts = Counter(row["chamber_anchor"] for row in output_rows)
    scenario_keys_seen = {
        key
        for row in output_rows
        for key in row["matched_scenario_keys"].split(";")
        if key
    }
    lines = [
        "# Comparative Institution Linkage Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Sources:",
        "",
        "- `data/validation/raw/comparative_institutions.csv`.",
        "- Existing simulator scenario-family keys used as metadata anchors.",
        "",
        "Transformation:",
        "",
        "- Country-year rows are classified into chamber, district-magnitude, party-system, judicial-review, and legislative-constraint bands.",
        "- Bands are mapped to a bounded set of simulator scenario keys that represent nearby institutional mechanisms.",
        "- `legislative_constraint_proxy` carries the existing V-Dem legislative-constraints proxy; it is not observed law-output productivity.",
        "",
        "Rows:",
        "",
        f"- Source comparative rows read: {len(source_rows)}",
        f"- Linkage rows written: {len(output_rows)}",
        f"- Countries represented: {len({row['iso3'] for row in output_rows if row['iso3']})}",
        f"- Unique simulator scenario anchors: {len(scenario_keys_seen)}",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Chamber anchors:"])
    for chamber, count in sorted(chamber_counts.items()):
        lines.append(f"- {chamber}: {count}")
    lines.extend([
        "",
        "Claim boundary:",
        "",
        CLAIM_BOUNDARY,
        "",
    ])
    OUT_METADATA.write_text("\n".join(lines))


def main() -> int:
    source_rows = read_csv(RAW)
    if not source_rows:
        raise SystemExit(f"{RAW} has no rows.")
    rows = build_rows(source_rows)
    if not rows:
        raise SystemExit("No comparative-institution linkage rows were produced.")
    write_csv(rows)
    write_metadata(source_rows, rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
