#!/usr/bin/env python3
"""Build CES policy-preference guide/codebook response-direction rows."""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata


CANDIDATES = Path("data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv")
RAW_DISTRIBUTIONS = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
OUT_CSV = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv"
)
OUT_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.metadata.md"
)

CLAIM_BOUNDARY = (
    "Official CES policy-preference guide/codebook response-direction review only; "
    "rows map official guide response labels or continuous-scale endpoints to "
    "observed source response codes for candidate policy-preference variables. "
    "They identify item-wording support/oppose labels, ordered/categorical labels, "
    "or continuous endpoint labels only. They are not bill-text-aligned support "
    "directions, not bill-topic public support estimates, not district support "
    "estimates, not MRP or small-area estimates, not bill-text-specific "
    "affected-population definitions, not affected-group support or harm, not "
    "public-benefit evidence, and not model validation."
)

MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; bill_text_direction_alignment_review; "
    "bill_topic_public_opinion; respondent_geography_merge; MRP_or_small_area_estimate; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "official_dataverse_policy_preferences_metadata; "
    "official_policy_preferences_tabular_header; "
    "official_policy_preferences_raw_response_code_distribution; "
    "official_policy_preferences_guide_response_codebook_direction"
)

FIELDNAMES = [
    "source_family",
    "source_name",
    "dataset_doi",
    "dataset_version",
    "dataset_release_time",
    "dataset_license",
    "guide_file_id",
    "guide_file_label",
    "guide_file_md5",
    "variable_id",
    "issue_area",
    "short_label",
    "guide_section_heading",
    "guide_item_description",
    "guide_years_in_data",
    "guide_year_count",
    "observed_response_code_count",
    "observed_response_codes",
    "guide_response_label_count",
    "guide_response_labels",
    "codebook_code_label_map",
    "code_label_map_status",
    "unmapped_observed_codes",
    "codebook_direction_type",
    "item_support_codes",
    "item_oppose_codes",
    "ordered_low_code",
    "ordered_low_label",
    "ordered_high_code",
    "ordered_high_label",
    "continuous_low_code",
    "continuous_low_label",
    "continuous_high_code",
    "continuous_high_label",
    "direction_review_status",
    "exact_bill_topic_support_status",
    "bill_text_direction_alignment_status",
    "district_estimation_status",
    "source_url",
    "guide_download_url",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CONTINUOUS_SCALE_TYPES = {
    "incometax_vs_salestax",
    "spending_vs_tax",
}

CATEGORICAL_BUDGET_CHOICES = {
    "spending_cuts_least",
    "spending_cuts_most",
}

ORDERED_SPENDING_SCALES = {
    "spending_education",
    "spending_healthcare",
    "spending_infrastructure",
    "spending_police",
    "spending_welfare",
}

ORDERED_SUPPORT_SCALES = {
    "affirmativeaction",
    "affirmativeaction_scale",
    "gaymarriage_scale",
}

ORDERED_ACCESS_SCALES = {
    "abortion_scale",
}

ORDERED_POLICY_SCALES = {
    "enviro_scale",
    "enviro_vs_jobs",
    "guns_scale",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty")
    return rows


def response_code_sort_key(value: str) -> tuple[int, float | str]:
    try:
        return (0, float(value))
    except ValueError:
        return (1, value)


def split_values(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def fetch_guide_pdf(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "congress-institutional-simulator/validation"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        destination.write_bytes(response.read())


def extract_guide_text(url: str) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise SystemExit("pdftotext is required to parse the official CES policy-preferences guide.")
    with tempfile.TemporaryDirectory(prefix="congress-ces-guide-") as tmp:
        pdf_path = Path(tmp) / "guide_cumulative_ces_policy_preferences.pdf"
        text_path = Path(tmp) / "guide.txt"
        fetch_guide_pdf(url, pdf_path)
        subprocess.run(
            [pdftotext, "-layout", str(pdf_path), str(text_path)],
            check=True,
        )
        return text_path.read_text(errors="replace")


def clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\f", " ")).strip()


def extract_sections(text: str) -> dict[str, tuple[str, str]]:
    starts = list(re.finditer(r"(?m)^[\f ]*(5\.\d+\.\d+)\s+([a-z0-9_]+)\s*$", text))
    if not starts:
        raise SystemExit("No CES policy-preference guide sections found.")
    sections: dict[str, tuple[str, str]] = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        section_id, variable_id = match.group(1), match.group(2)
        sections[variable_id] = (f"{section_id} {variable_id}", text[match.end():end])
    return sections


def guide_description(section: str) -> str:
    before_years = section.split("Years in data:", 1)[0]
    lines = [
        clean_line(line)
        for line in before_years.splitlines()
        if clean_line(line) and not re.fullmatch(r"\d+", clean_line(line))
    ]
    return " ".join(lines)


def guide_years(section: str) -> list[str]:
    if "Years in data:" not in section:
        return []
    after = section.split("Years in data:", 1)[1]
    cutoffs = [
        position
        for marker in ("Table", "Density plots", "Year-specific variable names")
        for position in [after.find(marker)]
        if position >= 0
    ]
    year_text = after[: min(cutoffs)] if cutoffs else after
    return re.findall(r"\b(20\d{2})\b", year_text)


def frequency_block(section: str) -> str:
    if "Frequency table" not in section:
        return ""
    after = section.split("Frequency table", 1)[1]
    return after.split("Year-specific variable names and wording", 1)[0]


def continuous_endpoint_labels(description: str) -> list[str]:
    match = re.search(r"from\s+0\s*\((.*?)\)\s+to\s+100\s*\((.*?)\)", description, re.I)
    if not match:
        return []
    return [f"0={match.group(1)}", f"100={match.group(2)}"]


def extract_response_labels(section: str, description: str) -> list[str]:
    if "Density plots" in section and "Frequency table" not in section:
        return continuous_endpoint_labels(description)
    block = frequency_block(section)
    result: list[str] = []
    header_labels: list[str] = []
    for raw_line in block.splitlines():
        line_for_split = raw_line.replace("\f", " ").strip()
        line = clean_line(line_for_split)
        if not line:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if "Frequency table" in line or "continued" in line or line.startswith("Table "):
            continue
        if line.startswith("Response"):
            continue
        if line.startswith("Year "):
            parts = [
                clean_line(part)
                for part in re.split(r"\s{2,}", line_for_split)
                if clean_line(part)
            ]
            if len(parts) > 1:
                header_labels = parts[1:]
            continue
        if re.match(r"^20\d{2}\b", line):
            continue
        label_match = re.match(
            r"^(.*?)(?:\s{2,})(?:\d{1,3}(?:,\d{3})*|0)(?:\s|$)",
            line_for_split,
        )
        if label_match:
            label = clean_line(label_match.group(1))
            if label and not re.fullmatch(r"20\d{2}", label):
                result.append(label)
    if result:
        return list(dict.fromkeys(result))
    return list(dict.fromkeys(header_labels))


def direction_type(variable_id: str, labels: list[str]) -> str:
    normalized_labels = [label.casefold() for label in labels]
    if variable_id in CONTINUOUS_SCALE_TYPES:
        return "continuous_policy_tradeoff_scale"
    if variable_id in CATEGORICAL_BUDGET_CHOICES:
        return "categorical_budget_choice"
    if variable_id in ORDERED_SPENDING_SCALES:
        return "ordered_spending_increase_decrease"
    if variable_id in ORDERED_SUPPORT_SCALES:
        return "ordered_support_opposition_scale"
    if variable_id in ORDERED_ACCESS_SCALES:
        return "ordered_access_scale"
    if variable_id in ORDERED_POLICY_SCALES:
        return "ordered_policy_scale"
    if normalized_labels == ["support", "oppose"]:
        return "binary_item_support_oppose"
    return "unclassified"


def is_continuous_direction(direction: str) -> bool:
    return direction == "continuous_policy_tradeoff_scale"


def scale_range_codes(observed_codes: list[str]) -> tuple[list[str], list[str]]:
    in_range: list[str] = []
    out_of_range: list[str] = []
    for code in observed_codes:
        try:
            value = float(code)
        except ValueError:
            out_of_range.append(code)
            continue
        if 0 <= value <= 100:
            in_range.append(code)
        else:
            out_of_range.append(code)
    return in_range, out_of_range


def code_label_fields(
    variable_id: str,
    observed_codes: list[str],
    labels: list[str],
    direction: str,
) -> dict[str, str]:
    if is_continuous_direction(direction):
        endpoints = continuous_endpoint_labels("; ".join(labels))
        if not endpoints:
            endpoints = labels
        endpoint_map: list[dict[str, str]] = []
        low_label = ""
        high_label = ""
        for label in endpoints:
            if label.startswith("0="):
                low_label = label.split("=", 1)[1]
                endpoint_map.append({"code": "0.0", "label": low_label})
            elif label.startswith("100="):
                high_label = label.split("=", 1)[1]
                endpoint_map.append({"code": "100.0", "label": high_label})
        _in_range, out_of_range = scale_range_codes(observed_codes)
        return {
            "codebook_code_label_map": json.dumps(endpoint_map, ensure_ascii=True, separators=(",", ":")),
            "code_label_map_status": (
                "continuous_scale_endpoint_labels_only_special_codes_unresolved"
                if out_of_range
                else "continuous_scale_endpoint_labels_only"
            ),
            "unmapped_observed_codes": "; ".join(out_of_range),
            "item_support_codes": "",
            "item_oppose_codes": "",
            "ordered_low_code": "",
            "ordered_low_label": "",
            "ordered_high_code": "",
            "ordered_high_label": "",
            "continuous_low_code": "0.0",
            "continuous_low_label": low_label,
            "continuous_high_code": "100.0",
            "continuous_high_label": high_label,
        }

    code_label_map = [
        {"code": code, "label": label}
        for code, label in zip(observed_codes, labels, strict=False)
    ]
    unmapped_codes = observed_codes[len(labels):] if len(observed_codes) > len(labels) else []
    support_codes = [
        item["code"]
        for item in code_label_map
        if item["label"].casefold() == "support"
    ]
    oppose_codes = [
        item["code"]
        for item in code_label_map
        if item["label"].casefold() == "oppose"
    ]
    ordered_low_code = observed_codes[0] if observed_codes else ""
    ordered_high_code = observed_codes[-1] if observed_codes else ""
    ordered_low_label = labels[0] if labels else ""
    ordered_high_label = labels[-1] if labels else ""
    return {
        "codebook_code_label_map": json.dumps(code_label_map, ensure_ascii=True, separators=(",", ":")),
        "code_label_map_status": (
            "all_observed_discrete_codes_labelled_from_guide"
            if not unmapped_codes and len(labels) == len(observed_codes)
            else "observed_discrete_codes_partially_labelled_from_guide"
        ),
        "unmapped_observed_codes": "; ".join(unmapped_codes),
        "item_support_codes": "; ".join(support_codes),
        "item_oppose_codes": "; ".join(oppose_codes),
        "ordered_low_code": ordered_low_code if direction.startswith("ordered_") else "",
        "ordered_low_label": ordered_low_label if direction.startswith("ordered_") else "",
        "ordered_high_code": ordered_high_code if direction.startswith("ordered_") else "",
        "ordered_high_label": ordered_high_label if direction.startswith("ordered_") else "",
        "continuous_low_code": "",
        "continuous_low_label": "",
        "continuous_high_code": "",
        "continuous_high_label": "",
    }


def direction_status(direction: str, map_status: str) -> str:
    if direction == "binary_item_support_oppose":
        return "guide_codebook_binary_item_direction_reviewed_no_bill_mapping"
    if direction.startswith("ordered_"):
        return "guide_codebook_ordered_item_scale_reviewed_no_bill_mapping"
    if direction == "categorical_budget_choice":
        return "guide_codebook_categorical_labels_reviewed_no_binary_direction"
    if direction == "continuous_policy_tradeoff_scale":
        return "guide_codebook_continuous_scale_endpoints_reviewed_no_bill_mapping"
    if "partially" in map_status:
        return "guide_codebook_labels_partially_reviewed_no_bill_mapping"
    return "guide_codebook_labels_reviewed_no_bill_mapping"


def build_rows(
    candidate_rows: list[dict[str, str]],
    distribution_rows: list[dict[str, str]],
    guide_text: str,
) -> list[dict[str, str]]:
    overall_distributions = {
        row["variable_id"]: row
        for row in distribution_rows
        if row.get("year") == "all"
    }
    sections = extract_sections(guide_text)
    missing_sections = sorted({row["variable_id"] for row in candidate_rows} - set(sections))
    if missing_sections:
        raise SystemExit(f"Official guide text missing policy-item sections: {missing_sections}")
    rows: list[dict[str, str]] = []
    for candidate in sorted(candidate_rows, key=lambda row: row["variable_id"]):
        variable_id = candidate["variable_id"]
        section_heading, section = sections[variable_id]
        distribution = overall_distributions.get(variable_id)
        if distribution is None:
            raise SystemExit(f"{RAW_DISTRIBUTIONS} missing overall distribution for {variable_id}")
        observed_codes = split_values(distribution.get("observed_response_codes", ""))
        observed_codes = sorted(observed_codes, key=response_code_sort_key)
        description = guide_description(section)
        years = sorted(set(guide_years(section)), key=response_code_sort_key)
        labels = extract_response_labels(section, description)
        direction = direction_type(variable_id, labels)
        label_fields = code_label_fields(variable_id, observed_codes, labels, direction)
        rows.append({
            "source_family": candidate["source_family"],
            "source_name": candidate["source_name"],
            "dataset_doi": candidate["dataset_doi"],
            "dataset_version": candidate["dataset_version"],
            "dataset_release_time": candidate["dataset_release_time"],
            "dataset_license": candidate["dataset_license"],
            "guide_file_id": candidate["guide_file_id"],
            "guide_file_label": candidate["guide_file_label"],
            "guide_file_md5": candidate["guide_file_md5"],
            "variable_id": variable_id,
            "issue_area": candidate["issue_area"],
            "short_label": candidate["short_label"],
            "guide_section_heading": section_heading,
            "guide_item_description": description,
            "guide_years_in_data": "; ".join(years),
            "guide_year_count": str(len(years)),
            "observed_response_code_count": str(len(observed_codes)),
            "observed_response_codes": "; ".join(observed_codes),
            "guide_response_label_count": str(len(labels)),
            "guide_response_labels": "; ".join(labels),
            **label_fields,
            "codebook_direction_type": direction,
            "direction_review_status": direction_status(direction, label_fields["code_label_map_status"]),
            "exact_bill_topic_support_status": "no_exact_bill_topic_support_estimate",
            "bill_text_direction_alignment_status": "no_bill_text_direction_alignment_review",
            "district_estimation_status": "no_mrp_or_small_area_estimate",
            "source_url": candidate["source_url"],
            "guide_download_url": candidate["guide_download_url"],
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


def write_metadata(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit("No CES policy-preferences codebook-direction rows built.")
    direction_counts = Counter(row["codebook_direction_type"] for row in rows)
    status_counts = Counter(row["direction_review_status"] for row in rows)
    rows_with_labels = [
        row for row in rows
        if row["guide_response_label_count"] != "0"
    ]
    rows_with_special_codes = [
        row for row in rows
        if row["unmapped_observed_codes"]
    ]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    first = rows[0]
    lines = [
        "# District Public-Opinion CES Policy Item Codebook Direction Metadata",
        "",
        f"Generated: {now}.",
        f"- Source family: {first['source_family']}.",
        f"- Source name: {first['source_name']}.",
        f"- Dataset DOI: {first['dataset_doi']}.",
        f"- Dataset version: {first['dataset_version']}.",
        f"- Dataset release time: {first['dataset_release_time']}.",
        f"- Dataset license: {first['dataset_license']}.",
        f"- Guide file: {first['guide_file_label']} (Dataverse file id {first['guide_file_id']}, MD5 {first['guide_file_md5']}).",
        f"- Official policy variables reviewed: {len(rows)}.",
        f"- Variables with guide response labels or endpoint labels: {len(rows_with_labels)}.",
        f"- Variables with unmapped observed special/raw codes after guide endpoint review: {len(rows_with_special_codes)}.",
        "",
        "Direction types:",
    ]
    for status, count in sorted(direction_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Direction review statuses:")
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Rows identify guide codebook labels and endpoint directions for source items only. They do not align those item directions to public-law bill text and do not estimate district support.",
    ])
    write_reproducible_metadata(OUT_METADATA, "\n".join(lines) + "\n")


def main() -> int:
    candidate_rows = read_csv(CANDIDATES)
    distribution_rows = read_csv(RAW_DISTRIBUTIONS)
    guide_url = candidate_rows[0].get("guide_download_url", "").strip()
    if not guide_url:
        raise SystemExit(f"{CANDIDATES} has no guide_download_url")
    guide_text = extract_guide_text(guide_url)
    rows = build_rows(candidate_rows, distribution_rows, guide_text)
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
