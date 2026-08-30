#!/usr/bin/env python3
"""Tests for stable reuse of the district denominator cache."""

from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "build_district_public_opinion_census_denominator_dataset.py"
)
SPEC = importlib.util.spec_from_file_location("district_denominator_builder", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class DistrictDenominatorCacheTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_output = BUILDER.OUT_CSV
        BUILDER.OUT_CSV = Path(self.temp_dir.name) / "denominators.csv"

    def tearDown(self) -> None:
        BUILDER.OUT_CSV = self.original_output
        self.temp_dir.cleanup()

    def write_rows(self, rows: list[dict[str, str]]) -> None:
        with BUILDER.OUT_CSV.open("w", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=BUILDER.FIELDNAMES,
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)

    def valid_row(self, district_id: str) -> dict[str, str]:
        row = dict.fromkeys(BUILDER.FIELDNAMES, "")
        row.update({
            "district_id": district_id,
            "cd_session": "116",
            "denominator_status": (
                "official_tigerweb_population_housing_denominator"
            ),
        })
        return row

    def test_missing_output_does_not_match(self) -> None:
        self.assertFalse(BUILDER.existing_output_matches(["NY-10"]))

    def test_matching_cache_is_reused(self) -> None:
        self.write_rows([self.valid_row("NY-10"), self.valid_row("OR-03")])
        self.assertTrue(BUILDER.existing_output_matches(["NY-10", "OR-03"]))

    def test_district_order_or_status_drift_forces_refresh(self) -> None:
        rows = [self.valid_row("OR-03"), self.valid_row("NY-10")]
        self.write_rows(rows)
        self.assertFalse(BUILDER.existing_output_matches(["NY-10", "OR-03"]))

        rows = [self.valid_row("NY-10"), self.valid_row("OR-03")]
        rows[1]["denominator_status"] = "stale"
        self.write_rows(rows)
        self.assertFalse(BUILDER.existing_output_matches(["NY-10", "OR-03"]))


if __name__ == "__main__":
    unittest.main()
