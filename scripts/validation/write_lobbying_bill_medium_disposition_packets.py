#!/usr/bin/env python3
"""Write grouped source-review packets for medium-priority LDA disposition rows."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


DISPOSITION_REVIEW = Path("reports/lobbying-bill-disposition-review.csv")
OUT_CSV = Path("reports/lobbying-bill-medium-disposition-packets.csv")
OUT_MD = Path("reports/lobbying-bill-medium-disposition-packets.md")

SUPPORT_STATUS = "exact_bill_text_with_explicit_support_signal"
OPPOSITION_STATUS = "exact_bill_text_with_explicit_opposition_signal"
POSITION_STATUS = "exact_bill_text_with_position_or_activity_signal"

STATUS_PACKET_REVIEW = {
    SUPPORT_STATUS: "medium_support_disposition_packet_needs_confirmation",
    OPPOSITION_STATUS: "medium_opposition_disposition_packet_needs_confirmation",
    POSITION_STATUS: "medium_position_activity_packet_needs_direction_review",
}

STATUS_NEXT_STEP = {
    SUPPORT_STATUS: (
        "Confirm whether the support signal applies to the current bill and "
        "whether any source text identifies a target, action, roll call, or "
        "outcome disposition."
    ),
    OPPOSITION_STATUS: (
        "Confirm whether the opposition signal applies to the current bill and "
        "whether any source text identifies a target, action, roll call, or "
        "outcome disposition."
    ),
    POSITION_STATUS: (
        "Review source text for directional support/opposition only if a future "
        "claim would use this packet beyond bill-reference or activity context."
    ),
}

STATUS_SIGNAL_SUMMARY = {
    SUPPORT_STATUS: "support_text_signal_needs_manual_confirmation",
    OPPOSITION_STATUS: "opposition_text_signal_needs_manual_confirmation",
    POSITION_STATUS: "position_or_activity_text_signal_needs_direction_review",
}

CLAIM_BOUNDARY = (
    "Medium-priority LDA disposition source-review packets only; grouped "
    "deterministic activity-text signals are not manual disposition confirmation, "
    "lobbying-contact evidence, sponsor/member targeting evidence, "
    "committee-action influence, roll-call influence, legislative-outcome "
    "causality, public benefit, welfare, causal capture, or model validation."
)

EVIDENCE_LAYERS = "; ".join([
    "official_lda_filing_text_bill_identifier",
    "official_lda_activity_text_source_review",
    "deterministic_activity_text_position_signal",
    "disposition_target_review_queue",
    "medium_disposition_review_packet",
])

MISSING_LINKS = "; ".join([
    "manual_disposition_confirmation",
    "lobbying_contact_confirmation",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

FIELDNAMES = [
    "packet_rank",
    "packet_fingerprint",
    "review_priority",
    "packet_review_status",
    "direction_signal_summary",
    "rows_represented",
    "source_row_fingerprints",
    "queue_review_ranks",
    "bill_id",
    "public_law_number",
    "policy_area",
    "client_name",
    "registrant_name",
    "activity_issue",
    "text_review_status",
    "manual_review_reason",
    "target_review_status",
    "filing_uuids",
    "filing_years",
    "filing_periods",
    "support_text_signals",
    "opposition_text_signals",
    "position_or_activity_text_signals",
    "distinct_context_count",
    "bill_reference_context_samples",
    "disposition_next_step",
    "target_next_step",
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


def split_values(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def unique_values(rows: list[dict[str, str]], field: str) -> list[str]:
    values: set[str] = set()
    for row in rows:
        value = row.get(field, "").strip()
        if not value:
            continue
        if ";" in value:
            values.update(split_values(value))
        else:
            values.add(value)
    return sorted(values)


def join_values(values: list[str]) -> str:
    return "; ".join(values)


def packet_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("policy_area", "").strip(),
        row.get("client_name", "").strip(),
        row.get("registrant_name", "").strip(),
        row.get("activity_issue", "").strip(),
        row.get("text_review_status", "").strip(),
        row.get("manual_review_reason", "").strip(),
        row.get("target_review_status", "").strip(),
    )


def packet_fingerprint(key: tuple[str, ...]) -> str:
    return hashlib.sha256("|".join(key).encode("utf-8")).hexdigest()[:16]


def int_value(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 999999


def context_samples(rows: list[dict[str, str]], limit: int = 3) -> tuple[int, str]:
    contexts = []
    seen: set[str] = set()
    for row in sorted(rows, key=lambda item: int_value(item.get("review_rank", ""))):
        context = row.get("bill_reference_context", "").strip()
        if context and context not in seen:
            seen.add(context)
            contexts.append(context)
    return len(contexts), " || ".join(contexts[:limit])


def target_next_step(target_status: str) -> str:
    if target_status == "possible_member_or_committee_reference_needs_manual_target_review":
        return "Review named target reference before any sponsor/member or committee-target claim."
    return "No specific target detected in current activity-text packet; keep target claims missing unless source review finds one."


def build_rows(disposition_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    medium_rows = [
        row for row in disposition_rows
        if row.get("review_priority", "").strip() == "medium"
    ]
    if not medium_rows:
        raise SystemExit(f"{DISPOSITION_REVIEW} has no medium-priority rows.")

    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in medium_rows:
        status = row.get("text_review_status", "").strip()
        if status not in STATUS_PACKET_REVIEW:
            raise SystemExit(f"Unexpected medium-priority text status: {status}")
        grouped[packet_key(row)].append(row)

    output: list[dict[str, str]] = []
    for key, rows in grouped.items():
        first = sorted(rows, key=lambda row: int_value(row.get("review_rank", "")))[0]
        context_count, sample = context_samples(rows)
        status = first.get("text_review_status", "").strip()
        target_status = first.get("target_review_status", "").strip()
        output.append({
            "packet_rank": "0",
            "packet_fingerprint": packet_fingerprint(key),
            "review_priority": "medium",
            "packet_review_status": STATUS_PACKET_REVIEW[status],
            "direction_signal_summary": STATUS_SIGNAL_SUMMARY[status],
            "rows_represented": str(len(rows)),
            "source_row_fingerprints": join_values(unique_values(rows, "source_row_fingerprint")),
            "queue_review_ranks": join_values(sorted(
                (row.get("review_rank", "").strip() for row in rows),
                key=int_value,
            )),
            "bill_id": first.get("bill_id", "").strip(),
            "public_law_number": first.get("public_law_number", "").strip(),
            "policy_area": first.get("policy_area", "").strip(),
            "client_name": first.get("client_name", "").strip(),
            "registrant_name": first.get("registrant_name", "").strip(),
            "activity_issue": first.get("activity_issue", "").strip(),
            "text_review_status": status,
            "manual_review_reason": first.get("manual_review_reason", "").strip(),
            "target_review_status": target_status,
            "filing_uuids": join_values(unique_values(rows, "filing_uuid")),
            "filing_years": join_values(unique_values(rows, "filing_year")),
            "filing_periods": join_values(unique_values(rows, "filing_period")),
            "support_text_signals": join_values(unique_values(rows, "support_text_signal")),
            "opposition_text_signals": join_values(unique_values(rows, "opposition_text_signal")),
            "position_or_activity_text_signals": join_values(
                unique_values(rows, "position_or_activity_text_signal")
            ),
            "distinct_context_count": str(context_count),
            "bill_reference_context_samples": sample,
            "disposition_next_step": STATUS_NEXT_STEP[status],
            "target_next_step": target_next_step(target_status),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "source_urls": join_values(unique_values(rows, "source_urls")),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    output.sort(key=lambda row: int_value(row["queue_review_ranks"].split(";")[0].strip()))
    for rank, row in enumerate(output, start=1):
        row["packet_rank"] = str(rank)
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
    statuses = Counter(row["text_review_status"] for row in rows)
    status_rows = Counter()
    bill_ids = {row["bill_id"] for row in rows}
    clients = {row["client_name"] for row in rows}
    represented_rows = 0
    for row in rows:
        count = int(row["rows_represented"])
        represented_rows += count
        status_rows[row["text_review_status"]] += count
    collapsed_rows = represented_rows - len(rows)
    lines = [
        "# LDA Medium-Priority Disposition Review Packets",
        "",
        "This report groups medium-priority LDA disposition queue rows into source-review packets. It is review infrastructure, not manual disposition confirmation or lobbying-influence evidence.",
        "",
        f"- Medium-priority queue rows represented: {represented_rows}",
        f"- Medium-priority source-review packets: {len(rows)}",
        f"- Rows collapsed by grouping: {collapsed_rows}",
        f"- Unique public-law bill IDs represented: {len(bill_ids)}",
        f"- Unique clients represented: {len(clients)}",
        f"- Explicit support packets: {statuses.get(SUPPORT_STATUS, 0)}",
        f"- Explicit support rows represented: {status_rows.get(SUPPORT_STATUS, 0)}",
        f"- Explicit opposition packets: {statuses.get(OPPOSITION_STATUS, 0)}",
        f"- Explicit opposition rows represented: {status_rows.get(OPPOSITION_STATUS, 0)}",
        f"- Position/activity packets: {statuses.get(POSITION_STATUS, 0)}",
        f"- Position/activity rows represented: {status_rows.get(POSITION_STATUS, 0)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Packet statuses:",
    ]
    packet_statuses = Counter(row["packet_review_status"] for row in rows)
    for status, count in sorted(packet_statuses.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "Top packets:",
        "",
        "| Packet | Rows | Bill | Public law | Client | Status | Next review |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ])
    for row in rows[:30]:
        lines.append(
            f"| {row['packet_rank']} | {row['rows_represented']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{md_escape(row['client_name'])} | `{row['packet_review_status']}` | "
            f"{md_escape(row['disposition_next_step'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows(read_csv(DISPOSITION_REVIEW))
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
