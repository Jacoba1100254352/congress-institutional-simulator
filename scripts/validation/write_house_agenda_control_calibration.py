#!/usr/bin/env python3
"""Run the locked House agenda-control simulator calibration and temporal test."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
from collections import Counter, defaultdict
from math import fsum, sqrt
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "papers" / "empirical-validation" / "house-agenda-control-calibration-specification.md"
AMENDMENT = ROOT / "papers" / "empirical-validation" / "house-agenda-control-provenance-amendment.md"
SOURCE_METRICS = ROOT / "reports" / "house-agenda-control-metrics.csv"
SOURCE_AGENDA = ROOT / "data" / "validation" / "raw" / "house_agenda_control.csv"
SOURCE_GRANTS = ROOT / "data" / "validation" / "raw" / "house_special_rule_grants.csv"
BASELINE = ROOT / "reports" / "legislative-lifecycle-calibration.csv"
PROBE_SOURCE = ROOT / "src" / "main" / "java" / "congresssim" / "simulation" / "catalog" / "HouseAgendaControlCalibrationProbe.java"
SIMULATOR_SOURCE = ROOT / "src" / "main" / "java" / "congresssim" / "institution" / "agenda" / "FloorRuleSchedulingProcess.java"
OUT_CANDIDATES = ROOT / "reports" / "house-agenda-control-calibration-candidates.csv"
OUT_METRICS = ROOT / "reports" / "house-agenda-control-calibration-metrics.csv"
OUT_REPORT = ROOT / "reports" / "house-agenda-control-calibration.md"
OUT_METADATA = ROOT / "reports" / "house-agenda-control-calibration-metadata.json"
OUT_SEEDS = ROOT / "reports" / "house-agenda-control-calibration-seeds.csv"
OUT_MONTE_CARLO = ROOT / "reports" / "house-agenda-control-calibration-monte-carlo.csv"

DEVELOPMENT_COHORT = "development_116_117"
TEST_COHORT = "118"

CALENDAR_THRESHOLDS = tuple(round(value / 100, 2) for value in range(62, 71, 2))
SPECIAL_THRESHOLDS = tuple(round(0.350 + (0.025 * index), 3) for index in range(17))
SUSPENSION_THRESHOLDS = tuple(round(0.350 + (0.025 * index), 3) for index in range(17))

DEVELOPMENT_SEED_BASE = 1_161_170_001
DEVELOPMENT_SEED_STEP = 104_729
DEVELOPMENT_SEED_COUNT = 20
DEVELOPMENT_SEEDS = tuple(
    DEVELOPMENT_SEED_BASE + (DEVELOPMENT_SEED_STEP * index)
    for index in range(DEVELOPMENT_SEED_COUNT)
)
DEVELOPMENT_RUNS = 12

TEST_SEED_BASE = 1_180_000_001
TEST_SEED_STEP = 130_363
TEST_SEED_COUNT = 30
TEST_SEEDS = tuple(
    TEST_SEED_BASE + (TEST_SEED_STEP * index)
    for index in range(TEST_SEED_COUNT)
)
TEST_RUNS = 20

EXPECTED_CANDIDATES = 1_445
EXPECTED_DEVELOPMENT_BILLS_PER_CANDIDATE = 14_400
EXPECTED_TEST_BILLS = 36_000
EXPECTED_JAVA_MAJOR = 21

ROUTE_FIELDS = (
    "specialRuleOnlyRouteShare",
    "suspensionOnlyRouteShare",
    "mixedSpecialRuleAndSuspensionRouteShare",
    "otherFloorRouteShare",
)
MONTE_CARLO_FIELDS = (
    "committeeAdvanceRate",
    "floorConsiderationRate",
    "advanceToFloorRate",
    "enactmentRate",
    *ROUTE_FIELDS,
    "restrictiveSpecialRuleShare",
    "closedRuleRate",
    "openRuleRate",
    "calendarCapacityDenialRate",
    "routeTotalVariation",
)
SELECTION_TOLERANCES = {
    "floorConsiderationRate": 0.015,
    "specialRuleOnlyRouteShare": 0.040,
    "suspensionOnlyRouteShare": 0.050,
    "mixedSpecialRuleAndSuspensionRouteShare": 0.020,
    "otherFloorRouteShare": 0.030,
}
TEST_TOLERANCES = {
    "committeeAdvanceRate": 0.020,
    "floorConsiderationRate": 0.020,
    "routeTotalVariation": 0.100,
    "restrictiveSpecialRuleShare": 0.020,
}

EXPECTED_SOURCE_TARGETS = {
    DEVELOPMENT_COHORT: {
        "agendaHrCount": (18_771, None, 18_771.0),
        "committeeAdvanceRate": (1_912, 18_771, 0.101859250972),
        "floorConsiderationRate": (1_500, 18_771, 0.079910500240),
        "advanceToFloorRate": (1_176, 1_912, 0.615062761506),
        "specialRuleOnlyRouteShare": (155, 1_500, 0.103333333333),
        "suspensionOnlyRouteShare": (1_248, 1_500, 0.832000000000),
        "mixedSpecialRuleAndSuspensionRouteShare": (38, 1_500, 0.025333333333),
        "otherFloorRouteShare": (59, 1_500, 0.039333333333),
        "restrictiveSpecialRuleShare": (198, 198, 1.0),
    },
    TEST_COHORT: {
        "agendaHrCount": (10_564, None, 10_564.0),
        "committeeAdvanceRate": (1_202, 10_564, 0.113782658084),
        "floorConsiderationRate": (676, 10_564, 0.063990912533),
        "advanceToFloorRate": (600, 1_202, 0.499168053245),
        "specialRuleOnlyRouteShare": (127, 676, 0.187869822485),
        "suspensionOnlyRouteShare": (544, 676, 0.804733727811),
        "mixedSpecialRuleAndSuspensionRouteShare": (4, 676, 0.005917159763),
        "otherFloorRouteShare": (1, 676, 0.001479289941),
        "restrictiveSpecialRuleShare": (134, 135, 0.992592592593),
    },
}

SOURCE_METRIC_KEYS = {
    "agendaHrCount": ("population", "agenda_hr_count", ""),
    "committeeAdvanceRate": ("lifecycle", "stage_committee_advanced_rate", ""),
    "floorConsiderationRate": ("lifecycle", "stage_floor_considered_rate", ""),
    "advanceToFloorRate": (
        "transitions",
        "transition_committee_advanced_to_floor_rate",
        "",
    ),
    "specialRuleOnlyRouteShare": (
        "floor_routes",
        "floor_path_share",
        "adopted_special_rule",
    ),
    "suspensionOnlyRouteShare": (
        "floor_routes",
        "floor_path_share",
        "suspension",
    ),
    "mixedSpecialRuleAndSuspensionRouteShare": (
        "floor_routes",
        "floor_path_share",
        "mixed_special_rule_and_suspension",
    ),
    "otherFloorRouteShare": (
        "floor_routes",
        "floor_path_share",
        "other_detected_floor_path",
    ),
    "restrictiveSpecialRuleShare": (
        "special_rules",
        "adopted_restrictive_hr_measure_share",
        "",
    ),
}

MEAN_FIELDS = (
    "committeeAdvanceRate",
    "floorConsiderationRate",
    "enactmentRate",
    "specialRuleOnlyRouteRate",
    "suspensionOnlyRouteRate",
    "mixedSpecialRuleAndSuspensionRouteRate",
    "otherFloorRouteRate",
    "floorRouteAssignmentRate",
    "restrictiveSpecialRuleRouteRate",
    "closedRuleRate",
    "openRuleRate",
    "calendarCapacityDenialRate",
)

CLAIM_BOUNDARY = (
    "This study calibrates one aggregate synthetic route assignment against one "
    "pooled development cohort and applies an unchanged scenario to one later "
    "completed Congress. It does not validate bill-level agenda decisions, causal "
    "gatekeeping, leadership motives, amendment opportunities, calendar timing, "
    "downstream outcomes, welfare, representation, capture, or institutional rankings."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def source_targets() -> dict[str, dict[str, tuple[int, int | None, float]]]:
    rows = read_csv(SOURCE_METRICS)
    output: dict[str, dict[str, tuple[int, int | None, float]]] = defaultdict(dict)
    for cohort, expected in EXPECTED_SOURCE_TARGETS.items():
        for name, (expected_numerator, expected_denominator, expected_value) in expected.items():
            section, metric_id, category = SOURCE_METRIC_KEYS[name]
            matches = [
                row
                for row in rows
                if row["cohortId"] == cohort
                and row["section"] == section
                and row["metricId"] == metric_id
                and row["category"] == category
            ]
            require(len(matches) == 1, f"Expected one source metric for {cohort} {name}.")
            row = matches[0]
            numerator = int(row["numerator"])
            denominator = int(row["denominator"]) if row["denominator"] else None
            value = float(row["value"])
            require(numerator == expected_numerator, f"Source numerator drifted for {cohort} {name}.")
            require(
                denominator == expected_denominator,
                f"Source denominator drifted for {cohort} {name}.",
            )
            require(
                abs(value - expected_value) <= 5e-13,
                f"Source value drifted for {cohort} {name}: {value}",
            )
            output[cohort][name] = (numerator, denominator, value)
    return dict(output)


def validate_baseline() -> dict[str, str]:
    rows = read_csv(BASELINE)
    selected = [row for row in rows if row.get("selected") == "1"]
    require(len(selected) == 1, "Lifecycle baseline must retain exactly one selected row.")
    row = selected[0]
    expected = {
        "calendarPriorityThreshold": "0.680",
        "seedCount": "50",
        "runsPerSeed": "24",
        "simulatedBills": "72000",
        "committeeAdvanceRate": "0.106278",
        "floorConsiderationRate": "0.061097",
        "enactmentRate": "0.027417",
    }
    for field, value in expected.items():
        require(row.get(field) == value, f"Frozen lifecycle baseline drifted at {field}.")
    return row


def parse_java_major(version_output: str) -> int:
    match = re.search(r'version "(?:1\.)?(\d+)', version_output)
    require(match is not None, f"Could not parse Java runtime version: {version_output!r}")
    return int(match.group(1))


def resolve_java_runtime() -> tuple[str, str]:
    configured = os.environ.get("JAVA_BIN")
    java_home = os.environ.get("JAVA_HOME")
    if configured:
        java_bin = configured
    elif java_home:
        java_bin = str(Path(java_home) / "bin" / "java")
    else:
        java_bin = shutil.which("java") or "java"
    completed = subprocess.run(
        [java_bin, "-version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    version_output = "\n".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
    )
    major = parse_java_major(version_output)
    require(
        major == EXPECTED_JAVA_MAJOR,
        f"House agenda-control calibration requires Java {EXPECTED_JAVA_MAJOR}; "
        f"found Java {major} at {java_bin}. Set JAVA_HOME to a Java "
        f"{EXPECTED_JAVA_MAJOR} installation.",
    )
    version_line = version_output.splitlines()[0]
    return java_bin, version_line


def run_probe(
    runs: int,
    seeds: Iterable[int],
    calendar_thresholds: Iterable[float],
    special_thresholds: Iterable[float],
    suspension_thresholds: Iterable[float],
    java_bin: str | None = None,
) -> list[dict[str, str]]:
    app_cp = os.environ.get("APP_CP", "out/congresssim.jar")
    jar_path = ROOT / app_cp
    require(jar_path.exists(), f"Missing simulator JAR: {jar_path}; run make build.")
    if java_bin is None:
        java_bin, _ = resolve_java_runtime()
    java_props = shlex.split(os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21"))
    command = [
        java_bin,
        *java_props,
        "-cp",
        app_cp,
        "congresssim.simulation.catalog.HouseAgendaControlCalibrationProbe",
        str(runs),
        ",".join(str(seed) for seed in seeds),
        ",".join(f"{value:.3f}" for value in calendar_thresholds),
        ",".join(f"{value:.3f}" for value in special_thresholds),
        ",".join(f"{value:.3f}" for value in suspension_thresholds),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    rows = list(csv.DictReader(completed.stdout.splitlines()))
    require(rows, "House agenda-control probe returned no rows.")
    return rows


def candidate_key(row: dict[str, str] | dict[str, float]) -> tuple[float, float, float]:
    return (
        float(row["calendarPriorityThreshold"]),
        float(row["specialRuleThreshold"]),
        float(row["suspensionThreshold"]),
    )


def aggregate_probe_rows(
    rows: list[dict[str, str]],
    targets: dict[str, tuple[int, int | None, float]],
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[float, float, float], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[candidate_key(row)].append(row)

    output: list[dict[str, float | int | str]] = []
    for key in sorted(grouped):
        candidate_rows = grouped[key]
        total_bills = sum(int(row["bills"]) for row in candidate_rows)
        require(total_bills > 0, f"Candidate {key} has no simulated bills.")
        result: dict[str, float | int | str] = {
            "calendarPriorityThreshold": key[0],
            "specialRuleThreshold": key[1],
            "suspensionThreshold": key[2],
            "seedCount": len(candidate_rows),
            "runsPerSeed": int(candidate_rows[0]["runs"]),
            "simulatedBills": total_bills,
        }
        for field in MEAN_FIELDS:
            result[field] = fsum(
                float(row[field]) * int(row["bills"]) for row in candidate_rows
            ) / total_bills

        floor = float(result["floorConsiderationRate"])
        route_total = fsum(float(result[field]) for field in (
            "specialRuleOnlyRouteRate",
            "suspensionOnlyRouteRate",
            "mixedSpecialRuleAndSuspensionRouteRate",
            "otherFloorRouteRate",
        ))
        require(
            abs(route_total - floor) <= 2e-12,
            f"Candidate {key} route total differs from floor rate.",
        )
        require(
            abs(float(result["floorRouteAssignmentRate"]) - floor) <= 2e-12,
            f"Candidate {key} route assignment differs from floor rate.",
        )
        result["advanceToFloorRate"] = (
            floor / float(result["committeeAdvanceRate"])
            if float(result["committeeAdvanceRate"]) > 0.0
            else 0.0
        )
        route_mapping = {
            "specialRuleOnlyRouteShare": "specialRuleOnlyRouteRate",
            "suspensionOnlyRouteShare": "suspensionOnlyRouteRate",
            "mixedSpecialRuleAndSuspensionRouteShare": "mixedSpecialRuleAndSuspensionRouteRate",
            "otherFloorRouteShare": "otherFloorRouteRate",
        }
        for share_field, rate_field in route_mapping.items():
            result[share_field] = float(result[rate_field]) / floor if floor else 0.0
        special_denominator = float(result["specialRuleOnlyRouteRate"]) + float(
            result["mixedSpecialRuleAndSuspensionRouteRate"]
        )
        result["restrictiveSpecialRuleShare"] = (
            float(result["restrictiveSpecialRuleRouteRate"]) / special_denominator
            if special_denominator
            else 0.0
        )

        standardized_errors: list[float] = []
        squared_errors: list[float] = []
        for field, tolerance in SELECTION_TOLERANCES.items():
            target = targets[field][2]
            error = float(result[field]) - target
            standardized = error / tolerance
            result[f"{field}Error"] = error
            result[f"{field}StandardizedError"] = standardized
            standardized_errors.append(abs(standardized))
            squared_errors.append(standardized * standardized)
        result["selectionLoss"] = fsum(squared_errors)
        result["maximumAbsoluteStandardizedError"] = max(standardized_errors)
        result["selected"] = "0"
        output.append(result)
    return output


def selection_key(row: dict[str, float | int | str]) -> tuple[float, float, float, float, float]:
    return (
        float(row["selectionLoss"]),
        float(row["maximumAbsoluteStandardizedError"]),
        float(row["calendarPriorityThreshold"]),
        float(row["specialRuleThreshold"]),
        float(row["suspensionThreshold"]),
    )


def select_candidate(
    candidates: list[dict[str, float | int | str]],
) -> dict[str, float | int | str]:
    require(candidates, "No calibration candidates were available for selection.")
    selected = min(candidates, key=selection_key)
    selected["selected"] = "1"
    return selected


def leave_one_seed_out(
    probe_rows: list[dict[str, str]],
    targets: dict[str, tuple[int, int | None, float]],
) -> Counter[tuple[float, float, float]]:
    seeds = sorted({row["seed"] for row in probe_rows}, key=int)
    selections: Counter[tuple[float, float, float]] = Counter()
    for omitted in seeds:
        candidates = aggregate_probe_rows(
            [row for row in probe_rows if row["seed"] != omitted],
            targets,
        )
        selected = select_candidate(candidates)
        selections[candidate_key(selected)] += 1
    return selections


def total_variation(
    observed: dict[str, float | int | str],
    targets: dict[str, tuple[int, int | None, float]],
) -> float:
    return 0.5 * fsum(
        abs(float(observed[field]) - targets[field][2]) for field in ROUTE_FIELDS
    )


def test_gate(
    test_result: dict[str, float | int | str],
    targets: dict[str, tuple[int, int | None, float]],
) -> dict[str, object]:
    committee_error = float(test_result["committeeAdvanceRate"]) - targets["committeeAdvanceRate"][2]
    floor_error = float(test_result["floorConsiderationRate"]) - targets["floorConsiderationRate"][2]
    route_tv = total_variation(test_result, targets)
    restrictive_error = (
        float(test_result["restrictiveSpecialRuleShare"])
        - targets["restrictiveSpecialRuleShare"][2]
    )
    checks = {
        "committeeAdvanceRate": abs(committee_error) <= TEST_TOLERANCES["committeeAdvanceRate"] + 1e-15,
        "floorConsiderationRate": abs(floor_error) <= TEST_TOLERANCES["floorConsiderationRate"] + 1e-15,
        "routeTotalVariation": route_tv <= TEST_TOLERANCES["routeTotalVariation"] + 1e-15,
        "restrictiveSpecialRuleShare": abs(restrictive_error)
        <= TEST_TOLERANCES["restrictiveSpecialRuleShare"] + 1e-15,
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "committeeAdvanceError": committee_error,
        "floorConsiderationError": floor_error,
        "routeTotalVariation": route_tv,
        "restrictiveSpecialRuleShareError": restrictive_error,
    }


def format_float(value: float | int | str) -> str:
    return f"{float(value):.12f}"


def seed_metric_rows(
    probe_rows: list[dict[str, str]],
    selected: tuple[float, float, float],
    cohort: str,
    targets: dict[str, tuple[int, int | None, float]],
) -> list[dict[str, str]]:
    rows = sorted(
        (row for row in probe_rows if candidate_key(row) == selected),
        key=lambda row: int(row["seed"]),
    )
    require(len({row["seed"] for row in rows}) == len(rows), "Duplicate Monte Carlo seed.")
    output = []
    for row in rows:
        candidate = aggregate_probe_rows([row], targets)[0]
        require(float(candidate["floorConsiderationRate"]) > 0.0, "Seed has no floor observations.")
        candidate["routeTotalVariation"] = total_variation(candidate, targets)
        output.append({
            "cohort": cohort,
            "seed": row["seed"],
            "runs": row["runs"],
            "simulatedBills": row["bills"],
            **{field: format_float(candidate[field]) for field in MONTE_CARLO_FIELDS},
        })
    return output


def monte_carlo_summary(seed_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Summarize seed variation, without adding or altering any acceptance gate."""
    output = []
    for cohort in (DEVELOPMENT_COHORT, TEST_COHORT):
        rows = [row for row in seed_rows if row["cohort"] == cohort]
        require(len(rows) >= 2, f"Insufficient Monte Carlo seeds for {cohort}.")
        for field in MONTE_CARLO_FIELDS:
            values = [float(row[field]) for row in rows]
            average = fsum(values) / len(values)
            deviation = sqrt(fsum((value - average) ** 2 for value in values) / (len(values) - 1))
            output.append({
                "cohort": cohort,
                "metric": field,
                "seedCount": str(len(values)),
                "mean": format_float(average),
                "sampleStandardDeviation": format_float(deviation),
                "standardErrorOfMean": format_float(deviation / sqrt(len(values))),
                "minimum": format_float(min(values)),
                "maximum": format_float(max(values)),
            })
    return output


