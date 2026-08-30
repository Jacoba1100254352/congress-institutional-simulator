#!/usr/bin/env python3
"""Write source-reviewed dispositions for directional medium-priority LDA packets."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PACKETS = Path("reports/lobbying-bill-medium-disposition-packets.csv")
RAW_REVIEW = Path("data/validation/raw/lobbying_bill_medium_directional_packet_review.csv")
OUT_CSV = Path("reports/lobbying-bill-medium-directional-packet-review.csv")
OUT_MD = Path("reports/lobbying-bill-medium-directional-packet-review.md")

CLAIM_BOUNDARY = (
    "Manual medium-priority LDA directional packet source review only; packet-level "
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
    "manual_medium_directional_packet_review",
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

DIRECTIONAL_PACKET_STATUSES = {
    "medium_support_disposition_packet_needs_confirmation",
    "medium_opposition_disposition_packet_needs_confirmation",
}

CONFIRMED_SUPPORT_STATUSES = {
    "reviewed_current_bill_support",
    "reviewed_current_bill_support_with_opposition_signal_correction",
}
CONFIRMED_OPPOSITION_STATUSES = {
    "reviewed_current_bill_opposition",
}
DOWNGRADED_STATUSES = {
    "reviewed_direction_signal_on_other_measure",
    "reviewed_current_bill_monitoring_only_with_related_opposition",
}
VALID_DISPOSITION_STATUSES = (
    CONFIRMED_SUPPORT_STATUSES | CONFIRMED_OPPOSITION_STATUSES | DOWNGRADED_STATUSES
)
VALID_TARGET_STATUSES = {
    "reviewed_named_member_or_chair_text_reference",
    "reviewed_no_specific_member_or_committee_target_in_activity_text",
}

RAW_FIELDNAMES = [
    "packet_fingerprint",
    "reviewed_packet_rank",
    "reviewed_bill_id",
    "reviewed_public_law_number",
    "manual_review_source",
    "manual_packet_disposition_status",
    "manual_packet_disposition",
    "manual_packet_disposition_basis",
    "manual_target_status",
    "manual_target_type",
    "manual_target_text",
    "manual_target_basis",
    "manual_outcome_link_status",
    "manual_reviewer_note",
    "claim_boundary",
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
    "support_text_signals",
    "opposition_text_signals",
    "manual_review_source",
    "manual_packet_disposition_status",
    "manual_packet_disposition",
    "manual_packet_disposition_basis",
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


def directional_packets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    packets = [
        row for row in rows
        if row.get("packet_review_status", "").strip() in DIRECTIONAL_PACKET_STATUSES
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
    if raw_row.get("claim_boundary", "").strip() != CLAIM_BOUNDARY:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: claim_boundary mismatch.")
    if raw_row.get("manual_packet_disposition_status", "").strip() not in VALID_DISPOSITION_STATUSES:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: invalid manual_packet_disposition_status.")
    if raw_row.get("manual_target_status", "").strip() not in VALID_TARGET_STATUSES:
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: invalid manual_target_status.")
    if raw_row.get("manual_outcome_link_status", "").strip() != "no_outcome_influence_evidence":
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: outcome status is too broad.")
    if (
        raw_row.get("manual_target_status", "").strip() == "reviewed_named_member_or_chair_text_reference"
        and not raw_row.get("manual_target_text", "").strip()
    ):
        raise SystemExit(f"{RAW_REVIEW}: {fingerprint}: named target text is missing.")


def build_rows(packet_rows: list[dict[str, str]], raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    packets = directional_packets(packet_rows)
    raw_by_fingerprint = by_fingerprint(raw_rows, RAW_REVIEW)
    expected_fingerprints = {
        row.get("packet_fingerprint", "").strip()
        for row in packets
    }
    if set(raw_by_fingerprint) != expected_fingerprints:
        raise SystemExit(
            "Medium directional LDA packet review rows must match directional packet rows: "
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
            "support_text_signals": packet.get("support_text_signals", "").strip(),
            "opposition_text_signals": packet.get("opposition_text_signals", "").strip(),
            "manual_review_source": raw_row.get("manual_review_source", "").strip(),
            "manual_packet_disposition_status": raw_row.get("manual_packet_disposition_status", "").strip(),
            "manual_packet_disposition": raw_row.get("manual_packet_disposition", "").strip(),
            "manual_packet_disposition_basis": raw_row.get("manual_packet_disposition_basis", "").strip(),
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


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["manual_packet_disposition_status"] for row in rows)
    target_statuses = Counter(row["manual_target_status"] for row in rows)
    support_rows = [
        row for row in rows
        if row["manual_packet_disposition_status"] in CONFIRMED_SUPPORT_STATUSES
    ]
    opposition_rows = [
        row for row in rows
        if row["manual_packet_disposition_status"] in CONFIRMED_OPPOSITION_STATUSES
    ]
    downgraded_rows = [
        row for row in rows
        if row["manual_packet_disposition_status"] in DOWNGRADED_STATUSES
    ]
    corrected_opposition_rows = [
        row for row in rows
        if row["manual_packet_disposition_status"]
        == "reviewed_current_bill_support_with_opposition_signal_correction"
    ]
    no_outcome_rows = [
        row for row in rows
        if row["manual_outcome_link_status"] == "no_outcome_influence_evidence"
    ]

    lines = [
        "# LDA Medium-Priority Directional Packet Review",
        "",
        "This report source-reviews medium-priority LDA packets with support or opposition text signals. It confirms some current-bill dispositions and narrows others to bill-reference or related-measure context. It is not lobbying-contact or influence evidence.",
        "",
        f"- Directional medium-priority packets reviewed: {len(rows)}",
        f"- Source rows represented by reviewed packets: {row_count(rows)}",
        f"- Packets confirming current-bill support: {len(support_rows)}",
        f"- Source rows in current-bill support packets: {row_count(support_rows)}",
        f"- Packets confirming current-bill opposition: {len(opposition_rows)}",
        f"- Source rows in current-bill opposition packets: {row_count(opposition_rows)}",
        f"- Directional packets downgraded to other-measure direction or monitoring/reference only: {len(downgraded_rows)}",
        f"- Opposition packets reclassified as current-bill support: {len(corrected_opposition_rows)}",
        f"- Packets with named member/chair text reference: {target_statuses.get('reviewed_named_member_or_chair_text_reference', 0)}",
        f"- Packets with no outcome influence evidence: {len(no_outcome_rows)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Manual packet disposition statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Source-reviewed directional packets:",
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
            f"`{row['manual_packet_disposition_status']}` | {md_escape(target)} | "
            f"{md_escape(row['manual_reviewer_note'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    packet_rows = read_csv(PACKETS)
    raw_rows = read_csv(RAW_REVIEW)
    require_columns(RAW_REVIEW, raw_rows, RAW_FIELDNAMES)
    rows = build_rows(packet_rows, raw_rows)
    if not rows:
        raise SystemExit("No directional medium-priority LDA packets were reviewed.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
