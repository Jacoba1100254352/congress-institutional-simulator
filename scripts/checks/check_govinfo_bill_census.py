#!/usr/bin/env python3
"""Verify the GovInfo bill census and lifecycle calibration artifacts."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/govinfo_bill_census.csv")
METADATA = Path("data/validation/raw/govinfo_bill_census.metadata.md")
RAW_116 = Path("data/validation/raw/govinfo_bill_census_116.csv")
METADATA_116 = Path("data/validation/raw/govinfo_bill_census_116.metadata.md")
RAW_118 = Path("data/validation/raw/govinfo_bill_census_118.csv")
METADATA_118 = Path("data/validation/raw/govinfo_bill_census_118.metadata.md")
BUILDER = Path("scripts/validation/build_govinfo_bill_census_dataset.py")
SUMMARY = Path("reports/govinfo-bill-census.csv")
SUMMARY_MD = Path("reports/govinfo-bill-census.md")
SUMMARY_116 = Path("reports/govinfo-bill-census-116.csv")
SUMMARY_116_MD = Path("reports/govinfo-bill-census-116.md")
SUMMARY_118 = Path("reports/govinfo-bill-census-118.csv")
SUMMARY_118_MD = Path("reports/govinfo-bill-census-118.md")
LIFECYCLE_CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
LIFECYCLE_CALIBRATION_MD = Path("reports/legislative-lifecycle-calibration.md")
TEMPORAL_REPLICATION = Path("reports/legislative-lifecycle-temporal-replication.csv")
TEMPORAL_REPLICATION_MD = Path("reports/legislative-lifecycle-temporal-replication.md")
EXECUTIVE_DIAGNOSTIC = Path("reports/legislative-executive-action-diagnostic.csv")
EXECUTIVE_DIAGNOSTIC_MD = Path("reports/legislative-executive-action-diagnostic.md")
EXECUTIVE_PANEL = Path("data/validation/raw/govinfo_executive_action_panel.csv")
EXECUTIVE_PANEL_METADATA = Path("data/validation/raw/govinfo_executive_action_panel.metadata.md")
EXECUTIVE_PANEL_BUILDER = Path("scripts/validation/build_govinfo_executive_action_panel.py")
EXECUTIVE_CONTEXT = Path("data/validation/reference/congress_executive_context.csv")
EXECUTIVE_VETO_REFERENCE = Path("data/validation/reference/senate_veto_reference_108_118.csv")
JOINT_PANEL = Path("data/validation/raw/govinfo_joint_resolution_panel.csv")
JOINT_PANEL_METADATA = Path("data/validation/raw/govinfo_joint_resolution_panel.metadata.md")
JOINT_VETO_REFERENCE = Path(
    "data/validation/reference/senate_joint_resolution_veto_reference_108_118.csv"
)
FINAL_VOTE_PANEL = Path("data/validation/raw/govinfo_final_chamber_vote_panel.csv")
FINAL_VOTE_PANEL_METADATA = Path(
    "data/validation/raw/govinfo_final_chamber_vote_panel.metadata.md"
)
FINAL_VOTE_PANEL_BUILDER = Path("scripts/validation/build_govinfo_final_vote_panel.py")
CALIBRATION_BASELINE = Path("reports/calibration-baseline.csv")
HELDOUT = Path("reports/empirical-flow-heldout.csv")

EXPECTED_ARCHIVES = {
    "BILLSTATUS-117-hr.zip": {
        "rows": 9709,
        "sha256": "658b2d280e4e7972c86bfd810ebff0c9bb61c115b242de8c8774034dea08de03",
    },
    "BILLSTATUS-117-s.zip": {
        "rows": 5357,
        "sha256": "69561f19333de31afd2e288700757f3794ecffa35287b9fb86bb2d5d313a1294",
    },
}
EXPECTED_ARCHIVES_116 = {
    "BILLSTATUS-116-hr.zip": {
        "rows": 9062,
        "sha256": "b3775e79914a9db29b3a8d55ae13638020c44822dcecb9e4517371e093d01dde",
    },
    "BILLSTATUS-116-s.zip": {
        "rows": 5086,
        "sha256": "e876253f4e3c8b58b28278c8e6e3b901eff0c336b74dfc6e90834d9d3af98132",
    },
}
EXPECTED_STAGE_COUNTS_116 = {
    "referredCount": 14086,
    "hearingCount": 676,
    "markupCount": 1297,
    "orderedReportedCount": 1264,
    "reportedCount": 1035,
    "dischargedCount": 540,
    "committeeAdvancedCount": 1488,
    "floorConsideredCount": 1048,
    "originPassageCount": 1039,
    "completedCongressionalPassageCount": 334,
    "presentedCount": 334,
    "vetoedCount": 2,
    "vetoOverriddenCount": 1,
    "enactedCount": 333,
}
EXPECTED_STAGE_COUNTS = {
    "referredCount": 14959,
    "hearingCount": 790,
    "markupCount": 1347,
    "orderedReportedCount": 1347,
    "reportedCount": 967,
    "dischargedCount": 573,
    "committeeAdvancedCount": 1511,
    "floorConsideredCount": 1003,
    "originPassageCount": 991,
    "completedCongressionalPassageCount": 358,
    "presentedCount": 358,
    "vetoedCount": 0,
    "vetoOverriddenCount": 0,
    "enactedCount": 358,
}
EXPECTED_ARCHIVES_118 = {
    "BILLSTATUS-118-hr.zip": {
        "rows": 10564,
        "sha256": "8e7ca7dab50a7b9b977f021ec1b3231f8fedf82c33494553857b892fadfdba98",
    },
    "BILLSTATUS-118-s.zip": {
        "rows": 5649,
        "sha256": "269261c0989db3ced789680ee2202747df9a7298f1ac8d2b074d3356b06e399c",
    },
}
EXPECTED_STAGE_COUNTS_118 = {
    "referredCount": 16155,
    "hearingCount": 664,
    "markupCount": 1683,
    "orderedReportedCount": 1677,
    "reportedCount": 1426,
    "dischargedCount": 510,
    "committeeAdvancedCount": 1843,
    "floorConsideredCount": 957,
    "originPassageCount": 935,
    "completedCongressionalPassageCount": 270,
    "presentedCount": 270,
    "vetoedCount": 1,
    "vetoOverriddenCount": 0,
    "enactedCount": 269,
}
EXPECTED_EXECUTIVE_DECISIONS = {
    "108": 476,
    "109": 466,
    "110": 449,
    "111": 367,
    "112": 272,
    "113": 282,
    "114": 330,
    "115": 417,
    "116": 334,
    "117": 358,
    "118": 270,
}
EXPECTED_EXECUTIVE_VETOES = {
    "109-hr-810",
    "110-hr-976",
    "110-hr-1495",
    "110-hr-1585",
    "110-hr-1591",
    "110-hr-2082",
    "110-hr-2419",
    "110-hr-3043",
    "110-hr-3963",
    "110-hr-6124",
    "110-hr-6331",
    "110-s-5",
    "111-hr-3808",
    "114-hr-1735",
    "114-hr-1777",
    "114-hr-3762",
    "114-s-1",
    "114-s-2040",
    "116-hr-6395",
    "116-s-906",
    "118-s-4199",
}
EXPECTED_EXECUTIVE_OVERRIDES = {
    "110-hr-1495",
    "110-hr-2419",
    "110-hr-6124",
    "110-hr-6331",
    "114-s-2040",
    "116-hr-6395",
}
EXPECTED_JOINT_EXECUTIVE_DECISIONS = {
    "108": 28,
    "109": 18,
    "110": 18,
    "111": 20,
    "112": 12,
    "113": 14,
    "114": 8,
    "115": 26,
    "116": 19,
    "117": 7,
    "118": 17,
}
EXPECTED_JOINT_VETOES = {
    "111-hjres-64",
    "114-hjres-88",
    "114-sjres-8",
    "114-sjres-22",
    "114-sjres-23",
    "114-sjres-24",
    "116-hjres-46",
    "116-hjres-76",
    "116-sjres-7",
    "116-sjres-36",
    "116-sjres-37",
    "116-sjres-38",
    "116-sjres-54",
    "116-sjres-68",
    "118-hjres-27",
    "118-hjres-30",
    "118-hjres-39",
    "118-hjres-42",
    "118-hjres-45",
    "118-hjres-98",
    "118-hjres-109",
    "118-sjres-9",
    "118-sjres-11",
    "118-sjres-24",
    "118-sjres-32",
    "118-sjres-38",
}
EXPECTED_SOURCE_LAW_NUMBER_ANOMALIES = {
    "109-hr-5441",
    "110-hr-6124",
    "110-s-2499",
}
EXPECTED_116_SOURCE_DATE_ANOMALIES = {
    "116-hr-2665",
    "116-hr-2779",
    "116-hr-3432",
    "116-hr-3630",
    "116-hr-3631",
    "116-hr-4618",
    "116-hr-4650",
    "116-hr-4665",
    "116-hr-4671",
    "116-hr-4995",
    "116-hr-4996",
    "116-hr-4997",
    "116-hr-5000",
    "116-hr-5035",
    "116-hr-5552",
    "116-s-1790",
    "116-s-2470",
    "116-s-2520",
    "116-s-2524",
    "116-s-2581",
    "116-s-2582",
    "116-s-2583",
    "116-s-2584",
    "116-s-4897",
}
EXPECTED_116_NONIDENTICAL_VERSION_BILLS = {
    "116-hr-550",
    "116-hr-925",
    "116-hr-1044",
    "116-hr-2486",
    "116-hr-2610",
    "116-hr-4764",
    "116-hr-6172",
    "116-s-178",
    "116-s-1811",
}
EXPECTED_118_SOURCE_DATE_ANOMALIES = {
    "118-hr-4821",
    "118-hr-6185",
    "118-hr-6544",
    "118-hr-8771",
    "118-hr-8772",
    "118-hr-9026",
    "118-hr-9027",
    "118-hr-9686",
    "118-hr-9711",
    "118-hr-9714",
    "118-hr-9716",
    "118-hr-9751",
    "118-s-2226",
    "118-s-2605",
    "118-s-4678",
    "118-s-4690",
    "118-s-4795",
    "118-s-4797",
    "118-s-4802",
    "118-s-4875",
}
EXPECTED_118_NONIDENTICAL_VERSION_BILLS = {
    "118-s-1146",
    "118-s-1258",
    "118-s-2073",
}
HASH = re.compile(r"[0-9a-f]{64}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_values(path: Path) -> dict[str, str]:
    require(path.exists(), f"Missing required artifact: {path}")
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            values[key] = value.strip().strip("`")
    return values


def truthy(row: dict[str, str], field: str) -> bool:
    return row.get(field) == "1"


def check_raw_116() -> list[dict[str, str]]:
    rows = read_csv(RAW_116)
    metadata = metadata_values(METADATA_116)
    require(len(rows) == 14148, f"Expected 14148 116th census rows; found {len(rows)}")
    require(len({row["bill_id"] for row in rows}) == len(rows), "116th census bill IDs are not unique")
    require(sum(int(row["actions_count"]) for row in rows) == 68345, "116th census action count drifted")
    require(Counter(row["bill_type"] for row in rows) == Counter({"hr": 9062, "s": 5086}), "116th bill-type counts drifted")
    require(
        Counter(row["source_archive"] for row in rows)
        == Counter({name: data["rows"] for name, data in EXPECTED_ARCHIVES_116.items()}),
        "116th archive row counts drifted",
    )
    require(
        Counter(row["law_type"] for row in rows if row["law_type"])
        == Counter({"Public Law": 333}),
        "116th law-type counts drifted",
    )

    statuses = Counter(row["integrity_status"].split(":", 1)[0] for row in rows)
    require(statuses == Counter({"valid": 14124, "source_date_anomaly": 24}), f"116th integrity statuses drifted: {statuses}")
    anomalies = {
        row["bill_id"]
        for row in rows
        if row["integrity_status"].startswith("source_date_anomaly:")
    }
    require(anomalies == EXPECTED_116_SOURCE_DATE_ANOMALIES, "116th source-date anomaly set drifted")
    require(not any(row["integrity_status"].startswith("invalid:") for row in rows), "116th census contains invalid lifecycle rows")
    require(all(HASH.fullmatch(row["source_xml_sha256"]) for row in rows), "Invalid 116th source XML hash")
    require(all(HASH.fullmatch(row["actions_sha256"]) for row in rows), "Invalid 116th canonical action hash")
    require(
        all(row["source_url"].startswith("https://www.govinfo.gov/bulkdata/BILLSTATUS/116/") for row in rows),
        "Unexpected 116th census source URL",
    )
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v3" for row in rows), "116th classification version drifted")

    for row in rows:
        expected_advance = any(
            truthy(row, field)
            for field in ("committee_ordered_reported", "committee_reported", "committee_discharged")
        )
        require(truthy(row, "committee_advanced") == expected_advance, f"116th committee-advance union mismatch for {row['bill_id']}")
        if truthy(row, "completed_congressional_passage"):
            require(truthy(row, "passed_house") and truthy(row, "passed_senate"), f"116th completed-passage chamber mismatch for {row['bill_id']}")
        if truthy(row, "enacted"):
            require(truthy(row, "presented_to_president"), f"116th enacted row lacks presentment: {row['bill_id']}")
        if truthy(row, "veto_overridden"):
            require(truthy(row, "vetoed") and truthy(row, "enacted"), f"116th override invariant failed: {row['bill_id']}")
        if truthy(row, "vetoed") and truthy(row, "enacted"):
            require(truthy(row, "veto_overridden"), f"116th vetoed enactment lacks override: {row['bill_id']}")

    by_bill = {row["bill_id"]: row for row in rows}
    require({row["bill_id"] for row in rows if truthy(row, "vetoed")} == {"116-hr-6395", "116-s-906"}, "116th veto set drifted")
    require({row["bill_id"] for row in rows if truthy(row, "veto_overridden")} == {"116-hr-6395"}, "116th override set drifted")
    require(by_bill["116-hr-6395"]["veto_overridden_date"] == "2021-01-01", "116-hr-6395 override date drifted")
    require(by_bill["116-hr-6395"]["law_number"] == "116-283", "116-hr-6395 law number drifted")
    presented_not_enacted = {
        row["bill_id"]
        for row in rows
        if truthy(row, "presented_to_president") and not truthy(row, "enacted")
    }
    require(presented_not_enacted == {"116-s-906"}, "116th presented/non-enacted set drifted")
    nonidentical_versions = {
        row["bill_id"]
        for row in rows
        if truthy(row, "passed_house")
        and truthy(row, "passed_senate")
        and not truthy(row, "completed_congressional_passage")
    }
    require(nonidentical_versions == EXPECTED_116_NONIDENTICAL_VERSION_BILLS, "116th nonidentical-version set drifted")

    expected_metadata = {
        "rows": "14148",
        "parsed_action_records": "68345",
        "enacted_rows": "333",
        "public_law_rows": "333",
        "private_law_rows": "0",
        "integrity_valid_rows": "14124",
        "source_date_anomaly_rows": "24",
        "classification_version": "govinfo-bill-lifecycle-v3",
    }
    for key, expected in expected_metadata.items():
        require(metadata.get(key) == expected, f"116th metadata {key} drifted")
    require(metadata.get("builder_sha256") == sha256_file(BUILDER), "116th metadata builder hash does not match current builder")
    require(metadata.get("output_sha256") == sha256_file(RAW_116), "116th metadata output hash does not match census bytes")
    metadata_text = METADATA_116.read_text()
    for archive in EXPECTED_ARCHIVES_116.values():
        require(archive["sha256"] in metadata_text, "Pinned 116th archive hash missing from metadata")
    return rows


def check_raw() -> list[dict[str, str]]:
    rows = read_csv(RAW)
    metadata = metadata_values(METADATA)
    require(len(rows) == 15066, f"Expected 15066 census rows; found {len(rows)}")
    require(len({row["bill_id"] for row in rows}) == len(rows), "Census bill IDs are not unique")
    require(sum(int(row["actions_count"]) for row in rows) == 72047, "Census action count drifted")
    require(Counter(row["bill_type"] for row in rows) == Counter({"hr": 9709, "s": 5357}), "Bill-type counts drifted")
    require(
        Counter(row["source_archive"] for row in rows)
        == Counter({name: data["rows"] for name, data in EXPECTED_ARCHIVES.items()}),
        "Archive row counts drifted",
    )
    require(
        Counter(row["law_type"] for row in rows if row["law_type"])
        == Counter({"Public Law": 355, "Private Law": 3}),
        "Law-type counts drifted",
    )

    statuses = Counter(row["integrity_status"].split(":", 1)[0] for row in rows)
    require(statuses == Counter({"valid": 15061, "source_date_anomaly": 5}), f"Integrity statuses drifted: {statuses}")
    require(not any(row["integrity_status"].startswith("invalid:") for row in rows), "Census contains invalid lifecycle rows")
    require(all(HASH.fullmatch(row["source_xml_sha256"]) for row in rows), "Invalid source XML hash")
    require(all(HASH.fullmatch(row["actions_sha256"]) for row in rows), "Invalid canonical action hash")
    require(
        all(row["source_url"].startswith("https://www.govinfo.gov/bulkdata/BILLSTATUS/117/") for row in rows),
        "Unexpected census source URL",
    )
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v3" for row in rows), "Classification version drifted")

    for row in rows:
        expected_advance = any(
            truthy(row, field)
            for field in ("committee_ordered_reported", "committee_reported", "committee_discharged")
        )
        require(truthy(row, "committee_advanced") == expected_advance, f"Committee-advance union mismatch for {row['bill_id']}")
        if truthy(row, "completed_congressional_passage"):
            require(truthy(row, "passed_house") and truthy(row, "passed_senate"), f"Completed-passage chamber mismatch for {row['bill_id']}")
            require(truthy(row, "enacted"), f"Non-enacted completed-passage row in 117th H.R./S. scope: {row['bill_id']}")
        if truthy(row, "enacted"):
            require(truthy(row, "presented_to_president"), f"Enacted row lacks presentment: {row['bill_id']}")
        require(not truthy(row, "veto_overridden"), f"Unexpected 117th override: {row['bill_id']}")

    require(metadata.get("rows") == "15066", "Metadata row count drifted")
    require(metadata.get("parsed_action_records") == "72047", "Metadata action count drifted")
    require(metadata.get("enacted_rows") == "358", "Metadata enacted count drifted")
    require(metadata.get("public_law_rows") == "355", "Metadata public-law count drifted")
    require(metadata.get("private_law_rows") == "3", "Metadata private-law count drifted")
    require(metadata.get("integrity_valid_rows") == "15061", "Metadata valid-row count drifted")
    require(metadata.get("source_date_anomaly_rows") == "5", "Metadata anomaly count drifted")
    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v3", "Metadata classifier version drifted")
    require(metadata.get("builder_sha256") == sha256_file(BUILDER), "Metadata builder hash does not match the current builder")
    require(metadata.get("output_sha256") == sha256_file(RAW), "Metadata output hash does not match census bytes")
    metadata_text = METADATA.read_text()
    for archive in EXPECTED_ARCHIVES.values():
        require(archive["sha256"] in metadata_text, "Pinned archive hash missing from metadata")
    return rows


def check_raw_118() -> list[dict[str, str]]:
    rows = read_csv(RAW_118)
    metadata = metadata_values(METADATA_118)
    require(len(rows) == 16213, f"Expected 16213 118th census rows; found {len(rows)}")
    require(len({row["bill_id"] for row in rows}) == len(rows), "118th census bill IDs are not unique")
    require(sum(int(row["actions_count"]) for row in rows) == 75239, "118th census action count drifted")
    require(Counter(row["bill_type"] for row in rows) == Counter({"hr": 10564, "s": 5649}), "118th bill-type counts drifted")
    require(
        Counter(row["source_archive"] for row in rows)
        == Counter({name: data["rows"] for name, data in EXPECTED_ARCHIVES_118.items()}),
        "118th archive row counts drifted",
    )
    require(
        Counter(row["law_type"] for row in rows if row["law_type"])
        == Counter({"Public Law": 269}),
        "118th law-type counts drifted",
    )

    statuses = Counter(row["integrity_status"].split(":", 1)[0] for row in rows)
    require(statuses == Counter({"valid": 16193, "source_date_anomaly": 20}), f"118th integrity statuses drifted: {statuses}")
    anomalies = {
        row["bill_id"]
        for row in rows
        if row["integrity_status"].startswith("source_date_anomaly:")
    }
    require(anomalies == EXPECTED_118_SOURCE_DATE_ANOMALIES, "118th source-date anomaly set drifted")
    require(not any(row["integrity_status"].startswith("invalid:") for row in rows), "118th census contains invalid lifecycle rows")
    require(all(HASH.fullmatch(row["source_xml_sha256"]) for row in rows), "Invalid 118th source XML hash")
    require(all(HASH.fullmatch(row["actions_sha256"]) for row in rows), "Invalid 118th canonical action hash")
    require(
        all(row["source_url"].startswith("https://www.govinfo.gov/bulkdata/BILLSTATUS/118/") for row in rows),
        "Unexpected 118th census source URL",
    )
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v3" for row in rows), "118th classification version drifted")

    for row in rows:
        expected_advance = any(
            truthy(row, field)
            for field in ("committee_ordered_reported", "committee_reported", "committee_discharged")
        )
        require(truthy(row, "committee_advanced") == expected_advance, f"118th committee-advance union mismatch for {row['bill_id']}")
        if truthy(row, "completed_congressional_passage"):
            require(truthy(row, "passed_house") and truthy(row, "passed_senate"), f"118th completed-passage chamber mismatch for {row['bill_id']}")
        if truthy(row, "enacted"):
            require(truthy(row, "presented_to_president"), f"118th enacted row lacks presentment: {row['bill_id']}")
        require(not truthy(row, "veto_overridden"), f"Unexpected 118th override: {row['bill_id']}")

    vetoed = [row for row in rows if truthy(row, "vetoed")]
    require([row["bill_id"] for row in vetoed] == ["118-s-4199"], "118th veto set drifted")
    require(not truthy(vetoed[0], "enacted"), "118-s-4199 is incorrectly enacted")
    require(vetoed[0]["vetoed_basis"] == "action_text:presidential_veto", "118-s-4199 veto basis drifted")
    presented_not_enacted = {
        row["bill_id"]
        for row in rows
        if truthy(row, "presented_to_president") and not truthy(row, "enacted")
    }
    require(presented_not_enacted == {"118-s-4199"}, "118th presented/non-enacted set drifted")
    nonidentical_versions = {
        row["bill_id"]
        for row in rows
        if truthy(row, "passed_house")
        and truthy(row, "passed_senate")
        and not truthy(row, "completed_congressional_passage")
    }
    require(nonidentical_versions == EXPECTED_118_NONIDENTICAL_VERSION_BILLS, "118th nonidentical-version set drifted")

    expected_metadata = {
        "rows": "16213",
        "parsed_action_records": "75239",
        "enacted_rows": "269",
        "public_law_rows": "269",
        "private_law_rows": "0",
        "integrity_valid_rows": "16193",
        "source_date_anomaly_rows": "20",
        "classification_version": "govinfo-bill-lifecycle-v3",
    }
    for key, expected in expected_metadata.items():
        require(metadata.get(key) == expected, f"118th metadata {key} drifted")
    require(metadata.get("builder_sha256") == sha256_file(BUILDER), "118th metadata builder hash does not match current builder")
    require(metadata.get("output_sha256") == sha256_file(RAW_118), "118th metadata output hash does not match census bytes")
    metadata_text = METADATA_118.read_text()
    require("Congress 118" in metadata_text and "117th Congress" not in metadata_text, "118th claim boundary is not Congress-specific")
    for archive in EXPECTED_ARCHIVES_118.values():
        require(archive["sha256"] in metadata_text, "Pinned 118th archive hash missing from metadata")
    return rows


def check_summary(rows: list[dict[str, str]]) -> None:
    summary_rows = read_csv(SUMMARY)
    overall = next((row for row in summary_rows if row["groupType"] == "all"), None)
    calibration = next((row for row in summary_rows if row["groupType"] == "split" and row["groupValue"] == "calibration"), None)
    heldout = next((row for row in summary_rows if row["groupType"] == "split" and row["groupValue"] == "heldout"), None)
    require(overall is not None and calibration is not None and heldout is not None, "Census summary is missing all/calibration/heldout rows")
    require(int(overall["billCount"]) == len(rows), "Summary bill count drifted")
    require(int(overall["actionCount"]) == 72047, "Summary action count drifted")
    require(int(calibration["billCount"]) == 7564 and int(heldout["billCount"]) == 7502, "Summary split counts drifted")
    for field, expected in EXPECTED_STAGE_COUNTS.items():
        require(int(overall[field]) == expected, f"Summary {field} drifted")

    text = SUMMARY_MD.read_text()
    require("40 overlap the census by bill ID" in text, "117th public-law cross-check count drifted")
    require("180 retain GovInfo identifier matches" in text, "118th bounded identifier cross-check drifted")
    require("within-Congress stability check, not a temporal" in text, "Census split boundary is missing")
    require("complete 116th and 118th censuses supply separate no-refit temporal backcast and forecast checks" in text, "117th report does not point to both temporal replications")


def check_summary_116(rows: list[dict[str, str]]) -> None:
    summary_rows = read_csv(SUMMARY_116)
    require(len(summary_rows) == 3, f"Expected three 116th summary rows; found {len(summary_rows)}")
    overall = next((row for row in summary_rows if row["groupType"] == "all"), None)
    require(overall is not None, "116th census summary lacks the all row")
    require(int(overall["billCount"]) == len(rows), "116th summary bill count drifted")
    require(int(overall["actionCount"]) == 68345, "116th summary action count drifted")
    for field, expected in EXPECTED_STAGE_COUNTS_116.items():
        require(int(overall[field]) == expected, f"116th summary {field} drifted")

    text = SUMMARY_116_MD.read_text()
    require("complete, provenance-pinned" in text, "116th completeness statement is missing")
    require("`116-hr-6395` was vetoed, overridden by both chambers" in text, "116th override audit is missing")
    require("`116-s-906` was vetoed without a successful override" in text, "116th sustained-veto audit is missing")
    require("No 116th-Congress record participates in threshold selection" in text, "116th no-refit boundary is missing")
    require("24 preserved source-date anomalies" in text, "116th anomaly disclosure is missing")


def check_summary_118(rows: list[dict[str, str]]) -> None:
    summary_rows = read_csv(SUMMARY_118)
    require(len(summary_rows) == 3, f"Expected three 118th summary rows; found {len(summary_rows)}")
    overall = next((row for row in summary_rows if row["groupType"] == "all"), None)
    require(overall is not None, "118th census summary lacks the all row")
    require(int(overall["billCount"]) == len(rows), "118th summary bill count drifted")
    require(int(overall["actionCount"]) == 75239, "118th summary action count drifted")
    for field, expected in EXPECTED_STAGE_COUNTS_118.items():
        require(int(overall[field]) == expected, f"118th summary {field} drifted")

    text = SUMMARY_118_MD.read_text()
    require("complete, provenance-pinned" in text, "118th completeness statement is missing")
    require("`118-s-4199` completed passage and was presented, then vetoed" in text, "118th veto audit is missing")
    require("No 118th-Congress bill satisfies it" in text, "118th zero-override audit is missing")
    require("No 118th-Congress record participates in threshold selection" in text, "118th no-refit boundary is missing")
    require("20 preserved source-date anomalies" in text, "118th anomaly disclosure is missing")


def check_temporal_replication() -> None:
    rows = read_csv(TEMPORAL_REPLICATION)
    require(len(rows) == 6, f"Expected six temporal transport rows; found {len(rows)}")
    by_metric = {(row["testCongress"], row["metric"]): row for row in rows}
    expected = {
        ("116", "committeeAdvanceRate"): ("1488", "14148", "0.105174", "0.001104", "0.020000", "pass"),
        ("116", "floorConsiderationRate"): ("1048", "14148", "0.074074", "-0.012977", "0.015000", "pass"),
        ("116", "enactmentRate"): ("333", "14148", "0.023537", "0.003880", "0.010000", "pass"),
        ("118", "committeeAdvanceRate"): ("1843", "16213", "0.113674", "-0.007396", "0.020000", "pass"),
        ("118", "floorConsiderationRate"): ("957", "16213", "0.059027", "0.002070", "0.015000", "pass"),
        ("118", "enactmentRate"): ("269", "16213", "0.016592", "0.010825", "0.010000", "fail"),
    }
    require(set(by_metric) == set(expected), "Temporal transport metric set drifted")
    for key, (count, bills, test_rate, error, tolerance, status) in expected.items():
        row = by_metric[key]
        congress, metric = key
        require(row["selectionCongress"] == "117" and row["testCongress"] == congress, f"Temporal Congress labels drifted for {key}")
        require(row["frozenThreshold"] == "0.680", f"Frozen threshold drifted for {key}")
        require(row["seedCount"] == "50" and row["simulatedBills"] == "72000", f"Frozen panel drifted for {key}")
        require(row["testCount"] == count and row["testBills"] == bills, f"Temporal count drifted for {key}")
        require(row["testRate"] == test_rate, f"Temporal test rate drifted for {key}")
        require(row["transportError"] == error, f"Temporal error drifted for {key}")
        require(row["prespecifiedTolerance"] == tolerance, f"Temporal tolerance drifted for {key}")
        require(row["toleranceStatus"] == status, f"Temporal tolerance result drifted for {key}")
        require(row["testRateInBaselineRange"] == "pass", f"Temporal broad-range result drifted for {key}")
        require(float(row["testWilson95Low"]) < float(row["testRate"]) < float(row["testWilson95High"]), f"Temporal Wilson interval does not contain rate for {key}")

    text = TEMPORAL_REPLICATION_MD.read_text()
    require("passes all 3 of 3 backcast tolerances" in text, "116th temporal pass summary drifted")
    require("2 of 3 forecast tolerances" in text, "118th temporal pass summary drifted")
    require("5 of 6 external cohort-metric cells overall" in text, "Combined temporal summary drifted")
    require("exceeds its tolerance by 0.000825" in text, "Temporal enactment miss disclosure drifted")
    require("No 116th or 118th rate is read by the calibration selector" in text, "Temporal no-refit protocol is missing")
    require("Both classifier revisions are source corrections, not post-hoc parameter changes" in text, "Classifier correction boundary is missing")


def check_executive_panel() -> None:
    rows = read_csv(EXECUTIVE_PANEL)
    metadata = metadata_values(EXECUTIVE_PANEL_METADATA)
    require(len(rows) == 4021, f"Expected 4021 executive decisions; found {len(rows)}")
    require(len({row["bill_id"] for row in rows}) == len(rows), "Executive panel bill IDs are not unique")
    require(
        Counter(row["congress"] for row in rows) == Counter(EXPECTED_EXECUTIVE_DECISIONS),
        "Executive panel Congress counts drifted",
    )
    require(
        {row["classification_version"] for row in rows} == {"govinfo-bill-lifecycle-v3"},
        "Executive panel classifier version drifted",
    )
    require(
        not any(row["integrity_status"].startswith("invalid:") for row in rows),
        "Executive panel contains invalid lifecycle rows",
    )
    require(
        all(len(row["source_xml_sha256"]) == 64 and len(row["actions_sha256"]) == 64 for row in rows),
        "Executive panel source hashes are incomplete",
    )
    require(
        all(row["executive_decision_date"] for row in rows),
        "Executive panel contains an undated final decision",
    )
    require(
        {row["bill_id"] for row in rows if truthy(row, "vetoed")} == EXPECTED_EXECUTIVE_VETOES,
        "Executive panel veto set drifted",
    )
    require(
        {row["bill_id"] for row in rows if truthy(row, "veto_overridden")}
        == EXPECTED_EXECUTIVE_OVERRIDES,
        "Executive panel override set drifted",
    )
    require(
        {row["bill_id"] for row in rows if row["source_law_number_status"] == "source_cross_congress_number"}
        == EXPECTED_SOURCE_LAW_NUMBER_ANOMALIES,
        "Executive panel source-law-number anomaly set drifted",
    )
    require(
        Counter(row["source_law_number_status"] for row in rows)
        == Counter({"aligned": 4003, "not_enacted": 15, "source_cross_congress_number": 3}),
        "Executive panel source-law-number status counts drifted",
    )
    require(
        Counter(row["government_control"] for row in rows)
        == Counter({"unified": 2084, "divided": 1937}),
        "Executive panel government-control strata drifted",
    )
    require(
        Counter(row["sponsor_same_party_as_president"] for row in rows)
        == Counter({"1": 2217, "0": 1790, "NA": 14}),
        "Executive panel sponsor-party strata drifted",
    )
    for congress, expected_count in EXPECTED_EXECUTIVE_DECISIONS.items():
        cohort = [row for row in rows if row["congress"] == congress]
        enacted = sum(truthy(row, "enacted") for row in cohort)
        vetoes = sum(truthy(row, "vetoed") for row in cohort)
        overrides = sum(truthy(row, "veto_overridden") for row in cohort)
        require(len(cohort) == expected_count, f"Congress {congress} decision count drifted")
        require(
            len(cohort) == enacted + vetoes - overrides,
            f"Congress {congress} executive-decision identity failed",
        )

    reference = {row["bill_id"]: row for row in read_csv(EXECUTIVE_VETO_REFERENCE)}
    require(set(reference) == EXPECTED_EXECUTIVE_VETOES, "Official Senate veto reference set drifted")
    by_bill = {row["bill_id"]: row for row in rows}
    for bill_id, expected in reference.items():
        observed = by_bill[bill_id]
        require(observed["president"] == expected["president"], f"{bill_id} president reference drifted")
        require(observed["vetoed_date"] == expected["veto_date"], f"{bill_id} veto-date reference drifted")
        require(
            observed["veto_overridden"] == expected["veto_overridden"],
            f"{bill_id} override reference drifted",
        )
        require(
            observed["veto_kind_reference"] == expected["veto_kind"],
            f"{bill_id} veto-kind reference drifted",
        )

    context = {row["congress"]: row for row in read_csv(EXECUTIVE_CONTEXT)}
    require(set(context) == set(EXPECTED_EXECUTIVE_DECISIONS), "Executive context Congress set drifted")
    for row in rows:
        expected = context[row["congress"]]
        for field in (
            "president",
            "president_party",
            "house_majority_party",
            "senate_majority_party",
            "government_control",
        ):
            require(row[field] == expected[field], f"{row['bill_id']} {field} context drifted")

    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v3", "Panel metadata classifier drifted")
    require(metadata.get("parsed_bill_records") == "126760", "Panel parsed-bill count drifted")
    require(metadata.get("executive_decisions") == "4021", "Panel decision count metadata drifted")
    require(metadata.get("vetoed_rows") == "21", "Panel veto count metadata drifted")
    require(metadata.get("overridden_veto_rows") == "6", "Panel override count metadata drifted")
    require(metadata.get("output_sha256") == sha256_file(EXECUTIVE_PANEL), "Panel output hash metadata drifted")
    require(
        metadata.get("panel_builder_sha256") == sha256_file(EXECUTIVE_PANEL_BUILDER),
        "Panel builder hash metadata drifted",
    )
    require(metadata.get("lifecycle_builder_sha256") == sha256_file(BUILDER), "Panel lifecycle-builder hash drifted")
    require(metadata.get("context_sha256") == sha256_file(EXECUTIVE_CONTEXT), "Panel context hash drifted")
    require(
        metadata.get("veto_reference_sha256") == sha256_file(EXECUTIVE_VETO_REFERENCE),
        "Panel veto-reference hash drifted",
    )
    metadata_text = EXECUTIVE_PANEL_METADATA.read_text()
    require("unconfigured" not in metadata_text, "Panel metadata retains unpinned archives")
    require("changed_explicitly_allowed" not in metadata_text, "Panel metadata accepts changed archives")
    require(
        metadata_text.count("| matched | https://www.govinfo.gov/bulkdata/BILLSTATUS/") == 22,
        "Panel metadata does not record 22 matched archive pins",
    )
    require(
        "The exact 21-measure veto set" in metadata_text,
        "Panel official-veto-reference audit is missing",
    )


def check_joint_resolution_panel() -> None:
    rows = read_csv(JOINT_PANEL)
    metadata = metadata_values(JOINT_PANEL_METADATA)
    require(len(rows) == 187, f"Expected 187 joint-resolution decisions; found {len(rows)}")
    require(len({row["bill_id"] for row in rows}) == len(rows), "Joint-resolution panel bill IDs are not unique")
    require(
        Counter(row["congress"] for row in rows) == Counter(EXPECTED_JOINT_EXECUTIVE_DECISIONS),
        "Joint-resolution panel Congress counts drifted",
    )
    require(
        Counter(row["bill_type"] for row in rows) == Counter({"hjres": 123, "sjres": 64}),
        "Joint-resolution type counts drifted",
    )
    require(
        {row["classification_version"] for row in rows} == {"govinfo-bill-lifecycle-v3"},
        "Joint-resolution classifier version drifted",
    )
    require(
        Counter(row["integrity_status"].split(":", 1)[0] for row in rows)
        == Counter({"valid": 186, "source_date_anomaly": 1}),
        "Joint-resolution lifecycle status counts drifted",
    )
    require(
        {
            row["bill_id"]
            for row in rows
            if row["integrity_status"].startswith("source_date_anomaly:")
        }
        == {"109-hjres-47"},
        "Joint-resolution source-date anomaly set drifted",
    )
    require(
        not any(row["integrity_status"].startswith("invalid:") for row in rows),
        "Joint-resolution panel contains an invalid lifecycle row",
    )
    require(
        {row["bill_id"] for row in rows if truthy(row, "vetoed")} == EXPECTED_JOINT_VETOES,
        "Joint-resolution veto set drifted",
    )
    require(not any(truthy(row, "veto_overridden") for row in rows), "Unexpected joint-resolution override")
    require(
        Counter(row["source_law_number_status"] for row in rows)
        == Counter({"aligned": 161, "not_enacted": 26}),
        "Joint-resolution source-law-number status counts drifted",
    )
    require(
        {row["bill_id"] for row in rows if row["veto_date_alignment"] == "source_date_discrepancy"}
        == {"114-sjres-22"},
        "Joint-resolution source-date discrepancy set drifted",
    )
    by_bill = {row["bill_id"]: row for row in rows}
    discrepancy = by_bill["114-sjres-22"]
    require(discrepancy["veto_date_reference"] == "2016-01-19", "S.J.Res. 22 reference veto date drifted")
    require(discrepancy["vetoed_date"] == "2016-01-20", "S.J.Res. 22 GovInfo veto date drifted")

    for congress, expected_count in EXPECTED_JOINT_EXECUTIVE_DECISIONS.items():
        cohort = [row for row in rows if row["congress"] == congress]
        enacted = sum(truthy(row, "enacted") for row in cohort)
        vetoes = sum(truthy(row, "vetoed") for row in cohort)
        overrides = sum(truthy(row, "veto_overridden") for row in cohort)
        require(len(cohort) == expected_count, f"Congress {congress} joint decision count drifted")
        require(
            len(cohort) == enacted + vetoes - overrides,
            f"Congress {congress} joint executive-decision identity failed",
        )

    reference = {row["bill_id"]: row for row in read_csv(JOINT_VETO_REFERENCE)}
    require(set(reference) == EXPECTED_JOINT_VETOES, "Official joint-resolution veto reference set drifted")
    require(
        Counter(row["veto_date_alignment"] for row in reference.values())
        == Counter({"aligned": 25, "source_date_discrepancy": 1}),
        "Joint-resolution reference date-alignment counts drifted",
    )
    require(
        {row["veto_overridden"] for row in reference.values()} == {"0"},
        "Joint-resolution reference contains an override",
    )
    for bill_id, expected in reference.items():
        observed = by_bill[bill_id]
        require(observed["president"] == expected["president"], f"{bill_id} president reference drifted")
        require(
            observed["veto_date_reference"] == expected["veto_date"],
            f"{bill_id} reference veto date drifted",
        )
        require(
            observed["veto_date_alignment"] == expected["veto_date_alignment"],
            f"{bill_id} veto-date alignment drifted",
        )
        require(
            observed["veto_kind_reference"] == expected["veto_kind"],
            f"{bill_id} veto-kind reference drifted",
        )

    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v3", "Joint panel classifier metadata drifted")
    require(metadata.get("parsed_bill_records") == "2031", "Joint panel parsed-bill count drifted")
    require(metadata.get("executive_decisions") == "187", "Joint panel decision count metadata drifted")
    require(metadata.get("enacted_rows") == "161", "Joint panel enactment count metadata drifted")
    require(metadata.get("vetoed_rows") == "26", "Joint panel veto count metadata drifted")
    require(metadata.get("overridden_veto_rows") == "0", "Joint panel override count metadata drifted")
    require(metadata.get("source_date_discrepancy_rows") == "1", "Joint panel date-discrepancy metadata drifted")
    require(metadata.get("output_sha256") == sha256_file(JOINT_PANEL), "Joint panel output hash metadata drifted")
    require(
        metadata.get("panel_builder_sha256") == sha256_file(EXECUTIVE_PANEL_BUILDER),
        "Joint panel builder hash metadata drifted",
    )
    require(metadata.get("lifecycle_builder_sha256") == sha256_file(BUILDER), "Joint panel lifecycle-builder hash drifted")
    require(metadata.get("context_sha256") == sha256_file(EXECUTIVE_CONTEXT), "Joint panel context hash drifted")
    require(
        metadata.get("veto_reference_sha256") == sha256_file(JOINT_VETO_REFERENCE),
        "Joint panel veto-reference hash drifted",
    )
    metadata_text = JOINT_PANEL_METADATA.read_text()
    require("unconfigured" not in metadata_text, "Joint panel metadata retains unpinned archives")
    require("changed_explicitly_allowed" not in metadata_text, "Joint panel metadata accepts changed archives")
    require(
        metadata_text.count("| matched | https://www.govinfo.gov/bulkdata/BILLSTATUS/") == 22,
        "Joint panel metadata does not record 22 matched archive pins",
    )
    require("The exact 26-measure veto set" in metadata_text, "Joint panel veto-reference audit is missing")


def check_final_vote_panel() -> None:
    rows = read_csv(FINAL_VOTE_PANEL)
    metadata = metadata_values(FINAL_VOTE_PANEL_METADATA)
    decisions = read_csv(EXECUTIVE_PANEL) + read_csv(JOINT_PANEL)
    decision_by_bill = {row["bill_id"]: row for row in decisions}
    require(len(decision_by_bill) == 4208, "Combined presidential-decision population drifted")
    require(len(rows) == 8416, f"Expected 8416 final chamber-vote rows; found {len(rows)}")

    by_bill: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_bill.setdefault(row["bill_id"], []).append(row)
    require(set(by_bill) == set(decision_by_bill), "Final-vote panel measure population drifted")
    for bill_id, cohort in by_bill.items():
        require(len(cohort) == 2, f"{bill_id} does not have exactly two chamber rows")
        require({row["chamber"] for row in cohort} == {"House", "Senate"}, f"{bill_id} chamber pair drifted")

    require(
        Counter((row["chamber"], row["selection_status"]) for row in rows)
        == Counter(
            {
                ("House", "official_roll_call_selected"): 1333,
                ("House", "final_approval_without_recorded_vote"): 2875,
                ("Senate", "official_roll_call_selected"): 352,
                ("Senate", "final_approval_without_recorded_vote"): 3856,
            }
        ),
        "Final-vote chamber coverage drifted",
    )
    require(
        Counter((row["measure_class"], row["selection_status"]) for row in rows)
        == Counter(
            {
                ("bill", "official_roll_call_selected"): 1526,
                ("bill", "final_approval_without_recorded_vote"): 6516,
                ("joint_resolution", "official_roll_call_selected"): 159,
                ("joint_resolution", "final_approval_without_recorded_vote"): 215,
            }
        ),
        "Final-vote measure-class coverage drifted",
    )
    require(
        Counter((row["chamber"], row["selection_category"]) for row in rows)
        == Counter(
            {
                ("House", "final_passage"): 3671,
                ("House", "concurrence"): 427,
                ("House", "conference_report"): 110,
                ("Senate", "final_passage"): 3889,
                ("Senate", "concurrence"): 209,
                ("Senate", "conference_report"): 110,
            }
        ),
        "Final-vote approval-category counts drifted",
    )
    require(
        Counter(row["integrity_status"] for row in rows)
        == Counter({"valid_official_roll_call": 1685, "valid_no_recorded_final_approval_vote": 6731}),
        "Final-vote integrity statuses drifted",
    )
    require(
        Counter(row["official_source_bill_match_status"] for row in rows)
        == Counter({"matched": 1684, "matched_grouped_question": 1, "": 6731}),
        "Final-vote official bill-match statuses drifted",
    )
    grouped = [row for row in rows if row["official_source_bill_match_status"] == "matched_grouped_question"]
    require(
        len(grouped) == 1
        and grouped[0]["bill_id"] == "116-sjres-37"
        and grouped[0]["chamber"] == "Senate"
        and grouped[0]["official_source_bill_id"] == "116-sjres-48"
        and "S.J.Res. 37" in grouped[0]["vote_question"],
        "Grouped Senate joint-resolution vote audit drifted",
    )

    official_urls: set[str] = set()
    for row in rows:
        decision = decision_by_bill[row["bill_id"]]
        for field in (
            "congress",
            "bill_type",
            "president",
            "president_party",
            "government_control",
            "executive_outcome",
            "vetoed",
            "enacted",
        ):
            require(row[field] == decision[field], f"{row['bill_id']} {field} decision linkage drifted")
        require(
            row["decision_source_xml_sha256"] == decision["source_xml_sha256"]
            and row["decision_actions_sha256"] == decision["actions_sha256"],
            f"{row['bill_id']} decision source hashes drifted",
        )
        require(row["action_date"] <= decision["presented_to_president_date"], f"{row['bill_id']} final vote follows presentment")
        require(row["classification_version"] == "govinfo-bill-lifecycle-v3", f"{row['bill_id']} lifecycle version drifted")
        require(row["selection_classifier_version"] == "govinfo-final-chamber-vote-v1", f"{row['bill_id']} selector version drifted")

        if row["selection_status"] == "final_approval_without_recorded_vote":
            require(
                row["official_source_status"] == "not_applicable_no_recorded_vote",
                f"{row['bill_id']} nonrecorded source status drifted",
            )
            require(
                not any(
                    row[field]
                    for field in (
                        "roll_number",
                        "session_number",
                        "source_url",
                        "official_source_sha256",
                        "yea_count",
                        "nay_count",
                        "support_share",
                    )
                ),
                f"{row['bill_id']} nonrecorded approval contains roll-call metrics",
            )
            continue

        require(row["source_url"] not in official_urls, f"Official roll call reused: {row['source_url']}")
        official_urls.add(row["source_url"])
        require(HASH.fullmatch(row["official_source_sha256"]) is not None, f"{row['bill_id']} official source hash is invalid")
        require(row["source_count_alignment"] == "aligned", f"{row['bill_id']} official source counts differ")
        expected_source_status = (
            "official_house_clerk_xml" if row["chamber"] == "House" else "official_senate_lis_xml"
        )
        require(row["official_source_status"] == expected_source_status, f"{row['bill_id']} official source status drifted")
        expected_prefix = (
            "https://clerk.house.gov/evs/"
            if row["chamber"] == "House"
            else "https://www.senate.gov/legislative/LIS/roll_call_votes/"
        )
        require(row["source_url"].startswith(expected_prefix), f"{row['bill_id']} official source URL drifted")

        yea = int(row["yea_count"])
        nay = int(row["nay_count"])
        present = int(row["present_count"])
        not_voting = int(row["not_voting_count"])
        require(yea + nay == int(row["participating_count"]), f"{row['bill_id']} participating count drifted")
        require(
            yea + nay + present + not_voting == int(row["member_vote_count"]),
            f"{row['bill_id']} member-vote count drifted",
        )
        require(
            sum(int(row[field]) for field in ("democratic_yea", "republican_yea", "independent_yea")) == yea,
            f"{row['bill_id']} party yea counts drifted",
        )
        require(
            sum(int(row[field]) for field in ("democratic_nay", "republican_nay", "independent_nay")) == nay,
            f"{row['bill_id']} party nay counts drifted",
        )
        require(row["support_share"] == f"{yea / (yea + nay):.6f}", f"{row['bill_id']} support share drifted")
        president_prefix = "democratic" if row["president_party"] == "D" else "republican"
        opposition_prefix = "republican" if row["president_party"] == "D" else "democratic"
        for target, source in (("president_party", president_prefix), ("opposition_party", opposition_prefix)):
            target_yea = int(row[f"{target}_yea"])
            target_nay = int(row[f"{target}_nay"])
            require(target_yea == int(row[f"{source}_yea"]), f"{row['bill_id']} {target} yea count drifted")
            require(target_nay == int(row[f"{source}_nay"]), f"{row['bill_id']} {target} nay count drifted")
            expected_share = f"{target_yea / (target_yea + target_nay):.6f}" if target_yea + target_nay else ""
            require(row[f"{target}_support_share"] == expected_share, f"{row['bill_id']} {target} share drifted")

    require(len(official_urls) == 1685, "Final-vote unique official-source count drifted")
    require(
        sum(
            all(row["selection_status"] == "official_roll_call_selected" for row in cohort)
            for cohort in by_bill.values()
        )
        == 310,
        "Measures with two recorded final votes drifted",
    )

    expected_metadata = {
        "selection_classifier_version": "govinfo-final-chamber-vote-v1",
        "lifecycle_classification_version": "govinfo-bill-lifecycle-v3",
        "presented_measures": "4208",
        "chamber_rows": "8416",
        "official_roll_call_rows": "1685",
        "nonrecorded_final_approval_rows": "6731",
        "measures_with_both_final_roll_calls": "310",
        "unique_official_vote_sources": "1685",
    }
    for key, expected in expected_metadata.items():
        require(metadata.get(key) == expected, f"Final-vote metadata {key} drifted")
    require(metadata.get("builder_sha256") == sha256_file(FINAL_VOTE_PANEL_BUILDER), "Final-vote builder hash drifted")
    require(metadata.get("lifecycle_builder_sha256") == sha256_file(BUILDER), "Final-vote lifecycle-builder hash drifted")
    require(metadata.get("output_sha256") == sha256_file(FINAL_VOTE_PANEL), "Final-vote output hash drifted")
    decision_panel_hash = hashlib.sha256(
        "|".join(sha256_file(path) for path in (EXECUTIVE_PANEL, JOINT_PANEL)).encode()
    ).hexdigest()
    require(metadata.get("decision_panel_sha256") == decision_panel_hash, "Final-vote decision-panel hash drifted")
    metadata_text = FINAL_VOTE_PANEL_METADATA.read_text()
    require("Earlier roll calls are not substituted" in metadata_text, "Final-vote non-imputation rule is missing")
    require("post-passage descriptive context" in metadata_text, "Final-vote claim boundary is missing")
    require("matched_grouped_question" in metadata_text, "Final-vote grouped-question audit is missing")


def check_executive_diagnostic() -> None:
    rows = read_csv(EXECUTIVE_DIAGNOSTIC)
    require(len(rows) == 32, f"Expected 32 executive-action rows; found {len(rows)}")
    by_cohort = {row["cohort"]: row for row in rows}
    expected = {
        "108": ("bill", "congress", 476, 0, 0, "0.000000", "empirical_reference_bill_congress"),
        "109": ("bill", "congress", 466, 1, 0, "0.002146", "empirical_reference_bill_congress"),
        "110": ("bill", "congress", 449, 11, 4, "0.024499", "empirical_reference_bill_congress"),
        "111": ("bill", "congress", 367, 1, 0, "0.002725", "empirical_reference_bill_congress"),
        "112": ("bill", "congress", 272, 0, 0, "0.000000", "empirical_reference_bill_congress"),
        "113": ("bill", "congress", 282, 0, 0, "0.000000", "empirical_reference_bill_congress"),
        "114": ("bill", "congress", 330, 5, 1, "0.015152", "empirical_reference_bill_congress"),
        "115": ("bill", "congress", 417, 0, 0, "0.000000", "empirical_reference_bill_congress"),
        "116": ("bill", "congress", 334, 2, 1, "0.005988", "empirical_reference_bill_congress"),
        "117": ("bill", "congress", 358, 0, 0, "0.000000", "empirical_reference_bill_congress"),
        "118": ("bill", "congress", 270, 1, 0, "0.003704", "empirical_reference_bill_congress"),
        "George W. Bush": ("bill", "administration", 1391, 12, 4, "0.008627", "descriptive_bill_stratum"),
        "Barack Obama": ("bill", "administration", 1251, 6, 1, "0.004796", "descriptive_bill_stratum"),
        "Donald J. Trump": ("bill", "administration", 751, 2, 1, "0.002663", "descriptive_bill_stratum"),
        "Joseph R. Biden Jr.": ("bill", "administration", 628, 1, 0, "0.001592", "descriptive_bill_stratum"),
        "unified": ("bill", "government_control", 2084, 2, 0, "0.000960", "descriptive_bill_stratum"),
        "divided": ("bill", "government_control", 1937, 19, 6, "0.009809", "descriptive_bill_stratum"),
        "same-party sponsor": ("bill", "sponsor_party", 2217, 1, 0, "0.000451", "descriptive_bill_stratum"),
        "opposition-party sponsor": ("bill", "sponsor_party", 1790, 20, 6, "0.011173", "descriptive_bill_stratum"),
        "other/unknown sponsor": ("bill", "sponsor_party", 14, 0, 0, "0.000000", "descriptive_bill_stratum"),
        "108-118 H.R./S. bills": ("bill", "measure_class", 4021, 21, 6, "0.005223", "empirical_reference_bill_class"),
        "108-118 joint resolutions": ("joint_resolution", "measure_class", 187, 26, 0, "0.139037", "empirical_reference_joint_resolution_class"),
        "108-118 all presented measures": ("all_presented_measures", "pooled", 4208, 47, 6, "0.011169", "empirical_reference_combined"),
        "both final roll calls": ("all_presented_measures", "final_vote_coverage", 310, 40, 4, "0.129032", "descriptive_final_vote_coverage"),
        "House final roll only": ("all_presented_measures", "final_vote_coverage", 1023, 3, 1, "0.002933", "descriptive_final_vote_coverage"),
        "Senate final roll only": ("all_presented_measures", "final_vote_coverage", 42, 0, 0, "0.000000", "descriptive_final_vote_coverage"),
        "no final roll calls": ("all_presented_measures", "final_vote_coverage", 2833, 4, 1, "0.001412", "descriptive_final_vote_coverage"),
        "both chambers at least two-thirds": ("all_presented_measures", "both_recorded_minimum_support", 165, 5, 4, "0.030303", "descriptive_both_recorded_support_stratum"),
        "one or both chambers below two-thirds": ("all_presented_measures", "both_recorded_minimum_support", 145, 35, 0, "0.241379", "descriptive_both_recorded_support_stratum"),
        "opposition majority in both chambers": ("all_presented_measures", "both_recorded_opposition_support", 199, 40, 4, "0.201005", "descriptive_both_recorded_opposition_support_stratum"),
        "opposition below majority in one or both chambers": ("all_presented_measures", "both_recorded_opposition_support", 111, 0, 0, "0.000000", "descriptive_both_recorded_opposition_support_stratum"),
        "117-selected 50-seed panel": ("undifferentiated_simulator_measures", "simulator", 2621, 647, 0, "0.246852", "large_descriptive_mismatch_no_prespecified_tolerance"),
    }
    require(set(by_cohort) == set(expected), "Executive-action cohort set drifted")
    for cohort, values in expected.items():
        measure_class, group_type, decisions, vetoes, overrides, veto_rate, status = values
        row = by_cohort[cohort]
        require(row["measureClass"] == measure_class, f"Executive diagnostic {cohort} measure class drifted")
        require(row["groupType"] == group_type, f"Executive diagnostic {cohort} group type drifted")
        require(row["decisionCount"] == str(decisions), f"Executive diagnostic {cohort} decisions drifted")
        require(row["enactedBills"] == str(decisions - vetoes + overrides), f"Executive diagnostic {cohort} enactments drifted")
        require(row["nonVetoEnactments"] == str(decisions - vetoes), f"Executive diagnostic {cohort} non-veto enactments drifted")
        require(row["vetoes"] == str(vetoes), f"Executive diagnostic {cohort} vetoes drifted")
        require(row["overriddenVetoes"] == str(overrides), f"Executive diagnostic {cohort} overrides drifted")
        require(row["conditionalVetoRate"] == veto_rate, f"Executive diagnostic {cohort} veto rate drifted")
        expected_override_rate = "NA" if vetoes == 0 else f"{overrides / vetoes:.6f}"
        require(
            row["overrideRateAmongVetoes"] == expected_override_rate,
            f"Executive diagnostic {cohort} override rate drifted",
        )
        require(row["diagnosticStatus"] == status, f"Executive diagnostic {cohort} status drifted")
        require(
            int(row["decisionCount"])
            == int(row["enactedBills"]) + int(row["vetoes"]) - int(row["overriddenVetoes"]),
            f"Executive-decision identity failed for {cohort}",
        )
    simulator = by_cohort["117-selected 50-seed panel"]
    pooled = by_cohort["108-118 all presented measures"]
    require(simulator["conditionalVetoRateDifferenceFromPooledEmpirical"] == "0.235683", "Veto-rate difference drifted")
    require(simulator["conditionalVetoRateRatioToPooledEmpirical"] == "22.101", "Veto-rate ratio drifted")
    require(float(pooled["conditionalVetoWilson95High"]) < float(simulator["conditionalVetoWilson95Low"]), "Veto-rate intervals unexpectedly overlap")
    for row in rows:
        if row["vetoes"] == "0":
            require(
                row["overrideWilson95Low"] == "NA"
                and row["overrideWilson95High"] == "NA",
                f"Zero-veto cohort {row['cohort']} must report an undefined override interval",
            )

    coverage = [row for row in rows if row["groupType"] == "final_vote_coverage"]
    require(sum(int(row["decisionCount"]) for row in coverage) == 4208, "Final-vote coverage denominator drifted")
    require(sum(int(row["vetoes"]) for row in coverage) == 47, "Final-vote coverage veto count drifted")
    minimum_support = [row for row in rows if row["groupType"] == "both_recorded_minimum_support"]
    opposition_support = [row for row in rows if row["groupType"] == "both_recorded_opposition_support"]
    for subset in (minimum_support, opposition_support):
        require(sum(int(row["decisionCount"]) for row in subset) == 310, "Both-recorded support denominator drifted")
        require(sum(int(row["vetoes"]) for row in subset) == 40, "Both-recorded support veto count drifted")

    text = EXECUTIVE_DIAGNOSTIC_MD.read_text()
    require("21 vetoes in 4021 decisions" in text, "Bill veto denominator disclosure drifted")
    require("26 vetoes in 187 decisions" in text, "Joint-resolution veto denominator disclosure drifted")
    require("47 vetoes in 4208 presented measures" in text, "Combined veto denominator disclosure drifted")
    require("647 vetoes in 2621 executive decisions" in text, "Simulator veto denominator disclosure drifted")
    require("22.101 times the combined empirical rate" in text, "Veto-rate mismatch disclosure drifted")
    require("computed from integer event counts before display rates are rounded" in text, "Exact-count ratio disclosure is missing")
    require("No veto-specific tolerance was prespecified" in text, "Post-hoc diagnostic boundary is missing")
    require("elevated-propensity veto stress mechanism" in text, "Veto mechanism interpretation boundary is missing")
    require("19 vetoes in 1937 decisions versus 2 in 2084" in text, "Government-control stratum disclosure drifted")
    require("20 vetoes in 1790 decisions versus 1 in 2217" in text, "Sponsor-party stratum disclosure drifted")
    require("do not estimate causal party-control or sponsor-party effects" in text, "Descriptive-strata boundary is missing")
    require("Bills and joint resolutions are reported separately" in text, "Measure-class boundary is missing")
    require("1,685 official final roll calls and 6,731 nonrecorded final approvals" in text, "Final-vote coverage disclosure drifted")
    require("earlier roll calls are never substituted" in text, "Final-vote non-imputation rule is missing")
    require("40 of 47 vetoes occur among the 310 measures" in text, "Final-vote selection disclosure drifted")
    require("35 of 145 measures" in text and "5 of 165 measures" in text, "Two-thirds support disclosure drifted")
    require("All 40 both-recorded vetoes" in text and "other 111 measures contain 0 vetoes" in text, "Opposition-support disclosure drifted")
    require("informative recording process" in text, "Final-vote missingness boundary is missing")
    require("log loss 0.026977 versus 0.223369" in text, "Locked presidential-choice result is missing")
    require("12 of 13 test vetoes arise among only 17 joint resolutions" in text, "Presidential-choice concentration boundary is missing")
    require("unchanged future whole-Congress replication" in text, "Presidential-choice next gate is missing")
    require("| 117 | 358 | 0 | 0.000000" in text and "| 0 | NA |" in text, "Undefined 117th override rate disclosure drifted")


def check_calibration() -> None:
    grid = read_csv(LIFECYCLE_CALIBRATION)
    require(len(grid) == 15, f"Expected 15 lifecycle candidates; found {len(grid)}")
    selected = [row for row in grid if row["selected"] == "1"]
    require(len(selected) == 1, "Lifecycle calibration must select exactly one candidate")
    require(selected[0]["calendarPriorityThreshold"] == "0.680", "Selected lifecycle threshold drifted")
    require(selected[0]["defaultThreshold"] == "0.680", "Model-default lifecycle threshold drifted")
    require(selected[0]["seedCount"] == "50" and selected[0]["simulatedBills"] == "72000", "Lifecycle calibration panel drifted")
    expected_diagnostics = {
        "enactedBills": "1974",
        "vetoes": "647",
        "overriddenVetoes": "0",
        "executiveDecisions": "2621",
        "conditionalVetoRate": "0.246852",
        "overrideRateAmongVetoes": "0.000000",
    }
    for field, expected_value in expected_diagnostics.items():
        require(selected[0][field] == expected_value, f"Lifecycle calibration {field} drifted")
    calibration_text = LIFECYCLE_CALIBRATION_MD.read_text()
    require(
        "Committee advancement is reported as an upstream workflow check" in calibration_text,
        "Committee-advance selection boundary is missing",
    )
    require(
        "Held-out use: reported only after threshold selection" in calibration_text,
        "Held-out selection boundary is missing",
    )
    require(
        "Leave-one-seed-out stability: 50 / 50 panels reselected 0.68" in calibration_text,
        "Lifecycle threshold leave-one-seed-out stability drifted",
    )
    require(
        "These quantities are diagnostics only. They do not enter threshold selection" in calibration_text,
        "Executive-action selection boundary is missing",
    )

    baseline = {row["key"]: row for row in read_csv(CALIBRATION_BASELINE)}
    expected = {
        "current-congress-committee-advance-rate": ("committeeAdvanceRate", "0.079", "0.120"),
        "current-congress-floor-consideration-rate": ("floor", "0.050", "0.081"),
        "current-congress-enactment-rate": ("productivity", "0.012", "0.033"),
    }
    for key, (metric, minimum, maximum) in expected.items():
        require(key in baseline, f"Missing lifecycle calibration baseline: {key}")
        row = baseline[key]
        require(row["scenarioKey"] == "current-congress-workflow", f"Wrong lifecycle scenario for {key}")
        require(row["metric"] == metric, f"Wrong lifecycle metric for {key}")
        require(row["minimum"] == minimum and row["maximum"] == maximum, f"Wrong lifecycle range for {key}")
        require(row["passed"] == "true", f"Lifecycle calibration failed: {key}")

    heldout = {
        row["metric"]: row
        for row in read_csv(HELDOUT)
        if row["sourceFamily"] == "govinfo bill and action records"
    }
    heldout_targets = {
        "committeeAdvanceRate": "current-congress-committee-advance-rate",
        "floorLoad": "current-congress-floor-consideration-rate",
        "enactmentRate": "current-congress-enactment-rate",
    }
    for metric, target in heldout_targets.items():
        require(metric in heldout, f"Missing GovInfo held-out metric: {metric}")
        require(heldout[metric]["calibrationTarget"] == target, f"Wrong held-out target for {metric}")
        require(heldout[metric]["heldoutTargetStatus"] == "pass", f"Held-out lifecycle check failed: {metric}")


def main() -> int:
    rows_116 = check_raw_116()
    rows = check_raw()
    rows_118 = check_raw_118()
    check_summary_116(rows_116)
    check_summary(rows)
    check_summary_118(rows_118)
    check_calibration()
    check_temporal_replication()
    check_executive_panel()
    check_joint_resolution_panel()
    check_final_vote_panel()
    check_executive_diagnostic()
    print("GovInfo censuses, lifecycle calibration, executive panels, and final-vote checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
