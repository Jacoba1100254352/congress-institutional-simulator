#!/usr/bin/env python3
"""Write a bounded source-text review report for exact LDA bill mentions."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


RAW_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
BILL_ACTION_CONTEXT = Path("reports/lobbying-bill-action-context.csv")
OUT_CSV = Path("reports/lobbying-bill-text-review.csv")
OUT_MD = Path("reports/lobbying-bill-text-review.md")

FIELDNAMES = [
    "review_rank",
    "source_row_fingerprint",
    "bill_id",
    "public_law_number",
    "policy_area",
    "filing_uuid",
    "filing_year",
    "filing_period",
    "client_name",
    "registrant_name",
    "activity_issue",
    "matched_bill_refs",
    "stored_activity_text_bill_reference_status",
    "bill_reference_context",
    "bill_reference_context_chars",
    "support_text_signal",
    "opposition_text_signal",
    "position_or_activity_text_signal",
    "text_review_status",
    "specific_bill_text_disposition",
    "government_entity_scope",
    "possible_member_or_committee_reference",
    "source_reviewed_exact_bill_text",
    "evidence_layers",
    "missing_links",
    "filing_document_url",
    "source_urls",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Official LDA activity-text review for exact bill mentions only; support, "
    "opposition, position, or bill-list text signals describe phrases in the "
    "disclosed filing text and do not show sponsor/member targeting, committee-action "
    "influence, roll-call influence, legislative-outcome causality, public benefit, "
    "welfare, causal capture, or model validation."
)

BASE_MISSING_LINKS = [
    "manual_source_review_confirmation",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
]

REFETCH_MISSING_LINK = "full_activity_text_refetch_for_truncated_rows"

SUPPORT_PATTERNS = [
    ("in_support_of", re.compile(r"\bin support of\b", re.IGNORECASE)),
    ("support_for", re.compile(r"\bsupport for\b", re.IGNORECASE)),
    ("supporting", re.compile(r"\bsupporting\b", re.IGNORECASE)),
    ("support_passage", re.compile(r"\bsupport passage\b", re.IGNORECASE)),
    (
        "support_bill_or_legislation",
        re.compile(
            r"\bsupports?\s+(?:the\s+)?(?:bill|legislation|reauthorization|"
            r"passage|provisions|funding|authorized|appropriations|research|"
            r"addressing|codification)\b",
            re.IGNORECASE,
        ),
    ),
    ("advocacy_for", re.compile(r"\badvocat(?:e|ed|ing)\s+for\b", re.IGNORECASE)),
]

OPPOSITION_PATTERNS = [
    ("oppose", re.compile(r"\boppos(?:e|es|ed|ing)\b", re.IGNORECASE)),
    ("opposition_to", re.compile(r"\bopposition to\b", re.IGNORECASE)),
    ("against_passage", re.compile(r"\bagainst\s+(?:passage|the bill|legislation)\b", re.IGNORECASE)),
    ("block_passage", re.compile(r"\bblock(?:ing)?\s+(?:passage|the bill|legislation)\b", re.IGNORECASE)),
]

POSITION_PATTERNS = [
    ("position_on", re.compile(r"\bposition on\b", re.IGNORECASE)),
    ("all_provisions", re.compile(r"\ball provisions\b", re.IGNORECASE)),
    ("issues_related_to", re.compile(r"\bissues? (?:and discussions? )?related to\b", re.IGNORECASE)),
    ("related_to", re.compile(r"\brelated to\b", re.IGNORECASE)),
    ("lobbied_for_or_on", re.compile(r"\blobbied (?:for|on)\b", re.IGNORECASE)),
    ("monitoring", re.compile(r"\bmonitor(?:ed|ing)?\b", re.IGNORECASE)),
    ("regarding", re.compile(r"\bregarding\b", re.IGNORECASE)),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(value: str) -> str:
    return " ".join((value or "").split())


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def split_values(value: str) -> list[str]:
    result: list[str] = []
    for part in (value or "").split(";"):
        clean = normalize_space(part)
        if clean and clean not in result:
            result.append(clean)
    return result


def join_values(values: list[str]) -> str:
    result: list[str] = []
    for value in values:
        clean = normalize_space(value)
        if clean and clean not in result:
            result.append(clean)
    return "; ".join(result)


def row_fingerprint(row: dict[str, str]) -> str:
    fields = [
        "bill_id",
        "filing_uuid",
        "client_name",
        "registrant_name",
        "activity_issue",
        "activity_description",
        "matched_bill_refs",
    ]
    source = "\x1f".join(row.get(field, "") for field in fields)
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def bill_reference_pattern(bill_id: str) -> re.Pattern[str]:
    parts = bill_id.split("-")
    if len(parts) < 3:
        return re.compile(re.escape(bill_id), re.IGNORECASE)
    bill_type = parts[1].lower()
    number = re.escape(parts[2])
    if bill_type == "hr":
        pattern = rf"(?<![A-Za-z0-9])(?:H\.?\s*R\.?|HR|H R)\s*\.?\s*{number}(?!\d)"
    elif bill_type == "s":
        pattern = rf"(?<![A-Za-z0-9])S\.?\s*{number}(?!\d)"
    else:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(bill_type)}\.?\s*{number}(?!\d)"
    return re.compile(pattern, re.IGNORECASE)


def bill_reference_context(description: str, bill_id: str) -> tuple[str, bool]:
    text = normalize_space(description)
    match = bill_reference_pattern(bill_id).search(text)
    if not match:
        return text[:360], False
    start = max(0, match.start() - 170)
    end = min(len(text), match.end() + 170)
    context = text[start:end].strip()
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    return context, True


def pattern_names(text: str, patterns: list[tuple[str, re.Pattern[str]]]) -> list[str]:
    return [name for name, pattern in patterns if pattern.search(text)]


def text_review_status(
    support_signals: list[str],
    opposition_signals: list[str],
    position_signals: list[str],
) -> tuple[str, str]:
    if support_signals and opposition_signals:
        return (
            "exact_bill_text_with_mixed_support_opposition_signal",
            "mixed_support_and_opposition_terms_in_activity_text",
        )
    if support_signals:
        return (
            "exact_bill_text_with_explicit_support_signal",
            "explicit_support_in_activity_text",
        )
    if opposition_signals:
        return (
            "exact_bill_text_with_explicit_opposition_signal",
            "explicit_opposition_in_activity_text",
        )
    if position_signals:
        return (
            "exact_bill_text_with_position_or_activity_signal",
            "position_or_activity_text_without_direction",
        )
    return (
        "exact_bill_text_bill_list_or_title_only",
        "bill_reference_only_no_position_signal",
    )


def government_entity_scope(entities_value: str) -> str:
    entities = split_values(entities_value)
    has_house = any(entity.upper() == "HOUSE OF REPRESENTATIVES" for entity in entities)
    has_senate = any(entity.upper() == "SENATE" for entity in entities)
    agency_count = sum(
        1
        for entity in entities
        if entity.upper() not in {"HOUSE OF REPRESENTATIVES", "SENATE"}
    )
    if has_house and has_senate and agency_count:
        return "house_senate_and_agency_entities_disclosed"
    if has_house and has_senate:
        return "house_and_senate_entities_disclosed"
    if has_house or has_senate:
        return "single_chamber_entity_disclosed"
    if agency_count:
        return "agency_entities_only_disclosed"
    return "no_government_entity_disclosed"


def possible_member_or_committee_reference(context: str) -> str:
    if re.search(r"\b(?:committee|subcommittee|chair(?:man|woman)?|ranking member)\b", context, re.IGNORECASE):
        return "possible_committee_reference_in_activity_text"
    if re.search(r"\b(?:rep\.|representative|senator)\s+[A-Z][A-Za-z'-]+", context):
        return "possible_member_reference_in_activity_text"
    if re.search(r"\bsen\.\s+[A-Z][A-Za-z'-]+", context):
        return "possible_member_reference_in_activity_text"
    return "not_detected_in_activity_text"


def action_context_by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("bill_id", "").strip(): row
        for row in rows
        if row.get("bill_id", "").strip()
    }


def build_rows(
    mention_rows: list[dict[str, str]],
    action_context_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    context_by_bill = action_context_by_bill(action_context_rows)
    output: list[dict[str, str]] = []
    for mention in mention_rows:
        bill_id = mention.get("bill_id", "").strip()
        if not bill_id:
            continue
        action_context = context_by_bill.get(bill_id, {})
        context, located_reference = bill_reference_context(mention.get("activity_description", ""), bill_id)
        if located_reference:
            support_signals = pattern_names(context, SUPPORT_PATTERNS)
            opposition_signals = pattern_names(context, OPPOSITION_PATTERNS)
            position_signals = pattern_names(context, POSITION_PATTERNS)
            status, disposition = text_review_status(support_signals, opposition_signals, position_signals)
            source_reviewed = "1"
            stored_status = "bill_reference_located_in_stored_activity_text"
            missing_links = BASE_MISSING_LINKS
        else:
            support_signals = []
            opposition_signals = []
            position_signals = []
            status = "matched_reference_not_located_in_stored_activity_text"
            disposition = "raw_search_exact_match_but_stored_excerpt_needs_refetch_for_text_review"
            source_reviewed = "0"
            stored_status = "matched_reference_not_located_in_stored_activity_text"
            missing_links = [REFETCH_MISSING_LINK, *BASE_MISSING_LINKS]
        action_source_urls = [
            url for url in split_values(action_context.get("source_urls", ""))
            if "congress.gov" in url
        ]
        source_urls = join_values([
            mention.get("filing_document_url", ""),
            mention.get("source_url", ""),
            *action_source_urls,
        ])
        output.append({
            "review_rank": "0",
            "source_row_fingerprint": row_fingerprint(mention),
            "bill_id": bill_id,
            "public_law_number": action_context.get("public_law_number", mention.get("public_law_number", "")),
            "policy_area": action_context.get("policy_area", mention.get("policy_area", "")),
            "filing_uuid": mention.get("filing_uuid", ""),
            "filing_year": mention.get("filing_year", ""),
            "filing_period": mention.get("filing_period", ""),
            "client_name": mention.get("client_name", ""),
            "registrant_name": mention.get("registrant_name", ""),
            "activity_issue": mention.get("activity_issue", ""),
            "matched_bill_refs": mention.get("matched_bill_refs", ""),
            "stored_activity_text_bill_reference_status": stored_status,
            "bill_reference_context": context,
            "bill_reference_context_chars": str(len(context)),
            "support_text_signal": join_values(support_signals) or "none_detected",
            "opposition_text_signal": join_values(opposition_signals) or "none_detected",
            "position_or_activity_text_signal": join_values(position_signals) or "none_detected",
            "text_review_status": status,
            "specific_bill_text_disposition": disposition,
            "government_entity_scope": government_entity_scope(mention.get("government_entities", "")),
            "possible_member_or_committee_reference": possible_member_or_committee_reference(context),
            "source_reviewed_exact_bill_text": source_reviewed,
            "evidence_layers": "; ".join([
                "official_lda_filing_text_bill_identifier",
                "official_lda_activity_text_source_review",
                "deterministic_activity_text_position_signal",
                "congressgov_bill_action_metadata_context",
            ]),
            "missing_links": "; ".join(missing_links),
            "filing_document_url": mention.get("filing_document_url", ""),
            "source_urls": source_urls,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    output.sort(key=lambda row: (row["bill_id"], row["filing_year"], row["filing_period"], row["client_name"], row["source_row_fingerprint"]))
    for index, row in enumerate(output, start=1):
        row["review_rank"] = str(index)
    return output


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def status_count(rows: list[dict[str, str]], status: str) -> int:
    return sum(1 for row in rows if row.get("text_review_status") == status)


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["text_review_status"] for row in rows)
    bill_ids = {row["bill_id"] for row in rows}
    filings = {row["filing_uuid"] for row in rows if row["filing_uuid"]}
    clients = {row["client_name"] for row in rows if row["client_name"]}
    stored_reference_rows = status_count(rows, "matched_reference_not_located_in_stored_activity_text")
    visible_reference_rows = len(rows) - stored_reference_rows
    explicit_support_rows = status_count(rows, "exact_bill_text_with_explicit_support_signal")
    explicit_opposition_rows = status_count(rows, "exact_bill_text_with_explicit_opposition_signal")
    mixed_rows = status_count(rows, "exact_bill_text_with_mixed_support_opposition_signal")
    position_rows = status_count(rows, "exact_bill_text_with_position_or_activity_signal")
    list_rows = status_count(rows, "exact_bill_text_bill_list_or_title_only")
    chamber_rows = sum(
        1
        for row in rows
        if row["government_entity_scope"] in {
            "house_senate_and_agency_entities_disclosed",
            "house_and_senate_entities_disclosed",
            "single_chamber_entity_disclosed",
        }
    )
    lines = [
        "# LDA Bill Text Review",
        "",
        "This report reviews the official LDA activity text for rows that already contain exact current-bill identifiers. It classifies text signals in the activity description; it is not evidence that lobbying changed any committee, roll-call, or enactment outcome.",
        "",
        f"- Cached exact LDA activity-text match rows represented: {len(rows)}",
        f"- Rows with bill reference located in stored activity text: {visible_reference_rows}",
        f"- Rows needing full activity-text refetch before text review: {stored_reference_rows}",
        f"- Public-law bill IDs represented: {len(bill_ids)}",
        f"- Unique LDA filing IDs represented: {len(filings)}",
        f"- Unique LDA clients represented: {len(clients)}",
        f"- Rows with explicit support text signal: {explicit_support_rows}",
        f"- Rows with explicit opposition text signal: {explicit_opposition_rows}",
        f"- Rows with mixed support/opposition text signal: {mixed_rows}",
        f"- Rows with position/activity text signal but no direction: {position_rows}",
        f"- Rows with bill-list or title-only text: {list_rows}",
        f"- Rows with disclosed House or Senate entity context: {chamber_rows}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Text review statuses:",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")

    by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_bill[row["bill_id"]].append(row)
    lines.extend([
        "",
        "| Bill | Public law | Policy area | Rows | Visible refs | Needs refetch | Clients | Support rows | Opposition rows | Position rows | List-only rows | Possible member/committee refs |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for bill_id, bill_rows in sorted(by_bill.items(), key=lambda item: (-len(item[1]), item[0])):
        sample = bill_rows[0]
        possible_refs = sum(
            1 for row in bill_rows
            if row["possible_member_or_committee_reference"] != "not_detected_in_activity_text"
        )
        lines.append(
            f"| `{bill_id}` | `{sample['public_law_number']}` | {sample['policy_area'] or '---'} | "
            f"{len(bill_rows)} | "
            f"{len(bill_rows) - status_count(bill_rows, 'matched_reference_not_located_in_stored_activity_text')} | "
            f"{status_count(bill_rows, 'matched_reference_not_located_in_stored_activity_text')} | "
            f"{len({row['client_name'] for row in bill_rows if row['client_name']})} | "
            f"{status_count(bill_rows, 'exact_bill_text_with_explicit_support_signal')} | "
            f"{status_count(bill_rows, 'exact_bill_text_with_explicit_opposition_signal')} | "
            f"{status_count(bill_rows, 'exact_bill_text_with_position_or_activity_signal')} | "
            f"{status_count(bill_rows, 'exact_bill_text_bill_list_or_title_only')} | {possible_refs} |"
        )

    lines.extend([
        "",
        "Sample reviewed contexts:",
        "",
        "| Bill | Client | Period | Status | Trigger phrases | Context |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    status_priority = {
        "exact_bill_text_with_explicit_support_signal": 0,
        "exact_bill_text_with_explicit_opposition_signal": 1,
        "exact_bill_text_with_mixed_support_opposition_signal": 2,
        "exact_bill_text_with_position_or_activity_signal": 3,
        "exact_bill_text_bill_list_or_title_only": 4,
    }
    sample_rows = sorted(
        [row for row in rows if row["text_review_status"] != "matched_reference_not_located_in_stored_activity_text"],
        key=lambda row: (
            status_priority.get(row["text_review_status"], 99),
            row["bill_id"],
            row["client_name"],
            row["review_rank"],
        ),
    )[:20]
    for row in sample_rows:
        trigger_values = [
            value
            for field in ("support_text_signal", "opposition_text_signal", "position_or_activity_text_signal")
            for value in split_values(row[field])
            if value != "none_detected"
        ]
        triggers = join_values(trigger_values)
        lines.append(
            f"| `{row['bill_id']}` | {md_escape(row['client_name'])} | "
            f"{md_escape(row['filing_year'] + ' ' + row['filing_period'])} | "
            f"{row['text_review_status']} | {md_escape(triggers or 'none_detected')} | "
            f"{md_escape(row['bill_reference_context'])} |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    mentions = read_csv(RAW_MENTIONS)
    action_context = read_csv(BILL_ACTION_CONTEXT)
    if not mentions:
        raise SystemExit(f"{RAW_MENTIONS} is empty.")
    if not action_context:
        raise SystemExit(f"{BILL_ACTION_CONTEXT} is empty; run make lobbying-bill-action-context first.")
    rows = build_rows(mentions, action_context)
    if len(rows) != len(mentions):
        raise SystemExit("text review row count does not match exact LDA mention row count.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
