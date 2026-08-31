#!/usr/bin/env python3
"""Write registry-backed empirical data inventory and boundary matrix reports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REGISTRY = Path("data/validation/source-registry.csv")
RAW_DIR = Path("data/validation/raw")
READINESS_CSV = Path("reports/empirical-validation-readiness.csv")
SUMMARY_CSV = Path("reports/empirical-validation-summary.csv")
BRIDGE_CSV = Path("reports/empirical-bridge.csv")
HELDOUT_CSV = Path("reports/empirical-flow-heldout.csv")
OUT_CSV = Path("reports/empirical-data-inventory.csv")
OUT_MD = Path("reports/empirical-data-inventory.md")
BOUNDARY_CSV = Path("reports/validation-boundary-matrix.csv")
BOUNDARY_MD = Path("reports/validation-boundary-matrix.md")

RELATED_RAW = {
    "govinfo_bill_census.csv": (
        Path("data/validation/raw/govinfo_bill_census_116.csv"),
        Path("data/validation/raw/govinfo_bill_census_118.csv"),
    ),
}

DATE_COLUMNS = (
    "introduced_date",
    "referred_to_committee_date",
    "committee_ordered_reported_date",
    "committee_reported_date",
    "floor_considered_date",
    "passed_origin_chamber_date",
    "completed_congressional_passage_date",
    "presented_to_president_date",
    "floor_action_date",
    "enacted_date",
    "period",
    "cycle",
    "year",
    "enacted_date",
    "proposed_rule_date",
    "final_rule_date",
    "effective_date",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_by_field(path: Path, field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in read_csv(path) if row.get(field)}


def summary_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in read_csv(SUMMARY_CSV):
        if row.get("status") == "computed":
            counts[row["dataset"]] += 1
    return counts


def bridge_statuses() -> dict[str, str]:
    statuses: dict[str, set[str]] = {}
    for row in read_csv(BRIDGE_CSV):
        statuses.setdefault(row["rawDataset"], set()).add(row["bridgeStatus"])
    return {dataset: "; ".join(sorted(values)) for dataset, values in statuses.items()}


def heldout_statuses() -> dict[str, str]:
    statuses: dict[str, set[str]] = {}
    for row in read_csv(HELDOUT_CSV):
        statuses.setdefault(row["sourceFamily"], set()).add(row["heldoutTargetStatus"])
    return {family: "; ".join(sorted(values)) for family, values in statuses.items()}


def raw_profile(raw_path: str) -> tuple[str, str, str]:
    if not raw_path:
        return "0", "", ""
    path = Path(raw_path)
    if not path.exists() or path.is_dir():
        return "0", "", ""
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        row_count = 0
        date_values: list[str] = []
        for row in reader:
            row_count += 1
            for column in DATE_COLUMNS:
                value = row.get(column, "").strip()
                if value:
                    date_values.append(value[:10])
        columns = ",".join(reader.fieldnames or [])
    if not date_values:
        return str(row_count), "", columns
    return str(row_count), f"{min(date_values)}..{max(date_values)}", columns


def inventory_status(readiness_status: str, offline_status: str) -> str:
    if readiness_status == "ready":
        return "ready"
    if readiness_status == "incomplete":
        return "schema gap"
    if offline_status == "fixture_only":
        return "fixture only"
    if offline_status in {"missing", ""}:
        return "missing"
    return offline_status


def evidence_label(row: dict[str, str], status: str, heldout: str, bridge: str) -> str:
    boundary = row["boundary_category"]
    if boundary == "held-out benchmark" and heldout:
        return f"held-out benchmark: {heldout}"
    if status == "ready" and bridge:
        return f"raw summary bridge: {bridge}"
    if status == "ready":
        return "raw summary available"
    if status == "fixture only":
        return "adapter fixture only"
    return "no raw empirical input"


def write_inventory(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    status_counts = Counter(row["inventoryStatus"] for row in rows)
    boundary_counts = Counter(row["boundaryCategory"] for row in rows)
    lines = [
        "# Empirical Data Inventory",
        "",
        "This registry-backed inventory lists each planned empirical source family, its local raw or cached support, and the boundary it can currently support. It is an evidence inventory, not a validation claim.",
        "",
        f"- Source families: {len(rows)}",
        f"- Ready or cached source families: {status_counts.get('ready', 0)}",
        f"- Fixture-only families: {status_counts.get('fixture only', 0)}",
        f"- Missing or schema-gap families: {status_counts.get('missing', 0) + status_counts.get('schema gap', 0)}",
        "",
        "Boundary categories:",
    ]
    for boundary, count in sorted(boundary_counts.items()):
        lines.append(f"- {boundary}: {count}")
    lines.extend([
        "",
        "| Source family | Dataset | Inventory status | Boundary | Rows | Related cohort | Date range | Evidence |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- |",
    ])
    for row in rows:
        date_range = row["dateRange"] if row["dateRange"] else "---"
        related = "---"
        if row["relatedRawPaths"]:
            related_paths = row["relatedRawPaths"].split(";")
            related_counts = row["relatedRawRowCounts"].split(";")
            related_dates = row["relatedRawDateRanges"].split(";")
            related = "; ".join(
                f"`{path}` ({count} rows; {date_range or 'no dates'})"
                for path, count, date_range in zip(
                    related_paths,
                    related_counts,
                    related_dates,
                )
            )
        lines.append(
            f"| {row['sourceFamily']} | `{row['dataset']}` | {row['inventoryStatus']} | "
            f"{row['boundaryCategory']} | {row['rowCount']} | {related} | {date_range} | "
            f"{row['evidenceStatus']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def write_boundary_matrix(rows: list[dict[str, str]]) -> None:
    matrix_rows = [
        {
            "sourceFamily": row["sourceFamily"],
            "dataset": row["dataset"],
            "boundaryCategory": row["boundaryCategory"],
            "observableSignal": row["observableSignal"],
            "simulatorProxy": row["simulatorProxy"],
            "supportedMetric": row["supportedMetric"],
            "evidenceStatus": row["evidenceStatus"],
            "claimBoundary": row["claimBoundary"],
            "nextStep": row["nextStep"],
        }
        for row in rows
    ]
    with BOUNDARY_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(matrix_rows)

    lines = [
        "# Validation Boundary Matrix",
        "",
        "Boundary categories are intentionally conservative:",
        "",
        "- `held-out benchmark`: a deterministic held-out empirical check exists for the named source family.",
        "- `flow sanity check`: the source supports broad flow plausibility only.",
        "- `calibration proxy`: the source supports a proxy or range check but does not validate the target construct directly.",
        "- `not validated`: the relevant source family is missing or only has adapter fixtures.",
        "",
        "| Source family | Boundary | Observable signal | Simulator proxy | Claim boundary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in matrix_rows:
        lines.append(
            f"| {row['sourceFamily']} | {row['boundaryCategory']} | {row['observableSignal']} | "
            f"{row['simulatorProxy']} | {row['claimBoundary']} |"
        )
    BOUNDARY_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    registry = read_csv(REGISTRY)
    if not registry:
        raise SystemExit(f"{REGISTRY} is missing or empty.")
    readiness = read_by_field(READINESS_CSV, "dataset")
    metrics_by_dataset = summary_counts()
    bridges = bridge_statuses()
    heldout = heldout_statuses()

    rows: list[dict[str, str]] = []
    for source in registry:
        dataset = source["dataset"]
        raw_count, date_range, columns = raw_profile(source["raw_path"])
        readiness_status = readiness.get(dataset, {}).get("status", "not tracked")
        status = inventory_status(readiness_status, source["offline_status"])
        heldout_status = heldout.get(source["source_family"], "")
        bridge_status = bridges.get(dataset, "")
        related_paths = RELATED_RAW.get(dataset, ())
        related_profiles = [raw_profile(str(path)) for path in related_paths]
        rows.append({
            "sourceFamily": source["source_family"],
            "sourceName": source["source_name"],
            "dataset": dataset,
            "priority": source["priority"],
            "inventoryStatus": status,
            "readinessStatus": readiness_status,
            "offlineStatus": source["offline_status"],
            "boundaryCategory": source["boundary_category"],
            "observableSignal": source["observable_signal"],
            "simulatorProxy": source["simulator_proxy"],
            "supportedMetric": source["supported_metric"],
            "claimBoundary": source["claim_boundary"],
            "rowCount": raw_count,
            "dateRange": date_range,
            "unitOfObservation": source["unit_of_observation"],
            "computedMetricCount": str(metrics_by_dataset.get(dataset, 0)),
            "bridgeStatus": bridge_status,
            "heldoutStatus": heldout_status,
            "evidenceStatus": evidence_label(source, status, heldout_status, bridge_status),
            "apiKeyRequired": source["api_key_required"],
            "networkRequired": source["network_required"],
            "cachePath": source["cache_path"],
            "rawPath": source["raw_path"],
            "relatedRawPaths": ";".join(str(path) for path in related_paths),
            "relatedRawRowCounts": ";".join(profile[0] for profile in related_profiles),
            "relatedRawDateRanges": ";".join(profile[1] for profile in related_profiles),
            "transformationScript": source["transformation_script"],
            "columns": columns,
            "limitations": source["limitations"],
            "nextStep": source["next_step"],
            "licenseAccessNotes": source["license_access_notes"],
        })

    write_inventory(rows)
    write_boundary_matrix(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {BOUNDARY_CSV}")
    print(f"Wrote {BOUNDARY_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
