#!/usr/bin/env python3
"""Join CES guide/codebook direction rows to public-opinion packets."""

from __future__ import annotations

import csv
import json
from pathlib import Path


RESPONSE_DISTRIBUTION_REVIEW = Path(
    "reports/district-public-opinion-ces-policy-item-response-distribution-review.csv"
)
CODEBOOK_DIRECTION = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv"
)
OUT_CSV = Path("reports/district-public-opinion-ces-policy-item-codebook-direction-review.csv")
OUT_MD = Path("reports/district-public-opinion-ces-policy-item-codebook-direction-review.md")

CLAIM_BOUNDARY = (
    "CES policy-preference codebook-direction packet review only; rows join queued "
    "public-law source packets to official guide response labels or continuous-scale "
    "endpoint labels for Cumulative CES Policy Preferences candidate variables. "
    "The joined labels identify survey-item wording direction only. They are not "
    "bill-text-aligned support directions, not exact bill-topic public support "
    "estimates, not district support estimates, not MRP or small-area estimates, "
    "not bill-text-specific affected-population definitions, not affected-group "
    "support or harm, not public-benefit evidence, and not model validation."
)

MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; bill_text_direction_alignment_review; "
    "bill_topic_public_opinion; respondent_geography_merge; MRP_or_small_area_estimate; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "district_public_opinion_ces_policy_item_response_distribution_review; "
    "official_policy_preferences_guide_response_codebook_direction; "
    "district_public_opinion_ces_policy_item_codebook_direction_review"
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
    "candidate_items_with_codebook_direction_count",
    "candidate_items_with_binary_item_direction_count",
    "candidate_item_direction_types",
    "candidate_item_support_code_summary",
    "candidate_item_oppose_code_summary",
    "candidate_item_codebook_label_summary",
    "guide_codebook_direction_status",
    "support_direction_status",
    "exact_bill_topic_support_status",
    "bill_text_direction_alignment_status",
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


def source_urls(response_row: dict[str, str], direction_rows: list[dict[str, str]]) -> str:
    urls: list[str] = []
    for value in split_values(response_row.get("source_urls", "")):
        if value and value not in urls:
            urls.append(value)
    for row in direction_rows:
        for field in ("source_url", "guide_download_url"):
            value = row.get(field, "").strip()
            if value and value not in urls:
                urls.append(value)
    return "; ".join(urls)


def code_summary(rows: list[dict[str, str]], field: str) -> str:
    parts: list[str] = []
    for row in rows:
        codes = split_values(row.get(field, ""))
        if codes:
            parts.append(f"{row['variable_id']}={','.join(codes)}")
    return "; ".join(parts)


