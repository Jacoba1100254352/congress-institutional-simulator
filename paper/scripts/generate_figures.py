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
FAMILY_SCREEN_CSV_PATH = ROOT / "reports" / "all-scenarios-baseline.csv"
FIGURE_DIR = ROOT / "paper" / "figures"
REPORT_DIR = ROOT / "reports"
CURRENT_SYSTEM_KEY = "current-system"
CONTENT_SELECTION_KEY = "content-selection-family"
CONTENT_SELECTION_COMPONENTS = (
    "simple-majority-alternatives-pairwise",
    "pairwise-amendment-tournament-majority",
)
VIRTUAL_SCENARIOS = {
    CONTENT_SELECTION_KEY: CONTENT_SELECTION_COMPONENTS,
}
TABLE_SCENARIOS = [
    (CURRENT_SYSTEM_KEY, "CUR"),
    ("current-congress-workflow", "FLOW"),
    ("simple-majority", "SM"),
    ("simple-majority-mediation", "SMED"),
    ("supermajority-60", "S60"),
    ("bicameral-majority", "BIC"),
    ("presidential-veto", "VETO"),
    ("leadership-cartel-majority", "LEAD"),
    ("committee-regular-order", "COMM"),
    ("committee-amendment-majority", "CAMD"),
    ("proportional-committee-assignment-majority", "PCOM"),
    ("committee-discharge-target-majority", "DIS"),
    ("cloture-conference-review", "PROC"),
    ("constitutional-court-architecture-majority", "COURT"),
    ("parliamentary-coalition-confidence", "PARL"),
    ("citizen-initiative-referendum", "INIT"),
    ("citizens-agenda-petition-majority", "PET"),
    ("district-population-majority", "DIST"),
    ("simple-majority-alternatives-pairwise", "PAIR"),
    ("pairwise-amendment-tournament-majority", "AMT"),
    ("citizen-assembly-threshold", "JURY"),
    ("random-public-review-panel-majority", "RPAN"),
    ("public-interest-majority", "SCR"),
    ("open-rule-calendar-majority", "OPEN"),
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
    ("anti-capture-access-majority", "ACG"),
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
    ("committee-discharge-target-majority", "DIS"),
    ("open-rule-calendar-majority", "OPEN"),
    (CONTENT_SELECTION_KEY, "SEL"),
    ("anti-capture-access-majority", "ACG"),
    ("harm-weighted-majority", "HARM"),
    ("default-pass", "DP"),
    ("default-pass-multiround-mediation-challenge", "DPM"),
    ("portfolio-hybrid-legislature", "PORT"),
]
MAIN_SCENARIO_KEYS = {
    actual_key
    for key, _label in MAIN_TABLE_SCENARIOS
    for actual_key in VIRTUAL_SCENARIOS.get(key, (key,))
}
COMPACT_SCENARIO_NAMES = {
    CURRENT_SYSTEM_KEY: "Stylized U.S.-like benchmark",
    "current-congress-workflow": "Current workflow model",
    "simple-majority": "Simple majority",
    "simple-majority-mediation": "Simple majority + mediation",
    "committee-regular-order": "Committee regular order",
    "committee-amendment-majority": "Committee amendment control",
    "proportional-committee-assignment-majority": "Proportional committees",
    "committee-discharge-target-majority": "Discharge petition",
    "parliamentary-coalition-confidence": "Parliamentary coalition",
    "citizen-initiative-referendum": "Citizen initiative",
    "citizens-agenda-petition-majority": "Citizen agenda petition",
    "simple-majority-alternatives-pairwise": "Pairwise alternatives",
    "pairwise-amendment-tournament-majority": "Amendment tournament",
    CONTENT_SELECTION_KEY: "Content-selection family",
    "citizen-assembly-threshold": "Citizen jury gate",
    "random-public-review-panel-majority": "Random public panel",
    "open-rule-calendar-majority": "Open floor calendar",
    "quadratic-attention-majority": "Attention budget",
    "proposal-bond-majority": "Proposal bond",
    "harm-weighted-majority": "Harm-weighted majority",
    "multidimensional-package-majority": "Package bargaining",
    "anti-capture-majority-bundle": "Anti-capture bundle",
    "anti-capture-access-majority": "Anti-capture access",
    "risk-routed-majority": "Risk-routed majority",
    "portfolio-hybrid-legislature": "Portfolio hybrid",
    "expanded-portfolio-hybrid-legislature": "Expanded portfolio",
    "law-registry-majority": "Law registry",
    "default-pass": "Burden-shifting stress case",
    "default-pass-multiround-mediation-challenge": "Burden shift + mediation",
}
SELECTION_RATIONALES = {
    CURRENT_SYSTEM_KEY: (
        "Conventional benchmark",
        "Stylized U.S.-like conventional benchmark used as the marked baseline; included for comparison, not as a calibrated model of Congress.",
    ),
    "current-congress-workflow": (
        "Agenda-control benchmark",
        "Adds leadership access, committee queueing, floor-rule scheduling, conference, veto, and judicial-review layers to the conventional benchmark.",
    ),
    "simple-majority": (
        "Conventional threshold",
        "Minimal affirmative-vote baseline that isolates the effect of ordinary majority passage.",
    ),
    "simple-majority-mediation": (
        "Fairness control",
        "Gives a conventional majority system a mediation content-improvement step so alternative-selection results are not compared only against unmodified yes/no voting.",
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
    "committee-amendment-majority": (
        "Fairness control",
        "Gives a committee-centered system information and amendment powers before floor voting.",
    ),
    "proportional-committee-assignment-majority": (
        "Committee assignment",
        "Represents party-proportional committee assignment rather than leadership-stacked committee selection.",
    ),
    "committee-discharge-target-majority": (
        "Committee bypass",
        "Represents discharge-petition reform as a backstop against committee burial.",
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
    "citizens-agenda-petition-majority": (
        "Public agenda access",
        "Represents citizen petition pressure forcing agenda access without replacing legislative final passage.",
    ),
    "district-population-majority": (
        "Public representation",
        "Represents district-public signals and population-alignment pressure.",
    ),
    "simple-majority-alternatives-pairwise": (
        "Policy tournament",
        "Main alternative-selection representative; tests agenda manipulation by comparing multiple substitutes before final ratification.",
    ),
    "pairwise-amendment-tournament-majority": (
        "Amendment control",
        "Represents pairwise selection among amended versions before final legislative ratification.",
    ),
    CONTENT_SELECTION_KEY: (
        "Content selection",
        "Combines pairwise alternatives and amendment tournaments in the main narrative because their synthetic outcomes are nearly identical.",
    ),
    "citizen-assembly-threshold": (
        "Mini-public review",
        "Represents citizen-panel certification changing the burden of proof.",
    ),
    "random-public-review-panel-majority": (
        "Mini-public review",
        "Represents a smaller, noisier public review panel as a realism stress variant.",
    ),
    "public-interest-majority": (
        "Public-interest screening",
        "Represents a welfare/support screen under affirmative majority passage.",
    ),
    "open-rule-calendar-majority": (
        "Open floor calendar",
        "Represents a default-open floor calendar with abusive-access screening and high-risk amendment routing.",
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
        "Main package-bargaining representative; tests whether richer cross-issue trades improve revision moderation after administrative load is counted.",
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
    "anti-capture-access-majority": (
        "Anti-capture access",
        "Represents proposal-access firewalls and audits targeted specifically at pre-floor capture.",
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
        "Portfolio",
        "Combines fast lanes, alternatives, citizen/harm review, bonds, anti-capture safeguards, and law review to test safeguard complexity.",
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
        "Burden-shifting stress test",
        "Tests open passage unless a blocking coalition forms.",
    ),
    "default-pass-challenge": (
        "Burden-shifting stress test",
        "Tests whether scarce challenge rights reduce burden-shifting passage risk.",
    ),
    "default-pass-multiround-mediation-challenge": (
        "Burden-shifting stress test",
        "Tests a guarded burden-shifting variant with mediation and challenge vouchers.",
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
        "floor",
        "accessDenied",
        "committeeRejected",
        "welfarePerSubmittedBill",
        "enactedPolicyQuality",
        "policyYield",
        "blockageReliance",
        "publicMandateLegitimacy",
        "representativeQuality",
        "riskControl",
        "administrativeFeasibility",
        "directionalScore",
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


def compromise_priority_score(values: dict[str, float]) -> float:
    return (
        0.30 * clamp01(values.get("compromise", 0.0))
        + 0.20 * clamp01(values.get("productivity", 0.0))
        + 0.20 * clamp01(values.get("riskControl", 0.0))
        + 0.15 * clamp01(values.get("administrativeFeasibility", 0.0))
        + 0.15 * clamp01(values.get("publicMandateLegitimacy", 0.0))
    )


def add_directional_scores(values: dict[str, float]) -> None:
    enacted_policy_quality = values.get("enactedPolicyQuality", mean([
        clamp01(values.get("welfare", 0.0)),
        clamp01(values.get("avgSupport", 0.0)),
        clamp01(values.get("compromise", 0.0)),
        clamp01(values.get("publicAlignment", 0.0)),
        clamp01(values.get("legitimacy", 0.0)),
    ]))
    policy_yield = values.get("policyYield", clamp01(values.get("welfarePerSubmittedBill", 0.0)))
    blockage_reliance = values.get("blockageReliance", mean([
        clamp01(values.get("accessDenied", 0.0)),
        clamp01(values.get("committeeRejected", 0.0)),
        inverse01(values.get("floor", 0.0)),
    ]))
    public_mandate_legitimacy = values.get("publicMandateLegitimacy", mean([
        clamp01(values.get("avgSupport", 0.0)),
        clamp01(values.get("publicAlignment", 0.0)),
        clamp01(values.get("legitimacy", 0.0)),
        inverse01(values.get("weakPublicMandatePassage", 0.0)),
    ]))
    representative_quality = mean([
        enacted_policy_quality,
        policy_yield,
        public_mandate_legitimacy,
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
    values["enactedPolicyQuality"] = enacted_policy_quality
    values["policyYield"] = policy_yield
    values["blockageReliance"] = blockage_reliance
    values["publicMandateLegitimacy"] = public_mandate_legitimacy
    values["representativeQuality"] = representative_quality
    values["riskControl"] = risk_control
    values["administrativeFeasibility"] = administrative_feasibility
    values["harmControl"] = inverse01(values.get("minorityHarm", 0.0))
    values["lowSupportAvoidance"] = inverse01(values.get("weakPublicMandatePassage", 0.0))
    values["directionalScore"] = mean([
        clamp01(values.get("productivity", 0.0)),
        representative_quality,
        risk_control,
        administrative_feasibility,
    ])
    values["compromisePriorityScore"] = compromise_priority_score(values)


def add_virtual_averages(averages: dict[str, dict[str, float]]) -> None:
    for virtual_key, components in VIRTUAL_SCENARIOS.items():
        present = [averages[key] for key in components if key in averages]
        if not present:
            continue
        fields = set().union(*(values.keys() for values in present))
        averages[virtual_key] = {
            field: mean([values[field] for values in present if field in values])
            for field in fields
        }
        add_directional_scores(averages[virtual_key])


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


def percentile(sorted_values: list[float], fraction: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def median_iqr(values: list[float]) -> tuple[float, float, float]:
    if not values:
        return 0.0, 0.0, 0.0
    ordered = sorted(values)
    return percentile(ordered, 0.50), percentile(ordered, 0.25), percentile(ordered, 0.75)


def table_value(values: list[float], decimals: int = 3) -> str:
    avg, half_range = mean_half_range(values)
    return f"{avg:.{decimals}f}$\\pm${half_range:.{decimals}f}"


def oriented_table_value(
    values: list[float],
    direction: str,
    decimals: int = 3,
    bold: bool = False,
) -> str:
    avg, half_range = mean_half_range(values)
    score = inverse01(avg) if direction == "lower" else clamp01(avg)
    shade = 5 + round(32 * score)
    color = f"black!{shade}"
    text = f"{avg:.{decimals}f}$\\pm${half_range:.{decimals}f}"
    if bold:
        text = f"\\textbf{{{text}}}"
    return f"\\colorbox{{{color}}}{{\\makebox[13.5mm][c]{{\\strut {text}}}}}"


def oriented_median_iqr_value(
    values: list[float],
    direction: str,
    decimals: int = 2,
    bold: bool = False,
) -> str:
    median, q1, q3 = median_iqr(values)
    score = inverse01(median) if direction == "lower" else clamp01(median)
    shade = 5 + round(32 * score)
    color = f"black!{shade}"
    text = f"{median:.{decimals}f} [{q1:.{decimals}f},{q3:.{decimals}f}]"
    if bold:
        text = f"\\textbf{{{text}}}"
    return f"\\colorbox{{{color}}}{{\\makebox[17.5mm][c]{{\\strut {text}}}}}"


def oriented_score_color(score: float) -> tuple[str, str]:
    score = clamp01(score)
    shade = 5 + round(32 * score)
    color = f"black!{shade}"
    text_color = "black"
    return color, text_color


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
    if scenario_key in VIRTUAL_SCENARIOS:
        by_case: dict[str, list[float]] = defaultdict(list)
        for component_key in VIRTUAL_SCENARIOS[scenario_key]:
            for row in rows:
                if row["scenarioKey"] != component_key:
                    continue
                numeric = {key: float(value) for key, value in row.items() if value and number_like(value)}
                add_directional_scores(numeric)
                by_case[row["caseKey"]].append(numeric[field])
        return [mean(case_values) for _case, case_values in sorted(by_case.items()) if case_values]
    values: list[float] = []
    for row in rows:
        if row["scenarioKey"] != scenario_key:
            continue
        numeric = {key: float(value) for key, value in row.items() if value and number_like(value)}
        add_directional_scores(numeric)
        values.append(numeric[field])
    return values


def sorted_main_table_scenarios(
    rows: list[dict[str, str]],
    score_field: str = "compromisePriorityScore",
) -> list[tuple[str, str]]:
    present_keys = {row["scenarioKey"] for row in rows}
    return [
        (scenario_key, label)
        for scenario_key, label in MAIN_TABLE_SCENARIOS
        if scenario_key in present_keys or scenario_key in VIRTUAL_SCENARIOS
    ]


def number_like(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def scenario_name(rows: list[dict[str, str]], scenario_key: str) -> str:
    if scenario_key == CONTENT_SELECTION_KEY:
        return "Content-selection family"
    for row in rows:
        if row["scenarioKey"] == scenario_key:
            return row["scenario"]
    return scenario_key


def compact_scenario_name(rows: list[dict[str, str]], scenario_key: str) -> str:
    return COMPACT_SCENARIO_NAMES.get(scenario_key, scenario_name(rows, scenario_key))


def display_label(label: str, scenario_key: str) -> str:
    return f"{label}*" if scenario_key == CURRENT_SYSTEM_KEY else label


def numbered_label(index: int, scenario_key: str) -> str:
    return f"{index}*" if scenario_key == CURRENT_SYSTEM_KEY else str(index)


def write_scenario_selection_manifest(rows: list[dict[str, str]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    present_keys = {row["scenarioKey"] for row in rows}
    lines = [
        "# Scenario Selection Manifest",
        "",
        "Generated by `paper/scripts/generate_figures.py` from the main comparison campaign.",
        "",
        "Selection rule: include the stylized U.S.-like benchmark, simple majority, committee regular order, discharge petition, open floor calendar, a combined content-selection family, anti-capture access, harm-weighted majority, one open burden-shifting stress case, one burden-shifting mediation case, and one portfolio hybrid. Where a family has many implemented variants, the representative is chosen for mechanism clarity rather than for highest observed score. Supplemental family-screen reports evaluate broader catalog champions under a fixed rule.",
        "",
        "| Label | Scenario key | Scenario name | Paper role | Family | Selection rationale |",
        "|---|---|---|---|---|---|",
    ]
    for scenario_key, label in TABLE_SCENARIOS:
        if scenario_key not in present_keys and scenario_key not in VIRTUAL_SCENARIOS:
            continue
        family, rationale = SELECTION_RATIONALES.get(
            scenario_key,
            ("Uncategorized", "Included because it appears in the generated paper scenario list."),
        )
        role = "Main mechanism-family display" if scenario_key in dict(MAIN_TABLE_SCENARIOS) else "Appendix/full comparison"
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
        "Historical burden-shifting sweeps remain available through catalog and campaign reports, but the main paper comparison uses only the two stress-test representatives listed above.",
        "",
    ])
    (REPORT_DIR / "scenario-selection-manifest.md").write_text("\n".join(lines))


def read_family_screen_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_representative_champion_comparison(rows: list[dict[str, str]]) -> None:
    family_rows = read_family_screen_rows(FAMILY_SCREEN_CSV_PATH)
    out_tex = FIGURE_DIR / "representative_champion_table.tex"
    out_csv = REPORT_DIR / "representative-vs-family-champions.csv"
    out_md = REPORT_DIR / "representative-vs-family-champions.md"
    if not family_rows:
        message = "Run `make family-screen` before generating this representative-selection audit."
        out_tex.write_text(
            "% Auto-generated by paper/scripts/generate_figures.py\n"
            "\\begin{table*}\n"
            "  \\caption{Representative-versus-family-champion selection audit.}\n"
            "  \\label{tab:representative-family-champions}\n"
            "  \\Description{Placeholder table for the family-champion selection audit.}\n"
            f"  \\small {latex_escape(message)}\n"
            "\\end{table*}\n"
        )
        out_md.write_text("# Representative vs. Family Champions\n\n" + message + "\n")
        return

    by_name = {row["scenario"]: row for row in family_rows}
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in family_rows:
        by_family[row["family"]].append(row)

    comparison_rows: list[dict[str, str]] = []
    for scenario_key, label in MAIN_TABLE_SCENARIOS:
        selected_name = scenario_name(rows, scenario_key)
        selected = by_name.get(selected_name)
        if selected is None:
            continue
        family = selected["family"]
        champion = max(by_family[family], key=lambda row: float(row["directionalScore"]))
        selected_score = float(selected["directionalScore"])
        champion_score = float(champion["directionalScore"])
        comparison_rows.append({
            "label": label,
            "family": family,
            "representativeScenario": selected_name,
            "representativeDirectional": f"{selected_score:.6f}",
            "championScenario": champion["scenario"],
            "championDirectional": f"{champion_score:.6f}",
            "directionalGap": f"{selected_score - champion_score:.6f}",
            "sameAsChampion": "yes" if selected_name == champion["scenario"] else "no",
        })

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "label",
                "family",
                "representativeScenario",
                "representativeDirectional",
                "championScenario",
                "championDirectional",
                "directionalGap",
                "sameAsChampion",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(comparison_rows)

    md_lines = [
        "# Representative vs. Family Champions",
        "",
        "This generated audit compares each main-table representative that also appears in the breadth-catalog screen with the highest directional-score scenario in that screen's family. Scores come from the fixed `make family-screen` baseline, not from the main campaign.",
        "",
        "| Label | Family | Representative | Rep. dir. | Family champion | Champ. dir. | Gap | Same? |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | --- |",
    ]
    for row in comparison_rows:
        md_lines.append(
            f"| {row['label']} | {row['family']} | {row['representativeScenario']} | "
            f"{float(row['representativeDirectional']):.3f} | {row['championScenario']} | "
            f"{float(row['championDirectional']):.3f} | {float(row['directionalGap']):+.3f} | "
            f"{row['sameAsChampion']} |"
        )
    md_lines.extend([
        "",
        "Negative gaps are expected when the paper chooses a readable family representative instead of the within-family top scorer. This table exists to make that judgment visible rather than implicit.",
    ])
    out_md.write_text("\n".join(md_lines) + "\n")

    notable = [
        row for row in comparison_rows
        if row["sameAsChampion"] == "no" and abs(float(row["directionalGap"])) >= 0.010
    ]
    if not notable:
        notable = [row for row in comparison_rows if row["sameAsChampion"] == "no"][:6]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Representative-versus-family-champion audit. Scores are from the fixed supplemental family-screen baseline, not the main comparison campaign. Negative gaps show cases where the paper uses a readable representative rather than the within-family top scorer.}",
        "  \\label{tab:representative-family-champions}",
        "  \\Description{A generated audit table comparing selected paper representatives with highest-scoring family-screen variants.}",
        "  \\scriptsize",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{lllrrr}",
        "    \\toprule",
        "    Label & Family & Family-screen champion & Rep. dir. & Champ. dir. & Gap \\\\",
        "    \\midrule",
    ]
    for row in notable[:12]:
        lines.append(
            "    "
            + latex_escape(row["label"])
            + " & "
            + latex_escape(row["family"])
            + " & "
            + latex_escape(row["championScenario"])
            + " & "
            + f"{float(row['representativeDirectional']):.3f}"
            + " & "
            + f"{float(row['championDirectional']):.3f}"
            + " & "
            + f"{float(row['directionalGap']):+.3f}"
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}%",
        "  }",
        "\\end{table*}",
        "",
    ])
    out_tex.write_text("\n".join(lines))


def pareto_front(
    averages: dict[str, dict[str, float]],
    fields: tuple[str, ...],
) -> list[str]:
    keys = [key for key, _label in MAIN_TABLE_SCENARIOS if key in averages]
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
        "DP": "Throughput",
        "DPM": "Throughput+med.",
        "XPORT": "Portfolio",
        "PAIR": "Alternatives",
        "AMT": "Amendments",
        "SEL": "Content selection",
    }.get(label, "Frontier")


def write_pareto_front_table(rows: list[dict[str, str]], averages: dict[str, dict[str, float]]) -> None:
    objective_rows = [
        (
            "Productivity + revision moderation + risk",
            frontier_labels(averages, ("productivity", "compromise", "riskControl")),
            "Original narrow frontier.",
        ),
        (
            "Productivity + revision moderation + risk + admin",
            frontier_labels(averages, ("productivity", "compromise", "riskControl", "administrativeFeasibility")),
            "Adding administrative feasibility makes most selected systems non-dominated.",
        ),
        (
            "Yield + risk + admin",
            frontier_labels(averages, ("policyYield", "riskControl", "administrativeFeasibility")),
            "Prioritizes generated public benefit per submitted proposal.",
        ),
        (
            "Public support + harm + admin",
            frontier_labels(averages, ("publicMandateLegitimacy", "harmControl", "administrativeFeasibility")),
            "Prioritizes support, affected-group protection, and feasibility.",
        ),
        (
            "Low-support avoidance + productivity",
            frontier_labels(averages, ("lowSupportAvoidance", "productivity")),
            "Makes low-public-support avoidance a hard objective.",
        ),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Objective-set frontier sensitivity.}",
        "  \\label{tab:pareto-front}",
        "  \\Description{A generated appendix table showing how frontier membership changes under different objective sets.}",
        "  \\small",
        "  \\begin{tabular}{p{0.32\\textwidth}p{0.25\\textwidth}p{0.34\\textwidth}}",
        "    \\toprule",
        "    Objective set & Frontier members & Interpretation \\\\",
        "    \\midrule",
    ]
    for objective, members, interpretation in objective_rows:
        lines.append(
            "    "
            + latex_escape(objective)
            + " & "
            + latex_escape(members)
            + " & "
            + latex_escape(interpretation)
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "  \\par\\smallskip\\footnotesize \\emph{Note:} This table is a sensitivity diagnostic. Frontier membership depends strongly on the objective set.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "pareto_front_table.tex").write_text("\n".join(lines))


def row_numeric_scores(row: dict[str, str]) -> dict[str, float]:
    values = {key: float(value) for key, value in row.items() if value and number_like(value)}
    add_directional_scores(values)
    return values


def label_for_key(scenario_key: str) -> str:
    if scenario_key == CONTENT_SELECTION_KEY:
        return "SEL"
    return dict(TABLE_SCENARIOS).get(scenario_key, scenario_key)


def scenario_metric_summary(averages: dict[str, dict[str, float]], scenario_key: str) -> str:
    values = averages.get(scenario_key)
    if values is None:
        return f"{label_for_key(scenario_key)} missing"
    return (
        f"{label_for_key(scenario_key)} P {values['productivity']:.2f}, "
        f"M {values['compromise']:.2f}, R {values['riskControl']:.2f}, "
        f"A {values['administrativeCost']:.2f}"
    )


def case_sensitivity_result(rows: list[dict[str, str]], case_key: str) -> str:
    case_rows = [
        row for row in rows
        if row["caseKey"] == case_key and row["scenarioKey"] in MAIN_SCENARIO_KEYS
    ]
    if not case_rows:
        return "case not present"
    scored = [(row["scenarioKey"], row_numeric_scores(row)) for row in case_rows]
    content_scores = [
        values["compromisePriorityScore"]
        for scenario_key, values in scored
        if scenario_key in CONTENT_SELECTION_COMPONENTS
    ]
    grouped: list[tuple[str, float]] = []
    if content_scores:
        grouped.append(("SEL", mean(content_scores)))
    for scenario_key, values in scored:
        if scenario_key in CONTENT_SELECTION_COMPONENTS:
            continue
        grouped.append((label_for_key(scenario_key), values["compromisePriorityScore"]))
    grouped.sort(key=lambda item: item[1], reverse=True)
    top = "; ".join(f"{label} {score:.2f}" for label, score in grouped[:3])
    parts = [f"top {top}"]
    dp = next((values for scenario_key, values in scored if scenario_key == "default-pass"), None)
    if dp is not None:
        parts.append(f"DP low supp. {dp['weakPublicMandatePassage']:.2f}")
    return "; ".join(parts)


def frontier_labels(averages: dict[str, dict[str, float]], fields: tuple[str, ...]) -> str:
    labels = [label_for_key(key) for key in pareto_front(averages, fields)]
    return ", ".join(labels) if labels else "none"


def write_sensitivity_controls_table(rows: list[dict[str, str]], averages: dict[str, dict[str, float]]) -> None:
    sensitivity_rows = [
        (
            "Generator",
            "Extreme-beneficial reform",
            case_sensitivity_result(rows, "adversarial-high-benefit-extreme"),
            "Tests whether high-distance proposals can carry high generated public benefit.",
        ),
        (
            "Generator",
            "Revision dilution",
            case_sensitivity_result(rows, "adversarial-compromise-dilution"),
            "Tests whether moderation can reduce generated public benefit.",
        ),
        (
            "Generator",
            "Lobby information",
            case_sensitivity_result(rows, "adversarial-lobby-information"),
            "Tests useful organized information rather than only capture pressure.",
        ),
        (
            "Generator",
            "Public-opinion error",
            case_sensitivity_result(rows, "adversarial-public-opinion-error"),
            "Tests noisy or systematically biased public-support signals.",
        ),
        (
            "Generator",
            "Minority-rights harm",
            case_sensitivity_result(rows, "adversarial-rights-harm"),
            "Tests majority support paired with concentrated rights-like harm.",
        ),
        (
            "Generator",
            "Technocratic delay",
            case_sensitivity_result(rows, "adversarial-delayed-benefit"),
            "Tests low initial support with delayed generated public benefit.",
        ),
        (
            "Fairness",
            "Conventional revision",
            "; ".join([
                scenario_metric_summary(averages, CURRENT_SYSTEM_KEY),
                scenario_metric_summary(averages, "cloture-conference-review"),
            ]),
            "Gives the conventional family conference/review content improvement.",
        ),
        (
            "Fairness",
            "Majority mediation",
            "; ".join([
                scenario_metric_summary(averages, "simple-majority"),
                scenario_metric_summary(averages, "simple-majority-mediation"),
            ]),
            "Compares simple majority with a mediation content-improvement step.",
        ),
        (
            "Fairness",
            "Committee amendment",
            "; ".join([
                scenario_metric_summary(averages, "committee-regular-order"),
                scenario_metric_summary(averages, "committee-amendment-majority"),
            ]),
            "Compares committee gatekeeping with committee information/amendment power.",
        ),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Appendix generator-sensitivity and fairness-control details. These rows summarize robustness probes; they are not validation evidence.}",
        "  \\label{tab:sensitivity-controls}",
        "  \\Description{A generated table summarizing generator sensitivity cases and fairness-control comparisons.}",
        "  \\scriptsize",
        "  \\setlength{\\tabcolsep}{2.0pt}",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{llll}",
        "    \\toprule",
        "    Type & Check & Result & Interpretation \\\\",
        "    \\midrule",
    ]
    for kind, check, result, interpretation in sensitivity_rows:
        lines.append(
            "    "
            + latex_escape(kind)
            + " & "
            + latex_escape(check)
            + " & "
            + latex_escape(result)
            + " & "
            + latex_escape(interpretation)
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}%",
        "  }",
        "  \\par\\smallskip\\footnotesize \\emph{Note:} P is productivity, M is revision moderation, R is risk control, and A is administrative cost. Fairness rows compare content-improvement variants; they do not impose a hard cost-constrained reoptimization.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "sensitivity_controls_table.tex").write_text("\n".join(lines))


def write_robustness_summary_table(rows: list[dict[str, str]], averages: dict[str, dict[str, float]]) -> None:
    summary_rows = [
        (
            "Extreme-beneficial reform",
            "Yes",
            "Portfolio leads and content selection remains close; this directly tests the moderation-friendly benefit generator.",
        ),
        (
            "Revision dilution",
            "Yes",
            "Portfolio leads when moving toward the center can reduce generated value.",
        ),
        (
            "Lobbying information",
            "No major change",
            "Content selection remains strongest when organized lobbying can carry useful information.",
        ),
        (
            "Public-opinion error",
            "Partial",
            "Portfolio and content selection are near-tied when support and benefit decouple.",
        ),
        (
            "Minority-rights harm",
            "No major change",
            "Content selection remains strongest, but the case targets majority-supported concentrated harm.",
        ),
        (
            "Cost-constrained fairness",
            "Unresolved",
            "Reported fairness rows add conventional revision, mediation, and committee amendment; they do not yet hard-budget process cost.",
        ),
        (
            "Ablation/stress probes",
            "Failure modes",
            "No alternatives weakens the content-selection result; clone/decoy, astroturf, and loose-harm cases expose manipulability.",
        ),
        (
            "Objective-set frontier",
            "Yes",
            "Adding administrative feasibility or harm/support objectives changes which systems are non-dominated.",
        ),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Robustness and failure-mode summary. Raw numeric rows are in the appendix.}",
        "  \\label{tab:robustness-summary}",
        "  \\Description{A compact generated table summarizing generator sensitivity, fairness controls, stress tests, and alternative frontier checks.}",
        "  \\small",
        "  \\begin{tabular}{p{0.25\\textwidth}p{0.16\\textwidth}p{0.50\\textwidth}}",
        "    \\toprule",
        "    Probe family & Main pattern changes? & Main implication \\\\",
        "    \\midrule",
    ]
    for probe, changes, implication in summary_rows:
        lines.append(
            "    "
            + latex_escape(probe)
            + " & "
            + latex_escape(changes)
            + " & "
            + latex_escape(implication)
            + " \\\\"
        )
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "robustness_summary_table.tex").write_text("\n".join(lines))


def write_compact_scenario_averages_table(rows: list[dict[str, str]]) -> None:
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}",
        "  \\caption{Selected core metrics from the main campaign, grouped by mechanism family. Entries are median [IQR] across broad and adversarial cases; the appendix reports mean/range, yield, seed diagnostics, and separate PAIR/AMT rows.}",
        "  \\label{tab:scenario-averages}",
        "  \\Description{A generated compact table comparing representative institutional families from the main comparison campaign.}",
        "  \\scriptsize",
        "  \\setlength{\\fboxsep}{0.8pt}",
        "  \\resizebox{\\textwidth}{!}{%",
        "  \\begin{tabular}{llrrrrrrr}",
        "    \\toprule",
        "    Label & Representative system & Prod. $\\uparrow$ & Rev. mod. $\\uparrow$ & Public $\\uparrow$ & Low supp. $\\downarrow$ & Risk ctrl. $\\uparrow$ & Admin $\\downarrow$ & Example profile $\\uparrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key, label in sorted_main_table_scenarios(rows):
        current = scenario_key == CURRENT_SYSTEM_KEY
        cells = [
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "productivity"), "higher", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "compromise"), "higher", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "publicMandateLegitimacy"), "higher", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "weakPublicMandatePassage"), "lower", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "riskControl"), "higher", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "administrativeCost"), "lower", bold=current),
            oriented_median_iqr_value(scenario_case_values(rows, scenario_key, "compromisePriorityScore"), "higher", bold=current),
        ]
        label = display_label(label, scenario_key)
        scenario = latex_escape(compact_scenario_name(rows, scenario_key))
        if current:
            label = f"\\textbf{{{label}}}"
            scenario = f"\\textbf{{{scenario}}}"
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
        "  \\par\\smallskip\\footnotesize \\emph{Note:} Example profile is one revision-moderation-weighted sensitivity check: $0.30\\,\\mathrm{Rev.\\ mod.}+0.20\\,\\mathrm{Prod.}+0.20\\,\\mathrm{Risk\\ ctrl.}+0.15\\,\\mathrm{Admin\\ feas.}+0.15\\,\\mathrm{Public}$. Admin feas. is the inverse of the administrative-cost index shown in the Admin column. Low supp. is low-public-support enactment. The asterisk marks the stylized U.S.-like conventional benchmark. Cell values carry the comparison; shading follows the column arrow as a secondary cue.",
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
        "  \\begin{tabular}{llrrrrrrrrrr}",
        "    \\toprule",
        "    Label & Scenario & Directional $\\uparrow$ & Seed dir. $\\uparrow$ & Prod. $\\uparrow$ & Yield $\\uparrow$ & Rev. mod. $\\uparrow$ & Enacted/run & Low supp. $\\downarrow$ & Block dep. $\\downarrow$ & Admin cost $\\downarrow$ & Risk ctrl. $\\uparrow$ \\\\",
        "    \\midrule",
    ]
    for scenario_key, label in TABLE_SCENARIOS:
        if not any(row["scenarioKey"] == scenario_key for row in rows):
            continue
        label = display_label(label, scenario_key)
        cells = [
            table_value(scenario_case_values(rows, scenario_key, "directionalScore")),
            seed_interval_value(seed_intervals, scenario_key),
            table_value(scenario_case_values(rows, scenario_key, "productivity")),
            table_value(scenario_case_values(rows, scenario_key, "policyYield")),
            table_value(scenario_case_values(rows, scenario_key, "compromise")),
            table_value(scenario_case_values(rows, scenario_key, "enactedPerRun"), 2),
            table_value(scenario_case_values(rows, scenario_key, "weakPublicMandatePassage")),
            table_value(scenario_case_values(rows, scenario_key, "blockageReliance")),
            table_value(scenario_case_values(rows, scenario_key, "administrativeCost")),
            table_value(scenario_case_values(rows, scenario_key, "riskControl")),
        ]
        scenario = latex_escape(scenario_name(rows, scenario_key))
        if scenario_key == CURRENT_SYSTEM_KEY:
            label = f"\\textbf{{{label}}}"
            scenario = f"\\textbf{{{scenario}}}"
            cells = [f"\\textbf{{{cell}}}" for cell in cells]
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
        "  \\par\\smallskip\\footnotesize \\emph{Note:} Case half-ranges are descriptive variation across campaign cases, not statistical confidence intervals. Directional, productivity, yield, revision moderation, low-public-support enactment, blockage reliance, administrative cost, and risk-control values are normalized scores or rates. \\emph{Enacted/run} is an absolute institutional-load count.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "scenario_averages_full_table.tex").write_text("\n".join(lines))


