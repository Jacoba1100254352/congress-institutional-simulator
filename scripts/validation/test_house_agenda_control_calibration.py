#!/usr/bin/env python3
"""Focused tests for the locked House agenda-control calibration."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

import write_house_agenda_control_calibration as study  # noqa: E402


class HouseAgendaControlCalibrationTests(unittest.TestCase):
    def test_java_runtime_major_parser_is_explicit(self) -> None:
        self.assertEqual(21, study.parse_java_major('openjdk version "21.0.11" 2026-04-21'))
        self.assertEqual(8, study.parse_java_major('java version "1.8.0_402"'))
        with self.assertRaises(SystemExit):
            study.parse_java_major("unparseable runtime output")

    def probe_row(
        self,
        *,
        seed: int = 1,
        calendar: float = 0.66,
        special_threshold: float = 0.55,
        suspension_threshold: float = 0.50,
        floor: float = 0.08,
        route_shares: tuple[float, float, float, float] = (
            0.103333333333,
            0.832,
            0.025333333333,
            0.039333333334,
        ),
    ) -> dict[str, str]:
        special, suspension, mixed, other = route_shares
        return {
            "calendarPriorityThreshold": f"{calendar:.3f}",
            "specialRuleThreshold": f"{special_threshold:.3f}",
            "suspensionThreshold": f"{suspension_threshold:.3f}",
            "seed": str(seed),
            "runs": "12",
            "bills": "720",
            "committeeAdvanceRate": "0.102",
            "floorConsiderationRate": f"{floor:.15f}",
            "advanceToFloorRate": "0.0",
            "enactmentRate": "0.025",
            "specialRuleOnlyRouteRate": f"{floor * special:.15f}",
            "suspensionOnlyRouteRate": f"{floor * suspension:.15f}",
            "mixedSpecialRuleAndSuspensionRouteRate": f"{floor * mixed:.15f}",
            "otherFloorRouteRate": f"{floor * other:.15f}",
            "floorRouteAssignmentRate": f"{floor:.15f}",
            "restrictiveSpecialRuleRouteRate": f"{floor * (special + mixed):.15f}",
            "closedRuleRate": "0.060",
            "openRuleRate": "0.042",
            "calendarCapacityDenialRate": "0.022",
        }

    def test_locked_source_targets_and_grid_are_exact(self) -> None:
        targets = study.source_targets()
        self.assertEqual(1_912, targets[study.DEVELOPMENT_COHORT]["committeeAdvanceRate"][0])
        self.assertEqual(676, targets[study.TEST_COHORT]["floorConsiderationRate"][0])
        self.assertEqual(
            study.EXPECTED_CANDIDATES,
            len(study.CALENDAR_THRESHOLDS)
            * len(study.SPECIAL_THRESHOLDS)
            * len(study.SUSPENSION_THRESHOLDS),
        )

    def test_aggregate_reconstructs_conditional_route_shares(self) -> None:
        targets = study.source_targets()[study.DEVELOPMENT_COHORT]
        rows = [self.probe_row(seed=1), self.probe_row(seed=2)]
        candidates = study.aggregate_probe_rows(rows, targets)
        self.assertEqual(1, len(candidates))
        candidate = candidates[0]
        self.assertAlmostEqual(0.08, float(candidate["floorRouteAssignmentRate"]), places=12)
        self.assertAlmostEqual(
            1.0,
            sum(float(candidate[field]) for field in study.ROUTE_FIELDS),
            places=12,
        )
        self.assertAlmostEqual(1.0, float(candidate["restrictiveSpecialRuleShare"]), places=12)

    def test_aggregate_uses_version_stable_float_summation(self) -> None:
        targets = study.source_targets()[study.DEVELOPMENT_COHORT]
        rows = [self.probe_row(seed=seed, floor=0.1) for seed in range(1, 21)]
        for row in rows:
            row["bills"] = "1"
        candidate = study.aggregate_probe_rows(rows, targets)[0]
        self.assertEqual(0.1, candidate["floorConsiderationRate"])

    def test_seed_tables_filter_candidate_and_report_sample_variation(self) -> None:
        probes = [self.probe_row(seed=1, floor=0.06), self.probe_row(seed=2, floor=0.10)]
        probes.append(self.probe_row(seed=3, calendar=0.70))
        targets = study.source_targets()
        seed_rows = []
        for cohort in (study.DEVELOPMENT_COHORT, study.TEST_COHORT):
            seed_rows.extend(study.seed_metric_rows(probes, (0.66, 0.55, 0.50), cohort, targets[cohort]))
        self.assertEqual(4, len(seed_rows))
        self.assertEqual({"1", "2"}, {row["seed"] for row in seed_rows})
        summary = study.monte_carlo_summary(seed_rows)
        self.assertEqual(2 * len(study.MONTE_CARLO_FIELDS), len(summary))
        row = next(row for row in summary if row["cohort"] == study.TEST_COHORT and row["metric"] == "floorConsiderationRate")
        self.assertEqual("0.080000000000", row["mean"])
        self.assertEqual("0.028284271247", row["sampleStandardDeviation"])
        self.assertEqual("0.020000000000", row["standardErrorOfMean"])
        self.assertEqual("0.060000000000", row["minimum"])
        self.assertEqual("0.100000000000", row["maximum"])

    def test_seed_tables_reject_duplicate_seeds(self) -> None:
        row = self.probe_row()
        with self.assertRaisesRegex(SystemExit, "Duplicate Monte Carlo seed"):
            study.seed_metric_rows([row, row], (0.66, 0.55, 0.50), study.TEST_COHORT, study.source_targets()[study.TEST_COHORT])

    def test_aggregate_rejects_nonexclusive_route_total(self) -> None:
        targets = study.source_targets()[study.DEVELOPMENT_COHORT]
        row = self.probe_row()
        row["otherFloorRouteRate"] = "0.020000000000000"
        with self.assertRaises(SystemExit):
            study.aggregate_probe_rows([row], targets)

    def test_selection_uses_locked_tie_break_order(self) -> None:
        first = {
            "selectionLoss": 1.0,
            "maximumAbsoluteStandardizedError": 0.5,
            "calendarPriorityThreshold": 0.64,
            "specialRuleThreshold": 0.55,
            "suspensionThreshold": 0.50,
            "selected": "0",
        }
        second = {
            "selectionLoss": 1.0,
            "maximumAbsoluteStandardizedError": 0.5,
            "calendarPriorityThreshold": 0.66,
            "specialRuleThreshold": 0.35,
            "suspensionThreshold": 0.35,
            "selected": "0",
        }
        selected = study.select_candidate([second, first])
        self.assertIs(first, selected)
        self.assertEqual("1", selected["selected"])

    def test_temporal_gate_requires_every_locked_condition(self) -> None:
        targets = study.source_targets()[study.TEST_COHORT]
        passing = {
            field: targets[field][2]
            for field in (
                "committeeAdvanceRate",
                "floorConsiderationRate",
                *study.ROUTE_FIELDS,
                "restrictiveSpecialRuleShare",
            )
        }
        gate = study.test_gate(passing, targets)
        self.assertEqual("pass", gate["status"])
        failing = dict(passing)
        failing["floorConsiderationRate"] = targets["floorConsiderationRate"][2] + 0.021
        failed_gate = study.test_gate(failing, targets)
        self.assertEqual("fail", failed_gate["status"])
        self.assertFalse(failed_gate["checks"]["floorConsiderationRate"])

    def test_frozen_lifecycle_baseline_remains_unchanged(self) -> None:
        selected = study.validate_baseline()
        self.assertEqual("0.680", selected["calendarPriorityThreshold"])
        self.assertEqual("72000", selected["simulatedBills"])


if __name__ == "__main__":
    unittest.main()
