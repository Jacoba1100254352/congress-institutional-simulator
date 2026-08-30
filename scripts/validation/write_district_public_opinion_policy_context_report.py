#!/usr/bin/env python3
"""Write a report for bounded district-opinion policy-area context."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW_CONTEXT = Path("data/validation/raw/district_public_opinion_policy_context.csv")
OUT_CSV = Path("reports/district-public-opinion-policy-context.csv")
OUT_MD = Path("reports/district-public-opinion-policy-context.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: str | None) -> float:
    try:
        return float(value or "0")
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def write_md(rows: list[dict[str, str]]) -> None:
    mapped = [
        row for row in rows
        if row["policy_context_status"] == "sponsor_district_bill_policy_context"
    ]
    policy_counts = Counter(row["policy_area"] for row in mapped if row["policy_area"])
    issue_counts = Counter(row["issue"] for row in rows if row["issue"])
    unique_keys = {(row["district_id"], row["issue"], row["year"]) for row in rows}
    unique_bills = {row["bill_id"] for row in rows if row["bill_id"]}
    unique_districts = {row["district_id"] for row in rows if row["district_id"]}

    lines = [
        "# District Public-Opinion Policy Context",
        "",
        "This report adds bounded bill policy-area context to cached Cumulative CES district aggregates that already join to House-sponsored public-law bill metadata by sponsor district. It is a context inventory, not bill-topic public-support validation.",
        "",
        f"- Policy-context rows: {len(rows)}",
        f"- Rows with mapped policy-area topic context: {len(mapped)}",
        f"- Unique district-opinion row keys: {len(unique_keys)}",
        f"- Unique public-law bills: {len(unique_bills)}",
        f"- Unique sponsor districts: {len(unique_districts)}",
        f"- Unique policy areas: {len(policy_counts)}",
        "",
        "Claim boundary: mapped rows connect generic CES district public-opinion proxies to sponsor-district public-law bill policy areas only. They do not identify issue-specific bill support, MRP or small-area estimates, affected-group harm, constituent contact, member vote choice, representative responsiveness, public benefit, welfare, causal effects, or model validation.",
        "",
        "Survey proxy rows:",
    ]
    for issue, count in sorted(issue_counts.items()):
        issue_rows = [row for row in rows if row["issue"] == issue]
        lines.append(
            f"- {issue}: {count} rows; mean support {mean([parse_float(row['support']) for row in issue_rows]):.3f}; "
            f"mean affected-group proxy {mean([parse_float(row['affected_group_share']) for row in issue_rows]):.3f}"
        )

    lines.extend([
        "",
        "| Policy area | Rows | Unique bills | Unique districts | Mean support | Mean affected-group proxy |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for policy, count in sorted(policy_counts.items(), key=lambda item: (-item[1], item[0])):
        policy_rows = [row for row in mapped if row["policy_area"] == policy]
        lines.append(
            f"| {policy} | {count} | {len({row['bill_id'] for row in policy_rows if row['bill_id']})} | "
            f"{len({row['district_id'] for row in policy_rows if row['district_id']})} | "
            f"{mean([parse_float(row['support']) for row in policy_rows]):.3f} | "
            f"{mean([parse_float(row['affected_group_share']) for row in policy_rows]):.3f} |"
        )

    lines.extend([
        "",
        "| Bill ID | Public law | District | Survey proxy | Policy area | Support | Affected-group proxy | Missing links |",
        "| --- | --- | --- | --- | --- | ---: | ---: | --- |",
    ])
    for row in mapped:
        lines.append(
            f"| `{row['bill_id']}` | `{row['public_law_number']}` | `{row['district_id']}` | "
            f"{row['issue']} | {row['policy_area']} | {row['support']} | "
            f"{row['affected_group_share']} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW_CONTEXT.exists():
        raise SystemExit(f"{RAW_CONTEXT} is missing; run make build-district-public-opinion-policy-context-raw first.")
    rows = read_csv(RAW_CONTEXT)
    if not rows:
        raise SystemExit(f"{RAW_CONTEXT} is empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