def write_design_space_coverage_table() -> None:
    rows = [
        ("Conventional benchmark", "CUR", "House/Senate/veto gate", "Bottlenecks"),
        ("Simple majority", "SM", "Affirmative threshold", "Low screening"),
        ("Committee regular order", "COMM", "Committee-first gate", "Burial/capture"),
        ("Discharge petition", "DIS", "Committee bypass", "Bypass pressure"),
        ("Open floor calendar", "OPEN", "Default-open agenda", "Floor overload"),
        ("Content selection", "SEL", "Alternatives/tournament", "Clones/agenda manipulation"),
        ("Anti-capture access", "ACG", "Pre-floor capture screen", "Gate bias"),
        ("Harm-weighted majority", "HARM", "Affected-group threshold", "Holdouts"),
        ("Burden-shifting stress", "DP", "Pass unless blocked", "False silence"),
        ("Burden shift + mediation", "DPM", "Mediation plus challenge", "Cost/weak consent"),
        ("Portfolio hybrid", "PORT", "Combined safeguards", "Complexity"),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}[!htbp]",
        "  \\caption{Mechanism families used in the main comparison. Labels match the Results figures; the appendix reports the broader implemented catalog.}",
        "  \\label{tab:design-space-coverage}",
        "  \\Description{A compact generated table showing the main mechanisms represented in the reported comparison, their labels, mechanism themes, and primary stress risks.}",
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
    has_leader = leader and (abs(dx) > 2.2 or abs(dy) > 2.2)
    lines.append(
        f"\\put({fmt(x)},{fmt(y)})"
        f"{{\\makebox(0,0){{\\color{{{color}}}\\rule{{{point_size}}}{{{point_size}}}}}}}"
    )
    if has_leader:
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
    lines.append(
        f"% point-label label={label} pointX={fmt(x)} pointY={fmt(y)} "
        f"labelX={fmt(label_x)} labelY={fmt(label_y)} "
        f"anchor={label_anchor_value} leader={1 if has_leader else 0}"
    )
    lines.append(
        f"\\put({fmt(label_x)},{fmt(label_y)})"
        f"{{\\makebox(0,0)[{label_anchor_value}]{{\\color{{{color}}}{label}}}}}"
    )


