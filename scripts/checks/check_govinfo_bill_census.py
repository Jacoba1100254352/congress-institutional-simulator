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
RAW_118 = Path("data/validation/raw/govinfo_bill_census_118.csv")
METADATA_118 = Path("data/validation/raw/govinfo_bill_census_118.metadata.md")
BUILDER = Path("scripts/validation/build_govinfo_bill_census_dataset.py")
SUMMARY = Path("reports/govinfo-bill-census.csv")
SUMMARY_MD = Path("reports/govinfo-bill-census.md")
SUMMARY_118 = Path("reports/govinfo-bill-census-118.csv")
SUMMARY_118_MD = Path("reports/govinfo-bill-census-118.md")
LIFECYCLE_CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
LIFECYCLE_CALIBRATION_MD = Path("reports/legislative-lifecycle-calibration.md")
TEMPORAL_REPLICATION = Path("reports/legislative-lifecycle-temporal-replication.csv")
TEMPORAL_REPLICATION_MD = Path("reports/legislative-lifecycle-temporal-replication.md")
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
    "enactedCount": 269,
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
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v2" for row in rows), "Classification version drifted")

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

    require(metadata.get("rows") == "15066", "Metadata row count drifted")
    require(metadata.get("parsed_action_records") == "72047", "Metadata action count drifted")
    require(metadata.get("enacted_rows") == "358", "Metadata enacted count drifted")
    require(metadata.get("public_law_rows") == "355", "Metadata public-law count drifted")
    require(metadata.get("private_law_rows") == "3", "Metadata private-law count drifted")
    require(metadata.get("integrity_valid_rows") == "15061", "Metadata valid-row count drifted")
    require(metadata.get("source_date_anomaly_rows") == "5", "Metadata anomaly count drifted")
    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v2", "Metadata classifier version drifted")
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
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v2" for row in rows), "118th classification version drifted")

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
        "classification_version": "govinfo-bill-lifecycle-v2",
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
    require("complete 118th census supplies the separate no-refit temporal transport test" in text, "117th report does not point to temporal replication")


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
    require("No 118th-Congress record participates in threshold selection" in text, "118th no-refit boundary is missing")
    require("20 preserved source-date anomalies" in text, "118th anomaly disclosure is missing")


def check_temporal_replication() -> None:
    rows = read_csv(TEMPORAL_REPLICATION)
    require(len(rows) == 3, f"Expected three temporal transport rows; found {len(rows)}")
    by_metric = {row["metric"]: row for row in rows}
    expected = {
        "committeeAdvanceRate": ("1843", "0.113674", "-0.007396", "0.020000", "pass"),
        "floorConsiderationRate": ("957", "0.059027", "0.002070", "0.015000", "pass"),
        "enactmentRate": ("269", "0.016592", "0.010825", "0.010000", "fail"),
    }
    require(set(by_metric) == set(expected), "Temporal transport metric set drifted")
    for metric, (count, test_rate, error, tolerance, status) in expected.items():
        row = by_metric[metric]
        require(row["selectionCongress"] == "117" and row["testCongress"] == "118", f"Temporal Congress labels drifted for {metric}")
        require(row["frozenThreshold"] == "0.680", f"Frozen threshold drifted for {metric}")
        require(row["seedCount"] == "50" and row["simulatedBills"] == "72000", f"Frozen panel drifted for {metric}")
        require(row["testCount"] == count and row["testBills"] == "16213", f"Temporal count drifted for {metric}")
        require(row["testRate"] == test_rate, f"Temporal test rate drifted for {metric}")
        require(row["transportError"] == error, f"Temporal error drifted for {metric}")
        require(row["prespecifiedTolerance"] == tolerance, f"Temporal tolerance drifted for {metric}")
        require(row["toleranceStatus"] == status, f"Temporal tolerance result drifted for {metric}")
        require(row["testRateInBaselineRange"] == "pass", f"Temporal broad-range result drifted for {metric}")
        require(float(row["testWilson95Low"]) < float(row["testRate"]) < float(row["testWilson95High"]), f"Temporal Wilson interval does not contain rate for {metric}")

    text = TEMPORAL_REPLICATION_MD.read_text()
    require("passes 2 of 3 point-error tolerances" in text, "Temporal pass/fail summary drifted")
    require("Enactment misses its tolerance by 0.000825" in text, "Temporal enactment miss disclosure drifted")
    require("No 118th rate is read by the calibration selector" in text, "Temporal no-refit protocol is missing")
    require("This is a classifier correction, not a post-hoc parameter change" in text, "Classifier correction boundary is missing")


def check_calibration() -> None:
    grid = read_csv(LIFECYCLE_CALIBRATION)
    require(len(grid) == 15, f"Expected 15 lifecycle candidates; found {len(grid)}")
    selected = [row for row in grid if row["selected"] == "1"]
    require(len(selected) == 1, "Lifecycle calibration must select exactly one candidate")
    require(selected[0]["calendarPriorityThreshold"] == "0.680", "Selected lifecycle threshold drifted")
    require(selected[0]["defaultThreshold"] == "0.680", "Model-default lifecycle threshold drifted")
    require(selected[0]["seedCount"] == "50" and selected[0]["simulatedBills"] == "72000", "Lifecycle calibration panel drifted")
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
    rows = check_raw()
    rows_118 = check_raw_118()
    check_summary(rows)
    check_summary_118(rows_118)
    check_calibration()
    check_temporal_replication()
    print("GovInfo bill censuses, lifecycle calibration, and temporal replication checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
