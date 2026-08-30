#!/usr/bin/env python3
"""Run resumable multi-seed replication for the A1 through A8 pilots."""

from __future__ import annotations

import csv
import json
import math
import os
import re
import shlex
import shutil
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import adversarial_replication_common as common


ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = ROOT / "out" / "adversarial-replication-a1-a8"
SEED_METRICS_CSV = ROOT / "reports" / "adversarial-replication-a1-a8-seed-metrics.csv"
SUMMARY_CSV = ROOT / "reports" / "adversarial-replication-a1-a8-summary.csv"
SUMMARY_MD = ROOT / "reports" / "adversarial-replication-a1-a8-summary.md"
RUN_MANIFEST = ROOT / "reports" / "adversarial-replication-a1-a8-run-manifest.json"
RUNNER_SOURCE = (
    ROOT
    / "src"
    / "main"
    / "java"
    / "congresssim"
    / "institution"
    / "adversary"
    / "A1A8AdversarialReplicationSeedRunner.java"
)
RUNNER_CLASS = "congresssim.institution.adversary.A1A8AdversarialReplicationSeedRunner"
COMMON_UTILITY = Path(common.__file__).resolve()
CHECKPOINT_SCHEMA = 1
DEFAULT_SEEDS = tuple(20260428 + offset for offset in range(30))
DEFAULT_RUNS = 5
DEFAULT_LEGISLATORS = 101
DEFAULT_BILLS = 60
INTERVAL_METHOD = "two_sided_student_t_on_base_seed_estimates"
CLAIM_BOUNDARY = (
    "A1-A8 multi-seed synthetic replication only. The fixed base-seed panel is the uncertainty unit; "
    "bills and worlds within a seed are not treated as independent replications. Intervals summarize "
    "Monte Carlo sensitivity under the fixed first-wave attack mechanisms, budgets, information levels, "
    "institutional paths, and recovery assumptions. They are not population intervals, empirical attack-"
    "frequency estimates, general mechanism rankings, or evidence for real-world institutional adoption. "
    "Success criteria and evaluated-row units differ by adversary, so the cross-family success total is an "
    "audit count rather than a pooled attack rate."
)


@dataclass(frozen=True)
class AdversarySpec:
    adversary_id: str
    name: str
    summary_filename: str
    canonical_path: Path
    expected_rows: int
    primary_metric: str
    primary_metric_label: str
    trace_multiplier: int = 1


ADVERSARY_SPECS = (
    AdversarySpec(
        "A1",
        "Clone/decoy pressure",
        "adversarial-stress-summary.csv",
        ROOT / "reports" / "adversarial-stress-summary.csv",
        6,
        "meanPublicBenefitLoss",
        "Mean public-benefit loss",
        2,
    ),
    AdversarySpec(
        "A2",
        "Poison-pill sequencing",
        "adversarial-stress-a2-summary.csv",
        ROOT / "reports" / "adversarial-stress-a2-summary.csv",
        6,
        "meanPublicBenefitLoss",
        "Mean public-benefit loss",
    ),
    AdversarySpec(
        "A3",
        "Public-input manipulation",
        "adversarial-stress-a3-summary.csv",
        ROOT / "reports" / "adversarial-stress-a3-summary.csv",
        6,
        "meanPublicPreferenceDistortionAdded",
        "Mean public-preference distortion added",
    ),
    AdversarySpec(
        "A4",
        "Bad-faith harm claims",
        "adversarial-stress-a4-summary.csv",
        ROOT / "reports" / "adversarial-stress-a4-summary.csv",
        3,
        "meanFalsePositiveBurdenAdded",
        "Mean false-positive burden added",
    ),
    AdversarySpec(
        "A5",
        "Proposal flooding",
        "adversarial-stress-a5-summary.csv",
        ROOT / "reports" / "adversarial-stress-a5-summary.csv",
        6,
        "meanPolicyYieldLoss",
        "Mean policy-yield loss",
    ),
    AdversarySpec(
        "A6",
        "Lobbying camouflage",
        "adversarial-stress-a6-summary.csv",
        ROOT / "reports" / "adversarial-stress-a6-summary.csv",
        6,
        "meanObservedScreenRiskDecline",
        "Mean observed-screen-risk decline",
    ),
    AdversarySpec(
        "A7",
        "Administrative overload",
        "adversarial-stress-a7-summary.csv",
        ROOT / "reports" / "adversarial-stress-a7-summary.csv",
        6,
        "meanRiskControlDegradationAdded",
        "Mean risk-control degradation added",
    ),
    AdversarySpec(
        "A8",
        "Public-support distortion",
        "adversarial-stress-a8-summary.csv",
        ROOT / "reports" / "adversarial-stress-a8-summary.csv",
        18,
        "meanResidualSignalDistortion",
        "Mean residual signal distortion",
    ),
)
SPEC_BY_ID = {spec.adversary_id: spec for spec in ADVERSARY_SPECS}
ADVERSARY_ORDER = {spec.adversary_id: index for index, spec in enumerate(ADVERSARY_SPECS)}
INFORMATION_ORDER = {value: index for index, value in enumerate(("low", "medium", "high"))}

