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
        "| Family | Champion | Dir. | Prod. | Comp. | Rep. quality | Risk ctrl. | Malapp. | Low public support |",
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


def label_width(label: str) -> float:
    return max(4.4, len(label) * 1.25)


def label_box(label_x: float, label_y: float, label: str, anchor: str) -> tuple[float, float, float, float]:
    width = label_width(label)
    if anchor == "l":
        left = label_x
        right = label_x + width
    elif anchor == "r":
        left = label_x - width
        right = label_x
    else:
        left = label_x - width / 2.0
        right = label_x + width / 2.0
    return left, right, label_y - 2.25, label_y + 2.25


def point_box(x: float, y: float) -> tuple[float, float, float, float]:
    return x - 1.9, x + 1.9, y - 1.9, y + 1.9


def expanded_box(box: tuple[float, float, float, float], padding_x: float = 0.7,
                 padding_y: float = 0.55) -> tuple[float, float, float, float]:
    left, right, bottom, top = box
    return left - padding_x, right + padding_x, bottom - padding_y, top + padding_y


def boxes_overlap(left_a: float, right_a: float, bottom_a: float, top_a: float,
                  left_b: float, right_b: float, bottom_b: float, top_b: float) -> bool:
    return left_a < right_b and right_a > left_b and bottom_a < top_b and top_a > bottom_b


def clamp_label_position(
    label_x: float,
    label_y: float,
    label: str,
    anchor: str,
    picture_width: float,
    picture_height: float,
) -> tuple[float, float]:
    margin = 0.8
    left, right, bottom, top = label_box(label_x, label_y, label, anchor)
    if left < margin:
        label_x += margin - left
    elif right > picture_width - margin:
        label_x -= right - (picture_width - margin)
    left, right, bottom, top = label_box(label_x, label_y, label, anchor)
    if bottom < margin:
        label_y += margin - bottom
    elif top > picture_height - margin:
        label_y -= top - (picture_height - margin)
    return label_x, label_y


