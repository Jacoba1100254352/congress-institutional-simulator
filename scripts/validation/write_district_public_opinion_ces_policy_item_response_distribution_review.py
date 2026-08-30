#!/usr/bin/env python3
"""Join CES policy-preference raw response distributions to public-opinion packets."""

from __future__ import annotations

import csv
from pathlib import Path


CANDIDATE_REVIEW = Path("reports/district-public-opinion-ces-policy-item-candidate-review.csv")
RAW_DISTRIBUTIONS = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
OUT_CSV = Path("reports/district-public-opinion-ces-policy-item-response-distribution-review.csv")
OUT_MD = Path("reports/district-public-opinion-ces-policy-item-response-distribution-review.md")

CLAIM_BOUNDARY = (
    "CES policy-preference response-distribution review only; rows join queued "
    "public-law source packets to unweighted raw response-code distributions "
    "for official Cumulative CES Policy Preferences candidate variables. These "
    "raw response-code summaries are not recoded support/opposition measures, "
    "not source-reviewed exact bill-topic support items, not district support "
    "estimates, not MRP or small-area estimates, not bill-text-specific "
    "affected-population definitions, not affected-group support or harm, not "
    "public-benefit evidence, and not model validation."
)

MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; response_codebook_direction_review; "
    "bill_topic_public_opinion; MRP_or_small_area_estimate; respondent_geography_merge; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "district_public_opinion_ces_policy_item_candidate_review; "
    "official_policy_preferences_raw_response_code_distribution; "
    "district_public_opinion_ces_policy_item_response_distribution_review"
)

FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "target_issue_construct",
    "candidate_policy_preference_item_ids",
    "candidate_policy_preference_item_count",
    "candidate_items_with_response_distribution_count",
    "candidate_item_year_distribution_rows",
    "source_item_response_observation_count",
    "source_item_blank_observation_count",
    "observed_response_years",
    "observed_response_year_count",
    "response_distribution_status",
    "exact_bill_topic_support_status",
    "support_direction_status",
    "district_estimation_status",
    "affected_group_item_status",
    "required_next_action",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def source_urls(candidate_row: dict[str, str], distribution_rows: list[dict[str, str]]) -> str:
    urls: list[str] = []
    for value in split_values(candidate_row.get("source_urls", "")):
        if value and value not in urls:
            urls.append(value)
    for row in distribution_rows:
        for field in ("source_url", "data_download_url"):
            value = row.get(field, "").strip()
            if value and value not in urls:
                urls.append(value)
    return "; ".join(urls)


