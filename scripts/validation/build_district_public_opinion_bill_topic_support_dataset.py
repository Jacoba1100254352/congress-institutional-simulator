#!/usr/bin/env python3
"""Build aggregate historical district issue support for reviewed bill-item links."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import urllib.request
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Iterator, TextIO

from reproducible_metadata import write_reproducible_metadata


ALIGNMENTS = Path("reports/district-public-opinion-bill-item-alignment-review.csv")
CODEBOOK = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv"
)
RESPONSE_DISTRIBUTIONS = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
OUT_CSV = Path(
    "data/validation/raw/district_public_opinion_bill_topic_support.csv"
)
OUT_METADATA = Path(
    "data/validation/raw/district_public_opinion_bill_topic_support.metadata.md"
)

ALIGNED_STATUS = "reviewed_aligned_historical_issue_item"
DEFAULT_MINIMUM_RESPONDENTS = 30
USER_AGENT = "CongressInstitutionalSimulator/district-bill-topic-support-audit"
FILE_API = "https://dataverse.harvard.edu/api/files/{file_id}"
ACCESS_API = "https://dataverse.harvard.edu/api/access/datafile/{file_id}"
WEIGHT_GUIDANCE_URL = "https://cces.gov.harvard.edu/frequently-asked-questions"

CUMULATIVE_DATASET_DOI = "10.7910/DVN/OSXDQO"
CUMULATIVE_DATASET_VERSION = "3.0"
CUMULATIVE_DATASET_RELEASE_TIME = "2023-01-18T18:03:54Z"
CUMULATIVE_DATASET_LICENSE = "CC0 1.0"
CUMULATIVE_FILE_ID = "6898233"
CUMULATIVE_FILE_LABEL = "cumulative_ces_policy_preferences.tab"
CUMULATIVE_FILE_MD5 = "aece03350d7b480d5e159f2c740a6ea0"
CUMULATIVE_ACCESS_FILE_SIZE_BYTES = 55_810_343
CUMULATIVE_ACCESS_FILE_SHA256 = (
    "6f26e0ca719383b9f5de1a86df4f2164a2b65cba9060f5e1ce8640204efc6dfd"
)
CUMULATIVE_DATA_URL = ACCESS_API.format(file_id=CUMULATIVE_FILE_ID)
CUMULATIVE_SOURCE_URL = (
    "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:"
    f"{CUMULATIVE_DATASET_DOI}"
)

CLAIM_BOUNDARY = (
    "Aggregate historical district issue-support context only. Each published row "
    "joins an official Cumulative CES policy-preference response to annual CCES "
    "Common Content geography and validated-voter weights, then reports only a "
    "district aggregate that meets the minimum respondent threshold. The survey "
    "item is directionally related to the bill but is not the bill wording, and the "
    "estimate predates enactment. It is a direct weighted descriptive estimate, not "
    "MRP, not a design-based uncertainty estimate, not contemporaneous bill support, "
    "not affected-group support or harm, not public benefit, not causal "
    "representation, and not model validation."
)

EVIDENCE_LAYERS = (
    "official_govinfo_billstatus_with_crs_summary; "
    "source_reviewed_historical_issue_item_alignment; "
    "official_cumulative_ces_policy_preference_response; "
    "official_annual_cces_question_wave_and_weight_guidance; "
    "official_annual_cces_common_content_geography; "
    "official_annual_cces_validated_voter_weight; "
    "cross_source_annual_question_response_equivalence; "
    "privacy_thresholded_direct_weighted_district_issue_estimate"
)

MISSING_LINKS = (
    "exact_bill_wording_survey_item; exact_bill_wording_support; "
    "contemporaneous_bill_support; "
    "MRP_or_small_area_estimate; district_boundary_crosswalk_validation; "
    "design_based_standard_error; bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

STATE_FIPS = {
    "AL": "1", "AK": "2", "AZ": "4", "AR": "5", "CA": "6", "CO": "8",
    "CT": "9", "DE": "10", "DC": "11", "FL": "12", "GA": "13", "HI": "15",
    "ID": "16", "IL": "17", "IN": "18", "IA": "19", "KS": "20", "KY": "21",
    "LA": "22", "ME": "23", "MD": "24", "MA": "25", "MI": "26", "MN": "27",
    "MS": "28", "MO": "29", "MT": "30", "NE": "31", "NV": "32", "NH": "33",
    "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46",
    "TN": "47", "TX": "48", "UT": "49", "VT": "50", "VA": "51", "WA": "53",
    "WV": "54", "WI": "55", "WY": "56",
}

FIELDNAMES = [
    "bill_id",
    "public_law_number",
    "policy_area",
    "bill_title",
    "sponsor_district_id",
    "sponsor_state_fips",
    "sponsor_district_number",
    "survey_item_id",
    "survey_item_label",
    "survey_item_support_codes",
    "survey_item_oppose_codes",
    "alignment_direction",
    "alignment_strength",
    "survey_year",
    "annual_congress",
    "estimate_method",
    "estimate_scope",
    "temporal_alignment_status",
    "question_alignment_status",
    "geography_alignment_status",
    "minimum_publishable_respondents",
    "estimate_status",
    "privacy_status",
    "cumulative_source_rows_in_year",
    "cumulative_item_nonmissing_responses_in_year",
    "annual_source_rows",
    "annual_district_source_rows",
    "annual_district_joined_rows",
    "published_response_respondents",
    "published_support_respondents",
    "published_oppose_respondents",
    "published_other_response_respondents",
    "published_invalid_weight_respondents",
    "unweighted_support_share",
    "weighted_support_share",
    "sum_analysis_weights",
    "sum_squared_analysis_weights",
    "effective_sample_size",
    "uncertainty_status",
    "cumulative_dataset_doi",
    "cumulative_dataset_version",
    "cumulative_dataset_release_time",
    "cumulative_dataset_license",
    "cumulative_data_file_id",
    "cumulative_data_file_label",
    "cumulative_data_file_md5",
    "cumulative_access_file_size_bytes",
    "cumulative_access_file_sha256",
    "annual_dataset_doi",
    "annual_dataset_version",
    "annual_dataset_release_time",
    "annual_dataset_license",
    "annual_data_file_id",
    "annual_data_file_label",
    "annual_data_file_md5",
    "annual_access_file_size_bytes",
    "annual_access_file_sha256",
    "annual_case_id_field",
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
    "annual_state_field",
    "annual_district_field",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


@dataclass(frozen=True)
class AnnualSource:
    year: str
    congress: str
    dataset_doi: str
    dataset_version: str
    dataset_release_time: str
    dataset_license: str
    file_id: str
    file_label: str
    file_md5: str
    access_file_size_bytes: int
    access_file_sha256: str
    case_id_field: str
    state_field: str
    district_field: str

    @property
    def data_url(self) -> str:
        return ACCESS_API.format(file_id=self.file_id)

    @property
    def source_url(self) -> str:
        return (
            "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:"
            f"{self.dataset_doi}"
        )


ANNUAL_SOURCES = {
    "2012": AnnualSource(
        year="2012",
        congress="113",
        dataset_doi="10.7910/DVN/HQEVPK",
        dataset_version="9.0",
        dataset_release_time="2017-07-16T20:29:53Z",
        dataset_license="CC0 1.0",
        file_id="2500154",
        file_label="CCES12_Common_VV.tab",
        file_md5="b89a059a4a41125811ebb496e5983b6a",
        access_file_size_bytes=116_562_350,
        access_file_sha256=(
            "7f4ac9d7d0945b5fa65b86d6e19c8e4c770f1edfa3539b3f8653c2d54d6e2b88"
        ),
        case_id_field="V101",
        state_field="inputstate",
        district_field="cdid113",
    ),
    "2016": AnnualSource(
        year="2016",
        congress="115",
        dataset_doi="10.7910/DVN/GDF6Z0",
        dataset_version="5.0",
        dataset_release_time="2025-01-06T16:29:38Z",
        dataset_license="CC0 1.0",
        file_id="3123547",
        file_label="CCES16_Common_OUTPUT_Feb2018_VV.tab",
        file_md5="dc61fe62ab7b44b4f4f613b9ee72eeb1",
        access_file_size_bytes=134_761_608,
        access_file_sha256=(
            "893c72d8d9e0b53ea640ea82b6db346ed424be6fc9fbb0c5c154feaf3eb46299"
        ),
        case_id_field="V101",
        state_field="inputstate",
        district_field="cdid115",
    ),
}


@dataclass(frozen=True)
class AnnualItemSource:
    year: str
    variable_id: str
    question_field: str
    question_wave: str
    weight_field: str
    weight_selection_status: str
    guide_file_id: str
    guide_file_label: str
    guide_file_md5: str
    guide_printed_page: str

    @property
    def guide_data_url(self) -> str:
        return ACCESS_API.format(file_id=self.guide_file_id)


ANNUAL_ITEM_SOURCES = {
    ("2012", "gaymarriage_legalize"): AnnualItemSource(
        year="2012",
        variable_id="gaymarriage_legalize",
        question_field="CC326",
        question_wave="pre_election",
        weight_field="weight_vv",
        weight_selection_status="official_validated_voter_pre_election_weight",
        guide_file_id="2688939",
        guide_file_label="cces_guide_2012.pdf",
        guide_file_md5="09fe9f595508c5b4254c2a3bb8f77871",
        guide_printed_page="61",
    ),
    ("2016", "gaymarriage_legalize"): AnnualItemSource(
        year="2016",
        variable_id="gaymarriage_legalize",
        question_field="CC16_335",
        question_wave="pre_election",
        weight_field="commonweight_vv",
        weight_selection_status="official_validated_voter_pre_election_weight",
        guide_file_id="10803737",
        guide_file_label="CCES Guide 2016.pdf",
        guide_file_md5="f3df4a99c753ed25472c8d704ae0b458",
        guide_printed_page="83",
    ),
}


@dataclass(frozen=True)
class EstimateTask:
    bill_id: str
    public_law_number: str
    policy_area: str
    bill_title: str
    district_id: str
    state_fips: str
    district_number: str
    variable_id: str
    item_label: str
    support_codes: frozenset[str]
    oppose_codes: frozenset[str]
    alignment_direction: str
    alignment_strength: str
    year: str


@dataclass
class EstimateAccumulator:
    district_source_rows: int = 0
    joined_rows: int = 0
    response_respondents: int = 0
    support_respondents: int = 0
    oppose_respondents: int = 0
    other_response_respondents: int = 0
    invalid_weight_respondents: int = 0
    weighted_support: float = 0.0
    sum_weights: float = 0.0
    sum_squared_weights: float = 0.0


class HashingReader(io.RawIOBase):
    """Stream bytes to the parser while retaining byte count and SHA-256."""

    def __init__(self, raw: BinaryIO) -> None:
        super().__init__()
        self.raw = raw
        self.digest = hashlib.sha256()
        self.byte_count = 0

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: bytearray) -> int:
        data = self.raw.read(len(buffer))
        if not data:
            return 0
        self.digest.update(data)
        self.byte_count += len(data)
        buffer[: len(data)] = data
        return len(data)

    def close(self) -> None:
        if not self.closed:
            self.raw.close()
        super().close()

    def hexdigest(self) -> str:
        return self.digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def normalize_integer(value: str) -> str:
    value = value.strip()
    match = re.fullmatch(r"([+-]?\d+)\.0+", value)
    return match.group(1) if match else value


def normalize_case_id(value: str) -> str:
    return normalize_integer(value)


def normalize_response_code(value: str) -> str:
    return normalize_integer(value)


def parse_positive_weight(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed) or parsed <= 0.0:
        return None
    return parsed


def parse_district_id(value: str) -> tuple[str, str]:
    parts = value.strip().upper().split("-", maxsplit=1)
    if len(parts) != 2 or parts[0] not in STATE_FIPS:
        raise SystemExit(f"Unsupported sponsor district identifier {value!r}.")
    state, district = parts
    if not district.isdigit():
        raise SystemExit(
            f"Sponsor district {value!r} is not numeric; add an explicit annual geography mapping."
        )
    return STATE_FIPS[state], str(int(district))


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if payload.get("status") != "OK":
        raise SystemExit(f"Official source metadata request failed for {url}.")
    return payload


def file_checksum(data_file: dict[str, Any]) -> str:
    checksum = data_file.get("checksum")
    if isinstance(checksum, dict) and checksum.get("value"):
        return str(checksum["value"])
    return str(data_file.get("md5", ""))


def validate_file_metadata(file_id: str, expected_label: str, expected_md5: str) -> None:
    payload = fetch_json(FILE_API.format(file_id=file_id))
    wrapper = payload.get("data")
    if not isinstance(wrapper, dict):
        raise SystemExit(f"Official file metadata for {file_id} has no data object.")
    data_file = wrapper.get("dataFile")
    if not isinstance(data_file, dict):
        raise SystemExit(f"Official file metadata for {file_id} has no dataFile object.")
    actual_id = str(data_file.get("id", ""))
    actual_label = str(wrapper.get("label") or data_file.get("filename", ""))
    actual_md5 = file_checksum(data_file)
    if (actual_id, actual_label, actual_md5) != (file_id, expected_label, expected_md5):
        raise SystemExit(
            f"Pinned source drift for file {file_id}: "
            f"expected {expected_label}/{expected_md5}, got {actual_label}/{actual_md5}."
        )


def verify_download(
    actual_size: int,
    actual_sha256: str,
    expected_size: int,
    expected_sha256: str,
    label: str,
) -> None:
    if actual_size != expected_size or actual_sha256.lower() != expected_sha256.lower():
        raise SystemExit(
            f"Downloaded source byte drift for {label}: expected "
            f"{expected_size} bytes/{expected_sha256}, got "
            f"{actual_size} bytes/{actual_sha256}."
        )


@contextmanager
def open_data_stream(
    url: str,
    expected_size: int,
    expected_sha256: str,
    label: str,
) -> Iterator[TextIO]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    response = urllib.request.urlopen(request, timeout=180)
    hashing_reader = HashingReader(response)
    handle = io.TextIOWrapper(
        io.BufferedReader(hashing_reader),
        encoding="utf-8-sig",
        newline="",
    )
    try:
        yield handle
        if handle.read(1):
            raise SystemExit(f"Source parser did not consume the complete file for {label}.")
        verify_download(
            hashing_reader.byte_count,
            hashing_reader.hexdigest(),
            expected_size,
            expected_sha256,
            label,
        )
    finally:
        handle.close()


def codebook_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        variable_id = row.get("variable_id", "").strip()
        if not variable_id or variable_id in result:
            raise SystemExit(f"{CODEBOOK}: empty or duplicate variable_id {variable_id!r}.")
        result[variable_id] = row
    return result


def response_distribution_index(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        year = row.get("year", "").strip()
        if year == "all":
            continue
        key = (year, row.get("variable_id", "").strip())
        if not key[1] or key in result:
            raise SystemExit(f"{RESPONSE_DISTRIBUTIONS}: empty or duplicate year-variable {key}.")
        result[key] = row
    return result


def build_tasks(
    alignment_rows: list[dict[str, str]],
    codebook_rows: list[dict[str, str]],
) -> list[EstimateTask]:
    codebooks = codebook_index(codebook_rows)
    tasks: list[EstimateTask] = []
    seen: set[tuple[str, str, str, str]] = set()
    for alignment in alignment_rows:
        if alignment.get("manual_alignment_status", "").strip() != ALIGNED_STATUS:
            continue
        districts = split_values(alignment.get("sponsor_districts", ""))
        variables = split_values(alignment.get("selected_variable_ids", ""))
        if not districts or not variables:
            raise SystemExit(
                f"{ALIGNMENTS}: positive alignment {alignment.get('bill_id', '')} lacks district or item."
            )
        for district_id in districts:
            state_fips, district_number = parse_district_id(district_id)
            for variable_id in variables:
                codebook = codebooks.get(variable_id)
                if codebook is None:
                    raise SystemExit(f"{ALIGNMENTS}: selected variable {variable_id} lacks codebook evidence.")
                support_codes = frozenset(
                    normalize_response_code(value)
                    for value in split_values(codebook.get("item_support_codes", ""))
                )
                oppose_codes = frozenset(
                    normalize_response_code(value)
                    for value in split_values(codebook.get("item_oppose_codes", ""))
                )
                if not support_codes or not oppose_codes or support_codes & oppose_codes:
                    raise SystemExit(
                        f"{CODEBOOK}: {variable_id} needs disjoint support and oppose codes."
                    )
                source_years = set(split_values(codebook.get("guide_years_in_data", "")))
                configured_years = sorted(source_years & set(ANNUAL_SOURCES))
                if not configured_years:
                    raise SystemExit(
                        f"{CODEBOOK}: {variable_id} has no year with a configured annual geography source."
                    )
                for year in configured_years:
                    key = (alignment["bill_id"], district_id, variable_id, year)
                    if key in seen:
                        raise SystemExit(f"Duplicate district support task {key}.")
                    seen.add(key)
                    tasks.append(EstimateTask(
                        bill_id=alignment["bill_id"].strip(),
                        public_law_number=alignment["public_law_number"].strip(),
                        policy_area=alignment["policy_area"].strip(),
                        bill_title=alignment["display_title"].strip(),
                        district_id=district_id,
                        state_fips=state_fips,
                        district_number=district_number,
                        variable_id=variable_id,
                        item_label=codebook["guide_item_description"].strip(),
                        support_codes=support_codes,
                        oppose_codes=oppose_codes,
                        alignment_direction=alignment["alignment_direction"].strip(),
                        alignment_strength=alignment["alignment_strength"].strip(),
                        year=year,
                    ))
    if not tasks:
        raise SystemExit(f"{ALIGNMENTS}: no positive historical issue-item alignment is available.")
    return sorted(
        tasks,
        key=lambda task: (task.bill_id, task.district_id, task.variable_id, task.year),
    )


def task_key(task: EstimateTask) -> tuple[str, str, str, str]:
    return task.bill_id, task.district_id, task.variable_id, task.year


def item_source_for(task: EstimateTask) -> AnnualItemSource:
    key = (task.year, task.variable_id)
    source = ANNUAL_ITEM_SOURCES.get(key)
    if source is None:
        raise SystemExit(
            f"No annual question-wave and weight mapping is configured for {key}."
        )
    if source.question_wave == "pre_election" and source.weight_field.endswith("_post"):
        raise SystemExit(f"Pre-election item {key} is configured with a post-election weight.")
    if source.question_wave == "post_election" and not source.weight_field.endswith("_post"):
        raise SystemExit(f"Post-election item {key} is configured without a post-election weight.")
    if source.question_wave not in {"pre_election", "post_election"}:
        raise SystemExit(f"Annual item {key} has unsupported wave {source.question_wave!r}.")
    return source


def row_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("sponsor_district_id", "").strip(),
        row.get("survey_item_id", "").strip(),
        row.get("survey_year", "").strip(),
    )


def expected_cache_fields(
    task: EstimateTask,
    source: AnnualSource,
    item_source: AnnualItemSource,
    minimum_respondents: int,
) -> dict[str, str]:
    return {
        "bill_id": task.bill_id,
        "public_law_number": task.public_law_number,
        "policy_area": task.policy_area,
        "bill_title": task.bill_title,
        "sponsor_district_id": task.district_id,
        "sponsor_state_fips": task.state_fips,
        "sponsor_district_number": task.district_number,
        "survey_item_id": task.variable_id,
        "survey_item_label": task.item_label,
        "survey_item_support_codes": "; ".join(sorted(task.support_codes)),
        "survey_item_oppose_codes": "; ".join(sorted(task.oppose_codes)),
        "alignment_direction": task.alignment_direction,
        "alignment_strength": task.alignment_strength,
        "survey_year": task.year,
        "annual_congress": source.congress,
        "estimate_method": "annual_cces_direct_weighted_descriptive_estimate",
        "estimate_scope": "sponsor_district_historical_related_issue_context",
        "temporal_alignment_status": "historical_pre_enactment_issue_context",
        "question_alignment_status": "related_issue_item_not_exact_bill_wording",
        "geography_alignment_status": (
            "same_state_district_number_post_2010_apportionment_cycle_"
            "without_boundary_file_crosswalk"
        ),
        "minimum_publishable_respondents": str(minimum_respondents),
        "uncertainty_status": (
            "descriptive_point_estimate_only_no_design_based_standard_error"
        ),
        "cumulative_dataset_doi": CUMULATIVE_DATASET_DOI,
        "cumulative_dataset_version": CUMULATIVE_DATASET_VERSION,
        "cumulative_dataset_release_time": CUMULATIVE_DATASET_RELEASE_TIME,
        "cumulative_dataset_license": CUMULATIVE_DATASET_LICENSE,
        "cumulative_data_file_id": CUMULATIVE_FILE_ID,
        "cumulative_data_file_label": CUMULATIVE_FILE_LABEL,
        "cumulative_data_file_md5": CUMULATIVE_FILE_MD5,
        "cumulative_access_file_size_bytes": str(
            CUMULATIVE_ACCESS_FILE_SIZE_BYTES
        ),
        "cumulative_access_file_sha256": CUMULATIVE_ACCESS_FILE_SHA256,
        "annual_dataset_doi": source.dataset_doi,
        "annual_dataset_version": source.dataset_version,
        "annual_dataset_release_time": source.dataset_release_time,
        "annual_dataset_license": source.dataset_license,
        "annual_data_file_id": source.file_id,
        "annual_data_file_label": source.file_label,
        "annual_data_file_md5": source.file_md5,
        "annual_access_file_size_bytes": str(source.access_file_size_bytes),
        "annual_access_file_sha256": source.access_file_sha256,
        "annual_case_id_field": source.case_id_field,
        "annual_question_field": item_source.question_field,
        "annual_question_wave": item_source.question_wave,
        "annual_question_guide_file_id": item_source.guide_file_id,
        "annual_question_guide_file_label": item_source.guide_file_label,
        "annual_question_guide_file_md5": item_source.guide_file_md5,
        "annual_question_guide_printed_page": item_source.guide_printed_page,
        "annual_weight_field": item_source.weight_field,
        "annual_weight_selection_status": item_source.weight_selection_status,
        "cross_source_response_validation_status": (
            "all_nonmissing_cumulative_responses_match_annual_question"
        ),
        "annual_state_field": source.state_field,
        "annual_district_field": source.district_field,
        "source_urls": "; ".join([
            CUMULATIVE_SOURCE_URL,
            CUMULATIVE_DATA_URL,
            source.source_url,
            source.data_url,
            item_source.guide_data_url,
            WEIGHT_GUIDANCE_URL,
        ]),
        "evidence_layers": EVIDENCE_LAYERS,
        "missing_links": MISSING_LINKS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def existing_output_matches(
    tasks: list[EstimateTask],
    minimum_respondents: int,
) -> bool:
    if not OUT_CSV.exists():
        return False
    try:
        with OUT_CSV.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDNAMES:
                return False
            rows = list(reader)
    except (OSError, csv.Error):
        return False
    if len(rows) != len(tasks):
        return False
    rows_by_key: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = row_key(row)
        if not all(key) or key in rows_by_key:
            return False
        rows_by_key[key] = row
    if set(rows_by_key) != {task_key(task) for task in tasks}:
        return False

    available_status = "historical_direct_weighted_district_issue_estimate_available"
    suppressed_status = "historical_district_issue_estimate_suppressed_below_threshold"
    published_fields = (
        "published_response_respondents",
        "published_support_respondents",
        "published_oppose_respondents",
        "published_other_response_respondents",
        "published_invalid_weight_respondents",
        "unweighted_support_share",
        "weighted_support_share",
        "sum_analysis_weights",
        "sum_squared_analysis_weights",
        "effective_sample_size",
    )
    for task in tasks:
        row = rows_by_key[task_key(task)]
        source = ANNUAL_SOURCES[task.year]
        item_source = item_source_for(task)
        if any(
            row.get(field, "").strip() != expected
            for field, expected in expected_cache_fields(
                task, source, item_source, minimum_respondents
            ).items()
        ):
            return False
        if (
            row.get("cross_source_validated_response_respondents", "").strip()
            != row.get("cumulative_item_nonmissing_responses_in_year", "").strip()
        ):
            return False
        status = row.get("estimate_status", "").strip()
        if status == available_status:
            if any(not row.get(field, "").strip() for field in published_fields):
                return False
            expected_privacy = (
                f"aggregate_only_minimum_n_{minimum_respondents}_met_no_case_ids_written"
            )
        elif status == suppressed_status:
            if any(row.get(field, "").strip() for field in published_fields):
                return False
            expected_privacy = (
                f"aggregate_suppressed_below_minimum_n_{minimum_respondents}_"
                "no_case_ids_written"
            )
        else:
            return False
        if row.get("privacy_status", "").strip() != expected_privacy:
            return False
    return True


def read_cumulative_responses(
    handle: TextIO,
    tasks: list[EstimateTask],
) -> tuple[
    dict[tuple[str, str], dict[str, str]],
    dict[str, int],
    dict[tuple[str, str], int],
]:
    variables_by_year: dict[str, set[str]] = defaultdict(set)
    for task in tasks:
        variables_by_year[task.year].add(task.variable_id)
    responses: dict[tuple[str, str], dict[str, str]] = {
        (year, variable): {}
        for year, variables in variables_by_year.items()
        for variable in variables
    }
    source_rows_by_year: dict[str, int] = defaultdict(int)
    nonmissing_by_year_variable: dict[tuple[str, str], int] = defaultdict(int)
    seen_case_ids_by_year: dict[str, set[str]] = defaultdict(set)

    reader = csv.DictReader(handle, delimiter="\t")
    if not reader.fieldnames:
        raise SystemExit("Cumulative CES source has no header.")
    required = {"year", "case_id"} | {
        task.variable_id for task in tasks
    }
    missing = sorted(required - set(reader.fieldnames))
    if missing:
        raise SystemExit(f"Cumulative CES source lacks required columns: {missing}.")
    for row in reader:
        year = normalize_integer(row.get("year", ""))
        if year not in variables_by_year:
            continue
        source_rows_by_year[year] += 1
        case_id = normalize_case_id(row.get("case_id", ""))
        if not case_id:
            raise SystemExit(f"Cumulative CES {year} row lacks case_id.")
        if case_id in seen_case_ids_by_year[year]:
            raise SystemExit(f"Cumulative CES {year} has duplicate case_id {case_id}.")
        seen_case_ids_by_year[year].add(case_id)
        for variable_id in variables_by_year[year]:
            response = normalize_response_code(row.get(variable_id, ""))
            responses[(year, variable_id)][case_id] = response
            if response:
                nonmissing_by_year_variable[(year, variable_id)] += 1
    return responses, dict(source_rows_by_year), dict(nonmissing_by_year_variable)


def validate_cumulative_counts(
    tasks: list[EstimateTask],
    source_rows_by_year: dict[str, int],
    nonmissing_by_year_variable: dict[tuple[str, str], int],
    expected_rows: dict[tuple[str, str], dict[str, str]],
) -> None:
    for task in tasks:
        key = (task.year, task.variable_id)
        expected = expected_rows.get(key)
        if expected is None:
            raise SystemExit(f"{RESPONSE_DISTRIBUTIONS}: missing expected row for {key}.")
        actual_total = source_rows_by_year.get(task.year, 0)
        actual_nonmissing = nonmissing_by_year_variable.get(key, 0)
        if actual_total != int(expected["total_source_rows"]):
            raise SystemExit(
                f"Cumulative CES {task.year} row count changed: "
                f"expected {expected['total_source_rows']}, got {actual_total}."
            )
        if actual_nonmissing != int(expected["response_nonmissing_count"]):
            raise SystemExit(
                f"Cumulative CES {key} nonmissing count changed: "
                f"expected {expected['response_nonmissing_count']}, got {actual_nonmissing}."
            )


def aggregate_annual_source(
    handle: TextIO,
    source: AnnualSource,
    tasks: list[EstimateTask],
    responses: dict[tuple[str, str], dict[str, str]],
    item_sources: dict[EstimateTask, AnnualItemSource],
) -> tuple[
    int,
    dict[EstimateTask, EstimateAccumulator],
    dict[EstimateTask, int],
]:
    annual_tasks = [task for task in tasks if task.year == source.year]
    tasks_by_district: dict[tuple[str, str], list[EstimateTask]] = defaultdict(list)
    for task in annual_tasks:
        tasks_by_district[(task.state_fips, task.district_number)].append(task)
    accumulators = {task: EstimateAccumulator() for task in annual_tasks}
    validated_responses = {task: 0 for task in annual_tasks}
    seen_case_ids: set[str] = set()
    annual_source_rows = 0

    reader = csv.DictReader(handle, delimiter="\t")
    if not reader.fieldnames:
        raise SystemExit(f"Annual CCES {source.year} source has no header.")
    required = {
        source.case_id_field,
        source.state_field,
        source.district_field,
    }
    for task in annual_tasks:
        item_source = item_sources[task]
        required.add(item_source.question_field)
        required.add(item_source.weight_field)
    missing = sorted(required - set(reader.fieldnames))
    if missing:
        raise SystemExit(f"Annual CCES {source.year} lacks required columns: {missing}.")
    for row in reader:
        annual_source_rows += 1
        case_id = normalize_case_id(row.get(source.case_id_field, ""))
        if not case_id:
            raise SystemExit(f"Annual CCES {source.year} row lacks {source.case_id_field}.")
        if case_id in seen_case_ids:
            raise SystemExit(f"Annual CCES {source.year} has duplicate case id {case_id}.")
        seen_case_ids.add(case_id)
        for task in annual_tasks:
            response_by_case = responses[(task.year, task.variable_id)]
            cumulative_response = response_by_case.get(case_id, "")
            if not cumulative_response:
                continue
            item_source = item_sources[task]
            annual_response = normalize_response_code(
                row.get(item_source.question_field, "")
            )
            if annual_response != cumulative_response:
                raise SystemExit(
                    f"Annual CCES {source.year} {item_source.question_field} response "
                    f"does not match cumulative {task.variable_id} for case {case_id}."
                )
            validated_responses[task] += 1
        district_key = (
            normalize_integer(row.get(source.state_field, "")),
            normalize_integer(row.get(source.district_field, "")),
        )
        matching_tasks = tasks_by_district.get(district_key, [])
        if not matching_tasks:
            continue
        for task in matching_tasks:
            item_source = item_sources[task]
            weight = parse_positive_weight(row.get(item_source.weight_field, ""))
            accumulator = accumulators[task]
            accumulator.district_source_rows += 1
            response_by_case = responses[(task.year, task.variable_id)]
            if case_id not in response_by_case:
                continue
            accumulator.joined_rows += 1
            response = response_by_case[case_id]
            if not response:
                continue
            accumulator.response_respondents += 1
            if response in task.support_codes:
                accumulator.support_respondents += 1
                support = 1.0
            elif response in task.oppose_codes:
                accumulator.oppose_respondents += 1
                support = 0.0
            else:
                accumulator.other_response_respondents += 1
                continue
            if weight is None:
                accumulator.invalid_weight_respondents += 1
                continue
            accumulator.weighted_support += weight * support
            accumulator.sum_weights += weight
            accumulator.sum_squared_weights += weight * weight
    for task, validated_count in validated_responses.items():
        expected_count = sum(
            bool(response)
            for response in responses[(task.year, task.variable_id)].values()
        )
        if validated_count != expected_count:
            raise SystemExit(
                f"Annual CCES {source.year} cross-source response coverage for "
                f"{task.variable_id} changed: expected {expected_count}, "
                f"validated {validated_count}."
            )
    return annual_source_rows, accumulators, validated_responses


def decimal(value: float, places: int = 6) -> str:
    return f"{value:.{places}f}"


def build_output_row(
    task: EstimateTask,
    source: AnnualSource,
    item_source: AnnualItemSource,
    accumulator: EstimateAccumulator,
    cross_source_validated_responses: int,
    annual_source_rows: int,
    cumulative_source_rows: int,
    cumulative_nonmissing: int,
    minimum_respondents: int,
) -> dict[str, str]:
    binary_respondents = accumulator.support_respondents + accumulator.oppose_respondents
    publish = (
        binary_respondents >= minimum_respondents
        and accumulator.sum_weights > 0.0
        and accumulator.sum_squared_weights > 0.0
    )
    effective_n = (
        accumulator.sum_weights * accumulator.sum_weights
        / accumulator.sum_squared_weights
        if accumulator.sum_squared_weights > 0.0
        else 0.0
    )
    if publish:
        estimate_status = "historical_direct_weighted_district_issue_estimate_available"
        privacy_status = (
            f"aggregate_only_minimum_n_{minimum_respondents}_met_no_case_ids_written"
        )
        published = {
            "published_response_respondents": str(accumulator.response_respondents),
            "published_support_respondents": str(accumulator.support_respondents),
            "published_oppose_respondents": str(accumulator.oppose_respondents),
            "published_other_response_respondents": str(
                accumulator.other_response_respondents
            ),
            "published_invalid_weight_respondents": str(
                accumulator.invalid_weight_respondents
            ),
            "unweighted_support_share": decimal(
                accumulator.support_respondents / binary_respondents
            ),
            "weighted_support_share": decimal(
                accumulator.weighted_support / accumulator.sum_weights
            ),
            "sum_analysis_weights": decimal(accumulator.sum_weights),
            "sum_squared_analysis_weights": decimal(
                accumulator.sum_squared_weights
            ),
            "effective_sample_size": decimal(effective_n),
        }
    else:
        estimate_status = "historical_district_issue_estimate_suppressed_below_threshold"
        privacy_status = (
            f"aggregate_suppressed_below_minimum_n_{minimum_respondents}_no_case_ids_written"
        )
        published = {
            "published_response_respondents": "",
            "published_support_respondents": "",
            "published_oppose_respondents": "",
            "published_other_response_respondents": "",
            "published_invalid_weight_respondents": "",
            "unweighted_support_share": "",
            "weighted_support_share": "",
            "sum_analysis_weights": "",
            "sum_squared_analysis_weights": "",
            "effective_sample_size": "",
        }
    return {
        "bill_id": task.bill_id,
        "public_law_number": task.public_law_number,
        "policy_area": task.policy_area,
        "bill_title": task.bill_title,
        "sponsor_district_id": task.district_id,
        "sponsor_state_fips": task.state_fips,
        "sponsor_district_number": task.district_number,
        "survey_item_id": task.variable_id,
        "survey_item_label": task.item_label,
        "survey_item_support_codes": "; ".join(sorted(task.support_codes)),
        "survey_item_oppose_codes": "; ".join(sorted(task.oppose_codes)),
        "alignment_direction": task.alignment_direction,
        "alignment_strength": task.alignment_strength,
        "survey_year": task.year,
        "annual_congress": source.congress,
        "estimate_method": "annual_cces_direct_weighted_descriptive_estimate",
        "estimate_scope": "sponsor_district_historical_related_issue_context",
        "temporal_alignment_status": "historical_pre_enactment_issue_context",
        "question_alignment_status": "related_issue_item_not_exact_bill_wording",
        "geography_alignment_status": (
            "same_state_district_number_post_2010_apportionment_cycle_"
            "without_boundary_file_crosswalk"
        ),
        "minimum_publishable_respondents": str(minimum_respondents),
        "estimate_status": estimate_status,
        "privacy_status": privacy_status,
        "cumulative_source_rows_in_year": str(cumulative_source_rows),
        "cumulative_item_nonmissing_responses_in_year": str(cumulative_nonmissing),
        "annual_source_rows": str(annual_source_rows),
        "annual_district_source_rows": str(accumulator.district_source_rows),
        "annual_district_joined_rows": str(accumulator.joined_rows),
        **published,
        "uncertainty_status": "descriptive_point_estimate_only_no_design_based_standard_error",
        "cumulative_dataset_doi": CUMULATIVE_DATASET_DOI,
        "cumulative_dataset_version": CUMULATIVE_DATASET_VERSION,
        "cumulative_dataset_release_time": CUMULATIVE_DATASET_RELEASE_TIME,
        "cumulative_dataset_license": CUMULATIVE_DATASET_LICENSE,
        "cumulative_data_file_id": CUMULATIVE_FILE_ID,
        "cumulative_data_file_label": CUMULATIVE_FILE_LABEL,
        "cumulative_data_file_md5": CUMULATIVE_FILE_MD5,
        "cumulative_access_file_size_bytes": str(
            CUMULATIVE_ACCESS_FILE_SIZE_BYTES
        ),
        "cumulative_access_file_sha256": CUMULATIVE_ACCESS_FILE_SHA256,
        "annual_dataset_doi": source.dataset_doi,
        "annual_dataset_version": source.dataset_version,
        "annual_dataset_release_time": source.dataset_release_time,
        "annual_dataset_license": source.dataset_license,
        "annual_data_file_id": source.file_id,
        "annual_data_file_label": source.file_label,
        "annual_data_file_md5": source.file_md5,
        "annual_access_file_size_bytes": str(source.access_file_size_bytes),
        "annual_access_file_sha256": source.access_file_sha256,
        "annual_case_id_field": source.case_id_field,
        "annual_question_field": item_source.question_field,
        "annual_question_wave": item_source.question_wave,
        "annual_question_guide_file_id": item_source.guide_file_id,
        "annual_question_guide_file_label": item_source.guide_file_label,
        "annual_question_guide_file_md5": item_source.guide_file_md5,
        "annual_question_guide_printed_page": item_source.guide_printed_page,
        "annual_weight_field": item_source.weight_field,
        "annual_weight_selection_status": item_source.weight_selection_status,
        "cross_source_validated_response_respondents": str(
            cross_source_validated_responses
        ),
        "cross_source_response_validation_status": (
            "all_nonmissing_cumulative_responses_match_annual_question"
        ),
        "annual_state_field": source.state_field,
        "annual_district_field": source.district_field,
        "source_urls": "; ".join([
            CUMULATIVE_SOURCE_URL,
            CUMULATIVE_DATA_URL,
            source.source_url,
            source.data_url,
            item_source.guide_data_url,
            WEIGHT_GUIDANCE_URL,
        ]),
        "evidence_layers": EVIDENCE_LAYERS,
        "missing_links": MISSING_LINKS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], minimum_respondents: int) -> None:
    available = [row for row in rows if row["weighted_support_share"]]
    suppressed = [row for row in rows if not row["weighted_support_share"]]
    bills = sorted({row["bill_id"] for row in rows})
    variables = sorted({row["survey_item_id"] for row in rows})
    districts = sorted({row["sponsor_district_id"] for row in rows})
    years = sorted({row["survey_year"] for row in rows})
    validated_responses = sum(
        int(row["cross_source_validated_response_respondents"])
        for row in rows
    )
    weight_fields = sorted({row["annual_weight_field"] for row in rows})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    lines = [
        "# District Public-Opinion Bill Topic Support Metadata",
        "",
        f"Generated: {now}.",
        f"- Source-reviewed bills represented: {len(bills)} ({'; '.join(bills)}).",
        f"- Historical issue items represented: {len(variables)} ({'; '.join(variables)}).",
        f"- Sponsor districts represented: {len(districts)} ({'; '.join(districts)}).",
        f"- Annual source years represented: {len(years)} ({'; '.join(years)}).",
        f"- Aggregate estimate rows available: {len(available)}.",
        f"- Aggregate estimate rows suppressed: {len(suppressed)}.",
        f"- Minimum publishable support-plus-oppose respondents: {minimum_respondents}.",
        "- Respondent-level records or case identifiers written: 0.",
        "- Annual question wave for every represented estimate: pre-election.",
        f"- Nonmissing cumulative responses matched to the original annual questions: {validated_responses}.",
        f"- Validated-voter pre-election weight fields used: {'; '.join(weight_fields)}.",
        "- Live refreshes verify the Dataverse catalog MD5 values and independently validate the byte count and SHA-256 of each tabular stream parsed.",
        "- Uncertainty intervals reported: 0; annual source replicate weights and design-based variance are not modeled here.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Pinned official sources:",
        f"- Cumulative CES Policy Preferences: {CUMULATIVE_SOURCE_URL}",
    ]
    for source in ANNUAL_SOURCES.values():
        if source.year in years:
            lines.append(f"- {source.year} CCES Common Content: {source.source_url}")
    for item_source in ANNUAL_ITEM_SOURCES.values():
        if item_source.year in years:
            lines.append(
                f"- {item_source.year} CCES guide: {item_source.guide_data_url}"
            )
    lines.append(f"- CES weight guidance: {WEIGHT_GUIDANCE_URL}")
    write_reproducible_metadata(OUT_METADATA, "\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="redownload pinned CES sources even if the existing aggregate cache matches",
    )
    parser.add_argument(
        "--minimum-respondents",
        type=int,
        default=DEFAULT_MINIMUM_RESPONDENTS,
        help="Minimum support-plus-oppose respondents required to publish an estimate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.minimum_respondents <= 0:
        raise SystemExit("--minimum-respondents must be positive.")
    alignment_rows = read_csv(ALIGNMENTS)
    codebook_rows = read_csv(CODEBOOK)
    expected_distributions = response_distribution_index(
        read_csv(RESPONSE_DISTRIBUTIONS)
    )
    tasks = build_tasks(alignment_rows, codebook_rows)
    item_sources = {task: item_source_for(task) for task in tasks}

    if not args.refresh and existing_output_matches(tasks, args.minimum_respondents):
        output_rows = read_csv(OUT_CSV)
        write_metadata(output_rows, args.minimum_respondents)
        print(f"Reused {OUT_CSV}")
        print(f"Wrote {OUT_METADATA}")
        return 0

    validate_file_metadata(
        CUMULATIVE_FILE_ID, CUMULATIVE_FILE_LABEL, CUMULATIVE_FILE_MD5
    )
    for year in sorted({task.year for task in tasks}):
        source = ANNUAL_SOURCES[year]
        validate_file_metadata(source.file_id, source.file_label, source.file_md5)
    validated_guides: set[str] = set()
    for item_source in item_sources.values():
        if item_source.guide_file_id in validated_guides:
            continue
        validate_file_metadata(
            item_source.guide_file_id,
            item_source.guide_file_label,
            item_source.guide_file_md5,
        )
        validated_guides.add(item_source.guide_file_id)

    with open_data_stream(
        CUMULATIVE_DATA_URL,
        CUMULATIVE_ACCESS_FILE_SIZE_BYTES,
        CUMULATIVE_ACCESS_FILE_SHA256,
        CUMULATIVE_FILE_LABEL,
    ) as handle:
        responses, cumulative_rows, cumulative_nonmissing = read_cumulative_responses(
            handle, tasks
        )
    validate_cumulative_counts(
        tasks,
        cumulative_rows,
        cumulative_nonmissing,
        expected_distributions,
    )

    output_rows: list[dict[str, str]] = []
    for year in sorted({task.year for task in tasks}):
        source = ANNUAL_SOURCES[year]
        with open_data_stream(
            source.data_url,
            source.access_file_size_bytes,
            source.access_file_sha256,
            source.file_label,
        ) as handle:
            annual_rows, accumulators, validated_responses = aggregate_annual_source(
                handle, source, tasks, responses, item_sources
            )
        for task in sorted(
            accumulators,
            key=lambda item: (item.bill_id, item.district_id, item.variable_id),
        ):
            output_rows.append(build_output_row(
                task=task,
                source=source,
                item_source=item_sources[task],
                accumulator=accumulators[task],
                cross_source_validated_responses=validated_responses[task],
                annual_source_rows=annual_rows,
                cumulative_source_rows=cumulative_rows[year],
                cumulative_nonmissing=cumulative_nonmissing[(year, task.variable_id)],
                minimum_respondents=args.minimum_respondents,
            ))
    output_rows.sort(
        key=lambda row: (
            row["bill_id"],
            row["sponsor_district_id"],
            row["survey_item_id"],
            row["survey_year"],
        )
    )
    write_csv(output_rows)
    write_metadata(output_rows, args.minimum_respondents)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
