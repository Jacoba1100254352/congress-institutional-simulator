#!/usr/bin/env python3
"""Shared deterministic utilities for adversarial seed-replication reports."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from pathlib import Path


def parse_positive_int(name: str, raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


def parse_seeds(raw: str) -> tuple[int, ...]:
    seeds = tuple(int(value.strip()) for value in raw.split(",") if value.strip())
    if len(seeds) < 2:
        raise ValueError("Adversarial replication requires at least two distinct base seeds.")
    if len(set(seeds)) != len(seeds):
        raise ValueError("Adversarial replication seed panel contains duplicates.")
    return seeds


def parse_bool(raw: str) -> bool:
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def seed_panel_label(seeds: tuple[int, ...]) -> str:
    ordered = sorted(seeds)
    contiguous = ordered == list(range(ordered[0], ordered[-1] + 1))
    if contiguous:
        return f"{len(ordered)} ({ordered[0]} through {ordered[-1]})"
    return f"{len(ordered)} ({', '.join(str(seed) for seed in ordered)})"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_source_tree(root: Path) -> str:
    digest = hashlib.sha256()
    source_root = root / "src" / "main" / "java"
    for path in sorted(source_root.rglob("*.java")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
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


def atomic_write_csv(
    path: Path,
    fieldnames: list[str] | tuple[str, ...],
    rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


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


def summarize_values(
    values: list[float],
    lower_bound: float | None = None,
    upper_bound: float | None = None,
) -> dict[str, float]:
    if not values:
        raise ValueError("Cannot summarize an empty seed panel.")
    average = statistics.fmean(values)
    sample_std_dev = statistics.stdev(values) if len(values) > 1 else 0.0
    standard_error = sample_std_dev / math.sqrt(len(values))
    margin = t_critical_95(len(values) - 1) * standard_error
    ci_low = clamp(average - margin, lower_bound, upper_bound)
    ci_high = clamp(average + margin, lower_bound, upper_bound)
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
