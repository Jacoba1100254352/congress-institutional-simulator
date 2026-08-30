#!/usr/bin/env python3
"""Build official Census district population/housing denominators.

This fetches 116th congressional-district attributes from Census TIGERweb for
the sponsor districts in the district public-opinion source-packet queue. The
116th layer is the pre-redistricting district frame used by the 117th Congress
House bills in the current queue. It provides 2020 population and housing-unit
counts plus geography attributes; it is not ACS affected-group detail.
"""

from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
OUT_CSV = Path("data/validation/raw/district_public_opinion_census_denominators.csv")
OUT_METADATA = Path("data/validation/raw/district_public_opinion_census_denominators.metadata.md")
TIGERWEB_LAYER_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/"
    "TIGERweb/Legislative/MapServer/12/query"
)
TIGERWEB_LAYER_DOC = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/"
    "TIGERweb/Legislative/MapServer/12"
)
USER_AGENT = "congress-institutional-simulator-validation/0.8"
TIMEOUT_SECONDS = 20

STATE_FIPS = {
    "AL": "01",
    "AK": "02",
    "AZ": "04",
    "AR": "05",
    "CA": "06",
    "CO": "08",
    "CT": "09",
    "DE": "10",
    "DC": "11",
    "FL": "12",
    "GA": "13",
    "HI": "15",
    "ID": "16",
    "IL": "17",
    "IN": "18",
    "IA": "19",
    "KS": "20",
    "KY": "21",
    "LA": "22",
    "ME": "23",
    "MD": "24",
    "MA": "25",
    "MI": "26",
    "MN": "27",
    "MS": "28",
    "MO": "29",
    "MT": "30",
    "NE": "31",
    "NV": "32",
    "NH": "33",
    "NJ": "34",
    "NM": "35",
    "NY": "36",
    "NC": "37",
    "ND": "38",
    "OH": "39",
    "OK": "40",
    "OR": "41",
    "PA": "42",
    "RI": "44",
    "SC": "45",
    "SD": "46",
    "TN": "47",
    "TX": "48",
    "UT": "49",
    "VT": "50",
    "VA": "51",
    "WA": "53",
    "WV": "54",
    "WI": "55",
    "WY": "56",
}

FIELDNAMES = [
    "district_id",
    "state",
    "state_fips",
    "congressional_district",
    "tigerweb_layer",
    "cd_session",
    "geoid",
    "name",
    "pop100",
    "hu100",
    "arealand_sq_m",
    "areawater_sq_m",
    "land_area_sq_km",
    "water_area_sq_km",
    "population_density_per_sq_km",
    "housing_unit_density_per_sq_km",
    "intptlat",
    "intptlon",
    "centlat",
    "centlon",
    "denominator_status",
    "linkage_basis",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

MISSING_LINKS = (
    "ACS_veteran_population; ACS_income_poverty_employment; "
    "ACS_internet_subscription; ACS_citizenship_nativity_language; "
    "ACS_disability; ACS_industry_occupation; bill_topic_public_opinion; "
    "MRP_or_small_area_estimate; issue_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; model_validation"
)

CLAIM_BOUNDARY = (
    "Official Census TIGERweb 116th congressional-district 2020 population, "
    "housing, and geography denominator only; not ACS socioeconomic or "
    "demographic affected-population detail, not bill-topic public support, "
    "not MRP or small-area estimates, not issue-specific affected-group "
    "support or harm, not public-benefit evidence, and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sponsor_districts(rows: list[dict[str, str]]) -> list[str]:
    values: set[str] = set()
    for row in rows:
        for value in row.get("sponsor_districts", "").split(";"):
            district_id = value.strip()
            if district_id:
                values.add(district_id)
    return sorted(values)


def district_parts(district_id: str) -> tuple[str, str, str]:
    state, district = district_id.split("-", maxsplit=1)
    state = state.upper()
    if state not in STATE_FIPS:
        raise ValueError(f"unknown state abbreviation in district_id {district_id!r}")
    try:
        district_number = int(district)
    except ValueError as exc:
        raise ValueError(f"invalid congressional district in {district_id!r}") from exc
    if district_number <= 0:
        district_number = 1
    return state, STATE_FIPS[state], f"{district_number:02d}"


def tigerweb_request_url(state_fips: str, district_code: str) -> str:
    where = f"STATE='{state_fips}' AND BASENAME='{int(district_code)}'"
    return f"{TIGERWEB_LAYER_URL}?{urlencode({
        'where': where,
        'outFields': '*',
        'returnGeometry': 'false',
        'f': 'json',
    })}"


