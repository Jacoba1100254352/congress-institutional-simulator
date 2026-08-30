#!/usr/bin/env python3
"""Bridge reviewed target-section diffs to bounded lifecycle context."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


TARGET_DIFF_REVIEW = Path("reports/statutory-lineage-target-section-diff-review.csv")
RULEMAKING_AUTHORITY = Path("data/validation/raw/rulemaking_authority_linkage.csv")
RULEMAKING_HISTORY = Path("data/validation/raw/rulemaking_history_linkage.csv")
RULEMAKING_COMMENT_METADATA = Path("data/validation/raw/rulemaking_comment_metadata.csv")
COURT_REVIEW = Path("data/validation/raw/court_review.csv")
COURT_LAW_LINKAGE = Path("data/validation/raw/court_law_linkage.csv")
COURT_PUBLIC_LAW_DIRECT_REVIEW = Path("reports/court-public-law-direct-review.csv")
BILL_LAW_SPINE = Path("reports/bill-law-evidence-spine.csv")
OUT_CSV = Path("reports/statutory-lineage-target-lifecycle-bridge.csv")
OUT_MD = Path("reports/statutory-lineage-target-lifecycle-bridge.md")

USC_PATTERN = re.compile(
    r"\b(?P<title>\d+)\s+U\.?\s*S\.?\s*C\.?\s*(?:§+\s*)?(?P<section>[0-9A-Za-z][0-9A-Za-z-]*)",
    re.IGNORECASE,
)
SUBSECTION_TOKEN_PATTERN = re.compile(r"\A\s*\(([0-9A-Za-z]+)\)?")

CLAIM_BOUNDARY = (
    "Target-section lifecycle bridge only; base U.S.C. section overlaps are "
    "metadata context and are not exact target-reference or subsection evidence. "
    "Raw SCDB target-section overlaps are date-screened section-citation context "
    "and do not prove review of the queued public law, bill, note, or subsection. "
    "Public-law-level rows remain context. This artifact does not establish "
    "implementation outcomes, direct court review of the target section, "
    "public-law causal attribution, law-revision effective text, welfare, causal "
    "effects, or model validation."
)

FIELDNAMES = [
    "bridge_rank",
    "review_rank",
    "target_review_packet_rank",
    "bill_id",
    "public_law_number",
    "enacted_date",
    "target_reference",
    "target_reference_type",
    "target_section_key",
    "target_base_section_key",
    "target_subsection",
    "target_reference_key",
    "normalized_title",
    "normalized_section",
    "target_is_note",
    "review_status",
    "source_reviewed_target_section_diff",
    "codified_lineage_relationship",
    "target_lifecycle_status",
    "bridge_evidence_grade",
    "authority_base_section_match",
    "authority_base_section_citations",
    "authority_exact_target_reference_match",
    "authority_exact_target_reference_citations",
    "public_law_authority_rule_rows",
    "public_law_authority_text_verified_rows",
    "public_law_authority_document_numbers",
    "public_law_authority_usc_citation_count",
    "implementation_history_final_rule_rows",
    "implementation_history_matched_final_rule_rows",
    "implementation_history_proposed_rule_links",
    "implementation_history_proposed_document_numbers",
    "implementation_comment_metadata_rows",
    "implementation_comment_metadata_statuses",
    "implementation_comment_metadata_final_comment_count_rows",
    "implementation_comment_metadata_final_comment_count_total",
    "implementation_comment_metadata_proposed_comment_url_count",
    "implementation_comment_metadata_proposed_comment_urls",
    "court_base_section_overlap",
    "court_base_section_overlap_case_count",
    "court_base_section_overlap_case_ids",
    "court_base_section_overlap_usc_sections",
    "court_exact_target_reference_overlap",
    "court_exact_target_reference_case_count",
    "court_exact_target_reference_case_ids",
    "raw_scdb_target_base_section_overlap",
    "raw_scdb_target_base_section_case_count",
    "raw_scdb_target_base_section_case_ids",
    "raw_scdb_target_base_section_usc_sections",
    "raw_scdb_target_base_section_pre_enactment_case_count",
    "raw_scdb_target_base_section_post_enactment_case_count",
    "raw_scdb_target_base_section_missing_date_case_count",
    "raw_scdb_target_base_section_decision_range",
    "raw_scdb_target_reference_overlap",
    "raw_scdb_target_reference_case_count",
    "raw_scdb_target_reference_case_ids",
    "raw_scdb_target_reference_post_enactment_case_count",
    "public_law_court_overlap_case_count",
    "public_law_court_overlap_case_ids",
    "public_law_court_overlap_usc_sections",
    "public_law_direct_review_rows",
    "public_law_direct_review_direct_rows",
    "public_law_direct_review_not_direct_rows",
    "public_law_direct_review_determinations",
    "spine_evidence_layers",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


@dataclass(frozen=True)
class UscReference:
    title: str
    section: str
    subsection: str
    note: bool
    chunk: str

    @property
    def base_key(self) -> tuple[str, str, bool]:
        return (self.title, self.section, self.note)

    @property
    def exact_key(self) -> tuple[str, str, bool, str]:
        return (self.title, self.section, self.note, self.subsection)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; run the upstream validation target first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


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


def is_note_reference(reference: str, reference_type: str = "") -> bool:
    text = f"{reference} {reference_type}".casefold()
    return " note" in f" {text}" or text.endswith("note")


def parse_leading_subsection_tail(tail: str) -> str:
    tokens: list[str] = []
    remaining = tail
    while True:
        match = SUBSECTION_TOKEN_PATTERN.match(remaining)
        if not match:
            break
        tokens.append(f"({match.group(1)})")
        remaining = remaining[match.end():]
    return "".join(tokens)


def target_base_key(row: dict[str, str]) -> tuple[str, str, bool]:
    title = row.get("normalized_title", "").strip()
    section = row.get("normalized_section", "").strip()
    if not title or not section:
        raise SystemExit(f"{TARGET_DIFF_REVIEW}: target row missing normalized title/section.")
    return (
        title,
        section,
        is_note_reference(row.get("target_reference", ""), row.get("target_reference_type", "")),
    )


def target_section_pair(row: dict[str, str]) -> tuple[str, str]:
    title, section, _note = target_base_key(row)
    return title, section


def target_subsection(row: dict[str, str]) -> str:
    reference = row.get("target_reference", "")
    expected_title = row.get("normalized_title", "").strip()
    expected_section = row.get("normalized_section", "").strip()
    for match in USC_PATTERN.finditer(reference):
        title = match.group("title").strip()
        section = match.group("section").strip().rstrip(".,;:")
        if title == expected_title and section == expected_section:
            return parse_leading_subsection_tail(reference[match.end():])
    return ""


def target_exact_key(row: dict[str, str]) -> tuple[str, str, bool, str]:
    base_key = target_base_key(row)
    return (*base_key, target_subsection(row))


def format_base_key(key: tuple[str, str, bool]) -> str:
    title, section, note = key
    suffix = " note" if note else ""
    return f"{title} USC {section}{suffix}"


def format_exact_key(key: tuple[str, str, bool, str]) -> str:
    title, section, note, subsection = key
    suffix = " note" if note else ""
    return f"{title} USC {section}{subsection}{suffix}"


def iter_usc_refs(value: str) -> list[UscReference]:
    refs: list[UscReference] = []
    for chunk in split_values(value):
        for match in USC_PATTERN.finditer(chunk):
            title = match.group("title").strip()
            section = match.group("section").strip().rstrip(".,;:")
            tail = chunk[match.end():]
            note = bool(re.match(r"\s*note\b", tail, re.IGNORECASE))
            refs.append(UscReference(
                title=title,
                section=section,
                subsection=parse_leading_subsection_tail(tail),
                note=note,
                chunk=chunk,
            ))
    return refs


def indexed_usc_refs(value: str) -> tuple[
    dict[tuple[str, str, bool], list[str]],
    dict[tuple[str, str, bool, str], list[str]],
]:
    by_base: dict[tuple[str, str, bool], list[str]] = defaultdict(list)
    by_exact: dict[tuple[str, str, bool, str], list[str]] = defaultdict(list)
    for ref in iter_usc_refs(value):
        by_base[ref.base_key].append(ref.chunk)
        by_exact[ref.exact_key].append(ref.chunk)
    return by_base, by_exact


def unique_join(values: list[str] | set[str]) -> str:
    return "; ".join(sorted({value.strip() for value in values if value and value.strip()}))


def parse_source_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except (TypeError, ValueError):
            continue
    return None


def format_decision_range(rows: list[dict[str, str]]) -> str:
    dates = [
        parsed
        for row in rows
        if (parsed := parse_source_date(row.get("decision_date", ""))) is not None
    ]
    if not dates:
        return ""
    return f"{min(dates).isoformat()}..{max(dates).isoformat()}"


def by_public_law(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        public_law = row.get("public_law_number", "").strip()
        if public_law:
            result[public_law].append(row)
    return result


def raw_court_indexes(
    rows: list[dict[str, str]],
) -> tuple[
    dict[tuple[str, str], list[dict[str, str]]],
    dict[tuple[str, str, bool, str], list[dict[str, str]]],
]:
    by_base: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    by_exact: dict[tuple[str, str, bool, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if not row.get("case_id", "").strip():
            continue
        for ref in iter_usc_refs(row.get("usc_sections", "")):
            by_base[(ref.title, ref.section)].append(row)
            by_exact[ref.exact_key].append(row)
    return by_base, by_exact


def court_by_public_law(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("linkage_status") != "usc_section_authority_overlap":
            continue
        for public_law in split_values(row.get("public_law_numbers", "")):
            result[public_law].append(row)
    return result


def status_for_row(
    review_row: dict[str, str],
    authority_base: bool,
    authority_exact: bool,
    court_base: bool,
    court_exact: bool,
    public_law_context: bool,
) -> tuple[str, str]:
    if review_row.get("review_status", "").strip() == "reviewed_related_section_context_no_exact_target_diff":
        return "reviewed_related_section_context_no_exact_target_diff", "reviewed_no_exact_target_diff"
    if review_row.get("source_reviewed_target_section_diff", "").strip() != "1":
        return "reviewed_target_diff_unresolved", "unresolved_review"
    if authority_exact and court_exact:
        return (
            "target_diff_with_exact_authority_and_court_target_reference_context",
            "exact_target_reference_context",
        )
    if authority_exact:
        return "target_diff_with_exact_authority_target_reference_context", "exact_target_reference_context"
    if court_exact:
        return "target_diff_with_exact_court_target_reference_overlap", "exact_target_reference_context"
    if authority_base and court_base:
        return "target_diff_with_authority_and_court_base_section_context", "base_section_context"
    if authority_base:
        return "target_diff_with_authority_base_section_context", "base_section_context"
    if court_base:
        return "target_diff_with_court_base_section_context", "base_section_context"
    if public_law_context:
        return "target_diff_with_public_law_lifecycle_context_only", "public_law_context_only"
    return "target_diff_without_lifecycle_context", "no_lifecycle_context"


def build_rows() -> list[dict[str, str]]:
    target_rows = read_csv(TARGET_DIFF_REVIEW)
    if not target_rows:
        raise SystemExit(f"{TARGET_DIFF_REVIEW} is empty.")

    authority_by_pl = {
        row.get("public_law_number", "").strip(): row
        for row in read_csv(RULEMAKING_AUTHORITY)
        if row.get("public_law_number", "").strip()
    }
    history_by_pl = by_public_law(read_csv(RULEMAKING_HISTORY))
    comment_by_pl = by_public_law(read_csv(RULEMAKING_COMMENT_METADATA))
    raw_court_by_base, raw_court_by_exact = raw_court_indexes(read_csv(COURT_REVIEW))
    court_rows_by_pl = court_by_public_law(read_csv(COURT_LAW_LINKAGE))
    direct_review_by_pl = by_public_law(read_csv(COURT_PUBLIC_LAW_DIRECT_REVIEW))
    spine_by_pl = {
        row.get("public_law_number", "").strip(): row
        for row in read_csv(BILL_LAW_SPINE)
        if row.get("public_law_number", "").strip()
    }

    rows: list[dict[str, str]] = []
    for index, review in enumerate(
        sorted(target_rows, key=lambda row: int_field(row, "review_rank")),
        start=1,
    ):
        public_law = review.get("public_law_number", "").strip()
        base_key = target_base_key(review)
        section_pair = target_section_pair(review)
        exact_key = target_exact_key(review)
        enacted = parse_source_date(review.get("enacted_date", ""))
        authority = authority_by_pl.get(public_law, {})
        authority_refs_by_base, authority_refs_by_exact = indexed_usc_refs(authority.get("usc_citations", ""))
        authority_base_citations = authority_refs_by_base.get(base_key, [])
        authority_exact_citations = authority_refs_by_exact.get(exact_key, [])
        history_rows = history_by_pl.get(public_law, [])
        history_match_rows = [
            row for row in history_rows
            if row.get("history_status", "").strip() == "proposed_rule_history_match"
        ]
        proposed_documents = [
            document
            for row in history_match_rows
            for document in split_values(row.get("proposed_document_numbers", ""))
        ]
        proposed_rule_links = sum(int_field(row, "matched_proposed_rule_count") for row in history_rows)
        comment_rows = comment_by_pl.get(public_law, [])
        comment_statuses = [
            row.get("comment_metadata_status", "").strip()
            for row in comment_rows
            if row.get("comment_metadata_status", "").strip()
        ]
        comment_final_counts = [
            int_field(row, "final_regulations_comments_count")
            for row in comment_rows
            if row.get("final_regulations_comments_count", "").strip()
        ]
        proposed_comment_urls = [
            url
            for row in comment_rows
            for url in split_values(row.get("proposed_regulations_comments_urls_refetched", ""))
        ]
        court_rows = court_rows_by_pl.get(public_law, [])
        court_base_rows = [
            row for row in court_rows
            if base_key in indexed_usc_refs(row.get("matched_usc_sections", ""))[0]
        ]
        court_exact_rows = [
            row for row in court_rows
            if exact_key in indexed_usc_refs(row.get("matched_usc_sections", ""))[1]
        ]
        public_law_court_cases = [
            row.get("case_id", "").strip()
            for row in court_rows
            if row.get("case_id", "").strip()
        ]
        court_base_cases = [
            row.get("case_id", "").strip()
            for row in court_base_rows
            if row.get("case_id", "").strip()
        ]
        court_exact_cases = [
            row.get("case_id", "").strip()
            for row in court_exact_rows
            if row.get("case_id", "").strip()
        ]
        raw_base_rows = raw_court_by_base.get(section_pair, [])
        raw_exact_rows = raw_court_by_exact.get(exact_key, [])
        raw_base_cases = [
            row.get("case_id", "").strip()
            for row in raw_base_rows
            if row.get("case_id", "").strip()
        ]
        raw_exact_cases = [
            row.get("case_id", "").strip()
            for row in raw_exact_rows
            if row.get("case_id", "").strip()
        ]
        raw_base_sections = [
            section
            for row in raw_base_rows
            for section in split_values(row.get("usc_sections", ""))
        ]
        raw_base_pre_rows = [
            row for row in raw_base_rows
            if (decision := parse_source_date(row.get("decision_date", ""))) is not None
            and enacted is not None
            and decision < enacted
        ]
        raw_base_post_rows = [
            row for row in raw_base_rows
            if (decision := parse_source_date(row.get("decision_date", ""))) is not None
            and enacted is not None
            and decision >= enacted
        ]
        raw_base_missing_date_rows = [
            row for row in raw_base_rows
            if parse_source_date(row.get("decision_date", "")) is None or enacted is None
        ]
        raw_exact_post_rows = [
            row for row in raw_exact_rows
            if (decision := parse_source_date(row.get("decision_date", ""))) is not None
            and enacted is not None
            and decision >= enacted
        ]
        court_base_sections = [
            section
            for row in court_base_rows
            for section in split_values(row.get("matched_usc_sections", ""))
        ]
        public_law_court_sections = [
            section
            for row in court_rows
            for section in split_values(row.get("matched_usc_sections", ""))
        ]
        direct_rows = direct_review_by_pl.get(public_law, [])
        direct_determinations = [
            row.get("direct_review_determination", "").strip()
            for row in direct_rows
            if row.get("direct_review_determination", "").strip()
        ]
        direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_case_to_public_law_identifier", "").strip() == "1"
        )
        not_direct_count = sum(
            1 for row in direct_rows
            if row.get("direct_case_to_public_law_identifier", "").strip() == "0"
        )
        public_law_context = bool(
            int_field(authority, "text_verified_rule_count") > 0
            or history_rows
            or comment_rows
            or court_rows
            or direct_rows
        )
        lifecycle_status, evidence_grade = status_for_row(
            review,
            bool(authority_base_citations),
            bool(authority_exact_citations),
            bool(court_base_rows),
            bool(court_exact_rows),
            public_law_context,
        )
        evidence_layers = ["statutory_lineage_target_section_diff_review"]
        if review.get("source_reviewed_target_section_diff", "").strip() == "1":
            evidence_layers.append("statutory_lineage_source_reviewed_target_section_diff")
        if int_field(authority, "text_verified_rule_count") > 0:
            evidence_layers.append("public_law_federal_register_authority_context")
        if authority_base_citations:
            evidence_layers.append("target_base_section_authority_usc_overlap")
        if authority_exact_citations:
            evidence_layers.append("target_reference_authority_usc_overlap")
        if history_rows:
            evidence_layers.append("public_law_rulemaking_history_context")
        if comment_rows:
            evidence_layers.append("public_law_federal_register_comment_metadata_context")
        if court_rows:
            evidence_layers.append("public_law_court_usc_section_overlap_context")
        if court_base_rows:
            evidence_layers.append("target_base_section_court_usc_overlap")
        if court_exact_rows:
            evidence_layers.append("target_reference_court_usc_overlap")
        if raw_base_rows:
            evidence_layers.append("raw_scdb_target_base_section_overlap_context")
        if raw_exact_rows:
            evidence_layers.append("raw_scdb_target_reference_overlap_context")
        if raw_base_post_rows or raw_exact_post_rows:
            evidence_layers.append("raw_scdb_post_enactment_target_section_overlap_needs_source_review")
        if direct_rows:
            evidence_layers.append("court_public_law_direct_review_disposition")
        if public_law in spine_by_pl:
            evidence_layers.append("bill_law_evidence_spine_context")

        missing_links = [
            "public_law_causal_attribution",
            "law_revision_effective_text",
            "complete_codified_usc_lineage_review",
            "complete_regulations_comments",
            "implementation_outcomes_or_enforcement",
            "direct_court_review_of_target_section",
            "welfare_or_public_benefit",
            "model_validation",
        ]
        if not authority_exact_citations:
            missing_links.append("exact_target_reference_implementation_authority")
        if not court_exact_rows:
            missing_links.append("exact_target_reference_court_overlap")
        if raw_base_rows:
            missing_links.append("source_reviewed_raw_scdb_target_section_disposition")
        if raw_base_post_rows or raw_exact_post_rows:
            missing_links.append("source_reviewed_post_enactment_target_section_court_disposition")
        if direct_count == 0:
            missing_links.append("direct_case_to_public_law_identifier")
        if not public_law_context:
            missing_links.append("public_law_lifecycle_context")
        if review.get("source_reviewed_target_section_diff", "").strip() != "1":
            missing_links.append("source_reviewed_target_section_diff")

        authority_usc_count = len(authority_refs_by_base)
        rows.append({
            "bridge_rank": str(index),
            "review_rank": review.get("review_rank", "").strip(),
            "target_review_packet_rank": review.get("target_review_packet_rank", "").strip(),
            "bill_id": review.get("bill_id", "").strip(),
            "public_law_number": public_law,
            "enacted_date": review.get("enacted_date", "").strip(),
            "target_reference": review.get("target_reference", "").strip(),
            "target_reference_type": review.get("target_reference_type", "").strip(),
            "target_section_key": format_base_key(base_key),
            "target_base_section_key": format_base_key(base_key),
            "target_subsection": exact_key[3],
            "target_reference_key": format_exact_key(exact_key),
            "normalized_title": base_key[0],
            "normalized_section": base_key[1],
            "target_is_note": "1" if base_key[2] else "0",
            "review_status": review.get("review_status", "").strip(),
            "source_reviewed_target_section_diff": review.get("source_reviewed_target_section_diff", "").strip(),
            "codified_lineage_relationship": review.get("codified_lineage_relationship", "").strip(),
            "target_lifecycle_status": lifecycle_status,
            "bridge_evidence_grade": evidence_grade,
            "authority_base_section_match": "1" if authority_base_citations else "0",
            "authority_base_section_citations": unique_join(authority_base_citations),
            "authority_exact_target_reference_match": "1" if authority_exact_citations else "0",
            "authority_exact_target_reference_citations": unique_join(authority_exact_citations),
            "public_law_authority_rule_rows": authority.get("matched_rule_count", "0"),
            "public_law_authority_text_verified_rows": authority.get("text_verified_rule_count", "0"),
            "public_law_authority_document_numbers": authority.get("matched_document_numbers", ""),
            "public_law_authority_usc_citation_count": str(authority_usc_count),
            "implementation_history_final_rule_rows": str(len(history_rows)),
            "implementation_history_matched_final_rule_rows": str(len(history_match_rows)),
            "implementation_history_proposed_rule_links": str(proposed_rule_links),
            "implementation_history_proposed_document_numbers": unique_join(proposed_documents),
            "implementation_comment_metadata_rows": str(len(comment_rows)),
            "implementation_comment_metadata_statuses": unique_join(comment_statuses),
            "implementation_comment_metadata_final_comment_count_rows": str(len(comment_final_counts)),
            "implementation_comment_metadata_final_comment_count_total": str(sum(comment_final_counts)),
            "implementation_comment_metadata_proposed_comment_url_count": str(len(set(proposed_comment_urls))),
            "implementation_comment_metadata_proposed_comment_urls": unique_join(proposed_comment_urls),
            "court_base_section_overlap": "1" if court_base_rows else "0",
            "court_base_section_overlap_case_count": str(len(set(court_base_cases))),
            "court_base_section_overlap_case_ids": unique_join(court_base_cases),
            "court_base_section_overlap_usc_sections": unique_join(court_base_sections),
            "court_exact_target_reference_overlap": "1" if court_exact_rows else "0",
            "court_exact_target_reference_case_count": str(len(set(court_exact_cases))),
            "court_exact_target_reference_case_ids": unique_join(court_exact_cases),
            "raw_scdb_target_base_section_overlap": "1" if raw_base_rows else "0",
            "raw_scdb_target_base_section_case_count": str(len(set(raw_base_cases))),
            "raw_scdb_target_base_section_case_ids": unique_join(raw_base_cases),
            "raw_scdb_target_base_section_usc_sections": unique_join(raw_base_sections),
            "raw_scdb_target_base_section_pre_enactment_case_count": str(len(set(
                row.get("case_id", "").strip()
                for row in raw_base_pre_rows
                if row.get("case_id", "").strip()
            ))),
            "raw_scdb_target_base_section_post_enactment_case_count": str(len(set(
                row.get("case_id", "").strip()
                for row in raw_base_post_rows
                if row.get("case_id", "").strip()
            ))),
            "raw_scdb_target_base_section_missing_date_case_count": str(len(set(
                row.get("case_id", "").strip()
                for row in raw_base_missing_date_rows
                if row.get("case_id", "").strip()
            ))),
            "raw_scdb_target_base_section_decision_range": format_decision_range(raw_base_rows),
            "raw_scdb_target_reference_overlap": "1" if raw_exact_rows else "0",
            "raw_scdb_target_reference_case_count": str(len(set(raw_exact_cases))),
            "raw_scdb_target_reference_case_ids": unique_join(raw_exact_cases),
            "raw_scdb_target_reference_post_enactment_case_count": str(len(set(
                row.get("case_id", "").strip()
                for row in raw_exact_post_rows
                if row.get("case_id", "").strip()
            ))),
            "public_law_court_overlap_case_count": str(len(set(public_law_court_cases))),
            "public_law_court_overlap_case_ids": unique_join(public_law_court_cases),
            "public_law_court_overlap_usc_sections": unique_join(public_law_court_sections),
            "public_law_direct_review_rows": str(len(direct_rows)),
            "public_law_direct_review_direct_rows": str(direct_count),
            "public_law_direct_review_not_direct_rows": str(not_direct_count),
            "public_law_direct_review_determinations": unique_join(direct_determinations),
            "spine_evidence_layers": spine_by_pl.get(public_law, {}).get("evidence_layers", ""),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
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
    status_counts = Counter(row["target_lifecycle_status"] for row in rows)
    grade_counts = Counter(row["bridge_evidence_grade"] for row in rows)
    public_laws = {row["public_law_number"] for row in rows}
    authority_base_rows = [row for row in rows if row["authority_base_section_match"] == "1"]
    authority_exact_rows = [row for row in rows if row["authority_exact_target_reference_match"] == "1"]
    court_base_rows = [row for row in rows if row["court_base_section_overlap"] == "1"]
    court_exact_rows = [row for row in rows if row["court_exact_target_reference_overlap"] == "1"]
    raw_scdb_base_rows = [row for row in rows if row["raw_scdb_target_base_section_overlap"] == "1"]
    raw_scdb_exact_rows = [row for row in rows if row["raw_scdb_target_reference_overlap"] == "1"]
    raw_scdb_post_enactment_attachments = sum(
        int(row["raw_scdb_target_base_section_post_enactment_case_count"] or "0")
        for row in rows
    )
    raw_scdb_case_ids = {
        case_id
        for row in rows
        for case_id in split_values(row["raw_scdb_target_base_section_case_ids"])
    }
    public_law_context_rows = [
        row for row in rows
        if row["bridge_evidence_grade"] in {
            "exact_target_reference_context",
            "base_section_context",
            "public_law_context_only",
        }
    ]
    direct_review_attachments = sum(int(row["public_law_direct_review_rows"] or "0") for row in rows)
    unique_direct_review_rows = {
        (row["public_law_number"], case_id)
        for row in rows
        for case_id in split_values(row["public_law_court_overlap_case_ids"])
        if int(row["public_law_direct_review_rows"] or "0") > 0
    }
    lines = [
        "# Statutory Lineage Target Lifecycle Bridge",
        "",
        "This report bridges source-reviewed statutory target-section diff rows to bounded implementation and court-review context. Base U.S.C. section overlaps are metadata context and are not exact target-reference or subsection evidence. Raw SCDB target-section overlaps are date-screened section-citation context and do not prove review of the queued public law, bill, note, or subsection. Public-law-level authority, rulemaking, comment, and court rows remain public-law context. It is not implementation outcome, direct target-section court-review, effective-text, causal, welfare, or model-validation evidence.",
        "",
        f"- Target-section bridge rows: {len(rows)}",
        f"- Reviewed public laws: {len(public_laws)}",
        f"- Rows with public-law lifecycle context: {len(public_law_context_rows)}",
        f"- Rows with authority base U.S.C. section overlap: {len(authority_base_rows)}",
        f"- Rows with exact authority target-reference overlap: {len(authority_exact_rows)}",
        f"- Rows with court base U.S.C. section overlap: {len(court_base_rows)}",
        f"- Rows with exact court target-reference overlap: {len(court_exact_rows)}",
        f"- Rows with raw SCDB target base-section overlap: {len(raw_scdb_base_rows)}",
        f"- Rows with raw SCDB exact target-reference overlap: {len(raw_scdb_exact_rows)}",
        f"- Unique raw SCDB target base-section cases represented: {len(raw_scdb_case_ids)}",
        f"- Raw SCDB post-enactment target base-section case attachments: {raw_scdb_post_enactment_attachments}",
        f"- Unique public-law direct-review disposition rows represented: {len(unique_direct_review_rows)}",
        f"- Target-level direct-review disposition row attachments: {direct_review_attachments}",
        "",
        "Lifecycle statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "Evidence grades:"])
    for grade, count in sorted(grade_counts.items()):
        lines.append(f"- {grade}: {count}")
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| Rank | Bill | Public law | Target | Lifecycle status | Authority base | Authority exact | Court base | Court exact | Raw SCDB base | Raw SCDB post | Public-law authority docs | Public-law court cases |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in rows:
        authority_docs = len(split_values(row["public_law_authority_document_numbers"]))
        lines.append(
            f"| {row['bridge_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"`{row['target_reference']}` | {row['target_lifecycle_status']} | "
            f"{row['authority_base_section_match']} | {row['authority_exact_target_reference_match']} | "
            f"{row['court_base_section_overlap']} | {row['court_exact_target_reference_overlap']} | "
            f"{row['raw_scdb_target_base_section_overlap']} | "
            f"{row['raw_scdb_target_base_section_post_enactment_case_count']} | "
            f"{authority_docs} | {row['public_law_court_overlap_case_count']} |"
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