def build_rows(
    candidate_review_rows: list[dict[str, str]],
    distribution_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    overall_distribution_by_variable = {
        row["variable_id"]: row
        for row in distribution_rows
        if row.get("year") == "all"
    }
    year_distribution_by_variable: dict[str, list[dict[str, str]]] = {}
    for row in distribution_rows:
        if row.get("year") == "all":
            continue
        year_distribution_by_variable.setdefault(row["variable_id"], []).append(row)

    rows: list[dict[str, str]] = []
    for candidate_row in candidate_review_rows:
        candidate_items = split_values(candidate_row.get("candidate_policy_preference_item_ids", ""))
        overall_rows = [
            overall_distribution_by_variable[item]
            for item in candidate_items
            if item in overall_distribution_by_variable
            and int(overall_distribution_by_variable[item].get("response_nonmissing_count", "0") or "0") > 0
        ]
        year_rows = [
            year_row
            for item in candidate_items
            for year_row in year_distribution_by_variable.get(item, [])
        ]
        years = sorted(
            {
                row.get("year", "")
                for row in year_rows
                if int(row.get("response_nonmissing_count", "0") or "0") > 0
            },
            key=lambda value: int(value) if value.isdigit() else value,
        )
        response_count = sum(int(row.get("response_nonmissing_count", "0") or "0") for row in overall_rows)
        blank_count = sum(int(row.get("response_blank_count", "0") or "0") for row in overall_rows)
        status = (
            "official_ces_policy_preference_raw_response_distributions_available_no_support_direction"
            if overall_rows
            else "no_candidate_item_response_distribution_available"
        )
        rows.append({
            "packet_rank": candidate_row.get("packet_rank", ""),
            "readiness_rank": candidate_row.get("readiness_rank", ""),
            "bill_id": candidate_row.get("bill_id", ""),
            "public_law_number": candidate_row.get("public_law_number", ""),
            "policy_area": candidate_row.get("policy_area", ""),
            "sponsor_districts": candidate_row.get("sponsor_districts", ""),
            "target_issue_construct": candidate_row.get("target_issue_construct", ""),
            "candidate_policy_preference_item_ids": "; ".join(candidate_items),
            "candidate_policy_preference_item_count": str(len(candidate_items)),
            "candidate_items_with_response_distribution_count": str(len(overall_rows)),
            "candidate_item_year_distribution_rows": str(len(year_rows)),
            "source_item_response_observation_count": str(response_count),
            "source_item_blank_observation_count": str(blank_count),
            "observed_response_years": "; ".join(years),
            "observed_response_year_count": str(len(years)),
            "response_distribution_status": status,
            "exact_bill_topic_support_status": "no_exact_bill_topic_support_estimate",
            "support_direction_status": "raw_response_codes_not_directionally_recoded",
            "district_estimation_status": "no_mrp_or_small_area_estimate",
            "affected_group_item_status": "no_bill_text_specific_affected_group_item_acquired",
            "required_next_action": (
                "Review codebook response direction and candidate wording against the specific "
                "public-law bill text, then add respondent geography/MRP or other small-area "
                "estimation before using these raw response-code distributions as public-opinion evidence."
            ),
            "source_urls": source_urls(candidate_row, overall_rows),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], distribution_rows: list[dict[str, str]]) -> None:
    rows_with_distributions = [
        row for row in rows
        if row["response_distribution_status"]
        == "official_ces_policy_preference_raw_response_distributions_available_no_support_direction"
    ]
    rows_without_distributions = [
        row for row in rows
        if row["response_distribution_status"] == "no_candidate_item_response_distribution_available"
    ]
    unique_items = sorted({
        item
        for row in rows_with_distributions
        for item in split_values(row["candidate_policy_preference_item_ids"])
    })
    all_distribution_rows = [row for row in distribution_rows if row.get("year") == "all"]
    year_distribution_rows = [row for row in distribution_rows if row.get("year") != "all"]
    years = sorted({row["year"] for row in year_distribution_rows}, key=lambda value: int(value))
    attached_observations = sum(
        int(row["source_item_response_observation_count"])
        for row in rows_with_distributions
    )
    lines = [
        "# District Public-Opinion CES Policy Item Response Distribution Review",
        "",
        "This report joins queued district public-opinion source packets to unweighted raw response-code distributions from the official Cumulative CES Policy Preferences dataset. It is response-distribution context, not bill-topic public-support evidence.",
        "",
        f"- Packet rows reviewed: {len(rows)}",
        f"- Source policy-preference variables with overall distributions: {len(all_distribution_rows)}",
        f"- Source variable-year distribution rows: {len(year_distribution_rows)}",
        f"- Source years represented: {len(years)}",
        f"- Source year range: {years[0]}-{years[-1]}" if years else "- Source year range: none",
        f"- Rows with candidate raw response distributions: {len(rows_with_distributions)}",
        f"- Rows without candidate raw response distributions: {len(rows_without_distributions)}",
        f"- Unique candidate variable IDs with raw response distributions attached to packets: {len(unique_items)}",
        f"- Aggregate attached source item-response observations: {attached_observations}",
        "- Rows with exact bill-topic support estimates: 0",
        "- Rows with directionally recoded support/opposition estimates: 0",
        "- Rows with MRP or small-area district estimates: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Packet review:",
        "",
        "| Packet | Bill ID | Policy area | Items with distributions | Item-response observations | Status |",
        "| ---: | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['candidate_items_with_response_distribution_count']} | "
            f"{row['source_item_response_observation_count']} | "
            f"`{row['response_distribution_status']}` |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    candidate_review_rows = read_csv(CANDIDATE_REVIEW)
    distribution_rows = read_csv(RAW_DISTRIBUTIONS)
    if not candidate_review_rows:
        raise SystemExit(
            f"{CANDIDATE_REVIEW} is missing or empty; run make district-public-opinion-ces-policy-item-candidate-review first."
        )
    if not distribution_rows:
        raise SystemExit(
            f"{RAW_DISTRIBUTIONS} is missing or empty; run make build-district-public-opinion-ces-policy-item-response-distributions-raw first."
        )
    rows = build_rows(candidate_review_rows, distribution_rows)
    write_csv(rows)
    write_md(rows, distribution_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