REQUIRED_SUMMARY_FIELDS = {
    "adversaryId",
    "attackFamily",
    "caseKey",
    "baselineScenario",
    "attackedScenario",
    "mechanismFamily",
    "budgetUnit",
    "budgetValue",
    "informationLevel",
    "runs",
    "legislators",
    "baseBillsPerRun",
    "traceRows",
    "attackSuccessCount",
    "attackSuccessRate",
    "recoveryStatus",
    "traceArtifact",
    "claimBoundary",
}
SUMMARY_METADATA_FIELDS = REQUIRED_SUMMARY_FIELDS - {"attackSuccessRate"}

SEED_METRIC_FIELDS = (
    "seed",
    "adversaryId",
    "adversaryName",
    "attackFamily",
    "caseKey",
    "baselineScenario",
    "attackedScenario",
    "mechanismFamily",
    "budgetUnit",
    "budgetValue",
    "informationLevel",
    "runs",
    "legislators",
    "billsPerRun",
    "traceRows",
    "metric",
    "metricLabel",
    "value",
    "eventCount",
    "recoveryStatus",
    "claimBoundary",
)

AGGREGATE_FIELDS = (
    "adversaryId",
    "adversaryName",
    "attackFamily",
    "caseKey",
    "baselineScenario",
    "attackedScenario",
    "mechanismFamily",
    "budgetUnit",
    "budgetValue",
    "informationLevel",
    "metric",
    "metricLabel",
    "seedCount",
    "runsPerSeed",
    "legislators",
    "billsPerRun",
    "traceRowsPerSeed",
    "evaluatedTraceRows",
    "eventCount",
    "mean",
    "sampleStdDev",
    "standardError",
    "ci95Low",
    "ci95High",
    "min",
    "q25",
    "median",
    "q75",
    "max",
    "positiveSeedShare",
    "nonzeroSeedShare",
    "signAgreementShare",
    "intervalMethod",
    "recoveryStatus",
    "claimBoundary",
)


@dataclass(frozen=True)
class Config:
    seeds: tuple[int, ...]
    runs: int
    legislators: int
    bills: int
    workers: int
    force: bool
    java: str
    java_props: tuple[str, ...]
    app_cp: Path


@dataclass(frozen=True)
class SummaryTable:
    fieldnames: tuple[str, ...]
    metric_fields: tuple[str, ...]
    rows: tuple[dict[str, str], ...]


parse_positive_int = common.parse_positive_int
parse_seeds = common.parse_seeds
parse_bool = common.parse_bool
seed_panel_label = common.seed_panel_label
summarize_values = common.summarize_values


