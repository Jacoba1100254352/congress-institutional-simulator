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
BUILDER = Path("scripts/validation/build_govinfo_bill_census_dataset.py")
SUMMARY = Path("reports/govinfo-bill-census.csv")
SUMMARY_MD = Path("reports/govinfo-bill-census.md")
LIFECYCLE_CALIBRATION = Path("reports/legislative-lifecycle-calibration.csv")
LIFECYCLE_CALIBRATION_MD = Path("reports/legislative-lifecycle-calibration.md")
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


def metadata_values() -> dict[str, str]:
    require(METADATA.exists(), f"Missing required artifact: {METADATA}")
    values: dict[str, str] = {}
    for line in METADATA.read_text().splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            values[key] = value.strip().strip("`")
    return values


def truthy(row: dict[str, str], field: str) -> bool:
    return row.get(field) == "1"


def check_raw() -> list[dict[str, str]]:
    rows = read_csv(RAW)
    metadata = metadata_values()
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
    require(all(row["classification_version"] == "govinfo-bill-lifecycle-v1" for row in rows), "Classification version drifted")

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
    require(metadata.get("classification_version") == "govinfo-bill-lifecycle-v1", "Metadata classifier version drifted")
    require(metadata.get("builder_sha256") == sha256_file(BUILDER), "Metadata builder hash does not match the current builder")
    require(metadata.get("output_sha256") == sha256_file(RAW), "Metadata output hash does not match census bytes")
    metadata_text = METADATA.read_text()
    for archive in EXPECTED_ARCHIVES.values():
        require(archive["sha256"] in metadata_text, "Pinned archive hash missing from metadata")
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
    check_summary(rows)
    check_calibration()
    print("GovInfo bill census and lifecycle calibration checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
