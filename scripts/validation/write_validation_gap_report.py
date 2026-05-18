#!/usr/bin/env python3
"""Write a paper-facing empirical boundary report.

The readiness and empirical-check reports intentionally avoid pretending that
missing raw data is validation. This script turns that state into a compact
artifact the paper can cite: what is already inspectable, what is still
synthetic, and which source family would close each gap.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


READINESS_CSV = Path("reports/empirical-validation-readiness.csv")
BRIDGE_CSV = Path("reports/empirical-bridge.csv")
OUT_CSV = Path("reports/empirical-validation-gap-report.csv")
OUT_MD = Path("reports/empirical-validation-gap-report.md")
OUT_TEX = Path("paper/figures/empirical_validation_gap_table.tex")


@dataclass(frozen=True)
class GapNote:
    area: str
    paper_boundary: str
    next_source: str
    priority: str


GAP_NOTES = {
    "voteview_rollcalls.csv": GapNote(
        "Roll-call behavior",
        "Party-unity and coalition-size proxies are inspectable.",
        "Extend Voteview coverage across more Congresses and chambers.",
        "available",
    ),
    "bill_progression.csv": GapNote(
        "Bill progression",
        "Floor load, committee reporting, and enactment-rate proxies are inspectable.",
        "Replace the bounded sample with a full Congress.gov/govinfo bill census.",
        "available",
    ),
    "lobbying_disclosure.csv": GapNote(
        "Lobbying disclosure",
        "Lobby-spend concentration is inspectable, but not yet tied to bill-level outcomes.",
        "Link LDA clients/issues to bill topics and committee referrals.",
        "available",
    ),
    "topic_throughput.csv": GapNote(
        "Topic throughput",
        "Agenda diversity and topic enactment proxies are inspectable.",
        "Map topics to CAP/congressional subject taxonomies across sessions.",
        "available",
    ),
    "sponsor_success.csv": GapNote(
        "Sponsor access",
        "Proposal-access concentration is inspectable with a rough sponsor sample.",
        "Replace with CEL-style sponsor effectiveness or complete sponsor histories.",
        "available",
    ),
    "committee_activity.csv": GapNote(
        "Committee gatekeeping",
        "Reporting and referral proxies are inspectable; hearings remain rough.",
        "Add committee hearing calendars, markup records, amendments, and discharge petitions.",
        "available",
    ),
    "district_public_opinion.csv": GapNote(
        "Public support",
        "District public-will and affected-group legitimacy remain synthetic.",
        "Add district-level MRP/CCES-style opinion, turnout, and affected-population estimates.",
        "high",
    ),
    "campaign_finance.csv": GapNote(
        "Campaign finance",
        "Money-in-politics effects remain represented by lobbying proxies.",
        "Add FEC/OpenFEC receipts, independent expenditures, and industry classifications.",
        "high",
    ),
    "court_review.csv": GapNote(
        "Court review",
        "Judicial-review and emergency-docket behavior remain speculative prototypes.",
        "Add Supreme Court Database/emergency-order coding and invalidation outcomes.",
        "medium",
    ),
    "rulemaking_implementation.csv": GapNote(
        "Implementation feedback",
        "Implementation delay, nonenforcement, and capacity feedback remain synthetic.",
        "Add Federal Register, Unified Agenda, Regulations.gov, and agency enforcement rows.",
        "high",
    ),
    "law_revision_history.csv": GapNote(
        "Law revision",
        "Law-registry correction and sunset dynamics remain synthetic.",
        "Add statutory lineage for amendment, reauthorization, repeal, expiration, and invalidation.",
        "high",
    ),
    "comparative_institutions.csv": GapNote(
        "Comparative institutions",
        "Chamber and party-system breadth is a sensitivity analysis, not cross-national fit.",
        "Add ParlGov, V-Dem, IPU/chamber data, electoral systems, and productivity proxies.",
        "medium",
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def bridge_statuses() -> dict[str, set[str]]:
    statuses: dict[str, set[str]] = {}
    for row in read_csv(BRIDGE_CSV):
        statuses.setdefault(row["rawDataset"], set()).add(row["bridgeStatus"])
    return statuses


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


def paper_status(status: str, bridge: set[str]) -> str:
    if status == "ready" and bridge and bridge <= {"raw summary available"}:
        return "empirical check"
    if status == "ready":
        return "raw ready"
    if status == "incomplete":
        return "schema gap"
    return "synthetic only"


def main() -> int:
    readiness = read_csv(READINESS_CSV)
    if not readiness:
        raise SystemExit(f"{READINESS_CSV} is missing; run make validation-readiness first.")
    bridges = bridge_statuses()

    rows: list[dict[str, str]] = []
    for row in readiness:
        dataset = row["dataset"]
        note = GAP_NOTES[dataset]
        statuses = bridges.get(dataset, set())
        rows.append({
            "area": note.area,
            "dataset": dataset,
            "inputStatus": row["status"],
            "paperStatus": paper_status(row["status"], statuses),
            "priority": note.priority,
            "paperBoundary": note.paper_boundary,
            "nextSource": note.next_source,
            "bridgeStatuses": "; ".join(sorted(statuses)) if statuses else "no bridge metric",
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    ready = sum(1 for row in rows if row["inputStatus"] == "ready")
    missing = sum(1 for row in rows if row["inputStatus"] == "missing")
    high_missing = [
        row["area"]
        for row in rows
        if row["inputStatus"] != "ready" and row["priority"] == "high"
    ]
    lines = [
        "# Empirical Boundary Report",
        "",
        "This report separates what the paper can inspect empirically from what remains a synthetic or speculative model component. It is generated from the validation-readiness and empirical-check artifacts.",
        "",
        f"- Raw validation inputs available: {ready} / {len(rows)}",
        f"- Raw validation inputs missing or incomplete: {missing} / {len(rows)}",
        f"- Highest-priority missing areas: {', '.join(high_missing) if high_missing else 'none'}",
        "",
        "| Area | Dataset | Input status | Paper status | Priority | Boundary for claims | Next source family |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['area']} | `{row['dataset']}` | {row['inputStatus']} | "
            f"{row['paperStatus']} | {row['priority']} | {row['paperBoundary']} | "
            f"{row['nextSource']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")

    table_rows = [
        row for row in rows
        if row["priority"] == "high" or row["paperStatus"] == "empirical check"
    ]
    tex_lines = [
        r"\begin{table}",
        r"\centering",
        r"\caption{Empirical boundary. Rows marked empirical check have shaped raw inputs and simulator proxy summaries; rows marked synthetic only are still modeled without raw-data support.}",
        r"\label{tab:empirical-validation-gap}",
        r"\small",
        r"\begin{tabular}{p{0.20\linewidth}p{0.20\linewidth}p{0.52\linewidth}}",
        r"\toprule",
        r"Area & Status & Claim boundary / next source \\",
        r"\midrule",
    ]
    for row in table_rows:
        boundary = f"{row['paperBoundary']} Next: {row['nextSource']}"
        tex_lines.append(
            f"{tex_escape(row['area'])} & {tex_escape(row['paperStatus'])} "
            f"({tex_escape(row['priority'])}) & {tex_escape(boundary)} \\\\"
        )
    tex_lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])
    OUT_TEX.write_text("\n".join(tex_lines) + "\n")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
