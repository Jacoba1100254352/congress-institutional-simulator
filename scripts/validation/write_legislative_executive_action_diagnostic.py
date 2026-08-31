#!/usr/bin/env python3
"""Compare frozen simulator veto behavior with GovInfo presidential decisions."""

from __future__ import annotations

import csv
from collections import defaultdict
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


BILL_PANEL = Path("data/validation/raw/govinfo_executive_action_panel.csv")
JOINT_PANEL = Path("data/validation/raw/govinfo_joint_resolution_panel.csv")
FINAL_VOTE_PANEL = Path("data/validation/raw/govinfo_final_chamber_vote_panel.csv")
CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
OUT_CSV = Path("reports/legislative-executive-action-diagnostic.csv")
OUT_MD = Path("reports/legislative-executive-action-diagnostic.md")

BILL_POOLED = "108-118 H.R./S. bills"
JOINT_POOLED = "108-118 joint resolutions"
COMBINED_POOLED = "108-118 all presented measures"

CLAIM_BOUNDARY = (
    "This is a descriptive mechanism diagnostic using complete H.R./S. and "
    "separately labeled H.J.Res./S.J.Res. presidential decisions for the "
    "108th-118th Congresses. Final-vote support and party strata are observed "
    "after congressional passage, and missing roll calls are retained process "
    "outcomes rather than imputed support. This is not a causal model, a "
    "presidential-choice calibration, or evidence about bill quality, welfare, "
    "public preferences, or institutional rankings."
)


def rate(successes: int, total: int) -> float:
    return successes / total if total else 0.0


def diagnostic_row(
    source_type: str,
    measure_class: str,
    cohort: str,
    decisions: int,
    enacted: int,
    vetoes: int,
    overrides: int,
    status: str,
    group_type: str = "cohort",
    subset_definition: str = "",
) -> dict[str, str]:
    require(decisions > 0, "Executive-decision denominator must be positive.")
    require(0 <= overrides <= vetoes <= decisions, "Executive-action counts are inconsistent.")
    require(decisions == enacted + vetoes - overrides, "Executive-decision identity failed.")
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
        "measureClass": measure_class,
        "groupType": group_type,
        "cohort": cohort,
        "subsetDefinition": subset_definition,
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
    measure_class: str,
    group_type: str,
    cohort: str,
    status: str,
    subset_definition: str = "",
) -> dict[str, str]:
    return diagnostic_row(
        "GovInfo panel",
        measure_class,
        cohort,
        *empirical_counts(rows),
        status,
        group_type,
        subset_definition,
    )


def recorded(row: dict[str, str]) -> bool:
    return row.get("selection_status") == "official_roll_call_selected"


def at_least_two_thirds(row: dict[str, str]) -> bool:
    yea = int(row["yea_count"])
    nay = int(row["nay_count"])
    return 3 * yea >= 2 * (yea + nay)


def opposition_majority(row: dict[str, str]) -> bool:
    return int(row["opposition_party_yea"]) >= int(row["opposition_party_nay"])


def final_vote_subsets(
    decisions: list[dict[str, str]],
    vote_rows: list[dict[str, str]],
) -> tuple[
    dict[str, list[dict[str, str]]],
    dict[str, list[dict[str, str]]],
    dict[str, list[dict[str, str]]],
]:
    require(len(vote_rows) == 2 * len(decisions), "Final-vote panel row count drifted.")
    by_bill: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in vote_rows:
        by_bill[row["bill_id"]].append(row)
    require(set(by_bill) == {row["bill_id"] for row in decisions}, "Final-vote population drifted.")

    coverage: dict[str, list[dict[str, str]]] = {
        "both final roll calls": [],
        "House final roll only": [],
        "Senate final roll only": [],
        "no final roll calls": [],
    }
    minimum_support: dict[str, list[dict[str, str]]] = {
        "both chambers at least two-thirds": [],
        "one or both chambers below two-thirds": [],
    }
    opposition_support: dict[str, list[dict[str, str]]] = {
        "opposition majority in both chambers": [],
        "opposition below majority in one or both chambers": [],
    }

    for decision in decisions:
        chamber_rows = {row["chamber"]: row for row in by_bill[decision["bill_id"]]}
        require(set(chamber_rows) == {"House", "Senate"}, f"{decision['bill_id']} chamber pair drifted.")
        house_recorded = recorded(chamber_rows["House"])
        senate_recorded = recorded(chamber_rows["Senate"])
        if house_recorded and senate_recorded:
            coverage["both final roll calls"].append(decision)
            if all(at_least_two_thirds(chamber_rows[chamber]) for chamber in ("House", "Senate")):
                minimum_support["both chambers at least two-thirds"].append(decision)
            else:
                minimum_support["one or both chambers below two-thirds"].append(decision)
            if all(opposition_majority(chamber_rows[chamber]) for chamber in ("House", "Senate")):
                opposition_support["opposition majority in both chambers"].append(decision)
            else:
                opposition_support["opposition below majority in one or both chambers"].append(decision)
        elif house_recorded:
            coverage["House final roll only"].append(decision)
        elif senate_recorded:
            coverage["Senate final roll only"].append(decision)
        else:
            coverage["no final roll calls"].append(decision)

    require(sum(len(rows) for rows in coverage.values()) == len(decisions), "Vote coverage partition failed.")
    both_count = len(coverage["both final roll calls"])
    require(sum(len(rows) for rows in minimum_support.values()) == both_count, "Support partition failed.")
    require(sum(len(rows) for rows in opposition_support.values()) == both_count, "Party-support partition failed.")
    return coverage, minimum_support, opposition_support


