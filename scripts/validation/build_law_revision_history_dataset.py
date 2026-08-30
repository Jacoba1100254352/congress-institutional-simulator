#!/usr/bin/env python3
"""Build a bounded statutory-revision proxy sample from Congress.gov laws."""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.congress.gov/v3"
USER_AGENT = "congress-institutional-simulator-validation/0.4"
OUT_CSV = Path("data/validation/raw/law_revision_history.csv")
OUT_METADATA = Path("data/validation/raw/law_revision_history.metadata.md")

PATTERNS = {
    "amended": re.compile(r"\bamend(?:s|ed|ing|ment|ments)?\b", re.IGNORECASE),
    "reauthorized": re.compile(r"\breauthori[sz](?:e|es|ed|ing|ation|ations)?\b", re.IGNORECASE),
    "repealed": re.compile(r"\brepeal(?:s|ed|ing)?\b", re.IGNORECASE),
    "expired": re.compile(r"\b(?:sunset|sunsets|sunsetted|sunsetting|expire|expires|expired|expiration|termination date)\b", re.IGNORECASE),
}
EXTENSION_PATTERN = re.compile(
    r"\bextend(?:s|ed|ing)?\b.{0,100}\b(?:authorization|program|commission|through|until|expire|expiration|fiscal year|fy\s*\d{4})\b",
    re.IGNORECASE,
)


