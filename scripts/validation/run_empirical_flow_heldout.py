#!/usr/bin/env python3
"""Run deterministic held-out empirical benchmark checks.

The splits are intentionally simple and auditable. Bill IDs, roll-call IDs, or
sponsor IDs whose stable hash is even are held out, and the rest form the
calibration slice. This does not make the simulator empirically validated, but
it creates real held-out checks for selected source families.
"""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


BILL_CENSUS_RAW = Path("data/validation/raw/govinfo_bill_census.csv")
VOTEVIEW_RAW = Path("data/validation/raw/voteview_rollcalls.csv")
SPONSOR_RAW = Path("data/validation/raw/sponsor_success.csv")
CAMPAIGN_RAW = Path("data/validation/raw/campaign_finance.csv")
DISTRICT_RAW = Path("data/validation/raw/district_public_opinion.csv")
COURT_RAW = Path("data/validation/raw/court_review.csv")
RULEMAKING_RAW = Path("data/validation/raw/rulemaking_implementation.csv")
LAW_REVISION_RAW = Path("data/validation/raw/law_revision_history.csv")
COMPARATIVE_RAW = Path("data/validation/raw/comparative_institutions.csv")
CALIBRATION = Path("reports/calibration-baseline.csv")
OUT_CSV = Path("reports/empirical-flow-heldout.csv")
OUT_MD = Path("reports/empirical-flow-heldout.md")

TRUE_VALUES = {"1", "true", "t", "yes", "y", "passed", "enacted"}

BILL_METRICS = [
    {
        "metric": "enactmentRate",
        "column": "enacted",
        "target": "current-congress-enactment-rate",
        "notes": "Share of introduced bills enacted.",
    },
    {
        "metric": "floorLoad",
        "column": "floor_considered",
        "target": "current-congress-floor-consideration-rate",
        "notes": "Share of introduced bills receiving floor action.",
    },
    {
        "metric": "committeeReportRate",
        "column": "committee_reported",
        "target": "",
        "notes": "Share of introduced bills with a committee report action or citation; reported without a separate calibration target.",
    },
    {
        "metric": "committeeAdvanceRate",
        "column": "committee_advanced",
        "target": "current-congress-committee-advance-rate",
        "notes": "Share of introduced bills ordered reported, reported, or discharged; matched to the workflow's broader committee-advancement construct.",
    },
    {
        "metric": "originPassageRate",
        "column": "passed_origin_chamber",
        "target": "",
        "notes": "Share of introduced bills passing the chamber of origin; reported without a separate calibration target.",
    },
    {
        "metric": "completedCongressionalPassageRate",
        "column": "completed_congressional_passage",
        "target": "",
        "notes": "Share completing congressional passage under the conservative census definition; reported without a separate calibration target.",
    },
]

VOTEVIEW_METRICS = [
    {
        "metric": "coalitionSize",
        "target": "party-unity-support-band",
        "notes": "Mean winning-side share by roll call.",
    },
    {
        "metric": "partyUnity",
        "target": "",
        "notes": "Mean within-party majority vote share by roll call; reported without a simulator tolerance target.",
    },
]

SPONSOR_METRICS = [
    {
        "metric": "sponsorIntroductionGini",
        "target": "sponsor-success-concentration",
        "notes": "Gini concentration of introduced bills by sponsor.",
    },
    {
        "metric": "sponsorSuccessGini",
        "target": "",
        "notes": "Gini concentration of enacted bills by sponsor; reported only because the bounded sample has no enacted sponsor successes.",
    },
]

CAMPAIGN_METRICS = [
    {
        "metric": "recipientFinanceGini",
        "target": "campaign-finance-observable-band",
        "notes": "Gini concentration of campaign money by recipient.",
    },
    {
        "metric": "outsideSpendingShare",
        "target": "campaign-finance-observable-band",
        "notes": "Share of campaign money marked as independent expenditure.",
    },
]

DISTRICT_METRICS = [
    {
        "metric": "intensityWeightedSupport",
        "target": "district-public-will-alignment",
        "notes": "District support weighted by issue intensity and turnout.",
    },
    {
        "metric": "turnoutGini",
        "target": "district-turnout-skew-proxy",
        "notes": "Turnout concentration across district-issue rows.",
    },
]

