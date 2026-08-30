#!/usr/bin/env python3
"""Write exact CES proxy-variable review rows for district-opinion packets."""

from __future__ import annotations

import csv
import re
from pathlib import Path


DISTRICT_PUBLIC_OPINION = Path("data/validation/raw/district_public_opinion.csv")
DISTRICT_PUBLIC_OPINION_METADATA = Path("data/validation/raw/district_public_opinion.metadata.md")
SURVEY_CROSSWALK = Path("reports/district-public-opinion-survey-source-crosswalk.csv")
OUT_CSV = Path("reports/district-public-opinion-survey-item-proxy-review.csv")
OUT_MD = Path("reports/district-public-opinion-survey-item-proxy-review.md")

CES_DOI = "10.7910/DVN/II2DB6"
CES_SOURCE_URL = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/II2DB6"
CURRENT_PROXY_VARIABLE_IDS = (
    "approval_rep; intent_pres_party; intent_rep_party; voted_turnout_self; "
    "intent_turnout_self; no_healthins; cd; weight; year"
)
CURRENT_PROXY_SIGNALS = (
    "house_representative_approval; presidential_democratic_preference; "
    "house_democratic_preference; turnout; uninsured_share_vulnerability_proxy"
)
FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "target_issue_construct",
    "primary_survey_source_family",
    "current_proxy_source_family",
    "current_proxy_dataset_doi",
    "current_proxy_dataset_version",
    "current_proxy_distribution_date",
    "current_proxy_survey_year",
    "current_proxy_variable_ids",
    "current_proxy_signal_names",
    "current_proxy_review_status",
    "bill_topic_candidate_constructs",
    "acquired_bill_topic_item_ids",
    "acquired_bill_topic_item_years",
    "bill_topic_item_review_status",
    "district_estimation_status",
    "affected_group_item_status",
    "required_next_action",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

MISSING_LINKS = (
    "bill_topic_public_opinion; acquired_bill_topic_survey_item_id; survey_item_crosswalk; "
    "MRP_or_small_area_estimate; bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

CLAIM_BOUNDARY = (
    "Rows record exact current CES proxy variables and attach them to queued "
    "bill-topic source packets. They are not acquired bill-topic survey item IDs, "
    "not bill-topic public support, not MRP or small-area estimates, not "
    "bill-text-specific affected-population definitions, not affected-group "
    "support or harm, not public-benefit evidence, and not model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def metadata_value(text: str, label: str) -> str:
    pattern = rf"^- {re.escape(label)}: (.+?)(?:\.)?$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def district_opinion_year(rows: list[dict[str, str]]) -> str:
    years = sorted({row.get("year", "").strip() for row in rows if row.get("year", "").strip()})
    return "; ".join(years)


def build_rows(crosswalk_rows: list[dict[str, str]], opinion_rows: list[dict[str, str]], metadata_text: str) -> list[dict[str, str]]:
    dataset_version = metadata_value(metadata_text, "Dataset version")
    distribution_date = metadata_value(metadata_text, "Distribution date")
    survey_year = district_opinion_year(opinion_rows)
    rows: list[dict[str, str]] = []
    for source in crosswalk_rows:
        rows.append({
            "packet_rank": source.get("packet_rank", ""),
            "readiness_rank": source.get("readiness_rank", ""),
            "bill_id": source.get("bill_id", ""),
            "public_law_number": source.get("public_law_number", ""),
            "policy_area": source.get("policy_area", ""),
            "sponsor_districts": source.get("sponsor_districts", ""),
            "target_issue_construct": source.get("target_issue_construct", ""),
            "primary_survey_source_family": source.get("primary_survey_source_family", ""),
            "current_proxy_source_family": "Cumulative CES Common Content",
            "current_proxy_dataset_doi": CES_DOI,
            "current_proxy_dataset_version": dataset_version,
            "current_proxy_distribution_date": distribution_date,
            "current_proxy_survey_year": survey_year,
            "current_proxy_variable_ids": CURRENT_PROXY_VARIABLE_IDS,
            "current_proxy_signal_names": CURRENT_PROXY_SIGNALS,
            "current_proxy_review_status": "exact_current_ces_proxy_variables_reviewed_no_bill_topic_item",
            "bill_topic_candidate_constructs": source.get("candidate_item_constructs", ""),
            "acquired_bill_topic_item_ids": "",
            "acquired_bill_topic_item_years": "",
            "bill_topic_item_review_status": "no_bill_topic_survey_item_acquired",
            "district_estimation_status": "no_mrp_or_small_area_estimate",
            "affected_group_item_status": "no_bill_text_specific_affected_group_item_acquired",
            "required_next_action": (
                "Review official source questionnaires/codebooks for the candidate constructs, "
                "record exact bill-topic survey item IDs and years, then build or import "
                "district-level estimates before using any row as bill-topic support evidence."
            ),
            "evidence_layers": (
                "public_opinion_survey_source_crosswalk; cumulative_ces_source_variable_review; "
                "cumulative_ces_district_aggregate; sponsor_district_bill_policy_area_context"
            ),
            "missing_links": MISSING_LINKS,
            "source_urls": f"{CES_SOURCE_URL}; {source.get('source_urls', '')}".strip("; "),
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
    proxy_reviewed = [
        row for row in rows
        if row["current_proxy_review_status"] == "exact_current_ces_proxy_variables_reviewed_no_bill_topic_item"
    ]
    bill_topic_items = [row for row in rows if row["acquired_bill_topic_item_ids"].strip()]
    lines = [
        "# District Public-Opinion Survey Item Proxy Review",
        "",
        "This report records the exact CES variables used by the current district public-opinion proxy and attaches that proxy-variable review to the queued bill-topic source packets. It is not bill-topic public-opinion evidence.",
        "",
        f"- Packet rows reviewed: {len(rows)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Rows with exact current CES proxy variables recorded: {len(proxy_reviewed)}",
        f"- Rows with acquired bill-topic survey item IDs: {len(bill_topic_items)}",
        "",
        "Current CES proxy variables:",
        "",
    ]
    for variable in CURRENT_PROXY_VARIABLE_IDS.split("; "):
        lines.append(f"- `{variable}`")
    lines.extend([
        "",
        "Claim boundary: rows record exact current CES proxy variables only. They do not acquire bill-topic survey items, estimate district support, define bill-text-specific affected populations, measure affected-group support or harm, or validate model outputs.",
        "",
        "| Packet | Bill ID | Policy area | Current proxy variables | Bill-topic item status |",
        "| ---: | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['current_proxy_variable_ids']} | {row['bill_topic_item_review_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    for path, command in (
        (DISTRICT_PUBLIC_OPINION, "make build-district-public-opinion-raw"),
        (DISTRICT_PUBLIC_OPINION_METADATA, "make build-district-public-opinion-raw"),
        (SURVEY_CROSSWALK, "make district-public-opinion-survey-source-crosswalk"),
    ):
        if not path.exists():
            raise SystemExit(f"{path} is missing; run {command} first.")
    opinion_rows = read_csv(DISTRICT_PUBLIC_OPINION)
    crosswalk_rows = read_csv(SURVEY_CROSSWALK)
    if not opinion_rows:
        raise SystemExit(f"{DISTRICT_PUBLIC_OPINION} is empty.")
    if not crosswalk_rows:
        raise SystemExit(f"{SURVEY_CROSSWALK} is empty.")
    metadata_text = DISTRICT_PUBLIC_OPINION_METADATA.read_text()
    rows = build_rows(crosswalk_rows, opinion_rows, metadata_text)
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
