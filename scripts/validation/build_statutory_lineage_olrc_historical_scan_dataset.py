#!/usr/bin/env python3
"""Fetch annual OLRC U.S. Code pages for current-page statutory-lineage candidates."""

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
from datetime import date, datetime, timezone
from pathlib import Path


CURRENT_SCAN = Path("reports/statutory-lineage-olrc-current-scan.csv")
QUEUE = Path("reports/statutory-lineage-review-queue.csv")
OUT_CSV = Path("data/validation/raw/statutory_lineage_olrc_historical_scan.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_olrc_historical_scan.metadata.md")

CLAIM_BOUNDARY = (
    "Official OLRC annual-edition availability scan only. Rows compare hashes "
    "and public-law mentions for year-before-enactment and enactment-year "
    "U.S. Code pages, but they do not establish historical codified U.S.C. "
    "lineage, public-law causation, before/after target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)
MISSING_LINKS = (
    "manual_olrc_classification_review",
    "codified_usc_lineage_adjudication",
    "source_reviewed_text_diff",
    "public_law_causal_attribution",
    "law_revision_effective_text",
    "model_validation",
)
EVIDENCE_LAYERS = (
    "statutory_lineage_olrc_current_scan",
    "official_olrc_annual_us_code_page",
    "historical_edition_availability_scan",
)
USER_AGENT = "CongressInstitutionalSimulatorValidation/0.1 (publication-readiness source scan)"

TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")

FIELDNAMES = [
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
    "pre_olrc_granule_id",
    "pre_olrc_url",
    "pre_fetch_status",
    "pre_http_status",
    "pre_text_sha256",
    "pre_text_bytes",
    "pre_public_law_reference_hits",
    "post_olrc_granule_id",
    "post_olrc_url",
    "post_fetch_status",
    "post_http_status",
    "post_text_sha256",
    "post_text_bytes",
    "post_public_law_reference_hits",
    "annual_text_hash_status",
    "annual_public_law_window_status",
    "historical_review_status",
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


def olrc_granule_id(edition: int, title: str, section: str) -> str:
    return f"USC-{edition}-title{title}-section{section}"


def olrc_url(edition: int, granule_id: str) -> str:
    query = urllib.parse.urlencode(
        {
            "edition": str(edition),
            "num": "0",
            "req": f"granuleid:{granule_id}",
        }
    )
    return f"https://uscode.house.gov/view.xhtml?{query}"


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


def public_law_hits(text: str, public_law_number: str) -> int:
    if not text or not public_law_number:
        return 0
    escaped = re.escape(public_law_number)
    patterns = (
        rf"\bPub\.\s*L\.\s*{escaped}\b",
        rf"\bPublic\s+Law\s+{escaped}\b",
    )
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def parse_enacted_year(value: str) -> int:
    return date.fromisoformat(value).year


def edition_payload(
    *,
    edition_label: str,
    edition: int,
    title: str,
    section: str,
    public_law_number: str,
    timeout: float,
    retries: int,
    sleep_seconds: float,
    cache: dict[str, tuple[int, bytes, str]],
    dry_run: bool,
) -> dict[str, str]:
    granule_id = olrc_granule_id(edition, title, section)
    url = olrc_url(edition, granule_id)
    if dry_run:
        status_code, body, error = 0, b"", ""
    else:
        status_code, body, error = fetch_url(url, timeout, retries, sleep_seconds, cache)
    text = normalize_text(body) if body else ""
    if status_code == 200 and body:
        fetch_status = "official_olrc_annual_section_page_fetched"
    elif dry_run:
        fetch_status = "dry_run_not_fetched"
    elif status_code:
        fetch_status = "official_olrc_annual_section_page_http_error"
    else:
        fetch_status = "official_olrc_annual_section_page_fetch_error"
    return {
        f"{edition_label}_olrc_granule_id": granule_id,
        f"{edition_label}_olrc_url": url,
        f"{edition_label}_fetch_status": fetch_status,
        f"{edition_label}_http_status": str(status_code) if status_code else "",
        f"{edition_label}_text_sha256": hashlib.sha256(body).hexdigest() if body else "",
        f"{edition_label}_text_bytes": str(len(body)) if body else "0",
        f"{edition_label}_public_law_reference_hits": str(public_law_hits(text, public_law_number)),
        f"{edition_label}_fetch_error": error,
    }


def annual_hash_status(row: dict[str, str]) -> str:
    if (
        row["pre_fetch_status"] != "official_olrc_annual_section_page_fetched"
        or row["post_fetch_status"] != "official_olrc_annual_section_page_fetched"
    ):
        return "pre_post_hash_unavailable"
    if row["pre_text_sha256"] == row["post_text_sha256"]:
        return "pre_post_hash_same"
    return "pre_post_hash_changed"


def annual_public_law_status(row: dict[str, str]) -> str:
    pre_hits = int(row["pre_public_law_reference_hits"] or "0")
    post_hits = int(row["post_public_law_reference_hits"] or "0")
    if pre_hits == 0 and post_hits > 0:
        return "public_law_appears_in_post_edition_only"
    if pre_hits > 0 and post_hits > 0:
        return "public_law_mentions_in_pre_and_post_editions"
    if pre_hits > 0 and post_hits == 0:
        return "public_law_mentions_in_pre_edition_only"
    return "public_law_mentions_absent_from_pre_and_post_editions"


def historical_review_status(row: dict[str, str]) -> str:
    if (
        row["pre_fetch_status"] == "official_olrc_annual_section_page_fetched"
        and row["post_fetch_status"] == "official_olrc_annual_section_page_fetched"
    ):
        return "annual_pre_post_pages_fetched_needs_manual_diff_review"
    if row["pre_fetch_status"] == "official_olrc_annual_section_page_fetched":
        return "pre_annual_page_only_needs_manual_followup"
    if row["post_fetch_status"] == "official_olrc_annual_section_page_fetched":
        return "post_annual_page_only_needs_manual_followup"
    return "annual_pages_not_fetched_needs_manual_followup"


def build_rows(
    current_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    enacted_by_bill = {
        (row["bill_id"], row["public_law_number"]): row["enacted_date"]
        for row in queue_rows
    }
    eligible_rows = [
        row
        for row in current_rows
        if row.get("public_law_reference_status") == "current_page_mentions_public_law"
        and row.get("olrc_scan_status") == "official_olrc_current_section_page_fetched"
        and row.get("normalized_title")
        and row.get("normalized_section")
    ]
    if args.limit is not None:
        eligible_rows = eligible_rows[: args.limit]
    cache: dict[str, tuple[int, bytes, str]] = {}
    rows: list[dict[str, str]] = []
    for index, current_row in enumerate(eligible_rows, start=1):
        enacted_date = enacted_by_bill.get((current_row["bill_id"], current_row["public_law_number"]), "")
        if not enacted_date:
            raise SystemExit(
                f"Missing enacted_date for {current_row['bill_id']} / {current_row['public_law_number']}"
            )
        enacted_year = parse_enacted_year(enacted_date)
        pre_edition = enacted_year - 1
        post_edition = enacted_year
        title = current_row["normalized_title"]
        section = current_row["normalized_section"]
        pre = edition_payload(
            edition_label="pre",
            edition=pre_edition,
            title=title,
            section=section,
            public_law_number=current_row["public_law_number"],
            timeout=args.timeout,
            retries=args.retries,
            sleep_seconds=args.sleep_seconds,
            cache=cache,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            time.sleep(args.sleep_seconds)
        post = edition_payload(
            edition_label="post",
            edition=post_edition,
            title=title,
            section=section,
            public_law_number=current_row["public_law_number"],
            timeout=args.timeout,
            retries=args.retries,
            sleep_seconds=args.sleep_seconds,
            cache=cache,
            dry_run=args.dry_run,
        )
        row = {
            "historical_scan_rank": str(index),
            "current_olrc_scan_rank": current_row["olrc_scan_rank"],
            "triage_rank": current_row["triage_rank"],
            "source_scan_rank": current_row["source_scan_rank"],
            "lineage_review_rank": current_row["lineage_review_rank"],
            "bill_id": current_row["bill_id"],
            "public_law_number": current_row["public_law_number"],
            "enacted_date": enacted_date,
            "target_reference": current_row["target_reference"],
            "target_reference_type": current_row["target_reference_type"],
            "normalized_title": title,
            "normalized_section": section,
            "pre_edition": str(pre_edition),
            "post_edition": str(post_edition),
            **{key: value for key, value in pre.items() if not key.endswith("_fetch_error")},
            **{key: value for key, value in post.items() if not key.endswith("_fetch_error")},
            "annual_text_hash_status": "",
            "annual_public_law_window_status": "",
            "historical_review_status": "",
            "lineage_evidence_status": "historical_edition_scan_not_codified_lineage_or_text_diff_evidence",
            "evidence_layers": "; ".join(EVIDENCE_LAYERS),
            "missing_links": "; ".join(MISSING_LINKS),
            "source_review_notes": (
                "Annual OLRC pre/post edition pages are source scaffolding only; "
                "manual classification and source-reviewed text-diff adjudication are still required."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["annual_text_hash_status"] = annual_hash_status(row)
        row["annual_public_law_window_status"] = annual_public_law_status(row)
        row["historical_review_status"] = historical_review_status(row)
        rows.append(row)
        if not args.dry_run and index < len(eligible_rows):
            time.sleep(args.sleep_seconds)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    both_fetched = sum(
        row["historical_review_status"] == "annual_pre_post_pages_fetched_needs_manual_diff_review"
        for row in rows
    )
    changed_hashes = sum(row["annual_text_hash_status"] == "pre_post_hash_changed" for row in rows)
    public_law_appears = sum(
        row["annual_public_law_window_status"] == "public_law_appears_in_post_edition_only"
        for row in rows
    )
    path.write_text(
        "\n".join(
            [
                "# Statutory Lineage OLRC Historical Scan Metadata",
                "",
                f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
                f"- source_input: `{args.input}`",
                f"- output_rows: {len(rows)}",
                f"- pre_post_page_pairs_fetched: {both_fetched}",
                f"- pre_post_hash_changed_rows: {changed_hashes}",
                f"- public_law_appears_in_post_edition_only_rows: {public_law_appears}",
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
    parser.add_argument("--input", type=Path, default=CURRENT_SCAN)
    parser.add_argument("--queue", type=Path, default=QUEUE)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    current_rows = read_csv(args.input)
    queue_rows = read_csv(args.queue)
    if not current_rows:
        raise SystemExit(f"{args.input} has no rows.")
    if not queue_rows:
        raise SystemExit(f"{args.queue} has no rows.")
    rows = build_rows(current_rows, queue_rows, args)
    if not rows:
        raise SystemExit("No eligible OLRC current-scan rows for historical edition availability scan.")
    write_csv(args.output, rows)
    write_metadata(args.metadata, rows, args)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
