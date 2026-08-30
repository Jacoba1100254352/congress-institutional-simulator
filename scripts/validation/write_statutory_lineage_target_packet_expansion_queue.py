#!/usr/bin/env python3
"""Write row-level target packet expansion tasks for complete-lineage review."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


COMPLETE_LINEAGE_EXPANSION_QUEUE = Path(
    "reports/statutory-lineage-complete-lineage-expansion-queue.csv"
)
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
TARGET_TRIAGE = Path("reports/statutory-lineage-target-section-triage.csv")
TARGET_REVIEW_PACKETS = Path("reports/statutory-lineage-target-review-packets.csv")
OUT_CSV = Path("reports/statutory-lineage-target-packet-expansion-queue.csv")
OUT_MD = Path("reports/statutory-lineage-target-packet-expansion-queue.md")

CLAIM_BOUNDARY = (
    "Target packet expansion queue only; rows identify already-triaged U.S.C. "
    "target references that are absent from the current OLRC target-review "
    "packet set. This artifact does not establish codified lineage, target-section "
    "text diffs, effective statutory text, public-law attribution, implementation "
    "outcomes, direct target-section court review, welfare evidence, causal "
    "effects, or model validation."
)

FIELDNAMES = [
    "packet_expansion_rank",
    "expansion_rank",
    "completion_rank",
    "triage_rank",
    "source_scan_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "target_reference",
    "target_reference_type",
    "codification_review_status",
    "packet_gap_status",
    "candidate_snippet_count",
    "amendment_snippet_count",
    "repeal_snippet_count",
    "redesignation_snippet_count",
    "incomplete_fragment_count",
    "example_snippets",
    "govinfo_text_url",
    "complete_lineage_expansion_status",
    "source_scan_target_candidate_count",
    "triage_to_packet_gap_rows",
    "remaining_completion_gates",
    "next_packet_expansion_action",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make statutory-lineage-complete-lineage-expansion-queue first.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def int_field(row: dict[str, str], field: str) -> int:
    try:
        return int(row.get(field, "0") or "0")
    except ValueError:
        return 0


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        clean = " ".join((value or "").split())
        if clean and clean not in seen:
            seen.append(clean)
    return "; ".join(seen)


def by_bill(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id and bill_id not in result:
            result[bill_id] = row
    return result


def packet_keys(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {
        (row.get("bill_id", "").strip(), row.get("target_reference", "").strip())
        for row in rows
        if row.get("bill_id", "").strip()
        and row.get("target_reference", "").strip()
    }


def is_candidate_triage_row(row: dict[str, str]) -> bool:
    target = row.get("target_reference", "").strip()
    return bool(target and target != "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN")


def action_for_status(row: dict[str, str]) -> str:
    status = row.get("codification_review_status", "").strip()
    target_reference = row.get("target_reference", "").strip()
    if status == "title_only_needs_manual_target":
        return (
            "Resolve the title-only U.S.C. reference to a specific section, note, "
            "or no-target disposition before building an OLRC pre/post packet."
        )
    if status == "incomplete_reference_fragment_needs_manual_review":
        return (
            "Resolve the incomplete U.S.C. fragment against the public-law source "
            "text before building an OLRC pre/post packet."
        )
    if status == "mixed_target_reference_needs_manual_review":
        return (
            "Separate mixed target-reference cues into concrete U.S.C. sections "
            "before building OLRC pre/post packets."
        )
    if target_reference.endswith(" title-only"):
        return (
            "Manually resolve the title-level reference to a concrete U.S.C. "
            "target or no-target disposition before packet construction."
        )
    return (
        "Build an official OLRC pre/post target-review packet for this triaged "
        "reference, preserving annual URLs, source hashes, public-law context, "
        "and manual source-review disposition boundaries."
    )


def build_rows() -> list[dict[str, str]]:
    expansion_rows = read_csv(COMPLETE_LINEAGE_EXPANSION_QUEUE)
    source_rows = read_csv(SOURCE_SCAN)
    triage_rows = read_csv(TARGET_TRIAGE)
    packet_rows = read_csv(TARGET_REVIEW_PACKETS)

    expansion_by_bill = by_bill(expansion_rows)
    source_by_bill = by_bill(source_rows)
    existing_packets = packet_keys(packet_rows)
    rows: list[dict[str, str]] = []

    for triage_row in sorted(triage_rows, key=lambda row: int_field(row, "triage_rank")):
        bill_id = triage_row.get("bill_id", "").strip()
        expansion_row = expansion_by_bill.get(bill_id, {})
        if not expansion_row:
            continue
        if expansion_row.get("next_actionable_upgrade_gate", "").strip() != "codified_usc_lineage":
            continue
        if not is_candidate_triage_row(triage_row):
            continue
        target_reference = triage_row.get("target_reference", "").strip()
        if (bill_id, target_reference) in existing_packets:
            continue
        if target_reference not in split_values(expansion_row.get("triage_references_needing_packet_review", "")):
            raise SystemExit(
                f"{COMPLETE_LINEAGE_EXPANSION_QUEUE}: {bill_id} {target_reference} "
                "is missing from packet set but absent from expansion gap list."
            )
        source_row = source_by_bill.get(bill_id, {})
        evidence_layers = [
            "statutory_lineage_target_packet_expansion_queue",
        ]
        missing_links = [
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "law_revision_effective_text",
            "public_law_causal_attribution",
            "complete_codified_usc_lineage_review",
            "implementation_outcomes_or_enforcement",
            "direct_target_section_court_review",
            "welfare_or_public_benefit",
            "model_validation",
        ]
        for row in (expansion_row, triage_row, source_row):
            evidence_layers.extend(split_values(row.get("evidence_layers", "")))
            missing_links.extend(split_values(row.get("missing_links", "")))
        source_artifacts = [
            str(COMPLETE_LINEAGE_EXPANSION_QUEUE),
            str(TARGET_TRIAGE),
            str(TARGET_REVIEW_PACKETS),
            str(SOURCE_SCAN),
        ]
        rows.append({
            "packet_expansion_rank": "0",
            "expansion_rank": expansion_row.get("expansion_rank", "").strip(),
            "completion_rank": expansion_row.get("completion_rank", "").strip(),
            "triage_rank": triage_row.get("triage_rank", "").strip(),
            "source_scan_rank": triage_row.get("source_scan_rank", "").strip(),
            "bill_id": bill_id,
            "public_law_number": triage_row.get("public_law_number", "").strip(),
            "policy_area": expansion_row.get("policy_area", "").strip(),
            "target_reference": target_reference,
            "target_reference_type": triage_row.get("target_reference_type", "").strip(),
            "codification_review_status": triage_row.get("codification_review_status", "").strip(),
            "packet_gap_status": "triaged_reference_needs_olrc_target_review_packet",
            "candidate_snippet_count": triage_row.get("candidate_snippet_count", "0").strip(),
            "amendment_snippet_count": triage_row.get("amendment_snippet_count", "0").strip(),
            "repeal_snippet_count": triage_row.get("repeal_snippet_count", "0").strip(),
            "redesignation_snippet_count": triage_row.get("redesignation_snippet_count", "0").strip(),
            "incomplete_fragment_count": triage_row.get("incomplete_fragment_count", "0").strip(),
            "example_snippets": triage_row.get("example_snippets", "").strip(),
            "govinfo_text_url": triage_row.get("govinfo_text_url", "").strip(),
            "complete_lineage_expansion_status": expansion_row.get("complete_lineage_expansion_status", "").strip(),
            "source_scan_target_candidate_count": source_row.get("target_section_candidate_count", "0").strip(),
            "triage_to_packet_gap_rows": expansion_row.get("triage_to_packet_gap_rows", "0").strip(),
            "remaining_completion_gates": expansion_row.get("remaining_completion_gates", "").strip(),
            "next_packet_expansion_action": action_for_status(triage_row),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join(source_artifacts),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    rows.sort(
        key=lambda row: (
            int(row["expansion_rank"] or "999999"),
            0 if row["codification_review_status"] == "needs_olrc_us_code_note_review" else 1,
            int(row["triage_rank"] or "999999"),
            row["target_reference"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["packet_expansion_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["codification_review_status"] for row in rows)
    bill_counts = Counter(row["bill_id"] for row in rows)
    type_counts = Counter(row["target_reference_type"] for row in rows)
    lines = [
        "# Statutory Lineage Target Packet Expansion Queue",
        "",
        "This report turns complete-lineage triage-to-packet gaps into row-level OLRC packet-construction tasks. It covers already-triaged target references that are absent from the current target-review packet set. It is a packet-building queue, not codified-lineage evidence.",
        "",
        f"- Target packet expansion queue rows: {len(rows)}",
        f"- Public laws with packet-expansion tasks: {len(bill_counts)}",
        f"- Direct U.S.C. note-review tasks: {status_counts.get('needs_olrc_us_code_note_review', 0)}",
        f"- Title-only manual-target tasks: {status_counts.get('title_only_needs_manual_target', 0)}",
        f"- Incomplete-fragment manual-review tasks: {status_counts.get('incomplete_reference_fragment_needs_manual_review', 0)}",
        "",
        "Target reference types:",
    ]
    for target_type, count in sorted(type_counts.items()):
        lines.append(f"- {target_type}: {count}")
    lines.extend([
        "",
        "Codification review statuses:",
    ])
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Target reference | Review status | Snippets | Next action |",
        "| ---: | --- | --- | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['packet_expansion_rank']} | `{row['bill_id']}` | "
            f"`{row['public_law_number']}` | `{row['target_reference']}` | "
            f"{row['codification_review_status']} | {row['candidate_snippet_count']} | "
            f"{row['next_packet_expansion_action']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No target packet expansion rows were generated.")
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
