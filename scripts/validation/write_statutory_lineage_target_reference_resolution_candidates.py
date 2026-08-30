#!/usr/bin/env python3
"""Write bounded resolution candidates for ambiguous target-packet references."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SOURCE_GAP_QUEUE = Path("reports/statutory-lineage-target-packet-source-gap-queue.csv")
SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-target-reference-resolution-candidates.csv")
OUT_MD = Path("reports/statutory-lineage-target-reference-resolution-candidates.md")

CLAIM_BOUNDARY = (
    "Target-reference resolution candidates only; rows use ordered GovInfo "
    "public-law source-scan snippets to suggest concrete U.S.C. sections for "
    "title-only or incomplete packet blockers. This artifact does not confirm "
    "the target section, establish codified lineage, create OLRC pre/post "
    "packets, prove target-section text diffs, effective statutory text, "
    "public-law attribution, implementation outcomes, direct court review, "
    "welfare evidence, causal effects, or model validation."
)

AMBIGUOUS_SOURCE_GAP_STATUSES = {
    "title_only_reference_needs_section_resolution_before_packet",
    "incomplete_or_nonsection_reference_needs_manual_resolution_before_packet",
}

FIELDNAMES = [
    "resolution_rank",
    "source_gap_rank",
    "packet_expansion_rank",
    "expansion_rank",
    "completion_rank",
    "triage_rank",
    "source_scan_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "unresolved_target_reference",
    "unresolved_target_reference_type",
    "codification_review_status",
    "source_gap_status",
    "resolution_candidate_status",
    "candidate_reference_count",
    "candidate_target_references",
    "strongest_candidate_reference",
    "candidate_basis",
    "candidate_context_snippets",
    "next_resolution_action",
    "remaining_completion_gates",
    "evidence_layers",
    "missing_links",
    "source_artifacts",
    "claim_boundary",
]

SECTION_RE = r"[A-Za-z0-9][A-Za-z0-9.\-]*(?:\([A-Za-z0-9]+\))*"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run make statutory-lineage-target-packet-source-gap-queue first.")
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


def snippets_for_source(row: dict[str, str]) -> list[str]:
    return split_values(row.get("target_section_candidates", ""))


def title_for_reference(reference: str) -> str:
    match = re.match(r"(?P<title>\d+)\s+USC\b", reference)
    return match.group("title") if match else ""


def clean_section(section: str) -> str:
    return re.sub(r"\s+", "", section).strip(" .;,")


def append_candidate(
    candidates: list[tuple[str, str, str]],
    reference: str,
    basis: str,
    context: str,
) -> None:
    clean_reference = " ".join(reference.split()).strip(" .;,")
    if not clean_reference:
        return
    if clean_reference.casefold().endswith(" title-only"):
        return
    if clean_reference not in {candidate[0] for candidate in candidates}:
        candidates.append((clean_reference, basis, context))


def title_only_at_end(snippet: str, title: str) -> bool:
    return bool(re.search(rf"\b{re.escape(title)}\s+U\.?\s*S\.?\s*C\.?\s*\.?$", snippet, re.IGNORECASE))


def resolution_candidates(row: dict[str, str], source_row: dict[str, str]) -> list[tuple[str, str, str]]:
    title = title_for_reference(row.get("target_reference", ""))
    if not title:
        return []
    snippets = snippets_for_source(source_row)
    candidates: list[tuple[str, str, str]] = []
    for index, snippet in enumerate(snippets):
        next_snippet = snippets[index + 1] if index + 1 < len(snippets) else ""
        context = f"{snippet} || {next_snippet}" if next_snippet else snippet

        for match in re.finditer(
            rf"<<NOTE:\s*{re.escape(title)}\s+USC\s+prec\.\s*(?P<section>{SECTION_RE})\.>>",
            snippet,
            re.IGNORECASE,
        ):
            section = clean_section(match.group("section"))
            append_candidate(
                candidates,
                f"{title} USC {section} prec",
                "same_snippet_note_marker_prec",
                context,
            )

        if re.search(rf"<<NOTE:\s*{re.escape(title)}\s+USC\s*$", snippet, re.IGNORECASE):
            match = re.match(rf"(?P<section>{SECTION_RE})\.>>", next_snippet.strip(), re.IGNORECASE)
            if match:
                section = clean_section(match.group("section"))
                append_candidate(candidates, f"{title} USC {section}", "split_note_marker", context)

        if not title_only_at_end(snippet, title):
            continue

        if "<<NOTE:" not in next_snippet and not next_snippet.strip().startswith("SEC."):
            match = re.search(
                rf"\(?\s*{re.escape(title)}\s+U\.?\s*S\.?\s*C\.?\s*\.?\s*(?P<section>{SECTION_RE}(?:\s+note)?)",
                next_snippet.strip(),
                re.IGNORECASE,
            )
            if match:
                section = clean_section(match.group("section"))
                append_candidate(candidates, f"{title} USC {section}", "next_snippet_full_title", context)

        match = re.match(
            rf"\(?\s*U\.?\s*S\.?\s*C\.?\s*\.?\s*(?P<section>{SECTION_RE}(?:\s+note)?)",
            next_snippet.strip(),
            re.IGNORECASE,
        )
        if match:
            section = clean_section(match.group("section"))
            append_candidate(candidates, f"{title} USC {section}", "next_snippet_implicit_title", context)

        match = re.match(
            rf"\(?\s*(?P<section>{SECTION_RE})\)+\s*(?:is|,|\s)",
            next_snippet.strip(),
            re.IGNORECASE,
        )
        if match:
            section = clean_section(match.group("section"))
            append_candidate(candidates, f"{title} USC {section}", "next_snippet_section_continuation", context)
    return candidates


def status_for(candidates: list[tuple[str, str, str]]) -> str:
    if candidates:
        return "bounded_govinfo_adjacent_snippet_candidate_identified"
    return "no_bounded_resolution_candidate_from_source_scan"


def next_action_for(candidates: list[tuple[str, str, str]]) -> str:
    if candidates:
        return (
            "Manually verify the suggested concrete U.S.C. target against official "
            "GovInfo public-law text and OLRC notes before building an OLRC "
            "pre/post packet."
        )
    return (
        "Manually review the GovInfo public-law text and OLRC notes because the "
        "bounded source scan did not produce a concrete section candidate."
    )


def build_rows() -> list[dict[str, str]]:
    source_gap_rows = read_csv(SOURCE_GAP_QUEUE)
    source_rows = read_csv(SOURCE_SCAN)
    source_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in source_rows
        if row.get("bill_id", "").strip()
    }
    rows: list[dict[str, str]] = []
    for source_gap_row in sorted(source_gap_rows, key=lambda row: int_field(row, "source_gap_rank")):
        if source_gap_row.get("source_gap_status", "").strip() not in AMBIGUOUS_SOURCE_GAP_STATUSES:
            continue
        bill_id = source_gap_row.get("bill_id", "").strip()
        source_row = source_by_bill.get(bill_id, {})
        candidates = resolution_candidates(source_gap_row, source_row) if source_row else []
        candidate_refs = [candidate[0] for candidate in candidates]
        bases = [candidate[1] for candidate in candidates]
        contexts = [candidate[2].replace("|", "/") for candidate in candidates[:3]]
        evidence_layers = [
            "statutory_lineage_target_reference_resolution_candidates",
            "statutory_lineage_target_packet_source_gap_queue",
            "statutory_lineage_source_scan",
        ]
        missing_links = [
            "manual_source_review_to_confirm_candidate_reference",
            "olrc_pre_post_target_review_packet",
            "source_reviewed_target_section_diff",
            "complete_codified_usc_lineage_review",
            "model_validation",
        ]
        for input_row in (source_gap_row, source_row):
            evidence_layers.extend(split_values(input_row.get("evidence_layers", "")))
            missing_links.extend(split_values(input_row.get("missing_links", "")))
        rows.append({
            "resolution_rank": "0",
            "source_gap_rank": source_gap_row.get("source_gap_rank", "").strip(),
            "packet_expansion_rank": source_gap_row.get("packet_expansion_rank", "").strip(),
            "expansion_rank": source_gap_row.get("expansion_rank", "").strip(),
            "completion_rank": source_gap_row.get("completion_rank", "").strip(),
            "triage_rank": source_gap_row.get("triage_rank", "").strip(),
            "source_scan_rank": source_gap_row.get("source_scan_rank", "").strip(),
            "bill_id": bill_id,
            "public_law_number": source_gap_row.get("public_law_number", "").strip(),
            "policy_area": source_gap_row.get("policy_area", "").strip(),
            "unresolved_target_reference": source_gap_row.get("target_reference", "").strip(),
            "unresolved_target_reference_type": source_gap_row.get("target_reference_type", "").strip(),
            "codification_review_status": source_gap_row.get("codification_review_status", "").strip(),
            "source_gap_status": source_gap_row.get("source_gap_status", "").strip(),
            "resolution_candidate_status": status_for(candidates),
            "candidate_reference_count": str(len(candidate_refs)),
            "candidate_target_references": "; ".join(candidate_refs),
            "strongest_candidate_reference": candidate_refs[0] if candidate_refs else "",
            "candidate_basis": unique_join(bases),
            "candidate_context_snippets": " || ".join(contexts),
            "next_resolution_action": next_action_for(candidates),
            "remaining_completion_gates": source_gap_row.get("remaining_completion_gates", "").strip(),
            "evidence_layers": unique_join(evidence_layers),
            "missing_links": unique_join(missing_links),
            "source_artifacts": unique_join([str(SOURCE_GAP_QUEUE), str(SOURCE_SCAN)]),
            "claim_boundary": CLAIM_BOUNDARY,
        })

    rows.sort(
        key=lambda row: (
            int(row["source_gap_rank"] or "999999"),
            row["unresolved_target_reference"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["resolution_rank"] = str(index)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["resolution_candidate_status"] for row in rows)
    bill_counts = Counter(row["bill_id"] for row in rows)
    candidate_rows = [
        row for row in rows
        if int(row.get("candidate_reference_count", "0") or "0") > 0
    ]
    candidate_count = sum(int(row.get("candidate_reference_count", "0") or "0") for row in rows)
    lines = [
        "# Statutory Lineage Target Reference Resolution Candidates",
        "",
        "This report suggests concrete U.S.C. target references for ambiguous target-packet blockers by pairing ordered GovInfo public-law source-scan snippets. It is a candidate list for manual review, not codified-lineage evidence.",
        "",
        f"- Ambiguous packet-blocker rows reviewed: {len(rows)}",
        f"- Public laws with ambiguous packet blockers: {len(bill_counts)}",
        f"- Rows with bounded candidate references: {len(candidate_rows)}",
        f"- Candidate concrete U.S.C. references suggested: {candidate_count}",
        f"- Rows still without bounded source-scan candidates: {len(rows) - len(candidate_rows)}",
        "",
        "Resolution candidate statuses:",
    ]
    if status_counts:
        for status, count in sorted(status_counts.items()):
            lines.append(f"- {status}: {count}")
    else:
        lines.append("- none: 0")
        lines.append("")
        lines.append("No ambiguous title-only or incomplete packet blockers remain in the current source-gap queue.")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Source-gap rank | Bill | Public law | Ambiguous reference | Candidates | Status | Next action |",
        "| ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        candidate_display = row["candidate_target_references"] or "none"
        lines.append(
            f"| {row['resolution_rank']} | {row['source_gap_rank']} | "
            f"`{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['unresolved_target_reference']}` | `{candidate_display}` | "
            f"{row['resolution_candidate_status']} | {row['next_resolution_action']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
