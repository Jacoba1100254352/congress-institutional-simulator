#!/usr/bin/env python3
"""Run resumable multi-seed replication for the A9 mixed-adversary pilot."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import shlex
import shutil
import statistics
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = ROOT / "out" / "adversarial-replication-a9"
SEED_RESULTS_CSV = ROOT / "reports" / "adversarial-replication-a9-seed-results.csv"
SUMMARY_CSV = ROOT / "reports" / "adversarial-replication-a9-summary.csv"
SUMMARY_MD = ROOT / "reports" / "adversarial-replication-a9-summary.md"
RUN_MANIFEST = ROOT / "reports" / "adversarial-replication-a9-run-manifest.json"
CANONICAL_SUMMARY = ROOT / "reports" / "adversarial-stress-a9-summary.csv"
RUNNER_SOURCE = ROOT / "src" / "main" / "java" / "congresssim" / "institution" / "adversary" / "A9MixedAdversaryPortfolioStressRunner.java"
RUNNER_CLASS = "congresssim.institution.adversary.A9MixedAdversaryPortfolioStressRunner"
CHECKPOINT_SCHEMA = 1
DEFAULT_SEEDS = tuple(20260428 + offset for offset in range(30))
DEFAULT_RUNS = 5
DEFAULT_LEGISLATORS = 101
DEFAULT_BILLS = 60
INFORMATION_LEVELS = ("medium", "high")
BUDGETS = (4, 8, 12)
PORTFOLIOS = {
    "clone-decoy-poison-pill": "A1+A2",
    "astroturf-harm-claims": "A3+A4",
    "flood-camouflage-support-distortion": "A5+A6+A8",
}
PORTFOLIO_ORDER = {key: index for index, key in enumerate(PORTFOLIOS)}
INFORMATION_ORDER = {key: index for index, key in enumerate(INFORMATION_LEVELS)}
INTERVAL_METHOD = "two_sided_student_t_on_base_seed_estimates"
CLAIM_BOUNDARY = (
    "A9 multi-seed synthetic replication only. The fixed base-seed panel is the uncertainty unit; "
    "bills and worlds within a seed are not treated as independent replications. Intervals summarize "
    "Monte Carlo sensitivity under the fixed A9 mechanisms, allocations, resource conversion, interaction "
    "coefficients, review capacity, and recovery assumptions. They are not population intervals, empirical "
    "attack-frequency estimates, general mechanism rankings, or evidence for real-world institutional adoption."
)


@dataclass(frozen=True)
class MetricSpec:
    key: str
    label: str
    lower_bound: float | None = None
    upper_bound: float | None = None


METRICS = (
    MetricSpec("attackSuccessRate", "Strict mixed-only success rate", 0.0, 1.0),
    MetricSpec("mixedFailureRate", "Mixed adverse-failure rate", 0.0, 1.0),
    MetricSpec("anySameBudgetSingleFailureRate", "Any full-budget single failure rate", 0.0, 1.0),
    MetricSpec("mixedDominatesStrongestSingleRate", "Mixed-dominates rate", 0.0, 1.0),
    MetricSpec("meanMixedDegradation", "Mean mixed degradation", 0.0, None),
    MetricSpec("medianMixedDegradation", "Median mixed degradation", 0.0, None),
    MetricSpec("worstMixedDegradation", "Worst mixed degradation", 0.0, None),
    MetricSpec("meanStrongestSingleDegradation", "Mean strongest-single degradation", 0.0, None),
    MetricSpec("meanInteractionDegradation", "Mean interaction degradation"),
    MetricSpec("medianInteractionDegradation", "Median interaction degradation"),
    MetricSpec("worstInteractionDegradation", "Worst interaction degradation"),
    MetricSpec("positiveInteractionRate", "Positive interaction trace rate", 0.0, 1.0),
    MetricSpec("meanSuperadditiveLoss", "Mean superadditive loss"),
    MetricSpec("medianSuperadditiveLoss", "Median superadditive loss"),
    MetricSpec("worstSuperadditiveLoss", "Worst superadditive loss"),
    MetricSpec("superadditiveRate", "Superadditive trace rate", 0.0, 1.0),
    MetricSpec("recoveryCorrectionAttemptRate", "Recovery/correction attempt rate", 0.0, 1.0),
    MetricSpec("recoveryCorrectionFailureRate", "Recovery/correction failure rate", 0.0, 1.0),
    MetricSpec("meanAdministrativeBurdenAdded", "Mean administrative burden added", 0.0, None),
    MetricSpec("worstAdministrativeBurdenAdded", "Worst administrative burden added", 0.0, None),
    MetricSpec("meanQueueOverflowAdded", "Mean queue overflow added", 0.0, None),
    MetricSpec("worstQueueOverflowAdded", "Worst queue overflow added", 0.0, None),
)
METRIC_BY_KEY = {metric.key: metric for metric in METRICS}
EVENT_COUNT_FIELDS = {
    "attackSuccessRate": "attackSuccessCount",
    "mixedFailureRate": "mixedFailureCount",
    "anySameBudgetSingleFailureRate": "anySameBudgetSingleFailureCount",
    "mixedDominatesStrongestSingleRate": "mixedDominatesStrongestSingleCount",
    "positiveInteractionRate": "positiveInteractionCount",
    "superadditiveRate": "superadditiveCount",
    "recoveryCorrectionAttemptRate": "recoveryCorrectionAttemptCount",
    "recoveryCorrectionFailureRate": "recoveryCorrectionFailureCount",
}
REQUIRED_SUMMARY_FIELDS = {
    "adversaryId",
    "portfolioKey",
    "componentAdversaries",
    "budgetValue",
    "informationLevel",
    "runs",
    "legislators",
    "baseBillsPerRun",
    "traceRows",
    "meanAttackerResourceSpend",
    "claimBoundary",
    *(metric.key for metric in METRICS),
    *EVENT_COUNT_FIELDS.values(),
}
AGGREGATE_FIELDS = (
    "portfolioKey",
    "componentAdversaries",
    "informationLevel",
    "budgetValue",
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


def parse_positive_int(name: str, raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


def parse_seeds(raw: str) -> tuple[int, ...]:
    seeds = tuple(int(value.strip()) for value in raw.split(",") if value.strip())
    if len(seeds) < 2:
        raise ValueError("A9 replication requires at least two distinct base seeds.")
    if len(set(seeds)) != len(seeds):
        raise ValueError("A9 replication seed panel contains duplicates.")
    return seeds


def parse_bool(raw: str) -> bool:
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def seed_panel_label(seeds: tuple[int, ...]) -> str:
    ordered = sorted(seeds)
    contiguous = ordered == list(range(ordered[0], ordered[-1] + 1))
    if contiguous:
        return f"{len(ordered)} ({ordered[0]} through {ordered[-1]})"
    return f"{len(ordered)} ({', '.join(str(seed) for seed in ordered)})"


def load_config() -> Config:
    seed_default = ",".join(str(seed) for seed in DEFAULT_SEEDS)
    app_cp = Path(os.environ.get("APP_CP", "out/congresssim.jar"))
    if not app_cp.is_absolute():
        app_cp = ROOT / app_cp
    return Config(
        seeds=parse_seeds(os.environ.get("A9_REPLICATION_SEEDS", seed_default)),
        runs=parse_positive_int("A9_REPLICATION_RUNS", os.environ.get("A9_REPLICATION_RUNS", str(DEFAULT_RUNS))),
        legislators=parse_positive_int(
            "A9_REPLICATION_LEGISLATORS",
            os.environ.get("A9_REPLICATION_LEGISLATORS", str(DEFAULT_LEGISLATORS)),
        ),
        bills=parse_positive_int("A9_REPLICATION_BILLS", os.environ.get("A9_REPLICATION_BILLS", str(DEFAULT_BILLS))),
        workers=parse_positive_int("A9_REPLICATION_WORKERS", os.environ.get("A9_REPLICATION_WORKERS", "2")),
        force=parse_bool(os.environ.get("A9_REPLICATION_FORCE", "0")),
        java=os.environ.get("JAVA", "java"),
        java_props=tuple(shlex.split(os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21"))),
        app_cp=app_cp,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_source_tree() -> str:
    digest = hashlib.sha256()
    source_root = ROOT / "src" / "main" / "java"
    for path in sorted(source_root.rglob("*.java")):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content)
    temporary.replace(path)


def atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_write_csv(path: Path, fieldnames: list[str] | tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def config_key(row: dict[str, str]) -> tuple[str, str, int]:
    return row["portfolioKey"], row["informationLevel"], int(row["budgetValue"])


def config_sort_key(row: dict[str, str] | dict[str, object]) -> tuple[int, int, int]:
    return (
        PORTFOLIO_ORDER[str(row["portfolioKey"])],
        INFORMATION_ORDER[str(row["informationLevel"])],
        int(row["budgetValue"]),
    )


def expected_config_keys() -> set[tuple[str, str, int]]:
    return {
        (portfolio, information, budget)
        for portfolio in PORTFOLIOS
        for information in INFORMATION_LEVELS
        for budget in BUDGETS
    }


def read_seed_summary(path: Path, config: Config) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    missing = REQUIRED_SUMMARY_FIELDS - set(fieldnames)
    if missing:
        raise ValueError(f"{path} is missing A9 summary fields: {sorted(missing)}")
    keys = [config_key(row) for row in rows]
    if len(rows) != 18 or len(set(keys)) != 18 or set(keys) != expected_config_keys():
        raise ValueError(f"{path} does not contain the expected 18 A9 portfolio/information/budget cells.")
    expected_trace_rows = config.runs * config.bills
    for row in rows:
        portfolio, information, budget = config_key(row)
        if row["adversaryId"] != "A9":
            raise ValueError(f"{path} contains a non-A9 row.")
        if row["componentAdversaries"] != PORTFOLIOS[portfolio]:
            raise ValueError(f"{path} has the wrong component set for {portfolio}.")
        if information not in INFORMATION_LEVELS or budget not in BUDGETS:
            raise ValueError(f"{path} contains an unexpected A9 configuration.")
        if int(row["runs"]) != config.runs:
            raise ValueError(f"{path} has a stale runs value.")
        if int(row["legislators"]) != config.legislators:
            raise ValueError(f"{path} has a stale legislator count.")
        if int(row["baseBillsPerRun"]) != config.bills:
            raise ValueError(f"{path} has a stale bills-per-run value.")
        if int(row["traceRows"]) != expected_trace_rows:
            raise ValueError(f"{path} has the wrong evaluated row count.")
        if not math.isclose(float(row["meanAttackerResourceSpend"]), budget, abs_tol=1e-9):
            raise ValueError(f"{path} violates the fixed-budget invariant.")
        for metric in METRICS:
            value = float(row[metric.key])
            if not math.isfinite(value):
                raise ValueError(f"{path} contains a non-finite {metric.key} value.")
        for rate_field, count_field in EVENT_COUNT_FIELDS.items():
            count = int(row[count_field])
            if count < 0 or count > expected_trace_rows:
                raise ValueError(f"{path} contains an invalid {count_field} value.")
            expected_rate = count / expected_trace_rows
            if not math.isclose(float(row[rate_field]), expected_rate, abs_tol=0.00000051):
                raise ValueError(f"{path} has inconsistent {count_field} and {rate_field} values.")
    return fieldnames, sorted(rows, key=config_sort_key)


def checkpoint_expectation(config: Config, seed: int, source_hash: str, script_hash: str) -> dict[str, object]:
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
    }


def valid_checkpoint(
    checkpoint_path: Path,
    summary_path: Path,
    expected: dict[str, object],
    config: Config,
) -> bool:
    if not checkpoint_path.exists() or not summary_path.exists():
        return False
    try:
        checkpoint = json.loads(checkpoint_path.read_text())
        if any(checkpoint.get(key) != value for key, value in expected.items()):
            return False
        if checkpoint.get("summarySha256") != sha256_file(summary_path):
            return False
        read_seed_summary(summary_path, config)
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    return True


def run_seed(
    config: Config,
    seed: int,
    source_hash: str,
    script_hash: str,
) -> tuple[int, list[str], list[dict[str, str]], bool, Path]:
    output_dir = CHECKPOINT_ROOT / str(seed)
    summary_path = output_dir / "adversarial-stress-a9-summary.csv"
    checkpoint_path = output_dir / "checkpoint.json"
    expected = checkpoint_expectation(config, seed, source_hash, script_hash)
    if not config.force and valid_checkpoint(checkpoint_path, summary_path, expected, config):
        fieldnames, rows = read_seed_summary(summary_path, config)
        return seed, fieldnames, rows, True, summary_path

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
        "--summary-only",
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no process output"
        raise RuntimeError(f"A9 replication seed {seed} failed: {detail}")
    fieldnames, rows = read_seed_summary(summary_path, config)
    checkpoint = dict(expected)
    checkpoint["summarySha256"] = sha256_file(summary_path)
    atomic_write_json(checkpoint_path, checkpoint)
    return seed, fieldnames, rows, False, summary_path


def execute_seed_panel(
    config: Config,
    source_hash: str,
    script_hash: str,
) -> tuple[list[str], list[dict[str, str]], int, dict[int, Path]]:
    CHECKPOINT_ROOT.mkdir(parents=True, exist_ok=True)
    completed_rows: dict[int, tuple[list[str], list[dict[str, str]]]] = {}
    summary_paths: dict[int, Path] = {}
    reused = 0
    worker_count = min(config.workers, len(config.seeds))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(run_seed, config, seed, source_hash, script_hash): seed
            for seed in config.seeds
        }
        for future in as_completed(futures):
            seed, fieldnames, rows, was_reused, summary_path = future.result()
            completed_rows[seed] = (fieldnames, rows)
            summary_paths[seed] = summary_path
            reused += int(was_reused)
            print(f"{'Reused' if was_reused else 'Completed'} A9 replication seed {seed}")

    first_fieldnames: list[str] | None = None
    seed_rows: list[dict[str, str]] = []
    for seed in sorted(config.seeds):
        fieldnames, rows = completed_rows[seed]
        if first_fieldnames is None:
            first_fieldnames = fieldnames
        elif fieldnames != first_fieldnames:
            raise ValueError(f"A9 replication seed {seed} has a different summary schema.")
        for row in rows:
            seed_rows.append({"seed": str(seed), **row})
    if first_fieldnames is None:
        raise ValueError("A9 replication produced no seed summaries.")
    return ["seed", *first_fieldnames], seed_rows, reused, summary_paths


def t_critical_95(degrees_of_freedom: int) -> float:
    table = {
        1: 12.706,
        2: 4.303,
        3: 3.182,
        4: 2.776,
        5: 2.571,
        6: 2.447,
        7: 2.365,
        8: 2.306,
        9: 2.262,
        10: 2.228,
        11: 2.201,
        12: 2.179,
        13: 2.160,
        14: 2.145,
        15: 2.131,
        16: 2.120,
        17: 2.110,
        18: 2.101,
        19: 2.093,
        20: 2.086,
        21: 2.080,
        22: 2.074,
        23: 2.069,
        24: 2.064,
        25: 2.060,
        26: 2.056,
        27: 2.052,
        28: 2.048,
        29: 2.045,
        30: 2.042,
    }
    if degrees_of_freedom <= 0:
        return 0.0
    if degrees_of_freedom <= 30:
        return table[degrees_of_freedom]
    if degrees_of_freedom <= 40:
        return 2.021
    if degrees_of_freedom <= 60:
        return 2.000
    if degrees_of_freedom <= 120:
        return 1.980
    return 1.960


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def clamp(value: float, lower: float | None, upper: float | None) -> float:
    if lower is not None:
        value = max(lower, value)
    if upper is not None:
        value = min(upper, value)
    return value


def summarize_values(values: list[float], metric: MetricSpec) -> dict[str, float]:
    if not values:
        raise ValueError("Cannot summarize an empty seed panel.")
    average = statistics.fmean(values)
    sample_std_dev = statistics.stdev(values) if len(values) > 1 else 0.0
    standard_error = sample_std_dev / math.sqrt(len(values))
    margin = t_critical_95(len(values) - 1) * standard_error
    ci_low = clamp(average - margin, metric.lower_bound, metric.upper_bound)
    ci_high = clamp(average + margin, metric.lower_bound, metric.upper_bound)
    tolerance = 1e-12
    if average > tolerance:
        agreement = sum(value > tolerance for value in values) / len(values)
    elif average < -tolerance:
        agreement = sum(value < -tolerance for value in values) / len(values)
    else:
        agreement = sum(abs(value) <= tolerance for value in values) / len(values)
    return {
        "mean": average,
        "sampleStdDev": sample_std_dev,
        "standardError": standard_error,
        "ci95Low": ci_low,
        "ci95High": ci_high,
        "min": min(values),
        "q25": quantile(values, 0.25),
        "median": statistics.median(values),
        "q75": quantile(values, 0.75),
        "max": max(values),
        "positiveSeedShare": sum(value > tolerance for value in values) / len(values),
        "nonzeroSeedShare": sum(abs(value) > tolerance for value in values) / len(values),
        "signAgreementShare": agreement,
    }


def format_number(value: float) -> str:
    return f"{value:.6f}"


def aggregate_seed_rows(seed_rows: list[dict[str, str]], config: Config) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, int], list[dict[str, str]]] = defaultdict(list)
    for row in seed_rows:
        grouped[config_key(row)].append(row)
    if set(grouped) != expected_config_keys():
        raise ValueError("A9 replication aggregation is missing expected cells.")

    aggregate_rows: list[dict[str, object]] = []
    for key in sorted(grouped, key=lambda item: (PORTFOLIO_ORDER[item[0]], INFORMATION_ORDER[item[1]], item[2])):
        rows = sorted(grouped[key], key=lambda row: int(row["seed"]))
        if len(rows) != len(config.seeds) or {int(row["seed"]) for row in rows} != set(config.seeds):
            raise ValueError(f"A9 replication cell {key} does not contain every base seed exactly once.")
        portfolio, information, budget = key
        trace_rows_per_seed = int(rows[0]["traceRows"])
        evaluated_rows = sum(int(row["traceRows"]) for row in rows)
        for metric in METRICS:
            values = [float(row[metric.key]) for row in rows]
            summary = summarize_values(values, metric)
            count_field = EVENT_COUNT_FIELDS.get(metric.key)
            event_count: str | int = "" if count_field is None else sum(int(row[count_field]) for row in rows)
            aggregate_rows.append({
                "portfolioKey": portfolio,
                "componentAdversaries": PORTFOLIOS[portfolio],
                "informationLevel": information,
                "budgetValue": budget,
                "metric": metric.key,
                "metricLabel": metric.label,
                "seedCount": len(rows),
                "runsPerSeed": config.runs,
                "legislators": config.legislators,
                "billsPerRun": config.bills,
                "traceRowsPerSeed": trace_rows_per_seed,
                "evaluatedTraceRows": evaluated_rows,
                "eventCount": event_count,
                **{name: format_number(value) for name, value in summary.items()},
                "intervalMethod": INTERVAL_METHOD,
                "claimBoundary": CLAIM_BOUNDARY,
            })
    return aggregate_rows


def statistic_lookup(aggregate_rows: list[dict[str, object]]) -> dict[tuple[str, str, int, str], dict[str, object]]:
    return {
        (
            str(row["portfolioKey"]),
            str(row["informationLevel"]),
            int(row["budgetValue"]),
            str(row["metric"]),
        ): row
        for row in aggregate_rows
    }


def format_interval(row: dict[str, object]) -> str:
    return f"{float(row['mean']):.3f} [{float(row['ci95Low']):.3f}, {float(row['ci95High']):.3f}]"


def write_markdown(
    aggregate_rows: list[dict[str, object]],
    seed_rows: list[dict[str, str]],
    config: Config,
) -> None:
    lookup = statistic_lookup(aggregate_rows)
    strict_success_total = sum(int(row["attackSuccessCount"]) for row in seed_rows)
    evaluated_rows = sum(int(row["traceRows"]) for row in seed_rows)
    lines = [
        "# A9 Multi-Seed Replication Summary",
        "",
        "Deterministic replication of the fixed-specification A9 mixed-adversary pilot across independent base seeds.",
        "",
        f"- Base seeds: {seed_panel_label(config.seeds)}",
        f"- Runs per seed: {config.runs}",
        f"- Bills per run: {config.bills}",
        f"- Portfolio/information/budget cells: {len(expected_config_keys())}",
        f"- Seed-cell rows: {len(seed_rows)}",
        f"- Evaluated A9 trace rows: {evaluated_rows}",
        f"- Strict mixed-only success rows: {strict_success_total}",
        f"- Interval method: `{INTERVAL_METHOD}`",
        "- Replication traces: not written; compact per-seed summaries are checkpointed under `out/`.",
        "",
        "The interval unit is the base seed. These intervals do not treat bills within a simulated world as independent observations.",
        "",
        "| Portfolio | Components | Information | Budget | Evaluated rows | Strict successes | Seeds with success | Success rate mean [95% CI] | Interaction mean [95% CI] | Superadditive mean [95% CI] | Positive-interaction seeds | Correction failure mean [95% CI] |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | --- |",
    ]
    grouped: dict[tuple[str, str, int], list[dict[str, str]]] = defaultdict(list)
    for row in seed_rows:
        grouped[config_key(row)].append(row)
    for portfolio in PORTFOLIOS:
        for information in INFORMATION_LEVELS:
            for budget in BUDGETS:
                key = (portfolio, information, budget)
                rows = grouped[key]
                success_count = sum(int(row["attackSuccessCount"]) for row in rows)
                seeds_with_success = sum(float(row["attackSuccessRate"]) > 0.0 for row in rows)
                success = lookup[(*key, "attackSuccessRate")]
                interaction = lookup[(*key, "meanInteractionDegradation")]
                superadditive = lookup[(*key, "meanSuperadditiveLoss")]
                correction = lookup[(*key, "recoveryCorrectionFailureRate")]
                lines.append(
                    f"| {portfolio} | {PORTFOLIOS[portfolio]} | {information} | {budget} | "
                    f"{sum(int(row['traceRows']) for row in rows)} | {success_count} | {seeds_with_success}/{len(rows)} | "
                    f"{format_interval(success)} | {format_interval(interaction)} | {format_interval(superadditive)} | "
                    f"{float(interaction['positiveSeedShare']):.3f} | {format_interval(correction)} |"
                )
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Gate status: independent-seed replication is now available for the fixed A9 pilot. The robustness paper remains below manuscript gate because A1-A8 adversarial replication, broader mechanism variants, alternative A9 allocation/resource/interaction specifications, substantive outcome replay, and external validation remain incomplete.",
    ])
    atomic_write_text(SUMMARY_MD, "\n".join(lines) + "\n")


def canonical_seed_status(config: Config, summary_paths: dict[int, Path]) -> str:
    canonical_config = (
        20260428 in config.seeds
        and config.runs == DEFAULT_RUNS
        and config.legislators == DEFAULT_LEGISLATORS
        and config.bills == DEFAULT_BILLS
    )
    if not canonical_config:
        return "not_applicable_noncanonical_parameters"
    if not CANONICAL_SUMMARY.exists():
        raise FileNotFoundError(f"Canonical A9 summary is missing: {CANONICAL_SUMMARY}")
    if sha256_file(summary_paths[20260428]) != sha256_file(CANONICAL_SUMMARY):
        raise ValueError("The A9 replication result for seed 20260428 does not match the canonical A9 summary.")
    return "matched"


def write_manifest(
    config: Config,
    seed_rows: list[dict[str, str]],
    aggregate_rows: list[dict[str, object]],
    source_hash: str,
    script_hash: str,
    canonical_status: str,
) -> None:
    evaluated_rows = sum(int(row["traceRows"]) for row in seed_rows)
    strict_success_rows = sum(int(row["attackSuccessCount"]) for row in seed_rows)
    outputs = []
    for path in (SEED_RESULTS_CSV, SUMMARY_CSV, SUMMARY_MD):
        outputs.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(path),
        })
    manifest: dict[str, object] = {
        "manifestVersion": "adversarial-replication-a9-v1",
        "status": "partial_a9_multiseed_replication",
        "adversaryId": "A9",
        "baseSeeds": list(config.seeds),
        "seedCount": len(config.seeds),
        "runsPerSeed": config.runs,
        "legislators": config.legislators,
        "billsPerRun": config.bills,
        "portfolioCellCount": len(expected_config_keys()),
        "seedResultRows": len(seed_rows),
        "summaryMetricRows": len(aggregate_rows),
        "evaluatedTraceRows": evaluated_rows,
        "strictMixedOnlySuccessRows": strict_success_rows,
        "replicationUnit": "base_seed",
        "intervalMethod": INTERVAL_METHOD,
        "seedPanelSelection": (
            "fixed_contiguous_integer_panel_starting_at_20260428_before_result_inspection"
            if config.seeds == DEFAULT_SEEDS
            else "user_supplied_environment_panel"
        ),
        "javaProperties": list(config.java_props),
        "rawTracePolicy": "not_written_for_replication; canonical single-seed per-bill traces remain under reports",
        "checkpointPolicy": "reuse only when parameters, Java properties, source tree, script, summary hash, and schema match",
        "checkpointRoot": CHECKPOINT_ROOT.relative_to(ROOT).as_posix(),
        "canonicalSeedCrossCheck": canonical_status,
        "sourceInputs": [
            {
                "path": RUNNER_SOURCE.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(RUNNER_SOURCE),
            },
            {
                "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
                "sha256": script_hash,
            },
            {
                "path": "src/main/java/**/*.java",
                "sha256": source_hash,
            },
        ],
        "outputs": outputs,
        "claimBoundary": CLAIM_BOUNDARY,
        "gateStatus": "a9_fixed_specification_multiseed_complete_broader_robustness_gate_open",
    }
    atomic_write_json(RUN_MANIFEST, manifest)


def verify_compiled_application(config: Config) -> None:
    if not config.app_cp.exists():
        raise FileNotFoundError(f"Compiled application is missing: {config.app_cp}. Run `make build` first.")
    newest_source = max(path.stat().st_mtime_ns for path in (ROOT / "src" / "main" / "java").rglob("*.java"))
    if config.app_cp.stat().st_mtime_ns < newest_source:
        raise ValueError(f"Compiled application is older than Java sources: {config.app_cp}. Run `make build` first.")


def main() -> int:
    config = load_config()
    verify_compiled_application(config)
    source_hash = sha256_source_tree()
    script_hash = sha256_file(Path(__file__).resolve())
    seed_fieldnames, seed_rows, reused, summary_paths = execute_seed_panel(config, source_hash, script_hash)
    canonical_status = canonical_seed_status(config, summary_paths)
    aggregate_rows = aggregate_seed_rows(seed_rows, config)
    atomic_write_csv(SEED_RESULTS_CSV, seed_fieldnames, seed_rows)
    atomic_write_csv(SUMMARY_CSV, AGGREGATE_FIELDS, aggregate_rows)
    write_markdown(aggregate_rows, seed_rows, config)
    write_manifest(config, seed_rows, aggregate_rows, source_hash, script_hash, canonical_status)
    print(f"Checkpoint reuse: {reused}/{len(config.seeds)} seeds")
    print(f"Wrote {SEED_RESULTS_CSV}")
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"Wrote {RUN_MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
