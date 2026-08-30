#!/usr/bin/env python3
"""Build a bounded Federal Register proposed-to-final rule history cache."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_API = "https://www.federalregister.gov/api/v1/documents.json"
DETAIL_API = "https://www.federalregister.gov/api/v1/documents"
USER_AGENT = "congress-institutional-simulator-validation/0.8"
AUTHORITY_CSV = Path("data/validation/raw/rulemaking_authority_linkage.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_history_linkage.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_history_linkage.metadata.md")
CLAIM_BOUNDARY = (
    "Bounded Federal Register proposed-rule search for final rules already "
    "text-verified as citing cached public laws; matches require shared RIN or "
    "docket identifiers and do not prove complete public-comment records, "
    "Unified Agenda stage coverage, enforcement outcomes, appropriations "
    "capacity, exhaustive implementation coverage, public benefit, welfare, "
    "causal effects, or model validation."
)
OUTPUT_FIELDS = [
    "public_law_number",
    "bill_id",
    "final_document_number",
    "history_status",
    "final_publication_date",
    "final_effective_date",
    "final_title",
    "final_citation",
    "agency_names",
    "regulation_id_numbers",
    "docket_ids",
    "cfr_references",
    "candidate_proposed_rule_count",
    "matched_proposed_rule_count",
    "proposed_document_numbers",
    "proposed_publication_dates",
    "proposed_titles",
    "proposed_citations",
    "proposed_comment_close_dates",
    "proposed_comment_urls",
    "proposed_regulations_docket_ids",
    "proposed_regulations_comments_urls",
    "shared_identifiers",
    "days_from_earliest_proposed_to_final",
    "source_urls",
    "api_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def api_get(url: str, retries: int = 3) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def join(values: list[str] | set[str], limit: int = 0) -> str:
    ordered = sorted({value for value in values if value})
    if limit > 0:
        ordered = ordered[:limit]
    return "; ".join(ordered)


def detail_url(document_number: str) -> str:
    return f"{DETAIL_API}/{document_number}.json"


def search_url(term: str, per_search: int) -> str:
    params: list[tuple[str, object]] = [
        ("conditions[term]", term),
        ("conditions[type][]", "PRORULE"),
        ("order", "relevance"),
        ("per_page", per_search),
    ]
    for field in (
        "document_number",
        "type",
        "title",
        "publication_date",
        "regulation_id_numbers",
        "docket_ids",
        "html_url",
    ):
        params.append(("fields[]", field))
    return f"{SEARCH_API}?{urlencode(params)}"


def normalize_rin(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().upper())


def normalize_docket(value: str) -> str:
    normalized = value.strip().upper()
    normalized = re.sub(r"\b(DOCKET|NO|NUMBER|NOS|NOS\.)\b", "", normalized)
    return re.sub(r"[^A-Z0-9]+", "", normalized)


def list_field(detail: dict[str, object], field: str) -> list[str]:
    values = detail.get(field)
    if not isinstance(values, list):
        return []
    return [str(value).strip() for value in values if str(value or "").strip()]


def agency_names(agencies: object) -> str:
    if not isinstance(agencies, list):
        return ""
    names: list[str] = []
    for agency in agencies:
        if isinstance(agency, dict):
            name = str(agency.get("name") or agency.get("raw_name") or "").strip()
            if name:
                names.append(name)
    return "; ".join(names)


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


def parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def date_not_after(value: str, ceiling: str) -> bool:
    left = parse_date(value)
    right = parse_date(ceiling)
    if left is None or right is None:
        return True
    return left <= right


def days_between(start: str, end: str) -> str:
    start_date = parse_date(start)
    end_date = parse_date(end)
    if start_date is None or end_date is None:
        return ""
    return str((end_date - start_date).days)


def identifier_sets(detail: dict[str, object]) -> tuple[set[str], set[str]]:
    rins = {normalize_rin(value) for value in list_field(detail, "regulation_id_numbers")}
    dockets = {normalize_docket(value) for value in list_field(detail, "docket_ids")}
    rins.discard("")
    dockets.discard("")
    return rins, dockets


def shared_identifiers(final_detail: dict[str, object], proposed_detail: dict[str, object]) -> set[str]:
    final_rins, final_dockets = identifier_sets(final_detail)
    proposed_rins, proposed_dockets = identifier_sets(proposed_detail)
    shared: set[str] = set()
    shared.update(f"RIN:{value}" for value in sorted(final_rins & proposed_rins))
    shared.update(f"DOCKET:{value}" for value in sorted(final_dockets & proposed_dockets))
    return shared


def search_terms(final_detail: dict[str, object]) -> list[str]:
    terms: list[str] = []
    terms.extend(list_field(final_detail, "regulation_id_numbers"))
    terms.extend(list_field(final_detail, "docket_ids"))
    seen: set[str] = set()
    unique: list[str] = []
    for term in terms:
        cleaned = term.strip()
        key = cleaned.casefold()
        if cleaned and key not in seen:
            seen.add(key)
            unique.append(cleaned)
    return unique


def search_proposed_documents(final_detail: dict[str, object], per_search: int) -> list[str]:
    documents: list[str] = []
    seen: set[str] = set()
    for term in search_terms(final_detail):
        try:
            payload = api_get(search_url(term, per_search))
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            continue
        results = payload.get("results", [])
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict):
                continue
            document_number = str(result.get("document_number") or "").strip()
            if document_number and document_number not in seen:
                seen.add(document_number)
                documents.append(document_number)
    return documents


def final_document_rows(authority_rows: list[dict[str, str]]) -> list[tuple[dict[str, str], str]]:
    rows: list[tuple[dict[str, str], str]] = []
    seen: set[tuple[str, str]] = set()
    for authority in authority_rows:
        if authority.get("linkage_status") != "federal_register_authority_match":
            continue
        public_law = authority.get("public_law_number", "").strip()
        for document_number in split_semicolon(authority.get("matched_document_numbers", "")):
            key = (public_law, document_number)
            if document_number and key not in seen:
                seen.add(key)
                rows.append((authority, document_number))
    return rows


def error_row(authority: dict[str, str], final_document_number: str, status: str) -> dict[str, str]:
    return {
        "public_law_number": authority.get("public_law_number", ""),
        "bill_id": authority.get("bill_id", ""),
        "final_document_number": final_document_number,
        "history_status": status,
        "final_publication_date": "",
        "final_effective_date": "",
        "final_title": "",
        "final_citation": "",
        "agency_names": "",
        "regulation_id_numbers": "",
        "docket_ids": "",
        "cfr_references": "",
        "candidate_proposed_rule_count": "0",
        "matched_proposed_rule_count": "0",
        "proposed_document_numbers": "",
        "proposed_publication_dates": "",
        "proposed_titles": "",
        "proposed_citations": "",
        "proposed_comment_close_dates": "",
        "proposed_comment_urls": "",
        "proposed_regulations_docket_ids": "",
        "proposed_regulations_comments_urls": "",
        "shared_identifiers": "",
        "days_from_earliest_proposed_to_final": "",
        "source_urls": "",
        "api_urls": detail_url(final_document_number) if final_document_number else "",
        "evidence_layers": "federal_register_authority_text_verified",
        "missing_links": "final_rule_detail_metadata; proposed_rule_history; complete_regulations_comments; unified_agenda_stage; enforcement_outcomes; appropriations_capacity; exhaustive_implementation_coverage; causal_implementation_effect; model_validation",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_row(
    authority: dict[str, str],
    final_document_number: str,
    args: argparse.Namespace,
) -> dict[str, str]:
    try:
        final_detail = api_get(detail_url(final_document_number))
    except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
        return error_row(authority, final_document_number, "final_rule_detail_error")

    candidate_documents = search_proposed_documents(final_detail, args.per_search)
    if args.max_proposed_per_final > 0:
        candidate_documents = candidate_documents[:args.max_proposed_per_final]

    proposed_details: list[dict[str, object]] = []
    shared_values: set[str] = set()
    for proposed_document_number in candidate_documents:
        try:
            proposed_detail = api_get(detail_url(proposed_document_number))
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            continue
        shared = shared_identifiers(final_detail, proposed_detail)
        publication_date = str(proposed_detail.get("publication_date") or "")
        final_date = str(final_detail.get("publication_date") or "")
        if shared and date_not_after(publication_date, final_date):
            proposed_details.append(proposed_detail)
            shared_values.update(shared)
        if args.sleep > 0.0:
            time.sleep(args.sleep)

    regs_values = [regulations_info(detail) for detail in proposed_details]
    proposed_dates = [str(detail.get("publication_date") or "") for detail in proposed_details]
    earliest_proposed_date = min([value for value in proposed_dates if value], default="")
    final_publication_date = str(final_detail.get("publication_date") or "")
    final_rins = list_field(final_detail, "regulation_id_numbers")
    final_dockets = list_field(final_detail, "docket_ids")
    matched_count = len(proposed_details)
    status = "proposed_rule_history_match" if matched_count else "no_proposed_rule_history_match"
    evidence_layers = [
        "federal_register_authority_text_verified",
        "final_rule_detail_metadata",
        "proposed_rule_search_by_rin_or_docket",
    ]
    if matched_count:
        evidence_layers.append("proposed_rule_shared_identifier_match")
    missing = [
        "complete_regulations_comments",
        "unified_agenda_stage",
        "enforcement_outcomes",
        "appropriations_capacity",
        "exhaustive_implementation_coverage",
        "causal_implementation_effect",
        "model_validation",
    ]
    if not matched_count:
        missing.insert(0, "proposed_rule_history")

    return {
        "public_law_number": authority.get("public_law_number", ""),
        "bill_id": authority.get("bill_id", ""),
        "final_document_number": final_document_number,
        "history_status": status,
        "final_publication_date": final_publication_date,
        "final_effective_date": str(final_detail.get("effective_on") or ""),
        "final_title": str(final_detail.get("title") or ""),
        "final_citation": str(final_detail.get("citation") or ""),
        "agency_names": agency_names(final_detail.get("agencies")),
        "regulation_id_numbers": join(final_rins),
        "docket_ids": join(final_dockets),
        "cfr_references": cfr_summary(final_detail.get("cfr_references")),
        "candidate_proposed_rule_count": str(len(candidate_documents)),
        "matched_proposed_rule_count": str(matched_count),
        "proposed_document_numbers": join([str(detail.get("document_number") or "") for detail in proposed_details]),
        "proposed_publication_dates": join(proposed_dates),
        "proposed_titles": join([str(detail.get("title") or "") for detail in proposed_details], limit=12),
        "proposed_citations": join([str(detail.get("citation") or "") for detail in proposed_details]),
        "proposed_comment_close_dates": join([str(detail.get("comments_close_on") or "") for detail in proposed_details]),
        "proposed_comment_urls": join([str(detail.get("comment_url") or "") for detail in proposed_details]),
        "proposed_regulations_docket_ids": join([str(regs.get("docket_id") or "") for regs in regs_values]),
        "proposed_regulations_comments_urls": join([str(regs.get("comments_url") or "") for regs in regs_values]),
        "shared_identifiers": join(shared_values),
        "days_from_earliest_proposed_to_final": days_between(earliest_proposed_date, final_publication_date),
        "source_urls": join(
            [str(final_detail.get("html_url") or "")]
            + [str(detail.get("html_url") or "") for detail in proposed_details]
        ),
        "api_urls": join(
            [detail_url(final_document_number)]
            + [detail_url(str(detail.get("document_number") or "")) for detail in proposed_details]
        ),
        "evidence_layers": "; ".join(evidence_layers),
        "missing_links": "; ".join(missing),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_rows(authority_rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    documents = final_document_rows(authority_rows)
    if args.limit > 0:
        documents = documents[:args.limit]
    rows: list[dict[str, str]] = []
    for index, (authority, document_number) in enumerate(documents, start=1):
        if args.progress_every > 0 and index % args.progress_every == 0:
            print(f"Checked proposed-rule history for {index} authority-matched final rules", file=sys.stderr)
        rows.append(build_row(authority, document_number, args))
        if args.sleep > 0.0:
            time.sleep(args.sleep)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    total = len(rows)
    matched_rows = [row for row in rows if row["history_status"] == "proposed_rule_history_match"]
    proposed_docs = {
        document
        for row in matched_rows
        for document in split_semicolon(row["proposed_document_numbers"])
    }
    final_docs = {row["final_document_number"] for row in rows if row["final_document_number"]}
    candidate_count = sum(int(row["candidate_proposed_rule_count"] or "0") for row in rows)
    matched_count = sum(int(row["matched_proposed_rule_count"] or "0") for row in rows)
    status_counts = Counter(row["history_status"] for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    args.metadata.write_text(
        "# Rulemaking History Linkage\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Federal Register API v1 search and single-document endpoints.\n"
        "- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api\n"
        f"- Input authority linkage file: `{args.authority_csv}`.\n"
        f"- Row limit: {args.limit if args.limit else 'all authority-matched final rules'}.\n\n"
        "Transformation:\n\n"
        "- Starts from final-rule documents already text-verified as citing cached public laws in the rulemaking authority linkage cache.\n"
        "- Fetches each final rule's Federal Register detail record.\n"
        "- Searches proposed-rule documents by the final rule's RIN and docket identifiers.\n"
        "- Keeps proposed-rule candidates only when their Federal Register metadata shares a normalized RIN or docket identifier with the final rule and the proposed-rule publication date is not later than the final rule publication date.\n"
        "- Does not fetch complete Regulations.gov comment records, Unified Agenda stages, enforcement outcomes, appropriations data, or nonpublic submitter information.\n\n"
        "Rows:\n\n"
        f"- Authority-matched final-rule rows checked: {total}.\n"
        f"- Unique final-rule documents checked: {len(final_docs)}.\n"
        f"- Final-rule rows with proposed-rule history matches: {len(matched_rows)}.\n"
        f"- Candidate proposed-rule documents inspected: {candidate_count}.\n"
        f"- Matched proposed-rule links: {matched_count}.\n"
        f"- Unique matched proposed-rule documents: {len(proposed_docs)}.\n\n"
        "History statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authority-csv", type=Path, default=AUTHORITY_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--per-search", type=int, default=20)
    parser.add_argument("--max-proposed-per-final", type=int, default=30)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--limit", type=int, default=0, help="Maximum authority-matched final-rule documents to check; 0 means all.")
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.authority_csv.exists():
        raise SystemExit(f"{args.authority_csv} is missing; run make build-rulemaking-authority-linkage-raw first.")
    authority_rows = read_csv(args.authority_csv)
    rows = build_rows(authority_rows, args)
    if not rows:
        raise SystemExit("No authority-matched final-rule documents were available to check.")
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