def write_seed_tables(seed_rows: list[dict[str, str]], summary: list[dict[str, str]]) -> None:
    for path, rows in ((OUT_SEEDS, seed_rows), (OUT_MONTE_CARLO, summary)):
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def write_candidates(rows: list[dict[str, float | int | str]]) -> None:
    fields = [
        "calendarPriorityThreshold",
        "specialRuleThreshold",
        "suspensionThreshold",
        "seedCount",
        "runsPerSeed",
        "simulatedBills",
        "committeeAdvanceRate",
        "floorConsiderationRate",
        "advanceToFloorRate",
        "enactmentRate",
        "specialRuleOnlyRouteShare",
        "suspensionOnlyRouteShare",
        "mixedSpecialRuleAndSuspensionRouteShare",
        "otherFloorRouteShare",
        "restrictiveSpecialRuleShare",
        "closedRuleRate",
        "openRuleRate",
        "calendarCapacityDenialRate",
        *[f"{field}Error" for field in SELECTION_TOLERANCES],
        *[f"{field}StandardizedError" for field in SELECTION_TOLERANCES],
        "selectionLoss",
        "maximumAbsoluteStandardizedError",
        "selected",
    ]
    OUT_CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CANDIDATES.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output: dict[str, str | int] = {}
            for field in fields:
                value = row[field]
                if field in {"seedCount", "runsPerSeed", "simulatedBills"}:
                    output[field] = int(value)
                elif field == "selected":
                    output[field] = str(value)
                else:
                    output[field] = format_float(value)
            writer.writerow(output)


