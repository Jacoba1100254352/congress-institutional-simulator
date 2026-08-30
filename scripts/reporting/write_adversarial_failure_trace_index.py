#!/usr/bin/env python3
"""Write aggregate pilot failure-trace candidates from manipulation stress output."""

from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("reports/simulation-manipulation-stress.csv")
OUT_CSV = Path("reports/adversarial-failure-trace-index.csv")
OUT_MD = Path("reports/adversarial-failure-trace-index.md")

CLAIM_BOUNDARY = (
    "Aggregate pilot failure-trace index only; rows compare bounded manipulation-stress "
    "aggregate cells against reference cells from the same campaign. This is not a "
    "per-bill action log, not a budget sweep, not an attack success rate, not recovery "
    "evidence, not empirical adversary validation, and not evidence for real-world "
    "institutional ranking."
)

MISSING_FOR_FULL_TRACE = (
    "explicit budget; information level; same-seed per-run baseline pairing; "
    "per-bill attack action log; recovery/correction event log; attack success rate; "
    "seed sensitivity"
)

TESTS = [
    {
        "attack_family": "clone_decoy_pressure",
        "adversary_id": "A1",
        "test": "Policy tournament clone/decoy attack",
        "actor_model": "clone/decoy proposer",
        "objective": "lower selected-alternative quality or move outcomes through strategic alternatives",
        "reference_case": "clone-decoy-pressure",
        "reference_scenario": "simple-majority-alternatives-pairwise",
        "stressed_case": "clone-decoy-pressure",
        "stressed_scenario": "simple-majority-alternatives-strategic",
        "stressor": "strategic clone and decoy variant",
    },
    {
        "attack_family": "public_input_manipulation",
        "adversary_id": "A3",
        "test": "Citizen-panel manipulation",
        "actor_model": "public-input manipulator",
        "objective": "distort citizen-panel certification and legitimacy signals",
        "reference_case": "capture-flooding",
        "reference_scenario": "citizen-assembly-threshold",
        "stressed_case": "capture-flooding",
        "stressed_scenario": "citizen-assembly-manipulation-stress",
        "stressor": "smaller, noisier, more manipulable panel",
    },
    {
        "attack_family": "bad_faith_harm_claims",
        "adversary_id": "A4",
        "test": "Bad-faith harm claims",
        "actor_model": "bad-faith harm claimant",
        "objective": "increase false-positive review pressure or let concentrated harm pass",
        "reference_case": "rights-harm-pressure",
        "reference_scenario": "harm-weighted-majority",
        "stressed_case": "rights-harm-pressure",
        "stressed_scenario": "harm-weighted-loose-claims-majority",
        "stressor": "lower harm threshold creates more false-positive review pressure",
    },
    {
        "attack_family": "astroturf_objection_pressure",
        "adversary_id": "A3/A8",
        "test": "Astroturf objection pressure",
        "actor_model": "public-input manipulator and public-support distortion actor",
        "objective": "distort objection-window signals and increase process burden",
        "reference_case": "capture-flooding",
        "reference_scenario": "public-objection-majority",
        "stressed_case": "capture-flooding",
        "stressed_scenario": "public-objection-astroturf-majority",
        "stressor": "lower objection threshold and higher noise",
    },
    {
        "attack_family": "proposal_flooding",
        "adversary_id": "A5",
        "test": "Agenda flooding",
        "actor_model": "proposal flooder",
        "objective": "crowd agenda capacity and degrade output quality",
        "reference_case": "baseline",
        "reference_scenario": "agenda-lottery-majority",
        "stressed_case": "proposal-flooding",
        "stressed_scenario": "agenda-lottery-majority",
        "stressor": "same agenda lottery under proposal flooding",
    },
    {
        "attack_family": "defensive_lobbying_backlash",
        "adversary_id": "A6",
        "test": "Anti-capture defensive backlash",
        "actor_model": "defensive lobbying actor",
        "objective": "weaken anti-capture reforms through defensive organized-interest pressure",
        "reference_case": "baseline",
        "reference_scenario": "anti-capture-majority-bundle",
        "stressed_case": "anti-lobbying-backlash",
        "stressed_scenario": "anti-capture-majority-bundle",
        "stressor": "same anti-capture bundle under defensive lobbying backlash",
    },
    {
        "attack_family": "burden_shifting_capture_flooding",
        "adversary_id": "A9/deferred",
        "test": "Open burden-shifting capture stress",
        "actor_model": "mixed capture and flooding actor",
        "objective": "increase weakly supported throughput under capture and proposal pressure",
        "reference_case": "baseline",
        "reference_scenario": "default-pass",
        "stressed_case": "capture-flooding",
        "stressed_scenario": "default-pass",
        "stressor": "throughput stress test under capture and flooding",
    },
]

