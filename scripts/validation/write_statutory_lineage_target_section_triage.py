#!/usr/bin/env python3
"""Write a bounded target-section triage report for statutory-lineage review."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SOURCE_SCAN = Path("reports/statutory-lineage-source-scan.csv")
OUT_CSV = Path("reports/statutory-lineage-target-section-triage.csv")
OUT_MD = Path("reports/statutory-lineage-target-section-triage.md")

CLAIM_BOUNDARY = (
    "Target-section triage derived from official public-law source scans only. "
    "Rows rank candidate U.S.C. targets for manual OLRC/codified-text review; "
    "they do not establish codified U.S.C. lineage, target-section text diffs, "
    "implementation outcomes, court review, welfare, causal effects, or model validation."
)
MISSING_LINKS = (
    "olrc_us_code_classification",
    "codified_usc_lineage",
    "target_section_diff",
    "law_revision_effective_text",
    "model_validation",
)
EVIDENCE_LAYERS = (
    "statutory_lineage_source_scan",
    "govinfo_public_law_text_scan",
    "target_section_candidate_triage",
)
NEXT_REVIEW_ACTION = (
    "Review target reference against OLRC/U.S. Code notes and capture codified "
    "target-section before/after text before treating this row as lineage evidence."
)

PREC_USC_RE = re.compile(
    r"\b(?P<title>\d+)\s+U\.?\s*S\.?\s*C\.?\.?\s+prec\.?\s*"
    r"(?P<section>[A-Za-z0-9][A-Za-z0-9.\-]*(?:\([A-Za-z0-9]+\))*)",
    re.IGNORECASE,
)
DIRECT_USC_RE = re.compile(
    r"\b(?P<title>\d+)\s+U\.?\s*S\.?\s*C\.?\.?\s*"
    r"(?:§+\s*)?(?P<section>[A-Za-z0-9][A-Za-z0-9.\-]*(?:\([A-Za-z0-9]+\))*)?",
    re.IGNORECASE,
)
TITLE_CODE_SECTION_RE = re.compile(
    r"\bsections?\s+(?P<section>[0-9A-Za-z][0-9A-Za-z.\-]*(?:\([A-Za-z0-9]+\))*)"
    r"\s+of\s+title\s+(?P<title>\d+),\s+United States Code",
    re.IGNORECASE,
)
AMEND_RE = re.compile(r"\bamend(?:ed|ing|ment|ments)?\b", re.IGNORECASE)
REPEAL_RE = re.compile(r"\brepeal(?:ed|ing)?\b", re.IGNORECASE)
REDESIGNATE_RE = re.compile(r"\bredesignat(?:e|ed|ing|ion)\b", re.IGNORECASE)

FIELDNAMES = [
    "triage_rank",
    "source_scan_rank",
    "lineage_review_rank",
    "bill_id",
    "public_law_number",
    "target_reference",
    "target_reference_type",
    "candidate_snippet_count",
    "amendment_snippet_count",
    "repeal_snippet_count",
    "redesignation_snippet_count",
    "incomplete_fragment_count",
    "example_snippets",
    "govinfo_text_url",
    "codification_review_status",
    "lineage_evidence_status",
    "evidence_layers",
    "missing_links",
    "next_review_action",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_candidates(value: str) -> list[str]:
    return [candidate.strip() for candidate in value.split(";") if candidate.strip()]


def clean_section(value: str) -> str:
    value = re.sub(r"\s+", "", value)
    return value.strip(" .;,")


def direct_reference_status(reference_type: str, reference: str) -> str:
    if reference_type == "title_code_only":
        return "title_only_needs_manual_target"
    if reference.rstrip().endswith("-"):
        return "incomplete_reference_fragment_needs_manual_review"
    return "needs_olrc_us_code_note_review"


def extract_references(snippet: str) -> list[tuple[str, str, str]]:
    references: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    for match in PREC_USC_RE.finditer(snippet):
        section = clean_section(match.group("section"))
        if not section:
            continue
        reference = f"{match.group('title')} USC {section}"
        if reference not in seen:
            seen.add(reference)
            references.append((
                reference,
                "direct_us_code_prec_reference",
                direct_reference_status("direct_us_code_reference", reference),
            ))

    for match in TITLE_CODE_SECTION_RE.finditer(snippet):
        section = clean_section(match.group("section"))
        if not section:
            continue
        reference = f"{match.group('title')} USC {section}"
        if reference not in seen:
            seen.add(reference)
            references.append((reference, "title_code_section_phrase", direct_reference_status("title_code_section_phrase", reference)))

    for match in DIRECT_USC_RE.finditer(snippet):
        title = match.group("title")
        section = clean_section(match.group("section") or "")
        if section:
            if section.casefold().rstrip(".") == "prec":
                continue
            note_tail = snippet[match.end() : match.end() + 8].strip().casefold()
            suffix = " note" if note_tail.startswith("note") else ""
            reference = f"{title} USC {section}{suffix}"
            reference_type = "direct_us_code_reference"
        else:
            reference = f"{title} USC title-only"
            reference_type = "title_code_only"
        if reference not in seen:
            seen.add(reference)
            references.append((reference, reference_type, direct_reference_status(reference_type, reference)))
    return references


def empty_record(row: dict[str, str], reference: str, reference_type: str, status: str) -> dict[str, object]:
    return {
        "source_scan_rank": row["scan_rank"],
        "lineage_review_rank": row["lineage_review_rank"],
        "bill_id": row["bill_id"],
        "public_law_number": row["public_law_number"],
        "target_reference": reference,
        "target_reference_type": reference_type,
        "candidate_snippet_count": 0,
        "amendment_snippet_count": 0,
        "repeal_snippet_count": 0,
        "redesignation_snippet_count": 0,
        "incomplete_fragment_count": 0,
        "snippets": [],
        "govinfo_text_url": row["govinfo_text_url"],
        "codification_review_status": status,
    }


def add_snippet(record: dict[str, object], snippet: str, status: str) -> None:
    record["candidate_snippet_count"] = int(record["candidate_snippet_count"]) + 1
    if AMEND_RE.search(snippet):
        record["amendment_snippet_count"] = int(record["amendment_snippet_count"]) + 1
    if REPEAL_RE.search(snippet):
        record["repeal_snippet_count"] = int(record["repeal_snippet_count"]) + 1
    if REDESIGNATE_RE.search(snippet):
        record["redesignation_snippet_count"] = int(record["redesignation_snippet_count"]) + 1
    if status == "incomplete_reference_fragment_needs_manual_review":
        record["incomplete_fragment_count"] = int(record["incomplete_fragment_count"]) + 1
    snippets = record["snippets"]
    assert isinstance(snippets, list)
    if snippet not in snippets and len(snippets) < 4:
        snippets.append(snippet)


def build_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    records: dict[tuple[str, str, str], dict[str, object]] = {}
    for source_row in source_rows:
        candidates = split_candidates(source_row.get("target_section_candidates", ""))
        bill_had_reference = False
        for snippet in candidates:
            references = extract_references(snippet)
            if not references:
                continue
            bill_had_reference = True
            for reference, reference_type, status in references:
                key = (source_row["bill_id"], source_row["public_law_number"], reference)
                if key not in records:
                    records[key] = empty_record(source_row, reference, reference_type, status)
                record = records[key]
                if record["codification_review_status"] != status:
                    record["codification_review_status"] = "mixed_target_reference_needs_manual_review"
                add_snippet(record, snippet, status)
        if not bill_had_reference:
            if candidates:
                reference = "NO_STRUCTURED_USC_TARGET_FOUND"
                status = "source_scan_needs_manual_target_extraction"
            else:
                reference = "NO_TARGET_REFERENCE_FROM_SOURCE_SCAN"
                status = "source_scan_has_no_structured_usc_target"
            key = (source_row["bill_id"], source_row["public_law_number"], reference)
            record = empty_record(source_row, reference, "no_structured_target", status)
            for snippet in candidates[:4]:
                add_snippet(record, snippet, status)
            records[key] = record

    sorted_records = sorted(
        records.values(),
        key=lambda record: (
            int(str(record["source_scan_rank"])),
            1 if str(record["target_reference_type"]) == "no_structured_target" else 0,
            -int(record["candidate_snippet_count"]),
            str(record["target_reference"]),
        ),
    )
    rows: list[dict[str, str]] = []
    for index, record in enumerate(sorted_records, start=1):
        snippets = record["snippets"]
        assert isinstance(snippets, list)
        rows.append(
            {
                "triage_rank": str(index),
                "source_scan_rank": str(record["source_scan_rank"]),
                "lineage_review_rank": str(record["lineage_review_rank"]),
                "bill_id": str(record["bill_id"]),
                "public_law_number": str(record["public_law_number"]),
                "target_reference": str(record["target_reference"]),
                "target_reference_type": str(record["target_reference_type"]),
                "candidate_snippet_count": str(record["candidate_snippet_count"]),
                "amendment_snippet_count": str(record["amendment_snippet_count"]),
                "repeal_snippet_count": str(record["repeal_snippet_count"]),
                "redesignation_snippet_count": str(record["redesignation_snippet_count"]),
                "incomplete_fragment_count": str(record["incomplete_fragment_count"]),
                "example_snippets": " || ".join(str(snippet).replace("|", "/") for snippet in snippets),
                "govinfo_text_url": str(record["govinfo_text_url"]),
                "codification_review_status": str(record["codification_review_status"]),
                "lineage_evidence_status": "target_section_triage_not_codified_lineage_evidence",
                "evidence_layers": "; ".join(EVIDENCE_LAYERS),
                "missing_links": "; ".join(MISSING_LINKS),
                "next_review_action": NEXT_REVIEW_ACTION,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], source_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["codification_review_status"] for row in rows)
    reference_type_counts = Counter(row["target_reference_type"] for row in rows)
    represented_bills = {row["bill_id"] for row in rows}
    structured_rows = [
        row
        for row in rows
        if row["target_reference_type"] != "no_structured_target"
        and not row["target_reference"].startswith("NO_")
    ]
    snippets_represented = sum(int(row["candidate_snippet_count"]) for row in rows)
    lines = [
        "# Statutory Lineage Target-Section Triage",
        "",
        "This report normalizes candidate U.S.C. target references from the official GovInfo public-law source scan. It is a review queue, not codified-lineage evidence.",
        "",
        f"- Target-section triage rows: {len(rows)}",
        f"- Bills covered: {len(represented_bills)} / {len(source_rows)}",
        f"- Structured U.S.C. target rows: {len(structured_rows)}",
        f"- Candidate snippets represented: {snippets_represented}",
        "",
        "Codification review statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Target reference types:")
    for reference_type, count in sorted(reference_type_counts.items()):
        lines.append(f"- {reference_type}: {count}")
    lines.extend(
        [
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "| Rank | Bill | Public law | Target reference | Type | Snippets | Status |",
            "| ---: | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    display_rows = rows[:80]
    for row in display_rows:
        lines.append(
            f"| {row['triage_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['target_reference_type']} | "
            f"{row['candidate_snippet_count']} | {row['codification_review_status']} |"
        )
    if len(display_rows) < len(rows):
        lines.extend(
            [
                "",
                f"CSV contains {len(rows) - len(display_rows)} additional triage rows not shown in the markdown table.",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not SOURCE_SCAN.exists():
        raise SystemExit(f"{SOURCE_SCAN} is missing; run make statutory-lineage-source-scan first.")
    source_rows = read_csv(SOURCE_SCAN)
    if not source_rows:
        raise SystemExit(f"{SOURCE_SCAN} is empty.")
    rows = build_rows(source_rows)
    if not rows:
        raise SystemExit("No statutory-lineage target-section triage rows generated.")
    write_csv(rows)
    write_md(rows, source_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
