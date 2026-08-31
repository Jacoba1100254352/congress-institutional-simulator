#!/usr/bin/env python3
"""Regression tests for the GovInfo BILLSTATUS census builder."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

try:
    from .build_govinfo_bill_census_dataset import (
        ArchiveInfo,
        CLASSIFICATION_VERSION,
        claim_boundary,
        output_cache_matches,
        parse_bill_xml,
        sha256_file,
    )
    from .write_legislative_lifecycle_calibration import (
        aggregate as aggregate_lifecycle_calibration,
        leave_one_seed_out_selections,
    )
    from .write_legislative_executive_action_diagnostic import diagnostic_row
    from .write_legislative_lifecycle_temporal_replication import (
        build_rows as build_temporal_rows,
        wilson_interval,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_bill_census_dataset import (
        ArchiveInfo,
        CLASSIFICATION_VERSION,
        claim_boundary,
        output_cache_matches,
        parse_bill_xml,
        sha256_file,
    )
    from write_legislative_lifecycle_calibration import (
        aggregate as aggregate_lifecycle_calibration,
        leave_one_seed_out_selections,
    )
    from write_legislative_executive_action_diagnostic import diagnostic_row
    from write_legislative_lifecycle_temporal_replication import (
        build_rows as build_temporal_rows,
        wilson_interval,
    )


V3_XML = """<?xml version="1.0" encoding="utf-8"?>
<billStatus>
  <version>3.0.0</version>
  <bill>
    <number>42</number>
    <updateDate>2023-01-04T10:00:00Z</updateDate>
    <originChamber>House</originChamber>
    <type>HR</type>
    <introducedDate>2021-01-04</introducedDate>
    <congress>117</congress>
    <committees>
      <item>
        <systemCode>hstw00</systemCode>
        <name>Test Committee</name>
        <activities>
          <item><name>Hearings by</name><date>2021-02-01T12:00:00Z</date></item>
          <item><name>Markup by</name><date>2021-02-02T12:00:00Z</date></item>
        </activities>
      </item>
    </committees>
    <committeeReports><committeeReport><citation>H. Rept. 117-1</citation></committeeReport></committeeReports>
    <actions>
      <item>
        <actionDate>2021-06-01</actionDate><text>Became Public Law No: 117-1.</text>
        <type>BecameLaw</type><actionCode>36000</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-05-31</actionDate><text>Presented to President.</text>
        <type>President</type><actionCode>28000</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-05-25</actionDate>
        <text>Passed Senate without amendment by Unanimous Consent.</text><type>Floor</type>
        <sourceSystem><name>Senate</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-05-01</actionDate><text>Passed/agreed to in House: On passage Passed.</text>
        <type>Floor</type><actionCode>8000</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
        <recordedVotes><recordedVote><congress>117</congress><sessionNumber>1</sessionNumber><chamber>House</chamber><rollNumber>10</rollNumber></recordedVote></recordedVotes>
      </item>
      <item>
        <actionDate>2021-03-01</actionDate><text>Reported by the Committee on Test.</text>
        <type>Committee</type><actionCode>5000</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-02-15</actionDate><text>Ordered to be Reported by Voice Vote.</text>
        <type>Committee</type>
        <sourceSystem><code>1</code><name>House committee actions</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-01-04</actionDate><text>Referred to the House Committee on Test.</text>
        <type>IntroReferral</type><actionCode>H11100</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
      </item>
      <item>
        <actionDate>2021-01-04</actionDate><text>Introduced in House</text>
        <type>IntroReferral</type><actionCode>1000</actionCode>
        <sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem>
      </item>
    </actions>
    <sponsors><item><bioguideId>T000001</bioguideId><party>D</party><state>GA</state><district>1</district></item></sponsors>
    <laws><item><number>117-1</number><type>Public Law</type></item></laws>
    <policyArea><name>Test policy</name></policyArea>
    <title>Lifecycle Test Act</title>
  </bill>
</billStatus>
"""


V1_XML = """<?xml version="1.0" encoding="UTF-8"?>
<billStatus>
  <bill>
    <billNumber>10</billNumber>
    <updateDate>2021-01-03T12:00:00Z</updateDate>
    <originChamber>House</originChamber>
    <billType>HR</billType>
    <introducedDate>2021-01-03</introducedDate>
    <congress>117</congress>
    <committees><billCommittees /></committees>
    <committeeReports />
    <actions>
      <item><actionDate>2021-01-03</actionDate><text>Introduced in House</text><type>IntroReferral</type><actionCode>1000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
    </actions>
    <sponsors />
    <laws />
    <policyArea />
    <title>Reserved for the Speaker.</title>
    <version>1.0.0</version>
  </bill>
