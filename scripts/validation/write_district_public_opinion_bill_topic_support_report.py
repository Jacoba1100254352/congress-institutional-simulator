#!/usr/bin/env python3
"""Write the reviewed historical district bill-topic support report."""

from __future__ import annotations

import csv
from pathlib import Path


RAW_SUPPORT = Path(
    "data/validation/raw/district_public_opinion_bill_topic_support.csv"
)
ALIGNMENTS = Path("reports/district-public-opinion-bill-item-alignment-review.csv")
OUT_CSV = Path("reports/district-public-opinion-bill-topic-support.csv")
OUT_MD = Path("reports/district-public-opinion-bill-topic-support.md")

ALIGNED_STATUS = "reviewed_aligned_historical_issue_item"
AVAILABLE_STATUS = "historical_direct_weighted_district_issue_estimate_available"

FIELDNAMES = [
    "estimate_rank",
    "historical_support_row_id",
    "bill_id",
    "public_law_number",
    "bill_title",
    "policy_area",
    "sponsor_district_id",
    "survey_item_id",
    "survey_item_label",
    "survey_year",
    "annual_congress",
    "alignment_direction",
    "alignment_strength",
    "historical_related_issue_support_status",
    "exact_bill_support_status",
    "contemporaneous_support_status",
    "mrp_or_small_area_status",
    "estimate_method",
    "minimum_publishable_respondents",
    "response_respondents",
    "support_respondents",
    "oppose_respondents",
    "weighted_support_share",
    "unweighted_support_share",
    "effective_sample_size",
    "privacy_status",
    "temporal_alignment_status",
    "question_alignment_status",
    "geography_alignment_status",
    "uncertainty_status",
    "cumulative_dataset_doi",
    "cumulative_data_file_id",
    "cumulative_data_file_md5",
    "cumulative_access_file_size_bytes",
    "cumulative_access_file_sha256",
    "annual_dataset_doi",
    "annual_data_file_id",
    "annual_data_file_md5",
    "annual_access_file_size_bytes",
    "annual_access_file_sha256",
    "annual_question_field",
    "annual_question_wave",
    "annual_question_guide_file_id",
    "annual_question_guide_file_label",
    "annual_question_guide_file_md5",
    "annual_question_guide_printed_page",
    "annual_weight_field",
    "annual_weight_selection_status",
    "cross_source_validated_response_respondents",
    "cross_source_response_validation_status",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return fieldnames, rows


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def parse_int(value: str, label: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise SystemExit(f"{label} must be an integer, got {value!r}.") from exc


def parse_share(value: str, label: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise SystemExit(f"{label} must be numeric, got {value!r}.") from exc
    if not 0.0 <= parsed <= 1.0:
        raise SystemExit(f"{label} must be between zero and one, got {parsed}.")
    return parsed


def validate_raw_schema(fieldnames: list[str]) -> None:
    forbidden = {"case_id", "respondent_id", "v101"}
    leaked = sorted(forbidden & {field.lower() for field in fieldnames})
    if leaked:
        raise SystemExit(f"{RAW_SUPPORT}: respondent identifier columns are forbidden: {leaked}.")


def alignment_keys(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for row in rows:
        if row.get("manual_alignment_status", "").strip() != ALIGNED_STATUS:
            continue
        for variable_id in split_values(row.get("selected_variable_ids", "")):
            key = (row.get("bill_id", "").strip(), variable_id)
            if key in keys:
                raise SystemExit(f"{ALIGNMENTS}: duplicate positive bill-item key {key}.")
            keys.add(key)
    if not keys:
        raise SystemExit(f"{ALIGNMENTS}: no positive bill-item alignments are available.")
    return keys


def build_rows(
    raw_rows: list[dict[str, str]],
    positive_keys: set[tuple[str, str]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    represented_keys: set[tuple[str, str]] = set()
    for raw in raw_rows:
        key = (raw.get("bill_id", "").strip(), raw.get("survey_item_id", "").strip())
        if key not in positive_keys:
            raise SystemExit(f"{RAW_SUPPORT}: estimate lacks a current positive alignment: {key}.")
        represented_keys.add(key)
        estimate_key = (
            key[0],
            raw.get("sponsor_district_id", "").strip(),
            key[1],
            raw.get("survey_year", "").strip(),
        )
        if estimate_key in seen:
            raise SystemExit(f"{RAW_SUPPORT}: duplicate estimate key {estimate_key}.")
        seen.add(estimate_key)
        if raw.get("estimate_status", "").strip() != AVAILABLE_STATUS:
            continue
        response_n = parse_int(raw.get("published_response_respondents", ""), str(estimate_key))
        support_n = parse_int(raw.get("published_support_respondents", ""), str(estimate_key))
        oppose_n = parse_int(raw.get("published_oppose_respondents", ""), str(estimate_key))
        minimum_n = parse_int(raw.get("minimum_publishable_respondents", ""), str(estimate_key))
        if support_n + oppose_n > response_n:
            raise SystemExit(f"{RAW_SUPPORT}: support and oppose counts exceed responses for {estimate_key}.")
        if support_n + oppose_n < minimum_n:
            raise SystemExit(f"{RAW_SUPPORT}: published estimate is below its threshold for {estimate_key}.")
        parse_share(raw.get("weighted_support_share", ""), f"{estimate_key} weighted share")
        parse_share(raw.get("unweighted_support_share", ""), f"{estimate_key} unweighted share")
        try:
            effective_n = float(raw.get("effective_sample_size", ""))
        except ValueError as exc:
            raise SystemExit(f"{RAW_SUPPORT}: invalid effective sample size for {estimate_key}.") from exc
        if effective_n <= 0.0 or effective_n > support_n + oppose_n + 1e-6:
            raise SystemExit(f"{RAW_SUPPORT}: impossible effective sample size for {estimate_key}.")
        validated_response_n = parse_int(
            raw.get("cross_source_validated_response_respondents", ""),
            f"{estimate_key} cross-source response count",
        )
        if (
            validated_response_n <= 0
            or raw.get("annual_question_wave", "").strip() != "pre_election"
            or raw.get("annual_weight_selection_status", "").strip()
            != "official_validated_voter_pre_election_weight"
            or raw.get("cross_source_response_validation_status", "").strip()
            != "all_nonmissing_cumulative_responses_match_annual_question"
        ):
            raise SystemExit(
                f"{RAW_SUPPORT}: annual question or weight validation failed for {estimate_key}."
            )
        output.append({
            "estimate_rank": "",
            "historical_support_row_id": "|".join(estimate_key),
            "bill_id": key[0],
            "public_law_number": raw["public_law_number"].strip(),
            "bill_title": raw["bill_title"].strip(),
            "policy_area": raw["policy_area"].strip(),
            "sponsor_district_id": raw["sponsor_district_id"].strip(),
            "survey_item_id": key[1],
            "survey_item_label": raw["survey_item_label"].strip(),
            "survey_year": raw["survey_year"].strip(),
            "annual_congress": raw["annual_congress"].strip(),
            "alignment_direction": raw["alignment_direction"].strip(),
            "alignment_strength": raw["alignment_strength"].strip(),
            "historical_related_issue_support_status": (
                "privacy_thresholded_direct_weighted_district_estimate_available"
            ),
            "exact_bill_support_status": "not_measured",
            "contemporaneous_support_status": "not_measured_historical_pre_enactment_only",
            "mrp_or_small_area_status": "not_performed_direct_weighted_estimate_only",
            "estimate_method": raw["estimate_method"].strip(),
            "minimum_publishable_respondents": str(minimum_n),
            "response_respondents": str(response_n),
            "support_respondents": str(support_n),
            "oppose_respondents": str(oppose_n),
            "weighted_support_share": raw["weighted_support_share"].strip(),
            "unweighted_support_share": raw["unweighted_support_share"].strip(),
            "effective_sample_size": raw["effective_sample_size"].strip(),
            "privacy_status": raw["privacy_status"].strip(),
            "temporal_alignment_status": raw["temporal_alignment_status"].strip(),
            "question_alignment_status": raw["question_alignment_status"].strip(),
            "geography_alignment_status": raw["geography_alignment_status"].strip(),
            "uncertainty_status": raw["uncertainty_status"].strip(),
            "cumulative_dataset_doi": raw["cumulative_dataset_doi"].strip(),
            "cumulative_data_file_id": raw["cumulative_data_file_id"].strip(),
            "cumulative_data_file_md5": raw["cumulative_data_file_md5"].strip(),
            "cumulative_access_file_size_bytes": raw[
                "cumulative_access_file_size_bytes"
            ].strip(),
            "cumulative_access_file_sha256": raw[
                "cumulative_access_file_sha256"
            ].strip(),
            "annual_dataset_doi": raw["annual_dataset_doi"].strip(),
            "annual_data_file_id": raw["annual_data_file_id"].strip(),
            "annual_data_file_md5": raw["annual_data_file_md5"].strip(),
            "annual_access_file_size_bytes": raw[
                "annual_access_file_size_bytes"
            ].strip(),
            "annual_access_file_sha256": raw[
                "annual_access_file_sha256"
            ].strip(),
            "annual_question_field": raw["annual_question_field"].strip(),
            "annual_question_wave": raw["annual_question_wave"].strip(),
            "annual_question_guide_file_id": raw[
                "annual_question_guide_file_id"
            ].strip(),
            "annual_question_guide_file_label": raw[
                "annual_question_guide_file_label"
            ].strip(),
            "annual_question_guide_file_md5": raw[
                "annual_question_guide_file_md5"
            ].strip(),
            "annual_question_guide_printed_page": raw[
                "annual_question_guide_printed_page"
            ].strip(),
            "annual_weight_field": raw["annual_weight_field"].strip(),
            "annual_weight_selection_status": raw[
                "annual_weight_selection_status"
            ].strip(),
            "cross_source_validated_response_respondents": str(
                validated_response_n
            ),
            "cross_source_response_validation_status": raw[
                "cross_source_response_validation_status"
            ].strip(),
            "source_urls": raw["source_urls"].strip(),
            "evidence_layers": raw["evidence_layers"].strip(),
            "missing_links": raw["missing_links"].strip(),
            "claim_boundary": raw["claim_boundary"].strip(),
        })
    if represented_keys != positive_keys:
        raise SystemExit(
            f"{RAW_SUPPORT}: estimate coverage differs from positive alignments; "
            f"missing={sorted(positive_keys - represented_keys)}, "
            f"extra={sorted(represented_keys - positive_keys)}."
        )
    output.sort(
        key=lambda row: (
            row["bill_id"],
            row["sponsor_district_id"],
            row["survey_item_id"],
            row["survey_year"],
        )
    )
    for rank, row in enumerate(output, start=1):
        row["estimate_rank"] = str(rank)
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")


def write_markdown(
    rows: list[dict[str, str]],
    positive_alignment_count: int,
    reviewed_bill_count: int,
) -> None:
    bills = sorted({row["bill_id"] for row in rows})
    districts = sorted({row["sponsor_district_id"] for row in rows})
    variables = sorted({row["survey_item_id"] for row in rows})
    years = sorted({row["survey_year"] for row in rows})
    negative_dispositions = reviewed_bill_count - positive_alignment_count
    validated_response_count = sum(
        int(row["cross_source_validated_response_respondents"])
        for row in rows
    )
    weight_fields = "; ".join(
        f"{row['survey_year']}: {row['annual_weight_field']}"
        for row in rows
    )
    lines = [
        "# District Public-Opinion Bill Topic Support",
        "",
        "This report publishes privacy-thresholded historical district estimates only for bill-item links retained by the source review. It does not reinterpret broad policy-area proxies as bill-topic support.",
        "",
        f"- Source-reviewed bill-item alignments retained: {positive_alignment_count}",
        f"- Source-reviewed bill packets without a retained alignment: {negative_dispositions}",
        f"- Bills with a publishable historical related-issue estimate: {len(bills)}",
        f"- Districts represented: {len(districts)} ({'; '.join(districts)})",
        f"- Survey items represented: {len(variables)} ({'; '.join(variables)})",
        f"- Annual estimates represented: {len(rows)} ({'; '.join(years)})",
        "- Exact bill-wording estimates: 0",
        "- Contemporaneous estimates: 0",
        "- MRP or other small-area estimates: 0",
        "- Respondent-level records or identifiers published: 0",
        "- Annual question wave: pre-election for both estimates",
        f"- Nonmissing cumulative responses matched to the original annual questions: {validated_response_count}",
        f"- Validated-voter pre-election weights: {weight_fields}",
        "",
        "The annual estimates are kept separate. No pooled estimate is reported because the annual validated-voter weights and survey designs differ, and this layer does not implement a cross-year variance model.",
        "",
        "| Rank | Bill | District | Historical item | Year | Responses | Weighted support | Effective N | Status |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['estimate_rank']} | `{row['bill_id']}` {escape_markdown(row['bill_title'])} | "
            f"{row['sponsor_district_id']} | `{row['survey_item_id']}` | "
            f"{row['survey_year']} | {row['response_respondents']} | "
            f"{float(row['weighted_support_share']):.3f} | "
            f"{float(row['effective_sample_size']):.1f} | historical related-issue context only |"
        )
    lines.extend([
        "",
        f"Claim boundary: {rows[0]['claim_boundary'] if rows else 'No publishable estimates.'}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    raw_fieldnames, raw_rows = read_csv(RAW_SUPPORT)
    validate_raw_schema(raw_fieldnames)
    _, alignment_rows = read_csv(ALIGNMENTS)
    positive_keys = alignment_keys(alignment_rows)
    rows = build_rows(raw_rows, positive_keys)
    if not rows:
        raise SystemExit("No privacy-thresholded district bill-topic support rows are publishable.")
    write_csv(rows)
    write_markdown(
        rows,
        positive_alignment_count=len(positive_keys),
        reviewed_bill_count=len(alignment_rows),
    )
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
