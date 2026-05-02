#!/usr/bin/env python3
"""Summarize manipulation-stress campaign output."""

from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("reports/simulation-manipulation-stress.csv")
OUT_CSV = Path("reports/manipulation-stress-summary.csv")
OUT_MD = Path("reports/manipulation-stress-summary.md")

PAIR_TESTS = [
    (
        "Policy tournament clone/decoy attack",
        "clone-decoy-pressure",
        "simple-majority-alternatives-pairwise",
        "simple-majority-alternatives-strategic",
        "strategic clone and decoy variant",
    ),
    (
        "Citizen-panel manipulation",
        "capture-flooding",
        "citizen-assembly-threshold",
        "citizen-assembly-manipulation-stress",
        "smaller, noisier, more manipulable panel",
    ),
    (
        "Bad-faith harm claims",
        "rights-harm-pressure",
        "harm-weighted-majority",
        "harm-weighted-loose-claims-majority",
        "lower harm threshold creates more false-positive review pressure",
    ),
    (
        "Astroturf objection pressure",
        "capture-flooding",
        "public-objection-majority",
        "public-objection-astroturf-majority",
        "lower objection threshold and higher noise",
    ),
]

CASE_TESTS = [
    (
        "Agenda flooding",
        "agenda-lottery-majority",
        "baseline",
        "proposal-flooding",
        "same agenda lottery under proposal flooding",
    ),
    (
        "Anti-capture defensive backlash",
        "anti-capture-majority-bundle",
        "baseline",
        "anti-lobbying-backlash",
        "same anti-capture bundle under defensive lobbying backlash",
    ),
    (
        "Open default-pass capture stress",
        "default-pass",
        "baseline",
        "capture-flooding",
        "throughput stress test under capture and flooding",
    ),
]


def rows_by_case_scenario() -> dict[tuple[str, str], dict[str, str]]:
    if not INPUT.exists():
        raise SystemExit(f"{INPUT} is missing. Run make manipulation-stress first.")
    with INPUT.open(newline="") as handle:
        return {(row["caseKey"], row["scenarioKey"]): row for row in csv.DictReader(handle)}


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def comparison_row(
        test: str,
        reference: dict[str, str],
        stressed: dict[str, str],
        stressor: str,
) -> dict[str, str]:
    directional_loss = f(reference, "directionalScore") - f(stressed, "directionalScore")
    compromise_loss = f(reference, "compromise") - f(stressed, "compromise")
    weak_mandate_added = f(stressed, "weakPublicMandatePassage") - f(reference, "weakPublicMandatePassage")
    admin_added = f(stressed, "administrativeCost") - f(reference, "administrativeCost")
    return {
        "test": test,
        "referenceScenario": reference["scenarioKey"],
        "stressedScenario": stressed["scenarioKey"],
        "referenceCase": reference["caseKey"],
        "stressedCase": stressed["caseKey"],
        "stressor": stressor,
        "directionalLoss": f"{directional_loss:.6f}",
        "compromiseLoss": f"{compromise_loss:.6f}",
        "weakMandateAdded": f"{weak_mandate_added:.6f}",
        "adminCostAdded": f"{admin_added:.6f}",
        "stressVerdict": verdict(directional_loss, weak_mandate_added, admin_added),
    }


def verdict(directional_loss: float, weak_mandate_added: float, admin_added: float) -> str:
    if directional_loss > 0.05 or weak_mandate_added > 0.05:
        return "material vulnerability"
    if admin_added > 0.08:
        return "resists partly through higher process cost"
    if directional_loss < -0.02:
        return "stress variant improves this score profile"
    return "limited observed degradation"


def write_outputs(index: dict[tuple[str, str], dict[str, str]]) -> None:
    rows: list[dict[str, str]] = []
    for test, case, reference, stressed, stressor in PAIR_TESTS:
        ref = index.get((case, reference))
        stress = index.get((case, stressed))
        if ref and stress:
            rows.append(comparison_row(test, ref, stress, stressor))
    for test, scenario, baseline_case, stress_case, stressor in CASE_TESTS:
        ref = index.get((baseline_case, scenario))
        stress = index.get((stress_case, scenario))
        if ref and stress:
            rows.append(comparison_row(test, ref, stress, stressor))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Manipulation Stress Summary",
        "",
        "Positive directional/compromise loss means the stress condition performed worse than its reference. Positive weak-mandate and admin-cost additions are also worse.",
        "",
        "| Test | Stressor | Directional loss | Compromise loss | Weak mandate added | Admin cost added | Verdict |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['test']} | {row['stressor']} | {float(row['directionalLoss']):.3f} | "
            f"{float(row['compromiseLoss']):.3f} | {float(row['weakMandateAdded']):.3f} | "
            f"{float(row['adminCostAdded']):.3f} | {row['stressVerdict']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    write_outputs(rows_by_case_scenario())
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
