#!/usr/bin/env python3
"""Summarize paper datapoint validation and comparison findings from generated CSVs."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN_CSV = ROOT / "reports" / "simulation-campaign-v21-paper.csv"
SEED_CSV = ROOT / "reports" / "seed-robustness-summary.csv"
REPORT = ROOT / "reports" / "paper-findings-validation.md"

FOCUS = [
    "current-system",
    "simple-majority-alternatives-pairwise",
    "portfolio-hybrid-legislature",
    "risk-routed-majority",
    "anti-capture-majority-bundle",
    "law-registry-majority",
    "default-pass",
    "default-pass-multiround-mediation-challenge",
]
FIELDS = [
    "directionalScore",
    "productivity",
    "compromise",
    "riskControl",
    "representativeQuality",
    "administrativeFeasibility",
    "weakPublicMandatePassage",
    "welfare",
    "lobbyCapture",
    "proposerGain",
    "policyShift",
    "minorityHarm",
    "administrativeCost",
]


def broad_case(case_key: str) -> bool:
    return not case_key.startswith("party-system-") and not case_key.startswith("era-")


def average(rows: list[dict[str, str]], case_filter=broad_case) -> dict[str, dict[str, float]]:
    totals: dict[str, defaultdict[str, float]] = defaultdict(lambda: defaultdict(float))
    counts: dict[str, int] = defaultdict(int)
    names: dict[str, str] = {}
    for row in rows:
        if not case_filter(row["caseKey"]):
            continue
        key = row["scenarioKey"]
        counts[key] += 1
        names[key] = row["scenario"]
        for field in FIELDS:
            totals[key][field] += float(row[field])
    return {
        key: {
            "__count__": float(counts[key]),
            **{field: totals[key][field] / counts[key] for field in FIELDS},
            "__name__": names[key],
        }
        for key in totals
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_seed_directional() -> dict[str, tuple[float, float, float]]:
    if not SEED_CSV.exists():
        return {}
    output: dict[str, tuple[float, float, float]] = {}
    with SEED_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["metric"] == "directionalScore":
                output[row["scenarioKey"]] = (
                    float(row["mean"]),
                    float(row["min"]),
                    float(row["max"]),
                )
    return output


def fmt(value: float) -> str:
    return f"{value:.3f}"


def delta(value: float) -> str:
    return f"{value:+.3f}"


def rank(averages: dict[str, dict[str, float]], field: str, reverse: bool = True) -> list[str]:
    return sorted(averages, key=lambda key: averages[key][field], reverse=reverse)


def row_md(key: str, values: dict[str, float], seeds: dict[str, tuple[float, float, float]]) -> str:
    seed = seeds.get(key)
    seed_text = "n/a"
    if seed:
        mean, low, high = seed
        seed_text = f"{fmt(mean)} [{fmt(low)}, {fmt(high)}]"
    return (
        f"| `{key}` | {values['__name__']} | {fmt(values['directionalScore'])} | "
        f"{fmt(values['productivity'])} | {fmt(values['compromise'])} | "
        f"{fmt(values['riskControl'])} | {fmt(values['representativeQuality'])} | "
        f"{fmt(values['weakPublicMandatePassage'])} | {fmt(values['welfare'])} | "
        f"{fmt(values['lobbyCapture'])} | {seed_text} |"
    )


def comparison_line(
        averages: dict[str, dict[str, float]],
        source: str,
        target: str,
        label: str
) -> str:
    source_values = averages[source]
    target_values = averages[target]
    return (
        f"- Versus {label}, `{source}` changes productivity by "
        f"{delta(source_values['productivity'] - target_values['productivity'])}, "
        f"compromise by {delta(source_values['compromise'] - target_values['compromise'])}, "
        f"risk control by {delta(source_values['riskControl'] - target_values['riskControl'])}, "
        f"weak-mandate passage by {delta(source_values['weakPublicMandatePassage'] - target_values['weakPublicMandatePassage'])}, "
        f"and lobbying capture by {delta(source_values['lobbyCapture'] - target_values['lobbyCapture'])}."
    )


def main() -> int:
    if not CAMPAIGN_CSV.exists():
        raise SystemExit(f"{CAMPAIGN_CSV} is missing; run make paper-campaign first.")
    rows = read_rows(CAMPAIGN_CSV)
    broad = average(rows)
    party = average(rows, lambda case_key: case_key.startswith("party-system-"))
    seeds = read_seed_directional()

    top_directional = rank(broad, "directionalScore")[:8]
    top_compromise = rank(party, "compromise")[:5] if party else rank(broad, "compromise")[:5]
    top_productivity = rank(broad, "productivity")[:5]
    lowest_weak = rank(broad, "weakPublicMandatePassage", reverse=False)[:5]
    highest_welfare = rank(broad, "welfare")[:5]

    lines = [
        "# Paper Findings Validation",
        "",
        "This report is generated from `reports/simulation-campaign-v21-paper.csv` and, when present, `reports/seed-robustness-summary.csv`. It is a validation aid for the paper tables and figures, not a separate empirical result.",
        "",
        "## Data Integrity Checks",
        "",
        f"- Campaign rows: {len(rows)}",
        f"- Broad/adversarial scenarios with averages: {len(broad)}",
        f"- Broad/adversarial cases per scenario: {sorted({int(values['__count__']) for values in broad.values()})}",
        f"- Portfolio hybrid present: {'yes' if 'portfolio-hybrid-legislature' in broad else 'no'}",
        f"- Seed directional intervals present for focus scenarios: {sum(1 for key in FOCUS if key in seeds)} / {len(FOCUS)}",
        "",
        "## Focus Scenario Averages",
        "",
        "| Key | Scenario | Dir. | Prod. | Comp. | Risk ctrl. | Rep. quality | Weak mandate | Welfare | Lobby capture | Seed dir. mean [min,max] |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for key in FOCUS:
        if key in broad:
            lines.append(row_md(key, broad[key], seeds))

    lines.extend([
        "",
        "## Ranking Cross-Checks",
        "",
        "- Top directional scores: "
        + ", ".join(f"`{key}` ({fmt(broad[key]['directionalScore'])})" for key in top_directional)
        + ".",
        "- Top compromise scores under party-system sensitivity cases: "
        + ", ".join(f"`{key}` ({fmt(party.get(key, broad[key])['compromise'])})" for key in top_compromise)
        + ".",
        "- Top productivity scores: "
        + ", ".join(f"`{key}` ({fmt(broad[key]['productivity'])})" for key in top_productivity)
        + ".",
        "- Lowest weak public-mandate passage: "
        + ", ".join(f"`{key}` ({fmt(broad[key]['weakPublicMandatePassage'])})" for key in lowest_weak)
        + ".",
        "- Highest generated welfare: "
        + ", ".join(f"`{key}` ({fmt(broad[key]['welfare'])})" for key in highest_welfare)
        + ".",
        "",
        "## Hybrid Interpretation",
        "",
    ])
    if "portfolio-hybrid-legislature" in broad:
        lines.extend([
            comparison_line(broad, "portfolio-hybrid-legislature", "simple-majority-alternatives-pairwise", "pairwise alternatives"),
            comparison_line(broad, "portfolio-hybrid-legislature", "risk-routed-majority", "risk-routed majority"),
            comparison_line(broad, "portfolio-hybrid-legislature", "anti-capture-majority-bundle", "anti-capture bundle"),
            comparison_line(broad, "portfolio-hybrid-legislature", "default-pass", "open default pass"),
            "",
            "The hybrid is best read as a synthesized candidate rather than a final winner. Pairwise alternatives remain the cleanest non-default productivity/compromise result. The hybrid preserves much of that productivity while adding lower lobbying capture and stronger weak-mandate control, but it pays in administrative load and loses some compromise because not every bill enters the pairwise route.",
            "",
            "The design hypothesis to carry forward is a portfolio legislature: low-risk bills should move quickly; medium-risk bills should face alternative comparison and mediation; high-risk or high-harm bills should face public/harm review; proposers should internalize some outcome risk; organized-interest pressure should be visible and audited; enacted high-uncertainty laws should be reviewed later.",
        ])

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
