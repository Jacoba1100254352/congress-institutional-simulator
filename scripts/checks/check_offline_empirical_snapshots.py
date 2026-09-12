#!/usr/bin/env python3
"""Verify frozen derived-source extracts without live source acquisition."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# These committed extracts retain Dataverse file IDs, source MD5s, and claim
# boundaries. A source refresh is a separate, reviewed baseline update.
CES_POLICY = {
    "data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv": (
        "aaa4e263255a583f83f22160fbaa2048e3f72e4d2495c621569b7a36d1e2ec80", 54,
    ),
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv": (
        "407ef1c7dd81c5e14f12d856ecd2e3f8433c04d8391607840312ad0f252694ee", 918,
    ),
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv": (
        "dd2fca55fe683d1c879431b3542bb9ad7a12b460708b38e55bf8cae950fb3ac6", 54,
    ),
}
MEMBER_VOTES = {
    "data/validation/raw/bill_finance_lobbying_member_vote_targets.csv": (
        "ffd5071e13553f9a9b452d0cd15204c3a3cc9815f15e5f0d62777425cb73c140", 3435,
    ),
}
SNAPSHOTS = {**CES_POLICY, **MEMBER_VOTES}


def check_snapshot(root: Path = ROOT, snapshots: dict[str, tuple[str, int]] = SNAPSHOTS) -> None:
    for relative, (expected_hash, expected_rows) in snapshots.items():
        path = root / relative
        if not path.is_file():
            raise SystemExit(f"Missing frozen source extract: {relative}. Restore the committed snapshot; offline reproduction does not download it.")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            raise SystemExit(f"Frozen source extract changed: {relative}. Restore the committed snapshot or review the explicit source refresh and its baseline pins.")
        with path.open(newline="", encoding="utf-8") as handle:
            count = sum(1 for _ in csv.DictReader(handle))
        if count != expected_rows:
            raise SystemExit(f"Frozen source row-count mismatch: {relative}: {count} != {expected_rows}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=("all", "ces-policy", "member-votes"), default="all")
    args = parser.parse_args()
    selected = {"all": SNAPSHOTS, "ces-policy": CES_POLICY, "member-votes": MEMBER_VOTES}[args.group]
    check_snapshot(snapshots=selected)
    print(f"Frozen source snapshot check passed: {len(selected)} files; no network access.")
