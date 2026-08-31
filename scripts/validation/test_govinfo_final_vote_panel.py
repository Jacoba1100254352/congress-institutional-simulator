#!/usr/bin/env python3
"""Regression tests for final chamber-vote selection and parsing."""

from __future__ import annotations

import unittest

try:
    from .build_govinfo_final_vote_panel import (
        RecordedVoteReference,
        SourceAction,
        approval_category,
        bill_ids_in_text,
        canonical_vote_url,
        normalize_bill_id,
        normalize_party,
        normalize_vote,
        official_bill_match_status,
        parse_house_vote,
        parse_senate_vote,
        select_approval_action,
    )
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_final_vote_panel import (
        RecordedVoteReference,
        SourceAction,
        approval_category,
        bill_ids_in_text,
        canonical_vote_url,
        normalize_bill_id,
        normalize_party,
        normalize_vote,
        official_bill_match_status,
        parse_house_vote,
        parse_senate_vote,
        select_approval_action,
    )


def action(
    *,
    index: int = 0,
    date: str = "2023-01-10",
    time: str = "12:00:00",
    text: str,
    action_type: str = "Floor",
    code: str = "",
    source_name: str,
    recorded_votes: tuple[RecordedVoteReference, ...] = (),
) -> SourceAction:
    return SourceAction(index, date, time, text, action_type, code, source_name, recorded_votes)


HOUSE_XML = b"""<?xml version="1.0"?>
<rollcall-vote>
  <vote-metadata>
    <congress>118</congress>
    <rollcall-num>123</rollcall-num>
    <legis-num>H R 1</legis-num>
    <vote-question>On Passage</vote-question>
    <vote-result>Passed</vote-result>
    <vote-type>YEA-AND-NAY</vote-type>
    <vote-totals><totals-by-vote><yea-total>2</yea-total><nay-total>1</nay-total></totals-by-vote></vote-totals>
  </vote-metadata>
  <vote-data>
    <recorded-vote><legislator party="D">One</legislator><vote>Yea</vote></recorded-vote>
    <recorded-vote><legislator party="D">Two</legislator><vote>Yea</vote></recorded-vote>
    <recorded-vote><legislator party="R">Three</legislator><vote>Nay</vote></recorded-vote>
    <recorded-vote><legislator party="I">Four</legislator><vote>Present</vote></recorded-vote>
    <recorded-vote><legislator party="R">Five</legislator><vote>Not Voting</vote></recorded-vote>
  </vote-data>
</rollcall-vote>
"""


SENATE_XML = b"""<?xml version="1.0"?>
<roll_call_vote>
  <congress>118</congress>
  <vote_number>42</vote_number>
  <vote_question_text>On Passage</vote_question_text>
  <vote_result>Bill Passed</vote_result>
  <majority_requirement>1/2</majority_requirement>
  <document><document_type>S.</document_type><document_number>2</document_number></document>
  <count><yeas>2</yeas><nays>1</nays></count>
  <members>
    <member><party>D</party><vote_cast>Yea</vote_cast></member>
    <member><party>R</party><vote_cast>Yea</vote_cast></member>
    <member><party>R</party><vote_cast>Nay</vote_cast></member>
    <member><party>I</party><vote_cast>Not Voting</vote_cast></member>
  </members>
</roll_call_vote>
"""


