#!/usr/bin/env python3
"""Build source-pinned House special-rule and agenda-control panels.

The special-rule classifications come from the House Committee on Rules'
completed-Congress Survey of Activities. Direct GovInfo BILLSTATUS actions
provide rule-resolution dispositions and bill procedure evidence. The parser
never treats nested related-bill or amendment text as a direct action.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

try:
    from .build_govinfo_bill_census_dataset import (
        Action,
        archive_info,
        archive_name,
        archive_url,
        at,
        canonical_actions_sha256,
        committee_reported_match,
        download_archive,
        house_passage_match,
        normalize_space,
        parse_actions,
        sha256_bytes,
        sha256_file,
        stage_from_actions,
        text_at,
    )
    from .reproducible_metadata import write_reproducible_metadata
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_bill_census_dataset import (
        Action,
        archive_info,
        archive_name,
        archive_url,
        at,
        canonical_actions_sha256,
        committee_reported_match,
        download_archive,
        house_passage_match,
        normalize_space,
        parse_actions,
        sha256_bytes,
        sha256_file,
        stage_from_actions,
        text_at,
    )
    from reproducible_metadata import write_reproducible_metadata


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "papers" / "empirical-validation" / "house-agenda-control-panel-specification.md"
SURVEY_CACHE_DIR = ROOT / "out" / "validation-cache" / "house-rules-surveys"
ARCHIVE_DIR = ROOT / "out" / "validation-cache" / "govinfo-billstatus"
GRANT_OUTPUT = ROOT / "data" / "validation" / "raw" / "house_special_rule_grants.csv"
GRANT_METADATA_OUTPUT = ROOT / "data" / "validation" / "raw" / "house_special_rule_grants.metadata.md"
AGENDA_OUTPUT = ROOT / "data" / "validation" / "raw" / "house_agenda_control.csv"
AGENDA_METADATA_OUTPUT = ROOT / "data" / "validation" / "raw" / "house_agenda_control.metadata.md"
USER_AGENT = "congress-institutional-simulator-validation/0.4"
CLASSIFICATION_VERSION = "house-agenda-control-v1"
CONGRESSES = (116, 117, 118)

CENSUS_PATHS = {
    116: ROOT / "data" / "validation" / "raw" / "govinfo_bill_census_116.csv",
    117: ROOT / "data" / "validation" / "raw" / "govinfo_bill_census.csv",
    118: ROOT / "data" / "validation" / "raw" / "govinfo_bill_census_118.csv",
}

CATEGORY_ORDER = {
    "open": 0,
    "modified_open": 1,
    "structured": 2,
    "closed": 3,
}
CATEGORY_LABELS = {
    "open": "open",
    "modified-open": "modified_open",
    "modified open": "modified_open",
    "structured": "structured",
    "closed": "closed",
}
EXPECTED_CATEGORY_COUNTS = {
    116: {"open": 0, "modified_open": 0, "structured": 55, "closed": 60},
    117: {"open": 0, "modified_open": 0, "structured": 57, "closed": 87},
    118: {"open": 0, "modified_open": 1, "structured": 83, "closed": 115},
}
NARRATIVE_CATEGORY_COUNTS = {
    116: {"open": 0, "modified_open": 0, "structured": 55, "closed": 60},
    117: {"open": 0, "modified_open": 0, "structured": 59, "closed": 89},
    118: {"open": 0, "modified_open": 1, "structured": 83, "closed": 115},
}

TABLE_START = "A. Table 1a.--Types of Rules Granted (Consideration)"
TABLE_END = "A. Table 1b.--Types of Rules Granted (Special Procedures)"
MEASURE_ROW_RE = re.compile(
    r"^\s*H\.\s*Res\.\s*(?P<rule>\d+)\s+"
    r"(?P<measure_type>H\.\s*Con\.\s*Res\.|H\.\s*J\.\s*Res\.|"
    r"S\.\s*J\.\s*Res\.|H\.\s*Res\.|H\.\s*R\.|S\.)\s*"
    r"(?P<measure_number>\d+)\b(?P<remainder>.*)$",
    re.IGNORECASE,
)
REPORT_ANNOTATION_RE = re.compile(
    r"^\s*\(\s*H\.\s*Rept\.\s*[^)]*\)\s*",
    re.IGNORECASE,
)
RULE_USE_RE = re.compile(
    r"(?:considered\s+under\s+the\s+provisions\s+of\s+rule|"
    r"pursuant\s+to\s+the\s+provisions\s+of)\s+"
    r"H\.\s*Res\.\s*(\d+)\b",
    re.IGNORECASE,
)
CALENDAR_RE = re.compile(
    r"Placed on the (House|Union|Private) Calendar(?:, Calendar No\.\s*([^.;]+))?",
    re.IGNORECASE,
)
SUSPENSION_PHRASES = (
    "suspend the rules",
    "suspension of the rules",
)
OTHER_PATH_PHRASES = (
    "considered as privileged matter",
    "considered by unanimous consent",
    "passed by unanimous consent",
    "pursuant to a previous order",
    "private calendar",
    "without objection, the chair laid before the house",
)
AMENDMENT_OFFER_CODES = {"H3A100"}


@dataclass(frozen=True)
class SurveySpec:
    congress: int
    package: str
    url: str
    sha256: str
    size_bytes: int

    @property
    def filename(self) -> str:
        return f"{self.package}.htm"


SURVEY_SPECS = {
    116: SurveySpec(
        116,
        "CRPT-116hrpt722",
        "https://www.govinfo.gov/content/pkg/CRPT-116hrpt722/html/CRPT-116hrpt722.htm",
        "5d65df8e35bc575d9c31b3bce10913647dd1dc59b7d8c68f9253f14490eb344a",
        552457,
    ),
    117: SurveySpec(
        117,
        "CRPT-117hrpt709",
        "https://www.govinfo.gov/content/pkg/CRPT-117hrpt709/html/CRPT-117hrpt709.htm",
        "a7777dcd7bec4ff4d00477ec8ad405226505972efbf86e6f5395af215258c969",
        532625,
    ),
    118: SurveySpec(
        118,
        "CRPT-118hrpt979",
        "https://www.govinfo.gov/content/pkg/CRPT-118hrpt979/html/CRPT-118hrpt979.htm",
        "62a7f7d70939c357c7bd7ab8bd8491ddcc6602665796382fc2c2df1ef9eb0aae",
        542453,
    ),
}


GRANT_FIELDNAMES = [
    "grant_id",
    "congress",
    "rule_resolution_id",
    "rule_number",
    "covered_measure_id",
    "covered_measure_type",
    "covered_measure_number",
    "covered_measure_title",
    "amendment_structure",
    "restrictive_structure",
    "survey_package",
    "survey_table",
    "survey_source_url",
    "survey_source_sha256",
    "survey_row_number",
    "rule_source_url",
    "rule_source_xml_update_date",
    "rule_source_xml_sha256",
    "rule_actions_sha256",
    "rule_reported",
    "rule_reported_date",
    "rule_reported_basis",
    "rule_passed_house",
    "rule_passed_house_date",
    "rule_passed_house_basis",
    "rule_disposition",
    "rule_disposition_date",
    "rule_disposition_basis",
    "covered_measure_in_hr_census",
    "linkage_status",
    "classification_version",
    "claim_boundary",
]

AGENDA_ADDITIONAL_FIELDNAMES = [
    "calendar_placed",
    "calendar_name",
    "calendar_number",
    "calendar_date",
    "calendar_basis",
    "suspension_path_evidence",
    "suspension_path_date",
    "suspension_path_basis",
    "other_floor_path_evidence",
    "other_floor_path_date",
    "other_floor_path_basis",
    "direct_rule_ids",
    "direct_rule_action_count",
    "direct_rule_action_date",
    "direct_rule_action_basis",
    "survey_rule_grant_count",
    "adopted_rule_count",
    "nonadopted_rule_count",
    "adopted_rule_ids",
    "nonadopted_rule_ids",
    "adopted_rule_categories",
    "adopted_rule_category_set",
    "most_restrictive_adopted_rule",
    "restrictive_adopted_rule_count",
    "nonrestrictive_adopted_rule_count",
    "mixed_adopted_rule_categories",
    "floor_path",
    "floor_path_basis",
    "house_floor_amendment_offer_actions",
    "house_floor_amendment_disposition_actions",
    "introduction_to_referral_days",
    "referral_to_committee_advance_days",
    "committee_advance_to_floor_days",
    "introduction_to_floor_days",
    "direct_rule_link_status",
    "agenda_integrity_status",
    "agenda_classification_version",
    "agenda_claim_boundary",
]

CLAIM_BOUNDARY = (
    "Official-source House procedure and timing evidence only; not causal agenda-control, "
    "unobserved floor-demand, public-benefit, welfare, capture, or model-validation evidence."
)


class PreTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.casefold() == "pre":
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "pre" and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


def flag(value: bool) -> str:
    return "1" if value else "0"


def normalize_category_label(value: str) -> str | None:
    return CATEGORY_LABELS.get(normalize_space(value).casefold())


def split_trailing_category(text: str) -> tuple[str, str | None]:
    for label in sorted(CATEGORY_LABELS, key=len, reverse=True):
        match = re.search(rf"\s+{re.escape(label)}:\s*$", text, re.IGNORECASE)
        if match:
            return text[: match.start()].rstrip(), CATEGORY_LABELS[label]
    return text.rstrip(), None


def normalize_measure_type(label: str) -> str:
    compact = re.sub(r"[^a-z]", "", label.casefold())
    mapping = {
        "hr": "hr",
        "s": "s",
        "hjres": "hjres",
        "sjres": "sjres",
        "hconres": "hconres",
        "hres": "hres",
    }
    if compact not in mapping:
        raise ValueError(f"Unsupported survey measure type: {label!r}")
    return mapping[compact]


def extract_pre_text(content: str) -> str:
    parser = PreTextExtractor()
    parser.feed(content)
    result = parser.text()
    if TABLE_START not in result or TABLE_END not in result:
        raise ValueError("Survey HTML does not contain the complete Table 1a boundary")
    return result


def parse_table_1a(
    content: str,
    spec: SurveySpec,
    expected_counts: dict[str, int] | None = None,
) -> list[dict[str, str]]:
    text = extract_pre_text(content)
    lines = text.splitlines()
    start_matches = [index for index, line in enumerate(lines) if TABLE_START in line]
    end_matches = [index for index, line in enumerate(lines) if TABLE_END in line]
    if len(start_matches) != 1 or len(end_matches) != 1:
        raise ValueError(
            f"Congress {spec.congress}: expected one Table 1a start and end, "
            f"found {len(start_matches)} and {len(end_matches)}"
        )
    start = start_matches[0]
    end = end_matches[0]
    if end <= start:
        raise ValueError(f"Congress {spec.congress}: Table 1a end precedes start")

    grants: list[dict[str, str]] = []
    active_category: str | None = None
    parsing_target_categories = True
    for source_line_number, line in enumerate(lines[start + 1 : end], start=start + 2):
        stripped = line.strip()
        if not stripped or set(stripped) == {"-"}:
            continue
        if stripped.casefold().startswith("resolution") and "measure" in stripped.casefold():
            continue

        if stripped.endswith(":") and not MEASURE_ROW_RE.match(line):
            category = normalize_category_label(stripped[:-1])
            if category:
                active_category = category
                continue
            if grants:
                parsing_target_categories = False
                active_category = None
                break
            raise ValueError(
                f"Congress {spec.congress} line {source_line_number}: "
                f"unexpected category before target rows: {stripped!r}"
            )

        match = MEASURE_ROW_RE.match(line)
        if match:
            if not parsing_target_categories or active_category is None:
                raise ValueError(
                    f"Congress {spec.congress} line {source_line_number}: "
                    "measure row has no recognized amendment-structure category"
                )
            measure_type = normalize_measure_type(match.group("measure_type"))
            measure_number = int(match.group("measure_number"))
            remainder = REPORT_ANNOTATION_RE.sub("", match.group("remainder"), count=1)
            title, trailing_category = split_trailing_category(remainder.strip())
            grants.append({
                "congress": str(spec.congress),
                "rule_number": str(int(match.group("rule"))),
                "measure_type": measure_type,
                "measure_number": str(measure_number),
                "title": title,
                "category": active_category,
                "survey_line_number": str(source_line_number),
            })
            if trailing_category:
                active_category = trailing_category
            continue

        if line[:1].isspace() and grants:
            continuation, trailing_category = split_trailing_category(stripped)
            if continuation:
                grants[-1]["title"] = normalize_space(
                    f"{grants[-1]['title']} {continuation}"
                )
            if trailing_category:
                active_category = trailing_category
            continue

        raise ValueError(
            f"Congress {spec.congress} line {source_line_number}: "
            f"unrecognized Table 1a content: {line!r}"
        )

    if not grants:
        raise ValueError(f"Congress {spec.congress}: no Table 1a grant rows parsed")
    for grant in grants:
        grant["title"] = normalize_space(grant["title"])
        if not grant["title"]:
            raise ValueError(
                f"Congress {spec.congress}: blank title for H. Res. "
                f"{grant['rule_number']} / {grant['measure_type']} {grant['measure_number']}"
            )

    actual_counts = Counter(grant["category"] for grant in grants)
    expected_counts = expected_counts or EXPECTED_CATEGORY_COUNTS[spec.congress]
    if dict(actual_counts) != {key: value for key, value in expected_counts.items() if value}:
        complete_actual = {key: actual_counts.get(key, 0) for key in CATEGORY_ORDER}
        raise ValueError(
            f"Congress {spec.congress}: Table 1a category counts changed: "
            f"expected {expected_counts}, found {complete_actual}"
        )

    identities = [
        (grant["rule_number"], grant["measure_type"], grant["measure_number"])
        for grant in grants
    ]
    duplicates = [identity for identity, count in Counter(identities).items() if count > 1]
    if duplicates:
        raise ValueError(
            f"Congress {spec.congress}: duplicate Table 1a rule-measure rows: {duplicates[:5]}"
        )
    return grants


def download_file(url: str, path: Path, retries: int, timeout: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                with temporary.open("wb") as handle:
                    while chunk := response.read(1024 * 1024):
                        handle.write(chunk)
            os.replace(temporary, path)
            return
        except (OSError, TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
            temporary.unlink(missing_ok=True)
            if attempt == retries:
                raise


def verify_survey_source(
    spec: SurveySpec,
    path: Path,
    allow_unpinned_source: bool,
) -> tuple[str, int, str]:
    digest = sha256_file(path)
    size = path.stat().st_size
    matched = digest == spec.sha256 and size == spec.size_bytes
    if not matched and not allow_unpinned_source:
        raise ValueError(
            f"{path} source pin changed: expected SHA-256 {spec.sha256} and "
            f"{spec.size_bytes} bytes; found {digest} and {size} bytes"
        )
    return digest, size, "matched" if matched else "changed_explicitly_allowed"


def load_hr_census() -> tuple[dict[int, list[dict[str, str]]], list[str], dict[int, str]]:
    rows_by_congress: dict[int, list[dict[str, str]]] = {}
    fieldnames: list[str] | None = None
    hashes: dict[int, str] = {}
    for congress in CONGRESSES:
        path = CENSUS_PATHS[congress]
        if not path.exists():
            raise FileNotFoundError(f"Missing complete bill census: {path}")
        hashes[congress] = sha256_file(path)
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"Missing CSV header in {path}")
            if fieldnames is None:
                fieldnames = list(reader.fieldnames)
            elif list(reader.fieldnames) != fieldnames:
                raise ValueError(f"Bill census fieldnames differ in {path}")
            rows = [
                dict(row)
                for row in reader
                if row.get("congress") == str(congress) and row.get("bill_type") == "hr"
            ]
        actual_ids = {row["bill_id"] for row in rows}
        if len(actual_ids) != len(rows):
            raise ValueError(f"Duplicate H.R. bill IDs in {path}")
        numbers = [int(row["bill_number"]) for row in rows]
        if any(number <= 0 for number in numbers) or len(set(numbers)) != len(numbers):
            raise ValueError(f"Congress {congress} H.R. census has invalid bill numbers")
        rows.sort(key=lambda row: int(row["bill_number"]))
        rows_by_congress[congress] = rows
    assert fieldnames is not None
    return rows_by_congress, fieldnames, hashes


def action_basis(action: Action, label: str) -> str:
    source = f"source_system:{action.source_code}" if action.source_code else "source_system:unknown"
    code = f"action_code:{action.code}" if action.code else f"action_text:{label}"
    return f"{code};{source}"


def earliest_action(
    actions: Iterable[Action],
    predicate,
) -> Action | None:
    matches = [(action.date, index, action) for index, action in enumerate(actions) if predicate(action)]
    if not matches:
        return None
    dated = [match for match in matches if match[0]]
    return (min(dated, key=lambda item: (item[0], item[1])) if dated else matches[0])[2]


def resolution_disposition(actions: list[Action], passed_house: bool) -> tuple[str, str, str]:
    if passed_house:
        amended = any(
            "as amended" in action.text.casefold()
            and ("agreed" in action.text.casefold() or "passed" in action.text.casefold())
            for action in actions
        )
        action = earliest_action(actions, lambda candidate: bool(house_passage_match(candidate)))
        return (
            "adopted_amended" if amended else "adopted",
            action.date if action else "",
            action_basis(action, "house_adoption") if action else "",
        )

    rejected = earliest_action(
        actions,
        lambda action: (
            "on agreeing to the resolution" in action.text.casefold()
            and any(word in action.text.casefold() for word in ("failed", "rejected"))
        )
        or "resolution rejected" in action.text.casefold(),
    )
    if rejected:
        return "rejected", rejected.date, action_basis(rejected, "resolution_rejected")
    tabled = earliest_action(
        actions,
        lambda action: action.code == "H1B000"
        or "is laid on the table" in action.text.casefold()
        or (
            "motion to table" in action.text.casefold()
            and any(word in action.text.casefold() for word in ("agreed", "passed"))
        ),
    )
    if tabled:
        return "tabled", tabled.date, action_basis(tabled, "resolution_tabled")
    return "not_adopted_or_no_house_disposition", "", ""


def parse_resolution_record(
    congress: int,
    rule_number: int,
    archive: zipfile.ZipFile,
) -> dict[str, str]:
    member_name = f"BILLSTATUS-{congress}hres{rule_number}.xml"
    try:
        xml_bytes = archive.read(member_name)
    except KeyError as error:
        raise ValueError(f"Missing rule-resolution source member {member_name}") from error
    root = ET.fromstring(xml_bytes)
    bill = at(root, "bill")
    if bill is None:
        raise ValueError(f"{member_name}: missing bill element")
    if (
        text_at(bill, "congress") != str(congress)
        or text_at(bill, "type").casefold() != "hres"
        or text_at(bill, "number") != str(rule_number)
    ):
        raise ValueError(f"{member_name}: source identity mismatch")
    actions = parse_actions(bill)
    reported = stage_from_actions(actions, committee_reported_match)
    passed = stage_from_actions(actions, house_passage_match)
    disposition, disposition_date, disposition_basis = resolution_disposition(
        actions, passed.reached
    )
    if passed.reached != disposition.startswith("adopted"):
        raise ValueError(f"{member_name}: passed-House flag conflicts with disposition")
    return {
        "rule_source_url": archive_url(congress, "hres").replace(
            archive_name(congress, "hres"), member_name
        ),
        "rule_source_xml_update_date": text_at(bill, "updateDate"),
        "rule_source_xml_sha256": sha256_bytes(xml_bytes),
        "rule_actions_sha256": canonical_actions_sha256(actions),
        "rule_reported": flag(reported.reached),
        "rule_reported_date": reported.date,
        "rule_reported_basis": reported.basis,
        "rule_passed_house": flag(passed.reached),
        "rule_passed_house_date": passed.date,
        "rule_passed_house_basis": passed.basis,
        "rule_disposition": disposition,
        "rule_disposition_date": disposition_date,
        "rule_disposition_basis": disposition_basis,
    }


def build_grant_rows(
    parsed_by_congress: dict[int, list[dict[str, str]]],
    survey_hashes: dict[int, str],
    hr_ids: set[str],
    archive_dir: Path,
    allow_unpinned_source: bool,
) -> tuple[list[dict[str, str]], dict[int, object]]:
    result: list[dict[str, str]] = []
    hres_archive_infos: dict[int, object] = {}
    for congress in CONGRESSES:
        path = archive_dir / archive_name(congress, "hres")
        info = archive_info(congress, "hres", path, allow_unpinned_source)
        hres_archive_infos[congress] = info
        rule_numbers = sorted({int(row["rule_number"]) for row in parsed_by_congress[congress]})
        with zipfile.ZipFile(path) as archive:
            resolution_records = {
                number: parse_resolution_record(congress, number, archive)
                for number in rule_numbers
            }
        spec = SURVEY_SPECS[congress]
        for index, parsed in enumerate(parsed_by_congress[congress], start=1):
            measure_id = f"{congress}-{parsed['measure_type']}-{parsed['measure_number']}"
            rule_id = f"{congress}-hres-{parsed['rule_number']}"
            resolution = resolution_records[int(parsed["rule_number"])]
            hr_linked = parsed["measure_type"] == "hr" and measure_id in hr_ids
            if parsed["measure_type"] == "hr" and not hr_linked:
                raise ValueError(f"Survey H.R. row does not map to complete census: {measure_id}")
            result.append({
                "grant_id": f"{congress}-rule-grant-{index:03d}",
                "congress": str(congress),
                "rule_resolution_id": rule_id,
                "rule_number": parsed["rule_number"],
                "covered_measure_id": measure_id,
                "covered_measure_type": parsed["measure_type"],
                "covered_measure_number": parsed["measure_number"],
                "covered_measure_title": parsed["title"],
                "amendment_structure": parsed["category"],
                "restrictive_structure": flag(parsed["category"] in {"structured", "closed"}),
                "survey_package": spec.package,
                "survey_table": "Table 1a - Types of Rules Granted (Consideration)",
                "survey_source_url": spec.url,
                "survey_source_sha256": survey_hashes[congress],
                "survey_row_number": parsed["survey_line_number"],
                "rule_source_url": resolution["rule_source_url"],
                "rule_source_xml_update_date": resolution["rule_source_xml_update_date"],
                "rule_source_xml_sha256": resolution["rule_source_xml_sha256"],
                "rule_actions_sha256": resolution["rule_actions_sha256"],
                "rule_reported": resolution["rule_reported"],
                "rule_reported_date": resolution["rule_reported_date"],
                "rule_reported_basis": resolution["rule_reported_basis"],
                "rule_passed_house": resolution["rule_passed_house"],
                "rule_passed_house_date": resolution["rule_passed_house_date"],
                "rule_passed_house_basis": resolution["rule_passed_house_basis"],
                "rule_disposition": resolution["rule_disposition"],
                "rule_disposition_date": resolution["rule_disposition_date"],
                "rule_disposition_basis": resolution["rule_disposition_basis"],
                "covered_measure_in_hr_census": flag(hr_linked),
                "linkage_status": "linked_hr_census" if hr_linked else "outside_hr_panel",
                "classification_version": CLASSIFICATION_VERSION,
                "claim_boundary": CLAIM_BOUNDARY,
            })
    return result, hres_archive_infos


def evidence_for_action(action: Action, label: str) -> str:
    text = normalize_space(action.text)
    if len(text) > 240:
        text = text[:237] + "..."
    return f"{action_basis(action, label)};text:{text}"


def extract_bill_procedure(actions: list[Action]) -> dict[str, str]:
    calendar_candidates: list[tuple[str, int, Action, re.Match[str]]] = []
    for index, action in enumerate(actions):
        match = CALENDAR_RE.search(action.text)
        if match and (action.action_type.casefold() == "calendars" or action.code):
            calendar_candidates.append((action.date, index, action, match))
    dated_calendars = [item for item in calendar_candidates if item[0]]
    calendar = (
        min(dated_calendars, key=lambda item: (item[0], item[1]))
        if dated_calendars
        else (calendar_candidates[0] if calendar_candidates else None)
    )

    suspension = earliest_action(
        actions,
        lambda action: action.action_type.casefold() == "floor"
        and any(phrase in action.text.casefold() for phrase in SUSPENSION_PHRASES),
    )
    other_path = earliest_action(
        actions,
        lambda action: action.action_type.casefold() == "floor"
        and any(phrase in action.text.casefold() for phrase in OTHER_PATH_PHRASES),
    )

    direct_rule_actions: list[tuple[Action, tuple[str, ...]]] = []
    for action in actions:
        ids = tuple(sorted(set(RULE_USE_RE.findall(action.text)), key=int))
        if ids:
            direct_rule_actions.append((action, ids))
    direct_rule_ids = sorted(
        {rule_id for _, ids in direct_rule_actions for rule_id in ids}, key=int
    )
    earliest_rule_action = earliest_action(
        (action for action, _ in direct_rule_actions), lambda action: True
    )

    offer_actions = 0
    disposition_actions = 0
    for action in actions:
        if action.action_type.casefold() != "floor" or action.source_code != "2":
            continue
        folded = action.text.casefold()
        if action.code in AMENDMENT_OFFER_CODES or re.search(
            r"\bamendment\b.*\boffered by\b", folded
        ):
            offer_actions += 1
        if re.search(r"\bon agreeing to\b.*\bamendment\b", folded) or (
            "amendment" in folded
            and any(term in folded for term in ("agreed to", "not agreed to", "withdrawn"))
        ):
            disposition_actions += 1

    return {
        "calendar_placed": flag(calendar is not None),
        "calendar_name": calendar[3].group(1).title() if calendar else "",
        "calendar_number": normalize_space(calendar[3].group(2) or "") if calendar else "",
        "calendar_date": calendar[2].date if calendar else "",
        "calendar_basis": evidence_for_action(calendar[2], "calendar_placement") if calendar else "",
        "suspension_path_evidence": flag(suspension is not None),
        "suspension_path_date": suspension.date if suspension else "",
        "suspension_path_basis": evidence_for_action(suspension, "suspension_path") if suspension else "",
        "other_floor_path_evidence": flag(other_path is not None),
        "other_floor_path_date": other_path.date if other_path else "",
        "other_floor_path_basis": evidence_for_action(other_path, "other_floor_path") if other_path else "",
        "direct_rule_ids": ";".join(f"hres-{number}" for number in direct_rule_ids),
        "direct_rule_action_count": str(len(direct_rule_actions)),
        "direct_rule_action_date": earliest_rule_action.date if earliest_rule_action else "",
        "direct_rule_action_basis": (
            evidence_for_action(earliest_rule_action, "direct_rule_action")
            if earliest_rule_action
            else ""
        ),
        "house_floor_amendment_offer_actions": str(offer_actions),
        "house_floor_amendment_disposition_actions": str(disposition_actions),
    }


def elapsed_days(start: str, end: str, label: str, bill_id: str) -> tuple[str, str]:
    if not start or not end:
        return "", ""
    value = (date.fromisoformat(end) - date.fromisoformat(start)).days
    if value < 0:
        return "", f"{label}_date_order:{bill_id}:{start}>{end}"
    return str(value), ""


def sorted_join(values: Iterable[str], *, numeric_suffix: bool = False) -> str:
    unique = set(value for value in values if value)
    if numeric_suffix:
        return ";".join(sorted(unique, key=lambda value: int(value.rsplit("-", 1)[-1])))
    return ";".join(sorted(unique))


def classify_floor_path(
    floor_considered: bool,
    adopted_rule_count: int,
    suspension: bool,
    other_detected: bool,
) -> str:
    if not floor_considered:
        return "not_floor_considered"
    if adopted_rule_count and suspension:
        return "mixed_special_rule_and_suspension"
    if adopted_rule_count:
        return "adopted_special_rule"
    if suspension:
        return "suspension"
    if other_detected:
        return "other_detected_floor_path"
    return "floor_path_not_identified"


def direct_rule_link_status(
    direct_ids: set[str],
    adopted_rule_ids: set[str],
) -> str:
    if not direct_ids and not adopted_rule_ids:
        return "no_direct_or_adopted_rule_link"
    if direct_ids == adopted_rule_ids:
        return "direct_and_adopted_rule_links_match"
    if adopted_rule_ids and adopted_rule_ids.issubset(direct_ids):
        return "direct_actions_include_all_adopted_rule_links"
    if adopted_rule_ids and not direct_ids:
        return "adopted_survey_rule_without_direct_action_id"
    if direct_ids and not adopted_rule_ids:
        return "direct_rule_action_without_adopted_table1a_link"
    return "direct_and_adopted_rule_links_differ"


def build_agenda_rows(
    census_rows_by_congress: dict[int, list[dict[str, str]]],
    census_fieldnames: list[str],
    grant_rows: list[dict[str, str]],
    archive_dir: Path,
    allow_unpinned_source: bool,
) -> tuple[list[dict[str, str]], dict[int, object]]:
    del census_fieldnames
    grants_by_measure: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in grant_rows:
        if row["covered_measure_type"] == "hr":
            grants_by_measure[row["covered_measure_id"]].append(row)

    result: list[dict[str, str]] = []
    hr_archive_infos: dict[int, object] = {}
    for congress in CONGRESSES:
        path = archive_dir / archive_name(congress, "hr")
        info = archive_info(congress, "hr", path, allow_unpinned_source)
        hr_archive_infos[congress] = info
        if len(census_rows_by_congress[congress]) != info.member_count:
            raise ValueError(
                f"Congress {congress} H.R. census/archive count mismatch: "
                f"{len(census_rows_by_congress[congress])} rows != {info.member_count} XML members"
            )
        with zipfile.ZipFile(path) as archive:
            for census in census_rows_by_congress[congress]:
                bill_id = census["bill_id"]
                member_name = f"BILLSTATUS-{congress}hr{census['bill_number']}.xml"
                try:
                    xml_bytes = archive.read(member_name)
                except KeyError as error:
                    raise ValueError(f"Missing H.R. source member {member_name}") from error
                xml_hash = sha256_bytes(xml_bytes)
                if xml_hash != census["source_xml_sha256"]:
                    raise ValueError(
                        f"{bill_id}: source XML hash differs from committed census "
                        f"({xml_hash} != {census['source_xml_sha256']})"
                    )
                root = ET.fromstring(xml_bytes)
                bill = at(root, "bill")
                if bill is None:
                    raise ValueError(f"{member_name}: missing bill element")
                actions = parse_actions(bill)
                actions_hash = canonical_actions_sha256(actions)
                if actions_hash != census["actions_sha256"]:
                    raise ValueError(
                        f"{bill_id}: direct action hash differs from committed census"
                    )
                procedure = extract_bill_procedure(actions)
                grants = grants_by_measure.get(bill_id, [])
                adopted = [row for row in grants if row["rule_passed_house"] == "1"]
                nonadopted = [row for row in grants if row["rule_passed_house"] != "1"]
                adopted_categories = [row["amendment_structure"] for row in adopted]
                category_set = sorted(set(adopted_categories), key=CATEGORY_ORDER.get)
                adopted_rule_ids = {row["rule_resolution_id"] for row in adopted}
                nonadopted_rule_ids = {row["rule_resolution_id"] for row in nonadopted}
                direct_numbers = {
                    token.removeprefix("hres-")
                    for token in procedure["direct_rule_ids"].split(";")
                    if token
                }
                direct_ids = {f"{congress}-hres-{number}" for number in direct_numbers}
                floor_considered = census["floor_considered"] == "1"
                suspension = procedure["suspension_path_evidence"] == "1"
                unlisted_rule_use = bool(direct_ids) and not adopted_rule_ids
                other_detected = (
                    procedure["other_floor_path_evidence"] == "1"
                    or unlisted_rule_use
                )
                floor_path = classify_floor_path(
                    floor_considered, len(adopted), suspension, other_detected
                )
                path_basis_parts: list[str] = []
                if adopted_rule_ids:
                    path_basis_parts.append(
                        "adopted_table1a_rules:" + sorted_join(adopted_rule_ids, numeric_suffix=True)
                    )
                if suspension:
                    path_basis_parts.append("direct_suspension_action")
                if other_detected:
                    if procedure["other_floor_path_evidence"] == "1":
                        path_basis_parts.append("direct_other_floor_path_action")
                    if unlisted_rule_use:
                        path_basis_parts.append(
                            "direct_rule_use_without_adopted_table1a_link"
                        )
                if floor_path == "floor_path_not_identified":
                    path_basis_parts.append("no_allowed_direct_path_evidence")

                interval_values: dict[str, str] = {}
                interval_anomalies: list[str] = []
                for field, start, end, label in (
                    (
                        "introduction_to_referral_days",
                        census["introduced_date"],
                        census["referred_to_committee_date"],
                        "introduction_to_referral",
                    ),
                    (
                        "referral_to_committee_advance_days",
                        census["referred_to_committee_date"],
                        census["committee_advanced_date"],
                        "referral_to_committee_advance",
                    ),
                    (
                        "committee_advance_to_floor_days",
                        census["committee_advanced_date"],
                        census["floor_considered_date"],
                        "committee_advance_to_floor",
                    ),
                    (
                        "introduction_to_floor_days",
                        census["introduced_date"],
                        census["floor_considered_date"],
                        "introduction_to_floor",
                    ),
                ):
                    value, anomaly = elapsed_days(start, end, label, bill_id)
                    interval_values[field] = value
                    if anomaly:
                        interval_anomalies.append(anomaly)

                row = dict(census)
                row.update(procedure)
                row.update({
                    "survey_rule_grant_count": str(len(grants)),
                    "adopted_rule_count": str(len(adopted)),
                    "nonadopted_rule_count": str(len(nonadopted)),
                    "adopted_rule_ids": sorted_join(adopted_rule_ids, numeric_suffix=True),
                    "nonadopted_rule_ids": sorted_join(nonadopted_rule_ids, numeric_suffix=True),
                    "adopted_rule_categories": ";".join(adopted_categories),
                    "adopted_rule_category_set": ";".join(category_set),
                    "most_restrictive_adopted_rule": max(
                        category_set, key=CATEGORY_ORDER.get
                    ) if category_set else "",
                    "restrictive_adopted_rule_count": str(
                        sum(category in {"structured", "closed"} for category in adopted_categories)
                    ),
                    "nonrestrictive_adopted_rule_count": str(
                        sum(category in {"open", "modified_open"} for category in adopted_categories)
                    ),
                    "mixed_adopted_rule_categories": flag(len(category_set) > 1),
                    "floor_path": floor_path,
                    "floor_path_basis": ";".join(path_basis_parts),
                    **interval_values,
                    "direct_rule_link_status": direct_rule_link_status(
                        direct_ids, adopted_rule_ids
                    ),
                    "agenda_integrity_status": (
                        "valid"
                        if not interval_anomalies
                        else "source_stage_order_anomaly:" + "|".join(interval_anomalies)
                    ),
                    "agenda_classification_version": CLASSIFICATION_VERSION,
                    "agenda_claim_boundary": CLAIM_BOUNDARY,
                })
                result.append(row)
    return result, hr_archive_infos


def write_csv_atomic(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="raise",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def metadata_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            values[key.strip()] = value.strip().strip("`")
    return values


def output_cache_matches(
    grant_output: Path,
    grant_metadata: Path,
    agenda_output: Path,
    agenda_metadata: Path,
    config_hash: str,
    builder_hash: str,
) -> bool:
    paths = (grant_output, grant_metadata, agenda_output, agenda_metadata)
    if not all(path.exists() for path in paths):
        return False
    values = metadata_values(agenda_metadata)
    return (
        values.get("configuration_sha256") == config_hash
        and values.get("builder_sha256") == builder_hash
        and values.get("grant_output_sha256") == sha256_file(grant_output)
        and values.get("agenda_output_sha256") == sha256_file(agenda_output)
        and metadata_values(grant_metadata).get("configuration_sha256") == config_hash
    )


def configuration_sha256(
    census_fieldnames: list[str],
    census_hashes: dict[int, str],
) -> str:
    payload = {
        "classificationVersion": CLASSIFICATION_VERSION,
        "specSha256": sha256_file(SPEC_PATH),
        "surveySources": {
            str(congress): {
                "url": spec.url,
                "sha256": spec.sha256,
                "bytes": spec.size_bytes,
                "expectedCounts": EXPECTED_CATEGORY_COUNTS[congress],
                "narrativeCounts": NARRATIVE_CATEGORY_COUNTS[congress],
            }
            for congress, spec in SURVEY_SPECS.items()
        },
        "censusSha256": {str(key): value for key, value in census_hashes.items()},
        "grantFieldnames": GRANT_FIELDNAMES,
        "agendaFieldnames": census_fieldnames + AGENDA_ADDITIONAL_FIELDNAMES,
    }
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())


def public_metadata_path(path: Path) -> str:
    """Keep local machine directories out of the public provenance record."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        # External cache locations are identified by filename, URL, and hash.
        return resolved.name