def env_values(path: Path | None) -> dict[str, str]:
    values: dict[str, str] = {}
    if path is None or not path.exists():
        return values
    for line in path.read_text(errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def api_get(path: str, params: dict[str, object], retries: int = 4) -> dict[str, object]:
    request_url = f"{API_BASE}{path}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=25) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)
    raise RuntimeError("unreachable retry state")


def parse_congresses(value: str) -> list[int]:
    congresses: list[int] = []
    for part in value.split(","):
        stripped = part.strip()
        if stripped:
            congresses.append(int(stripped))
    return congresses or [118]


def text_only(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def law_id(law: dict[str, object]) -> str:
    laws = law.get("laws")
    if isinstance(laws, list) and laws and isinstance(laws[0], dict):
        return str(laws[0].get("number") or "").strip()
    congress = law.get("congress")
    latest = law.get("latestAction")
    text = str(latest.get("text") if isinstance(latest, dict) else "")
    match = re.search(r"Public Law No:\s*([0-9]+-[0-9]+)", text)
    if match:
        return match.group(1)
    return f"{congress}-{law.get('type', '').lower()}-{law.get('number', '')}"


def bill_id(law: dict[str, object]) -> str:
    return f"{law.get('congress')}-{str(law.get('type', '')).lower()}-{law.get('number')}"


def source_url(congress: int, bill_type: str, number: object) -> str:
    bill_kind = bill_type.lower()
    return f"https://www.congress.gov/bill/{congress}th-congress/{bill_kind}-bill/{number}"


def law_refs(api_key: str, congresses: list[int], laws_per_congress: int) -> list[dict[str, object]]:
    refs: dict[str, dict[str, object]] = {}
    for congress in congresses:
        offset = 0
        while len([row for row in refs.values() if row.get("congress") == congress]) < laws_per_congress:
            remaining = laws_per_congress - len([row for row in refs.values() if row.get("congress") == congress])
            payload = api_get(
                f"/law/{congress}/pub",
                {"api_key": api_key, "format": "json", "limit": min(250, remaining), "offset": offset},
            )
            bills = payload.get("bills", [])
            if not isinstance(bills, list) or not bills:
                break
            for bill in bills:
                if not isinstance(bill, dict):
                    continue
                identifier = law_id(bill)
                if identifier:
                    refs[identifier] = bill
            offset += len(bills)
            if len(bills) == 0:
                break
    return sorted(refs.values(), key=lambda row: law_id(row))


def summaries_text(api_key: str, congress: int, bill_type: str, number: object) -> tuple[str, int]:
    payload = api_get(
        f"/bill/{congress}/{bill_type.lower()}/{number}/summaries",
        {"api_key": api_key, "format": "json", "limit": 250},
    )
    summaries = payload.get("summaries", [])
    if not isinstance(summaries, list):
        return "", 0
    values = [text_only(row.get("text", "")) for row in summaries if isinstance(row, dict)]
    return " ".join(value for value in values if value), len(summaries)


def titles_text(api_key: str, congress: int, bill_type: str, number: object) -> tuple[str, int]:
    payload = api_get(
        f"/bill/{congress}/{bill_type.lower()}/{number}/titles",
        {"api_key": api_key, "format": "json", "limit": 250},
    )
    titles = payload.get("titles", [])
    if not isinstance(titles, list):
        return "", 0
    values = [text_only(row.get("title", "")) for row in titles if isinstance(row, dict)]
    return " ".join(value for value in values if value), len(titles)


def enacted_date(row: dict[str, object]) -> str:
    latest = row.get("latestAction")
    if isinstance(latest, dict):
        return str(latest.get("actionDate") or "")
    return ""


def classify_revision(corpus: str) -> tuple[dict[str, str], str]:
    flags = {name: "1" if pattern.search(corpus) else "0" for name, pattern in PATTERNS.items()}
    if flags["reauthorized"] == "0" and EXTENSION_PATTERN.search(corpus):
        flags["reauthorized"] = "1"
    flags["invalidated"] = "0"
    labels = [name for name, value in flags.items() if value == "1"]
    return flags, ";".join(labels)


def build_rows(api_key: str, args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    refs = law_refs(api_key, parse_congresses(args.congresses), args.laws_per_congress)
    for index, ref in enumerate(refs, start=1):
        congress = int(ref.get("congress") or 0)
        bill_type = str(ref.get("type") or "").lower()
        number = ref.get("number")
        if not congress or not bill_type or not number:
            continue
        summaries, summary_count = summaries_text(api_key, congress, bill_type, number)
        titles, title_count = titles_text(api_key, congress, bill_type, number)
        title = text_only(ref.get("title") or "")
        corpus = " ".join(part for part in (title, titles, summaries) if part)
        flags, basis = classify_revision(corpus)
        rows.append({
            "law_id": law_id(ref),
            "enacted_date": enacted_date(ref),
            "amended": flags["amended"],
            "reauthorized": flags["reauthorized"],
            "repealed": flags["repealed"],
            "expired": flags["expired"],
            "invalidated": flags["invalidated"],
            "congress": str(congress),
            "bill_id": bill_id(ref),
            "public_law_number": law_id(ref),
            "bill_title": title,
            "policy_area": "Unclassified",
            "revision_terms": basis,
            "summary_count": str(summary_count),
            "title_count": str(title_count),
            "source_url": source_url(congress, bill_type, number),
        })
        if index % 25 == 0:
            print(f"Fetched {index} / {len(refs)} public-law rows", file=sys.stderr)
        if args.sleep > 0.0:
            time.sleep(args.sleep)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "law_id",
        "enacted_date",
        "amended",
        "reauthorized",
        "repealed",
        "expired",
        "invalidated",
        "congress",
        "bill_id",
        "public_law_number",
        "bill_title",
        "policy_area",
        "revision_terms",
        "summary_count",
        "title_count",
        "source_url",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, str]]) -> None:
    total = len(rows)
    counts = {
        field: sum(1 for row in rows if row[field] == "1")
        for field in ("amended", "reauthorized", "repealed", "expired", "invalidated")
    }
    lines = [
        "# Law Revision History Raw Validation Dataset",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Source:",
        "",
        "- Congress.gov API v3 law-list, bill-summary, and bill-title endpoints.",
        "- API documentation: https://api.congress.gov/",
        f"- Congresses sampled: {args.congresses}.",
        f"- Maximum public laws per Congress: {args.laws_per_congress}.",
        "- API key: provided key, not recorded.",
        "",
        "Transformation:",
        "",
        "- Unit of observation is an enacted public law.",
        "- `law_id` and `public_law_number` use the Congress.gov public-law number when available.",
        "- `enacted_date` is the public-law action date from the Congress.gov law-list endpoint.",
        "- `policy_area` is currently `Unclassified` because the builder avoids per-bill detail calls to keep the source refresh bounded.",
        "- Revision flags are text-derived indicators from enacted-law titles and CRS summaries: amendment, reauthorization or extension, repeal, and sunset/expiration language.",
        "- `invalidated` is fixed at `0` because Congress.gov law titles and summaries are not a judicial-invalidation source; the SCDB court-review extract is the current invalidation proxy.",
        "",
        "Rows:",
        "",
        f"- Normalized rows: {total}",
        f"- Amendment-text rows: {counts['amended']}",
        f"- Reauthorization/extension-text rows: {counts['reauthorized']}",
        f"- Repeal-text rows: {counts['repealed']}",
        f"- Sunset/expiration-text rows: {counts['expired']}",
        f"- Invalidation-text rows: {counts['invalidated']}",
        "",
        "Claim boundary:",
        "",
        "This file supports a bounded statutory revision-activity proxy for public laws whose titles or summaries mention amendment, reauthorization, repeal, or sunset/expiration language. It does not provide longitudinal lineage for every target statute, observed expiration outcomes, codified-text diffs, OLRC notes, or later judicial invalidation.",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Optional dotenv file containing CONGRESS_API_KEY.")
    parser.add_argument("--api-key", help="Congress.gov API key. Defaults to CONGRESS_API_KEY.")
    parser.add_argument("--congresses", default="117,118")
    parser.add_argument("--laws-per-congress", type=int, default=80)
    parser.add_argument("--sleep", type=float, default=0.03)
    args = parser.parse_args()

    values = env_values(args.env_file)
    api_key = args.api_key or os.environ.get("CONGRESS_API_KEY") or values.get("CONGRESS_API_KEY")
    if not api_key:
        raise SystemExit("CONGRESS_API_KEY not found. Pass --env-file or export it in the environment.")

    rows = build_rows(api_key, args)
    if not rows:
        raise SystemExit("No Congress.gov public-law rows matched the requested query.")
    write_csv(rows)
    write_metadata(args, rows)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
