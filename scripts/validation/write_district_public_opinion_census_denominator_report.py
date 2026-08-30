#!/usr/bin/env python3
"""Write a bill-packet report for Census district denominators."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
DENOMINATORS = Path("data/validation/raw/district_public_opinion_census_denominators.csv")
OUT_CSV = Path("reports/district-public-opinion-census-denominators.csv")
OUT_MD = Path("reports/district-public-opinion-census-denominators.md")

FIELDNAMES = [
    "packet_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "denominator_district_count",
    "matched_denominator_districts",
    "missing_denominator_districts",
    "total_pop100",
    "total_hu100",
    "total_land_area_sq_km",
    "total_water_area_sq_km",
    "mean_population_density_per_sq_km",
    "mean_housing_unit_density_per_sq_km",
    "denominator_status",
    "denominator_source",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

MISSING_LINKS = (
    "bill_topic_public_opinion; survey_item_crosswalk; MRP_or_small_area_estimate; "
    "ACS_policy_specific_affected_population_denominator; ACS_veteran_population; "
    "ACS_income_poverty_employment; ACS_internet_subscription; "
    "ACS_citizenship_nativity_language; ACS_disability; ACS_industry_occupation; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "model_validation"
)

CLAIM_BOUNDARY = (
    "Census TIGERweb population and housing denominators are joined to source packets "
    "by sponsor district only; they are not bill-topic public support, not MRP or "
    "small-area estimates, not ACS policy-specific affected-population detail, not "
    "issue-specific affected-group support or harm, not public-benefit evidence, "
    "and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def parse_float(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def build_rows(
    packets: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    denominators = {row["district_id"]: row for row in denominator_rows if row.get("district_id")}
    rows: list[dict[str, str]] = []
    for packet in packets:
        districts = split_values(packet.get("sponsor_districts", ""))
        matched = [denominators[district] for district in districts if district in denominators]
        missing = [district for district in districts if district not in denominators]
        densities = [parse_float(row.get("population_density_per_sq_km")) for row in matched]
        housing_densities = [parse_float(row.get("housing_unit_density_per_sq_km")) for row in matched]
        status = (
            "official_tigerweb_population_housing_denominator"
            if matched and not missing
            else "partial_tigerweb_population_housing_denominator"
        )
        source_urls = sorted({row.get("source_url", "") for row in matched if row.get("source_url", "")})
        rows.append({
            "packet_rank": packet.get("packet_rank", ""),
            "bill_id": packet.get("bill_id", ""),
            "public_law_number": packet.get("public_law_number", ""),
            "policy_area": packet.get("policy_area", ""),
            "sponsor_districts": packet.get("sponsor_districts", ""),
            "denominator_district_count": str(len(matched)),
            "matched_denominator_districts": "; ".join(row["district_id"] for row in matched),
            "missing_denominator_districts": "; ".join(missing),
            "total_pop100": str(sum(parse_int(row.get("pop100")) for row in matched)),
            "total_hu100": str(sum(parse_int(row.get("hu100")) for row in matched)),
            "total_land_area_sq_km": f"{sum(parse_float(row.get('land_area_sq_km')) for row in matched):.3f}",
            "total_water_area_sq_km": f"{sum(parse_float(row.get('water_area_sq_km')) for row in matched):.3f}",
            "mean_population_density_per_sq_km": f"{mean(densities):.3f}",
            "mean_housing_unit_density_per_sq_km": f"{mean(housing_densities):.3f}",
            "denominator_status": status,
            "denominator_source": "U.S. Census Bureau TIGERweb 116th Congressional Districts, 2020 population and housing attributes",
            "evidence_layers": (
                "public_opinion_source_acquisition_packet; "
                "census_tigerweb_116th_district_population_housing_denominator"
            ),
            "missing_links": MISSING_LINKS,
            "source_url": "; ".join(source_urls),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    matched_rows = [
        row for row in rows
        if row["denominator_status"] == "official_tigerweb_population_housing_denominator"
    ]
    unique_districts = {
        district
        for row in rows
        for district in split_values(row.get("matched_denominator_districts", ""))
    }
    total_pop = sum(parse_int(row["total_pop100"]) for row in rows)
    total_hu = sum(parse_int(row["total_hu100"]) for row in rows)
    policy_areas = {row["policy_area"] for row in rows if row["policy_area"]}
    lines = [
        "# District Public-Opinion Census Denominators",
        "",
        "This report joins official Census TIGERweb 116th congressional-district population and housing denominators to the district public-opinion source-packet queue. It is district-frame evidence, not bill-topic support or affected-group harm evidence.",
        "",
        f"- Source packets with denominator rows: {len(matched_rows)} / {len(rows)}",
        f"- Unique sponsor districts with denominators: {len(unique_districts)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Sum of packet-level 2020 population denominators: {total_pop}",
        f"- Sum of packet-level 2020 housing-unit denominators: {total_hu}",
        "",
        "Claim boundary: this closes only the core district population/housing denominator sub-gap for queued sponsor districts. It does not provide ACS policy-specific affected-population detail, issue-specific bill support, MRP/small-area estimates, affected-group support or harm, public-benefit evidence, or model validation.",
        "",
        "| Packet | Bill ID | Policy area | Districts | Population | Housing units | Land sq km | Status |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['matched_denominator_districts']} | {row['total_pop100']} | "
            f"{row['total_hu100']} | {row['total_land_area_sq_km']} | "
            f"{row['denominator_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not SOURCE_PACKETS.exists():
        raise SystemExit(f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first.")
    if not DENOMINATORS.exists():
        raise SystemExit(f"{DENOMINATORS} is missing; run make build-district-public-opinion-census-denominators-raw first.")
    packets = read_csv(SOURCE_PACKETS)
    denominators = read_csv(DENOMINATORS)
    if not packets:
        raise SystemExit(f"{SOURCE_PACKETS} is empty.")
    if not denominators:
        raise SystemExit(f"{DENOMINATORS} is empty.")
    rows = build_rows(packets, denominators)
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
