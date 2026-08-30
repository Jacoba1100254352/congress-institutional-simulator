#!/usr/bin/env python3
"""Write a temporal triage report for court/public-law review tasks."""

from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path


COURT_PUBLIC_LAW_REVIEW_QUEUE = Path("reports/court-public-law-review-queue.csv")
BILL_LAW_SPINE = Path("reports/bill-law-evidence-spine.csv")
OUT_CSV = Path("reports/court-public-law-temporal-triage.csv")
OUT_MD = Path("reports/court-public-law-temporal-triage.md")

FIELDNAMES = [
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
    "temporal_status",
    "direct_review_status_after_temporal_screen",
    "next_review_action",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Temporal triage only; rows compare SCDB decision dates to cached "
    "Congress.gov public-law enacted dates. A pre-enactment decision date rules "
    "out direct review of the listed public law, but the screen does not prove "
    "direct review for post-enactment rows and does not resolve older statutory "
    "lineage, codification, emergency-order, lower-court, causal-effect, "
    "welfare, or model-validation claims."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def spine_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["bill_id"]: row for row in rows if row.get("bill_id")}


def temporal_result(decision: date | None, enacted: date | None) -> tuple[str, str, str, str]:
    if not decision or not enacted:
        return (
            "missing_date_needs_source_review",
            "date_screen_inconclusive",
            "",
            "Fill missing decision or enacted date before direct-review coding.",
        )
    days = (decision - enacted).days
    if days < 0:
        return (
            "pre_enactment_impossible_direct_review_of_listed_public_law",
            "temporally_excluded_for_listed_public_law",
            str(days),
            "Do not code as direct review of this public law; reserve review only for older statute or codification-lineage questions.",
        )
    return (
        "post_enactment_possible_needs_direct_source_review",
        "post_enactment_source_review_needed",
        str(days),
        "Review the Supreme Court opinion or syllabus, cited-statute table, public-law text, and authority document for a direct link.",
    )


def build_rows() -> list[dict[str, str]]:
    queue_rows = read_csv(COURT_PUBLIC_LAW_REVIEW_QUEUE)
    spine = spine_by_bill(read_csv(BILL_LAW_SPINE))
    output: list[dict[str, str]] = []
    for queue_row in queue_rows:
        bill_id = queue_row.get("bill_id", "").strip()
        spine_row = spine.get(bill_id, {})
        decision = parse_date(queue_row.get("decision_date", ""))
        enacted = parse_date(spine_row.get("enacted_date", ""))
        temporal_status, direct_status, days_after, next_action = temporal_result(decision, enacted)
        output.append({
            "triage_rank": "0",
            "review_queue_rank": queue_row.get("review_queue_rank", ""),
            "bill_id": bill_id,
            "public_law_number": queue_row.get("public_law_number", ""),
            "case_id": queue_row.get("case_id", ""),
            "case_name": queue_row.get("case_name", ""),
            "decision_date": queue_row.get("decision_date", ""),
            "enacted_date": spine_row.get("enacted_date", ""),
            "days_after_enactment": days_after,
            "matched_usc_sections": queue_row.get("matched_usc_sections", ""),
            "temporal_status": temporal_status,
            "direct_review_status_after_temporal_screen": direct_status,
            "next_review_action": next_action,
            "evidence_layers": (
                "court_public_law_review_queue; public_law_enacted_date_metadata; "
                "court_public_law_temporal_triage"
            ),
            "missing_links": (
                "direct_case_to_public_law_identifier; direct_case_to_bill_identifier; "
                "reviewed_case_disposition_to_public_law; codified_usc_lineage; "
                "emergency_order_dataset; lower_court_history; causal_invalidation_effect; "
                "model_validation"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    output.sort(
        key=lambda row: (
            row["temporal_status"] != "post_enactment_possible_needs_direct_source_review",
            int(row["review_queue_rank"] or "999999"),
            row["case_id"],
            row["public_law_number"],
            row["bill_id"],
        )
    )
    for rank, row in enumerate(output, start=1):
        row["triage_rank"] = str(rank)
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["temporal_status"]] = status_counts.get(row["temporal_status"], 0) + 1
    post_rows = [
        row for row in rows
        if row["temporal_status"] == "post_enactment_possible_needs_direct_source_review"
    ]
    lines = [
        "# Court/Public-Law Temporal Triage",
        "",
        "This report applies a date screen to the court/public-law review queue. It does not prove direct court review.",
        "",
        f"- Triage rows: {len(rows)}",
        "- Pre-enactment rows ruled out as direct review of the listed public law: "
        f"{status_counts.get('pre_enactment_impossible_direct_review_of_listed_public_law', 0)}",
        "- Post-enactment rows still needing source review: "
        f"{status_counts.get('post_enactment_possible_needs_direct_source_review', 0)}",
        "- Missing-date rows needing source review: "
        f"{status_counts.get('missing_date_needs_source_review', 0)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "## Post-Enactment Review Tasks",
        "",
        "| Triage rank | Queue rank | Case | Public law | Bill | Decision | Enacted | Days after enactment | U.S.C. section |",
        "| ---: | ---: | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    if post_rows:
        for row in post_rows:
            lines.append(
                f"| {row['triage_rank']} | {row['review_queue_rank']} | "
                f"`{row['case_id']}` {row['case_name']} | `{row['public_law_number']}` | "
                f"`{row['bill_id']}` | {row['decision_date']} | {row['enacted_date']} | "
                f"{row['days_after_enactment']} | {row['matched_usc_sections'] or '---'} |"
            )
    else:
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    lines.extend([
        "",
        "## Status Counts",
        "",
        "| Temporal status | Rows |",
        "| --- | ---: |",
    ])
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(
            "No temporal triage rows; run make court-public-law-review-queue first."
        )
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
