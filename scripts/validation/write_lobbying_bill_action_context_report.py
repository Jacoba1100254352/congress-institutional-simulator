#!/usr/bin/env python3
"""Write a bounded LDA exact bill-mention to bill-action context report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


LOBBYING_BILL_MENTIONS = Path("data/validation/raw/lobbying_bill_mentions.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("reports/lobbying-bill-action-context.csv")
OUT_MD = Path("reports/lobbying-bill-action-context.md")

FIELDNAMES = [
    "bill_id",
    "public_law_number",
    "policy_area",
    "introduced_date",
    "enacted_date",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "actions_count",
    "committee_reported",
    "floor_considered",
    "enacted",
    "exact_lda_bill_mention_rows",
    "unique_lda_filings",
    "unique_lda_clients",
    "unique_lda_registrants",
    "lda_activity_issues",
    "lda_government_entities",
    "lda_filing_years",
    "lda_filing_periods",
    "lda_matched_bill_refs",
    "lda_filing_document_urls",
    "bill_action_context_status",
    "match_basis",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "claim_boundary",
]

CLAIM_BOUNDARY = (
    "Bounded official LDA filing-text bill identifiers joined to cached "
    "Congress.gov public-law bill/action metadata only; exact filing text plus "
    "sponsor, action-count, floor-consideration, committee-reported, and enacted "
    "public-law metadata do not show support, opposition, sponsor/member targeting, "
    "committee-action influence, roll-call influence, legislative-outcome causality, "
    "public benefit, welfare, causal capture, or model validation."
)

MISSING_LINKS = "; ".join([
    "support_or_opposition_source_review",
    "sponsor_or_member_target",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_int(value: str) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def split_values(value: str) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def join_values(values: list[str]) -> str:
    return "; ".join(values)


def unique_field(rows: list[dict[str, str]], field: str) -> list[str]:
    values: list[str] = []
    for row in rows:
        for value in split_values(row.get(field, "")):
            if value not in values:
                values.append(value)
    return values


def sort_bill_id(bill_id: str) -> tuple[int, str, int, str]:
    parts = bill_id.split("-")
    if len(parts) >= 3:
        return (parse_int(parts[0]), parts[1], parse_int(parts[2]), bill_id)
    return (0, "", 0, bill_id)


def build_rows(
    mention_rows: list[dict[str, str]],
    law_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    law_by_bill = {
        row.get("bill_id", "").strip(): row
        for row in law_rows
        if row.get("bill_id", "").strip()
    }
    mentions_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in mention_rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            mentions_by_bill[bill_id].append(row)

    output: list[dict[str, str]] = []
    for bill_id in sorted(mentions_by_bill, key=sort_bill_id):
        mentions = mentions_by_bill[bill_id]
        law = law_by_bill.get(bill_id, {})
        status = (
            "exact_lda_bill_mention_with_bill_action_metadata"
            if law else
            "exact_lda_bill_mention_without_cached_bill_action_metadata"
        )
        evidence_layers = ["official_lda_filing_text_bill_identifier"]
        if law:
            evidence_layers.extend([
                "congressgov_bill_action_metadata",
                "congressgov_public_law_outcome_metadata",
                "congressgov_sponsor_metadata",
            ])
        source_urls = unique_field(mentions, "filing_document_url")
        source_urls.extend(
            url for url in unique_field(mentions, "source_url")
            if url not in source_urls
        )
        source_urls.extend(
            url for url in (law.get("source_url", ""), law.get("api_url", ""))
            if url and url not in source_urls
        )
        output.append({
            "bill_id": bill_id,
            "public_law_number": law.get("public_law_number", mentions[0].get("public_law_number", "")),
            "policy_area": law.get("policy_area", mentions[0].get("policy_area", "")),
            "introduced_date": law.get("introduced_date", mentions[0].get("introduced_date", "")),
            "enacted_date": law.get("enacted_date", mentions[0].get("enacted_date", "")),
            "sponsor_bioguide_id": law.get("sponsor_bioguide_id", ""),
            "sponsor_party": law.get("sponsor_party", ""),
            "sponsor_state": law.get("sponsor_state", ""),
            "actions_count": law.get("actions_count", ""),
            "committee_reported": law.get("committee_reported", ""),
            "floor_considered": law.get("floor_considered", ""),
            "enacted": law.get("enacted", ""),
            "exact_lda_bill_mention_rows": str(len(mentions)),
            "unique_lda_filings": str(len(set(unique_field(mentions, "filing_uuid")))),
            "unique_lda_clients": str(len(set(unique_field(mentions, "client_name")))),
            "unique_lda_registrants": str(len(set(unique_field(mentions, "registrant_name")))),
            "lda_activity_issues": join_values(sorted(unique_field(mentions, "activity_issue"))),
            "lda_government_entities": join_values(sorted(unique_field(mentions, "government_entities"))),
            "lda_filing_years": join_values(sorted(unique_field(mentions, "filing_year"))),
            "lda_filing_periods": join_values(sorted(unique_field(mentions, "filing_period"))),
            "lda_matched_bill_refs": join_values(sorted(unique_field(mentions, "matched_bill_refs"))),
            "lda_filing_document_urls": join_values(unique_field(mentions, "filing_document_url")),
            "bill_action_context_status": status,
            "match_basis": "lobbying_bill_mentions.bill_id_to_law_revision_bill_linkage.bill_id",
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": MISSING_LINKS,
            "source_urls": join_values(source_urls),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], mention_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["bill_action_context_status"] for row in rows)
    rows_with_metadata = [
        row for row in rows
        if row["bill_action_context_status"] == "exact_lda_bill_mention_with_bill_action_metadata"
    ]
    exact_rows = sum(parse_int(row["exact_lda_bill_mention_rows"]) for row in rows)
    unique_filings = {
        row.get("filing_uuid", "").strip()
        for row in mention_rows
        if row.get("filing_uuid", "").strip()
    }
    unique_clients = {
        row.get("client_name", "").strip()
        for row in mention_rows
        if row.get("client_name", "").strip()
    }
    unique_urls = {
        row.get("filing_document_url", "").strip()
        for row in mention_rows
        if row.get("filing_document_url", "").strip()
    }
    sponsor_rows = sum(1 for row in rows if row.get("sponsor_bioguide_id", ""))
    committee_reported_rows = sum(1 for row in rows if row.get("committee_reported", "") == "1")
    floor_rows = sum(1 for row in rows if row.get("floor_considered", "") == "1")
    enacted_rows = sum(1 for row in rows if row.get("enacted", "") == "1")
    lines = [
        "# Lobbying Bill Action Context",
        "",
        "This report joins exact official LDA filing-text bill mentions to cached Congress.gov public-law bill/action metadata. It is legislative metadata context only, not influence or validation evidence.",
        "",
        f"- Public-law bills with exact LDA filing-text bill mentions: {len(rows)}",
        f"- Exact LDA filing activity rows represented: {exact_rows}",
        f"- Rows with cached bill/action metadata: {len(rows_with_metadata)}",
        f"- Rows with sponsor metadata: {sponsor_rows}",
        f"- Rows with committee-reported flag: {committee_reported_rows}",
        f"- Rows with floor-considered flag: {floor_rows}",
        f"- Rows with enacted public-law outcome metadata: {enacted_rows}",
        f"- Unique LDA filing IDs represented: {len(unique_filings)}",
        f"- Unique LDA clients represented: {len(unique_clients)}",
        f"- Unique LDA filing document URLs represented: {len(unique_urls)}",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Bill-action context statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Bill | Public law | Policy area | LDA rows | Filings | Clients | Sponsor | Committee reported | Floor | Enacted | Status | Missing links |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for row in sorted(rows, key=lambda item: (-parse_int(item["exact_lda_bill_mention_rows"]), item["bill_id"])):
        sponsor = row["sponsor_bioguide_id"] or "---"
        lines.append(
            f"| `{row['bill_id']}` | `{row['public_law_number']}` | {row['policy_area'] or '---'} | "
            f"{row['exact_lda_bill_mention_rows']} | {row['unique_lda_filings']} | "
            f"{row['unique_lda_clients']} | {sponsor} | {row['committee_reported'] or '0'} | "
            f"{row['floor_considered'] or '0'} | {row['enacted'] or '0'} | "
            f"{row['bill_action_context_status']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    mention_rows = read_csv(LOBBYING_BILL_MENTIONS)
    law_rows = read_csv(LAW_REVISION_BILL_LINKAGE)
    if not mention_rows:
        raise SystemExit(f"{LOBBYING_BILL_MENTIONS} is empty; run make build-lobbying-bill-mentions-raw first.")
    if not law_rows:
        raise SystemExit(f"{LAW_REVISION_BILL_LINKAGE} is empty; run make build-law-revision-bill-linkage-raw first.")
    rows = build_rows(mention_rows, law_rows)
    write_csv(rows)
    write_markdown(rows, mention_rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
