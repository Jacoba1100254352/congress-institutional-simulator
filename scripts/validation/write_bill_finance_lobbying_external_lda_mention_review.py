#!/usr/bin/env python3
"""Source-review external LDA current-bill mention packets."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


LDA_MENTIONS = Path("data/validation/raw/bill_finance_lobbying_external_lda_mentions.csv")
EXTERNAL_SEARCH_REVIEW = Path("reports/bill-finance-lobbying-external-search-review.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-external-lda-mention-review.csv")
OUT_MD = Path("reports/bill-finance-lobbying-external-lda-mention-review.md")

CLAIM_BOUNDARY = (
    "External LDA current-bill mention source review only; packet-level dispositions "
    "are based on cached official LDA activity text that mentions the reviewed current "
    "bill. The review does not show lobbying contacts, support or opposition unless "
    "explicitly stated in the activity text, sponsor/member targeting beyond text "
    "references, committee-action influence, roll-call influence, legislative-outcome "
    "causality, campaign-finance influence, public benefit or welfare, causal capture, "
    "or model validation."
)

EVIDENCE_LAYERS = "; ".join([
    "bill_finance_lobbying_external_search_review",
    "official_lda_external_current_bill_search",
    "official_lda_filing_text_bill_identifier",
    "external_lda_activity_text_source_review",
])

MISSING_LINKS = "; ".join([
    "lobbying_contact_confirmation",
    "explicit_support_or_opposition_if_not_stated",
    "sponsor_or_member_target_beyond_activity_text_reference",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "candidate_or_committee_campaign_finance_target_join",
    "reviewed_outside_spending_target",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

FIELDNAMES = [
    "packet_review_rank",
    "packet_id",
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "client_name",
    "registrant_name",
    "filing_uuid",
    "filing_year",
    "filing_period",
    "rows_represented",
    "activity_issue_count",
    "activity_issues",
    "matched_bill_refs",
    "direction_status",
    "activity_disposition_status",
    "activity_disposition_basis",
    "target_status",
    "target_type",
    "target_text",
    "government_entity_count",
    "government_entities",
    "committee_action_status",
    "roll_call_status",
    "outcome_link_status",
    "activity_description_samples",
    "source_urls",
    "filing_document_url",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

SUPPORT_RE = re.compile(
    r"\b(support|supports|supported|supporting|endorse|endorsed|endorsing)\b",
    re.IGNORECASE,
)
OPPOSITION_RE = re.compile(
    r"\b(oppose|opposes|opposed|opposing|opposition|against)\b",
    re.IGNORECASE,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def join_values(values: set[str] | list[str]) -> str:
    return "; ".join(sorted(value for value in values if value))


def compact_space(value: str) -> str:
    return " ".join((value or "").split())


def packet_id_for(row: dict[str, str]) -> str:
    key = "|".join([
        row.get("bill_id", ""),
        row.get("filing_uuid", ""),
        row.get("client_name", ""),
        row.get("registrant_name", ""),
    ])
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def grouped_by_packet(rows: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(
            row.get("bill_id", ""),
            row.get("filing_uuid", ""),
            row.get("client_name", ""),
            row.get("registrant_name", ""),
        )].append(row)
    return [
        grouped[key]
        for key in sorted(
            grouped,
            key=lambda key: (
                parse_int(grouped[key][0].get("review_rank", "")),
                grouped[key][0].get("filing_year", ""),
                grouped[key][0].get("filing_period", ""),
                key[1],
            ),
        )
    ]


def validate_mentions(mentions: list[dict[str, str]], search_review_rows: list[dict[str, str]]) -> None:
    if not mentions:
        raise SystemExit(f"{LDA_MENTIONS} is empty.")
    search_review_by_bill = {
        row.get("bill_id", ""): row
        for row in search_review_rows
        if parse_int(row.get("lda_exact_activity_match_rows")) > 0
    }
    mention_bills = {row.get("bill_id", "") for row in mentions}
    if mention_bills != set(search_review_by_bill):
        raise SystemExit(
            "External LDA mention review must match exact-mention rows in "
            f"{EXTERNAL_SEARCH_REVIEW}: missing={sorted(set(search_review_by_bill) - mention_bills)}, "
            f"extra={sorted(mention_bills - set(search_review_by_bill))}"
        )
    for bill_id, search_row in search_review_by_bill.items():
        expected = parse_int(search_row.get("lda_exact_activity_match_rows"))
        actual = sum(1 for row in mentions if row.get("bill_id", "") == bill_id)
        if expected != actual:
            raise SystemExit(
                f"{LDA_MENTIONS}: {bill_id}: expected {expected} exact rows from "
                f"{EXTERNAL_SEARCH_REVIEW}, found {actual}."
            )
    for row in mentions:
        if row.get("exact_current_bill_match", "") != "1":
            raise SystemExit(f"{LDA_MENTIONS}: {row.get('bill_id', '')}: non-exact match row found.")
        if "official_lda_filing_text_bill_identifier" not in row.get("evidence_layers", ""):
            raise SystemExit(f"{LDA_MENTIONS}: {row.get('bill_id', '')}: missing bill-identifier layer.")


def classify_activity(descriptions: list[str]) -> tuple[str, str, str]:
    text = " ".join(descriptions)
    has_support = bool(SUPPORT_RE.search(text))
    has_opposition = bool(OPPOSITION_RE.search(text))
    has_advocacy = "advocacy" in text.casefold() or "advocat" in text.casefold()
    if has_support and has_opposition:
        return (
            "explicit_mixed_support_opposition_text_signal",
            "reviewed_current_bill_mixed_direction_from_external_activity_text",
            "The packet contains explicit support and opposition terms in activity text; this requires claim-specific follow-up before using it as a directional signal.",
        )
    if has_support:
        return (
            "explicit_support_text_signal",
            "reviewed_current_bill_support_from_external_activity_text",
            "The packet contains an explicit support term in activity text; it remains activity-text evidence only.",
        )
    if has_opposition:
        return (
            "explicit_opposition_text_signal",
            "reviewed_current_bill_opposition_from_external_activity_text",
            "The packet contains an explicit opposition term in activity text; it remains activity-text evidence only.",
        )
    if has_advocacy:
        return (
            "no_explicit_support_or_opposition",
            "reviewed_current_bill_issue_advocacy_without_direction",
            "The packet uses education or advocacy language and lists the current bill, but does not state support or opposition for the bill.",
        )
    return (
        "no_explicit_support_or_opposition",
        "reviewed_current_bill_issue_reference_without_direction",
        "The packet lists the current bill in issue/activity text, but does not state support or opposition for the bill.",
    )


def classify_target(entities: set[str]) -> tuple[str, str, str]:
    if not entities:
        return (
            "reviewed_no_government_entity_text_reference",
            "none",
            "",
        )
    return (
        "reviewed_generic_chamber_or_agency_text_reference",
        "generic_government_entities",
        join_values(entities),
    )


def snippet_for_bill(description: str, refs: set[str]) -> str:
    text = compact_space(description)
    lowered = text.casefold()
    positions = [
        lowered.find(ref.casefold())
        for ref in refs
        if ref and lowered.find(ref.casefold()) >= 0
    ]
    if not positions:
        return text[:260]
    start = max(min(positions) - 110, 0)
    end = min(min(positions) + 170, len(text))
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{text[start:end]}{suffix}"


def build_rows() -> list[dict[str, str]]:
    mentions = read_csv(LDA_MENTIONS)
    search_review_rows = read_csv(EXTERNAL_SEARCH_REVIEW)
    validate_mentions(mentions, search_review_rows)
    rows: list[dict[str, str]] = []
    for packet_rows in grouped_by_packet(mentions):
        first = packet_rows[0]
        descriptions = sorted({row.get("activity_description", "") for row in packet_rows if row.get("activity_description", "")})
        activity_issues = {row.get("activity_issue", "") for row in packet_rows if row.get("activity_issue", "")}
        matched_refs = {
            ref
            for row in packet_rows
            for ref in split_semicolon(row.get("matched_bill_refs", ""))
        }
        entities = {
            entity
            for row in packet_rows
            for entity in split_semicolon(row.get("government_entities", ""))
        }
        direction_status, disposition_status, disposition_basis = classify_activity(descriptions)
        target_status, target_type, target_text = classify_target(entities)
        snippets = [
            snippet_for_bill(description, matched_refs)
            for description in descriptions[:3]
        ]
        rows.append({
            "packet_review_rank": str(len(rows) + 1),
            "packet_id": packet_id_for(first),
            "review_rank": first.get("review_rank", ""),
            "bill_id": first.get("bill_id", ""),
            "public_law_number": first.get("public_law_number", ""),
            "policy_area": first.get("policy_area", ""),
            "client_name": first.get("client_name", ""),
            "registrant_name": first.get("registrant_name", ""),
            "filing_uuid": first.get("filing_uuid", ""),
            "filing_year": first.get("filing_year", ""),
            "filing_period": first.get("filing_period", ""),
            "rows_represented": str(len(packet_rows)),
            "activity_issue_count": str(len(activity_issues)),
            "activity_issues": join_values(activity_issues),
            "matched_bill_refs": join_values(matched_refs),
            "direction_status": direction_status,
            "activity_disposition_status": disposition_status,
            "activity_disposition_basis": disposition_basis,
            "target_status": target_status,
            "target_type": target_type,
            "target_text": target_text,
            "government_entity_count": str(len(entities)),
            "government_entities": join_values(entities),
            "committee_action_status": "no_committee_action_influence_evidence",
            "roll_call_status": "no_roll_call_influence_evidence",
            "outcome_link_status": "no_outcome_influence_evidence",
            "activity_description_samples": " || ".join(snippets),
            "source_urls": join_values({row.get("source_url", "") for row in packet_rows}),
            "filing_document_url": first.get("filing_document_url", ""),
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def sum_rows(rows: list[dict[str, str]]) -> int:
    return sum(parse_int(row.get("rows_represented")) for row in rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    disposition_counts = Counter(row["activity_disposition_status"] for row in rows)
    direction_counts = Counter(row["direction_status"] for row in rows)
    target_counts = Counter(row["target_status"] for row in rows)
    by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_bill[row["bill_id"]].append(row)
    explicit_direction_packets = [
        row for row in rows
        if row["direction_status"] != "no_explicit_support_or_opposition"
    ]
    lines = [
        "# Bill Finance/Lobbying External LDA Mention Review",
        "",
        "This report source-reviews the exact external LDA current-bill activity-text mention rows found by `reports/bill-finance-lobbying-external-search-review.*`. It classifies only the text visible in the cached LDA activity rows and remains bounded to activity-text dispositions.",
        "",
        f"- External LDA filing packets reviewed: {len(rows)}",
        f"- Exact activity-text mention rows represented: {sum_rows(rows)}",
        f"- Packets with explicit support/opposition text: {len(explicit_direction_packets)}",
        f"- Packets without explicit support/opposition text: {direction_counts['no_explicit_support_or_opposition']}",
        f"- Packets with named sponsor/member/committee target beyond generic entity text: 0",
        f"- Packets with committee-action influence evidence: 0",
        f"- Packets with roll-call influence evidence: 0",
        f"- Packets with legislative-outcome causality evidence: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Activity dispositions:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(disposition_counts.items()))
    lines.extend([
        "",
        "Target dispositions:",
    ])
    lines.extend(f"- {status}: {count}" for status, count in sorted(target_counts.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Bill | Public law | Client | Packets | Rows represented | Activity disposition summary |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ])
    for bill_id, bill_rows in sorted(by_bill.items()):
        bill_dispositions = Counter(row["activity_disposition_status"] for row in bill_rows)
        summary = "; ".join(f"{status}: {count}" for status, count in sorted(bill_dispositions.items()))
        lines.append(
            f"| `{bill_id}` | `{bill_rows[0]['public_law_number']}` | "
            f"{md_escape(bill_rows[0]['client_name'])} | {len(bill_rows)} | "
            f"{sum_rows(bill_rows)} | {md_escape(summary)} |"
        )
    lines.extend([
        "",
        "Packet review:",
        "",
        "| Rank | Bill | Filing year | Rows | Registrant | Activity disposition | Target status |",
        "| ---: | --- | --- | ---: | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['packet_review_rank']} | `{row['bill_id']}` | {row['filing_year']} | "
            f"{row['rows_represented']} | {md_escape(row['registrant_name'])} | "
            f"{row['activity_disposition_status']} | {row['target_status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No external LDA current-bill mention packets found.")
    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
