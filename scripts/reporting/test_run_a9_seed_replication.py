#!/usr/bin/env python3
"""Regression tests for A9 multi-seed replication reporting."""

from __future__ import annotations

import csv
import json
import math
import tempfile
import unittest
from pathlib import Path

import run_a9_seed_replication as replication


def test_config() -> replication.Config:
    return replication.Config(
        seeds=(101, 202),
        runs=1,
        legislators=15,
        bills=3,
        workers=1,
        force=False,
        java="java",
        java_props=(),
        app_cp=Path("out/congresssim.jar"),
    )


def synthetic_seed_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for seed_index, seed in enumerate((101, 202)):
        for portfolio, components in replication.PORTFOLIOS.items():
            for information in replication.INFORMATION_LEVELS:
                for budget in replication.BUDGETS:
                    row = {
                        "seed": str(seed),
                        "adversaryId": "A9",
                        "portfolioKey": portfolio,
                        "componentAdversaries": components,
                        "budgetValue": str(budget),
                        "informationLevel": information,
                        "runs": "1",
                        "legislators": "15",
                        "baseBillsPerRun": "3",
                        "traceRows": "3",
                        "meanAttackerResourceSpend": str(budget),
                        "claimBoundary": "synthetic test row",
                    }
                    for metric in replication.METRICS:
                        if metric.lower_bound == 0.0 and metric.upper_bound == 1.0:
                            row[metric.key] = "0.000000" if seed_index == 0 else "0.333333"
                        else:
                            row[metric.key] = "0.100000" if seed_index == 0 else "0.300000"
                    for count_field in replication.EVENT_COUNT_FIELDS.values():
                        row[count_field] = "0" if seed_index == 0 else "1"
                    rows.append(row)
    return rows


class A9SeedReplicationTests(unittest.TestCase):
    def test_seed_panel_requires_distinct_replications(self) -> None:
        self.assertEqual((1, 2, 3), replication.parse_seeds("1, 2,3"))
        self.assertEqual("3 (1 through 3)", replication.seed_panel_label((3, 1, 2)))
        self.assertEqual("2 (1, 3)", replication.seed_panel_label((3, 1)))
        with self.assertRaisesRegex(ValueError, "at least two"):
            replication.parse_seeds("1")
        with self.assertRaisesRegex(ValueError, "duplicates"):
            replication.parse_seeds("1,2,1")

    def test_student_t_interval_uses_seed_level_sample_variance(self) -> None:
        metric = replication.MetricSpec("test", "Test metric")
        summary = replication.summarize_values([0.1, 0.2, 0.3, 0.4, 0.5], metric)
        self.assertAlmostEqual(0.3, summary["mean"])
        self.assertAlmostEqual(math.sqrt(0.025), summary["sampleStdDev"])
        self.assertAlmostEqual(math.sqrt(0.025) / math.sqrt(5), summary["standardError"])
        self.assertAlmostEqual(0.1037, summary["ci95Low"], places=4)
        self.assertAlmostEqual(0.4963, summary["ci95High"], places=4)
        self.assertAlmostEqual(1.0, summary["positiveSeedShare"])
        self.assertAlmostEqual(1.0, summary["signAgreementShare"])

    def test_aggregation_covers_every_cell_and_reconstructs_rate_events(self) -> None:
        rows = synthetic_seed_rows()
        aggregates = replication.aggregate_seed_rows(rows, test_config())
        self.assertEqual(18 * len(replication.METRICS), len(aggregates))
        attack_success = next(
            row
            for row in aggregates
            if row["portfolioKey"] == "clone-decoy-poison-pill"
            and row["informationLevel"] == "medium"
            and row["budgetValue"] == 4
            and row["metric"] == "attackSuccessRate"
        )
        self.assertEqual(2, attack_success["seedCount"])
        self.assertEqual(6, attack_success["evaluatedTraceRows"])
        self.assertEqual(1, attack_success["eventCount"])
        self.assertEqual("0.166666", attack_success["mean"])
        self.assertEqual("0.500000", attack_success["positiveSeedShare"])

    def test_checkpoint_reuse_requires_matching_summary_hash(self) -> None:
        config = test_config()
        rows = synthetic_seed_rows()[:18]
        fieldnames = [field for field in rows[0] if field != "seed"]
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            summary = root / "adversarial-stress-a9-summary.csv"
            checkpoint = root / "checkpoint.json"
            with summary.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows([{key: row[key] for key in fieldnames} for row in rows])
            expected = replication.checkpoint_expectation(config, 101, "source", "script")
            self.assertEqual([], expected["javaProperties"])
            checkpoint.write_text(json.dumps({
                **expected,
                "summarySha256": replication.sha256_file(summary),
            }))
            self.assertTrue(replication.valid_checkpoint(checkpoint, summary, expected, config))
            changed_properties = {**expected, "javaProperties": ["-Dchanged=true"]}
            self.assertFalse(replication.valid_checkpoint(checkpoint, summary, changed_properties, config))
            summary.write_text(summary.read_text() + "\n")
            self.assertFalse(replication.valid_checkpoint(checkpoint, summary, expected, config))


if __name__ == "__main__":
    unittest.main()
