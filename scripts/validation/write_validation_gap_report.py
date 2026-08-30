#!/usr/bin/env python3
"""Write a registry-backed empirical boundary report.

The readiness, inventory, bridge, and held-out reports intentionally avoid
pretending that raw-data presence is validation. This script turns the current
state into a compact paper-facing artifact: source-family readiness, supported
claim boundary, and the next source needed to close each gap.
"""

from __future__ import annotations

import csv
from pathlib import Path


REGISTRY_CSV = Path("data/validation/source-registry.csv")
READINESS_CSV = Path("reports/empirical-validation-readiness.csv")
INVENTORY_CSV = Path("reports/empirical-data-inventory.csv")
BRIDGE_CSV = Path("reports/empirical-bridge.csv")
HELDOUT_CSV = Path("reports/empirical-flow-heldout.csv")
LINKAGE_CSV = Path("reports/empirical-linkage-report.csv")
OUT_CSV = Path("reports/empirical-validation-gap-report.csv")
OUT_MD = Path("reports/empirical-validation-gap-report.md")
OUT_TEX = Path("paper/figures/empirical_validation_gap_table.tex")
LINKED_STATUSES = {"linked", "metadata linked", "partially linked"}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def by_field(path: Path, field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in read_csv(path) if row.get(field)}


def bridge_statuses() -> dict[str, str]:
    statuses: dict[str, set[str]] = {}
    for row in read_csv(BRIDGE_CSV):
        statuses.setdefault(row["rawDataset"], set()).add(row["bridgeStatus"])
    return {dataset: "; ".join(sorted(values)) for dataset, values in statuses.items()}


def heldout_statuses() -> dict[str, str]:
    statuses: dict[str, set[str]] = {}
    for row in read_csv(HELDOUT_CSV):
        statuses.setdefault(row["sourceFamily"], set()).add(row["heldoutTargetStatus"])
    return {source: "; ".join(sorted(values)) for source, values in statuses.items()}


def paper_status(
    boundary: str,
    inventory_status: str,
    bridge_status: str,
    heldout_status: str,
) -> str:
    if boundary == "held-out benchmark" and heldout_status:
        return "held-out benchmark"
    if inventory_status == "ready" and boundary in {"flow sanity check", "calibration proxy"}:
        return boundary
    if inventory_status == "ready" and bridge_status:
        return "empirical check"
    if inventory_status == "schema gap":
        return "schema gap"
    return "synthetic only"


def tex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(replacements.get(char, char) for char in text)