def label_summary(rows: list[dict[str, str]]) -> str:
    payload = []
    for row in rows:
        try:
            code_label_map = json.loads(row.get("codebook_code_label_map", "[]") or "[]")
        except json.JSONDecodeError:
            code_label_map = []
        payload.append({
            "variable_id": row.get("variable_id", ""),
            "direction_type": row.get("codebook_direction_type", ""),
            "code_label_map": code_label_map,
            "unmapped_observed_codes": split_values(row.get("unmapped_observed_codes", "")),
        })
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def support_direction_status(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "no_candidate_item_codebook_direction_available"
    binary_rows = [
        row for row in rows
        if row.get("codebook_direction_type") == "binary_item_support_oppose"
    ]
    if binary_rows:
        return "guide_item_wording_support_oppose_codes_available_no_bill_text_alignment"
    return "guide_codebook_labels_available_no_binary_support_direction"


def build_rows(
    response_review_rows: list[dict[str, str]],
    direction_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    direction_by_variable = {row["variable_id"]: row for row in direction_rows}
    rows: list[dict[str, str]] = []
    for response_row in response_review_rows:
        candidate_items = split_values(response_row.get("candidate_policy_preference_item_ids", ""))
        matched_direction_rows = [
            direction_by_variable[item]
            for item in candidate_items
            if item in direction_by_variable
        ]
        binary_direction_rows = [
            row for row in matched_direction_rows
            if row.get("codebook_direction_type") == "binary_item_support_oppose"
        ]
        direction_types = sorted({
            row.get("codebook_direction_type", "")
            for row in matched_direction_rows
            if row.get("codebook_direction_type", "")
        })
        status = (
            "official_ces_policy_preference_codebook_direction_review_available_no_bill_mapping"
            if matched_direction_rows
            else "no_candidate_item_codebook_direction_available"
        )
        rows.append({
            "packet_rank": response_row.get("packet_rank", ""),
            "readiness_rank": response_row.get("readiness_rank", ""),
            "bill_id": response_row.get("bill_id", ""),
            "public_law_number": response_row.get("public_law_number", ""),
            "policy_area": response_row.get("policy_area", ""),
            "sponsor_districts": response_row.get("sponsor_districts", ""),
            "target_issue_construct": response_row.get("target_issue_construct", ""),
            "candidate_policy_preference_item_ids": "; ".join(candidate_items),
            "candidate_policy_preference_item_count": str(len(candidate_items)),
            "candidate_items_with_codebook_direction_count": str(len(matched_direction_rows)),
            "candidate_items_with_binary_item_direction_count": str(len(binary_direction_rows)),
            "candidate_item_direction_types": "; ".join(direction_types),
            "candidate_item_support_code_summary": code_summary(matched_direction_rows, "item_support_codes"),
            "candidate_item_oppose_code_summary": code_summary(matched_direction_rows, "item_oppose_codes"),
            "candidate_item_codebook_label_summary": label_summary(matched_direction_rows),
            "guide_codebook_direction_status": status,
            "support_direction_status": support_direction_status(matched_direction_rows),
            "exact_bill_topic_support_status": "no_exact_bill_topic_support_estimate",
            "bill_text_direction_alignment_status": "no_bill_text_direction_alignment_review",
            "district_estimation_status": "no_mrp_or_small_area_estimate",
            "affected_group_item_status": "no_bill_text_specific_affected_group_item_acquired",
            "required_next_action": (
                "Review candidate item wording and item direction against the specific public-law "
                "bill text, then add respondent geography, microdata, MRP or other small-area "
                "estimation, and bill-text-specific affected-population/support/harm sources "
                "before treating these codebook directions as bill-topic public-opinion evidence."
            ),
            "source_urls": source_urls(response_row, matched_direction_rows),
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


def write_md(rows: list[dict[str, str]], direction_rows: list[dict[str, str]]) -> None:
    rows_with_direction = [
        row for row in rows
        if row["guide_codebook_direction_status"]
        == "official_ces_policy_preference_codebook_direction_review_available_no_bill_mapping"
    ]
    rows_without_direction = [
        row for row in rows
        if row["guide_codebook_direction_status"] == "no_candidate_item_codebook_direction_available"
    ]
    rows_with_binary_direction = [
        row for row in rows
        if int(row["candidate_items_with_binary_item_direction_count"] or "0") > 0
    ]
    unique_items = sorted({
        item
        for row in rows_with_direction
        for item in split_values(row["candidate_policy_preference_item_ids"])
    })
    unique_binary_items = sorted({
        item
        for row in rows_with_direction
        for item in split_values(row["candidate_policy_preference_item_ids"])
        for direction_row in direction_rows
        if direction_row.get("variable_id") == item
        and direction_row.get("codebook_direction_type") == "binary_item_support_oppose"
    })
    direction_types = sorted({
        direction_type
        for row in rows_with_direction
        for direction_type in split_values(row["candidate_item_direction_types"])
    })
    source_variables_with_labels = [
        row for row in direction_rows
        if row.get("guide_response_label_count") != "0"
    ]
    lines = [
        "# District Public-Opinion CES Policy Item Codebook Direction Review",
        "",
        "This report joins queued district public-opinion source packets to official guide response labels from the Cumulative CES Policy Preferences dataset. It records survey-item codebook direction only, not bill-topic public-support evidence.",
        "",
        f"- Packet rows reviewed: {len(rows)}",
        f"- Source policy-preference variables with guide labels or endpoints: {len(source_variables_with_labels)}",
        f"- Rows with candidate codebook direction review: {len(rows_with_direction)}",
        f"- Rows without candidate codebook direction review: {len(rows_without_direction)}",
        f"- Rows with at least one binary item-wording support/oppose direction: {len(rows_with_binary_direction)}",
        f"- Unique candidate variable IDs with codebook directions attached to packets: {len(unique_items)}",
        f"- Unique attached binary support/oppose candidate variable IDs: {len(unique_binary_items)}",
        f"- Candidate direction types represented: {'; '.join(direction_types) if direction_types else 'none'}",
        "- Rows with bill-text direction alignment: 0",
        "- Rows with exact bill-topic support estimates: 0",
        "- Rows with MRP or small-area district estimates: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Packet review:",
        "",
        "| Packet | Bill ID | Policy area | Items with codebook direction | Binary items | Status |",
        "| ---: | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['packet_rank']} | `{row['bill_id']}` | {row['policy_area']} | "
            f"{row['candidate_items_with_codebook_direction_count']} | "
            f"{row['candidate_items_with_binary_item_direction_count']} | "
            f"`{row['guide_codebook_direction_status']}` |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    response_review_rows = read_csv(RESPONSE_DISTRIBUTION_REVIEW)
    direction_rows = read_csv(CODEBOOK_DIRECTION)
    if not response_review_rows:
        raise SystemExit(
            f"{RESPONSE_DISTRIBUTION_REVIEW} is missing or empty; run make district-public-opinion-ces-policy-item-response-distribution-review first."
        )
    if not direction_rows:
        raise SystemExit(
            f"{CODEBOOK_DIRECTION} is missing or empty; run make build-district-public-opinion-ces-policy-item-codebook-direction-raw first."
        )
    rows = build_rows(response_review_rows, direction_rows)
    write_csv(rows)
    write_md(rows, direction_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
