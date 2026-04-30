#!/usr/bin/env python3
"""Run a deterministic multi-seed robustness sweep for all paper scenarios."""

from __future__ import annotations

import csv
import os
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "out" / "seed-robustness"
REPORT_CSV = ROOT / "reports" / "seed-robustness-summary.csv"
REPORT_MD = ROOT / "reports" / "seed-robustness-summary.md"
DEFAULT_SEEDS = [20260428, 20260429, 20260430, 20260501, 20260502]
SEEDS = [
    int(seed.strip())
    for seed in os.environ.get("SEED_ROBUSTNESS_SEEDS", ",".join(str(seed) for seed in DEFAULT_SEEDS)).split(",")
    if seed.strip()
]
RUNS = int(os.environ.get("SEED_ROBUSTNESS_RUNS", "24"))
SCENARIOS = [
    ("current-system", "Stylized U.S.-like benchmark"),
    ("simple-majority", "Unicameral simple majority"),
    ("supermajority-60", "Unicameral 60 percent passage"),
    ("bicameral-majority", "Bicameral simple majority"),
    ("presidential-veto", "Bicameral majority + presidential veto"),
    ("leadership-cartel-majority", "Leadership agenda cartel + majority"),
    ("committee-regular-order", "Committee-first regular order"),
    ("cloture-conference-review", "Cloture, conference, and judicial review"),
    ("parliamentary-coalition-confidence", "Parliamentary coalition confidence"),
    ("citizen-initiative-referendum", "Citizen initiative and referendum"),
    ("simple-majority-alternatives-pairwise", "Majority pairwise policy tournament"),
    ("citizen-assembly-threshold", "Citizen assembly threshold gate"),
    ("public-interest-majority", "Majority + public-interest screen"),
    ("agenda-lottery-majority", "Weighted agenda lottery + majority"),
    ("quadratic-attention-majority", "Quadratic attention budget + majority"),
    ("proposal-bond-majority", "Proposal bonds + majority"),
    ("harm-weighted-majority", "Harm-weighted double majority"),
    ("compensation-majority", "Compensation amendments + majority"),
    ("package-bargaining-majority", "Package bargaining + majority"),
    ("multidimensional-package-majority", "Multidimensional package bargaining + majority"),
    ("law-registry-majority", "Active-law registry + majority review"),
    ("public-objection-majority", "Public objection window + majority"),
    ("anti-capture-majority-bundle", "Majority + anti-capture bundle"),
    ("risk-routed-majority", "Risk-routed majority legislature"),
    ("portfolio-hybrid-legislature", "Portfolio hybrid legislature"),
    ("norm-erosion-majority", "Endogenous norm erosion + majority"),
    ("default-pass", "Default pass unless 2/3 block"),
    ("default-pass-challenge", "Default pass + challenge vouchers"),
    ("default-pass-multiround-mediation-challenge", "Default pass + mediation + challenge"),
]
FIELDS = [
    "directionalScore",
    "productivity",
    "compromise",
    "weakPublicMandatePassage",
    "administrativeCost",
    "welfare",
    "riskControl",
]


def broad_case(case_key: str) -> bool:
    return not case_key.startswith("party-system-") and not case_key.startswith("era-")


def run_campaign(seed: int) -> Path:
    output_dir = RAW_DIR / str(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    java_props = os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21").split()
    command = [
        "java",
        *java_props,
        "-cp",
        "out/main",
        "congresssim.Main",
        "--campaign",
        "v21-paper",
        "--runs",
        str(RUNS),
        "--legislators",
        "101",
        "--bills",
        "60",
        "--seed",
        str(seed),
        "--output-dir",
        str(output_dir),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    return output_dir / "simulation-campaign-v21-paper.csv"


def read_seed_means(path: Path) -> dict[str, dict[str, float]]:
    totals: dict[str, defaultdict[str, float]] = {}
    counts: dict[str, int] = defaultdict(int)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            scenario = row["scenarioKey"]
            if scenario not in {key for key, _label in SCENARIOS} or not broad_case(row["caseKey"]):
                continue
            totals.setdefault(scenario, defaultdict(float))
            counts[scenario] += 1
            for field in FIELDS:
                totals[scenario][field] += float(row[field])
    return {
        scenario: {field: value / counts[scenario] for field, value in values.items()}
        for scenario, values in totals.items()
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def main() -> int:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)

    by_scenario: dict[str, defaultdict[str, list[float]]] = {
        key: defaultdict(list) for key, _label in SCENARIOS
    }
    for seed in SEEDS:
        seed_means = read_seed_means(run_campaign(seed))
        for scenario, values in seed_means.items():
            for field, value in values.items():
                by_scenario[scenario][field].append(value)

    with REPORT_CSV.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["scenarioKey", "scenario", "metric", "seedCount", "mean", "min", "max", "range"])
        for scenario_key, scenario_name in SCENARIOS:
            for field in FIELDS:
                values = by_scenario[scenario_key][field]
                writer.writerow([
                    scenario_key,
                    scenario_name,
                    field,
                    len(values),
                    f"{mean(values):.6f}",
                    f"{min(values):.6f}",
                    f"{max(values):.6f}",
                    f"{(max(values) - min(values)):.6f}",
                ])

    lines = [
        "# Seed Robustness Summary",
        "",
        "Deterministic multi-seed sweep for all paper comparison scenarios.",
        "The main paper table reports assumption-sensitivity bands across broad and adversarial campaign cases; this report checks whether paper-scenario relationships are stable across independent base seeds.",
        "",
        f"- Seeds: {', '.join(str(seed) for seed in SEEDS)}",
        f"- Runs per seed: {RUNS}",
        "- Cases summarized: broad and adversarial assumption cases only",
        "",
        "| Scenario | Metric | Mean | Min | Max | Range |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for scenario_key, scenario_name in SCENARIOS:
        for field in FIELDS:
            values = by_scenario[scenario_key][field]
            lines.append(
                f"| {scenario_name} | {field} | {mean(values):.3f} | "
                f"{min(values):.3f} | {max(values):.3f} | {(max(values) - min(values)):.3f} |"
            )
    REPORT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT_CSV}")
    print(f"Wrote {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
