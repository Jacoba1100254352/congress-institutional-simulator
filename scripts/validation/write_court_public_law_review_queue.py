#!/usr/bin/env python3
"""Write a court/public-law direct-review work queue from overlap metadata."""

from __future__ import annotations

import csv
from pathlib import Path


COURT_LAW_LINKAGE = Path("reports/court-law-linkage.csv")
BILL_LAW_LIFECYCLE_READINESS = Path("reports/bill-law-lifecycle-readiness.csv")
OUT_CSV = Path("reports/court-public-law-review-queue.csv")
OUT_MD = Path("reports/court-public-law-review-queue.md")

FIELDNAMES = [
    "review_queue_rank",
    "lifecycle_review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "case_id",
    "case_name",
    "term",
    "decision_date",
    "matched_usc_sections",
    "court_usc_sections",
    "authority_document_numbers",
    "authority_agencies",
    "scdb_invalidated",
    "signed_opinion",
    "vote_margin",
    "direct_review_status",
    "review_question",
    "review_search_terms",
    "review_sources_needed",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Court/public-law review queue only; rows are generated from SCDB lawMinor "
    "U.S.C.-section overlaps with Federal Register authority citations attached "
    "to cached public-law rows. The queue does not prove that the case directly "
    "challenged, reviewed, interpreted, or invalidated the listed public law, "
    "bill, agency rule, or implementation chain, and it is not emergency-order, "
    "lower-court, causal-effect, welfare, or model-validation evidence."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def lifecycle_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["bill_id"]: row for row in rows if row.get("bill_id")}


def search_terms(row: dict[str, str], public_law: str, bill_id: str) -> str:
    terms = [
        f'"{row.get("case_name", "").strip()}"',
        f'"{public_law}"',
        f'"{bill_id}"',
    ]
    for section in split_values(row.get("matched_usc_sections", ""))[:3]:
        terms.append(f'"{section}"')
    return " ".join(term for term in terms if term != '""')


def review_question(row: dict[str, str], public_law: str, bill_id: str) -> str:
    sections = row.get("matched_usc_sections", "") or row.get("court_usc_sections", "")
    return (
        f"Does SCDB case {row.get('case_id', '')} directly challenge, review, "
        f"interpret, or invalidate public law {public_law} / {bill_id}, or does "
        f"it only share U.S.C. section metadata ({sections}) with Federal Register "
        "authority citations?"
    )


def build_rows() -> list[dict[str, str]]:
    court_rows = [
        row for row in read_csv(COURT_LAW_LINKAGE)
        if row.get("linkage_status") == "usc_section_authority_overlap"
    ]
    lifecycle = lifecycle_by_bill(read_csv(BILL_LAW_LIFECYCLE_READINESS))
    output: list[dict[str, str]] = []
    for row in court_rows:
        public_laws = split_values(row.get("public_law_numbers", ""))
        bill_ids = split_values(row.get("bill_ids", ""))
        if not public_laws:
            public_laws = [""]
        if not bill_ids:
            bill_ids = [""]
        for public_law in public_laws:
            matching_bill_ids = [
                bill_id for bill_id in bill_ids
                if lifecycle.get(bill_id, {}).get("public_law_number", "") == public_law
            ]
            if not matching_bill_ids:
                matching_bill_ids = bill_ids
            for bill_id in matching_bill_ids:
                lifecycle_row = lifecycle.get(bill_id, {})
                output.append({
                    "review_queue_rank": "0",
                    "lifecycle_review_rank": lifecycle_row.get("review_priority_rank", ""),
                    "bill_id": bill_id,
                    "public_law_number": public_law,
                    "policy_area": lifecycle_row.get("policy_area", ""),
                    "case_id": row.get("case_id", ""),
                    "case_name": row.get("case_name", ""),
                    "term": row.get("term", ""),
                    "decision_date": row.get("decision_date", ""),
                    "matched_usc_sections": row.get("matched_usc_sections", ""),
                    "court_usc_sections": row.get("court_usc_sections", ""),
                    "authority_document_numbers": row.get("authority_document_numbers", ""),
                    "authority_agencies": row.get("authority_agencies", ""),
                    "scdb_invalidated": row.get("invalidated", ""),
                    "signed_opinion": row.get("signed_opinion", ""),
                    "vote_margin": row.get("vote_margin", ""),
                    "direct_review_status": "needs_direct_case_to_public_law_review",
                    "review_question": review_question(row, public_law, bill_id),
                    "review_search_terms": search_terms(row, public_law, bill_id),
                    "review_sources_needed": (
                        "SCDB case row; Supreme Court opinion or syllabus; cited-statute table; "
                        "Federal Register authority document; public-law text"
                    ),
                    "evidence_layers": (
                        "scdb_law_minor_usc_section; federal_register_authority_usc_overlap; "
                        "public_law_bill_metadata; court_public_law_review_queue"
                    ),
                    "missing_links": (
                        "direct_case_to_public_law_identifier; direct_case_to_bill_identifier; "
                        "direct_case_to_rule_or_agency_docket; merits_record_statute_disposition_review; "
                        "emergency_order_dataset; lower_court_history; causal_invalidation_effect; "
                        "model_validation"
                    ),
                    "claim_boundary": CLAIM_BOUNDARY,
                })
    output.sort(
        key=lambda item: (
            int(item["lifecycle_review_rank"] or "999999"),
            item["case_id"],
            item["public_law_number"],
            item["bill_id"],
        )
    )
    for rank, row in enumerate(output, start=1):
        row["review_queue_rank"] = str(rank)
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    bills = {row["bill_id"] for row in rows if row["bill_id"]}
    cases = {row["case_id"] for row in rows if row["case_id"]}
    sections = {
        section
        for row in rows
        for section in split_values(row.get("matched_usc_sections", ""))
    }
    invalidated = sum(1 for row in rows if row["scdb_invalidated"] == "1")
    lines = [
        "# Court/Public-Law Review Queue",
        "",
        "This report turns the bounded court-law U.S.C.-section overlap cache into direct-review tasks. It is not direct court-review evidence.",
        "",
        f"- Review rows: {len(rows)}",
        f"- Unique SCDB cases: {len(cases)}",
        f"- Public laws needing direct review: {len(public_laws)}",
        f"- Bill IDs needing direct review: {len(bills)}",
        f"- Matched U.S.C. sections: {len(sections)}",
        f"- Rows coded invalidated by SCDB: {invalidated}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Case | Public law | Bill | U.S.C. section | Direct-review status |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows[:60]:
        lines.append(
            f"| {row['review_queue_rank']} | `{row['case_id']}` {row['case_name']} | "
            f"`{row['public_law_number']}` | `{row['bill_id']}` | "
            f"{row['matched_usc_sections'] or row['court_usc_sections'] or '---'} | "
            f"{row['direct_review_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(
            f"No court/public-law review rows; run make court-law-linkage and make bill-law-lifecycle-readiness first."
        )
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
