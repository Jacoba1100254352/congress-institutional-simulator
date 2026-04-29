#!/usr/bin/env python3
"""Generate ACM-friendly LaTeX figure fragments from campaign CSV output."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_CSV_PATH = ROOT / "reports" / "simulation-campaign-v17.csv"
PARTY_CSV_PATH = ROOT / "reports" / "simulation-campaign-v18.csv"
TIMELINE_CSV_PATH = ROOT / "reports" / "simulation-campaign-v19.csv"
FIGURE_DIR = ROOT / "paper" / "figures"
CURRENT_SYSTEM_KEY = "current-system"


def read_averages(path: Path, weighted: bool = False) -> dict[str, dict[str, float]]:
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


def read_timeline(path: Path) -> tuple[list[str], dict[str, dict[str, dict[str, float]]]]:
    case_names: dict[str, str] = {}
    values: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
    if not path.exists():
        return [], values
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
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


def write_productivity_low_support(averages: dict[str, dict[str, float]]) -> None:
    points = [
        ("supermajority-60", "S60", 1.5, -4.0),
        (CURRENT_SYSTEM_KEY, "Current", 2.0, 7.0),
        ("presidential-veto", "Veto", 2.0, 2.5),
        ("bicameral-majority", "Bicam", 2.0, 5.0),
        ("simple-majority", "SM", 1.5, -6.0),
        ("default-pass", "DP", 2.0, 2.2),
        ("default-pass-constituent-citizen-panel", "Public+Panel", 2.0, 2.5),
        ("default-pass-proposal-bonds", "Bond", -16.0, 4.0),
        ("default-pass-affected-sponsor-gate", "Aff.Spon", 2.0, 2.5),
        ("default-pass-multiround-mediation", "Med", -17.0, 2.5),
        ("default-pass-multiround-mediation-challenge", "Med+Chal", -20.0, -4.0),
        ("default-pass-challenge-minority-bonus", "MinTok", 2.0, -4.0),
        ("default-pass-adaptive-track-strict", "AdaptS", 2.0, 2.5),
        ("default-pass-cost-lobby-surcharge", "Cost", 2.0, 2.5),
        ("default-pass-weighted-agenda-lottery", "Lot.", 2.0, -4.0),
        ("default-pass-public-objection", "Obj.", 2.0, -4.0),
        ("default-pass-alternatives-pairwise", "Pair", 2.0, -4.0),
        ("default-pass-alternatives-strategic", "Strat", -18.0, 3.0),
        ("default-pass-adaptive-proposers", "PropStrat", -24.0, -4.0),
        ("default-pass-strategic-lobbying", "LobbyLearn", -26.0, 5.0),
        ("default-pass-challenge", "Chal.", 2.0, -4.0),
        ("default-pass-adaptive-track", "Adapt", 2.0, -4.0),
        ("default-pass-law-registry", "LawReg", 2.0, 2.4),
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
    for key, label, dx, dy in points:
        if key not in averages:
            continue
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "1.9mm" if key == CURRENT_SYSTEM_KEY else "1.5mm"
        x = left + averages[key]["productivity"] * width
        y = bottom + averages[key]["lowSupport"] * height
        lines.extend([
            f"\\put({fmt(x)},{fmt(y)}){{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}",
            f"\\put({fmt(x + dx)},{fmt(y + dy)}){{\\makebox(0,0)[l]{{\\color{{{color}}}{label}}}}}",
        ])
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
        "simple-majority": ("SM", 2.0, -4.0),
        "supermajority-60": ("S60", 2.0, -4.0),
        "bicameral-majority": ("Bicam", 2.0, 2.5),
        "presidential-veto": ("Veto", 2.0, 2.5),
        CURRENT_SYSTEM_KEY: ("Current", 2.0, 2.5),
        "default-pass": ("DP", 2.0, 2.5),
        "default-pass-constituent-citizen-panel": ("Public+Panel", -26.0, 2.5),
        "default-pass-proposal-bonds": ("Bond", -14.0, 2.8),
        "default-pass-affected-sponsor-gate": ("Aff.Spon", 2.0, -4.0),
        "default-pass-multiround-mediation": ("Med", -18.0, 2.5),
        "default-pass-multiround-mediation-challenge": ("Med+Chal", -24.0, -4.0),
        "default-pass-alternatives-pairwise": ("Pair", 2.0, -4.0),
        "default-pass-adaptive-proposers": ("PropStrat", -24.0, -4.0),
        "default-pass-strategic-lobbying": ("LobbyLearn", -26.0, 5.0),
        "default-pass-challenge": ("Chal.", 2.0, -4.0),
        "default-pass-challenge-minority-bonus": ("MinTok", 2.0, 2.5),
        "default-pass-public-objection": ("Obj.", 2.0, -4.0),
        "default-pass-weighted-agenda-lottery": ("Lot.", 2.0, 2.5),
        "default-pass-law-registry": ("LawReg", -19.0, -4.0),
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
    for key, (label, dx, dy) in labels.items():
        if key not in averages:
            continue
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "2.0mm" if key == CURRENT_SYSTEM_KEY else "1.7mm"
        x = left + averages[key]["productivity"] * width
        y = bottom + averages[key]["compromise"] * height
        lines.extend([
            f"\\put({fmt(x)},{fmt(y)}){{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}",
            f"\\put({fmt(x + dx)},{fmt(y + dy)}){{\\makebox(0,0)[l]{{\\color{{{color}}}{label}}}}}",
        ])
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
        (CURRENT_SYSTEM_KEY, "Current", "red", 7.0),
        ("simple-majority", "Simple maj.", "black", -6.0),
        ("presidential-veto", "Veto", "black!55", 11.0),
        ("default-pass", "Default", "black!30", 1.0),
        ("default-pass-challenge", "Challenge", "black!70", -6.0),
        ("default-pass-multiround-mediation-challenge", "Med.+chal.", "black!45", 7.0),
        ("default-pass-alternatives-pairwise", "Pairwise", "black!80", -13.0),
    ]
    left, bottom, width, height = 16.0, 14.0, 94.0, 58.0
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,84)",
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

    for scenario_key, label, color, label_offset in scenarios:
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
        final_x, final_y = points[-1]
        lines.append(
            f"\\put({fmt(final_x + 2.2)},{fmt(final_y + label_offset)})"
            f"{{\\makebox(0,0)[l]{{\\color{{{color}}}{label}}}}}"
        )
    lines.extend([
        "\\linethickness{0.25mm}",
        f"\\put({fmt(left + width / 2.0)},{fmt(2.0)}){{\\makebox(0,0){{Stylized timeline era}}}}",
        f"\\put({fmt(4.0)},{fmt(bottom + height / 2.0)}){{\\rotatebox{{90}}{{Contention index $\\downarrow$}}}}",
        "\\put(17,77){\\makebox(0,0)[l]{Contention = 0.50 gridlock + 0.30 compromise loss + 0.20 low-support}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "timeline_contention.tex").write_text("\n".join(lines))


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    base_averages = read_averages(BASE_CSV_PATH)
    party_averages = read_averages(PARTY_CSV_PATH, weighted=True) if PARTY_CSV_PATH.exists() else base_averages
    timeline_cases, timeline_values = read_timeline(TIMELINE_CSV_PATH)
    write_productivity_low_support(base_averages)
    write_default_pass_deltas(base_averages)
    write_compromise_productivity(party_averages)
    write_broad_system_comparison(base_averages)
    write_directional_scoreboard(base_averages)
    write_timeline_contention(timeline_cases, timeline_values)


if __name__ == "__main__":
    main()
