#!/usr/bin/env python3
"""Hard publication check for the locked House agenda-control calibration."""

from __future__ import annotations

import csv
import hashlib
import json
from math import fsum, isfinite, sqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ROOT / "reports" / "house-agenda-control-calibration-candidates.csv"
METRICS = ROOT / "reports" / "house-agenda-control-calibration-metrics.csv"
REPORT = ROOT / "reports" / "house-agenda-control-calibration.md"
METADATA = ROOT / "reports" / "house-agenda-control-calibration-metadata.json"
SEEDS = ROOT / "reports" / "house-agenda-control-calibration-seeds.csv"
MONTE_CARLO = ROOT / "reports" / "house-agenda-control-calibration-monte-carlo.csv"

EXPECTED_HASHES = {
    "papers/empirical-validation/house-agenda-control-calibration-specification.md": "d7fdb1b7cd6131077479ed7bacf2c5404706e671e9cf12c200b7580ae99ccc72",
    "papers/empirical-validation/house-agenda-control-provenance-amendment.md": "6d57e0cd78fcb09d76946a440ef81702343de0c67363f53ea5ab2dc139867ef2",
    "data/validation/raw/house_agenda_control.csv": "d801a86290d2eb7127736ef259a44847fe5d19acff2c4dd738d2f00ba0556f7b",
    "data/validation/raw/house_special_rule_grants.csv": "5b31f228e25449f05210234c19a8c9311911c5f75a35d9dd6bb77d6333988a53",
    "reports/house-agenda-control-metrics.csv": "8b90b8a5e0ee48898de46acdb8d81061cd18546849181691a725016157542c09",
    "reports/house-agenda-control-calibration-candidates.csv": "8574e596907390c5e6991ae81e0b17724912f685034f13c69868d8d5a5047797",
    "reports/house-agenda-control-calibration-metrics.csv": "09084f95ce1331be4c776669b31fd58d2da5650e22b53f6b65d336d308750b5c",
    "reports/house-agenda-control-calibration.md": "e941e8e48964d743a6d7f521ddcd2402f08ab14880fb6fa676b3220fc43315d3",
    "reports/house-agenda-control-calibration-seeds.csv": "018ee8dab0c7467b798543a47ca5a358ff94ac66b372f9162acfaaca987b5036",
    "reports/house-agenda-control-calibration-monte-carlo.csv": "be1221d144ccf220b103d20642ea2594f5964329e7c7362f708a87c56bf0ff2b",
    "scripts/validation/write_house_agenda_control_calibration.py": "62ad8596d5337e8f1dce6bd318db8d00698941086cd43f040ffbbe904e6817c5",
    "src/main/java/congresssim/institution/agenda/FloorRuleSchedulingProcess.java": "f4ac1fee47b093c33f79121c397ce8de9311d9f887eabbc8bbb49763728a9395",
    "src/main/java/congresssim/simulation/catalog/HouseAgendaControlCalibrationProbe.java": "c1e23822d4c542591628e6dafa7899224847f404d92c835dca65fac77834900c",
    "out/congresssim.jar": "c27e9827c717bb2e7f0080cfe7b3bd2e34df5360d3a3c5393b82bfefa913704b",
}

EXPECTED_SELECTED = {
    "calendarPriorityThreshold": "0.680000000000",
    "specialRuleThreshold": "0.475000000000",
    "suspensionThreshold": "0.750000000000",
    "seedCount": "20",
    "runsPerSeed": "12",
    "simulatedBills": "14400",
    "committeeAdvanceRate": "0.110555555556",
    "floorConsiderationRate": "0.065277777778",
    "specialRuleOnlyRouteShare": "0.081914893617",
    "suspensionOnlyRouteShare": "0.818085106383",
    "mixedSpecialRuleAndSuspensionRouteShare": "0.059574468085",
    "otherFloorRouteShare": "0.040425531915",
    "restrictiveSpecialRuleShare": "1.000000000000",
    "selectionLoss": "4.248261080522",
    "maximumAbsoluteStandardizedError": "1.712056737605",
    "selected": "1",
}