FIELDNAMES = [
    "trace_rank",
    "adversary_id",
    "attack_family",
    "test",
    "actor_model",
    "objective",
    "budget_level",
    "information_level",
    "reference_case",
    "stressed_case",
    "reference_scenario",
    "stressed_scenario",
    "stressor",
    "directional_loss",
    "revision_moderation_loss",
    "weak_mandate_added",
    "admin_cost_added",
    "risk_control_loss",
    "productivity_loss",
    "public_support_loss",
    "policy_yield_loss",
    "leading_failure_metric",
    "pilot_success_flag",
    "severity",
    "observed_path_summary",
    "missing_for_full_trace",
    "evidence_source",
    "claim_boundary",
]


def read_rows() -> dict[tuple[str, str], dict[str, str]]:
    if not INPUT.exists():
        raise SystemExit(f"{INPUT} is missing. Run make manipulation-stress first.")
    with INPUT.open(newline="") as handle:
        return {(row["caseKey"], row["scenarioKey"]): row for row in csv.DictReader(handle)}


def as_float(row: dict[str, str], field: str) -> float:
    try:
        return float(row.get(field, "0") or "0")
    except ValueError:
        return 0.0


def fmt(value: float) -> str:
    return f"{value:.6f}"


def leading_metric(metrics: dict[str, float]) -> str:
    positive = {key: value for key, value in metrics.items() if value > 0}
    if not positive:
        return "none"
    return max(positive.items(), key=lambda item: item[1])[0]


def pilot_success(metrics: dict[str, float]) -> bool:
    return (
        metrics["directional_loss"] >= 0.02
        or metrics["weak_mandate_added"] >= 0.02
        or metrics["risk_control_loss"] >= 0.02
        or metrics["admin_cost_added"] >= 0.05
        or metrics["policy_yield_loss"] >= 0.02
        or metrics["public_support_loss"] >= 0.02
    )


def severity(metrics: dict[str, float], success: bool) -> str:
    if metrics["directional_loss"] >= 0.05 or metrics["weak_mandate_added"] >= 0.05:
        return "material_pilot_degradation"
    if metrics["admin_cost_added"] >= 0.08:
        return "process_cost_degradation"
    if success:
        return "bounded_pilot_degradation"
    if metrics["directional_loss"] <= -0.02:
        return "stress_variant_improves_aggregate_profile"
    return "limited_or_no_observed_degradation"


def path_summary(test: dict[str, str], ref: dict[str, str], stress: dict[str, str], metrics: dict[str, float]) -> str:
    if test["attack_family"] == "clone_decoy_pressure":
        return (
            "Strategic-alternative variant changes aggregate selection diagnostics: "
            f"strategic decoy rate {as_float(ref, 'strategicDecoyRate'):.3f} -> "
            f"{as_float(stress, 'strategicDecoyRate'):.3f}; "
            f"selected-alternative median distance {as_float(ref, 'selectedAlternativeMedianDistance'):.3f} -> "
            f"{as_float(stress, 'selectedAlternativeMedianDistance'):.3f}."
        )
    if test["attack_family"] == "public_input_manipulation":
        return (
            "Manipulated citizen-panel variant changes public-review diagnostics: "
            f"citizen review rate {as_float(ref, 'citizenReviewRate'):.3f} -> "
            f"{as_float(stress, 'citizenReviewRate'):.3f}; "
            f"citizen legitimacy {as_float(ref, 'citizenLegitimacy'):.3f} -> "
            f"{as_float(stress, 'citizenLegitimacy'):.3f}."
        )
    if test["attack_family"] == "bad_faith_harm_claims":
        return (
            "Loose-claims variant changes harm-screen diagnostics: "
            f"minority harm {as_float(ref, 'minorityHarm'):.3f} -> {as_float(stress, 'minorityHarm'):.3f}; "
            f"concentrated-harm passage {as_float(ref, 'concentratedHarmPassage'):.3f} -> "
            f"{as_float(stress, 'concentratedHarmPassage'):.3f}."
        )
    if test["attack_family"] == "astroturf_objection_pressure":
        return (
            "Astroturf objection variant changes objection-window diagnostics: "
            f"objection-window rate {as_float(ref, 'objectionWindowRate'):.3f} -> "
            f"{as_float(stress, 'objectionWindowRate'):.3f}; "
            f"cheap signal distortion {as_float(ref, 'cheapSignalDistortion'):.3f} -> "
            f"{as_float(stress, 'cheapSignalDistortion'):.3f}."
        )
    if test["attack_family"] == "proposal_flooding":
        return (
            "Proposal-flooding case changes agenda-lottery diagnostics: "
            f"floor per run {as_float(ref, 'floorPerRun'):.3f} -> {as_float(stress, 'floorPerRun'):.3f}; "
            f"policy yield {as_float(ref, 'policyYield'):.3f} -> {as_float(stress, 'policyYield'):.3f}."
        )
    if test["attack_family"] == "defensive_lobbying_backlash":
        return (
            "Defensive-lobbying case changes anti-capture diagnostics: "
            f"defensive lobbying share {as_float(ref, 'defensiveLobbyingShare'):.3f} -> "
            f"{as_float(stress, 'defensiveLobbyingShare'):.3f}; "
            f"lobby capture {as_float(ref, 'lobbyCapture'):.3f} -> {as_float(stress, 'lobbyCapture'):.3f}."
        )
    return (
        "Capture/flooding case changes open burden-shifting diagnostics: "
        f"weak mandate passage {as_float(ref, 'weakPublicMandatePassage'):.3f} -> "
        f"{as_float(stress, 'weakPublicMandatePassage'):.3f}; "
        f"policy shift {as_float(ref, 'policyShift'):.3f} -> {as_float(stress, 'policyShift'):.3f}."
    )