def archive_metadata_lines(kind: str, infos: dict[int, object]) -> list[str]:
    lines = [f"## {kind} Archives", ""]
    for congress in CONGRESSES:
        info = infos[congress]
        lines.extend([
            f"### Congress {congress}",
            "",
            f"- archive: `{public_metadata_path(info.path)}`",
            f"- source_url: {info.url}",
            f"- archive_sha256: `{info.sha256}`",
            f"- xml_members: {info.member_count}",
            f"- pin_status: `{info.pin_status}`",
            "",
        ])
    return lines


def metadata_content(
    grant_rows: list[dict[str, str]],
    agenda_rows: list[dict[str, str]],
    survey_statuses: dict[int, tuple[str, int, str]],
    census_hashes: dict[int, str],
    hres_infos: dict[int, object],
    hr_infos: dict[int, object],
    grant_output: Path,
    agenda_output: Path,
    config_hash: str,
    builder_hash: str,
) -> str:
    category_counts = Counter(row["amendment_structure"] for row in grant_rows)
    floor_paths = Counter(row["floor_path"] for row in agenda_rows)
    lines = [
        "# House Agenda-Control Source Panels",
        "",
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- classification_version: `{CLASSIFICATION_VERSION}`",
        f"- configuration_sha256: `{config_hash}`",
        f"- builder_sha256: `{builder_hash}`",
        f"- specification_sha256: `{sha256_file(SPEC_PATH)}`",
        f"- grant_output_sha256: `{sha256_file(grant_output)}`",
        f"- agenda_output_sha256: `{sha256_file(agenda_output)}`",
        f"- grant_rows: {len(grant_rows)}",
        f"- agenda_hr_rows: {len(agenda_rows)}",
        f"- adopted_grant_rows: {sum(row['rule_passed_house'] == '1' for row in grant_rows)}",
        f"- linked_hr_grant_rows: {sum(row['covered_measure_in_hr_census'] == '1' for row in grant_rows)}",
        f"- floor_considered_hr_rows: {sum(row['floor_considered'] == '1' for row in agenda_rows)}",
        f"- category_counts: `{json.dumps(dict(sorted(category_counts.items())), sort_keys=True)}`",
        f"- floor_path_counts: `{json.dumps(dict(sorted(floor_paths.items())), sort_keys=True)}`",
        f"- claim_boundary: {CLAIM_BOUNDARY}",
        "",
        "## Survey Sources",
        "",
    ]
    for congress in CONGRESSES:
        spec = SURVEY_SPECS[congress]
        digest, size, status = survey_statuses[congress]
        literal_counts = Counter(
            row["amendment_structure"]
            for row in grant_rows
            if row["congress"] == str(congress)
        )
        discrepancy = {
            category: literal_counts.get(category, 0)
            - NARRATIVE_CATEGORY_COUNTS[congress][category]
            for category in CATEGORY_ORDER
        }
        lines.extend([
            f"### Congress {congress}",
            "",
            f"- package: `{spec.package}`",
            f"- source_url: {spec.url}",
            f"- source_sha256: `{digest}`",
            f"- source_bytes: {size}",
            f"- pin_status: `{status}`",
            f"- narrative_category_counts: `{json.dumps(NARRATIVE_CATEGORY_COUNTS[congress], sort_keys=True)}`",
            f"- literal_table_category_counts: `{json.dumps({key: literal_counts.get(key, 0) for key in CATEGORY_ORDER}, sort_keys=True)}`",
            f"- literal_minus_narrative: `{json.dumps(discrepancy, sort_keys=True)}`",
            "",
        ])
    lines.extend(archive_metadata_lines("H. Res.", hres_infos))
    lines.extend(archive_metadata_lines("H.R.", hr_infos))
    lines.extend(["## Complete H.R. Census Inputs", ""])
    for congress in CONGRESSES:
        lines.append(
            f"- Congress {congress}: `{public_metadata_path(CENSUS_PATHS[congress])}` / `{census_hashes[congress]}`"
        )
    lines.extend([
        "",
        "## Method Boundary",
        "",
        "- Survey Table 1a supplies official amendment-structure labels. The labels are not inferred from bill outcomes.",
        "- H. Res. passage and disposition fields use only direct resolution actions.",
        "- H.R. calendar, suspension, other-path, rule-link, and amendment-action fields use only direct bill actions.",
        "- Nonconsideration by adjournment is an observed endpoint, not an inferred leadership rejection or capacity denial.",
        "- The panels are descriptive procedure evidence, not causal or model-validation evidence.",
        "",
    ])
    return "\n".join(lines)


