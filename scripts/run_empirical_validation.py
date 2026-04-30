#!/usr/bin/env python3
"""Compute empirical validation summaries from optional raw input datasets."""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


RAW_DIR = Path("data/validation/raw")
REPORT_CSV = Path("reports/empirical-validation-summary.csv")
REPORT_MD = Path("reports/empirical-validation-summary.md")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def numeric(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "passed", "enacted"}


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def gini(values: list[float]) -> float:
    values = sorted(max(0.0, value) for value in values)
    if not values or sum(values) == 0.0:
        return 0.0
    weighted = sum((index + 1) * value for index, value in enumerate(values))
    return ((2.0 * weighted) / (len(values) * sum(values))) - ((len(values) + 1.0) / len(values))


def entropy_share(counts: list[float]) -> float:
    total = sum(counts)
    if total <= 0.0:
        return 0.0
    entropy = 0.0
    for count in counts:
        if count <= 0.0:
            continue
        share = count / total
        entropy -= share * math.log(share)
    return entropy / math.log(len(counts)) if len(counts) > 1 else 0.0


def append(results: list[dict[str, str]], dataset: str, metric: str, value: float, note: str) -> None:
    results.append({
        "dataset": dataset,
        "metric": metric,
        "value": f"{value:.6f}",
        "status": "computed",
        "note": note,
    })


def append_missing(results: list[dict[str, str]], dataset: str, note: str) -> None:
    results.append({
        "dataset": dataset,
        "metric": "missing",
        "value": "",
        "status": "missing",
        "note": note,
    })


def validate_voteview(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "voteview_rollcalls.csv"
    if not path.exists():
        append_missing(results, path.name, "Add Voteview-like member vote rows to compute party unity and coalition size.")
        return
    grouped: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    by_vote: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows(path):
        vote_id = row["vote_id"]
        party = row["party"]
        vote = row["vote"].strip().lower()
        if vote in {"yea", "yes", "1", "aye", "nay", "no", "0"}:
            normalized = "yes" if vote in {"yea", "yes", "1", "aye"} else "no"
            grouped[(vote_id, party)][normalized] += 1
            by_vote[vote_id][normalized] += 1
    unity = [
        max(counter.values()) / sum(counter.values())
        for counter in grouped.values()
        if sum(counter.values()) >= 2
    ]
    coalition = [
        max(counter.values()) / sum(counter.values())
        for counter in by_vote.values()
        if sum(counter.values()) >= 2
    ]
    append(results, path.name, "partyUnity", mean(unity), "Mean within-party majority vote share by roll call.")
    append(results, path.name, "coalitionSize", mean(coalition), "Mean winning-side share by roll call.")


def validate_bill_progression(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "bill_progression.csv"
    if not path.exists():
        append_missing(results, path.name, "Add Congress.gov/govinfo-style bill history rows to compute attrition.")
        return
    data = rows(path)
    introduced = [row for row in data if truthy(row.get("introduced", "1"))]
    denominator = len(introduced) or len(data)
    floor = sum(1 for row in data if truthy(row.get("floor_considered", "")))
    committee = sum(1 for row in data if truthy(row.get("committee_reported", "")))
    enacted = sum(1 for row in data if truthy(row.get("enacted", "")))
    append(results, path.name, "floorLoad", floor / denominator if denominator else 0.0, "Share of introduced bills receiving floor action.")
    append(results, path.name, "committeeReportRate", committee / denominator if denominator else 0.0, "Share of introduced bills reported by committee.")
    append(results, path.name, "enactmentRate", enacted / denominator if denominator else 0.0, "Share of introduced bills enacted.")


def validate_lobbying(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "lobbying_disclosure.csv"
    if not path.exists():
        append_missing(results, path.name, "Add LDA-style client issue spending rows to compute spend concentration.")
        return
    data = rows(path)
    spends = [numeric(row.get("amount", "")) for row in data]
    by_client: dict[str, float] = defaultdict(float)
    issue_counts: Counter[str] = Counter()
    for row in data:
        by_client[row["client"]] += numeric(row.get("amount", ""))
        issue_counts[row["issue"]] += 1
    append(results, path.name, "meanSpend", mean(spends), "Mean disclosed spending row amount.")
    append(results, path.name, "clientSpendGini", gini(list(by_client.values())), "Gini concentration of spending by client.")
    append(results, path.name, "issueEntropy", entropy_share(list(issue_counts.values())), "Normalized issue diversity in lobbying rows.")


def validate_topic_throughput(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "topic_throughput.csv"
    if not path.exists():
        append_missing(results, path.name, "Add topic-level bill counts to compute agenda diversity and throughput.")
        return
    data = rows(path)
    introduced = [numeric(row.get("introduced", "")) for row in data]
    enacted = [numeric(row.get("enacted", "")) for row in data]
    floor = [numeric(row.get("floor_considered", "")) for row in data]
    append(results, path.name, "topicAgendaEntropy", entropy_share(introduced), "Normalized diversity of introduced bills across topics.")
    append(results, path.name, "topicFloorRate", sum(floor) / sum(introduced) if sum(introduced) else 0.0, "Topic-weighted floor-consideration rate.")
    append(results, path.name, "topicEnactmentRate", sum(enacted) / sum(introduced) if sum(introduced) else 0.0, "Topic-weighted enactment rate.")


def validate_sponsor_success(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "sponsor_success.csv"
    if not path.exists():
        append_missing(results, path.name, "Add sponsor-level introduced/enacted counts to compute sponsor success concentration.")
        return
    success_rates: list[float] = []
    enacted_counts: list[float] = []
    for row in rows(path):
        introduced = numeric(row.get("introduced", ""))
        enacted = numeric(row.get("enacted", ""))
        if introduced > 0.0:
            success_rates.append(enacted / introduced)
        enacted_counts.append(enacted)
    append(results, path.name, "sponsorSuccessRate", mean(success_rates), "Mean sponsor enactment rate.")
    append(results, path.name, "sponsorSuccessGini", gini(enacted_counts), "Gini concentration of enacted bills by sponsor.")


def write_reports(results: list[dict[str, str]]) -> None:
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dataset", "metric", "value", "status", "note"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    lines = [
        "# Empirical Validation Summary",
        "",
        "This report computes validation summaries when optional raw datasets are present under `data/validation/raw/`. Missing rows indicate absent local data, not a simulator failure.",
        "",
        "| Dataset | Metric | Value | Status | Note |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for row in results:
        value = row["value"] if row["value"] else "---"
        lines.append(f"| `{row['dataset']}` | {row['metric']} | {value} | {row['status']} | {row['note']} |")
    REPORT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    results: list[dict[str, str]] = []
    validate_voteview(results)
    validate_bill_progression(results)
    validate_lobbying(results)
    validate_topic_throughput(results)
    validate_sponsor_success(results)
    write_reports(results)
    print(f"Wrote {REPORT_CSV}")
    print(f"Wrote {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
