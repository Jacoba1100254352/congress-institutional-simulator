#!/usr/bin/env python3
"""Build a source-pinned panel of final chamber approval support."""

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
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    from .build_govinfo_bill_census_dataset import (
        CLASSIFICATION_VERSION,
        DEFAULT_ARCHIVE_DIR,
        archive_info,
        at,
        child,
        children,
        local_name,
        metadata_values,
        positive_result,
        sha256_bytes,
        sha256_file,
        text_at,
    )
    from .reproducible_metadata import write_reproducible_metadata
except ImportError:  # Direct script execution used by the Makefile.
    from build_govinfo_bill_census_dataset import (
        CLASSIFICATION_VERSION,
        DEFAULT_ARCHIVE_DIR,
        archive_info,
        at,
        child,
        children,
        local_name,
        metadata_values,
        positive_result,
        sha256_bytes,
        sha256_file,
        text_at,
    )
    from reproducible_metadata import write_reproducible_metadata


CLASSIFIER_VERSION = "govinfo-final-chamber-vote-v1"
DEFAULT_DECISION_PANELS = (
    Path("data/validation/raw/govinfo_executive_action_panel.csv"),
    Path("data/validation/raw/govinfo_joint_resolution_panel.csv"),
)
DEFAULT_VOTE_CACHE = Path("out/validation-cache/official-roll-calls")
OUT_CSV = Path("data/validation/raw/govinfo_final_chamber_vote_panel.csv")
OUT_METADATA = Path("data/validation/raw/govinfo_final_chamber_vote_panel.metadata.md")
USER_AGENT = "congress-institutional-simulator-validation/0.9"

HOUSE_ACTION_CODES = {"8000", "19500", "21000", "H37100", "H37300", "H41610", "H41941", "H42510"}
SENATE_ACTION_CODES = {"17000", "20500", "23000"}
PROCEDURAL_EXCLUSIONS = (
    "cloture",
    "motion to instruct",
    "motion to proceed",
    "motion to recommit",
    "motion to reconsider",
    "motion to table",
    "order of procedure",
    "point of order",
    "postponed proceedings",
    "question of consideration",
    "subject to postponement",
)

OUTPUT_FIELDS = [
    "bill_id",
    "congress",
    "bill_type",
    "measure_class",
    "bill_number",
    "origin_chamber",
    "president",
    "president_party",
    "government_control",
    "sponsor_party",
    "sponsor_same_party_as_president",
    "executive_outcome",
    "vetoed",
    "enacted",
    "chamber",
    "selection_status",
    "selection_category",
    "candidate_action_count",
    "action_date",
    "action_time",
    "action_code",
    "action_type",
    "action_source_name",
    "action_text",
    "roll_number",
    "session_number",
    "recorded_vote_date",
    "source_url",
    "official_source_status",
    "official_source_sha256",
    "official_source_congress",
    "official_source_chamber",
    "official_source_roll_number",
    "official_source_bill_id",
    "official_source_bill_match_status",
    "vote_question",
    "vote_result",
    "majority_requirement",
    "yea_count",
    "nay_count",
    "present_count",
    "not_voting_count",
    "member_vote_count",
    "participating_count",
    "support_share",
    "democratic_yea",
    "democratic_nay",
    "republican_yea",
    "republican_nay",
    "independent_yea",
    "independent_nay",
    "president_party_yea",
    "president_party_nay",
    "president_party_support_share",
    "opposition_party_yea",
    "opposition_party_nay",
    "opposition_party_support_share",
    "source_count_alignment",
    "decision_source_xml_sha256",
    "decision_actions_sha256",
    "classification_version",
    "selection_classifier_version",
    "integrity_status",
]


@dataclass(frozen=True)
class RecordedVoteReference:
    chamber: str
    congress: str
    session: str
    roll: str
    date: str
    url: str


