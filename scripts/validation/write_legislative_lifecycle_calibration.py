#!/usr/bin/env python3
"""Select and report the current-Congress workflow calendar threshold."""

from __future__ import annotations

import csv
import os
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[2]
CENSUS_REPORT = ROOT / "reports" / "govinfo-bill-census.csv"
OUT_CSV = ROOT / "reports" / "legislative-lifecycle-calibration.csv"
OUT_MD = ROOT / "reports" / "legislative-lifecycle-calibration.md"

SEED_BASE = 117_000_001
SEED_STEP = 104_729
SEED_COUNT = 50
SEEDS = tuple(SEED_BASE + (SEED_STEP * index) for index in range(SEED_COUNT))
RUNS_PER_SEED = 24
CANDIDATES = tuple(round(value / 100, 2) for value in range(60, 75))
METRICS = (
    ("committeeAdvanceRate", "committeeAdvancedRate", 0.020),
    ("floorConsiderationRate", "floorConsideredRate", 0.015),
    ("enactmentRate", "enactedRate", 0.010),
)
SELECTION_METRICS = {"floorConsiderationRate", "enactmentRate"}

CLAIM_BOUNDARY = (
    "This procedure reports three aggregate flow rates for one stylized workflow and "
    "selects one downstream calendar threshold against two of them using a deterministic "
    "split of one Congress. It does not validate causal mechanisms, bill quality, public "
    "preferences, welfare, or institutional rankings, and the within-Congress held-out "
    "split is not temporal validation."
)


def read_census_targets() -> dict[str, dict[str, float]]:
    if not CENSUS_REPORT.exists():
        raise SystemExit(f"Missing {CENSUS_REPORT}; run make govinfo-bill-census.")
    with CENSUS_REPORT.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    targets: dict[str, dict[str, float]] = {}
    for split in ("calibration", "heldout"):
        row = next(
            (
                item
                for item in rows
                if item.get("groupType") == "split" and item.get("groupValue") == split
            ),
            None,
        )
        if row is None:
            raise SystemExit(f"Missing {split} split in {CENSUS_REPORT}.")
        targets[split] = {
            empirical_field: float(row[empirical_field])
            for _, empirical_field, _ in METRICS
        }
    return targets


