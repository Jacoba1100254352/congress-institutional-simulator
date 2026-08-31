#!/usr/bin/env python3
"""Compare frozen simulator veto behavior with a longer GovInfo decision panel."""

from __future__ import annotations

import csv
from pathlib import Path

try:
    from .write_legislative_lifecycle_temporal_replication import (
        read_csv,
        require,
        wilson_interval,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from write_legislative_lifecycle_temporal_replication import (
        read_csv,
        require,
        wilson_interval,
    )


PANEL = Path("data/validation/raw/govinfo_executive_action_panel.csv")
CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
OUT_CSV = Path("reports/legislative-executive-action-diagnostic.csv")
OUT_MD = Path("reports/legislative-executive-action-diagnostic.md")

CLAIM_BOUNDARY = (
    "This is a descriptive mechanism diagnostic using complete H.R./S. presentment, "
    "veto, override, and enactment classifications for the 108th-118th Congresses. "
    "Party-control and sponsor-party strata are descriptive, selected post-passage "
    "comparisons. This is not a causal model, a presidential-choice calibration, or "
    "evidence about bill quality, welfare, public preferences, or institutional rankings."
)


def rate(successes: int, total: int) -> float:
    return successes / total if total else 0.0


def diagnostic_row(
    source_type: str,
    cohort: str,
    decisions: int,
    enacted: int,
    vetoes: int,
    overrides: int,
    status: str,
    group_type: str = "cohort",
) -> dict[str, str]:
    require(decisions > 0, "Executive-decision denominator must be positive.")
    require(0 <= overrides <= vetoes <= decisions, "Executive-action counts are inconsistent.")
    require(
        decisions == enacted + vetoes - overrides,
        "Executive-decision identity failed.",
    )
    veto_low, veto_high = wilson_interval(vetoes, decisions)
    if vetoes:
        override_rate = f"{rate(overrides, vetoes):.6f}"
        override_low, override_high = wilson_interval(overrides, vetoes)
        override_low_text = f"{override_low:.6f}"
        override_high_text = f"{override_high:.6f}"
    else:
        override_rate = "NA"
        override_low_text = "NA"
        override_high_text = "NA"
    return {
        "sourceType": source_type,
        "groupType": group_type,
        "cohort": cohort,
        "decisionDefinition": (
            "presented_to_president"
            if source_type == "GovInfo panel"
            else "enactedBills + vetoes - overriddenVetoes"
        ),
        "decisionCount": str(decisions),
        "enactedBills": str(enacted),
        "nonVetoEnactments": str(enacted - overrides),
        "vetoes": str(vetoes),
        "overriddenVetoes": str(overrides),
        "conditionalVetoRate": f"{rate(vetoes, decisions):.6f}",
        "conditionalVetoWilson95Low": f"{veto_low:.6f}",
        "conditionalVetoWilson95High": f"{veto_high:.6f}",
        "overrideRateAmongVetoes": override_rate,
        "overrideWilson95Low": override_low_text,
        "overrideWilson95High": override_high_text,
        "conditionalVetoRateDifferenceFromPooledEmpirical": "",
        "conditionalVetoRateRatioToPooledEmpirical": "",
        "diagnosticStatus": status,
    }


def empirical_counts(rows: list[dict[str, str]]) -> tuple[int, int, int, int]:
    presented = len(rows)
    enacted = sum(row.get("enacted") == "1" for row in rows)
    vetoes = sum(row.get("vetoed") == "1" for row in rows)
    overrides = sum(row.get("veto_overridden") == "1" for row in rows)
    require(
        presented == enacted + vetoes - overrides,
        "Empirical executive-decision identity failed.",
    )
    return presented, enacted, vetoes, overrides


def empirical_group_row(
    rows: list[dict[str, str]],
    group_type: str,
    cohort: str,
    status: str,
) -> dict[str, str]:
    return diagnostic_row(
        "GovInfo panel",
        cohort,
        *empirical_counts(rows),
        status,
        group_type,
    )


def build_rows() -> list[dict[str, str]]:
    panel = read_csv(PANEL)
    require(len(panel) == 4021, "Executive-action panel row count drifted.")
    require(
        {row.get("congress") for row in panel} == {str(item) for item in range(108, 119)},
        "Executive-action panel Congress scope drifted.",
    )
    require(
        not any(row.get("integrity_status", "").startswith("invalid:") for row in panel),
        "Executive-action panel contains invalid rows.",
    )
    rows: list[dict[str, str]] = []
    for congress in range(108, 119):
        cohort = [row for row in panel if row["congress"] == str(congress)]
        rows.append(
            empirical_group_row(
                cohort,
                "congress",
                str(congress),
                "empirical_reference_congress",
            )
        )

    for president in dict.fromkeys(row["president"] for row in panel):
        rows.append(
            empirical_group_row(
                [row for row in panel if row["president"] == president],
                "administration",
                president,
                "empirical_reference_administration",
            )
        )

    for control in ("unified", "divided"):
        rows.append(
            empirical_group_row(
                [row for row in panel if row["government_control"] == control],
                "government_control",
                control,
                "descriptive_selected_stratum",
            )
        )

    sponsor_labels = {
        "1": "same-party sponsor",
        "0": "opposition-party sponsor",
        "NA": "other/unknown sponsor",
    }
    for value, label in sponsor_labels.items():
        rows.append(
            empirical_group_row(
                [row for row in panel if row["sponsor_same_party_as_president"] == value],
                "sponsor_party",
                label,
                "descriptive_selected_stratum",
            )
        )

    pooled = empirical_counts(panel)
    pooled_row = diagnostic_row(
        "GovInfo panel",
        "108-118 pooled",
        *pooled,
        "empirical_reference_pooled",
        "pooled",
    )
    rows.append(pooled_row)

    selected_rows = [row for row in read_csv(CALIBRATION) if row.get("selected") == "1"]
    require(len(selected_rows) == 1, "Calibration must contain one selected row.")
    selected = selected_rows[0]
    decisions = int(selected["executiveDecisions"])
    enacted = int(selected["enactedBills"])
    vetoes = int(selected["vetoes"])
    overrides = int(selected["overriddenVetoes"])
    require(decisions == enacted + vetoes - overrides, "Simulator executive-decision identity failed.")
    simulator_row = diagnostic_row(
        "frozen simulator",
        "117-selected 50-seed panel",
        decisions,
        enacted,
        vetoes,
        overrides,
        "large_descriptive_mismatch_no_prespecified_tolerance",
        "simulator",
    )
    pooled_rate = pooled[2] / pooled[0]
    simulator_rate = vetoes / decisions
    simulator_row["conditionalVetoRateDifferenceFromPooledEmpirical"] = (
        f"{simulator_rate - pooled_rate:.6f}"
    )
    simulator_row["conditionalVetoRateRatioToPooledEmpirical"] = (
        f"{simulator_rate / pooled_rate:.3f}" if pooled_rate else ""
    )
    rows.append(simulator_row)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    pooled = next(row for row in rows if row["cohort"] == "108-118 pooled")
    simulator = next(row for row in rows if row["sourceType"] == "frozen simulator")
    divided = next(row for row in rows if row["cohort"] == "divided")
    unified = next(row for row in rows if row["cohort"] == "unified")
    opposition = next(row for row in rows if row["cohort"] == "opposition-party sponsor")
    same_party = next(row for row in rows if row["cohort"] == "same-party sponsor")

    def interval(row: dict[str, str]) -> str:
        return (
            f"{float(row['conditionalVetoRate']):.6f} "
            f"[{float(row['conditionalVetoWilson95Low']):.6f}, "
            f"{float(row['conditionalVetoWilson95High']):.6f}]"
        )

    def override_interval(row: dict[str, str]) -> str:
        if row["overrideRateAmongVetoes"] == "NA":
            return "NA"
        return (
            f"{float(row['overrideRateAmongVetoes']):.6f} "
            f"[{float(row['overrideWilson95Low']):.6f}, "
            f"{float(row['overrideWilson95High']):.6f}]"
        )

    def append_rows(lines: list[str], selected: list[dict[str, str]]) -> None:
        for row in selected:
            lines.append(
                f"| {row['cohort']} | {row['decisionCount']} | {row['vetoes']} | "
                f"{interval(row)} | {row['overriddenVetoes']} | "
                f"{override_interval(row)} |"
            )

    lines = [
        "# Legislative Executive-Action Diagnostic",
        "",
        "Source-aligned diagnostic of presentment, presidential veto, successful override, and enactment in complete 108th-118th-Congress H.R./S. GovInfo archives and the frozen selected workflow panel.",
        "",
        "## Denominator Alignment",
        "",
        "- The committed panel parses all 126,760 H.R./S. source records and retains the 4,021 measures classified as presented to the President.",
        "- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. This avoids double-counting bills enacted over a veto.",
        "- In every empirical cohort, presentments equal enactments plus vetoes minus overrides, so the two denominators describe the same decision point.",
        "- The exact 21-bill veto set, veto dates, regular or disputed-return pocket-veto labels, and six successful overrides match an independently compiled official Senate reference.",
        "- Joint resolutions are excluded because the lifecycle calibration is scoped to H.R. and S. measures. Their distinct recent veto incidence must be modeled as a separate measure class before broader presidential-veto claims are made.",
        "- Veto and override diagnostics do not participate in calendar-threshold selection or alter any frozen tolerance.",
        "",
        "## Pooled Comparison",
        "",
        "| Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    append_rows(lines, [pooled, simulator])
    lines.extend([
        "",
        "## Congress Results",
        "",
        "| Congress | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(lines, [row for row in rows if row["groupType"] == "congress"])
    lines.extend([
        "",
        "## Descriptive Strata",
        "",
        "| Stratum | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(
        lines,
        [
            row
            for row in rows
            if row["groupType"] in {"administration", "government_control", "sponsor_party"}
        ],
    )
    control_ratio = (
        (int(divided["vetoes"]) / int(divided["decisionCount"]))
        / (int(unified["vetoes"]) / int(unified["decisionCount"]))
    )
    sponsor_ratio = (
        (int(opposition["vetoes"]) / int(opposition["decisionCount"]))
        / (int(same_party["vetoes"]) / int(same_party["decisionCount"]))
    )
    lines.extend([
        "",
        "## Findings",
        "",
        f"The complete empirical panel contains {pooled['vetoes']} vetoes in {pooled['decisionCount']} H.R./S. presentments, a conditional rate of {float(pooled['conditionalVetoRate']):.6f}. The frozen selected panel produces {simulator['vetoes']} vetoes in {simulator['decisionCount']} executive decisions, a rate of {float(simulator['conditionalVetoRate']):.6f}. The absolute difference is {float(simulator['conditionalVetoRateDifferenceFromPooledEmpirical']):.6f}, and the simulator rate is {float(simulator['conditionalVetoRateRatioToPooledEmpirical']):.3f} times the pooled empirical rate.",
        "The difference and ratio are computed from the integer event counts before rates are rounded to six decimals for display.",
        "",
        "The Wilson intervals do not overlap. That makes the mechanism discrepancy too large to hide behind the aggregate enactment fit. No veto-specific tolerance was prespecified, so this report preserves the result as a descriptive diagnostic rather than relabeling it as a formal held-out pass or failure.",
        "",
        f"Divided-government Congresses contain {divided['vetoes']} vetoes in {divided['decisionCount']} decisions versus {unified['vetoes']} in {unified['decisionCount']} under unified government, an unadjusted rate ratio of {control_ratio:.3f}. Opposite-party sponsors account for {opposition['vetoes']} vetoes in {opposition['decisionCount']} decisions versus {same_party['vetoes']} in {same_party['decisionCount']} for same-party sponsors, an unadjusted rate ratio of {sponsor_ratio:.3f}.",
        "These strata are selected after congressional passage, overlap with administration and issue mix, and omit final-vote support. They identify variables a future model must represent; they do not estimate causal party-control or sponsor-party effects.",
        "",
        f"The panel contains {pooled['vetoes']} vetoes and {pooled['overriddenVetoes']} successful overrides. That is materially stronger than the earlier three-veto diagnostic but remains sparse for a flexible presidential-choice model or stable override calibration.",
        "",
        "## Model Boundary And Next Gate",
        "",
        "The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can be produced while the internal executive-action pathway is wrong.",
        "",
        "The next gate is a separately frozen presidential-choice study. It should add joint resolutions as a distinct measure class, link final House and Senate vote support, encode administration and party control without treating sponsor party as policy distance, specify a low-event estimator and calibration loss before fitting, and reserve whole Congresses for temporal testing. The current flow threshold and transport tolerances remain frozen.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