def figure_label_width(label: str) -> float:
    return max(4.2, len(label) * 1.25)


def label_box(label_x: float, label_y: float, label: str, anchor: str) -> tuple[float, float, float, float]:
    width = figure_label_width(label)
    if anchor == "l":
        left = label_x
        right = label_x + width
    elif anchor == "r":
        left = label_x - width
        right = label_x
    else:
        left = label_x - (width / 2.0)
        right = label_x + (width / 2.0)
    return left, right, label_y - 2.25, label_y + 2.25


def boxes_overlap(left_a: float, right_a: float, bottom_a: float, top_a: float,
                  left_b: float, right_b: float, bottom_b: float, top_b: float) -> bool:
    return left_a < right_b and right_a > left_b and bottom_a < top_b and top_a > bottom_b


def expanded_box(box: tuple[float, float, float, float], padding_x: float = 0.7,
                 padding_y: float = 0.55) -> tuple[float, float, float, float]:
    left, right, bottom, top = box
    return left - padding_x, right + padding_x, bottom - padding_y, top + padding_y


def point_box(x: float, y: float) -> tuple[float, float, float, float]:
    return x - 1.9, x + 1.9, y - 1.9, y + 1.9


def clamp_label_position(
    label_x: float,
    label_y: float,
    label: str,
    anchor: str,
    picture_width: float,
    picture_height: float,
    label_bounds: tuple[float, float, float, float] | None = None,
) -> tuple[float, float]:
    margin = 0.8
    min_x, max_x, min_y, max_y = label_bounds or (
        margin,
        picture_width - margin,
        margin,
        picture_height - margin,
    )
    left, right, bottom, top = label_box(label_x, label_y, label, anchor)
    if left < min_x:
        label_x += min_x - left
    elif right > max_x:
        label_x -= right - max_x
    left, right, bottom, top = label_box(label_x, label_y, label, anchor)
    if bottom < min_y:
        label_y += min_y - bottom
    elif top > max_y:
        label_y -= top - max_y
    return label_x, label_y


