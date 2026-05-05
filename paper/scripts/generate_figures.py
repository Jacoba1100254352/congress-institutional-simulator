#!/usr/bin/env python3
"""Generate ACM-friendly LaTeX figure fragments from campaign CSV output."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_CSV_PATH = ROOT / "reports" / "simulation-campaign-v21-paper.csv"
SEED_ROBUSTNESS_CSV_PATH = ROOT / "reports" / "seed-robustness-summary.csv"
FIGURE_DIR = ROOT / "paper" / "figures"
REPORT_DIR = ROOT / "reports"
CURRENT_SYSTEM_KEY = "current-system"
TABLE_SCENARIOS = [
    (CURRENT_SYSTEM_KEY, "CUR"),
    ("simple-majority", "SM"),
    ("supermajority-60", "S60"),
    ("bicameral-majority", "BIC"),
    ("presidential-veto", "VETO"),
    ("leadership-cartel-majority", "LEAD"),
    ("committee-regular-order", "COMM"),
    ("cloture-conference-review", "PROC"),
    ("constitutional-court-architecture-majority", "COURT"),
    ("parliamentary-coalition-confidence", "PARL"),
    ("citizen-initiative-referendum", "INIT"),
    ("district-population-majority", "DIST"),
    ("simple-majority-alternatives-pairwise", "PAIR"),
    ("citizen-assembly-threshold", "JURY"),
    ("public-interest-majority", "SCR"),
    ("agenda-lottery-majority", "LOT"),
    ("quadratic-attention-majority", "QAB"),
    ("proposal-bond-majority", "BOND"),
    ("harm-weighted-majority", "HARM"),
    ("compensation-majority", "COMP"),
    ("package-bargaining-majority", "PKG"),
    ("multidimensional-package-majority", "MPKG"),
    ("omnibus-bargaining-majority", "OMNI"),
    ("law-registry-majority", "LAW"),
    ("public-objection-majority", "OBJ"),
    ("anti-capture-majority-bundle", "CAP"),
    ("influence-system-majority", "INFL"),
    ("risk-routed-majority", "RISK"),
    ("portfolio-hybrid-legislature", "PORT"),
    ("expanded-portfolio-hybrid-legislature", "XPORT"),
    ("norm-erosion-majority", "NORM"),
    ("long-horizon-learning-majority", "LEARN"),
    ("default-pass", "DP"),
    ("default-pass-challenge", "DPC"),
    ("default-pass-multiround-mediation-challenge", "DPM"),
]
MAIN_TABLE_SCENARIOS = [
    (CURRENT_SYSTEM_KEY, "CUR"),
    ("simple-majority", "SM"),
    ("committee-regular-order", "COMM"),
    ("parliamentary-coalition-confidence", "PARL"),
    ("citizen-initiative-referendum", "INIT"),
    ("simple-majority-alternatives-pairwise", "PAIR"),
    ("citizen-assembly-threshold", "JURY"),
    ("quadratic-attention-majority", "QAB"),
    ("proposal-bond-majority", "BOND"),
    ("harm-weighted-majority", "HARM"),
    ("multidimensional-package-majority", "MPKG"),
    ("anti-capture-majority-bundle", "CAP"),
    ("risk-routed-majority", "RISK"),
    ("portfolio-hybrid-legislature", "PORT"),
    ("expanded-portfolio-hybrid-legislature", "XPORT"),
    ("law-registry-majority", "LAW"),
    ("default-pass", "DP"),
    ("default-pass-multiround-mediation-challenge", "DPM"),
]
MAIN_SCENARIO_KEYS = {key for key, _label in MAIN_TABLE_SCENARIOS}
SELECTION_RATIONALES = {
    CURRENT_SYSTEM_KEY: (
        "Conventional benchmark",
        "Stylized U.S.-like conventional benchmark used as the red baseline; included for comparison, not as a calibrated model of Congress.",
    ),
    "simple-majority": (
        "Conventional threshold",
        "Minimal affirmative-vote baseline that isolates the effect of ordinary majority passage.",
    ),
    "supermajority-60": (
        "Conventional threshold",
        "Higher-threshold baseline for separating risk suppression from throughput loss.",
    ),
    "bicameral-majority": (
        "Conventional threshold",
        "Adds second-chamber consent while keeping a conventional majority decision rule.",
    ),
    "presidential-veto": (
        "Conventional veto",
        "Adds executive veto and override pressure to the bicameral baseline.",
    ),
    "leadership-cartel-majority": (
        "Agenda control",
        "Represents leadership-controlled floor access and majority-cartel agenda power.",
    ),
    "committee-regular-order": (
        "Committee gate",
        "Represents committee-first screening before floor consideration.",
    ),
    "cloture-conference-review": (
        "Procedural legislature",
        "Represents cloture-like delay, conference revision, and post-passage review.",
    ),
    "constitutional-court-architecture-majority": (
        "Constitutional review",
        "Represents an ex post legal-review architecture as a risk-control layer.",
    ),
    "parliamentary-coalition-confidence": (
        "Coalition parliamentarism",
        "Represents confidence/access discipline and cross-bloc coalition bargaining.",
    ),
    "citizen-initiative-referendum": (
        "Direct democracy",
        "Represents a non-legislator proposal/ratification channel.",
    ),
    "district-population-majority": (
        "Public representation",
        "Represents district-public signals and population-alignment pressure.",
    ),
    "simple-majority-alternatives-pairwise": (
        "Policy tournament",
        "Main alternative-selection representative; tests agenda manipulation by comparing multiple substitutes before final ratification.",
    ),
    "citizen-assembly-threshold": (
        "Mini-public review",
        "Represents citizen-panel certification changing the burden of proof.",
    ),
    "public-interest-majority": (
        "Public-interest screening",
        "Represents a welfare/support screen without default enactment.",
    ),
    "agenda-lottery-majority": (
        "Agenda allocation",
        "Represents weighted/randomized agenda access without a permanent gatekeeper.",
    ),
    "quadratic-attention-majority": (
        "Agenda scarcity",
        "Represents quadratic attention costs for scarce proposal and procedural capacity.",
    ),
    "proposal-bond-majority": (
        "Proposal accountability",
        "Represents refundable proposer accountability tied to estimated proposal quality.",
    ),
    "harm-weighted-majority": (
        "Affected-group protection",
        "Represents higher thresholds when concentrated harm is generated.",
    ),
    "compensation-majority": (
        "Distributional justice",
        "Represents compensation amendments for concentrated losses.",
    ),
    "package-bargaining-majority": (
        "Package bargaining",
        "Represents side payments, delay, and harm-reducing package trades.",
    ),
    "multidimensional-package-majority": (
        "Multidimensional bargaining",
        "Main package-bargaining representative; tests whether richer cross-issue trades improve compromise after administrative load is counted.",
    ),
    "omnibus-bargaining-majority": (
        "Omnibus bargaining",
        "Represents omnibus-style package formation and bundled coalition trades.",
    ),
    "law-registry-majority": (
        "Correction/reversibility",
        "Represents persistent laws, review, renewal, and rollback after enactment.",
    ),
    "public-objection-majority": (
        "Contestatory public review",
        "Represents objection windows and public contestation before or after enactment.",
    ),
    "anti-capture-majority-bundle": (
        "Anti-capture",
        "Main anti-lobbying representative; combines transparency, public advocate, audit, and access screen safeguards.",
    ),
    "influence-system-majority": (
        "Influence system",
        "Represents explicit campaign-finance and organized-influence pressure beyond bill-level lobbying.",
    ),
    "risk-routed-majority": (
        "Adaptive routing",
        "Represents risk-based fast, middle, and high-review lanes under affirmative majority rule.",
    ),
    "portfolio-hybrid-legislature": (
        "Synthesized hybrid",
        "Main design hypothesis combining fast lanes, alternatives, citizen/harm review, bonds, anti-capture safeguards, and law review.",
    ),
    "expanded-portfolio-hybrid-legislature": (
        "Expanded hybrid",
        "Stress-tests the portfolio idea with added district, learning, influence, package, and court modules.",
    ),
    "norm-erosion-majority": (
        "Norm erosion",
        "Represents parameterized procedural deterioration and rising contention.",
    ),
    "long-horizon-learning-majority": (
        "Actor learning",
        "Represents bounded long-horizon proposer and lobby adaptation across sessions.",
    ),
    "default-pass": (
        "Default-enactment stress test",
        "Kept as the open default-enactment endpoint rather than the organizing case.",
    ),
    "default-pass-challenge": (
        "Default-enactment stress test",
        "Tests whether scarce challenge rights reduce default-enactment risk.",
    ),
    "default-pass-multiround-mediation-challenge": (
        "Default-enactment stress test",
        "Tests a guarded default-enactment variant with mediation and challenge vouchers.",
    ),
}


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
        "weakPublicMandatePassage",
        "administrativeCost",
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
        inverse01(values.get("weakPublicMandatePassage", 0.0)),
        inverse01(values.get("minorityHarm", 0.0)),
        inverse01(values.get("lobbyCapture", 0.0)),
        inverse01(values.get("publicPreferenceDistortion", 0.0)),
        inverse01(values.get("concentratedHarmPassage", 0.0)),
        inverse_range(values.get("proposerGain", 0.0)),
        inverse_range(values.get("policyShift", 0.0)),
    ])
    administrative_feasibility = inverse01(values.get("administrativeCost", 0.0))
    values["representativeQuality"] = representative_quality
    values["riskControl"] = risk_control
    values["administrativeFeasibility"] = administrative_feasibility
    values["directionalScore"] = mean([
        clamp01(values.get("productivity", 0.0)),
        representative_quality,
        risk_control,
        administrative_feasibility,
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
                "weakPublicMandatePassage": float(row.get("weakPublicMandatePassage", row["lowSupport"])),
                "contention": contention_index(row),
            }
    return list(case_names.keys()), values


def contention_index(row: dict[str, str]) -> float:
    gridlock = float(row["gridlock"])
    compromise_loss = 1.0 - float(row["compromise"])
    weak_mandate = float(row.get("weakPublicMandatePassage", row["lowSupport"]))
    return max(0.0, min(1.0, (0.50 * gridlock) + (0.30 * compromise_loss) + (0.20 * weak_mandate)))


def fmt(value: float) -> str:
    return f"{value:.1f}"


def latex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def mean_half_range(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    avg = sum(values) / len(values)
    if len(values) == 1:
        return avg, 0.0
    return avg, (max(values) - min(values)) / 2.0


def table_value(values: list[float], decimals: int = 3) -> str:
    avg, half_range = mean_half_range(values)
    return f"{avg:.{decimals}f}$\\pm${half_range:.{decimals}f}"


def read_seed_directional_intervals(path: Path) -> dict[str, tuple[float, float]]:
    intervals: dict[str, tuple[float, float]] = {}
    if not path.exists():
        return intervals
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("metric") != "directionalScore":
                continue
            mean_value = float(row["mean"])
            half_range = (float(row["max"]) - float(row["min"])) / 2.0
            intervals[row["scenarioKey"]] = (mean_value, half_range)
    return intervals


def seed_interval_value(intervals: dict[str, tuple[float, float]], scenario_key: str) -> str:
    interval = intervals.get(scenario_key)
    if interval is None:
        return "---"
    mean_value, half_range = interval
    return f"{mean_value:.3f}$\\pm${half_range:.3f}"


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


def write_scenario_selection_manifest(rows: list[dict[str, str]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    present_keys = {row["scenarioKey"] for row in rows}
    lines = [
        "# Scenario Selection Manifest",
        "",
        "Generated by `paper/scripts/generate_figures.py` from the main comparison campaign.",
        "",
        "Selection rule: include conventional baselines, the stylized U.S.-like benchmark, one readable representative for each implemented non-default design family, and three default-enactment stress tests. Where a family has many implemented variants, the representative is chosen for mechanism clarity rather than for highest observed score. Supplemental family-screen reports evaluate broader catalog champions under a fixed rule.",
        "",
        "| Label | Scenario key | Scenario name | Paper role | Family | Selection rationale |",
        "|---|---|---|---|---|---|",
    ]
    for scenario_key, label in TABLE_SCENARIOS:
        if scenario_key not in present_keys:
            continue
        family, rationale = SELECTION_RATIONALES.get(
            scenario_key,
            ("Uncategorized", "Included because it appears in the generated paper scenario list."),
        )
        role = "Main Table 1" if scenario_key in MAIN_SCENARIO_KEYS else "Appendix/full comparison"
        lines.append(
            "| "
            + " | ".join([
                label,
                f"`{scenario_key}`",
                scenario_name(rows, scenario_key),
                role,
                family,
                rationale,
            ])
            + " |"
        )
    lines.extend([
        "",
        "Historical default-pass sweeps remain available through catalog and campaign reports, but they are not used as the organizing frame for the main paper comparison.",
        "",
    ])
    (REPORT_DIR / "scenario-selection-manifest.md").write_text("\n".join(lines))


def pareto_front(
    averages: dict[str, dict[str, float]],
    fields: tuple[str, ...],
) -> list[str]:
    keys = [key for key, _label in TABLE_SCENARIOS if key in averages]
    front: list[str] = []
    for key in keys:
        values = averages[key]
        dominated = False
        for other_key in keys:
            if other_key == key:
                continue
            other = averages[other_key]
            at_least_as_good = all(other[field] >= values[field] - 1e-9 for field in fields)
            strictly_better = any(other[field] > values[field] + 1e-9 for field in fields)
            if at_least_as_good and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(key)
    return sorted(front, key=lambda key: averages[key]["productivity"], reverse=True)


def frontier_role(label: str) -> str:
    return {
        "DP": "Throughput endpoint",
        "DPM": "Throughput with mediation/challenge",
        "PAIR": "Alternative-comparison endpoint",
    }.get(label, "Non-dominated profile")


def write_pareto_front_table(rows: list[dict[str, str]], averages: dict[str, dict[str, float]]) -> None:
    label_by_key = dict(TABLE_SCENARIOS)
    front = pareto_front(averages, ("productivity", "compromise", "riskControl"))
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\centering",
        "  \\begin{minipage}[t]{0.39\\textwidth}",
        "    \\centering",
        "    \\caption{Pareto-front scenarios under productivity, compromise, and risk control.}",
        "    \\label{tab:pareto-front}",
        "    \\scriptsize",
        "    \\setlength{\\tabcolsep}{2.2pt}",
        "    \\resizebox{\\linewidth}{!}{%",
        "  \\begin{tabular}{llrrrrr}",
        "    \\toprule",
        "    Label & Role & Prod. $\\uparrow$ & Comp. $\\uparrow$ & Risk $\\uparrow$ & Weak mand. $\\downarrow$ & Admin $\\downarrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key in front:
        label = label_by_key[scenario_key]
        values = averages[scenario_key]
        label_cell = label
        if scenario_key == CURRENT_SYSTEM_KEY:
            label_cell = f"\\textcolor{{red}}{{\\textbf{{{label}}}}}"
        lines.append(
            "    "
            + label_cell
            + " & "
            + latex_escape(frontier_role(label))
            + " & "
            + f"{values['productivity']:.3f}"
            + " & "
            + f"{values['compromise']:.3f}"
            + " & "
            + f"{values['riskControl']:.3f}"
            + " & "
            + f"{values.get('weakPublicMandatePassage', 0.0):.3f}"
            + " & "
            + f"{values.get('administrativeCost', 0.0):.3f}"
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "    }",
        "    \\par\\smallskip\\scriptsize \\emph{Note:} The frontier changes if administrative feasibility, welfare, or rights/harm priorities are hard objectives.",
        "  \\end{minipage}\\hfill",
        "  \\begin{minipage}[t]{0.58\\textwidth}",
        "    \\centering",
        "    \\input{figures/mechanism_diagnostics_table}",
        "  \\end{minipage}",
        "  \\Description{Two generated side-by-side tables. The first lists Pareto-front scenarios under productivity, compromise, and risk control; the second lists selected mechanism ablations and manipulation stress tests.}",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "pareto_front_table.tex").write_text("\n".join(lines))


def write_compact_scenario_averages_table(rows: list[dict[str, str]]) -> None:
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Representative family comparison from the main campaign. Metric entries are mean$\\pm$case half-range across broad and adversarial cases. The full table with directional and seed diagnostics is in the appendix and supplement.}",
        "  \\label{tab:scenario-averages}",
        "  \\Description{A generated compact table comparing representative institutional families from the main comparison campaign.}",
        "  \\scriptsize",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{llrrrrr}",
        "    \\toprule",
        "    Label & Representative system & Prod. $\\uparrow$ & Comp. $\\uparrow$ & Weak mand. $\\downarrow$ & Risk ctrl. $\\uparrow$ & Admin $\\downarrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key, label in MAIN_TABLE_SCENARIOS:
        if not any(row["scenarioKey"] == scenario_key for row in rows):
            continue
        cells = [
            table_value(scenario_case_values(rows, scenario_key, "productivity")),
            table_value(scenario_case_values(rows, scenario_key, "compromise")),
            table_value(scenario_case_values(rows, scenario_key, "weakPublicMandatePassage")),
            table_value(scenario_case_values(rows, scenario_key, "riskControl")),
            table_value(scenario_case_values(rows, scenario_key, "administrativeCost")),
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
        "  \\par\\smallskip\\footnotesize \\emph{Note:} Case half-ranges are descriptive variation across campaign cases, not statistical confidence intervals. Red marks the stylized U.S.-like conventional benchmark.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "scenario_averages_table.tex").write_text("\n".join(lines))


def write_full_scenario_averages_table(rows: list[dict[str, str]]) -> None:
    seed_intervals = read_seed_directional_intervals(SEED_ROBUSTNESS_CSV_PATH)
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Full scenario averages from the main comparison campaign. Metric entries are mean$\\pm$case half-range across broad and adversarial cases; Seed dir. reports directional-score mean$\\pm$half-range across the independent seed sweep.}",
        "  \\label{tab:scenario-averages-full}",
        "  \\Description{A generated full table comparing all paper scenarios using the main comparison campaign.}",
        "  \\scriptsize",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{llrrrrrrrr}",
        "    \\toprule",
        "    Label & Scenario & Directional $\\uparrow$ & Seed dir. $\\uparrow$ & Prod. $\\uparrow$ & Comp. $\\uparrow$ & Enacted/run & Weak mandate $\\downarrow$ & Admin cost $\\downarrow$ & Risk ctrl. $\\uparrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key, label in TABLE_SCENARIOS:
        if not any(row["scenarioKey"] == scenario_key for row in rows):
            continue
        cells = [
            table_value(scenario_case_values(rows, scenario_key, "directionalScore")),
            seed_interval_value(seed_intervals, scenario_key),
            table_value(scenario_case_values(rows, scenario_key, "productivity")),
            table_value(scenario_case_values(rows, scenario_key, "compromise")),
            table_value(scenario_case_values(rows, scenario_key, "enactedPerRun"), 2),
            table_value(scenario_case_values(rows, scenario_key, "weakPublicMandatePassage")),
            table_value(scenario_case_values(rows, scenario_key, "administrativeCost")),
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
        "  \\par\\smallskip\\footnotesize \\emph{Note:} Case half-ranges are descriptive variation across campaign cases, not statistical confidence intervals. Directional, productivity, compromise, weak public-mandate passage, administrative cost, and risk-control values are normalized scores or rates. \\emph{Enacted/run} is an absolute institutional-load count.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "scenario_averages_full_table.tex").write_text("\n".join(lines))


def write_design_space_coverage_table() -> None:
    rows = [
        ("Conventional", "SM S60 BIC VETO CUR", "Thresholds/vetoes", "Bottlenecks"),
        ("Procedure", "LEAD PROC COMM", "Agenda control", "Queue capture"),
        ("Courts", "COURT", "Review architecture", "Juridification"),
        ("Public model", "DIST", "District publics", "Proxy opinion"),
        ("Agenda gates", "SCR LOT", "Screen/lottery", "Gate bias"),
        ("Coalition", "PARL", "Confidence/access", "Bloc cartels"),
        ("Direct democracy", "INIT", "Initiative path", "Campaign bias"),
        ("Tournaments", "PAIR", "Alternatives", "Clones/decoys"),
        ("Mini-public", "JURY", "Citizen burden shift", "Manipulation"),
        ("Scarcity", "QAB BOND", "Credits/bonds", "Hoarding"),
        ("Harm rules", "HARM COMP", "Minority protection", "Holdouts"),
        ("Bargaining", "PKG MPKG OMNI", "Package trades", "Proxy limits"),
        ("Correction", "LAW OBJ", "Review/objection", "Instability"),
        ("Anti-capture", "CAP INFL", "Lobby safeguards", "Evasion"),
        ("Adaptive", "RISK NORM LEARN", "Risk/norm/learning", "Gaming"),
        ("Portfolio", "PORT XPORT", "Mechanism bundle", "Complexity"),
        ("Default stress", "DP DPC DPM", "Burden shift", "False silence"),
        ("Out of scope", "---", "Elections/media/etc.", "Endogeneity"),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Compact design-space index for the main comparison campaign. Labels match Table~\\ref{tab:scenario-averages} and the scatter plots; detailed mechanism descriptions are in the appendix and supplement.}",
        "  \\label{tab:design-space-coverage}",
        "  \\Description{A compact generated index showing the design families represented in the main comparison campaign, their labels, the mechanism theme, and the primary stress risk.}",
        "  \\small",
        "  \\begin{tabular}{@{}llll@{}}",
        "    \\toprule",
        "    Family & Labels & Mechanism theme & Primary stress risk \\\\",
        "    \\midrule",
    ]
    for family, labels, mechanism, risk in rows:
        lines.append(
            "    "
            + latex_escape(family)
            + " & "
            + latex_escape(labels)
            + " & "
            + latex_escape(mechanism)
            + " & "
            + latex_escape(risk)
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "design_space_coverage.tex").write_text("\n".join(lines))


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
    leader: bool = False,
) -> None:
    label_x = x + dx
    label_y = y + dy
    label_anchor_value = label_anchor(dx, anchor)
    lines.append(
        f"\\put({fmt(x)},{fmt(y)})"
        f"{{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}"
    )
    if leader and (abs(dx) > 2.2 or abs(dy) > 2.2):
        leader_color = "red!55" if color == "red" else "black!35"
        end_x = label_x - 1.2 if label_anchor_value == "l" else label_x + 1.2
        mid_x = (x + end_x) / 2.0
        mid_y = (y + label_y) / 2.0
        lines.extend([
            "\\linethickness{0.10mm}",
            "{\\color{"
            + leader_color
            + "}"
            + f"\\qbezier[8]({fmt(x)},{fmt(y)})({fmt(mid_x)},{fmt(mid_y)})({fmt(end_x)},{fmt(label_y)})"
            + "}",
            "\\linethickness{0.25mm}",
        ])
    lines.append(f"% point-label label={label} x={fmt(label_x)} y={fmt(label_y)}")
    lines.append(
        f"\\put({fmt(label_x)},{fmt(label_y)})"
        f"{{\\makebox(0,0)[{label_anchor_value}]{{\\color{{{color}}}{label}}}}}"
    )


def figure_label_width(label: str) -> float:
    return max(3.8, len(label) * 1.12)


def label_box(label_x: float, label_y: float, label: str, anchor: str) -> tuple[float, float, float, float]:
    width = figure_label_width(label)
    # Mirror scripts/checks/check_figure_labels.py: comments record one label coordinate,
    # and the checker treats that coordinate as the label center regardless of
    # TeX anchoring.
    return label_x - (width / 2.0), label_x + (width / 2.0), label_y - 2.0, label_y + 2.0


def boxes_overlap(left_a: float, right_a: float, bottom_a: float, top_a: float,
                  left_b: float, right_b: float, bottom_b: float, top_b: float) -> bool:
    return left_a < right_b and right_a > left_b and bottom_a < top_b and top_a > bottom_b


def auto_label_offsets(
    points: list[tuple[str, str, float, float]],
    picture_width: float,
    picture_height: float,
) -> dict[str, tuple[float, float, str]]:
    candidates = [
        (3.2, 5.2, "l"),
        (3.2, -5.2, "l"),
        (-3.2, 5.2, "r"),
        (-3.2, -5.2, "r"),
        (6.8, 0.8, "l"),
        (-6.8, 0.8, "r"),
        (0.0, 7.4, "c"),
        (0.0, -7.4, "c"),
        (8.2, 5.8, "l"),
        (8.2, -5.8, "l"),
        (-8.2, 5.8, "r"),
        (-8.2, -5.8, "r"),
        (11.0, 0.0, "l"),
        (-11.0, 0.0, "r"),
        (4.8, 9.4, "l"),
        (-4.8, 9.4, "r"),
        (4.8, -9.4, "l"),
        (-4.8, -9.4, "r"),
        (13.0, 5.0, "l"),
        (-13.0, 5.0, "r"),
        (13.0, -5.0, "l"),
        (-13.0, -5.0, "r"),
        (0.0, 11.8, "c"),
        (0.0, -11.8, "c"),
        (9.5, 11.2, "l"),
        (-9.5, 11.2, "r"),
        (9.5, -11.2, "l"),
        (-9.5, -11.2, "r"),
        (17.0, 0.0, "l"),
        (-17.0, 0.0, "r"),
        (15.0, 10.0, "l"),
        (-15.0, 10.0, "r"),
        (15.0, -10.0, "l"),
        (-15.0, -10.0, "r"),
    ]
    placed: list[tuple[float, float, float, float]] = []
    placements: dict[str, tuple[float, float, str]] = {}
    fallback_slots: list[tuple[float, float, str]] = []
    for y in (80.0, 76.0, 72.0, 68.0, 64.0, 60.0, 56.0, 52.0, 48.0, 44.0):
        fallback_slots.append((picture_width - 4.0, y, "r"))
        fallback_slots.append((4.0, y, "l"))
    for x in (18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0):
        fallback_slots.append((x, 4.0, "c"))
        fallback_slots.append((x, picture_height - 4.0, "c"))
    ordered = sorted(points, key=lambda item: (item[0] != CURRENT_SYSTEM_KEY, item[3], item[2]))
    for key, label, x, y in ordered:
        selected = candidates[-1]
        selected_box: tuple[float, float, float, float] | None = None
        for dx, dy, anchor in candidates:
            label_x = max(1.0, min(picture_width - 1.0, x + dx))
            label_y = max(1.0, min(picture_height - 1.0, y + dy))
            box = label_box(label_x, label_y, label, anchor)
            if box[0] < 0.5 or box[1] > picture_width - 0.5 or box[2] < 0.5 or box[3] > picture_height - 0.5:
                continue
            if any(boxes_overlap(*box, *existing) for existing in placed):
                continue
            selected = (label_x - x, label_y - y, anchor)
            selected_box = box
            break
        if selected_box is None:
            for label_x, label_y, anchor in fallback_slots:
                box = label_box(label_x, label_y, label, anchor)
                if any(boxes_overlap(*box, *existing) for existing in placed):
                    continue
                selected = (label_x - x, label_y - y, anchor)
                selected_box = box
                break
        if selected_box is None:
            dx, dy, anchor = selected
            label_x = max(1.0, min(picture_width - 1.0, x + dx))
            label_y = max(1.0, min(picture_height - 1.0, y + dy))
            selected = (label_x - x, label_y - y, anchor)
            selected_box = label_box(label_x, label_y, label, anchor)
        placements[key] = selected
        placed.append(selected_box)
    return placements


def table_points(averages: dict[str, dict[str, float]], x_field: str, y_field: str,
                 left: float, bottom: float, width: float, height: float) -> list[tuple[str, str, float, float]]:
    points: list[tuple[str, str, float, float]] = []
    for key, label in MAIN_TABLE_SCENARIOS:
        if key not in averages:
            continue
        x = left + clamp01(averages[key][x_field]) * width
        y = bottom + clamp01(averages[key][y_field]) * height
        points.append((key, label, x, y))
    return points


def write_productivity_low_support(averages: dict[str, dict[str, float]]) -> None:
    left, bottom, width, height = 23.0, 14.0, 90.0, 58.0
    picture_width, picture_height = 128.0, 84.0
    max_burden = max((1.0 - averages[key]["riskControl"]) for key, _label in MAIN_TABLE_SCENARIOS if key in averages)
    y_max = min(1.0, max(0.40, math.ceil((max_burden + 0.02) * 10.0) / 10.0))
    points = []
    for key, label in MAIN_TABLE_SCENARIOS:
        if key not in averages:
            continue
        x = left + clamp01(averages[key]["productivity"]) * width
        risk_burden = 1.0 - clamp01(averages[key]["riskControl"])
        y = bottom + clamp01(risk_burden / y_max) * height
        points.append((key, label, x, y))
    placements = auto_label_offsets(points, picture_width, picture_height)
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,84)",
        "\\scriptsize",
    ]
    for index in range(5):
        tick = y_max * index / 4.0
        y = bottom + (tick / y_max) * height
        x_tick = index / 4.0
        grid_x = left + x_tick * width
        lines.extend([
            f"\\put({fmt(grid_x)},{fmt(bottom)}){{\\color{{black!15}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(grid_x)},{fmt(bottom - 3.0)}){{\\makebox(0,0){{{x_tick:.2g}}}}}",
            f"\\put({fmt(left - 4.0)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
    ])
    for key, label, x, y in points:
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "1.9mm" if key == CURRENT_SYSTEM_KEY else "1.5mm"
        dx, dy, anchor = placements[key]
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor, leader=True)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(3.0)}){{\\makebox(0,0){{Productivity $\\uparrow$ (share enacted)}}}}",
        f"\\put({fmt(5.0)},{fmt(bottom + height / 2.0)}){{\\rotatebox{{90}}{{Representative-risk burden $\\downarrow$}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "productivity_low_support.tex").write_text("\n".join(lines))


def write_default_pass_deltas(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [
        ("default-pass-constituent-citizen-panel", "Public+panel"),
        (CURRENT_SYSTEM_KEY, "U.S.-like"),
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
    left, bottom, width, height = 23.0, 14.0, 90.0, 58.0
    picture_width, picture_height = 128.0, 84.0
    points = table_points(averages, "productivity", "compromise", left, bottom, width, height)
    placements = auto_label_offsets(points, picture_width, picture_height)
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
    for key, label, x, y in points:
        color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        point_size = "2.0mm" if key == CURRENT_SYSTEM_KEY else "1.7mm"
        dx, dy, anchor = placements[key]
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor, leader=True)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(3.0)}){{\\makebox(0,0){{Productivity $\\uparrow$ (share enacted)}}}}",
        f"\\put({fmt(5.0)},{fmt(bottom + height / 2.0)}){{\\rotatebox{{90}}{{Compromise score $\\uparrow$}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "compromise_productivity.tex").write_text("\n".join(lines))


def write_broad_system_comparison(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [(key, label) for key, label in TABLE_SCENARIOS if key in averages]
    metrics = [
        ("productivity", "Prod.", "black"),
        ("compromise", "Comp.", "black!55"),
        ("welfare", "Welfare", "black!25"),
    ]
    left_label, left_axis, scale = 34.0, 38.0, 76.0
    top, row_gap, bar_gap = 78.0, 3.25, 0.72
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
    scenarios = [(key, label) for key, label in MAIN_TABLE_SCENARIOS if key in averages]
    metrics = [
        ("productivity", "Productivity"),
        ("compromise", "Compromise"),
        ("representativeQuality", "Rep. quality"),
        ("riskControl", "Risk ctrl."),
        ("administrativeFeasibility", "Admin feas."),
    ]
    left_label = 22.0
    left_matrix = 28.0
    col_width = 18.8
    top = 73.0
    row_height = 3.75
    cell_height = 3.05
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(128,86)",
        "\\scriptsize",
    ]
    for index, (_field, label) in enumerate(metrics):
        x = left_matrix + index * col_width
        lines.extend([
            f"\\put({fmt(x + col_width / 2.0)},{fmt(80.5)}){{\\makebox(0,0){{\\textbf{{{label}}}}}}}",
            f"\\put({fmt(x)},{fmt(77.0)}){{\\color{{black!20}}\\line(1,0){{{fmt(col_width)}}}}}",
        ])
    for row_index, (key, label) in enumerate(scenarios):
        y = top - row_index * row_height
        label_color = "red" if key == CURRENT_SYSTEM_KEY else "black"
        label_text = f"\\textbf{{{label}}}" if key == CURRENT_SYSTEM_KEY else label
        lines.append(f"\\put({fmt(left_label)},{fmt(y + 0.45)}){{\\makebox(0,0)[r]{{\\color{{{label_color}}}{label_text}}}}}")
        for metric_index, (field, _short) in enumerate(metrics):
            value = clamp01(averages[key][field])
            shade = 8 + round(value * 72)
            fill = f"red!{shade}" if key == CURRENT_SYSTEM_KEY else f"black!{shade}"
            text_color = "white" if shade >= 54 else "black"
            x = left_matrix + metric_index * col_width
            cell_text = f"\\textbf{{{value:.2f}}}" if key == CURRENT_SYSTEM_KEY else f"{value:.2f}"
            lines.extend([
                f"\\put({fmt(x)},{fmt(y)}){{\\color{{{fill}}}\\rule{{{fmt(col_width - 0.6)}mm}}{{{fmt(cell_height)}mm}}}}",
                f"\\put({fmt(x + col_width / 2.0 - 0.3)},{fmt(y + cell_height / 2.0)}){{\\makebox(0,0){{\\color{{{text_color}}}{cell_text}}}}}",
            ])
    lines.extend([
        f"\\put({fmt(left_label)},{fmt(80.5)}){{\\makebox(0,0)[r]{{\\textbf{{Label}}}}}}",
        f"\\put({fmt(74.0)},{fmt(6.4)}){{\\makebox(0,0){{Representative Table rows; darker cells are higher/better-oriented values}}}}",
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
        (CURRENT_SYSTEM_KEY, "CUR", "red"),
        ("simple-majority", "SM", "black"),
        ("committee-regular-order", "COMM", "black!55"),
        ("parliamentary-coalition-confidence", "PARL", "black!70"),
        ("simple-majority-alternatives-pairwise", "PAIR", "black!80"),
        ("citizen-assembly-threshold", "JURY", "black!45"),
        ("risk-routed-majority", "RISK", "black!35"),
        ("expanded-portfolio-hybrid-legislature", "XPORT", "black"),
        ("default-pass", "DP", "black!25"),
        ("default-pass-multiround-mediation-challenge", "DPM", "black!60"),
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
        (16.0, 82.8),
        (38.0, 82.8),
        (60.0, 82.8),
        (82.0, 82.8),
        (104.0, 82.8),
        (16.0, 78.8),
        (38.0, 78.8),
        (60.0, 78.8),
        (82.0, 78.8),
        (104.0, 78.8),
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
    write_compact_scenario_averages_table(broad_rows)
    write_full_scenario_averages_table(broad_rows)
    write_scenario_selection_manifest(broad_rows)
    write_pareto_front_table(broad_rows, base_averages)
    write_design_space_coverage_table()
    write_productivity_low_support(base_averages)
    write_default_pass_deltas(base_averages)
    write_compromise_productivity(party_averages)
    write_broad_system_comparison(base_averages)
    write_directional_scoreboard(base_averages)
    write_timeline_contention(timeline_cases, timeline_values)


if __name__ == "__main__":
    main()
