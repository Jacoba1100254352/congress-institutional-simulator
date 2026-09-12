#!/usr/bin/env python3
"""Tests for the locked House agenda-control descriptive study."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

from write_house_agenda_control_study import (  # noqa: E402
    FLOOR_PATHS,
    build_metrics,
    nearest_rank,
    read_csv,
    validate_inputs,
)


AGENDA_PATH = ROOT / "data/validation/raw/house_agenda_control.csv"
GRANT_PATH = ROOT / "data/validation/raw/house_special_rule_grants.csv"
METRICS_PATH = ROOT / "reports/house-agenda-control-metrics.csv"
REPORT_PATH = ROOT / "reports/house-agenda-control-study.md"
METADATA_PATH = ROOT / "reports/house-agenda-control-study-metadata.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class HouseAgendaControlStudyUnitTests(unittest.TestCase):
    def test_nearest_rank_uses_ceiling_without_interpolation(self) -> None:
        values = [4, 1, 3, 2]
        self.assertEqual(nearest_rank(values, 0.50), 2)
        self.assertEqual(nearest_rank(values, 0.90), 4)
        self.assertIsNone(nearest_rank([], 0.50))

    def test_locked_panels_build_unique_metric_keys(self) -> None:
        agenda = read_csv(AGENDA_PATH)
        grants = read_csv(GRANT_PATH)
        validate_inputs(agenda, grants)
        rows = build_metrics(agenda, grants)
        keys = {
            (row["cohortId"], row["section"], row["metricId"], row["category"])
            for row in rows
        }
        self.assertEqual(len(rows), 469)
        self.assertEqual(len(keys), len(rows))


class HouseAgendaControlStudyArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with METRICS_PATH.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))
        cls.metrics = {
            (row["cohortId"], row["metricId"], row["category"]): row
            for row in cls.rows
        }
        cls.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        cls.report = REPORT_PATH.read_text(encoding="utf-8")

    def metric(self, cohort: str, metric: str, category: str = "") -> dict[str, str]:
        return self.metrics[(cohort, metric, category)]

    def test_exact_primary_counts_and_temporal_denominators(self) -> None:
        self.assertEqual(
            self.metric("development_116_117", "stage_floor_considered_rate")[
                "numerator"
            ],
            "1500",
        )
        self.assertEqual(
            self.metric("development_116_117", "stage_floor_considered_rate")[
                "denominator"
            ],
            "18771",
        )
        self.assertEqual(
            self.metric("118", "transition_committee_advanced_to_floor_rate")
            ["numerator"],
            "600",
        )
        self.assertEqual(
            self.metric("118", "transition_committee_advanced_to_floor_rate")
            ["denominator"],
            "1202",
        )

    def test_floor_paths_sum_to_floor_considered(self) -> None:
        expected = {
            "116": (778, (69, 644, 17, 48)),
            "117": (722, (86, 604, 21, 11)),
            "development_116_117": (1500, (155, 1248, 38, 59)),
            "118": (676, (127, 544, 4, 1)),
        }
        for cohort, (floor_count, path_counts) in expected.items():
            with self.subTest(cohort=cohort):
                actual = tuple(
                    int(self.metric(cohort, "floor_path_count", path)["value"])
                    for path in FLOOR_PATHS
                )
                self.assertEqual(actual, path_counts)
                self.assertEqual(sum(actual), floor_count)
                self.assertEqual(
                    self.metric(cohort, "unidentified_floor_path_count")["value"],
                    "0",
                )

    def test_rule_reconciliation_and_restrictive_share_are_exact(self) -> None:
        self.assertEqual(
            self.metric("117", "survey_literal_minus_narrative", "structured")[
                "value"
            ],
            "-2",
        )
        self.assertEqual(
            self.metric("117", "survey_literal_minus_narrative", "closed")[
                "value"
            ],
            "-2",
        )
        self.assertEqual(
            (
                self.metric("118", "adopted_restrictive_grant_share")["numerator"],
                self.metric("118", "adopted_restrictive_grant_share")["denominator"],
            ),
            ("178", "179"),
        )

    def test_nearest_rank_timing_artifacts_are_exact(self) -> None:
        self.assertEqual(
            self.metric(
                "development_116_117",
                "interval_p50_days",
                "committee_advance_to_floor",
            )["value"],
            "63",
        )
        self.assertEqual(
            self.metric(
                "development_116_117",
                "interval_p90_days",
                "committee_advance_to_floor",
            )["value"],
            "218",
        )
        self.assertEqual(
            self.metric("118", "interval_p50_days", "committee_advance_to_floor")
            ["value"],
            "105",
        )
        self.assertEqual(
            self.metric("118", "interval_p90_days", "committee_advance_to_floor")
            ["value"],
            "292",
        )

    def test_metadata_hashes_current_artifacts(self) -> None:
        sources = {row["path"]: row for row in self.metadata["sources"]}
        outputs = {row["path"]: row for row in self.metadata["outputs"]}
        self.assertEqual(
            sources["data/validation/raw/house_agenda_control.csv"]["sha256"],
            sha256_file(AGENDA_PATH),
        )
        self.assertEqual(
            sources["data/validation/raw/house_special_rule_grants.csv"]["sha256"],
            sha256_file(GRANT_PATH),
        )
        self.assertEqual(
            outputs["reports/house-agenda-control-metrics.csv"]["sha256"],
            sha256_file(METRICS_PATH),
        )
        self.assertEqual(
            outputs["reports/house-agenda-control-study.md"]["sha256"],
            sha256_file(REPORT_PATH),
        )

    def test_report_preserves_calibration_and_causal_boundaries(self) -> None:
        self.assertIn("Source attribution status: **CAVEAT**", self.report)
        self.assertIn("one Senate action used as House suspension evidence", self.report)
        self.assertIn("No identities or categories are imputed", self.report)
        self.assertIn("not a causal estimate of agenda power", self.report)
        self.assertIn("do not authorize parameter fitting", self.report)
        self.assertNotIn("validates the simulator", self.report.casefold())


if __name__ == "__main__":
    unittest.main()