def build_rows(index: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for test in TESTS:
        ref = index.get((test["reference_case"], test["reference_scenario"]))
        stress = index.get((test["stressed_case"], test["stressed_scenario"]))
        if not ref or not stress:
            continue
        metrics = {
            "directional_loss": as_float(ref, "directionalScore") - as_float(stress, "directionalScore"),
            "revision_moderation_loss": as_float(ref, "compromise") - as_float(stress, "compromise"),
            "weak_mandate_added": as_float(stress, "weakPublicMandatePassage") - as_float(ref, "weakPublicMandatePassage"),
            "admin_cost_added": as_float(stress, "administrativeCost") - as_float(ref, "administrativeCost"),
            "risk_control_loss": as_float(ref, "riskControl") - as_float(stress, "riskControl"),
            "productivity_loss": as_float(ref, "productivity") - as_float(stress, "productivity"),
            "public_support_loss": as_float(ref, "avgSupport") - as_float(stress, "avgSupport"),
            "policy_yield_loss": as_float(ref, "policyYield") - as_float(stress, "policyYield"),
        }
        success = pilot_success(metrics)
        rows.append({
            "trace_rank": "",
            "adversary_id": test["adversary_id"],
            "attack_family": test["attack_family"],
            "test": test["test"],
            "actor_model": test["actor_model"],
            "objective": test["objective"],
            "budget_level": "pilot_not_budgeted",
            "information_level": "pilot_not_modeled",
            "reference_case": test["reference_case"],
            "stressed_case": test["stressed_case"],
            "reference_scenario": test["reference_scenario"],
            "stressed_scenario": test["stressed_scenario"],
            "stressor": test["stressor"],
            "directional_loss": fmt(metrics["directional_loss"]),
            "revision_moderation_loss": fmt(metrics["revision_moderation_loss"]),
            "weak_mandate_added": fmt(metrics["weak_mandate_added"]),
            "admin_cost_added": fmt(metrics["admin_cost_added"]),
            "risk_control_loss": fmt(metrics["risk_control_loss"]),
            "productivity_loss": fmt(metrics["productivity_loss"]),
            "public_support_loss": fmt(metrics["public_support_loss"]),
            "policy_yield_loss": fmt(metrics["policy_yield_loss"]),
            "leading_failure_metric": leading_metric(metrics),
            "pilot_success_flag": "yes" if success else "no",
            "severity": severity(metrics, success),
            "observed_path_summary": path_summary(test, ref, stress, metrics),
            "missing_for_full_trace": MISSING_FOR_FULL_TRACE,
            "evidence_source": str(INPUT),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    rows.sort(
        key=lambda row: (
            row["pilot_success_flag"] != "yes",
            -float(row["directional_loss"]),
            -float(row["weak_mandate_added"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["trace_rank"] = str(index)
    return rows


def md_escape(value: str) -> str:
    return value.replace("|", "\\|")


def write_outputs(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit("No adversarial pilot trace rows built.")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    pilot_success_rows = [row for row in rows if row["pilot_success_flag"] == "yes"]
    material_rows = [row for row in rows if row["severity"] == "material_pilot_degradation"]
    lines = [
        "# Adversarial Failure Trace Index",
        "",
        "This report converts the existing manipulation-stress aggregate comparisons into pilot trace candidates for the robustness/failure-mode breakout. It is an index of where to collect full traces next, not a substitute for explicit adversary experiments.",
        "",
        f"- Pilot trace candidates: {len(rows)}",
        f"- Pilot success flags: {len(pilot_success_rows)}",
        f"- Material pilot degradation rows: {len(material_rows)}",
        "- Budget coverage: pilot_not_budgeted",
        "- Information coverage: pilot_not_modeled",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Trace candidates:",
        "",
        "| Rank | Adversary | Test | Reference | Stressed | Leading metric | Directional loss | Weak mandate added | Severity |",
        "| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['trace_rank']} | {row['adversary_id']} | {md_escape(row['test'])} | "
            f"`{row['reference_case']} / {row['reference_scenario']}` | "
            f"`{row['stressed_case']} / {row['stressed_scenario']}` | "
            f"{row['leading_failure_metric']} | {float(row['directional_loss']):.3f} | "
            f"{float(row['weak_mandate_added']):.3f} | {row['severity']} |"
        )
    lines.extend([
        "",
        "Missing before manuscript-grade traces:",
        "",
        f"- {MISSING_FOR_FULL_TRACE}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    write_outputs(build_rows(read_rows()))
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