def metric_rows(
    development: dict[str, float | int | str],
    test: dict[str, float | int | str],
    targets: dict[str, dict[str, tuple[int, int | None, float]]],
    gate: dict[str, object],
) -> list[dict[str, str]]:
    definitions = {
        "committeeAdvanceRate": "Committee-advanced H.R. measures divided by introduced H.R. measures.",
        "floorConsiderationRate": "Substantively floor-considered H.R. measures divided by introduced H.R. measures.",
        "advanceToFloorRate": "Floor-considered after committee advancement divided by committee-advanced H.R. measures; simulator ratio is aggregate floor divided by aggregate advancement.",
        "specialRuleOnlyRouteShare": "Special-rule-only route share among floor-considered measures.",
        "suspensionOnlyRouteShare": "Suspension-only route share among floor-considered measures.",
        "mixedSpecialRuleAndSuspensionRouteShare": "Mixed route share among floor-considered measures.",
        "otherFloorRouteShare": "Other route share among floor-considered measures.",
        "restrictiveSpecialRuleShare": "Restrictive modeled special-rule routes divided by all modeled special-rule-only and mixed routes.",
        "routeTotalVariation": "One half of the sum of absolute differences across the four route shares.",
    }
    output: list[dict[str, str]] = []
    for cohort_role, result, cohort_id in (
        ("development", development, DEVELOPMENT_COHORT),
        ("primary_temporal_test", test, TEST_COHORT),
    ):
        for metric in (
            "committeeAdvanceRate",
            "floorConsiderationRate",
            "advanceToFloorRate",
            *ROUTE_FIELDS,
            "restrictiveSpecialRuleShare",
        ):
            numerator, denominator, target = targets[cohort_id][metric]
            simulated = float(result[metric])
            tolerance = ""
            status = "reported"
            if cohort_role == "development" and metric in SELECTION_TOLERANCES:
                tolerance = f"{SELECTION_TOLERANCES[metric]:.12f}"
                status = "selection_metric"
            if cohort_role == "primary_temporal_test" and metric in {
                "committeeAdvanceRate",
                "floorConsiderationRate",
                "restrictiveSpecialRuleShare",
            }:
                tolerance = f"{TEST_TOLERANCES[metric]:.12f}"
                status = "pass" if gate["checks"][metric] else "fail"  # type: ignore[index]
            output.append({
                "cohortRole": cohort_role,
                "metric": metric,
                "targetNumerator": str(numerator),
                "targetDenominator": "" if denominator is None else str(denominator),
                "targetValue": f"{target:.12f}",
                "simulatorValue": f"{simulated:.12f}",
                "error": f"{simulated - target:.12f}",
                "tolerance": tolerance,
                "status": status,
                "definition": definitions[metric],
            })
        route_tv = total_variation(result, targets[cohort_id])
        output.append({
            "cohortRole": cohort_role,
            "metric": "routeTotalVariation",
            "targetNumerator": "",
            "targetDenominator": "",
            "targetValue": "0.000000000000",
            "simulatorValue": f"{route_tv:.12f}",
            "error": f"{route_tv:.12f}",
            "tolerance": (
                f"{TEST_TOLERANCES['routeTotalVariation']:.12f}"
                if cohort_role == "primary_temporal_test"
                else ""
            ),
            "status": (
                ("pass" if gate["checks"]["routeTotalVariation"] else "fail")  # type: ignore[index]
                if cohort_role == "primary_temporal_test"
                else "reported"
            ),
            "definition": definitions["routeTotalVariation"],
        })
    return output