def ensure_sources(
    survey_cache_dir: Path,
    archive_dir: Path,
    refresh: bool,
    offline: bool,
    allow_unpinned_source: bool,
    retries: int,
    timeout: float,
) -> tuple[dict[int, str], dict[int, tuple[str, int, str]]]:
    survey_contents: dict[int, str] = {}
    statuses: dict[int, tuple[str, int, str]] = {}
    for congress in CONGRESSES:
        spec = SURVEY_SPECS[congress]
        path = survey_cache_dir / spec.filename
        if refresh or not path.exists():
            if offline:
                raise SystemExit(f"Offline mode requires cached survey source {path}")
            print(f"Downloading {spec.url}")
            download_file(spec.url, path, max(1, retries), timeout)
        statuses[congress] = verify_survey_source(spec, path, allow_unpinned_source)
        survey_contents[congress] = path.read_text()

    for congress in CONGRESSES:
        for bill_type in ("hr", "hres"):
            path = archive_dir / archive_name(congress, bill_type)
            if refresh or not path.exists():
                if offline:
                    raise SystemExit(f"Offline mode requires cached archive {path}")
                print(f"Downloading {archive_url(congress, bill_type)}")
                download_archive(
                    archive_url(congress, bill_type),
                    path,
                    max(1, retries),
                    timeout,
                )
            archive_info(congress, bill_type, path, allow_unpinned_source)
    return survey_contents, statuses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--survey-cache-dir", type=Path, default=SURVEY_CACHE_DIR)
    parser.add_argument("--archive-dir", type=Path, default=ARCHIVE_DIR)
    parser.add_argument("--grant-output", type=Path, default=GRANT_OUTPUT)
    parser.add_argument("--grant-metadata-output", type=Path, default=GRANT_METADATA_OUTPUT)
    parser.add_argument("--agenda-output", type=Path, default=AGENDA_OUTPUT)
    parser.add_argument("--agenda-metadata-output", type=Path, default=AGENDA_METADATA_OUTPUT)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--allow-unpinned-source", action="store_true")
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    census_rows, census_fieldnames, census_hashes = load_hr_census()
    config_hash = configuration_sha256(census_fieldnames, census_hashes)
    builder_hash = sha256_file(Path(__file__).resolve())
    if (
        not args.refresh
        and not args.rebuild
        and output_cache_matches(
            args.grant_output,
            args.grant_metadata_output,
            args.agenda_output,
            args.agenda_metadata_output,
            config_hash,
            builder_hash,
        )
    ):
        print(f"Using matching output caches {args.grant_output} and {args.agenda_output}")
        return 0

    survey_contents, survey_statuses = ensure_sources(
        args.survey_cache_dir,
        args.archive_dir,
        args.refresh,
        args.offline,
        args.allow_unpinned_source,
        args.retries,
        args.timeout,
    )
    parsed_by_congress = {
        congress: parse_table_1a(survey_contents[congress], SURVEY_SPECS[congress])
        for congress in CONGRESSES
    }
    hr_ids = {
        row["bill_id"]
        for rows in census_rows.values()
        for row in rows
    }
    grant_rows, hres_infos = build_grant_rows(
        parsed_by_congress,
        {congress: survey_statuses[congress][0] for congress in CONGRESSES},
        hr_ids,
        args.archive_dir,
        args.allow_unpinned_source,
    )
    agenda_rows, hr_infos = build_agenda_rows(
        census_rows,
        census_fieldnames,
        grant_rows,
        args.archive_dir,
        args.allow_unpinned_source,
    )
    agenda_fieldnames = census_fieldnames + AGENDA_ADDITIONAL_FIELDNAMES
    write_csv_atomic(args.grant_output, GRANT_FIELDNAMES, grant_rows)
    write_csv_atomic(args.agenda_output, agenda_fieldnames, agenda_rows)
    metadata = metadata_content(
        grant_rows,
        agenda_rows,
        survey_statuses,
        census_hashes,
        hres_infos,
        hr_infos,
        args.grant_output,
        args.agenda_output,
        config_hash,
        builder_hash,
    )
    write_reproducible_metadata(args.grant_metadata_output, metadata)
    write_reproducible_metadata(args.agenda_metadata_output, metadata)
    print(f"Wrote {args.grant_output} ({len(grant_rows)} rows)")
    print(f"Wrote {args.agenda_output} ({len(agenda_rows)} rows)")
    print(f"Wrote {args.grant_metadata_output}")
    print(f"Wrote {args.agenda_metadata_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
