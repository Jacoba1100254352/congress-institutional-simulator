#!/usr/bin/env python3
"""Regression tests for district bill-topic support aggregation."""

from __future__ import annotations

import csv
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build_district_public_opinion_bill_topic_support_dataset as target


def task(year: str = "2012") -> target.EstimateTask:
    return target.EstimateTask(
        bill_id="117-hr-8404",
        public_law_number="117-228",
        policy_area="Civil Rights and Liberties, Minority Issues",
        bill_title="Respect for Marriage Act",
        district_id="NY-10",
        state_fips="36",
        district_number="10",
        variable_id="gaymarriage_legalize",
        item_label="Support for legalizing gay marriage",
        support_codes=frozenset({"1"}),
        oppose_codes=frozenset({"2"}),
        alignment_direction="survey_support_directionally_consistent_with_bill",
        alignment_strength="close_issue_construct_historical_not_exact_bill_question",
        year=year,
    )


def source(year: str = "2012") -> target.AnnualSource:
    return target.AnnualSource(
        year=year,
        congress="113",
        dataset_doi="example",
        dataset_version="1.0",
        dataset_release_time="2026-01-01T00:00:00Z",
        dataset_license="CC0 1.0",
        file_id="1",
        file_label="annual.tab",
        file_md5="abc",
        access_file_size_bytes=100,
        access_file_sha256="def",
        case_id_field="V101",
        state_field="state",
        district_field="district",
    )


def item_source(year: str = "2012") -> target.AnnualItemSource:
    return target.AnnualItemSource(
        year=year,
        variable_id="gaymarriage_legalize",
        question_field="question",
        question_wave="pre_election",
        weight_field="weight",
        weight_selection_status="official_validated_voter_pre_election_weight",
        guide_file_id="2",
        guide_file_label="guide.pdf",
        guide_file_md5="ghi",
        guide_printed_page="1",
    )


