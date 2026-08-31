#!/usr/bin/env python3
"""Write the publication-facing summary for the complete 116th bill census."""

from __future__ import annotations

import csv
from pathlib import Path

try:
    from .write_govinfo_bill_census_report import (
        STAGES,
        metadata_values,
        read_csv,
        sha256_file,
        summarize,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from write_govinfo_bill_census_report import (
        STAGES,
        metadata_values,
        read_csv,
        sha256_file,
        summarize,
    )


CENSUS = Path("data/validation/raw/govinfo_bill_census_116.csv")
METADATA = Path("data/validation/raw/govinfo_bill_census_116.metadata.md")
OUT_CSV = Path("reports/govinfo-bill-census-116.csv")
OUT_MD = Path("reports/govinfo-bill-census-116.md")

EXPECTED_VETO_BILLS = {"116-hr-6395", "116-s-906"}
EXPECTED_OVERRIDE_BILL = "116-hr-6395"
EXPECTED_PRESENTED_NOT_ENACTED = {"116-s-906"}
EXPECTED_NONIDENTICAL_VERSION_BILLS = {
    "116-hr-550",
    "116-hr-925",
    "116-hr-1044",
    "116-hr-2486",
    "116-hr-2610",
    "116-hr-4764",
    "116-hr-6172",
    "116-s-178",
    "116-s-1811",
}
EXPECTED_SOURCE_DATE_ANOMALIES = {
    "116-hr-2665",
    "116-hr-2779",
    "116-hr-3432",
    "116-hr-3630",
    "116-hr-3631",
    "116-hr-4618",
    "116-hr-4650",
    "116-hr-4665",
    "116-hr-4671",
    "116-hr-4995",
    "116-hr-4996",
    "116-hr-4997",
    "116-hr-5000",
    "116-hr-5035",
    "116-hr-5552",
    "116-s-1790",
    "116-s-2470",
    "116-s-2520",
    "116-s-2524",
    "116-s-2581",
    "116-s-2582",
    "116-s-2583",
    "116-s-2584",
    "116-s-4897",
}

CLAIM_BOUNDARY = (
    "The census supports descriptive 116th-Congress H.R./S. legislative-flow "
    "benchmarks and an aggregate backcast for the frozen 117th-Congress calibration. "
    "It does not establish causal mechanism validity, bill quality, public preferences, "
    "public benefit, welfare, or institutional rankings."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate(rows: list[dict[str, str]], metadata: dict[str, str]) -> None:
    require(rows, f"{CENSUS} is missing or empty.")
    require({row.get("congress") for row in rows} == {"116"}, "116th census contains another Congress.")
    require(len({row["bill_id"] for row in rows}) == len(rows), "116th census bill IDs are not unique.")
    require(not any(row.get("integrity_status", "").startswith("invalid:") for row in rows), "116th census contains invalid lifecycle rows.")
    require(metadata.get("congress") == "116", "116th census metadata has the wrong Congress.")
    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v3", "116th classifier version drifted.")
    require(metadata.get("rows") == str(len(rows)), "116th census metadata row count differs from CSV.")
    require(metadata.get("output_sha256") == sha256_file(CENSUS), "116th census metadata hash differs from CSV bytes.")

    veto_bills = {row["bill_id"] for row in rows if row.get("vetoed") == "1"}
    require(veto_bills == EXPECTED_VETO_BILLS, "116th veto classification drifted.")
    override_bills = {row["bill_id"] for row in rows if row.get("veto_overridden") == "1"}
    require(override_bills == {EXPECTED_OVERRIDE_BILL}, "116th successful-override classification drifted.")
    by_bill = {row["bill_id"]: row for row in rows}
    require(by_bill[EXPECTED_OVERRIDE_BILL].get("enacted") == "1", "The overridden 116th bill is not enacted.")
    presented_not_enacted = {
        row["bill_id"]
        for row in rows
        if row.get("presented_to_president") == "1" and row.get("enacted") == "0"
    }
    require(presented_not_enacted == EXPECTED_PRESENTED_NOT_ENACTED, "116th presentment/non-enactment set drifted.")
    nonidentical_versions = {
        row["bill_id"]
        for row in rows
        if row.get("passed_house") == "1"
        and row.get("passed_senate") == "1"
        and row.get("completed_congressional_passage") == "0"
    }
    require(nonidentical_versions == EXPECTED_NONIDENTICAL_VERSION_BILLS, "116th nonidentical-version set drifted.")
    anomaly_bills = {
        row["bill_id"]
        for row in rows
        if row.get("integrity_status", "").startswith("source_date_anomaly:")
    }
    require(anomaly_bills == EXPECTED_SOURCE_DATE_ANOMALIES, "116th source-date anomaly set drifted.")


def report_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result = [summarize("all", "all H.R. and S. bills", rows)]
    for bill_type in ("hr", "s"):
        result.append(
            summarize(
                "bill_type",
                bill_type,
                [row for row in rows if row.get("bill_type") == bill_type],
            )
        )
    return result


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    summaries: list[dict[str, str]],
    metadata: dict[str, str],
) -> None:
    by_group = {(row["groupType"], row["groupValue"]): row for row in summaries}
    overall = by_group[("all", "all H.R. and S. bills")]
    anomalies = sorted(EXPECTED_SOURCE_DATE_ANOMALIES)
    anomaly_text = ", ".join(f"`{bill_id}`" for bill_id in anomalies)
    nonidentical = sorted(EXPECTED_NONIDENTICAL_VERSION_BILLS)
    nonidentical_text = ", ".join(f"`{bill_id}`" for bill_id in nonidentical)

    lines = [
        "# GovInfo Bill Lifecycle Census: 116th Congress",
        "",
        "This report summarizes the complete, provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 116th Congress. It is the pre-calibration backcast cohort for the frozen 117th-Congress lifecycle design.",
        "",
        f"- Bills: {overall['billCount']} ({by_group[('bill_type', 'hr')]['billCount']} H.R.; {by_group[('bill_type', 's')]['billCount']} S.)",
        f"- Parsed direct bill actions: {overall['actionCount']}",
        f"- Public/private law rows: {overall['publicLawCount']} / {overall['privateLawCount']}",
        "- Structurally invalid rows: 0",
        f"- Preserved source-date anomaly rows: {overall['sourceDateAnomalyCount']}",
        f"- Classification version: `{metadata.get('classification_version', '')}`",
        f"- Committed CSV SHA-256: `{metadata.get('output_sha256', '')}`",
        "",
        "## Lifecycle Funnel",
        "",
        "| Stage | Count | Rate |",
        "| --- | ---: | ---: |",
    ]
    for prefix, _, label in STAGES:
        lines.append(f"| {label} | {overall[f'{prefix}Count']} | {overall[f'{prefix}Rate']} |")

    lines.extend([
        "",
        "## Bill-Type Strata",
        "",
        "| Type | Bills | Committee advanced | Floor considered | Origin passage | Completed passage | Vetoed | Overridden | Enacted |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for bill_type in ("hr", "s"):
        row = by_group[("bill_type", bill_type)]
        lines.append(
            f"| `{bill_type}` | {row['billCount']} | {row['committeeAdvancedRate']} | "
            f"{row['floorConsideredRate']} | {row['originPassageRate']} | "
            f"{row['completedCongressionalPassageRate']} | {row['vetoedRate']} | "
            f"{row['vetoOverriddenRate']} | {row['enactedRate']} |"
        )

    lines.extend([
        "",
        "## Executive-Action Audit",
        "",
        "- `116-hr-6395` was vetoed, overridden by both chambers, and enacted as Public Law 116-283. The successful-override date is the final Senate override action on 2021-01-01.",
        "- `116-s-906` was vetoed without a successful override and is the only presented measure in scope that was not enacted.",
        "- These two records make veto and override rates directly observable, but the event count is too small for a stable mechanism calibration by itself.",
        "",
        "## Classification And Integrity Audit",
        "",
        "- Classifier v3 requires affirmative House and Senate override evidence before labeling a veto successfully overridden. One chamber alone is insufficient.",
        f"- Both chamber-passage flags are present for {nonidentical_text}, but the conservative classifier does not mark completed passage because the records do not establish agreement on identical text.",
        f"- The {len(anomalies)} preserved source-date anomalies are hearing dates before introduction in official committee-activity metadata: {anomaly_text}.",
        "",
        "## Interpretation Boundary",
        "",
        "- No 116th-Congress record participates in threshold selection, tolerance selection, or refitting.",
        "- The census is complete for H.R. and S. measures, not resolutions or joint resolutions.",
        "- Stage flags are conservative operational classifications of GovInfo records, not official legal-status determinations.",
        "- The temporal comparison tests transport of aggregate rates and exposes an executive-action mechanism discrepancy. It does not identify why Congresses differ or validate individual causal mechanisms.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    raw_rows = read_csv(CENSUS)
    metadata = metadata_values(METADATA)
    validate(raw_rows, metadata)
    summaries = report_rows(raw_rows)
    write_csv(summaries)
    write_markdown(summaries, metadata)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
