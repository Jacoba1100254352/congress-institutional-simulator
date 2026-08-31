#!/usr/bin/env python3
"""Write publication-facing summaries for the GovInfo bill lifecycle census."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path
from statistics import median


CENSUS = Path("data/validation/raw/govinfo_bill_census.csv")
METADATA = Path("data/validation/raw/govinfo_bill_census.metadata.md")
PUBLIC_LAW_CROSSCHECK = Path("data/validation/raw/law_revision_bill_linkage.csv")
BOUNDED_CROSSCHECK = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
OUT_CSV = Path("reports/govinfo-bill-census.csv")
OUT_MD = Path("reports/govinfo-bill-census.md")

STAGES = (
    ("referred", "referred_to_committee", "Referred to committee"),
    ("hearing", "hearing_held", "Committee hearing"),
    ("markup", "markup_held", "Committee markup"),
    ("orderedReported", "committee_ordered_reported", "Committee ordered reported"),
    ("reported", "committee_reported", "Committee report"),
    ("discharged", "committee_discharged", "Committee discharge"),
    ("committeeAdvanced", "committee_advanced", "Committee advanced"),
    ("floorConsidered", "floor_considered", "Substantive floor consideration"),
    ("originPassage", "passed_origin_chamber", "Passed origin chamber"),
    (
        "completedCongressionalPassage",
        "completed_congressional_passage",
        "Completed congressional passage",
    ),
    ("presented", "presented_to_president", "Presented to President"),
    ("vetoed", "vetoed", "Vetoed"),
    ("vetoOverridden", "veto_overridden", "Veto overridden"),
    ("enacted", "enacted", "Enacted"),
)

CLAIM_BOUNDARY = (
    "The census supports descriptive 117th-Congress H.R./S. legislative-flow "
    "benchmarks, calibration, and deterministic within-Congress held-out checks. "
    "Its use with the complete 116th and 118th censuses supports aggregate temporal "
    "transport checks, not causal mechanism validity, public support, public benefit, welfare, "
    "or institutional rankings."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_values(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            result[key] = value.strip().strip("`")
    return result


def numeric(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def stable_hash_heldout(value: str) -> bool:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 2 == 0


def rate(count: int, total: int) -> str:
    return f"{count / total:.6f}" if total else "0.000000"


def summarize(group_type: str, group_value: str, rows: list[dict[str, str]]) -> dict[str, str]:
    total = len(rows)
    action_counts = [numeric(row.get("actions_count", "")) for row in rows]
    result: dict[str, str] = {
        "groupType": group_type,
        "groupValue": group_value,
        "billCount": str(total),
        "actionCount": str(sum(action_counts)),
        "recordedVoteCount": str(sum(numeric(row.get("recorded_vote_count", "")) for row in rows)),
        "meanActions": f"{sum(action_counts) / total:.6f}" if total else "0.000000",
        "medianActions": f"{median(action_counts):.6f}" if action_counts else "0.000000",
        "publicLawCount": str(sum("Public Law" in row.get("law_type", "") for row in rows)),
        "privateLawCount": str(sum("Private Law" in row.get("law_type", "") for row in rows)),
        "sourceDateAnomalyCount": str(
            sum(row.get("integrity_status", "").startswith("source_date_anomaly:") for row in rows)
        ),
    }
    for prefix, field, _ in STAGES:
        count = sum(row.get(field) == "1" for row in rows)
        result[f"{prefix}Count"] = str(count)
        result[f"{prefix}Rate"] = rate(count, total)
    return result


def report_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    calibration = [row for row in rows if not stable_hash_heldout(row["bill_id"])]
    heldout = [row for row in rows if stable_hash_heldout(row["bill_id"])]
    output = [
        summarize("all", "all H.R. and S. bills", rows),
        summarize("split", "calibration", calibration),
        summarize("split", "heldout", heldout),
    ]
    for bill_type in sorted({row["bill_type"] for row in rows}):
        output.append(
            summarize(
                "bill_type",
                bill_type,
                [row for row in rows if row["bill_type"] == bill_type],
            )
        )
    parties = Counter(row.get("sponsor_party", "unknown") or "unknown" for row in rows)
    for party, _ in sorted(parties.items(), key=lambda item: (-item[1], item[0])):
        output.append(
            summarize(
                "sponsor_party",
                party,
                [row for row in rows if (row.get("sponsor_party", "unknown") or "unknown") == party],
            )
        )
    policy_areas = Counter(row.get("policy_area", "Unclassified") or "Unclassified" for row in rows)
    for policy_area, _ in sorted(policy_areas.items(), key=lambda item: (-item[1], item[0])):
        output.append(
            summarize(
                "policy_area",
                policy_area,
                [row for row in rows if (row.get("policy_area", "Unclassified") or "Unclassified") == policy_area],
            )
        )
    return output


def validate_census(rows: list[dict[str, str]], metadata: dict[str, str]) -> None:
    if not rows:
        raise SystemExit(f"{CENSUS} is missing or empty; run make build-govinfo-bill-census-raw.")
    required = {
        "bill_id",
        "congress",
        "bill_type",
        "bill_number",
        "introduced",
        "committee_ordered_reported",
        "committee_reported",
        "committee_advanced",
        "floor_considered",
        "passed_origin_chamber",
        "completed_congressional_passage",
        "veto_overridden",
        "enacted",
        "actions_count",
        "source_xml_sha256",
        "actions_sha256",
        "integrity_status",
    }
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"{CENSUS} is missing required columns: {sorted(missing)}")
    identifiers = [row["bill_id"] for row in rows]
    if len(set(identifiers)) != len(identifiers):
        raise SystemExit(f"{CENSUS} contains duplicate bill IDs.")
    invalid = [row for row in rows if row.get("integrity_status", "").startswith("invalid:")]
    if invalid:
        raise SystemExit(f"{CENSUS} contains {len(invalid)} invalid lifecycle rows.")
    if metadata.get("rows") and numeric(metadata["rows"]) != len(rows):
        raise SystemExit("Census metadata row count does not match the CSV.")
    action_count = sum(numeric(row.get("actions_count", "")) for row in rows)
    if metadata.get("parsed_action_records") and numeric(metadata["parsed_action_records"]) != action_count:
        raise SystemExit("Census metadata action count does not match the CSV.")
    if metadata.get("output_sha256") and metadata["output_sha256"] != sha256_file(CENSUS):
        raise SystemExit("Census metadata output SHA-256 does not match the CSV bytes.")


def public_law_crosscheck(rows: list[dict[str, str]]) -> dict[str, int]:
    by_bill = {row["bill_id"]: row for row in rows}
    source = read_csv(PUBLIC_LAW_CROSSCHECK)
    overlaps = [row for row in source if row.get("bill_id") in by_bill]
    return {
        "rows": len(source),
        "overlaps": len(overlaps),
        "enactedAligned": sum(
            by_bill[row["bill_id"]].get("enacted") == row.get("enacted")
            for row in overlaps
        ),
        "introducedDateAligned": sum(
            by_bill[row["bill_id"]].get("introduced_date") == row.get("introduced_date")
            for row in overlaps
        ),
        "policyAreaAligned": sum(
            by_bill[row["bill_id"]].get("policy_area") == row.get("policy_area")
            for row in overlaps
        ),
    }


def bounded_crosscheck() -> dict[str, int]:
    rows = read_csv(BOUNDED_CROSSCHECK)
    linked = [row for row in rows if row.get("linkage_status") == "govinfo_billstatus_metadata"]
    return {
        "rows": len(rows),
        "linked": len(linked),
        "actionAligned": sum(row.get("action_alignment_status") == "aligned" for row in linked),
        "policyAreaAligned": sum(
            row.get("policy_area_alignment_status") == "aligned" for row in linked
        ),
    }


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    rows: list[dict[str, str]],
    metadata: dict[str, str],
    public_law: dict[str, int],
    bounded: dict[str, int],
) -> None:
    by_group = {(row["groupType"], row["groupValue"]): row for row in rows}
    all_row = by_group[("all", "all H.R. and S. bills")]
    calibration = by_group[("split", "calibration")]
    heldout = by_group[("split", "heldout")]
    source_anomalies = all_row["sourceDateAnomalyCount"]
    lines = [
        "# GovInfo Bill Lifecycle Census",
        "",
        "This report summarizes the provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 117th Congress. It supplies the frozen calibration baseline for the separate 116th- and 118th-Congress temporal transport checks; none of these artifacts is a causal simulator-validation claim.",
        "",
        f"- Bills: {all_row['billCount']} ({by_group[('bill_type', 'hr')]['billCount']} H.R.; {by_group[('bill_type', 's')]['billCount']} S.)",
        f"- Parsed direct bill actions: {all_row['actionCount']}",
        f"- Public/private law rows: {all_row['publicLawCount']} / {all_row['privateLawCount']}",
        f"- Structurally invalid rows: 0",
        f"- Preserved source-date anomaly rows: {source_anomalies}",
        f"- Classification version: `{metadata.get('classification_version', '')}`",
        f"- Committed CSV SHA-256: `{metadata.get('output_sha256', '')}`",
        "",
        "## Lifecycle Funnel",
        "",
        "The split is deterministic: `sha256(bill_id)` first 32 bits modulo 2 equals zero is held out. It is a within-Congress stability check, not a temporal or cross-Congress validation design.",
        "",
        "| Stage | All count | All rate | Calibration rate | Held-out rate | Absolute split delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for prefix, _, label in STAGES:
        all_rate = float(all_row[f"{prefix}Rate"])
        calibration_rate = float(calibration[f"{prefix}Rate"])
        heldout_rate = float(heldout[f"{prefix}Rate"])
        lines.append(
            f"| {label} | {all_row[f'{prefix}Count']} | {all_rate:.6f} | "
            f"{calibration_rate:.6f} | {heldout_rate:.6f} | "
            f"{abs(calibration_rate - heldout_rate):.6f} |"
        )

    lines.extend([
        "",
        "## Bill-Type Strata",
        "",
        "| Type | Bills | Committee ordered reported | Committee report | Floor considered | Origin passage | Completed passage | Enacted |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for bill_type in ("hr", "s"):
        row = by_group[("bill_type", bill_type)]
        lines.append(
            f"| `{bill_type}` | {row['billCount']} | {row['orderedReportedRate']} | "
            f"{row['reportedRate']} | {row['floorConsideredRate']} | "
            f"{row['originPassageRate']} | {row['completedCongressionalPassageRate']} | "
            f"{row['enactedRate']} |"
        )

    lines.extend([
        "",
        "## Independent Cross-Checks",
        "",
        f"- The existing 117th-Congress Congress.gov public-law linkage contributes {public_law['rows']} rows; {public_law['overlaps']} overlap the census by bill ID, with {public_law['enactedAligned']} enacted flags, {public_law['introducedDateAligned']} introduction dates, and {public_law['policyAreaAligned']} policy areas aligned.",
        f"- The separate bounded 118th-Congress Congress.gov/GovInfo sample contains {bounded['rows']} rows; {bounded['linked']} retain GovInfo identifier matches, {bounded['actionAligned']} align on the earlier coarse action flags, and {bounded['policyAreaAligned']} align on policy area. It remains a source-translation cross-check; the complete 118th census is the temporal flow test.",
        "",
        "## Interpretation Boundary",
        "",
        "- The source archives contain both legacy v1 and current v3 XML records; both schemas are parsed, and no record is dropped for schema generation.",
        "- Action codes are used only where their observed meaning is stable in this corpus. Special-rule actions, failed discharge requests, administrative messages, and sponsorship substitutions do not advance the bill lifecycle.",
        "- Classifier v2 excluded context-dependent action code `E30000` from code-only enactment. Classifier v3 adds successful veto-override evidence only when both chambers affirmatively override; neither change alters a 117th aggregate funnel count.",
        "- Committee ordered-reported actions are separate from filed committee reports. Committee advancement is the union of ordered reported, reported, and discharged.",
        "- Completed congressional passage requires presentment, enactment, or second-chamber passage without amendment. Passing nonidentical versions in each chamber is not enough.",
        "- Five official committee-activity dates precede bill introduction. The source dates are retained and labeled rather than corrected locally.",
        "- The calibration/held-out split is suitable for within-Congress stability only. The complete 116th and 118th censuses supply separate no-refit temporal backcast and forecast checks.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = read_csv(CENSUS)
    metadata = metadata_values(METADATA)
    validate_census(rows, metadata)
    summaries = report_rows(rows)
    public_law = public_law_crosscheck(rows)
    bounded = bounded_crosscheck()
    write_csv(summaries)
    write_markdown(summaries, metadata, public_law, bounded)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
