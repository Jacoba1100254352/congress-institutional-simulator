#!/usr/bin/env python3
"""Build a provenance-pinned bill lifecycle census from GovInfo BILLSTATUS.

The committed output is bill-level, but every action in each source XML record
is parsed, counted, and hashed.  Stage flags retain the action-code or
action-text basis used to classify them so downstream reports can audit the
operational definitions without redistributing the much larger XML archives.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

try:
    from .reproducible_metadata import write_reproducible_metadata
except ImportError:  # Direct script execution used by the Makefile.
    from reproducible_metadata import write_reproducible_metadata


BASE_URL = "https://www.govinfo.gov/bulkdata/BILLSTATUS"
DEFAULT_CONGRESS = 117
DEFAULT_BILL_TYPES = ("hr", "s")
DEFAULT_ARCHIVE_DIR = Path("out/validation-cache/govinfo-billstatus")
OUT_CSV = Path("data/validation/raw/govinfo_bill_census.csv")
OUT_METADATA = Path("data/validation/raw/govinfo_bill_census.metadata.md")
USER_AGENT = "congress-institutional-simulator-validation/0.3"
CLASSIFICATION_VERSION = "govinfo-bill-lifecycle-v3"

# These pins freeze the completed-Congress source bytes used for the committed
# publication artifact. A changed upstream archive must be reviewed explicitly.
KNOWN_ARCHIVE_PINS: dict[tuple[int, str], tuple[str, int]] = {
    (108, "hr"): (
        "c0d5d3a5cb2b080d9f1c6621bd303b7b6aa27c687c20ad9abd562cf284f9d326",
        5429,
    ),
    (108, "s"): (
        "52f1fea91a1ec4efb33a468562e627531db426a9ed2a1337b464350dfa2bdd43",
        3035,
    ),
    (109, "hr"): (
        "a65885dfb6b495d6384b85274c2c6c41b7480c9f77a30f1915e555575744230b",
        6432,
    ),
    (109, "s"): (
        "30b5c5145dd7f9e5e428aa1c02d13d421e7b7169b4841dac85f3fd572bbb3a8a",
        4122,
    ),
    (110, "hr"): (
        "f1f1bd5e418c6fa64761226356e789fd5fbc893e9b417729af4f7aed8fa7696e",
        7336,
    ),
    (110, "s"): (
        "6bc552c1081764245feeecfea165e49012857c36b0613a76e3729ca6a63f705c",
        3741,
    ),
    (111, "hr"): (
        "296ddd0d99ab420f56a3579e3895d8bab6f118c35ea31646bb466f746cab23b2",
        6562,
    ),
    (111, "s"): (
        "abe085e923d194befa5b7ef7a10ddeeabc0f183c58fed1eb4f973b0b756fcf5d",
        4059,
    ),
    (112, "hr"): (
        "c1c88f2bbea589b5147d487b134e2c3a0612f517715f441572fdd159a2e89f4b",
        6723,
    ),
    (112, "s"): (
        "9debaafe8c12586274432daf678ccd93bc5eb6fa83777a7c23bcd8257d64a218",
        3716,
    ),
    (113, "hr"): (
        "0182b94de536510f06828eb33cdfda80d2cf4efb5d8345bc2799c1d63592bbc5",
        5885,
    ),
    (113, "s"): (
        "674dd3747ff67662cb7ec2310a09b79d128b2f48ae51a47e6a248b2896b4770a",
        3020,
    ),
    (114, "hr"): (
        "a0e6f66a4b1f13ff4df026fd9c95692caa173b2f1c4510b9d7e0d6db5b784950",
        6526,
    ),
    (114, "s"): (
        "0ab8114fa49d48d056db920f6841b3d5b8c6a223ee432c7b42b869c078c40331",
        3548,
    ),
    (115, "hr"): (
        "493b4a6974af962abde28ce49ce0a2f084e4cce8d63fac7acb241fe91c6a45f3",
        7394,
    ),
    (115, "s"): (
        "e7fc54a07ddf6d796ffba8f83a98e6c33fa0dfeea3c521c6721d5ed98dd27e9a",
        3805,
    ),
    (116, "hr"): (
        "b3775e79914a9db29b3a8d55ae13638020c44822dcecb9e4517371e093d01dde",
        9062,
    ),
    (116, "s"): (
        "e876253f4e3c8b58b28278c8e6e3b901eff0c336b74dfc6e90834d9d3af98132",
        5086,
    ),
    (117, "hr"): (
        "658b2d280e4e7972c86bfd810ebff0c9bb61c115b242de8c8774034dea08de03",
        9709,
    ),
    (117, "s"): (
        "69561f19333de31afd2e288700757f3794ecffa35287b9fb86bb2d5d313a1294",
        5357,
    ),
    (118, "hr"): (
        "8e7ca7dab50a7b9b977f021ec1b3231f8fedf82c33494553857b892fadfdba98",
        10564,
    ),
    (118, "s"): (
        "269261c0989db3ced789680ee2202747df9a7298f1ac8d2b074d3356b06e399c",
        5649,
    ),
    (108, "hjres"): (
        "0f1f3cd96bce24e97ab1778ceb3c88921b5ce43b54e4b69450731c05dfdd1e23",
        115,
    ),
    (108, "sjres"): (
        "13c978a69636ef529d8c2b3877cc77f9226a9af900663118461547689e856540",
        42,
    ),
    (109, "hjres"): (
        "189d99ae3361ea283fcfb8842388a3851c7762027934c2477d2a863c04c2d46f",
        102,
    ),
    (109, "sjres"): (
        "fb89bd5d2e8d5a3a773a42298be50a2e7b04becb13518f2f9ecc46f492011549",
        41,
    ),
    (110, "hjres"): (
        "123692815274b0e43ea15dbf51b666118368d3eb42557de256060aeb06526b92",
        101,
    ),
    (110, "sjres"): (
        "711c77f0b2f8d4e07fbb82985752f864bfbd69d11fdd10589ea4bc9bf551b10e",
        46,
    ),
    (111, "hjres"): (
        "94823359899c6a77ec8805bd5b3f86bf36e71779b759f55cef13aebb111dbe41",
        107,
    ),
    (111, "sjres"): (
        "ee14cb09a375f91edbb4b1c51413d95265961c9bf21cc8d6b3dbed782bbed03a",
        42,
    ),
    (112, "hjres"): (
        "682165425079d6443741818cb09c869e6bf446c2c3090245e0d027ef910baf74",
        122,
    ),
    (112, "sjres"): (
        "604ee52dfd3f7100ec37f1c017797b5c8ac043c9f8185ab9a977e44ecd53f2a8",
        51,
    ),
    (113, "hjres"): (
        "8b3142f0592a111609f5faf390bff876ccd50a19d3c34a14b4a9245e54a3c1af",
        131,
    ),
    (113, "sjres"): (
        "afe08fc2748804ec630dc65a5e351cbb4e089c871dad999e8afe9b2a3352469a",
        47,
    ),
    (114, "hjres"): (
        "3c0ba49e4d90a18fba701d8193940204c07491c0a2f3d5c62f9cf9f6880764dc",
        108,
    ),
    (114, "sjres"): (
        "628bfce49748b2f40310dc761a219a6acddf7e6f784cc0f6482b618e295fca73",
        41,
    ),
    (115, "hjres"): (
        "9403bf92c16c5c6f6c40163839c828c4f5d8573797bca295d99fda0bb709d135",
        146,
    ),
    (115, "sjres"): (
        "1e048fd7508a8dd597d35dac323c1e5ff4c36d4fa0bbebbdc0d82b135c129f42",
        69,
    ),
    (116, "hjres"): (
        "9939bc21d8d8d40718d67e233b94d1075951314d673ffe02c5ba26788e1fdfc3",
        110,
    ),
    (116, "sjres"): (
        "f039d684b21421613bf4c980525e9a7c5759ab80db8083473da19b20ffdeea54",
        82,
    ),
    (117, "hjres"): (
        "55855f0441d0e691691e5cd8f12b46375314ab4994e9744575f5e4eb343810f4",
        106,
    ),
    (117, "sjres"): (
        "857969d43fb4fa63f608bafbe43c297be05b65ffbb5f2c4d7180e7d2cb2f72a9",
        70,
    ),
    (118, "hjres"): (
        "010db05723a7ae43db92455f0415d9ce5c4be3a89feac56bbbd2a78da4a2af83",
        230,
    ),
    (118, "sjres"): (
        "da94d59404d5eba1e35939ecc276d012fc56c2b1171a3467fc89456cf9c28569",
        122,
    ),
}


def claim_boundary(congress: int) -> str:
    return (
        "Complete GovInfo BILLSTATUS bill/action coverage for H.R. and S. measures "
        f"in Congress {congress}, with conservative operational lifecycle stages. "
        "This is descriptive legislative-flow evidence, not causal model validation, "
        "public-opinion evidence, public benefit, welfare, or institutional ranking."
    )

FIELDNAMES = [
    "bill_id",
    "congress",
    "bill_type",
    "bill_number",
    "origin_chamber",
    "title",
    "introduced",
    "introduced_date",
    "referred_to_committee",
    "referred_to_committee_date",
    "referred_to_committee_basis",
    "hearing_held",
    "hearing_held_date",
    "hearing_held_basis",
    "markup_held",
    "markup_held_date",
    "markup_held_basis",
    "committee_ordered_reported",
    "committee_ordered_reported_date",
    "committee_ordered_reported_basis",
    "committee_reported",
    "committee_reported_date",
    "committee_reported_basis",
    "committee_discharged",
    "committee_discharged_date",
    "committee_discharged_basis",
    "committee_advanced",
    "committee_advanced_date",
    "committee_advanced_basis",
    "floor_considered",
    "floor_considered_date",
    "floor_considered_basis",
    "passed_house",
    "passed_house_date",
    "passed_house_basis",
    "passed_senate",
    "passed_senate_date",
    "passed_senate_basis",
    "passed_origin_chamber",
    "passed_origin_chamber_date",
    "passed_origin_chamber_basis",
    "completed_congressional_passage",
    "completed_congressional_passage_date",
    "completed_congressional_passage_basis",
    "presented_to_president",
    "presented_to_president_date",
    "presented_to_president_basis",
    "vetoed",
    "vetoed_date",
    "vetoed_basis",
    "veto_overridden",
    "veto_overridden_date",
    "veto_overridden_basis",
    "enacted",
    "enacted_date",
    "enacted_basis",
    "law_type",
    "law_number",
    "policy_area",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "sponsor_district",
    "committees",
    "committee_system_codes",
    "actions_count",
    "committee_action_count",
    "floor_action_count",
    "president_action_count",
    "resolving_differences_action_count",
    "recorded_vote_count",
    "latest_action_date",
    "latest_action_text",
    "source_xml_update_date",
    "source_xml_sha256",
    "actions_sha256",
    "source_archive",
    "source_url",
    "classification_version",
    "integrity_status",
]

REFERRAL_CODES = {"2000", "11000", "H11100", "H11200", "H11210"}
HEARING_CODES = {"13100"}
MARKUP_CODES = {"13200"}
COMMITTEE_REPORTED_CODES = {
    "5000",
    "H12100",
    "H12200",
    "H12210",
    "14000",
    "14900",
}
COMMITTEE_DISCHARGED_CODES = {"5500", "H12300", "14500"}
FLOOR_CONSIDERATION_CODES = {
    "8000",
    "9000",
    "17000",
    "H30000",
    "H30300",
    "H35000",
    "H36200",
    "H36210",
    "H37100",
    "H37220",
    "H37300",
    "H38310",
    "H8A000",
}
HOUSE_PASSAGE_CODES = {"8000", "H37100", "H37300"}
SENATE_PASSAGE_CODES = {"17000"}
PRESENTED_CODES = {"E20000", "28000"}
HOUSE_VETO_OVERRIDE_CODES = {"32000"}
SENATE_VETO_OVERRIDE_CODES = {"34000"}
# E30000 is deliberately excluded. GovInfo uses it for both presidential
# signatures and vetoes in different source streams, so its text must disambiguate.
ENACTED_CODES = {"E40000", "36000", "41000"}
SPECIAL_RULE_CODES = {"H1L210", "H1L220"}

NEGATIVE_RESULT_PHRASES = (
    "failed of passage",
    "failed by",
    "not agreed to",
    "not invoked",
    "rejected",
    "withdrawn",
    "rendered moot",
    "fell when",
    "objection heard",
)


@dataclass(frozen=True)
class Action:
    date: str
    time: str
    text: str
    action_type: str
    code: str
    source_code: str
    source_name: str
    recorded_votes: tuple[str, ...]


@dataclass(frozen=True)
class Stage:
    reached: bool
    date: str = ""
    basis: str = ""


@dataclass(frozen=True)
class ArchiveInfo:
    bill_type: str
    path: Path
    url: str
    sha256: str
    byte_count: int
    member_count: int
    latest_member_timestamp: str
    pin_status: str


def normalize_space(value: str | None) -> str:
    return " ".join((value or "").split())


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(element: ET.Element | None, name: str) -> ET.Element | None:
    if element is None:
        return None
    for candidate in element:
        if local_name(candidate.tag) == name:
            return candidate
    return None


def children(element: ET.Element | None, name: str) -> list[ET.Element]:
    if element is None:
        return []
    return [candidate for candidate in element if local_name(candidate.tag) == name]


def at(element: ET.Element | None, *path: str) -> ET.Element | None:
    current = element
    for part in path:
        current = child(current, part)
        if current is None:
            return None
    return current


def text_at(element: ET.Element | None, *path: str) -> str:
    found = at(element, *path)
    return normalize_space(found.text if found is not None else "")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flag(value: bool) -> str:
    return "1" if value else "0"


def archive_name(congress: int, bill_type: str) -> str:
    return f"BILLSTATUS-{congress}-{bill_type}.zip"


def archive_url(congress: int, bill_type: str) -> str:
    return f"{BASE_URL}/{congress}/{bill_type}/{archive_name(congress, bill_type)}"


def source_xml_url(congress: str, bill_type: str, bill_number: str) -> str:
    return (
        f"{BASE_URL}/{congress}/{bill_type}/"
        f"BILLSTATUS-{congress}{bill_type}{bill_number}.xml"
    )


def parse_bill_types(value: str) -> tuple[str, ...]:
    result: list[str] = []
    for part in value.split(","):
        normalized = part.strip().lower()
        if not normalized:
            continue
        if not re.fullmatch(r"[a-z]+", normalized):
            raise argparse.ArgumentTypeError(f"Invalid bill type: {part}")
        if normalized not in result:
            result.append(normalized)
    if not result:
        raise argparse.ArgumentTypeError("At least one bill type is required.")
    return tuple(result)


def download_archive(url: str, path: Path, retries: int, timeout: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                with temporary.open("wb") as handle:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
            os.replace(temporary, path)
            return
        except (OSError, TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
            temporary.unlink(missing_ok=True)
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)


def archive_info(
    congress: int,
    bill_type: str,
    path: Path,
    allow_unpinned_source: bool,
) -> ArchiveInfo:
    digest = sha256_file(path)
    expected = KNOWN_ARCHIVE_PINS.get((congress, bill_type))
    pin_status = "unconfigured"
    if expected is not None:
        expected_digest, expected_members = expected
        if digest != expected_digest and not allow_unpinned_source:
            raise ValueError(
                f"{path} SHA-256 changed: expected {expected_digest}, found {digest}. "
                "Review the upstream change before using --allow-unpinned-source."
            )
        pin_status = "matched" if digest == expected_digest else "changed_explicitly_allowed"
    elif not allow_unpinned_source:
        raise ValueError(
            f"No publication pin is configured for Congress {congress} bill type {bill_type}; "
            "use --allow-unpinned-source for an exploratory build."
        )

    with zipfile.ZipFile(path) as archive:
        corrupt_member = archive.testzip()
        if corrupt_member:
            raise ValueError(f"Corrupt ZIP member in {path}: {corrupt_member}")
        members = [info for info in archive.infolist() if not info.is_dir()]
        xml_members = [info for info in members if info.filename.lower().endswith(".xml")]
        if len(xml_members) != len(members):
            unexpected = sorted(
                info.filename for info in members if not info.filename.lower().endswith(".xml")
            )
            raise ValueError(f"Unexpected non-XML archive members in {path}: {unexpected[:5]}")
        if not xml_members:
            raise ValueError(f"No XML records found in {path}")
        if expected is not None and digest == expected[0] and len(xml_members) != expected[1]:
            raise ValueError(
                f"Pinned archive {path} has {len(xml_members)} XML members; expected {expected[1]}."
            )
        latest = max(info.date_time for info in xml_members)
        latest_timestamp = datetime(*latest, tzinfo=timezone.utc).isoformat(timespec="seconds")

    return ArchiveInfo(
        bill_type=bill_type,
        path=path,
        url=archive_url(congress, bill_type),
        sha256=digest,
        byte_count=path.stat().st_size,
        member_count=len(xml_members),
        latest_member_timestamp=latest_timestamp,
        pin_status=pin_status,
    )


def recorded_vote_keys(action: ET.Element) -> tuple[str, ...]:
    values: set[str] = set()
    recorded_votes = at(action, "recordedVotes")
    if recorded_votes is None:
        return ()
    for vote in recorded_votes.iter():
        if local_name(vote.tag) not in {"recordedVote", "item"}:
            continue
        chamber = text_at(vote, "chamber")
        congress = text_at(vote, "congress")
        session = text_at(vote, "sessionNumber")
        roll = text_at(vote, "rollNumber")
        url = text_at(vote, "url")
        key = ":".join(part for part in (congress, session, chamber, roll) if part)
        if key or url:
            values.add(key or url)
    return tuple(sorted(values))


def parse_actions(bill: ET.Element) -> list[Action]:
    result: list[Action] = []
    for item in children(at(bill, "actions"), "item"):
        result.append(Action(
            date=text_at(item, "actionDate")[:10],
            time=text_at(item, "actionTime"),
            text=text_at(item, "text"),
            action_type=text_at(item, "type"),
            code=text_at(item, "actionCode").upper(),
            source_code=text_at(item, "sourceSystem", "code"),
            source_name=text_at(item, "sourceSystem", "name"),
            recorded_votes=recorded_vote_keys(item),
        ))
    return result


def canonical_actions_sha256(actions: Iterable[Action]) -> str:
    payload = [
        {
            "date": action.date,
            "time": action.time,
            "text": action.text,
            "type": action.action_type,
            "code": action.code,
            "sourceCode": action.source_code,
            "sourceName": action.source_name,
            "recordedVotes": list(action.recorded_votes),
        }
        for action in actions
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


Matcher = Callable[[Action], str]


def action_basis(action: Action, fallback: str, code_triggered: bool = False) -> str:
    if code_triggered and action.code:
        return f"action_code:{action.code}"
    return f"action_text:{fallback}"


def stage_from_actions(actions: list[Action], matcher: Matcher) -> Stage:
    matches: list[tuple[str, int, str]] = []
    for index, action in enumerate(actions):
        basis = matcher(action)
        if basis:
            matches.append((action.date, index, basis))
    if not matches:
        return Stage(False)
    dated = [match for match in matches if match[0]]
    selected = min(dated, key=lambda item: (item[0], item[1])) if dated else matches[0]
    return Stage(True, selected[0], selected[2])


def positive_result(text: str) -> bool:
    folded = text.casefold()
    return not any(phrase in folded for phrase in NEGATIVE_RESULT_PHRASES)


def referral_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in REFERRAL_CODES:
        return action_basis(action, "committee_referral", code_triggered=True)
    if action.action_type.casefold() != "introreferral":
        return ""
    if "referred" in folded and ("committee" in folded or "subcommittee" in folded):
        return action_basis(action, "committee_referral")
    return ""


def hearing_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in HEARING_CODES:
        return action_basis(action, "committee_hearing", code_triggered=True)
    if action.action_type.casefold() == "committee" and "hearing" in folded:
        return action_basis(action, "committee_hearing")
    return ""


def markup_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in MARKUP_CODES:
        return action_basis(action, "committee_markup", code_triggered=True)
    if action.action_type.casefold() == "committee" and "markup" in folded:
        return action_basis(action, "committee_markup")
    return ""


def committee_reported_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in COMMITTEE_REPORTED_CODES:
        return action_basis(action, "committee_reported", code_triggered=True)
    if action.code in SPECIAL_RULE_CODES:
        return ""
    committee_phrases = (
        "reported by the committee",
        "reported (amended) by the committee",
        "reported (original measure) by the committee",
        "reported to house",
        "reported to senate",
    )
    if action.action_type.casefold() == "committee" and any(
        phrase in folded for phrase in committee_phrases
    ):
        return action_basis(action, "committee_reported")
    if "filed written report" in folded:
        return action_basis(action, "committee_reported")
    return ""


def committee_ordered_reported_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in SPECIAL_RULE_CODES:
        return ""
    if action.action_type.casefold() == "committee" and "ordered to be reported" in folded:
        return action_basis(action, "committee_ordered_reported")
    return ""


def committee_discharged_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in COMMITTEE_DISCHARGED_CODES:
        return action_basis(action, "committee_discharged", code_triggered=True)
    if positive_result(action.text) and "committee" in folded and "discharged" in folded:
        return action_basis(action, "committee_discharged")
    return ""


def floor_considered_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in FLOOR_CONSIDERATION_CODES:
        return action_basis(action, "substantive_floor_consideration", code_triggered=True)
    if action.code in SPECIAL_RULE_CODES:
        return ""
    if action.action_type.casefold() == "resolvingdifferences":
        return action_basis(action, "resolving_differences")
    phrases = (
        "considered under suspension",
        "considered as unfinished business",
        "considered by senate",
        "measure laid before senate",
        "motion to proceed",
        "cloture on the measure",
        "cloture motion on the measure",
        "the house proceeded with",
        "debate - the house",
        "on passage",
        "final passage",
        "passed/agreed to in house",
        "passed/agreed to in senate",
        "passed senate",
        "failed of passage",
        "conference report",
    )
    if action.action_type.casefold() == "floor" and any(phrase in folded for phrase in phrases):
        return action_basis(action, "substantive_floor_consideration")
    return ""


def house_passage_match(action: Action) -> str:
    folded = action.text.casefold()
    if not positive_result(action.text):
        return ""
    if action.code in HOUSE_PASSAGE_CODES:
        return action_basis(action, "house_passage", code_triggered=True)
    if action.code in SPECIAL_RULE_CODES:
        return ""
    direct_phrases = (
        "passed/agreed to in house",
        "on passage passed",
        "following bills passed under suspension",
    )
    if any(phrase in folded for phrase in direct_phrases):
        return action_basis(action, "house_passage")
    if "motion to suspend the rules and pass" in folded and "agreed to" in folded:
        return action_basis(action, "house_passage")
    if (
        ("house agree to the senate amendment" in folded or "house concur" in folded)
        and "agreed to" in folded
    ):
        return action_basis(action, "house_final_agreement")
    return ""


def senate_passage_match(action: Action) -> str:
    folded = action.text.casefold()
    if not positive_result(action.text):
        return ""
    if action.code in SENATE_PASSAGE_CODES:
        return action_basis(action, "senate_passage", code_triggered=True)
    direct_phrases = (
        "passed/agreed to in senate",
        "passed senate",
        "passed without amendment by unanimous consent",
        "passed with an amendment by unanimous consent",
        "passed with amendments by unanimous consent",
        "passed without amendment by voice vote",
        "passed with an amendment by voice vote",
    )
    if any(phrase in folded for phrase in direct_phrases) and "senate" in folded:
        return action_basis(action, "senate_passage")
    if (
        ("senate agreed" in folded or "senate concur" in folded)
        and ("house amendment" in folded or "conference report" in folded)
    ):
        return action_basis(action, "senate_final_agreement")
    return ""


def presented_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in PRESENTED_CODES or "presented to president" in folded:
        return action_basis(
            action,
            "presented_to_president",
            code_triggered=action.code in PRESENTED_CODES,
        )
    if "cleared for white house" in folded:
        return action_basis(action, "cleared_for_white_house")
    return ""


def enacted_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in ENACTED_CODES:
        return action_basis(action, "enacted", code_triggered=True)
    if "became public law" in folded or "became private law" in folded:
        return action_basis(action, "enacted")
    if "signed by president" in folded:
        return action_basis(action, "signed_by_president")
    return ""


def vetoed_match(action: Action) -> str:
    folded = action.text.casefold()
    phrases = (
        "vetoed by president",
        "pocket veto",
        "veto message transmitted",
        "presidential veto message",
    )
    if any(phrase in folded for phrase in phrases):
        return action_basis(action, "presidential_veto")
    return ""


def house_veto_override_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in HOUSE_VETO_OVERRIDE_CODES:
        return action_basis(action, "house_veto_override", code_triggered=True)
    if positive_result(action.text) and "passed house over veto" in folded:
        return action_basis(action, "house_veto_override")
    return ""


def senate_veto_override_match(action: Action) -> str:
    folded = action.text.casefold()
    if action.code in SENATE_VETO_OVERRIDE_CODES:
        return action_basis(action, "senate_veto_override", code_triggered=True)
    if positive_result(action.text) and "passed senate over veto" in folded:
        return action_basis(action, "senate_veto_override")
    return ""


def stage_from_activity(
    committees: list[ET.Element],
    name_fragment: str,
    basis: str,
) -> Stage:
    matches: list[str] = []
    for committee in committees:
        for activity in children(at(committee, "activities"), "item"):
            if name_fragment in text_at(activity, "name").casefold():
                value = text_at(activity, "date")[:10]
                if value:
                    matches.append(value)
    return Stage(True, min(matches), basis) if matches else Stage(False)


def earliest_stage(*stages: Stage) -> Stage:
    reached = [stage for stage in stages if stage.reached]
    if not reached:
        return Stage(False)
    dated = [stage for stage in reached if stage.date]
    if dated:
        return min(dated, key=lambda stage: (stage.date, stage.basis))
    return reached[0]


def latest_stage(*stages: Stage) -> Stage:
    reached = [stage for stage in stages if stage.reached]
    if not reached:
        return Stage(False)
    dated = [stage for stage in reached if stage.date]
    if dated:
        return max(dated, key=lambda stage: (stage.date, stage.basis))
    return reached[-1]


def infer_stage(stage: Stage, source: Stage, label: str) -> Stage:
    if stage.reached or not source.reached:
        return stage
    return Stage(True, source.date, f"inferred_from:{label}")


def latest_action(actions: list[Action]) -> Action | None:
    dated = [(action.date, -index, action) for index, action in enumerate(actions) if action.date]
    if dated:
        return max(dated, key=lambda item: (item[0], item[1]))[2]
    return actions[0] if actions else None


def stage_columns(row: dict[str, str], prefix: str, stage: Stage) -> None:
    row[prefix] = flag(stage.reached)
    row[f"{prefix}_date"] = stage.date
    row[f"{prefix}_basis"] = stage.basis


def integrity_issues(row: dict[str, str]) -> list[str]:
    issues: list[str] = []
    required = (
        "bill_id",
        "congress",
        "bill_type",
        "bill_number",
        "origin_chamber",
        "introduced_date",
        "source_xml_sha256",
        "actions_sha256",
        "source_url",
    )
    for field in required:
        if not row.get(field, "").strip():
            issues.append(f"missing_{field}")

    if row.get("introduced") != "1":
        issues.append("not_introduced")
    if row.get("committee_advanced") == "1" and not (
        row.get("committee_ordered_reported") == "1"
        or row.get("committee_reported") == "1"
        or row.get("committee_discharged") == "1"
    ):
        issues.append("committee_advance_without_order_report_or_discharge")
    if row.get("passed_origin_chamber") == "1" and row.get("floor_considered") != "1":
        issues.append("origin_passage_without_floor_consideration")
    if row.get("completed_congressional_passage") == "1" and not (
        row.get("passed_house") == "1" and row.get("passed_senate") == "1"
    ):
        issues.append("completed_passage_without_both_chambers")
    if row.get("enacted") == "1" and row.get("completed_congressional_passage") != "1":
        issues.append("enacted_without_completed_passage")
    if row.get("veto_overridden") == "1" and row.get("vetoed") != "1":
        issues.append("override_without_veto")
    if row.get("veto_overridden") == "1" and row.get("enacted") != "1":
        issues.append("override_without_enactment")
    if (
        row.get("vetoed") == "1"
        and row.get("enacted") == "1"
        and row.get("veto_overridden") != "1"
    ):
        issues.append("vetoed_enactment_without_override")

    introduced_date = row.get("introduced_date", "")
    for field in (
        "referred_to_committee_date",
        "hearing_held_date",
        "markup_held_date",
        "committee_reported_date",
        "committee_ordered_reported_date",
        "committee_discharged_date",
        "floor_considered_date",
        "passed_house_date",
        "passed_senate_date",
        "passed_origin_chamber_date",
        "completed_congressional_passage_date",
        "presented_to_president_date",
        "vetoed_date",
        "veto_overridden_date",
        "enacted_date",
        "latest_action_date",
    ):
        value = row.get(field, "")
        if introduced_date and value and value < introduced_date:
            issues.append(f"{field}_before_introduction")
    if (
        row.get("completed_congressional_passage_date")
        and row.get("enacted_date")
        and row["enacted_date"] < row["completed_congressional_passage_date"]
    ):
        issues.append("enactment_before_completed_passage")
    if (
        row.get("vetoed_date")
        and row.get("veto_overridden_date")
        and row["veto_overridden_date"] < row["vetoed_date"]
    ):
        issues.append("override_before_veto")
    return sorted(set(issues))


def integrity_status(issues: list[str]) -> str:
    if not issues:
        return "valid"
    source_date_anomalies = [
        issue for issue in issues if issue.endswith("_before_introduction")
    ]
    fatal = [issue for issue in issues if issue not in source_date_anomalies]
    if fatal:
        return "invalid:" + "; ".join(issues)
    return "source_date_anomaly:" + "; ".join(source_date_anomalies)


def parse_bill_xml(
    xml_bytes: bytes,
    archive: ArchiveInfo,
    expected_congress: int,
    expected_bill_type: str,
    member_name: str,
) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    bill = at(root, "bill")
    if bill is None:
        raise ValueError(f"{member_name}: missing bill element")

    congress = text_at(bill, "congress")
    bill_type = (text_at(bill, "type") or text_at(bill, "billType")).lower()
    bill_number = text_at(bill, "number") or text_at(bill, "billNumber")
    if congress != str(expected_congress) or bill_type != expected_bill_type or not bill_number:
        raise ValueError(
            f"{member_name}: identifier mismatch; expected {expected_congress}-{expected_bill_type}, "
            f"found {congress}-{bill_type}-{bill_number}"
        )
    expected_member = f"BILLSTATUS-{congress}{bill_type}{bill_number}.xml"
    if Path(member_name).name != expected_member:
        raise ValueError(
            f"{member_name}: filename does not match XML identifier {expected_member}"
        )

    actions = parse_actions(bill)
    if not actions:
        raise ValueError(f"{member_name}: no direct bill actions found")
    committee_elements = children(at(bill, "committees"), "item")
    if not committee_elements:
        committee_elements = children(at(bill, "committees", "billCommittees"), "item")
    committee_names = sorted({text_at(item, "name") for item in committee_elements if text_at(item, "name")})
    committee_codes = sorted({text_at(item, "systemCode") for item in committee_elements if text_at(item, "systemCode")})

    introduced_date = text_at(bill, "introducedDate")[:10]
    introduced = Stage(bool(introduced_date), introduced_date, "bill.introducedDate")
    referred = stage_from_actions(actions, referral_match)
    if not referred.reached and committee_elements:
        referred = Stage(True, "", "bill.committees")

    hearing = earliest_stage(
        stage_from_actions(actions, hearing_match),
        stage_from_activity(committee_elements, "hearing", "bill.committees.activities:hearing"),
    )
    markup = earliest_stage(
        stage_from_actions(actions, markup_match),
        stage_from_activity(committee_elements, "markup", "bill.committees.activities:markup"),
    )
    committee_ordered_reported = stage_from_actions(
        actions, committee_ordered_reported_match
    )
    committee_reported = stage_from_actions(actions, committee_reported_match)
    if not committee_reported.reached and children(at(bill, "committeeReports"), "committeeReport"):
        committee_reported = Stage(True, "", "bill.committeeReports")
    committee_discharged = stage_from_actions(actions, committee_discharged_match)
    committee_advanced = earliest_stage(
        committee_ordered_reported, committee_reported, committee_discharged
    )

    floor_considered = stage_from_actions(actions, floor_considered_match)
    passed_house = stage_from_actions(actions, house_passage_match)
    passed_senate = stage_from_actions(actions, senate_passage_match)
    presented = stage_from_actions(actions, presented_match)
    enacted_action = stage_from_actions(actions, enacted_match)
    vetoed = stage_from_actions(actions, vetoed_match)
    house_veto_override = stage_from_actions(actions, house_veto_override_match)
    senate_veto_override = stage_from_actions(actions, senate_veto_override_match)
    veto_overridden = (
        latest_stage(house_veto_override, senate_veto_override)
        if house_veto_override.reached and senate_veto_override.reached
        else Stage(False)
    )

    law_elements = children(at(bill, "laws"), "item")
    law_types = sorted({text_at(item, "type") for item in law_elements if text_at(item, "type")})
    law_numbers = sorted({text_at(item, "number") for item in law_elements if text_at(item, "number")})
    enacted = enacted_action
    if law_elements:
        law_date = enacted_action.date
        enacted = Stage(True, law_date, "bill.laws")

    same_text_second_chamber = Stage(False)
    origin_chamber = text_at(bill, "originChamber")
    if passed_house.reached and passed_senate.reached:
        for action in actions:
            folded = action.text.casefold()
            if "without amendment" not in folded:
                continue
            if origin_chamber == "House" and senate_passage_match(action):
                same_text_second_chamber = Stage(
                    True,
                    action.date,
                    action_basis(action, "second_chamber_passed_without_amendment"),
                )
                break
            if origin_chamber == "Senate" and house_passage_match(action):
                same_text_second_chamber = Stage(
                    True,
                    action.date,
                    action_basis(action, "second_chamber_passed_without_amendment"),
                )
                break

    completed = earliest_stage(presented, same_text_second_chamber)
    completed = infer_stage(completed, enacted, "enactment")
    presented = infer_stage(presented, enacted, "enactment")
    passed_house = infer_stage(passed_house, completed, "completed_congressional_passage")
    passed_senate = infer_stage(passed_senate, completed, "completed_congressional_passage")

    passed_origin = passed_house if origin_chamber == "House" else passed_senate
    floor_considered = infer_stage(floor_considered, passed_origin, "origin_chamber_passage")
    floor_considered = infer_stage(floor_considered, completed, "completed_congressional_passage")

    latest = latest_action(actions)
    sponsor_elements = children(at(bill, "sponsors"), "item")
    sponsor = sponsor_elements[0] if sponsor_elements else None
    action_type_counts = Counter(action.action_type for action in actions)
    recorded_votes = {vote for action in actions for vote in action.recorded_votes}

    row: dict[str, str] = {
        "bill_id": f"{congress}-{bill_type}-{bill_number}",
        "congress": congress,
        "bill_type": bill_type,
        "bill_number": bill_number,
        "origin_chamber": origin_chamber,
        "title": text_at(bill, "title"),
        "introduced": flag(introduced.reached),
        "introduced_date": introduced.date,
        "law_type": "; ".join(law_types),
        "law_number": "; ".join(law_numbers),
        "policy_area": text_at(bill, "policyArea", "name") or "Unclassified",
        "sponsor_bioguide_id": text_at(sponsor, "bioguideId"),
        "sponsor_party": text_at(sponsor, "party") or "unknown",
        "sponsor_state": text_at(sponsor, "state"),
        "sponsor_district": text_at(sponsor, "district"),
        "committees": "; ".join(committee_names),
        "committee_system_codes": "; ".join(committee_codes),
        "actions_count": str(len(actions)),
        "committee_action_count": str(action_type_counts.get("Committee", 0)),
        "floor_action_count": str(action_type_counts.get("Floor", 0)),
        "president_action_count": str(
            action_type_counts.get("President", 0) + action_type_counts.get("BecameLaw", 0)
        ),
        "resolving_differences_action_count": str(action_type_counts.get("ResolvingDifferences", 0)),
        "recorded_vote_count": str(len(recorded_votes)),
        "latest_action_date": latest.date if latest else "",
        "latest_action_text": latest.text if latest else "",
        "source_xml_update_date": text_at(bill, "updateDate"),
        "source_xml_sha256": sha256_bytes(xml_bytes),
        "actions_sha256": canonical_actions_sha256(actions),
        "source_archive": archive.path.name,
        "source_url": source_xml_url(congress, bill_type, bill_number),
        "classification_version": CLASSIFICATION_VERSION,
        "integrity_status": "",
    }

    stage_columns(row, "referred_to_committee", referred)
    stage_columns(row, "hearing_held", hearing)
    stage_columns(row, "markup_held", markup)
    stage_columns(row, "committee_ordered_reported", committee_ordered_reported)
    stage_columns(row, "committee_reported", committee_reported)
    stage_columns(row, "committee_discharged", committee_discharged)
    stage_columns(row, "committee_advanced", committee_advanced)
    stage_columns(row, "floor_considered", floor_considered)
    stage_columns(row, "passed_house", passed_house)
    stage_columns(row, "passed_senate", passed_senate)
    stage_columns(row, "passed_origin_chamber", passed_origin)
    stage_columns(row, "completed_congressional_passage", completed)
    stage_columns(row, "presented_to_president", presented)
    stage_columns(row, "vetoed", vetoed)
    stage_columns(row, "veto_overridden", veto_overridden)
    stage_columns(row, "enacted", enacted)

    row["integrity_status"] = integrity_status(integrity_issues(row))
    return {field: row.get(field, "") for field in FIELDNAMES}


def bill_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    type_order = {"hr": 0, "s": 1}
    return (
        int(row["congress"]),
        type_order.get(row["bill_type"], 99),
        int(row["bill_number"]),
    )


def build_rows(
    archives: list[ArchiveInfo],
    congress: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for archive_info_item in archives:
        with zipfile.ZipFile(archive_info_item.path) as archive:
            members = sorted(
                info.filename
                for info in archive.infolist()
                if not info.is_dir() and info.filename.lower().endswith(".xml")
            )
            for member_name in members:
                row = parse_bill_xml(
                    archive.read(member_name),
                    archive_info_item,
                    congress,
                    archive_info_item.bill_type,
                    member_name,
                )
                if row["bill_id"] in seen:
                    raise ValueError(f"Duplicate bill identifier: {row['bill_id']}")
                seen.add(row["bill_id"])
                rows.append(row)
    rows.sort(key=bill_sort_key)
    validate_rows(rows, archives)
    return rows


def validate_rows(rows: list[dict[str, str]], archives: list[ArchiveInfo]) -> None:
    expected_rows = sum(archive.member_count for archive in archives)
    if len(rows) != expected_rows:
        raise ValueError(f"Parsed {len(rows)} rows from {expected_rows} XML members.")
    identifiers = [row["bill_id"] for row in rows]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Duplicate bill identifiers remain after parsing.")
    invalid = [
        row for row in rows if row.get("integrity_status", "").startswith("invalid:")
    ]
    if invalid:
        examples = ", ".join(
            f"{row['bill_id']}={row['integrity_status']}" for row in invalid[:8]
        )
        raise ValueError(f"Lifecycle integrity checks failed for {len(invalid)} rows: {examples}")


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def metric_count(rows: list[dict[str, str]], field: str) -> int:
    return sum(1 for row in rows if row.get(field) == "1")


def configuration_sha256(congress: int, bill_types: tuple[str, ...]) -> str:
    payload = {
        "classificationVersion": CLASSIFICATION_VERSION,
        "congress": congress,
        "billTypes": list(bill_types),
        "fieldnames": FIELDNAMES,
    }
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())


def builder_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def metadata_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line.startswith("- ") or ": " not in line:
            continue
        key, value = line[2:].split(": ", 1)
        result[key.strip()] = value.strip().strip("`")
    return result


def output_cache_matches(
    output: Path,
    metadata: Path,
    config_hash: str,
    code_hash: str,
) -> bool:
    if not output.exists() or not metadata.exists():
        return False
    values = metadata_values(metadata)
    expected_output_hash = values.get("output_sha256", "")
    return (
        values.get("configuration_sha256") == config_hash
        and values.get("builder_sha256") == code_hash
        and len(expected_output_hash) == 64
        and sha256_file(output) == expected_output_hash
    )


def metadata_content(
    rows: list[dict[str, str]],
    archives: list[ArchiveInfo],
    output: Path,
    congress: int,
    bill_types: tuple[str, ...],
    config_hash: str,
    code_hash: str,
) -> str:
    actions = sum(int(row["actions_count"]) for row in rows)
    laws = metric_count(rows, "enacted")
    public_laws = sum(1 for row in rows if "Public Law" in row["law_type"])
    private_laws = sum(1 for row in rows if "Private Law" in row["law_type"])
    output_hash = sha256_file(output)
    lines = [
        "# GovInfo Bill Lifecycle Census",
        "",
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- classification_version: `{CLASSIFICATION_VERSION}`",
        f"- configuration_sha256: `{config_hash}`",
        f"- builder_sha256: `{code_hash}`",
        f"- output_sha256: `{output_hash}`",
        f"- congress: {congress}",
        f"- bill_types: {','.join(bill_types)}",
        f"- rows: {len(rows)}",
        f"- parsed_action_records: {actions}",
        f"- enacted_rows: {laws}",
        f"- public_law_rows: {public_laws}",
        f"- private_law_rows: {private_laws}",
        f"- integrity_valid_rows: {sum(1 for row in rows if row['integrity_status'] == 'valid')}",
        f"- source_date_anomaly_rows: {sum(1 for row in rows if row['integrity_status'].startswith('source_date_anomaly:'))}",
        "",
        "## Source Archives",
        "",
        "| Bill type | URL | Bytes | XML members | SHA-256 | Latest member timestamp | Pin status |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for archive in archives:
        lines.append(
            f"| `{archive.bill_type}` | {archive.url} | {archive.byte_count} | "
            f"{archive.member_count} | `{archive.sha256}` | {archive.latest_member_timestamp} | "
            f"{archive.pin_status} |"
        )
    lines.extend([
        "",
        "## Lifecycle Coverage",
        "",
        "| Stage | Rows | Share |",
        "| --- | ---: | ---: |",
    ])
    for label, field in (
        ("Referred to committee", "referred_to_committee"),
        ("Committee hearing", "hearing_held"),
        ("Committee markup", "markup_held"),
        ("Committee ordered reported", "committee_ordered_reported"),
        ("Committee reported", "committee_reported"),
        ("Committee discharged", "committee_discharged"),
        ("Committee advanced", "committee_advanced"),
        ("Substantive floor consideration", "floor_considered"),
        ("Passed origin chamber", "passed_origin_chamber"),
        ("Completed congressional passage", "completed_congressional_passage"),
        ("Presented to President", "presented_to_president"),
        ("Vetoed", "vetoed"),
        ("Veto overridden", "veto_overridden"),
        ("Enacted", "enacted"),
    ):
        count = metric_count(rows, field)
        share = count / len(rows) if rows else 0.0
        lines.append(f"| {label} | {count} | {share:.6f} |")
    lines.extend([
        "",
        "## Operational Definitions",
        "",
        "- Scope is limited to H.R. and S. measures. Resolutions and joint resolutions are excluded.",
        "- Every direct `bill/actions/item` record is parsed. The committed bill row stores action counts and a canonical action hash; the source XML row stores a byte-level hash.",
        "- Referral, hearing, markup, reporting, discharge, floor consideration, chamber passage, presentment, veto, successful override, and enactment use documented action codes where available and conservative text rules where codes are absent.",
        "- `committee_ordered_reported` records a committee vote or action ordering the measure reported; `committee_reported` requires a report action or report citation. `committee_advanced` means ordered reported, reported, or discharged. None of these fields asserts a hearing, favorable recommendation, or committee influence.",
        "- `floor_considered` means substantive consideration or passage evidence. Administrative receipt, message, calendar, and special-rule actions alone do not satisfy it.",
        "- `completed_congressional_passage` requires presentment, final chamber agreement, a second-chamber passage without amendment, or enactment. Separate chamber passage flags can describe passage of nonidentical versions and are not alone treated as completed passage.",
        "- `veto_overridden` requires affirmative House and Senate override evidence. A vetoed enacted bill without both chamber stages fails the integrity audit.",
        "- Missing explicit intermediate records may be conservatively inferred from completed passage or enactment; each inferred field carries an `inferred_from:` basis and may have only the downstream date.",
        "- The GPO guide states that no complete authoritative action-code list exists and that action type values are processing categories. Therefore every stage remains an operational classification, not an official legal-status determination.",
        "",
        "Official format guide: https://github.com/usgpo/bill-status/blob/main/BILLSTATUS-XML_User_User-Guide.md",
        "",
        f"Claim boundary: {claim_boundary(congress)}",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--congress", type=int, default=DEFAULT_CONGRESS)
    parser.add_argument(
        "--bill-types",
        type=parse_bill_types,
        default=DEFAULT_BILL_TYPES,
        help="Comma-separated GovInfo bill type directories (default: hr,s).",
    )
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE_DIR)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata-output", type=Path, default=OUT_METADATA)
    parser.add_argument("--refresh", action="store_true", help="Redownload source archives before parsing.")
    parser.add_argument("--rebuild", action="store_true", help="Reparse archives even when committed output cache metadata matches.")
    parser.add_argument("--offline", action="store_true", help="Never download a missing source archive.")
    parser.add_argument(
        "--allow-unpinned-source",
        action="store_true",
        help="Allow an unconfigured or changed archive for exploratory review.",
    )
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    bill_types = tuple(args.bill_types)
    config_hash = configuration_sha256(args.congress, bill_types)
    code_hash = builder_sha256()
    if (
        not args.refresh
        and not args.rebuild
        and output_cache_matches(args.output, args.metadata_output, config_hash, code_hash)
    ):
        print(f"Using matching output cache {args.output}")
        return 0

    archives: list[ArchiveInfo] = []
    for bill_type in bill_types:
        path = args.archive_dir / archive_name(args.congress, bill_type)
        if args.refresh or not path.exists():
            if args.offline:
                raise SystemExit(f"Offline mode requires cached archive {path}")
            print(f"Downloading {archive_url(args.congress, bill_type)}")
            download_archive(
                archive_url(args.congress, bill_type),
                path,
                max(1, args.retries),
                args.timeout,
            )
        archives.append(
            archive_info(args.congress, bill_type, path, args.allow_unpinned_source)
        )

    rows = build_rows(archives, args.congress)
    write_csv(rows, args.output)
    metadata = metadata_content(
        rows,
        archives,
        args.output,
        args.congress,
        bill_types,
        config_hash,
        code_hash,
    )
    write_reproducible_metadata(args.metadata_output, metadata)
    print(f"Wrote {args.output} ({len(rows)} rows)")
    print(f"Wrote {args.metadata_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
