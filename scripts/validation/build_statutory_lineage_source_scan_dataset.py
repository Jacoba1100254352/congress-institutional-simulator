#!/usr/bin/env python3
"""Build an official GovInfo public-law text scan for lineage candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


QUEUE = Path("reports/statutory-lineage-review-queue.csv")
NO_TARGET_REVIEW = Path("data/validation/raw/statutory_lineage_no_target_review.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_source_scan.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_source_scan.metadata.md")
USER_AGENT = "congress-institutional-simulator-validation/0.7"
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_FIELD_VALUES = 50
MAX_SNIPPETS = 40
MAX_SNIPPET_CHARS = 420

USC_REFERENCE_RE = re.compile(
    r"\b\d+\s+U\.?\s*S\.?\s*C\.?\s*(?:§\s*)?[A-Za-z0-9().\-–]+(?:\s+note)?",
    re.IGNORECASE,
)
TITLE_CODE_RE = re.compile(r"\btitle\s+\d+\s*,?\s+United States Code\b", re.IGNORECASE)
AMENDMENT_RE = re.compile(
    r"\b(?:is|are|be|was|were)\s+amended\b|\bamended\s+by\b|\bis\s+amended--\b|\bare\s+amended--\b",
    re.IGNORECASE,
)
REPEAL_RE = re.compile(
    r"\b(?:is|are|be|was|were)\s+repealed\b|\brepeal(?:ed|ing)?\b",
    re.IGNORECASE,
)
REDESIGNATION_RE = re.compile(r"\bredesignat(?:e|ed|ing|ion)\b", re.IGNORECASE)
SECTION_CANDIDATE_RE = re.compile(
    r"(U\.?\s*S\.?\s*C\.?|United States Code|is amended|are amended|amended by|"
    r"is repealed|are repealed|redesignat|by striking|by inserting|added at the end)",
    re.IGNORECASE,
)
OPEN_USC_REFERENCE_RE = re.compile(
    r"\b\d+\s+U\.?\s*S\.?\s*C\.?\.?\s*(?:§+\s*)?$",
    re.IGNORECASE,
)
HYPHENATED_USC_FRAGMENT_RE = re.compile(
    r"\b\d+\s+U\.?\s*S\.?\s*C\.?\.?\s*(?:§+\s*)?[A-Za-z0-9][A-Za-z0-9.\-–]*[-–]$",
    re.IGNORECASE,
)
PAGE_MARKER_RE = re.compile(r"^\[\[Page\b.*\]\]$", re.IGNORECASE)
USC_CONTINUATION_START_RE = re.compile(
    r"^(?:[A-Za-z0-9][A-Za-z0-9.\-–]*(?:\([A-Za-z0-9]+\))*\)?|"
    r"prec\.?\s+\d+[A-Za-z0-9.\-–]*)(?=[\s,.;:)>]|$)",
    re.IGNORECASE,
)

CLAIM_BOUNDARY = (
    "Official public-law text scan only; this row records candidate statutory "
    "references and amendment language from GovInfo public-law text. It does "
    "not establish codified U.S.C. lineage, target-section diffs, observed "
    "expiration outcomes, implementation outcomes, direct court review, "
    "causal effects, welfare, or model validation."
)

FIELDNAMES = [
    "scan_rank",
    "lineage_review_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "govinfo_package_id",
    "govinfo_text_url",
    "govinfo_details_url",
    "source_review_status",
    "official_text_sha256",
    "official_text_bytes",
    "bill_title",
    "revision_flags",
    "usc_reference_count",
    "unique_usc_references",
    "title_code_reference_count",
    "amendment_phrase_count",
    "repeal_phrase_count",
    "redesignation_phrase_count",
    "target_section_candidate_count",
    "target_section_candidates",
    "codification_source_status",
    "lineage_evidence_status",
    "evidence_layers",
    "missing_links",
    "source_review_notes",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def public_law_package(public_law_number: str) -> str:
    congress, law_number = public_law_number.strip().split("-", maxsplit=1)
    return f"PLAW-{congress}publ{int(law_number)}"


def html_to_text(source: str) -> str:
    source = re.sub(r"(?is)<script.*?</script>", " ", source)
    source = re.sub(r"(?is)<style.*?</style>", " ", source)
    source = re.sub(r"(?i)<br\s*/?>", "\n", source)
    source = re.sub(r"(?i)</(?:p|div|tr|h[1-6]|li|pre)>", "\n", source)
    source = re.sub(r"<[^>]+>", " ", source)
    return html.unescape(source).replace("\r\n", "\n").replace("\r", "\n")


def clean_space(value: str) -> str:
    return " ".join(value.split())


def ordered_unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = clean_space(value)
        if not clean:
            continue
        key = clean.casefold()
        if key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def fetch_text(url: str, timeout: float, retries: int) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = response.read()
                encoding = response.headers.get_content_charset() or "utf-8"
                return payload, payload.decode(encoding, errors="replace")
        except (HTTPError, TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def source_inputs(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = list(queue_rows)
    existing_bills = {
        row.get("bill_id", "").strip()
        for row in rows
        if row.get("bill_id", "").strip()
    }
    for review_row in read_csv(NO_TARGET_REVIEW) if NO_TARGET_REVIEW.exists() else []:
        bill_id = review_row.get("bill_id", "").strip()
        if not bill_id or bill_id in existing_bills:
            continue
        rows.append({
            "lineage_review_rank": review_row.get("lineage_review_rank", ""),
            "action_rank": review_row.get("action_rank", ""),
            "bill_id": bill_id,
            "public_law_number": review_row.get("public_law_number", ""),
            "bill_title": review_row.get("designation_subject", ""),
            "revision_flags": "reviewed_no_structured_usc_target",
            "evidence_layers": review_row.get("evidence_layers", ""),
            "missing_links": review_row.get("missing_links", ""),
        })
        existing_bills.add(bill_id)
    return rows


def is_usc_reference_continuation(context: str, next_line: str) -> bool:
    if not USC_CONTINUATION_START_RE.search(next_line):
        return False
    return bool(
        OPEN_USC_REFERENCE_RE.search(context)
        or HYPHENATED_USC_FRAGMENT_RE.search(context)
    )


def needs_source_continuation(context: str, next_line: str, continuation_count: int) -> bool:
    if continuation_count == 0 and (AMENDMENT_RE.search(context) or context.endswith("--")):
        return True
    return is_usc_reference_continuation(context, next_line)


def join_source_continuation(context: str, next_line: str) -> str:
    if HYPHENATED_USC_FRAGMENT_RE.search(context):
        return f"{context}{next_line}"
    return f"{context} {next_line}"


def scan_text(text: str) -> dict[str, str]:
    lines = [clean_space(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    usc_references = ordered_unique(USC_REFERENCE_RE.findall(text))
    title_code_references = ordered_unique(TITLE_CODE_RE.findall(text))
    amendment_count = len(AMENDMENT_RE.findall(text))
    repeal_count = len(REPEAL_RE.findall(text))
    redesignation_count = len(REDESIGNATION_RE.findall(text))
    snippets: list[str] = []
    candidate_count = 0
    consumed_continuation_indexes: set[int] = set()
    for index, line in enumerate(lines):
        if index in consumed_continuation_indexes:
            continue
        if not SECTION_CANDIDATE_RE.search(line):
            continue
        candidate_count += 1
        context = line
        continuation_count = 0
        next_index = index + 1
        while next_index < len(lines) and len(context) < MAX_SNIPPET_CHARS:
            next_line = lines[next_index]
            if (
                PAGE_MARKER_RE.match(next_line)
                and (
                    OPEN_USC_REFERENCE_RE.search(context)
                    or HYPHENATED_USC_FRAGMENT_RE.search(context)
                )
            ):
                consumed_continuation_indexes.add(next_index)
                next_index += 1
                continue
            if not needs_source_continuation(context, next_line, continuation_count):
                break
            if is_usc_reference_continuation(context, next_line):
                consumed_continuation_indexes.add(next_index)
            context = join_source_continuation(context, next_line)
            continuation_count += 1
            next_index += 1
        if len(context) > MAX_SNIPPET_CHARS:
            context = context[: MAX_SNIPPET_CHARS - 3].rstrip() + "..."
        snippets.append(context)
    snippets = ordered_unique(snippets)
    return {
        "usc_reference_count": str(len(usc_references)),
        "unique_usc_references": "; ".join(usc_references[:MAX_FIELD_VALUES]),
        "title_code_reference_count": str(len(title_code_references)),
        "amendment_phrase_count": str(amendment_count),
        "repeal_phrase_count": str(repeal_count),
        "redesignation_phrase_count": str(redesignation_count),
        "target_section_candidate_count": str(candidate_count),
        "target_section_candidates": "; ".join(snippets[:MAX_SNIPPETS]),
    }


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    queue_rows = source_inputs(read_csv(args.input))
    if args.limit:
        queue_rows = queue_rows[: args.limit]
    rows: list[dict[str, str]] = []
    for index, queue_row in enumerate(queue_rows, start=1):
        public_law = queue_row["public_law_number"]
        package_id = public_law_package(public_law)
        text_url = f"https://www.govinfo.gov/content/pkg/{package_id}/html/{package_id}.htm"
        details_url = f"https://www.govinfo.gov/app/details/{package_id}"
        payload, source_html = fetch_text(text_url, args.timeout, args.retries)
        text = html_to_text(source_html)
        scan = scan_text(text)
        missing_links = ordered_unique(
            [
                "olrc_us_code_classification",
                "codified_usc_lineage",
                "target_section_diff",
                "law_revision_effective_text",
                "model_validation",
            ]
            + [
                value.strip()
                for value in queue_row.get("missing_links", "").split(";")
                if value.strip()
            ]
        )
        evidence_layers = ordered_unique(
            [
                "govinfo_public_law_text_scan",
                "statutory_lineage_review_queue",
            ]
            + [
                value.strip()
                for value in queue_row.get("evidence_layers", "").split(";")
                if value.strip()
            ]
        )
        rows.append({
            "scan_rank": str(index),
            "lineage_review_rank": queue_row.get("lineage_review_rank", ""),
            "action_rank": queue_row.get("action_rank", ""),
            "bill_id": queue_row.get("bill_id", ""),
            "public_law_number": public_law,
            "govinfo_package_id": package_id,
            "govinfo_text_url": text_url,
            "govinfo_details_url": details_url,
            "source_review_status": "official_govinfo_public_law_text_scanned",
            "official_text_sha256": hashlib.sha256(payload).hexdigest(),
            "official_text_bytes": str(len(payload)),
            "bill_title": queue_row.get("bill_title", ""),
            "revision_flags": queue_row.get("revision_flags", ""),
            "usc_reference_count": scan["usc_reference_count"],
            "unique_usc_references": scan["unique_usc_references"],
            "title_code_reference_count": scan["title_code_reference_count"],
            "amendment_phrase_count": scan["amendment_phrase_count"],
            "repeal_phrase_count": scan["repeal_phrase_count"],
            "redesignation_phrase_count": scan["redesignation_phrase_count"],
            "target_section_candidate_count": scan["target_section_candidate_count"],
            "target_section_candidates": scan["target_section_candidates"],
            "codification_source_status": "govinfo_public_law_text_only_needs_olrc_or_us_code_notes",
            "lineage_evidence_status": "source_text_scan_not_codified_lineage_evidence",
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "source_review_notes": (
                "Scanned official GovInfo public-law text for U.S.C. references "
                "and amendment/repeal/redesignation language; use OLRC or "
                "govinfo USLM/U.S. Code notes before coding target-section lineage."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        })
        if args.sleep_seconds and index < len(queue_rows):
            time.sleep(args.sleep_seconds)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]], path: Path) -> None:
    scanned = sum(1 for row in rows if row["source_review_status"] == "official_govinfo_public_law_text_scanned")
    lines = [
        "# Statutory Lineage Source Scan Metadata",
        "",
        "Official GovInfo public-law text scan for the statutory-lineage review queue.",
        "",
        f"- Input queue: `{QUEUE}`",
        f"- Output rows: {len(rows)}",
        f"- Official GovInfo text rows scanned: {scanned}",
        "- Access method: GovInfo public-law HTML text pages.",
        "- Network required to refresh: yes.",
        "- API key required: no.",
        "",
        "Claim boundary: official public-law text scan only. The file records candidate U.S.C. references and amendment, repeal, or redesignation language in public-law text, but it does not establish codified U.S.C. lineage, target-section text diffs, implementation outcomes, direct court review, welfare, causal effects, or model validation.",
    ]
    path.write_text("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=QUEUE)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep-seconds", type=float, default=0.1)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = build_rows(args)
    if not rows:
        raise SystemExit(f"{args.input} is empty.")
    write_csv(rows, args.output)
    write_metadata(rows, args.metadata)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
