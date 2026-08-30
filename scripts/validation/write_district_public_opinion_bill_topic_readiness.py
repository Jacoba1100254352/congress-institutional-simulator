#!/usr/bin/env python3
"""Write a bill-topic public-opinion readiness report.

The current district-opinion layer joins Cumulative CES district aggregates to
House-sponsored public-law bill policy areas. This report converts that bounded
proxy context into a bill-level source queue for the next real public-opinion
upgrade, while keeping the claim boundary explicit.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


POLICY_CONTEXT = Path("reports/district-public-opinion-policy-context.csv")
NEXT_ACTIONS = Path("reports/bill-law-lifecycle-next-actions.csv")
OUT_CSV = Path("reports/district-public-opinion-bill-topic-readiness.csv")
OUT_MD = Path("reports/district-public-opinion-bill-topic-readiness.md")

BROAD_PROXY_ISSUES = {
    "house_representative_approval",
    "presidential_democratic_preference",
    "house_democratic_preference",
}

FIELDNAMES = [
    "readiness_rank",
    "action_rank",
    "bill_id",
    "public_law_number",
    "policy_area",
    "sponsor_districts",
    "proxy_row_count",
    "proxy_issue_count",
    "proxy_issues",
    "mean_support",
    "mean_affected_group_proxy",
    "issue_specific_support_rows",
    "mrp_or_small_area_rows",
    "affected_group_support_rows",
    "bill_topic_public_opinion_status",
    "mrp_or_small_area_status",
    "affected_group_status",
    "next_review_sources",
    "review_packet",
    "evidence_layers",
    "missing_links",
    "source_url",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def sort_key(value: str) -> tuple[int, str]:
    try:
        return int(value), value
    except ValueError:
        return 999999, value


def unique_join(values: list[str]) -> str:
    return "; ".join(sorted({value for value in values if value}))


def action_rank_by_bill(rows: list[dict[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in rows:
        bill_id = row.get("bill_id", "")
        action_rank = row.get("action_rank", "")
        if bill_id and action_rank and bill_id not in result:
            result[bill_id] = action_rank
    return result


def build_rows(
    policy_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows_by_bill: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in policy_rows:
        bill_id = row.get("bill_id", "")
        if bill_id:
            rows_by_bill[bill_id].append(row)

    ranks = action_rank_by_bill(action_rows)
    sorted_bill_rows = sorted(
        rows_by_bill.items(),
        key=lambda item: (sort_key(ranks.get(item[0], "")), item[0]),
    )

    output: list[dict[str, str]] = []
    for index, (bill_id, rows) in enumerate(sorted_bill_rows, start=1):
        issues = sorted({row.get("issue", "") for row in rows if row.get("issue", "")})
        issue_specific_support_rows = [
            row for row in rows
            if row.get("issue", "") not in BROAD_PROXY_ISSUES
        ]
        policy_areas = unique_join([row.get("policy_area", "") for row in rows])
        public_laws = unique_join([row.get("public_law_number", "") for row in rows])
        sponsor_districts = unique_join([row.get("district_id", "") for row in rows])
        source_urls = unique_join([row.get("source_url", "") for row in rows])
        mean_support = mean([parse_float(row.get("support")) for row in rows])
        mean_affected_group = mean([
            parse_float(row.get("affected_group_share"))
            for row in rows
        ])
        issue_specific_count = len(issue_specific_support_rows)

        bill_topic_status = (
            "issue_specific_bill_support_available"
            if issue_specific_count
            else "proxy_only_missing_issue_specific_bill_support"
        )
        mrp_status = "missing_mrp_or_small_area_estimate"
        affected_group_status = "missing_issue_specific_affected_group_support_or_harm"

        output.append({
            "readiness_rank": str(index),
            "action_rank": ranks.get(bill_id, ""),
            "bill_id": bill_id,
            "public_law_number": public_laws,
            "policy_area": policy_areas,
            "sponsor_districts": sponsor_districts,
            "proxy_row_count": str(len(rows)),
            "proxy_issue_count": str(len(issues)),
            "proxy_issues": "; ".join(issues),
            "mean_support": f"{mean_support:.6f}",
            "mean_affected_group_proxy": f"{mean_affected_group:.6f}",
            "issue_specific_support_rows": str(issue_specific_count),
            "mrp_or_small_area_rows": "0",
            "affected_group_support_rows": "0",
            "bill_topic_public_opinion_status": bill_topic_status,
            "mrp_or_small_area_status": mrp_status,
            "affected_group_status": affected_group_status,
            "next_review_sources": (
                "bill-topic survey item crosswalk; district MRP or small-area estimate; "
                "ACS or comparable affected-population denominator; affected-group support "
                "or harm source"
            ),
            "review_packet": (
                f"{bill_id}: map {policy_areas or 'unknown policy area'} to an issue-specific "
                "survey item, estimate or import district support, and keep affected-population "
                "exposure separate from general support."
            ),
            "evidence_layers": (
                "cumulative_ces_district_aggregate; sponsor_district_public_law_bill_metadata; "
                "sponsor_district_bill_policy_area_context; topic_throughput_policy_area; "
                "bill_topic_public_opinion_readiness_queue"
            ),
            "missing_links": (
                "bill_topic_public_opinion; MRP_or_small_area_estimate; "
                "issue_specific_affected_group_support; affected_group_harm; "
                "constituent_contacts; member_vote; causal_representation; public_benefit; "
                "model_validation"
            ),
            "source_url": source_urls,
            "claim_boundary": (
                "Bill-level readiness queue derived from bounded CES district aggregate, "
                "sponsor-district public-law bill metadata, and policy-area context only; not "
                "bill-topic public support, MRP or small-area estimation, issue-specific "
                "affected-group support or harm, public benefit, welfare, causal "
                "representation, or model validation."
            ),
        })
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    proxy_only = [
        row for row in rows
        if row["bill_topic_public_opinion_status"] == "proxy_only_missing_issue_specific_bill_support"
    ]
    policy_areas = {
        value.strip()
        for row in rows
        for value in row["policy_area"].split(";")
        if value.strip()
    }
    proxy_rows = sum(int(row["proxy_row_count"]) for row in rows)
    issue_specific_rows = sum(int(row["issue_specific_support_rows"]) for row in rows)
    affected_group_rows = sum(int(row["affected_group_support_rows"]) for row in rows)

    lines = [
        "# District Public-Opinion Bill-Topic Readiness",
        "",
        "This report turns the bounded sponsor-district public-opinion policy-context layer into a bill-level source queue for issue-specific public-opinion and affected-group evidence. It is readiness evidence only, not bill-topic support validation.",
        "",
        f"- Public-law bills queued: {len(rows)}",
        f"- Proxy context rows represented: {proxy_rows}",
        f"- Policy areas represented: {len(policy_areas)}",
        f"- Bills still proxy-only for bill-topic support: {len(proxy_only)}",
        f"- Issue-specific support rows present: {issue_specific_rows}",
        f"- Affected-group support/harm rows present: {affected_group_rows}",
        "",
        "Claim boundary: these rows are derived from CES district aggregate proxies, sponsor-district public-law metadata, and policy-area context only. They do not provide issue-specific bill support, MRP/small-area estimates, affected-group support or harm, public benefit, welfare, causal representation, or model validation.",
        "",
        "| Rank | Bill ID | Public law | Policy area | Proxy rows | Proxy issues | Status | Next review packet |",
        "| ---: | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['readiness_rank']} | `{row['bill_id']}` | `{row['public_law_number']}` | "
            f"{row['policy_area']} | {row['proxy_row_count']} | {row['proxy_issues']} | "
            f"{row['bill_topic_public_opinion_status']} | {row['review_packet']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not POLICY_CONTEXT.exists():
        raise SystemExit(f"{POLICY_CONTEXT} is missing; run make district-public-opinion-policy-context first.")
    if not NEXT_ACTIONS.exists():
        raise SystemExit(f"{NEXT_ACTIONS} is missing; run make bill-law-lifecycle-next-actions first.")
    policy_rows = read_csv(POLICY_CONTEXT)
    if not policy_rows:
        raise SystemExit(f"{POLICY_CONTEXT} is empty.")
    rows = build_rows(policy_rows, read_csv(NEXT_ACTIONS))
    if not rows:
        raise SystemExit("No bill-topic public-opinion readiness rows could be built.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