def auto_label_offsets(
    points: list[tuple[str, str, float, float]],
    picture_width: float,
    picture_height: float,
    label_bounds: tuple[float, float, float, float] | None = None,
) -> dict[str, tuple[float, float, str]]:
    candidates: list[tuple[float, float, str]] = []
    for radius_x, radius_y in (
        (3.8, 5.8),
        (7.2, 7.0),
        (10.6, 8.8),
        (14.0, 10.8),
        (18.0, 12.0),
        (22.0, 16.0),
        (26.0, 20.0),
        (30.0, 24.0),
        (34.0, 28.0),
    ):
        candidates.extend([
            (radius_x, radius_y, "l"),
            (-radius_x, radius_y, "r"),
            (radius_x, -radius_y, "l"),
            (-radius_x, -radius_y, "r"),
            (radius_x + 2.8, 0.9, "l"),
            (-(radius_x + 2.8), 0.9, "r"),
            (0.0, radius_y + 2.0, "c"),
            (0.0, -(radius_y + 2.0), "c"),
            (radius_x + 4.5, radius_y * 0.55, "l"),
            (-(radius_x + 4.5), radius_y * 0.55, "r"),
            (radius_x + 4.5, -radius_y * 0.55, "l"),
            (-(radius_x + 4.5), -radius_y * 0.55, "r"),
        ])
    placed: list[tuple[float, float, float, float]] = []
    plotted_point_boxes = [point_box(x, y) for _key, _label, x, y in points]
    placements: dict[str, tuple[float, float, str]] = {}
    fallback_slots: list[tuple[float, float, str]] = []
    min_x, max_x, min_y, max_y = label_bounds or (0.5, picture_width - 0.5, 0.5, picture_height - 0.5)
    for y in (
        max_y - 2.0,
        max_y - 6.0,
        max_y - 10.0,
        max_y - 14.0,
        max_y - 18.0,
        max_y - 22.0,
        max_y - 26.0,
        max_y - 30.0,
        max_y - 34.0,
        max_y - 38.0,
    ):
        fallback_slots.append((picture_width - 4.0, y, "r"))
        fallback_slots.append((4.0, y, "l"))
    for x in (18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0):
        fallback_slots.append((x, min_y + 2.0, "c"))
        fallback_slots.append((x, max_y - 2.0, "c"))
    def local_density(point: tuple[str, str, float, float]) -> int:
        _key, _label, x, y = point
        return sum(1 for _other_key, _other_label, other_x, other_y in points
                   if math.hypot(x - other_x, y - other_y) <= 12.0)

    ordered = sorted(points, key=lambda item: (item[0] != CURRENT_SYSTEM_KEY, -local_density(item), item[3], item[2]))
    for key, label, x, y in ordered:
        selected = candidates[-1]
        selected_box: tuple[float, float, float, float] | None = None
        for dx, dy, anchor in candidates:
            label_x, label_y = clamp_label_position(
                x + dx,
                y + dy,
                label,
                anchor,
                picture_width,
                picture_height,
                label_bounds,
            )
            box = label_box(label_x, label_y, label, anchor)
            if box[0] < min_x or box[1] > max_x or box[2] < min_y or box[3] > max_y:
                continue
            padded_box = expanded_box(box)
            if any(boxes_overlap(*padded_box, *point) for point in plotted_point_boxes):
                continue
            if any(boxes_overlap(*padded_box, *existing) for existing in placed):
                continue
            selected = (label_x - x, label_y - y, anchor)
            selected_box = padded_box
            break
        if selected_box is None:
            for label_x, label_y, anchor in fallback_slots:
                label_x, label_y = clamp_label_position(
                    label_x,
                    label_y,
                    label,
                    anchor,
                    picture_width,
                    picture_height,
                    label_bounds,
                )
                box = label_box(label_x, label_y, label, anchor)
                padded_box = expanded_box(box)
                if any(boxes_overlap(*padded_box, *point) for point in plotted_point_boxes):
                    continue
                if any(boxes_overlap(*padded_box, *existing) for existing in placed):
                    continue
                selected = (label_x - x, label_y - y, anchor)
                selected_box = padded_box
                break
        if selected_box is None:
            dx, dy, anchor = selected
            label_x, label_y = clamp_label_position(
                x + dx,
                y + dy,
                label,
                anchor,
                picture_width,
                picture_height,
                label_bounds,
            )
            selected = (label_x - x, label_y - y, anchor)
            selected_box = expanded_box(label_box(label_x, label_y, label, anchor))
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
        points.append((key, display_label(label, key), x, y))
    return points


