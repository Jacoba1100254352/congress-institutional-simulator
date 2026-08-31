#!/usr/bin/env python3
"""Tests for the locked presidential-choice temporal transport study."""

from __future__ import annotations

import math
import unittest

try:
    from .write_presidential_choice_study import (
        BILL_PANEL,
        FINAL_VOTE_PANEL,
        JOINT_PANEL,
        StudyRow,
        assemble_study_rows,
        evaluate_probabilities,
        fit_penalized_logistic,
        objective_gradient_information,
        read_csv,
        run_study,
        sigmoid,
        standardize_design,
        validate_frozen_population,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from write_presidential_choice_study import (
        BILL_PANEL,
        FINAL_VOTE_PANEL,
        JOINT_PANEL,
        StudyRow,
        assemble_study_rows,
        evaluate_probabilities,
        fit_penalized_logistic,
        objective_gradient_information,
        read_csv,
        run_study,
        sigmoid,
        standardize_design,
        validate_frozen_population,
    )


def synthetic_row(
    bill_id: str,
    joint_resolution: float,
    divided_government: float,
) -> StudyRow:
    features = {
        "joint_resolution": joint_resolution,
        "divided_government": divided_government,
        "opposition_party_sponsor": 0.0,
        "other_or_unknown_sponsor": 0.0,
        "any_final_roll_call": 0.0,
        "both_final_roll_calls": 0.0,
        "minimum_observed_final_support": 0.0,
        "minimum_observed_opposition_support": 0.0,
    }
    return StudyRow(
        bill_id=bill_id,
        congress=118,
        bill_type="hr",
        measure_class="bill",
        bill_number=1,
        origin_chamber="House",
        president="Test President",
        president_party="D",
        government_control="divided" if divided_government else "unified",
        sponsor_party="D",
        executive_outcome="enacted_without_veto",
        vetoed=0,
        veto_overridden=0,
        recorded_chambers=(),
        minimum_support_raw=None,
        minimum_opposition_support_raw=None,
        features=features,
    )


def decision_fixture() -> dict[str, str]:
    return {
        "bill_id": "118-hr-1",
        "congress": "118",
        "bill_type": "hr",
        "bill_number": "1",
        "origin_chamber": "House",
        "president": "Test President",
        "president_party": "D",
        "government_control": "divided",
        "sponsor_party": "R",
        "executive_outcome": "veto_sustained",
        "vetoed": "1",
        "veto_overridden": "0",
        "presented_to_president_date": "2024-01-10",
        "source_xml_sha256": "source-hash",
        "actions_sha256": "actions-hash",
        "integrity_status": "valid",
    }


def vote_fixture(
    chamber: str,
    *,
    recorded: bool,
    support: str = "",
    opposition_support: str = "",
) -> dict[str, str]:
    return {
        "bill_id": "118-hr-1",
        "chamber": chamber,
        "selection_status": (
            "official_roll_call_selected"
            if recorded
            else "final_approval_without_recorded_vote"
        ),
        "integrity_status": (
            "valid_official_roll_call"
            if recorded
            else "valid_no_recorded_final_approval_vote"
        ),
        "support_share": support,
        "opposition_party_support_share": opposition_support,
        "yea_count": "70" if recorded else "",
        "nay_count": "30" if recorded else "",
        "opposition_party_yea": "60" if recorded else "",
        "opposition_party_nay": "40" if recorded else "",
        "action_date": "2024-01-09",
        "official_source_status": (
            "official_house_clerk_xml"
            if recorded and chamber == "House"
            else "official_senate_lis_xml"
            if recorded
            else "not_applicable_no_recorded_vote"
        ),
        "official_source_bill_match_status": "matched" if recorded else "",
        "official_source_sha256": "vote-source-hash" if recorded else "",
        "decision_source_xml_sha256": "source-hash",
        "decision_actions_sha256": "actions-hash",
    }


def reference_penalized_objective(
    matrix: tuple[tuple[float, ...], ...],
    outcomes: tuple[int, ...],
    coefficients: tuple[float, ...],
    penalty: float,
) -> float:
    log_likelihood = math.fsum(
        outcome * linear_predictor
        - (
            linear_predictor + math.log1p(math.exp(-linear_predictor))
            if linear_predictor >= 0.0
            else math.log1p(math.exp(linear_predictor))
        )
        for values, outcome in zip(matrix, outcomes)
        for linear_predictor in (
            math.fsum(
                value * coefficient
                for value, coefficient in zip(values, coefficients)
            ),
        )
    )
    penalty_term = 0.5 * penalty * math.fsum(
        coefficient * coefficient for coefficient in coefficients[1:]
    )
    return log_likelihood - penalty_term


class PresidentialChoiceStudyTests(unittest.TestCase):
    def test_sigmoid_is_stable_at_extreme_values(self) -> None:
        self.assertEqual(1.0, sigmoid(1000.0))
        self.assertEqual(0.0, sigmoid(-1000.0))
        self.assertAlmostEqual(0.5, sigmoid(0.0), places=15)

    def test_intercept_only_fit_recovers_observed_prevalence(self) -> None:
        matrix = tuple((1.0,) for _ in range(10))
        outcomes = (1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        fit = fit_penalized_logistic(matrix, outcomes)
        self.assertAlmostEqual(0.2, sigmoid(fit.coefficients[0]), places=10)
        self.assertLessEqual(fit.gradient_infinity_norm, 1e-9)
        self.assertLessEqual(fit.step_infinity_norm, 1e-10)

    def test_fixed_penalty_produces_finite_fit_under_separation(self) -> None:
        matrix = ((1.0, -1.0),) * 5 + ((1.0, 1.0),) * 5
        outcomes = (0,) * 5 + (1,) * 5
        fit = fit_penalized_logistic(matrix, outcomes)
        self.assertTrue(all(math.isfinite(value) for value in fit.coefficients))
        self.assertGreater(fit.coefficients[1], 0.0)
        self.assertLessEqual(fit.gradient_infinity_norm, 1e-9)

    def test_analytic_gradient_matches_reference_finite_difference(self) -> None:
        matrix = (
            (1.0, -1.25, 0.0),
            (1.0, -0.25, 1.0),
            (1.0, 0.50, -1.0),
            (1.0, 1.50, 0.5),
        )
        outcomes = (0, 1, 0, 1)
        coefficients = (-0.7, 0.9, -0.4)
        penalty = 0.16
        _, gradient, information = objective_gradient_information(
            matrix, outcomes, coefficients, penalty
        )
        epsilon = 1e-6
        for index, analytic in enumerate(gradient):
            plus = list(coefficients)
            minus = list(coefficients)
            plus[index] += epsilon
            minus[index] -= epsilon
            finite_difference = (
                reference_penalized_objective(
                    matrix, outcomes, tuple(plus), penalty
                )
                - reference_penalized_objective(
                    matrix, outcomes, tuple(minus), penalty
                )
            ) / (2.0 * epsilon)
            self.assertAlmostEqual(analytic, finite_difference, places=8)
        self.assertTrue(
            all(
                math.isclose(
                    information[left][right],
                    information[right][left],
                    rel_tol=0.0,
                    abs_tol=1e-14,
                )
                for left in range(len(information))
                for right in range(len(information))
            )
        )

    def test_scaling_uses_training_rows_and_reports_zero_variance(self) -> None:
        train = (
            synthetic_row("118-hr-1", 0.0, 0.0),
            synthetic_row("118-hr-2", 0.0, 1.0),
        )
        test = (synthetic_row("118-hr-3", 1.0, 1.0),)
        design = standardize_design(
            train, test, ("joint_resolution", "divided_government")
        )
        self.assertEqual(("divided_government",), design.active_features)
        self.assertEqual(
            "omitted_zero_training_variance", design.statuses["joint_resolution"]
        )
        self.assertAlmostEqual(0.5, design.means["divided_government"])
        self.assertAlmostEqual(0.5, design.standard_deviations["divided_government"])
        self.assertEqual(((1.0, -1.0), (1.0, 1.0)), design.train_matrix)
        self.assertEqual(((1.0, 1.0),), design.test_matrix)

    def test_nonrecorded_chamber_is_not_imputed(self) -> None:
        rows = assemble_study_rows(
            [decision_fixture()],
            [
                vote_fixture(
                    "House",
                    recorded=True,
                    support="0.700000",
                    opposition_support="0.600000",
                ),
                vote_fixture("Senate", recorded=False),
            ],
        )
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual(("House",), row.recorded_chambers)
        self.assertAlmostEqual(0.7, row.minimum_support_raw or 0.0)
        self.assertAlmostEqual(0.6, row.minimum_opposition_support_raw or 0.0)
        self.assertEqual(1.0, row.features["any_final_roll_call"])
        self.assertEqual(0.0, row.features["both_final_roll_calls"])
        self.assertAlmostEqual(
            0.7 - (2.0 / 3.0), row.features["minimum_observed_final_support"]
        )

    def test_probability_metrics_match_known_values(self) -> None:
        metrics = evaluate_probabilities((0, 1), (0.25, 0.75))
        self.assertAlmostEqual(-math.log(0.75), metrics["log_loss"], places=15)
        self.assertAlmostEqual(0.0625, metrics["brier"], places=15)
        self.assertAlmostEqual(0.0, metrics["calibration"], places=15)

    def test_full_locked_population_runs_without_feature_or_count_drift(self) -> None:
        bill_decisions = read_csv(BILL_PANEL)
        joint_decisions = read_csv(JOINT_PANEL)
        vote_rows = read_csv(FINAL_VOTE_PANEL)
        rows = assemble_study_rows(bill_decisions + joint_decisions, vote_rows)
        validate_frozen_population(rows, bill_decisions, joint_decisions, vote_rows)
        metrics, coefficients, predictions, full_precision = run_study(rows)
        self.assertEqual(8, len(metrics))
        self.assertEqual(32, len(coefficients))
        self.assertEqual(640, len(predictions))
        self.assertEqual(
            {"primary_118", "secondary_116"},
            set(full_precision["splits"]),
        )
        fitted = [row for row in metrics if row["modelId"] in {"M1", "M2"}]
        self.assertTrue(all(row["fitIterations"] for row in fitted))
        self.assertIn(
            next(
                row
                for row in metrics
                if row["splitId"] == "primary_118" and row["modelId"] == "M2"
            )["primaryGateStatus"],
            {"pass", "fail"},
        )


if __name__ == "__main__":
    unittest.main()
