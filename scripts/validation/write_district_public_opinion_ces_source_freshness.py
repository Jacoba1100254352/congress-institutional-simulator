#!/usr/bin/env python3
"""Audit the cached district public-opinion CES source against Dataverse."""

from __future__ import annotations

import csv
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATASET_DOI = "10.7910/DVN/II2DB6"
DATAVERSE_API_URL = (
    "https://dataverse.harvard.edu/api/datasets/:persistentId/"
    f"?persistentId=doi:{DATASET_DOI}"
)
DATAVERSE_DATASET_URL = (
    "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:"
    f"{DATASET_DOI}"
)
CES_DOWNLOADS_URL = (
    "https://tischcollege.tufts.edu/research-faculty/research-centers/"
    "cooperative-election-study/data-downloads"
)
LOCAL_METADATA = Path("data/validation/raw/district_public_opinion.metadata.md")
OUT_CSV = Path("reports/district-public-opinion-ces-source-freshness.csv")
OUT_MD = Path("reports/district-public-opinion-ces-source-freshness.md")

MISSING_LINKS = (
    "acquired_survey_item_ids; bill_topic_public_opinion; "
    "mrp_or_small_area_estimates; bill_text_specific_affected_population; "
    "affected_group_support_harm"
)
EVIDENCE_LAYERS = (
    "source_version_metadata; current_dataverse_distribution; "
    "local_cached_extract_metadata"
)
CLAIM_BOUNDARY = (
    "Source freshness audit only. It does not acquire survey item IDs, "
    "estimate bill-topic public support, build MRP/small-area estimates, "
    "define bill-text-specific affected populations, measure affected-group "
    "support or harm, or validate public benefit."
)
STALE_ACTION = (
    "Refresh district_public_opinion.csv from the latest Cumulative CES "
    "distribution after optional Feather/Stata tooling is available, then "
    "rerun the district linkage, policy-context, bill-topic readiness, "
    "source-packet, Census, ACS, survey-source crosswalk, raw-source manifest, "
    "and empirical-boundary reports before treating the public-opinion cache "
    "as current."
)
CURRENT_ACTION = (
    "Keep the cached district_public_opinion.csv source metadata pinned to "
    "the current Dataverse distribution and continue bill-topic item, MRP, and "
    "affected-population acquisition."
)


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/source-freshness-audit"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def latest_version(data: dict[str, Any]) -> dict[str, Any]:
    latest = data.get("data", {}).get("latestVersion")
    if not isinstance(latest, dict):
        raise SystemExit("Dataverse response did not include data.latestVersion.")
    return latest


def version_label(version: dict[str, Any]) -> str:
    number = version.get("versionNumber")
    minor = version.get("versionMinorNumber")
    if number is None:
        return ""
    if minor is None:
        return str(number)
    return f"{number}.{minor}"


def checksum(data_file: dict[str, Any]) -> str:
    if data_file.get("md5"):
        return str(data_file["md5"])
    nested = data_file.get("checksum")
    if isinstance(nested, dict):
        return str(nested.get("value", ""))
    return ""


