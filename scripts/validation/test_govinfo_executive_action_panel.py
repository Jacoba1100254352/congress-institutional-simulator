#!/usr/bin/env python3
"""Regression tests for the compact GovInfo executive-action panel."""

from __future__ import annotations

import argparse
import unittest
from pathlib import Path

try:
    from .build_govinfo_bill_census_dataset import CLASSIFICATION_VERSION
    from .build_govinfo_executive_action_panel import (
        CONTEXT,
        VETO_REFERENCE,
        executive_outcome,
        panel_row,
        parse_congresses,
        read_context,
        read_veto_reference,
        source_law_number_status,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_bill_census_dataset import CLASSIFICATION_VERSION
    from build_govinfo_executive_action_panel import (
        CONTEXT,
        VETO_REFERENCE,
        executive_outcome,
        panel_row,
        parse_congresses,
        read_context,
        read_veto_reference,
        source_law_number_status,
    )


def census_row(**overrides: str) -> dict[str, str]:
    row = {
        "bill_id": "110-hr-6124",
        "congress": "110",
        "bill_type": "hr",
        "bill_number": "6124",
        "origin_chamber": "House",
        "title": "Test Act",
        "policy_area": "Agriculture and Food",
        "sponsor_bioguide_id": "T000001",
        "sponsor_party": "D",
        "presented_to_president_date": "2008-06-16",
        "presented_to_president_basis": "action_code:E20000",
        "vetoed": "1",
        "vetoed_date": "2008-06-18",
        "vetoed_basis": "action_text:presidential_veto",
        "veto_overridden": "1",
        "veto_overridden_date": "2008-06-18",
        "veto_overridden_basis": "action_text:senate_veto_override",
        "enacted": "1",
        "enacted_date": "2008-06-18",
        "enacted_basis": "action_code:36000",
        "law_type": "Public Law",
        "law_number": "106-246; 110-246",
        "recorded_vote_count": "4",
        "actions_count": "88",
        "president_action_count": "3",
        "source_xml_update_date": "2024-01-16",
        "source_xml_sha256": "a" * 64,
        "actions_sha256": "b" * 64,
        "source_archive": "BILLSTATUS-110-hr.zip",
        "source_url": "https://www.govinfo.gov/bulkdata/BILLSTATUS/110/hr/BILLSTATUS-110hr6124.xml",
        "classification_version": CLASSIFICATION_VERSION,
        "integrity_status": "valid",
    }
    row.update(overrides)
    return row


JOINT_VETO_REFERENCE = Path(
    "data/validation/reference/senate_joint_resolution_veto_reference_108_118.csv"
)


class GovInfoExecutiveActionPanelTests(unittest.TestCase):
    def test_parse_congresses_accepts_ranges_and_deduplicates(self) -> None:
        self.assertEqual((108, 109, 110, 118), parse_congresses("108-110,118,109"))

    def test_parse_congresses_rejects_reversed_range(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_congresses("118-108")

    def test_official_context_and_veto_reference_cover_panel_scope(self) -> None:
        contexts = read_context(CONTEXT, tuple(range(108, 119)))
        vetoes = read_veto_reference(VETO_REFERENCE, tuple(range(108, 119)))
        self.assertEqual(11, len(contexts))
        self.assertEqual(21, len(vetoes))
        self.assertEqual("divided", contexts["110"]["government_control"])
        self.assertEqual("disputed_return_pocket", vetoes["111-hr-3808"]["veto_kind"])
        self.assertEqual("1", vetoes["116-hr-6395"]["veto_overridden"])

    def test_panel_row_preserves_override_and_source_anomaly(self) -> None:
        context = read_context(CONTEXT, (110,))["110"]
        veto_reference = read_veto_reference(VETO_REFERENCE, (110,))
        row = panel_row(census_row(), context, veto_reference)
        self.assertEqual("veto_overridden", row["executive_outcome"])
        self.assertEqual("0", row["sponsor_same_party_as_president"])
        self.assertEqual("regular", row["veto_kind_reference"])
        self.assertEqual("2008-06-18", row["veto_date_reference"])
        self.assertEqual("aligned", row["veto_date_alignment"])
        self.assertEqual("source_cross_congress_number", row["source_law_number_status"])

    def test_joint_reference_preserves_audited_source_date_discrepancy(self) -> None:
        vetoes = read_veto_reference(
            JOINT_VETO_REFERENCE,
            tuple(range(108, 119)),
            ("hjres", "sjres"),
        )
        self.assertEqual(26, len(vetoes))
        self.assertEqual({"0"}, {row["veto_overridden"] for row in vetoes.values()})
        reference = vetoes["114-sjres-22"]
        self.assertEqual("2016-01-19", reference["veto_date"])
        self.assertEqual("2016-01-20", reference["govinfo_veto_date"])
        self.assertEqual("source_date_discrepancy", reference["veto_date_alignment"])

        context = read_context(CONTEXT, (114,))["114"]
        row = panel_row(
            census_row(
                bill_id="114-sjres-22",
                congress="114",
                bill_type="sjres",
                bill_number="22",
                origin_chamber="Senate",
                president_action_count="2",
                sponsor_party="R",
                presented_to_president_date="2016-01-19",
                vetoed_date="2016-01-20",
                veto_overridden="0",
                veto_overridden_date="",
                veto_overridden_basis="",
                enacted="0",
                enacted_date="",
                enacted_basis="",
                law_number="",
            ),
            context,
            vetoes,
        )
        self.assertEqual("2016-01-19", row["veto_date_reference"])
        self.assertEqual("2016-01-20", row["vetoed_date"])
        self.assertEqual("source_date_discrepancy", row["veto_date_alignment"])

    def test_unknown_sponsor_party_is_not_forced_into_binary_group(self) -> None:
        context = read_context(CONTEXT, (110,))["110"]
        row = panel_row(census_row(sponsor_party="I"), context, read_veto_reference(VETO_REFERENCE, (110,)))
        self.assertEqual("NA", row["sponsor_same_party_as_president"])

    def test_unresolved_presentment_is_explicit(self) -> None:
        row = census_row(vetoed="0", veto_overridden="0", enacted="0", law_number="")
        self.assertEqual("unresolved_presentment", executive_outcome(row))
        self.assertEqual("not_enacted", source_law_number_status(row))


if __name__ == "__main__":
    unittest.main()