def fetch_district(district_id: str) -> dict[str, object]:
    _, state_fips, district_code = district_parts(district_id)
    url = tigerweb_request_url(state_fips, district_code)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.load(response)
    features = payload.get("features")
    if not isinstance(features, list) or len(features) != 1:
        raise RuntimeError(f"TIGERweb returned {len(features) if isinstance(features, list) else 0} rows for {district_id}")
    attrs = features[0].get("attributes")
    if not isinstance(attrs, dict):
        raise RuntimeError(f"TIGERweb row for {district_id} has no attributes")
    return attrs


def parse_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def parse_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def density(numerator: int, area_sq_km: float) -> str:
    return f"{numerator / area_sq_km:.3f}" if area_sq_km > 0 else ""


def build_rows(district_ids: list[str], sleep_seconds: float) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, district_id in enumerate(district_ids):
        state, state_fips, district_code = district_parts(district_id)
        attrs = fetch_district(district_id)
        pop100 = parse_int(attrs.get("POP100"))
        hu100 = parse_int(attrs.get("HU100"))
        land_sq_m = parse_int(attrs.get("AREALAND"))
        water_sq_m = parse_int(attrs.get("AREAWATER"))
        land_sq_km = land_sq_m / 1_000_000
        water_sq_km = water_sq_m / 1_000_000
        source_url = tigerweb_request_url(state_fips, district_code)
        rows.append({
            "district_id": district_id,
            "state": state,
            "state_fips": state_fips,
            "congressional_district": district_code,
            "tigerweb_layer": "TIGERweb Legislative MapServer layer 12",
            "cd_session": str(attrs.get("CDSESSN") or "116"),
            "geoid": str(attrs.get("GEOID") or ""),
            "name": str(attrs.get("NAME") or ""),
            "pop100": str(pop100),
            "hu100": str(hu100),
            "arealand_sq_m": str(land_sq_m),
            "areawater_sq_m": str(water_sq_m),
            "land_area_sq_km": f"{land_sq_km:.3f}",
            "water_area_sq_km": f"{water_sq_km:.3f}",
            "population_density_per_sq_km": density(pop100, land_sq_km),
            "housing_unit_density_per_sq_km": density(hu100, land_sq_km),
            "intptlat": str(attrs.get("INTPTLAT") or ""),
            "intptlon": str(attrs.get("INTPTLON") or ""),
            "centlat": str(attrs.get("CENTLAT") or ""),
            "centlon": str(attrs.get("CENTLON") or ""),
            "denominator_status": "official_tigerweb_population_housing_denominator",
            "linkage_basis": (
                "district_public_opinion_source_packets.sponsor_districts -> "
                "Census TIGERweb 116th congressional district STATE/BASENAME"
            ),
            "evidence_layers": "census_tigerweb_116th_district_population_housing_denominator",
            "missing_links": MISSING_LINKS,
            "source_url": source_url,
            "claim_boundary": CLAIM_BOUNDARY,
        })
        if sleep_seconds > 0 and index < len(district_ids) - 1:
            time.sleep(sleep_seconds)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], districts: list[str]) -> None:
    total_pop = sum(parse_int(row["pop100"]) for row in rows)
    total_hu = sum(parse_int(row["hu100"]) for row in rows)
    write_reproducible_metadata(
        OUT_METADATA,
        "# District Public-Opinion Census Denominators\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- District queue: `{SOURCE_PACKETS}`.\n"
        f"- Census TIGERweb 116th Congressional District layer: {TIGERWEB_LAYER_DOC}.\n\n"
        "Transformation:\n\n"
        "- Extracts unique sponsor districts from the district public-opinion source-packet queue.\n"
        "- Queries Census TIGERweb Legislative MapServer layer 12 by state FIPS and congressional district basename.\n"
        "- Preserves 2020 population count, 2020 housing-unit count, land/water area, centroid, and internal point fields.\n"
        "- Uses the 116th congressional-district layer because the current queue is built from 117th Congress bills, before the 118th/119th post-2020 redistricting frame.\n"
        "- Does not fetch ACS socioeconomic, veteran, citizenship, language, disability, industry, employment, income, internet-access, survey, or MRP estimates.\n\n"
        "Rows:\n\n"
        f"- Requested sponsor districts: {len(districts)}.\n"
        f"- Retrieved denominator rows: {len(rows)}.\n"
        f"- Total represented 2020 population across retrieved sponsor districts: {total_pop}.\n"
        f"- Total represented 2020 housing units across retrieved sponsor districts: {total_hu}.\n"
        f"- States represented: {len({row['state'] for row in rows})}.\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def main() -> int:
    if not SOURCE_PACKETS.exists():
        raise SystemExit(f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first.")
    packets = read_csv(SOURCE_PACKETS)
    districts = sponsor_districts(packets)
    if not districts:
        raise SystemExit(f"{SOURCE_PACKETS} has no sponsor_districts values.")
    rows = build_rows(districts, sleep_seconds=0.05)
    write_csv(rows)
    write_metadata(rows, districts)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
