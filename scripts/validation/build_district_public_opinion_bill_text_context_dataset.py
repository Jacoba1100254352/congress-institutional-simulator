#!/usr/bin/env python3
"""Build official bill-text context for district public-opinion review packets."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


SOURCE_PACKETS = Path("reports/district-public-opinion-source-packets.csv")
OUT_CSV = Path("data/validation/raw/district_public_opinion_bill_text_context.csv")
OUT_METADATA = Path(
    "data/validation/raw/district_public_opinion_bill_text_context.metadata.md"
)
USER_AGENT = "congress-institutional-simulator/validation-bill-text-context"

EVIDENCE_LAYERS = (
    "district_public_opinion_source_packet; official_govinfo_billstatus_xml; "
    "official_congressional_research_service_bill_summary"
)
MISSING_LINKS = (
    "exact_bill_topic_item_wording_review; bill_text_direction_alignment_review; "
    "bill_topic_public_opinion; respondent_geography_merge; "
    "MRP_or_small_area_estimate; bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)
CLAIM_BOUNDARY = (
    "Official bill-context cache only; rows preserve GovInfo BILLSTATUS titles, "
    "legislative subjects, and the latest available CRS summary for current district "
    "public-opinion review packets. They do not establish a survey-item match, "
    "bill-topic public support, district support, affected-group support or harm, "
    "public benefit, causal representation, or model validation."
)

FIELDNAMES = [
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "display_title",
    "official_title",
    "short_titles",
    "legislative_subjects",
    "latest_summary_version_code",
    "latest_summary_action_date",
    "latest_summary_action_description",
    "latest_summary_update_date",
    "latest_summary_text",
    "summary_count",
    "govinfo_billstatus_url",
    "govinfo_billstatus_sha256",
    "source_status",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CACHE_INPUT_FIELDS = (
    "packet_rank",
    "readiness_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
)
SOURCE_STATUSES = {
    "official_govinfo_billstatus_with_crs_summary",
    "official_govinfo_billstatus_without_crs_summary",
}


class PlainTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.parts.append(value)

    def text(self) -> str:
        return " ".join(self.parts)


def normalize_markup(value: str) -> str:
    parser = PlainTextExtractor()
    parser.feed(html.unescape(value))
    parser.close()
    return parser.text()


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def child_text(element: ET.Element, name: str) -> str:
    for child in element:
        if local_name(child) == name:
            return " ".join((child.text or "").split())
    return ""


def first_container(root: ET.Element, name: str) -> ET.Element | None:
    return next((element for element in root.iter() if local_name(element) == name), None)


def read_packets() -> list[dict[str, str]]:
    if not SOURCE_PACKETS.exists():
        raise SystemExit(
            f"{SOURCE_PACKETS} is missing; run make district-public-opinion-source-packets first."
        )
    with SOURCE_PACKETS.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{SOURCE_PACKETS} is empty.")
    required = {
        "packet_rank",
        "readiness_rank",
        "bill_id",
        "public_law_number",
        "policy_area",
        "sponsor_districts",
    }
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"{SOURCE_PACKETS} is missing columns: {sorted(missing)}")
    bill_ids = [row["bill_id"].strip() for row in rows]
    if len(bill_ids) != len(set(bill_ids)):
        raise SystemExit(f"{SOURCE_PACKETS} contains duplicate bill IDs.")
    return sorted(rows, key=lambda row: int(row["packet_rank"]))


def existing_output_matches(packets: list[dict[str, str]]) -> bool:
    if not OUT_CSV.exists():
        return False
    try:
        with OUT_CSV.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDNAMES:
                return False
            rows = list(reader)
    except (OSError, csv.Error):
        return False
    if len(rows) != len(packets):
        return False
    for packet, row in zip(packets, rows, strict=True):
        if any(
            row.get(field, "").strip() != packet.get(field, "").strip()
            for field in CACHE_INPUT_FIELDS
        ):
            return False
        bill_id = packet.get("bill_id", "").strip()
        source_hash = row.get("govinfo_billstatus_sha256", "").strip().lower()
        if (
            row.get("govinfo_billstatus_url", "").strip() != govinfo_url(bill_id)
            or len(source_hash) != 64
            or any(character not in "0123456789abcdef" for character in source_hash)
            or row.get("source_status", "").strip() not in SOURCE_STATUSES
            or row.get("evidence_layers", "").strip() != EVIDENCE_LAYERS
            or row.get("missing_links", "").strip() != MISSING_LINKS
            or row.get("claim_boundary", "").strip() != CLAIM_BOUNDARY
        ):
            return False
    return True


def read_existing_rows() -> list[dict[str, str]]:
    with OUT_CSV.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bill_id(bill_id: str) -> tuple[int, str, int]:
    parts = bill_id.split("-")
    if len(parts) != 3:
        raise ValueError(f"Unsupported bill ID: {bill_id}")
    return int(parts[0]), parts[1].lower(), int(parts[2])


def govinfo_url(bill_id: str) -> str:
    congress, bill_type, number = parse_bill_id(bill_id)
    return (
        f"https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{bill_type}/"
        f"BILLSTATUS-{congress}{bill_type}{number}.xml"
    )


def fetch(url: str, retries: int, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)
    raise RuntimeError("unreachable retry state")


def title_rows(root: ET.Element) -> list[dict[str, str]]:
    container = first_container(root, "titles")
    if container is None:
        return []
    rows: list[dict[str, str]] = []
    for item in container:
        if local_name(item) != "item":
            continue
        rows.append({
            "title_type": child_text(item, "titleType"),
            "title": child_text(item, "title"),
        })
    return rows


def preferred_title(rows: list[dict[str, str]], title_type: str) -> str:
    return next(
        (row["title"] for row in rows if row["title_type"] == title_type and row["title"]),
        "",
    )


def unique_join(values: list[str]) -> str:
    return "; ".join(dict.fromkeys(value for value in values if value))


def legislative_subjects(root: ET.Element) -> str:
    container = first_container(root, "legislativeSubjects")
    if container is None:
        return ""
    values: list[str] = []
    for item in container:
        value = child_text(item, "name")
        if value:
            values.append(value)
    return unique_join(sorted(values))


def summary_rows(root: ET.Element) -> list[dict[str, str]]:
    container = first_container(root, "summaries")
    if container is None:
        return []
    rows: list[dict[str, str]] = []
    for item in container:
        if local_name(item) != "summary":
            continue
        raw_text = child_text(item, "text")
        rows.append({
            "version_code": child_text(item, "versionCode"),
            "action_date": child_text(item, "actionDate"),
            "action_description": child_text(item, "actionDesc"),
            "update_date": child_text(item, "updateDate"),
            "text": normalize_markup(raw_text),
        })
    return rows


def latest_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    if not rows:
        return {
            "version_code": "",
            "action_date": "",
            "action_description": "",
            "update_date": "",
            "text": "",
        }
    return max(
        rows,
        key=lambda row: (row["action_date"], row["update_date"], row["version_code"]),
    )


def build_row(packet: dict[str, str], xml_bytes: bytes, url: str) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    titles = title_rows(root)
    summaries = summary_rows(root)
    latest = latest_summary(summaries)
    display_title = preferred_title(titles, "Display Title")
    official_title = preferred_title(titles, "Official Title as Introduced")
    short_titles = unique_join([
        row["title"]
        for row in titles
        if row["title"] and "Short Title" in row["title_type"]
    ])
    if not display_title:
        display_title = short_titles or official_title
    if not official_title:
        official_title = display_title
    source_status = (
        "official_govinfo_billstatus_with_crs_summary"
        if latest["text"]
        else "official_govinfo_billstatus_without_crs_summary"
    )
    return {
        "packet_rank": packet["packet_rank"].strip(),
        "readiness_rank": packet["readiness_rank"].strip(),
        "bill_id": packet["bill_id"].strip(),
        "public_law_number": packet["public_law_number"].strip(),
        "policy_area": packet["policy_area"].strip(),
        "sponsor_districts": packet["sponsor_districts"].strip(),
        "display_title": display_title,
        "official_title": official_title,
        "short_titles": short_titles,
        "legislative_subjects": legislative_subjects(root),
        "latest_summary_version_code": latest["version_code"],
        "latest_summary_action_date": latest["action_date"],
        "latest_summary_action_description": latest["action_description"],
        "latest_summary_update_date": latest["update_date"],
        "latest_summary_text": latest["text"],
        "summary_count": str(len(summaries)),
        "govinfo_billstatus_url": url,
        "govinfo_billstatus_sha256": hashlib.sha256(xml_bytes).hexdigest(),
        "source_status": source_status,
        "evidence_layers": EVIDENCE_LAYERS,
        "missing_links": MISSING_LINKS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    with_summaries = sum(1 for row in rows if row["latest_summary_text"])
    unique_subjects = {
        subject
        for row in rows
        for subject in row["legislative_subjects"].split("; ")
        if subject
    }
    lines = [
        "# District Public-Opinion Bill Text Context Metadata",
        "",
        "Source: official GovInfo BILLSTATUS XML, including CRS bill-summary fields.",
        "",
        f"- Review-packet bills: {len(rows)}",
        f"- Bills with a latest CRS summary: {with_summaries}",
        f"- Unique legislative subjects retained: {len(unique_subjects)}",
        "- Raw respondent data: not used or retained.",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="refetch GovInfo even if the existing context matches the packet queue",
    )
    parser.add_argument("--sleep", type=float, default=0.05)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()
    if args.sleep < 0 or args.retries <= 0 or args.timeout <= 0:
        raise SystemExit("sleep must be nonnegative; retries and timeout must be positive.")

    packets = read_packets()
    if not args.refresh and existing_output_matches(packets):
        rows = read_existing_rows()
        write_metadata(rows)
        print(f"Reused {OUT_CSV}")
        print(f"Wrote {OUT_METADATA}")
        return 0

    rows: list[dict[str, str]] = []
    for packet in packets:
        url = govinfo_url(packet["bill_id"])
        xml_bytes = fetch(url, args.retries, args.timeout)
        rows.append(build_row(packet, xml_bytes, url))
        print(f"Fetched bill context for {packet['bill_id']}")
        if args.sleep:
            time.sleep(args.sleep)
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
