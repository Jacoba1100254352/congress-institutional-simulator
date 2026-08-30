#!/usr/bin/env python3
"""Write a survey-source crosswalk for district public-opinion packets.

The source-packet report names broad acquisition targets. This report narrows
each packet to official survey/source families, candidate item constructs, and
search terms while preserving the boundary that no survey item, MRP estimate, or
bill-specific support value has been acquired yet.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
ACS_CONTEXT = Path("reports/district-public-opinion-acs-context.csv")
OUT_CSV = Path("reports/district-public-opinion-survey-source-crosswalk.csv")
OUT_MD = Path("reports/district-public-opinion-survey-source-crosswalk.md")

SOURCE_URLS = {
    "CES/CCES": "https://cces.gov.harvard.edu/",
    "ANES": "https://electionstudies.org/data-center/",
    "GSS": "https://gssdataexplorer.norc.org/",
    "Pew Research Center": "https://www.pewresearch.org/datasets/",
    "KFF": "https://www.kff.org/topic/public-opinion/",
    "PRRI": "https://prri.org/prri-research/data-vault/",
    "Chicago Council Survey": (
        "https://globalaffairs.org/explore-research/lester-crown-center-us-foreign-policy/"
        "public-opinion-surveys/chicago-council"
    ),
    "Gallup Analytics": "https://www.gallup.com/analytics/213617/gallup-analytics.aspx",
}

SOURCE_ACCESS_NOTES = {
    "CES/CCES": "large national election survey with common/team content; use only after item year and variable IDs are recorded",
    "ANES": "national election studies data center; useful for item wording and covariates but not district estimates by itself",
    "GSS": "national trend data explorer; useful for long-run item wording but not district estimates by itself",
    "Pew Research Center": "public survey datasets are topic-specific and may require a free account before microdata download",
    "KFF": "health-policy polling source; use only for health or benefit provisions with matching item wording",
    "PRRI": "public-religion and values survey archive; often useful for civil-rights, immigration, religion, and values items",
    "Chicago Council Survey": "foreign-policy survey series; useful for international-affairs item wording and national benchmarks",
    "Gallup Analytics": "subscription public-opinion platform; mark as access-constrained unless licensed data are available",
}

DEFAULT_SOURCE_PLAN = {
    "primary": "CES/CCES",
    "secondary": ["ANES", "Pew Research Center", "GSS"],
    "candidate_item_constructs": "general policy support; government performance; party and ideology covariates",
    "district_estimation_requirement": (
        "Acquire item-level microdata with respondent geography and demographics, then estimate "
        "district support with an MRP or comparable small-area model."
    ),
}

POLICY_SOURCE_PLANS: dict[str, dict[str, object]] = {
    "Armed Forces and National Security": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "Pew Research Center", "Gallup Analytics"],
        "candidate_item_constructs": (
            "defense spending; veterans benefits; military family support; national-security threat response"
        ),
        "district_estimation_requirement": (
            "Use item-level defense or veterans responses with district veteran, age, education, income, "
            "and party poststratification covariates."
        ),
    },
    "Civil Rights and Liberties, Minority Issues": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "PRRI", "Pew Research Center"],
        "candidate_item_constructs": (
            "civil-rights enforcement; marriage equality; minority-rights protections; discrimination remedies"
        ),
        "district_estimation_requirement": (
            "Use civil-rights item responses with race, ethnicity, citizenship, language, age, education, "
            "income, and party poststratification covariates."
        ),
    },
    "Commerce": {
        "primary": "CES/CCES",
        "secondary": ["Pew Research Center", "GSS", "Gallup Analytics"],
        "candidate_item_constructs": (
            "consumer protection; business regulation; supply-chain policy; competition or market oversight"
        ),
        "district_estimation_requirement": (
            "Use commerce or economic-regulation item responses with employment, industry, income, "
            "education, and party poststratification covariates."
        ),
    },
    "Crime and Law Enforcement": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "Pew Research Center", "Gallup Analytics"],
        "candidate_item_constructs": (
            "policing; sentencing; public safety; victimization; justice-system confidence"
        ),
        "district_estimation_requirement": (
            "Use crime or justice item responses with race, age, urbanicity proxy, education, income, "
            "and party poststratification covariates."
        ),
    },
    "Economics and Public Finance": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "Pew Research Center", "Gallup Analytics"],
        "candidate_item_constructs": (
            "taxes; spending; inflation; redistribution; budget priorities; household affordability"
        ),
        "district_estimation_requirement": (
            "Use economic-policy item responses with income, employment, education, age, family status, "
            "and party poststratification covariates."
        ),
    },
    "Finance and Financial Sector": {
        "primary": "CES/CCES",
        "secondary": ["Pew Research Center", "GSS", "Gallup Analytics"],
        "candidate_item_constructs": (
            "bank regulation; credit access; borrower protection; investor protection; financial oversight"
        ),
        "district_estimation_requirement": (
            "Use financial-regulation or consumer-finance item responses with income, homeownership, "
            "education, age, and party poststratification covariates."
        ),
    },
    "Government Operations and Politics": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "Pew Research Center", "GSS", "PRRI"],
        "candidate_item_constructs": (
            "trust in government; election administration; democracy protection; ethics reform; civic access"
        ),
        "district_estimation_requirement": (
            "Use trust, democracy, or election-administration item responses with education, age, race, "
            "income, turnout proxy, and party poststratification covariates."
        ),
    },
    "Immigration": {
        "primary": "CES/CCES",
        "secondary": ["ANES", "Pew Research Center", "PRRI"],
        "candidate_item_constructs": (
            "border enforcement; legalization; naturalization; refugee policy; noncitizen access"
        ),
        "district_estimation_requirement": (
            "Use immigration-policy item responses with nativity, citizenship, language, race, education, "
            "income, and party poststratification covariates."
        ),
    },
    "International Affairs": {
        "primary": "CES/CCES",
        "secondary": ["Chicago Council Survey", "ANES", "Pew Research Center"],
        "candidate_item_constructs": (
            "foreign aid; sanctions; trade; military assistance; international engagement"
        ),
        "district_estimation_requirement": (
            "Use district-estimable foreign-policy responses where possible, with Chicago Council or ANES "
            "items as wording and national-benchmark sources when respondent geography is insufficient."
        ),
    },
    "Public Lands and Natural Resources": {
        "primary": "CES/CCES",
        "secondary": ["Pew Research Center", "Gallup Analytics", "GSS"],
        "candidate_item_constructs": (
            "public lands; conservation; environmental regulation; resource extraction; land-user interests"
        ),
        "district_estimation_requirement": (
            "Use public-lands or environmental item responses with rurality proxy, income, education, "
            "industry, age, and party poststratification covariates."
        ),
    },
    "Science, Technology, Communications": {
        "primary": "CES/CCES",
        "secondary": ["Pew Research Center", "GSS", "Gallup Analytics"],
        "candidate_item_constructs": (
            "broadband; privacy; communications access; science funding; technology regulation"
        ),
        "district_estimation_requirement": (
            "Use technology, broadband, privacy, or science-policy item responses with internet access, "
            "education, age, income, urbanicity proxy, and party poststratification covariates."
        ),
    },
}

FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "target_issue_construct",
    "primary_survey_source_family",
    "primary_survey_source_url",
    "secondary_survey_source_families",
    "secondary_survey_source_urls",
    "source_access_notes",
    "candidate_item_constructs",
    "candidate_item_search_terms",
    "district_estimation_requirement",
    "poststratification_frame",
    "affected_population_requirement",
    "affected_support_or_harm_requirement",
    "survey_crosswalk_status",
    "next_action",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

MISSING_LINKS = (
    "bill_topic_public_opinion; survey_item_id; survey_item_crosswalk; "
    "MRP_or_small_area_estimate; bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

CLAIM_BOUNDARY = (
    "Survey-source crosswalk rows identify official source families, candidate item "
    "constructs, and acquisition search terms only; they are not acquired survey item "
    "IDs, not bill-topic public support, not MRP or small-area estimates, not "
    "bill-text-specific affected-population definitions, not affected-group support "
    "or harm, not public-benefit evidence, and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def plan_for(policy_area: str) -> dict[str, object]:
    return POLICY_SOURCE_PLANS.get(policy_area, DEFAULT_SOURCE_PLAN)


def source_urls(names: list[str]) -> str:
    return "; ".join(SOURCE_URLS[name] for name in names if name in SOURCE_URLS)


def access_notes(names: list[str]) -> str:
    return "; ".join(f"{name}: {SOURCE_ACCESS_NOTES[name]}" for name in names if name in SOURCE_ACCESS_NOTES)


def search_terms(packet: dict[str, str], plan: dict[str, object]) -> str:
    source_names = [str(plan["primary"]), *[str(value) for value in plan.get("secondary", [])]]
    chunks = [
        packet.get("bill_id", ""),
        packet.get("public_law_number", ""),
        packet.get("policy_area", ""),
        packet.get("target_issue_construct", ""),
        packet.get("bill_topic_survey_source", ""),
        packet.get("proxy_issues", ""),
        str(plan.get("candidate_item_constructs", "")),
        " ".join(source_names),
    ]
    terms: list[str] = []
    for chunk in chunks:
        for token in re.split(r"[^A-Za-z0-9/-]+", chunk):
            token = token.strip().lower()
            if len(token) < 3 and not token.startswith("hr"):
                continue
            terms.append(token)
    ordered = []
    seen = set()
    for term in terms:
        if term not in seen:
            seen.add(term)
            ordered.append(term)
    return " ".join(ordered[:60])


def poststratification_frame(packet: dict[str, str], acs_by_bill: dict[str, dict[str, str]]) -> str:
    acs_row = acs_by_bill.get(packet.get("bill_id", ""), {})
    selected = acs_row.get("selected_acs_context_fields", "")
    if selected:
        return f"ACS 2017-2021 district frame: {selected}"
    return "ACS/Census district poststratification frame selected by policy area"


def build_rows(
    packet_rows: list[dict[str, str]],
    acs_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    acs_by_bill = {row.get("bill_id", ""): row for row in acs_rows if row.get("bill_id")}
    rows: list[dict[str, str]] = []
    for packet in packet_rows:
        policy_area = packet.get("policy_area", "")
        plan = plan_for(policy_area)
        primary = str(plan["primary"])
        secondary = [str(value) for value in plan.get("secondary", [])]
        source_names = [primary, *secondary]
        rows.append({
            "packet_rank": packet.get("packet_rank", ""),
            "readiness_rank": packet.get("readiness_rank", ""),
            "bill_id": packet.get("bill_id", ""),
            "public_law_number": packet.get("public_law_number", ""),
            "policy_area": policy_area,
            "sponsor_districts": packet.get("sponsor_districts", ""),
            "target_issue_construct": packet.get("target_issue_construct", ""),
            "primary_survey_source_family": primary,
            "primary_survey_source_url": SOURCE_URLS.get(primary, ""),
            "secondary_survey_source_families": "; ".join(secondary),
            "secondary_survey_source_urls": source_urls(secondary),
            "source_access_notes": access_notes(source_names),
            "candidate_item_constructs": str(plan.get("candidate_item_constructs", "")),
            "candidate_item_search_terms": search_terms(packet, plan),
            "district_estimation_requirement": str(plan.get("district_estimation_requirement", "")),
            "poststratification_frame": poststratification_frame(packet, acs_by_bill),
            "affected_population_requirement": packet.get("affected_population_source", ""),
            "affected_support_or_harm_requirement": packet.get("affected_support_or_harm_source", ""),
            "survey_crosswalk_status": "survey_source_crosswalk_no_item_acquired",
            "next_action": (
                "Review official questionnaires/codebooks for the named source families, record exact "
                "survey year and item IDs, then build or import district-level support estimates before "
                "using any row as bill-topic public-opinion evidence."
            ),
            "evidence_layers": (
                "public_opinion_source_acquisition_packet; "
                "census_tigerweb_116th_district_population_housing_denominator; "
                "acs_2017_2021_5yr_116th_congressional_district_context; "
                "public_opinion_survey_source_crosswalk"
            ),
            "missing_links": MISSING_LINKS,
            "source_urls": source_urls(source_names),
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
    policy_areas = {row["policy_area"] for row in rows if row["policy_area"]}
    no_item_rows = [
        row for row in rows
        if row["survey_crosswalk_status"] == "survey_source_crosswalk_no_item_acquired"
    ]
    source_families = {
        source
        for row in rows
        for source in [row["primary_survey_source_family"], *split_values(row["secondary_survey_source_families"])]
        if source
    }
    lines = [
        "# District Public-Opinion Survey-Source Crosswalk",
        "",
        "This report maps each district public-opinion source packet to official survey/source families, candidate item constructs, and acquisition search terms. It is a source-review crosswalk, not acquired public-opinion evidence.",
        "",
        f"- Crosswalk rows: {len(rows)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Official source families referenced: {len(source_families)}",
        f"- Rows without acquired survey item IDs or estimates: {len(no_item_rows)}",
        "",
        "Official source families referenced:",
    ]
    for source in sorted(source_families):
        url = SOURCE_URLS.get(source, "")
        if url:
            lines.append(f"- {source}: {url}")
    lines.extend([
        "",
        "Claim boundary: rows identify source families and candidate item-search terms only. They do not acquire survey item IDs, estimate district support, define bill-text-specific affected populations, measure affected-group support or harm, or validate model outputs.",
        "",
        "| Packet | Bill ID | Policy area | Primary source | Candidate item constructs | Status |",
        "| ---: | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['primary_survey_source_family']} | {row['candidate_item_constructs']} | "
            f"{row['survey_crosswalk_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not SOURCE_PACKETS.exists():
        raise SystemExit(f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first.")
    if not ACS_CONTEXT.exists():
        raise SystemExit(f"{ACS_CONTEXT} is missing; run make district-public-opinion-acs-context first.")
    packet_rows = read_csv(SOURCE_PACKETS)
    acs_rows = read_csv(ACS_CONTEXT)
    if not packet_rows:
        raise SystemExit(f"{SOURCE_PACKETS} is empty.")
    if not acs_rows:
        raise SystemExit(f"{ACS_CONTEXT} is empty.")
    rows = build_rows(packet_rows, acs_rows)
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
