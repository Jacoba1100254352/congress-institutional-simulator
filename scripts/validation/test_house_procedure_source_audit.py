#!/usr/bin/env python3
"""Independent arithmetic and attribution checks for the post-fit source audit."""

import copy
import json
import unittest
from write_house_resolution_link_reference import checked_bytes, evidence

from write_house_procedure_source_audit import (
    ACTIONS, METRICS, PANEL, PROVENANCE, audit, chamber, csv_text, read_rows, sensitivity, verify_extract,
)


class AttributionTests(unittest.TestCase):
    def test_resolution_link_has_direct_official_evidence(self):
        link = evidence()
        self.assertEqual("118-hres-1061", link["resolution_id"])
        self.assertEqual("118-hr-4366", link["bill_id"])
        self.assertEqual((339, 85), (link["yeas"], link["nays"]))
        self.assertIn("the bill, H.R. 4366", link["resolution_clause"])
        self.assertIn("not a direct H.R. suspension motion", link["claim_boundary"])

    def test_resolution_source_drift_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Pinned resolution-link source changed"):
            checked_bytes("house-2024-roll064.xml", b"different source")

    def test_csv_bytes_follow_git_line_endings(self):
        self.assertEqual("value\nexample\n", csv_text([{"value": "example"}], ("value",)))

    def test_explicit_senate_does_not_become_house(self):
        self.assertEqual("senate", chamber({"source_name": "Senate", "source_code": "", "action_code": ""}))
        self.assertEqual("senate", chamber({"source_name": "Senate", "source_code": "2", "action_code": "H30000"}))

    def test_house_requires_positive_evidence(self):
        for source in (
            {"source_name": "House floor actions", "source_code": "2", "action_code": ""},
            {"source_name": "Library of Congress", "source_code": "9", "action_code": "H37300"},
            {"source_name": "Library of Congress", "source_code": "9", "action_code": "8000", "text": "Passed/agreed to in House: On motion to suspend the rules..."},
            {"source_name": "Library of Congress", "source_code": "9", "action_code": "9000", "text": "Failed of passage/not agreed to in House On motion to suspend the rules..."},
        ):
            self.assertEqual("house", chamber(source))
        self.assertEqual("unresolved", chamber({"source_name": "", "source_code": "", "action_code": ""}))


class CommittedSourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = read_rows(PANEL)
        cls.actions = read_rows(ACTIONS)
        cls.provenance = json.loads(PROVENANCE.read_text())

    def test_complete_coverage_and_provenance(self):
        self.assertEqual(29335, len(self.panel))
        verify_extract(self.panel, self.actions, self.provenance)

    def test_duplicated_action_is_rejected(self):
        actions = self.actions + [self.actions[0]]
        meta = dict(self.provenance, candidateActionRows=len(actions))
        with self.assertRaisesRegex(ValueError, "Duplicate or orphan"):
            verify_extract(self.panel, actions, meta)

    def test_only_hr4366_changes_and_input_is_not_mutated(self):
        before = copy.deepcopy(self.panel)
        corrected, changes = audit(self.panel, self.actions)
        self.assertEqual(before, self.panel)
        self.assertEqual(["118-hr-4366"], [r["bill_id"] for r in changes])
        self.assertEqual("senate", changes[0]["excluded_chambers"])
        row = next(r for r in corrected if r["bill_id"] == "118-hr-4366")
        self.assertEqual("adopted_special_rule", row["floor_path"])

    def test_fixed_model_sensitivity_is_not_a_refit(self):
        corrected, _ = audit(self.panel, self.actions)
        metrics = sensitivity(self.panel, corrected, read_rows(METRICS))
        test = {r["metric"]: r for r in metrics if r["cohort"] == "test"}
        special = test["specialRuleOnlyRouteShare"]
        self.assertEqual("127", special["original_count"])
        self.assertEqual("128", special["house_screened_count"])
        self.assertEqual("676", special["denominator"])
        self.assertEqual("0.077399380805", special["fixed_simulator_value"])
        expected = 128 / 676 - float(special["fixed_simulator_value"])
        distance = test["routeTotalVariation"]
        self.assertEqual("", distance["fixed_simulator_value"])
        self.assertAlmostEqual(expected, float(distance["house_screened_total_variation"]), places=11)
        self.assertGreater(float(distance["house_screened_total_variation"]), 0.1)
        for row in metrics:
            if row["cohort"] == "development":
                self.assertEqual(row["original_count"], row["house_screened_count"])


if __name__ == "__main__":
    unittest.main()
