#!/usr/bin/env python3
"""Regression tests for the official bill-text context cache."""

from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

import build_district_public_opinion_bill_text_context_dataset as target


def packet() -> dict[str, str]:
    return {
        "packet_rank": "1",
        "readiness_rank": "2",
        "bill_id": "117-hr-8404",
        "public_law_number": "117-228",
        "policy_area": "Civil Rights and Liberties, Minority Issues",
        "sponsor_districts": "NY-10",
    }


def bill_xml() -> bytes:
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<billStatus>
  <titles>
    <item><titleType>Display Title</titleType><title>Respect for Marriage Act</title></item>
    <item><titleType>Official Title as Introduced</titleType><title>An Act</title></item>
    <item><titleType>Short Title as Enacted</titleType><title>RFMA</title></item>
  </titles>
  <legislativeSubjects>
    <item><name>Marriage and family status</name></item>
    <item><name>Civil rights and liberties</name></item>
  </legislativeSubjects>
  <summaries>
    <summary>
      <versionCode>00</versionCode><actionDate>2022-07-19</actionDate>
      <actionDesc>Introduced in House</actionDesc><updateDate>2022-07-20T00:00:00Z</updateDate>
      <text>&lt;p&gt;Earlier summary.&lt;/p&gt;</text>
    </summary>
    <summary>
      <versionCode>49</versionCode><actionDate>2022-12-13</actionDate>
      <actionDesc>Public Law</actionDesc><updateDate>2022-12-14T00:00:00Z</updateDate>
      <text>&lt;p&gt;Latest &amp;amp; final summary.&lt;/p&gt;</text>
    </summary>
  </summaries>
</billStatus>
"""


class BillTextContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_output = target.OUT_CSV
        target.OUT_CSV = Path(self.temp_dir.name) / "bill-context.csv"

    def tearDown(self) -> None:
        target.OUT_CSV = self.original_output
        self.temp_dir.cleanup()

    def write_rows(self, rows: list[dict[str, str]]) -> None:
        with target.OUT_CSV.open("w", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=target.FIELDNAMES,
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)

    def test_build_row_uses_latest_summary_and_normalizes_markup(self) -> None:
        source = bill_xml()
        row = target.build_row(packet(), source, target.govinfo_url("117-hr-8404"))

        self.assertEqual("Respect for Marriage Act", row["display_title"])
        self.assertEqual("Latest & final summary.", row["latest_summary_text"])
        self.assertEqual("2", row["summary_count"])
        self.assertEqual(
            "Civil rights and liberties; Marriage and family status",
            row["legislative_subjects"],
        )
        self.assertEqual(hashlib.sha256(source).hexdigest(), row["govinfo_billstatus_sha256"])

    def test_matching_cache_is_reused_and_input_drift_is_rejected(self) -> None:
        source = bill_xml()
        row = target.build_row(packet(), source, target.govinfo_url("117-hr-8404"))
        self.write_rows([row])

        self.assertTrue(target.existing_output_matches([packet()]))

        changed_packet = {**packet(), "sponsor_districts": "NY-11"}
        self.assertFalse(target.existing_output_matches([changed_packet]))

        row["govinfo_billstatus_sha256"] = "not-a-hash"
        self.write_rows([row])
        self.assertFalse(target.existing_output_matches([packet()]))


if __name__ == "__main__":
    unittest.main()