def auto_label_offsets(
    points: list[tuple[str, float, float]],
    picture_width: float,
    picture_height: float,
) -> dict[str, tuple[float, float, str]]:
    candidates: list[tuple[float, float, str]] = []
    for radius_x, radius_y in ((4.0, 6.4), (7.8, 8.0), (11.8, 9.8), (15.8, 11.2), (19.5, 12.4)):
        candidates.extend([
            (radius_x, radius_y, "l"),
            (-radius_x, radius_y, "r"),
            (radius_x, -radius_y, "l"),
            (-radius_x, -radius_y, "r"),
            (radius_x + 3.2, 0.9, "l"),
            (-(radius_x + 3.2), 0.9, "r"),
            (0.0, radius_y + 2.0, "c"),
            (0.0, -(radius_y + 2.0), "c"),
            (radius_x + 5.0, radius_y * 0.55, "l"),
            (-(radius_x + 5.0), radius_y * 0.55, "r"),
            (radius_x + 5.0, -radius_y * 0.55, "l"),
            (-(radius_x + 5.0), -radius_y * 0.55, "r"),
        ])
    placed: list[tuple[float, float, float, float]] = []
    point_boxes = [point_box(x, y) for _label, x, y in points]
    placements: dict[str, tuple[float, float, str]] = {}
    def local_density(point: tuple[str, float, float]) -> int:
        _label, x, y = point
        return sum(1 for _other_label, other_x, other_y in points
                   if ((x - other_x) ** 2 + (y - other_y) ** 2) ** 0.5 <= 12.0)

    ordered = sorted(points, key=lambda item: (-local_density(item), item[1], -item[2]))
    for label, x, y in ordered:
        selected: tuple[float, float, str] | None = None
        selected_box: tuple[float, float, float, float] | None = None
        for dx, dy, anchor in candidates:
            label_x, label_y = clamp_label_position(
                x + dx,
                y + dy,
                label,
                anchor,
                picture_width,
                picture_height,
            )
            box = label_box(label_x, label_y, label, anchor)
            padded_box = expanded_box(box)
            if any(boxes_overlap(*padded_box, *point) for point in point_boxes):
                continue
            if any(boxes_overlap(*padded_box, *existing) for existing in placed):
                continue
            selected = (label_x - x, label_y - y, anchor)
            selected_box = padded_box
            break
        if selected is None:
            dx, dy, anchor = candidates[-1]
            label_x, label_y = clamp_label_position(
                x + dx,
                y + dy,
                label,
                anchor,
                picture_width,
                picture_height,
            )
            selected = (label_x - x, label_y - y, anchor)
            selected_box = expanded_box(label_box(label_x, label_y, label, anchor))
        placements[label] = selected
        placed.append(selected_box)
    return placements


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
    picture_width = 128.0
    picture_height = 84.0
    x_min, x_max = 0.20, 0.38
    y_min, y_max = 0.22, 0.31

    def scaled(value: float, axis_min: float, axis_max: float) -> float:
        if value <= axis_min:
            return 0.0
        if value >= axis_max:
            return 1.0
        return (value - axis_min) / (axis_max - axis_min)

    preferred_offsets = {
        "ASSIGN": (-4.0, 7.0, "r"),
        "COMMP": (0.0, 7.0, "c"),
        "BICAM": (0.0, 7.0, "c"),
        "ROUTE": (8.3, 7.4, "l"),
        "OTHER": (-7.0, -5.0, "r"),
        "CONV": (3.0, 3.0, "l"),
        "REVIEW": (0.0, 9.5, "c"),
        "SEAT": (-3.0, -7.0, "r"),
        "SELECT": (6.0, -3.0, "l"),
        "UPPER": (6.0, 4.0, "l"),
    }

    point_rows: list[tuple[dict[str, str], str, float, float]] = []
    for row in champs:
        x = left + scaled(f(row, "productivity"), x_min, x_max) * width
        y = bottom + scaled(f(row, "compromise"), y_min, y_max) * height
        point_rows.append((row, label_for(row["family"]), x, y))
    placements = auto_label_offsets(
        [(label, x, y) for _row, label, x, y in point_rows],
        picture_width,
        picture_height,
    )
    placements.update(preferred_offsets)
    lines = [
        "% Auto-generated by scripts/reporting/summarize_chamber_structure.py",
        r"\begingroup",
        r"\setlength{\unitlength}{1mm}",
        r"\begin{picture}(128,84)",
        r"\scriptsize",
    ]
    for tick in [0.20, 0.25, 0.30, 0.35]:
        x = left + scaled(tick, x_min, x_max) * width
        label = f"{tick:.2f}"
        lines.append(fr"\put({x:.1f},{bottom:.1f}){{\color{{black!15}}\line(0,1){{{height:.1f}}}}}")
        lines.append(fr"\put({x:.1f},{bottom - 3.0:.1f}){{\makebox(0,0){{{label}}}}}")
    for tick in [0.22, 0.25, 0.28, 0.31]:
        y = bottom + scaled(tick, y_min, y_max) * height
        label = f"{tick:.2f}"
        lines.append(fr"\put({left:.1f},{y:.1f}){{\color{{black!15}}\line(1,0){{{width:.1f}}}}}")
        lines.append(fr"\put({left - 4.0:.1f},{y:.1f}){{\makebox(0,0)[r]{{{label}}}}}")
    lines.append(fr"\put({left:.1f},{bottom:.1f}){{\line(1,0){{{width:.1f}}}}}")
    lines.append(fr"\put({left:.1f},{bottom:.1f}){{\line(0,1){{{height:.1f}}}}}")
    for row, label, x, y in sorted(point_rows, key=lambda item: item[0]["family"] == "Conventional benchmark"):
        dx, dy, align = placements[label]
        label_x = x + dx
        label_y = y + dy
        point_color = "red" if row["family"] == "Conventional benchmark" else "black"
        label_color = "red" if row["family"] == "Conventional benchmark" else "black"
        size = "2.2" if row["family"] == "Conventional benchmark" else "1.6"
        lines.append(fr"\put({x:.1f},{y:.1f}){{\makebox(0,0){{\color{{{point_color}}}\rule{{{size}mm}}{{{size}mm}}}}}}")
        lines.append(r"\linethickness{0.14mm}")
        leader_color = "red!55" if row["family"] == "Conventional benchmark" else "black!42"
        lines.append(fr"{{\color{{{leader_color}}}\qbezier({x:.1f},{y:.1f})({x + dx / 2:.1f},{y + dy / 2:.1f})({label_x:.1f},{label_y:.1f})}}")
        lines.append(r"\linethickness{0.25mm}")
        lines.append(
            f"% point-label label={label} pointX={x:.1f} pointY={y:.1f} "
            f"labelX={label_x:.1f} labelY={label_y:.1f} anchor={align} leader=1"
        )
        lines.append(fr"\put({label_x:.1f},{label_y:.1f}){{\makebox(0,0)[{align}]{{\color{{{label_color}}}{label}}}}}")
    lines.append(fr"\put({left + width / 2:.1f},{bottom - 10.0:.1f}){{\makebox(0,0){{Productivity $\uparrow$}}}}")
    lines.append(fr"\put({left - 15.0:.1f},{bottom + height / 2:.1f}){{\makebox(0,0){{\rotatebox{{90}}{{Compromise $\uparrow$}}}}}}")
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
