#!/usr/bin/env python3
"""Build a bounded district public-opinion proxy from Cumulative CES."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request
from urllib.request import urlopen


DATASET_DOI = "doi:10.7910/DVN/II2DB6"
DATASET_API = f"https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId={DATASET_DOI}"
ACCESS_API = "https://dataverse.harvard.edu/api/access/datafile/{file_id}"
FEATHER_LABEL = "cumulative_2006-2024.feather"
USER_AGENT = "congress-institutional-simulator-validation/0.4"
OUT_CSV = Path("data/validation/raw/district_public_opinion.csv")
OUT_METADATA = Path("data/validation/raw/district_public_opinion.metadata.md")
DEFAULT_CACHE_DIR = Path("no-include/validation-cache/ces")

READ_COLUMNS = [
    "year",
    "weight",
    "cd",
    "approval_rep",
    "intent_pres_party",
    "intent_rep_party",
    "voted_turnout_self",
    "intent_turnout_self",
    "no_healthins",
]

APPROVAL_SUPPORT = {
    "Strongly Approve": 1.0,
    "Approve / Somewhat Approve": 1.0,
    "Disapprove / Somewhat Disapprove": 0.0,
    "Strongly Disapprove": 0.0,
}
APPROVAL_STRONG = {"Strongly Approve", "Strongly Disapprove"}
MAJOR_PARTY_SUPPORT = {"Democratic": 1.0, "Republican": 0.0}
VOTED_TURNOUT = {"Yes": 1.0, "No": 0.0}
INTENT_TURNOUT = {
    "Yes, definitely": 1.0,
    "I already voted (early or absentee)": 1.0,
    "I Plan to Vote Before November 5th": 1.0,
    "Probably": 0.75,
    "Undecided": 0.5,
    "No": 0.0,
}


def fetch_json(url: str) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def dataset_metadata() -> dict[str, object]:
    payload = fetch_json(DATASET_API)
    if payload.get("status") != "OK":
        raise RuntimeError(f"Dataverse metadata request failed: {payload!r}")
    data = payload.get("data")
    return data if isinstance(data, dict) else {}


def latest_version(metadata: dict[str, object]) -> dict[str, object]:
    version = metadata.get("latestVersion")
    return version if isinstance(version, dict) else {}


def file_metadata(version: dict[str, object], label: str) -> dict[str, object]:
    files = version.get("files", [])
    if not isinstance(files, list):
        return {}
    for row in files:
        if not isinstance(row, dict):
            continue
        if row.get("label") == label:
            return row
    return {}


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_file(file_id: int, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    url = ACCESS_API.format(file_id=file_id)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=120) as response, destination.open("wb") as handle:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            handle.write(block)


def source_file(args: argparse.Namespace, meta: dict[str, object]) -> Path:
    if args.source_file:
        return args.source_file
    version = latest_version(meta)
    file_row = file_metadata(version, args.file_label)
    data_file = file_row.get("dataFile") if file_row else {}
    if not isinstance(data_file, dict):
        raise SystemExit(f"Could not find Dataverse file labeled {args.file_label!r}.")
    file_id = int(data_file["id"])
    checksum = data_file.get("checksum", {})
    expected_md5 = checksum.get("value") if isinstance(checksum, dict) else ""
    destination = args.cache_dir / args.file_label
    if destination.exists() and (not expected_md5 or md5(destination) == expected_md5):
        return destination
    print(f"Downloading CES source file {args.file_label} to {destination}", file=sys.stderr)
    download_file(file_id, destination)
    if expected_md5 and md5(destination) != expected_md5:
        raise SystemExit(f"Downloaded {destination} but MD5 did not match Dataverse metadata.")
    return destination


def load_table(path: Path, year: int):
    try:
        import pyarrow.compute as pc
        import pyarrow.feather as feather
    except ImportError as exc:
        raise SystemExit(
            "build_district_public_opinion_dataset.py requires pyarrow for the CES Feather file. "
            "Install it for this optional live-data target, for example: python3 -m pip install pyarrow"
        ) from exc
    table = feather.read_table(path, columns=READ_COLUMNS)
    return table.filter(pc.equal(table["year"], year))


def value(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def weight(value: object) -> float:
    value = value if value is not None else 1.0
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 1.0
    return parsed if parsed > 0 else 0.0


class DistrictStats:
    def __init__(self) -> None:
        self.respondents = 0
        self.weighted_respondents = 0.0
        self.uninsured_weight = 0.0
        self.uninsured_denom = 0.0
        self.turnout_weight = 0.0
        self.turnout_denom = 0.0
        self.issue_support: dict[str, float] = defaultdict(float)
        self.issue_denom: dict[str, float] = defaultdict(float)
        self.issue_respondents: dict[str, int] = defaultdict(int)
        self.issue_intensity: dict[str, float] = defaultdict(float)

    def add_affected(self, response: object, w: float) -> None:
        if response not in {"Yes", "No"}:
            return
        self.uninsured_denom += w
        if response == "Yes":
            self.uninsured_weight += w

    def add_turnout(self, voted: object, intent: object, w: float) -> None:
        score = VOTED_TURNOUT.get(voted)
        if score is None:
            score = INTENT_TURNOUT.get(intent)
        if score is None:
            return
        self.turnout_denom += w
        self.turnout_weight += w * score

    def add_issue(self, issue: str, support: float | None, intensity: float | None, w: float) -> None:
        if support is None:
            return
        self.issue_respondents[issue] += 1
        self.issue_denom[issue] += w
        self.issue_support[issue] += w * support
        self.issue_intensity[issue] += w * (intensity if intensity is not None else 1.0)

    def turnout(self) -> float:
        return self.turnout_weight / self.turnout_denom if self.turnout_denom else 0.0

    def affected(self) -> float:
        return self.uninsured_weight / self.uninsured_denom if self.uninsured_denom else 0.0


def aggregate_rows(table, year: int, min_support_respondents: int) -> list[dict[str, str]]:
    columns = {name: table[name].to_pylist() for name in READ_COLUMNS}
    districts: dict[str, DistrictStats] = defaultdict(DistrictStats)
    for index, district in enumerate(columns["cd"]):
        district = value(district)
        if not district:
            continue
        stats = districts[str(district)]
        w = weight(value(columns["weight"][index]))
        stats.respondents += 1
        stats.weighted_respondents += w
        approval = value(columns["approval_rep"][index])
        approval_support = APPROVAL_SUPPORT.get(approval)
        approval_intensity = 1.0 if approval in APPROVAL_STRONG else 0.5 if approval_support is not None else None
        stats.add_issue("house_representative_approval", approval_support, approval_intensity, w)
        pres_party = value(columns["intent_pres_party"][index])
        pres_support = MAJOR_PARTY_SUPPORT.get(pres_party)
        stats.add_issue("presidential_democratic_preference", pres_support, 1.0, w)
        house_party = value(columns["intent_rep_party"][index])
        house_support = MAJOR_PARTY_SUPPORT.get(house_party)
        stats.add_issue("house_democratic_preference", house_support, 1.0, w)
        stats.add_turnout(value(columns["voted_turnout_self"][index]), value(columns["intent_turnout_self"][index]), w)
        stats.add_affected(value(columns["no_healthins"][index]), w)

    rows: list[dict[str, str]] = []
    for district_id in sorted(districts):
        stats = districts[district_id]
        for issue in ("house_representative_approval", "presidential_democratic_preference", "house_democratic_preference"):
            support_n = stats.issue_respondents[issue]
            support_weight = stats.issue_denom[issue]
            if support_n < min_support_respondents or support_weight <= 0.0:
                continue
            rows.append({
                "district_id": district_id,
                "issue": issue,
                "support": f"{stats.issue_support[issue] / support_weight:.6f}",
                "intensity": f"{stats.issue_intensity[issue] / support_weight:.6f}",
                "turnout": f"{stats.turnout():.6f}",
                "affected_group_share": f"{stats.affected():.6f}",
                "year": str(year),
                "respondents": str(stats.respondents),
                "support_respondents": str(support_n),
                "weighted_respondents": f"{stats.weighted_respondents:.3f}",
                "support_weight": f"{support_weight:.3f}",
                "source": "Cumulative CES Common Content",
            })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "district_id",
        "issue",
        "support",
        "intensity",
        "turnout",
        "affected_group_share",
        "year",
        "respondents",
        "support_respondents",
        "weighted_respondents",
        "support_weight",
        "source",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]], meta: dict[str, object], source: Path) -> None:
    version = latest_version(meta)
    file_row = file_metadata(version, args.file_label)
    data_file = file_row.get("dataFile") if file_row else {}
    data_file = data_file if isinstance(data_file, dict) else {}
    issue_counts: dict[str, int] = defaultdict(int)
    districts = set()
    for row in rows:
        issue_counts[row["issue"]] += 1
        districts.add(row["district_id"])
    lines = [
        "# District Public Opinion Raw Validation Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Source:",
        "",
        "- Cumulative CES Common Content, Harvard Dataverse DOI 10.7910/DVN/II2DB6.",
        f"- Dataset version: {version.get('versionNumber', 'unknown')}.{version.get('versionMinorNumber', '0')}.",
        f"- Distribution date: {version.get('distributionDate', 'unknown')}.",
        f"- License: {version.get('license', {}).get('name', 'unknown') if isinstance(version.get('license'), dict) else 'unknown'}.",
        f"- Source file: {args.file_label} (Dataverse file id {data_file.get('id', 'unknown')}).",
        f"- Source cache path: {source}.",
        "",
        "Transformation:",
        "",
        f"- Filtered to survey year {args.year}.",
        f"- District-issue rows are retained only when at least {args.min_support_respondents} respondents answered the issue signal.",
        "- Unit of observation is district issue.",
        "- District ID is the CES `cd` congressional-district identifier.",
        "- `support` is a weighted district share for one of three survey-derived signals: own House representative approval, Democratic presidential preference, or Democratic House preference.",
        "- `intensity` is the weighted strong-opinion share for representative approval and the weighted major-party response share for the two preference rows.",
        "- `turnout` is the weighted self-reported post-election turnout share where available, with pre-election turnout intent as fallback.",
        "- `affected_group_share` is the weighted uninsured share from `no_healthins`; it is a generic district vulnerability proxy and not issue-specific affected-population mapping.",
        "",
        "Rows:",
        "",
        f"- Normalized district-issue rows: {len(rows)}",
        f"- Districts represented: {len(districts)}",
    ]
    for issue in sorted(issue_counts):
        lines.append(f"- {issue}: {issue_counts[issue]} rows")
    lines.extend([
        "",
        "Claim boundary:",
        "",
        "This file supports a bounded district-level public-opinion and turnout proxy. It is a direct aggregation of CES survey responses, not an MRP estimate, not bill-topic support, not issue-specific affected-group measurement, and not validation of generated public benefit or harm.",
    ])
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--file-label", default=FEATHER_LABEL)
    parser.add_argument("--source-file", type=Path)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--min-support-respondents", type=int, default=30)
    args = parser.parse_args()

    meta = dataset_metadata()
    source = source_file(args, meta)
    table = load_table(source, args.year)
    rows = aggregate_rows(table, args.year, args.min_support_respondents)
    if not rows:
        raise SystemExit("No CES district public-opinion rows matched the requested year.")
    write_csv(rows)
    write_metadata(args, rows, meta, source)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
