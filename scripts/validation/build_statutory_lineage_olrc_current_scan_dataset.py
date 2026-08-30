#!/usr/bin/env python3
"""Fetch official OLRC current U.S. Code pages for statutory-lineage triage rows."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


INPUT = Path("reports/statutory-lineage-target-section-triage.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_olrc_current_scan.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_olrc_current_scan.metadata.md")

CLAIM_BOUNDARY = (
    "Official OLRC current-section availability scan only. Rows show whether a "
    "candidate target reference has a current U.S. Code page and whether that "
    "page text mentions the queued public law; they do not establish historical "
    "codified U.S.C. lineage, before/after target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)
MISSING_LINKS = (
    "olrc_classification_review",
    "historical_us_code_version",
    "codified_usc_lineage",
    "target_section_diff",
    "law_revision_effective_text",
    "model_validation",
)
EVIDENCE_LAYERS = (
    "statutory_lineage_target_section_triage",
    "official_olrc_current_us_code_page",
)
USER_AGENT = "CongressInstitutionalSimulatorValidation/0.1 (publication-readiness source scan)"

REFERENCE_RE = re.compile(r"^(?P<title>\d+)\s+USC\s+(?P<section>\S+)", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")

FIELDNAMES = [
    "olrc_scan_rank",
    "triage_rank",
    "source_scan_rank",
    "lineage_review_rank",
    "bill_id",
    "public_law_number",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "olrc_granule_id",
    "olrc_url",
    "olrc_scan_status",
    "http_status",
    "official_text_sha256",
    "official_text_bytes",
    "section_heading",
    "public_law_reference_hits",
    "public_law_reference_status",
    "codification_review_status",
    "lineage_evidence_status",
    "evidence_layers",
    "missing_links",
    "source_review_notes",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def target_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("target_reference", "").strip(),
        row.get("target_reference_type", "").strip(),
    )


def existing_successful_rows(path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    if not path.exists():
        return {}
    return {
        target_key(row): row
        for row in read_csv(path)
        if row.get("olrc_scan_status", "").strip() == "official_olrc_current_section_page_fetched"
        and all(target_key(row))
    }


def normalize_text(raw_html: bytes) -> str:
    text = raw_html.decode("utf-8", errors="replace")
    text = html.unescape(TAG_RE.sub(" ", text))
    text = text.replace("\u2010", "-").replace("\u2011", "-")
    text = text.replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")
    return WHITESPACE_RE.sub(" ", text).strip()


def normalize_target_reference(reference: str, reference_type: str) -> tuple[str, str, str]:
    if reference_type in {"no_structured_target", "title_code_only"}:
        return "", "", ""
    match = REFERENCE_RE.match(reference.strip())
    if not match:
        return "", "", ""
    title = match.group("title")
    section = match.group("section").strip()
    section = section.removesuffix("note").strip()
    section = section.split("(", maxsplit=1)[0].strip()
    section = section.strip(" .;,")
    if not section or section.endswith("-") or not re.match(r"^\d", section):
        return title, section, ""
    granule_id = f"USC-prelim-title{title}-section{section}"
    return title, section, granule_id


def olrc_url(granule_id: str) -> str:
    query = urllib.parse.urlencode(
        {
            "edition": "prelim",
            "num": "0",
            "req": f"granuleid:{granule_id}",
        }
    )
    return f"https://uscode.house.gov/view.xhtml?{query}"


def fetch_url(url: str, timeout: float, retries: int, sleep_seconds: float) -> tuple[int, bytes, str]:
    last_error = ""
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return int(response.status), response.read(), ""
        except urllib.error.HTTPError as exception:
            return int(exception.code), exception.read(), ""
        except (urllib.error.URLError, TimeoutError) as exception:
            last_error = str(exception)
            if attempt < retries:
                time.sleep(sleep_seconds)
    return 0, b"", last_error


def public_law_hits(text: str, public_law_number: str) -> int:
    if not text or not public_law_number:
        return 0
    escaped = re.escape(public_law_number)
    patterns = (
        rf"\bPub\.\s*L\.\s*{escaped}\b",
        rf"\bPublic\s+Law\s+{escaped}\b",
    )
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def section_heading(text: str, title: str, section: str) -> str:
    if not text or not section:
        return ""
    marker = f"§{section}."
    if marker in text:
        start = text.find(marker)
        heading = text[start : start + 180]
        return heading.split("(", maxsplit=1)[0].strip()
    marker = f"{title} USC {section}"
    if marker in text:
        start = text.find(marker)
        return text[start : start + 180].strip()
    return text[:180].strip()


def not_fetched_status(row: dict[str, str], title: str, section: str) -> str:
    reference_type = row.get("target_reference_type", "")
    if reference_type == "no_structured_target":
        return "no_structured_target_not_fetched"
    if reference_type == "title_code_only":
        return "title_only_not_fetched"
    if not title or not section:
        return "unparseable_target_not_fetched"
    return "incomplete_or_nonsection_target_not_fetched"


def build_row(
    index: int,
    source_row: dict[str, str],
    *,
    timeout: float,
    retries: int,
    sleep_seconds: float,
    dry_run: bool,
) -> dict[str, str]:
    title, section, granule_id = normalize_target_reference(
        source_row.get("target_reference", ""),
        source_row.get("target_reference_type", ""),
    )
    url = olrc_url(granule_id) if granule_id else ""
    status = ""
    http_status = ""
    body = b""
    notes = ""
    text = ""
    if not url:
        status = not_fetched_status(source_row, title, section)
        notes = "No current OLRC section page fetched because the target reference is title-only, missing, incomplete, or not a section-level U.S.C. reference."
    elif dry_run:
        status = "dry_run_not_fetched"
        notes = "Dry run; current OLRC page was not fetched."
    else:
        response_status, body, error = fetch_url(url, timeout, retries, sleep_seconds)
        http_status = str(response_status) if response_status else ""
        if response_status == 200 and body:
            status = "official_olrc_current_section_page_fetched"
            text = normalize_text(body)
            notes = "Official OLRC current U.S. Code page fetched; review remains current-text availability only until historical/codified-lineage review is complete."
        elif response_status:
            status = "official_olrc_current_section_page_http_error"
            text = normalize_text(body) if body else ""
            notes = f"Official OLRC page request returned HTTP {response_status}; manual review required before using this target."
        else:
            status = "official_olrc_current_section_page_fetch_error"
            notes = f"Official OLRC page request failed: {error}"
    public_law_count = public_law_hits(text, source_row.get("public_law_number", ""))
    if not text:
        public_law_status = "not_checked_no_current_page_text"
    elif public_law_count > 0:
        public_law_status = "current_page_mentions_public_law"
    else:
        public_law_status = "current_page_no_public_law_mention"
    return {
        "olrc_scan_rank": str(index),
        "triage_rank": source_row.get("triage_rank", ""),
        "source_scan_rank": source_row.get("source_scan_rank", ""),
        "lineage_review_rank": source_row.get("lineage_review_rank", ""),
        "bill_id": source_row.get("bill_id", ""),
        "public_law_number": source_row.get("public_law_number", ""),
        "target_reference": source_row.get("target_reference", ""),
        "target_reference_type": source_row.get("target_reference_type", ""),
        "normalized_title": title,
        "normalized_section": section,
        "olrc_granule_id": granule_id,
        "olrc_url": url,
        "olrc_scan_status": status,
        "http_status": http_status,
        "official_text_sha256": hashlib.sha256(body).hexdigest() if body else "",
        "official_text_bytes": str(len(body)) if body else "0",
        "section_heading": section_heading(text, title, section),
        "public_law_reference_hits": str(public_law_count),
        "public_law_reference_status": public_law_status,
        "codification_review_status": "current_olrc_page_availability_only",
        "lineage_evidence_status": "current_olrc_scan_not_codified_lineage_evidence",
        "evidence_layers": "; ".join(EVIDENCE_LAYERS),
        "missing_links": "; ".join(MISSING_LINKS),
        "source_review_notes": notes,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def reusable_row(index: int, source_row: dict[str, str], existing_row: dict[str, str]) -> dict[str, str]:
    title, section, granule_id = normalize_target_reference(
        source_row.get("target_reference", ""),
        source_row.get("target_reference_type", ""),
    )
    row = dict(existing_row)
    row.update({
        "olrc_scan_rank": str(index),
        "triage_rank": source_row.get("triage_rank", ""),
        "source_scan_rank": source_row.get("source_scan_rank", ""),
        "lineage_review_rank": source_row.get("lineage_review_rank", ""),
        "bill_id": source_row.get("bill_id", ""),
        "public_law_number": source_row.get("public_law_number", ""),
        "target_reference": source_row.get("target_reference", ""),
        "target_reference_type": source_row.get("target_reference_type", ""),
        "normalized_title": title,
        "normalized_section": section,
        "olrc_granule_id": granule_id,
        "olrc_url": olrc_url(granule_id) if granule_id else "",
        "codification_review_status": "current_olrc_page_availability_only",
        "lineage_evidence_status": "current_olrc_scan_not_codified_lineage_evidence",
        "evidence_layers": "; ".join(EVIDENCE_LAYERS),
        "missing_links": "; ".join(MISSING_LINKS),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    return row


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
    source_input: Path,
) -> None:
    fetched = sum(row["olrc_scan_status"] == "official_olrc_current_section_page_fetched" for row in rows)
    mentions = sum(row["public_law_reference_status"] == "current_page_mentions_public_law" for row in rows)
    path.write_text(
        "\n".join(
            [
                "# Statutory Lineage OLRC Current Scan Metadata",
                "",
                f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
                f"- source_input: `{source_input}`",
                f"- output_rows: {len(rows)}",
                f"- current_olrc_pages_fetched: {fetched}",
                f"- current_pages_with_public_law_mentions: {mentions}",
                f"- limit: {args.limit if args.limit is not None else 'all'}",
                f"- dry_run: {args.dry_run}",
                "- network_required: yes unless `--dry-run` is used",
                "- api_key_required: no",
                "",
                f"Claim boundary: {CLAIM_BOUNDARY}",
            ]
        )
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--refetch-successful", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_rows = read_csv(args.input)
    if args.limit is not None:
        source_rows = source_rows[: args.limit]
    if not source_rows:
        raise SystemExit(f"{args.input} has no rows.")
    reusable_rows = (
        {}
        if args.dry_run or args.refetch_successful
        else existing_successful_rows(args.output)
    )
    rows: list[dict[str, str]] = []
    for index, source_row in enumerate(source_rows, start=1):
        reused = reusable_rows.get(target_key(source_row))
        if reused:
            rows.append(reusable_row(index, source_row, reused))
        else:
            rows.append(
                build_row(
                    index,
                    source_row,
                    timeout=args.timeout,
                    retries=args.retries,
                    sleep_seconds=args.sleep_seconds,
                    dry_run=args.dry_run,
                )
            )
        if not args.dry_run and index < len(source_rows):
            time.sleep(args.sleep_seconds)
    write_csv(args.output, rows)
    write_metadata(args.metadata, rows, args, args.input)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