class GovInfoFinalVotePanelTests(unittest.TestCase):
    def test_house_final_passage_action_is_accepted(self) -> None:
        item = action(
            text="On passage Passed by the Yeas and Nays: 220 - 210.",
            code="8000",
            source_name="House floor actions",
        )
        self.assertEqual("final_passage", approval_category(item, "House"))

    def test_senate_concurrence_precedes_generic_passage_classification(self) -> None:
        item = action(
            text="Senate agreed to House amendment to S. 2 by Yea-Nay Vote.",
            code="20500",
            source_name="Senate",
        )
        self.assertEqual("concurrence", approval_category(item, "Senate"))

    def test_procedural_conference_motion_is_rejected(self) -> None:
        item = action(
            text="Motion to proceed to consideration of the conference report agreed to in Senate.",
            code="20500",
            source_name="Senate",
        )
        self.assertEqual("", approval_category(item, "Senate"))

    def test_house_reconsideration_and_procedure_orders_are_rejected(self) -> None:
        for text in (
            "On motion to reconsider Agreed to by the Yeas and Nays.",
            "Order of procedure agreed to in House without objection.",
        ):
            with self.subTest(text=text):
                item = action(text=text, code="8000", source_name="House floor actions")
                self.assertEqual("", approval_category(item, "House"))

    def test_later_nonrecorded_concurrence_is_selected_over_earlier_roll_call(self) -> None:
        reference = RecordedVoteReference("House", "118", "1", "10", "2023-01-10", "")
        initial = action(
            index=0,
            date="2023-01-10",
            text="Passed/agreed to in House: On passage Passed by the Yeas and Nays.",
            code="8000",
            source_name="House floor actions",
            recorded_votes=(reference,),
        )
        concurrence = action(
            index=1,
            date="2023-02-03",
            text="House agreed to Senate amendment without objection.",
            code="H37300",
            source_name="House floor actions",
        )
        selected, category, count = select_approval_action(
            [initial, concurrence], "House", "2023-02-04"
        )
        self.assertIs(selected, concurrence)
        self.assertEqual("concurrence", category)
        self.assertEqual(2, count)
        self.assertEqual((), selected.recorded_votes)

    def test_canonical_vote_urls_use_official_xml_patterns(self) -> None:
        house = RecordedVoteReference("House", "118", "1", "7", "2023-01-09", "ignored")
        senate = RecordedVoteReference("Senate", "118", "2", "7", "2024-01-09", "ignored")
        self.assertEqual("https://clerk.house.gov/evs/2023/roll007.xml", canonical_vote_url(house, ""))
        self.assertEqual(
            "https://www.senate.gov/legislative/LIS/roll_call_votes/vote1182/vote_118_2_00007.xml",
            canonical_vote_url(senate, ""),
        )

    def test_house_reference_preserves_clerk_archive_year_at_session_boundary(self) -> None:
        reference = RecordedVoteReference(
            "House",
            "112",
            "2",
            "659",
            "2013-01-02T04:01:15Z",
            "https://clerk.house.gov/evs/2012/roll659.xml",
        )
        self.assertEqual(
            "https://clerk.house.gov/evs/2012/roll659.xml",
            canonical_vote_url(reference, "2013-01-01"),
        )

    def test_house_vote_parser_aggregates_party_support(self) -> None:
        row = parse_house_vote(HOUSE_XML)
        self.assertEqual("118-hr-1", row["official_source_bill_id"])
        self.assertEqual("123", row["official_source_roll_number"])
        self.assertEqual("2", row["yea_count"])
        self.assertEqual("1", row["nay_count"])
        self.assertEqual("5", row["member_vote_count"])
        self.assertEqual("0.666667", row["support_share"])
        self.assertEqual("aligned", row["source_count_alignment"])

    def test_senate_vote_parser_aggregates_party_support(self) -> None:
        row = parse_senate_vote(SENATE_XML)
        self.assertEqual("118-s-2", row["official_source_bill_id"])
        self.assertEqual("42", row["official_source_roll_number"])
        self.assertEqual("1", row["democratic_yea"])
        self.assertEqual("1", row["republican_yea"])
        self.assertEqual("1", row["republican_nay"])
        self.assertEqual("aligned", row["source_count_alignment"])

    def test_normalize_bill_id_handles_all_scoped_measure_types(self) -> None:
        expected = {
            "H.R. 10": "118-hr-10",
            "S. 20": "118-s-20",
            "H.J.Res. 30": "118-hjres-30",
            "S J Res 40": "118-sjres-40",
        }
        for raw, bill_id in expected.items():
            with self.subTest(raw=raw):
                self.assertEqual(bill_id, normalize_bill_id(raw, "118"))

    def test_grouped_senate_question_matches_each_named_measure(self) -> None:
        question = "On the Joint Resolution S.J.Res. 27 and S.J.Res. 37 and S.J.Res. 48"
        self.assertEqual(
            {"116-sjres-27", "116-sjres-37", "116-sjres-48"},
            bill_ids_in_text(question, "116"),
        )
        metrics = {
            "official_source_bill_id": "116-sjres-48",
            "vote_question": question,
        }
        self.assertEqual(
            "matched_grouped_question",
            official_bill_match_status(metrics, "116-sjres-37", "116"),
        )

    def test_historical_senate_independent_and_live_pair_labels_are_normalized(self) -> None:
        self.assertEqual("I", normalize_party("ID"))
        self.assertEqual("I", normalize_party("Independent Democrat"))
        self.assertEqual("present", normalize_vote("Present, Giving Live Pair"))


if __name__ == "__main__":
    unittest.main()