@dataclass(frozen=True)
class SourceAction:
    index: int
    date: str
    time: str
    text: str
    action_type: str
    code: str
    source_name: str
    recorded_votes: tuple[RecordedVoteReference, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def normalized_int(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    return str(int(stripped))


def recorded_vote_references(item: ET.Element) -> tuple[RecordedVoteReference, ...]:
    result: dict[tuple[str, str, str, str], RecordedVoteReference] = {}
    container = at(item, "recordedVotes")
    if container is None:
        return ()
    for vote in container.iter():
        if local_name(vote.tag) not in {"recordedVote", "item"}:
            continue
        chamber = text_at(vote, "chamber")
        congress = text_at(vote, "congress")
        session = normalized_int(text_at(vote, "sessionNumber"))
        roll = normalized_int(text_at(vote, "rollNumber"))
        if chamber not in {"House", "Senate"} or not congress or not session or not roll:
            continue
        reference = RecordedVoteReference(
            chamber=chamber,
            congress=congress,
            session=session,
            roll=roll,
            date=text_at(vote, "date"),
            url=text_at(vote, "url"),
        )
        result[(chamber, congress, session, roll)] = reference
    return tuple(result[key] for key in sorted(result))


def parse_source_actions(xml_bytes: bytes) -> list[SourceAction]:
    bill = at(ET.fromstring(xml_bytes), "bill")
    require(bill is not None, "BILLSTATUS XML lacks a bill element")
    result = []
    for index, item in enumerate(children(at(bill, "actions"), "item")):
        result.append(
            SourceAction(
                index=index,
                date=text_at(item, "actionDate")[:10],
                time=text_at(item, "actionTime"),
                text=text_at(item, "text"),
                action_type=text_at(item, "type"),
                code=text_at(item, "actionCode").upper(),
                source_name=text_at(item, "sourceSystem", "name"),
                recorded_votes=recorded_vote_references(item),
            )
        )
    return result


def action_chamber(action: SourceAction) -> str:
    vote_chambers = {item.chamber for item in action.recorded_votes}
    if len(vote_chambers) == 1:
        return next(iter(vote_chambers))
    if action.code.startswith("H") or action.code in {"8000", "19500", "21000"}:
        return "House"
    if action.code in SENATE_ACTION_CODES:
        return "Senate"
    source = action.source_name.casefold()
    if source.startswith("house"):
        return "House"
    if source == "senate":
        return "Senate"
    folded = action.text.casefold()
    house = any(term in folded for term in ("in house", "house agree", "house concur", "passed house"))
    senate = any(term in folded for term in ("in senate", "senate agree", "senate concur", "passed senate"))
    if house != senate:
        return "House" if house else "Senate"
    return ""


def approval_category(action: SourceAction, chamber: str) -> str:
    if action_chamber(action) != chamber or action.action_type.casefold() == "veto":
        return ""
    folded = action.text.casefold()
    if not positive_result(action.text) or any(term in folded for term in PROCEDURAL_EXCLUSIONS):
        return ""
    if not any(term in folded for term in ("agreed to", "passed", "considered passed")):
        return ""

    if chamber == "House":
        if any(
            term in folded
            for term in (
                "conference report agreed to in house",
                "house agreed to conference report",
                "on agreeing to the conference report agreed to",
                "agree to the conference report agreed to",
            )
        ):
            return "conference_report"
        if (
            "senate amendment" in folded
            and any(
                term in folded
                for term in (
                    "house agree",
                    "house agreed",
                    "house concur",
                    "motion to agree",
                    "motion to concur",
                    "recede and concur",
                )
            )
        ):
            return "concurrence"
        if action.code in {"8000", "H37100", "H37300"} or any(
            term in folded
            for term in (
                "passed/agreed to in house",
                "on passage passed",
                "passed house",
                "following bills passed under suspension",
                "motion to suspend the rules and pass",
            )
        ):
            return "final_passage"
    else:
        if any(
            term in folded
            for term in (
                "conference report agreed to in senate",
                "senate agreed to conference report",
                "senate agreed to the conference report",
            )
        ):
            return "conference_report"
        if (
            "house amendment" in folded
            and any(
                term in folded
                for term in (
                    "senate agree",
                    "senate agreed",
                    "senate concur",
                    "recede and concur",
                )
            )
        ):
            return "concurrence"
        if action.code == "17000" or any(
            term in folded
            for term in (
                "passed/agreed to in senate",
                "passed senate",
                "resolution agreed to in senate",
            )
        ):
            return "final_passage"
    return ""


def select_approval_action(
    actions: list[SourceAction],
    chamber: str,
    presented_date: str,
) -> tuple[SourceAction | None, str, int]:
    candidates: list[tuple[tuple[str, str, int], SourceAction, str]] = []
    for action in actions:
        category = approval_category(action, chamber)
        if not category:
            continue
        if action.date and presented_date and action.date > presented_date:
            continue
        candidates.append(((action.date, action.time, -action.index), action, category))
    if not candidates:
        return None, "", 0
    _, selected, category = max(candidates, key=lambda item: item[0])
    return selected, category, len(candidates)


def canonical_vote_url(reference: RecordedVoteReference, action_date: str) -> str:
    roll = int(reference.roll)
    if reference.chamber == "House":
        source_match = re.fullmatch(
            r"https?://clerk\.house\.gov/evs/(\d{4})/roll0*(\d+)\.xml",
            reference.url,
            flags=re.IGNORECASE,
        )
        if source_match is not None and int(source_match.group(2)) == roll:
            year = source_match.group(1)
        else:
            year = (reference.date or action_date)[:4]
        require(re.fullmatch(r"\d{4}", year) is not None, "House vote reference lacks a year")
        return f"https://clerk.house.gov/evs/{year}/roll{roll:03d}.xml"
    return (
        "https://www.senate.gov/legislative/LIS/roll_call_votes/"
        f"vote{reference.congress}{reference.session}/"
        f"vote_{reference.congress}_{reference.session}_{roll:05d}.xml"
    )


def vote_cache_path(cache: Path, reference: RecordedVoteReference) -> Path:
    return cache / (
        f"{reference.congress}-{reference.chamber.lower()}-"
        f"{reference.session}-{int(reference.roll)}.xml"
    )


def download(url: str, path: Path, retries: int, timeout: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                temporary.write_bytes(response.read())
            os.replace(temporary, path)
            return
        except (OSError, TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
            temporary.unlink(missing_ok=True)
            if attempt == retries:
                raise
            time.sleep(1.5 * attempt)


def normalize_party(value: str) -> str:
    folded = value.strip().casefold()
    if folded in {"d", "democrat", "democratic"}:
        return "D"
    if folded in {"r", "republican"}:
        return "R"
    if folded in {"i", "id", "independent", "independent democrat"}:
        return "I"
    return value.strip().upper() or "U"


def normalize_vote(value: str) -> str:
    folded = " ".join(value.split()).casefold()
    if folded in {"aye", "yea", "yes"}:
        return "yea"
    if folded in {"nay", "no"}:
        return "nay"
    if folded in {"present", "announced present", "present, giving live pair"}:
        return "present"
    if folded in {"absent", "not voting", "not voting/paired"}:
        return "not_voting"
    return folded.replace(" ", "_") or "unknown"


def normalize_bill_id(raw: str, congress: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9]", "", raw).upper()
    for prefix, bill_type in (("HJRES", "hjres"), ("SJRES", "sjres"), ("HR", "hr"), ("S", "s")):
        if compact.startswith(prefix):
            number = compact[len(prefix):]
            if number.isdigit():
                return f"{congress}-{bill_type}-{int(number)}"
    return ""


def bill_ids_in_text(raw: str, congress: str) -> set[str]:
    patterns = (
        (r"\bH\s*\.?\s*J\s*\.?\s*Res\s*\.?\s*(\d+)\b", "hjres"),
        (r"\bS\s*\.?\s*J\s*\.?\s*Res\s*\.?\s*(\d+)\b", "sjres"),
        (r"\bH\s*\.?\s*R\s*\.?\s*(\d+)\b", "hr"),
        (r"\bS\s*\.\s*(\d+)\b", "s"),
    )
    return {
        f"{congress}-{bill_type}-{int(match.group(1))}"
        for pattern, bill_type in patterns
        for match in re.finditer(pattern, raw, flags=re.IGNORECASE)
    }


def official_bill_match_status(metrics: dict[str, str], bill_id: str, congress: str) -> str:
    if metrics["official_source_bill_id"] == bill_id:
        return "matched"
    if bill_id in bill_ids_in_text(metrics["vote_question"], congress):
        return "matched_grouped_question"
    if not metrics["official_source_bill_id"]:
        return "missing_official_bill_id"
    return "mismatch"


def integer_text(element: ET.Element | None, *path: str) -> int | None:
    value = text_at(element, *path)
    return int(value) if value.isdigit() else None


def metric_row(
    *,
    congress: str,
    chamber: str,
    roll: str,
    official_bill_id: str,
    question: str,
    result: str,
    majority: str,
    party_votes: Counter[tuple[str, str]],
    vote_counts: Counter[str],
    source_counts: dict[str, int | None],
) -> dict[str, str]:
    yea = vote_counts["yea"]
    nay = vote_counts["nay"]
    present = vote_counts["present"]
    not_voting = vote_counts["not_voting"]
    member_count = sum(vote_counts.values())
    participating = yea + nay
    source_alignment = "aligned"
    for key in ("yea", "nay"):
        if source_counts.get(key) is not None and source_counts[key] != vote_counts[key]:
            source_alignment = "source_member_count_difference"
    return {
        "official_source_congress": congress,
        "official_source_chamber": chamber,
        "official_source_roll_number": normalized_int(roll),
        "official_source_bill_id": official_bill_id,
        "vote_question": question,
        "vote_result": result,
        "majority_requirement": majority,
        "yea_count": str(yea),
        "nay_count": str(nay),
        "present_count": str(present),
        "not_voting_count": str(not_voting),
        "member_vote_count": str(member_count),
        "participating_count": str(participating),
        "support_share": f"{yea / participating:.6f}" if participating else "",
        "democratic_yea": str(party_votes[("D", "yea")]),
        "democratic_nay": str(party_votes[("D", "nay")]),
        "republican_yea": str(party_votes[("R", "yea")]),
        "republican_nay": str(party_votes[("R", "nay")]),
        "independent_yea": str(party_votes[("I", "yea")]),
        "independent_nay": str(party_votes[("I", "nay")]),
        "source_count_alignment": source_alignment,
    }


def parse_house_vote(xml_bytes: bytes) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    require(local_name(root.tag) == "rollcall-vote", "House source is not rollcall-vote XML")
    metadata = child(root, "vote-metadata")
    require(metadata is not None, "House vote XML lacks metadata")
    congress = text_at(metadata, "congress")
    roll = text_at(metadata, "rollcall-num")
    party_votes: Counter[tuple[str, str]] = Counter()
    vote_counts: Counter[str] = Counter()
    vote_data = child(root, "vote-data")
    for item in children(vote_data, "recorded-vote"):
        legislator = child(item, "legislator")
        party = normalize_party(legislator.attrib.get("party", "") if legislator is not None else "")
        vote = normalize_vote(text_at(item, "vote"))
        vote_counts[vote] += 1
        party_votes[(party, vote)] += 1
    totals = at(metadata, "vote-totals", "totals-by-vote")
    source_counts = {
        "yea": integer_text(totals, "yea-total"),
        "nay": integer_text(totals, "nay-total"),
    }
    return metric_row(
        congress=congress,
        chamber="House",
        roll=roll,
        official_bill_id=normalize_bill_id(text_at(metadata, "legis-num"), congress),
        question=text_at(metadata, "vote-question"),
        result=text_at(metadata, "vote-result"),
        majority=text_at(metadata, "vote-type"),
        party_votes=party_votes,
        vote_counts=vote_counts,
        source_counts=source_counts,
    )


def parse_senate_vote(xml_bytes: bytes) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    require(local_name(root.tag) == "roll_call_vote", "Senate source is not roll_call_vote XML")
    congress = text_at(root, "congress")
    roll = text_at(root, "vote_number")
    party_votes: Counter[tuple[str, str]] = Counter()
    vote_counts: Counter[str] = Counter()
    for member in children(at(root, "members"), "member"):
        party = normalize_party(text_at(member, "party"))
        vote = normalize_vote(text_at(member, "vote_cast"))
        vote_counts[vote] += 1
        party_votes[(party, vote)] += 1
    source_counts = {
        "yea": integer_text(at(root, "count"), "yeas"),
        "nay": integer_text(at(root, "count"), "nays"),
    }
    document = child(root, "document")
    bill_text = f"{text_at(document, 'document_type')} {text_at(document, 'document_number')}"
    return metric_row(
        congress=congress,
        chamber="Senate",
        roll=roll,
        official_bill_id=normalize_bill_id(bill_text, congress),
        question=text_at(root, "vote_question_text") or text_at(root, "question"),
        result=text_at(root, "vote_result"),
        majority=text_at(root, "majority_requirement"),
        party_votes=party_votes,
        vote_counts=vote_counts,
        source_counts=source_counts,
    )


def affirmative_result(value: str) -> bool:
    folded = value.casefold()
    return (
        any(term in folded for term in ("agreed", "passed", "approved"))
        and not any(term in folded for term in ("failed", "not agreed", "rejected"))
    )


def base_row(decision: dict[str, str], chamber: str) -> dict[str, str]:
    result = {field: "" for field in OUTPUT_FIELDS}
    for field in (
        "bill_id",
        "congress",
        "bill_type",
        "bill_number",
        "origin_chamber",
        "president",
        "president_party",
        "government_control",
        "sponsor_party",
        "sponsor_same_party_as_president",
        "executive_outcome",
        "vetoed",
        "enacted",
    ):
        result[field] = decision.get(field, "")
    result.update(
        {
            "measure_class": "joint_resolution" if decision["bill_type"] in {"hjres", "sjres"} else "bill",
            "chamber": chamber,
            "decision_source_xml_sha256": decision["source_xml_sha256"],
            "decision_actions_sha256": decision["actions_sha256"],
            "classification_version": decision["classification_version"],
            "selection_classifier_version": CLASSIFIER_VERSION,
        }
    )
    return result


def add_party_context(row: dict[str, str]) -> None:
    president_party = row["president_party"]
    opposition_party = "R" if president_party == "D" else "D"
    for prefix, party in (("president_party", president_party), ("opposition_party", opposition_party)):
        name = "democratic" if party == "D" else "republican"
        yea = int(row[f"{name}_yea"])
        nay = int(row[f"{name}_nay"])
        row[f"{prefix}_yea"] = str(yea)
        row[f"{prefix}_nay"] = str(nay)
        row[f"{prefix}_support_share"] = f"{yea / (yea + nay):.6f}" if yea + nay else ""


def decision_rows(paths: tuple[Path, ...]) -> list[dict[str, str]]:
    rows = [row for path in paths for row in read_csv(path)]
    require(rows, "Decision panels are empty")
    require(len({row["bill_id"] for row in rows}) == len(rows), "Decision panel bill IDs overlap")
    require(
        {row["bill_type"] for row in rows} == {"hr", "s", "hjres", "sjres"},
        "Decision panels do not contain all four scoped measure types",
    )
    return sorted(rows, key=lambda row: (int(row["congress"]), row["bill_type"], int(row["bill_number"])))


def build_rows(
    decisions: list[dict[str, str]],
    archive_dir: Path,
    vote_cache: Path,
    refresh: bool,
    offline: bool,
    retries: int,
    timeout: float,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in decisions:
        grouped[row["source_archive"]].append(row)
    output: list[dict[str, str]] = []
    source_manifest: dict[str, dict[str, str]] = {}
    processed = 0
    for archive_name in sorted(grouped):
        cohort = grouped[archive_name]
        congress = int(cohort[0]["congress"])
        bill_type = cohort[0]["bill_type"]
        archive_path = archive_dir / archive_name
        source = archive_info(congress, bill_type, archive_path, False)
        with zipfile.ZipFile(archive_path) as archive:
            for decision in cohort:
                member_name = f"BILLSTATUS-{decision['congress']}{decision['bill_type']}{decision['bill_number']}.xml"
                xml_bytes = archive.read(member_name)
                require(
                    sha256_bytes(xml_bytes) == decision["source_xml_sha256"],
                    f"{decision['bill_id']} source XML differs from decision panel",
                )
                actions = parse_source_actions(xml_bytes)
                for chamber in ("House", "Senate"):
                    row = base_row(decision, chamber)
                    selected, category, candidate_count = select_approval_action(
                        actions,
                        chamber,
                        decision["presented_to_president_date"],
                    )
                    require(selected is not None, f"{decision['bill_id']} lacks a {chamber} final approval action")
                    row.update(
                        {
                            "selection_category": category,
                            "candidate_action_count": str(candidate_count),
                            "action_date": selected.date,
                            "action_time": selected.time,
                            "action_code": selected.code,
                            "action_type": selected.action_type,
                            "action_source_name": selected.source_name,
                            "action_text": selected.text,
                        }
                    )
                    references = [item for item in selected.recorded_votes if item.chamber == chamber]
                    if not references:
                        row.update(
                            {
                                "selection_status": "final_approval_without_recorded_vote",
                                "official_source_status": "not_applicable_no_recorded_vote",
                                "integrity_status": "valid_no_recorded_final_approval_vote",
                            }
                        )
                        output.append(row)
                        continue
                    require(
                        len(references) == 1,
                        f"{decision['bill_id']} {chamber} final action has multiple recorded votes",
                    )
                    reference = references[0]
                    url = canonical_vote_url(reference, selected.date)
                    cache_path = vote_cache_path(vote_cache, reference)
                    if refresh or not cache_path.exists():
                        if offline:
                            raise SystemExit(f"Offline mode requires cached official vote {cache_path}")
                        download(url, cache_path, max(1, retries), timeout)
                    vote_bytes = cache_path.read_bytes()
                    metrics = parse_house_vote(vote_bytes) if chamber == "House" else parse_senate_vote(vote_bytes)
                    require(metrics["official_source_congress"] == decision["congress"], f"{url} Congress mismatch")
                    require(metrics["official_source_chamber"] == chamber, f"{url} chamber mismatch")
                    require(metrics["official_source_roll_number"] == reference.roll, f"{url} roll mismatch")
                    require(affirmative_result(metrics["vote_result"]), f"{url} is not an affirmative final vote")
                    bill_match = official_bill_match_status(
                        metrics,
                        decision["bill_id"],
                        decision["congress"],
                    )
                    row.update(metrics)
                    row.update(
                        {
                            "selection_status": "official_roll_call_selected",
                            "roll_number": reference.roll,
                            "session_number": reference.session,
                            "recorded_vote_date": reference.date,
                            "source_url": url,
                            "official_source_status": (
                                "official_house_clerk_xml" if chamber == "House" else "official_senate_lis_xml"
                            ),
                            "official_source_sha256": sha256_bytes(vote_bytes),
                            "official_source_bill_match_status": bill_match,
                            "integrity_status": (
                                "valid_official_roll_call"
                                if bill_match in {"matched", "matched_grouped_question"}
                                and metrics["source_count_alignment"] == "aligned"
                                else "review_official_source_metadata"
                            ),
                        }
                    )
                    add_party_context(row)
                    source_manifest[url] = {
                        "url": url,
                        "sha256": row["official_source_sha256"],
                        "bytes": str(len(vote_bytes)),
                        "chamber": chamber,
                    }
                    output.append(row)
                processed += 1
                if processed % 100 == 0:
                    print(f"Processed {processed} / {len(decisions)} presented measures")
    require(len(output) == 2 * len(decisions), "Final-vote panel does not contain two chamber rows per decision")
    output.sort(key=lambda row: (int(row["congress"]), row["bill_type"], int(row["bill_number"]), row["chamber"]))
    manifest = [source_manifest[url] for url in sorted(source_manifest)]
    return output, manifest


def configuration_sha256(paths: tuple[Path, ...], lifecycle_builder: Path) -> str:
    payload = {
        "classifierVersion": CLASSIFIER_VERSION,
        "decisionPanels": {str(path): sha256_file(path) for path in paths},
        "lifecycleBuilderSha256": sha256_file(lifecycle_builder),
        "outputFields": OUTPUT_FIELDS,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def output_cache_matches(output: Path, metadata: Path, config_hash: str, code_hash: str) -> bool:
    if not output.exists() or not metadata.exists():
        return False
    values = metadata_values(metadata)
    return (
        values.get("configuration_sha256") == config_hash
        and values.get("builder_sha256") == code_hash
        and values.get("output_sha256") == sha256_file(output)
    )


def metadata_content(
    rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    source_manifest: list[dict[str, str]],
    output: Path,
    decision_panels: tuple[Path, ...],
    config_hash: str,
    code_hash: str,
    lifecycle_builder: Path,
) -> str:
    status_counts = Counter(row["selection_status"] for row in rows)
    class_status = Counter((row["measure_class"], row["selection_status"]) for row in rows)
    official_urls_hash = hashlib.sha256(
        json.dumps(source_manifest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    by_bill = defaultdict(list)
    for row in rows:
        by_bill[row["bill_id"]].append(row)
    both_chambers = sum(
        len(items) == 2 and all(item["selection_status"] == "official_roll_call_selected" for item in items)
        for items in by_bill.values()
    )
    lines = [
        "# GovInfo Final Chamber-Vote Panel",
        "",
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- selection_classifier_version: `{CLASSIFIER_VERSION}`",
        f"- lifecycle_classification_version: `{CLASSIFICATION_VERSION}`",
        f"- configuration_sha256: `{config_hash}`",
        f"- builder_sha256: `{code_hash}`",
        f"- lifecycle_builder_sha256: `{sha256_file(lifecycle_builder)}`",
        f"- output_sha256: `{sha256_file(output)}`",
        f"- official_source_manifest_sha256: `{official_urls_hash}`",
        f"- decision_panel_sha256: `{hashlib.sha256('|'.join(sha256_file(path) for path in decision_panels).encode()).hexdigest()}`",
        f"- presented_measures: {len(decisions)}",
        f"- chamber_rows: {len(rows)}",
        f"- official_roll_call_rows: {status_counts['official_roll_call_selected']}",
        f"- nonrecorded_final_approval_rows: {status_counts['final_approval_without_recorded_vote']}",
        f"- measures_with_both_final_roll_calls: {both_chambers}",
        f"- unique_official_vote_sources: {len(source_manifest)}",
        "",
        "## Coverage",
        "",
        "| Measure class | Selection status | Chamber rows |",
        "| --- | --- | ---: |",
    ]
    for (measure_class, status), count in sorted(class_status.items()):
        lines.append(f"| {measure_class.replace('_', ' ')} | `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Operational Definition",
            "",
            "- The population is every H.R., S., H.J.Res., and S.J.Res. measure classified as presented to the President in the committed 108th-118th Congress decision panels.",
            "- Each measure contributes one House row and one Senate row. The selected event is the latest successful final passage, concurrence, or conference-report approval action in that chamber on or before presentment.",
            "- Motions to proceed, instruct, recommit, reconsider, table, invoke cloture, postpone, or decide consideration are excluded even when their text contains an affirmative result.",
            "- A roll call is retained only when the selected final approval action itself carries a GovInfo recorded-vote reference. Earlier roll calls are not substituted for a later voice vote or unanimous-consent approval.",
            "- Recorded votes are parsed from official House Clerk or Senate LIS XML. Overall and party support shares use yea divided by yea plus nay; present, absent, and not-voting members are excluded from that denominator.",
            "- When one official Senate roll-call question expressly names several measures but the document field names only one, each named measure is labeled `matched_grouped_question`; the representative document identifier remains unchanged in the panel.",
            "- H.R./S. bills and joint resolutions remain separately labeled. Constitutional-amendment joint resolutions never presented to the President are outside this decision population.",
            "",
            "Claim boundary: final chamber-vote support is post-passage descriptive context for presidential decisions. The panel does not identify causal presidential preferences, legislator ideal points, public opinion, bill quality, welfare, or institutional rank. Missing roll calls are observed voice-vote or unanimous-consent pathways and are not imputed.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision-panels", type=Path, nargs="+", default=list(DEFAULT_DECISION_PANELS))
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE_DIR)
    parser.add_argument("--vote-cache", type=Path, default=DEFAULT_VOTE_CACHE)
    parser.add_argument("--output", type=Path, default=OUT_CSV)
    parser.add_argument("--metadata-output", type=Path, default=OUT_METADATA)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=90.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    decision_panels = tuple(args.decision_panels)
    for path in decision_panels:
        require(path.exists(), f"Missing decision panel: {path}")
    lifecycle_builder = Path(__file__).with_name("build_govinfo_bill_census_dataset.py")
    code_hash = sha256_file(Path(__file__))
    config_hash = configuration_sha256(decision_panels, lifecycle_builder)
    if not args.refresh and not args.rebuild and output_cache_matches(
        args.output, args.metadata_output, config_hash, code_hash
    ):
        print(f"Using matching output cache {args.output}")
        return 0
    decisions = decision_rows(decision_panels)
    rows, source_manifest = build_rows(
        decisions,
        args.archive_dir,
        args.vote_cache,
        args.refresh,
        args.offline,
        args.retries,
        args.timeout,
    )
    write_csv(rows, args.output)
    write_reproducible_metadata(
        args.metadata_output,
        metadata_content(
            rows,
            decisions,
            source_manifest,
            args.output,
            decision_panels,
            config_hash,
            code_hash,
            lifecycle_builder,
        ),
    )
    print(f"Wrote {args.output} ({len(rows)} chamber rows)")
    print(f"Wrote {args.metadata_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
