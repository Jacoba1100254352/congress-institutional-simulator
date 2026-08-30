#!/usr/bin/env python3
"""Build a bounded SCDB-to-public-law authority-overlap linkage cache."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


COURT_REVIEW = Path("data/validation/raw/court_review.csv")
RULEMAKING_AUTHORITY_LINKAGE = Path("data/validation/raw/rulemaking_authority_linkage.csv")
OUT_CSV = Path("data/validation/raw/court_law_linkage.csv")
OUT_METADATA = Path("data/validation/raw/court_law_linkage.metadata.md")

FIELDNAMES = [
    "case_id",
    "case_name",
    "term",
    "decision_date",
    "issue",
    "invalidated",
    "signed_opinion",
    "vote_margin",
    "law_type",
    "law_supp",
    "law_minor",
    "court_usc_sections",
    "linkage_status",
    "candidate_usc_section_count",
    "matched_usc_section_count",
    "matched_authority_overlap_count",
    "matched_public_law_count",
    "public_law_numbers",
    "bill_ids",
    "matched_usc_sections",
    "authority_document_numbers",
    "authority_agencies",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded metadata overlap between SCDB lawMinor U.S.C. citations and Federal Register "
    "authority U.S.C. citations attached to cached public-law rows; not proof that the case "
    "challenged or invalidated the listed public law, bill, agency implementation chain, "
    "or rule, and not emergency-order, lower-court, welfare, causal-effect, or model validation evidence."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing; build the prerequisite cache first.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = part.strip()
        if clean and clean not in values:
            values.append(clean)
    return values


def normalize_usc_sections(value: str) -> list[str]:
    text = (value or "").replace("\u00a7", " ")
    sections: list[str] = []
    for match in re.finditer(
        r"\b(?P<title>\d{1,3})\s*U\.?S\.?C\.?\s*(?:\u00a7+\s*)?"
        r"(?P<section>[0-9A-Za-z][0-9A-Za-z.\-]*)",
        text,
        flags=re.IGNORECASE,
    ):
        title = str(int(match.group("title")))
        section = match.group("section").strip().lower()
        normalized = f"{title} U.S.C. {section}"
        if normalized not in sections:
            sections.append(normalized)
    return sections


def court_usc_sections(row: dict[str, str]) -> list[str]:
    sections = split_values(row.get("usc_sections", ""))
    if sections:
        return sections
    return normalize_usc_sections(row.get("law_minor", ""))


def authority_index(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        if row.get("linkage_status") != "federal_register_authority_match":
            continue
        public_law = row.get("public_law_number", "").strip()
        bill_id = row.get("bill_id", "").strip()
        if not public_law:
            continue
        documents = split_values(row.get("matched_document_numbers", ""))
        agencies = split_values(row.get("agency_names", ""))
        for section in normalize_usc_sections(row.get("usc_citations", "")):
            key = (section, public_law, bill_id)
            if key in seen:
                continue
            seen.add(key)
            indexed[section].append({
                "public_law_number": public_law,
                "bill_id": bill_id,
                "usc_section": section,
                "authority_document_numbers": "; ".join(documents),
                "authority_agencies": "; ".join(agencies),
            })
    return indexed


def missing_links(status: str) -> str:
    links = [
        "direct_case_to_public_law_identifier",
        "direct_case_to_bill_identifier",
        "direct_case_to_rule_or_agency_docket",
        "merits_record_statute_disposition_review",
        "emergency_order_dataset",
        "lower_court_history",
        "causal_invalidation_effect",
        "model_validation",
    ]
    if status == "no_usc_section":
        links.insert(0, "scdb_law_minor_usc_section")
    elif status == "usc_section_only":
        links.insert(1, "public_law_or_rule_authority_overlap")
    return "; ".join(links)


def build_rows() -> list[dict[str, str]]:
    court_rows = read_csv(COURT_REVIEW)
    authority_rows = read_csv(RULEMAKING_AUTHORITY_LINKAGE)
    indexed_authority = authority_index(authority_rows)
    output: list[dict[str, str]] = []

    for row in court_rows:
        sections = court_usc_sections(row)
        matches: list[dict[str, str]] = []
        for section in sections:
            matches.extend(indexed_authority.get(section, []))
        public_laws = sorted({match["public_law_number"] for match in matches if match["public_law_number"]})
        bill_ids = sorted({match["bill_id"] for match in matches if match["bill_id"]})
        matched_sections = sorted({match["usc_section"] for match in matches if match["usc_section"]})
        documents = sorted({
            document
            for match in matches
            for document in split_values(match.get("authority_document_numbers", ""))
        })
        agencies = sorted({
            agency
            for match in matches
            for agency in split_values(match.get("authority_agencies", ""))
        })
        if matches:
            status = "usc_section_authority_overlap"
            layers = [
                "scdb_law_minor_usc_section",
                "federal_register_authority_usc_overlap",
                "public_law_bill_metadata",
            ]
        elif sections:
            status = "usc_section_only"
            layers = ["scdb_law_minor_usc_section"]
        else:
            status = "no_usc_section"
            layers = ["scdb_case_metadata"]

        output.append({
            "case_id": row.get("case_id", "").strip(),
            "case_name": row.get("case_name", "").strip(),
            "term": row.get("term", "").strip(),
            "decision_date": row.get("decision_date", "").strip(),
            "issue": row.get("issue", "").strip(),
            "invalidated": row.get("invalidated", "").strip(),
            "signed_opinion": row.get("signed_opinion", "").strip(),
            "vote_margin": row.get("vote_margin", "").strip(),
            "law_type": row.get("law_type", "").strip(),
            "law_supp": row.get("law_supp", "").strip(),
            "law_minor": row.get("law_minor", "").strip(),
            "court_usc_sections": "; ".join(sections),
            "linkage_status": status,
            "candidate_usc_section_count": str(len(sections)),
            "matched_usc_section_count": str(len(matched_sections)),
            "matched_authority_overlap_count": str(len({
                (match["usc_section"], match["public_law_number"], match["bill_id"])
                for match in matches
            })),
            "matched_public_law_count": str(len(public_laws)),
            "public_law_numbers": "; ".join(public_laws),
            "bill_ids": "; ".join(bill_ids),
            "matched_usc_sections": "; ".join(matched_sections),
            "authority_document_numbers": "; ".join(documents),
            "authority_agencies": "; ".join(agencies),
            "evidence_layers": "; ".join(layers),
            "missing_links": missing_links(status),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    section_rows = sum(1 for row in rows if row["court_usc_sections"])
    matched_rows = [
        row for row in rows
        if row["linkage_status"] == "usc_section_authority_overlap"
    ]
    public_laws = {
        public_law
        for row in matched_rows
        for public_law in split_values(row["public_law_numbers"])
    }
    bill_ids = {
        bill_id
        for row in matched_rows
        for bill_id in split_values(row["bill_ids"])
    }
    sections = {
        section
        for row in matched_rows
        for section in split_values(row["matched_usc_sections"])
    }
    lines = [
        "# Court-Law Linkage Raw Dataset",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Inputs:",
        "",
        f"- `{COURT_REVIEW}`",
        f"- `{RULEMAKING_AUTHORITY_LINKAGE}`",
        "",
        "Transformation:",
        "",
        "- Parses U.S.C. title-section citations from SCDB `law_minor` / `usc_sections` fields.",
        "- Parses U.S.C. title-section citations from Federal Register authority-search `usc_citations` fields.",
        "- Marks a court row as `usc_section_authority_overlap` only when a normalized U.S.C. section appears in both places.",
        "- Keeps unmatched SCDB rows in the output so the denominator remains explicit.",
        "",
        "Rows:",
        "",
        f"- SCDB court rows checked: {len(rows)}",
        f"- Court rows with parsed U.S.C. sections: {section_rows}",
        f"- Court rows with authority-section overlaps: {len(matched_rows)}",
        f"- Public-law rows overlapped by at least one court U.S.C. section: {len(public_laws)}",
        f"- Bill IDs overlapped by at least one court U.S.C. section: {len(bill_ids)}",
        f"- Unique matched U.S.C. sections: {len(sections)}",
        "",
        "Claim boundary:",
        "",
        CLAIM_BOUNDARY,
    ]
    OUT_METADATA.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No court rows were available for linkage.")
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
