#!/usr/bin/env python3
"""Check readiness of optional raw empirical validation inputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


RAW_DIR = Path("data/validation/raw")
REPORT = Path("reports/empirical-validation-readiness.md")


@dataclass(frozen=True)
class DatasetSpec:
    file_name: str
    purpose: str
    required_columns: tuple[str, ...]


DATASETS = [
    DatasetSpec(
        "voteview_rollcalls.csv",
        "party unity, coalition size, and ideological voting checks",
        ("congress", "party", "vote_id", "vote", "ideology"),
    ),
    DatasetSpec(
        "bill_progression.csv",
        "bill attrition, floor load, and enactment-rate checks",
        ("bill_id", "introduced", "committee_reported", "floor_considered", "enacted"),
    ),
    DatasetSpec(
        "lobbying_disclosure.csv",
        "lobby spending distribution and issue-pressure checks",
        ("client", "issue", "amount", "period"),
    ),
    DatasetSpec(
        "topic_throughput.csv",
        "topic-level throughput and agenda distribution checks",
        ("topic", "introduced", "floor_considered", "enacted"),
    ),
    DatasetSpec(
        "sponsor_success.csv",
        "sponsor success and proposal-access concentration checks",
        ("sponsor_id", "party", "introduced", "enacted"),
    ),
    DatasetSpec(
        "district_public_opinion.csv",
        "district-level public will, issue intensity, turnout, and affected-group checks",
        ("district_id", "issue", "support", "intensity", "turnout", "affected_group_share"),
    ),
    DatasetSpec(
        "committee_activity.csv",
        "committee referral, hearing, reporting, amendment, and discharge checks",
        ("committee", "issue", "referred", "hearings", "reported", "amendments", "discharged"),
    ),
    DatasetSpec(
        "campaign_finance.csv",
        "campaign-finance and outside-spending influence checks",
        ("cycle", "recipient", "industry", "amount", "independent_expenditure"),
    ),
    DatasetSpec(
        "court_review.csv",
        "constitutional review, emergency docket, signed-opinion, and invalidation checks",
        ("case_id", "issue", "emergency_order", "invalidated", "vote_margin", "signed_opinion"),
    ),
    DatasetSpec(
        "comparative_institutions.csv",
        "cross-national chamber, court, party-system, and productivity checks",
        ("country", "year", "chambers", "district_magnitude", "judicial_review", "party_fragmentation", "legislative_productivity"),
    ),
]


def columns(path: Path) -> set[str]:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return set()
    return {column.strip() for column in header}


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Empirical Validation Readiness",
        "",
        "This report checks whether optional raw empirical inputs are present and shaped for future validation. It is a readiness check, not a validation result.",
        "",
        "| Dataset | Purpose | Status | Missing columns |",
        "| --- | --- | --- | --- |",
    ]
    present = 0
    complete = 0
    for spec in DATASETS:
        path = RAW_DIR / spec.file_name
        if not path.exists():
            lines.append(f"| `{spec.file_name}` | {spec.purpose} | missing | all |")
            continue
        present += 1
        found_columns = columns(path)
        missing = [column for column in spec.required_columns if column not in found_columns]
        if missing:
            lines.append(f"| `{spec.file_name}` | {spec.purpose} | incomplete | {', '.join(missing)} |")
        else:
            complete += 1
            lines.append(f"| `{spec.file_name}` | {spec.purpose} | ready | none |")

    lines.extend([
        "",
        f"- Files present: {present} / {len(DATASETS)}",
        f"- Files with required columns: {complete} / {len(DATASETS)}",
        "",
        "Next empirical step: add curated raw files and document source-specific transformations. The adapters now cover roll calls, bill progress, lobbying, topics, sponsor success, district opinion, committee activity, campaign finance, court review, and comparative institutions.",
    ])
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
