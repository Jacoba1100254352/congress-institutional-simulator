#!/usr/bin/env python3
"""Build a bounded rulemaking comment-metadata cache for authority chains."""

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


DETAIL_API = "https://www.federalregister.gov/api/v1/documents"
USER_AGENT = "congress-institutional-simulator-validation/0.8"
HISTORY_CSV = Path("data/validation/raw/rulemaking_history_linkage.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_comment_metadata.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_comment_metadata.metadata.md")
CLAIM_BOUNDARY = (
    "Bounded Federal Register-exposed Regulations.gov metadata for "
    "authority-matched final-rule and matched proposed-rule records only; this "
    "is not complete Regulations.gov comment-record evidence, commenter "
    "identity or comment-text evidence, Unified Agenda stage coverage, "
    "enforcement outcomes, appropriations capacity, exhaustive implementation "
    "coverage, public benefit, welfare, causal effects, or model validation."
)

HISTORY_FIELDS = [
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
    "matched_proposed_rule_count",
    "proposed_document_numbers",
    "proposed_comment_close_dates",
    "proposed_regulations_docket_ids",
    "proposed_regulations_comments_urls",
    "shared_identifiers",
    "days_from_earliest_proposed_to_final",
]

OUTPUT_FIELDS = HISTORY_FIELDS + [
    "final_detail_status",
    "final_regulations_docket_id",
    "final_regulations_document_id",
    "final_regulations_agency_id",
    "final_regulations_comments_count",
    "final_regulations_supporting_documents_count",
    "final_regulations_checked_at",
    "final_regulations_comments_url",
    "final_comment_url",
    "final_comments_close_on",
    "proposed_detail_fetch_count",
    "proposed_regulations_docket_count",
    "proposed_regulations_docket_ids_refetched",
    "proposed_regulations_comment_url_count",
    "proposed_regulations_comments_urls_refetched",
    "proposed_comment_count_rows",
    "proposed_comment_count_total",
    "proposed_positive_comment_count_rows",
    "proposed_comments_close_date_count_refetched",
    "proposed_comments_close_dates_refetched",
    "comment_metadata_status",
    "source_urls",
    "api_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

COMMENT_METADATA_STATUSES = {
    "final_and_proposed_comment_metadata",
    "proposed_comment_metadata_only",
    "final_comment_metadata_only",
    "no_comment_metadata",
    "final_detail_error",
}


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


def detail_url(document_number: str) -> str:
    return f"{DETAIL_API}/{document_number}.json"


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def join(values: list[str] | set[str], limit: int = 0) -> str:
    ordered = sorted({value for value in values if value})
    if limit > 0:
        ordered = ordered[:limit]
    return "; ".join(ordered)


def regulations_info(detail: dict[str, object]) -> dict[str, object]:
    info = detail.get("regulations_dot_gov_info")
    return info if isinstance(info, dict) else {}


def value(info: dict[str, object], key: str) -> str:
    current = info.get(key)
    if current is None:
        return ""
    return str(current).strip()


def detail_value(detail: dict[str, object], key: str) -> str:
    current = detail.get(key)
    if current is None:
        return ""
    return str(current).strip()


def parse_int(value_text: str) -> int | None:
    if not value_text:
        return None
    try:
        return int(value_text)
    except ValueError:
        return None


def has_final_comment_metadata(final_info: dict[str, object], final_detail: dict[str, object]) -> bool:
    return any(
        value(final_info, field)
        for field in (
            "docket_id",
            "document_id",
            "comments_count",
            "comments_url",
            "supporting_documents_count",
        )
    ) or any(
        detail_value(final_detail, field)
        for field in ("comment_url", "comments_close_on")
    )


def has_proposed_comment_metadata(proposed_details: list[dict[str, object]]) -> bool:
    for detail in proposed_details:
        info = regulations_info(detail)
        if any(
            value(info, field)
            for field in (
                "docket_id",
                "document_id",
                "comments_count",
                "comments_url",
                "supporting_documents_count",
            )
        ):
            return True
        if detail_value(detail, "comment_url") or detail_value(detail, "comments_close_on"):
            return True
    return False


def comment_metadata_status(
    final_detail_status: str,
    final_metadata: bool,
    proposed_metadata: bool,
) -> str:
    if final_detail_status != "federal_register_final_detail_fetched":
        return "final_detail_error"
    if final_metadata and proposed_metadata:
        return "final_and_proposed_comment_metadata"
    if proposed_metadata:
        return "proposed_comment_metadata_only"
    if final_metadata:
        return "final_comment_metadata_only"
    return "no_comment_metadata"


def build_row(history: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    row = {field: history.get(field, "") for field in HISTORY_FIELDS}
    final_document_number = history.get("final_document_number", "").strip()
    final_detail: dict[str, object] = {}
    final_detail_status = "federal_register_final_detail_error"
    api_urls = [detail_url(final_document_number)] if final_document_number else []
    source_urls = split_semicolon(history.get("source_urls", ""))

    if final_document_number:
        try:
            final_detail = api_get(detail_url(final_document_number))
            final_detail_status = "federal_register_final_detail_fetched"
            html_url = detail_value(final_detail, "html_url")
            if html_url:
                source_urls.append(html_url)
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            final_detail = {}

    proposed_details: list[dict[str, object]] = []
    for proposed_document_number in split_semicolon(history.get("proposed_document_numbers", "")):
        api_urls.append(detail_url(proposed_document_number))
        try:
            proposed_detail = api_get(detail_url(proposed_document_number))
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            continue
        proposed_details.append(proposed_detail)
        html_url = detail_value(proposed_detail, "html_url")
        if html_url:
            source_urls.append(html_url)
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    final_info = regulations_info(final_detail)
    proposed_infos = [regulations_info(detail) for detail in proposed_details]
    proposed_comment_counts = [
        parsed
        for parsed in (
            parse_int(value(info, "comments_count")) for info in proposed_infos
        )
        if parsed is not None
    ]
    final_metadata = has_final_comment_metadata(final_info, final_detail)
    proposed_metadata = has_proposed_comment_metadata(proposed_details)
    status = comment_metadata_status(final_detail_status, final_metadata, proposed_metadata)
    evidence_layers = [
        "rulemaking_history_linkage",
        "federal_register_document_detail_metadata",
    ]
    if final_metadata or proposed_metadata:
        evidence_layers.append("federal_register_exposed_regulations_gov_comment_metadata")
    missing_links = [
        "complete_regulations_comments",
        "unified_agenda_stage",
        "enforcement_outcomes",
        "appropriations_capacity",
        "exhaustive_implementation_coverage",
        "causal_implementation_effect",
        "model_validation",
    ]

    row.update({
        "final_detail_status": final_detail_status,
        "final_regulations_docket_id": value(final_info, "docket_id"),
        "final_regulations_document_id": value(final_info, "document_id"),
        "final_regulations_agency_id": value(final_info, "agency_id"),
        "final_regulations_comments_count": value(final_info, "comments_count"),
        "final_regulations_supporting_documents_count": value(final_info, "supporting_documents_count"),
        "final_regulations_checked_at": value(final_info, "checked_regulationsdotgov_at"),
        "final_regulations_comments_url": value(final_info, "comments_url"),
        "final_comment_url": detail_value(final_detail, "comment_url"),
        "final_comments_close_on": detail_value(final_detail, "comments_close_on"),
        "proposed_detail_fetch_count": str(len(proposed_details)),
        "proposed_regulations_docket_count": str(len({
            value(info, "docket_id") for info in proposed_infos if value(info, "docket_id")
        })),
        "proposed_regulations_docket_ids_refetched": join([
            value(info, "docket_id") for info in proposed_infos
        ]),
        "proposed_regulations_comment_url_count": str(len({
            value(info, "comments_url") for info in proposed_infos if value(info, "comments_url")
        })),
        "proposed_regulations_comments_urls_refetched": join([
            value(info, "comments_url") for info in proposed_infos
        ]),
        "proposed_comment_count_rows": str(len(proposed_comment_counts)),
        "proposed_comment_count_total": str(sum(proposed_comment_counts)),
        "proposed_positive_comment_count_rows": str(sum(1 for count in proposed_comment_counts if count > 0)),
        "proposed_comments_close_date_count_refetched": str(len({
            detail_value(detail, "comments_close_on")
            for detail in proposed_details
            if detail_value(detail, "comments_close_on")
        })),
        "proposed_comments_close_dates_refetched": join([
            detail_value(detail, "comments_close_on") for detail in proposed_details
        ]),
        "comment_metadata_status": status,
        "source_urls": join(source_urls),
        "api_urls": join(api_urls),
        "evidence_layers": "; ".join(evidence_layers),
        "missing_links": "; ".join(missing_links),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    return row


def build_rows(history_rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    rows = history_rows[: args.limit] if args.limit > 0 else history_rows
    output: list[dict[str, str]] = []
    for index, history in enumerate(rows, start=1):
        if args.progress_every > 0 and index % args.progress_every == 0:
            print(f"Checked comment metadata for {index} authority-matched final rules", file=sys.stderr)
        output.append(build_row(history, args))
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)
    return output


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["comment_metadata_status"] for row in rows)
    final_fetched = sum(1 for row in rows if row["final_detail_status"] == "federal_register_final_detail_fetched")
    final_docket_rows = sum(1 for row in rows if row["final_regulations_docket_id"])
    final_comment_count_rows = sum(1 for row in rows if row["final_regulations_comments_count"])
    final_positive_comment_rows = sum(
        1
        for row in rows
        if (parse_int(row["final_regulations_comments_count"]) or 0) > 0
    )
    proposed_docket_rows = sum(1 for row in rows if int(row["proposed_regulations_docket_count"] or "0") > 0)
    proposed_comment_url_rows = sum(1 for row in rows if int(row["proposed_regulations_comment_url_count"] or "0") > 0)
    proposed_comment_count_rows = sum(1 for row in rows if int(row["proposed_comment_count_rows"] or "0") > 0)
    proposed_positive_comment_rows = sum(1 for row in rows if int(row["proposed_positive_comment_count_rows"] or "0") > 0)
    proposed_comment_total = sum(int(row["proposed_comment_count_total"] or "0") for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    args.metadata.write_text(
        "# Rulemaking Comment Metadata\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Federal Register API v1 single-document endpoint.\n"
        "- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api\n"
        f"- Input history linkage file: `{args.history_csv}`.\n"
        f"- Row limit: {args.limit if args.limit else 'all rulemaking history rows'}.\n"
        "- API key required: no.\n\n"
        "Transformation:\n\n"
        "- Starts from authority-matched final-rule rows in the rulemaking history cache.\n"
        "- Refetches each final-rule Federal Register detail record.\n"
        "- Refetches matched proposed-rule Federal Register detail records already retained by shared RIN or docket identifiers.\n"
        "- Extracts only Federal Register-exposed Regulations.gov docket, comment URL, comment-count, and comment-close metadata.\n"
        "- Does not fetch complete Regulations.gov comment records, commenter identities, comment text, Unified Agenda stages, enforcement outcomes, appropriations data, or nonpublic submitter information.\n\n"
        "Rows:\n\n"
        f"- Authority-matched final-rule rows reviewed: {len(rows)}.\n"
        f"- Rows with final Federal Register detail fetched: {final_fetched}.\n"
        f"- Rows with final Regulations.gov docket metadata: {final_docket_rows}.\n"
        f"- Rows with final comments-count metadata: {final_comment_count_rows}.\n"
        f"- Rows with final positive comments counts: {final_positive_comment_rows}.\n"
        f"- Rows with proposed-rule Regulations.gov docket metadata: {proposed_docket_rows}.\n"
        f"- Rows with proposed-rule comment URLs: {proposed_comment_url_rows}.\n"
        f"- Rows with proposed-rule comments-count metadata: {proposed_comment_count_rows}.\n"
        f"- Rows with proposed-rule positive comments counts: {proposed_positive_comment_rows}.\n"
        f"- Proposed-rule comments counted in exposed metadata: {proposed_comment_total}.\n\n"
        "Comment metadata statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history-csv", type=Path, default=HISTORY_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--sleep", "--sleep-seconds", dest="sleep_seconds", type=float, default=0.02)
    parser.add_argument("--limit", type=int, default=0, help="Maximum history rows to check; 0 means all.")
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.history_csv.exists():
        raise SystemExit(f"{args.history_csv} is missing; run make build-rulemaking-history-linkage-raw first.")
    history_rows = read_csv(args.history_csv)
    if not history_rows:
        raise SystemExit(f"{args.history_csv} is empty.")
    rows = build_rows(history_rows, args)
    if not rows:
        raise SystemExit("No rulemaking history rows were available to check.")
    invalid_statuses = {row["comment_metadata_status"] for row in rows} - COMMENT_METADATA_STATUSES
    if invalid_statuses:
        raise SystemExit(f"internal error: invalid comment metadata statuses {sorted(invalid_statuses)}")
    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