def load_config() -> Config:
    seed_default = ",".join(str(seed) for seed in DEFAULT_SEEDS)
    app_cp = Path(os.environ.get("APP_CP", "out/congresssim.jar"))
    if not app_cp.is_absolute():
        app_cp = ROOT / app_cp
    return Config(
        seeds=parse_seeds(os.environ.get("A1_A8_REPLICATION_SEEDS", seed_default)),
        runs=parse_positive_int(
            "A1_A8_REPLICATION_RUNS",
            os.environ.get("A1_A8_REPLICATION_RUNS", str(DEFAULT_RUNS)),
        ),
        legislators=parse_positive_int(
            "A1_A8_REPLICATION_LEGISLATORS",
            os.environ.get("A1_A8_REPLICATION_LEGISLATORS", str(DEFAULT_LEGISLATORS)),
        ),
        bills=parse_positive_int(
            "A1_A8_REPLICATION_BILLS",
            os.environ.get("A1_A8_REPLICATION_BILLS", str(DEFAULT_BILLS)),
        ),
        workers=parse_positive_int(
            "A1_A8_REPLICATION_WORKERS",
            os.environ.get("A1_A8_REPLICATION_WORKERS", "2"),
        ),
        force=parse_bool(os.environ.get("A1_A8_REPLICATION_FORCE", "0")),
        java=os.environ.get("JAVA", "java"),
        java_props=tuple(shlex.split(os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21"))),
        app_cp=app_cp,
    )


def metric_label(metric: str, spec: AdversarySpec) -> str:
    if metric == spec.primary_metric:
        return spec.primary_metric_label
    words = re.sub(r"(?<!^)(?=[A-Z])", " ", metric).replace("_", " ")
    return words[:1].upper() + words[1:]


def metric_fields(fieldnames: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    fields = tuple(field for field in fieldnames if field not in SUMMARY_METADATA_FIELDS)
    if "attackSuccessRate" not in fields:
        raise ValueError("A1-A8 summary schema is missing attackSuccessRate as a metric.")
    if len(set(fields)) != len(fields):
        raise ValueError("A1-A8 summary schema contains duplicate metric fields.")
    return fields


def cell_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row["adversaryId"],
        row["attackFamily"],
        row["caseKey"],
        row["baselineScenario"],
        row["attackedScenario"],
        row["mechanismFamily"],
        row["budgetUnit"],
        row["budgetValue"],
        row["informationLevel"],
    )


def cell_sort_key(row: dict[str, str] | dict[str, object]) -> tuple[object, ...]:
    adversary_id = str(row["adversaryId"])
    information = str(row["informationLevel"])
    try:
        budget = float(str(row["budgetValue"]))
    except ValueError:
        budget = math.inf
    return (
        ADVERSARY_ORDER.get(adversary_id, len(ADVERSARY_ORDER)),
        str(row["mechanismFamily"]),
        INFORMATION_ORDER.get(information, len(INFORMATION_ORDER)),
        budget,
        str(row["caseKey"]),
        str(row.get("metric", "")),
    )


def read_seed_summary(path: Path, spec: AdversarySpec, config: Config) -> SummaryTable:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if len(fieldnames) != len(set(fieldnames)):
        raise ValueError(f"{path} contains duplicate summary columns.")
    missing = REQUIRED_SUMMARY_FIELDS - set(fieldnames)
    if missing:
        raise ValueError(f"{path} is missing A1-A8 summary fields: {sorted(missing)}")
    metrics = metric_fields(fieldnames)
    if spec.primary_metric not in metrics:
        raise ValueError(f"{path} is missing primary metric {spec.primary_metric}.")
    keys = [cell_key(row) for row in rows]
    if len(rows) != spec.expected_rows or len(set(keys)) != spec.expected_rows:
        raise ValueError(
            f"{path} does not contain {spec.expected_rows} unique {spec.adversary_id} attack cells."
        )
    expected_trace_rows = config.runs * config.bills * spec.trace_multiplier
    for row in rows:
        if row["adversaryId"] != spec.adversary_id:
            raise ValueError(f"{path} contains a row outside {spec.adversary_id}.")
        if int(row["runs"]) != config.runs:
            raise ValueError(f"{path} has a stale runs value.")
        if int(row["legislators"]) != config.legislators:
            raise ValueError(f"{path} has a stale legislator count.")
        if int(row["baseBillsPerRun"]) != config.bills:
            raise ValueError(f"{path} has a stale bills-per-run value.")
        if int(row["traceRows"]) != expected_trace_rows:
            raise ValueError(f"{path} has the wrong evaluated row count.")
        count = int(row["attackSuccessCount"])
        if count < 0 or count > expected_trace_rows:
            raise ValueError(f"{path} contains an invalid attackSuccessCount value.")
        expected_rate = count / expected_trace_rows
        if not math.isclose(float(row["attackSuccessRate"]), expected_rate, abs_tol=0.00000051):
            raise ValueError(f"{path} has inconsistent attackSuccessCount and attackSuccessRate values.")
        for metric in metrics:
            value = float(row[metric])
            if not math.isfinite(value):
                raise ValueError(f"{path} contains a non-finite {metric} value.")
        if not row["claimBoundary"]:
            raise ValueError(f"{path} contains an empty claim boundary.")
    return SummaryTable(
        tuple(fieldnames),
        metrics,
        tuple(sorted(rows, key=cell_sort_key)),
    )


def read_seed_output(
    output_dir: Path,
    config: Config,
    specs: tuple[AdversarySpec, ...] = ADVERSARY_SPECS,
) -> dict[str, SummaryTable]:
    return {
        spec.adversary_id: read_seed_summary(output_dir / spec.summary_filename, spec, config)
        for spec in specs
    }


def checkpoint_expectation(
    config: Config,
    seed: int,
    source_hash: str,
    script_hash: str,
    common_hash: str,
) -> dict[str, object]:
    return {
        "schemaVersion": CHECKPOINT_SCHEMA,
        "seed": seed,
        "runs": config.runs,
        "legislators": config.legislators,
        "bills": config.bills,
        "runnerClass": RUNNER_CLASS,
        "javaProperties": list(config.java_props),
        "mainSourceSha256": source_hash,
        "replicationScriptSha256": script_hash,
        "commonUtilitySha256": common_hash,
    }


def valid_checkpoint(
    output_dir: Path,
    expected: dict[str, object],
    config: Config,
    specs: tuple[AdversarySpec, ...] = ADVERSARY_SPECS,
) -> bool:
    checkpoint_path = output_dir / "checkpoint.json"
    if not checkpoint_path.exists():
        return False
    expected_filenames = {spec.summary_filename for spec in specs}
    try:
        actual_entries = {path.name for path in output_dir.iterdir()}
        if actual_entries != expected_filenames | {"checkpoint.json"}:
            return False
        if any(path.is_dir() for path in output_dir.iterdir()):
            return False
        checkpoint = json.loads(checkpoint_path.read_text())
        if any(checkpoint.get(key) != value for key, value in expected.items()):
            return False
        recorded_hashes = checkpoint.get("summarySha256ByFile")
        if not isinstance(recorded_hashes, dict) or set(recorded_hashes) != expected_filenames:
            return False
        for filename in expected_filenames:
            if recorded_hashes[filename] != common.sha256_file(output_dir / filename):
                return False
        read_seed_output(output_dir, config, specs)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return False
    return True


def run_seed(
    config: Config,
    seed: int,
    source_hash: str,
    script_hash: str,
    common_hash: str,
) -> tuple[int, dict[str, SummaryTable], bool, dict[str, Path]]:
    output_dir = CHECKPOINT_ROOT / str(seed)
    expected = checkpoint_expectation(config, seed, source_hash, script_hash, common_hash)
    if not config.force and valid_checkpoint(output_dir, expected, config):
        tables = read_seed_output(output_dir, config)
        paths = {
            spec.adversary_id: output_dir / spec.summary_filename
            for spec in ADVERSARY_SPECS
        }
        return seed, tables, True, paths

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        config.java,
        *config.java_props,
        "-cp",
        str(config.app_cp),
        RUNNER_CLASS,
        str(output_dir),
        str(config.runs),
        str(config.legislators),
        str(config.bills),
        str(seed),
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no process output"
        raise RuntimeError(f"A1-A8 replication seed {seed} failed: {detail}")
    expected_filenames = {spec.summary_filename for spec in ADVERSARY_SPECS}
    actual_entries = {path.name for path in output_dir.iterdir()}
    if actual_entries != expected_filenames:
        raise ValueError(
            f"A1-A8 replication seed {seed} wrote unexpected artifacts: {sorted(actual_entries)}"
        )
    tables = read_seed_output(output_dir, config)
    checkpoint = dict(expected)
    checkpoint["summarySha256ByFile"] = {
        filename: common.sha256_file(output_dir / filename)
        for filename in sorted(expected_filenames)
    }
    common.atomic_write_json(output_dir / "checkpoint.json", checkpoint)
    paths = {
        spec.adversary_id: output_dir / spec.summary_filename
        for spec in ADVERSARY_SPECS
    }
    return seed, tables, False, paths


def validate_panel_tables(
    tables_by_seed: dict[int, dict[str, SummaryTable]],
    specs: tuple[AdversarySpec, ...] = ADVERSARY_SPECS,
) -> None:
    if not tables_by_seed:
        raise ValueError("A1-A8 replication produced no seed summaries.")
    first_seed = min(tables_by_seed)
    reference = tables_by_seed[first_seed]
    for seed, tables in sorted(tables_by_seed.items()):
        if set(tables) != {spec.adversary_id for spec in specs}:
            raise ValueError(f"A1-A8 replication seed {seed} has an incomplete adversary set.")
        for spec in specs:
            expected_table = reference[spec.adversary_id]
            table = tables[spec.adversary_id]
            if table.fieldnames != expected_table.fieldnames:
                raise ValueError(f"{spec.adversary_id} seed {seed} has a different summary schema.")
            if table.metric_fields != expected_table.metric_fields:
                raise ValueError(f"{spec.adversary_id} seed {seed} has a different metric set.")
            if {cell_key(row) for row in table.rows} != {
                cell_key(row) for row in expected_table.rows
            }:
                raise ValueError(f"{spec.adversary_id} seed {seed} has a different attack-cell set.")


def execute_seed_panel(
    config: Config,
    source_hash: str,
    script_hash: str,
    common_hash: str,
) -> tuple[dict[int, dict[str, SummaryTable]], int, dict[int, dict[str, Path]]]:
    CHECKPOINT_ROOT.mkdir(parents=True, exist_ok=True)
    tables_by_seed: dict[int, dict[str, SummaryTable]] = {}
    paths_by_seed: dict[int, dict[str, Path]] = {}
    reused = 0
    worker_count = min(config.workers, len(config.seeds))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(run_seed, config, seed, source_hash, script_hash, common_hash): seed
            for seed in config.seeds
        }
        for future in as_completed(futures):
            seed, tables, was_reused, paths = future.result()
            tables_by_seed[seed] = tables
            paths_by_seed[seed] = paths
            reused += int(was_reused)
            print(f"{'Reused' if was_reused else 'Completed'} A1-A8 replication seed {seed}")
    validate_panel_tables(tables_by_seed)
    return tables_by_seed, reused, paths_by_seed


def seed_metric_rows(
    tables_by_seed: dict[int, dict[str, SummaryTable]],
    config: Config,
    specs: tuple[AdversarySpec, ...] = ADVERSARY_SPECS,
) -> list[dict[str, object]]:
    validate_panel_tables(tables_by_seed, specs)
    rows: list[dict[str, object]] = []
    for seed in sorted(config.seeds):
        if seed not in tables_by_seed:
            raise ValueError(f"A1-A8 replication is missing seed {seed}.")
        for spec in specs:
            table = tables_by_seed[seed][spec.adversary_id]
            for summary_row in table.rows:
                for metric in table.metric_fields:
                    rows.append({
                        "seed": seed,
                        "adversaryId": spec.adversary_id,
                        "adversaryName": spec.name,
                        "attackFamily": summary_row["attackFamily"],
                        "caseKey": summary_row["caseKey"],
                        "baselineScenario": summary_row["baselineScenario"],
                        "attackedScenario": summary_row["attackedScenario"],
                        "mechanismFamily": summary_row["mechanismFamily"],
                        "budgetUnit": summary_row["budgetUnit"],
                        "budgetValue": summary_row["budgetValue"],
                        "informationLevel": summary_row["informationLevel"],
                        "runs": config.runs,
                        "legislators": config.legislators,
                        "billsPerRun": config.bills,
                        "traceRows": int(summary_row["traceRows"]),
                        "metric": metric,
                        "metricLabel": metric_label(metric, spec),
                        "value": summary_row[metric],
                        "eventCount": (
                            int(summary_row["attackSuccessCount"])
                            if metric == "attackSuccessRate"
                            else ""
                        ),
                        "recoveryStatus": summary_row["recoveryStatus"],
                        "claimBoundary": summary_row["claimBoundary"],
                    })
    return rows


def metric_bounds(metric: str) -> tuple[float | None, float | None]:
    if metric.endswith("Rate") or metric.endswith("Share"):
        return 0.0, 1.0
    return None, None


def aggregate_seed_metrics(
    seed_rows: list[dict[str, object]],
    config: Config,
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for row in seed_rows:
        key = (*cell_key({name: str(value) for name, value in row.items()}), str(row["metric"]))
        grouped[key].append(row)
    if not grouped:
        raise ValueError("A1-A8 replication aggregation received no seed metrics.")

    aggregate_rows: list[dict[str, object]] = []
    expected_seed_set = set(config.seeds)
    stable_fields = (
        "adversaryName",
        "metricLabel",
        "runs",
        "legislators",
        "billsPerRun",
        "traceRows",
        "recoveryStatus",
        "claimBoundary",
    )
    for key, rows in grouped.items():
        rows = sorted(rows, key=lambda row: int(row["seed"]))
        seeds = [int(row["seed"]) for row in rows]
        if len(rows) != len(config.seeds) or set(seeds) != expected_seed_set:
            raise ValueError(f"A1-A8 replication cell/metric {key} does not contain every seed once.")
        if len(seeds) != len(set(seeds)):
            raise ValueError(f"A1-A8 replication cell/metric {key} contains duplicate seeds.")
        first = rows[0]
        for row in rows[1:]:
            for field in stable_fields:
                if row[field] != first[field]:
                    raise ValueError(f"A1-A8 replication cell/metric {key} varies in {field} across seeds.")
        values = [float(row["value"]) for row in rows]
        lower_bound, upper_bound = metric_bounds(str(first["metric"]))
        summary = summarize_values(values, lower_bound, upper_bound)
        event_count: str | int = ""
        if first["metric"] == "attackSuccessRate":
            if any(row["eventCount"] == "" for row in rows):
                raise ValueError(f"A1-A8 replication cell {key} is missing exact event counts.")
            event_count = sum(int(row["eventCount"]) for row in rows)
        aggregate_rows.append({
            "adversaryId": first["adversaryId"],
            "adversaryName": first["adversaryName"],
            "attackFamily": first["attackFamily"],
            "caseKey": first["caseKey"],
            "baselineScenario": first["baselineScenario"],
            "attackedScenario": first["attackedScenario"],
            "mechanismFamily": first["mechanismFamily"],
            "budgetUnit": first["budgetUnit"],
            "budgetValue": first["budgetValue"],
            "informationLevel": first["informationLevel"],
            "metric": first["metric"],
            "metricLabel": first["metricLabel"],
            "seedCount": len(rows),
            "runsPerSeed": config.runs,
            "legislators": config.legislators,
            "billsPerRun": config.bills,
            "traceRowsPerSeed": int(first["traceRows"]),
            "evaluatedTraceRows": sum(int(row["traceRows"]) for row in rows),
            "eventCount": event_count,
            **{name: common.format_number(value) for name, value in summary.items()},
            "intervalMethod": INTERVAL_METHOD,
            "recoveryStatus": first["recoveryStatus"],
            "claimBoundary": CLAIM_BOUNDARY,
        })
    return sorted(aggregate_rows, key=cell_sort_key)


def aggregate_lookup(
    aggregate_rows: list[dict[str, object]],
) -> dict[tuple[str, ...], dict[str, object]]:
    return {
        (*cell_key({name: str(value) for name, value in row.items()}), str(row["metric"])): row
        for row in aggregate_rows
    }


def format_interval(row: dict[str, object]) -> str:
    return f"{float(row['mean']):.3f} [{float(row['ci95Low']):.3f}, {float(row['ci95High']):.3f}]"


def escape_markdown(value: object) -> str:
    return str(value).replace("|", "\\|")


def attack_seed_rows(seed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in seed_rows if row["metric"] == "attackSuccessRate"]


def write_markdown(
    aggregate_rows: list[dict[str, object]],
    seed_rows: list[dict[str, object]],
    config: Config,
) -> None:
    lookup = aggregate_lookup(aggregate_rows)
    attack_rows = attack_seed_rows(seed_rows)
    grouped: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for row in attack_rows:
        grouped[cell_key({name: str(value) for name, value in row.items()})].append(row)
    evaluated_rows = sum(int(row["traceRows"]) for row in attack_rows)
    exact_successes = sum(int(row["eventCount"]) for row in attack_rows)
    lines = [
        "# A1-A8 Multi-Seed Replication Summary",
        "",
        "Deterministic replication of the fixed first-wave A1 through A8 adversarial pilots across independent base seeds.",
        "",
        f"- Adversaries: {len(ADVERSARY_SPECS)} (A1 through A8)",
        f"- Base seeds: {seed_panel_label(config.seeds)}",
        f"- Runs per seed: {config.runs}",
        f"- Bills per run: {config.bills}",
        f"- Attack cells: {len(grouped)}",
        f"- Seed-cell summaries: {len(attack_rows)}",
        f"- Seed-metric rows: {len(seed_rows)}",
        f"- Evaluated attack rows: {evaluated_rows}",
        f"- Exact attack-success rows: {exact_successes}",
        f"- Interval method: `{INTERVAL_METHOD}`",
        "- Replication traces: not written; compact per-seed summaries are checkpointed under `out/`.",
        "",
        "The interval unit is the base seed. These intervals do not treat bills within a simulated world as independent observations.",
        "Success criteria and evaluated-row units differ by adversary. The cross-family exact-success total is an audit count, not a pooled attack rate.",
        "",
        "| Adversary | Mechanism | Information | Budget | Evaluated rows | Exact successes | Seeds with success | Success rate mean [95% CI] | Primary metric | Primary mean [95% CI] |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for key, rows in sorted(grouped.items(), key=lambda item: cell_sort_key(item[1][0])):
        rows = sorted(rows, key=lambda row: int(row["seed"]))
        spec = SPEC_BY_ID[str(rows[0]["adversaryId"])]
        success = lookup[(*key, "attackSuccessRate")]
        primary = lookup[(*key, spec.primary_metric)]
        lines.append(
            f"| {spec.adversary_id} {escape_markdown(spec.name)} | "
            f"{escape_markdown(rows[0]['mechanismFamily'])} | "
            f"{escape_markdown(rows[0]['informationLevel'])} | "
            f"{escape_markdown(rows[0]['budgetValue'])} | "
            f"{sum(int(row['traceRows']) for row in rows)} | "
            f"{sum(int(row['eventCount']) for row in rows)} | "
            f"{sum(int(row['eventCount']) > 0 for row in rows)}/{len(rows)} | "
            f"{format_interval(success)} | {escape_markdown(spec.primary_metric_label)} | "
            f"{format_interval(primary)} |"
        )
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Gate status: fixed-specification base-seed replication is available for all first-wave A1-A8 pilots. The robustness paper remains below manuscript gate because broader mechanism variants, substantive recovery and correction, alternative A9 specifications, and external validation remain incomplete.",
    ])
    common.atomic_write_text(SUMMARY_MD, "\n".join(lines) + "\n")


def canonical_seed_crosscheck(
    config: Config,
    paths_by_seed: dict[int, dict[str, Path]],
    specs: tuple[AdversarySpec, ...] = ADVERSARY_SPECS,
) -> dict[str, object]:
    canonical_config = (
        20260428 in config.seeds
        and config.runs == DEFAULT_RUNS
        and config.legislators == DEFAULT_LEGISLATORS
        and config.bills == DEFAULT_BILLS
    )
    if not canonical_config:
        return {"status": "not_applicable_noncanonical_parameters"}
    entries = []
    for spec in specs:
        if not spec.canonical_path.exists():
            raise FileNotFoundError(f"Canonical {spec.adversary_id} summary is missing: {spec.canonical_path}")
        replication_path = paths_by_seed[20260428][spec.adversary_id]
        replication_hash = common.sha256_file(replication_path)
        canonical_hash = common.sha256_file(spec.canonical_path)
        if replication_hash != canonical_hash:
            raise ValueError(
                f"The {spec.adversary_id} replication result for seed 20260428 does not match its canonical summary."
            )
        entries.append({
            "adversaryId": spec.adversary_id,
            "canonicalPath": spec.canonical_path.relative_to(ROOT).as_posix(),
            "sha256": canonical_hash,
            "status": "matched",
        })
    return {"status": "all_matched", "seed": 20260428, "adversaries": entries}


def write_manifest(
    config: Config,
    seed_rows: list[dict[str, object]],
    aggregate_rows: list[dict[str, object]],
    source_hash: str,
    script_hash: str,
    common_hash: str,
    canonical_status: dict[str, object],
) -> None:
    attack_rows = attack_seed_rows(seed_rows)
    cell_count = len({cell_key({name: str(value) for name, value in row.items()}) for row in attack_rows})
    evaluated_rows = sum(int(row["traceRows"]) for row in attack_rows)
    exact_success_rows = sum(int(row["eventCount"]) for row in attack_rows)
    outputs = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": common.sha256_file(path),
        }
        for path in (SEED_METRICS_CSV, SUMMARY_CSV, SUMMARY_MD)
    ]
    adversaries = []
    for spec in ADVERSARY_SPECS:
        spec_rows = [row for row in attack_rows if row["adversaryId"] == spec.adversary_id]
        adversaries.append({
            "adversaryId": spec.adversary_id,
            "name": spec.name,
            "attackCellCount": len({cell_key({name: str(value) for name, value in row.items()}) for row in spec_rows}),
            "evaluatedTraceRows": sum(int(row["traceRows"]) for row in spec_rows),
            "attackSuccessRows": sum(int(row["eventCount"]) for row in spec_rows),
            "primaryMetric": spec.primary_metric,
        })
    manifest: dict[str, object] = {
        "manifestVersion": "adversarial-replication-a1-a8-v1",
        "status": "partial_a1_a8_multiseed_replication",
        "adversaryIds": [spec.adversary_id for spec in ADVERSARY_SPECS],
        "adversaries": adversaries,
        "baseSeeds": list(config.seeds),
        "seedCount": len(config.seeds),
        "runsPerSeed": config.runs,
        "legislators": config.legislators,
        "billsPerRun": config.bills,
        "attackCellCount": cell_count,
        "seedCellRows": len(attack_rows),
        "seedMetricRows": len(seed_rows),
        "summaryMetricRows": len(aggregate_rows),
        "evaluatedTraceRows": evaluated_rows,
        "attackSuccessRows": exact_success_rows,
        "attackSuccessAggregationBoundary": "cross_family_sum_for_audit_only_not_a_pooled_rate",
        "replicationUnit": "base_seed",
        "intervalMethod": INTERVAL_METHOD,
        "seedPanelSelection": (
            "fixed_contiguous_integer_panel_starting_at_20260428_before_result_inspection"
            if config.seeds == DEFAULT_SEEDS
            else "user_supplied_environment_panel"
        ),
        "javaProperties": list(config.java_props),
        "rawTracePolicy": "not_written_for_replication; canonical single-seed per-bill traces remain under reports",
        "checkpointPolicy": "reuse only when parameters, Java properties, Java source tree, replication script, common utility, all summary hashes, and all schemas match",
        "checkpointRoot": CHECKPOINT_ROOT.relative_to(ROOT).as_posix(),
        "canonicalSeedCrossCheck": canonical_status,
        "sourceInputs": [
            {
                "path": RUNNER_SOURCE.relative_to(ROOT).as_posix(),
                "sha256": common.sha256_file(RUNNER_SOURCE),
            },
            {
                "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
                "sha256": script_hash,
            },
            {
                "path": COMMON_UTILITY.relative_to(ROOT).as_posix(),
                "sha256": common_hash,
            },
            {
                "path": "src/main/java/**/*.java",
                "sha256": source_hash,
            },
        ],
        "outputs": outputs,
        "claimBoundary": CLAIM_BOUNDARY,
        "gateStatus": "a1_a8_fixed_specification_multiseed_complete_broader_robustness_gate_open",
    }
    common.atomic_write_json(RUN_MANIFEST, manifest)


