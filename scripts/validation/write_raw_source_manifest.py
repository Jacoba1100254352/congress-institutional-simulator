#!/usr/bin/env python3
"""Write an offline manifest for curated raw validation extracts."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


REGISTRY = Path("data/validation/source-registry.csv")
RAW_DIR = Path("data/validation/raw")
OUT_CSV = Path("reports/raw-source-manifest.csv")
OUT_MD = Path("reports/raw-source-manifest.md")

DERIVED_METADATA = {
    "topic_throughput.csv": RAW_DIR / "congress_derived.metadata.md",
    "sponsor_success.csv": RAW_DIR / "congress_derived.metadata.md",
    "committee_activity.csv": RAW_DIR / "congress_derived.metadata.md",
}

RELATED_RAW = {
    "govinfo_bill_census.csv": (
        RAW_DIR / "govinfo_bill_census_116.csv",
        RAW_DIR / "govinfo_bill_census_118.csv",
        RAW_DIR / "govinfo_executive_action_panel.csv",
    ),
}

DATE_COLUMNS = (
    "introduced_date",
    "referred_to_committee_date",
    "committee_ordered_reported_date",
    "committee_reported_date",
    "floor_considered_date",
    "passed_origin_chamber_date",
    "completed_congressional_passage_date",
    "presented_to_president_date",
    "floor_action_date",
    "enacted_date",
    "transaction_date",
    "period",
    "cycle",
    "year",
    "proposed_rule_date",
    "final_rule_date",
    "effective_date",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_path(dataset: str, raw_path: Path) -> Path:
    if dataset in DERIVED_METADATA:
        return DERIVED_METADATA[dataset]
    return raw_path.with_name(raw_path.name.replace(".csv", ".metadata.md"))


def metadata_title(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def raw_profile(path: Path) -> tuple[int, str, list[str], str]:
    if not path.exists() or path.is_dir():
        return 0, "", [], ""
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        row_count = 0
        date_values: list[str] = []
        for row in reader:
            row_count += 1
            for column in DATE_COLUMNS:
                value = row.get(column, "").strip()
                if value:
                    date_values.append(value[:10])
    date_range = f"{min(date_values)}..{max(date_values)}" if date_values else ""
    return row_count, date_range, columns, sha256(path)


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    ready = sum(1 for row in rows if row["rawStatus"] == "present")
    metadata_ready = sum(1 for row in rows if row["metadataStatus"] == "present")
    unique_raw = len({row["rawPath"] for row in rows if row["rawPath"]})
    related_count = sum(
        len([path for path in row["relatedRawPaths"].split(";") if path])
        for row in rows
    )
    related_ready = sum(
        status == "present"
        for row in rows
        for status in row["relatedRawStatuses"].split(";")
        if status
    )
    lines = [
        "# Raw Source Manifest",
        "",
        "This registry-backed manifest records the committed raw validation extracts used by the empirical-boundary workflow. It is a reproducibility inventory, not a validation claim.",
        "",
        f"- Source-family rows: {len(rows)}",
        f"- Unique raw files: {unique_raw}",
        f"- Present raw files: {ready} / {len(rows)}",
        f"- Present metadata notes: {metadata_ready} / {len(rows)}",
        f"- Related temporal-cohort files: {related_ready} / {related_count}",
        "",
        "| Source family | Dataset | Rows | Related cohort | Metadata | Boundary | Source hash | Claim boundary |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        source_hash = row["rawSha256"][:12] if row["rawSha256"] else "---"
        metadata = row["metadataPath"] if row["metadataStatus"] == "present" else "missing"
        related = "---"
        if row["relatedRawPaths"]:
            related_paths = row["relatedRawPaths"].split(";")
            related_counts = row["relatedRawRowCounts"].split(";")
            related_hashes = row["relatedRawSha256"].split(";")
            related = "; ".join(
                f"`{path}` ({count} rows; `{digest[:12]}`)"
                for path, count, digest in zip(related_paths, related_counts, related_hashes)
            )
        lines.append(
            f"| {row['sourceFamily']} | `{row['dataset']}` | {row['rowCount']} | "
            f"{related} | `{metadata}` | {row['boundaryCategory']} | `{source_hash}` | "
            f"{row['claimBoundary']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    registry = read_csv(REGISTRY)
    if not registry:
        raise SystemExit(f"{REGISTRY} is missing or empty.")

    rows: list[dict[str, str]] = []
    for source in registry:
        raw_path = Path(source["raw_path"]) if source.get("raw_path") else Path("")
        dataset = source["dataset"]
        row_count, date_range, columns, raw_hash = raw_profile(raw_path)
        meta_path = metadata_path(dataset, raw_path) if raw_path else Path("")
        meta_hash = sha256(meta_path) if meta_path.exists() else ""
        related_paths = RELATED_RAW.get(dataset, ())
        related_profiles = [raw_profile(path) for path in related_paths]
        related_metadata = [metadata_path(path.name, path) for path in related_paths]
        rows.append({
            "sourceFamily": source["source_family"],
            "sourceName": source["source_name"],
            "dataset": dataset,
            "rawPath": str(raw_path) if raw_path else "",
            "rawStatus": "present" if raw_path.exists() else "missing",
            "rowCount": str(row_count),
            "dateRange": date_range,
            "columnCount": str(len(columns)),
            "columns": ",".join(columns),
            "rawSha256": raw_hash,
            "metadataPath": str(meta_path) if meta_path else "",
            "metadataStatus": "present" if meta_path.exists() else "missing",
            "metadataTitle": metadata_title(meta_path),
            "metadataSha256": meta_hash,
            "relatedRawPaths": ";".join(str(path) for path in related_paths),
            "relatedRawStatuses": ";".join("present" if path.exists() else "missing" for path in related_paths),
            "relatedRawRowCounts": ";".join(str(profile[0]) for profile in related_profiles),
            "relatedRawSha256": ";".join(profile[3] for profile in related_profiles),
            "relatedMetadataPaths": ";".join(str(path) for path in related_metadata),
            "relatedMetadataStatuses": ";".join("present" if path.exists() else "missing" for path in related_metadata),
            "relatedMetadataSha256": ";".join(sha256(path) if path.exists() else "" for path in related_metadata),
            "transformationScript": source["transformation_script"],
            "networkRequired": source["network_required"],
            "apiKeyRequired": source["api_key_required"],
            "offlineStatus": source["offline_status"],
            "boundaryCategory": source["boundary_category"],
            "claimBoundary": source["claim_boundary"],
            "limitations": source["limitations"],
            "licenseAccessNotes": source["license_access_notes"],
        })

    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
