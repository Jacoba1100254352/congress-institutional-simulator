#!/usr/bin/env python3
"""Write the publication-facing summary for the complete 118th bill census."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

try:
    from .write_govinfo_bill_census_report import (
        STAGES,
        bounded_crosscheck,
        metadata_values,
        read_csv,
        sha256_file,
        summarize,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from write_govinfo_bill_census_report import (
        STAGES,
        bounded_crosscheck,
        metadata_values,
        read_csv,
        sha256_file,
        summarize,
    )


CENSUS = Path("data/validation/raw/govinfo_bill_census_118.csv")
METADATA = Path("data/validation/raw/govinfo_bill_census_118.metadata.md")
OUT_CSV = Path("reports/govinfo-bill-census-118.csv")
OUT_MD = Path("reports/govinfo-bill-census-118.md")

EXPECTED_VETO_BILL = "118-s-4199"
EXPECTED_NONIDENTICAL_VERSION_BILLS = {
    "118-s-1146",
    "118-s-1258",
    "118-s-2073",
}

CLAIM_BOUNDARY = (
    "The census supports descriptive 118th-Congress H.R./S. legislative-flow "
    "benchmarks and an aggregate temporal transport check for the frozen 117th-"
    "Congress calibration. It does not establish causal mechanism validity, bill "
    "quality, public preferences, public benefit, welfare, or institutional rankings."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate(rows: list[dict[str, str]], metadata: dict[str, str]) -> None:
    require(rows, f"{CENSUS} is missing or empty.")
    require({row.get("congress") for row in rows} == {"118"}, "118th census contains another Congress.")
    require(len({row["bill_id"] for row in rows}) == len(rows), "118th census bill IDs are not unique.")
    require(not any(row.get("integrity_status", "").startswith("invalid:") for row in rows), "118th census contains invalid lifecycle rows.")
    require(metadata.get("congress") == "118", "118th census metadata has the wrong Congress.")
    require(metadata.get("rows") == str(len(rows)), "118th census metadata row count differs from CSV.")
    require(metadata.get("output_sha256") == sha256_file(CENSUS), "118th census metadata hash differs from CSV bytes.")

    veto_rows = [row for row in rows if row.get("vetoed") == "1"]
    require([row["bill_id"] for row in veto_rows] == [EXPECTED_VETO_BILL], "118th veto classification drifted.")
    require(veto_rows[0].get("enacted") == "0", "The 118th veto row is incorrectly enacted.")
    presented_not_enacted = {
        row["bill_id"]
        for row in rows
        if row.get("presented_to_president") == "1" and row.get("enacted") == "0"
    }
    require(presented_not_enacted == {EXPECTED_VETO_BILL}, "118th presentment/non-enactment set drifted.")
    nonidentical_versions = {
        row["bill_id"]
        for row in rows
        if row.get("passed_house") == "1"
        and row.get("passed_senate") == "1"
        and row.get("completed_congressional_passage") == "0"
    }
    require(nonidentical_versions == EXPECTED_NONIDENTICAL_VERSION_BILLS, "118th nonidentical-version set drifted.")


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
    raw_rows: list[dict[str, str]],
    metadata: dict[str, str],
) -> None:
    by_group = {(row["groupType"], row["groupValue"]): row for row in summaries}
    overall = by_group[("all", "all H.R. and S. bills")]
    bounded = bounded_crosscheck()
    anomalies = [
        row for row in raw_rows if row.get("integrity_status", "").startswith("source_date_anomaly:")
    ]
    anomaly_bills = ", ".join(f"`{row['bill_id']}`" for row in anomalies)
    nonidentical = sorted(EXPECTED_NONIDENTICAL_VERSION_BILLS)
    nonidentical_text = ", ".join(f"`{bill_id}`" for bill_id in nonidentical)

    lines = [
        "# GovInfo Bill Lifecycle Census: 118th Congress",
        "",
        "This report summarizes the complete, provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 118th Congress. The full census is the temporal test cohort for the frozen 117th-Congress lifecycle calibration.",
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
        "| Type | Bills | Committee advanced | Floor considered | Origin passage | Completed passage | Vetoed | Enacted |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for bill_type in ("hr", "s"):
        row = by_group[("bill_type", bill_type)]
        lines.append(
            f"| `{bill_type}` | {row['billCount']} | {row['committeeAdvancedRate']} | "
            f"{row['floorConsideredRate']} | {row['originPassageRate']} | "
            f"{row['completedCongressionalPassageRate']} | {row['vetoedRate']} | "
            f"{row['enactedRate']} |"
        )

    lines.extend([
        "",
        "## Classification And Integrity Audit",
        "",
        "- The temporal audit found that GovInfo action code `E30000` is context-dependent: it labels signatures in most records but labels the presidential veto of `118-s-4199`. Classifier v2 therefore requires positive signature/enactment text or an unambiguous law record/code rather than treating `E30000` alone as enactment.",
        "- `118-s-4199` completed passage and was presented, then vetoed; it is the only presented bill in this scope that was not enacted.",
        f"- Both chamber-passage flags are present for {nonidentical_text}, but the conservative classifier does not mark completed passage because the records do not establish agreement on identical text.",
        f"- The {len(anomalies)} preserved source-date anomalies are hearing dates before introduction in official committee-activity metadata: {anomaly_bills}.",
        "",
        "## Independent Source Cross-Check",
        "",
        f"The separate bounded 118th-Congress Congress.gov/GovInfo sample contains {bounded['rows']} rows; {bounded['linked']} retain GovInfo identifier matches, {bounded['actionAligned']} align on the earlier coarse action flags, and {bounded['policyAreaAligned']} align on policy area. This bounded sample audits source translation; the full census supplies the temporal flow rates.",
        "",
        "## Interpretation Boundary",
        "",
        "- No 118th-Congress record participates in threshold selection or refitting.",
        "- The census is complete for H.R. and S. measures, not resolutions or joint resolutions.",
        "- Stage flags are conservative operational classifications of GovInfo records, not official legal-status determinations.",
        "- The temporal comparison tests transport of three aggregate rates. It does not identify why Congresses differ or validate individual mechanisms.",
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
    write_markdown(summaries, raw_rows, metadata)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
