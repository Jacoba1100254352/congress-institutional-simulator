#!/usr/bin/env python3
"""Generate ACM-friendly LaTeX figure fragments from campaign CSV output."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_CSV_PATH = ROOT / "reports" / "simulation-campaign-v21-paper.csv"
FIGURE_DIR = ROOT / "paper" / "figures"
CURRENT_SYSTEM_KEY = "current-system"
TABLE_SCENARIOS = [
    (CURRENT_SYSTEM_KEY, "Current"),
    ("simple-majority", "SM"),
    ("supermajority-60", "S60"),
    ("bicameral-majority", "Bic"),
    ("presidential-veto", "Veto"),
    ("default-pass", "DP"),
    ("default-pass-challenge", "Chal."),
    ("default-pass-multiround-mediation-challenge", "MedC"),
    ("default-pass-constituent-citizen-panel", "Panel"),
    ("default-pass-adaptive-track-strict", "Adapt"),
    ("default-pass-alternatives-pairwise", "Pair"),
    ("default-pass-affected-sponsor-gate", "Aff."),
    ("default-pass-public-objection", "Obj."),
    ("default-pass-law-registry", "Law"),
    ("default-pass-cost-lobby-surcharge", "Cost"),
    ("default-pass-deep-strategy-bundle", "Strat"),
]


def broad_case(case_key: str) -> bool:
    return not case_key.startswith("party-system-") and not case_key.startswith("era-")


def party_case(case_key: str) -> bool:
    return case_key.startswith("party-system-")


def timeline_case(case_key: str) -> bool:
    return case_key.startswith("era-")


def read_averages(path: Path, weighted: bool = False, case_filter=broad_case) -> dict[str, dict[str, float]]:
    totals: dict[str, defaultdict[str, float]] = {}
    weights: dict[str, float] = {}
    fields = (
        "productivity",
        "enactedPerRun",
        "avgSupport",
        "welfare",
        "lowSupport",
        "policyShift",
        "proposerGain",
        "lobbyCapture",
        "publicAlignment",
        "publicPreferenceDistortion",
        "minorityHarm",
        "concentratedHarmPassage",
        "challengeRate",
        "compromise",
        "legitimacy",
    )
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if not case_filter(row["caseKey"]):
                continue
            key = row["scenarioKey"]
            weight = float(row.get("caseWeight", "1.0")) if weighted else 1.0
            totals.setdefault(key, defaultdict(float))
            weights[key] = weights.get(key, 0.0) + weight
            for field in fields:
                if field in row and row[field] != "":
                    totals[key][field] += float(row[field]) * weight
    averages = {
        key: {field: value / weights[key] for field, value in values.items()}
        for key, values in totals.items()
    }
    for values in averages.values():
        add_directional_scores(values)
    return averages


def read_case_rows(path: Path, case_filter=broad_case) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [row for row in csv.DictReader(handle) if case_filter(row["caseKey"])]


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def inverse01(value: float) -> float:
    return 1.0 - clamp01(value)


def inverse_range(value: float, max_value: float = 2.0) -> float:
    if max_value <= 0.0:
        return inverse01(value)
    return 1.0 - clamp01(value / max_value)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def add_directional_scores(values: dict[str, float]) -> None:
    representative_quality = mean([
        clamp01(values.get("welfare", 0.0)),
        clamp01(values.get("avgSupport", 0.0)),
        clamp01(values.get("compromise", 0.0)),
        clamp01(values.get("publicAlignment", 0.0)),
        clamp01(values.get("legitimacy", 0.0)),
    ])
    risk_control = mean([
        inverse01(values.get("lowSupport", 0.0)),
        inverse01(values.get("minorityHarm", 0.0)),
        inverse01(values.get("lobbyCapture", 0.0)),
        inverse01(values.get("publicPreferenceDistortion", 0.0)),
        inverse01(values.get("concentratedHarmPassage", 0.0)),
        inverse_range(values.get("proposerGain", 0.0)),
        inverse_range(values.get("policyShift", 0.0)),
    ])
    values["representativeQuality"] = representative_quality
    values["riskControl"] = risk_control
    values["directionalScore"] = mean([
        clamp01(values.get("productivity", 0.0)),
        representative_quality,
        risk_control,
    ])


def read_timeline(path: Path, case_filter=timeline_case) -> tuple[list[str], dict[str, dict[str, dict[str, float]]]]:
    case_names: dict[str, str] = {}
    values: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
    if not path.exists():
        return [], values
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if not case_filter(row["caseKey"]):
                continue
            case_key = row["caseKey"]
            scenario_key = row["scenarioKey"]
            case_names.setdefault(case_key, row["caseName"])
            values[case_key][scenario_key] = {
                "productivity": float(row["productivity"]),
                "compromise": float(row["compromise"]),
                "gridlock": float(row["gridlock"]),
                "lowSupport": float(row["lowSupport"]),
                "contention": contention_index(row),
            }
    return list(case_names.keys()), values


def contention_index(row: dict[str, str]) -> float:
    gridlock = float(row["gridlock"])
    compromise_loss = 1.0 - float(row["compromise"])
    low_support = float(row["lowSupport"])
    return max(0.0, min(1.0, (0.50 * gridlock) + (0.30 * compromise_loss) + (0.20 * low_support)))


def fmt(value: float) -> str:
    return f"{value:.1f}"


def latex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def mean_ci(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    avg = sum(values) / len(values)
    if len(values) == 1:
        return avg, 0.0
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return avg, 1.96 * ((variance ** 0.5) / (len(values) ** 0.5))


def table_value(values: list[float], decimals: int = 3) -> str:
    avg, ci = mean_ci(values)
    return f"{avg:.{decimals}f}$\\pm${ci:.{decimals}f}"


def scenario_case_values(rows: list[dict[str, str]], scenario_key: str, field: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        if row["scenarioKey"] != scenario_key:
            continue
        numeric = {key: float(value) for key, value in row.items() if value and number_like(value)}
        add_directional_scores(numeric)
        values.append(numeric[field])
    return values


def number_like(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def scenario_name(rows: list[dict[str, str]], scenario_key: str) -> str:
    for row in rows:
        if row["scenarioKey"] == scenario_key:
            return row["scenario"]
    return scenario_key


def write_scenario_averages_table(rows: list[dict[str, str]]) -> None:
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Canonical v21-paper scenario averages across broad assumption cases. Entries are mean$\\pm$95\\% sensitivity interval across assumption cases, not seed uncertainty.}",
        "  \\label{tab:scenario-averages}",
        "  \\Description{A generated table comparing selected institutional scenarios using the canonical v21-paper campaign, including sensitivity intervals across broad assumption cases.}",
        "  \\scriptsize",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{llrrrrrr}",
        "    \\toprule",
        "    Label & Scenario & Directional $\\uparrow$ & Prod. $\\uparrow$ & Comp. $\\uparrow$ & Enacted/run & Low-sup. $\\downarrow$ & Risk ctrl. $\\uparrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key, label in TABLE_SCENARIOS:
        if not any(row["scenarioKey"] == scenario_key for row in rows):
            continue
        cells = [
            table_value(scenario_case_values(rows, scenario_key, "directionalScore")),
            table_value(scenario_case_values(rows, scenario_key, "productivity")),
            table_value(scenario_case_values(rows, scenario_key, "compromise")),
            table_value(scenario_case_values(rows, scenario_key, "enactedPerRun"), 2),
            table_value(scenario_case_values(rows, scenario_key, "lowSupport")),
            table_value(scenario_case_values(rows, scenario_key, "riskControl")),
        ]
        scenario = latex_escape(scenario_name(rows, scenario_key))
        if scenario_key == CURRENT_SYSTEM_KEY:
            label = f"\\textcolor{{red}}{{\\textbf{{{label}}}}}"
            scenario = f"\\textcolor{{red}}{{\\textbf{{{scenario}}}}}"
            cells = [f"\\textcolor{{red}}{{\\textbf{{{cell}}}}}" for cell in cells]
        lines.append(
            "    "
            + label
            + " & "
            + scenario
            + " & "
            + " & ".join(cells)
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}%",
        "  }",
        "  \\par\\smallskip\\footnotesize \\emph{Note:} All table entries come from \\texttt{simulation-campaign-v21-paper.csv}. Directional, productivity, compromise, low-support, and risk-control values are normalized scores or rates. \\emph{Enacted/run} is an absolute institutional-load count. Red marks the stylized current-system benchmark.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "scenario_averages_table.tex").write_text("\n".join(lines))


def label_anchor(dx: float, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    return "r" if dx < 0.0 else "l"


def append_labeled_square(
    lines: list[str],
    x: float,
    y: float,
    label: str,
    color: str,
    point_size: str,
    dx: float,
    dy: float,
    anchor: str | None = None,
) -> None:
    lines.append(
        f"\\put({fmt(x)},{fmt(y)})"
        f"{{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}"
    )
    lines.append(f"% point-label label={label} x={fmt(x + dx)} y={fmt(y + dy)}")
    lines.append(
        f"\\put({fmt(x + dx)},{fmt(y + dy)})"
        f"{{\\makebox(0,0)[{label_anchor(dx, anchor)}]{{\\color{{{color}}}{label}}}}}"
    )


def write_productivity_low_support(averages: dict[str, dict[str, float]]) -> None:
    points = [
        ("supermajority-60", "S60", 2.0, 7.6, None),
        (CURRENT_SYSTEM_KEY, "Current", -1.5, 9.0, "r"),
        ("presidential-veto", "Veto", 5.6, 3.6, None),
        ("bicameral-majority", "Bic", 3.0, 8.4, None),
        ("simple-majority", "SM", 2.2, 5.0, None),
        ("default-pass", "DP", 2.4, 8.0, None),
        ("default-pass-constituent-citizen-panel", "Panel", -3.6, 5.5, "r"),
        ("default-pass-proposal-bonds", "Bond", -5.0, 5.2, "r"),
        ("default-pass-affected-sponsor-gate", "Aff.", 2.4, 3.8, None),
        ("default-pass-multiround-mediation", "Med", -5.2, 5.2, "r"),
        ("default-pass-multiround-mediation-challenge", "MedC", -4.6, 5.2, "r"),
        ("default-pass-challenge-minority-bonus", "MinTok", 2.4, -6.2, None),
        ("default-pass-adaptive-track-strict", "Adapt", 2.4, 4.8, None),
        ("default-pass-cost-lobby-surcharge", "Cost", 2.2, 4.6, None),
        ("default-pass-weighted-agenda-lottery", "Lot.", 2.0, 5.2, None),
        ("default-pass-public-objection", "Obj.", 2.2, 5.0, None),
        ("default-pass-alternatives-pairwise", "Pair", 2.0, 5.2, None),
        ("default-pass-alternatives-strategic", "Strat", -5.0, 5.0, "r"),
        ("default-pass-adaptive-proposers", "PropStrat", -4.6, -6.8, "r"),
        ("default-pass-strategic-lobbying", "LobbyLearn", -5.2, 5.6, "r"),
        ("default-pass-challenge", "Chal.", 2.2, -6.4, None),
        ("default-pass-adaptive-track", "Adapt", 2.0, -6.0, None),
        ("default-pass-law-registry", "Law", 2.2, 4.4, None),
    ]
    left, bottom, width, height = 23.0, 14.0, 90.0, 58.0
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,84)",
        "\\scriptsize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = left + tick * width
        y = bottom + tick * height
        lines.extend([
            f"\\put({fmt(x)},{fmt(bottom)}){{\\color{{black!15}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(x)},{fmt(bottom - 3.0)}){{\\makebox(0,0){{{tick:.2g}}}}}",
            f"\\put({fmt(left - 4.0)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
    ])
    for key, label, dx, dy, anchor in points:
        if key not in averages:
            continue
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "1.9mm" if key == CURRENT_SYSTEM_KEY else "1.5mm"
        x = left + averages[key]["productivity"] * width
        y = bottom + averages[key]["lowSupport"] * height
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(3.0)}){{\\makebox(0,0){{Productivity $\\uparrow$ (share enacted)}}}}",
        f"\\put({fmt(5.0)},{fmt(bottom + height / 2.0)}){{\\rotatebox{{90}}{{Low-support passage $\\downarrow$}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "productivity_low_support.tex").write_text("\n".join(lines))


def write_default_pass_deltas(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [
        ("default-pass-constituent-citizen-panel", "Public+panel"),
        (CURRENT_SYSTEM_KEY, "Current system"),
        ("default-pass-proposal-bonds", "Bonds"),
        ("default-pass-affected-sponsor-gate", "Affected sponsor"),
        ("default-pass-multiround-mediation", "Multi-mediation"),
        ("default-pass-multiround-mediation-challenge", "Med.+challenge"),
        ("default-pass-alternatives-strategic", "Strategic alt."),
        ("default-pass-adaptive-proposers", "Adaptive prop."),
        ("default-pass-strategic-lobbying", "Strategic lobby"),
        ("default-pass-challenge-minority-bonus", "Minority tokens"),
        ("default-pass-adaptive-track-strict", "Strict adaptive"),
        ("default-pass-cost-lobby-surcharge", "Lobby-cost"),
        ("default-pass-weighted-agenda-lottery", "Lottery"),
        ("default-pass-public-objection", "Objection"),
        ("default-pass-alternatives-pairwise", "Pairwise"),
        ("default-pass-challenge", "Challenge"),
        ("default-pass-adaptive-track", "Adaptive"),
        ("default-pass-law-registry", "Law reg."),
    ]
    metrics = [
        ("productivity", "Prod.", "black"),
        ("policyShift", "Shift", "black!55"),
        ("proposerGain", "Prop.", "black!25"),
    ]
    baseline = averages["default-pass"]
    left_label, zero_x, scale = 34.0, 101.0, 82.0
    top, row_gap, bar_gap = 72.0, 3.6, 1.0
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,82)",
        "\\scriptsize",
    ]
    for tick in (-0.6, -0.3, 0.0, 0.1):
        x = zero_x + tick * scale
        lines.extend([
            f"\\put({fmt(x)},{fmt(8.0)}){{\\color{{black!15}}\\line(0,1){{66.0}}}}",
            f"\\put({fmt(x)},{fmt(4.5)}){{\\makebox(0,0){{{tick:.1f}}}}}",
        ])
    lines.append(f"\\put({fmt(zero_x)},{fmt(8.0)}){{\\line(0,1){{66.0}}}}")
    for row_index, (key, label) in enumerate(scenarios):
        if key not in averages:
            continue
        y = top - row_index * row_gap
        label_color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        lines.append(f"\\put({fmt(left_label)},{fmt(y - 1.0)}){{\\makebox(0,0)[r]{{\\color{{{label_color}}}{label}}}}}")
        for metric_index, (field, _short, color) in enumerate(metrics):
            if key == CURRENT_SYSTEM_KEY:
                color = ("red", "red!65", "red!35")[metric_index]
            delta = averages[key][field] - baseline[field]
            bar_y = y + (1 - metric_index) * bar_gap
            if delta < 0:
                x = zero_x + delta * scale
                w = abs(delta) * scale
            else:
                x = zero_x
                w = delta * scale
            lines.append(f"\\put({fmt(x)},{fmt(bar_y)}){{\\color{{{color}}}\\rule{{{max(w, 0.3):.1f}mm}}{{0.9mm}}}}")
    legend_y = 78.0
    legend_x = 42.0
    for index, (_field, short, color) in enumerate(metrics):
        x = legend_x + index * 24.0
        lines.extend([
            f"\\put({fmt(x)},{fmt(legend_y)}){{\\color{{{color}}}\\rule{{5.0mm}}{{1.8mm}}}}",
            f"\\put({fmt(x + 7.0)},{fmt(legend_y + 0.2)}){{\\makebox(0,0)[l]{{{short} delta}}}}",
        ])
    lines.extend([
        f"\\put({fmt(69.0)},{fmt(0.5)}){{\\makebox(0,0){{Delta relative to open default-pass}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "default_pass_deltas.tex").write_text("\n".join(lines))


def write_compromise_productivity(averages: dict[str, dict[str, float]]) -> None:
    labels = {
        "simple-majority": ("SM", 2.6, -8.2, None),
        "supermajority-60": ("S60", -0.6, -5.8, None),
        "bicameral-majority": ("Bic", 2.8, 5.0, None),
        "presidential-veto": ("Veto", 3.0, 4.2, None),
        CURRENT_SYSTEM_KEY: ("Current", 2.6, 5.2, None),
        "default-pass": ("DP", 2.4, 3.6, None),
        "default-pass-constituent-citizen-panel": ("Panel", -3.8, -7.2, "r"),
        "default-pass-proposal-bonds": ("Bond", -4.6, 4.8, "r"),
        "default-pass-affected-sponsor-gate": ("Aff.", 4.8, -4.8, None),
        "default-pass-multiround-mediation": ("Med", -4.8, 4.8, "r"),
        "default-pass-multiround-mediation-challenge": ("MedC", 2.2, -6.0, None),
        "default-pass-alternatives-pairwise": ("Pair", 2.4, -7.6, None),
        "default-pass-adaptive-proposers": ("Prop", -4.8, -7.8, "r"),
        "default-pass-strategic-lobbying": ("Lob", -4.8, 5.8, "r"),
        "default-pass-challenge": ("Chal.", 2.4, -3.8, None),
        "default-pass-challenge-minority-bonus": ("MinTok", 2.8, -7.4, None),
        "default-pass-public-objection": ("Obj.", -3.0, 5.0, "r"),
        "default-pass-weighted-agenda-lottery": ("Lot.", 2.8, 5.4, None),
        "default-pass-law-registry": ("Law", -4.0, -4.0, "r"),
    }
    left, bottom, width, height = 23.0, 14.0, 90.0, 58.0
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,84)",
        "\\scriptsize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = left + tick * width
        y = bottom + tick * height
        lines.extend([
            f"\\put({fmt(x)},{fmt(bottom)}){{\\color{{black!15}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(x)},{fmt(bottom - 3.0)}){{\\makebox(0,0){{{tick:.2g}}}}}",
            f"\\put({fmt(left - 4.0)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
    ])
    for key, values in sorted(averages.items()):
        x = left + values["productivity"] * width
        y = bottom + values["compromise"] * height
        lines.append(f"\\put({fmt(x)},{fmt(y)}){{\\makebox(0,0){{\\color{{black!55}}\\rule{{1.1mm}}{{1.1mm}}}}}}")
    for key, (label, dx, dy, anchor) in labels.items():
        if key not in averages:
            continue
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "2.0mm" if key == CURRENT_SYSTEM_KEY else "1.7mm"
        x = left + averages[key]["productivity"] * width
        y = bottom + averages[key]["compromise"] * height
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(3.0)}){{\\makebox(0,0){{Productivity $\\uparrow$ (share enacted)}}}}",
        f"\\put({fmt(5.0)},{fmt(bottom + height / 2.0)}){{\\rotatebox{{90}}{{Compromise score $\\uparrow$}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "compromise_productivity.tex").write_text("\n".join(lines))


def write_broad_system_comparison(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [
        (CURRENT_SYSTEM_KEY, "Current"),
        ("simple-majority", "Simple maj."),
        ("supermajority-60", "60\\%"),
        ("bicameral-majority", "Bicameral"),
        ("presidential-veto", "Pres. veto"),
        ("default-pass", "Default"),
        ("default-pass-challenge", "Challenge"),
        ("default-pass-multiround-mediation-challenge", "Med.+chal."),
        ("default-pass-constituent-citizen-panel", "Public+panel"),
        ("default-pass-adaptive-track-strict", "Strict adaptive"),
        ("default-pass-alternatives-pairwise", "Pairwise"),
        ("default-pass-affected-sponsor-gate", "Affected gate"),
    ]
    metrics = [
        ("productivity", "Prod.", "black"),
        ("compromise", "Comp.", "black!55"),
        ("welfare", "Welfare", "black!25"),
    ]
    left_label, left_axis, scale = 34.0, 38.0, 76.0
    top, row_gap, bar_gap = 77.0, 5.6, 1.15
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,88)",
        "\\scriptsize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = left_axis + tick * scale
        lines.extend([
            f"\\put({fmt(x)},{fmt(8.0)}){{\\color{{black!15}}\\line(0,1){{72.0}}}}",
            f"\\put({fmt(x)},{fmt(4.5)}){{\\makebox(0,0){{{tick:.2g}}}}}",
        ])
    for row_index, (key, label) in enumerate(scenarios):
        if key not in averages:
            continue
        y = top - row_index * row_gap
        label_color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        lines.append(f"\\put({fmt(left_label)},{fmt(y)}){{\\makebox(0,0)[r]{{\\color{{{label_color}}}{label}}}}}")
        for metric_index, (field, _short, color) in enumerate(metrics):
            if key == CURRENT_SYSTEM_KEY:
                color = ("red", "red!65", "red!35")[metric_index]
            value = max(0.0, min(1.0, averages[key][field]))
            bar_y = y + (1 - metric_index) * bar_gap
            lines.append(f"\\put({fmt(left_axis)},{fmt(bar_y)}){{\\color{{{color}}}\\rule{{{max(value * scale, 0.3):.1f}mm}}{{0.95mm}}}}")
    legend_y = 84.0
    legend_x = 40.0
    for index, (_field, short, color) in enumerate(metrics):
        x = legend_x + index * 25.0
        lines.extend([
            f"\\put({fmt(x)},{fmt(legend_y)}){{\\color{{{color}}}\\rule{{5.0mm}}{{1.8mm}}}}",
            f"\\put({fmt(x + 7.0)},{fmt(legend_y + 0.2)}){{\\makebox(0,0)[l]{{{short}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(76.0)},{fmt(0.8)}){{\\makebox(0,0){{Raw normalized score (higher is better for shown bars)}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "broad_system_comparison.tex").write_text("\n".join(lines))


def write_directional_scoreboard(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [
        (CURRENT_SYSTEM_KEY, "Current"),
        ("simple-majority", "Simple maj."),
        ("supermajority-60", "60\\%"),
        ("bicameral-majority", "Bicameral"),
        ("presidential-veto", "Pres. veto"),
        ("default-pass", "Default"),
        ("default-pass-challenge", "Challenge"),
        ("default-pass-multiround-mediation-challenge", "Med.+chal."),
        ("default-pass-constituent-citizen-panel", "Public+panel"),
        ("default-pass-adaptive-track-strict", "Strict adaptive"),
        ("default-pass-alternatives-pairwise", "Pairwise"),
        ("default-pass-affected-sponsor-gate", "Affected gate"),
    ]
    metrics = [
        ("directionalScore", "Directional", "black"),
        ("productivity", "Productivity", "black!70"),
        ("representativeQuality", "Rep. quality", "black!45"),
        ("riskControl", "Risk control", "black!20"),
    ]
    left_label, left_axis, scale = 34.0, 38.0, 76.0
    top, row_gap, bar_gap = 78.0, 5.8, 0.95
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,90)",
        "\\scriptsize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = left_axis + tick * scale
        lines.extend([
            f"\\put({fmt(x)},{fmt(8.0)}){{\\color{{black!15}}\\line(0,1){{73.0}}}}",
            f"\\put({fmt(x)},{fmt(4.5)}){{\\makebox(0,0){{{tick:.2g}}}}}",
        ])
    for row_index, (key, label) in enumerate(scenarios):
        if key not in averages:
            continue
        y = top - row_index * row_gap
        label_color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        lines.append(f"\\put({fmt(left_label)},{fmt(y)}){{\\makebox(0,0)[r]{{\\color{{{label_color}}}{label}}}}}")
        for metric_index, (field, _short, color) in enumerate(metrics):
            if key == CURRENT_SYSTEM_KEY:
                color = ("red", "red!70", "red!45", "red!25")[metric_index]
            value = clamp01(averages[key][field])
            bar_y = y + (1.5 - metric_index) * bar_gap
            lines.append(f"\\put({fmt(left_axis)},{fmt(bar_y)}){{\\color{{{color}}}\\rule{{{max(value * scale, 0.3):.1f}mm}}{{0.75mm}}}}")
    legend_y = 86.0
    legend_x = 23.0
    for index, (_field, short, color) in enumerate(metrics):
        x = legend_x + index * 27.0
        lines.extend([
            f"\\put({fmt(x)},{fmt(legend_y)}){{\\color{{{color}}}\\rule{{5.0mm}}{{1.6mm}}}}",
            f"\\put({fmt(x + 7.0)},{fmt(legend_y + 0.1)}){{\\makebox(0,0)[l]{{{short}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(76.0)},{fmt(0.8)}){{\\makebox(0,0){{Directional score/components (all oriented so rightward is better)}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "directional_scoreboard.tex").write_text("\n".join(lines))


def write_timeline_contention(
    case_keys: list[str],
    timeline: dict[str, dict[str, dict[str, float]]],
) -> None:
    scenarios = [
        ("presidential-veto", "Veto", "black!55"),
        (CURRENT_SYSTEM_KEY, "Current", "red"),
        ("simple-majority", "Simple maj.", "black"),
        ("default-pass-alternatives-pairwise", "Pairwise", "black!80"),
        ("default-pass", "Default", "black!30"),
        ("default-pass-challenge", "Challenge", "black!70"),
        ("default-pass-multiround-mediation-challenge", "Med.+chal.", "black!45"),
    ]
    left, bottom, width, height = 23.0, 14.0, 86.0, 58.0
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,90)",
        "\\scriptsize",
    ]
    if not case_keys:
        lines.extend([
            "\\put(64,42){\\makebox(0,0){Run \\texttt{make campaign-v19} to generate timeline data.}}",
            "\\end{picture}",
            "\\endgroup",
            "",
        ])
        (FIGURE_DIR / "timeline_contention.tex").write_text("\n".join(lines))
        return

    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom + tick * height
        lines.extend([
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(left - 3.0)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    for index, case_key in enumerate(case_keys):
        x = left + (index / max(1, len(case_keys) - 1)) * width
        label = f"E{index + 1}"
        lines.extend([
            f"\\put({fmt(x)},{fmt(bottom)}){{\\color{{black!12}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(x)},{fmt(bottom - 4.0)}){{\\makebox(0,0){{{label}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
    ])

    for scenario_key, _label, color in scenarios:
        points: list[tuple[float, float]] = []
        for index, case_key in enumerate(case_keys):
            if scenario_key not in timeline.get(case_key, {}):
                continue
            x = left + (index / max(1, len(case_keys) - 1)) * width
            y = bottom + timeline[case_key][scenario_key]["contention"] * height
            points.append((x, y))
        if len(points) < 2:
            continue
        thickness = "0.45mm" if scenario_key == CURRENT_SYSTEM_KEY else "0.25mm"
        lines.append(f"\\linethickness{{{thickness}}}")
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            mid_x = (x1 + x2) / 2.0
            mid_y = (y1 + y2) / 2.0
            lines.append(
                f"\\qbezier[{int(max(abs(x2 - x1), abs(y2 - y1)) * 2)}]"
                f"({fmt(x1)},{fmt(y1)})({fmt(mid_x)},{fmt(mid_y)})({fmt(x2)},{fmt(y2)})"
            )
            lines[-1] = "{\\color{" + color + "}" + lines[-1] + "}"
        point_size = "1.8mm" if scenario_key == CURRENT_SYSTEM_KEY else "1.3mm"
        for x, y in points:
            lines.append(f"\\put({fmt(x)},{fmt(y)}){{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}")

    legend_positions = [
        (23.0, 82.8),
        (51.0, 82.8),
        (84.0, 82.8),
        (23.0, 78.8),
        (51.0, 78.8),
        (84.0, 78.8),
        (23.0, 74.8),
    ]
    for (scenario_key, label, color), (x, y) in zip(scenarios, legend_positions):
        swatch = "1.8mm" if scenario_key == CURRENT_SYSTEM_KEY else "1.3mm"
        lines.extend([
            f"\\put({fmt(x)},{fmt(y)}){{\\makebox(0,0){{\\color{{{color}}}\\rule{{{swatch}}}{{{swatch}}}}}}}",
            f"% legend-label label={label} x={fmt(x + 3.5)} y={fmt(y)}",
            f"\\put({fmt(x + 3.5)},{fmt(y)}){{\\makebox(0,0)[l]{{\\color{{{color}}}{label}}}}}",
        ])
    lines.extend([
        "\\linethickness{0.25mm}",
        f"\\put({fmt(left + width / 2.0)},{fmt(2.0)}){{\\makebox(0,0){{Stylized timeline era}}}}",
        f"\\put({fmt(5.5)},{fmt(bottom + height / 2.0)}){{\\makebox(0,0){{\\rotatebox{{90}}{{Contention index $\\downarrow$}}}}}}",
        f"\\put({fmt(left + width / 2.0)},{fmt(87.0)}){{\\makebox(0,0){{Contention = 0.50 gridlock + 0.30 compromise loss + 0.20 low-support}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "timeline_contention.tex").write_text("\n".join(lines))


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    broad_rows = read_case_rows(PAPER_CSV_PATH, broad_case)
    base_averages = read_averages(PAPER_CSV_PATH, case_filter=broad_case)
    party_averages = read_averages(PAPER_CSV_PATH, weighted=True, case_filter=party_case)
    timeline_cases, timeline_values = read_timeline(PAPER_CSV_PATH, case_filter=timeline_case)
    write_scenario_averages_table(broad_rows)
    write_productivity_low_support(base_averages)
    write_default_pass_deltas(base_averages)
    write_compromise_productivity(party_averages)
    write_broad_system_comparison(base_averages)
    write_directional_scoreboard(base_averages)
    write_timeline_contention(timeline_cases, timeline_values)


if __name__ == "__main__":
    main()