def verify_compiled_application(config: Config) -> None:
    if not config.app_cp.exists():
        raise FileNotFoundError(f"Compiled application is missing: {config.app_cp}. Run `make build` first.")
    newest_source = max(path.stat().st_mtime_ns for path in (ROOT / "src" / "main" / "java").rglob("*.java"))
    if config.app_cp.stat().st_mtime_ns < newest_source:
        raise ValueError(f"Compiled application is older than Java sources: {config.app_cp}. Run `make build` first.")


def main() -> int:
    config = load_config()
    verify_compiled_application(config)
    source_hash = common.sha256_source_tree(ROOT)
    script_hash = common.sha256_file(Path(__file__).resolve())
    common_hash = common.sha256_file(COMMON_UTILITY)
    tables_by_seed, reused, paths_by_seed = execute_seed_panel(
        config,
        source_hash,
        script_hash,
        common_hash,
    )
    canonical_status = canonical_seed_crosscheck(config, paths_by_seed)
    seed_rows = seed_metric_rows(tables_by_seed, config)
    aggregate_rows = aggregate_seed_metrics(seed_rows, config)
    common.atomic_write_csv(SEED_METRICS_CSV, SEED_METRIC_FIELDS, seed_rows)
    common.atomic_write_csv(SUMMARY_CSV, AGGREGATE_FIELDS, aggregate_rows)
    write_markdown(aggregate_rows, seed_rows, config)
    write_manifest(
        config,
        seed_rows,
        aggregate_rows,
        source_hash,
        script_hash,
        common_hash,
        canonical_status,
    )
    print(f"Checkpoint reuse: {reused}/{len(config.seeds)} seeds")
    print(f"Wrote {SEED_METRICS_CSV}")
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"Wrote {RUN_MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
