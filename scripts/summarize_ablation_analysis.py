#!/usr/bin/env python3
"""Summarize mechanism ablation campaign output."""

from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("reports/simulation-ablation-analysis.csv")
OUT_CSV = Path("reports/ablation-analysis-summary.csv")
OUT_MD = Path("reports/ablation-analysis-summary.md")

ABLATIONS = [
    ("Policy tournament", "simple-majority-alternatives-pairwise", "simple-majority", "remove alternative comparison"),
    ("Risk routing", "risk-routed-majority", "simple-majority", "remove routing and high-risk lane"),
    ("Risk routing", "risk-routed-majority", "risk-routed-no-citizen-majority", "replace citizen review with supermajority lane"),
    ("Anti-capture", "anti-capture-majority-bundle", "simple-majority", "remove screen/audit/transparency bundle"),
    ("Anti-capture", "anti-capture-majority-bundle", "public-interest-majority", "keep public-interest screen only"),
    ("Affected groups", "compensation-majority", "simple-majority", "remove compensation stage"),
    ("Affected groups", "affected-consent-majority", "compensation-majority", "replace consent with compensation-only"),
    ("Package bargaining", "multidimensional-package-majority", "simple-majority", "remove package bargaining"),
    ("Package bargaining", "multidimensional-package-majority", "package-bargaining-majority", "replace multidimensional package with scalar package"),
    ("Reversibility", "law-registry-majority", "simple-majority", "remove active-law registry"),
]


def read_rows() -> list[dict[str, str]]:
    if not INPUT.exists():
        raise SystemExit(f"{INPUT} is missing. Run make ablation-analysis first.")
    with INPUT.open(newline="") as handle:
        return list(csv.DictReader(handle))


def average_by_scenario(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    totals: dict[str, dict[str, float]] = {}
    counts: dict[str, int] = {}
    fields = [
        "directionalScore",
        "productivity",
        "compromise",
        "weakPublicMandatePassage",
        "administrativeCost",
        "riskControl",
        "welfare",
    ]
    for row in rows:
        scenario = row["scenarioKey"]
        totals.setdefault(scenario, {field: 0.0 for field in fields})
        counts[scenario] = counts.get(scenario, 0) + 1
        for field in fields:
            totals[scenario][field] += float(row[field])
    return {
        scenario: {field: value / counts[scenario] for field, value in values.items()}
        for scenario, values in totals.items()
    }


def classify(delta_directional: float, delta_compromise: float, weak_mandate_reduction: float, admin_added: float) -> str:
    if delta_directional > 0.02 and (delta_compromise > 0.01 or weak_mandate_reduction > 0.01):
        if admin_added > 0.08:
            return "helps, but with visible process cost"
        return "helps under this ablation screen"
    if delta_directional < -0.02:
        return "component hurts this value profile"
    if admin_added > 0.08:
        return "small gain relative to added process cost"
    return "mixed or small effect"


def write_outputs(averages: dict[str, dict[str, float]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for family, full, base, ablation in ABLATIONS:
        if full not in averages or base not in averages:
            continue
        full_values = averages[full]
        base_values = averages[base]
        delta_directional = full_values["directionalScore"] - base_values["directionalScore"]
        delta_productivity = full_values["productivity"] - base_values["productivity"]
        delta_compromise = full_values["compromise"] - base_values["compromise"]
        weak_mandate_reduction = base_values["weakPublicMandatePassage"] - full_values["weakPublicMandatePassage"]
        admin_added = full_values["administrativeCost"] - base_values["administrativeCost"]
        rows.append({
            "family": family,
            "fullScenario": full,
            "comparisonScenario": base,
            "ablation": ablation,
            "deltaDirectional": f"{delta_directional:.6f}",
            "deltaProductivity": f"{delta_productivity:.6f}",
            "deltaCompromise": f"{delta_compromise:.6f}",
            "weakMandateReduction": f"{weak_mandate_reduction:.6f}",
            "adminCostAdded": f"{admin_added:.6f}",
            "interpretation": classify(delta_directional, delta_compromise, weak_mandate_reduction, admin_added),
        })

    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Mechanism Ablation Summary",
        "",
        "This report compares selected mechanism bundles with nearby ablations across the ablation campaign's broad and adversarial cases. Positive directional/productivity/compromise deltas favor the full mechanism. Positive weak-mandate reduction means fewer weakly publicly supported enactments. Positive admin-cost added means the full mechanism is procedurally heavier.",
        "",
        "| Family | Full scenario | Comparison | Δ directional | Δ productivity | Δ compromise | Weak-mandate reduction | Admin cost added | Interpretation |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['family']} | `{row['fullScenario']}` | `{row['comparisonScenario']}` | "
            f"{float(row['deltaDirectional']):.3f} | {float(row['deltaProductivity']):.3f} | "
            f"{float(row['deltaCompromise']):.3f} | {float(row['weakMandateReduction']):.3f} | "
            f"{float(row['adminCostAdded']):.3f} | {row['interpretation']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    write_outputs(average_by_scenario(read_rows()))
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