COURT_METRICS = [
    {
        "metric": "invalidationRate",
        "target": "judicial-review-constraint",
        "notes": "Share of SCDB merits cases invalidating the challenged action.",
    },
    {
        "metric": "signedOpinionRate",
        "target": "",
        "notes": "Share of SCDB merits cases coded as signed opinions; reported without a simulator tolerance target.",
    },
]

RULEMAKING_METRICS = [
    {
        "metric": "meanFinalToEffectiveDays",
        "target": "implementation-delay-proxy",
        "notes": "Mean days between Federal Register final-rule publication and effective date.",
    },
    {
        "metric": "effectiveDateCoverage",
        "target": "",
        "notes": "Share of final-rule rows with effective-date coverage; reported as source completeness.",
    },
    {
        "metric": "meanEnforcementCapacity",
        "target": "implementation-capacity-proxy",
        "notes": "Mean encoded implementation-speed or enforcement-capacity proxy where available.",
    },
]

LAW_REVISION_METRICS = [
    {
        "metric": "postEnactmentCorrectionRate",
        "target": "law-revision-correction-proxy",
        "notes": "Share of public-law rows with amendment, reauthorization, repeal, expiration, or invalidation flags.",
    },
    {
        "metric": "repealRate",
        "target": "",
        "notes": "Share of public-law rows with repeal text flags; reported without a simulator tolerance target.",
    },
]

COMPARATIVE_METRICS = [
    {
        "metric": "bicameralShare",
        "target": "bicameral-veto-burden",
        "notes": "Share of comparative country-year rows with two or more chambers.",
    },
    {
        "metric": "meanJudicialReviewStrength",
        "target": "",
        "notes": "Mean encoded judicial-review strength; reported as comparative context.",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str) -> bool:
    return value.strip().lower() in TRUE_VALUES


def stable_hash_heldout(value: str) -> bool:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 2 == 0


def bill_rate(rows: list[dict[str, str]], column: str) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if truthy(row.get(column, ""))) / len(rows)


def numeric(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def gini(values: list[float]) -> float:
    values = sorted(max(0.0, value) for value in values)
    if not values or sum(values) == 0.0:
        return 0.0
    weighted = sum((index + 1) * value for index, value in enumerate(values))
    return ((2.0 * weighted) / (len(values) * sum(values))) - ((len(values) + 1.0) / len(values))


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip()[:10])
    except (TypeError, ValueError):
        return None


def days_between(start: str, end: str) -> float | None:
    start_date = parse_date(start)
    end_date = parse_date(end)
    if start_date is None or end_date is None:
        return None
    return max(0, (end_date - start_date).days)


def voteview_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    grouped: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    by_vote: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
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
    return {
        "partyUnity": sum(unity) / len(unity) if unity else 0.0,
        "coalitionSize": sum(coalition) / len(coalition) if coalition else 0.0,
    }


def sponsor_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    introduced = [numeric(row.get("introduced", "")) for row in rows]
    enacted = [numeric(row.get("enacted", "")) for row in rows]
    return {
        "sponsorIntroductionGini": gini(introduced),
        "sponsorSuccessGini": gini(enacted),
    }


def campaign_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    by_recipient: dict[str, float] = defaultdict(float)
    independent_total = 0.0
    total = 0.0
    for row in rows:
        amount = numeric(row.get("amount", ""))
        total += amount
        by_recipient[row["recipient"]] += amount
        if truthy(row.get("independent_expenditure", "")):
            independent_total += amount
    return {
        "recipientFinanceGini": gini(list(by_recipient.values())),
        "outsideSpendingShare": independent_total / total if total else 0.0,
    }


def district_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    supports = [numeric(row.get("support", "")) for row in rows]
    intensities = [numeric(row.get("intensity", "")) for row in rows]
    turnouts = [numeric(row.get("turnout", "")) for row in rows]
    weighted_support = sum(s * max(0.0, i) * max(0.0, t) for s, i, t in zip(supports, intensities, turnouts))
    weight = sum(max(0.0, i) * max(0.0, t) for i, t in zip(intensities, turnouts))
    return {
        "intensityWeightedSupport": weighted_support / weight if weight else 0.0,
        "turnoutGini": gini(turnouts),
    }


