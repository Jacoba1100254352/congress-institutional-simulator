#!/usr/bin/env python3
"""Write source-reviewed bill-to-CES policy-item alignment dispositions."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


RAW_REVIEW = Path(
    "data/validation/raw/district_public_opinion_bill_item_alignment_review.csv"
)
BILL_CONTEXT = Path(
    "data/validation/raw/district_public_opinion_bill_text_context.csv"
)
PACKET_ITEMS = Path(
    "reports/district-public-opinion-ces-policy-item-codebook-direction-review.csv"
)
CODEBOOK = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_codebook_direction.csv"
)
RESPONSES = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_response_distributions.csv"
)
SUPPORT_REPORT = Path("reports/district-public-opinion-bill-topic-support.csv")
OUT_CSV = Path("reports/district-public-opinion-bill-item-alignment-review.csv")
OUT_MD = Path("reports/district-public-opinion-bill-item-alignment-review.md")

ALIGNED_STATUS = "reviewed_aligned_historical_issue_item"
ALLOWED_STATUSES = {
    ALIGNED_STATUS,
    "reviewed_related_construct_no_defensible_bill_alignment",
    "reviewed_candidate_items_not_relevant_to_bill_text",
    "reviewed_no_candidate_item_in_current_ces_source",
}

CLAIM_BOUNDARY = (
    "Source-reviewed bill-to-CES item alignment only. A positive row links official "
    "bill text to a directionally aligned historical policy-preference item; it is "
    "not the wording of the bill, not a contemporaneous bill-support question, and "
    "not itself a district estimate; any linked aggregate is reported separately. "
    "Negative dispositions are evidence against forced "
    "policy-area matches. These rows do not provide MRP, affected-group support or "
    "harm, public benefit, causal representation, or model validation."
)

FIELDNAMES = [
    "review_rank",
    "packet_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "display_title",
    "official_title",
    "latest_summary_action_date",
    "latest_summary_update_date",
    "latest_summary_sha256",
    "govinfo_billstatus_url",
    "govinfo_billstatus_sha256",
    "candidate_variable_ids",
    "candidate_variable_count",
    "manual_alignment_status",
    "selected_variable_ids",
    "selected_variable_count",
    "selected_item_labels",
    "selected_item_issue_areas",
    "selected_item_years",
    "selected_item_support_codes",
    "selected_item_oppose_codes",
    "selected_item_nonmissing_responses",
    "bill_policy_direction",
    "survey_item_direction",
    "alignment_direction",
    "alignment_strength",
    "historical_issue_context_status",
    "district_estimation_status",
    "historical_district_estimate_rows",
    "historical_district_estimate_years",
    "historical_district_estimate_artifact",
    "source_review_notes",
    "source_urls",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty.")
    return rows


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def unique_join(values: list[str]) -> str:
    return "; ".join(dict.fromkeys(value for value in values if value))


def indexed(rows: list[dict[str, str]], field: str, source: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row.get(field, "").strip()
        if not key:
            raise SystemExit(f"{source}: row missing {field}.")
        if key in result:
            raise SystemExit(f"{source}: duplicate {field}={key}.")
        result[key] = row
    return result


def validate_review_rows(
    raw_rows: list[dict[str, str]],
    contexts: dict[str, dict[str, str]],
    packets: dict[str, dict[str, str]],
) -> None:
    ranks: list[int] = []
    seen_bills: set[str] = set()
    for row in raw_rows:
        rank = int(row.get("review_rank", "0"))
        ranks.append(rank)
        bill_id = row.get("reviewed_bill_id", "").strip()
        if bill_id in seen_bills:
            raise SystemExit(f"{RAW_REVIEW}: duplicate reviewed bill {bill_id}.")
        seen_bills.add(bill_id)
        context = contexts.get(bill_id)
        packet = packets.get(bill_id)
        if context is None or packet is None:
            raise SystemExit(f"{RAW_REVIEW}: {bill_id} lacks current context or item packet.")
        checks = {
            "reviewed_packet_rank": context["packet_rank"],
            "reviewed_public_law_number": context["public_law_number"],
        }
        for field, expected in checks.items():
            if row.get(field, "").strip() != expected.strip():
                raise SystemExit(f"{RAW_REVIEW}: {bill_id}: stale {field}.")
        if row.get("source_reviewed", "").strip() != "1":
            raise SystemExit(f"{RAW_REVIEW}: {bill_id}: source_reviewed must be 1.")
        status = row.get("manual_alignment_status", "").strip()
        if status not in ALLOWED_STATUSES:
            raise SystemExit(f"{RAW_REVIEW}: {bill_id}: invalid alignment status {status}.")
        selected = split_values(row.get("selected_variable_ids", ""))
        candidates = set(split_values(packet.get("candidate_policy_preference_item_ids", "")))
        if status == ALIGNED_STATUS:
            if not selected or not set(selected).issubset(candidates):
                raise SystemExit(
                    f"{RAW_REVIEW}: {bill_id}: aligned items must be current packet candidates."
                )
            for field in (
                "bill_policy_direction",
                "survey_item_direction",
                "alignment_direction",
                "alignment_strength",
            ):
                if not row.get(field, "").strip():
                    raise SystemExit(f"{RAW_REVIEW}: {bill_id}: aligned row missing {field}.")
        elif selected:
            raise SystemExit(f"{RAW_REVIEW}: {bill_id}: nonaligned row selects an item.")
        if not row.get("source_review_notes", "").strip():
            raise SystemExit(f"{RAW_REVIEW}: {bill_id}: source review notes are empty.")
        if "model validation" not in row.get("claim_boundary", "").lower():
            raise SystemExit(f"{RAW_REVIEW}: {bill_id}: claim boundary is too weak.")
    if ranks != list(range(1, len(raw_rows) + 1)):
        raise SystemExit(f"{RAW_REVIEW}: review ranks must be contiguous and ordered.")
    if seen_bills != set(contexts) or seen_bills != set(packets):
        raise SystemExit(
            f"{RAW_REVIEW}: review coverage must exactly match current context and packet bills."
        )


def selected_metadata(
    variables: list[str],
    codebook_by_variable: dict[str, dict[str, str]],
    response_by_variable: dict[str, dict[str, str]],
) -> dict[str, str]:
    codebook_rows: list[dict[str, str]] = []
    response_rows: list[dict[str, str]] = []
    for variable in variables:
        codebook = codebook_by_variable.get(variable)
        response = response_by_variable.get(variable)
        if codebook is None or response is None:
            raise SystemExit(f"Selected CES variable {variable} lacks codebook or response evidence.")
        if not codebook.get("item_support_codes", "").strip():
            raise SystemExit(f"Selected CES variable {variable} lacks item support codes.")
        codebook_rows.append(codebook)
        response_rows.append(response)
    return {
        "selected_item_labels": unique_join([row["guide_item_description"] for row in codebook_rows]),
        "selected_item_issue_areas": unique_join([row["issue_area"] for row in codebook_rows]),
        "selected_item_years": unique_join([row["guide_years_in_data"] for row in codebook_rows]),
        "selected_item_support_codes": unique_join([
            f"{row['variable_id']}={row['item_support_codes']}" for row in codebook_rows
        ]),
        "selected_item_oppose_codes": unique_join([
            f"{row['variable_id']}={row['item_oppose_codes']}" for row in codebook_rows
        ]),
        "selected_item_nonmissing_responses": str(sum(
            int(row["response_nonmissing_count"]) for row in response_rows
        )),
    }


def build_rows() -> list[dict[str, str]]:
    raw_rows = read_csv(RAW_REVIEW)
    contexts = indexed(read_csv(BILL_CONTEXT), "bill_id", BILL_CONTEXT)
    packets = indexed(read_csv(PACKET_ITEMS), "bill_id", PACKET_ITEMS)
    validate_review_rows(raw_rows, contexts, packets)
    codebook_by_variable = indexed(read_csv(CODEBOOK), "variable_id", CODEBOOK)
    response_by_variable = indexed(
        [row for row in read_csv(RESPONSES) if row.get("year", "").strip() == "all"],
        "variable_id",
        RESPONSES,
    )
    support_rows = read_csv(SUPPORT_REPORT) if SUPPORT_REPORT.exists() else []
    support_by_bill_item: dict[tuple[str, str], list[dict[str, str]]] = {}
    for support_row in support_rows:
        support_key = (
            support_row.get("bill_id", "").strip(),
            support_row.get("survey_item_id", "").strip(),
        )
        if not all(support_key):
            raise SystemExit(f"{SUPPORT_REPORT}: support row lacks bill or survey item ID.")
        support_by_bill_item.setdefault(support_key, []).append(support_row)

    rows: list[dict[str, str]] = []
    for review in raw_rows:
        bill_id = review["reviewed_bill_id"].strip()
        context = contexts[bill_id]
        packet = packets[bill_id]
        selected = split_values(review.get("selected_variable_ids", ""))
        selected_fields = selected_metadata(
            selected, codebook_by_variable, response_by_variable
        ) if selected else {
            "selected_item_labels": "",
            "selected_item_issue_areas": "",
            "selected_item_years": "",
            "selected_item_support_codes": "",
            "selected_item_oppose_codes": "",
            "selected_item_nonmissing_responses": "",
        }
        aligned = review["manual_alignment_status"].strip() == ALIGNED_STATUS
        district_estimates = [
            support_row
            for variable in selected
            for support_row in support_by_bill_item.get((bill_id, variable), [])
        ]
        evidence_layers = [
            "district_public_opinion_bill_text_context",
            "official_govinfo_billstatus_xml",
            "official_congressional_research_service_bill_summary",
            "official_policy_preferences_guide_response_codebook_direction",
            "source_reviewed_bill_item_alignment_disposition",
        ]
        if aligned:
            evidence_layers.append("source_reviewed_historical_issue_item_alignment")
        if district_estimates:
            evidence_layers.append(
                "privacy_thresholded_direct_weighted_district_issue_estimate"
            )
        missing_links = [
            "exact_bill_wording_support",
            "contemporaneous_bill_support",
            "MRP_or_small_area_estimate",
            "bill_text_specific_affected_population_denominator",
            "issue_specific_affected_group_support",
            "affected_group_harm",
            "public_benefit",
            "causal_representation",
            "model_validation",
        ]
        if not aligned:
            missing_links[:0] = [
                "exact_bill_topic_item_wording_review",
                "bill_text_direction_alignment_review",
            ]
        elif not district_estimates:
            missing_links[:0] = [
                "respondent_geography_merge",
                "historical_related_issue_district_estimate",
            ]
        rows.append({
            "review_rank": review["review_rank"].strip(),
            "packet_rank": context["packet_rank"].strip(),
            "bill_id": bill_id,
            "public_law_number": context["public_law_number"].strip(),
            "policy_area": context["policy_area"].strip(),
            "sponsor_districts": context["sponsor_districts"].strip(),
            "display_title": context["display_title"].strip(),
            "official_title": context["official_title"].strip(),
            "latest_summary_action_date": context["latest_summary_action_date"].strip(),
            "latest_summary_update_date": context["latest_summary_update_date"].strip(),
            "latest_summary_sha256": hashlib.sha256(
                context["latest_summary_text"].encode("utf-8")
            ).hexdigest(),
            "govinfo_billstatus_url": context["govinfo_billstatus_url"].strip(),
            "govinfo_billstatus_sha256": context["govinfo_billstatus_sha256"].strip(),
            "candidate_variable_ids": packet["candidate_policy_preference_item_ids"].strip(),
            "candidate_variable_count": packet["candidate_policy_preference_item_count"].strip(),
            "manual_alignment_status": review["manual_alignment_status"].strip(),
            "selected_variable_ids": "; ".join(selected),
            "selected_variable_count": str(len(selected)),
            **selected_fields,
            "bill_policy_direction": review["bill_policy_direction"].strip(),
            "survey_item_direction": review["survey_item_direction"].strip(),
            "alignment_direction": review["alignment_direction"].strip(),
            "alignment_strength": review["alignment_strength"].strip(),
            "historical_issue_context_status": (
                "source_reviewed_historical_issue_item_context_available"
                if aligned
                else "no_source_reviewed_aligned_issue_item"
            ),
            "district_estimation_status": (
                "privacy_thresholded_historical_direct_weighted_estimate_available"
                if district_estimates
                else "pending_annual_cces_geography_join"
                if aligned
                else "not_applicable_without_aligned_issue_item"
            ),
            "historical_district_estimate_rows": str(len(district_estimates)),
            "historical_district_estimate_years": unique_join([
                row.get("survey_year", "") for row in district_estimates
            ]),
            "historical_district_estimate_artifact": (
                str(SUPPORT_REPORT) if district_estimates else ""
            ),
            "source_review_notes": review["source_review_notes"].strip(),
            "source_urls": unique_join([
                context["govinfo_billstatus_url"].strip(),
                codebook_by_variable[selected[0]]["source_url"].strip() if selected else "",
            ]),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": "; ".join(missing_links),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    statuses = Counter(row["manual_alignment_status"] for row in rows)
    aligned = [row for row in rows if row["manual_alignment_status"] == ALIGNED_STATUS]
    district_estimate_rows = sum(
        int(row["historical_district_estimate_rows"] or "0") for row in rows
    )
    lines = [
        "# District Public-Opinion Bill Item Alignment Review",
        "",
        "This report source-reviews current public-law acquisition packets against official bill text and current Cumulative CES policy-preference items.",
        "",
        f"- Source-reviewed bill packets: {len(rows)}",
        f"- Historical issue-item alignments retained: {len(aligned)}",
        f"- Reviewed related constructs without a defensible bill alignment: {statuses['reviewed_related_construct_no_defensible_bill_alignment']}",
        f"- Reviewed candidate sets not relevant to bill text: {statuses['reviewed_candidate_items_not_relevant_to_bill_text']}",
        f"- Packets with no current CES candidate item: {statuses['reviewed_no_candidate_item_in_current_ces_source']}",
        "- Exact bill-wording survey questions: 0",
        f"- Linked privacy-thresholded historical district estimates: {district_estimate_rows}",
        "",
        "Negative dispositions are retained. A broad policy-area match is not promoted to bill-topic evidence when the item wording does not measure the enacted provisions.",
        "",
        "| Rank | Bill | Title | Sponsor district | Review disposition | Selected item | Alignment strength |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['review_rank']} | {row['bill_id']} | "
            f"{row['display_title'].replace('|', '\\|')} | {row['sponsor_districts']} | "
            f"{row['manual_alignment_status']} | {row['selected_variable_ids'] or '-'} | "
            f"{row['alignment_strength'] or '-'} |"
        )
    lines.extend([
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Next gate: acquire exact or closer contemporaneous bill-topic items, design-based uncertainty or MRP where needed, and bill-text-specific affected-population, support, and harm evidence while retaining the historical/nonexact wording limits.",
    ])
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