def build_rows() -> list[dict[str, str]]:
    bill_panel = read_csv(BILL_PANEL)
    joint_panel = read_csv(JOINT_PANEL)
    require(len(bill_panel) == 4021, "Bill executive-action panel row count drifted.")
    require(len(joint_panel) == 187, "Joint-resolution panel row count drifted.")
    require(
        {row.get("congress") for row in bill_panel + joint_panel}
        == {str(item) for item in range(108, 119)},
        "Executive-action panel Congress scope drifted.",
    )
    require(
        not any(
            row.get("integrity_status", "").startswith("invalid:")
            for row in bill_panel + joint_panel
        ),
        "Executive-action panel contains invalid rows.",
    )
    all_decisions = bill_panel + joint_panel
    require(
        len({row["bill_id"] for row in all_decisions}) == len(all_decisions),
        "Executive-action panel bill IDs overlap.",
    )

    rows: list[dict[str, str]] = []
    for congress in range(108, 119):
        cohort = [row for row in bill_panel if row["congress"] == str(congress)]
        rows.append(
            empirical_group_row(
                cohort,
                "bill",
                "congress",
                str(congress),
                "empirical_reference_bill_congress",
            )
        )

    for president in dict.fromkeys(row["president"] for row in bill_panel):
        rows.append(
            empirical_group_row(
                [row for row in bill_panel if row["president"] == president],
                "bill",
                "administration",
                president,
                "descriptive_bill_stratum",
            )
        )

    for control in ("unified", "divided"):
        rows.append(
            empirical_group_row(
                [row for row in bill_panel if row["government_control"] == control],
                "bill",
                "government_control",
                control,
                "descriptive_bill_stratum",
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
                [row for row in bill_panel if row["sponsor_same_party_as_president"] == value],
                "bill",
                "sponsor_party",
                label,
                "descriptive_bill_stratum",
            )
        )

    bill_pooled = empirical_counts(bill_panel)
    rows.append(
        diagnostic_row(
            "GovInfo panel",
            "bill",
            BILL_POOLED,
            *bill_pooled,
            "empirical_reference_bill_class",
            "measure_class",
            "H.R. and S. measures only",
        )
    )
    rows.append(
        diagnostic_row(
            "GovInfo panel",
            "joint_resolution",
            JOINT_POOLED,
            *empirical_counts(joint_panel),
            "empirical_reference_joint_resolution_class",
            "measure_class",
            "H.J.Res. and S.J.Res. measures presented to the President",
        )
    )
    combined_counts = empirical_counts(all_decisions)
    rows.append(
        diagnostic_row(
            "GovInfo panel",
            "all_presented_measures",
            COMBINED_POOLED,
            *combined_counts,
            "empirical_reference_combined",
            "pooled",
            "H.R. S. H.J.Res. and S.J.Res. presentments",
        )
    )

    coverage, minimum_support, opposition_support = final_vote_subsets(
        all_decisions,
        read_csv(FINAL_VOTE_PANEL),
    )
    for label, cohort in coverage.items():
        rows.append(
            empirical_group_row(
                cohort,
                "all_presented_measures",
                "final_vote_coverage",
                label,
                "descriptive_final_vote_coverage",
                label,
            )
        )
    for label, cohort in minimum_support.items():
        rows.append(
            empirical_group_row(
                cohort,
                "all_presented_measures",
                "both_recorded_minimum_support",
                label,
                "descriptive_both_recorded_support_stratum",
                "both chambers recorded; threshold uses yea divided by yea plus nay",
            )
        )
    for label, cohort in opposition_support.items():
        rows.append(
            empirical_group_row(
                cohort,
                "all_presented_measures",
                "both_recorded_opposition_support",
                label,
                "descriptive_both_recorded_opposition_support_stratum",
                "both chambers recorded; opposition party is the major party opposite the President",
            )
        )

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
        "undifferentiated_simulator_measures",
        "117-selected 50-seed panel",
        decisions,
        enacted,
        vetoes,
        overrides,
        "large_descriptive_mismatch_no_prespecified_tolerance",
        "simulator",
        "simulator does not separately label bill and joint-resolution measure classes",
    )
    pooled_rate = combined_counts[2] / combined_counts[0]
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
    bill_pooled = next(row for row in rows if row["cohort"] == BILL_POOLED)
    joint_pooled = next(row for row in rows if row["cohort"] == JOINT_POOLED)
    combined = next(row for row in rows if row["cohort"] == COMBINED_POOLED)
    simulator = next(row for row in rows if row["sourceType"] == "frozen simulator")
    divided = next(row for row in rows if row["cohort"] == "divided")
    unified = next(row for row in rows if row["cohort"] == "unified")
    opposition = next(row for row in rows if row["cohort"] == "opposition-party sponsor")
    same_party = next(row for row in rows if row["cohort"] == "same-party sponsor")
    both_recorded = next(row for row in rows if row["cohort"] == "both final roll calls")
    no_recorded = next(row for row in rows if row["cohort"] == "no final roll calls")
    below_two_thirds = next(
        row for row in rows if row["cohort"] == "one or both chambers below two-thirds"
    )
    both_two_thirds = next(
        row for row in rows if row["cohort"] == "both chambers at least two-thirds"
    )
    opposition_both = next(
        row for row in rows if row["cohort"] == "opposition majority in both chambers"
    )
    opposition_below = next(
        row
        for row in rows
        if row["cohort"] == "opposition below majority in one or both chambers"
    )

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

    coverage_rows = [row for row in rows if row["groupType"] == "final_vote_coverage"]
    minimum_support_rows = [
        row for row in rows if row["groupType"] == "both_recorded_minimum_support"
    ]
    opposition_support_rows = [
        row for row in rows if row["groupType"] == "both_recorded_opposition_support"
    ]
    class_ratio = float(joint_pooled["conditionalVetoRate"]) / float(
        bill_pooled["conditionalVetoRate"]
    )
    control_ratio = (
        (int(divided["vetoes"]) / int(divided["decisionCount"]))
        / (int(unified["vetoes"]) / int(unified["decisionCount"]))
    )
    sponsor_ratio = (
        (int(opposition["vetoes"]) / int(opposition["decisionCount"]))
        / (int(same_party["vetoes"]) / int(same_party["decisionCount"]))
    )

    lines = [
        "# Legislative Executive-Action Diagnostic",
        "",
        "Source-aligned diagnostic of presentment, presidential veto, successful override, enactment, and observed final chamber support in complete 108th-118th-Congress GovInfo decision panels and the frozen selected workflow panel.",
        "",
        "## Denominator Alignment",
        "",
        "- The bill panel parses 126,760 H.R./S. source records and retains 4,021 measures presented to the President. A separate panel parses 2,031 H.J.Res./S.J.Res. records and retains 187 presidential decisions.",
        "- Bills and joint resolutions are reported separately before a combined 4,208-measure denominator is shown. Constitutional-amendment joint resolutions that are not presented to the President remain outside the population.",
        "- The bill veto reference contains 21 vetoes and six successful overrides. The joint-resolution reference contains 26 vetoes and no overrides; the S.J.Res. 22 source-date discrepancy is preserved rather than forced into agreement.",
        "- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. Every empirical subset uses the same identity, avoiding double-counting measures enacted over a veto.",
        "- The final-vote panel contains one House and one Senate row for every presented measure. It retains 1,685 official final roll calls and 6,731 nonrecorded final approvals; earlier roll calls are never substituted for a later voice vote or unanimous-consent approval.",
        "- These diagnostics do not participate in calendar-threshold selection or alter any frozen lifecycle tolerance.",
        "",
        "## Measure-Class And Simulator Comparison",
        "",
        "| Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    append_rows(lines, [bill_pooled, joint_pooled, combined, simulator])
    lines.extend([
        "",
        "## H.R./S. Congress Results",
        "",
        "| Congress | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(lines, [row for row in rows if row["groupType"] == "congress"])
    lines.extend([
        "",
        "## H.R./S. Descriptive Strata",
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
    lines.extend([
        "",
        "## Final-Vote Coverage",
        "",
        "These four rows partition all 4,208 measures. A nonrecorded final approval is an observed legislative pathway, not missing data to be silently imputed.",
        "",
        "| Coverage | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(lines, coverage_rows)
    lines.extend([
        "",
        "## Both-Recorded Support Strata",
        "",
        "The next rows are restricted to the 310 measures with recorded final votes in both chambers. The two-thirds split uses yea divided by yea plus nay, matching the constitutional override benchmark. The opposition-party split uses the major party opposite the President. Neither split was used for model fitting or causal estimation.",
        "",
        "| Minimum chamber support | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(lines, minimum_support_rows)
    lines.extend([
        "",
        "| Opposition-party support | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    append_rows(lines, opposition_support_rows)
    lines.extend([
        "",
        "## Findings",
        "",
        f"The bill class contains {bill_pooled['vetoes']} vetoes in {bill_pooled['decisionCount']} decisions, a rate of {float(bill_pooled['conditionalVetoRate']):.6f}. Joint resolutions contain {joint_pooled['vetoes']} vetoes in {joint_pooled['decisionCount']} decisions, a rate of {float(joint_pooled['conditionalVetoRate']):.6f}, or {class_ratio:.3f} times the bill-class rate. Pooling without a measure-class label would therefore conceal a large composition difference.",
        "",
        f"The combined empirical population contains {combined['vetoes']} vetoes in {combined['decisionCount']} presented measures, a rate of {float(combined['conditionalVetoRate']):.6f}. The frozen selected simulator panel produces {simulator['vetoes']} vetoes in {simulator['decisionCount']} executive decisions, a rate of {float(simulator['conditionalVetoRate']):.6f}. The exact-count difference is {float(simulator['conditionalVetoRateDifferenceFromPooledEmpirical']):.6f}, and the simulator rate is {float(simulator['conditionalVetoRateRatioToPooledEmpirical']):.3f} times the combined empirical rate.",
        "The difference and ratio are computed from integer event counts before display rates are rounded.",
        "",
        "The combined empirical and simulator Wilson intervals do not overlap. No veto-specific tolerance was prespecified, so this remains a descriptive mechanism discrepancy rather than a retroactive formal pass or failure.",
        "",
        f"Within the bill class, divided-government Congresses contain {divided['vetoes']} vetoes in {divided['decisionCount']} decisions versus {unified['vetoes']} in {unified['decisionCount']} under unified government, an unadjusted rate ratio of {control_ratio:.3f}. Opposite-party sponsors account for {opposition['vetoes']} vetoes in {opposition['decisionCount']} decisions versus {same_party['vetoes']} in {same_party['decisionCount']} for same-party sponsors, an unadjusted rate ratio of {sponsor_ratio:.3f}.",
        "These strata overlap with administration and issue mix and do not estimate causal party-control or sponsor-party effects.",
        "",
        f"Final-roll coverage is strongly selected: {both_recorded['vetoes']} of {combined['vetoes']} vetoes occur among the {both_recorded['decisionCount']} measures with recorded final votes in both chambers, while {no_recorded['vetoes']} occur among {no_recorded['decisionCount']} measures with neither final roll call. This pattern makes complete-case support analysis nonrepresentative of the full presentment population.",
        "",
        f"Within the both-recorded subset, {below_two_thirds['vetoes']} of {below_two_thirds['decisionCount']} measures with one or both chambers below two-thirds were vetoed, compared with {both_two_thirds['vetoes']} of {both_two_thirds['decisionCount']} measures at or above two-thirds in both chambers. All {opposition_both['vetoes']} both-recorded vetoes occur among the {opposition_both['decisionCount']} measures with opposition-party majority support in both chambers; the other {opposition_below['decisionCount']} measures contain {opposition_below['vetoes']} vetoes. These are descriptive associations conditioned on an informative recording process, measure class, and completed passage.",
        "",
        "## Model Boundary And Next Gate",
        "",
        "The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can coexist with a badly mis-scaled executive-action pathway.",
        "",
        "The next gate is a separately frozen presidential-choice study using the now-committed measure-class and final-vote fields. It must specify the low-event estimator, predictor availability rules, treatment of nonrecorded approvals, calibration loss, and whole-Congress holdout before fitting. The current flow threshold and transport tolerances remain frozen.",
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