</billStatus>
"""


SPECIAL_RULE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<billStatus>
  <bill>
    <number>77</number><updateDate>2022-01-01T00:00:00Z</updateDate>
    <originChamber>House</originChamber><type>HR</type>
    <introducedDate>2021-01-04</introducedDate><congress>117</congress>
    <committees><item><systemCode>hstw00</systemCode><name>Test Committee</name></item></committees>
    <committeeReports />
    <actions>
      <item><actionDate>2021-03-03</actionDate><text>Mr. Test asked unanimous consent that the Committee on Test be discharged from further consideration of H.R. 77. Objection heard.</text><type>Floor</type><actionCode>H8D000</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2021-03-02</actionDate><text>Rule H. Res. 10 passed House.</text><type>Floor</type><actionCode>H1L220</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2021-03-01</actionDate><text>Rules Committee Resolution H. Res. 10 Reported to House. Rule provides for consideration of H.R. 77.</text><type>Floor</type><actionCode>H1L210</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2021-01-04</actionDate><text>Referred to the House Committee on Test.</text><type>IntroReferral</type><actionCode>H11100</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
    </actions>
    <sponsors><item><bioguideId>T000001</bioguideId><party>D</party><state>GA</state><district>1</district></item></sponsors>
    <laws /><policyArea><name>Test policy</name></policyArea><title>Special Rule Test Act</title>
  </bill>
</billStatus>
"""


PRESIDENTIAL_ACTION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<billStatus>
  <bill>
    <number>4199</number><updateDate>2025-01-03T00:00:00Z</updateDate>
    <originChamber>Senate</originChamber><type>S</type>
    <introducedDate>2024-04-19</introducedDate><congress>118</congress>
    <committees><item><systemCode>ssju00</systemCode><name>Committee on the Judiciary</name></item></committees>
    <committeeReports />
    <actions>
      {override_actions}
      <item><actionDate>2024-12-23</actionDate><text>{presidential_text}</text><type>President</type><actionCode>E30000</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2024-12-20</actionDate><text>Presented to President.</text><type>President</type><actionCode>E20000</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2024-12-16</actionDate><text>On passage Passed without objection.</text><type>Floor</type><actionCode>H37300</actionCode><sourceSystem><code>2</code><name>House floor actions</name></sourceSystem></item>
      <item><actionDate>2024-06-12</actionDate><text>Passed Senate without amendment by Unanimous Consent.</text><type>Floor</type><actionCode>17000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
      <item><actionDate>2024-04-19</actionDate><text>Referred to the Committee on the Judiciary.</text><type>IntroReferral</type><actionCode>2000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
    </actions>
    <sponsors><item><bioguideId>T000002</bioguideId><party>R</party><state>NC</state></item></sponsors>
    {laws}<policyArea><name>Law</name></policyArea><title>Presidential Action Test Act</title>
  </bill>
