#!/usr/bin/env python3
"""Regression tests for A1 through A8 multi-seed replication reporting."""

from __future__ import annotations

import csv
import json
import math
import tempfile
import unittest
from pathlib import Path

import adversarial_replication_common as common
import run_a1_a8_seed_replication as replication


TEST_SPEC = replication.AdversarySpec(
    "T1",
    "Test adversary",
    "test-summary.csv",
    Path("reports/test-summary.csv"),
    1,
    "meanLoss",
    "Mean loss",
)

TEST_FIELDNAMES = (
    "adversaryId",
    "attackFamily",
    "caseKey",
    "baselineScenario",
    "attackedScenario",
    "mechanismFamily",
    "budgetUnit",
    "budgetValue",
    "informationLevel",
    "runs",
    "legislators",
    "baseBillsPerRun",
    "traceRows",
    "attackSuccessCount",
    "attackSuccessRate",
    "meanLoss",
    "recoveryStatus",
    "traceArtifact",
    "claimBoundary",
)


def test_config(java_props: tuple[str, ...] = ()) -> replication.Config:
    return replication.Config(
        seeds=(101, 202),
        runs=1,
        legislators=15,
        bills=3,
        workers=1,
        force=False,
        java="java",
        java_props=java_props,
        app_cp=Path("out/congresssim.jar"),
    )


def synthetic_summary_row(seed_index: int) -> dict[str, str]:
    success_count = seed_index + 1
    return {
        "adversaryId": "T1",
        "attackFamily": "test_attack",
        "caseKey": "test-case",
        "baselineScenario": "baseline",
        "attackedScenario": "attacked",
        "mechanismFamily": "test_mechanism",
        "budgetUnit": "test_units",
        "budgetValue": "1",
        "informationLevel": "medium",
        "runs": "1",
        "legislators": "15",
        "baseBillsPerRun": "3",
        "traceRows": "3",
        "attackSuccessCount": str(success_count),
        "attackSuccessRate": f"{success_count / 3:.6f}",
        "meanLoss": "0.100000" if seed_index == 0 else "0.300000",
        "recoveryStatus": "not_modeled",
        "traceArtifact": "reports/test-traces.jsonl",
        "claimBoundary": "synthetic test row",
    }


def synthetic_table(seed_index: int) -> replication.SummaryTable:
    return replication.SummaryTable(
        TEST_FIELDNAMES,
        ("attackSuccessRate", "meanLoss"),
        (synthetic_summary_row(seed_index),),
    )


def write_summary(path: Path, row: dict[str, str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TEST_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


class A1A8ReplicationTests(unittest.TestCase):
    def test_seed_parsing_and_panel_labels(self) -> None:
        self.assertEqual(replication.parse_seeds("10, 11,12"), (10, 11, 12))
        self.assertEqual(replication.seed_panel_label((12, 10, 11)), "3 (10 through 12)")
        self.assertEqual(replication.seed_panel_label((10, 12)), "2 (10, 12)")
        with self.assertRaises(ValueError):
            replication.parse_seeds("10")
        with self.assertRaises(ValueError):
            replication.parse_seeds("10,10")

    def test_student_t_interval_math_and_bounds(self) -> None:
        summary = replication.summarize_values([1.0, 3.0])
        self.assertAlmostEqual(summary["mean"], 2.0)
        self.assertAlmostEqual(summary["sampleStdDev"], math.sqrt(2.0))
        self.assertAlmostEqual(summary["standardError"], 1.0)
        self.assertAlmostEqual(summary["ci95Low"], -10.706)
        self.assertAlmostEqual(summary["ci95High"], 14.706)
        bounded = replication.summarize_values([0.0, 1.0], 0.0, 1.0)
        self.assertEqual(bounded["ci95Low"], 0.0)
        self.assertEqual(bounded["ci95High"], 1.0)

    def test_metric_field_discovery_excludes_metadata(self) -> None:
        fields = replication.metric_fields(TEST_FIELDNAMES)
        self.assertEqual(fields, ("attackSuccessRate", "meanLoss"))
        self.assertNotIn("attackSuccessCount", fields)
        self.assertNotIn("traceRows", fields)

    def test_seed_metric_expansion_and_aggregation_cover_panel(self) -> None:
        config = test_config()
        tables = {
            101: {"T1": synthetic_table(0)},
            202: {"T1": synthetic_table(1)},
        }
        seed_rows = replication.seed_metric_rows(tables, config, (TEST_SPEC,))
        self.assertEqual(len(seed_rows), 4)
        self.assertEqual({int(row["seed"]) for row in seed_rows}, {101, 202})
        aggregates = replication.aggregate_seed_metrics(seed_rows, config)
        self.assertEqual(len(aggregates), 2)
        by_metric = {str(row["metric"]): row for row in aggregates}
        success = by_metric["attackSuccessRate"]
        self.assertEqual(success["seedCount"], 2)
        self.assertEqual(success["evaluatedTraceRows"], 6)
        self.assertEqual(success["eventCount"], 3)
        self.assertEqual(success["mean"], "0.500000")
        loss = by_metric["meanLoss"]
        self.assertEqual(loss["eventCount"], "")
        self.assertEqual(loss["mean"], "0.200000")

    def test_summary_reader_rejects_inconsistent_exact_count(self) -> None:
        config = test_config()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / TEST_SPEC.summary_filename
            row = synthetic_summary_row(0)
            row["attackSuccessRate"] = "0.666667"
            write_summary(path, row)
            with self.assertRaises(ValueError):
                replication.read_seed_summary(path, TEST_SPEC, config)

    def test_checkpoint_hashes_and_provenance_invalidate_reuse(self) -> None:
        config = test_config()
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            summary_path = output_dir / TEST_SPEC.summary_filename
            write_summary(summary_path, synthetic_summary_row(0))
            expected = replication.checkpoint_expectation(
                config,
                101,
                "source-hash",
                "script-hash",
                "common-hash",
            )
            checkpoint = {
                **expected,
                "summarySha256ByFile": {
                    TEST_SPEC.summary_filename: common.sha256_file(summary_path),
                },
            }
            (output_dir / "checkpoint.json").write_text(
                json.dumps(checkpoint, indent=2, sort_keys=True) + "\n"
            )
            self.assertTrue(
                replication.valid_checkpoint(output_dir, expected, config, (TEST_SPEC,))
            )

            changed_row = synthetic_summary_row(0)
            changed_row["meanLoss"] = "0.200000"
            write_summary(summary_path, changed_row)
            self.assertFalse(
                replication.valid_checkpoint(output_dir, expected, config, (TEST_SPEC,))
            )

            write_summary(summary_path, synthetic_summary_row(0))
            changed_properties = replication.checkpoint_expectation(
                test_config(("-Dchanged=true",)),
                101,
                "source-hash",
                "script-hash",
                "common-hash",
            )
            self.assertFalse(
                replication.valid_checkpoint(output_dir, changed_properties, config, (TEST_SPEC,))
            )
            changed_script = dict(expected, replicationScriptSha256="changed")
            self.assertFalse(
                replication.valid_checkpoint(output_dir, changed_script, config, (TEST_SPEC,))
            )
            changed_common = dict(expected, commonUtilitySha256="changed")
            self.assertFalse(
                replication.valid_checkpoint(output_dir, changed_common, config, (TEST_SPEC,))
            )


if __name__ == "__main__":
    unittest.main()
