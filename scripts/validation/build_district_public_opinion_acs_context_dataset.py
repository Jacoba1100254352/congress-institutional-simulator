#!/usr/bin/env python3
"""Build official ACS district context for public-opinion source packets.

This extracts a bounded set of 2017-2021 ACS 5-year detailed-table estimates
for the 116th congressional districts used by the current 117th Congress
district public-opinion source-packet queue. It uses the Census table-based
Summary File, not the keyed Census API. The rows are broad district context
only; they are not bill-topic support estimates or bill-specific harm evidence.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata
from urllib.request import Request, urlopen


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
OUT_CSV = Path("data/validation/raw/district_public_opinion_acs_context.csv")
OUT_METADATA = Path("data/validation/raw/district_public_opinion_acs_context.metadata.md")

SUMMARY_FILE_BASE = (
    "https://www2.census.gov/programs-surveys/acs/summary_file/2021/"
    "table-based-SF"
)
GEOS_URL = f"{SUMMARY_FILE_BASE}/documentation/Geos20215YR.txt"
DATA_BASE_URL = f"{SUMMARY_FILE_BASE}/data/5YRData"
USER_AGENT = "congress-institutional-simulator-validation/0.9"
TIMEOUT_SECONDS = 120
ACS_SPECIAL_NUMERIC_VALUES = {
    -222222222.0,
    -333333333.0,
    -555555555.0,
    -666666666.0,
    -777777777.0,
    -888888888.0,
    -999999999.0,
}

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

TABLE_COLUMNS: dict[str, dict[str, str]] = {
    "b02001": {
        "race_total_population": "B02001_E001",
        "white_alone": "B02001_E002",
        "black_alone": "B02001_E003",
        "asian_alone": "B02001_E005",
    },
    "b03003": {
        "hispanic_total_population": "B03003_E001",
        "hispanic_or_latino": "B03003_E003",
    },
    "b05002": {
        "nativity_citizenship_total_population": "B05002_E001",
        "foreign_born": "B05002_E013",
        "naturalized_citizen": "B05002_E014",
        "not_us_citizen": "B05002_E021",
    },
    "b16001": {
        "language_population_5_plus": "B16001_E001",
        "speak_only_english": "B16001_E002",
    },
    "b18101": {
        "disability_universe": "B18101_E001",
        "male_under_5_with_disability": "B18101_E004",
        "male_5_17_with_disability": "B18101_E007",
        "male_18_34_with_disability": "B18101_E010",
        "male_35_64_with_disability": "B18101_E013",
        "male_65_74_with_disability": "B18101_E016",
        "male_75_plus_with_disability": "B18101_E019",
        "female_under_5_with_disability": "B18101_E023",
        "female_5_17_with_disability": "B18101_E026",
        "female_18_34_with_disability": "B18101_E029",
        "female_35_64_with_disability": "B18101_E032",
        "female_65_74_with_disability": "B18101_E035",
        "female_75_plus_with_disability": "B18101_E038",
    },
    "b19013": {
        "median_household_income": "B19013_E001",
    },
    "c17002": {
        "poverty_ratio_universe": "C17002_E001",
        "income_under_50pct_poverty": "C17002_E002",
        "income_50_to_99pct_poverty": "C17002_E003",
    },
    "b21001": {
        "civilian_population_18_plus": "B21001_E001",
        "veterans": "B21001_E002",
    },
    "b23025": {
        "population_16_plus": "B23025_E001",
        "civilian_labor_force": "B23025_E003",
        "employed": "B23025_E004",
        "unemployed": "B23025_E005",
        "not_in_labor_force": "B23025_E007",
    },
    "b28002": {
        "households": "B28002_E001",
        "with_internet_subscription": "B28002_E002",
        "no_internet_access": "B28002_E013",
    },
}

DIRECT_ESTIMATE_FIELDS = [
    "race_total_population",
    "white_alone",
    "black_alone",
    "asian_alone",
    "hispanic_total_population",
    "hispanic_or_latino",
    "nativity_citizenship_total_population",
    "foreign_born",
    "naturalized_citizen",
    "not_us_citizen",
    "language_population_5_plus",
    "speak_only_english",
    "disability_universe",
    "median_household_income",
    "poverty_ratio_universe",
    "income_under_50pct_poverty",
    "income_50_to_99pct_poverty",
    "civilian_population_18_plus",
    "veterans",
    "population_16_plus",
    "civilian_labor_force",
    "employed",
    "unemployed",
    "not_in_labor_force",
    "households",
    "with_internet_subscription",
    "no_internet_access",
]

DISABILITY_COMPONENT_FIELDS = [
    "male_under_5_with_disability",
    "male_5_17_with_disability",
    "male_18_34_with_disability",
    "male_35_64_with_disability",
    "male_65_74_with_disability",
    "male_75_plus_with_disability",
    "female_under_5_with_disability",
    "female_5_17_with_disability",
    "female_18_34_with_disability",
    "female_35_64_with_disability",
    "female_65_74_with_disability",
    "female_75_plus_with_disability",
]

FIELDNAMES = [
    "district_id",
    "state",
    "state_fips",
    "congressional_district",
    "acs_geoid",
    "tl_geoid",
    "acs_name",
    "acs_dataset",
    "acs_vintage",
    "congressional_district_session",
    "acs_context_status",
    "linkage_basis",
]

for field in DIRECT_ESTIMATE_FIELDS + [
    "below_poverty",
    "non_english_home_language",
    "with_disability",
]:
    FIELDNAMES.extend([f"{field}_est", f"{field}_moe"])

FIELDNAMES.extend([
    "veteran_share",
    "foreign_born_share",
    "noncitizen_share",
    "naturalized_share",
    "non_english_home_language_share",
    "with_disability_share",
    "below_poverty_share",
    "unemployment_rate",
    "labor_force_participation_rate",
    "internet_subscription_share",
    "no_internet_access_share",
    "white_alone_share",
    "black_alone_share",
    "asian_alone_share",
    "hispanic_or_latino_share",
    "source_tables",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
])

MISSING_LINKS = (
    "bill_topic_public_opinion; survey_item_crosswalk; MRP_or_small_area_estimate; "
    "bill_text_specific_affected_population_denominator; issue_specific_affected_group_support; "
    "affected_group_harm; public_benefit; causal_representation; model_validation"
)

CLAIM_BOUNDARY = (
    "Official ACS 2017-2021 5-year broad congressional-district demographic, "
    "economic, language, disability, internet, citizenship, and veteran context "
    "only; not bill-topic public support, not MRP or small-area estimates, not "
    "bill-text-specific affected-population definitions, not issue-specific "
    "affected-group support or harm, not public-benefit evidence, and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def sponsor_districts(rows: list[dict[str, str]]) -> list[str]:
    values = {
        district_id
        for row in rows
        for district_id in split_values(row.get("sponsor_districts", ""))
    }
    return sorted(values)


def district_parts(district_id: str) -> tuple[str, str, str]:
    state, district = district_id.split("-", maxsplit=1)
    state = state.upper()
    if state not in STATE_FIPS:
        raise ValueError(f"unknown state abbreviation in district_id {district_id!r}")
    district_number = int(district)
    return state, STATE_FIPS[state], f"{district_number:02d}"


def request_url(url: str):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    return urlopen(request, timeout=TIMEOUT_SECONDS)


def existing_output_matches(district_ids: list[str]) -> bool:
    if not OUT_CSV.exists():
        return False
    try:
        rows = read_csv(OUT_CSV)
    except (OSError, csv.Error):
        return False
    if not rows:
        return False
    if set(rows[0]) < set(FIELDNAMES):
        return False
    return {row.get("district_id", "") for row in rows} == set(district_ids)


def load_geographies(district_ids: list[str]) -> dict[str, dict[str, str]]:
    expected_by_key: dict[tuple[str, str], str] = {}
    for district_id in district_ids:
        _, state_fips, district_code = district_parts(district_id)
        expected_by_key[(state_fips, district_code)] = district_id

    geographies: dict[str, dict[str, str]] = {}
    with request_url(GEOS_URL) as response:
        wrapper = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(wrapper, delimiter="|")
        for row in reader:
            if row.get("SUMLEVEL") != "500":
                continue
            key = (row.get("STATE", ""), row.get("CDCURR", ""))
            district_id = expected_by_key.get(key)
            if district_id:
                geographies[district_id] = row
                if len(geographies) == len(expected_by_key):
                    break
    missing = sorted(set(district_ids) - set(geographies))
    if missing:
        raise RuntimeError(f"ACS geography file is missing queued districts: {missing}")
    return geographies


def moe_column(column: str) -> str:
    return column.replace("_E", "_M", 1)


def table_url(table: str) -> str:
    return f"{DATA_BASE_URL}/acsdt5y2021-{table}.dat"


def load_table_rows(acs_geoids: set[str]) -> dict[str, dict[str, str]]:
    values_by_geoid: dict[str, dict[str, str]] = {geoid: {} for geoid in acs_geoids}
    for table, field_map in TABLE_COLUMNS.items():
        wanted_columns = set(field_map.values())
        wanted_columns.update(moe_column(column) for column in field_map.values())
        with request_url(table_url(table)) as response:
            wrapper = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(wrapper, delimiter="|")
            found: set[str] = set()
            for row in reader:
                geoid = row.get("GEO_ID", "")
                if geoid not in acs_geoids:
                    continue
                values_by_geoid[geoid].update({
                    column: row.get(column, "")
                    for column in wanted_columns
                })
                found.add(geoid)
                if len(found) == len(acs_geoids):
                    break
        missing = acs_geoids - found
        if missing:
            raise RuntimeError(f"{table_url(table)} missing ACS rows for {sorted(missing)}")
    return values_by_geoid


def parse_number(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if parsed in ACS_SPECIAL_NUMERIC_VALUES:
        return None
    return parsed


def fmt_number(value: float | None) -> str:
    if value is None:
        return ""
    if math.isfinite(value) and abs(value - round(value)) < 0.0000001:
        return str(int(round(value)))
    return f"{value:.3f}"


def estimate(values: dict[str, str], column: str) -> float | None:
    return parse_number(values.get(column))


def moe(values: dict[str, str], column: str) -> float | None:
    return parse_number(values.get(moe_column(column)))


def sum_estimates(values: dict[str, str], fields: list[str]) -> float | None:
    total = 0.0
    seen = False
    column_by_field = {
        field: column
        for field_map in TABLE_COLUMNS.values()
        for field, column in field_map.items()
    }
    for field in fields:
        value = estimate(values, column_by_field[field])
        if value is not None:
            total += value
            seen = True
    return total if seen else None


def rss_moes(values: dict[str, str], fields: list[str]) -> float | None:
    total = 0.0
    seen = False
    column_by_field = {
        field: column
        for field_map in TABLE_COLUMNS.values()
        for field, column in field_map.items()
    }
    for field in fields:
        value = moe(values, column_by_field[field])
        if value is not None:
            total += value * value
            seen = True
    return math.sqrt(total) if seen else None


def share(numerator: float | None, denominator: float | None) -> str:
    if numerator is None or denominator is None or denominator <= 0:
        return ""
    return f"{numerator / denominator:.4f}"


def build_rows(
    district_ids: list[str],
    geographies: dict[str, dict[str, str]],
    values_by_geoid: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    column_by_field = {
        field: column
        for field_map in TABLE_COLUMNS.values()
        for field, column in field_map.items()
    }
    source_tables = "; ".join(sorted(TABLE_COLUMNS))
    source_urls = "; ".join([GEOS_URL] + [table_url(table) for table in sorted(TABLE_COLUMNS)])
    rows: list[dict[str, str]] = []
    for district_id in district_ids:
        state, state_fips, district_code = district_parts(district_id)
        geo = geographies[district_id]
        values = values_by_geoid[geo["GEO_ID"]]
        row = {
            "district_id": district_id,
            "state": state,
            "state_fips": state_fips,
            "congressional_district": district_code,
            "acs_geoid": geo["GEO_ID"],
            "tl_geoid": geo.get("TL_GEO_ID", ""),
            "acs_name": geo.get("NAME", ""),
            "acs_dataset": "ACS 2017-2021 5-year detailed tables, table-based Summary File",
            "acs_vintage": "2017-2021",
            "congressional_district_session": "116",
            "acs_context_status": "official_acs_2017_2021_5yr_district_context",
            "linkage_basis": (
                "district_public_opinion_source_packets.sponsor_districts -> "
                "ACS 2017-2021 5-year congressional district GEO_ID"
            ),
        }
        for field in DIRECT_ESTIMATE_FIELDS:
            column = column_by_field[field]
            row[f"{field}_est"] = fmt_number(estimate(values, column))
            row[f"{field}_moe"] = fmt_number(moe(values, column))

        below_poverty = sum_estimates(
            values,
            ["income_under_50pct_poverty", "income_50_to_99pct_poverty"],
        )
        below_poverty_moe = rss_moes(
            values,
            ["income_under_50pct_poverty", "income_50_to_99pct_poverty"],
        )
        language_total = estimate(values, column_by_field["language_population_5_plus"])
        english_only = estimate(values, column_by_field["speak_only_english"])
        language_total_moe = moe(values, column_by_field["language_population_5_plus"])
        english_only_moe = moe(values, column_by_field["speak_only_english"])
        non_english = None
        non_english_moe = None
        if language_total is not None and english_only is not None:
            non_english = language_total - english_only
        if language_total_moe is not None and english_only_moe is not None:
            non_english_moe = math.sqrt(language_total_moe**2 + english_only_moe**2)
        with_disability = sum_estimates(values, DISABILITY_COMPONENT_FIELDS)
        with_disability_moe = rss_moes(values, DISABILITY_COMPONENT_FIELDS)
        derived_values = {
            "below_poverty": (below_poverty, below_poverty_moe),
            "non_english_home_language": (non_english, non_english_moe),
            "with_disability": (with_disability, with_disability_moe),
        }
        for field, (est_value, moe_value) in derived_values.items():
            row[f"{field}_est"] = fmt_number(est_value)
            row[f"{field}_moe"] = fmt_number(moe_value)

        row.update({
            "veteran_share": share(
                estimate(values, column_by_field["veterans"]),
                estimate(values, column_by_field["civilian_population_18_plus"]),
            ),
            "foreign_born_share": share(
                estimate(values, column_by_field["foreign_born"]),
                estimate(values, column_by_field["nativity_citizenship_total_population"]),
            ),
            "noncitizen_share": share(
                estimate(values, column_by_field["not_us_citizen"]),
                estimate(values, column_by_field["nativity_citizenship_total_population"]),
            ),
            "naturalized_share": share(
                estimate(values, column_by_field["naturalized_citizen"]),
                estimate(values, column_by_field["nativity_citizenship_total_population"]),
            ),
            "non_english_home_language_share": share(non_english, language_total),
            "with_disability_share": share(
                with_disability,
                estimate(values, column_by_field["disability_universe"]),
            ),
            "below_poverty_share": share(
                below_poverty,
                estimate(values, column_by_field["poverty_ratio_universe"]),
            ),
            "unemployment_rate": share(
                estimate(values, column_by_field["unemployed"]),
                estimate(values, column_by_field["civilian_labor_force"]),
            ),
            "labor_force_participation_rate": share(
                estimate(values, column_by_field["civilian_labor_force"]),
                estimate(values, column_by_field["population_16_plus"]),
            ),
            "internet_subscription_share": share(
                estimate(values, column_by_field["with_internet_subscription"]),
                estimate(values, column_by_field["households"]),
            ),
            "no_internet_access_share": share(
                estimate(values, column_by_field["no_internet_access"]),
                estimate(values, column_by_field["households"]),
            ),
            "white_alone_share": share(
                estimate(values, column_by_field["white_alone"]),
                estimate(values, column_by_field["race_total_population"]),
            ),
            "black_alone_share": share(
                estimate(values, column_by_field["black_alone"]),
                estimate(values, column_by_field["race_total_population"]),
            ),
            "asian_alone_share": share(
                estimate(values, column_by_field["asian_alone"]),
                estimate(values, column_by_field["race_total_population"]),
            ),
            "hispanic_or_latino_share": share(
                estimate(values, column_by_field["hispanic_or_latino"]),
                estimate(values, column_by_field["hispanic_total_population"]),
            ),
            "source_tables": source_tables,
            "source_urls": source_urls,
            "evidence_layers": (
                "acs_2017_2021_5yr_116th_congressional_district_context; "
                "acs_table_based_summary_file"
            ),
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], reused: bool = False) -> None:
    total_population = sum(int(float(row["race_total_population_est"] or 0)) for row in rows)
    total_veterans = sum(int(float(row["veterans_est"] or 0)) for row in rows)
    total_poverty = sum(int(float(row["below_poverty_est"] or 0)) for row in rows)
    total_non_citizens = sum(int(float(row["not_us_citizen_est"] or 0)) for row in rows)
    total_no_internet = sum(int(float(row["no_internet_access_est"] or 0)) for row in rows)
    lines = [
        "# District Public-Opinion ACS Context",
        "",
        f"Generated: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        f"Reused existing extract: {'yes' if reused else 'no'}",
        "",
        "Sources:",
        "",
        f"- District queue: `{SOURCE_PACKETS}`.",
        f"- ACS geography labels: {GEOS_URL}.",
        f"- ACS table-based Summary File data directory: {DATA_BASE_URL}.",
        "",
        "Tables:",
        "",
    ]
    for table in sorted(TABLE_COLUMNS):
        lines.append(f"- `{table.upper()}`: {table_url(table)}")
    lines.extend([
        "",
        "Transformation:",
        "",
        "- Extracts unique sponsor districts from the district public-opinion source-packet queue.",
        "- Joins those districts to 116th congressional-district GEO_IDs in `Geos20215YR.txt`.",
        "- Streams selected ACS detailed-table files and stores only queued district rows.",
        "- Treats Census ACS special numeric estimate/MOE sentinel values as missing numeric fields.",
        "- Preserves estimates and margins of error for selected variables; derived sums use root-sum-square MOE where component MOEs are present.",
        "",
        "Rows:",
        "",
        f"- Retrieved ACS district context rows: {len(rows)}.",
        f"- Total ACS race-table population across retrieved sponsor districts: {total_population}.",
        f"- Total ACS veteran estimate across retrieved sponsor districts: {total_veterans}.",
        f"- Total ACS below-poverty estimate across retrieved sponsor districts: {total_poverty}.",
        f"- Total ACS noncitizen estimate across retrieved sponsor districts: {total_non_citizens}.",
        f"- Total ACS no-internet-access household estimate across retrieved sponsor districts: {total_no_internet}.",
        "",
        "Claim boundary:",
        "",
        CLAIM_BOUNDARY,
    ])
    write_reproducible_metadata(OUT_METADATA, "\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="rebuild the ACS extract even if the existing output matches the current district set",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SOURCE_PACKETS.exists():
        raise SystemExit(f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first.")
    packet_rows = read_csv(SOURCE_PACKETS)
    if not packet_rows:
        raise SystemExit(f"{SOURCE_PACKETS} is empty.")
    district_ids = sponsor_districts(packet_rows)
    if not district_ids:
        raise SystemExit(f"{SOURCE_PACKETS} has no sponsor districts.")
    if not args.refresh and existing_output_matches(district_ids):
        rows = read_csv(OUT_CSV)
        write_metadata(rows, reused=True)
        print(f"Reused {OUT_CSV}")
        print(f"Wrote {OUT_METADATA}")
        return 0
    geographies = load_geographies(district_ids)
    acs_geoids = {row["GEO_ID"] for row in geographies.values()}
    values_by_geoid = load_table_rows(acs_geoids)
    rows = build_rows(district_ids, geographies, values_by_geoid)
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - command-line failure path
        print(f"ACS context build failed: {exc}", file=sys.stderr)
        raise
