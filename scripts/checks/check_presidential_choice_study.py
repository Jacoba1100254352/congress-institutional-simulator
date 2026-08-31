#!/usr/bin/env python3
"""Hard checks for the locked presidential-choice temporal transport study."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


BILL_PANEL = Path("data/validation/raw/govinfo_executive_action_panel.csv")
JOINT_PANEL = Path("data/validation/raw/govinfo_joint_resolution_panel.csv")
FINAL_VOTE_PANEL = Path("data/validation/raw/govinfo_final_chamber_vote_panel.csv")
SPECIFICATION = Path(
    "papers/empirical-validation/presidential-choice-study-specification.md"
)
IMPLEMENTATION = Path("scripts/validation/write_presidential_choice_study.py")
METRICS = Path("reports/presidential-choice-study-metrics.csv")
COEFFICIENTS = Path("reports/presidential-choice-study-coefficients.csv")
PREDICTIONS = Path("reports/presidential-choice-study-predictions.csv")
REPORT = Path("reports/presidential-choice-study.md")
METADATA = Path("reports/presidential-choice-study-metadata.json")
README = Path("README.md")
MAIN_MANUSCRIPT = Path("paper/acm-ci-framework/acm-ci-framework.tex")
TECHNICAL_APPENDIX = Path("paper/technical-appendix/odd-d-appendix.tex")
EMPIRICAL_LINKAGE_REPORT = Path("reports/empirical-linkage-report.md")
EMPIRICAL_GAP_REPORT = Path("reports/empirical-validation-gap-report.md")
EXECUTIVE_DIAGNOSTIC = Path("reports/legislative-executive-action-diagnostic.md")

EXPECTED_SPECIFICATION_SHA256 = (
    "b251e967787c01c8f48385d064d7a82a9e792aba48b1b6d946ba6931772d6256"
)
EXPECTED_SOURCE_HASHES = {
    str(BILL_PANEL): "d9241abd003919841e97464d6d1e5d79a85820517d72215adbdcdd7f17dd3c54",
    str(JOINT_PANEL): "d834c32834e2bf78e9ff36ab8b3c39016fd08013297a81980ff35c50c4038d57",
    str(FINAL_VOTE_PANEL): "539c497f8a6f0349fe284048228d652cb43cd9da42bec77da15ba72e63ed149c",
}
EXPECTED_SOURCE_ROWS = {
    str(BILL_PANEL): 4021,
    str(JOINT_PANEL): 187,
    str(FINAL_VOTE_PANEL): 8416,
}
EXPECTED_METRICS = {
    ("secondary_116", "M0"): (
        "0.145942382199",
        "0.027960225397",
        "-0.020835636562",
    ),
    ("secondary_116", "M1"): (
        "0.062968834227",
        "0.016533047710",
        "-0.012114527605",
    ),
    ("secondary_116", "M2"): (
        "0.038737685429",
        "0.010357463518",
        "0.000907854754",
    ),
    ("secondary_116", "SIM"): (
        "0.315093726262",
        "0.075278724201",
        "0.218523734535",
    ),
    ("primary_118", "M0"): (
        "0.223369075904",
        "0.044585808506",
        "-0.036624909915",
    ),
    ("primary_118", "M1"): (
        "0.058347134086",
        "0.015232313351",
        "-0.011633635795",
    ),
    ("primary_118", "M2"): (
        "0.026976966127",
        "0.008143260977",
        "0.003149381508",
    ),
    ("primary_118", "SIM"): (
        "0.334020540931",
        "0.083869317848",
        "0.201556179185",
    ),
}
EXPECTED_PRIMARY_M2_COEFFICIENTS = {
    "intercept": "-6.765604163196",
    "joint_resolution": "0.254952346265",
    "divided_government": "0.017018696529",
    "opposition_party_sponsor": "0.662335990801",
    "other_or_unknown_sponsor": "0.109729512278",
    "any_final_roll_call": "-0.517199625303",
    "both_final_roll_calls": "0.505274969246",
    "minimum_observed_final_support": "-1.721300439883",
    "minimum_observed_opposition_support": "2.220548887014",
}
EXPECTED_MODEL_FEATURES = {
    "M1": {
        "intercept",
        "joint_resolution",
        "divided_government",
        "opposition_party_sponsor",
        "other_or_unknown_sponsor",
        "any_final_roll_call",
        "both_final_roll_calls",
    },
    "M2": set(EXPECTED_PRIMARY_M2_COEFFICIENTS),
}
PROBABILITY_FIELDS = {
    "M0": "m0Probability",
    "M1": "m1Probability",
    "M2": "m2Probability",
    "SIM": "simulatorConstantProbability",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.exists(), f"Missing required artifact: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate(rows: list[dict[str, str]], probability_field: str) -> tuple[float, float, float]:
    probabilities = [float(row[probability_field]) for row in rows]
    outcomes = [int(row["vetoed"]) for row in rows]
    require(all(0.0 < value < 1.0 for value in probabilities), "Invalid probability.")
    log_loss = math.fsum(
        -outcome * math.log(probability)
        - (1 - outcome) * math.log1p(-probability)
        for outcome, probability in zip(outcomes, probabilities)
    ) / len(rows)
    brier = math.fsum(
        (probability - outcome) ** 2
        for outcome, probability in zip(outcomes, probabilities)
    ) / len(rows)
    calibration = math.fsum(probabilities) / len(rows) - math.fsum(outcomes) / len(rows)
    return log_loss, brier, calibration


def check_source_and_specification_hashes() -> None:
    require(
        sha256_file(SPECIFICATION) == EXPECTED_SPECIFICATION_SHA256,
        "Locked presidential-choice specification hash drifted.",
    )
    for path_text, expected_hash in EXPECTED_SOURCE_HASHES.items():
        path = Path(path_text)
        require(sha256_file(path) == expected_hash, f"Source-panel hash drifted: {path}")
        require(
            len(read_csv(path)) == EXPECTED_SOURCE_ROWS[path_text],
            f"Source-panel row count drifted: {path}",
        )


def check_metrics_and_predictions() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    metrics = read_csv(METRICS)
    predictions = read_csv(PREDICTIONS)
    require(len(metrics) == 8, "Presidential-choice metric row count drifted.")
    require(len(predictions) == 640, "Presidential-choice prediction row count drifted.")
    metrics_by_key = {(row["splitId"], row["modelId"]): row for row in metrics}
    require(set(metrics_by_key) == set(EXPECTED_METRICS), "Study model/split set drifted.")
    predictions_by_split: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in predictions:
        predictions_by_split[row["splitId"]].append(row)
    require(
        {key: len(value) for key, value in predictions_by_split.items()}
        == {"secondary_116": 353, "primary_118": 287},
        "Prediction split counts drifted.",
    )
    require(
        len({(row["splitId"], row["billId"]) for row in predictions}) == 640,
        "Prediction bill IDs are not unique within split.",
    )
    require(
        sum(int(row["vetoed"]) for row in predictions_by_split["secondary_116"]) == 10
        and sum(int(row["vetoed"]) for row in predictions_by_split["primary_118"]) == 13,
        "Prediction event counts drifted.",
    )

    for key, expected in EXPECTED_METRICS.items():
        row = metrics_by_key[key]
        require(
            (row["meanLogLoss"], row["brierScore"], row["calibrationInTheLarge"])
            == expected,
            f"Frozen metric drifted: {key}",
        )
        recomputed = evaluate(predictions_by_split[key[0]], PROBABILITY_FIELDS[key[1]])
        reported = tuple(float(value) for value in expected)
        require(
            all(abs(left - right) <= 1e-9 for left, right in zip(recomputed, reported)),
            f"Prediction arithmetic does not reproduce metrics: {key}",
        )

    primary_m0 = metrics_by_key[("primary_118", "M0")]
    primary_m2 = metrics_by_key[("primary_118", "M2")]
    require(primary_m2["primaryGateStatus"] == "pass", "Primary gate status drifted.")
    require(
        primary_m2["gateLogLossStatus"] == "pass"
        and primary_m2["gateCalibrationStatus"] == "pass",
        "Primary component gate status drifted.",
    )
    require(
        float(primary_m2["meanLogLoss"]) < float(primary_m0["meanLogLoss"]),
        "Primary M2 no longer improves log loss.",
    )
    require(
        abs(float(primary_m2["calibrationInTheLarge"])) <= 0.020,
        "Primary M2 no longer meets the locked calibration tolerance.",
    )
    require(
        float(primary_m2["fitGradientInfinityNorm"]) <= 1e-9
        and float(primary_m2["fitStepInfinityNorm"]) <= 1e-10,
        "Primary fit no longer meets solver tolerances.",
    )
    for split_rows in predictions_by_split.values():
        for row in split_rows:
            any_roll = row["anyFinalRollCall"] == "1"
            require(
                bool(row["minimumObservedFinalSupport"]) == any_roll,
                f"{row['billId']}: final support missingness drifted",
            )
            require(
                bool(row["minimumObservedOppositionSupport"]) == any_roll,
                f"{row['billId']}: opposition support missingness drifted",
            )
            require(
                (row["bothFinalRollCalls"] == "1")
                <= (row["anyFinalRollCall"] == "1"),
                f"{row['billId']}: invalid vote-coverage indicator",
            )
    return metrics, predictions


def check_prediction_source_alignment(predictions: list[dict[str, str]]) -> None:
    decisions = {
        row["bill_id"]: row for row in read_csv(BILL_PANEL) + read_csv(JOINT_PANEL)
    }
    vote_rows: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(FINAL_VOTE_PANEL):
        vote_rows[row["bill_id"]].append(row)
    for prediction in predictions:
        bill_id = prediction["billId"]
        decision = decisions[bill_id]
        require(
            decision["congress"] == prediction["testCongress"],
            f"{bill_id}: prediction Congress mismatch",
        )
        require(
            decision["vetoed"] == prediction["vetoed"],
            f"{bill_id}: prediction outcome mismatch",
        )
        expected_class = (
            "joint_resolution"
            if decision["bill_type"] in {"hjres", "sjres"}
            else "bill"
        )
        require(
            prediction["measureClass"] == expected_class,
            f"{bill_id}: prediction measure class mismatch",
        )
        recorded = [
            row
            for row in vote_rows[bill_id]
            if row["selection_status"] == "official_roll_call_selected"
        ]
        expected_chambers = "|".join(row["chamber"] for row in recorded)
        require(
            prediction["recordedFinalChambers"] == expected_chambers,
            f"{bill_id}: prediction chamber coverage mismatch",
        )
        if recorded:
            expected_support = min(float(row["support_share"]) for row in recorded)
            expected_opposition = min(
                float(row["opposition_party_support_share"]) for row in recorded
            )
            require(
                abs(float(prediction["minimumObservedFinalSupport"]) - expected_support)
                <= 5e-13,
                f"{bill_id}: prediction final support mismatch",
            )
            require(
                abs(
                    float(prediction["minimumObservedOppositionSupport"])
                    - expected_opposition
                )
                <= 5e-13,
                f"{bill_id}: prediction opposition support mismatch",
            )


def check_coefficients() -> None:
    rows = read_csv(COEFFICIENTS)
    require(len(rows) == 32, "Presidential-choice coefficient row count drifted.")
    require(
        len({(row["splitId"], row["modelId"], row["feature"]) for row in rows})
        == 32,
        "Coefficient keys are not unique.",
    )
    for split in ("secondary_116", "primary_118"):
        for model in ("M1", "M2"):
            subset = [
                row for row in rows if row["splitId"] == split and row["modelId"] == model
            ]
            require(
                {row["feature"] for row in subset} == EXPECTED_MODEL_FEATURES[model],
                f"{split}/{model}: feature set drifted",
            )
            require(
                all(row["featureStatus"].startswith("fitted") for row in subset),
                f"{split}/{model}: unexpected omitted feature",
            )
            require(
                all(row["penaltyLambda"] == "0.160000000000" for row in subset),
                f"{split}/{model}: penalty drifted",
            )
    primary = {
        row["feature"]: row["standardizedCoefficient"]
        for row in rows
        if row["splitId"] == "primary_118" and row["modelId"] == "M2"
    }
    require(
        primary == EXPECTED_PRIMARY_M2_COEFFICIENTS,
        "Primary M2 coefficients drifted.",
    )


def check_metadata_and_report() -> None:
    require(METADATA.exists(), f"Missing required artifact: {METADATA}")
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    require(metadata["studyVersion"] == "presidential-choice-transport-v1", "Study version drifted.")
    require(
        metadata["specification"]["sha256"] == EXPECTED_SPECIFICATION_SHA256,
        "Metadata specification hash drifted.",
    )
    require(
        metadata["implementation"]["sha256"] == sha256_file(IMPLEMENTATION),
        "Metadata implementation hash is stale.",
    )
    sources = {row["path"]: row for row in metadata["sources"]}
    require(set(sources) == set(EXPECTED_SOURCE_HASHES), "Metadata source set drifted.")
    for path, expected_hash in EXPECTED_SOURCE_HASHES.items():
        require(sources[path]["sha256"] == expected_hash, f"Metadata source hash drifted: {path}")
        require(
            sources[path]["rowsExcludingHeader"] == EXPECTED_SOURCE_ROWS[path],
            f"Metadata source row count drifted: {path}",
        )
    outputs = {row["path"]: row["sha256"] for row in metadata["outputs"]}
    expected_outputs = {str(path) for path in (METRICS, COEFFICIENTS, PREDICTIONS, REPORT)}
    require(set(outputs) == expected_outputs, "Metadata output set drifted.")
    for path, expected_hash in outputs.items():
        require(sha256_file(Path(path)) == expected_hash, f"Stale output hash: {path}")
    require(metadata["primaryGate"]["status"] == "pass", "Metadata primary gate drifted.")
    require(
        metadata["postFitConcentrationDiagnostic"]
        == {
            "billMeasures": 270,
            "billVetoes": 1,
            "jointResolutionMeasures": 17,
            "jointResolutionVetoes": 12,
            "lowestRankedVetoPosition": 16,
            "primaryMeasures": 287,
            "primaryVetoes": 13,
            "status": "post_fit_descriptive_not_gate",
            "vetoesAmongTop13Predictions": 12,
        },
        "Post-fit concentration diagnostic drifted.",
    )
    report = REPORT.read_text(encoding="utf-8")
    for snippet in (
        "Primary locked gate: **PASS**.",
        "This diagnostic was computed after fitting.",
        "12 vetoes among 17 joint resolutions",
        "not estimate causal presidential behavior",
        "simulator constant remains a scale diagnostic",
    ):
        require(snippet in report, f"Presidential-choice report lost boundary text: {snippet}")


def check_publication_claims() -> None:
    required_snippets = {
        README: (
            "The frozen simulator veto rate is 22.101 times their",
            "lowers log loss from 0.223369 to 0.026977",
            "Twelve of the 13 test vetoes occur among only 17 joint",
            "not causal model validation or broad out-of-regime validation",
        ),
        MAIN_MANUSCRIPT: (
            "combined empirical veto rate is 0.011169",
            "exact-count ratio of 22.101",
            "structural M1 ablation reaches log loss 0.058347 and Brier score 0.015232",
            "M2 reaches 0.026977 and 0.008143 versus 0.223369 and 0.044586",
            "M1 and M2 log losses are 0.062969 and 0.038738 versus 0.145942",
            "12 of 13 primary test vetoes among only 17 joint resolutions",
            "This is narrow predictive transport, not a blinded preregistration",
        ),
        TECHNICAL_APPENDIX: (
            "combined conditional veto rate is 0.011169",
            "22.101 times the combined empirical rate",
            "structural M1 ablation records primary log loss 0.058347 and Brier score 0.015232",
            "support model records 0.026977 and 0.008143 versus 0.223369 and 0.044586",
            "M1 and M2 log losses are 0.062969 and 0.038738 versus 0.145942",
            "12 of 13 primary test vetoes among only 17 joint resolutions",
            "not a blinded preregistration, a causal estimate",
        ),
        EMPIRICAL_LINKAGE_REPORT: (
            "log loss 0.026977 versus 0.223369",
            "the locked gate status is pass",
            "12 of the 13 test vetoes among only 17 joint resolutions",
            "not a causal estimate",
        ),
        EMPIRICAL_GAP_REPORT: (
            "log loss 0.026977 versus 0.223369",
            "the locked gate status is pass",
            "12 of the 13 test vetoes among only 17 joint resolutions",
            "replicate it in a future completed whole-Congress cohort",
        ),
        EXECUTIVE_DIAGNOSTIC: (
            "22.101 times the combined empirical rate",
            "log loss 0.026977 versus 0.223369",
            "12 of 13 test vetoes arise among only 17 joint resolutions",
            "does not retroactively convert the descriptive strata above into causal effects",
        ),
    }
    for path, snippets in required_snippets.items():
        require(path.exists(), f"Missing publication integration artifact: {path}")
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            require(
                snippet in text,
                f"Publication integration text drifted in {path}: {snippet}",
            )

    manuscript_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (README, MAIN_MANUSCRIPT, TECHNICAL_APPENDIX)
    ).lower()
    for stale_phrase in (
        "47.266",
        "joint resolutions are excluded",
        "pre-specified low-event presidential-choice",
    ):
        require(
            stale_phrase not in manuscript_text,
            f"Stale pre-study claim remains in publication text: {stale_phrase}",
        )


def main() -> None:
    check_source_and_specification_hashes()
    _, predictions = check_metrics_and_predictions()
    check_prediction_source_alignment(predictions)
    check_coefficients()
    check_metadata_and_report()
    check_publication_claims()
    print("Locked presidential-choice study checks passed.")


if __name__ == "__main__":
    main()
