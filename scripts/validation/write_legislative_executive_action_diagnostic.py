#!/usr/bin/env python3
"""Compare frozen simulator veto behavior with complete-Congress GovInfo records."""

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


CENSUSES = {
    "116": Path("data/validation/raw/govinfo_bill_census_116.csv"),
    "117": Path("data/validation/raw/govinfo_bill_census.csv"),
    "118": Path("data/validation/raw/govinfo_bill_census_118.csv"),
}
CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
OUT_CSV = Path("reports/legislative-executive-action-diagnostic.csv")
OUT_MD = Path("reports/legislative-executive-action-diagnostic.md")

CLAIM_BOUNDARY = (
    "This is a descriptive mechanism diagnostic using complete H.R./S. presentment, "
    "veto, override, and enactment classifications for three Congresses. It is not a "
    "causal model, a presidential-choice calibration, or evidence about bill quality, "
    "welfare, public preferences, or institutional rankings."
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
        "cohort": cohort,
        "decisionDefinition": (
            "presented_to_president"
            if source_type == "GovInfo census"
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


def empirical_counts(rows: list[dict[str, str]], congress: str) -> tuple[int, int, int, int]:
    require({row.get("congress") for row in rows} == {congress}, f"Congress {congress} scope drifted.")
    presented = sum(row.get("presented_to_president") == "1" for row in rows)
    enacted = sum(row.get("enacted") == "1" for row in rows)
    vetoes = sum(row.get("vetoed") == "1" for row in rows)
    overrides = sum(row.get("veto_overridden") == "1" for row in rows)
    require(
        presented == enacted + vetoes - overrides,
        f"Congress {congress} executive-decision identity failed.",
    )
    return presented, enacted, vetoes, overrides


def build_rows() -> list[dict[str, str]]:
    counts_by_congress: dict[str, tuple[int, int, int, int]] = {}
    rows: list[dict[str, str]] = []
    for congress, path in CENSUSES.items():
        counts = empirical_counts(read_csv(path), congress)
        counts_by_congress[congress] = counts
        rows.append(
            diagnostic_row(
                "GovInfo census",
                congress,
                *counts,
                "empirical_reference",
            )
        )

    pooled = tuple(sum(counts[index] for counts in counts_by_congress.values()) for index in range(4))
    pooled_row = diagnostic_row(
        "GovInfo census",
        "116-118 pooled",
        *pooled,
        "empirical_reference_pooled",
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
    pooled = next(row for row in rows if row["cohort"] == "116-118 pooled")
    simulator = next(row for row in rows if row["sourceType"] == "frozen simulator")
    lines = [
        "# Legislative Executive-Action Diagnostic",
        "",
        "Source-aligned diagnostic of presentment, presidential veto, successful override, and enactment in the complete 116th-118th H.R./S. censuses and the frozen selected workflow panel.",
        "",
        "## Denominator Alignment",
        "",
        "- Empirical executive decisions are measures classified as presented to the President.",
        "- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. This avoids double-counting bills enacted over a veto.",
        "- In every empirical cohort, presentments equal enactments plus vetoes minus overrides, so the two denominators describe the same decision point.",
        "- Veto and override diagnostics do not participate in calendar-threshold selection or alter any frozen tolerance.",
        "",
        "## Results",
        "",
        "| Source | Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) | Status |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        override_interval = "NA"
        if row["overrideRateAmongVetoes"] != "NA":
            override_interval = (
                f"{float(row['overrideRateAmongVetoes']):.6f} "
                f"[{float(row['overrideWilson95Low']):.6f}, "
                f"{float(row['overrideWilson95High']):.6f}]"
            )
        lines.append(
            f"| {row['sourceType']} | {row['cohort']} | {row['decisionCount']} | "
            f"{row['vetoes']} | {float(row['conditionalVetoRate']):.6f} "
            f"[{float(row['conditionalVetoWilson95Low']):.6f}, "
            f"{float(row['conditionalVetoWilson95High']):.6f}] | "
            f"{row['overriddenVetoes']} | {override_interval} | "
            f"{row['diagnosticStatus']} |"
        )
    lines.extend([
        "",
        "## Finding",
        "",
        f"The complete empirical cohorts contain {pooled['vetoes']} vetoes in {pooled['decisionCount']} presentments, a conditional rate of {float(pooled['conditionalVetoRate']):.6f}. The frozen selected panel produces {simulator['vetoes']} vetoes in {simulator['decisionCount']} executive decisions, a rate of {float(simulator['conditionalVetoRate']):.6f}. The absolute difference is {float(simulator['conditionalVetoRateDifferenceFromPooledEmpirical']):.6f}, and the simulator rate is {float(simulator['conditionalVetoRateRatioToPooledEmpirical']):.3f} times the pooled empirical rate.",
        "The difference and ratio are computed from the integer event counts before rates are rounded to six decimals for display.",
        "",
        "The Wilson intervals do not overlap. That makes the mechanism discrepancy too large to hide behind the aggregate enactment fit. No veto-specific tolerance was prespecified, so this report preserves the result as a descriptive diagnostic rather than relabeling it as a formal held-out pass or failure.",
        "",
        "Only three empirical vetoes are observed, including one successful override. The override estimate is therefore extremely sparse and should not be used for parameter fitting by itself.",
        "",
        "## Model Boundary And Next Gate",
        "",
        "The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can be produced while the internal executive-action pathway is wrong.",
        "",
        "A future calibration should use a longer completed-Congress panel spanning multiple administrations, classify regular and pocket vetoes plus both-chamber overrides, condition presidential choice on policy distance, party control, and chamber support, and reserve complete Congresses for temporal testing. The current flow threshold and transport tolerances should remain frozen while that separate mechanism model is designed.",
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
