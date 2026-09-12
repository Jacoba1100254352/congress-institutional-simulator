#!/usr/bin/env python3
"""Hard-check the locked House agenda-control source study artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AGENDA_PANEL = ROOT / "data/validation/raw/house_agenda_control.csv"
GRANT_PANEL = ROOT / "data/validation/raw/house_special_rule_grants.csv"
RAW_METADATA = ROOT / "data/validation/raw/house_agenda_control.metadata.md"
SPECIFICATION = (
    ROOT
    / "papers/empirical-validation/house-agenda-control-panel-specification.md"
)
BUILDER = ROOT / "scripts/validation/build_house_agenda_control_panel.py"
WRITER = ROOT / "scripts/validation/write_house_agenda_control_study.py"
METRICS = ROOT / "reports/house-agenda-control-metrics.csv"
REPORT = ROOT / "reports/house-agenda-control-study.md"
STUDY_METADATA = ROOT / "reports/house-agenda-control-study-metadata.json"

EXPECTED_HASHES = {
    "agenda": "d801a86290d2eb7127736ef259a44847fe5d19acff2c4dd738d2f00ba0556f7b",
    "grants": "5b31f228e25449f05210234c19a8c9311911c5f75a35d9dd6bb77d6333988a53",
    "specification": "28c1b3874fb99a1987f1f8b146517dd4f2be14f74ea93b36bfadbb48591200ec",
}
OFFICIAL_SOURCE_HASHES = {
    "5d65df8e35bc575d9c31b3bce10913647dd1dc59b7d8c68f9253f14490eb344a",
    "a7777dcd7bec4ff4d00477ec8ad405226505972efbf86e6f5395af215258c969",
    "62a7f7d70939c357c7bd7ab8bd8491ddcc6602665796382fc2c2df1ef9eb0aae",
    "dc79a72dea6c2ad6ff4e4065a2f44b9f954e0f3880ad9e86e1740ef69d71772a",
    "2a915021d570e1de5592d5126be42ce3f02251a9252961c7ac98eb51d6796e72",
    "b71a85e04d980fde4c4ad95919f214c4154575ddb874afb365b547e82b634e43",
    "b3775e79914a9db29b3a8d55ae13638020c44822dcecb9e4517371e093d01dde",
    "658b2d280e4e7972c86bfd810ebff0c9bb61c115b242de8c8774034dea08de03",
    "8e7ca7dab50a7b9b977f021ec1b3231f8fedf82c33494553857b892fadfdba98",
}
EXPECTED_AGENDA_ROWS = {"116": 9062, "117": 9709, "118": 10564}
EXPECTED_LITERAL = {
    "116": Counter({"structured": 55, "closed": 60}),
    "117": Counter({"structured": 57, "closed": 87}),
    "118": Counter({"modified_open": 1, "structured": 83, "closed": 115}),
}
EXPECTED_ROUTES = {
    "116": Counter(
        {
            "adopted_special_rule": 69,
            "suspension": 644,
            "mixed_special_rule_and_suspension": 17,
            "other_detected_floor_path": 48,
        }
    ),
    "117": Counter(
        {
            "adopted_special_rule": 86,
            "suspension": 604,
            "mixed_special_rule_and_suspension": 21,
            "other_detected_floor_path": 11,
        }
    ),
    "118": Counter(
        {
            "adopted_special_rule": 127,
            "suspension": 544,
            "mixed_special_rule_and_suspension": 4,
            "other_detected_floor_path": 1,
        }
    ),
}
EXPECTED_DISPOSITIONS = {
    "116": Counter({"adopted": 69}),
    "117": Counter({"adopted": 66, "tabled": 3}),
    "118": Counter(
        {"adopted": 56, "adopted_amended": 4, "rejected": 6, "tabled": 1}
    ),
}
EXPECTED_STAGE_ANOMALIES = {"116": 70, "117": 32, "118": 15}


class CheckError(RuntimeError):
    """Raised when a publication gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def sha256_file(path: Path) -> str:
    require(path.exists(), f"Missing artifact: {path.relative_to(ROOT)}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def top_level_metadata(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            values[key] = value.strip().strip("`")
    return values


def check_source_pins() -> None:
    require(sha256_file(AGENDA_PANEL) == EXPECTED_HASHES["agenda"], "Agenda panel hash drifted.")
    require(sha256_file(GRANT_PANEL) == EXPECTED_HASHES["grants"], "Grant panel hash drifted.")
    require(sha256_file(SPECIFICATION) == EXPECTED_HASHES["specification"], "Locked specification hash drifted.")
    raw_text = RAW_METADATA.read_text(encoding="utf-8")
    for path in (RAW_METADATA, GRANT_PANEL.with_suffix(".metadata.md")):
        text = path.read_text(encoding="utf-8")
        require(
            str(ROOT) not in text
            and not any(prefix in text for prefix in ("/Users/", "/home/", "/var/folders/")),
            "Public House metadata contains a machine-specific path.",
        )
    for digest in OFFICIAL_SOURCE_HASHES:
        require(digest in raw_text, f"Raw metadata lacks official source pin {digest}.")
    metadata = top_level_metadata(RAW_METADATA)
    require(metadata.get("agenda_output_sha256") == EXPECTED_HASHES["agenda"], "Raw metadata agenda hash drifted.")
    require(metadata.get("grant_output_sha256") == EXPECTED_HASHES["grants"], "Raw metadata grant hash drifted.")
    require(metadata.get("specification_sha256") == EXPECTED_HASHES["specification"], "Raw metadata specification hash drifted.")
    require(metadata.get("builder_sha256") == sha256_file(BUILDER), "Raw metadata builder hash is stale.")


def check_panels(
    agenda: list[dict[str, str]],
    grants: list[dict[str, str]],
) -> None:
    require(len(agenda) == 29335, "Agenda panel must contain 29,335 H.R. rows.")
    require(len(grants) == 458, "Grant panel must contain 458 literal Table 1a rows.")
    require(len({row["bill_id"] for row in agenda}) == len(agenda), "Duplicate agenda bill IDs.")
    require(len({row["grant_id"] for row in grants}) == len(grants), "Duplicate grant IDs.")
    agenda_ids = {row["bill_id"] for row in agenda}
    for congress in ("116", "117", "118"):
        agenda_rows = [row for row in agenda if row["congress"] == congress]
        grant_rows = [row for row in grants if row["congress"] == congress]
        require(len(agenda_rows) == EXPECTED_AGENDA_ROWS[congress], f"{congress}: agenda count drifted.")
        require(Counter(row["amendment_structure"] for row in grant_rows) == EXPECTED_LITERAL[congress], f"{congress}: literal category counts drifted.")
        floor_rows = [row for row in agenda_rows if row["floor_considered"] == "1"]
        require(Counter(row["floor_path"] for row in floor_rows) == EXPECTED_ROUTES[congress], f"{congress}: floor routes drifted.")
        require(all(row["floor_path"] != "floor_path_not_identified" for row in floor_rows), f"{congress}: unidentified floor path returned.")
        anomaly_count = sum(
            row["agenda_integrity_status"].startswith("source_stage_order_anomaly:")
            for row in agenda_rows
        )
        require(anomaly_count == EXPECTED_STAGE_ANOMALIES[congress], f"{congress}: stage anomaly count drifted.")

    for row in grants:
        if row["covered_measure_type"] == "hr":
            require(row["covered_measure_in_hr_census"] == "1", f"{row['grant_id']}: H.R. link failed.")
            require(row["covered_measure_id"] in agenda_ids, f"{row['grant_id']}: H.R. parent missing.")

    dispositions: dict[str, str] = {}
    for row in grants:
        prior = dispositions.setdefault(row["rule_resolution_id"], row["rule_disposition"])
        require(prior == row["rule_disposition"], f"{row['rule_resolution_id']}: inconsistent disposition.")
    for congress in ("116", "117", "118"):
        counts = Counter(
            disposition
            for rule_id, disposition in dispositions.items()
            if rule_id.startswith(f"{congress}-")
        )
        require(counts == EXPECTED_DISPOSITIONS[congress], f"{congress}: resolution dispositions drifted.")


def metric_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    keys = [(row["cohortId"], row["metricId"], row["category"]) for row in rows]
    require(len(keys) == len(set(keys)), "Metric table has duplicate keys.")
    return {key: row for key, row in zip(keys, rows)}


def require_metric(
    metrics: dict[tuple[str, str, str], dict[str, str]],
    cohort: str,
    metric: str,
    *,
    category: str = "",
    numerator: str | None = None,
    denominator: str | None = None,
    value: str | None = None,
) -> None:
    key = (cohort, metric, category)
    require(key in metrics, f"Missing metric {key}.")
    row = metrics[key]
    if numerator is not None:
        require(row["numerator"] == numerator, f"{key}: numerator drifted.")
    if denominator is not None:
        require(row["denominator"] == denominator, f"{key}: denominator drifted.")
    if value is not None:
        require(row["value"] == value, f"{key}: value drifted.")


def check_metrics(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 469, "Metric row count drifted.")
    metrics = metric_index(rows)
    require_metric(metrics, "development_116_117", "stage_floor_considered_rate", numerator="1500", denominator="18771", value="0.079910500240")
    require_metric(metrics, "118", "stage_floor_considered_rate", numerator="676", denominator="10564", value="0.063990912533")
    require_metric(metrics, "development_116_117", "transition_committee_advanced_to_floor_rate", numerator="1176", denominator="1912", value="0.615062761506")
    require_metric(metrics, "118", "transition_committee_advanced_to_floor_rate", numerator="600", denominator="1202", value="0.499168053245")
    require_metric(metrics, "development_116_117", "floor_path_share", category="adopted_special_rule", numerator="155", denominator="1500", value="0.103333333333")
    require_metric(metrics, "118", "floor_path_share", category="adopted_special_rule", numerator="127", denominator="676", value="0.187869822485")
    require_metric(metrics, "development_116_117", "adopted_restrictive_grant_share", numerator="255", denominator="255", value="1.000000000000")
    require_metric(metrics, "118", "adopted_restrictive_grant_share", numerator="178", denominator="179", value="0.994413407821")
    require_metric(metrics, "117", "survey_literal_minus_narrative", category="structured", value="-2")
    require_metric(metrics, "117", "survey_literal_minus_narrative", category="closed", value="-2")
    require_metric(metrics, "development_116_117", "interval_p50_days", category="committee_advance_to_floor", value="63")
    require_metric(metrics, "development_116_117", "interval_p90_days", category="committee_advance_to_floor", value="218")
    require_metric(metrics, "118", "interval_p50_days", category="committee_advance_to_floor", value="105")
    require_metric(metrics, "118", "interval_p90_days", category="committee_advance_to_floor", value="292")
    for cohort in ("116", "117", "development_116_117", "118"):
        require_metric(metrics, cohort, "unidentified_floor_path_count", value="0")


def check_metadata() -> None:
    metadata = json.loads(STUDY_METADATA.read_text(encoding="utf-8"))
    require(metadata.get("schemaVersion") == 1, "Study metadata schema drifted.")
    require(metadata.get("studyVersion") == "house-agenda-control-source-study-v1", "Study version drifted.")
    require(metadata.get("status") == "frozen_v1_artifact_pass_source_attribution_caveat", "Study status drifted.")
    require(metadata["specification"]["sha256"] == EXPECTED_HASHES["specification"], "Study metadata specification hash drifted.")
    require(metadata["implementation"]["sha256"] == sha256_file(WRITER), "Study metadata writer hash is stale.")
    sources = {row["path"]: row for row in metadata["sources"]}
    outputs = {row["path"]: row for row in metadata["outputs"]}
    require(sources["data/validation/raw/house_agenda_control.csv"]["sha256"] == sha256_file(AGENDA_PANEL), "Study metadata agenda hash is stale.")
    require(sources["data/validation/raw/house_special_rule_grants.csv"]["sha256"] == sha256_file(GRANT_PANEL), "Study metadata grant hash is stale.")
    require(outputs["reports/house-agenda-control-metrics.csv"]["sha256"] == sha256_file(METRICS), "Study metadata metrics hash is stale.")
    require(outputs["reports/house-agenda-control-study.md"]["sha256"] == sha256_file(REPORT), "Study metadata report hash is stale.")
    reconciliation = metadata["sourceReconciliation"]["117"]
    require(reconciliation["structured"]["literalMinusNarrative"] == -2, "Metadata lost structured discrepancy.")
    require(reconciliation["closed"]["literalMinusNarrative"] == -2, "Metadata lost closed discrepancy.")
    require(metadata["cohortResults"]["118"]["unidentifiedFloorPaths"] == 0, "Metadata reports an unidentified test path.")


def check_report() -> None:
    text = REPORT.read_text(encoding="utf-8")
    required = (
        "Frozen-artifact integrity status: **PASS**. Source attribution status: **CAVEAT**.",
        "one Senate action used as House suspension evidence",
        "No identities or categories are imputed for those four rows.",
        "not a causal estimate of agenda power",
        "do not authorize parameter fitting by themselves",
        "Official-source descriptive House procedure and timing evidence only",
        "separate pre-fit specification",
    )
    for phrase in required:
        require(phrase in text, f"Report lacks required boundary text: {phrase!r}")
    folded = text.casefold()
    for forbidden in (
        "validates the simulator",
        "proves agenda control",
        "caused the decline",
        "causal effect of a special rule",
    ):
        require(forbidden not in folded, f"Report contains forbidden overclaim: {forbidden!r}")


def main() -> None:
    check_source_pins()
    agenda = read_csv(AGENDA_PANEL)
    grants = read_csv(GRANT_PANEL)
    check_panels(agenda, grants)
    metrics = read_csv(METRICS)
    check_metrics(metrics)
    check_metadata()
    check_report()
    print(
        "House agenda-control study check passed: 29,335 H.R. rows, "
        "458 literal grants, 469 metrics, zero unidentified floor paths."
    )


if __name__ == "__main__":
    main()