</billStatus>
"""


def archive(
    path: str = "/tmp/BILLSTATUS-117-hr.zip",
    bill_type: str = "hr",
) -> ArchiveInfo:
    return ArchiveInfo(
        bill_type=bill_type,
        path=Path(path),
        url="https://www.govinfo.gov/example.zip",
        sha256="a" * 64,
        byte_count=1,
        member_count=1,
        latest_member_timestamp="2024-01-01T00:00:00+00:00",
        pin_status="matched",
    )


class GovInfoBillCensusTests(unittest.TestCase):
    def test_v3_lifecycle_classification_and_provenance(self) -> None:
        row = parse_bill_xml(
            V3_XML.encode(),
            archive(),
            117,
            "hr",
            "BILLSTATUS-117hr42.xml",
        )

        self.assertEqual("117-hr-42", row["bill_id"])
        self.assertEqual("1", row["referred_to_committee"])
        self.assertEqual("1", row["hearing_held"])
        self.assertEqual("1", row["markup_held"])
        self.assertEqual("1", row["committee_ordered_reported"])
        self.assertEqual("1", row["committee_reported"])
        self.assertEqual("1", row["committee_advanced"])
        self.assertEqual("1", row["floor_considered"])
        self.assertEqual("1", row["passed_house"])
        self.assertEqual("1", row["passed_senate"])
        self.assertEqual("1", row["passed_origin_chamber"])
        self.assertEqual("1", row["completed_congressional_passage"])
        self.assertEqual("2021-05-25", row["completed_congressional_passage_date"])
        self.assertEqual("1", row["presented_to_president"])
        self.assertEqual("1", row["enacted"])
        self.assertEqual("Public Law", row["law_type"])
        self.assertEqual("117-1", row["law_number"])
        self.assertEqual("8", row["actions_count"])
        self.assertEqual("1", row["recorded_vote_count"])
        self.assertEqual("2021-06-01", row["latest_action_date"])
        self.assertEqual("Test Committee", row["committees"])
        self.assertEqual("T000001", row["sponsor_bioguide_id"])
        self.assertEqual(CLASSIFICATION_VERSION, row["classification_version"])
        self.assertEqual("valid", row["integrity_status"])
        self.assertEqual(64, len(row["source_xml_sha256"]))
        self.assertEqual(64, len(row["actions_sha256"]))

    def test_legacy_v1_identifiers_and_empty_containers(self) -> None:
        row = parse_bill_xml(
            V1_XML.encode(),
            archive(),
            117,
            "hr",
            "BILLSTATUS-117hr10.xml",
        )

        self.assertEqual("117-hr-10", row["bill_id"])
        self.assertEqual("Reserved for the Speaker.", row["title"])
        self.assertEqual("Unclassified", row["policy_area"])
        self.assertEqual("unknown", row["sponsor_party"])
        self.assertEqual("0", row["referred_to_committee"])
        self.assertEqual("valid", row["integrity_status"])

    def test_source_date_anomaly_is_preserved_and_labeled(self) -> None:
        xml = V3_XML.replace(
            "2021-02-01T12:00:00Z",
            "2020-12-01T12:00:00Z",
        )
        row = parse_bill_xml(
            xml.encode(),
            archive(),
            117,
            "hr",
            "BILLSTATUS-117hr42.xml",
        )

        self.assertEqual("2020-12-01", row["hearing_held_date"])
        self.assertEqual(
            "source_date_anomaly:hearing_held_date_before_introduction",
            row["integrity_status"],
        )

    def test_special_rule_and_failed_discharge_do_not_advance_bill(self) -> None:
        row = parse_bill_xml(
            SPECIAL_RULE_XML.encode(),
            archive(),
            117,
            "hr",
            "BILLSTATUS-117hr77.xml",
        )

        self.assertEqual("1", row["referred_to_committee"])
        self.assertEqual("0", row["committee_ordered_reported"])
        self.assertEqual("0", row["committee_reported"])
        self.assertEqual("0", row["committee_discharged"])
        self.assertEqual("0", row["committee_advanced"])
        self.assertEqual("0", row["floor_considered"])
        self.assertEqual("0", row["passed_house"])
        self.assertEqual("0", row["passed_origin_chamber"])
        self.assertEqual("valid", row["integrity_status"])

    def test_context_dependent_e30000_veto_is_not_enactment(self) -> None:
        row = parse_bill_xml(
            PRESIDENTIAL_ACTION_XML.format(
                presidential_text="Vetoed by President.",
                override_actions="",
                laws="<laws />",
            ).encode(),
            archive("/tmp/BILLSTATUS-118-s.zip", "s"),
            118,
            "s",
            "BILLSTATUS-118s4199.xml",
        )

        self.assertEqual("1", row["completed_congressional_passage"])
        self.assertEqual("1", row["presented_to_president"])
        self.assertEqual("1", row["vetoed"])
        self.assertEqual("action_text:presidential_veto", row["vetoed_basis"])
        self.assertEqual("0", row["veto_overridden"])
        self.assertEqual("0", row["enacted"])
        self.assertEqual("valid", row["integrity_status"])

    def test_context_dependent_e30000_signature_uses_positive_text(self) -> None:
        row = parse_bill_xml(
            PRESIDENTIAL_ACTION_XML.format(
                presidential_text="Signed by President.",
                override_actions="",
                laws="<laws />",
            ).encode(),
            archive("/tmp/BILLSTATUS-118-s.zip", "s"),
            118,
            "s",
            "BILLSTATUS-118s4199.xml",
        )

        self.assertEqual("1", row["enacted"])
        self.assertEqual("action_text:signed_by_president", row["enacted_basis"])
        self.assertEqual("0", row["vetoed"])
        self.assertEqual("0", row["veto_overridden"])
        self.assertEqual("valid", row["integrity_status"])

    def test_successful_veto_override_requires_both_chambers(self) -> None:
        override_actions = """
      <item><actionDate>2025-01-02</actionDate><text>Became Public Law No: 118-999.</text><type>BecameLaw</type><actionCode>36000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
      <item><actionDate>2025-01-01</actionDate><text>Passed Senate over veto by Yea-Nay Vote.</text><type>Veto</type><actionCode>34000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
      <item><actionDate>2024-12-30</actionDate><text>Passed House over veto by the Yeas and Nays.</text><type>Veto</type><actionCode>32000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
        """
        row = parse_bill_xml(
            PRESIDENTIAL_ACTION_XML.format(
                presidential_text="Vetoed by President.",
                override_actions=override_actions,
                laws="<laws><item><number>118-999</number><type>Public Law</type></item></laws>",
            ).encode(),
            archive("/tmp/BILLSTATUS-118-s.zip", "s"),
            118,
            "s",
            "BILLSTATUS-118s4199.xml",
        )

        self.assertEqual("1", row["vetoed"])
        self.assertEqual("1", row["veto_overridden"])
        self.assertEqual("2025-01-01", row["veto_overridden_date"])
        self.assertEqual("action_code:34000", row["veto_overridden_basis"])
        self.assertEqual("1", row["enacted"])
        self.assertEqual("valid", row["integrity_status"])

    def test_one_chamber_override_does_not_count_as_successful(self) -> None:
        house_override = """
      <item><actionDate>2024-12-30</actionDate><text>Passed House over veto by the Yeas and Nays.</text><type>Veto</type><actionCode>32000</actionCode><sourceSystem><code>9</code><name>Library of Congress</name></sourceSystem></item>
        """
        row = parse_bill_xml(
            PRESIDENTIAL_ACTION_XML.format(
                presidential_text="Vetoed by President.",
                override_actions=house_override,
                laws="<laws />",
            ).encode(),
            archive("/tmp/BILLSTATUS-118-s.zip", "s"),
            118,
            "s",
            "BILLSTATUS-118s4199.xml",
        )

        self.assertEqual("1", row["vetoed"])
        self.assertEqual("0", row["veto_overridden"])
        self.assertEqual("0", row["enacted"])
        self.assertEqual("valid", row["integrity_status"])

    def test_claim_boundary_uses_requested_congress(self) -> None:
        self.assertIn("Congress 118", claim_boundary(118))
        self.assertNotIn("117th Congress", claim_boundary(118))

    def test_action_hash_normalizes_insignificant_whitespace(self) -> None:
        row = parse_bill_xml(
            V3_XML.encode(), archive(), 117, "hr", "BILLSTATUS-117hr42.xml"
        )
        spaced = V3_XML.replace(
            "Passed Senate without amendment by Unanimous Consent.",
            "Passed   Senate without amendment by Unanimous   Consent.",
        )
        spaced_row = parse_bill_xml(
            spaced.encode(), archive(), 117, "hr", "BILLSTATUS-117hr42.xml"
        )

        self.assertNotEqual(row["source_xml_sha256"], spaced_row["source_xml_sha256"])
        self.assertEqual(row["actions_sha256"], spaced_row["actions_sha256"])

    def test_identifier_mismatch_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "filename does not match"):
            parse_bill_xml(
                V3_XML.encode(), archive(), 117, "hr", "BILLSTATUS-117hr43.xml"
            )

    def test_matching_output_cache_verifies_bytes_and_builder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "census.csv"
            metadata = root / "census.metadata.md"
            output.write_text("a,b\n1,2\n")
            output_hash = sha256_file(output)
            metadata.write_text(
                "# Metadata\n\n"
                "- configuration_sha256: `config`\n"
                "- builder_sha256: `builder`\n"
                f"- output_sha256: `{output_hash}`\n"
            )

            self.assertTrue(
                output_cache_matches(output, metadata, "config", "builder")
            )
            output.write_text("a,b\n1,3\n")
            self.assertFalse(
                output_cache_matches(output, metadata, "config", "builder")
            )

    def test_calendar_selection_excludes_upstream_committee_rate(self) -> None:
        rows: list[dict[str, str]] = []
        for seed in ("1", "2", "3"):
            rows.extend([
                {
                    "threshold": "0.670",
                    "seed": seed,
                    "runs": "1",
                    "bills": "60",
                    "defaultThreshold": "0.680",
                    "committeeAdvanceRate": "0.500000",
                    "floorConsiderationRate": "0.060000",
                    "enactmentRate": "0.030000",
                    "calendarCapacityDenialRate": "0.040000",
                    "enactedBills": "5",
                    "vetoes": "2",
                    "overriddenVetoes": "1",
                    "executiveDecisions": "6",
                    "conditionalVetoRate": "0.333333",
                    "overrideRateAmongVetoes": "0.500000",
                },
                {
                    "threshold": "0.680",
                    "seed": seed,
                    "runs": "1",
                    "bills": "60",
                    "defaultThreshold": "0.680",
                    "committeeAdvanceRate": "0.100000",
                    "floorConsiderationRate": "0.075000",
                    "enactmentRate": "0.040000",
                    "calendarCapacityDenialRate": "0.050000",
                    "enactedBills": "7",
                    "vetoes": "3",
                    "overriddenVetoes": "1",
                    "executiveDecisions": "9",
                    "conditionalVetoRate": "0.333333",
                    "overrideRateAmongVetoes": "0.333333",
                },
            ])
        targets = {
            "committeeAdvancedRate": 0.100000,
            "floorConsideredRate": 0.060000,
            "enactedRate": 0.030000,
        }

        aggregated = aggregate_lifecycle_calibration(
            rows,
            targets,
            enforce_model_default=False,
        )
        selected = next(row for row in aggregated if row["selected"] == "1")
        self.assertEqual("0.670", selected["calendarPriorityThreshold"])
        self.assertEqual("15", selected["enactedBills"])
        self.assertEqual("6", selected["vetoes"])
        self.assertEqual("0.333333", selected["conditionalVetoRate"])
        self.assertEqual(
            {"0.670": 3},
            dict(leave_one_seed_out_selections(rows, targets)),
        )

    def test_override_rate_is_undefined_without_vetoes(self) -> None:
        row = diagnostic_row(
            "GovInfo census",
            "test",
            decisions=10,
            enacted=10,
            vetoes=0,
            overrides=0,
            status="empirical_reference",
        )
        self.assertEqual("NA", row["overrideRateAmongVetoes"])
        self.assertEqual("NA", row["overrideWilson95Low"])
        self.assertEqual("NA", row["overrideWilson95High"])

    def test_temporal_transport_tolerances_are_inclusive(self) -> None:
        rows_117 = [
            {"committee_advanced": "1", "floor_considered": "1", "enacted": "1"},
            {"committee_advanced": "1", "floor_considered": "0", "enacted": "0"},
            {"committee_advanced": "0", "floor_considered": "1", "enacted": "0"},
            {"committee_advanced": "0", "floor_considered": "0", "enacted": "0"},
        ]
        rows_118 = list(rows_117)
        selected = {
            "calendarPriorityThreshold": "0.680",
            "seedCount": "50",
            "simulatedBills": "72000",
            "committeeAdvanceRate": "0.520",
            "floorConsiderationRate": "0.516",
            "enactmentRate": "0.260",
        }
        selection_summary = {
            "committeeAdvancedRate": "0.500",
            "floorConsideredRate": "0.500",
            "enactedRate": "0.250",
        }
        baselines = {
            "current-congress-committee-advance-rate": {"minimum": "0.0", "maximum": "1.0"},
            "current-congress-floor-consideration-rate": {"minimum": "0.0", "maximum": "1.0"},
            "current-congress-enactment-rate": {"minimum": "0.0", "maximum": "1.0"},
        }

        output = {
            row["metric"]: row
            for row in build_temporal_rows(
                rows_117,
                rows_118,
                selected,
                selection_summary,
                baselines,
            )
        }

        self.assertEqual("pass", output["committeeAdvanceRate"]["toleranceStatus"])
        self.assertEqual("fail", output["floorConsiderationRate"]["toleranceStatus"])
        self.assertEqual("pass", output["enactmentRate"]["toleranceStatus"])
        self.assertEqual("0.500000", output["committeeAdvanceRate"]["testRate"])
        self.assertEqual((0.0, 0.0), wilson_interval(0, 0))


if __name__ == "__main__":
    unittest.main()
