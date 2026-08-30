#!/usr/bin/env python3
"""Build a bounded Federal Register public-law authority linkage cache."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_API = "https://www.federalregister.gov/api/v1/documents.json"
DETAIL_API = "https://www.federalregister.gov/api/v1/documents"
USER_AGENT = "congress-institutional-simulator-validation/0.7"
LAW_LINKAGE_CSV = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("data/validation/raw/rulemaking_authority_linkage.csv")
OUT_METADATA = Path("data/validation/raw/rulemaking_authority_linkage.metadata.md")
PUBLIC_LAW_RE = re.compile(
    r"\b(?:Public\s+Law|Pub\.?\s*L\.?|Pub\.?\s*Law)\s*(?:No\.?\s*)?(\d{2,3})[-–](\d{1,5})\b",
    re.IGNORECASE,
)
USC_RE = re.compile(
    r"\b\d+\s+U\.S\.C\.?\s+(?:§+\s*)?[0-9A-Za-z][0-9A-Za-z.\-]*(?:\([^)]+\))*",
    re.IGNORECASE,
)
CLAIM_BOUNDARY = (
    "Bounded Federal Register text search for public-law authority citations only; "
    "not proof of exhaustive implementation, proposed-rule history, enforcement "
    "outcome, appropriations capacity, complete public-comment record, court "
    "review, public benefit, welfare, causal effect, or model validation."
)
OUTPUT_FIELDS = [
    "public_law_number",
    "bill_id",
    "congress",
    "bill_type",
    "bill_number",
    "linkage_status",
    "candidate_rule_count",
    "matched_rule_count",
    "text_verified_rule_count",
    "matched_document_numbers",
    "matched_publication_dates",
    "matched_rule_titles",
    "federal_register_citations",
    "agency_names",
    "cfr_references",
    "regulation_id_numbers",
    "docket_ids",
    "public_law_citations",
    "usc_citations",
    "authority_excerpt",
    "source_urls",
    "raw_text_urls",
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


def text_get(url: str, retries: int = 3) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8", "replace")
        except (HTTPError, TimeoutError, URLError, OSError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_public_law(congress: str, number: str) -> str:
    return f"{int(congress)}-{int(number)}"


def public_law_citations(text: str) -> set[str]:
    return {
        normalize_public_law(congress, number)
        for congress, number in PUBLIC_LAW_RE.findall(text)
    }


def usc_citations(text: str) -> set[str]:
    cleaned = normalize_spaces(text)
    values: set[str] = set()
    for match in USC_RE.findall(cleaned):
        value = re.sub(r"\s+", " ", match).strip(" .;,)")
        if value:
            values.add(value)
    return values


def join(values: set[str] | list[str], limit: int = 0) -> str:
    ordered = sorted(value for value in values if value)
    if limit > 0:
        ordered = ordered[:limit]
    return "; ".join(ordered)


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


def detail_url(document_number: str) -> str:
    return f"{DETAIL_API}/{document_number}.json"


def search_terms(public_law_number: str) -> list[str]:
    return [
        f"Public Law {public_law_number}",
        f"Pub. L. {public_law_number}",
        f"Pub. L. No. {public_law_number}",
        public_law_number,
    ]


def search_documents(public_law_number: str, per_term: int) -> list[str]:
    documents: list[str] = []
    seen: set[str] = set()
    fields = ["document_number", "title", "publication_date", "html_url"]
    for term in search_terms(public_law_number):
        params: list[tuple[str, object]] = [
            ("conditions[term]", term),
            ("conditions[type][]", "RULE"),
            ("conditions[correction]", "0"),
            ("order", "relevance"),
            ("per_page", per_term),
        ]
        for field in fields:
            params.append(("fields[]", field))
        try:
            payload = api_get(f"{SEARCH_API}?{urlencode(params)}")
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


def authority_excerpt(text: str, public_law_number: str) -> str:
    normalized = normalize_spaces(text)
    patterns = [
        re.compile(rf"(Public Law|Pub\.?\s*L\.?|Pub\.?\s*Law)\s*(No\.?\s*)?{re.escape(public_law_number)}", re.IGNORECASE),
        re.compile(r"\bAuthority:\s*", re.IGNORECASE),
    ]
    for pattern in patterns:
        match = pattern.search(normalized)
        if match:
            start = max(0, match.start() - 90)
            end = min(len(normalized), match.end() + 220)
            return normalized[start:end]
    return ""


def build_row(source: dict[str, str], args: argparse.Namespace) -> dict[str, str]:
    public_law_number = source.get("public_law_number", "").strip()
    candidate_documents = search_documents(public_law_number, args.per_term)
    if args.max_documents_per_law > 0:
        candidate_documents = candidate_documents[:args.max_documents_per_law]

    titles: list[str] = []
    publication_dates: set[str] = set()
    citations: set[str] = set()
    agencies: set[str] = set()
    cfrs: set[str] = set()
    rins: set[str] = set()
    dockets: set[str] = set()
    source_urls: set[str] = set()
    raw_text_urls: set[str] = set()
    public_laws: set[str] = set()
    uscs: set[str] = set()
    verified_documents: set[str] = set()
    excerpts: list[str] = []

    for document_number in candidate_documents:
        try:
            detail = api_get(detail_url(document_number))
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            continue
        raw_text_url = str(detail.get("raw_text_url") or "")
        agency_value = agency_names(detail.get("agencies"))
        cfr_value = cfr_summary(detail.get("cfr_references"))
        if not raw_text_url:
            continue
        try:
            text = text_get(raw_text_url)
        except (HTTPError, TimeoutError, URLError, OSError, RuntimeError):
            continue
        found_public_laws = public_law_citations(text)
        if public_law_number in found_public_laws:
            verified_documents.add(document_number)
            title = str(detail.get("title") or "")
            if title:
                titles.append(title)
            if detail.get("publication_date"):
                publication_dates.add(str(detail["publication_date"]))
            if detail.get("citation"):
                citations.add(str(detail["citation"]))
            if detail.get("html_url"):
                source_urls.add(str(detail["html_url"]))
            raw_text_urls.add(raw_text_url)
            if agency_value:
                agencies.add(agency_value)
            if cfr_value:
                cfrs.add(cfr_value)
            for value in detail.get("regulation_id_numbers") or []:
                if str(value).strip():
                    rins.add(str(value).strip())
            for value in detail.get("docket_ids") or []:
                if str(value).strip():
                    dockets.add(str(value).strip())
            public_laws.update(found_public_laws)
            uscs.update(usc_citations(text))
            excerpt = authority_excerpt(text, public_law_number)
            if excerpt:
                excerpts.append(excerpt)
        if args.sleep > 0:
            time.sleep(args.sleep)

    verified = len(verified_documents)
    status = "federal_register_authority_match" if verified else "no_federal_register_authority_match"
    layers = ["public_law_bill_metadata", "federal_register_rule_search"]
    if verified:
        layers.append("public_law_authority_text_match")
    if uscs:
        layers.append("usc_authority_citations")
    missing = [
        "proposed_rule_history",
        "complete_regulations_comments",
        "enforcement_outcomes",
        "appropriations_capacity",
        "court_review_or_invalidation",
        "causal_implementation_effect",
        "exhaustive_authority_census",
    ]
    if not verified:
        missing.insert(0, "federal_register_public_law_authority_match")

    return {
        "public_law_number": public_law_number,
        "bill_id": source.get("bill_id", ""),
        "congress": source.get("congress", ""),
        "bill_type": source.get("bill_type", ""),
        "bill_number": source.get("bill_number", ""),
        "linkage_status": status,
        "candidate_rule_count": str(len(candidate_documents)),
        "matched_rule_count": str(verified),
        "text_verified_rule_count": str(verified),
        "matched_document_numbers": "; ".join(document for document in candidate_documents if document in verified_documents),
        "matched_publication_dates": join(publication_dates),
        "matched_rule_titles": "; ".join(titles[:5]),
        "federal_register_citations": join(citations),
        "agency_names": join(agencies),
        "cfr_references": join(cfrs),
        "regulation_id_numbers": join(rins),
        "docket_ids": join(dockets),
        "public_law_citations": join(public_laws, limit=30),
        "usc_citations": join(uscs, limit=40),
        "authority_excerpt": excerpts[0] if excerpts else "",
        "source_urls": join(source_urls),
        "raw_text_urls": join(raw_text_urls),
        "evidence_layers": "; ".join(layers),
        "missing_links": "; ".join(missing),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    matched = sum(1 for row in rows if row["linkage_status"] == "federal_register_authority_match")
    verified_docs = sum(int(row["text_verified_rule_count"] or "0") for row in rows)
    usc_rows = sum(1 for row in rows if row["usc_citations"])
    status_lines = "\n".join(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    args.metadata.write_text(
        "# Rulemaking Authority Linkage Raw Dataset\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Source:\n\n"
        "- Federal Register API v1 document search and single-document endpoints.\n"
        "- Federal Register full-text text URLs exposed by the single-document endpoint.\n"
        f"- Public-law input file: `{args.law_linkage_csv}`.\n\n"
        "Transformation:\n\n"
        "- Reads bounded public-law bill/action rows from the cached Congress.gov linkage file.\n"
        "- Searches Federal Register rule documents for exact public-law citation forms.\n"
        "- Fetches matched rule metadata and raw text, then verifies whether the text contains the public-law number.\n"
        "- Extracts bounded public-law citation lists, U.S. Code citation lists, agencies, CFR references, RINs, dockets, and a short authority-citation excerpt.\n"
        "- Rows are keyed by public-law number; this is an authority-search bridge, not an exhaustive implementation census.\n\n"
        "Rows:\n\n"
        f"- Public-law rows searched: {len(rows)}.\n"
        f"- Rows with text-verified Federal Register authority matches: {matched}.\n"
        f"- Candidate rule documents inspected: {sum(int(row['candidate_rule_count'] or '0') for row in rows)}.\n"
        f"- Text-verified matched rule documents: {verified_docs}.\n"
        f"- Rows with U.S. Code citations in matched rule text: {usc_rows}.\n\n"
        "Linkage statuses:\n\n"
        f"{status_lines}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law-linkage-csv", type=Path, default=LAW_LINKAGE_CSV)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata", type=Path, default=OUT_METADATA)
    parser.add_argument("--per-term", type=int, default=5)
    parser.add_argument("--max-documents-per-law", type=int, default=6)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--progress-every", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.law_linkage_csv.exists():
        raise SystemExit(f"{args.law_linkage_csv} is missing; run make build-law-revision-bill-linkage-raw first.")
    source_rows = [
        row for row in read_csv(args.law_linkage_csv)
        if row.get("public_law_number", "").strip()
    ]
    if not source_rows:
        raise SystemExit(f"{args.law_linkage_csv} has no public-law rows.")

    rows: list[dict[str, str]] = []
    for index, source in enumerate(source_rows, start=1):
        if args.progress_every > 0 and index % args.progress_every == 0:
            print(f"Searched Federal Register authority text for {index} public laws", file=sys.stderr)
        rows.append(build_row(source, args))
        if args.sleep > 0:
            time.sleep(args.sleep)

    write_csv(rows, args.output)
    write_metadata(args, rows)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
