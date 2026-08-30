#!/usr/bin/env python3
"""Write bounded committee/action context for bill-finance/lobbying queue rows."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


QUEUE = Path("reports/bill-finance-lobbying-review-queue.csv")
LOCAL_CONTEXT_REVIEW = Path("reports/bill-finance-lobbying-local-context-review.csv")
EXTERNAL_SEARCH_REVIEW = Path("reports/bill-finance-lobbying-external-search-review.csv")
EXTERNAL_LDA_MENTION_REVIEW = Path("reports/bill-finance-lobbying-external-lda-mention-review.csv")
CAMPAIGN_TARGET_SCOPE_REVIEW = Path("reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv")
LAW_REVISION_BILL_LINKAGE = Path("data/validation/raw/law_revision_bill_linkage.csv")
OUT_CSV = Path("reports/bill-finance-lobbying-committee-action-context.csv")
OUT_MD = Path("reports/bill-finance-lobbying-committee-action-context.md")

CLAIM_BOUNDARY = (
    "Bill finance/lobbying committee/action context only; rows join the existing "
    "finance/lobbying review queue to cached public bill-action metadata and "
    "current LDA/FEC review dispositions. Committee-reported and floor-considered "
    "flags are bill-action metadata, not evidence that campaign finance or "
    "lobbying targeted, caused, influenced, supported, opposed, or benefited a "
    "committee action, roll call, legislative outcome, public benefit, welfare, "
    "causal capture, or model result. Current cached bill-action metadata does "
    "not provide committee-of-jurisdiction names for these rows."
)

MISSING_LINKS = "; ".join([
    "committee_of_jurisdiction",
    "committee_action_influence",
    "roll_call_influence",
    "legislative_outcome_causality",
    "bill_specific_campaign_finance_influence",
    "bill_specific_lobbying_influence",
    "external_campaign_target_source_document",
    "lobbying_contact_or_target_source",
    "reviewed_outside_spending_target_beyond_candidate_id",
    "public_benefit_or_welfare_validation",
    "causal_capture_validation",
    "model_validation",
])

FIELDNAMES = [
    "context_rank",
    "review_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_bioguide_id",
    "sponsor_party",
    "sponsor_state",
    "introduced_date",
    "enacted_date",
    "actions_count",
    "committee_reported",
    "floor_considered",
    "bill_action_context_status",
    "committee_name_context_status",
    "floor_action_context_status",
    "local_review_status",
    "external_lda_search_disposition",
    "external_lda_exact_activity_match_rows",
    "external_lda_mention_packets",
    "external_lda_mention_rows_represented",
    "external_lda_committee_action_statuses",
    "campaign_target_scope_status",
    "campaign_target_scope_disposition",
    "committee_action_influence_status",
    "roll_call_influence_status",
    "legislative_outcome_causality_status",
    "next_review_action",
    "evidence_layers",
    "missing_links",
    "source_urls",
    "source_url",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def yes_no(value: str | None) -> str:
    return "yes" if parse_int(value) > 0 else "no"


def split_values(value: str | None) -> list[str]:
    values: list[str] = []
    for part in (value or "").split(";"):
        clean = " ".join(part.split())
        if clean and clean not in values:
            values.append(clean)
    return values


def join_values(values: list[str] | set[str]) -> str:
    ordered: list[str] = []
    for value in values:
        clean = " ".join(str(value or "").split())
        if clean and clean not in ordered:
            ordered.append(clean)
    return "; ".join(ordered)


def by_bill(rows: list[dict[str, str]], *, unique: bool = True) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if not bill_id:
            continue
        if unique and bill_id in result:
            raise SystemExit(f"duplicate bill_id={bill_id}")
        result[bill_id] = row
    return result


def grouped_by_bill(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        bill_id = row.get("bill_id", "").strip()
        if bill_id:
            result[bill_id].append(row)
    return result


def action_status(committee_reported: str, floor_considered: str) -> str:
    if committee_reported == "yes" and floor_considered == "yes":
        return "public_bill_action_metadata_committee_reported_and_floor_considered"
    if committee_reported == "yes":
        return "public_bill_action_metadata_committee_reported_without_floor_flag"
    if floor_considered == "yes":
        return "public_bill_action_metadata_floor_considered_without_committee_reported_flag"
    return "public_bill_action_metadata_no_committee_or_floor_flag"


def floor_status(floor_considered: str) -> str:
    if floor_considered == "yes":
        return "public_bill_action_metadata_floor_considered_flag_present"
    return "public_bill_action_metadata_floor_considered_flag_absent"


def build_rows() -> list[dict[str, str]]:
    queue_rows = sorted(read_csv(QUEUE), key=lambda row: parse_int(row.get("review_rank")))
    local_by_bill = by_bill(read_csv(LOCAL_CONTEXT_REVIEW))
    external_by_bill = by_bill(read_csv(EXTERNAL_SEARCH_REVIEW))
    campaign_by_bill = by_bill(read_csv(CAMPAIGN_TARGET_SCOPE_REVIEW), unique=False)
    law_by_bill = by_bill(read_csv(LAW_REVISION_BILL_LINKAGE))
    mentions_by_bill = grouped_by_bill(read_csv(EXTERNAL_LDA_MENTION_REVIEW))

    queue_bill_ids = {row.get("bill_id", "").strip() for row in queue_rows}
    for name, mapping in (
        (LOCAL_CONTEXT_REVIEW, local_by_bill),
        (EXTERNAL_SEARCH_REVIEW, external_by_bill),
        (LAW_REVISION_BILL_LINKAGE, law_by_bill),
    ):
        missing = sorted(queue_bill_ids - set(mapping))
        if missing:
            raise SystemExit(f"{name}: missing queue bills {missing}")

    rows: list[dict[str, str]] = []
    for queue_row in queue_rows:
        bill_id = queue_row["bill_id"]
        local = local_by_bill[bill_id]
        external = external_by_bill[bill_id]
        law = law_by_bill[bill_id]
        campaign = campaign_by_bill.get(bill_id, {})
        mention_rows = mentions_by_bill.get(bill_id, [])
        committee_reported = yes_no(law.get("committee_reported"))
        floor_considered = yes_no(law.get("floor_considered"))
        exact_lda_rows = parse_int(external.get("lda_exact_activity_match_rows"))
        mention_packet_rows = sum(parse_int(row.get("rows_represented")) for row in mention_rows)
        evidence_layers = [
            "bill_finance_lobbying_review_queue",
            "manual_bill_finance_lobbying_local_context_review",
            "bill_finance_lobbying_external_search_review",
            "law_revision_bill_action_metadata",
        ]
        if mention_rows:
            evidence_layers.append("external_lda_activity_text_mention_review")
        if campaign:
            evidence_layers.append("campaign_finance_target_scope_review")
        source_urls = split_values(queue_row.get("source_url"))
        source_urls.extend(split_values(law.get("source_url")))
        source_urls.extend(split_values(external.get("source_url")))
        source_urls.extend(split_values(campaign.get("source_url")))
        rows.append({
            "context_rank": str(len(rows) + 1),
            "review_rank": queue_row.get("review_rank", ""),
            "bill_id": bill_id,
            "public_law_number": queue_row.get("public_law_number", ""),
            "policy_area": queue_row.get("policy_area", ""),
            "sponsor_bioguide_id": queue_row.get("sponsor_bioguide_id", ""),
            "sponsor_party": queue_row.get("sponsor_party", ""),
            "sponsor_state": queue_row.get("sponsor_state", ""),
            "introduced_date": queue_row.get("introduced_date", ""),
            "enacted_date": queue_row.get("enacted_date", ""),
            "actions_count": law.get("actions_count", ""),
            "committee_reported": committee_reported,
            "floor_considered": floor_considered,
            "bill_action_context_status": action_status(committee_reported, floor_considered),
            "committee_name_context_status": "no_committee_name_or_jurisdiction_source_in_current_cache",
            "floor_action_context_status": floor_status(floor_considered),
            "local_review_status": local.get("manual_bill_specific_gate_status", ""),
            "external_lda_search_disposition": external.get("lda_search_disposition", ""),
            "external_lda_exact_activity_match_rows": str(exact_lda_rows),
            "external_lda_mention_packets": str(len(mention_rows)),
            "external_lda_mention_rows_represented": str(mention_packet_rows),
            "external_lda_committee_action_statuses": join_values({
                row.get("committee_action_status", "") for row in mention_rows
            }) if mention_rows else "not_in_external_lda_mention_review",
            "campaign_target_scope_status": (
                campaign.get("public_fec_target_scope_status", "")
                if campaign else "not_in_campaign_finance_target_scope_review"
            ),
            "campaign_target_scope_disposition": (
                campaign.get("target_scope_disposition", "")
                if campaign else "not_in_campaign_finance_target_scope_review"
            ),
            "committee_action_influence_status": (
                "no_finance_or_lobbying_committee_action_influence_evidence"
            ),
            "roll_call_influence_status": "no_finance_or_lobbying_roll_call_influence_evidence",
            "legislative_outcome_causality_status": (
                "enacted_public_law_metadata_only_no_finance_or_lobbying_outcome_causality"
            ),
            "next_review_action": (
                "Acquire committee-of-jurisdiction names, source-reviewed committee action records, "
                "roll-call context, and independent finance/lobbying target documents before making "
                "any committee-action, roll-call, or legislative-outcome influence claim."
            ),
            "evidence_layers": "; ".join(evidence_layers),
            "missing_links": MISSING_LINKS,
            "source_urls": join_values(source_urls),
            "source_url": law.get("source_url", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|")


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["bill_action_context_status"] for row in rows)
    committee_reported_rows = [row for row in rows if row["committee_reported"] == "yes"]
    floor_rows = [row for row in rows if row["floor_considered"] == "yes"]
    lda_rows = [row for row in rows if parse_int(row["external_lda_exact_activity_match_rows"]) > 0]
    campaign_rows = [
        row for row in rows
        if row["campaign_target_scope_status"] != "not_in_campaign_finance_target_scope_review"
    ]
    lines = [
        "# Bill Finance/Lobbying Committee-Action Context",
        "",
        "This report joins the bill-finance/lobbying review queue to cached public-law bill-action metadata and the current external LDA/FEC review dispositions. It is committee/action context only, not influence evidence.",
        "",
        f"- Queued public-law rows reviewed: {len(rows)}",
        f"- Rows with cached committee-reported flag: {len(committee_reported_rows)}",
        f"- Rows with cached floor-considered flag: {len(floor_rows)}",
        f"- Rows with exact external LDA activity-text current-bill mentions: {len(lda_rows)}",
        f"- Rows with campaign-finance target-scope review: {len(campaign_rows)}",
        "- Rows with committee-of-jurisdiction names in current cache: 0",
        "- Rows with finance/lobbying committee-action influence evidence: 0",
        "- Rows with finance/lobbying roll-call influence evidence: 0",
        "- Rows with finance/lobbying legislative-outcome causality evidence: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "Bill-action context statuses:",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend([
        "",
        "By bill:",
        "",
        "| Rank | Bill | Public law | Actions | Committee reported | Floor considered | External LDA rows | Campaign target scope |",
        "| ---: | --- | --- | ---: | --- | --- | ---: | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['context_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['actions_count']} | {row['committee_reported']} | {row['floor_considered']} | "
            f"{row['external_lda_exact_activity_match_rows']} | "
            f"{md_escape(row['campaign_target_scope_disposition'])} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No bill-finance/lobbying committee-action context rows found.")
    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_markdown(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
