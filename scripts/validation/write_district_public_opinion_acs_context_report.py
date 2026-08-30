#!/usr/bin/env python3
"""Write a packet-level report for district ACS context."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
ACS_CONTEXT = Path("data/validation/raw/district_public_opinion_acs_context.csv")
OUT_CSV = Path("reports/district-public-opinion-acs-context.csv")
OUT_MD = Path("reports/district-public-opinion-acs-context.md")

FIELDNAMES = [
    "packet_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "acs_context_district_count",
    "matched_acs_context_districts",
    "missing_acs_context_districts",
    "total_acs_population_est",
    "total_veterans_est",
    "veteran_share",
    "total_foreign_born_est",
    "total_not_us_citizen_est",
    "noncitizen_share",
    "total_non_english_home_language_est",
    "non_english_home_language_share",
    "total_with_disability_est",
    "with_disability_share",
    "total_below_poverty_est",
    "below_poverty_share",
    "total_civilian_labor_force_est",
    "total_unemployed_est",
    "unemployment_rate",
    "mean_median_household_income_est",
    "total_households_est",
    "total_no_internet_access_est",
    "no_internet_access_share",
    "black_alone_share",
    "asian_alone_share",
    "hispanic_or_latino_share",
    "selected_acs_context_fields",
    "still_missing_policy_specific_fields",
    "acs_context_status",
    "acs_context_source",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

POLICY_CONTEXT_FIELDS: dict[str, str] = {
    "Armed Forces and National Security": "veterans; civilian_population_18_plus; median_household_income; poverty; disability",
    "Civil Rights and Liberties, Minority Issues": "race; ethnicity; citizenship; language; disability; poverty",
    "Commerce": "employment; unemployment; median_household_income; poverty; internet_access",
    "Crime and Law Enforcement": "race; ethnicity; poverty; employment; disability; language",
    "Economics and Public Finance": "poverty; employment; unemployment; median_household_income; households",
    "Finance and Financial Sector": "median_household_income; poverty; employment; unemployment; households",
    "Government Operations and Politics": "citizenship; language; disability; internet_access; race; ethnicity",
    "Immigration": "foreign_born; naturalized_citizen; not_us_citizen; language; poverty; employment",
    "International Affairs": "foreign_born; language; employment; poverty; median_household_income",
    "Public Lands and Natural Resources": "employment; poverty; median_household_income; households; race; ethnicity",
    "Science, Technology, Communications": "internet_access; education_proxy_not_included; income; age_proxy_not_included; employment",
}

POLICY_MISSING_FIELDS: dict[str, str] = {
    "Armed Forces and National Security": "active-duty population; military-family status; bill-text-specific veteran or defense affected group; veteran support/harm source",
    "Civil Rights and Liberties, Minority Issues": "bill-targeted protected class; discrimination or harm outcome; affected-group support source",
    "Commerce": "industry-specific affected firms/workers; small-business owner denominators; consumer harm/support source",
    "Crime and Law Enforcement": "justice-system exposure; victimization/policing outcome; affected-community support/harm source",
    "Economics and Public Finance": "program beneficiary/taxpayer denominator selected from bill text; fiscal incidence; bill-topic public support",
    "Finance and Financial Sector": "borrower/investor/account-holder target group; financial-access harm/source; bill-topic public support",
    "Government Operations and Politics": "voting-age citizen by access burden; election-administration exposure; democracy/trust survey item",
    "Immigration": "bill-targeted visa/status class; border-community exposure; immigrant/noncitizen support or harm source",
    "International Affairs": "trade-exposed industry/worker denominator; diaspora or sanctions target group; foreign-policy survey item",
    "Public Lands and Natural Resources": "land-adjacent or tribal/Indigenous target geography; resource-user group; environmental harm/source",
    "Science, Technology, Communications": "computer-device access; broadband availability/adoption by target group; privacy/technology support item",
}

MISSING_LINKS = (
    "bill_topic_public_opinion; survey_item_crosswalk; MRP_or_small_area_estimate; "
    "bill_text_specific_affected_population_denominator; issue_specific_affected_group_support; "
    "affected_group_harm; public_benefit; causal_representation; model_validation"
)

CLAIM_BOUNDARY = (
    "ACS context rows provide broad 2017-2021 district demographic, economic, "
    "language, disability, internet, citizenship, and veteran context selected by "
    "source-packet policy area; they are not bill-topic public support, not MRP "
    "or small-area estimates, not bill-text-specific affected-population definitions, "
    "not issue-specific affected-group support or harm, not public-benefit evidence, "
    "and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def parse_float(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def fmt_number(value: float) -> str:
    if abs(value - round(value)) < 0.0000001:
        return str(int(round(value)))
    return f"{value:.3f}"


def share(numerator: float, denominator: float) -> str:
    return f"{numerator / denominator:.4f}" if denominator > 0 else ""


def mean(values: list[float]) -> str:
    return f"{sum(values) / len(values):.3f}" if values else ""


def sum_field(rows: list[dict[str, str]], field: str) -> float:
    return sum(parse_float(row.get(field)) for row in rows)


def build_rows(packet_rows: list[dict[str, str]], context_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    context_by_district = {
        row["district_id"]: row
        for row in context_rows
        if row.get("district_id")
    }
    rows: list[dict[str, str]] = []
    for packet in packet_rows:
        districts = split_values(packet.get("sponsor_districts", ""))
        matched = [context_by_district[district] for district in districts if district in context_by_district]
        missing = [district for district in districts if district not in context_by_district]
        total_population = sum_field(matched, "race_total_population_est")
        total_veterans = sum_field(matched, "veterans_est")
        total_veteran_universe = sum_field(matched, "civilian_population_18_plus_est")
        total_foreign_born = sum_field(matched, "foreign_born_est")
        total_not_us_citizen = sum_field(matched, "not_us_citizen_est")
        total_citizenship_universe = sum_field(matched, "nativity_citizenship_total_population_est")
        total_non_english = sum_field(matched, "non_english_home_language_est")
        total_language_universe = sum_field(matched, "language_population_5_plus_est")
        total_disability = sum_field(matched, "with_disability_est")
        total_disability_universe = sum_field(matched, "disability_universe_est")
        total_below_poverty = sum_field(matched, "below_poverty_est")
        total_poverty_universe = sum_field(matched, "poverty_ratio_universe_est")
        total_labor_force = sum_field(matched, "civilian_labor_force_est")
        total_unemployed = sum_field(matched, "unemployed_est")
        median_incomes = [
            parse_float(row.get("median_household_income_est"))
            for row in matched
            if parse_float(row.get("median_household_income_est")) > 0
        ]
        total_households = sum_field(matched, "households_est")
        total_no_internet = sum_field(matched, "no_internet_access_est")
        total_black = sum_field(matched, "black_alone_est")
        total_asian = sum_field(matched, "asian_alone_est")
        total_hispanic = sum_field(matched, "hispanic_or_latino_est")
        total_hispanic_universe = sum_field(matched, "hispanic_total_population_est")
        status = (
            "official_acs_2017_2021_5yr_district_context"
            if matched and not missing
            else "partial_acs_2017_2021_5yr_district_context"
        )
        policy_area = packet.get("policy_area", "")
        rows.append({
            "packet_rank": packet.get("packet_rank", ""),
            "bill_id": packet.get("bill_id", ""),
            "public_law_number": packet.get("public_law_number", ""),
            "policy_area": policy_area,
            "sponsor_districts": packet.get("sponsor_districts", ""),
            "acs_context_district_count": str(len(matched)),
            "matched_acs_context_districts": "; ".join(row["district_id"] for row in matched),
            "missing_acs_context_districts": "; ".join(missing),
            "total_acs_population_est": fmt_number(total_population),
            "total_veterans_est": fmt_number(total_veterans),
            "veteran_share": share(total_veterans, total_veteran_universe),
            "total_foreign_born_est": fmt_number(total_foreign_born),
            "total_not_us_citizen_est": fmt_number(total_not_us_citizen),
            "noncitizen_share": share(total_not_us_citizen, total_citizenship_universe),
            "total_non_english_home_language_est": fmt_number(total_non_english),
            "non_english_home_language_share": share(total_non_english, total_language_universe),
            "total_with_disability_est": fmt_number(total_disability),
            "with_disability_share": share(total_disability, total_disability_universe),
            "total_below_poverty_est": fmt_number(total_below_poverty),
            "below_poverty_share": share(total_below_poverty, total_poverty_universe),
            "total_civilian_labor_force_est": fmt_number(total_labor_force),
            "total_unemployed_est": fmt_number(total_unemployed),
            "unemployment_rate": share(total_unemployed, total_labor_force),
            "mean_median_household_income_est": mean(median_incomes),
            "total_households_est": fmt_number(total_households),
            "total_no_internet_access_est": fmt_number(total_no_internet),
            "no_internet_access_share": share(total_no_internet, total_households),
            "black_alone_share": share(total_black, total_population),
            "asian_alone_share": share(total_asian, total_population),
            "hispanic_or_latino_share": share(total_hispanic, total_hispanic_universe),
            "selected_acs_context_fields": POLICY_CONTEXT_FIELDS.get(policy_area, "broad ACS district context"),
            "still_missing_policy_specific_fields": POLICY_MISSING_FIELDS.get(
                policy_area,
                "bill-text-specific affected population; bill-topic support; affected-group support or harm",
            ),
            "acs_context_status": status,
            "acs_context_source": "U.S. Census Bureau ACS 2017-2021 5-year detailed tables, table-based Summary File",
            "evidence_layers": (
                "public_opinion_source_acquisition_packet; "
                "census_tigerweb_116th_district_population_housing_denominator; "
                "acs_2017_2021_5yr_116th_congressional_district_context"
            ),
            "missing_links": MISSING_LINKS,
            "source_urls": "; ".join(sorted({
                row.get("source_urls", "")
                for row in matched
                if row.get("source_urls", "")
            })),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], context_rows: list[dict[str, str]]) -> None:
    matched_rows = [
        row for row in rows
        if row["acs_context_status"] == "official_acs_2017_2021_5yr_district_context"
    ]
    policy_areas = {row["policy_area"] for row in rows if row["policy_area"]}
    unique_districts = {
        district
        for row in rows
        for district in split_values(row.get("matched_acs_context_districts", ""))
    }
    total_population = sum(parse_float(row.get("race_total_population_est")) for row in context_rows)
    total_veterans = sum(parse_float(row.get("veterans_est")) for row in context_rows)
    total_non_citizens = sum(parse_float(row.get("not_us_citizen_est")) for row in context_rows)
    total_below_poverty = sum(parse_float(row.get("below_poverty_est")) for row in context_rows)
    lines = [
        "# District Public-Opinion ACS Context",
        "",
        "This report joins official ACS 2017-2021 5-year congressional-district context to the district public-opinion source-packet queue. It is broad district context, not bill-topic support or affected-group harm evidence.",
        "",
        f"- Source packets with ACS context rows: {len(matched_rows)} / {len(rows)}",
        f"- Unique sponsor districts with ACS context: {len(unique_districts)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Unique-district ACS population estimate total: {fmt_number(total_population)}",
        f"- Unique-district ACS veteran estimate total: {fmt_number(total_veterans)}",
        f"- Unique-district ACS noncitizen estimate total: {fmt_number(total_non_citizens)}",
        f"- Unique-district ACS below-poverty estimate total: {fmt_number(total_below_poverty)}",
        "",
        "Claim boundary: this closes only a broad ACS district-context sub-gap for queued sponsor districts. It does not provide issue-specific bill support, MRP/small-area estimates, bill-text-specific affected-population definitions, affected-group support or harm, public-benefit evidence, or model validation.",
        "",
        "| Packet | Bill ID | Policy area | Districts | Population | Veterans | Noncitizens | Below poverty | No internet | Status |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['matched_acs_context_districts']} | {row['total_acs_population_est']} | "
            f"{row['total_veterans_est']} | {row['total_not_us_citizen_est']} | "
            f"{row['total_below_poverty_est']} | {row['total_no_internet_access_est']} | "
            f"{row['acs_context_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not SOURCE_PACKETS.exists():
        raise SystemExit(f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first.")
    if not ACS_CONTEXT.exists():
        raise SystemExit(f"{ACS_CONTEXT} is missing; run make build-district-public-opinion-acs-context-raw first.")
    packet_rows = read_csv(SOURCE_PACKETS)
    context_rows = read_csv(ACS_CONTEXT)
    if not packet_rows:
        raise SystemExit(f"{SOURCE_PACKETS} is empty.")
    if not context_rows:
        raise SystemExit(f"{ACS_CONTEXT} is empty.")
    rows = build_rows(packet_rows, context_rows)
    write_csv(rows)
    write_md(rows, context_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
