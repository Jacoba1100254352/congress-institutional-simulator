#!/usr/bin/env python3
"""Fetch OLRC annual pages and write bounded text-diff cues for lineage review."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


INPUT = Path("reports/statutory-lineage-olrc-historical-scan.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_olrc_annual_text_diff.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_olrc_annual_text_diff.metadata.md")

CLAIM_BOUNDARY = (
    "Official OLRC annual-page text-diff cue scan only. Rows preserve bounded "
    "post-edition public-law context snippets, raw-hash comparisons, normalized "
    "section-text signatures, and bounded first-change windows for annual U.S. "
    "Code pages, but they do not establish source-reviewed codified U.S.C. "
    "lineage, public-law causation, adjudicated target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)
MISSING_LINKS = (
    "manual_olrc_classification_review",
    "codified_usc_lineage_adjudication",
    "source_reviewed_target_section_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "model_validation",
)
EVIDENCE_LAYERS = (
    "statutory_lineage_olrc_historical_scan",
    "official_olrc_annual_us_code_page",
    "bounded_annual_text_diff_cue_scan",
)
USER_AGENT = "CongressInstitutionalSimulatorValidation/0.1 (publication-readiness source scan)"

TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
OLRC_EFFECTIVE_DATE_RE = re.compile(
    r"Text contains those laws in effect on [A-Za-z]+\s+\d{1,2},\s+\d{4}",
    re.IGNORECASE,
)

FIELDNAMES = [
    "text_diff_rank",
    "historical_scan_rank",
    "current_olrc_scan_rank",
    "triage_rank",
    "source_scan_rank",
    "lineage_review_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "normalized_title",
    "normalized_section",
    "pre_edition",
    "post_edition",
    "pre_olrc_url",
    "post_olrc_url",
    "pre_fetch_status",
    "pre_http_status",
    "pre_text_sha256",
    "pre_text_bytes",
    "pre_hash_matches_historical_scan",
    "pre_section_anchor_status",
    "pre_normalized_text_chars",
    "pre_normalized_text_sha256",
    "pre_public_law_reference_hits",
    "post_fetch_status",
    "post_http_status",
    "post_text_sha256",
    "post_text_bytes",
    "post_hash_matches_historical_scan",
    "post_section_anchor_status",
    "post_normalized_text_chars",
    "post_normalized_text_sha256",
    "post_public_law_reference_hits",
    "normalized_text_hash_status",
    "normalized_text_char_delta",
    "first_changed_text_pre_window",
    "first_changed_text_post_window",
    "public_law_reference_hit_delta",
    "post_public_law_context_count",
    "post_public_law_context_snippets",
    "automated_diff_cue_status",
    "section_change_cue_status",
    "manual_review_priority",
    "lineage_evidence_status",
    "evidence_layers",
    "missing_links",
    "source_review_notes",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_text(raw_html: bytes) -> str:
    text = raw_html.decode("utf-8", errors="replace")
    text = html.unescape(TAG_RE.sub(" ", text))
    text = text.replace("\u2010", "-").replace("\u2011", "-")
    text = text.replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")
    return WHITESPACE_RE.sub(" ", text).strip()


def fetch_url(
    url: str,
    timeout: float,
    retries: int,
    sleep_seconds: float,
    cache: dict[str, tuple[int, bytes, str]],
) -> tuple[int, bytes, str]:
    if url in cache:
        return cache[url]
    last_error = ""
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                result = (int(response.status), response.read(), "")
                cache[url] = result
                return result
        except urllib.error.HTTPError as exception:
            result = (int(exception.code), exception.read(), "")
            cache[url] = result
            return result
        except (urllib.error.URLError, TimeoutError) as exception:
            last_error = str(exception)
            if attempt < retries:
                time.sleep(sleep_seconds)
    result = (0, b"", last_error)
    cache[url] = result
    return result


def public_law_patterns(public_law_number: str) -> list[re.Pattern[str]]:
    escaped = re.escape(public_law_number)
    return [
        re.compile(rf"\bPub\.\s*L\.\s*{escaped}\b", flags=re.IGNORECASE),
        re.compile(rf"\bPublic\s+Law\s+{escaped}\b", flags=re.IGNORECASE),
    ]


def public_law_hits(text: str, public_law_number: str) -> int:
    if not text or not public_law_number:
        return 0
    return sum(len(pattern.findall(text)) for pattern in public_law_patterns(public_law_number))


def context_snippets(text: str, public_law_number: str, max_snippets: int, radius: int) -> list[str]:
    if not text or not public_law_number:
        return []
    snippets: list[str] = []
    seen: set[str] = set()
    for pattern in public_law_patterns(public_law_number):
        for match in pattern.finditer(text):
            start = max(0, match.start() - radius)
            end = min(len(text), match.end() + radius)
            snippet = text[start:end].strip()
            snippet = WHITESPACE_RE.sub(" ", snippet)
            if start > 0:
                snippet = f"... {snippet}"
            if end < len(text):
                snippet = f"{snippet} ..."
            if snippet not in seen:
                snippets.append(snippet)
                seen.add(snippet)
            if len(snippets) >= max_snippets:
                return snippets
    return snippets


def normalized_text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else ""


def bounded_window(text: str, center: int, radius: int) -> str:
    if not text:
        return ""
    start = max(0, center - radius)
    end = min(len(text), center + radius)
    snippet = text[start:end].strip()
    snippet = WHITESPACE_RE.sub(" ", snippet)
    if start > 0:
        snippet = f"... {snippet}"
    if end < len(text):
        snippet = f"{snippet} ..."
    return snippet


def section_content_text(text: str, title: str, section: str) -> tuple[str, str]:
    if not text or not title or not section:
        return text, "section_anchor_unavailable"
    section_pattern = re.escape(section)
    patterns = (
        re.compile(rf"\b{re.escape(title)}\s+USC\s+{section_pattern}\s*:", re.IGNORECASE),
        re.compile(rf"\b{re.escape(title)}\s+U\.S\.C\.\s+{section_pattern}\s*:", re.IGNORECASE),
    )
    for pattern in patterns:
        matches = list(pattern.finditer(text))
        if matches:
            match = matches[-1]
            return text[match.start() :].strip(), "section_anchor_found"
    return text, "section_anchor_not_found"


def normalize_section_comparison_text(text: str) -> str:
    text = OLRC_EFFECTIVE_DATE_RE.sub("Text contains those laws in effect on DATE", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def first_changed_windows(pre_text: str, post_text: str, radius: int) -> tuple[str, str]:
    if not pre_text or not post_text or pre_text == post_text:
        return "", ""
    shared_prefix = 0
    max_prefix = min(len(pre_text), len(post_text))
    while shared_prefix < max_prefix and pre_text[shared_prefix] == post_text[shared_prefix]:
        shared_prefix += 1
    return (
        bounded_window(pre_text, shared_prefix, radius),
        bounded_window(post_text, shared_prefix, radius),
    )


def fetch_payload(
    *,
    prefix: str,
    source_row: dict[str, str],
    timeout: float,
    retries: int,
    sleep_seconds: float,
    cache: dict[str, tuple[int, bytes, str]],
    dry_run: bool,
) -> dict[str, str]:
    url = source_row[f"{prefix}_olrc_url"]
    if dry_run:
        status_code, body, error = 0, b"", ""
    else:
        status_code, body, error = fetch_url(url, timeout, retries, sleep_seconds, cache)
    normalized = normalize_text(body) if body else ""
    section_text, section_anchor_status = section_content_text(
        normalized,
        source_row.get("normalized_title", ""),
        source_row.get("normalized_section", ""),
    )
    section_text = normalize_section_comparison_text(section_text)
    if status_code == 200 and body:
        fetch_status = "official_olrc_annual_section_page_fetched"
    elif dry_run:
        fetch_status = "dry_run_not_fetched"
    elif status_code:
        fetch_status = "official_olrc_annual_section_page_http_error"
    else:
        fetch_status = "official_olrc_annual_section_page_fetch_error"
    source_hash = hashlib.sha256(body).hexdigest() if body else ""
    expected_hash = source_row.get(f"{prefix}_text_sha256", "")
    return {
        f"{prefix}_fetch_status": fetch_status,
        f"{prefix}_http_status": str(status_code) if status_code else "",
        f"{prefix}_text_sha256": source_hash,
        f"{prefix}_text_bytes": str(len(body)) if body else "0",
        f"{prefix}_hash_matches_historical_scan": (
            "yes" if source_hash and source_hash == expected_hash else "no"
        ),
        f"{prefix}_section_anchor_status": section_anchor_status,
        f"{prefix}_normalized_text_chars": str(len(section_text)),
        f"{prefix}_normalized_text_sha256": normalized_text_sha256(section_text),
        f"{prefix}_public_law_reference_hits": str(
            public_law_hits(section_text, source_row["public_law_number"])
        ),
        f"{prefix}_normalized_text": section_text,
        f"{prefix}_fetch_error": error,
    }


def diff_cue_status(row: dict[str, str]) -> str:
    pre_hits = int(row["pre_public_law_reference_hits"] or "0")
    post_hits = int(row["post_public_law_reference_hits"] or "0")
    pre_fetched = row["pre_fetch_status"] == "official_olrc_annual_section_page_fetched"
    post_fetched = row["post_fetch_status"] == "official_olrc_annual_section_page_fetched"
    if pre_fetched and post_fetched and pre_hits == 0 and post_hits > 0:
        return "post_only_public_law_marker_on_changed_annual_page"
    if pre_fetched and post_fetched and pre_hits > 0 and post_hits > 0:
        return "public_law_marker_present_in_pre_and_post_annual_pages"
    if pre_fetched and post_fetched:
        return "annual_pages_fetched_without_post_only_public_law_marker"
    if pre_fetched or post_fetched:
        return "partial_annual_text_available_needs_manual_followup"
    return "annual_text_not_available_needs_manual_followup"


def normalized_hash_status(row: dict[str, str]) -> str:
    pre_fetched = row["pre_fetch_status"] == "official_olrc_annual_section_page_fetched"
    post_fetched = row["post_fetch_status"] == "official_olrc_annual_section_page_fetched"
    if not pre_fetched and not post_fetched:
        return "pre_post_normalized_text_unavailable"
    if not pre_fetched or not post_fetched:
        return "partial_normalized_text_available"
    if row["pre_normalized_text_sha256"] == row["post_normalized_text_sha256"]:
        return "pre_post_normalized_text_same"
    return "pre_post_normalized_text_changed"


def section_change_cue_status(row: dict[str, str]) -> str:
    pre_fetched = row["pre_fetch_status"] == "official_olrc_annual_section_page_fetched"
    post_fetched = row["post_fetch_status"] == "official_olrc_annual_section_page_fetched"
    if not pre_fetched and not post_fetched:
        return "annual_text_not_available_needs_manual_followup"
    if not pre_fetched or not post_fetched:
        return "partial_annual_text_available_needs_manual_followup"
    normalized_changed = row["normalized_text_hash_status"] == "pre_post_normalized_text_changed"
    pre_hits = int(row["pre_public_law_reference_hits"] or "0")
    post_hits = int(row["post_public_law_reference_hits"] or "0")
    post_only_marker = pre_hits == 0 and post_hits > 0
    if normalized_changed and post_only_marker:
        return "normalized_section_changed_with_post_only_public_law_marker"
    if normalized_changed:
        return "normalized_section_changed_without_post_only_public_law_marker"
    if post_only_marker:
        return "normalized_section_unchanged_with_post_only_public_law_marker"
    return "normalized_section_unchanged_without_post_only_public_law_marker"


def manual_review_priority(row: dict[str, str]) -> str:
    if row["section_change_cue_status"] == "normalized_section_changed_with_post_only_public_law_marker":
        return "priority_1_review_post_public_law_context_and_target_section"
    if row["section_change_cue_status"] == "normalized_section_changed_without_post_only_public_law_marker":
        return "priority_1_review_section_text_change_without_public_law_marker"
    if row["post_fetch_status"] == "official_olrc_annual_section_page_fetched":
        return "priority_2_review_post_annual_text"
    return "priority_3_refetch_or_manual_olrc_lookup"


def build_rows(source_rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    selected_rows = source_rows[: args.limit] if args.limit is not None else source_rows
    cache: dict[str, tuple[int, bytes, str]] = {}
    rows: list[dict[str, str]] = []
    for index, source_row in enumerate(selected_rows, start=1):
        pre = fetch_payload(
            prefix="pre",
            source_row=source_row,
            timeout=args.timeout,
            retries=args.retries,
            sleep_seconds=args.sleep_seconds,
            cache=cache,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            time.sleep(args.sleep_seconds)
        post = fetch_payload(
            prefix="post",
            source_row=source_row,
            timeout=args.timeout,
            retries=args.retries,
            sleep_seconds=args.sleep_seconds,
            cache=cache,
            dry_run=args.dry_run,
        )
        pre_text = pre.pop("pre_normalized_text")
        post_text = post.pop("post_normalized_text")
        snippets = context_snippets(
            post_text,
            source_row["public_law_number"],
            args.max_snippets,
            args.snippet_radius,
        )
        pre_change_window, post_change_window = first_changed_windows(
            pre_text,
            post_text,
            args.change_window_radius,
        )
        pre.pop("pre_fetch_error")
        post.pop("post_fetch_error")
        row = {
            "text_diff_rank": str(index),
            "historical_scan_rank": source_row["historical_scan_rank"],
            "current_olrc_scan_rank": source_row["current_olrc_scan_rank"],
            "triage_rank": source_row["triage_rank"],
            "source_scan_rank": source_row["source_scan_rank"],
            "lineage_review_rank": source_row["lineage_review_rank"],
            "bill_id": source_row["bill_id"],
            "public_law_number": source_row["public_law_number"],
            "enacted_date": source_row["enacted_date"],
            "target_reference": source_row["target_reference"],
            "target_reference_type": source_row["target_reference_type"],
            "normalized_title": source_row["normalized_title"],
            "normalized_section": source_row["normalized_section"],
            "pre_edition": source_row["pre_edition"],
            "post_edition": source_row["post_edition"],
            "pre_olrc_url": source_row["pre_olrc_url"],
            "post_olrc_url": source_row["post_olrc_url"],
            **pre,
            **post,
            "normalized_text_hash_status": "",
            "normalized_text_char_delta": str(
                int(post["post_normalized_text_chars"] or "0")
                - int(pre["pre_normalized_text_chars"] or "0")
            ),
            "first_changed_text_pre_window": pre_change_window,
            "first_changed_text_post_window": post_change_window,
            "public_law_reference_hit_delta": str(
                int(post["post_public_law_reference_hits"] or "0")
                - int(pre["pre_public_law_reference_hits"] or "0")
            ),
            "post_public_law_context_count": str(len(snippets)),
            "post_public_law_context_snippets": " || ".join(snippets),
            "automated_diff_cue_status": "",
            "section_change_cue_status": "",
            "manual_review_priority": "",
            "lineage_evidence_status": "annual_text_diff_cue_scan_not_codified_lineage_evidence",
            "evidence_layers": "; ".join(EVIDENCE_LAYERS),
            "missing_links": "; ".join(MISSING_LINKS),
            "source_review_notes": (
                "Automated annual text cue only; normalized text signatures and "
                "first-change windows are review aids, and a reviewer still must "
                "adjudicate OLRC classification, causation, and target-section text changes."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["normalized_text_hash_status"] = normalized_hash_status(row)
        row["automated_diff_cue_status"] = diff_cue_status(row)
        row["section_change_cue_status"] = section_change_cue_status(row)
        row["manual_review_priority"] = manual_review_priority(row)
        rows.append(row)
        if not args.dry_run and index < len(selected_rows):
            time.sleep(args.sleep_seconds)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    post_only = sum(
        row["automated_diff_cue_status"] == "post_only_public_law_marker_on_changed_annual_page"
        for row in rows
    )
    hash_matches = sum(
        row["pre_hash_matches_historical_scan"] == "yes"
        and row["post_hash_matches_historical_scan"] == "yes"
        for row in rows
    )
    normalized_changes = sum(
        row["normalized_text_hash_status"] == "pre_post_normalized_text_changed"
        for row in rows
    )
    changed_windows = sum(
        bool(row["first_changed_text_pre_window"] and row["first_changed_text_post_window"])
        for row in rows
    )
    pre_anchor_found = sum(row["pre_section_anchor_status"] == "section_anchor_found" for row in rows)
    post_anchor_found = sum(row["post_section_anchor_status"] == "section_anchor_found" for row in rows)
    path.write_text(
        "\n".join(
            [
                "# Statutory Lineage OLRC Annual Text-Diff Cue Metadata",
                "",
                f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
                f"- source_input: `{args.input}`",
                f"- output_rows: {len(rows)}",
                f"- hash_verified_pre_post_rows: {hash_matches}",
                f"- normalized_section_text_changed_rows: {normalized_changes}",
                f"- first_changed_text_window_rows: {changed_windows}",
                f"- pre_section_anchor_found_rows: {pre_anchor_found}",
                f"- post_section_anchor_found_rows: {post_anchor_found}",
                f"- post_only_public_law_marker_rows: {post_only}",
                f"- max_snippets_per_row: {args.max_snippets}",
                f"- snippet_radius: {args.snippet_radius}",
                f"- change_window_radius: {args.change_window_radius}",
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
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    parser.add_argument("--max-snippets", type=int, default=3)
    parser.add_argument("--snippet-radius", type=int, default=220)
    parser.add_argument("--change-window-radius", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_rows = read_csv(args.input)
    if not source_rows:
        raise SystemExit(f"{args.input} has no rows.")
    rows = build_rows(source_rows, args)
    if not rows:
        raise SystemExit("No historical OLRC rows available for annual text-diff cue scan.")
    write_csv(args.output, rows)
    write_metadata(args.metadata, rows, args)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
