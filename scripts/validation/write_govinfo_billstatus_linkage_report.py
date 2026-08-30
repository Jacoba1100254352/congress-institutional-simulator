#!/usr/bin/env python3
"""Write a report for the bounded govinfo BILLSTATUS linkage cache."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


RAW = Path("data/validation/raw/govinfo_billstatus_linkage.csv")
OUT_CSV = Path("reports/govinfo-billstatus-linkage.csv")
OUT_MD = Path("reports/govinfo-billstatus-linkage.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["linkage_status"] for row in rows)
    metadata_rows = [
        row for row in rows
        if row["linkage_status"] == "govinfo_billstatus_metadata"
    ]
    aligned_rows = [
        row for row in metadata_rows
        if row["action_alignment_status"] == "aligned"
    ]
    policy_rows = [
        row for row in metadata_rows
        if row["policy_area_alignment_status"] == "aligned"
    ]
    action_differences = [
        row for row in metadata_rows
        if row["action_alignment_status"] == "flag_difference"
    ]

    lines = [
        "# govinfo BILLSTATUS Linkage",
        "",
        "This report derives an independent govinfo BILLSTATUS cross-check for the cached Congress.gov bill-progression universe. It is a join inventory, not validation evidence.",
        "",
        f"- Bill rows inspected: {len(rows)}",
        f"- Rows with govinfo BILLSTATUS metadata: {len(metadata_rows)}",
        f"- Rows with aligned coarse action flags: {len(aligned_rows)}",
        f"- Rows with differing coarse action flags: {len(action_differences)}",
        f"- Rows with aligned policy area: {len(policy_rows)}",
        "",
        "Claim boundary: this cache checks public govinfo bill-status metadata against the bounded Congress.gov bill sample. It is not a full bill census, public-opinion evidence, lobbying or campaign-finance influence, implementation or court outcome linkage, public benefit, welfare, or model validation.",
        "",
        "Linkage statuses:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Bill | govinfo status | Action alignment | Policy alignment | Actions | Latest action | Missing links |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for row in rows:
        latest_action = row["latest_action_text"] or "---"
        if len(latest_action) > 120:
            latest_action = latest_action[:117] + "..."
        lines.append(
            f"| `{row['bill_id']}` | {row['linkage_status']} | "
            f"{row['action_alignment_status']} | {row['policy_area_alignment_status']} | "
            f"{row['actions_count']} | {latest_action} | {row['missing_links']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not RAW.exists():
        raise SystemExit(f"{RAW} is missing; run make build-govinfo-billstatus-linkage-raw first.")
    rows = read_csv(RAW)
    if not rows:
        raise SystemExit(f"{RAW} is empty.")
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