def run_probe() -> list[dict[str, str]]:
    app_cp = os.environ.get("APP_CP", "out/congresssim.jar")
    java_props = shlex.split(os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21"))
    command = [
        "java",
        *java_props,
        "-cp",
        app_cp,
        "congresssim.simulation.catalog.CurrentCongressWorkflowCalibrationProbe",
        str(RUNS_PER_SEED),
        ",".join(str(seed) for seed in SEEDS),
        ",".join(f"{candidate:.2f}" for candidate in CANDIDATES),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return list(csv.DictReader(completed.stdout.splitlines()))


def aggregate(
    rows: list[dict[str, str]],
    calibration_targets: dict[str, float],
    *,
    enforce_model_default: bool = True,
) -> list[dict[str, str]]:
    by_threshold: dict[float, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_threshold[float(row["threshold"])].append(row)

    output: list[dict[str, str]] = []
    for threshold in sorted(by_threshold):
        candidate_rows = by_threshold[threshold]
        result: dict[str, str] = {
            "calendarPriorityThreshold": f"{threshold:.3f}",
            "seedCount": str(len(candidate_rows)),
            "runsPerSeed": candidate_rows[0]["runs"],
            "simulatedBills": str(sum(int(row["bills"]) for row in candidate_rows)),
            "defaultThreshold": candidate_rows[0]["defaultThreshold"],
        }
        fit_error = 0.0
        for simulator_field, empirical_field, tolerance in METRICS:
            observed = mean(float(row[simulator_field]) for row in candidate_rows)
            target = calibration_targets[empirical_field]
            error = observed - target
            result[simulator_field] = f"{observed:.6f}"
            result[f"{simulator_field}CalibrationError"] = f"{error:.6f}"
            if simulator_field in SELECTION_METRICS:
                fit_error += (error / tolerance) ** 2
        result["calendarCapacityDenialRate"] = f"{mean(float(row['calendarCapacityDenialRate']) for row in candidate_rows):.6f}"
        enacted_bills = sum(int(row["enactedBills"]) for row in candidate_rows)
        vetoes = sum(int(row["vetoes"]) for row in candidate_rows)
        overridden_vetoes = sum(int(row["overriddenVetoes"]) for row in candidate_rows)
        executive_decisions = sum(int(row["executiveDecisions"]) for row in candidate_rows)
        result["enactedBills"] = str(enacted_bills)
        result["vetoes"] = str(vetoes)
        result["overriddenVetoes"] = str(overridden_vetoes)
        result["executiveDecisions"] = str(executive_decisions)
        result["conditionalVetoRate"] = (
            f"{vetoes / executive_decisions:.6f}" if executive_decisions else "0.000000"
        )
        result["overrideRateAmongVetoes"] = (
            f"{overridden_vetoes / vetoes:.6f}" if vetoes else "0.000000"
        )
        result["standardizedSquaredError"] = f"{fit_error:.6f}"
        result["selected"] = "0"
        output.append(result)

    selected = min(
        output,
        key=lambda row: (
            float(row["standardizedSquaredError"]),
            float(row["calendarPriorityThreshold"]),
        ),
    )
    selected["selected"] = "1"
    if (
        enforce_model_default
        and float(selected["calendarPriorityThreshold"]) != float(selected["defaultThreshold"])
    ):
        raise SystemExit(
            "Selected calendar threshold does not match the model default: "
            f"selected={selected['calendarPriorityThreshold']}, default={selected['defaultThreshold']}"
        )
    return output


def leave_one_seed_out_selections(
    probe_rows: list[dict[str, str]],
    calibration_targets: dict[str, float],
) -> Counter[str]:
    seeds = sorted({row["seed"] for row in probe_rows}, key=int)
    selections: Counter[str] = Counter()
    for omitted_seed in seeds:
        rows = aggregate(
            [row for row in probe_rows if row["seed"] != omitted_seed],
            calibration_targets,
            enforce_model_default=False,
        )
        selected = next(row for row in rows if row["selected"] == "1")
        selections[selected["calendarPriorityThreshold"]] += 1
    return selections


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    rows: list[dict[str, str]],
    targets: dict[str, dict[str, float]],
    leave_one_out: Counter[str],
) -> None:
    selected = next(row for row in rows if row["selected"] == "1")
    selected_threshold = selected["calendarPriorityThreshold"]
    stable_reselections = leave_one_out[selected_threshold]
    lines = [
        "# Legislative Lifecycle Calibration",
        "",
        "Deterministic calibration-only parameter sweep for the stylized current-Congress workflow.",
        "",
        "## Selection Protocol",
        "",
        f"- Candidate calendar-priority thresholds: {CANDIDATES[0]:.2f} through {CANDIDATES[-1]:.2f} in 0.01 steps",
        f"- Fixed simulator seed panel: {SEED_COUNT} seeds defined by `{SEED_BASE} + ({SEED_STEP} * index)` for indices 0 through {SEED_COUNT - 1}",
        f"- Runs per seed: {RUNS_PER_SEED}",
        f"- Simulated bills per candidate: {selected['simulatedBills']}",
        "- Selection data: calibration half of the 117th-Congress H.R./S. census only",
        "- Selection criterion: sum of squared errors standardized by tolerances of 0.015 for floor consideration and 0.010 for enactment",
        "- Committee advancement is reported as an upstream workflow check and does not enter calendar-threshold selection",
        "- Held-out use: reported only after threshold selection; it does not participate in the fit criterion",
        f"- Leave-one-seed-out stability: {stable_reselections} / {SEED_COUNT} panels reselected {float(selected_threshold):.2f}",
        "",
        f"Selected and model-default threshold: **{float(selected['calendarPriorityThreshold']):.2f}**.",
        "",
        "## Selected Fit",
        "",
        "| Metric | Calibration target | Simulator mean | Calibration error | Held-out target | Held-out error |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for simulator_field, empirical_field, _ in METRICS:
        simulated = float(selected[simulator_field])
        calibration = targets["calibration"][empirical_field]
        heldout = targets["heldout"][empirical_field]
        lines.append(
            f"| {simulator_field} | {calibration:.6f} | {simulated:.6f} | "
            f"{simulated - calibration:+.6f} | {heldout:.6f} | {simulated - heldout:+.6f} |"
        )
    lines.extend(
        [
            "",
            "## Executive-Action Diagnostic",
            "",
            f"- Enacted bills: {selected['enactedBills']}",
            f"- Veto events: {selected['vetoes']}",
            f"- Successful overrides: {selected['overriddenVetoes']}",
            f"- Executive decisions: {selected['executiveDecisions']} (enactments plus vetoes minus overridden vetoes)",
            f"- Conditional veto rate: {float(selected['conditionalVetoRate']):.6f}",
            f"- Override rate among vetoes: {float(selected['overrideRateAmongVetoes']):.6f}",
            "",
            "These quantities are diagnostics only. They do not enter threshold selection, which remains frozen to floor consideration and enactment on the 117th calibration split.",
            "",
            "## Candidate Grid",
            "",
            "| Threshold | Committee advance | Floor | Enactment | Calendar denial | Standardized squared error | Selected |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {float(row['calendarPriorityThreshold']):.2f} | "
            f"{float(row['committeeAdvanceRate']):.6f} | "
            f"{float(row['floorConsiderationRate']):.6f} | "
            f"{float(row['enactmentRate']):.6f} | "
            f"{float(row['calendarCapacityDenialRate']):.6f} | "
            f"{float(row['standardizedSquaredError']):.6f} | "
            f"{'yes' if row['selected'] == '1' else 'no'} |"
        )
    lines.extend(["", "## Claim Boundary", "", CLAIM_BOUNDARY, ""])
    OUT_MD.write_text("\n".join(lines))


def main() -> int:
    targets = read_census_targets()
    probe_rows = run_probe()
    rows = aggregate(probe_rows, targets["calibration"])
    leave_one_out = leave_one_seed_out_selections(probe_rows, targets["calibration"])
    write_csv(rows)
    write_markdown(rows, targets, leave_one_out)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
