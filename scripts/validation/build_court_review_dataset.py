#!/usr/bin/env python3
"""Build a normalized court-review validation dataset from SCDB."""

from __future__ import annotations

import argparse
import csv
import re
import tempfile
import zipfile
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


RELEASE_PAGE = "https://scdb.la.psu.edu/data/2025-release-01/"
DOWNLOAD_LABEL = "Download CSV Organized by Supreme Court Citation"
USER_AGENT = "congress-institutional-simulator-validation/0.1"
OUT_CSV = Path("data/validation/raw/court_review.csv")
OUT_METADATA = Path("data/validation/raw/court_review.metadata.md")
FIELDNAMES = [
    "case_id",
    "case_name",
    "term",
    "decision_date",
    "issue",
    "emergency_order",
    "invalidated",
    "vote_margin",
    "signed_opinion",
    "us_cite",
    "sct_cite",
    "lexis_cite",
    "law_type",
    "law_supp",
    "law_minor",
    "usc_sections",
]


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return response.read()


def resolve_download_url(release_page: str) -> str:
    html = fetch_text(release_page)
    pattern = re.compile(
        r'<a\b(?=[^>]*\bhref="(?P<href>[^"]+)")[^>]*>'
        r'(?:(?!</a>).)*?'
        + re.escape(DOWNLOAD_LABEL)
        + r".*?</a>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        raise SystemExit(f"Could not find SCDB download link labeled {DOWNLOAD_LABEL!r} on {release_page}.")
    return match.group("href").replace("&amp;", "&")


def numeric_int(value: str, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def normalize_usc_sections(value: str) -> list[str]:
    """Extract stable title-section U.S.C. identifiers from SCDB lawMinor text."""
    text = (value or "").replace("\u00a7", " ")
    sections: list[str] = []
    for match in re.finditer(
        r"\b(?P<title>\d{1,3})\s*U\.?S\.?C\.?\s*(?:\u00a7+\s*)?"
        r"(?P<section>[0-9A-Za-z][0-9A-Za-z.\-]*)",
        text,
        flags=re.IGNORECASE,
    ):
        title = str(int(match.group("title")))
        section = match.group("section").strip().lower()
        normalized = f"{title} U.S.C. {section}"
        if normalized not in sections:
            sections.append(normalized)
    return sections


def normalized_rows(zip_bytes: bytes, start_term: int, end_term: int, limit: int | None) -> tuple[list[dict[str, str]], str]:
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        tmp.write(zip_bytes)
        tmp.flush()
        with zipfile.ZipFile(tmp.name) as archive:
            csv_name = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
            with archive.open(csv_name) as handle:
                text = (line.decode("utf-8-sig") for line in handle)
                reader = csv.DictReader(text)
                rows: list[dict[str, str]] = []
                for row in reader:
                    term = numeric_int(row.get("term", ""))
                    if term < start_term or term > end_term:
                        continue
                    declaration = numeric_int(row.get("declarationUncon", ""))
                    decision_type = numeric_int(row.get("decisionType", ""))
                    maj_votes = numeric_int(row.get("majVotes", ""))
                    min_votes = numeric_int(row.get("minVotes", ""))
                    rows.append({
                        "case_id": str(row.get("caseId", "")).strip(),
                        "case_name": str(row.get("caseName", "")).strip(),
                        "term": str(term),
                        "decision_date": str(row.get("dateDecision", "")).strip(),
                        "issue": str(row.get("issueArea") or row.get("issue") or "unknown").strip() or "unknown",
                        "emergency_order": "0",
                        "invalidated": "1" if declaration in {2, 3, 4} else "0",
                        "vote_margin": str(max(0, maj_votes - min_votes)),
                        "signed_opinion": "1" if decision_type == 1 else "0",
                        "us_cite": str(row.get("usCite", "")).strip(),
                        "sct_cite": str(row.get("sctCite", "")).strip(),
                        "lexis_cite": str(row.get("lexisCite", "")).strip(),
                        "law_type": str(row.get("lawType", "")).strip(),
                        "law_supp": str(row.get("lawSupp", "")).strip(),
                        "law_minor": str(row.get("lawMinor", "")).strip(),
                        "usc_sections": "; ".join(normalize_usc_sections(str(row.get("lawMinor", "")))),
                    })
                    if limit is not None and len(rows) >= limit:
                        break
    return rows, csv_name


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(
    *,
    rows: list[dict[str, str]],
    release_page: str,
    download_url: str,
    source_csv: str,
    start_term: int,
    end_term: int,
) -> None:
    invalidated = sum(1 for row in rows if row["invalidated"] == "1")
    signed = sum(1 for row in rows if row["signed_opinion"] == "1")
    usc_rows = sum(1 for row in rows if row["usc_sections"])
    unique_usc_sections = {
        section.strip()
        for row in rows
        for section in row["usc_sections"].split(";")
        if section.strip()
    }
    lines = [
        "# Court Review Raw Validation Dataset",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Source:",
        "",
        "- Supreme Court Database, 2025 Release 01.",
        f"- Release page: {release_page}",
        f"- Download URL used: {download_url}",
        f"- Source CSV inside archive: `{source_csv}`.",
        "",
        "Transformation:",
        "",
        f"- Included SCDB terms: {start_term}-{end_term}.",
        "- Unit of observation: SCDB case-centered row organized by Supreme Court citation.",
        "- `invalidated` is `1` when `declarationUncon` is 2, 3, or 4; `declarationUncon=1` is no declaration of unconstitutionality.",
        "- `signed_opinion` is `1` when `decisionType=1`, SCDB's signed-opinion category.",
        "- `vote_margin` is `majVotes - minVotes` with a floor at 0.",
        "- `emergency_order` is fixed at `0` because this SCDB case-centered release covers merits decisions, not a separately coded emergency or shadow-docket dataset.",
        "- `law_type`, `law_supp`, and `law_minor` preserve SCDB legal-authority fields for bounded statute-linkage audits.",
        "- `usc_sections` normalizes U.S. Code citations found in `lawMinor`; blank values mean no U.S.C. citation was parsed from the SCDB row.",
        "",
        "Rows:",
        "",
        f"- Normalized rows: {len(rows)}",
        f"- Invalidated rows: {invalidated}",
        f"- Signed-opinion rows: {signed}",
        f"- Rows with parsed U.S.C. sections: {usc_rows}",
        f"- Unique parsed U.S.C. sections: {len(unique_usc_sections)}",
        "",
        "Claim boundary:",
        "",
        "This file supports a merits-case court-review bridge for invalidation, vote-margin, signed-opinion, and bounded legal-authority metadata. Parsed U.S.C. sections are not direct public-law, bill, lower-court, emergency-order, implementation-effect, welfare, or model validation evidence.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-page", default=RELEASE_PAGE)
    parser.add_argument("--source-url", help="Direct SCDB zip download URL. Defaults to resolving the case-centered CSV from --release-page.")
    parser.add_argument("--start-term", type=int, default=1946)
    parser.add_argument("--end-term", type=int, default=2024)
    parser.add_argument("--limit", type=int, help="Optional row limit for smoke testing.")
    args = parser.parse_args()

    download_url = args.source_url or resolve_download_url(args.release_page)
    zip_bytes = fetch_bytes(download_url)
    if not zip_bytes.startswith(b"PK"):
        raise SystemExit(f"SCDB download did not return a zip archive: {download_url}")
    rows, source_csv = normalized_rows(zip_bytes, args.start_term, args.end_term, args.limit)
    if not rows:
        raise SystemExit("No SCDB rows matched the requested term range.")
    write_csv(rows)
    write_metadata(
        rows=rows,
        release_page=args.release_page,
        download_url=download_url,
        source_csv=source_csv,
        start_term=args.start_term,
        end_term=args.end_term,
    )
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
