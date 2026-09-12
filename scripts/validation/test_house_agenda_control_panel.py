#!/usr/bin/env python3
"""Tests for the source-pinned House agenda-control panel."""

from __future__ import annotations

import csv
import sys
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

from build_govinfo_bill_census_dataset import Action, at, parse_actions  # noqa: E402
from build_house_agenda_control_panel import (  # noqa: E402
    CATEGORY_ORDER,
    EXPECTED_CATEGORY_COUNTS,
    NARRATIVE_CATEGORY_COUNTS,
    SurveySpec,
    classify_floor_path,
    direct_rule_link_status,
    elapsed_days,
    extract_bill_procedure,
    parse_table_1a,
    public_metadata_path,
    resolution_disposition,
)


GRANT_PATH = ROOT / "data" / "validation" / "raw" / "house_special_rule_grants.csv"
AGENDA_PATH = ROOT / "data" / "validation" / "raw" / "house_agenda_control.csv"
METADATA_PATH = ROOT / "data" / "validation" / "raw" / "house_agenda_control.metadata.md"


def action(
    text: str,
    *,
    action_date: str = "2024-01-01",
    action_type: str = "Floor",
    code: str = "",
    source_code: str = "2",
) -> Action:
    return Action(
        date=action_date,
        time="",
        text=text,
        action_type=action_type,
        code=code,
        source_code=source_code,
        source_name="House floor actions",
        recorded_votes=(),
    )