def court_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    total = len(rows)
    invalidated = sum(1 for row in rows if truthy(row.get("invalidated", "")))
    signed = sum(1 for row in rows if truthy(row.get("signed_opinion", "")))
    return {
        "invalidationRate": invalidated / total if total else 0.0,
        "signedOpinionRate": signed / total if total else 0.0,
    }


def rulemaking_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    final_to_effective = [
        value for value in (
            days_between(row.get("final_rule_date", ""), row.get("effective_date", ""))
            for row in rows
        )
        if value is not None
    ]
    effective_date_rows = sum(1 for row in rows if row.get("effective_date", "").strip())
    capacities = [numeric(row.get("enforcement_capacity", "")) for row in rows if row.get("enforcement_capacity", "").strip()]
    total = len(rows)
    return {
        "meanFinalToEffectiveDays": mean(final_to_effective),
        "effectiveDateCoverage": effective_date_rows / total if total else 0.0,
        "meanEnforcementCapacity": mean(capacities),
    }


def law_revision_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    total = len(rows)
    correction = sum(
        1
        for row in rows
        if any(truthy(row.get(column, "")) for column in ("amended", "reauthorized", "repealed", "expired", "invalidated"))
    )
    repealed = sum(1 for row in rows if truthy(row.get("repealed", "")))
    return {
        "postEnactmentCorrectionRate": correction / total if total else 0.0,
        "repealRate": repealed / total if total else 0.0,
    }


def comparative_metric_values(rows: list[dict[str, str]]) -> dict[str, float]:
    chambers = [numeric(row.get("chambers", "")) for row in rows]
    review = [numeric(row.get("judicial_review", "")) for row in rows]
    return {
        "bicameralShare": sum(1 for value in chambers if value >= 2.0) / len(chambers) if chambers else 0.0,
        "meanJudicialReviewStrength": mean(review),
    }


def read_calibration() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in read_csv(CALIBRATION):
        result[row["key"]] = row
    return result


def status(value: float, target: dict[str, str] | None) -> str:
    if target is None:
        return "reported"
    minimum = float(target["minimum"])
    maximum = float(target["maximum"])
    return "pass" if minimum <= value <= maximum else "outside tolerance"


