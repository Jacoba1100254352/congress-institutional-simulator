#!/usr/bin/env python3
"""Write source-reviewed dispositions for position/activity medium-priority LDA packets."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PACKETS = Path("reports/lobbying-bill-medium-disposition-packets.csv")
RAW_REVIEW = Path("data/validation/raw/lobbying_bill_medium_position_activity_packet_review.csv")
OUT_CSV = Path("reports/lobbying-bill-medium-position-activity-packet-review.csv")
OUT_MD = Path("reports/lobbying-bill-medium-position-activity-packet-review.md")

CLAIM_BOUNDARY = (
    "Manual medium-priority LDA position/activity packet source review only; packet-level "
    "activity-text dispositions do not show lobbying contact or sponsor/member "
    "targeting beyond text references or committee-action influence or roll-call "
    "influence or legislative-outcome causality or public benefit or welfare or "
    "causal capture or model validation."
)

EVIDENCE_LAYERS = "; ".join([
    "official_lda_filing_text_bill_identifier",
    "official_lda_activity_text_source_review",
    "deterministic_activity_text_position_signal",
    "disposition_target_review_queue",
    "medium_disposition_review_packet",
    "manual_medium_position_activity_packet_review",
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

POSITION_ACTIVITY_PACKET_STATUSES = {
    "medium_position_activity_packet_needs_direction_review",
}

ISSUE_OR_PROVISION_STATUSES = {
    "reviewed_current_bill_issue_or_provision_activity_without_direction",
}
MONITORING_STATUSES = {
    "reviewed_current_bill_monitoring_or_analysis_only",
}
ALL_PROVISIONS_STATUSES = {
    "reviewed_current_bill_all_provisions_without_direction",
}
POSITION_REPRESENTED_STATUSES = {
    "reviewed_current_bill_position_represented_without_direction",
}
LOBBIED_ON_STATUSES = {
    "reviewed_current_bill_lobbied_on_without_direction",
}
OPPOSITION_STATUSES = {
    "reviewed_current_bill_opposition_from_activity_text",
}
VALID_ACTIVITY_DISPOSITION_STATUSES = (
    ISSUE_OR_PROVISION_STATUSES
    | MONITORING_STATUSES
    | ALL_PROVISIONS_STATUSES
    | POSITION_REPRESENTED_STATUSES
    | LOBBIED_ON_STATUSES
    | OPPOSITION_STATUSES
)
VALID_TARGET_STATUSES = {
    "reviewed_no_specific_member_or_committee_target_in_activity_text",
    "reviewed_generic_congress_text_reference",
}

RAW_FIELDNAMES = [
    "packet_fingerprint",
    "reviewed_packet_rank",
    "reviewed_bill_id",
    "reviewed_public_law_number",
    "manual_review_source",
    "manual_activity_disposition_status",
    "manual_activity_disposition",
    "manual_activity_disposition_basis",
    "manual_target_status",
    "manual_target_type",
    "manual_target_text",
    "manual_target_basis",
    "manual_outcome_link_status",
    "manual_reviewer_note",
]

FIELDNAMES = [
    "manual_packet_review_rank",
    "packet_rank",
    "packet_fingerprint",
    "bill_id",
    "public_law_number",
    "policy_area",
    "client_name",
    "registrant_name",
    "activity_issue",
    "packet_review_status",
    "direction_signal_summary",
    "rows_represented",
    "source_row_fingerprints",
    "queue_review_ranks",
    "position_or_activity_text_signals",
    "support_text_signals",
    "opposition_text_signals",
    "manual_review_source",
    "manual_activity_disposition_status",
    "manual_activity_disposition",
    "manual_activity_disposition_basis",
    "manual_target_status",
    "manual_target_type",
    "manual_target_text",
    "manual_target_basis",
    "manual_outcome_link_status",
    "manual_reviewer_note",
    "bill_reference_context_samples",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]


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


def by_fingerprint(rows: list[dict[str, str]], path: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        fingerprint = row.get("packet_fingerprint", "").strip()
        if not fingerprint:
            raise SystemExit(f"{path} contains a blank packet_fingerprint.")
        if fingerprint in result:
            raise SystemExit(f"{path} contains duplicate packet_fingerprint {fingerprint}.")
        result[fingerprint] = row
    return result


def position_activity_packets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    packets = [
        row for row in rows
        if row.get("packet_review_status", "").strip() in POSITION_ACTIVITY_PACKET_STATUSES
    ]
    packets.sort(key=lambda row: int(row.get("packet_rank", "999999") or "999999"))
    return packets


def validate_raw_review(packet: dict[str, str], raw_row: dict[str, str]) -> None:
    fingerprint = packet.get("packet_fingerprint", "").strip()
    if raw_row.get("reviewed_packet_rank", "").strip() != packet.get("packet_rank", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_packet_rank mismatch.")
    if raw_row.get("reviewed_bill_id", "").strip() != packet.get("bill_id", "").strip():
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_bill_id mismatch.")
    if (
        raw_row.get("reviewed_public_law_number", "").strip()
        != packet.get("public_law_number", "").strip()
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: reviewed_public_law_number mismatch.")
    if (
        raw_row.get("manual_activity_disposition_status", "").strip()
        not in VALID_ACTIVITY_DISPOSITION_STATUSES
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: invalid manual_activity_disposition_status.")
    if raw_row.get("manual_target_status", "").strip() not in VALID_TARGET_STATUSES:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: invalid manual_target_status.")
    if raw_row.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: outcome status is too broad.")
    if (
        raw_row.get("manual_target_status", "").strip() == "reviewed_generic_congress_text_reference"
        and raw_row.get("manual_target_text", "").strip().casefold() != "congress"
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: generic Congress target text is missing.")
    if (
        raw_row.get("manual_activity_disposition_status", "").strip()
        == "reviewed_current_bill_opposition_from_activity_text"
        and "against" not in raw_row.get("manual_activity_disposition_basis", "").casefold()
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: opposition basis is missing.")


def build_rows(packet_rows: list[dict[str, str]], raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    packets = position_activity_packets(packet_rows)
    raw_by_fingerprint = by_fingerprint(raw_rows, RAW_REVIEW)
    expected_fingerprints = {
        row.get("packet_fingerprint", "").strip()
        for row in packets
    }
    if set(raw_by_fingerprint) != expected_fingerprints:
        raise SystemExit(
            "Medium position/activity LDA packet review rows must match position/activity packet rows: "
            f"missing={sorted(expected_fingerprints - set(raw_by_fingerprint))}, "
            f"extra={sorted(set(raw_by_fingerprint) - expected_fingerprints)}"
        )

    output: list[dict[str, str]] = []
    for packet in packets:
        fingerprint = packet.get("packet_fingerprint", "").strip()
        raw_row = raw_by_fingerprint[fingerprint]
        validate_raw_review(packet, raw_row)
        output.append({
            "manual_packet_review_rank": str(len(output) + 1),
            "packet_rank": packet.get("packet_rank", "").strip(),
            "packet_fingerprint": fingerprint,
            "bill_id": packet.get("bill_id", "").strip(),
            "public_law_number": packet.get("public_law_number", "").strip(),
            "policy_area": packet.get("policy_area", "").strip(),
            "client_name": packet.get("client_name", "").strip(),
            "registrant_name": packet.get("registrant_name", "").strip(),
            "activity_issue": packet.get("activity_issue", "").strip(),
            "packet_review_status": packet.get("packet_review_status", "").strip(),
            "direction_signal_summary": packet.get("direction_signal_summary", "").strip(),
            "rows_represented": packet.get("rows_represented", "").strip(),
            "source_row_fingerprints": packet.get("source_row_fingerprints", "").strip(),
            "queue_review_ranks": packet.get("queue_review_ranks", "").strip(),
            "position_or_activity_text_signals": packet.get("position_or_activity_text_signals", "").strip(),
            "support_text_signals": packet.get("support_text_signals", "").strip(),
            "opposition_text_signals": packet.get("opposition_text_signals", "").strip(),
            "manual_review_source": raw_row.get("manual_review_source", "").strip(),
            "manual_activity_disposition_status": raw_row.get("manual_activity_disposition_status", "").strip(),
            "manual_activity_disposition": raw_row.get("manual_activity_disposition", "").strip(),
            "manual_activity_disposition_basis": raw_row.get("manual_activity_disposition_basis", "").strip(),
            "manual_target_status": raw_row.get("manual_target_status", "").strip(),
            "manual_target_type": raw_row.get("manual_target_type", "").strip(),
            "manual_target_text": raw_row.get("manual_target_text", "").strip(),
            "manual_target_basis": raw_row.get("manual_target_basis", "").strip(),
            "manual_outcome_link_status": raw_row.get("manual_outcome_link_status", "").strip(),
            "manual_reviewer_note": raw_row.get("manual_reviewer_note", "").strip(),
            "bill_reference_context_samples": packet.get("bill_reference_context_samples", "").strip(),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "source_urls": packet.get("source_urls", "").strip(),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def row_count(rows: list[dict[str, str]]) -> int:
    return sum(int(row.get("rows_represented", "0") or "0") for row in rows)


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rows_with_status(rows: list[dict[str, str]], statuses: set[str]) -> list[dict[str, str]]:
    return [
        row for row in rows
        if row["manual_activity_disposition_status"] in statuses
    ]


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["manual_activity_disposition_status"] for row in rows)
    target_statuses = Counter(row["manual_target_status"] for row in rows)
    issue_rows = rows_with_status(rows, ISSUE_OR_PROVISION_STATUSES)
    monitoring_rows = rows_with_status(rows, MONITORING_STATUSES)
    all_provisions_rows = rows_with_status(rows, ALL_PROVISIONS_STATUSES)
    position_rows = rows_with_status(rows, POSITION_REPRESENTED_STATUSES)
    lobbied_on_rows = rows_with_status(rows, LOBBIED_ON_STATUSES)
    opposition_rows = rows_with_status(rows, OPPOSITION_STATUSES)
    no_outcome_rows = [
        row for row in rows
        if row["manual_outcome_link_status"] == "no_outcome_influence_evidence"
    ]

    lines = [
        "# LDA Medium-Priority Position/Activity Packet Review",
        "",
        "This report source-reviews medium-priority LDA packets with position or activity text signals but no explicit support/opposition direction. It classifies current-bill activity-text dispositions and preserves the no-outcome-influence boundary.",
        "",
        f"- Position/activity medium-priority packets reviewed: {len(rows)}",
        f"- Source rows represented by reviewed position/activity packets: {row_count(rows)}",
        f"- Packets confirming current-bill issue/provision activity without direction: {len(issue_rows)}",
        f"- Source rows in current-bill issue/provision activity packets: {row_count(issue_rows)}",
        f"- Packets confirming current-bill monitoring or analysis only: {len(monitoring_rows)}",
        f"- Source rows in monitoring or analysis packets: {row_count(monitoring_rows)}",
        f"- Packets listing all provisions without direction: {len(all_provisions_rows)}",
        f"- Source rows in all-provisions packets: {row_count(all_provisions_rows)}",
        f"- Packets representing a current-bill position without direction: {len(position_rows)}",
        f"- Source rows in position-represented packets: {row_count(position_rows)}",
        f"- Packets saying lobbied on the current bill without direction: {len(lobbied_on_rows)}",
        f"- Packets with generic Congress text reference: {target_statuses.get('reviewed_generic_congress_text_reference', 0)}",
        f"- Packets upgraded to current-bill opposition: {len(opposition_rows)}",
        f"- Source rows in upgraded opposition packets: {row_count(opposition_rows)}",
        f"- Packets with no outcome influence evidence: {len(no_outcome_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Manual activity disposition statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Source-reviewed position/activity packets:",
        "",
        "| Rank | Packet | Rows | Bill | Public law | Client | Manual disposition | Manual target | Note |",
        "| ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        target = row["manual_target_text"] or row["manual_target_status"]
        lines.append(
            f"| {row['manual_packet_review_rank']} | {row['packet_rank']} | "
            f"{row['rows_represented']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | {md_escape(row['client_name'])} | "
            f"`{row['manual_activity_disposition_status']}` | {md_escape(target)} | "
            f"{md_escape(row['manual_reviewer_note'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    packet_rows = read_csv(PACKETS)
    raw_rows = read_csv(RAW_REVIEW)
    require_columns(RAW_REVIEW, raw_rows, RAW_FIELDNAMES)
    rows = build_rows(packet_rows, raw_rows)
    if not rows:
        raise SystemExit("No position/activity medium-priority LDA packets were reviewed.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
