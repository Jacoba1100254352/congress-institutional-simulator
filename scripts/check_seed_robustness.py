#!/usr/bin/env python3
"""Validate the generated seed-robustness regression report."""

from __future__ import annotations

import csv
import math
import os
import sys
from collections import defaultdict
from pathlib import Path


REPORT_CSV = Path("reports/seed-robustness-summary.csv")
METRIC_BOUNDS = {
    "directionalScore": (0.0, 1.0),
    "productivity": (0.0, 1.0),
    "compromise": (0.0, 1.0),
    "weakPublicMandatePassage": (0.0, 1.0),
    "administrativeCost": (0.0, 1.0),
    "welfare": (-1.0, 1.0),
    "riskControl": (0.0, 1.0),
}
PAPER_SCENARIOS = {
    "current-system",
    "simple-majority",
    "supermajority-60",
    "bicameral-majority",
    "presidential-veto",
    "leadership-cartel-majority",
    "committee-regular-order",
    "cloture-conference-review",
    "parliamentary-coalition-confidence",
    "citizen-initiative-referendum",
    "simple-majority-alternatives-pairwise",
    "citizen-assembly-threshold",
    "public-interest-majority",
    "agenda-lottery-majority",
    "quadratic-attention-majority",
    "proposal-bond-majority",
    "harm-weighted-majority",
    "compensation-majority",
    "package-bargaining-majority",
    "multidimensional-package-majority",
    "law-registry-majority",
    "public-objection-majority",
    "anti-capture-majority-bundle",
    "risk-routed-majority",
    "portfolio-hybrid-legislature",
    "norm-erosion-majority",
    "default-pass",
    "default-pass-challenge",
    "default-pass-multiround-mediation-challenge",
}


def main() -> int:
    minimum_seed_count = int(os.environ.get("SEED_ROBUSTNESS_MIN_SEEDS", "5"))
    if not REPORT_CSV.exists():
        print(f"{REPORT_CSV} is missing. Run make seed-robustness first.", file=sys.stderr)
        return 1

    seen: dict[str, set[str]] = defaultdict(set)
    values: dict[tuple[str, str], float] = {}
    failures: list[str] = []
    with REPORT_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            scenario = row["scenarioKey"]
            metric = row["metric"]
            seen[scenario].add(metric)
            seed_count = int(row["seedCount"])
            mean = float(row["mean"])
            min_value = float(row["min"])
            max_value = float(row["max"])
            range_value = float(row["range"])
            values[(scenario, metric)] = mean

            if seed_count < minimum_seed_count:
                failures.append(f"{scenario}/{metric}: seedCount {seed_count} < {minimum_seed_count}")
            if not all(math.isfinite(value) for value in (mean, min_value, max_value, range_value)):
                failures.append(f"{scenario}/{metric}: non-finite value")
                continue
            if min_value > mean or mean > max_value:
                failures.append(f"{scenario}/{metric}: mean outside min/max")
            if abs((max_value - min_value) - range_value) > 0.000002:
                failures.append(f"{scenario}/{metric}: range does not equal max-min")
            if metric in METRIC_BOUNDS:
                lower, upper = METRIC_BOUNDS[metric]
                if mean < lower - 0.000001 or mean > upper + 0.000001:
                    failures.append(f"{scenario}/{metric}: mean {mean:.4f} outside [{lower}, {upper}]")

    missing_scenarios = sorted(PAPER_SCENARIOS - set(seen))
    if missing_scenarios:
        failures.append("missing paper scenarios: " + ", ".join(missing_scenarios))
    for scenario in sorted(PAPER_SCENARIOS & set(seen)):
        missing_metrics = sorted(set(METRIC_BOUNDS) - seen[scenario])
        if missing_metrics:
            failures.append(f"{scenario}: missing metrics {', '.join(missing_metrics)}")

    current_productivity = values.get(("current-system", "productivity"))
    default_productivity = values.get(("default-pass", "productivity"))
    if current_productivity is not None and default_productivity is not None:
        if current_productivity >= default_productivity:
            failures.append("current-system productivity should remain below open default-pass throughput")

    if failures:
        print("Seed robustness check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("Seed robustness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
