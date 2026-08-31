#!/usr/bin/env python3
"""Run the locked low-event presidential-choice temporal transport study."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


BILL_PANEL = Path("data/validation/raw/govinfo_executive_action_panel.csv")
JOINT_PANEL = Path("data/validation/raw/govinfo_joint_resolution_panel.csv")
FINAL_VOTE_PANEL = Path("data/validation/raw/govinfo_final_chamber_vote_panel.csv")
SPECIFICATION = Path(
    "papers/empirical-validation/presidential-choice-study-specification.md"
)
SCRIPT_PATH = Path("scripts/validation/write_presidential_choice_study.py")

METRICS_OUTPUT = Path("reports/presidential-choice-study-metrics.csv")
COEFFICIENTS_OUTPUT = Path("reports/presidential-choice-study-coefficients.csv")
PREDICTIONS_OUTPUT = Path("reports/presidential-choice-study-predictions.csv")
REPORT_OUTPUT = Path("reports/presidential-choice-study.md")
METADATA_OUTPUT = Path("reports/presidential-choice-study-metadata.json")

STUDY_VERSION = "presidential-choice-transport-v1"
L2_PENALTY = 0.16
SIMULATOR_RATE = 647 / 2621
PROBABILITY_CLIP = 1e-12
GRADIENT_TOLERANCE = 1e-9
STEP_TOLERANCE = 1e-10
PIVOT_TOLERANCE = 1e-14
ARMIJO_CONSTANT = 1e-4
ARMIJO_ULP_SLACK = 8
MAX_LINE_SEARCH_HALVINGS = 50
MAX_ITERATIONS = 200
PRIMARY_CALIBRATION_TOLERANCE = 0.020

STRUCTURAL_FEATURES = (
    "joint_resolution",
    "divided_government",
    "opposition_party_sponsor",
    "other_or_unknown_sponsor",
    "any_final_roll_call",
    "both_final_roll_calls",
)
SUPPORT_FEATURES = (
    "minimum_observed_final_support",
    "minimum_observed_opposition_support",
)
MODEL_FEATURES = {
    "M1": STRUCTURAL_FEATURES,
    "M2": STRUCTURAL_FEATURES + SUPPORT_FEATURES,
}
MODEL_LABELS = {
    "M0": "training prevalence",
    "M1": "structural penalized logistic",
    "M2": "support penalized logistic",
    "SIM": "frozen simulator constant",
}
MODEL_ORDER = ("M0", "M1", "M2", "SIM")
TYPE_ORDER = {"hr": 0, "s": 1, "hjres": 2, "sjres": 3}
EXPECTED_DECISION_INTEGRITY_STATUSES = {
    "valid",
    "source_date_anomaly:hearing_held_date_before_introduction",
    "source_date_anomaly:committee_reported_date_before_introduction",
    "source_date_anomaly:committee_ordered_reported_date_before_introduction; markup_held_date_before_introduction",
    "source_date_anomaly:floor_considered_date_before_introduction; passed_house_date_before_introduction; passed_origin_chamber_date_before_introduction",
}

SPLITS = (
    {
        "split_id": "secondary_116",
        "role": "secondary_temporal_check",
        "train_start": 108,
        "train_end": 115,
        "test_congress": 116,
        "expected_train_rows": 3203,
        "expected_train_vetoes": 24,
        "expected_test_rows": 353,
        "expected_test_vetoes": 10,
    },
    {
        "split_id": "primary_118",
        "role": "primary_temporal_test",
        "train_start": 108,
        "train_end": 117,
        "test_congress": 118,
        "expected_train_rows": 3921,
        "expected_train_vetoes": 34,
        "expected_test_rows": 287,
        "expected_test_vetoes": 13,
    },
)


class StudyError(RuntimeError):
    """Raised when a locked input or numerical requirement is violated."""


@dataclass(frozen=True)
class StudyRow:
    bill_id: str
    congress: int
    bill_type: str
    measure_class: str
    bill_number: int
    origin_chamber: str
    president: str
    president_party: str
    government_control: str
    sponsor_party: str
    executive_outcome: str
    vetoed: int
    veto_overridden: int
    recorded_chambers: tuple[str, ...]
    minimum_support_raw: float | None
    minimum_opposition_support_raw: float | None
    features: dict[str, float]


@dataclass(frozen=True)
class ScaledDesign:
    feature_names: tuple[str, ...]
    active_features: tuple[str, ...]
    means: dict[str, float]
    standard_deviations: dict[str, float]
    statuses: dict[str, str]
    train_matrix: tuple[tuple[float, ...], ...]
    test_matrix: tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class FitResult:
    coefficients: tuple[float, ...]
    iterations: int
    objective: float
    gradient_infinity_norm: float
    step_infinity_norm: float


def require(condition: bool, message: str) -> None:
    if not condition:
        raise StudyError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_binary(value: str, field: str, bill_id: str) -> int:
    require(value in {"0", "1"}, f"{bill_id}: invalid {field}={value!r}")
    return int(value)


def parse_share(value: str, field: str, bill_id: str) -> float:
    require(value != "", f"{bill_id}: missing {field} on official roll call")
    result = float(value)
    require(math.isfinite(result), f"{bill_id}: nonfinite {field}")
    require(0.0 <= result <= 1.0, f"{bill_id}: out-of-range {field}")
    return result


def bill_sort_key(row: StudyRow) -> tuple[int, int, int, str]:
    return (
        row.congress,
        TYPE_ORDER.get(row.bill_type, 99),
        row.bill_number,
        row.bill_id,
    )


def assemble_study_rows(
    decision_rows: Sequence[dict[str, str]],
    vote_rows: Sequence[dict[str, str]],
) -> list[StudyRow]:
    decisions: dict[str, dict[str, str]] = {}
    for row in decision_rows:
        bill_id = row.get("bill_id", "")
        require(bill_id != "", "Decision row is missing bill_id.")
        require(bill_id not in decisions, f"Duplicate decision row: {bill_id}")
        decisions[bill_id] = row

    votes_by_bill: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in vote_rows:
        bill_id = row.get("bill_id", "")
        require(bill_id in decisions, f"Final-vote row lacks a decision: {bill_id}")
        votes_by_bill[bill_id].append(row)
    require(set(votes_by_bill) == set(decisions), "Decision/final-vote bill IDs differ.")

    result: list[StudyRow] = []
    for bill_id, decision in decisions.items():
        require(
            decision.get("integrity_status", "")
            in EXPECTED_DECISION_INTEGRITY_STATUSES,
            f"{bill_id}: invalid decision-panel integrity status",
        )
        chamber_rows = votes_by_bill[bill_id]
        require(len(chamber_rows) == 2, f"{bill_id}: expected two final-vote rows")
        by_chamber = {row.get("chamber", ""): row for row in chamber_rows}
        require(
            set(by_chamber) == {"House", "Senate"},
            f"{bill_id}: invalid final-vote chamber pair",
        )

        recorded: list[dict[str, str]] = []
        for chamber in ("House", "Senate"):
            vote = by_chamber[chamber]
            action_date = vote.get("action_date", "")
            presentment_date = decision.get("presented_to_president_date", "")
            require(action_date != "", f"{bill_id}: missing selected action date")
            require(presentment_date != "", f"{bill_id}: missing presentment date")
            require(
                action_date <= presentment_date,
                f"{bill_id}: selected final approval follows presentment",
            )
            require(
                vote.get("decision_source_xml_sha256")
                == decision.get("source_xml_sha256"),
                f"{bill_id}: decision source hash mismatch in {chamber}",
            )
            require(
                vote.get("decision_actions_sha256") == decision.get("actions_sha256"),
                f"{bill_id}: decision action hash mismatch in {chamber}",
            )
            if vote.get("selection_status") == "official_roll_call_selected":
                require(
                    vote.get("integrity_status") == "valid_official_roll_call",
                    f"{bill_id}: invalid official roll-call integrity status",
                )
                expected_source = (
                    "official_house_clerk_xml"
                    if chamber == "House"
                    else "official_senate_lis_xml"
                )
                require(
                    vote.get("official_source_status") == expected_source,
                    f"{bill_id}: wrong official source for {chamber}",
                )
                require(
                    vote.get("official_source_bill_match_status")
                    in {"matched", "matched_grouped_question"},
                    f"{bill_id}: official source does not match the measure",
                )
                require(
                    vote.get("official_source_sha256", "") != "",
                    f"{bill_id}: missing official source hash",
                )
                yea = int(vote.get("yea_count", ""))
                nay = int(vote.get("nay_count", ""))
                require(yea + nay > 0, f"{bill_id}: empty yea/nay denominator")
                support = parse_share(
                    vote.get("support_share", ""), "support_share", bill_id
                )
                require(
                    abs(support - yea / (yea + nay)) <= 0.00000051,
                    f"{bill_id}: support share does not reconcile",
                )
                opposition_yea = int(vote.get("opposition_party_yea", ""))
                opposition_nay = int(vote.get("opposition_party_nay", ""))
                require(
                    opposition_yea + opposition_nay > 0,
                    f"{bill_id}: empty opposition-party denominator",
                )
                opposition_support = parse_share(
                    vote.get("opposition_party_support_share", ""),
                    "opposition_party_support_share",
                    bill_id,
                )
                require(
                    abs(
                        opposition_support
                        - opposition_yea / (opposition_yea + opposition_nay)
                    )
                    <= 0.00000051,
                    f"{bill_id}: opposition support share does not reconcile",
                )
                recorded.append(vote)
            else:
                require(
                    vote.get("selection_status")
                    == "final_approval_without_recorded_vote",
                    f"{bill_id}: unexpected final-vote selection status",
                )
                require(
                    vote.get("official_source_status")
                    == "not_applicable_no_recorded_vote",
                    f"{bill_id}: nonrecorded approval has an official vote source",
                )
                require(
                    vote.get("integrity_status")
                    == "valid_no_recorded_final_approval_vote",
                    f"{bill_id}: invalid nonrecorded approval integrity status",
                )
                for field in (
                    "support_share",
                    "opposition_party_support_share",
                    "yea_count",
                    "nay_count",
                ):
                    require(
                        vote.get(field, "") == "",
                        f"{bill_id}: nonrecorded approval has imputed {field}",
                    )

        support_values = [
            parse_share(row.get("support_share", ""), "support_share", bill_id)
            for row in recorded
        ]
        opposition_values = [
            parse_share(
                row.get("opposition_party_support_share", ""),
                "opposition_party_support_share",
                bill_id,
            )
            for row in recorded
        ]
        minimum_support = min(support_values) if support_values else None
        minimum_opposition = min(opposition_values) if opposition_values else None

        bill_type = decision.get("bill_type", "")
        require(bill_type in TYPE_ORDER, f"{bill_id}: invalid bill type {bill_type!r}")
        president_party = decision.get("president_party", "")
        sponsor_party = decision.get("sponsor_party", "")
        require(president_party in {"D", "R"}, f"{bill_id}: invalid president party")
        opposition_sponsor = float(
            sponsor_party in {"D", "R"} and sponsor_party != president_party
        )
        other_sponsor = float(sponsor_party not in {"D", "R"})
        features = {
            "joint_resolution": float(bill_type in {"hjres", "sjres"}),
            "divided_government": float(
                decision.get("government_control") == "divided"
            ),
            "opposition_party_sponsor": opposition_sponsor,
            "other_or_unknown_sponsor": other_sponsor,
            "any_final_roll_call": float(bool(recorded)),
            "both_final_roll_calls": float(len(recorded) == 2),
            "minimum_observed_final_support": (
                minimum_support - (2.0 / 3.0)
                if minimum_support is not None
                else 0.0
            ),
            "minimum_observed_opposition_support": (
                minimum_opposition - 0.5
                if minimum_opposition is not None
                else 0.0
            ),
        }
        vetoed = parse_binary(decision.get("vetoed", ""), "vetoed", bill_id)
        veto_overridden = parse_binary(
            decision.get("veto_overridden", ""), "veto_overridden", bill_id
        )
        require(veto_overridden <= vetoed, f"{bill_id}: override without veto")
        result.append(
            StudyRow(
                bill_id=bill_id,
                congress=int(decision["congress"]),
                bill_type=bill_type,
                measure_class=(
                    "joint_resolution"
                    if bill_type in {"hjres", "sjres"}
                    else "bill"
                ),
                bill_number=int(decision["bill_number"]),
                origin_chamber=decision.get("origin_chamber", ""),
                president=decision.get("president", ""),
                president_party=president_party,
                government_control=decision.get("government_control", ""),
                sponsor_party=sponsor_party,
                executive_outcome=decision.get("executive_outcome", ""),
                vetoed=vetoed,
                veto_overridden=veto_overridden,
                recorded_chambers=tuple(row["chamber"] for row in recorded),
                minimum_support_raw=minimum_support,
                minimum_opposition_support_raw=minimum_opposition,
                features=features,
            )
        )
    return sorted(result, key=bill_sort_key)


def validate_frozen_population(
    rows: Sequence[StudyRow],
    bill_decisions: Sequence[dict[str, str]],
    joint_decisions: Sequence[dict[str, str]],
    vote_rows: Sequence[dict[str, str]],
) -> None:
    require(len(bill_decisions) == 4021, "H.R./S. panel row count drifted.")
    require(len(joint_decisions) == 187, "Joint-resolution panel row count drifted.")
    require(len(rows) == 4208, "Combined presentment row count drifted.")
    require(len({row.bill_id for row in rows}) == 4208, "Decision IDs are not unique.")
    require(len(vote_rows) == 8416, "Final-vote panel row count drifted.")
    require(sum(row.vetoed for row in rows) == 47, "Combined veto count drifted.")
    require(
        sum(row.veto_overridden for row in rows) == 6,
        "Combined override count drifted.",
    )
    require(
        sum(row.measure_class == "bill" and row.vetoed for row in rows) == 21,
        "H.R./S. veto count drifted.",
    )
    require(
        sum(row.measure_class == "joint_resolution" and row.vetoed for row in rows)
        == 26,
        "Joint-resolution veto count drifted.",
    )
    require(
        {row.congress for row in rows} == set(range(108, 119)),
        "Congress scope drifted.",
    )
    coverage = Counter(len(row.recorded_chambers) for row in rows)
    require(
        coverage == Counter({0: 2833, 1: 1065, 2: 310}),
        f"Final-vote coverage drifted: {coverage}",
    )
    require(
        sum(len(row.recorded_chambers) for row in rows) == 1685,
        "Official final-roll-call count drifted.",
    )
    relation = Counter(
        "other"
        if row.features["other_or_unknown_sponsor"]
        else "opposition"
        if row.features["opposition_party_sponsor"]
        else "same"
        for row in rows
    )
    require(
        relation == Counter({"same": 2320, "opposition": 1869, "other": 19}),
        f"Sponsor relation counts drifted: {relation}",
    )
    for split in SPLITS:
        train = [
            row
            for row in rows
            if int(split["train_start"]) <= row.congress <= int(split["train_end"])
        ]
        test = [row for row in rows if row.congress == int(split["test_congress"])]
        require(
            len(train) == int(split["expected_train_rows"]),
            f"{split['split_id']}: training row count drifted",
        )
        require(
            sum(row.vetoed for row in train) == int(split["expected_train_vetoes"]),
            f"{split['split_id']}: training veto count drifted",
        )
        require(
            len(test) == int(split["expected_test_rows"]),
            f"{split['split_id']}: test row count drifted",
        )
        require(
            sum(row.vetoed for row in test) == int(split["expected_test_vetoes"]),
            f"{split['split_id']}: test veto count drifted",
        )


def standardize_design(
    train_rows: Sequence[StudyRow],
    test_rows: Sequence[StudyRow],
    feature_names: Sequence[str],
) -> ScaledDesign:
    require(bool(train_rows), "Cannot standardize an empty training cohort.")
    means: dict[str, float] = {}
    standard_deviations: dict[str, float] = {}
    statuses: dict[str, str] = {}
    active: list[str] = []
    for feature in feature_names:
        values = [row.features[feature] for row in train_rows]
        mean = math.fsum(values) / len(values)
        variance = math.fsum((value - mean) ** 2 for value in values) / len(values)
        standard_deviation = math.sqrt(max(0.0, variance))
        means[feature] = mean
        standard_deviations[feature] = standard_deviation
        if standard_deviation == 0.0:
            statuses[feature] = "omitted_zero_training_variance"
        else:
            statuses[feature] = "fitted"
            active.append(feature)

    def matrix(source: Sequence[StudyRow]) -> tuple[tuple[float, ...], ...]:
        return tuple(
            tuple(
                [1.0]
                + [
                    (row.features[feature] - means[feature])
                    / standard_deviations[feature]
                    for feature in active
                ]
            )
            for row in source
        )

    return ScaledDesign(
        feature_names=tuple(feature_names),
        active_features=tuple(active),
        means=means,
        standard_deviations=standard_deviations,
        statuses=statuses,
        train_matrix=matrix(train_rows),
        test_matrix=matrix(test_rows),
    )


def sigmoid(value: float) -> float:
    if value >= 0.0:
        inverse = math.exp(-value)
        return 1.0 / (1.0 + inverse)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def softplus(value: float) -> float:
    if value >= 0.0:
        return value + math.log1p(math.exp(-value))
    return math.log1p(math.exp(value))


def objective_gradient_information(
    matrix: Sequence[Sequence[float]],
    outcomes: Sequence[int],
    coefficients: Sequence[float],
    penalty: float,
) -> tuple[float, list[float], list[list[float]]]:
    require(len(matrix) == len(outcomes), "Matrix/outcome length mismatch.")
    dimension = len(coefficients)
    require(dimension > 0, "Model must include an intercept.")
    gradient = [0.0] * dimension
    information = [[0.0] * dimension for _ in range(dimension)]
    objective_terms: list[float] = []
    gradient_terms: list[list[float]] = [[] for _ in range(dimension)]
    information_terms: list[list[list[float]]] = [
        [[] for _ in range(dimension)] for _ in range(dimension)
    ]
    for values, outcome in zip(matrix, outcomes):
        require(len(values) == dimension, "Inconsistent design-matrix width.")
        linear_predictor = math.fsum(
            value * coefficient for value, coefficient in zip(values, coefficients)
        )
        probability = sigmoid(linear_predictor)
        residual = outcome - probability
        weight = probability * (1.0 - probability)
        objective_terms.append(outcome * linear_predictor - softplus(linear_predictor))
        for left in range(dimension):
            gradient_terms[left].append(values[left] * residual)
            for right in range(left, dimension):
                information_terms[left][right].append(
                    values[left] * weight * values[right]
                )
    objective = math.fsum(
        objective_terms
        + [-0.5 * penalty * coefficients[index] ** 2 for index in range(1, dimension)]
    )
    for left in range(dimension):
        gradient[left] = math.fsum(
            gradient_terms[left]
            + ([-penalty * coefficients[left]] if left > 0 else [])
        )
        for right in range(left, dimension):
            value = math.fsum(information_terms[left][right])
            information[left][right] = value
            information[right][left] = value
    for index in range(1, dimension):
        information[index][index] += penalty
    require(math.isfinite(objective), "Nonfinite penalized objective.")
    require(all(math.isfinite(value) for value in gradient), "Nonfinite gradient.")
    require(
        all(math.isfinite(value) for row in information for value in row),
        "Nonfinite information matrix.",
    )
    return objective, gradient, information


def solve_linear_system(
    matrix: Sequence[Sequence[float]],
    vector: Sequence[float],
    pivot_tolerance: float = PIVOT_TOLERANCE,
) -> list[float]:
    dimension = len(vector)
    require(len(matrix) == dimension, "Linear-system dimension mismatch.")
    augmented = [list(row) + [vector[index]] for index, row in enumerate(matrix)]
    require(
        all(len(row) == dimension + 1 for row in augmented),
        "Linear system is not square.",
    )
    for column in range(dimension):
        pivot_row = max(
            range(column, dimension), key=lambda index: abs(augmented[index][column])
        )
        pivot = augmented[pivot_row][column]
        require(abs(pivot) >= pivot_tolerance, "Singular penalized Newton system.")
        if pivot_row != column:
            augmented[column], augmented[pivot_row] = (
                augmented[pivot_row],
                augmented[column],
            )
        for row in range(column + 1, dimension):
            factor = augmented[row][column] / augmented[column][column]
            augmented[row][column] = 0.0
            for item in range(column + 1, dimension + 1):
                augmented[row][item] -= factor * augmented[column][item]

    solution = [0.0] * dimension
    for row in range(dimension - 1, -1, -1):
        remainder = math.fsum(
            augmented[row][column] * solution[column]
            for column in range(row + 1, dimension)
        )
        pivot = augmented[row][row]
        require(abs(pivot) >= pivot_tolerance, "Singular back-substitution pivot.")
        solution[row] = (augmented[row][dimension] - remainder) / pivot
    require(all(math.isfinite(value) for value in solution), "Nonfinite Newton step.")
    return solution


def fit_penalized_logistic(
    matrix: Sequence[Sequence[float]],
    outcomes: Sequence[int],
    penalty: float = L2_PENALTY,
) -> FitResult:
    require(bool(matrix), "Cannot fit an empty model matrix.")
    require(all(outcome in {0, 1} for outcome in outcomes), "Outcomes must be binary.")
    dimension = len(matrix[0])
    coefficients = [0.0] * dimension
    last_step_norm = math.inf
    for iteration in range(1, MAX_ITERATIONS + 1):
        objective, gradient, information = objective_gradient_information(
            matrix, outcomes, coefficients, penalty
        )
        gradient_norm = max(abs(value) for value in gradient)
        if gradient_norm <= GRADIENT_TOLERANCE and last_step_norm <= STEP_TOLERANCE:
            return FitResult(
                coefficients=tuple(coefficients),
                iterations=iteration - 1,
                objective=objective,
                gradient_infinity_norm=gradient_norm,
                step_infinity_norm=last_step_norm,
            )
        direction = solve_linear_system(information, gradient)
        direction_norm = max(abs(value) for value in direction)
        if (
            gradient_norm <= GRADIENT_TOLERANCE
            and direction_norm <= STEP_TOLERANCE
        ):
            return FitResult(
                coefficients=tuple(coefficients),
                iterations=iteration - 1,
                objective=objective,
                gradient_infinity_norm=gradient_norm,
                step_infinity_norm=direction_norm,
            )
        directional_derivative = math.fsum(
            gradient[index] * direction[index] for index in range(dimension)
        )
        require(
            directional_derivative > 0.0,
            "Newton direction is not an ascent direction.",
        )
        accepted: tuple[list[float], float, list[float]] | None = None
        step_size = 1.0
        for _ in range(MAX_LINE_SEARCH_HALVINGS + 1):
            candidate = [
                coefficients[index] + step_size * direction[index]
                for index in range(dimension)
            ]
            candidate_objective, candidate_gradient, _ = (
                objective_gradient_information(matrix, outcomes, candidate, penalty)
            )
            armijo_threshold = (
                objective + ARMIJO_CONSTANT * step_size * directional_derivative
            )
            numerical_slack = ARMIJO_ULP_SLACK * math.ulp(
                max(1.0, abs(objective), abs(candidate_objective))
            )
            if candidate_objective + numerical_slack >= armijo_threshold:
                accepted = (candidate, candidate_objective, candidate_gradient)
                break
            step_size *= 0.5
        require(accepted is not None, "Penalized logistic line search failed.")
        candidate, candidate_objective, candidate_gradient = accepted
        last_step_norm = max(
            abs(candidate[index] - coefficients[index]) for index in range(dimension)
        )
        coefficients = candidate
        candidate_gradient_norm = max(abs(value) for value in candidate_gradient)
        if (
            candidate_gradient_norm <= GRADIENT_TOLERANCE
            and last_step_norm <= STEP_TOLERANCE
        ):
            return FitResult(
                coefficients=tuple(coefficients),
                iterations=iteration,
                objective=candidate_objective,
                gradient_infinity_norm=candidate_gradient_norm,
                step_infinity_norm=last_step_norm,
            )
    raise StudyError(f"Penalized logistic fit did not converge in {MAX_ITERATIONS} iterations.")


def predict_probabilities(
    matrix: Sequence[Sequence[float]], coefficients: Sequence[float]
) -> list[float]:
    return [
        sigmoid(math.fsum(value * coefficient for value, coefficient in zip(row, coefficients)))
        for row in matrix
    ]


def evaluate_probabilities(
    outcomes: Sequence[int], probabilities: Sequence[float]
) -> dict[str, float]:
    require(len(outcomes) == len(probabilities), "Outcome/probability length mismatch.")
    require(bool(outcomes), "Cannot evaluate an empty test cohort.")
    clipped = [
        min(1.0 - PROBABILITY_CLIP, max(PROBABILITY_CLIP, probability))
        for probability in probabilities
    ]
    log_loss = math.fsum(
        -outcome * math.log(probability)
        - (1 - outcome) * math.log1p(-probability)
        for outcome, probability in zip(outcomes, clipped)
    ) / len(outcomes)
    brier = math.fsum(
        (probability - outcome) ** 2
        for outcome, probability in zip(outcomes, probabilities)
    ) / len(outcomes)
    mean_probability = math.fsum(probabilities) / len(probabilities)
    observed_rate = math.fsum(outcomes) / len(outcomes)
    return {
        "log_loss": log_loss,
        "brier": brier,
        "calibration": mean_probability - observed_rate,
        "mean_probability": mean_probability,
        "minimum_probability": min(probabilities),
        "maximum_probability": max(probabilities),
        "observed_rate": observed_rate,
    }


def format_float(value: float) -> str:
    return f"{value:.12f}"


def output_coefficient_rows(
    split: dict[str, int | str],
    model_id: str,
    design: ScaledDesign,
    fit: FitResult,
) -> list[dict[str, str]]:
    active_index = {feature: index + 1 for index, feature in enumerate(design.active_features)}
    rows = [
        {
            "splitId": str(split["split_id"]),
            "testCongress": str(split["test_congress"]),
            "modelId": model_id,
            "feature": "intercept",
            "featureStatus": "fitted_unpenalized",
            "trainingMean": "",
            "trainingPopulationSd": "",
            "standardizedCoefficient": format_float(fit.coefficients[0]),
            "oddsRatioPerTrainingSd": "",
            "penaltyLambda": format_float(L2_PENALTY),
            "fitIterations": str(fit.iterations),
        }
    ]
    for feature in design.feature_names:
        index = active_index.get(feature)
        coefficient = fit.coefficients[index] if index is not None else None
        rows.append(
            {
                "splitId": str(split["split_id"]),
                "testCongress": str(split["test_congress"]),
                "modelId": model_id,
                "feature": feature,
                "featureStatus": design.statuses[feature],
                "trainingMean": format_float(design.means[feature]),
                "trainingPopulationSd": format_float(
                    design.standard_deviations[feature]
                ),
                "standardizedCoefficient": (
                    format_float(coefficient) if coefficient is not None else ""
                ),
                "oddsRatioPerTrainingSd": (
                    format_float(math.exp(coefficient)) if coefficient is not None else ""
                ),
                "penaltyLambda": format_float(L2_PENALTY),
                "fitIterations": str(fit.iterations),
            }
        )
    return rows


def run_study(
    rows: Sequence[StudyRow],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, object],
]:
    metrics_rows: list[dict[str, str]] = []
    coefficient_rows: list[dict[str, str]] = []
    prediction_rows: list[dict[str, str]] = []
    full_precision: dict[str, object] = {"splits": {}}

    for split in SPLITS:
        train_rows = [
            row
            for row in rows
            if int(split["train_start"]) <= row.congress <= int(split["train_end"])
        ]
        test_rows = [row for row in rows if row.congress == int(split["test_congress"])]
        train_outcomes = [row.vetoed for row in train_rows]
        test_outcomes = [row.vetoed for row in test_rows]
        prevalence = math.fsum(train_outcomes) / len(train_outcomes)

        probabilities: dict[str, list[float]] = {
            "M0": [prevalence] * len(test_rows),
            "SIM": [SIMULATOR_RATE] * len(test_rows),
        }
        fit_results: dict[str, FitResult] = {}
        designs: dict[str, ScaledDesign] = {}
        for model_id in ("M1", "M2"):
            design = standardize_design(
                train_rows, test_rows, MODEL_FEATURES[model_id]
            )
            fit = fit_penalized_logistic(
                design.train_matrix, train_outcomes, L2_PENALTY
            )
            probabilities[model_id] = predict_probabilities(
                design.test_matrix, fit.coefficients
            )
            fit_results[model_id] = fit
            designs[model_id] = design
            coefficient_rows.extend(
                output_coefficient_rows(split, model_id, design, fit)
            )

        evaluations = {
            model_id: evaluate_probabilities(test_outcomes, probabilities[model_id])
            for model_id in MODEL_ORDER
        }
        baseline_log_loss = evaluations["M0"]["log_loss"]
        baseline_brier = evaluations["M0"]["brier"]
        is_primary = split["split_id"] == "primary_118"
        m2_log_loss_pass = evaluations["M2"]["log_loss"] < baseline_log_loss
        m2_calibration_pass = (
            abs(evaluations["M2"]["calibration"])
            <= PRIMARY_CALIBRATION_TOLERANCE
        )
        primary_gate = "pass" if m2_log_loss_pass and m2_calibration_pass else "fail"

        split_precision: dict[str, object] = {
            "trainRows": len(train_rows),
            "trainVetoes": sum(train_outcomes),
            "testRows": len(test_rows),
            "testVetoes": sum(test_outcomes),
            "models": {},
        }
        for model_id in MODEL_ORDER:
            evaluation = evaluations[model_id]
            fit = fit_results.get(model_id)
            metrics_rows.append(
                {
                    "splitId": str(split["split_id"]),
                    "splitRole": str(split["role"]),
                    "trainCongressStart": str(split["train_start"]),
                    "trainCongressEnd": str(split["train_end"]),
                    "testCongress": str(split["test_congress"]),
                    "modelId": model_id,
                    "modelLabel": MODEL_LABELS[model_id],
                    "predictorCount": (
                        str(len(designs[model_id].active_features))
                        if model_id in designs
                        else "0"
                    ),
                    "trainRows": str(len(train_rows)),
                    "trainVetoes": str(sum(train_outcomes)),
                    "trainVetoRate": format_float(prevalence),
                    "testRows": str(len(test_rows)),
                    "testVetoes": str(sum(test_outcomes)),
                    "testVetoRate": format_float(evaluation["observed_rate"]),
                    "meanPredictedProbability": format_float(
                        evaluation["mean_probability"]
                    ),
                    "minimumPredictedProbability": format_float(
                        evaluation["minimum_probability"]
                    ),
                    "maximumPredictedProbability": format_float(
                        evaluation["maximum_probability"]
                    ),
                    "meanLogLoss": format_float(evaluation["log_loss"]),
                    "brierScore": format_float(evaluation["brier"]),
                    "calibrationInTheLarge": format_float(
                        evaluation["calibration"]
                    ),
                    "logLossDifferenceFromM0": format_float(
                        evaluation["log_loss"] - baseline_log_loss
                    ),
                    "brierDifferenceFromM0": format_float(
                        evaluation["brier"] - baseline_brier
                    ),
                    "gateLogLossStatus": (
                        "pass" if m2_log_loss_pass else "fail"
                    )
                    if is_primary and model_id == "M2"
                    else "not_applicable",
                    "gateCalibrationStatus": (
                        "pass" if m2_calibration_pass else "fail"
                    )
                    if is_primary and model_id == "M2"
                    else "not_applicable",
                    "primaryGateStatus": (
                        primary_gate
                        if is_primary and model_id == "M2"
                        else "not_applicable"
                    ),
                    "fitIterations": str(fit.iterations) if fit else "",
                    "fitObjective": format_float(fit.objective) if fit else "",
                    "fitGradientInfinityNorm": (
                        format_float(fit.gradient_infinity_norm) if fit else ""
                    ),
                    "fitStepInfinityNorm": (
                        format_float(fit.step_infinity_norm) if fit else ""
                    ),
                    "metricStatus": (
                        "primary_locked_model"
                        if model_id == "M2"
                        else "fixed_ablation"
                        if model_id == "M1"
                        else "training_baseline"
                        if model_id == "M0"
                        else "scale_diagnostic_only"
                    ),
                }
            )
            split_precision["models"][model_id] = {
                **evaluation,
                "fitIterations": fit.iterations if fit else None,
                "fitObjective": fit.objective if fit else None,
                "fitGradientInfinityNorm": (
                    fit.gradient_infinity_norm if fit else None
                ),
                "fitStepInfinityNorm": fit.step_infinity_norm if fit else None,
            }
        split_precision["primaryGateStatus"] = primary_gate if is_primary else None
        full_precision["splits"][str(split["split_id"])] = split_precision

        for index, row in enumerate(test_rows):
            prediction_rows.append(
                {
                    "splitId": str(split["split_id"]),
                    "testCongress": str(split["test_congress"]),
                    "billId": row.bill_id,
                    "billType": row.bill_type,
                    "measureClass": row.measure_class,
                    "billNumber": str(row.bill_number),
                    "originChamber": row.origin_chamber,
                    "president": row.president,
                    "presidentParty": row.president_party,
                    "governmentControl": row.government_control,
                    "sponsorParty": row.sponsor_party,
                    "vetoed": str(row.vetoed),
                    "executiveOutcome": row.executive_outcome,
                    "recordedFinalChambers": "|".join(row.recorded_chambers),
                    "anyFinalRollCall": str(
                        int(row.features["any_final_roll_call"])
                    ),
                    "bothFinalRollCalls": str(
                        int(row.features["both_final_roll_calls"])
                    ),
                    "minimumObservedFinalSupport": (
                        format_float(row.minimum_support_raw)
                        if row.minimum_support_raw is not None
                        else ""
                    ),
                    "minimumObservedOppositionSupport": (
                        format_float(row.minimum_opposition_support_raw)
                        if row.minimum_opposition_support_raw is not None
                        else ""
                    ),
                    "m0Probability": format_float(probabilities["M0"][index]),
                    "m1Probability": format_float(probabilities["M1"][index]),
                    "m2Probability": format_float(probabilities["M2"][index]),
                    "simulatorConstantProbability": format_float(
                        probabilities["SIM"][index]
                    ),
                }
            )
    return metrics_rows, coefficient_rows, prediction_rows, full_precision


def write_csv(path: Path, rows: Sequence[dict[str, str]]) -> None:
    require(bool(rows), f"Refusing to write empty output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n", extrasaction="raise"
        )
        writer.writeheader()
        writer.writerows(rows)


def metric_index(metrics_rows: Sequence[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["splitId"], row["modelId"]): row for row in metrics_rows}


def post_fit_concentration_diagnostic(
    prediction_rows: Sequence[dict[str, str]],
) -> dict[str, int | str]:
    primary = [row for row in prediction_rows if row["splitId"] == "primary_118"]
    ranked = sorted(primary, key=lambda row: float(row["m2Probability"]), reverse=True)
    event_ranks = [
        index + 1 for index, row in enumerate(ranked) if row["vetoed"] == "1"
    ]
    joint = [row for row in primary if row["measureClass"] == "joint_resolution"]
    bills = [row for row in primary if row["measureClass"] == "bill"]
    require(len(primary) == 287, "Primary prediction count drifted.")
    require(len(event_ranks) == 13, "Primary prediction veto count drifted.")
    return {
        "status": "post_fit_descriptive_not_gate",
        "primaryMeasures": len(primary),
        "primaryVetoes": len(event_ranks),
        "jointResolutionMeasures": len(joint),
        "jointResolutionVetoes": sum(row["vetoed"] == "1" for row in joint),
        "billMeasures": len(bills),
        "billVetoes": sum(row["vetoed"] == "1" for row in bills),
        "vetoesAmongTop13Predictions": sum(
            row["vetoed"] == "1" for row in ranked[:13]
        ),
        "lowestRankedVetoPosition": max(event_ranks),
    }


def write_report(
    metrics_rows: Sequence[dict[str, str]],
    coefficient_rows: Sequence[dict[str, str]],
    prediction_rows: Sequence[dict[str, str]],
    specification_hash: str,
) -> None:
    metrics = metric_index(metrics_rows)
    primary_m0 = metrics[("primary_118", "M0")]
    primary_m2 = metrics[("primary_118", "M2")]
    secondary_m0 = metrics[("secondary_116", "M0")]
    secondary_m2 = metrics[("secondary_116", "M2")]
    gate = primary_m2["primaryGateStatus"]
    concentration = post_fit_concentration_diagnostic(prediction_rows)
    lines = [
        "# Presidential-Choice Temporal Transport Study",
        "",
        f"Primary locked gate: **{gate.upper()}**.",
        "",
        "This report implements the post-source-audit, pre-fit specification in "
        "`papers/empirical-validation/presidential-choice-study-specification.md`. "
        f"Specification SHA-256: `{specification_hash}`.",
        "",
        "## Result",
        "",
        (
            "On the 118th-Congress test cohort, M2 has mean log loss "
            f"{primary_m2['meanLogLoss']} versus {primary_m0['meanLogLoss']} for "
            "the training-prevalence baseline. Its calibration-in-the-large is "
            f"{primary_m2['calibrationInTheLarge']}. The gate requires strictly "
            "lower log loss and absolute calibration-in-the-large no greater "
            "than 0.020."
        ),
        "",
        (
            "On the secondary 116th-Congress check, M2 has mean log loss "
            f"{secondary_m2['meanLogLoss']} versus {secondary_m0['meanLogLoss']} "
            "for the training-prevalence baseline and calibration-in-the-large "
            f"{secondary_m2['calibrationInTheLarge']}. This check does not "
            "determine the primary gate."
        ),
        "",
        "## Test Metrics",
        "",
        "| Test Congress | Model | Log loss | Brier | Mean predicted | Observed rate | Calibration | Gate |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for split_id in ("secondary_116", "primary_118"):
        for model_id in MODEL_ORDER:
            row = metrics[(split_id, model_id)]
            lines.append(
                "| "
                + " | ".join(
                    [
                        row["testCongress"],
                        f"{model_id}: {row['modelLabel']}",
                        row["meanLogLoss"],
                        row["brierScore"],
                        row["meanPredictedProbability"],
                        row["testVetoRate"],
                        row["calibrationInTheLarge"],
                        row["primaryGateStatus"],
                    ]
                )
                + " |"
            )

    primary_coefficients = [
        row
        for row in coefficient_rows
        if row["splitId"] == "primary_118" and row["modelId"] == "M2"
    ]
    lines.extend(
        [
            "",
            "## Primary M2 Coefficients",
            "",
            "Coefficients are on the training-standardized predictor scale. They are descriptive model parameters, not causal effects or significance tests.",
            "",
            "| Feature | Status | Coefficient | Odds ratio per training SD |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for row in primary_coefficients:
        lines.append(
            f"| `{row['feature']}` | {row['featureStatus']} | "
            f"{row['standardizedCoefficient'] or 'NA'} | "
            f"{row['oddsRatioPerTrainingSd'] or 'NA'} |"
        )

    lines.extend(
        [
            "",
            "## Post-Fit Concentration Audit",
            "",
            "This diagnostic was computed after fitting. It was not prespecified, does not alter the locked gate, and is included to prevent the aggregate score from being read as broad presidential-choice validation.",
            "",
            (
                "The 118th-Congress cohort contains "
                f"{concentration['jointResolutionVetoes']} vetoes among "
                f"{concentration['jointResolutionMeasures']} joint resolutions "
                f"and {concentration['billVetoes']} veto among "
                f"{concentration['billMeasures']} H.R./S. bills. Thus, 12 of "
                "the 13 test events arise from the small joint-resolution class."
            ),
            "",
            (
                "Twelve vetoes appear among the 13 highest M2 probabilities, "
                f"and all 13 appear by rank {concentration['lowestRankedVetoPosition']}. "
                "The score improvement is therefore concentrated in a specific "
                "measure-class and final-vote pattern. Transport to a Congress "
                "with a different resolution mix or political process remains untested."
            ),
            "",
            "## Boundary",
            "",
            "The final-vote pathway is informatively recorded: many measures have voice-vote or unanimous-consent final approvals, and those missing support values are retained rather than imputed. The model mixes H.R./S. measures with separately labeled joint resolutions because measure class is a locked predictor. Its probabilities describe temporal forecasting under the frozen source construction.",
            "",
            "This study does not estimate causal presidential behavior, recover support behind nonrecorded votes, validate bill quality or public preferences, or validate the simulator's veto mechanism and institutional rankings. The simulator constant remains a scale diagnostic rather than a competing fitted bill-level model.",
            "",
            "## Reproduction",
            "",
            "Run `make presidential-choice-study`. The pipeline uses only committed source panels and Python's standard library. Source, specification, implementation, and output hashes are recorded in `reports/presidential-choice-study-metadata.json`.",
            "",
        ]
    )
    REPORT_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def write_metadata(
    metrics_rows: Sequence[dict[str, str]],
    prediction_rows: Sequence[dict[str, str]],
    full_precision: dict[str, object],
) -> None:
    metrics = metric_index(metrics_rows)
    primary = metrics[("primary_118", "M2")]
    sources = []
    for path in (BILL_PANEL, JOINT_PANEL, FINAL_VOTE_PANEL):
        sources.append(
            {
                "path": str(path),
                "sha256": sha256_file(path),
                "rowsExcludingHeader": len(read_csv(path)),
            }
        )
    outputs = []
    for path in (
        METRICS_OUTPUT,
        COEFFICIENTS_OUTPUT,
        PREDICTIONS_OUTPUT,
        REPORT_OUTPUT,
    ):
        outputs.append({"path": str(path), "sha256": sha256_file(path)})
    metadata = {
        "schemaVersion": 1,
        "studyVersion": STUDY_VERSION,
        "claimBoundary": "predictive descriptive temporal transport study; not causal or simulator validation",
        "specification": {
            "path": str(SPECIFICATION),
            "sha256": sha256_file(SPECIFICATION),
            "status": "locked_post_source_audit_pre_fit",
        },
        "implementation": {
            "path": str(SCRIPT_PATH),
            "sha256": sha256_file(SCRIPT_PATH),
            "runtime": "Python standard library",
        },
        "sources": sources,
        "solver": {
            "type": "damped_newton_irls",
            "l2Penalty": L2_PENALTY,
            "interceptPenalized": False,
            "gradientTolerance": GRADIENT_TOLERANCE,
            "stepTolerance": STEP_TOLERANCE,
            "pivotTolerance": PIVOT_TOLERANCE,
            "armijoConstant": ARMIJO_CONSTANT,
            "armijoNumericalSlackUlps": ARMIJO_ULP_SLACK,
            "maximumLineSearchHalvings": MAX_LINE_SEARCH_HALVINGS,
            "maximumIterations": MAX_ITERATIONS,
            "classWeights": False,
            "resampling": False,
            "hyperparameterTuning": False,
        },
        "primaryGate": {
            "testCongress": 118,
            "model": "M2",
            "status": primary["primaryGateStatus"],
            "requiresStrictlyLowerLogLossThanM0": True,
            "absoluteCalibrationTolerance": PRIMARY_CALIBRATION_TOLERANCE,
            "logLossStatus": primary["gateLogLossStatus"],
            "calibrationStatus": primary["gateCalibrationStatus"],
        },
        "postFitConcentrationDiagnostic": post_fit_concentration_diagnostic(
            prediction_rows
        ),
        "fullPrecisionResults": full_precision,
        "outputs": outputs,
    }
    METADATA_OUTPUT.write_text(
        json.dumps(metadata, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for path in (BILL_PANEL, JOINT_PANEL, FINAL_VOTE_PANEL, SPECIFICATION):
        require(path.exists(), f"Missing required locked input: {path}")
    bill_decisions = read_csv(BILL_PANEL)
    joint_decisions = read_csv(JOINT_PANEL)
    vote_rows = read_csv(FINAL_VOTE_PANEL)
    rows = assemble_study_rows(bill_decisions + joint_decisions, vote_rows)
    validate_frozen_population(rows, bill_decisions, joint_decisions, vote_rows)
    metrics, coefficients, predictions, full_precision = run_study(rows)
    write_csv(METRICS_OUTPUT, metrics)
    write_csv(COEFFICIENTS_OUTPUT, coefficients)
    write_csv(PREDICTIONS_OUTPUT, predictions)
    specification_hash = sha256_file(SPECIFICATION)
    write_report(metrics, coefficients, predictions, specification_hash)
    write_metadata(metrics, predictions, full_precision)
    print(f"Wrote {METRICS_OUTPUT}")
    print(f"Wrote {COEFFICIENTS_OUTPUT}")
    print(f"Wrote {PREDICTIONS_OUTPUT}")
    print(f"Wrote {REPORT_OUTPUT}")
    print(f"Wrote {METADATA_OUTPUT}")


if __name__ == "__main__":
    try:
        main()
    except StudyError as error:
        raise SystemExit(str(error)) from error
