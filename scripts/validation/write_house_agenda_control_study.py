#!/usr/bin/env python3
"""Write the locked House agenda-control source and temporal study."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
AGENDA_PANEL = ROOT / "data/validation/raw/house_agenda_control.csv"
AGENDA_METADATA = ROOT / "data/validation/raw/house_agenda_control.metadata.md"
GRANT_PANEL = ROOT / "data/validation/raw/house_special_rule_grants.csv"
GRANT_METADATA = ROOT / "data/validation/raw/house_special_rule_grants.metadata.md"
SPECIFICATION = (
    ROOT
    / "papers/empirical-validation/house-agenda-control-panel-specification.md"
)
SCRIPT_PATH = Path(__file__).resolve()

METRICS_OUTPUT = ROOT / "reports/house-agenda-control-metrics.csv"
REPORT_OUTPUT = ROOT / "reports/house-agenda-control-study.md"
METADATA_OUTPUT = ROOT / "reports/house-agenda-control-study-metadata.json"

STUDY_VERSION = "house-agenda-control-source-study-v1"
PANEL_VERSION = "house-agenda-control-v1"
CLAIM_BOUNDARY = (
    "Official-source descriptive House procedure and timing evidence only; not "
    "causal agenda-control, unobserved floor-demand, public-benefit, welfare, "
    "capture, or simulator-validation evidence."
)

EXPECTED_AGENDA_ROWS = {116: 9062, 117: 9709, 118: 10564}
EXPECTED_LITERAL_COUNTS = {
    116: {"open": 0, "modified_open": 0, "structured": 55, "closed": 60},
    117: {"open": 0, "modified_open": 0, "structured": 57, "closed": 87},
    118: {"open": 0, "modified_open": 1, "structured": 83, "closed": 115},
}
EXPECTED_NARRATIVE_COUNTS = {
    116: {"open": 0, "modified_open": 0, "structured": 55, "closed": 60},
    117: {"open": 0, "modified_open": 0, "structured": 59, "closed": 89},
    118: {"open": 0, "modified_open": 1, "structured": 83, "closed": 115},
}

CATEGORIES = ("open", "modified_open", "structured", "closed")
FLOOR_PATHS = (
    "adopted_special_rule",
    "suspension",
    "mixed_special_rule_and_suspension",
    "other_detected_floor_path",
)
DIRECT_RULE_LINK_STATUSES = (
    "no_direct_or_adopted_rule_link",
    "direct_and_adopted_rule_links_match",
    "direct_actions_include_all_adopted_rule_links",
    "adopted_survey_rule_without_direct_action_id",
    "direct_rule_action_without_adopted_table1a_link",
    "direct_and_adopted_rule_links_differ",
)
STAGES = (
    ("introduced", "introduced", "Introduced"),
    ("referred", "referred_to_committee", "Referred"),
    ("committee_advanced", "committee_advanced", "Committee advanced"),
    ("calendar_placed", "calendar_placed", "Calendar placed"),
    ("floor_considered", "floor_considered", "Floor considered"),
    ("passed_house", "passed_house", "Passed House"),
    ("enacted", "enacted", "Enacted"),
)
INTERVALS = (
    (
        "introduction_to_referral",
        "introduction_to_referral_days",
        "Introduction to referral",
    ),
    (
        "referral_to_committee_advance",
        "referral_to_committee_advance_days",
        "Referral to committee advance",
    ),
    (
        "committee_advance_to_floor",
        "committee_advance_to_floor_days",
        "Committee advance to floor",
    ),
    (
        "introduction_to_floor",
        "introduction_to_floor_days",
        "Introduction to floor",
    ),
)


class StudyError(RuntimeError):
    """Raised when a locked study input or invariant fails."""


@dataclass(frozen=True)
class Cohort:
    cohort_id: str
    role: str
    label: str
    congresses: tuple[int, ...]


COHORTS = (
    Cohort("116", "development_component", "116th", (116,)),
    Cohort("117", "development_component", "117th", (117,)),
    Cohort(
        "development_116_117",
        "development",
        "116th-117th development",
        (116, 117),
    ),
    Cohort("118", "primary_temporal_test", "118th test", (118,)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise StudyError(message)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {relative(path)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def metadata_values(path: Path) -> dict[str, str]:
    require(path.exists(), f"Missing required metadata: {relative(path)}")
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            result[key] = value.strip().strip("`")
    return result


def parse_int(value: str, field: str, row_id: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as error:
        raise StudyError(f"{row_id}: invalid integer {field}={value!r}") from error
    require(result >= 0, f"{row_id}: negative integer {field}={value!r}")
    return result


def nearest_rank(values: Iterable[int], proportion: float) -> int | None:
    ordered = sorted(values)
    if not ordered:
        return None
    require(0.0 < proportion <= 1.0, "Nearest-rank proportion must be in (0, 1].")
    index = max(0, min(len(ordered) - 1, math.ceil(proportion * len(ordered)) - 1))
    return ordered[index]


def format_ratio(numerator: int, denominator: int) -> str:
    return f"{numerator / denominator:.12f}" if denominator else ""


def format_percent(numerator: int, denominator: int) -> str:
    return f"{100 * numerator / denominator:.3f}%" if denominator else "NA"


def split_tokens(value: str) -> set[str]:
    return {token for token in value.split(";") if token}


def validate_inputs(
    agenda_rows: Sequence[dict[str, str]],
    grant_rows: Sequence[dict[str, str]],
) -> None:
    agenda_required = {
        "bill_id",
        "congress",
        "introduced",
        "referred_to_committee",
        "committee_advanced",
        "calendar_placed",
        "floor_considered",
        "passed_house",
        "enacted",
        "suspension_path_evidence",
        "other_floor_path_evidence",
        "direct_rule_ids",
        "adopted_rule_count",
        "floor_path",
        "house_floor_amendment_offer_actions",
        "house_floor_amendment_disposition_actions",
        "direct_rule_link_status",
        "agenda_integrity_status",
        "agenda_classification_version",
    }
    grant_required = {
        "grant_id",
        "congress",
        "rule_resolution_id",
        "covered_measure_id",
        "covered_measure_type",
        "amendment_structure",
        "restrictive_structure",
        "rule_passed_house",
        "rule_disposition",
        "covered_measure_in_hr_census",
        "classification_version",
    }
    require(bool(agenda_rows), "Agenda panel is empty.")
    require(bool(grant_rows), "Special-rule grant panel is empty.")
    require(
        agenda_required <= set(agenda_rows[0]),
        f"Agenda panel lacks columns: {sorted(agenda_required - set(agenda_rows[0]))}",
    )
    require(
        grant_required <= set(grant_rows[0]),
        f"Grant panel lacks columns: {sorted(grant_required - set(grant_rows[0]))}",
    )

    agenda_ids = [row["bill_id"] for row in agenda_rows]
    grant_ids = [row["grant_id"] for row in grant_rows]
    require(len(agenda_ids) == len(set(agenda_ids)), "Duplicate agenda bill IDs.")
    require(len(grant_ids) == len(set(grant_ids)), "Duplicate grant IDs.")
    require(len(agenda_rows) == sum(EXPECTED_AGENDA_ROWS.values()), "Agenda row count drifted.")
    require(len(grant_rows) == 458, "Grant row count drifted.")
    agenda_id_set = set(agenda_ids)

    for congress, expected in EXPECTED_AGENDA_ROWS.items():
        actual = sum(row["congress"] == str(congress) for row in agenda_rows)
        require(actual == expected, f"Congress {congress} agenda row count drifted.")
        grants = [row for row in grant_rows if row["congress"] == str(congress)]
        counts = Counter(row["amendment_structure"] for row in grants)
        require(
            {category: counts.get(category, 0) for category in CATEGORIES}
            == EXPECTED_LITERAL_COUNTS[congress],
            f"Congress {congress} literal Table 1a counts drifted.",
        )

    for row in grant_rows:
        grant_id = row["grant_id"]
        require(row["classification_version"] == PANEL_VERSION, f"{grant_id}: version drift.")
        require(row["amendment_structure"] in CATEGORIES, f"{grant_id}: invalid category.")
        require(row["rule_passed_house"] in {"0", "1"}, f"{grant_id}: invalid passage flag.")
        require(row["restrictive_structure"] in {"0", "1"}, f"{grant_id}: invalid restrictive flag.")
        require(
            (row["amendment_structure"] in {"structured", "closed"})
            == (row["restrictive_structure"] == "1"),
            f"{grant_id}: restrictive flag conflicts with category.",
        )
        if row["covered_measure_type"] == "hr":
            require(row["covered_measure_in_hr_census"] == "1", f"{grant_id}: H.R. not linked.")
            require(row["covered_measure_id"] in agenda_id_set, f"{grant_id}: H.R. parent missing.")

    for row in agenda_rows:
        bill_id = row["bill_id"]
        require(row["agenda_classification_version"] == PANEL_VERSION, f"{bill_id}: version drift.")
        require(row["direct_rule_link_status"] in DIRECT_RULE_LINK_STATUSES, f"{bill_id}: bad rule-link status.")
        floor = row["floor_considered"] == "1"
        adopted = parse_int(row["adopted_rule_count"], "adopted_rule_count", bill_id)
        suspension = row["suspension_path_evidence"] == "1"
        other = row["other_floor_path_evidence"] == "1"
        direct_ids = split_tokens(row["direct_rule_ids"])
        expected_path: str
        if not floor:
            expected_path = "not_floor_considered"
        elif adopted and suspension:
            expected_path = "mixed_special_rule_and_suspension"
        elif adopted:
            expected_path = "adopted_special_rule"
        elif suspension:
            expected_path = "suspension"
        elif other or direct_ids:
            expected_path = "other_detected_floor_path"
        else:
            expected_path = "floor_path_not_identified"
        require(row["floor_path"] == expected_path, f"{bill_id}: floor-path precedence conflict.")
        require(
            not (floor and row["floor_path"] == "floor_path_not_identified"),
            f"{bill_id}: floor-considered path remains unidentified.",
        )
        for _, field, _ in INTERVALS:
            if row[field]:
                parse_int(row[field], field, bill_id)
        parse_int(
            row["house_floor_amendment_offer_actions"],
            "house_floor_amendment_offer_actions",
            bill_id,
        )
        parse_int(
            row["house_floor_amendment_disposition_actions"],
            "house_floor_amendment_disposition_actions",
            bill_id,
        )

    agenda_metadata = metadata_values(AGENDA_METADATA)
    grant_metadata = metadata_values(GRANT_METADATA)
    require(
        agenda_metadata.get("agenda_output_sha256") == sha256_file(AGENDA_PANEL),
        "Agenda metadata hash does not match the panel.",
    )
    require(
        agenda_metadata.get("grant_output_sha256") == sha256_file(GRANT_PANEL),
        "Agenda metadata grant hash does not match the panel.",
    )
    require(
        grant_metadata.get("agenda_output_sha256") == sha256_file(AGENDA_PANEL),
        "Grant metadata agenda hash does not match the panel.",
    )
    require(
        grant_metadata.get("grant_output_sha256") == sha256_file(GRANT_PANEL),
        "Grant metadata hash does not match the panel.",
    )


def metric_row(
    cohort: Cohort,
    section: str,
    metric_id: str,
    *,
    category: str = "",
    numerator: int | None = None,
    denominator: int | None = None,
    value: str,
    unit: str,
    definition: str,
) -> dict[str, str]:
    return {
        "cohortId": cohort.cohort_id,
        "cohortRole": cohort.role,
        "congresses": ";".join(str(value) for value in cohort.congresses),
        "section": section,
        "metricId": metric_id,
        "category": category,
        "numerator": "" if numerator is None else str(numerator),
        "denominator": "" if denominator is None else str(denominator),
        "value": value,
        "unit": unit,
        "definition": definition,
    }


def add_count(
    output: list[dict[str, str]],
    cohort: Cohort,
    section: str,
    metric_id: str,
    count: int,
    definition: str,
    *,
    category: str = "",
    unit: str = "rows",
) -> None:
    output.append(
        metric_row(
            cohort,
            section,
            metric_id,
            category=category,
            numerator=count,
            value=str(count),
            unit=unit,
            definition=definition,
        )
    )


def add_rate(
    output: list[dict[str, str]],
    cohort: Cohort,
    section: str,
    metric_id: str,
    numerator: int,
    denominator: int,
    definition: str,
    *,
    category: str = "",
) -> None:
    require(denominator > 0, f"{cohort.cohort_id}/{metric_id}: zero denominator.")
    output.append(
        metric_row(
            cohort,
            section,
            metric_id,
            category=category,
            numerator=numerator,
            denominator=denominator,
            value=format_ratio(numerator, denominator),
            unit="proportion",
            definition=definition,
        )
    )


def category_presence(
    rows: Sequence[dict[str, str]],
    id_field: str,
) -> dict[str, set[str]]:
    result: defaultdict[str, set[str]] = defaultdict(set)
    for row in rows:
        result[row[id_field]].add(row["amendment_structure"])
    return dict(result)


def build_metrics(
    agenda_rows: Sequence[dict[str, str]],
    grant_rows: Sequence[dict[str, str]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for cohort in COHORTS:
        congresses = {str(value) for value in cohort.congresses}
        agenda = [row for row in agenda_rows if row["congress"] in congresses]
        grants = [row for row in grant_rows if row["congress"] in congresses]
        total = len(agenda)
        add_count(output, cohort, "population", "agenda_hr_count", total, "Complete H.R. census rows.", unit="bills")

        stage_counts: dict[str, int] = {}
        for stage_id, field, label in STAGES:
            count = sum(row[field] == "1" for row in agenda)
            stage_counts[stage_id] = count
            add_count(output, cohort, "lifecycle", f"stage_{stage_id}_count", count, f"H.R. measures observed at stage: {label}.", unit="bills")
            add_rate(output, cohort, "lifecycle", f"stage_{stage_id}_rate", count, total, f"{label} count divided by all H.R. rows.")

        referred = [row for row in agenda if row["referred_to_committee"] == "1"]
        advanced = [row for row in agenda if row["committee_advanced"] == "1"]
        referred_advanced = sum(row["committee_advanced"] == "1" for row in referred)
        advanced_floor = sum(row["floor_considered"] == "1" for row in advanced)
        add_rate(
            output,
            cohort,
            "transitions",
            "transition_referred_to_committee_advanced_rate",
            referred_advanced,
            len(referred),
            "Referred H.R. measures also observed committee-advanced, divided by referred H.R. measures.",
        )
        add_rate(
            output,
            cohort,
            "transitions",
            "transition_committee_advanced_to_floor_rate",
            advanced_floor,
            len(advanced),
            "Committee-advanced H.R. measures also observed floor-considered, divided by committee-advanced H.R. measures.",
        )

        floor = [row for row in agenda if row["floor_considered"] == "1"]
        calendar_floor = sum(row["calendar_placed"] == "1" for row in floor)
        add_rate(
            output,
            cohort,
            "floor_routes",
            "calendar_coverage_among_floor_rate",
            calendar_floor,
            len(floor),
            "Floor-considered H.R. measures with a direct House, Union, or Private Calendar placement, divided by floor-considered H.R. measures.",
        )
        for path in FLOOR_PATHS:
            path_rows = [row for row in floor if row["floor_path"] == path]
            add_count(output, cohort, "floor_routes", "floor_path_count", len(path_rows), "Floor-considered H.R. measures in the mutually exclusive source path.", category=path, unit="bills")
            add_rate(output, cohort, "floor_routes", "floor_path_share", len(path_rows), len(floor), "Path count divided by floor-considered H.R. measures.", category=path)

            offer_bills = sum(
                parse_int(row["house_floor_amendment_offer_actions"], "offer", row["bill_id"]) > 0
                for row in path_rows
            )
            disposition_bills = sum(
                parse_int(row["house_floor_amendment_disposition_actions"], "disposition", row["bill_id"]) > 0
                for row in path_rows
            )
            offer_actions = sum(
                parse_int(row["house_floor_amendment_offer_actions"], "offer", row["bill_id"])
                for row in path_rows
            )
            disposition_actions = sum(
                parse_int(row["house_floor_amendment_disposition_actions"], "disposition", row["bill_id"])
                for row in path_rows
            )
            add_count(output, cohort, "amendment_actions", "amendment_offer_evidence_bill_count", offer_bills, "Bills with at least one matched direct House floor amendment-offer action.", category=path, unit="bills")
            add_rate(output, cohort, "amendment_actions", "amendment_offer_evidence_bill_rate", offer_bills, len(path_rows), "Bills with matched amendment-offer actions divided by bills in the path.", category=path)
            add_count(output, cohort, "amendment_actions", "amendment_disposition_evidence_bill_count", disposition_bills, "Bills with at least one matched direct House floor amendment-disposition action.", category=path, unit="bills")
            add_rate(output, cohort, "amendment_actions", "amendment_disposition_evidence_bill_rate", disposition_bills, len(path_rows), "Bills with matched amendment-disposition actions divided by bills in the path.", category=path)
            add_count(output, cohort, "amendment_actions", "amendment_offer_action_count", offer_actions, "Matched direct House floor amendment-offer actions.", category=path, unit="actions")
            add_count(output, cohort, "amendment_actions", "amendment_disposition_action_count", disposition_actions, "Matched direct House floor amendment-disposition actions.", category=path, unit="actions")

        for interval_id, field, label in INTERVALS:
            values = [parse_int(row[field], field, row["bill_id"]) for row in agenda if row[field]]
            p50 = nearest_rank(values, 0.50)
            p90 = nearest_rank(values, 0.90)
            add_count(output, cohort, "timing", "interval_observed_count", len(values), f"Nonmissing, nonnegative {label.lower()} intervals.", category=interval_id, unit="intervals")
            output.append(metric_row(cohort, "timing", "interval_p50_days", category=interval_id, numerator=len(values), value="" if p50 is None else str(p50), unit="days", definition=f"Nearest-rank 50th percentile for {label.lower()} among observed intervals."))
            output.append(metric_row(cohort, "timing", "interval_p90_days", category=interval_id, numerator=len(values), value="" if p90 is None else str(p90), unit="days", definition=f"Nearest-rank 90th percentile for {label.lower()} among observed intervals."))

        adopted = [row for row in grants if row["rule_passed_house"] == "1"]
        all_resolutions = category_presence(grants, "rule_resolution_id")
        adopted_resolutions = category_presence(adopted, "rule_resolution_id")
        all_hr = category_presence(
            [row for row in grants if row["covered_measure_type"] == "hr"],
            "covered_measure_id",
        )
        adopted_hr = category_presence(
            [row for row in adopted if row["covered_measure_type"] == "hr"],
            "covered_measure_id",
        )
        add_count(output, cohort, "special_rules", "survey_grant_count", len(grants), "Literal Table 1a rule-to-measure rows.", unit="grants")
        add_count(output, cohort, "special_rules", "adopted_survey_grant_count", len(adopted), "Literal Table 1a grant rows whose H. Res. passed the House.", unit="grants")
        add_count(output, cohort, "special_rules", "survey_unique_resolution_count", len(all_resolutions), "Unique H. Res. identifiers in literal Table 1a.", unit="resolutions")
        add_count(output, cohort, "special_rules", "adopted_unique_resolution_count", len(adopted_resolutions), "Unique Table 1a H. Res. identifiers that passed the House.", unit="resolutions")
        add_count(output, cohort, "special_rules", "survey_unique_hr_measure_count", len(all_hr), "Unique H.R. measures in literal Table 1a.", unit="bills")
        add_count(output, cohort, "special_rules", "adopted_unique_hr_measure_count", len(adopted_hr), "Unique H.R. measures linked to an adopted Table 1a rule.", unit="bills")
        for category in CATEGORIES:
            add_count(output, cohort, "special_rules", "survey_grant_category_count", sum(row["amendment_structure"] == category for row in grants), "Literal Table 1a grant rows in the source category.", category=category, unit="grants")
            add_count(output, cohort, "special_rules", "adopted_grant_category_count", sum(row["amendment_structure"] == category for row in adopted), "Adopted literal Table 1a grant rows in the source category.", category=category, unit="grants")
            add_count(output, cohort, "special_rules", "survey_unique_resolution_category_presence_count", sum(category in categories for categories in all_resolutions.values()), "Unique Table 1a resolutions with at least one row in the category; mixed resolutions contribute to each present category.", category=category, unit="resolutions")
            add_count(output, cohort, "special_rules", "adopted_unique_resolution_category_presence_count", sum(category in categories for categories in adopted_resolutions.values()), "Unique adopted Table 1a resolutions with at least one row in the category; mixed resolutions contribute to each present category.", category=category, unit="resolutions")
            add_count(output, cohort, "special_rules", "survey_unique_hr_measure_category_presence_count", sum(category in categories for categories in all_hr.values()), "Unique Table 1a H.R. measures with at least one row in the category.", category=category, unit="bills")
            add_count(output, cohort, "special_rules", "adopted_unique_hr_measure_category_presence_count", sum(category in categories for categories in adopted_hr.values()), "Unique H.R. measures with at least one adopted Table 1a rule in the category.", category=category, unit="bills")

        restrictive_grants = sum(row["restrictive_structure"] == "1" for row in adopted)
        restrictive_hr = sum(bool(categories & {"structured", "closed"}) for categories in adopted_hr.values())
        add_rate(output, cohort, "special_rules", "adopted_restrictive_grant_share", restrictive_grants, len(adopted), "Adopted structured or closed grant rows divided by all adopted Table 1a grant rows.")
        add_rate(output, cohort, "special_rules", "adopted_restrictive_hr_measure_share", restrictive_hr, len(adopted_hr), "Unique H.R. measures with any adopted structured or closed rule divided by unique H.R. measures with an adopted Table 1a rule.")
        add_count(output, cohort, "special_rules", "adopted_mixed_category_resolution_count", sum(len(categories) > 1 for categories in adopted_resolutions.values()), "Adopted resolutions with grant rows in more than one category.", unit="resolutions")
        add_count(output, cohort, "special_rules", "adopted_mixed_category_hr_measure_count", sum(len(categories) > 1 for categories in adopted_hr.values()), "H.R. measures with adopted grant rows in more than one category.", unit="bills")

        stage_anomalies = sum(
            row["agenda_integrity_status"].startswith("source_stage_order_anomaly:")
            for row in agenda
        )
        lifecycle_anomalies = sum(
            row["integrity_status"].startswith("source_date_anomaly:")
            for row in agenda
        )
        add_count(output, cohort, "integrity", "stage_order_anomaly_count", stage_anomalies, "Rows with at least one non-linear stage-date sequence; affected elapsed intervals are blank.", unit="bills")
        add_count(output, cohort, "integrity", "lifecycle_source_date_anomaly_count", lifecycle_anomalies, "Rows carrying a preserved source-date anomaly from the underlying lifecycle census.", unit="bills")
        add_count(output, cohort, "integrity", "unidentified_floor_path_count", sum(row["floor_path"] == "floor_path_not_identified" for row in agenda), "Floor-considered rows without an allowed direct path classification.", unit="bills")
        add_count(output, cohort, "integrity", "mixed_floor_path_count", sum(row["floor_path"] == "mixed_special_rule_and_suspension" for row in agenda), "Rows with both adopted Table 1a special-rule and direct suspension evidence.", unit="bills")
        link_counts = Counter(row["direct_rule_link_status"] for row in agenda)
        for status in DIRECT_RULE_LINK_STATUSES:
            add_count(output, cohort, "integrity", "direct_rule_link_status_count", link_counts.get(status, 0), "Count by conservative direct-rule-use versus adopted-Table-1a linkage status.", category=status, unit="bills")

        dispositions: dict[str, str] = {}
        for row in grants:
            prior = dispositions.setdefault(row["rule_resolution_id"], row["rule_disposition"])
            require(prior == row["rule_disposition"], f"{row['rule_resolution_id']}: inconsistent disposition.")
        for disposition, count in sorted(Counter(dispositions.values()).items()):
            add_count(output, cohort, "integrity", "table1a_resolution_disposition_count", count, "Unique literal Table 1a resolutions by direct House disposition.", category=disposition, unit="resolutions")

    for congress in (116, 117, 118):
        cohort = next(value for value in COHORTS if value.cohort_id == str(congress))
        rows = [row for row in grant_rows if row["congress"] == str(congress)]
        literal = Counter(row["amendment_structure"] for row in rows)
        for category in CATEGORIES:
            narrative_count = EXPECTED_NARRATIVE_COUNTS[congress][category]
            literal_count = literal.get(category, 0)
            add_count(output, cohort, "source_reconciliation", "survey_narrative_category_count", narrative_count, "Official survey narrative amendment-structure count.", category=category, unit="grants")
            add_count(output, cohort, "source_reconciliation", "survey_literal_table_category_count", literal_count, "Identifiable literal Table 1a rule-to-measure rows.", category=category, unit="grants")
            output.append(metric_row(cohort, "source_reconciliation", "survey_literal_minus_narrative", category=category, numerator=literal_count, denominator=narrative_count, value=str(literal_count - narrative_count), unit="grants", definition="Literal Table 1a count minus official narrative count; this is reconciliation, not a rate."))

    keys = [
        (row["cohortId"], row["section"], row["metricId"], row["category"])
        for row in output
    ]
    require(len(keys) == len(set(keys)), "Metric table contains duplicate keys.")
    return output


def metric_index(
    rows: Sequence[dict[str, str]],
) -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["cohortId"], row["metricId"], row["category"]): row
        for row in rows
    }


def count_value(
    metrics: dict[tuple[str, str, str], dict[str, str]],
    cohort: str,
    metric: str,
    category: str = "",
) -> int:
    return int(metrics[(cohort, metric, category)]["value"])


def ratio_parts(
    metrics: dict[tuple[str, str, str], dict[str, str]],
    cohort: str,
    metric: str,
    category: str = "",
) -> tuple[int, int]:
    row = metrics[(cohort, metric, category)]
    return int(row["numerator"]), int(row["denominator"])


def stage_cell(
    metrics: dict[tuple[str, str, str], dict[str, str]],
    cohort: str,
    stage: str,
) -> str:
    count = count_value(metrics, cohort, f"stage_{stage}_count")
    numerator, denominator = ratio_parts(metrics, cohort, f"stage_{stage}_rate")
    require(numerator == count, f"{cohort}/{stage}: stage count/rate mismatch.")
    return f"{count} ({format_percent(numerator, denominator)})"


def write_csv(path: Path, rows: Sequence[dict[str, str]]) -> None:
    require(bool(rows), f"Refusing to write empty output: {relative(path)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_report(metrics_rows: Sequence[dict[str, str]], specification_hash: str) -> None:
    metrics = metric_index(metrics_rows)
    dev_floor = ratio_parts(metrics, "development_116_117", "stage_floor_considered_rate")
    test_floor = ratio_parts(metrics, "118", "stage_floor_considered_rate")
    dev_advance_floor = ratio_parts(
        metrics,
        "development_116_117",
        "transition_committee_advanced_to_floor_rate",
    )
    test_advance_floor = ratio_parts(
        metrics,
        "118",
        "transition_committee_advanced_to_floor_rate",
    )
    dev_special = ratio_parts(
        metrics,
        "development_116_117",
        "floor_path_share",
        "adopted_special_rule",
    )
    test_special = ratio_parts(
        metrics,
        "118",
        "floor_path_share",
        "adopted_special_rule",
    )
    dev_restrictive = ratio_parts(
        metrics,
        "development_116_117",
        "adopted_restrictive_grant_share",
    )
    test_restrictive = ratio_parts(
        metrics,
        "118",
        "adopted_restrictive_grant_share",
    )

    lines = [
        "# House Agenda-Control Source and Temporal Comparison",
        "",
        "Frozen-artifact integrity status: **PASS**. Source attribution status: **CAVEAT**. Simulator fitting is reported separately.",
        "",
        "Post-fit chamber review identifies one Senate action used as House suspension evidence in the frozen v1 panel (H.R. 4366, 118th Congress). The preserved counts below are not corrected census estimates. See [House procedure source audit](house-agenda-control-source-audit.md) for the full-archive review and the fixed-model sensitivity, which retains failure. The source mixed-route category spans a bill's history, not one scheduling decision.",
        "",
        "This report implements the locked source specification in "
        "`papers/empirical-validation/house-agenda-control-panel-specification.md`. "
        f"Specification SHA-256: `{specification_hash}`.",
        "",
        "## Descriptive Result",
        "",
        (
            "The pooled 116th-117th development cohort has "
            f"{dev_floor[0]} floor-considered H.R. measures among {dev_floor[1]} "
            f"introduced measures ({format_percent(*dev_floor)}), compared with "
            f"{test_floor[0]} of {test_floor[1]} ({format_percent(*test_floor)}) in "
            "the 118th-Congress test cohort. Among committee-advanced H.R. measures, "
            f"the observed floor-consideration transition is {format_percent(*dev_advance_floor)} "
            f"in development and {format_percent(*test_advance_floor)} in the test cohort."
        ),
        "",
        (
            "Adopted Table 1a special rules account for "
            f"{format_percent(*dev_special)} of floor-considered measures in development "
            f"and {format_percent(*test_special)} in the test cohort. Suspension remains "
            "the largest observed route in every Congress, while mixed and other direct "
            "paths remain separately identified."
        ),
        "",
        (
            "Among adopted Table 1a grant rows, the structured-or-closed share is "
            f"{dev_restrictive[0]}/{dev_restrictive[1]} "
            f"({format_percent(*dev_restrictive)}) in development and "
            f"{test_restrictive[0]}/{test_restrictive[1]} "
            f"({format_percent(*test_restrictive)}) in the test cohort. This is a "
            "description of officially classified rules, not a causal estimate of agenda power."
        ),
        "",
        "## Lifecycle and Transitions",
        "",
        "Rates in stage cells use all complete H.R. rows as the denominator. Transition rates use the preceding observed stage as the denominator.",
        "",
        "| Cohort | H.R. rows | Referred | Committee advanced | Calendar placed | Floor considered | Passed House | Enacted | Referred to advanced | Advanced to floor |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for cohort in COHORTS:
        ref_adv = ratio_parts(
            metrics,
            cohort.cohort_id,
            "transition_referred_to_committee_advanced_rate",
        )
        adv_floor = ratio_parts(
            metrics,
            cohort.cohort_id,
            "transition_committee_advanced_to_floor_rate",
        )
        lines.append(
            f"| {cohort.label} | {count_value(metrics, cohort.cohort_id, 'agenda_hr_count')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'referred')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'committee_advanced')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'calendar_placed')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'floor_considered')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'passed_house')} | "
            f"{stage_cell(metrics, cohort.cohort_id, 'enacted')} | "
            f"{ref_adv[0]}/{ref_adv[1]} ({format_percent(*ref_adv)}) | "
            f"{adv_floor[0]}/{adv_floor[1]} ({format_percent(*adv_floor)}) |"
        )

    lines.extend([
        "",
        "## Floor Routes",
        "",
        "Shares condition on substantive House floor consideration. The categories are mutually exclusive; an adopted Table 1a rule takes precedence, with concurrent suspension evidence retained as mixed.",
        "",
        "| Cohort | Route | Count | Share of floor-considered |",
        "| --- | --- | ---: | ---: |",
    ])
    path_labels = {
        "adopted_special_rule": "Adopted Table 1a special rule only",
        "suspension": "Suspension only",
        "mixed_special_rule_and_suspension": "Mixed special rule and suspension",
        "other_detected_floor_path": "Other direct path",
    }
    for cohort in COHORTS:
        for path in FLOOR_PATHS:
            count = count_value(metrics, cohort.cohort_id, "floor_path_count", path)
            share = ratio_parts(metrics, cohort.cohort_id, "floor_path_share", path)
            lines.append(
                f"| {cohort.label} | {path_labels[path]} | {count} | "
                f"{format_percent(*share)} |"
            )

    lines.extend([
        "",
        "## Special-Rule Structure",
        "",
        "The first table reconciles the official narrative counts with identifiable literal Table 1a rows. The 117th-Congress table is short by two structured and two closed rule-to-measure rows. No identities or categories are imputed for those four rows.",
        "",
        "| Congress | Category | Narrative | Literal Table 1a | Literal minus narrative |",
        "| ---: | --- | ---: | ---: | ---: |",
    ])
    for congress in ("116", "117", "118"):
        for category in CATEGORIES:
            narrative = count_value(metrics, congress, "survey_narrative_category_count", category)
            literal = count_value(metrics, congress, "survey_literal_table_category_count", category)
            difference = count_value(metrics, congress, "survey_literal_minus_narrative", category)
            lines.append(
                f"| {congress} | {category.replace('_', ' ')} | {narrative} | {literal} | {difference} |"
            )

    lines.extend([
        "",
        "Category-presence counts at the resolution level can exceed the number of unique resolutions because a single rule may cover measures assigned to different categories. H.R.-measure counts preserve the category attached to each literal grant row.",
        "",
        "| Cohort | Category | Adopted grant rows | Adopted resolution presence | Adopted H.R. measure presence |",
        "| --- | --- | ---: | ---: | ---: |",
    ])
    for cohort in COHORTS:
        for category in CATEGORIES:
            lines.append(
                f"| {cohort.label} | {category.replace('_', ' ')} | "
                f"{count_value(metrics, cohort.cohort_id, 'adopted_grant_category_count', category)} | "
                f"{count_value(metrics, cohort.cohort_id, 'adopted_unique_resolution_category_presence_count', category)} | "
                f"{count_value(metrics, cohort.cohort_id, 'adopted_unique_hr_measure_category_presence_count', category)} |"
            )

    lines.extend([
        "",
        "## Stage Timing",
        "",
        "Both summaries use the nearest-rank rule. Missing intervals are not imputed. Non-linear source stage sequences are excluded from the affected interval and reported below.",
        "",
        "| Cohort | Interval | Observed n | P50 days | P90 days |",
        "| --- | --- | ---: | ---: | ---: |",
    ])
    for cohort in COHORTS:
        for interval_id, _, label in INTERVALS:
            lines.append(
                f"| {cohort.label} | {label} | "
                f"{count_value(metrics, cohort.cohort_id, 'interval_observed_count', interval_id)} | "
                f"{count_value(metrics, cohort.cohort_id, 'interval_p50_days', interval_id)} | "
                f"{count_value(metrics, cohort.cohort_id, 'interval_p90_days', interval_id)} |"
            )

    lines.extend([
        "",
        "## Amendment-Action Coverage",
        "",
        "These are matched GovInfo direct-action records, not counts of amendments permitted by a rule. Offer-action recording is sparse, so the disposition evidence is reported separately and neither field is treated as complete amendment opportunity data.",
        "",
        "| Cohort | Route | Bills | Bills with offer action | Bills with disposition action | Offer actions | Disposition actions |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for cohort in COHORTS:
        for path in FLOOR_PATHS:
            lines.append(
                f"| {cohort.label} | {path_labels[path]} | "
                f"{count_value(metrics, cohort.cohort_id, 'floor_path_count', path)} | "
                f"{count_value(metrics, cohort.cohort_id, 'amendment_offer_evidence_bill_count', path)} | "
                f"{count_value(metrics, cohort.cohort_id, 'amendment_disposition_evidence_bill_count', path)} | "
                f"{count_value(metrics, cohort.cohort_id, 'amendment_offer_action_count', path)} | "
                f"{count_value(metrics, cohort.cohort_id, 'amendment_disposition_action_count', path)} |"
            )

    lines.extend([
        "",
        "## Integrity and Source Limits",
        "",
        "| Cohort | Non-linear stage rows | Lifecycle source-date anomalies | Unidentified floor paths | Mixed paths | Direct rule use without adopted Table 1a link | Adopted Table 1a link without direct rule-use ID |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for cohort in COHORTS:
        lines.append(
            f"| {cohort.label} | "
            f"{count_value(metrics, cohort.cohort_id, 'stage_order_anomaly_count')} | "
            f"{count_value(metrics, cohort.cohort_id, 'lifecycle_source_date_anomaly_count')} | "
            f"{count_value(metrics, cohort.cohort_id, 'unidentified_floor_path_count')} | "
            f"{count_value(metrics, cohort.cohort_id, 'mixed_floor_path_count')} | "
            f"{count_value(metrics, cohort.cohort_id, 'direct_rule_link_status_count', 'direct_rule_action_without_adopted_table1a_link')} | "
            f"{count_value(metrics, cohort.cohort_id, 'direct_rule_link_status_count', 'adopted_survey_rule_without_direct_action_id')} |"
        )

    lines.extend([
        "",
        "Direct rule-use differences are not automatically errors. Some H. Res. actions govern suspension batches, resolving-differences proceedings, or other House orders outside literal Table 1a. Conversely, a granted rule can cover a measure that is not ultimately floor-considered. In the 117th Congress, direct action records show H. Res. 1119 used for H.R. 6531 and H.R. 7309 even though literal Table 1a omits those measure rows; their amendment structures remain unassigned in this panel.",
        "",
        "The 117 total preserved non-linear stage rows across the three Congresses arise when a later committee-stage date follows an earlier floor event or, less often, when the first extracted referral follows the first extracted advance event. Their affected elapsed intervals are blank rather than negative.",
        "",
        "## Simulator Implication and Boundary",
        "",
        "The source evidence supports representing suspension, adopted special-rule, mixed, and other detected floor paths separately. It also shows that the official special-rule categories in these completed Congresses are overwhelmingly structured or closed. Those observations identify a structural comparison target, but they do not authorize parameter fitting by themselves.",
        "",
        CLAIM_BOUNDARY,
        "",
        "A separate pre-fit specification must freeze comparable simulator metrics, development-only fitting, seeds, candidate grid, loss, tie-breaking, and 118th-Congress no-refit tolerances before simulator behavior changes.",
        "",
        "## Reproduction",
        "",
        "Run `make house-agenda-control-study`. The study uses the committed source panels and Python's standard library. Source, specification, implementation, and output hashes are recorded in `reports/house-agenda-control-study-metadata.json`.",
        "",
    ])
    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def write_metadata(
    metrics_rows: Sequence[dict[str, str]],
    agenda_rows: Sequence[dict[str, str]],
    grant_rows: Sequence[dict[str, str]],
) -> None:
    metrics = metric_index(metrics_rows)
    cohort_results: dict[str, object] = {}
    for cohort in COHORTS:
        cohort_results[cohort.cohort_id] = {
            "congresses": list(cohort.congresses),
            "agendaRows": count_value(metrics, cohort.cohort_id, "agenda_hr_count"),
            "floorConsidered": count_value(
                metrics, cohort.cohort_id, "stage_floor_considered_count"
            ),
            "floorPaths": {
                path: count_value(
                    metrics, cohort.cohort_id, "floor_path_count", path
                )
                for path in FLOOR_PATHS
            },
            "stageOrderAnomalies": count_value(
                metrics, cohort.cohort_id, "stage_order_anomaly_count"
            ),
            "unidentifiedFloorPaths": count_value(
                metrics, cohort.cohort_id, "unidentified_floor_path_count"
            ),
        }
    reconciliation = {
        str(congress): {
            category: {
                "narrative": EXPECTED_NARRATIVE_COUNTS[congress][category],
                "literalTable": EXPECTED_LITERAL_COUNTS[congress][category],
                "literalMinusNarrative": (
                    EXPECTED_LITERAL_COUNTS[congress][category]
                    - EXPECTED_NARRATIVE_COUNTS[congress][category]
                ),
            }
            for category in CATEGORIES
        }
        for congress in (116, 117, 118)
    }
    metadata = {
        "schemaVersion": 1,
        "studyVersion": STUDY_VERSION,
        "status": "frozen_v1_artifact_pass_source_attribution_caveat",
        "sourceAudit": "reports/house-agenda-control-source-audit.md",
        "claimBoundary": CLAIM_BOUNDARY,
        "temporalDesign": {
            "developmentCongresses": [116, 117],
            "primaryTestCongress": 118,
            "outcomeBlind": False,
            "percentileMethod": "nearest_rank_ceiling",
        },
        "specification": {
            "path": relative(SPECIFICATION),
            "sha256": sha256_file(SPECIFICATION),
            "status": "locked_post_source_audit_pre_hr_metrics",
        },
        "implementation": {
            "path": relative(SCRIPT_PATH),
            "sha256": sha256_file(SCRIPT_PATH),
            "runtime": "Python standard library",
        },
        "sources": [
            {
                "path": relative(AGENDA_PANEL),
                "rowsExcludingHeader": len(agenda_rows),
                "sha256": sha256_file(AGENDA_PANEL),
            },
            {
                "path": relative(GRANT_PANEL),
                "rowsExcludingHeader": len(grant_rows),
                "sha256": sha256_file(GRANT_PANEL),
            },
        ],
        "outputs": [
            {"path": relative(METRICS_OUTPUT), "sha256": sha256_file(METRICS_OUTPUT)},
            {"path": relative(REPORT_OUTPUT), "sha256": sha256_file(REPORT_OUTPUT)},
        ],
        "cohortResults": cohort_results,
        "sourceReconciliation": reconciliation,
    }
    METADATA_OUTPUT.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    agenda_rows = read_csv(AGENDA_PANEL)
    grant_rows = read_csv(GRANT_PANEL)
    validate_inputs(agenda_rows, grant_rows)
    metrics_rows = build_metrics(agenda_rows, grant_rows)
    write_csv(METRICS_OUTPUT, metrics_rows)
    specification_hash = sha256_file(SPECIFICATION)
    write_report(metrics_rows, specification_hash)
    write_metadata(metrics_rows, agenda_rows, grant_rows)
    print(f"Wrote {relative(METRICS_OUTPUT)} ({len(metrics_rows)} metrics)")
    print(f"Wrote {relative(REPORT_OUTPUT)}")
    print(f"Wrote {relative(METADATA_OUTPUT)}")


if __name__ == "__main__":
    main()
