#!/usr/bin/env python3
"""Bridge optional raw empirical summaries to simulator calibration targets."""

from __future__ import annotations

import csv
from pathlib import Path


CALIBRATION = Path("reports/calibration-baseline.csv")
EMPIRICAL = Path("reports/empirical-validation-summary.csv")
OUT_CSV = Path("reports/empirical-bridge.csv")
OUT_MD = Path("reports/empirical-bridge.md")

BRIDGE = [
    ("Bill attrition", "bill_progression.csv", "enactmentRate", "current-system-enactment-rate"),
    ("Floor consideration", "bill_progression.csv", "floorLoad", "current-system-floor-load"),
    ("Roll-call coalition size", "voteview_rollcalls.csv", "coalitionSize", "party-unity-support-band"),
    ("Party unity", "voteview_rollcalls.csv", "partyUnity", "party-unity-support-band"),
    ("Sponsor success concentration", "sponsor_success.csv", "sponsorSuccessGini", "sponsor-success-concentration"),
    ("Lobby spending observability", "lobbying_disclosure.csv", "meanSpend", "lobbying-spend-observable"),
    ("Lobby spending concentration", "lobbying_disclosure.csv", "clientSpendGini", "lobbying-spend-observable"),
    ("Topic throughput", "topic_throughput.csv", "topicEnactmentRate", "topic-throughput-yield"),
    ("District public will", "district_public_opinion.csv", "intensityWeightedSupport", "district-public-will-alignment"),
    ("District turnout skew", "district_public_opinion.csv", "turnoutGini", "district-public-will-alignment"),
    ("Committee reporting", "committee_activity.csv", "committeeReportRate", "current-system-floor-load"),
    ("Campaign finance concentration", "campaign_finance.csv", "recipientFinanceGini", "lobbying-spend-observable"),
    ("Outside spending share", "campaign_finance.csv", "outsideSpendingShare", "lobbying-spend-observable"),
    ("Court emergency posture", "court_review.csv", "emergencyOrderRate", "judicial-review-constraint"),
    ("Court invalidation", "court_review.csv", "invalidationRate", "judicial-review-constraint"),
    ("Comparative bicameralism", "comparative_institutions.csv", "bicameralShare", "bicameral-veto-burden"),
    ("Comparative productivity", "comparative_institutions.csv", "meanLegislativeProductivity", "topic-throughput-yield"),
]


def read_by_key(path: Path, key_field: str) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="") as handle:
        return {row[key_field]: row for row in csv.DictReader(handle)}


def read_empirical(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="") as handle:
        return {(row["dataset"], row["metric"]): row for row in csv.DictReader(handle)}


def status(raw: dict[str, str] | None, calibration: dict[str, str] | None) -> str:
    if calibration is None:
        return "missing calibration target"
    if raw is None or raw.get("status") == "missing":
        return "needs raw dataset"
    if raw.get("status") != "computed":
        return raw.get("status", "unknown")
    return "raw summary available"


def write_outputs() -> None:
    calibration = read_by_key(CALIBRATION, "key")
    empirical = read_empirical(EMPIRICAL)
    rows: list[dict[str, str]] = []
    for signal, dataset, metric, target in BRIDGE:
        raw = empirical.get((dataset, metric))
        cal = calibration.get(target)
        rows.append({
            "signal": signal,
            "rawDataset": dataset,
            "rawMetric": metric,
            "rawValue": "" if raw is None else raw.get("value", ""),
            "rawStatus": "missing" if raw is None else raw.get("status", "unknown"),
            "calibrationTarget": target,
            "simulatorScenario": "" if cal is None else cal["scenarioKey"],
            "simulatorMetric": "" if cal is None else cal["metric"],
            "simulatorObserved": "" if cal is None else cal["observed"],
            "targetRange": "" if cal is None else f"{cal['minimum']}--{cal['maximum']}",
            "bridgeStatus": status(raw, cal),
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Empirical Bridge",
        "",
        "This bridge makes the validation gap explicit. It maps each desired real-world signal to an optional raw-data summary and to the closest current simulator calibration target. Missing raw datasets are reported as work remaining, not as a failed simulator run.",
        "",
        "| Signal | Raw input/status | Simulator proxy | Observed | Target range | Bridge status |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        raw_value = row["rawValue"] if row["rawValue"] else "---"
        raw = f"`{row['rawDataset']}` / {row['rawMetric']} = {raw_value} ({row['rawStatus']})"
        proxy = f"`{row['simulatorScenario']}` / {row['simulatorMetric']}" if row["simulatorScenario"] else "---"
        observed = row["simulatorObserved"] if row["simulatorObserved"] else "---"
        target_range = row["targetRange"] if row["targetRange"] else "---"
        lines.append(f"| {row['signal']} | {raw} | {proxy} | {observed} | {target_range} | {row['bridgeStatus']} |")
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    write_outputs()
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
