#!/usr/bin/env python3
"""Build a sanitized Regulations.gov public comment-detail review cache."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


COMMENTS_API = "https://api.regulations.gov/v4/comments"
USER_AGENT = "congress-institutional-simulator-validation/0.9"
COMMENT_RECORDS_CSV = Path("data/validation/raw/rulemaking_comment_records.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_comment_text_review.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_comment_text_review.metadata.md")

COMPLETE_RECORD_STATUS = "complete_comment_record_metadata_retrieved"
OMITTED_FIELDS = (
    "comment_body; firstName; lastName; address1; address2; city; stateProvinceRegion; "
    "zip; email; phone; fax; organization; trackingNbr"
)
CLAIM_BOUNDARY = (
    "Sanitized Regulations.gov public comment-detail review for complete bounded "
    "comment-record rows and bounded partial-docket samples. It records text "
    "availability, normalized text hash, text length, attachment count, source "
    "comment-record status, and coarse implementation-related cue flags while "
    "omitting the comment body and submitter/contact fields. Partial sample rows "
    "do not prove complete docket coverage. This is not a full comment-text "
    "corpus, attachment text, commenter-identity validation, sentiment or "
    "position coding, representativeness evidence, Unified Agenda stage coverage, "
    "enforcement outcome, appropriations capacity, implementation-outcome "
    "evidence, public benefit, welfare, causal-effect, or model-validation "
    "evidence."
)

OUTPUT_FIELDS = [
    "public_law_number",
    "bill_id",
    "docket_id",
    "comment_id",
    "comment_record_retrieval_status",
    "comment_detail_review_scope",
    "source_retrieved_comment_count",
    "source_expected_comment_count",
    "detail_fetch_status",
    "api_key_mode",
    "document_type",
    "posted_date",
    "receive_date",
    "modify_date",
    "withdrawn",
    "comment_on_document_id",
    "comment_text_available",
    "comment_text_character_count",
    "comment_text_word_count",
    "comment_text_sha256",
    "implementation_timing_cue",
    "cost_or_burden_cue",
    "compliance_or_standard_cue",
    "safety_or_security_cue",
    "program_design_cue",
    "cue_terms",
    "attachment_count",
    "attachment_detail_status",
    "omitted_fields",
    "api_urls",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CUE_PATTERNS = {
    "implementation_timing_cue": (
        "deadline",
        "delay",
        "effective date",
        "implementation",
        "phase",
        "timeline",
        "transition",
    ),
    "cost_or_burden_cue": (
        "administrative burden",
        "burden",
        "cost",
        "expense",
        "paperwork",
    ),
    "compliance_or_standard_cue": (
        "certification",
        "compliance",
        "criterion",
        "criteria",
        "requirement",
        "standard",
    ),
    "safety_or_security_cue": (
        "risk",
        "safety",
        "secure",
        "security",
        "vulnerability",
    ),
    "program_design_cue": (
        "application",
        "eligibility",
        "program",
        "selection",
        "service",
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def join(values: list[str] | set[str]) -> str:
    return "; ".join(sorted({value for value in values if value}))


def api_key_mode(api_key: str, allow_demo_key: bool) -> tuple[str, str]:
    if api_key:
        return api_key, "env_or_argument_key"
    if allow_demo_key:
        return "DEMO_KEY", "public_demo_key"
    return "", "missing_api_key"


def display_detail_url(comment_id: str) -> str:
    return f"{COMMENTS_API}/{comment_id}"


def request_detail_url(comment_id: str, api_key: str) -> str:
    query = urlencode({"api_key": api_key})
    return f"{display_detail_url(comment_id)}?{query}"


def api_get(url: str, retries: int = 3) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code < 500:
                raise
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
        except (TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def detail_error_status(exc: BaseException) -> str:
    if isinstance(exc, HTTPError):
        return f"comment_detail_api_error:HTTPError{exc.code}"
    return f"comment_detail_api_error:{type(exc).__name__}"


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    unescaped = html.unescape(value)
    return re.sub(r"\s+", " ", unescaped).strip()


def bool_text(value: object) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return ""


def attachment_count(payload: dict[str, object]) -> tuple[int, str]:
    relationships = payload.get("data", {}).get("relationships", {})  # type: ignore[union-attr]
    if not isinstance(relationships, dict):
        return 0, "no_relationships"
    attachments = relationships.get("attachments", {})
    if not isinstance(attachments, dict):
        return 0, "no_attachment_relationship"
    data = attachments.get("data", [])
    if isinstance(data, list):
        return len(data), "attachment_relationship_counted"
    return 0, "attachment_relationship_not_list"


def cue_flags(text: str) -> tuple[dict[str, str], str]:
    lowered = text.lower()
    flags: dict[str, str] = {}
    found: list[str] = []
    for field, terms in CUE_PATTERNS.items():
        matched = [term for term in terms if term in lowered]
        flags[field] = "yes" if matched else "no"
        found.extend(matched)
    return flags, join(found)


def detail_scope(record: dict[str, str]) -> str:
    if record.get("retrieval_status") == COMPLETE_RECORD_STATUS:
        return "complete_docket_detail"
    return "partial_docket_sample_detail"


def source_evidence_layer(record: dict[str, str]) -> str:
    if record.get("retrieval_status") == COMPLETE_RECORD_STATUS:
        return "regulations_gov_complete_comment_record_metadata"
    return "regulations_gov_partial_comment_record_metadata"


def eligible_record_rows(rows: list[dict[str, str]], public_laws: set[str]) -> list[dict[str, str]]:
    complete: list[dict[str, str]] = []
    partial: list[dict[str, str]] = []
    for row in rows:
        if public_laws and row.get("public_law_number", "").strip() not in public_laws:
            continue
        comment_ids = split_semicolon(row.get("retrieved_comment_ids", ""))
        if not comment_ids:
            continue
        target = complete if row.get("retrieval_status") == COMPLETE_RECORD_STATUS else partial
        for sequence, comment_id in enumerate(comment_ids, start=1):
            item = dict(row)
            item["comment_id"] = comment_id
            item["source_comment_sequence"] = str(sequence)
            target.append(item)
    sort_key = lambda row: (
        row.get("public_law_number", ""),
        row.get("docket_id", ""),
        row.get("comment_id", ""),
    )
    return sorted(
        complete,
        key=sort_key,
    ) + sorted(
        partial,
        key=lambda row: (
            row.get("public_law_number", ""),
            row.get("docket_id", ""),
            row.get("comment_id", ""),
        ),
    )


def error_row(record: dict[str, str], status: str, detail_url: str, key_mode: str) -> dict[str, str]:
    missing_links = [
        "complete_public_comment_detail",
        "full_comment_text_corpus",
        "attachment_text_review",
        "commenter_identity_review",
        "sentiment_or_position_coding",
        "unified_agenda_stage",
        "enforcement_outcomes",
        "appropriations_capacity",
        "causal_implementation_effect",
        "model_validation",
    ]
    if record.get("retrieval_status") != COMPLETE_RECORD_STATUS:
        missing_links.insert(0, "complete_regulations_comments")
    return {
        "public_law_number": record.get("public_law_number", ""),
        "bill_id": record.get("bill_id", ""),
        "docket_id": record.get("docket_id", ""),
        "comment_id": record.get("comment_id", ""),
        "comment_record_retrieval_status": record.get("retrieval_status", ""),
        "comment_detail_review_scope": detail_scope(record),
        "source_retrieved_comment_count": record.get("retrieved_comment_count", ""),
        "source_expected_comment_count": record.get("expected_comment_count", ""),
        "detail_fetch_status": status,
        "api_key_mode": key_mode,
        "document_type": "",
        "posted_date": "",
        "receive_date": "",
        "modify_date": "",
        "withdrawn": "",
        "comment_on_document_id": "",
        "comment_text_available": "no",
        "comment_text_character_count": "0",
        "comment_text_word_count": "0",
        "comment_text_sha256": "",
        "implementation_timing_cue": "no",
        "cost_or_burden_cue": "no",
        "compliance_or_standard_cue": "no",
        "safety_or_security_cue": "no",
        "program_design_cue": "no",
        "cue_terms": "",
        "attachment_count": "0",
        "attachment_detail_status": "",
        "omitted_fields": OMITTED_FIELDS,
        "api_urls": detail_url,
        "source_urls": record.get("source_urls", ""),
        "evidence_layers": source_evidence_layer(record),
        "missing_links": "; ".join(missing_links),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_detail_row(record: dict[str, str], args: argparse.Namespace, key: str, key_mode: str) -> dict[str, str]:
    comment_id = record["comment_id"]
    detail_url = display_detail_url(comment_id)
    if not key:
        return error_row(record, "api_key_required", detail_url, key_mode)
    try:
        payload = api_get(request_detail_url(comment_id, key))
    except (HTTPError, TimeoutError, URLError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        return error_row(record, detail_error_status(exc), detail_url, key_mode)
    data = payload.get("data", {})
    attributes = data.get("attributes", {}) if isinstance(data, dict) else {}
    if not isinstance(attributes, dict):
        return error_row(record, "comment_detail_missing_attributes", detail_url, key_mode)
    text = normalize_text(attributes.get("comment"))
    text_available = bool(text)
    cue_map, terms = cue_flags(text)
    attachments, attachment_status = attachment_count(payload)
    evidence_layers = [
        source_evidence_layer(record),
        "regulations_gov_public_comment_detail_metadata",
    ]
    missing_links = [
        "full_comment_text_corpus",
        "attachment_text_review",
        "commenter_identity_review",
        "sentiment_or_position_coding",
        "unified_agenda_stage",
        "enforcement_outcomes",
        "appropriations_capacity",
        "causal_implementation_effect",
        "model_validation",
    ]
    if record.get("retrieval_status") != COMPLETE_RECORD_STATUS:
        missing_links.insert(0, "complete_regulations_comments")
    if text_available:
        evidence_layers.append("sanitized_comment_text_availability_hash")
    else:
        missing_links.insert(0, "comment_text_body_available")
    return {
        "public_law_number": record.get("public_law_number", ""),
        "bill_id": record.get("bill_id", ""),
        "docket_id": record.get("docket_id", ""),
        "comment_id": comment_id,
        "comment_record_retrieval_status": record.get("retrieval_status", ""),
        "comment_detail_review_scope": detail_scope(record),
        "source_retrieved_comment_count": record.get("retrieved_comment_count", ""),
        "source_expected_comment_count": record.get("expected_comment_count", ""),
        "detail_fetch_status": "comment_detail_fetched",
        "api_key_mode": key_mode,
        "document_type": str(attributes.get("documentType") or ""),
        "posted_date": str(attributes.get("postedDate") or "")[:10],
        "receive_date": str(attributes.get("receiveDate") or "")[:10],
        "modify_date": str(attributes.get("modifyDate") or "")[:10],
        "withdrawn": bool_text(attributes.get("withdrawn")),
        "comment_on_document_id": str(attributes.get("commentOnDocumentId") or ""),
        "comment_text_available": "yes" if text_available else "no",
        "comment_text_character_count": str(len(text)),
        "comment_text_word_count": str(len(text.split())) if text else "0",
        "comment_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else "",
        **cue_map,
        "cue_terms": terms,
        "attachment_count": str(attachments),
        "attachment_detail_status": attachment_status,
        "omitted_fields": OMITTED_FIELDS,
        "api_urls": detail_url,
        "source_urls": record.get("source_urls", ""),
        "evidence_layers": "; ".join(evidence_layers),
        "missing_links": "; ".join(missing_links),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]], key_mode: str) -> None:
    statuses = Counter(row["detail_fetch_status"] for row in rows)
    scopes = Counter(row["comment_detail_review_scope"] for row in rows)
    fetched_rows = sum(1 for row in rows if row["detail_fetch_status"] == "comment_detail_fetched")
    text_rows = sum(1 for row in rows if row["comment_text_available"] == "yes")
    public_laws = {row["public_law_number"] for row in rows if row["public_law_number"]}
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    scope_lines = "\n".join(f"- {scope}: {count}" for scope, count in sorted(scopes.items()))
    args.metadata.write_text(
        "# Rulemaking Comment Text Review\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Regulations.gov API v4 comment detail endpoint.\n"
        "- API documentation: https://open.gsa.gov/api/regulationsgov/\n"
        f"- Input comment-record file: `{args.comment_records_csv}`.\n"
        f"- API key mode: {key_mode}.\n"
        f"- Max comments fetched: {args.max_comments}.\n"
        f"- Public-law filter: {args.public_laws or 'all'}.\n"
        "- API key required: yes for non-demo production use; the bounded default "
        "may use the public DEMO_KEY for low-volume detail checks.\n\n"
        "Transformation:\n\n"
        "- Starts from complete Regulations.gov comment-record metadata rows and bounded partial rows with retrieved comment IDs.\n"
        "- Prioritizes complete-docket detail rows, then adds partial-docket sample rows up to the max-comments limit.\n"
        "- Fetches bounded public comment-detail records by comment ID.\n"
        "- Records comment text availability, normalized text hash, text length, attachment count, and coarse implementation-related cue flags.\n"
        "- Omits the full comment body and submitter/contact fields from the CSV and report.\n"
        "- Does not fetch attachment text, validate commenter identity, code sentiment, or infer implementation outcomes.\n\n"
        "Rows:\n\n"
        f"- Public-law rows represented: {len(public_laws)}.\n"
        f"- Public comment-detail rows: {len(rows)}.\n"
        f"- Detail rows fetched: {fetched_rows}.\n"
        f"- Rows with public comment text available and hashed: {text_rows}.\n\n"
        "Review scopes:\n\n"
        f"{scope_lines}\n\n"
        "Detail statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def preserve_existing_successful_cache(args: argparse.Namespace, rows: list[dict[str, str]]) -> bool:
    if not args.preserve_existing_successful_cache:
        return False
    if any(row["detail_fetch_status"] == "comment_detail_fetched" for row in rows):
        return False
    if not args.output.exists():
        return False
    existing_rows = read_csv(args.output)
    if any(row.get("detail_fetch_status") == "comment_detail_fetched" for row in existing_rows):
        print(
            f"Preserved {args.output}: refresh produced no fetched detail rows; "
            "use --no-preserve-existing-successful-cache to overwrite."
        )
        return True
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comment-records-csv", type=Path, default=COMMENT_RECORDS_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--api-key", default=os.environ.get("REGULATIONS_GOV_API_KEY", ""))
    parser.add_argument("--allow-demo-key", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--public-laws", default="", help="Comma-separated public-law numbers to include; empty means all.")
    parser.add_argument("--max-comments", type=int, default=25, help="Maximum detail rows, prioritizing complete-docket rows before partial samples.")
    parser.add_argument(
        "--preserve-existing-successful-cache",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Do not overwrite an existing cache with fetched detail rows when the current refresh produces only errors.",
    )
    parser.add_argument("--sleep", "--sleep-seconds", dest="sleep_seconds", type=float, default=0.1)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.comment_records_csv.exists():
        raise SystemExit(f"{args.comment_records_csv} is missing; run make build-rulemaking-comment-records-raw first.")
    records = read_csv(args.comment_records_csv)
    if not records:
        raise SystemExit(f"{args.comment_records_csv} is empty.")
    public_laws = {value.strip() for value in args.public_laws.split(",") if value.strip()}
    eligible = eligible_record_rows(records, public_laws)
    if not eligible:
        raise SystemExit("No comment-record metadata rows with retrieved comment IDs were available.")
    eligible = eligible[: args.max_comments]
    key, key_mode = api_key_mode(args.api_key, args.allow_demo_key)
    rows: list[dict[str, str]] = []
    for index, record in enumerate(eligible, start=1):
        rows.append(build_detail_row(record, args, key, key_mode))
        if args.sleep_seconds > 0 and index < len(eligible):
            time.sleep(args.sleep_seconds)
    if preserve_existing_successful_cache(args, rows):
        return 0
    write_csv(rows, args.output)
    write_metadata(args, rows, key_mode)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
