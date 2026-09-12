#!/usr/bin/env python3
"""Regression coverage for cached-only empirical report dependency chains."""

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from check_offline_empirical_snapshots import ROOT, check_snapshot


class OfflineEmpiricalSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = b"variable,value\na,1\nb,2\n"
        self.path = self.root / "extract.csv"
        self.path.write_bytes(self.data)
        self.pins = {"extract.csv": (hashlib.sha256(self.data).hexdigest(), 2)}

    def test_committed_snapshot_is_complete(self):
        check_snapshot()

    def test_valid_snapshot_is_not_mutated(self):
        check_snapshot(self.root, self.pins)
        self.assertEqual(self.path.read_bytes(), self.data)

    def test_missing_snapshot_fails_without_fetching(self):
        with self.assertRaisesRegex(SystemExit, "Missing frozen source extract"):
            check_snapshot(self.root, {"absent.csv": next(iter(self.pins.values()))})

    def test_changed_snapshot_fails(self):
        self.path.write_bytes(b"variable,value\na,9\nb,2\n")
        with self.assertRaisesRegex(SystemExit, "Frozen source extract changed"):
            check_snapshot(self.root, self.pins)

    def test_incorrect_row_count_fails(self):
        with self.assertRaisesRegex(SystemExit, "row-count mismatch"):
            check_snapshot(self.root, {"extract.csv": (hashlib.sha256(self.data).hexdigest(), 3)})

    def make_commands(self, target):
        return subprocess.check_output(["make", "-n", target], cwd=ROOT, text=True)

    def test_offline_workflow_rebuilds_reviews_without_source_acquisition(self):
        commands = self.make_commands("reproduce-paper-offline")
        self.assertIn("scripts/checks/check_offline_empirical_snapshots.py", commands)
        for kind in ("candidate", "response_distribution", "codebook_direction"):
            self.assertNotIn(f"build_district_public_opinion_ces_policy_item_{kind}_dataset.py", commands)
            self.assertIn(f"write_district_public_opinion_ces_policy_item_{kind}_review.py", commands)

    def test_explicit_refresh_retains_source_acquisition_chain(self):
        commands = self.make_commands("build-district-public-opinion-ces-policy-item-codebook-direction-raw")
        for kind in ("candidate", "response_distribution", "codebook_direction"):
            self.assertIn(f"build_district_public_opinion_ces_policy_item_{kind}_dataset.py", commands)

    def test_offline_workflow_rebuilds_member_review_without_vote_downloads(self):
        commands = self.make_commands("reproduce-paper-offline")
        self.assertNotIn("build_bill_finance_lobbying_member_vote_target_dataset.py", commands)
        self.assertIn("write_bill_finance_lobbying_member_vote_target_review.py", commands)
        self.assertIn("write_bill_finance_lobbying_roll_call_source_review.py", commands)

    def test_explicit_member_vote_refresh_retains_source_acquisition(self):
        commands = self.make_commands("build-bill-finance-lobbying-member-vote-target-raw")
        self.assertIn("build_bill_finance_lobbying_member_vote_target_dataset.py", commands)


if __name__ == "__main__":
    unittest.main()