def write_metrics(rows: list[dict[str, str]]) -> None:
    with OUT_METRICS.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    selected: dict[str, float | int | str],
    test: dict[str, float | int | str],
    targets: dict[str, dict[str, tuple[int, int | None, float]]],
    leave_one_out: Counter[tuple[float, float, float]],
    gate: dict[str, object],
    baseline: dict[str, str],
    monte_carlo: list[dict[str, str]],
) -> None:
    selected_key = candidate_key(selected)
    stable_count = leave_one_out[selected_key]
    boundary = (
        selected_key[0] in {min(CALENDAR_THRESHOLDS), max(CALENDAR_THRESHOLDS)}
        or selected_key[1] in {min(SPECIAL_THRESHOLDS), max(SPECIAL_THRESHOLDS)}
        or selected_key[2] in {min(SUSPENSION_THRESHOLDS), max(SUSPENSION_THRESHOLDS)}
    )
    lines = [
        "# House Agenda-Control Calibration and Temporal Test",
        "",
        f"Primary temporal gate: **{str(gate['status']).upper()}**.",
        "",
        "Source-attribution caveat: these are the preserved v1 results. A post-fit audit found one Senate action counted as House suspension evidence (118th-Congress H.R. 4366). [The separate source audit](house-agenda-control-source-audit.md) screens the chamber attribution without refitting; the discrepancy increases and the failure remains. Its history-wide source routes are also not equivalent to the simulator's single-decision score overlap.",
        "",
        "## Locked Design",
        "",
        "- Development source: all 18,771 H.R. measures in the 116th and 117th Congresses",
        "- Primary test source: all 10,564 H.R. measures in the 118th Congress",
        f"- Candidate grid: {EXPECTED_CANDIDATES:,} parameter triples",
        f"- Development simulation: {DEVELOPMENT_SEED_COUNT} seeds, {DEVELOPMENT_RUNS} runs per seed, {EXPECTED_DEVELOPMENT_BILLS_PER_CANDIDATE:,} bills per candidate",
        f"- Test simulation: {TEST_SEED_COUNT} independent seeds, {TEST_RUNS} runs per seed, {EXPECTED_TEST_BILLS:,} bills",
        "- The 118th-Congress route distribution was known before tolerances were locked, so the test is no-refit but not outcome blind",
        "",
        "Protocol chronology is unverified: no separate pre-fit commit exists in the available Git history. The original specification records a pre-fit lock, but it was untracked alongside the fitted results at publication audit. See [Provenance and Numerical Amendment 1](../papers/empirical-validation/house-agenda-control-provenance-amendment.md). The fixed protocol and failed comparison are reproducible; their asserted pre-fit timing is not independently established by this artifact.",
        "",
        "## Selected Development Candidate",
        "",
        f"- Minimum calendar priority: {selected_key[0]:.3f}",
        f"- Special-rule threshold: {selected_key[1]:.3f}",
        f"- Suspension threshold: {selected_key[2]:.3f}",
        f"- Standardized squared selection loss: {float(selected['selectionLoss']):.6f}",
        f"- Maximum absolute standardized fitted error: {float(selected['maximumAbsoluteStandardizedError']):.6f}",
        f"- Leave-one-seed-out stability: {stable_count} / {DEVELOPMENT_SEED_COUNT} panels reselected the full-panel triple",
        f"- Grid-boundary warning: {'yes' if boundary else 'no'}",
        "",
        "| Development metric | Source target | Simulator | Error |",
        "| --- | ---: | ---: | ---: |",
    ]
    labels = {
        "committeeAdvanceRate": "Committee advancement",
        "floorConsiderationRate": "Floor consideration",
        "advanceToFloorRate": "Advance-to-floor ratio",
        "specialRuleOnlyRouteShare": "Special-rule-only route",
        "suspensionOnlyRouteShare": "Suspension-only route",
        "mixedSpecialRuleAndSuspensionRouteShare": "Mixed route",
        "otherFloorRouteShare": "Other route",
        "restrictiveSpecialRuleShare": "Restrictive special-rule share",
    }
    for metric in labels:
        target = targets[DEVELOPMENT_COHORT][metric][2]
        simulated = float(selected[metric])
        lines.append(
            f"| {labels[metric]} | {target:.6f} | {simulated:.6f} | {simulated - target:+.6f} |"
        )
    lines.extend([
        f"| Route total variation | 0.000000 | {total_variation(selected, targets[DEVELOPMENT_COHORT]):.6f} | +{total_variation(selected, targets[DEVELOPMENT_COHORT]):.6f} |",
        "",
        "Committee advancement and the restrictive share are reported development checks, not fitted terms. The advance-to-floor ratio is descriptive because real floor paths can bypass a recorded committee-advance stage while the simulator route layer follows its committee layer.",
        "",
        "## No-Refit 118th-Congress Test",
        "",
        "| Gate | Source target | Simulator | Error or distance | Tolerance | Result |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| Committee advancement | {targets[TEST_COHORT]['committeeAdvanceRate'][2]:.6f} | {float(test['committeeAdvanceRate']):.6f} | {float(gate['committeeAdvanceError']):+.6f} | {TEST_TOLERANCES['committeeAdvanceRate']:.3f} | {'pass' if gate['checks']['committeeAdvanceRate'] else 'fail'} |",  # type: ignore[index]
        f"| Floor consideration | {targets[TEST_COHORT]['floorConsiderationRate'][2]:.6f} | {float(test['floorConsiderationRate']):.6f} | {float(gate['floorConsiderationError']):+.6f} | {TEST_TOLERANCES['floorConsiderationRate']:.3f} | {'pass' if gate['checks']['floorConsiderationRate'] else 'fail'} |",  # type: ignore[index]
        f"| Four-route total variation | 0.000000 | {float(gate['routeTotalVariation']):.6f} | +{float(gate['routeTotalVariation']):.6f} | {TEST_TOLERANCES['routeTotalVariation']:.3f} | {'pass' if gate['checks']['routeTotalVariation'] else 'fail'} |",  # type: ignore[index]
        f"| Restrictive special-rule share | {targets[TEST_COHORT]['restrictiveSpecialRuleShare'][2]:.6f} | {float(test['restrictiveSpecialRuleShare']):.6f} | {float(gate['restrictiveSpecialRuleShareError']):+.6f} | {TEST_TOLERANCES['restrictiveSpecialRuleShare']:.3f} | {'pass' if gate['checks']['restrictiveSpecialRuleShare'] else 'fail'} |",  # type: ignore[index]
        "",
        "The route-composition gate fails by 0.010470 total-variation units. The other three frozen conditions pass. This miss is retained; the candidate grid is not expanded and no route threshold is retuned against the 118th Congress.",
        "",
        "### Test Route Composition",
        "",
        "| Route | 118th source | Simulator | Error |",
        "| --- | ---: | ---: | ---: |",
    ])
    for metric in ROUTE_FIELDS:
        target = targets[TEST_COHORT][metric][2]
        simulated = float(test[metric])
        lines.append(
            f"| {labels[metric]} | {target:.6f} | {simulated:.6f} | {simulated - target:+.6f} |"
        )
    lines.extend([
        "",
        "## Failure Diagnosis",
        "",
        "The selected suspension threshold is the upper boundary of the locked grid, and the development candidate's mixed-route error is 1.712057 standardized tolerance units. In the later cohort, the source special-rule-only share rises to 0.187870, while the unchanged simulator remains at 0.077399 and allocates excess share to mixed and other routes. The current two-score overlap construction therefore does not transport the observed route shift. This is evidence against treating its route mechanism as calibrated Congress behavior.",
        "",
        "## Monte Carlo Variation",
        "",
        "The seed table retains all 20 selected-candidate development seeds and 30 independent test seeds. The summary reports means, sample standard deviations, standard errors of means, minima, and maxima computed from the serialized seed metrics. These describe simulation variability conditional on the fixed model and selected thresholds. Development variability is conditional on selection using the same seeds; it is not independent validation or an estimate of source-data uncertainty.",
        "",
        "The acceptance gate continues to use pooled bill rates and pooled conditional route shares. A mean of per-seed shares or per-seed total-variation distances generally differs from its pooled counterpart and does not replace it. No new acceptance condition is introduced.",
        "",
        "| Metric | Development seed SD | Test seed mean | Test seed SD | Test mean SE |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    summary_index = {(row["cohort"], row["metric"]): row for row in monte_carlo}
    labels.update({
        "enactmentRate": "Enactment (descriptive)",
        "closedRuleRate": "Restrictive rule pressure",
        "openRuleRate": "Open rule pressure",
        "calendarCapacityDenialRate": "Calendar capacity denial",
        "routeTotalVariation": "Route total variation",
    })
    for field in MONTE_CARLO_FIELDS:
        development_row = summary_index[DEVELOPMENT_COHORT, field]
        test_row = summary_index[TEST_COHORT, field]
        lines.append(
            f"| {labels[field]} | {float(development_row['sampleStandardDeviation']):.6f} "
            f"| {float(test_row['mean']):.6f} | {float(test_row['sampleStandardDeviation']):.6f} "
            f"| {float(test_row['standardErrorOfMean']):.6f} |"
        )
    lines.extend([
        "",
        "## Preserved Lifecycle Baseline",
        "",
        f"The earlier lifecycle calibration remains unchanged at calendar threshold {float(baseline['calendarPriorityThreshold']):.2f}, committee advancement {float(baseline['committeeAdvanceRate']):.6f}, floor consideration {float(baseline['floorConsiderationRate']):.6f}, and enactment {float(baseline['enactmentRate']):.6f}. The route study is a separately named calibration and does not overwrite that frozen result.",
        "",
        "## Noncomparable Evidence",
        "",
        "Official calendar-placement coverage, calendar-day stage durations, and amendment action counts are not fitted. The simulator has no official-calendar action record, defensible day scale, or route-specific amendment action log. House passage and enactment are also excluded from this gate because the source panel is H.R.-specific while the simulator continues through a stylized Senate, conference, President, and court.",
        "",
        "## Claim Boundary",
        "",
        CLAIM_BOUNDARY,
        "",
    ])
    OUT_REPORT.write_text("\n".join(lines))


def write_metadata(
    selected: dict[str, float | int | str],
    leave_one_out: Counter[tuple[float, float, float]],
    gate: dict[str, object],
    java_major: int,
) -> None:
    app_cp = Path(os.environ.get("APP_CP", "out/congresssim.jar"))
    jar_path = ROOT / app_cp
    selected_key = candidate_key(selected)
    metadata = {
        "study": "house-agenda-control-calibration-v1",
        "lockStatus": "post-source-audit-prefit-chronology-unverified",
        "runtime": {"javaMajorVersion": java_major},
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                SPEC,
                AMENDMENT,
                SOURCE_AGENDA,
                SOURCE_GRANTS,
                SOURCE_METRICS,
                BASELINE,
                PROBE_SOURCE,
                SIMULATOR_SOURCE,
                Path(__file__),
                jar_path,
            )
        },
        "protocol": {
            "candidateCount": EXPECTED_CANDIDATES,
            "developmentSeedBase": DEVELOPMENT_SEED_BASE,
            "developmentSeedStep": DEVELOPMENT_SEED_STEP,
            "developmentSeedCount": DEVELOPMENT_SEED_COUNT,
            "developmentRunsPerSeed": DEVELOPMENT_RUNS,
            "developmentBillsPerCandidate": EXPECTED_DEVELOPMENT_BILLS_PER_CANDIDATE,
            "testSeedBase": TEST_SEED_BASE,
            "testSeedStep": TEST_SEED_STEP,
            "testSeedCount": TEST_SEED_COUNT,
            "testRunsPerSeed": TEST_RUNS,
            "testBills": EXPECTED_TEST_BILLS,
            "selectionTolerances": SELECTION_TOLERANCES,
            "testTolerances": TEST_TOLERANCES,
        },
        "selected": {
            "calendarPriorityThreshold": selected_key[0],
            "specialRuleThreshold": selected_key[1],
            "suspensionThreshold": selected_key[2],
            "selectionLoss": float(selected["selectionLoss"]),
            "maximumAbsoluteStandardizedError": float(
                selected["maximumAbsoluteStandardizedError"]
            ),
            "leaveOneSeedOutReselections": leave_one_out[selected_key],
            "leaveOneSeedOutPanels": DEVELOPMENT_SEED_COUNT,
        },
        "primaryTemporalGate": gate,
        "outputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (OUT_CANDIDATES, OUT_METRICS, OUT_REPORT, OUT_SEEDS, OUT_MONTE_CARLO)
        },
        "claimBoundary": CLAIM_BOUNDARY,
    }
    OUT_METADATA.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def main() -> int:
    require(len(CALENDAR_THRESHOLDS) * len(SPECIAL_THRESHOLDS) * len(SUSPENSION_THRESHOLDS) == EXPECTED_CANDIDATES, "Locked candidate grid drifted.")
    targets = source_targets()
    baseline = validate_baseline()
    java_bin, java_version = resolve_java_runtime()

    development_probe = run_probe(
        DEVELOPMENT_RUNS,
        DEVELOPMENT_SEEDS,
        CALENDAR_THRESHOLDS,
        SPECIAL_THRESHOLDS,
        SUSPENSION_THRESHOLDS,
        java_bin,
    )
    require(
        len(development_probe) == EXPECTED_CANDIDATES * DEVELOPMENT_SEED_COUNT,
        "Development probe row count drifted.",
    )
    candidates = aggregate_probe_rows(development_probe, targets[DEVELOPMENT_COHORT])
    require(len(candidates) == EXPECTED_CANDIDATES, "Aggregated candidate count drifted.")
    require(
        all(int(row["simulatedBills"]) == EXPECTED_DEVELOPMENT_BILLS_PER_CANDIDATE for row in candidates),
        "Development simulated-bill count drifted.",
    )
    selected = select_candidate(candidates)
    leave_one_out = leave_one_seed_out(development_probe, targets[DEVELOPMENT_COHORT])

    selected_key = candidate_key(selected)
    test_probe = run_probe(
        TEST_RUNS,
        TEST_SEEDS,
        (selected_key[0],),
        (selected_key[1],),
        (selected_key[2],),
        java_bin,
    )
    require(len(test_probe) == TEST_SEED_COUNT, "Test probe row count drifted.")
    test_candidates = aggregate_probe_rows(test_probe, targets[DEVELOPMENT_COHORT])
    require(len(test_candidates) == 1, "Test probe produced more than one candidate.")
    test = test_candidates[0]
    require(int(test["simulatedBills"]) == EXPECTED_TEST_BILLS, "Test simulated-bill count drifted.")
    gate = test_gate(test, targets[TEST_COHORT])

    seed_rows = seed_metric_rows(
        development_probe, selected_key, DEVELOPMENT_COHORT, targets[DEVELOPMENT_COHORT]
    ) + seed_metric_rows(test_probe, selected_key, TEST_COHORT, targets[TEST_COHORT])
    require(len(seed_rows) == DEVELOPMENT_SEED_COUNT + TEST_SEED_COUNT, "Seed output count drifted.")
    monte_carlo = monte_carlo_summary(seed_rows)

    write_candidates(candidates)
    metrics = metric_rows(selected, test, targets, gate)
    write_metrics(metrics)
    write_seed_tables(seed_rows, monte_carlo)
    write_report(selected, test, targets, leave_one_out, gate, baseline, monte_carlo)
    write_metadata(selected, leave_one_out, gate, EXPECTED_JAVA_MAJOR)
    print(f"Wrote {OUT_CANDIDATES.relative_to(ROOT)} ({len(candidates):,} candidates)")
    print(f"Wrote {OUT_METRICS.relative_to(ROOT)} ({len(metrics)} metrics)")
    print(f"Wrote {OUT_REPORT.relative_to(ROOT)}")
    print(f"Wrote {OUT_SEEDS.relative_to(ROOT)} ({len(seed_rows)} seeds)")
    print(f"Wrote {OUT_MONTE_CARLO.relative_to(ROOT)} ({len(monte_carlo)} summaries)")
    print(f"Java runtime: {java_version}")
    print(f"Primary temporal gate: {str(gate['status']).upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
