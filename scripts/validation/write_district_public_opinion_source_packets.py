#!/usr/bin/env python3
"""Write source-acquisition packets for bill-topic public opinion.

The bill-topic readiness report shows which sponsor-district public-law rows are
still proxy-only. This report turns those rows into source-specific acquisition
packets so the next data build can target survey items, MRP/small-area estimates,
and affected-population joins without treating the packet itself as evidence.
"""

from __future__ import annotations

import csv
from pathlib import Path


READINESS = Path("reports/district-public-opinion-bill-topic-readiness.csv")
OUT_CSV = Path("reports/district-public-opinion-source-packets.csv")
OUT_MD = Path("reports/district-public-opinion-source-packets.md")

FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "proxy_issues",
    "proxy_row_count",
    "current_proxy_status",
    "target_issue_construct",
    "bill_topic_survey_source",
    "district_estimation_source",
    "affected_population_source",
    "affected_support_or_harm_source",
    "required_join_keys",
    "acquisition_status",
    "next_action",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

DEFAULT_PACKET = {
    "target_issue_construct": "policy-area-specific bill support",
    "bill_topic_survey_source": "Cumulative CES or CCES-style issue item crosswalk; ANES/GSS/Pew-style public issue items if district or model covariates are available",
    "district_estimation_source": "MRP or comparable small-area estimate using survey microdata and district poststratification covariates",
    "affected_population_source": "ACS/Census district denominator selected for the bill policy area",
    "affected_support_or_harm_source": "issue-specific affected-group survey, administrative outcome, or harm source selected after bill-text review",
}