def bill_output(calibration_targets: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    data = read_csv(BILL_CENSUS_RAW)
    if not data:
        raise SystemExit(
            f"{BILL_CENSUS_RAW} is missing or empty; run make build-govinfo-bill-census-raw first."
        )
    calibration_rows = [row for row in data if not stable_hash_heldout(row.get("bill_id", ""))]
    heldout_rows = [row for row in data if stable_hash_heldout(row.get("bill_id", ""))]
    if not calibration_rows or not heldout_rows:
        raise SystemExit("Bill held-out split produced an empty slice; check bill_id values.")

    output: list[dict[str, str]] = []
    for spec in BILL_METRICS:
        target_key = spec["target"]
        target = calibration_targets.get(target_key) if target_key else None
        calibration_value = bill_rate(calibration_rows, spec["column"])
        heldout_value = bill_rate(heldout_rows, spec["column"])
        all_value = bill_rate(data, spec["column"])
        output.append({
            "sourceFamily": "govinfo bill and action records",
            "dataset": BILL_CENSUS_RAW.name,
            "splitMethod": "sha256(bill_id) first32bits mod 2 equals 0 held out",
            "totalRows": str(len(data)),
            "calibrationRows": str(len(calibration_rows)),
            "heldoutRows": str(len(heldout_rows)),
            "totalUnits": str(len(data)),
            "calibrationUnits": str(len(calibration_rows)),
            "heldoutUnits": str(len(heldout_rows)),
            "unit": "bill",
            "metric": spec["metric"],
            "calibrationValue": f"{calibration_value:.6f}",
            "heldoutValue": f"{heldout_value:.6f}",
            "allValue": f"{all_value:.6f}",
            "trainHeldoutAbsDelta": f"{abs(calibration_value - heldout_value):.6f}",
            "calibrationTarget": target_key,
            "simulatorScenario": "" if target is None else target["scenarioKey"],
            "simulatorMetric": "" if target is None else target["metric"],
            "simulatorObserved": "" if target is None else target["observed"],
            "targetMinimum": "" if target is None else target["minimum"],
            "targetMaximum": "" if target is None else target["maximum"],
            "heldoutTargetStatus": status(heldout_value, target),
            "boundaryCategory": "held-out benchmark",
            "notes": spec["notes"],
        })
    return output


def voteview_output(calibration_targets: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    data = read_csv(VOTEVIEW_RAW)
    if not data:
        raise SystemExit(f"{VOTEVIEW_RAW} is missing or empty; run make build-core-raw-validation first.")
    calibration_rows = [row for row in data if not stable_hash_heldout(row.get("vote_id", ""))]
    heldout_rows = [row for row in data if stable_hash_heldout(row.get("vote_id", ""))]
    if not calibration_rows or not heldout_rows:
        raise SystemExit("Voteview held-out split produced an empty slice; check vote_id values.")

    calibration_metrics = voteview_metric_values(calibration_rows)
    heldout_metrics = voteview_metric_values(heldout_rows)
    all_metrics = voteview_metric_values(data)
    all_votes = {row["vote_id"] for row in data}
    calibration_votes = {row["vote_id"] for row in calibration_rows}
    heldout_votes = {row["vote_id"] for row in heldout_rows}

    output: list[dict[str, str]] = []
    for spec in VOTEVIEW_METRICS:
        target_key = spec["target"]
        target = calibration_targets.get(target_key) if target_key else None
        calibration_value = calibration_metrics[spec["metric"]]
        heldout_value = heldout_metrics[spec["metric"]]
        all_value = all_metrics[spec["metric"]]
        output.append({
            "sourceFamily": "Voteview roll-call data",
            "dataset": VOTEVIEW_RAW.name,
            "splitMethod": "sha256(vote_id) first32bits mod 2 equals 0 held out",
            "totalRows": str(len(data)),
            "calibrationRows": str(len(calibration_rows)),
            "heldoutRows": str(len(heldout_rows)),
            "totalUnits": str(len(all_votes)),
            "calibrationUnits": str(len(calibration_votes)),
            "heldoutUnits": str(len(heldout_votes)),
            "unit": "roll call",
            "metric": spec["metric"],
            "calibrationValue": f"{calibration_value:.6f}",
            "heldoutValue": f"{heldout_value:.6f}",
            "allValue": f"{all_value:.6f}",
            "trainHeldoutAbsDelta": f"{abs(calibration_value - heldout_value):.6f}",
            "calibrationTarget": target_key,
            "simulatorScenario": "" if target is None else target["scenarioKey"],
            "simulatorMetric": "" if target is None else target["metric"],
            "simulatorObserved": "" if target is None else target["observed"],
            "targetMinimum": "" if target is None else target["minimum"],
            "targetMaximum": "" if target is None else target["maximum"],
            "heldoutTargetStatus": status(heldout_value, target),
            "boundaryCategory": "held-out benchmark",
            "notes": spec["notes"],
        })
    return output


def sponsor_output(calibration_targets: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    data = read_csv(SPONSOR_RAW)
    if not data:
        raise SystemExit(f"{SPONSOR_RAW} is missing or empty; run make build-core-raw-validation first.")
    calibration_rows = [row for row in data if not stable_hash_heldout(row.get("sponsor_id", ""))]
    heldout_rows = [row for row in data if stable_hash_heldout(row.get("sponsor_id", ""))]
    if not calibration_rows or not heldout_rows:
        raise SystemExit("Sponsor held-out split produced an empty slice; check sponsor_id values.")

    calibration_metrics = sponsor_metric_values(calibration_rows)
    heldout_metrics = sponsor_metric_values(heldout_rows)
    all_metrics = sponsor_metric_values(data)

    output: list[dict[str, str]] = []
    for spec in SPONSOR_METRICS:
        target_key = spec["target"]
        target = calibration_targets.get(target_key) if target_key else None
        calibration_value = calibration_metrics[spec["metric"]]
        heldout_value = heldout_metrics[spec["metric"]]
        all_value = all_metrics[spec["metric"]]
        output.append({
            "sourceFamily": "Center for Effective Lawmaking and sponsor histories",
            "dataset": SPONSOR_RAW.name,
            "splitMethod": "sha256(sponsor_id) first32bits mod 2 equals 0 held out",
            "totalRows": str(len(data)),
            "calibrationRows": str(len(calibration_rows)),
            "heldoutRows": str(len(heldout_rows)),
            "totalUnits": str(len(data)),
            "calibrationUnits": str(len(calibration_rows)),
            "heldoutUnits": str(len(heldout_rows)),
            "unit": "sponsor",
            "metric": spec["metric"],
            "calibrationValue": f"{calibration_value:.6f}",
            "heldoutValue": f"{heldout_value:.6f}",
            "allValue": f"{all_value:.6f}",
            "trainHeldoutAbsDelta": f"{abs(calibration_value - heldout_value):.6f}",
            "calibrationTarget": target_key,
            "simulatorScenario": "" if target is None else target["scenarioKey"],
            "simulatorMetric": "" if target is None else target["metric"],
            "simulatorObserved": "" if target is None else target["observed"],
            "targetMinimum": "" if target is None else target["minimum"],
            "targetMaximum": "" if target is None else target["maximum"],
            "heldoutTargetStatus": status(heldout_value, target),
            "boundaryCategory": "held-out benchmark",
            "notes": spec["notes"],
        })
    return output


def source_family_output(
        raw_path: Path,
        source_family: str,
        key_column: str,
        unit: str,
        metrics: list[dict[str, str]],
        metric_values,
        calibration_targets: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    data = read_csv(raw_path)
    if not data:
        raise SystemExit(f"{raw_path} is missing or empty; run its raw-data build target first.")
    calibration_rows = [row for row in data if not stable_hash_heldout(row.get(key_column, ""))]
    heldout_rows = [row for row in data if stable_hash_heldout(row.get(key_column, ""))]
    if not calibration_rows or not heldout_rows:
        raise SystemExit(f"{source_family} held-out split produced an empty slice; check {key_column} values.")

    calibration_metrics = metric_values(calibration_rows)
    heldout_metrics = metric_values(heldout_rows)
    all_metrics = metric_values(data)
    all_units = {row.get(key_column, "") for row in data}
    calibration_units = {row.get(key_column, "") for row in calibration_rows}
    heldout_units = {row.get(key_column, "") for row in heldout_rows}

    output: list[dict[str, str]] = []
    for spec in metrics:
        target_key = spec["target"]
        target = calibration_targets.get(target_key) if target_key else None
        metric = spec["metric"]
        calibration_value = calibration_metrics[metric]
        heldout_value = heldout_metrics[metric]
        all_value = all_metrics[metric]
        output.append({
            "sourceFamily": source_family,
            "dataset": raw_path.name,
            "splitMethod": f"sha256({key_column}) first32bits mod 2 equals 0 held out",
            "totalRows": str(len(data)),
            "calibrationRows": str(len(calibration_rows)),
            "heldoutRows": str(len(heldout_rows)),
            "totalUnits": str(len(all_units)),
            "calibrationUnits": str(len(calibration_units)),
            "heldoutUnits": str(len(heldout_units)),
            "unit": unit,
            "metric": metric,
            "calibrationValue": f"{calibration_value:.6f}",
            "heldoutValue": f"{heldout_value:.6f}",
            "allValue": f"{all_value:.6f}",
            "trainHeldoutAbsDelta": f"{abs(calibration_value - heldout_value):.6f}",
            "calibrationTarget": target_key,
            "simulatorScenario": "" if target is None else target["scenarioKey"],
            "simulatorMetric": "" if target is None else target["metric"],
            "simulatorObserved": "" if target is None else target["observed"],
            "targetMinimum": "" if target is None else target["minimum"],
            "targetMaximum": "" if target is None else target["maximum"],
            "heldoutTargetStatus": status(heldout_value, target),
            "boundaryCategory": "held-out benchmark",
            "notes": spec["notes"],
        })
    return output


def write_reports(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    pass_count = sum(1 for row in rows if row["heldoutTargetStatus"] == "pass")
    target_count = sum(1 for row in rows if row["heldoutTargetStatus"] != "reported")
    lines = [
        "# Empirical Held-Out Benchmarks",
        "",
        "This report runs deterministic held-out checks on committed raw empirical samples. These are source-family benchmarks for legislative flow, roll-call behavior, sponsor proposal access, campaign-finance concentration, district public-will proxies, court review, implementation delay, law revision, and comparative institutional context. They are not validation of public benefit, welfare, bill-specific public support, harm, capture, representation, or institutional rankings.",
        "",
        f"- Source families with held-out rows: {len({row['sourceFamily'] for row in rows})}",
        f"- Targeted held-out checks passing: {pass_count} / {target_count}",
        "",
        "| Source family | Metric | Calibration slice | Held-out slice | All rows | Units | Simulator observed | Target range | Status |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        target_range = "---"
        observed = "---"
        if row["targetMinimum"] and row["targetMaximum"]:
            target_range = f"{row['targetMinimum']}--{row['targetMaximum']}"
            observed = row["simulatorObserved"]
        lines.append(
            f"| {row['sourceFamily']} | {row['metric']} | {row['calibrationValue']} | "
            f"{row['heldoutValue']} | {row['allValue']} | {row['calibrationUnits']} / "
            f"{row['heldoutUnits']} {row['unit']}s | {observed} | {target_range} | "
            f"{row['heldoutTargetStatus']} |"
        )
    lines.extend([
        "",
        "Boundary notes:",
        "",
        "- The deterministic GovInfo held-out rows remain within the 117th Congress. The separate complete 116th and 118th censuses supply external no-refit temporal transport tests and are reported independently so neither can enter calibration selection.",
        "- Voteview roll-call rows support held-out coalition-size and party-unity plausibility only; they do not validate district public opinion, representation, or generated public benefit.",
        "- Sponsor rows support held-out proposal-access concentration benchmarking only; they do not validate full member effectiveness or bill-level sponsor success.",
        "- Campaign-finance rows support held-out concentration and outside-spending observability only; they do not validate bill-level influence or capture.",
        "- District public-opinion rows support held-out district proxy stability only; they do not validate bill-topic support, MRP estimates, or affected-group harm.",
        "- Court-review rows support held-out merits-case invalidation plausibility only; they do not validate emergency-order behavior or lower-court review.",
        "- Rulemaking rows support held-out final-to-effective-delay plausibility only; they do not validate comments, enforcement, underfunding, or proposed-rule linkage.",
        "- Law-revision rows support held-out text-flag correction plausibility only; they do not validate full statutory lineage or codified-text diffs.",
        "- Comparative-institution rows support held-out bicameral-context plausibility only; they do not validate cross-national productivity or institutional fit.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    calibration_targets = read_calibration()
    output = (
        bill_output(calibration_targets)
        + voteview_output(calibration_targets)
        + sponsor_output(calibration_targets)
        + source_family_output(
            CAMPAIGN_RAW,
            "OpenFEC campaign finance",
            "source_id",
            "transaction",
            CAMPAIGN_METRICS,
            campaign_metric_values,
            calibration_targets,
        )
        + source_family_output(
            DISTRICT_RAW,
            "District public opinion and affected groups",
            "district_id",
            "district",
            DISTRICT_METRICS,
            district_metric_values,
            calibration_targets,
        )
        + source_family_output(
            COURT_RAW,
            "Court review and invalidation",
            "case_id",
            "case",
            COURT_METRICS,
            court_metric_values,
            calibration_targets,
        )
        + source_family_output(
            RULEMAKING_RAW,
            "Rulemaking implementation and enforcement",
            "law_id",
            "final rule",
            RULEMAKING_METRICS,
            rulemaking_metric_values,
            calibration_targets,
        )
        + source_family_output(
            LAW_REVISION_RAW,
            "Statutory revision and law lineage",
            "law_id",
            "public law",
            LAW_REVISION_METRICS,
            law_revision_metric_values,
            calibration_targets,
        )
        + source_family_output(
            COMPARATIVE_RAW,
            "QoG and V-Dem comparative institutions",
            "country",
            "country-year",
            COMPARATIVE_METRICS,
            comparative_metric_values,
            calibration_targets,
        )
    )
    write_reports(output)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
