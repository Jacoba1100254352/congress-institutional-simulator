#!/usr/bin/env python3
"""Build raw response-code distributions for CES policy-preference items."""

from __future__ import annotations

import csv
import json
import urllib.request
from collections import Counter, defaultdict
from io import TextIOWrapper
from pathlib import Path
from typing import TextIO


CANDIDATES = Path("data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv")
OUT_CSV = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
OUT_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.metadata.md"
)

CLAIM_BOUNDARY = (
    "Official CES policy-preference raw response-code distribution only; rows "
    "summarize unweighted observed response codes from the source tabular file "
    "for candidate policy-preference variables. They are not normalized support "
    "directions, not bill-topic public support estimates, not district support "
    "estimates, not MRP or small-area estimates, not bill-text-specific affected "
    "population definitions, not affected-group support or harm, not public-benefit "
    "evidence, and not model validation."
)

MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; response_codebook_direction_review; "
    "bill_topic_public_opinion; MRP_or_small_area_estimate; respondent_geography_merge; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "official_dataverse_policy_preferences_metadata; "
    "official_policy_preferences_tabular_header; "
    "official_policy_preferences_raw_response_code_distribution"
)

FIELDNAMES = [
    "source_family",
    "source_name",
    "dataset_doi",
    "dataset_version",
    "dataset_release_time",
    "dataset_license",
    "data_file_id",
    "data_file_label",
    "data_file_md5",
    "variable_id",
    "issue_area",
    "short_label",
    "year",
    "response_scope",
    "total_source_rows",
    "response_nonmissing_count",
    "response_blank_count",
    "observed_response_code_count",
    "observed_response_codes",
    "response_code_counts",
    "response_distribution_status",
    "source_url",
    "data_download_url",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_candidates() -> list[dict[str, str]]:
    if not CANDIDATES.exists():
        raise SystemExit(
            f"{CANDIDATES} is missing; run make build-district-public-opinion-ces-policy-item-candidates-raw first."
        )
    with CANDIDATES.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{CANDIDATES} is empty")
    return rows


def response_code_sort_key(value: str) -> tuple[int, float | str]:
    try:
        return (0, float(value))
    except ValueError:
        return (1, value)


def open_data_stream(url: str) -> TextIO:
    request = urllib.request.Request(url, headers={"User-Agent": "congress-institutional-simulator/validation"})
    response = urllib.request.urlopen(request, timeout=120)
    return TextIOWrapper(response, encoding="utf-8", newline="")


def summarize_source(
    candidate_rows: list[dict[str, str]],
) -> tuple[
    dict[str, int],
    dict[tuple[str, str], Counter[str]],
    dict[str, Counter[str]],
]:
    variables = [row["variable_id"] for row in candidate_rows]
    data_url = candidate_rows[0]["data_download_url"]
    rows_by_year: dict[str, int] = defaultdict(int)
    counts_by_year_variable: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    counts_by_variable: dict[str, Counter[str]] = defaultdict(Counter)
    with open_data_stream(data_url) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            raise SystemExit("CES policy-preference data file has no header")
        missing_variables = sorted(set(variables) - set(reader.fieldnames))
        if missing_variables:
            raise SystemExit(f"CES policy-preference data file missing variables: {missing_variables}")
        for source_row in reader:
            year = source_row.get("year", "").strip()
            if year.endswith(".0"):
                year = year[:-2]
            if not year:
                year = "unknown"
            rows_by_year[year] += 1
            for variable in variables:
                value = source_row.get(variable, "").strip()
                if not value:
                    value = "__blank__"
                counts_by_year_variable[(year, variable)][value] += 1
                counts_by_variable[variable][value] += 1
    return rows_by_year, counts_by_year_variable, counts_by_variable


def distribution_fields(counter: Counter[str], total_rows: int) -> dict[str, str]:
    nonmissing = sum(count for value, count in counter.items() if value != "__blank__")
    blank = counter.get("__blank__", 0)
    observed_codes = sorted(
        (value for value in counter if value != "__blank__"),
        key=response_code_sort_key,
    )
    code_counts = [
        {"code": code, "count": counter[code]}
        for code in observed_codes
    ]
    return {
        "total_source_rows": str(total_rows),
        "response_nonmissing_count": str(nonmissing),
        "response_blank_count": str(blank),
        "observed_response_code_count": str(len(observed_codes)),
        "observed_response_codes": "; ".join(observed_codes),
        "response_code_counts": json.dumps(code_counts, separators=(",", ":")),
        "response_distribution_status": (
            "official_raw_response_code_distribution_available"
            if nonmissing > 0
            else "official_variable_present_no_nonmissing_responses_in_scope"
        ),
    }


def build_rows(candidate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_year, counts_by_year_variable, counts_by_variable = summarize_source(candidate_rows)
    total_rows = sum(rows_by_year.values())
    source_years = sorted(rows_by_year, key=response_code_sort_key)
    rows: list[dict[str, str]] = []
    for candidate in sorted(candidate_rows, key=lambda row: row["variable_id"]):
        variable = candidate["variable_id"]
        common = {
            "source_family": candidate["source_family"],
            "source_name": candidate["source_name"],
            "dataset_doi": candidate["dataset_doi"],
            "dataset_version": candidate["dataset_version"],
            "dataset_release_time": candidate["dataset_release_time"],
            "dataset_license": candidate["dataset_license"],
            "data_file_id": candidate["data_file_id"],
            "data_file_label": candidate["data_file_label"],
            "data_file_md5": candidate["data_file_md5"],
            "variable_id": variable,
            "issue_area": candidate["issue_area"],
            "short_label": candidate["short_label"],
            "source_url": candidate["source_url"],
            "data_download_url": candidate["data_download_url"],
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({
            **common,
            "year": "all",
            "response_scope": "all_available_years_unweighted_raw_codes",
            **distribution_fields(counts_by_variable[variable], total_rows),
        })
        for year in source_years:
            rows.append({
                **common,
                "year": year,
                "response_scope": "single_year_unweighted_raw_codes",
                **distribution_fields(counts_by_year_variable[(year, variable)], rows_by_year[year]),
            })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    all_rows = [row for row in rows if row["year"] == "all"]
    year_rows = [row for row in rows if row["year"] != "all"]
    source_years = sorted({row["year"] for row in year_rows}, key=response_code_sort_key)
    variables_with_responses = [
        row for row in all_rows
        if int(row["response_nonmissing_count"]) > 0
    ]
    total_source_rows = all_rows[0]["total_source_rows"] if all_rows else "0"
    total_nonmissing = sum(int(row["response_nonmissing_count"]) for row in all_rows)
    lines = [
        "# District Public-Opinion CES Policy Item Response Distributions Metadata",
        "",
        f"Source: Cumulative CES Policy Preferences (`10.7910/DVN/OSXDQO`).",
        "",
        f"Official source rows streamed: {total_source_rows}",
        f"Official policy variables summarized: {len(all_rows)}",
        f"Variables with at least one observed response: {len(variables_with_responses)}",
        f"Source years represented: {len(source_years)}",
        f"Source year range: {source_years[0]}-{source_years[-1]}" if source_years else "Source year range: none",
        f"Variable-year distribution rows: {len(year_rows)}",
        f"Aggregate variable-level nonmissing response observations: {total_nonmissing}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Rows are unweighted raw response-code distributions. Response codes are not recoded into support/opposition direction here.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    candidate_rows = read_candidates()
    rows = build_rows(candidate_rows)
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
