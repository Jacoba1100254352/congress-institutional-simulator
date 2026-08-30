#!/usr/bin/env python3
"""Write a prioritized disposition/target review queue for exact LDA bill mentions."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


TEXT_REVIEW = Path("reports/lobbying-bill-text-review.csv")
ACTION_CONTEXT = Path("reports/lobbying-bill-action-context.csv")
OUT_CSV = Path("reports/lobbying-bill-disposition-review.csv")
OUT_MD = Path("reports/lobbying-bill-disposition-review.md")

FIELDNAMES = [
    "review_rank",
    "source_row_fingerprint",
    "review_priority",
    "manual_review_needed",
    "manual_review_reason",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_bioguide_id",
    "committee_reported",
    "floor_considered",
    "enacted",
    "filing_uuid",
    "filing_year",
    "filing_period",
    "client_name",
    "registrant_name",
    "activity_issue",
    "matched_bill_refs",
    "text_review_status",
    "preliminary_text_disposition",
    "support_text_signal",
    "opposition_text_signal",
    "position_or_activity_text_signal",
    "government_entity_scope",
    "possible_member_or_committee_reference",
    "target_review_status",
    "bill_reference_context",
    "recommended_next_review",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "LDA disposition/target source-review queue only; deterministic text signals "
    "and possible target references are not manual disposition confirmation, "
    "sponsor/member targeting evidence, committee-action influence, roll-call "
    "influence, legislative-outcome causality, public benefit, welfare, causal "
    "capture, or model validation."
)

MISSING_LINKS = "; ".join([
    "manual_disposition_confirmation",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

EVIDENCE_LAYERS = "; ".join([
    "official_lda_filing_text_bill_identifier",
    "official_lda_activity_text_source_review",
    "deterministic_activity_text_position_signal",
    "disposition_target_review_queue",
    "congressgov_bill_action_metadata_context",
])

SUPPORT_STATUS = "exact_bill_text_with_explicit_support_signal"
OPPOSITION_STATUS = "exact_bill_text_with_explicit_opposition_signal"
MIXED_STATUS = "exact_bill_text_with_mixed_support_opposition_signal"
POSITION_STATUS = "exact_bill_text_with_position_or_activity_signal"
LIST_ONLY_STATUS = "exact_bill_text_bill_list_or_title_only"
REFETCH_STATUS = "matched_reference_not_located_in_stored_activity_text"

STATUS_DISPOSITIONS = {
    SUPPORT_STATUS: "support_signal_needs_manual_confirmation",
    OPPOSITION_STATUS: "opposition_signal_needs_manual_confirmation",
    MIXED_STATUS: "mixed_support_opposition_signal_needs_manual_confirmation",
    POSITION_STATUS: "position_or_activity_signal_needs_manual_confirmation",
    LIST_ONLY_STATUS: "bill_reference_without_disposition_signal",
    REFETCH_STATUS: "stored_excerpt_needs_full_activity_text_refetch",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def action_context_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("bill_id", "").strip(): row
        for row in rows
        if row.get("bill_id", "").strip()
    }


def target_reference_detected(row: dict[str, str]) -> bool:
    return row.get("possible_member_or_committee_reference", "").strip() != "not_detected_in_activity_text"


def review_priority(row: dict[str, str]) -> str:
    status = row.get("text_review_status", "").strip()
    if status == MIXED_STATUS or target_reference_detected(row):
        return "high"
    if status in {SUPPORT_STATUS, OPPOSITION_STATUS, POSITION_STATUS}:
        return "medium"
    return "low"


def manual_review_reason(row: dict[str, str], priority: str) -> str:
    reasons: list[str] = []
    status = row.get("text_review_status", "").strip()
    if status == MIXED_STATUS:
        reasons.append("mixed_support_opposition_signal")
    elif status == SUPPORT_STATUS:
        reasons.append("support_signal")
    elif status == OPPOSITION_STATUS:
        reasons.append("opposition_signal")
    elif status == POSITION_STATUS:
        reasons.append("position_or_activity_signal")
    elif status == REFETCH_STATUS:
        reasons.append("full_activity_text_refetch_needed")
    if target_reference_detected(row):
        reasons.append("possible_member_or_committee_reference")
    if not reasons and priority == "low":
        return "bill_reference_only_no_disposition_or_target_signal"
    return "; ".join(reasons)


def target_review_status(row: dict[str, str]) -> str:
    possible_reference = row.get("possible_member_or_committee_reference", "").strip()
    if possible_reference != "not_detected_in_activity_text":
        return "possible_member_or_committee_reference_needs_manual_target_review"
    scope = row.get("government_entity_scope", "").strip()
    if scope in {
        "house_senate_and_agency_entities_disclosed",
        "house_and_senate_entities_disclosed",
        "single_chamber_entity_disclosed",
    }:
        return "chamber_entity_context_only_no_specific_target_detected"
    if scope == "agency_entities_only_disclosed":
        return "agency_entity_context_only_no_specific_target_detected"
    return "no_government_entity_context_or_specific_target_detected"


def recommended_next_review(row: dict[str, str], priority: str) -> str:
    if priority == "high":
        return (
            "Inspect filing text and linked Congress.gov bill/action metadata for "
            "manual disposition and target/outcome context."
        )
    if priority == "medium":
        return (
            "Manually confirm direction/position and check whether the filing "
            "names a target, member, or committee rather than only a chamber/entity."
        )
    return "Keep as bill-reference context unless later target/outcome review needs it."


def build_rows(
    text_review_rows: list[dict[str, str]],
    action_context_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    action_by_bill = action_context_by_bill(action_context_rows)
    output: list[dict[str, str]] = []
    for text_row in text_review_rows:
        bill_id = text_row.get("bill_id", "").strip()
        action_row = action_by_bill.get(bill_id)
        if action_row is None:
            raise SystemExit(f"missing action context row for bill {bill_id}")
        priority = review_priority(text_row)
        manual_needed = "yes" if priority in {"high", "medium"} else "no"
        output.append({
            "review_rank": "0",
            "source_row_fingerprint": text_row.get("source_row_fingerprint", ""),
            "review_priority": priority,
            "manual_review_needed": manual_needed,
            "manual_review_reason": manual_review_reason(text_row, priority),
            "bill_id": bill_id,
            "public_law_number": text_row.get("public_law_number", ""),
            "policy_area": text_row.get("policy_area", ""),
            "sponsor_bioguide_id": action_row.get("sponsor_bioguide_id", ""),
            "committee_reported": action_row.get("committee_reported", ""),
            "floor_considered": action_row.get("floor_considered", ""),
            "enacted": action_row.get("enacted", ""),
            "filing_uuid": text_row.get("filing_uuid", ""),
            "filing_year": text_row.get("filing_year", ""),
            "filing_period": text_row.get("filing_period", ""),
            "client_name": text_row.get("client_name", ""),
            "registrant_name": text_row.get("registrant_name", ""),
            "activity_issue": text_row.get("activity_issue", ""),
            "matched_bill_refs": text_row.get("matched_bill_refs", ""),
            "text_review_status": text_row.get("text_review_status", ""),
            "preliminary_text_disposition": STATUS_DISPOSITIONS.get(
                text_row.get("text_review_status", "").strip(),
                "unclassified_text_signal_needs_manual_review",
            ),
            "support_text_signal": text_row.get("support_text_signal", ""),
            "opposition_text_signal": text_row.get("opposition_text_signal", ""),
            "position_or_activity_text_signal": text_row.get("position_or_activity_text_signal", ""),
            "government_entity_scope": text_row.get("government_entity_scope", ""),
            "possible_member_or_committee_reference": text_row.get("possible_member_or_committee_reference", ""),
            "target_review_status": target_review_status(text_row),
            "bill_reference_context": text_row.get("bill_reference_context", ""),
            "recommended_next_review": recommended_next_review(text_row, priority),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "source_urls": text_row.get("source_urls", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    priority_order = {"high": 0, "medium": 1, "low": 2}
    output.sort(key=lambda row: (
        priority_order.get(row["review_priority"], 99),
        row["bill_id"],
        row["filing_year"],
        row["filing_period"],
        row["client_name"],
        row["source_row_fingerprint"],
    ))
    for index, row in enumerate(output, start=1):
        row["review_rank"] = str(index)
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
    priorities = Counter(row["review_priority"] for row in rows)
    statuses = Counter(row["text_review_status"] for row in rows)
    manual_rows = [row for row in rows if row["manual_review_needed"] == "yes"]
    possible_target_rows = [
        row for row in rows
        if row["possible_member_or_committee_reference"] != "not_detected_in_activity_text"
    ]
    committee_rows = [row for row in rows if row["committee_reported"] == "1"]
    floor_rows = [row for row in rows if row["floor_considered"] == "1"]
    enacted_rows = [row for row in rows if row["enacted"] == "1"]
    lines = [
        "# LDA Bill Disposition/Target Review",
        "",
        "This report prioritizes exact LDA bill-text rows for manual disposition and target review. It is a source-review queue, not evidence that lobbying targeted or changed any legislative action or outcome.",
        "",
        f"- Exact LDA bill-text rows represented: {len(rows)}",
        f"- Rows needing manual disposition or target review: {len(manual_rows)}",
        f"- High-priority review rows: {priorities.get('high', 0)}",
        f"- Medium-priority review rows: {priorities.get('medium', 0)}",
        f"- Low-priority bill-reference-only rows: {priorities.get('low', 0)}",
        f"- Support-only rows: {statuses.get(SUPPORT_STATUS, 0)}",
        f"- Opposition-only rows: {statuses.get(OPPOSITION_STATUS, 0)}",
        f"- Mixed support/opposition rows: {statuses.get(MIXED_STATUS, 0)}",
        f"- Position/activity rows: {statuses.get(POSITION_STATUS, 0)}",
        f"- Bill-list/title-only rows: {statuses.get(LIST_ONLY_STATUS, 0)}",
        f"- Possible member/committee reference rows: {len(possible_target_rows)}",
        f"- Rows with committee-reported metadata: {len(committee_rows)}",
        f"- Rows with floor-considered metadata: {len(floor_rows)}",
        f"- Rows with enacted public-law metadata: {len(enacted_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Review priorities:",
    ]
    for priority, count in sorted(priorities.items()):
        lines.append(f"- {priority}: {count}")
    lines.extend([
        "",
        "Text review statuses:",
    ])
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Top priority rows:",
        "",
        "| Rank | Priority | Bill | Public law | Client | Status | Target status | Reason | Next review |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows[:20]:
        lines.append(
            f"| {row['review_rank']} | {row['review_priority']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | {md_escape(row['client_name'])} | "
            f"{row['text_review_status']} | {row['target_review_status']} | "
            f"{md_escape(row['manual_review_reason'])} | "
            f"{md_escape(row['recommended_next_review'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    text_review_rows = read_csv(TEXT_REVIEW)
    action_context_rows = read_csv(ACTION_CONTEXT)
    if not text_review_rows:
        raise SystemExit(f"{TEXT_REVIEW} is empty; run make lobbying-bill-text-review first.")
    if not action_context_rows:
        raise SystemExit(f"{ACTION_CONTEXT} is empty; run make lobbying-bill-action-context first.")
    rows = build_rows(text_review_rows, action_context_rows)
    if len(rows) != len(text_review_rows):
        raise SystemExit("disposition review row count does not match LDA text-review row count.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