def write_productivity_low_support(averages: dict[str, dict[str, float]]) -> None:
    left, bottom, width, height = 16.0, 13.0, 96.0, 58.0
    picture_width, picture_height = 122.0, 82.0
    y_max = 1.0
    points = []
    for key, label in MAIN_TABLE_SCENARIOS:
        if key not in averages:
            continue
        x = left + clamp01(averages[key]["productivity"]) * width
        y = bottom + clamp01(averages[key]["riskControl"]) * height
        points.append((key, display_label(label, key), x, y))
    label_bounds = (left + 2.0, left + width - 2.0, bottom + 4.6, bottom + height - 1.2)
    placements = auto_label_offsets(points, picture_width, picture_height, label_bounds)
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(122,82)",
        "\\footnotesize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom + tick * height
        grid_x = left + tick * width
        lines.extend([
            f"\\put({fmt(grid_x)},{fmt(bottom)}){{\\color{{black!15}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(grid_x)},{fmt(bottom - 3.1)}){{\\makebox(0,0){{{tick:.2g}}}}}",
            f"\\put({fmt(left - 3.2)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
        f"\\put({fmt(left + width)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom + height)}){{\\line(1,0){{{fmt(width)}}}}}",
    ])
    for key, label, x, y in points:
        color = "black"
        point_size = "2.5mm" if key == CURRENT_SYSTEM_KEY else "1.7mm"
        dx, dy, anchor = placements[key]
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor, leader=True)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(bottom + height + 5.8)}){{\\makebox(0,0){{Risk control (higher is better)}}}}",
        f"\\put({fmt(left + width / 2.0)},{fmt(2.0)}){{\\makebox(0,0){{Productivity (share enacted; higher is better)}}}}",
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
    left, bottom, width, height = 16.0, 13.0, 96.0, 58.0
    picture_width, picture_height = 122.0, 82.0
    points = table_points(averages, "productivity", "compromise", left, bottom, width, height)
    label_bounds = (left + 2.0, left + width - 2.0, bottom + 4.6, bottom + height - 1.2)
    placements = auto_label_offsets(points, picture_width, picture_height, label_bounds)
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begingroup",
        "\\setlength{\\unitlength}{1mm}",
        "\\begin{picture}(122,82)",
        "\\footnotesize",
    ]
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = left + tick * width
        y = bottom + tick * height
        lines.extend([
            f"\\put({fmt(x)},{fmt(bottom)}){{\\color{{black!15}}\\line(0,1){{{fmt(height)}}}}}",
            f"\\put({fmt(left)},{fmt(y)}){{\\color{{black!15}}\\line(1,0){{{fmt(width)}}}}}",
            f"\\put({fmt(x)},{fmt(bottom - 3.1)}){{\\makebox(0,0){{{tick:.2g}}}}}",
            f"\\put({fmt(left - 3.2)},{fmt(y)}){{\\makebox(0,0)[r]{{{tick:.2g}}}}}",
        ])
    lines.extend([
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(1,0){{{fmt(width)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
        f"\\put({fmt(left + width)},{fmt(bottom)}){{\\line(0,1){{{fmt(height)}}}}}",
        f"\\put({fmt(left)},{fmt(bottom + height)}){{\\line(1,0){{{fmt(width)}}}}}",
    ])
    for key, label, x, y in points:
        color = "black"
        point_size = "2.5mm" if key == CURRENT_SYSTEM_KEY else "1.8mm"
        dx, dy, anchor = placements[key]
        append_labeled_square(lines, x, y, label, color, point_size, dx, dy, anchor, leader=True)
    lines.extend([
        f"\\put({fmt(left + width / 2.0)},{fmt(bottom + height + 5.8)}){{\\makebox(0,0){{Revision moderation (higher is better)}}}}",
        f"\\put({fmt(left + width / 2.0)},{fmt(2.0)}){{\\makebox(0,0){{Productivity (share enacted; higher is better)}}}}",
        "\\end{picture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "compromise_productivity.tex").write_text("\n".join(lines))


def write_broad_system_comparison(averages: dict[str, dict[str, float]]) -> None:
    scenarios = [(key, label) for key, label in TABLE_SCENARIOS if key in averages]
    metrics = [
        ("productivity", "Prod.", "black"),
        ("compromise", "Rev. mod.", "black!55"),
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


def write_directional_scoreboard(
    averages: dict[str, dict[str, float]],
    rows: list[dict[str, str]],
) -> None:
    scenarios = [(key, label) for key, label in sorted_main_table_scenarios(rows) if key in averages]
    metrics = [
        ("productivity", "Prod."),
        ("compromise", "Rev. mod."),
        ("publicMandateLegitimacy", "Public"),
        ("riskControl", "Risk"),
        ("administrativeFeasibility", "Admin"),
        ("compromisePriorityScore", "Example profile"),
    ]
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "\\begin{table*}[!htbp]",
        "  \\caption{Selected metric profiles for the main mechanisms.}",
        "  \\label{tab:directional-scoreboard}",
        "  \\Description{A compact generated table comparing selected normalized metrics for the main mechanism families.}",
        "  \\small",
        "  \\setlength{\\tabcolsep}{3.2pt}",
        "  \\begin{tabular}{@{}lrrrrrr@{}}",
        "    \\toprule",
        "    Label & Prod. & Rev. mod. & Public & Risk & Admin & Example profile \\\\",
        "    \\midrule",
    ]
    for key, label in scenarios:
        label_text = display_label(label, key)
        cells: list[str] = []
        for field, _short in metrics:
            value = clamp01(averages[key][field])
            fill, text_color = oriented_score_color(value)
            cell_text = f"{value:.2f}"
            if key == CURRENT_SYSTEM_KEY:
                cell_text = f"\\textbf{{{cell_text}}}"
            cells.append(
                f"\\colorbox{{{fill}}}{{\\makebox[11mm][c]{{\\strut \\color{{{text_color}}}{cell_text}}}}}"
            )
        if key == CURRENT_SYSTEM_KEY:
            label_text = f"\\textbf{{{label_text}}}"
        lines.append("    " + label_text + " & " + " & ".join(cells) + " \\\\")
    lines.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "  \\par\\smallskip\\footnotesize \\emph{Note:} Values are normalized to the metric direction shown in Table~\\ref{tab:metric-groups}; grayscale shading is secondary. Admin is administrative feasibility, the inverse of the cost index. The asterisk marks the stylized U.S.-like benchmark.",
        "\\end{table*}",
        "",
    ])
    (FIGURE_DIR / "directional_scoreboard.tex").write_text("\n".join(lines))


def write_timeline_contention(
    case_keys: list[str],
    timeline: dict[str, dict[str, dict[str, float]]],
) -> None:
    scenarios = [
        (CURRENT_SYSTEM_KEY, "CUR", "red", "line width=0.55pt"),
        ("simple-majority", "SM", "black", "line width=0.38pt"),
        ("committee-regular-order", "COMM", "black!55", "line width=0.34pt,dash pattern=on 3pt off 1.8pt"),
        ("parliamentary-coalition-confidence", "PARL", "black!70", "line width=0.36pt,dash pattern=on 5pt off 1.8pt"),
        ("simple-majority-alternatives-pairwise", "PAIR", "black!80", "line width=0.36pt"),
        ("portfolio-hybrid-legislature", "PORT", "black", "line width=0.42pt"),
        ("default-pass", "DP", "black!25", "line width=0.32pt"),
        ("default-pass-multiround-mediation-challenge", "DPM", "black!60", "line width=0.34pt,dash pattern=on 2pt off 1.6pt"),
    ]
    picture_width, picture_height = 128.0, 76.0
    left, bottom, width, height = 18.0, 12.0, 92.0, 54.0
    label_x = left + width + 3.5
    lines = [
        "% Auto-generated by paper/scripts/generate_figures.py",
        "% figure-bounds width=128 height=76",
        "\\begingroup",
        "\\scriptsize",
        "\\begin{tikzpicture}[x=1mm,y=1mm]",
        f"\\path[use as bounding box] (0,0) rectangle ({fmt(picture_width)},{fmt(picture_height)});",
    ]
    if not case_keys:
        lines.extend([
            "\\node at (64,38) {Run \\texttt{make campaign} to generate timeline data.};",
            "\\end{tikzpicture}",
            "\\endgroup",
            "",
        ])
        (FIGURE_DIR / "timeline_contention.tex").write_text("\n".join(lines))
        return

    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom + tick * height
        lines.extend([
            f"\\draw[black!13,line width=0.18pt] ({fmt(left)},{fmt(y)}) -- ({fmt(left + width)},{fmt(y)});",
            f"\\node[anchor=east] at ({fmt(left - 2.8)},{fmt(y)}) {{{tick:.2g}}};",
        ])
    for index, case_key in enumerate(case_keys):
        x = left + (index / max(1, len(case_keys) - 1)) * width
        label = f"E{index + 1}"
        lines.extend([
            f"\\draw[black!12,line width=0.18pt] ({fmt(x)},{fmt(bottom)}) -- ({fmt(x)},{fmt(bottom + height)});",
            f"\\node[anchor=north] at ({fmt(x)},{fmt(bottom - 2.8)}) {{{label}}};",
        ])
    lines.extend([
        f"\\draw[black,line width=0.28pt] ({fmt(left)},{fmt(bottom)}) rectangle ({fmt(left + width)},{fmt(bottom + height)});",
    ])

    endpoint_labels: list[tuple[str, str, str, float, float]] = []
    for scenario_key, label, color, style in scenarios:
        points: list[tuple[float, float]] = []
        for index, case_key in enumerate(case_keys):
            if scenario_key not in timeline.get(case_key, {}):
                continue
            x = left + (index / max(1, len(case_keys) - 1)) * width
            y = bottom + timeline[case_key][scenario_key]["contention"] * height
            points.append((x, y))
        if len(points) < 2:
            continue
        path = " -- ".join(f"({fmt(x)},{fmt(y)})" for x, y in points)
        lines.append(f"\\draw[{color},{style}] {path};")
        radius = 0.78 if scenario_key == CURRENT_SYSTEM_KEY else 0.55
        for x, y in points:
            lines.append(f"\\fill[{color}] ({fmt(x)},{fmt(y)}) circle[radius={radius:.2f}];")
        end_x, end_y = points[-1]
        endpoint_labels.append((scenario_key, label, color, end_x, end_y))

    sorted_endpoints = sorted(endpoint_labels, key=lambda item: item[4])
    label_gap = 5.7
    label_min = bottom + 2.0
    label_max = bottom + height - 1.0
    label_slots = [max(label_min, min(label_max, item[4])) for item in sorted_endpoints]
    for index in range(1, len(label_slots)):
        label_slots[index] = max(label_slots[index], label_slots[index - 1] + label_gap)
    overflow = label_slots[-1] - label_max if label_slots else 0.0
    if overflow > 0.0:
        label_slots = [slot - overflow for slot in label_slots]
    for index in range(1, len(label_slots)):
        label_slots[index] = max(label_slots[index], label_slots[index - 1] + label_gap)

    for (scenario_key, label, color, end_x, end_y), label_y in zip(sorted_endpoints, label_slots):
        label_text = f"\\textbf{{{label}}}" if scenario_key == CURRENT_SYSTEM_KEY else label
        leader_style = "line width=0.25pt" if scenario_key == CURRENT_SYSTEM_KEY else "line width=0.2pt"
        lines.extend([
            f"\\draw[{color},{leader_style}] ({fmt(end_x)},{fmt(end_y)}) -- ({fmt(label_x - 0.8)},{fmt(label_y)});",
            f"% legend-label label={label} x={fmt(label_x)} y={fmt(label_y)}",
            f"\\node[anchor=west,inner sep=0.5pt,text={color}] at ({fmt(label_x)},{fmt(label_y)}) {{{label_text}}};",
        ])
    lines.extend([
        f"\\node at ({fmt(left + width / 2.0)},{fmt(3.0)}) {{Stylized timeline era}};",
        f"\\node[anchor=south] at ({fmt(left + width / 2.0)},{fmt(bottom + height + 3.0)}) {{Contention index (lower is better)}};",
        "\\end{tikzpicture}",
        "\\endgroup",
        "",
    ])
    (FIGURE_DIR / "timeline_contention.tex").write_text("\n".join(lines))


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    broad_rows = read_case_rows(PAPER_CSV_PATH, broad_case)
    base_averages = read_averages(PAPER_CSV_PATH, case_filter=broad_case)
    party_averages = read_averages(PAPER_CSV_PATH, weighted=True, case_filter=party_case)
    add_virtual_averages(base_averages)
    add_virtual_averages(party_averages)
    timeline_cases, timeline_values = read_timeline(PAPER_CSV_PATH, case_filter=timeline_case)
    write_compact_scenario_averages_table(broad_rows)
    write_full_scenario_averages_table(broad_rows)
    write_scenario_selection_manifest(broad_rows)
    write_representative_champion_comparison(broad_rows)
    write_pareto_front_table(broad_rows, base_averages)
    write_sensitivity_controls_table(broad_rows, base_averages)
    write_robustness_summary_table(broad_rows, base_averages)
    write_design_space_coverage_table()
    write_productivity_low_support(base_averages)
    write_default_pass_deltas(base_averages)
    write_compromise_productivity(party_averages)
    write_broad_system_comparison(base_averages)
    write_directional_scoreboard(base_averages, broad_rows)
    write_timeline_contention(timeline_cases, timeline_values)


if __name__ == "__main__":
    main()
