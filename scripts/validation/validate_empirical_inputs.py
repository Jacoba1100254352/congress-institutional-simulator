#!/usr/bin/env python3
"""Check readiness of optional raw empirical validation inputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


RAW_DIR = Path("data/validation/raw")
FIXTURE_DIR = Path("data/validation/fixtures")
REPORT = Path("reports/empirical-validation-readiness.md")
REPORT_CSV = Path("reports/empirical-validation-readiness.csv")


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
        "bounded Congress.gov bill-flow and independent source-cross-check rows",
        ("bill_id", "introduced", "committee_reported", "floor_considered", "enacted"),
    ),
    DatasetSpec(
        "govinfo_bill_census_116.csv",
        "complete 116th-Congress no-refit temporal bill-lifecycle backcast",
        (
            "bill_id",
            "introduced",
            "committee_ordered_reported",
            "committee_reported",
            "committee_advanced",
            "floor_considered",
            "passed_origin_chamber",
            "completed_congressional_passage",
            "presented_to_president",
            "vetoed",
            "veto_overridden",
            "enacted",
            "actions_count",
            "source_xml_sha256",
            "actions_sha256",
            "classification_version",
            "integrity_status",
        ),
    ),
    DatasetSpec(
        "govinfo_bill_census.csv",
        "117th-Congress calibration and within-Congress bill-lifecycle checks",
        (
            "bill_id",
            "introduced",
            "committee_ordered_reported",
            "committee_reported",
            "committee_advanced",
            "floor_considered",
            "passed_origin_chamber",
            "completed_congressional_passage",
            "presented_to_president",
            "vetoed",
            "veto_overridden",
            "enacted",
            "actions_count",
            "source_xml_sha256",
            "actions_sha256",
            "integrity_status",
        ),
    ),
    DatasetSpec(
        "govinfo_bill_census_118.csv",
        "complete 118th-Congress no-refit temporal bill-lifecycle test",
        (
            "bill_id",
            "introduced",
            "committee_ordered_reported",
            "committee_reported",
            "committee_advanced",
            "floor_considered",
            "passed_origin_chamber",
            "completed_congressional_passage",
            "presented_to_president",
            "vetoed",
            "veto_overridden",
            "enacted",
            "actions_count",
            "source_xml_sha256",
            "actions_sha256",
            "classification_version",
            "integrity_status",
        ),
    ),
    DatasetSpec(
        "govinfo_executive_action_panel.csv",
        "108th-118th-Congress presidential-decision mechanism diagnostic",
        (
            "bill_id",
            "congress",
            "president",
            "president_party",
            "government_control",
            "sponsor_party",
            "sponsor_same_party_as_president",
            "presented_to_president_date",
            "executive_outcome",
            "vetoed",
            "veto_overridden",
            "enacted",
            "source_xml_sha256",
            "actions_sha256",
            "classification_version",
            "integrity_status",
        ),
    ),
    DatasetSpec(
        "govinfo_joint_resolution_panel.csv",
        "separate 108th-118th-Congress joint-resolution presidential decisions",
        (
            "bill_id",
            "congress",
            "bill_type",
            "president",
            "president_party",
            "government_control",
            "presented_to_president_date",
            "executive_outcome",
            "veto_date_reference",
            "veto_date_alignment",
            "vetoed",
            "veto_overridden",
            "enacted",
            "source_xml_sha256",
            "actions_sha256",
            "classification_version",
            "integrity_status",
        ),
    ),
    DatasetSpec(
        "govinfo_final_chamber_vote_panel.csv",
        "final House and Senate approval support for all retained presidential decisions",
        (
            "bill_id",
            "congress",
            "bill_type",
            "measure_class",
            "president_party",
            "executive_outcome",
            "vetoed",
            "chamber",
            "selection_status",
            "selection_category",
            "action_date",
            "source_url",
            "official_source_status",
            "official_source_sha256",
            "official_source_bill_match_status",
            "yea_count",
            "nay_count",
            "support_share",
            "president_party_support_share",
            "opposition_party_support_share",
            "decision_source_xml_sha256",
            "decision_actions_sha256",
            "selection_classifier_version",
            "integrity_status",
        ),
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
        "rulemaking_implementation.csv",
        "post-enactment implementation delay, enforcement capacity, comment, and nonenforcement checks",
        ("law_id", "proposed_rule_date", "final_rule_date", "effective_date", "comment_count", "enforcement_capacity", "nonenforced", "underfunded"),
    ),
    DatasetSpec(
        "law_revision_history.csv",
        "law revision text flags and optional invalidation-linkage checks",
        ("law_id", "enacted_date", "amended", "reauthorized", "repealed", "expired", "invalidated"),
    ),
    DatasetSpec(
        "comparative_institutions.csv",
        "cross-national chamber, court, party-system, and legislative-capacity checks",
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
    output_rows: list[dict[str, str]] = []
    lines = [
        "# Empirical Validation Readiness",
        "",
        "This report checks whether optional raw empirical inputs are present and shaped for future validation. It is a readiness check, not a validation result. Adapter fixtures under `data/validation/fixtures/` are intentionally ignored.",
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
            output_rows.append({
                "dataset": spec.file_name,
                "purpose": spec.purpose,
                "status": "missing",
                "missingColumns": "all",
                "requiredColumns": ",".join(spec.required_columns),
            })
            continue
        present += 1
        found_columns = columns(path)
        missing = [column for column in spec.required_columns if column not in found_columns]
        if missing:
            lines.append(f"| `{spec.file_name}` | {spec.purpose} | incomplete | {', '.join(missing)} |")
            output_rows.append({
                "dataset": spec.file_name,
                "purpose": spec.purpose,
                "status": "incomplete",
                "missingColumns": ",".join(missing),
                "requiredColumns": ",".join(spec.required_columns),
            })
        else:
            complete += 1
            lines.append(f"| `{spec.file_name}` | {spec.purpose} | ready | none |")
            output_rows.append({
                "dataset": spec.file_name,
                "purpose": spec.purpose,
                "status": "ready",
                "missingColumns": "",
                "requiredColumns": ",".join(spec.required_columns),
            })

    fixture_count = len([path for path in FIXTURE_DIR.glob("*.csv") if path.is_file()]) if FIXTURE_DIR.exists() else 0
    lines.extend([
        "",
        f"- Files present: {present} / {len(DATASETS)}",
        f"- Files with required columns: {complete} / {len(DATASETS)}",
        f"- Adapter fixture CSVs ignored: {fixture_count}",
        "",
        "Next empirical step: implement the locked low-event presidential-choice estimator, loss, and whole-Congress temporal tests without post-fit changes while continuing to upgrade bounded source-family checks into linked bill-topic, sponsor, finance, implementation, court, and statutory-lineage evidence. The configured datasets cover roll calls, bounded Congress.gov bill progress, three complete GovInfo lifecycle censuses, separate 108th-118th-Congress bill and joint-resolution decision panels, final chamber-vote support, lobbying, topics, sponsor success, district opinion, committee activity, campaign finance, court review, post-enactment implementation, law revision, and comparative institutions.",
    ])
    REPORT.write_text("\n".join(lines) + "\n")
    with REPORT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["dataset", "purpose", "status", "missingColumns", "requiredColumns"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Wrote {REPORT}")
    print(f"Wrote {REPORT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