def main() -> int:
    registry = read_csv(REGISTRY_CSV)
    if not registry:
        raise SystemExit(f"{REGISTRY_CSV} is missing; create the source registry first.")
    readiness = by_field(READINESS_CSV, "dataset")
    inventory = by_field(INVENTORY_CSV, "sourceFamily")
    linkage = by_field(LINKAGE_CSV, "sourceFamily")
    bridges = bridge_statuses()
    heldouts = heldout_statuses()

    rows: list[dict[str, str]] = []
    for source in registry:
        family = source["source_family"]
        dataset = source["dataset"]
        inventory_row = inventory.get(family, {})
        readiness_row = readiness.get(dataset, {})
        inventory_status = inventory_row.get("inventoryStatus", readiness_row.get("status", "missing"))
        bridge_status = bridges.get(dataset, "")
        heldout_status = heldouts.get(family, "")
        linkage_row = linkage.get(family, {})
        status = paper_status(source["boundary_category"], inventory_status, bridge_status, heldout_status)
        rows.append({
            "sourceFamily": family,
            "sourceName": source["source_name"],
            "dataset": dataset,
            "inputStatus": readiness_row.get("status", inventory_status),
            "inventoryStatus": inventory_status,
            "paperStatus": status,
            "boundaryCategory": source["boundary_category"],
            "priority": source["priority"],
            "offlineStatus": source["offline_status"],
            "rowCount": inventory_row.get("rowCount", "0"),
            "dateRange": inventory_row.get("dateRange", ""),
            "observableSignal": source["observable_signal"],
            "simulatorProxy": source["simulator_proxy"],
            "supportedMetric": source["supported_metric"],
            "paperBoundary": source["claim_boundary"],
            "nextSource": source["next_step"],
            "bridgeStatuses": bridge_status if bridge_status else "no bridge metric",
            "heldoutStatus": heldout_status if heldout_status else "not run",
            "linkageStatus": linkage_row.get("linkageStatus", "not reported"),
            "linkedTo": linkage_row.get("linkedTo", ""),
            "linkedRows": (
                f"{linkage_row.get('linkedRows', '0')}/{linkage_row.get('totalRows', '0')}"
                if linkage_row else "0/0"
            ),
            "linkedShare": linkage_row.get("linkedShare", "0.000"),
            "linkageBoundary": linkage_row.get("linkageBoundary", "No linkage report row was generated."),
            "nextLinkStep": linkage_row.get("nextLinkStep", source["next_step"]),
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    ready = sum(1 for row in rows if row["inventoryStatus"] == "ready")
    heldout = sum(1 for row in rows if row["paperStatus"] == "held-out benchmark")
    linked = sum(1 for row in rows if row["linkageStatus"] in LINKED_STATUSES)
    missing = sum(1 for row in rows if row["paperStatus"] == "synthetic only")
    high_missing = [
        row["sourceFamily"]
        for row in rows
        if row["paperStatus"] == "synthetic only" and row["priority"] == "high"
    ]
    high_unlinked = [
        row["sourceFamily"]
        for row in rows
        if row["priority"] == "high" and row["linkageStatus"] not in LINKED_STATUSES
    ]
    lines = [
        "# Empirical Boundary Report",
        "",
        "This report separates source-family evidence from claims that remain synthetic. It is generated from the source registry, readiness report, empirical data inventory, bridge report, held-out benchmark report, and linkage report.",
        "",
        f"- Source families inventoried: {len(rows)}",
        f"- Ready or cached source families: {ready} / {len(rows)}",
        f"- Held-out benchmark families: {heldout} / {len(rows)}",
        f"- Linked, metadata-linked, or partially linked source families: {linked} / {len(rows)}",
        f"- Synthetic-only families: {missing} / {len(rows)}",
        f"- Highest-priority missing areas: {', '.join(high_missing) if high_missing else 'none'}",
        f"- Highest-priority unlinked linkage areas: {', '.join(high_unlinked) if high_unlinked else 'none'}",
        "",
        "| Source family | Dataset | Inventory status | Paper status | Linkage | Priority | Rows | Boundary for claims | Next evidence step |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        linkage_summary = f"{row['linkageStatus']} ({row['linkedRows']}, {row['linkedShare']})"
        lines.append(
            f"| {row['sourceFamily']} | `{row['dataset']}` | {row['inventoryStatus']} | "
            f"{row['paperStatus']} | {linkage_summary} | {row['priority']} | {row['rowCount']} | "
            f"{row['paperBoundary']} Linkage boundary: {row['linkageBoundary']} | {row['nextLinkStep']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")

    table_rows = [
        row for row in rows
        if row["priority"] == "high" or row["paperStatus"] in {"held-out benchmark", "flow sanity check", "calibration proxy"}
    ]
    tex_lines = [
        r"\clearpage",
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\LTpre}{0pt}",
        r"\setlength{\LTpost}{0pt}",
        r"\begin{longtable}{>{\raggedright\arraybackslash}p{0.21\linewidth}>{\raggedright\arraybackslash}p{0.18\linewidth}>{\raggedright\arraybackslash}p{0.53\linewidth}}",
        r"\caption{Empirical boundary by source family. Held-out benchmark rows have a deterministic held-out empirical check; flow sanity and calibration proxy rows remain limited empirical screens. Full next-source acceptance gates appear in the generated empirical-boundary report.}",
        r"\label{tab:empirical-validation-gap} \\",
        r"\toprule",
        r"Source family & Status & Claim boundary \\",
        r"\midrule",
        r"\endfirsthead",
        r"\multicolumn{3}{l}{\small Empirical boundary by source family (continued)} \\",
        r"\toprule",
        r"Source family & Status & Claim boundary \\",
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{3}{r}{\footnotesize Continued on next page} \\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]
    for row in table_rows:
        boundary = f"{row['paperBoundary']} Linkage: {row['linkageStatus']}."
        tex_lines.append(
            f"{tex_escape(row['sourceFamily'])} & {tex_escape(row['paperStatus'])} "
            f"({tex_escape(row['priority'])}) & {tex_escape(boundary)} \\\\"
        )
    tex_lines.extend([
        r"\end{longtable}",
        r"\endgroup",
        r"\clearpage",
    ])
    OUT_TEX.write_text("\n".join(tex_lines) + "\n")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