EXPECTED_TEST_METRICS = {
    "committeeAdvanceRate": ("0.107527777778", "0.020000000000", "pass"),
    "floorConsiderationRate": ("0.062805555556", "0.020000000000", "pass"),
    "specialRuleOnlyRouteShare": ("0.077399380805", "", "reported"),
    "suspensionOnlyRouteShare": ("0.812914639540", "", "reported"),
    "mixedSpecialRuleAndSuspensionRouteShare": ("0.057054400708", "", "reported"),
    "otherFloorRouteShare": ("0.052631578947", "", "reported"),
    "restrictiveSpecialRuleShare": ("1.000000000000", "0.020000000000", "pass"),
    "routeTotalVariation": ("0.110470441680", "0.100000000000", "fail"),
}


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
    require(path.exists(), f"Missing required calibration artifact: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def check_hashes() -> None:
    for relative, expected in EXPECTED_HASHES.items():
        path = ROOT / relative
        require(path.exists(), f"Missing hash-pinned artifact: {relative}")
        actual = sha256(path)
        require(actual == expected, f"Hash drift for {relative}: {actual}")


def check_candidates() -> None:
    rows = read_csv(CANDIDATES)
    require(len(rows) == 1_445, "Calibration candidate count must remain 1,445.")
    require(
        len({(
            row["calendarPriorityThreshold"],
            row["specialRuleThreshold"],
            row["suspensionThreshold"],
        ) for row in rows}) == 1_445,
        "Calibration candidate triples must be unique.",
    )
    require(
        {row["calendarPriorityThreshold"] for row in rows}
        == {f"{value:.12f}" for value in (0.62, 0.64, 0.66, 0.68, 0.70)},
        "Calendar-priority grid drifted.",
    )
    require(
        len({row["specialRuleThreshold"] for row in rows}) == 17,
        "Special-rule grid size drifted.",
    )
    require(
        len({row["suspensionThreshold"] for row in rows}) == 17,
        "Suspension grid size drifted.",
    )
    selected = [row for row in rows if row["selected"] == "1"]
    require(len(selected) == 1, "Calibration must retain exactly one selected candidate.")
    for field, expected in EXPECTED_SELECTED.items():
        require(
            selected[0].get(field) == expected,
            f"Selected calibration field drifted: {field}={selected[0].get(field)}",
        )
    recomputed = min(
        rows,
        key=lambda row: (
            float(row["selectionLoss"]),
            float(row["maximumAbsoluteStandardizedError"]),
            float(row["calendarPriorityThreshold"]),
            float(row["specialRuleThreshold"]),
            float(row["suspensionThreshold"]),
        ),
    )
    require(recomputed is selected[0], "Selected row no longer minimizes the locked loss and tie break.")


def check_metrics() -> None:
    rows = read_csv(METRICS)
    require(len(rows) == 18, "Calibration metric table must retain 18 rows.")
    test_rows = {
        row["metric"]: row
        for row in rows
        if row["cohortRole"] == "primary_temporal_test"
    }
    require(len(test_rows) == 9, "Temporal-test metric count drifted.")
    for metric, (value, tolerance, status) in EXPECTED_TEST_METRICS.items():
        row = test_rows.get(metric)
        require(row is not None, f"Missing temporal-test metric: {metric}")
        require(row["simulatorValue"] == value, f"Temporal-test value drifted for {metric}.")
        require(row["tolerance"] == tolerance, f"Temporal-test tolerance drifted for {metric}.")
        require(row["status"] == status, f"Temporal-test status drifted for {metric}.")
    route_sum = sum(float(test_rows[metric]["simulatorValue"]) for metric in (
        "specialRuleOnlyRouteShare",
        "suspensionOnlyRouteShare",
        "mixedSpecialRuleAndSuspensionRouteShare",
        "otherFloorRouteShare",
    ))
    require(abs(route_sum - 1.0) <= 2e-12, "Temporal-test route shares must sum to one.")


def check_metadata() -> None:
    require(METADATA.exists(), "Missing calibration metadata.")
    metadata = json.loads(METADATA.read_text())
    require(metadata.get("study") == "house-agenda-control-calibration-v1", "Study ID drifted.")
    require(
        metadata.get("lockStatus") == "post-source-audit-prefit-chronology-unverified",
        "The unverified pre-fit chronology must remain explicit.",
    )
    require(
        metadata.get("runtime") == {"javaMajorVersion": 21},
        "Calibration runtime provenance drifted.",
    )
    protocol = metadata["protocol"]
    require(protocol["candidateCount"] == 1_445, "Metadata candidate count drifted.")
    require(protocol["developmentBillsPerCandidate"] == 14_400, "Development bill count drifted.")
    require(protocol["testBills"] == 36_000, "Test bill count drifted.")
    selected = metadata["selected"]
    require(selected["calendarPriorityThreshold"] == 0.68, "Selected calendar threshold drifted.")
    require(selected["specialRuleThreshold"] == 0.475, "Selected special threshold drifted.")
    require(selected["suspensionThreshold"] == 0.75, "Selected suspension threshold drifted.")
    require(selected["leaveOneSeedOutReselections"] == 16, "Stability count drifted.")
    gate = metadata["primaryTemporalGate"]
    require(gate["status"] == "fail", "The locked temporal failure must be retained.")
    require(gate["checks"] == {
        "committeeAdvanceRate": True,
        "floorConsiderationRate": True,
        "restrictiveSpecialRuleShare": True,
        "routeTotalVariation": False,
    }, "Temporal gate cells drifted.")
    for relative, digest in metadata["inputs"].items():
        require(sha256(ROOT / relative) == digest, f"Metadata input hash drifted: {relative}")
    require(
        set(metadata["outputs"]) == {
            str(path.relative_to(ROOT))
            for path in (CANDIDATES, METRICS, REPORT, SEEDS, MONTE_CARLO)
        },
        "Metadata must include the full candidate, metric, report, and seed outputs.",
    )
    for relative, digest in metadata["outputs"].items():
        require(sha256(ROOT / relative) == digest, f"Metadata output hash drifted: {relative}")


def check_monte_carlo() -> None:
    seeds = read_csv(SEEDS)
    summaries = read_csv(MONTE_CARLO)
    require(len(seeds) == 50, "Monte Carlo output must retain 50 seeds.")
    require(len(summaries) == 26, "Monte Carlo output must retain 26 metric summaries.")
    require(len({(row["cohort"], row["seed"]) for row in seeds}) == 50, "Duplicate seed rows.")
    require(len({(row["cohort"], row["metric"]) for row in summaries}) == 26, "Duplicate summaries.")
    pooled = {(row["cohortRole"], row["metric"]): row for row in read_csv(METRICS)}
    for cohort, role, count, base, step, runs in (
        ("development_116_117", "development", 20, 1161170001, 104729, 12),
        ("118", "primary_temporal_test", 30, 1180000001, 130363, 20),
    ):
        rows = [row for row in seeds if row["cohort"] == cohort]
        require(
            {int(row["seed"]) for row in rows} == {base + step * index for index in range(count)},
            f"{cohort}: seed panel drifted.",
        )
        require(all(int(row["runs"]) == runs and int(row["simulatedBills"]) == runs * 60 for row in rows), "Seed denominators drifted.")
        for field in ("committeeAdvanceRate", "floorConsiderationRate"):
            average = fsum(float(row[field]) for row in rows) / count
            require(abs(average - float(pooled[role, field]["simulatorValue"])) < 2e-12, "Pooled rates disagree with seed output.")
        total_floor = fsum(float(row["floorConsiderationRate"]) for row in rows)
        for field in (
            "specialRuleOnlyRouteShare", "suspensionOnlyRouteShare",
            "mixedSpecialRuleAndSuspensionRouteShare", "otherFloorRouteShare",
        ):
            share = fsum(float(row[field]) * float(row["floorConsiderationRate"]) for row in rows) / total_floor
            require(abs(share - float(pooled[role, field]["simulatorValue"])) < 2e-11, "Pooled route shares disagree with seed output.")
        for summary in (row for row in summaries if row["cohort"] == cohort):
            values = [float(row[summary["metric"]]) for row in rows]
            require(all(isfinite(value) and 0 <= value <= 1 for value in values), "Invalid seed metric.")
            average = fsum(values) / count
            deviation = sqrt(fsum((value - average) ** 2 for value in values) / (count - 1))
            expected = {
                "mean": average,
                "sampleStandardDeviation": deviation,
                "standardErrorOfMean": deviation / sqrt(count),
                "minimum": min(values),
                "maximum": max(values),
            }
            require(summary["seedCount"] == str(count), "Summary seed count drifted.")
            for field, value in expected.items():
                require(summary[field] == f"{value:.12f}", f"Monte Carlo {summary['metric']} {field} drifted.")


def check_report() -> None:
    require(REPORT.exists(), "Missing calibration report.")
    text = REPORT.read_text()
    required = (
        "Protocol chronology is unverified: no separate pre-fit commit exists",
        "## Monte Carlo Variation",
        "The acceptance gate continues to use pooled bill rates and pooled conditional route shares.",
        "Primary temporal gate: **FAIL**.",
        "Source-attribution caveat: these are the preserved v1 results.",
        "The route-composition gate fails by 0.010470 total-variation units.",
        "the candidate grid is not expanded and no route threshold is retuned",
        "Grid-boundary warning: yes",
        "16 / 20 panels reselected the full-panel triple",
        "does not transport the observed route shift",
        "The earlier lifecycle calibration remains unchanged",
        "It does not validate bill-level agenda decisions",
    )
    for phrase in required:
        require(phrase in text, f"Calibration report lost required boundary text: {phrase}")
    require("Primary temporal gate: **PASS**" not in text, "Report must not upgrade the locked failure.")


def check_publication_claims() -> None:
    for relative in (
        "paper/acm-ci-framework/acm-ci-framework.tex",
        "paper/simulation-backlog.md",
    ):
        text = (ROOT / relative).read_text()
        require(
            "overproduces special-only" not in text
            and "overproducing special-only" not in text,
            f"Incorrect House route-error direction in {relative}.",
        )
    # Planning README files are intentionally excluded from the reviewer bundle.
    planning_readme = ROOT / "papers/empirical-validation/README.md"
    if planning_readme.exists():
        require(
            "overproduces special-only" not in planning_readme.read_text(),
            "Incorrect House route-error direction in the empirical planning README.",
        )
    appendix = (ROOT / "paper/technical-appendix/odd-d-appendix.tex").read_text()
    require(
        "The route-calibration specification was committed" not in appendix,
        "Appendix must not claim an unverified pre-fit House protocol commit.",
    )
    require(
        "thresholds only label admitted bills" in appendix
        and "do not change the inner voting rule" in appendix,
        "Appendix must distinguish diagnostic route labels from voting behavior.",
    )
    main_paper = (ROOT / "paper/acm-ci-framework/acm-ci-framework.tex").read_text()
    require(
        "assign diagnostic labels to admitted bills" in main_paper
        and "do not alter the inner voting threshold or amendment rights" in main_paper,
        "Main paper must preserve the diagnostic-only House route boundary.",
    )


def main() -> int:
    check_hashes()
    check_candidates()
    check_metrics()
    check_metadata()
    check_monte_carlo()
    check_report()
    check_publication_claims()
    print(
        "House agenda-control calibration check passed: 1,445 candidates, "
        "selected boundary triple retained, 3/4 temporal gates pass, route gate fails."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