class HouseAgendaControlUnitTests(unittest.TestCase):
    def test_public_metadata_omits_machine_directories(self) -> None:
        self.assertEqual(
            "out/validation-cache/panel.zip",
            public_metadata_path(ROOT / "out/validation-cache/panel.zip"),
        )
        self.assertEqual(
            "panel.zip",
            public_metadata_path(ROOT.parent / "external-cache/panel.zip"),
        )

    def test_table_parser_handles_trailing_category_transition(self) -> None:
        source = """<html><body><pre>
A. Table 1a.--Types of Rules Granted (Consideration)
----------------------------------------------------------------
Resolution Measure Title
----------------------------------------------------------------
Modified-Open:
    H. Res. 5             H.R. 21                 First title Structured:
    H. Res. 9             H.R. 30                 A title that wraps
                                                   onto another line
Closed:
    H. Res. 10            H.J. Res. 2             Closed title
----------------------------------------------------------------
A. Table 1b.--Types of Rules Granted (Special Procedures)
</pre></body></html>"""
        spec = SurveySpec(999, "TEST", "https://example.test", "0" * 64, 0)
        rows = parse_table_1a(
            source,
            spec,
            {"open": 0, "modified_open": 1, "structured": 1, "closed": 1},
        )
        self.assertEqual(
            [row["category"] for row in rows],
            ["modified_open", "structured", "closed"],
        )
        self.assertEqual(rows[1]["title"], "A title that wraps onto another line")

    def test_parser_rejects_changed_category_counts(self) -> None:
        source = """<html><body><pre>
A. Table 1a.--Types of Rules Granted (Consideration)
Resolution Measure Title
Structured:
    H. Res. 9             H.R. 30                 One row
A. Table 1b.--Types of Rules Granted (Special Procedures)
</pre></body></html>"""
        spec = SurveySpec(999, "TEST", "https://example.test", "0" * 64, 0)
        with self.assertRaisesRegex(ValueError, "category counts changed"):
            parse_table_1a(
                source,
                spec,
                {"open": 0, "modified_open": 0, "structured": 2, "closed": 0},
            )

    def test_direct_action_parser_ignores_nested_related_bill_actions(self) -> None:
        root = ET.fromstring("""
        <billStatus><bill>
          <relatedBills><item><actions><item>
            <actionDate>2024-01-01</actionDate>
            <text>Considered under the provisions of H. Res. 999.</text>
            <type>Floor</type><actionCode>H30000</actionCode>
          </item></actions></item></relatedBills>
          <actions><item>
            <actionDate>2024-02-01</actionDate>
            <text>On motion to suspend the rules and pass, as amended, Agreed to.</text>
            <type>Floor</type><actionCode>H37310</actionCode>
            <sourceSystem><code>2</code><name>House floor actions</name></sourceSystem>
          </item></actions>
        </bill></billStatus>
        """)
        actions = parse_actions(at(root, "bill"))
        procedure = extract_bill_procedure(actions)
        self.assertEqual(procedure["suspension_path_evidence"], "1")
        self.assertEqual(procedure["direct_rule_ids"], "")
        self.assertEqual(procedure["direct_rule_action_count"], "0")

    def test_direct_rule_parser_requires_use_not_report_or_suspension_notice(self) -> None:
        procedure = extract_bill_procedure([
            action(
                "Rules Committee Resolution H. Res. 1119 Reported to House. "
                "Rule provides for consideration of H.R. 7309.",
                code="H1L210",
            ),
            action(
                "Pursuant to section 5 of H. Res. 403, the bill passed under "
                "suspension of the rules.",
                code="H37300",
            ),
            action(
                "Considered under the provisions of rule H. Res. 1119.",
                code="H30000",
            ),
        ])
        self.assertEqual(procedure["direct_rule_ids"], "hres-1119")
        self.assertEqual(procedure["direct_rule_action_count"], "1")
        self.assertIn("H. Res. 1119", procedure["direct_rule_action_basis"])

    def test_without_objection_chair_action_is_an_other_floor_path(self) -> None:
        procedure = extract_bill_procedure([
            action(
                "Without objection, the Chair laid before the House H.R. 6322 "
                "with an amendment.",
                code="H8D000",
            )
        ])
        self.assertEqual(procedure["other_floor_path_evidence"], "1")
        self.assertIn("without objection", procedure["other_floor_path_basis"].casefold())

    def test_floor_path_precedence_is_mutually_exclusive(self) -> None:
        cases = {
            (False, 2, True, True): "not_floor_considered",
            (True, 1, True, True): "mixed_special_rule_and_suspension",
            (True, 1, False, True): "adopted_special_rule",
            (True, 0, True, True): "suspension",
            (True, 0, False, True): "other_detected_floor_path",
            (True, 0, False, False): "floor_path_not_identified",
        }
        for arguments, expected in cases.items():
            with self.subTest(arguments=arguments):
                self.assertEqual(classify_floor_path(*arguments), expected)

    def test_resolution_disposition_recognizes_table_action_code(self) -> None:
        disposition = resolution_disposition(
            [action("Pursuant to H. Res. 10, H. Res. 9 is laid on the table.", code="H1B000")],
            False,
        )
        self.assertEqual(disposition[0], "tabled")

    def test_elapsed_days_preserves_stage_order_anomaly(self) -> None:
        value, anomaly = elapsed_days(
            "2024-02-01", "2024-01-01", "advance_to_floor", "118-hr-1"
        )
        self.assertEqual(value, "")
        self.assertIn("advance_to_floor_date_order", anomaly)
        self.assertEqual(elapsed_days("2024-01-01", "2024-01-11", "x", "b"), ("10", ""))

    def test_direct_rule_link_status_preserves_mismatches(self) -> None:
        self.assertEqual(
            direct_rule_link_status({"118-hres-1"}, {"118-hres-1"}),
            "direct_and_adopted_rule_links_match",
        )
        self.assertEqual(
            direct_rule_link_status({"118-hres-1"}, set()),
            "direct_rule_action_without_adopted_table1a_link",
        )


class HouseAgendaControlCommittedPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with GRANT_PATH.open(newline="") as handle:
            cls.grants = list(csv.DictReader(handle))
        with AGENDA_PATH.open(newline="") as handle:
            cls.agenda = list(csv.DictReader(handle))

    def test_primary_keys_and_row_counts(self) -> None:
        self.assertEqual(len(self.grants), 458)
        self.assertEqual(len({row["grant_id"] for row in self.grants}), 458)
        self.assertEqual(len(self.agenda), 29335)
        self.assertEqual(len({row["bill_id"] for row in self.agenda}), 29335)
        self.assertEqual(
            Counter(row["congress"] for row in self.agenda),
            Counter({"116": 9062, "117": 9709, "118": 10564}),
        )

    def test_literal_table_counts_and_narrative_discrepancy(self) -> None:
        for congress in (116, 117, 118):
            rows = [row for row in self.grants if row["congress"] == str(congress)]
            counts = Counter(row["amendment_structure"] for row in rows)
            self.assertEqual(
                {category: counts.get(category, 0) for category in CATEGORY_ORDER},
                EXPECTED_CATEGORY_COUNTS[congress],
            )
        self.assertEqual(
            EXPECTED_CATEGORY_COUNTS[117]["structured"]
            - NARRATIVE_CATEGORY_COUNTS[117]["structured"],
            -2,
        )
        self.assertEqual(
            EXPECTED_CATEGORY_COUNTS[117]["closed"]
            - NARRATIVE_CATEGORY_COUNTS[117]["closed"],
            -2,
        )
        metadata = METADATA_PATH.read_text()
        self.assertIn('"structured": -2', metadata)
        self.assertIn('"closed": -2', metadata)

    def test_every_table_hr_row_has_one_parent(self) -> None:
        agenda_ids = {row["bill_id"] for row in self.agenda}
        hr_grants = [row for row in self.grants if row["covered_measure_type"] == "hr"]
        self.assertTrue(hr_grants)
        self.assertTrue(all(row["covered_measure_id"] in agenda_ids for row in hr_grants))
        self.assertTrue(all(row["covered_measure_in_hr_census"] == "1" for row in hr_grants))

    def test_allowed_values_and_cross_field_consistency(self) -> None:
        allowed_paths = {
            "not_floor_considered",
            "adopted_special_rule",
            "suspension",
            "mixed_special_rule_and_suspension",
            "other_detected_floor_path",
            "floor_path_not_identified",
        }
        allowed_categories = set(CATEGORY_ORDER)
        self.assertTrue(all(row["amendment_structure"] in allowed_categories for row in self.grants))
        for row in self.agenda:
            self.assertIn(row["floor_path"], allowed_paths)
            if row["floor_considered"] == "0":
                self.assertEqual(row["floor_path"], "not_floor_considered")
            if row["floor_path"] == "adopted_special_rule":
                self.assertGreater(int(row["adopted_rule_count"]), 0)
                self.assertEqual(row["suspension_path_evidence"], "0")
            if row["floor_path"] == "suspension":
                self.assertEqual(row["adopted_rule_count"], "0")
                self.assertEqual(row["suspension_path_evidence"], "1")
            if int(row["direct_rule_action_count"]):
                self.assertTrue(row["direct_rule_ids"])
                self.assertTrue(row["direct_rule_action_date"])
                self.assertTrue(row["direct_rule_action_basis"])
            for field in (
                "introduction_to_referral_days",
                "referral_to_committee_advance_days",
                "committee_advance_to_floor_days",
                "introduction_to_floor_days",
            ):
                if row[field]:
                    self.assertGreaterEqual(int(row[field]), 0)

    def test_source_stage_anomalies_are_explicit(self) -> None:
        anomalies = [
            row for row in self.agenda
            if row["agenda_integrity_status"].startswith("source_stage_order_anomaly:")
        ]
        self.assertEqual(len(anomalies), 117)
        self.assertTrue(
            all(
                not row["committee_advance_to_floor_days"]
                or not row["referral_to_committee_advance_days"]
                for row in anomalies
            )
        )

    def test_all_floor_considered_rows_have_a_detected_path(self) -> None:
        self.assertFalse(
            any(
                row["floor_path"] == "floor_path_not_identified"
                for row in self.agenda
            )
        )

    def test_table1a_resolution_dispositions_reconcile(self) -> None:
        dispositions: dict[str, str] = {}
        for row in self.grants:
            prior = dispositions.setdefault(row["rule_resolution_id"], row["rule_disposition"])
            self.assertEqual(prior, row["rule_disposition"])
        by_congress = {
            congress: Counter(
                disposition
                for rule_id, disposition in dispositions.items()
                if rule_id.startswith(f"{congress}-")
            )
            for congress in (116, 117, 118)
        }
        self.assertEqual(by_congress[116], Counter({"adopted": 69}))
        self.assertEqual(by_congress[117], Counter({"adopted": 66, "tabled": 3}))
        self.assertEqual(
            by_congress[118],
            Counter({"adopted": 56, "adopted_amended": 4, "rejected": 6, "tabled": 1}),
        )


if __name__ == "__main__":
    unittest.main()
