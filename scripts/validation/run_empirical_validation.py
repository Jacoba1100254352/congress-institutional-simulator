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


def variance(values: list[float]) -> float:
    if not values:
        return 0.0
    avg = mean(values)
    return mean([(value - avg) ** 2 for value in values])


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


def validate_district_public_opinion(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "district_public_opinion.csv"
    if not path.exists():
        append_missing(results, path.name, "Add district opinion rows to compute public-will intensity and affected-group representation.")
        return
    data = rows(path)
    supports = [numeric(row.get("support", "")) for row in data]
    intensities = [numeric(row.get("intensity", "")) for row in data]
    turnouts = [numeric(row.get("turnout", "")) for row in data]
    affected = [numeric(row.get("affected_group_share", "")) for row in data]
    weighted_support = sum(s * max(0.0, i) * max(0.0, t) for s, i, t in zip(supports, intensities, turnouts))
    weight = sum(max(0.0, i) * max(0.0, t) for i, t in zip(intensities, turnouts))
    append(results, path.name, "districtSupportMean", mean(supports), "Mean district-level issue support.")
    append(results, path.name, "intensityWeightedSupport", weighted_support / weight if weight else 0.0, "Support weighted by intensity and turnout.")
    append(results, path.name, "districtSupportVariance", variance(supports), "Variance of district public support.")
    append(results, path.name, "turnoutGini", gini(turnouts), "Turnout concentration across districts.")
    append(results, path.name, "affectedGroupMeanShare", mean(affected), "Mean affected-group population share.")


def validate_committee_activity(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "committee_activity.csv"
    if not path.exists():
        append_missing(results, path.name, "Add committee activity rows to compute referral, reporting, hearing, and discharge rates.")
        return
    data = rows(path)
    referred = sum(numeric(row.get("referred", "")) for row in data)
    reported = sum(numeric(row.get("reported", "")) for row in data)
    hearings = sum(numeric(row.get("hearings", "")) for row in data)
    amendments = sum(numeric(row.get("amendments", "")) for row in data)
    discharged = sum(numeric(row.get("discharged", "")) for row in data)
    append(results, path.name, "committeeReportRate", reported / referred if referred else 0.0, "Reported bills per referred bill.")
    append(results, path.name, "hearingPerReferral", hearings / referred if referred else 0.0, "Hearings per referred bill.")
    append(results, path.name, "amendmentPerReferral", amendments / referred if referred else 0.0, "Amendments per referred bill.")
    append(results, path.name, "dischargeRate", discharged / referred if referred else 0.0, "Discharge petitions or bypasses per referred bill.")


def validate_campaign_finance(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "campaign_finance.csv"
    if not path.exists():
        append_missing(results, path.name, "Add campaign-finance rows to compute private-spending concentration and outside-spending share.")
        return
    data = rows(path)
    by_recipient: dict[str, float] = defaultdict(float)
    by_industry: dict[str, float] = defaultdict(float)
    independent_total = 0.0
    total = 0.0
    for row in data:
        amount = numeric(row.get("amount", ""))
        total += amount
        by_recipient[row["recipient"]] += amount
        by_industry[row["industry"]] += amount
        if truthy(row.get("independent_expenditure", "")):
            independent_total += amount
    append(results, path.name, "recipientFinanceGini", gini(list(by_recipient.values())), "Gini concentration of campaign money by recipient.")
    append(results, path.name, "industryFinanceEntropy", entropy_share(list(by_industry.values())), "Issue/industry diversity of campaign money.")
    append(results, path.name, "outsideSpendingShare", independent_total / total if total else 0.0, "Share of campaign money marked independent expenditure.")


def validate_court_review(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "court_review.csv"
    if not path.exists():
        append_missing(results, path.name, "Add constitutional-court review rows to compute emergency-order and invalidation rates.")
        return
    data = rows(path)
    total = len(data)
    emergency = sum(1 for row in data if truthy(row.get("emergency_order", "")))
    invalidated = sum(1 for row in data if truthy(row.get("invalidated", "")))
    signed = sum(1 for row in data if truthy(row.get("signed_opinion", "")))
    margins = [numeric(row.get("vote_margin", "")) for row in data]
    append(results, path.name, "emergencyOrderRate", emergency / total if total else 0.0, "Share of reviewed cases using emergency-order posture.")
    append(results, path.name, "invalidationRate", invalidated / total if total else 0.0, "Share of reviewed cases invalidating the challenged action.")
    append(results, path.name, "signedOpinionRate", signed / total if total else 0.0, "Share of reviewed cases with signed opinion disclosure.")
    append(results, path.name, "meanVoteMargin", mean(margins), "Mean vote margin or coalition margin in court review.")


def validate_comparative_institutions(results: list[dict[str, str]]) -> None:
    path = RAW_DIR / "comparative_institutions.csv"
    if not path.exists():
        append_missing(results, path.name, "Add comparative-institution rows to compute chamber, party-system, and productivity benchmarks.")
        return
    data = rows(path)
    chambers = [numeric(row.get("chambers", "")) for row in data]
    magnitudes = [numeric(row.get("district_magnitude", "")) for row in data]
    review = [numeric(row.get("judicial_review", "")) for row in data]
    fragmentation = [numeric(row.get("party_fragmentation", "")) for row in data]
    productivity = [numeric(row.get("legislative_productivity", "")) for row in data]
    append(results, path.name, "bicameralShare", sum(1 for value in chambers if value >= 2.0) / len(chambers) if chambers else 0.0, "Share of country-years with two or more chambers.")
    append(results, path.name, "meanDistrictMagnitude", mean(magnitudes), "Mean lower-house district magnitude or equivalent seat magnitude.")
    append(results, path.name, "meanJudicialReviewStrength", mean(review), "Mean encoded judicial-review strength.")
    append(results, path.name, "meanPartyFragmentation", mean(fragmentation), "Mean party-system fragmentation.")
    append(results, path.name, "meanLegislativeProductivity", mean(productivity), "Mean comparative productivity proxy.")


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
    validate_district_public_opinion(results)
    validate_committee_activity(results)
    validate_campaign_finance(results)
    validate_court_review(results)
    validate_comparative_institutions(results)
    write_reports(results)
    print(f"Wrote {REPORT_CSV}")
    print(f"Wrote {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
