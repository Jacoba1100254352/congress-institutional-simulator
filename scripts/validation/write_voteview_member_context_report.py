#!/usr/bin/env python3
"""Write a bounded Voteview member-context report from cached rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROLLCALLS = Path("data/validation/raw/voteview_rollcalls.csv")
MEMBER_CONTEXT = Path("data/validation/raw/voteview_member_context.csv")
OUT_CSV = Path("reports/voteview-member-context.csv")
OUT_MD = Path("reports/voteview-member-context.md")

FIELDNAMES = [
    "congress",
    "chamber",
    "icpsr",
    "bioguide_id",
    "bioname",
    "party",
    "state_abbrev",
    "district_id",
    "rollcall_rows",
    "unique_vote_ids",
    "linkage_status",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Voteview actor-metadata context only; not roll-call-to-bill linkage, "
    "district public-opinion representation, sponsor effectiveness, public "
    "benefit, welfare, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(MEMBER_CONTEXT):
        evidence_layers = ["voteview_member_metadata"]
        if row.get("bioguide_id"):
            evidence_layers.append("bioguide_actor_identifier")
        if row.get("district_id"):
            evidence_layers.append("member_district_metadata")
        rows.append({
            "congress": row.get("congress", ""),
            "chamber": row.get("chamber", ""),
            "icpsr": row.get("icpsr", ""),
            "bioguide_id": row.get("bioguide_id", ""),
            "bioname": row.get("bioname", ""),
            "party": row.get("party", ""),
            "state_abbrev": row.get("state_abbrev", ""),
            "district_id": row.get("district_id", ""),
            "rollcall_rows": row.get("rollcall_rows", ""),
            "unique_vote_ids": row.get("unique_vote_ids", ""),
            "linkage_status": row.get("linkage_status", ""),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join([
                "roll_call_to_bill_or_action",
                "public_law_or_statute",
                "district_public_opinion_issue",
                "sponsor_success_or_member_effectiveness",
                "model_validation",
            ]),
            "source_url": row.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    rollcall_total = sum(int(row["rollcall_rows"] or "0") for row in rows)
    bioguide_rows = [row for row in rows if row["bioguide_id"]]
    bioguide_rollcall_rows = sum(int(row["rollcall_rows"] or "0") for row in bioguide_rows)
    district_rows = [row for row in rows if row["district_id"]]
    status_counts = Counter(row["linkage_status"] for row in rows)
    chamber_counts = Counter(row["chamber"] or "Unknown" for row in rows)
    party_counts = Counter(row["party"] or "Unknown" for row in rows)

    lines = [
        "# Voteview Member Context",
        "",
        "This report derives a bounded actor-metadata join from cached Voteview roll-call rows and cached Voteview member metadata. It is a member-context inventory, not bill-level roll-call validation.",
        "",
        f"- Voteview member-context rows: {len(rows)}",
        f"- Roll-call member-vote rows represented: {rollcall_total}",
        f"- Member-context rows with Bioguide IDs: {len(bioguide_rows)}",
        f"- Roll-call member-vote rows with Bioguide member metadata: {bioguide_rollcall_rows}",
        f"- Member-context rows with district metadata: {len(district_rows)}",
        "",
        "Claim boundary: this context attaches public Voteview member identifiers, Bioguide IDs, state/district metadata, and ideal-point fields to current roll-call rows. It does not join roll calls to bills, public laws, statutory sections, issue-specific public opinion, sponsor-effectiveness rows, or legislative outcomes, and it does not validate representation, welfare, public benefit, or model behavior.",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Chambers:")
    for chamber, count in sorted(chamber_counts.items()):
        lines.append(f"- {chamber}: {count}")
    lines.append("")
    lines.append("Parties:")
    for party, count in sorted(party_counts.items()):
        lines.append(f"- {party}: {count}")
    lines.extend([
        "",
        "| Member | Bioguide | Party | District | Roll-call rows | Missing links |",
        "| --- | --- | --- | --- | ---: | --- |",
    ])
    for row in sorted(rows, key=lambda item: (-int(item["rollcall_rows"] or "0"), item["bioname"]))[:20]:
        district = row["district_id"] or row["state_abbrev"] or "---"
        lines.append(
            f"| {row['bioname'] or row['icpsr']} | `{row['bioguide_id'] or '---'}` | "
            f"{row['party'] or '---'} | `{district}` | {row['rollcall_rows']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit(f"{MEMBER_CONTEXT} is missing or empty; run make build-voteview-member-context-raw first.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