POLICY_PACKETS: dict[str, dict[str, str]] = {
    "Armed Forces and National Security": {
        "target_issue_construct": "defense, veterans, or national-security bill support",
        "bill_topic_survey_source": "CES/CCES or ANES foreign-policy and defense items; veteran/military-family issue surveys where available",
        "district_estimation_source": "MRP over survey defense/veterans items using district veteran, age, education, income, and party covariates",
        "affected_population_source": "ACS veteran, active-duty, age, income, and household composition denominators by congressional district",
        "affected_support_or_harm_source": "veteran or military-family survey/outcome source paired with bill text before harm/support claims",
    },
    "Civil Rights and Liberties, Minority Issues": {
        "target_issue_construct": "civil-rights or minority-rights bill support",
        "bill_topic_survey_source": "CES/CCES, ANES, or issue-specific civil-rights survey items with demographic response fields",
        "district_estimation_source": "MRP over civil-rights items using race, ethnicity, age, education, income, and party covariates",
        "affected_population_source": "ACS race, ethnicity, citizenship, disability, language, age, sex, and household denominators by district",
        "affected_support_or_harm_source": "affected-group survey or administrative discrimination/harm source tied to the bill target",
    },
    "Commerce": {
        "target_issue_construct": "commerce, consumer, or business-regulation bill support",
        "bill_topic_survey_source": "CES/CCES economic-regulation items; consumer or business policy surveys where bill-topic wording exists",
        "district_estimation_source": "MRP over commerce/economic-regulation items using employment, industry, income, education, and party covariates",
        "affected_population_source": "ACS employment, industry, occupation, income, and small-business-relevant denominators by district",
        "affected_support_or_harm_source": "consumer, worker, or industry-specific support/harm source selected from bill text",
    },
    "Crime and Law Enforcement": {
        "target_issue_construct": "crime, policing, sentencing, or law-enforcement bill support",
        "bill_topic_survey_source": "CES/CCES or ANES crime, policing, public-safety, and justice-system items",
        "district_estimation_source": "MRP over crime/law-enforcement items using race, age, urbanicity, education, income, and party covariates",
        "affected_population_source": "ACS demographic denominators plus district-level exposure measures selected for the bill target",
        "affected_support_or_harm_source": "victimization, justice-system, policing, or affected-community survey/outcome source tied to bill text",
    },
    "Economics and Public Finance": {
        "target_issue_construct": "tax, spending, inflation, or fiscal-policy bill support",
        "bill_topic_survey_source": "CES/CCES economic-policy, tax, spending, inflation, or redistribution issue items",
        "district_estimation_source": "MRP over economic-policy items using income, employment, education, age, family status, and party covariates",
        "affected_population_source": "ACS income, poverty, employment, age, household, and benefit-relevant denominators by district",
        "affected_support_or_harm_source": "taxpayer, beneficiary, worker, or household outcome/support source selected after bill-text review",
    },
    "Finance and Financial Sector": {
        "target_issue_construct": "banking, credit, investor, or financial-regulation bill support",
        "bill_topic_survey_source": "CES/CCES economic-regulation items; financial consumer or investor survey items where available",
        "district_estimation_source": "MRP over financial-regulation items using income, homeownership, education, age, and party covariates",
        "affected_population_source": "ACS income, homeownership, mortgage, age, poverty, and employment denominators by district",
        "affected_support_or_harm_source": "consumer-finance, borrower, investor, or financial-access outcome source tied to bill text",
    },
    "Government Operations and Politics": {
        "target_issue_construct": "government-operations, democracy, ethics, or institutional-reform bill support",
        "bill_topic_survey_source": "CES/CCES government trust, election administration, democracy, or ethics items where wording matches bill target",
        "district_estimation_source": "MRP over trust/democracy/election items using education, age, race, income, turnout, and party covariates",
        "affected_population_source": "ACS voting-age, citizenship, language, disability, and access-relevant denominators by district",
        "affected_support_or_harm_source": "election-administration, civic-access, or administrative-burden source tied to bill text",
    },
    "Immigration": {
        "target_issue_construct": "immigration, border, naturalization, or noncitizen-policy bill support",
        "bill_topic_survey_source": "CES/CCES or ANES immigration-policy items with respondent geography and demographics",
        "district_estimation_source": "MRP over immigration-policy items using nativity, citizenship, language, race, education, income, and party covariates",
        "affected_population_source": "ACS foreign-born, noncitizen, naturalized-citizen, language, income, and household denominators by district",
        "affected_support_or_harm_source": "immigrant, noncitizen, border-community, or employer/worker source tied to bill text",
    },
    "International Affairs": {
        "target_issue_construct": "foreign-policy, trade, aid, sanctions, or international-affairs bill support",
        "bill_topic_survey_source": "CES/CCES, ANES, Chicago Council, or similar foreign-policy/trade issue items if district covariates are usable",
        "district_estimation_source": "MRP over foreign-policy/trade items using education, income, industry, nativity, race, age, and party covariates",
        "affected_population_source": "ACS industry, trade-exposed employment proxy, foreign-born, language, and income denominators by district",
        "affected_support_or_harm_source": "trade-exposed worker, diaspora, aid-recipient, sanctions, or foreign-policy constituency source tied to bill text",
    },
    "Public Lands and Natural Resources": {
        "target_issue_construct": "public-lands, conservation, resource, or environmental-management bill support",
        "bill_topic_survey_source": "CES/CCES environmental/public-lands items; conservation or resource-policy survey items where district covariates exist",
        "district_estimation_source": "MRP over environment/public-lands items using rurality, income, education, industry, age, and party covariates",
        "affected_population_source": "ACS rural, industry, income, housing, tribal/Indigenous where applicable, and land-adjacent denominators by district",
        "affected_support_or_harm_source": "land-user, conservation, tribal/Indigenous, environmental, or resource-community source tied to bill text",
    },
    "Science, Technology, Communications": {
        "target_issue_construct": "technology, communications, broadband, research, or science-policy bill support",
        "bill_topic_survey_source": "CES/CCES technology, privacy, broadband, science, or communications policy items where wording matches bill target",
        "district_estimation_source": "MRP over technology/communications items using internet access, education, age, income, urbanicity, and party covariates",
        "affected_population_source": "ACS internet subscription, computer access, education, income, age, and rural denominators by district",
        "affected_support_or_harm_source": "broadband-access, privacy, technology-consumer, research-workforce, or communications source tied to bill text",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def packet_for(policy_area: str) -> dict[str, str]:
    return POLICY_PACKETS.get(policy_area, DEFAULT_PACKET)


def build_rows(readiness_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(readiness_rows, start=1):
        policy_area = source.get("policy_area", "")
        packet = packet_for(policy_area)
        historical_source_acquired = (
            source.get("source_reviewed_bill_item_alignment_rows", "0").strip() == "1"
            and int(source.get("issue_specific_support_rows", "0") or "0") > 0
        )
        rows.append({
            "packet_rank": str(index),
            "readiness_rank": source.get("readiness_rank", ""),
            "bill_id": source.get("bill_id", ""),
            "public_law_number": source.get("public_law_number", ""),
            "policy_area": policy_area,
            "sponsor_districts": source.get("sponsor_districts", ""),
            "proxy_issues": source.get("proxy_issues", ""),
            "proxy_row_count": source.get("proxy_row_count", ""),
            "current_proxy_status": source.get("bill_topic_public_opinion_status", ""),
            "target_issue_construct": packet["target_issue_construct"],
            "bill_topic_survey_source": packet["bill_topic_survey_source"],
            "district_estimation_source": packet["district_estimation_source"],
            "affected_population_source": packet["affected_population_source"],
            "affected_support_or_harm_source": packet["affected_support_or_harm_source"],
            "required_join_keys": (
                "bill_id; public_law_number; policy_area; district_id; issue_topic; "
                "survey_item_id; mrp_estimate_id; affected_group; affected_population_denominator"
            ),
            "acquisition_status": (
                "historical_related_issue_source_acquired_exact_bill_support_pending"
                if historical_source_acquired
                else "source_packet_only_no_external_dataset_acquired"
            ),
            "next_action": (
                "Retain the privacy-thresholded historical related-issue estimates separately; "
                "acquire exact or closer contemporaneous bill-topic support, add design-based "
                "uncertainty or MRP where needed, and add affected-population evidence."
                if historical_source_acquired
                else "Select source item or microdata for the bill topic, build or import district-level "
                "MRP/small-area support, add affected-population denominators, and keep support "
                "separate from affected-group exposure."
            ),
            "evidence_layers": (
                "cumulative_ces_district_aggregate; sponsor_district_public_law_bill_metadata; "
                "sponsor_district_bill_policy_area_context; bill_topic_public_opinion_readiness_queue; "
                "public_opinion_source_acquisition_packet"
                + (
                    "; source_reviewed_historical_issue_item_alignment; "
                    "privacy_thresholded_direct_weighted_district_issue_estimate"
                    if historical_source_acquired
                    else ""
                )
            ),
            "missing_links": (
                "bill_topic_public_opinion; survey_item_crosswalk; "
                "exact_bill_wording_support; "
                "contemporaneous_bill_support; MRP_or_small_area_estimate; "
                "affected_population_denominator; issue_specific_affected_group_support; "
                "affected_group_harm; causal_representation; public_benefit; model_validation"
            ),
            "source_url": source.get("source_url", ""),
            "claim_boundary": (
                "Source-acquisition packet with bounded CES sponsor-district proxy context and, "
                "where present, a privacy-thresholded historical related-issue district estimate. "
                "The historical estimate is not exact or contemporaneous bill-topic support; "
                "packets have not acquired bill-topic support data that are exact or "
                "contemporaneous to the bill. "
                "Packets do not provide MRP, affected-population denominators, affected-group "
                "support or harm, public-benefit evidence, or model validation."
            ),
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
    missing_status_rows = [
        row for row in rows
        if row["acquisition_status"] == "source_packet_only_no_external_dataset_acquired"
    ]
    lines = [
        "# District Public-Opinion Source Packets",
        "",
        "This report converts the bill-topic public-opinion readiness queue into source-acquisition packets and records bounded historical source acquisition where completed. It is a work queue, not exact bill-support validation evidence.",
        "",
        f"- Source packets: {len(rows)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Packets without acquired external bill-topic data: {len(missing_status_rows)}",
        "",
        "Claim boundary: packets name plausible survey, MRP/small-area, and affected-population source families for each queued public-law bill. One packet carries historical related-issue estimates, but no packet provides exact or contemporaneous bill support, affected-group harm, or model validation.",
        "",
        "| Packet | Bill ID | Policy area | Target construct | Survey source | Affected-population source | Status |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['target_issue_construct']} | {row['bill_topic_survey_source']} | "
            f"{row['affected_population_source']} | {row['acquisition_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not READINESS.exists():
        raise SystemExit(f"{READINESS} is missing; run make district-public-opinion-bill-topic-readiness first.")
    readiness_rows = read_csv(READINESS)
    if not readiness_rows:
        raise SystemExit(f"{READINESS} is empty.")
    rows = build_rows(readiness_rows)
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
