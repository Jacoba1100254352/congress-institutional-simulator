#!/usr/bin/env python3
"""Build Federal Register document-metadata links for final-rule rows."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE = "https://www.federalregister.gov/api/v1/documents"
USER_AGENT = "congress-institutional-simulator-validation/0.6"
API_TIMEOUT_SECONDS = 30.0
RULEMAKING_CSV = Path("data/validation/raw/rulemaking_implementation.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_implementation_linkage.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_implementation_linkage.metadata.md")
OUTPUT_FIELDS = [
    "law_id",
    "document_number",
    "linkage_status",
    "final_rule_date",
    "effective_date",
    "title",
    "federal_register_citation",
    "agency_names",
    "agency_ids",
    "agency_slugs",
    "docket_id_raw",
    "federal_register_docket_ids",
    "regulation_id_number_raw",
    "regulation_id_numbers",
    "cfr_references",
    "regulations_docket_id",
    "regulations_document_id",
    "regulations_agency_id",
    "regulations_comments_count",
    "regulations_supporting_documents_count",
    "regulations_checked_at",
    "comments_close_on",
    "comment_url",
    "regulations_comments_url",
    "significant",
    "page_length",
    "topics",
    "source_url",
    "api_url",
]


def api_get(document_number: str, retries: int = 3) -> dict[str, object]:
    request_url = f"{API_BASE}/{document_number}.json"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=API_TIMEOUT_SECONDS) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def join_values(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return "; ".join(str(value) for value in values if str(value or "").strip())


def agency_field(agencies: object, field: str) -> str:
    if not isinstance(agencies, list):
        return ""
    values: list[str] = []
    for agency in agencies:
        if isinstance(agency, dict) and agency.get(field) not in (None, ""):
            values.append(str(agency[field]))
    return "; ".join(values)


def cfr_summary(references: object) -> str:
    if not isinstance(references, list):
        return ""
    values: list[str] = []
    for reference in references:
        if not isinstance(reference, dict):
            continue
        title = reference.get("title")
        part = reference.get("part")
        if title and part:
            values.append(f"{title} CFR {part}")
    return "; ".join(values)


def regulations_info(detail: dict[str, object]) -> dict[str, object]:
    info = detail.get("regulations_dot_gov_info")
    return info if isinstance(info, dict) else {}


def source_api_url(document_number: str) -> str:
    return f"{API_BASE}/{document_number}.json"


def error_row(source: dict[str, str], linkage_status: str) -> dict[str, str]:
    document_number = source.get("law_id", "")
    return {
        "law_id": document_number,
        "document_number": document_number,
        "linkage_status": linkage_status,
        "final_rule_date": source.get("final_rule_date", ""),
        "effective_date": source.get("effective_date", ""),
        "title": source.get("title", ""),
        "federal_register_citation": "",
        "agency_names": source.get("agency", ""),
        "agency_ids": "",
        "agency_slugs": "",
        "docket_id_raw": source.get("docket_id", ""),
        "federal_register_docket_ids": "",
        "regulation_id_number_raw": source.get("regulation_id_number", ""),
        "regulation_id_numbers": "",
        "cfr_references": source.get("cfr_reference", ""),
        "regulations_docket_id": "",
        "regulations_document_id": "",
        "regulations_agency_id": "",
        "regulations_comments_count": "",
        "regulations_supporting_documents_count": "",
        "regulations_checked_at": "",
        "comments_close_on": "",
        "comment_url": "",
        "regulations_comments_url": "",
        "significant": "",
        "page_length": "",
        "topics": "",
        "source_url": source.get("source_url", ""),
        "api_url": source_api_url(document_number) if document_number else "",
    }


def build_linkage_row(source: dict[str, str], detail: dict[str, object]) -> dict[str, str]:
    document_number = str(detail.get("document_number") or source.get("law_id") or "")
    regs = regulations_info(detail)
    status = "federal_register_document_metadata" if detail.get("document_number") else "unmatched"
    return {
        "law_id": source.get("law_id", ""),
        "document_number": document_number,
        "linkage_status": status,
        "final_rule_date": str(detail.get("publication_date") or source.get("final_rule_date") or ""),
        "effective_date": str(detail.get("effective_on") or source.get("effective_date") or ""),
        "title": str(detail.get("title") or source.get("title") or ""),
        "federal_register_citation": str(detail.get("citation") or ""),
        "agency_names": agency_field(detail.get("agencies"), "name") or source.get("agency", ""),
        "agency_ids": agency_field(detail.get("agencies"), "id"),
        "agency_slugs": agency_field(detail.get("agencies"), "slug"),
        "docket_id_raw": source.get("docket_id", ""),
        "federal_register_docket_ids": join_values(detail.get("docket_ids")),
        "regulation_id_number_raw": source.get("regulation_id_number", ""),
        "regulation_id_numbers": join_values(detail.get("regulation_id_numbers")),
        "cfr_references": cfr_summary(detail.get("cfr_references")) or source.get("cfr_reference", ""),
        "regulations_docket_id": str(regs.get("docket_id") or ""),
        "regulations_document_id": str(regs.get("document_id") or ""),
        "regulations_agency_id": str(regs.get("agency_id") or ""),
        "regulations_comments_count": str(regs.get("comments_count") if regs.get("comments_count") is not None else ""),
        "regulations_supporting_documents_count": str(
            regs.get("supporting_documents_count")
            if regs.get("supporting_documents_count") is not None
            else ""
        ),
        "regulations_checked_at": str(regs.get("checked_regulationsdotgov_at") or ""),
        "comments_close_on": str(detail.get("comments_close_on") or ""),
        "comment_url": str(detail.get("comment_url") or ""),
        "regulations_comments_url": str(regs.get("comments_url") or ""),
        "significant": "1" if detail.get("significant") is True else "0" if detail.get("significant") is False else "",
        "page_length": str(detail.get("page_length") or ""),
        "topics": join_values(detail.get("topics")),
        "source_url": str(detail.get("html_url") or source.get("source_url") or ""),
        "api_url": source_api_url(document_number),
    }


def build_rows(source_rows: list[dict[str, str]], sleep_seconds: float, progress_every: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for source in source_rows:
        document_number = source.get("law_id", "").strip()
        if not document_number:
            rows.append(error_row(source, "unmatched"))
            continue
        if document_number in seen:
            continue
        seen.add(document_number)
        if progress_every > 0 and len(seen) % progress_every == 0:
            print(f"Fetched Federal Register metadata for {len(seen)} final-rule documents", file=sys.stderr)
        try:
            detail = api_get(document_number)
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            rows.append(error_row(source, "api_error"))
            continue
        rows.append(build_linkage_row(source, detail))
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    total = len(rows)
    linked = sum(1 for row in rows if row["linkage_status"] == "federal_register_document_metadata")
    regulations_rows = sum(1 for row in rows if row["regulations_docket_id"] or row["regulations_document_id"])
    comment_count_rows = sum(1 for row in rows if row["regulations_comments_count"] != "")
    cfr_rows = sum(1 for row in rows if row["cfr_references"])
    status_counts = Counter(row["linkage_status"] for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    args.metadata.write_text(
        "# Rulemaking Implementation Metadata Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Federal Register API v1 single-document endpoint.\n"
        "- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api\n"
        f"- Input rulemaking file: `{args.rulemaking_csv}`.\n"
        f"- Row limit: {args.limit if args.limit else 'all'}.\n\n"
        "Transformation:\n\n"
        "- Reads Federal Register final-rule rows from the cached implementation dataset.\n"
        "- Fetches document-level public metadata by Federal Register document number.\n"
        "- Retains docket IDs, RINs, CFR references, agency identifiers, topics, page length, significant-rule flag, and Federal Register-exposed Regulations.gov docket/comment metadata when present.\n"
        "- Does not fetch full rule text, proposed-rule histories, public-law authorities, enforcement outcomes, appropriations records, or private comment submitter fields.\n\n"
        "Rows:\n\n"
        f"- Unique final-rule document rows: {total}.\n"
        f"- Rows with Federal Register document metadata: {linked}.\n"
        f"- Rows with Federal Register-exposed Regulations.gov document or docket IDs: {regulations_rows}.\n"
        f"- Rows with Federal Register-exposed Regulations.gov comment counts: {comment_count_rows}.\n"
        f"- Rows with CFR references: {cfr_rows}.\n"
        f"- Linkage share: {(linked / total) if total else 0.0:.3f}.\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        "This file links bounded final-rule rows to official Federal Register document metadata and, when exposed by Federal Register, Regulations.gov docket, document, and comment-count metadata. "
        "It does not provide public-law or U.S. Code authority linkage, proposed-to-final rule histories, complete Regulations.gov comment records, enforcement outcomes, appropriations capacity, or observed nonenforcement.\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rulemaking-csv", type=Path, default=RULEMAKING_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--limit", type=int, default=0, help="Maximum unique final-rule rows to fetch; 0 means all.")
    parser.add_argument("--progress-every", type=int, default=50)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.rulemaking_csv.exists():
        raise SystemExit(f"{args.rulemaking_csv} is missing; run make build-rulemaking-implementation-raw first.")
    source_rows = read_csv(args.rulemaking_csv)
    if args.limit > 0:
        source_rows = source_rows[:args.limit]
    rows = build_rows(source_rows, args.sleep, args.progress_every)
    if not rows:
        raise SystemExit("No Federal Register document numbers were available to link.")
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
