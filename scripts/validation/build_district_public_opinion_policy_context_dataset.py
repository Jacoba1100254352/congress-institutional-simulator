#!/usr/bin/env python3
"""Build bounded district-opinion policy-area context rows.

The district-opinion linkage cache joins Cumulative CES district aggregates to
House-sponsored public-law bill metadata by sponsor district. This derived file
adds local topic-throughput counts for those bill policy areas. It is policy-area
context only, not issue-specific bill support or MRP evidence.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


DISTRICT_OPINION_LINKAGE = Path("data/validation/raw/district_public_opinion_linkage.csv")
TOPIC_THROUGHPUT = Path("data/validation/raw/topic_throughput.csv")
OUT_CSV = Path("data/validation/raw/district_public_opinion_policy_context.csv")
OUT_METADATA = Path("data/validation/raw/district_public_opinion_policy_context.metadata.md")

CLAIM_BOUNDARY = (
    "Bounded Cumulative CES district aggregate to sponsor-district public-law "
    "bill policy-area context only; not bill-topic support, MRP or small-area "
    "estimation, issue-specific affected-group mapping or harm, representative "
    "responsiveness, public benefit, welfare, causal effect, or model validation."
)

MISSING_LINKS = (
    "issue_specific_bill_support; MRP_or_small_area_estimate; "
    "ACS_affected_population; affected_group_harm; constituent_contacts; "
    "member_vote; causal_representation; public_benefit; model_validation"
)

FIELDNAMES = [
    "district_id",
    "issue",
    "year",
    "support",
    "intensity",
    "turnout",
    "affected_group_share",
    "bill_id",
    "public_law_number",
    "congress",
    "bill_type",
    "bill_number",
    "policy_area",
    "topic_introduced",
    "topic_floor_considered",
    "topic_enacted",
    "sponsor_bioguide_id",
    "sponsor_name",
    "sponsor_party",
    "sponsor_state",
    "sponsor_district",
    "sponsor_chamber",
    "policy_context_status",
    "linkage_status",
    "linkage_basis",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
    "source_url",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def topic_by_name(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("topic", "").strip(): row for row in rows if row.get("topic", "").strip()}


def build_rows() -> list[dict[str, str]]:
    topic_lookup = topic_by_name(read_csv(TOPIC_THROUGHPUT))
    rows: list[dict[str, str]] = []
    for source in read_csv(DISTRICT_OPINION_LINKAGE):
        policy_area = source.get("policy_area", "").strip()
        topic = topic_lookup.get(policy_area, {})
        mapped = bool(topic)
        rows.append({
            "district_id": source.get("district_id", ""),
            "issue": source.get("issue", ""),
            "year": source.get("year", ""),
            "support": source.get("support", ""),
            "intensity": source.get("intensity", ""),
            "turnout": source.get("turnout", ""),
            "affected_group_share": source.get("affected_group_share", ""),
            "bill_id": source.get("bill_id", ""),
            "public_law_number": source.get("public_law_number", ""),
            "congress": source.get("congress", ""),
            "bill_type": source.get("bill_type", ""),
            "bill_number": source.get("bill_number", ""),
            "policy_area": policy_area,
            "topic_introduced": topic.get("introduced", ""),
            "topic_floor_considered": topic.get("floor_considered", ""),
            "topic_enacted": topic.get("enacted", ""),
            "sponsor_bioguide_id": source.get("sponsor_bioguide_id", ""),
            "sponsor_name": source.get("sponsor_name", ""),
            "sponsor_party": source.get("sponsor_party", ""),
            "sponsor_state": source.get("sponsor_state", ""),
            "sponsor_district": source.get("sponsor_district", ""),
            "sponsor_chamber": source.get("sponsor_chamber", ""),
            "policy_context_status": (
                "sponsor_district_bill_policy_context"
                if mapped
                else "unmapped_sponsor_district_policy_area"
            ),
            "linkage_status": source.get("linkage_status", ""),
            "linkage_basis": (
                source.get("linkage_basis", "")
                + "; district_public_opinion_linkage.policy_area -> topic_throughput.topic"
            ),
            "evidence_layers": (
                "cumulative_ces_district_aggregate; sponsor_district_public_law_bill_metadata; "
                "topic_throughput_policy_area"
                if mapped
                else "cumulative_ces_district_aggregate; sponsor_district_public_law_bill_metadata"
            ),
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
            "source_url": source.get("source_url", ""),
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    mapped = [
        row for row in rows
        if row["policy_context_status"] == "sponsor_district_bill_policy_context"
    ]
    policy_counts = Counter(row["policy_area"] for row in mapped if row["policy_area"])
    issue_counts = Counter(row["issue"] for row in rows if row["issue"])
    policy_lines = "\n".join(
        f"- {policy}: {count}"
        for policy, count in sorted(policy_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    issue_lines = "\n".join(
        f"- {issue}: {count}"
        for issue, count in sorted(issue_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    unique_keys = {(row["district_id"], row["issue"], row["year"]) for row in rows}
    OUT_METADATA.write_text(
        "# District Public-Opinion Policy Context\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        "Sources:\n\n"
        f"- District public-opinion bill-sponsor linkage: `{DISTRICT_OPINION_LINKAGE}`.\n"
        f"- Local Congress.gov policy-area topic throughput: `{TOPIC_THROUGHPUT}`.\n\n"
        "Transformation:\n\n"
        "- Preserves one output row per cached sponsor-district public-law bill metadata row.\n"
        "- Adds local topic-throughput counts when the linked bill policy area is present in the topic sample.\n"
        "- Keeps support, turnout, intensity, and affected-group-share proxy fields separate from bill policy area.\n"
        "- Does not infer issue-specific bill support, MRP estimates, affected-group harm, constituent contact, member vote choice, or causal representation.\n\n"
        "Rows:\n\n"
        f"- Policy-context rows: {len(rows)}.\n"
        f"- Rows with mapped policy-area topic context: {len(mapped)}.\n"
        f"- Unique district-opinion row keys: {len(unique_keys)}.\n"
        f"- Unique public-law bills: {len({row['bill_id'] for row in rows if row['bill_id']})}.\n"
        f"- Unique sponsor districts: {len({row['district_id'] for row in rows if row['district_id']})}.\n"
        f"- Unique policy areas: {len(policy_counts)}.\n\n"
        "Rows by survey proxy:\n\n"
        f"{issue_lines if issue_lines else '- none'}\n\n"
        "Rows by policy area:\n\n"
        f"{policy_lines if policy_lines else '- none'}\n\n"
        "Claim boundary:\n\n"
        f"{CLAIM_BOUNDARY}\n"
    )


def main() -> int:
    for path in (DISTRICT_OPINION_LINKAGE, TOPIC_THROUGHPUT):
        if not path.exists():
            raise SystemExit(f"{path} is missing; build prerequisite raw data first.")
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{DISTRICT_OPINION_LINKAGE} is empty.")
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
