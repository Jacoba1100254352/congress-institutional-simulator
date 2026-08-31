# Presidential-Choice Temporal Transport Study

Primary locked gate: **PASS**.

This report implements the post-source-audit, pre-fit specification in `papers/empirical-validation/presidential-choice-study-specification.md`. Specification SHA-256: `b251e967787c01c8f48385d064d7a82a9e792aba48b1b6d946ba6931772d6256`.

## Result

On the 118th-Congress test cohort, M2 has mean log loss 0.026976966127 versus 0.223369075904 for the training-prevalence baseline. Its calibration-in-the-large is 0.003149381508. The gate requires strictly lower log loss and absolute calibration-in-the-large no greater than 0.020.

On the secondary 116th-Congress check, M2 has mean log loss 0.038737685429 versus 0.145942382199 for the training-prevalence baseline and calibration-in-the-large 0.000907854754. This check does not determine the primary gate.

## Test Metrics

| Test Congress | Model | Log loss | Brier | Mean predicted | Observed rate | Calibration | Gate |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 116 | M0: training prevalence | 0.145942382199 | 0.027960225397 | 0.007492975336 | 0.028328611898 | -0.020835636562 | not_applicable |
| 116 | M1: structural penalized logistic | 0.062968834227 | 0.016533047710 | 0.016214084293 | 0.028328611898 | -0.012114527605 | not_applicable |
| 116 | M2: support penalized logistic | 0.038737685429 | 0.010357463518 | 0.029236466652 | 0.028328611898 | 0.000907854754 | not_applicable |
| 116 | SIM: frozen simulator constant | 0.315093726262 | 0.075278724201 | 0.246852346433 | 0.028328611898 | 0.218523734535 | not_applicable |
| 118 | M0: training prevalence | 0.223369075904 | 0.044585808506 | 0.008671257332 | 0.045296167247 | -0.036624909915 | not_applicable |
| 118 | M1: structural penalized logistic | 0.058347134086 | 0.015232313351 | 0.033662531453 | 0.045296167247 | -0.011633635795 | not_applicable |
| 118 | M2: support penalized logistic | 0.026976966127 | 0.008143260977 | 0.048445548755 | 0.045296167247 | 0.003149381508 | pass |
| 118 | SIM: frozen simulator constant | 0.334020540931 | 0.083869317848 | 0.246852346433 | 0.045296167247 | 0.201556179185 | not_applicable |

## Primary M2 Coefficients

Coefficients are on the training-standardized predictor scale. They are descriptive model parameters, not causal effects or significance tests.

| Feature | Status | Coefficient | Odds ratio per training SD |
| --- | --- | ---: | ---: |
| `intercept` | fitted_unpenalized | -6.765604163196 | NA |
| `joint_resolution` | fitted | 0.254952346265 | 1.290400127022 |
| `divided_government` | fitted | 0.017018696529 | 1.017164339590 |
| `opposition_party_sponsor` | fitted | 0.662335990801 | 1.939317274548 |
| `other_or_unknown_sponsor` | fitted | 0.109729512278 | 1.115976171778 |
| `any_final_roll_call` | fitted | -0.517199625303 | 0.596187761591 |
| `both_final_roll_calls` | fitted | 0.505274969246 | 1.657441203167 |
| `minimum_observed_final_support` | fitted | -1.721300439883 | 0.178833434499 |
| `minimum_observed_opposition_support` | fitted | 2.220548887014 | 9.212386037461 |

## Post-Fit Concentration Audit

This diagnostic was computed after fitting. It was not prespecified, does not alter the locked gate, and is included to prevent the aggregate score from being read as broad presidential-choice validation.

The 118th-Congress cohort contains 12 vetoes among 17 joint resolutions and 1 veto among 270 H.R./S. bills. Thus, 12 of the 13 test events arise from the small joint-resolution class.

Twelve vetoes appear among the 13 highest M2 probabilities, and all 13 appear by rank 16. The score improvement is therefore concentrated in a specific measure-class and final-vote pattern. Transport to a Congress with a different resolution mix or political process remains untested.

## Boundary

The final-vote pathway is informatively recorded: many measures have voice-vote or unanimous-consent final approvals, and those missing support values are retained rather than imputed. The model mixes H.R./S. measures with separately labeled joint resolutions because measure class is a locked predictor. Its probabilities describe temporal forecasting under the frozen source construction.

This study does not estimate causal presidential behavior, recover support behind nonrecorded votes, validate bill quality or public preferences, or validate the simulator's veto mechanism and institutional rankings. The simulator constant remains a scale diagnostic rather than a competing fitted bill-level model.

## Reproduction

Run `make presidential-choice-study`. The pipeline uses only committed source panels and Python's standard library. Source, specification, implementation, and output hashes are recorded in `reports/presidential-choice-study-metadata.json`.
