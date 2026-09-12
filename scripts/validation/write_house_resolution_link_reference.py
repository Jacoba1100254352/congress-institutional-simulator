#!/usr/bin/env python3
"""Retain and verify one resolution-mediated House procedure link.

Normal generation and --check are offline. --fetch downloads the two exact
public source versions; it refuses changed content rather than silently
refreshing this reviewed evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "data/validation/reference/house-procedure-resolution-sources"
REPORT = ROOT / "reports/house-agenda-control-resolution-linkage.json"
SOURCES = {
    "hres1061-eh.html": (
        "https://www.govinfo.gov/content/pkg/BILLS-118hres1061eh/html/BILLS-118hres1061eh.htm",
        "ad55e7cdf80fc09be8990e77e951969f5a427a0da4c4f787a91b014c32c77e16",
    ),
    "house-2024-roll064.xml": (
        "https://clerk.house.gov/evs/2024/roll064.xml",
        "cfc05b6a5cb336c0189261aa8dca96fa711e8a4493cb17055e2adf81d75b4716",
    ),
}


def checked_bytes(name: str, raw: bytes) -> bytes:
    # Retain LF-normalized source snapshots so Git checkout preserves hashes.
    normalized = raw.replace(b"\r\n", b"\n")
    if hashlib.sha256(normalized).hexdigest() != SOURCES[name][1]:
        raise ValueError(f"Pinned resolution-link source changed: {name}")
    return normalized


def evidence() -> dict:
    snapshots = {
        name: checked_bytes(name, (SOURCE_DIR / name).read_bytes())
        for name in SOURCES
    }
    vote = ET.fromstring(snapshots["house-2024-roll064.xml"]).find("vote-metadata")
    expected = {
        "congress": "118", "session": "2nd",
        "chamber": "U.S. House of Representatives", "rollcall-num": "64",
        "legis-num": "H RES 1061",
        "vote-question": "On Motion to Suspend the Rules and Agree",
        "vote-type": "2/3 YEA-AND-NAY", "vote-result": "Passed",
        "action-date": "6-Mar-2024",
        "vote-totals/totals-by-vote/yea-total": "339",
        "vote-totals/totals-by-vote/nay-total": "85",
    }
    if vote is None or any(vote.findtext(key) != value for key, value in expected.items()):
        raise ValueError("Resolution vote metadata does not match the reviewed House action")
    text = " ".join(html.unescape(snapshots["hres1061-eh.html"].decode()).split())
    match = re.search(r"Resolved, That upon the adoption.*?following amendment:", text)
    if match is None or "the bill, H.R. 4366" not in match.group():
        raise ValueError("Resolution must explicitly direct the reviewed bill-amendment concurrence")
    return {
        "schema_version": 1,
        "bill_id": "118-hr-4366", "resolution_id": "118-hres-1061",
        "date": "2024-03-06", "house_roll_call": 64,
        "vote_question": expected["vote-question"], "vote_result": "Passed",
        "yeas": 339, "nays": 85,
        "resolution_clause": match.group(),
        "finding": "The House adopted H. Res. 1061 under suspension; that resolution deemed concurrence in the Senate amendment to H.R. 4366 with an amendment.",
        "claim_boundary": "This verifies one resolution-mediated House suspension path, not a direct H.R. suspension motion or a complete cross-measure procedural census. It does not repair the original Senate-action provenance or change the frozen panel, fit, or failed gate.",
        "source_normalization": "CRLF to LF only; hashes cover complete retained source documents.",
        "sources": {
            str((SOURCE_DIR / name).relative_to(ROOT)): {"url": url, "sha256": digest}
            for name, (url, digest) in SOURCES.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fetch", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        fetched = {}
        for name, (url, _) in SOURCES.items():
            with urllib.request.urlopen(url, timeout=60) as response:
                fetched[name] = checked_bytes(name, response.read())
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        for name, raw in fetched.items():
            (SOURCE_DIR / name).write_bytes(raw)
    expected = json.dumps(evidence(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if REPORT.read_text() != expected:
            raise SystemExit("Resolution linkage reference is stale")
        print("Pinned House resolution linkage check passed.")
    else:
        REPORT.write_text(expected)
        print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