class DistrictBillTopicSupportTests(unittest.TestCase):
    def test_normalization_preserves_identifiers_without_float_rounding(self) -> None:
        self.assertEqual("123456789", target.normalize_case_id("123456789.0"))
        self.assertEqual("123456789", target.normalize_case_id("123456789"))
        self.assertEqual("36", target.normalize_integer("36.000"))
        self.assertEqual(("36", "10"), target.parse_district_id("NY-10"))

    def test_cumulative_reader_counts_years_and_nonmissing_responses(self) -> None:
        source_text = io.StringIO(
            "year\tcase_id\tgaymarriage_legalize\n"
            "2012\t100.0\t1\n"
            "2012\t200\t2.0\n"
            "2012\t300\t\n"
            "2016\t400\t1\n"
            "2014\t500\t2\n"
        )

        responses, row_counts, nonmissing = target.read_cumulative_responses(
            source_text, [task("2012"), task("2016")]
        )

        self.assertEqual({"2012": 3, "2016": 1}, row_counts)
        self.assertEqual(2, nonmissing[("2012", "gaymarriage_legalize")])
        self.assertEqual(1, nonmissing[("2016", "gaymarriage_legalize")])
        self.assertEqual("1", responses[("2012", "gaymarriage_legalize")]["100"])
        self.assertEqual("2", responses[("2012", "gaymarriage_legalize")]["200"])
        self.assertEqual("", responses[("2012", "gaymarriage_legalize")]["300"])

    def test_annual_join_and_weighted_estimate(self) -> None:
        estimate_task = task()
        responses = {
            ("2012", "gaymarriage_legalize"): {
                "100": "1",
                "200": "2",
                "300": "",
                "500": "1",
            }
        }
        annual_text = io.StringIO(
            "V101\tweight\tstate\tdistrict\tquestion\n"
            "100\t2\t36\t10\t1\n"
            "200.0\t1\t36.0\t10.0\t2\n"
            "300\t3\t36\t10\t\n"
            "400\t4\t36\t10\t\n"
            "500\t5\t36\t11\t1\n"
        )

        source_rows, accumulators, validated = target.aggregate_annual_source(
            annual_text,
            source(),
            [estimate_task],
            responses,
            {estimate_task: item_source()},
        )
        accumulator = accumulators[estimate_task]

        self.assertEqual(5, source_rows)
        self.assertEqual(4, accumulator.district_source_rows)
        self.assertEqual(3, accumulator.joined_rows)
        self.assertEqual(2, accumulator.response_respondents)
        self.assertEqual(1, accumulator.support_respondents)
        self.assertEqual(1, accumulator.oppose_respondents)
        self.assertAlmostEqual(2.0, accumulator.weighted_support)
        self.assertAlmostEqual(3.0, accumulator.sum_weights)
        self.assertAlmostEqual(5.0, accumulator.sum_squared_weights)
        self.assertEqual(3, validated[estimate_task])

        row = target.build_output_row(
            estimate_task,
            source(),
            item_source(),
            accumulator,
            cross_source_validated_responses=3,
            annual_source_rows=source_rows,
            cumulative_source_rows=3,
            cumulative_nonmissing=2,
            minimum_respondents=2,
        )
        self.assertEqual("0.500000", row["unweighted_support_share"])
        self.assertEqual("0.666667", row["weighted_support_share"])
        self.assertEqual("1.800000", row["effective_sample_size"])
        self.assertIn("no_case_ids_written", row["privacy_status"])

    def test_invalid_weight_is_excluded_from_weighted_denominator(self) -> None:
        estimate_task = task()
        responses = {
            ("2012", "gaymarriage_legalize"): {"100": "1", "200": "2"}
        }
        annual_text = io.StringIO(
            "V101\tweight\tstate\tdistrict\tquestion\n"
            "100\tnan\t36\t10\t1\n"
            "200\t2\t36\t10\t2\n"
        )

        _, accumulators, _ = target.aggregate_annual_source(
            annual_text,
            source(),
            [estimate_task],
            responses,
            {estimate_task: item_source()},
        )
        accumulator = accumulators[estimate_task]

        self.assertEqual(1, accumulator.invalid_weight_respondents)
        self.assertEqual(2, accumulator.response_respondents)
        self.assertAlmostEqual(2.0, accumulator.sum_weights)
        self.assertAlmostEqual(0.0, accumulator.weighted_support)

    def test_small_cell_suppresses_counts_and_estimates(self) -> None:
        estimate_task = task()
        accumulator = target.EstimateAccumulator(
            district_source_rows=2,
            joined_rows=2,
            response_respondents=2,
            support_respondents=1,
            oppose_respondents=1,
            weighted_support=1.0,
            sum_weights=2.0,
            sum_squared_weights=2.0,
        )

        row = target.build_output_row(
            estimate_task,
            source(),
            item_source(),
            accumulator,
            cross_source_validated_responses=2,
            annual_source_rows=2,
            cumulative_source_rows=2,
            cumulative_nonmissing=2,
            minimum_respondents=3,
        )

        self.assertEqual(
            "historical_district_issue_estimate_suppressed_below_threshold",
            row["estimate_status"],
        )
        for field in (
            "published_response_respondents",
            "published_support_respondents",
            "published_oppose_respondents",
            "weighted_support_share",
            "unweighted_support_share",
            "effective_sample_size",
        ):
            self.assertEqual("", row[field])

    def test_annual_question_must_match_cumulative_response(self) -> None:
        estimate_task = task()
        responses = {
            ("2012", "gaymarriage_legalize"): {"100": "1"}
        }
        annual_text = io.StringIO(
            "V101\tweight\tstate\tdistrict\tquestion\n"
            "100\t1\t36\t10\t2\n"
        )

        with self.assertRaisesRegex(SystemExit, "does not match cumulative"):
            target.aggregate_annual_source(
                annual_text,
                source(),
                [estimate_task],
                responses,
                {estimate_task: item_source()},
            )

    def test_download_stream_verifies_the_bytes_consumed_by_parser(self) -> None:
        payload = b"case_id\tvalue\n1\t2\n"
        expected_sha256 = hashlib.sha256(payload).hexdigest()
        with mock.patch.object(
            target.urllib.request,
            "urlopen",
            return_value=io.BytesIO(payload),
        ):
            with target.open_data_stream(
                "https://example.test/source.tab",
                len(payload),
                expected_sha256,
                "source.tab",
            ) as handle:
                self.assertEqual(1, len(list(csv.DictReader(handle, delimiter="\t"))))

        with mock.patch.object(
            target.urllib.request,
            "urlopen",
            return_value=io.BytesIO(payload),
        ):
            with self.assertRaisesRegex(SystemExit, "source byte drift"):
                with target.open_data_stream(
                    "https://example.test/source.tab",
                    len(payload),
                    "0" * 64,
                    "source.tab",
                ) as handle:
                    list(csv.DictReader(handle, delimiter="\t"))

    def test_matching_aggregate_cache_is_reused(self) -> None:
        estimate_task = task()
        annual_source = target.ANNUAL_SOURCES["2012"]
        accumulator = target.EstimateAccumulator(
            district_source_rows=40,
            joined_rows=40,
            response_respondents=40,
            support_respondents=30,
            oppose_respondents=10,
            weighted_support=30.0,
            sum_weights=40.0,
            sum_squared_weights=40.0,
        )
        row = target.build_output_row(
            estimate_task,
            annual_source,
            target.item_source_for(estimate_task),
            accumulator,
            cross_source_validated_responses=90,
            annual_source_rows=100,
            cumulative_source_rows=100,
            cumulative_nonmissing=90,
            minimum_respondents=30,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            original_output = target.OUT_CSV
            target.OUT_CSV = Path(temp_dir) / "support.csv"
            try:
                with target.OUT_CSV.open("w", newline="") as handle:
                    writer = csv.DictWriter(
                        handle,
                        fieldnames=target.FIELDNAMES,
                        lineterminator="\n",
                    )
                    writer.writeheader()
                    writer.writerow(row)
                self.assertTrue(target.existing_output_matches([estimate_task], 30))
                self.assertFalse(target.existing_output_matches([estimate_task], 31))
            finally:
                target.OUT_CSV = original_output


if __name__ == "__main__":
    unittest.main()
