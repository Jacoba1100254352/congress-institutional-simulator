#!/usr/bin/env python3
"""Write source-reviewed manual dispositions for high-priority LDA bill rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


DISPOSITION_REVIEW = Path("reports/lobbying-bill-disposition-review.csv")
RAW_REVIEW = Path("data/validation/raw/lobbying_bill_manual_disposition_review.csv")
OUT_CSV = Path("reports/lobbying-bill-manual-disposition-review.csv")
OUT_MD = Path("reports/lobbying-bill-manual-disposition-review.md")

CLAIM_BOUNDARY = (
    "Manual high-priority LDA disposition/target source review only; reviewed "
    "activity-text dispositions and named target references do not show lobbying "
    "contact, sponsor/member targeting beyond the text reference, committee-action "
    "influence, roll-call influence, legislative-outcome causality, public benefit, "
    "welfare, causal capture, or model validation."
)

EVIDENCE_LAYERS = "; ".join([
    "official_lda_filing_text_bill_identifier",
    "official_lda_activity_text_source_review",
    "deterministic_activity_text_position_signal",
    "disposition_target_review_queue",
    "manual_high_priority_disposition_review",
])

MISSING_LINKS = "; ".join([
    "lobbying_contact_confirmation",
    "sponsor_or_member_target_beyond_activity_text_reference",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

RAW_FIELDNAMES = [
    "source_row_fingerprint",
    "reviewed_bill_id",
    "reviewed_public_law_number",
    "manual_review_source",
    "reviewed_source_url",
    "reviewed_source_text",
    "manual_disposition_status",
    "manual_disposition",
    "manual_disposition_basis",
    "manual_target_status",
    "manual_target_type",
    "manual_target_text",
    "manual_target_basis",
    "manual_outcome_link_status",
    "manual_reviewer_note",
    "claim_boundary",
]

FIELDNAMES = [
    "manual_review_rank",
    "queue_review_rank",
    "source_row_fingerprint",
    "bill_id",
    "public_law_number",
    "policy_area",
    "filing_uuid",
    "client_name",
    "registrant_name",
    "activity_issue",
    "text_review_status",
    "queue_review_priority",
    "queue_manual_review_reason",
    "queue_target_review_status",
    "manual_review_source",
    "manual_disposition_status",
    "manual_disposition",
    "manual_disposition_basis",
    "manual_target_status",
    "manual_target_type",
    "manual_target_text",
    "manual_target_basis",
    "manual_outcome_link_status",
    "manual_reviewer_note",
    "reviewed_source_text",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

EXPECTED_MANUAL_STATUS_BY_TEXT_STATUS = {
    "exact_bill_text_with_explicit_support_signal": "reviewed_current_bill_support",
    "exact_bill_text_with_mixed_support_opposition_signal": (
        "reviewed_current_bill_support_with_related_opposition"
    ),
    "exact_bill_text_bill_list_or_title_only": "reviewed_bill_reference_only",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require_columns(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    if not rows:
        raise SystemExit(f"{path} is empty.")
    missing = set(columns) - set(rows[0])
    if missing:
        raise SystemExit(f"{path} is missing columns: {sorted(missing)}")


def high_priority_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    high_rows = [
        row for row in rows
        if row.get("review_priority", "").strip() == "high"
    ]
    high_rows.sort(key=lambda row: int(row.get("review_rank", "999999") or "999999"))
    return high_rows


def by_fingerprint(rows: list[dict[str, str]], path: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        fingerprint = row.get("source_row_fingerprint", "").strip()
        if not fingerprint:
            raise SystemExit(f"{path} contains a blank source_row_fingerprint.")
        if fingerprint in result:
            raise SystemExit(f"{path} contains duplicate source_row_fingerprint {fingerprint}.")
        result[fingerprint] = row
    return result


def validate_raw_review(queue_row: dict[str, str], raw_row: dict[str, str]) -> None:
    fingerprint = queue_row.get("source_row_fingerprint", "").strip()
    if raw_row.get("reviewed_bill_id", "").strip() != queue_row.get("bill_id", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_bill_id mismatch.")
    if (
        raw_row.get("reviewed_public_law_number", "").strip()
        != queue_row.get("public_law_number", "").strip()
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_public_law_number mismatch.")
    if raw_row.get("reviewed_source_text", "").strip() != queue_row.get("bill_reference_context", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_source_text mismatch.")
    if raw_row.get("claim_boundary", "").strip() != CLAIM_BOUNDARY:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: claim_boundary mismatch.")
    expected_status = EXPECTED_MANUAL_STATUS_BY_TEXT_STATUS.get(
        queue_row.get("text_review_status", "").strip()
    )
    if expected_status and raw_row.get("manual_disposition_status", "").strip() != expected_status:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: manual_disposition_status mismatch.")
    if raw_row.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: outcome status is too broad.")


def build_rows(queue_rows: list[dict[str, str]], raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    high_rows = high_priority_rows(queue_rows)
    raw_by_fingerprint = by_fingerprint(raw_rows, RAW_REVIEW)
    expected_fingerprints = {
        row.get("source_row_fingerprint", "").strip()
        for row in high_rows
    }
    if set(raw_by_fingerprint) != expected_fingerprints:
        raise SystemExit(
            "Manual LDA disposition source-review rows must match high-priority queue rows: "
            f"missing={sorted(expected_fingerprints - set(raw_by_fingerprint))}, "
            f"extra={sorted(set(raw_by_fingerprint) - expected_fingerprints)}"
        )

    output: list[dict[str, str]] = []
    for queue_row in high_rows:
        fingerprint = queue_row.get("source_row_fingerprint", "").strip()
        raw_row = raw_by_fingerprint[fingerprint]
        validate_raw_review(queue_row, raw_row)
        output.append({
            "manual_review_rank": str(len(output) + 1),
            "queue_review_rank": queue_row.get("review_rank", "").strip(),
            "source_row_fingerprint": fingerprint,
            "bill_id": queue_row.get("bill_id", "").strip(),
            "public_law_number": queue_row.get("public_law_number", "").strip(),
            "policy_area": queue_row.get("policy_area", "").strip(),
            "filing_uuid": queue_row.get("filing_uuid", "").strip(),
            "client_name": queue_row.get("client_name", "").strip(),
            "registrant_name": queue_row.get("registrant_name", "").strip(),
            "activity_issue": queue_row.get("activity_issue", "").strip(),
            "text_review_status": queue_row.get("text_review_status", "").strip(),
            "queue_review_priority": queue_row.get("review_priority", "").strip(),
            "queue_manual_review_reason": queue_row.get("manual_review_reason", "").strip(),
            "queue_target_review_status": queue_row.get("target_review_status", "").strip(),
            "manual_review_source": raw_row.get("manual_review_source", "").strip(),
            "manual_disposition_status": raw_row.get("manual_disposition_status", "").strip(),
            "manual_disposition": raw_row.get("manual_disposition", "").strip(),
            "manual_disposition_basis": raw_row.get("manual_disposition_basis", "").strip(),
            "manual_target_status": raw_row.get("manual_target_status", "").strip(),
            "manual_target_type": raw_row.get("manual_target_type", "").strip(),
            "manual_target_text": raw_row.get("manual_target_text", "").strip(),
            "manual_target_basis": raw_row.get("manual_target_basis", "").strip(),
            "manual_outcome_link_status": raw_row.get("manual_outcome_link_status", "").strip(),
            "manual_reviewer_note": raw_row.get("manual_reviewer_note", "").strip(),
            "reviewed_source_text": raw_row.get("reviewed_source_text", "").strip(),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "source_urls": queue_row.get("source_urls", "").strip(),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    dispositions = Counter(row["manual_disposition_status"] for row in rows)
    targets = Counter(row["manual_target_status"] for row in rows)
    support_rows = [
        row for row in rows
        if row["manual_disposition_status"] in {
            "reviewed_current_bill_support",
            "reviewed_current_bill_support_with_related_opposition",
        }
    ]
    related_opposition_rows = [
        row for row in rows
        if row["manual_disposition_status"] == "reviewed_current_bill_support_with_related_opposition"
    ]
    bill_reference_only_rows = [
        row for row in rows
        if row["manual_disposition_status"] == "reviewed_bill_reference_only"
    ]
    no_outcome_rows = [
        row for row in rows
        if row["manual_outcome_link_status"] == "no_outcome_influence_evidence"
    ]
    lines = [
        "# LDA High-Priority Manual Disposition/Target Review",
        "",
        "This report records source-reviewed manual disposition and target-reference classifications for the high-priority LDA disposition queue. It is not evidence that lobbying contacted a member, targeted a committee action, changed a vote, or caused an outcome.",
        "",
        f"- High-priority queue rows reviewed: {len(rows)}",
        f"- Confirmed current-bill support rows: {len(support_rows)}",
        f"- Rows with support plus opposition to amendments or related measures: {len(related_opposition_rows)}",
        f"- Bill-reference-only rows after manual review: {len(bill_reference_only_rows)}",
        f"- Rows with named member/chair text reference: {targets.get('reviewed_named_member_or_chair_text_reference', 0)}",
        f"- Rows with committee-context text reference: {targets.get('reviewed_committee_context_text_reference', 0)}",
        f"- Rows with no outcome influence evidence: {len(no_outcome_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Manual disposition statuses:",
    ]
    for status, count in sorted(dispositions.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Manual target statuses:",
    ])
    for status, count in sorted(targets.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Source-reviewed rows:",
        "",
        "| Rank | Queue rank | Bill | Public law | Client | Manual disposition | Manual target | Note |",
        "| ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        target = row["manual_target_text"] or row["manual_target_status"]
        lines.append(
            f"| {row['manual_review_rank']} | {row['queue_review_rank']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{md_escape(row['client_name'])} | `{row['manual_disposition_status']}` | "
            f"{md_escape(target)} | {md_escape(row['manual_reviewer_note'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    queue_rows = read_csv(DISPOSITION_REVIEW)
    raw_rows = read_csv(RAW_REVIEW)
    require_columns(RAW_REVIEW, raw_rows, RAW_FIELDNAMES)
    rows = build_rows(queue_rows, raw_rows)
    if not rows:
        raise SystemExit("No high-priority LDA disposition rows were reviewed.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
