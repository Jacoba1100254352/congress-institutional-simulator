#!/usr/bin/env python3
"""Summarize chamber/apportionment/committee campaign outputs for reports and paper."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "reports" / "simulation-chamber-structure.csv"
CHAMPION_MD = ROOT / "reports" / "chamber-family-champions.md"
STRESS_MD = ROOT / "reports" / "chamber-stress-screen.md"
PAPER_TABLE = ROOT / "paper" / "figures" / "chamber_family_table.tex"
PAPER_FIGURE = ROOT / "paper" / "figures" / "chamber_productivity_compromise.tex"


def f(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "0") or 0.0)
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def family(row: dict[str, str]) -> str:
    name = row["scenario"].lower()
    if "stylized u.s" in name or name == "unicameral simple majority":
        return "Conventional benchmark"
    if "proportional" in name or "equal-population" in name:
        return "Seat allocation"
    if "malapportioned" in name or "territorial" in name or "appointed upper" in name:
        return "Upper-chamber composition"
    if "origin" in name or "routing" in name or "preclearance" in name or "emergency" in name:
        return "Origination and routing"
    if "revision" in name or "navette" in name or "joint-sitting" in name or "mediation" in name or "last-offer" in name or "override" in name or "amendment-only" in name or "absolute veto" in name:
        return "Bicameral conflict"
    if "committee" in name and ("fast-track" in name or "scrutiny" in name or "public-accounts" in name or "legal" in name or "discharge" in name or "priority" in name or "veto player" in name):
        return "Committee power"
    if "committee" in name:
        return "Committee assignment"
    if "eligibility" in name or "appointment" in name or "recusal" in name:
        return "Selection and retention"
    if "ex ante" in name or "clearance" in name or "independent" in name or "insulation" in name:
        return "Independent review"
    return "Other chamber design"


def aggregate(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_scenario: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_scenario[row["scenario"]].append(row)

    aggregated = []
    for scenario, scenario_rows in by_scenario.items():
        first = scenario_rows[0]
        output = {
            "scenario": scenario,
            "family": family(first),
        }
        for key in [
            "directionalScore",
            "productivity",
            "compromise",
            "representativeQuality",
            "riskControl",
            "administrativeFeasibility",
            "weakPublicMandatePassage",
            "populationSeatDistortion",
            "malapportionmentIndex",
            "interChamberConflictRate",
            "committeeCaptureIndex",
            "exAnteReviewRate",
        ]:
            output[key] = f"{mean([f(row, key) for row in scenario_rows]):.6f}"
        aggregated.append(output)
    return aggregated


def champions(aggregated: list[dict[str, str]]) -> list[dict[str, str]]:
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in aggregated:
        by_family[row["family"]].append(row)
    return [
        max(rows, key=lambda row: f(row, "directionalScore"))
        for _, rows in sorted(by_family.items())
    ]


def write_champion_md(champs: list[dict[str, str]]) -> None:
    lines = [
        "# Chamber Family Champions",
        "",
        "Fixed-rule champion screen for the chamber/apportionment/committee campaign. Each row is the highest directional-score scenario within a structural family, averaged across the chamber campaign's baseline, adversarial, party-system, and timeline cases.",
        "",
        "| Family | Champion | Dir. | Prod. | Comp. | Rep. quality | Risk ctrl. | Malapp. | Weak mandate |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in champs:
        lines.append(
            f"| {row['family']} | {row['scenario']} | {f(row, 'directionalScore'):.3f} | "
            f"{f(row, 'productivity'):.3f} | {f(row, 'compromise'):.3f} | "
            f"{f(row, 'representativeQuality'):.3f} | {f(row, 'riskControl'):.3f} | "
            f"{f(row, 'malapportionmentIndex'):.3f} | {f(row, 'weakPublicMandatePassage'):.3f} |"
        )
    CHAMPION_MD.write_text("\n".join(lines) + "\n")


def write_stress_md(rows: list[dict[str, str]]) -> None:
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_case[row["caseName"]].append(row)
    lines = [
        "# Chamber Stress Screen",
        "",
        "Best chamber/committee scenario in each stress case, using the same directional diagnostic as the main report. This is a sensitivity screen, not a validation claim.",
        "",
        "| Case | Best scenario | Dir. | Prod. | Comp. | Risk ctrl. | Inter-chamber conflict | Committee capture | Ex ante review |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for case_name in sorted(by_case):
        best = max(by_case[case_name], key=lambda row: f(row, "directionalScore"))
        lines.append(
            f"| {case_name} | {best['scenario']} | {f(best, 'directionalScore'):.3f} | "
            f"{f(best, 'productivity'):.3f} | {f(best, 'compromise'):.3f} | "
            f"{f(best, 'riskControl'):.3f} | {f(best, 'interChamberConflictRate'):.3f} | "
            f"{f(best, 'committeeCaptureIndex'):.3f} | {f(best, 'exAnteReviewRate'):.3f} |"
        )
    STRESS_MD.write_text("\n".join(lines) + "\n")


def label_for(family_name: str) -> str:
    labels = {
        "Conventional benchmark": "CONV",
        "Seat allocation": "SEAT",
        "Upper-chamber composition": "UPPER",
        "Origination and routing": "ROUTE",
        "Bicameral conflict": "BICAM",
        "Committee assignment": "ASSIGN",
        "Committee power": "COMMP",
        "Selection and retention": "SELECT",
        "Independent review": "REVIEW",
        "Other chamber design": "OTHER",
    }
    return labels.get(family_name, "OTHER")


def write_paper_table(champs: list[dict[str, str]]) -> None:
    rows = [
        r"\begin{table}",
        r"  \caption{Chamber, apportionment, committee, and review family champions from the chamber-structure supplement. Values are averaged across the chamber campaign cases.}",
        r"  \label{tab:chamber-family-champions}",
        r"  \Description{Compact table of chamber-family champion scenarios and core metrics.}",
        r"  \scriptsize",
        r"  \begin{tabular}{llrrrr}",
        r"    \toprule",
        r"    Label & Family champion & Prod. & Comp. & Risk & Malapp. \\",
        r"    \midrule",
    ]
    for row in champs:
        rows.append(
            f"    {label_for(row['family'])} & {escape(row['family'])} & "
            f"{f(row, 'productivity'):.2f} & {f(row, 'compromise'):.2f} & "
            f"{f(row, 'riskControl'):.2f} & {f(row, 'malapportionmentIndex'):.2f} \\\\"
        )
    rows.extend([
        r"    \bottomrule",
        r"  \end{tabular}",
        r"\end{table}",
    ])
    PAPER_TABLE.write_text("% Auto-generated by scripts/reporting/summarize_chamber_structure.py\n" + "\n".join(rows) + "\n")


def write_paper_figure(champs: list[dict[str, str]]) -> None:
    width = 95.0
    height = 58.0
    left = 22.0
    bottom = 14.0
    lines = [
        "% Auto-generated by scripts/reporting/summarize_chamber_structure.py",
        r"\begingroup",
        r"\setlength{\unitlength}{1mm}",
        r"\begin{picture}(128,84)",
        r"\scriptsize",
    ]
    for tick in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x = left + tick * width
        y = bottom + tick * height
        label = "1" if tick == 1.0 else ("0" if tick == 0.0 else f"{tick:.2g}")
        lines.append(fr"\put({x:.1f},{bottom:.1f}){{\color{{black!15}}\line(0,1){{{height:.1f}}}}}")
        lines.append(fr"\put({left:.1f},{y:.1f}){{\color{{black!15}}\line(1,0){{{width:.1f}}}}}")
        lines.append(fr"\put({x:.1f},{bottom - 3.0:.1f}){{\makebox(0,0){{{label}}}}}")
        lines.append(fr"\put({left - 4.0:.1f},{y:.1f}){{\makebox(0,0)[r]{{{label}}}}}")
    lines.append(fr"\put({left:.1f},{bottom:.1f}){{\line(1,0){{{width:.1f}}}}}")
    lines.append(fr"\put({left:.1f},{bottom:.1f}){{\line(0,1){{{height:.1f}}}}}")
    offsets = [(3, 5, "l"), (-3, 5, "r"), (3, -5, "l"), (-3, -5, "r"), (5, 1, "l"), (-5, 1, "r")]
    for index, row in enumerate(champs):
        x = left + max(0.0, min(1.0, f(row, "productivity"))) * width
        y = bottom + max(0.0, min(1.0, f(row, "compromise"))) * height
        # Keep the light end printable. The previous black!15 floor made most
        # non-malapportioned labels nearly indistinguishable from the grid.
        malapportionment = max(0.0, min(1.0, f(row, "malapportionmentIndex")))
        intensity = int(round(45 + 45 * malapportionment))
        label = label_for(row["family"])
        dx, dy, align = offsets[index % len(offsets)]
        color = "red" if row["family"] == "Conventional benchmark" else f"black!{intensity}"
        size = "2.0" if row["family"] == "Conventional benchmark" else "1.6"
        lines.append(fr"\put({x:.1f},{y:.1f}){{\makebox(0,0){{\color{{{color}}}\rule{{{size}mm}}{{{size}mm}}}}}}")
        lines.append(r"\linethickness{0.10mm}")
        leader_color = "red!55" if row["family"] == "Conventional benchmark" else "black!50"
        lines.append(fr"{{\color{{{leader_color}}}\qbezier[6]({x:.1f},{y:.1f})({x + dx / 2:.1f},{y + dy / 2:.1f})({x + dx:.1f},{y + dy:.1f})}}")
        lines.append(r"\linethickness{0.25mm}")
        lines.append(fr"\put({x + dx:.1f},{y + dy:.1f}){{\makebox(0,0)[{align}]{{\color{{{color}}}{label}}}}}")
    lines.append(fr"\put({left + width / 2:.1f},{bottom - 10.0:.1f}){{\makebox(0,0){{Productivity $\uparrow$}}}}")
    lines.append(fr"\put({left - 15.0:.1f},{bottom + height / 2:.1f}){{\rotatebox{{90}}{{Compromise $\uparrow$}}}}")
    lines.append(fr"\put({left + width - 18.0:.1f},{bottom + height + 4.0:.1f}){{\makebox(0,0)[l]{{darker = more malapportioned}}}}")
    lines.extend([r"\end{picture}", r"\endgroup"])
    PAPER_FIGURE.write_text("\n".join(lines) + "\n")


def escape(value: str) -> str:
    return value.replace("&", r"\&")


def main() -> int:
    if not CSV.exists():
        raise SystemExit(f"Missing {CSV}; run make chamber-structure first.")
    rows = list(csv.DictReader(CSV.read_text().splitlines()))
    aggregated = aggregate(rows)
    champs = champions(aggregated)
    write_champion_md(champs)
    write_stress_md(rows)
    write_paper_table(champs)
    write_paper_figure(champs)
    print(f"Wrote {CHAMPION_MD}")
    print(f"Wrote {STRESS_MD}")
    print(f"Wrote {PAPER_TABLE}")
    print(f"Wrote {PAPER_FIGURE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
