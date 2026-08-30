#!/usr/bin/env python3
"""Write source-reviewed court/public-law direct-review dispositions."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


TEMPORAL_TRIAGE = Path("reports/court-public-law-temporal-triage.csv")
RAW_REVIEW = Path("data/validation/raw/court_public_law_direct_review.csv")
OUT_CSV = Path("reports/court-public-law-direct-review.csv")
OUT_MD = Path("reports/court-public-law-direct-review.md")

POST_ENACTMENT_STATUS = "post_enactment_possible_needs_direct_source_review"
PRE_ENACTMENT_STATUS = "pre_enactment_impossible_direct_review_of_listed_public_law"
MISSING_DATE_STATUS = "missing_date_needs_source_review"

FIELDNAMES = [
    "review_rank",
    "triage_rank",
    "review_queue_rank",
    "bill_id",
    "public_law_number",
    "case_id",
    "case_name",
    "decision_date",
    "enacted_date",
    "days_after_enactment",
    "matched_usc_sections",
    "direct_review_determination",
    "direct_case_to_public_law_identifier",
    "direct_case_to_bill_identifier",
    "reviewed_case_disposition_to_public_law",
    "usc_section_relationship",
    "case_source_url",
    "public_law_source_url",
    "case_source_summary",
    "public_law_source_summary",
    "source_review_notes",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Source-reviewed direct-review disposition only; rows classify whether "
    "a queued SCDB/public-law overlap has direct source evidence that the case "
    "reviewed the listed public law or bill. The artifact does not create "
    "lower-court, emergency-order, causal-invalidation-effect, welfare, "
    "implementation-outcome, or model-validation evidence."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("case_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("bill_id", "").strip(),
    )


def reviewed_keys(raw_rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in raw_rows:
        row_key = key(row)
        if row_key in result:
            raise SystemExit(f"Duplicate direct-review source row for {row_key}.")
        result[row_key] = row
    return result


def pre_enactment_row(triage_row: dict[str, str]) -> dict[str, str]:
    return {
        "direct_review_determination": "temporally_excluded_before_public_law_enactment",
        "direct_case_to_public_law_identifier": "0",
        "direct_case_to_bill_identifier": "0",
        "reviewed_case_disposition_to_public_law": "0",
        "usc_section_relationship": "temporal_exclusion",
        "case_source_url": "",
        "public_law_source_url": "",
        "case_source_summary": "",
        "public_law_source_summary": "",
        "source_review_notes": (
            "Decision date predates the listed public law enactment date, so this "
            "row is excluded as direct review of that public law without manual "
            "opinion review."
        ),
    }


def missing_date_row(triage_row: dict[str, str]) -> dict[str, str]:
    return {
        "direct_review_determination": "missing_date_source_review_needed",
        "direct_case_to_public_law_identifier": "0",
        "direct_case_to_bill_identifier": "0",
        "reviewed_case_disposition_to_public_law": "0",
        "usc_section_relationship": "date_screen_inconclusive",
        "case_source_url": "",
        "public_law_source_url": "",
        "case_source_summary": "",
        "public_law_source_summary": "",
        "source_review_notes": (
            "Decision or enactment date is missing; source review is still needed "
            "before any direct-review disposition can be assigned."
        ),
    }


def reviewed_row(triage_row: dict[str, str], raw_row: dict[str, str]) -> dict[str, str]:
    return {
        "direct_review_determination": raw_row.get("review_status", "").strip(),
        "direct_case_to_public_law_identifier": raw_row.get("direct_case_to_public_law_identifier", "").strip(),
        "direct_case_to_bill_identifier": raw_row.get("direct_case_to_bill_identifier", "").strip(),
        "reviewed_case_disposition_to_public_law": raw_row.get("reviewed_case_disposition_to_public_law", "").strip(),
        "usc_section_relationship": raw_row.get("usc_section_relationship", "").strip(),
        "case_source_url": raw_row.get("case_source_url", "").strip(),
        "public_law_source_url": raw_row.get("public_law_source_url", "").strip(),
        "case_source_summary": raw_row.get("case_source_summary", "").strip(),
        "public_law_source_summary": raw_row.get("public_law_source_summary", "").strip(),
        "source_review_notes": raw_row.get("source_review_notes", "").strip(),
    }


def disposition_for(
    triage_row: dict[str, str],
    raw_by_key: dict[tuple[str, str, str], dict[str, str]],
) -> dict[str, str]:
    status = triage_row.get("temporal_status", "").strip()
    if status == PRE_ENACTMENT_STATUS:
        return pre_enactment_row(triage_row)
    if status == MISSING_DATE_STATUS:
        return missing_date_row(triage_row)
    if status != POST_ENACTMENT_STATUS:
        raise SystemExit(f"Unknown temporal status for {key(triage_row)}: {status}")

    raw_row = raw_by_key.get(key(triage_row))
    if not raw_row:
        raise SystemExit(
            f"Post-enactment court/public-law row needs source review: {key(triage_row)}"
        )
    return reviewed_row(triage_row, raw_row)


def build_rows() -> list[dict[str, str]]:
    triage_rows = read_csv(TEMPORAL_TRIAGE)
    raw_rows = read_csv(RAW_REVIEW)
    if not triage_rows:
        raise SystemExit("No temporal triage rows; run make court-public-law-temporal-triage first.")
    raw_by_key = reviewed_keys(raw_rows)
    required_raw_keys = {
        key(row) for row in triage_rows
        if row.get("temporal_status", "").strip() == POST_ENACTMENT_STATUS
    }
    raw_keys = set(raw_by_key)
    if raw_keys != required_raw_keys:
        raise SystemExit(
            "Direct-review source rows must match post-enactment temporal-triage rows: "
            f"missing={sorted(required_raw_keys - raw_keys)}, extra={sorted(raw_keys - required_raw_keys)}"
        )

    output: list[dict[str, str]] = []
    for triage_row in triage_rows:
        disposition = disposition_for(triage_row, raw_by_key)
        output.append({
            "review_rank": "0",
            "triage_rank": triage_row.get("triage_rank", "").strip(),
            "review_queue_rank": triage_row.get("review_queue_rank", "").strip(),
            "bill_id": triage_row.get("bill_id", "").strip(),
            "public_law_number": triage_row.get("public_law_number", "").strip(),
            "case_id": triage_row.get("case_id", "").strip(),
            "case_name": triage_row.get("case_name", "").strip(),
            "decision_date": triage_row.get("decision_date", "").strip(),
            "enacted_date": triage_row.get("enacted_date", "").strip(),
            "days_after_enactment": triage_row.get("days_after_enactment", "").strip(),
            "matched_usc_sections": triage_row.get("matched_usc_sections", "").strip(),
            "direct_review_determination": disposition["direct_review_determination"],
            "direct_case_to_public_law_identifier": disposition["direct_case_to_public_law_identifier"],
            "direct_case_to_bill_identifier": disposition["direct_case_to_bill_identifier"],
            "reviewed_case_disposition_to_public_law": disposition["reviewed_case_disposition_to_public_law"],
            "usc_section_relationship": disposition["usc_section_relationship"],
            "case_source_url": disposition["case_source_url"],
            "public_law_source_url": disposition["public_law_source_url"],
            "case_source_summary": disposition["case_source_summary"],
            "public_law_source_summary": disposition["public_law_source_summary"],
            "source_review_notes": disposition["source_review_notes"],
            "evidence_layers": (
                "court_public_law_temporal_triage; "
                "court_public_law_direct_review_disposition"
            ),
            "missing_links": (
                "direct_case_to_public_law_identifier; direct_case_to_bill_identifier; "
                "codified_usc_lineage; emergency_order_dataset; lower_court_history; "
                "causal_invalidation_effect; implementation_outcome; model_validation"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    output.sort(key=lambda row: int(row["triage_rank"] or "999999"))
    for rank, row in enumerate(output, start=1):
        row["review_rank"] = str(rank)
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_decision_date(value: str) -> date | None:
    try:
        month, day, year = (int(part) for part in value.split("/"))
        return date(year, month, day)
    except (TypeError, ValueError):
        return None


def write_markdown(rows: list[dict[str, str]]) -> None:
    direct_rows = [
        row for row in rows
        if row["direct_review_determination"] == "reviewed_direct_public_law_review"
    ]
    reviewed_not_direct = [
        row for row in rows
        if row["direct_review_determination"] == "reviewed_not_direct_public_law_review"
    ]
    temporal_exclusions = [
        row for row in rows
        if row["direct_review_determination"] == "temporally_excluded_before_public_law_enactment"
    ]
    remaining = [
        row for row in rows
        if row["direct_review_determination"] == "missing_date_source_review_needed"
    ]
    source_reviewed = [
        row for row in rows
        if row["direct_review_determination"].startswith("reviewed_")
    ]

    lines = [
        "# Court/Public-Law Direct Review Dispositions",
        "",
        "This report records source-reviewed direct-review dispositions for the court/public-law review queue. It is not model-validation evidence.",
        "",
        f"- Disposition rows: {len(rows)}",
        f"- Temporally excluded rows: {len(temporal_exclusions)}",
        f"- Source-reviewed post-enactment rows: {len(source_reviewed)}",
        f"- Direct public-law review rows: {len(direct_rows)}",
        f"- Source-reviewed not-direct rows: {len(reviewed_not_direct)}",
        f"- Remaining source-review-needed rows: {len(remaining)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "## Source-Reviewed Rows",
        "",
        "| Review rank | Case | Public law | Bill | Determination | U.S.C. relationship | Notes |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    if source_reviewed:
        for row in source_reviewed:
            lines.append(
                f"| {row['review_rank']} | `{row['case_id']}` {row['case_name']} | "
                f"`{row['public_law_number']}` | `{row['bill_id']}` | "
                f"`{row['direct_review_determination']}` | "
                f"`{row['usc_section_relationship']}` | {row['source_review_notes']} |"
            )
    else:
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")

    lines.extend([
        "",
        "## Source Evidence",
        "",
        "| Case | Case source | Public-law source | Case source summary | Public-law source summary |",
        "| --- | --- | --- | --- | --- |",
    ])
    if source_reviewed:
        for row in source_reviewed:
            case_source = row["case_source_url"] or "---"
            public_law_source = row["public_law_source_url"] or "---"
            lines.append(
                f"| `{row['case_id']}` {row['case_name']} | {case_source} | "
                f"{public_law_source} | {row.get('case_source_summary', '---') or '---'} | "
                f"{row.get('public_law_source_summary', '---') or '---'} |"
            )
    else:
        lines.append("| --- | --- | --- | --- | --- |")

    temporal_groups: dict[tuple[str, str], dict[str, object]] = {}
    for row in temporal_exclusions:
        group_key = (row["public_law_number"], row["bill_id"])
        group = temporal_groups.setdefault(
            group_key,
            {
                "rows": 0,
                "cases": set(),
                "sections": set(),
                "first_decision": "",
                "first_decision_sort": None,
                "last_decision": "",
                "last_decision_sort": None,
            },
        )
        group["rows"] = int(group["rows"]) + 1
        group["cases"].add(row["case_id"])  # type: ignore[union-attr]
        for section in row["matched_usc_sections"].split(";"):
            if section.strip():
                group["sections"].add(section.strip())  # type: ignore[union-attr]
        decision = row["decision_date"]
        decision_sort = parse_decision_date(decision)
        if decision_sort:
            first_sort = group["first_decision_sort"]
            last_sort = group["last_decision_sort"]
            if first_sort is None or decision_sort < first_sort:
                group["first_decision"] = decision
                group["first_decision_sort"] = decision_sort
            if last_sort is None or decision_sort > last_sort:
                group["last_decision"] = decision
                group["last_decision_sort"] = decision_sort

    lines.extend([
        "",
        "## Temporal Exclusion Summary",
        "",
        "Pre-enactment rows are ruled out only as direct review of the listed 117th Congress public law. This does not rule out older statutory-lineage relationships to the same U.S.C. section.",
        "",
        "| Public law | Bill | Excluded rows | Unique cases | U.S.C. sections | Decision range |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ])
    for (public_law, bill_id), group in sorted(temporal_groups.items()):
        cases = group["cases"]
        sections = group["sections"]
        decision_range = (
            f"{group['first_decision']}..{group['last_decision']}"
            if group["first_decision"] and group["last_decision"]
            else "---"
        )
        lines.append(
            f"| `{public_law}` | `{bill_id}` | {group['rows']} | "
            f"{len(cases)} | {'; '.join(sorted(sections)) or '---'} | {decision_range} |"
        )

    lines.extend([
        "",
        "## Determination Counts",
        "",
        "| Determination | Rows |",
        "| --- | ---: |",
    ])
    counts: dict[str, int] = {}
    for row in rows:
        determination = row["direct_review_determination"]
        counts[determination] = counts.get(determination, 0) + 1
    for determination, count in sorted(counts.items()):
        lines.append(f"| `{determination}` | {count} |")

    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
