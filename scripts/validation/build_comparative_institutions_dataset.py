#!/usr/bin/env python3
"""Build a bounded comparative-institutions validation sample."""

from __future__ import annotations

import argparse
import csv
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


QOG_URL = (
    "https://datafinder.qog.gu.se/data_generator"
    "?download=gol_adm,gol_enpp,h_l1,h_l2&type=csv"
)
JUDICIAL_URL = (
    "https://ourworldindata.org/grapher/"
    "judicial-constraints-on-the-executive-index.csv"
    "?v=1&csvType=full&useColumnShortNames=false"
)
LEGISLATIVE_URL = (
    "https://ourworldindata.org/grapher/"
    "legislative-constraints-on-the-executive-index.csv"
    "?v=1&csvType=full&useColumnShortNames=false"
)
USER_AGENT = "congress-institutional-simulator-validation/0.1"
OUT_CSV = Path("data/validation/raw/comparative_institutions.csv")
OUT_METADATA = Path("data/validation/raw/comparative_institutions.metadata.md")
DEFAULT_CACHE_DIR = Path("no-include/validation-cache/comparative-institutions")


def fetch(url: str, target: Path, retries: int = 4) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=90) as response, target.open("wb") as handle:
                shutil.copyfileobj(response, handle)
            return
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)


def cached_or_source(source_file: Path | None, cache_dir: Path, name: str, url: str) -> Path:
    if source_file is not None:
        if not source_file.exists():
            raise FileNotFoundError(f"Missing source file: {source_file}")
        return source_file
    path = cache_dir / name
    fetch(url, path)
    return path


def qog_float(value: str) -> float | None:
    text = (value or "").strip().replace(",", ".")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def standard_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def qog_rows(path: Path, start_year: int, end_year: int) -> tuple[list[dict[str, str]], dict[str, int]]:
    complete: list[dict[str, str]] = []
    stats = {
        "source_rows": 0,
        "outside_window": 0,
        "missing_qog_fields": 0,
        "missing_iso3": 0,
    }
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        for row in reader:
            stats["source_rows"] += 1
            try:
                year = int(row.get("year", ""))
            except ValueError:
                stats["missing_qog_fields"] += 1
                continue
            if year < start_year or year > end_year:
                stats["outside_window"] += 1
                continue
            iso3 = (row.get("ccodealp") or "").strip()
            if not iso3:
                stats["missing_iso3"] += 1
                continue
            required = {
                "district_magnitude": qog_float(row.get("gol_adm", "")),
                "party_fragmentation": qog_float(row.get("gol_enpp", "")),
                "h_l1": qog_float(row.get("h_l1", "")),
                "h_l2": qog_float(row.get("h_l2", "")),
            }
            if any(value is None for value in required.values()):
                stats["missing_qog_fields"] += 1
                continue
            lower = required["h_l1"] or 0.0
            upper = required["h_l2"] or 0.0
            chambers = 0
            if lower >= 0.5:
                chambers = 1 + (1 if upper >= 0.5 else 0)
            complete.append({
                "country": (row.get("cname") or row.get("cname_qog") or "").strip(),
                "year": str(year),
                "iso3": iso3,
                "chambers": str(chambers),
                "district_magnitude": f"{required['district_magnitude']:.6f}",
                "party_fragmentation": f"{required['party_fragmentation']:.6f}",
                "raw_h_l1": f"{lower:.6f}",
                "raw_h_l2": f"{upper:.6f}",
                "raw_gol_adm": f"{required['district_magnitude']:.6f}",
                "raw_gol_enpp": f"{required['party_fragmentation']:.6f}",
            })
    stats["complete_qog_rows"] = len(complete)
    return complete, stats


def owid_index(path: Path, value_column: str) -> dict[tuple[str, int], float]:
    values: dict[tuple[str, int], float] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            code = (row.get("Code") or "").strip()
            if len(code) != 3:
                continue
            try:
                year = int(row.get("Year", ""))
            except ValueError:
                continue
            value = standard_float(row.get(value_column, ""))
            if value is None:
                continue
            values[(code, year)] = value
    return values


