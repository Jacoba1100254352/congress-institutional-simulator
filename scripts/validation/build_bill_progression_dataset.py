#!/usr/bin/env python3
"""Build a documented raw bill-progression validation sample.

The project keeps API adapter fixtures separate from raw validation inputs. This
script uses the Congress.gov bill and action endpoints to create a small,
documented empirical sample under data/validation/raw/. It intentionally does
not write API keys or local environment values to disk.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


RAW_DIR = Path("data/validation/raw")
OUT_CSV = RAW_DIR / "bill_progression.csv"
OUT_META = RAW_DIR / "bill_progression.metadata.md"
USER_AGENT = "congress-institutional-simulator-validation/0.2"


@dataclass(frozen=True)
class BillRef:
    congress: int
    bill_type: str
    number: str
    title: str
    update_date: str

    @property
    def bill_id(self) -> str:
        return f"{self.congress}-{self.bill_type.lower()}-{self.number}"

    @property
    def detail_url(self) -> str:
        return f"https://www.congress.gov/bill/{self.congress}th-congress/{self.bill_type.lower()}-bill/{self.number}"


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


def api_get(url: str, params: dict[str, object], retries: int = 4) -> dict[str, object]:
    request_url = f"{url}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except (HTTPError, TimeoutError, URLError):
            if attempt == retries:
                raise
            time.sleep(1.75 * attempt)
    raise RuntimeError("unreachable retry state")


def parse_offsets(value: str) -> list[int]:
    offsets: list[int] = []
    for part in value.split(","):
        stripped = part.strip()
        if stripped:
            offsets.append(max(0, int(stripped)))
    return offsets or [0]


def bill_refs(api_key: str, congress: int, page_limit: int, offsets: list[int]) -> list[BillRef]:
    refs: dict[str, BillRef] = {}
    for offset in offsets:
        payload = api_get(
            f"https://api.congress.gov/v3/bill/{congress}",
            {"api_key": api_key, "format": "json", "limit": page_limit, "offset": offset},
        )
        bills = payload.get("bills", [])
        if not isinstance(bills, list):
            continue
        for bill in bills:
            if not isinstance(bill, dict):
                continue
            bill_type = str(bill.get("type", "")).lower()
            number = str(bill.get("number", ""))
            if not bill_type or not number:
                continue
            ref = BillRef(
                congress=congress,
                bill_type=bill_type,
                number=number,
                title=str(bill.get("title") or ""),
                update_date=str(bill.get("updateDate") or bill.get("latestAction", {}).get("actionDate") or ""),
            )
            refs[ref.bill_id] = ref
    return list(refs.values())


def action_flag(actions: list[dict[str, object]], needles: tuple[str, ...]) -> bool:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in needles):
            return True
    return False


def action_date(actions: list[dict[str, object]], predicate: tuple[str, ...]) -> str:
    for action in actions:
        text = str(action.get("text", "")).lower()
        action_type = str(action.get("type", "")).lower()
        if any(needle in text or needle in action_type for needle in predicate):
            return str(action.get("actionDate") or "")
    return ""


def policy_area(detail: dict[str, object]) -> str:
    area = detail.get("policyArea")
    if isinstance(area, dict):
        return str(area.get("name") or "Unclassified")
    return "Unclassified"


def sponsor_party(detail: dict[str, object]) -> str:
    sponsors = detail.get("sponsors") or []
    if isinstance(sponsors, list) and sponsors and isinstance(sponsors[0], dict):
        return str(sponsors[0].get("party") or "unknown")
    return "unknown"


def build_rows(api_key: str, refs: list[BillRef], sleep_seconds: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for ref in refs:
        detail_payload = api_get(
            f"https://api.congress.gov/v3/bill/{ref.congress}/{ref.bill_type}/{ref.number}",
            {"api_key": api_key, "format": "json"},
        )
        detail = detail_payload.get("bill", {})
        if not isinstance(detail, dict):
            detail = {}
        actions_payload = api_get(
            f"https://api.congress.gov/v3/bill/{ref.congress}/{ref.bill_type}/{ref.number}/actions",
            {"api_key": api_key, "format": "json", "limit": 250},
        )
        actions = actions_payload.get("actions", [])
        if not isinstance(actions, list):
            actions = []

        committee_reported = action_flag(actions, (
            "reported by",
            "reported to",
            "ordered to be reported",
            "committee discharged",
        ))
        floor_considered = action_flag(actions, (
            "passed house",
            "passed/agreed to in house",
            "passed senate",
            "passed/agreed to in senate",
            "considered under",
            "on motion to suspend the rules and pass",
            "cloture on the motion to proceed",
            "motion to proceed",
            "agreed to",
        ))
        enacted = action_flag(actions, ("became public law", "signed by president"))
        if detail.get("laws"):
            enacted = True

        rows.append({
            "bill_id": ref.bill_id,
            "congress": ref.congress,
            "bill_type": ref.bill_type,
            "bill_number": ref.number,
            "introduced": "1",
            "committee_reported": "1" if committee_reported else "0",
            "floor_considered": "1" if floor_considered else "0",
            "enacted": "1" if enacted else "0",
            "introduced_date": str(detail.get("introducedDate") or ""),
            "committee_reported_date": action_date(actions, ("reported by", "ordered to be reported")),
            "floor_action_date": action_date(actions, ("passed house", "passed senate", "considered under", "motion to proceed", "agreed to")),
            "enacted_date": action_date(actions, ("became public law", "signed by president")),
            "policy_area": policy_area(detail),
            "sponsor_party": sponsor_party(detail),
            "actions_count": len(actions),
            "source_url": ref.detail_url,
        })
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)
    return rows


def write_csv(rows: list[dict[str, object]]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "bill_id",
        "congress",
        "bill_type",
        "bill_number",
        "introduced",
        "committee_reported",
        "floor_considered",
        "enacted",
        "introduced_date",
        "committee_reported_date",
        "floor_action_date",
        "enacted_date",
        "policy_area",
        "sponsor_party",
        "actions_count",
        "source_url",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(args: argparse.Namespace, rows: list[dict[str, object]]) -> None:
    introduced = len(rows)
    floor = sum(1 for row in rows if row["floor_considered"] == "1")
    committee = sum(1 for row in rows if row["committee_reported"] == "1")
    enacted = sum(1 for row in rows if row["enacted"] == "1")
    lines = [
        "# Bill Progression Raw Validation Sample",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "- Source: Congress.gov API v3 bill, bill-detail, and bill-action endpoints.",
        f"- Congress: {args.congress}",
        f"- List offsets: {args.offsets}",
        f"- Page limit per offset: {args.page_limit}",
        f"- Rows: {introduced}",
        f"- Committee reported share: {committee / introduced:.4f}" if introduced else "- Committee reported share: 0.0000",
        f"- Floor-considered share: {floor / introduced:.4f}" if introduced else "- Floor-considered share: 0.0000",
        f"- Enactment share: {enacted / introduced:.4f}" if introduced else "- Enactment share: 0.0000",
        "",
        "This is a curated validation sample, not a complete Census of Congress.",
        "It is suitable for smoke-testing empirical bridge calculations and rough",
        "plausibility comparison. Do not treat it as a final fitted benchmark.",
    ]
    OUT_META.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=None, help="Optional .env file containing CONGRESS_API_KEY.")
    parser.add_argument("--congress", type=int, default=118)
    parser.add_argument("--page-limit", type=int, default=60)
    parser.add_argument("--offsets", default="0,500,1500", help="Comma-separated Congress.gov list offsets.")
    parser.add_argument("--sleep", type=float, default=0.05, help="Delay between bill detail/action requests.")
    args = parser.parse_args()

    import os

    api_key = os.environ.get("CONGRESS_API_KEY") or env_values(args.env_file).get("CONGRESS_API_KEY")
    if not api_key:
        raise SystemExit("CONGRESS_API_KEY not found. Pass --env-file or export it in the environment.")

    offsets = parse_offsets(args.offsets)
    refs = bill_refs(api_key, args.congress, args.page_limit, offsets)
    rows = build_rows(api_key, refs, args.sleep)
    rows.sort(key=lambda row: str(row["bill_id"]))
    write_csv(rows)
    write_metadata(args, rows)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_META}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