def official_file_rows(version: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for wrapper in version.get("files", []):
        data_file = wrapper.get("dataFile", {})
        label = wrapper.get("label") or data_file.get("filename") or ""
        file_id = str(data_file.get("id", ""))
        if label.endswith(".feather"):
            role = "preferred_current_microdata_file"
        elif label.endswith(".pdf") or label.startswith("guide_"):
            role = "current_guide_pdf"
        else:
            role = "current_distribution_file"
        rows.append({
            "officialFileRole": role,
            "officialFileLabel": label,
            "officialFileId": file_id,
            "officialFileMd5": checksum(data_file),
            "officialFileSizeBytes": str(data_file.get("filesize", "")),
            "officialContentType": str(data_file.get("contentType", "")),
            "officialDownloadUrl": (
                f"https://dataverse.harvard.edu/api/access/datafile/{file_id}"
                if file_id else ""
            ),
        })
    return rows


def metadata_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip().rstrip(".")
    return ""


def read_local_metadata() -> dict[str, str]:
    if not LOCAL_METADATA.exists():
        raise SystemExit(f"{LOCAL_METADATA} is missing.")
    text = LOCAL_METADATA.read_text()
    source_match = re.search(
        r"Source file:\s*([^\s]+)\s*\(Dataverse file id\s*([^)]+)\)",
        text,
    )
    extract_match = re.search(r"Filtered to survey year\s+([0-9]{4})", text)
    cache_path = metadata_line(text, "- Source cache path")
    cache = Path(cache_path) if cache_path else Path("")
    return {
        "localMetadataPath": str(LOCAL_METADATA),
        "localMetadataGenerated": metadata_line(text, "Generated"),
        "localMetadataVersion": metadata_line(text, "- Dataset version"),
        "localMetadataDistributionDate": metadata_line(text, "- Distribution date"),
        "localSourceFile": source_match.group(1) if source_match else "",
        "localDataverseFileId": source_match.group(2) if source_match else "",
        "localSourceCachePath": cache_path,
        "localCacheStatus": "present" if cache_path and cache.exists() else "missing",
        "localCacheSizeBytes": str(cache.stat().st_size) if cache_path and cache.exists() else "",
        "localExtractYear": extract_match.group(1) if extract_match else "",
    }


def freshness_status(
    official_version: str,
    official_files: list[dict[str, str]],
    local: dict[str, str],
) -> str:
    official_feather = next(
        (
            row["officialFileLabel"]
            for row in official_files
            if row["officialFileRole"] == "preferred_current_microdata_file"
        ),
        "",
    )
    if official_version != local["localMetadataVersion"]:
        return "official_ces_source_newer_than_cached_extract"
    if official_feather and official_feather != local["localSourceFile"]:
        return "official_ces_source_file_differs_from_cached_extract"
    return "cached_extract_matches_official_latest_metadata"


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    first = rows[0]
    stale = first["freshnessStatus"] != "cached_extract_matches_official_latest_metadata"
    status_text = "stale relative to the official latest CES distribution" if stale else "current against official latest CES metadata"
    lines = [
        "# District Public Opinion CES Source Freshness",
        "",
        "This report compares the cached district public-opinion raw-source metadata to the live Harvard Dataverse metadata for the Cumulative CES Common Content dataset.",
        "",
        f"- Audit generated: {first['auditGeneratedUtc']}",
        f"- Source family: {first['sourceFamily']}",
        f"- Dataset DOI: {first['datasetDoi']}",
        f"- Official latest version: {first['officialLatestVersion']}",
        f"- Official release time: {first['officialReleaseTime']}",
        f"- Local cached metadata version: {first['localMetadataVersion']}",
        f"- Local cached source file: `{first['localSourceFile']}`",
        f"- Local extract year: {first['localExtractYear']}",
        f"- Freshness status: `{first['freshnessStatus']}` ({status_text})",
        "",
        "The local district public-opinion extract remains a bounded 2024 direct-aggregation snapshot until it is rebuilt from the current official distribution. This source-freshness audit is intentionally separate from the offline paper checks because it depends on live Dataverse metadata.",
        "",
        "## Official Files",
        "",
        "| Role | File | File id | Size bytes | MD5 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['officialFileRole']} | `{row['officialFileLabel']}` | "
            f"{row['officialFileId']} | {row['officialFileSizeBytes']} | "
            f"`{row['officialFileMd5']}` |"
        )
    lines.extend([
        "",
        "## Action Required",
        "",
        first["actionRequired"],
        "",
        "## Claim Boundary",
        "",
        first["claimBoundary"],
        "",
        "## Source URLs",
        "",
        f"- {DATAVERSE_DATASET_URL}",
        f"- {DATAVERSE_API_URL}",
        f"- {CES_DOWNLOADS_URL}",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    payload = fetch_json(DATAVERSE_API_URL)
    latest = latest_version(payload)
    official_version = version_label(latest)
    official_release = latest.get("releaseTime") or latest.get("lastUpdateTime") or ""
    official_files = official_file_rows(latest)
    if not official_files:
        raise SystemExit("Dataverse response did not include latest-version files.")
    local = read_local_metadata()
    status = freshness_status(official_version, official_files, local)
    action = STALE_ACTION if status != "cached_extract_matches_official_latest_metadata" else CURRENT_ACTION
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    source_urls = "; ".join([DATAVERSE_DATASET_URL, DATAVERSE_API_URL, CES_DOWNLOADS_URL])

    rows: list[dict[str, str]] = []
    for official in official_files:
        rows.append({
            "auditGeneratedUtc": now,
            "sourceFamily": "District public opinion and affected groups",
            "sourceName": "Cumulative CES Common Content",
            "datasetDoi": DATASET_DOI,
            "officialLatestVersion": official_version,
            "officialVersionState": str(latest.get("versionState", "")),
            "officialReleaseTime": str(official_release),
            **official,
            **local,
            "freshnessStatus": status,
            "actionRequired": action,
            "evidenceLayers": EVIDENCE_LAYERS,
            "missingLinks": MISSING_LINKS,
            "sourceUrls": source_urls,
            "claimBoundary": CLAIM_BOUNDARY,
        })

    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
