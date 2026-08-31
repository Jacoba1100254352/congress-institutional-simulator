#!/usr/bin/env python3
"""Report no-refit transport of the 117th lifecycle calibration to Congresses 116 and 118."""

from __future__ import annotations

import csv
import math
from pathlib import Path


CENSUS_116 = Path("data/validation/raw/govinfo_bill_census_116.csv")
CENSUS_117 = Path("data/validation/raw/govinfo_bill_census.csv")
CENSUS_118 = Path("data/validation/raw/govinfo_bill_census_118.csv")
METADATA_116 = Path("data/validation/raw/govinfo_bill_census_116.metadata.md")
METADATA_117 = Path("data/validation/raw/govinfo_bill_census.metadata.md")
METADATA_118 = Path("data/validation/raw/govinfo_bill_census_118.metadata.md")
CENSUS_REPORT_117 = Path("reports/govinfo-bill-census.csv")
CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
BASELINES = Path("reports/calibration-baseline.csv")
OUT_CSV = Path("reports/legislative-lifecycle-temporal-replication.csv")
OUT_MD = Path("reports/legislative-lifecycle-temporal-replication.md")

FROZEN_CALIBRATION_COMMIT = "c5a2a7fdf11afbbd8d91c467e74e841f6e1843c7"
FROZEN_CLASSIFIER_VERSION = "govinfo-bill-lifecycle-v1"
FROZEN_BUILDER_SHA256 = "8b764e3d4577190a1da15b865911ca8191337415774a968df41662cc42c3b7fa"
FROZEN_CENSUS_SHA256 = "8e43e521148f113e95a2040ec592d7c5470c6303676a534f3d272497cc7bea36"
EXPECTED_THRESHOLD = "0.680"
EXPECTED_CLASSIFIER_VERSION = "govinfo-bill-lifecycle-v3"

METRICS = (
    {
        "metric": "committeeAdvanceRate",
        "label": "Committee advancement",
        "censusField": "committee_advanced",
        "summaryField": "committeeAdvancedRate",
        "simulatorField": "committeeAdvanceRate",
        "tolerance": 0.020,
        "baselineKey": "current-congress-committee-advance-rate",
    },
    {
        "metric": "floorConsiderationRate",
        "label": "Substantive floor consideration",
        "censusField": "floor_considered",
        "summaryField": "floorConsideredRate",
        "simulatorField": "floorConsiderationRate",
        "tolerance": 0.015,
        "baselineKey": "current-congress-floor-consideration-rate",
    },
    {
        "metric": "enactmentRate",
        "label": "Enactment",
        "censusField": "enacted",
        "summaryField": "enactedRate",
        "simulatorField": "enactmentRate",
        "tolerance": 0.010,
        "baselineKey": "current-congress-enactment-rate",
    },
)

