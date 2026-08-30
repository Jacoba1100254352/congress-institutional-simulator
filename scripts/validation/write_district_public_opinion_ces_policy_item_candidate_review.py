#!/usr/bin/env python3
"""Join CES policy-preference item candidates to public-opinion packets."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE_CROSSWALK = Path("reports/district-public-opinion-survey-source-crosswalk.csv")
RAW_CANDIDATES = Path("data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv")
OUT_CSV = Path("reports/district-public-opinion-ces-policy-item-candidate-review.csv")
OUT_MD = Path("reports/district-public-opinion-ces-policy-item-candidate-review.md")

FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "target_issue_construct",
    "primary_survey_source_family",
    "policy_preference_source_name",
    "policy_preference_dataset_doi",
    "policy_preference_dataset_version",
    "policy_preference_dataset_release_time",
    "candidate_policy_preference_item_ids",
    "candidate_policy_preference_item_count",
    "candidate_policy_preference_issue_areas",
    "candidate_policy_preference_short_labels",
    "candidate_item_review_status",
    "exact_bill_topic_support_status",
    "district_estimation_status",
    "affected_group_item_status",
    "required_next_action",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "CES policy-preference item-candidate review only; rows join queued "
    "public-law source packets to official Cumulative CES Policy Preferences "
    "variable IDs where a broad policy-area candidate exists. These candidate "
    "IDs are not source-reviewed exact bill-topic support items, not district "
    "support estimates, not MRP or small-area estimates, not bill-text-specific "
    "affected-population definitions, not affected-group support or harm, not "
    "public-benefit evidence, and not model validation."
)

MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; bill_topic_public_opinion; "
    "MRP_or_small_area_estimate; respondent_geography_merge; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "public_opinion_survey_source_crosswalk; "
    "official_dataverse_policy_preferences_metadata; "
    "official_policy_preferences_tabular_header; "
    "ces_policy_preferences_guide_candidate_item_review; "
    "district_public_opinion_ces_policy_item_candidate_review"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def candidates_by_policy_area(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row.get("official_header_present", "") != "1":
            raise SystemExit(
                f"{RAW_CANDIDATES}: {row.get('variable_id', '')}: official_header_present must be 1"
            )
        for policy_area in split_values(row.get("policy_area_targets", "")):
            result.setdefault(policy_area, []).append(row)
    for policy_area, area_rows in result.items():
        result[policy_area] = sorted(area_rows, key=lambda row: row.get("variable_id", ""))
    return result


def candidate_status(candidates: list[dict[str, str]]) -> str:
    if candidates:
        return "official_ces_policy_preference_candidate_items_found_no_bill_support_estimate"
    return "no_official_ces_policy_preference_candidate_item_for_policy_area"


def source_urls(candidates: list[dict[str, str]], packet: dict[str, str]) -> str:
    urls: list[str] = []
    for row in candidates:
        for field in ("source_url", "api_url", "data_download_url", "guide_download_url"):
            value = row.get(field, "").strip()
            if value and value not in urls:
                urls.append(value)
    for value in split_values(packet.get("source_urls", "")):
        if value and value not in urls:
            urls.append(value)
    return "; ".join(urls)


def build_rows(packet_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_area = candidates_by_policy_area(candidate_rows)
    rows: list[dict[str, str]] = []
    for packet in packet_rows:
        policy_area = packet.get("policy_area", "")
        candidates = by_area.get(policy_area, [])
        first = candidates[0] if candidates else {}
        candidate_ids = [row["variable_id"] for row in candidates]
        issue_areas = sorted({row["issue_area"] for row in candidates if row.get("issue_area")})
        short_labels = [f"{row['variable_id']}: {row['short_label']}" for row in candidates]
        rows.append({
            "packet_rank": packet.get("packet_rank", ""),
            "readiness_rank": packet.get("readiness_rank", ""),
            "bill_id": packet.get("bill_id", ""),
            "public_law_number": packet.get("public_law_number", ""),
            "policy_area": policy_area,
            "sponsor_districts": packet.get("sponsor_districts", ""),
            "target_issue_construct": packet.get("target_issue_construct", ""),
            "primary_survey_source_family": packet.get("primary_survey_source_family", ""),
            "policy_preference_source_name": first.get("source_name", "Cumulative CES Policy Preferences"),
            "policy_preference_dataset_doi": first.get("dataset_doi", ""),
            "policy_preference_dataset_version": first.get("dataset_version", ""),
            "policy_preference_dataset_release_time": first.get("dataset_release_time", ""),
            "candidate_policy_preference_item_ids": "; ".join(candidate_ids),
            "candidate_policy_preference_item_count": str(len(candidate_ids)),
            "candidate_policy_preference_issue_areas": "; ".join(issue_areas),
            "candidate_policy_preference_short_labels": "; ".join(short_labels),
            "candidate_item_review_status": candidate_status(candidates),
            "exact_bill_topic_support_status": "no_exact_bill_topic_support_estimate",
            "district_estimation_status": "no_mrp_or_small_area_estimate",
            "affected_group_item_status": "no_bill_text_specific_affected_group_item_acquired",
            "required_next_action": (
                "Review candidate variable wording against the specific public-law bill text, "
                "merge respondent geography from Cumulative CES Common Content where suitable, "
                "then build or import MRP/small-area estimates and bill-text-specific affected "
                "population support/harm measures before using any row as bill-topic public-opinion evidence."
            ),
            "source_urls": source_urls(candidates, packet),
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


def write_md(rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> None:
    rows_with_candidates = [
        row for row in rows
        if row["candidate_item_review_status"]
        == "official_ces_policy_preference_candidate_items_found_no_bill_support_estimate"
    ]
    rows_without_candidates = [
        row for row in rows
        if row["candidate_item_review_status"]
        == "no_official_ces_policy_preference_candidate_item_for_policy_area"
    ]
    policy_areas = sorted({row["policy_area"] for row in rows if row["policy_area"]})
    candidate_policy_areas = sorted({row["policy_area"] for row in rows_with_candidates})
    unique_candidate_items = sorted(
        {
            item
            for row in rows
            for item in split_values(row["candidate_policy_preference_item_ids"])
        }
    )
    source_issue_areas = sorted({row["issue_area"] for row in candidate_rows if row.get("issue_area")})
    lines = [
        "# District Public-Opinion CES Policy Item Candidate Review",
        "",
        "This report joins queued district public-opinion source packets to exact variable IDs from the official Cumulative CES Policy Preferences dataset. It is candidate item metadata, not bill-topic public-support evidence.",
        "",
        f"- Packet rows reviewed: {len(rows)}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Source policy-preference variables reviewed: {len(candidate_rows)}",
        f"- Source issue areas represented: {len(source_issue_areas)}",
        f"- Rows with official CES policy-preference candidate item IDs: {len(rows_with_candidates)}",
        f"- Rows without a candidate item in this CES policy-preferences source: {len(rows_without_candidates)}",
        f"- Unique candidate variable IDs attached to packets: {len(unique_candidate_items)}",
        "- Rows with exact bill-topic support estimates: 0",
        "- Rows with MRP or small-area district estimates: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Candidate-covered policy areas:",
        "",
    ]
    if candidate_policy_areas:
        for policy_area in candidate_policy_areas:
            lines.append(f"- {policy_area}")
    else:
        lines.append("- None")
    lines.extend([
        "",
        "Packet review:",
        "",
        "| Packet | Bill ID | Policy area | Candidate variables | Status |",
        "| ---: | --- | --- | --- | --- |",
    ])
    for row in rows:
        candidates = row["candidate_policy_preference_item_ids"] or "---"
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{candidates} | `{row['candidate_item_review_status']}` |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    packet_rows = read_csv(SOURCE_CROSSWALK)
    candidate_rows = read_csv(RAW_CANDIDATES)
    if not packet_rows:
        raise SystemExit(
            f"{SOURCE_CROSSWALK} is missing or empty; run make district-public-opinion-survey-source-crosswalk first."
        )
    if not candidate_rows:
        raise SystemExit(
            f"{RAW_CANDIDATES} is missing or empty; run make build-district-public-opinion-ces-policy-item-candidates-raw first."
        )
    rows = build_rows(packet_rows, candidate_rows)
    write_csv(rows)
    write_md(rows, candidate_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
