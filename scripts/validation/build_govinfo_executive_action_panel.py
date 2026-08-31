#!/usr/bin/env python3
"""Build a compact, provenance-pinned panel of presidential bill decisions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from .build_govinfo_bill_census_dataset import (
        ArchiveInfo,
        CLASSIFICATION_VERSION,
        DEFAULT_ARCHIVE_DIR,
        DEFAULT_BILL_TYPES,
        archive_info,
        archive_name,
        archive_url,
        bill_sort_key,
        download_archive,
        metadata_values,
        parse_bill_xml,
        sha256_file,
    )
    from .reproducible_metadata import write_reproducible_metadata
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_bill_census_dataset import (
        ArchiveInfo,
        CLASSIFICATION_VERSION,
        DEFAULT_ARCHIVE_DIR,
        DEFAULT_BILL_TYPES,
        archive_info,
        archive_name,
        archive_url,
        bill_sort_key,
        download_archive,
        metadata_values,
        parse_bill_xml,
        sha256_file,
    )
    from reproducible_metadata import write_reproducible_metadata


DEFAULT_CONGRESSES = tuple(range(108, 119))
CONTEXT = Path("data/validation/reference/congress_executive_context.csv")
VETO_REFERENCE = Path("data/validation/reference/senate_veto_reference_108_118.csv")
OUT_CSV = Path("data/validation/raw/govinfo_executive_action_panel.csv")
OUT_METADATA = Path("data/validation/raw/govinfo_executive_action_panel.metadata.md")

EXPECTED_SOURCE_CROSS_CONGRESS_LAW_NUMBERS = {
    "109-hr-5441",
    "110-hr-6124",
    "110-s-2499",
}

FIELDNAMES = [
    "bill_id",
    "congress",
    "bill_type",
    "bill_number",
    "origin_chamber",
    "title",
    "policy_area",
    "president",
    "president_party",
    "house_majority_party",
    "senate_majority_party",
    "government_control",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_same_party_as_president",
    "presented_to_president_date",
    "presented_to_president_basis",
    "executive_outcome",
    "executive_decision_date",
    "veto_kind_reference",
    "vetoed",
    "vetoed_date",
    "vetoed_basis",
    "veto_overridden",
    "veto_overridden_date",
    "veto_overridden_basis",
    "enacted",
    "enacted_date",
    "enacted_basis",
    "law_type",
    "law_number",
    "source_law_number_status",
    "recorded_vote_count",
    "actions_count",
    "president_action_count",
    "source_xml_update_date",
    "source_xml_sha256",
    "actions_sha256",
    "source_archive",
    "source_url",
    "classification_version",
    "integrity_status",
]

CLAIM_BOUNDARY = (
    "This panel supports descriptive analysis of H.R./S. presentment, veto, "
    "override, and enactment decisions from complete GovInfo BILLSTATUS archives. "
    "Party-control fields are congressional context, not estimates of policy "
    "distance, causal presidential choice, bill quality, welfare, or institutional rank."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def parse_congresses(value: str) -> tuple[int, ...]:
    result: set[int] = set()
    for part in value.split(","):
        normalized = part.strip()
        if not normalized:
            continue
        if re.fullmatch(r"\d+", normalized):
            result.add(int(normalized))
            continue
        match = re.fullmatch(r"(\d+)-(\d+)", normalized)
        if not match:
            raise argparse.ArgumentTypeError(f"Invalid Congress selection: {part}")
        start, end = (int(item) for item in match.groups())
        if start > end:
            raise argparse.ArgumentTypeError(f"Congress range is reversed: {part}")
        result.update(range(start, end + 1))
    if not result:
        raise argparse.ArgumentTypeError("At least one Congress is required.")
    return tuple(sorted(result))


def read_context(path: Path, congresses: tuple[int, ...]) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_congress = {row["congress"]: row for row in rows}
    require(len(by_congress) == len(rows), f"{path} contains duplicate Congress rows.")
    selected: dict[str, dict[str, str]] = {}
    for congress in congresses:
        key = str(congress)
        require(key in by_congress, f"{path} lacks Congress {congress} context.")
        row = by_congress[key]
        for field in ("president_party", "house_majority_party", "senate_majority_party"):
            require(row.get(field) in {"D", "R"}, f"Congress {congress} has invalid {field}.")
        expected_control = (
            "unified"
            if len(
                {
                    row["president_party"],
                    row["house_majority_party"],
                    row["senate_majority_party"],
                }
            )
            == 1
            else "divided"
        )
        require(
            row.get("government_control") == expected_control,
            f"Congress {congress} government-control label is inconsistent.",
        )
        require(row.get("president", "").strip(), f"Congress {congress} lacks a president.")
        require(
            row.get("source_url", "").startswith("https://history.house.gov/"),
            f"Congress {congress} context lacks an official House source.",
        )
        selected[key] = row
    return selected


def read_veto_reference(
    path: Path,
    congresses: tuple[int, ...],
) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    selected_congresses = {str(congress) for congress in congresses}
    selected = {
        row["bill_id"]: row
        for row in rows
        if row.get("bill_id", "").split("-", 1)[0] in selected_congresses
    }
    require(
        len(selected)
        == sum(
            row.get("bill_id", "").split("-", 1)[0] in selected_congresses
            for row in rows
        ),
        f"{path} contains duplicate bill IDs.",
    )
    for bill_id, row in selected.items():
        require(
            re.fullmatch(r"\d+-(?:hr|s)-\d+", bill_id) is not None,
            f"{path} contains an invalid bill ID: {bill_id}",
        )
        require(row.get("veto_overridden") in {"0", "1"}, f"{bill_id} has an invalid override flag.")
        require(
            row.get("veto_kind") in {"regular", "disputed_return_pocket"},
            f"{bill_id} has an invalid veto-kind label.",
        )
        require(
            row.get("source_url", "").startswith("https://www.senate.gov/legislative/vetoes/"),
            f"{bill_id} lacks an official Senate veto source.",
        )
    return selected


def same_party(sponsor_party: str, president_party: str) -> str:
    if sponsor_party not in {"D", "R"}:
        return "NA"
    return "1" if sponsor_party == president_party else "0"


def executive_outcome(row: dict[str, str]) -> str:
    if row.get("vetoed") == "1":
        return "veto_overridden" if row.get("veto_overridden") == "1" else "veto_sustained"
    if row.get("enacted") == "1":
        return "enacted_without_veto"
    return "unresolved_presentment"


def executive_decision_date(row: dict[str, str]) -> str:
    if row.get("vetoed") == "1":
        return row.get("vetoed_date", "")
    return row.get("enacted_date", "")


def source_law_number_status(row: dict[str, str]) -> str:
    numbers = [item.strip() for item in row.get("law_number", "").split(";") if item.strip()]
    if not numbers:
        return "enacted_without_law_number" if row.get("enacted") == "1" else "not_enacted"
    if any(number.split("-", 1)[0] != row["congress"] for number in numbers):
        return "source_cross_congress_number"
    if len(numbers) > 1:
        return "source_multiple_same_congress_numbers"
    return "aligned"


def panel_row(
    row: dict[str, str],
    context: dict[str, str],
    veto_reference: dict[str, dict[str, str]],
) -> dict[str, str]:
    reference = veto_reference.get(row["bill_id"], {})
    result = {
        "bill_id": row["bill_id"],
        "congress": row["congress"],
        "bill_type": row["bill_type"],
        "bill_number": row["bill_number"],
        "origin_chamber": row["origin_chamber"],
        "title": row["title"],
        "policy_area": row["policy_area"],
        "president": context["president"],
        "president_party": context["president_party"],
        "house_majority_party": context["house_majority_party"],
        "senate_majority_party": context["senate_majority_party"],
        "government_control": context["government_control"],
        "sponsor_bioguide_id": row["sponsor_bioguide_id"],
        "sponsor_party": row["sponsor_party"],
        "sponsor_same_party_as_president": same_party(
            row["sponsor_party"], context["president_party"]
        ),
        "presented_to_president_date": row["presented_to_president_date"],
        "presented_to_president_basis": row["presented_to_president_basis"],
        "executive_outcome": executive_outcome(row),
        "executive_decision_date": executive_decision_date(row),
        "veto_kind_reference": reference.get("veto_kind", ""),
        "vetoed": row["vetoed"],
        "vetoed_date": row["vetoed_date"],
        "vetoed_basis": row["vetoed_basis"],
        "veto_overridden": row["veto_overridden"],
        "veto_overridden_date": row["veto_overridden_date"],
        "veto_overridden_basis": row["veto_overridden_basis"],
        "enacted": row["enacted"],
        "enacted_date": row["enacted_date"],
        "enacted_basis": row["enacted_basis"],
        "law_type": row["law_type"],
        "law_number": row["law_number"],
        "source_law_number_status": source_law_number_status(row),
        "recorded_vote_count": row["recorded_vote_count"],
        "actions_count": row["actions_count"],
        "president_action_count": row["president_action_count"],
        "source_xml_update_date": row["source_xml_update_date"],
        "source_xml_sha256": row["source_xml_sha256"],
        "actions_sha256": row["actions_sha256"],
        "source_archive": row["source_archive"],
        "source_url": row["source_url"],
        "classification_version": row["classification_version"],
        "integrity_status": row["integrity_status"],
    }
    return {field: result.get(field, "") for field in FIELDNAMES}


def build_panel(
    archives: list[tuple[int, ArchiveInfo]],
    contexts: dict[str, dict[str, str]],
    veto_reference: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    archive_stats: list[dict[str, str]] = []
    seen: set[str] = set()
    invalid: list[str] = []
    for congress, source in archives:
        parsed = 0
        presentments = 0
        with zipfile.ZipFile(source.path) as archive:
            members = sorted(
                info.filename
                for info in archive.infolist()
                if not info.is_dir() and info.filename.lower().endswith(".xml")
            )
            require(
                len(members) == source.member_count,
                f"{source.path} member count changed during parsing.",
            )
            for member_name in members:
                parsed += 1
                row = parse_bill_xml(
                    archive.read(member_name),
                    source,
                    congress,
                    source.bill_type,
                    member_name,
                )
                require(row["bill_id"] not in seen, f"Duplicate bill identifier: {row['bill_id']}")
                seen.add(row["bill_id"])
                if row["integrity_status"].startswith("invalid:"):
                    invalid.append(f"{row['bill_id']}={row['integrity_status']}")
                if row["presented_to_president"] == "1":
                    rows.append(panel_row(row, contexts[str(congress)], veto_reference))
                    presentments += 1
        archive_stats.append(
            {
                "congress": str(congress),
                "billType": source.bill_type,
                "parsedBills": str(parsed),
                "presentments": str(presentments),
                "sha256": source.sha256,
                "bytes": str(source.byte_count),
                "members": str(source.member_count),
                "latestMemberTimestamp": source.latest_member_timestamp,
                "pinStatus": source.pin_status,
                "url": source.url,
            }
        )
    require(not invalid, f"Lifecycle integrity failures: {', '.join(invalid[:8])}")
    rows.sort(key=bill_sort_key)
    validate_panel(rows, contexts, veto_reference)
    return rows, archive_stats


def validate_panel(
    rows: list[dict[str, str]],
    contexts: dict[str, dict[str, str]],
    veto_reference: dict[str, dict[str, str]],
) -> None:
    require(rows, "Executive-action panel is empty.")
    require(len({row["bill_id"] for row in rows}) == len(rows), "Panel bill IDs are not unique.")
    require(
        {row["congress"] for row in rows} == set(contexts),
        "Panel does not contain at least one decision for every selected Congress.",
    )
    require(
        {row["classification_version"] for row in rows} == {CLASSIFICATION_VERSION},
        "Panel mixes lifecycle-classifier versions.",
    )
    require(
        not any(row["integrity_status"].startswith("invalid:") for row in rows),
        "Panel contains invalid lifecycle rows.",
    )
    require(
        not any(row["executive_outcome"] == "unresolved_presentment" for row in rows),
        "Panel contains presented measures with no classified final executive outcome.",
    )
    observed_vetoes = {row["bill_id"]: row for row in rows if row["vetoed"] == "1"}
    require(
        set(observed_vetoes) == set(veto_reference),
        "Panel veto set differs from the scoped official Senate reference.",
    )
    for bill_id, reference in veto_reference.items():
        observed = observed_vetoes[bill_id]
        require(observed["president"] == reference["president"], f"{bill_id} president differs from reference.")
        require(observed["vetoed_date"] == reference["veto_date"], f"{bill_id} veto date differs from reference.")
        require(
            observed["veto_overridden"] == reference["veto_overridden"],
            f"{bill_id} override result differs from reference.",
        )
        require(
            observed["veto_kind_reference"] == reference["veto_kind"],
            f"{bill_id} veto kind differs from reference.",
        )
    cross_congress_law_numbers = {
        row["bill_id"]
        for row in rows
        if row["source_law_number_status"] == "source_cross_congress_number"
    }
    expected_law_number_anomalies = {
        bill_id
        for bill_id in EXPECTED_SOURCE_CROSS_CONGRESS_LAW_NUMBERS
        if bill_id.split("-", 1)[0] in contexts
    }
    require(
        cross_congress_law_numbers == expected_law_number_anomalies,
        "Source cross-Congress law-number anomaly set drifted.",
    )
    for congress in sorted(contexts, key=int):
        cohort = [row for row in rows if row["congress"] == congress]
        enacted = sum(row["enacted"] == "1" for row in cohort)
        vetoes = sum(row["vetoed"] == "1" for row in cohort)
        overrides = sum(row["veto_overridden"] == "1" for row in cohort)
        require(
            len(cohort) == enacted + vetoes - overrides,
            f"Congress {congress} executive-decision identity failed.",
        )
        require(overrides <= vetoes, f"Congress {congress} has more overrides than vetoes.")


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def configuration_sha256(
    congresses: tuple[int, ...],
    bill_types: tuple[str, ...],
    context_hash: str,
    veto_reference_hash: str,
    lifecycle_builder_hash: str,
) -> str:
    payload = {
        "classificationVersion": CLASSIFICATION_VERSION,
        "congresses": congresses,
        "billTypes": bill_types,
        "contextSha256": context_hash,
        "vetoReferenceSha256": veto_reference_hash,
        "lifecycleBuilderSha256": lifecycle_builder_hash,
        "fieldnames": FIELDNAMES,
    }
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())


def output_cache_matches(
    output: Path,
    metadata: Path,
    config_hash: str,
    code_hash: str,
) -> bool:
    if not output.exists() or not metadata.exists():
        return False
    values = metadata_values(metadata)
    output_hash = values.get("output_sha256", "")
    return (
        values.get("configuration_sha256") == config_hash
        and values.get("panel_builder_sha256") == code_hash
        and len(output_hash) == 64
        and sha256_file(output) == output_hash
    )


def metadata_content(
    rows: list[dict[str, str]],
    archive_stats: list[dict[str, str]],
    output: Path,
    congresses: tuple[int, ...],
    bill_types: tuple[str, ...],
    config_hash: str,
    code_hash: str,
    lifecycle_builder_hash: str,
    context_hash: str,
    veto_reference_hash: str,
) -> str:
    vetoes = sum(row["vetoed"] == "1" for row in rows)
    overrides = sum(row["veto_overridden"] == "1" for row in rows)
    enacted = sum(row["enacted"] == "1" for row in rows)
    lines = [
        "# GovInfo Executive-Action Panel",
        "",
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- classification_version: `{CLASSIFICATION_VERSION}`",
        f"- configuration_sha256: `{config_hash}`",
        f"- panel_builder_sha256: `{code_hash}`",
        f"- lifecycle_builder_sha256: `{lifecycle_builder_hash}`",
        f"- context_sha256: `{context_hash}`",
        f"- veto_reference_sha256: `{veto_reference_hash}`",
        f"- output_sha256: `{sha256_file(output)}`",
        f"- congresses: {','.join(str(item) for item in congresses)}",
        f"- bill_types: {','.join(bill_types)}",
        f"- parsed_bill_records: {sum(int(item['parsedBills']) for item in archive_stats)}",
        f"- executive_decisions: {len(rows)}",
        f"- enacted_rows: {enacted}",
        f"- vetoed_rows: {vetoes}",
        f"- overridden_veto_rows: {overrides}",
        "- unresolved_presentments: 0",
        "- structurally_invalid_rows: 0",
        "",
        "## Source Archives",
        "",
        "| Congress | Type | Bills parsed | Presentments | Bytes | SHA-256 | Latest member timestamp | Pin status | URL |",
        "| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for item in archive_stats:
        lines.append(
            f"| {item['congress']} | `{item['billType']}` | {item['parsedBills']} | "
            f"{item['presentments']} | {item['bytes']} | `{item['sha256']}` | "
            f"{item['latestMemberTimestamp']} | {item['pinStatus']} | {item['url']} |"
        )
    lines.extend(
        [
            "",
            "## Congress Summary",
            "",
            "| Congress | President | Control | Decisions | Vetoes | Overrides | Veto rate |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    by_congress = {str(congress): [] for congress in congresses}
    for row in rows:
        by_congress[row["congress"]].append(row)
    for congress, cohort in by_congress.items():
        cohort_vetoes = sum(row["vetoed"] == "1" for row in cohort)
        cohort_overrides = sum(row["veto_overridden"] == "1" for row in cohort)
        lines.append(
            f"| {congress} | {cohort[0]['president']} | {cohort[0]['government_control']} | "
            f"{len(cohort)} | {cohort_vetoes} | {cohort_overrides} | "
            f"{cohort_vetoes / len(cohort):.6f} |"
        )
    outcome_counts = Counter(row["executive_outcome"] for row in rows)
    source_law_number_anomalies = sorted(
        row["bill_id"]
        for row in rows
        if row["source_law_number_status"] == "source_cross_congress_number"
    )
    lines.extend(
        [
            "",
            "## Operational Definitions",
            "",
            "- Scope is every H.R. and S. XML record in each listed complete GovInfo BILLSTATUS archive. Joint resolutions and other measure types are excluded.",
            "- Only measures classified as presented to the President are retained in the committed panel; all source records are still parsed and integrity-checked.",
            "- Veto and successful-override classifications use the shared lifecycle classifier. Successful override requires affirmative House and Senate evidence.",
            f"- The exact {vetoes}-bill H.R./S. veto set, dates, veto kind, and {overrides} override outcomes match `{VETO_REFERENCE}`, compiled from the official Senate presidential-veto histories.",
            "- Executive decisions equal enactments plus vetoes minus successful overrides. Every Congress must satisfy this identity.",
            f"- Final outcomes: {outcome_counts.get('enacted_without_veto', 0)} enacted without veto; {outcome_counts.get('veto_sustained', 0)} sustained vetoes; {outcome_counts.get('veto_overridden', 0)} successful overrides.",
            f"- Party-control context is pinned in `{CONTEXT}` from the official House history table `Party Government Since 1857`.",
            f"- GovInfo supplies cross-Congress law numbers on {len(source_law_number_anomalies)} enacted source rows ({', '.join(source_law_number_anomalies)}). The panel preserves those values and marks them `source_cross_congress_number` rather than silently correcting official source metadata.",
            "- Record-level source XML and canonical action hashes allow any classified decision to be traced back to the source bytes.",
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--congresses",
        type=parse_congresses,
        default=DEFAULT_CONGRESSES,
        help="Comma-separated Congresses or ranges (default: 108-118).",
    )
    parser.add_argument(
        "--bill-types",
        default=",".join(DEFAULT_BILL_TYPES),
        help="Comma-separated GovInfo bill types (default: hr,s).",
    )
    parser.add_argument("--context", type=Path, default=CONTEXT)
    parser.add_argument("--veto-reference", type=Path, default=VETO_REFERENCE)
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE_DIR)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata-output", type=Path, default=OUT_METADATA)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--allow-unpinned-source", action="store_true")
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    congresses = tuple(args.congresses)
    bill_types = tuple(
        item.strip().lower() for item in args.bill_types.split(",") if item.strip()
    )
    require(bill_types, "At least one bill type is required.")
    require(
        all(re.fullmatch(r"[a-z]+", item) for item in bill_types),
        "Bill types must contain only lowercase letters.",
    )
    contexts = read_context(args.context, congresses)
    veto_reference = read_veto_reference(args.veto_reference, congresses)
    context_hash = sha256_file(args.context)
    veto_reference_hash = sha256_file(args.veto_reference)
    lifecycle_builder = Path(__file__).with_name("build_govinfo_bill_census_dataset.py")
    lifecycle_builder_hash = sha256_file(lifecycle_builder)
    code_hash = sha256_file(Path(__file__))
    config_hash = configuration_sha256(
        congresses,
        bill_types,
        context_hash,
        veto_reference_hash,
        lifecycle_builder_hash,
    )
    if (
        not args.refresh
        and not args.rebuild
        and output_cache_matches(args.output, args.metadata_output, config_hash, code_hash)
    ):
        print(f"Using matching output cache {args.output}")
        return 0

    archives: list[tuple[int, ArchiveInfo]] = []
    for congress in congresses:
        for bill_type in bill_types:
            path = args.archive_dir / archive_name(congress, bill_type)
            if args.refresh or not path.exists():
                if args.offline:
                    raise SystemExit(f"Offline mode requires cached archive {path}")
                print(f"Downloading {archive_url(congress, bill_type)}")
                download_archive(
                    archive_url(congress, bill_type),
                    path,
                    max(1, args.retries),
                    args.timeout,
                )
            archives.append(
                (
                    congress,
                    archive_info(
                        congress,
                        bill_type,
                        path,
                        args.allow_unpinned_source,
                    ),
                )
            )

    rows, archive_stats = build_panel(archives, contexts, veto_reference)
    write_csv(rows, args.output)
    metadata = metadata_content(
        rows,
        archive_stats,
        args.output,
        congresses,
        bill_types,
        config_hash,
        code_hash,
        lifecycle_builder_hash,
        context_hash,
        veto_reference_hash,
    )
    write_reproducible_metadata(args.metadata_output, metadata)
    print(f"Wrote {args.output} ({len(rows)} executive decisions)")
    print(f"Wrote {args.metadata_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