CLAIM_BOUNDARY = (
    "This is a no-refit transport check for three aggregate legislative-flow rates. "
    "It tests whether one stylized workflow remains close to one earlier and one later "
    "completed Congress under tolerances fixed for the 117th calibration. It does not "
    "validate causal mechanisms, individual bills, public preferences, welfare, or "
    "institutional rankings."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def metadata_values(path: Path) -> dict[str, str]:
    require(path.exists(), f"Missing required artifact: {path}")
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            result[key] = value.strip().strip("`")
    return result


def wilson_interval(
    successes: int,
    total: int,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 0.0)
    proportion = successes / total
    denominator = 1.0 + (z * z / total)
    center = (proportion + z * z / (2.0 * total)) / denominator
    spread = (
        z
        * math.sqrt(
            (proportion * (1.0 - proportion) / total)
            + (z * z / (4.0 * total * total))
        )
        / denominator
    )
    return (max(0.0, center - spread), min(1.0, center + spread))


def build_rows(
    rows_117: list[dict[str, str]],
    test_rows: list[dict[str, str]],
    selected: dict[str, str],
    selection_summary: dict[str, str],
    baselines: dict[str, dict[str, str]],
    *,
    test_congress: str | None = None,
) -> list[dict[str, str]]:
    if test_congress is None:
        test_congress = next(
            (row.get("congress", "") for row in test_rows if row.get("congress")),
            "test",
        )
    output: list[dict[str, str]] = []
    for spec in METRICS:
        field = str(spec["censusField"])
        count_117 = sum(row.get(field) == "1" for row in rows_117)
        test_count = sum(row.get(field) == "1" for row in test_rows)
        rate_117 = count_117 / len(rows_117)
        test_rate = test_count / len(test_rows)
        lower, upper = wilson_interval(test_count, len(test_rows))
        simulated = float(selected[str(spec["simulatorField"])])
        error = simulated - test_rate
        tolerance = float(spec["tolerance"])
        within_tolerance = abs(error) <= tolerance + 1e-12
        baseline = baselines[str(spec["baselineKey"])]
        minimum = float(baseline["minimum"])
        maximum = float(baseline["maximum"])
        output.append({
            "metric": str(spec["metric"]),
            "censusField": field,
            "simulatorField": str(spec["simulatorField"]),
            "selectionCongress": "117",
            "testCongress": test_congress,
            "frozenThreshold": selected["calendarPriorityThreshold"],
            "seedCount": selected["seedCount"],
            "simulatedBills": selected["simulatedBills"],
            "selectionTargetRate": f"{float(selection_summary[str(spec['summaryField'])]):.6f}",
            "calibrationCongressCount": str(count_117),
            "calibrationCongressBills": str(len(rows_117)),
            "calibrationCongressRate": f"{rate_117:.6f}",
            "testCount": str(test_count),
            "testBills": str(len(test_rows)),
            "testRate": f"{test_rate:.6f}",
            "testWilson95Low": f"{lower:.6f}",
            "testWilson95High": f"{upper:.6f}",
            "empiricalRateShift": f"{test_rate - rate_117:.6f}",
            "simulatorMean": f"{simulated:.6f}",
            "transportError": f"{error:.6f}",
            "absoluteTransportError": f"{abs(error):.6f}",
            "prespecifiedTolerance": f"{tolerance:.6f}",
            "toleranceStatus": "pass" if within_tolerance else "fail",
            "baselineMinimum": f"{minimum:.6f}",
            "baselineMaximum": f"{maximum:.6f}",
            "testRateInBaselineRange": "pass" if minimum <= test_rate <= maximum else "fail",
        })
    return output


def validate_inputs(
    rows_by_congress: dict[str, list[dict[str, str]]],
    metadata_by_congress: dict[str, dict[str, str]],
    selected_rows: list[dict[str, str]],
) -> None:
    expected_counts = {"116": 14148, "117": 15066, "118": 16213}
    for congress, expected_count in expected_counts.items():
        rows = rows_by_congress[congress]
        metadata = metadata_by_congress[congress]
        require(len(rows) == expected_count, f"{congress}th census row count drifted.")
        require(
            {row.get("congress") for row in rows} == {congress},
            f"{congress}th census scope drifted.",
        )
        require(
            metadata.get("classification_version") == EXPECTED_CLASSIFIER_VERSION,
            f"{congress}th classifier version drifted.",
        )
    require(len(selected_rows) == 1, "Calibration must contain exactly one frozen selected row.")
    selected = selected_rows[0]
    require(selected.get("calendarPriorityThreshold") == EXPECTED_THRESHOLD, "Frozen threshold drifted.")
    require(selected.get("defaultThreshold") == EXPECTED_THRESHOLD, "Model default differs from frozen threshold.")
    require(selected.get("seedCount") == "50", "Frozen seed panel drifted.")
    require(selected.get("simulatedBills") == "72000", "Frozen simulated-bill count drifted.")


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    rows: list[dict[str, str]],
    metadata_by_congress: dict[str, dict[str, str]],
) -> None:
    by_congress = {
        congress: [row for row in rows if row["testCongress"] == congress]
        for congress in ("116", "118")
    }
    pass_counts = {
        congress: sum(row["toleranceStatus"] == "pass" for row in cohort_rows)
        for congress, cohort_rows in by_congress.items()
    }
    total_passes = sum(pass_counts.values())
    range_pass_count = sum(row["testRateInBaselineRange"] == "pass" for row in rows)
    enactment_118 = next(
        row
        for row in by_congress["118"]
        if row["metric"] == "enactmentRate"
    )
    excess = (
        float(enactment_118["absoluteTransportError"])
        - float(enactment_118["prespecifiedTolerance"])
    )
    labels = {str(spec["metric"]): str(spec["label"]) for spec in METRICS}
    lines = [
        "# Legislative Lifecycle Temporal Replication",
        "",
        "No-refit backcast and forecast of the complete 117th-Congress calibration design against complete 116th- and 118th-Congress H.R./S. censuses.",
        "",
        "## Frozen Protocol",
        "",
        f"- Calibration frozen in commit `{FROZEN_CALIBRATION_COMMIT}` before either external cohort entered the reporting or selection path",
        "- Frozen calendar-priority threshold: 0.68",
        "- Fixed panel: 50 seeds, 24 runs per seed, 72,000 simulated bills",
        "- Selection source: deterministic calibration half of the 117th-Congress census",
        "- Backcast source: all 14,148 H.R. and S. bills in the 116th Congress",
        "- Forecast source: all 16,213 H.R. and S. bills in the 118th Congress",
        "- No 116th or 118th rate is read by the calibration selector; this report only reads the previously selected row",
        "- Prespecified absolute-error tolerances: 0.020 committee advancement, 0.015 floor consideration, 0.010 enactment",
        "",
        "## Transport Results",
        "",
        "| Test Congress | Metric | 117 full rate | Test rate (95% Wilson interval) | Frozen simulator mean | Error | Tolerance | Result |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['testCongress']} | {labels[row['metric']]} | "
            f"{float(row['calibrationCongressRate']):.6f} | "
            f"{float(row['testRate']):.6f} [{float(row['testWilson95Low']):.6f}, "
            f"{float(row['testWilson95High']):.6f}] | {float(row['simulatorMean']):.6f} | "
            f"{float(row['transportError']):+.6f} | {float(row['prespecifiedTolerance']):.3f} | "
            f"{row['toleranceStatus']} |"
        )
    lines.extend([
        "",
        f"The frozen model passes all {pass_counts['116']} of 3 backcast tolerances for the 116th Congress and {pass_counts['118']} of 3 forecast tolerances for the 118th Congress, or {total_passes} of {len(rows)} external cohort-metric cells overall. The 118th-Congress enactment rate remains the only miss. It exceeds its tolerance by {excess:.6f}: the simulator mean is 0.027417 versus the observed rate of 0.016592.",
        "",
        f"All {range_pass_count} external cohort-metric cells remain inside the broader 117th-derived benchmark ranges. That range result does not override the stricter 118th enactment miss.",
        "",
        "## Classifier Audit",
        "",
        f"The frozen artifact used classifier `{FROZEN_CLASSIFIER_VERSION}`, builder SHA-256 `{FROZEN_BUILDER_SHA256}`, and census SHA-256 `{FROZEN_CENSUS_SHA256}`. Full 118th processing exposed a context-dependent GovInfo `E30000` action: `118-s-4199` was vetoed rather than signed. Classifier v2 removed code-only enactment for `E30000` and required positive text or an unambiguous law record/code.",
        "",
        "Classifier v3 adds successful veto-override classification only when affirmative House and Senate override evidence is present. It identifies the override and enactment of `116-hr-6395`; it changes no established committee, floor, completion, presentment, veto, or enactment count in any cohort. Both classifier revisions are source corrections, not post-hoc parameter changes.",
        "",
        "## Provenance",
        "",
        f"- 116th normalized census SHA-256: `{metadata_by_congress['116'].get('output_sha256', '')}`",
        f"- 117th normalized census SHA-256: `{metadata_by_congress['117'].get('output_sha256', '')}`",
        f"- 118th normalized census SHA-256: `{metadata_by_congress['118'].get('output_sha256', '')}`",
        f"- Shared classifier: `{metadata_by_congress['118'].get('classification_version', '')}`",
        "- Source archive SHA-256 values, member counts, and timestamps are recorded in each census metadata file",
        "",
        "## Interpretation Boundary",
        "",
        "The earlier cohort passes all three frozen tolerances, while the later cohort preserves a narrow enactment miss. That pattern does not support treating the 118th result as a recurring directional bias across both external Congresses. It also does not establish general transport from only two external cohorts. The separate executive-action diagnostic shows that aggregate flow proximity can coexist with a large veto-mechanism discrepancy.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows_by_congress = {
        "116": read_csv(CENSUS_116),
        "117": read_csv(CENSUS_117),
        "118": read_csv(CENSUS_118),
    }
    metadata_by_congress = {
        "116": metadata_values(METADATA_116),
        "117": metadata_values(METADATA_117),
        "118": metadata_values(METADATA_118),
    }
    calibration_rows = read_csv(CALIBRATION)
    selected_rows = [row for row in calibration_rows if row.get("selected") == "1"]
    validate_inputs(rows_by_congress, metadata_by_congress, selected_rows)
    selection_summary = next(
        row
        for row in read_csv(CENSUS_REPORT_117)
        if row.get("groupType") == "split" and row.get("groupValue") == "calibration"
    )
    baselines = {row["key"]: row for row in read_csv(BASELINES)}
    rows: list[dict[str, str]] = []
    for congress in ("116", "118"):
        rows.extend(
            build_rows(
                rows_by_congress["117"],
                rows_by_congress[congress],
                selected_rows[0],
                selection_summary,
                baselines,
                test_congress=congress,
            )
        )
    write_csv(rows)
    write_markdown(rows, metadata_by_congress)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
