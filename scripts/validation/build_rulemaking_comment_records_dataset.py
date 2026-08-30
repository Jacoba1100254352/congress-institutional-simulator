#!/usr/bin/env python3
"""Build a bounded Regulations.gov comment-record metadata cache."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


COMMENTS_API = "https://api.regulations.gov/v4/comments"
USER_AGENT = "congress-institutional-simulator-validation/0.9"
COMMENT_METADATA_CSV = Path("data/validation/raw/rulemaking_comment_metadata.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_comment_records.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_comment_records.metadata.md")
CLAIM_BOUNDARY = (
    "Bounded Regulations.gov comment-record metadata for Federal "
    "Register-exposed dockets only; complete rows mean all public comment "
    "record metadata returned by the Regulations.gov comments endpoint for a "
    "docket within the configured retrieval threshold or no comments expected "
    "from Federal Register metadata. This is not comment-text, attachment, "
    "commenter-identity, sentiment, Unified Agenda, enforcement, "
    "appropriations, implementation-outcome, public benefit, welfare, "
    "causal-effect, or model-validation evidence."
)

OUTPUT_FIELDS = [
    "public_law_number",
    "bill_id",
    "docket_id",
    "source_contexts",
    "final_document_numbers",
    "proposed_document_numbers",
    "expected_comment_count",
    "expected_comment_count_source",
    "retrieval_status",
    "retrieval_detail",
    "api_key_mode",
    "api_total_comment_count",
    "retrieved_comment_count",
    "retrieved_comment_ids",
    "retrieved_comment_document_types",
    "retrieved_comment_posted_dates",
    "withdrawn_comment_count",
    "api_urls",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

COMPLETE_STATUSES = {
    "complete_comment_record_metadata_retrieved",
    "complete_no_comments_expected",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def join(values: list[str] | set[str], limit: int = 0) -> str:
    ordered = sorted({value for value in values if value})
    if limit > 0:
        ordered = ordered[:limit]
    return "; ".join(ordered)


def parse_int(value: str) -> int | None:
    if not value.strip():
        return None
    try:
        return int(value)
    except ValueError:
        return None


def display_api_url(docket_id: str, page_size: int, page_number: int) -> str:
    query = urlencode({
        "filter[docketId]": docket_id,
        "page[size]": str(page_size),
        "page[number]": str(page_number),
    })
    return f"{COMMENTS_API}?{query}"


def request_api_url(docket_id: str, page_size: int, page_number: int, api_key: str) -> str:
    query = urlencode({
        "filter[docketId]": docket_id,
        "page[size]": str(page_size),
        "page[number]": str(page_number),
        "api_key": api_key,
    })
    return f"{COMMENTS_API}?{query}"


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


def api_key_mode(api_key: str, allow_demo_key: bool) -> tuple[str, str]:
    if api_key:
        return api_key, "env_or_argument_key"
    if allow_demo_key:
        return "DEMO_KEY", "public_demo_key"
    return "", "missing_api_key"


def add_target(
    targets: dict[tuple[str, str], dict[str, object]],
    row: dict[str, str],
    docket_id: str,
    expected_count: int | None,
    expected_source: str,
    source_context: str,
) -> None:
    if not docket_id:
        return
    key = (row.get("public_law_number", "").strip(), docket_id)
    target = targets.setdefault(
        key,
        {
            "public_law_number": row.get("public_law_number", "").strip(),
            "bill_id": row.get("bill_id", "").strip(),
            "docket_id": docket_id,
            "source_contexts": set(),
            "final_document_numbers": set(),
            "proposed_document_numbers": set(),
            "expected_counts": [],
            "expected_sources": set(),
            "has_unknown_expected_count": False,
            "source_urls": set(),
            "api_urls": set(),
        },
    )
    target["source_contexts"].add(source_context)  # type: ignore[index, union-attr]
    target["expected_sources"].add(expected_source)  # type: ignore[index, union-attr]
    if expected_count is None:
        target["has_unknown_expected_count"] = True
    else:
        target["expected_counts"].append(expected_count)  # type: ignore[index, union-attr]
    final_document = row.get("final_document_number", "").strip()
    if source_context.startswith("final_rule") and final_document:
        target["final_document_numbers"].add(final_document)  # type: ignore[index, union-attr]
    if source_context.startswith("proposed_rule"):
        for document in split_semicolon(row.get("proposed_document_numbers", "")):
            target["proposed_document_numbers"].add(document)  # type: ignore[index, union-attr]
    for source_url in split_semicolon(row.get("source_urls", "")):
        target["source_urls"].add(source_url)  # type: ignore[index, union-attr]
    for api_url in split_semicolon(row.get("api_urls", "")):
        target["api_urls"].add(api_url)  # type: ignore[index, union-attr]


def build_targets(
    metadata_rows: list[dict[str, str]],
    public_laws: set[str],
) -> list[dict[str, object]]:
    targets: dict[tuple[str, str], dict[str, object]] = {}
    for row in metadata_rows:
        public_law = row.get("public_law_number", "").strip()
        if public_laws and public_law not in public_laws:
            continue
        final_count = parse_int(row.get("final_regulations_comments_count", ""))
        add_target(
            targets,
            row,
            row.get("final_regulations_docket_id", "").strip(),
            final_count,
            "federal_register_final_regulations_comments_count",
            f"final_rule:{row.get('final_document_number', '').strip()}",
        )

        proposed_dockets = split_semicolon(row.get("proposed_regulations_docket_ids_refetched", ""))
        proposed_total = parse_int(row.get("proposed_comment_count_total", ""))
        proposed_count_rows = parse_int(row.get("proposed_comment_count_rows", "")) or 0
        for docket_id in proposed_dockets:
            expected = proposed_total if len(proposed_dockets) == 1 else None
            source = "federal_register_proposed_regulations_comments_count"
            if len(proposed_dockets) > 1 and proposed_count_rows > 0:
                source = "ambiguous_multi_docket_proposed_comment_count_total"
            add_target(
                targets,
                row,
                docket_id,
                expected,
                source,
                f"proposed_rule:{row.get('proposed_document_numbers', '').strip()}",
            )
    return sorted(
        targets.values(),
        key=lambda target: (
            str(target["public_law_number"]),
            str(target["docket_id"]),
        ),
    )


def summarize_expected(target: dict[str, object]) -> tuple[str, str]:
    counts = target["expected_counts"]  # type: ignore[index]
    unknown = bool(target["has_unknown_expected_count"])
    if unknown and not counts:
        return "", "unknown"
    if unknown:
        return str(max(counts)), "at_least_known_count_with_ambiguous_context"
    if counts:
        return str(max(counts)), "max_federal_register_exposed_count"
    return "", "missing"


def fetch_comments(
    docket_id: str,
    expected_count: int,
    args: argparse.Namespace,
    key: str,
    key_mode: str,
) -> dict[str, str]:
    if expected_count == 0:
        return {
            "retrieval_status": "complete_no_comments_expected",
            "retrieval_detail": "Federal Register metadata exposes zero comments for this docket.",
            "api_key_mode": "not_used_zero_expected",
            "api_total_comment_count": "0",
            "retrieved_comment_count": "0",
            "retrieved_comment_ids": "",
            "retrieved_comment_document_types": "",
            "retrieved_comment_posted_dates": "",
            "withdrawn_comment_count": "0",
            "api_urls": display_api_url(docket_id, args.page_size, 1),
        }
    if expected_count > args.max_expected_comments:
        return {
            "retrieval_status": "skipped_high_volume_comment_docket",
            "retrieval_detail": (
                f"Expected {expected_count} comments exceeds bounded retrieval "
                f"limit {args.max_expected_comments}."
            ),
            "api_key_mode": "not_used_high_volume_skip",
            "api_total_comment_count": "",
            "retrieved_comment_count": "0",
            "retrieved_comment_ids": "",
            "retrieved_comment_document_types": "",
            "retrieved_comment_posted_dates": "",
            "withdrawn_comment_count": "0",
            "api_urls": display_api_url(docket_id, args.page_size, 1),
        }
    if not key:
        return {
            "retrieval_status": "api_key_required",
            "retrieval_detail": "Regulations.gov API requires an api_key for comment records.",
            "api_key_mode": key_mode,
            "api_total_comment_count": "",
            "retrieved_comment_count": "0",
            "retrieved_comment_ids": "",
            "retrieved_comment_document_types": "",
            "retrieved_comment_posted_dates": "",
            "withdrawn_comment_count": "0",
            "api_urls": display_api_url(docket_id, args.page_size, 1),
        }

    comment_ids: list[str] = []
    document_types: list[str] = []
    posted_dates: list[str] = []
    withdrawn_count = 0
    api_total = ""
    api_urls: list[str] = []
    status = "partial_comment_record_metadata_retrieved"
    detail = ""
    try:
        for page_number in range(1, args.max_pages + 1):
            api_urls.append(display_api_url(docket_id, args.page_size, page_number))
            payload = api_get(request_api_url(docket_id, args.page_size, page_number, key))
            data = payload.get("data", [])
            meta = payload.get("meta", {})
            if isinstance(meta, dict) and meta.get("totalElements") is not None:
                api_total = str(meta.get("totalElements"))
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    comment_id = str(item.get("id") or "").strip()
                    if comment_id:
                        comment_ids.append(comment_id)
                    attributes = item.get("attributes", {})
                    if isinstance(attributes, dict):
                        document_type = str(attributes.get("documentType") or "").strip()
                        if document_type:
                            document_types.append(document_type)
                        posted_date = str(attributes.get("postedDate") or "").strip()
                        if posted_date:
                            posted_dates.append(posted_date[:10])
                        if attributes.get("withdrawn") is True:
                            withdrawn_count += 1
            has_next = bool(meta.get("hasNextPage")) if isinstance(meta, dict) else False
            if not has_next:
                break
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
        retrieved_count = len(set(comment_ids))
        api_total_int = parse_int(api_total)
        if api_total_int == expected_count and retrieved_count == expected_count:
            status = "complete_comment_record_metadata_retrieved"
            detail = "Retrieved every public comment record metadata row reported by the API."
        elif api_total_int is not None and api_total_int != expected_count:
            status = "comment_record_count_mismatch"
            detail = (
                f"API total {api_total_int} does not match Federal Register-exposed "
                f"expected count {expected_count}."
            )
        else:
            detail = (
                f"Retrieved {retrieved_count} records against expected count {expected_count}; "
                "pagination or API metadata did not prove completeness."
            )
        return {
            "retrieval_status": status,
            "retrieval_detail": detail,
            "api_key_mode": key_mode,
            "api_total_comment_count": api_total,
            "retrieved_comment_count": str(retrieved_count),
            "retrieved_comment_ids": join(comment_ids),
            "retrieved_comment_document_types": join(document_types),
            "retrieved_comment_posted_dates": join(posted_dates),
            "withdrawn_comment_count": str(withdrawn_count),
            "api_urls": "; ".join(api_urls),
        }
    except (HTTPError, TimeoutError, URLError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        retrieved_count = len(set(comment_ids))
        error_status = (
            "partial_comment_record_metadata_api_error"
            if retrieved_count > 0
            else "comment_record_api_error"
        )
        return {
            "retrieval_status": error_status,
            "retrieval_detail": (
                f"{type(exc).__name__} while fetching Regulations.gov comments "
                f"after retrieving {retrieved_count} unique metadata rows."
            ),
            "api_key_mode": key_mode,
            "api_total_comment_count": api_total,
            "retrieved_comment_count": str(retrieved_count),
            "retrieved_comment_ids": join(comment_ids),
            "retrieved_comment_document_types": join(document_types),
            "retrieved_comment_posted_dates": join(posted_dates),
            "withdrawn_comment_count": str(withdrawn_count),
            "api_urls": "; ".join(api_urls) or display_api_url(docket_id, args.page_size, 1),
        }


def build_row(target: dict[str, object], args: argparse.Namespace, key: str, key_mode: str) -> dict[str, str]:
    expected_text, expected_source = summarize_expected(target)
    expected_count = parse_int(expected_text) if expected_text else None
    if expected_count is None:
        retrieval = {
            "retrieval_status": "expected_comment_count_unknown",
            "retrieval_detail": "Federal Register metadata did not expose a docket-specific comment count.",
            "api_key_mode": "not_used_unknown_expected_count",
            "api_total_comment_count": "",
            "retrieved_comment_count": "0",
            "retrieved_comment_ids": "",
            "retrieved_comment_document_types": "",
            "retrieved_comment_posted_dates": "",
            "withdrawn_comment_count": "0",
            "api_urls": display_api_url(str(target["docket_id"]), args.page_size, 1),
        }
    else:
        retrieval = fetch_comments(str(target["docket_id"]), expected_count, args, key, key_mode)

    evidence_layers = ["federal_register_exposed_regulations_gov_comment_metadata"]
    if retrieval["retrieval_status"] in COMPLETE_STATUSES:
        evidence_layers.append("regulations_gov_complete_comment_record_metadata")
    elif (parse_int(retrieval["retrieved_comment_count"]) or 0) > 0:
        evidence_layers.append("regulations_gov_partial_comment_record_metadata")
    missing_links = [
        "comment_text_or_attachment_review",
        "commenter_identity_review",
        "unified_agenda_stage",
        "enforcement_outcomes",
        "appropriations_capacity",
        "causal_implementation_effect",
        "model_validation",
    ]
    if retrieval["retrieval_status"] not in COMPLETE_STATUSES:
        missing_links.insert(0, "complete_regulations_comments")

    return {
        "public_law_number": str(target["public_law_number"]),
        "bill_id": str(target["bill_id"]),
        "docket_id": str(target["docket_id"]),
        "source_contexts": join(target["source_contexts"]),  # type: ignore[arg-type]
        "final_document_numbers": join(target["final_document_numbers"]),  # type: ignore[arg-type]
        "proposed_document_numbers": join(target["proposed_document_numbers"]),  # type: ignore[arg-type]
        "expected_comment_count": expected_text,
        "expected_comment_count_source": expected_source,
        **retrieval,
        "source_urls": join(target["source_urls"]),  # type: ignore[arg-type]
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


def row_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("public_law_number", "").strip(), row.get("docket_id", "").strip())


def merge_existing_rows(new_rows: list[dict[str, str]], output: Path) -> list[dict[str, str]]:
    if not output.exists():
        return new_rows
    existing_rows = read_csv(output)
    merged = {row_key(row): {field: row.get(field, "") for field in OUTPUT_FIELDS} for row in existing_rows}
    for row in new_rows:
        merged[row_key(row)] = {field: row.get(field, "") for field in OUTPUT_FIELDS}
    return [
        merged[key]
        for key in sorted(
            merged,
            key=lambda item: (item[0], item[1]),
        )
    ]


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]], key_mode: str) -> None:
    statuses = Counter(row["retrieval_status"] for row in rows)
    complete_rows = sum(1 for row in rows if row["retrieval_status"] in COMPLETE_STATUSES)
    fetched_comments = sum(parse_int(row["retrieved_comment_count"]) or 0 for row in rows)
    expected_comments = sum(parse_int(row["expected_comment_count"]) or 0 for row in rows)
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(statuses.items()))
    args.metadata.write_text(
        "# Rulemaking Comment Records\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Regulations.gov API v4 comments endpoint.\n"
        "- API documentation: https://open.gsa.gov/api/regulationsgov/\n"
        f"- Input comment metadata file: `{args.comment_metadata_csv}`.\n"
        f"- API key mode: {key_mode}.\n"
        f"- Max expected comments fetched per docket: {args.max_expected_comments}.\n"
        f"- Page size: {args.page_size}; max pages: {args.max_pages}.\n"
        f"- Public-law filter: {args.public_laws or 'all'}.\n"
        f"- Merged with existing output: {'yes' if args.merge_existing else 'no'}.\n"
        "- API key required: yes for non-demo production use; the bounded default "
        "may use the public DEMO_KEY for low-volume or resumed bounded retrievals.\n\n"
        "Transformation:\n\n"
        "- Starts from Federal Register-exposed Regulations.gov docket and comment-count metadata.\n"
        "- Builds one public-law/docket row per final or proposed-rule docket.\n"
        "- Fetches only dockets at or below the configured expected-comment threshold.\n"
        "- Preserves partial metadata rows when an API error occurs after records have been retrieved.\n"
        "- Treats zero-comment dockets as complete no-comment rows without calling the API.\n"
        "- Does not fetch comment text, attachments, private submitter details, Unified Agenda stages, enforcement outcomes, or appropriations records.\n\n"
        "Rows:\n\n"
        f"- Public-law/docket rows: {len(rows)}.\n"
        f"- Complete docket rows: {complete_rows}.\n"
        f"- Expected comments counted from Federal Register metadata: {expected_comments}.\n"
        f"- Retrieved public comment record metadata rows: {fetched_comments}.\n\n"
        "Retrieval statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comment-metadata-csv", type=Path, default=COMMENT_METADATA_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--api-key", default=os.environ.get("REGULATIONS_GOV_API_KEY", ""))
    parser.add_argument("--allow-demo-key", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--public-laws", default="", help="Comma-separated public-law numbers to include; empty means all.")
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="Merge filtered output rows into the existing output CSV instead of replacing the whole cache.",
    )
    parser.add_argument("--max-expected-comments", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=250)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--sleep", "--sleep-seconds", dest="sleep_seconds", type=float, default=0.1)
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.comment_metadata_csv.exists():
        raise SystemExit(f"{args.comment_metadata_csv} is missing; run make build-rulemaking-comment-metadata-raw first.")
    metadata_rows = read_csv(args.comment_metadata_csv)
    if not metadata_rows:
        raise SystemExit(f"{args.comment_metadata_csv} is empty.")
    public_laws = {value.strip() for value in args.public_laws.split(",") if value.strip()}
    key, key_mode = api_key_mode(args.api_key, args.allow_demo_key)
    targets = build_targets(metadata_rows, public_laws)
    if not targets:
        raise SystemExit("No Federal Register-exposed Regulations.gov dockets were available.")
    rows: list[dict[str, str]] = []
    for index, target in enumerate(targets, start=1):
        if args.progress_every > 0 and index % args.progress_every == 0:
            print(f"Checked comment-record metadata for {index} public-law/docket rows", file=sys.stderr)
        rows.append(build_row(target, args, key, key_mode))
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)
    if args.merge_existing:
        rows = merge_existing_rows(rows, args.output)
    write_csv(rows, args.output)
    write_metadata(args, rows, key_mode)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
