#!/usr/bin/env python3
"""Write a statutory-lineage source-review queue from lifecycle next actions."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
SPINE = Path("reports/bill-law-evidence-spine.csv")
LAW_REVISION_HISTORY = Path("data/validation/raw/law_revision_history.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("reports/statutory-lineage-review-queue.csv")
OUT_MD = Path("reports/statutory-lineage-review-queue.md")

REVISION_FLAG_FIELDS = [
    "amended",
    "reauthorized",
    "repealed",
    "expired",
    "invalidated",
]

SOURCE_REVIEW_TARGETS = [
    "public_law_text",
    "us_code_notes",
    "olrc_us_code_classification",
    "govinfo_uslm_or_statutes_at_large",
    "ecfr_or_cfr_authority_if_applicable",
]

MISSING_LINKS = [
    "codified_usc_lineage",
    "amended_section_identifier",
    "target_section_diff",
    "law_revision_effective_text",
    "source_reviewed_statutory_lineage",
    "model_validation",
]

FIELDNAMES = [
    "lineage_review_rank",
    "action_rank",
    "base_review_priority_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "enacted_date",
    "bill_title",
    "revision_flags",
    "revision_terms",
    "law_revision_summary_count",
    "law_revision_title_count",
    "bill_actions_count",
    "committee_reported",
    "floor_considered",
    "authority_document_count",
    "authority_document_numbers",
    "authority_usc_citation_count",
    "authority_usc_citations",
    "proposed_rule_document_count",
    "proposed_rule_document_numbers",
    "regulations_docket_count",
    "regulations_docket_ids",
    "court_case_count",
    "court_case_ids",
    "court_usc_section_count",
    "court_usc_sections",
    "court_direct_review_status",
    "closed_review_gates",
    "lineage_review_status",
    "source_review_targets",
    "next_review_action",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Statutory-lineage source-review queue only; not statutory-lineage evidence. "
    "This report preserves bill/action, revision-text proxy, Federal Register "
    "authority, proposed-rule, court-overlap, and direct-review disposition "
    "pointers for source review, but it does not establish codified U.S.C. "
    "lineage, amended target sections, text diffs, implementation outcomes, "
    "direct court review, causal effects, welfare, or model validation."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def ordered_union(*groups: list[str]) -> list[str]:
    values: list[str] = []
    for group in groups:
        for value in group:
            if value and value not in values:
                values.append(value)
    return values


def count_values(value: str) -> int:
    return len(split_values(value))


def by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {
        row.get(key, "").strip(): row
        for row in rows
        if row.get(key, "").strip()
    }


def revision_flags(history_row: dict[str, str]) -> list[str]:
    flags = [
        field
        for field in REVISION_FLAG_FIELDS
        if history_row.get(field, "").strip() == "1"
    ]
    return flags or ["none"]


def build_rows() -> list[dict[str, str]]:
    next_actions = read_csv(NEXT_ACTIONS)
    spine_rows = read_csv(SPINE)
    history_rows = read_csv(LAW_REVISION_HISTORY)
    linkage_rows = read_csv(LAW_REVISION_BILL_LINKAGE)
    if not next_actions:
        raise SystemExit(f"{NEXT_ACTIONS} is missing or empty; run make bill-law-lifecycle-next-actions first.")
    if not spine_rows:
        raise SystemExit(f"{SPINE} is missing or empty; run make bill-law-evidence-spine first.")
    if not history_rows:
        raise SystemExit(f"{LAW_REVISION_HISTORY} is missing or empty; run make build-law-revision-raw first.")
    if not linkage_rows:
        raise SystemExit(
            f"{LAW_REVISION_BILL_LINKAGE} is missing or empty; run make build-law-revision-bill-linkage-raw first."
        )

    spine_by_bill = by_key(spine_rows, "bill_id")
    history_by_public_law = by_key(history_rows, "public_law_number")
    linkage_by_bill = by_key(linkage_rows, "bill_id")

    candidates = [
        row for row in next_actions
        if row.get("next_actionable_upgrade_gate", "").strip() == "codified_usc_lineage"
    ]
    candidates.sort(key=lambda row: int(row.get("action_rank", "999999") or "999999"))

    rows: list[dict[str, str]] = []
    for index, action_row in enumerate(candidates, start=1):
        bill_id = action_row.get("bill_id", "").strip()
        public_law = action_row.get("public_law_number", "").strip()
        spine_row = spine_by_bill.get(bill_id, {})
        history_row = history_by_public_law.get(public_law, {})
        linkage_row = linkage_by_bill.get(bill_id, {})

        authority_docs = spine_row.get("implementation_authority_document_numbers", "")
        authority_usc = spine_row.get("implementation_authority_usc_citations", "")
        proposed_docs = spine_row.get("implementation_history_proposed_document_numbers", "")
        dockets = spine_row.get("implementation_history_proposed_regulations_docket_ids", "")
        court_cases = spine_row.get("court_review_case_ids", "")
        court_sections = spine_row.get("court_review_usc_sections", "")

        evidence_layers = ordered_union(
            [
                "statutory_lineage_review_queue",
                "bill_law_lifecycle_next_actions",
                "bill_law_evidence_spine",
            ],
            split_values(spine_row.get("evidence_layers", "")),
        )
        missing_links = ordered_union(
            MISSING_LINKS,
            split_values(spine_row.get("missing_links", "")),
        )

        rows.append({
            "lineage_review_rank": str(index),
            "action_rank": action_row.get("action_rank", ""),
            "base_review_priority_rank": action_row.get("base_review_priority_rank", ""),
            "bill_id": bill_id,
            "public_law_number": public_law,
            "policy_area": action_row.get("policy_area", ""),
            "enacted_date": history_row.get("enacted_date", linkage_row.get("enacted_date", "")),
            "bill_title": history_row.get("bill_title", ""),
            "revision_flags": "; ".join(revision_flags(history_row)),
            "revision_terms": history_row.get("revision_terms", ""),
            "law_revision_summary_count": history_row.get("summary_count", ""),
            "law_revision_title_count": history_row.get("title_count", ""),
            "bill_actions_count": linkage_row.get("actions_count", spine_row.get("actions_count", "")),
            "committee_reported": linkage_row.get("committee_reported", spine_row.get("committee_reported", "")),
            "floor_considered": linkage_row.get("floor_considered", spine_row.get("floor_considered", "")),
            "authority_document_count": str(count_values(authority_docs)),
            "authority_document_numbers": authority_docs,
            "authority_usc_citation_count": str(count_values(authority_usc)),
            "authority_usc_citations": authority_usc,
            "proposed_rule_document_count": str(count_values(proposed_docs)),
            "proposed_rule_document_numbers": proposed_docs,
            "regulations_docket_count": str(count_values(dockets)),
            "regulations_docket_ids": dockets,
            "court_case_count": str(count_values(court_cases)),
            "court_case_ids": court_cases,
            "court_usc_section_count": str(count_values(court_sections)),
            "court_usc_sections": court_sections,
            "court_direct_review_status": action_row.get("court_direct_review_status", ""),
            "closed_review_gates": action_row.get("closed_review_gates", ""),
            "lineage_review_status": "needs_codified_usc_lineage_source_review",
            "source_review_targets": "; ".join(SOURCE_REVIEW_TARGETS),
            "next_review_action": (
                "Review public-law text, OLRC/govinfo codification tables, and "
                "U.S. Code notes for amended or newly enacted sections; record "
                "target-section identifiers and text-diff status before using "
                "this row as statutory-lineage evidence."
            ),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "source_url": history_row.get("source_url", linkage_row.get("source_url", "")),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    flags = Counter()
    for row in rows:
        for flag in split_values(row["revision_flags"]):
            flags[flag] += 1
    rows_with_revision_flags = sum(
        1 for row in rows
        if split_values(row["revision_flags"]) != ["none"]
    )
    rows_with_authority_docs = sum(1 for row in rows if int(row["authority_document_count"]) > 0)
    rows_with_authority_usc = sum(1 for row in rows if int(row["authority_usc_citation_count"]) > 0)
    rows_with_proposed_docs = sum(1 for row in rows if int(row["proposed_rule_document_count"]) > 0)
    rows_with_dockets = sum(1 for row in rows if int(row["regulations_docket_count"]) > 0)
    rows_with_closed_court_gates = sum(1 for row in rows if row["closed_review_gates"].strip())

    lines = [
        "# Statutory Lineage Review Queue",
        "",
        "This source-review queue isolates public-law rows whose next lifecycle gate is codified U.S.C. lineage. It is not statutory-lineage evidence.",
        "",
        f"- Lineage review rows: {len(rows)}",
        f"- Rows with revision flags: {rows_with_revision_flags}",
        f"- Rows with authority documents: {rows_with_authority_docs}",
        f"- Rows with authority U.S.C. citations: {rows_with_authority_usc}",
        f"- Rows with proposed-rule documents: {rows_with_proposed_docs}",
        f"- Rows with Regulations.gov dockets: {rows_with_dockets}",
        f"- Rows with closed court direct-review gates: {rows_with_closed_court_gates}",
        "",
        "Revision flag counts:",
    ]
    for flag, count in sorted(flags.items()):
        lines.append(f"- {flag}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Revision flags | Authority docs | U.S.C. citations | Court status | Next action |",
        "| ---: | --- | --- | --- | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['lineage_review_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['revision_flags']} | {row['authority_document_count']} | "
            f"{row['authority_usc_citation_count']} | `{row['court_direct_review_status']}` | "
            "source review |"
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