def normalize(args: argparse.Namespace) -> tuple[list[dict[str, str]], dict[str, int]]:
    cache_dir = Path(args.cache_dir)
    qog_path = cached_or_source(args.qog_source_file, cache_dir, "qog_des_polcon_selected.csv", QOG_URL)
    judicial_path = cached_or_source(args.judicial_source_file, cache_dir, "owid_vdem_judicial_constraints.csv", JUDICIAL_URL)
    legislative_path = cached_or_source(args.legislative_source_file, cache_dir, "owid_vdem_legislative_constraints.csv", LEGISLATIVE_URL)

    base_rows, stats = qog_rows(qog_path, args.start_year, args.end_year)
    judicial = owid_index(judicial_path, "Judicial Checks on Government Index")
    legislative = owid_index(legislative_path, "Legislative constraints on the executive index")

    joined: list[dict[str, str]] = []
    missing_judicial = 0
    missing_legislative = 0
    for row in base_rows:
        key = (row["iso3"], int(row["year"]))
        judicial_review = judicial.get(key)
        legislative_capacity = legislative.get(key)
        if judicial_review is None:
            missing_judicial += 1
            continue
        if legislative_capacity is None:
            missing_legislative += 1
            continue
        joined.append({
            **row,
            "judicial_review": f"{judicial_review:.6f}",
            "legislative_productivity": f"{legislative_capacity:.6f}",
            "judicial_review_source": "OWID/V-Dem v2x_jucon",
            "legislative_productivity_source": "OWID/V-Dem v2xlg_legcon",
        })

    if args.latest_per_country:
        latest: dict[str, dict[str, str]] = {}
        for row in joined:
            current = latest.get(row["iso3"])
            if current is None or int(row["year"]) > int(current["year"]):
                latest[row["iso3"]] = row
        joined = sorted(latest.values(), key=lambda row: (row["country"], row["year"], row["iso3"]))
    else:
        joined = sorted(joined, key=lambda row: (row["country"], row["year"], row["iso3"]))

    stats.update({
        "missing_judicial_index": missing_judicial,
        "missing_legislative_index": missing_legislative,
        "normalized_rows": len(joined),
        "countries": len({row["iso3"] for row in joined}),
        "min_year": min((int(row["year"]) for row in joined), default=0),
        "max_year": max((int(row["year"]) for row in joined), default=0),
        "latest_per_country": 1 if args.latest_per_country else 0,
    })
    return joined, stats


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "country",
        "year",
        "chambers",
        "district_magnitude",
        "judicial_review",
        "party_fragmentation",
        "legislative_productivity",
        "iso3",
        "raw_h_l1",
        "raw_h_l2",
        "raw_gol_adm",
        "raw_gol_enpp",
        "judicial_review_source",
        "legislative_productivity_source",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, stats: dict[str, int]) -> None:
    mode = "latest complete country-year per ISO3 country" if args.latest_per_country else "all complete country-years"
    lines = [
        "# Comparative Institutions Raw Validation Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Sources:",
        "",
        "- QoG Data Finder selected-variable CSV endpoint for `gol_adm`, `gol_enpp`, `h_l1`, and `h_l2`.",
        "- Democratic Electoral Systems 1919-2020 dataset via QoG for lower-house district magnitude and effective number of legislative parties.",
        "- Henisz POLCON dataset via QoG for effective first and second legislative chamber indicators.",
        "- Our World in Data/V-Dem judicial constraints on the executive index (`v2x_jucon`).",
        "- Our World in Data/V-Dem legislative constraints on the executive index (`v2xlg_legcon`).",
        "",
        "Source URLs:",
        "",
        f"- QoG selected CSV: {QOG_URL}",
        "- DES metadata: https://datafinder.qog.gu.se/dataset/gol",
        "- POLCON metadata: https://datafinder.qog.gu.se/dataset/h",
        "- OWID/V-Dem judicial constraints: https://ourworldindata.org/grapher/judicial-constraints-on-the-executive-index",
        "- OWID/V-Dem legislative constraints: https://ourworldindata.org/grapher/legislative-constraints-on-the-executive-index",
        "- V-Dem dataset page: https://www.v-dem.net/data/the-v-dem-dataset/",
        "",
        "Transformation:",
        "",
        f"- Source year window requested: {args.start_year}-{args.end_year}.",
        f"- Output mode: {mode}.",
        "- `chambers` is encoded as 1 plus `h_l2` when `h_l1` indicates an effective lower chamber; otherwise it is 0.",
        "- `district_magnitude` is QoG/DES `gol_adm`.",
        "- `party_fragmentation` is QoG/DES `gol_enpp`, the effective number of parliamentary or legislative parties.",
        "- `judicial_review` is OWID/V-Dem `v2x_jucon`, a 0-1 judicial-constraints index.",
        "- `legislative_productivity` is OWID/V-Dem `v2xlg_legcon`, a 0-1 legislative-constraints and oversight index. The column name is kept for schema compatibility; it is not observed law-output productivity.",
        "",
        "Rows:",
        "",
        f"- QoG source rows read: {stats['source_rows']}",
        f"- Complete QoG rows in window: {stats['complete_qog_rows']}",
        f"- Normalized rows written: {stats['normalized_rows']}",
        f"- Countries represented: {stats['countries']}",
        f"- Output year range: {stats['min_year']}-{stats['max_year']}",
        f"- Skipped outside requested window: {stats['outside_window']}",
        f"- Skipped for missing QoG fields: {stats['missing_qog_fields']}",
        f"- Skipped for missing ISO3 code: {stats['missing_iso3']}",
        f"- Skipped for missing OWID/V-Dem judicial index: {stats['missing_judicial_index']}",
        f"- Skipped for missing OWID/V-Dem legislative index: {stats['missing_legislative_index']}",
        "",
        "Claim boundary:",
        "",
        "This file supports a bounded comparative-institution profile for chamber structure, district magnitude, judicial constraints, party fragmentation, and legislative-constraint proxies. It does not validate comparative institutional fit, bicameral disagreement, chamber-specific representation, law-output productivity, or country-level adoption claims.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-year", type=int, default=2010)
    parser.add_argument("--end-year", type=int, default=2020)
    parser.add_argument("--latest-per-country", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE_DIR))
    parser.add_argument("--qog-source-file", type=Path)
    parser.add_argument("--judicial-source-file", type=Path)
    parser.add_argument("--legislative-source-file", type=Path)
    args = parser.parse_args()

    rows, stats = normalize(args)
    if not rows:
        raise SystemExit("No comparative-institution rows matched the requested source window.")
    write_csv(rows)
    write_metadata(args, stats)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
